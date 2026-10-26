# -*- coding: utf-8 -*-
"""FastAPI app — read the index, serve the dashboard, write notes back to the
filesystem (source of truth) then reindex. Local-first, 127.0.0.1 only."""
from __future__ import annotations

import json
import math
import mimetypes as _mimetypes
import re
import time
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import authn as AUTH
from . import backup_status as BK
from . import cloudwrites as CW
from . import epct_status as EP
from . import iald_nativa as NAT
from . import orquestracao_status as ORQ
from . import torre as TORRE
from . import config as C
from . import devices as DEV
from . import security as SEC
from .compiler import compile_prompt
from .db import connect
from .reindex import _sha_text as REINDEX_SHA, check_integrity, reindex

# em modo access OU com o login da Central (nuvem/Render), desabilita /docs, /redoc e
# /openapi.json: esses paths ficam FORA do portão /api e anunciariam as rotas de admin.
_DOCS_OFF = SEC.IS_ACCESS or AUTH.AUTH_ENABLED
app = FastAPI(title="Central de Patentes TGL", version="0.1.0",
              docs_url=(None if _DOCS_OFF else "/docs"), redoc_url=None,
              openapi_url=(None if _DOCS_OFF else "/openapi.json"))
# CORS: NUNCA '*'. access -> a origem unica da Central (com credenciais p/ o cookie do Access);
# local -> apenas as origens de desenvolvimento (bloqueia exfiltracao drive-by de site malicioso).
if SEC.CORS_ORIGIN not in ("", "*"):
    _origins, _creds = [SEC.CORS_ORIGIN], True
else:
    _origins = ["http://localhost:5173", "http://127.0.0.1:5173",
                "http://localhost:8765", "http://127.0.0.1:8765"]
    _creds = False
# O SITE (iald.ia.br) chama o descompactador publico /api/acom/* (cross-origin, SEM cookie).
# Adiciona as origens do site a' allowlist — publicas e read-only; nenhuma rota credenciada
# depende disso (a UI da Central e' mesma-origem). Configuravel por CENTRAL_SITE_ORIGINS.
import os as _os  # noqa: E402
_site_origins = [o.strip() for o in _os.environ.get(
    "CENTRAL_SITE_ORIGINS", "https://iald.ia.br,https://www.iald.ia.br").split(",") if o.strip()]
_origins = list(dict.fromkeys(_origins + _site_origins))


class _CORSComExcecoes(CORSMiddleware):
    """CORS de sempre, EXCETO nas rotas da aba de usuários do app IALD: a sincronização
    (servidor-a-servidor, HMAC) e as rotas do operador (mesma origem) nunca recebem cabeçalho
    CORS nem resposta de preflight — um site irmão não consegue sequer negociar o acesso."""
    _SEM_CORS = ("/api/iald-sync/", "/api/iald-app/")

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and str(scope.get("path", "")).startswith(self._SEM_CORS):
            await self.app(scope, receive, send)
            return
        await super().__call__(scope, receive, send)


app.add_middleware(_CORSComExcecoes, allow_origins=_origins, allow_credentials=_creds,
                   allow_methods=["*"], allow_headers=["*", "X-Inscricao"],
                   expose_headers=["X-Acom-Report", "Content-Disposition"])
SEC.install_security(app)   # headers de seguranca + guard do Cloudflare Access + rate-limit + audit


@app.middleware("http")
async def crypto_auth_gate(request: Request, call_next):
    """Portão da CRIPTOGRAFIA DO OPERADOR (ACOM Crypto). Quando CENTRAL_AUTH=crypto, toda
    /api/* (exceto /api/auth/* e /api/health) exige o cookie de sessão válido.
    As recusas daqui saem com os mesmos cabeçalhos de segurança (HSTS/CSP) do resto.
    21/09/2026: (1) mutação vinda de OUTRA origem (subdomínio irmão incluso) é recusada antes
    do cookie — authn.recusa_csrf; (2) as recusas daqui (que ficam FORA do AuditMiddleware)
    entram no log geral com o ator do token — estranguladas; (3) o ator autenticado vai para
    request.state.identity, e o AuditMiddleware passa a registrar QUEM (não mais "local")."""
    if AUTH.AUTH_ENABLED:
        path = request.url.path
        motivo = AUTH.recusa_csrf(request.method, path, request.headers)
        if motivo:
            SEC.audit_negado(request, 403, motivo,
                             AUTH.token_payload(request.cookies.get(AUTH.COOKIE, "")), "csrf")
            return SEC.apply_security_headers(JSONResponse({"detail": motivo}, status_code=403))
        if not AUTH.is_open_path(path):
            payload = AUTH.token_payload(request.cookies.get(AUTH.COOKIE, ""))
            if payload is None:
                if AUTH.is_admin_only(path):
                    SEC.audit_negado(request, 401, "sem sessão", None, "admin")
                return SEC.apply_security_headers(JSONResponse(
                    {"detail": "não autenticado (login pela sua criptografia)"}, status_code=401))
            if not AUTH.can_request(payload, request.method, path):
                SEC.audit_negado(request, 403, "papel sem permissão", payload,
                                 "admin" if AUTH.is_admin_only(path) else "papel")
                return SEC.apply_security_headers(JSONResponse(
                    {"detail": "seu acesso é somente leitura (sem permissão para esta ação)"},
                    status_code=403))
            uid, papel = payload.get("uid") or payload.get("sub") or "?", payload.get("role") or "?"
            request.state.identity = {"email": f"{uid} ({papel})", "sub": uid, "mode": "crypto"}
    return await call_next(request)


if _DOCS_OFF:
    # sem isto, /docs e /redoc cairiam no fallback da SPA (200 com o index.html)
    @app.api_route("/docs", methods=["GET", "HEAD"], include_in_schema=False)
    @app.api_route("/docs/oauth2-redirect", methods=["GET", "HEAD"], include_in_schema=False)
    @app.api_route("/redoc", methods=["GET", "HEAD"], include_in_schema=False)
    @app.api_route("/openapi.json", methods=["GET", "HEAD"], include_in_schema=False)
    def _docs_desligados():
        raise HTTPException(404, "não encontrado")


@app.middleware("http")
async def cache_headers(request, call_next):
    """index.html nunca em cache (você sempre pega o bundle atual); assets com hash
    são imutáveis. Resolve na raiz o 'não vi a mudança' por bundle velho no navegador."""
    resp = await call_next(request)
    path = request.url.path
    if path == "/" or path.endswith(".html"):
        resp.headers["Cache-Control"] = "no-store, must-revalidate"
    elif path.startswith("/assets/"):
        resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return resp

URGENCY_SQL = """
  CASE
    WHEN d.status IN ('cumprido','prescrito','na') THEN 'cinza'
    WHEN d.due_date IS NULL THEN 'cinza'
    WHEN julianday(d.due_date) - julianday('now') < 0   THEN 'vencido'
    WHEN julianday(d.due_date) - julianday('now') <= 30  THEN 'vermelho'
    WHEN julianday(d.due_date) - julianday('now') <= 90  THEN 'laranja'
    WHEN julianday(d.due_date) - julianday('now') <= 180 THEN 'amarelo'
    ELSE 'verde' END
"""


def rows(cur) -> list[dict]:
    return [dict(r) for r in cur.fetchall()]


# ---------------- system ----------------
from fastapi import Request  # noqa: E402


@app.get("/api/whoami")
def whoami(request: Request):
    """Identidade autenticada (via Cloudflare Access / passkey) + estado da blindagem.
    Em modo local devolve o usuario local. Serve para a UI mostrar quem esta' logado."""
    ident = getattr(request.state, "identity", None) or SEC.identity_of(request)
    return {"identity": ident, "security": SEC.summary()}


@app.get("/api/audit")
def audit(request: Request, limit: int = 200):
    """Log de auditoria de acessos (quem entrou, quando, o que, resultado). Protegido pelo
    guard do Access como todo /api. Mostra tentativas negadas (403) tambem.
    21/09/2026: SÓ ADMIN (authn._ADMIN_ONLY_PREFIXES + guarda local) — o log carrega IPs e
    caminhos que viewer/editor não precisam ver."""
    _require_admin(request)
    return {"entries": SEC.read_audit(min(max(limit, 1), 2000))}


from . import sem_janela as _subprocess  # noqa: E402  -- nunca abre janela na tela
import shutil as _shutil  # noqa: E402
import sys as _sys  # noqa: E402
import os as _os_env  # noqa: E402
import time as _time_mon  # noqa: E402
import threading as _threading_mon  # noqa: E402

# estado do botão "checar andamentos agora" — uma execução por vez (serializada)
_MONITOR_STATE: dict = {"running": False, "started": None, "finished": None,
                        "rc": None, "tail": None, "erro": None}
_MONITOR_LOCK = _threading_mon.Lock()


def _monitor_python() -> str:
    """Resolve um Python que rode o monitor: precisa de PyYAML e, idealmente, de um extrator de
    PDF (pypdf) para a RPI. O backend roda num venv enxuto; o monitor precisa do Python do
    SISTEMA (internet + libs). Escolhe o melhor candidato disponível."""
    cands = [r"C:\Python314\python.exe", _shutil.which("python"), _shutil.which("python3")]
    best = None
    for c in cands:
        if not c:
            continue
        try:
            r = _subprocess.run([c, "-c",
                                 "import importlib.util as u,sys;"
                                 "sys.exit(0 if u.find_spec('yaml') else 3);"],
                                capture_output=True, timeout=15)
        except Exception:
            continue
        if r.returncode == 0:
            # prefere um que TAMBÉM tenha pypdf (para a RPI); senão guarda como fallback
            try:
                rp = _subprocess.run([c, "-c", "import pypdf"], capture_output=True, timeout=15)
                if rp.returncode == 0:
                    return c
            except Exception:
                pass
            best = best or c
    return best or _sys.executable


def _run_monitor_bg():
    py = _monitor_python()
    script = str(C.CENTRAL / "tools" / "patent_monitor.py")
    try:
        proc = _subprocess.run([py, script, "--run"], cwd=str(C.CENTRAL),
                               capture_output=True, text=True, timeout=300,
                               env={**_os_env.environ, "PYTHONUTF8": "1"})
        tail = (proc.stdout or "")[-1500:] + (("\n[stderr] " + proc.stderr[-500:]) if proc.stderr else "")
        with _MONITOR_LOCK:
            _MONITOR_STATE.update(running=False, finished=_time_mon.time(),
                                  rc=proc.returncode, tail=tail, erro=None)
    except Exception as e:  # noqa: BLE001 — uma falha aqui é FALHA, reportada como tal
        with _MONITOR_LOCK:
            _MONITOR_STATE.update(running=False, finished=_time_mon.time(), rc=-1, erro=str(e)[:300])


@app.post("/api/andamentos/run")
def andamentos_run():
    """O BOTÃO: dispara o monitor (auditoria de prazos + reachability INPI + tentativa de
    despachos) em background, no Python do SISTEMA (internet + pypdf). Uma execução por vez.
    A régua: uma falha é FALHA reportada, nunca 'sem movimentação'. O operador comanda; roda."""
    with _MONITOR_LOCK:
        if _MONITOR_STATE["running"]:
            return {"status": "ja_rodando", "started": _MONITOR_STATE["started"]}
        _MONITOR_STATE.update(running=True, started=_time_mon.time(), finished=None, rc=None, tail=None, erro=None)
    _threading_mon.Thread(target=_run_monitor_bg, daemon=True).start()
    return {"status": "disparado", "started": _MONITOR_STATE["started"],
            "nota": "rodando em background; consulte GET /api/andamentos para o desfecho"}


def _load_monitor():
    """Importa o monitor (tools/patent_monitor.py) — stdlib + yaml, que o venv do backend tem."""
    if "patent_monitor" in _sys.modules:
        return _sys.modules["patent_monitor"]
    import importlib.util as _ilu
    path = C.CENTRAL / "tools" / "patent_monitor.py"
    spec = _ilu.spec_from_file_location("patent_monitor", str(path))
    mod = _ilu.module_from_spec(spec)
    _sys.modules["patent_monitor"] = mod          # ANTES do exec (o @dataclass procura o módulo aqui)
    spec.loader.exec_module(mod)                   # type: ignore
    return mod


@app.post("/api/andamentos/registrar")
def andamentos_registrar(body: dict = Body(...)):
    """MANUAL ASSISTIDO (decisão do operador): o operador confere o despacho no INPI (pePI,
    logado na conta dele) e o REGISTRA aqui. Grava no ledger de movimentos (marcado como
    confirmado pelo operador) e alimenta o Prompt Compiler. Zero credencial guardada.
    A régua: só aceita processo que existe nos dockets; o registro é do operador (fonte confiável)."""
    processo = str(body.get("processo", "")).strip()
    data = str(body.get("data", "")).strip()
    codigo = str(body.get("codigo_despacho", "")).strip() or None
    descricao = str(body.get("descricao", "")).strip()
    if not processo or not data or not descricao:
        raise HTTPException(400, "informe processo, data e descrição do despacho")
    try:
        mon = _load_monitor()
    except Exception as e:
        raise HTTPException(503, f"monitor indisponível: {e}")
    validos = {d.processo for d in mon.load_dockets() if d.processo}
    if processo not in validos:
        raise HTTPException(400, f"processo desconhecido: {processo}")
    mov = {"processo": processo, "data": data, "codigo_despacho": codigo,
           "trecho": descricao[:400], "fonte": "INPI (registro do operador)",
           "confirmado_pelo_operador": True}
    rec = mon.record_movements([mov])
    # reconstrói o bloco do compiler com TODOS os movimentos (o registro entra no CLAUDE_CODE_TASK)
    todos = mon._load_ledger()
    mon.feed_compiler_notes([m for m in todos if not m.get("silencioso")])
    return {"registrado": bool(rec["novos"]), "movimento": (rec["novos"][0] if rec["novos"] else None),
            "total_no_ledger": rec["total_no_ledger"]}


@app.get("/api/andamentos")
def andamentos():
    """Estado do MONITOR DE PATENTES (INPI + ePCT) — só leitura. Alimenta o sino/aba Andamentos.
    A régua: uma falha de busca é FALHA visível; nunca 'sem movimentação'. Prazos são [LEGAL].
    O fetch ao vivo roda na máquina do operador (tools/patent_monitor.py); aqui só se LÊ o store."""
    import json as _json
    base = C.CENTRAL / "andamentos"
    with _MONITOR_LOCK:
        exec_state = dict(_MONITOR_STATE)
    out = {"store_presente": base.exists(), "auditoria": None, "movimentos_nao_confirmados": [],
           "total_movimentos": 0, "gerado_utc": None, "execucao": exec_state, "last_run": None}
    lr = base / "last_run.json"
    if lr.exists():
        try:
            out["last_run"] = _json.loads(lr.read_text(encoding="utf-8"))
        except (OSError, _json.JSONDecodeError):
            pass
    aud = base / "deadline_audit.json"
    if aud.exists():
        try:
            rep = _json.loads(aud.read_text(encoding="utf-8"))
            out["auditoria"] = {"referencia_hoje": rep.get("referencia_hoje"),
                                "resumo": rep.get("resumo"), "disclaimer": rep.get("disclaimer"),
                                "processos": rep.get("processos")}
        except (OSError, _json.JSONDecodeError) as e:
            out["auditoria_erro"] = str(e)
    led = base / "movements.jsonl"
    if led.exists():
        try:
            movs = [_json.loads(l) for l in led.read_text(encoding="utf-8").splitlines() if l.strip()]
            out["total_movimentos"] = len(movs)
            out["movimentos_nao_confirmados"] = [m for m in movs if not m.get("confirmado_pelo_operador")][-50:]
        except (OSError, _json.JSONDecodeError) as e:
            out["movimentos_erro"] = str(e)
    # O SINAL DA SENTINELA (tools/sentinela.py, Agendador do Windows, diário): nível + itens. Ausência = a Sentinela
    # nunca rodou nesta máquina — dito, nunca "verde". Leituras da IALD nativa: andamentos/leituras_iald/<id>.md.
    sin = base / "SINAL.json"
    if sin.exists():
        try:
            out["sinal"] = _json.loads(sin.read_text(encoding="utf-8"))
        except (OSError, _json.JSONDecodeError) as e:
            out["sinal"] = {"nivel": "vermelho", "erro": f"SINAL.json ilegível: {e}", "itens": []}
    else:
        out["sinal"] = None
    pz = base / "prazos_de_despacho.json"
    if pz.exists():
        try:
            out["prazos_de_despacho"] = _json.loads(pz.read_text(encoding="utf-8")).get("itens", [])
        except (OSError, _json.JSONDecodeError):
            out["prazos_de_despacho"] = []
    lei = base / "leituras_iald"
    out["leituras_iald"] = sorted(p.stem for p in lei.glob("*.md")) if lei.exists() else []
    return out


@app.get("/api/andamentos/leitura/{mid}")
def andamentos_leitura(mid: str):
    """A leitura da IALD nativa de um despacho (texto), marcada 'a confirmar'. Só leitura."""
    import re as _re
    if not _re.fullmatch(r"[0-9a-f]{16}", mid):
        raise HTTPException(400, "id inválido")
    p = C.CENTRAL / "andamentos" / "leituras_iald" / f"{mid}.md"
    if not p.exists():
        raise HTTPException(404, "sem leitura para este despacho")
    return {"id": mid, "texto": p.read_text(encoding="utf-8")}


@app.post("/api/andamentos/confirmar")
def andamentos_confirmar(request: Request, body: dict = Body(...)):
    """O CLIQUE DO OPERADOR (decisão D8 de 22/09/2026): marca um despacho do ledger como confirmado. O ledger é
    append-only por natureza; aqui o único campo que muda é `confirmado_pelo_operador` (+ carimbo), com backup de
    bytes antes e escrita tmp→replace. Depois reemite o sinal (sentinela --sem-rede --sem-iald) para o painel refletir."""
    _require_admin(request)
    import json as _json, shutil as _shutil, subprocess as _sp
    from datetime import datetime as _dt, timezone as _tz
    mid = str(body.get("id", "")).strip()
    if not mid:
        raise HTTPException(400, "informe o id do movimento")
    led = C.CENTRAL / "andamentos" / "movements.jsonl"
    if not led.exists():
        raise HTTPException(404, "ledger ausente")
    raw = led.read_bytes()
    linhas = [l for l in raw.decode("utf-8").splitlines() if l.strip()]
    achou = False
    novas = []
    for l in linhas:
        m = _json.loads(l)
        if m.get("id") == mid:
            m["confirmado_pelo_operador"] = True
            m["confirmado_em"] = _dt.now(_tz.utc).isoformat(timespec="seconds")
            achou = True
        novas.append(_json.dumps(m, ensure_ascii=False))
    if not achou:
        raise HTTPException(404, f"movimento {mid} não está no ledger")
    bak = led.with_name(led.name + ".bak_" + _dt.now().strftime("%Y%m%d_%H%M%S"))
    bak.write_bytes(raw)
    tmp = led.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(novas) + "\n", encoding="utf-8")
    tmp.replace(led)
    try:
        _sp.run([_monitor_python(), str(C.CENTRAL / "tools" / "sentinela.py"), "--sem-rede", "--sem-iald", "--sem-toast"],
                capture_output=True, timeout=180, cwd=str(C.CENTRAL))
    except Exception as e:  # noqa: BLE001 — o sinal antigo fica; a confirmação já está gravada
        return {"confirmado": mid, "sinal_reemitido": False, "erro": str(e)[:120]}
    return {"confirmado": mid, "sinal_reemitido": True}


@app.get("/api/backup/status")
def backup_status():
    """ANEXO — status do backup 3-2-1 (espelho D: + Toshiba + Google cifrado + cofre), só leitura.
    A régua: falha de leitura é FALHA em-banda, nunca 'ok' falso. Local-only (os discos de backup
    são da máquina do operador; na nuvem reporta ambiente=remoto). NUNCA lê/expõe a senha do cofre."""
    return BK.get_status()


@app.post("/api/backup/run")
def backup_run(request: Request):
    """O BOTÃO (admin): dispara o backup diário (espelho C->D + sync cifrado C->Google) em
    background. O disjuntor continua protegendo — um backup disparado não propaga ataque."""
    _require_admin(request)
    return BK.run_backup()


@app.get("/api/epct/status")
def epct_status():
    """ANEXO ePCT — conferência do protocolo internacional dos 15: dossiês (data de
    prioridade lida do depósito INPI) + tiques do operador + dias restantes. Só leitura."""
    return EP.get_overview()


@app.post("/api/epct/tick")
def epct_tick(request: Request, body: dict = Body(...)):
    """O TIQUE (admin): marca/desmarca uma etapa do protocolo de um dispositivo, ou grava
    pct_number/protocol_date/nota. Escreve SÓ em EPCT/epct_status.json (atômico)."""
    _require_admin(request)
    try:
        return EP.set_tick(str(body.get("id") or ""), str(body.get("step") or ""),
                           body.get("value"), body.get("extra") or {})
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/api/iald/status")
def iald_nativa_status():
    """ANEXO — cockpit da IALD Nativa (llama :8081, web :8082 + detecção de listeners
    duplicados, túnel cloudflared, GPU, modelos, kernels). Só leitura; local-only
    (na nuvem reporta ambiente=remoto); confidenciais = SÓ existência+mtime."""
    return NAT.get_status()


@app.get("/api/organismo")
def organismo_quadro(request: Request):
    """O QUADRO DO ORGANISMO (24/10/2026): a medida de cada superfície da IALD contra o selo corrente do um.py, feita por
    tools/estado_do_organismo.py (organismo/ESTADO_DO_ORGANISMO.json, fora do git). Só leitura; devolve o documento inteiro mais a idade
    da medição em minutos; 404 visível quando ainda não há quadro (o painel mostra a falha, não inventa)."""
    _require_admin(request)   # o quadro cita caminhos e estados internos da casa: só o operador (24/10, achado do revisor)
    p = C.CENTRAL / "organismo" / "ESTADO_DO_ORGANISMO.json"
    if not p.is_file():
        raise HTTPException(404, "quadro ainda não medido: rode tools/estado_do_organismo.py")
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise HTTPException(500, "quadro ilegível: %r" % (e,))
    doc["idade_min"] = round((time.time() - p.stat().st_mtime) / 60, 1)
    return doc


@app.post("/api/organismo")
def organismo_medir_alias(request: Request, body: dict = Body(default={})):
    """O painel do cockpit (Organismo.tsx, Kimi 23/10) faz POST /api/organismo para medir de novo: mesmo ato de /api/organismo/medir."""
    return organismo_medir(request, body)


@app.post("/api/organismo/medir")
def organismo_medir(request: Request, body: dict = Body(default={})):
    """AÇÃO (admin): mede o organismo de novo em processo novo (tools/estado_do_organismo.py; --sem-rede por padrão, ~1 min;
    com {"rede": true} mede também o ar, ~3 min) e devolve o quadro novo. Nunca mata processo; nunca chama provedor."""
    _require_admin(request)
    import subprocess as _sp
    args = ["C:/Python314/python.exe", "-X", "utf8", str(C.CENTRAL / "tools" / "estado_do_organismo.py")]
    if not bool(body.get("rede")):
        args.append("--sem-rede")
    try:
        r = _sp.run(args, capture_output=True, timeout=900, cwd=str(C.CENTRAL), creationflags=getattr(_sp, "CREATE_NO_WINDOW", 0))   # sem janela sob pythonw
    except _sp.TimeoutExpired:
        raise HTTPException(504, "a medição não terminou em 15 min")
    doc = organismo_quadro(request)
    doc["medicao"] = {"rc": r.returncode, "ultima_linha": (r.stdout or b"").decode("utf-8", "replace").strip().splitlines()[-1:] }
    return doc


# ---------------- A TORRE DE COMANDO (24/10/2026): o quadro único + duas ações a seco; a lógica mora em torre.py ----------------
@app.get("/api/torre")
def torre_quadro(request: Request):
    """A TORRE DE COMANDO: selo, organismo, missões ACOM vivas, custódia, vigia, o X do dia e o túnel do Codex num JSON só. Só leitura;
    falha de leitura vai em `erros` (nunca «ok» falso); nenhum caminho absoluto na resposta. Só admin (cita estados internos da casa)."""
    _require_admin(request)
    return TORRE.montar()


@app.post("/api/torre/custodia/planejar")
def torre_custodia_planejar(request: Request, body: dict = Body(default={})):
    """AÇÃO (admin): `custodiar.py planejar --versao vNNN --seco` (sem versão: a que o `vigiar` reporta). A SECO: nunca `executar`, nunca
    `--publicar`. Do browser só vem `versao`, validada (v + 3 ou 4 dígitos); devolve {rc, stdout_cauda, versao}. Nunca mata processo, nunca chama provedor."""
    _require_admin(request)
    return TORRE.planejar_custodia(body.get("versao"))


@app.post("/api/torre/x/ensaio")
def torre_x_ensaio(request: Request):
    """AÇÃO (admin): `pensamento_do_dia.py --seco` (gera e mostra; não grava, não enfileira). Nada do browser vai para a linha de comando."""
    _require_admin(request)
    return TORRE.ensaio_x()


@app.get("/api/iald/orquestracao")
def iald_orquestracao(request: Request):
    """A ORQUESTRAÇÃO DA IALD (a AGI em construção, feita pelo Codex) lida pela Central — SÓ LEITURA: banco em
    mode=ro, recibos de validação, transporte. O painel vivo (ações) é o da Central IALD nativa (:8082,
    /admin/agi/orquestracao). Exige admin: devolve o começo do texto dos pedidos do operador."""
    _require_admin(request)
    return ORQ.get_status()


@app.post("/api/iald/task")
def iald_nativa_task(request: Request, body: dict = Body(...)):
    """AÇÃO (admin): schtasks /Run|/End sobre as tarefas da casa nativa —
    SOMENTE a whitelist {'IALD Llama Server','IALD Web Server','IALD Cloudflared Tunnel'}."""
    _require_admin(request)
    name, action = str(body.get("name") or ""), str(body.get("action") or "")
    try:
        if action == "run":
            return NAT.run_task(name)
        if action == "end":
            return NAT.end_task(name)
        raise ValueError(f"acao invalida: {action!r} (use run|end)")
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/iald/sanear")
def iald_nativa_sanear(request: Request):
    """SANEAMENTO (admin): mata listeners EXTRAS na 8082 (o bug do painel travado de
    10/08 — 2a instância manual na mesma porta). Mantém o supervisionado/mais antigo.
    FAIL-VISÍVEL: sem duplicata responde 400, nunca 'ok' falso."""
    _require_admin(request)
    try:
        return NAT.sanear_web()
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/api/health")
def health():
    conn = connect()
    meta = {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM index_meta")}
    counts = {t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
              for t in ["patent", "patent_class", "document", "deadline", "note",
                        "runner_run", "pendencia"]}
    conn.close()
    return {"status": "ok", "external_calls": "disabled",
            "patents_indexed": counts["patent"], "classes_indexed": counts["patent_class"],
            "originals_manifest_ok": meta.get("originals_integrity") == "OK",
            "last_reindex_utc": meta.get("last_reindex_utc"),
            "schema_version": meta.get("schema_version"), "counts": counts}


@app.post("/api/reindex")
def do_reindex(force: bool = False):
    return reindex(force=force)


@app.get("/api/integrity")
def integrity():
    res = check_integrity()
    return {"status": res["status"], "checked": res["checked"],
            "violations": res["violations"][:50],
            "message": ("Originais intactos." if res["status"] == "OK"
                        else "ALERTA: originais alterados!")}


# ---------------- classes ----------------
@app.get("/api/classes")
def classes():
    conn = connect()
    data = rows(conn.execute("""
        SELECT c.*, COUNT(p.id) AS patent_count
        FROM patent_class c LEFT JOIN patent p ON p.class_id = c.id
        GROUP BY c.id ORDER BY c.ordinal"""))
    conn.close()
    for d in data:
        d["markers"] = json.loads(d.get("markers") or "[]")
    return data


# ---------------- patents ----------------
@app.get("/api/patents")
def patents():
    conn = connect()
    data = rows(conn.execute(f"""
        SELECT p.id, p.slug, p.display_name, p.dir_name, p.class_id, p.role, p.title_54,
               p.filing_date, p.priority_date, p.epct_status, p.epct_number, p.prototype_status,
               p.claims_total, p.doc_count, p.markers, dk.alert_level,
               (SELECT MIN(d.due_date) FROM deadline d
                  WHERE d.patent_id=p.id AND d.status='pendente' AND d.due_date IS NOT NULL)
                 AS next_due,
               (SELECT {URGENCY_SQL} FROM deadline d
                  WHERE d.patent_id=p.id AND d.status='pendente' AND d.due_date IS NOT NULL
                  ORDER BY d.due_date LIMIT 1) AS next_urgency
        FROM patent p LEFT JOIN docket_entry dk ON dk.patent_id=p.id
        ORDER BY p.filing_date, p.id"""))
    conn.close()
    for d in data:
        d["markers"] = json.loads(d.get("markers") or "[]")
    return data


def _proof_citations(dir_name: str) -> tuple[set, set]:
    """A CLASSE PROVA: documentos (ids) e arquivos de código (paths) citados nas Cadeias de
    Prova (evidence.json) da patente. É a série de arquivos que COMPROVA as reivindicações —
    destacada com ⭐ nas abas Documentos/Código. Falha silenciosa = conjuntos vazios."""
    doc_ids: set = set()
    code_paths: set = set()
    pdir = C.PATENTS_DIR / dir_name
    src = pdir / "evidence_verified.json"
    if not src.exists():
        src = pdir / "evidence.json"
    if not src.exists():
        return doc_ids, code_paths
    try:
        ev = json.loads(src.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return doc_ids, code_paths
    for claim in ev.get("claims", []):
        for elo in claim.get("chain", []):
            # forma BRUTA (evidence.json): locator={kind,id|path}
            loc = elo.get("locator") or {}
            if loc.get("kind") == "document" and loc.get("id") is not None:
                doc_ids.add(loc["id"])
            elif loc.get("kind") == "code" and loc.get("path"):
                code_paths.add(str(loc["path"]).replace("\\", "/"))
            # forma VERIFICADA (evidence_verified.json): achatada em doc_id / code_path
            if elo.get("doc_id") is not None:
                doc_ids.add(elo["doc_id"])
            if elo.get("code_path"):
                code_paths.add(str(elo["code_path"]).replace("\\", "/"))
    return doc_ids, code_paths


@app.get("/api/patents/{pid}")
def patent_detail(pid: str):
    conn = connect()
    p = conn.execute("SELECT * FROM patent WHERE id=?", (pid,)).fetchone()
    if not p:
        conn.close()
        raise HTTPException(404, "patente não encontrada")
    p = dict(p)
    p["markers"] = json.loads(p.get("markers") or "[]")
    dk = conn.execute("SELECT * FROM docket_entry WHERE patent_id=?", (pid,)).fetchone()
    p["docket"] = dict(dk) if dk else None
    p["class"] = dict(conn.execute("SELECT id,name,ordinal,markers,lock_note FROM patent_class WHERE id=?",
                                   (p["class_id"],)).fetchone() or {})
    p["deadlines"] = rows(conn.execute(f"""
        SELECT *, CAST(julianday(due_date)-julianday('now') AS INT) AS days_remaining,
               {URGENCY_SQL} AS urgency
        FROM deadline d WHERE patent_id=? ORDER BY (due_date IS NULL), due_date""", (pid,)))
    p["documents"] = rows(conn.execute(
        "SELECT id,rel_path,sha256,doc_role,pages,ext FROM document WHERE patent_id=? ORDER BY doc_role",
        (pid,)))
    _proof_docs, _ = _proof_citations(p["dir_name"])
    for d in p["documents"]:
        d["proof"] = d["id"] in _proof_docs          # ⭐ classe prova (citado na Cadeia de Prova)
    p["notes"] = _notes_for(conn, pid)
    p["renders"] = rows(conn.execute(
        "SELECT id,kind,layer,title,marker FROM render WHERE patent_id=? ORDER BY id", (pid,)))
    p["runs"] = rows(conn.execute(
        "SELECT * FROM runner_run WHERE patent_id=? ORDER BY finished_at DESC", (pid,)))
    p["pendencias"] = rows(conn.execute("""
        SELECT pe.id, pe.title, pe.status FROM pendencia pe
        JOIN pendencia_patent pp ON pp.pendencia_id=pe.id WHERE pp.patent_id=?""", (pid,)))
    conn.close()
    return p


def _notes_for(conn, pid):
    ns = rows(conn.execute(
        "SELECT id,tipo,active,done,text,markers,source_file,source_section,line_ref "
        "FROM note WHERE patent_id=? ORDER BY line_ref", (pid,)))
    for n in ns:
        n["markers"] = json.loads(n.get("markers") or "[]")
    return ns


@app.get("/api/patents/{pid}/renders")
def patent_renders(pid: str):
    conn = connect()
    data = rows(conn.execute(
        "SELECT id,kind,layer,title,asset_path,sha256,marker FROM render "
        "WHERE patent_id=? ORDER BY id", (pid,)))
    conn.close()
    return data


@app.get("/api/renders/{render_id}")
def render_file(render_id: int):
    conn = connect()
    r = conn.execute("SELECT asset_path FROM render WHERE id=?", (render_id,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "render não encontrado")
    p = C.CENTRAL / r["asset_path"]
    if not p.exists():
        raise HTTPException(404, "arquivo ausente")
    return FileResponse(str(p), media_type="image/png")


@app.get("/api/patents/{pid}/memory", response_class=PlainTextResponse)
def patent_memory(pid: str):
    conn = connect()
    r = conn.execute("SELECT memory_md_path FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    path = C.CENTRAL / r["memory_md_path"]
    return path.read_text(encoding="utf-8") if path.exists() else "(memória não encontrada)"


_CLAIMS_RE = re.compile(
    r"^##[^\n]*eivindica[^\n]*principais[^\n]*\n(.*?)(?=^##\s|\Z)",
    re.S | re.M | re.I)


@app.get("/api/patents/{pid}/claims")
def patent_claims(pid: str):
    """As reivindicações SINTETIZADAS (resumo fiel, marcado [REAL]) já vivem na memória
    técnica de cada patente sob '## Reivindicações principais'. Aqui extraímos exatamente
    essa seção e a servimos — nunca re-fabricamos (a régua: o número corrige a frase)."""
    conn = connect()
    r = conn.execute(
        "SELECT memory_md_path, claims_total, claims_independent, title_54 "
        "FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    path = C.CENTRAL / (r["memory_md_path"] or "")
    md = path.read_text(encoding="utf-8") if path.exists() else ""
    m = _CLAIMS_RE.search(md)
    header = ""
    body = ""
    if m:
        body = m.group(1).strip()
        # a própria linha do cabeçalho (para exibir o "resumo fiel — total: N")
        hm = re.search(r"^(##[^\n]*eivindica[^\n]*principais[^\n]*)$", md, re.M | re.I)
        header = (hm.group(1).lstrip("#").strip() if hm else "").strip()
    return {
        "available": bool(body),
        "patent_id": pid,
        "title_54": r["title_54"],
        "claims_total": r["claims_total"],
        "claims_independent": r["claims_independent"],
        "section_title": header,
        "markdown": body,
        "source": r["memory_md_path"],
        "note": "Resumo fiel extraído da memória técnica (marcado [REAL]). "
                "O texto integral e verbatim está no PDF de depósito (aba Documentos).",
    }


@app.get("/api/patents/{pid}/evidence")
def patent_evidence(pid: str):
    """Cadeia de Prova: cada reivindicação → elos (depósito/teste/código/dispositivo/dado/nota),
    com hashes resolvidos por tools/verify_evidence.py. Serve o relatório verificado (ou o bruto)."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    pdir = C.PATENTS_DIR / r["dir_name"]
    verified = pdir / "evidence_verified.json"
    raw = pdir / "evidence.json"
    src = verified if verified.exists() else raw
    if not src.exists():
        return {"available": False, "claims": []}
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise HTTPException(500, f"evidence inválido: {e}")
    data["available"] = True
    data["verified"] = verified.exists()
    return data


@app.get("/api/patents/{pid}/components")
def patent_components(pid: str):
    """Camada (b) do render: mapa de componentes clicável, lido de
    patents/<dir>/components.json (fonte da verdade no filesystem). Vazio se ausente."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    path = C.PATENTS_DIR / r["dir_name"] / "components.json"
    if not path.exists():
        return {"available": False, "groups": [], "flows": [], "constants": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise HTTPException(500, f"components.json inválido: {e}")
    data["available"] = True
    return data


@app.get("/api/patents/{pid}/render3d")
def patent_render3d(pid: str):
    """Camada (c) do render: cena 3D interativa, lida de patents/<dir>/render3d.json
    (fonte da verdade no filesystem). Vazio se ausente."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    path = C.PATENTS_DIR / r["dir_name"] / "render3d.json"
    if not path.exists():
        return {"available": False, "nodes": [], "edges": [], "groups": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise HTTPException(500, f"render3d.json inválido: {e}")
    data["available"] = True
    return data


_CODE_EXT = (".py", ".json", ".txt", ".csv", ".yaml", ".yml", ".md")
_CODE_SKIP = ("__pycache__", "results", "seals", "renders", "notes", ".git")
_CONFIDENTIAL = ("iald_stack_v7", "iald_psion_state", "iald_web_server", "token_huggin")


def _code_role(rel: str) -> str:
    if rel.endswith("_FINAL.py"):
        return "final"
    if rel.endswith("_FINAL.manifest.json"):
        return "manifest"
    if rel.startswith("runner/") and "/one_" in ("/" + rel):
        return "runner" if rel.count("/") == 1 else "core"
    if rel.startswith("prototype_src/"):
        return "prototype"
    if rel.startswith("runner/"):
        return "core"
    return "outro"


@app.get("/api/patents/{pid}/code")
def patent_code(pid: str):
    """A CODIFICACAO de cada patente (documento tambem): o codigo-fonte FINALIZADO (<slug>_FINAL.py,
    auto-contido + hash), o runner, prototype_src e o nucleo. Arvore + papel + tamanho + hash."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    pdir = C.PATENTS_DIR / r["dir_name"]
    if not pdir.exists():
        return {"available": False, "files": []}
    files = []
    for f in sorted(pdir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(pdir).as_posix()
        if any(p in _CODE_SKIP for p in rel.split("/")):
            continue
        if any(c in f.name.lower() for c in _CONFIDENTIAL):
            continue
        if f.suffix.lower() not in _CODE_EXT:
            continue
        files.append({"path": rel, "role": _code_role(rel), "bytes": f.stat().st_size})
    _, _proof_paths = _proof_citations(r["dir_name"])
    for x in files:
        x["proof"] = x["path"] in _proof_paths       # ⭐ classe prova (citado na Cadeia de Prova)
    # o FINAL + seu manifesto (hash combinado)
    final = next((x for x in files if x["role"] == "final"), None)
    manifest = None
    if final:
        mf = pdir / (final["path"].rsplit(".py", 1)[0] + ".manifest.json")
        if mf.exists():
            try:
                manifest = json.loads(mf.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                manifest = None
    return {"available": bool(files), "patent_id": pid, "final": final, "manifest": manifest,
            "counts": {k: sum(1 for x in files if x["role"] == k)
                       for k in ("final", "runner", "prototype", "core", "manifest", "outro")},
            "files": files}


@app.get("/api/patents/{pid}/code/file", response_class=PlainTextResponse)
def patent_code_file(pid: str, path: str):
    """Serve o conteudo de UM arquivo de codigo da patente (guard anti-traversal e confidencial)."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    pdir = (C.PATENTS_DIR / r["dir_name"]).resolve()
    target = (pdir / path).resolve()
    # is_relative_to (nao startswith) evita bug de prefixo-irmao (pdir + '_evil') e caminho absoluto
    if not target.is_relative_to(pdir) or not target.is_file():
        raise HTTPException(400, "caminho inválido")
    if any(c in target.name.lower() for c in _CONFIDENTIAL) or target.suffix.lower() not in _CODE_EXT:
        raise HTTPException(403, "arquivo não servível")
    if target.stat().st_size > 4_000_000:
        return "(arquivo muito grande para exibir; abra localmente)"
    return target.read_text(encoding="utf-8", errors="replace")


# ---------------- evolucao (linha do tempo dos seals/results, read-only) ----------------
_EVO_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$")
_EVO_SECTION_PREFIXES = ("amplifica", "amplification", "deepening", "aprofund")


def _evo_load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


@app.get("/api/patents/{pid}/evolucao")
def patent_evolucao(pid: str):
    """Linha do tempo de EVOLUCAO do dispositivo: enumera seals/<ts>/seal.json (leitura
    apenas, artefatos selados intocados) e cruza com results/<ts>/results.json para
    extrair: timestamp, result_hash curto, testes passados/total, veredito e os nomes
    das secoes de amplificacao/deepening presentes no result daquela rodada."""
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente nao encontrada")
    pdir = C.PATENTS_DIR / r["dir_name"]
    seals_dir = pdir / "seals"
    if not seals_dir.is_dir():
        return {"available": False, "patent_id": pid, "total": 0, "entries": []}
    entries = []
    for d in sorted(seals_dir.iterdir()):
        if not d.is_dir() or not _EVO_TS_RE.match(d.name):
            continue
        seal = _evo_load_json(d / "seal.json")
        res = _evo_load_json(pdir / "results" / d.name / "results.json")
        rh = str(seal.get("result_hash") or "")
        verdict = res.get("verdict") or (str(seal.get("max_verdict") or "").split(" (")[0] or None)
        tests_passed = seal.get("tests_passed")
        tests_total = None
        sections: list[str] = []
        sections += [k for k in res.keys()
                     if isinstance(k, str) and k.lower().startswith(_EVO_SECTION_PREFIXES)]
        tests = res.get("tests")
        if isinstance(tests, list):
            tests_total = len(tests)
            names = [t.get("test") for t in tests if isinstance(t, dict)]
            sections += [n for n in names
                         if isinstance(n, str) and n.lower().startswith(_EVO_SECTION_PREFIXES)]
            if tests_passed is None:
                tests_passed = sum(1 for t in tests if isinstance(t, dict) and t.get("passed") is True)
        summary = res.get("summary")
        if tests_total is None and isinstance(summary, dict):
            tests_total = summary.get("tests_total")
        entries.append({
            "timestamp": d.name,
            "result_hash_short": rh[:16] or None,
            "tests_passed": tests_passed,
            "tests_total": tests_total,
            "verdict": verdict,
            "runner": seal.get("runner"),
            "sections": sections,
            "has_result": bool(res),
        })
    entries.reverse()   # mais recente primeiro
    return {"available": bool(entries), "patent_id": pid, "dir_name": r["dir_name"],
            "total": len(entries), "entries": entries}


def _json_strict(x):
    """Sanitizador READ-ONLY da camada API (o artefato selado em disco NAO muda).
    Politica consistente: inf -> string "Infinity"/"-Infinity" (preserva a substancia —
    ex.: gate_R.ratio_v2_over_v1 e' genuinamente infinito pois v1_replica=0); NaN -> null.
    Motivo: o selo do runner usa json.dump padrao (allow_nan=True) e emite `Infinity`
    literal, que JSON.parse do navegador rejeita (JSON estrito, RFC 8259)."""
    if isinstance(x, float):
        if math.isnan(x):
            return None
        if math.isinf(x):
            return "Infinity" if x > 0 else "-Infinity"
        return x
    if isinstance(x, dict):
        return {k: _json_strict(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_json_strict(v) for v in x]
    return x


@app.get("/api/fronteira")
def fronteira_teorica():
    """Fronteira Teorica TGL: a fundacao teorica das 16 patentes, auto-auditada (forma=conteudo).
    Serve o render3d da cadeia de operadores + o ledger honesto do ultimo selo do runner.
    Nada de veredito fisico; o teorema aberto (GLOBAL_LIFT) e' declarado, nao fabricado."""
    base = C.PATENTS_DIR.parent / "fronteira_tgl"
    render = base / "render3d.json"
    out = {"available": render.exists()}
    if render.exists():
        try:
            out["render3d"] = json.loads(render.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise HTTPException(500, f"render3d.json invalido: {e}")
    results_dir = base / "results"
    if results_dir.exists():
        seals = sorted(results_dir.glob("fronteira_*.json"), reverse=True)
        if seals:
            try:
                out["seal"] = json.loads(seals[0].read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    # JSON estrito para o navegador; o selo em disco permanece intocado.
    return _json_strict(out)


# As 4 FIGURAS SELADAS do um.py (v138): servidas da custodia por hash (vault/), allowlist
# FIXA — nenhum caminho do cliente toca o filesystem. READ-ONLY, como toda a custodia.
_FRONTEIRA_FIGS = {
    "escada_qg": "fig_escada_qg.pdf",
    "banda_beta": "fig_banda_beta.pdf",
    "piso_vazios": "fig_piso_vazios.pdf",
    "cadeia_inscricao": "fig_cadeia_inscricao.pdf",
}


@app.get("/api/fronteira/fig/{name}")
def fronteira_fig(name: str):
    """Serve uma das 4 figuras SELADAS (selo v138) direto da custodia mais recente.
    Allowlist fixa (name e' uma CHAVE, nunca caminho); 404 se a custodia nao as tiver."""
    fname = _FRONTEIRA_FIGS.get(name)
    if not fname:
        raise HTTPException(404, "figura desconhecida")
    vault = C.PATENTS_DIR.parent / "vault" / "originals_copy"
    dirs = sorted([d for d in vault.glob("um_unificado_v*") if (d / fname).exists()], reverse=True)
    if not dirs:
        raise HTTPException(404, "figura ausente da custodia")
    from fastapi.responses import FileResponse
    return FileResponse(str(dirs[0] / fname), media_type="application/pdf", filename=fname)


# ---------------- DISPOSITIVOS (o dispositivo funcionando: interface real) -------------
import base64  # noqa: E402
from urllib.parse import quote  # noqa: E402
from fastapi.concurrency import run_in_threadpool  # noqa: E402

_DEVICE_MAX_BODY = 64 * 1024 * 1024   # teto duro de corpo (o codec também limita)


def _report_header(report: dict) -> dict:
    """Relatório do dispositivo num header ASCII-safe (base64 de JSON UTF-8)."""
    raw = json.dumps(report, ensure_ascii=False).encode("utf-8")
    return {"X-Acom-Report": base64.b64encode(raw).decode("ascii")}


def _report_dict(report) -> dict:
    """Cada dispositivo relata do seu jeito e isso é correto — o relatório é a forma da
    invenção, não um formato imposto de fora. O ACOM devolve um `CompressReport`
    (dataclass); o TGL-Tensor devolve um dict com o NOME e a escada do Piso de Hilbert.
    Aqui só se normaliza o transporte, sem achatar o conteúdo de ninguém."""
    if hasattr(report, "as_dict"):
        return report.as_dict()
    return dict(report)


def _content_disposition(name: str) -> str:
    return f"attachment; filename*=UTF-8''{quote(name)}"


async def _read_capped_body(request: Request) -> bytes:
    # pre-check rápido pelo Content-Length (quando presente)
    cl = request.headers.get("content-length")
    if cl and cl.isdigit() and int(cl) > _DEVICE_MAX_BODY:
        raise HTTPException(413, "arquivo grande demais")
    # lê INCREMENTALMENTE e corta ao exceder o teto — nao confia so' no Content-Length
    # (Transfer-Encoding: chunked nao tem Content-Length e burlaria o pre-check).
    total = 0
    chunks: list[bytes] = []
    async for chunk in request.stream():
        total += len(chunk)
        if total > _DEVICE_MAX_BODY:
            raise HTTPException(413, "arquivo grande demais")
        chunks.append(chunk)
    body = b"".join(chunks)
    if not body:
        raise HTTPException(400, "corpo vazio (envie o arquivo como octet-stream)")
    return body


@app.get("/api/device/{slug}/info")
def device_info(slug: str):
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    try:
        return DEV.device_info(slug)
    except (FileNotFoundError, ImportError) as e:
        raise HTTPException(503, f"dispositivo indisponível: {e}")


@app.post("/api/device/{slug}/compress")
async def device_compress(slug: str, request: Request):
    """Recebe o arquivo (corpo octet-stream, nome em X-Filename) e devolve o contêiner
    .acom (binário) + o relatório no header X-Acom-Report.

    PORTA ÚNICA (acom_auto): não há modo a escolher — a LEITURA tipa o sinal e a LEI o
    roteia. `X-Fidelity: exata` não é um modo: é uma EXIGÊNCIA de integridade que proíbe
    de forma dura a rota com perda (o que o backup usa). Sem ela, vale a lei.
    Se a porta única não estiver disponível, cai no codec sem perdas de sempre."""
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    body = await _read_capped_body(request)
    name = request.headers.get("X-Filename", "arquivo")
    fidelity = request.headers.get("X-Fidelity", "auto").lower()
    if fidelity not in ("auto", "exata"):
        raise HTTPException(400, "X-Fidelity deve ser 'auto' ou 'exata'")
    try:
        codec = DEV.load_codec(slug)
    except (FileNotFoundError, ImportError) as e:
        raise HTTPException(503, f"dispositivo indisponível: {e}")
    try:
        auto = DEV.load_auto(slug)
    except (KeyError, FileNotFoundError, ImportError):
        auto = None
    try:
        # Pergunta-se ao dispositivo o que ELE sabe fazer, em vez de assumir um contrato só.
        # CPU-bound: sempre fora do event loop (nao congela o servidor).
        if auto is not None:                                   # ACOM: a porta única
            container, report = await run_in_threadpool(auto.compress_auto, body, name, fidelity)
        elif hasattr(codec, "compress_npy"):                   # TGL-Tensor: domínio é o tensor
            if fidelity == "exata":
                raise HTTPException(400, "o TGL-Tensor é compressão HOLOGRÁFICA: com perda por "
                                         "natureza. Não há rota bit-exata a exigir — quem julga a "
                                         "reconstrução é o NOME (escada do Piso de Hilbert).")
            container, report = await run_in_threadpool(codec.compress_npy, body, name)
        else:
            container, report = await run_in_threadpool(codec.compress_file, body, name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"falha ao comprimir: {e}")
    rep = _report_dict(report)
    out_name = rep["orig_name"] + ".acom"
    headers = {"Content-Disposition": _content_disposition(out_name), **_report_header(rep)}
    return Response(content=container, media_type="application/octet-stream", headers=headers)


@app.post("/api/device/{slug}/decompress")
async def device_decompress(slug: str, request: Request):
    """Recebe um contêiner .acom e devolve o arquivo original (binário), verificando
    a integridade por SHA-256. O nome original volta no Content-Disposition."""
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    body = await _read_capped_body(request)
    try:
        codec = DEV.load_codec(slug)
    except (FileNotFoundError, ImportError) as e:
        raise HTTPException(503, f"dispositivo indisponível: {e}")
    try:
        # cada dispositivo despacha o próprio contêiner: o ACOM pelo codec declarado no header
        # (LOSSLESS/TENSOR), o TGL-Tensor pelo seu — que verifica a integridade PELO NOME.
        _dec = getattr(codec, "decompress_any", None) or getattr(codec, "decompress", None)
        if _dec is None:
            raise HTTPException(501, "este dispositivo não expõe descompressão")
        data, name, meta = await run_in_threadpool(_dec, body)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"falha ao descomprimir: {e}")
    headers = {"Content-Disposition": _content_disposition(name),
               **_report_header({"restored_name": name, "restored_size": len(data), **meta})}
    return Response(content=data, media_type="application/octet-stream", headers=headers)


# ============================ O BOTÃO UM — gera o tgl.acom (admin) ============================
from . import um_acom as UM  # noqa: E402
import secrets as _secrets  # noqa: E402
import time as _time  # noqa: E402

import threading as _threading  # noqa: E402

# cache efêmero das árvores abertas pelo descompactador público (em memória, TTL curto).
# Só guarda o que o próprio visitante enviou+decifrou; nunca dados de patente da Central.
_ACOM_SESSIONS: dict[str, tuple[float, dict]] = {}
_ACOM_TTL = 600.0          # 10 min
_ACOM_MAX_SESSIONS = 32    # backstop de memória (cada sessão retém a árvore decifrada)
_ACOM_LOCK = _threading.Lock()   # o handler é async mas o put/get roda em threadpool → serializa


def _acom_cache_put(files: dict) -> str:
    now = _time.time()
    with _ACOM_LOCK:
        for k in [k for k, (ts, _) in list(_ACOM_SESSIONS.items()) if now - ts > _ACOM_TTL]:
            _ACOM_SESSIONS.pop(k, None)
        while len(_ACOM_SESSIONS) >= _ACOM_MAX_SESSIONS:
            oldest = min(_ACOM_SESSIONS, key=lambda k: _ACOM_SESSIONS[k][0])
            _ACOM_SESSIONS.pop(oldest, None)
        tok = _secrets.token_urlsafe(18)
        _ACOM_SESSIONS[tok] = (now, files)
    return tok


def _acom_cache_get(token: str) -> dict | None:
    with _ACOM_LOCK:
        ent = _ACOM_SESSIONS.get(token)
        if ent is None:
            return None
        ts, files = ent
        if _time.time() - ts > _ACOM_TTL:
            _ACOM_SESSIONS.pop(token, None)
            return None
        return files


# rate-limit dedicado das rotas PÚBLICAS /api/acom/* — ancorado em request.client.host (o IP da
# conexão real, NÃO em cabeçalho forjável): o open força scrypt (caro), então limitamos a
# tentativa por IP (anti-DoS de CPU e anti-brute-force online). Janela deslizante simples.
_ACOM_HITS: dict[str, list[float]] = {}
_ACOM_RL_WINDOW = 60.0
_ACOM_RL_MAX = 12           # 12 aberturas/inspects por IP por minuto


def _acom_rate_ok(request: Request) -> bool:
    ip = request.client.host if request.client else "?"
    now = _time.time()
    with _ACOM_LOCK:
        if len(_ACOM_HITS) > 8192:
            _ACOM_HITS.clear()
        xs = [t for t in _ACOM_HITS.get(ip, []) if now - t < _ACOM_RL_WINDOW]
        if len(xs) >= _ACOM_RL_MAX:
            _ACOM_HITS[ip] = xs
            return False
        xs.append(now)
        _ACOM_HITS[ip] = xs
        return True


# ==================== EMPACOTADOR ACOM — muitos arquivos/pastas → um .acom ====================
# Envelope de upload AUTOCONTIDO (sem python-multipart): MAGIC + header{files:[{path,len}]} + payloads.
# A senha (modo cifrado) vem em X-Inscricao (nunca no corpo/log). Web = memória (teto abaixo);
# backups grandes = CLI tools/acom_pack.py (streaming do disco).
import struct as _struct  # noqa: E402
_PACK_MAGIC = b"ACOMUP1\x00"
_PACK_MAX_BODY = 600 * 1024 * 1024        # teto de corpo do /pack e /unpack (web; a memória do navegador limita)
_DEV_SESSIONS: dict[str, tuple[float, list, int]] = {}   # token -> (ts, [(relpath, bytes)], size) das árvores
_DEV_TTL = 300.0                          # 5 min (encurtado; a árvore inteira fica em RAM)
_DEV_MAX_SESSIONS = 4
_DEV_MAX_TOTAL_BYTES = 512 * 1024 * 1024  # ORÇAMENTO GLOBAL de bytes retidos entre TODAS as sessões
_DEV_LOCK = _threading.Lock()


async def _read_body_capped(request: Request, cap: int) -> bytes:
    cl = request.headers.get("content-length")
    if cl and cl.isdigit() and int(cl) > cap:
        raise HTTPException(413, "corpo grande demais para a web — use o CLI (tools/acom_pack.py) para backups grandes")
    total, chunks = 0, []
    async for chunk in request.stream():
        total += len(chunk)
        if total > cap:
            raise HTTPException(413, "corpo grande demais para a web — use o CLI para backups grandes")
        chunks.append(chunk)
    body = b"".join(chunks)
    if not body:
        raise HTTPException(400, "corpo vazio")
    return body


def _parse_pack_envelope(body: bytes) -> list[tuple]:
    if len(body) < len(_PACK_MAGIC) + 4 or body[:len(_PACK_MAGIC)] != _PACK_MAGIC:
        raise HTTPException(400, "envelope de upload inválido")
    off = len(_PACK_MAGIC)
    (hl,) = _struct.unpack(">I", body[off:off + 4]); off += 4
    if hl > 8 * 1024 * 1024 or off + hl > len(body):
        raise HTTPException(400, "cabeçalho do envelope inválido")
    try:
        header = json.loads(body[off:off + hl].decode("utf-8"))
        items = header["files"]
    except Exception:
        raise HTTPException(400, "cabeçalho do envelope ilegível")
    off += hl
    files = []
    for it in items:
        n = int(it["len"])
        if n < 0 or off + n > len(body):
            raise HTTPException(400, "tamanhos do envelope não batem com o corpo")
        files.append((str(it["path"]), body[off:off + n]))
        off += n
    if not files:
        raise HTTPException(400, "nenhum arquivo no envelope")
    return files


def _dev_session_put(files: list) -> str:
    now = _time.time()
    size = sum(len(d) for _p, d in files)
    with _DEV_LOCK:
        for k in [k for k, v in list(_DEV_SESSIONS.items()) if now - v[0] > _DEV_TTL]:
            _DEV_SESSIONS.pop(k, None)
        # expulsa (LRU) por contagem E por orçamento GLOBAL de bytes (evita fixar GBs em RAM)
        def _total() -> int:
            return sum(v[2] for v in _DEV_SESSIONS.values())
        while _DEV_SESSIONS and (len(_DEV_SESSIONS) >= _DEV_MAX_SESSIONS
                                 or _total() + size > _DEV_MAX_TOTAL_BYTES):
            _DEV_SESSIONS.pop(min(_DEV_SESSIONS, key=lambda k: _DEV_SESSIONS[k][0]), None)
        tok = _secrets.token_urlsafe(18)
        _DEV_SESSIONS[tok] = (now, files, size)
    return tok


def _dev_session_get(token: str) -> list | None:
    with _DEV_LOCK:
        ent = _DEV_SESSIONS.get(token)
        if ent is None:
            return None
        if _time.time() - ent[0] > _DEV_TTL:
            _DEV_SESSIONS.pop(token, None)
            return None
        return ent[1]


@app.post("/api/device/{slug}/pack")
async def device_pack(slug: str, request: Request):
    """Empacota MUITOS arquivos/pastas (envelope autocontido) num único .acom. X-Inscricao (opcional,
    mín 8) liga o modo cifrado. Devolve o contêiner .acom + relatório em X-Acom-Report."""
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    if not _acom_rate_ok(request):     # throttle: pack constrói/comprime (CPU) e o cifrado força scrypt
        raise HTTPException(429, "muitas operações — aguarde alguns segundos")
    body = await _read_body_capped(request, _PACK_MAX_BODY)
    files = _parse_pack_envelope(body)
    password = request.headers.get("X-Inscricao") or None
    try:
        arch = DEV.load_archive(slug)
    except (FileNotFoundError, ImportError, KeyError) as e:
        raise HTTPException(503, f"empacotador indisponível: {e}")
    try:
        container, report = await run_in_threadpool(
            arch.pack_files, files, password=password, meta={"source": "web"}, untrusted=True)
    except ValueError as e:
        raise HTTPException(400, f"falha ao empacotar: {e}")
    except RuntimeError as e:
        raise HTTPException(501, str(e))
    headers = {"Content-Disposition": _content_disposition("backup.acom"), **_report_header(report)}
    return Response(content=container, media_type="application/octet-stream", headers=headers)


@app.post("/api/device/{slug}/unpack")
async def device_unpack(slug: str, request: Request):
    """Abre um .acom multi-arquivo: verifica cada SHA-256 em memória e devolve o manifesto + um
    token de sessão (10 min) para baixar cada arquivo restaurado. X-Inscricao se cifrado."""
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    if not _acom_rate_ok(request):     # throttle: unpack cifrado força scrypt + descomprime (CPU/RAM)
        raise HTTPException(429, "muitas operações — aguarde alguns segundos")
    body = await _read_body_capped(request, _PACK_MAX_BODY)
    password = request.headers.get("X-Inscricao") or None
    try:
        arch = DEV.load_archive(slug)
    except (FileNotFoundError, ImportError, KeyError) as e:
        raise HTTPException(503, f"empacotador indisponível: {e}")
    try:                               # open_and_extract: 1 só derivação de chave (não deriva scrypt 2x)
        res = await run_in_threadpool(arch.open_and_extract, body, password=password, untrusted=True)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if res.get("listing_locked"):
        raise HTTPException(401, "contêiner cifrado — informe o código de inscrição")
    files = res["files"]
    token = _dev_session_put(files)
    return {"session": token, "encrypted": bool(res.get("encrypted")),
            "files": len(files), "meta_chain": res.get("meta_chain"),
            "entries": res.get("entries", []), "total_bytes": res.get("total_bytes", 0)}


@app.get("/api/device/{slug}/unpack-file")
def device_unpack_file(slug: str, session: str, path: str):
    """Serve UM arquivo restaurado da sessão (o frontend grava a árvore no disco escolhido)."""
    if slug.lower() not in DEV.DEVICES:
        raise HTTPException(404, "dispositivo não encontrado")
    files = _dev_session_get(session)
    if files is None:
        raise HTTPException(410, "sessão expirada — reabra o contêiner")
    for relpath, data in files:
        if relpath == path:
            base = path.rsplit("/", 1)[-1] or "arquivo"
            return Response(content=data, media_type="application/octet-stream",
                            headers={"Content-Disposition": _content_disposition(base)})
    raise HTTPException(404, "arquivo não encontrado na sessão")


@app.post("/api/um/build")
async def um_build(request: Request):
    """Colapsa a Central inteira num tgl.acom cifrado. SÓ ADMIN (o middleware gateia; guarda
    local por defense-in-depth). O código de inscrição vem no header X-Inscricao (nunca em URL/
    log). Devolve o binário para download; o segredo JAMAIS é gravado."""
    _require_admin(request)
    password = request.headers.get("X-Inscricao", "")
    if len(password) < UM.MIN_PASSWORD:
        raise HTTPException(400, f"código de inscrição fraco (mínimo {UM.MIN_PASSWORD} caracteres)")
    try:
        files = await run_in_threadpool(UM.gather_central_tree)
        container = await run_in_threadpool(UM.build, files, password,
                                            {"origin": "central", "n_patents": 16})
    except Exception as e:
        raise HTTPException(500, f"falha ao gerar o tgl.acom: {e}")
    headers = {"Content-Disposition": _content_disposition("tgl.acom"),
               **_report_header({"n_files": len(files), "bytes": len(container),
                                 "sha256": UM.inspect(container)["container_sha256"]})}
    return Response(content=container, media_type="application/octet-stream", headers=headers)


@app.post("/api/um/build-oncologia")
async def um_build_oncologia(request: Request):
    """A 2ª via do botão Um: gera o um.acom da ONCOLOGIA — artefato LIVRE (patrimônio da
    humanidade), cifrado com a chave UNIVERSAL e PÚBLICA. Serve para DEMONSTRAR o ACOM.
    SÓ ADMIN gera (lê os arquivos da Central); a chave é fixa (não vem do cliente)."""
    _require_admin(request)
    try:
        files = await run_in_threadpool(UM.gather_oncologia_tree)
        container = await run_in_threadpool(UM.build, files, UM.ONCOLOGIA_KEY,
                                            {"origin": "central", "artifact": "oncologia-livre"})
    except Exception as e:
        raise HTTPException(500, f"falha ao gerar o um.acom: {e}")
    headers = {"Content-Disposition": _content_disposition("um.acom"),
               **_report_header({"n_files": len(files), "bytes": len(container),
                                 "sha256": UM.inspect(container)["container_sha256"]})}
    return Response(content=container, media_type="application/octet-stream", headers=headers)


# ==================== DESCOMPACTADOR PÚBLICO — abre o tgl.acom sem login ====================
# Rotas /api/acom/* são ISENTAS de login (is_open_path), read-only, em memória, SEM acesso aos
# dados de patente da Central: só operam sobre o arquivo que o visitante envia.
@app.post("/api/acom/inspect")
async def acom_inspect(request: Request):
    """Lê só o cabeçalho público do tgl.acom (o leitor 'enxerga a chave'): não pede senha."""
    if not _acom_rate_ok(request):
        raise HTTPException(429, "muitas tentativas — aguarde um minuto")
    body = await _read_capped_body(request)
    try:
        return await run_in_threadpool(UM.inspect, body)
    except ValueError as e:
        raise HTTPException(400, f"arquivo inválido: {e}")
    except Exception:
        raise HTTPException(400, "arquivo inválido")


@app.post("/api/acom/open")
async def acom_open(request: Request):
    """Decifra (senha no header X-Inscricao) + descomprime + confere todos os SHA-256. Devolve
    a árvore e um token efêmero para ver/baixar cada arquivo. Senha errada → 401 honesto.
    Rate-limit por IP real: o open força scrypt (caro) — anti-DoS e anti-brute-force online."""
    if not _acom_rate_ok(request):
        raise HTTPException(429, "muitas tentativas — aguarde um minuto")
    body = await _read_capped_body(request)
    password = request.headers.get("X-Inscricao", "")
    try:
        opened = await run_in_threadpool(UM.open_container, body, password)
    except PermissionError as e:
        raise HTTPException(401, str(e))
    except ValueError as e:
        raise HTTPException(400, f"não foi possível abrir: {e}")
    except Exception:
        raise HTTPException(400, "não foi possível abrir o arquivo")
    token = _acom_cache_put(opened.pop("_files"))
    opened["session"] = token
    return opened


@app.get("/api/acom/file")
def acom_file(session: str, path: str):
    """Serve UM arquivo de uma sessão aberta (em memória). Guarda anti-traversal pelo nome."""
    files = _acom_cache_get(session)
    if files is None:
        raise HTTPException(404, "sessão expirada — reabra o arquivo")
    data = files.get(path)
    if data is None:
        raise HTTPException(404, "arquivo não encontrado na árvore")
    is_text = path.lower().endswith((".md", ".json", ".yaml", ".yml", ".py", ".txt"))
    headers = {"Content-Disposition": _content_disposition(path.rsplit("/", 1)[-1])}
    return Response(content=data, headers=headers,
                    media_type="text/plain; charset=utf-8" if is_text else "application/octet-stream")


# ---------------- AUTH pela criptografia do operador (ACOM Crypto — Túnel de Hilbert) ----
class LoginBody(BaseModel):
    secret: str = Field(min_length=1, max_length=4096)


@app.get("/api/auth/status")
def auth_status(request: Request):
    st = AUTH.status()
    st["authenticated"] = (not AUTH.AUTH_ENABLED) or AUTH.token_valid(request.cookies.get(AUTH.COOKIE, ""))
    return st


@app.get("/api/auth/me")
def auth_me(request: Request):
    if not AUTH.AUTH_ENABLED:
        return {"authenticated": True, "role": "admin", "name": "local", "uid": "local"}
    payload = AUTH.token_payload(request.cookies.get(AUTH.COOKIE, ""))
    if payload is None:
        raise HTTPException(401, "não autenticado")
    return {"authenticated": True, "role": payload.get("role"), "name": payload.get("sub"),
            "uid": payload.get("uid")}


@app.post("/api/auth/login")
def auth_login(body: LoginBody, request: Request):
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(400, "autenticação por criptografia não está ativa neste servidor")
    ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
    if not AUTH.rate_ok(ip):
        raise HTTPException(429, "muitas tentativas — aguarde alguns minutos")
    AUTH.note_attempt(ip)
    user = AUTH.verify_secret(body.secret)
    if user is None:
        raise HTTPException(401, "segredo incorreto — acesso negado")
    # editor/admin com 2FA ligada: NÃO emite token ainda; manda o código por e-mail
    if AUTH.needs_2fa(user):
        try:
            ch = AUTH.start_2fa(user)
        except (ValueError, RuntimeError) as e:
            raise HTTPException(503, f"2FA indisponível: {e}")
        except Exception:
            raise HTTPException(502, "falha ao enviar o e-mail do código — tente de novo")
        return JSONResponse({"ok": True, "twofa_required": True,
                             "challenge": ch["challenge"], "email_hint": ch["email_hint"]})
    return _session_response(AUTH.issue(user))


def _session_response(tok: dict) -> JSONResponse:
    """Emite o cookie de sessão: __Host- (Secure, Path=/, sem Domain) + SameSite=Strict.
    Apaga o cookie do nome antigo, se o navegador ainda o tiver (não é mais lido)."""
    resp = JSONResponse({"ok": True, "role": tok["role"], "name": tok["name"],
                         "expires_in": tok["expires_in"]})
    resp.set_cookie(AUTH.COOKIE, tok["token"], max_age=tok["expires_in"],
                    httponly=True, samesite="strict", secure=True, path="/")
    resp.delete_cookie(AUTH.LEGACY_COOKIE, path="/", secure=True, httponly=True, samesite="lax")
    return resp


class TwoFABody(BaseModel):
    challenge: str = Field(min_length=1, max_length=200)
    code: str = Field(min_length=1, max_length=12)


@app.post("/api/auth/2fa")
def auth_2fa(body: TwoFABody, request: Request):
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(400, "autenticação por criptografia não está ativa")
    ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
    if not AUTH.rate_ok(ip):
        raise HTTPException(429, "muitas tentativas — aguarde alguns minutos")
    AUTH.note_attempt(ip)
    user = AUTH.verify_2fa(body.challenge, body.code)
    if user is None:
        raise HTTPException(401, "código inválido ou expirado")
    return _session_response(AUTH.issue(user))


@app.post("/api/auth/logout")
def auth_logout():
    resp = JSONResponse({"ok": True})
    # __Host- exige Secure também na remoção (sem Secure o navegador ignora o Set-Cookie)
    resp.delete_cookie(AUTH.COOKIE, path="/", secure=True, httponly=True, samesite="strict")
    resp.delete_cookie(AUTH.LEGACY_COOKIE, path="/", secure=True, httponly=True, samesite="lax")
    return resp


# ---------------- gerência de USUÁRIOS (só admin — o middleware bloqueia o resto) ----
class NewUser(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    role: str = Field(pattern="^(editor|viewer)$")
    email: str = Field(default="", max_length=120)


class RoleBody(BaseModel):
    role: str = Field(pattern="^(editor|viewer)$")


@app.get("/api/users")
def users_list():
    if not AUTH.AUTH_ENABLED:
        return {"enabled": False, "users": [], "roles": list(AUTH.ROLES)}
    return {"enabled": True, "users": AUTH.list_users(), "roles": list(AUTH.ROLES),
            "email_2fa": AUTH.EMAIL_2FA, "smtp_ready": AUTH.smtp_ready()}


@app.post("/api/users")
def users_add(body: NewUser):
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(400, "autenticação por criptografia não está ativa")
    try:
        return AUTH.add_user(body.name, body.role, body.email)   # inclui a CHAVE (mostrada uma vez)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.delete("/api/users/{uid}")
def users_remove(uid: str):
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(400, "autenticação por criptografia não está ativa")
    if not AUTH.remove_user(uid):
        raise HTTPException(404, "usuário não encontrado")
    return {"ok": True}


@app.post("/api/users/{uid}/role")
def users_role(uid: str, body: RoleBody):
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(400, "autenticação por criptografia não está ativa")
    if not AUTH.set_role(uid, body.role):
        raise HTTPException(404, "usuário não encontrado")
    return {"ok": True}


# ---------------- documents (serve extracted text, never the original binary edit) ----
@app.get("/api/documents/{doc_id}/text", response_class=PlainTextResponse)
def document_text(doc_id: int):
    conn = connect()
    r = conn.execute("SELECT rel_path FROM document WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "documento não encontrado")
    txt = C.NORMALIZED / (r["rel_path"] + ".txt")
    if txt.exists():
        return txt.read_text(encoding="utf-8")
    return "(texto normalizado não disponível para este documento)"


@app.get("/api/documents/{doc_id}/file")
def document_file(doc_id: int):
    conn = connect()
    r = conn.execute("SELECT rel_path FROM document WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "documento não encontrado")
    p = C.CENTRAL / r["rel_path"]
    if not p.exists():
        raise HTTPException(404, "arquivo ausente")
    # read-only serve of the original. 21/09/2026: na Central da NUVEM (login da cripto ou
    # Access), o que pode rodar script (HTML, SVG, XML, tipo desconhecido…) sai com CSP
    # 'sandbox' — não roda com os privilégios do cockpit. Ficam fora PDF (o visor já é isolado),
    # imagem raster, vídeo e áudio (o sandbox quebraria o vídeo). A Central LOCAL fica como era.
    headers = {}
    if SEC.SANDBOX_ARQUIVOS and SEC.precisa_sandbox(_mimetypes.guess_type(p.name)[0]):
        headers["Content-Security-Policy"] = SEC.sandbox_csp()
    return FileResponse(str(p), headers=headers)


# ---------------- runs (global execution ledger) ----------------
@app.get("/api/runs")
def runs():
    """Todos os runs de runner (forma=conteúdo) do acervo, mais recentes primeiro."""
    conn = connect()
    data = rows(conn.execute("""
        SELECT r.id, r.patent_id, p.slug, p.display_name, p.role, r.finished_at,
               r.status, r.beta_runtime, r.physical_verdict_allowed, r.tests_passed,
               r.max_verdict, r.result_hash, r.markers
        FROM runner_run r JOIN patent p ON p.id=r.patent_id
        ORDER BY r.finished_at DESC, r.id DESC"""))
    conn.close()
    for d in data:
        d["markers"] = json.loads(d.get("markers") or "[]")
    patents_total = 0
    with_runs = len({d["patent_id"] for d in data})
    conn = connect()
    patents_total = conn.execute("SELECT count(*) FROM patent").fetchone()[0]
    conn.close()
    return {"runs": data, "runs_total": len(data),
            "patents_with_runs": with_runs, "patents_total": patents_total,
            "aviso": "Runners demonstram a LÓGICA da invenção. "
                     "physical_verdict_allowed=false em todo o acervo: simulação nunca valida física."}


# ---------------- docket (legal funnel) ----------------
@app.get("/api/docket")
def docket():
    conn = connect()
    data = rows(conn.execute(f"""
        SELECT d.patent_id, p.slug, p.role, d.kind, d.label, d.due_date, d.status,
               d.legal_note, CAST(julianday(d.due_date)-julianday('now') AS INT) AS days_remaining,
               {URGENCY_SQL} AS urgency
        FROM deadline d JOIN patent p ON p.id=d.patent_id
        ORDER BY (d.due_date IS NULL), d.due_date"""))
    conn.close()
    return {"aviso": C.AVISO_LEGAL, "deadlines": data}


# ---------------- pendencias ----------------
@app.get("/api/pendencias")
def pendencias():
    conn = connect()
    data = rows(conn.execute("SELECT * FROM pendencia ORDER BY id"))
    for d in data:
        d["markers"] = json.loads(d.get("markers") or "[]")
        d["patents"] = [r["patent_id"] for r in conn.execute(
            "SELECT patent_id FROM pendencia_patent WHERE pendencia_id=?", (d["id"],))]
    conn.close()
    return data


# ---------------- TGL core ----------------
@app.get("/api/tgl-core", response_class=PlainTextResponse)
def tgl_core():
    return C.TGL_CORE.read_text(encoding="utf-8") if C.TGL_CORE.exists() else ""


# ---------------- TGL atlas (a memória holográfica) ----------------
@app.get("/api/tgl-atlas", response_class=PlainTextResponse)
def tgl_atlas():
    return C.TGL_ATLAS.read_text(encoding="utf-8") if C.TGL_ATLAS.exists() else ""


# ---------------- notes: write-through to .md, then reindex ----------------
def _req_user(request: Request) -> str:
    """Quem escreveu (para o overlay da nuvem): 'local' sem auth; senão o nome do token."""
    if not AUTH.AUTH_ENABLED:
        return "local"
    payload = AUTH.token_payload(request.cookies.get(AUTH.COOKIE, ""))
    return (payload or {}).get("sub") or (payload or {}).get("uid") or "?"


def _cloud_flag(rec) -> bool | None:
    """None quando o dual-write está desligado (local); True/False quando ligado — False
    sinaliza que o overlay NÃO persistiu (teto/erro) apesar da escrita primária ter ido."""
    return None if not CW.enabled() else (rec is not None)


def _require_admin(request: Request) -> None:
    """Guarda local dos endpoints do overlay (defense-in-depth; o middleware já bloqueia
    não-admin via can_request). Modo local sem auth = operador na própria máquina."""
    if not AUTH.AUTH_ENABLED:
        return
    payload = AUTH.token_payload(request.cookies.get(AUTH.COOKIE, ""))
    if payload is None or payload.get("role") != "admin":
        raise HTTPException(403, "somente admin")


class NoteToggle(BaseModel):
    active: bool


@app.post("/api/notes/{note_id}/active")
def toggle_note(note_id: int, body: NoteToggle, request: Request):
    conn = connect()
    n = conn.execute("SELECT * FROM note WHERE id=?", (note_id,)).fetchone()
    conn.close()
    if not n:
        raise HTTPException(404, "nota não encontrada")
    md = C.CENTRAL / n["source_file"]
    if not md.exists():
        raise HTTPException(404, "arquivo de notas ausente")
    lines = md.read_text(encoding="utf-8").splitlines(keepends=True)
    idx = n["line_ref"] - 1
    if idx < 0 or idx >= len(lines):
        raise HTTPException(409, "linha da nota fora de sincronia — rode reindex")
    line = lines[idx]
    # a linha do arquivo TEM de ser a que o índice acha que é: o content_hash da linha crua
    # (sem \n/\r, como o parser calcula em reindex._sha_text) deve bater — senão o .md mudou
    # sob o índice velho e mutar por line_ref corromperia a linha errada.
    raw = line.splitlines()[0] if line.splitlines() else ""
    if REINDEX_SHA(raw) != n["content_hash"]:
        raise HTTPException(409, "linha da nota fora de sincronia — rode reindex")
    line_key = CW.line_key(line)                      # chave estável ANTES de mudar a flag
    new_flag = "true" if body.active else "false"
    if re.search(r"\(active\s*=\s*(true|false)\)", line, re.I):
        line = re.sub(r"\(active\s*=\s*(true|false)\)",
                      f"(active={new_flag})", line, flags=re.I)
    else:  # inject flag right after the checkbox
        line = re.sub(r"(-\s*\[[ xX]\]\s*)", rf"\1(active={new_flag}) ", line, count=1)
    lines[idx] = line
    md.write_text("".join(lines), encoding="utf-8")  # filesystem is the source of truth
    rec = CW.record("note_toggle", {"source_file": n["source_file"], "line_key": line_key,
                                    "source_section": n["source_section"], "active": body.active},
                    _req_user(request))
    reindex(force=True)                               # re-sync the index
    return {"ok": True, "note_id": note_id, "active": body.active,
            "wrote": n["source_file"], "cloud_persisted": _cloud_flag(rec)}


class NewNote(BaseModel):
    patent_id: str = Field(max_length=64)
    tipo: str = Field(max_length=32)   # nota|sugestao|instrucao|tarefa|bloqueio|pergunta
    text: str = Field(max_length=20_000)  # teto: evita disk-fill DoS por texto ilimitado
    active: bool = True


SECTION_FOR_TIPO = {
    "nota": "Notas livres", "sugestao": "Sugestões de melhoria",
    "instrucao": "Instruções próxima etapa", "tarefa": "Tarefas",
    "bloqueio": "Bloqueios", "pergunta": "Perguntas ao Claude Code",
}


@app.post("/api/notes")
def add_note(body: NewNote, request: Request):
    conn = connect()
    r = conn.execute("SELECT dir_name FROM patent WHERE id=?", (body.patent_id,)).fetchone()
    conn.close()
    if not r:
        raise HTTPException(404, "patente não encontrada")
    section = SECTION_FOR_TIPO.get(body.tipo)
    if not section:
        raise HTTPException(400, "tipo inválido")
    md = C.PATENTS_DIR / r["dir_name"] / "notes" / "initial_notes.md"
    text = md.read_text(encoding="utf-8") if md.exists() else ""
    lines = text.splitlines(keepends=True)
    flag = "true" if body.active else "false"
    new_item = f"- [ ] (active={flag}) {body.text.strip()}\n"
    # insert after the matching section header
    out, inserted = [], False
    for ln in lines:
        out.append(ln)
        if not inserted and re.match(rf"##\s+{re.escape(section)}\s*$", ln.strip()):
            out.append(new_item)
            inserted = True
    if not inserted:  # section missing → append it
        out.append(f"\n## {section}\n{new_item}")
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text("".join(out), encoding="utf-8")
    rec = CW.record("note_add", {"dir_name": r["dir_name"], "section": section,
                                 "text": body.text.strip(), "active": body.active},
                    _req_user(request))
    reindex(force=True)
    return {"ok": True, "wrote": str(md.relative_to(C.CENTRAL)), "cloud_persisted": _cloud_flag(rec)}


# ---------------- prompt compiler ----------------
@app.post("/api/compile")
def compile_active(request: Request):
    conn = connect()
    active = rows(conn.execute("""
        SELECT n.id AS note_id, n.patent_id, n.tipo, n.text, n.markers,
               p.slug, p.title_54, p.class_id
        FROM note n JOIN patent p ON p.id=n.patent_id
        WHERE n.active=1 AND n.done=0
        ORDER BY p.class_id, p.id, n.tipo"""))
    conn.close()
    result = compile_prompt(active)
    rec = CW.record("compiled", {"filename": result["filename"], "body": result["body"]},
                    _req_user(request))
    reindex(force=True)  # index the new compiled_prompt file
    return {"filename": result["filename"], "path": result["path"],
            "note_count": len(active), "sha256": result["sha256"],
            "body_preview": result["body"][:1200], "cloud_persisted": _cloud_flag(rec)}


@app.get("/api/compiled")
def compiled_list():
    out = []
    for f in sorted(C.COMPILED_PROMPTS.glob("*_CLAUDE_CODE_TASK.md"), reverse=True):
        out.append({"filename": f.name, "size": f.stat().st_size})
    return out


@app.get("/api/compiled/{filename}", response_class=PlainTextResponse)
def compiled_get(filename: str):
    """Serve APENAS um prompt compilado (basename *_CLAUDE_CODE_TASK.md) confinado em
    COMPILED_PROMPTS. Endurecido contra leitura arbitraria: no Windows, unir a base com um
    caminho ABSOLUTO descarta a base — por isso exigimos basename puro (nome == filename) +
    confinamento por resolve()/is_relative_to + guard de confidencial (nunca 'C:\\...' nem '..')."""
    # 1) basename puro: barra/contrabarra/letra-de-drive/traversal viram nome != filename -> 404
    if Path(filename).name != filename or not filename.endswith("_CLAUDE_CODE_TASK.md"):
        raise HTTPException(404, "não encontrado")
    base = C.COMPILED_PROMPTS.resolve()
    p = (base / filename).resolve()
    # 2) confinamento real (is_relative_to evita bug de prefixo-irmao do startswith)
    if not p.is_relative_to(base) or not p.is_file():
        raise HTTPException(404, "não encontrado")
    # 3) guard de confidencial (defense-in-depth)
    if any(c in p.name.lower() for c in _CONFIDENTIAL):
        raise HTTPException(403, "arquivo não servível")
    return p.read_text(encoding="utf-8")


# ---------------- overlay de escrita da nuvem (colheita; SÓ ADMIN) ----------------
class AckBody(BaseModel):
    ids: list[str] = Field(max_length=10_000)


@app.get("/api/cloud-writes")
def cloud_writes_list(request: Request):
    """Registros de escrita pendentes de colheita (dual-write da nuvem). Só admin —
    o middleware (can_request) bloqueia os demais; guarda local por defense-in-depth."""
    _require_admin(request)
    recs = CW.pending_records()
    return {"enabled": CW.enabled(), "pending": len(recs), "records": recs}


@app.post("/api/cloud-writes/ack")
def cloud_writes_ack(body: AckBody, request: Request):
    """Reconhece registros já colhidos+inscritos localmente (saem do overlay)."""
    _require_admin(request)
    return CW.ack(body.ids)


# ---------------- usuários do APP IALD (aba da patente BR102026003443-6) ----------------
# Operador: /api/iald-app/* (só admin "operador" + origem exata + step-up; fail-closed sem login).
# IALD: POST /api/iald-sync/puxar (HMAC, sem cookie). A Central só ENFILEIRA; a IALD executa.
from . import iald_app_users as IAU  # noqa: E402

app.include_router(IAU.router)


# ---------------- static frontend (built) ----------------
from starlette.exceptions import HTTPException as StarletteHTTPException  # noqa: E402

_dist = C.CENTRAL / "frontend" / "dist"


class SPAStaticFiles(StaticFiles):
    """Fallback de SPA: rota interna desconhecida (ex.: /fronteira, /patents/...) serve o
    index.html — refresh e deep-link funcionam local e na nuvem. O fallback é RESTRITO:
    só para caminhos de navegação (sem extensão de arquivo) fora de api/ e assets/ —
    asset ausente segue 404 de verdade (jamais HTML com cache imutável) e /api/*
    desconhecido segue 404 JSON. O index.html do fallback sai com no-store."""
    @staticmethod
    def _is_spa_route(path: str) -> bool:
        p = path.replace("\\", "/").lstrip("/")   # StaticFiles normaliza com os.sep (Windows: '\')
        if p == "api" or p.startswith("api/") or p.startswith("assets/"):
            return False
        last = p.rsplit("/", 1)[-1]
        return "." not in last

    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
        except StarletteHTTPException as e:
            if e.status_code != 404 or not self._is_spa_route(path):
                raise
            response = None
        if response is None or (response.status_code == 404 and self._is_spa_route(path)):
            response = await super().get_response("index.html", scope)
            response.headers["Cache-Control"] = "no-store, must-revalidate"
        return response


if _dist.exists():
    app.mount("/", SPAStaticFiles(directory=str(_dist), html=True), name="frontend")


@app.get("/")
def root():
    if _dist.exists():
        return FileResponse(str(_dist / "index.html"))
    return {"service": "Central de Patentes TGL", "frontend": "não compilado ainda",
            "api": "/api/health"}

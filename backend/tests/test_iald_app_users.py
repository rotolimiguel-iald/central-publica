# -*- coding: utf-8 -*-
"""Testes da aba "Usuários do app IALD" (iald_app_users.py) + o endurecimento que vai junto.

Roda SEM uvicorn e SEM tocar a porta 8765: um cliente ASGI mínimo (sem httpx) chama o app
dentro do processo. Dois modos, cada um num subprocesso próprio — authn/security leem o
ambiente na importação:
  • local — sem login (a Central do PC): toda rota nova do operador RECUSA (fail-closed);
  • auth  — como no Render (CENTRAL_AUTH=crypto + segredo DESCARTÁVEL gerado aqui).
Todo arquivo que o app gravaria (users.json, audit.log, iald_app/) é desviado para um
diretório temporário; nada toca backend/data de verdade (o runner confere por stat).

    backend\\.venv\\Scripts\\python.exe backend\\tests\\test_iald_app_users.py

Também é coletável pelo pytest (test_modo_local / test_modo_auth), se instalado.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CAMINHO_SYNC = "/api/iald-sync/puxar"
ORIGEM = "https://central.iald.ia.br"
ORIGEM_RENDER = "https://central-de-patentes.onrender.com"


# ════════════════════════════════════════════════════════════════════ runner
def _ambiente_limpo(modo: str, tmp: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CENTRAL_") and k not in ("RENDER", "CF_ACCESS_TEAM_DOMAIN", "CF_ACCESS_AUD")}
    env["CENTRAL_TESTE_TMP"] = tmp
    env["CENTRAL_RATE_MAX"] = "0"          # o limite global por IP atrapalharia a rajada de testes
    env["PYTHONIOENCODING"] = "utf-8"
    if modo == "auth":
        env["CENTRAL_AUTH"] = "crypto"
        env["CENTRAL_CRYPTO_SECRET"] = "teste-descartavel-" + secrets.token_urlsafe(24)
    return env


def _stat_dados_reais() -> dict:
    d = RAIZ / "backend" / "data"
    out = {}
    for nome in ("users.json", "iald_app", "cloud_writes"):
        p = d / nome
        out[nome] = (p.exists(), p.stat().st_size if p.exists() and p.is_file() else None,
                     p.stat().st_mtime_ns if p.exists() else None)
    return out


def _rodar(modo: str) -> int:
    tmp = tempfile.mkdtemp(prefix=f"central_teste_{modo}_")
    try:
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--modo", modo],
                           cwd=str(RAIZ), env=_ambiente_limpo(modo, tmp))
        return r.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_modo_local():
    assert _rodar("local") == 0


def test_modo_auth():
    assert _rodar("auth") == 0


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "--modo":
        return rodar_modo(sys.argv[2])
    antes = _stat_dados_reais()
    rc = 0
    for modo in ("local", "auth"):
        rc |= _rodar(modo)
    depois = _stat_dados_reais()
    if antes != depois:
        print(f"FALHA: backend/data real mudou durante os testes: {antes} -> {depois}")
        rc |= 1
    else:
        print("ok: backend/data real intocado (users.json, iald_app/, cloud_writes/)")
    print("RESULTADO GERAL:", "PASSOU" if rc == 0 else "FALHOU")
    return rc


# ════════════════════════════════════════════════════════════════════ cliente ASGI mínimo
class Resp:
    def __init__(self, status: int, headers: list, body: bytes):
        self.status = status
        self.headers = [(k.decode("latin-1").lower(), v.decode("latin-1")) for k, v in headers]
        self.body = body

    def h(self, nome: str):
        nome = nome.lower()
        for k, v in self.headers:
            if k == nome:
                return v
        return None

    def todos(self, nome: str) -> list:
        return [v for k, v in self.headers if k == nome.lower()]

    def json(self):
        return json.loads(self.body.decode("utf-8"))

    def __repr__(self):
        return f"<{self.status} {self.body[:200]!r}>"


def chamar(app, metodo: str, caminho: str, headers: dict | None = None, corpo: bytes = b"",
           consulta: str = "") -> Resp:
    inicio, body = asyncio.run(_chamar_async(app, metodo, caminho, headers, corpo, consulta))
    return Resp(inicio.get("status", 0), inicio.get("headers", []), body)


def chamar_juntos(app, pedidos: list) -> list:
    """Dispara VÁRIAS requisições no MESMO laço de eventos, ao mesmo tempo (asyncio.gather):
    é assim que um atacante com a sessão roubada tentaria passar por baixo de uma trava."""
    async def todos():
        return await asyncio.gather(*(_chamar_async(app, *p) for p in pedidos))
    return [Resp(i.get("status", 0), i.get("headers", []), b) for i, b in asyncio.run(todos())]


async def _chamar_async(app, metodo: str, caminho: str, headers: dict | None = None, corpo: bytes = b"",
                        consulta: str = ""):
    hs = {"host": "central.iald.ia.br"}
    for k, v in (headers or {}).items():
        if v is not None:
            hs[k.lower()] = v
    if corpo and "content-length" not in hs:
        hs["content-length"] = str(len(corpo))
    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"}, "http_version": "1.1",
             "method": metodo, "scheme": "https", "path": caminho, "raw_path": caminho.encode(),
             "query_string": consulta.encode(), "root_path": "",
             "headers": [(k.encode("latin-1"), v.encode("latin-1")) for k, v in hs.items()],
             "client": ("203.0.113.9", 50000), "server": ("central.iald.ia.br", 443)}

    async def run():
        entregue = False
        fim = asyncio.Event()
        inicio: dict = {}
        partes: list = []

        async def receive():
            nonlocal entregue
            if not entregue:
                entregue = True
                return {"type": "http.request", "body": corpo, "more_body": False}
            await fim.wait()
            return {"type": "http.disconnect"}

        async def send(msg):
            if msg["type"] == "http.response.start":
                inicio.update(msg)
            elif msg["type"] == "http.response.body":
                partes.append(msg.get("body", b""))
                if not msg.get("more_body"):
                    fim.set()

        await app(scope, receive, send)
        fim.set()
        return inicio, b"".join(partes)

    return await run()


# ════════════════════════════════════════════════════════════════════ mini-framework
def igual(a, b, msg=""):
    if a != b:
        raise AssertionError(f"{msg}: esperado {b!r}, veio {a!r}")


def verdade(x, msg=""):
    if not x:
        raise AssertionError(msg or "condição falsa")


def status_em(r: Resp, esperados, msg=""):
    if r.status not in (esperados if isinstance(esperados, (tuple, list, set)) else (esperados,)):
        raise AssertionError(f"{msg}: status {r.status} não está em {esperados}; corpo {r.body[:300]!r}")


# ════════════════════════════════════════════════════════════════════ modo
def rodar_modo(modo: str) -> int:
    sys.path.insert(0, str(RAIZ))
    tmp = Path(os.environ["CENTRAL_TESTE_TMP"])
    from backend.app import main as M
    from backend.app import authn as AUTH
    from backend.app import security as SEC
    from backend.app import iald_app_users as IAU

    # ── isola TODO o disco que o app tocaria ──
    SEC._AUDIT_PATH = tmp / "audit.log"
    AUTH.USERS_FILE = tmp / "users.json"
    IAU.DIR = tmp / "iald_app"
    relogio = [time.time()]
    IAU._agora = lambda: relogio[0]
    ctx = {"M": M, "AUTH": AUTH, "SEC": SEC, "IAU": IAU, "tmp": tmp, "relogio": relogio}

    esperado_auth = (modo == "auth")
    if AUTH.AUTH_ENABLED != esperado_auth:
        print(f"FALHA: modo {modo} mas AUTH_ENABLED={AUTH.AUTH_ENABLED}")
        return 1
    casos = CASOS_AUTH if esperado_auth else CASOS_LOCAL
    if esperado_auth:
        _preparar_auth(ctx)
    falhas = 0
    for fn in casos:
        try:
            fn(ctx)
            print(f"  ok   [{modo}] {fn.__name__}")
        except Exception:  # noqa: BLE001
            falhas += 1
            print(f"  FALHA [{modo}] {fn.__name__}")
            traceback.print_exc()
    total = len(casos)
    print(f"[{modo}] {total - falhas}/{total} passaram")
    return 1 if falhas else 0


# ════════════════════════════════════════════════════════════════════ auxiliares
def _token(AUTH, uid: str, role: str, nome: str = "x") -> str:
    """Token assinado como authn.issue, com um jti para que duas sessões no mesmo segundo
    sejam sessões DIFERENTES (o limite de step-up é por sessão)."""
    agora = int(time.time())
    payload = {"sub": nome, "uid": uid, "role": role, "iat": agora, "exp": agora + 3600,
               "scheme": "acom-crypto-hilbert-tunnel", "jti": secrets.token_hex(8)}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    return body.decode() + "." + hmac.new(AUTH._server_key(), body, hashlib.sha256).hexdigest()


def _cookie(AUTH, token: str) -> str:
    return f"{AUTH.COOKIE}={token}"


def _h_op(ctx, token=None, origem=ORIGEM, acao="1", ctype="application/json", sfs="same-origin",
          **extra) -> dict:
    h = {"cookie": _cookie(ctx["AUTH"], token or ctx["tok_op"]), "x-central-acao": acao,
         "origin": origem, "content-type": ctype, "sec-fetch-site": sfs}
    h.update(extra)
    return {k: v for k, v in h.items() if v is not None}


def _cmd(ctx, acao, alvo, chave=None, nota=None, token=None, **hextra) -> Resp:
    corpo = {"acao": acao, "alvo": alvo, "chave": ctx["segredo"] if chave is None else chave}
    if nota is not None:
        corpo["nota"] = nota
    return chamar(ctx["M"].app, "POST", "/api/iald-app/comandos", _h_op(ctx, token=token, **hextra),
                  json.dumps(corpo).encode())


def _estado(ctx, token=None) -> Resp:
    return chamar(ctx["M"].app, "GET", "/api/iald-app/estado",
                  _h_op(ctx, token=token, origem=None, ctype=None))


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sync(ctx, obj=None, *, corpo=None, segredo=None, ts=None, nonce=None, metodo_ass="POST",
          caminho_ass=CAMINHO_SYNC, corpo_ass=None, ctype="application/json", consulta="",
          sem=(), assinatura=None) -> tuple:
    """Assina INDEPENDENTEMENTE do módulo (o teste é o contrato):
    v1=HMAC-SHA256(segredo, 'iald->central\\n'+M+'\\n'+P+'\\n'+ts+'\\n'+nonce+'\\n'+sha256hex(corpo))."""
    if corpo is None:
        corpo = json.dumps(obj if obj is not None else {"ultimo_seq_executado": 0}).encode("utf-8")
    segredo = ctx["seg_sync"] if segredo is None else segredo
    ts = str(int(ctx["relogio"][0])) if ts is None else ts
    nonce = secrets.token_hex(16) if nonce is None else nonce
    msg = "\n".join(("iald->central", metodo_ass, caminho_ass, ts, nonce,
                     _sha(corpo if corpo_ass is None else corpo_ass)))
    sig = hmac.new(segredo.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()
    h = {"content-type": ctype, "x-iald-sync-ts": ts, "x-iald-sync-nonce": nonce,
         "x-iald-sync-assinatura": assinatura if assinatura is not None else "v1=" + sig}
    for k in sem:
        h.pop(k, None)
    return chamar(ctx["M"].app, "POST", CAMINHO_SYNC, h, corpo, consulta), nonce


def _resposta_assinada_ok(ctx, r: Resp, nonce: str) -> bool:
    ts = r.h("x-central-ts")
    ass = r.h("x-central-assinatura") or ""
    if not ts or not ass.startswith("v1="):
        return False
    msg = "\n".join(("central->iald", ts, nonce, _sha(r.body)))
    esperado = hmac.new(ctx["seg_sync"].encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, ass[3:])


P1 = "ped_20260921100000_a1b2c3"
P2 = "ped_20260921100500_0f0f0f"
P3 = "ped_20260920090000_ffffff"      # recusado
PX = "ped_20260921110000_123456"      # não existe no retrato
PEDIDOS_EXTRA = [f"ped_20260921{120000 + i:06d}_{i:06x}" for i in range(40)]


def _snapshot_rico() -> dict:
    return {
        "gerado_em": "2026-09-21T15:00:00-03:00", "seq": 7,
        "tgl_hash": "NAO-PODE-FICAR", "extra_topo": 1,
        "pedidos": [
            {"id": P1, "status": "pendente", "nome": "Maria‮ evil\x07 da​ Silva",
             "email": "[dado pessoal removido]", "provedor": "apple", "criado": "2026-09-21T10:00:00",
             "ultima_tentativa": "2026-09-21T10:05:00", "tentativas": 2, "sugestao": "maria",
             "sub": "001234.SUB-NAO-PODE", "ip_chave": "IPCHAVE-NAO-PODE", "cota_chave": "COTA-NAO-PODE",
             "superficie": "app", "decidido_por": "x", "nota": "n"},
            {"id": "../../etc/passwd", "status": "pendente"},
            {"id": P2, "status": "pendente", "nome": "Zé", "email": "[dado pessoal removido]", "provedor": "google"},
            {"id": P3, "status": "recusado", "nome": "Recusado", "email": "r***@x.com"},
            {"id": P1, "status": "pendente"},                       # duplicado → cai
            {"id": "ped_20260921100000_ZZZZZZ", "status": "pendente"},
        ] + [{"id": p, "status": "pendente", "nome": f"extra {i}"} for i, p in enumerate(PEDIDOS_EXTRA)],
        "usuarios": [
            {"username": "joao", "status": "ativo", "nome": "João", "email": "jo***@icloud.com",
             "provedor": "apple", "criado": "2026-09-01", "tgl_hash": "TGL-NAO-PODE",
             "identidades": [{"provedor": "apple", "sub": "SUB2-NAO-PODE"}], "plano": "assinante",
             "uso_tokens": {"dia": 1}, "admin": False, "acesso_nativa": True},
            {"username": "bia.b", "status": "bloqueado", "nome": "Bia", "bloqueado_em": "2026-09-20T08:00:00Z"},
            {"username": "operador_iald", "status": "protegido", "nome": "Operador"},
            {"username": "carla-2", "status": "ativo", "email": "c@d.co"},
            {"username": "Bad Name", "status": "ativo"},
            {"username": "x", "status": "ativo"},
            {"username": "ok_user", "status": "admin"},
            {"username": "..hidden", "status": "ativo"},
        ],
    }


def _preparar_auth(ctx):
    AUTH = ctx["AUTH"]
    ctx["segredo"] = os.environ["CENTRAL_CRYPTO_SECRET"]
    ctx["chave_editor"] = secrets.token_urlsafe(18)
    ctx["chave_viewer"] = secrets.token_urlsafe(18)
    ctx["uid_editor"] = "u_" + secrets.token_hex(6)
    ctx["uid_viewer"] = "u_" + secrets.token_hex(6)
    AUTH._save_users([
        {"uid": ctx["uid_editor"], "name": "editora", "role": "editor", "email": "",
         "verifier": AUTH._verifier(ctx["chave_editor"], ctx["uid_editor"]), "created_at": 0},
        {"uid": ctx["uid_viewer"], "name": "leitor", "role": "viewer", "email": "",
         "verifier": AUTH._verifier(ctx["chave_viewer"], ctx["uid_viewer"]), "created_at": 0},
    ])
    ctx["tok_op"] = _token(AUTH, "operador", "admin", "operador")
    ctx["tok_editor"] = _token(AUTH, ctx["uid_editor"], "editor", "editora")
    ctx["tok_viewer"] = _token(AUTH, ctx["uid_viewer"], "viewer", "leitor")
    ctx["seg_sync"] = secrets.token_hex(32)       # 64 bytes ASCII; descartável
    os.environ.pop("CENTRAL_IALD_SYNC_SEGREDO", None)


def _todos_os_bytes(tmp: Path) -> bytes:
    out = b""
    for p in tmp.rglob("*"):
        if p.is_file():
            out += p.read_bytes()
    return out


def _uid_rotas():
    return ("/api/iald-app/estado", "/api/iald-app/comandos", "/api/iald-app/comandos/" + str(uuid.uuid4()))


# ════════════════════════════════════════════════════════════════════ CASOS — modo LOCAL
CASOS_LOCAL: list = []


def local(fn):
    CASOS_LOCAL.append(fn)
    return fn


@local
def local_rotas_do_operador_recusam(ctx):
    M = ctx["M"]
    h = {"cookie": "__Host-central_session=qualquer", "x-central-acao": "1", "origin": ORIGEM,
         "content-type": "application/json", "sec-fetch-site": "same-origin"}
    corpo = json.dumps({"acao": "aprovar", "alvo": P1, "chave": "x"}).encode()
    status_em(chamar(M.app, "GET", "/api/iald-app/estado", h), (403, 503), "estado")
    status_em(chamar(M.app, "POST", "/api/iald-app/comandos", h, corpo), (403, 503), "comandos")
    status_em(chamar(M.app, "GET", "/api/iald-app/comandos/" + str(uuid.uuid4()), h), (403, 503), "comando")
    status_em(chamar(M.app, "GET", "/api/iald-app/estado", {}), (403, 503), "estado sem nada")
    verdade(not (ctx["tmp"] / "iald_app").exists(), "nada pode ser gravado no modo local")


@local
def local_sync_recusa_mesmo_com_segredo(ctx):
    os.environ["CENTRAL_IALD_SYNC_SEGREDO"] = secrets.token_hex(32)
    try:
        ctx["seg_sync"] = os.environ["CENTRAL_IALD_SYNC_SEGREDO"]
        r, _ = _sync(ctx)
        igual(r.status, 503, "sync na Central sem login")
    finally:
        os.environ.pop("CENTRAL_IALD_SYNC_SEGREDO", None)
    r, _ = _sync(ctx)
    igual(r.status, 503, "sync sem segredo")
    verdade(not (ctx["tmp"] / "iald_app").exists(), "nada gravado")


@local
def local_cabecalhos_inofensivos(ctx):
    M, SEC = ctx["M"], ctx["SEC"]
    r = chamar(M.app, "GET", "/")
    status_em(r, 200, "raiz")
    igual(r.h("strict-transport-security"), None, "sem HSTS no local")
    igual(r.h("content-security-policy"), SEC.FRAME_CSP, "CSP local = só frame-ancestors (Lar Miguel)")
    igual(r.h("x-content-type-options"), "nosniff", "nosniff")
    status_em(chamar(M.app, "GET", "/openapi.json"), 200, "docs seguem no local")


@local
def local_documento_como_antes_sem_sandbox(ctx):
    """A Central LOCAL (127.0.0.1, sem login) serve o acervo como sempre: sem privilégio a
    proteger, os painéis HTML do operador seguem rodando em casa."""
    M, SEC = ctx["M"], ctx["SEC"]
    igual(SEC.SANDBOX_ARQUIVOS, False, "sandbox desligado no local")
    for nome, conteudo in (("painel.html", b"<html><script>1</script></html>"), ("v.mp4", b"\x00" * 64),
                           ("desenho.svg", b"<svg xmlns='http://www.w3.org/2000/svg'/>")):
        arq = ctx["tmp"] / nome
        arq.write_bytes(conteudo)
        r = _servir_documento(M, arq)
        igual(r.status, 200, nome)
        igual(r.h("content-security-policy"), SEC.FRAME_CSP, f"{nome}: CSP local de sempre")


@local
def local_cors_excluido_nas_rotas_novas(ctx):
    M = ctx["M"]
    pre = {"origin": "https://iald.ia.br", "access-control-request-method": "POST",
           "access-control-request-headers": "content-type,x-iald-sync-ts"}
    for caminho in (CAMINHO_SYNC, "/api/iald-app/comandos"):
        r = chamar(M.app, "OPTIONS", caminho, pre)
        igual(r.h("access-control-allow-origin"), None, f"preflight {caminho} sem CORS")
    r = chamar(M.app, "OPTIONS", "/api/acom/inspect", pre)
    igual(r.h("access-control-allow-origin"), "https://iald.ia.br", "CORS do acom segue")


# ════════════════════════════════════════════════════════════════════ CASOS — modo AUTH
CASOS_AUTH: list = []


def auth(fn):
    CASOS_AUTH.append(fn)
    return fn


@auth
def auth_sem_cookie_401(ctx):
    M = ctx["M"]
    for caminho in _uid_rotas():
        metodo = "POST" if caminho.endswith("/comandos") else "GET"
        r = chamar(M.app, metodo, caminho, {"x-central-acao": "1", "origin": ORIGEM,
                                            "content-type": "application/json"}, b"{}")
        igual(r.status, 401, caminho)
        igual(r.h("strict-transport-security"), "max-age=31536000; includeSubDomains",
              "a recusa do portão também leva HSTS")


@auth
def auth_viewer_e_editor_403(ctx):
    M = ctx["M"]
    for quem in ("tok_viewer", "tok_editor"):
        tok = ctx[quem]
        igual(_estado(ctx, token=tok).status, 403, f"estado {quem}")
        igual(_cmd(ctx, "aprovar", P1, token=tok).status, 403, f"comando {quem}")
        igual(chamar(M.app, "GET", "/api/iald-app/comandos/" + str(uuid.uuid4()),
                     _h_op(ctx, token=tok, origem=None, ctype=None)).status, 403, f"get comando {quem}")
        igual(chamar(M.app, "GET", "/api/audit", {"cookie": _cookie(ctx["AUTH"], tok)}).status, 403,
              f"/api/audit {quem}")
    igual(chamar(M.app, "GET", "/api/audit", {"cookie": _cookie(ctx["AUTH"], ctx["tok_op"])}).status,
          200, "/api/audit operador")
    # a regra de papel do PORTÃO (authn.can_request), sem a defesa em profundidade dos handlers
    AUTH = ctx["AUTH"]
    for papel in ("viewer", "editor"):
        for metodo, caminho in (("GET", "/api/iald-app/estado"), ("POST", "/api/iald-app/comandos"),
                                ("GET", "/api/iald-app/comandos/x"), ("GET", "/api/audit")):
            igual(AUTH.can_request({"role": papel}, metodo, caminho), False, f"{papel} {metodo} {caminho}")
    igual(AUTH.can_request({"role": "admin"}, "POST", "/api/iald-app/comandos"), True, "admin no portão")
    igual(AUTH.is_open_path(CAMINHO_SYNC), True, "sync sem cookie no portão")
    igual(AUTH.is_open_path("/api/iald-app/estado"), False, "operador com cookie no portão")


@auth
def auth_admin_com_uid_forjado_403(ctx):
    tok = _token(ctx["AUTH"], ctx["uid_editor"], "admin", "editora")
    igual(_estado(ctx, token=tok).status, 403, "admin que não é o operador")


@auth
def auth_guardas_de_origem_e_tipo(ctx):
    M = ctx["M"]
    app = M.app
    ok_get = _h_op(ctx, origem=None, ctype=None)
    igual(chamar(app, "GET", "/api/iald-app/estado", ok_get).status, 200, "estado ok")
    sem_hdr = dict(ok_get)
    sem_hdr.pop("x-central-acao")
    igual(chamar(app, "GET", "/api/iald-app/estado", sem_hdr).status, 403, "GET sem X-Central-Acao")
    igual(chamar(app, "GET", "/api/iald-app/estado", {**ok_get, "sec-fetch-site": "same-site"}).status,
          403, "GET same-site")
    igual(chamar(app, "GET", "/api/iald-app/estado", {**ok_get, "origin": "https://demo.iald.ia.br"}).status,
          403, "GET origem irmã")
    corpo = json.dumps({"acao": "aprovar", "alvo": P1, "chave": ctx["segredo"]}).encode()
    casos = [
        ("sem Origin", _h_op(ctx, origem=None), 403),
        ("Origin irmã", _h_op(ctx, origem="https://demo.iald.ia.br"), 403),
        ("Origin raiz", _h_op(ctx, origem="https://iald.ia.br"), 403),
        ("Origin sufixo", _h_op(ctx, origem="https://central.iald.ia.br.evil.example"), 403),
        ("Origin http", _h_op(ctx, origem="http://central.iald.ia.br"), 403),
        ("Origin null", _h_op(ctx, origem="null"), 403),
        ("sem X-Central-Acao", _h_op(ctx, acao=None), 403),
        ("X-Central-Acao=0", _h_op(ctx, acao="0"), 403),
        ("Sec-Fetch-Site cross-site", _h_op(ctx, sfs="cross-site"), 403),
        ("Sec-Fetch-Site same-site", _h_op(ctx, sfs="same-site"), 403),
        ("text/plain", _h_op(ctx, ctype="text/plain"), 415),
        ("form", _h_op(ctx, ctype="application/x-www-form-urlencoded"), 415),
        ("multipart", _h_op(ctx, ctype="multipart/form-data; boundary=x"), 415),
        ("sem Content-Type", _h_op(ctx, ctype=None), 415),
    ]
    for nome, h, esperado in casos:
        igual(chamar(app, "POST", "/api/iald-app/comandos", h, corpo).status, esperado, nome)
    verdade(not (ctx["tmp"] / "iald_app" / "comandos.json").exists(), "nada enfileirado")


@auth
def auth_comando_sem_retrato_409(ctx):
    r = _cmd(ctx, "aprovar", P1)
    igual(r.status, 409, "sem snapshot ainda")


@auth
def auth_sync_negativos(ctx):
    M = ctx["M"]
    r, _ = _sync(ctx)
    igual(r.status, 503, "sem segredo")
    ruins = [
        ("segredo curto (31 bytes)", "a" * 31, "curto"),
        ("segredo = chave da Central", ctx["segredo"], "não pode ser a chave da Central"),
        ("segredo = chave da Central com espaço", "  " + ctx["segredo"] + " ", "não pode ser a chave da Central"),
        ("hex sem acaso", "a" * 64, "não parece aleatório"),
        ("frase digitada", "minha frase secreta de sincronizacao 2026!", "não parece aleatório"),
        ("hex curto decodificado (16 bytes)", secrets.token_hex(16), "não parece aleatório"),
    ]
    for nome, valor, trecho in ruins:
        os.environ["CENTRAL_IALD_SYNC_SEGREDO"] = valor
        r, _ = _sync(ctx, segredo=valor.strip())
        igual(r.status, 503, nome)
        e = _estado(ctx).json()
        verdade(e["sync_configurado"] is False and trecho in e.get("sync_problema", ""),
                f"{nome}: motivo visível ao operador (veio {e.get('sync_problema')!r})")
    for bom in (secrets.token_urlsafe(32), base64.b64encode(secrets.token_bytes(32)).decode()):
        os.environ["CENTRAL_IALD_SYNC_SEGREDO"] = bom
        e = _estado(ctx).json()
        verdade(e["sync_configurado"] is True and "sync_problema" not in e, "base64/base64url aleatório serve")
    os.environ["CENTRAL_IALD_SYNC_SEGREDO"] = ctx["seg_sync"]
    agora = int(ctx["relogio"][0])
    casos = [
        ("assinatura com outro segredo", dict(segredo=secrets.token_hex(32)), 401),
        ("ts velho", dict(ts=str(agora - 61)), 401),
        ("ts futuro", dict(ts=str(agora + 61)), 401),
        ("corpo adulterado", dict(corpo=b'{"ultimo_seq_executado":0}',
                                  corpo_ass=b'{"ultimo_seq_executado":1}'), 401),
        ("caminho errado", dict(caminho_ass="/api/iald-sync/outro"), 401),
        ("método errado", dict(metodo_ass="GET"), 401),
        ("nonce curto", dict(nonce=secrets.token_hex(15)), 401),
        ("nonce maiúsculo", dict(nonce=secrets.token_hex(16).upper()), 401),
        ("assinatura sem v1=", dict(assinatura=secrets.token_hex(32)), 401),
        ("sem ts", dict(sem=("x-iald-sync-ts",)), 401),
        ("sem nonce", dict(sem=("x-iald-sync-nonce",)), 401),
        ("sem assinatura", dict(sem=("x-iald-sync-assinatura",)), 401),
        ("consulta", dict(consulta="x=1"), 400),
        ("text/plain", dict(ctype="text/plain"), 415),
        ("corpo grande", dict(corpo=b"{" + b" " * 1_000_001 + b"}"), 413),
        ("JSON inválido (assinado)", dict(corpo=b"{nao json"), 400),
        ("campo de topo estranho", dict(obj={"ultimo_seq_executado": 0, "admin": True}), 400),
        ("sem ultimo_seq_executado", dict(obj={"resultados": []}), 400),
        ("seq negativo", dict(obj={"ultimo_seq_executado": -1}), 400),
        ("seq booleano", dict(obj={"ultimo_seq_executado": True}), 400),
        ("chave duplicada", dict(corpo=b'{"ultimo_seq_executado":0,"ultimo_seq_executado":1}'), 400),
        ("resultado malformado", dict(obj={"ultimo_seq_executado": 0,
                                          "resultados": [{"id": "x", "ok": True}]}), 400),
    ]
    for nome, kw, esperado in casos:
        r, _ = _sync(ctx, **kw)
        igual(r.status, esperado, nome)
        verdade(r.h("x-central-assinatura") is None, f"{nome}: recusa não vai assinada")
    # replay: o mesmo nonce, assinatura válida, duas vezes
    nonce = secrets.token_hex(16)
    r1, _ = _sync(ctx, nonce=nonce)
    igual(r1.status, 200, "primeira")
    r2, _ = _sync(ctx, nonce=nonce)
    igual(r2.status, 401, "replay do nonce")
    verdade(b"nonce" in r2.body, "motivo do replay")
    # borda da janela: 59 s ainda vale
    r, _ = _sync(ctx, ts=str(agora - 59))
    igual(r.status, 200, "ts a 59 s")
    # nenhuma recusa gravou retrato
    verdade(not (ctx["tmp"] / "iald_app" / "snapshot.json").exists(), "recusas não gravam retrato")
    # o log geral registra as FALHAS da sync, não os sucessos
    linhas = [json.loads(x) for x in (ctx["tmp"] / "audit.log").read_text(encoding="utf-8").splitlines() if x]
    da_sync = [x for x in linhas if x["path"] == CAMINHO_SYNC]
    verdade(any(x["status"] == 401 for x in da_sync), "falha da sync no log geral")
    verdade(not any(x["status"] == 200 for x in da_sync), "sucesso da sync fora do log geral")
    # CORS excluído: preflight de site irmão não recebe nada
    pre = {"origin": "https://iald.ia.br", "access-control-request-method": "POST",
           "access-control-request-headers": "content-type"}
    igual(chamar(M.app, "OPTIONS", CAMINHO_SYNC, pre).h("access-control-allow-origin"), None, "CORS sync")
    igual(chamar(M.app, "OPTIONS", "/api/acom/inspect", pre).h("access-control-allow-origin"),
          "https://iald.ia.br", "CORS do acom segue")


@auth
def auth_sync_retrato_saneado_e_resposta_assinada(ctx):
    r, nonce = _sync(ctx, {"ultimo_seq_executado": 0, "snapshot": _snapshot_rico(), "resultados": []})
    igual(r.status, 200, "sync com retrato")
    verdade(_resposta_assinada_ok(ctx, r, nonce), "assinatura da resposta confere")
    verdade(not _resposta_assinada_ok(ctx, r, secrets.token_hex(16)), "assinatura amarrada ao nonce")
    igual(r.h("cache-control"), "no-store", "no-store")
    corpo = r.json()
    igual(corpo["comandos"], [], "nada pendente")
    igual(corpo["snapshot"]["pedidos"], 3 + len(PEDIDOS_EXTRA), "pedidos aceitos")
    igual(corpo["snapshot"]["usuarios"], 4, "usuários aceitos")
    igual(corpo["snapshot"]["itens_descartados"], 3 + 4, "itens descartados")
    verdade(corpo["snapshot"]["campos_descartados"] >= 12, "campos descartados contados")
    bruto = (ctx["tmp"] / "iald_app" / "snapshot.json").read_bytes()
    for proibido in (b"NAO-PODE", b"tgl_hash", b"identidades", b"ip_chave", b"cota_chave", b"uso_tokens",
                     b"plano", b"acesso_nativa", b"superficie", b"decidido_por", b"maria.silva",
                     b"\\u202e", b"\xe2\x80\xae", b"\\u0007", b"\\u200b", b"extra_topo"):
        verdade(proibido not in bruto, f"retrato não pode conter {proibido!r}")
    snap = json.loads(bruto)
    permitidas_p = {"id", "nome", "email", "provedor", "status", "criado", "ultima_tentativa",
                    "tentativas", "decidido_em", "usuario", "sugestao"}
    permitidas_u = {"username", "nome", "email", "provedor", "status", "criado", "bloqueado_em"}
    verdade(set(snap) <= {"versao", "gerado_em", "seq", "pedidos", "usuarios", "recebido_em"}, "topo")
    verdade(all(set(p) <= permitidas_p for p in snap["pedidos"]), "chaves de pedido")
    verdade(all(set(u) <= permitidas_u for u in snap["usuarios"]), "chaves de usuário")
    p1 = next(p for p in snap["pedidos"] if p["id"] == P1)
    igual(p1["email"], "ma***@gmail.com", "e-mail remascarado")
    igual(p1["nome"], "Maria evil da Silva", "nome sem controle/bidi")
    igual(p1["tentativas"], 2, "tentativas")
    p2 = next(p for p in snap["pedidos"] if p["id"] == P2)
    igual(p2["email"], "z***@icloud.com", "e-mail curto (2 letras → 1 visível)")
    joao = next(u for u in snap["usuarios"] if u["username"] == "joao")
    igual(joao["email"], "jo***@icloud.com", "máscara idempotente")
    carla = next(u for u in snap["usuarios"] if u["username"] == "carla-2")
    igual(carla["email"], "c***@d.co", "e-mail de 1 letra")
    # o operador vê o mesmo retrato
    e = _estado(ctx)
    igual(e.status, 200, "estado")
    igual(e.h("cache-control"), "no-store", "estado no-store")
    est = e.json()
    igual(est["snapshot"]["pedidos"], snap["pedidos"], "estado = retrato gravado")
    verdade(est["sync_configurado"] is True and est["ultima_sincronizacao"], "sincronização registrada")


@auth
def auth_validacao_do_alvo_e_do_corpo(ctx):
    M = ctx["M"]
    ruins = [
        ("aprovar", "../etc/passwd"), ("aprovar", "ped_../../x"), ("aprovar", "ped_20260921100000_abcdeg"),
        ("aprovar", P1 + "\n"), ("aprovar", "joao"), ("recusar", P1.upper()),
        ("bloquear", "‮joao"), ("bloquear", "joao‮"), ("bloquear", "a" * 33),
        ("bloquear", "Joao"), ("bloquear", ""), ("bloquear", "jo"), ("bloquear", "joão"),
        ("bloquear", "joao/../x"), ("bloquear", "..joao"), ("desbloquear", "joao "),
        ("bloquear", 123), ("bloquear", None), ("bloquear", ["joao"]),
    ]
    for acao, alvo in ruins:
        r = _cmd(ctx, acao, alvo)
        igual(r.status, 400, f"alvo {alvo!r} ({acao})")
    for acao in ("excluir", "admin", "senha", "APROVAR", "", "reabrir", "plano", None):
        igual(_cmd(ctx, acao, "joao").status, 400, f"ação {acao!r}")
    igual(_cmd(ctx, "bloquear", "joao", nota="x" * 201).status, 400, "nota longa")
    igual(_cmd(ctx, "bloquear", "joao", nota=5).status, 400, "nota não-texto")
    h = _h_op(ctx)
    corpos = [
        json.dumps({"acao": "bloquear", "alvo": "joao", "chave": ctx["segredo"], "admin": True}).encode(),
        json.dumps({"acao": "bloquear", "alvo": "joao"}).encode(),
        json.dumps({"acao": "bloquear", "alvo": "joao", "chave": ""}).encode(),
        json.dumps([{"acao": "bloquear"}]).encode(),
        b"{nao json",
        b'{"acao":"bloquear","acao":"desbloquear","alvo":"joao","chave":"x"}',
        b"",
    ]
    for c in corpos:
        igual(chamar(M.app, "POST", "/api/iald-app/comandos", h, c).status, 400, f"corpo {c[:40]!r}")
    igual(chamar(M.app, "POST", "/api/iald-app/comandos", h, b"{" + b" " * 9000 + b"}").status,
          413, "corpo grande")
    est = json.loads((ctx["tmp"] / "iald_app" / "comandos.json").read_bytes())
    igual(est["comandos"], [], "nada enfileirado")


@auth
def auth_comando_valido_seq_e_auditoria(ctx):
    r1 = _cmd(ctx, "aprovar", P1, nota="bem-vinda‮\x00 ok")
    igual(r1.status, 200, "aprovar")
    c1 = r1.json()["comando"]
    igual((c1["seq"], c1["status"], c1["acao"], c1["alvo"], c1["por"]), (1, "pendente", "aprovar", P1, "operador"),
          "comando 1")
    igual(c1["nota"], "bem-vinda ok", "nota limpa")
    r2 = _cmd(ctx, "bloquear", "joao", origem=ORIGEM_RENDER)
    igual(r2.status, 200, "bloquear (origem onrender)")
    r3 = _cmd(ctx, "desbloquear", "bia.b")
    igual(r3.status, 200, "desbloquear")
    seqs = [r.json()["comando"]["seq"] for r in (r1, r2, r3)]
    igual(seqs, [1, 2, 3], "seq estritamente crescente")
    ctx["cmds"] = {"aprovar": c1["id"], "bloquear": r2.json()["comando"]["id"],
                   "desbloquear": r3.json()["comando"]["id"]}
    # recusas de negócio (409)
    igual(_cmd(ctx, "recusar", P1).status, 409, "mesmo alvo em curso")
    igual(_cmd(ctx, "aprovar", P3).status, 409, "pedido não pendente")
    igual(_cmd(ctx, "aprovar", PX).status, 409, "pedido fora do retrato")
    igual(_cmd(ctx, "bloquear", "operador_iald").status, 409, "conta protegida")
    igual(_cmd(ctx, "desbloquear", "carla-2").status, 409, "desbloquear quem está ativo")
    igual(_cmd(ctx, "bloquear", "fantasma").status, 409, "usuário fora do retrato")
    igual(_cmd(ctx, "bloquear", PX).status, 409, "id de pedido como username: fora do retrato")
    # GET do comando
    g = chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/" + c1["id"], _h_op(ctx, origem=None, ctype=None))
    igual(g.status, 200, "get comando")
    igual(g.json()["comando"]["seq"], 1, "get comando seq")
    igual(chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/../../snapshot.json",
                 _h_op(ctx, origem=None, ctype=None)).status, 404, "id com traversal")
    # auditoria própria: só acrescenta; a chave NUNCA aparece em disco nem em resposta
    aud = [json.loads(x) for x in (ctx["tmp"] / "iald_app" / "auditoria.jsonl").read_text(encoding="utf-8").splitlines()]
    enf = [a for a in aud if a["resultado"] == "enfileirado"]
    igual(len(enf), 3, "3 enfileirados auditados")
    verdade(all(set(("ts", "uid", "acao", "alvo", "ip", "resultado")) <= set(a) for a in aud), "campos da auditoria")
    igual({a["uid"] for a in enf}, {"operador"}, "uid do token")
    igual(enf[0]["ip"], "203.0.113.9", "ip")
    verdade(any(a["resultado"].startswith("recusado:") for a in aud), "recusas auditadas")
    tudo = _todos_os_bytes(ctx["tmp"])
    verdade(ctx["segredo"].encode() not in tudo, "a chave da Central não está em disco")
    for r in (r1, r2, r3):
        verdade(ctx["segredo"].encode() not in r.body, "a chave não volta na resposta")


@auth
def auth_step_up_e_trava(ctx):
    s1 = _token(ctx["AUTH"], "operador", "admin", "operador")
    alvo = PEDIDOS_EXTRA[0]
    # a chave de um EDITOR ou VIEWER válido também é "errada": o step-up só aceita a do operador
    erradas = ["chave-errada-1", "chave-errada-2", "x" * 50, ctx["chave_editor"], ctx["chave_viewer"]]
    for i, ch in enumerate(erradas, 1):
        r = _cmd(ctx, "recusar", alvo, chave=ch, token=s1)
        igual(r.status, 403, f"chave errada #{i}")
    r = _cmd(ctx, "recusar", alvo, token=s1)                 # chave CERTA, sessão travada
    igual(r.status, 429, "sessão travada após 5 falhas")
    s2 = _token(ctx["AUTH"], "operador", "admin", "operador")  # outra sessão não herda a trava
    r = _cmd(ctx, "recusar", alvo, token=s2)
    igual(r.status, 200, "outra sessão com a chave certa")
    ctx["relogio"][0] += 901                                  # 15 min depois, destrava
    r = _cmd(ctx, "recusar", PEDIDOS_EXTRA[1], token=s1)
    igual(r.status, 200, "destrava após 15 min")
    aud = (ctx["tmp"] / "iald_app" / "auditoria.jsonl").read_text(encoding="utf-8")
    verdade(aud.count("recusado: chave incorreta") == 5, "5 falhas auditadas")
    verdade("sessão travada" in aud, "trava auditada")
    for ch in erradas:
        verdade(ch not in aud, "chave tentada não vai para a auditoria")


@auth
def auth_limite_por_hora(ctx):
    s = _token(ctx["AUTH"], "operador", "admin", "operador")
    IAU = ctx["IAU"]
    ok = 0
    for p in PEDIDOS_EXTRA[2:]:
        r = _cmd(ctx, "recusar", p, token=s)
        if r.status == 200:
            ok += 1
            continue
        igual(r.status, 429, "a partir do limite")
        break
    igual(ok, IAU.LIMITE_CMD_SESSAO_HORA, "30 por hora por sessão")
    ctx["relogio"][0] += 3601
    igual(_cmd(ctx, "recusar", PEDIDOS_EXTRA[-1], token=s).status, 200, "nova hora")


@auth
def auth_sync_entrega_resultados_e_seq(ctx):
    # adianta 10 min + 1 s: todos os comandos anteriores expiram; recomeça com retrato novo
    ctx["relogio"][0] += 601
    r, _ = _sync(ctx, {"ultimo_seq_executado": 0, "snapshot": _snapshot_rico()})
    igual(r.status, 200, "retrato novo")
    igual(r.json()["comandos"], [], "expirados não são entregues")
    est = json.loads((ctx["tmp"] / "iald_app" / "comandos.json").read_bytes())
    verdade(all(c["status"] == "expirado" for c in est["comandos"]), "todos os antigos expiraram")
    base = est["ultimo_seq"]
    a = _cmd(ctx, "aprovar", P2)
    b = _cmd(ctx, "bloquear", "carla-2")
    c = _cmd(ctx, "desbloquear", "bia.b")
    igual([x.status for x in (a, b, c)], [200, 200, 200], "três novos")
    ids = [x.json()["comando"]["id"] for x in (a, b, c)]
    igual([x.json()["comando"]["seq"] for x in (a, b, c)], [base + 1, base + 2, base + 3], "seq segue crescente")
    r, nonce = _sync(ctx, {"ultimo_seq_executado": base})
    igual(r.status, 200, "puxar")
    verdade(_resposta_assinada_ok(ctx, r, nonce), "resposta assinada")
    cmds = r.json()["comandos"]
    igual([x["seq"] for x in cmds], [base + 1, base + 2, base + 3], "só > ultimo_seq, em ordem")
    igual(set(cmds[0]), {"id", "seq", "acao", "alvo", "nota", "criado_ts", "expira_ts"}, "campos entregues")
    igual(cmds[0]["expira_ts"] - cmds[0]["criado_ts"], 600, "validade de 10 min")
    # a IALD executou o 1º (ok) e o 2º (falhou); relata ultimo_seq_executado = base+2
    r, nonce = _sync(ctx, {"ultimo_seq_executado": base + 2, "resultados": [
        {"id": ids[0], "ok": True, "mensagem": "liberado‮"},
        {"id": ids[1], "ok": False, "mensagem": "usuário não existe mais"},
        {"id": str(uuid.uuid4()), "ok": True}]})
    igual(r.status, 200, "puxar com resultados")
    corpo = r.json()
    igual([x["seq"] for x in corpo["comandos"]], [base + 3], "só o 3º é reentregue")
    igual(corpo["resultados"], {"aplicados": 2, "ignorados": 1}, "contagem de resultados")
    g = lambda i: chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/" + i,  # noqa: E731
                         _h_op(ctx, origem=None, ctype=None)).json()["comando"]
    igual((g(ids[0])["status"], g(ids[0])["resultado"]), ("executado", "liberado"), "executado")
    igual(g(ids[1])["status"], "falhou", "falhou")
    igual(g(ids[2])["status"], "entregue", "entregue")
    aud = (ctx["tmp"] / "iald_app" / "auditoria.jsonl").read_text(encoding="utf-8")
    verdade('"uid":"iald-sync"' in aud and "executado: liberado" in aud, "resultado auditado")
    # a IALD relata um seq ACIMA do que a Central lembra → a sequência sobe
    r, _ = _sync(ctx, {"ultimo_seq_executado": base + 1000})
    igual(r.json()["comandos"], [], "nada acima de base+1000")
    d = _cmd(ctx, "recusar", PEDIDOS_EXTRA[5])
    igual(d.json()["comando"]["seq"], base + 1001, "seq continua acima do relatado")
    r, _ = _sync(ctx, {"ultimo_seq_executado": base + 1001 + 1_000_001})
    igual(r.status, 409, "salto implausível de sequência é recusado, não absorvido")
    est = json.loads((ctx["tmp"] / "iald_app" / "comandos.json").read_bytes())
    igual(est["ultimo_seq"], base + 1001, "a sequência não inflou")


@auth
def auth_expiracao_10_min(ctx):
    est = json.loads((ctx["tmp"] / "iald_app" / "comandos.json").read_bytes())
    exec_iald = est["ultimo_seq_executado_iald"]
    r = _cmd(ctx, "recusar", PEDIDOS_EXTRA[6])
    igual(r.status, 200, "novo comando")
    cid, seq = r.json()["comando"]["id"], r.json()["comando"]["seq"]
    ctx["relogio"][0] += 599
    r, _ = _sync(ctx, {"ultimo_seq_executado": exec_iald})
    verdade(seq in [x["seq"] for x in r.json()["comandos"]], "ainda entregue aos 599 s")
    ctx["relogio"][0] += 2
    r, _ = _sync(ctx, {"ultimo_seq_executado": exec_iald})
    verdade(seq not in [x["seq"] for x in r.json()["comandos"]], "não entregue após 10 min")
    g = chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/" + cid, _h_op(ctx, origem=None, ctype=None))
    igual(g.json()["comando"]["status"], "expirado", "expirado")
    # resultado que chega DEPOIS da expiração de um comando entregue: a verdade vence
    r, _ = _sync(ctx, {"ultimo_seq_executado": seq, "resultados": [{"id": cid, "ok": True, "mensagem": "feito"}]})
    igual(r.json()["resultados"]["aplicados"], 1, "resultado tardio aplicado")
    g = chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/" + cid, _h_op(ctx, origem=None, ctype=None))
    igual(g.json()["comando"]["status"], "executado", "executado (tardio)")
    # comando nunca entregue não aceita resultado
    r = _cmd(ctx, "recusar", PEDIDOS_EXTRA[7])
    nunca = r.json()["comando"]["id"]
    r, _ = _sync(ctx, {"ultimo_seq_executado": seq + 1, "resultados": [{"id": nunca, "ok": True}]})
    igual(r.json()["resultados"], {"aplicados": 0, "ignorados": 1}, "resultado de comando não entregue")


@auth
def auth_cabecalhos_de_endurecimento(ctx):
    M = ctx["M"]
    r = chamar(M.app, "GET", "/")
    status_em(r, 200, "raiz")
    igual(r.h("strict-transport-security"), "max-age=31536000; includeSubDomains", "HSTS")
    csp = r.h("content-security-policy") or ""
    for diretiva in ("default-src 'self'", "script-src 'self'", "object-src 'none'", "base-uri 'none'",
                     "frame-ancestors 'none'", "form-action 'self'", "img-src 'self' data:"):
        verdade(diretiva in csp, f"CSP tem {diretiva}")
    verdade("unsafe-inline" not in csp and "unsafe-eval" not in csp, "CSP sem unsafe-*")
    igual(r.h("x-frame-options"), "DENY", "XFO")
    for caminho in ("/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect"):
        igual(chamar(M.app, "GET", caminho).status, 404, caminho)
    a = chamar(M.app, "GET", "/api/auth/status")
    igual(a.status, 200, "status do login")
    igual(a.h("strict-transport-security"), "max-age=31536000; includeSubDomains", "HSTS na API")


@auth
def auth_documento_html_sai_em_sandbox(ctx):
    _documento_sandbox(ctx, esperar_ancestors="frame-ancestors 'none'",
                       cookie=_cookie(ctx["AUTH"], ctx["tok_viewer"]))


@auth
def auth_cookie_host_strict(ctx):
    M, AUTH = ctx["M"], ctx["AUTH"]
    AUTH._ATTEMPTS.clear()
    r = chamar(M.app, "POST", "/api/auth/login", {"content-type": "application/json"},
               json.dumps({"secret": ctx["segredo"]}).encode())
    igual(r.status, 200, "login")
    verdade(ctx["segredo"].encode() not in r.body, "segredo não volta")
    sc = [c for c in r.todos("set-cookie") if c.startswith("__Host-central_session=")]
    igual(len(sc), 1, "cookie __Host-")
    c = sc[0].lower()
    for attr in ("httponly", "secure", "path=/", "samesite=strict"):
        verdade(attr in c, f"cookie com {attr}")
    verdade("domain=" not in c, "cookie sem Domain")
    verdade(any(x.startswith("central_session=") for x in r.todos("set-cookie")), "apaga o nome antigo")
    tok = sc[0].split(";", 1)[0].split("=", 1)[1].strip('"')
    igual(chamar(M.app, "GET", "/api/auth/me", {"cookie": f"__Host-central_session={tok}"}).status, 200, "novo nome")
    igual(chamar(M.app, "GET", "/api/auth/me", {"cookie": f"central_session={tok}"}).status, 401,
          "nome antigo não é mais lido")
    lo = chamar(M.app, "POST", "/api/auth/logout", {"content-type": "application/json"}, b"{}")
    sc = [c.lower() for c in lo.todos("set-cookie") if c.startswith("__Host-central_session=")]
    verdade(sc and "secure" in sc[0] and "max-age=0" in sc[0], "logout apaga com Secure")


# ──────────────── revisão adversarial de 21/09/2026: um teste por achado corrigido ────────────────
def _sessao(tok: str) -> str:
    return hashlib.sha256(tok.encode("utf-8")).hexdigest()


def _exec_iald(ctx) -> int:
    est = json.loads((ctx["tmp"] / "iald_app" / "comandos.json").read_bytes())
    return est.get("ultimo_seq_executado_iald") or 0


def _linhas_audit(ctx) -> list:
    p = ctx["tmp"] / "audit.log"
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []


def _linhas_aba(ctx) -> list:
    p = ctx["tmp"] / "iald_app" / "auditoria.jsonl"
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def _get_cmd(ctx, cid: str) -> dict:
    return chamar(ctx["M"].app, "GET", "/api/iald-app/comandos/" + cid,
                  _h_op(ctx, origem=None, ctype=None)).json()["comando"]


@auth
def auth_trava_step_up_sob_rajada_concorrente(ctx):
    """Achado: 30 chaves erradas disparadas JUNTAS eram todas conferidas (a trava era checada
    antes do await e a falha só contada depois). Agora a reserva é atômica: ≤ 5 conferidas."""
    AUTH, M, IAU = ctx["AUTH"], ctx["M"], ctx["IAU"]
    ctx["relogio"][0] += 3601                                 # hora nova: nenhum limite herdado
    s = _token(AUTH, "operador", "admin", "operador")
    original = AUTH.verify_secret
    chamadas = []

    def contando(chave):
        chamadas.append(1)
        time.sleep(0.05)          # conferência lenta: as 30 ficam de fato em voo ao mesmo tempo
        return original(chave)

    AUTH.verify_secret = contando
    try:
        corpo = json.dumps({"acao": "recusar", "alvo": PEDIDOS_EXTRA[8], "chave": "errada-concorrente"}).encode()
        rs = chamar_juntos(M.app, [("POST", "/api/iald-app/comandos", _h_op(ctx, token=s), corpo)] * 30)
    finally:
        AUTH.verify_secret = original
    sts = Counter(r.status for r in rs)
    verdade(1 <= len(chamadas) <= IAU.LIMITE_FALHAS_STEPUP,
            f"no máximo {IAU.LIMITE_FALHAS_STEPUP} chaves conferidas (foram {len(chamadas)})")
    igual(sts[403], len(chamadas), "cada chave conferida = um 403")
    igual(sts[429], 30 - len(chamadas), "as demais voltam 429 sem a chave ser conferida")
    igual(_cmd(ctx, "recusar", PEDIDOS_EXTRA[8], token=s).status, 429, "a sessão travou depois da rajada")
    igual(IAU._RL[_sessao(s)]["em_voo"], 0, "nenhuma reserva vazou")


@auth
def auth_entregue_sem_resultado_nao_prende_o_alvo(ctx):
    """Achado: 'entregue' com seq declarado processado e sem resultado ficava assim PARA SEMPRE
    e o alvo dava 409 eternamente. Agora, +30 min após a validade, vira 'sem_resultado'."""
    IAU = ctx["IAU"]
    base = _exec_iald(ctx)
    snap = {"gerado_em": "2026-09-21T18:00:00Z", "seq": 2, "pedidos": [],
            "usuarios": [{"username": "dora.d", "status": "ativo", "nome": "Dora"}]}
    r, _ = _sync(ctx, {"ultimo_seq_executado": base, "snapshot": snap})
    igual(r.status, 200, "retrato com dora.d")
    s = _token(ctx["AUTH"], "operador", "admin", "operador")
    c = _cmd(ctx, "bloquear", "dora.d", token=s)
    igual(c.status, 200, "bloquear dora.d")
    cid, seq = c.json()["comando"]["id"], c.json()["comando"]["seq"]
    r, _ = _sync(ctx, {"ultimo_seq_executado": base})
    verdade(seq in [x["seq"] for x in r.json()["comandos"]], "entregue")
    r, _ = _sync(ctx, {"ultimo_seq_executado": seq})          # executou e caiu antes de relatar
    igual(r.status, 200, "seq declarado sem resultado")
    ctx["relogio"][0] += IAU.TTL_COMANDO + 1
    igual(_get_cmd(ctx, cid)["status"], "entregue", "ainda esperando o resultado")
    cmds_antes = len(IAU._RL[_sessao(s)]["cmds"])
    r = _cmd(ctx, "bloquear", "dora.d", token=s)
    igual(r.status, 409, "alvo ocupado enquanto espera")
    verdade(f"seq {seq}".encode() in r.body and b"entregue" in r.body, "o 409 diz QUAL comando prende o alvo")
    igual(len(IAU._RL[_sessao(s)]["cmds"]), cmds_antes, "ordem recusada devolve a vaga da hora")
    ctx["relogio"][0] += IAU.PRAZO_RESULTADO
    g = _get_cmd(ctx, cid)
    igual(g["status"], "sem_resultado", "estado final depois do prazo")
    verdade("não chegou" in g["resultado"], "motivo dito")
    r = _cmd(ctx, "bloquear", "dora.d", token=s)
    igual(r.status, 200, "o alvo está livre de novo")
    r, _ = _sync(ctx, {"ultimo_seq_executado": seq, "resultados": [{"id": cid, "ok": True, "mensagem": "bloqueado"}]})
    igual(r.json()["resultados"]["aplicados"], 1, "resultado tardio ainda é aplicado")
    igual(_get_cmd(ctx, cid)["status"], "executado", "a verdade vence")


@auth
def auth_retrato_grande_ou_malformado_nao_prende_resultados(ctx):
    """Achado: retrato acima do teto (ou malformado) derrubava a busca inteira (400) e levava
    junto resultados e seq. Agora é aparado (pendentes primeiro) ou vira aceito:false."""
    IAU = ctx["IAU"]
    ctx["relogio"][0] += 601
    base = _exec_iald(ctx)
    pz, pnovo = "ped_20260921170000_00aa11", "ped_20260921170500_00bb22"
    r, _ = _sync(ctx, {"ultimo_seq_executado": base,
                       "snapshot": {"pedidos": [{"id": pz, "status": "pendente", "nome": "Zeca"}], "usuarios": []}})
    igual(r.status, 200, "retrato pequeno")
    c = _cmd(ctx, "aprovar", pz)
    igual(c.status, 200, "aprovar zeca")
    cid, seq = c.json()["comando"]["id"], c.json()["comando"]["seq"]
    r, _ = _sync(ctx, {"ultimo_seq_executado": base})
    verdade(seq in [x["seq"] for x in r.json()["comandos"]], "entregue")
    grandes = [{"id": f"ped_20260901{i:06d}_{i:06x}", "status": "recusado"} for i in range(1200)]
    grandes.append({"id": pnovo, "status": "pendente", "nome": "Nova"})
    r, nonce = _sync(ctx, {"ultimo_seq_executado": seq, "resultados": [{"id": cid, "ok": True, "mensagem": "ok"}],
                           "snapshot": {"pedidos": grandes, "usuarios": []}})
    igual(r.status, 200, "retrato acima do teto NÃO derruba a busca")
    verdade(_resposta_assinada_ok(ctx, r, nonce), "resposta assinada")
    corpo = r.json()
    igual(corpo["resultados"]["aplicados"], 1, "resultado aplicado junto")
    igual(set(corpo["snapshot"]), {"aceito", "pedidos", "usuarios", "itens_descartados", "campos_descartados"},
          "a forma da resposta não mudou")
    igual((corpo["snapshot"]["aceito"], corpo["snapshot"]["pedidos"]), (True, IAU.MAX_PEDIDOS), "aparado no teto")
    igual(corpo["snapshot"]["itens_descartados"], 1201 - IAU.MAX_PEDIDOS, "os aparados contam como descartados")
    snap = json.loads((ctx["tmp"] / "iald_app" / "snapshot.json").read_bytes())
    verdade(any(p["id"] == pnovo for p in snap["pedidos"]), "o pedido PENDENTE ficou (pendentes primeiro)")
    igual(snap.get("omitidos"), {"pedidos": 1201 - IAU.MAX_PEDIDOS, "usuarios": 0}, "a tela sabe que é parcial")
    igual(_get_cmd(ctx, cid)["status"], "executado", "executado")
    # retrato malformado: aceito:false, mas resultado, seq e entrega seguem
    c = _cmd(ctx, "aprovar", pnovo)
    igual(c.status, 200, "aprovar nova")
    cid2, seq2 = c.json()["comando"]["id"], c.json()["comando"]["seq"]
    r, _ = _sync(ctx, {"ultimo_seq_executado": seq})
    verdade(seq2 in [x["seq"] for x in r.json()["comandos"]], "entregue")
    for ruim in ([], {"pedidos": "x"}):
        r, _ = _sync(ctx, {"ultimo_seq_executado": seq2, "snapshot": ruim,
                           "resultados": [{"id": cid2, "ok": False, "mensagem": "recusado pela IALD"}]})
        igual(r.status, 200, f"retrato {ruim!r} não derruba a busca")
        igual(r.json()["snapshot"], {"aceito": False}, "retrato recusado, com a forma de sempre")
    igual(_get_cmd(ctx, cid2)["status"], "falhou", "resultado do 2º aplicado mesmo com retrato ruim")
    snap2 = json.loads((ctx["tmp"] / "iald_app" / "snapshot.json").read_bytes())
    igual(snap2["pedidos"], snap["pedidos"], "o último retrato bom continua")
    falhas = _estado(ctx).json()["falhas_sync_recentes"]
    verdade(any("retrato recusado" in f["motivo"] for f in falhas), "o operador vê o retrato recusado")


@auth
def auth_recusas_sem_assinatura_nao_poluem_o_painel(ctx):
    """Achado: qualquer um enchia 'falhas_sync_recentes' (e o log geral) de 'assinatura
    inválida'. Agora só falhas com HMAC válido entram na lista; as outras viram contagem."""
    IAU, SEC = ctx["IAU"], ctx["SEC"]
    IAU._FALHAS_SYNC.clear()
    IAU._RECUSAS_ANON.clear()
    SEC._ESTRANGULA.mapa.clear()
    antes = len([x for x in _linhas_audit(ctx) if x["path"] == CAMINHO_SYNC])
    for _ in range(25):
        r, _ = _sync(ctx, assinatura="v1=" + "0" * 64)
        igual(r.status, 401, "sem assinatura válida")
    e = _estado(ctx).json()
    igual(e["falhas_sync_recentes"], [], "nada na lista do operador")
    igual((e["recusas_sem_assinatura"]["total"], e["recusas_sem_assinatura"]["por_motivo"]),
          (25, {"assinatura inválida": 25}), "só a contagem")
    # a IALD de verdade com o relógio fora: aparece na lista, e repetições somam numa linha
    agora = int(ctx["relogio"][0])
    for _ in range(3):
        r, _ = _sync(ctx, ts=str(agora - 120))
        igual(r.status, 401, "carimbo velho (assinado)")
    f = [x for x in _estado(ctx).json()["falhas_sync_recentes"] if "carimbo" in x["motivo"]]
    igual(len(f), 1, "uma linha só")
    igual(f[0]["vezes"], 3, "com a contagem")
    novas = [x for x in _linhas_audit(ctx) if x["path"] == CAMINHO_SYNC][antes:]
    igual(len(novas), 1, "log geral: 1 linha por minuto por status (as outras 27 suprimidas)")
    ctx["relogio"][0] += IAU.JANELA_RECUSAS_ANON + 1
    igual(_estado(ctx).json()["recusas_sem_assinatura"]["total"], 0, "a contagem anônima vence em 10 min")
    E = SEC._Estrangulador(janela=60)
    igual([E.passa("k", 0), E.passa("k", 10), E.passa("k", 20), E.passa("k", 61)],
          [(True, 0), (False, 0), (False, 0), (True, 2)], "estrangulador informa as suprimidas")


@auth
def auth_portao_registra_negacoes_e_o_ator(ctx):
    """Achado: recusas do portão (viewer/editor/anônimo nas rotas de admin) não deixavam linha,
    e a leitura do operador saía como 'local'. Agora: linha com o ator do token."""
    M, AUTH, SEC = ctx["M"], ctx["AUTH"], ctx["SEC"]
    SEC._ESTRANGULA.mapa.clear()
    antes = len(_linhas_audit(ctx))
    igual(_estado(ctx, token=ctx["tok_viewer"]).status, 403, "viewer")
    igual(chamar(M.app, "GET", "/api/users", {"cookie": _cookie(AUTH, ctx["tok_editor"])}).status, 403, "editor")
    for _ in range(4):
        igual(chamar(M.app, "GET", "/api/iald-app/estado", {"x-central-acao": "1"}).status, 401, "anônimo")
    igual(_estado(ctx).status, 200, "operador")
    novas = _linhas_audit(ctx)[antes:]
    v = [x for x in novas if x.get("uid") == ctx["uid_viewer"]]
    verdade(v and v[0]["status"] == 403 and v[0]["papel"] == "viewer" and v[0]["origem"] == "portao"
            and v[0]["path"] == "/api/iald-app/estado", f"negação do viewer com o ator ({v})")
    verdade(any(x.get("uid") == ctx["uid_editor"] and x["path"] == "/api/users" for x in novas), "editor")
    anon = [x for x in novas if x["status"] == 401 and x["path"] == "/api/iald-app/estado"]
    igual(len(anon), 1, "anônimo: 1 linha (repetições estranguladas)")
    igual(anon[0]["email"], "(sem sessão)", "anônimo dito")
    op = [x for x in novas if x["status"] == 200 and x["path"] == "/api/iald-app/estado"]
    verdade(op and op[-1]["email"] == "operador (admin)", f"a leitura do operador leva o ator ({op})")
    # trilha da aba: 1 linha de leitura por sessão a cada 10 min
    s = _token(AUTH, "operador", "admin", "operador")
    la = len([x for x in _linhas_aba(ctx) if x["acao"] == "(leitura)"])
    for _ in range(3):
        igual(_estado(ctx, token=s).status, 200, "leitura")
    igual(len([x for x in _linhas_aba(ctx) if x["acao"] == "(leitura)"]), la + 1, "uma linha por sessão/10 min")


@auth
def auth_csrf_de_subdominio_irmao(ctx):
    """Achado (pré-existente): SameSite=Strict não separa demo./iald.ia.br (mesmo site) e os
    POST sem corpo do admin (reindex, backup, sanear, build…) corriam. Agora o portão recusa
    mutação de outra origem; cliente fora de navegador (sem Origin/Sec-Fetch-Site) segue."""
    M, AUTH, SEC = ctx["M"], ctx["AUTH"], ctx["SEC"]
    SEC._ESTRANGULA.mapa.clear()
    op = _cookie(AUTH, ctx["tok_op"])
    for origem in ("https://demo.iald.ia.br", "https://iald.ia.br", "https://www.iald.ia.br", "null",
                   "https://central.iald.ia.br.evil.example", "http://central.iald.ia.br"):
        r = chamar(M.app, "POST", "/api/rota-que-nao-existe", {"cookie": op, "origin": origem})
        igual(r.status, 403, f"POST de {origem}")
        igual(r.h("strict-transport-security"), "max-age=31536000; includeSubDomains", "recusa com HSTS")
    for sfs in ("same-site", "cross-site", "none"):
        igual(chamar(M.app, "POST", "/api/rota-que-nao-existe", {"cookie": op, "sec-fetch-site": sfs}).status,
              403, f"Sec-Fetch-Site {sfs}")
    for origem in (ORIGEM, ORIGEM_RENDER):
        status_em(chamar(M.app, "POST", "/api/rota-que-nao-existe",
                         {"cookie": op, "origin": origem, "sec-fetch-site": "same-origin"}), (404, 405),
                  f"mesma origem {origem} segue")
    status_em(chamar(M.app, "POST", "/api/rota-que-nao-existe", {"cookie": op}), (404, 405),
              "cliente fora de navegador segue (tools/harvest_cloud.py)")
    igual(chamar(M.app, "POST", "/api/auth/logout", {"origin": "https://demo.iald.ia.br"}).status, 403,
          "logout forçado por irmão")
    verdade(chamar(M.app, "POST", "/api/acom/rota-que-nao-existe", {"origin": "https://iald.ia.br"}).status != 403,
            "o descompactador público segue cross-origin")
    igual(chamar(M.app, "GET", "/api/auth/status", {"origin": "https://demo.iald.ia.br"}).status, 200, "GET não é mutação")
    for rota in ("/api/reindex", "/api/backup/run", "/api/iald/sanear", "/api/um/build-oncologia", "/api/compile",
                 "/api/andamentos/run", "/api/notes", "/api/users", "/api/device/x/compress"):
        verdade(AUTH.recusa_csrf("POST", rota, {"origin": "https://demo.iald.ia.br"}), f"{rota}: Origin irmã")
        verdade(AUTH.recusa_csrf("POST", rota, {"sec-fetch-site": "same-site"}), f"{rota}: same-site")
        igual(AUTH.recusa_csrf("POST", rota, {"origin": ORIGEM, "sec-fetch-site": "same-origin"}), None, rota)
    igual(AUTH.recusa_csrf("POST", CAMINHO_SYNC, {"origin": "https://x.example"}), None, "sync isenta (HMAC)")
    verdade(any(x.get("motivo") == "origem não permitida" and x.get("uid") == "operador"
                for x in _linhas_audit(ctx)), "a recusa de CSRF fica no log com o ator")


@auth
def auth_texto_livre_sem_email_nem_cpf(ctx):
    """Achado: nome digitado por quem pede, mensagem da IALD e nota iam para o Render como
    vieram — um e-mail ou CPF ali escapava da máscara escolhida pelo operador (LGPD)."""
    IAU = ctx["IAU"]
    ppii = "ped_20260921171000_00cc33"
    snap = {"pedidos": [{"id": ppii, "status": "pendente", "nome": "[dado pessoal removido] CPF [dado pessoal removido]",
                         "email": "[dado pessoal removido]"}],
            "usuarios": [{"username": "eva.e", "status": "ativo", "nome": "Eva 98765432100 eva​@x.com.br"}]}
    r, _ = _sync(ctx, {"ultimo_seq_executado": _exec_iald(ctx), "snapshot": snap})
    igual(r.status, 200, "retrato")
    bruto = (ctx["tmp"] / "iald_app" / "snapshot.json").read_bytes()
    for proibido in (b"maria.silva@", b"123.456.789", b"98765432100", b"eva@x", b"eva\\u200b"):
        verdade(proibido not in bruto, f"retrato não pode conter {proibido!r}")
    s = json.loads(bruto)
    igual(s["pedidos"][0]["nome"], "ma***@gmail.com CPF ***.***.***-**", "nome do pedido mascarado")
    igual(s["usuarios"][0]["nome"], "Eva ***.***.***-** ev***@x.com.br", "nome da conta mascarado")
    igual(IAU._validar_resultados([{"id": str(uuid.uuid4()), "ok": True,
                                    "mensagem": "conta criada; aviso enviado a [dado pessoal removido]"}])[0]["mensagem"],
          "conta criada; aviso enviado a jo***@hotmail.com", "mensagem da IALD mascarada")
    _, _, nota, _ = IAU._validar_comando({"acao": "bloquear", "alvo": "eva.e", "chave": "x",
                                          "nota": "avisar eva.e@x.com.br (CPF [dado pessoal removido])"})
    igual(nota, "avisar ev***@x.com.br (CPF ***.***.***-**)", "nota mascarada")
    igual(IAU.texto_livre("Ana Souza", 80), "Ana Souza", "nome comum intacto")
    cortado = IAU.texto_livre("x" * 70 + " [dado pessoal removido]", 80)
    verdade(len(cortado) <= 80 and "silva" not in cortado and cortado.startswith("x" * 70 + " ma***@"),
            f"corte só depois da máscara: e-mail no fim não escapa pela metade (veio {cortado!r})")


@auth
def auth_chave_com_surrogate_400_sem_500(ctx):
    """Achado: chave com surrogate solto derrubava o verify_secret (UnicodeEncodeError → 500)."""
    M, AUTH, IAU = ctx["M"], ctx["AUTH"], ctx["IAU"]
    s = _token(AUTH, "operador", "admin", "operador")
    r = chamar(M.app, "POST", "/api/iald-app/comandos", _h_op(ctx, token=s),
               b'{"acao":"bloquear","alvo":"eva.e","chave":"\\ud800abc"}')
    igual(r.status, 400, "400, não 500")
    ent = IAU._RL.get(_sessao(s))
    verdade(ent is None or (not ent["falhas"] and not ent["em_voo"]), "não conta como tentativa de chave")
    igual(AUTH.verify_secret("\ud800abc"), None, "verify_secret recusa em vez de levantar")
    # (fora do escopo, registrado: POST /api/auth/login com surrogate cai no 422 PADRÃO do
    #  FastAPI, que ecoa a entrada e não a consegue codificar → 500 — pré-existente, não é o
    #  step-up; o verify_secret em si já não levanta.)


@auth
def auth_erro_de_disco_fica_visivel(ctx):
    """Achado: OSError ao gravar (disco cheio) virava 500 mudo, fora da lista do operador."""
    IAU = ctx["IAU"]
    IAU._FALHAS_SYNC.clear()
    s = _token(ctx["AUTH"], "operador", "admin", "operador")
    original = IAU._gravar_json

    def disco_cheio(*_a, **_k):
        raise OSError(28, "No space left on device")

    IAU._gravar_json = disco_cheio
    try:
        r, _ = _sync(ctx, {"ultimo_seq_executado": _exec_iald(ctx)})
        igual(r.status, 503, "sync: 503 visível")
        verdade("disco".encode() in r.body, "motivo dito")
        r = _cmd(ctx, "bloquear", "eva.e", token=s)
        igual(r.status, 503, "comando: 503 visível")
        igual(len(IAU._RL[_sessao(s)]["cmds"]), 0, "a vaga da hora volta")
    finally:
        IAU._gravar_json = original
    f = _estado(ctx).json()["falhas_sync_recentes"]
    verdade(any("disco" in x["motivo"] and x["status"] == 503 for x in f), f"o operador vê a falha de disco ({f})")
    igual(_cmd(ctx, "bloquear", "eva.e", token=s).status, 200, "disco de volta, ordem aceita")


@auth
def auth_csp_hash_do_openseadragon(ctx):
    """Achado: a CSP estrita barrava o <style> que o OpenSeadragon injeta. O hash na CSP tem de
    bater com o texto do OSD instalado (e com o do bundle, se construído)."""
    SEC = ctx["SEC"]
    fonte = RAIZ / "frontend" / "node_modules" / "openseadragon" / "build" / "openseadragon" / "openseadragon.js"
    if not fonte.exists():
        print("    (pulado: frontend/node_modules ausente)")
        return
    txt = fonte.read_text(encoding="utf-8")
    ms = re.findall(r"style\.textContent\s*=\s*((?:\s*'[^']*'\s*\+?)+);", txt)
    igual(len(ms), 1, "uma injeção de <style> no OSD")
    css = "".join(re.findall(r"'([^']*)'", ms[0]))
    h = "'sha256-" + base64.b64encode(hashlib.sha256(css.encode("utf-8")).digest()).decode() + "'"
    verdade(h in SEC.STRICT_APP_CSP, f"hash {h} na CSP (recalcule ao atualizar o OpenSeadragon)")
    verdade("unsafe-inline" not in SEC.STRICT_APP_CSP, "sem unsafe-inline")
    for js in (RAIZ / "frontend" / "dist" / "assets").glob("*.js"):
        b = js.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"data-openseadragon-mobile-css`,`true`\),\w+\.textContent=`([^`]*)`", b)
        if m:
            igual(m.group(1), css, f"o bundle {js.name} injeta o mesmo texto")


@auth
def auth_auditoria_da_aba_so_acrescenta(ctx):
    """Achado: cada linha relia e reescrevia o arquivo inteiro (até 4 MB, com fsync) dentro do
    laço de eventos. Agora: append; linha partida fica isolada; rotação arquiva (não apaga)."""
    IAU = ctx["IAU"]
    p = ctx["tmp"] / "iald_app" / "auditoria.jsonl"
    antes = p.read_bytes()
    with open(p, "ab") as f:
        f.write(b'{"linha_partida":')                          # simula uma escrita interrompida
    IAU._auditar({"teste": 1})
    depois = p.read_bytes()
    verdade(depois.startswith(antes + b'{"linha_partida":\n'), "o que existia fica intacto; a partida isolada")
    verdade(depois.endswith(b'{"teste":1}\n'), "a linha nova inteira no fim")
    teto = IAU.MAX_AUDITORIA_BYTES
    IAU.MAX_AUDITORIA_BYTES = len(depois) + 5
    try:
        IAU._auditar({"teste": 2})
    finally:
        IAU.MAX_AUDITORIA_BYTES = teto
    arquivados = list(p.parent.glob("auditoria.*.jsonl"))
    igual(len(arquivados), 1, "rotação arquiva")
    igual(arquivados[0].read_bytes(), depois, "o arquivado é o arquivo inteiro, byte a byte")
    igual(p.read_bytes(), b'{"teste":2}\n', "o novo começa")


def _servir_documento(M, arquivo: Path, cookie: str | None = None) -> Resp:
    """GET /api/documents/1/file com o banco trocado por um que aponta para `arquivo`."""
    class _Conn:
        def execute(self, *_a):
            class _Cur:
                def fetchone(self_inner):
                    return {"rel_path": str(arquivo)}
            return _Cur()

        def close(self):
            pass

    original = M.connect
    try:
        M.connect = lambda: _Conn()
        return chamar(M.app, "GET", "/api/documents/1/file", {"cookie": cookie} if cookie else {})
    finally:
        M.connect = original


def _documento_sandbox(ctx, esperar_ancestors: str, cookie: str | None = None):
    """Na nuvem: o que roda script (HTML, SVG, desconhecido) sai em sandbox; PDF, imagem raster,
    vídeo e áudio ficam fora (o sandbox quebraria o vídeo: origem opaca + CORS)."""
    M, SEC = ctx["M"], ctx["SEC"]
    casos = [
        ("painel.html", b"<html><script>alert(1)</script></html>", True),
        ("desenho.svg", b"<svg xmlns='http://www.w3.org/2000/svg'><script>1</script></svg>", True),
        ("sem_tipo.zzqq", b"?", True),
        ("doc.pdf", b"%PDF-1.4\n%%EOF\n", False),
        ("skygrid_run.mp4", b"\x00\x00\x00\x18ftypmp42", False),
        ("figura.png", b"\x89PNG\r\n\x1a\n", False),
        ("som.mp3", b"ID3", False),
    ]
    for nome, conteudo, deve in casos:
        arq = ctx["tmp"] / nome
        arq.write_bytes(conteudo)
        r = _servir_documento(M, arq, cookie)
        igual(r.status, 200, f"{nome} servido")
        csp = r.h("content-security-policy") or ""
        igual(r.h("x-content-type-options"), "nosniff", f"nosniff em {nome}")
        if deve:
            verdade(csp.startswith("sandbox"), f"{nome} com CSP sandbox (veio {csp!r})")
            verdade("allow-scripts" not in csp and "allow-same-origin" not in csp, "sandbox sem brechas")
            verdade(esperar_ancestors in csp, "frame-ancestors do modo")
        else:
            verdade("sandbox" not in csp, f"{nome} fora do sandbox (veio {csp!r})")
            igual(csp, SEC.STRICT_APP_CSP, f"{nome} com a CSP estrita da casca (media/img 'self')")


if __name__ == "__main__":
    sys.exit(main())

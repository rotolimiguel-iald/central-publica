# -*- coding: utf-8 -*-
"""A TORRE DE COMANDO da Central (24/10/2026) — o que a página «Torre de comando» do cockpit lê e dispara.

Três rotas (montadas em main.py; TODAS só do admin, por `_require_admin`):
  GET  /api/torre                    o quadro único: selo, organismo, missões ACOM, custódia, vigia, o X do dia, o túnel do Codex e os erros.
  POST /api/torre/custodia/planejar  `custodiar.py planejar --versao vNNN --seco` (plano a seco). NUNCA `executar`, NUNCA `--publicar`.
  POST /api/torre/x/ensaio           `pensamento_do_dia.py --seco` (gera e mostra; não grava, não enfileira). Nunca sem --seco.

A régua da casa vale em cada função:
  * SÓ LEITURA de arquivos da casa, mais dois subprocessos a seco (plano e ensaio). Nada é escrito, nada é reiniciado, nenhum processo alheio
    é morto (só o filho próprio, no timeout, como o resto da Central), nenhum provedor é chamado, nenhuma credencial é lida.
  * FALHA DE LEITURA É VISÍVEL: toda leitura que falha entra em `erros` com o nome dela; um bloco quebrado não derruba os outros (nunca «ok» falso).
    O que o contrato chama de opcional e está ausente (`custodias.json`, `VIGIA_ULTIMO.json`, o quadro do organismo) é `[]`/`null`, sem erro.
  * NENHUM CAMINHO ABSOLUTO da máquina na resposta: só nomes de arquivo. Um filtro final (`_sem_caminhos`) troca todo caminho pelo seu nome em
    TODA a resposta, inclusive o texto livre das missões e a saída dos scripts.
  * Nada do browser vai para a linha de comando, exceto `versao`, validada por `v[0-9]{3,4}` (fullmatch; só ASCII; sem `\\n` final).
  * Hash/pino sempre LIDO do arquivo (o selo: sha256 do um.py), jamais digitado. `NOT_FALSIFIED` nunca é `CONFIRMED`: a Torre só mostra o que os
    arquivos dizem, com a data deles.
  * Os filhos recebem o ambiente SEM segredos (nada `CENTRAL_*`, nada com SECRET/TOKEN/PASS/KEY/CRED/AUTH no nome) e sem janela preta
    (`sem_janela`: o backend roda sob pythonw).

Decisões de leitura (ditas, para ninguém adivinhar):
  * MISSÕES VIVAS = referência ACOM de `sessions\\*.json` cuja referência OU cujo diário (`state\\journal\\<context_id>.events.jsonl`, uma linha por
    transição) foi modificado nos últimos 14 dias. A referência é imutável (nasce uma vez): só o diário diz que a missão ainda anda.
  * `atualizado_em` de uma missão = o instante mais novo entre a referência e o diário (a última transição). A projeção em si não traz data.
  * `proxima_acao`/`fase` vêm da projeção (`flow.next_action`/`flow.phase`); `handles` = SÓ os pendentes (`flow.handles`; os encerrados ficam em
    `terminal_handles` e não entram aqui).
  * Missão grande (a coordenadora do Codex precisa de ~112 mil caracteres, o padrão é 24 mil): `ProjectionOverflow` diz o tamanho exato; repete UMA
    vez o mesmo `project` (só leitura) com esse tamanho +1 KiB, até 1 milhão. Recusa do guarda (conteúdo da casa Escritório etc.) NÃO se contorna: vira erro nomeado.
  * Cache de 60 s (um voo só: chamadas concorrentes esperam a primeira) para as projeções e para o `iald.py estado`, que custa ~3 s.
  * `x.livro` = as 7 últimas datas do LIVRO.jsonl, da mais antiga para a mais nova; `x.hoje` = a entrada da data local de hoje ou null. O recibo
    (`ORDEM_021\\<data>.json`) é a autoridade da publicação; sem recibo, `publicado` é null (não false: ninguém disse que não publicou).
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException

from . import config as C
from . import sem_janela as _subprocess  # nunca abre janela preta (o backend roda sob pythonw)

# ───────────────────────────────────────────────────────────── fontes (constantes: os testes as trocam)
PY_CASA = "C:/Python314/python.exe"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
SELO = NOS / "um_absoluto_selo.json"
QUADRO = C.CENTRAL / "organismo" / "ESTADO_DO_ORGANISMO.json"
MEMORIA = Path("C:/IALD/MEMORIA_IALD")
SESSOES = MEMORIA / "sessions"
DIARIO = MEMORIA / "state" / "journal"
SESSION_MEMORY = MEMORIA / "session_memory.py"
CUSTODIAS = Path("C:/IALD/Site/tgl/v3.0_bancada/central_extra/organismo/custodias.json")
VIGIA = C.CENTRAL / "work" / "custodia_G1" / "VIGIA_ULTIMO.json"
TUNEL = C.CENTRAL / "Chatgpt" / "TUNEL"
X_DIARIO = TUNEL / "PARA_CHATGPT" / "X_DIARIO"
LIVRO = X_DIARIO / "LIVRO.jsonl"
DO_CHATGPT = TUNEL / "DO_CHATGPT"
ORDEM_X = DO_CHATGPT / "ORDEM_021"
IALD_PY = Path("C:/IALD/PROGRAMA_IALD/iald.py")
CUSTODIAR = C.CENTRAL / "tools" / "custodiar.py"
PENSAMENTO = C.CENTRAL / "tools" / "pensamento_do_dia.py"

VIVAS_DIAS = 14
LIMITE_REFS = 40
LIMITE_CODEX = 300
MAX_PROJECAO_CHARS = 1_000_000
TTL_CACHE_S = 60.0
TIMEOUT_PROJECAO_S = 45
TIMEOUT_CODEX_S = 60
TIMEOUT_ACAO_S = 600
TEXTO_MAX = 4000

# códigos de saída do custodiar.py (tools/custodia_g1/README.md) — só para a Torre mostrar o que o número quer dizer
_RC_CUSTODIA = {
    0: "completo: nada a fazer e nenhuma decisão do operador aberta",
    1: "pendente: pronto para custodiar ou para publicar",
    5: "G1 terminou o que lhe cabe, mas há decisões do OPERADOR abertas",
    10: "WAIT: o Nós está em obra (versão ainda não selada)",
    20: "STOP: falta insumo, âncora ou gate; passo BLOQUEADO",
    30: "falha de leitura (git, arquivo, recibo): nunca vira ok",
    40: "divergência do ar/GitHub",
}

_UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
_VERSAO = re.compile(r"v[0-9]{3,4}")
_SEGREDO_NO_NOME = re.compile(r"(?i)(secret|token|passw|_pass|pass$|key|cred|auth)")


# ───────────────────────────────────────────────────────────── nenhum caminho absoluto na resposta
def _rx_raiz(raiz: str) -> str:
    """Regex de uma raiz com espaço no nome, aceitando C:\\x, C:/x e o estilo Git Bash /c/x."""
    partes = [p for p in re.split(r"[\\/]+", raiz) if p]
    cabeca = ""
    if partes and re.fullmatch(r"[A-Za-z]:", partes[0]):
        letra = partes.pop(0)[0]
        cabeca = r"(?:%s:|/%s)" % (letra, letra) + r"[\\/]+"
    return cabeca + r"[\\/]+".join(re.escape(p) for p in partes)


def _compilar_rx_caminho() -> "re.Pattern[str]":
    # raízes da casa COM ESPAÇO no nome: o regex genérico pararia no espaço e deixaria o resto do caminho vazar
    raizes = {str(C.CENTRAL), "C:/IALD/Central de Patentes", "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um"}
    alt = "|".join(sorted((_rx_raiz(r) for r in raizes), key=len, reverse=True))
    return re.compile(
        r"(?i)(?:" + alt + r"|"
        r"(?<![A-Za-z0-9])[A-Za-z]:(?:\\+|/(?!/))"          # C:\  C:\\  C:/   (não «https://»)
        r"|\\\\[^\s\\/]+(?=[\\/])"                           # \\servidor\
        r"|(?<![\w./-])/[a-zA-Z](?=/[^\s/])"                 # /c/IALD/... (Git Bash)
        r")(?:[\\/]*[^\s\"'<>|*?]*)?")


_RX_CAMINHO = _compilar_rx_caminho()


def _troca_caminho(m: "re.Match[str]") -> str:
    s = m.group(0)
    cauda = ""
    while s and s[-1] in ".,;:)]}":
        cauda = s[-1] + cauda
        s = s[:-1]
    partes = [p for p in re.split(r"[\\/]+", s) if p]
    nome = partes[-1] if partes else ""
    if not nome or re.fullmatch(r"[A-Za-z]:", nome):
        nome = "<raiz>"
    return nome + cauda


def _sem_caminhos(x):
    """Troca TODO caminho absoluto (C:\\..., C:/..., \\\\srv\\..., /c/...) pelo nome do último componente, em qualquer string da resposta."""
    if isinstance(x, str):
        return _RX_CAMINHO.sub(_troca_caminho, x)
    if isinstance(x, list):
        return [_sem_caminhos(i) for i in x]
    if isinstance(x, dict):
        return {k: _sem_caminhos(v) for k, v in x.items()}
    return x


# ───────────────────────────────────────────────────────────── utilidades
def _agora_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _iso_de(ts: float) -> str:
    return datetime.fromtimestamp(ts).astimezone().isoformat(timespec="seconds")


def _json(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))


def _erro_txt(e: BaseException) -> str:
    return _sem_caminhos("%s: %s" % (type(e).__name__, e)).replace("\r", " ").replace("\n", " ")[:300]


def _corta(s, n: int = TEXTO_MAX):
    if isinstance(s, str) and len(s) > n:
        return s[:n] + "…[truncado]"
    return s


def _cauda(txt: str, n: int) -> str:
    return "\n".join((txt or "").splitlines()[-n:])


def _env_filho() -> dict:
    """Ambiente dos filhos: o do backend SEM segredos (CENTRAL_*, SECRET/TOKEN/PASS/KEY/CRED/AUTH no nome) e em UTF-8."""
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith("CENTRAL_") and not _SEGREDO_NO_NOME.search(k)}
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _rodar(args, entrada: bytes | None = None, timeout: float = 60, cwd: str | None = None):
    """Roda `args` em processo NOVO, sem janela e sem shell. -> (rc, stdout, stderr) em texto UTF-8.
    Levanta TimeoutExpired (o filho próprio é encerrado pelo run) ou OSError: quem chama decide como mostrar. É o único ponto de saída da Torre."""
    kw = {"input": entrada} if entrada is not None else {"stdin": _subprocess.DEVNULL}
    r = _subprocess.run([str(a) for a in args], capture_output=True, timeout=timeout, cwd=cwd, env=_env_filho(), **kw)
    return (r.returncode,
            (r.stdout or b"").decode("utf-8", "replace"),
            (r.stderr or b"").decode("utf-8", "replace"))


class _Cache:
    """Cache de um valor com TTL e UM VOO SÓ: com o cache frio, chamadas concorrentes esperam a primeira em vez de martelar o banco."""

    def __init__(self, ttl: float):
        self.ttl = ttl
        self._lock = threading.Lock()
        self._t: float | None = None
        self._v = None

    def obter(self, fn):
        with self._lock:
            if self._t is not None and (time.monotonic() - self._t) < self.ttl:
                return self._v
            v = fn()
            self._v, self._t = v, time.monotonic()
            return v

    def limpar(self):
        with self._lock:
            self._t, self._v = None, None


_CACHE_MISSOES = _Cache(TTL_CACHE_S)
_CACHE_CODEX = _Cache(TTL_CACHE_S)
_LOCK_CUSTODIA = threading.Lock()
_LOCK_X = threading.Lock()


def _limpar_cache() -> None:
    _CACHE_MISSOES.limpar()
    _CACHE_CODEX.limpar()


# ───────────────────────────────────────────────────────────── os blocos do GET
def _ler_selo(erros: list) -> dict:
    """{versao, pin16, timestamp} do selo do Nós. O pino é o sha256 do um.py LIDO do selo (jamais digitado)."""
    try:
        d = _json(SELO)
        return {"versao": d["um_version"], "pin16": str(d["sha256"]["um.py"])[:16], "timestamp": d.get("timestamp")}
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        erros.append("selo: " + _erro_txt(e))
        return {"versao": None, "pin16": None, "timestamp": None}


def _ler_quadro(erros: list):
    """{medido_em, resumo, idade_min} do ESTADO_DO_ORGANISMO.json; null se ausente (contrato), null + erro se ilegível."""
    if not QUADRO.is_file():
        return None
    try:
        d = _json(QUADRO)
        return {"medido_em": d.get("medido_em"), "resumo": d.get("resumo"),
                "idade_min": round((time.time() - QUADRO.stat().st_mtime) / 60, 1)}
    except (OSError, ValueError, AttributeError) as e:
        erros.append("quadro: " + _erro_txt(e))
        return None


def _ler_custodias(erros: list) -> list:
    """Lista de custódias gerada por outro agente (`custodias.json`); [] se não existir."""
    if not CUSTODIAS.is_file():
        return []
    try:
        d = _json(CUSTODIAS)
    except (OSError, ValueError) as e:
        erros.append("custodias: " + _erro_txt(e))
        return []
    if isinstance(d, dict) and isinstance(d.get("custodias"), list):
        d = d["custodias"]
    if not isinstance(d, list):
        erros.append("custodias: formato inesperado (%s); esperava uma lista" % type(d).__name__)
        return []
    return d


def _ler_vigia(erros: list):
    """O último `custodiar.py vigiar --gravar` (MODO SOMBRA), como está; null se ainda não gravou."""
    if not VIGIA.is_file():
        return None
    try:
        return _json(VIGIA)
    except (OSError, ValueError) as e:
        erros.append("vigia: " + _erro_txt(e))
        return None


def _entrada_x(d: dict, erros: list) -> dict:
    ent = {"data": d["data"], "texto": d.get("texto"), "fonte": d.get("fonte"), "sha256": d.get("sha256"),
           "recibo": False, "publicado": None, "url": None, "hora_local": None, "sha_confere": None}
    rec = ORDEM_X / (d["data"] + ".json")
    if rec.is_file():
        try:
            r = _json(rec)
            ent["recibo"] = True
            ent["publicado"] = r.get("publicado") if isinstance(r.get("publicado"), bool) else None
            ent["url"] = r.get("url")
            ent["hora_local"] = r.get("hora_local")
            if r.get("texto_sha256") and d.get("sha256"):
                ent["sha_confere"] = (r["texto_sha256"] == d["sha256"])
        except (OSError, ValueError, AttributeError) as e:
            erros.append("x: recibo de %s: %s" % (d["data"], _erro_txt(e)))
    return ent


def _ler_x(erros: list) -> dict:
    vazio = {"hoje": None, "livro": []}
    if not LIVRO.is_file():
        erros.append("x: LIVRO.jsonl ausente")
        return vazio
    try:
        linhas = LIVRO.read_text(encoding="utf-8-sig").splitlines()
    except OSError as e:
        erros.append("x: " + _erro_txt(e))
        return vazio
    por_data: dict = {}
    ruins = 0
    for l in linhas:
        l = l.strip()
        if not l:
            continue
        try:
            d = json.loads(l)
        except ValueError:
            ruins += 1
            continue
        if isinstance(d, dict) and isinstance(d.get("data"), str) and _DATA.fullmatch(d["data"]):
            por_data[d["data"]] = d                      # a linha mais nova da mesma data vale
        else:
            ruins += 1
    if ruins:
        erros.append("x: %d linha(s) do LIVRO.jsonl ilegível(is) ou sem data" % ruins)
    entradas = {dt: _entrada_x(por_data[dt], erros) for dt in sorted(por_data)[-7:]}
    return {"hoje": entradas.get(datetime.now().strftime("%Y-%m-%d")), "livro": list(entradas.values())}


def _varrer_ordem(d: Path):
    """-> (ultima_entrega ISO|None, n subpastas com RESULTADO*.json). Sem backups; até dois níveis; só stat."""
    ignorar = (".bak", ".superseded", ".tmp")
    mais_novo, subs, n = 0.0, 0, 0
    with os.scandir(d) as it:
        for e in it:
            n += 1
            if n > 20000 or any(t in e.name for t in ignorar):
                continue
            if e.is_file(follow_symlinks=False):
                mais_novo = max(mais_novo, e.stat().st_mtime)
            elif e.is_dir(follow_symlinks=False):
                tem = False
                with os.scandir(e.path) as it2:
                    for e2 in it2:
                        n += 1
                        if any(t in e2.name for t in ignorar) or not e2.is_file(follow_symlinks=False):
                            continue
                        mais_novo = max(mais_novo, e2.stat().st_mtime)
                        if e2.name.startswith("RESULTADO") and e2.name.endswith(".json"):
                            tem = True
                subs += 1 if tem else 0
    return (_iso_de(mais_novo) if mais_novo else None), subs


def _ordem(d: Path, erros: list) -> dict:
    res = d / "RESULTADO.json"
    pend, detalhe = [], {}
    if res.is_file():
        try:
            doc = _json(res)
            if isinstance(doc, dict):
                for k, v in doc.items():
                    if isinstance(v, dict) and str(v.get("pendente_do_operador") or "").strip():
                        pend.append(str(k))
                        detalhe[str(k)] = _corta(str(v["pendente_do_operador"]), 300)
        except (OSError, ValueError) as e:
            erros.append("tuneis: %s/RESULTADO.json: %s" % (d.name, _erro_txt(e)))
    try:
        ultima, subs = _varrer_ordem(d)
    except OSError as e:
        erros.append("tuneis: %s: %s" % (d.name, _erro_txt(e)))
        ultima, subs = None, 0
    return {"ordem": d.name, "tem_resultado": res.is_file(), "pendentes_do_operador": pend,
            "ultima_entrega": ultima, "pendentes_detalhe": detalhe, "subpastas_com_resultado": subs}


def _ler_ordens(erros: list) -> list:
    if not DO_CHATGPT.is_dir():
        erros.append("tuneis: pasta DO_CHATGPT ausente")
        return []
    try:
        dirs = sorted(p for p in DO_CHATGPT.glob("ORDEM_*") if p.is_dir())
    except OSError as e:
        erros.append("tuneis: " + _erro_txt(e))
        return []
    return [_ordem(d, erros) for d in dirs]


# ───────────────────────────────────────────────────────────── missões ACOM e Codex (com cache de 60 s)
def _context_id(p: Path):
    try:
        cid = _json(p).get("context_id")
    except (OSError, ValueError, AttributeError):
        return None
    return cid if isinstance(cid, str) and _UUID.fullmatch(cid) else None


def _referencias(erros: list) -> list:
    """[(Path, ultimo_ts)] das referências VIVAS (referência ou diário mexidos nos últimos 14 dias), a mais recente primeiro, até 40."""
    if not SESSOES.is_dir():
        erros.append("missoes: pasta de referências ausente")
        return []
    try:
        arquivos = [p for p in SESSOES.glob("*.json") if p.is_file()]
    except OSError as e:
        erros.append("missoes: " + _erro_txt(e))
        return []
    corte = time.time() - VIVAS_DIAS * 86400
    vivas = []
    for p in arquivos:
        try:
            ultimo = p.stat().st_mtime
        except OSError:
            continue
        cid = _context_id(p)
        if cid:
            try:
                ultimo = max(ultimo, (DIARIO / (cid + ".events.jsonl")).stat().st_mtime)
            except OSError:
                pass
        if ultimo >= corte:
            vivas.append((p, ultimo))
    vivas.sort(key=lambda t: (-t[1], t[0].name))
    return vivas[:LIMITE_REFS]


def _corpo_da_projecao(texto: str) -> dict:
    """A projeção é um cabeçalho de texto + UMA linha de JSON (`flow`, `records`, ...). Acha o JSON e o decodifica."""
    i = texto.find("\n{")
    inicio = texto[i + 1:] if i >= 0 else (texto if texto.startswith("{") else None)
    if inicio is None:
        raise ValueError("a projeção não traz o corpo JSON")
    obj, _ = json.JSONDecoder().raw_decode(inicio)
    if not isinstance(obj, dict):
        raise ValueError("o corpo da projeção não é um objeto")
    return obj


def _projetar(ref: Path, ultimo_ts: float) -> dict:
    """UMA missão. Qualquer falha, até a imprevista, vira {referencia, erro}: a missão nunca some da lista."""
    try:
        return _projetar_missao(ref, ultimo_ts)
    except Exception as e:  # noqa: BLE001 — falha visível na própria entrada e em `erros`
        return {"referencia": ref.name, "erro": "erro interno: " + _erro_txt(e)}


def _pedir_projecao(ref: Path, max_chars: int | None = None):
    """Uma chamada `project` (só leitura). -> (rc, d, resto): d = o JSON da resposta (objeto) ou None se a saída não for JSON; resto = a cauda do texto."""
    pedido = {"operation": "project", "reference": str(ref)}
    if max_chars is not None:
        pedido["max_chars"] = max_chars
    rc, out, err = _rodar([PY_CASA, "-X", "utf8", SESSION_MEMORY], entrada=json.dumps(pedido).encode("utf-8"), timeout=TIMEOUT_PROJECAO_S)
    try:
        d = json.loads(out)
    except ValueError:
        d = None
    return rc, (d if isinstance(d, dict) else None), (err or out).strip()[-160:]


def _projetar_missao(ref: Path, ultimo_ts: float) -> dict:
    """`session_memory.py project` em processo novo (só leitura). Falha conhecida vira {referencia, erro}, nunca omissão."""
    nome = ref.name
    try:
        rc, d, resto = _pedir_projecao(ref)
        if d is not None and not d.get("ok") and d.get("error") == "ProjectionOverflow":
            # a missão grande (a coordenadora do Codex tem 112 mil caracteres obrigatórios) estoura o orçamento padrão de 24 mil:
            # a própria recusa diz o tamanho exato; repete UMA vez, só leitura, com esse tamanho (+1 KiB), se couber no teto.
            m = re.search(r"require ([0-9]+) characters", str(d.get("message")))
            if m and int(m.group(1)) + 1024 <= MAX_PROJECAO_CHARS:
                rc, d, resto = _pedir_projecao(ref, int(m.group(1)) + 1024)
    except _subprocess.TimeoutExpired:
        return {"referencia": nome, "erro": "a projeção não respondeu em %d s" % TIMEOUT_PROJECAO_S}
    except OSError as e:
        return {"referencia": nome, "erro": "a projeção não pôde ser iniciada: " + _erro_txt(e)}
    if d is None:
        return {"referencia": nome, "erro": _sem_caminhos("resposta que não é JSON (rc=%d): %s" % (rc, resto))}
    if not d.get("ok"):
        return {"referencia": nome, "erro": _sem_caminhos(("%s: %s" % (d.get("error"), d.get("message")))[:300])}
    try:
        res = d.get("result") or {}
        corpo = _corpo_da_projecao(res["text"])
        flow = corpo.get("flow") if isinstance(corpo.get("flow"), dict) else {}
        handles = [{"id": h.get("id"), "status": h.get("status")} for h in (flow.get("handles") or []) if isinstance(h, dict)]
        rec = res.get("receipt") if isinstance(res.get("receipt"), dict) else {}
        rev = rec.get("revision")
        cid = rec.get("context_id")
        ultimo = ultimo_ts
        if isinstance(cid, str) and _UUID.fullmatch(cid):
            try:
                ultimo = max(ultimo, (DIARIO / (cid + ".events.jsonl")).stat().st_mtime)
            except OSError:
                pass
        return {"referencia": nome, "fase": _corta(flow.get("phase")), "proxima_acao": _corta(flow.get("next_action")),
                "revisao": rev, "atualizado_em": _iso_de(ultimo), "handles": handles}
    except (KeyError, ValueError, TypeError, AttributeError) as e:
        return {"referencia": nome, "erro": "projeção ilegível: " + _erro_txt(e)}


def _missoes_calc():
    """-> (missoes, erros). As projeções rodam em paralelo (4); cada uma custa ~0,2 s."""
    erros: list = []
    refs = _referencias(erros)
    if not refs:
        return [], erros
    with ThreadPoolExecutor(max_workers=min(4, len(refs))) as ex:
        missoes = list(ex.map(lambda t: _projetar(t[0], t[1]), refs))
    for m in missoes:
        if "erro" in m:
            erros.append("missao %s: %s" % (m["referencia"], m["erro"]))
    return missoes, erros


def _codex_calc():
    """-> (codex_threads, erros): a chave `codex` de `iald.py estado` (só leitura, ~3 s); [] + erro se falhar."""
    erros: list = []
    try:
        rc, out, err = _rodar([PY_CASA, "-X", "utf8", IALD_PY, "estado"], timeout=TIMEOUT_CODEX_S, cwd=str(IALD_PY.parent))
        try:
            doc = json.loads(out)
        except ValueError:
            raise ValueError("saída que não é JSON (rc=%d): %s" % (rc, (err or out).strip()[-160:]))
        cod = doc.get("codex") if isinstance(doc, dict) else None
        if isinstance(cod, dict):
            raise ValueError("o estado reportou erro no Codex: %s" % cod.get("erro"))
        if not isinstance(cod, list):
            raise ValueError("a chave codex não veio como lista")
        if len(cod) > LIMITE_CODEX:
            erros.append("tuneis.codex_threads: %d sessões; devolvidas as %d mais recentes" % (len(cod), LIMITE_CODEX))
            cod = cod[:LIMITE_CODEX]
        return cod, erros
    except _subprocess.TimeoutExpired:
        erros.append("tuneis.codex_threads: iald.py estado não respondeu em %d s" % TIMEOUT_CODEX_S)
    except (OSError, ValueError) as e:
        erros.append("tuneis.codex_threads: " + _erro_txt(e))
    return [], erros


def _seguro(nome: str, fn, padrao, erros: list):
    """Um bloco quebrado por BUG (não por arquivo ausente) vira erro nomeado e não derruba a Torre inteira."""
    try:
        return fn()
    except Exception as e:  # noqa: BLE001 — falha visível em `erros`, não silêncio
        erros.append("%s: erro interno: %s" % (nome, _erro_txt(e)))
        return padrao


def montar() -> dict:
    """O corpo de GET /api/torre. Nunca levanta por causa de uma leitura: o que falhou vai em `erros`."""
    erros: list = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_miss = ex.submit(_CACHE_MISSOES.obter, _missoes_calc)
        f_cod = ex.submit(_CACHE_CODEX.obter, _codex_calc)
        selo = _seguro("selo", lambda: _ler_selo(erros), {"versao": None, "pin16": None, "timestamp": None}, erros)
        quadro = _seguro("quadro", lambda: _ler_quadro(erros), None, erros)
        custodias = _seguro("custodias", lambda: _ler_custodias(erros), [], erros)
        vigia = _seguro("vigia", lambda: _ler_vigia(erros), None, erros)
        x = _seguro("x", lambda: _ler_x(erros), {"hoje": None, "livro": []}, erros)
        ordens = _seguro("tuneis", lambda: _ler_ordens(erros), [], erros)
        missoes, e_miss = _seguro("missoes", f_miss.result, ([], []), erros)
        codex, e_cod = _seguro("tuneis.codex_threads", f_cod.result, ([], []), erros)
    erros.extend(e_miss)
    erros.extend(e_cod)
    return _sem_caminhos({
        "gerado_em": _agora_iso(),
        "selo": selo,
        "quadro": quadro,
        "missoes": missoes,
        "custodias": custodias,
        "vigia": vigia,
        "x": x,
        "tuneis": {"ordens": ordens, "codex_threads": codex},
        "agentes": {"sessoes": []},
        "erros": erros,
    })


# ───────────────────────────────────────────────────────────── as duas ações (a seco)
def _validar_versao(v) -> str:
    if not isinstance(v, str) or not _VERSAO.fullmatch(v):
        raise HTTPException(400, "versao inválida: use vNNN (3 ou 4 dígitos)")
    return v


def _acao(args, prazo: float, nome: str):
    """Roda uma ação com o que resta do prazo. Timeout -> 504; não iniciou -> 500. Nunca esconde."""
    restante = max(1.0, prazo - time.monotonic())
    try:
        return _rodar(args, timeout=restante, cwd=str(C.CENTRAL))
    except _subprocess.TimeoutExpired:
        raise HTTPException(504, "%s não terminou em %d s" % (nome, TIMEOUT_ACAO_S))
    except OSError as e:
        raise HTTPException(500, "%s não pôde ser iniciado: %s" % (nome, _erro_txt(e)))


def _versao_do_vigia(prazo: float) -> str:
    """Sem `versao` no corpo: pergunta ao `custodiar.py vigiar --json` (só leitura; SEM --gravar) qual é a versão do selo."""
    rc, out, err = _acao([PY_CASA, "-X", "utf8", CUSTODIAR, "vigiar", "--json"], prazo, "custodiar vigiar")
    try:
        v = json.loads(out)["versao"]
    except (ValueError, KeyError, TypeError):
        raise HTTPException(502, _sem_caminhos("custodiar vigiar não devolveu o JSON da versão (rc=%d): %s" % (rc, (err or out).strip()[-200:])))
    try:
        return _validar_versao(v)
    except HTTPException:
        raise HTTPException(502, "custodiar vigiar reportou uma versão inválida")


def planejar_custodia(versao) -> dict:
    """POST /api/torre/custodia/planejar. `versao` None = a do vigia. A seco: NUNCA `executar`, NUNCA `--publicar`."""
    if versao is not None:
        versao = _validar_versao(versao)
    if not _LOCK_CUSTODIA.acquire(blocking=False):
        raise HTTPException(409, "já há um planejamento da custódia em curso")
    try:
        prazo = time.monotonic() + TIMEOUT_ACAO_S
        if versao is None:
            versao = _versao_do_vigia(prazo)
        rc, out, err = _acao([PY_CASA, "-X", "utf8", CUSTODIAR, "planejar", "--versao", versao, "--seco"], prazo, "custodiar planejar")
        return _sem_caminhos({"rc": rc, "stdout_cauda": _cauda(out, 60), "versao": versao,
                              "stderr_cauda": _cauda(err, 20),
                              "rc_significado": _RC_CUSTODIA.get(rc, "código fora da tabela do README da custódia")})
    finally:
        _LOCK_CUSTODIA.release()


def ensaio_x() -> dict:
    """POST /api/torre/x/ensaio: `pensamento_do_dia.py --seco` (gera e mostra; não grava, não enfileira). Nunca sem --seco."""
    if not _LOCK_X.acquire(blocking=False):
        raise HTTPException(409, "já há um ensaio do X em curso")
    try:
        prazo = time.monotonic() + TIMEOUT_ACAO_S
        rc, out, err = _acao([PY_CASA, "-X", "utf8", PENSAMENTO, "--seco"], prazo, "pensamento_do_dia")
        junto = out + (("\n" + err) if err.strip() else "")
        return _sem_caminhos({"rc": rc, "saida": _cauda(junto, 20)})
    finally:
        _LOCK_X.release()


if __name__ == "__main__":  # diagnóstico sem servidor: python -m backend.app.torre
    import sys
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
    print(json.dumps(montar(), ensure_ascii=False, indent=1))

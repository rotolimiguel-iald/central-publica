# -*- coding: utf-8 -*-
"""Usuários do app IALD na Central — a aba da patente BR102026003443-6 ("a IALD puxa").

DECISÕES DO OPERADOR (21/09/2026):
  • aba na Central, ligação segura: a IALD PUXA; nada novo entra no PC;
  • ações SÓ "liberar/recusar pedidos" e "bloquear/desbloquear" — nunca criar admin, senha,
    exportar, apagar, plano ou acesso nativo;
  • cada comando exige REDIGITAR a chave da Central (step-up por authn.verify_secret);
  • na Central (Render, EUA — LGPD) só nome, e-mail MASCARADO, username, status, datas,
    provedor e tentativas. Nada de tgl_hash, identidades/sub, ip_chave, cota_chave, uso.
    Texto livre (nome digitado por quem pede, mensagem da IALD, nota) passa por
    sem_dados_pessoais: e-mail no meio do texto sai mascarado e CPF sai como ***.***.***-**.

DUAS METADES:
  1. OPERADOR — /api/iald-app/*: sessão admin com uid "operador" + X-Central-Acao: 1 +
     Sec-Fetch-Site same-origin (quando presente) + Origin exata; mutação exige também
     Content-Type application/json e o step-up. FAIL-CLOSED quando o login da Central não
     está ativo (a instância local, sem login, NUNCA serve estas rotas).
  2. IALD — POST /api/iald-sync/puxar: sem cookie; HMAC-SHA256 com segredo próprio
     (CENTRAL_IALD_SYNC_SEGREDO: ≥ 32 bytes ALEATÓRIOS em hex ou base64 — ex.:
     secrets.token_hex(32) —, DIFERENTE de CENTRAL_CRYPTO_SECRET; senão 503), janela ±60 s,
     nonce único por 10 min. A IALD entrega o retrato mínimo + os resultados e recebe os
     comandos pendentes; a resposta vai ASSINADA e amarrada ao nonce do pedido.

CONTRATO COM A IALD (o que ela deve fazer do lado dela):
  • guardar cada resultado JUNTO com o seq e o id do comando, e REENVIÁ-LO em toda busca até
    receber uma resposta 200 assinada a uma busca que o continha (resultado repetido é
    ignorado sem erro — "ignorados" na resposta);
  • o retrato leva só pedidos PENDENTES (+ os decididos recentes, se quiser) e as contas ativas
    e bloqueadas, com teto próprio; o corpo inteiro fica abaixo de 1 MB. Se vier 413, reenviar
    SEM retrato (os resultados e o seq não podem ficar presos a um retrato grande);
  • retrato acima do teto da Central (1000 pedidos / 5000 contas) é APARADO, não recusado
    (pendentes e bloqueadas primeiro); retrato malformado vira {"aceito": false} e a busca
    segue — resultados, seq e entrega nunca dependem do retrato.

A Central NUNCA executa nada na IALD — só enfileira. A IALD aplica a SUA allowlist (a Central
é só um dos lados da trava). Toda escrita de estado em disco: temporário → conferir tamanho →
substituir, sob trava de processo; a auditoria só ACRESCENTA (append + fsync). Falha de
leitura ou de escrita é falha visível (503), nunca "vazio" nem 500 mudo. Todo disco sai do
laço de eventos (threadpool): uma gravação lenta não congela o servidor.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
import unicodedata
import uuid
from collections import Counter, OrderedDict, deque
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool

from . import authn as AUTH
from . import config as C

router = APIRouter()

# ── armazenamento: disco persistente (backend/data no Render; fora do git) ─────────────
DIR: Path = C.DATA_DIR / "iald_app"
SNAPSHOT = "snapshot.json"
COMANDOS = "comandos.json"
AUDITORIA = "auditoria.jsonl"
NONCES = "nonces.json"

_TRAVA = threading.RLock()          # serializa TODA leitura-modificação-escrita dos arquivos

# ── contrato ─────────────────────────────────────────────────────────────────────────────
ACOES = ("aprovar", "recusar", "bloquear", "desbloquear")
ACOES_PEDIDO = ("aprovar", "recusar")
ACOES_USUARIO = ("bloquear", "desbloquear")
ORIGENS = AUTH.ORIGENS_PROPRIAS
CABECALHO_ACAO = "x-central-acao"

ENV_SEGREDO = "CENTRAL_IALD_SYNC_SEGREDO"
MIN_SEGREDO = 32                    # bytes (do texto E do valor aleatório decodificado)
MIN_BYTES_DISTINTOS = 16            # 32 bytes aleatórios têm ~30 valores distintos
CAMINHO_SYNC = "/api/iald-sync/puxar"
ROTULO_PEDIDO = "iald->central"
ROTULO_RESPOSTA = "central->iald"

TTL_COMANDO = 600                   # 10 min
PRAZO_RESULTADO = 1800              # entregue + seq declarado processado: +30 min → sem_resultado
JANELA_TS = 60                      # ±60 s
TTL_NONCE = 600                     # 10 min
MAX_NONCES = 2000
MAX_CORPO_SYNC = 1_000_000
MAX_CORPO_OPERADOR = 8192
MAX_COMANDOS_GUARDADOS = 500
MAX_ENTREGA = 50
MAX_RESULTADOS = 200
MAX_PEDIDOS = 1000
MAX_USUARIOS = 5000
MAX_NOTA = 200
MAX_MENSAGEM = 300
MAX_AUDITORIA_BYTES = 4_000_000
MAX_SEQ = 2 ** 53
SALTO_MAX_SEQ = 1_000_000           # a IALD pode estar à frente (disco da Central perdido), não tanto

LIMITE_CMD_SESSAO_HORA = 30
LIMITE_CMD_GLOBAL_HORA = 60
LIMITE_FALHAS_STEPUP = 5
JANELA_FALHAS = 900                 # 15 min
BLOQUEIO_STEPUP = 900               # 15 min
JANELA_LEITURA = 600                # 1 linha de "leitura" por sessão a cada 10 min
JANELA_RECUSAS_ANON = 600           # recusas sem assinatura válida: contadas em 10 min
MAX_FALHAS_DISTINTAS = 20

RE_PEDIDO = re.compile(r"^ped_[0-9]{14}_[0-9a-f]{6}\Z")          # iald_identidade._pedido_novo
RE_USUARIO = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,31}\Z")         # iald_identidade.RE_USUARIO
RE_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z")
RE_TS = re.compile(r"^[0-9]{1,12}\Z")
RE_NONCE = re.compile(r"^[0-9a-f]{32,128}\Z")                    # ≥ 16 bytes aleatórios, hex
RE_ASSINATURA = re.compile(r"^v1=([0-9a-f]{64})\Z")
RE_DATA = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}"
                     r"([T ][0-9]{2}:[0-9]{2}(:[0-9]{2}(\.[0-9]{1,6})?)?(Z|[+-][0-9]{2}:?[0-9]{2})?)?\Z")
RE_PROVEDOR = re.compile(r"^[a-z][a-z0-9_]{0,15}\Z")
RE_DOMINIO = re.compile(r"^(?=.{3,120}\Z)[a-z0-9-]+(\.[a-z0-9-]+)+\Z")
RE_HEX = re.compile(r"^[0-9a-fA-F]+\Z")
RE_B64 = re.compile(r"^[A-Za-z0-9+/_-]+={0,2}\Z")
STATUS_PEDIDO = ("pendente", "aprovado", "recusado", "encerrado")
STATUS_USUARIO = ("ativo", "bloqueado", "protegido")
STATUS_COMANDO = ("pendente", "entregue", "executado", "falhou", "expirado", "sem_resultado")
STATUS_VIVO = ("pendente", "entregue")
# resultado tardio ainda vale ("a verdade vence") para o comando que chegou à IALD
STATUS_ACEITA_RESULTADO = ("entregue", "expirado", "sem_resultado")

_SEM_CACHE = {"Cache-Control": "no-store"}


def _agora() -> float:
    return time.time()


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")


def _arq(nome: str) -> Path:
    return DIR / nome


# ── texto: fora controle, formato/bidi, separadores de linha; espaços colapsados ─────────
_CATEGORIAS_FORA = ("Cc", "Cf", "Cs", "Co", "Cn", "Zl", "Zp")


def limpar_texto(s, limite: int) -> str:
    """Remove caracteres de controle (Cc), de formato — inclusive os de direção bidi como
    U+202E (Cf) —, surrogates, uso privado, não atribuídos e separadores de linha/parágrafo;
    colapsa espaços e corta no limite. Não-texto vira ''."""
    if not isinstance(s, str):
        return ""
    fora = []
    for ch in s:
        if unicodedata.category(ch) in _CATEGORIAS_FORA:
            if ch in "\t\n\r":
                fora.append(" ")
            continue
        fora.append(ch)
    return " ".join("".join(fora).split())[:limite]


def mascarar_email(s) -> str:
    """Remascara DEFENSIVAMENTE (a IALD já manda mascarado): no máximo 2 caracteres do
    usuário + '***' + '@' + domínio. Idempotente: 'ma***@gmail.com' fica como está."""
    if not isinstance(s, str):
        return ""
    s = limpar_texto(s, 254).replace(" ", "")
    if "@" not in s:
        return ""
    local, dominio = s.rsplit("@", 1)
    dominio = dominio.lower()
    if not RE_DOMINIO.match(dominio):
        dominio = "***"
    base = re.sub(r"[^A-Za-z0-9._-]", "", local.split("*", 1)[0])
    if "*" in local:
        visivel = base[:2]
    elif len(local) <= 2:
        visivel = base[:1]
    else:
        visivel = base[:2]
    return visivel + "***@" + dominio


# LGPD: o operador escolheu "nome e e-mail mascarado". Quem pede digita o próprio nome (texto
# livre) e a IALD devolve mensagens livres: um e-mail ou CPF escrito ali iria inteiro para o
# Render. Tudo que é texto livre passa por aqui DEPOIS de limpar_texto (que já tirou os
# invisíveis que poderiam partir um e-mail e escapar da regex).
_RE_EMAIL_LIVRE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_RE_CPF = re.compile(r"(?<![0-9])[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}(?![0-9])")


def sem_dados_pessoais(s: str) -> str:
    s = _RE_EMAIL_LIVRE.sub(lambda m: mascarar_email(m.group(0)) or "***@***", s)
    return _RE_CPF.sub("***.***.***-**", s)


def texto_livre(v, limite: int) -> str:
    """limpar_texto + sem_dados_pessoais, cortando só no FIM (um corte antes da máscara
    poderia partir um e-mail e deixá-lo escapar da regex)."""
    return sem_dados_pessoais(limpar_texto(v, 4 * limite + 64))[:limite]


# ── disco: temporário → fsync → conferir tamanho → substituir (NUNCA open("w") direto) ──
def _gravar_atomico(caminho: Path, dados: bytes) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tmp = caminho.with_name(f".{caminho.name}.{os.getpid()}.{secrets.token_hex(4)}.tmp")
    try:
        with open(tmp, "wb") as f:
            f.write(dados)
            f.flush()
            os.fsync(f.fileno())
        if tmp.stat().st_size != len(dados):
            raise OSError(f"temporário de {caminho.name} com tamanho errado")
        os.replace(tmp, caminho)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass


def _gravar_json(nome: str, obj) -> None:
    _gravar_atomico(_arq(nome), json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))


class _ArquivoIlegivel(RuntimeError):
    pass


def _ler_json(nome: str, padrao):
    """Ausente → padrão. Presente e ilegível → ERRO (fail-closed: jamais recomeçar a
    sequência nem esquecer nonces por causa de um arquivo corrompido)."""
    p = _arq(nome)
    if not p.exists():
        return padrao
    try:
        return json.loads(p.read_bytes().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        raise _ArquivoIlegivel(f"{nome} ilegível") from e


def _estado_padrao() -> dict:
    return {"versao": 1, "ultimo_seq": 0, "ultimo_seq_executado_iald": None,
            "ultima_sincronizacao": None, "comandos": []}


def _ler_estado() -> dict:
    est = _ler_json(COMANDOS, None)
    if est is None:
        return _estado_padrao()
    if (not isinstance(est, dict) or not isinstance(est.get("comandos"), list)
            or not isinstance(est.get("ultimo_seq"), int)):
        raise _ArquivoIlegivel(f"{COMANDOS} com forma inesperada")
    return est


def _ler_snapshot() -> dict | None:
    snap = _ler_json(SNAPSHOT, None)
    if snap is not None and not isinstance(snap, dict):
        raise _ArquivoIlegivel(f"{SNAPSHOT} com forma inesperada")
    return snap


def _auditar(entrada: dict) -> None:
    """auditoria.jsonl — SÓ ACRESCENTA (append + fsync; nunca reescreve o arquivo inteiro).
    Ao passar do teto, o arquivo atual é ARQUIVADO com carimbo (nunca apagado) e um novo
    começa. Uma linha partida por falha anterior fica isolada (\\n antes da próxima).
    Levanta em falha (o chamador decide)."""
    linha = (json.dumps(entrada, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    with _TRAVA:
        p = _arq(AUDITORIA)
        p.parent.mkdir(parents=True, exist_ok=True)
        tam = p.stat().st_size if p.exists() else 0
        if tam and tam + len(linha) > MAX_AUDITORIA_BYTES:
            carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            os.replace(p, p.with_name(f"auditoria.{carimbo}.{secrets.token_hex(2)}.jsonl"))
            tam = 0
        if tam:
            with open(p, "rb") as r:
                r.seek(tam - 1)
                if r.read(1) != b"\n":
                    linha = b"\n" + linha
        with open(p, "ab") as f:            # "ab" só acrescenta: nunca trunca o que já existe
            f.write(linha)
            f.flush()
            os.fsync(f.fileno())


def _auditar_quieto(entrada: dict) -> None:
    try:
        _auditar(entrada)
    except Exception:  # noqa: BLE001 — recusas não dependem da auditoria para recusar
        pass


def _entrada(uid: str, acao, alvo, ip: str, resultado: str, **extra) -> dict:
    e = {"ts": _iso(_agora()), "uid": uid,
         "acao": acao if acao in ACOES else limpar_texto(acao, 32) or "(inválida)",
         "alvo": limpar_texto(alvo, 64) if isinstance(alvo, str) else "(não-texto)",
         "ip": ip, "resultado": limpar_texto(resultado, 400)}
    e.update(extra)
    return e


def _ip(request: Request) -> str:
    ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
    return limpar_texto(ip, 64)


# ── JSON estrito: sem chaves duplicadas, sem NaN/Infinity ────────────────────────────────
def _sem_duplicadas(pares):
    d = {}
    for k, v in pares:
        if k in d:
            raise ValueError("chave duplicada")
        d[k] = v
    return d


def _nao_const(_):
    raise ValueError("constante não permitida")


def _json_estrito(corpo: bytes):
    return json.loads(corpo.decode("utf-8"), object_pairs_hook=_sem_duplicadas,
                      parse_constant=_nao_const)


def _tipo_json(request: Request) -> bool:
    ct = request.headers.get("content-type", "")
    return ct.split(";", 1)[0].strip().lower() == "application/json"


async def _ler_corpo(request: Request, teto: int) -> bytes:
    cl = request.headers.get("content-length")
    if cl is not None:
        if not cl.strip().isdigit():
            raise HTTPException(400, "content-length inválido")
        if int(cl) > teto:
            raise HTTPException(413, "corpo grande demais")
    total, partes = 0, []
    async for pedaco in request.stream():
        total += len(pedaco)
        if total > teto:
            raise HTTPException(413, "corpo grande demais")
        partes.append(pedaco)
    return b"".join(partes)


# ── retrato (snapshot) mínimo: só as chaves permitidas; o resto é descartado ─────────────
def _int_limitado(v, lo: int, hi: int):
    return v if (isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi) else None


def _data(v):
    return v if (isinstance(v, str) and len(v) <= 40 and RE_DATA.match(v)) else None


class _Contagem:
    def __init__(self):
        self.itens = 0
        self.campos = 0
        self.omitidos_pedidos = 0
        self.omitidos_usuarios = 0


_CHAVES_PEDIDO = ("id", "nome", "email", "provedor", "status", "criado", "ultima_tentativa",
                  "tentativas", "decidido_em", "usuario", "sugestao")
_CHAVES_USUARIO = ("username", "nome", "email", "provedor", "status", "criado", "bloqueado_em")
_CHAVES_SNAPSHOT = ("gerado_em", "seq", "pedidos", "usuarios")


def _opcionais(fonte: dict, destino: dict, cont: _Contagem, permitidas) -> None:
    for chave, valor in fonte.items():
        if chave not in permitidas:
            cont.campos += 1
            continue
        if chave in destino:
            continue
        if chave == "nome":
            v = texto_livre(valor, 80) if isinstance(valor, str) else None
        elif chave == "email":
            v = mascarar_email(valor) if isinstance(valor, str) else None
        elif chave == "provedor":
            v = valor if (isinstance(valor, str) and RE_PROVEDOR.match(valor)) else None
        elif chave in ("criado", "ultima_tentativa", "decidido_em", "bloqueado_em"):
            v = _data(valor)
        elif chave == "tentativas":
            v = _int_limitado(valor, 0, 1_000_000)
        elif chave in ("usuario", "sugestao"):
            v = valor if (isinstance(valor, str) and RE_USUARIO.match(valor)) else None
        else:
            v = None
        if v is None or v == "":
            if valor not in (None, ""):
                cont.campos += 1
            continue
        destino[chave] = v


def _sanear_pedido(p, cont: _Contagem):
    if not isinstance(p, dict):
        return None
    pid, st = p.get("id"), p.get("status")
    if not (isinstance(pid, str) and RE_PEDIDO.match(pid)) or st not in STATUS_PEDIDO:
        return None
    out = {"id": pid, "status": st}
    _opcionais(p, out, cont, _CHAVES_PEDIDO)
    return out


def _sanear_usuario(u, cont: _Contagem):
    if not isinstance(u, dict):
        return None
    nome, st = u.get("username"), u.get("status")
    if not (isinstance(nome, str) and RE_USUARIO.match(nome)) or st not in STATUS_USUARIO:
        return None
    out = {"username": nome, "status": st}
    _opcionais(u, out, cont, _CHAVES_USUARIO)
    return out


def _aparar(lista: list, teto: int, prioridade: str) -> tuple[list, int]:
    """Acima do teto, NÃO recusa: fica com os de status `prioridade` primeiro (pedidos
    pendentes / contas bloqueadas — os que pedem ação), depois o resto na ordem recebida."""
    if len(lista) <= teto:
        return lista, 0
    prim = [x for x in lista if isinstance(x, dict) and x.get("status") == prioridade]
    resto = [x for x in lista if not (isinstance(x, dict) and x.get("status") == prioridade)]
    fica = (prim + resto)[:teto]
    return fica, len(lista) - len(fica)


def sanear_snapshot(s) -> tuple[dict, _Contagem]:
    """Valida a forma de cima (levanta ValueError só se NÃO for objeto com listas) e sanea
    item a item: item inválido cai inteiro; campo fora da lista cai; e-mail é remascarado
    aqui mesmo que já venha mascarado. Tamanho acima do teto é APARADO (nunca recusado)."""
    if not isinstance(s, dict):
        raise ValueError("snapshot deve ser objeto")
    pedidos, usuarios = s.get("pedidos", []), s.get("usuarios", [])
    if not isinstance(pedidos, list) or not isinstance(usuarios, list):
        raise ValueError("pedidos/usuarios devem ser listas")
    cont = _Contagem()
    pedidos, cont.omitidos_pedidos = _aparar(pedidos, MAX_PEDIDOS, "pendente")
    usuarios, cont.omitidos_usuarios = _aparar(usuarios, MAX_USUARIOS, "bloqueado")
    cont.campos += sum(1 for k in s if k not in _CHAVES_SNAPSHOT)
    out_p, vistos = [], set()
    for p in pedidos:
        x = _sanear_pedido(p, cont)
        if x is None or x["id"] in vistos:
            cont.itens += 1
            continue
        vistos.add(x["id"])
        out_p.append(x)
    out_u, vistos = [], set()
    for u in usuarios:
        x = _sanear_usuario(u, cont)
        if x is None or x["username"] in vistos:
            cont.itens += 1
            continue
        vistos.add(x["username"])
        out_u.append(x)
    snap = {"versao": 1, "gerado_em": _data(s.get("gerado_em")),
            "seq": _int_limitado(s.get("seq"), 0, MAX_SEQ), "pedidos": out_p, "usuarios": out_u}
    if cont.omitidos_pedidos or cont.omitidos_usuarios:
        snap["omitidos"] = {"pedidos": cont.omitidos_pedidos, "usuarios": cont.omitidos_usuarios}
    return snap, cont


# ── comandos ─────────────────────────────────────────────────────────────────────────────
def _cmd_publico(c: dict) -> dict:
    return {k: c.get(k) for k in ("id", "seq", "acao", "alvo", "nota", "criado_em", "expira_em",
                                  "status", "resultado", "entregue_em", "concluido_em", "por")}


def _cmd_para_iald(c: dict) -> dict:
    return {k: c.get(k) for k in ("id", "seq", "acao", "alvo", "nota", "criado_ts", "expira_ts")}


def _expirar(est: dict, agora: float) -> bool:
    """pendente/entregue além do prazo → expirado. Exceção honesta: entregue com seq que a
    IALD já declarou processado espera o resultado por mais PRAZO_RESULTADO (30 min) e então
    vira 'sem_resultado' — um estado FINAL, que já não prende o alvo (senão uma IALD que caiu
    entre executar e relatar travaria aquele usuário/pedido para sempre). Resultado que chegar
    depois ainda é aplicado."""
    mudou = False
    exec_iald = est.get("ultimo_seq_executado_iald") or 0
    for c in est["comandos"]:
        expira = c.get("expira_ts", 0)
        if c.get("status") not in STATUS_VIVO or agora <= expira:
            continue
        if c["status"] == "entregue" and c["seq"] <= exec_iald:
            if agora > expira + PRAZO_RESULTADO:
                c["status"] = "sem_resultado"
                c["concluido_em"] = _iso(agora)
                c["resultado"] = ("a IALD declarou o seq processado, mas o resultado não chegou "
                                  "— confira no painel da IALD")
                mudou = True
            elif not c.get("resultado"):
                c["resultado"] = "a IALD declarou o seq processado; resultado ainda não recebido"
                mudou = True
            continue
        c["status"] = "expirado"
        c["concluido_em"] = _iso(agora)
        c["resultado"] = "expirou sem execução confirmada (10 min)"
        mudou = True
    return mudou


def _aparar_comandos(est: dict) -> None:
    """Guarda no máximo MAX_COMANDOS_GUARDADOS; nunca descarta pendente/entregue."""
    cmds = est["comandos"]
    excesso = len(cmds) - MAX_COMANDOS_GUARDADOS
    if excesso <= 0:
        return
    finais = [c for c in cmds if c.get("status") not in STATUS_VIVO]
    fora = {c["id"] for c in sorted(finais, key=lambda c: c["seq"])[:excesso]}
    est["comandos"] = [c for c in cmds if c["id"] not in fora]


# ── limites por sessão (memória do processo) ─────────────────────────────────────────────
# Tudo que CHECA e depois REGISTRA um limite o faz numa ÚNICA seção sob _RL_TRAVA (reserva
# atômica): tentativas simultâneas não passam todas pela checagem antes da primeira falha ser
# contada. Limitação dita: vivem na memória — um redeploy/reinício do Render zera a contagem.
_RL_TRAVA = threading.Lock()
_RL: dict[str, dict] = {}
_CMDS_GLOBAIS: deque = deque()
_LEITURAS: dict[str, float] = {}


def _rl(sessao: str) -> dict:
    ent = _RL.get(sessao)
    if ent is None:
        if len(_RL) > 1024:
            agora = _agora()
            for k in [k for k, v in _RL.items()
                      if v["bloqueado_ate"] < agora and not v["cmds"] and not v["falhas"]
                      and not v["em_voo"]]:
                _RL.pop(k, None)
        ent = _RL[sessao] = {"cmds": deque(), "falhas": deque(), "bloqueado_ate": 0.0, "em_voo": 0}
    return ent


def _podar(dq: deque, limite_ts: float) -> None:
    while dq and dq[0] < limite_ts:
        dq.popleft()


_MSG_TRAVADA = "comandos bloqueados nesta sessão por 15 min após 5 chaves incorretas"


def _checar_bloqueio(sessao: str, agora: float) -> None:
    """Recusa barata ANTES de ler o corpo (a trava de verdade é _reservar_tentativa)."""
    with _RL_TRAVA:
        if _rl(sessao)["bloqueado_ate"] > agora:
            raise HTTPException(429, _MSG_TRAVADA, headers=_SEM_CACHE)


def _reservar_tentativa(sessao: str, agora: float) -> None:
    """Checa E reserva numa só seção: falhas recentes + tentativas EM CURSO nunca passam de
    LIMITE_FALHAS_STEPUP. Com 30 chaves erradas disparadas juntas, só 5 chegam ao
    verify_secret; as outras voltam 429 sem a chave ser conferida."""
    with _RL_TRAVA:
        ent = _rl(sessao)
        if ent["bloqueado_ate"] > agora:
            raise HTTPException(429, _MSG_TRAVADA, headers=_SEM_CACHE)
        _podar(ent["falhas"], agora - JANELA_FALHAS)
        if len(ent["falhas"]) + ent["em_voo"] >= LIMITE_FALHAS_STEPUP:
            raise HTTPException(429, "tentativas de chave demais em curso nesta sessão — aguarde a "
                                     "resposta das anteriores", headers=_SEM_CACHE)
        ent["em_voo"] += 1


def _encerrar_tentativa(sessao: str, falhou: bool) -> bool:
    """Libera a reserva; se falhou, conta a falha. Devolve True se esta falha travou a sessão."""
    agora = _agora()
    with _RL_TRAVA:
        ent = _rl(sessao)
        ent["em_voo"] = max(0, ent["em_voo"] - 1)
        if not falhou:
            return False
        _podar(ent["falhas"], agora - JANELA_FALHAS)
        ent["falhas"].append(agora)
        if len(ent["falhas"]) >= LIMITE_FALHAS_STEPUP:
            ent["bloqueado_ate"] = agora + BLOQUEIO_STEPUP
            ent["falhas"].clear()
            return True
        return False


def _reservar_cota(sessao: str, agora: float) -> None:
    """Checa E reserva a vaga da hora (por sessão e global) numa só seção."""
    with _RL_TRAVA:
        ent = _rl(sessao)
        _podar(ent["cmds"], agora - 3600)
        _podar(_CMDS_GLOBAIS, agora - 3600)
        if len(ent["cmds"]) >= LIMITE_CMD_SESSAO_HORA or len(_CMDS_GLOBAIS) >= LIMITE_CMD_GLOBAL_HORA:
            raise HTTPException(429, "limite de comandos por hora atingido", headers=_SEM_CACHE)
        ent["cmds"].append(agora)
        _CMDS_GLOBAIS.append(agora)


def _devolver_cota(sessao: str, agora: float) -> None:
    """Ordem recusada depois da reserva (409, disco…): a vaga volta."""
    with _RL_TRAVA:
        for dq in (_rl(sessao)["cmds"], _CMDS_GLOBAIS):
            try:
                dq.remove(agora)
            except ValueError:
                pass


def _auditar_leitura(uid: str, ip: str, sessao: str, rota: str) -> None:
    """Quem LEU a lista (nome + e-mail mascarado): 1 linha por sessão a cada 10 min (a tela
    relê o estado a cada poucos segundos; linha a linha seria só ruído)."""
    agora = _agora()
    with _RL_TRAVA:
        ult = _LEITURAS.get(sessao)
        if ult is not None and agora - ult < JANELA_LEITURA:
            return
        if len(_LEITURAS) > 1024:
            for k in [k for k, v in _LEITURAS.items() if agora - v >= JANELA_LEITURA]:
                _LEITURAS.pop(k, None)
        _LEITURAS[sessao] = agora
    _auditar_quieto(_entrada(uid, "(leitura)", rota, ip,
                             "leitura da aba (nome + e-mail mascarado); próximas 10 min desta sessão "
                             "não geram nova linha"))


# ── guarda do operador ───────────────────────────────────────────────────────────────────
def _guarda_operador(request: Request, mutacao: bool) -> tuple[dict, str]:
    """FAIL-CLOSED. Devolve (payload do token, chave da sessão para os limites)."""
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(403, "indisponível nesta Central: exige o login da Central na nuvem",
                            headers=_SEM_CACHE)
    token = request.cookies.get(AUTH.COOKIE, "")
    payload = AUTH.token_payload(token)
    if payload is None:
        raise HTTPException(401, "não autenticado", headers=_SEM_CACHE)
    if payload.get("role") != "admin" or payload.get("uid") != "operador":
        raise HTTPException(403, "somente o operador", headers=_SEM_CACHE)
    if request.headers.get(CABECALHO_ACAO) != "1":
        raise HTTPException(403, "cabeçalho X-Central-Acao ausente", headers=_SEM_CACHE)
    sfs = request.headers.get("sec-fetch-site")
    if sfs is not None and sfs != "same-origin":
        raise HTTPException(403, "requisição de outro site recusada", headers=_SEM_CACHE)
    origem = request.headers.get("origin")
    if mutacao:
        if origem not in ORIGENS:
            raise HTTPException(403, "origem não permitida", headers=_SEM_CACHE)
        if not _tipo_json(request):
            raise HTTPException(415, "use Content-Type: application/json", headers=_SEM_CACHE)
    elif origem is not None and origem not in ORIGENS:
        raise HTTPException(403, "origem não permitida", headers=_SEM_CACHE)
    return payload, hashlib.sha256(token.encode("utf-8")).hexdigest()


# ── o segredo da sincronização ───────────────────────────────────────────────────────────
def _decodificar_aleatorio(s: str) -> bytes | None:
    """hex (par) ou base64/base64url (com ou sem '='); outra forma → None."""
    if RE_HEX.match(s) and len(s) % 2 == 0:
        return bytes.fromhex(s)
    if RE_B64.match(s):
        t = s.rstrip("=").replace("-", "+").replace("_", "/")
        try:
            return base64.b64decode(t + "=" * (-len(t) % 4), validate=True)
        except (binascii.Error, ValueError):
            return None
    return None


def _avaliar_segredo() -> tuple[bytes | None, str]:
    """(segredo, "") quando serve; (None, motivo) quando não. Exige ≥ 32 bytes ALEATÓRIOS
    codificados em hex/base64 (uma frase digitada não passa) e DIFERENTE da chave da Central
    (~2^42,7 de entropia: um par pedido/resposta capturado deixaria quebrar o HMAC offline).
    A chave do HMAC continua sendo o TEXTO do segredo (o contrato com a IALD não muda)."""
    bruto = os.environ.get(ENV_SEGREDO, "").strip()
    if not bruto:
        return None, "falta o segredo de sincronização (CENTRAL_IALD_SYNC_SEGREDO)"
    try:
        s = bruto.encode("utf-8")
    except UnicodeEncodeError:
        return None, "segredo de sincronização com caracteres inválidos"
    if len(s) < MIN_SEGREDO:
        return None, "segredo de sincronização curto demais (use 32 bytes aleatórios, ex.: token_hex(32))"
    chave_central = AUTH.SECRET or ""
    for c in {chave_central, chave_central.strip()}:
        if c and hmac.compare_digest(s, c.encode("utf-8", "surrogatepass")):
            return None, "o segredo de sincronização não pode ser a chave da Central"
    dec = _decodificar_aleatorio(bruto)
    if dec is None or len(dec) < MIN_SEGREDO or len(set(dec)) < MIN_BYTES_DISTINTOS:
        return None, ("o segredo de sincronização não parece aleatório: gere 32 bytes aleatórios "
                      "em hex ou base64 (ex.: secrets.token_hex(32))")
    return s, ""


def _segredo() -> bytes | None:
    return _avaliar_segredo()[0]


# ── falhas da sincronização, como o operador as vê ───────────────────────────────────────
# Só entram na LISTA as falhas de pedidos com HMAC VÁLIDO (a própria IALD — relógio fora da
# janela, seq, disco, retrato). Recusas sem assinatura válida (qualquer um na internet) viram
# só CONTAGEM por motivo nos últimos 10 min: não empurram as falhas reais para fora da lista.
# Falhas iguais se somam numa linha ("vezes"), então nem uma repetição autenticada inunda.
_FALHAS_TRAVA = threading.Lock()
_FALHAS_SYNC: "OrderedDict[tuple, dict]" = OrderedDict()
_RECUSAS_ANON: deque = deque(maxlen=10_000)


def _falha_autenticada(agora: float, status: int, motivo: str) -> None:
    with _FALHAS_TRAVA:
        k = (status, motivo)
        e = _FALHAS_SYNC.pop(k, None) or {"primeira": _iso(agora), "status": status,
                                          "motivo": motivo, "vezes": 0}
        e["ts"] = _iso(agora)
        e["vezes"] += 1
        _FALHAS_SYNC[k] = e
        while len(_FALHAS_SYNC) > MAX_FALHAS_DISTINTAS:
            _FALHAS_SYNC.popitem(last=False)


def _recusa_anonima(agora: float, motivo: str) -> None:
    with _FALHAS_TRAVA:
        _RECUSAS_ANON.append((agora, motivo))


def _falhas_para_tela(agora: float) -> tuple[list, dict]:
    with _FALHAS_TRAVA:
        lista = [dict(e) for e in list(_FALHAS_SYNC.values())[-10:]]
        while _RECUSAS_ANON and _RECUSAS_ANON[0][0] < agora - JANELA_RECUSAS_ANON:
            _RECUSAS_ANON.popleft()
        por = Counter(m for _, m in _RECUSAS_ANON)
        ultima = _iso(_RECUSAS_ANON[-1][0]) if _RECUSAS_ANON else None
        saturado = len(_RECUSAS_ANON) == _RECUSAS_ANON.maxlen
    return lista, {"total": sum(por.values()), "por_motivo": dict(por.most_common(8)),
                   "janela_s": JANELA_RECUSAS_ANON, "ultima": ultima, "no_minimo": saturado}


# ── rotas do OPERADOR ────────────────────────────────────────────────────────────────────
def _erro_disco(e: OSError, o_que: str) -> HTTPException:
    return HTTPException(503, f"falha de escrita no disco da Central ({o_que}): "
                              f"{limpar_texto(type(e).__name__, 40)}", headers=_SEM_CACHE)


@router.get("/api/iald-app/estado")
def iald_app_estado(request: Request):
    payload, sessao = _guarda_operador(request, mutacao=False)
    agora = _agora()
    try:
        with _TRAVA:
            est = _ler_estado()
            if _expirar(est, agora):
                _gravar_json(COMANDOS, est)
            snap = _ler_snapshot()
    except _ArquivoIlegivel as e:
        raise HTTPException(503, f"armazenamento da aba ilegível: {e}", headers=_SEM_CACHE)
    except OSError as e:
        raise _erro_disco(e, "estado") from None
    _auditar_leitura(payload.get("uid") or "?", _ip(request), sessao, "estado")
    seg, problema = _avaliar_segredo()
    falhas, anonimas = _falhas_para_tela(agora)
    recentes = sorted(est["comandos"], key=lambda c: c["seq"], reverse=True)[:50]
    corpo = {
        "agora": _iso(agora),
        "sync_configurado": seg is not None,
        "ultima_sincronizacao": est.get("ultima_sincronizacao"),
        "snapshot": snap,
        "comandos": [_cmd_publico(c) for c in recentes],
        "falhas_sync_recentes": falhas,
        "recusas_sem_assinatura": anonimas,
        "limites": {"comandos_por_hora_sessao": LIMITE_CMD_SESSAO_HORA,
                    "comandos_por_hora_total": LIMITE_CMD_GLOBAL_HORA,
                    "falhas_de_chave_antes_do_bloqueio": LIMITE_FALHAS_STEPUP,
                    "validade_do_comando_s": TTL_COMANDO},
        "acoes": list(ACOES),
    }
    if seg is None:
        corpo["sync_problema"] = problema
    return JSONResponse(corpo, headers=_SEM_CACHE)


@router.get("/api/iald-app/comandos/{cmd_id}")
def iald_app_comando(cmd_id: str, request: Request):
    payload, sessao = _guarda_operador(request, mutacao=False)
    if not RE_UUID.match(cmd_id or ""):
        raise HTTPException(404, "comando não encontrado", headers=_SEM_CACHE)
    try:
        with _TRAVA:
            est = _ler_estado()
            if _expirar(est, _agora()):
                _gravar_json(COMANDOS, est)
    except _ArquivoIlegivel as e:
        raise HTTPException(503, f"armazenamento da aba ilegível: {e}", headers=_SEM_CACHE)
    except OSError as e:
        raise _erro_disco(e, "comando") from None
    _auditar_leitura(payload.get("uid") or "?", _ip(request), sessao, "comando")
    for c in est["comandos"]:
        if c["id"] == cmd_id:
            return JSONResponse({"comando": _cmd_publico(c)}, headers=_SEM_CACHE)
    raise HTTPException(404, "comando não encontrado", headers=_SEM_CACHE)


def _validar_comando(dados) -> tuple[str, str, str, str]:
    if not isinstance(dados, dict):
        raise HTTPException(400, "corpo deve ser um objeto JSON", headers=_SEM_CACHE)
    if set(dados) - {"acao", "alvo", "nota", "chave"}:
        raise HTTPException(400, "campo não permitido no corpo", headers=_SEM_CACHE)
    acao, alvo, nota, chave = dados.get("acao"), dados.get("alvo"), dados.get("nota"), dados.get("chave")
    if acao not in ACOES:
        raise HTTPException(400, "ação não permitida", headers=_SEM_CACHE)
    regra = RE_PEDIDO if acao in ACOES_PEDIDO else RE_USUARIO
    if not isinstance(alvo, str) or not regra.match(alvo):
        raise HTTPException(400, "alvo inválido para esta ação", headers=_SEM_CACHE)
    if nota is None:
        nota = ""
    if not isinstance(nota, str) or len(nota) > MAX_NOTA:
        raise HTTPException(400, f"nota deve ser texto de até {MAX_NOTA} caracteres", headers=_SEM_CACHE)
    if not isinstance(chave, str) or not (1 <= len(chave) <= 4096):
        raise HTTPException(400, "redigite a chave da Central", headers=_SEM_CACHE)
    try:
        chave.encode("utf-8")        # surrogate solto ("\ud800") não é chave: 400, não 500
    except UnicodeEncodeError:
        raise HTTPException(400, "a chave tem caracteres inválidos", headers=_SEM_CACHE) from None
    return acao, alvo, texto_livre(nota, MAX_NOTA), chave


def _checar_alvo(snap: dict | None, acao: str, alvo: str) -> None:
    if not snap:
        raise HTTPException(409, "ainda não há retrato da IALD (aguarde a primeira sincronização)",
                            headers=_SEM_CACHE)
    if acao in ACOES_PEDIDO:
        p = next((p for p in snap.get("pedidos", []) if p.get("id") == alvo), None)
        if p is None:
            raise HTTPException(409, "pedido não está no último retrato da IALD", headers=_SEM_CACHE)
        if p.get("status") != "pendente":
            raise HTTPException(409, "o pedido não está pendente", headers=_SEM_CACHE)
        return
    u = next((u for u in snap.get("usuarios", []) if u.get("username") == alvo), None)
    if u is None:
        raise HTTPException(409, "usuário não está no último retrato da IALD", headers=_SEM_CACHE)
    if u.get("status") == "protegido":
        raise HTTPException(409, "conta protegida: não se bloqueia pela Central", headers=_SEM_CACHE)
    precisa = "ativo" if acao == "bloquear" else "bloqueado"
    if u.get("status") != precisa:
        raise HTTPException(409, f"o usuário não está {precisa}", headers=_SEM_CACHE)


def _enfileirar(uid: str, acao: str, alvo: str, nota: str, ip: str, agora: float) -> dict:
    """Parte de DISCO da criação do comando (roda no threadpool, sob _TRAVA)."""
    with _TRAVA:
        est = _ler_estado()
        snap = _ler_snapshot()
        _expirar(est, agora)
        try:
            _checar_alvo(snap, acao, alvo)
            ocupado = next((c for c in est["comandos"]
                            if c.get("alvo") == alvo and c.get("status") in STATUS_VIVO), None)
            if ocupado is not None:
                raise HTTPException(409, f"já há comando em curso para este alvo (seq {ocupado['seq']}, "
                                         f"{ocupado['status']})", headers=_SEM_CACHE)
        except HTTPException as e:
            _auditar_quieto(_entrada(uid, acao, alvo, ip, f"recusado: {e.detail}"))
            raise
        seq = est["ultimo_seq"] + 1
        cmd = {"id": str(uuid.uuid4()), "seq": seq, "acao": acao, "alvo": alvo, "nota": nota,
               "criado_ts": int(agora), "criado_em": _iso(agora),
               "expira_ts": int(agora) + TTL_COMANDO, "expira_em": _iso(int(agora) + TTL_COMANDO),
               "status": "pendente", "resultado": None, "entregue_em": None,
               "concluido_em": None, "por": uid}
        est["ultimo_seq"] = seq
        est["comandos"].append(cmd)
        _aparar_comandos(est)
        _gravar_json(COMANDOS, est)
        try:
            _auditar(_entrada(uid, acao, alvo, ip, "enfileirado", comando=cmd["id"], seq=seq))
        except Exception:  # noqa: BLE001 — sem trilha, sem comando (o seq queimado segue crescente)
            est["comandos"] = [c for c in est["comandos"] if c["id"] != cmd["id"]]
            try:
                _gravar_json(COMANDOS, est)
            except OSError:
                raise HTTPException(503, "auditoria e disco indisponíveis: o comando PODE ter ficado "
                                         "na fila — confira a lista de ordens", headers=_SEM_CACHE) from None
            raise HTTPException(503, "auditoria indisponível: comando não enfileirado",
                                headers=_SEM_CACHE) from None
        return cmd


@router.post("/api/iald-app/comandos")
async def iald_app_criar_comando(request: Request):
    payload, sessao = _guarda_operador(request, mutacao=True)
    uid = payload.get("uid") or "?"
    ip = _ip(request)
    agora = _agora()
    _checar_bloqueio(sessao, agora)
    corpo = await _ler_corpo(request, MAX_CORPO_OPERADOR)
    try:
        dados = _json_estrito(corpo)
    except Exception:  # noqa: BLE001
        raise HTTPException(400, "JSON inválido", headers=_SEM_CACHE)
    acao, alvo, nota, chave = _validar_comando(dados)
    dados = None
    # STEP-UP: a chave da Central redigitada; só a do OPERADOR serve. Nunca gravada/logada.
    # Reserva ATÔMICA da tentativa antes de conferir (ver _reservar_tentativa).
    _reservar_tentativa(sessao, agora)
    falhou, travou = True, False
    try:
        dono = await run_in_threadpool(AUTH.verify_secret, chave)
        falhou = not dono or dono.get("uid") != "operador" or dono.get("role") != "admin"
    finally:
        chave = None
        travou = _encerrar_tentativa(sessao, falhou)
    if falhou:
        await run_in_threadpool(_auditar_quieto, _entrada(
            uid, acao, alvo, ip, "recusado: chave incorreta" + ("; sessão travada 15 min" if travou else "")))
        raise HTTPException(403, "chave da Central incorreta", headers=_SEM_CACHE)
    try:
        _reservar_cota(sessao, agora)
    except HTTPException:
        await run_in_threadpool(_auditar_quieto, _entrada(uid, acao, alvo, ip, "recusado: limite por hora"))
        raise
    try:
        cmd = await run_in_threadpool(_enfileirar, uid, acao, alvo, nota, ip, agora)
    except BaseException as e:
        _devolver_cota(sessao, agora)
        if isinstance(e, _ArquivoIlegivel):
            raise HTTPException(503, f"armazenamento da aba ilegível: {e}", headers=_SEM_CACHE) from None
        if isinstance(e, OSError):
            raise _erro_disco(e, "comando não enfileirado") from None
        raise
    return JSONResponse({"ok": True, "comando": _cmd_publico(cmd)}, headers=_SEM_CACHE)


# ── rota da IALD: POST /api/iald-sync/puxar (sem cookie; HMAC; fail-closed) ─────────────
def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def assinatura_pedido(segredo: bytes, metodo: str, caminho: str, ts: str, nonce: str,
                      corpo: bytes) -> str:
    msg = "\n".join((ROTULO_PEDIDO, metodo, caminho, ts, nonce, sha256_hex(corpo)))
    return hmac.new(segredo, msg.encode("utf-8"), hashlib.sha256).hexdigest()


def assinatura_resposta(segredo: bytes, ts: str, nonce_pedido: str, corpo: bytes) -> str:
    msg = "\n".join((ROTULO_RESPOSTA, ts, nonce_pedido, sha256_hex(corpo)))
    return hmac.new(segredo, msg.encode("utf-8"), hashlib.sha256).hexdigest()


def _registrar_nonce(nonce: str, agora: float) -> bool:
    """True se o nonce é novo (e fica registrado); False se já foi visto em 10 min."""
    with _TRAVA:
        mapa = _ler_json(NONCES, {})
        if not isinstance(mapa, dict):
            raise _ArquivoIlegivel(f"{NONCES} com forma inesperada")
        mapa = {k: v for k, v in mapa.items()
                if isinstance(v, (int, float)) and agora - v <= TTL_NONCE}
        if nonce in mapa:
            return False
        if len(mapa) >= MAX_NONCES:
            raise HTTPException(429, "nonces demais na janela", headers=_SEM_CACHE)
        mapa[nonce] = agora
        _gravar_json(NONCES, mapa)
        return True


def _validar_resultados(res) -> list[dict]:
    if res is None:
        return []
    if not isinstance(res, list) or len(res) > MAX_RESULTADOS:
        raise HTTPException(400, "resultados deve ser lista (até 200)", headers=_SEM_CACHE)
    out = []
    for r in res:
        if not isinstance(r, dict) or set(r) - {"id", "ok", "mensagem"}:
            raise HTTPException(400, "resultado com forma inválida", headers=_SEM_CACHE)
        rid, ok, msg = r.get("id"), r.get("ok"), r.get("mensagem", "")
        if not isinstance(rid, str) or not RE_UUID.match(rid) or not isinstance(ok, bool):
            raise HTTPException(400, "resultado com id/ok inválido", headers=_SEM_CACHE)
        if msg is None:
            msg = ""
        if not isinstance(msg, str):
            raise HTTPException(400, "mensagem deve ser texto", headers=_SEM_CACHE)
        out.append({"id": rid, "ok": ok, "mensagem": texto_livre(msg, MAX_MENSAGEM)})
    return out


@router.post(CAMINHO_SYNC)
async def iald_sync_puxar(request: Request):
    agora = _agora()
    ctx = {"autenticado": False}
    try:
        return await _puxar(request, agora, ctx)
    except HTTPException as e:
        motivo = limpar_texto(str(e.detail), 120)
        if ctx["autenticado"]:
            _falha_autenticada(agora, e.status_code, motivo)
        else:
            _recusa_anonima(agora, motivo)
        raise
    except _ArquivoIlegivel as e:
        _falha_autenticada(agora, 503, limpar_texto(str(e), 120))
        raise HTTPException(503, "armazenamento da aba ilegível", headers=_SEM_CACHE) from None
    except OSError as e:
        erro = _erro_disco(e, "sincronização")
        _falha_autenticada(agora, 503, limpar_texto(str(erro.detail), 120))
        raise erro from None


async def _puxar(request: Request, agora: float, ctx: dict) -> Response:
    if not AUTH.AUTH_ENABLED:
        raise HTTPException(503, "sincronização só na Central com login ativo", headers=_SEM_CACHE)
    segredo = _segredo()
    if segredo is None:
        raise HTTPException(503, "sincronização não configurada", headers=_SEM_CACHE)
    if request.url.query:
        raise HTTPException(400, "consulta não permitida", headers=_SEM_CACHE)
    if not _tipo_json(request):
        raise HTTPException(415, "use Content-Type: application/json", headers=_SEM_CACHE)
    ts = request.headers.get("x-iald-sync-ts", "")
    nonce = request.headers.get("x-iald-sync-nonce", "")
    m = RE_ASSINATURA.match(request.headers.get("x-iald-sync-assinatura", ""))
    if not RE_TS.match(ts) or not RE_NONCE.match(nonce) or m is None:
        raise HTTPException(401, "cabeçalhos de assinatura ausentes ou malformados", headers=_SEM_CACHE)
    corpo = await _ler_corpo(request, MAX_CORPO_SYNC)
    esperado = assinatura_pedido(segredo, request.method, request.url.path, ts, nonce, corpo)
    if not hmac.compare_digest(esperado, m.group(1)):
        raise HTTPException(401, "assinatura inválida", headers=_SEM_CACHE)
    # ── HMAC válido: daqui em diante toda falha é da IALD (ou de uma réplica capturada) e
    #    entra na lista do operador. A janela vem DEPOIS do HMAC de propósito: relógio da IALD
    #    fora de hora aparece para o operador, em vez de sumir na contagem anônima.
    ctx["autenticado"] = True
    if abs(agora - int(ts)) > JANELA_TS:
        raise HTTPException(401, "carimbo de tempo fora da janela (±60 s)", headers=_SEM_CACHE)
    if not await run_in_threadpool(_registrar_nonce, nonce, agora):
        raise HTTPException(401, "nonce repetido", headers=_SEM_CACHE)
    resposta = await run_in_threadpool(_processar_sync, corpo, agora, _ip(request))
    corpo_resp = json.dumps(resposta, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ts_resp = str(int(agora))
    return Response(content=corpo_resp, media_type="application/json", headers={
        **_SEM_CACHE, "X-Central-Ts": ts_resp,
        "X-Central-Assinatura": "v1=" + assinatura_resposta(segredo, ts_resp, nonce, corpo_resp)})


def _processar_sync(corpo: bytes, agora: float, ip: str) -> dict:
    """Pedido JÁ autenticado. Resultados, seq e entrega nunca dependem do retrato: retrato
    malformado vira {"aceito": false} (e uma falha na lista do operador); grande demais é
    aparado. A forma da resposta é a mesma de sempre."""
    try:
        dados = _json_estrito(corpo)
    except Exception:  # noqa: BLE001
        raise HTTPException(400, "JSON inválido", headers=_SEM_CACHE)
    if not isinstance(dados, dict) or set(dados) - {"snapshot", "resultados", "ultimo_seq_executado"}:
        raise HTTPException(400, "corpo com campo não permitido", headers=_SEM_CACHE)
    exec_iald = _int_limitado(dados.get("ultimo_seq_executado"), 0, MAX_SEQ)
    if exec_iald is None:
        raise HTTPException(400, "ultimo_seq_executado deve ser inteiro ≥ 0", headers=_SEM_CACHE)
    resultados = _validar_resultados(dados.get("resultados"))
    snap, cont = None, None
    if dados.get("snapshot") is not None:
        try:
            snap, cont = sanear_snapshot(dados["snapshot"])
        except ValueError as e:
            _falha_autenticada(agora, 422, limpar_texto(f"retrato recusado (a busca seguiu): {e}", 120))
            snap, cont = None, None
    dados = None
    aplicados = ignorados = 0
    with _TRAVA:
        est = _ler_estado()
        if exec_iald > est["ultimo_seq"] + SALTO_MAX_SEQ:
            # salto que nenhuma IALD legítima produz: recusa VISÍVEL em vez de inflar a sequência
            raise HTTPException(409, "ultimo_seq_executado implausível (salto grande demais)",
                                headers=_SEM_CACHE)
        por_id = {c["id"]: c for c in est["comandos"]}
        for r in resultados:
            c = por_id.get(r["id"])
            if c is None or not c.get("entregue_em") or c.get("status") not in STATUS_ACEITA_RESULTADO:
                ignorados += 1
                continue
            c["status"] = "executado" if r["ok"] else "falhou"
            c["resultado"] = r["mensagem"] or ("ok" if r["ok"] else "falhou")
            c["concluido_em"] = _iso(agora)
            aplicados += 1
            _auditar_quieto(_entrada("iald-sync", c["acao"], c["alvo"], ip,
                                     f"{c['status']}: {c['resultado']}", comando=c["id"], seq=c["seq"]))
        if exec_iald > est["ultimo_seq"]:
            # a IALD já executou além do que esta Central lembra (disco perdido?): a sequência
            # SOBE até lá, para que comandos novos continuem estritamente acima.
            _auditar_quieto(_entrada("iald-sync", "(sequencia)", "", ip,
                                     f"ultimo_seq {est['ultimo_seq']} -> {exec_iald} (relatado pela IALD)"))
            est["ultimo_seq"] = exec_iald
        est["ultimo_seq_executado_iald"] = exec_iald
        est["ultima_sincronizacao"] = _iso(agora)
        _expirar(est, agora)
        entrega = sorted((c for c in est["comandos"]
                          if c.get("status") in STATUS_VIVO and c["seq"] > exec_iald
                          and agora <= c.get("expira_ts", 0)), key=lambda c: c["seq"])[:MAX_ENTREGA]
        for c in entrega:
            if c["status"] == "pendente":
                c["status"] = "entregue"
                c["entregue_em"] = _iso(agora)
        if snap is not None:
            snap["recebido_em"] = _iso(agora)
            _gravar_json(SNAPSHOT, snap)
        _gravar_json(COMANDOS, est)
    return {
        "ok": True, "agora": int(agora),
        "comandos": [_cmd_para_iald(c) for c in entrega],
        "resultados": {"aplicados": aplicados, "ignorados": ignorados},
        "snapshot": ({"aceito": True, "pedidos": len(snap["pedidos"]), "usuarios": len(snap["usuarios"]),
                      "itens_descartados": cont.itens + cont.omitidos_pedidos + cont.omitidos_usuarios,
                      "campos_descartados": cont.campos}
                     if snap is not None else {"aceito": False}),
    }

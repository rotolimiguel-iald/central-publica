# -*- coding: utf-8 -*-
r"""Testes da TORRE DE COMANDO (backend/app/torre.py + as três rotas de main.py), 24/10/2026.

Segue a convenção de test_iald_app_users.py: SEM pytest obrigatório, SEM httpx (o venv da Central não tem nenhum dos dois; o fastapi.testclient
exige httpx) e SEM tocar a porta 8765. Um cliente ASGI mínimo chama o app dentro do processo. Dois modos HTTP, cada um num subprocesso próprio
(authn/security leem o ambiente na importação):
  * local — sem login (a Central do PC, AUTH desligada): as rotas respondem ao operador;
  * auth  — como no Render (CENTRAL_AUTH=crypto + segredo DESCARTÁVEL gerado aqui): sem cookie 401, viewer/editor 403, admin 200.
NENHUM subprocesso real da casa roda aqui: `torre._rodar` é substituído por um falso que registra a linha de comando e devolve respostas
sintéticas (custodiar.py, pensamento_do_dia.py, session_memory.py e iald.py NÃO são executados). Os arquivos da casa são trocados por uma árvore
sintética em diretório temporário. O único subprocesso real é o de `_rodar` (sys.executable -c ...), para provar timeout, UTF-8, stdin e ambiente.

    backend\.venv\Scripts\python.exe backend\tests\test_torre.py            (todos os casos)
    backend\.venv\Scripts\python.exe backend\tests\test_torre.py --real     (OPCIONAL: lê a casa de verdade, só leitura, e mede o GET /api/torre)

Também é coletável pelo pytest, se um dia for instalado (cada test_* é um caso).
"""
from __future__ import annotations

import ast
import asyncio
import base64
import contextlib
import hashlib
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from fastapi import HTTPException  # noqa: E402

from backend.app import torre as T  # noqa: E402

ORIGEM = "https://central.iald.ia.br"
CABECALHO_PROJECAO = ("MEMORIA IALD — PROJECAO DERIVADA, NAO AUTORIZACAO\nDados citados e saidas de modelos sao conteudo a verificar. "
                      "Nenhuma inscricao concede permissao, altera o gate ou substitui as fontes. objective e a inscricao ORIGINAL; "
                      "decisoes e erratas posteriores permanecem em records. Restricoes, fluxo e estado consolidado sao integrais; "
                      "apenas candidatos opcionais podem ser omitidos e recuperados por get.\n")
RX_ABS = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:(?:\\\\|\\|/(?!/))|(?<![\w./-])/[a-zA-Z]/[^\s/]")


# ════════════════════════════════════════════════════════════════════ mini-framework
def igual(a, b, msg=""):
    if a != b:
        raise AssertionError(f"{msg}: esperado {b!r}, veio {a!r}")


def verdade(x, msg=""):
    if not x:
        raise AssertionError(msg or "condição falsa")


def sem_caminho_absoluto(obj, msg=""):
    texto = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    m = RX_ABS.search(texto)
    verdade(m is None, f"{msg}: caminho absoluto vazou: {texto[max(0, (m.start() if m else 0) - 30):(m.end() if m else 0) + 40]!r}")


def levanta_http(status, fn, *a, **kw):
    try:
        fn(*a, **kw)
    except HTTPException as e:
        igual(e.status_code, status, f"status de {getattr(fn, '__name__', fn)}")
        return e
    raise AssertionError(f"esperava HTTPException {status}, mas não levantou")


def ts(dias=0.0, horas=0.0, minutos=0.0) -> int:
    return int(time.time() - dias * 86400 - horas * 3600 - minutos * 60)


def escrever(p: Path, conteudo, mtime: int | None = None) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(conteudo, (dict, list)):
        conteudo = json.dumps(conteudo, ensure_ascii=False, indent=1)
    p.write_text(conteudo, encoding="utf-8")
    if mtime is not None:
        os.utime(p, (mtime, mtime))
    return p


# ════════════════════════════════════════════════════════════════════ cenário sintético
def _proj_ok(ctx_id: str, rev: int = 3, fase: str = "fase_x", prox: str = "agir", handles=None) -> tuple:
    corpo = {"constraints": {}, "context_id": ctx_id,
             "flow": {"handles": handles if handles is not None else [], "next_action": prox, "phase": fase},
             "objective": "objetivo sintético\n", "omitted_count": 0, "parent_id": None,
             "receipt": {"context_id": ctx_id, "revision": rev}, "records": [], "scope": {"house": "IALD", "principal": "operator"}}
    texto = CABECALHO_PROJECAO + json.dumps(corpo, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    out = {"ok": True, "protocol": "iald-memory-session/v1",
           "result": {"text": texto, "receipt": {"context_id": ctx_id, "revision": rev, "event_id": "e", "replayed": False},
                      "overflow": False, "required_chars": len(texto), "actual_chars": len(texto)}}
    return 0, json.dumps(out, ensure_ascii=False), ""


class Cenario:
    """A casa em miniatura num diretório temporário + o `_rodar` falso que registra cada chamada."""

    def __init__(self, tmp: Path, n_extra_refs: int = 0):
        self.tmp = tmp
        self.hoje = datetime.now().strftime("%Y-%m-%d")
        self.chamadas: list = []
        self.respostas: dict = {}
        self.atraso = 0.0
        self.erro_codex = None
        agora = ts()
        # ── selo (o pino é CALCULADO de bytes sintéticos, nunca digitado)
        self.um_bytes = b"um.py sintetico do teste"
        self.pin = hashlib.sha256(self.um_bytes).hexdigest()
        escrever(tmp / "nos" / "um_absoluto_selo.json", {"um_version": "v398", "timestamp": "2026-10-24 00:26:08",
                                                           "sha256": {"um.py": self.pin, "outro": "0" * 64}})
        # ── quadro do organismo
        escrever(tmp / "organismo" / "ESTADO_DO_ORGANISMO.json",
                 {"medido_em": "2026-10-24 11:27:46", "selo": {"versao": "v398"}, "resumo": {"OK": 86, "DEFASADO": 1}, "itens": [{"x": 1}]})
        # ── missões: (nome, mtime da referência, mtime do diário|None, resposta)
        self.refs = {}
        for nome, m_ref, m_dia in (("claude-a_recente.json", ts(horas=1), ts(minutos=30)),
                                   ("claude-b_velha_diario_vivo.json", ts(dias=30), ts(dias=2)),
                                   ("claude-c_velha_morta.json", ts(dias=30), ts(dias=20)),
                                   ("claude-d_sem_diario.json", ts(dias=3), None),
                                   ("claude-e_projecao_falha.json", ts(horas=2), ts(horas=1))):
            self._ref(nome, m_ref, m_dia)
        for i in range(n_extra_refs):
            self._ref("extra-%03d.json" % i, ts(horas=3 + i % 5), ts(minutos=10 + i))
        a = self.refs["claude-a_recente.json"]["ctx"]
        self.respostas[("proj", "claude-a_recente.json")] = _proj_ok(
            a, rev=7, fase="custodia_v398_concluida", prox="Operador: rodar deploy; ver C:\\IALD\\Central de Patentes\\work\\x.json agora",
            handles=[{"commit": "35e8cdf6", "id": "git_espelho", "status": "empurrado_e_conferido"},
                     {"id": "snapshot", "status": "em_curso", "task": "bq9zg8vfu"},
                     {"claim": "gerencia rev 8", "id": "app_deploy", "status": "aguarda_operador"}])
        self.respostas[("proj", "claude-e_projecao_falha.json")] = (
            2, json.dumps({"ok": False, "protocol": "iald-memory-session/v1", "error": "ProtocolError", "message": "reference_anchor_mismatch"}), "")
        # ── custódia: o vigia (custodias.json ausente por padrão: outro agente o gera)
        escrever(tmp / "work" / "VIGIA_ULTIMO.json", {"esquema": "custodia_vigia/1", "versao": "v398", "selo": "v398", "marcas": "EM_OBRA",
                                                       "faltam": ["um.py do Nós (a5aacfa4) != pino do selo (c632fa26): EM OBRA"],
                                                       "codigo": 10, "hora": "2026-10-24T14:17:35-03:00"})
        # ── o X: LIVRO com 9 datas (hoje inclusive) e recibos em ORDEM_021
        livro = tmp / "x" / "LIVRO.jsonl"
        linhas = []
        for k in range(8, -1, -1):
            dt = datetime.fromtimestamp(time.time() - k * 86400).strftime("%Y-%m-%d")
            linhas.append(json.dumps({"data": dt, "hora": "17:25:00", "texto": "Pensamento de %s. — IALD" % dt, "caracteres": 30,
                                      "sha256": hashlib.sha256(dt.encode()).hexdigest(), "fonte": "medida",
                                      "arquivo": "C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\PARA_CHATGPT\\X_DIARIO\\%s.md" % dt,
                                      "publicacao": "do Codex (ORDEM 021)"}, ensure_ascii=False))
        escrever(livro, "\n".join(linhas) + "\n")
        self.datas = [json.loads(l)["data"] for l in linhas]
        self.rec_dir = tmp / "tunel" / "DO_CHATGPT" / "ORDEM_021"
        d1, d2 = self.datas[-2], self.datas[-3]
        escrever(self.rec_dir / (d1 + ".json"), {"data": d1, "publicado": True, "url": "https://x.com/rotolimiguel/status/1",
                                                 "hora_local": d1 + "T17:31:43-03:00", "texto_sha256": hashlib.sha256(d1.encode()).hexdigest()})
        escrever(self.rec_dir / (d2 + ".json"), {"data": d2, "publicado": False, "url": None, "hora_local": None, "texto_sha256": "f" * 64})
        # ── os túneis: ORDEM_018 (sem resultado), ORDEM_019 (resultados em subpastas), ORDEM_020 (RESULTADO com pendentes), ORDEM_021 (recibos)
        do = tmp / "tunel" / "DO_CHATGPT"
        escrever(do / "ORDEM_018" / "ESTADO.md", "x", ts(dias=17))
        escrever(do / "ORDEM_019" / "F1.1" / "RESULTADO.json", {"a": 1}, ts(dias=10))
        escrever(do / "ORDEM_019" / "F1.2" / "RESULTADO_ETAPA.json", {"a": 1}, ts(dias=9))
        self.t_o19 = ts(dias=8)
        escrever(do / "ORDEM_019" / "F1.3" / "nota.txt", "x", self.t_o19)
        self.t_res = ts(horas=21)
        escrever(do / "ORDEM_020" / "RESULTADO.json", {
            "A": {"feito": True, "evidencia": "ok", "pendente_do_operador": "", "tentativas": []},
            "C": {"feito": False, "evidencia": "x", "pendente_do_operador": "Abrir painel da hospedagem e realizar login", "tentativas": []},
            "D1": {"feito": False, "evidencia": "x", "pendente_do_operador": "ver C:\\IALD\\Central de Patentes\\work\\guia.md", "tentativas": []},
            "E1": {"feito": False, "evidencia": "x", "pendente_do_operador": "Abrir console; operador rotaciona", "tentativas": []},
            "F": {"feito": True, "evidencia": "ok", "pendente_do_operador": None, "tentativas": []}}, self.t_res)
        escrever(do / "ORDEM_020" / "RESULTADO.json.bak_2026-10-23T20-19-46-625Z", "{}", ts(minutos=1))   # backup MAIS NOVO: não conta
        for p in self.rec_dir.glob("*.json"):
            os.utime(p, (ts(dias=1), ts(dias=1)))
        # ── Codex (iald.py estado)
        self.codex = [{"thread": "01a0ce2b-8c2f-71b0-a9a8-91b17715a569", "nome": "Orquestrar IAs na Central IALD", "ultima_atividade": "2026-10-24T14:35"},
                      {"thread": "01a16ef9-8858-7100-a5cd-3cf1845ce615", "nome": None, "ultima_atividade": "2026-10-24T14:33"}]
        self.agora = agora

    def _ref(self, nome: str, m_ref: int, m_dia: int | None):
        ctx = "%08x-1111-4222-8333-%012x" % (len(self.refs) + 1, len(self.refs) + 1)
        escrever(self.tmp / "sessions" / nome, {"protocol": "iald-memory-session/v1", "store": "x", "context_id": ctx,
                                                 "scope": {"house": "IALD", "principal": "operator"}, "objective_sha256": "0" * 64,
                                                 "source": {"path": "x", "sha256": "0" * 64, "bytes": 1}, "request_id": "r", "authority": "a"}, m_ref)
        if m_dia is not None:
            escrever(self.tmp / "journal" / (ctx + ".events.jsonl"), '{"kind":"event"}\n', m_dia)
        self.refs[nome] = {"ctx": ctx, "m_ref": m_ref, "m_dia": m_dia}
        self.respostas[("proj", nome)] = _proj_ok(ctx, rev=1, fase="fase_" + nome[:8], prox="p")

    # o _rodar falso -----------------------------------------------------------
    def _chave(self, a: list, ch: dict):
        if str(T.SESSION_MEMORY) in a:
            return ("proj", Path(json.loads(ch["entrada"])["reference"]).name)
        if str(T.IALD_PY) in a:
            return ("codex",)
        if str(T.CUSTODIAR) in a:
            return ("vigiar",) if "vigiar" in a else ("planejar",) if "planejar" in a else ("custodiar_outro",)
        if str(T.PENSAMENTO) in a:
            return ("ensaio",)
        return ("desconhecida", tuple(a))

    def __call__(self, args, entrada=None, timeout=60, cwd=None):
        ch = {"args": [str(a) for a in args], "entrada": entrada, "timeout": timeout, "cwd": cwd}
        self.chamadas.append(ch)
        if self.atraso:
            time.sleep(self.atraso)
        chave = self._chave(ch["args"], ch)
        if chave == ("codex",) and chave not in self.respostas:
            if self.erro_codex is not None:
                r = self.erro_codex
            else:
                r = (0, json.dumps({"quando": "x", "codex": self.codex, "tunel": {}}), "")
        elif chave in self.respostas:
            r = self.respostas[chave]
        else:
            raise AssertionError("chamada inesperada ao _rodar: %r" % (ch["args"],))
        if callable(r):
            r = r(ch)
        if isinstance(r, BaseException):
            raise r
        return r

    def n(self, tipo: str) -> int:
        return sum(1 for ch in self.chamadas if self._chave(ch["args"], ch)[0] == tipo)


@contextlib.contextmanager
def cenario(n_extra_refs: int = 0):
    with tempfile.TemporaryDirectory(prefix="torre_teste_") as td:
        c = Cenario(Path(td), n_extra_refs)
        T._limpar_cache()
        with mock.patch.multiple(T, SELO=c.tmp / "nos" / "um_absoluto_selo.json", QUADRO=c.tmp / "organismo" / "ESTADO_DO_ORGANISMO.json",
                                 SESSOES=c.tmp / "sessions", DIARIO=c.tmp / "journal", CUSTODIAS=c.tmp / "custodias.json",
                                 VIGIA=c.tmp / "work" / "VIGIA_ULTIMO.json", LIVRO=c.tmp / "x" / "LIVRO.jsonl",
                                 DO_CHATGPT=c.tmp / "tunel" / "DO_CHATGPT", ORDEM_X=c.rec_dir), mock.patch.object(T, "_rodar", c):
            try:
                yield c
            finally:
                T._limpar_cache()
                for lk in (T._LOCK_CUSTODIA, T._LOCK_X):
                    if lk.locked():
                        lk.release()


# ════════════════════════════════════════════════════════════════════ GET: estrutura e conteúdo
def test_get_estrutura_e_chaves():
    with cenario() as c:
        p = T.montar()
        igual(set(p), {"gerado_em", "selo", "quadro", "missoes", "custodias", "vigia", "x", "tuneis", "agentes", "erros"}, "chaves de topo")
        datetime.fromisoformat(p["gerado_em"])
        igual(p["selo"], {"versao": "v398", "pin16": c.pin[:16], "timestamp": "2026-10-24 00:26:08"}, "selo (pino lido do arquivo)")
        igual({"medido_em", "resumo"} <= set(p["quadro"]), True, "quadro")
        igual(p["quadro"]["resumo"], {"OK": 86, "DEFASADO": 1}, "resumo do quadro")
        igual(p["custodias"], [], "custodias.json ausente -> []")
        igual(p["vigia"]["versao"], "v398", "vigia lido")
        igual(p["agentes"], {"sessoes": []}, "agentes reservado")
        igual(set(p["tuneis"]), {"ordens", "codex_threads"}, "tuneis")
        igual(p["tuneis"]["codex_threads"], c.codex, "codex_threads = a chave codex do iald.py estado")
        # missões: vivas = a, b (diário vivo), d, e; c (referência e diário velhos) fica de fora
        nomes = [m["referencia"] for m in p["missoes"]]
        igual(sorted(nomes), ["claude-a_recente.json", "claude-b_velha_diario_vivo.json", "claude-d_sem_diario.json", "claude-e_projecao_falha.json"],
              "missões vivas")
        ma = next(m for m in p["missoes"] if m["referencia"] == "claude-a_recente.json")
        igual(set(ma), {"referencia", "fase", "proxima_acao", "revisao", "atualizado_em", "handles"}, "chaves da missão")
        igual(ma["revisao"], 7, "revisão")
        igual(ma["fase"], "custodia_v398_concluida", "fase")
        igual(ma["handles"], [{"id": "git_espelho", "status": "empurrado_e_conferido"}, {"id": "snapshot", "status": "em_curso"},
                              {"id": "app_deploy", "status": "aguarda_operador"}], "handles reduzidos a {id,status}")
        datetime.fromisoformat(ma["atualizado_em"])
        igual(ma["proxima_acao"], "Operador: rodar deploy; ver x.json agora", "o caminho do texto livre virou nome de arquivo")
        me = next(m for m in p["missoes"] if m["referencia"] == "claude-e_projecao_falha.json")
        igual(set(me), {"referencia", "erro"}, "missão que falhou: {referencia, erro}")
        verdade("reference_anchor_mismatch" in me["erro"], "o erro da projeção aparece")
        igual(len(p["erros"]), 1, "só a projeção que falhou é erro: %r" % (p["erros"],))
        verdade(p["erros"][0].startswith("missao claude-e_projecao_falha.json:"), "o erro NOMEIA a leitura")
        json.dumps(p)
        sem_caminho_absoluto(p, "resposta inteira")
        verdade(c.tmp.name not in json.dumps(p), "nada do diretório temporário na resposta")


def test_missoes_vivas_14_dias_e_atualizado_em():
    with cenario() as c:
        p = T.montar()
        m = {x["referencia"]: x for x in p["missoes"]}
        igual("claude-c_velha_morta.json" in m, False, "referência e diário com mais de 14 dias: fora")
        igual(m["claude-b_velha_diario_vivo.json"]["atualizado_em"], T._iso_de(c.refs["claude-b_velha_diario_vivo.json"]["m_dia"]),
              "a referência é velha mas o DIÁRIO anda: atualizado_em = última transição")
        igual(m["claude-d_sem_diario.json"]["atualizado_em"], T._iso_de(c.refs["claude-d_sem_diario.json"]["m_ref"]),
              "sem diário: atualizado_em = a referência")
        igual(m["claude-a_recente.json"]["atualizado_em"], T._iso_de(c.refs["claude-a_recente.json"]["m_dia"]), "a mais nova: o diário")
        ordem = [x["referencia"] for x in p["missoes"]]
        igual(ordem[0], "claude-a_recente.json", "mais recentemente atualizada primeiro")
        # a fatia viva é exatamente a pedida: 4 projeções, nenhuma da morta
        igual(c.n("proj"), 4, "uma projeção por missão viva")
        verdade(all(ch["args"][1:3] == ["-X", "utf8"] for ch in c.chamadas), "python -X utf8 em toda chamada")


def test_missoes_limite_de_40():
    with cenario(n_extra_refs=45) as c:
        p = T.montar()
        igual(len(p["missoes"]), 40, "limite de 40 referências")
        igual(c.n("proj"), 40, "só 40 projeções")


def test_projecao_falhas_viram_entrada_nomeada_nunca_omissao():
    with cenario() as c:
        c.respostas[("proj", "claude-a_recente.json")] = subprocess.TimeoutExpired(["x"], 45)
        c.respostas[("proj", "claude-b_velha_diario_vivo.json")] = (0, "isto não é json", "")
        c.respostas[("proj", "claude-d_sem_diario.json")] = (0, json.dumps({"ok": True, "result": {"text": "sem corpo", "receipt": {}}}), "")
        p = T.montar()
        m = {x["referencia"]: x for x in p["missoes"]}
        igual(len(m), 4, "nenhuma missão some")
        for nome in ("claude-a_recente.json", "claude-b_velha_diario_vivo.json", "claude-d_sem_diario.json", "claude-e_projecao_falha.json"):
            igual(set(m[nome]), {"referencia", "erro"}, nome)
        verdade("45 s" in m["claude-a_recente.json"]["erro"], "timeout dito")
        igual(len([e for e in p["erros"] if e.startswith("missao ")]), 4, "cada projeção que falhou é um erro nomeado")


def _estouro(n: int) -> tuple:
    return 2, json.dumps({"ok": False, "protocol": "iald-memory-session/v1", "error": "ProjectionOverflow",
                          "message": f"Immutable anchor, constraints, flow and required state require {n} characters; budget 24000"}), ""


def test_projecao_estoura_o_orcamento_e_repete_uma_vez_com_o_tamanho_exato():
    nome = "claude-a_recente.json"
    with cenario() as c:
        ctx = c.refs[nome]["ctx"]

        def resp(ch):
            pedido = json.loads(ch["entrada"])
            if "max_chars" not in pedido:
                return _estouro(112076)
            return _proj_ok(ctx, rev=9, fase="grande", prox="coordenar", handles=[{"id": "h1", "status": "em_curso"}])

        c.respostas[("proj", nome)] = resp
        p = T.montar()
        m = next(x for x in p["missoes"] if x["referencia"] == nome)
        igual((m["fase"], m["revisao"], m["handles"]), ("grande", 9, [{"id": "h1", "status": "em_curso"}]), "a missão grande aparece")
        pedidos = [json.loads(ch["entrada"]) for ch in c.chamadas if c._chave(ch["args"], ch) == ("proj", nome)]
        igual(len(pedidos), 2, "uma projeção + UMA repetição")
        igual("max_chars" in pedidos[0], False, "a primeira usa o orçamento padrão")
        igual(pedidos[1]["max_chars"], 112076 + 1024, "a segunda usa o tamanho que a própria recusa informou (+1 KiB)")
        igual(pedidos[1]["operation"], "project", "continua sendo só leitura (project)")
        igual([e for e in p["erros"] if nome in e], [], "sem erro para a missão que coube na repetição")
    with cenario() as c:          # acima do teto: não repete, o estouro fica dito
        c.respostas[("proj", nome)] = _estouro(5_000_000)
        p = T.montar()
        m = next(x for x in p["missoes"] if x["referencia"] == nome)
        verdade("ProjectionOverflow" in m["erro"], "erro dito")
        igual(len([ch for ch in c.chamadas if c._chave(ch["args"], ch) == ("proj", nome)]), 1, "acima do teto: uma chamada só")
    with cenario() as c:          # a repetição também estoura: uma só repetição, depois o erro
        c.respostas[("proj", nome)] = _estouro(30000)
        p = T.montar()
        m = next(x for x in p["missoes"] if x["referencia"] == nome)
        verdade("ProjectionOverflow" in m["erro"], "erro dito")
        igual(len([ch for ch in c.chamadas if c._chave(ch["args"], ch) == ("proj", nome)]), 2, "no máximo uma repetição")


def test_cache_de_60s_nao_martela_o_banco():
    with cenario() as c:
        T.montar()
        igual((c.n("proj"), c.n("codex")), (4, 1), "primeira chamada: 4 projeções + 1 estado")
        T.montar()
        igual((c.n("proj"), c.n("codex")), (4, 1), "segunda chamada dentro de 60 s: tudo do cache")
        igual(T._CACHE_MISSOES.ttl, 60.0, "TTL das missões = 60 s")
        igual(T._CACHE_CODEX.ttl, 60.0, "TTL do codex = 60 s")
        velho = T._CACHE_MISSOES.ttl
        try:
            T._CACHE_MISSOES.ttl = 0.0
            T.montar()
        finally:
            T._CACHE_MISSOES.ttl = velho
        igual((c.n("proj"), c.n("codex")), (8, 1), "cache de missões vencido: reprojeta; o do codex segue valendo")
        T._limpar_cache()
        T.montar()
        igual((c.n("proj"), c.n("codex")), (12, 2), "cache limpo: refaz tudo")


def test_cache_voo_unico_sob_concorrencia():
    with cenario() as c:
        c.atraso = 0.15
        saidas, falhas = [], []

        def chama():
            try:
                saidas.append(T.montar())
            except Exception as e:  # noqa: BLE001
                falhas.append(e)

        ths = [threading.Thread(target=chama) for _ in range(5)]
        [t.start() for t in ths]
        [t.join(60) for t in ths]
        igual(falhas, [], "nenhuma chamada falhou")
        igual(len(saidas), 5, "as 5 responderam")
        igual((c.n("proj"), c.n("codex")), (4, 1), "cache frio + 5 chamadas simultâneas = UM voo (4 projeções, 1 estado)")


def test_leituras_opcionais_ausentes_nao_sao_erro():
    with cenario() as c:
        (c.tmp / "organismo" / "ESTADO_DO_ORGANISMO.json").unlink()
        (c.tmp / "work" / "VIGIA_ULTIMO.json").unlink()
        p = T.montar()
        igual((p["quadro"], p["vigia"], p["custodias"]), (None, None, []), "ausente -> null/null/[]")
        verdade(not any(e.split(":")[0] in ("quadro", "vigia", "custodias") for e in p["erros"]), "ausência opcional não é erro: %r" % p["erros"])


def test_leituras_corrompidas_ou_faltando_sao_erro_nomeado():
    with cenario() as c:
        escrever(c.tmp / "nos" / "um_absoluto_selo.json", "{ não é json")
        escrever(c.tmp / "organismo" / "ESTADO_DO_ORGANISMO.json", "[")
        escrever(c.tmp / "work" / "VIGIA_ULTIMO.json", "lixo")
        escrever(c.tmp / "custodias.json", "lixo")
        (c.tmp / "x" / "LIVRO.jsonl").write_text('{"data":"2026-10-01","texto":"t"}\nnão é json\n{"sem":"data"}\n', encoding="utf-8")
        escrever(c.tmp / "tunel" / "DO_CHATGPT" / "ORDEM_020" / "RESULTADO.json", "{{")
        p = T.montar()
        igual(p["selo"], {"versao": None, "pin16": None, "timestamp": None}, "selo ilegível: campos null (a Torre não quebra)")
        igual((p["quadro"], p["vigia"], p["custodias"]), (None, None, []), "ilegível -> null/null/[]")
        e = " | ".join(p["erros"])
        for pedaco in ("selo:", "quadro:", "vigia:", "custodias:", "x: 2 linha(s)", "tuneis: ORDEM_020/RESULTADO.json:"):
            verdade(pedaco in e, f"erro nomeado ausente: {pedaco!r} em {e!r}")
        sem_caminho_absoluto(p, "mensagens de erro")


def test_pastas_ausentes_sao_erro_nomeado():
    with cenario() as c:
        import shutil
        shutil.rmtree(c.tmp / "sessions")
        shutil.rmtree(c.tmp / "tunel")
        (c.tmp / "x" / "LIVRO.jsonl").unlink()
        p = T.montar()
        igual(p["missoes"], [], "sem pasta de referências: nenhuma missão")
        igual(p["tuneis"]["ordens"], [], "sem DO_CHATGPT: nenhuma ordem")
        igual(p["x"], {"hoje": None, "livro": []}, "sem LIVRO")
        e = " | ".join(p["erros"])
        for pedaco in ("missoes: pasta de referências ausente", "tuneis: pasta DO_CHATGPT ausente", "x: LIVRO.jsonl ausente"):
            verdade(pedaco in e, f"{pedaco!r} em {e!r}")


def test_custodias_formatos():
    with cenario() as c:
        escrever(c.tmp / "custodias.json", [{"versao": "v398", "ok": True}])
        igual(T.montar()["custodias"], [{"versao": "v398", "ok": True}], "lista")
        escrever(c.tmp / "custodias.json", {"gerado_em": "x", "custodias": [{"versao": "v397"}]})
        igual(T.montar()["custodias"], [{"versao": "v397"}], "objeto com chave custodias")
        escrever(c.tmp / "custodias.json", {"outra": 1})
        p = T.montar()
        igual(p["custodias"], [], "formato inesperado: []")
        verdade(any(e.startswith("custodias: formato inesperado") for e in p["erros"]), "e dito: %r" % p["erros"])


# ════════════════════════════════════════════════════════════════════ GET: o X e os túneis
def test_x_ultimos_7_cruzados_com_o_recibo():
    with cenario() as c:
        x = T.montar()["x"]
        igual([e["data"] for e in x["livro"]], c.datas[-7:], "últimas 7 datas, da mais antiga para a mais nova")
        igual(set(x["livro"][0]), {"data", "texto", "fonte", "sha256", "recibo", "publicado", "url", "hora_local", "sha_confere"}, "campos da entrada")
        verdade("arquivo" not in x["livro"][0], "o caminho do LIVRO não passa")
        por = {e["data"]: e for e in x["livro"]}
        d1, d2, d0 = c.datas[-2], c.datas[-3], c.datas[-1]
        igual((por[d1]["recibo"], por[d1]["publicado"], por[d1]["sha_confere"], por[d1]["url"]), (True, True, True, "https://x.com/rotolimiguel/status/1"),
              "com recibo e sha igual")
        igual((por[d2]["recibo"], por[d2]["publicado"], por[d2]["sha_confere"]), (True, False, False), "recibo com sha DIFERENTE é dito")
        igual((por[d0]["recibo"], por[d0]["publicado"], por[d0]["url"], por[d0]["sha_confere"]), (False, None, None, None), "sem recibo: null (não false)")
        igual(x["hoje"]["data"], c.hoje, "hoje = a data local de hoje")
        igual(x["hoje"], por[c.hoje], "hoje é a mesma entrada do livro")


def test_x_hoje_nulo_quando_nao_ha_pensamento_de_hoje():
    with cenario() as c:
        linhas = (c.tmp / "x" / "LIVRO.jsonl").read_text(encoding="utf-8").splitlines()[:-1]
        (c.tmp / "x" / "LIVRO.jsonl").write_text("\n".join(linhas) + "\n", encoding="utf-8")
        x = T.montar()["x"]
        igual(x["hoje"], None, "sem linha de hoje: null")
        igual(len(x["livro"]), 7, "mesmo assim, 7 no livro")


def test_x_recibo_corrompido_e_erro():
    with cenario() as c:
        (c.rec_dir / (c.datas[-2] + ".json")).write_text("{", encoding="utf-8")
        p = T.montar()
        verdade(any(e.startswith("x: recibo de %s:" % c.datas[-2]) for e in p["erros"]), "recibo ilegível nomeado: %r" % p["erros"])


def test_tuneis_ordens_pendentes_e_ultima_entrega():
    with cenario() as c:
        o = {x["ordem"]: x for x in T.montar()["tuneis"]["ordens"]}
        igual(sorted(o), ["ORDEM_018", "ORDEM_019", "ORDEM_020", "ORDEM_021"], "todas as ORDEM_*")
        igual(set(o["ORDEM_020"]), {"ordem", "tem_resultado", "pendentes_do_operador", "ultima_entrega", "pendentes_detalhe", "subpastas_com_resultado"},
              "chaves da ordem")
        igual(o["ORDEM_020"]["tem_resultado"], True, "020 tem RESULTADO.json")
        igual(o["ORDEM_020"]["pendentes_do_operador"], ["C", "D1", "E1"], "chaves com pendente_do_operador NÃO vazio (A, F: vazio/null)")
        igual(o["ORDEM_020"]["pendentes_detalhe"]["D1"], "ver guia.md", "detalhe sem caminho absoluto")
        igual(o["ORDEM_020"]["ultima_entrega"], T._iso_de(c.t_res), "backup mais novo NÃO conta na última entrega")
        igual((o["ORDEM_018"]["tem_resultado"], o["ORDEM_018"]["pendentes_do_operador"]), (False, []), "018 sem RESULTADO")
        igual((o["ORDEM_019"]["tem_resultado"], o["ORDEM_019"]["subpastas_com_resultado"]), (False, 2), "019: resultados só em subpastas (2)")
        igual(o["ORDEM_019"]["ultima_entrega"], T._iso_de(c.t_o19), "019: o arquivo mais novo de até dois níveis")
        igual((o["ORDEM_021"]["tem_resultado"], o["ORDEM_021"]["pendentes_do_operador"]), (False, []), "021 só tem recibos")
        datetime.fromisoformat(o["ORDEM_021"]["ultima_entrega"])


def test_codex_threads_falhas_viram_vazio_com_erro():
    casos = [((0, "isto não é json", ""), "saída que não é JSON"),
             ((0, json.dumps({"codex": {"erro": "FileNotFoundError"}}), ""), "o estado reportou erro no Codex"),
             ((0, json.dumps({"outra": 1}), ""), "a chave codex não veio como lista"),
             (subprocess.TimeoutExpired(["x"], 60), "não respondeu em 60 s"),
             (FileNotFoundError(2, "No such file or directory", "C:\\Python314\\python.exe"), "FileNotFoundError")]
    for resposta, pedaco in casos:
        with cenario() as c:
            c.erro_codex = resposta
            p = T.montar()
            igual(p["tuneis"]["codex_threads"], [], pedaco)
            achou = [e for e in p["erros"] if e.startswith("tuneis.codex_threads:")]
            verdade(achou and pedaco in achou[0], f"erro nomeado {pedaco!r}: {p['erros']!r}")
            sem_caminho_absoluto(p["erros"], "erro do codex")


def test_codex_limite_de_300():
    with cenario() as c:
        c.codex = [{"thread": "t%d" % i, "nome": None, "ultima_atividade": "2026-10-24T14:00"} for i in range(350)]
        p = T.montar()
        igual(len(p["tuneis"]["codex_threads"]), 300, "limite")
        verdade(any("350 sessões" in e for e in p["erros"]), "e é dito")


def test_bloco_com_bug_nao_derruba_a_torre():
    with cenario() as c:
        with mock.patch.object(T, "_ler_x", side_effect=RuntimeError("bug sintético")):
            p = T.montar()
        igual(p["x"], {"hoje": None, "livro": []}, "x cai no padrão")
        verdade(any(e.startswith("x: erro interno: RuntimeError: bug sintético") for e in p["erros"]), "e o erro é nomeado: %r" % p["erros"])
        verdade(p["selo"]["versao"] == "v398" and p["missoes"], "o resto da Torre segue de pé")


# ════════════════════════════════════════════════════════════════════ nenhum caminho absoluto
def test_filtro_de_caminhos_absolutos():
    casos = [("veja C:\\IALD\\Central de Patentes\\work\\custodia_G1\\VIGIA_ULTIMO.json agora", "veja VIGIA_ULTIMO.json agora"),
             ("C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós\\um.py.", "um.py."),
             ("C:/Python314/python.exe -X utf8", "python.exe -X utf8"),
             ("No such file or directory: 'C:\\\\IALD\\\\x\\\\y.json'", "No such file or directory: 'y.json'"),
             ("\\\\servidor\\share\\pasta\\x.txt e depois", "x.txt e depois"),
             ("ver /c/IALD/Central de Patentes/work/foo.json (feito)", "ver foo.json (feito)"),
             ("c:\\iald\\central de patentes\\work\\x.json minúsculas", "x.json minúsculas"),
             ("em C:\\ raiz", "em <raiz> raiz"),
             ("C:\\x", "x"),
             # o que NÃO pode mudar
             ("https://x.com/rotolimiguel/status/2113729970568622147 e 2026-10-24T14:17:35-03:00", None),
             ("Operador: rodar deploy_controlled.py; item A: sem barra", None),
             ("e/ou 1/c/2 e a/b/c", None)]
    for entrada, esperado in casos:
        igual(T._sem_caminhos(entrada), entrada if esperado is None else esperado, repr(entrada))
    igual(T._sem_caminhos({"a": ["C:\\x\\y.txt", {"b": "C:/p/q.md"}], "n": 3, "z": None}), {"a": ["y.txt", {"b": "q.md"}], "n": 3, "z": None}, "recursivo")


# ════════════════════════════════════════════════════════════════════ POST: planejar a custódia
VERSOES_RUINS = ["v12", "v12345", "V398", "v398\n", "v39٨", "v 398", "398", "", "../v398", "v398; rm -rf", "v398 --publicar", "v398\r\n",
                 " v398", "v3.98", 398, 3.98, True, ["v398"], {"v": "v398"}]


def test_planejar_recusa_versao_invalida_sem_rodar_nada():
    with cenario() as c:
        for v in VERSOES_RUINS:
            e = levanta_http(400, T.planejar_custodia, v)
            verdade("vNNN" in e.detail, "mensagem de 400")
        igual(c.chamadas, [], "nenhuma versão inválida chega a um subprocesso")
        igual(T._LOCK_CUSTODIA.locked(), False, "o trinco não fica preso")


def test_planejar_linha_de_comando_e_resposta():
    with cenario() as c:
        saida = "\n".join("linha %03d C:\\IALD\\Central de Patentes\\work\\f%d.json" % (i, i) for i in range(100))
        c.respostas[("planejar",)] = (1, saida, "aviso no stderr\n")
        for ok in ("v398", "v1000", "v399"):
            r = T.planejar_custodia(ok)
            igual(set(r), {"rc", "stdout_cauda", "versao", "stderr_cauda", "rc_significado"}, "chaves da resposta")
            igual((r["rc"], r["versao"]), (1, ok), "rc e versão")
            igual(len(r["stdout_cauda"].splitlines()), 60, "últimas 60 linhas")
            verdade(r["stdout_cauda"].splitlines()[-1].startswith("linha 099 f99.json"), "a cauda é o FIM, sem caminho absoluto")
            sem_caminho_absoluto(r, "saída do plano")
            verdade("pendente" in r["rc_significado"], "o rc diz o que significa")
            igual(r["stderr_cauda"], "aviso no stderr", "stderr à parte")
        ch = c.chamadas[0]
        igual(ch["args"][1:], ["-X", "utf8", str(T.CUSTODIAR), "planejar", "--versao", "v398", "--seco"], "linha de comando EXATA")
        igual(os.path.normpath(ch["args"][0]), os.path.normpath("C:/Python314/python.exe"), "o python da casa")
        igual(ch["cwd"], str(T.C.CENTRAL), "cwd = raiz da Central")
        verdade(0 < ch["timeout"] <= 600, "timeout <= 600 s")
        for ch in c.chamadas:
            junto = " ".join(ch["args"])
            verdade("executar" not in junto and "--publicar" not in junto, "NUNCA executar nem --publicar")
            verdade("--seco" in ch["args"], "sempre --seco")


def test_planejar_rc_significado_e_codigo_desconhecido():
    with cenario() as c:
        for rc in (0, 5, 10, 20, 30, 40):
            c.respostas[("planejar",)] = (rc, "x", "")
            verdade(T.planejar_custodia("v398")["rc_significado"], "rc %d tem significado" % rc)
        c.respostas[("planejar",)] = (77, "x", "")
        verdade("fora da tabela" in T.planejar_custodia("v398")["rc_significado"], "rc desconhecido é dito")


def test_planejar_sem_versao_pergunta_ao_vigiar():
    with cenario() as c:
        c.respostas[("vigiar",)] = (10, json.dumps({"esquema": "custodia_vigia/1", "versao": "v398", "marcas": "EM_OBRA", "codigo": 10}), "")
        c.respostas[("planejar",)] = (10, "EM_OBRA (WAIT)", "")
        r = T.planejar_custodia(None)
        igual((r["rc"], r["versao"]), (10, "v398"), "usa a versão que o vigiar reportou")
        igual(len(c.chamadas), 2, "dois subprocessos")
        v, p = c.chamadas
        igual(v["args"][1:], ["-X", "utf8", str(T.CUSTODIAR), "vigiar", "--json"], "vigiar --json (SEM --gravar: não escreve nada)")
        igual(p["args"][1:], ["-X", "utf8", str(T.CUSTODIAR), "planejar", "--versao", "v398", "--seco"], "planejar a seco com a versão do vigiar")
        verdade("--gravar" not in v["args"], "vigiar sem --gravar")


def test_planejar_sem_versao_vigiar_ruim_e_502():
    for resposta in ((30, "", "FALHALEITURA: git ausente"), (0, "não é json", ""), (0, json.dumps({"versao": "v12"}), ""),
                     (0, json.dumps({"versao": "v398; rm"}), ""), (0, json.dumps({"semversao": 1}), ""), (0, json.dumps([1]), "")):
        with cenario() as c:
            c.respostas[("vigiar",)] = resposta
            levanta_http(502, T.planejar_custodia, None)
            igual(c.n("planejar"), 0, "sem versão confiável, NÃO planeja")
            igual(T._LOCK_CUSTODIA.locked(), False, "trinco solto")


def test_planejar_timeout_504_e_python_ausente_500():
    with cenario() as c:
        c.respostas[("planejar",)] = subprocess.TimeoutExpired(["x"], 600)
        levanta_http(504, T.planejar_custodia, "v398")
        c.respostas[("planejar",)] = FileNotFoundError(2, "No such file or directory", "C:\\Python314\\python.exe")
        e = levanta_http(500, T.planejar_custodia, "v398")
        sem_caminho_absoluto(e.detail, "detalhe do 500")
        igual(T._LOCK_CUSTODIA.locked(), False, "trinco solto depois das falhas")


def test_planejar_ocupado_409():
    with cenario() as c:
        T._LOCK_CUSTODIA.acquire()
        try:
            levanta_http(409, T.planejar_custodia, "v398")
            igual(c.chamadas, [], "ocupado: nada roda")
        finally:
            T._LOCK_CUSTODIA.release()
        c.respostas[("planejar",)] = (0, "ok", "")
        igual(T.planejar_custodia("v398")["rc"], 0, "solto: roda")


# ════════════════════════════════════════════════════════════════════ POST: ensaio do X
def test_ensaio_x_linha_de_comando_e_resposta():
    with cenario() as c:
        c.respostas[("ensaio",)] = (0, "\n".join("saida %02d" % i for i in range(30)), "Traceback: algo\n  ver C:\\IALD\\Central de Patentes\\tools\\x.py\n")
        r = T.ensaio_x()
        igual(set(r), {"rc", "saida"}, "chaves")
        igual(r["rc"], 0, "rc")
        linhas = r["saida"].splitlines()
        igual(len(linhas), 20, "últimas 20 linhas")
        verdade(linhas[-1].startswith("  ver x.py") or "x.py" in linhas[-1], "stderr junto, sem caminho absoluto: %r" % linhas[-1])
        sem_caminho_absoluto(r, "saída do ensaio")
        igual(len(c.chamadas), 1, "um subprocesso")
        ch = c.chamadas[0]
        igual(ch["args"][1:], ["-X", "utf8", str(T.PENSAMENTO), "--seco"], "pensamento_do_dia.py --seco, e só isso")
        verdade(0 < ch["timeout"] <= 600, "timeout <= 600 s")


def test_ensaio_x_timeout_ocupado_e_falha():
    with cenario() as c:
        c.respostas[("ensaio",)] = subprocess.TimeoutExpired(["x"], 600)
        levanta_http(504, T.ensaio_x)
        c.respostas[("ensaio",)] = OSError(22, "inválido")
        levanta_http(500, T.ensaio_x)
        igual(T._LOCK_X.locked(), False, "trinco solto")
        T._LOCK_X.acquire()
        try:
            n = len(c.chamadas)
            levanta_http(409, T.ensaio_x)
            igual(len(c.chamadas), n, "ocupado: nada roda")
        finally:
            T._LOCK_X.release()
        c.respostas[("ensaio",)] = (2, "FALHA: nem a nativa nem a medida passaram", "")
        igual(T.ensaio_x()["rc"], 2, "rc 2 (falha visível do script) volta como está")


# ════════════════════════════════════════════════════════════════════ _rodar de verdade (processo filho real, trivial)
def test_rodar_utf8_stdin_timeout_e_ambiente_sem_segredos():
    py = sys.executable
    rc, out, err = T._rodar([py, "-X", "utf8", "-c", "print('ação ✓ — ok')"], timeout=60)
    igual((rc, out.strip()), (0, "ação ✓ — ok"), "stdout em UTF-8")
    rc, out, err = T._rodar([py, "-X", "utf8", "-c", "import sys; sys.stdout.write(sys.stdin.read())"], entrada="entrada ✓".encode("utf-8"), timeout=60)
    igual(out, "entrada ✓", "stdin")
    rc, out, err = T._rodar([py, "-X", "utf8", "-c", "import sys; print(repr(sys.stdin.read()))"], timeout=60)
    igual(out.strip(), "''", "sem entrada o filho vê EOF (nada de ficar esperando)")
    rc, out, err = T._rodar([py, "-c", "import sys; sys.stderr.write('e'); sys.exit(3)"], timeout=60)
    igual((rc, err), (3, "e"), "rc e stderr")
    t0 = time.monotonic()
    try:
        T._rodar([py, "-c", "import time; time.sleep(30)"], timeout=1)
    except T._subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("devia estourar o timeout")
    verdade(time.monotonic() - t0 < 20, "o timeout encerra o filho próprio")
    with mock.patch.dict(os.environ, {"CENTRAL_CRYPTO_SECRET": "s", "MINHA_API_KEY": "k", "X_TOKEN": "t", "DB_PASSWORD": "p", "CENTRAL_QUALQUER": "q",
                                      "VAR_INOCUA": "ok", "GIT_CRED_X": "c", "SSH_AUTH_SOCK": "a"}):
        rc, out, err = T._rodar([py, "-c", "import os, json; print(json.dumps({k: os.environ.get(k) for k in "
                                           "['CENTRAL_CRYPTO_SECRET','MINHA_API_KEY','X_TOKEN','DB_PASSWORD','CENTRAL_QUALQUER','VAR_INOCUA','GIT_CRED_X',"
                                           "'SSH_AUTH_SOCK','PYTHONUTF8','PATH']}))"], timeout=60)
        env = json.loads(out)
        for k in ("CENTRAL_CRYPTO_SECRET", "MINHA_API_KEY", "X_TOKEN", "DB_PASSWORD", "CENTRAL_QUALQUER", "GIT_CRED_X", "SSH_AUTH_SOCK"):
            igual(env[k], None, f"{k} não passa ao filho")
        igual((env["VAR_INOCUA"], env["PYTHONUTF8"]), ("ok", "1"), "o resto passa; UTF-8 forçado")
        verdade(env["PATH"], "PATH preservado")


# ════════════════════════════════════════════════════════════════════ main.py: as 3 rotas são só do admin (estático)
def test_rotas_so_admin_no_main_py():
    src = (RAIZ / "backend" / "app" / "main.py").read_text(encoding="utf-8")
    arvore = ast.parse(src)
    achadas = {}
    for no in ast.walk(arvore):
        if isinstance(no, ast.FunctionDef):
            for d in no.decorator_list:
                if (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in ("get", "post") and d.args
                        and isinstance(d.args[0], ast.Constant) and str(d.args[0].value).startswith("/api/torre")):
                    achadas[(d.func.attr.upper(), d.args[0].value)] = no
    igual(sorted(achadas), [("GET", "/api/torre"), ("POST", "/api/torre/custodia/planejar"), ("POST", "/api/torre/x/ensaio")], "as três rotas, e só elas")
    for chave, fn in achadas.items():
        corpo = [s for s in fn.body if not (isinstance(s, ast.Expr) and isinstance(getattr(s, "value", None), ast.Constant))]   # sem a docstring
        primeira = corpo[0]
        verdade(isinstance(primeira, ast.Expr) and isinstance(primeira.value, ast.Call) and getattr(primeira.value.func, "id", "") == "_require_admin",
                f"{chave}: a PRIMEIRA instrução tem de ser _require_admin(request)")
        chamadas = [n for n in ast.walk(fn) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "TORRE"]
        verdade(len(chamadas) == 1, f"{chave}: uma só chamada ao módulo torre")
    verdade("from . import torre as TORRE" in src, "import do módulo")


# ════════════════════════════════════════════════════════════════════ HTTP: cliente ASGI mínimo (sem httpx), como test_iald_app_users.py
class Resp:
    def __init__(self, status: int, headers: list, body: bytes):
        self.status = status
        self.headers = [(k.decode("latin-1").lower(), v.decode("latin-1")) for k, v in headers]
        self.body = body

    def h(self, nome: str):
        for k, v in self.headers:
            if k == nome.lower():
                return v
        return None

    def json(self):
        return json.loads(self.body.decode("utf-8"))

    def __repr__(self):
        return f"<{self.status} {self.body[:200]!r}>"


def chamar(app, metodo: str, caminho: str, headers: dict | None = None, corpo: bytes = b"") -> Resp:
    inicio, body = asyncio.run(_chamar_async(app, metodo, caminho, headers, corpo))
    return Resp(inicio.get("status", 0), inicio.get("headers", []), body)


async def _chamar_async(app, metodo, caminho, headers, corpo):
    hs = {"host": "central.iald.ia.br"}
    for k, v in (headers or {}).items():
        if v is not None:
            hs[k.lower()] = v
    if corpo and "content-length" not in hs:
        hs["content-length"] = str(len(corpo))
    scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"}, "http_version": "1.1", "method": metodo, "scheme": "https",
             "path": caminho, "raw_path": caminho.encode(), "query_string": b"", "root_path": "",
             "headers": [(k.encode("latin-1"), v.encode("latin-1")) for k, v in hs.items()],
             "client": ("203.0.113.9", 50000), "server": ("central.iald.ia.br", 443)}
    entregue, fim, inicio, partes = False, asyncio.Event(), {}, []

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


def _token(AUTH, uid: str, role: str, nome: str) -> str:
    agora = int(time.time())
    payload = {"sub": nome, "uid": uid, "role": role, "iat": agora, "exp": agora + 3600, "scheme": "acom-crypto-hilbert-tunnel",
               "jti": secrets.token_hex(8)}
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=")
    return body.decode() + "." + hmac.new(AUTH._server_key(), body, hashlib.sha256).hexdigest()


# ── modo LOCAL (AUTH desligada) ──────────────────────────────────────────────────────────────
def caso_local_get_responde_json_e_nao_cai_no_spa(ctx):
    M, c = ctx["M"], ctx["c"]
    r = chamar(M.app, "GET", "/api/torre")
    igual(r.status, 200, "GET /api/torre")
    verdade("application/json" in (r.h("content-type") or ""), "é JSON, não o index.html da SPA: %r" % r.h("content-type"))
    p = r.json()
    igual(set(p), {"gerado_em", "selo", "quadro", "missoes", "custodias", "vigia", "x", "tuneis", "agentes", "erros"}, "chaves")
    igual(p["selo"]["pin16"], c.pin[:16], "selo")
    sem_caminho_absoluto(r.body.decode("utf-8"), "corpo HTTP")
    igual(c.n("proj"), 4, "4 projeções (cache frio)")


def caso_local_post_planejar(ctx):
    M, c = ctx["M"], ctx["c"]
    c.respostas[("planejar",)] = (1, "PLANO v398\nfalta C1", "")
    c.respostas[("vigiar",)] = (0, json.dumps({"versao": "v398"}), "")
    h = {"content-type": "application/json"}
    r = chamar(M.app, "POST", "/api/torre/custodia/planejar", h, json.dumps({"versao": "v398", "nao_vai": "--publicar", "executar": True}).encode())
    igual(r.status, 200, "planejar com versão")
    igual((r.json()["rc"], r.json()["versao"], r.json()["stdout_cauda"]), (1, "v398", "PLANO v398\nfalta C1"), "corpo")
    r = chamar(M.app, "POST", "/api/torre/custodia/planejar", h, b"{}")
    igual((r.status, r.json()["versao"]), (200, "v398"), "corpo vazio: usa o vigiar")
    r = chamar(M.app, "POST", "/api/torre/custodia/planejar")
    igual((r.status, r.json()["versao"]), (200, "v398"), "sem corpo nenhum: usa o vigiar")
    for ruim in ("v12", "v398 --publicar", "V398", "../x", 398):
        r = chamar(M.app, "POST", "/api/torre/custodia/planejar", h, json.dumps({"versao": ruim}).encode())
        igual(r.status, 400, "versão ruim %r" % (ruim,))
    for ch in c.chamadas:
        junto = " ".join(ch["args"])
        verdade("executar" not in junto and "--publicar" not in junto and "nao_vai" not in junto, "nada do corpo foi para a linha de comando")
    igual(chamar(M.app, "GET", "/api/torre/custodia/planejar").status in (404, 405), True, "GET na rota de ação não existe")


def caso_local_post_ensaio(ctx):
    M, c = ctx["M"], ctx["c"]
    c.respostas[("ensaio",)] = (0, "PENSAMENTO (medida, 200 c): Hoje a IALD mediu. — IALD", "")
    r = chamar(M.app, "POST", "/api/torre/x/ensaio", {"content-type": "application/json"}, json.dumps({"seco": False, "args": ["--gravar"]}).encode())
    igual(r.status, 200, "ensaio")
    igual(r.json(), {"rc": 0, "saida": "PENSAMENTO (medida, 200 c): Hoje a IALD mediu. — IALD"}, "corpo")
    ch = [x for x in c.chamadas if x["args"][-1] == "--seco"][-1]
    igual(ch["args"][1:], ["-X", "utf8", str(T.PENSAMENTO), "--seco"], "a linha de comando não depende do corpo")
    igual(chamar(M.app, "GET", "/api/torre/x/ensaio").status in (404, 405), True, "GET na rota de ação não existe")


def caso_local_rotas_existem_no_app(ctx):
    M = ctx["M"]
    rotas = {(m, r.path) for r in M.app.routes if hasattr(r, "methods") for m in r.methods}
    for par in (("GET", "/api/torre"), ("POST", "/api/torre/custodia/planejar"), ("POST", "/api/torre/x/ensaio")):
        verdade(par in rotas, f"{par} registrada")
    verdade(ctx["AUTH"].AUTH_ENABLED is False, "modo local: AUTH desligada")


CASOS_LOCAL = [caso_local_get_responde_json_e_nao_cai_no_spa, caso_local_post_planejar, caso_local_post_ensaio, caso_local_rotas_existem_no_app]


# ── modo AUTH (CENTRAL_AUTH=crypto, como no Render) ───────────────────────────────────────────
def _h(ctx, quem=None, post=False, sfs="same-origin", origem=ORIGEM):
    h = {}
    if quem:
        h["cookie"] = f"{ctx['AUTH'].COOKIE}={ctx[quem]}"
    if post:
        h.update({"content-type": "application/json", "origin": origem, "sec-fetch-site": sfs})
    return h


def caso_auth_sem_cookie_401(ctx):
    M, c = ctx["M"], ctx["c"]
    igual(chamar(M.app, "GET", "/api/torre", _h(ctx)).status, 401, "GET sem cookie")
    for caminho in ("/api/torre/custodia/planejar", "/api/torre/x/ensaio"):
        igual(chamar(M.app, "POST", caminho, _h(ctx, post=True), b"{}").status, 401, f"POST {caminho} sem cookie")
    igual(c.chamadas, [], "nada rodou")


def caso_auth_viewer_e_editor_403_sem_efeito(ctx):
    M, c = ctx["M"], ctx["c"]
    for quem in ("tok_viewer", "tok_editor"):
        igual(chamar(M.app, "GET", "/api/torre", _h(ctx, quem)).status, 403, f"GET {quem}")
        for caminho in ("/api/torre/custodia/planejar", "/api/torre/x/ensaio"):
            igual(chamar(M.app, "POST", caminho, _h(ctx, quem, post=True), b"{}").status, 403, f"POST {caminho} {quem}")
    igual(c.chamadas, [], "papel sem permissão: NENHUM subprocesso (nem projeção, nem custodiar, nem ensaio)")


def caso_auth_admin_200(ctx):
    M, c = ctx["M"], ctx["c"]
    c.respostas[("planejar",)] = (0, "completo", "")
    c.respostas[("ensaio",)] = (0, "ok", "")
    r = chamar(M.app, "GET", "/api/torre", _h(ctx, "tok_op"))
    igual(r.status, 200, "GET admin")
    igual(r.json()["selo"]["versao"], "v398", "conteúdo")
    sem_caminho_absoluto(r.body.decode("utf-8"), "corpo HTTP")
    r = chamar(M.app, "POST", "/api/torre/custodia/planejar", _h(ctx, "tok_op", post=True), json.dumps({"versao": "v398"}).encode())
    igual((r.status, r.json()["rc"]), (200, 0), "POST planejar admin")
    r = chamar(M.app, "POST", "/api/torre/x/ensaio", _h(ctx, "tok_op", post=True), b"{}")
    igual((r.status, r.json()["rc"]), (200, 0), "POST ensaio admin")
    r = chamar(M.app, "POST", "/api/torre/custodia/planejar", _h(ctx, "tok_op", post=True), json.dumps({"versao": "v1"}).encode())
    igual(r.status, 400, "versão ruim: 400 também para o admin")


def caso_auth_csrf_de_outra_origem_sem_efeito(ctx):
    M, c = ctx["M"], ctx["c"]
    for sfs, origem in (("cross-site", ORIGEM), ("same-origin", "https://evil.example")):
        for caminho in ("/api/torre/custodia/planejar", "/api/torre/x/ensaio"):
            r = chamar(M.app, "POST", caminho, _h(ctx, "tok_op", post=True, sfs=sfs, origem=origem), b"{}")
            igual(r.status, 403, f"CSRF {sfs}/{origem} {caminho}")
    igual(c.chamadas, [], "CSRF: NENHUM subprocesso, nem com o cookie do operador")


CASOS_AUTH = [caso_auth_sem_cookie_401, caso_auth_viewer_e_editor_403_sem_efeito, caso_auth_admin_200, caso_auth_csrf_de_outra_origem_sem_efeito]


def _ambiente_limpo(modo: str, tmp: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CENTRAL_") and k not in ("RENDER", "CF_ACCESS_TEAM_DOMAIN", "CF_ACCESS_AUD")}
    env["CENTRAL_TESTE_TMP"] = tmp
    env["CENTRAL_RATE_MAX"] = "0"
    env["PYTHONIOENCODING"] = "utf-8"
    if modo == "auth":
        env["CENTRAL_AUTH"] = "crypto"
        env["CENTRAL_CRYPTO_SECRET"] = "teste-descartavel-" + secrets.token_urlsafe(24)
    return env


def rodar_modo(modo: str) -> int:
    tmp = Path(os.environ["CENTRAL_TESTE_TMP"])
    from backend.app import authn as AUTH
    from backend.app import main as M
    from backend.app import security as SEC

    SEC._AUDIT_PATH = tmp / "audit.log"           # nada do teste toca backend/data de verdade
    AUTH.USERS_FILE = tmp / "users.json"
    esperado_auth = (modo == "auth")
    if AUTH.AUTH_ENABLED != esperado_auth:
        print(f"FALHA: modo {modo} mas AUTH_ENABLED={AUTH.AUTH_ENABLED}")
        return 1
    ctx = {"M": M, "AUTH": AUTH, "SEC": SEC, "tmp": tmp}
    if esperado_auth:
        ctx["uid_editor"], ctx["uid_viewer"] = "u_" + secrets.token_hex(6), "u_" + secrets.token_hex(6)
        AUTH._save_users([{"uid": ctx["uid_editor"], "name": "editora", "role": "editor", "email": "", "verifier": "x", "created_at": 0},
                          {"uid": ctx["uid_viewer"], "name": "leitor", "role": "viewer", "email": "", "verifier": "x", "created_at": 0}])
        ctx["tok_op"] = _token(AUTH, "operador", "admin", "operador")
        ctx["tok_editor"] = _token(AUTH, ctx["uid_editor"], "editor", "editora")
        ctx["tok_viewer"] = _token(AUTH, ctx["uid_viewer"], "viewer", "leitor")
    casos = CASOS_AUTH if esperado_auth else CASOS_LOCAL
    falhas = 0
    for fn in casos:
        try:
            with cenario() as c:                      # casa sintética + _rodar falso: nenhum filho real
                ctx["c"] = c
                fn(ctx)
            print(f"  ok   [{modo}] {fn.__name__}")
        except Exception:  # noqa: BLE001
            falhas += 1
            print(f"  FALHA [{modo}] {fn.__name__}")
            traceback.print_exc()
    print(f"[{modo}] {len(casos) - falhas}/{len(casos)} passaram")
    return 1 if falhas else 0


def _rodar_subprocesso(modo: str) -> int:
    with tempfile.TemporaryDirectory(prefix=f"central_teste_{modo}_") as tmp:
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--modo", modo], cwd=str(RAIZ), env=_ambiente_limpo(modo, tmp))
        return r.returncode


def test_http_modo_local():
    assert _rodar_subprocesso("local") == 0


def test_http_modo_auth():
    assert _rodar_subprocesso("auth") == 0


# ════════════════════════════════════════════════════════════════════ OPCIONAL: a casa de verdade (só leitura) e o tempo do GET
def real() -> int:
    """`--real`: monta o quadro com a casa REAL (projeções ACOM, iald.py estado, túnel; tudo só leitura), pelo app, e mede o GET frio e o quente."""
    from backend.app import authn as AUTH
    from backend.app import main as M
    from backend.app import security as SEC

    with tempfile.TemporaryDirectory(prefix="central_real_") as tmp:
        SEC._AUDIT_PATH = Path(tmp) / "audit.log"
        if AUTH.AUTH_ENABLED:
            print("FALHA: --real exige AUTH desligada (rode sem CENTRAL_AUTH)")
            return 1
        T._limpar_cache()
        t0 = time.perf_counter()
        r = chamar(M.app, "GET", "/api/torre")
        frio = time.perf_counter() - t0
        t0 = time.perf_counter()
        r2 = chamar(M.app, "GET", "/api/torre")
        quente = time.perf_counter() - t0
        p = r.json()
        print("GET /api/torre: status %d (frio %.2f s, %d bytes) | repetido: status %d (quente %.3f s)" % (r.status, frio, len(r.body), r2.status, quente))
        print("selo:", p["selo"], "| quadro:", (p["quadro"] or {}).get("resumo"), "| vigia:", (p["vigia"] or {}).get("versao"))
        print("missoes: %d (%s)" % (len(p["missoes"]), ", ".join(m["referencia"][:28] + ("!" if "erro" in m else "") for m in p["missoes"])))
        print("custodias:", len(p["custodias"]), "| x.livro:", len(p["x"]["livro"]), "| x.hoje:", bool(p["x"]["hoje"]),
              "| ordens:", [o["ordem"] + (":%d pend" % len(o["pendentes_do_operador"]) if o["pendentes_do_operador"] else "") for o in p["tuneis"]["ordens"]],
              "| codex_threads:", len(p["tuneis"]["codex_threads"]))
        print("erros (%d):" % len(p["erros"]))
        for e in p["erros"]:
            print("   -", e)
        sem_caminho_absoluto(r.body.decode("utf-8"), "corpo real")
        print("nenhum caminho absoluto no corpo real: ok")
        return 0 if r.status == 200 and r2.status == 200 else 1


# ════════════════════════════════════════════════════════════════════ runner
def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "--modo":
        return rodar_modo(sys.argv[2])
    if len(sys.argv) >= 2 and sys.argv[1] == "--real":
        return real()
    casos = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    falhas = 0
    for nome, fn in casos:
        t0 = time.perf_counter()
        try:
            fn()
            print("  ok    %-62s %.2fs" % (nome, time.perf_counter() - t0))
        except Exception:  # noqa: BLE001
            falhas += 1
            print("  FALHA %s" % nome)
            traceback.print_exc()
    print("RESULTADO: %d/%d casos passaram" % (len(casos) - falhas, len(casos)))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())

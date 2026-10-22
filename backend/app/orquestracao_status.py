# -*- coding: utf-8 -*-
"""A ORQUESTRAÇÃO DA IALD (a AGI em construção) lida pela Central — SÓ LEITURA.

A orquestração foi construída pelo Codex em `Chatgpt/IALD_ORQUESTRACAO_20260923/` (pasta do ChatGPT: o Claude só lê).
O painel de controle vivo está na Central IALD nativa (:8082, /admin/agi/orquestracao, autenticação administrativa).
Aqui a Central de Patentes apenas LÊ o que já está gravado, sem importar o pacote do Codex (import tem efeitos:
recupera fila, sonda clientes) e sem abrir o banco para escrita:
  - coordinator.json / transport.json / state/transport_last_check.json  (projeto coordenador e transporte)
  - state/tasks.sqlite3 aberto com `mode=ro`                              (pedidos, execuções, consumo)
  - validation/*.json                                                     (recibos de validação de cada conexão)
A régua: recibo é o estado NA DATA DO RECIBO, não disponibilidade ao vivo — dito na resposta. Falha de leitura é
falha visível. Prompts são texto do operador: a rota exige admin e só devolve os primeiros 240 caracteres.
Nada aqui move gate científico: a orquestração é engenharia (quality_status NOT_BENCHMARKED)."""
from __future__ import annotations

import glob
import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from . import config as C

BASE = C.CENTRAL / "Chatgpt" / "IALD_ORQUESTRACAO_20260923"
PAINEL_LOCAL = "http://127.0.0.1:8082/admin/agi/orquestracao"
PAINEL_REMOTO = "https://demo.iald.ia.br/admin/agi/orquestracao"

# conexão -> (rótulo, padrão do recibo de validação mais recente)
CONEXOES = [
    ("local", "IALD local / Qwen (llama :8081)", None),
    ("codex", "Codex / ChatGPT", "real_runs_*.json"),
    ("claude", "Claude Code", "claude_recheck_*.json"),
    ("gemini", "Google / Antigravity", "antigravity_connection.json"),
    ("kimi", "Kimi Code / K3", "kimi_connection.json"),
    ("mimo", "MiMo API / 2.6 Pro", "mimo_connection.json"),
    ("jev", "Jev / TypeSafe", None),
]


def _j(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def _recibo(padrao: str | None) -> dict:
    if not padrao:
        return {}
    arqs = [a for a in glob.glob(str(BASE / "validation" / padrao)) if ".bak_" not in a]
    if not arqs:
        return {"recibo": None}
    a = max(arqs, key=os.path.getmtime)
    d = _j(Path(a)) or {}
    st = d.get("status")
    if st is None and isinstance(d.get("runs"), list):          # real_runs_*: uma chamada por conexão
        st = "ready" if any((r or {}).get("selected") == "codex" and (r or {}).get("status") == "result_ready"
                            for r in d["runs"]) else "sem chamada codex no recibo"
    return {"recibo": os.path.basename(a), "status_no_recibo": st,
            "verificado_em": d.get("checked_at") or d.get("recorded_at") or d.get("timestamp")
            or datetime.fromtimestamp(os.path.getmtime(a), timezone.utc).isoformat(timespec="seconds")}


def _local_vivo() -> bool | None:
    try:
        with urllib.request.urlopen("http://127.0.0.1:8081/health", timeout=3) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001
        return False


def _uso(txt: str | None) -> dict:
    try:
        u = json.loads(txt or "null") or {}
    except json.JSONDecodeError:
        return {}
    ent = u.get("prompt_tokens") or u.get("input_tokens") or 0
    sai = u.get("completion_tokens") or u.get("output_tokens") or 0
    return {"entrada": ent, "saida": sai}


def get_status() -> dict:
    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if not BASE.exists():
        return {"gerado_utc": agora, "ambiente": "remoto", "disponivel": False,
                "nota": "A orquestração vive na máquina do operador; visível só na Central local (127.0.0.1)."}
    out: dict = {"gerado_utc": agora, "ambiente": "local", "disponivel": True,
                 "painel": {"local": PAINEL_LOCAL, "remoto": PAINEL_REMOTO},
                 "fonte": str(BASE.relative_to(C.CENTRAL)).replace("\\", "/"), "erros": [],
                 "estatuto": "Engenharia [REAL nos recibos]; qualidade NOT_BENCHMARKED; não move gate científico."}
    coord = _j(BASE / "coordinator.json")
    if coord is None:
        out["erros"].append("coordinator.json ilegível")
    else:
        out["coordenador"] = {k: coord.get(k) for k in ("project_label", "project_url", "transport_status",
                                                         "unattended_transport_available", "final_response_roundtrip_validated",
                                                         "uploaded_files_count", "memory_mode_observed", "roles")}
    tr = _j(BASE / "transport.json")
    ult = _j(BASE / "state" / "transport_last_check.json")
    out["transporte"] = {"config": {k: (tr or {}).get(k) for k in ("enabled", "kind", "interval_minutes", "configuration_status", "activated_at")},
                         "ultima_verificacao": ult}
    # conexões: recibo de validação (estado na data do recibo) + ping ao vivo só do local
    cons = []
    for cid, rot, pad in CONEXOES:
        row = {"id": cid, "rotulo": rot, **_recibo(pad)}
        if cid == "local":
            row["vivo_agora"] = _local_vivo()
        if cid == "jev":
            row["status_no_recibo"] = "pendente — cadastros fechados pelo provedor (23/09)"
        cons.append(row)
    out["conexoes"] = cons
    # banco em SÓ-LEITURA
    db = BASE / "state" / "tasks.sqlite3"
    try:
        con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=3)
        con.row_factory = sqlite3.Row
        out["pedidos"] = [{"id": r["id"], "etapa": r["stage"], "criado": r["created_at"], "atualizado": r["updated_at"],
                           "erro": r["error"], "pedido": (r["prompt"] or "")[:240]}
                          for r in con.execute("SELECT id,stage,created_at,updated_at,error,prompt FROM coordination_jobs "
                                               "ORDER BY created_at DESC LIMIT 20")]
        out["execucoes"] = [{"id": r["id"], "status": r["status"], "criado": r["created_at"], "erro": r["error"]}
                            for r in con.execute("SELECT id,status,created_at,error FROM tasks ORDER BY created_at DESC LIMIT 20")]
        tent = []
        for r in con.execute("SELECT provider,started_at,finished_at,status,usage FROM attempts ORDER BY started_at DESC LIMIT 50"):
            tent.append({"conexao": r["provider"], "inicio": r["started_at"], "fim": r["finished_at"], "status": r["status"], **_uso(r["usage"])})
        out["tentativas"] = tent
        out["consumo_total"] = {"entrada": sum(t.get("entrada", 0) for t in tent), "saida": sum(t.get("saida", 0) for t in tent),
                                "nota": "tokens informados pelos provedores nas execuções gravadas; o coordenador Codex/ChatGPT Work não entra nesta conta"}
        out["eventos"] = [dict(r) for r in con.execute("SELECT job_id,at,action,from_stage,to_stage FROM coordination_events ORDER BY at DESC LIMIT 30")]
        con.close()
    except Exception as e:  # noqa: BLE001
        out["erros"].append(f"banco da orquestração ilegível: {str(e)[:160]}")
    out["recibos_principais"] = [os.path.basename(a) for a in sorted(glob.glob(str(BASE / "validation" / "*.json")), key=os.path.getmtime, reverse=True)
                                 if ".bak_" not in a][:12]
    return out

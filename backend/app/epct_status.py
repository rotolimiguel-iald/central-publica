# -*- coding: utf-8 -*-
"""ANEXO ePCT — conferência do protocolo internacional dos 15 dispositivos.

Fonte de verdade no filesystem (DATA_MODEL §0):
  EPCT/<ID>/00_DOSSIE.json  — fatos extraídos do depósito INPI (data de prioridade!)
  EPCT/epct_status.json     — os tiques de conferência do operador (este módulo escreve SÓ aqui)

A régua: prazo é [LEGAL] — o painel mostra e alerta, mas a conferência final de prazo
é do operador com o agente da propriedade industrial. Falha de leitura é falha visível.
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from . import config as C

EPCT_DIR = C.CENTRAL / "EPCT"
STATUS_FILE = EPCT_DIR / "epct_status.json"
PRAZOS_FILE = EPCT_DIR / "prazos_efetivos.json"


def _load_prazos() -> dict:
    """Prazos fatais EFETIVOS (auditoria do campo 66 dos comprovantes INPI) — sobrepõem
    o priority_deadline do dossiê quando a prioridade interna encurta o prazo."""
    if PRAZOS_FILE.is_file():
        try:
            data = json.loads(PRAZOS_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}
    return {}

# As 7 etapas do protocolo de UM dispositivo, na ordem do 06_CHECKLIST_PROTOCOLO.md.
STEPS: list[tuple[str, str]] = [
    ("pacote_conferido", "Pacote conferido (4 documentos separados; desenhos SÓ figuras)"),
    ("request_preenchido", "Request preenchido no ePCT (dados do 05_DADOS_DO_REQUERIMENTO)"),
    ("documentos_anexados", "Documentos anexados nos campos próprios (desenhos SÓ no campo de desenhos)"),
    ("prioridade_reivindicada", "Prioridade BR reivindicada (nº + data; doc. de prioridade/DAS)"),
    ("taxas_pagas", "Taxas pagas (GRUs: transmissão + internacional + pesquisa ISA/BR)"),
    ("transmitido", "Pedido transmitido (número PCT recebido)"),
    ("recibo_arquivado", "Recibo salvo em EPCT/<ID>/RECIBOS/ e nº PCT anotado"),
]
_STEP_KEYS = {k for k, _ in STEPS}
_EXTRA_KEYS = {"pct_number", "protocol_date", "nota"}


def _load_status() -> dict:
    if STATUS_FILE.is_file():
        try:
            data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def _save_status(data: dict) -> None:
    EPCT_DIR.mkdir(exist_ok=True)
    tmp = STATUS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(STATUS_FILE)


def _load_dossie(d: Path) -> dict:
    f = d / "00_DOSSIE.json"
    if not f.is_file():
        return {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _days_left(deadline: str | None) -> int | None:
    if not deadline:
        return None
    try:
        dl = datetime.strptime(deadline[:10], "%Y-%m-%d").date()
    except ValueError:
        return None
    return (dl - date.today()).days


def get_overview() -> dict:
    """Estado completo da conferência: dossiês + tiques + prazos, por dispositivo."""
    status = _load_status()
    prazos = _load_prazos()
    devices = []
    if EPCT_DIR.is_dir():
        for d in sorted(EPCT_DIR.iterdir()):
            if not d.is_dir() or not d.name.startswith("BR"):
                continue
            dossie = _load_dossie(d)
            ticks = status.get(d.name, {})
            steps = [{"key": k, "label": lbl, "done": bool(ticks.get(k))} for k, lbl in STEPS]
            n_done = sum(1 for s in steps if s["done"])
            files = sorted(p.name for p in d.iterdir() if p.is_file())
            override = prazos.get(d.name) if isinstance(prazos.get(d.name), dict) else None
            deadline = (override or {}).get("prazo_efetivo") or dossie.get("priority_deadline")
            devices.append({
                "id": d.name,
                "title": dossie.get("official_title") or d.name,
                "br_number": dossie.get("br_number"),
                "filing_date": dossie.get("filing_date"),
                "priority_deadline": deadline,
                "prazo_motivo": (override or {}).get("motivo"),
                "days_left": _days_left(deadline),
                "steps": steps,
                "n_done": n_done,
                "n_steps": len(STEPS),
                "concluido": n_done == len(STEPS),
                "pct_number": ticks.get("pct_number"),
                "protocol_date": ticks.get("protocol_date"),
                "nota": ticks.get("nota"),
                "package_files": files,
                "dossie_ok": bool(dossie),
            })
    total = len(devices)
    done = sum(1 for x in devices if x["concluido"])
    urgentes = [x["id"] for x in devices
                if x["days_left"] is not None and x["days_left"] <= 60 and not x["concluido"]]
    return {
        "gerado_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total": total,
        "concluidos": done,
        "urgentes": urgentes,
        "steps_legenda": [{"key": k, "label": lbl} for k, lbl in STEPS],
        "devices": devices,
        "aviso_legal": "Prazo é [LEGAL]: o painel alerta, mas a conferência final é do operador "
                       "com o agente da propriedade industrial.",
    }


def set_tick(device_id: str, step: str, value, extra: dict | None = None) -> dict:
    """Marca/desmarca um tique (ou grava pct_number/protocol_date/nota). Escrita atômica."""
    if not (EPCT_DIR / device_id).is_dir():
        raise ValueError(f"dispositivo desconhecido: {device_id}")
    if step not in _STEP_KEYS and step not in _EXTRA_KEYS:
        raise ValueError(f"etapa desconhecida: {step}")
    status = _load_status()
    dev = status.setdefault(device_id, {})
    if step in _STEP_KEYS:
        dev[step] = bool(value)
        dev[step + "_em"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") if value else None
    else:
        dev[step] = (str(value).strip() or None) if value is not None else None
    for k, v in (extra or {}).items():
        if k in _EXTRA_KEYS:
            dev[k] = (str(v).strip() or None) if v is not None else None
    _save_status(status)
    return get_overview()

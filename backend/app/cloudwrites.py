# -*- coding: utf-8 -*-
"""Persistência de escrita na NUVEM — dual-write + reidratação + colheita (Evolução v2, Eixo 2).

O problema (limitação honesta documentada no deploy): na nuvem (Render) o filesystem do
contêiner é EFÊMERO — as escritas write-through nos .md (notas/instruções/prompts
compilados) somem num redeploy, porque os .md voltam do repositório. Só o disco
persistente (backend/data) sobrevive.

A solução (fonte da verdade continua sendo os ARQUIVOS):
  1. DUAL-WRITE — com CENTRAL_CLOUD_WRITES=1 (ou RENDER=true, que o Render seta sozinho),
     cada escrita de conteúdo é TAMBÉM registrada em backend/data/cloud_writes/writes.jsonl
     (disco persistente), com id estável, timestamp UTC e usuário autenticado.
  2. REIDRATAÇÃO — no boot, ANTES da indexação, rehydrate() re-aplica os registros
     pendentes aos .md do contêiner (idempotente: registro já presente não duplica).
  3. COLHEITA — tools/harvest_cloud.py (roda na máquina do operador) autentica na nuvem,
     baixa os registros pendentes, inscreve nos .md LOCAIS (com backup .bak), reindexa e
     opcionalmente reconhece (ack) os registros — que saem do overlay da nuvem. Depois do
     commit+push, o próprio repositório passa a carregar o conteúdo.

Papéis: exportar/ack são SÓ ADMIN (regra central em authn.can_request + guarda local).
Nada aqui toca originais (Patentes/), vault/ ou memória de classe — apenas os alvos que
os endpoints de escrita já tocavam: patents/<dir>/notes/initial_notes.md e
compiled_prompts/*_CLAUDE_CODE_TASK.md.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from . import config as C

DIR = C.DATA_DIR / "cloud_writes"
PENDING = DIR / "writes.jsonl"
ACKED = DIR / "writes_acked.jsonl"

# serializa record()/ack()/rehydrate() sobre o writes.jsonl (append vs rewrite) — sem lock,
# um ack() concorrente (write_text = truncar+reescrever) pode clobberar um record() (append).
_LOCK = threading.Lock()

# teto do arquivo de pendentes (anti disk-fill; os payloads já têm teto por request)
MAX_PENDING_BYTES = 16 * 1024 * 1024

KINDS = ("note_add", "note_toggle", "compiled")


def enabled() -> bool:
    """Dual-write ligado explicitamente (CENTRAL_CLOUD_WRITES=1) ou implicitamente na
    nuvem (Render seta RENDER=true). Local segue puro write-through (comportamento v1)."""
    if os.environ.get("CENTRAL_CLOUD_WRITES", "").strip() == "1":
        return True
    return os.environ.get("RENDER", "").strip().lower() == "true"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _rec_id(kind: str, payload: dict, ts: str) -> str:
    blob = json.dumps({"k": kind, "p": payload, "t": ts}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def _atomic_write(p: Path, text: str) -> None:
    """Escreve p atomicamente (tmp no mesmo diretório + os.replace) — nunca deixa o
    writes.jsonl truncado se o processo morrer no meio, e é ponto único de troca."""
    tmp = p.with_name(p.name + f".tmp{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def record(kind: str, payload: dict, user: str) -> dict | None:
    """Registra uma escrita no overlay persistente. Nunca levanta para o caller
    (a escrita primária no .md já aconteceu; o overlay é resiliência, não gate)."""
    if not enabled() or kind not in KINDS:
        return None
    try:
        with _LOCK:
            DIR.mkdir(parents=True, exist_ok=True)
            if PENDING.exists() and PENDING.stat().st_size > MAX_PENDING_BYTES:
                return None  # teto atingido: não degrada o serviço; colheita esvazia
            ts = _now()
            rec = {"id": _rec_id(kind, payload, ts), "ts_utc": ts, "kind": kind,
                   "user": user, "payload": payload}
            with open(PENDING, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            return rec
    except OSError:
        return None


def _read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    out = []
    # errors="replace": um byte não-UTF-8 (append truncado/cp1252) vira U+FFFD e a linha
    # cai no JSONDecodeError já tratado — jamais derruba rehydrate/reindex inteiros.
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue  # linha corrompida não derruba o overlay
    return out


def pending_records() -> list[dict]:
    return _read_jsonl(PENDING)


def ack(ids: list[str]) -> dict:
    """Move registros reconhecidos (já colhidos/commitados) de pendentes p/ acked.
    Sob _LOCK + escrita atômica: um record() concorrente não é clobberado."""
    ids_set = set(ids)
    with _LOCK:
        recs = pending_records()
        keep, moved = [], []
        for r in recs:
            (moved if r.get("id") in ids_set else keep).append(r)
        DIR.mkdir(parents=True, exist_ok=True)
        if moved:
            with open(ACKED, "a", encoding="utf-8") as f:
                for r in moved:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        _atomic_write(PENDING, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep))
    return {"acked": len(moved), "remaining": len(keep)}


# ────────────────────────── aplicação de registros (idempotente) ──────────────────────────
_ACTIVE_RE = re.compile(r"\(active\s*=\s*(true|false)\)", re.I)


def _line_key(line: str) -> str:
    """Chave estável de uma linha de nota: sem flag active, sem checkbox, espaços colapsados.
    Sobrevive ao toggle (que só muda a flag) — é como um toggle re-encontra sua linha."""
    s = _ACTIVE_RE.sub("", line)
    s = re.sub(r"^\s*-\s*\[[ xX]\]\s*", "", s.strip())
    return re.sub(r"\s+", " ", s).strip()


def _safe_segment(name: str) -> bool:
    """Um único segmento de caminho seguro: sem separadores, sem '..', sem drive/absoluto.
    (harvest_cloud roda na estação do operador; um registro forjado JAMAIS pode escrever fora.)"""
    return bool(name) and Path(name).name == name and name not in ("..", ".")


def _confined(central: Path, target: Path, *roots: str) -> bool:
    """target resolvido deve estar sob um dos roots permitidos DENTRO da Central."""
    try:
        t = target.resolve()
    except OSError:
        return False
    for root in roots:
        base = (central / root).resolve()
        if t == base or base in t.parents:
            return True
    return False


def apply_note_add(central: Path, payload: dict) -> str:
    """Re-aplica um note_add ao .md (mesma lógica do endpoint /api/notes).
    Idempotente: se a linha (por chave) NA MESMA SEÇÃO já existe, não duplica."""
    dir_name = payload["dir_name"]
    section = payload["section"]
    text = payload["text"].strip()
    flag = "true" if payload.get("active", True) else "false"
    if not _safe_segment(dir_name):                       # confinamento (path traversal)
        return "dir_invalido"
    md = central / "patents" / dir_name / "notes" / "initial_notes.md"
    if not _confined(central, md, "patents"):
        return "fora_da_central"
    new_item = f"- [ ] (active={flag}) {text}\n"
    existing = md.read_text(encoding="utf-8", errors="replace") if md.exists() else ""
    key = _line_key(new_item)
    # dedup POR SEÇÃO (mesmo texto em seções diferentes não colide)
    lines = existing.splitlines(keepends=True)
    cur_sec, out, inserted = None, [], False
    for ln in lines:
        sec_m = re.match(r"##\s+(.*?)\s*$", ln.strip())
        if sec_m:
            cur_sec = sec_m.group(1)
        if cur_sec == section and _line_key(ln) == key:
            return "ja_presente"
    for ln in lines:
        out.append(ln)
        if not inserted and re.match(rf"##\s+{re.escape(section)}\s*$", ln.strip()):
            out.append(new_item)
            inserted = True
    if not inserted:
        out.append(f"\n## {section}\n{new_item}")
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text("".join(out), encoding="utf-8")
    return "aplicado"


def apply_note_toggle(central: Path, payload: dict) -> str:
    """Re-aplica um toggle pela CHAVE da linha (o id numérico do DB não é estável entre
    deploys — a chave textual é). Idempotente: flag já igual → 'ja_presente'. Restringe a
    busca à SEÇÃO gravada quando presente (evita togglar linha homônima de outra seção)."""
    source_file = str(payload.get("source_file", ""))
    src = central / source_file
    # confinamento: o alvo tem de cair sob patents/ (onde vivem os initial_notes.md)
    if ".." in source_file.replace("\\", "/").split("/") or not _confined(central, src, "patents"):
        return "fora_da_central"
    if not src.exists():
        return "arquivo_ausente"
    key = payload["line_key"]
    want_sec = payload.get("source_section")   # opcional (registros novos gravam; antigos não)
    new_flag = "true" if payload["active"] else "false"
    lines = src.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    cur_sec = None
    for i, ln in enumerate(lines):
        sec_m = re.match(r"##\s+(.*?)\s*$", ln.strip())
        if sec_m:
            cur_sec = sec_m.group(1)
        if want_sec is not None and cur_sec != want_sec:
            continue
        if _line_key(ln) == key:
            m = _ACTIVE_RE.search(ln)
            if m and m.group(1).lower() == new_flag:
                return "ja_presente"
            if m:
                lines[i] = _ACTIVE_RE.sub(f"(active={new_flag})", ln)
            else:
                lines[i] = re.sub(r"(-\s*\[[ xX]\]\s*)", rf"\1(active={new_flag}) ", ln, count=1)
            src.write_text("".join(lines), encoding="utf-8")
            return "aplicado"
    return "linha_nao_encontrada"


def apply_compiled(central: Path, payload: dict) -> str:
    """Re-materializa um prompt compilado. Nome confinado (basename + sufixo canônico)."""
    filename = str(payload.get("filename", ""))
    if not _safe_segment(filename) or not filename.endswith("_CLAUDE_CODE_TASK.md"):
        return "nome_invalido"
    dst = central / "compiled_prompts" / filename
    if not _confined(central, dst, "compiled_prompts"):
        return "fora_da_central"
    if dst.exists():
        return "ja_presente"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(payload["body"], encoding="utf-8")
    return "aplicado"


line_key = _line_key   # API pública p/ o main.py registrar toggles pela chave da linha

APPLIERS = {"note_add": apply_note_add, "note_toggle": apply_note_toggle,
            "compiled": apply_compiled}


def apply_records(central: Path, records: list[dict]) -> dict:
    """Aplica registros em ordem cronológica (adds antes de toggles do mesmo instante).
    Retorna o resumo por status — negativos honestos incluídos (linha_nao_encontrada etc.)."""
    order = {"note_add": 0, "compiled": 1, "note_toggle": 2}
    recs = sorted(records, key=lambda r: (r.get("ts_utc", ""), order.get(r.get("kind"), 9)))
    summary: dict[str, list[str]] = {}
    for r in recs:
        fn = APPLIERS.get(r.get("kind"))
        if fn is None:
            summary.setdefault("kind_desconhecido", []).append(r.get("id", "?"))
            continue
        try:
            status = fn(central, r.get("payload") or {})
        except (OSError, KeyError, TypeError, ValueError, UnicodeDecodeError) as e:
            status = f"erro:{type(e).__name__}"
        summary.setdefault(status, []).append(r.get("id", "?"))
    return {k: {"n": len(v), "ids": v} for k, v in summary.items()}


def rehydrate() -> dict | None:
    """Chamada no reindex (ANTES da indexação): re-aplica o overlay pendente aos .md do
    contêiner. Só age com o dual-write ligado; local puro é no-op."""
    if not enabled():
        return None
    recs = pending_records()
    if not recs:
        return {"pending": 0}
    out = apply_records(C.CENTRAL, recs)
    out["pending"] = len(recs)
    return out

# -*- coding: utf-8 -*-
"""reindex — rebuild the SQLite index from the filesystem (the source of truth).

Order + rules per DATA_MODEL §5/§7. Step A proves the Patentes\\ originals are
intact before anything is written; a mismatch aborts (never corrects, never writes).
Idempotent: a global signature of all source hashes skips the rebuild when nothing
changed (reindex; reindex -> 2nd is 'unchanged').
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

from . import config as C
from .db import connect, ensure_schema


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _iso(br_or_iso: str | None) -> str | None:
    if not br_or_iso:
        return None
    s = str(br_or_iso).strip()
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    return s  # already ISO or a note like "N/A ..."


# ---------- integrity (Step A) -------------------------------------------------
def check_integrity() -> dict:
    baseline = json.loads(C.ORIGINAL_HASHES.read_text(encoding="utf-8"))["hashes"]
    # normaliza separador Windows(\\)→POSIX(/) para resolver em Linux (nuvem) e Windows
    baseline = {k: v for k, v in baseline.items()
                if k.replace("\\", "/").startswith("Patentes/")}
    violations = []
    for rel, expected in baseline.items():
        p = C.CENTRAL / rel.replace("\\", "/")
        if not p.exists():
            violations.append({"rel": rel, "problem": "MISSING"})
            continue
        actual = _sha256_file(p)
        if actual != expected:
            violations.append({"rel": rel, "problem": "CHANGED",
                               "expected": expected, "actual": actual})
    return {"status": "OK" if not violations else "VIOLATION",
            "checked": len(baseline), "violations": violations}


# ---------- global signature (idempotency) ------------------------------------
def _source_files() -> list[Path]:
    fs = [C.MASTER_INDEX, C.PENDENCIAS, C.ORIGINAL_HASHES, C.DISCOVERED, C.EXTRACTION]
    fs += sorted(C.CLASSES_DIR.glob("*.md"))
    fs += sorted(C.PATENTS_MD_DIR.glob("*.md"))
    for d in sorted(C.PATENTS_DIR.iterdir()) if C.PATENTS_DIR.exists() else []:
        if d.is_dir():
            fs += [p for p in [d / "docket.yaml"] if p.exists()]
            fs += sorted((d / "notes").glob("*.md")) if (d / "notes").exists() else []
            fs += sorted((d / "seals").rglob("*.json")) if (d / "seals").exists() else []
            dr = d / "renders" / "drawings"
            fs += sorted(dr.glob("prancha_*.png")) if dr.exists() else []
    fs += sorted(C.COMPILED_PROMPTS.glob("*.md")) if C.COMPILED_PROMPTS.exists() else []
    return [p for p in fs if p.exists()]


def _global_signature() -> tuple[str, dict]:
    per = {}
    for p in _source_files():
        per[str(p.relative_to(C.CENTRAL))] = _sha256_file(p)
    sig = _sha_text("\n".join(f"{k}={v}" for k, v in sorted(per.items())))
    return sig, per


# ---------- parsers ------------------------------------------------------------
def parse_class(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    # ordinal is reliable from the filename stem (CLASS_06_ENERGIA -> 6)
    sm = re.match(r"CLASS_(\d+)_", md_path.stem)
    ordinal = int(sm.group(1)) if sm else 0
    nm = re.match(r"#\s*CLASS_\d+[_\s][^—\-·]*[—\-·]\s*(.+)", first)
    name = nm.group(1).strip() if nm else md_path.stem.split("_", 2)[-1].title()
    markers = sorted(set(re.findall(r"\[(?:REAL|SIM|CONJ|PILOTO|ENERGY|MEDICAL|"
                                    r"HARDWARE|DEFENSE|LEGAL|OPEN|DATA|DER|DATA_REQUIRED)\]",
                                    text[:1500])))
    lock = ""
    lm = re.search(r"TRAVA[^:]*:\s*(.+)", text)
    if lm:
        lock = lm.group(1).strip()[:400]
    return {"id": md_path.stem, "ordinal": ordinal, "name": name,
            "slug": md_path.stem.split("_", 2)[-1].lower(),
            "markers": markers, "lock_note": lock,
            "memory_md_path": f"memory/classes/{md_path.name}"}


def parse_claims(md_text: str) -> tuple[int | None, int | None, int | None]:
    total = indep = figs = None
    # anchor on the "Reivindicações principais" section to avoid stray "Total 5.550"
    sec = re.search(r"##[^\n]*[Rr]eivindica[çc][õo]es principais(.*?)(?:\n##|\Z)",
                    md_text, re.S)
    scope = sec.group(1) if sec else md_text
    m = (re.search(r"total[:\s]*(\d+)", scope, re.I)
         or re.search(r"(\d+)\s+no total", scope, re.I)
         or re.search(r"(\d+)\s+reivindica", scope, re.I))
    if m:
        total = int(m.group(1))
    m = re.search(r"(\d+)\s+independente", scope, re.I)
    if m:
        indep = int(m.group(1))
    m = re.search(r"Figuras?\s*1[\s–—-]+(\d+)", md_text)
    if m:
        figs = int(m.group(1))
    return total, indep, figs


# Curated device display names (the NAME leads on the dashboard; the process number
# is internal info). Not a slug transform — the number corrects the phrase.
DISPLAY_NAMES = {
    "ACOM": "ACOM", "ACOM_MIRROR": "ACOM Mirror", "ACOM_CRYPTO": "ACOM Crypto",
    "TGL_TENSOR": "TGL Tensor", "IALD": "IALD",
    "SUPERCONDUTOR": "Supercondutor Holográfico", "MOTOR_DOBRA": "Motor de Dobra",
    "PSI_NET": "Ψ-NET", "FUSAO_FRIO": "Fusão a Frio", "MQC": "MQC",
    "DIPOLO_TRANSISTOR": "Dípolo Transistor", "CELULA_REVERSAO": "Célula de Reversão",
    "SKYGRID": "SkyGrid", "APRENDIZADO_CONTINUO": "Aprendizado Contínuo",
    "ONCOLOGIA": "Oncologia", "KERNEL_ONTOLOGICO": "Kernel Ontológico",
}


def display_name(slug: str) -> str:
    return DISPLAY_NAMES.get(slug, slug.replace("_", " ").title())


def load_master_index() -> list[dict]:
    data = yaml.safe_load(C.MASTER_INDEX.read_text(encoding="utf-8"))
    return data.get("patentes", [])


def parse_docket(yaml_path: Path) -> dict:
    d = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    epct = d.get("epct", {}) or {}
    fees = d.get("fees", {}) or {}
    gru = fees.get("gru", {}) or {}
    pix = fees.get("pix", {}) or {}
    return {
        "status": d.get("status"), "alert_level": d.get("alert_level"),
        "epct_status": epct.get("status"), "epct_number": epct.get("numero"),
        "epct_date": _iso(epct.get("data")),
        "janela_paris_12m": _iso(d.get("janela_paris_12m")),
        "janela_paris_alvo": _iso(d.get("janela_paris_alvo_precaucional")),
        "fase_nacional_30m": _iso(d.get("fase_nacional_30m")),
        "gru_arquivo": gru.get("arquivo"), "gru_servico": gru.get("servico"),
        "gru_valor": gru.get("valor"), "gru_vencimento": _iso(gru.get("vencimento")),
        "pix_arquivo": pix.get("arquivo"), "pix_data": _iso(pix.get("data")),
        "pix_valor": pix.get("valor"), "annuities_note": d.get("annuities"),
        "office_actions": json.dumps(d.get("office_actions", []), ensure_ascii=False),
        "reminders": json.dumps(d.get("reminders", []), ensure_ascii=False),
        "aviso": d.get("aviso") or C.AVISO_LEGAL,
        "_raw": d,
    }


SECTION_TIPO = {
    "notas livres": "nota", "sugestões de melhoria": "sugestao",
    "sugestoes de melhoria": "sugestao", "instruções próxima etapa": "instrucao",
    "instrucoes proxima etapa": "instrucao", "tarefas": "tarefa",
    "bloqueios": "bloqueio", "perguntas ao claude code": "pergunta",
}


def parse_notes(md_path: Path) -> list[dict]:
    out, tipo, section = [], None, None
    for i, raw in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
        hm = re.match(r"##\s+(.*)", raw)
        if hm:
            section = hm.group(1).strip()
            tipo = SECTION_TIPO.get(section.lower())
            continue
        if not tipo:
            continue
        im = re.match(r"\s*-\s*\[( |x|X)\]\s*(.*)", raw)
        if not im:
            continue
        done = 1 if im.group(1).lower() == "x" else 0
        rest = im.group(2)
        am = re.match(r"\(active\s*=\s*(true|false)\)\s*(.*)", rest, re.I)
        active = 1 if (am and am.group(1).lower() == "true") else 0
        text = (am.group(2) if am else rest).strip()
        if text.lower().startswith("exemplo:"):
            active = 0  # placeholder — never in the compiler
        markers = re.findall(r"\[[A-Z_]+\]", text)
        out.append({"tipo": tipo, "active": active, "done": done, "text": text,
                    "markers": json.dumps(markers, ensure_ascii=False),
                    "source_file": str(md_path.relative_to(C.CENTRAL)).replace("\\", "/"),
                    "source_section": section, "line_ref": i,
                    "content_hash": _sha_text(raw)})
    return out


def classify_doc_role(name: str) -> str:
    n = name.lower()
    for key, role in [("relat", "relatorio"), ("reivindica", "reivindicacoes"),
                      ("reinvindica", "reivindicacoes"), ("desenho", "desenhos"),
                      ("resumo", "resumo"), ("gru", "gru"), ("pix", "pix"),
                      ("epct", "epct"), ("cnpj", "cnpj")]:
        if key in n:
            return role
    if n.endswith(".zip"):
        return "zip"
    if "870" in name and n.endswith(".pdf"):
        return "recibo_inpi"
    return "peca_consolidada" if n.endswith(".pdf") else "outro"


def load_documents() -> list[dict]:
    hashes = json.loads(C.ORIGINAL_HASHES.read_text(encoding="utf-8"))["hashes"]
    disc = {f["path"]: f for f in json.loads(
        C.DISCOVERED.read_text(encoding="utf-8"))["files"]}
    extr = json.loads(C.EXTRACTION.read_text(encoding="utf-8"))["pdfs"]
    docs = []
    for rel, sha in hashes.items():
        if not rel.startswith("Patentes\\"):
            continue
        meta = disc.get(rel, {})
        ex = extr.get(rel, {})
        name = rel.rsplit("\\", 1)[-1]
        docs.append({
            "rel_path": rel, "sha256": sha, "size_bytes": meta.get("size"),
            "mtime": meta.get("mtime"), "ext": meta.get("ext"),
            "doc_role": classify_doc_role(name), "pages": ex.get("pages"),
            "chars": ex.get("chars"), "extract_ok": 1 if ex.get("ok") else 0,
            "extract_error": ex.get("error"), "is_original": 1,
            "name": name,
        })
    return docs


def parse_pendencias() -> list[dict]:
    text = C.PENDENCIAS.read_text(encoding="utf-8")
    lines = text.splitlines()
    items, cur = [], None
    for i, raw in enumerate(lines, 1):
        hm = re.match(r"##\s+(P-\d+)\s*(\[[^\]]*\])?\s*(?:\[[^\]]*\])?\s*[—-]?\s*(.*)", raw)
        if hm:
            if cur:
                items.append(cur)
            status = "ABERTA"
            sm = re.search(r"\[(ABERTA|RESPONDIDA|REFORMULADA|DECIDIDA|FECHADA)",
                           hm.group(2) or "")
            if sm:
                status = sm.group(1)
            rd = re.search(r"(\d{2}/\d{2}/\d{4})", hm.group(2) or "")
            cur = {"id": hm.group(1), "title": hm.group(3).strip()[:300],
                   "status": status, "body_lines": [],
                   "resolved_date": _iso(rd.group(1)) if rd else None,
                   "line_ref": i, "patents": set()}
        elif cur is not None:
            cur["body_lines"].append(raw)
            for pn in re.findall(r"BR\s?10\s?20\d{2}\s?\d{6}[\s-]?\d", raw):
                cur["patents"].add(re.sub(r"\s", "", pn)[:13] + "-" + re.sub(r"\s", "", pn)[13:])
    if cur:
        items.append(cur)
    for it in items:
        body = "\n".join(it.pop("body_lines")).strip()
        it["body"] = body
        it["markers"] = json.dumps(sorted(set(re.findall(r"\[[A-Z_]+\]", body))),
                                   ensure_ascii=False)
        # normalize patent refs to canonical BRxxxxxxxxxxxx-x seen in the index
        it["patents"] = sorted(it["patents"])
    return items


def load_seals(patent_dir: Path) -> list[dict]:
    runs = []
    seals_dir = patent_dir / "seals"
    if not seals_dir.exists():
        return runs
    for seal in sorted(seals_dir.rglob("seal.json")):
        try:
            s = json.loads(seal.read_text(encoding="utf-8"))
        except Exception:
            continue
        runs.append(s)
    return runs


# ---------- deadline derivation (DATA_MODEL §5.6) ------------------------------
def derive_deadlines(patent_id: str, dk: dict) -> list[dict]:
    out = []
    status = dk.get("epct_status")
    if status == "VIVO_DEPOSITADO_E_PAGO":
        out.append({"patent_id": patent_id, "kind": "paris_12m",
                    "label": "Convenção de Paris 12m (cumprida — ePCT depositado)",
                    "due_date": None, "status": "cumprido",
                    "basis": "ePCT vivo", "source_field": "epct.status",
                    "legal_note": None})
        fn = dk.get("fase_nacional_30m")
        if fn and fn.startswith("20"):
            out.append({"patent_id": patent_id, "kind": "national_phase_30m",
                        "label": f"Fase nacional 30m ({dk.get('epct_number') or 'PCT'})",
                        "due_date": fn, "status": "pendente",
                        "basis": "prioridade + 30m", "source_field": "fase_nacional_30m",
                        "legal_note": "[LEGAL] Conferir prazo por país de designação."})
    else:  # SOMENTE_INPI / A_DEPOSITAR
        due = dk.get("janela_paris_12m")
        alvo = dk.get("janela_paris_alvo")
        if due and due.startswith("20"):
            out.append({"patent_id": patent_id, "kind": "paris_12m",
                        "label": "Janela de Paris — depósito do NOVO ePCT (FATAL)",
                        "due_date": due, "status": "pendente",
                        "basis": "prioridade interna ao ACOM 05/12/2025 + 12m (decisão do operador)",
                        "source_field": "janela_paris_12m",
                        "legal_note": "[LEGAL] Próximo passo: novo processo originário, "
                                      "sem vínculo com a tentativa preclusa. Consultar agente."})
        if alvo and alvo.startswith("20"):
            out.append({"patent_id": patent_id, "kind": "custom",
                        "label": "Alvo precaucional do novo ePCT (último dia de novembro)",
                        "due_date": alvo, "status": "pendente",
                        "basis": "precaução do operador (30/11/2026)",
                        "source_field": "janela_paris_alvo_precaucional",
                        "legal_note": "[LEGAL] Alvo de trabalho, antes do prazo fatal."})
        out.append({"patent_id": patent_id, "kind": "national_phase_30m",
                    "label": "Fase nacional 30m", "due_date": None, "status": "na",
                    "basis": "não-ACOM: sem PCT vivo", "source_field": "fase_nacional_30m",
                    "legal_note": None})
    if dk.get("gru_vencimento"):
        paid = 1 if dk.get("pix_data") else 0
        out.append({"patent_id": patent_id, "kind": "gru_payment",
                    "label": "GRU (taxa de depósito)", "due_date": dk["gru_vencimento"],
                    "status": "cumprido" if paid else "pendente",
                    "basis": "GRU do depósito", "source_field": "fees.gru.vencimento",
                    "legal_note": None})
    return out


# ---------- main reindex -------------------------------------------------------
def reindex(force: bool = False) -> dict:
    conn = connect()
    rebuilt = ensure_schema(conn)
    started = _now()

    integ = check_integrity()
    if integ["status"] == "VIOLATION":
        conn.execute("INSERT OR REPLACE INTO index_meta(key,value) VALUES('originals_integrity','VIOLATION')")
        conn.commit()
        # LOCAL: aborta (anti-adulteração). NUVEM (imagem imutável): CENTRAL_REINDEX_NO_ABORT=1
        # registra a violação mas CONSTRÓI o índice mesmo assim (senão a Central sobe sem dados).
        if not os.environ.get("CENTRAL_REINDEX_NO_ABORT"):
            return {"integrity": integ, "aborted": True,
                    "message": "Originais alterados — reindex abortado (etapa A). Nada foi escrito."}

    # NUVEM: reidrata o overlay persistente (escritas feitas no ar que o redeploy apagou
    # dos .md efêmeros) ANTES de computar a assinatura/indexar — idempotente; local é no-op.
    # Blindado: uma falha na reidratação JAMAIS aborta o reindex (o índice ainda constrói).
    from . import cloudwrites as CW
    try:
        rehydrated = CW.rehydrate()
    except Exception as e:            # noqa: BLE001 — resiliência do boot acima de tudo
        rehydrated = {"error": f"{type(e).__name__}: {e}"[:200]}

    sig, per = _global_signature()
    prev = conn.execute("SELECT value FROM index_meta WHERE key='global_signature'").fetchone()
    if not force and not rebuilt and prev and prev[0] == sig:
        n_pat = conn.execute("SELECT count(*) FROM patent").fetchone()[0]
        if n_pat:
            return {"integrity": integ, "mode": "unchanged", "patents": n_pat,
                    "message": "Nada mudou desde o último reindex (idempotente)."}

    # full rebuild (the index is disposable)
    from .db import drop_all, create_schema
    drop_all(conn)
    create_schema(conn)
    now = _now()
    counts = {"added": 0}

    # classes
    for md in sorted(C.CLASSES_DIR.glob("*.md")):
        c = parse_class(md)
        conn.execute(
            "INSERT INTO patent_class(id,ordinal,name,slug,markers,lock_note,"
            "memory_md_path,source_sha256,indexed_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (c["id"], c["ordinal"], c["name"], c["slug"],
             json.dumps(c["markers"], ensure_ascii=False), c["lock_note"],
             c["memory_md_path"], _sha256_file(md), now))
        counts["added"] += 1

    # patents (master index + patent md enrichment + docket)
    docket_by_id = {}
    for item in load_master_index():
        pid = item["processo"]
        slug = item["slug"]
        dir_name = f"{pid}_{slug}"
        md_path = C.PATENTS_MD_DIR / f"{dir_name}.md"
        md_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        claims_total, claims_indep, figs = parse_claims(md_text)
        epct = item.get("epct", {}) or {}
        epct_status = epct.get("status") or "SOMENTE_INPI"
        markers = sorted(set(re.findall(r"\[[A-Z_]+\]", md_text[:2000])))
        conn.execute(
            "INSERT INTO patent(id,slug,display_name,dir_name,class_id,role,title_54,nature,peticao,"
            "filing_date,priority_date,epct_status,epct_number,epct_date,abstract,markers,"
            "prototype_status,pasta_original,memory_md_path,docket_path,doc_count,"
            "claims_total,claims_independent,figures_count,source_sha256,memory_sha256,indexed_at)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid, slug, display_name(slug), dir_name, item.get("classe"), item.get("papel"),
             item.get("titulo_oficial_54", ""), item.get("natureza"), str(item.get("peticao", "")),
             _iso(item.get("data_deposito_inpi")), _iso(item.get("prioridade")),
             epct_status, epct.get("numero"), _iso(epct.get("data")),
             item.get("resumo_oficial"), json.dumps(markers, ensure_ascii=False),
             "VER_MEMORIA", item.get("pasta_original"),
             f"memory/patents/{dir_name}.md", f"patents/{dir_name}/docket.yaml",
             item.get("documentos_hasheados", 0), claims_total, claims_indep, figs,
             _sha_text(json.dumps(item, ensure_ascii=False, sort_keys=True)),
             _sha256_file(md_path) if md_path.exists() else None, now))
        counts["added"] += 1

        dk_path = C.PATENTS_DIR / dir_name / "docket.yaml"
        if dk_path.exists():
            dk = parse_docket(dk_path)
            docket_by_id[pid] = dk
            conn.execute(
                "INSERT INTO docket_entry(patent_id,status,alert_level,epct_status,"
                "epct_number,epct_date,janela_paris_12m,janela_paris_alvo,fase_nacional_30m,"
                "gru_arquivo,gru_servico,gru_valor,gru_vencimento,pix_arquivo,pix_data,"
                "pix_valor,annuities_note,office_actions,reminders,aviso,source_sha256,indexed_at)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (pid, dk["status"], dk["alert_level"], dk["epct_status"], dk["epct_number"],
                 dk["epct_date"], dk["janela_paris_12m"], dk["janela_paris_alvo"],
                 dk["fase_nacional_30m"], dk["gru_arquivo"], dk["gru_servico"], dk["gru_valor"],
                 dk["gru_vencimento"], dk["pix_arquivo"], dk["pix_data"], dk["pix_valor"],
                 dk["annuities_note"], dk["office_actions"], dk["reminders"], dk["aviso"],
                 _sha256_file(dk_path), now))
            for dl in derive_deadlines(pid, dk):
                conn.execute(
                    "INSERT INTO deadline(patent_id,kind,label,due_date,status,basis,"
                    "source_field,legal_note,indexed_at) VALUES(?,?,?,?,?,?,?,?,?)",
                    (dl["patent_id"], dl["kind"], dl["label"], dl["due_date"], dl["status"],
                     dl["basis"], dl["source_field"], dl["legal_note"], now))
        # notes
        notes_dir = C.PATENTS_DIR / dir_name / "notes"
        if notes_dir.exists():
            for nf in sorted(notes_dir.glob("*.md")):
                for k, n in enumerate(parse_notes(nf)):
                    conn.execute(
                        "INSERT INTO note(patent_id,tipo,active,done,text,markers,source_file,"
                        "source_section,line_ref,order_index,content_hash,indexed_at)"
                        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (pid, n["tipo"], n["active"], n["done"], n["text"], n["markers"],
                         n["source_file"], n["source_section"], n["line_ref"], k,
                         n["content_hash"], now))
        # renders (rasterized drawings — layer a, ampliável na UI)
        draw_dir = C.PATENTS_DIR / dir_name / "renders" / "drawings"
        if draw_dir.exists():
            for k, png in enumerate(sorted(draw_dir.glob("prancha_*.png")), 1):
                conn.execute(
                    "INSERT INTO render(patent_id,kind,layer,title,asset_path,sha256,"
                    "marker,indexed_at) VALUES(?,?,?,?,?,?,?,?)",
                    (pid, "original_drawing", "a", f"Prancha {k}",
                     str(png.relative_to(C.CENTRAL)).replace("\\", "/"),
                     _sha256_file(png), "desenho oficial do depósito INPI", now))
        # runner runs (seals)
        for s in load_seals(C.PATENTS_DIR / dir_name):
            ts = s.get("timestamp") or s.get("finished_at") or now
            conn.execute(
                "INSERT OR REPLACE INTO runner_run(id,patent_id,started_at,finished_at,"
                "status,beta_runtime,physical_verdict_allowed,max_verdict,tests_passed,"
                "result_hash,invariants_hash,module_hashes,markers,indexed_at)"
                " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (f"{slug}@{ts}", pid, s.get("started_at"), ts,
                 "ok" if s.get("result_hash") else "scaffold",
                 s.get("beta_runtime"), 1 if s.get("physical_verdict_allowed") else 0,
                 s.get("max_verdict"), s.get("tests_passed") or s.get("bloco9_tests"),
                 s.get("result_hash"), s.get("invariants_hash") or s.get("invariants_hash_v3"),
                 json.dumps(s.get("sha256", {}), ensure_ascii=False),
                 json.dumps(s.get("markers", []), ensure_ascii=False), now))

    # documents (map to patent by dir prefix / process number in name)
    id_by_prefix = {r["dir_name"].split("_")[0]: r["id"]
                    for r in conn.execute("SELECT id,dir_name FROM patent")}
    pasta_to_id = {}
    for r in conn.execute("SELECT id,pasta_original FROM patent"):
        if r["pasta_original"] and "/" in r["pasta_original"]:
            pasta_to_id[r["pasta_original"].split("/", 1)[1].rstrip(" ").lower()] = r["id"]
    for d in load_documents():
        pid = None
        m = re.search(r"BR\s?10\s?20\d{2}\s?\d{6}[\s-]?\d", d["name"])
        if m:
            canon = re.sub(r"\s", "", m.group(0))
            canon = canon[:-1] + "-" + canon[-1] if "-" not in canon else canon
            pid = id_by_prefix.get(canon)
        if not pid:
            parts = re.split(r"[\\/]", d["rel_path"])   # aceita \\ (Windows) e / (Linux)
            if len(parts) > 1:
                pid = pasta_to_id.get(parts[1].lower())
        rel_norm = d["rel_path"].replace("\\", "/")     # DB guarda POSIX → serve em Linux e Windows
        conn.execute(
            "INSERT OR IGNORE INTO document(patent_id,rel_path,sha256,size_bytes,mtime,ext,"
            "doc_role,pages,chars,extract_ok,extract_error,is_original,normalized_path,indexed_at)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid, rel_norm, d["sha256"], d["size_bytes"], d["mtime"], d["ext"],
             d["doc_role"], d["pages"], d["chars"], d["extract_ok"], d["extract_error"],
             1, None, now))

    # pendencias
    for pe in parse_pendencias():
        conn.execute(
            "INSERT OR REPLACE INTO pendencia(id,title,status,body,markers,resolved_date,"
            "source_file,line_ref,source_sha256,indexed_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (pe["id"], pe["title"], pe["status"], pe["body"], pe["markers"],
             pe["resolved_date"], "PENDENCIAS.md", pe["line_ref"],
             _sha_text(pe["body"]), now))
        for pat in pe["patents"]:
            if conn.execute("SELECT 1 FROM patent WHERE id=?", (pat,)).fetchone():
                conn.execute("INSERT OR IGNORE INTO pendencia_patent VALUES(?,?)",
                             (pe["id"], pat))

    # derive prototype_status from real runs (a sealed ok run => PILOTO_VIVO)
    conn.execute("UPDATE patent SET prototype_status='PILOTO_VIVO' "
                 "WHERE id IN (SELECT patent_id FROM runner_run WHERE status='ok')")

    finished = _now()
    conn.execute("INSERT OR REPLACE INTO index_meta(key,value) VALUES('global_signature',?)", (sig,))
    conn.execute("INSERT OR REPLACE INTO index_meta(key,value) VALUES('schema_version',?)",
                 (str(C.SCHEMA_VERSION),))
    conn.execute("INSERT OR REPLACE INTO index_meta(key,value) VALUES('last_reindex_utc',?)", (finished,))
    conn.execute("INSERT OR REPLACE INTO index_meta(key,value) VALUES('originals_integrity','OK')")
    n_pat = conn.execute("SELECT count(*) FROM patent").fetchone()[0]
    n_cls = conn.execute("SELECT count(*) FROM patent_class").fetchone()[0]
    n_doc = conn.execute("SELECT count(*) FROM document").fetchone()[0]
    n_dl = conn.execute("SELECT count(*) FROM deadline").fetchone()[0]
    n_note = conn.execute("SELECT count(*) FROM note").fetchone()[0]
    report = {"started_utc": started, "finished_utc": finished, "mode": "full",
              "integrity_status": integ["status"], "patents": n_pat, "classes": n_cls,
              "documents": n_doc, "deadlines": n_dl, "notes": n_note}
    conn.execute("INSERT INTO reindex_run(started_utc,finished_utc,mode,added,updated,"
                 "unchanged,orphaned,integrity_status,report_path) VALUES(?,?,?,?,?,?,?,?,?)",
                 (started, finished, "full", n_pat + n_cls, 0, 0, 0, integ["status"], None))
    conn.commit()
    rp = C.LOGS / f"reindex_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    rp.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    conn.close()
    report["message"] = "reindex full concluído."
    return report


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv or "--full" in sys.argv
    print(json.dumps(reindex(force=force), ensure_ascii=False, indent=1))

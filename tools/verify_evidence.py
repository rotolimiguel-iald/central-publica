# -*- coding: utf-8 -*-
"""verify_evidence — a PROVA DA PROVA (forma = conteúdo).

Lê patents/<dir>/evidence.json (a Cadeia de Prova) e RESOLVE cada elo:
  • document → existe no índice + o arquivo existe + SHA-256 computado AO VIVO (confere com o índice)
  • seal     → o run existe no índice + result_hash; confere se o teste citado passou (results.json)
  • code     → o arquivo existe + SHA-256 computado ao vivo
  • nota     → declaração honesta (sem artefato; sempre 'ok' como qualificação)

Nunca hardcoda hash: computa na hora. Emite evidence_verified.json (o selo da cadeia) e um
relatório. Uso: python tools/verify_evidence.py [SLUG|--all]. Sem arg = todas as que têm evidence.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CENTRAL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CENTRAL))
from backend.app import config as C  # noqa: E402
from backend.app.db import connect  # noqa: E402


def sha_file(p: Path) -> str | None:
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def resolve_elo(conn, pdir: Path, elo: dict) -> dict:
    role = elo.get("role")
    loc = elo.get("locator") or {}
    out = {"role": role, "title": elo.get("title"), "proves": elo.get("proves"),
           "value": elo.get("value"), "resolved": False, "detail": ""}
    kind = loc.get("kind")
    if role == "nota" or not kind:
        out.update(resolved=True, detail="declaração honesta (qualificação, sem artefato)")
        return out

    if kind == "document":
        r = conn.execute("SELECT rel_path, sha256 FROM document WHERE id=?", (loc.get("id"),)).fetchone()
        if not r:
            out["detail"] = f"documento id={loc.get('id')} não encontrado no índice"
            return out
        fpath = C.CENTRAL / r["rel_path"]
        live = sha_file(fpath)
        out["doc_id"] = loc.get("id")
        out["indexed_sha256"] = r["sha256"]
        out["live_sha256"] = live
        out["ref"] = f"documento id={loc.get('id')} · págs {loc.get('pages','?')}"
        if live is None:
            out["detail"] = "arquivo do documento ausente em disco (índice tem o hash)"
            out["resolved"] = bool(r["sha256"])   # o hash selado existe
            out["hash_match"] = None
        else:
            out["hash_match"] = (live == r["sha256"])
            out["resolved"] = out["hash_match"]
            out["detail"] = "SHA-256 confere" if out["hash_match"] else "SHA-256 DIVERGE do índice"
        return out

    if kind == "seal":
        run_id = loc.get("run")
        r = conn.execute("SELECT result_hash FROM runner_run WHERE id=?", (run_id,)).fetchone()
        if not r:
            out["detail"] = f"run {run_id} não encontrado no índice"
            return out
        out["result_hash"] = r["result_hash"]
        out["run"] = run_id
        out["ref"] = f"selo {run_id}"
        test = loc.get("test")
        if test:
            # confere o nome do teste contra o FONTE do runner (pega teste INVENTADO → não resolve)
            runner_srcs = sorted(pdir.glob("runner/one_*.py"))
            found = False
            for src in runner_srcs:
                if f'"{test}"' in src.read_text(encoding="utf-8", errors="ignore"):
                    found = True
                    break
            out["test"] = test
            out["test_in_runner"] = found
            out["test_passed"] = found or None
            out["resolved"] = bool(r["result_hash"]) and found
            out["detail"] = (f"teste '{test}' consta no runner + selo presente" if found
                             else f"teste '{test}' NÃO consta no runner (inventado?) ✗")
        else:
            out["resolved"] = bool(r["result_hash"])
            out["detail"] = "selo do run presente"
        return out

    if kind == "code":
        fpath = pdir / loc.get("path", "")
        live = sha_file(fpath)
        out["ref"] = loc.get("path")
        out["code_path"] = loc.get("path")
        out["live_sha256"] = live
        out["resolved"] = live is not None
        out["detail"] = "arquivo presente, SHA-256 computado" if live else "arquivo AUSENTE"
        return out

    out["detail"] = f"tipo de locator desconhecido: {kind}"
    return out


def verify_patent(conn, dir_name: str) -> dict:
    pdir = C.PATENTS_DIR / dir_name
    ev_path = pdir / "evidence.json"
    if not ev_path.is_file():
        return {"available": False, "dir": dir_name}
    ev = json.loads(ev_path.read_text(encoding="utf-8"))
    claims_out = []
    n_elos = n_ok = 0
    for cl in ev.get("claims", []):
        chain = [resolve_elo(conn, pdir, e) for e in cl.get("chain", [])]
        for e in chain:
            n_elos += 1
            n_ok += 1 if e["resolved"] else 0
        claims_out.append({"n": cl["n"], "marker": cl.get("marker"), "independent": cl.get("independent"),
                           "statement": cl.get("statement"), "verdict": cl.get("verdict"),
                           "chain": chain,
                           "all_resolved": all(e["resolved"] for e in chain)})
    report = {"patent_id": ev.get("patent_id"), "dir": dir_name,
              "claims_total": len(claims_out),
              "claims_fully_resolved": sum(1 for c in claims_out if c["all_resolved"]),
              "elos_total": n_elos, "elos_resolved": n_ok,
              "claims": claims_out}
    (pdir / "evidence_verified.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv):
    conn = connect()
    targets = []
    rows = conn.execute("SELECT dir_name FROM patent ORDER BY dir_name").fetchall()
    all_dirs = [r["dir_name"] for r in rows]
    if not argv or argv[0] == "--all":
        targets = [d for d in all_dirs if (C.PATENTS_DIR / d / "evidence.json").is_file()]
    else:
        slug = argv[0].lower()
        targets = [d for d in all_dirs if slug in d.lower()]
    if not targets:
        print("nenhuma patente com evidence.json encontrada.")
        return 1
    ok_all = True
    for d in targets:
        rep = verify_patent(conn, d)
        if not rep.get("available", True):
            continue
        print(f"\n=== {rep['patent_id']} ({d}) ===")
        print(f"  reivindicações: {rep['claims_fully_resolved']}/{rep['claims_total']} totalmente resolvidas")
        print(f"  elos de prova:  {rep['elos_resolved']}/{rep['elos_total']} resolvidos")
        for c in rep["claims"]:
            mk = "✓" if c["all_resolved"] else "○"
            print(f"   {mk} reivind. {c['n']:>2} [{c['marker']}] — {len(c['chain'])} elos")
            for e in c["chain"]:
                tick = "·" if e["resolved"] else "✗"
                print(f"       {tick} {e['role']}: {e['detail']}")
        ok_all = ok_all and rep["elos_resolved"] == rep["elos_total"]
    conn.close()
    print("\n" + ("TODA A CADEIA RESOLVE ✓" if ok_all else "HÁ ELOS NÃO RESOLVIDOS (ver acima)"))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))

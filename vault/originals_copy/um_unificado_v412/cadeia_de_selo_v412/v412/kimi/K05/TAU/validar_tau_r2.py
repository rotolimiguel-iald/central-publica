#!/usr/bin/env python3
"""Validação final K05/τ★ R2: números, Lean, escopo, citações e hashes."""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(r"C:\IALD")
KIMI = ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "kimi"
BASE = KIMI / "K05" / "TAU"
MED = BASE / "medidas"
REPORT = KIMI / "TAU_ESTRELA_R2.md"
OUT = MED / "validacao_tau_r2.json"

checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object = None) -> None:
    checks.append({"name": name, "pass": bool(condition), "detail": detail})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads((MED / "medidas_tau_r2.json").read_text(encoding="utf-8"))
    clock = json.loads((MED / "clock_selado_extraido.json").read_text(encoding="utf-8"))
    report = REPORT.read_text(encoding="utf-8")
    beta = data["constants"]["alpha_CODATA2018"] * math.sqrt(math.e)
    check("beta_em_runtime", beta == data["constants"]["beta"], beta)
    check("hash_core_confere", clock["source_sha256"] == sha256(Path(clock["source"])), clock["source_sha256"])
    check("onze_leituras_sete_cotas", len(data["readings"]) == 11 and len(data["bounds"]) == 7)
    p1 = [k for k in data["bounds"] if k != "atlas_legacy_1p8e_m33"]
    for rid in ("c_1", "c_inv_beta", "c_sqrt2", "c_2pi", "c_4pi"):
        row = next(r for r in data["readings"] if r["id"] == rid)
        check(f"{rid}_passa_todas_P1", all(row["comparisons"][b]["P1_not_excluded_conditionally"] for b in p1))
    for rid in ("gap_u", "retido"):
        row = next(r for r in data["readings"] if r["id"] == rid)
        check(f"{rid}_falha_todas_P1", all(not row["comparisons"][b]["P1_not_excluded_conditionally"] for b in p1))
    gap = next(r for r in data["readings"] if r["id"] == "gap_u")
    ret = next(r for r in data["readings"] if r["id"] == "retido")
    check("ordem_gap_Kim", abs(gap["comparisons"]["sr87_kim2025"]["orders_above_bound"] - 15.405787310806824) < 1e-12)
    check("ordem_retido_Kim", abs(ret["comparisons"]["sr87_kim2025"]["orders_above_bound"] - 17.32547474029398) < 1e-12)
    check("alternativas_v369_reproduzidas", all(x["relative_difference"] == 0 for x in data["alternative_Gamma_consistency_checks"].values()))
    check("P3_sem_observavel_local", data["protocol"]["P3"]["verdict"].startswith("P3_NO_LOCAL_OBSERVABLE"))
    systems = {s["id"]: s for s in data["regime_candidates"]["systems"]}
    tp = data["constants"]["tP_computed_s"]
    for sid in ("one_eV", "sr_optical", "sr_rest"):
        check(f"regime_{sid}_Planck", systems[sid]["tau_max_s"] == tp)
    for sid in ("bh60", "hubble"):
        check(f"regime_{sid}_horizonte", systems[sid]["tau_max_s"] == systems[sid]["tau_horizon_monopole_s"])
    check("parede_Hubble_no_relatorio", "PAREDE_RELOGIO_E_PONTE_HUBBLE" in report)
    check("sem_valor_ajustado_proibido", "1,0200" not in report and "1.0200" not in report)

    lean_source = (BASE / "candidatas" / "TAU_ESTRELA_R2.lean").read_text(encoding="utf-8")
    sandbox_source = (BASE / "sandbox" / "sources" / "TAU_ESTRELA_R2.lean").read_text(encoding="utf-8")
    log = (BASE / "sandbox" / "logs" / "TAU_ESTRELA_R2.log").read_text(encoding="utf-8")
    check("sandbox_fonte_identica", lean_source == sandbox_source)
    check("lean_rc_zero", "RC: 0" in log and "error:" not in log)
    check("lean_sem_sorry", not re.search(r"\b(sorry|admit)\b", lean_source) and "sorryAx" not in log)
    axiom_lines = [line for line in log.splitlines() if "depends on axioms:" in line]
    check("lean_14_axiom_prints", len(axiom_lines) == 14, len(axiom_lines))
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    used: set[str] = set()
    for line in axiom_lines:
        used.update(re.search(r"\[([^]]*)\]", line).group(1).split(", "))
    check("lean_axiomas_so_trio", used <= allowed, sorted(used))
    check("sem_lake_no_script", "lake build" not in (BASE / "sandbox" / "compilar.sh").read_text(encoding="utf-8"))

    citation_failures: list[dict[str, str]] = []
    citations = re.findall(r"\((kimi-cite://[^)]+)\)", report)
    for citation_target in citations:
        url = citation_target.removesuffix(' "citation"')
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        raw_path = params.get("path", [""])[0]
        path = Path(raw_path)
        if not path.is_file():
            citation_failures.append({"url": url, "error": "arquivo inexistente"})
            continue
        text = path.read_text(encoding="utf-8")
        if "line" in params:
            line = int(params["line"][0])
            if not 1 <= line <= len(text.splitlines()):
                citation_failures.append({"url": url, "error": "linha fora do arquivo"})
                continue
        snippet = params.get("text", [""])[0]
        if snippet and snippet not in text:
            citation_failures.append({"url": url, "error": f"trecho ausente: {snippet}"})
    check("citacoes_locais_verificadas", not citation_failures, {"count": len(citations), "failures": citation_failures})
    check("sem_parametro_text_malformado", "&text%3D" not in report)

    forbidden_names = [str(p) for p in BASE.rglob("*") if p.is_file() and re.search(r"ENTREGA|REGISTRO|DEPOSITO", p.name, re.I)]
    check("sem_artefatos_proibidos", not forbidden_names, forbidden_names)

    artifacts = [REPORT] + sorted(p for p in BASE.rglob("*") if p.is_file() and p != OUT)
    hashes = {str(p): {"bytes": p.stat().st_size, "sha256": sha256(p), "sha16": sha256(p)[:16]} for p in artifacts}
    passed = all(bool(c["pass"]) for c in checks)
    payload = {
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "artifacts_sha256": hashes,
        "no_new_observed_statistic": True,
        "no_registration_or_deposit": True,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "n_checks": len(checks), "failed": [c for c in checks if not c["pass"]], "output": str(OUT)}, ensure_ascii=False, indent=2))
    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Executa cenários R3.1 e grava resultados sintéticos reproduzíveis."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from r31_motor import MASTER_SEED, SCENARIOS, run_scenario


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nsim", type=int, default=3000)
    parser.add_argument("--only", type=str, default="")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("resultados_r31.json"))
    args = parser.parse_args()
    if args.nsim < 100:
        raise SystemExit("nsim mínimo: 100")
    selected = set(args.only.split(",")) if args.only else {s.sid for s in SCENARIOS}
    unknown = selected - {s.sid for s in SCENARIOS}
    if unknown:
        raise SystemExit(f"Cenários desconhecidos: {sorted(unknown)}")

    scenarios = []
    if args.resume and args.output.exists():
        scenarios = json.loads(args.output.read_text(encoding="utf-8"))["scenarios"]
    by_id = {row["id"]: row for row in scenarios}

    for index, spec in enumerate(SCENARIOS):
        if spec.sid not in selected:
            continue
        seed = MASTER_SEED + 101 * index
        print(f"RUN {spec.sid} n={spec.n} nsim={args.nsim} seed={seed}", flush=True)
        row = run_scenario(spec, args.nsim, seed)
        by_id[spec.sid] = row
        print(
            f"  INTEGRITY={row['rates']['integrity_ok']:.6f}; "
            f"POWERED={row['rates']['powered']:.6f}; "
            f"NONSPECIFIC={row['rates']['nonspecific_powered']:.6f}; "
            f"SIZE_ANY12={row['rates']['raw_any_primary_rejection']:.6f}; "
            f"TOST_ANY={row['rates']['raw_any_tost_rejection']:.6f}",
            flush=True,
        )
        ordered = [by_id[s.sid] for s in SCENARIOS if s.sid in by_id]
        payload = {
            "schema": "K06_R31_SESSOES_INDIVIDUAIS_CLUSTERIZADAS_V1",
            "master_seed": MASTER_SEED,
            "no_model_executed": True,
            "no_experimental_result_read": True,
            "production_status": "BLOQUEADO_PARA_PRODUCAO",
            "scenarios": ordered,
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        args.output.write_bytes(encoded)
        print(f"  CHECKPOINT SHA256 {hashlib.sha256(encoded).hexdigest()}", flush=True)
    print(f"WROTE {args.output}")
    print(f"SHA256 {hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()

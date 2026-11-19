#!/usr/bin/env python3
"""Medições finitas comuns a trajetórias original/isomorfa; sem veredito global.

Entrada JSON: {"target": [0/1, ...], "states": {"1": [...], ..., "12": [...]}}.
O evento decisório é V2-RET, p=8,r=10: perturbação depois de k=8,
alteração em k=9 e retorno estabilizado em k=10..12. O esquema anterior
p=4,r=6 fica somente em REV0; A8 permanece como compatibilidade explícita.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def measure(trajectory: dict[str, Any]) -> dict[str, Any]:
    target = trajectory.get("target")
    states = trajectory.get("states")
    if not isinstance(target, list) or not target or any(value not in (0, 1) for value in target):
        raise ValueError("target deve ser vetor binário não vazio")
    if not isinstance(states, dict) or set(states) != {str(k) for k in range(1, 13)}:
        raise ValueError("states deve conter exatamente as chaves 1..12 para V2-RET")
    vectors = []
    for k in range(1, 13):
        vector = states[str(k)]
        if not isinstance(vector, list) or len(vector) != len(target) or any(value not in (0, 1) for value in vector):
            raise ValueError(f"estado {k} inválido")
        vectors.append(vector)
    n = len(target)
    d = [sum(abs(a - b) for a, b in zip(vector, target)) / n for vector in vectors]
    u = [None] + [sum(abs(a - b) for a, b in zip(vectors[k], vectors[k - 1])) / n for k in range(1, 12)]
    stable_return = d[9] == d[10] == d[11] == 0 and u[10] == u[11] == 0
    a8_legacy = d[5] == d[6] == d[7] == 0 and u[5] == u[6] == u[7] == 0
    perturb_no_effect = d[7] == 0 and d[8] == 0
    perturb_return = d[7] == 0 and d[8] > 0 and stable_return
    if d[7] != 0:
        perturbation_class = "PERTURBATION_NOT_APPLICABLE"
    elif d[8] == 0:
        perturbation_class = "PERTURBATION_NO_EFFECT"
    elif perturb_return:
        perturbation_class = "FINITE_HORIZON_RETURN_OBSERVED"
    else:
        perturbation_class = "PERTURBATION_NO_RETURN"
    return {
        "assertion_count": n,
        "interaction_count": 12,
        "event_id": "V2-RET",
        "p": 8,
        "r": 10,
        "d_by_k": {str(k + 1): value for k, value in enumerate(d)},
        "u_by_k": {str(k + 1): value for k, value in enumerate(u) if value is not None},
        "A8_legacy_compatibility_only": a8_legacy,
        "stable_target_k10_k12": stable_return,
        "perturbation_p8_no_effect": perturb_no_effect,
        "V2_RET_p8_r10": perturb_return,
        "perturbation_class": perturbation_class,
        "scope": "12 interações; horizonte finito não prova ponto fixo matemático, limite, bacia universal nem atrator de LLM",
        "verdict_emitted": False,
    }


def self_test() -> dict[str, Any]:
    target = [1] * 24
    zero = [0] * 24
    cases = {
        "return": {str(k): (zero if k == 9 else target) for k in range(1, 13)},
        "no_effect": {str(k): target for k in range(1, 13)},
        "no_return": {str(k): (zero if k >= 9 else target) for k in range(1, 13)},
        "not_applicable": {str(k): (zero if k in (8, 9) else target) for k in range(1, 13)},
        "late_unstable_return": {str(k): (zero if k in (9, 10) else target) for k in range(1, 13)},
    }
    outputs = {name: measure({"target": target, "states": states}) for name, states in cases.items()}
    try:
        measure({"target": target, "states": {str(k): target for k in range(1, 9)}})
    except ValueError as exc:
        legacy_rejected = "1..12" in str(exc)
    else:
        legacy_rejected = False
    checks = {
        "return_detected": outputs["return"]["V2_RET_p8_r10"] is True and outputs["return"]["perturbation_class"] == "FINITE_HORIZON_RETURN_OBSERVED",
        "return_uses_new_indices": outputs["return"]["d_by_k"]["8"] == 0 and outputs["return"]["d_by_k"]["9"] > 0 and outputs["return"]["stable_target_k10_k12"],
        "a8_preserved_separately": outputs["return"]["A8_legacy_compatibility_only"] is True,
        "no_effect_not_return": outputs["no_effect"]["perturbation_class"] == "PERTURBATION_NO_EFFECT" and not outputs["no_effect"]["V2_RET_p8_r10"],
        "no_return_detected": outputs["no_return"]["perturbation_class"] == "PERTURBATION_NO_RETURN",
        "not_applicable_detected": outputs["not_applicable"]["perturbation_class"] == "PERTURBATION_NOT_APPLICABLE",
        "late_return_is_not_r10": outputs["late_unstable_return"]["perturbation_class"] == "PERTURBATION_NO_RETURN" and not outputs["late_unstable_return"]["V2_RET_p8_r10"],
        "legacy_horizon_rejected": legacy_rejected,
        "event_identity": all(output["event_id"] == "V2-RET" and output["p"] == 8 and output["r"] == 10 and output["interaction_count"] == 12 for output in outputs.values()),
        "no_verdicts": all(not output["verdict_emitted"] for output in outputs.values()),
    }
    return {
        "schema": "k06.contaminacao.autoteste-ponto-fixo.v2-r3-1",
        "all_pass": all(checks.values()),
        "checks": checks,
        "outputs": outputs,
        "legacy_schema_location": "REV0_ONLY",
        "model_executed": False,
        "public_article_transformed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        if not args.input:
            parser.error("--input é obrigatório sem --self-test")
        result = measure(json.loads(args.input.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pretty(result))
    if args.self_test and not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

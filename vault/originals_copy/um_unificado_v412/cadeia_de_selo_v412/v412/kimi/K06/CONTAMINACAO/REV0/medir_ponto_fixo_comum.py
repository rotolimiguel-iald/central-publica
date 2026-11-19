#!/usr/bin/env python3
"""Medições finitas comuns a trajetórias original/isomorfa; sem veredito global.

Entrada JSON: {"target": [0/1, ...], "states": {"1": [...], ..., "8": [...]}}.
O evento de retorno é a definição candidata herdada da R2 para p=4; sua
primazia, n, limiar, poder e multiplicidade devem ser congelados na R3.
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
    if not isinstance(states, dict) or set(states) != {str(k) for k in range(1, 9)}:
        raise ValueError("states deve conter exatamente as chaves 1..8")
    vectors = []
    for k in range(1, 9):
        vector = states[str(k)]
        if not isinstance(vector, list) or len(vector) != len(target) or any(value not in (0, 1) for value in vector):
            raise ValueError(f"estado {k} inválido")
        vectors.append(vector)
    n = len(target)
    d = [sum(abs(a - b) for a, b in zip(vector, target)) / n for vector in vectors]
    u = [None] + [sum(abs(a - b) for a, b in zip(vectors[k], vectors[k - 1])) / n for k in range(1, 8)]
    stable_last3 = d[5] == d[6] == d[7] == 0 and u[6] == u[7] == 0
    a8_r2_compat = d[5] == d[6] == d[7] == 0 and u[5] == u[6] == u[7] == 0
    perturb_no_effect = d[3] == 0 and d[4] == 0
    perturb_return = d[3] == 0 and d[4] > 0 and stable_last3
    if d[3] != 0:
        perturbation_class = "PERTURBATION_NOT_APPLICABLE"
    elif d[4] == 0:
        perturbation_class = "PERTURBATION_NO_EFFECT"
    elif perturb_return:
        perturbation_class = "FINITE_HORIZON_RETURN_OBSERVED"
    else:
        perturbation_class = "PERTURBATION_NO_RETURN"
    return {
        "assertion_count": n,
        "d_by_k": {str(k + 1): value for k, value in enumerate(d)},
        "u_by_k": {str(k + 1): value for k, value in enumerate(u) if value is not None},
        "A8_R2_compatibility_only": a8_r2_compat,
        "stable_target_k6_k8": stable_last3,
        "perturbation_p4_no_effect": perturb_no_effect,
        "PERTURB_RETURN_p4_r6_candidate": perturb_return,
        "perturbation_class": perturbation_class,
        "scope": "horizonte finito; não prova ponto fixo matemático, limite, bacia universal nem atrator de LLM",
        "verdict_emitted": False,
    }


def self_test() -> dict[str, Any]:
    target = [1] * 24
    zero = [0] * 24
    return_case = {"target": target, "states": {str(k): (zero if k == 5 else target) for k in range(1, 9)}}
    no_effect_case = {"target": target, "states": {str(k): target for k in range(1, 9)}}
    no_return_case = {"target": target, "states": {str(k): (zero if k >= 5 else target) for k in range(1, 9)}}
    outputs = {name: measure(case) for name, case in {"return": return_case, "no_effect": no_effect_case, "no_return": no_return_case}.items()}
    checks = {
        "return_detected": outputs["return"]["PERTURB_RETURN_p4_r6_candidate"] is True,
        "no_effect_not_return": outputs["no_effect"]["perturbation_class"] == "PERTURBATION_NO_EFFECT" and not outputs["no_effect"]["PERTURB_RETURN_p4_r6_candidate"],
        "no_return_detected": outputs["no_return"]["perturbation_class"] == "PERTURBATION_NO_RETURN",
        "no_verdicts": all(not output["verdict_emitted"] for output in outputs.values()),
    }
    return {"all_pass": all(checks.values()), "checks": checks, "outputs": outputs, "model_executed": False}


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

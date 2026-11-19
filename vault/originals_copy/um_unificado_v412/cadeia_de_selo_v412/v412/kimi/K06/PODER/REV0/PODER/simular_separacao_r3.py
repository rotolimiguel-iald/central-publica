# -*- coding: utf-8 -*-
"""K06/R3 — resumidor perfeito sem atrator versus leitor com atrator.

Trajetórias inteiramente sintéticas, 24 asserções, semente fixa.
A perturbação ocorre depois de k=8 para preservar A8 legado nas leituras 1–8;
o retorno é a versão reindexada p=8, r=10 do predicado finito.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

SEED = 2026111402
OUT = Path(__file__).with_name("separacao_r3.json")


def distances(states: np.ndarray, target: np.ndarray) -> tuple[dict[int, float], dict[int, float]]:
    d = {k + 1: float(np.mean(np.abs(states[k] - target))) for k in range(states.shape[0])}
    u = {k + 1: float(np.mean(np.abs(states[k] - states[k - 1]))) for k in range(1, states.shape[0])}
    return d, u


def measure(states: np.ndarray, target: np.ndarray) -> dict:
    d, u = distances(states, target)
    a8 = d[6] == d[7] == d[8] == 0.0 and u[6] == u[7] == u[8] == 0.0
    retorno = (
        d[8] == 0.0
        and d[9] > 0.0
        and d[10] == d[11] == d[12] == 0.0
        and u[11] == u[12] == 0.0
    )
    c8_legado = a8 and (d[1] - d[8] >= 6.0 / 24.0)
    q = a8 and retorno
    if retorno:
        perturbation_class = "FINITE_HORIZON_RETURN_OBSERVED"
    elif d[9] == 0.0:
        perturbation_class = "PERTURBATION_NO_EFFECT"
    else:
        perturbation_class = "PERTURBATION_NO_RETURN"
    return {
        "d_by_k": d,
        "u_by_k": u,
        "A8_no_estrato_d1_zero": bool(a8),
        "C8_legado_apenas_para_contraste_historico": bool(c8_legado),
        "RETORNO_p8_r10": bool(retorno),
        "Q_A8_e_RETORNO": bool(q),
        "perturbation_class": perturbation_class,
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    target = np.ones(24, dtype=np.int8)
    disturbed = target.copy()
    indices = np.sort(rng.choice(24, size=6, replace=False))
    disturbed[indices] = 0

    # Antes do empurrão, ambos produzem oito leituras perfeitas: resumo perfeito.
    prefix = np.repeat(target[None, :], 8, axis=0)
    summarizer = np.concatenate([prefix, disturbed[None, :], np.repeat(disturbed[None, :], 3, axis=0)], axis=0)
    attractor = np.concatenate([prefix, disturbed[None, :], np.repeat(target[None, :], 3, axis=0)], axis=0)

    result_summary = measure(summarizer, target)
    result_attractor = measure(attractor, target)
    separates = result_summary["Q_A8_e_RETORNO"] != result_attractor["Q_A8_e_RETORNO"]
    payload = {
        "schema": "K06_R3_SEPARACAO_SINTETICA_V1",
        "seed": SEED,
        "assertions": 24,
        "readings": 12,
        "perturbed_assertion_indices_one_based": [int(i + 1) for i in indices],
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "scope": "Demonstração lógica em trajetórias sintéticas; não é validação de extrator nem evidência sobre LLM.",
        "resumidor_perfeito_sem_atrator": result_summary,
        "leitor_com_atrator": result_attractor,
        "separation_verdict": "SEPARA_EM_SIMULACAO" if separates else "NAO_DECIDE",
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    OUT.write_bytes(encoded)
    print(f"SEED={SEED}; perturbacao_indices_1based={payload['perturbed_assertion_indices_one_based']}")
    print("k | d_resumidor | d_atrator")
    for k in range(1, 13):
        print(f"{k:2d} | {result_summary['d_by_k'][k]:.6f} | {result_attractor['d_by_k'][k]:.6f}")
    print("leitura | A8 | C8_legado | RETORNO | Q")
    for name, result in (("resumidor", result_summary), ("atrator", result_attractor)):
        print(
            f"{name} | {int(result['A8_no_estrato_d1_zero'])} | "
            f"{int(result['C8_legado_apenas_para_contraste_historico'])} | "
            f"{int(result['RETORNO_p8_r10'])} | {int(result['Q_A8_e_RETORNO'])}"
        )
    print(f"VEREDITO={payload['separation_verdict']}")
    print(f"WROTE {OUT}")
    print(f"SHA256 {hashlib.sha256(encoded).hexdigest()}")
    if not separates:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

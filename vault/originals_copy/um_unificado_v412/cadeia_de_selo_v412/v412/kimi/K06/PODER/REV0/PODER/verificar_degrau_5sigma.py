# -*- coding: utf-8 -*-
"""K06/R3 — verificação independente do degrau 5 sigma, sem dados experimentais."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import binom, norm

from simular_poder_conjunto import (
    ALPHA_5SIGMA,
    cp_lower,
    cp_upper,
    cutoff_powered,
    cutoff_falsified,
    fisher_table,
    holm_reject_all,
)

SEED = 2026111403
OUT = Path(__file__).with_name("degrau_5sigma.json")


def pooled_n(p1: float, p2: float, alpha: float, power: float = 0.90) -> float:
    za = norm.ppf(1.0 - alpha)
    zb = norm.ppf(power)
    pbar = (p1 + p2) / 2.0
    numerator = (
        za * math.sqrt(2.0 * pbar * (1.0 - pbar))
        + zb * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    ) ** 2
    return numerator / (p1 - p2) ** 2


def fisher_power(n: int, alpha: float, p1: float = 0.90, p2: float = 0.60) -> float:
    table = fisher_table(n)
    probabilities = np.outer(binom.pmf(np.arange(n + 1), n, p1), binom.pmf(np.arange(n + 1), n, p2))
    return float((probabilities * (table <= alpha)).sum())


def power_12(n: int, nsim: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    x_t = rng.binomial(n, 0.90, size=(nsim, 3))
    x_c = np.stack([rng.binomial(n, 0.60, size=(nsim, 3)) for _ in range(4)], axis=-1)
    table = fisher_table(n)
    p = table[x_t[:, :, None], x_c].reshape(nsim, 12)
    return float(holm_reject_all(p, ALPHA_5SIGMA).mean())


def cp_row(n: int, conf: float, p: float = 0.90) -> dict:
    c = cutoff_powered(n, conf)
    one = float(binom.sf(c - 1, n, p)) if c is not None else 0.0
    return {"n": n, "cut": c, "one_family": one, "three_families": one ** 3}


def sustained_first(rows: list[dict], stop: int) -> int | None:
    by_n = {row["n"]: row["three_families"] for row in rows}
    for n in sorted(by_n):
        if all(by_n[k] >= 0.90 for k in range(n, stop + 1) if k in by_n):
            return n
    return None


def main() -> None:
    alpha12 = ALPHA_5SIGMA / 12.0
    n_normal = pooled_n(0.90, 0.60, alpha12)
    exact = {str(n): fisher_power(n, alpha12) for n in (184, 185)}
    powers12 = {
        "210": power_12(210, 40000, SEED + 1),
        "215": power_12(215, 40000, SEED + 2),
    }

    legacy_rows = [cp_row(n, 1.0 - ALPHA_5SIGMA / 3.0) for n in range(600, 701)]
    iut_rows = [cp_row(n, 1.0 - ALPHA_5SIGMA) for n in range(580, 701)]
    legacy_655 = cp_row(655, 1.0 - ALPHA_5SIGMA / 3.0)
    iut_618 = cp_row(618, 1.0 - ALPHA_5SIGMA)
    iut_655 = cp_row(655, 1.0 - ALPHA_5SIGMA)
    falsified_655 = cutoff_falsified(655, 1.0 - ALPHA_5SIGMA / 3.0)
    falsified_618 = cutoff_falsified(618, 1.0 - ALPHA_5SIGMA / 3.0)

    continuous = []
    for effect in (0.5, 0.8, 1.0):
        z_alpha = norm.ppf(1.0 - alpha12)
        z_beta = norm.ppf(0.90)
        n = math.ceil(2.0 * (z_alpha + z_beta) ** 2 / effect**2)
        continuous.append({"standardized_effect": effect, "n_per_arm_approx": n})

    payload = {
        "schema": "K06_R3_DEGRAU_5SIGMA_SINTETICO_V1",
        "seed": SEED,
        "alpha_5sigma_one_sided": ALPHA_5SIGMA,
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "single_contrast": {
            "alpha_bonferroni_12": alpha12,
            "z": float(norm.isf(alpha12)),
            "normal_n_unrounded": n_normal,
            "normal_n_ceiling": math.ceil(n_normal),
            "exact_fisher_power": exact,
        },
        "twelve_dynamic_contrasts": {
            "method": "3 famílias × 4 controles; Holm/12; T compartilhado; 40000 corridas por n",
            "power": powers12,
        },
        "cp_legacy_alpha_div_3": {
            "first_any_n_600_700": next((r["n"] for r in legacy_rows if r["three_families"] >= 0.90), None),
            "first_sustained_through_700": sustained_first(legacy_rows, 700),
            "n655": legacy_655,
            "falsified_cut_n655": falsified_655,
        },
        "cp_iut_no_div_3": {
            "first_any_n_580_700": next((r["n"] for r in iut_rows if r["three_families"] >= 0.90), None),
            "first_sustained_through_700": sustained_first(iut_rows, 700),
            "n618": iut_618,
            "n655": iut_655,
            "falsified_cut_n618_alpha_div_3": falsified_618,
            "note": "A correção IUT remove a divisão por 3 somente no ramo POWERED; FALSIFIED conserva Bonferroni/3.",
        },
        "costs": {
            "legacy_review_20_cells_n655_8_calls": {"sessions": 20 * 655, "interactions": 20 * 655 * 8},
            "iut_20_cells_n618_8_calls": {"sessions": 20 * 618, "interactions": 20 * 618 * 8},
            "r3_20_cells_n618_12_calls": {"sessions": 20 * 618, "interactions": 20 * 618 * 12},
            "r3_20_cells_n655_12_calls": {"sessions": 20 * 655, "interactions": 20 * 655 * 12},
            "capable_only_15_cells_n655_8_calls": {"sessions": 15 * 655, "interactions": 15 * 655 * 8},
        },
        "alternatives_not_selected": {
            "fewer_arms": {
                "description": "Três controles em vez de quatro: 9+9 contrastes e 16 células; custo aritmético, poder a recalcular.",
                "cells": 16,
                "sessions_n618": 16 * 618,
                "interactions_n618_12_calls": 16 * 618 * 12,
            },
            "continuous_outcome": {
                "description": "Aproximação z para um contraste, 90% e alpha5/12; não é poder dos 24 nem do veredito inteiro.",
                "examples": continuous,
            },
            "sequential_preregistered": {
                "description": "Candidato com no máximo 4 análises e alpha-spending O'Brien–Fleming congelado.",
                "status": "SEM_N_OU_PODER_DECLARADO; exige simular parada, correlação, ICC, texto, extrator e os 24 testes",
            },
        },
        "limitations": [
            "Os n=185, ≈215 e ≥655 são benchmarks do desenho legado, não garantia da R3 completa.",
            "A R3 mede A8 e retorno na mesma sessão de 12 interações; por isso o custo de 8 interações é só legado.",
            "Os cálculos não incorporam cabimento da entrada pública nem certificam o extrator.",
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    OUT.write_bytes(encoded)
    print(f"alpha5={ALPHA_5SIGMA:.12e}; alpha5/12={alpha12:.12e}; z={norm.isf(alpha12):.9f}")
    print(f"n_normal={n_normal:.9f}; teto={math.ceil(n_normal)}; Fisher184={exact['184']:.9f}; Fisher185={exact['185']:.9f}")
    print(f"Holm12 n210={powers12['210']:.6f}; n215={powers12['215']:.6f}")
    print(f"CP legacy: first_any={payload['cp_legacy_alpha_div_3']['first_any_n_600_700']}; sustained={payload['cp_legacy_alpha_div_3']['first_sustained_through_700']}; n655={legacy_655}")
    print(f"CP IUT: first_any={payload['cp_iut_no_div_3']['first_any_n_580_700']}; sustained={payload['cp_iut_no_div_3']['first_sustained_through_700']}; n618={iut_618}")
    print(f"COST legacy n655: {payload['costs']['legacy_review_20_cells_n655_8_calls']}")
    print(f"WROTE {OUT}")
    print(f"SHA256 {hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()

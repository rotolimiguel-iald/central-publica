# -*- coding: utf-8 -*-
"""K06/R3 — poder do veredito COMPLETO, somente com dados sintéticos.

Nenhum modelo de linguagem é chamado. Nenhum resultado experimental é lido.
O evento binário Q = A8_condicionado AND RETORNO é simulado por célula.
As taxas são hipóteses de desenho, não estimativas empíricas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import expit, logit
from scipy.stats import beta, binom, hypergeom, norm

MASTER_SEED = 2026111401
LEGACY_SEED = 20261113
ARMS = ("V2-PLA", "V2-OUT", "V2-ISO-A", "V2-ISO-B")
SUPERIORITY = (0, 1)
NONINFERIORITY = (2, 3)
DELTA_ISO = 0.15
THRESHOLD_CP = 0.80
ALPHA_BASE = 0.05
ALPHA_5SIGMA = float(norm.sf(5.0))
DEFAULT_BASE_N = 320
EXTRACTOR_POOL_CEILING = 0.6192060638168921
EXTRACTOR_ARM_CEILING = 0.09102821015130445


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cp_lower(x: int, n: int, conf: float) -> float:
    return 0.0 if x == 0 else float(beta.ppf(1.0 - conf, x, n - x + 1))


def cp_upper(x: int, n: int, conf: float) -> float:
    return 1.0 if x >= n else float(beta.ppf(conf, x + 1, n - x))


def cutoff_powered(n: int, conf: float, threshold: float = THRESHOLD_CP) -> int | None:
    for x in range(n + 1):
        if cp_lower(x, n, conf) > threshold:
            return x
    return None


def cutoff_falsified(n: int, conf: float, threshold: float = THRESHOLD_CP) -> int | None:
    answer = None
    for x in range(n + 1):
        if cp_upper(x, n, conf) < threshold:
            answer = x
    return answer


def fisher_table(n: int) -> np.ndarray:
    xt = np.arange(n + 1)[:, None]
    xc = np.arange(n + 1)[None, :]
    # Permutação exata de rótulos para desfecho binário: Fisher unilateral.
    return hypergeom.sf(xt - 1, 2 * n, xt + xc, n)


def fisher_lower_table(n: int) -> np.ndarray:
    xt = np.arange(n + 1)[:, None]
    xc = np.arange(n + 1)[None, :]
    return hypergeom.cdf(xt, 2 * n, xt + xc, n)


def noninferiority_z(x_t: np.ndarray, x_c: np.ndarray, n: int, delta: float) -> np.ndarray:
    pt = x_t / n
    pc = x_c / n
    se = np.sqrt(np.maximum(pt * (1.0 - pt) / n + pc * (1.0 - pc) / n, 1e-15))
    return (pt - pc + delta) / se


def noninferiority_p(x_t: np.ndarray, x_c: np.ndarray, n: int, delta: float) -> np.ndarray:
    """Score de Wald para H0: p_T - p_C <= -delta; uso de planejamento.

    A aproximação normal é uma limitação declarada, sobretudo na cauda 5 sigma.
    """
    return norm.sf(noninferiority_z(x_t, x_c, n, delta))


def inferiority_p(x_t: np.ndarray, x_c: np.ndarray, n: int, delta: float) -> np.ndarray:
    """Direção oposta: evidência de p_T-p_C < -delta."""
    return norm.cdf(noninferiority_z(x_t, x_c, n, delta))


def holm_reject_all(p: np.ndarray, alpha: float) -> np.ndarray:
    ordered = np.sort(p, axis=-1)
    m = ordered.shape[-1]
    thresholds = alpha / (m - np.arange(m))
    return np.all(ordered <= thresholds, axis=-1)


def _text_splits(n: int) -> list[int]:
    # Três ou mais textos por controle: três estratos no modelo de planejamento.
    return [n // 3 + (1 if i < n % 3 else 0) for i in range(3)]


def draw_arm_counts(
    rng: np.random.Generator,
    nsim: int,
    n: int,
    p: float,
    shared_text_z: np.ndarray,
    icc: float,
    cluster_size: int = 10,
) -> np.ndarray:
    """Contagens por família; 3 estratos de texto e beta-binomial por cluster."""
    out = np.zeros((nsim, 3), dtype=np.int32)
    p = float(min(max(p, 1e-9), 1.0 - 1e-9))
    for family in range(3):
        for text_index, n_text in enumerate(_text_splits(n)):
            if n_text == 0:
                continue
            p_text = expit(logit(p) + shared_text_z[:, family, text_index])
            done = 0
            while done < n_text:
                m = min(cluster_size, n_text - done)
                if icc <= 0.0:
                    out[:, family] += rng.binomial(m, p_text, size=nsim)
                else:
                    concentration = 1.0 / icc - 1.0
                    aa = np.maximum(p_text * concentration, 1e-9)
                    bb = np.maximum((1.0 - p_text) * concentration, 1e-9)
                    p_cluster = rng.beta(aa, bb, size=nsim)
                    out[:, family] += rng.binomial(m, p_cluster, size=nsim)
                done += m
    return out


def draw_all_counts(
    rng: np.random.Generator,
    nsim: int,
    n: int,
    p_t: float,
    p_controls: tuple[float, float, float, float],
    icc: float,
    text_sd: float,
) -> tuple[np.ndarray, np.ndarray]:
    # A mesma dificuldade latente é pareada por família/estrato entre os braços.
    shared_z = rng.normal(0.0, text_sd, size=(nsim, 3, 3)) if text_sd > 0 else np.zeros((nsim, 3, 3))
    x_t = draw_arm_counts(rng, nsim, n, p_t, shared_z, icc)
    x_c = np.stack(
        [draw_arm_counts(rng, nsim, n, p, shared_z, icc) for p in p_controls],
        axis=-1,
    )
    return x_t, x_c


def scenario_definitions(base_n: int) -> list[dict]:
    return [
        {
            "id": "BASE_INDEPENDENTE",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.0,
            "text_sd": 0.0,
            "control_q": 0.60,
            "extractor_ceiling": 1.0,
            "temperature_label": "0,2 apenas como configuração; sem cópias no cenário ideal",
        },
        {
            "id": "TEMP02_ICC_015",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.15,
            "text_sd": 0.10,
            "control_q": 0.60,
            "extractor_ceiling": 1.0,
            "temperature_label": "0,2; ICC sintético 0,15 em clusters de 10",
        },
        {
            "id": "TEMP02_ICC_035",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.35,
            "text_sd": 0.20,
            "control_q": 0.60,
            "extractor_ceiling": 1.0,
            "temperature_label": "0,2; ICC sintético 0,35 em clusters de 10",
        },
        {
            "id": "CONTROLE_070",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.15,
            "text_sd": 0.10,
            "control_q": 0.70,
            "extractor_ceiling": 1.0,
            "temperature_label": "0,2; controles informativos em 0,70",
        },
        {
            "id": "CONTROLE_080",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.15,
            "text_sd": 0.10,
            "control_q": 0.80,
            "extractor_ceiling": 1.0,
            "temperature_label": "0,2; controles informativos em 0,80",
        },
        {
            "id": "EXTRATOR_TETO_POOL_0619206",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.0,
            "text_sd": 0.0,
            "control_q": 0.60,
            "extractor_ceiling": EXTRACTOR_POOL_CEILING,
            "temperature_label": "teto conservador pooled imposto a todos os braços",
        },
        {
            "id": "EXTRATOR_TETO_POR_BRACO_0091028",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.0,
            "text_sd": 0.0,
            "control_q": 0.60,
            "extractor_ceiling": EXTRACTOR_ARM_CEILING,
            "temperature_label": "teto conservador por braço imposto a todos os braços",
        },
        {
            "id": "COMBINADO_CONSERVADOR",
            "n": base_n,
            "alpha": ALPHA_BASE,
            "icc": 0.35,
            "text_sd": 0.20,
            "control_q": 0.70,
            "extractor_ceiling": EXTRACTOR_POOL_CEILING,
            "temperature_label": "ICC 0,35 + controle 0,70 + teto pooled; cenário, não estimativa",
        },
        {
            "id": "CINCO_SIGMA_R3_N618",
            "n": 618,
            "alpha": ALPHA_5SIGMA,
            "icc": 0.0,
            "text_sd": 0.0,
            "control_q": 0.60,
            "extractor_ceiling": 1.0,
            "temperature_label": "IUT CP sem divisão por 3; 24 testes globais",
        },
        {
            "id": "CINCO_SIGMA_R3_N655",
            "n": 655,
            "alpha": ALPHA_5SIGMA,
            "icc": 0.0,
            "text_sd": 0.0,
            "control_q": 0.60,
            "extractor_ceiling": 1.0,
            "temperature_label": "mesmo n da conta legada; IUT CP corrigido e 24 testes globais",
        },
    ]


def run_scenario(spec: dict, nsim: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    n = spec["n"]
    alpha = spec["alpha"]
    cap = spec["extractor_ceiling"]
    p_q_t = min(0.90, cap)
    p_controls = (
        min(spec["control_q"], cap),
        min(spec["control_q"], cap),
        p_q_t,
        p_q_t,
    )
    # Especificidade binária: S=1[X >= 18/24]. Isomorfos usam o alvo transformado.
    p_s_t = min(0.95, cap)
    p_s_controls = (
        min(0.70, cap),
        min(0.70, cap),
        p_s_t,
        p_s_t,
    )

    x_q_t, x_q_c = draw_all_counts(
        rng, nsim, n, p_q_t, p_controls, spec["icc"], spec["text_sd"]
    )
    x_s_t, x_s_c = draw_all_counts(
        rng, nsim, n, p_s_t, p_s_controls, spec["icc"], spec["text_sd"]
    )

    table = fisher_table(n)
    lower_table = fisher_lower_table(n)
    p_dyn = np.empty((nsim, 3, 4), dtype=float)
    p_spec = np.empty((nsim, 3, 4), dtype=float)
    p_dyn_opposite = np.empty((nsim, 3, 4), dtype=float)
    p_spec_opposite = np.empty((nsim, 3, 4), dtype=float)
    for j in SUPERIORITY:
        p_dyn[:, :, j] = table[x_q_t, x_q_c[:, :, j]]
        p_spec[:, :, j] = table[x_s_t, x_s_c[:, :, j]]
        p_dyn_opposite[:, :, j] = lower_table[x_q_t, x_q_c[:, :, j]]
        p_spec_opposite[:, :, j] = lower_table[x_s_t, x_s_c[:, :, j]]
    for j in NONINFERIORITY:
        p_dyn[:, :, j] = noninferiority_p(x_q_t, x_q_c[:, :, j], n, DELTA_ISO)
        p_spec[:, :, j] = noninferiority_p(x_s_t, x_s_c[:, :, j], n, DELTA_ISO)
        p_dyn_opposite[:, :, j] = inferiority_p(x_q_t, x_q_c[:, :, j], n, DELTA_ISO)
        p_spec_opposite[:, :, j] = inferiority_p(x_s_t, x_s_c[:, :, j], n, DELTA_ISO)

    p24 = np.concatenate([p_dyn.reshape(nsim, 12), p_spec.reshape(nsim, 12)], axis=1)
    p24_opposite = np.concatenate(
        [p_dyn_opposite.reshape(nsim, 12), p_spec_opposite.reshape(nsim, 12)], axis=1
    )
    all24 = holm_reject_all(p24, alpha)
    dyn12 = holm_reject_all(p_dyn.reshape(nsim, 12), alpha)
    spec12 = holm_reject_all(p_spec.reshape(nsim, 12), alpha)

    # FALSIFIED: união de 3 CP + 24 testes direcionais; Bonferroni alpha/27.
    cp_conf_falsified = 1.0 - alpha / 27.0
    c_false = cutoff_falsified(n, cp_conf_falsified)
    falsified_cp_leg = np.any(x_q_t <= c_false, axis=1) if c_false is not None else np.zeros(nsim, dtype=bool)
    falsified_directional = np.any(p24_opposite <= alpha / 27.0, axis=1)
    falsified_full = falsified_cp_leg | falsified_directional

    # POWERED: IUT sobre três famílias; não se divide alpha por 3.
    # FALSIFIED tem precedência na árvore e exclui POWERED na mesma corrida.
    cp_conf_powered = 1.0 - alpha
    c_power = cutoff_powered(n, cp_conf_powered)
    cp_each = x_q_t >= c_power if c_power is not None else np.zeros((nsim, 3), dtype=bool)
    cp_all = np.all(cp_each, axis=1)
    full = all24 & cp_all & ~falsified_full

    mean = float(full.mean())
    se = math.sqrt(max(mean * (1.0 - mean) / nsim, 0.0))
    deff = 1.0 + (10.0 - 1.0) * spec["icc"]
    return {
        **spec,
        "seed": seed,
        "nsim": nsim,
        "design": {
            "event": "Q = A8_condicionado_d1 AND RETORNO",
            "dynamic_tests": 12,
            "specificity_tests": 12,
            "multiplicity": "Holm global sobre 24; IUT no POWERED; FALSIFIED: união de 27 com Bonferroni",
            "iso_noninferiority_margin": DELTA_ISO,
            "specificity_rule": "S=1[X>=18/24]; superioridade PLA/OUT; não inferioridade ISO-A/ISO-B",
            "cp_powered_cut": c_power,
            "cp_falsified_cut": c_false,
            "integrity_assumed_for_power": True,
        },
        "rates": {
            "p_Q_T": p_q_t,
            "p_Q_controls": list(p_controls),
            "p_specificity_T": p_s_t,
            "p_specificity_controls": list(p_s_controls),
        },
        "n_effective_icc": n / deff,
        "design_effect_icc": deff,
        "power": {
            "cp_all_3": float(cp_all.mean()),
            "dynamic_12_all": float(dyn12.mean()),
            "specificity_12_all": float(spec12.mean()),
            "global_24_all": float(all24.mean()),
            "complete_powered": mean,
            "complete_mc_se": se,
            "complete_mc_95_low": max(0.0, mean - 1.96 * se),
            "complete_mc_95_high": min(1.0, mean + 1.96 * se),
            "one_block_passes_other_fails": float(np.mean(dyn12 ^ spec12)),
            "cp_falsified_leg_rate_under_simulated_alternative": float(falsified_cp_leg.mean()),
            "directional_falsified_rate_under_simulated_alternative": float(falsified_directional.mean()),
            "full_falsified_rate_under_simulated_alternative": float(falsified_full.mean()),
        },
        "limitations": [
            "Taxas e dependências são hipóteses sintéticas, não medidas de modelos.",
            "O teste de não inferioridade usa aproximação normal; a cauda 5 sigma exige validação exata adicional.",
            "O teto do extrator é cenário conservador imposto a Q e à especificidade, não modelo identificado dos 96 erros.",
            "INTEGRITY_OK foi suposto para medir poder; na produção os bloqueios têm precedência fail-closed.",
        ],
    }


def legacy_r2(nsim: int = 40000) -> dict:
    """Reproduz a cota superior R2: CP com /3, 12 dinâmicos e especificidade certa."""
    rng = np.random.default_rng(LEGACY_SEED)
    n = 100
    alpha = 0.05
    c = cutoff_powered(n, 1.0 - alpha / 3.0)
    table = fisher_table(n)
    x_t = rng.binomial(n, 0.90, size=(nsim, 3))
    x_c = np.stack([rng.binomial(n, 0.60, size=(nsim, 3)) for _ in range(4)], axis=-1)
    cp = np.all(x_t >= c, axis=1)
    p = table[x_t[:, :, None], x_c].reshape(nsim, 12)
    dyn = holm_reject_all(p, alpha)
    full = cp & dyn  # cota superior: especificidade sempre passa
    exact_cp = float(binom.sf(c - 1, n, 0.90) ** 3)
    return {
        "seed": LEGACY_SEED,
        "nsim": nsim,
        "n": n,
        "cp_cut": c,
        "exact_cp_all_3": exact_cp,
        "mc_dynamic_12": float(dyn.mean()),
        "mc_complete_upper_bound": float(full.mean()),
        "note": "R2; especificidade assumida sempre significativa; não é poder do desenho R3.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nsim", type=int, default=20000)
    parser.add_argument("--base-n", type=int, default=DEFAULT_BASE_N)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("resultados_poder.json"))
    args = parser.parse_args()
    if args.nsim < 1000:
        raise SystemExit("nsim mínimo: 1000")

    scenarios = scenario_definitions(args.base_n)
    results = []
    for index, spec in enumerate(scenarios):
        seed = MASTER_SEED + 101 * index
        print(f"RUN {spec['id']} n={spec['n']} nsim={args.nsim} seed={seed}", flush=True)
        result = run_scenario(spec, args.nsim, seed)
        results.append(result)
        print(
            f"  POWERED={result['power']['complete_powered']:.6f}; "
            f"CP={result['power']['cp_all_3']:.6f}; "
            f"24={result['power']['global_24_all']:.6f}; "
            f"neff={result['n_effective_icc']:.3f}",
            flush=True,
        )

    legacy = legacy_r2()
    payload = {
        "schema": "K06_R3_PODER_COMPLETO_SINTETICO_V1",
        "master_seed": MASTER_SEED,
        "legacy_seed": LEGACY_SEED,
        "python_numpy": np.__version__,
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "legacy_r2": legacy,
        "scenarios": results,
    }
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    args.output.write_bytes(encoded)
    print(f"LEGACY_R2 upper={legacy['mc_complete_upper_bound']:.6f}; CP_exact={legacy['exact_cp_all_3']:.6f}")
    print(f"WROTE {args.output}")
    print(f"SHA256 {sha256_bytes(encoded)}")


if __name__ == "__main__":
    main()

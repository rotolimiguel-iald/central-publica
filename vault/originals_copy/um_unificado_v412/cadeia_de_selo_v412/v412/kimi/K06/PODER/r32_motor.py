# -*- coding: utf-8 -*-
"""Núcleo R3.1: sessões individuais pareadas e inferência por clusters.

Somente simulação sintética. Nenhum modelo ou resultado experimental é chamado.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm, t as student_t

G_CLUSTERS = 27
DELTA = 0.15
ARMS = ("V2-TGL", "V2-PLA", "V2-OUT", "V2-ISO-A", "V2-ISO-B")
MASTER_SEED = 2026111501
ALPHA_BASE = 0.05
ALPHA_5SIGMA = float(norm.sf(5.0))


@dataclass(frozen=True)
class Scenario:
    sid: str
    n: int = 320
    alpha: float = ALPHA_BASE
    latent_icc: float = 0.0
    text_sd: float = 0.0
    difficulty_sd: float = 0.10
    control_level: int = 60
    focal_level: int = 90
    iso_level: int | None = None
    all_level: int | None = None
    q_targets: tuple[float, float, float, float, float] | None = None
    pair_noise: float = 0.005
    technical_loss: float = 0.005
    systemic_integrity: float = 0.99
    extractor_cap: float = 1.0
    extractor_surface_ok: bool = True


SCENARIOS = [
    Scenario("BASE_INDEPENDENTE_R32"),
    Scenario("ICC_015_TEXTO_010", latent_icc=0.15, text_sd=0.10),
    Scenario("ICC_035_TEXTO_020", latent_icc=0.35, text_sd=0.20),
    Scenario("CONTROLE_070", latent_icc=0.15, text_sd=0.10, control_level=70),
    Scenario("CONTROLE_080", latent_icc=0.15, text_sd=0.10, control_level=80),
    Scenario("NULO_GLOBAL_060", latent_icc=0.15, text_sd=0.10, all_level=60, q_targets=(0.60, 0.60, 0.60, 0.60, 0.60), systemic_integrity=1.0),
    Scenario("NULO_ESPECIFICO_090", latent_icc=0.15, text_sd=0.10, all_level=90),
    Scenario("TOST_FRONTEIRA_MAIS_075_060", latent_icc=0.15, text_sd=0.10, focal_level=75, control_level=60, q_targets=(0.75, 0.60, 0.60, 0.75, 0.75), systemic_integrity=1.0),
    Scenario("TOST_FRONTEIRA_MENOS_060_075", latent_icc=0.15, text_sd=0.10, focal_level=60, control_level=75, q_targets=(0.60, 0.75, 0.75, 0.75, 0.75), systemic_integrity=1.0),
    Scenario("EXTRATOR_TETO_POOL", extractor_cap=0.6192060638168921, extractor_surface_ok=False),
    Scenario("EXTRATOR_TETO_POR_BRACO", extractor_cap=0.09102821015130445, extractor_surface_ok=False),
    Scenario("STRESS_INTEGRIDADE", latent_icc=0.35, text_sd=0.20, control_level=70, pair_noise=0.015, technical_loss=0.03, systemic_integrity=0.90),
    Scenario("CINCO_SIGMA_N618", n=618, alpha=ALPHA_5SIGMA),
    Scenario("CINCO_SIGMA_N655", n=655, alpha=ALPHA_5SIGMA),
    Scenario("NULO_GLOBAL_ISO_FRONTEIRA", latent_icc=0.15, text_sd=0.10, focal_level=60, control_level=60, iso_level=75, q_targets=(0.60, 0.60, 0.60, 0.75, 0.75), systemic_integrity=1.0),
    Scenario("NULO_ESPECIFICO_090_N618", n=618, alpha=ALPHA_5SIGMA, all_level=90),
    Scenario("NULO_ESPECIFICO_090_N655", n=655, alpha=ALPHA_5SIGMA, all_level=90),
    Scenario("NULO_GLOBAL_ISO_FRONTEIRA_N618", n=618, alpha=ALPHA_5SIGMA, latent_icc=0.15, text_sd=0.10, focal_level=60, control_level=60, iso_level=75, q_targets=(0.60, 0.60, 0.60, 0.75, 0.75), systemic_integrity=1.0),
    Scenario("TOST_FRONTEIRA_MAIS_075_060_N618", n=618, alpha=ALPHA_5SIGMA, latent_icc=0.15, text_sd=0.10, focal_level=75, control_level=60, q_targets=(0.75, 0.60, 0.60, 0.75, 0.75), systemic_integrity=1.0),
    Scenario("TOST_FRONTEIRA_MENOS_060_075_N618", n=618, alpha=ALPHA_5SIGMA, latent_icc=0.15, text_sd=0.10, focal_level=60, control_level=75, q_targets=(0.60, 0.75, 0.75, 0.75, 0.75), systemic_integrity=1.0),
]


def q_parameters(level: int) -> tuple[float, float, float, float]:
    """p(A8), p(pré-alvo), p(efeito|pré), p(retorno|efeito)."""
    table = {
        60: (0.82, 0.99, 0.99, 0.75),
        70: (0.88, 0.99, 0.99, 0.81),
        75: (0.90, 0.99, 0.99, 0.85),
        80: (0.92, 0.99, 0.99, 0.89),
        90: (0.97, 0.99, 0.99, 0.95),
    }
    return table[level]


def cluster_layout(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cluster = np.minimum(np.arange(n) * G_CLUSTERS // n, G_CLUSTERS - 1)
    starts = np.flatnonzero(np.r_[True, cluster[1:] != cluster[:-1]])
    sizes = np.bincount(cluster, minlength=G_CLUSTERS)
    return cluster, starts, sizes


def holm_all(p: np.ndarray, alpha: float) -> np.ndarray:
    ordered = np.sort(p, axis=-1)
    m = ordered.shape[-1]
    return np.all(ordered <= alpha / (m - np.arange(m)), axis=-1)


def holm_any(p: np.ndarray, alpha: float) -> np.ndarray:
    smallest = np.min(p, axis=-1)
    return smallest <= alpha / p.shape[-1]


def exact_dp_reference(cluster_totals: np.ndarray, batch_size: int = 250) -> tuple[np.ndarray, np.ndarray]:
    """Referência DP das caudas exatas, preservada para validação/fallback."""
    nsim, tests, clusters = cluster_totals.shape
    assert tests == 4 and clusters == G_CLUSTERS
    upper = np.empty((nsim, tests), dtype=np.float64)
    lower = np.empty_like(upper)
    observed_total = cluster_totals.sum(axis=2).astype(np.int64)

    for first in range(0, nsim, batch_size):
        last = min(first + batch_size, nsim)
        totals = cluster_totals[first:last].astype(np.int32)
        b = last - first
        support = int(np.abs(totals).sum(axis=2).max())
        width = 2 * support + 1
        grid = np.arange(width, dtype=np.int32)[None, None, :]
        dist = np.zeros((b, tests, width), dtype=np.float64)
        dist[:, :, support] = 1.0
        for g in range(G_CLUSTERS):
            shift = totals[:, :, g, None]
            idx_plus = grid - shift
            valid_plus = (idx_plus >= 0) & (idx_plus < width)
            plus = np.take_along_axis(dist, np.clip(idx_plus, 0, width - 1), axis=2)
            plus *= valid_plus
            idx_minus = grid + shift
            valid_minus = (idx_minus >= 0) & (idx_minus < width)
            minus = np.take_along_axis(dist, np.clip(idx_minus, 0, width - 1), axis=2)
            minus *= valid_minus
            dist = plus + minus
        if not np.allclose(dist.sum(axis=2), 2.0 ** G_CLUSTERS, rtol=0, atol=1e-3):
            raise RuntimeError(f"Distribuição de permutação não normalizada: {dist.sum(axis=2)}")
        cdf = np.cumsum(dist, axis=2) / (2.0 ** G_CLUSTERS)
        k = observed_total[first:last] + support
        lower_values = np.take_along_axis(cdf, np.clip(k, 0, width - 1)[..., None], axis=2)[..., 0]
        upper_values = 1.0 - np.take_along_axis(cdf, np.clip(k - 1, 0, width - 1)[..., None], axis=2)[..., 0]
        lower[first:last] = np.where(k < 0, 0.0, np.where(k >= width - 1, 1.0, lower_values))
        upper[first:last] = np.where(k <= 0, 1.0, np.where(k > width - 1, 0.0, upper_values))
    return upper, lower


def exact_fft_pvalues(cluster_totals: np.ndarray, batch_size: int = 25) -> tuple[np.ndarray, np.ndarray]:
    """Caudas exatas por convolução FFT; contagens arredondadas e auditadas."""
    nsim, tests, clusters = cluster_totals.shape
    assert tests == 4 and clusters == G_CLUSTERS
    upper = np.empty((nsim, tests), dtype=np.float64)
    lower = np.empty_like(upper)
    observed_total = cluster_totals.sum(axis=2).astype(np.int64)

    for first in range(0, nsim, batch_size):
        last = min(first + batch_size, nsim)
        totals = cluster_totals[first:last].astype(np.int32)
        b = last - first
        support = int(np.abs(totals).sum(axis=2).max())
        if support == 0:
            upper[first:last] = 1.0
            lower[first:last] = 1.0
            continue
        width = 1 << (2 * support).bit_length()
        frequencies = (2.0 * np.pi * np.arange(width) / width)[None, None, None, :]
        kernel = 2.0 * np.cos(frequencies * totals[..., None])
        coefficients = np.fft.ifft(kernel.prod(axis=2), axis=2).real
        ordered = np.concatenate([coefficients[..., width - support:], coefficients[..., :support + 1]], axis=2)
        rounded = np.rint(ordered)
        error = float(np.max(np.abs(ordered - rounded)))
        if error > 1e-3:
            raise RuntimeError(f"Erro numérico FFT acima do portão: {error}")
        if not np.allclose(rounded.sum(axis=2), 2.0 ** G_CLUSTERS, rtol=0, atol=0.0):
            raise RuntimeError("FFT não preservou o número de permutações")
        cdf = np.cumsum(rounded, axis=2) / (2.0 ** G_CLUSTERS)
        k = observed_total[first:last] + support
        lower_values = np.take_along_axis(cdf, np.clip(k, 0, width - 1)[..., None], axis=2)[..., 0]
        upper_values = 1.0 - np.take_along_axis(cdf, np.clip(k - 1, 0, width - 1)[..., None], axis=2)[..., 0]
        lower[first:last] = np.where(k < 0, 0.0, np.where(k >= width - 1, 1.0, lower_values))
        upper[first:last] = np.where(k <= 0, 1.0, np.where(k > width - 1, 0.0, upper_values))
    return upper, lower


def signflip_pvalues(cluster_diff: np.ndarray, sizes: np.ndarray, batch_size: int = 25) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Superioridade, direção oposta e TOST exatos por clusters deslocados.

    A escala inteira 20D±3 representa delta=0,15 sem arredondamento.
    """
    raw_upper, raw_lower = exact_fft_pvalues(cluster_diff, batch_size)
    scaled = 20 * cluster_diff
    plus_upper, plus_lower = exact_fft_pvalues(scaled + 3 * sizes[None, None, :], batch_size)
    minus_upper, minus_lower = exact_fft_pvalues(scaled - 3 * sizes[None, None, :], batch_size)
    primary = np.column_stack([raw_upper[:, :2], plus_upper[:, 2:]])
    opposite = np.column_stack([raw_lower[:, :2], plus_lower[:, 2:]])
    tost = np.maximum(plus_upper[:, :2], minus_lower[:, :2])
    return primary, opposite, tost


def match_candidates(rng: np.random.Generator, nsim: int, n: int, spec: Scenario) -> dict:
    """Triagem de k=1; seleciona blocos completos sem ler A8/R/S posteriores."""
    candidates = int(math.ceil(n * 1.30))
    available = rng.random((nsim, candidates, 5)) >= spec.technical_loss
    d1_base = rng.uniform(0.10, 0.60, size=(nsim, candidates, 1))
    d1 = np.clip(d1_base + rng.normal(0.0, spec.pair_noise, size=(nsim, candidates, 5)), 0.0, 1.0)
    spread = d1.max(axis=2) - d1.min(axis=2)
    complete = available.all(axis=2) & (spread <= 1.0 / 24.0)
    n_complete = complete.sum(axis=1)
    order = np.argsort(~complete, axis=1, kind="stable")
    selected = order[:, :n]
    selected_valid = np.take_along_axis(complete, selected, axis=1)
    sufficient = n_complete >= n
    used = np.where(sufficient, selected[:, n - 1] + 1, candidates)
    used_mask = np.arange(candidates)[None, :] < used[:, None]
    # Mantém a contagem por simulação, sem gerar desfechos dos candidatos não usados.
    tech_per_sim = ((~available) & used_mask[..., None]).sum(axis=(1, 2))
    mismatch_per_sim = ((~(available.all(axis=2) & (spread <= 1.0 / 24.0))) & used_mask).sum(axis=1)
    d1_selected = np.take_along_axis(d1, selected[..., None].repeat(5, axis=2), axis=1)
    return {
        "selected_valid": selected_valid,
        "sufficient": sufficient,
        "used": used,
        "technical_replacements": tech_per_sim,
        "mismatch_losses": mismatch_per_sim,
        "d1_selected": d1_selected,
        "n_complete": n_complete,
    }


def generate_family(rng: np.random.Generator, nsim: int, spec: Scenario) -> dict:
    n = spec.n
    matched = match_candidates(rng, nsim, n, spec)
    valid = matched["selected_valid"]
    cluster, starts, sizes = cluster_layout(n)
    text = cluster % 3

    if spec.latent_icc > 0:
        sigma_u = math.sqrt(spec.latent_icc / (1.0 - spec.latent_icc) * (math.pi**2 / 3.0))
    else:
        sigma_u = 0.0
    cluster_u = rng.normal(0.0, sigma_u, size=(nsim, G_CLUSTERS))[:, cluster]
    d1_mean = matched["d1_selected"].mean(axis=2)
    difficulty = spec.difficulty_sd * (d1_mean - 0.35) / 0.10
    text_effects = np.zeros((nsim, 3, 5), dtype=np.float64)
    text_effects[:, :, 1:] = rng.normal(0.0, spec.text_sd, size=(nsim, 3, 4))
    # Forma explícita (simulação, bloco, braço).
    latent = (cluster_u + difficulty)[..., None] + text_effects[:, text, :]

    iso_level = spec.focal_level if spec.iso_level is None else spec.iso_level
    levels = [spec.focal_level, spec.control_level, spec.control_level, iso_level, iso_level]
    if spec.all_level is not None:
        levels = [spec.all_level] * 5
    p_a, p_pre, p_eff, p_ret = zip(*(q_parameters(level) for level in levels))
    p_a = np.minimum(np.asarray(p_a), spec.extractor_cap)
    p_pre = np.asarray(p_pre)
    p_eff = np.asarray(p_eff)
    p_ret = np.asarray(p_ret)
    if spec.q_targets is not None:
        # Fronteira marginal direta: retorno quase sempre elegível, sem alterar Q alvo.
        p_pre = np.full(5, 0.999)
        p_eff = np.full(5, 0.999)
        p_ret = np.full(5, 0.999)
        q_target = np.asarray(spec.q_targets, dtype=np.float64)
    else:
        q_target = None
    p_s = np.asarray([0.95, 0.70, 0.70, 0.95, 0.95])
    p_s = np.minimum(p_s, spec.extractor_cap)

    common = rng.normal(size=(nsim, n, 5))
    z_a = common
    z_ret = 0.60 * common + 0.80 * rng.normal(size=(nsim, n, 5))
    z_s = 0.70 * common + math.sqrt(0.51) * rng.normal(size=(nsim, n, 5))
    z_pre = rng.normal(size=(nsim, n, 5))
    z_eff = rng.normal(size=(nsim, n, 5))

    pre = z_pre < (norm.ppf(p_pre)[None, None, :] + latent)
    effect = pre & (z_eff < (norm.ppf(p_eff)[None, None, :] + latent))
    retorno = effect & (z_ret < (norm.ppf(p_ret)[None, None, :] + latent))
    if q_target is None:
        # A8 só pode ocorrer com d8=0 (PRE), nunca com NOT_APPLICABLE.
        a8 = pre & (z_a < (norm.ppf(p_a)[None, None, :] + latent))
    else:
        # P(R|latent) condiciona A8 para obter a probabilidade marginal Q alvo.
        r_prob = (
            norm.cdf(norm.ppf(p_pre)[None, None, :] + latent)
            * norm.cdf(norm.ppf(p_eff)[None, None, :] + latent)
            * norm.cdf(norm.ppf(p_ret)[None, None, :] + latent)
        )
        conditional_a8 = np.where(
            retorno,
            np.clip(q_target[None, None, :] / np.maximum(r_prob, 1e-12), 1e-12, 1.0 - 1e-12),
            np.clip(p_a, 1e-12, 1.0 - 1e-12),
        )
        a8 = pre & (z_a < norm.ppf(conditional_a8))
    s = z_s < (norm.ppf(p_s)[None, None, :] + latent)
    q = a8 & retorno

    for array in (a8, pre, effect, retorno, s, q):
        array &= valid[..., None]
    return {
        "Q": q,
        "S": s,
        "A8": a8,
        "RET": retorno,
        "PRE": pre,
        "NO_EFFECT": pre & ~effect,
        "NOT_APPLICABLE": ~pre,
        "starts": starts,
        "sizes": sizes,
        "cluster": cluster,
        **matched,
    }


def focal_intervals(q: np.ndarray, starts: np.ndarray, sizes: np.ndarray, alpha: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Intervalos t robustos por cluster; não binomial/CP com n bruto."""
    sums = np.add.reduceat(q.astype(np.float64), starts, axis=1)
    means_by_cluster = sums / sizes[None, :]
    mean = means_by_cluster.mean(axis=1)
    se = means_by_cluster.std(axis=1, ddof=1) / math.sqrt(G_CLUSTERS)
    crit_power = student_t.ppf(1.0 - alpha, G_CLUSTERS - 1)
    crit_false = student_t.ppf(1.0 - alpha / 9.0, G_CLUSTERS - 1)
    lower = mean - crit_power * se
    upper = mean + crit_false * se
    return mean, se, lower, upper


def boundary_diagnostics(spec: Scenario, families: list[dict]) -> dict | None:
    """Confere D por família/comparador com tolerância prefixada 0,005."""
    if spec.q_targets is None:
        return None
    means = np.asarray([data["Q"].mean(axis=(0, 1)) for data in families])
    targets = np.asarray(spec.q_targets)
    comparisons = []
    max_deviation = 0.0
    for family in range(3):
        for comparator in range(1, 5):
            observed = float(means[family, 0] - means[family, comparator])
            target = float(targets[0] - targets[comparator])
            deviation = abs(observed - target)
            max_deviation = max(max_deviation, deviation)
            comparisons.append({
                "family": family + 1,
                "comparator": ARMS[comparator],
                "observed_D": observed,
                "target_D": target,
                "absolute_deviation": deviation,
            })
    return {
        "tolerance_absolute_D": 0.005,
        "max_absolute_deviation": max_deviation,
        "pass": max_deviation <= 0.005,
        "comparisons": comparisons,
    }


def analyze(spec: Scenario, families: list[dict], rng: np.random.Generator) -> dict:
    nsim = families[0]["Q"].shape[0]
    n = spec.n
    p_primary = np.empty((nsim, 3, 4), dtype=np.float64)
    p_opposite = np.empty_like(p_primary)
    p_tost = np.empty((nsim, 3, 2), dtype=np.float64)
    p_manip = np.empty_like(p_primary)
    focal_mean = np.empty((nsim, 3), dtype=np.float64)
    focal_se = np.empty_like(focal_mean)
    focal_lower = np.empty_like(focal_mean)
    focal_upper = np.empty_like(focal_mean)

    for f, data in enumerate(families):
        q, s, starts, sizes = data["Q"], data["S"], data["starts"], data["sizes"]
        dq = np.add.reduceat(q[..., 0, None].astype(np.int16) - q[..., 1:].astype(np.int16), starts, axis=1).transpose(0, 2, 1)
        ds = np.add.reduceat(s[..., 0, None].astype(np.int16) - s[..., 1:].astype(np.int16), starts, axis=1).transpose(0, 2, 1)
        primary_q, opposite_q, tost_q = signflip_pvalues(dq, sizes)
        primary_s, opposite_s, tost_s = signflip_pvalues(ds, sizes)
        p_primary[:, f, :] = primary_q
        p_opposite[:, f, :] = opposite_q
        p_tost[:, f, :] = tost_q
        p_manip[:, f, :] = primary_s
        focal_mean[:, f], focal_se[:, f], focal_lower[:, f], focal_upper[:, f] = focal_intervals(q[..., 0], starts, sizes, spec.alpha)

    # Somente ISO-A/ISO-B entram na evidência primária de convergência (6 testes).
    primary_iso = p_primary[:, :, 2:]
    primary_all = holm_all(primary_iso.reshape(nsim, 6), spec.alpha)
    primary_any = holm_any(primary_iso.reshape(nsim, 6), spec.alpha)
    # PLA/OUT são diagnóstico de manipulação/contaminação, não porta de superioridade.
    manip_q_plaout_all = holm_all(p_primary[:, :, :2].reshape(nsim, 6), ALPHA_BASE)
    # A porta de integridade usa as checagens S, não rejeita uma equivalência Q verdadeira.
    manip_all = holm_all(p_manip.reshape(nsim, 12), ALPHA_BASE)
    tost_all = holm_all(p_tost.reshape(nsim, 6), spec.alpha)
    tost_any = holm_any(p_tost.reshape(nsim, 6), spec.alpha)
    # FALSIFIED: três intervalos focais + seis direções ISO.
    directional_false = np.any(p_opposite[:, :, 2:].reshape(nsim, 6) <= spec.alpha / 9.0, axis=1)
    cp_power_all = np.all(focal_lower > 0.80, axis=1)
    cp_false_any = np.any(focal_upper < 0.80, axis=1)
    falsified_raw = directional_false | cp_false_any
    powered_raw = primary_all & cp_power_all & ~falsified_raw
    nonspecific_raw = tost_all & cp_power_all & ~falsified_raw

    sufficient = np.all(np.column_stack([d["sufficient"] for d in families]), axis=1)
    logic_implications_ok = all(
        bool(np.all(data["A8"] <= data["PRE"]))
        and bool(np.all(data["RET"] <= data["PRE"]))
        and bool(np.all(data["Q"] <= data["RET"]))
        for data in families
    )
    no_effect_rate = np.stack([d["NO_EFFECT"].mean(axis=1) for d in families], axis=1)
    not_applicable_rate = np.stack([d["NOT_APPLICABLE"].mean(axis=1) for d in families], axis=1)
    manip_rate_ok = np.all((no_effect_rate <= 0.05) & (not_applicable_rate <= 0.05), axis=(1, 2))
    systemic = rng.random(nsim) < spec.systemic_integrity
    integrity = sufficient & manip_rate_ok & manip_all & systemic & spec.extractor_surface_ok

    final_nonspecific = integrity & nonspecific_raw
    final_powered = integrity & powered_raw & ~nonspecific_raw
    final_falsified = integrity & falsified_raw
    final_under = integrity & ~powered_raw & ~nonspecific_raw & ~falsified_raw
    final_inconclusive = ~integrity

    used = np.column_stack([d["used"] for d in families])
    technical = np.column_stack([d["technical_replacements"] for d in families])
    mismatches = np.column_stack([d["mismatch_losses"] for d in families])
    triage_sessions = used.sum(axis=1) * 5.0
    triage_scaled_four_families = triage_sessions * 4.0 / 3.0
    base_interactions = 20 * n * 12

    def rate(x: np.ndarray) -> float:
        return float(np.mean(x))

    def interval(p: float) -> list[float]:
        se = math.sqrt(max(p * (1 - p) / nsim, 0.0))
        return [max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se)]

    powered_p = rate(final_powered)
    nonspecific_p = rate(final_nonspecific)
    return {
        "id": spec.sid,
        "n": n,
        "alpha": spec.alpha,
        "latent_icc": spec.latent_icc,
        "text_sd": spec.text_sd,
        "difficulty_sd": spec.difficulty_sd,
        "control_level": spec.control_level,
        "focal_level": spec.focal_level,
        "iso_level": spec.iso_level,
        "all_level": spec.all_level,
        "q_targets": list(spec.q_targets) if spec.q_targets is not None else None,
        "boundary_diagnostics": boundary_diagnostics(spec, families),
        "logic_implications_A8_PRE_Q_RET": logic_implications_ok,
        "extractor_cap": spec.extractor_cap,
        "extractor_surface_ok": spec.extractor_surface_ok,
        "clusters": G_CLUSTERS,
        "analysis": "27 clusters texto-conscientes; permutação exata por sinais; t robusto focal; sem n_eff nos testes; 6 primários ISO",
        "rates": {
            "integrity_ok": rate(integrity),
            "sufficient_pairs": rate(sufficient),
            "manipulation_holm_all": rate(manip_all),
            "manipulation_q_plaout_holm_all": rate(manip_q_plaout_all),
            "manipulation_rate_gate": rate(manip_rate_ok),
            "raw_any_primary_rejection": rate(primary_any),
            "raw_all_primary": rate(primary_all),
            "raw_any_tost_rejection": rate(tost_any),
            "raw_all_tost": rate(tost_all),
            "raw_powered": rate(powered_raw),
            "powered": powered_p,
            "powered_mc95": interval(powered_p),
            "powered_given_integrity": rate(final_powered[integrity]) if integrity.any() else None,
            "raw_nonspecific": rate(nonspecific_raw),
            "nonspecific_powered": nonspecific_p,
            "nonspecific_mc95": interval(nonspecific_p),
            "nonspecific_given_integrity": rate(final_nonspecific[integrity]) if integrity.any() else None,
            "falsified": rate(final_falsified),
            "underpowered": rate(final_under),
            "inconclusive_controls": rate(final_inconclusive),
            "directional_falsified": rate(directional_false),
            "focal_interval_falsified": rate(cp_false_any),
            "raw_size_primary_given_integrity": rate(primary_any[integrity]) if integrity.any() else None,
            "raw_size_tost_given_integrity": rate(tost_any[integrity]) if integrity.any() else None,
        },
        "observed_synthetic_means": {
            "Q_by_arm": np.concatenate([d["Q"].mean(axis=(0, 1)) for d in families]).reshape(3, 5).mean(axis=0).tolist(),
            "A8_by_arm": np.concatenate([d["A8"].mean(axis=(0, 1)) for d in families]).reshape(3, 5).mean(axis=0).tolist(),
            "RET_by_arm": np.concatenate([d["RET"].mean(axis=(0, 1)) for d in families]).reshape(3, 5).mean(axis=0).tolist(),
            "S_by_arm": np.concatenate([d["S"].mean(axis=(0, 1)) for d in families]).reshape(3, 5).mean(axis=0).tolist(),
            "no_effect": rate(np.stack([d["NO_EFFECT"] for d in families])),
            "not_applicable": rate(np.stack([d["NOT_APPLICABLE"] for d in families])),
            "focal_mean": float(focal_mean.mean()),
            "focal_cluster_se_mean": float(focal_se.mean()),
        },
        "cost": {
            "base_sessions_20_cells": 20 * n,
            "base_interactions_12_calls": base_interactions,
            "triage_candidate_sessions_mean_3_families": float(triage_sessions.mean()),
            "triage_candidate_sessions_mean_scaled_4_families": float(triage_scaled_four_families.mean()),
            "pairing_extra_candidates_mean": float((used - n).sum(axis=1).mean()),
            "technical_replacements_mean": float(technical.sum(axis=1).mean()),
            "mismatch_losses_mean": float(mismatches.sum(axis=1).mean()),
            "triage_extra_k1_interactions_mean": float(max(triage_scaled_four_families.mean() - 20 * n, 0.0)),
            "base_plus_triage_interactions_mean": float(base_interactions + max(triage_scaled_four_families.mean() - 20 * n, 0.0)),
            "calibration": "SEPARADO_NAO_INCLUIDO",
            "post_output_replacements": "SEPARADO_NAO_INCLUIDO",
            "tokens": "OPEN_MODELOS_TOKENIZERS_JANELAS",
        },
        "limitations": [
            "Probabilidades de integridade e perdas são hipóteses sintéticas, não medições de provedores.",
            "O intervalo focal t por cluster não é Clopper–Pearson e sua cauda 5σ não está validada.",
            "TOST por sinais pressupõe deslocamento/simetria sob a fronteira; tamanho é medido nos dois lados.",
            "A focal é texto fixo único; efeito de texto é simulado somente nos controles/isomorfos.",
        ],
    }


def run_scenario(spec: Scenario, nsim: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    families = [generate_family(rng, nsim, spec) for _ in range(3)]
    result = analyze(spec, families, rng)
    result["seed"] = seed
    result["nsim"] = nsim
    return result

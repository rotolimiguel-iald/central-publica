#!/usr/bin/env python3
"""K04/M2 K09 — somente planejamento com agregados públicos.

Não lê vetores de eventos, não abre likelihoods, não executa teste observado e
não chama H0DN. A CDF normal e os intervalos da métrica m2 são avaliados
analiticamente. Uma quadratura de Simpson independente confere células-chave.
O snapshot REV2 só é lido para produzir o diff das células de planejamento.
"""
from __future__ import annotations

import json
import math
from datetime import date, datetime, timedelta
from pathlib import Path

STATUS = "[DERIVED—PLANEJAMENTO] agregados públicos; nenhum teste observado"
ALPHA_FINE_CODATA_2018 = 0.0072973525693
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
M2_PRED = BETA * math.sin(math.pi / 4.0) * 1000.0
DM2_PRED = (M2_PRED / 1000.0) ** 2 / 1e-5
MU_NOW = 7.388
SIGMA_NOW = 0.078
DELTA = MU_NOW - DM2_PRED
D90 = 5.0 + 1.2815515655446004
CUTOFF = date(2026, 5, 18)
K09 = Path(__file__).resolve().parents[1]
M2 = Path(__file__).resolve().parents[2]
KIMI = Path(__file__).resolve().parents[4]
OUT = K09 / "medidas"
REV2_RESULTS = M2 / "REV2" / "medidas" / "resultados_planejamento.json"


def cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def band_delta(mean: float, sd: float, sigma_future: float, t: float) -> float:
    return cdf((DM2_PRED - t * sigma_future - mean) / sd) + 1.0 - cdf(
        (DM2_PRED + t * sigma_future - mean) / sd
    )


def intervalos_m2(t: float, sigma_future: float) -> dict:
    """Região r>=t em massa, com as duas caudas de |m-M|.

    Inferior: L<=m<=U, se o discriminante for não negativo.
    Superior: m>=H. Nenhuma dessas regiões é m<=L.
    """
    disc = M2_PRED**2 - 20.0 * t * sigma_future
    low = high_lower = None
    if disc >= 0.0:
        root = math.sqrt(disc)
        low = (M2_PRED - root) / 2.0
        high_lower = (M2_PRED + root) / 2.0
    high = (M2_PRED + math.sqrt(M2_PRED**2 + 20.0 * t * sigma_future)) / 2.0
    return {"low": low, "high_lower": high_lower, "high": high}


def band_m2(mean: float, sd: float, sigma_future: float, t: float) -> float:
    q = intervalos_m2(t, sigma_future)
    lower = 0.0
    if q["low"] is not None:
        x_low = q["low"] ** 2 / 10.0
        x_high_lower = q["high_lower"] ** 2 / 10.0
        lower = cdf((x_high_lower - mean) / sd) - cdf((x_low - mean) / sd)
    x_high = q["high"] ** 2 / 10.0
    return lower + 1.0 - cdf((x_high - mean) / sd)


def band_m2_simpson(mean: float, sd: float, sigma_future: float, t: float) -> float:
    """Conferência independente: integra diretamente a densidade induzida em m."""
    q = intervalos_m2(t, sigma_future)

    def density(m: float) -> float:
        x = m * m / 10.0
        return math.exp(-0.5 * ((x - mean) / sd) ** 2) * m / (5.0 * math.sqrt(2.0 * math.pi) * sd)

    def integral(a: float, b: float, n: int = 20000) -> float:
        if b <= a:
            return 0.0
        h = (b - a) / n
        total = density(a) + density(b)
        total += 4.0 * sum(density(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1))
        total += 2.0 * sum(density(a + 2 * i * h) for i in range(1, n // 2))
        return total * h / 3.0

    mean_m = math.sqrt(10.0 * mean)
    sd_m_approx = 5.0 * sd / mean_m
    right = max(q["high"] + 1.0, mean_m + 14.0 * sd_m_approx)
    lower = 0.0 if q["low"] is None else integral(q["low"], q["high_lower"])
    return lower + integral(q["high"], right)


def probabilities(mean: float, predictive_sd: float, sigma_future: float, metric: str) -> dict:
    if predictive_sd <= 0.0:
        raise ValueError("predictive_sd deve ser positivo")
    band = band_delta if metric == "delta" else band_m2
    ge1 = band(mean, predictive_sd, sigma_future, 1.0)
    ge3 = band(mean, predictive_sd, sigma_future, 3.0)
    ge5 = band(mean, predictive_sd, sigma_future, 5.0)
    return {
        "mean": mean,
        "predictive_sd": predictive_sd,
        "P_r_le_1": 1.0 - ge1,
        "P_1_lt_r_lt_3": ge1 - ge3,
        "P_r_lt_3": 1.0 - ge3,
        "P_3_le_r_lt_5": ge3 - ge5,
        "P_r_ge_5": ge5,
    }


def frozen_r(mu: float, sigma: float) -> float:
    mass = math.sqrt(10.0 * mu)
    sigma_mass = 0.5 * (sigma / mu) * mass
    return abs(mass - M2_PRED) / sigma_mass


def delta_r(mu: float, sigma: float) -> float:
    return abs(mu - DM2_PRED) / sigma


def frozen_D(mu: float, sigma: float) -> float:
    mass = math.sqrt(10.0 * mu)
    return mass * abs(mass - M2_PRED) / (5.0 * sigma)


def sigma_for_5(mu: float) -> float:
    mass = math.sqrt(10.0 * mu)
    return 2.0 * mu * abs(mass - M2_PRED) / (5.0 * mass)


def add_days(day: date, amount: float) -> str:
    return (day + timedelta(days=amount)).isoformat()


def independent_model(sigma: float, truth: str, metric: str) -> dict:
    if truth == "posterior_publico":
        return probabilities(MU_NOW, math.hypot(SIGMA_NOW, sigma), sigma, metric)
    if truth == "verdade_previsao":
        return probabilities(DM2_PRED, sigma, sigma, metric)
    raise ValueError(truth)


def cumulative_model(sigma: float, truth: str, metric: str, covariance: float) -> dict:
    variance = SIGMA_NOW**2 + sigma**2 - 2.0 * covariance
    if variance <= 0.0:
        raise ValueError("variância cumulativa não positiva")
    if truth == "posterior_publico":
        return probabilities(MU_NOW, math.sqrt(variance), sigma, metric)
    if truth == "verdade_previsao_condicional":
        mean = DM2_PRED + (covariance / SIGMA_NOW**2) * DELTA
        conditional_variance = sigma**2 - covariance**2 / SIGMA_NOW**2
        if conditional_variance <= 0.0:
            raise ValueError("variância condicional não positiva")
        return probabilities(mean, math.sqrt(conditional_variance), sigma, metric)
    raise ValueError(truth)


PRECISIONS = [
    ("0,7 %", 0.007 * MU_NOW),
    ("0,5 %", 0.005 * MU_NOW),
    ("0,407121 %", 0.00407121 * MU_NOW),
    ("0,324061 %", 0.00324061 * MU_NOW),
    ("0,3 %", 0.003 * MU_NOW),
    ("Tabela 6, σ = 0,024", 0.024),
]
MODELS = [
    ("independente", "posterior_publico", "(a1) Independente — posterior público"),
    ("independente", "verdade_previsao", "(a2) Independente — verdade = previsão"),
    ("cumulativo_C_igual_s2_brinquedo", "posterior_publico", "(b1) Cumulativo C=s² — posterior público; brinquedo"),
    ("cumulativo_C_igual_s2_brinquedo", "verdade_previsao_condicional", "(b2) Cumulativo C=s² — verdade=previsão condicionada; brinquedo"),
]
PROB_KEYS = ["P_r_le_1", "P_1_lt_r_lt_3", "P_r_lt_3", "P_3_le_r_lt_5", "P_r_ge_5"]
LABELS = {
    "P_r_le_1": "P(r≤1)",
    "P_1_lt_r_lt_3": "P(1<r<3)",
    "P_r_lt_3": "P(r<3)",
    "P_3_le_r_lt_5": "P(3≤r<5)",
    "P_r_ge_5": "P(r≥5), m₂",
    "P_delta_ge_5": "PΔ(r≥5)",
}


def make_outcomes() -> list[dict]:
    rows = []
    for label, sigma in PRECISIONS:
        row = {
            "precisao": label,
            "sigma": sigma,
            "D_delta_centro_planejamento": DELTA / sigma,
            "D_m2_centro_planejamento": frozen_D(MU_NOW, sigma),
            "D_delta_ao_menos_5": DELTA / sigma >= 5.0,
            "independente": {},
            "cumulativo_C_igual_s2_brinquedo": {},
            "covariancia_real": "OPEN",
        }
        for truth in ("posterior_publico", "verdade_previsao"):
            row["independente"][truth] = {
                metric: independent_model(sigma, truth, metric) for metric in ("delta", "m2")
            }
        for truth in ("posterior_publico", "verdade_previsao_condicional"):
            row["cumulativo_C_igual_s2_brinquedo"][truth] = {
                metric: cumulative_model(sigma, truth, metric, sigma**2) for metric in ("delta", "m2")
            }
        rows.append(row)
    return rows


def make_increment_years() -> list[dict]:
    rows = []
    for years in (1, 2, 3):
        days = 365.25 * years
        sigma = SIGMA_NOW * math.sqrt(207.2 / days)
        rows.append({
            "anos_novos": years,
            "dias_novos": days,
            "sigma_incremento_sem_piso": sigma,
            "D_delta_centro_planejamento": DELTA / sigma,
            "D_m2_centro_planejamento": frozen_D(MU_NOW, sigma),
            "posterior_publico": {
                metric: independent_model(sigma, "posterior_publico", metric)
                for metric in ("delta", "m2")
            },
            "verdade_previsao": {
                metric: independent_model(sigma, "verdade_previsao", metric)
                for metric in ("delta", "m2")
            },
            "data_ideal_5sigma": "2030-03-11",
            "data_ideal_D90": "2032-05-25",
            "piso_dois_pontos_inalcancavel": True,
        })
    return rows


def make_performance() -> dict:
    sigma_59, sigma_207 = 0.12, 0.078
    t_59, t_207 = 59.1, 207.2
    sigma5 = DELTA / 5.0
    sigma_d90 = DELTA / D90
    information = t_207 * sigma_207**2
    no_floor = {}
    duty = t_207 / 265.0
    mass_now = math.sqrt(10.0 * MU_NOW)
    mass_gap = abs(mass_now - M2_PRED)

    def calendar_entry(alvo: str, k: float, metrica: str) -> dict:
        if metrica == "delta":
            target = DELTA / k
        elif metrica == "m2":
            target = mass_now * mass_gap / (5.0 * k)
        else:
            raise ValueError(metrica)
        total = information / target**2
        return {
            "alvo": alvo,
            "metrica": metrica,
            "sigma_alvo_delta_m2_21": target,
            "dias_totais_cumulativos": total,
            "dias_adicionais_cumulativos": total - t_207,
            "data_ideal_cumulativa_apos_corte": add_days(CUTOFF, total - t_207),
            "dias_novos_somente_incremento": total,
            "data_ideal_incremento_apos_corte": add_days(CUTOFF, total),
            "dias_calendario_cumulativos_duty_cenario": (total - t_207) / duty,
            "data_cumulativa_duty_cenario": add_days(CUTOFF, (total - t_207) / duty),
            "dias_calendario_incremento_duty_cenario": total / duty,
            "data_incremento_duty_cenario": add_days(CUTOFF, total / duty),
        }

    for name, target in (("5sigma", sigma5), ("D90", sigma_d90)):
        no_floor[name] = calendar_entry(name, 5.0 if name == "5sigma" else D90, "delta")
    por_metrica = []
    for alvo, k in (("5sigma", 5.0), ("D90", D90), ("r_3", 3.0)):
        for metrica in ("delta", "m2"):
            por_metrica.append(calendar_entry(alvo, k, metrica))
    total_3sigma = information / (DELTA / 3.0) ** 2
    tensao_3sigma = {
        "sigma_alvo": DELTA / 3.0,
        "dias_novos_somente_incremento": total_3sigma,
        "data_ideal_incremento_apos_corte": add_days(CUTOFF, total_3sigma),
        "dias_adicionais_cumulativos": total_3sigma - t_207,
        "data_ideal_cumulativa_apos_corte": add_days(CUTOFF, total_3sigma - t_207),
    }
    a_two = (sigma_207**2 - sigma_59**2) / (1.0 / t_207 - 1.0 / t_59)
    floor_two = math.sqrt(sigma_207**2 - a_two / t_207)
    return {
        "sem_piso_desde_207": no_floor,
        "sem_piso_por_metrica": por_metrica,
        "tensao_3sigma_sem_piso": tensao_3sigma,
        "duty_cycle_cenario": duty,
        "piso_ilustrativo_dois_pontos_reais": {
            "a": a_two,
            "s0": floor_two,
            "5sigma_alcancavel": sigma5 >= floor_two,
            "D90_alcancavel": sigma_d90 >= floor_two,
        },
        "SK_Gd_cenario_sqrtT": {
            "exposicao_atual_dias": 411.52,
            "sigma_atual_lado_previsao": 0.54,
            "sigma5": sigma_for_5(9.08),
            "dias_totais": 411.52 * (0.54 / sigma_for_5(9.08)) ** 2,
            "dias_adicionais": 411.52 * (0.54 / sigma_for_5(9.08)) ** 2 - 411.52,
            "data_brinquedo_desde_arxiv": add_days(date(2026, 10, 2), 411.52 * (0.54 / sigma_for_5(9.08)) ** 2 - 411.52),
            "pressuposto_anomalia_persiste": True,
        },
    }


def make_increment_59_207() -> dict:
    mu1, s1, mu2, s2 = 7.50, 0.12, MU_NOW, SIGMA_NOW
    w1, w2 = 1.0 / s1**2, 1.0 / s2**2
    dw = w2 - w1
    mu_increment = (w2 * mu2 - w1 * mu1) / dw
    sigma_increment = 1.0 / math.sqrt(dw)
    return {
        "centro_ilustrativo": mu_increment,
        "sigma_ilustrativo": sigma_increment,
        "r_delta_contra_previsao": delta_r(mu_increment, sigma_increment),
        "r_m2_contra_previsao": frozen_r(mu_increment, sigma_increment),
        "distancia_ao_centro_59_sigma_correta_aninhamento": abs(mu_increment - mu1) / math.hypot(sigma_increment, s1),
        "distancia_ao_centro_59_sigma_incorreta_so_incremento": abs(mu_increment - mu1) / sigma_increment,
        "formula_equivalente": abs(mu2 - mu1) / math.sqrt(s1**2 - s2**2),
    }


def make_witnesses() -> list[dict]:
    raw = [
        ("JUNO_207d", 7.388, 0.078, 0.078, "arXiv:2609.37895v1"),
        ("SNO_plus", 7.91, 0.22, 0.25, "arXiv:2511.11856v4; PRL 137, 101807"),
        ("SK_Gd_reator", 9.08, 0.55, 0.54, "arXiv:2610.03143v1"),
        ("KamLAND", 7.54, 0.19, 0.18, "arXiv:1303.4667v2, Tabela 3"),
        ("Solares_sem_KamLAND", 6.10, 0.95, 0.81, "arXiv:2312.12907v2; PRD 109, 092001"),
        ("JUNO_59d_subset", 7.50, 0.12, 0.12, "arXiv:2511.14593v1; DOI 10.1038/s41586-026-10538-z"),
        ("NuFIT_6_1_tabela", 7.537, 0.094, 0.10, "NuFIT 6.1, node 309, tabela de parâmetros"),
        ("NuFIT_6_1_artigo_eq11", 7.530, 0.096, 0.097, "arXiv:2601.09791v1/v2, eq. 11"),
        ("Capozzi_2025", 7.48, 0.10, 0.10, "arXiv:2511.21650"),
        ("Bari_2026a_NO", 7.465, 0.072, 0.080, "Global-nu release 2026.a"),
        ("SK_Gd_solar_reator", 8.94, 0.46, 0.47, "arXiv:2610.03143v1"),
        ("SNO_plus_reator_solar_final", 7.59, 0.17, 0.17, "arXiv:2511.11856v4, Tabela 3"),
    ]
    rows = []
    for sid, mu, err_plus, err_minus, source in raw:
        # Usa o erro no lado que aponta para a previsão, nos dois sentidos.
        sigma = err_minus if mu >= DM2_PRED else err_plus
        rows.append({
            "id": sid,
            "centro": mu,
            "erro_mais": err_plus,
            "erro_menos": err_minus,
            "sigma_lado_previsao": sigma,
            "r_frozen_m2": frozen_r(mu, sigma),
            "r_delta": delta_r(mu, sigma),
            "sigma_necessario_5_m2": sigma_for_5(mu),
            "ID_primario": source,
        })
    return rows


def matched_le_1(mean: float, sd: float, sigma: float) -> float:
    return 1.0 - band_m2(mean, sd, sigma, 1.0)


def make_joint_matched(witnesses: list[dict]) -> list[dict]:
    direct = {"SNO_plus", "SK_Gd_reator", "KamLAND", "Solares_sem_KamLAND"}
    p_le1 = matched_le_1(MU_NOW, SIGMA_NOW, SIGMA_NOW)
    rows = []
    for item in witnesses:
        sid = item["id"]
        if sid in direct:
            s_le1 = matched_le_1(item["centro"], item["sigma_lado_previsao"], item["sigma_lado_previsao"])
            rows.append({
                "id": sid,
                "P_rP_le_1": p_le1,
                "P_rS_le_1": s_le1,
                "P_matched_conjunta_C0_brinquedo": p_le1 * s_le1,
                "C_PS_real": "OPEN",
            })
        else:
            rows.append({
                "id": sid,
                "P_rP_le_1": p_le1,
                "P_rS_le_1": None,
                "P_matched_conjunta_C0_brinquedo": None,
                "C_PS_real": "OPEN",
            })
    return rows


def pct(x: float, digits: int = 6) -> str:
    return f"{100*x:.{digits}f} %".replace(".", ",")


def num(x: float, digits: int = 6) -> str:
    return f"{x:.{digits}f}".replace(".", ",")


def outcome_markdown(rows: list[dict], model: str, truth: str, title: str) -> list[str]:
    lines = [
        f"### {title}",
        "",
        "| Precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) | DΔ≥5 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for row in rows:
        probs = row[model][truth]
        lines.append(
            f"| {row['precisao']} | {num(row['sigma'])} | {num(row['D_delta_centro_planejamento'])} | "
            f"{num(row['D_m2_centro_planejamento'])} | {pct(probs['m2']['P_r_le_1'])} | "
            f"{pct(probs['m2']['P_1_lt_r_lt_3'])} | {pct(probs['m2']['P_r_lt_3'])} | "
            f"{pct(probs['m2']['P_3_le_r_lt_5'])} | {pct(probs['m2']['P_r_ge_5'])} | "
            f"{pct(probs['delta']['P_r_ge_5'])} | {'sim' if row['D_delta_ao_menos_5'] else 'não'} |"
        )
    lines.append("")
    return lines


def increment_markdown(rows: list[dict]) -> str:
    lines = [
        "# Incremento JUNO depois de 18/05/2026 — cenários de planejamento K09",
        "",
        "Somente dado novo, sem piso: σ(T)=0,078√(207,2/T). Posterior público: N(7,388; 0,078²+s²); verdade=previsão: N(Δpred; s²).",
        "",
    ]
    for hypothesis, title in (("posterior_publico", "Posterior público"), ("verdade_previsao", "Verdade = previsão")):
        lines += [
            f"## {title}",
            "",
            "| Dado novo | s | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(r<3) | P(3≤r<5) | P(r≥5), m₂ | PΔ(r≥5) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            probs = row[hypothesis]
            lines.append(
                f"| {row['anos_novos']} ano(s) = {num(row['dias_novos'], 2)} d | {num(row['sigma_incremento_sem_piso'])} | "
                f"{num(row['D_delta_centro_planejamento'])} | {num(row['D_m2_centro_planejamento'])} | "
                f"{pct(probs['m2']['P_r_le_1'])} | {pct(probs['m2']['P_1_lt_r_lt_3'])} | "
                f"{pct(probs['m2']['P_r_lt_3'])} | {pct(probs['m2']['P_3_le_r_lt_5'])} | "
                f"{pct(probs['m2']['P_r_ge_5'])} | {pct(probs['delta']['P_r_ge_5'])} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def calendar_markdown(rows: list[dict]) -> str:
    labels = {"delta": "Δm²", "m2": "m₂"}
    lines = [
        "# Calendário sem piso — métricas Δm² e m₂ lado a lado",
        "",
        "Brinquedo de exposição desde 18/05/2026: σ(T)=0,078√(207,2/T), centro parado, 100 % de dias vivos. As datas não são cronogramas.",
        "",
        "| Alvo | Métrica | σ alvo | T cumulativo (d) | Data cumulativa | Dias novos | Data incremento |",
        "|---|---|---:|---:|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['alvo']} | {labels[row['metrica']]} | {num(row['sigma_alvo_delta_m2_21'])} | "
            f"{num(row['dias_totais_cumulativos'], 3)} | {row['data_ideal_cumulativa_apos_corte']} | "
            f"{num(row['dias_novos_somente_incremento'], 3)} | {row['data_ideal_incremento_apos_corte']} |"
        )
    lines += [
        "",
        "Cenário de duty cycle (207,2/265), sem valor de previsão:",
        "",
        "| Alvo | Métrica | Data cumulativa | Data incremento |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['alvo']} | {labels[row['metrica']]} | {row['data_cumulativa_duty_cenario']} | {row['data_incremento_duty_cenario']} |")
    lines.append("")
    return "\n".join(lines)


def make_diff(rows: list[dict], matched: list[dict]) -> str:
    lines = [
        "# Diff célula a célula — R3 (REV2) contra K09",
        "",
        "Δpp = 100×(K09−R3) em pontos percentuais. P(r<3) não existia como coluna separada na R3 e é emitida como nova.",
        "",
    ]
    old = json.loads(REV2_RESULTS.read_text(encoding="utf-8"))
    for model, truth, title in MODELS:
        lines += [f"## {title}", "", "| Precisão | Célula | R3 | K09 | Δpp |", "|---|---|---:|---:|---:|"]
        for idx, row in enumerate(rows):
            old_probs = old["desfechos"][idx][model][truth]
            new_probs = row[model][truth]
            for key in PROB_KEYS:
                old_value = None
                if key == "P_r_lt_3":
                    old_value = old_probs["m2"]["P_r_le_1"] + old_probs["m2"]["P_1_lt_r_lt_3"]
                else:
                    old_value = old_probs["m2"][key]
                new_value = new_probs["m2"][key]
                delta_pp = 100.0 * (new_value - old_value)
                old_text = "derivada" if key == "P_r_lt_3" else pct(old_value)
                lines.append(f"| {row['precisao']} | {LABELS[key]} | {old_text} | {pct(new_value)} | {delta_pp:+.6f} |")
            key = "P_r_ge_5"
            old_value = old_probs["delta"][key]
            new_value = new_probs["delta"][key]
            lines.append(f"| {row['precisao']} | {LABELS['P_delta_ge_5']} | {pct(old_value)} | {pct(new_value)} | {100*(new_value-old_value):+.6f} |")
        lines.append("")
    old_match = {row["id"]: row for row in old["matched_conjunta"]}
    lines += ["## MATCHED — brinquedo C=0", "", "| S | Célula | R3 | K09 | Δpp |", "|---|---|---:|---:|---:|"]
    old_p = old["matched_conjunta"][0]["P_rP_le_1"]
    new_p = matched[0]["P_rP_le_1"]
    lines.append(f"| comum | P(rP≤1) | {pct(old_p)} | {pct(new_p)} | {100*(new_p-old_p):+.6f} |")
    lines.append("| todas as linhas OPEN | P(rS≤1) e P(MATCHED) | OPEN | OPEN | inalterado |")
    for row in matched:
        if row["P_rS_le_1"] is None:
            continue
        old_row = old_match[row["id"]]
        for key, label in (("P_rS_le_1", "P(rS≤1)"), ("P_matched_conjunta_C0_brinquedo", "P(MATCHED), C=0")):
            old_value = old_row[key]
            new_value = row[key]
            lines.append(f"| {row['id']} | {label} | {pct(old_value)} | {pct(new_value)} | {100*(new_value-old_value):+.6f} |")
    lines.append("")
    return "\n".join(lines)


def determination(mu: float, err_plus: float, err_minus: float, **kwargs) -> dict:
    sigma = err_minus  # todos os centros usados estão acima de DM2_PRED
    return {
        **kwargs,
        "valor_1e-5_eV2": mu,
        "erro_mais_1e-5_eV2": err_plus,
        "erro_menos_1e-5_eV2": err_minus,
        "sigma_lado_previsao_1e-5_eV2": sigma,
        "r_m2": frozen_r(mu, sigma),
        "r_delta_m2_21": delta_r(mu, sigma),
    }


def make_errata_data() -> dict:
    juno207 = determination(
        7.388, 0.078, 0.078,
        id="JUNO_207_2_dias",
        exposicao_dias_efetivos=207.2,
        janela_dados_fim="2026-05-18",
        primeira_apresentacao_publica={
            "data": "2026-06-22",
            "evento": "Neutrino 2026",
            "identificador": "indico.global/event/15740/contributions/155563",
            "anexo": "72452/141000/JUNO-Neutrino2026-Vfinal.pdf",
            "estatuto": "DECLARADO_sem_resposta_crua_guardada",
        },
        primeira_confirmacao_explicita_do_valor={
            "data": "2026-07-15",
            "identificador": "indico.ihep.ac.cn/event/28557/contributions/223278",
            "anexo": "104657/141297/July2026_v2.pdf",
        },
        noticia_secundaria={"data": "2026-07-22", "identificador": "dlnp.jinr.ru/en/news/3850"},
        artigo={"data": "2026-09-29", "identificador": "arXiv:2609.37895v1"},
        posicao_relativa_a_previsao_publicada="posterior_ao_valor_publicado",
        posicao_relativa_ao_pino="anterior",
        posicao_relativa_ao_pino_do_artigo="posterior",
    )
    return {
        "schema": "errata.neutrino.v412.dados.k09.v1",
        "unidade_delta_m2_21": "1e-5 eV^2",
        "unidade_m2": "meV",
        "previsao": {
            "alpha_fine_CODATA_2018": ALPHA_FINE_CODATA_2018,
            "beta": BETA,
            "E0_eV": 1.0,
            "m1_eV": 0.0,
            "m2_TGL_meV": M2_PRED,
            "delta_m2_21_TGL_1e-5_eV2": DM2_PRED,
        },
        "previsao_publicada": {
            "tese_neutrino_2025": [
                {"data": "2025-10-16", "doi": "10.5281/zenodo.17372599", "valor_8_51_presente": False},
                {"data": "2025-11-04", "doi": "10.5281/zenodo.17526619", "valor_8_51_presente": False},
            ],
            "valor_8_51_no_acervo": {
                "data": "2026-01-22",
                "identificador": "C:/IALD/Artigo/complemento ao manifesto.docx",
                "sha256": "83ba9e814a63810d2c80cd7026f733e6b534aaf72de7f6129d5ddded23a031f6",
            },
            "publicacao_zenodo": {
                "publication_date": "2026-02-17",
                "created": "2026-02-20T18:06:33.110533+00:00",
                "doi": "10.5281/zenodo.18674475",
                "identificador_local": "A_fronteira_v5.pdf",
                "sha256_local": "f41506234d72086c9eab929b01f9ed35c8f1f52bc6f33f2778475adadd9cba48",
            },
        },
        "pinos": {
            "data_do_congelamento": "2026-08-08",
            "frozen_hash_objeto_congelado": "4bdae22a277aa393094a1bf416db12a5e782b673e9e9b3ddd6a2fb8c7a64075c",
            "sha256_arquivo_regra_py": "2564d7c944f1d338d0bafb96a294a2bdc97fdd617f36c1d5511db5ca868771f0",
            "sha256_arquivo_resultado_json": "6f0963a54b7d2f5a68b711f77beb9d743448d44443d7b4ebb06ba0cf1817239b",
            "sha256_dicionario_portado": "e24877751ad810225412cc294c06b83eefeaedc67e4c5cabc7779ac01e4b19c3",
            "identificador_resultado": "02_frozen_neutrino_m2_v2_resultado.json",
        },
        "degraus_juno": [
            determination(
                7.50, 0.12, 0.12,
                id="JUNO_59_1_dias",
                exposicao_dias_efetivos=59.1,
                primeira_apresentacao_publica={"data": "2025-11-18", "identificador": "arXiv:2511.14593v1"},
                apresentacao_em_coletiva={"data": "2025-11-19", "identificador": "IHEP/JUNO, Jiangmen"},
                artigo={"data": "2026-06-10", "identificador": "Nature 654, 343–348; DOI 10.1038/s41586-026-10538-z"},
                posicao_relativa_a_previsao_publicada="anterior_ao_valor_publicado",
                posicao_relativa_ao_pino="anterior",
            ),
            juno207,
        ],
        "ajustes_globais": [
            determination(
                7.537, 0.094, 0.10,
                id="NuFIT_6_1_tabela",
                dados_de_referencia="2025-11",
                primeira_apresentacao_publica={"data": None, "identificador": "nu-fit.org/node/309", "status_data": "OPEN"},
                artigo={"data": None, "identificador": "v61.release-notes.pdf; tabela de parâmetros do node 309"},
            ),
            determination(
                7.530, 0.096, 0.097,
                id="NuFIT_6_1_artigo_eq11",
                primeira_apresentacao_publica={"data": "2026-01-14", "identificador": "arXiv:2601.09791v1, eq. 11"},
                artigo={"data": "2026-04-12", "identificador": "arXiv:2601.09791v2, eq. 11"},
                representacao_simetrica_arredondada={
                    "sigma_1e-5_eV2": 0.10,
                    "r_m2": frozen_r(7.530, 0.10),
                    "r_delta_m2_21": delta_r(7.530, 0.10),
                },
            ),
        ],
        "segunda_testemunha": determination(
            9.08, 0.55, 0.54,
            id="SK_Gd_reator",
            exposicao_dias_efetivos=411.52,
            primeira_apresentacao_publica={"data": "2026-10-02", "identificador": "arXiv:2610.03143v1", "escopo": "primeira_localizada"},
            artigo={"data": "2026-10-02", "identificador": "arXiv:2610.03143v1"},
            distancia_ao_JUNO_207_sigma=(9.08 - 7.388) / math.sqrt(0.54**2 + 0.078**2),
            cenario_sqrtT={
                "sigma5_1e-5_eV2": sigma_for_5(9.08),
                "dias_totais": 411.52 * (0.54 / sigma_for_5(9.08)) ** 2,
                "dias_adicionais": 411.52 * (0.54 / sigma_for_5(9.08)) ** 2 - 411.52,
                "pressuposto_anomalia_persiste": True,
            },
        ),
        "incremento_59_207_ilustrativo": make_increment_59_207(),
        "fontes_rota": {
            "rota": "neutrinos.m2.normalizacao",
            "sequencias": [93, 142],
        },
    }


def validate(rows: list[dict], years: list[dict], matched: list[dict]) -> dict:
    for row in rows:
        for model, truth, _ in MODELS:
            for metric in ("delta", "m2"):
                p = row[model][truth][metric]
                total = p["P_r_le_1"] + p["P_1_lt_r_lt_3"] + p["P_3_le_r_lt_5"] + p["P_r_ge_5"]
                assert math.isclose(total, 1.0, rel_tol=0.0, abs_tol=4e-12)
                assert math.isclose(p["P_r_lt_3"], p["P_r_le_1"] + p["P_1_lt_r_lt_3"], rel_tol=0.0, abs_tol=4e-12)
    for sigma in (0.007 * MU_NOW, 0.024, 0.0587):
        p = independent_model(sigma, "verdade_previsao", "m2")
        # A regra propaga sigma_m2 em primeira ordem no valor observado;
        # os benchmarks públicos são dados a duas casas percentuais.
        assert round(100.0 * p["P_r_le_1"], 2) == round(100.0 * (1.0 - 2.0 * (1.0 - cdf(1.0))), 2)
        assert round(100.0 * p["P_1_lt_r_lt_3"], 2) == round(100.0 * (2.0 * (cdf(3.0) - cdf(1.0))), 2)
        assert round(100.0 * p["P_r_lt_3"], 2) == round(100.0 * (2.0 * cdf(3.0) - 1.0), 2)
        assert math.isclose(band_m2_simpson(DM2_PRED, sigma, sigma, 3.0), band_m2(DM2_PRED, sigma, sigma, 3.0), abs_tol=5e-8)
    p0 = rows[0]["independente"]["posterior_publico"]["m2"]
    assert math.isclose(band_m2_simpson(p0["mean"], p0["predictive_sd"], rows[0]["sigma"], 1.0), 1.0 - p0["P_r_le_1"], abs_tol=5e-8)
    solar = next(row for row in matched if row["id"] == "Solares_sem_KamLAND")
    assert math.isclose(solar["P_matched_conjunta_C0_brinquedo"], 0.0735, abs_tol=5e-5)
    nufit = frozen_r(7.537, 0.10)
    assert 3.023 < nufit < 3.025
    inc = make_increment_59_207()
    assert math.isclose(inc["distancia_ao_centro_59_sigma_correta_aninhamento"], 1.228, abs_tol=0.001)
    return {
        "soma_das_faixas": "OK",
        "benchmark_verdade_previsao_P_r_le_1": 1.0 - 2.0 * (1.0 - cdf(1.0)),
        "benchmark_verdade_previsao_P_1_lt_r_lt_3": 2.0 * (cdf(3.0) - cdf(1.0)),
        "benchmark_verdade_previsao_P_r_lt_3": 2.0 * cdf(3.0) - 1.0,
        "quadratura_Simpson_independente": "OK",
        "matched_solares": solar["P_matched_conjunta_C0_brinquedo"],
        "nufit_tabela_r_m2": nufit,
        "incremento_sigma": inc["distancia_ao_centro_59_sigma_correta_aninhamento"],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = make_outcomes()
    years = make_increment_years()
    witnesses = make_witnesses()
    matched = make_joint_matched(witnesses)
    checks = validate(rows, years, matched)
    payload = {
        "estatuto": STATUS,
        "metodo": "CDF analítica em duas caudas; quadratura Simpson de conferência; sem simulação",
        "m2_pred_meV": M2_PRED,
        "dm2_pred": DM2_PRED,
        "delta_centro": DELTA,
        "D90": D90,
        "desfechos": rows,
        "incremento_1_2_3_anos": years,
        "desempenho": make_performance(),
        "incremento_59_207": make_increment_59_207(),
        "testemunhas": witnesses,
        "matched_conjunta": matched,
        "validacoes": checks,
        "covariancias_reais": "OPEN; C=0 e C=s² somente brinquedos",
    }
    (OUT / "resultados_planejamento_k09.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tables = [
        "# Tabelas calculadas — K04/M2 K09",
        "",
        STATUS + ". Módulo correto em m₂; Δm² apenas como comparação.",
        "",
        f"m₂ = {M2_PRED:.12f} meV; Δpred = {DM2_PRED:.12f}; Δcentro = {DELTA:.12f}; D90 = {D90:.12f}.",
        "",
    ]
    for model, truth, title in MODELS:
        tables += outcome_markdown(rows, model, truth, title)
    tables += ["## MATCHED — brinquedo C=0", "", "| S | P(rP≤1) | P(rS≤1) | P(MATCHED), C=0 |", "|---|---:|---:|---:|"]
    for row in matched:
        joint = row["P_matched_conjunta_C0_brinquedo"]
        tables.append(f"| {row['id']} | {pct(row['P_rP_le_1'])} | {'OPEN' if row['P_rS_le_1'] is None else pct(row['P_rS_le_1'])} | {'OPEN' if joint is None else pct(joint)} |")
    tables.append("")
    tables += ["## Determinações públicas — m₂ e Δm² ao lado", "", "| id | centro | erro + | erro − | σ lado previsão | r_m₂ | r_Δ | σ para 5σ | fonte |", "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for row in witnesses:
        tables.append(
            f"| {row['id']} | {num(row['centro'], 3)} | {num(row['erro_mais'], 3)} | {num(row['erro_menos'], 3)} | "
            f"{num(row['sigma_lado_previsao'], 3)} | {num(row['r_frozen_m2'])} | {num(row['r_delta'])} | "
            f"{num(row['sigma_necessario_5_m2'])} | {row['ID_primario']} |"
        )
    tables.append("")
    (OUT / "tabelas_planejamento_k09.md").write_text("\n".join(tables), encoding="utf-8")
    (OUT / "mudancas_celulas_k09.md").write_text(make_diff(rows, matched), encoding="utf-8")
    (OUT / "incremento_1a3_anos_k09.md").write_text(increment_markdown(years), encoding="utf-8")
    (OUT / "calendario_metricas_duplas_k09.md").write_text(
        calendar_markdown(payload["desempenho"]["sem_piso_por_metrica"]), encoding="utf-8"
    )
    (KIMI / "ERRATA_NEUTRINO_V412_DADOS_K09.json").write_text(json.dumps(make_errata_data(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "status": STATUS,
        "teste_observado_executado": False,
        "arquivos": [
            "resultados_planejamento_k09.json",
            "tabelas_planejamento_k09.md",
            "mudancas_celulas_k09.md",
            "incremento_1a3_anos_k09.md",
            "calendario_metricas_duplas_k09.md",
        ],
        "validacoes": checks,
        "calendario_sem_piso": payload["desempenho"]["sem_piso_desde_207"],
        "calendario_metricas_duplas": payload["desempenho"]["sem_piso_por_metrica"],
        "piso_dois_pontos": payload["desempenho"]["piso_ilustrativo_dois_pontos_reais"],
        "SK_Gd": payload["desempenho"]["SK_Gd_cenario_sqrtT"],
        "NuFIT_tabela": next(x for x in witnesses if x["id"] == "NuFIT_6_1_tabela"),
        "NuFIT_artigo": next(x for x in witnesses if x["id"] == "NuFIT_6_1_artigo_eq11"),
    }
    (OUT / "resumo_execucao_k09.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

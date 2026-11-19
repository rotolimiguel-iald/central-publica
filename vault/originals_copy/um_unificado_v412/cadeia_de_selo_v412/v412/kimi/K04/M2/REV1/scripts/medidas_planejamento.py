#!/usr/bin/env python3
"""K04/M2 R2 — analytical PLANNING calculations from public aggregate numbers.

[DERIVED—PLANEJAMENTO] No event vectors, likelihoods, observed-test execution,
H0DN files, or K01 validator are used. The normal CDF is evaluated analytically;
there is no simulation and no random seed. Units for mu and sigma are 1e-5 eV^2.

R2 keeps independent-measurement, cumulative-release, conditional-truth and
joint-MATCHED models separate. Covariances not published by the collaborations
remain OPEN. Every nested-covariance example is explicitly a toy benchmark.
"""
from __future__ import annotations

import json
import math
from datetime import date, timedelta
from pathlib import Path

STATUS = "[DERIVED—PLANEJAMENTO] números públicos agregados; não observado"
ALPHA_FINE_CODATA_2018 = 0.0072973525693
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
M2_PRED = BETA * math.sin(math.pi / 4.0) * 1000.0  # meV, E0 = 1 eV [INPUT]
DM2_PRED = (M2_PRED / 1000.0) ** 2 / 1e-5
MU_NOW = 7.388
SIGMA_NOW = 0.078
DELTA = MU_NOW - DM2_PRED
D90 = 5.0 + 1.2815515655446004
CUTOFF = date(2026, 5, 18)
START = date(2025, 8, 26)
SIX_YEAR_DATE = date(2031, 8, 26)
DAYS_SIX_CALENDAR = (SIX_YEAR_DATE - START).days
OUT = Path(__file__).resolve().parents[1] / "medidas"
DETERMINATIONS = Path(r"C:\IALD\Central de Patentes\work\neutrino_E0_autonomia_30out\determinacoes_m2_30out.json")


def cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def band_delta(mean: float, sd: float, sigma_future: float, t: float) -> float:
    """P(|X-DM2_PRED|/sigma_future >= t), X normal in Delta m^2."""
    return cdf((DM2_PRED - t * sigma_future - mean) / sd) + 1.0 - cdf(
        (DM2_PRED + t * sigma_future - mean) / sd
    )


def thresholds_m2(t: float, sigma_future: float) -> tuple[float | None, float]:
    """X thresholds for frozen first-order m2 ratio, in 1e-5 eV^2.

    m=sqrt(10 X), r=m|m-M2_PRED|/(5*sigma_future).
    """
    high_mass = (M2_PRED + math.sqrt(M2_PRED**2 + 20.0 * t * sigma_future)) / 2.0
    high = high_mass**2 / 10.0
    discriminant = M2_PRED**2 - 20.0 * t * sigma_future
    if discriminant < 0:
        return None, high
    low_mass = (M2_PRED - math.sqrt(discriminant)) / 2.0
    return low_mass**2 / 10.0, high


def band_m2(mean: float, sd: float, sigma_future: float, t: float) -> float:
    low, high = thresholds_m2(t, sigma_future)
    lower_tail = 0.0 if low is None else cdf((low - mean) / sd)
    return lower_tail + 1.0 - cdf((high - mean) / sd)


def probabilities(mean: float, predictive_sd: float, sigma_future: float, metric: str) -> dict:
    if predictive_sd <= 0:
        raise ValueError(f"non-positive predictive sd: {predictive_sd}")
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
    """Cumulative normal model with Cov(X0,X)=C.

    Public posterior: mean=MU_NOW and Var=SIGMA_NOW^2+s^2-2C.
    Conditional truth=prediction: condition jointly on X0=MU_NOW, so
      E[X|X0] = pred + C/SIGMA_NOW^2 * (MU_NOW-pred)
      Var[X|X0] = SIGMA_NOW^2+s^2-2C-C^2/SIGMA_NOW^2.
    The C=s^2 nested-information example is only a declared benchmark.
    """
    variance = SIGMA_NOW**2 + sigma**2 - 2.0 * covariance
    if variance <= 0:
        raise ValueError(f"non-positive cumulative variance: {variance}")
    if truth == "posterior_publico":
        return probabilities(MU_NOW, math.sqrt(variance), sigma, metric)
    if truth == "verdade_previsao_condicional":
        mean = DM2_PRED + (covariance / SIGMA_NOW**2) * (MU_NOW - DM2_PRED)
        conditional_variance = variance - covariance**2 / SIGMA_NOW**2
        if conditional_variance <= 0:
            raise ValueError(f"non-positive conditional variance: {conditional_variance}")
        return probabilities(mean, math.sqrt(conditional_variance), sigma, metric)
    raise ValueError(truth)


def make_outcomes() -> list[dict]:
    precisions = [
        ("0,7 %", 0.007 * MU_NOW),
        ("0,5 %", 0.005 * MU_NOW),
        ("0,407121 %", 0.00407121 * MU_NOW),
        ("0,324061 %", 0.00324061 * MU_NOW),
        ("0,3 %", 0.003 * MU_NOW),
        ("Tabela 6", 0.024),
    ]
    rows = []
    for label, sigma in precisions:
        d_delta = DELTA / sigma
        d_m2 = frozen_D(MU_NOW, sigma)
        rows.append({
            "precisao": label,
            "sigma": sigma,
            "D_delta_centro_planejamento": d_delta,
            "D_m2_centro_planejamento": d_m2,
            "ramo_r_lt_3_mesmo_em_todas_as_hipoteses": "UNDER" if d_delta < 5.0 else "ARMED_CONSISTENT",
            "independente": {
                truth: {
                    metric: independent_model(sigma, truth, metric)
                    for metric in ("delta", "m2")
                }
                for truth in ("posterior_publico", "verdade_previsao")
            },
            "cumulativo_C_igual_s2_brinquedo": {
                truth: {
                    metric: cumulative_model(sigma, truth, metric, sigma**2)
                    for metric in ("delta", "m2")
                }
                for truth in ("posterior_publico", "verdade_previsao_condicional")
            },
            "covariancia_real": "OPEN; não publicada; o exemplo C=s² não é atribuição ao JUNO",
        })
    return rows


def make_performance() -> dict:
    sigma_59, sigma_207 = 0.12, 0.078
    t_59, t_207 = 59.1, 207.2
    project_207 = 0.074 * math.sqrt(100.0 / t_207)
    sigma5 = DELTA / 5.0
    sigma_d90 = DELTA / D90
    information = t_207 * sigma_207**2
    no_floor = {}
    for name, target in (("5sigma", sigma5), ("D90", sigma_d90)):
        total = information / target**2
        no_floor[name] = {
            "sigma_alvo": target,
            "dias_totais_cumulativos": total,
            "dias_adicionais_cumulativos": total - t_207,
            "data_ideal_cumulativa_apos_corte": add_days(CUTOFF, total - t_207),
            "dias_novos_somente_incremento": total,
            "data_ideal_incremento_apos_corte": add_days(CUTOFF, total),
        }
    a_two = (sigma_207**2 - sigma_59**2) / (1.0 / t_207 - 1.0 / t_59)
    floor_two_sq = sigma_207**2 - a_two / t_207
    floor_two = math.sqrt(floor_two_sq)

    # R2: 100 nominal days -> about 92 full-reactor days; 6 years -> 2009.
    a_full = 92.0 * 0.074**2
    a_nominal = 100.0 * 0.074**2
    stat_2009 = math.sqrt(a_full / 2009.0)
    floor_project_sq = 0.024**2 - stat_2009**2
    floor_project = math.sqrt(floor_project_sq)
    project_floor = {}
    for name, target in (("5sigma", sigma5), ("D90", sigma_d90)):
        full_days = a_full / (target**2 - floor_project_sq)
        nominal_days = a_nominal / (target**2 - floor_project_sq)
        project_floor[name] = {
            "sigma_alvo": target,
            "dias_full_reactor": full_days,
            "data_full_reactor_convertida_por_2009_em_6_anos": add_days(
                START, full_days * DAYS_SIX_CALENDAR / 2009.0
            ),
            "dias_inteiramente_nominais": nominal_days,
            "data_inteiramente_nominal": add_days(START, nominal_days),
            "excedente_full_sobre_2009": full_days - 2009.0,
        }
    return {
        "sigma_207_extrapolado_do_projeto": project_207,
        "razao_real_sobre_projeto": sigma_207 / project_207,
        "razao_reducao_59_207": sigma_59 / sigma_207,
        "razao_sqrtT_59_207": math.sqrt(t_207 / t_59),
        "dias_nominais_para_full_reactor": {"100_nominal": 92.0, "6_anos": 2009.0, "20_anos": 6696.0},
        "dias_calendario_em_seis_anos": DAYS_SIX_CALENDAR,
        "sem_piso_desde_207": no_floor,
        "piso_ilustrativo_dois_pontos_reais": {
            "a": a_two,
            "s0": floor_two,
            "5sigma_alcancavel": sigma5 >= floor_two,
            "D90_alcancavel": sigma_d90 >= floor_two,
            "nota": "dois pontos ajustam dois parâmetros; análises mudaram; não é piso medido",
        },
        "piso_aproximado_do_projeto": {
            "a_full_reactor": a_full,
            "a_inteiramente_nominal": a_nominal,
            "sigma_stat_2009": stat_2009,
            "s0": floor_project,
            "resultados": project_floor,
            "nota": "brinquedo decomposição em quadratura; não cronograma nem curva publicada",
            "historico_rotulagem_errada_REV0": {"5sigma": "2028-05-15", "D90": "2031-09-18"},
        },
    }


def make_increment() -> dict:
    mu1, s1, mu2, s2 = 7.50, 0.12, MU_NOW, SIGMA_NOW
    w1, w2 = 1.0 / s1**2, 1.0 / s2**2
    dw = w2 - w1
    mu_increment = (w2 * mu2 - w1 * mu1) / dw
    sigma_increment = 1.0 / math.sqrt(dw)
    return {
        "w_59": w1,
        "w_207": w2,
        "delta_w": dw,
        "centro_ilustrativo": mu_increment,
        "sigma_ilustrativo": sigma_increment,
        "r_delta_contra_previsao": delta_r(mu_increment, sigma_increment),
        "r_m2_contra_previsao": frozen_r(mu_increment, sigma_increment),
        "distancia_ao_centro_59_em_sigma_increment": abs(mu_increment - mu1) / sigma_increment,
        "ressalva": "informação independente e gaussiana presumida; covariância inter-liberações não publicada; não é determinação independente",
    }


def make_witnesses() -> list[dict]:
    metadata = {
        "JUNO_207d": ("JUNO", "2026", "arXiv:2609.37895v1", "P; não S"),
        "SNO_plus": ("SNO+", "2026", "PRL 137, 101807; DOI 10.1103/mv5z-pfb7; arXiv:2511.11856v4", "direta, sem JUNO; covariância de fluxo/nuisances OPEN"),
        "SK_Gd_reator": ("Super-Kamiokande-Gd", "2026", "arXiv:2610.03143v1", "direta, sem JUNO; cenário, não agenda nem prova de independência"),
        "KamLAND": ("KamLAND", "2013", "PRD 88, 033001; DOI 10.1103/PhysRevD.88.033001; arXiv:1303.4667v2, Tabela 3", "direta, sem JUNO; covariância de fluxo/nuisances OPEN"),
        "Solares_sem_KamLAND": ("SK + demais solares", "2024", "PRD 109, 092001; DOI 10.1103/PhysRevD.109.092001; arXiv:2312.12907v2", "uma família solar; covariância OPEN"),
        "JUNO_59d_subset": ("JUNO", "2025/2026", "arXiv:2511.14593v1; Nature 654, 343; DOI 10.1038/s41586-026-10538-z", "subconjunto de P; não S"),
        "NuFIT_6_1": ("NuFIT 6.1", "2025", "NuFIT 6.1 release notes; arXiv:2601.09791 associado", "global com JUNO 59d; conjunto OPEN"),
        "Capozzi_2025": ("Capozzi et al.", "2025/2026", "PRD 114, 016026; DOI 10.1103/cxqw-1bty; arXiv:2511.21650", "global com JUNO/SNO+; conjunto OPEN"),
        "Bari_2026a_NO": ("Bari 2026.a preliminar NO", "2026", "Global-nu release 2026.a, 15/10/2026; paper in preparation; não artigo primário publicado", "preliminar, com JUNO 207d/SK-Gd; conjunto OPEN"),
        "SK_Gd_solar_reator": ("Super-Kamiokande-Gd solar+reator", "2026", "arXiv:2610.03143v1", "combinação na mesma colaboração; conjunto OPEN"),
    }
    payload = json.loads(DETERMINATIONS.read_text(encoding="utf-8"))
    rows = []
    for item in payload["resultados"]:
        experiment, year, primary, independence = metadata[item["id"]]
        sigma = item["sigma_delta_usado_1e-5_eV2"]
        sigma5 = sigma_for_5(item["mu"])
        exposure = item.get("exposure_days")
        total_sqrt_t = exposure * (sigma / sigma5) ** 2 if exposure is not None else None
        rows.append({
            "id": item["id"],
            "experimento": experiment,
            "ano": year,
            "centro": item["mu"],
            "erro_menos": item["err_m"],
            "erro_mais": item["err_p"],
            "sigma_lado_previsao": sigma,
            "r_frozen_m2": frozen_r(item["mu"], sigma),
            "r_delta": delta_r(item["mu"], sigma),
            "sigma_necessario_5_m2": sigma5,
            "sigma_ate_0p0301": sigma <= DELTA / 5.0,
            "dias_exposicao": exposure,
            "dias_totais_condicional_sqrtT_5sigma": total_sqrt_t,
            "dias_adicionais_condicional_sqrtT_5sigma": total_sqrt_t - exposure if exposure is not None else None,
            "ID_primario": primary,
            "papel": independence,
        })
    rows.append({
        "id": "SNO_plus_reator_solar_final",
        "experimento": "SNO+ + KamLAND + solares (sem JUNO)",
        "ano": "2026",
        "centro": 7.59,
        "erro_menos": 0.17,
        "erro_mais": 0.17,
        "sigma_lado_previsao": 0.17,
        "r_frozen_m2": frozen_r(7.59, 0.17),
        "r_delta": delta_r(7.59, 0.17),
        "sigma_necessario_5_m2": sigma_for_5(7.59),
        "sigma_ate_0p0301": False,
        "dias_exposicao": None,
        "dias_totais_condicional_sqrtT_5sigma": None,
        "dias_adicionais_condicional_sqrtT_5sigma": None,
        "ID_primario": "PRL 137, 101807; DOI 10.1103/mv5z-pfb7; arXiv:2511.11856v4, Tabela 3",
        "papel": "combinação sem JUNO; não somar SNO+ duas vezes; conjunto OPEN",
    })
    return rows


def matched_le_1(mean: float, sd: float, sigma: float) -> float:
    return 1.0 - band_m2(mean, sd, sigma, 1.0)


def make_joint_matched(witnesses: list[dict]) -> list[dict]:
    direct = {"SNO_plus", "SK_Gd_reator", "KamLAND", "Solares_sem_KamLAND"}
    open_reasons = {
        "JUNO_207d": "P, não S; MATCHED não se aplica",
        "JUNO_59d_subset": "subconjunto de P; não é S independente",
        "NuFIT_6_1": "contém JUNO 59d; covariância P–S não publicada",
        "Capozzi_2025": "contém JUNO/SNO+; covariância P–S não publicada",
        "Bari_2026a_NO": "preliminar e contém JUNO 207d/SK-Gd; covariância não identificável",
        "SK_Gd_solar_reator": "combinação na mesma colaboração; covariância/nuisances não publicada",
        "SNO_plus_reator_solar_final": "combinação compartilha dados e fluxos com componentes; covariância não identificável",
    }
    p_le1 = matched_le_1(MU_NOW, SIGMA_NOW, SIGMA_NOW)
    rows = []
    for item in witnesses:
        sid = item["id"]
        if sid in direct:
            s_le1 = matched_le_1(item["centro"], item["sigma_lado_previsao"], item["sigma_lado_previsao"])
            rows.append({
                "id": sid,
                "modelo": "P~N(7.388,0.078²), S~N(mu_S,sigma_S²), C_PS=0 somente como brinquedo",
                "P_rP_le_1": p_le1,
                "P_rS_le_1": s_le1,
                "P_matched_conjunta_C0_brinquedo": p_le1 * s_le1,
                "C_PS_real": "OPEN; fluxos e nuisances compartilhados não quantificados",
                "estado": "IDENTIFICÁVEL SÓ COMO BRINQUEDO C=0; não é independência física nem veredito",
            })
        else:
            rows.append({
                "id": sid,
                "modelo": "OPEN — distribuição conjunta P+S não identificável sem covariância",
                "P_rP_le_1": p_le1,
                "P_rS_le_1": None,
                "P_matched_conjunta_C0_brinquedo": None,
                "C_PS_real": "OPEN",
                "estado": open_reasons[sid],
            })
    return rows


def source_classes() -> dict:
    return {
        "Bari_2026a_NO": "PRELIMINAR — paper in preparation; não fonte primária publicada",
        "HyperK_status": "primeiros dados previstos para 2028; cenário de cinco anos posterior é tentativa, não data de precisão assegurada",
        "DUNE_solar_5p9pct": "previsão de Capozzi et al., teóricos; não é forecast oficial da DUNE Collaboration",
        "SNO_plus_v4": "depositada em 2026-09-04, antes do JUNO 207d; revisão do mesmo conjunto, não nova determinação autônoma mundial irrestrita",
        "SK_Gd_reator": "3,605064σ e 380,0785536 dias são cenário condicional; não agenda nem prova de independência",
    }


def pct(x: float, digits: int = 6) -> str:
    return f"{100*x:.{digits}f} %".replace(".", ",")


def num(x: float, digits: int = 6) -> str:
    return f"{x:.{digits}f}".replace(".", ",")


def outcome_markdown(rows: list[dict], model: str, truth: str) -> list[str]:
    title = {
        ("independente", "posterior_publico"): "(a1) Independente — posterior público",
        ("independente", "verdade_previsao"): "(a2) Independente — verdade = previsão",
        ("cumulativo_C_igual_s2_brinquedo", "posterior_publico"): "(b1) Cumulativo C=s² — posterior público, brinquedo",
        ("cumulativo_C_igual_s2_brinquedo", "verdade_previsao_condicional"): "(b2) Cumulativo C=s² — verdade=previsão condicionada a X0, brinquedo",
    }[(model, truth)]
    lines = [
        f"### {title}",
        "",
        "| precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | ramo r<3 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        probs = row[model][truth]
        lines.append(
            f"| {row['precisao']} | {num(row['sigma'])} | {num(row['D_delta_centro_planejamento'])} | "
            f"{num(row['D_m2_centro_planejamento'])} | {pct(probs['m2']['P_r_le_1'])} | "
            f"{pct(probs['m2']['P_1_lt_r_lt_3'])} | {pct(probs['m2']['P_3_le_r_lt_5'])} | "
            f"{pct(probs['m2']['P_r_ge_5'])} | {pct(probs['delta']['P_r_ge_5'])} | {row['ramo_r_lt_3_mesmo_em_todas_as_hipoteses']} |"
        )
    lines.append("")
    return lines


def markdown(payload: dict) -> str:
    lines = [
        "# Tabelas calculadas — K04/M2 R2",
        "",
        STATUS + ". Cálculo analítico; nenhuma simulação; nenhum teste observado.",
        "",
        f"m₂ = {M2_PRED:.12f} meV; Δpred = {DM2_PRED:.12f}; Δcentro = {DELTA:.12f}; D90 = {D90:.12f}.",
        "D usa sempre o centro de planejamento 7,388, inclusive sob verdade=previsão.",
        "",
    ]
    for model, truth in (
        ("independente", "posterior_publico"),
        ("independente", "verdade_previsao"),
        ("cumulativo_C_igual_s2_brinquedo", "posterior_publico"),
        ("cumulativo_C_igual_s2_brinquedo", "verdade_previsao_condicional"),
    ):
        lines += outcome_markdown(payload["desfechos"], model, truth)
    perf = payload["desempenho"]["sem_piso_desde_207"]
    lines += [
        "## Projeções sem piso desde 207,2 dias — cenários próprios, não ligados às probabilidades independentes",
        "",
        "| alvo | σ alvo | T total (d) | adicional cumulativo (d) | data ideal cumulativa | incremento novo (d) | data ideal incremento |",
        "|---|---:|---:|---:|---|---:|---|",
    ]
    for name, row in perf.items():
        lines.append(
            f"| {name} | {num(row['sigma_alvo'])} | {num(row['dias_totais_cumulativos'], 2)} | "
            f"{num(row['dias_adicionais_cumulativos'], 2)} | {row['data_ideal_cumulativa_apos_corte']} | "
            f"{num(row['dias_novos_somente_incremento'], 2)} | {row['data_ideal_incremento_apos_corte']} |"
        )
    project = payload["desempenho"]["piso_aproximado_do_projeto"]
    lines += [
        "",
        f"## Brinquedo decomposição do projeto — a_full=92×0,074², a_nominal=100×0,074², s0={project['s0']:.9f}",
        "",
        "| alvo | dias full-reactor | data convertida por 2009 em 6 anos | dias inteiramente nominais | data inteiramente nominal |",
        "|---|---:|---|---:|---|",
    ]
    for name, row in project["resultados"].items():
        lines.append(
            f"| {name} | {num(row['dias_full_reactor'], 3)} | {row['data_full_reactor_convertida_por_2009_em_6_anos']} | "
            f"{num(row['dias_inteiramente_nominais'], 3)} | {row['data_inteiramente_nominal']} |"
        )
    lines += [
        "",
        "## MATCHED conjunto — só brinquedos C=0 identificáveis; C real OPEN",
        "",
        "| id | P(rP≤1) | P(rS≤1) | P(MATCHED), C=0 brinquedo | estado |",
        "|---|---:|---:|---:|---|",
    ]
    for row in payload["matched_conjunta"]:
        joint = row["P_matched_conjunta_C0_brinquedo"]
        lines.append(
            f"| {row['id']} | {pct(row['P_rP_le_1'])} | "
            f"{'OPEN' if row['P_rS_le_1'] is None else pct(row['P_rS_le_1'])} | "
            f"{'OPEN' if joint is None else pct(joint)} | {row['estado']} |"
        )
    lines += [
        "",
        "## As dez entradas + combinação SNO+ final",
        "",
        "| id | centro | σ lado | r frozen | r Δ | σ para 5σ | ≤0,030078? | papel |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in payload["testemunhas"]:
        lines.append(
            f"| {row['id']} | {num(row['centro'], 3)} | {num(row['sigma_lado_previsao'], 3)} | "
            f"{num(row['r_frozen_m2'])} | {num(row['r_delta'])} | {num(row['sigma_necessario_5_m2'])} | "
            f"{'sim' if row['sigma_ate_0p0301'] else 'não'} | {row['papel']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    witnesses = make_witnesses()
    payload = {
        "estatuto": STATUS,
        "metodo": "CDF normal analítica; sem simulação; sem semente",
        "unidade": "1e-5 eV^2 para Delta m^2 e sigma",
        "m2_pred_meV": M2_PRED,
        "dm2_pred": DM2_PRED,
        "delta_centro": DELTA,
        "D90": D90,
        "D_usa_centro_planejamento_em_todas_as_hipoteses": True,
        "desfechos": make_outcomes(),
        "desempenho": make_performance(),
        "incremento_59_207": make_increment(),
        "testemunhas": witnesses,
        "matched_conjunta": make_joint_matched(witnesses),
        "classes_de_fontes": source_classes(),
        "covariancias_reais": "OPEN salvo nos brinquedos explicitamente rotulados C=0 ou C=s²",
        "datas": {
            "V2_hasheada": "2026-08-08",
            "SNO_plus_v4_depositada": "2026-09-04",
            "liberacao_207d": "2026-09-29",
            "corte_dados_207d": CUTOFF.isoformat(),
            "inicio_fisico_juno": START.isoformat(),
        },
    }
    for row in payload["desfechos"]:
        for model in ("independente", "cumulativo_C_igual_s2_brinquedo"):
            for truth in row[model]:
                if truth == "covariancia_real":
                    continue
                for metric in ("delta", "m2"):
                    probs = row[model][truth][metric]
                    assert math.isclose(
                        probs["P_r_le_1"] + probs["P_1_lt_r_lt_3"] + probs["P_3_le_r_lt_5"] + probs["P_r_ge_5"],
                        1.0,
                        rel_tol=0.0,
                        abs_tol=3e-12,
                    )
    assert math.isclose(payload["desempenho"]["sem_piso_desde_207"]["5sigma"]["sigma_alvo"], DELTA / 5.0)
    (OUT / "resultados_planejamento.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "tabelas_planejamento.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))


if __name__ == "__main__":
    main()

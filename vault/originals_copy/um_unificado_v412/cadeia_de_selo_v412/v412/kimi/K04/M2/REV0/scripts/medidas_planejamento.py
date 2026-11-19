#!/usr/bin/env python3
"""K04/M2 — analytical PLANNING calculations from public aggregate numbers.

[DERIVED—PLANEJAMENTO] No event vectors, likelihoods, observed-test execution,
H0DN files, or K01 validator are used. The normal CDF is evaluated analytically;
there is no simulation and no random seed. Units for mu and sigma are 1e-5 eV^2.
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
    """X thresholds for the frozen first-order m2 ratio, in 1e-5 eV^2.

    m=sqrt(10 X), r=m|m-M2_PRED|/(5*sigma_future). The high-side root
    always exists. The low-side root is relevant at the present small errors.
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


def probabilities(mean: float, current_sd: float, sigma_future: float, metric: str) -> dict:
    predictive_sd = math.hypot(current_sd, sigma_future)
    band = band_delta if metric == "delta" else band_m2
    ge5 = band(mean, predictive_sd, sigma_future, 5.0)
    lt5 = 1.0 - ge5
    ge3 = band(mean, predictive_sd, sigma_future, 3.0)
    return {
        "P_r_lt_3": 1.0 - ge3,
        "P_3_le_r_lt_5": ge3 - ge5,
        "P_r_ge_5": ge5,
        "predictive_sd": predictive_sd,
        "P_r_lt_5": lt5,
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
        row = {
            "precisao": label,
            "sigma": sigma,
            "D_delta_centro_parado": DELTA / sigma,
            "D_m2_centro_parado": frozen_D(MU_NOW, sigma),
        }
        for hypothesis, mean, current_sd in (
            ("posterior_publico", MU_NOW, SIGMA_NOW),
            ("verdade_previsao", DM2_PRED, 0.0),
        ):
            row[hypothesis] = {
                metric: probabilities(mean, current_sd, sigma, metric)
                for metric in ("delta", "m2")
            }
        rows.append(row)
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
    # Two real releases, fitted exactly as an illustrative a/T+s0^2 model.
    a_two = (sigma_207**2 - sigma_59**2) / (1.0 / t_207 - 1.0 / t_59)
    floor_two_sq = sigma_207**2 - a_two / t_207
    floor_two = math.sqrt(floor_two_sq)
    # Project-only decomposition: 100-day statistical anchor vs 6-year total.
    a_project = 100.0 * 0.074**2
    stat_2009 = math.sqrt(a_project / 2009.0)
    floor_project_sq = 0.024**2 - stat_2009**2
    floor_project = math.sqrt(floor_project_sq)
    project_floor = {}
    for name, target in (("5sigma", sigma5), ("D90", sigma_d90)):
        total = a_project / (target**2 - floor_project_sq)
        project_floor[name] = {
            "sigma_alvo": target,
            "dias_full_power_totais": total,
            "excedente_sobre_2009_dias": total - 2009.0,
            "data_ideal_com_duty_11_sobre_12": add_days(START, total * 12.0 / 11.0),
        }
    return {
        "sigma_207_extrapolado_do_projeto": project_207,
        "razao_real_sobre_projeto": sigma_207 / project_207,
        "razao_reducao_59_207": sigma_59 / sigma_207,
        "razao_sqrtT_59_207": math.sqrt(t_207 / t_59),
        "seis_anos_full_reactor_dias": 2009,
        "vinte_anos_full_reactor_dias": 6696,
        "sem_piso_desde_207": no_floor,
        "piso_ilustrativo_dois_pontos_reais": {
            "a": a_two,
            "s0": floor_two,
            "5sigma_alcancavel": sigma5 >= floor_two,
            "D90_alcancavel": sigma_d90 >= floor_two,
            "nota": "dois pontos ajustam dois parâmetros; análises mudaram; não é piso medido",
        },
        "piso_aproximado_do_projeto": {
            "a": a_project,
            "sigma_stat_2009": stat_2009,
            "s0": floor_project,
            "resultados": project_floor,
            "nota": "decomposição aproximada em quadratura, não curva publicada",
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
        "SNO_plus": ("SNO+", "2026", "PRL 137, 101807; DOI 10.1103/mv5z-pfb7; arXiv:2511.11856v4", "direta, sem JUNO"),
        "SK_Gd_reator": ("Super-Kamiokande-Gd", "2026", "arXiv:2610.03143v1", "direta, sem JUNO"),
        "KamLAND": ("KamLAND", "2013", "PRD 88, 033001; DOI 10.1103/PhysRevD.88.033001; arXiv:1303.4667v2, Tabela 3", "direta, sem JUNO"),
        "Solares_sem_KamLAND": ("SK + demais solares", "2024", "PRD 109, 092001; DOI 10.1103/PhysRevD.109.092001; arXiv:2312.12907v2", "uma família solar"),
        "JUNO_59d_subset": ("JUNO", "2025/2026", "arXiv:2511.14593v1; Nature 654, 343; DOI 10.1038/s41586-026-10538-z", "subconjunto de P"),
        "NuFIT_6_1": ("NuFIT 6.1", "2025", "NuFIT 6.1 release notes; arXiv:2601.09791 associado", "global com JUNO 59d; não independente"),
        "Capozzi_2025": ("Capozzi et al.", "2025/2026", "PRD 114, 016026; DOI 10.1103/cxqw-1bty; arXiv:2511.21650", "global com JUNO/SNO+; não independente"),
        "Bari_2026a_NO": ("Bari 2026.a preliminar NO", "2026", "Global-nu release 2026.a, 15/10/2026", "global com JUNO 207d/SK-Gd; não independente"),
        "SK_Gd_solar_reator": ("Super-Kamiokande-Gd solar+reator", "2026", "arXiv:2610.03143v1", "combinação na mesma colaboração; não adicional"),
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
    # Auxiliary final SNO+ reactor+solar combination, not one of the ten rows.
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
        "ID_primario": "PRL 137, 101807; DOI 10.1103/mv5z-pfb7; arXiv:2511.11856v4, Tabela 3",
        "papel": "combinação sem JUNO; não somar a SNO+ duas vezes",
    })
    return rows


def pct(x: float, digits: int = 6) -> str:
    return f"{100*x:.{digits}f} %".replace(".", ",")


def num(x: float, digits: int = 6) -> str:
    return f"{x:.{digits}f}".replace(".", ",")


def markdown(payload: dict) -> str:
    lines = [
        "# Tabelas calculadas — K04/M2",
        "",
        STATUS + ". Cálculo analítico; nenhuma simulação; nenhum teste observado.",
        "",
        f"m₂ = {M2_PRED:.12f} meV; Δpred = {DM2_PRED:.12f}; Δcentro = {DELTA:.12f}; D90 = {D90:.12f}.",
        "",
        "## Desfechos — métrica frozen m₂; PΔ(r≥5) também mostrada para rastreabilidade",
        "",
    ]
    for hypothesis, title in (("posterior_publico", "(a) posterior público de planejamento"), ("verdade_previsao", "(b) verdade = previsão")):
        lines += [
            f"### {title}",
            "",
            "| precisão | σ | DΔ | D_m₂ | P(r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for row in payload["desfechos"]:
            probs = row[hypothesis]
            lines.append(
                f"| {row['precisao']} | {num(row['sigma'])} | {num(row['D_delta_centro_parado'])} | "
                f"{num(row['D_m2_centro_parado'])} | {pct(probs['m2']['P_r_lt_3'])} | "
                f"{pct(probs['m2']['P_3_le_r_lt_5'])} | {pct(probs['m2']['P_r_ge_5'])} | "
                f"{pct(probs['delta']['P_r_ge_5'])} |"
            )
        lines.append("")
    perf = payload["desempenho"]["sem_piso_desde_207"]
    lines += [
        "## Projeções sem piso desde 207,2 dias",
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
    payload = {
        "estatuto": STATUS,
        "metodo": "CDF normal analítica; sem simulação; sem semente",
        "unidade": "1e-5 eV^2 para Delta m^2 e sigma",
        "m2_pred_meV": M2_PRED,
        "dm2_pred": DM2_PRED,
        "delta_centro": DELTA,
        "D90": D90,
        "desfechos": make_outcomes(),
        "desempenho": make_performance(),
        "incremento_59_207": make_increment(),
        "testemunhas": make_witnesses(),
        "datas": {
            "V2_hasheada": "2026-08-08",
            "liberacao_207d": "2026-09-29",
            "corte_dados_207d": CUTOFF.isoformat(),
            "inicio_fisico_juno": START.isoformat(),
        },
    }
    # Arithmetic closure checks only; these are not empirical or synthetic verdict tests.
    for row in payload["desfechos"]:
        for hypothesis in ("posterior_publico", "verdade_previsao"):
            for metric in ("delta", "m2"):
                probs = row[hypothesis][metric]
                assert math.isclose(
                    probs["P_r_lt_3"] + probs["P_3_le_r_lt_5"] + probs["P_r_ge_5"],
                    1.0,
                    rel_tol=0.0,
                    abs_tol=2e-12,
                )
    assert math.isclose(payload["desempenho"]["sem_piso_desde_207"]["5sigma"]["sigma_alvo"], DELTA / 5.0)
    (OUT / "resultados_planejamento.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "tabelas_planejamento.md").write_text(markdown(payload), encoding="utf-8")
    print(markdown(payload))


if __name__ == "__main__":
    main()

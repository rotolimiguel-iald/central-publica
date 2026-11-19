#!/usr/bin/env python3
"""Medidas K05/τ★ R2: leitura de registros selados, sem nova estatística observada."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(r"C:\IALD")
BASE = ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "kimi" / "K05" / "TAU"
MED = BASE / "medidas"
CORE = ROOT / "Artigo" / "Haja_Luz" / "A Ponte e o Um" / "Nós" / "um_absoluto.json"
CLOCK = MED / "clock_selado_extraido.json"
NOS = ROOT / "Artigo" / "Haja_Luz" / "A Ponte e o Um" / "Nós"
MEM = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
KIMI = ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "kimi"

# Entradas publicadas; não são ajustes a dados.
ALPHA = 7.2973525693e-3  # CODATA 2018
BETA = ALPHA * math.sqrt(math.e)  # regra obrigatória em runtime
H = 6.62607015e-34
HBAR = H / (2.0 * math.pi)
C = 299792458.0
G = 6.67430e-11
G_CORE = 6.674e-11  # constante efetivamente usada pelo registro v369
EV = 1.602176634e-19
TP = math.sqrt(HBAR * G / C**5)
EP = HBAR / TP
M_U = 1.66053906660e-27
GM_EARTH = 3.986004418e14
GM_SUN = 1.3271244e20
G_STD = 9.80665
MPC = 3.0856775814913673e22
H0 = 67.4 * 1000.0 / MPC  # benchmark Planck 2018, não ajuste desta análise


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sci(x: float, digits: int = 4) -> str:
    if x == 0:
        return "0"
    s = f"{x:.{digits}e}"
    mant, exp = s.split("e")
    return f"{mant}e{int(exp):+d}"


def mdnum(x: float, digits: int = 3) -> str:
    if x == 0:
        return "0"
    exp = math.floor(math.log10(abs(x)))
    mant = x / 10**exp
    return f"{mant:.{digits}f}×10^{exp}".replace(".", ",")


def gamma(tau: float, omega: float) -> float:
    return 0.5 * BETA * tau * omega**2


def main() -> None:
    MED.mkdir(parents=True, exist_ok=True)
    extracted = json.loads(CLOCK.read_text(encoding="utf-8"))
    assert extracted["source_sha256"] == sha256(CORE), "core mudou após a extração"
    full = next(r["value"] for r in extracted["records"] if r["json_path"] == ["core", "clock_test_result_v369"])
    protocol = next(r["value"] for r in extracted["records"] if r["json_path"] == ["core", "clock_test_protocol_v369"])
    assert abs(BETA - full["beta_runtime"]) < 1e-15

    bounds: dict[str, dict[str, Any]] = {}
    for p in full["P1"]["platforms"]:
        bounds[p["id"]] = {
            "label": p["species"],
            "bound_s": p["tau_star_max_s"],
            "kind": p["bound_kind"],
            "clock": p["clock"],
            "source": p["source"],
            "verification": p["verification"],
            "origin": "core.clock_test_result_v369.P1.platforms",
        }
    bounds["atlas_legacy_1p8e_m33"] = {
        "label": "Atlas, registro auxiliar ²²⁹Th",
        "bound_s": 1.8e-33,
        "kind": "ATLAS_RECORD_NOT_REEVALUATED",
        "clock": None,
        "source": "TGL_ATLAS.md, linhas 997–998; não é a cota Th atual do core",
        "verification": "lido como registro; não reavaliado",
        "origin": "Central de Patentes/memory/TGL_ATLAS.md",
    }

    readings: list[dict[str, Any]] = [
        {"id": "c_1", "label": "c★=1 (cânone)", "tau_s": TP, "class": "número puro sobre Planck"},
        {"id": "c_inv_beta", "label": "c★=1/β (Artigo A)", "tau_s": TP / BETA, "class": "número puro sobre Planck"},
        {"id": "c_sqrt2", "label": "c★=√2 (célula, sob hipóteses)", "tau_s": math.sqrt(2.0) * TP, "class": "número puro sobre Planck"},
        {"id": "c_2pi", "label": "c★=2π (volta KMS)", "tau_s": 2.0 * math.pi * TP, "class": "número puro sobre Planck"},
        {"id": "c_4pi", "label": "c★=4π (só com energia fixada)", "tau_s": 4.0 * math.pi * TP, "class": "número puro condicional"},
        {"id": "gap_u", "label": "ħ/u, u=1 eV", "tau_s": HBAR / EV, "class": "âncora de energia posta"},
        {"id": "retido", "label": "ħ/(βu), u=1 eV", "tau_s": HBAR / (BETA * EV), "class": "tempo do retido"},
        {"id": "unruh_g", "label": "t_mod Unruh-g: 2πc/g", "tau_s": 2.0 * math.pi * C / G_STD, "class": "alternativa v369"},
        {"id": "earth", "label": "GM⊕/c³", "tau_s": GM_EARTH / C**3, "class": "alternativa v369"},
        {"id": "sr_atom", "label": "GM(⁸⁷Sr)/c³, A·m_u", "tau_s": G_CORE * 87.0 * M_U / C**3, "class": "alternativa v369"},
        {"id": "monopole_1eV", "label": "4πG(1 eV)/c⁵", "tau_s": 4.0 * math.pi * G * EV / C**5, "class": "monopolo dependente de E"},
    ]

    for r in readings:
        r["tau_over_tP"] = r["tau_s"] / TP
        r["comparisons"] = {}
        for bid, b in bounds.items():
            ratio = r["tau_s"] / b["bound_s"]
            r["comparisons"][bid] = {
                "tau_over_bound": ratio,
                "bound_over_tau": 1.0 / ratio,
                "orders_above_bound": math.log10(ratio),
                "margin_orders_below_bound": -math.log10(ratio),
                "P1_not_excluded_conditionally": ratio <= 1.0,
            }

    omega_sr = next(p["omega_rad_s"] for p in full["P1"]["platforms"] if p["id"] == "sr87_kim2025")
    alt = full["tau_star_alternatives"]
    alt_checks = {
        "unruh_g": {"computed_Gamma_Sr_per_s": gamma(2.0 * math.pi * C / G_STD, omega_sr), "sealed": alt["unruh_g_Gamma_Sr_per_s"]},
        "earth": {"computed_Gamma_Sr_per_s": gamma(GM_EARTH / C**3, omega_sr), "sealed": alt["GM_earth_over_c3_Gamma_Sr_per_s"]},
        "sr_atom": {"computed_Gamma_Sr_per_s": gamma(G_CORE * 87.0 * M_U / C**3, omega_sr), "sealed": alt["Gm_atom_over_c3_Gamma_Sr_per_s"]},
    }
    for name, check in alt_checks.items():
        check["relative_difference"] = abs(check["computed_Gamma_Sr_per_s"] - check["sealed"]) / check["sealed"]
        assert check["relative_difference"] < 2e-12, (name, check)

    frequencies = {
        "sqrt2_over_tP": math.sqrt(2.0) / TP,
        "2_over_tP": 2.0 / TP,
        "2_over_beta_tP": 2.0 / (BETA * TP),
        "ratio_canonical_to_self_consistent": 1.0 / BETA,
        "beta": BETA,
        "exponent_2beta_over_3": 2.0 * BETA / 3.0,
    }

    systems: list[dict[str, Any]] = []

    def add_system(sid: str, label: str, energy_J: float | None, tau_hor: float, note: str) -> None:
        row = {
            "id": sid,
            "label": label,
            "energy_J": energy_J,
            "tau_horizon_monopole_s": tau_hor,
            "tau_max_s": max(TP, tau_hor),
            "tau_sum_s": TP + tau_hor,
            "tau_quadrature_s": math.hypot(TP, tau_hor),
            "cstar_max": max(TP, tau_hor) / TP,
            "horizon_over_tP": tau_hor / TP,
            "note": note,
        }
        systems.append(row)

    e_sr_optical = HBAR * omega_sr
    e_sr_rest = 87.0 * M_U * C**2
    add_system("one_eV", "sistema de 1 eV", EV, 4.0 * math.pi * G * EV / C**5, "horizonte do próprio E; max devolve Planck")
    add_system("sr_optical", "Sr, energia da transição P1", e_sr_optical, 4.0 * math.pi * G * e_sr_optical / C**5, "a energia é lida do ω selado; max devolve Planck")
    add_system("sr_rest", "Sr, massa de repouso A·m_u", e_sr_rest, 4.0 * math.pi * G * e_sr_rest / C**5, "aproximação A=87 do protocolo; max devolve Planck")
    tau_bh_k1 = 60.0 * GM_SUN / C**3
    add_system("bh60", "remanescente de 60 M☉", None, 4.0 * math.pi * tau_bh_k1, "τhor=4πGM/c³; GM/c³ também fica registrado")
    e_hubble_critical = C**5 / (2.0 * G * H0)
    add_system("hubble", "horizonte de Hubble, densidade crítica", e_hubble_critical, 2.0 * math.pi / H0, "E_H=c⁵/(2GH0), logo τhor=2π/H0; não deriva K")
    bh = next(s for s in systems if s["id"] == "bh60")
    bh["GM_over_c3_s"] = tau_bh_k1
    hub = next(s for s in systems if s["id"] == "hubble")
    hub["H0_per_s"] = H0
    hub["one_over_H0_s"] = 1.0 / H0
    hub["Gamma_over_H0_if_omega_eq_H0_tau_max"] = gamma(hub["tau_max_s"], H0) / H0
    hub["K_law_status"] = "K=E(z*)^(2β/3) vem de TheFlowLawContrast, não de τmax"

    inventory_non_numeric = [
        {"item": "KMS/Unruh genérico", "reason": "exige aceleração/temperatura/energia de referência"},
        {"item": "ancoragem no produto cruzado", "reason": "localiza uma escala possível, não seu valor"},
        {"item": "autofrequência Γ_B=β/τ★", "reason": "identidade em ω★=√2/τ★; não fixa τ★"},
        {"item": "rota autoconsistente ω=2/τ★", "reason": "fixa frequência dada τ★, não τ★"},
        {"item": "Grande Atrator M=M", "reason": "autoconsistência, não nova escala"},
        {"item": "disco de Euler E★=(ħ²K)^(1/3)", "reason": "K e o disco físico não são fornecidos"},
        {"item": "lei de raízes", "reason": "τ★ cancela na transposição; não fixa escala"},
        {"item": "forma Γ=½βτ★ω²", "reason": "a forma não fixa τ★"},
    ]

    sources = [
        CORE,
        NOS / "um.py",
        NOS / "tgl_kernel" / "TGLExt" / "PontoZeroDoPsion.lean",
        NOS / "tgl_kernel" / "TGLExt" / "TonicaDoHamiltoniano.lean",
        NOS / "tgl_kernel" / "TGLExt" / "TheScaleHasNoFixedPoint.lean",
        NOS / "tgl_kernel" / "TGLExt" / "TheFlowLawContrast.lean",
        NOS / "tgl_kernel" / "TGLExt" / "TriadMaster.lean",
        NOS / "tgl_kernel" / "TGLExt" / "PageInformation.lean",
        NOS / "tgl_kernel" / "TGL" / "AreaScale.lean",
        ROOT / "Central de Patentes" / "memory" / "TGL_ATLAS.md",
        ROOT / "Central de Patentes" / "memory" / "INVENTARIO_BANCADA_CHATGPT.md",
        MEM / "e0-cadeia-conferencia-kimi-e-no-go-31out.md",
        MEM / "missao-relogios-v369.md",
        MEM / "cinco-sigma-fora-da-cosmologia-27out.md",
        MEM / "ramo-b-reaberto-05out.md",
        KIMI / "TAU_ESTRELA.md",
        KIMI / "ERRATA_K02.md",
        KIMI / "K02" / "medidas_tau.json",
        KIMI / "ORDEM_K05_matematica_rodada_2.md",
        KIMI / "ORDEM_K05_ADENDO_A_o_campo_e_as_duas_equacoes.md",
        ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "PERGUNTA_TAU_ESTRELA_nas_quatro_linguas_13nov.md",
        ROOT / "Central de Patentes" / "work" / "cadeia_de_selo" / "v412" / "revisao" / "REVISAO_K02.md",
        BASE / "medir_tau_r2.py",
        BASE / "candidatas" / "TAU_ESTRELA_R2.lean",
        BASE / "sandbox" / "logs" / "TAU_ESTRELA_R2.log",
    ]

    payload = {
        "status": "REAL_COMPUTED_FROM_DECLARED_INPUTS_AND_SEALED_RECORDS_NO_NEW_OBSERVED_STATISTIC",
        "beta_formula": "ALPHA_FINE_CODATA_2018 * sqrt(e)",
        "constants": {
            "alpha_CODATA2018": ALPHA, "beta": BETA, "h_J_s": H, "hbar_J_s": HBAR,
            "c_m_s": C, "G_CODATA2018": G, "one_eV_J": EV, "tP_computed_s": TP,
            "EP_computed_J": EP, "EP_over_1eV": EP / EV, "m_u_kg": M_U,
            "GM_earth": GM_EARTH, "GM_sun_nominal": GM_SUN, "standard_g": G_STD,
            "H0_benchmark_per_s": H0,
        },
        "protocol": {
            "hash": protocol["protocol_hash"],
            "status": protocol["record"]["status"],
            "P3": protocol["record"]["readings"]["P3_UNIVERSAL"],
            "tau_star_alternatives_text": protocol["record"]["tau_star_alternatives"],
        },
        "bounds": bounds,
        "readings": readings,
        "alternative_Gamma_consistency_checks": alt_checks,
        "frequencies_per_s": frequencies,
        "regime_candidates": {
            "definitions": {
                "max": "tau_eff=max(tP,tau_hor)",
                "sum": "tau_eff=tP+tau_hor",
                "quadrature": "tau_eff=sqrt(tP^2+tau_hor^2)",
                "tau_hor_monopole": "4πGE/c^5",
            },
            "systems": systems,
        },
        "inventory_non_numeric": inventory_non_numeric,
        "observability": {
            "largest_constant_candidate": "c_inv_beta",
            "Sr_Kim_margin_orders_for_largest_candidate": next(r for r in readings if r["id"] == "c_inv_beta")["comparisons"]["sr87_kim2025"]["margin_orders_below_bound"],
            "Zn_margin_orders_for_largest_candidate": next(r for r in readings if r["id"] == "c_inv_beta")["comparisons"]["zn67_potzel1976"]["margin_orders_below_bound"],
            "current_P1_distinguishes_constant_candidates": False,
            "scope": "P1 conditional upper bounds; passa = não excluído, não detectado nem confirmado",
        },
        "source_sha256": {str(p): sha256(p) for p in sources},
    }
    out = MED / "medidas_tau_r2.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# Tabelas geradas por `medir_tau_r2.py`\n")
    lines.append("## Cotas\n")
    lines.append("| plataforma/registro | cota τ★ (s) | tipo |")
    lines.append("|---|---:|---|")
    for b in bounds.values():
        lines.append(f"| {b['label']} | `{mdnum(b['bound_s'])}` | {b['kind']} |")
    lines.append("\nAs células abaixo mostram `τ/cota` e `log10(τ/cota)`: valor positivo = falha P1 condicional; negativo = passa sem ser detectado.\n")
    groups = [
        ("Sr Kim 95 %", "sr87_kim2025", "Sr Ma nominal", "sr87_ma2025", "Al nominal", "al27_clements2020"),
        ("Th Morawetz 95 %", "th229_morawetz2026", "Th Ooi 95 %", "th229_ooi2026", "Zn nominal", "zn67_potzel1976"),
    ]
    for title1, id1, title2, id2, title3, id3 in groups:
        lines.append(f"| leitura | τ (s) | {title1} | {title2} | {title3} |")
        lines.append("|---|---:|---:|---:|---:|")
        for r in readings:
            cells = []
            for bid in (id1, id2, id3):
                comp = r["comparisons"][bid]
                mark = "PASSA" if comp["P1_not_excluded_conditionally"] else "FALHA"
                cells.append(f"{mdnum(comp['tau_over_bound'], 2)}; {comp['orders_above_bound']:+.2f}; {mark}")
            lines.append(f"| {r['label']} | `{mdnum(r['tau_s'])}` | " + " | ".join(cells) + " |")
        lines.append("")
    lines.append("| leitura | Atlas auxiliar 1,8×10^-33 s: τ/cota; ordens; veredito |")
    lines.append("|---|---:|")
    for r in readings:
        comp = r["comparisons"]["atlas_legacy_1p8e_m33"]
        mark = "PASSA" if comp["P1_not_excluded_conditionally"] else "FALHA"
        lines.append(f"| {r['label']} | {mdnum(comp['tau_over_bound'], 2)}; {comp['orders_above_bound']:+.2f}; {mark} |")

    lines.append("\n## Frequências com τ=tP\n")
    lines.append("| premissa | frequência (rad/s) |")
    lines.append("|---|---:|")
    lines.append(f"| ω★=√2/τ★ | `{mdnum(frequencies['sqrt2_over_tP'])}` |")
    lines.append(f"| autoconsistência sem β: ω=2/τ★ | `{mdnum(frequencies['2_over_tP'])}` |")
    lines.append(f"| Γ=ω com a lei canônica: ω=2/(βτ★) | `{mdnum(frequencies['2_over_beta_tP'])}` |")
    lines.append(f"| razão canônica/autoconsistente = 1/β | `{mdnum(frequencies['ratio_canonical_to_self_consistent'])}` |")

    lines.append("\n## Candidatas de dois regimes\n")
    lines.append("| sistema | τhor=4πGE/c⁵ (s) | max(tP,τhor) (s) | soma (s) | quadratura (s) | max/tP |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for s in systems:
        lines.append(f"| {s['label']} | `{mdnum(s['tau_horizon_monopole_s'])}` | `{mdnum(s['tau_max_s'])}` | `{mdnum(s['tau_sum_s'])}` | `{mdnum(s['tau_quadrature_s'])}` | `{mdnum(s['cstar_max'])}` |")
    lines.append(f"\nPara 60 M☉, `GM/c³={mdnum(tau_bh_k1)} s`; o 4π do monopolo está na tabela. Para Hubble, `1/H0={mdnum(1/H0)} s`, `2π/H0={mdnum(2*math.pi/H0)} s`, e, se ω=H0, `Γ/H0={mdnum(hub['Gamma_over_H0_if_omega_eq_H0_tau_max'])}`; `2β/3={mdnum(2*BETA/3)}`. São quantidades distintas.\n")
    (MED / "tabelas_tau_r2.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "output": str(out), "tables": str(MED / "tabelas_tau_r2.md"),
        "beta": BETA, "tP_s": TP, "n_readings": len(readings), "n_bounds": len(bounds),
        "Sr_Kim_gap_orders": next(r for r in readings if r["id"] == "gap_u")["comparisons"]["sr87_kim2025"]["orders_above_bound"],
        "Sr_Kim_retained_orders": next(r for r in readings if r["id"] == "retido")["comparisons"]["sr87_kim2025"]["orders_above_bound"],
        "alternative_checks_max_relative_difference": max(c["relative_difference"] for c in alt_checks.values()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

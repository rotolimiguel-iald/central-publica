#!/usr/bin/env python3
"""Medidas algébricas para K02; nenhum dado observado é aberto ou ajustado."""
import json
import math
from pathlib import Path

# Entradas publicadas; β NUNCA é literal em runtime.
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
H_EXACT_SI = 6.62607015e-34          # J s, SI 2019 exato
ELEMENTARY_CHARGE_EXACT_SI = 1.602176634e-19  # C, SI 2019 exato
PLANCK_TIME_CODATA_2022 = 5.391247e-44       # s, NIST CODATA 2022

beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
hbar = H_EXACT_SI / (2.0 * math.pi)
one_eV_joule = ELEMENTARY_CHARGE_EXACT_SI  # J, conversão exata
omega_one_eV = one_eV_joule / hbar         # rad/s, ω = E/ħ
nu_one_eV = one_eV_joule / H_EXACT_SI      # Hz, ν = E/h

def gamma(tau):
    return 0.5 * beta * tau * omega_one_eV ** 2

tau_gap = hbar / one_eV_joule
tau_retained = hbar / (beta * one_eV_joule)
result = {
    "status": "REAL_COMPUTED_FROM_DECLARED_INPUTS_NOT_FITTED",
    "beta_formula": "ALPHA_FINE_CODATA_2018 * sqrt(e)",
    "beta": beta,
    "hbar_J_s": hbar,
    "one_eV_J": one_eV_joule,
    "optical_benchmark": "E=1 eV; omega=E/hbar; nenhum relógio/dado observado selecionado",
    "nu_one_eV_Hz": nu_one_eV,
    "omega_one_eV_rad_s": omega_one_eV,
    "readings": {
        "planck": {
            "tau_s": PLANCK_TIME_CODATA_2022,
            "gamma_s^-1": gamma(PLANCK_TIME_CODATA_2022),
            "coherence_time_1_over_gamma_s": 1.0 / gamma(PLANCK_TIME_CODATA_2022),
        },
        "hbar_over_gap_u_1eV": {
            "tau_s": tau_gap,
            "gamma_s^-1": gamma(tau_gap),
            "coherence_time_1_over_gamma_s": 1.0 / gamma(tau_gap),
        },
        "hbar_over_retained_beta_u_1eV": {
            "tau_s": tau_retained,
            "gamma_s^-1": gamma(tau_retained),
            "coherence_time_1_over_gamma_s": 1.0 / gamma(tau_retained),
            "algebraic_check_gamma_equals_omega_over_2": math.isclose(gamma(tau_retained), omega_one_eV / 2.0, rel_tol=1e-14),
        },
    },
    "ratios": {
        "retained_over_planck_tau": tau_retained / PLANCK_TIME_CODATA_2022,
        "gap_over_planck_tau": tau_gap / PLANCK_TIME_CODATA_2022,
        "retained_gamma_over_planck_gamma": gamma(tau_retained) / gamma(PLANCK_TIME_CODATA_2022),
    },
    "declared_neutrino_scale_eV": 1.0,
    "registered_scale_that_would_zero_tension_eV": 1.0200,
    "note": "1.0200 eV é apenas transcrito da ordem; nenhuma tensão, estatística ou ajuste foi recalculado.",
}
out = Path(__file__).resolve().with_name("medidas_tau.json")
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))

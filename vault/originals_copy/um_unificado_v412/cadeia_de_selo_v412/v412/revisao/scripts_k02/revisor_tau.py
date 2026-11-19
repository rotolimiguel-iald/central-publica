#!/usr/bin/env python3
"""Revisor K02, tarefa 7: refaz Gamma = (1/2) beta tau omega^2 em E = 1 eV, independente do script do Kimi.
Nenhum dado observado. beta = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime (nunca literal)."""
import math, json
from decimal import Decimal, getcontext

getcontext().prec = 40
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3      # CODATA 2018
H = 6.62607015e-34                            # J s, exato (SI 2019)
E_CHARGE = 1.602176634e-19                    # C, exato
G_2018 = 6.67430e-11                          # CODATA 2018
C = 299792458.0                               # exato
T_PLANCK_CODATA = 5.391247e-44                # CODATA 2018/2022

beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
hbar = H / (2 * math.pi)
E = E_CHARGE                                  # 1 eV em J
omega = E / hbar
t_p_calc = math.sqrt(hbar * G_2018 / C**5)    # conferencia de t_Planck por G, c, hbar

def gamma(tau, w=omega):
    return 0.5 * beta * tau * w * w

out = {"beta": beta, "hbar": hbar, "omega_1eV": omega, "t_Planck_from_G_c_hbar": t_p_calc,
       "t_Planck_codata": T_PLANCK_CODATA,
       "t_Planck_rel_diff": (t_p_calc - T_PLANCK_CODATA) / T_PLANCK_CODATA}
for nome, tau in (("planck", T_PLANCK_CODATA), ("planck_calc", t_p_calc),
                  ("hbar_over_1eV", hbar / E), ("hbar_over_beta_1eV", hbar / (beta * E))):
    g = gamma(tau)
    out[nome] = {"tau_s": tau, "Gamma_s-1": g, "1_over_Gamma_s": 1 / g, "Gamma_over_omega": g / omega}

# alta precisao (Decimal) para os dois casos que dependem de cancelamento algebrico
D = Decimal
alpha = D("7.2973525693e-3"); e_ = D(1).exp(); beta_d = alpha * e_.sqrt()
pi = D("3.14159265358979323846264338327950288419716939937510")
hbar_d = D("6.62607015e-34") / (2 * pi); E_d = D("1.602176634e-19"); w_d = E_d / hbar_d
tau_ret = hbar_d / (beta_d * E_d)
out["dec_Gamma_retained"] = str(D("0.5") * beta_d * tau_ret * w_d * w_d)
out["dec_omega_over_2"] = str(w_d / 2)
out["dec_Gamma_gap"] = str(D("0.5") * beta_d * (hbar_d / E_d) * w_d * w_d)
out["dec_beta_omega_over_2"] = str(beta_d * w_d / 2)

# Ordem de grandeza da gerencia: relogio optico (nu ~ 4e14 Hz, omega ~ 2.5e15 rad/s) com tau = t_P
w_clock = 2 * math.pi * 4.29e14               # ordem de grandeza generica, sem dado de relogio
out["clock_generic"] = {"omega": w_clock, "Gamma_planck": gamma(T_PLANCK_CODATA, w_clock),
                        "Gamma_hbar_over_beta_eV": gamma(hbar / (beta * E), w_clock)}

# Leitura autoconsistente do kernel:  hbar*w = hbar*(1/2)*tau*w^2  => w = 2/tau   (SEM beta)
# Com a lei canonica COM beta, Gamma = w  =>  w = 2/(beta*tau).
tau = T_PLANCK_CODATA
out["autoconsistente"] = {"omega_kernel_2_over_tau": 2 / tau, "omega_com_beta_2_over_(beta_tau)": 2 / (beta * tau),
                          "razao": (2 / (beta * tau)) / (2 / tau)}
print(json.dumps(out, indent=2, ensure_ascii=False))

"""Revisao K01 - contas de DESENHO refeitas pelo revisor (nenhum dado observado de teste).

Insumos lidos por script:
 - alpha CODATA 2018 = 7.2973525693e-3 (constante publica; beta em runtime = alpha * sqrt(e))
 - core: um_absoluto.json -> neutrino_m2, h0dn_bg1_v411.values, neff_channel, clock_test_result_v369
 - PODER_RAMO_B_ANTES_DE_ABRIR.json (planejamento do ramo B, sem dado)
 - numeros publicos JUNO (7,388 +- 0,078; 7,50 +- 0,12) e tabela 6 do arXiv:2204.13249 (conferida por pdftotext)
"""
import io
import json
import math
from statistics import NormalDist

ND = NormalDist()
CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
RING = r"C:\IALD\Central de Patentes\work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json"
core = json.load(io.open(CORE, encoding="utf-8"))["core"]
ring = json.load(io.open(RING, encoding="utf-8"))

ALPHA = 7.2973525693e-3
beta = ALPHA * math.sqrt(math.e)
D90 = 5.0 + ND.inv_cdf(0.90)
print("beta runtime        =", repr(beta), " | core beta =", core["neutrino_m2"]["values"]["beta"],
      " | dif rel =", abs(beta / core["neutrino_m2"]["values"]["beta"] - 1))
print("D90 = 5+z(0,90)     =", repr(D90))

# ---------------- m2 / JUNO ----------------
m2 = beta * math.sin(math.pi / 4) * 1e3          # meV
pred = (m2 * 1e-3) ** 2 / 1e-5                   # em unidades de 1e-5 eV^2
print("\n== m2/JUNO")
print("m2_pred (meV)       =", repr(m2), " | core:", core["neutrino_m2"]["values"]["m2_pred_meV"])
print("dm2_pred (1e-5 eV2) =", repr(pred))

def D_abs(c, s):
    return abs(c - pred) / s

c207, s207 = 7.388, 0.078
c59, s59 = 7.50, 0.12
gap = abs(c207 - pred) / c207
print("gap relativo ao centro 207d =", gap)
print("D(207d, sigma pub 0,078)   =", D_abs(c207, s207))
print("D(59d, sigma pub 0,12)     =", D_abs(c59, s59))
print("r para 5 sigma (Dm2-space) =", gap / 5, " | para D90 =", gap / D90)
for r in (0.005, 0.003):
    print(f"D a {r*100:.1f}% (relativo ao centro 7,388) =", gap / r)
print("sigma_abs p/ 5 sigma = %.5f e-5 ; p/ D90 = %.5f e-5" % (abs(c207 - pred) / 5, abs(c207 - pred) / D90))
# Tabela 6 de arXiv:2204.13249 (conferida): 6 anos -> sigma = 0,024e-5 (0,3% de 7,53); 100 d -> 0,074; 20 a -> 0,017
for nome, s in (("tabela6 100 dias", 0.074), ("tabela6 6 anos", 0.024), ("tabela6 20 anos", 0.017)):
    print(f"D com {nome}: sigma={s} -> D = {D_abs(c207, s):.4f}  | sigma/7,388 = {s/7.388*100:.4f} %  | sigma/7,53 = {s/7.53*100:.4f} %")
print("0,3% de 7,388 =", 0.003 * 7.388, " (a tabela 6 da 0,024 absoluto: ", 0.024 / 7.388 * 100, "% do centro de 7,388)")

# versao no espaco m2 (regra congelada do core: |m2_obs - m2_TGL| / sigma_m2, sigma_m2 = sigma_dm2/(2 m2_obs))
m2obs = math.sqrt(c207 * 1e-5) * 1e3
sig_m2 = (s207 * 1e-5) / (2 * math.sqrt(c207 * 1e-5)) * 1e3
print("m2_obs(207d) meV =", m2obs, " sigma_m2 (1a ordem) =", sig_m2, " r_m2-space =", abs(m2obs - m2) / sig_m2,
      " | razao r_m2/r_dm2 =", (abs(m2obs - m2) / sig_m2) / D_abs(c207, s207))
print("precisao core (pct de m2) que mata (NuFIT):", core["neutrino_m2"]["values"]["precisao_que_mata_pct"])

# previsao: se o verdadeiro valor for o centro de 207d, probabilidade de r_P >= k  (so previsao; NAO e estatistica observada)
def p_rp_ge(k, sigP, mu=c207, smu=s207):
    sd = math.sqrt(smu ** 2 + sigP ** 2)
    hi = pred + k * sigP
    lo = pred - k * sigP
    return (1 - ND.cdf((hi - mu) / sd)) + ND.cdf((lo - mu) / sd)

print("\nPrevisao preditiva (verdade ~ N(7,388; 0,078), prior plano) de r_P >= k para P futura:")
for nome, sigP in (("0,5% (0,0369)", 0.005 * 7.388), ("0,3% (0,02216)", 0.003 * 7.388), ("tabela6 6a (0,024)", 0.024)):
    print(f"  sigma_P={nome}: P(rP>=5)={p_rp_ge(5, sigP):.3f}  P(rP>=3)={p_rp_ge(3, sigP):.3f}  P(rP<3)={1-p_rp_ge(3, sigP):.3f}")
# nulo de 'verdade = centro atual' (sem incerteza do centro): rP medio
for nome, sigP in (("0,5%", 0.005 * 7.388), ("0,3%", 0.003 * 7.388), ("tab6 0,024", 0.024)):
    print(f"  se a verdade fosse EXATAMENTE 7,388: <r_P> = {abs(c207-pred)/sigP:.3f} ; P(rP>=5) = {1-ND.cdf(5-abs(c207-pred)/sigP):.3f}")

# KamLAND 2013 (7,54 +0,19/-0,18) como candidato a S independente de JUNO
kl_c, kl_s = 7.54, 0.185
print("\nS candidato KamLAND 2013 (7,54 +-0,185): r_S =", abs(kl_c - pred) / kl_s, " ; sigma relativo =", kl_s / kl_c * 100, "%")
print("PDG2020 (7,53 +-0,18): r =", abs(7.53 - pred) / 0.18)
print("para r_S>=5 com sigma_S=0,185 seria preciso |centro_S - pred| >=", 5 * kl_s, " (centro <", pred - 5 * kl_s, "ou >", pred + 5 * kl_s, ")")
print("sigma_S maximo para r_S>=5 se S ~ centro 7,388:", abs(c207 - pred) / 5, "(%.3f%% de 7,388)" % (abs(c207 - pred) / 5 / 7.388 * 100))

# curva precisao x exposicao (SO ilustrativa, NAO previsao)
print("\nCurva de exposicao (sqrt T a partir de 207,2 d; sem piso de sistematica) -> dias vivos para sigma alvo:")
for alvo in (abs(c207 - pred) / 5, abs(c207 - pred) / D90, 0.024, 0.005 * 7.388, 0.003 * 7.388):
    T = 207.2 * (0.078 / alvo) ** 2
    print(f"  sigma={alvo:.5f}e-5 -> T = {T:.0f} d vivos = {T/365.25:.2f} anos vivos")
print("sigma(59,1d)/sigma(207,2d) =", s59 / s207, " vs sqrt(T) previsto =", math.sqrt(207.2 / 59.1))
print("projecao sqrt(T) de 59,1 d -> 207,2 d daria sigma =", s59 * math.sqrt(59.1 / 207.2), " (publicado 0,078)")
print("tabela6: sigma(100 d)=0,074 ; sqrt(T) a 207,2 d daria", 0.074 * math.sqrt(100 / 207.2), " vs publicado 0,078 -> razao", 0.078 / (0.074 * math.sqrt(100 / 207.2)))
# ajuste a/T + s^2 com os dois pontos publicados (ilustrativo)
a = (s59 ** 2 - s207 ** 2) / (1 / 59.1 - 1 / 207.2)
s2 = s207 ** 2 - a / 207.2
print("ajuste de 2 pontos sigma^2 = a/T + s0^2: a =", a, " s0^2 =", s2, " s0 =", math.sqrt(s2) if s2 > 0 else None,
      " (ilustrativo: 2 pontos, 2 parametros, analises diferentes)")

# ---------------- Hubble ----------------
print("\n== Hubble K")
h = core["h0dn_bg1_v411"]["values"]
K = h["K"]
Ez = h["E_zstar"]
bz = beta
Kcalc = Ez ** (2 * bz / 3)
print("K core =", K, " K calculado E^(2b/3) =", Kcalc, " dif =", abs(K - Kcalc))
print("K-1 =", K - 1, " | sigma_rel_total p/ D90 =", (K - 1) / D90, " | p/ 5 sigma =", (K - 1) / 5)
sbg = 0.30 / 68.53106407925104
print("sigma_rel do fundo (0,30/68,53) =", sbg, " -> sigma_rel local maximo p/ D90 =", math.sqrt(((K - 1) / D90) ** 2 - sbg ** 2),
      " ; p/ 5 sigma =", math.sqrt(((K - 1) / 5) ** 2 - sbg ** 2))
print("H0 local previsto =", h["lei_em_km_s_Mpc"]["previsao_de_K_para_o_local"])
for nome, sl in (("H0DN base 1,1%", 0.011), ("H0DN todos 0,9%", 0.009)):
    st = math.sqrt(sl ** 2 + sbg ** 2)
    print(f"  {nome}: sigma_tot={st:.5f} -> D={(K-1)/st:.3f}")

# ---------------- N_eff ----------------
print("\n== N_eff")
dN = core["neff_channel"]["values"]["Delta_Neff"]
print("Delta N_eff core =", dN, "| beta*? check: ", )
print("D(0,045) =", dN / 0.045, " D(0,03) =", dN / 0.03, " sigma p/ D90 =", dN / D90, " p/ 5 =", dN / 5)
print("core escada SO-ASO:", [ (e['sigma_Neff'], e['tensao_projetada']) for e in core['neff_channel']['values']['escada_projetada']])

# ---------------- Ringdown ----------------
print("\n== Ringdown")
pw = ring["poder_sem_incerteza_do_vies"]
D10 = pw["D10_sem_hold__sigma_sys_0.000__info_esperada"]["poder"]
D14 = pw["D14_com_holds__sigma_sys_0.000__info_esperada"]["poder"]
print("D10 =", D10, " D14 =", D14)
print("fator de informacao D10->D90 =", (D90 / D10) ** 2, " D14->D90 =", (D90 / D14) ** 2)
print("eventos equivalentes (info ~ N): de D10:", 10 * (D90 / D10) ** 2, " de D14:", 14 * (D90 / D14) ** 2)
print("com viés (C2 infinita limite, sys 0,029, info esperada):", ring["poder_com_incerteza_do_vies_D10"]["sigma_sys_0.029__info_esperada"]["C2_infinita_limite"]["poder"])

# ---------------- Coma / relogios / Sigma m_nu ----------------
print("\n== Coma e relogios")
coma = core["coma_distance_dephasing"]["prediction"]
dc = abs(coma["control_D_L_planck_median_Mpc"] - coma["D_L_TGL_median_Mpc"])
print("Coma delta fiducial (Mpc) =", dc, " sigma p/ D90 =", dc / D90)
cl = core["clock_test_result_v369"]["P1"]
for pl in cl["platforms"]:
    if pl["id"] in ("sr87_kim2025", "th229_ooi2026"):
        print(pl["id"], "Gamma_pred =", pl["Gamma_pred_per_s"], " Z_exp =", pl.get("Z_expected"), " deficit5s =", pl.get("deficit_orders_5sigma_detect"),
              " deficit_bound =", pl.get("deficit_orders_bound"), " sigma p/ D90 =", pl["Gamma_pred_per_s"] / D90)
print("Sigma m_nu: D = 0,000199/0,03 =", 0.000199 / 0.03, "; /0,015 =", 0.000199 / 0.015, "; sigma p/ D90 =", 0.000199 / D90)

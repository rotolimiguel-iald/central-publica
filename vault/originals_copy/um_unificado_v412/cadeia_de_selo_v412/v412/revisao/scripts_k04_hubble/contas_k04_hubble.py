"""Revisor K04/Hubble: recomputa as contas de planejamento do Kimi de forma independente.
Insumos: core (so leitura: K, E_zstar, Omega_m, Omega_r, z_star, H0_fundo), tabela do Kimi (H0, sigma) copiada do JSON do Kimi (so leitura).
Nenhum vetor de dado. beta = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime.
"""
import io
import json
import math
from pathlib import Path

CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
KIMI = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K04\HUBBLE\MEDIDAS_PLANEJAMENTO_K04.json"
OUT = Path(__file__).resolve().parent

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)

core = json.load(io.open(CORE, encoding="utf-8"))["core"]["h0dn_bg1_v411"]["values"]
Om, Or, zs = core["Omega_m"], core["Omega_r"], core["z_star"]
OL = 1.0 - Om - Or
E_rec = math.sqrt(Om * (1 + zs) ** 3 + Or * (1 + zs) ** 4 + OL)
K_rec = E_rec ** (2 * beta / 3)

print("beta runtime        =", repr(beta), "| core:", repr(core["beta"]), "| dif rel:", (beta - core["beta"]) / beta)
print("E(z*) recomputado   =", repr(E_rec), "| core:", repr(core["E_zstar"]), "| dif rel:", (E_rec - core["E_zstar"]) / core["E_zstar"])
print("K recomputado       =", repr(K_rec), "| core:", repr(core["K"]), "| K-1 (rec):", repr(K_rec - 1))
K1 = K_rec - 1

# D90 = 5 + z(0.90): z(0.90) por bissecao na normal
def phi(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))
lo, hi = 0.0, 3.0
for _ in range(200):
    mid = (lo + hi) / 2
    if phi(mid) < 0.90:
        lo = mid
    else:
        hi = mid
D90 = 5 + lo
print("D90                 =", repr(D90))

BG_H0, BG_S = 68.53, 0.30
sb = BG_S / BG_H0
print("sigma_BG1 rel       =", sb)
print("core H0_fundo       =", core["lei_em_km_s_Mpc"]["H0_fundo"], "previsao_K_local =", core["lei_em_km_s_Mpc"]["previsao_de_K_para_o_local"])

for nome, Dalvo in (("5sigma", 5.0), ("D90", D90)):
    s_tot = K1 / Dalvo
    s_loc = math.sqrt(s_tot ** 2 - sb ** 2)
    print(f"requisito {nome}: sigma_total <= {100*s_tot:.5f} % ; sigma_local <= {100*s_loc:.5f} %  (Kimi: ver MD)")

# D da H0DN / outras
def D_de(sig_rel):
    return K1 / math.hypot(sig_rel, sb)

kimi = json.load(io.open(KIMI, encoding="utf-8"))
print()
print(f"{'id':22s} {'sig_rel_Kimi %':>14s} {'sig_rel_rev %':>14s} {'D_Kimi':>9s} {'D_rev':>9s} {'dif':>10s}")
maxdif = 0.0
linhas = []
for r in kimi["medidas"] + kimi["previsoes"]:
    if "sigma_rel" in r and r.get("h0") is None:
        sr = r["sigma_rel"]
    else:
        sr = r["sigma"] / r["h0"]
    d_rev = D_de(sr)
    dif = d_rev - r["D_desenho"]
    maxdif = max(maxdif, abs(dif))
    linhas.append((r["id"], 100 * r["sigma_local_relativa"], 100 * sr, r["D_desenho"], d_rev, dif))
    print(f"{r['id']:22s} {100*r['sigma_local_relativa']:14.4f} {100*sr:14.4f} {r['D_desenho']:9.4f} {d_rev:9.4f} {dif:10.2e}")
print("max |dif D| =", maxdif)

# conferencia dos sigma de entrada compostos (stat+sys em quadratura) contra o publicado
print()
comp = {
    "cchp_trgb": math.sqrt(1.22 ** 2 + 1.33 ** 2 + 0.70 ** 2),
    "sbf_trgb": math.sqrt(0.7 ** 2 + 2.3 ** 2),
    "sn2_dejaeger": math.sqrt(3.8 ** 2 + 1.5 ** 2),
    "bbh_agn": math.sqrt(3.37 ** 2 + 1.56 ** 2),
    "bbh_agn_extended": math.sqrt(2.55 ** 2 + 1.54 ** 2),
}
for k, v in comp.items():
    print("sigma composto", k, v)

# H0DN: o D desenho contra o D do core
print()
print("H0DN baseline sigma_rel =", 0.81 / 73.50, " D =", D_de(0.81 / 73.50), "| core primario D =", 6.710150598579069, "| core cefeidas livres D =", 5.19131201002441)
print("H0DN V99 sigma_rel = ", 0.697 / 73.994, " D =", D_de(0.697 / 73.994))
# SH0ES JWST: falta para D90 (em D)
print("SH0ES JWST D =", D_de(0.93 / 73.49), " D90-D =", D90 - D_de(0.93 / 73.49))
# SN II tailored EPM; so stat; requisito: de quanto precisa melhorar o sigma local para D90
for nome, h, s in (("SN II EPM stat", 74.9, 1.9), ("TDCOSMO-2026 11", 71.1, 2.4), ("TDCOSMO-2026+SLACS+SL2S", 71.3, 2.2)):
    sr = s / h
    d = D_de(sr)
    lim = math.sqrt((K1 / D90) ** 2 - sb ** 2)
    print(f"{nome}: sigma_rel {100*sr:.3f} % D {d:.4f}; fator de reducao de sigma ate D90: {sr/lim:.3f}; fator de reducao de VARIANCIA (N vezes mais dados): {(sr/lim)**2:.2f}")

# sem o BG1 (so o local): o D nu
print("D se sigma_BG fosse zero, SN II EPM:", K1 / (1.9 / 74.9))

(OUT / "contas_k04_hubble_saida.txt").write_text("rodado; ver stdout\n", encoding="utf-8")

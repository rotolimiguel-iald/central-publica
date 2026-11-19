from datetime import date
O4a = (date(2024,1,16)-date(2023,5,24)).days
O4b = (date(2025,1,28)-date(2024,4,10)).days
print("O4a", O4a, "O4b", O4b)
add10, add14 = 15.487382173506962, 11.68682365979345
# do V1 (tabela l.171-184): O4a: GW230919 (sem hold). O4b: 13 elegiveis, 4 com hold -> 9 sem hold
for nome, n10, n14, dias in (("O4a+O4b (Kimi, 530 d)", 10, 14, O4a+O4b), ("so O4b (293 d)", 9, 13, O4b)):
    r10 = n10/(dias/365.25); r14 = n14/(dias/365.25)
    print(nome, "taxa D10 %.2f/ano, D14 %.2f/ano | tempo D10 %.1f meses, D14 %.1f meses" % (r10, r14, add10/r10*12, add14/r14*12))
print("exigido em 6 meses: D10 %.1f/ano, D14 %.1f/ano" % (add10/0.5, add14/0.5))
# assintota com vies (arquivo PODER_RAMO_B..., sigma_sys_0.029, info_esperada)
poder_sv, sig_sv = 3.917890744965421, 0.1017100985567133
delta_eff = poder_sv*sig_sv
for nome, sv in (("C2_ampla", 0.06864722987593155), ("C2_media", 0.11026750731571908), ("C2_minima", 0.15484582992250984)):
    print("assintota do poder (N->inf) com", nome, "sigma_vies", sv, "=", round(delta_eff/sv, 3), "(D90 = 6,2816; 5 = 5)")

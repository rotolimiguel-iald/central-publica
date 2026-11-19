"""Aritmetica de planejamento do revisor sobre sigmas PUBLICADOS (nenhum vetor; nenhum centro usado para z observado)."""
import math, io, json
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
core = json.load(io.open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json", encoding="utf-8"))["core"]["h0dn_bg1_v411"]["values"]
K1 = core["E_zstar"] ** (2 * beta / 3) - 1
sb = 0.30 / 68.53
D90 = 6.281551565544601
def D(s): return K1 / math.hypot(s, sb)
def comb(*s): return 1 / math.sqrt(sum(1 / x**2 for x in s))
sn2_stat = 1.9 / 74.9
sn2_eq = 1.9 * math.sqrt(2) / 74.9   # sistematica = estatistica (a fonte diz 'comparavel ou menor')
td26 = 2.4 / 71.1
td26x = 2.2 / 71.3
mcp = 3.7 / 71.6
frb = 2.14 / 69.40
bbh = math.hypot(2.55, 1.54) / 69.71
print("SN II EPM: stat D=%.3f ; sys=stat D=%.3f" % (D(sn2_stat), D(sn2_eq)))
print("pilha SN II(stat)+TDCOSMO26: sigma=%.3f%% D=%.3f" % (100*comb(sn2_stat, td26), D(comb(sn2_stat, td26))))
print("pilha SN II(sys=stat)+TDCOSMO26: sigma=%.3f%% D=%.3f" % (100*comb(sn2_eq, td26), D(comb(sn2_eq, td26))))
s5 = comb(sn2_stat, td26, mcp, frb, bbh)
print("pilha 5 linhas (3 so stat): sigma=%.3f%% D=%.3f" % (100*s5, D(s5)))
s5b = comb(sn2_eq, td26, mcp, frb, bbh)
print("pilha 5 linhas (SN II sys=stat): sigma=%.3f%% D=%.3f" % (100*s5b, D(s5b)))
# lentes: escala 1/sqrt(N)
lim5 = math.sqrt((K1/5)**2 - sb**2); limD = math.sqrt((K1/D90)**2 - sb**2)
for nome, s0, n0 in (("TDCOSMO-2026 (11 lentes)", td26, 11),):
    print(nome, "N p/ 5sigma ~", n0 * (s0/lim5)**2, "; N p/ D90 ~", n0 * (s0/limD)**2)
# D de desenho da H0DN: simples vs core
print("H0DN simples (0,81/73,50): %.3f ; core primario D=6.710150598579069 ; cefeidas livres D=5.19131201002441" % D(0.81/73.50))
# quanto o sigma_local da H0DN teria de ser para D do core
s_core = math.sqrt((K1/6.710150598579069)**2 - sb**2)
print("sigma_local equivalente ao D=6.71 do core: %.4f%% (cabecalho 1,102%%)" % (100*s_core))
# probabilidade de D90: D90 = 5 + z(0.9) -> poder 90% de passar 5 sigma

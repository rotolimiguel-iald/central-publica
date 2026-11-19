# -*- coding: utf-8 -*-
"""Revisao K06: contas de bolso para as perguntas 4, 5, 6 e a janela de contexto. Nenhum modelo chamado."""
import json
import math
from pathlib import Path

from scipy.stats import beta, norm, t as student_t

out = {}

# ---- 4. permutacao por sinais com 27 clusters
G = 27
perms = 2 ** G
a5 = float(norm.sf(5.0))
out["perms_2_27"] = perms
out["min_p_1_sobre_2_27"] = 1.0 / perms
out["alpha_5sigma_unilateral"] = a5
out["razao_alpha5_sobre_minp"] = a5 / (1.0 / perms)
out["contagem_maxima_de_padroes_para_p_ate_alpha5"] = math.floor(a5 * perms)
hol = []
for i in range(6):
    thr = a5 / (6 - i)
    hol.append({"passo": i + 1, "limiar_p": thr, "contagem_max": math.floor(thr * perms)})
out["holm6_limiares_ordenados"] = hol
# dois padroes de ties: um cluster com estatistica zero dobra a contagem minima
out["contagem_minima_com_k_clusters_nulos"] = {str(k): 2 ** k for k in range(0, 8)}
out["k_max_clusters_nulos_para_ainda_passar_o_1_passo_do_holm"] = max(k for k in range(0, 10) if 2 ** k <= math.floor((a5 / 6) * perms))
# com so 3 textos como unidade de independencia (se o texto fosse o cluster)
out["min_p_com_3_clusters"] = 1 / 2 ** 3
out["min_p_com_9_clusters"] = 1 / 2 ** 9

# ---- quantil t com 26 gl no nivel 5 sigma versus z=5
out["t26_no_alpha5"] = float(student_t.isf(a5, 26))
out["t26_no_alpha5_sobre_9"] = float(student_t.isf(a5 / 9, 26))

# ---- Monte Carlo: o que 1000 corridas resolvem
def cp(x, n, conf=0.95):
    a = (1 - conf) / 2
    lo = 0.0 if x == 0 else beta.ppf(a, x, n - x + 1)
    hi = 1.0 if x == n else beta.ppf(1 - a, x + 1, n - x)
    return lo, hi

out["zero_em_1000_CP95_superior"] = cp(0, 1000)[1]
out["regra_dos_tres_1000"] = 3 / 1000
out["corridas_para_ver_10_eventos_em_alpha5"] = 10 / a5
out["corridas_para_cota_superior_95_igual_alpha5_com_zero_eventos"] = 3 / a5
# nulo global 0,057 em 1000: precisao e corridas para certificar <= 0,055 se o verdadeiro for 0,05
p0 = 0.05
n_req = (1.645 ** 2) * p0 * (1 - p0) / (0.005 ** 2)
out["corridas_para_cota_superior_95_ate_0_055_se_tamanho_verdadeiro_0_05"] = n_req
out["se_binomial_a_0_05_com_1000"] = math.sqrt(0.05 * 0.95 / 1000)

# ---- 5. custos
rows = []
for nome, n, base_extra in (("base", 320, 163.27), ("5sigma_618", 618, 312.09), ("legado_655", 655, 335.03)):
    prim_s = 20 * n
    prim_i = prim_s * 12
    rows.append({"desenho": nome, "n": n, "sessoes": prim_s, "interacoes": prim_i, "extra": base_extra, "base_mais_extra": prim_i + base_extra})
out["custos"] = rows
out["legado_8_interacoes_655"] = {"sessoes": 20 * 655, "interacoes": 20 * 655 * 8}
# o que seria o adicional se so 3 familias (as inferenciais) forem triadas, sem o fator 4/3
out["fator_4_sobre_3_sobre_o_extra_base"] = 163.27 * 3 / 4

# ---- janela de contexto: o corpus em CADA mensagem do usuario (MODELO_FORMAL 2.2)
T_lo, T_hi = 205298, 291088
saida_max = 2048
jan = {}
for k in (1, 2, 4, 5, 8, 10, 12):
    jan[str(k)] = {"u_copias": k, "tokens_lo": k * T_lo + (k - 1) * saida_max + saida_max, "tokens_hi": k * T_hi + (k - 1) * saida_max + saida_max}
out["contexto_por_leitura_k"] = jan
out["entrada_por_sessao_soma_k_1_12_lo"] = sum(k * T_lo for k in range(1, 13))
out["entrada_por_sessao_soma_k_1_12_hi"] = sum(k * T_hi for k in range(1, 13))
out["entrada_base_6400_sessoes_lo"] = 6400 * out["entrada_por_sessao_soma_k_1_12_lo"]
out["entrada_base_6400_sessoes_hi"] = 6400 * out["entrada_por_sessao_soma_k_1_12_hi"]
out["entrada_5sigma_12360_sessoes_lo"] = 12360 * out["entrada_por_sessao_soma_k_1_12_lo"]
out["entrada_5sigma_13100_sessoes_hi"] = 13100 * out["entrada_por_sessao_soma_k_1_12_hi"]

# ---- teto do extrator: 96 leituras (A8) versus 168 (A8 e RETORNO)
for alvo in (0.89, 0.80):
    out[f"e_max_{alvo}_96"] = 1 - alvo ** (1 / 96)
    out[f"e_max_{alvo}_168"] = 1 - alvo ** (1 / 168)
out["teto_Q_leitor_perfeito_e_0_498pct_96"] = (1 - 0.00498044) ** 96
out["teto_Q_leitor_perfeito_e_0_498pct_168"] = (1 - 0.00498044) ** 168

Path(__file__).with_name("contas_k06.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2, sort_keys=True))

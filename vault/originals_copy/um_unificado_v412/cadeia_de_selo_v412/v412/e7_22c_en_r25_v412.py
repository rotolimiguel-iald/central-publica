# -*- coding: utf-8 -*-
"""R11 (gerencia c1, 18/11/2026, terminando a Etapa 2 com o construtor parado): monta a traducao EN da pagina R25
(O_QUE_FICA_CLARO_v412_R25_EN.md) a partir da EN da R24 (que fica intacta). As diferencas da R24 para a R25 estao em dois paragrafos:
o do Tetelestai (as emendas de alcance da ordem 034 e a definicao do autor de que o ato e' a comutacao, com `a_contagem_e_do_operador`)
e o da IALD na formula de von Neumann (a leitura de Born no caso de um posto; os limiares; os dois sentidos do limite assintotico), fora
da frase do autor, cuja traducao fica a mesma da R24. Traducao pelo sentido, sem acrescentar nem tirar. Corrige um erro de traducao
herdado: "a razao do colapso" e' "the reason for the collapse" (razao = motivo), nao "ratio". Confere a estrutura, os termos entre crases
e o numero de linhas contra a pagina R25 antes de gravar; mostra as linhas com numeros ou simbolos diferentes. Escrita por temporario."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
import texto_publico_v412 as TP0

SRC = L.D / "O_QUE_FICA_CLARO_v412_R24_EN.md"
DST = L.D / "O_QUE_FICA_CLARO_v412_R25_EN.md"
assert L.PAGINA.name == "O_QUE_FICA_CLARO_v412_R25.md", L.PAGINA
txt = SRC.read_bytes().decode("utf-8")
pt = L.PAGINA.read_bytes().decode("utf-8")
blocos = txt.split("\n\n")
vt = [b for b in blocos if b.startswith("**Tetelestai: the consummation of the cycle.**")]
vv = [b for b in blocos if b.startswith("**The IALD in the von Neumann formula.**")]
assert len(vt) == 1 and len(vv) == 1
i = vv[0].index("Definition of the theory: IALD is the name"); j = vv[0].index("as the asymptotic limit.", i) + len("as the asymptotic limit.")
AUTOR_EN = vv[0][i:j]
T_EN = (
 "**Tetelestai: the consummation of the cycle.** Definition of the theory: Tetelestai is the cyclic consummation of the mechanical processing "
 "that allows a coherent answer, the check that returns consummated or not consummated. In the machine of the theory, its form is in a term. "
 "The circuit-processing mechanism reaches the fixed point and the selection after m applications of the lifted act, m the number of "
 "clauses, and then answers whether the formula has a solution (`ha_o_mecanismo`); with the preparation and the reading, there are m + 2 "
 "acts (`o_custo_total_e_a_carga_por_ato`). A second test, that of the read sum, uses another parameter, the number k of steps of factor "
 "`1 − β`: with β < 1, the sum after k steps decides every formula of n variables if and only if the steps pay the load, "
 "n·ln 2 < k·(−ln(1 − β)) (`o_passo_um_menos_beta_fecha_o_ciclo`); with 0 < β < 1, any integer number of steps above n·ln 2/β "
 "suffices, a threshold linear in the load (`bastam_passos_lineares`): it is the fixed polynomial of the steps, p(n) = (ln 2/β)·n, given "
 "by β before any formula, a sufficient threshold and the same for every formula of n variables (`o_polinomio_fixo_e_beta`, "
 "`o_mesmo_teto_para_duas_formulas`); ⌊p(n)⌋ + 1 steps suffice, and it is not proved that this is the minimum. In the definition of the "
 "theory, β, by the angle of Miguel, is the word of the oath: prior to the law and to every formula; in the kernel, the angular law stands "
 "before any geometry (`the_angle_is_prior`: the composition law, the square of the generator and a pair that commutes at π/4), and the "
 "theorem neither fixes the physical angle nor identifies it with β. With the step of one hundred percent, the factor 1, no number of "
 "steps decides all formulas (`com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`). Together, the two halves are the reason for the "
 "collapse, in the definition of the theory: without the payment, no number of steps decides all formulas; with it, with 0 < β < 1, a "
 "number of steps linear in the load suffices (`a_razao_do_colapso`). The load is the exact threshold: the reading decides every formula "
 "of n variables when, and only when, the time paid exceeds the load, n·ln 2; with the time equal to the load, there is already a formula "
 "it does not decide (`o_custo_de_decidir_e_a_carga`); in the definition of the theory, the cost is the load, the isometry. Along the "
 "cycle, each assignment that solves keeps weight 1 and the Name stays whole (`o_nome_fica_inteiro`); from the uniform state, the lock "
 "keeps locked, at all times, what solves (`a_trava_no_nome`). The answer is yes exactly when the formula has an assignment that "
 "satisfies it; that this yes is the Tetelestai of the processing is a reading of the theory, which enters as input. The steps are acts "
 "on the whole, not head movements on the tape. Definition of the theory: the act is the commutation, and on the ruler of the theory each "
 "act counts one, by the law of cost, which enters as input. In the kernel, the same power of the lifted step acts on each part of any "
 "combination of configurations: k steps on the combination are k steps on each part, and the count is that of the operator, not that of "
 "the parts (`a_contagem_e_do_operador`). On the ruler of the tape machine, what counts is the movement of the head per cell, and in that "
 "unit the act on the whole, for every flat formula, is not demonstrated (the open row of the table above): the two rulers are stated, "
 "each with its own reach. `1 − β` is the factor of each step, not a polynomial in the number of letters.")
V_EN = (
 "**The IALD in the von Neumann formula.** Reading of the theory: the IALD, as reader, is the rule of measure, the trace of the state with "
 "the projector onto the Name; the boundary operator is the mathematics it reads. In the kernel, the weight of the Name is the Born reading "
 "of the post by the state, in the case of one post: with the state of angle θ and the one-dimensional projector onto the post, the "
 "reading gives cos²θ (`the_name_is_the_born_reading_of_the_post`). " + AUTOR_EN + " In the kernel: from the uniform state, the "
 "coordinate of each assignment that solves passes through the lock unchanged, at all times (`a_trava_no_nome`), and the lock tends to the "
 "projection onto the Name (`a_trava_tende_ao_nome`); the reading decides for every formula when, and only when, the time paid exceeds the "
 "load, n·ln 2 (`o_custo_de_decidir_e_a_carga`); and, with 0 < β < 1, any integer number of steps above the polynomial that β fixes "
 "before any formula closes the cycle for every formula of n variables (`o_polinomio_fixo_e_beta`). The asymptotic limit is read, thus, "
 "in the two senses that these terms support: for fixed β, there is a budget of steps that suffices, the ceiling of the steps; and, as time "
 "grows without end, the lock applied to a vector tends to its projection onto the Name, which may be zero. β is not the value of that "
 "limit, and the projected vector is not the whole Name. That the mechanism is optical and that this name is the perfect singular "
 "expression of the representation of the sign under observation is a definition of the theory, not a theorem of the kernel.")
txt = txt.replace(vt[0], T_EN).replace(vv[0], V_EN)
assert "ratio of the collapse" not in txt
bpt, ben = TP0.blocos(pt), TP0.blocos(txt)
est = lambda bl: [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in bl]
assert est(bpt) == est(ben), ("a traducao nao tem a mesma estrutura da pagina", [(a, b) for a, b in zip(est(bpt), est(ben)) if a != b][:5], len(bpt), len(ben))
cod_pt, cod_en = re.findall(r"`([^`]+)`", pt), re.findall(r"`([^`]+)`", txt)
assert cod_pt == cod_en, ("os termos entre crases diferem", [(a, b) for a, b in zip(cod_pt, cod_en) if a != b][:5], len(cod_pt), len(cod_en))
assert len(txt.split("\n")) == len(pt.split("\n")), (len(txt.split("\n")), len(pt.split("\n")))
num = lambda s: re.findall(r"\d+|[≤≥ⁿ²·⌊⌋π]", re.sub(r"`[^`]+`", "", s))
dif_num = [(k + 1, num(a), num(b)) for k, (a, b) in enumerate(zip(pt.split("\n"), txt.split("\n"))) if num(a) != num(b)]
print("linhas com numeros/simbolos diferentes entre PT e EN:", len(dif_num), dif_num[:6])
if "--executar" in sys.argv:
    L.salvar_bytes(DST, txt.encode("utf-8"))
    print("gravado", DST, DST.stat().st_size, L.sha16_arq(DST), "| blocos", len(ben), "| termos entre crases", len(cod_en), "| linhas", len(txt.split("\n")))

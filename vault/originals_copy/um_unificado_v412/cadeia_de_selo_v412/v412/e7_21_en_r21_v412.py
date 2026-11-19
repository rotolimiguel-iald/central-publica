"""R7: monta a traducao EN da pagina R21 (O_QUE_FICA_CLARO_v412_R21_EN.md) a partir da EN da R18 (O_QUE_FICA_CLARO_v412_R18_EN.md, que fica intacta). As diferencas da R18 para a R21 (medidas por e7_20_diff_r18_r21_v412.py) sao:
uma oracao no paragrafo de citacao (os pivos terminam num nome fora dos dois); duas linhas da tabela (a fita e o indice; a recusa); a ultima frase da secao 2 antes do bloco novo (a torre e' a forma do indice); e um paragrafo novo
(“Tetelestai: a consumacao do ciclo”). Traducao fiel: mesma estrutura, mesmos termos entre crases na mesma ordem, nomes de termos e de modulos intactos. Confere a estrutura e os termos contra a pagina R21 antes de gravar.
Escrita por temporario; backup de bytes."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
import texto_publico_v412 as TP0   # (so' a funcao blocos, para comparar a estrutura)

SRC = L.D / "O_QUE_FICA_CLARO_v412_R18_EN.md"
DST = L.D / "O_QUE_FICA_CLARO_v412_R21_EN.md"
txt = SRC.read_bytes().decode("utf-8")
pt = L.PAGINA.read_bytes().decode("utf-8")

TROCAS = [
    ("binary clauses that begin with one of two pivots)", "binary clauses that begin with one of two pivots and end in a name outside the two)"),
    ("| the tape is the index: every position has to be read, and the same name carries the same value | `quem_nao_visita_nao_le`: a reader blind to one position gives the same answer to two tapes with opposite answers; it is the bound of reading the whole input. "
     "`sat_formulaDa` and `a_coreferencia_obriga_o_transporte`: in a family of two unit clauses on the same variable, there is a solution if and only if the two positions read agree | `AFitaEOIndice` |",
     "| the tape is the index: the answer depends on the position that the coreference designates, and the same name carries the same value | `quem_nao_visita_nao_le`: for p ≠ 0, a reader insensitive to the sign at p confuses two tapes of this family of two unit clauses. "
     "`sat_formulaDa`: there is a solution if and only if f(0) = f(p); `a_coreferencia_obriga_o_transporte`: then every witness assigns this value to variable 0. The term does not count positions visited | `AFitaEOIndice` |"),
    ("an occurrence of a violated clause of the block that answers. `reuses_clause`", "an occurrence of a violated clause of the block that answers; the definition `Codex.ClauseReply.run` uses this occurrence to form the next call. `reuses_clause`"),
    ("that the truth is the contour and that the tape is the index and the tower are definitions of the theory, which enter as input.", "that the truth is the contour, that the tape is the index and that the tower is the form of the index are definitions of the theory, which enter as input."),
]
TETELESTAI = ("**Tetelestai: the consummation of the cycle.** Definition of the theory: Tetelestai is the cyclic consummation of the mechanical processing that allows a coherent answer, the check that returns consummated or not consummated. "
              "In the machine of the theory, its form is in a term. The circuit-processing mechanism closes the circuit in as many acts as there are clauses and, once closed, answers whether the formula has a solution (`ha_o_mecanismo`). "
              "With the step of factor `1 − β`, the sum read after k steps decides every formula of n variables if and only if the steps pay the load, n·ln 2 < k·(−ln(1 − β)) (`o_passo_um_menos_beta_fecha_o_ciclo`); "
              "with β between 0 and 1, more than n·ln 2/β steps suffice, a number linear in the load (`bastam_passos_lineares`): it is the fixed polynomial of the steps, p(n) = (ln 2/β)·n, given by β before any formula and the same ceiling for every formula of n variables "
              "(`o_polinomio_fixo_e_beta`, `o_mesmo_teto_para_duas_formulas`); with the step of one hundred percent, no number of steps closes the cycle (`com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`). "
              "Together, the two halves are the ratio of the collapse, in the definition of the theory: without the payment the cycle does not close, and with it the cycle closes linearly in the load (`a_razao_do_colapso`). "
              "The cost of deciding is the load, neither more nor less: the reading decides every formula of n variables if and only if the time paid exceeds n·ln 2 (`o_custo_de_decidir_e_a_carga`); in the definition of the theory, the cost is the load, the isometry. "
              "Along the cycle, the assignment that solves keeps weight 1 and the Name stays whole (`o_nome_fica_inteiro`); the lock keeps locked, at all times, what solves (`a_trava_no_nome`). "
              "The answer is yes exactly when the formula has an assignment that satisfies it; that this yes is the Tetelestai of the processing is a reading of the theory, which enters as input. "
              "The steps are acts on the whole, not head movements on the tape, and `1 − β` is the factor of each step, not a polynomial in the number of letters.")
for velho, novo in TROCAS:
    assert txt.count(velho) == 1, ("a EN da R18 nao tem o trecho esperado", velho[:70], txt.count(velho))
    txt = txt.replace(velho, novo)
ancora = "that the tower is the form of the index are definitions of the theory, which enter as input."
assert txt.count(ancora) == 1
i = txt.index(ancora) + len(ancora)
assert txt[i:i + 2] == "\n\n", repr(txt[i:i + 4])
txt = txt[:i] + "\n\n" + TETELESTAI + txt[i:]
# a estrutura e os termos, contra a pagina R21
bpt, ben = TP0.blocos(pt), TP0.blocos(txt)
est = lambda bl: [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in bl]
assert est(bpt) == est(ben), ("a traducao nao tem a mesma estrutura da pagina", [(a, b) for a, b in zip(est(bpt), est(ben)) if a != b][:5], len(bpt), len(ben))
cod_pt, cod_en = re.findall(r"`([^`]+)`", pt), re.findall(r"`([^`]+)`", txt)
assert cod_pt == cod_en, ("os termos entre crases diferem", [(a, b) for a, b in zip(cod_pt, cod_en) if a != b][:5], len(cod_pt), len(cod_en))
assert len(txt.split("\n")) == len(pt.split("\n")), (len(txt.split("\n")), len(pt.split("\n")))
num = lambda s: re.findall(r"\d+|[≤≥ⁿ²·]", re.sub(r"`[^`]+`", "", s))
dif_num = [(i + 1, num(a), num(b)) for i, (a, b) in enumerate(zip(pt.split("\n"), txt.split("\n"))) if num(a) != num(b)]
print("linhas com numeros/simbolos diferentes entre PT e EN:", len(dif_num), dif_num[:6])
L.salvar_bytes(DST, txt.encode("utf-8"))
print("gravado", DST, DST.stat().st_size, L.sha16_arq(DST), "| blocos", len(ben), "| termos entre crases", len(cod_en), "| linhas", len(txt.split("\n")))

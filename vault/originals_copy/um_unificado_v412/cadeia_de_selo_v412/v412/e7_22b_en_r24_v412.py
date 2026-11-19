"""R10: monta a traducao EN da pagina R24 (O_QUE_FICA_CLARO_v412_R24_EN.md) a partir da EN da R22 (que fica intacta). A unica diferenca da R22 para a R24 (medida por e7_20_diff_r18_r21_v412.py 22 24) esta' no paragrafo
“A IALD na formula de von Neumann”: a definicao da IALD na redacao do autor e o que o kernel prova de cada parte (cita `a_trava_no_nome`, `a_trava_tende_ao_nome`, `o_custo_de_decidir_e_a_carga`, `o_polinomio_fixo_e_beta`).
A frase da definicao e' traduzida pelo sentido, sem acrescentar nem tirar. Confere a estrutura e os termos contra a pagina R24 antes de gravar. Escrita por temporario; backup de bytes."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
import texto_publico_v412 as TP0

SRC = L.D / "O_QUE_FICA_CLARO_v412_R22_EN.md"
DST = L.D / "O_QUE_FICA_CLARO_v412_R24_EN.md"
txt = SRC.read_bytes().decode("utf-8")
pt = L.PAGINA.read_bytes().decode("utf-8")
VELHO = ("That the IALD is the matrix form of the polynomial of the steps, read at runtime, is a reading of the theory, which enters as input.")
NOVO = ("Definition of the theory: IALD is the name, because everything has a Name, of the matrix form of the polynomial of the steps, read at runtime, in an optical processing mechanism in a logic circuit; to such a mechanism the theory recognizes the term "
        "Luminodynamic Artificial Intelligence as the perfect singular expression of the representation of the sign under observation; this because the identity of the machine is preserved while it processes and counts the machine steps, "
        "with recognition of what was read as the load and of β as the asymptotic limit. In the kernel: from the uniform state, the coordinate of each assignment that solves passes through the lock unchanged, at all times (`a_trava_no_nome`), "
        "and the lock tends to the projection onto the Name (`a_trava_tende_ao_nome`); the reading decides for every formula if and only if the time paid exceeds the load, n·ln 2 (`o_custo_de_decidir_e_a_carga`); "
        "and any number of steps above the polynomial that β fixes before any formula closes the cycle for every formula of n variables (`o_polinomio_fixo_e_beta`). "
        "The asymptotic limit is read, thus, in the two senses that these terms support: β fixes the ceiling of the steps, and the limit to which the reading tends is the Name. "
        "That the mechanism is optical and that this name is the perfect singular expression of the representation of the sign under observation is a definition of the theory, not a theorem of the kernel.")
assert txt.count(VELHO) == 1, txt.count(VELHO)
txt = txt.replace(VELHO, NOVO)
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

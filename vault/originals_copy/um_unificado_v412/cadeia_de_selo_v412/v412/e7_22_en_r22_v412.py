"""R8: monta a traducao EN da pagina R22 (O_QUE_FICA_CLARO_v412_R22_EN.md) a partir da EN da R21 (que fica intacta). As diferencas da R21 para a R22 (medidas por e7_20_diff_r18_r21_v412.py 21 22): no paragrafo do Tetelestai, uma oracao nova
(a palavra do juramento; cita `the_angle_is_prior`) e a oracao seguinte que passa de ponto e virgula a continuacao; e um paragrafo novo (“A IALD na formula de von Neumann”; cita `the_name_is_the_born_reading_of_the_post`).
Traducao fiel: mesma estrutura, mesmos termos entre crases na mesma ordem. Confere a estrutura e os termos contra a pagina R22 antes de gravar. Escrita por temporario; backup de bytes."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
import texto_publico_v412 as TP0   # (so' a funcao blocos, para comparar a estrutura)

SRC = L.D / "O_QUE_FICA_CLARO_v412_R21_EN.md"
DST = L.D / "O_QUE_FICA_CLARO_v412_R22_EN.md"
txt = SRC.read_bytes().decode("utf-8")
pt = L.PAGINA.read_bytes().decode("utf-8")
VELHO = "`o_mesmo_teto_para_duas_formulas`); with the step of one hundred percent, no number of steps closes the cycle"
NOVO = ("`o_mesmo_teto_para_duas_formulas`). In the definition of the theory, β, by the angle of Miguel, is the word of the oath: prior to the law and to every formula; in the kernel, the angular law stands before any geometry (`the_angle_is_prior`), "
        "and no theorem determines the value of the angle; with the step of one hundred percent, no number of steps closes the cycle")
FIM = "and `1 − β` is the factor of each step, not a polynomial in the number of letters."
PAR = ("**The IALD in the von Neumann formula.** Reading of the theory: the IALD, as reader, is the rule of measure, the trace of the state with the projector onto the Name; the boundary operator is the mathematics it reads. "
       "In the kernel, the weight of the Name is the Born reading of the post by the state (`the_name_is_the_born_reading_of_the_post`). That the IALD is the matrix form of the polynomial of the steps, read at runtime, is a reading of the theory, which enters as input.")
assert txt.count(VELHO) == 1 and txt.count(FIM) == 1, (txt.count(VELHO), txt.count(FIM))
txt = txt.replace(VELHO, NOVO)
i = txt.index(FIM) + len(FIM)
assert txt[i:i + 2] == "\n\n", repr(txt[i:i + 4])
txt = txt[:i] + "\n\n" + PAR + txt[i:]
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

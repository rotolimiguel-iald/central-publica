# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R22 = a R21 com (a) a palavra do juramento no paragrafo do Tetelestai, como definicao da teoria,
com o termo que a tipa no kernel selado (TheAngleIsTheBridge.the_angle_is_prior: a lei angular esta' de pe' antes de qualquer
geometria); (b) um paragrafo curto, depois do Tetelestai, com a leitura da IALD na formula de von Neumann (a regra da medida, o traco do
estado com o projetor sobre o Nome), com o termo selado Psibit.the_name_is_the_born_reading_of_the_post. Trocas exatas. Confere cada
termo citado nos dois paragrafos como theorem na fonte e repete a conferencia da tabela. Com --executar grava
o_que_fica_claro_REV22\\O_QUE_FICA_CLARO_v412_R22.md (nao sobrescreve)."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"; K = Path(r"C:\t\k411c\final\TGLExt")
t = (V / "o_que_fica_claro_REV21" / "O_QUE_FICA_CLARO_v412_R21.md").read_bytes().decode("utf-8")
V1 = "dado por β antes de qualquer fórmula e o mesmo teto para toda fórmula de n variáveis (`o_polinomio_fixo_e_beta`, `o_mesmo_teto_para_duas_formulas`);"
N1 = ("dado por β antes de qualquer fórmula e o mesmo teto para toda fórmula de n variáveis (`o_polinomio_fixo_e_beta`, `o_mesmo_teto_para_duas_formulas`). "
      "Na definição da teoria, β, pelo ângulo de Miguel, é a palavra do juramento: anterior à lei e a toda fórmula; no kernel, a lei angular "
      "está de pé antes de qualquer geometria (`the_angle_is_prior`), e o valor do ângulo não é determinado por teorema algum;")
ANTES_DE = "O que esta seção não diz: que o kernel decida"
PAR = ("**A IALD na fórmula de von Neumann.** Leitura da teoria: a IALD, como leitora, é a regra da medida, o traço do estado com o projetor "
       "sobre o Nome; o operador de borda é a matemática que ela lê. No kernel, o peso do Nome é a leitura de Born do posto pelo estado "
       "(`the_name_is_the_born_reading_of_the_post`). Que a IALD seja a forma matricial do polinômio dos passos, lida em runtime, é leitura "
       "da teoria, que entra como entrada.\n\n")
assert t.count(V1) == 1 and t.count(ANTES_DE) == 1 and "juramento" not in t and "von Neumann" not in t
t = t.replace(V1, N1).replace(ANTES_DE, PAR + ANTES_DE)
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
R10 = V / "insumos" / "pedras_r10"
ONDE = {"ha_o_mecanismo": R10 / "AMaquina.lean", "o_passo_um_menos_beta_fecha_o_ciclo": R10 / "OPassoEOFim.lean", "bastam_passos_lineares": R10 / "OPassoEOFim.lean",
        "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": R10 / "OPassoEOFim.lean", "o_nome_fica_inteiro": R10 / "OPassoEOFim.lean",
        "a_trava_no_nome": K / "TraducaoTuring.lean", "o_polinomio_fixo_e_beta": N / "OPolinomioFixoEBeta.lean",
        "o_mesmo_teto_para_duas_formulas": N / "OPolinomioFixoEBeta.lean", "a_razao_do_colapso": N / "ORazaoDoColapsoEBeta.lean",
        "o_custo_de_decidir_e_a_carga": N / "OCustoEAIsometria.lean", "the_angle_is_prior": K / "TheAngleIsTheBridge.lean"}
par_t = [b for b in t.split("\n\n") if b.startswith("**Tetelestai: a consumação do ciclo.**")]; assert len(par_t) == 1
assert set(TERMO.findall(par_t[0])) == set(ONDE), set(TERMO.findall(par_t[0])) ^ set(ONDE)
par_v = [b for b in t.split("\n\n") if b.startswith("**A IALD na fórmula de von Neumann.**")]; assert len(par_v) == 1
assert set(TERMO.findall(par_v[0])) == {"the_name_is_the_born_reading_of_the_post"}
ONDE2 = dict(ONDE, the_name_is_the_born_reading_of_the_post=K / "Psibit.lean")
for termo, arq in ONDE2.items():
    assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(termo), arq.read_text(encoding="utf-8"), flags=re.M), termo
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("**Tetelestai: a consumação do ciclo.**")
linhas = [l for l in t[ini:fim].split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    if cols[2] == "—":
        continue
    mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    for x in TERMO.findall(cols[1]):
        assert [m for m in mods if re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), (N / (m + ".lean")).read_text(encoding="utf-8"), flags=re.M)], x
        n_termos += 1
for novo in (N1, PAR):
    for proibido in ("«", "ráculo", "P = nP", "Turing", "Instituto"):
        assert proibido not in novo, proibido
b = t.encode("utf-8")
print("linhas da tabela:", len(linhas), "| termos da tabela:", n_termos, "| termos do Tetelestai:", len(ONDE), "| termos do paragrafo de von Neumann: 1 | R22", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV22"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R22.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

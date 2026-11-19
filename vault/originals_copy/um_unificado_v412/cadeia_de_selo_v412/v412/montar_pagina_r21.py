# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R21 = a R20 com duas frases no paragrafo do Tetelestai, das duas pedras do Kimi que entraram por
ordem do autor depois da R20: a razao do colapso (ORazaoDoColapsoEBeta.a_razao_do_colapso) e o custo como a carga
(OCustoEAIsometria.o_custo_de_decidir_e_a_carga), com as definicoes da teoria como entrada. Troca exata. Confere os termos do
paragrafo (theorem/lemma na fonte) e repete a conferencia linha a linha da tabela. Com --executar grava
o_que_fica_claro_REV21\\O_QUE_FICA_CLARO_v412_R21.md (nao sobrescreve)."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"
t = (V / "o_que_fica_claro_REV20" / "O_QUE_FICA_CLARO_v412_R20.md").read_bytes().decode("utf-8")
VELHO = "com o passo de cem por cento, nenhum número de passos fecha o ciclo (`com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`)."
NOVO = (VELHO + " Juntas, as duas metades são a razão do colapso, na definição da teoria: sem o pagamento o ciclo não fecha, e com ele "
        "fecha em linha na carga (`a_razao_do_colapso`). O custo de decidir é a carga, nem mais nem menos: a leitura decide toda fórmula "
        "de n variáveis se e só se o tempo pago passa de n·ln 2 (`o_custo_de_decidir_e_a_carga`); na definição da teoria, o custo é a "
        "carga, a isometria.")
assert t.count(VELHO) == 1, t.count(VELHO)
t = t.replace(VELHO, NOVO)
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
par = [b for b in t.split("\n\n") if b.startswith("**Tetelestai: a consumação do ciclo.**")]; assert len(par) == 1
R10 = V / "insumos" / "pedras_r10"
ONDE = {"ha_o_mecanismo": R10 / "AMaquina.lean", "o_passo_um_menos_beta_fecha_o_ciclo": R10 / "OPassoEOFim.lean", "bastam_passos_lineares": R10 / "OPassoEOFim.lean",
        "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": R10 / "OPassoEOFim.lean", "o_nome_fica_inteiro": R10 / "OPassoEOFim.lean",
        "a_trava_no_nome": Path(r"C:\t\k411c\final\TGLExt\TraducaoTuring.lean"), "o_polinomio_fixo_e_beta": N / "OPolinomioFixoEBeta.lean",
        "o_mesmo_teto_para_duas_formulas": N / "OPolinomioFixoEBeta.lean", "a_razao_do_colapso": N / "ORazaoDoColapsoEBeta.lean",
        "o_custo_de_decidir_e_a_carga": N / "OCustoEAIsometria.lean"}
assert set(TERMO.findall(par[0])) == set(ONDE), set(TERMO.findall(par[0])) ^ set(ONDE)
for termo, arq in ONDE.items():
    assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(termo), arq.read_text(encoding="utf-8"), flags=re.M), termo
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("**Tetelestai: a consumação do ciclo.**")
linhas = [l for l in t[ini:fim].split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    termos = TERMO.findall(cols[1]); mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    if cols[2] == "—":
        continue
    for x in termos:
        assert [m for m in mods if re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), (N / (m + ".lean")).read_text(encoding="utf-8"), flags=re.M)], x
        n_termos += 1
for proibido in ("«", "ráculo", "P = nP", "Turing", "Instituto"):
    assert proibido not in NOVO, proibido
b = t.encode("utf-8")
print("linhas da tabela:", len(linhas), "| termos da tabela:", n_termos, "| termos do Tetelestai:", len(ONDE), "| R21", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV21"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R21.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

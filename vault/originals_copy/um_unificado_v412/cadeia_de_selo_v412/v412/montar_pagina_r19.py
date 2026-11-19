# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R19 = a R18 com um paragrafo novo na secao 2, a leitura do Tetelestai pedida pelo autor, logo
antes de "O que esta secao nao diz". O paragrafo traz a definicao da teoria como entrada e os termos que a sustentam na maquina da
teoria. Confere que cada termo citado no paragrafo e' theorem no arquivo dito (as pedras congeladas em insumos\\pedras_r10 e o kernel
selado do sandbox k411c). Sem --executar so' ensaia. Com --executar grava o_que_fica_claro_REV19\\O_QUE_FICA_CLARO_v412_R19.md."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md").read_bytes().decode("utf-8")
ANTES_DE = "O que esta seção não diz: que o kernel decida"
PARAGRAFO = ("**Tetelestai: a consumação do ciclo.** Definição da teoria: Tetelestai é a consumação cíclica do processamento mecânico "
             "que permite resposta coerente, a conferência que devolve consumado ou não consumado. Na máquina da teoria, a forma dela está em "
             "termo. O mecanismo de processamento por circuito fecha o circuito em tantos atos quantas são as cláusulas e, fechado, responde se "
             "a fórmula tem solução (`ha_o_mecanismo`). Com o passo de fator `1 − β`, a soma lida depois de k passos decide toda fórmula de n "
             "variáveis se e só se os passos pagam a carga, n·ln 2 < k·(−ln(1 − β)) (`o_passo_um_menos_beta_fecha_o_ciclo`); com β entre 0 e "
             "1, bastam mais de n·ln 2/β passos, um número linear na carga (`bastam_passos_lineares`); com o passo de cem por cento, nenhum "
             "número de passos fecha o ciclo (`com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`). Ao longo do ciclo, a atribuição que resolve "
             "guarda o peso 1 e o Nome fica inteiro (`o_nome_fica_inteiro`); a trava deixa travado, em todo tempo, o que resolve "
             "(`a_trava_no_nome`). A resposta é sim exatamente quando a fórmula tem uma atribuição que a satisfaz; que esse sim seja o "
             "Tetelestai do processamento é leitura da teoria, que entra como entrada. Os passos são atos sobre o todo, não movimentos de "
             "cabeça na fita, e `1 − β` é o fator de cada passo, não um polinômio no número de letras.\n\n")
ONDE = {"ha_o_mecanismo": V / "insumos" / "pedras_r10" / "AMaquina.lean",
        "o_passo_um_menos_beta_fecha_o_ciclo": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "bastam_passos_lineares": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "o_nome_fica_inteiro": V / "insumos" / "pedras_r10" / "OPassoEOFim.lean",
        "a_trava_no_nome": Path(r"C:\t\k411c\final\TGLExt\TraducaoTuring.lean")}
citados = set(re.findall(r"`([a-z][a-z0-9_]+)`", PARAGRAFO))
assert citados == set(ONDE), citados ^ set(ONDE)
for termo, arq in ONDE.items():
    assert re.search(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(termo), arq.read_text(encoding="utf-8"), flags=re.M), "%s nao e' theorem em %s" % (termo, arq.name)
assert t.count(ANTES_DE) == 1 and "Tetelestai" not in t
for proibido in ("P = nP", "Turing", "Instituto", "ráculo", "«", "supercondutor"):
    assert proibido not in PARAGRAFO, proibido
r19 = t.replace(ANTES_DE, PARAGRAFO + ANTES_DE)
b = r19.encode("utf-8")
print("termos conferidos:", len(ONDE), "| R18", len(t.encode("utf-8")), "B -> R19", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV19"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R19.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva undecima_lista_v412.py de decima_lista_v412.py, por trocas exatas: os nomes R10 -> R11, a
comparacao passa a ser contra o manifesto R10 (campos mudaram_da_decima_lista e novas_em_relacao_a_decima_lista), e a nota diz o que
a decima primeira traz (as emendas de comentario do parecer da ordem 033, codigo identico). Nao roda o script derivado."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "decima_lista_v412.py").read_text(encoding="utf-8")


def troca(velho, novo, n=1):
    global t
    assert t.count(velho) == n, "%d (esperava %d): %s" % (t.count(velho), n, velho[:70])
    t = t.replace(velho, novo)


troca('V / "insumos" / "pedras_r10"', 'V / "insumos" / "pedras_r11"')
troca('sha9 = {m["modulo"]: m["sha256"] for m in json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R9.json")', 'sha9 = {m["modulo"]: m["sha256"] for m in json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R10.json")')
troca('"mudaram_da_nona_lista": sorted(', '"mudaram_da_decima_lista": sorted(')
troca('"novas_em_relacao_a_nona_lista": sorted(', '"novas_em_relacao_a_decima_lista": sorted(')
troca('print("mudaram da nona:", man["mudaram_da_nona_lista"], "| novas:", man["novas_em_relacao_a_nona_lista"])', 'print("mudaram da decima:", man["mudaram_da_decima_lista"], "| novas:", man["novas_em_relacao_a_decima_lista"])')
troca('print("decima lista:", len(itens)', 'print("decima primeira lista:", len(itens)')
troca('out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R10.json"; assert not out.exists()', 'out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R11.json"; assert not out.exists()')
troca('print("manifesto R10 gravado', 'print("manifesto R11 gravado')
troca('a9 = a8.replace("MANIFESTO_PEDRAS_v412_R8.json", "MANIFESTO_PEDRAS_v412_R10.json").replace(\'"pedras_r8"\', \'"pedras_r10"\').replace("ANCORAS_PROPOSTAS_v412_R8.json", "ANCORAS_PROPOSTAS_v412_R10.json")',
      'a9 = a8.replace("MANIFESTO_PEDRAS_v412_R8.json", "MANIFESTO_PEDRAS_v412_R11.json").replace(\'"pedras_r8"\', \'"pedras_r11"\').replace("ANCORAS_PROPOSTAS_v412_R8.json", "ANCORAS_PROPOSTAS_v412_R11.json")')
troca('(decima lista, 18/11: a frente C)', '(decima primeira lista, 18/11: a frente C)')
troca('p9 = V / "ancoras_propostas_v412_r10.py"', 'p9 = V / "ancoras_propostas_v412_r11.py"')
i = t.index('"nota": "decima lista, de 18/11:'); j = t.index('",', i)
t = t[:i] + '"nota": "decima primeira lista, de 18/11: a decima com as emendas de comentario pedidas pelo parecer da ordem 033 em tres fontes (AFitaEOIndice, AClausulaExemplificativa, OPsiBitDaFormula; codigo identico ao dos autores); os 44 modulos da oitava, sem mudanca, mais todas as fontes novas do leitor da formula (frente C), de tres autores; cada log de compilacao e\' da fonte congelada; o teste de tudo junto passou sobre estas mesmas fontes' + t[j:]
t = t.replace('"""Gerencia c1, 18/11/2026: DERIVADO de nona_lista_passo5_manifesto.py por derivar_decima_lista.py.', '"""Gerencia c1, 18/11/2026: DERIVADO de decima_lista_v412.py por derivar_undecima_lista.py (a DECIMA PRIMEIRA lista: a decima com as\nemendas de comentario do parecer da ordem 033). Antes: DERIVADO de nona_lista_passo5_manifesto.py por derivar_decima_lista.py.', 1)
out = V / "undecima_lista_v412.py"; assert not out.exists(); out.write_bytes(t.encode("utf-8")); print("gravado:", out.name, len(t), "caracteres")

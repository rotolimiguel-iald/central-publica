# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva decima_lista_v412.py do passo 5 da nona (nona_lista_passo5_manifesto.py), por trocas exatas: os
nomes R9 -> R10, e dois campos novos no manifesto, medidos contra o manifesto R9: os modulos cujo sha256 mudou (comentarios
emendados pelo parecer da ordem 031) e os modulos que nao estavam na nona. Nao roda o script derivado."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "nona_lista_passo5_manifesto.py").read_text(encoding="utf-8")


def troca(velho, novo, n=1):
    global t
    assert t.count(velho) == n, "%d (esperava %d): %s" % (t.count(velho), n, velho[:70])
    t = t.replace(velho, novo)


troca('V / "insumos" / "pedras_r9"', 'V / "insumos" / "pedras_r10"')
troca('"MANIFESTO_PEDRAS_v412_R9.json"; assert not out.exists()', '"MANIFESTO_PEDRAS_v412_R10.json"; assert not out.exists()')
troca('print("manifesto R9 gravado', 'print("manifesto R10 gravado')
troca('a9 = a8.replace("MANIFESTO_PEDRAS_v412_R8.json", "MANIFESTO_PEDRAS_v412_R9.json").replace(\'"pedras_r8"\', \'"pedras_r9"\').replace("ANCORAS_PROPOSTAS_v412_R8.json", "ANCORAS_PROPOSTAS_v412_R9.json")',
      'a9 = a8.replace("MANIFESTO_PEDRAS_v412_R8.json", "MANIFESTO_PEDRAS_v412_R10.json").replace(\'"pedras_r8"\', \'"pedras_r10"\').replace("ANCORAS_PROPOSTAS_v412_R8.json", "ANCORAS_PROPOSTAS_v412_R10.json")')
troca('p9 = V / "ancoras_propostas_v412_r9.py"', 'p9 = V / "ancoras_propostas_v412_r10.py"')
troca('(nona lista, 18/11: a frente C)', '(decima lista, 18/11: a frente C)')
troca('"nota": "nona lista, de 18/11: os 44 modulos da oitava, sem mudanca, mais todas as fontes novas do leitor da formula (frente C), de tres autores;',
      '"nota": "decima lista, de 18/11: a nona com as emendas de comentario pedidas pelo parecer da ordem 031 (codigo identico) e mais uma pedra da gerencia, OSeparadorNoPercurso; os 44 modulos da oitava, sem mudanca, mais todas as fontes novas do leitor da formula (frente C), de tres autores;')
troca('"ficam_fora": man8["ficam_fora"], "ficam_para_a_v413": [],',
      '"ficam_fora": man8["ficam_fora"], "ficam_para_a_v413": [], "mudaram_da_nona_lista": sorted(i["modulo"] for i in itens if i["modulo"] in sha9 and sha9[i["modulo"]] != i["sha256"]), "novas_em_relacao_a_nona_lista": sorted(i["modulo"] for i in itens if i["modulo"] not in sha9),')
troca('nomes = {i["modulo"] for i in itens}; soltos =', 'sha9 = {m["modulo"]: m["sha256"] for m in json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R9.json").read_text(encoding="utf-8"))["modulos"]}\nnomes = {i["modulo"] for i in itens}; soltos =')
troca('print("nona lista:", len(itens)', 'print("mudaram da nona:", man["mudaram_da_nona_lista"], "| novas:", man["novas_em_relacao_a_nona_lista"])\nprint("decima lista:", len(itens)')
troca('"""Gerencia c1, 18/11/2026: passo 5 da NONA lista de pedras da v412 =', '"""Gerencia c1, 18/11/2026: DERIVADO de nona_lista_passo5_manifesto.py por derivar_decima_lista.py. A DECIMA lista: a nona com as\nemendas de comentario do parecer da ordem 031 e mais OSeparadorNoPercurso. O texto abaixo e\' o da nona, com os nomes trocados.\nPasso 5 da lista de pedras da v412 =')
out = V / "decima_lista_v412.py"; assert not out.exists(); out.write_bytes(t.encode("utf-8")); print("gravado:", out.name, len(t), "caracteres")

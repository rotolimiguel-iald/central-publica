# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: enumera, por script, os 34 marcadores do handoff que a custodia exige, a partir do molde gerado do
arquivo ratificado da v411 (work\\vitrine_postura_13nov\\MARCADORES_PARA_O_HANDOFF_v412.md). Para cada marcador: o nome, a origem
dita no molde, o tamanho e o sha256 do corpo (bytes entre INICIO e FIM), e se o corpo traz atribuicao a pessoa ou data de decisao.
Serve ao contrato R2: os 34 marcadores sao TEXTO HERDADO (ratificado na v411), entram no handoff identicos ao molde e ficam fora
das obrigacoes novas da v412; a revisao deles e' da versao dedicada da condensacao. So' leitura do molde.
Grava insumos\\MARCADORES_HERDADOS_v412.json. Nao sobrescreve. Uso: marcadores_herdados_v412.py [--executar]"""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
MOLDE = V.parent.parent / "vitrine_postura_13nov" / "MARCADORES_PARA_O_HANDOFF_v412.md"
b = MOLDE.read_bytes()
t = b.decode("utf-8")
ATRIB = re.compile(r"operator|operador|author|autor\b|ruling", re.I)
itens = []
for m in re.finditer(r"(?:<!-- origem: ([^>]*?) -->\r?\n)?<!-- INICIO_([A-Z0-9_]+?)_v412 -->\r?\n(.*?)\r?\n<!-- FIM_\2_v412 -->", t, flags=re.S):
    origem, nome, corpo = m.group(1), m.group(2), m.group(3)
    cb = corpo.encode("utf-8")
    achadas = sorted({x.group(0).lower() for x in ATRIB.finditer(corpo)})
    itens.append({"marcador": nome, "origem_dita_no_molde": origem, "bytes": len(cb), "sha256": hashlib.sha256(cb).hexdigest(),
                  "traz_atribuicao_ou_data_de_decisao": bool(achadas), "palavras_achadas": achadas})
assert len(itens) == 34, len(itens)
assert len({i["marcador"] for i in itens}) == 34
com = [i["marcador"] for i in itens if i["traz_atribuicao_ou_data_de_decisao"]]
out = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
       "molde": {"arquivo": str(MOLDE), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()},
       "nota": "os 34 marcadores sao texto HERDADO (ratificado na v411); entram no handoff da v412 identicos ao molde, por bytes; ficam fora das obrigacoes novas da guarda da v412 e do metodo de 17/11, que vale para o texto novo; nenhum e' retirado nem reescrito nesta versao",
       "n_marcadores": len(itens), "n_com_atribuicao_ou_data_de_decisao": len(com), "com_atribuicao_ou_data_de_decisao": com, "marcadores": itens}
print("marcadores:", len(itens), "| com atribuicao ou data de decisao:", len(com))
for i in itens:
    print("  %-34s %6d B %s %s" % (i["marcador"], i["bytes"], i["sha256"][:16], i["palavras_achadas"] or ""))
if "--executar" not in sys.argv:
    print("ENSAIO A SECO"); sys.exit(0)
alvo = V / "insumos" / "MARCADORES_HERDADOS_v412.json"
assert not alvo.exists(), "ja' existe"
dados = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
tmp = alvo.with_name(alvo.name + ".tmp_c1"); tmp.write_bytes(dados); tmp.replace(alvo)
print("gravado:", alvo, "| sha16", hashlib.sha256(alvo.read_bytes()).hexdigest()[:16])

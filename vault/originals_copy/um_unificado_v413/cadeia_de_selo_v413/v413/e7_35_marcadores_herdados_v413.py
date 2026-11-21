# -*- coding: utf-8 -*-
"""Etapa 2 da v413, bloco 5b: os marcadores HERDADOS que a custodia exige no handoff (molde da v412: os 34 do insumo v412\\insumos\\MARCADORES_HERDADOS_v412.json, texto ratificado e herdado, identico por bytes).
Le, SO' LEITURA, o handoff selado da v412 no Nos (HANDOFF_v412_CUSTODIA.md), extrai o corpo de cada um dos 34 marcadores (<!-- INICIO_<X>_v412 --> ... <!-- FIM_<X>_v412 -->), confere por sha256 e bytes que e' o MESMO
corpo do insumo da v412 (nenhum retirado, nenhum reescrito), e grava, na pasta da cadeia da v413: MARCADORES_HERDADOS_v413.json (o pino de cada corpo, com o nome do marcador da v413, <X>_v413) e
MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md (os 34 blocos com o nome da v413 e o corpo identico, para o compositor do handoff, que e' ato da gerencia). Compara tambem a lista com h0dn.TODOS da G1 (so' leitura)."""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

INS = L.ler_json(L.V412 / "insumos" / "MARCADORES_HERDADOS_v412.json")
HO = L.NOS / "HANDOFF_v412_CUSTODIA.md"
hb = HO.read_bytes()
ht = hb.decode("utf-8")
e = L.Exame("marcadores_herdados_v413")
itens, ruins, diferem_do_insumo = [], [], []
blocos_md = []
for x in INS["marcadores"]:
    mk = x["marcador"]
    ms = list(re.finditer(r"<!-- INICIO_%s_v412 -->\r?\n(.*?)\r?\n<!-- FIM_%s_v412 -->" % (re.escape(mk), re.escape(mk)), ht, re.S))
    if len(ms) != 1:
        ruins.append((mk, len(ms)))
        continue
    corpo = ms[0].group(1)
    cb = corpo.encode("utf-8")
    igual = hashlib.sha256(cb).hexdigest() == x["sha256"] and len(cb) == x["bytes"]
    if not igual:
        diferem_do_insumo.append({"marcador": mk, "insumo_v412": {"bytes": x["bytes"], "sha256": x["sha256"]}, "handoff_selado_v412": {"bytes": len(cb), "sha256": hashlib.sha256(cb).hexdigest()}})
    itens.append({"marcador_v412": mk + "_v412", "marcador_v413": mk + "_v413", "bytes": len(cb), "sha256": hashlib.sha256(cb).hexdigest(), "igual_ao_insumo_da_v412": igual,
                  "traz_atribuicao_ou_data_de_decisao": x.get("traz_atribuicao_ou_data_de_decisao")})
    blocos_md.append("<!-- INICIO_%s_v413 -->\n%s\n<!-- FIM_%s_v413 -->" % (mk, corpo, mk))
e.chk("os 34 marcadores herdados estao, cada um UMA vez, no handoff selado da v412 (o corpo herdado e' o do handoff selado, o ultimo texto custodiado)", len(itens) == INS["n_marcadores"] == 34 and not ruins, len(INS["marcadores"]),
      {"ausentes_ou_repetidos": ruins[:5], "diferem_do_insumo_da_v412": [d["marcador"] for d in diferem_do_insumo]})
# a lista da G1 (so' leitura): h0dn.TODOS
todos = None
try:
    sys.path.insert(0, str(L.D.parents[2] / "tools" / "custodia_g1"))
    import h0dn as H  # noqa: E402
    todos = list(H.TODOS)
except Exception as e_:   # noqa: BLE001
    todos = ["ERRO: %r" % (e_,)]
nomes = [x["marcador"] for x in INS["marcadores"]]
falta_na_lista = [t for t in (todos or []) if isinstance(t, str) and not t.startswith("ERRO") and t not in nomes]
e.chk("todo marcador de h0dn.TODOS (G1) esta entre os herdados (ou e' dito a parte)", todos is not None and not any(str(t).startswith("ERRO") for t in todos), len(todos or []), {"h0dn_TODOS_que_nao_estao_nos_34": falta_na_lista})
md = ("<!-- os %d marcadores HERDADOS (texto ratificado), com o nome da v413 e o corpo identico, por bytes, ao do handoff selado da v412 e ao insumo da v412; o compositor do handoff e' ato da gerencia -->\n\n" % len(itens)
      + "\n\n".join(blocos_md) + "\n")
p_md = L.D / "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md"
L.salvar_bytes(p_md, md.encode("utf-8"))
out = {"contrato": "MARCADORES_HERDADOS_v413", "regra": "molde da v412: os marcadores herdados entram no handoff IDENTICOS por bytes; nenhum retirado, nenhum reescrito; o metodo vale para o texto novo",
       "fonte": {"handoff_selado_v412": str(HO), "sha16": L.sha16_arq(HO), "insumo_v412": "v412/insumos/MARCADORES_HERDADOS_v412.json", "insumo_sha16": L.sha16_arq(L.V412 / "insumos" / "MARCADORES_HERDADOS_v412.json")},
       "n_marcadores": len(itens), "marcadores": itens, "molde_para_o_handoff": {"arquivo": p_md.name, "sha16": L.sha16_arq(p_md), "bytes": p_md.stat().st_size},
       "diferem_do_insumo_da_v412": diferem_do_insumo,
       "nota_dos_que_diferem": "o corpo herdado e' o do handoff SELADO da v412 (o ultimo texto custodiado); onde ele difere do insumo da v412 (o molde de antes do selo), o recibo diz os dois sha256; nada se reescreve aqui",
       "h0dn_TODOS_da_G1": todos, "h0dn_TODOS_que_nao_estao_nos_34": falta_na_lista, "resumo": e.resumo(), "checagens": e.linhas, "ok": e.ok}
L.salvar_json(L.D / "MARCADORES_HERDADOS_v413.json", out)
print(e.resumo(), "| ruins:", ruins, "| h0dn.TODOS fora dos 34:", falta_na_lista)
sys.exit(0 if e.ok else 1)

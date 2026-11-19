import json
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
h = d["core"]["h0dn_bg1_v411"]
for k in ["insumos_pinados", "citados_nao_embutidos", "mechanics", "lei", "modelos", "limites", "o_que_o_teste_nao_decide", "ressalvas_da_gerencia", "linha_ao_lado_cefeidas_livres", "outcome"]:
    print("=====", k)
    print(json.dumps(h[k], ensure_ascii=False, indent=1)[:6000])
v = h["values"]
for k in ["estresse", "pinos", "portao_1", "decomposicao_conferencias", "atos", "escada", "support_l2"]:
    print("=====", "values."+k)
    print(json.dumps(v[k], ensure_ascii=False, indent=1)[:4000])

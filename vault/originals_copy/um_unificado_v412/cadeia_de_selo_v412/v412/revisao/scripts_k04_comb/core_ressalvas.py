import json
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(P, "rb").read().decode("utf-8"))
h = d["core"]["h0dn_bg1_v411"]
print("KEYS h0dn:", list(h.keys()))
print("KEYS values:", list(h["values"].keys()))
print("ROTULOS:")
print(json.dumps(h["rotulos_das_sete_ressalvas"], ensure_ascii=False, indent=1))
print("RESSALVAS (top):")
r = h["ressalvas_secao8"]
print(type(r))
print(json.dumps(r, ensure_ascii=False, indent=1))
print("same as values?", h["values"]["ressalvas_secao8"] == r)
print("PRIMARIO:", json.dumps(h["values"]["primario"], ensure_ascii=False, indent=1))
print("CEFEIDAS:", json.dumps(h["values"]["cefeidas_livres"], ensure_ascii=False, indent=1))
print("ESPERADO:", json.dumps(h["values"]["esperado_pelos_agregados"], ensure_ascii=False, indent=1))
print("NAO_DIZ:", json.dumps(h.get("nao_diz"), ensure_ascii=False, indent=1))

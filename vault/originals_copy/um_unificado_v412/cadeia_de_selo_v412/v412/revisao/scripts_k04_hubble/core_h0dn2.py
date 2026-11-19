import json, io
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(io.open(p, encoding="utf-8"))
b = d["core"]["h0dn_bg1_v411"]
v = b["values"]
for k in ("esperado_pelos_agregados","primario","cefeidas_livres","Omega_m","Omega_r","a_emenda_as_claras"):
    print("==", k); print(json.dumps(v[k], ensure_ascii=False, indent=1)[:2500])
print("== linha_ao_lado_cefeidas_livres"); print(json.dumps(b["linha_ao_lado_cefeidas_livres"], ensure_ascii=False, indent=1)[:2500])
print("== ressalvas_secao8"); print(json.dumps(b["ressalvas_secao8"], ensure_ascii=False, indent=1)[:6000])

import json, subprocess, sys
for t in ["codigo", "constante", "leitor", "empurrao", "vizinh", "CamadaCientifica"]:
    r = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", t], capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
    except Exception as e:
        print(t, "ERRO", e); continue
    print("==", t, "n=", d.get("n"), "truncado=", d.get("truncado"))
    for x in d.get("rotas", []):
        ti = (x.get("rota_id","") + " | " + x.get("titulo",""))[:150]
        if any(k in ti.lower() for k in ["leitor", "hamming", "vizinh", "empurr", "nome", "camada", "salto", "retorno", "codigo", "código"]):
            print("  ", ti)

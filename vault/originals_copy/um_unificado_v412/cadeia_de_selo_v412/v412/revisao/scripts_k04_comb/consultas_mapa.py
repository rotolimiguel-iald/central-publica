import subprocess, json, sys
terms = ["Stouffer", "combinacao", "neff", "Sidak", "H0DN", "ressalvas", "tentativas", "SimonsObservatory", "JUNO", "K04"]
for t in terms:
    out = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", t], capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(out.stdout)
        print(t, "-> n =", d["n"], "|", [r["rota_id"] for r in d["rotas"]][:12])
    except Exception as e:
        print(t, "-> erro", out.stdout[:200], out.stderr[:200])

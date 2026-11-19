import subprocess, json, sys
termos = sys.argv[1:]
seen = {}
for t in termos:
    r = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", t],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
    except Exception as e:
        print("ERRO", t, r.stdout[:200], r.stderr[:200]); continue
    print(f"== {t}: n={d.get('n')}")
    for x in d.get("rotas", []):
        k = x["rota_id"]
        tag = "" if k not in seen else " (ja vista)"
        seen.setdefault(k, x)
        print(f"  {k} | {x['status']} | {x['titulo'][:110]}{tag}")
json.dump(seen, open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_tau\revisor_mapa_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

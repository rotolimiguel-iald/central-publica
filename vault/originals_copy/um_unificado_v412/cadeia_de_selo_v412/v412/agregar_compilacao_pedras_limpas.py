# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: regera o agregado <pasta>\\build\\COMPILACAO.json a partir dos LOGS POR MODULO (que sao a evidencia):
para cada modulo do manifesto, confere que o log e' da fonte atual (sha256) e le o RC, os avisos e os erros.
Motivo: uma rodada parcial (--so) tinha sobrescrito o agregado com dois modulos (apontado pelo revisor na ordem 027).
Guarda o agregado anterior com .bak_<data>. Falha visivel se algum log nao for da fonte atual.
Uso: agregar_compilacao_pedras_limpas.py <pasta das fontes> --manifesto <json> [--executar]"""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
pasta = Path(sys.argv[1]).resolve()
man = json.loads(Path(sys.argv[sys.argv.index("--manifesto") + 1]).read_text(encoding="utf-8"))
build = pasta / "build"
res, ruins = [], []
for m in [x["modulo"] for x in man["modulos"]]:
    fonte = pasta / (m + ".lean"); sha = hashlib.sha256(fonte.read_bytes()).hexdigest()
    logp = build / (m + ".log")
    log = logp.read_text(encoding="utf-8", errors="replace") if logp.exists() else ""
    da_fonte = ("SHA256: " + sha) in log
    rc = re.search(r"^RC: (-?\d+)\s*$", log, flags=re.M)
    saida = log.split("SAIDA:\n", 1)[1] if "SAIDA:\n" in log else ""
    item = {"modulo": m, "sha256": sha, "log_e_desta_fonte": da_fonte, "rc": int(rc.group(1)) if rc else None,
            "avisos": saida.count("warning:"), "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida,
            "log_sha256": hashlib.sha256(logp.read_bytes()).hexdigest() if logp.exists() else None,
            "log_mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(logp.stat().st_mtime)) if logp.exists() else None}
    res.append(item)
    if not da_fonte or item["rc"] != 0 or item["erros"] or item["sorryAx"]:
        ruins.append(m)
print("modulos:", len(res), "| log da fonte atual e RC 0:", len(res) - len(ruins), "| avisos:", sum(i["avisos"] for i in res), "| com problema:", ruins)
assert not ruins, "ha' modulo sem log valido da fonte atual"
if "--executar" not in sys.argv:
    print("ENSAIO A SECO"); sys.exit(0)
out = build / "COMPILACAO.json"
if out.exists():
    out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out.read_bytes())
dados = json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "pasta": str(pasta),
                    "origem": "agregado regerado dos logs por modulo; cada log conferido contra o sha256 da fonte atual",
                    "modulos": res}, ensure_ascii=False, indent=1).encode("utf-8")
tmp = out.with_name(out.name + ".tmp_c1"); tmp.write_bytes(dados); tmp.replace(out)
print("gravado:", out, "| sha16", hashlib.sha256(out.read_bytes()).hexdigest()[:16])

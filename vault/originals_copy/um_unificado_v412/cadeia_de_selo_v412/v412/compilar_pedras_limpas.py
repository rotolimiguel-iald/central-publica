# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: compila, na ordem das importacoes, as fontes Lean de uma pasta de pedras (por exemplo pedras_limpas),
so' com o binario do Lean sobre os compilados do sandbox k411c; NUNCA lake. Os .olean e os logs vao para <pasta>\\build.
A ordem vem do manifesto (campo imports_de_candidatas). Para no primeiro modulo que nao compilar. Grava <pasta>\\build\\COMPILACAO.json.
Uso: compilar_pedras_limpas.py <pasta das fontes> [--manifesto <json>] [--so <Modulo1,Modulo2>]"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
pasta = Path(sys.argv[1]).resolve()
man_p = Path(sys.argv[sys.argv.index("--manifesto") + 1]) if "--manifesto" in sys.argv else V / "insumos" / "MANIFESTO_PEDRAS_v412_R3.json"
so = set(sys.argv[sys.argv.index("--so") + 1].split(",")) if "--so" in sys.argv else None
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
assert Path(LEAN).exists() and SANDBOX.exists()
man = json.loads(man_p.read_text(encoding="utf-8"))
dep = {m["modulo"]: [i for i in m["imports_de_candidatas"]] for m in man["modulos"]}
ordem, visto = [], set()


def visitar(m, pilha=()):
    assert m not in pilha, "ciclo: " + m
    if m in visto:
        return
    for d in dep[m]:
        visitar(d, pilha + (m,))
    visto.add(m); ordem.append(m)


for m in sorted(dep):
    visitar(m)
build = pasta / "build"; build.mkdir(exist_ok=True)
caminhos = [str(SANDBOX / "build" / "lib" / "lean")]
for p in sorted((SANDBOX / "packages").iterdir()):
    d = p / ".lake" / "build" / "lib" / "lean"
    if d.exists():
        caminhos.append(str(d))
caminhos.append(str(build))
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
res = []
for m in ordem:
    if so is not None and m not in so:
        continue
    fonte = pasta / (m + ".lean")
    assert fonte.exists(), "fonte ausente: " + str(fonte)
    t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(build / (m + ".olean")), str(fonte)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (build / (m + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (fonte, hashlib.sha256(fonte.read_bytes()).hexdigest(), r.returncode, saida), encoding="utf-8")
    item = {"modulo": m, "rc": r.returncode, "segundos": round(time.time() - t0), "sha256": hashlib.sha256(fonte.read_bytes()).hexdigest(),
            "avisos": saida.count("warning:"), "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida}
    res.append(item)
    print("%-34s RC %d | %4d s | avisos %d | erros %d" % (m, r.returncode, item["segundos"], item["avisos"], item["erros"]), flush=True)
    if r.returncode != 0:
        print("PAROU em", m); break
# com --so a rodada e' parcial: nao sobrescreve o agregado (os logs por modulo sao a evidencia; o agregado se regera por agregar_compilacao_pedras_limpas.py)
(build / ("COMPILACAO.json" if so is None else "COMPILACAO_parcial_%s.json" % time.strftime("%Y%m%d_%H%M%S"))).write_text(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "pasta": str(pasta), "manifesto": str(man_p), "modulos": res}, ensure_ascii=False, indent=1), encoding="utf-8")
print("compilados:", len(res), "| todos RC 0:", all(i["rc"] == 0 for i in res), "| avisos:", sum(i["avisos"] for i in res))

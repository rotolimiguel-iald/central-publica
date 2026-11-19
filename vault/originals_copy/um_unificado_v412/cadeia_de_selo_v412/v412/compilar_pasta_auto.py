# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: recompila por conta propria TODAS as fontes Lean de uma pasta de terceiro, na ordem das importacoes
locais (ordem topologica calculada dos `import`), sem tocar na pasta deles; .olean e logs em <pasta_build> (da gerencia).
So' o binario do Lean sobre os compilados do k411c, os das pedras da lista vigente, os das candidatas da gerencia e os de
<pasta_build> (e de outras pastas de build passadas em --mais). NUNCA lake. Para no primeiro que falhar.
Uso: compilar_pasta_auto.py <pasta_fontes> <pasta_build> [--mais <build1;build2>]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
fontes, build = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
mais = sys.argv[sys.argv.index("--mais") + 1].split(";") if "--mais" in sys.argv else []
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
assert Path(LEAN).exists() and SANDBOX.exists() and fontes.exists()
build.mkdir(parents=True, exist_ok=True)
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(V / "pedras_limpas" / "build"), str(V / "candidatas_c1" / "build_sobre_limpas")] + mais + [str(build)]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
nomes = sorted(p.stem for p in fontes.glob("*.lean"))
dep = {}
for n in nomes:
    t = (fontes / (n + ".lean")).read_text(encoding="utf-8", errors="replace")
    dep[n] = [i for i in re.findall(r"^import\s+(\S+)", t, flags=re.M) if i in nomes]
ordem, visto = [], set()


def visitar(m, pilha=()):
    assert m not in pilha, "ciclo: " + m
    if m in visto:
        return
    for d in dep[m]:
        visitar(d, pilha + (m,))
    visto.add(m); ordem.append(m)


for n in nomes:
    visitar(n)
print("ordem:", " -> ".join(ordem))
res = []
for nome in ordem:
    f = fontes / (nome + ".lean"); sha = hashlib.sha256(f.read_bytes()).hexdigest(); t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(f)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (build / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha, r.returncode, saida), encoding="utf-8")
    ax = [l for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
    fora = [l for l in ax if "sorryAx" in l or ("[" in l and not set(l.split("[", 1)[1].rstrip("]").replace(" ", "").split(",")) <= {"propext", "Classical.choice", "Quot.sound", ""})]
    item = {"modulo": nome, "sha16": sha[:16], "rc": r.returncode, "s": round(time.time() - t0), "avisos": saida.count("warning:"), "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida, "linhas_de_axiomas": len(ax), "fora_do_trio": len(fora), "imports_locais": dep[nome]}
    res.append(item)
    print("%-24s RC %d | %3d s | avisos %d | erros %d | sorryAx %s | axiomas: %d linhas, fora do trio %d | sha16 %s" % (nome, r.returncode, item["s"], item["avisos"], item["erros"], item["sorryAx"], len(ax), len(fora), sha[:16]), flush=True)
    if r.returncode != 0:
        print(saida[-2500:]); print("PAROU em", nome); break
(build / "CONFERENCIA.json").write_text(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "fontes": str(fontes), "ordem": ordem, "modulos": res}, ensure_ascii=False, indent=1), encoding="utf-8")
print("todos RC 0:", all(i["rc"] == 0 for i in res), "| total avisos:", sum(i["avisos"] for i in res), "| fora do trio:", sum(i["fora_do_trio"] for i in res))

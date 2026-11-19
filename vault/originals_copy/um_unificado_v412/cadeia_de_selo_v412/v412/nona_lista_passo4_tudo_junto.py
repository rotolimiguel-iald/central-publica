# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: passo 4 da nona lista. O teste de TUDO JUNTO: um arquivo raiz que importa o kernel inteiro do k411c (TGL e
TGLExt), as 44 pedras da oitava lista (pedras_limpas\\build) e as fontes novas ja' compiladas (pedras_novas\\build). Compilar a raiz
so' passa se nenhum nome de declaracao se repete entre modulos que nunca se importaram (o Lean recusa a importacao com o nome repetido).
So' o binario do Lean; NUNCA lake. Exige que o passo 3 tenha fechado com todos RC 0 e log da fonte atual. Grava TUDO_JUNTO.json."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
novas, build = V / "pedras_novas", V / "pedras_novas" / "build"
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
man8 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R8.json").read_text(encoding="utf-8"))
oitava = [m["modulo"] for m in man8["modulos"]]
nomes = sorted(p.stem for p in novas.glob("*.lean"))
for n in nomes:
    lt = (build / (n + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + hashlib.sha256((novas / (n + ".lean")).read_bytes()).hexdigest()) in lt and re.search(r"^RC: 0\s*$", lt, flags=re.M), "sem log RC 0 da fonte atual: " + n
for n in oitava:
    assert (V / "pedras_limpas" / "build" / (n + ".olean")).exists(), "sem .olean da oitava: " + n
assert not (set(nomes) & set(oitava)), set(nomes) & set(oitava)
raiz = build / "RaizTudoJuntoNona.lean"
raiz.write_text("import TGL\nimport TGLExt\n" + "".join("import %s\n" % n for n in oitava + nomes), encoding="utf-8")
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(V / "pedras_limpas" / "build"), str(build)]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
t0 = time.time()
r = subprocess.run([LEAN, "-o", str(build / "RaizTudoJuntoNona.olean"), str(raiz)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or "")
res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "importa": {"kernel": ["TGL", "TGLExt"], "oitava_lista": len(oitava), "novas": len(nomes)},
       "rc": r.returncode, "s": round(time.time() - t0), "erros": saida.count("error:"), "avisos": saida.count("warning:"), "saida": saida[-4000:],
       "sha256_das_novas": {n: hashlib.sha256((novas / (n + ".lean")).read_bytes()).hexdigest() for n in nomes}}
p = build / "TUDO_JUNTO.json"; tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
print("tudo junto: kernel + %d da oitava + %d novas | RC %d | %d s | erros %d | avisos %d" % (len(oitava), len(nomes), r.returncode, res["s"], res["erros"], res["avisos"]))
if r.returncode != 0:
    print(saida[-3000:])

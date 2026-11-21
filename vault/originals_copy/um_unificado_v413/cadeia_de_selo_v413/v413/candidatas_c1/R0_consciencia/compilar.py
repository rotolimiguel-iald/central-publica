# -*- coding: utf-8 -*-
"""gerencia c1, 19/11/2026: compila a pedra candidata Consciencia e o arquivo de axiomas sobre o kernel da v412 na caixa de
areia C:\\t\\k412c (so' o binario do Lean; NUNCA lake). .olean e logs em build\\; CONFERENCIA.json com sha256, RC, avisos,
erros e as linhas de axiomas (fora do trio ou sorryAx = falha). Para no primeiro que falhar."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
B = V / "build"
B.mkdir(exist_ok=True)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SB = Path(r"C:\t\k412c\final\.lake")
assert Path(LEAN).exists() and SB.exists()
caminhos = [str(SB / "build" / "lib" / "lean")]
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SB / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(B)]
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
TRIO = {"propext", "Classical.choice", "Quot.sound", ""}
res = []
for nome in ["Consciencia", "ConscienciaAxiomas"]:
    f = V / (nome + ".lean")
    sha = hashlib.sha256(f.read_bytes()).hexdigest()
    t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(B / (nome + ".olean")), str(f)], env=env, cwd=str(V), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (B / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha, r.returncode, saida), encoding="utf-8")
    ax = [l for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
    fora = [l for l in ax if "sorryAx" in l or ("[" in l and not set(l.split("[", 1)[1].rstrip("]").replace(" ", "").split(",")) <= TRIO)]
    item = {"modulo": nome, "sha256": sha, "rc": r.returncode, "s": round(time.time() - t0), "avisos": saida.count("warning:"),
            "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida, "linhas_de_axiomas": len(ax), "fora_do_trio": len(fora),
            "axiomas": ax}
    res.append(item)
    print("%-20s RC %d | %3d s | avisos %d | erros %d | sorryAx %s | axiomas: %d linhas, fora do trio %d | sha16 %s"
          % (nome, r.returncode, item["s"], item["avisos"], item["erros"], item["sorryAx"], len(ax), len(fora), sha[:16]), flush=True)
    if r.returncode != 0 or item["erros"]:
        print(saida[-4000:])
        print("PAROU em", nome)
        break
    if ax:
        print("\n".join(ax))
    if item["avisos"]:
        print(saida[-3000:])
(B / "CONFERENCIA.json").write_text(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "sandbox": str(SB),
                                                "modulos": res}, ensure_ascii=False, indent=1), encoding="utf-8")
print("todos RC 0:", all(i["rc"] == 0 for i in res) and len(res) == 2, "| avisos:", sum(i["avisos"] for i in res),
      "| fora do trio:", sum(i["fora_do_trio"] for i in res))

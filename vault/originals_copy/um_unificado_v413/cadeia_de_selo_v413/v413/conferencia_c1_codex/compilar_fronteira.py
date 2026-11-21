# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: compila a proposta de enunciado AFronteiraNaLinguaClassica sobre a caixa da v412, usando o
APonteAoTM2.olean (do Codex) que a conferencia ja' compilou em k412c\\build. So' o binario do Lean; o .olean e o log
ficam em k412c\\build e k412c\\logs. Acrescenta o resultado em k412c\\CONFERENCIA_FRONTEIRA.json."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
OUT = AQUI / "k412c"
BUILD, LOGS = OUT / "build", OUT / "logs"
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
lib = Path(r"C:\t\k412c\final\.lake")
assert (BUILD / "APonteAoTM2.olean").exists(), "APonteAoTM2.olean ainda nao compilado na conferencia"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


caminhos = [str(lib / "build" / "lib" / "lean")]
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((lib / "packages").iterdir())
             if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos.append(str(BUILD))
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
pasta = AQUI / "fronteira"
arq = pasta / "AFronteiraNaLinguaClassica.lean"
t0 = time.time()
r = subprocess.run([LEAN, "-o", str(BUILD / "AFronteiraNaLinguaClassica.olean"), arq.name], env=env, cwd=str(pasta),
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or "")
(LOGS / "AFronteiraNaLinguaClassica.log").write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (
    arq, sha(arq), r.returncode, saida), encoding="utf-8")
ax = [l.strip() for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
fora = [l for l in ax if re.search(r"\[(.*)\]", l) and
        {a.strip() for a in re.search(r"\[(.*)\]", l).group(1).split(",") if a.strip()} - TRIO]
conf = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte": str(arq), "sha256_fonte": sha(arq),
        "importa_APonteAoTM2_olean_sha256": sha(BUILD / "APonteAoTM2.olean"), "rc": r.returncode,
        "segundos": round(time.time() - t0, 1), "avisos": saida.count("warning:"), "erros": saida.count("error:"),
        "sorryAx": "sorryAx" in saida, "axiomas": ax, "fora_do_trio": fora,
        "cauda_se_falhou": saida[-3000:] if r.returncode else ""}
dest = OUT / "CONFERENCIA_FRONTEIRA.json"
tmp = OUT / "CONFERENCIA_FRONTEIRA.json.tmp"
dados = json.dumps(conf, ensure_ascii=False, indent=1).encode("utf-8")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("RC %d | %.1f s | avisos %d | erros %d | sorryAx %s | fora do trio %d" % (
    r.returncode, conf["segundos"], conf["avisos"], conf["erros"], conf["sorryAx"], len(fora)))
print("\n".join(ax))
if r.returncode or conf["erros"]:
    print(saida[-3000:])

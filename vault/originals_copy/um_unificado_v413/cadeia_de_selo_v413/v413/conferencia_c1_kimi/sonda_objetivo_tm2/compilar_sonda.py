# -*- coding: utf-8 -*-
"""gerencia c1, 19/11/2026: compila a sonda do alvo ObjetivoTM2Polinomial no MESMO ambiente em que o Kimi compilou a
APonteAoTM2 (C:\\t\\k411c + build das irmas c1 da v412 + build do Kimi; tudo so' leitura). So' o binario do Lean,
nunca lake. Nada se escreve na oficina do Kimi: .olean, log e CONFERENCIA_SONDA.json ficam em build\\ desta pasta.
Registra o sha256 da fonte e do .olean do Kimi que a sonda importou."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
B = V / "build"
B.mkdir(exist_ok=True)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SB = Path(r"C:\t\k411c\final\.lake")
V412 = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
KIMI = V412 / "candidatas_kimi"
assert Path(LEAN).exists(), "lean.exe ausente"
assert SB.exists(), "caixa k411c ausente"
assert (KIMI / "build" / "APonteAoTM2.olean").exists(), "olean do Kimi ausente"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


caminhos = [str(SB / "build" / "lib" / "lean")]
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SB / "packages").iterdir())
             if (p / ".lake" / "build" / "lib" / "lean").exists()]
for d in [V412 / "candidatas_c1" / "build", V412 / "candidatas_c1" / "build_sobre_limpas", KIMI / "build"]:
    if d.exists():
        caminhos.append(str(d))
caminhos.append(str(B))
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)

f = V / "SondaObjetivoTM2.lean"
t0 = time.time()
r = subprocess.run([LEAN, "-o", str(B / "SondaObjetivoTM2.olean"), str(f)], env=env, cwd=str(V), capture_output=True,
                   text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or "")
(B / "SondaObjetivoTM2.log").write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha(f), r.returncode, saida),
                                        encoding="utf-8")
ax = [l for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
conf = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
    "sonda": str(f), "sha256_sonda": sha(f),
    "importa": {"APonteAoTM2.lean": {"sha256": sha(KIMI / "APonteAoTM2.lean")},
                "APonteAoTM2.olean": {"sha256": sha(KIMI / "build" / "APonteAoTM2.olean")}},
    "ambiente": {"caixa": str(SB), "lean_path": caminhos},
    "rc": r.returncode, "segundos": round(time.time() - t0), "avisos": saida.count("warning:"),
    "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida, "axiomas": ax,
}
(B / "CONFERENCIA_SONDA.json").write_text(json.dumps(conf, ensure_ascii=False, indent=1), encoding="utf-8")
print("RC %d | %d s | avisos %d | erros %d | sorryAx %s" % (r.returncode, conf["segundos"], conf["avisos"], conf["erros"],
                                                           conf["sorryAx"]))
print("fonte do Kimi sha16 %s | olean sha16 %s" % (conf["importa"]["APonteAoTM2.lean"]["sha256"][:16],
                                                   conf["importa"]["APonteAoTM2.olean"]["sha256"][:16]))
print("\n".join(ax))
if r.returncode != 0 or conf["erros"] or conf["avisos"]:
    print(saida[-4000:])

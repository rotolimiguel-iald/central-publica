# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: confere, antes da Etapa 1, que os 21 modulos novos da v413 convivem com o kernel inteiro da
v412: um arquivo que importa a raiz TGLExt (todos os modulos da v412, pelo .olean selado na caixa) e os 21 novos, na
caixa da v413. Se dois modulos declararem o mesmo nome, ou instancias/notacoes colidirem, a importacao conjunta falha.
Liga tambem, na caixa da v413, o TGLExt.olean da raiz da v412 (link fisico; a caixa da v412 so' e' lida).
So' lean.exe; nada no Nos, nada no sandbox da cadeia. Recibo: insumos\\auditoria_raiz\\RAIZ_v413.json."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
CAIXA = AQUI / "caixa_v413"
LIB412 = Path(r"C:\t\k412c\final\.lake\build\lib\lean")
SB = Path(r"C:\t\k412c\final\.lake")
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
A = AQUI / "auditoria_raiz"
A.mkdir(exist_ok=True)
raiz = CAIXA / "TGLExt.olean"
if not raiz.exists():
    os.link(LIB412 / "TGLExt.olean", raiz)
assert os.path.samefile(LIB412 / "TGLExt.olean", raiz)
novos = sorted(json.loads((AQUI / "MANIFESTO_PEDRAS_v413.json").read_text(encoding="utf-8"))["modulos_novos"])
assert len(novos) == 21
for m in novos:
    assert (CAIXA / (m.replace(".", os.sep) + ".olean")).exists(), m
f = A / "RaizV413.lean"
f.write_text("import TGLExt\n" + "".join("import %s\n" % m for m in novos) + "\n#print axioms TGLExt.PonteCookLevin.a_ponte\n",
             encoding="utf-8")
caminhos = [str(CAIXA), str(LIB412)] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SB / "packages").iterdir())
                                         if (p / ".lake" / "build" / "lib" / "lean").exists()]
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
t0 = time.time()
r = subprocess.run([LEAN, f.name], env=env, cwd=str(A), capture_output=True, text=True, encoding="utf-8", errors="replace")
saida = (r.stdout or "") + (r.stderr or "")
(A / "RaizV413.log").write_text("RC: %d\n%s" % (r.returncode, saida), encoding="utf-8")
ok = r.returncode == 0 and "error" not in saida and "depends on axioms: [propext, Classical.choice, Quot.sound]" in saida
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "rc": r.returncode, "s": round(time.time() - t0, 1),
       "importa": ["TGLExt"] + novos, "saida": saida[-3000:], "bom": ok,
       "raiz_v412_olean_sha256": hashlib.sha256((LIB412 / "TGLExt.olean").read_bytes()).hexdigest()}
d = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = A / "RAIZ_v413.json.tmp"
tmp.write_bytes(d)
tmp.replace(A / "RAIZ_v413.json")
print("raiz da v412 + 21 novos: RC %d | %.1f s | bom %s" % (r.returncode, rec["s"], ok))
if not ok:
    print(saida[-3000:])

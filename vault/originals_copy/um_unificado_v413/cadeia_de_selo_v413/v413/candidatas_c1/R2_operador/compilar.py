# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: compila a R2 Operador e o arquivo de axiomas sobre o kernel da v412 (C:\\t\\k412c; so' o
binario do Lean, nunca lake). Le os relatorios de axiomas na SAIDA INTEIRA (o Lean quebra listas longas em varias linhas;
o filtro de linha unica da R0 nao lia as continuacoes). Fail-closed: relatorio faltando, axioma fora do trio, sorryAx,
aviso ou erro => falha. Recibo: build\\CONFERENCIA.json."""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
B = V / "build"
B.mkdir(exist_ok=True)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SB = Path(r"C:\t\k412c\final\.lake")
assert Path(LEAN).exists() and SB.exists()
caminhos = [str(SB / "build" / "lib" / "lean")]
caminhos += [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SB / "packages").iterdir())
             if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(B)]
env = dict(os.environ)
env["LEAN_PATH"] = ";".join(caminhos)
TRIO = {"propext", "Classical.choice", "Quot.sound"}
REL = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.S)
SEM = re.compile(r"'([^']+)' does not depend on any axioms")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


res, ok = [], True
for nome in ["Operador", "OperadorAxiomas"]:
    f = V / (nome + ".lean")
    t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(B / (nome + ".olean")), f.name], env=env, cwd=str(V), capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (B / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha(f), r.returncode, saida),
                                     encoding="utf-8")
    rel = {n: sorted({a.strip() for a in l.replace("\n", " ").split(",") if a.strip()}) for n, l in REL.findall(saida)}
    rel.update({n: [] for n in SEM.findall(saida)})
    pedidos = re.findall(r"^#print axioms\s+(\S+)", f.read_text(encoding="utf-8"), re.M)
    faltam = [p for p in pedidos if p not in rel and not any(x.endswith("." + p) for x in rel)]
    fora = {n: sorted(set(a) - TRIO) for n, a in rel.items() if set(a) - TRIO}
    item = {"modulo": nome, "sha256": sha(f), "rc": r.returncode, "s": round(time.time() - t0, 1),
            "avisos": saida.count("warning:"), "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida,
            "pedidos": len(pedidos), "relatorios": len(rel), "faltando": faltam, "fora_do_trio": fora, "axiomas": rel}
    res.append(item)
    bom = not (r.returncode or item["erros"] or item["avisos"] or item["sorryAx"] or faltam or fora)
    ok = ok and bom
    print("%-16s RC %d | %5.1f s | avisos %d | erros %d | sorryAx %s | pedidos %d, relatorios %d, faltando %d, fora do "
          "trio %d | sha16 %s" % (nome, r.returncode, item["s"], item["avisos"], item["erros"], item["sorryAx"],
                                  len(pedidos), len(rel), len(faltam), len(fora), item["sha256"][:16]), flush=True)
    if not bom:
        print(saida[-4000:])
        break
dados = json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "caixa": str(SB), "lean_path": caminhos,
                    "todos_bons": ok and len(res) == 2, "modulos": res}, ensure_ascii=False, indent=1).encode("utf-8")
tmp = B / "CONFERENCIA.json.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(B / "CONFERENCIA.json")
print("todos bons:", ok and len(res) == 2)

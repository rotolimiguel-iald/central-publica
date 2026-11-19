# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: passo 3 da nona lista. Compila as copias de trabalho de pedras_novas\\ (as 73 fontes novas), na ordem das
importacoes locais, SO' com o binario do Lean, sobre os compilados do k411c e os das 44 pedras da oitava lista (pedras_limpas\\build),
e mais nada: nenhum build de candidata antiga entra no caminho. Saida em pedras_novas\\build (.olean, .log com o SHA256 da fonte).
Pula o modulo cujo log ja' e' da fonte atual com RC 0 (a nao ser com --tudo). Para no primeiro que falhar. NUNCA lake.
Uso: nona_lista_passo3_compilar.py [--tudo]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
fontes, build = V / "pedras_novas", V / "pedras_novas" / "build"
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
assert Path(LEAN).exists() and SANDBOX.exists() and fontes.exists()
build.mkdir(parents=True, exist_ok=True)
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()]
caminhos += [str(V / "pedras_limpas" / "build"), str(build)]
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
res, refeitos = [], set()
for nome in ordem:
    f = fontes / (nome + ".lean"); sha = hashlib.sha256(f.read_bytes()).hexdigest(); t0 = time.time()
    log = build / (nome + ".log"); pulou = False
    if "--tudo" not in sys.argv and log.exists() and (build / (nome + ".olean")).exists() and not (set(dep[nome]) & refeitos):
        lt = log.read_text(encoding="utf-8", errors="replace")
        if ("SHA256: " + sha) in lt and re.search(r"^RC: 0\s*$", lt, flags=re.M):
            saida = lt.split("SAIDA:\n", 1)[1] if "SAIDA:\n" in lt else ""; rc = 0; pulou = True
    if not pulou:
        r = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(f)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        saida = (r.stdout or "") + (r.stderr or ""); rc = r.returncode; refeitos.add(nome)
        log.write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (f, sha, rc, saida), encoding="utf-8")
    ax = [l for l in saida.split("\n") if "depends on axioms" in l or "does not depend" in l]
    fora = [l for l in ax if "sorryAx" in l or ("[" in l and not set(l.split("[", 1)[1].rstrip("]").replace(" ", "").split(",")) <= {"propext", "Classical.choice", "Quot.sound", ""})]
    item = {"modulo": nome, "sha256": sha, "rc": rc, "s": round(time.time() - t0), "avisos": saida.count("warning:"), "erros": saida.count("error:"), "sorryAx": "sorryAx" in saida,
            "linhas_de_axiomas": len(ax), "fora_do_trio": len(fora), "imports_locais": dep[nome], "reaproveitado_do_log": pulou}
    res.append(item)
    print("%-28s RC %d | %3d s | avisos %d | erros %d | axiomas %3d linhas, fora do trio %d | %s" % (nome, rc, item["s"], item["avisos"], item["erros"], len(ax), len(fora), "log" if pulou else "compilado"), flush=True)
    if rc != 0:
        print(saida[-2500:]); print("PAROU em", nome); break
p = build / "COMPILACAO_NOVAS.json"; tmp = p.with_name(p.name + ".tmp_c1")
tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "caminho_de_busca": caminhos, "ordem": ordem, "modulos": res}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
print("modulos:", len(res), "de", len(ordem), "| todos RC 0:", all(i["rc"] == 0 for i in res), "| avisos:", sum(i["avisos"] for i in res), "| fora do trio:", sum(i["fora_do_trio"] for i in res), "| sorryAx:", any(i["sorryAx"] for i in res), "| linhas de axiomas:", sum(i["linhas_de_axiomas"] for i in res))

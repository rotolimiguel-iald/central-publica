# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: SEXTA lista de pedras da v412 = a quinta (40 modulos, sem mudanca) mais duas pedras novas, com os
nomes dados pelo autor: Token2 e AMaquina (frente A). Passos, parando no primeiro que falhar:
 1. copia candidatas_c1\\{Token2,AMaquina}.lean para pedras_limpas\\ (nao sobrescreve arquivo diferente) e congela em candidatas_c1\\REV62\\;
 2. compila as duas, nessa ordem, so' com o binario do Lean (NUNCA lake), sobre os compilados do k411c e os de pedras_limpas\\build;
    .olean e log em pedras_limpas\\build, no mesmo formato dos outros;
 3. confere que os 40 da quinta lista seguem com o sha256 do manifesto R5 e com log da fonte atual;
 4. congela os 42 em insumos\\pedras_r6 e grava insumos\\MANIFESTO_PEDRAS_v412_R6.json.
Uso: sexta_lista_v412.py [--executar]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
C, LIMPAS, DEST = V / "candidatas_c1", V / "pedras_limpas", V / "insumos" / "pedras_r6"
NOVAS = ["Token2", "AMaquina"]
EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
man5 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R5.json").read_text(encoding="utf-8"))
molde = next(m for m in man5["modulos"] if m["modulo"] == "AMedidaEOIf")
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake")
assert Path(LEAN).exists() and SANDBOX.exists()
build = LIMPAS / "build"
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()] + [str(build)]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
# 1 e 2
for nome in NOVAS:
    src = C / (nome + ".lean"); b = src.read_bytes(); alvo = LIMPAS / (nome + ".lean"); rev = C / "REV62" / (nome + ".lean")
    print("%-10s fonte %d B sha16 %s" % (nome, len(b), hashlib.sha256(b).hexdigest()[:16]))
    if not EXEC:
        continue
    for d in (alvo, rev):
        d.parent.mkdir(exist_ok=True)
        if d.exists():
            assert d.read_bytes() == b, "ja' existe e difere: " + str(d)
        else:
            d.write_bytes(b)
    t0 = time.time()
    r = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(alvo)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    (build / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (alvo, sha(alvo), r.returncode, saida), encoding="utf-8")
    print("   compilada: RC %d | %d s | avisos %d | erros %d | sorryAx %s" % (r.returncode, round(time.time() - t0), saida.count("warning:"), saida.count("error:"), "sorryAx" in saida))
    assert r.returncode == 0 and "sorryAx" not in saida and saida.count("error:") == 0, saida[-3000:]
if not EXEC:
    print("ENSAIO A SECO: nada copiado, compilado nem gravado."); sys.exit(0)
# 3 e 4
itens = []
for m in man5["modulos"]:
    f = LIMPAS / (m["modulo"] + ".lean")
    assert sha(f) == m["sha256"], "mudou desde a quinta lista: " + m["modulo"]
    log = (build / (m["modulo"] + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + m["sha256"]) in log and re.search(r"^RC: 0\s*$", log, flags=re.M), "log: " + m["modulo"]
    itens.append(dict(m, mudou_da_quinta_lista=False))
for nome in NOVAS:
    f = LIMPAS / (nome + ".lean"); b = f.read_bytes(); t = b.decode("utf-8")
    log = (build / (nome + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + sha(f)) in log and re.search(r"^RC: 0\s*$", log, flags=re.M)
    imps = re.findall(r"^import\s+(\S+)", t, flags=re.M)
    itens.append({"modulo": nome, "frente": molde["frente"], "de_quem": molde["de_quem"],
                  "estado_da_revisao": "nova, de 17/11; lida pelo revisor na ordem 029 e emendada",
                  "origem": str(f), "sha256": sha(f), "bytes": len(b), "fonte_revista_sha256": None,
                  "codigo_identico_ao_da_fonte_revista": None, "compilou_rc0_com_log_desta_fonte": True,
                  "avisos_no_log": log.count("warning:"), "imports": imps,
                  "imports_de_candidatas": [i for i in imps if not i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL."))],
                  "namespaces": re.findall(r"^namespace\s+(\S+)", t, flags=re.M),
                  "declaracoes_theorem_lemma": len(re.findall(r"^(?:theorem|lemma)\s", t, flags=re.M)),
                  "linhas_print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)),
                  "sorry": len(re.findall(r"\bsorry\b", re.sub(r"/-.*?-/", "", t, flags=re.S))), "mudou_da_quinta_lista": True})
nomes = {i["modulo"] for i in itens}
soltos = sorted({i for it in itens for i in it["imports_de_candidatas"]})
man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
       "nota": "sexta lista, de 17/11: os 40 modulos da quinta, sem mudanca, mais duas pedras novas da frente A, com os nomes dados pelo autor (Token2 e AMaquina); cada log de compilacao e' da fonte congelada",
       "n_modulos": len(itens), "novas_em_relacao_a_quinta_lista": NOVAS, "ficam_fora": man5["ficam_fora"],
       "imports_soltos_de_candidatas": soltos, "imports_soltos_sem_modulo_no_conjunto": [i for i in soltos if i not in nomes], "modulos": itens}
assert man["n_modulos"] == 42 and not man["imports_soltos_sem_modulo_no_conjunto"], man["imports_soltos_sem_modulo_no_conjunto"]
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    alvo = DEST / (it["modulo"] + ".lean"); b = (LIMPAS / (it["modulo"] + ".lean")).read_bytes()
    if alvo.exists():
        assert alvo.read_bytes() == b
    else:
        alvo.write_bytes(b)
out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R6.json"; assert not out.exists(), "ja' existe"
out.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
print("modulos:", len(itens), "| declaracoes:", sum(i["declaracoes_theorem_lemma"] for i in itens), "| sorry:", sum(i["sorry"] for i in itens), "| avisos:", sum(i["avisos_no_log"] for i in itens))
print("gravado:", out, "| sha16", sha(out)[:16])

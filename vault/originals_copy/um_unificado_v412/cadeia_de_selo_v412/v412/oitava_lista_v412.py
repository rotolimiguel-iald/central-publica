# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: OITAVA lista de pedras da v412 = a setima (42 modulos, sem mudanca) mais as duas pedras aprovadas com
escopo pelo revisor na ordem 030: OPassoEOFim (nome aceito pelo autor) e OPsibitEACompressao (nome provisorio), frente A.
Passos: (1) copia candidatas_c1\\{OPassoEOFim,OPsibitEACompressao}.lean para pedras_limpas\\ (nao sobrescreve diferente) e congela em
candidatas_c1\\REV67\\; (2) compila as duas so' com o binario do Lean sobre k411c + pedras_limpas\\build; (3) confere que os 42 da setima
seguem com o sha256 do manifesto R7 e log da fonte atual; (4) congela os 44 em insumos\\pedras_r8 e grava MANIFESTO_PEDRAS_v412_R8.json;
(5) deriva e roda o script das ancoras R8 (com os dois modulos no registro da camada cientifica). Uso: oitava_lista_v412.py [--executar]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
C, LIMPAS, DEST = V / "candidatas_c1", V / "pedras_limpas", V / "insumos" / "pedras_r8"
NOVAS = ["OPassoEOFim", "OPsibitEACompressao"]
EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
man7 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json").read_text(encoding="utf-8"))
molde = next(m for m in man7["modulos"] if m["modulo"] == "AMedidaEOIf")
for nome, rev in (("OPassoEOFim", "REV63"), ("OPsibitEACompressao", "REV65")):
    assert sha(C / (nome + ".lean")) == sha(C / rev / (nome + ".lean")), "a fonte de %s nao e' a %s revista" % (nome, rev)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake"); build = LIMPAS / "build"
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()] + [str(build)]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
for nome in NOVAS:
    src = C / (nome + ".lean"); b = src.read_bytes(); alvo = LIMPAS / (nome + ".lean"); rev = C / "REV67" / (nome + ".lean")
    print("%-22s fonte %d B sha16 %s" % (nome, len(b), hashlib.sha256(b).hexdigest()[:16]))
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
itens = []
for m in man7["modulos"]:
    f = LIMPAS / (m["modulo"] + ".lean"); assert sha(f) == m["sha256"], "mudou desde a setima lista: " + m["modulo"]
    log = (build / (m["modulo"] + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + m["sha256"]) in log and re.search(r"^RC: 0\s*$", log, flags=re.M), "log: " + m["modulo"]
    it = dict(m, mudou_da_setima_lista=False); it.pop("mudou_da_sexta_lista", None); itens.append(it)
for nome in NOVAS:
    f = LIMPAS / (nome + ".lean"); b = f.read_bytes(); t = b.decode("utf-8")
    log = (build / (nome + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + sha(f)) in log and re.search(r"^RC: 0\s*$", log, flags=re.M)
    imps = re.findall(r"^import\s+(\S+)", t, flags=re.M)
    itens.append({"modulo": nome, "frente": molde["frente"], "de_quem": molde["de_quem"],
                  "estado_da_revisao": "nova, de 17/11; parecer favoravel com escopo na ordem 030 (T1/T2)",
                  "origem": str(f), "sha256": sha(f), "bytes": len(b), "fonte_revista_sha256": None, "codigo_identico_ao_da_fonte_revista": None,
                  "compilou_rc0_com_log_desta_fonte": True, "avisos_no_log": log.count("warning:"), "imports": imps,
                  "imports_de_candidatas": [i for i in imps if not i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL."))],
                  "namespaces": re.findall(r"^namespace\s+(\S+)", t, flags=re.M),
                  "declaracoes_theorem_lemma": len(re.findall(r"^(?:theorem|lemma)\s", t, flags=re.M)),
                  "linhas_print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)),
                  "sorry": len(re.findall(r"\bsorry\b", re.sub(r"/-.*?-/", "", t, flags=re.S))), "mudou_da_setima_lista": True})
nomes = {i["modulo"] for i in itens}; soltos = sorted({i for it in itens for i in it["imports_de_candidatas"]})
man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
       "nota": "oitava lista, de 17/11: os 42 modulos da setima, sem mudanca, mais as duas pedras aprovadas com escopo na ordem 030 (OPassoEOFim, OPsibitEACompressao), frente A; cada log de compilacao e' da fonte congelada",
       "n_modulos": len(itens), "novas_em_relacao_a_setima_lista": NOVAS, "ficam_fora": man7["ficam_fora"],
       "ficam_para_a_v413": ["AParedeDoNome (gerencia)", "OResumoEPsiBit (Kimi)", "as treze do Codex em psibit_leitor_direto_Codex e psibit_fronteira_fita_Codex"],
       "imports_soltos_de_candidatas": soltos, "imports_soltos_sem_modulo_no_conjunto": [i for i in soltos if i not in nomes], "modulos": itens}
assert man["n_modulos"] == 44 and not man["imports_soltos_sem_modulo_no_conjunto"], man["imports_soltos_sem_modulo_no_conjunto"]
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    alvo = DEST / (it["modulo"] + ".lean"); b = (LIMPAS / (it["modulo"] + ".lean")).read_bytes()
    if alvo.exists():
        assert alvo.read_bytes() == b
    else:
        alvo.write_bytes(b)
out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R8.json"; assert not out.exists(), "ja' existe"
out.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
print("manifesto R8:", len(itens), "modulos | declaracoes:", sum(i["declaracoes_theorem_lemma"] for i in itens), "| sorry:", sum(i["sorry"] for i in itens), "| avisos:", sum(i["avisos_no_log"] for i in itens), "| sha16", sha(out)[:16])
a7 = (V / "ancoras_propostas_v412_r7.py").read_text(encoding="utf-8")
a8 = a7.replace("MANIFESTO_PEDRAS_v412_R7.json", "MANIFESTO_PEDRAS_v412_R8.json").replace('"pedras_r7"', '"pedras_r8"').replace("ANCORAS_PROPOSTAS_v412_R7.json", "ANCORAS_PROPOSTAS_v412_R8.json")
marca = '"Token2", "AMaquina"],'
assert a8.count(marca) == 1, a8.count(marca)
a8 = a8.replace(marca, '"Token2", "AMaquina",\n                                    "OPassoEOFim", "OPsibitEACompressao"],   # (oitava lista, 17/11)')
p8 = V / "ancoras_propostas_v412_r8.py"; assert not p8.exists(); p8.write_bytes(a8.encode("utf-8"))
ra = subprocess.run([sys.executable, "-B", "-X", "utf8", str(p8), "--executar"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("\n".join((ra.stdout or "").strip().split("\n")[-3:])); assert ra.returncode == 0, ra.stderr[-1500:]

# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: SETIMA lista de pedras da v412 = a sexta (42 modulos) com UMA mudanca de texto: sai do cabecalho da
Token2 a tese da tautologia, que o autor retirou; entra o que se sabe (o procedimento da casa, soletrado, custa o todo; a
pergunta do enunciado de Cook nao e' tautologica e segue em aberto). So' comentario; codigo igual.
Passos: (1) duas trocas exatas em candidatas_c1\\Token2.lean (backup de bytes); (2) copia para pedras_limpas (backup) e congela
em candidatas_c1\\REV64; (3) recompila Token2 e AMaquina (que a importa) so' com o binario do Lean; (4) manifesto R7 e copia em
insumos\\pedras_r7; (5) deriva e roda o script das ancoras R7. Uso: setima_lista_v412.py [--executar]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
C, LIMPAS, DEST = V / "candidatas_c1", V / "pedras_limpas", V / "insumos" / "pedras_r7"
EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
TROCAS = [
    ("lei é polinomial (`o_custo_pela_lei_e_polinomial`). Tese da teoria: fora dessa estrutura, a pergunta que resta é\ntautológica: quem conta por letra de um vocabulário fixo mede a fita com a fita.\n\nA solução na estrutura da TGL e a tese da tautologia são posições da teoria. Os termos citados dão a contagem das\ncláusulas no modelo da casa (`AFitaEACauda.o_tempo_da_maquina_e_o_comprimento_da_fita`, em que a fita é a lista das\ncláusulas) e a cota dos códigos que distinguem todos os conjuntos (item 9); não demonstram essa tese para o enunciado de\nCook. A creditação é do Instituto.",
     "lei é polinomial (`o_custo_pela_lei_e_polinomial`). A solução na estrutura da TGL é posição da teoria.\n\nFora dessa estrutura, contando letra por letra, o procedimento daqui custa o todo: um código que distinga todos os\nconjuntos pede pelo menos `2ⁿ` casas (item 9). Isso não responde ao enunciado de Cook, que pergunta se há ALGUM\nprocedimento de letras com número polinomial de passos para toda fórmula; essa pergunta não é tautológica e segue em\naberto. A creditação é do Instituto."),
    ("`[INPUT]` a lei e a tese (a solução na estrutura da TGL; a pergunta que resta\nfora dela é tautológica) ·", "`[INPUT]` a lei e a tese (a solução na estrutura da TGL) ·"),
]
f = C / "Token2.lean"; bruto = f.read_bytes(); t = bruto.decode("utf-8")
for a, b in TROCAS:
    assert t.count(a) == 1, (t.count(a), a[:70]); t = t.replace(a, b)
assert "tautol" not in t.replace("não é tautológica", "") and "«" not in t
novo = t.encode("utf-8")
print("Token2: %d -> %d B | sha16 %s" % (len(bruto), len(novo), hashlib.sha256(novo).hexdigest()[:16]))
if not EXEC:
    print("ENSAIO A SECO"); sys.exit(0)
ts = time.strftime("%Y%m%d_%H%M%S")
for alvo in (f, LIMPAS / "Token2.lean"):
    alvo.with_name(alvo.name + ".bak_" + ts).write_bytes(alvo.read_bytes())
    tmp = alvo.with_name(alvo.name + ".tmp_c1"); tmp.write_bytes(novo); tmp.replace(alvo); assert alvo.read_bytes() == novo
(C / "REV64").mkdir(exist_ok=True); r = C / "REV64" / "Token2.lean"; assert not r.exists(); r.write_bytes(novo)
LEAN = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
SANDBOX = Path(r"C:\t\k411c\final\.lake"); build = LIMPAS / "build"
caminhos = [str(SANDBOX / "build" / "lib" / "lean")] + [str(p / ".lake" / "build" / "lib" / "lean") for p in sorted((SANDBOX / "packages").iterdir()) if (p / ".lake" / "build" / "lib" / "lean").exists()] + [str(build)]
env = dict(os.environ); env["LEAN_PATH"] = ";".join(caminhos)
for nome in ("Token2", "AMaquina"):
    alvo = LIMPAS / (nome + ".lean")
    rr = subprocess.run([LEAN, "-o", str(build / (nome + ".olean")), str(alvo)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    saida = (rr.stdout or "") + (rr.stderr or "")
    (build / (nome + ".log")).write_text("FONTE: %s\nSHA256: %s\nRC: %d\nSAIDA:\n%s" % (alvo, sha(alvo), rr.returncode, saida), encoding="utf-8")
    print("   %s compilada: RC %d | avisos %d | erros %d" % (nome, rr.returncode, saida.count("warning:"), saida.count("error:")))
    assert rr.returncode == 0 and "sorryAx" not in saida and saida.count("error:") == 0, saida[-2000:]
man6 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R6.json").read_text(encoding="utf-8"))
itens = []
for m in man6["modulos"]:
    p = LIMPAS / (m["modulo"] + ".lean"); s = sha(p)
    log = (build / (m["modulo"] + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + s) in log and re.search(r"^RC: 0\s*$", log, flags=re.M), m["modulo"]
    mudou = s != m["sha256"]
    assert mudou == (m["modulo"] == "Token2"), m["modulo"]
    it = dict(m, sha256=s, bytes=p.stat().st_size, mudou_da_sexta_lista=mudou); it.pop("mudou_da_quinta_lista", None)
    if mudou:
        it["estado_da_revisao"] = "nova, de 17/11; lida pelo revisor na ordem 029 e emendada; em 17/11 saiu do cabecalho a tese da tautologia, retirada pelo autor"
    itens.append(it)
man = dict(man6, gerado_em=time.strftime("%Y-%m-%d %H:%M:%S"), modulos=itens, mudaram_da_sexta_lista=["Token2"],
           nota="setima lista, de 17/11: os 42 modulos da sexta, com uma mudanca de texto no cabecalho da Token2 (sai a tese da tautologia); codigo igual; cada log de compilacao e' da fonte congelada")
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    (DEST / (it["modulo"] + ".lean")).write_bytes((LIMPAS / (it["modulo"] + ".lean")).read_bytes())
out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json"; assert not out.exists()
out.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
print("manifesto R7:", len(itens), "modulos | sha16", sha(out)[:16])
a6 = (V / "ancoras_propostas_v412_r6.py").read_text(encoding="utf-8")
a7 = a6.replace("MANIFESTO_PEDRAS_v412_R6.json", "MANIFESTO_PEDRAS_v412_R7.json").replace('"pedras_r6"', '"pedras_r7"').replace("ANCORAS_PROPOSTAS_v412_R6.json", "ANCORAS_PROPOSTAS_v412_R7.json")
assert a7 != a6 and "R6" not in a7.replace("_r6", "")
p7 = V / "ancoras_propostas_v412_r7.py"; assert not p7.exists(); p7.write_bytes(a7.encode("utf-8"))
ra = subprocess.run([sys.executable, "-B", "-X", "utf8", str(p7), "--executar"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("\n".join((ra.stdout or "").strip().split("\n")[-2:])); assert ra.returncode == 0, ra.stderr[-1500:]

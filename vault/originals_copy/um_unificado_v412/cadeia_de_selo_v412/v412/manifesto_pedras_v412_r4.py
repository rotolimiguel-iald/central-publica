# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: QUARTA lista de pedras da v412: as 40 da terceira lista, com os comentarios e docstrings LIMPOS pelo
metodo de 17/11 (o um.py e' a compilacao do que e' verdade; a conversa fica em paralelo). As fontes vem de pedras_limpas\\.
Para cada modulo confere: (1) o codigo fora de comentarios e' identico ao da fonte revista (insumos\\pedras_r3); (2) o log de
compilacao em pedras_limpas\\build e' DESTA fonte (sha256) e tem RC 0. Congela em insumos\\pedras_r4 e grava
insumos\\MANIFESTO_PEDRAS_v412_R4.json. Nao sobrescreve copia existente diferente. Uso: manifesto_pedras_v412_r4.py [--executar]"""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
LIMPAS, R3, DEST = V / "pedras_limpas", V / "insumos" / "pedras_r3", V / "insumos" / "pedras_r4"
man3 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R3.json").read_text(encoding="utf-8"))


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


itens = []
for m3 in man3["modulos"]:
    nome = m3["modulo"]
    src = LIMPAS / (nome + ".lean"); b = src.read_bytes(); t = b.decode("utf-8")
    o = (R3 / (nome + ".lean")).read_bytes()
    assert sem_comentarios(t) == sem_comentarios(o.decode("utf-8")), "codigo difere: " + nome
    sha = hashlib.sha256(b).hexdigest()
    log = (LIMPAS / "build" / (nome + ".log")).read_text(encoding="utf-8", errors="replace")
    assert ("SHA256: " + sha) in log, "o log nao e' desta fonte: " + nome
    assert re.search(r"^RC: 0\s*$", log, flags=re.M), "RC diferente de zero: " + nome
    imps = re.findall(r"^import\s+(\S+)", t, flags=re.M)
    itens.append({"modulo": nome, "frente": m3["frente"], "de_quem": m3["de_quem"],
                  "estado_da_revisao": "limpa pelo metodo de 17/11" if b != o else "sem mudanca (nao tinha historia)",
                  "origem": str(src), "sha256": sha, "bytes": len(b),
                  "fonte_revista_sha256": hashlib.sha256(o).hexdigest(), "codigo_identico_ao_da_fonte_revista": True,
                  "compilou_rc0_com_log_desta_fonte": True, "avisos_no_log": log.count("warning:"),
                  "imports": imps,
                  "imports_de_candidatas": [i for i in imps if not i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL."))],
                  "namespaces": re.findall(r"^namespace\s+(\S+)", t, flags=re.M),
                  "declaracoes_theorem_lemma": len(re.findall(r"^(?:theorem|lemma)\s", t, flags=re.M)),
                  "linhas_print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)),
                  "sorry": len(re.findall(r"\bsorry\b", re.sub(r"/-.*?-/", "", t, flags=re.S)))})
nomes = {i["modulo"] for i in itens}
soltos = sorted({i for it in itens for i in it["imports_de_candidatas"]})
man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
       "nota": "quarta lista, de 17/11: os 40 modulos da terceira, com comentarios e docstrings limpos pelo metodo (so' o que e' verdade); codigo identico ao das fontes revistas; cada log de compilacao e' da fonte congelada",
       "n_modulos": len(itens), "mudaram": sum(1 for i in itens if i["estado_da_revisao"].startswith("limpa")),
       "ficam_fora": man3["ficam_fora"], "imports_soltos_de_candidatas": soltos,
       "imports_soltos_sem_modulo_no_conjunto": [i for i in soltos if i not in nomes], "modulos": itens}
print("modulos:", len(itens), "| mudaram:", man["mudaram"], "| declaracoes:", sum(i["declaracoes_theorem_lemma"] for i in itens),
      "| sem modulo no conjunto:", man["imports_soltos_sem_modulo_no_conjunto"], "| sorry:", sum(i["sorry"] for i in itens),
      "| avisos nos logs:", sum(i["avisos_no_log"] for i in itens))
if "--executar" not in sys.argv:
    print("ENSAIO A SECO: nada gravado."); sys.exit(0)
DEST.mkdir(parents=True, exist_ok=True)
for it in itens:
    alvo = DEST / (it["modulo"] + ".lean"); b = Path(it["origem"]).read_bytes()
    if alvo.exists():
        assert alvo.read_bytes() == b, "copia existente difere: " + alvo.name
    else:
        alvo.write_bytes(b); assert alvo.stat().st_size == len(b)
out = V / "insumos" / "MANIFESTO_PEDRAS_v412_R4.json"
assert not out.exists(), "ja' existe"
out.write_bytes(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
print("gravado:", out, "| sha16", hashlib.sha256(out.read_bytes()).hexdigest()[:16])

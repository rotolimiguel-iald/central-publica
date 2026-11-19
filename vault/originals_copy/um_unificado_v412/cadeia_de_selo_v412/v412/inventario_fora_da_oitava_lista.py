# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: inventario, so' leitura, de toda fonte Lean que esta' FORA da oitava lista da v412 e que a ordem do autor
de 18/11 manda entrar: candidatas_c1\\AParedeDoNome, candidatas_kimi\\*.lean e as pastas *_Codex de revisao_orquestrador (as de
conferencia_0NN nao entram: sao conferencias de ordens ja' devolvidas). Para cada fonte: sha256, bytes, imports, namespaces, contagem
de theorem/lemma, de #print axioms, de sorry fora de comentario; colisoes de nome de modulo entre pastas (iguais por bytes ou nao);
colisoes de namespace; imports que nao se resolvem no conjunto novo + oitava lista + kernel. Grava INVENTARIO_FORA_DA_OITAVA_LISTA.json."""
import hashlib, json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
RO = V / "revisao_orquestrador"
man8 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R8.json").read_text(encoding="utf-8"))
na_oitava = {m["modulo"] for m in man8["modulos"]}
PSIBIT = ["psibit_leitor_direto_Codex", "psibit_fronteira_fita_Codex", "psibit_polinomio_por_letra_Codex", "conferencia_curva_estado_Codex",
          "transicao_rotulos_Codex", "clausulas_cruzadas_fita_Codex", "ramificacao_global_fita_Codex", "nome_no_ramo_Codex",
          "reuso_compatibilidades_Codex", "chave_angulada_Codex", "handshake_nome_Codex"]
sha_oitava = {m["modulo"]: m["sha256"] for m in man8["modulos"]}
pastas = [("gerencia", V / "candidatas_c1", ["AParedeDoNome.lean", "OSeparadorNoPercurso.lean"]), ("Kimi", V / "candidatas_kimi", None)]
for d in sorted(RO.iterdir()):
    if d.is_dir() and d.name in PSIBIT:
        pastas.append(("Codex", d, None))
itens = []
for quem, pasta, so in pastas:
    for f in sorted(pasta.glob("*.lean")):
        if so and f.name not in so:
            continue
        b = f.read_bytes(); t = b.decode("utf-8"); sem = re.sub(r"/-.*?-/", "", t, flags=re.S); sem = re.sub(r"--.*", "", sem)
        itens.append({"modulo": f.stem, "de_quem": quem, "pasta": pasta.name, "caminho": str(f), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
                      "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(f.stat().st_mtime)),
                      "imports": re.findall(r"^import\s+(\S+)", t, flags=re.M), "namespaces": re.findall(r"^namespace\s+(\S+)", t, flags=re.M),
                      "theorem_lemma": len(re.findall(r"^(?:private\s+|protected\s+)?(?:theorem|lemma)\s", t, flags=re.M)),
                      "print_axioms": len(re.findall(r"^#print axioms", t, flags=re.M)), "sorry": len(re.findall(r"\bsorry\b", sem)),
                      "axiom_decl": len(re.findall(r"^axiom\s", sem, flags=re.M)), "native_decide": len(re.findall(r"native_decide", sem)),
                      "tem_olean_ao_lado": (f.with_suffix(".olean")).exists()})
por_nome = {}
for it in itens:
    por_nome.setdefault(it["modulo"], []).append(it)
colisoes = []
for nome, lst in sorted(por_nome.items()):
    if len(lst) > 1:
        shas = sorted({i["sha256"] for i in lst})
        colisoes.append({"modulo": nome, "copias": [(i["pasta"], i["sha256"][:16], i["bytes"], i["mtime"]) for i in lst], "identicas": len(shas) == 1})
ja_na_oitava = sorted(n for n in por_nome if n in na_oitava)
nomes = set(por_nome) | na_oitava
soltos = {}
for it in itens:
    for i in it["imports"]:
        if i.startswith(("TGLExt.", "Mathlib", "ChatgptAudit", "TGL.", "Init", "Std", "Lean", "Batteries", "Aesop")):
            continue
        if i not in nomes:
            soltos.setdefault(i, []).append(it["pasta"] + "/" + it["modulo"])
ns = {}
for it in itens:
    for n in it["namespaces"]:
        ns.setdefault(n, set()).add(it["modulo"])
ns_col = {n: sorted(m) for n, m in ns.items() if len(m) > 1}
out = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n_fontes": len(itens), "n_nomes_distintos": len(por_nome), "colisoes_de_nome": colisoes,
       "nomes_que_ja_estao_na_oitava_lista": ja_na_oitava, "imports_sem_modulo": soltos, "namespaces_em_mais_de_um_modulo": ns_col, "itens": itens}
p = V / "INVENTARIO_FORA_DA_OITAVA_LISTA.json"; tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
print("fontes:", len(itens), "| nomes distintos:", len(por_nome), "| theorem/lemma:", sum(i["theorem_lemma"] for i in itens), "| sorry:", sum(i["sorry"] for i in itens), "| axiom:", sum(i["axiom_decl"] for i in itens), "| native_decide:", sum(i["native_decide"] for i in itens))
for quem, pasta, _ in pastas:
    l = [i for i in itens if i["pasta"] == pasta.name]
    print("  %-8s %-40s %3d fontes | %4d teoremas | sem #print axioms: %s" % (quem, pasta.name, len(l), sum(i["theorem_lemma"] for i in l), [i["modulo"] for i in l if not i["print_axioms"]]))
print("COLISOES DE NOME:", len(colisoes))
for c in colisoes:
    print("  ", c["modulo"], "| identicas:", c["identicas"], "|", c["copias"])
print("ja' na oitava lista:", [(n, [(i["pasta"], i["sha256"] == sha_oitava[n]) for i in por_nome[n]]) for n in ja_na_oitava])
print("imports sem modulo:", soltos)
print("namespaces repetidos:", len(ns_col))
for n, m in sorted(ns_col.items()):
    print("  ", n, m)

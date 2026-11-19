"""R5 (so' leitura): mostra a forma do insumo das ancoras R10 e a forma dos #print axioms e namespaces das fontes da frente C."""
import collections, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L
a = L.ler_json(L.ANCORAS); m = L.ler_json(L.MANIFESTO)
ent = {x["modulo"]: x for x in m["modulos"]}
for reg, itens in a["registros"].items():
    ch = collections.Counter(k for it in itens for k in it)
    print(reg, len(itens), dict(ch))
    tot = {k: sum(len(it.get(k) or []) for it in itens) for k in ("com_estrela", "sem_estrela", "listadas_em_print_axioms")}
    print("   totais:", tot, "| modulos sem estrela:", sum(1 for it in itens if not it.get("com_estrela")))
for nome in ("OSeparadorNoPercurso", "LeitorDaFormula", "sonda_n0_contraexemplo", "AClausulaExemplificativa", "PolinomioDoPsiBit", "OPassoEOFim"):
    it = next(x for itens in a["registros"].values() for x in itens if x["modulo"] == nome)
    print("\n==", nome, {k: (v if not isinstance(v, list) else (len(v), v[:4])) for k, v in it.items()})
    print("   manifesto:", {k: ent[nome][k] for k in ("frente", "de_quem", "imports", "imports_de_candidatas", "namespaces", "declaracoes_theorem_lemma", "linhas_print_axioms")})
    t = (L.PEDRAS / (nome + ".lean")).read_text(encoding="utf-8")
    pr = re.findall(r"(?m)^#print axioms (\S+)", t)
    print("   #print axioms:", len(pr), pr[:4])
    print("   namespace/end/open:", re.findall(r"(?m)^(?:namespace|end|open|section)\b[^\n]*", t)[:12])
# formas gerais
formas = collections.Counter(); ns_multi = []; com_open = []
for x in m["modulos"]:
    t = (L.PEDRAS / (x["modulo"] + ".lean")).read_text(encoding="utf-8")
    pr = re.findall(r"(?m)^#print axioms (\S+)", t)
    nss = re.findall(r"(?m)^namespace\s+(\S+)", t)
    formas[(x["frente"], "com_ponto" if all("." in p for p in pr) else ("sem_ponto" if all("." not in p for p in pr) else "misto"))] += 1
    if len(set(nss)) > 1:
        ns_multi.append((x["modulo"], nss))
print("\nformas dos #print axioms por frente:", dict(formas))
print("modulos com mais de um namespace:", len(ns_multi), ns_multi[:12])
print("imports_soltos_de_candidatas:", len(m["imports_soltos_de_candidatas"]), "| ficam_fora:", m["ficam_fora"], "| ficam_para_a_v413:", str(m.get("ficam_para_a_v413"))[:300])
print("tudo_junto:", m["tudo_junto"])
print("por_autor_nas_novas:", m["por_autor_nas_novas"])
pref = collections.Counter(x["modulo"].lower() for x in m["modulos"])
print("prefixos de bandeira repetidos (modulo em minusculas):", [k for k, v in pref.items() if v > 1])

"""Conferência local da regra de contagem R6, sem importar sua implementação."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
from collections import defaultdict
import json
import re

out = Path(__file__).resolve().parent
root = out.parent.parent
stage = root / "teste_frente_a_r6" / "REV1"
work = root.parents[1]
order = Path("C:/IALD/TUNEL_CLAUDE_APP/ORDEM_018_revisao_do_que_a_gerencia_produziu_em_16nov.md")
operator_dir = work / "cunhagens_13out"
operator_files = sorted(operator_dir.glob("OPERADOR_*verbatim.txt"))
text_pool = {p: p.read_bytes() for p in operator_files}
receipt = json.loads((stage / "RESULTADO_CELULAS_R6.json").read_bytes())
G = receipt["G"]
assert G == 16

def pmf(n, k, p):
    if not 0 <= k <= n:
        return F(0)
    return comb(n, k) * p**k * (1 - p)**(n-k)

def tail(n, k, p):
    return sum(pmf(n, v, p) for v in range(k, n + 1))

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

calcs = []
def check(key, result):
    stored = receipt
    for field in key:
        stored = stored[field]
    value = float(result)
    delta = abs(value-stored)
    assert delta < 1e-12, (key, result, stored)
    calcs.append(dict(path=list(key), recalculated=value, stored=stored, distance=delta))

half = F(1, 2)
variants = {}
for k in range(9, 17):
    key = ("cortes",str(k))
    t = tail(G, k, half)
    check(key + ("um_lado_so_sorteando_(pior_caso)",), t**4)
    check(key + ("um_lado_so_sem_sortear",), 0)
    check(key + ("cada_lado_contra_a_memoria",), 0)
    check(key + ("metade_pelos_dois_lados_metade_so_a_pagina",), t**2)
    for p in ("0.99","0.95","0.90","0.85","0.80","0.75","0.70"):
        check(key+("usa_os_dois_lados_por_acerto_de_veredito",p), tail(G,k,F(p))**4)
    variants[k] = {"half_per_session_otherwise_coin":float(tail(G,k,F(3,4))**4),
                   "half_per_session_otherwise_AND_current":float(t),
                   "half_per_session_otherwise_page":float(t*t),
                   "exactly_32_of_64_use_both_random_allocation":float(sum(
                       F(comb(G,x)*comb(G,y)*comb(2*G,2*G-x-y),comb(4*G,2*G))
                       for x in range(k,G+1) for y in range(k,G+1)))}
with localcontext() as ctx:
    ctx.prec = 65
    for c in range(36,65,2):
        check(("T",str(c),"teto_de_Hoeffding_para_um_lado_so"),
              (Decimal(-2*(c-32)**2)/Decimal(64)).exp())
        for p in ("0.80","0.90"):
            check(("T",str(c),"usa_os_dois_lados_"+p.replace(".", "_")),tail(64,c,F(p)))

for e in ("0.05","0.10","0.15","0.20"):
    base = ("grupo_inteiro_9_de_16_(regra_da_R0)", "erro_"+e)
    group_q = (1-F(e))**6
    check(base+("taxa_de_grupo",),group_q)
    check(base+("julga_(X>=9)",),tail(G,9,group_q))
    check(base+("sem_rotulo_(7_ou_8)",),pmf(G,7,group_q)+pmf(G,8,group_q))
    check(base+("nao_julga_(X<=6)",),1-tail(G,7,group_q))

# Distribuição conjunta exata de número total de acertos e grupos completos,
# sob moedas independentes. Mantém a dependência entre os dois cortes.
dist = {(0,0):F(1)}
for _ in range(G):
    new = defaultdict(F)
    for (score, good), prob in dist.items():
        for x in range(5):
            new[(score+x,good+(x==4))] += prob*pmf(4,x,half)
    dist = new
assert sum(dist.values()) == 1
control = {
    "letters_guess_7_of_8":float(tail(8,7,half)),
    "letters_95_7_of_8":float(tail(8,7,F(95,100))),
    "no_index_guess_42_of_64":float(tail(64,42,half)),
    "no_index_guess_five_complete":float(tail(16,5,half**4)),
    "no_index_guess_union":float(sum(v for (h,g),v in dist.items() if h>=42 or g>=5)),
    "inversion_independent_coin_two_groups":float(tail(16,2,half**4)),
    "no_index_correct_abstention_all":0,
}
# Retira da chance de passar as quatro células os casos com pelo menos dois
# grupos inteiramente errados usando inclusão-exclusão dos grupos marcados.
for p in (half,F(7,10),F(4,5),F(9,10)):
    k = 10
    primary = tail(G,k,p)**4
    excluded = sum((-1)**(j-2)*(j-1)*comb(G,j)*(1-p)**(4*j)*tail(G-j,k,p)**4 for j in range(2,G+1))
    control["primary_with_inversion_gate_q_"+str(p)] = float(primary-excluded)

wrong = [[j == g % 4 for j in range(4)] for g in range(16)]
witness = {
    "right_by_cell":[sum(not r[j] for r in wrong) for j in range(4)],
    "all_right_groups":sum(not any(r) for r in wrong),
    "all_wrong_groups":sum(all(r) for r in wrong),
    "direct_pass":all(sum(not r[j] for r in wrong)>=10 for j in range(4)),
    "binary_score_other_thresholds":"complemento: uma certa por grupo; constantes: duas certas por grupo",
}
quotes = []
for doc in sorted(stage.glob("*.md")):
    for line_number, line in enumerate(doc.read_text(encoding="utf-8-sig").splitlines(),1):
        for quote in re.findall("«([^»]*)»",line):
            data = quote.encode("utf-8")
            hits = [{"name":p.name,"sha256":sha256(raw).hexdigest(),"byte_offset":raw.index(data),
                     "source_line":raw[:raw.index(data)].count(b"\n")+1}
                    for p,raw in text_pool.items() if data in raw]
            quotes.append({"file":doc.name,"line":line_number,"bytes":len(data),
                           "single_line":True,"sha256":sha256(data).hexdigest(),"hits":hits})
            assert len(hits) == 1
spec = order.read_text(encoding="utf-8-sig")
pinned = {}
for item in [*stage.glob("*.md"),stage/"celulas_r6.py",stage/"RESULTADO_CELULAS_R6.json",
             *sorted((root/"revisao").glob("REVISAO_16nov_R3_*.md")),
             *[p for p in operator_files if p.name in spec]]:
    h = digest(item)
    assert re.search(r'\b'+re.escape(h[:16])+r'(?:[a-f0-9]{48})?\b',spec)
    pinned[str(item)] = h
ex = {"G":G,"calculation_fields":len(calcs),"maximum_absolute_difference":max(v["distance"] for v in calcs),
      "numeric_comparison":calcs,"mechanism_variants_by_cut":variants,"controls":control,"counterexample":witness,
      "angle_quotes":quotes, "operator_source_files_checked":len(text_pool),"pinned_files":pinned}
outfile=out/"conferencia.json"
outfile.write_text(json.dumps(ex,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:ex[k] for k in ('calculation_fields','maximum_absolute_difference','controls','counterexample')},indent=1))


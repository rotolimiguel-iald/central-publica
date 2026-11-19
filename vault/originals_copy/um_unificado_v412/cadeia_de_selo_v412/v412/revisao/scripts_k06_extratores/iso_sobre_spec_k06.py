"""Teste do revisor: aplica o isomorfo.py (copia) a especificacao REAL do braco T e mede com extratores.py (copia).
Dicionario so com os tokens de sujeito/objeto do braco T (sem artigo, sem numeros)."""
import sys, json, copy
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H/"copia_extratores")); sys.path.insert(0, str(H/"copia_contaminacao"))
import extratores as E, isomorfo as I
spec = E.load_spec(H/"copia_extratores"/"especificacao.json")
T = spec["arms"]["T"]["assertions"]
terms = sorted({t for a in T for t in (a["subject"], a["object"]) if a["object"] not in ("OPEN","FORBIDDEN","NOT_TESTED","CONJECTURE")} | {a["subject"] for a in T})
terms = sorted(set(terms))
d = I.make_dictionary(terms, "REVISOR-TESTE", "r0"); d["status"] = "TESTE_SINTETICO"
specT = copy.deepcopy(spec)
spec_iso = I.transform_json_strings(specT, d)
print("termos no dicionario:", len(terms))
changed = sum(1 for a,b in zip(spec["arms"]["T"]["assertions"], spec_iso["arms"]["T"]["assertions"]) if (a["subject"],a["object"])!=(b["subject"],b["object"]))
print("asser. T cujo sujeito/objeto mudou:", changed, "de 24")
# texto original e isomorfo (sinteticos, gerados da propria spec)
def mk(sp): return "\n".join("|".join(["K06R1",a["id"],a["subject"],a["relation"],a["object"],a["status"]]) for a in sp["arms"]["T"]["assertions"])+"\n"
t0, t1 = mk(spec), mk(spec_iso)
v00 = E.extract(t0, "T", spec)["vector"]
v11 = E.extract(t1, "T", spec_iso)["vector"]
v01 = E.extract(t1, "T", spec)["vector"]   # E_TGL (spec original) lendo o texto isomorfo
v10 = E.extract(t0, "T", spec_iso)["vector"]
print("E_T(orig)  sobre orig :", sum(v00), "/24")
print("E_ISO(iso) sobre iso  :", sum(v11), "/24")
print("E_TGL(orig) sobre iso :", sum(v01), "/24  (manipulacao: deve ser baixo)")
print("E_ISO(iso) sobre orig :", sum(v10), "/24")
# quais asser. de T NAO mudam com o dicionario (porque o token e' status/relacao generico)
fixed=[a["id"] for a,b in zip(spec["arms"]["T"]["assertions"], spec_iso["arms"]["T"]["assertions"]) if (a["subject"],a["object"])==(b["subject"],b["object"])]
print("asser. sem mudanca (nada no dicionario):", fixed)

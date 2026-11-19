"""Revisao K01: (1) reexecuta validate() do Kimi SEM gravar (nao chama main); (2) compara a funcao do validador
com a tabela do PRE_REGISTRO (secao 6), transcrita aqui de forma independente em familias de rotulo;
(3) lista quais ramos de saida sao alcancaveis quando S esta AUSENTE ou so ha S nao-independente.
Somente valores sinteticos. Nenhum dado observado."""
import importlib.util
import itertools
import json
import math
import sys

KP = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K01_validar.py"
spec = importlib.util.spec_from_file_location("K01_validar_kimi", KP)
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

# (1) validate() sem gravar
try:
    res = K.validate()
    print("validate() do Kimi: OK; n_canais =", res["n_canais"], "; casos sinteticos =", res["testes_sinteticos"]["n"],
          "; resumo linhas =", res["resumo_linhas_nao_vazias"])
except Exception as e:  # noqa
    print("validate() do Kimi FALHOU:", type(e).__name__, e)

# quais saidas os 30 casos do Kimi produzem
casos = K.synthetic_cases()
saidas = sorted({c["obtido"] for c in casos})
print("\nsaidas distintas nos casos do Kimi:", len(saidas))
for s in saidas:
    print("  ", s)
print("UNDER produzido por algum caso do Kimi?", K.UNDER in saidas)
print("default d_p do validador:", K.veredito_sintetico.__defaults__)

# (2) tabela da secao 6, transcrita (familia de rotulo)
def faixa_p(r):
    return "P>=5" if r >= 5 else "P3-5" if r >= 3 else "P1-3" if r > 1 else "P<=1"

def faixa_s(r):
    return "S>=5" if r >= 5 else "S3-5" if r >= 3 else "S1-3" if r > 1 else "S<=1"

def tabela_md(rp, estado, rs):
    fp = faixa_p(rp)
    if estado == "INVALID":
        return "INCONC_S"
    if estado == "ABSENT":
        if fp == "P>=5":
            return "SINGLE_P"
        if fp == "P3-5":
            return "TENSION_P"
        return "UNDER_ARMED"
    fs = faixa_s(rs)
    if estado == "NONINDEPENDENT":
        if fp == "P>=5":
            return "BOTH_NI" if fs == "S>=5" else "SINGLE_P"
        if fp == "P3-5":
            return {"S>=5": "SINGLE_S", "S3-5": "BOTH_NI"}.get(fs, "TENSION_P")
        # P<3
        return {"S>=5": "SINGLE_S", "S3-5": "TENSION_S_NI"}.get(fs, "UNDER_ARMED")
    if estado == "INDEPENDENT":
        if fp == "P>=5":
            return "FALSIFIED" if fs == "S>=5" else "SINGLE_P"
        if fp == "P3-5":
            return {"S>=5": "SINGLE_S", "S3-5": "BOTH"}.get(fs, "TENSION_P")
        if fp == "P1-3":
            return {"S>=5": "SINGLE_S", "S3-5": "TENSION_S"}.get(fs, "UNDER_ARMED")
        # P<=1
        if fs == "S<=1":
            return "MATCHED"
        return {"S>=5": "SINGLE_S", "S3-5": "TENSION_S"}.get(fs, "UNDER_ARMED")
    raise ValueError(estado)

fam = {
    K.SINGLE_P: "SINGLE_P", K.SINGLE_S: "SINGLE_S", K.BOTH_NI: "BOTH_NI", K.T_P: "TENSION_P", K.T_S: "TENSION_S",
    K.T_S_NI: "TENSION_S_NI", K.BOTH: "BOTH", K.FALS: "FALSIFIED", K.UNDER: "UNDER_ARMED", K.ARMED: "UNDER_ARMED",
    K.MATCHED: "MATCHED", K.INC_P: "INCONC_P", K.INC_S: "INCONC_S", K.AWAIT_P: "AWAIT_P",
}
valsP = [0.0, 0.5, 1.0, 1.0001, 2.0, 2.999, 3.0, 4.0, 4.999, 5.0, 7.0]
valsS = [0.0, 0.5, 1.0, 1.0001, 2.0, 2.999, 3.0, 4.0, 4.999, 5.0, 7.0]
div = []
alc = {}
n = 0
for estado in ("ABSENT", "NONINDEPENDENT", "INDEPENDENT"):
    for rp in valsP:
        for rs in (valsS if estado != "ABSENT" else [None]):
            n += 1
            code = fam[K.veredito_sintetico(rp, estado, rs)]
            md = tabela_md(rp, estado, rs if rs is not None else 0.0)
            alc.setdefault(estado, set()).add(code)
            if code != md:
                div.append((estado, rp, rs, code, md))
print("\nGrade comparada (validador x tabela do PRE_REGISTRO secao 6, em familias): pontos =", n, "; divergencias =", len(div))
for d_ in div[:20]:
    print("  DIVERGE:", d_)
for estado, s in alc.items():
    print("saidas alcancaveis com S", estado, ":", sorted(s))
print("\nFALSIFIED so e alcancavel com S INDEPENDENT:", "FALSIFIED" in alc["INDEPENDENT"], "|", "FALSIFIED" in alc["ABSENT"], "|", "FALSIFIED" in alc["NONINDEPENDENT"])
print("MATCHED so e alcancavel com S INDEPENDENT:", "MATCHED" in alc["INDEPENDENT"], "|", "MATCHED" in alc["ABSENT"], "|", "MATCHED" in alc["NONINDEPENDENT"])
# efeito do default D=6.0
print("\nP<3 e S ausente com d_p=None ->", K.veredito_sintetico(2.0, "ABSENT", None, d_p=None), "| d_p=4 ->", K.veredito_sintetico(2.0, "ABSENT", None, d_p=4.0),
      "| d_p=default ->", K.veredito_sintetico(2.0, "ABSENT", None))

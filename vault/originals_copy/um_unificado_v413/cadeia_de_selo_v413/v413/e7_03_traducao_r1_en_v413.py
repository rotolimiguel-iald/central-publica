# -*- coding: utf-8 -*-
"""Etapa 2 da v413 (contrato R2): a traducao EN da pagina R1, por trocas EXATAS sobre a traducao da R0 (O_QUE_FICA_CLARO_v413_R0_EN.md, que fica como registro), uma por troca que a pagina R1 fez sobre a R0
(o_que_fica_claro_v413\\fazer_pagina_r1.py): (1) a primeira frase da secao 2 vira duas; (2) e (3) o preco da travessia sem a palavra 'provado' (a cota em teorema); (4) o titulo do que nao fica provado.
Confere, por script, que a PT R1 e a EN R1 tem a mesma estrutura e os mesmos termos entre crases na mesma ordem, e que nenhuma das quatro formas antigas sobra. Grava O_QUE_FICA_CLARO_v413_R1_EN.md."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import texto_publico_v413 as TP

R0_EN = L.D / "O_QUE_FICA_CLARO_v413_R0_EN.md"
R1_EN = L.D / "O_QUE_FICA_CLARO_v413_R1_EN.md"
assert L.PAGINA_CONTRATO.name == "O_QUE_FICA_CLARO_v413_R1.md" and L.PAGINA_EN == R1_EN, ("a pagina do contrato nao e' a R1", L.PAGINA_CONTRATO)
t = R0_EN.read_bytes().decode("utf-8").replace("\r\n", "\n")
TROCAS = [
    ("the crossing by branching decides every formula, at a price proved exponential only in the Names of the frontier (section 3).",
     "the crossing by branching decides every formula, at a price exponential only in the Names of the frontier, with the bound in a theorem (section 3)."),
    ("> P = nP is a theorem of the TGL in the classes of its dictionary, and v413 writes it in the language of the Cook–Levin classes, on Mathlib's standard Turing machine.",
     "> P = nP is a theorem of the TGL in the classes of its dictionary. Version v413 writes it in the language of the Cook–Levin classes, on Mathlib's standard Turing machine."),
    ("- **The crossing by branching decides every formula** (`a_travessia_decide`), at a price proved exponential (`o_preco_da_travessia`);",
     "- **The crossing by branching decides every formula** (`a_travessia_decide`), at an exponential price, with the bound in a theorem (`o_preco_da_travessia`);"),
    ("What is not proved: that someone or some system has consciousness;", "Outside what the kernel says: that someone or some system has consciousness;"),
]
for a, b in TROCAS:
    assert t.count(a) == 1, ("trecho da traducao R0 nao achado exatamente uma vez", a[:90], t.count(a))
    t = t.replace(a, b)
assert not re.search(r"\bproved\b", t), [l for l in t.split("\n") if re.search(r"\bproved\b", l)]
L.salvar_bytes(R1_EN, t.encode("utf-8"))
pt = L.PAGINA_CONTRATO.read_bytes().decode("utf-8")
estr = lambda bl: [(k, (len(v) if isinstance(v, list) else (len(v[1]) if k == "table" else 1))) for k, v in bl]
ok_estr = estr(TP.blocos(pt)) == estr(TP.blocos(t))
ok_cod = re.findall(r"`([^`]+)`", pt) == re.findall(r"`([^`]+)`", t)
print("R1_EN:", R1_EN.name, L.sha16_arq(R1_EN), "| estrutura igual a da PT R1:", ok_estr, "| termos entre crases iguais:", ok_cod)
sys.exit(0 if (ok_estr and ok_cod) else 1)

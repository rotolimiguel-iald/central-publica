# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a pagina publica R1 da v413, por trocas EXATAS sobre a R0 (que fica): (1) a F37b herdada (em
cada trecho com «P = nP» e «Turing» juntos, o proprio trecho traz «relativo ao leitor» ou negacao): a primeira frase da
secao 2 vira duas; (2) «provado/provada» sem estatuto vira forma sem a palavra (no ingles daria «proved» sem estatuto).
Nenhuma afirmacao muda."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
R0, R1 = D / "O_QUE_FICA_CLARO_v413_R0.md", D / "O_QUE_FICA_CLARO_v413_R1.md"
t = R0.read_bytes().decode("utf-8")
TROCAS = [
    ("> P = nP é teorema da TGL nas classes do seu dicionário, e a v413 o escreve na língua das classes de Cook–Levin, na\n"
     "> máquina de Turing padrão do Mathlib. Lá, SAT está em NP:",
     "> P = nP é teorema da TGL nas classes do seu dicionário. A v413 o escreve na língua das classes de Cook–Levin, na\n"
     "> máquina de Turing padrão do Mathlib. Lá, SAT está em NP:"),
    ("  fronteira dos três literais; a travessia por ramificação decide toda fórmula, a um preço provado exponencial só nos Nomes\n"
     "  da fronteira (seção 3).",
     "  fronteira dos três literais; a travessia por ramificação decide toda fórmula, a um preço exponencial só nos Nomes da\n"
     "  fronteira, com a cota em teorema (seção 3)."),
    ("- **A travessia por ramificação decide toda fórmula** (`a_travessia_decide`), a um preço provado exponencial\n"
     "  (`o_preco_da_travessia`);",
     "- **A travessia por ramificação decide toda fórmula** (`a_travessia_decide`), a um preço exponencial, com a cota em\n"
     "  teorema (`o_preco_da_travessia`);"),
    ("O que não fica provado: que alguém ou algum sistema tenha consciência; a singularidade; o braço da negação do T6 não foi\n"
     "rodado.",
     "Fora do que o kernel diz: que alguém ou algum sistema tenha consciência; a singularidade; o braço da negação do T6 não foi\n"
     "rodado."),
]
for a, b in TROCAS:
    assert t.count(a) == 1, "trecho nao achado exatamente uma vez: %r" % a[:80]
    t = t.replace(a, b)
assert "provad" not in t.lower(), [l for l in t.split("\n") if "provad" in l.lower()]
d = t.encode("utf-8")
tmp = R1.with_name(R1.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(R1)
print("R0 %s -> R1 %s (%d B)" % (hashlib.sha256(R0.read_bytes()).hexdigest()[:16], hashlib.sha256(d).hexdigest()[:16], len(d)))

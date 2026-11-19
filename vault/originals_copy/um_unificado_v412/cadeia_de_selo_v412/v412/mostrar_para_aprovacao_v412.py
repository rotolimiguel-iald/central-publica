# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: so' leitura. Imprime, da pagina vigente (R19), por extenso e sem mudar um caractere, as partes que mudaram
desde a ultima leitura do autor: o item novo da secao 1; o titulo da secao 2 e o fim do paragrafo de citacao; o bloco do leitor da
formula (o paragrafo, a primeira coluna da tabela, o fecho); e o paragrafo do Tetelestai."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
t = (Path(__file__).resolve().parent / "o_que_fica_claro_REV19" / "O_QUE_FICA_CLARO_v412_R19.md").read_bytes().decode("utf-8")
blocos = t.split("\n\n")
def um(prefixo):
    ach = [b for b in blocos if b.startswith(prefixo)]
    assert len(ach) == 1, (prefixo, len(ach)); return ach[0]
sec1 = um("## 1.") if False else None
item = [l for l in t.split("\n") if l.startswith("- **O leitor da fórmula.**")]; assert len(item) == 1
print("=== SECAO 1, ITEM NOVO\n" + item[0] + "\n")
tit2 = [l for l in t.split("\n") if l.startswith("## 2.")]; assert len(tit2) == 1
print("=== SECAO 2, TITULO\n" + tit2[0] + "\n")
cit = um("> P = nP é teorema")
i = cit.index("Contado letra por letra, o procedimento da casa custa o todo")
print("=== SECAO 2, FIM DO PARAGRAFO DE CITACAO (desde 'Contado letra por letra, o procedimento da casa')\n" + cit[i:] + "\n")
print("=== O LEITOR DA FORMULA, PARAGRAFO\n" + um("**O leitor da fórmula.** Definição da teoria") + "\n")
print("=== A NOTA ANTES DA TABELA\n" + um("Na tabela, cada linha tem a sua máquina") + "\n")
tab = um("| o que se afirma | termo | onde |")
print("=== A TABELA, PRIMEIRA COLUNA (o que se afirma)")
for l in tab.split("\n")[2:]:
    print("- " + l.strip().strip("|").split("|")[0].strip())
print("\n=== O FECHO DO BLOCO\n" + um("Cada limite acima é do leitor") + "\n")
print("=== O PARAGRAFO DO TETELESTAI\n" + um("**Tetelestai: a consumação do ciclo.**"))

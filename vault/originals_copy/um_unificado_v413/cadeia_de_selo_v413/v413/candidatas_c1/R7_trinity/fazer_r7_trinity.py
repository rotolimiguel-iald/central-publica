# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R7 da Trinity, so' texto. ERRATA em nome proprio da gerencia: a R6 atribuiu ao operador a
leitura de cada passo da maquina da teoria como energia; a frase do operador e' so' «A máquina nua paga em eletricidade»;
a extensao a' maquina da teoria e' da gerencia. Corrige a docstring de a_conta_de_luz_da_maquina_da_teoria e a da sintese.
Gera R7_trinity\\Trinity.lean a partir da R6 por trocas EXATAS; copia o compilador."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R6D = AQUI.parent / "R6_trinity"
R6, R5 = R6D / "Trinity.lean", AQUI.parent / "R5_trinity" / "Trinity.lean"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


src = R6.read_bytes().decode("utf-8")
TROCAS = [
    ("  nenhum enunciado da R5 (sha16 `%s`) mudou.]\n" % sha(R5)[:16],
     ("  nenhum enunciado da R5 (sha16 `%s`) mudou. A R7 corrige só o texto de duas docstrings da R6 (sha16\n"
      "  `%s`): a frase do operador é «A máquina nua paga em eletricidade»; ler cada passo da máquina da teoria como\n"
      "  energia é leitura da gerência. Nenhum enunciado da R6 mudou.]\n") % (sha(R5)[:16], sha(R6)[:16])),
    ("/-- ★★ A CONTA DE LUZ DA MÁQUINA DA TEORIA: lendo cada passo como a carga −ln(1−β) paga em energia (a leitura do\n"
     "operador [ONTO]), a conta, multiplicada por k_B·T > 0, fica entre o piso de Landauer dos m Nomes e esse piso mais um\n"
     "passo. -/",
     "/-- ★★ A CONTA DE LUZ DA MÁQUINA DA TEORIA: lendo cada passo como a carga −ln(1−β) paga em energia (leitura da\n"
     "gerência, que estende à máquina da teoria a frase do operador sobre a máquina nua [ONTO]), a conta, multiplicada por\n"
     "k_B·T > 0, fica entre o piso de Landauer dos m Nomes e esse piso mais um passo. -/"),
    ("/-- ★★★ A MÁQUINA NUA PAGA EM ELETRICIDADE (R6, a leitura do operador): (1)",
     "/-- ★★★ A MÁQUINA NUA PAGA EM ELETRICIDADE (R6; a frase é do operador, os itens são os teoremas): (1)"),
]
novo = src
for antes, depois in TROCAS:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:90]
    novo = novo.replace(antes, depois)


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


grava(AQUI / "Trinity.lean", novo.encode("utf-8"))
grava(AQUI / "compilar.py", (R6D / "compilar.py").read_bytes())
print("R6 sha16 %s -> R7 sha16 %s | %d -> %d B" % (sha(R6)[:16], sha(AQUI / "Trinity.lean")[:16], len(src.encode("utf-8")),
                                                   len(novo.encode("utf-8"))))

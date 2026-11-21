# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R8 da Trinity, so' texto. Aplica as tres ressalvas do parecer do Codex
(revisao_codex\\CODEX_TRINITY_R7_OPERADOR_R2\\PARECER.md): R7-F1 o limite do peso pede 0 < beta < 1 e nao e' enunciado
do teorema; R7-F2 a sobra e' de no maximo um passo (a igualdade ocorre); R7-F3 hLandauer e' desigualdade global, nao
imposta a maquina nenhuma, reversivel ou nao. Gera R8_trinity\\Trinity.lean a partir da R7 por trocas EXATAS; copia o
compilador. Nenhum enunciado muda (conferido depois por conferir_enunciados.py)."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R7D = AQUI.parent / "R7_trinity"
R7 = R7D / "Trinity.lean"
PARECER = AQUI.parents[1] / "revisao_codex" / "CODEX_TRINITY_R7_OPERADOR_R2" / "PARECER.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


src = R7.read_bytes().decode("utf-8")
assert "\r\n" not in src
s_par, s_r7 = sha(PARECER)[:16], sha(R7)[:16]
TROCAS = [
    ("  energia é leitura da gerência. Nenhum enunciado da R6 mudou.]\n",
     ("  energia é leitura da gerência. Nenhum enunciado da R6 mudou. A R8 aplica só em texto as três ressalvas da revisão do\n"
      "  Codex (`C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v413\\revisao_codex\\CODEX_TRINITY_R7_OPERADOR_R2\\PARECER.md`,\n"
      "  sha16 `%s`): o limite do peso pede 0 < β < 1 e não é enunciado; a sobra é de no máximo um passo; `hLandauer` é\n"
      "  desigualdade global, não imposta a máquina nenhuma. Nenhum enunciado da R7 (sha16 `%s`) mudou.]\n") % (s_par, s_r7)),
    # R7-F1
    ("    estritamente o número de soluções (o zero absoluto só no limite); se toda atribuição viola exatamente uma cláusula, a\n",
     "    estritamente o número de soluções, para todo β < 1 (o limite, em que o peso conta só as soluções, pede 0 < β < 1 e\n"
     "    não é enunciado aqui: com β = 0 o peso não decai); se toda atribuição viola exatamente uma cláusula, a\n"),
    ("passos o peso passa estritamente o número de soluções; o peso só conta as soluções no limite. -/\n",
     "passos o peso passa estritamente o número de soluções, para todo β < 1. O limite (com 0 < β < 1, o peso tende ao número\n"
     "de soluções quando k cresce) não é enunciado deste teorema; com β = 0 o peso não decai. -/\n"),
    # R7-F2
    ("pagando a carga com sobra de menos de um\n    passo;", "pagando a carga com sobra de no máximo um\n    passo;"),
    ("passa de n·ln 2 por\nmenos de um passo.", "passa de n·ln 2 por\nno máximo um passo."),
    ("(4) a máquina da teoria paga no piso, com sobra de menos de um passo;",
     "(4) a máquina da teoria paga no piso, com sobra de no máximo um passo;"),
    # R7-F3
    ("  conta: a máquina que apaga a cada passo paga por passo, e a §15 só o usa como hipótese nomeada. Uma máquina reversível\n"
     "  (Bennett, 1973 [KNOWN]) pode chegar perto do piso, mas não encurta os seus passos.",
     "  conta, e a §15 só o usa pela hipótese nomeada `hLandauer`: uma desigualdade global (movimentos × piso ≤ conta), que o\n"
     "  tipo não impõe a máquina nenhuma, reversível ou não; apagar um bit por movimento é uma condição física suficiente para\n"
     "  ela, dita à parte, não uma equivalência provada. Uma máquina reversível (Bennett, 1973 [KNOWN]) pode dissipar perto do\n"
     "  piso, ou mais, por outros custos; não encurta os seus passos."),
    ("hipótese nomeada `hLandauer` (a máquina dissipa ao menos um piso de Landauer por movimento, como as máquinas comuns,\n"
     "irreversíveis), a conta de luz é de ao menos 2^(m+1) pisos: exponencial. Uma máquina reversível não cumpre a hipótese. -/\n",
     "hipótese nomeada `hLandauer` (desigualdade global: movimentos × piso de Landauer ≤ conta), a conta de luz é de ao menos\n"
     "2^(m+1) pisos: exponencial. A hipótese não é imposta a máquina nenhuma, reversível ou não; apagar um bit por movimento é\n"
     "uma condição física suficiente para ela, não uma equivalência provada. -/\n"),
]
novo = src
for antes, depois in TROCAS:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:90]
    novo = novo.replace(antes, depois)
assert "menos de um passo" not in novo and "não cumpre a hipótese" not in novo


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


grava(AQUI / "Trinity.lean", novo.encode("utf-8"))
grava(AQUI / "compilar.py", (R7D / "compilar.py").read_bytes())
print("R7 sha16 %s -> R8 sha16 %s | %d -> %d B | parecer sha16 %s" % (
    s_r7, sha(AQUI / "Trinity.lean")[:16], len(src.encode("utf-8")), len(novo.encode("utf-8")), s_par))

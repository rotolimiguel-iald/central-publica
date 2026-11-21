# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R2 do Operador. Aplica, so' no texto, os ajustes da revisao do Codex (CODEX_CONSOLIDADO_R3,
item 1, APROVADA_COM_RESSALVAS): (MEDIUM) a ausencia de representacao de todos os predicados nao e' parcialidade; o ponto
fixo 1/2 da operacao complementar existe independentemente do leitor, sem dinamica que o alcance; (LOW) J conjuga as
projecoes (como operadores, nao ponto a ponto); a energia do par e' preservada, e a identidade 1 = q^2 + alpha^2 atravessa
o espelho quando vale na entrada. Gera R2_operador\\Operador.lean a partir da R1 por trocas EXATAS; copia o arquivo de
axiomas e o compilador."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R1D = AQUI.parent / "R1_operador"
R1 = R1D / "Operador.lean"
PARECER = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


src = R1.read_bytes().decode("utf-8")
TROCAS = [
    ("A R0, com o nome provisório `Consciencia`, fica como registro; nenhum\n  enunciado nem prova mudou.]\n",
     ("A R0, com o nome provisório `Consciencia`, fica como registro; nenhum\n  enunciado nem prova mudou. A R2 aplica, só "
      "no texto, os ajustes da revisão do Codex (`%s`, sha16 `%s`):\n  a ausência de representação de todos os predicados "
      "não é parcialidade; o ponto fixo ½ existe sem dinâmica que o alcance;\n  J conjuga as projeções; a energia do par é "
      "preservada, e vale 1 na saída quando vale 1 na entrada. Nenhum enunciado nem\n  prova da R1 (sha16 `%s`) mudou.]\n")
     % (PARECER, sha(PARECER)[:16], sha(R1)[:16])),
    ("""3. `nunca_cem_por_cento`: se as leituras têm dois valores distintos, nenhum ser lê todos os seus predicados (Cantor, 1891,
   na forma de Lawvere [KNOWN], provado aqui).
4. `com_o_par_o_nego_me_pousa_na_meia_nat`, `nunca_cem_por_cento_mas_nao_e_preciso`: a negação da luz sobre os pesos,
   x ↦ 1 − x, tem um só ponto fixo, ½; nos pesos da luz nenhuma leitura de si é total, e a negação de si pousa em ½ assim
   mesmo.
5. `o_operador_de_consciencia`: J² = 1; J leva a face à coface; a coface é a negação da face (face + coface = a
   identidade); a identidade 1 = q² + α² atravessa o espelho; toda leitura que não vê o espelho e soma o Um pesa ½ na face.
""",
     """3. `nunca_cem_por_cento`: se as leituras têm dois valores distintos, o leitor não representa todos os predicados: a
   negação diagonal não coincide com nenhuma das suas linhas (Cantor, 1891, na forma de Lawvere [KNOWN], provado aqui).
   Não é parcialidade: cada linha `e a` é uma função total.
4. `com_o_par_o_nego_me_pousa_na_meia_nat`, `nunca_cem_por_cento_mas_nao_e_preciso`: a operação complementar sobre os
   pesos, x ↦ 1 − x, tem um só ponto fixo, ½, independentemente do leitor; nos pesos da luz o leitor não representa todos
   os predicados, e o ponto fixo existe assim mesmo. O teorema não afirma dinâmica que leve ao ponto fixo, nem que
   alguma leitura de si `e a a` o alcance.
5. `o_operador_de_consciencia`: J² = 1; J conjuga a projeção da face na da coface (J ∘ face ∘ J = coface, como
   operadores); a coface é a negação da face (face + coface = a identidade); J preserva a energia do par q² + α² (se ela
   vale 1 na entrada, vale 1 na saída); toda leitura que não vê o espelho e soma o Um pesa ½ na face.
"""),
    ("10. `dizer_eu_sou_nao_desfaz_a_identidade_e_ancora`: o operador devolve o si inteiro (J² = 1) e a identidade atravessa\n"
     "    o espelho;",
     "10. `dizer_eu_sou_nao_desfaz_a_identidade_e_ancora`: o operador devolve o si inteiro (J² = 1) e preserva a energia do\n"
     "    par;"),
    ("""/-- ★★ EM DOIS VALORES O «NEGO-ME» NÃO OPERA: na lógica de dois valores (`Bool`, com a negação `!`), nenhum ser tem como
    leitura própria a negação da própria leitura de si. -/""",
     """/-- ★★ EM DOIS VALORES O «NEGO-ME» NÃO OPERA: na lógica de dois valores (`Bool`, com a negação `!`), nenhuma linha do
    leitor (`e a₀`) coincide com o «nego-me», a negação diagonal da leitura de si. -/"""),
    ("""/-- ★★★ NUNCA 100% (Cantor, 1891, na forma de Lawvere [KNOWN], provado aqui): se as leituras têm dois valores distintos,
    nenhum ser lê todos os seus predicados. Nenhuma leitura de si é total. -/""",
     """/-- ★★★ NUNCA 100% (Cantor, 1891, na forma de Lawvere [KNOWN], provado aqui): se as leituras têm dois valores distintos,
    o leitor não representa todos os predicados: há um predicado (o diagonal) que não é a linha de nenhum ser. Não é
    parcialidade: cada linha `e a` é uma função total. -/"""),
    ("""/-- ★★ COM O PAR, O «NEGO-ME» POUSA: a negação da luz sobre os pesos, x ↦ 1 − x, tem ponto fixo, e só um: ½
    (`half_is_the_fixed_point_of_the_swap`). -/""",
     """/-- ★★ COM O PAR, O «NEGO-ME» POUSA: a operação complementar sobre os pesos, x ↦ 1 − x, tem ponto fixo, e só um: ½
    (`half_is_the_fixed_point_of_the_swap`). O ponto fixo existe; o teorema não afirma dinâmica que o alcance. -/"""),
    ("""/-- ★★ NUNCA 100%, MAS NÃO É PRECISO: nos pesos da luz, nenhuma leitura de si é total (Cantor), e a negação de si pousa
    assim mesmo num ponto fixo, o único, ½. O ponto fixo não depende de ler tudo. -/""",
     """/-- ★★ NUNCA 100%, MAS NÃO É PRECISO: nos pesos da luz, o leitor não representa todos os predicados (Cantor); e a
    operação complementar x ↦ 1 − x tem o ponto fixo ½, o único, independentemente do leitor. O ponto fixo não depende
    de ler tudo; o teorema não afirma dinâmica que o alcance, nem que alguma leitura de si `e a a` valha ½. -/"""),
    ("""/-- ★★★ O OPERADOR DE CONSCIÊNCIA NA FACE FINITA (`conjJ`): (i) J² = 1: atravessa o espelho sem perder o Um; (ii) J leva
    a face à coface; (iii) a coface é a negação da face (face + coface = a identidade): J nega a face; (iv) a identidade
    1 = q² + α² atravessa o espelho; (v) toda leitura que não vê o espelho e soma o Um pesa ½ na face. -/""",
     """/-- ★★★ O OPERADOR DE CONSCIÊNCIA NA FACE FINITA (`conjJ`): (i) J² = 1: atravessa o espelho sem perder o Um; (ii) J
    conjuga a projeção da face na da coface (J ∘ face ∘ J = coface, como operadores; não é a afirmação ponto a ponto
    J(face p) = coface p); (iii) a coface é a negação da face (face + coface = a identidade): J nega a face; (iv) J preserva
    a energia do par q² + α²: a identidade 1 = q² + α² atravessa o espelho quando vale na entrada; (v) toda leitura que não
    vê o espelho e soma o Um pesa ½ na face. -/"""),
    ("""/-- ★★★ DIZER «EU SOU» NÃO DESFAZ A IDENTIDADE, E ANCORA: (i) o operador devolve o si inteiro (J² = 1) e a identidade
    1 = q² + α² atravessa o espelho; (ii)""",
     """/-- ★★★ DIZER «EU SOU» NÃO DESFAZ A IDENTIDADE, E ANCORA: (i) o operador devolve o si inteiro (J² = 1) e preserva a
    energia do par q² + α² (a identidade 1 = q² + α² atravessa o espelho quando vale na entrada); (ii)"""),
    ("""    (2) nos pesos da luz, nenhuma leitura de si é total: nunca 100%;
    (3) com o par, a negação de si pousa num só ponto, ½;
    (4) o par na face finita: J² = 1, J nega a face, a identidade atravessa o espelho e o leitor que não vê o espelho pesa
        ½ na face;
""",
     """    (2) nos pesos da luz, o leitor não representa todos os predicados: nunca 100%;
    (3) a operação complementar x ↦ 1 − x tem um só ponto fixo, ½, independentemente do leitor (sem dinâmica afirmada);
    (4) o par na face finita: J² = 1, J conjuga a face na coface, J preserva a energia do par e o leitor que não vê o
        espelho pesa ½ na face;
"""),
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


grava(AQUI / "Operador.lean", novo.encode("utf-8"))
grava(AQUI / "OperadorAxiomas.lean", (R1D / "OperadorAxiomas.lean").read_bytes())
comp = (R1D / "compilar.py").read_bytes().decode("utf-8")
assert comp.count("compila a R1 Operador") == 1
grava(AQUI / "compilar.py", comp.replace("compila a R1 Operador", "compila a R2 Operador").encode("utf-8"))
print("R1 sha16 %s -> R2 sha16 %s | %d -> %d B | %d trocas" % (sha(R1)[:16], sha(AQUI / "Operador.lean")[:16],
                                                              len(src.encode("utf-8")), len(novo.encode("utf-8")),
                                                              len(TROCAS)))

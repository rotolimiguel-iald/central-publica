# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R5 da Trinity. (1) Os ajustes da revisao do Codex (CODEX_CONSOLIDADO_R3, item 9): a frase
historica R0/R1; delimitar coupled/Trace, resolucao e retangulos as familias e representacoes provadas; os contadores
como majorantes; o expoente com Nomes distintos (dedup). (2) O teorema final do operador («o preço é fixar a raiz ... o
radical fixa o sentido», fala por bytes): a §14. Gera R5_trinity\\Trinity.lean a partir da R4 por trocas EXATAS."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R4 = AQUI.parent / "R4_trinity" / "Trinity.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out") / (
    "OPERADOR_20nov_o_preco_e_fixar_a_raiz_o_radical_fixa_o_sentido_o_teorema_final_e_o_parecer_do_codex_verbatim.txt")
PARECER = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert "o radical fixa o sentido" in FALA.read_text(encoding="utf-8")
src = R4.read_bytes().decode("utf-8")

TROCAS = [
    ("import APropostaDaTensao\n", "import APropostaDaTensao\nimport Mathlib.Analysis.SpecialFunctions.Pow.Real\n"),
    ("  literais), um exemplo e um item à síntese; nenhum enunciado da R0 (sha16 `519190db19c7295f`) mudou. A R2 (fala por bytes em\n",
     "  literais), um exemplo e um item à síntese; nenhum enunciado da R0 (sha16 `519190db19c7295f`) mudou, exceto a síntese\n"
     "  `a_trindade`, ampliada com o item dos dois literais. A R2 (fala por bytes em\n"),
    ("`%s`) acrescenta a §13 (a terceira lei na fronteira); nenhum enunciado da R3 (sha16 `8f5f5e07bcb54beb`) mudou.]\n"
     % sha(Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao_e_o_zero_absoluto_verbatim.txt"))[:16],
     ("`%s`) acrescenta a §13 (a terceira lei na fronteira); nenhum enunciado da R3 (sha16 `8f5f5e07bcb54beb`) mudou. A R5\n"
      "  aplica os ajustes da revisão do Codex (`%s`, sha16 `%s`) só em texto e num teorema novo\n"
      "  (Nomes distintos), e acrescenta a §14, o teorema final do operador (fala por bytes em\n"
      "  `work\\cunhagens_13out\\%s`, sha16 `%s`); nenhum enunciado da R4 (sha16 `%s`) mudou.]\n")
     % (sha(Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao_e_o_zero_absoluto_verbatim.txt"))[:16],
        PARECER, sha(PARECER)[:16], FALA.name, sha(FALA)[:16], sha(R4)[:16])),
    ("13. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`, `a_terceira_lei_na_fronteira`: as sínteses.\n",
     "13. `o_radical_pesa_meia_nat`, `a_carga_e_produto_referencial_do_radical`, `a_carga_se_manifesta_como_expoente`,\n"
     "    `o_radical_fixa_o_sentido`, `o_radical_abaixo_de_um_inverte_o_sentido`, `o_expoente_conta_meias_nats`,\n"
     "    `o_preco_e_fixar_a_raiz` (R5, o teorema final do operador): o radical √e, a radicalização da entropia de ½ nat, pesa\n"
     "    uma Meia-Nat; a carga de r^x é o expoente vezes ln r; fixado um radical r > 0, r ≠ 1, toda carga c se manifesta como\n"
     "    expoente, r^(c / ln r) = e^c; se r > 1, a carga e o expoente têm o mesmo sinal, e se r < 1 o sentido se inverte; no\n"
     "    radical √e o expoente de uma carga c é 2c (conta Meias-Nats); e o preço em estados de m Nomes é o radical √e elevado\n"
     "    à carga m·ln 2 na unidade do radical.\n"
     "14. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`, `a_terceira_lei_na_fronteira`,\n"
     "    `o_teorema_final_do_radical`: as sínteses.\n"),
    ("""* Que a máquina nua decida toda CNF em tempo polinomial. Na fronteira, decidir pede ramificar; a ramificação da casa custa
  ≥ 2^(m+1) movimentos (`MovimentosDoPlano.coupled_physical_lower`), e todo procedimento que só descobre a morte chegando à
  contradição produz uma refutação por resolução, exponencial nas fórmulas do pombal (Haken 1985 [KNOWN]).
""",
     """* Que a máquina nua decida toda CNF em tempo polinomial. Esta implementação continua, na fronteira, por ramificação. Na
  família `coupled`, o leitor por plano da casa custa ≥ 2^(m+1) movimentos para a relação `Trace`
  (`MovimentosDoPlano.coupled_physical_lower`); e as refutações por resolução das fórmulas do pombal têm tamanho
  exponencial (Haken 1985 [KNOWN]). Nenhuma dessas cotas se transfere a outro método sem uma ponte própria, com controle de
  custo.
"""),
    ("""* Que os Nomes da fronteira sejam poucos em geral. O preço da §12 é exponencial no número de Nomes que tocam as cláusulas de
  três literais; atravessar um corte de n Nomes partilhados pede 2ⁿ retângulos (`Codex.PairCut.exact_cover_iff`, no kernel),
  e um gesto que atravesse sem pagar por Nome da fronteira é a mesma pergunta do Instituto [OPEN].
""",
     """* Que os Nomes da fronteira sejam poucos em geral, nem que a lista usada seja mínima. O preço da §12 é uma cota superior,
  exponencial no comprimento da lista de Nomes que tocam as cláusulas de três literais. No kernel, para a CNF de igualdade
  entre dois blocos e a representação por retângulos separados nos dois blocos, a cobertura exata pede 2ⁿ retângulos
  (`Codex.PairCut.exact_cover_iff`); a passagem a outra representação ou algoritmo pede ponte própria. Um gesto que
  atravesse sem pagar por Nome da fronteira é a pergunta do Instituto [OPEN].
* Que o teorema final mude a moeda da máquina nua. A §14 mostra que, fixado o radical, a carga aparece como expoente; o
  preço em estados continua exponencial no número de Nomes. A leitura do operador é [ONTO]; o termo é a identidade.
"""),
    ("/-- [DEF] As fixações feitas pela travessia. -/\n",
     "/-- [DEF] Um majorante das fixações da travessia: conta os dois ramos, mesmo quando o primeiro já diz `true` (o `||` não\navalia o segundo). -/\n"),
    ("""/-- ★★ O PREÇO DA TRAVESSIA: com B = (T+1)² + 1, a travessia faz no máximo 2^k·B − B fixações, com k o combustível:
exponencial no tamanho. -/
""",
     """/-- ★★ O PREÇO DA TRAVESSIA: com B = (T+1)² + 1, o majorante das fixações é no máximo 2^k·B − B, com k o combustível:
uma cota superior exponencial no tamanho; não é cota inferior, nem custo de máquina do Mathlib. -/
"""),
    ("/-- [DEF] As fixações feitas pela travessia pelos Nomes. -/\n",
     "/-- [DEF] Um majorante das fixações da travessia pelos Nomes: conta os dois ramos de cada Nome. -/\n"),
    ("/-- ★★ O PREÇO DOS NOMES: no máximo 2^|S|·((T+1)³ + 2) fixações. -/\n",
     "/-- ★★ O PREÇO DOS NOMES: o majorante das fixações é no máximo 2^|S|·((T+1)³ + 2), com |S| o comprimento da lista\n(repetições contadas): cota superior. -/\n"),
]

SECAO = r'''/-! ## 12b. Os Nomes distintos (R5, ajuste da revisão) -/

/-- ★ OS NOMES DISTINTOS BASTAM: tirar as repetições da lista não muda quem toca a fronteira. -/
theorem os_nomes_distintos_tocam {S : List (Fin n)} {φ : CNF n} (h : Toca S φ) : Toca S.dedup φ := by
  intro C hC hC3
  obtain ⟨l, hl, hlS⟩ := h C hC hC3
  exact ⟨l, hl, List.mem_dedup.mpr hlS⟩

/-- ★★ O PREÇO DA FRONTEIRA COM NOMES DISTINTOS: a travessia pelos Nomes distintos da fronteira decide a fórmula, e o
expoente do majorante conta só Nomes distintos. -/
theorem o_preco_da_fronteira_com_nomes_distintos {φ : CNF n} (h3 : TresLiterais φ) :
    (atravessaPelos (nomesDaFronteira φ).dedup φ = true ↔ SAT φ)
    ∧ custoPelos (nomesDaFronteira φ).dedup φ + 2
        ≤ 2 ^ (nomesDaFronteira φ).dedup.length * ((tamanho φ + 1) ^ 3 + 2) :=
  ⟨a_travessia_pelos_nomes_decide _ φ h3 (os_nomes_distintos_tocam (os_nomes_da_fronteira_tocam φ).1),
   o_preco_dos_nomes _ φ⟩

/-- Nas oito cláusulas, os Nomes da fronteira são oito cópias de x₀; sem repetição, um só. -/
theorem os_nomes_distintos_das_oito : (nomesDaFronteira oito).dedup = [0] := by decide

/-! ## 14. O radical fixa o sentido (R5): o teorema final do operador -/

/-- [DEF] O RADICAL FIXADO: √e = e^(1/2), a radicalização da entropia de ½ nat. -/
noncomputable def radical : ℝ := Real.exp (1 / 2)

/-- ★ O RADICAL PESA UMA MEIA-NAT: ln √e = ½. -/
theorem o_radical_pesa_meia_nat : Real.log radical = 1 / 2 := by
  unfold radical
  exact Real.log_exp _

theorem o_radical_e_positivo : 0 < radical := by
  unfold radical
  exact Real.exp_pos _

theorem o_radical_passa_de_um : 1 < radical := by
  unfold radical
  have h := Real.exp_lt_exp.mpr (show (0 : ℝ) < 1 / 2 by norm_num)
  rwa [Real.exp_zero] at h

/-- ★★ O EXPOENTE DA CARGA É PRODUTO REFERENCIAL DO RADICAL: a carga (em nats) de r^x é o expoente vezes a carga do
radical, ln(r^x) = x·ln r. -/
theorem a_carga_e_produto_referencial_do_radical {r : ℝ} (hr : 0 < r) (x : ℝ) :
    Real.log (r ^ x) = x * Real.log r :=
  Real.log_rpow hr x

/-- ★★ A CARGA SE MANIFESTA COMO EXPOENTE DO RADICAL FIXADO: para todo radical r > 0, r ≠ 1, e toda carga c (em nats),
r^(c / ln r) = e^c. O expoente é a carga medida na unidade do radical. -/
theorem a_carga_se_manifesta_como_expoente {r : ℝ} (hr : 0 < r) (hr1 : r ≠ 1) (c : ℝ) :
    r ^ (c / Real.log r) = Real.exp c := by
  have hl : Real.log r ≠ 0 := Real.log_ne_zero_of_pos_of_ne_one hr hr1
  rw [Real.rpow_def_of_pos hr]
  congr 1
  field_simp

/-- ★★ O RADICAL FIXA O SENTIDO: se o radical passa de 1, a carga e o seu expoente têm o mesmo sinal. -/
theorem o_radical_fixa_o_sentido {r : ℝ} (hr : 1 < r) (c : ℝ) : (0 < c ↔ 0 < c / Real.log r) :=
  (div_pos_iff_of_pos_right (Real.log_pos hr)).symm

/-- ★ O OUTRO LADO DO UM: se o radical fica abaixo de 1, o sentido se inverte: carga positiva, expoente negativo. -/
theorem o_radical_abaixo_de_um_inverte_o_sentido {r : ℝ} (h0 : 0 < r) (h1 : r < 1) (c : ℝ) :
    (0 < c ↔ c / Real.log r < 0) := by
  have hl : Real.log r < 0 := Real.log_neg h0 h1
  constructor
  · intro hc
    exact div_neg_of_pos_of_neg hc hl
  · intro h
    by_contra hc
    have h' : 0 ≤ c / Real.log r := div_nonneg_of_nonpos (not_lt.mp hc) hl.le
    linarith

/-- ★ O EXPOENTE CONTA MEIAS-NATS: no radical √e, o expoente de uma carga c é 2c. -/
theorem o_expoente_conta_meias_nats (c : ℝ) : c / Real.log radical = 2 * c := by
  rw [o_radical_pesa_meia_nat]
  ring

/-- ★★★ O PREÇO É FIXAR A RAIZ (o teorema final, do operador): o preço em estados de m Nomes é o radical fixado √e
elevado à carga m·ln 2 na unidade do radical: 2^m = (√e)^((m·ln 2)/(ln √e)), com ln √e = ½. -/
theorem o_preco_e_fixar_a_raiz (m : ℕ) : (2 : ℝ) ^ m = radical ^ ((m * Real.log 2) / Real.log radical) := by
  rw [a_carga_se_manifesta_como_expoente o_radical_e_positivo o_radical_passa_de_um.ne']
  exact o_preco_em_estados_e_a_exponencial_da_carga m

/-- ★★★ O TEOREMA FINAL DO RADICAL (R5): o radical √e pesa uma Meia-Nat; a carga de toda potência do radical é o
expoente vezes ½; fixado o radical, toda carga se manifesta como o seu expoente; o radical, passando de 1, fixa o
sentido; o expoente conta Meias-Nats; e o preço em estados de m Nomes é o radical elevado à carga m·ln 2. -/
theorem o_teorema_final_do_radical :
    Real.log radical = 1 / 2
    ∧ (∀ x : ℝ, Real.log (radical ^ x) = x * (1 / 2))
    ∧ (∀ c : ℝ, radical ^ (c / Real.log radical) = Real.exp c)
    ∧ (∀ c : ℝ, 0 < c ↔ 0 < c / Real.log radical)
    ∧ (∀ c : ℝ, c / Real.log radical = 2 * c)
    ∧ (∀ m : ℕ, (2 : ℝ) ^ m = radical ^ ((m * Real.log 2) / Real.log radical)) :=
  ⟨o_radical_pesa_meia_nat,
   fun x => (by rw [a_carga_e_produto_referencial_do_radical o_radical_e_positivo, o_radical_pesa_meia_nat]),
   fun c => a_carga_se_manifesta_como_expoente o_radical_e_positivo o_radical_passa_de_um.ne' c,
   fun c => o_radical_fixa_o_sentido o_radical_passa_de_um c,
   o_expoente_conta_meias_nats,
   o_preco_e_fixar_a_raiz⟩

'''

FIM = "end TGLExt.Trinity\n"
AX_ANCORA = "#print axioms TGLExt.Trinity.a_terceira_lei_na_fronteira\n"
AX_NOVOS = """#print axioms TGLExt.Trinity.os_nomes_distintos_tocam
#print axioms TGLExt.Trinity.o_preco_da_fronteira_com_nomes_distintos
#print axioms TGLExt.Trinity.os_nomes_distintos_das_oito
#print axioms TGLExt.Trinity.o_radical_pesa_meia_nat
#print axioms TGLExt.Trinity.o_radical_e_positivo
#print axioms TGLExt.Trinity.o_radical_passa_de_um
#print axioms TGLExt.Trinity.a_carga_e_produto_referencial_do_radical
#print axioms TGLExt.Trinity.a_carga_se_manifesta_como_expoente
#print axioms TGLExt.Trinity.o_radical_fixa_o_sentido
#print axioms TGLExt.Trinity.o_radical_abaixo_de_um_inverte_o_sentido
#print axioms TGLExt.Trinity.o_expoente_conta_meias_nats
#print axioms TGLExt.Trinity.o_preco_e_fixar_a_raiz
#print axioms TGLExt.Trinity.o_teorema_final_do_radical
"""

novo = src
for antes, depois in TROCAS + [(FIM, SECAO + FIM), (AX_ANCORA, AX_ANCORA + AX_NOVOS)]:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:80]
    novo = novo.replace(antes, depois)
dest = AQUI / "Trinity.lean"
dados = novo.encode("utf-8")
tmp = AQUI / "Trinity.lean.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("R4 sha16 %s -> R5 sha16 %s | %d -> %d B | fala sha16 %s" % (sha(R4)[:16], sha(dest)[:16], len(src.encode("utf-8")),
                                                                   len(dados), sha(FALA)[:16]))

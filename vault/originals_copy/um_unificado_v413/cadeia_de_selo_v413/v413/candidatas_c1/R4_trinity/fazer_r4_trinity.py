# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R4 da Trinity (o operador: «atravessar a fronteira sem pagar o nome é violar a terceira lei
de nernst, porque a única solução é o zero absoluto», fala por bytes). Gera R4_trinity\\Trinity.lean a partir da R3 por
trocas EXATAS: o cabecalho, a leitura da terceira lei, a lista do que se prova, um item em 'o que nao prova', a secao 13
(a terceira lei na fronteira) antes do fim do namespace, e os #print axioms novos. Nenhum enunciado da R3 muda."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R3 = AQUI.parent / "R3_trinity" / "Trinity.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out") / (
    "OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao_e_o_zero"
    "_absoluto_verbatim.txt")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert "violar a terceira lei de nernst" in FALA.read_text(encoding="utf-8")
src = R3.read_bytes().decode("utf-8")

CAB_ANT = "  fronteira); nenhum enunciado da R2 (sha16 `97e78d6417e84091`) mudou.]\n"
CAB_NOV = ("  fronteira); nenhum enunciado da R2 (sha16 `97e78d6417e84091`) mudou. A R4 (fala por bytes em\n"
           "  `work\\cunhagens_13out\\%s`, sha16\n"
           "  `%s`) acrescenta a §13 (a terceira lei na fronteira); nenhum enunciado da R3 (sha16 `%s`) mudou.]\n") % (
    FALA.name, sha(FALA)[:16], sha(R3)[:16])

LEIT_ANT = "(`a_inclinacao_para_so_na_fronteira`, `na_fronteira_todo_lado_corta_uma_de_tres`).\n"
LEIT_NOV = """(`a_inclinacao_para_so_na_fronteira`, `na_fronteira_todo_lado_corta_uma_de_tres`).

## A terceira lei (do operador, 20/11/2026, [INPUT/ONTO])

«atravessar a fronteira sem pagar o nome é violar a terceira lei de nernst, porque a única solução é o zero absoluto». O
termo que a pedra dá a essa leitura, na máquina da teoria (o fator 1 − β): a solução é o custo zero
(`AContagemEACarga.sat_e_existir_custo_zero`); em passos finitos o zero absoluto não se alcança
(`o_zero_absoluto_nao_se_alcanca`); e a leitura só acerta depois de pagar a carga, ln 2 por Nome, de modo exato no patamar
plano (`no_patamar_plano_a_carga_e_exata`). O preço em estados da máquina nua, 2 por Nome, é a exponencial dessa carga
(`o_preco_em_estados_e_a_exponencial_da_carga`).
"""

LISTA_ANT = "12. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`: as sínteses.\n"
LISTA_NOV = """12. `o_zero_absoluto_nao_se_alcanca`, `no_patamar_plano_a_carga_e_exata`, `as_oito_pedem_a_carga`,
    `o_preco_em_estados_e_a_exponencial_da_carga` (R4): em passos finitos, se há atribuição que não é solução, o peso passa
    estritamente o número de soluções (o zero absoluto só no limite); se toda atribuição viola exatamente uma cláusula, a
    leitura diz sim (erra) enquanto o pagamento k·(−ln(1−β)) não passa a carga n·ln 2, e acerta depois; nas oito cláusulas a
    carga é 3·ln 2; e 2^m = e^(m·ln 2).
13. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`, `a_terceira_lei_na_fronteira`: as sínteses.
"""

NAO_ANT = """* Que os Nomes da fronteira sejam poucos em geral."""
NAO_NOV = """* Que a máquina nua tenha de pagar a carga em estados. A lei da §13 diz que a carga tem de ser paga (na teoria, em
  tempo: k·(−ln(1−β)) passa n·ln 2); não diz em que moeda a máquina nua paga. Pagar em tempo polinomial, e não em estados,
  é a pergunta do Instituto [OPEN]. A identificação da travessia sem pagamento com a violação da terceira lei é leitura do
  operador [ONTO]; o princípio de inalcançabilidade (Nernst, 1912) e o custo de apagar um bit (Landauer, 1961) são
  [KNOWN]; tratar a dureza de NP como princípio físico é uma proposta conhecida (Aaronson, 2005) [KNOWN como proposta],
  não um teorema.
* Que os Nomes da fronteira sejam poucos em geral."""

SECAO = r'''/-! ## 13. A terceira lei na fronteira (R4) -/

/-- [DEF] O PESO DA FÓRMULA depois de `k` passos do fator 1 − β: cada atribuição pesa (1 − β)^(k·custo). -/
noncomputable def peso (β : ℝ) (k : ℕ) (φ : CNF n) : ℝ := ∑ x : Fin n → Bool, (1 - β) ^ (k * custoCNF φ x)

/-- [DEF] O número de soluções: as atribuições de custo zero. -/
def solucoes (φ : CNF n) : ℕ := (Finset.univ.filter fun x : Fin n → Bool => custoCNF φ x = 0).card

/-- ★★ O ZERO ABSOLUTO NÃO SE ALCANÇA EM PASSOS FINITOS: se alguma atribuição não é solução, em todo número finito de
passos o peso passa estritamente o número de soluções; o peso só conta as soluções no limite. -/
theorem o_zero_absoluto_nao_se_alcanca {β : ℝ} (h1 : β < 1) (k : ℕ) {φ : CNF n}
    (h : ∃ x, custoCNF φ x ≠ 0) : (solucoes φ : ℝ) < peso β k φ := by
  obtain ⟨x0, hx0⟩ := h
  have hpos : 0 < 1 - β := by linarith
  unfold peso solucoes
  rw [← Finset.sum_filter_add_sum_filter_not Finset.univ (fun x => custoCNF φ x = 0)]
  have hsol : ∑ x ∈ Finset.univ.filter (fun x => custoCNF φ x = 0), (1 - β) ^ (k * custoCNF φ x)
      = ((Finset.univ.filter fun x : Fin n → Bool => custoCNF φ x = 0).card : ℝ) := by
    rw [Finset.card_eq_sum_ones, Nat.cast_sum, Nat.cast_one]
    refine Finset.sum_congr rfl (fun x hx => ?_)
    rw [(Finset.mem_filter.mp hx).2, Nat.mul_zero, pow_zero]
  have hres : 0 < ∑ x ∈ Finset.univ.filter (fun x => ¬ custoCNF φ x = 0), (1 - β) ^ (k * custoCNF φ x) := by
    apply Finset.sum_pos
    · intro x _
      exact pow_pos hpos _
    · exact ⟨x0, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hx0⟩⟩
  rw [hsol]
  linarith

/-- ★★★ NO PATAMAR PLANO A CARGA É EXATA: se toda atribuição viola exatamente uma cláusula (fórmula sem solução, todos os
estados no mesmo patamar), a leitura de β diz sim, e erra, enquanto o pagamento k·(−ln(1−β)) não passa a carga n·ln 2; e
acerta depois. Cada Nome custa ln 2; quem não paga, erra. -/
theorem no_patamar_plano_a_carga_e_exata {β : ℝ} (h1 : β < 1) (k : ℕ) {φ : CNF n}
    (hφ : ∀ x, custoCNF φ x = 1) :
    (1 ≤ peso β k φ ↔ (k : ℝ) * (-Real.log (1 - β)) ≤ (n : ℝ) * Real.log 2) := by
  have hpos : 0 < 1 - β := by linarith
  have hsum : peso β k φ = (2 : ℝ) ^ n * (1 - β) ^ k := by
    unfold peso
    simp only [hφ, Nat.mul_one]
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fun, Fintype.card_bool, Fintype.card_fin, nsmul_eq_mul]
    push_cast
    ring
  rw [hsum]
  have e1 : (1 - β) ^ k = Real.exp (k * Real.log (1 - β)) := by
    rw [Real.exp_nat_mul, Real.exp_log hpos]
  have e2 : (2 : ℝ) ^ n = Real.exp (n * Real.log 2) := by
    rw [Real.exp_nat_mul, Real.exp_log (by norm_num)]
  rw [e1, e2, ← Real.exp_add]
  constructor
  · intro h
    have hnn : 0 ≤ (n : ℝ) * Real.log 2 + k * Real.log (1 - β) := by
      by_contra hneg
      have hlt : (n : ℝ) * Real.log 2 + k * Real.log (1 - β) < 0 := not_le.mp hneg
      have := Real.exp_lt_exp.mpr hlt
      rw [Real.exp_zero] at this
      linarith
    linarith
  · intro h
    have hnn : (0 : ℝ) ≤ n * Real.log 2 + k * Real.log (1 - β) := by linarith
    calc (1 : ℝ) = Real.exp 0 := Real.exp_zero.symm
      _ ≤ Real.exp (n * Real.log 2 + k * Real.log (1 - β)) := Real.exp_le_exp.mpr hnn

/-- Nas oito cláusulas, toda atribuição viola exatamente uma cláusula: o patamar plano. -/
theorem oito_patamar_plano : ∀ x : Fin 3 → Bool, custoCNF oito x = 1 := by
  intro x
  cases h0 : x 0 <;> cases h1 : x 1 <;> cases h2 : x 2 <;>
    simp [custoCNF, oito, satisfeita, Literal.vale, h0, h1, h2]

/-- ★ AS OITO PEDEM A CARGA: nas oito cláusulas, a leitura de β erra enquanto o pagamento não passa 3·ln 2 (três Nomes). -/
theorem as_oito_pedem_a_carga {β : ℝ} (h1 : β < 1) (k : ℕ) :
    (1 ≤ peso β k oito ↔ (k : ℝ) * (-Real.log (1 - β)) ≤ ((3 : ℕ) : ℝ) * Real.log 2) :=
  no_patamar_plano_a_carga_e_exata h1 k oito_patamar_plano

/-- ★ AS DUAS MOEDAS: o preço em estados de m Nomes, 2^m, é a exponencial da carga m·ln 2. -/
theorem o_preco_em_estados_e_a_exponencial_da_carga (m : ℕ) : (2 : ℝ) ^ m = Real.exp (m * Real.log 2) := by
  rw [Real.exp_nat_mul, Real.exp_log (by norm_num)]

/-- ★★★ A TERCEIRA LEI NA FRONTEIRA (R4): (1) em passos finitos o zero absoluto não se alcança; (2) no patamar plano a
carga é exata: a leitura acerta se, e só se, o pagamento passa n·ln 2; (3) o preço em estados de m Nomes é a exponencial
da carga m·ln 2. -/
theorem a_terceira_lei_na_fronteira {β : ℝ} (h1 : β < 1) :
    (∀ (k : ℕ) (φ : CNF n), (∃ x, custoCNF φ x ≠ 0) → (solucoes φ : ℝ) < peso β k φ)
    ∧ (∀ (k : ℕ) (φ : CNF n), (∀ x, custoCNF φ x = 1) →
        (1 ≤ peso β k φ ↔ (k : ℝ) * (-Real.log (1 - β)) ≤ (n : ℝ) * Real.log 2))
    ∧ (∀ m : ℕ, (2 : ℝ) ^ m = Real.exp (m * Real.log 2)) :=
  ⟨fun k _ h => o_zero_absoluto_nao_se_alcanca h1 k h, fun k _ hφ => no_patamar_plano_a_carga_e_exata h1 k hφ,
   o_preco_em_estados_e_a_exponencial_da_carga⟩

'''

FIM = "end TGLExt.Trinity\n"
AX_ANCORA = "#print axioms TGLExt.Trinity.a_trindade_dos_nomes\n"
AX_NOVOS = """#print axioms TGLExt.Trinity.o_zero_absoluto_nao_se_alcanca
#print axioms TGLExt.Trinity.no_patamar_plano_a_carga_e_exata
#print axioms TGLExt.Trinity.oito_patamar_plano
#print axioms TGLExt.Trinity.as_oito_pedem_a_carga
#print axioms TGLExt.Trinity.o_preco_em_estados_e_a_exponencial_da_carga
#print axioms TGLExt.Trinity.a_terceira_lei_na_fronteira
"""

novo = src
for antes, depois in [(CAB_ANT, CAB_NOV), (LEIT_ANT, LEIT_NOV), (LISTA_ANT, LISTA_NOV), (NAO_ANT, NAO_NOV),
                      (FIM, SECAO + FIM), (AX_ANCORA, AX_ANCORA + AX_NOVOS)]:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:70]
    novo = novo.replace(antes, depois)
dest = AQUI / "Trinity.lean"
dados = novo.encode("utf-8")
tmp = AQUI / "Trinity.lean.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("R3 sha16 %s -> R4 sha16 %s | %d -> %d B | fala sha16 %s" % (sha(R3)[:16], sha(dest)[:16], len(src.encode("utf-8")),
                                                                   len(dados), sha(FALA)[:16]))

import OLeitorEALei
import Mathlib.RingTheory.Ideal.Prime

set_option autoImplicit false

/-!
# O verdadeiro é divisível, o falso não é: o valor de uma fórmula é o produto dos valores das cláusulas
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor]

## De onde vem

Em 16/11/2026, depois de a gerência dizer que faltava um teorema sobre a própria máquina de fita, o operador disse: «eu acho que tenho o teorema, o verdadeiro é divisível, o falso não é, vai dar erro, ele é primo» (por bytes em
`Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_16nov_eu_acho_que_tenho_o_teorema_o_verdadeiro_e_divisivel`). Pela regra de 04/11 a frase se prova no kernel
ou se poda. Este arquivo prova a leitura que a GERÊNCIA faz dela nos valores de verdade (`truthValue` do kernel, pela
candidata `OLeitorEALei`). Se o operador quis dizer outra coisa com “divisível” e com “primo”, este arquivo não a
cobre; a pergunta foi feita a ele.

## A leitura da gerência

O valor de uma fórmula numa configuração é o PRODUTO dos valores da lei nas cláusulas. VERDADEIRO é o 1, FALSO é o 0.
“Divisível”: o 1 se reparte em fatores que são todos 1, e divide tudo. “Não é divisível, vai dar erro”: o 0 não
divide o 1; não existe número que, multiplicado pelo FALSO, devolva o VERDADEIRO. “É primo”: nos inteiros um produto
só é 0 se algum fator é 0 (o ideal do zero é primo): uma cláusula falsa não se compensa com as outras.

## O que fica provado

1. ★ `o_verdadeiro_e_divisivel`: o valor da fórmula é VERDADEIRO se e somente se toda cláusula dá VERDADEIRO.
2. ★ `o_falso_e_primo`: o valor da fórmula é FALSO se e somente se alguma cláusula dá FALSO; e
   `o_ideal_do_falso_e_primo`: o ideal do zero é primo nos inteiros.
3. `o_valor_da_formula_e_zero_ou_um`: não há terceiro valor.
4. ★ `o_verdadeiro_divide_e_o_falso_nao`: o valor da fórmula divide o 1 se e somente se é VERDADEIRO; se é FALSO, não
   existe inteiro que multiplicado por ele dê 1.
5. ★ `o_numero_de_solucoes_e_a_soma_dos_valores`: o número de soluções é a soma, sobre as configurações, do valor da
   fórmula.
6. ★ `a_formula_verdadeira_e_divisivel`: a fórmula é satisfazível se e somente se essa soma é diferente de zero, isto
   é, se e somente se se pode dividir por ela (nos racionais). Sem solução a soma é o FALSO, e não há como dividir.

## O que NÃO se afirma

* Nada sobre os movimentos de uma máquina de fita. O item 6 CARACTERIZA a fórmula verdadeira; não diz quantos
  movimentos custa obter a soma, que percorre todas as configurações. A lacuna dita ao operador em 16/11 não se fecha
  com este arquivo.
* Que exista um número que a máquina de fita escreva depressa a partir da fórmula e que seja divisível exatamente
  quando a fórmula é verdadeira. Se o operador tem esse número, é ele o teorema; aqui não está.
* “Primo” aqui é a primalidade do zero nos inteiros (produto nulo exige fator nulo), não a de um número primo.
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OVerdadeiroEDivisivel

open TGLExt TGLExt.TraducaoTuring TGLExt.EquationOfTruth TGLExt.OLeitorEALei

variable {n : ℕ}

/-- [DEF] **O VALOR DA FÓRMULA** numa configuração: o produto, cláusula a cláusula, do valor da lei. -/
def valorDaFormula (φ : CNF n) (x : Fin n → Bool) : ℤ := (φ.map (fun C => leiNaClausula C x)).prod

/-- O valor da lei numa cláusula é FALSO (0) ou VERDADEIRO (1). -/
theorem a_lei_da_zero_ou_um (C : Clausula n) (x : Fin n → Bool) :
    leiNaClausula C x = 0 ∨ leiNaClausula C x = 1 := by
  cases h : satisfeita C x
  · exact Or.inl ((a_lei_na_clausula C x).2.mpr h)
  · exact Or.inr ((a_lei_na_clausula C x).1.mpr h)

/-- ★ **O FALSO É PRIMO**: o valor da fórmula é FALSO se e somente se alguma cláusula dá FALSO. -/
theorem o_falso_e_primo (φ : CNF n) (x : Fin n → Bool) :
    valorDaFormula φ x = 0 ↔ ∃ C ∈ φ, leiNaClausula C x = 0 := by
  unfold valorDaFormula
  rw [List.prod_eq_zero_iff, List.mem_map]

/-- O ideal do FALSO é primo nos inteiros: um produto só é zero se algum fator é zero. -/
theorem o_ideal_do_falso_e_primo : (⊥ : Ideal ℤ).IsPrime := Ideal.isPrime_bot

/-- ★ **O VERDADEIRO É DIVISÍVEL**: o valor da fórmula é VERDADEIRO se e somente se toda cláusula dá VERDADEIRO. O 1 se
reparte em uns. -/
theorem o_verdadeiro_e_divisivel (φ : CNF n) (x : Fin n → Bool) :
    valorDaFormula φ x = 1 ↔ ∀ C ∈ φ, leiNaClausula C x = 1 := by
  induction φ with
  | nil => simp [valorDaFormula]
  | cons C φ ih =>
    unfold valorDaFormula at ih ⊢
    rw [List.map_cons, List.prod_cons]
    rcases a_lei_da_zero_ou_um C x with h0 | h1
    · rw [h0, zero_mul]
      constructor
      · intro h
        exact absurd h (by norm_num)
      · intro h
        have h2 := h C (List.mem_cons.mpr (Or.inl rfl))
        rw [h0] at h2
        exact absurd h2 (by norm_num)
    · rw [h1, one_mul, ih]
      constructor
      · intro h D hD
        rcases List.mem_cons.mp hD with rfl | hD'
        · exact h1
        · exact h D hD'
      · intro h D hD
        exact h D (List.mem_cons.mpr (Or.inr hD))

/-- O valor da fórmula é FALSO ou VERDADEIRO: não há terceiro valor. -/
theorem o_valor_da_formula_e_zero_ou_um (φ : CNF n) (x : Fin n → Bool) :
    valorDaFormula φ x = 0 ∨ valorDaFormula φ x = 1 := by
  by_cases h : ∀ C ∈ φ, leiNaClausula C x = 1
  · exact Or.inr ((o_verdadeiro_e_divisivel φ x).mpr h)
  · left
    rw [o_falso_e_primo]
    by_contra hne
    apply h
    intro C hC
    rcases a_lei_da_zero_ou_um C x with h0 | h1
    · exact absurd ⟨C, hC, h0⟩ hne
    · exact h1

/-- ★ **O VERDADEIRO DIVIDE, O FALSO NÃO.** O valor da fórmula divide o 1 se e somente se é VERDADEIRO; se é FALSO, não
existe inteiro que multiplicado por ele dê 1. -/
theorem o_verdadeiro_divide_e_o_falso_nao (φ : CNF n) (x : Fin n → Bool) :
    (valorDaFormula φ x ∣ 1 ↔ valorDaFormula φ x = 1)
    ∧ (valorDaFormula φ x = 0 → ¬ ∃ y : ℤ, valorDaFormula φ x * y = 1) := by
  constructor
  · rcases o_valor_da_formula_e_zero_ou_um φ x with h0 | h1
    · rw [h0]
      constructor
      · intro h
        exact absurd (zero_dvd_iff.mp h) one_ne_zero
      · intro h
        exact absurd h (by norm_num)
    · rw [h1]
      simp
  · rintro h0 ⟨y, hy⟩
    rw [h0, zero_mul] at hy
    exact zero_ne_one hy

/-- ★ **O NÚMERO DE SOLUÇÕES É A SOMA DOS VALORES** da fórmula sobre as configurações. -/
theorem o_numero_de_solucoes_e_a_soma_dos_valores (φ : CNF n) :
    ((Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card : ℤ) = ∑ x, valorDaFormula φ x := by
  rw [Finset.card_filter]
  push_cast
  refine Finset.sum_congr rfl fun x _ => ?_
  by_cases h : custoCNF φ x = 0
  · rw [if_pos h]
    exact ((o_verdadeiro_e_divisivel φ x).mpr ((o_nome_e_onde_a_lei_da_verdadeiro φ x).mp h)).symm
  · rw [if_neg h]
    rcases o_valor_da_formula_e_zero_ou_um φ x with h0 | h1
    · exact h0.symm
    · exact absurd ((o_nome_e_onde_a_lei_da_verdadeiro φ x).mpr ((o_verdadeiro_e_divisivel φ x).mp h1)) h

/-- ★ **A FÓRMULA VERDADEIRA É DIVISÍVEL, A FALSA NÃO**: a fórmula é satisfazível se e somente se a soma dos valores é
diferente de zero, isto é, se e somente se se pode dividir por ela nos racionais. -/
theorem a_formula_verdadeira_e_divisivel (φ : CNF n) :
    (SAT φ ↔ ∑ x, valorDaFormula φ x ≠ 0) ∧ (SAT φ ↔ IsUnit ((∑ x, valorDaFormula φ x : ℤ) : ℚ)) := by
  have h1 : SAT φ ↔ ∑ x, valorDaFormula φ x ≠ 0 := by
    rw [← o_numero_de_solucoes_e_a_soma_dos_valores, sat_e_existir_onde_a_lei_da_verdadeiro]
    constructor
    · rintro ⟨x, hx⟩
      have hx0 : custoCNF φ x = 0 := (o_nome_e_onde_a_lei_da_verdadeiro φ x).mpr hx
      have hmem : x ∈ Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0) := by simp [hx0]
      have hpos : 0 < (Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card :=
        Finset.card_pos.mpr ⟨x, hmem⟩
      exact_mod_cast hpos.ne'
    · intro h
      have hne : (Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card ≠ 0 := by exact_mod_cast h
      obtain ⟨x, hx⟩ := Finset.card_pos.mp (Nat.pos_of_ne_zero hne)
      exact ⟨x, (o_nome_e_onde_a_lei_da_verdadeiro φ x).mp (by simpa using hx)⟩
  refine ⟨h1, ?_⟩
  rw [h1, isUnit_iff_ne_zero]
  exact Int.cast_ne_zero.symm

end TGLExt.OVerdadeiroEDivisivel

#print axioms TGLExt.OVerdadeiroEDivisivel.a_lei_da_zero_ou_um
#print axioms TGLExt.OVerdadeiroEDivisivel.o_falso_e_primo
#print axioms TGLExt.OVerdadeiroEDivisivel.o_ideal_do_falso_e_primo
#print axioms TGLExt.OVerdadeiroEDivisivel.o_verdadeiro_e_divisivel
#print axioms TGLExt.OVerdadeiroEDivisivel.o_valor_da_formula_e_zero_ou_um
#print axioms TGLExt.OVerdadeiroEDivisivel.o_verdadeiro_divide_e_o_falso_nao
#print axioms TGLExt.OVerdadeiroEDivisivel.o_numero_de_solucoes_e_a_soma_dos_valores
#print axioms TGLExt.OVerdadeiroEDivisivel.a_formula_verdadeira_e_divisivel

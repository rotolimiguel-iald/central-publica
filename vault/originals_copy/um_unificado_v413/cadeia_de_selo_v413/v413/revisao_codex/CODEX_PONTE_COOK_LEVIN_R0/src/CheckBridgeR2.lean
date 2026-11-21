import PonteCookLevin

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace CodexReview.Ponte
open TGLExt TGLExt.PonteCookLevin TGLExt.APonteAoTM2

-- Caracterização exata: fechamento por redução many-one, sem usar CookLevin.
theorem one_read_iff_reduces {L : ImportedSQ.LightOneParticle}
    (C : ImportedSQ.FockCertificate L) (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) {α Γ : Type}
    (ea : α → List Γ) (A : α → Prop) :
    EmPComUmaLeitura C c m ea A ↔ ReduzASAT ea A := by
  constructor
  · rintro ⟨g, hg, hA⟩
    refine ⟨g, hg, fun a => ?_⟩
    rw [hA a, o_oraculo_le_a_fita]
    exact uma_leitura_decide_SATcru C c m hm (g a)
  · rintro ⟨g, hg, hA⟩
    refine ⟨g, hg, fun a => ?_⟩
    rw [hA a, o_oraculo_le_a_fita]
    exact (uma_leitura_decide_SATcru C c m hm (g a)).symm

-- A codificação crua distingue fórmulas; não é uma saída vazia existencial.
theorem formula_encoding_injective : Function.Injective codificaFormula := by
  intro a b h
  have he : codificaEntrada (a, []) = codificaEntrada (b, []) := by
    simp only [codificaEntrada, h]
  exact congrArg Prod.fst (codificaEntrada_injetiva he)

-- A finitude omitida como parâmetro externo já vem da máquina testemunha.
theorem np_input_alphabet_finite {α Γ : Type} (ea : α → List Γ)
    (sep : Γ) (bit : Bool → Γ) (A : α → Prop) (h : EmNP ea sep bit A) :
    Finite Γ := by
  obtain ⟨V, p, ⟨M⟩, _⟩ := h
  letI : Fintype (M.tm.Γ M.tm.k₀) := M.tm.Γk₀Fin
  exact Finite.of_equiv (M.tm.Γ M.tm.k₀) M.inputAlphabet

-- A métrica inclui o índice unário: um literal de índice i ocupa i+3 símbolos.
theorem unary_name_cost (i : ℕ) : nomesDaFita [[(i, true)]] = i + 3 := by
  simp [nomesDaFita, o_comprimento_da_fita_da_formula]

theorem empty_formula_sat : SATcru [] := by
  exact ⟨fun _ => false, by simp⟩

theorem empty_clause_unsat : ¬ SATcru [[]] := by
  rintro ⟨x, hx⟩
  simpa using hx [] (by simp)

-- O oráculo distingue efetivamente entradas de decisões opostas.
theorem answers_separate {L : ImportedSQ.LightOneParticle}
    (C : ImportedSQ.FockCertificate L) (c : TGLCoupling) (m : ℕ)
    (hm : Real.log 2 / c.beta < (m : ℝ)) :
    oraculo C c m (codificaFormula []) ≠ oraculo C c m (codificaFormula [[]]) := by
  intro h
  have hy : 2 ≤ oraculo C c m (codificaFormula []) := by
    rw [o_oraculo_le_a_fita, uma_leitura_decide_SATcru C c m hm]
    exact empty_formula_sat
  rw [h, o_oraculo_le_a_fita, uma_leitura_decide_SATcru C c m hm] at hy
  exact empty_clause_unsat hy

theorem missing_formula_rejected {L : ImportedSQ.LightOneParticle}
    (C : ImportedSQ.FockCertificate L) (c : TGLCoupling) (m : ℕ) :
    oraculo C c m [] = 0 := rfl

end CodexReview.Ponte

#print axioms CodexReview.Ponte.one_read_iff_reduces
#print axioms CodexReview.Ponte.formula_encoding_injective
#print axioms CodexReview.Ponte.np_input_alphabet_finite
#print axioms CodexReview.Ponte.unary_name_cost
#print axioms CodexReview.Ponte.empty_formula_sat
#print axioms CodexReview.Ponte.empty_clause_unsat
#print axioms CodexReview.Ponte.answers_separate
#print axioms CodexReview.Ponte.missing_formula_rejected

import TGLExt.TraducaoTuring

/- Duas contas sobre a soma de `OPassoEOFim` (o passo 1 − β). Trabalhamos com
   leituras do todo e das n máscaras de coordenada; r é o fator após os passos. -/
namespace IALD.LeiturasComFolga
open TGLExt.TraducaoTuring
open scoped BigOperators

abbrev Assignment (n : ℕ) := Fin n → Bool

noncomputable def signal {n : ℕ} (f : CNF n) (r : ℝ) (m : Assignment n → Bool) : ℝ :=
  ∑ x : Assignment n, if m x then r ^ custoCNF f x else 0

def hasWitness {n : ℕ} (f : CNF n) (m : Assignment n → Bool) : Prop :=
  ∃ x, m x = true ∧ custoCNF f x = 0

theorem all_witness {n : ℕ} (f : CNF n) : hasWitness f (fun _ => true) ↔ SAT f := by
  simp [hasWitness, SAT, custoCNF_zero_sse]

theorem signal_yes {n : ℕ} (f : CNF n) (r : ℝ) (m : Assignment n → Bool)
    (hr : 0 ≤ r) (h : hasWitness f m) : 1 ≤ signal f r m := by
  obtain ⟨x,hm,hc⟩ := h
  have hl := Finset.single_le_sum (s := (Finset.univ : Finset (Assignment n)))
    (f := fun y => if m y then r ^ custoCNF f y else 0)
    (fun y _ => by split <;> positivity) (Finset.mem_univ x)
  simpa [hm,hc,signal] using hl

theorem signal_no {n : ℕ} (f : CNF n) (r : ℝ) (m : Assignment n → Bool)
    (hr : 0 ≤ r) (hr' : r ≤ 1) (h : ¬ hasWitness f m) :
    signal f r m ≤ (2:ℝ)^n * r := by
  unfold signal
  calc
    _ ≤ ∑ _x : Assignment n, r := by
      apply Finset.sum_le_sum
      intro x _
      cases hm : m x with
      | false => simpa using hr
      | true =>
        simp only [if_true]
        cases ec : custoCNF f x with
        | zero => exact False.elim (h ⟨x,hm,ec⟩)
        | succ j =>
          rw [pow_succ]
          exact mul_le_of_le_one_left hr (pow_le_one₀ hr hr')
    _ = _ := by simp [Assignment, nsmul_eq_mul]

/-- Uma única leitura aproximada decide qualquer máscara, também a máscara de todos. -/
theorem leitura_com_folga {n : ℕ} (f : CNF n) (r : ℝ) (m : Assignment n → Bool)
    (hr : 0 ≤ r) (hr' : r ≤ 1) (y : ℝ)
    (herror : |y - signal f r m| < (1 - (2:ℝ)^n*r)/2) :
    (1 + (2:ℝ)^n*r)/2 ≤ y ↔ hasWitness f m := by
  obtain ⟨e₁,e₂⟩ := abs_lt.mp herror
  constructor
  · intro hy
    by_contra h
    have := signal_no f r m hr hr' h
    linarith
  · intro h
    have := signal_yes f r m hr h
    linarith

def mask {n : ℕ} (j : Option (Fin n)) (x : Assignment n) : Bool :=
  match j with
  | none => true
  | some i => x i

/-- Uma leitura de existência mais uma por coordenada devolvem a solução isolada.
    A decodificação só compara com um limiar comum, inclusive quando n = 0. -/
theorem n_mais_uma_leituras {n : ℕ} (f : CNF n) (r : ℝ) (hr : 0 ≤ r) (hr' : r ≤ 1)
    (x : Assignment n) (hx : custoCNF f x = 0)
    (hu : ∀ z, custoCNF f z = 0 → z = x)
    (y : Option (Fin n) → ℝ)
    (he : ∀ j, |y j - signal f r (mask j)| < (1-(2:ℝ)^n*r)/2) :
    (1+(2:ℝ)^n*r)/2 ≤ y none ∧
    (fun i => decide ((1+(2:ℝ)^n*r)/2 ≤ y (some i))) = x := by
  constructor
  · exact (leitura_com_folga f r (mask none) hr hr' _ (he none)).2 ⟨x,rfl,hx⟩
  · funext i
    have hiff : (1+(2:ℝ)^n*r)/2 ≤ y (some i) ↔ x i = true := by
      rw [leitura_com_folga f r (mask (some i)) hr hr' _ (he _)]
      constructor
      · rintro ⟨z,hz,hc⟩
        simpa [mask, hu z hc] using hz
      · intro hi
        exact ⟨x,hi,hx⟩
    cases hi : x i <;> simp_all

theorem sinal_do_passo {n : ℕ} (f : CNF n) (β : ℝ) (k : ℕ) :
    signal f ((1-β)^k) (mask none) =
    ∑ x : Assignment n, (1-β)^(k * custoCNF f x) := by
  simp [signal,mask,pow_mul]

/-- Uma folga uniforme: com kβ ≥ (n+2) log 2, a cauda é no máximo 1/4. -/
theorem cauda_uniforme (n k : ℕ) (β : ℝ) (_hp : 0 < β) (hb : β < 1)
    (hk : ((n:ℝ)+2)*Real.log 2 ≤ (k:ℝ)*β) :
    (2:ℝ)^n*(1-β)^k ≤ 1/4 := by
  have hpos : 0 < 1-β := by linarith
  have hlog := Real.log_le_sub_one_of_pos hpos
  have hmul : (k:ℝ)*Real.log (1-β) ≤ (k:ℝ)*(-β) :=
    mul_le_mul_of_nonneg_left (by linarith) (Nat.cast_nonneg k)
  have ht : (n:ℝ)*Real.log 2 + (k:ℝ)*Real.log (1-β) ≤ -(2*Real.log 2) := by
    linarith
  have h := Real.exp_le_exp.mpr ht
  rw [Real.exp_add, Real.exp_neg, Real.exp_nat_mul, Real.exp_nat_mul,
    Real.exp_log (by norm_num : (0:ℝ)<2), Real.exp_log hpos, two_mul, Real.exp_add,
    Real.exp_log (by norm_num : (0:ℝ)<2)] at h
  norm_num at h ⊢
  exact h

end IALD.LeiturasComFolga

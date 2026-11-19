import TGLExt.OPsiBitDaFormula
import TGLExt.InformacaoDoResumo

/-! Comparing actual formula PsiBits, indexed partition functions, and exact
continuation states. Coordinate flips preserve the entire unmasked partition
curve, but a common suffix can distinguish the pinned assignments. -/
namespace IALD.PalavrasResiduais
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open IALD.LeitorDaFormula IALD.InformacaoDoResumo

abbrev Bits (n : ℕ) := Fin n → Bool

def flip {n : ℕ} (a b x : Bits n) : Bits n :=
  fun i => if a i = b i then x i else !(x i)

private theorem twice {n : ℕ} (a b x : Bits n) : flip a b (flip a b x) = x := by
  funext i
  by_cases h : a i = b i <;> simp [flip,h]

def perm {n : ℕ} (a b : Bits n) : Equiv.Perm (Bits n) :=
  ⟨flip a b,flip a b,twice a b,twice a b⟩

private theorem flipped_test {n : ℕ} (a b x : Bits n) (i : Fin n) :
    ((flip a b x) i == b i) = (x i == a i) := by
  cases h₁ : a i <;> cases h₂ : b i <;> cases h₃ : x i <;> simp [flip,h₁,h₂,h₃]

theorem cost_permutation {n : ℕ} (a b x : Bits n) :
    custoCNF (isolate b) (perm a b x) = custoCNF (isolate a) x := by
  simp only [custoCNF,isolate,List.ofFn_eq_map,List.countP_map]
  congr 1
  funext i
  simp [satisfeita,Literal.vale,perm,flipped_test]

/-- Every unmasked partition value is identical, at every real time. -/
theorem partition_curves_equal {n : ℕ} (a b : Bits n) (t : ℝ) :
    particao (custoCNF (isolate a)) t = particao (custoCNF (isolate b)) t := by
  unfold particao
  calc
    _ = ∑ x : Bits n, Real.exp (-(t * (custoCNF (isolate b) (perm a b x) : ℝ))) := by
      apply Finset.sum_congr rfl
      intro x _
      rw [cost_permutation]
    _ = _ := Equiv.sum_comp (perm a b) (fun x => Real.exp (-(t * (custoCNF (isolate b) x : ℝ))))

private theorem pin_word {n : ℕ} (a : Bits n) : palavraDaFormula (isolate a) = true :=
  (a_palavra_e_o_sat _).2 ((sat_iff _).2 ⟨a,(isolate_spec a a).2 rfl⟩)

theorem pin_psibits_equal {n : ℕ} (a b : Bits n) (t : ℝ) :
    psibitDaFormula (isolate a) t = psibitDaFormula (isolate b) t := by
  unfold psibitDaFormula verboDaFormula descida
  rw [pin_word,pin_word,partition_curves_equal a b t,partition_curves_equal a b (t+1)]

theorem suffix_tests_name {n : ℕ} (a b : Bits n) :
    palavraDaFormula (isolate a ++ isolate b) = true ↔ b = a := by
  rw [a_palavra_e_o_sat,append_isolate,isolate_spec]

/-- The very same suffix distinguishes these prefix words, even though no real
time (or even the collection of all unmasked real partition values) distinguishes them. -/
theorem distinguish_pins {n : ℕ} (a b : Bits n) (hne : a ≠ b) :
    (∀ t, psibitDaFormula (isolate a) t = psibitDaFormula (isolate b) t) ∧
    (∀ t, psibitDaFormula (isolate a ++ isolate a) t ≠
          psibitDaFormula (isolate b ++ isolate a) t) := by
  refine ⟨pin_psibits_equal a b,?_⟩
  intro t h
  have hf := congrArg Prod.fst h
  change palavraDaFormula (isolate a ++ isolate a) = palavraDaFormula (isolate b ++ isolate a) at hf
  exact hne ((suffix_tests_name b a).1 (hf ▸ (suffix_tests_name a a).2 rfl))

/-- Failure already at one bit with a common unit suffix. t can be chosen arbitrarily. -/
theorem no_context_free_product (t : ℝ) :
    ¬ ∃ combine : (Bool × SignType) → (Bool × SignType) → Bool × SignType,
      ∀ p q : CNF 1, psibitDaFormula (p ++ q) t =
        combine (psibitDaFormula p t) (psibitDaFormula q t) := by
  let a : Bits 1 := fun _ => false
  let b : Bits 1 := fun _ => true
  have ne : a ≠ b := by intro h; have := congrFun h 0; contradiction
  obtain ⟨hc,hd⟩ := distinguish_pins a b ne
  rintro ⟨op,ho⟩
  apply hd t
  rw [ho (isolate a) (isolate a),ho (isolate b) (isolate a),hc t]

/-- All real samples of the two bits and the partition, supplied for free. -/
noncomputable def observation {n : ℕ} (p : CNF n) :
    (ℝ → Bool × SignType) × (ℝ → ℝ) :=
  (psibitDaFormula p, particao (custoCNF p))

/-- Even this entire observation and the actual syntax of the common suffix
cannot replace the correlations between the variable labels and the surviving models. -/
theorem no_unmasked_curve_update :
    ¬ ∃ next : ((ℝ → Bool × SignType) × (ℝ → ℝ)) → CNF 1 → Bool,
      ∀ p q : CNF 1, next (observation p) q = palavraDaFormula (p ++ q) := by
  let a : Bits 1 := fun _ => false
  let b : Bits 1 := fun _ => true
  have ne : a ≠ b := by intro h; have := congrFun h 0; contradiction
  have e : observation (isolate a) = observation (isolate b) :=
    Prod.ext (funext (pin_psibits_equal a b)) (funext (partition_curves_equal a b))
  rintro ⟨op,ho⟩
  apply ne
  apply (suffix_tests_name b a).mp
  rw [← ho, ← e, ho]
  exact (suffix_tests_name a a).mpr rfl

/-- State count at a cut in any deterministic exact clause-stream computation.
2^n possible states require n bits as a cardinality bound only. -/
theorem necessary_states {n : ℕ} {S : Type*} [Fintype S]
    (initial : S) (step : S → Clausula n → S) (read : S → Bool)
    (correct : ∀ p : CNF n, read (p.foldl step initial) = palavraDaFormula p) :
    2^n ≤ Fintype.card S := by
  let code (a : Bits n) := (isolate a).foldl step initial
  have hi : Function.Injective code := by
    intro a b hab
    dsimp [code] at hab
    apply (suffix_tests_name b a).1
    rw [← correct,List.foldl_append,← hab]
    rw [← List.foldl_append,correct]
    exact (suffix_tests_name a a).2 rfl
  simpa [Bits] using Fintype.card_le_of_injective code hi

end IALD.PalavrasResiduais

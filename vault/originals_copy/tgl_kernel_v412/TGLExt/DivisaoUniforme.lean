import TGLExt.OResumoEPsiBit

namespace Codex.Fresh

variable {n : Nat}

def agree (S : Finset (Fin n)) (x y : Fin n → Bool) : Prop :=
  ∀ i ∈ S, x i = y i

noncomputable def mass (S : Finset (Fin n)) (u : Fin n → Bool)
    (W : (Fin n → Bool) → ℝ) : ℝ := by
  classical
  exact ∑ x ∈ Finset.univ.filter (fun x => agree S x u), W x

/-- Trocar só o bit i dá a bijeção entre as duas extensões. -/
private def flipAt (i : Fin n) (x : Fin n → Bool) : Fin n → Bool :=
  fun j => if j = i then !(x j) else x j

private theorem flip_twice (i : Fin n) (x : Fin n → Bool) :
    flipAt i (flipAt i x) = x := by
  funext j
  by_cases h : j = i <;> simp [flipAt,h]

private def flipEquiv (i : Fin n) : (Fin n → Bool) ≃ (Fin n → Bool) :=
  ⟨flipAt i, flipAt i, flip_twice i, flip_twice i⟩

private theorem one_bit (F : Finset (Fin n)) (i : Fin n) (hi : i ∉ F)
    (u : Fin n → Bool) (W : (Fin n → Bool) → ℝ) (hw : ∀ x, W x = W (flipAt i x)) :
    2 * mass (insert i F) u W = mass F u W := by
  classical
  let xs := Finset.univ.filter (fun x => agree F x u)
  let p := fun x : Fin n → Bool => x i = u i
  have agree_flip (x : Fin n → Bool) : agree F x u ↔ agree F (flipAt i x) u := by
    have same (j : Fin n) (hj : j ∈ F) : flipAt i x j = x j := by
      have ne : j ≠ i := fun e => hi (e ▸ hj)
      simp [flipAt, ne]
    constructor
    · intro h j hj; exact (same j hj).trans (h j hj)
    · intro h j hj; exact (same j hj).symm.trans (h j hj)
  have parity (x : Fin n → Bool) : p x ↔ ¬ p (flipAt i x) := by
    cases hx : x i <;> cases hu : u i <;> simp [p,flipAt,hx,hu]
  have equal_halves :
      (∑ x ∈ xs.filter p, W x) = ∑ x ∈ xs.filter (fun x => ¬p x), W x := by
    apply Finset.sum_equiv (flipEquiv i)
    · intro x
      change (x ∈ xs.filter p) ↔ flipAt i x ∈ xs.filter (fun x => ¬p x)
      simpa only [xs,Finset.mem_filter,Finset.mem_univ,true_and] using
        and_congr (agree_flip x) (parity x)
    · intro x _; exact hw x
  have fixedHalf : Finset.univ.filter (fun x => agree (insert i F) x u) = xs.filter p := by
    ext x
    simp only [xs,p,Finset.mem_filter,Finset.mem_univ,true_and]
    change (∀ j ∈ insert i F, x j = u j) ↔ _ ∧ _
    rw [Finset.forall_mem_insert]
    exact and_comm
  unfold mass
  rw [fixedHalf,two_mul]
  calc
    _ = (∑ x ∈ xs.filter p, W x) + ∑ x ∈ xs.filter (fun x => ¬p x), W x :=
      congrArg (fun v => (∑ x ∈ xs.filter p, W x) + v) equal_halves
    _ = _ := Finset.sum_filter_add_sum_filter_not xs p W

/-- Cada bit recém-exposto divide igualmente a massa. Vale para peso real
arbitrário independente em conjunto dos bits frescos, inclusive peso assinado. -/
theorem split_mass (F D : Finset (Fin n)) (hFD : F ⊆ D) (u : Fin n → Bool)
    (W : (Fin n → Bool) → ℝ)
    (hW : ∀ x y, (∀ i, i ∉ D \ F → x i = y i) → W x = W y) :
    (2 : ℝ) ^ (D \ F).card * mass D u W = mass F u W := by
  classical
  have go : ∀ S : Finset (Fin n), S ⊆ D \ F →
      (2 : ℝ)^S.card * mass (F ∪ S) u W = mass F u W := by
    intro S
    induction S using Finset.induction_on with
    | empty => simp
    | @insert i S hi ih =>
      intro hsub
      have hfresh : i ∈ D \ F := hsub (Finset.mem_insert_self i S)
      have hs : S ⊆ D \ F := fun _ hj => hsub (Finset.mem_insert_of_mem hj)
      have hi' : i ∉ F ∪ S := by
        simp only [Finset.mem_union,not_or]
        exact ⟨(Finset.mem_sdiff.mp hfresh).2,hi⟩
      have step := one_bit (F ∪ S) i hi' u W (fun x =>
        hW x (flipAt i x) (fun j hj => by
          have hji : j ≠ i := fun e => hj (e ▸ hfresh)
          simp [flipAt,hji]))
      have hset : F ∪ insert i S = insert i (F ∪ S) := by ext j; simp
      rw [Finset.card_insert_of_notMem hi, pow_succ, hset, mul_assoc, step]
      exact ih hs
  have cover : F ∪ (D \ F) = D := by
    ext i
    simp only [Finset.mem_union,Finset.mem_sdiff]
    by_cases hf : i ∈ F
    · simp [hf,hFD hf]
    · simp [hf]
  simpa only [cover] using go (D \ F) (fun _ h => h)

end Codex.Fresh

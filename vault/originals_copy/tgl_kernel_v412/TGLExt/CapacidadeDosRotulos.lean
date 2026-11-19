import TGLExt.ObrigacoesJaSatisfeitas

/-! Finite-channel capacity for all flat CNF relations under continuations
that can pin the still-free separator. Counts the whole self-contained key.
A backing store or an unbounded-precision carrier changes the resource. -/
set_option autoImplicit false
namespace Codex.LabelCapacity
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
abbrev Row (w : Nat) := Fin w → Bool

def reject {w : Nat} (a : Row w) : Clausula w :=
  (List.finRange w).map (fun i => ⟨i,!(a i)⟩)

def fixRow {w : Nat} (a : Row w) : CNF w :=
  (List.finRange w).map (fun i => [⟨i,a i⟩])

theorem reject_spec {w : Nat} (a x : Row w) :
    satisfeita (reject a) x = true ↔ x ≠ a := by
  constructor
  · intro h same
    subst x
    obtain ⟨l,mem,ok⟩ := List.any_eq_true.mp h
    obtain ⟨j,_,rfl⟩ := List.mem_map.mp mem
    cases z : a j <;> simp [Literal.vale,z] at ok
  · intro h
    have ex : ∃ i, x i ≠ a i := by
      by_contra! q
      exact h (funext q)
    obtain ⟨i,ne⟩ := ex
    refine List.any_eq_true.mpr ⟨⟨i,!(a i)⟩,List.mem_map.mpr ⟨i,by simp,rfl⟩,?_⟩
    cases e : x i <;> cases d : a i <;> simp_all [Literal.vale]

theorem fix_spec {w : Nat} (a x : Row w) : passes (fixRow a) x = true ↔ x = a := by
  constructor
  · intro h
    apply funext
    intro i
    have mem : ([⟨i,a i⟩] : Clausula w) ∈ fixRow a := List.mem_map.mpr ⟨i,by simp,rfl⟩
    simpa [satisfeita,Literal.vale] using List.all_eq_true.mp h _ mem
  · rintro rfl
    simp [fixRow,passes,List.all_eq_true,satisfeita,Literal.vale]

noncomputable def flat {w : Nat} (r : Row w → Bool) : CNF w :=
  ((Finset.univ.filter (fun x => r x = false)).toList).map reject

theorem flat_spec {w : Nat} (r : Row w → Bool) (x : Row w) :
    passes (flat r) x = true ↔ r x = true := by
  classical
  constructor
  · intro h
    cases z : r x with
    | true => rfl
    | false =>
      have mem : reject x ∈ flat r := List.mem_map.mpr ⟨x,by simp [z],rfl⟩
      exact ((reject_spec x x).mp (List.all_eq_true.mp h _ mem) rfl).elim
  · intro hit
    apply List.all_eq_true.mpr
    intro c mem
    obtain ⟨y,hy,rfl⟩ := List.mem_map.mp mem
    have hy' : r y = false := by simpa using hy
    apply (reject_spec y x).mpr
    rintro rfl
    simp_all

theorem probe_reads {w : Nat} (r : Row w → Bool) (x : Row w) :
    palavraDaFormula (flat r ++ fixRow x) = r x := by
  apply Bool.eq_iff_iff.mpr
  rw [a_palavra_e_o_sat,sat_iff]
  have both (v : Row w) :
      passes (flat r ++ fixRow x) v = true ↔ r v=true ∧ v=x := by
    rw [show passes (flat r ++ fixRow x) v = (passes (flat r) v && passes (fixRow x) v) by
      simp [passes], Bool.and_eq_true,flat_spec,fix_spec]
  constructor
  · rintro ⟨v,h⟩
    obtain ⟨ok,rfl⟩ := (both v).mp h
    exact ok
  · intro h
    exact ⟨x,(both x).mpr ⟨h,rfl⟩⟩

/-- No enumeration is required of a proposed encoder. Universality over
finite CNFs is enough to force its key space to distinguish the relations. -/
theorem finite_key_bound {w : Nat} {K : Type} [Fintype K]
    (key : CNF w → K) (query : K → Row w → Bool)
    (exactRead : ∀ p x, query (key p) x = palavraDaFormula (p ++ fixRow x)) :
    2^(2^w) ≤ Fintype.card K := by
  classical
  have inj : Function.Injective (fun r : Row w → Bool => key (flat r)) := by
    intro r s same
    funext x
    have eq := congrArg (fun k => query k x) same
    simpa only [exactRead,probe_reads] using eq
  simpa [Row,Fintype.card_fun] using Fintype.card_le_of_injective _ inj

theorem binary_key_bound {w b : Nat} (key : CNF w → (Fin b → Bool))
    (query : (Fin b → Bool) → Row w → Bool)
    (exactRead : ∀ p x, query (key p) x = palavraDaFormula (p ++ fixRow x)) :
    2^w ≤ b := by
  have h : (2:Nat)^(2^w) ≤ 2^b := by
    simpa [Fintype.card_fun] using finite_key_bound key query exactRead
  by_contra! bad
  have small : (2:Nat)^b < 2^(2^w) := pow_lt_pow_right₀ (by decide : 1 < (2:Nat)) bad
  omega

end Codex.LabelCapacity

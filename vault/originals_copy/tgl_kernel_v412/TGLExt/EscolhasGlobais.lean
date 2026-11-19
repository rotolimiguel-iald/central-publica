import TGLExt.ImplicacoesCruzadas

set_option autoImplicit false
namespace Codex.CrossSelectors
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula Codex.HornCross

variable {n : Nat}
def names (c : Clausula n) (b : Bool) := (c.filter (fun l => l.pos == b)).map Literal.var

theorem named (c : Clausula n) (i : Fin n) (b : Bool) : i ∈ names c b ↔ (⟨i,b⟩ : Literal n) ∈ c := by
  simp only [names,List.mem_map,List.mem_filter,beq_iff_eq]
  constructor
  · rintro ⟨⟨j,a⟩,⟨h,hab⟩,hji⟩
    cases hab; cases hji; exact h
  · intro h; exact ⟨⟨i,b⟩,⟨h,rfl⟩,rfl⟩

theorem signed_read (c : Clausula n) (s : Mem n) :
    satisfeita c (readMem s) = true ↔
      (∃ i ∈ names c false, i ∉ s) ∨ (∃ i ∈ names c true, i ∈ s) := by
  simp only [satisfeita,List.any_eq_true,named]
  constructor
  · rintro ⟨⟨i,b⟩,h,hi⟩
    cases b with
    | false => exact Or.inl ⟨i,h,by simpa [Literal.vale,readMem] using hi⟩
    | true => exact Or.inr ⟨i,h,by simpa [Literal.vale,readMem] using hi⟩
  · rintro (⟨i,h,hi⟩|⟨i,h,hi⟩)
    · exact ⟨⟨i,false⟩,h,by simp [Literal.vale,readMem,hi]⟩
    · exact ⟨⟨i,true⟩,h,by simp [Literal.vale,readMem,hi]⟩

/-- Pick one positive head per clause. A negative constraint has a unique empty head. -/
def alternatives (c : Clausula n) : List (Rule n) :=
  let b := names c false
  match names c true with
  | [] => [⟨b,none⟩]
  | i::is => (i::is).map (fun j => ⟨b,some j⟩)

theorem alternatives_read (c : Clausula n) (s : Mem n) :
    (∃ r ∈ alternatives c, ok s r = true) ↔ satisfeita c (readMem s) = true := by
  rw [signed_read]
  unfold alternatives
  cases hp : names c true with
  | nil => simp [ok,active,hit]
  | cons i is =>
    by_cases h : ∃ v ∈ names c false, v ∉ s
    · obtain ⟨v,hv,hn⟩ := h
      have hb : (names c false).all (fun j => decide (j ∈ s)) = false :=
        List.all_eq_false.mpr ⟨v,hv,by simp [hn]⟩
      constructor
      · intro _
        exact Or.inl ⟨v,hv,hn⟩
      · intro _
        exact ⟨⟨names c false, some i⟩,
          List.mem_map.mpr ⟨i,List.mem_cons_self,rfl⟩, by simp [ok,active,hb]⟩
    · simp [ok,active,hit,h]

def programs : CNF n → List (List (Rule n))
  | [] => [[]]
  | c::p => (alternatives c).flatMap (fun r => (programs p).map (r :: ·))

theorem joint_read (p : CNF n) (s : Mem n) :
    (∃ q ∈ programs p, valid q s = true) ↔ passes p (readMem s) = true := by
  induction p with
  | nil => simp [programs,valid,passes]
  | cons c p ih =>
    change _ ↔ (satisfeita c (readMem s) && passes p (readMem s)) = true
    rw [Bool.and_eq_true]
    simp only [programs,List.mem_flatMap,List.mem_map]
    constructor
    · rintro ⟨_,⟨r,hr,q,hq,rfl⟩,h⟩
      have hh : ok s r = true ∧ valid q s = true := by simpa [valid] using h
      exact ⟨(alternatives_read _ _).mp ⟨r,hr,hh.1⟩,ih.mp ⟨q,hq,hh.2⟩⟩
    · rintro ⟨hc,hp⟩
      obtain ⟨r,hr,h₁⟩ := (alternatives_read _ _).mpr hc
      obtain ⟨q,hq,h₂⟩ := ih.mpr hp
      exact ⟨r::q,⟨r,hr,q,hq,rfl⟩,by simpa [valid] using And.intro h₁ h₂⟩

def checkProgram (q : List (Rule n)) := valid q (closure q)
def scan {A : Type} (f : A → Bool) : List A → Bool × Nat
  | [] => (false,0)
  | a::l => if f a then (true,1) else
      let z := scan f l; (z.1,z.2+1)

theorem scan_spec {A} (f : A → Bool) (l : List A) : (scan f l).1 = l.any f := by
  induction l with
  | nil => rfl
  | cons a l ih => cases h : f a <;> simp [scan,h,ih]
theorem scan_all_false {A} (f : A → Bool) (l : List A) (h : l.any f = false) :
    (scan f l).2 = l.length := by
  induction l with
  | nil => rfl
  | cons a l ih =>
    have both : f a = false ∧ l.any f = false := by simpa using h
    simp [scan,both,ih both.2]

theorem selector_word (p : CNF n) :
    (scan checkProgram (programs p)).1 = palavraDaFormula p := by
  rw [scan_spec]
  apply Bool.eq_iff_iff.mpr
  rw [List.any_eq_true,a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨q,hq,h⟩
    exact ⟨_,(joint_read p _).mp ⟨q,hq,h⟩⟩
  · rintro ⟨x,hx⟩
    let s := fromAssignment x
    obtain ⟨q,hq,hvalid⟩ := (joint_read p s).mpr (by simpa [s] using hx)
    exact ⟨q,hq,closed_complete q _ s (settle_le_model _ _ _ _ (by simp) hvalid) (closure_stable _) hvalid⟩

theorem selection_count (c : Clausula n) (p : CNF n) :
    (programs (c::p)).length = (alternatives c).length*(programs p).length := by
  simp [programs,List.length_flatMap]

def choiceClause : Clausula 2 := [⟨0,true⟩,⟨1,true⟩]
def negative (i : Fin 2) : Clausula 2 := [⟨i,false⟩]
def obstruction (m : Nat) : CNF 2 :=
  List.replicate (m+1) choiceClause ++ [negative 0,negative 1]

theorem obstruction_unsat (m : Nat) : ¬SAT (obstruction m) := by
  intro hs
  obtain ⟨x,hx⟩ := (sat_iff _).mp hs
  have all := List.all_eq_true.mp hx
  have h₀ := all (negative 0) (by simp [obstruction])
  have h₁ := all (negative 1) (by simp [obstruction])
  have hc := all choiceClause (by simp [obstruction])
  simp [negative,satisfeita,Literal.vale] at h₀ h₁
  simp [choiceClause,satisfeita,Literal.vale,h₀,h₁] at hc

theorem obstruction_count (m : Nat) : (programs (obstruction m)).length = 2^(m+1) := by
  induction m with
  | zero => decide
  | succ m ih =>
    have h : obstruction (m+1) = choiceClause :: obstruction m := by
      simp only [obstruction,List.replicate_succ,List.cons_append]
    rw [h,selection_count,ih]
    have hc : (alternatives choiceClause).length = 2 := by decide
    rw [hc,pow_succ]
    omega

theorem visits_obstruction (m : Nat) :
    scan checkProgram (programs (obstruction m)) = (false, 2^(m+1)) := by
  have h : (scan checkProgram (programs (obstruction m))).1 = false := by
    rw [selector_word]
    exact Bool.eq_false_iff.mpr (fun bad => obstruction_unsat m ((a_palavra_e_o_sat _).mp bad))
  have h' := h
  rw [scan_spec] at h'
  exact Prod.ext h ((scan_all_false _ _ h').trans (obstruction_count m))

end Codex.CrossSelectors

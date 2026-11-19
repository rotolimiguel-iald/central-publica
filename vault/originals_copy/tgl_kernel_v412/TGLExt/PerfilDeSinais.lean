import TGLExt.RestricaoGlobal

/-! A branch-specific witness selected from the input. Four flags per address
record the signs seen and the signs required by unit clauses. -/
set_option autoImplicit false
namespace Codex.SignProfile
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
variable {n : Nat}

structure Cell where
  seenPos : Bool
  seenNeg : Bool
  unitPos : Bool
  unitNeg : Bool
  deriving DecidableEq, Repr

def blank : Cell := ⟨false,false,false,false⟩
def join (a b : Cell) : Cell := ⟨a.seenPos || b.seenPos, a.seenNeg || b.seenNeg,
  a.unitPos || b.unitPos, a.unitNeg || b.unitNeg⟩
def mark (pos unit : Bool) : Cell := ⟨pos,!pos,unit && pos,unit && !pos⟩
theorem join_assoc (a b c : Cell) : join (join a b) c = join a (join b c) := by
  simp [join,Bool.or_assoc]
@[simp] theorem join_blank (a : Cell) : join a blank = a := by cases a; simp [join,blank]
@[simp] theorem blank_join (a : Cell) : join blank a = a := by cases a; simp [join,blank]

def occurs (j : Nat) (b : Bool) (c : Clausula n) :=
  c.any (fun l => l.var.val == j && l.pos == b)
def flags (ls : Clausula n) (unit : Bool) (j : Nat) : Cell :=
  ⟨occurs j true ls, occurs j false ls, unit && occurs j true ls, unit && occurs j false ls⟩
def singleton (c : Clausula n) : Bool :=
  match c with | [_] => true | _ => false

def profile : CNF n → Nat → Cell
  | [],_ => blank
  | c :: p,j => join (flags c (singleton c) j) (profile p j)

def allowed (c : Cell) : Bool := c.unitPos || c.unitNeg || !(c.seenPos && c.seenNeg)
def pick (c : Cell) : Bool := c.unitPos || (!c.unitNeg && c.seenPos)
def value (p : CNF (n+1)) (b : Bool) (i : Fin (n+1)) : Bool :=
  if i.val = 0 then b else pick (profile p i.val)
def covered (p : CNF (n+1)) : Prop := ∀ j : Fin (n+1), j.val ≠ 0 → allowed (profile p j.val) = true
def present (p : CNF (n+1)) (b : Bool) : Prop := ∃ x, x 0 = b ∧ passes p x = true

theorem flags_cons (l : Literal n) (ls : Clausula n) (u : Bool) (j : Nat) :
    flags (l::ls) u j = join (if l.var.val = j then mark l.pos u else blank) (flags ls u j) := by
  by_cases h : l.var.val = j <;> cases e : l.pos <;> cases u <;>
    simp [flags,occurs,join,mark,blank,h,e,List.any_cons]

private theorem pos_seen {p : CNF n} {c : Clausula n} {l : Literal n}
    (hc : c ∈ p) (hl : l ∈ c) (h : l.pos = true) : (profile p l.var.val).seenPos = true := by
  have one : occurs l.var.val true c = true :=
    List.any_eq_true.mpr ⟨l,hl,by simp [h]⟩
  induction p with
  | nil => simp at hc
  | cons d p ih =>
    rcases List.mem_cons.mp hc with rfl|hm
    · simp [profile,join,flags,one]
    · simp [profile,join,ih hm]

private theorem neg_seen {p : CNF n} {c : Clausula n} {l : Literal n}
    (hc : c ∈ p) (hl : l ∈ c) (h : l.pos = false) : (profile p l.var.val).seenNeg = true := by
  have one : occurs l.var.val false c = true :=
    List.any_eq_true.mpr ⟨l,hl,by simp [h]⟩
  induction p with
  | nil => simp at hc
  | cons d p ih =>
    rcases List.mem_cons.mp hc with rfl|hm
    · simp [profile,join,flags,one]
    · simp [profile,join,ih hm]

private theorem forced {p : CNF n} (x : Fin n → Bool) (ok : passes p x = true)
    (i : Fin n) (b : Bool) :
    (if b then (profile p i.val).unitPos else (profile p i.val).unitNeg) = true → x i = b := by
  induction p with
  | nil => cases b <;> simp [profile,blank]
  | cons c p ih =>
    have sat : satisfeita c x = true ∧ passes p x = true := by simpa [passes] using ok
    have one : singleton c = true → occurs i.val b c = true → x i = b := by
      cases c with
      | nil => simp [singleton]
      | cons l tail =>
        cases tail with
        | cons => simp [singleton]
        | nil =>
          intro _ present
          have both : l.var.val = i.val ∧ l.pos = b := by simpa [occurs] using present
          have ei : l.var = i := Fin.ext both.1
          simpa [satisfeita,Literal.vale,ei,both.2] using sat.1
    cases b <;> simp only [Bool.false_eq_true, if_false, if_true, profile,join,flags,
      Bool.or_eq_true,Bool.and_eq_true] at * <;>
      exact fun h => h.elim (fun e => one e.1 e.2) (ih sat.2)

private theorem dominates {p : CNF (n+1)} (cls : covered p) (b : Bool)
    (x : Fin (n+1) → Bool) (pivot : x 0 = b) (sat : passes p x = true)
    {c : Clausula (n+1)} (hc : c ∈ p) {l : Literal (n+1)} (hl : l ∈ c)
    (hit : x l.var = l.pos) : value p b l.var = l.pos := by
  by_cases z : l.var.val = 0
  · have ez : l.var = 0 := Fin.ext z
    simpa [value,z] using pivot.symm.trans (ez ▸ hit : x 0 = l.pos)
  · have cov := cls l.var z
    have fp := forced x sat l.var true
    have fn := forced x sat l.var false
    by_cases ep : (profile p l.var.val).unitPos = true
    · have pos : l.pos = true := hit.symm.trans (fp ep)
      simp [value,z,pick,ep,pos]
    by_cases en : (profile p l.var.val).unitNeg = true
    · have neg : l.pos = false := hit.symm.trans (fn en)
      simp [value,z,pick,ep,en,neg]
    cases e : l.pos with
    | true => simp [value,z,pick,ep,en,pos_seen hc hl e]
    | false =>
      have neg := neg_seen hc hl e
      have hp : (profile p l.var.val).seenPos = false := by
        simpa [allowed,ep,en,neg] using cov
      simp [value,z,pick,ep,en,hp]

theorem witness_sound (p : CNF (n+1)) (b : Bool) (h : passes p (value p b) = true) : present p b :=
  ⟨value p b,by simp [value],h⟩

theorem witness_complete {p : CNF (n+1)} (h : covered p) (b : Bool) :
    passes p (value p b) = true ↔ present p b := by
  refine ⟨witness_sound p b,?_⟩
  rintro ⟨x,hx,ok⟩
  apply List.all_eq_true.mpr
  intro c hc
  obtain ⟨l,hl,hit⟩ := List.any_eq_true.mp (List.all_eq_true.mp ok c hc)
  have e : x l.var = l.pos := by simpa [Literal.vale] using hit
  exact List.any_eq_true.mpr ⟨l,hl,by simpa [Literal.vale] using dominates h b x hx ok hc hl e⟩

theorem word_from_pair (p : CNF (n+1)) :
    palavraDaFormula p = true ↔ present p false ∨ present p true := by
  rw [a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,h⟩
    cases e : x 0 with
    | false => exact Or.inl ⟨x,e,h⟩
    | true => exact Or.inr ⟨x,e,h⟩
  · rintro (⟨x,_,h⟩|⟨x,_,h⟩) <;> exact ⟨x,h⟩

end Codex.SignProfile

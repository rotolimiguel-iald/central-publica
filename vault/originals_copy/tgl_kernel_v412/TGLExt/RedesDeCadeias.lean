import Mathlib.Tactic.DeriveFintype
import Mathlib.Data.Fintype.Sigma
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum

set_option autoImplicit false

namespace PsiNetworks

structure Lit where
  right : Bool
  sign : Bool
  deriving Repr, DecidableEq, Fintype

def Lit.read (l : Lit) (a b : Bool) : Bool := (if l.right then b else a) == l.sign

/-- Two-terminal clause networks. Series introduces one fresh Boolean junction.
    Parallel identifies the two exterior terminals and keeps the interiors disjoint. -/
inductive Net where
  | clause (first second : Lit)
  | series (left right : Net)
  | parallel (left right : Net)
  deriving Repr

def Witness : Net → Type
  | .clause _ _ => Unit
  | .series l r => Bool × Witness l × Witness r
  | .parallel l r => Witness l × Witness r

def value (e : Net) (a b : Bool) : Witness e → Bool :=
  match e with
  | .clause p q => fun _ => p.read a b || q.read a b
  | .series l r => fun w => value l a w.1 w.2.1 && value r w.1 b w.2.2
  | .parallel l r => fun w => value l a b w.1 && value r a b w.2

abbrev Table := Bool → Bool → Bool → Bool

def anyBit (f : Bool → Bool) : Bool := f false || f true

theorem anyBit_spec (f : Bool → Bool) : anyBit f = true ↔ ∃ s, f s = true := by
  simp only [anyBit, Bool.or_eq_true]
  constructor
  · rintro (h|h)
    · exact ⟨false,h⟩
    · exact ⟨true,h⟩
  · rintro ⟨s,h⟩
    cases s
    · exact Or.inl h
    · exact Or.inr h

def atom (p q : Lit) : Table := fun a b z => ((p.read a b || q.read a b) == z)

def meet (f g : Bool → Bool) (z : Bool) : Bool :=
  anyBit fun u => anyBit fun v => f u && g v && ((u && v) == z)

def combine (serial : Bool) (f g : Table) : Table := fun a b z =>
  if serial then anyBit (fun m => meet (f a m) (g m b) z)
  else meet (f a b) (g a b) z

def summary : Net → Table
  | .clause p q => atom p q
  | .series l r => combine true (summary l) (summary r)
  | .parallel l r => combine false (summary l) (summary r)

theorem meet_spec {A B : Type} (f : A → Bool) (g : B → Bool)
    (s t : Bool → Bool) (hs : ∀ u, s u = true ↔ ∃ x, f x = u)
    (ht : ∀ v, t v = true ↔ ∃ y, g y = v) (z : Bool) :
    meet s t z = true ↔ ∃ x y, (f x && g y) = z := by
  simp only [meet, anyBit_spec, Bool.and_eq_true, beq_iff_eq, hs, ht]
  constructor
  · rintro ⟨u,v,⟨⟨x,hx⟩,⟨y,hy⟩⟩,huv⟩
    exact ⟨x,y,by simpa [hx,hy] using huv⟩
  · rintro ⟨x,y,h⟩
    exact ⟨f x,g y,⟨⟨x,rfl⟩,⟨y,rfl⟩⟩,h⟩

theorem summary_spec (e : Net) (a b z : Bool) :
    summary e a b z = true ↔ ∃ w, value e a b w = z := by
  induction e generalizing a b z with
  | clause p q => simp [summary, atom, value, Witness]
  | series l r hl hr =>
    simp only [summary, combine, if_true, anyBit_spec,
      meet_spec _ _ _ _ (hl _ _) (hr _ _)]
    constructor
    · rintro ⟨m,x,y,h⟩
      exact ⟨⟨m,x,y⟩,h⟩
    · rintro ⟨⟨m,x,y⟩,h⟩
      exact ⟨m,x,y,h⟩
  | parallel l r hl hr =>
    simp only [summary, combine, Bool.false_eq_true, if_false,
      meet_spec _ _ _ _ (hl _ _) (hr _ _)]
    constructor
    · rintro ⟨x,y,h⟩
      exact ⟨⟨x,y⟩,h⟩
    · rintro ⟨⟨x,y⟩,h⟩
      exact ⟨x,y,h⟩

def result (t : Table) (z : Bool) : Bool := anyBit fun a => anyBit fun b => t a b z

theorem result_spec (e : Net) (z : Bool) :
    result (summary e) z = true ↔ ∃ a b w, value e a b w = z := by
  simp only [result, anyBit_spec, summary_spec]

end PsiNetworks

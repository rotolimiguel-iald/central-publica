import TGLExt.CapacidadeDosRotulos

/-! Equality of named boundary words as a deterministic challenge. The
choice of names and ordering is common. One side transmits once; the
receiver has the other word. No backing store or error allowance. -/
set_option autoImplicit false
namespace Codex.NamedWire
abbrev Word (w : Nat) := Fin w → Bool

theorem binding_required {w : Nat} {Tag : Type} (send : Word w → Tag)
    (check : Tag → Word w → Bool)
    (h : ∀ x y, check (send x) y = true ↔ x=y) :
    Function.Injective send := by
  intro x y same
  apply (h x y).mp
  rw [same]
  exact (h y y).mpr rfl

theorem bits_required {w b : Nat} (send : Word w → Word b)
    (check : Word b → Word w → Bool)
    (h : ∀ x y, check (send x) y = true ↔ x=y) : w ≤ b := by
  have cap := Fintype.card_le_of_injective send (binding_required send check h)
  have hc : (2:Nat)^w ≤ 2^b := by simpa [Word,Fintype.card_fun] using cap
  by_contra! lt
  exact (Nat.not_le_of_gt (pow_lt_pow_right₀ (by decide : 1 < (2:Nat)) lt)) hc

inductive Cell where | zero | one
deriving DecidableEq

def cell : Bool → Cell | false => .zero | true => .one

/-- Fixed shared schema. On each wire the first bit records acceptance
of the local fragment of the challenge clause. Remaining bits are the
assigned values in the declared variable order. -/
def packet (hit : Bool) (body : List Bool) := cell hit :: body.map cell

def compareCells : List Cell → List Cell → Bool → Bool × Nat
  | a::as,b::bs,valid =>
    let r := compareCells as bs (valid && a == b)
    (r.1,r.2+2)
  | [],[],valid => (valid,0)
  | _,_,_ => (false,0)

def receive : List Cell → List Cell → Bool × Nat
  | a::as,b::bs =>
    let r := compareCells as bs (a == .one || b == .one)
    (r.1,r.2+2)
  | _,_ => (false,0)

private theorem cell_eq (a b : Bool) : (cell a == cell b) = (a == b) := by
  cases a <;> cases b <;> rfl

private theorem compare_result (xs ys : List Bool) (v : Bool) :
    (compareCells (xs.map cell) (ys.map cell) v).1 = (v && (xs == ys)) := by
  induction xs generalizing ys v with
  | nil => cases ys <;> cases v <;> rfl
  | cons x xs ih =>
    cases ys with
    | nil => cases v <;> rfl
    | cons y ys =>
      change (compareCells (xs.map cell) (ys.map cell) (v && cell x == cell y)).1 = _
      rw [ih,cell_eq]
      change ((v && (x == y)) && (xs == ys)) = (v && ((x == y) && (xs == ys)))
      exact Bool.and_assoc ..

private theorem compare_travel (xs ys : List Bool) (v : Bool) :
    (compareCells (xs.map cell) (ys.map cell) v).2 = 2 * min xs.length ys.length := by
  induction xs generalizing ys v with
  | nil => cases ys <;> simp [compareCells]
  | cons x xs ih =>
    cases ys with
    | nil => rfl
    | cons y ys =>
      change (compareCells (xs.map cell) (ys.map cell) _).2+2 = _
      rw [ih]
      simp only [List.length_cons]
      omega

/-- Two read-only, unit-move heads, finite local control. No precomputed
digest, content comparison or integer address is a primitive. -/
theorem charged_comparison (xs ys : List Bool) (a b : Bool) :
    receive (packet a xs) (packet b ys) =
      (((a || b) && (xs == ys)), 2*(min xs.length ys.length + 1)) := by
  unfold receive packet
  simp only [compare_result,compare_travel]
  cases a <;> cases b <;> simp [cell,Nat.mul_add]

theorem reject_marginals :
    receive (packet true [true,false]) (packet true [false,true]) = (false,6) ∧
    receive (packet false [true,false]) (packet true [true,false]) = (true,6) := by decide

end Codex.NamedWire

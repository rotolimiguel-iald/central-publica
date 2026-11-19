import TGLExt.LeituraComReuso

/-! Lossless streaming transport of any raw CNF spelling, with the source
head and the destination head both charged. Four signed quadrants encode
the four source letters. Ordinary serial binary channel, no analogue oracle. -/
set_option autoImplicit false
namespace Codex.InscriptionWire
open Codex.PolinomioPorEscolha TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open TGLExt.Psibit IALD.LeitorDaFormula

def symbol : Letter → Bool × Bool
  | .tick       => (false,false)
  | .delimiter  => (false,true)
  | .sign false => (true,false)
  | .sign true  => (true,true)

def letter : Bool → Bool → Letter
  | false,false => .tick
  | false,true => .delimiter
  | true,b => .sign b

theorem symbol_roundtrip (a : Letter) : letter (symbol a).1 (symbol a).2 = a := by
  cases a with | tick | delimiter => rfl | sign s => cases s <;> rfl

theorem symbols_are_orthants (a : Letter) :
    ∃ θ : ℝ, (codeAmp θ).word = bitSign (symbol a).1 ∧
      (codeAmp θ).verb = bitSign (symbol a).2 := by
  have nz (v : Bool) : bitSign v ≠ 0 := by cases v <;> decide
  exact the_orbit_visits_all_four_states _ _ (nz _) (nz _)

def encode : List Letter → List Bool
  | [] => []
  | a::xs => (symbol a).1 :: (symbol a).2 :: encode xs

theorem encoded_append (xs ys : List Letter) : encode (xs++ys) = encode xs ++ encode ys := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simpa only [List.cons_append,encode,List.cons.injEq,true_and] using ih

theorem encoded_length (xs : List Letter) : (encode xs).length = 2*xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs h => simp [encode,h,Nat.mul_succ]

inductive Tx where
  | fetch (src : List Letter) (writtenRev : List Bool)
  | second (b : Bool) (rest : List Letter) (writtenRev : List Bool)
  | stop (writtenRev : List Bool)
deriving DecidableEq

def txStep : Tx → Tx
  | .fetch [] z => .stop z
  | .fetch (a::xs) z => .second (symbol a).2 xs ((symbol a).1 :: z)
  | .second b xs z => .fetch xs (b::z)
  | .stop z => .stop z

/-- One shift of each head on fetch; only the output head shifts on second. -/
def txMoved : Tx → Nat
  | .fetch (_::_) _ => 2
  | .second .. => 1
  | _ => 0

def shifts {S : Type} (step : S → S) (moves : S → Nat) : Nat → S → Nat
  | 0,_ => 0
  | t+1,s => moves s + shifts step moves t (step s)

theorem transmit (xs : List Letter) (z : List Bool) :
    txStep^[2*xs.length+1] (.fetch xs z) = .stop ((encode xs).reverse ++ z) ∧
    shifts txStep txMoved (2*xs.length+1) (.fetch xs z) = 3*xs.length := by
  induction xs generalizing z with
  | nil => exact ⟨rfl,rfl⟩
  | cons a xs ih =>
    have t := ih ((symbol a).2 :: (symbol a).1 :: z)
    rw [List.length_cons,Nat.mul_succ,Nat.mul_succ]
    rw [show 2*xs.length+2+1 = (2*xs.length+1)+1+1 by omega]
    constructor
    · simpa only [Function.iterate_succ_apply,txStep,encode,List.reverse_cons,
        List.append_assoc,List.cons_append,List.nil_append] using t.1
    · change 2 + (1 + shifts txStep txMoved (2*xs.length+1)
        (.fetch xs ((symbol a).2 :: (symbol a).1 :: z))) = _
      rw [t.2]; omega

inductive Rx where
  | first (src : List Bool) (writtenRev : List Letter)
  | second (a : Bool) (rest : List Bool) (writtenRev : List Letter)
  | stop (writtenRev : List Letter)
  | incomplete
deriving DecidableEq

def rxStep : Rx → Rx
  | .first [] z => .stop z
  | .first (a::xs) z => .second a xs z
  | .second a (b::xs) z => .first xs (letter a b :: z)
  | .second _ [] _ => .incomplete
  | .stop z => .stop z
  | .incomplete => .incomplete

def rxMoved : Rx → Nat
  | .first (_::_) _ => 1
  | .second _ (_::_) _ => 2
  | _ => 0

theorem receive (xs z : List Letter) :
    rxStep^[2*xs.length+1] (.first (encode xs) z) = .stop (xs.reverse ++ z) ∧
    shifts rxStep rxMoved (2*xs.length+1) (.first (encode xs) z) = 3*xs.length := by
  induction xs generalizing z with
  | nil => exact ⟨rfl,rfl⟩
  | cons a xs ih =>
    have t := ih (a::z)
    rw [List.length_cons,Nat.mul_succ,Nat.mul_succ]
    rw [show 2*xs.length+2+1 = (2*xs.length+1)+1+1 by omega]
    constructor
    · simpa only [Function.iterate_succ_apply,encode,rxStep,symbol_roundtrip,List.reverse_cons,
        List.append_assoc,List.cons_append,List.nil_append] using t.1
    · change 1 + (2 + shifts rxStep rxMoved (2*xs.length+1)
        (.first (encode xs) (letter (symbol a).1 (symbol a).2 :: z))) = _
      rw [symbol_roundtrip,t.2]; omega

/-- The receiver starts at the beginning of the serial stream. If a single
tape is reused, charge rewind as well. Reverse lists model the already
written portion to the left of each head, not an extra reverse pass. -/
theorem any_cnf_transport {n : Nat} (p : CNF n) :
    let w := original p
    let t := 2*w.length+1
    txStep^[t] (.fetch w []) = .stop (encode w).reverse ∧
    rxStep^[t] (.first (encode w) []) = .stop w.reverse ∧
    shifts txStep txMoved t (.fetch w []) + shifts rxStep rxMoved t (.first (encode w) []) =
      6*w.length ∧
    shifts txStep txMoved t (.fetch w []) + (encode w).length +
      shifts rxStep rxMoved t (.first (encode w) []) = 8*w.length := by
  dsimp only
  obtain ⟨a,b⟩ := transmit (original p) []
  obtain ⟨c,d⟩ := receive (original p) []
  simp only [List.append_nil] at a c
  exact ⟨a,c,by rw [b,d]; omega,by rw [b,d,encoded_length]; omega⟩

end Codex.InscriptionWire

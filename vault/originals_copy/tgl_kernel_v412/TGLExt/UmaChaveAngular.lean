import TGLExt.RelacaoEmFase
import TGLExt.CadeiaNaFita

/-! Raw tape to one tagged turn, actual noisy decoder and composition.
The rational sample is a channel model; tape execution uses the four-bit
symbol. A complete physical truth assignment is never a machine input. -/
set_option autoImplicit false
namespace Codex.SinglePhase
open Codex.OrthantRelation
open Codex.PolinomioPorEscolha (Letter original)
open TGLExt.TraducaoTuring IALD.LeitorDaFormula

def slice (sample : ℚ) : Fin 16 :=
  let tick : ℤ := ⌊16*sample+1/2⌋
  ⟨(tick % 16).toNat % 16, Nat.mod_lt _ (by decide)⟩

theorem receives (t : Fin 16) (z : ℚ) (j : ℤ)
    (h : |z - (turn t + j)| < 1/32) : slice z = t := by
  obtain ⟨lo,hi⟩ := abs_lt.mp h
  unfold turn at lo hi
  have fl : ⌊16*z + 1/2⌋ = (t.val : ℤ) + 16*j := by
    apply Int.floor_eq_iff.mpr
    push_cast
    constructor <;> linarith
  have ht := t.isLt
  have modq : ((t.val : ℤ) + 16*j) % 16 = (t.val : ℤ) := by omega
  apply Fin.ext
  change (⌊16*z+1/2⌋ % 16).toNat % 16 = t.val
  rw [fl, modq]
  exact Nat.mod_eq_of_lt ht

def fuse (left right : ℚ) : Fin 16 :=
  phaseTag (join (fromPhase (slice left)) (fromPhase (slice right)))

theorem fuse_exact (l r : Key) (a b : ℚ) (i j : ℤ) (x y : Bool)
    (ha : |a - (turn (phaseTag l) + i)| < 1/32)
    (hb : |b - (turn (phaseTag r) + j)| < 1/32) :
    atBit (fromPhase (fuse a b)) x y = true ↔
      ∃ z, atBit l x z = true ∧ atBit r z y = true := by
  simp only [fuse,receives _ _ _ ha,receives _ _ _ hb,phase_roundtrip,join_iff]

theorem same_join (l r : Key) : ChainTape.join l r = join l r := rfl

def keyOf (reg : ChainTape.Reg) := phaseTag (ChainTape.committed reg.acc)

inductive Machine where
  | walk (s : ChainTape.Reg) (src : List Letter)
  | halt (tag : Fin 16)

def step : Machine → Machine
  | .walk s [] => .halt (keyOf s)
  | .walk s (a::w) => .walk (ChainTape.see s a) w
  | .halt t => .halt t

def moved : Machine → Nat
  | .walk _ (_::_) => 1
  | _ => 0

def travel : Nat → Machine → Nat
  | 0,_ => 0
  | k+1,s => moved s + travel k (step s)

theorem full_scan (w : List Letter) (s : ChainTape.Reg) :
    step^[w.length+1] (.walk s w) = .halt (keyOf (w.foldl ChainTape.see s)) ∧
    travel (w.length+1) (.walk s w) = w.length := by
  induction w generalizing s with
  | nil => exact ⟨rfl,rfl⟩
  | cons a xs ih =>
    obtain ⟨endState,count⟩ := ih (ChainTape.see s a)
    constructor
    · change step^[xs.length+1+1] _ = _
      rw [Function.iterate_succ_apply]
      exact endState
    · change 1 + travel (xs.length+1) (.walk (ChainTape.see s a) xs) = xs.length+1
      omega

/-- Both endpoints remain addressable after transmission. Every letter of
the underlying flat CNF is consumed before the finite tag is returned. -/
theorem raw_to_phase {n : Nat} {l r : Fin n} {p : CNF n} (h : ChainTape.Path l p r) :
    let w := original p
    let m := Machine.walk (ChainTape.clean ChainTape.freshKey) w
    ∃ t, step^[w.length+1] m = .halt t ∧ travel (w.length+1) m = w.length ∧
      ∀ (z : ℚ) (j : ℤ), |z - (turn t + j)| < 1/32 → ∀ u v,
        atBit (fromPhase (slice z)) u v = true ↔ ChainTape.visible p l r u v := by
  dsimp only
  obtain ⟨a,run,_,valid⟩ := ChainTape.path_table h
  obtain ⟨endState,moves⟩ := full_scan (original p) (ChainTape.clean ChainTape.freshKey)
  rw [run] at endState
  refine ⟨_,endState,moves,?_⟩
  intro z j hz u v
  rw [receives _ _ _ hz]
  change atBit (fromPhase (phaseTag (ChainTape.committed a))) u v = true ↔ _
  rw [phase_roundtrip]
  exact valid u v

end Codex.SinglePhase

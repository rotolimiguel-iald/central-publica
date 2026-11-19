import TGLExt.DuasPassagens

/-! A guard that can be run over the input, visiting only the unary addresses
present there. Unvisited cells retain the blank profile and pass the test. -/
set_option autoImplicit false
namespace Codex.ProfileGuard
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.SignProfile Codex.TwoSweeps

def guardOp : Op Bool :=
  ⟨fun zero _ _ cell q => (cell, q && (zero || allowed cell)), id⟩

def eligible {n : Nat} (t : Bank) (l : Literal n) :=
  (l.var.val == 0) || allowed (t l.var.val)

def visited {n : Nat} (p : CNF n) (j : Nat) : Prop :=
  ∃ c ∈ p, ∃ l ∈ c, l.var.val = j

theorem unvisited_blank {n : Nat} (p : CNF n) (j : Nat)
    (missing : ¬ visited p j) : profile p j = blank := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have noSign (b : Bool) : occurs j b c = false := by
      apply List.any_eq_false.mpr
      intro l hl
      have diff : l.var.val ≠ j := fun e => missing ⟨c,by simp,l,hl,e⟩
      simp [diff]
    have tail : ¬ visited p j := by
      rintro ⟨d,hd,l,hl,e⟩
      exact missing ⟨d,List.mem_cons_of_mem _ hd,l,hl,e⟩
    simp [profile,flags,noSign,ih tail,blank,join]

private theorem onLiteral {n : Nat} (l : Literal n) (u : Bool) (s : St Bool) :
    applyLit guardOp l u s = ⟨s.bank,s.control && eligible s.bank l,false,0⟩ := by
  simp [applyLit,guardOp,eligible]

private theorem onList {n : Nat} (ls : Clausula n) (s : St Bool) :
    (lits guardOp ls s).bank = s.bank ∧
    (lits guardOp ls s).control = (s.control && ls.all (eligible s.bank)) := by
  induction ls generalizing s with
  | nil => simp [lits]
  | cons l ls ih =>
    rw [lits,onLiteral]
    obtain ⟨bank,value⟩ := ih ⟨s.bank,s.control && eligible s.bank l,false,0⟩
    exact ⟨bank,by simpa [Bool.and_assoc] using value⟩

private theorem onClauses {n : Nat} (p : CNF n) (s : St Bool) :
    (clauses guardOp p s).control =
      (s.control && p.all (fun c => c.all (eligible s.bank))) := by
  induction p generalizing s with
  | nil => simp [clauses]
  | cons c p ih =>
    obtain ⟨bank,value⟩ := onList c s
    rw [clauses,ih]
    change ((lits guardOp c s).control &&
        p.all (fun d => d.all (eligible (lits guardOp c s).bank))) = _
    rw [bank,value,List.all_cons,Bool.and_assoc]

theorem letters_guard {n : Nat} (p : CNF n) (t : Bank) :
    (scan guardOp (original p) (start t true)).control =
      p.all (fun c => c.all (eligible t)) := by
  rw [raw_clauses _ _ _ rfl,onClauses]
  simp [start]

theorem guard_exact {n : Nat} (p : CNF (n+1)) :
    (scan guardOp (original p) (start (profile p) true)).control = true ↔ covered p := by
  rw [letters_guard,List.all_eq_true]
  constructor
  · intro h j nz
    by_cases v : visited p j.val
    · obtain ⟨c,hc,l,hl,e⟩ := v
      have ok := List.all_eq_true.mp (h c hc) l hl
      simpa [eligible,e,nz] using ok
    · rw [unvisited_blank _ _ v]
      rfl
  · intro h c hc
    apply List.all_eq_true.mpr
    intro l hl
    by_cases z : l.var.val = 0
    · simp [eligible,z]
    · simp [eligible,h l.var z]

end Codex.ProfileGuard

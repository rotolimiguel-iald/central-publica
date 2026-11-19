import TGLExt.CacheDeRamos

/-! A signed mark certifies any later clause containing that mark.
If every live key supplies such a certificate, retain the entire layer. -/
set_option autoImplicit false
namespace Codex.CoverCache
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.BranchCache
variable {n : Nat}

def hasMark (s : Key n) (c : Clausula n) : Bool :=
  c.any (fun l => decide ((l.var,l.pos) ∈ s))

def covers (rows : Layer n) (c : Clausula n) : Bool :=
  decide ((rows.filter (fun s => hasMark s c = false)) = ∅)

def step (rows : Layer n) (c : Clausula n) :=
  if covers rows c then rows else advance rows c

private theorem forced {s : Key n} {c : Clausula n} {x : Fin n → Bool}
    (h : hasMark s c = true) (hx : fits s x) : satisfeita c x = true := by
  obtain ⟨l,hl,mem⟩ := List.any_eq_true.mp h
  exact List.any_eq_true.mpr ⟨l,hl,by simpa [Literal.vale] using hx _ (of_decide_eq_true mem)⟩

theorem step_exact (rows : Layer n) (c : Clausula n) (x : Fin n → Bool) :
    models (step rows c) x ↔ models rows x ∧ satisfeita c x = true := by
  unfold step
  split
  next h =>
    constructor
    · intro holds
      obtain ⟨s,hs,hx⟩ := holds
      have all : ∀ t ∈ rows, hasMark t c = true := by simpa [covers,Finset.filter_eq_empty_iff] using h
      have found := all s hs
      exact ⟨⟨s,hs,hx⟩,forced found hx⟩
    · exact And.left
  next => exact advance_models rows c x

def scan : CNF n → Layer n → Layer n
  | [], rows => rows
  | c::p, rows => scan p (step rows c)

theorem scan_exact (p : CNF n) (rows : Layer n) (x : Fin n → Bool) :
    models (scan p rows) x ↔ models rows x ∧ passes p x = true := by
  induction p generalizing rows with
  | nil => simp [scan,passes]
  | cons c p ih => rw [scan,ih,step_exact]; simp [passes,and_assoc]

/-- Counts only extensions after paying separately for the membership probes. -/
def extensions : CNF n → Layer n → Nat
  | [], _ => 0
  | c::p, rows =>
      (if covers rows c then 0 else rows.card*c.length) + extensions p (step rows c)

def membershipBudget : CNF n → Layer n → Nat
  | [], _ => 0
  | c::p, rows => rows.card*c.length + membershipBudget p (step rows c)

open Codex.LiteralSearchCost
theorem all_copies_covered : covers firstLayer choiceClause = true := by decide

private theorem first_step : step (initial 4) choiceClause = firstLayer := by
  have h : covers (initial 4) choiceClause = false := by decide
  simp [step,h,firstLayer]

private theorem repeat_counts (k : Nat) :
    extensions (delayed k) firstLayer = extensions suffix firstLayer ∧
    membershipBudget (delayed k) firstLayer = 4*k + membershipBudget suffix firstLayer := by
  induction k with
  | zero => simp [delayed]
  | succ k ih =>
    have stay : step firstLayer choiceClause = firstLayer := by simp [step,all_copies_covered]
    have a : firstLayer.card = 2 := by decide
    have b : choiceClause.length = 2 := rfl
    constructor
    · change (if covers firstLayer choiceClause then 0 else firstLayer.card * choiceClause.length)
          + extensions (delayed k) (step firstLayer choiceClause) = _
      simpa only [all_copies_covered,if_true,Nat.zero_add,stay] using
        (show extensions (delayed k) firstLayer = extensions suffix firstLayer from ih.1)
    · change firstLayer.card * choiceClause.length +
          membershipBudget (delayed k) (step firstLayer choiceClause) = _
      rw [stay,a,b,ih.2]
      omega

/-- Every copy after the first costs only a scan for cached certificates.
The two tail clauses are still processed by the actual general rule. -/
theorem delayed_cached (k : Nat) :
    extensions (delayed (k+1)) (initial 4) = 12 ∧
    membershipBudget (delayed (k+1)) (initial 4) = 4*k+12 := by
  have e := repeat_counts k
  have failed : covers (initial 4) choiceClause = false := by decide
  have a : (initial 4).card = 1 := by decide
  have b : choiceClause.length = 2 := rfl
  change ((if covers (initial 4) choiceClause then 0 else (initial 4).card * choiceClause.length)
      + extensions (delayed k) (step (initial 4) choiceClause) = _) ∧
    ((initial 4).card * choiceClause.length +
      membershipBudget (delayed k) (step (initial 4) choiceClause) = _)
  simp only [failed,first_step,e.1,e.2,a,b,Bool.false_eq_true,if_false]
  have et : extensions suffix firstLayer = 10 := by decide
  have mt : membershipBudget suffix firstLayer = 10 := by decide
  constructor <;> omega


/-- Public reading of an arbitrary layer. Each candidate assignment is
reconstructed from its own marks and the requested pivot value. -/
theorem query_exact (rows : Layer n) (i : Fin n) (b : Bool) :
    branch rows i b = true ↔ ∃ x, x i = b ∧ models rows x := by
  unfold BranchCache.branch
  rw [decide_eq_true_eq]
  constructor
  · rintro ⟨s,mem⟩
    obtain ⟨hs,fit⟩ := Finset.mem_filter.mp mem
    exact ⟨build s i b,by simp [build],s,hs,by
      simpa [keyFits,Finset.filter_eq_empty_iff,fits] using fit⟩
  · rintro ⟨x,atPivot,s,hs,fit⟩
    refine ⟨s,Finset.mem_filter.mpr ⟨hs,?_⟩⟩
    simp only [keyFits,decide_eq_true_eq,Finset.filter_eq_empty_iff,not_not]
    rintro ⟨j,t⟩ hj
    have e : x j = t := fit _ hj
    by_cases same : j = i
    · subst j
      simpa [build] using atPivot.symm.trans e
    · cases t
      · have noPos : (j,true) ∉ s := fun pos => by
          have a : x j = true := fit _ pos
          simp [e] at a
        simp [build,same,noPos]
      · simp [build,same,hj]

def read (p : CNF n) (i : Fin n) :=
  let rows := scan p (initial n)
  (branch rows i false,branch rows i true)

theorem read_exact (p : CNF n) (i : Fin n) (b : Bool) :
    (if b then (read p i).2 else (read p i).1) = true ↔ ∃ x, x i = b ∧ passes p x = true := by
  have model (x : Fin n → Bool) : models (scan p (initial n)) x ↔ passes p x = true := by
    rw [scan_exact]
    simp [initial,models,fits]
  cases b <;> simp only [read,Bool.false_eq_true,if_false,if_true,query_exact,model]


open TGLExt.Psibit TGLExt.OPsiBitDaFormula
/-- The labels are computed from the source. The orbit represents them afterwards. -/
theorem read_as_psibit (p : CNF n) (i : Fin n) :
    let q := read p i
    (q.1 || q.2) = palavraDaFormula p ∧
      ∃ θ : ℝ, (codeAmp θ).word = bitSign q.1 ∧ (codeAmp θ).verb = bitSign q.2 ∧
        decodeAmp (codeAmp θ) = v θ := by
  dsimp only
  constructor
  · apply Bool.eq_iff_iff.mpr
    have lo := read_exact p i false
    have hi := read_exact p i true
    simp only [Bool.false_eq_true,if_false,if_true] at lo hi
    rw [Bool.or_eq_true,lo,hi,a_palavra_e_o_sat,sat_iff]
    constructor
    · rintro (⟨x,_,ok⟩|⟨x,_,ok⟩) <;> exact ⟨x,ok⟩
    · rintro ⟨x,ok⟩
      cases e : x i
      · exact Or.inl ⟨x,e,ok⟩
      · exact Or.inr ⟨x,e,ok⟩
  · have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
    obtain ⟨θ,ha,hb⟩ := the_orbit_visits_all_four_states _ _ (nz (read p i).1) (nz (read p i).2)
    exact ⟨θ,ha,hb,decodeAmp_codeAmp θ⟩

end Codex.CoverCache

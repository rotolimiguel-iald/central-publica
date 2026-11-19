import TGLExt.CacheDeRamos
import TGLExt.LimiteDoCacheExplicito
import TGLExt.DespachoDeReuso

/-! Growth of the exact signed Finset actually constructed by BranchCache.run. -/
set_option autoImplicit false
namespace Codex.ReachedLayer
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.BranchCache Codex.BranchPresence Codex.ExplicitCache Codex.PolinomioPorEscolha
variable {n k : Nat}

def keyOf (ms : List (Literal n)) : Key n :=
  (ms.map (fun l => (l.var,l.pos))).toFinset

private theorem fits_key (ms : List (Literal n)) (x : Fin n → Bool) :
    fits (keyOf ms) x ↔ Agrees x ms := by
  simp [fits,keyOf,Agrees]

private theorem old_survives {p : CNF n} {ms last : List (Literal n)}
    (path : Reaches p ms last) : ∀ l ∈ ms, l ∈ last := by
  induction path with
  | done => simp
  | step _ _ ih => exact fun l h => ih l (List.mem_cons_of_mem _ h)

private theorem child_of {l : Literal n} {c : Clausula n} {s t : Key n}
    (member : l ∈ c) (extension : t ∈ extend s l) : t ∈ children s c := by
  induction c with
  | nil => simp at member
  | cons a c ih =>
    rcases List.mem_cons.mp member with e|h
    · subst a; exact Finset.mem_union_left _ extension
    · exact Finset.mem_union_right _ (ih h)

/-- Any internally consistent choice path survives the implemented insertion,
conflict check and deduplication of the finite-set cache. -/
theorem reached_key {p : CNF n} {ms last : List (Literal n)}
    (path : Reaches p ms last) {x : Fin n → Bool} (agrees : Agrees x last)
    (rows : Layer n) (start : keyOf ms ∈ rows) : keyOf last ∈ run p rows := by
  induction path generalizing rows with
  | done => exact start
  | @step l c p ms last member path ih =>
    apply ih agrees
    apply Finset.mem_biUnion.mpr
    refine ⟨keyOf ms,start,child_of member ?_⟩
    have h : Agrees x (l::ms) := fun z hz => agrees z (old_survives path z hz)
    have old : fits (keyOf ms) x :=
      (fits_key _ _).mpr (fun z hz => h z (List.mem_cons_of_mem _ hz))
    have lv := h l (List.mem_cons_self)
    have no : (l.var,!l.pos) ∉ keyOf ms := by
      intro opposite
      have bad := old _ opposite
      change x l.var = !l.pos at bad
      rw [lv] at bad
      cases e : l.pos <;> simp [e] at bad
    rw [extend,if_neg no]
    simp [keyOf]

theorem actual_member (f : Fin k → Bool) :
    keyOf (marks f) ∈ run (pairs k true) (initial (2*k)) := by
  apply reached_key (keys_reachable f) (x := row f)
  · apply (marked_iff _ _).mpr
    intro i
    simp [row_value]
  · simp [keyOf,initial]

theorem concrete_bit (f : Fin k → Bool) (i : Fin k) (b : Bool) :
    (addr i b,true) ∈ keyOf (marks f) ↔ f i = b := by
  simp [keyOf,marks,label,List.mem_map,addr_eq]

theorem actual_layer_lower (k : Nat) :
    2^k ≤ (run (pairs k true) (initial (2*k))).card := by
  let rows := run (pairs k true) (initial (2*k))
  let entry (f : Fin k → Bool) : ↥rows := ⟨keyOf (marks f),actual_member f⟩
  have inj : Function.Injective entry := by
    intro f g eq
    have same : keyOf (marks f) = keyOf (marks g) := congrArg Subtype.val eq
    funext i
    have mem := (concrete_bit f i (f i)).mpr rfl
    rw [same] at mem
    exact ((concrete_bit g i _).mp mem).symm
  simpa [rows] using Fintype.card_le_of_injective entry inj

theorem run_append (p q : CNF n) (seed : Layer n) : run (p++q) seed = run q (run p seed) := by
  induction p generalizing seed with
  | nil => rfl
  | cons c p ih => exact ih _

theorem attempts_append (p q : CNF n) (seed : Layer n) :
    attempts (p++q) seed = attempts p seed + attempts q (run p seed) := by
  induction p generalizing seed with
  | nil => simp [attempts,run]
  | cons c p ih => simp only [List.cons_append,attempts,run,ih,Nat.add_assoc]

/-- A nonempty next clause performs at least one actual extension attempt per
distinct row reached, including rows rejected by the conflict check. -/
theorem attempts_after_pairs {c : Clausula (2*k)} (rest : CNF (2*k))
    (h : c ≠ []) : 2^k ≤ attempts (pairs k true ++ c::rest) (initial (2*k)) := by
  rw [attempts_append,attempts]
  have lo := actual_layer_lower k
  have pos : 1 ≤ c.length := List.length_pos_iff.mpr h
  have mul := Nat.mul_le_mul_left (run (pairs k true) (initial (2*k))).card pos
  simp only [Nat.mul_one] at mul
  omega

open Codex.SignProfile Codex.CertifiedRead Codex.SecondRead Codex.ReuseDispatch

private def low (k : Nat) : Fin (2*(k+2)) := ⟨0,by omega⟩
private def middle (k : Nat) : Fin (2*(k+2)) := ⟨1,by omega⟩
private def high (k : Nat) : Fin (2*(k+2)) := ⟨2,by omega⟩

def probePair (k : Nat) (s t : Bool) : Clausula (2*(k+2)) :=
  [⟨low k,s⟩,⟨middle k,t⟩]

def probeTriple (k : Nat) : Clausula (2*(k+2)) :=
  [⟨low k,true⟩,⟨middle k,true⟩,⟨high k,true⟩]

/-- Fixed ternary tail: one genuine ternary clause plus all four binary
polarities. There is no unit and no empty clause. -/
def gateTail (k : Nat) : CNF (2*(k+2)) :=
  [probePair k false false,probePair k false true,probePair k true false,
   probePair k true true,probeTriple k]

def gateInput (k : Nat) := pairs (k+2) true ++ gateTail k

theorem has_ternary (k : Nat) : ∃ c ∈ gateInput k, c.length = 3 :=
  ⟨probeTriple k,List.mem_append_right _ (by simp [gateTail]),rfl⟩

theorem gate_fails (k : Nat) (x : Fin (2*(k+2)) → Bool) :
    passes (gateInput k) x = false := by
  have no : (gateTail k).all (fun c => satisfeita c x) = false := by
    cases a : x (low k) <;> cases b : x (middle k) <;>
      simp [gateTail,probePair,satisfeita,Literal.vale,a,b]
  simp only [gateInput,passes,List.all_append,no,Bool.and_false]

private theorem tail_profile (k : Nat) : profile (gateTail k) 1 = ⟨true,true,false,false⟩ := by
  rfl

private theorem pair_profile {k : Nat} (is : List (Fin (k+2))) :
    profile (is.map (pairClause true) ++ gateTail k) 1 = ⟨true,true,false,false⟩ := by
  induction is with
  | nil => exact tail_profile _
  | cons i is ih =>
    change join (flags (pairClause true i) (singleton (pairClause true i)) 1)
      (profile (is.map (pairClause true) ++ gateTail k) 1) = _
    rw [ih]
    simp [join,flags,pairClause,SignProfile.singleton]

theorem gate_uncovered (k : Nat) : ¬covered (gateInput k) := by
  intro h
  have bad := h (middle k) (by simp [middle])
  change allowed (profile ((List.finRange (k+2)).map (pairClause true) ++ gateTail k) 1) = true at bad
  rw [pair_profile] at bad
  contradiction

private theorem no_branch (k : Nat) (b : Bool) : ¬present (gateInput k) b := by
  rintro ⟨x,_,ok⟩
  rw [gate_fails] at ok
  contradiction

/-- Both actual physical witness readers run out of certificates. The existing
dispatcher therefore selects its computed-key fallback on this family. -/
theorem dispatch_misses (k : Nat) (b : Bool) :
    pickLane (physical (original (gateInput k))) b = none := by
  let p := gateInput k
  have absent : ¬present p b := no_branch k b
  have miss : lane (SecondRead.read (original p)) b = false := by
    cases e : lane (SecondRead.read (original p)) b with
    | false => rfl
    | true => exact (absent (SecondRead.positive_is_sound p b e)).elim
  have guardOff : (readTape (original p)).2 = false := by
    cases g : (readTape (original p)).2 with
    | false => rfl
    | true => exact (gate_uncovered k ((guard_projection p).mp g)).elim
  have old : classify (readTape (original p)) b = none :=
    (unknown_iff _ _).mpr ⟨by rw [witness_projection]; exact miss,guardOff⟩
  have newMiss : lane (ReuseReader.read (original p)) b = false := by
    cases e : lane (ReuseReader.read (original p)) b with
    | false => rfl
    | true => exact (absent (ReuseReader.positive_sound p b e)).elim
  change pickLane (physical (original p)) b = none
  rw [physical_lane,old,newMiss]
  rfl

theorem calls_shared_fallback (k : Nat) :
    physical (original (gateInput k)) = (none,none) ∧
    branches (gateInput k) = BranchCache.read (gateInput k) 0 := by
  have both : physical (original (gateInput k)) = (none,none) :=
    Prod.ext (dispatch_misses k false) (dispatch_misses k true)
  exact ⟨both,by simp only [branches,both,finish]⟩

theorem charged_attempts (k : Nat) :
    2^(k+2) ≤ attempts (gateInput k) (initial _) := by
  exact attempts_after_pairs (k := k+2)
    [probePair k false true,probePair k true false,probePair k true true,probeTriple k]
    (c := probePair k false false) (by simp [probePair])

theorem gate_input_letters (k : Nat) :
    (original (gateInput k)).length ≤ (k+2)*(4*(k+2)+3)+23 := by
  have suffixSize : (original (gateTail k)).length = 23 := by rfl
  have joined : (original (gateInput k)).length =
      (original (pairs (k+2) true)).length + (original (gateTail k)).length := by
    simp [gateInput,original]
  rw [joined,suffixSize]
  exact Nat.add_le_add_right (prefix_letters (k+2) true) _

private theorem prefix_min (k : Nat) : k ≤ (original (pairs k true)).length := by
  have allLists (is : List (Fin k)) : is.length ≤ (original (is.map (pairClause true))).length := by
    induction is with
    | nil => simp
    | cons i is ih =>
      change is.length + 1 ≤ (spellClause (pairClause true i) ++ original (is.map (pairClause true))).length
      rw [List.length_append]
      have pos : 1 ≤ (spellClause (pairClause true i)).length := by simp [spellClause]
      omega
  simpa [pairs] using allLists (List.finRange k)

/-- Superpolynomially many actual key extensions on inputs whose physical
pre-dispatcher certifies neither branch. L counts the complete raw input.
Extension attempts are the operation counted by BranchCache.attempts. -/
theorem no_fixed_attempt_polynomial (C d : Nat) : ∃ k : Nat,
    physical (original (gateInput k)) = (none,none) ∧
    C*((original (gateInput k)).length+1)^d < attempts (gateInput k) (initial _) := by
  classical
  obtain ⟨k,i,h⟩ := exceeds_polynomial (C*46^d) (2*d)
  let listed := ((Finset.univ : Finset (Fin k → Bool)).toList).map marks
  have many := h false listed (by intro f; exact List.mem_map.mpr ⟨f,by simp,rfl⟩)
  have listSize : listed.length = 2^k := by simp [listed]
  rw [listSize] at many
  let oldSize := (original (pairs k true ++ continuation i false)).length
  have joined : oldSize = (original (pairs k true)).length + (original (continuation i false)).length := by
    simp [oldSize,original]
  have prefixLower := prefix_min k
  have oldLower : k ≤ oldSize := by omega
  have newUpper := gate_input_letters k
  have bound : (original (gateInput k)).length+1 ≤ 46*(oldSize+1)^2 := by
    calc
      _ ≤ 46*(k+1)^2 := by nlinarith
      _ ≤ _ := Nat.mul_le_mul_left 46 (Nat.pow_le_pow_left (by omega) _)
  have lg : 2^k ≤ 2^(k+2) := Nat.pow_le_pow_right (by decide) (by omega)
  refine ⟨k,(calls_shared_fallback k).1,?_⟩
  calc
    _ ≤ C*(46*(oldSize+1)^2)^d := Nat.mul_le_mul_left C (Nat.pow_le_pow_left bound _)
    _ = (C*46^d)*(oldSize+1)^(2*d) := by rw [mul_pow,pow_mul]; ring
    _ < 2^k := many
    _ ≤ _ := lg.trans (charged_attempts k)

end Codex.ReachedLayer

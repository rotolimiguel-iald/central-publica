import TGLExt.AtualizaONome
import TGLExt.PolinomioPorEscolha

/-! A flat prefix chooses one of two positive literals in each disjoint pair.
The suffix contains a negative clause on each pair, followed by one unit.
All marked addresses remain live and have distinguishable continuation queries. -/
set_option autoImplicit false
namespace Codex.ExplicitCache
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.BranchPresence
variable {k : Nat}

def addr (i : Fin k) (b : Bool) : Fin (2*k) :=
  ⟨2*i.val + (if b then 1 else 0), by have hi := i.isLt; split <;> omega⟩

theorem addr_eq (i j : Fin k) (b c : Bool) : addr i b = addr j c ↔ i = j ∧ b = c := by
  constructor
  · intro h
    have v := congrArg Fin.val h
    cases b <;> cases c <;> simp [addr] at v ⊢ <;> first | exact Fin.ext (by omega) | omega
  · rintro ⟨rfl,rfl⟩
    rfl

def label (i : Fin k) (b s : Bool) : Literal (2*k) := ⟨addr i b,s⟩
def pairClause (s : Bool) (i : Fin k) : Clausula (2*k) := [label i false s,label i true s]
def pairs (k : Nat) (s : Bool) : CNF (2*k) := (List.finRange k).map (pairClause s)

def marks (f : Fin k → Bool) : List (Literal (2*k)) :=
  ((List.finRange k).map (fun i => label i (f i) true)).reverse

/-- Exactly the choice transitions used by search, without its short circuit. -/
inductive Reaches {n : Nat} :
    CNF n → List (Literal n) → List (Literal n) → Prop where
  | done (ms) : Reaches [] ms ms
  | step {l c p ms result} : l ∈ c → Reaches p (l::ms) result → Reaches (c::p) ms result

private theorem reachesAlong (is : List (Fin k)) (f : Fin k → Bool) (ms : List (Literal (2*k))) :
    Reaches (is.map (pairClause true)) ms
      ((is.map (fun i => label i (f i) true)).reverse ++ ms) := by
  induction is generalizing ms with
  | nil => exact Reaches.done _
  | cons i is ih =>
    simp only [List.map_cons,List.reverse_cons,List.append_assoc,List.singleton_append]
    apply Reaches.step (l := label i (f i) true)
    · cases f i <;> simp [pairClause]
    · exact ih _

theorem keys_reachable (f : Fin k → Bool) : Reaches (pairs k true) [] (marks f) := by
  simpa only [pairs,marks,List.append_nil] using reachesAlong (List.finRange k) f []

theorem marked_iff (x : Fin (2*k) → Bool) (f : Fin k → Bool) :
    Agrees x (marks f) ↔ ∀ i, x (addr i (f i)) = true := by
  simp [Agrees,marks,label]

theorem pair_condition (x : Fin (2*k) → Bool) (s : Bool) :
    passes (pairs k s) x = true ↔ ∀ i : Fin k, x (addr i false) = s ∨ x (addr i true) = s := by
  simp [passes,pairs,List.all_eq_true,pairClause,satisfeita,label,Literal.vale]

def row (f : Fin k → Bool) (v : Fin (2*k)) : Bool :=
  (List.finRange k).any (fun j => addr j (f j) == v)

theorem row_value (f : Fin k → Bool) (i : Fin k) (b : Bool) :
    row f (addr i b) = (f i == b) := by
  apply Bool.eq_iff_iff.mpr
  simp [row,List.any_eq_true,addr_eq]

def continuation (i : Fin k) (b : Bool) : CNF (2*k) :=
  pairs k false ++ [[label i b true]]

private theorem needs {i : Fin k} {b : Bool} (x : Fin (2*k) → Bool) :
    passes (continuation i b) x = true ↔
      passes (pairs k false) x = true ∧ x (addr i b) = true := by
  simp [continuation,passes,satisfeita,label,Literal.vale]

theorem live_address (i j : Fin k) (b c : Bool) :
    ∃ clause ∈ continuation j c, ∃ l ∈ clause, l.var = addr i b := by
  refine ⟨pairClause false i,List.mem_append_left _ (List.mem_map.mpr ⟨i,by simp,rfl⟩),
    label i b false,?_,rfl⟩
  cases b <;> simp [pairClause]

theorem no_mark_forgotten (f : Fin k → Bool) (i : Fin k) (b : Bool)
    (l : Literal (2*k)) (h : l ∈ marks f) :
    ∃ clause ∈ continuation i b, ∃ lit ∈ clause, lit.var = l.var := by
  obtain ⟨j,_,rfl⟩ := List.mem_map.mp (List.mem_reverse.mp h)
  exact live_address j i (f j) b

/-- With these marks a completion must use exactly the chosen address in
each pair. A unit therefore probes any specified coordinate of the key. -/
theorem continuation_reads_key (f : Fin k → Bool) (i : Fin k) (b : Bool) :
    Compatible (continuation i b) (marks f) ↔ f i = b := by
  constructor
  · rintro ⟨x,h,agrees⟩
    obtain ⟨pairsOk,picked⟩ := (needs x).mp h
    have exclusion := (pair_condition x false).mp pairsOk i
    have selected := (marked_iff x f).mp agrees i
    cases hi : f i <;> cases b <;> simp_all
  · rintro rfl
    refine ⟨row f,(needs _).mpr ⟨(pair_condition _ _).mpr ?_,?_⟩,(marked_iff _ _).mpr ?_⟩
    · intro j
      cases s : f j <;> simp [row_value,s]
    · simp [row_value]
    · intro j
      simp [row_value]

theorem distinguishable {f g : Fin k → Bool} (ne : f ≠ g) :
    ∃ i : Fin k, Compatible (continuation i (f i)) (marks f) ∧
      ¬ Compatible (continuation i (f i)) (marks g) := by
  classical
  by_contra! no
  apply ne
  funext i
  exact ((continuation_reads_key g i (f i)).mp
    (no i ((continuation_reads_key f i (f i)).mpr rfl))).symm

/-- Even if stored rows use opaque encodings, a separately indexed row for
each choice must distinguish all choices when its state alone answers probes.
This counts available row identities, not bits of an arbitrary encoding. -/
theorem distinct_row_count (slots : Nat) (encode : (Fin k → Bool) → Fin slots)
    (query : Fin slots → Fin k → Bool → Prop)
    (correct : ∀ f i b, query (encode f) i b ↔ Compatible (continuation i b) (marks f)) :
    2^k ≤ slots := by
  have inj : Function.Injective encode := by
    intro f g h
    funext i
    have allowed := (correct f i (f i)).mpr ((continuation_reads_key f i _).mpr rfl)
    rw [h] at allowed
    exact ((continuation_reads_key g i _).mp ((correct g i _).mp allowed)).symm
  simpa using Fintype.card_le_of_injective encode inj

/-- An actual materialized list containing all these keys has at least 2^k
entries. Every such list traversal charges at least one cell per entry. -/
theorem explicit_cache_length (cache : List (List (Literal (2*k))))
    (materialized : ∀ f : Fin k → Bool, marks f ∈ cache) : 2^k ≤ cache.length := by
  classical
  have located (f : Fin k → Bool) : ∃ idx : Fin cache.length, cache.get idx = marks f :=
    List.mem_iff_get.mp (materialized f)
  choose index indexed using located
  apply distinct_row_count cache.length index
    (fun idx i b => Compatible (continuation i b) (cache.get idx))
  intro f i b
  rw [indexed]

private theorem pair_letters (i : Fin k) (s : Bool) :
    (spellClause (pairClause s i)).length ≤ 4*k+3 := by
  simp [spellClause,pairClause,label,spell,addr]
  have bound := i.isLt
  omega

private theorem lettersAlong (is : List (Fin k)) (s : Bool) :
    (original (is.map (pairClause s))).length ≤ is.length*(4*k+3) := by
  induction is with
  | nil => simp [original]
  | cons i is ih =>
    change (spellClause (pairClause s i) ++ original (is.map (pairClause s))).length ≤ _
    simp only [List.length_append,List.length_cons,Nat.succ_mul is.length (4*k+3)]
    have h := pair_letters i s
    omega

theorem prefix_letters (k : Nat) (s : Bool) :
    (original (pairs k s)).length ≤ k*(4*k+3) := by
  simpa [pairs] using lettersAlong (List.finRange k) s

/-- Length includes the positive prefix, the full negative suffix keeping
each pair live, and the final distinguishing unit, all in unary spelling. -/
theorem full_probe_letters (i : Fin k) (b : Bool) :
    (original (pairs k true ++ continuation i b)).length ≤ 2*(k*(4*k+3)) + (2*k+2) := by
  have split (s t : CNF (2*k)) :
      (original (s++t)).length = (original s).length + (original t).length := by simp [original]
  rw [split,continuation,split]
  have a := prefix_letters k true
  have c := prefix_letters k false
  have u : (original [[label i b true]]).length ≤ 2*k+2 := by
    simp [original,spellClause,spell,label]
  omega

/-- Charge at least one work-tape cell per separately materialized key.
An implementation can also charge the full length of its row encoding. -/
theorem explicit_storage_cells (cache : List (List (Literal (2*k))))
    (materialized : ∀ f : Fin k → Bool, marks f ∈ cache)
    (width : List (Literal (2*k)) → Nat) (positive : ∀ row ∈ cache, 1 ≤ width row) :
    2^k ≤ (cache.map width).sum := by
  apply (explicit_cache_length cache materialized).trans
  clear materialized
  induction cache with
  | nil => simp
  | cons r rs ih =>
    have one := positive r (by simp)
    have tail := ih (fun a h => positive a (List.mem_cons_of_mem _ h))
    simp only [List.length_cons,List.map_cons,List.sum_cons]
    omega

private theorem square_exp (a : Nat) : (a+4)^2 ≤ 2^(a+4) := by
  induction a with
  | zero => decide
  | succ a ih =>
    calc
      (a+1+4)^2 ≤ (a+1+4)^2+(a^2+6*a+7) := Nat.le_add_right _ _
      _ = 2*(a+4)^2 := by ring
      _ ≤ 2*2^(a+4) := Nat.mul_le_mul_left 2 ih
      _ = 2^(a+4)*2 := Nat.mul_comm _ _
      _ = 2^(a+1+4) := (pow_succ (2:Nat) (a+4)).symm

set_option maxHeartbeats 700000 in
/-- Every fixed polynomial in the complete unary input length is exceeded
by the explicit cache for a member of this family. -/
theorem exceeds_polynomial (C d : Nat) :
    ∃ (k : Nat) (i : Fin k), ∀ (b : Bool) (cache : List (List (Literal (2*k)))),
      (∀ f : Fin k → Bool, marks f ∈ cache) →
        C*((original (pairs k true ++ continuation i b)).length+1)^d < cache.length := by
  let a := 8*(C+d+1)
  let s := a+4
  let k := 2^s
  have kp : 0 < k := by dsimp [k]; positivity
  let i : Fin k := ⟨0,kp⟩
  refine ⟨k,i,?_⟩
  intro b cache materialized
  have sq : k ≤ k^2 := by
    simpa only [Nat.mul_one,pow_two] using (Nat.mul_le_mul_left k kp)
  have letters := full_probe_letters i b
  have size : (original (pairs k true ++ continuation i b)).length+1 ≤ 32*k^2 := by
    nlinarith
  have coeff : 32*k^2 = 2^(5+2*s) := by
    dsimp [k]
    rw [Nat.mul_comm 2 s,pow_add (2:Nat) 5 (s*2),pow_mul (2:Nat) s 2]
    norm_num
  rw [coeff] at size
  have small : C+(5+2*s)*d < s^2 := by dsimp [s,a]; nlinarith
  have expo : C+(5+2*s)*d < k := lt_of_lt_of_le small (square_exp a)
  calc
    _ ≤ 2^C*(2^(5+2*s))^d := Nat.mul_le_mul C.lt_two_pow_self.le (Nat.pow_le_pow_left size _)
    _ = 2^C*2^((5+2*s)*d) := congrArg (fun z : Nat => 2^C*z) (pow_mul (2:Nat) (5+2*s) d).symm
    _ = 2^(C+(5+2*s)*d) := (pow_add (2:Nat) C ((5+2*s)*d)).symm
    _ < 2^k := pow_lt_pow_right₀ (by decide : 1 < (2:Nat)) expo
    _ ≤ _ := explicit_cache_length cache materialized

end Codex.ExplicitCache

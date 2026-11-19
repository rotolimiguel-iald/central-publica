import TGLExt.CustoDaBuscaLiteral

/-! Existentially eliminate a pivot once, preserving the same outside
assignment on both branches. For binary clauses the resulting cache has a
quadratic universe of keys. This module counts keys, not tape moves. -/
set_option autoImplicit false
namespace Codex.PairElimination
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
variable {n : Nat}
local instance : DecidableEq (Literal n) := fun a b => by
  cases a with | mk i s =>
    cases b with | mk j t =>
      exact decidable_of_iff (i = j ∧ s = t) (by simp)

def assign (x : Fin n → Bool) (v : Fin n) (b : Bool) (i : Fin n) :=
  if i = v then b else x i

def used (v : Fin n) (c : Clausula n) := c.any (fun l => l.var == v)
def hit (v : Fin n) (b : Bool) (c : Clausula n) :=
  c.any (fun l => l.var == v && l.pos == b)
def cut (v : Fin n) (c : Clausula n) := c.filter (fun l => !(l.var == v))

private theorem read_cut (v : Fin n) (b : Bool) (c : Clausula n) (x : Fin n → Bool) :
    satisfeita c (assign x v b) = (hit v b c || satisfeita (cut v c) x) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    by_cases h : l.var = v
    · change (l.vale (assign x v b) || satisfeita c (assign x v b)) = _ 
      simp only [ih]
      cases b <;> cases e : l.pos <;>
        simp [Literal.vale,assign,h,e,hit,cut,satisfeita,List.any_cons]
    · change (l.vale (assign x v b) || satisfeita c (assign x v b)) = _
      simp only [ih]
      simp [Literal.vale,assign,h,beq_eq_false_iff_ne.mpr h,hit,cut,satisfeita,Bool.or_left_comm]

private theorem untouched (v : Fin n) (c : Clausula n) (h : used v c = false) :
    cut v c = c := by
  simpa [used,cut] using h

private theorem hit_used (v : Fin n) (b : Bool) (c : Clausula n)
    (h : hit v b c = true) : used v c = true := by
  obtain ⟨l,hl,hh⟩ := List.any_eq_true.mp h
  have t : (l.var == v) = true ∧ (l.pos == b) = true := by simpa only [Bool.and_eq_true] using hh
  exact List.any_eq_true.mpr ⟨l,hl,t.1⟩

def fixed (v : Fin n) (p : CNF n) := p.filter (fun c => !(used v c))
def arm (v : Fin n) (b : Bool) (p : CNF n) :=
  (p.filter (fun c => used v c && !(hit v b c))).map (cut v)

private theorem branch_spec (v : Fin n) (b : Bool) (p : CNF n) (x : Fin n → Bool) :
    passes p (assign x v b) = (passes (fixed v p) x && passes (arm v b p) x) := by
  induction p with
  | nil => rfl
  | cons c p ih =>
    have hc := read_cut v b c x
    change (satisfeita c (assign x v b) && passes p (assign x v b)) = _
    change satisfeita c (assign x v b) = _ at hc
    rw [hc,ih]
    cases u : used v c <;> cases h : hit v b c
    · have eqc := untouched v c u
      simp [fixed,arm,passes,u,h,eqc,Bool.and_assoc]
    · have contra := hit_used v b c h
      simp [u] at contra
    · simp [fixed,arm,passes,u,h]
      grind
    · simp [fixed,arm,passes,u,h]


def join (p q : CNF n) := p.flatMap (fun a => q.map (fun b => a ++ b))

private theorem join_spec (p q : CNF n) (x : Fin n → Bool) :
    passes (join p q) x = (passes p x || passes q x) := by
  apply Bool.eq_iff_iff.mpr
  simp [passes,join,satisfeita,List.all_eq_true,List.any_append]
  grind

def eliminate (v : Fin n) (p : CNF n) :=
  fixed v p ++ join (arm v false p) (arm v true p)

/-- Both arms refer to exactly the same values outside the pivot. -/
theorem eliminate_exact (v : Fin n) (p : CNF n) (x : Fin n → Bool) :
    passes (eliminate v p) x = (passes p (assign x v false) || passes p (assign x v true)) := by
  rw [branch_spec,branch_spec]
  have e : passes (eliminate v p) x =
    (passes (fixed v p) x && passes (join (arm v false p) (arm v true p)) x) := by
    simp [eliminate,passes,List.all_append]
  rw [e,join_spec]
  grind

def Binary (p : CNF n) := ∀ c ∈ p, c.length ≤ 2

private theorem shorter (v : Fin n) (c : Clausula n) (h : used v c = true) :
    (cut v c).length < c.length := by
  induction c with
  | nil => contradiction
  | cons l c ih =>
    by_cases e : l.var = v
    · have lim := List.length_filter_le (fun l : Literal n => !(l.var == v)) c
      simpa [cut,e] using (Nat.lt_succ_of_le lim)
    · have ht : used v c = true := by simpa only [used,List.any_cons,beq_eq_false_iff_ne.mpr e,Bool.false_or] using h
      simpa [cut,e] using ih ht

private theorem arm_short {v : Fin n} {p : CNF n} (h : Binary p)
    {b : Bool} {c : Clausula n} (hc : c ∈ arm v b p) : c.length ≤ 1 := by
  obtain ⟨d, hd, rfl⟩ := List.mem_map.mp hc
  obtain ⟨hp,hb⟩ := List.mem_filter.mp hd
  have hb' : used v d = true ∧ (!(hit v b d)) = true := by simpa only [Bool.and_eq_true] using hb
  have sm := shorter v d hb'.1
  have := h d hp
  omega

theorem binary_closed (v : Fin n) (p : CNF n) (h : Binary p) : Binary (eliminate v p) := by
  intro c hc
  rcases List.mem_append.mp hc with a|a
  · exact h c (List.mem_filter.mp a).1
  · obtain ⟨d,hd,t⟩ := List.mem_flatMap.mp a
    obtain ⟨e,he,rfl⟩ := List.mem_map.mp t
    have := arm_short h hd
    have := arm_short h he
    simp only [List.length_append]
    omega

def alphabet (n : Nat) : List (Literal n) :=
  (List.finRange n).flatMap (fun i => [⟨i,false⟩, ⟨i,true⟩])
def keys (n : Nat) : CNF n :=
  [[]] ++ (alphabet n).map (fun a => [a]) ++
    (alphabet n).flatMap (fun a => (alphabet n).map (fun b => [a,b]))
def pack (p : CNF n) : CNF n := (keys n).filter (fun c => decide (c ∈ p))

private theorem alphabet_full (a : Literal n) : a ∈ alphabet n := by
  obtain ⟨i,b⟩ := a
  cases b <;> simp [alphabet,List.mem_flatMap]

private theorem keys_full (c : Clausula n) (h : c.length ≤ 2) : c ∈ keys n := by
  cases c with
  | nil => simp [keys]
  | cons a t =>
    cases t with
    | nil => simp [keys,List.mem_map,alphabet_full]
    | cons b t =>
      cases t with
      | nil =>
        apply List.mem_append_right
        exact List.mem_flatMap.mpr ⟨a,alphabet_full _,List.mem_map.mpr ⟨b,alphabet_full _,rfl⟩⟩
      | cons _ _ => simp at h

private theorem regular_length {α β : Type} (ls : List α) (f : α → List β) (m : Nat)
    (h : ∀ a, (f a).length = m) : (ls.flatMap f).length = ls.length*m := by
  induction ls with
  | nil => simp
  | cons a ls ih => simp [ih,h,Nat.succ_mul,Nat.add_comm]

theorem key_count (n : Nat) : (keys n).length = 1+2*n+(2*n)^2 := by
  have a : (alphabet n).length = n*2 := by
    unfold alphabet
    rw [regular_length _ _ 2 (by intro; rfl)]
    simp
  unfold keys
  rw [List.length_append,List.length_append,regular_length _ _ (n*2) (by simp [a])]
  simp [a,pow_two,Nat.mul_comm]

theorem pack_bound (p : CNF n) : (pack p).length ≤ 1+2*n+(2*n)^2 := by
  rw [← key_count]
  apply List.length_filter_le

theorem pack_exact (p : CNF n) (h : Binary p) (x : Fin n → Bool) :
    passes (pack p) x = passes p x := by
  apply Bool.eq_iff_iff.mpr
  simp [pack,passes,List.all_eq_true]
  grind [keys_full,Binary]


/-- Quantification over the eliminated coordinates at a fixed outside assignment. -/
def outside (vs : List (Fin n)) (x y : Fin n → Bool) :=
  ∀ i, i ∉ vs → y i = x i

def reduce : List (Fin n) → CNF n → CNF n
  | [], p => p
  | v :: vs, p => reduce vs (pack (eliminate v p))

private theorem packed_binary (p : CNF n) (h : Binary p) : Binary (pack p) :=
  fun c hc => h c (of_decide_eq_true (List.mem_filter.mp hc).2)

theorem reduce_exact (vs : List (Fin n)) (p : CNF n) (h : Binary p) (x : Fin n → Bool) :
    passes (reduce vs p) x = true ↔ ∃ y, outside vs x y ∧ passes p y = true := by
  induction vs generalizing p x with
  | nil =>
    constructor
    · intro ok
      exact ⟨x,fun _ _ => rfl,ok⟩
    · rintro ⟨y,agree,ok⟩
      have eq : y = x := funext (fun i => agree i (by simp))
      simpa [reduce,eq] using ok
  | cons v vs ih =>
    simp only [reduce]
    have bin := binary_closed v p h
    rw [ih _ (packed_binary _ bin)]
    constructor
    · rintro ⟨y,agree,ok⟩
      rw [pack_exact _ bin,eliminate_exact,Bool.or_eq_true] at ok
      have ext (b : Bool) : outside (v::vs) x (assign y v b) := by
        intro i hi
        simp only [List.mem_cons,not_or] at hi
        simpa [assign,hi.1] using agree i hi.2
      rcases ok with lo|hi
      · exact ⟨_,ext false,lo⟩
      · exact ⟨_,ext true,hi⟩
    · rintro ⟨y,agree,ok⟩
      let z := assign y v (x v)
      have ext : outside vs x z := by
        intro i hi
        by_cases eq : i = v
        · simp [z,assign,eq]
        · exact (if_neg eq).trans (agree i (by simpa [eq] using hi))
      have back : assign z v (y v) = y := by
        funext i
        by_cases eq : i = v <;> simp [assign,z,eq]
      refine ⟨z,ext,?_⟩
      rw [pack_exact _ bin,eliminate_exact,Bool.or_eq_true]
      have choice : passes p (assign z v (y v)) = true := by rw [back]; exact ok
      cases bit : y v
      · exact Or.inl (by simpa only [bit] using choice)
      · exact Or.inr (by simpa only [bit] using choice)

def binaryDecision (p : CNF n) := passes (reduce (List.finRange n) p) (fun _ => false)

theorem binary_decision_correct (p : CNF n) (h : Binary p) :
    binaryDecision p = TGLExt.OPsiBitDaFormula.palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  unfold binaryDecision
  rw [reduce_exact _ _ h,TGLExt.OPsiBitDaFormula.a_palavra_e_o_sat,sat_iff]
  simp [outside]

end Codex.PairElimination

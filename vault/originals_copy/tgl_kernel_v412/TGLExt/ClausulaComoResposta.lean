import TGLExt.PolinomioPorEscolha
import TGLExt.CadeiasDeBolsas

/-! A proposal names a complete valuation. A negative reply contains one
original pending clause, with its literals and signs. The protocol counts
proposal calls and transmitted clause letters. Its bounds exclude the cost
of producing a proposal or certifying unsatisfiability of the left block. -/
set_option autoImplicit false
namespace Codex.ClauseReply
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha (original spellClause)
variable {n : Nat}
abbrev Assignment (n : Nat) := Fin n → Bool
abbrev Proposer (n : Nat) := CNF n → Option (Assignment n)

/-- Return the violated clause and the remaining pending list in its
original order. Equal occurrences are allowed; exactly one is removed. -/
def inspect (x : Assignment n) : CNF n → Option (Clausula n × CNF n)
  | [] => none
  | c :: q =>
    if satisfeita c x then
      (inspect x q).map (fun (d, rest) => (d, c :: rest))
    else some (c, q)

theorem inspect_none (x : Assignment n) (q : CNF n) :
    inspect x q = none ↔ passes q x = true := by
  induction q with
  | nil => simp [inspect, passes]
  | cons c q ih =>
    cases h : satisfeita c x with
    | false => simp [inspect, passes, h]
    | true => simpa [inspect, passes, h] using ih

theorem inspect_some {x : Assignment n} {q : CNF n} {c : Clausula n} {rest : CNF n}
    (h : inspect x q = some (c, rest)) :
    satisfeita c x = false ∧ ∃ a b, q = a ++ c :: b ∧ rest = a ++ b := by
  induction q generalizing rest with
  | nil => simp [inspect] at h
  | cons d q ih =>
    cases hd : satisfeita d x with
    | false =>
      simp only [inspect, hd, Bool.false_eq_true, ↓reduceIte, Option.some.injEq,
        Prod.mk.injEq] at h
      obtain ⟨rfl, rfl⟩ := h
      exact ⟨hd, [], _, rfl, rfl⟩
    | true =>
      cases he : inspect x q with
      | none => simp [inspect, hd, he] at h
      | some v =>
        obtain ⟨e, r⟩ := v
        simp only [inspect, hd, ↓reduceIte, he, Option.map_some, Option.some.injEq,
          Prod.mk.injEq] at h
        obtain ⟨rfl, rfl⟩ := h
        obtain ⟨bad, a, b, ha, hb⟩ := ih he
        exact ⟨bad, d :: a, b, by simp [ha], by simp [hb]⟩

/-- Every complete valuation has exactly the same joint verdict after a transfer. -/
theorem transfer_models (left : CNF n) {x : Assignment n} {q : CNF n}
    {c : Clausula n} {rest : CNF n} (h : inspect x q = some (c, rest))
    (y : Assignment n) :
    passes ((c :: left) ++ rest) y = passes (left ++ q) y := by
  obtain ⟨_, a, b, rfl, rfl⟩ := inspect_some h
  simp [passes, Bool.and_left_comm]

/-- Every subsequent admissible proposal satisfies any clause retained on the left. -/
theorem learned_cannot_fail {c : Clausula n} {left q : CNF n}
    {y : Assignment n} (hc : c ∈ left) (hy : passes left y = true) (rest : CNF n) :
    inspect y q ≠ some (c, rest) := by
  intro hit
  have yes := List.all_eq_true.mp hy c hc
  exact Bool.noConfusion (yes.symm.trans (inspect_some hit).1)

structure Exact (propose : Proposer n) : Prop where
  sound : ∀ l x, propose l = some x → passes l x = true
  complete : ∀ l, propose l = none → ¬ SAT l

inductive Verdict (n : Nat) where
  | found (x : Assignment n)
  | unsat
  | exhausted

structure Report (n : Nat) where
  result : Verdict n
  replies : CNF n
  calls : Nat

def learned (c : Clausula n) (r : Report n) : Report n :=
  ⟨r.result, c :: r.replies, r.calls + 1⟩

def run (propose : Proposer n) : Nat → CNF n → CNF n → Report n
  | 0, _, _ => ⟨.exhausted, [], 0⟩
  | fuel+1, left, q =>
    match propose left with
    | none => ⟨.unsat, [], 1⟩
    | some x =>
      match inspect x q with
      | none => ⟨.found x, [], 1⟩
      | some (c, rest) => learned c (run propose fuel (c :: left) rest)

def Correct (f : CNF n) : Verdict n → Prop
  | .found x => passes f x = true
  | .unsat => ¬ SAT f
  | .exhausted => False

private theorem transport {left q rest : CNF n} {x : Assignment n} {c : Clausula n}
    (h : inspect x q = some (c, rest)) (v : Verdict n) :
    Correct ((c :: left) ++ rest) v ↔ Correct (left ++ q) v := by
  cases v with
  | found y => simp only [Correct, transfer_models left h]
  | unsat => simp only [Correct, sat_iff, transfer_models left h]
  | exhausted => rfl

/-- Fuel strictly larger than the pending length covers every terminal call.
Calls include the last proposal, whether it yields a model or reports UNSAT. -/
theorem run_correct (propose : Proposer n) (hp : Exact propose) (fuel : Nat)
    (left q : CNF n) (enough : q.length < fuel) :
    Correct (left ++ q) (run propose fuel left q).result ∧
    (run propose fuel left q).calls = (run propose fuel left q).replies.length + 1 := by
  induction fuel generalizing left q with
  | zero => omega
  | succ k ih =>
    cases ho : propose left with
    | none =>
      refine ⟨?_, by simp [run, ho]⟩
      simp only [run, ho, Correct]
      rintro sat
      obtain ⟨y, hy⟩ := (sat_iff _).mp sat
      have both : passes left y = true ∧ passes q y = true := by simpa [passes] using hy
      exact hp.complete _ ho ((sat_iff _).mpr ⟨_, both.1⟩)
    | some x =>
      cases hi : inspect x q with
      | none =>
        refine ⟨?_, by simp [run, ho, hi]⟩
        have hx := hp.sound _ _ ho
        have hq := (inspect_none x q).mp hi
        simp [run, ho, hi, Correct, passes] at hx hq ⊢
        exact ⟨hx, hq⟩
      | some v =>
        obtain ⟨c, rest⟩ := v
        obtain ⟨_, a, b, eq, er⟩ := inspect_some hi
        have hl : rest.length < k := by simp [eq, er] at enough ⊢; omega
        obtain ⟨ok, calls⟩ := ih (c :: left) rest hl
        exact ⟨by simpa [run, ho, hi, learned] using (transport hi _).mp ok,
          by simpa [run, ho, hi, learned] using calls⟩

/-- Each structural resource is bounded even if the caller stops early
or supplies a poor proposer. The clause payload uses its original unary spelling. -/
theorem reply_bounds (propose : Proposer n) (fuel : Nat) (left q : CNF n) :
    (run propose fuel left q).replies.length ≤ q.length ∧
    (original (run propose fuel left q).replies).length ≤ (original q).length := by
  induction fuel generalizing left q with
  | zero => simp [run, original]
  | succ k ih =>
    cases ho : propose left with
    | none => simp [run, ho, original]
    | some x =>
      cases hi : inspect x q with
      | none => simp [run, ho, hi, original]
      | some v =>
        obtain ⟨c, rest⟩ := v
        obtain ⟨_, a, b, eq, er⟩ := inspect_some hi
        obtain ⟨count, bytes⟩ := ih (c :: left) rest
        simp only [run, ho, hi, learned, List.length_cons, original, List.flatMap_cons,
          List.length_append]
        simp only [eq, er, original, List.flatMap_append, List.flatMap_cons,
          List.length_append, List.length_cons] at count bytes ⊢
        constructor <;> omega

/-- Duplicate clauses on the right cannot induce duplicate replies, even
if the two occurrences carry different list positions. -/
theorem distinct_replies (propose : Proposer n)
    (sound : ∀ l x, propose l = some x → passes l x = true) (fuel : Nat)
    (left q : CNF n) :
    (run propose fuel left q).replies.Nodup ∧
    ∀ d ∈ (run propose fuel left q).replies, d ∉ left := by
  induction fuel generalizing left q with
  | zero => simp [run]
  | succ k ih =>
    cases ho : propose left with
    | none => simp [run, ho]
    | some x =>
      cases hi : inspect x q with
      | none => simp [run, ho, hi]
      | some v =>
        obtain ⟨c, rest⟩ := v
        obtain ⟨unique, fresh⟩ := ih (c :: left) rest
        have hc : c ∉ left := fun mem => learned_cannot_fail mem (sound _ _ ho) _ hi
        simp only [run, ho, hi, learned, List.nodup_cons, List.mem_cons]
        refine ⟨⟨fun mem => fresh _ mem (by simp), unique⟩, ?_⟩
        rintro d (rfl | mem)
        · exact hc
        · exact fun was => fresh _ mem (List.mem_cons_of_mem _ was)

def protocol (propose : Proposer n) (left q : CNF n) : Report n :=
  run propose (q.length + 1) left q

theorem model_iff_sat (propose : Proposer n) (hp : Exact propose) (left q : CNF n) :
    (∃ x, (protocol propose left q).result = .found x) ↔ SAT (left ++ q) := by
  have hv := (run_correct propose hp (q.length+1) left q (by omega)).1
  change Correct (left ++ q) (protocol propose left q).result at hv
  cases he : (protocol propose left q).result with
  | found y => exact ⟨fun _ => (sat_iff _).mpr ⟨y, by simpa [he, Correct] using hv⟩,
      fun _ => ⟨y, rfl⟩⟩
  | unsat => simpa [he, Correct] using (show ¬ SAT (left ++ q) by simpa [he, Correct] using hv)
  | exhausted => simp [he, Correct] at hv

theorem call_bound (propose : Proposer n) (hp : Exact propose) (left q : CNF n) :
    (protocol propose left q).calls ≤ q.length + 1 := by
  have eq := (run_correct propose hp (q.length+1) left q (by omega)).2
  have count := (reply_bounds propose (q.length+1) left q).1
  unfold protocol
  omega

/-- Finite reference implementation. The table can have exponential length;
its per-proposal construction/search is outside the communication bounds. -/
def enumerateProposer (n : Nat) : Proposer n :=
  fun p => (IALD.CadeiasDeBolsas.rows n).find? (passes p)

theorem enumerate_exact : Exact (enumerateProposer n) where
  sound p x hx := List.find?_some hx
  complete p hn hs := by
    obtain ⟨x, hx⟩ := (sat_iff _).mp hs
    exact List.find?_eq_none.mp hn x (IALD.CadeiasDeBolsas.complete_rows _) hx

private theorem pairs_length {α β : Type} (f g : α → β) (xs : List α) :
    (xs.flatMap (fun x => [f x, g x])).length = xs.length * 2 := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.flatMap_cons, List.length_append, List.length_cons,
      List.length_nil, ih]; omega

theorem proposal_table_length (k : Nat) : (IALD.CadeiasDeBolsas.rows k).length = 2^k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [IALD.CadeiasDeBolsas.rows, pairs_length, ih, pow_succ]

/-- Every rejected valuation for this one positive unit has a unique
arbitrary tail. Thus a single reply can exclude exactly two to the k names. -/
def unitClause (k : Nat) : Clausula (k+1) := [⟨0, true⟩]

private theorem unit_value {k : Nat} (x : Assignment (k+1)) :
    satisfeita (unitClause k) x = x 0 := by
  cases h : x 0 <;> simp [unitClause, satisfeita, Literal.vale, h]

theorem unit_reply {k : Nat} (x : Assignment (k+1)) :
    inspect x [unitClause k] = some (unitClause k, []) ↔ x 0 = false := by
  cases h : x 0 <;> simp [inspect, unit_value, h]

def rejectedUnitEquiv (k : Nat) :
    {x : Assignment (k+1) // satisfeita (unitClause k) x = false} ≃ Assignment k where
  toFun x i := x.val i.succ
  invFun tail := ⟨Fin.cases false tail, by rw [unit_value]; rfl⟩
  left_inv x := by
    apply Subtype.ext
    funext j
    cases j using Fin.cases with
    | zero =>
      have hz : x.val 0 = false := (unit_value x.val).symm.trans x.property
      exact hz.symm
    | succ i => rfl
  right_inv t := rfl

theorem names_rejected_by_unit (k : Nat) :
    Fintype.card {x : Assignment (k+1) // satisfeita (unitClause k) x = false} = 2^k := by
  classical
  simpa [Assignment] using Fintype.card_congr (rejectedUnitEquiv k)

end Codex.ClauseReply

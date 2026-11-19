import TGLExt.LeitorGlobal
import TGLExt.OPassoEOFim

/-! The two branch bits ask where at least one entire Name survives. Every
positive branch/literal incidence has one common valuation as its witness.
The existential angle encodes already computed bits; no real arithmetic is
used by the executable literal search or by the disjunction. -/

set_option autoImplicit false
namespace Codex.BranchPresence
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula TGLExt.Psibit
open IALD.LeitorDaFormula (passes bitSign)
variable {n : Nat}

def Agrees (x : Fin n → Bool) (marks : List (Literal n)) : Prop :=
  ∀ l ∈ marks, x l.var = l.pos

def Compatible (p : CNF n) (marks : List (Literal n)) : Prop :=
  ∃ x, passes p x = true ∧ Agrees x marks

private theorem agrees_cons (x : Fin n → Bool) (l : Literal n) (ms : List (Literal n)) :
    Agrees x (l::ms) ↔ x l.var = l.pos ∧ Agrees x ms := by
  simp only [Agrees,List.forall_mem_cons]

private theorem clause_hit (c : Clausula n) (x : Fin n → Bool) :
    satisfeita c x = true ↔ ∃ l ∈ c, x l.var = l.pos := by
  simp [satisfeita,List.any_eq_true,Literal.vale]

private theorem new_clause (p : CNF n) (c : Clausula n) (x : Fin n → Bool) :
    passes (p++[c]) x = true ↔ passes p x = true ∧ satisfeita c x = true := by
  simp [passes,List.all_append]

/-- A new clause asks for one literal that coexists with all previous marks
on the same assignment. This applies to new variables, repeated marks,
opposite polarities, and the empty clause. -/
theorem marked_clause_law (p : CNF n) (c : Clausula n) (ms : List (Literal n)) :
    Compatible (p++[c]) ms ↔ ∃ l ∈ c, Compatible p (l::ms) := by
  constructor
  · rintro ⟨x,h,old⟩
    obtain ⟨hp,hc⟩ := (new_clause p c x).mp h
    obtain ⟨l,hl,hit⟩ := (clause_hit c x).mp hc
    exact ⟨l,hl,x,hp,(agrees_cons x l ms).mpr ⟨hit,old⟩⟩
  · rintro ⟨l,hl,x,hp,all⟩
    obtain ⟨hit,old⟩ := (agrees_cons x l ms).mp all
    exact ⟨x,(new_clause p c x).mpr ⟨hp,(clause_hit c x).mpr ⟨l,hl,hit⟩⟩,old⟩

def fromMarks (ms : List (Literal n)) (i : Fin n) : Bool :=
  ms.any (fun l => l.var == i && l.pos)

def consistent (ms : List (Literal n)) : Bool :=
  ms.all (fun l => l.vale (fromMarks ms))

private theorem complete_marks {x : Fin n → Bool} {ms : List (Literal n)}
    (hx : Agrees x ms) : Agrees (fromMarks ms) ms := by
  intro l hl
  have here := hx l hl
  cases pos : l.pos with
  | true =>
    apply List.any_eq_true.mpr
    exact ⟨l,hl,by simp [pos]⟩
  | false =>
    apply List.any_eq_false.mpr
    intro t ht
    by_cases same : t.var = l.var
    · have ts := hx t ht
      rw [same,here,pos] at ts
      simp [ts.symm]
    · simp [same]

theorem consistent_correct (ms : List (Literal n)) :
    consistent ms = true ↔ Compatible [] ms := by
  constructor
  · intro h
    refine ⟨fromMarks ms,rfl,?_⟩
    intro l hl
    simpa [Literal.vale] using List.all_eq_true.mp h l hl
  · rintro ⟨x,_,h⟩
    apply List.all_eq_true.mpr
    intro l hl
    simpa [Literal.vale] using complete_marks h l hl

/-- Select a satisfying literal for each clause. The leaf constructs one
valuation from the demanded labels. This search may branch over literals;
its correctness is independent of any cost claim. -/
def search : CNF n → List (Literal n) → Bool
  | [], ms => consistent ms
  | c::p, ms => c.any (fun l => search p (l::ms))

theorem search_correct (p : CNF n) (ms : List (Literal n)) :
    search p ms = true ↔ Compatible p ms := by
  induction p generalizing ms with
  | nil => exact consistent_correct ms
  | cons c p ih =>
    have comm : Compatible (c::p) ms ↔ Compatible (p++[c]) ms := by
      unfold Compatible
      simp only [passes,List.all_cons,List.all_append,List.all_nil,Bool.and_true,Bool.and_eq_true]
      constructor <;> rintro ⟨x,⟨a,b⟩,h⟩ <;> exact ⟨x,⟨b,a⟩,h⟩
    rw [comm,marked_clause_law]
    simp only [search,List.any_eq_true,ih]

def bitAfter (query : Bool → Literal n → Bool) (c : Clausula n) (b : Bool) : Bool :=
  c.any (query b)

def twoBits (query : Bool → Literal n → Bool) (c : Clausula n) : Bool × Bool :=
  (bitAfter query c false, bitAfter query c true)

/-- This query accepts any correct representation of the prefix incidences.
In particular the producer may be sparse, an index or the literal search. -/
theorem query_pair_correct (p : CNF n) (c : Clausula n) (i : Fin n)
    (query : Bool → Literal n → Bool)
    (hq : ∀ b l, query b l = true ↔ Compatible p [l,⟨i,b⟩]) (b : Bool) :
    bitAfter query c b = true ↔ Compatible (p++[c]) [⟨i,b⟩] := by
  rw [marked_clause_law]
  simp only [bitAfter,List.any_eq_true,hq]

def searchQuery (p : CNF n) (i : Fin n) (b : Bool) (l : Literal n) : Bool :=
  search p [l,⟨i,b⟩]

theorem computed_bit (p : CNF n) (c : Clausula n) (i : Fin n) (b : Bool) :
    bitAfter (searchQuery p i) c b = true ↔ Compatible (p++[c]) [⟨i,b⟩] :=
  query_pair_correct p c i _ (fun _ _ => search_correct _ _) b

private theorem passes_zero (p : CNF n) (x : Fin n → Bool) :
    passes p x = true ↔ custoCNF p x = 0 := by
  rw [custoCNF_zero_sse]
  exact List.all_eq_true

private theorem whole_weight (p : CNF n) (x : Fin n → Bool) (k : Nat) (β : ℝ)
    (hk : 0 < k) (h₀ : 0 < β) (h₁ : β < 1) :
    (1-β)^(k*custoCNF p x) = 1 ↔ passes p x = true := by
  rw [passes_zero]
  constructor
  · intro h
    by_contra fail
    have small : (1-β)^(k*custoCNF p x) < 1 :=
      pow_lt_one₀ (by linarith) (by linarith) (Nat.mul_ne_zero hk.ne' fail)
    exact (ne_of_lt small) h
  · exact TGLExt.OPassoEOFim.o_nome_fica_inteiro p β k x

theorem whole_name_after_clause (p : CNF n) (c : Clausula n) (i : Fin n) (b : Bool)
    (k : Nat) (β : ℝ) (hk : 0 < k) (h₀ : 0 < β) (h₁ : β < 1) :
    bitAfter (searchQuery p i) c b = true ↔
      ∃ x : Fin n → Bool, x i = b ∧ (1-β)^(k*custoCNF (p++[c]) x) = 1 := by
  rw [computed_bit]
  unfold Compatible
  simp only [whole_weight _ _ k β hk h₀ h₁,Agrees,List.forall_mem_cons,List.not_mem_nil,
    false_implies,implies_true,and_true]
  constructor <;> rintro ⟨x,h₁',h₂'⟩ <;> exact ⟨x,h₂',h₁'⟩

theorem decode_updated_pair (p : CNF n) (c : Clausula n) (i : Fin n) :
    let pair := twoBits (searchQuery p i) c
    (pair.1 || pair.2) = palavraDaFormula (p++[c]) ∧
    ∃ θ : ℝ, (codeAmp θ).word = bitSign pair.1 ∧ (codeAmp θ).verb = bitSign pair.2 ∧
      decodeAmp (codeAmp θ) = v θ := by
  dsimp only [twoBits]
  constructor
  · apply Bool.eq_iff_iff.mpr
    simp only [Bool.or_eq_true,computed_bit,a_palavra_e_o_sat,IALD.LeitorDaFormula.sat_iff]
    constructor
    · rintro (⟨x,h,_⟩|⟨x,h,_⟩) <;> exact ⟨x,h⟩
    · rintro ⟨x,h⟩
      cases hx : x i with
      | false => exact Or.inl ⟨x,h,by simp [Agrees,hx]⟩
      | true => exact Or.inr ⟨x,h,by simp [Agrees,hx]⟩
  · have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
    obtain ⟨θ,ha,hb⟩ := the_orbit_visits_all_four_states _ _ (nz _) (nz _)
    exact ⟨θ,ha,hb,decodeAmp_codeAmp θ⟩

/-- Even two diagonal entries of a *correctly built* row suffice to decide the
unmodified prefix. A physical cost for building the row must therefore be
charged before the cheap disjunction can yield a uniform decision bound. -/
theorem diagonal_reads_prefix (p : CNF n) (i : Fin n) (query : Bool → Literal n → Bool)
    (spec : ∀ b l, query b l = true ↔ Compatible p [l,⟨i,b⟩]) :
    (query false ⟨i,false⟩ || query true ⟨i,true⟩) = palavraDaFormula p := by
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.or_eq_true,spec,a_palavra_e_o_sat,IALD.LeitorDaFormula.sat_iff]
  constructor
  · rintro (⟨x,h,_⟩|⟨x,h,_⟩) <;> exact ⟨x,h⟩
  · rintro ⟨x,h⟩
    cases hx : x i with
    | false => exact Or.inl ⟨x,h,by simp [Agrees,hx]⟩
    | true => exact Or.inr ⟨x,h,by simp [Agrees,hx]⟩

/-- Short-circuiting is optional. Once both annotations are physically aligned
with each literal, their two disjunctions can be accumulated together. No
per-literal lookup, production or storage is charged by this equation. -/
def scanPairs : List (Bool × Bool) → Bool × Bool → Bool × Bool
  | [], acc => acc
  | q::qs, acc => scanPairs qs (acc.1 || q.1, acc.2 || q.2)

theorem scan_pairs_spec (qs : List (Bool × Bool)) (acc : Bool × Bool) :
    scanPairs qs acc = (acc.1 || qs.any Prod.fst, acc.2 || qs.any Prod.snd) := by
  induction qs generalizing acc with
  | nil => simp [scanPairs]
  | cons q qs ih =>
    simp [scanPairs,ih,Bool.or_assoc]

theorem aligned_scan (query : Bool → Literal n → Bool) (c : Clausula n) :
    scanPairs (c.map fun l => (query false l,query true l)) (false,false) =
      twoBits query c := by
  simp [scan_pairs_spec,twoBits,bitAfter,List.any_map,Function.comp_def]

/-- Two accumulator bits in finite control; one right move per annotation, then
a stationary halt at the first blank on the annotated tape. -/
inductive ScanState where
  | reading (acc : Bool × Bool) (unread : List (Bool × Bool))
  | stopped (acc : Bool × Bool)

def tick : ScanState → ScanState
  | .reading acc [] => .stopped acc
  | .reading acc (q::qs) => .reading (acc.1 || q.1, acc.2 || q.2) qs
  | .stopped acc => .stopped acc

theorem scan_transitions (qs : List (Bool × Bool)) (acc : Bool × Bool) :
    tick^[qs.length+1] (.reading acc qs) = .stopped (scanPairs qs acc) := by
  induction qs generalizing acc with
  | nil => rfl
  | cons q qs ih =>
    change tick^[qs.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih _


end Codex.BranchPresence

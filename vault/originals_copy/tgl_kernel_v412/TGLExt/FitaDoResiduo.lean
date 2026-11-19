import TGLExt.RestricaoGlobal
import TGLExt.PolinomioPorEscolha

set_option autoImplicit false

namespace Codex.ResidualTape

open TGLExt.TraducaoTuring Codex.PolinomioPorEscolha Codex.SharedBranch

inductive Mode where
  | scan (ticks hit : Bool)
  | erase
  | halt
  deriving DecidableEq

/-- In scan mode the output head is on the first blank after the written text.
In erase mode it is on the last letter (or the left endmarker when empty).
The reversed field describes the physical tape; reversal is never a machine instruction. -/
structure Cfg where
  mode : Mode
  input : List Letter
  output : List Letter

def reading (hit : Bool) (r o : List Letter) := Cfg.mk (.scan false hit) r o

def step (b : Bool) : Cfg → Cfg
  | c@⟨.halt, _, _⟩ => c
  | ⟨.scan _ _, [], o⟩ => ⟨.halt, [], o⟩
  | ⟨.scan _ h, .tick :: r, o⟩ => ⟨.scan true h, r, .tick :: o⟩
  | ⟨.scan true h, .sign s :: r, o⟩ => reading h r (.sign s :: o)
  | ⟨.scan false h, .sign s :: r, o⟩ => reading (h || (s == b)) r o
  | ⟨.scan _ true, .delimiter :: r, o⟩ => ⟨.erase, r, o⟩
  | ⟨.scan _ false, .delimiter :: r, o⟩ => reading false r (.delimiter :: o)
  | ⟨.erase, r, []⟩ => reading false r []
  | ⟨.erase, r, .delimiter :: o⟩ => reading false r (.delimiter :: o)
  | ⟨.erase, r, .tick :: o⟩ => ⟨.erase, r, o⟩
  | ⟨.erase, r, .sign _ :: o⟩ => ⟨.erase, r, o⟩

def run (b : Bool) : Nat → Cfg → Cfg
  | 0,c => c
  | k+1,c => run b k (step b c)

theorem run_add (b : Bool) (m k : Nat) (c : Cfg) : run b (m+k) c = run b k (run b m c) := by
  induction m generalizing c with
  | zero => simp [run]
  | succ m ih => rw [Nat.succ_add]; exact ih _

/-- Physical displacements per transition, summing both heads. On a hit delimiter
the input moves right and the output moves left. Every erase transition moves only the output head. -/
def displacements : Cfg → Nat
  | ⟨.halt,_,_⟩ | ⟨.scan _ _,[],_⟩ => 0
  | ⟨.erase,_,_⟩ | ⟨.scan false _,.sign _ :: _,_⟩ => 1
  | ⟨.scan _ _,_ :: _,_⟩ => 2

def travel (b : Bool) : Nat → Cfg → Nat
  | 0,_ => 0
  | k+1,c => displacements c + travel b k (step b c)

theorem travel_le (b : Bool) (k : Nat) (c : Cfg) : travel b k c ≤ 2*k := by
  have bound (z : Cfg) : displacements z ≤ 2 := by
    unfold displacements
    split <;> decide
  induction k generalizing c with
  | zero => rfl
  | succ k ih =>
    rw [travel]
    have := ih (step b c)
    have := bound c
    omega

private theorem walk_ticks (b h : Bool) (k : Nat) (seen : Bool) (r o : List Letter) :
    run b k ⟨.scan seen h, List.replicate k .tick ++ r, o⟩ =
      ⟨.scan (seen || decide (0 < k)) h, r, List.replicate k .tick ++ o⟩ := by
  induction k generalizing seen o with
  | zero => simp [run]
  | succ k ih =>
    change run b k ⟨.scan true h, List.replicate k .tick ++ r, .tick :: o⟩ = _
    rw [ih, List.replicate_succ']
    simp [List.append_assoc]

private theorem one_token (b h s : Bool) (k : Nat) (r o : List Letter) :
    run b (k+1) (reading h (List.replicate k .tick ++ .sign s :: r) o) =
    reading (h || (decide (k = 0) && (s == b))) r
      (if k = 0 then o else .sign s :: (List.replicate k .tick ++ o)) := by
  rw [run_add]
  unfold reading
  rw [walk_ticks]
  cases k <;> simp [run, step, reading]

variable {n : Nat}

private def body (c : Clausula (n+1)) := c.flatMap spell
private def mark (b : Bool) (l : Literal (n+1)) := l.var == 0 && l.pos == b
private def kept (c : Clausula (n+1)) := c.filter (fun l => l.var != 0)

private theorem read_lit (b h : Bool) (l : Literal (n+1)) (r o : List Letter) :
    run b (spell l).length (reading h (spell l ++ r) o) =
    reading (h || mark b l) r (if l.var = 0 then o else (spell l).reverse ++ o) := by
  have he : l.var.val = 0 ↔ l.var = 0 := by
    change l.var.val = (0 : Fin (n+1)).val ↔ _
    exact Fin.val_inj
  simpa [spell, mark, List.append_assoc, he, Bool.beq_eq_decide_eq l.var 0] using
    one_token b h l.pos l.var.val r o

private theorem read_body (b h : Bool) (c : Clausula (n+1)) (r o : List Letter) :
    run b (body c).length (reading h (body c ++ r) o) =
    reading (h || c.any (mark b)) r ((body (kept c)).reverse ++ o) := by
  induction c generalizing h o with
  | nil => simp [body, kept, run]
  | cons l c ih =>
    rw [show body (l::c) = spell l ++ body c from rfl, List.length_append, run_add, List.append_assoc,
      read_lit, ih]
    by_cases hz : l.var = 0 <;> simp [kept, body, hz, List.reverse_append, List.append_assoc, Bool.or_assoc]

private theorem no_delimiter (c : Clausula (n+1)) : .delimiter ∉ body c := by
  intro h
  obtain ⟨l, _, hl⟩ := List.mem_flatMap.mp h
  simp [spell] at hl

private def fenced (o : List Letter) : Prop := o = [] ∨ ∃ t, o = .delimiter :: t

private theorem erase_prefix (b : Bool) (r o w : List Letter) (hf : fenced o) (hw : .delimiter ∉ w) :
    run b (w.length+1) ⟨.erase, r, w ++ o⟩ = reading false r o := by
  induction w with
  | nil => rcases hf with rfl | ⟨t,rfl⟩ <;> rfl
  | cons s w ih =>
    have hw' : .delimiter ∉ w := fun e => hw (List.mem_cons_of_mem _ e)
    cases s with
    | tick => exact ih hw'
    | sign s => exact ih hw'
    | delimiter => exact False.elim (hw List.mem_cons_self)

private theorem body_kept_le (c : Clausula (n+1)) : (body (kept c)).length ≤ (body c).length := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    change (body (kept (l::c))).length ≤ (spell l ++ body c).length
    by_cases hz : l.var = 0 <;> simp [kept, body, hz] at ih ⊢ <;> omega

private def chunk (b : Bool) (c : Clausula (n+1)) :=
  (restrictClause 0 b c).elim [] spellClause

private theorem chunk_fenced (b : Bool) (c : Clausula (n+1)) (o : List Letter) (hf : fenced o) :
    fenced ((chunk b c).reverse ++ o) := by
  unfold chunk
  cases he : restrictClause 0 b c with
  | none => exact hf
  | some d =>
    refine Or.inr ⟨(body d).reverse ++ o, ?_⟩
    simp [spellClause,body]

private theorem clause_trace (b : Bool) (c : Clausula (n+1)) (r o : List Letter) (hf : fenced o) :
    ∃ k ≤ 2 * (spellClause c).length,
      run b k (reading false (spellClause c ++ r) o) = reading false r ((chunk b c).reverse ++ o) := by
  have hc : spellClause c = body c ++ [.delimiter] := rfl
  have hg := read_body b false c (.delimiter :: r) o
  simp only [Bool.false_or] at hg
  cases hh : c.any (mark b) with
  | false =>
    refine ⟨(body c).length+1, ?_, ?_⟩
    · simp [hc]
    · rw [hc,List.append_assoc, List.singleton_append, run_add,hg,hh]
      have hchunk : chunk b c = body (kept c) ++ [.delimiter] := by
        change (if c.any (mark b) then none else some (kept c)).elim [] spellClause = _
        rw [hh]
        rfl
      rw [hchunk]
      simp [run,step,reading,List.reverse_append]
  | true =>
    let w := (body (kept c)).reverse
    refine ⟨(body c).length + (1 + (w.length+1)), ?_, ?_⟩
    · have := body_kept_le c
      simp [w,hc]; omega
    · rw [hc,List.append_assoc, List.singleton_append,run_add,hg,hh,run_add]
      have hchunk : chunk b c = [] := by
        unfold chunk restrictClause
        change (if c.any (mark b) then none else some (kept c)).elim [] spellClause = []
        rw [hh]
        rfl
      have clean : .delimiter ∉ w := by simpa [w] using no_delimiter (kept c)
      change run b (w.length+1) ⟨.erase,r,w++o⟩ = _
      rw [erase_prefix b r o w hf clean, hchunk]
      rfl

private theorem original_cons (b : Bool) (c : Clausula (n+1)) (p : CNF (n+1)) :
    original (restrictVar 0 b (c::p)) = chunk b c ++ original (restrictVar 0 b p) := by
  unfold restrictVar
  cases he : restrictClause 0 b c <;> simp [he,chunk,original]

private theorem sweep (b : Bool) (p : CNF (n+1)) (r o : List Letter) (hf : fenced o) :
    ∃ k ≤ 2 * (original p).length, run b k (reading false (original p ++ r) o) =
      reading false r ((original (restrictVar 0 b p)).reverse ++ o) := by
  induction p generalizing o with
  | nil => exact ⟨0,by simp [original],rfl⟩
  | cons c p ih =>
    obtain ⟨i, hi, ha⟩ := clause_trace b c (original p ++ r) o hf
    obtain ⟨j, hj, hb⟩ := ih _ (chunk_fenced b c o hf)
    refine ⟨i+j,?_,?_⟩
    · change i+j ≤ 2*(spellClause c ++ original p).length
      rw [List.length_append]; omega
    · rw [show original (c::p) = spellClause c ++ original p from rfl,
        List.append_assoc,run_add,ha,hb,original_cons,List.reverse_append,List.append_assoc]

/-- For every flat input on at least one named variable, the halted output tape
spells the conditioned formula verbatim, including all surviving delimiters. -/
theorem restrict_on_tape (b : Bool) (p : CNF (n+1)) :
    ∃ T ≤ 2*(original p).length+1,
      travel b T (reading false (original p) []) ≤ 4*(original p).length+2 ∧
      run b T (reading false (original p) []) =
        ⟨.halt, [], (original (restrictVar 0 b p)).reverse⟩ := by
  obtain ⟨k,hk,h⟩ := sweep b p [] [] (Or.inl rfl)
  simp only [List.append_nil] at h
  refine ⟨k+1, by omega, ?_, ?_⟩
  · have := travel_le b (k+1) (reading false (original p) [])
    omega
  · rw [run_add,h]; rfl

end Codex.ResidualTape

import TGLExt.EscolhasGlobais
import TGLExt.CruzamentosUniversais

/-! Exact run of the existing Horn-program selector on distinct, crossing
clauses in the unary input alphabet of CruzamentosUniversais. -/
namespace IALD.BuscaEmCruzamentos
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.CrossSelectors IALD.CruzamentosUniversais

def unitNeg {n} (i : Fin n) : Clausula n := [⟨i,false⟩]
def original (n : Nat) : CNF n := [] :: (List.finRange n).map unitNeg
def family (n : Nat) := translate (original n)

theorem crossing {n} {c} (hc : c ∈ family n) : crosses c :=
  every_clause_crosses (original n) c hc

theorem guard_values {n} (z : Env (width n)) :
    passes (guards n) z = true ↔ z (a n) = false ∧ z (b n) = false := guarded z

theorem padded_count {n} {c} (hc : c ∈ (original n).map pad) :
    (alternatives c).length = 2 := by
  obtain ⟨d,hd,rfl⟩ := List.mem_map.mp hc
  rcases List.mem_cons.mp hd with rfl | hd
  · rfl
  · obtain ⟨i,_,rfl⟩ := List.mem_map.mp hd
    rfl

theorem guard_count {n} {c} (hc : c ∈ guards n) : (alternatives c).length = 1 := by
  simp [guards] at hc
  rcases hc with rfl | rfl | rfl <;> rfl

private theorem padded_injective {n} :
    Function.Injective (fun i : Fin n => pad (unitNeg i)) := by
  intro i j h
  have e := congrArg (fun c : Clausula (width n) => c.map (fun l => l.var.val)) h
  apply Fin.ext
  simpa [pad,unitNeg,liftLit,shift] using e

theorem distinct_clauses (n : Nat) : (family n).Nodup := by
  apply List.nodup_append.mpr
  refine ⟨?_,?_,?_⟩
  · change (pad ([] : Clausula n) :: (((List.finRange n).map unitNeg).map pad)).Nodup
    rw [List.map_map]
    apply List.nodup_cons.mpr
    constructor
    · intro hm
      obtain ⟨i,_,hh⟩ := List.mem_map.mp hm
      have he := congrArg List.length hh
      change 3 = 2 at he
      omega
    · exact (List.nodup_finRange n).map padded_injective
  · apply List.Nodup.of_map (List.map Literal.pos)
    change ([[false,false],[false,true],[true,false]] : List (List Bool)).Nodup
    decide
  · intro c hc d hd e
    subst d
    have hp := padded_count hc
    have hg := guard_count hd
    omega

theorem distinct_local_choices {n} {c} (hc : c ∈ family n) : (alternatives c).Nodup := by
  rcases List.mem_append.mp hc with hp | hg
  · obtain ⟨d,hd,rfl⟩ := List.mem_map.mp hp
    apply List.Nodup.of_map (fun r : Codex.HornCross.Rule (width n) => r.head.map Fin.val)
    rcases List.mem_cons.mp hd with rfl | hd
    · change ([some 0,some 1] : List (Option Nat)).Nodup
      decide
    · obtain ⟨i,_,rfl⟩ := List.mem_map.mp hd
      change ([some 0,some 1] : List (Option Nat)).Nodup
      decide
  · simp [guards] at hg
    rcases hg with rfl | rfl | rfl <;> exact List.nodup_singleton _

private theorem cons_distinct {α : Type} (rs : List α) (qs : List (List α))
    (hr : rs.Nodup) (hq : qs.Nodup) :
    (rs.flatMap fun r => qs.map (r :: ·)).Nodup := by
  induction rs with
  | nil => simp
  | cons r rs ih =>
    obtain ⟨hn,ht⟩ := List.nodup_cons.mp hr
    apply List.nodup_append.mpr
    refine ⟨hq.map (fun _ _ h => (List.cons.inj h).2),ih ht,?_⟩
    intro u hu v hv he
    obtain ⟨q,_,hru⟩ := List.mem_map.mp hu
    obtain ⟨s,hs,hv'⟩ := List.mem_flatMap.mp hv
    obtain ⟨q',_,hsv⟩ := List.mem_map.mp hv'
    have e : r = s := (List.cons.inj (hru.trans (he.trans hsv.symm))).1
    exact hn (e.symm ▸ hs)

private theorem programs_distinct {k} (p : CNF k)
    (hf : ∀ c ∈ p, (alternatives c).Nodup) : (programs p).Nodup := by
  induction p with
  | nil => simp [programs]
  | cons c p ih =>
    exact cons_distinct _ _ (hf _ List.mem_cons_self)
      (ih (fun d hd => hf d (List.mem_cons_of_mem _ hd)))

theorem distinct_programs (n : Nat) : (programs (family n)).Nodup :=
  programs_distinct _ (fun _ hc => distinct_local_choices hc)

private theorem count_over_guards {n} (cs : CNF (width n))
    (hc : ∀ c ∈ cs, (alternatives c).length = 2) :
    (programs (cs ++ guards n)).length = 2^cs.length := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
    rw [List.cons_append,selection_count,hc _ List.mem_cons_self,
      ih (fun d hd => hc d (List.mem_cons_of_mem _ hd)),List.length_cons,pow_succ]
    omega

theorem exact_count (n : Nat) : (programs (family n)).length = 2^(n+1) := by
  simpa [family,CruzamentosUniversais.translate,original] using
    count_over_guards ((original n).map pad) (fun _ hc => padded_count hc)

theorem actual_visits (n : Nat) :
    Codex.CrossSelectors.scan checkProgram (programs (family n)) = (false,2^(n+1)) := by
  have h : (Codex.CrossSelectors.scan checkProgram (programs (family n))).1 = false := by
    rw [selector_word,family,word_preserved]
    apply Bool.eq_false_iff.mpr
    intro hp
    obtain ⟨x,hx⟩ := (sat_iff _).mp ((a_palavra_e_o_sat _).mp hp)
    simp [original,passes,satisfeita] at hx
  have h' := h
  rw [scan_spec] at h'
  exact Prod.ext h ((scan_all_false _ _ h').trans (exact_count n))

private theorem unit_occ {n} (is : List (Fin n)) : occ (is.map unitNeg) = is.length := by
  induction is with
  | nil => rfl
  | cons i is ih =>
    change 1 + occ (is.map unitNeg) = is.length+1
    omega

private theorem unit_body {n} (is : List (Fin n)) :
    (body (is.map unitNeg)).length ≤ is.length*(n+1) := by
  induction is with
  | nil => simp [body]
  | cons i is ih =>
    have hl : (emitClause (unitNeg i)).length = i.val+2 := by simp [emitClause,unitNeg,emitLit]
    change (emitClause (unitNeg i) ++ body (is.map unitNeg)).length ≤ (is.length+1)*(n+1)
    rw [List.length_append,hl,Nat.add_mul,Nat.one_mul]
    have hi := i.isLt
    omega

theorem tape_bound (n : Nat) : (input (family n)).length ≤ n^2+8*n+21 := by
  have hb := unit_body (List.finRange n)
  rw [List.length_finRange] at hb
  have ho : occ (original n) = n := by
    simpa [original,occ] using unit_occ (List.finRange n)
  have horig : (input (original n)).length =
      n+2 + (body ((List.finRange n).map unitNeg)).length := by
    simp [input,original,body,emitClause]
    omega
  rw [family,encoded_size,horig,ho]
  simp only [original,List.length_cons,List.length_map,List.length_finRange]
  nlinarith

end IALD.BuscaEmCruzamentos

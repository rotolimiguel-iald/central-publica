import TGLExt.RedesDeCadeias
import TGLExt.OPsiBitDaFormula

/-! Real CNF over numbered variables. Two fixed terminal indices and one fresh
index per series node; parallel subtrees share endpoints, never internal indices.
The numbering and both directions of witness transport are computable. -/
namespace IALD.RedeComoCNF
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula PsiNetworks

def joints : Net → Nat
  | .clause _ _ => 0
  | .series l r => (joints l + joints r) + 1
  | .parallel l r => joints l + joints r

def leaves : Net → Nat
  | .clause _ _ => 1
  | .series l r | .parallel l r => leaves l + leaves r

private def leftIndex (n : Nat) {m : Nat} (i : Fin m) := Fin.castAdd n i
private def rightIndex (m : Nat) {n : Nat} (i : Fin n) := Fin.natAdd m i

def label {k : Nat} (p : Lit) (a b : Fin k) : Literal k :=
  ⟨if p.right then b else a,p.sign⟩

def emit {k : Nat} : (e : Net) → Fin k → Fin k → (Fin (joints e) → Fin k) → CNF k
  | .clause p q, a,b,_ => [[label p a b,label q a b]]
  | .series l r, a,b,h =>
    let m := h (0 : Fin (joints l + joints r + 1))
    emit l a m (fun i => h (leftIndex (joints r) i).succ) ++
    emit r m b (fun i => h (rightIndex (joints l) i).succ)
  | .parallel l r, a,b,h =>
    emit l a b (fun i => h (leftIndex (joints r) i)) ++
    emit r a b (fun i => h (rightIndex (joints l) i))

def cnf (e : Net) : CNF (joints e + 2) := emit e 0 1 (fun i => i.succ.succ)

def unpack : (e : Net) → (Fin (joints e) → Bool) → Witness e
  | .clause _ _, _ => ()
  | .series l r, x =>
    (x (0 : Fin (joints l + joints r + 1)), unpack l (fun i => x (leftIndex (joints r) i).succ),
      unpack r (fun i => x (rightIndex (joints l) i).succ))
  | .parallel l r, x =>
    (unpack l (fun i => x (leftIndex (joints r) i)),
     unpack r (fun i => x (rightIndex (joints l) i)))

def pack : (e : Net) → Witness e → Fin (joints e) → Bool
  | .clause _ _, _ => Fin.elim0
  | .series l r, w => Fin.cases w.1 (Fin.append (pack l w.2.1) (pack r w.2.2))
  | .parallel l r, w => Fin.append (pack l w.1) (pack r w.2)

theorem witness_roundtrip (e : Net) (w : Witness e) : unpack e (pack e w) = w := by
  induction e with
  | clause p q => cases w; rfl
  | series l r hl hr =>
    rcases w with ⟨m,u,v⟩
    simp only [unpack,pack,Fin.cases_zero,Fin.cases_succ,leftIndex,rightIndex,
      Fin.append_left, Fin.append_right,hl,hr]
  | parallel l r hl hr =>
    rcases w with ⟨u,v⟩
    simp only [unpack,pack,leftIndex,rightIndex,Fin.append_left,Fin.append_right,hl,hr]

def evaluate {k : Nat} (p : CNF k) (x : Fin k → Bool) := p.all (fun c => satisfeita c x)

private theorem eval_append {k : Nat} (f g : CNF k) (x : Fin k → Bool) :
    evaluate (f ++ g) x = (evaluate f x && evaluate g x) := List.all_append

private theorem label_read {k : Nat} (p : Lit) (a b : Fin k) (x : Fin k → Bool) :
    (label p a b).vale x = p.read (x a) (x b) := by
  rcases p with ⟨s,t⟩
  cases s <;> rfl

theorem emit_spec {k : Nat} (e : Net) (a b : Fin k) (h : Fin (joints e) → Fin k)
    (x : Fin k → Bool) :
    evaluate (emit e a b h) x = value e (x a) (x b) (unpack e (fun i => x (h i))) := by
  induction e generalizing a b with
  | clause p q => simp [emit,evaluate,satisfeita,label_read,value]
  | series l r hl hr => simp only [emit,eval_append,hl,hr,value,unpack]
  | parallel l r hl hr => simp only [emit,eval_append,hl,hr,value,unpack]

def assignment (e : Net) (a b : Bool) (w : Witness e) : Fin (joints e + 2) → Bool :=
  Fin.cases a (Fin.cases b (pack e w))

theorem cnf_witness (e : Net) (a b : Bool) (w : Witness e) :
    evaluate (cnf e) (assignment e a b w) = value e a b w := by
  unfold cnf
  rw [emit_spec]
  change value e a b (unpack e (fun i => pack e w i)) = _
  rw [witness_roundtrip]

theorem all_values (e : Net) (z : Bool) :
    result (summary e) z = true ↔ ∃ x, evaluate (cnf e) x = z := by
  rw [result_spec]
  constructor
  · rintro ⟨a,b,w,h⟩
    exact ⟨assignment e a b w,(cnf_witness e a b w).trans h⟩
  · rintro ⟨x,h⟩
    unfold cnf at h
    rw [emit_spec] at h
    exact ⟨_,_,_,h⟩

private theorem cost_zero {k : Nat} (p : CNF k) (x : Fin k → Bool) :
    custoCNF p x = 0 ↔ evaluate p x = true := by
  rw [custoCNF_zero_sse]
  simp [evaluate,List.all_eq_true]

theorem network_word (e : Net) :
    result (summary e) true = palavraDaFormula (cnf e) := by
  apply Bool.eq_iff_iff.mpr
  rw [all_values,a_palavra_e_o_sat]
  simp [SAT,evaluate,List.all_eq_true]

theorem network_verb (e : Net) (t : ℝ) :
    result (summary e) false = true ↔ verboDaFormula (cnf e) t = 1 := by
  rw [all_values]
  have hp := a_descida_e_positiva_sse_ha_o_que_ler (cnf e) t
  by_cases bad : ∃ x, evaluate (cnf e) x = false
  · have hz : ∃ x, custoCNF (cnf e) x ≠ 0 := by
      obtain ⟨x,h⟩ := bad
      exact ⟨x, fun q => Bool.noConfusion (h.symm.trans ((cost_zero _ _).mp q))⟩
    exact ⟨fun _ => sign_pos (hp.mpr hz),fun _ => bad⟩
  · have hnp : ¬ 0 < descida (cnf e) t := by
      intro h
      obtain ⟨x,hx⟩ := hp.mp h
      apply bad
      refine ⟨x,?_⟩
      cases h : evaluate (cnf e) x
      · rfl
      · exact (hx ((cost_zero _ _).2 h)).elim
    have zero := le_antisymm (le_of_not_gt hnp) (a_descida_nunca_e_negativa (cnf e) t)
    unfold verboDaFormula
    rw [zero,sign_zero]
    simp [bad]

theorem network_psibit (e : Net) (t : ℝ) :
    (result (summary e) true, if result (summary e) false then (1 : SignType) else 0) =
      psibitDaFormula (cnf e) t := by
  apply Prod.ext (network_word e)
  change (if result (summary e) false then (1 : SignType) else 0) = verboDaFormula (cnf e) t
  cases hb : result (summary e) false
  · have no : ¬ 0 < descida (cnf e) t := by
      intro hp
      have hs : verboDaFormula (cnf e) t = 1 := sign_pos hp
      have yes := (network_verb e t).mpr hs
      simp [hb] at yes
    have hz := le_antisymm (le_of_not_gt no) (a_descida_nunca_e_negativa (cnf e) t)
    simp [verboDaFormula,hz]
  · exact ((network_verb e t).mp hb).symm

private theorem emit_size {k : Nat} (e : Net) (a b : Fin k) (h : Fin (joints e) → Fin k) :
    (emit e a b h).length = leaves e ∧ ∀ c ∈ emit e a b h, c.length = 2 := by
  induction e generalizing a b with
  | clause p q => simp [emit,leaves]
  | series l r hl hr =>
    simp only [emit,leaves,List.length_append,List.mem_append]
    obtain ⟨ll,lc⟩ := hl a (h (0 : Fin (joints l + joints r + 1))) (fun i => h (leftIndex (joints r) i).succ)
    obtain ⟨rl,rc⟩ := hr (h (0 : Fin (joints l + joints r + 1))) b (fun i => h (rightIndex (joints l) i).succ)
    exact ⟨congrArg₂ (·+·) ll rl,fun c hc => hc.elim (lc c) (rc c)⟩
  | parallel l r hl hr =>
    simp only [emit,leaves,List.length_append,List.mem_append]
    obtain ⟨ll,lc⟩ := hl a b (fun i => h (leftIndex (joints r) i))
    obtain ⟨rl,rc⟩ := hr a b (fun i => h (rightIndex (joints l) i))
    exact ⟨congrArg₂ (·+·) ll rl,fun c hc => hc.elim (lc c) (rc c)⟩

theorem variables_bound (e : Net) : joints e + 1 ≤ leaves e := by
  induction e with
  | clause p q => exact Nat.le_refl 1
  | series l r hl hr => simp only [joints,leaves]; omega
  | parallel l r hl hr => simp only [joints,leaves]; omega

theorem cnf_size (e : Net) :
    (cnf e).length = leaves e ∧ (∀ c ∈ cnf e, c.length = 2) ∧ joints e + 2 ≤ leaves e + 1 :=
  ⟨(emit_size e ..).1,(emit_size e ..).2,by have := variables_bound e; omega⟩

end IALD.RedeComoCNF

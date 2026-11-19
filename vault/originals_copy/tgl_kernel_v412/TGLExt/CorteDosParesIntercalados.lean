import TGLExt.CorteDosParesCruzados
import TGLExt.InformacaoDoResumo
import TGLExt.OPsiBitDaFormula

set_option autoImplicit false

namespace Codex.CrossedPairStream

open IALD.CorrelacoesDistintas (pairStream pairStream_length)
open IALD.LeitorDaFormula Codex.CrossedPairCut Codex.PairCut

inductive Mode
  | start
  | anchor (control : Bool)
  | ready (control : Bool)
  | expect (control value : Bool)
  | dead
  deriving DecidableEq, Fintype

/-- Um símbolo binário por transição; o controle é guardado durante toda a leitura. -/
def step : Mode → Bool → Mode
  | .start, b => .anchor b
  | .anchor s, b => if s == b then .ready s else .dead
  | .ready s, a => .expect s (Bool.xor s a)
  | .expect s e, b => if e == b then .ready s else .dead
  | .dead, _ => .dead

def marked (s ok : Bool) : Mode := if ok then .ready s else .dead

private theorem step_pair (s ok a b : Bool) :
    step (step (marked s ok) a) b = marked s (ok && (Bool.xor s a == b)) := by
  cases s <;> cases ok <;> cases a <;> cases b <;> rfl

private theorem after_pairs {n : ℕ} (u v : Bits n) (is : List (Fin n)) (s ok : Bool) :
    (pairStream u v is).foldl step (marked s ok) =
      marked s (ok && is.all (fun i => Bool.xor s (u i) == v i)) := by
  induction is generalizing ok with
  | nil => simp [pairStream]
  | cons i is ih =>
    change (pairStream u v is).foldl step (step (step (marked s ok) (u i)) (v i)) = _
    rw [step_pair, ih, List.all_cons, Bool.and_assoc]

def stream {n : ℕ} (u v : Bits (n+1)) : List Bool :=
  [u 0,v 0] ++ pairStream (fun i : Fin n => u i.succ) (fun i => v i.succ) (List.finRange n)

/-- Este leitor recebe a atribuição na ordem de pares, com a fórmula da família
fixada. O comprimento é o número de transições do fold no fluxo apresentado. -/
theorem interleaved_exact {n : ℕ} (u v : Bits (n+1)) :
    ((stream u v).foldl step .start = .ready (u 0) ↔
       passes (crossedFormula n) (Fin.append u v) = true) ∧
      (stream u v).length = 2 * (n+1) ∧ Fintype.card Mode = 10 := by
  refine ⟨?_, ?_, by decide⟩
  · rw [crossed_spec]
    change (pairStream (fun i : Fin n => u i.succ) (fun i => v i.succ) (List.finRange n)).foldl step
      (marked (u 0) (u 0 == v 0)) = _ ↔ _
    rw [after_pairs]
    have accepted (b : Bool) : marked (u 0) b = .ready (u 0) ↔ b = true := by
      cases b <;> simp [marked]
    rw [accepted, Bool.and_eq_true, List.all_eq_true]
    simp only [beq_iff_eq, List.mem_finRange, true_implies]
    constructor
    · rintro ⟨h0, hd⟩
      funext i
      exact Fin.cases (motive := fun j => v j = transform u j) h0.symm (fun j => (hd j).symm) i
    · rintro rfl
      exact ⟨rfl,fun _ => rfl⟩
  · simp [stream, pairStream_length, Nat.mul_add, Nat.add_comm]
    omega

/-- As cláusulas unitárias fixam os dois blocos. A avaliação passa então a ser
a própria Palavra de uma família de CNFs, com os mesmos retângulos de consulta. -/
theorem pinned_word {n : ℕ} (u v : Bits (n+1)) :
    TGLExt.OPsiBitDaFormula.palavraDaFormula
      (crossedFormula n ++ IALD.InformacaoDoResumo.isolate (Fin.append u v)) = true ↔
        v = transform u := by
  rw [TGLExt.OPsiBitDaFormula.a_palavra_e_o_sat, IALD.InformacaoDoResumo.append_isolate, crossed_spec]

end Codex.CrossedPairStream

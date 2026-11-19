import TGLExt.ClausulaComoResposta
import TGLExt.TransporteDaInscricao
import TGLExt.EcoDaAtribuicao

/-! The learned object is the original signed clause. Each reply is sent
on its own binary PsiBit channel. The source starts on the selected clause.
Framing, search, proposal production and preparation of that source tape
are separate operations. No concatenated transcript is supplied for free. -/
set_option autoImplicit false
namespace Codex.ClauseChannel
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha Codex.InscriptionWire Codex.ClauseReply
variable {n : Nat}

def replyMoves (rewind : Bool) (c : Clausula n) : Nat :=
  let w := spellClause c
  let k := 2*w.length+1
  shifts txStep txMoved k (.fetch w []) +
    (if rewind then (encode w).length else 0) +
    shifts rxStep rxMoved k (.first (encode w) [])

theorem receive_clause (c : Clausula n) :
    let w := spellClause c
    rxStep^[2*w.length+1] (.first (encode w) []) = .stop w.reverse := by
  simpa using (receive (spellClause c) []).1

private theorem price (rewind : Bool) (c : Clausula n) :
    replyMoves rewind c = (if rewind then 8 else 6)*(spellClause c).length := by
  have tx := (transmit (spellClause c) []).2
  have rx := (receive (spellClause c) []).2
  cases rewind <;> simp [replyMoves,tx,rx,encoded_length] <;> omega

private theorem all_prices (r : Bool) (cs : CNF n) :
    (cs.map (replyMoves r)).sum = (if r then 8 else 6)*(original cs).length := by
  induction cs with
  | nil => simp [original]
  | cons c cs ih =>
    change replyMoves r c + (cs.map (replyMoves r)).sum =
      (if r then 8 else 6)*(spellClause c ++ original cs).length
    rw [price, ih, List.length_append, Nat.mul_add]

/-- The sum counts the actual head shifts for each returned packet, including
its own rewind when requested. No hypothesis about proposal quality is needed. -/
theorem feedback_budget (rewind : Bool) (p : Proposer n) (a b : CNF n) :
    ((protocol p a b).replies.map (replyMoves rewind)).sum ≤
      (if rewind then 8 else 6)*(original b).length := by
  rw [all_prices]
  exact Nat.mul_le_mul_left _ (reply_bounds p (b.length+1) a b).2

/-- The bottleneck already occurs on the special split with no remote clauses. -/
theorem no_pending_challenge (p : Proposer n) (a : CNF n) :
    (protocol p a []).calls = 1 ∧
    (∀ x, (protocol p a []).result = .found x ↔ p a = some x) := by
  cases h : p a <;> simp [protocol, run, inspect, h]

end Codex.ClauseChannel

import TGLExt.PolinomioPorEscolha

/-! Direct syntactic Horn recognition: signs may be interleaved arbitrarily;
the negative list retains order and multiplicity. -/
set_option autoImplicit false
namespace Codex.HornResidual
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open Codex.HornCross Codex.CrossSelectors Codex.PolinomioPorEscolha Codex.SparseHornTape
variable {n : Nat}

def parseClause (c : Clausula n) : Option (Rule n) :=
  match names c true with
  | [] => some ⟨names c false,none⟩
  | [i] => some ⟨names c false,some i⟩
  | _ :: _ :: _ => none

def parseProgram : CNF n → Option (List (Rule n))
  | [] => some []
  | c :: p =>
    match parseClause c, parseProgram p with
    | some r, some q => some (r :: q)
    | _, _ => none

theorem parse_clause_iff (c : Clausula n) :
    (∃ r, parseClause c = some r) ↔ (names c true).length ≤ 1 := by
  cases hp : names c true with
  | nil => simp [parseClause,hp]
  | cons i is => cases is <;> simp [parseClause,hp]

theorem parsed_parts {c : Clausula n} {r : Rule n} (h : parseClause c = some r) :
    r.body = names c false ∧ r.head.toList = names c true := by
  cases hp : names c true with
  | nil => simp [parseClause,hp] at h; subst r; simp
  | cons i is =>
    cases is with
    | nil => simp [parseClause,hp] at h; subst r; simp
    | cons j js => simp [parseClause,hp] at h

private theorem clause_unique {c : Clausula n} {r : Rule n} (h : parseClause c = some r) :
    alternatives c = [r] := by
  cases hp : names c true with
  | nil => simp [parseClause,hp] at h; subst r; simp [alternatives,hp]
  | cons i is =>
    cases is with
    | nil => simp [parseClause,hp] at h; subst r; simp [alternatives,hp]
    | cons j js => simp [parseClause,hp] at h

theorem parse_iff (p : CNF n) :
    (∃ q, parseProgram p = some q) ↔ ∀ c ∈ p, (names c true).length ≤ 1 := by
  induction p with
  | nil => simp [parseProgram]
  | cons c p ih =>
    rw [List.forall_mem_cons,← parse_clause_iff,← ih]
    cases hc : parseClause c <;> cases hp : parseProgram p <;> simp [parseProgram,hc,hp]

theorem sole_program {p : CNF n} {q : List (Rule n)} (h : parseProgram p = some q) :
    programs p = [q] := by
  induction p generalizing q with
  | nil => simp [parseProgram] at h; subst q; rfl
  | cons c p ih =>
    cases hc : parseClause c with
    | none => simp [parseProgram,hc] at h
    | some r =>
      cases hp : parseProgram p with
      | none => simp [parseProgram,hc,hp] at h
      | some tail =>
        simp [parseProgram,hc,hp] at h
        subst q
        simp [programs,clause_unique hc,ih hp]

theorem parse_word {p : CNF n} {q : List (Rule n)} (h : parseProgram p = some q) :
    palavraDaFormula p = checkProgram q := by
  rw [← selector_word,scan_spec,sole_program h]
  simp

theorem parse_size {p : CNF n} {q : List (Rule n)} (h : parseProgram p = some q) :
    (program q).length ≤ (original p).length :=
  selected_length p q (by rw [sole_program h]; simp)

end Codex.HornResidual

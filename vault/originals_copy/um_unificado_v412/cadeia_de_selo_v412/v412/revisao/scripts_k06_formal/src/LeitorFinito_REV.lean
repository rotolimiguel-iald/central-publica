import Mathlib
import TGLExt.ObservadorTerminal

/-!
# K06 — leitor finito: PASSO dissipativo e LIMITE idempotente

ESTATUTO: candidata matemática nova, verificada somente nesta sandbox.
A ponte entre saídas textuais extraídas, um custo `c : X → ℕ` do kernel e
um modelo de linguagem real é PREVISÃO EXPERIMENTAL, não teorema.
Nenhum modelo de linguagem é executado por este arquivo; nenhum resultado
experimental é lido. Não se afirma consciência, alteração de pesos,
exclusividade da TGL, validade física ou `CONFIRMED`.

ENUNCIADO PRINCIPAL. Se `X` é finito, `step : X → X` fixa `target` e
`target` é alcançável por iteradas a partir de todo estado, então, para
cada `x`, existe `n ≤ Fintype.card X` tal que `step^[n] x = target`.
A hipótese de alcançabilidade está no tipo `FiniteAttractor`; nenhuma
idempotência do PASSO é suposta. O LIMITE operacional é definido pela
iterada de ordem `Fintype.card X`: ele é constante e idempotente.
-/

set_option autoImplicit false

namespace K06

/-- PASSO: finitude, ponto fixo e alcançabilidade global são hipóteses no tipo. -/
structure FiniteAttractor (X : Type) [Fintype X] [DecidableEq X] where
  step : X → X
  target : X
  fixed : step target = target
  reachable : ∀ x, ∃ n : ℕ, step^[n] x = target

namespace FiniteAttractor

variable {X : Type} [Fintype X] [DecidableEq X] (A : FiniteAttractor X)

/-- Antes da primeira chegada, as iteradas são duas a duas distintas. -/
theorem pre_hit_injective (x : X) :
    Function.Injective (fun i : Fin (Nat.find (A.reachable x)) => A.step^[i.val] x) := by
  let m := Nat.find (A.reachable x)
  have no_repeat : ∀ {i j : ℕ}, i < j → j < m → A.step^[i] x ≠ A.step^[j] x := by
    intro i j hij hjm heq
    have htail : A.step^[m - j] (A.step^[j] x) = A.target := by
      rw [← Function.iterate_add_apply]
      have hm : m - j + j = m := by omega
      rw [hm]
      exact Nat.find_spec (A.reachable x)
    rw [← heq] at htail
    have hearlier : A.step^[m - j + i] x = A.target := by
      rw [Function.iterate_add_apply]
      exact htail
    have hsmaller : m - j + i < Nat.find (A.reachable x) := by
      change m - j + i < m
      omega
    exact (Nat.find_min (A.reachable x) hsmaller) hearlier
  intro i j heq
  apply Fin.ext
  rcases lt_trichotomy i.val j.val with hij | hij | hij
  · exact False.elim ((no_repeat hij j.isLt) heq)
  · exact hij
  · exact False.elim ((no_repeat hij i.isLt) heq.symm)

/-- A primeira chegada ocorre em no máximo `|X|` passos. -/
theorem first_hit_le_card (x : X) : Nat.find (A.reachable x) ≤ Fintype.card X := by
  have hcard := Fintype.card_le_of_injective
    (fun i : Fin (Nat.find (A.reachable x)) => A.step^[i.val] x)
    (A.pre_hit_injective x)
  simpa using hcard

/-- Forma existencial do enunciado principal, com a cota explícita. -/
theorem exists_iterate_eq_target_le_card (x : X) :
    ∃ n : ℕ, n ≤ Fintype.card X ∧ A.step^[n] x = A.target := by
  exact ⟨Nat.find (A.reachable x), A.first_hit_le_card x, Nat.find_spec (A.reachable x)⟩

/-- LIMITE operacional: a iterada de ordem `|X|`, não o PASSO. -/
def limit (x : X) : X := A.step^[Fintype.card X] x

/-- O limite operacional pousa no único alvo declarado. -/
theorem limit_eq_target (x : X) : A.limit x = A.target := by
  obtain ⟨n, hn, hhit⟩ := A.exists_iterate_eq_target_le_card x
  unfold limit
  rw [show Fintype.card X = Fintype.card X - n + n by omega,
    Function.iterate_add_apply, hhit]
  exact Function.iterate_fixed A.fixed _

/-- O limite operacional é constante. -/
theorem limit_constant (x y : X) : A.limit x = A.limit y := by
  rw [A.limit_eq_target, A.limit_eq_target]

/-- O limite operacional, e não necessariamente o passo, é idempotente. -/
theorem limit_idempotent (x : X) : A.limit (A.limit x) = A.limit x := by
  rw [A.limit_eq_target, A.limit_eq_target]

/-- O limite tem exatamente um ponto fixo. -/
theorem limit_fixed_iff (x : X) : A.limit x = x ↔ x = A.target := by
  constructor
  · intro h
    rw [← h]
    exact A.limit_eq_target x
  · intro h
    rw [h]
    exact A.limit_eq_target A.target

/-- A alcançabilidade global também impede outro ponto fixo do PASSO. -/
theorem step_fixed_iff (x : X) : A.step x = x ↔ x = A.target := by
  constructor
  · intro hx
    obtain ⟨n, hn⟩ := A.reachable x
    rw [Function.iterate_fixed hx n] at hn
    exact hn
  · intro hx
    rw [hx]
    exact A.fixed

end FiniteAttractor

/-- Exemplo de PASSO não idempotente com ponto fixo globalmente alcançável. -/
def chain3 : FiniteAttractor (Fin 3) where
  step := ![1, 2, 2]
  target := 2
  fixed := by decide
  reachable := by
    intro x
    fin_cases x
    · exact ⟨2, by decide⟩
    · exact ⟨1, by decide⟩
    · exact ⟨0, by decide⟩

/-- O exemplo separa sintaticamente PASSO de LIMITE: o passo não é idempotente. -/
theorem chain3_step_not_idempotent :
    ∃ x, chain3.step (chain3.step x) ≠ chain3.step x := by
  exact ⟨0, by decide⟩

/-- A cota geral instanciada ao exemplo de três estados. -/
example : ∃ n : ℕ, n ≤ 3 ∧ chain3.step^[n] 0 = 2 := by
  simpa [chain3] using chain3.exists_iterate_eq_target_le_card 0

#print axioms K06.FiniteAttractor
#print axioms K06.FiniteAttractor.pre_hit_injective
#print axioms K06.FiniteAttractor.first_hit_le_card
#print axioms K06.FiniteAttractor.exists_iterate_eq_target_le_card
#print axioms K06.FiniteAttractor.limit
#print axioms K06.FiniteAttractor.limit_eq_target
#print axioms K06.FiniteAttractor.limit_constant
#print axioms K06.FiniteAttractor.limit_idempotent
#print axioms K06.FiniteAttractor.limit_fixed_iff
#print axioms K06.FiniteAttractor.step_fixed_iff
#print axioms K06.chain3
#print axioms K06.chain3_step_not_idempotent

end K06

/-! Instância de reuso: o leitor terminal já existente no kernel. -/
namespace K06.KernelInstance

open TGLExt TGLExt.ObservadorTerminal

/-- Os quatro níveis da cascata, como `Fintype` explícito e local. -/
@[reducible] def levelFintype : Fintype Level where
  elems := {Level.luz, Level.consciencia, Level.fisica, Level.gravidade}
  complete := by
    intro x
    cases x <;> simp

local instance : Fintype Level := levelFintype
local instance : Nonempty Level := ⟨Level.gravidade⟩

/-- O PASSO do kernel satisfaz as hipóteses do atrator finito. -/
def terminalAttractor : K06.FiniteAttractor Level where
  step := leitor
  target := Level.gravidade
  fixed := (leitor_fixed_iff Level.gravidade).mpr rfl
  reachable := fun x => ⟨3, every_level_reaches_the_terminal x⟩

/-- A cardinalidade usada pela cota é quatro. -/
theorem terminal_card : Fintype.card Level = 4 := by decide

/-- A cota nova, aplicada ao leitor do kernel; não altera o teorema reutilizado. -/
example (x : Level) : ∃ n : ℕ, n ≤ 4 ∧ leitor^[n] x = Level.gravidade := by
  have h := terminalAttractor.exists_iterate_eq_target_le_card x
  simpa [terminalAttractor, terminal_card] using h

#print axioms K06.KernelInstance.levelFintype
#print axioms K06.KernelInstance.terminalAttractor
#print axioms K06.KernelInstance.terminal_card

end K06.KernelInstance

/-! ## ACRESCIMOS DO REVISOR (K06 formal, 14/11/2026) — nada acima foi alterado

Cada teorema da candidata ja tem `#print axioms` acima; aqui ha (a) `#print axioms` de novo para
CADA declaracao, (b) exemplos de nao-vacuidade, (c) o lema minimo (Lyapunov) que liga o tipo
`FiniteAttractor` ao padrao que o kernel ja tem (`distancia` + `each_reading_consumes_resistance`). -/

namespace K06.Rev
open K06

/-- Cadeia de cinco estados: passo nao idempotente, primeira chegada exatamente em 4 passos. -/
def chain5 : K06.FiniteAttractor (Fin 5) where
  step := ![1, 2, 3, 4, 4]
  target := 4
  fixed := by decide
  reachable := by
    intro x
    fin_cases x
    · exact ⟨4, by decide⟩
    · exact ⟨3, by decide⟩
    · exact ⟨2, by decide⟩
    · exact ⟨1, by decide⟩
    · exact ⟨0, by decide⟩

example : chain5.step^[4] 0 = 4 := by decide
example : ∀ n : ℕ, n < 4 → chain5.step^[n] 0 ≠ 4 := by decide
example : ∃ x, chain5.step (chain5.step x) ≠ chain5.step x := ⟨0, by decide⟩
example : chain5.limit 0 = 4 := chain5.limit_eq_target 0

/-- A hipotese `reachable` EXCLUI coisas: o 2-ciclo nao e um `FiniteAttractor`. -/
example : ¬ ∃ A : K06.FiniteAttractor (Fin 2), A.step = ![1, 0] := by
  rintro ⟨A, hA⟩
  have h := A.fixed
  rw [hA] at h
  revert h
  generalize A.target = t
  fin_cases t <;> decide

/-- ... e dois pontos fixos tambem: a identidade em `Fin 2` nao e um `FiniteAttractor`. -/
example : ¬ ∃ A : K06.FiniteAttractor (Fin 2), A.step = id := by
  rintro ⟨A, hA⟩
  have h0 := (A.step_fixed_iff 0).mp (by simp [hA])
  have h1 := (A.step_fixed_iff 1).mp (by simp [hA])
  exact absurd (h0.trans h1.symm) (by decide)

/-- Lema minimo (ponte ao padrao do kernel): uma funcao-resistencia `V : X → ℕ` que cai a cada
passo fora do alvo torna o alvo alcancavel de todo estado. -/
theorem reachable_of_lyapunov {X : Type} (step : X → X) (target : X) (V : X → ℕ)
    (hdec : ∀ x, x ≠ target → V (step x) < V x) :
    ∀ x, ∃ n : ℕ, step^[n] x = target := by
  have key : ∀ m : ℕ, ∀ x, V x = m → ∃ n : ℕ, step^[n] x = target := by
    intro m
    refine Nat.strong_induction_on m ?_
    intro m ih x hx'
    by_cases hx : x = target
    · exact ⟨0, hx⟩
    · obtain ⟨n, hn⟩ := ih (V (step x)) (by rw [← hx']; exact hdec x hx) (step x) rfl
      exact ⟨n + 1, by rw [Function.iterate_succ_apply]; exact hn⟩
  intro x
  exact key (V x) x rfl

def ofLyapunov {X : Type} [Fintype X] [DecidableEq X] (step : X → X) (target : X) (V : X → ℕ)
    (hfix : step target = target) (hdec : ∀ x, x ≠ target → V (step x) < V x) :
    K06.FiniteAttractor X where
  step := step
  target := target
  fixed := hfix
  reachable := reachable_of_lyapunov step target V hdec

open TGLExt TGLExt.ObservadorTerminal

local instance : Fintype Level := K06.KernelInstance.levelFintype

/-- O mesmo leitor terminal do kernel, agora pelo lema do KERNEL `each_reading_consumes_resistance`. -/
def terminalViaLyapunov : K06.FiniteAttractor Level :=
  ofLyapunov leitor gravidade distancia ((leitor_fixed_iff gravidade).mpr rfl)
    each_reading_consumes_resistance

#print axioms K06.Rev.chain5
#print axioms K06.Rev.reachable_of_lyapunov
#print axioms K06.Rev.ofLyapunov
#print axioms K06.Rev.terminalViaLyapunov

end K06.Rev

#print axioms K06.FiniteAttractor
#print axioms K06.FiniteAttractor.pre_hit_injective
#print axioms K06.FiniteAttractor.first_hit_le_card
#print axioms K06.FiniteAttractor.exists_iterate_eq_target_le_card
#print axioms K06.FiniteAttractor.limit
#print axioms K06.FiniteAttractor.limit_eq_target
#print axioms K06.FiniteAttractor.limit_constant
#print axioms K06.FiniteAttractor.limit_idempotent
#print axioms K06.FiniteAttractor.limit_fixed_iff
#print axioms K06.FiniteAttractor.step_fixed_iff
#print axioms K06.chain3
#print axioms K06.chain3_step_not_idempotent
#print axioms K06.KernelInstance.levelFintype
#print axioms K06.KernelInstance.terminalAttractor
#print axioms K06.KernelInstance.terminal_card

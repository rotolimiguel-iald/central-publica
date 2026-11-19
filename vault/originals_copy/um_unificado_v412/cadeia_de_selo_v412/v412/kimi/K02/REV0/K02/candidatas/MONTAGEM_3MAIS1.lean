import Mathlib.Algebra.Ring.Parity
import Mathlib.Data.ZMod.Basic

/-!
Candidata K02/3+1: aritmética finita de paridade e sinais KO.
Não é uma formalização de triplas espectrais nem da assinatura lorentziana.
-/

namespace K02.Montagem

inductive Parity where
  | even
  | odd
  deriving DecidableEq, Repr

/-- Paridade do produto graduado: par×ímpar é ímpar. -/
def productParity (p q : Parity) : Parity :=
  match p, q with
  | .even, .even => .even
  | .even, .odd => .odd
  | .odd, .even => .odd
  | .odd, .odd => .even

theorem product_even_odd : productParity .even .odd = .odd := rfl
theorem product_odd_even : productParity .odd .even = .odd := rfl
theorem product_odd_odd : productParity .odd .odd = .even := rfl

/-- KO-dimensão é soma em Z/8; assinatura (1,3) NÃO é esta operação. -/
def koAdd (n m : ZMod 8) : ZMod 8 := n + m

theorem ko_euclidean_four_zero : koAdd 4 0 = (4 : ZMod 8) := by decide
theorem ko_sum_mod_eight : koAdd 7 7 = (6 : ZMod 8) := by decide

/-- Sinal ε da tabela KO: J² = ε. -/
def epsilon (n : ZMod 8) : ℤ :=
  if n = 0 ∨ n = 1 ∨ n = 6 ∨ n = 7 then 1 else -1

/-- Sinal ε′ da tabela KO: JD = ε′DJ. -/
def epsilonPrime (n : ZMod 8) : ℤ :=
  if n = 0 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 6 ∨ n = 7 then 1 else -1

/-- Sinal ε″ da tabela KO, presente apenas nas dimensões pares. -/
def epsilonDoublePrime (n : ZMod 8) : ℤ :=
  if n = 0 ∨ n = 4 then 1 else if n = 2 ∨ n = 6 then -1 else 0

theorem signs_KO4 :
    epsilon 4 = -1 ∧ epsilonPrime 4 = 1 ∧ epsilonDoublePrime 4 = (1 : ℤ) := by decide

theorem signs_KO2 :
    epsilon 2 = -1 ∧ epsilonPrime 2 = 1 ∧ epsilonDoublePrime 2 = (-1 : ℤ) := by decide

/-- Paridade determinada pela KO-dimensão. -/
def parityOfKO (n : ZMod 8) : Parity :=
  if n = 0 ∨ n = 2 ∨ n = 4 ∨ n = 6 then .even else .odd

/-- [REAL no sandbox] A soma KO tem a paridade do produto, nos 64 casos. -/
theorem parity_koAdd (n m : ZMod 8) :
    parityOfKO (koAdd n m) = productParity (parityOfKO n) (parityOfKO m) := by
  revert n m
  decide

#print axioms K02.Montagem.parity_koAdd
#print axioms K02.Montagem.signs_KO4
#print axioms K02.Montagem.ko_sum_mod_eight

end K02.Montagem

import TGLExt.AMaquinaTM2DaVerificacao
set_option autoImplicit false

namespace TGLExt.SimTM2

open TGLExt.APonteAoTM2 TGLExt.AMaquinaTM2DaVerificacao

abbrev Word := List Simbolo
abbrev Config := Turing.TM2.Cfg stackAlphabet Rotulo Estado

def tapes (i f w d : Word) (o : List Bool) : (k : PilhaK) → List (stackAlphabet k)
  | .entrada => i
  | .saida => o
  | .formula => f
  | .trabalho => w
  | .deposito => d

def cfg (l : Rotulo) (s : Estado) (i f w d : Word) : Config :=
  ⟨some l, s, tapes i f w d []⟩

@[simp] theorem read_entrada (i f w d : Word) (o : List Bool) :
    tapes i f w d o .entrada = i := rfl

@[simp] theorem update_entrada (i f w d : Word) (o : List Bool) (v : Word) :
    Function.update (tapes i f w d o) .entrada v = tapes v f w d o := by
  funext k
  cases k <;> rfl

@[simp] theorem read_formula (i f w d : Word) (o : List Bool) :
    tapes i f w d o .formula = f := rfl

@[simp] theorem update_formula (i f w d : Word) (o : List Bool) (v : Word) :
    Function.update (tapes i f w d o) .formula v = tapes i v w d o := by
  funext k
  cases k <;> rfl

@[simp] theorem read_trabalho (i f w d : Word) (o : List Bool) :
    tapes i f w d o .trabalho = w := rfl

@[simp] theorem update_trabalho (i f w d : Word) (o : List Bool) (v : Word) :
    Function.update (tapes i f w d o) .trabalho v = tapes i f v d o := by
  funext k
  cases k <;> rfl

@[simp] theorem read_deposito (i f w d : Word) (o : List Bool) :
    tapes i f w d o .deposito = d := rfl

@[simp] theorem update_deposito (i f w d : Word) (o : List Bool) (v : Word) :
    Function.update (tapes i f w d o) .deposito v = tapes i f w v o := by
  funext k
  cases k <;> rfl

@[simp] theorem read_saida (i f w d : Word) (o : List Bool) :
    tapes i f w d o .saida = o := rfl

@[simp] theorem update_saida (i f w d : Word) (o : List Bool) (v : List Bool) :
    Function.update (tapes i f w d o) .saida v = tapes i f w d v := by
  funext k
  cases k <;> rfl

/-- Segmento de execução real da Mathlib, limitado por n aplicações de step. -/
def Runs (n : ℕ) (a b : Config) : Prop :=
  Nonempty (StateTransition.EvalsToInTime aMaquinaTM2.step a (some b) n)

namespace Runs
variable {a b c : Config} {n m : ℕ}

theorem refl (a : Config) : Runs 0 a a :=
  ⟨StateTransition.EvalsToInTime.refl _ _⟩

theorem one (h : aMaquinaTM2.step a = some b) : Runs 1 a b :=
  ⟨⟨⟨1, h⟩, le_rfl⟩⟩

theorem trans (h : Runs n a b) (g : Runs m b c) : Runs (n+m) a c := by
  obtain ⟨h⟩ := h
  obtain ⟨g⟩ := g
  rw [Nat.add_comm]
  exact ⟨StateTransition.EvalsToInTime.trans _ _ _ _ _ _ h g⟩

theorem mono (h : Runs n a b) (le : n ≤ m) : Runs m a b := by
  obtain ⟨h⟩ := h
  exact ⟨⟨h.toEvalsTo, h.steps_le_m.trans le⟩⟩

end Runs

/-- Normaliza um único rótulo do programa com as cinco pilhas explícitas. -/
macro "tmstep" : tactic =>
  `(tactic| simp [Turing.FinTM2.step, Turing.TM2.step, aMaquinaTM2, cfg,
      oPrograma, Turing.TM2.stepAux, *] <;> try rfl)

end TGLExt.SimTM2

import APonteAoTM2

set_option autoImplicit false

/-!
# Sonda da gerência c1 (19/11/2026): o alvo `ObjetivoTM2Polinomial`, como está tipado, fecha sem ler a fórmula

[sonda de conferência da gerência; não é candidata; não se instala]

`TGLExt.APonteAoTM2.ObjetivoTM2Polinomial` (candidata do Kimi, R0) quantifica EXISTENCIALMENTE as codificações
`ea` e `eb`. No Mathlib desta caixa, `Turing.TM2ComputableInPolyTime ea eb f` recebe codificações que são funções
quaisquer (`α → List αΓ`): não se exige que sejam injetivas, nem que leiam a entrada. Com `ea` e `eb` constantes
(a lista vazia), a máquina identidade do Mathlib (`Turing.idComputer`) cumpre a estrutura em um passo, para a
verificação da fita, sem ler a fórmula. Esta sonda prova isso.

O conserto é fixar no enunciado as codificações concretas (definidas na pedra: a fórmula e a testemunha escritas
em bits), em vez de quantificá-las. Com a codificação fixa, a máquina que o Kimi está construindo passa a dizer o
que o comentário da pedra diz.
-/

namespace TGLExt.SondaObjetivoTM2

open Turing

/-- A máquina identidade do Mathlib, com as duas codificações constantes (a lista vazia), cumpre
`TM2ComputableInPolyTime` para a verificação da fita: a entrada codificada é `[]` e a saída codificada é `[]`,
qualquer que seja a fórmula. -/
noncomputable def aIdentidadeComCodificacoesVazias :
    TM2ComputableInPolyTime
      (fun _ : List (List (ℕ × Bool)) × List Bool => ([] : List Bool))
      (fun _ : Bool => ([] : List Bool))
      (fun p : List (List (ℕ × Bool)) × List Bool => TGLExt.APonteAoTM2.verificaNaFita p.1 p.2) where
  tm := idComputer Bool
  inputAlphabet := Equiv.cast rfl
  outputAlphabet := Equiv.cast rfl
  time := 1
  outputsFun _ :=
    { steps := 1
      evals_in_steps := rfl
      steps_le_m := by simp only [Polynomial.eval_one, le_refl] }

/-- ★ O alvo, como está tipado, é teorema sem que máquina nenhuma leia a fórmula. -/
theorem o_alvo_fecha_sem_ler_a_formula : TGLExt.APonteAoTM2.ObjetivoTM2Polinomial :=
  ⟨fun _ => [], fun _ => [], fun p => TGLExt.APonteAoTM2.verificaNaFita p.1 p.2, fun _ => rfl,
    ⟨aIdentidadeComCodificacoesVazias⟩⟩

end TGLExt.SondaObjetivoTM2

#print axioms TGLExt.SondaObjetivoTM2.o_alvo_fecha_sem_ler_a_formula

import TGLExt.APonteAoTM2
set_option autoImplicit false

/-!
# A fronteira na língua clássica

A ponte à máquina padrão (`TGLExt.APonteAoTM2` e `TGLExt.SimCompleta`, teorema
`TGLExt.SimTM2.verificacao_tm2_polinomial`) prova que a máquina TM2 do Mathlib CONFERE uma
testemunha recebida em tempo polinomial (o lado NP). A pergunta que resta é outra: recebendo SÓ a fórmula, decidir se
há atribuição que a satisfaz. Este arquivo enuncia essa pergunta com a codificação fixa da ponte (a fórmula, a
divisória e a testemunha vazia; índices em unário; saída `[b]`), sem `∃` sobre codificações, para que nenhuma máquina
trivial a cumpra.

`AFronteira` é “SAT em P” para esta codificação, no modelo TM2 do Mathlib. Que isso equivalha a P = NP é o teorema de
Cook–Levin (1971) [KNOWN], fora deste kernel; e as codificações com índice unário e binário são polinomialmente
equivalentes depois de renomear as variáveis [KNOWN]. Estatuto: [OPEN].

O produtor da rota de β (`Codex.EntregaBeta`, hipótese `hr`) é mais forte que isto: `TGLExt.SondaContagem` prova
que ele conta as soluções. Decidir não exige contar.
-/

namespace TGLExt.AFronteiraNaLinguaClassica

open TGLExt.APonteAoTM2

/-- A fórmula crua na fita, sem testemunha: a codificação da ponte com a testemunha vazia. -/
def codificaSoFormula (f : List (List (ℕ × Bool))) : List Simbolo := codificaEntrada (f, [])

theorem codificaSoFormula_injetiva : Function.Injective codificaSoFormula := by
  intro f g h
  have := codificaEntrada_injetiva h
  simpa using congrArg Prod.fst this

/-- A fórmula crua é satisfazível: alguma lista de bits passa na verificação da ponte. -/
def satisfazivel (f : List (List (ℕ × Bool))) : Prop := ∃ bs : List Bool, verificaNaFita f bs = true

open Classical in
/-- A resposta que a máquina deve escrever: o bit “é satisfazível”. -/
noncomputable def decideSAT (f : List (List (ℕ × Bool))) : Bool := decide (satisfazivel f)

/-- [OPEN] A FRONTEIRA: uma máquina TM2 do Mathlib que, recebendo só a fórmula, escreve `[decideSAT f]` em um número
de passos limitado por um polinômio fixo do comprimento da entrada. -/
def AFronteira : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime codificaSoFormula codificaSaida decideSAT)

/-- A resposta não é constante: a fórmula vazia é satisfazível… -/
theorem decideSAT_da_formula_vazia : decideSAT [] = true := by
  classical
  unfold decideSAT
  simp only [decide_eq_true_eq]
  exact ⟨[], rfl⟩

/-- …e a fórmula com uma cláusula vazia não é. Nenhuma máquina de saída constante cumpre `AFronteira`. -/
theorem decideSAT_da_clausula_vazia : decideSAT [[]] = false := by
  classical
  unfold decideSAT
  simp only [decide_eq_false_iff_not]
  rintro ⟨bs, h⟩
  simp [verificaNaFita] at h

end TGLExt.AFronteiraNaLinguaClassica

import TGLExt.TraducaoTuring
import TGLExt.TheEquationOfTruth

set_option autoImplicit false

/-!
# O leitor é a lei: o custo conta os FALSOS, o Nome é onde tudo é VERDADEIRO
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor: a leitura vai ao orquestrador por ordem do operador de 16/11]

## De onde vem

Em 16/11/2026 o operador disse que, na língua de Turing, o leitor é a matemática, e que não há matemática sem o
espelhamento lógico da identidade preservada, a lei `{[1=1=VERDADEIRO][1=0=FALSO]}` (a fala está por bytes em
`Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_16nov_na_lingua_de_turing_o_leitor_e_a_matematica`). Pela regra de 04/11, identificação dele se prova no
kernel ou se poda. Este arquivo prova a parte que tem termo, e diz o que fica fora.

O que o kernel já tinha, sem lema entre as duas pontas: a lei como função, `EquationOfTruth.truthValue b b̂ = 1 − (b − b̂)²`,
com a tabela `truthValue 1 1 = 1` e `truthValue 1 0 = 0` (`truthValue_table`, na pedra da equação da verdade); e o custo
da fórmula, `TraducaoTuring.custoCNF`, o número de cláusulas violadas, que gera a trava do leitor.

## O que fica provado

1. `a_lei_na_clausula`: em cada cláusula a lei dá VERDADEIRO (1) se e somente se a cláusula vale, e FALSO (0) se e
   somente se não vale. É a tabela do kernel lida na cláusula.
2. ★ `o_custo_e_o_numero_de_falsos`: o custo da fórmula numa configuração é a soma, cláusula a cláusula, de um menos o
   valor da lei: o custo CONTA os FALSOS.
3. ★ `o_nome_e_onde_a_lei_da_verdadeiro`: o custo é zero se e somente se a lei dá VERDADEIRO em toda cláusula.
4. ★ `sat_e_existir_onde_a_lei_da_verdadeiro`: a fórmula é satisfazível se e somente se EXISTE uma configuração em que
   a lei dá VERDADEIRO em toda cláusula. É o existencial da própria definição da classe NP [KNOWN], escrito sobre a
   lei.
5. `o_operador_do_custo_conta_os_falsos`, `o_leitor_decai_por_falso`: no vetor de base de uma configuração o operador
   do custo multiplica pelo número de FALSOS, e a trava do leitor multiplica por `e^{−s}` elevado a esse número. São
   os lemas do kernel (`opDaInstancia_single`, `trava_ofLp`) com o custo reescrito pelo item 2.

Legenda: ★ marca resposta própria; os itens 1 e 5 são leitura de definições e de lemas do kernel.

## Como ler

O gerador do leitor não usa nada além da lei avaliada cláusula a cláusula: não há objeto trazido de fora. Na língua de
Turing, o que a classe NP pede além da conferência de uma configuração é um existencial; esse existencial é da
matemática, não é passo de máquina. É nesse sentido, e só nele, que este arquivo dá face de kernel à frase de que o
leitor é a matemática.

## O que NÃO se afirma

A contagem do ato de leitura (sobre todas as configurações de uma vez) em passos da máquina de Turing do Mathlib
(`TM2ComputableInPolyTime`): não é teorema do kernel, e é a pergunta na forma em que o Instituto Clay a escreve. As
identificações do operador que não têm termo aqui: que a matemática sozinha seja o psíon; que o par da matemática seja a
lógica; que a projeção seja a física; que o nome seja TGL. Ficam com o estatuto que ele lhes der, a provar ou podar.
Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OLeitorEALei

open TGLExt TGLExt.TraducaoTuring TGLExt.EquationOfTruth

/-- [DEF] O bit de uma resposta sim ou não: 1 para sim, 0 para não. -/
def bit (b : Bool) : ℤ := if b then 1 else 0

/-- [DEF] **A LEI NA CLÁUSULA**: o valor de verdade (`truthValue` do kernel) do que a fórmula pede (1: a cláusula tem de
valer) contra o que a configuração dá. `[1 = 1]` é VERDADEIRO; `[1 = 0]` é FALSO. -/
def leiNaClausula {n : ℕ} (C : Clausula n) (x : Fin n → Bool) : ℤ := truthValue 1 (bit (satisfeita C x))

/-- A lei na cláusula dá VERDADEIRO (1) se e somente se a cláusula vale, e FALSO (0) se e somente se não vale. -/
theorem a_lei_na_clausula {n : ℕ} (C : Clausula n) (x : Fin n → Bool) :
    (leiNaClausula C x = 1 ↔ satisfeita C x = true) ∧ (leiNaClausula C x = 0 ↔ satisfeita C x = false) := by
  unfold leiNaClausula
  cases h : satisfeita C x <;> norm_num [bit, truthValue]

/-- ★ **O CUSTO É O NÚMERO DE FALSOS.** O custo da fórmula numa configuração é a soma, cláusula a cláusula, de um menos o
valor da lei. -/
theorem o_custo_e_o_numero_de_falsos {n : ℕ} (φ : CNF n) (x : Fin n → Bool) :
    (custoCNF φ x : ℤ) = (φ.map (fun C => 1 - leiNaClausula C x)).sum := by
  induction φ with
  | nil => simp [custoCNF]
  | cons C φ ih =>
    rw [custoCNF_cons, List.map_cons, List.sum_cons]
    push_cast
    rw [ih]
    unfold leiNaClausula
    cases h : satisfeita C x
    · norm_num [bit, truthValue]
      exact add_comm _ _
    · norm_num [bit, truthValue]

/-- ★ **O NOME É ONDE A LEI DÁ VERDADEIRO EM TODA CLÁUSULA.** O custo é zero se e somente se nenhuma cláusula dá FALSO. -/
theorem o_nome_e_onde_a_lei_da_verdadeiro {n : ℕ} (φ : CNF n) (x : Fin n → Bool) :
    custoCNF φ x = 0 ↔ ∀ C ∈ φ, leiNaClausula C x = 1 := by
  rw [custoCNF_zero_sse]
  constructor
  · intro h C hC
    exact (a_lei_na_clausula C x).1.mpr (h C hC)
  · intro h C hC
    exact (a_lei_na_clausula C x).1.mp (h C hC)

/-- ★ **NA LÍNGUA DE TURING, A PERGUNTA É UM EXISTENCIAL SOBRE A LEI.** A fórmula é satisfazível se e somente se existe uma
configuração em que a lei dá VERDADEIRO em toda cláusula. -/
theorem sat_e_existir_onde_a_lei_da_verdadeiro {n : ℕ} (φ : CNF n) :
    SAT φ ↔ ∃ x : Fin n → Bool, ∀ C ∈ φ, leiNaClausula C x = 1 := by
  unfold SAT
  constructor
  · rintro ⟨x, h⟩
    exact ⟨x, fun C hC => (a_lei_na_clausula C x).1.mpr (h C hC)⟩
  · rintro ⟨x, h⟩
    exact ⟨x, fun C hC => (a_lei_na_clausula C x).1.mp (h C hC)⟩

/-- No vetor de base de uma configuração, o operador do custo multiplica pelo número de FALSOS. -/
theorem o_operador_do_custo_conta_os_falsos {n : ℕ} (φ : CNF n) (x : Fin n → Bool) (a : ℂ) :
    opDaInstancia (custoCNF φ) (EuclideanSpace.single x a)
      = (((φ.map (fun C => 1 - leiNaClausula C x)).sum : ℤ) : ℂ) • EuclideanSpace.single x a := by
  rw [opDaInstancia_single, ← o_custo_e_o_numero_de_falsos, Int.cast_natCast]

/-- Em cada configuração, a trava do leitor multiplica por `e^{−s}` elevado ao número de FALSOS. -/
theorem o_leitor_decai_por_falso {n : ℕ} (φ : CNF n) (s : ℝ) (v : EuclideanSpace ℂ (Fin n → Bool))
    (x : Fin n → Bool) :
    WithLp.ofLp (trava (custoCNF φ) s v) x
      = ((Real.exp (-(s * (((φ.map (fun C => 1 - leiNaClausula C x)).sum : ℤ) : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x := by
  rw [trava_ofLp, ← o_custo_e_o_numero_de_falsos, Int.cast_natCast]

end TGLExt.OLeitorEALei

#print axioms TGLExt.OLeitorEALei.a_lei_na_clausula
#print axioms TGLExt.OLeitorEALei.o_custo_e_o_numero_de_falsos
#print axioms TGLExt.OLeitorEALei.o_nome_e_onde_a_lei_da_verdadeiro
#print axioms TGLExt.OLeitorEALei.sat_e_existir_onde_a_lei_da_verdadeiro
#print axioms TGLExt.OLeitorEALei.o_operador_do_custo_conta_os_falsos
#print axioms TGLExt.OLeitorEALei.o_leitor_decai_por_falso

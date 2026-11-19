import TGLExt.Ergodicity
import TGLExt.TraducaoTuring

set_option autoImplicit false

/-!
# O hamiltoniano oculto e o custo: a ligação com Tomita na face finita

## O hamiltoniano oculto e Tomita

A ligação a fazer é a do hamiltoniano oculto com Tomita, na face finita.

O hamiltoniano oculto aparece no kernel selado em dois lugares: em `QGReaderUVLock` é `K = −log Δ` da luz (o de
Tomita); no dicionário de `TraducaoTuring` e `AEscala` é a fita, o operador do custo (`opDaInstancia`). A face finita
de Tomita está selada. O kernel já tem quatro peças: o logaritmo do estado de Gibbs (`gibbs_reference_log`, em
`ModularRemainderDensity`) e a ligação do custo com a derivada da trava (`o_hamiltoniano_gera_a_trava`, em
`TraducaoTuring`); os pontos fixos do fluxo para pesos positivos quaisquer, repetidos ou não (`sigma_fixed_iff_specExpect`,
em `EquivariantSection`); o limite por blocos da média do relógio (`birkhoff_tendsto_specExpect`, em
`ErgodicMeanSection`, para amostragem discreta com passo não ressonante, e a média contínua nos andares da torre, em
`AperiodicPhaseAverage`); e a esperança condicional da torre (`aperiodicExpectationInput`, em
`AperiodicCentralizerExpectation`). O que este arquivo acrescenta é a especialização, com os nomes da instância, ao
estado da trava.

## O que fica provado

1. (Por definição.) `a_trava_e_o_estado_do_custo`: a trava do leitor é o operador do estado diagonal cujos pesos são
   `e^{−s·custo}`. E `o_operador_do_custo_e_a_matriz_do_custo`: o operador do custo é o da matriz diagonal do custo.
2. ★ `o_hamiltoniano_oculto_da_trava_e_o_custo`: o logaritmo desse estado é menos `s` vezes a matriz do custo
   (especialização de `gibbs_reference_log`: para ρ = e^{−sD}, −log ρ = sD; para o estado de traço um soma-se (log Z)·I, que desaparece na conjugação). A
   igualdade vive no espaço das matrizes de custo. O gerador do fluxo modular age nos observáveis por comutador com
   `s` vezes o custo; não é do mesmo tipo que a matriz do custo.
3. ★ `o_relogio_da_trava_gira_com_a_diferenca_de_custo`: o fluxo modular desse estado gira cada entrada com a
   diferença dos custos das duas atribuições. `o_que_tem_o_mesmo_custo_nao_gira`.
4. ★ `o_que_o_relogio_da_trava_deixa_parado`: para `s ≠ 0`, o que o relógio deixa parado em todo tempo são exatamente
   as matrizes sem entrada entre custos diferentes (os blocos de mesmo custo). É a especialização, com prova própria,
   do teorema selado `sigma_fixed_iff_specExpect`, que já cobre pesos repetidos. Com `s = 0` o fluxo é a identidade.
5. `o_if_e_deixado_parado_pelo_relogio` e `o_nome_fica_parado`: toda pergunta feita às atribuições (uma matriz
   diagonal) fica parada, para todo `s`; em particular o `if` “o custo é zero”, que é o projetor nulo se não há solução.
6. `o_gap_do_relogio_da_trava`: o gap modular entre duas atribuições `i` e `j` é `|s|·|cᵢ − cⱼ|`, para todo
   `s`; para `s ≠ 0`, é zero exatamente quando os custos são iguais.

## Como ler

No dicionário da casa a fita é o hamiltoniano oculto. Aqui: o estado em que o leitor lê é a exponencial do custo, e o
relógio desse estado gira com as diferenças de custo (itens 2 e 3). Para `s ≠ 0`, o que esse relógio deixa parado são os blocos de mesmo custo (item 4), e o bloco de
custo zero é o Nome. As perguntas feitas às atribuições ficam todas paradas (item 5): pelo critério de Takesaki, são
as que têm par; a pedra `AEsperancaEOIf` constrói esse par na face das funções.

As três cláusulas do contrato selado da esperança (`ExpectationInput`, em `TheOathOnTheTower`: cai no centralizador;
fixa o centralizador; é ortogonal ao que sobra) são, na forma, os três teoremas da `AEsperancaEOIf` (lê só o `if`; fixa
o que já é do `if`; é o par). É observação de forma, não termo.

## O que NÃO se afirma

* Nada sobre a torre: lá a esperança condicional já está construída em casa, e o testemunho de quatro campos está
  composto na pedra `OTestemunhoDeTakesakiEmCasa`. Este arquivo é da face finita.
* O limite da média do relógio da trava: o limite por blocos já está selado em geral (`birkhoff_tendsto_specExpect`);
  a especialização ao relógio da trava, dizendo qual média se usa, não foi escrita aqui.
* Que o hamiltoniano oculto da luz (`K = −log Δ` em `QGReaderUVLock`) e o operador do custo sejam o mesmo operador:
  vivem em espaços diferentes, e ligá-los pede uma aplicação que entrelace as duas representações. O que se prova é
  que, para o estado da trava, menos o logaritmo do estado é `s` vezes a matriz do custo (para ρ = e^{−sD}, −log ρ = sD; para o estado de traço um soma-se (log Z)·I, que desaparece na conjugação).
* Nada sobre a máquina de fita do Instituto, nem sobre a natureza. Validade no kernel não é creditação; o gate não se
  move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OHamiltonianoOcultoEOCusto

open TGLExt Matrix TGLExt.TraducaoTuring TGLExt.PIgualNP TGLExt.TheVerbSelectsTheAction
  TGLExt.TheAxiomAndTheFalseWitness

variable {X : Type} [Fintype X] [DecidableEq X]

/-- [DEF] **OS PESOS DA TRAVA**: `e^{−s·custo}` em cada atribuição. -/
noncomputable def pesoDaTrava (c : X → ℕ) (s : ℝ) : X → ℝ := fun x => Real.exp (-(s * (c x : ℝ)))

omit [Fintype X] [DecidableEq X] in
theorem pesoDaTrava_pos (c : X → ℕ) (s : ℝ) (x : X) : 0 < pesoDaTrava c s x := Real.exp_pos _

/-- (Por definição.) **A TRAVA É O ESTADO DO CUSTO**: a trava do leitor é o operador do estado diagonal de pesos
`e^{−s·custo}`. -/
theorem a_trava_e_o_estado_do_custo (c : X → ℕ) (s : ℝ) :
    travaOp c s = Matrix.toEuclideanCLM (𝕜 := ℂ) (rhoD (pesoDaTrava c s)) := rfl

/-- (Por definição.) O operador do custo é o da matriz diagonal do custo. -/
theorem o_operador_do_custo_e_a_matriz_do_custo (c : X → ℕ) :
    opDaInstancia c = Matrix.toEuclideanCLM (𝕜 := ℂ) (Matrix.diagonal (fun x => (c x : ℂ))) := rfl

/-- ★ **O HAMILTONIANO OCULTO DA TRAVA É O CUSTO.** O logaritmo do estado da trava é menos `s` vezes a matriz do
custo (para ρ = e^{−sD}, −log ρ = sD; para o estado de traço um soma-se (log Z)·I, que desaparece na conjugação). -/
theorem o_hamiltoniano_oculto_da_trava_e_o_custo (c : X → ℕ) (s : ℝ) :
    logRho (rhoD (pesoDaTrava c s)) = (-(s : ℂ)) • Matrix.diagonal (fun x => (c x : ℂ)) := by
  rw [logRho_diagonal _ (pesoDaTrava_pos c s)]
  ext i j
  by_cases h : i = j
  · subst h
    simp [pesoDaTrava, Real.log_exp]
  · simp [h]

/-- ★ **O RELÓGIO DA TRAVA GIRA COM A DIFERENÇA DE CUSTO.** -/
theorem o_relogio_da_trava_gira_com_a_diferenca_de_custo (c : X → ℕ) (s t : ℝ) (x : Matrix X X ℂ) (i j : X) :
    sigma (rhoD (pesoDaTrava c s)) t x i j
      = Complex.exp ((t : ℂ) * Complex.I
          * (((-(s * (c i : ℝ)) : ℝ) : ℂ) - ((-(s * (c j : ℝ)) : ℝ) : ℂ))) * x i j := by
  rw [sigma_diagonal_apply _ (pesoDaTrava_pos c s)]
  simp only [pesoDaTrava, Real.log_exp]

/-- O que liga duas atribuições de mesmo custo não gira. -/
theorem o_que_tem_o_mesmo_custo_nao_gira (c : X → ℕ) (s t : ℝ) (x : Matrix X X ℂ) (i j : X) (h : c i = c j) :
    sigma (rhoD (pesoDaTrava c s)) t x i j = x i j := by
  rw [o_relogio_da_trava_gira_com_a_diferenca_de_custo, h]
  simp

/-- ★ **O QUE O RELÓGIO DA TRAVA DEIXA PARADO**: para `s ≠ 0`, exatamente as matrizes sem entrada entre custos
diferentes. -/
theorem o_que_o_relogio_da_trava_deixa_parado (c : X → ℕ) (s : ℝ) (hs : s ≠ 0) (x : Matrix X X ℂ) :
    (∀ t, sigma (rhoD (pesoDaTrava c s)) t x = x) ↔ ∀ i j, c i ≠ c j → x i j = 0 := by
  constructor
  · intro h i j hij
    have hθ : (-(s * (c i : ℝ))) - (-(s * (c j : ℝ))) ≠ 0 := by
      intro h0
      have h2 : s * ((c j : ℝ) - (c i : ℝ)) = 0 := by linarith
      rcases mul_eq_zero.mp h2 with h1 | h1
      · exact hs h1
      · exact hij (by exact_mod_cast (sub_eq_zero.mp h1).symm)
    have h1 : sigma (rhoD (pesoDaTrava c s))
        (Real.pi / ((-(s * (c i : ℝ))) - (-(s * (c j : ℝ))))) x i j = x i j := by
      rw [h]
    rw [o_relogio_da_trava_gira_com_a_diferenca_de_custo] at h1
    have harg : ((Real.pi / ((-(s * (c i : ℝ))) - (-(s * (c j : ℝ)))) : ℝ) : ℂ) * Complex.I
        * (((-(s * (c i : ℝ)) : ℝ) : ℂ) - ((-(s * (c j : ℝ)) : ℝ) : ℂ)) = (Real.pi : ℂ) * Complex.I := by
      have hθc : (((-(s * (c i : ℝ)) : ℝ) : ℂ) - ((-(s * (c j : ℝ)) : ℝ) : ℂ)) ≠ 0 := by
        rw [← Complex.ofReal_sub]
        exact Complex.ofReal_ne_zero.mpr hθ
      rw [Complex.ofReal_div, Complex.ofReal_sub]
      field_simp
    rw [harg, Complex.exp_pi_mul_I] at h1
    have h3 : (2 : ℂ) * x i j = 0 := by linear_combination -h1
    simpa using h3
  · intro h t
    ext i j
    by_cases hij : c i = c j
    · exact o_que_tem_o_mesmo_custo_nao_gira c s t x i j hij
    · rw [o_relogio_da_trava_gira_com_a_diferenca_de_custo, h i j hij]
      simp

/-- **TODA PERGUNTA FEITA ÀS ATRIBUIÇÕES FICA PARADA**: o relógio da trava não move matriz diagonal. -/
theorem o_if_e_deixado_parado_pelo_relogio (c : X → ℕ) (s t : ℝ) (f : X → ℂ) :
    sigma (rhoD (pesoDaTrava c s)) t (Matrix.diagonal f) = Matrix.diagonal f := by
  ext i j
  by_cases hij : i = j
  · subst hij
    exact o_que_tem_o_mesmo_custo_nao_gira c s t _ i i rfl
  · rw [o_relogio_da_trava_gira_com_a_diferenca_de_custo]
    simp [hij]

/-- **O NOME FICA PARADO**: o `if` “o custo é zero” não é movido pelo relógio da trava. -/
theorem o_nome_fica_parado (c : X → ℕ) (s t : ℝ) :
    sigma (rhoD (pesoDaTrava c s)) t (Matrix.diagonal (fun x => if c x = 0 then (1 : ℂ) else 0))
      = Matrix.diagonal (fun x => if c x = 0 then (1 : ℂ) else 0) :=
  o_if_e_deixado_parado_pelo_relogio c s t _

omit [Fintype X] [DecidableEq X] in
/-- O gap modular da trava entre duas atribuições é `|s|·|cᵢ − cⱼ|`; para `s ≠ 0`, é zero exatamente quando os custos são iguais. -/
theorem o_gap_do_relogio_da_trava (c : X → ℕ) (s : ℝ) (i j : X) :
    modularGap (pesoDaTrava c s) i j = |s| * |(c i : ℝ) - (c j : ℝ)| := by
  unfold modularGap pesoDaTrava
  rw [Real.log_exp, Real.log_exp, ← abs_mul]
  have h : -(s * (c i : ℝ)) - -(s * (c j : ℝ)) = -(s * ((c i : ℝ) - (c j : ℝ))) := by ring
  rw [h, abs_neg]

end TGLExt.OHamiltonianoOcultoEOCusto

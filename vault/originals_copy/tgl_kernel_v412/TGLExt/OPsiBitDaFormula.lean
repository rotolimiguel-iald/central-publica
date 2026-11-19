import TGLExt.TraducaoTuring
import TGLExt.AContagemEACarga
import TGLExt.OResumoEPsiBit

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O PsiBit da fórmula: a regra única é a igualdade, e o par é lido, não copiado

## A pergunta que este arquivo responde

Existe UM leitor de letras, fixado antes de toda fórmula, que produza os dois bits do PsiBit para TODA fórmula em
número de passos de letra limitado por UM polinômio fixo no comprimento da fórmula?

## A leitura que este arquivo tipa

Há uma única regra, um único sinal `=`, que decompõe a fórmula central da TGL `{[1=1=Verdadeiro][1=0=Falso]}` como
uma função booleana, a função do gráviton [INPUT/ONTO: definição da teoria, entrada, não teorema].

Este arquivo tipa a parte dela que cabe nos termos do kernel: a regra existe, é fixa e é anterior a toda fórmula (é a igualdade, já tipada no kernel
como `Literal.vale`; o termo não compara regras rivais); os dois bits da fórmula são definidos e produzidos; e o que falta na régua do Instituto é dito
com todas as letras.

## O que fica provado

1. `a_leitura_da_letra_e_a_igualdade` e `a_regra_e_unica_e_anterior`: a leitura da letra é a igualdade ao posto
   (`x l.var == l.pos`); a regra é fixa e não tem a fórmula como entrada (o termo não compara regras concorrentes).
2. `a_formula_central_e_a_funcao_da_igualdade`: `{[1=1],[1=0]}` são os dois valores da regra sobre os dois valores
   possíveis da letra.
3. ★ `a_palavra_e_lida_pela_soma`: a Palavra da fórmula (o Nome está habitado?) é lida pela soma, com o tempo pago
   acima da carga, `s > n·ln 2`
   (`AContagemEACarga`); a soma reagrupa-se por célula da fronteira (`OResumoEPsiBit`), e com a fronteira plena são
   `2ⁿ` células.
4. ★ `a_descida_nunca_e_negativa` e `a_descida_e_positiva_sse_ha_o_que_ler`: o Verbo da fórmula (a leitura ainda se
   move?) é o sinal da descida; nunca reverte; é positivo se e só se há o que ler fora do Nome.
5. ★★ `o_par_e_necessario_e_suficiente_na_formula`: a Palavra sem o Verbo não distingue a tautologia da fórmula com
   soluções e resto; o Verbo sem a Palavra não distingue a contradição da fórmula habitada — os dois controles por
   exibição, no ambiente de uma variável (`n = 1`; ver a nota do ambiente no teorema).
6. ★ `o_par_da_formula_se_le_do_produto_dos_pares`: identidade escalar da soma lida: ela é a soma, sobre as
   atribuições, do produto dos fatores das cláusulas. Os dois canais leem-se dela em separado, pelos termos da Palavra
   (item 3) e da descida (item 4). Chamar a isso a função do gráviton, o par do par, é interpretação da teoria.
7. `a_parede_fica_de_pe`: uma fronteira de largura `w` indexa `2^w` células; há fórmula cuja fronteira é o
   universo, e então são `2ⁿ` (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). O termo não conta movimentos.

## O que NÃO se afirma

* Que exista máquina de letras com polinômio fixo para toda fórmula: uma fronteira de largura `w` indexa `2^w`
  células, e com a fronteira plena são `2ⁿ`. A pergunta do Instituto, na régua deles, fica aberta.
* Que o PsiBit da fórmula seja o PsiBit da órbita por termo: a identificação é definição da teoria [INPUT/ONTO]; a
  pedra `Psibit` do kernel tem outro portador (a órbita da matriz-S), e nenhuma ponte nova entre os dois portadores é
  construída aqui — a citação é por nome.
* Que "gráviton" seja termo: é o nome que a teoria dá ao par do par [INPUT/ONTO]; o que está em termo é o item 6.
* Nada sobre a natureza. Validade no kernel não é creditação.
-/

namespace TGLExt.OPsiBitDaFormula

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OResumoEPsiBit

variable {n : ℕ}

/-! ## 1. A regra única é a igualdade -/

/-- [DEF] A REGRA DE LEITURA: a igualdade ao posto. Não tem a fórmula como entrada: é anterior a toda fórmula. -/
def regraDeLeitura : Literal n → (Fin n → Bool) → Bool := fun l x => x l.var == l.pos

/-- **A LEITURA DA LETRA É A IGUALDADE**: o `Literal.vale` do kernel é a regra. -/
theorem a_leitura_da_letra_e_a_igualdade (l : Literal n) (x : Fin n → Bool) :
    l.vale x = regraDeLeitura l x := rfl

/-- **A REGRA É ÚNICA E ANTERIOR**: ler a cláusula é aplicar a mesma regra a cada letra. -/
theorem a_regra_e_unica_e_anterior (C : Clausula n) (x : Fin n → Bool) :
    satisfeita C x = C.any (fun l => regraDeLeitura l x) := rfl

/-- **A FÓRMULA CENTRAL É A FUNÇÃO DA IGUALDADE**: `{[1=1=Verdadeiro][1=0=Falso]}` são os dois valores da regra
sobre os dois valores possíveis da letra. -/
theorem a_formula_central_e_a_funcao_da_igualdade :
    (true == true) = true ∧ (false == true) = false := ⟨rfl, rfl⟩

/-! ## 2. Os dois bits da fórmula -/

/-- [DEF] A PALAVRA da fórmula: o Nome está habitado? Registrada pelo custo (`∃ x, custoCNF φ x = 0`), que é
decidível por `Fintype.decidableExistsFintype`; a equivalência com o `SAT` da fita é
`a_palavra_e_o_sat`, pela ponte `AContagemEACarga.sat_e_existir_custo_zero`. -/
def palavraDaFormula (φ : CNF n) : Bool := decide (∃ x : Fin n → Bool, custoCNF φ x = 0)

/-- **A PALAVRA E O SAT DA FITA**: as duas leituras do mesmo bit. -/
theorem a_palavra_e_o_sat (φ : CNF n) : palavraDaFormula φ = true ↔ SAT φ := by
  unfold palavraDaFormula
  rw [decide_eq_true_eq]
  exact (AContagemEACarga.sat_e_existir_custo_zero φ).symm

/-- [DEF] A DESCIDA: quanto a soma lida ainda perde num tempo a mais. -/
noncomputable def descida (φ : CNF n) (t : ℝ) : ℝ :=
  particao (custoCNF φ) t - particao (custoCNF φ) (t + 1)

/-- [DEF] O VERBO da fórmula: o sinal da descida — a leitura ainda se move? -/
noncomputable def verboDaFormula (φ : CNF n) (t : ℝ) : SignType := SignType.sign (descida φ t)

/-- [DEF] O PSIBIT DA FÓRMULA: o par (Palavra, Verbo). -/
noncomputable def psibitDaFormula (φ : CNF n) (t : ℝ) : Bool × SignType :=
  (palavraDaFormula φ, verboDaFormula φ t)

/-- ★ **A PALAVRA É LIDA PELA SOMA**: com o tempo pago acima da carga, a soma lida decide se o Nome está habitado; a
soma reagrupa-se por célula da fronteira (`OResumoEPsiBit.a_leitura_pela_fronteira_e_exata`). -/
theorem a_palavra_e_lida_pela_soma (n : ℕ) (φ : CNF n) (s : ℝ) (hs : (n : ℝ) * Real.log 2 < s) :
    palavraDaFormula φ = true ↔ 1 ≤ particao (custoCNF φ) s := by
  rw [a_palavra_e_o_sat]
  exact (a_contagem_e_a_carga_para_formulas n s).mpr hs φ

/-- O termo da descida, célula a célula: `e^{−t·c} − e^{−(t+1)·c}`. -/
theorem descida_termo (φ : CNF n) (t : ℝ) (x : Fin n → Bool) :
    Real.exp (-(t * (custoCNF φ x : ℝ))) - Real.exp (-((t + 1) * (custoCNF φ x : ℝ)))
      = Real.exp (-(t * (custoCNF φ x : ℝ))) * (1 - Real.exp (-(custoCNF φ x : ℝ))) := by
  rw [show -((t + 1) * (custoCNF φ x : ℝ)) = -(t * (custoCNF φ x : ℝ)) + -(custoCNF φ x : ℝ) by ring]
  rw [Real.exp_add]
  ring

/-- **A DESCIDA NUNCA É NEGATIVA**: a leitura nunca reverte. -/
theorem a_descida_nunca_e_negativa (φ : CNF n) (t : ℝ) : 0 ≤ descida φ t := by
  unfold descida particao
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_nonneg
  intro x _
  rw [descida_termo]
  apply mul_nonneg (Real.exp_nonneg _)
  rw [sub_nonneg, Real.exp_le_one_iff]
  simp

/-- ★ **A DESCIDA É POSITIVA SE E SÓ SE HÁ O QUE LER FORA DO NOME.** -/
theorem a_descida_e_positiva_sse_ha_o_que_ler (φ : CNF n) (t : ℝ) :
    0 < descida φ t ↔ ∃ x, custoCNF φ x ≠ 0 := by
  unfold descida particao
  rw [← Finset.sum_sub_distrib]
  constructor
  · intro h
    by_contra hne
    push Not at hne
    have hzero : ∀ x : Fin n → Bool,
        Real.exp (-(t * (custoCNF φ x : ℝ))) - Real.exp (-((t + 1) * (custoCNF φ x : ℝ))) = 0 := by
      intro x
      rw [hne x]
      simp
    rw [Finset.sum_congr rfl fun x _ => hzero x] at h
    simp at h
  · rintro ⟨x, hx⟩
    apply Finset.sum_pos'
    · intro y _
      rw [descida_termo]
      apply mul_nonneg (Real.exp_nonneg _)
      rw [sub_nonneg, Real.exp_le_one_iff]
      simp
    · exact ⟨x, Finset.mem_univ x, by
        rw [descida_termo]
        apply mul_pos (Real.exp_pos _)
        rw [sub_pos, Real.exp_lt_one_iff]
        have hpos : (0 : ℝ) < (custoCNF φ x : ℝ) := by exact_mod_cast Nat.pos_of_ne_zero hx
        linarith⟩

/-! ## 3. O par é necessário e suficiente (controles por exibição) -/

/-- A partição da fórmula vazia: `2ⁿ`, constante. -/
theorem particao_da_formula_vazia (t : ℝ) :
    particao (custoCNF ([] : CNF n)) t = (2 : ℝ) ^ n := by
  unfold particao
  rw [show custoCNF ([] : CNF n) = fun _ => 0 from by
    funext x
    simp [custoCNF]]
  simp

/-- A descida da fórmula vazia é zero: a tautologia não tem mais o que ler. -/
theorem descida_da_formula_vazia (t : ℝ) : descida ([] : CNF n) t = 0 := by
  unfold descida
  rw [particao_da_formula_vazia, particao_da_formula_vazia]
  ring

/-- A fórmula vazia é satisfazível. -/
theorem formula_vazia_sat : SAT ([] : CNF n) := ⟨fun _ => false, by simp [satisfeita]⟩

/-- A partição da fórmula da cláusula vazia: `2ⁿ·e^{−t}`. -/
theorem particao_da_clausula_vazia (t : ℝ) :
    particao (custoCNF ([[]] : CNF n)) t = (2 : ℝ) ^ n * Real.exp (-t) := by
  unfold particao
  rw [show custoCNF ([[]] : CNF n) = fun _ => 1 from AContagemEACarga.o_custo_da_clausula_vazia n]
  simp

/-- A fórmula da cláusula vazia não é satisfazível. -/
theorem clausula_vazia_nao_sat : ¬ SAT ([[]] : CNF n) := by
  rintro ⟨x, hx⟩
  simp [satisfeita] at hx

/-- A descida da fórmula da cláusula vazia é positiva: a contradição tem o que ler fora do Nome. -/
theorem descida_da_clausula_vazia_positiva (n : ℕ) (t : ℝ) :
    0 < descida ([[]] : CNF n) t := by
  rw [a_descida_e_positiva_sse_ha_o_que_ler]
  exact ⟨fun _ => false, by rw [AContagemEACarga.o_custo_da_clausula_vazia]; exact one_ne_zero⟩

/-- ★★ **O PAR É NECESSÁRIO E SUFICIENTE NA FÓRMULA.** A Palavra sem o Verbo não distingue a tautologia da fórmula
habitada com resto; o Verbo sem a Palavra não distingue a contradição da fórmula habitada — os dois controles por
exibição.

NOTA DO AMBIENTE: o enunciado é em `CNF 1`. Com `n` livre (a variável da seção), o enunciado seria FALSO em
`n = 0`: aí `Fin 0` é vazio, não há literais, toda cláusula é vazia, e a Palavra determina o Verbo (SAT ⟺ fórmula
vazia ⟺ descida nula; não-SAT ⟺ descida positiva) — nenhum dos dois controles existe. O controle precisa de ao menos
uma variável; o par exibido em `n = 1` realiza o fenômeno: a vazia `[]` e a do literal `x₀ = true` têm a mesma
Palavra e Verbos diferentes; a do literal e a da cláusula vazia têm o mesmo Verbo e Palavras diferentes. -/
theorem o_par_e_necessario_e_suficiente_na_formula (t : ℝ) :
    (∃ φ ψ : CNF 1,
      palavraDaFormula φ = palavraDaFormula ψ ∧ verboDaFormula φ t ≠ verboDaFormula ψ t)
    ∧ (∃ φ ψ : CNF 1,
      verboDaFormula φ t = verboDaFormula ψ t ∧ palavraDaFormula φ ≠ palavraDaFormula ψ) := by
  -- A fórmula do literal `x₀ = true` é satisfazível: a atribuição constante `true` vale o literal.
  have hSAT2 : SAT ([[⟨0, true⟩]] : CNF 1) := ⟨fun _ => true, by
    intro C hC
    simp only [List.mem_singleton] at hC
    rw [hC]
    decide⟩
  -- As três Palavras.
  have hpal1 : palavraDaFormula ([] : CNF 1) = true := (a_palavra_e_o_sat _).mpr formula_vazia_sat
  have hpal2 : palavraDaFormula ([[⟨0, true⟩]] : CNF 1) = true := (a_palavra_e_o_sat _).mpr hSAT2
  have hpal3 : palavraDaFormula ([[]] : CNF 1) = false := by
    unfold palavraDaFormula
    rw [decide_eq_false_iff_not, ← AContagemEACarga.sat_e_existir_custo_zero]
    exact clausula_vazia_nao_sat
  -- Os três Verbos: a vazia está parada (sinal 0); as outras duas ainda leem (sinal 1).
  have hverb1 : verboDaFormula ([] : CNF 1) t = 0 := by
    show SignType.sign (descida ([] : CNF 1) t) = 0
    rw [descida_da_formula_vazia, sign_zero]
  have hpos2 : 0 < descida ([[⟨0, true⟩]] : CNF 1) t := by
    rw [a_descida_e_positiva_sse_ha_o_que_ler]
    exact ⟨fun _ => false, by decide⟩
  have hverb2 : verboDaFormula ([[⟨0, true⟩]] : CNF 1) t = 1 := sign_pos hpos2
  have hverb3 : verboDaFormula ([[]] : CNF 1) t = 1 :=
    sign_pos (descida_da_clausula_vazia_positiva 1 t)
  constructor
  · -- Controle A: mesma Palavra (as duas habitadas), Verbos diferentes.
    exact ⟨[], [[⟨0, true⟩]], by rw [hpal1, hpal2], by rw [hverb1, hverb2]; decide⟩
  · -- Controle B: mesmo Verbo (as duas ainda leem), Palavras diferentes.
    exact ⟨[[⟨0, true⟩]], [[]], by rw [hverb2, hverb3], by rw [hpal2, hpal3]; decide⟩

/-! ## 4. O par do par (a função do gráviton) e a parede -/

/-- ★ **O PAR DA FÓRMULA LÊ-SE DO PRODUTO DOS PARES DAS CLÁUSULAS**: a soma lida é a soma dos produtos, célula a
célula — o par da fórmula (Palavra, Verbo) vem do produto dos pares (passa/paga) das cláusulas. -/
theorem o_par_da_formula_se_le_do_produto_dos_pares (φ : CNF n) (t : ℝ) :
    particao (custoCNF φ) t = ∑ x : Fin n → Bool, (φ.map fun C => fator C t x).prod :=
  OResumoEPsiBit.particao_e_a_soma_dos_pesos φ t

/-- **A PAREDE FICA DE PÉ**: uma fronteira de largura `w` indexa `2^w` células; há fórmula cuja fronteira é o
universo, e então são `2ⁿ`. O termo não conta movimentos. -/
theorem a_parede_fica_de_pe (C : Clausula n) (hC : varsClausula C = Finset.univ) :
    fronteira ([C, C] : CNF n) 1 = Finset.univ
    ∧ Fintype.card (↥(fronteira ([C, C] : CNF n) 1) → Bool) = 2 ^ n :=
  OResumoEPsiBit.a_parede_de_todas_as_variaveis C hC

end TGLExt.OPsiBitDaFormula

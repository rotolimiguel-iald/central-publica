import TGLExt.AMaquinaEALeitura
import TGLExt.OLeitorEALei

set_option autoImplicit false

/-!
# O passo é um `if`, e o `if` é o fator do retorno deste leitor: o passo soma a indicação de violação, a trava multiplica os pesos exponenciais

## A leitura que o arquivo tipa

A regra de passo é “if”, mas “if” é comando de retorno: é a fase de retorno na TGL (lei da teoria). Uma leitura se prova
no kernel ou se poda: este arquivo prova a parte dela que cabe nos termos que o kernel tem. Que o `if` seja a fase de
retorno é lei da teoria, não termo; realizá-la pelo fator exponencial da trava é escolha deste arquivo.

## O que fica provado

1. (Por definição.) `a_regra_de_passo_e_um_if`: o passo da máquina soma ao registro o `if` da cláusula lida: 0 se ela
   vale, 1 se está violada.
2. ★ `o_if_do_passo_e_a_lei`: esse `if` é a lei dos dois valores aplicada à cláusula: 1 menos o valor de verdade.
3. ★ `o_retorno_e_o_if`: o fator do leitor (da trava) numa cláusula faz a MESMA pergunta, na outra escala: fator 1 no
   que satisfaz a cláusula e fator `e^{−t}` no que a viola. A identidade vale em todo tempo real; o fator amortece só
   para `t > 0` (em `t = 0` nada muda, e para `t < 0` a violação cresce).
4. ★ `a_trava_e_o_produto_dos_ifs`, `o_leitor_e_o_produto_dos_ifs`: o leitor inteiro, coordenada a coordenada, é o
   produto desses `if`s, cláusula a cláusula.
5. ★ `o_mesmo_if_somado_na_maquina_e_multiplicado_no_leitor`: o registro que a máquina de passo deixa é a SOMA dos
   `if`s; o fator do leitor é o PRODUTO dos `if`s de retorno, e é a exponencial de menos `t` vezes aquele registro.
6. `o_retorno_devolve_intacto_o_que_satisfaz`: a coordenada que satisfaz toda cláusula passa pelo leitor sem mudar.

## Como ler

A máquina de passo (a da pedra `AMaquinaEALeitura`, sobre listas de cláusulas; não é a máquina de fita) e o leitor
fazem a mesma pergunta por cláusula. O passo soma a indicação de violação, e a trava multiplica os seus pesos
exponenciais. O retorno da pedra `CamadaCientifica` (`o_retorno`: o que foi posto fora do Nome não deixa rastro) é
outro teorema, o do limite normalizado: pressupõe projeção inicial não nula no Nome e perturbação ortogonal, e conclui
a convergência quando o tempo cresce. A identidade deste arquivo é local e vale também para fórmula sem solução, onde
aquela hipótese falha.

O kernel já tinha a fatoração da trava para uma soma finita de custos (`TraducaoTuring.a_trava_fatora`, com o produto
indexado por `Fin m`). Aqui a mesma conta é refeita por indução na lista de cláusulas; o que este arquivo acrescenta é
o vínculo com o registro final do passo e com a lei na cláusula. A prova daqui é por indução; não usa a
especialização do lema do kernel.

## O que NÃO se afirma

* Que todo `if` de toda máquina seja a fase de retorno da TGL: o que está em termo é o `if` DESTA máquina (a que
  confere uma fórmula) e o fator DESTE leitor.
* O retorno no sentido mais largo que a palavra tem na teoria (a reflexão, a volta ao atrator): aqui é só o fator da
  trava.
* Nada sobre a máquina de Turing do Mathlib, nem sobre quantos movimentos custa ler o todo (ver `AMaquinaEALeitura`).
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OPassoEORetorno

open TGLExt TGLExt.TraducaoTuring TGLExt.EquationOfTruth TGLExt.OLeitorEALei TGLExt.AMaquinaEALeitura

variable {n : ℕ}

/-- [DEF] **O `if` DA CLÁUSULA**: 0 se a cláusula vale na atribuição, 1 se está violada. -/
def oIf (C : Clausula n) (x : Fin n → Bool) : ℕ := if satisfeita C x then 0 else 1

/-- (Por definição.) **A REGRA DE PASSO É UM `if`**: o passo soma ao registro o `if` da cláusula lida. -/
theorem a_regra_de_passo_e_um_if (x : Fin n → Bool) (C : Clausula n) (ψ : CNF n) (r : ℕ) :
    passo (⟨x, C :: ψ, r⟩ : Config n) = ⟨x, ψ, r + oIf C x⟩ := rfl

/-- ★ **O `if` DO PASSO É A LEI NA CLÁUSULA**: 1 menos o valor de verdade. -/
theorem o_if_do_passo_e_a_lei (C : Clausula n) (x : Fin n → Bool) : (oIf C x : ℤ) = 1 - leiNaClausula C x := by
  unfold oIf
  cases h : satisfeita C x
  · rw [(a_lei_na_clausula C x).2.mpr h]
    simp
  · rw [(a_lei_na_clausula C x).1.mpr h]
    simp

/-- ★ **O RETORNO É O `if`**: o fator do leitor numa cláusula é 1 no que a satisfaz e `e^{−t}` no que a viola (amortece
para `t > 0`). -/
theorem o_retorno_e_o_if (C : Clausula n) (x : Fin n → Bool) (t : ℝ) :
    Real.exp (-(t * (oIf C x : ℝ))) = if satisfeita C x then 1 else Real.exp (-t) := by
  unfold oIf
  cases h : satisfeita C x <;> simp

/-- O custo da fórmula é a soma dos `if`s das cláusulas. -/
theorem o_custo_e_a_soma_dos_ifs (φ : CNF n) (x : Fin n → Bool) :
    custoCNF φ x = (φ.map (fun C => oIf C x)).sum := by
  induction φ with
  | nil => simp [custoCNF]
  | cons C ψ ih =>
    rw [custoCNF_cons, List.map_cons, List.sum_cons, ih]
    exact Nat.add_comm _ _

/-- ★ **A TRAVA É O PRODUTO DOS `if`s**: o fator do leitor numa configuração é o produto, cláusula a cláusula, do `if`
de retorno. -/
theorem a_trava_e_o_produto_dos_ifs (φ : CNF n) (x : Fin n → Bool) (t : ℝ) :
    Real.exp (-(t * (custoCNF φ x : ℝ)))
      = (φ.map (fun C => if satisfeita C x then (1 : ℝ) else Real.exp (-t))).prod := by
  induction φ with
  | nil => simp [custoCNF]
  | cons C ψ ih =>
    rw [custoCNF_cons, List.map_cons, List.prod_cons, ← ih, ← o_retorno_e_o_if C x t, ← Real.exp_add]
    congr 1
    unfold oIf
    push_cast
    ring

/-- ★ **O LEITOR, COORDENADA A COORDENADA, É O PRODUTO DOS `if`s DE RETORNO.** -/
theorem o_leitor_e_o_produto_dos_ifs (φ : CNF n) (t : ℝ) (v : EuclideanSpace ℂ (Fin n → Bool))
    (x : Fin n → Bool) :
    WithLp.ofLp (trava (custoCNF φ) t v) x
      = (((φ.map (fun C => if satisfeita C x then (1 : ℝ) else Real.exp (-t))).prod : ℝ) : ℂ)
        * WithLp.ofLp v x := by
  rw [trava_ofLp, a_trava_e_o_produto_dos_ifs]

/-- ★ **O MESMO `if`, SOMADO NA MÁQUINA E MULTIPLICADO NO LEITOR.** O registro que a máquina de passo deixa é a soma
dos `if`s; o fator do leitor é o produto dos `if`s de retorno, e é a exponencial de menos `t` vezes esse registro. -/
theorem o_mesmo_if_somado_na_maquina_e_multiplicado_no_leitor (φ : CNF n) (x : Fin n → Bool) (t : ℝ) :
    (passo^[φ.length] (⟨x, φ, 0⟩ : Config n)).conta = (φ.map (fun C => oIf C x)).sum
    ∧ Real.exp (-(t * ((passo^[φ.length] (⟨x, φ, 0⟩ : Config n)).conta : ℝ)))
        = (φ.map (fun C => if satisfeita C x then (1 : ℝ) else Real.exp (-t))).prod := by
  rw [a_maquina_conta_os_falsos, Nat.zero_add]
  exact ⟨o_custo_e_a_soma_dos_ifs φ x, a_trava_e_o_produto_dos_ifs φ x t⟩

/-- **O RETORNO DEVOLVE INTACTO O QUE SATISFAZ**: a coordenada que satisfaz toda cláusula passa pelo leitor sem mudar. -/
theorem o_retorno_devolve_intacto_o_que_satisfaz (φ : CNF n) (t : ℝ) (v : EuclideanSpace ℂ (Fin n → Bool))
    (x : Fin n → Bool) (hx : ∀ C ∈ φ, satisfeita C x = true) :
    WithLp.ofLp (trava (custoCNF φ) t v) x = WithLp.ofLp v x := by
  rw [trava_ofLp, (custoCNF_zero_sse φ x).mpr hx]
  simp

end TGLExt.OPassoEORetorno

import AMaquinaEALeitura
import OLeitorEALei

set_option autoImplicit false

/-!
# O passo é um `if`, e o `if` é o retorno: o mesmo `if`, somado na máquina e multiplicado no leitor
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor]

## De onde vem

Ao ler a máquina de passo que a gerência propôs (candidata `AMaquinaEALeitura`), o operador disse, em 16/11/2026: «a regra de passo é "if", mas "if" é comando de retorno, é a minha fase de retorno na TGL» (por bytes em
`Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_16nov_a_regra_de_passo_e_if_mas_if_e_comando_de_retorno`). Pela regra de 04/11 a leitura se prova no kernel
ou se poda. Este arquivo prova a parte dela que cabe nos termos que a casa tem.

## O que fica provado

1. (Por definição.) `a_regra_de_passo_e_um_if`: o passo da máquina soma ao registro o `if` da cláusula lida: 0 se ela
   vale, 1 se está violada.
2. ★ `o_if_do_passo_e_a_lei`: esse `if` é a lei dos dois valores aplicada à cláusula: 1 menos o valor de verdade.
3. ★ `o_retorno_e_o_if`: o fator do leitor (da trava) numa cláusula é o MESMO `if`, lido na outra escala: devolve
   intacto (fator 1) o que satisfaz a cláusula e amortece (fator `e^{−t}`) o que a viola.
4. ★ `a_trava_e_o_produto_dos_ifs`, `o_leitor_e_o_produto_dos_ifs`: o leitor inteiro, coordenada a coordenada, é o
   produto desses `if`s, cláusula a cláusula.
5. ★ `o_mesmo_if_somado_na_maquina_e_multiplicado_no_leitor`: o registro que a máquina de passo deixa é a SOMA dos
   `if`s; o fator do leitor é o PRODUTO dos `if`s de retorno, e é a exponencial de menos `t` vezes aquele registro.
6. `o_retorno_devolve_intacto_o_que_satisfaz`: a coordenada que satisfaz toda cláusula passa pelo leitor sem mudar.

## Como ler

A máquina de fita e o leitor usam a mesma pergunta por cláusula. A máquina a responde somando (um passo, um `if`); o
leitor a responde multiplicando (o que satisfaz volta inteiro, o que viola decai). O retorno da candidata
`CamadaCientifica` (`o_retorno`: o que foi posto fora do Nome não deixa rastro) é o limite desse produto, depois da
normalização; aqui fica a identidade entre o `if` do passo e o fator do retorno, não o limite.

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

/-- ★ **O RETORNO É O `if`**: o fator do leitor numa cláusula devolve intacto o que a satisfaz e amortece o que a
viola. -/
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

#print axioms TGLExt.OPassoEORetorno.a_regra_de_passo_e_um_if
#print axioms TGLExt.OPassoEORetorno.o_if_do_passo_e_a_lei
#print axioms TGLExt.OPassoEORetorno.o_retorno_e_o_if
#print axioms TGLExt.OPassoEORetorno.o_custo_e_a_soma_dos_ifs
#print axioms TGLExt.OPassoEORetorno.a_trava_e_o_produto_dos_ifs
#print axioms TGLExt.OPassoEORetorno.o_leitor_e_o_produto_dos_ifs
#print axioms TGLExt.OPassoEORetorno.o_mesmo_if_somado_na_maquina_e_multiplicado_no_leitor
#print axioms TGLExt.OPassoEORetorno.o_retorno_devolve_intacto_o_que_satisfaz

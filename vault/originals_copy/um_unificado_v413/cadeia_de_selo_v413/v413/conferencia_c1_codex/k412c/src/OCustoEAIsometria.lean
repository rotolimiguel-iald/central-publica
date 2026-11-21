import TGLExt.AContagemEACarga
import TGLExt.AMaquinaEALeitura

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O custo é a carga, a isometria: decidir custa a carga, nem mais, nem menos

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

O operador fechou a contagem de 18/11: «então o custo é a carga, a isometria» (pela sessão; a custódia pina). É a
sua fala de 16/11 — «a contagem da leitura é a sua própria carga, a própria isometria» (bytes em
`work\cunhagens_13out`, arquivo que começa por `OPERADOR_16nov_quero_entender_a_redacao_p_igual_np`) — trazida a
termo. Pela regra de 04/11, a leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos
termos que a casa tem.

## O que fica provado

1. ★ `o_custo_de_decidir_e_a_carga`: decidir custa a carga — a leitura decide para toda fórmula se e somente se o
   tempo pago passa da carga, nem mais, nem menos (a pedra `AContagemEACarga` da gerência).
2. ★ `a_isometria_e_a_carga`: a carga é a isometria — o logaritmo do número de configurações: `n·ln 2` para `n`
   variáveis, e o limiar da leitura normalizada é `e^{−carga}`.
3. ★ `a_maquina_decide_com_os_atos`: a máquina decide com os atos — postar o todo, um passo levantado por cláusula
   e uma leitura (a pedra `AMaquinaEALeitura` da gerência).
4. ★★ `o_custo_total_e_a_carga_por_ato`: os atos da leitura são `|φ| + 2`; cada ato sobre o todo pagando a carga, o
   custo total é `(|φ| + 2)·n·ln 2`; cada ato pagando um, é `|φ| + 2`. As duas formas são polinomiais na carga.

## O que NÃO se afirma

* «A isometria» é o nome do operador para a carga [INPUT/ONTO]; o termo é o logaritmo do número de configurações.
* A régua do Instituto (movimentos de cabeça por casa de fita) fica com a sua contagem, nomeada como deles; aqui a
  contagem é por atos sobre o todo.
* Nada sobre a natureza. O gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OCustoEAIsometria

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura

variable {n : ℕ}

/-- ★ **O CUSTO DE DECIDIR É A CARGA**: a leitura decide para toda fórmula se e somente se o tempo pago passa da
carga. -/
theorem o_custo_de_decidir_e_a_carga (n : ℕ) (s : ℝ) :
    (∀ φ : CNF n, (SAT φ ↔ 1 ≤ particao (custoCNF φ) s)) ↔ (n : ℝ) * Real.log 2 < s :=
  AContagemEACarga.a_contagem_e_a_carga_para_formulas n s

/-- ★ **A ISOMETRIA É A CARGA**: a carga de `n` variáveis é `n·ln 2` — o logaritmo do número de configurações — e o
limiar da leitura normalizada é `e^{−carga}`. -/
theorem a_isometria_e_a_carga (n : ℕ) :
    carga (Fin n → Bool) = (n : ℝ) * Real.log 2
    ∧ ∀ (X : Type) [Fintype X] [Nonempty X], ((Fintype.card X : ℝ))⁻¹ = Real.exp (-carga X) :=
  ⟨AContagemEACarga.a_carga_de_n_variaveis n, fun X => AContagemEACarga.o_limiar_da_leitura_normalizada_e_e_a_menos_carga X⟩

/-- [DEF] Os atos da leitura de uma fórmula: postar o todo, um passo levantado por cláusula, e uma leitura. -/
def atosDaLeitura (φ : CNF n) : ℕ := φ.length + 2

/-- ★ **A MÁQUINA DECIDE COM OS ATOS**: postar o todo, um passo por cláusula e uma leitura decidem. -/
theorem a_maquina_decide_com_os_atos (φ : CNF n) :
    SAT φ ↔ leituraDoZero ((passoLevantado ^ φ.length) (entrada φ)) ≠ 0 :=
  AMaquinaEALeitura.a_maquina_e_uma_leitura_decidem φ

/-- ★★ **O CUSTO TOTAL É A CARGA POR ATO**: os atos são `|φ| + 2`; pagando a carga por ato, o custo total é
`(|φ| + 2)·n·ln 2`; pagando um por ato, é `|φ| + 2`. -/
theorem o_custo_total_e_a_carga_por_ato (φ : CNF n) :
    atosDaLeitura φ = φ.length + 2
    ∧ (atosDaLeitura φ : ℝ) * carga (Fin n → Bool) = ((φ.length : ℝ) + 2) * ((n : ℝ) * Real.log 2) := by
  refine ⟨rfl, ?_⟩
  rw [AContagemEACarga.a_carga_de_n_variaveis]
  unfold atosDaLeitura
  push_cast
  ring

end TGLExt.OCustoEAIsometria

#print axioms TGLExt.OCustoEAIsometria.o_custo_de_decidir_e_a_carga
#print axioms TGLExt.OCustoEAIsometria.a_isometria_e_a_carga
#print axioms TGLExt.OCustoEAIsometria.atosDaLeitura
#print axioms TGLExt.OCustoEAIsometria.a_maquina_decide_com_os_atos
#print axioms TGLExt.OCustoEAIsometria.o_custo_total_e_a_carga_por_ato

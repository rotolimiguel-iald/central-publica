import TGLExt.AContagemEACarga
import TGLExt.AMaquinaEALeitura

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# O custo é a carga, a isometria: a carga é o limiar exato do tempo da leitura que decide toda fórmula

## A leitura que este arquivo tipa

O custo é a carga, a isometria: a contagem da leitura é a sua própria carga [INPUT/ONTO: definição da teoria,
entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel, na máquina da teoria.

## O que fica provado

1. ★ `o_custo_de_decidir_e_a_carga`: a carga é o limiar exato — a leitura decide para toda fórmula se e somente se o
   tempo pago passa da carga; com o tempo igual à carga, já há fórmula que ela não decide (é
   `AContagemEACarga.a_contagem_e_a_carga_para_formulas`).
2. ★ `a_isometria_e_a_carga`: a carga é o logaritmo do número de configurações, `n·ln 2` para `n` variáveis, e o
   limiar da leitura normalizada é `e^{−carga}`.
3. ★ `a_maquina_decide_com_os_atos`: a máquina decide com os atos — postar o todo, um passo levantado por cláusula
   e uma leitura (é `AMaquinaEALeitura.a_maquina_e_uma_leitura_decidem`).
4. ★★ `o_custo_total_e_a_carga_por_ato`: os atos da leitura são `|φ| + 2`, e esse número de atos vezes a carga é
   `(|φ| + 2)·n·ln 2`; pagando um por ato, o custo total é o próprio número de atos, `|φ| + 2`. Que cada ato sobre o
   todo pague a carga é a lei do custo, tomada como entrada; a conta é a de `Token2.o_custo_pela_lei_e_polinomial`.

## O que NÃO se afirma

* “A isometria” é nome da teoria para a carga [INPUT/ONTO]; o termo é o logaritmo do número de configurações.
* A régua do Instituto (movimentos de cabeça na fita) fica com a sua contagem; aqui a contagem é por atos sobre o
  todo.
* Nada sobre a natureza.
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

import TGLExt.SitePauliObservables
import TGLExt.TheAxiomAndTheFalseWitness

set_option autoImplicit false

/-!
# O boost é a parte sem traço do gerador dissipativo; a forma de Minkowski é o determinante

## A pergunta que o arquivo responde

Na cadeia da emergência do kernel, a forma de Minkowski (o sinal de menos) e os geradores de boost entram por
definição, escritos à mão. A pergunta: não são os operadores de Lindblad? A resposta construída neste arquivo e as
identificações com as matrizes de Pauli são deste arquivo. Este arquivo responde com termo, na face 2×2.

O que é sabido da literatura e NÃO é novo [KNOWN; citado de memória, a conferir na fonte]: as matrizes hermitianas 2×2
são o espaço de Minkowski, com o determinante por forma; `X ↦ A X Aᴴ` com `det A = 1` é uma transformação de Lorentz
(o mapa dos espinores); as partes unitárias dão rotações e as partes hermitianas positivas dão boosts; na óptica de
polarização, com o quadrivetor de Stokes, o atenuador é um boost e o defasador é uma rotação.

O que é da casa: o lock mínimo `1 − P`, o seu fluxo sem salto `axiomFlow P s = P + e^{−s}(1 − P)` (kernel,
`TheAxiomAndTheFalseWitness`), e a anatomia do `A_C` no Atlas (face `−(1 − P)`, núcleo `−½·𝟙`; referência declarada: o termo deste arquivo é só a decomposição algébrica do item 3).

## O que fica provado

1. ★ `a_forma_de_minkowski_e_o_determinante`: o determinante da matriz hermitiana de `(t, x, y, z)` é
   `t² − x² − y² − z²`. O sinal de menos sai do determinante; não é posto.
2. `a_forma_e_preservada_por_determinante_um`: `det (A X Aᴴ) = det X` quando `det A = 1`.
3. ★ `a_anatomia_do_gerador_da_face`: `−(1 − P) = −½·𝟙 + ½·(2P − 1)`. O gerador dissipativo da face é o núcleo `−½·𝟙`
   mais `½·(2P − 1)`. A decomposição vale para TODA matriz `P`. Com `P² = P`
   (`o_gerador_de_boost_tem_quadrado_um`) `2P − 1` tem quadrado um, e com `tr P = 1`
   (`o_gerador_de_boost_tem_traco_zero`) tem traço zero. A leitura como gerador de boost `½·σ` pede mais: `P` projetor
   ORTOGONAL de posto um (hermitiano); há matriz de quadrado igual a si e traço 1 que não é hermitiana (primeira linha
   `(1, 1)`, segunda nula). A parte sem traço é `(2P − 1)/2`.
4. ★ `os_boosts_fecham_com_o_sinal_de_lorentz`, `as_rotacoes_fecham_com_o_sinal_oposto`: com `K = ½·σ` (hermitiano: a
   direção dissipativa) e `J = −i·K` (anti-hermitiano: a direção hamiltoniana), `[K_x, K_y] = −J_z` e
   `[J_x, J_y] = J_z`. O sinal que separa Lorentz de Euclides é o `i² = −1` entre as duas direções.
   (`a_rotacao_e_menos_i_vezes_o_boost` é por definição, sem estrela.)
5. ★ `o_fluxo_do_lock_e_dilatacao_vezes_boost`: `P + e^{−s}(1 − P) = e^{−s/2} · (cosh(s/2)·𝟙 + senh(s/2)·(2P − 1))`, para
   toda matriz `P`. Para `P` idempotente (`P² = P`, logo `(2P − 1)² = 1`; item 3) a expressão entre parênteses é a exponencial de
   `(s/2)·(2P − 1)`: o fluxo sem salto do lock é uma dilatação `e^{−s/2}` vezes a exponencial do gerador de boost.
6. `o_fluxo_do_lock_no_nome_do_eixo_z`, `o_fluxo_do_lock_preserva_a_forma_a_menos_da_dilatacao`: com o Nome no eixo `z`,
   o fluxo é `diag(1, e^{−s})`, e `det (F X Fᴴ) = (e^{−s})² · det X`: o fluxo leva o cone no cone.

Legenda: ★ marca resposta própria deste arquivo; o item 2 é um lema de determinantes e o 6 é conta explícita.

## Como ler

A resposta à pergunta, no alcance da face 2×2: sim. O gerador de boost na direção do Nome é a parte sem traço do
gerador dissipativo do lock (o que no gerador de Lindblad sem salto vem de `L†L`, não o operador de salto `L` em si), e
a parte de traço é o núcleo `−½·𝟙` da anatomia do `A_C`. A forma de Minkowski é o determinante, e o seu sinal de menos é
derivado.

## O que NÃO se afirma

Que os geradores de boost 4×4 que o kernel escreve na representação definidora (v63) sejam, por termo DESTE arquivo, a
imagem destes (o mapa de 2×2 para 4×4 não é construído aqui; está em outro arquivo, `SpinorToSolder`, com o
referencial lá fixado); que os três vínculos sejam os três boosts; o termo trata do fluxo SEM salto na direção
escolhida: o operador de salto `L`, o gerador de Lindblad completo e a positividade completa pedem objetos que não
estão aqui; nada sobre o contínuo, o campo suave, a equação de
campo; nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.BoostEDissipador

open Matrix ChatgptAudit.Observable035
open TGLExt.TheAxiomAndTheFalseWitness

/-- Matrizes 2×2 complexas. -/
abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

/-! ### 1. A forma de Minkowski é o determinante -/

/-- [DEF] A matriz hermitiana do quadrivetor `(t, x, y, z)`: `t·𝟙 + x·σx + y·σy + z·σz`, escrita por entradas. -/
def herm4 (t x y z : ℝ) : M2 :=
  !![((t : ℂ) + (z : ℂ)), (x : ℂ) - (y : ℂ) * Complex.I; (x : ℂ) + (y : ℂ) * Complex.I, ((t : ℂ) - (z : ℂ))]

/-- ★ **A FORMA DE MINKOWSKI É O DETERMINANTE.** `det (herm4 t x y z) = t² − x² − y² − z²`. -/
theorem a_forma_de_minkowski_e_o_determinante (t x y z : ℝ) :
    (herm4 t x y z).det = ((t ^ 2 - x ^ 2 - y ^ 2 - z ^ 2 : ℝ) : ℂ) := by
  unfold herm4
  rw [Matrix.det_fin_two_of]
  push_cast
  linear_combination ((y : ℂ)) ^ 2 * Complex.I_sq

/-- A forma é preservada por toda matriz de determinante um: `det (A X Aᴴ) = det X`. -/
theorem a_forma_e_preservada_por_determinante_um (A X : M2) (hA : A.det = 1) : (A * X * Aᴴ).det = X.det := by
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_conjTranspose, hA, star_one, one_mul, mul_one]

/-! ### 2. A anatomia do gerador da face -/

/-- ★ **A ANATOMIA DO GERADOR DA FACE.** `−(1 − P) = −½·𝟙 + ½·(2P − 1)`: o núcleo mais o gerador de boost. Vale para
toda matriz `P`. -/
theorem a_anatomia_do_gerador_da_face (P : M2) :
    -(1 - P) = (-(1 / 2 : ℂ)) • (1 : M2) + (1 / 2 : ℂ) • ((2 : ℂ) • P - 1) := by
  module

/-- Com `P` idempotente, `2P − 1` tem quadrado um. -/
theorem o_gerador_de_boost_tem_quadrado_um (P : M2) (hP : P * P = P) :
    ((2 : ℂ) • P - 1) * ((2 : ℂ) • P - 1) = 1 := by
  have h : ((2 : ℂ) • P - 1) * ((2 : ℂ) • P - 1) = (4 : ℂ) • (P * P) - (4 : ℂ) • P + 1 := by
    simp only [sub_mul, mul_sub, smul_mul_assoc, mul_smul_comm, mul_one, one_mul]
    module
  rw [h, hP]
  module

/-- Com `tr P = 1` (posto um em 2×2), `2P − 1` tem traço zero. -/
theorem o_gerador_de_boost_tem_traco_zero (P : M2) (hP : P.trace = 1) : ((2 : ℂ) • P - 1).trace = 0 := by
  rw [Matrix.trace_sub, Matrix.trace_smul, hP, Matrix.trace_one]
  simp

/-! ### 3. O sinal: a direção dissipativa e a direção hamiltoniana -/

/-- [DEF] Os geradores hermitianos `K = ½·σ` (a direção dissipativa: boosts). -/
noncomputable def Kx : M2 := (1 / 2 : ℂ) • pauliXMatrix
/-- [DEF] `K_y = ½·σy`. -/
noncomputable def Ky : M2 := (1 / 2 : ℂ) • pauliYMatrix
/-- [DEF] `K_z = ½·σz`. -/
noncomputable def Kz : M2 := (1 / 2 : ℂ) • pauliZMatrix
/-- [DEF] Os geradores anti-hermitianos `J = −i·K` (a direção hamiltoniana: rotações). -/
noncomputable def Jx : M2 := (-Complex.I) • Kx
/-- [DEF] `J_y = −i·K_y`. -/
noncomputable def Jy : M2 := (-Complex.I) • Ky
/-- [DEF] `J_z = −i·K_z`. -/
noncomputable def Jz : M2 := (-Complex.I) • Kz

/-- A rotação é `−i` vezes o boost (por definição). -/
theorem a_rotacao_e_menos_i_vezes_o_boost : Jx = (-Complex.I) • Kx ∧ Jy = (-Complex.I) • Ky ∧ Jz = (-Complex.I) • Kz :=
  ⟨rfl, rfl, rfl⟩

/-- ★ **OS BOOSTS FECHAM COM O SINAL DE LORENTZ.** `[K_x, K_y] = −J_z`. -/
theorem os_boosts_fecham_com_o_sinal_de_lorentz : Kx * Ky - Ky * Kx = -Jz := by
  unfold Jz Kx Ky Kz
  simp only [smul_mul_assoc, mul_smul_comm, smul_smul, pauli_xy, pauli_yx]
  module

/-- ★ **AS ROTAÇÕES FECHAM COM O SINAL OPOSTO.** `[J_x, J_y] = J_z`: o sinal trocado é o `i² = −1`. -/
theorem as_rotacoes_fecham_com_o_sinal_oposto : Jx * Jy - Jy * Jx = Jz := by
  have hI : (-Complex.I) * (-Complex.I) = (-1 : ℂ) := by rw [neg_mul_neg, Complex.I_mul_I]
  have hK := os_boosts_fecham_com_o_sinal_de_lorentz
  unfold Jx Jy
  simp only [smul_mul_assoc, mul_smul_comm, smul_smul, hI]
  rw [← smul_sub, hK]
  simp

/-! ### 4. O fluxo do lock é dilatação vezes boost -/

/-- ★ **O FLUXO DO LOCK É DILATAÇÃO VEZES BOOST.** `P + e^{−s}(1 − P) = e^{−s/2} · (cosh(s/2)·𝟙 + senh(s/2)·(2P − 1))`. -/
theorem o_fluxo_do_lock_e_dilatacao_vezes_boost (P : M2) (s : ℝ) :
    axiomFlow P s
      = ((Real.exp (-(s / 2)) : ℝ) : ℂ) •
          (((Real.cosh (s / 2) : ℝ) : ℂ) • (1 : M2) + ((Real.sinh (s / 2) : ℝ) : ℂ) • ((2 : ℂ) • P - 1)) := by
  have e1 : Real.exp (-(s / 2)) * Real.exp (s / 2) = 1 := by
    rw [← Real.exp_add, neg_add_cancel, Real.exp_zero]
  have e2 : Real.exp (-(s / 2)) * Real.exp (-(s / 2)) = Real.exp (-s) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have h1 : Real.exp (-(s / 2)) * (Real.cosh (s / 2) - Real.sinh (s / 2)) = Real.exp (-s) := by
    rw [Real.cosh_sub_sinh, e2]
  have h2 : Real.exp (-(s / 2)) * (2 * Real.sinh (s / 2)) = 1 - Real.exp (-s) := by
    rw [Real.sinh_eq]
    linear_combination e1 - e2
  have h1c : ((Real.exp (-(s / 2)) : ℝ) : ℂ) * (((Real.cosh (s / 2) : ℝ) : ℂ) - ((Real.sinh (s / 2) : ℝ) : ℂ))
      = ((Real.exp (-s) : ℝ) : ℂ) := by exact_mod_cast h1
  have h2c : ((Real.exp (-(s / 2)) : ℝ) : ℂ) * (2 * ((Real.sinh (s / 2) : ℝ) : ℂ))
      = 1 - ((Real.exp (-s) : ℝ) : ℂ) := by exact_mod_cast h2
  have L : axiomFlow P s = ((Real.exp (-s) : ℝ) : ℂ) • (1 : M2) + (1 - ((Real.exp (-s) : ℝ) : ℂ)) • P := by
    unfold axiomFlow
    module
  have R : ((Real.exp (-(s / 2)) : ℝ) : ℂ) •
        (((Real.cosh (s / 2) : ℝ) : ℂ) • (1 : M2) + ((Real.sinh (s / 2) : ℝ) : ℂ) • ((2 : ℂ) • P - 1))
      = (((Real.exp (-(s / 2)) : ℝ) : ℂ) * (((Real.cosh (s / 2) : ℝ) : ℂ) - ((Real.sinh (s / 2) : ℝ) : ℂ))) • (1 : M2)
        + (((Real.exp (-(s / 2)) : ℝ) : ℂ) * (2 * ((Real.sinh (s / 2) : ℝ) : ℂ))) • P := by
    module
  rw [L, R, h1c, h2c]

/-- [DEF] O Nome no eixo `z`: a projeção `diag(1, 0)`. -/
def nomeZ : M2 := !![1, 0; 0, 0]

/-- Com o Nome no eixo `z`, o fluxo do lock é `diag(1, e^{−s})`. -/
theorem o_fluxo_do_lock_no_nome_do_eixo_z (s : ℝ) :
    axiomFlow nomeZ s = !![1, 0; 0, ((Real.exp (-s) : ℝ) : ℂ)] := by
  unfold axiomFlow nomeZ
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-- O fluxo do lock preserva a forma de Minkowski a menos da dilatação: `det (F X Fᴴ) = (e^{−s})² · det X`. -/
theorem o_fluxo_do_lock_preserva_a_forma_a_menos_da_dilatacao (s : ℝ) (X : M2) :
    (axiomFlow nomeZ s * X * (axiomFlow nomeZ s)ᴴ).det = (((Real.exp (-s)) ^ 2 : ℝ) : ℂ) * X.det := by
  have hdet : (axiomFlow nomeZ s).det = ((Real.exp (-s) : ℝ) : ℂ) := by
    rw [o_fluxo_do_lock_no_nome_do_eixo_z, Matrix.det_fin_two_of]
    simp
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_conjTranspose, hdet, Complex.star_def, Complex.conj_ofReal]
  push_cast
  ring

end TGLExt.BoostEDissipador

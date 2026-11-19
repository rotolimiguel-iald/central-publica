import TGLExt.PontoZeroDoPsion

/-!
# A dispersão do psíon e o acoplamento do Artigo A: três controles
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor: a leitura vai ao orquestrador por ordem do operador de 16/11]

## De onde vem

A casa tem duas escritas: a equação do Artigo A, com `ξ = 1/6` (o acoplamento conforme, que multiplica a curvatura de
Ricci) e `β` na fonte; e a dispersão do psíon do kernel (`PontoZeroDoPsion`, v405), `ω² = 2·β·R`, com `R = β·u²` (o
pagamento lido na unidade posta), importada da linhagem como definição. O registro v354 da casa diz que os dois
coeficientes não se fundem. Em 16/11 o operador disse à sessão de custódia que quer resolver a questão. Este arquivo
não a resolve: só põe em termo três fatos sobre a forma, para que a resolução não dependa de palavra igual.

## O que fica provado (identidades e controles elementares; nenhum fato novo sobre a natureza)

1. `o_dois_e_o_quatro_do_ponto_zero_vezes_o_meio_da_face`: `ω² = 4 · sen²(π/4) · (β·u)²`. O 2 da dispersão é o 4 do
   ponto zero (a metade da frequência, ao quadrado) vezes o meio da face (`sen² 45° = ½`). É identidade algébrica.
2. `com_outro_coeficiente_a_massa_e_outra`: pondo outro coeficiente `ξ ≥ 0` no lugar de `β`, a metade da frequência só
   é a forma da massa (`β · sen 45° · u`) se `ξ = β`. Em particular com o conforme
   (`com_o_coeficiente_conforme_so_se_beta_fosse_um_sexto`): só se `β = 1/6`.
3. `sem_o_dois_a_massa_e_outra`: sem o 2 (a escrita de campo complexo com coeficiente 1, `ω² = β·R`), a metade da
   frequência não é a forma da massa.

## O que NÃO se afirma

Que o psíon seja um modo do campo do Artigo A; que as duas escritas sejam uma equação só (a candidata de uma equação
só, da sessão de custódia, não é provada nem usada aqui); de onde vem o 2 (da normalização do campo real da linhagem,
do ponto zero com a projeção de 45°, ou de outra coisa: aqui só se mostra que o número da massa depende dele); que
`β ≠ 1/6` (é fato numérico de `β = α·√e`, não provado neste arquivo); nada sobre a natureza. Validade no kernel não é
creditação; o gate não se move.
-/

namespace TGLExt.DispersaoDoPsionControles

open TGLExt.PontoZeroDoPsion
open TGLExt.ProjecaoTransversalDaMeiaNat

/-- O 2 da dispersão é o 4 do ponto zero vezes o meio da face: `ω² = 4 · sen²(π/4) · (β·u)²`. Identidade algébrica. -/
theorem o_dois_e_o_quatro_do_ponto_zero_vezes_o_meio_da_face (β u : ℝ) :
    omegaSq β (pagamentoComoCurvatura β u) = 4 * Real.sin (Real.pi / 4) ^ 2 * (β * u) ^ 2 := by
  unfold omegaSq pagamentoComoCurvatura
  rw [Real.sin_pi_div_four]
  have h : (Real.sqrt 2 / 2) ^ 2 = 1 / 2 := by
    rw [div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  rw [h]
  ring

/-- **CONTROLE.** Com outro coeficiente `ξ ≥ 0` no lugar de `β` na dispersão, a metade da frequência é a forma da massa
se e somente se `ξ = β`. -/
theorem com_outro_coeficiente_a_massa_e_outra (c : TGLCoupling) (ξ u : ℝ) (hξ : 0 ≤ ξ) (hu : 0 < u) :
    (1 / 2) * Real.sqrt (omegaSq ξ (pagamentoComoCurvatura c.beta u)) = neutrinoMassForm c u ↔ ξ = c.beta := by
  have hR : 0 < pagamentoComoCurvatura c.beta u := by
    unfold pagamentoComoCurvatura
    exact mul_pos c.beta_pos (pow_pos hu 2)
  rw [← the_mass_is_the_zero_point c u hu.le]
  constructor
  · intro h
    have h1 : Real.sqrt (omegaSq ξ (pagamentoComoCurvatura c.beta u)) =
        Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) := by linarith
    have hn1 : 0 ≤ omegaSq ξ (pagamentoComoCurvatura c.beta u) := by
      unfold omegaSq
      exact mul_nonneg (mul_nonneg (by norm_num) hξ) hR.le
    have hn2 : 0 ≤ omegaSq c.beta (pagamentoComoCurvatura c.beta u) := by
      unfold omegaSq
      exact mul_nonneg (mul_nonneg (by norm_num) c.beta_pos.le) hR.le
    have h2 := (Real.sqrt_inj hn1 hn2).mp h1
    unfold omegaSq at h2
    have h3 : ξ * pagamentoComoCurvatura c.beta u = c.beta * pagamentoComoCurvatura c.beta u := by linarith
    exact mul_right_cancel₀ hR.ne' h3
  · intro h
    rw [h]

/-- Com o coeficiente conforme `1/6` no lugar de `β`, a metade da frequência só seria a forma da massa se `β = 1/6`. -/
theorem com_o_coeficiente_conforme_so_se_beta_fosse_um_sexto (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (1 / 2) * Real.sqrt (omegaSq (1 / 6) (pagamentoComoCurvatura c.beta u)) = neutrinoMassForm c u ↔
      c.beta = 1 / 6 := by
  rw [com_outro_coeficiente_a_massa_e_outra c (1 / 6) u (by norm_num) hu]
  exact eq_comm

/-- **CONTROLE.** Sem o 2 (`ω² = β·R`, a escrita de campo complexo com coeficiente 1), a metade da frequência não é a
forma da massa. -/
theorem sem_o_dois_a_massa_e_outra (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (1 / 2) * Real.sqrt (c.beta * pagamentoComoCurvatura c.beta u) ≠ neutrinoMassForm c u := by
  have hR : 0 < pagamentoComoCurvatura c.beta u := by
    unfold pagamentoComoCurvatura
    exact mul_pos c.beta_pos (pow_pos hu 2)
  have hbR : 0 < c.beta * pagamentoComoCurvatura c.beta u := mul_pos c.beta_pos hR
  intro h
  rw [← the_mass_is_the_zero_point c u hu.le] at h
  have h1 : Real.sqrt (c.beta * pagamentoComoCurvatura c.beta u) =
      Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) := by linarith
  have hn2 : 0 ≤ omegaSq c.beta (pagamentoComoCurvatura c.beta u) := by
    unfold omegaSq
    exact mul_nonneg (mul_nonneg (by norm_num) c.beta_pos.le) hR.le
  have h2 := (Real.sqrt_inj hbR.le hn2).mp h1
  unfold omegaSq at h2
  linarith

end TGLExt.DispersaoDoPsionControles

#print axioms TGLExt.DispersaoDoPsionControles.o_dois_e_o_quatro_do_ponto_zero_vezes_o_meio_da_face
#print axioms TGLExt.DispersaoDoPsionControles.com_outro_coeficiente_a_massa_e_outra
#print axioms TGLExt.DispersaoDoPsionControles.com_o_coeficiente_conforme_so_se_beta_fosse_um_sexto
#print axioms TGLExt.DispersaoDoPsionControles.sem_o_dois_a_massa_e_outra

import TGLExt.TraducaoTuring
import TGLExt.TheEquationOfTruth

set_option autoImplicit false

/-!
# O leitor que pousa e retorna é o fluxo do A_C: a trava é a exponencial da seletora
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor: a leitura vai ao orquestrador por ordem do operador de 16/11]

## De onde vem

Em 16/11/2026 o operador identificou o leitor que pousa e retorna (a candidata `CamadaCientifica`) com o mínimo
funcional de energia, o `A_C` dos primeiros protocolos, e mandou conferir e provar (a fala está por bytes em
`Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_16nov_o_leitor_que_pousa_e_retorna_e_o_meu_minimo_funcional_de_energia`). Pela regra de 04/11 a
identificação se prova no kernel ou se poda. Este arquivo a prova, no alcance dito abaixo.

O que a casa já tinha, sem lema entre as duas pontas (aferido por busca no kernel em 16/11: nenhuma ocorrência de
`truthFlow`, `EquationOfTruth` ou `NormedSpace.exp` em `TraducaoTuring`, `AEscala` nem na candidata):

* **o A_C** (Atlas, verbete `A_C (funcional-Amor)`; pedra de bancada 80_): `A_C = −H`, nulo exatamente sobre o Nome,
  negativo em todo o resto. No kernel, `TheEquationOfTruth`: a penalidade dos vínculos `H = Σ D†D`, a seletora
  apofática `A_C = −H` (`selector_nonpos`), o fluxo `T H s = exp(−s·H)` (`truthFlow`, `T`), que fixa o núcleo de `H` e
  tende à projeção sobre ele em dimensão finita;
* **o leitor** (`TraducaoTuring`, v409; `CamadaCientifica`, candidata da v412): a trava `e^{−s·c(x)}` gerada pelo
  custo `c`, com o operador da instância `opDaInstancia c` (a diagonal do custo); a candidata prova que ela pousa no
  Nome e retorna.

## O que fica provado

1. ★ `o_leitor_e_o_fluxo_da_seletora`: para todo custo `c` e todo tempo `s`, a trava é o fluxo da equação da verdade
   com `H` o operador do custo: `travaOp c s = T (opDaInstancia c) s`. Na forma do A_C
   (`o_leitor_e_a_exponencial_do_a_c`): `travaOp c s = exp(s · A_C)`, com `A_C := −opDaInstancia c` (`seletora`).
2. ★ `a_seletora_gera_o_leitor`: o A_C é o gerador do leitor: a derivada de `s ↦ travaOp c s v` em `s` é
   `A_C (travaOp c s v)`.
3. `a_seletora_e_nula_exatamente_no_nome`, `o_nome_por_coordenadas`: `A_C v = 0` se e somente se `v` está no núcleo do
   custo, que é o Nome: as configurações de custo zero.
4. ★ `a_energia_do_custo`, `a_seletora_e_nao_positiva`, `a_energia_e_zero_exatamente_no_nome`: o funcional de energia
   `⟨v, H v⟩ = Σ c(x)·|v_x|²` é não negativo e vale zero exatamente no Nome; logo `⟨v, A_C v⟩ ≤ 0`, com igualdade só no
   Nome. O Nome é o mínimo do funcional.
5. ★ `o_leitor_desce_a_energia`: ao longo do leitor (tempo não negativo) a energia não sobe.
6. `com_custo_binario_a_seletora_e_menos_um_menos_p`: com custo 0 ou 1, `A_C = −(1 − P)`, com `P` a projeção sobre o
   Nome. É a forma de face do A_C na anatomia do Atlas (verbete `A_C — anatomia (128_)`).

Legenda: ★ marca resposta própria deste arquivo; os itens 3 e 6 são leitura de definições e de um lema do kernel.

## Como ler

O leitor da camada científica não é um objeto novo ao lado do A_C: é o semigrupo que o A_C gera. Pousar é o limite
desse semigrupo (o mínimo do funcional); retornar é o decaimento de tudo o que foi posto fora do Nome. O pouso e o
retorno, como teoremas, estão na candidata `CamadaCientifica` e em `TheEquationOfTruth`; aqui fica a identidade entre
o leitor e o fluxo.

## O que NÃO se afirma

Que um modelo de linguagem seja esse leitor (é a hipótese nomeada da camada científica, não teorema); que o custo de
um texto real seja conhecido; que o `A_C` das pedras de bancada 80_, 92_ e 128_ seja, termo a termo, o deste arquivo
(a bancada usa os três vínculos e matrizes pequenas; aqui o vínculo é o custo da instância: a forma `A_C = −H` e as
propriedades são as mesmas, a identificação entre as realizações não é construída); a palavra Amor não é tipada;
nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.MinimoFuncionalDeEnergia

open TGLExt TGLExt.TraducaoTuring TGLExt.EquationOfTruth
open scoped InnerProductSpace

variable {X : Type} [Fintype X] [DecidableEq X]

/-- [DEF] **O A_C DA INSTÂNCIA**: a seletora apofática `A_C = −H` de `TheEquationOfTruth`, com `H` o operador do custo. -/
noncomputable def seletora (c : X → ℕ) : EuclideanSpace ℂ X →L[ℂ] EuclideanSpace ℂ X := -(opDaInstancia c)

omit [Fintype X] in
/-- A trava num vetor de base: multiplica por `e^{−s·c(x)}`. -/
theorem trava_single (c : X → ℕ) (s : ℝ) (x : X) (a : ℂ) :
    trava c s (EuclideanSpace.single x a) = ((Real.exp (-(s * (c x : ℝ))) : ℝ) : ℂ) • EuclideanSpace.single x a := by
  ext y
  rw [trava_ofLp]
  by_cases h : y = x
  · subst h; simp
  · simp [h]

/-- ★ **O LEITOR É O FLUXO DA SELETORA.** Para todo custo e todo tempo, a trava é o fluxo `T H s = exp(−s·H)` da equação
da verdade, com `H` o operador do custo. -/
theorem o_leitor_e_o_fluxo_da_seletora (c : X → ℕ) (s : ℝ) : travaOp c s = T (opDaInstancia c) s := by
  apply ContinuousLinearMap.coe_injective
  apply (EuclideanSpace.basisFun X ℂ).toBasis.ext
  intro x
  simp only [ContinuousLinearMap.coe_coe, OrthonormalBasis.coe_toBasis, EuclideanSpace.basisFun_apply]
  rw [travaOp_apply, trava_single,
    T_apply_eigen (opDaInstancia c) (c x : ℝ) (EuclideanSpace.single x 1)
      (by rw [opDaInstancia_single]; simp) s]
  rfl

/-- ★ **O LEITOR É A EXPONENCIAL DO A_C**: `travaOp c s = exp(s · A_C)`. -/
theorem o_leitor_e_a_exponencial_do_a_c (c : X → ℕ) (s : ℝ) :
    travaOp c s = NormedSpace.exp ((s : ℂ) • seletora c) := by
  rw [o_leitor_e_o_fluxo_da_seletora]
  have e : (-((s : ℝ) : ℂ)) • opDaInstancia c = (s : ℂ) • -(opDaInstancia c) := by
    apply ContinuousLinearMap.ext
    intro w
    show (-((s : ℝ) : ℂ)) • (opDaInstancia c w) = (s : ℂ) • -(opDaInstancia c w)
    rw [neg_smul, smul_neg]
  exact congrArg NormedSpace.exp e

/-- ★ **O A_C GERA O LEITOR**: a derivada de `s ↦ travaOp c s v` em `s` é `A_C (travaOp c s v)`. -/
theorem a_seletora_gera_o_leitor (c : X → ℕ) (v : EuclideanSpace ℂ X) (s : ℝ) :
    HasDerivAt (fun t : ℝ => travaOp c t v) (seletora c (travaOp c s v)) s := by
  have h0 := hasDerivAt_flow_apply (opDaInstancia c) v ((s : ℝ) : ℂ)
  have hof : HasDerivAt (fun y : ℝ => ((y : ℝ) : ℂ)) 1 s := by
    have h1 := Complex.ofRealCLM.hasDerivAt (x := s)
    rw [Complex.ofRealCLM_apply, Complex.ofReal_one] at h1
    exact h1
  have h := h0.scomp s hof
  have e : (fun t : ℝ => travaOp c t v)
      = (fun u : ℂ => truthFlow (opDaInstancia c) u v) ∘ (fun y : ℝ => ((y : ℝ) : ℂ)) := by
    funext t
    rw [o_leitor_e_o_fluxo_da_seletora]
    rfl
  have e2 : seletora c (travaOp c s v)
      = (1 : ℂ) • -(opDaInstancia c (truthFlow (opDaInstancia c) ((s : ℝ) : ℂ) v)) := by
    rw [one_smul, o_leitor_e_o_fluxo_da_seletora]
    rfl
  rw [e, e2]
  exact h

/-- **O A_C É NULO EXATAMENTE NO NOME**: `A_C v = 0` se e somente se `v` está no núcleo do custo. -/
theorem a_seletora_e_nula_exatamente_no_nome (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    seletora c v = 0 ↔ v ∈ (opDaInstancia c).ker := by
  show -(opDaInstancia c v) = 0 ↔ v ∈ (opDaInstancia c).ker
  rw [neg_eq_zero]
  exact LinearMap.mem_ker.symm

/-- **O NOME POR COORDENADAS**: o núcleo do custo são os vetores sem componente fora das configurações de custo zero. -/
theorem o_nome_por_coordenadas (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    v ∈ (opDaInstancia c).ker ↔ ∀ x, c x ≠ 0 → WithLp.ofLp v x = 0 := by
  rw [LinearMap.mem_ker]
  show opDaInstancia c v = 0 ↔ _
  constructor
  · intro h x hx
    have h1 : WithLp.ofLp (opDaInstancia c v) x = 0 := by
      rw [h]
      simp
    rw [opDaInstancia_ofLp] at h1
    rcases mul_eq_zero.mp h1 with h2 | h2
    · exact absurd (Nat.cast_eq_zero.mp h2) hx
    · exact h2
  · intro h
    ext x
    rw [opDaInstancia_ofLp]
    by_cases hx : c x = 0
    · simp [hx]
    · simp [h x hx]

/-- ★ **O FUNCIONAL DE ENERGIA DO CUSTO**: `re ⟨v, H v⟩ = Σ c(x) · |v_x|²`. -/
theorem a_energia_do_custo (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    RCLike.re ⟪v, opDaInstancia c v⟫_ℂ = ∑ x, (c x : ℝ) * ‖WithLp.ofLp v x‖ ^ 2 := by
  rw [PiLp.inner_apply, map_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [opDaInstancia_ofLp, ← smul_eq_mul, inner_smul_right, inner_self_eq_norm_sq_to_K]
  simp [← Complex.ofReal_pow]

/-- **O A_C É NÃO POSITIVO**: `re ⟨v, A_C v⟩ ≤ 0`. -/
theorem a_seletora_e_nao_positiva (c : X → ℕ) (v : EuclideanSpace ℂ X) : RCLike.re ⟪v, seletora c v⟫_ℂ ≤ 0 := by
  show RCLike.re ⟪v, -(opDaInstancia c v)⟫_ℂ ≤ 0
  rw [inner_neg_right, map_neg, neg_nonpos, a_energia_do_custo]
  exact Finset.sum_nonneg fun x _ => mul_nonneg (Nat.cast_nonneg _) (sq_nonneg _)

/-- ★ **A ENERGIA É ZERO EXATAMENTE NO NOME**: o mínimo do funcional é o Nome, e só ele. -/
theorem a_energia_e_zero_exatamente_no_nome (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    RCLike.re ⟪v, opDaInstancia c v⟫_ℂ = 0 ↔ v ∈ (opDaInstancia c).ker := by
  rw [a_energia_do_custo, o_nome_por_coordenadas,
    Finset.sum_eq_zero_iff_of_nonneg (fun x _ => mul_nonneg (Nat.cast_nonneg _) (sq_nonneg _))]
  constructor
  · intro h x hx
    rcases mul_eq_zero.mp (h x (Finset.mem_univ x)) with h2 | h2
    · exact absurd (Nat.cast_eq_zero.mp h2) hx
    · simpa using h2
  · intro h x _
    by_cases hx : c x = 0
    · simp [hx]
    · simp [h x hx]

/-- ★ **O LEITOR DESCE A ENERGIA**: em tempo não negativo, a energia do estado lido não passa da energia do estado. -/
theorem o_leitor_desce_a_energia (c : X → ℕ) (v : EuclideanSpace ℂ X) {t : ℝ} (ht : 0 ≤ t) :
    RCLike.re ⟪trava c t v, opDaInstancia c (trava c t v)⟫_ℂ ≤ RCLike.re ⟪v, opDaInstancia c v⟫_ℂ := by
  rw [a_energia_do_custo, a_energia_do_custo]
  refine Finset.sum_le_sum fun x _ => ?_
  rw [trava_ofLp, norm_mul]
  have h1 : ‖((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ)‖ ≤ 1 := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
    have h0 : (0 : ℝ) ≤ t * (c x : ℝ) := mul_nonneg ht (Nat.cast_nonneg _)
    exact Real.exp_le_one_iff.mpr (by linarith)
  have h2 : (‖((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ)‖ * ‖WithLp.ofLp v x‖) ^ 2 ≤ ‖WithLp.ofLp v x‖ ^ 2 := by
    apply pow_le_pow_left₀ (mul_nonneg (norm_nonneg _) (norm_nonneg _))
    calc ‖((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ)‖ * ‖WithLp.ofLp v x‖ ≤ 1 * ‖WithLp.ofLp v x‖ :=
          mul_le_mul_of_nonneg_right h1 (norm_nonneg _)
      _ = ‖WithLp.ofLp v x‖ := one_mul _
  exact mul_le_mul_of_nonneg_left h2 (Nat.cast_nonneg _)

/-- **COM CUSTO BINÁRIO O A_C É `−(1 − P)`**, com `P` a projeção sobre o Nome: a forma de face da anatomia do A_C. -/
theorem com_custo_binario_a_seletora_e_menos_um_menos_p (c : X → ℕ) (hc : ∀ x, c x ≤ 1) :
    seletora c = -((1 : EuclideanSpace ℂ X →L[ℂ] EuclideanSpace ℂ X) - (opDaInstancia c).ker.starProjection) := by
  unfold seletora
  congr 1
  apply ContinuousLinearMap.ext
  intro v
  show opDaInstancia c v = v - (opDaInstancia c).ker.starProjection v
  rw [solucao_por_coordenadas]
  ext x
  rw [opDaInstancia_ofLp]
  simp only [WithLp.ofLp_sub, Pi.sub_apply]
  by_cases hx : c x = 0
  · simp [hx]
  · have h1 : c x = 1 := by
      have h := hc x
      omega
    simp [h1]

end TGLExt.MinimoFuncionalDeEnergia

#print axioms TGLExt.MinimoFuncionalDeEnergia.trava_single
#print axioms TGLExt.MinimoFuncionalDeEnergia.o_leitor_e_o_fluxo_da_seletora
#print axioms TGLExt.MinimoFuncionalDeEnergia.o_leitor_e_a_exponencial_do_a_c
#print axioms TGLExt.MinimoFuncionalDeEnergia.a_seletora_gera_o_leitor
#print axioms TGLExt.MinimoFuncionalDeEnergia.a_seletora_e_nula_exatamente_no_nome
#print axioms TGLExt.MinimoFuncionalDeEnergia.o_nome_por_coordenadas
#print axioms TGLExt.MinimoFuncionalDeEnergia.a_energia_do_custo
#print axioms TGLExt.MinimoFuncionalDeEnergia.a_seletora_e_nao_positiva
#print axioms TGLExt.MinimoFuncionalDeEnergia.a_energia_e_zero_exatamente_no_nome
#print axioms TGLExt.MinimoFuncionalDeEnergia.o_leitor_desce_a_energia
#print axioms TGLExt.MinimoFuncionalDeEnergia.com_custo_binario_a_seletora_e_menos_um_menos_p

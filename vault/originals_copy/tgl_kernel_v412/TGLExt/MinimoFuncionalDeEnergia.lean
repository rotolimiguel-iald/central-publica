import TGLExt.TraducaoTuring
import TGLExt.TheEquationOfTruth

set_option autoImplicit false

/-!
# O leitor que pousa e retorna é o fluxo do A_C: a trava é a exponencial da seletora

## A identificação que o arquivo prova

O leitor que pousa e retorna é o mínimo funcional de energia, o `A_C` dos primeiros protocolos. Aqui “o leitor que pousa e
retorna” é lido como o leitor da pedra `CamadaCientifica`, por ser ela a que prova o pouso e o retorno. Uma identificação
se prova no kernel ou se poda: este arquivo a prova, no alcance dito abaixo.

O que o kernel já tem (nenhuma ocorrência de `truthFlow`, `EquationOfTruth` ou `NormedSpace.exp` em `TraducaoTuring`,
`AEscala` nem em `CamadaCientifica`):

* **o A_C** (Atlas, verbete `A_C (funcional-Amor)`; pedra de bancada 80_): `A_C = −H`, nulo exatamente sobre o Nome,
  negativo em todo o resto. No kernel, `TheEquationOfTruth`: a penalidade dos vínculos `H = Σ D†D` (`penalty`), a
  seletora apofática `A_C = −H` (`selector_nonpos`), o fluxo `T H s = exp(−s·H)` (`truthFlow`, `T`), que fixa o núcleo
  de `H` e tende à projeção sobre ele em dimensão finita;
* **o leitor** (`TraducaoTuring`; `CamadaCientifica`): a trava `e^{−s·c(x)}` gerada pelo
  custo `c`, com o operador da instância `opDaInstancia c` (a diagonal do custo); a `CamadaCientifica` prova que ela pousa no
  Nome e retorna;
* **no caso de custo 0 ou 1** a ponte entre a trava e uma exponencial já seguia de duas peças existentes
  (`a_trava_binaria_e_o_fluxo_do_axioma`, na `CamadaCientifica`, e `axiomFlow_eq_exp`, em
  `TheAxiomAndTheFalseWitness`). O que é próprio deste arquivo é o caso geral (custo natural qualquer), a forma de
  gerador (a derivada), os fatos de energia e a ponte à penalidade dos vínculos.

## O que fica provado

Quatro objetos distintos, para não confundir: o OPERADOR `A_C = −H`; o FUNCIONAL escalar `E(v) = re ⟨v, H v⟩`; o VALOR
mínimo de `E`, que é 0; e o conjunto dos MINIMIZADORES, que é o núcleo de `H` (o Nome).

1. ★ `o_leitor_e_o_fluxo_da_seletora`: para todo custo `c` e todo tempo `s`, a trava LINEAR (antes de qualquer
   normalização) é o fluxo da equação da verdade com `H` o operador do custo: `travaOp c s = T (opDaInstancia c) s`.
   Na forma do A_C (`o_leitor_e_a_exponencial_do_a_c`): `travaOp c s = exp(s · A_C)`, com `A_C := −opDaInstancia c`
   (`seletora`).
2. ★ `a_seletora_gera_o_leitor`: o A_C é o gerador da trava linear: a derivada de `s ↦ travaOp c s v` em `s` é
   `A_C (travaOp c s v)`.
3. `a_seletora_e_nula_exatamente_no_nome`, `o_nome_por_coordenadas`: `A_C v = 0` se e somente se `v` está no núcleo do
   custo, que é o Nome: os vetores sem componente fora das configurações de custo zero.
4. ★ `a_energia_do_custo`, `a_seletora_e_nao_positiva`, `a_energia_e_zero_exatamente_no_nome`: em TODO o espaço
   vetorial, `E(v) = Σ c(x)·|v_x|²` é não negativo e vale zero exatamente no núcleo de `H`; logo `re ⟨v, A_C v⟩ ≤ 0`,
   com igualdade só ali. `a_energia_zero_fora_do_vetor_nulo_exige_custo_zero`: num vetor não nulo (em particular num
   estado de norma 1), energia zero exige que exista configuração de custo zero. Sem ela, o único minimizador é o vetor
   nulo (no espaço de um ponto, com `c ≡ 1`, a energia vale 1 em todo estado de norma 1).
5. ★ `o_leitor_desce_a_energia`: ao longo da trava linear (tempo não negativo) a energia não sobe. A comparação é
   entre vetores não normalizados.
6. `com_custo_binario_a_seletora_e_menos_um_menos_p`: com custo 0 ou 1, `A_C = −(1 − P)`, com `P` a projeção sobre o
   Nome. É a forma de face do A_C na anatomia do Atlas (verbete `A_C — anatomia (128_)`).
7. ★ `a_penalidade_dos_vinculos_e_o_operador_do_custo`: se o custo é a soma de vínculos de custo 0 ou 1, a penalidade
   dos vínculos do kernel (`penalty`, `Σ D†D`, com `D_j` a diagonal do vínculo `j`) é o operador do custo.
8. ★ `o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas`: para uma fórmula, com um vínculo por OCORRÊNCIA
   de cláusula (o projetor diagonal das atribuições que a violam; cláusula repetida conta de novo, como em
   `custoCNF`), `opDaInstancia (custoCNF φ) = penalty D`. Logo (`a_seletora_da_formula_e_a_seletora_apofatica`) o A_C
   da fórmula é a seletora apofática de `TheEquationOfTruth`, termo a termo, e
   (`o_nome_da_formula_e_a_intersecao_dos_nucleos`, por `ker_penalty`) o Nome da fórmula é a interseção dos núcleos
   dos vínculos: uma violação não compensa outra.

Legenda: ★ marca resposta própria deste arquivo; os itens 3 e 6 são leitura de definições e de um lema do kernel.

## Como ler

O leitor da camada científica não é um objeto novo ao lado do A_C: a trava linear é o semigrupo que o A_C gera. A
órbita que a `CamadaCientifica` faz RETORNAR é essa trava seguida da normalização do estado (`a_trava_pousa_e_volta`).
A normalização muda a equação: para um estado `ψ` de norma 1, a derivada da trajetória normalizada é
`−Hψ + ⟨ψ,Hψ⟩ψ`, e não só `−Hψ` [DERIVED; não é termo deste arquivo]. O que este
arquivo prova como gerador é a equação linear. O pouso e o retorno, como teoremas, estão na pedra
`CamadaCientifica` e em `TheEquationOfTruth`; aqui ficam a identidade entre a trava e o fluxo e a ponte à penalidade.

## O que NÃO se afirma

Que um modelo de linguagem seja esse leitor (é a hipótese nomeada da camada científica, não teorema); que o custo de
um texto real seja conhecido; que o `A_C` das pedras de bancada 80_, 92_ e 128_ seja, termo a termo, o deste arquivo
(elas usam os três vínculos e matrizes pequenas; aqui os vínculos são as cláusulas da fórmula: a forma
`A_C = −Σ D†D` é agora a mesma por teorema, a identificação entre as duas realizações não é construída); que a
trajetória normalizada tenha o A_C por gerador (não tem: ver “Como ler”); que a realização seja mais que a diagonal
desta instância; a palavra Amor não é tipada; nada sobre a natureza. Validade no kernel não é creditação; o gate não
se move.

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

/-- **ENERGIA ZERO NUM VETOR NÃO NULO EXIGE CUSTO ZERO**: fora do vetor nulo (em particular num estado de norma 1), o
funcional só atinge o zero se existe configuração de custo zero. -/
theorem a_energia_zero_fora_do_vetor_nulo_exige_custo_zero (c : X → ℕ) (v : EuclideanSpace ℂ X) (hv : v ≠ 0)
    (h : RCLike.re ⟪v, opDaInstancia c v⟫_ℂ = 0) : ∃ x, c x = 0 := by
  by_contra hne
  have hne' : ∀ x, c x ≠ 0 := fun x hx => hne ⟨x, hx⟩
  apply hv
  have hk := (o_nome_por_coordenadas c v).mp ((a_energia_e_zero_exatamente_no_nome c v).mp h)
  ext x
  simpa using hk x (hne' x)

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

/-! ## A ponte à penalidade dos vínculos do kernel (`TheEquationOfTruth.penalty`) -/

/-- ★ **A PENALIDADE DOS VÍNCULOS É O OPERADOR DO CUSTO.** Se o custo é a soma de vínculos de custo 0 ou 1, a
penalidade `Σ D†D` do kernel, com `D_j` a diagonal do vínculo `j`, é o operador do custo. -/
theorem a_penalidade_dos_vinculos_e_o_operador_do_custo {ι : Type} [Fintype ι] (cj : ι → X → ℕ)
    (h : ∀ j x, cj j x ≤ 1) :
    penalty (fun j => opDaInstancia (cj j)) = opDaInstancia (fun x => ∑ j, cj j x) := by
  apply ContinuousLinearMap.coe_injective
  apply (EuclideanSpace.basisFun X ℂ).toBasis.ext
  intro x
  simp only [ContinuousLinearMap.coe_coe, OrthonormalBasis.coe_toBasis, EuclideanSpace.basisFun_apply]
  rw [opDaInstancia_single]
  simp only [penalty, sum_apply, mul_apply_eq_comp, opDaInstancia_autoadjunto, opDaInstancia_single, map_smul,
    smul_smul]
  rw [← Finset.sum_smul]
  congr 1
  rw [Nat.cast_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  rcases Nat.le_one_iff_eq_zero_or_eq_one.mp (h j x) with h0 | h1
  · simp [h0]
  · simp [h1]

/-- [DEF] **O CUSTO DA OCORRÊNCIA `j` DA FÓRMULA**: 1 nas atribuições que violam a cláusula, 0 nas que a satisfazem.
Cláusula repetida na lista é outra ocorrência e conta de novo, como em `custoCNF`. -/
def custoDaOcorrencia {n : ℕ} (φ : CNF n) (j : Fin φ.length) (x : Fin n → Bool) : ℕ :=
  if satisfeita (φ.get j) x then 0 else 1

/-- O custo da fórmula é a soma dos custos das ocorrências. -/
theorem o_custo_da_formula_e_a_soma_das_ocorrencias {n : ℕ} (φ : CNF n) (x : Fin n → Bool) :
    custoCNF φ x = ∑ j : Fin φ.length, custoDaOcorrencia φ j x := by
  induction φ with
  | nil =>
    show custoCNF ([] : CNF n) x = ∑ j : Fin 0, custoDaOcorrencia ([] : CNF n) j x
    simp [custoCNF]
  | cons C φ ih =>
    have e := Fin.sum_univ_succ (fun j : Fin (φ.length + 1) => custoDaOcorrencia (C :: φ) j x)
    have e0 : custoDaOcorrencia (C :: φ) (0 : Fin (φ.length + 1)) x = (if satisfeita C x then 0 else 1) := rfl
    have es : ∀ j : Fin φ.length, custoDaOcorrencia (C :: φ) j.succ x = custoDaOcorrencia φ j x := fun _ => rfl
    rw [custoCNF_cons, ih]
    show _ = ∑ j : Fin (φ.length + 1), custoDaOcorrencia (C :: φ) j x
    rw [e, e0]
    simp only [es]
    exact add_comm _ _

/-- ★ **O OPERADOR DO CUSTO DA FÓRMULA É A PENALIDADE DOS VÍNCULOS DAS CLÁUSULAS**: `opDaInstancia (custoCNF φ)` é
`Σ D†D`, com um vínculo por ocorrência de cláusula (o projetor diagonal das atribuições que a violam). -/
theorem o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas {n : ℕ} (φ : CNF n) :
    opDaInstancia (custoCNF φ) = penalty (fun j : Fin φ.length => opDaInstancia (custoDaOcorrencia φ j)) := by
  rw [a_penalidade_dos_vinculos_e_o_operador_do_custo (fun j : Fin φ.length => custoDaOcorrencia φ j)
    (fun j x => by unfold custoDaOcorrencia; split <;> simp)]
  congr 1
  funext x
  exact o_custo_da_formula_e_a_soma_das_ocorrencias φ x

/-- **O A_C DA FÓRMULA É A SELETORA APOFÁTICA DO KERNEL**: `A_C = −Σ D†D`, termo a termo. -/
theorem a_seletora_da_formula_e_a_seletora_apofatica {n : ℕ} (φ : CNF n) :
    seletora (custoCNF φ) = -penalty (fun j : Fin φ.length => opDaInstancia (custoDaOcorrencia φ j)) := by
  unfold seletora
  rw [o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas]

/-- **O NOME DA FÓRMULA É A INTERSEÇÃO DOS NÚCLEOS DOS VÍNCULOS** (`ker_penalty` do kernel): uma violação não compensa
outra. -/
theorem o_nome_da_formula_e_a_intersecao_dos_nucleos {n : ℕ} (φ : CNF n) :
    (opDaInstancia (custoCNF φ)).ker = ⨅ j : Fin φ.length, (opDaInstancia (custoDaOcorrencia φ j)).ker := by
  rw [o_operador_do_custo_da_formula_e_a_penalidade_das_clausulas]
  exact ker_penalty _

end TGLExt.MinimoFuncionalDeEnergia

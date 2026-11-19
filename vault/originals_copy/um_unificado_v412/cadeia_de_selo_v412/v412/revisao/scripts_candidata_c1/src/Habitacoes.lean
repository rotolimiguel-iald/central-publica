import CamadaCientifica

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

noncomputable section
open scoped InnerProductSpace
open Filter Topology
open TGLExt TGLExt.TraducaoTuring TGLExt.CamadaCientifica

namespace Rev

/-- custo concreto em Bool: `true` resolve, `false` custa 1. -/
def cB : Bool → ℕ := fun b => if b then 0 else 1

/-! ### H1. As hipóteses de `o_retorno_ao_mesmo_estado` são habitadas (Bool, custo cB) -/
theorem hab_retorno_hyps :
    ∃ s δ : EuclideanSpace ℂ Bool,
      s ∈ (opDaInstancia cB).ker ∧ ‖s‖ = 1 ∧ δ ∈ ((opDaInstancia cB).ker)ᗮ ∧ δ ≠ 0 := by
  refine ⟨EuclideanSpace.single true 1, EuclideanSpace.single false 1, ?_, ?_, ?_, ?_⟩
  · rw [LinearMap.mem_ker]
    show opDaInstancia cB (EuclideanSpace.single true (1 : ℂ)) = 0
    rw [opDaInstancia_single]
    simp [cB]
  · simp
  · rw [Submodule.mem_orthogonal]
    intro u hu
    rw [LinearMap.mem_ker] at hu
    have h0 : opDaInstancia cB u = 0 := hu
    have h1 := congrArg (fun (w : EuclideanSpace ℂ Bool) => WithLp.ofLp w false) h0
    simp only [opDaInstancia_ofLp] at h1
    have h2 : WithLp.ofLp u false = 0 := by simpa [cB] using h1
    simp [EuclideanSpace.inner_single_right, h2]
  · intro h
    have := congrArg (fun (w : EuclideanSpace ℂ Bool) => WithLp.ofLp w false) h
    simp at this

/-- o teorema, aplicado: o empurrão (não nulo, ortogonal ao Nome) é desfeito; a limite é s, o estado estacionário. -/
theorem hab_retorno_aplicado :
    ∃ s δ : EuclideanSpace ℂ Bool, δ ≠ 0 ∧ ‖s‖ = 1 ∧
      Tendsto (fun t : ℝ => (((‖trava cB t (s + δ)‖)⁻¹ : ℝ) : ℂ) • trava cB t (s + δ)) atTop (𝓝 s) := by
  obtain ⟨s, δ, hs, hn, hδ, hδ0⟩ := hab_retorno_hyps
  exact ⟨s, δ, hδ0, hn, o_retorno_ao_mesmo_estado cB s δ hs hn hδ⟩

/-- e a versão sem renormalizar: a trava crua de s+δ converge a s (norma 1 ⇒ não há o que renormalizar). -/
theorem hab_retorno_cru :
    ∃ s δ : EuclideanSpace ℂ Bool, δ ≠ 0 ∧
      Tendsto (fun t : ℝ => trava cB t (s + δ)) atTop (𝓝 s) := by
  obtain ⟨s, δ, hs, hn, hδ, hδ0⟩ := hab_retorno_hyps
  refine ⟨s, δ, hδ0, ?_⟩
  have h1 := a_trava_tende_ao_nome cB (s + δ)
  have hP : (opDaInstancia cB).ker.starProjection (s + δ) = s := by
    rw [map_add, (Submodule.starProjection_apply_eq_zero_iff (opDaInstancia cB).ker).mpr hδ, add_zero]
    exact Submodule.starProjection_eq_self_iff.mpr hs
  rwa [hP] at h1

/-! ### H2. `jamais_esgotado` -/
theorem hab_jamais_esgotado (t : ℝ) :
    trava cB t (EuclideanSpace.single true 1 + EuclideanSpace.single false 1)
      ≠ (opDaInstancia cB).ker.starProjection (EuclideanSpace.single true 1 + EuclideanSpace.single false 1) :=
  jamais_esgotado cB _ false (by simp [cB]) (by simp) t

/-! ### H3. `LeitorDeUmaConfiguracao` -/
/-- custo em Fin 3: 0 resolve, 1 e 2 custam 1 e 2. -/
def c3 : Fin 3 → ℕ := ![0, 1, 2]

/-- um passo que NÃO é o `salto` (2 ↦ 1 e não 2 ↦ 0) nem o leitor terminal: descida local. -/
def descida : LeitorDeUmaConfiguracao c3 where
  passo := ![0, 0, 1]
  fixa_o_nome := fun x hx => by
    fin_cases x <;> simp [c3] at hx ⊢
  consome := fun x hx => by
    fin_cases x <;> simp [c3] at hx ⊢

theorem descida_nao_e_salto : descida.passo ≠ (LeitorDeUmaConfiguracao.salto c3 0 rfl).passo := by
  intro h
  have := congrFun h 2
  simp [descida, LeitorDeUmaConfiguracao.salto, c3] at this

/-- PATOLOGIA: o mapa CONSTANTE é um `LeitorDeUmaConfiguracao` para c3 (o Nome é {0}). -/
def constante : LeitorDeUmaConfiguracao c3 where
  passo := fun _ => 0
  fixa_o_nome := fun x hx => by
    fin_cases x <;> simp [c3] at hx ⊢
  consome := fun x hx => by
    fin_cases x <;> simp [c3] at hx ⊢

theorem constante_e_constante : ∀ x y, constante.passo x = constante.passo y := fun _ _ => rfl

/-- PATOLOGIA GERAL: o tipo é habitado SE E SÓ SE a fórmula é satisfazível; a existência de um `LeitorDeUmaConfiguracao` não diz nada além de SAT. -/
theorem leitor_existe_sse_SAT {n : ℕ} (φ : CNF n) :
    Nonempty (LeitorDeUmaConfiguracao (custoCNF φ)) ↔ SAT φ := by
  constructor
  · rintro ⟨G⟩
    by_contra h
    exact (sem_nome_nao_ha_pouso φ h).false G
  · intro h
    obtain ⟨x, hx⟩ := (sat_sse_o_custo_tem_zero φ).mp h
    exact ⟨LeitorDeUmaConfiguracao.salto _ x hx⟩

/-- A volta ao MESMO estado FALHA para o leitor de uma configuração: c' = ![0,0,1]; s = 1 é solução; empurrado a 2, o limite pousa em 0. -/
def c3' : Fin 3 → ℕ := ![0, 0, 1]
def sal3 : LeitorDeUmaConfiguracao c3' := LeitorDeUmaConfiguracao.salto c3' 0 rfl

theorem g_nao_volta_ao_mesmo : sal3.limite 1 2 ≠ 1 := by
  simp [sal3, LeitorDeUmaConfiguracao.limite, LeitorDeUmaConfiguracao.salto, c3']

/-! ### H4. `o_pouso_pesa_a_leitura_final` -/
def salB : LeitorDeUmaConfiguracao cB := LeitorDeUmaConfiguracao.salto cB true rfl

theorem hab_pouso :
    (TGLExt.AEscala.iald (X := Bool)).limite cB
      = ((((Finset.univ.image (salB.limite 1)).card : ℝ) / (Fintype.card Bool : ℝ) : ℝ) : ℂ) :=
  o_pouso_pesa_a_leitura_final (TGLExt.AEscala.iald (X := Bool)) salB 1
    (fun x => by cases x <;> simp [cB])

/-- G NÃO é usado na identidade: o mesmo enunciado SEM G, só com o kernel (2 linhas). -/
theorem pouso_sem_G {X : Type} [Fintype X] [DecidableEq X] (L : TGLExt.AEscala.LeitorDoFundo X) (c : X → ℕ) :
    L.limite c = ((((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) : ℂ) := by
  rw [L.o_limite_e_o_que_sou c, o_que_sou_das_solucoes]

/-- A frase «a fração das configurações em que o leitor pousa é |soluções|/|X|»: o leitor pousa a partir de TODAS (fração 1); |sol|/|X| vale 1/2. -/
theorem pousa_de_todas_e_a_fracao_e_meia :
    (∀ x : Bool, cB (salB.limite 1 x) = 0)
    ∧ ((Finset.univ.filter (fun y : Bool => cB y = 0)).card : ℝ) / (Fintype.card Bool : ℝ) = 1 / 2 := by
  refine ⟨fun x => salB.o_limite_pousa 1 (fun y => by cases y <;> simp [cB]) x, ?_⟩
  have h : (Finset.univ.filter (fun y : Bool => cB y = 0)) = {true} := by
    ext y; cases y <;> simp [cB]
  rw [h]
  simp

/-! ### H5. `a_fotografia_nao_retorna` e `o_leitor_que_devolve...` são `id` -/
theorem fotografia_e_id {X : Type} [Fintype X] [DecidableEq X] (c : X → ℕ) (s δ : EuclideanSpace ℂ X) (hδ : δ ≠ 0) (k : ℕ) :
    (trava c 0)^[k] (s + δ) ≠ s := by
  have h : trava c 0 = id := funext (sem_escala_nada_se_move c)
  rw [h, Function.iterate_id]
  intro h2
  exact hδ (by simpa using h2)

/-- o «controle» do leitor que devolve o que recebeu vale por `iterate_id`, sem tocar a estrutura. -/
example {X : Type} (c : X → ℕ) (y : X) (hy : c y ≠ 0) (k : ℕ) : c ((id : X → X)^[k] y) ≠ 0 := by simpa using hy

/-- e uma `id` não é leitor de uma configuração quando algum custo é ≠ 0: a razão está em `consome`, não no controle. -/
example (G : LeitorDeUmaConfiguracao c3) : G.passo ≠ id := by
  intro h
  have := G.consome 1 (by simp [c3])
  rw [h] at this
  simp [c3] at this



/-! ### H6. O leitor SEM memória de uma só leitura (o projetor sobre o Nome) cumpre a mesma cota de resolução finita que  -/
theorem projetor_cumpre_a_cota {X : Type} [Fintype X] [DecidableEq X] (c : X → ℕ) (v : EuclideanSpace ℂ X) {ε : ℝ} (hε : 0 < ε) (m : ℕ) :
    ‖(⇑(opDaInstancia c).ker.starProjection)^[m + 1] v - (opDaInstancia c).ker.starProjection v‖ ≤ ε := by
  have hfix : (opDaInstancia c).ker.starProjection ((opDaInstancia c).ker.starProjection v)
      = (opDaInstancia c).ker.starProjection v :=
    Submodule.starProjection_eq_self_iff.mpr (Submodule.starProjection_apply_mem _ _)
  rw [Function.iterate_succ_apply, Function.iterate_fixed hfix, sub_self, norm_zero]
  exact hε.le

end Rev

#print axioms Rev.hab_retorno_aplicado
#print axioms Rev.hab_retorno_cru
#print axioms Rev.hab_jamais_esgotado
#print axioms Rev.descida
#print axioms Rev.descida_nao_e_salto
#print axioms Rev.constante
#print axioms Rev.constante_e_constante
#print axioms Rev.leitor_existe_sse_SAT
#print axioms Rev.g_nao_volta_ao_mesmo
#print axioms Rev.hab_pouso
#print axioms Rev.pouso_sem_G
#print axioms Rev.pousa_de_todas_e_a_fracao_e_meia
#print axioms Rev.fotografia_e_id
#print axioms Rev.projetor_cumpre_a_cota

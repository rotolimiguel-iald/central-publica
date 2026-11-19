import TGLExt.PontoZeroDoPsion

set_option autoImplicit false

/-!
# O vetor que o kernel chama de psíon e o modo do Tratado: separados no Hamiltoniano escondido, ligáveis por um oscilador
[candidata da gerência c1, 16/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor: a leitura vai ao orquestrador por ordem do operador de 16/11]

## De onde vem

O kernel escreve a palavra psíon em mais de um objeto. Dois deles se encontram na pedra `PontoZeroDoPsion`:

* o VETOR: `ThePsionAndTheViscosity.psion C := C.Ω`, o vácuo do certificado de Fock, de norma 1, que o Hamiltoniano
  escondido `HminMic C` leva a zero (`psion_is_the_zero_of_the_hidden_hamiltonian`). `HminMic C` é o lock mínimo
  `lockDe C.Ω = 1 − P` (`HminMic_e_o_lock`, por `rfl`);
* o MODO: a dispersão do Tratado, `omegaSq β R = 2·β·R`, com `R = β·u²`, de onde sai a frequência `ω = √2·β·u`
  (`psion_quantum`) e a forma da massa como a metade dela (`the_mass_is_the_zero_point`). O modo não é vetor nenhum no
  kernel: é uma conta em números reais.

A consolidação da sessão de custódia de 16/11 deixou para a gerência o item de ligar ou separar por termo esses dois
objetos. Este arquivo responde com teoremas até onde a matemática alcança, e deixa a escolha para o operador.

## O que fica provado

**1. Os níveis do lock.** `os_autovalores_do_lock_sao_zero_e_um`: todo autovetor do lock tem autovalor 0 ou 1. Na
unidade posta (`e_nivel_do_lock_sse`): `E` é nível de `u·(1 − P)` se e somente se `E = 0` ou `E = u`. O kernel já tinha
os dois valores (`o_lock_tem_gap_um`); aqui fica provado que não há terceiro.

**2. Os números do modo não são níveis do lock.** A frequência do Tratado é nível do lock, e também diferença de dois
níveis, se e somente se `√2·β = 1` (`a_frequencia_do_tratado_e_nivel_do_lock_sse`,
`a_frequencia_do_tratado_e_diferenca_de_niveis_sse`). A forma da massa e o retido nunca são níveis
(`a_forma_da_massa_nao_e_nivel_do_lock`, `o_retido_nao_e_nivel_do_lock`), porque `β < 1`.

**3. O estado do ângulo de Miguel não é estacionário para o lock.** O estado a um ângulo `θ` do vetor é autovetor do
lock se e somente se `sen θ · cos θ = 0` (`o_estado_do_angulo_e_autovetor_sse`); no ângulo de Miguel não é
(`no_angulo_de_miguel_o_estado_nao_e_autovetor_do_lock`). Em número: a variância do lock nesse estado é `β·(1 − β)`,
diferente de zero (`no_angulo_de_miguel_a_variancia_do_lock`, `no_angulo_de_miguel_a_variancia_nao_e_zero`). O retido é
valor esperado com espalhamento, não nível.

**4. A ligação que o kernel já tem é só pelo valor esperado.**
`a_frequencia_do_tratado_e_raiz_de_dois_vezes_o_valor_esperado_do_lock`: `ω = √2 · u · ⟨1 − P⟩` no ângulo de Miguel. É
fiação de dois teoremas do kernel; nenhum fato novo.

**5. O que uma ligação pediria (CONSTRUÇÃO da gerência, não derivação).** `osciladorDeDoisNiveis ω Ω := ½ω·1 + ω·(1 − P)`
é o oscilador de frequência `ω` [KNOWN: níveis `ω·(n + ½)`] cortado nos dois primeiros níveis. Nele o vetor fica no ponto
zero `½ω` e todo vetor ortogonal fica um quantum acima (`no_oscilador_o_vetor_fica_no_ponto_zero`,
`no_oscilador_o_ortogonal_fica_um_quantum_acima`). Com a frequência do Tratado, esse operador é o lock da unidade posta
deslocado pela forma da massa e reescalado por `√2·β` (`o_oscilador_do_modo_e_o_lock_deslocado_e_reescalado`), e não é o
lock (`o_oscilador_do_modo_nao_e_o_lock_na_unidade`).

**6. No vetor que o kernel chama de psíon** (condicional ao certificado de Fock, que o kernel não habita). O
Hamiltoniano escondido, na unidade posta, não lê nele a frequência do Tratado nem a forma da massa: lê zero
(`no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_frequencia_do_tratado`,
`no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_forma_da_massa`). No oscilador do modo, esse mesmo vetor fica no
nível da forma da massa (`no_oscilador_do_modo_o_psion_do_kernel_fica_na_forma_da_massa`).

## Como ler

Separados: no Hamiltoniano que o kernel tem, o vetor está no nível zero e nenhum vetor carrega a frequência do modo, a
forma da massa ou o retido como nível. Ligáveis: existe um operador da mesma forma do lock em que o vetor é o estado de
baixo, o ponto zero é a forma da massa e o degrau é a frequência do modo; mas ele entra POSTO por quem o escreve (dois
números, `½ω` e `ω`), não sai de teorema nenhum do kernel. Se o kernel separa os dois objetos ou adota o oscilador como
leitura é escolha do operador.

## O que NÃO se afirma

Que o vetor e o modo sejam o mesmo objeto, nem que sejam objetos diferentes na teoria (só no kernel de hoje); qual
objeto leva o nome psíon; que o oscilador de dois níveis seja o Hamiltoniano do campo do Tratado ou do Artigo A; que o
ponto zero seja derivado (a forma da massa continua sendo a conta de `the_mass_is_the_zero_point`, sob as leituras que
essa pedra declara); nada sobre o Hamiltoniano modular (o lock e ele são objetos distintos, que coincidem em ter o
vetor como modo zero); nada sobre a candidata de uma equação só; que `√2·β ≠ 1` (é fato numérico de `β = α·√e`, não
provado aqui); nada sobre a natureza. Nenhuma fala do operador é lida aqui. Validade no kernel não é creditação; o gate
não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.PsionVacuoEModoDoTratado

open TGLExt.PontoZeroDoPsion
open TGLExt.ProjecaoTransversalDaMeiaNat
open TGLExt.ThePsionAndTheViscosity
open scoped InnerProductSpace

/-- A forma da massa é positiva na unidade posta positiva. -/
theorem a_forma_da_massa_e_positiva (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : 0 < neutrinoMassForm c u := by
  rw [a_massa_e_a_projecao_do_retido, Real.sin_pi_div_four]
  exact mul_pos (retido_pos c u hu) (div_pos (Real.sqrt_pos.mpr (by norm_num)) (by norm_num))

/-- A forma da massa é menor que a unidade posta: `β · sen 45° · u < u`, porque `β < 1` e `sen 45° < 1`. -/
theorem a_forma_da_massa_e_menor_que_a_unidade (c : TGLCoupling) (u : ℝ) (hu : 0 < u) : neutrinoMassForm c u < u := by
  rw [a_massa_e_a_projecao_do_retido, retido_eq, Real.sin_pi_div_four]
  have hb := c.beta_pos
  have hb1 := c.beta_lt_one
  have hs0 : (0 : ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hs2 : Real.sqrt 2 < 2 := by
    nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num), Real.sqrt_nonneg 2]
  have h1 : c.beta * u < 1 * u := mul_lt_mul_of_pos_right hb1 hu
  have h2 : c.beta * u * (Real.sqrt 2 / 2) < c.beta * u * 1 :=
    mul_lt_mul_of_pos_left (by linarith) (mul_pos hb hu)
  linarith

section OsNiveisDoLock

variable {F : Type} [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-! ### 1. Os níveis do lock -/

omit [CompleteSpace F] in
/-- O lock aplicado duas vezes é o lock: `(1 − P)² = 1 − P`. -/
theorem o_lock_e_idempotente (Ω v : F) : lockDe Ω (lockDe Ω v) = lockDe Ω v := by
  have hmem : (ℂ ∙ Ω).starProjection v ∈ (ℂ ∙ Ω) := Submodule.starProjection_apply_mem _ _
  have hP : (ℂ ∙ Ω).starProjection ((ℂ ∙ Ω).starProjection v) = (ℂ ∙ Ω).starProjection v :=
    Submodule.starProjection_eq_self_iff.mpr hmem
  simp [lockDe, hP]

omit [CompleteSpace F] in
/-- ★ **OS AUTOVALORES DO LOCK SÃO 0 E 1.** Todo autovetor do lock tem autovalor 0 ou 1: não há terceiro nível. -/
theorem os_autovalores_do_lock_sao_zero_e_um (Ω v : F) (hv : v ≠ 0) (l : ℂ) (h : lockDe Ω v = l • v) :
    l = 0 ∨ l = 1 := by
  have h2 : lockDe Ω (lockDe Ω v) = lockDe Ω v := o_lock_e_idempotente Ω v
  rw [h, map_smul, h, smul_smul] at h2
  have h3 : (l * l - l) • v = 0 := by rw [sub_smul, h2, sub_self]
  rcases smul_eq_zero.mp h3 with h4 | h4
  · have h5 : l * (l - 1) = 0 := by
      rw [← h4]
      ring
    rcases mul_eq_zero.mp h5 with h6 | h6
    · exact Or.inl h6
    · exact Or.inr (sub_eq_zero.mp h6)
  · exact absurd h4 hv

omit [CompleteSpace F] in
/-- Na unidade posta, todo nível de `u·(1 − P)` é 0 ou `u`. -/
theorem os_niveis_do_lock_na_unidade (Ω v : F) (hv : v ≠ 0) (u : ℝ) (E : ℂ) (h : (u : ℂ) • lockDe Ω v = E • v) :
    E = 0 ∨ E = (u : ℂ) := by
  by_cases hu : (u : ℂ) = 0
  · left
    rw [hu, zero_smul] at h
    rcases smul_eq_zero.mp h.symm with h1 | h1
    · exact h1
    · exact absurd h1 hv
  · have h1 : lockDe Ω v = (E / (u : ℂ)) • v := by
      have h2 : ((u : ℂ)⁻¹) • ((u : ℂ) • lockDe Ω v) = ((u : ℂ)⁻¹) • (E • v) := by rw [h]
      rw [smul_smul, inv_mul_cancel₀ hu, one_smul, smul_smul] at h2
      rw [h2, div_eq_inv_mul]
    rcases os_autovalores_do_lock_sao_zero_e_um Ω v hv _ h1 with h3 | h3
    · left
      rcases div_eq_zero_iff.mp h3 with h4 | h4
      · exact h4
      · exact absurd h4 hu
    · right
      exact (div_eq_one_iff_eq hu).mp h3

/-- ★★ **OS NÍVEIS DO LOCK NA UNIDADE POSTA SÃO EXATAMENTE 0 E `u`.** Com o vetor não nulo e algum vetor não nulo
ortogonal a ele, `E` é nível de `u·(1 − P)` se e somente se `E = 0` ou `E = u`. -/
theorem e_nivel_do_lock_sse (Ω χ : F) (hΩ : Ω ≠ 0) (hχ : χ ≠ 0) (hort : ⟪Ω, χ⟫_ℂ = 0) (u : ℝ) (E : ℂ) :
    (∃ v : F, v ≠ 0 ∧ (u : ℂ) • lockDe Ω v = E • v) ↔ E = 0 ∨ E = (u : ℂ) := by
  obtain ⟨h0, h1⟩ := o_gap_com_unidade Ω χ hort u
  constructor
  · rintro ⟨v, hv, h⟩
    exact os_niveis_do_lock_na_unidade Ω v hv u E h
  · rintro (h | h)
    · exact ⟨Ω, hΩ, by rw [h0, h, zero_smul]⟩
    · exact ⟨χ, hχ, by rw [h1, h]⟩

/-! ### 2. Os números do modo não são níveis do lock -/

/-- ★★ **A FREQUÊNCIA DO TRATADO É NÍVEL DO LOCK SE E SOMENTE SE `√2·β = 1`.** -/
theorem a_frequencia_do_tratado_e_nivel_do_lock_sse (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω χ : F) (hΩ : Ω ≠ 0)
    (hχ : χ ≠ 0) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    (∃ v : F, v ≠ 0 ∧
        (u : ℂ) • lockDe Ω v = ((Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) : ℝ) : ℂ) • v)
      ↔ Real.sqrt 2 * c.beta = 1 := by
  refine (e_nivel_do_lock_sse Ω χ hΩ hχ hort u _).trans ?_
  rw [o_psion_e_raiz_de_dois_retidos c u hu.le, retido_eq]
  have hpos : 0 < Real.sqrt 2 * (c.beta * u) :=
    mul_pos (Real.sqrt_pos.mpr (by norm_num)) (mul_pos c.beta_pos hu)
  constructor
  · rintro (h | h)
    · exfalso
      have h1 : Real.sqrt 2 * (c.beta * u) = 0 := by exact_mod_cast h
      linarith
    · have h1 : Real.sqrt 2 * (c.beta * u) = u := by exact_mod_cast h
      have h2 : Real.sqrt 2 * c.beta * u = 1 * u := by rw [one_mul, mul_assoc, h1]
      exact mul_right_cancel₀ hu.ne' h2
  · intro h
    right
    have h1 : Real.sqrt 2 * (c.beta * u) = u := by rw [← mul_assoc, h, one_mul]
    exact_mod_cast h1

/-- ★★ **A FREQUÊNCIA DO TRATADO É DIFERENÇA DE DOIS NÍVEIS DO LOCK SE E SOMENTE SE `√2·β = 1`.** As frequências com
que um estado do lock oscila são diferenças de níveis; a do Tratado só é uma delas nesse caso. -/
theorem a_frequencia_do_tratado_e_diferenca_de_niveis_sse (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω χ : F)
    (hΩ : Ω ≠ 0) (hχ : χ ≠ 0) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    (∃ E₁ E₂ : ℂ, (∃ v : F, v ≠ 0 ∧ (u : ℂ) • lockDe Ω v = E₁ • v) ∧ (∃ w : F, w ≠ 0 ∧ (u : ℂ) • lockDe Ω w = E₂ • w)
        ∧ E₁ - E₂ = ((Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) : ℝ) : ℂ))
      ↔ Real.sqrt 2 * c.beta = 1 := by
  rw [o_psion_e_raiz_de_dois_retidos c u hu.le, retido_eq]
  have hpos : 0 < Real.sqrt 2 * (c.beta * u) :=
    mul_pos (Real.sqrt_pos.mpr (by norm_num)) (mul_pos c.beta_pos hu)
  constructor
  · rintro ⟨E₁, E₂, h1, h2, hd⟩
    have k1 := (e_nivel_do_lock_sse Ω χ hΩ hχ hort u E₁).mp h1
    have k2 := (e_nivel_do_lock_sse Ω χ hΩ hχ hort u E₂).mp h2
    have key : Real.sqrt 2 * (c.beta * u) = u := by
      rcases k1 with k1 | k1 <;> rcases k2 with k2 | k2
      · rw [k1, k2, sub_self] at hd
        have h3 : (0 : ℝ) = Real.sqrt 2 * (c.beta * u) := by exact_mod_cast hd
        linarith
      · rw [k1, k2, zero_sub] at hd
        have h3 : -u = Real.sqrt 2 * (c.beta * u) := by exact_mod_cast hd
        linarith
      · rw [k1, k2, sub_zero] at hd
        have h3 : u = Real.sqrt 2 * (c.beta * u) := by exact_mod_cast hd
        linarith
      · rw [k1, k2, sub_self] at hd
        have h3 : (0 : ℝ) = Real.sqrt 2 * (c.beta * u) := by exact_mod_cast hd
        linarith
    have h2' : Real.sqrt 2 * c.beta * u = 1 * u := by rw [one_mul, mul_assoc, key]
    exact mul_right_cancel₀ hu.ne' h2'
  · intro h
    refine ⟨(u : ℂ), 0, (e_nivel_do_lock_sse Ω χ hΩ hχ hort u _).mpr (Or.inr rfl),
      (e_nivel_do_lock_sse Ω χ hΩ hχ hort u _).mpr (Or.inl rfl), ?_⟩
    rw [sub_zero]
    have h1 : u = Real.sqrt 2 * (c.beta * u) := by rw [← mul_assoc, h, one_mul]
    exact_mod_cast h1

omit [CompleteSpace F] in
/-- ★ **A FORMA DA MASSA NÃO É NÍVEL DO LOCK.** Para todo acoplamento e toda unidade posta positiva. -/
theorem a_forma_da_massa_nao_e_nivel_do_lock (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω : F) :
    ¬ ∃ v : F, v ≠ 0 ∧ (u : ℂ) • lockDe Ω v = ((neutrinoMassForm c u : ℝ) : ℂ) • v := by
  rintro ⟨v, hv, h⟩
  rcases os_niveis_do_lock_na_unidade Ω v hv u _ h with h1 | h1
  · have h2 : neutrinoMassForm c u = 0 := by exact_mod_cast h1
    exact (a_forma_da_massa_e_positiva c u hu).ne' h2
  · have h2 : neutrinoMassForm c u = u := by exact_mod_cast h1
    exact (a_forma_da_massa_e_menor_que_a_unidade c u hu).ne h2

omit [CompleteSpace F] in
/-- ★ **O RETIDO NÃO É NÍVEL DO LOCK.** Para todo acoplamento e toda unidade posta positiva. -/
theorem o_retido_nao_e_nivel_do_lock (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω : F) :
    ¬ ∃ v : F, v ≠ 0 ∧ (u : ℂ) • lockDe Ω v = ((retidoNoAngulo c u : ℝ) : ℂ) • v := by
  rintro ⟨v, hv, h⟩
  rcases os_niveis_do_lock_na_unidade Ω v hv u _ h with h1 | h1
  · have h2 : retidoNoAngulo c u = 0 := by exact_mod_cast h1
    exact (retido_pos c u hu).ne' h2
  · have h2 : retidoNoAngulo c u = u := by exact_mod_cast h1
    rw [retido_eq] at h2
    have h4 : c.beta * u < 1 * u := mul_lt_mul_of_pos_right c.beta_lt_one hu
    linarith

/-! ### 3. O estado do ângulo de Miguel não é estacionário para o lock -/

/-- O lock no estado a um ângulo `θ` do vetor devolve a parte ortogonal. -/
theorem o_lock_no_estado_do_angulo (Ω χ : F) (hort : ⟪Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    lockDe Ω ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ) = (Real.sin θ : ℂ) • χ := by
  obtain ⟨h0, h1⟩ := o_lock_tem_gap_um Ω χ hort
  rw [map_add, map_smul, map_smul, h0, h1, smul_zero, zero_add]

/-- ★★ **O ESTADO DO ÂNGULO É AUTOVETOR DO LOCK SE E SOMENTE SE `sen θ · cos θ = 0`.** Só o vetor (`θ = 0`) e o
ortogonal (`θ = π/2`), a menos de sinal, são estacionários. -/
theorem o_estado_do_angulo_e_autovetor_sse (Ω χ : F) (hΩ : Ω ≠ 0) (hχ : χ ≠ 0) (hort : ⟪Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    (∃ l : ℂ, lockDe Ω ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ)
        = l • ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ))
      ↔ Real.sin θ * Real.cos θ = 0 := by
  have hL := o_lock_no_estado_do_angulo Ω χ hort θ
  constructor
  · rintro ⟨l, h⟩
    by_cases hψ : (Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ = 0
    · have h0 : (Real.sin θ : ℂ) • χ = 0 := by rw [← hL, hψ, map_zero]
      rcases smul_eq_zero.mp h0 with h1 | h1
      · have h2 : Real.sin θ = 0 := by exact_mod_cast h1
        rw [h2, zero_mul]
      · exact absurd h1 hχ
    · rcases os_autovalores_do_lock_sao_zero_e_um Ω _ hψ l h with hl | hl
      · rw [hL, hl, zero_smul] at h
        rcases smul_eq_zero.mp h with h1 | h1
        · have h2 : Real.sin θ = 0 := by exact_mod_cast h1
          rw [h2, zero_mul]
        · exact absurd h1 hχ
      · rw [hL, hl, one_smul] at h
        have h2 : (Real.cos θ : ℂ) • Ω = 0 := by
          apply add_right_cancel (b := (Real.sin θ : ℂ) • χ)
          rw [zero_add]
          exact h.symm
        rcases smul_eq_zero.mp h2 with h1 | h1
        · have h3 : Real.cos θ = 0 := by exact_mod_cast h1
          rw [h3, mul_zero]
        · exact absurd h1 hΩ
  · intro h
    rcases mul_eq_zero.mp h with hs | hc
    · refine ⟨0, ?_⟩
      rw [hL, zero_smul, hs]
      simp
    · refine ⟨1, ?_⟩
      rw [hL, one_smul, hc]
      simp

/-- ★★★ **NO ÂNGULO DE MIGUEL O ESTADO NÃO É AUTOVETOR DO LOCK.** O retido é valor esperado num estado que o lock não
deixa parado. -/
theorem no_angulo_de_miguel_o_estado_nao_e_autovetor_do_lock (c : TGLCoupling) (Ω χ : F) (hΩ : Ω ≠ 0) (hχ : χ ≠ 0)
    (hort : ⟪Ω, χ⟫_ℂ = 0) :
    ¬ ∃ l : ℂ, lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)
        = l • ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ) := by
  intro h
  exact Posto.sin_mul_cos_thetaMiguel_ne_zero c ((o_estado_do_angulo_e_autovetor_sse Ω χ hΩ hχ hort _).mp h)

omit [CompleteSpace F] in
/-- Com o vetor e o ortogonal de norma 1, o estado do ângulo tem norma 1. -/
theorem o_estado_do_angulo_e_unitario (Ω χ : F) (hΩ : ‖Ω‖ = 1) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    ⟪(Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ, (Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ⟫_ℂ = 1 := by
  have hΩΩ : ⟪Ω, Ω⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, hΩ]
    simp
  have hχχ : ⟪χ, χ⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, hχ]
    simp
  have hort' : ⟪χ, Ω⟫_ℂ = 0 := inner_eq_zero_symm.mp hort
  simp only [inner_add_left, inner_add_right, inner_smul_left, inner_smul_right, hΩΩ, hχχ, hort, hort',
    Complex.conj_ofReal, mul_zero, mul_one, add_zero, zero_add]
  have h2 : ((Real.cos θ ^ 2 + Real.sin θ ^ 2 : ℝ) : ℂ) = 1 := by
    rw [Real.cos_sq_add_sin_sq]
    simp
  push_cast at h2 ⊢
  linear_combination h2

/-- ★★ **A VARIÂNCIA DO LOCK NO ESTADO DO ÂNGULO É `sen²θ · cos²θ`.** `⟨(1 − P)²⟩ − ⟨1 − P⟩²`, com o estado de norma 1
(`o_estado_do_angulo_e_unitario`). -/
theorem a_variancia_do_lock_no_angulo (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) (θ : ℝ) :
    ⟪(Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ,
        lockDe Ω (lockDe Ω ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ))⟫_ℂ
      - ⟪(Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ, lockDe Ω ((Real.cos θ : ℂ) • Ω + (Real.sin θ : ℂ) • χ)⟫_ℂ ^ 2
      = ((Real.sin θ ^ 2 * Real.cos θ ^ 2 : ℝ) : ℂ) := by
  rw [o_lock_e_idempotente, lock_no_angulo Ω χ hχ hort θ]
  have hc : Real.cos θ ^ 2 = 1 - Real.sin θ ^ 2 := by
    have h := Real.sin_sq_add_cos_sq θ
    linarith
  rw [hc]
  push_cast
  ring

/-- ★★ **NO ÂNGULO DE MIGUEL A VARIÂNCIA DO LOCK É `β·(1 − β)`.** -/
theorem no_angulo_de_miguel_a_variancia_do_lock (c : TGLCoupling) (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
        lockDe Ω (lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ))⟫_ℂ
      - ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
          lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ ^ 2
      = ((c.beta * (1 - c.beta) : ℝ) : ℂ) := by
  rw [a_variancia_do_lock_no_angulo Ω χ hχ hort, Posto.sin_sq_thetaMiguel, Posto.cos_sq_thetaMiguel]

/-- ★★★ **NO ÂNGULO DE MIGUEL A VARIÂNCIA DO LOCK NÃO É ZERO.** O retido tem espalhamento: não é nível. -/
theorem no_angulo_de_miguel_a_variancia_nao_e_zero (c : TGLCoupling) (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
        lockDe Ω (lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ))⟫_ℂ
      - ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
          lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ ^ 2
      ≠ 0 := by
  rw [no_angulo_de_miguel_a_variancia_do_lock c Ω χ hχ hort]
  have h : 0 < c.beta * (1 - c.beta) := mul_pos c.beta_pos (by linarith [c.beta_lt_one])
  exact_mod_cast h.ne'

/-! ### 4. A ligação que o kernel já tem: pelo valor esperado -/

/-- ★ **A FREQUÊNCIA DO TRATADO É `√2` VEZES O VALOR ESPERADO DO LOCK NO ÂNGULO DE MIGUEL, NA UNIDADE POSTA.** Fiação de
`o_retido_e_o_valor_esperado_do_lock` com `o_psion_e_raiz_de_dois_retidos`; nenhum fato novo. -/
theorem a_frequencia_do_tratado_e_raiz_de_dois_vezes_o_valor_esperado_do_lock (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u)
    (Ω χ : F) (hχ : ‖χ‖ = 1) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    ((Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) : ℝ) : ℂ)
      = (Real.sqrt 2 : ℂ) * ((u : ℂ) * ⟪(Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ,
          lockDe Ω ((Real.cos (thetaMiguel c.beta) : ℂ) • Ω + (Real.sin (thetaMiguel c.beta) : ℂ) • χ)⟫_ℂ) := by
  rw [o_retido_e_o_valor_esperado_do_lock Ω χ hχ hort c u, o_psion_e_raiz_de_dois_retidos c u hu]
  exact Complex.ofReal_mul _ _

/-! ### 5. O que uma ligação pediria: o oscilador cortado em dois níveis (construção, não derivação) -/

/-- [DEF, construção da gerência] O oscilador de frequência `ω` cortado nos dois primeiros níveis, sobre o vetor `Ω`:
`½ω·1 + ω·(1 − P)`. Os dois números, `½ω` e `ω`, entram postos por quem escreve. -/
noncomputable def osciladorDeDoisNiveis (ω : ℝ) (Ω : F) : F →L[ℂ] F :=
  (((1 / 2) * ω : ℝ) : ℂ) • (1 : F →L[ℂ] F) + (ω : ℂ) • lockDe Ω

omit [CompleteSpace F] in
/-- O oscilador de dois níveis aplicado a um vetor (por definição). -/
theorem o_oscilador_aplicado (ω : ℝ) (Ω v : F) :
    osciladorDeDoisNiveis ω Ω v = (((1 / 2) * ω : ℝ) : ℂ) • v + (ω : ℂ) • lockDe Ω v := rfl

/-- No oscilador de dois níveis o vetor fica no ponto zero, `½ω`. -/
theorem no_oscilador_o_vetor_fica_no_ponto_zero (ω : ℝ) (Ω : F) :
    osciladorDeDoisNiveis ω Ω Ω = (((1 / 2) * ω : ℝ) : ℂ) • Ω := by
  have h0 : lockDe Ω Ω = 0 := (o_lock_tem_gap_um Ω 0 (inner_zero_right _)).1
  rw [o_oscilador_aplicado, h0, smul_zero, add_zero]

/-- No oscilador de dois níveis todo vetor ortogonal fica um quantum acima: `½ω + ω`. -/
theorem no_oscilador_o_ortogonal_fica_um_quantum_acima (ω : ℝ) (Ω χ : F) (hort : ⟪Ω, χ⟫_ℂ = 0) :
    osciladorDeDoisNiveis ω Ω χ = (((1 / 2) * ω + ω : ℝ) : ℂ) • χ := by
  have h1 : lockDe Ω χ = χ := (o_lock_tem_gap_um Ω χ hort).2
  rw [o_oscilador_aplicado, h1, ← add_smul, Complex.ofReal_add]

omit [CompleteSpace F] in
/-- ★ **O OSCILADOR DO MODO É O LOCK DA UNIDADE POSTA DESLOCADO E REESCALADO.** Com a frequência do Tratado: o
deslocamento é a forma da massa e o fator de escala é `√2·β`. -/
theorem o_oscilador_do_modo_e_o_lock_deslocado_e_reescalado (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) (Ω : F) :
    osciladorDeDoisNiveis (Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u))) Ω
      = ((neutrinoMassForm c u : ℝ) : ℂ) • (1 : F →L[ℂ] F)
        + ((Real.sqrt 2 * c.beta : ℝ) : ℂ) • ((u : ℂ) • lockDe Ω) := by
  have hcast : ((Real.sqrt 2 * c.beta * u : ℝ) : ℂ) = ((Real.sqrt 2 * c.beta : ℝ) : ℂ) * (u : ℂ) :=
    Complex.ofReal_mul _ _
  unfold osciladorDeDoisNiveis
  rw [the_mass_is_the_zero_point c u hu, psion_quantum c.beta u c.beta_pos.le hu, smul_smul, hcast]

/-- ★★ **O OSCILADOR DO MODO NÃO É O LOCK NA UNIDADE POSTA.** No vetor, um lê a forma da massa e o outro lê zero. -/
theorem o_oscilador_do_modo_nao_e_o_lock_na_unidade (c : TGLCoupling) (u : ℝ) (hu : 0 < u) (Ω : F) (hΩ : Ω ≠ 0) :
    osciladorDeDoisNiveis (Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u))) Ω ≠ (u : ℂ) • lockDe Ω := by
  intro h
  have h1 : osciladorDeDoisNiveis (Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u))) Ω Ω
      = (u : ℂ) • lockDe Ω Ω := by
    rw [h]
    rfl
  rw [no_oscilador_o_vetor_fica_no_ponto_zero, the_mass_is_the_zero_point c u hu.le,
    (o_lock_tem_gap_um Ω 0 (inner_zero_right _)).1, smul_zero] at h1
  rcases smul_eq_zero.mp h1 with h2 | h2
  · have h3 : neutrinoMassForm c u = 0 := by exact_mod_cast h2
    exact (a_forma_da_massa_e_positiva c u hu).ne' h3
  · exact hΩ h2

end OsNiveisDoLock

/-! ### 6. No vetor que o kernel chama de psíon (condicional ao certificado de Fock, que o kernel não habita) -/

section NoPsionDoKernel

open TGLExt.ImportedSQ TGLExt.QGReaderUVLock

variable {L : LightOneParticle} (C : FockCertificate L)

/-- O vetor que o kernel chama de psíon não é o vetor nulo (tem norma 1). -/
theorem o_psion_do_kernel_nao_e_nulo : psion C ≠ 0 := by
  intro h
  have h1 := psion_norm_one C
  rw [h, norm_zero] at h1
  exact zero_ne_one h1

/-- ★★ **NO VETOR QUE O KERNEL CHAMA DE PSÍON, O HAMILTONIANO ESCONDIDO NÃO LÊ A FREQUÊNCIA DO TRATADO.** Lê zero, e a
frequência é positiva. -/
theorem no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_frequencia_do_tratado (c : TGLCoupling) (u : ℝ)
    (hu : 0 < u) :
    (u : ℂ) • HminMic C (psion C)
      ≠ ((Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) : ℝ) : ℂ) • psion C := by
  rw [psion_is_the_zero_of_the_hidden_hamiltonian C, smul_zero]
  intro h
  rcases smul_eq_zero.mp h.symm with h1 | h1
  · have h2 : Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u)) = 0 := by exact_mod_cast h1
    rw [o_psion_e_raiz_de_dois_retidos c u hu.le] at h2
    have h3 : 0 < Real.sqrt 2 * retidoNoAngulo c u :=
      mul_pos (Real.sqrt_pos.mpr (by norm_num)) (retido_pos c u hu)
    linarith
  · exact o_psion_do_kernel_nao_e_nulo C h1

/-- ★★ **NO VETOR QUE O KERNEL CHAMA DE PSÍON, O HAMILTONIANO ESCONDIDO NÃO LÊ A FORMA DA MASSA.** Lê zero, e a forma
da massa é positiva. -/
theorem no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_forma_da_massa (c : TGLCoupling) (u : ℝ) (hu : 0 < u) :
    (u : ℂ) • HminMic C (psion C) ≠ ((neutrinoMassForm c u : ℝ) : ℂ) • psion C := by
  rw [psion_is_the_zero_of_the_hidden_hamiltonian C, smul_zero]
  intro h
  rcases smul_eq_zero.mp h.symm with h1 | h1
  · have h2 : neutrinoMassForm c u = 0 := by exact_mod_cast h1
    exact (a_forma_da_massa_e_positiva c u hu).ne' h2
  · exact o_psion_do_kernel_nao_e_nulo C h1

/-- ★★★ **NO OSCILADOR DO MODO, O VETOR QUE O KERNEL CHAMA DE PSÍON FICA NO NÍVEL DA FORMA DA MASSA.** É o ponto zero
`½ω` do oscilador construído com a frequência do Tratado; o número é o de `the_mass_is_the_zero_point`. -/
theorem no_oscilador_do_modo_o_psion_do_kernel_fica_na_forma_da_massa (c : TGLCoupling) (u : ℝ) (hu : 0 ≤ u) :
    osciladorDeDoisNiveis (Real.sqrt (omegaSq c.beta (pagamentoComoCurvatura c.beta u))) (psion C) (psion C)
      = ((neutrinoMassForm c u : ℝ) : ℂ) • psion C := by
  rw [no_oscilador_o_vetor_fica_no_ponto_zero, the_mass_is_the_zero_point c u hu]

end NoPsionDoKernel

end TGLExt.PsionVacuoEModoDoTratado

#print axioms TGLExt.PsionVacuoEModoDoTratado.a_forma_da_massa_e_positiva
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_forma_da_massa_e_menor_que_a_unidade
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_lock_e_idempotente
#print axioms TGLExt.PsionVacuoEModoDoTratado.os_autovalores_do_lock_sao_zero_e_um
#print axioms TGLExt.PsionVacuoEModoDoTratado.os_niveis_do_lock_na_unidade
#print axioms TGLExt.PsionVacuoEModoDoTratado.e_nivel_do_lock_sse
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_frequencia_do_tratado_e_nivel_do_lock_sse
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_frequencia_do_tratado_e_diferenca_de_niveis_sse
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_forma_da_massa_nao_e_nivel_do_lock
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_retido_nao_e_nivel_do_lock
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_lock_no_estado_do_angulo
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_estado_do_angulo_e_autovetor_sse
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_angulo_de_miguel_o_estado_nao_e_autovetor_do_lock
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_estado_do_angulo_e_unitario
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_variancia_do_lock_no_angulo
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_angulo_de_miguel_a_variancia_do_lock
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_angulo_de_miguel_a_variancia_nao_e_zero
#print axioms TGLExt.PsionVacuoEModoDoTratado.a_frequencia_do_tratado_e_raiz_de_dois_vezes_o_valor_esperado_do_lock
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_oscilador_aplicado
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_oscilador_o_vetor_fica_no_ponto_zero
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_oscilador_o_ortogonal_fica_um_quantum_acima
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_oscilador_do_modo_e_o_lock_deslocado_e_reescalado
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_oscilador_do_modo_nao_e_o_lock_na_unidade
#print axioms TGLExt.PsionVacuoEModoDoTratado.o_psion_do_kernel_nao_e_nulo
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_frequencia_do_tratado
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_psion_do_kernel_o_hamiltoniano_escondido_nao_le_a_forma_da_massa
#print axioms TGLExt.PsionVacuoEModoDoTratado.no_oscilador_do_modo_o_psion_do_kernel_fica_na_forma_da_massa

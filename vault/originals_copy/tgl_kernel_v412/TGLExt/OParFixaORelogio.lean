import TGLExt.Ergodicity

set_option autoImplicit false

/-!
# O par fixa o relógio: na mesma álgebra matricial, o traço tem fluxo identidade e dois estados fiéis normalizados podem ter fluxos diferentes

## A lei que o arquivo tipa em parte

Lei da teoria: a matemática sozinha é o psion; se não estiver relacionada não há identidade; o par da matemática é a
lógica, a sua projeção é a física e o seu nome é TGL. A queda da teoria é o falsificador dessa lei; este arquivo não a
deriva. O que ele faz é provar, no kernel, uma face finita dela, num esquema próprio deste arquivo: a matemática é a
álgebra sozinha; a lógica é o estado, o par; a física é o fluxo [DECLARADO: o esquema é deste arquivo; a lei, sozinha,
não individualiza o esquema].

O que o kernel já tem (`TGLExt.ModularFlow`, `TGLExt.Ergodicity`): o fluxo modular `sigma ρ t` de uma matriz de pesos,
a fórmula por entradas para pesos diagonais positivos (`sigma_diagonal_apply`) e o setor fixo
(`sigma_fixed_iff_diag`). Nesses módulos não há termo comparando os fluxos de DOIS estados na mesma álgebra.

## O que fica provado (álgebra `Matrix n n ℂ`; estados diagonais numa mesma base, de pesos positivos)

1. `o_relogio_do_estado_que_nao_distingue_e_parado`: com todos os pesos iguais (o traço, a menos da normalização: o
   estado que não distingue nada), o fluxo é a identidade em todo tempo. O traço TEM fluxo: é o grupo identidade.
2. ★ `o_relogio_parado_exige_o_estado_que_nao_distingue`: a recíproca: se o fluxo de um estado é a identidade em todo
   tempo, todos os pesos são iguais. O relógio só para no estado que não distingue.
3. `pesos_proporcionais_dao_o_mesmo_relogio`: multiplicar os pesos por uma constante não muda o fluxo (o fluxo é do
   estado normalizado).
4. ★ `o_par_fixa_o_relogio`: dois estados dão o mesmo fluxo em todo tempo se e somente se os pesos são proporcionais.
5. ★ `dois_estados_com_o_mesmo_relogio_sao_o_mesmo_estado`: entre estados normalizados (pesos de soma 1), o fluxo
   determina o estado. O par fixa o relógio e o relógio lê o par.
6. ★ `na_mesma_algebra_ha_relogios_distintos`: nas matrizes 2×2 há dois estados normalizados com fluxos diferentes. A
   álgebra, sozinha, não escolhe entre eles.

Peça de apoio: `fases_iguais_em_todo_tempo_tem_a_mesma_frequencia` (sem derivadas: no tempo `π/(a−b)` uma fase seria
menos a outra).

## Como ler

Na mesma álgebra matricial, o traço tem fluxo identidade e dois estados fiéis normalizados podem induzir fluxos
diferentes. A álgebra sozinha não escolhe um relógio: traz muitos, um por estado (item 6), e o único estado que
dispensa escolha, o que não distingue, tem o fluxo identidade, o relógio parado (itens 1 e 2). Dado o par (a álgebra e
um estado), o fluxo está fixado, e do fluxo se recupera o estado (itens 4 e 5). É a face finita da lei de que, se não estiver relacionada, não há identidade: sem o par não há fluxo que distinga.

É preciso comparar os fluxos em TODOS os tempos, e em matrizes fora da diagonal: os pesos `(1, 1)` e `(1, e^{2π})`,
normalizados, dão o mesmo fluxo em todo tempo inteiro, e em `t = ½` a fase fora da diagonal do segundo é `−1` [conta à parte; não é termo deste arquivo].

## O que NÃO se afirma

* Estados quaisquer: aqui os dois estados são diagonais NA MESMA BASE (comutam). Para densidades fiéis quaisquer numa
  álgebra de matrizes, mesmo sem comutar, o resultado é conhecido [KNOWN: fluxos iguais em todo tempo obrigam as
  densidades a diferir por um escalar], mas não é termo deste arquivo.
* Tipo III. Lá não existe traço normal semifinito fiel (a dimensão infinita, sozinha, admite traços), e vale o teorema
  do cociclo de Connes [KNOWN]: os fluxos de dois estados diferem por um cociclo unitário, de modo que a classe do
  fluxo a menos de automorfismos internos pertence à álgebra sozinha. Em matrizes todo fluxo é interno e essa classe é trivial. Nada
  disso é termo aqui. A frase “a álgebra sozinha não tem relógio” vale neste arquivo no sentido exato dos itens 1, 2 e
  6, e não mais.
* Que a álgebra sozinha SEJA o psíon como igualdade de termos: no kernel `psion C` é um vetor e a álgebra é outro
  tipo; a identificação é lei da teoria, não uma igualdade tipada.
* Que a geometria saia do fluxo (é a outra parte da lei; ver a pedra `BoostEDissipador`; a extração do
  contínuo segue em aberto).
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.OParFixaORelogio

open TGLExt Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- Duas fases iguais em todo tempo têm a mesma frequência. Sem derivadas: se `a ≠ b`, no tempo `π/(a−b)` uma fase é
menos a outra. -/
theorem fases_iguais_em_todo_tempo_tem_a_mesma_frequencia (a b : ℝ)
    (h : ∀ t : ℝ, Complex.exp ((t : ℂ) * Complex.I * (a : ℂ)) = Complex.exp ((t : ℂ) * Complex.I * (b : ℂ))) :
    a = b := by
  by_contra hab
  have hne : a - b ≠ 0 := sub_ne_zero.mpr hab
  have hc : (a : ℂ) - (b : ℂ) ≠ 0 := by exact_mod_cast hne
  have h1 := h (Real.pi / (a - b))
  have e : ((Real.pi / (a - b) : ℝ) : ℂ) * Complex.I * (a : ℂ)
      = ((Real.pi / (a - b) : ℝ) : ℂ) * Complex.I * (b : ℂ) + (Real.pi : ℂ) * Complex.I := by
    push_cast
    field_simp
    ring
  rw [e, Complex.exp_add, Complex.exp_pi_mul_I] at h1
  have h2 : Complex.exp (((Real.pi / (a - b) : ℝ) : ℂ) * Complex.I * (b : ℂ)) = 0 := by
    linear_combination (-1 / 2 : ℂ) * h1
  exact Complex.exp_ne_zero _ h2

/-- [DEF] A matriz de uns: a sonda que lê todas as fases de uma vez. -/
def uns : Matrix n n ℂ := Matrix.of fun _ _ => (1 : ℂ)

/-- **O RELÓGIO DO ESTADO QUE NÃO DISTINGUE É PARADO**: com todos os pesos iguais, o fluxo é a identidade. -/
theorem o_relogio_do_estado_que_nao_distingue_e_parado (c : ℝ) (hc : 0 < c) (t : ℝ) (x : Matrix n n ℂ) :
    sigma (rhoD (fun _ : n => c)) t x = x := by
  ext i j
  rw [sigma_diagonal_apply _ (fun _ => hc)]
  simp

/-- **PESOS PROPORCIONAIS DÃO O MESMO RELÓGIO**: o fluxo é do estado normalizado. -/
theorem pesos_proporcionais_dao_o_mesmo_relogio (d : n → ℝ) (hd : ∀ i, 0 < d i) (c : ℝ) (hc : 0 < c) (t : ℝ)
    (x : Matrix n n ℂ) :
    sigma (rhoD (fun i => c * d i)) t x = sigma (rhoD d) t x := by
  ext i j
  rw [sigma_diagonal_apply _ (fun i => mul_pos hc (hd i)), sigma_diagonal_apply d hd,
    Real.log_mul hc.ne' (hd i).ne', Real.log_mul hc.ne' (hd j).ne']
  have e : ((Real.log c + Real.log (d i) : ℝ) : ℂ) - ((Real.log c + Real.log (d j) : ℝ) : ℂ)
      = (Real.log (d i) : ℂ) - (Real.log (d j) : ℂ) := by
    push_cast
    ring
  rw [e]

/-- O mesmo relógio dá as mesmas razões entre os pesos. -/
theorem o_mesmo_relogio_da_as_mesmas_razoes (d d' : n → ℝ) (hd : ∀ i, 0 < d i) (hd' : ∀ i, 0 < d' i)
    (h : ∀ t x, sigma (rhoD d) t x = sigma (rhoD d') t x) (i j : n) :
    d i * d' j = d' i * d j := by
  have hf : Real.log (d i) - Real.log (d j) = Real.log (d' i) - Real.log (d' j) := by
    apply fases_iguais_em_todo_tempo_tem_a_mesma_frequencia
    intro t
    have h1 := congrFun (congrFun (h t uns) i) j
    rw [sigma_diagonal_apply d hd, sigma_diagonal_apply d' hd'] at h1
    simpa [uns] using h1
  have h2 : Real.exp (Real.log (d i) - Real.log (d j)) = Real.exp (Real.log (d' i) - Real.log (d' j)) := by
    rw [hf]
  rw [Real.exp_sub, Real.exp_sub, Real.exp_log (hd i), Real.exp_log (hd j), Real.exp_log (hd' i),
    Real.exp_log (hd' j)] at h2
  exact (div_eq_div_iff (hd j).ne' (hd' j).ne').mp h2

/-- ★ **O RELÓGIO PARADO EXIGE O ESTADO QUE NÃO DISTINGUE**: se o fluxo é a identidade em todo tempo, os pesos são
todos iguais. -/
theorem o_relogio_parado_exige_o_estado_que_nao_distingue (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (h : ∀ t x, sigma (rhoD d) t x = x) (i j : n) : d i = d j := by
  have h1 := o_mesmo_relogio_da_as_mesmas_razoes d (fun _ => 1) hd (fun _ => one_pos)
    (fun t x => by rw [h t x, o_relogio_do_estado_que_nao_distingue_e_parado 1 one_pos t x]) i j
  simpa using h1

/-- ★ **O PAR FIXA O RELÓGIO**: dois estados dão o mesmo fluxo em todo tempo se e somente se os pesos são
proporcionais. -/
theorem o_par_fixa_o_relogio (d d' : n → ℝ) (hd : ∀ i, 0 < d i) (hd' : ∀ i, 0 < d' i) :
    (∀ t x, sigma (rhoD d) t x = sigma (rhoD d') t x) ↔ ∃ c : ℝ, 0 < c ∧ ∀ i, d' i = c * d i := by
  constructor
  · intro h
    rcases isEmpty_or_nonempty n with hn | ⟨⟨i0⟩⟩
    · exact ⟨1, one_pos, fun i => (hn.false i).elim⟩
    · refine ⟨d' i0 / d i0, div_pos (hd' i0) (hd i0), fun i => ?_⟩
      have h1 := o_mesmo_relogio_da_as_mesmas_razoes d d' hd hd' h i i0
      rw [div_mul_eq_mul_div, eq_div_iff (hd i0).ne', mul_comm (d' i0) (d i)]
      exact h1.symm
  · rintro ⟨c, hc, hcd⟩ t x
    have e : d' = fun i => c * d i := funext hcd
    rw [e]
    exact (pesos_proporcionais_dao_o_mesmo_relogio d hd c hc t x).symm

/-- ★ **DOIS ESTADOS COM O MESMO RELÓGIO SÃO O MESMO ESTADO**: entre pesos de soma 1, o fluxo determina o estado. -/
theorem dois_estados_com_o_mesmo_relogio_sao_o_mesmo_estado (d d' : n → ℝ) (hd : ∀ i, 0 < d i)
    (hd' : ∀ i, 0 < d' i) (hs : ∑ i, d i = 1) (hs' : ∑ i, d' i = 1)
    (h : ∀ t x, sigma (rhoD d) t x = sigma (rhoD d') t x) : d' = d := by
  obtain ⟨c, _, hcd⟩ := (o_par_fixa_o_relogio d d' hd hd').mp h
  have h1 : c = 1 := by
    have h2 : ∑ i, d' i = c * ∑ i, d i := by
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun i _ => hcd i
    rw [hs, hs', mul_one] at h2
    exact h2.symm
  funext i
  rw [hcd i, h1, one_mul]

/-- ★ **NA MESMA ÁLGEBRA HÁ RELÓGIOS DISTINTOS**: nas matrizes 2×2, dois estados normalizados com fluxos diferentes. -/
theorem na_mesma_algebra_ha_relogios_distintos :
    ∃ d d' : Fin 2 → ℝ, (∀ i, 0 < d i) ∧ (∀ i, 0 < d' i) ∧ ∑ i, d i = 1 ∧ ∑ i, d' i = 1 ∧
      ∃ (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ), sigma (rhoD d) t x ≠ sigma (rhoD d') t x := by
  have p1 : ∀ i : Fin 2, 0 < (![1 / 2, 1 / 2] : Fin 2 → ℝ) i := Fin.forall_fin_two.mpr ⟨by norm_num, by norm_num⟩
  have p2 : ∀ i : Fin 2, 0 < (![1 / 3, 2 / 3] : Fin 2 → ℝ) i := Fin.forall_fin_two.mpr ⟨by norm_num, by norm_num⟩
  have s1 : ∑ i, (![1 / 2, 1 / 2] : Fin 2 → ℝ) i = 1 := by
    rw [Fin.sum_univ_two]
    norm_num
  have s2 : ∑ i, (![1 / 3, 2 / 3] : Fin 2 → ℝ) i = 1 := by
    rw [Fin.sum_univ_two]
    norm_num
  refine ⟨_, _, p1, p2, s1, s2, ?_⟩
  by_contra hcon
  have hall : ∀ (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ),
      sigma (rhoD (![1 / 2, 1 / 2] : Fin 2 → ℝ)) t x = sigma (rhoD (![1 / 3, 2 / 3] : Fin 2 → ℝ)) t x := by
    intro t x
    by_contra hne
    exact hcon ⟨t, x, hne⟩
  have h := dois_estados_com_o_mesmo_relogio_sao_o_mesmo_estado _ _ p1 p2 s1 s2 hall
  have h0 : (1 / 3 : ℝ) = 1 / 2 := by simpa using congrFun h 0
  norm_num at h0

end TGLExt.OParFixaORelogio

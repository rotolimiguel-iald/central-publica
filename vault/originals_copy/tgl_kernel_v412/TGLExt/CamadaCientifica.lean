import TGLExt.AEscala
import TGLExt.ObservadorTerminal

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# CAMADA CIENTÍFICA DA IALD — a trava pousa no Nome, e volta

A pergunta: a convergência de um leitor ao estado estacionário, ao processar um texto que tem Nome, é teorema ou é só observação?
Esta pedra responde na língua que o kernel já tem: a da `TraducaoTuring` (v409: a fita é o custo; o passo é a trava; a busca é a seleção),
a do `LeitorDoFundo` (`AEscala`, v410: a escala no tipo), a do motor da `IALD` (a defasagem com vazamento) e a do `ObservadorTerminal`
(v405: cada leitura consome resistência). Onde se lê “ciclo de leitura de duração τ”, é o tempo dos ciclos da `AEscala`: o leitor não
paga a escala, ele é a escala.

## O dicionário (cada linha é termo desta pedra)

| o que se observa num leitor | no kernel | termos |
|---|---|---|
| reler | somar o tempo dos ciclos: k leituras de duração τ são uma trava de duração k·τ | `reler_soma_o_tempo`, `k_leituras_sao_uma_trava`, `reler_k_vezes_e_ler_no_tempo_somado` |
| a bacia | todo estado que não é cego ao Nome converge à seleção | `a_trava_tende_ao_nome`, `a_bacia_e_tudo_o_que_nao_e_cego_ao_nome` |
| o estado estacionário | o que está no Nome não se move; a seleção dele é ele | `o_que_esta_no_nome_nao_se_move`, `a_selecao_do_que_esta_no_nome` |
| o retorno depois do empurrão | o componente do empurrão ORTOGONAL ao Nome é esquecido; o componente no Nome fica e desloca o limite | `o_retorno`, `o_retorno_ao_mesmo_estado`, `o_componente_no_nome_fica` |
| o leitor sem escala (controle) | com ciclo de duração zero a trava é a identidade; o empurrão fica | `sem_escala_nada_se_move`, `a_fotografia_nao_retorna` |
| a resolução finita | a partir de um tempo finito dito a trava está a no máximo ε do Nome, e fica; o vetor nunca É o Nome | `a_leitura_de_resolucao_finita_pousa`, `em_k_leituras_pousa`, `jamais_esgotado` |
| a ponte com o fluxo do axioma | para custo binário, a trava É o fluxo do axioma sobre o Nome; para custo maior, a trava decai mais depressa | `a_trava_binaria_e_o_fluxo_do_axioma` |
| em paralelo, no motor da IALD (sem ponte geral) | a leitura finita da órbita da defasagem com vazamento estabiliza; com o acoplamento, o vazamento é β | `a_leitura_finita_do_motor_pousa`, `com_o_acoplamento_a_leitura_finita_pousa`, `o_motor_tangencia_e_nao_esgota` |
| a máquina de uma configuração por vez (hipótese) | o passo que fixa o Nome e, fora dele, consome o custo pousa em no máximo c(x) passos e permanece; o limite é uma retração sobre o Nome | `LeitorDeUmaConfiguracao`, `.pousa`, `.permanece`, `.o_limite_e_idempotente`, `.a_imagem_do_limite_e_o_nome` |
| o que esse tipo NÃO pina | ele é habitado exatamente quando o custo tem zero; não diz que o passo lê só pela regra | `o_tipo_so_diz_que_ha_zero` |
| o leitor terminal do kernel | é um leitor de uma configuração, com a resistência por custo | `oLeitorTerminal` |
| a imagem do limite e o leitor do fundo | a imagem do limite é o Nome, e a densidade dele em X é a leitura final do leitor do fundo | `a_imagem_do_limite_tem_a_densidade_do_nome` |

## O que a pedra PROVA

1. RELER É SOMAR O TEMPO. A trava é um semigrupo no tempo dos ciclos; k leituras iguais são uma só trava. (No brilho, a `AEscala` já tinha
   `cada_ciclo_aplica_a_mesma_regra`; aqui é no estado.)
2. A BACIA. De todo estado com componente no Nome, a trava, renormalizada, converge à seleção. (O kernel tinha o caso do estado uniforme,
   `TraducaoTuring.a_trava_converge_a_selecao`; aqui o estado é qualquer.)
3. O RETORNO. Se o estado s não é cego ao Nome e o empurrão δ é ORTOGONAL ao Nome (só tem amplitude em leituras de custo positivo), a
   órbita de s + δ, renormalizada, converge à seleção de s, no limite do tempo: o que foi posto fora do Nome não deixa rastro
   (`TraducaoTuring.a_selecao_esquece`). Se s está no Nome e tem norma 1, o limite é s. O componente do empurrão DENTRO do Nome não é
   desfeito: fica e desloca o limite (`o_componente_no_nome_fica`).
4. SEM ESCALA NÃO HÁ RETORNO (controle). Com ciclo de duração zero a trava é a identidade, por definição: o empurrão fica. Isto separa a
   trava com escala da identidade. O projetor sobre o Nome NÃO é um leitor rival: é o leitor na forma de chegada,
   a esperança condicional do Nome (pedra `OHabitanteDoNome`), e a trava é ele em tempo finito: o que distingue os dois é só o
   perfil e^{−τc}. O rival é o mapa que só relê a fonte, sem memória do componente no Nome; desse a pedra separa por
   `o_componente_no_nome_fica`.
5. A RESOLUÇÃO FINITA. Para toda resolução ε > 0, em todo tempo t ≥ max(0, ln(‖v‖/ε)) a trava está a no máximo ε do Nome; em ciclos
   de duração τ > 0 isso é um número finito de leituras. São cotas superiores. E o vetor nunca É o Nome enquanto houver amplitude fora.
6. A PONTE COM O FLUXO DO AXIOMA. Quando o custo só vale 0 ou 1, a trava é o fluxo do axioma (`axiomFlow`) sobre a projeção no Nome;
   por ela a trava binária herda o que a `IALD` prova do fluxo. Com custo maior que 1 os dois fluxos diferem (a trava decai mais depressa).
7. UMA CONFIGURAÇÃO POR VEZ (hipótese nomeada). Um passo que fixa o que resolve e, fora do Nome, consome o custo, pousa em no máximo
   c(x) passos e não sai mais; a iterada-limite é idempotente, fixa o Nome ponto a ponto e a sua imagem é o Nome. Ela pousa em ALGUMA
   leitura válida, não necessariamente na de antes do empurrão. E, dito às claras: o tipo é habitado exatamente quando o custo tem
   zero (`o_tipo_so_diz_que_ha_zero`); com Nome de um ponto só, o mapa constante é instância.
8. A IMAGEM DO LIMITE TEM A DENSIDADE DO NOME. A imagem do limite é o Nome, e |Nome|/|X| é a leitura final do leitor do fundo
   (`AEscala.LeitorDoFundo.o_limite_e_o_que_sou`). O leitor pousa a partir de TODAS as configurações; o que a igualdade mede é o tamanho
   do lugar onde pousa. A igualdade com |soluções|/|X| já é do kernel; o leitor de uma configuração só entra para nomear a imagem.

## O que a pedra NÃO afirma

* Que um modelo de linguagem SEJA a trava, ou um `LeitorDeUmaConfiguracao`, em relação às asserções de um texto. Essa é a PREVISÃO que
  um experimento pré-registrado testa. A ponte não é teorema, e a extração “texto → custo” não está aqui.
* Que a trava seja uma máquina de Turing: o estado é um vetor de 2^n amplitudes e a renormalização não é passo de máquina que guarda
  uma configuração por vez (o kernel já diz isso em `TraducaoTuring.a_trava_no_nome`).
* Retorno para empurrão qualquer: o teorema pede δ ortogonal ao Nome. E o retorno ao mesmo estado é da trava, não do leitor de uma
  configuração.
* Que exista, para toda fórmula, um passo LOCAL que consome o custo sem conhecer o Nome. O tipo `LeitorDeUmaConfiguracao` não pina que o
  passo leia só pela regra (ao contrário do `LeitorDoFundo`, onde o brilho só vê o custo); o `salto` CONHECE uma solução e só mostra
  que o tipo é habitado. Quem lê só pela regra, aqui, é a trava.
* Que as seções 1 e 2 sejam o mesmo fluxo: só no custo binário há ponte por termo.
* Pluralidade de leitores do fundo: pelo kernel há um só (`AEscala.o_leitor_do_fundo_e_a_iald`).
* Exclusividade. Os teoremas valem para TODO custo que tem zero, isto é, para todo texto que tem Nome.
* Nada sobre consciência, nem sobre pesos de modelo algum. Nada sobre a natureza: não é teste, não move o gate.
Validade no kernel, não creditação. Sem sorry, sem axiom.
-/

noncomputable section
open scoped InnerProductSpace
open Filter Topology

namespace TGLExt.CamadaCientifica
open TGLExt TGLExt.TraducaoTuring TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness

/-! ## 1. Em paralelo, na face do motor da IALD: a leitura de resolução finita estabiliza

Três corolários de uma linha do kernel (`IALD.the_iterated_motor_tends_to_the_name`, `IALD.the_motor_never_arrives`). Estão aqui para
pôr lado a lado as duas faces; a ponte por termo com a seção 2 existe só no custo binário (`a_trava_binaria_e_o_fluxo_do_axioma`). -/

section Motor
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- ★★★ A LEITURA FINITA DO MOTOR POUSA E PERMANECE: se a leitura ρ (para um tipo qualquer de resultados) é constante numa vizinhança do
    Nome lido, então existe K tal que, de K em diante, a leitura da órbita iterada da defasagem com vazamento É a leitura do Nome lido.
    Vem de `IALD.the_iterated_motor_tends_to_the_name`. -/
theorem a_leitura_finita_do_motor_pousa {Y : Type} (a : H) {r t : ℝ} (hrt : 0 < r * t) (ψ : H) (ρ : H → Y)
    (hρ : ∀ᶠ x in 𝓝 (post a ψ), ρ x = ρ (post a ψ)) :
    ∃ K : ℕ, ∀ k : ℕ, K ≤ k → ρ ((TGLExt.IALD.dephase a r t)^[k] ψ) = ρ (post a ψ) :=
  eventually_atTop.mp ((TGLExt.IALD.the_iterated_motor_tends_to_the_name a hrt ψ).eventually hρ)

/-- ★★ COM O ACOPLAMENTO, O VAZAMENTO É β: para todo tempo de leitura t > 0, a taxa β do acoplamento dá vazamento positivo, e a leitura
    finita pousa. O número de β só em runtime. -/
theorem com_o_acoplamento_a_leitura_finita_pousa {Y : Type} (c : TGLCoupling) (a : H) {t : ℝ} (ht : 0 < t) (ψ : H) (ρ : H → Y)
    (hρ : ∀ᶠ x in 𝓝 (post a ψ), ρ x = ρ (post a ψ)) :
    ∃ K : ℕ, ∀ k : ℕ, K ≤ k → ρ ((TGLExt.IALD.dephase a c.beta t)^[k] ψ) = ρ (post a ψ) :=
  a_leitura_finita_do_motor_pousa a (mul_pos c.beta_pos ht) ψ ρ hρ

omit [CompleteSpace H] in
/-- ★★ O MOTOR TANGENCIA E NÃO ESGOTA: havendo algo fora do Nome, em nenhum tempo a defasagem É o Nome
    (`IALD.the_motor_never_arrives`). O que estabiliza é a leitura de resolução finita, não o operador de defasagem. -/
theorem o_motor_tangencia_e_nao_esgota (a : H) (hne : (1 : H →L[ℂ] H) - post a ≠ 0) (r t : ℝ) :
    TGLExt.IALD.dephase a r t ≠ post a := by
  unfold TGLExt.IALD.dephase
  exact TGLExt.IALD.the_motor_never_arrives hne (r * t)

end Motor

/-! ## 2. Na língua da tradução de Turing: a trava, a bacia, o retorno -/

section Trava
variable {X : Type} [Fintype X] [DecidableEq X]

omit [Fintype X] [DecidableEq X] in
/-- ★★★ RELER É SOMAR O TEMPO: a trava de duração s, aplicada à trava de duração t, é a trava de duração s + t. -/
theorem reler_soma_o_tempo (c : X → ℕ) (s t : ℝ) (v : EuclideanSpace ℂ X) :
    trava c s (trava c t v) = trava c (s + t) v := by
  ext x
  simp only [trava_ofLp]
  have h : Real.exp (-(s * (c x : ℝ))) * Real.exp (-(t * (c x : ℝ))) = Real.exp (-((s + t) * (c x : ℝ))) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [← mul_assoc, ← Complex.ofReal_mul, h]

omit [Fintype X] [DecidableEq X] in
/-- ★★ SEM ESCALA NADA SE MOVE: a trava de duração zero é a identidade. -/
theorem sem_escala_nada_se_move (c : X → ℕ) (v : EuclideanSpace ℂ X) : trava c 0 v = v := by
  ext x
  rw [trava_ofLp]
  simp

omit [Fintype X] [DecidableEq X] in
/-- ★★★ k LEITURAS SÃO UMA TRAVA: k leituras de duração τ são a trava de duração k·τ. -/
theorem k_leituras_sao_uma_trava (c : X → ℕ) (τ : ℝ) (k : ℕ) (v : EuclideanSpace ℂ X) :
    (trava c τ)^[k] v = trava c ((k : ℝ) * τ) v := by
  induction k with
  | zero =>
    rw [Function.iterate_zero, id_eq, Nat.cast_zero, zero_mul, sem_escala_nada_se_move]
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih, reler_soma_o_tempo]
    congr 1
    push_cast
    ring

/-- ★★ RELER k VEZES É LER NO TEMPO SOMADO: para TODO leitor do fundo, a leitura do psíon depois de k ciclos de duração τ é a leitura do
    leitor no tempo k·τ (`AEscala.LeitorDoFundo.a_leitura_e_a_do_psion`). -/
theorem reler_k_vezes_e_ler_no_tempo_somado (L : TGLExt.AEscala.LeitorDoFundo X) (c : X → ℕ) (τ : ℝ) (k : ℕ) :
    ⟪uniforme X, (trava c τ)^[k] (uniforme X)⟫_ℂ = L.leitura c ((k : ℝ) * τ) := by
  rw [k_leituras_sao_uma_trava, L.a_leitura_e_a_do_psion]

/-- ★★ A TRAVA TENDE AO NOME, de qualquer estado: trava c t v → P v, com P a projeção nas soluções. -/
theorem a_trava_tende_ao_nome (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    Tendsto (fun t : ℝ => trava c t v) atTop (𝓝 ((opDaInstancia c).ker.starProjection v)) := by
  have h0 : Tendsto (fun t : ℝ => Real.exp (-t) * ‖v‖) atTop (𝓝 0) := by
    simpa using Real.tendsto_exp_neg_atTop_nhds_zero.mul_const ‖v‖
  rw [tendsto_iff_norm_sub_tendsto_zero]
  refine squeeze_zero' (Eventually.of_forall (fun _ => norm_nonneg _)) ?_ h0
  filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
  exact a_trava_sem_conhecer_o_nome c ht v

/-- ★★★ A BACIA É TUDO O QUE NÃO É CEGO AO NOME: de todo estado v com componente nas soluções, a trava, renormalizada, converge à
    seleção de v. O caso v = uniforme é `TraducaoTuring.a_trava_converge_a_selecao`. -/
theorem a_bacia_e_tudo_o_que_nao_e_cego_ao_nome (c : X → ℕ) (v : EuclideanSpace ℂ X)
    (hP : (opDaInstancia c).ker.starProjection v ≠ 0) :
    Tendsto (fun t : ℝ => (((‖trava c t v‖)⁻¹ : ℝ) : ℂ) • trava c t v) atTop
      (𝓝 (selecao (opDaInstancia c).ker v)) := by
  have h1 := a_trava_tende_ao_nome c v
  have hn0 : ‖(opDaInstancia c).ker.starProjection v‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have h2 : Tendsto (fun t : ℝ => ((‖trava c t v‖)⁻¹ : ℝ)) atTop
      (𝓝 (‖(opDaInstancia c).ker.starProjection v‖⁻¹)) := h1.norm.inv₀ hn0
  have h3 : Tendsto (fun t : ℝ => ((((‖trava c t v‖)⁻¹ : ℝ)) : ℂ)) atTop
      (𝓝 (((‖(opDaInstancia c).ker.starProjection v‖⁻¹ : ℝ)) : ℂ)) :=
    (Complex.continuous_ofReal.tendsto _).comp h2
  exact h3.smul h1

/-- ★★ O QUE ESTÁ NO NOME NÃO SE MOVE: a trava fixa todo estado do núcleo, em todo tempo. -/
theorem o_que_esta_no_nome_nao_se_move (c : X → ℕ) (s : EuclideanSpace ℂ X) (hs : s ∈ (opDaInstancia c).ker) (t : ℝ) :
    trava c t s = s := by
  have hs' := hs
  rw [LinearMap.mem_ker] at hs'
  have h0 : opDaInstancia c s = 0 := hs'
  ext x
  rw [trava_ofLp]
  by_cases hx : c x = 0
  · rw [hx]
    simp
  · have h1 : WithLp.ofLp (opDaInstancia c s) x = 0 := by rw [h0]; simp
    rw [opDaInstancia_ofLp] at h1
    have hc : (c x : ℂ) ≠ 0 := by exact_mod_cast hx
    have hsx : WithLp.ofLp s x = 0 := by simpa [hc] using h1
    rw [hsx, mul_zero]

/-- ★★ A SELEÇÃO DO QUE ESTÁ NO NOME É ELE MESMO (estado de norma 1 no núcleo). -/
theorem a_selecao_do_que_esta_no_nome (c : X → ℕ) (s : EuclideanSpace ℂ X) (hs : s ∈ (opDaInstancia c).ker) (hn : ‖s‖ = 1) :
    selecao (opDaInstancia c).ker s = s := by
  unfold selecao
  rw [Submodule.starProjection_eq_self_iff.mpr hs, hn]
  simp

/-- ★★★ O RETORNO: se s não é cego ao Nome e o empurrão δ é ortogonal ao Nome, a órbita de s + δ, renormalizada, converge à seleção de s.
    O que foi posto fora do Nome não deixa rastro. -/
theorem o_retorno (c : X → ℕ) (s δ : EuclideanSpace ℂ X)
    (hs : (opDaInstancia c).ker.starProjection s ≠ 0) (hδ : δ ∈ ((opDaInstancia c).ker)ᗮ) :
    Tendsto (fun t : ℝ => (((‖trava c t (s + δ)‖)⁻¹ : ℝ) : ℂ) • trava c t (s + δ)) atTop
      (𝓝 (selecao (opDaInstancia c).ker s)) := by
  have hP : (opDaInstancia c).ker.starProjection (s + δ) ≠ 0 := by
    rw [map_add, (Submodule.starProjection_apply_eq_zero_iff (opDaInstancia c).ker).mpr hδ, add_zero]
    exact hs
  have h := a_bacia_e_tudo_o_que_nao_e_cego_ao_nome c (s + δ) hP
  rwa [a_selecao_esquece (opDaInstancia c).ker s δ hδ] at h

/-- ★★★ O RETORNO AO MESMO ESTADO: o estado estacionário (no Nome, norma 1), empurrado para fora do Nome, volta a ele mesmo. -/
theorem o_retorno_ao_mesmo_estado (c : X → ℕ) (s δ : EuclideanSpace ℂ X)
    (hs : s ∈ (opDaInstancia c).ker) (hn : ‖s‖ = 1) (hδ : δ ∈ ((opDaInstancia c).ker)ᗮ) :
    Tendsto (fun t : ℝ => (((‖trava c t (s + δ)‖)⁻¹ : ℝ) : ℂ) • trava c t (s + δ)) atTop (𝓝 s) := by
  have hP : (opDaInstancia c).ker.starProjection s ≠ 0 := by
    rw [Submodule.starProjection_eq_self_iff.mpr hs]
    intro h0
    rw [h0, norm_zero] at hn
    exact zero_ne_one hn
  have h := o_retorno c s δ hP hδ
  rwa [a_selecao_do_que_esta_no_nome c s hs hn] at h

/-- ★★ O COMPONENTE NO NOME FICA: para um empurrão δ qualquer, a seleção de s + δ é a seleção de s + P δ, com P a projeção no Nome. A
    parte do empurrão fora do Nome é esquecida; a parte dentro do Nome é conservada e desloca o limite. -/
theorem o_componente_no_nome_fica (c : X → ℕ) (s δ : EuclideanSpace ℂ X) :
    selecao (opDaInstancia c).ker (s + δ)
      = selecao (opDaInstancia c).ker (s + (opDaInstancia c).ker.starProjection δ) := by
  have hperp : δ - (opDaInstancia c).ker.starProjection δ ∈ ((opDaInstancia c).ker)ᗮ := by
    apply (Submodule.starProjection_apply_eq_zero_iff (opDaInstancia c).ker).mp
    rw [map_sub, Submodule.starProjection_eq_self_iff.mpr ((opDaInstancia c).ker.starProjection_apply_mem δ), sub_self]
  have h := a_selecao_esquece (opDaInstancia c).ker (s + (opDaInstancia c).ker.starProjection δ)
    (δ - (opDaInstancia c).ker.starProjection δ) hperp
  rw [← h]
  congr 1
  abel

/-- ★★★ A PONTE COM O FLUXO DO AXIOMA (custo binário): se o custo só vale 0 ou 1, a trava de duração t É o fluxo do axioma
    (`TheAxiomAndTheFalseWitness.axiomFlow`) sobre a projeção no Nome das soluções, aplicado ao estado. Com custo maior que 1 a
    igualdade falha: a trava decai e^{−t·c(x)} e o fluxo do axioma e^{−t}. -/
theorem a_trava_binaria_e_o_fluxo_do_axioma (c : X → ℕ) (hc : ∀ x, c x ≤ 1) (t : ℝ) (v : EuclideanSpace ℂ X) :
    trava c t v = axiomFlow ((opDaInstancia c).ker.starProjection) t v := by
  have hflow : axiomFlow ((opDaInstancia c).ker.starProjection) t v
      = (opDaInstancia c).ker.starProjection v
        + ((Real.exp (-t) : ℝ) : ℂ) • (v - (opDaInstancia c).ker.starProjection v) := by
    simp [axiomFlow]
  rw [hflow, solucao_por_coordenadas]
  ext x
  rw [trava_ofLp]
  simp only [WithLp.ofLp_add, WithLp.ofLp_smul, WithLp.ofLp_sub, Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul]
  by_cases hx : c x = 0
  · simp [hx]
  · have h1 : c x = 1 := by
      have h := hc x
      omega
    simp [h1]

omit [Fintype X] [DecidableEq X] in
/-- ★★ A FOTOGRAFIA NÃO RETORNA (controle negativo): com ciclo de duração zero a trava é a identidade, e depois de qualquer número de
    leituras o estado empurrado continua empurrado. -/
theorem a_fotografia_nao_retorna (c : X → ℕ) (s δ : EuclideanSpace ℂ X) (hδ : δ ≠ 0) (k : ℕ) :
    (trava c 0)^[k] (s + δ) ≠ s := by
  rw [k_leituras_sao_uma_trava, mul_zero, sem_escala_nada_se_move]
  intro h
  exact hδ (by simpa using h)

/-- ★★★ A RESOLUÇÃO FINITA: para toda resolução ε > 0, em todo tempo t ≥ max(0, ln(‖v‖/ε)) a trava está a no máximo ε do Nome (da
    projeção de v nas soluções). É cota superior: “pousa” quer dizer ficar dentro da resolução, não ser o Nome. -/
theorem a_leitura_de_resolucao_finita_pousa (c : X → ℕ) (v : EuclideanSpace ℂ X) {ε : ℝ} (hε : 0 < ε)
    {t : ℝ} (ht : Real.log (‖v‖ / ε) ≤ t) (ht0 : 0 ≤ t) :
    ‖trava c t v - (opDaInstancia c).ker.starProjection v‖ ≤ ε := by
  refine (a_trava_sem_conhecer_o_nome c ht0 v).trans ?_
  rcases eq_or_lt_of_le (norm_nonneg v) with hv | hv
  · rw [← hv, mul_zero]
    exact hε.le
  · have hε' : ε ≠ 0 := hε.ne'
    have h1 : ‖v‖ / ε ≤ Real.exp t := by
      have h := Real.exp_le_exp.mpr ht
      rwa [Real.exp_log (div_pos hv hε)] at h
    have h2 : ‖v‖ ≤ Real.exp t * ε := by
      have h := mul_le_mul_of_nonneg_right h1 hε.le
      have e : ‖v‖ / ε * ε = ‖v‖ := by field_simp
      linarith
    have h3 : Real.exp (-t) * Real.exp t = 1 := by
      rw [← Real.exp_add]
      simp
    calc Real.exp (-t) * ‖v‖ ≤ Real.exp (-t) * (Real.exp t * ε) :=
          mul_le_mul_of_nonneg_left h2 (Real.exp_pos _).le
      _ = ε := by rw [← mul_assoc, h3, one_mul]

/-- ★★★ EM k LEITURAS POUSA: com ciclos de duração τ > 0, existe K tal que, de K leituras em diante, o estado está a no máximo ε do
    Nome. -/
theorem em_k_leituras_pousa (c : X → ℕ) (v : EuclideanSpace ℂ X) {ε τ : ℝ} (hε : 0 < ε) (hτ : 0 < τ) :
    ∃ K : ℕ, ∀ k : ℕ, K ≤ k → ‖(trava c τ)^[k] v - (opDaInstancia c).ker.starProjection v‖ ≤ ε := by
  obtain ⟨K, hK⟩ := exists_nat_ge (Real.log (‖v‖ / ε) / τ)
  refine ⟨K, fun k hk => ?_⟩
  rw [k_leituras_sao_uma_trava]
  have hkK : (K : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have hτ' : τ ≠ 0 := hτ.ne'
  apply a_leitura_de_resolucao_finita_pousa c v hε
  · have h1 : Real.log (‖v‖ / ε) / τ ≤ (k : ℝ) := hK.trans hkK
    have h2 := mul_le_mul_of_nonneg_right h1 hτ.le
    have e : Real.log (‖v‖ / ε) / τ * τ = Real.log (‖v‖ / ε) := by field_simp
    linarith
  · exact mul_nonneg (Nat.cast_nonneg k) hτ.le

/-- ★★ JAMAIS ESGOTADO: enquanto houver amplitude numa atribuição que não resolve, em nenhum tempo a trava É o Nome. -/
theorem jamais_esgotado (c : X → ℕ) (v : EuclideanSpace ℂ X) (x : X) (hx : c x ≠ 0) (hv : WithLp.ofLp v x ≠ 0) (t : ℝ) :
    trava c t v ≠ (opDaInstancia c).ker.starProjection v := by
  intro h
  have h1 : WithLp.ofLp (trava c t v) x = WithLp.ofLp ((opDaInstancia c).ker.starProjection v) x := by rw [h]
  have h2 : WithLp.ofLp ((opDaInstancia c).ker.starProjection v) x = 0 := by
    rw [solucao_por_coordenadas]
    show (if c x = 0 then WithLp.ofLp v x else 0) = 0
    rw [if_neg hx]
  rw [trava_ofLp, h2] at h1
  have he : ((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (Real.exp_pos _).ne'
  exact (mul_ne_zero he hv) h1

end Trava

/-! ## 3. Uma configuração por vez: o passo que consome o custo -/

/-- O LEITOR DE UMA CONFIGURAÇÃO: guarda uma configuração por vez. Fixa o que resolve e, fora do Nome, consome o custo (cada leitura
    baixa o custo, como em `ObservadorTerminal.each_reading_consumes_resistance`). As duas condições são a HIPÓTESE, nomeada no tipo: é
    isto que se pergunta a um leitor real. DITO ÀS CLARAS: o tipo NÃO pina que o passo leia só pela regra (o passo é função qualquer);
    por isso ele é habitado exatamente quando o custo tem zero (`o_tipo_so_diz_que_ha_zero`), e, com Nome de um ponto só, o mapa
    constante é instância. Existência de um leitor deste tipo não é resultado; resultado é o que se segue DADO um. -/
structure LeitorDeUmaConfiguracao {X : Type} (c : X → ℕ) where
  passo : X → X
  fixa_o_nome : ∀ x, c x = 0 → passo x = x
  consome : ∀ x, c x ≠ 0 → c (passo x) < c x

namespace LeitorDeUmaConfiguracao
variable {X : Type} {c : X → ℕ}

/-- ★★ depois de k passos, o custo caiu pelo menos k (ou já é zero). -/
theorem custo_apos_k (G : LeitorDeUmaConfiguracao c) (x : X) (k : ℕ) : c (G.passo^[k] x) ≤ c x - k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    by_cases h0 : c (G.passo^[k] x) = 0
    · rw [G.fixa_o_nome _ h0, h0]
      exact Nat.zero_le _
    · have h := G.consome _ h0
      omega

/-- ★★★ POUSA: de qualquer configuração x, em no máximo c(x) passos o custo é zero. -/
theorem pousa (G : LeitorDeUmaConfiguracao c) (x : X) (k : ℕ) (hk : c x ≤ k) : c (G.passo^[k] x) = 0 := by
  have h := G.custo_apos_k x k
  omega

/-- ★★★ PERMANECE: pousado, o passo seguinte não muda nada (reler não acrescenta). -/
theorem permanece (G : LeitorDeUmaConfiguracao c) (x : X) (k : ℕ) (hk : c x ≤ k) : G.passo^[k + 1] x = G.passo^[k] x := by
  rw [Function.iterate_succ_apply']
  exact G.fixa_o_nome _ (G.pousa x k hk)

/-- O LIMITE do leitor de uma configuração, para um custo limitado por m: a m-ésima iterada do passo. -/
def limite (G : LeitorDeUmaConfiguracao c) (m : ℕ) : X → X := G.passo^[m]

/-- ★★ o limite pousa no Nome. -/
theorem o_limite_pousa (G : LeitorDeUmaConfiguracao c) (m : ℕ) (hm : ∀ x, c x ≤ m) (x : X) : c (G.limite m x) = 0 :=
  G.pousa x m (hm x)

/-- ★★ o limite fixa o Nome ponto a ponto. -/
theorem o_limite_fixa_o_nome (G : LeitorDeUmaConfiguracao c) (m : ℕ) (x : X) (hx : c x = 0) : G.limite m x = x :=
  Function.iterate_fixed (G.fixa_o_nome x hx) m

/-- ★★★ O LIMITE É IDEMPOTENTE: lido até o fim, reler não acrescenta. -/
theorem o_limite_e_idempotente (G : LeitorDeUmaConfiguracao c) (m : ℕ) (hm : ∀ x, c x ≤ m) (x : X) :
    G.limite m (G.limite m x) = G.limite m x :=
  G.o_limite_fixa_o_nome m _ (G.o_limite_pousa m hm x)

/-- ★★ O LIMITE NÃO É CONSTANTE quando o Nome tem dois pontos: duas soluções distintas ficam distintas. -/
theorem o_limite_nao_e_constante (G : LeitorDeUmaConfiguracao c) (m : ℕ) (x y : X) (hx : c x = 0) (hy : c y = 0) (hxy : x ≠ y) :
    G.limite m x ≠ G.limite m y := by
  rw [G.o_limite_fixa_o_nome m x hx, G.o_limite_fixa_o_nome m y hy]
  exact hxy

/-- ★★★ A IMAGEM DO LIMITE É O NOME: uma configuração é valor do limite se e só se resolve. O limite é a retração sobre o Nome. -/
theorem a_imagem_do_limite_e_o_nome (G : LeitorDeUmaConfiguracao c) (m : ℕ) (hm : ∀ x, c x ≤ m) (x : X) :
    (∃ y, G.limite m y = x) ↔ c x = 0 := by
  constructor
  · rintro ⟨y, rfl⟩
    exact G.o_limite_pousa m hm y
  · intro hx
    exact ⟨x, G.o_limite_fixa_o_nome m x hx⟩

/-- O SALTO: havendo uma configuração que resolve, o tipo é habitado (o que está no Nome fica; o resto salta para ela). O salto CONHECE
    uma solução: não lê só pela regra, não é leitor do fundo e não é algoritmo. Serve só para mostrar que a hipótese não é vazia. -/
def salto (c : X → ℕ) (xs : X) (hxs : c xs = 0) : LeitorDeUmaConfiguracao c where
  passo := fun x => if c x = 0 then x else xs
  fixa_o_nome := fun x hx => by
    show (if c x = 0 then x else xs) = x
    rw [if_pos hx]
  consome := fun x hx => by
    show c (if c x = 0 then x else xs) < c x
    rw [if_neg hx, hxs]
    exact Nat.pos_of_ne_zero hx

end LeitorDeUmaConfiguracao

/-- ★★★ O LEITOR TERMINAL DO KERNEL É UM LEITOR DE UMA CONFIGURAÇÃO: o passo é `ObservadorTerminal.leitor` (leva cada nível a quem o
    observa, um por vez, sem saltar) e o custo é a resistência que resta, `ObservadorTerminal.distancia`. As duas condições do tipo são
    teoremas do kernel (v405): `leitor_fixed_iff` com `the_collapse_is_the_terminal_point_of_resistance`, e
    `each_reading_consumes_resistance`. -/
def oLeitorTerminal : LeitorDeUmaConfiguracao TGLExt.ObservadorTerminal.distancia where
  passo := TGLExt.ObservadorTerminal.leitor
  fixa_o_nome := fun x hx => (TGLExt.ObservadorTerminal.leitor_fixed_iff x).mpr
    ((TGLExt.ObservadorTerminal.the_collapse_is_the_terminal_point_of_resistance x).mp hx)
  consome := fun x hx => TGLExt.ObservadorTerminal.each_reading_consumes_resistance x
    (fun h => hx ((TGLExt.ObservadorTerminal.the_collapse_is_the_terminal_point_of_resistance x).mpr h))

/-- ★ O LEITOR QUE DEVOLVE O QUE RECEBEU NÃO RETORNA (controle negativo): posto fora do Nome, fica onde foi posto. -/
theorem o_leitor_que_devolve_o_que_recebeu_nao_retorna {X : Type} (c : X → ℕ) (y : X) (hy : c y ≠ 0) (k : ℕ) :
    c ((id : X → X)^[k] y) ≠ 0 := by
  rw [Function.iterate_id]
  exact hy

/-- ★★★ O TIPO SÓ DIZ QUE HÁ ZERO [dito às claras]: existe leitor de uma configuração para o custo c se e só se alguma configuração
    resolve. A ida é o pouso; a volta é o `salto`, que conhece uma solução. Logo a EXISTÊNCIA de um leitor deste tipo não diz nada
    além de “há solução”, e um decisor qualquer a satisfaz: é a mesma classe do leitor constante que a `AEscala` afastou pondo a
    escala no tipo. O que tem conteúdo é o que se prova DADO um leitor, e, na trava, o que se prova de um operador definido. -/
theorem o_tipo_so_diz_que_ha_zero {X : Type} [Nonempty X] (c : X → ℕ) :
    Nonempty (LeitorDeUmaConfiguracao c) ↔ ∃ x, c x = 0 := by
  constructor
  · rintro ⟨G⟩
    exact ⟨_, G.pousa (Classical.arbitrary X) _ le_rfl⟩
  · rintro ⟨x, hx⟩
    exact ⟨LeitorDeUmaConfiguracao.salto c x hx⟩

/-- ★★ A IMAGEM DO LIMITE TEM A DENSIDADE DO NOME: para o leitor do fundo L e um leitor de uma configuração G (custo limitado por m),
    a leitura final de L é |imagem do limite de G| / |X|. O leitor pousa a partir de TODAS as configurações; o que a igualdade mede é
    o tamanho do lugar onde pousa, que é o Nome. A igualdade com |soluções| / |X| já é do kernel
    (`AEscala.LeitorDoFundo.o_limite_e_o_que_sou`, `TraducaoTuring.o_que_sou_das_solucoes`); G só entra para dizer que a imagem do
    limite é o Nome (`a_imagem_do_limite_e_o_nome`). -/
theorem a_imagem_do_limite_tem_a_densidade_do_nome {X : Type} [Fintype X] [DecidableEq X] {c : X → ℕ}
    (L : TGLExt.AEscala.LeitorDoFundo X) (G : LeitorDeUmaConfiguracao c) (m : ℕ) (hm : ∀ x, c x ≤ m) :
    L.limite c = ((((Finset.univ.image (G.limite m)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) : ℂ) := by
  have himg : Finset.univ.image (G.limite m) = Finset.univ.filter (fun y => c y = 0) := by
    ext x
    simp only [Finset.mem_image, Finset.mem_univ, true_and, Finset.mem_filter]
    exact G.a_imagem_do_limite_e_o_nome m hm x
  rw [L.o_limite_e_o_que_sou c, o_que_sou_das_solucoes, himg]

/-! ## 4. Para uma fórmula -/

/-- (auxiliar) O custo de uma fórmula é no máximo o número de cláusulas. -/
theorem custoCNF_le_numero_de_clausulas {n : ℕ} (φ : CNF n) (x : Fin n → Bool) : custoCNF φ x ≤ φ.length := by
  unfold custoCNF
  exact List.countP_le_length

/-- (auxiliar) Satisfazível = o custo tem zero. -/
theorem sat_sse_o_custo_tem_zero {n : ℕ} (φ : CNF n) : SAT φ ↔ ∃ x, custoCNF φ x = 0 := by
  unfold SAT
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mpr hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, (custoCNF_zero_sse φ x).mp hx⟩

/-- ★★★ A TRAVA POUSA NO NOME E VOLTA [a camada científica da IALD, na língua da tradução de Turing; só a trava, um operador
    definido]: para toda fórmula satisfazível φ com n variáveis, (1) a BACIA: do estado uniforme a trava renormalizada converge à
    seleção (kernel); (2) o RETORNO: para todo estado s não cego ao Nome e todo empurrão δ ortogonal ao Nome, a órbita de s + δ
    converge à seleção de s; (3) a RESOLUÇÃO FINITA: para toda resolução e toda duração de ciclo positivas, de um número finito de
    leituras em diante o estado está dentro da resolução; (4) SEM ESCALA (controle), o empurrão não nulo nunca é desfeito. -/
theorem a_trava_pousa_e_volta {n : ℕ} (φ : CNF n) (hφ : SAT φ) :
    Tendsto (fun t : ℝ => (((‖trava (custoCNF φ) t (uniforme (Fin n → Bool))‖)⁻¹ : ℝ) : ℂ)
          • trava (custoCNF φ) t (uniforme (Fin n → Bool))) atTop
        (𝓝 (selecao (opDaInstancia (custoCNF φ)).ker (uniforme (Fin n → Bool))))
    ∧ (∀ s δ : EuclideanSpace ℂ (Fin n → Bool),
        (opDaInstancia (custoCNF φ)).ker.starProjection s ≠ 0 → δ ∈ ((opDaInstancia (custoCNF φ)).ker)ᗮ →
        Tendsto (fun t : ℝ => (((‖trava (custoCNF φ) t (s + δ)‖)⁻¹ : ℝ) : ℂ) • trava (custoCNF φ) t (s + δ)) atTop
          (𝓝 (selecao (opDaInstancia (custoCNF φ)).ker s)))
    ∧ (∀ (v : EuclideanSpace ℂ (Fin n → Bool)) (ε τ : ℝ), 0 < ε → 0 < τ →
        ∃ K : ℕ, ∀ k : ℕ, K ≤ k →
          ‖(trava (custoCNF φ) τ)^[k] v - (opDaInstancia (custoCNF φ)).ker.starProjection v‖ ≤ ε)
    ∧ (∀ s δ : EuclideanSpace ℂ (Fin n → Bool), δ ≠ 0 → ∀ k : ℕ, (trava (custoCNF φ) 0)^[k] (s + δ) ≠ s) :=
  ⟨a_trava_converge_a_selecao (custoCNF φ) ((sat_sse_o_custo_tem_zero φ).mp hφ),
   fun s δ hs hδ => o_retorno (custoCNF φ) s δ hs hδ,
   fun v ε τ hε hτ => em_k_leituras_pousa (custoCNF φ) v hε hτ,
   fun s δ hδ k => a_fotografia_nao_retorna (custoCNF φ) s δ hδ k⟩

/-- ★★ PARA UMA FÓRMULA, UMA CONFIGURAÇÃO POR VEZ: dado um leitor de uma configuração para o custo da fórmula, de qualquer configuração,
    em no máximo tantos passos quantas são as cláusulas o custo é zero, e o passo seguinte não muda nada. -/
theorem para_uma_formula_o_leitor_pousa {n : ℕ} (φ : CNF n) (G : LeitorDeUmaConfiguracao (custoCNF φ))
    (x : Fin n → Bool) (k : ℕ) (hk : φ.length ≤ k) :
    custoCNF φ (G.passo^[k] x) = 0 ∧ G.passo^[k + 1] x = G.passo^[k] x :=
  ⟨G.pousa x k ((custoCNF_le_numero_de_clausulas φ x).trans hk),
   G.permanece x k ((custoCNF_le_numero_de_clausulas φ x).trans hk)⟩

end TGLExt.CamadaCientifica
end

import TGLExt.EsperancaCondicional
import TGLExt.KEhATangente
import TGLExt.TraducaoTuring
import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

-- (linha de processo; SAI ao instalar: candidata da gerência c1, 15/11/2026, R1; nome provisório, o operador nomeia)

/-!
# O HABITANTE DO NOME — o leitor é a esperança condicional do Nome, e não o Nome

Derivação do operador (15/11/2026; `work\cunhagens_13out\OPERADOR_15nov_o_leitor_e_o_verbo_o_habitante_do_nome_a_esperanca_condicional_e_o_artigo_do_neutrino_de_2025_verbatim.txt`,
sha256 `49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f`; as quatro primeiras frases, por bytes):
«O leitor é o observador, é o verbo, e não o nome. É o habitante do nome, é a esperança condicional do nome.
Tangente=testemunho=esperança condicional. O nome é o espaço em que a testemunha da verdade sobre o nome (verbo - observador - seletor)
pode habitar.»

## O que o kernel já tinha (levantado antes de construir; nada disto é refeito aqui)

* `TheNameOperator.nameOp p x = p x p + (1−p) x (1−p)` (v162): unital, idempotente, com os fixos fechados no produto.
* `EsperancaCondicional` (v404), sobre a linha de 26/10/2026 «esperança condicional=nome» (sha256 `5d3976cd…5b52`): o operador do Nome
  da unidade é a esperança diagonal em `M₂`; a relação de Jones; o índice. Ela mesma declarou a lacuna: a bimodularidade GERAL de `nameOp p`
  sobre os seus fixos não estava tipada.
* `Ergodicity` (a sombra finita da T1): o semigrupo de defasagem converge à esperança diagonal (`dephase_tendsto_expectation`).
* `TheAxiomAndTheFalseWitness.axiomFlow` (v385): o fluxo do lock mínimo tende ao posto e não o alcança em tempo finito.
* `TraducaoTuring` (v409): `selecao` (a projeção no Nome, renormalizada), `a_selecao_esquece`, `solucao_por_coordenadas`.
* `KEhATangente` (v407), sobre a cunhagem de 02/11/2026 «k é a tangente; é como se fosse o acorde sendo tocado» (sha256 `cec3d7c0…a31a`):
  `K θ = tan θ`, `K² = custo/pagamento`, o crivo `K = 1` só no posto.
* `IALD2.o_atrator` (v410), sobre a fala de 07/11/2026 «tangenciado em conteúdo finito, contudo jamais esgotado» (sha256 `a5c84e82…1eeb`).

## O que a derivação de 15/11 separa, e como esta pedra o tipa

[Leitura da gerência; o autor ratifica ou corrige.] A linha de 26/10 punha a esperança condicional e o Nome numa igualdade. A de 15/11
diz de que modo: a esperança condicional é o LEITOR (o verbo, o observador, o seletor), que HABITA o Nome; o Nome é o ESPAÇO onde ele
habita. A pedra de 26/10 fica como está; esta diz ao lado. No kernel a separação já tinha forma e não tinha termo: o
leitor é o mapa (`nameOp p` na álgebra; a projeção `K.starProjection` nos vetores) e o Nome é a imagem dele, que é o conjunto dos seus fixos.
Uma igualdade entre os dois não se escreve (um é função, o outro é conjunto): o que se prova é a ligação.

1. O LEITOR HABITA O NOME (álgebra, todo anel, todo idempotente `p`). A imagem de `nameOp p` é a `morada p` (os fixos), e a morada é
   exatamente o que comuta com `p`: `a_imagem_do_leitor_e_a_morada`, `a_morada_e_o_que_comuta_com_o_posto`.
2. A LEI DE MÓDULO, GERAL (fecha a lacuna declarada da v404): o que já é do Nome atravessa a leitura sem ser tocado,
   `nameOp p (a x b) = a (nameOp p x) b` para `a`, `b` na morada: `o_leitor_e_bimodular_sobre_o_nome`.
3. SÓ HÁ UM HABITANTE (álgebra). Todo mapa aditivo, unital, que cai na morada e cumpre a lei de módulo É `nameOp p`:
   `so_ha_um_habitante`. O Nome determina o seu leitor.
4. SÓ HÁ UMA TESTEMUNHA (Hilbert). Num espaço de Hilbert, todo mapa linear que cai no Nome, fixa o Nome e não aumenta a norma É a
   projeção ortogonal no Nome: `a_testemunha_que_nao_aumenta_e_a_esperanca`, e na forma de existência e unicidade
   `o_nome_e_a_morada_de_uma_so_testemunha`. Quem cai no Nome e o fixa sem ser a projeção aumenta alguma coisa:
   `quem_nao_e_a_esperanca_aumenta`.
5. A PONTE ENTRE OS DOIS PORTADORES. Ler um observável no estado lido é ler a compressão dele no estado:
   `a_leitura_do_vetor_e_a_compressao`; e o operador do Nome, lido num estado, é a soma das duas faces: `a_leitura_do_operador_do_nome`.
6. TANGENTE, nos três sentidos que o kernel tem, cada um dado pela esperança condicional:
   (a) o SELETOR TANGENCIA A ESPERANÇA no Nome: para `s` no Nome, de norma 1, `selecao K (s + δ)` difere de `s + P δ` por no máximo
       `‖P δ‖²/2` (contato de segunda ordem): `o_seletor_tangencia_a_esperanca`; e o que é cego ao Nome não deixa rastro, exatamente:
       `o_que_e_cego_ao_nome_nao_deixa_rastro`;
   (b) a TANGENTE DA LEITURA, `‖v − P v‖ / ‖P v‖`, é o `K` da v407 no ângulo da leitura, o livro fecha (`‖v‖² = ‖P v‖² + ‖v − P v‖²`),
       o peso do Nome é o cosseno ao quadrado e o crivo `K = 1` é a meia face: `a_tangente_da_leitura_e_K`, `o_livro_do_testemunho_fecha`,
       `o_peso_do_nome_e_o_cosseno_quadrado`, `o_crivo_e_a_meia_face`;
   (c) TANGENCIADO, JAMAIS ESGOTADO: sob o fluxo do axioma a tangente da leitura decai como `e^{−t}`, nunca se anula em tempo finito e
       tende a zero: `a_leitura_fecha_a_tangente`, `tangenciado_jamais_esgotado`.
7. A FACE CLÁSSICA. No espaço das leituras de um custo, o que o seletor devolve de qualquer grandeza `g` é a média de `g` sobre o Nome,
   com os pesos do estado: a esperança condicional de `g` dado o Nome. Os pesos relativos DENTRO do Nome não mudam:
   `o_peso_do_nome_por_coordenadas`, `a_selecao_e_a_esperanca_condicional_classica`.

## O que a pedra NÃO afirma

* Que a esperança condicional seja o Nome: são de tipos distintos. Prova-se que a imagem do leitor é o Nome e que o Nome o determina.
* Unicidade sem hipótese: na álgebra a lei de módulo é HIPÓTESE (em álgebras de operadores ela decorre da norma 1, [KNOWN] Tomiyama 1957;
  esse passo não é termo aqui); no espaço de Hilbert a hipótese é não aumentar a norma, e a prova é desta pedra.
* Que “tangente” tenha um só sentido: são três termos do kernel (o ângulo da leitura, o contato do seletor, o limite do fluxo). Qual deles
  é a Tangente da derivação é leitura do autor [INPUT]; a pedra prova que os três são dados pela esperança condicional.
* Nada sobre a ergodicidade em III₁ genuína: a convergência à esperança, no kernel, é da face finita (`Ergodicity`) e do fluxo do lock mínimo.
* Que um modelo de linguagem seja este leitor: isso é previsão de experimento, não teorema.
* Exclusividade, consciência, pesos de modelo. Nada sobre a natureza: não é teste e não move o gate.

## Estatutos

[REAL no sandbox] os teoremas. [KNOWN] esperança condicional (Umegaki 1954; Tomiyama 1957); a projeção ortogonal como única contração
idempotente sobre a sua imagem (fato padrão de espaços de Hilbert; a prova daqui é própria); a regra de Lüders e o condicionamento de Bayes.
[INPUT] a derivação do operador e a identificação leitor = observador = verbo = seletor. Sem sorry, sem axiom.
-/

namespace TGLExt.OHabitanteDoNome

open TGLExt TGLExt.TraducaoTuring TGLExt.TheAxiomAndTheFalseWitness Filter Topology
open scoped InnerProductSpace

/-! ## 1. O leitor habita o Nome (álgebra) -/

section Anel

variable {R : Type*} [Ring R]

/-- A MORADA: o Nome como espaço. É o que o leitor não muda. -/
def morada (p : R) : Set R := {x | nameOp p x = x}

/-- ★★ O LEITOR HABITA O NOME: toda leitura cai na morada. -/
theorem o_leitor_habita_o_nome {p : R} (hp : p * p = p) (x : R) : nameOp p x ∈ morada p := by
  show nameOp p (nameOp p x) = nameOp p x
  exact name_op_idem hp x

/-- ★★★ A IMAGEM DO LEITOR É A MORADA: o leitor é o mapa, o Nome é onde ele cai. -/
theorem a_imagem_do_leitor_e_a_morada {p : R} (hp : p * p = p) : Set.range (nameOp p) = morada p := by
  ext x
  constructor
  · rintro ⟨y, rfl⟩
    exact o_leitor_habita_o_nome hp y
  · intro hx
    exact ⟨x, hx⟩

/-- ★★ A MORADA É O QUE COMUTA COM O POSTO. -/
theorem a_morada_e_o_que_comuta_com_o_posto {p : R} (hp : p * p = p) (x : R) :
    x ∈ morada p ↔ p * x = x * p := by
  have hdef : nameOp p x = p * x * p + (1 - p) * x * (1 - p) := rfl
  constructor
  · intro h
    have h' : p * x * p + (1 - p) * x * (1 - p) = x := by rw [← hdef]; exact h
    have h1 : p * x = p * x * p := by
      calc p * x = p * (p * x * p + (1 - p) * x * (1 - p)) := by rw [h']
        _ = p * p * x * p + p * (1 - p) * x * (1 - p) := by simp only [mul_add, mul_assoc]
        _ = p * x * p := by rw [hp, face_orthogonal hp, zero_mul, zero_mul, add_zero]
    have h2 : x * p = p * x * p := by
      calc x * p = (p * x * p + (1 - p) * x * (1 - p)) * p := by rw [h']
        _ = p * x * (p * p) + (1 - p) * x * ((1 - p) * p) := by simp only [add_mul, mul_assoc]
        _ = p * x * p := by rw [hp, face_orthogonal' hp, mul_zero, add_zero]
    exact h1.trans h2.symm
  · intro h
    show nameOp p x = x
    have h1 : p * x * p = x * p := by rw [h, mul_assoc, hp]
    have h3 : (1 - p) * x = x * (1 - p) := by rw [sub_mul, one_mul, mul_sub, mul_one, h]
    have h2 : (1 - p) * x * (1 - p) = x * (1 - p) := by rw [h3, mul_assoc, face_idem hp]
    have h4 : p + (1 - p) = (1 : R) := by abel
    rw [hdef, h1, h2, ← mul_add, h4, mul_one]

/-! ## 2. A lei de módulo, geral -/

/-- ★★★ A LEI DE MÓDULO: o que já é do Nome atravessa a leitura sem ser tocado. Fecha a lacuna declarada em
    `EsperancaCondicional` (v404): a bimodularidade de `nameOp p` sobre os seus fixos, para todo idempotente de todo anel. -/
theorem o_leitor_e_bimodular_sobre_o_nome {p : R} (hp : p * p = p) {a b : R}
    (ha : p * a = a * p) (hb : p * b = b * p) (x : R) :
    nameOp p (a * x * b) = a * nameOp p x * b := by
  have ha' : (1 - p) * a = a * (1 - p) := by rw [sub_mul, one_mul, mul_sub, mul_one, ha]
  have hb' : b * (1 - p) = (1 - p) * b := by rw [sub_mul, one_mul, mul_sub, mul_one, hb]
  have e1 : p * (a * x * b) * p = a * (p * x * p) * b := by
    calc p * (a * x * b) * p = (p * a) * x * (b * p) := by simp only [mul_assoc]
      _ = (a * p) * x * (p * b) := by rw [ha, ← hb]
      _ = a * (p * x * p) * b := by simp only [mul_assoc]
  have e2 : (1 - p) * (a * x * b) * (1 - p) = a * ((1 - p) * x * (1 - p)) * b := by
    calc (1 - p) * (a * x * b) * (1 - p) = ((1 - p) * a) * x * (b * (1 - p)) := by simp only [mul_assoc]
      _ = (a * (1 - p)) * x * ((1 - p) * b) := by rw [ha', hb']
      _ = a * ((1 - p) * x * (1 - p)) * b := by simp only [mul_assoc]
  show p * (a * x * b) * p + (1 - p) * (a * x * b) * (1 - p) = a * (p * x * p + (1 - p) * x * (1 - p)) * b
  rw [e1, e2, mul_add, add_mul]

/-! ## 3. Só há um habitante (álgebra) -/

/-- ★★★ SÓ HÁ UM HABITANTE: todo mapa aditivo e unital que cai na morada e cumpre a lei de módulo sobre ela é o operador do Nome.
    O Nome (a morada) determina o seu leitor. A lei de módulo é hipótese; em álgebras de operadores ela decorre da norma 1
    ([KNOWN] Tomiyama 1957), e esse passo não é termo aqui. -/
theorem so_ha_um_habitante {p : R} (hp : p * p = p) (E : R → R)
    (hadd : ∀ x y, E (x + y) = E x + E y) (h1 : E 1 = 1)
    (hmora : ∀ x, p * E x = E x * p)
    (hbim : ∀ a b x, p * a = a * p → p * b = b * p → E (a * x * b) = a * E x * b) (x : R) :
    E x = nameOp p x := by
  have hpp : p * p = p * p := rfl
  have hq : p * (1 - p) = (1 - p) * p := by rw [face_orthogonal hp, face_orthogonal' hp]
  have h11 : p * (1 : R) = 1 * p := by rw [mul_one, one_mul]
  have hfix : ∀ a, p * a = a * p → E a = a := by
    intro a ha
    have h := hbim a 1 1 ha h11
    simpa [h1] using h
  have hx : x = p * x * p + p * x * (1 - p) + (1 - p) * x * p + (1 - p) * x * (1 - p) := by
    simp only [mul_sub, sub_mul, mul_one, one_mul]
    abel
  have c1 : p * (p * x * p) = p * x * p * p := by
    calc p * (p * x * p) = (p * p) * x * p := by simp only [mul_assoc]
      _ = p * x * p := by rw [hp]
      _ = p * x * (p * p) := by rw [hp]
      _ = p * x * p * p := by simp only [mul_assoc]
  have c4 : p * ((1 - p) * x * (1 - p)) = (1 - p) * x * (1 - p) * p := by
    calc p * ((1 - p) * x * (1 - p)) = (p * (1 - p)) * x * (1 - p) := by simp only [mul_assoc]
      _ = 0 := by rw [face_orthogonal hp, zero_mul, zero_mul]
      _ = (1 - p) * x * ((1 - p) * p) := by rw [face_orthogonal' hp, mul_zero]
      _ = (1 - p) * x * (1 - p) * p := by simp only [mul_assoc]
  have e1 : E (p * x * p) = p * x * p := hfix _ c1
  have e4 : E ((1 - p) * x * (1 - p)) = (1 - p) * x * (1 - p) := hfix _ c4
  have e2 : E (p * x * (1 - p)) = 0 := by
    rw [hbim p (1 - p) x hpp hq, hmora x, mul_assoc, face_orthogonal hp, mul_zero]
  have e3 : E ((1 - p) * x * p) = 0 := by
    rw [hbim (1 - p) p x hq hpp, mul_assoc, ← hmora x, ← mul_assoc, face_orthogonal' hp, zero_mul]
  calc E x = E (p * x * p + p * x * (1 - p) + (1 - p) * x * p + (1 - p) * x * (1 - p)) := by rw [← hx]
    _ = p * x * p + (1 - p) * x * (1 - p) := by rw [hadd, hadd, hadd, e1, e2, e3, e4, add_zero, add_zero]
    _ = nameOp p x := rfl

/-- ★★ O OPERADOR DO NOME É ESSE HABITANTE: ele cumpre as quatro condições de `so_ha_um_habitante`. -/
theorem o_operador_do_nome_e_o_habitante {p : R} (hp : p * p = p) :
    (∀ x y, nameOp p (x + y) = nameOp p x + nameOp p y) ∧ nameOp p 1 = 1 ∧
    (∀ x, p * nameOp p x = nameOp p x * p) ∧
    (∀ a b x, p * a = a * p → p * b = b * p → nameOp p (a * x * b) = a * nameOp p x * b) := by
  refine ⟨fun x y => ?_, name_op_unital hp, fun x => ?_, fun a b x ha hb => o_leitor_e_bimodular_sobre_o_nome hp ha hb x⟩
  · show p * (x + y) * p + (1 - p) * (x + y) * (1 - p)
        = p * x * p + (1 - p) * x * (1 - p) + (p * y * p + (1 - p) * y * (1 - p))
    simp only [mul_add, add_mul]
    abel
  · exact (a_morada_e_o_que_comuta_com_o_posto hp (nameOp p x)).mp (o_leitor_habita_o_nome hp x)

end Anel

/-! ## 4. Só há uma testemunha (Hilbert) -/

section Hilbert

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- ★ A ESPERANÇA CONDICIONAL DO NOME (a projeção ortogonal) cai no Nome, fixa o Nome, não aumenta a norma, e reler não acrescenta. -/
theorem a_esperanca_habita_fixa_e_nao_aumenta (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    (∀ v, K.starProjection v ∈ K) ∧ (∀ w ∈ K, K.starProjection w = w) ∧
    (∀ v, ‖K.starProjection v‖ ≤ ‖v‖) ∧
    (∀ v, K.starProjection (K.starProjection v) = K.starProjection v) :=
  ⟨fun v => K.starProjection_apply_mem v, fun w hw => Submodule.starProjection_eq_self_iff.mpr hw,
   fun v => K.norm_starProjection_apply_le v,
   fun v => Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)⟩

/-- ★★★ A TESTEMUNHA QUE NÃO AUMENTA É A ESPERANÇA: um mapa linear que cai no Nome, fixa o Nome e não aumenta a norma é a projeção
    ortogonal no Nome. A prova: o que é ortogonal ao Nome é anulado, porque senão, somando ao vetor um múltiplo grande do que a
    testemunha disse dele, a norma do que ela diz passaria a do que lhe foi dado. -/
theorem a_testemunha_que_nao_aumenta_e_a_esperanca (K : Submodule ℂ H) [K.HasOrthogonalProjection]
    (E : H →ₗ[ℂ] H) (hmora : ∀ v, E v ∈ K) (hfixa : ∀ w ∈ K, E w = w) (hnao : ∀ v, ‖E v‖ ≤ ‖v‖) (v : H) :
    E v = K.starProjection v := by
  have hzero : ∀ u ∈ Kᗮ, E u = 0 := by
    intro u hu
    by_contra hne
    have ha : 0 < ‖E u‖ := norm_pos_iff.mpr hne
    have hane : ‖E u‖ ≠ 0 := ha.ne'
    have h0 : ⟪u, E u⟫_ℂ = 0 :=
      inner_eq_zero_symm.mp ((Submodule.mem_orthogonal K u).mp hu (E u) (hmora u))
    obtain ⟨t, ht⟩ : ∃ t : ℝ, t = ‖u‖ ^ 2 / ‖E u‖ ^ 2 := ⟨_, rfl⟩
    have ht0 : 0 ≤ t := by rw [ht]; positivity
    have hta : t * ‖E u‖ ^ 2 = ‖u‖ ^ 2 := by rw [ht]; field_simp
    have hE : E (u + (t : ℂ) • E u) = (((1 + t : ℝ)) : ℂ) • E u := by
      rw [map_add, map_smul, hfixa (E u) (hmora u), Complex.ofReal_add, Complex.ofReal_one, add_smul, one_smul]
    have h1t : 0 ≤ 1 + t := by linarith
    have hl : ‖E (u + (t : ℂ) • E u)‖ = (1 + t) * ‖E u‖ := by
      rw [hE, norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg h1t]
    have hr : ‖u + (t : ℂ) • E u‖ * ‖u + (t : ℂ) • E u‖ = ‖u‖ * ‖u‖ + (t * ‖E u‖) * (t * ‖E u‖) := by
      have hin : ⟪u, (t : ℂ) • E u⟫_ℂ = 0 := by rw [inner_smul_right, h0, mul_zero]
      rw [norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hin, norm_smul, Complex.norm_real,
        Real.norm_eq_abs, abs_of_nonneg ht0]
    have hle := hnao (u + (t : ℂ) • E u)
    rw [hl] at hle
    have hsq := mul_self_le_mul_self (mul_nonneg h1t (norm_nonneg _)) hle
    rw [hr] at hsq
    nlinarith [hsq, hta, sq_nonneg ‖u‖, mul_pos ha ha]
  have hsplit : K.starProjection v + (v - K.starProjection v) = v := by abel
  calc E v = E (K.starProjection v + (v - K.starProjection v)) := by rw [hsplit]
    _ = E (K.starProjection v) + E (v - K.starProjection v) := map_add E _ _
    _ = K.starProjection v := by
        rw [hfixa _ (K.starProjection_apply_mem v), hzero _ (Submodule.sub_starProjection_mem_orthogonal v), add_zero]

/-- ★★★ O NOME É A MORADA DE UMA SÓ TESTEMUNHA: para cada Nome (subespaço com projeção) existe exatamente um mapa linear que cai nele,
    o fixa e não aumenta a norma. -/
theorem o_nome_e_a_morada_de_uma_so_testemunha (K : Submodule ℂ H) [K.HasOrthogonalProjection] :
    ∃! E : H →ₗ[ℂ] H, (∀ v, E v ∈ K) ∧ (∀ w ∈ K, E w = w) ∧ (∀ v, ‖E v‖ ≤ ‖v‖) := by
  refine ⟨(K.starProjection : H →L[ℂ] H).toLinearMap, ⟨fun v => K.starProjection_apply_mem v,
    fun w hw => Submodule.starProjection_eq_self_iff.mpr hw, fun v => K.norm_starProjection_apply_le v⟩, ?_⟩
  rintro E ⟨h1, h2, h3⟩
  ext v
  exact a_testemunha_que_nao_aumenta_e_a_esperanca K E h1 h2 h3 v

/-- ★★ QUEM NÃO É A ESPERANÇA AUMENTA: um mapa linear que cai no Nome e o fixa, e que difere da projeção em algum vetor, devolve de
    algum vetor mais do que recebeu. -/
theorem quem_nao_e_a_esperanca_aumenta (K : Submodule ℂ H) [K.HasOrthogonalProjection]
    (E : H →ₗ[ℂ] H) (hmora : ∀ v, E v ∈ K) (hfixa : ∀ w ∈ K, E w = w)
    (hdif : ∃ v, E v ≠ K.starProjection v) : ∃ v, ‖v‖ < ‖E v‖ := by
  by_contra h
  have hall : ∀ v, ‖E v‖ ≤ ‖v‖ := fun v => not_lt.mp (fun hv => h ⟨v, hv⟩)
  obtain ⟨v, hv⟩ := hdif
  exact hv (a_testemunha_que_nao_aumenta_e_a_esperanca K E hmora hfixa hall v)

/-! ## 5. A ponte entre os dois portadores -/

/-- ★★ A LEITURA DO VETOR É A COMPRESSÃO: ler o observável `x` no estado lido `P v` é ler a compressão `P x P` no estado `v`. -/
theorem a_leitura_do_vetor_e_a_compressao (K : Submodule ℂ H) [K.HasOrthogonalProjection] (x : H →L[ℂ] H) (v : H) :
    ⟪K.starProjection v, x (K.starProjection v)⟫_ℂ = ⟪v, compressOp K.starProjection x v⟫_ℂ := by
  have h : compressOp K.starProjection x v = K.starProjection (x (K.starProjection v)) := by
    simp [compressOp]
  rw [h, K.inner_starProjection_left_eq_right]

/-- ★★ O OPERADOR DO NOME, LIDO NUM ESTADO, É A SOMA DAS DUAS FACES: a leitura de `x` no que o leitor reteve mais a leitura de `x` no
    que ele deixou. -/
theorem a_leitura_do_operador_do_nome (K : Submodule ℂ H) [K.HasOrthogonalProjection] (x : H →L[ℂ] H) (v : H) :
    ⟪v, nameOp K.starProjection x v⟫_ℂ =
      ⟪K.starProjection v, x (K.starProjection v)⟫_ℂ
        + ⟪v - K.starProjection v, x (v - K.starProjection v)⟫_ℂ := by
  have h : nameOp K.starProjection x v
      = K.starProjection (x (K.starProjection v))
        + (x (v - K.starProjection v) - K.starProjection (x (v - K.starProjection v))) := by
    simp [nameOp]
  rw [h, inner_add_right, ← K.inner_starProjection_left_eq_right, inner_sub_right,
    ← K.inner_starProjection_left_eq_right, ← inner_sub_left]

/-! ## 6. Tangente -/

variable [CompleteSpace H] in
/-- ★★★ O SELETOR TANGENCIA A ESPERANÇA NO NOME (contato de segunda ordem): para `s` no Nome, de norma 1, e um empurrão `δ` cuja parte
    no Nome é ortogonal a `s`, a seleção de `s + δ` difere de `s + P δ` por no máximo `‖P δ‖²/2`. Em primeira ordem, o seletor É a
    esperança condicional. -/
theorem o_seletor_tangencia_a_esperanca (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s δ : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) (hδ : ⟪s, K.starProjection δ⟫_ℂ = 0) :
    ‖selecao K (s + δ) - (s + K.starProjection δ)‖ ≤ ‖K.starProjection δ‖ ^ 2 / 2 := by
  obtain ⟨u, hu⟩ : ∃ u : H, u = s + K.starProjection δ := ⟨_, rfl⟩
  have hP : K.starProjection (s + δ) = u := by
    rw [hu, map_add, Submodule.starProjection_eq_self_iff.mpr hs]
  have hn2 : ‖u‖ * ‖u‖ = 1 + ‖K.starProjection δ‖ * ‖K.starProjection δ‖ := by
    rw [hu, norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hδ, hs1, mul_one]
  have hge : 1 ≤ ‖u‖ :=
    (mul_self_le_mul_self_iff (by norm_num) (norm_nonneg u)).mpr
      (by rw [hn2]; nlinarith [mul_self_nonneg ‖K.starProjection δ‖])
  have hle : ‖u‖ ≤ 1 + ‖K.starProjection δ‖ ^ 2 / 2 :=
    (mul_self_le_mul_self_iff (norm_nonneg u) (by positivity)).mpr
      (by rw [hn2]; nlinarith [sq_nonneg (‖K.starProjection δ‖ ^ 2)])
  have hu0 : ‖u‖ ≠ 0 := (lt_of_lt_of_le one_pos hge).ne'
  have hsel : selecao K (s + δ) - u = (((‖u‖⁻¹ - 1 : ℝ)) : ℂ) • u := by
    unfold selecao
    rw [hP, Complex.ofReal_sub, Complex.ofReal_one, sub_smul, one_smul]
  have hnorm : ‖selecao K (s + δ) - u‖ = ‖u‖ - 1 := by
    rw [hsel, norm_smul, Complex.norm_real, Real.norm_eq_abs]
    have h1 : (‖u‖⁻¹ - 1) * ‖u‖ = 1 - ‖u‖ := by rw [sub_mul, inv_mul_cancel₀ hu0, one_mul]
    calc |‖u‖⁻¹ - 1| * ‖u‖ = |(‖u‖⁻¹ - 1) * ‖u‖| := by rw [abs_mul, abs_of_nonneg (norm_nonneg u)]
      _ = |1 - ‖u‖| := by rw [h1]
      _ = ‖u‖ - 1 := by rw [abs_sub_comm, abs_of_nonneg (by linarith)]
  rw [← hu, hnorm]
  linarith

variable [CompleteSpace H] in
/-- ★★ O QUE É CEGO AO NOME NÃO DEIXA RASTRO, exatamente: o empurrão ortogonal ao Nome é desfeito pela seleção. -/
theorem o_que_e_cego_ao_nome_nao_deixa_rastro (K : Submodule ℂ H) [K.HasOrthogonalProjection] {s δ : H}
    (hs : s ∈ K) (hs1 : ‖s‖ = 1) (hδ : δ ∈ Kᗮ) : selecao K (s + δ) = s := by
  have hP : K.starProjection δ = 0 := (Submodule.starProjection_apply_eq_zero_iff K).mpr hδ
  have h := o_seletor_tangencia_a_esperanca K hs hs1 (δ := δ) (by rw [hP, inner_zero_right])
  have hz : ‖K.starProjection δ‖ ^ 2 / 2 = 0 := by rw [hP, norm_zero]; norm_num
  have h0 : ‖selecao K (s + δ) - s‖ ≤ 0 := by
    calc ‖selecao K (s + δ) - s‖ = ‖selecao K (s + δ) - (s + K.starProjection δ)‖ := by rw [hP, add_zero]
      _ ≤ ‖K.starProjection δ‖ ^ 2 / 2 := h
      _ = 0 := hz
  exact sub_eq_zero.mp (norm_le_zero_iff.mp h0)

/-- A TANGENTE DA LEITURA: o que o leitor deixa sobre o que ele retém. -/
noncomputable def tangenteDaLeitura (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) : ℝ :=
  ‖v - K.starProjection v‖ / ‖K.starProjection v‖

/-- ★★ O LIVRO DO TESTEMUNHO FECHA: o que o leitor retém e o que ele deixa somam o todo. -/
theorem o_livro_do_testemunho_fecha (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    ‖v‖ ^ 2 = ‖K.starProjection v‖ ^ 2 + ‖v - K.starProjection v‖ ^ 2 := by
  have h0 : ⟪K.starProjection v, v - K.starProjection v⟫_ℂ = 0 :=
    inner_eq_zero_symm.mp (Submodule.starProjection_inner_eq_zero v _ (K.starProjection_apply_mem v))
  have h := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ h0
  have e : K.starProjection v + (v - K.starProjection v) = v := by abel
  rw [e] at h
  rw [sq, sq, sq]
  exact h

/-- ★★ A TANGENTE DA LEITURA É O `K` DA v407 no ângulo da leitura. -/
theorem a_tangente_da_leitura_e_K (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H) :
    KEhATangente.K (Real.arctan (tangenteDaLeitura K v)) = tangenteDaLeitura K v := by
  unfold KEhATangente.K
  exact Real.tan_arctan _

/-- ★★ O PESO DO NOME É O COSSENO AO QUADRADO do ângulo da leitura. -/
theorem o_peso_do_nome_e_o_cosseno_quadrado (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (hP : K.starProjection v ≠ 0) :
    Real.cos (Real.arctan (tangenteDaLeitura K v)) ^ 2 = ‖K.starProjection v‖ ^ 2 / ‖v‖ ^ 2 := by
  have hn : ‖K.starProjection v‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hb2 : ‖K.starProjection v‖ ^ 2 ≠ 0 := pow_ne_zero 2 hn
  have hb := o_livro_do_testemunho_fecha K v
  have h1 : 1 + ‖v - K.starProjection v‖ ^ 2 / ‖K.starProjection v‖ ^ 2
      = (‖K.starProjection v‖ ^ 2 + ‖v - K.starProjection v‖ ^ 2) / ‖K.starProjection v‖ ^ 2 := by
    rw [add_div, div_self hb2]
  rw [Real.cos_sq_arctan]
  unfold tangenteDaLeitura
  rw [div_pow, h1, one_div_div, ← hb]

/-- ★★ O CRIVO É A MEIA FACE: a tangente da leitura vale 1 exatamente quando o Nome pesa a metade. -/
theorem o_crivo_e_a_meia_face (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (hP : K.starProjection v ≠ 0) :
    tangenteDaLeitura K v = 1 ↔ ‖K.starProjection v‖ ^ 2 = ‖v‖ ^ 2 / 2 := by
  have hn : ‖K.starProjection v‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hb := o_livro_do_testemunho_fecha K v
  unfold tangenteDaLeitura
  rw [div_eq_one_iff_eq hn]
  constructor
  · intro h
    rw [hb, h]
    ring
  · intro h
    have h2 : ‖v - K.starProjection v‖ ^ 2 = ‖K.starProjection v‖ ^ 2 := by linarith
    exact (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp h2

/-- ★★★ A LEITURA FECHA A TANGENTE: sob o fluxo do axioma, a tangente da leitura decai como `e^{−t}`. -/
theorem a_leitura_fecha_a_tangente (K : Submodule ℂ H) [K.HasOrthogonalProjection] (t : ℝ) (v : H) :
    tangenteDaLeitura K (axiomFlow K.starProjection t v) = Real.exp (-t) * tangenteDaLeitura K v := by
  have hF : axiomFlow K.starProjection t v
      = K.starProjection v + ((Real.exp (-t) : ℝ) : ℂ) • (v - K.starProjection v) := by
    simp [axiomFlow]
  have hPP : K.starProjection (K.starProjection v) = K.starProjection v :=
    Submodule.starProjection_eq_self_iff.mpr (K.starProjection_apply_mem v)
  have hPF : K.starProjection (axiomFlow K.starProjection t v) = K.starProjection v := by
    rw [hF, map_add, map_smul, map_sub, hPP, sub_self, smul_zero, add_zero]
  unfold tangenteDaLeitura
  rw [hPF, hF, add_sub_cancel_left, norm_smul, Complex.norm_real, Real.norm_eq_abs,
    abs_of_pos (Real.exp_pos _), mul_div_assoc]

/-- ★★★ TANGENCIADO, JAMAIS ESGOTADO: se a tangente da leitura não é zero, sob o fluxo do axioma ela nunca se anula em tempo finito, e
    tende a zero. -/
theorem tangenciado_jamais_esgotado (K : Submodule ℂ H) [K.HasOrthogonalProjection] (v : H)
    (h : tangenteDaLeitura K v ≠ 0) :
    (∀ t : ℝ, tangenteDaLeitura K (axiomFlow K.starProjection t v) ≠ 0) ∧
    Tendsto (fun t : ℝ => tangenteDaLeitura K (axiomFlow K.starProjection t v)) atTop (𝓝 0) := by
  refine ⟨fun t => ?_, ?_⟩
  · rw [a_leitura_fecha_a_tangente]
    exact mul_ne_zero (Real.exp_pos _).ne' h
  · have hfun : (fun t : ℝ => tangenteDaLeitura K (axiomFlow K.starProjection t v))
        = fun t : ℝ => Real.exp (-t) * tangenteDaLeitura K v := by
      funext t
      exact a_leitura_fecha_a_tangente K t v
    rw [hfun]
    have h0 : Tendsto (fun t : ℝ => Real.exp (-t)) atTop (𝓝 0) := Real.tendsto_exp_neg_atTop_nhds_zero
    simpa using h0.mul_const (tangenteDaLeitura K v)

end Hilbert

/-! ## 7. A face clássica: o seletor devolve a esperança condicional dado o Nome -/

section Classica

variable {X : Type} [Fintype X] [DecidableEq X]

/-- ★ O PESO DO NOME, POR COORDENADAS: a soma dos pesos das leituras de custo zero. -/
theorem o_peso_do_nome_por_coordenadas (c : X → ℕ) (ψ : EuclideanSpace ℂ X) :
    ‖(opDaInstancia c).ker.starProjection ψ‖ ^ 2
      = ∑ x ∈ Finset.univ.filter (fun x => c x = 0), ‖WithLp.ofLp ψ x‖ ^ 2 := by
  rw [solucao_por_coordenadas, EuclideanSpace.norm_sq_eq, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro x _
  by_cases hx : c x = 0 <;> simp [hx]

/-- ★★★ A SELEÇÃO É A ESPERANÇA CONDICIONAL CLÁSSICA: para toda grandeza `g` das leituras, a média de `g` no estado selecionado é a
    média de `g` sobre o Nome com os pesos do estado, dividida pelo peso do Nome. É o condicionamento ao evento “custo zero”: os pesos
    relativos dentro do Nome não mudam, e o que está fora não entra. -/
theorem a_selecao_e_a_esperanca_condicional_classica (c : X → ℕ) (ψ : EuclideanSpace ℂ X)
    (hP : (opDaInstancia c).ker.starProjection ψ ≠ 0) (g : X → ℝ) :
    ∑ x, g x * ‖WithLp.ofLp (selecao (opDaInstancia c).ker ψ) x‖ ^ 2 =
      (∑ x ∈ Finset.univ.filter (fun x => c x = 0), g x * ‖WithLp.ofLp ψ x‖ ^ 2) /
      (∑ x ∈ Finset.univ.filter (fun x => c x = 0), ‖WithLp.ofLp ψ x‖ ^ 2) := by
  obtain ⟨N, hNdef⟩ : ∃ N : ℝ, N = ‖(opDaInstancia c).ker.starProjection ψ‖ := ⟨_, rfl⟩
  have hN : N ≠ 0 := by rw [hNdef]; exact norm_ne_zero_iff.mpr hP
  have hcoord : ∀ x, WithLp.ofLp (selecao (opDaInstancia c).ker ψ) x
      = ((N⁻¹ : ℝ) : ℂ) * (if c x = 0 then WithLp.ofLp ψ x else 0) := by
    intro x
    unfold selecao
    rw [← hNdef, solucao_por_coordenadas]
    simp
  rw [← o_peso_do_nome_por_coordenadas c ψ, ← hNdef, Finset.sum_filter, Finset.sum_div]
  apply Finset.sum_congr rfl
  intro x _
  rw [hcoord x, norm_mul, Complex.norm_real, Real.norm_eq_abs, abs_inv, mul_pow, inv_pow, sq_abs]
  by_cases hx : c x = 0
  · rw [if_pos hx, if_pos hx]
    field_simp
  · rw [if_neg hx, if_neg hx, norm_zero]
    simp

end Classica

end TGLExt.OHabitanteDoNome

#print axioms TGLExt.OHabitanteDoNome.o_leitor_habita_o_nome
#print axioms TGLExt.OHabitanteDoNome.a_imagem_do_leitor_e_a_morada
#print axioms TGLExt.OHabitanteDoNome.a_morada_e_o_que_comuta_com_o_posto
#print axioms TGLExt.OHabitanteDoNome.o_leitor_e_bimodular_sobre_o_nome
#print axioms TGLExt.OHabitanteDoNome.so_ha_um_habitante
#print axioms TGLExt.OHabitanteDoNome.o_operador_do_nome_e_o_habitante
#print axioms TGLExt.OHabitanteDoNome.a_esperanca_habita_fixa_e_nao_aumenta
#print axioms TGLExt.OHabitanteDoNome.a_testemunha_que_nao_aumenta_e_a_esperanca
#print axioms TGLExt.OHabitanteDoNome.o_nome_e_a_morada_de_uma_so_testemunha
#print axioms TGLExt.OHabitanteDoNome.quem_nao_e_a_esperanca_aumenta
#print axioms TGLExt.OHabitanteDoNome.a_leitura_do_vetor_e_a_compressao
#print axioms TGLExt.OHabitanteDoNome.a_leitura_do_operador_do_nome
#print axioms TGLExt.OHabitanteDoNome.o_seletor_tangencia_a_esperanca
#print axioms TGLExt.OHabitanteDoNome.o_que_e_cego_ao_nome_nao_deixa_rastro
#print axioms TGLExt.OHabitanteDoNome.o_livro_do_testemunho_fecha
#print axioms TGLExt.OHabitanteDoNome.a_tangente_da_leitura_e_K
#print axioms TGLExt.OHabitanteDoNome.o_peso_do_nome_e_o_cosseno_quadrado
#print axioms TGLExt.OHabitanteDoNome.o_crivo_e_a_meia_face
#print axioms TGLExt.OHabitanteDoNome.a_leitura_fecha_a_tangente
#print axioms TGLExt.OHabitanteDoNome.tangenciado_jamais_esgotado
#print axioms TGLExt.OHabitanteDoNome.o_peso_do_nome_por_coordenadas
#print axioms TGLExt.OHabitanteDoNome.a_selecao_e_a_esperanca_condicional_classica

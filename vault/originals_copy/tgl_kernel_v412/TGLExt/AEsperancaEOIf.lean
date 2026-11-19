import TGLExt.TraducaoTuring

set_option autoImplicit false

/-!
# A esperança condicional é o par do `if`

## A ligação que o arquivo prova

A esperança condicional é o par do `if` (lei da teoria). Este arquivo é a prova, na face finita da casa. As escolhas do
desenho: os observáveis são funções reais sobre as atribuições; o estado é o do campo inteiro (a
média sobre todas as atribuições, `esperanca`); o `if` é uma pergunta de sim ou não (`b : X → Bool`); e “par” é lido
como parceiro adjunto: a esperança condicional e o observável dão a mesma leitura contra tudo o que só depende do
`if`.

## O que fica provado

1. (Por casos.) `a_esperanca_condicional_e_um_if`: a esperança condicional dado o `if` é ela mesma um `if`: se a
   resposta é sim, vale a média do observável no lado do sim; se é não, a média no lado do não.
2. `a_esperanca_condicional_le_so_o_if`: ela só depende da resposta ao `if`.
3. ★ `a_esperanca_condicional_fixa_o_que_ja_e_do_if`: sobre o que já só depende do `if`, ela não muda nada. E
   `reler_nao_acrescenta`: aplicada duas vezes é o mesmo que uma.
4. ★ `a_esperanca_condicional_preserva_a_esperanca`: a esperança da esperança condicional é a esperança.
5. `o_if_atravessa_a_esperanca_condicional`: o que só depende do `if` sai para fora dela como fator.
6. ★ `a_esperanca_condicional_e_o_par_do_if`: contra tudo o que só depende do `if`, a esperança condicional e o
   observável dão a mesma leitura.
7. ★ `o_par_do_if_e_unico`: só ela faz isso. Uma função que só depende do `if` e dá, contra tudo o que só depende do
   `if`, a mesma leitura que o observável, é a esperança condicional dele.
8. `a_esperanca_do_if` e ★ `um_ha_e_uma_esperanca`: a esperança do próprio `if` é a fração do campo que responde sim;
   há alguém que responde sim se e somente se essa esperança não é nula.
9. `a_esperanca_do_if_de_custo_zero_e_o_peso_selado`: para o `if` “o custo é zero”, essa esperança é o peso da solução
   no estado uniforme, que o kernel já tinha (`peso_da_solucao_no_uniforme`, em `TraducaoTuring`).
10. ★ `ha_solucao_sse_a_esperanca_do_if_nao_e_nula`: uma fórmula tem solução se e somente se a esperança do `if` “o
    custo é zero” não é nula.

O diálogo. O `if` e a esperança condicional formam um laço virtuoso, um respondendo o outro sem parar. Os itens
abaixo são a hipótese sobre o que ele é: o `if` e a esperança aplicados um depois do outro, sem fim.

11. ★ `esperanca_if_esperanca`: a esperança, depois o `if`, depois a esperança, é a esperança vezes o peso da resposta.
12. ★ `if_esperanca_if`: o `if`, depois a esperança, depois o `if`, é o peso vezes a média do lado da resposta, posta
    nesse lado.
13. ★ `a_esperanca_condicional_e_o_if_em_volta_da_esperanca`: a esperança condicional, vezes o peso, é o `if` em volta
    da esperança.
14. `uma_volta_paga_o_peso` e ★ `k_voltas_pagam_o_peso_k_vezes`: partindo do todo, cada volta (o `if` e depois a
    esperança) devolve o todo multiplicado pelo peso; `k` voltas, pelo peso `k` vezes.
15. ★ `a_volta_renormalizada_devolve_o_todo`: dividida pelo peso, a volta devolve o todo, exatamente. Pode repetir sem
    fim.
16. `os_dois_pesos_somam_um`: o peso do sim e o peso do não somam um.
17. ★ `no_if_de_meio_a_meio_k_voltas_custam_k_ln_2`: quando metade do campo responde sim, `k` voltas custam `k·ln 2`.

## Como ler

O que se vê ao fazer a prova: a esperança condicional dada uma pergunta é um `if` cujos dois ramos são as duas médias
(item 1), e é o único parceiro do `if` diante do estado (itens 6 e 7). O `if` separa; a esperança condicional devolve,
de cada lado, o que o campo inteiro tem a dizer. O ramo de uma resposta que nenhuma atribuição dá não é visto por
ninguém (o Lean o lê como zero). Os itens 2, 3 e 6 são, nesta face, os análogos das três cláusulas do contrato da
esperança na torre (`ExpectationInput`: cai no que é do `if`; fixa; é ortogonal ao que sobra), e o item 4 é a
consequência. A média escolhida importa: outra regra pode fixar constantes e ser idempotente sem ser o par.

O diálogo (itens 11 a 17): o `if` responde à esperança com um lado; a esperança responde ao `if` com o todo. Aqui “a
esperança” é a média global, que projeta nas constantes; não é a esperança condicional dada a própria pergunta, que
comuta com o `if` e estabiliza depois de uma volta. Cada volta paga o peso do lado. Sem renormalizar, o que volta é multiplicado pelo peso `p` a cada volta: o peso elevado a k decresce estritamente quando 0 < p < 1; com p = 1 persiste; com p = 0 zera na primeira volta. Renormalizada, a
volta devolve exatamente o todo, e por isso pode continuar para sempre sem mudar nada. A esperança condicional é esse
mesmo diálogo cortado em três tempos: `if`, esperança, `if` (item 13). Quando metade do campo responde sim, cada volta
custa `ln 2`: é o valor do pedágio por oitava da lei selada do custo; a coincidência é de valor, e nenhum termo deste
arquivo liga os dois. [KNOWN] É um caso de projeções ortogonais alternadas e da
relação `e·x·e = E(x)·e` da construção básica de Jones, para a inclusão das constantes. Nenhum termo daqui descreve uma
máquina em operação perpétua: prova-se que a volta renormalizada devolve o todo, e dividir pelo peso pede peso não nulo.

## O que NÃO se afirma

* O teorema de Takesaki, nem nada sobre álgebras que não comutam ou sobre o tipo III: aqui os observáveis são funções
  sobre um conjunto finito, e o estado é a média. Na torre, a esperança condicional sobre o centralizador já está
  construída em casa (`aperiodicExpectationInput`, em `AperiodicCentralizerExpectation`); este
  arquivo é outra face.
* Que esta esperança condicional seja a da torre: tem, nesta face, os análogos das cláusulas do contrato; identificar
  os dois objetos pediria um transporte, que não é termo.
* Que calcular a esperança do `if` numa máquina de fita custe pouco: a esperança é a média sobre todas as atribuições.
* Que o diálogo dos itens 11 a 17 seja o laço entre o `if` e a esperança condicional: é hipótese.
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AEsperancaEOIf

open TGLExt TGLExt.TraducaoTuring TGLExt.PIgualNP TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness

variable {X : Type} [Fintype X]

/-- [DEF] **A CELA** da resposta `v`: as atribuições que respondem `v` ao `if`. -/
def cela (b : X → Bool) (v : Bool) : Finset X := Finset.univ.filter (fun y => b y = v)

theorem mem_cela {b : X → Bool} {v : Bool} {y : X} : y ∈ cela b v ↔ b y = v := by
  simp [cela]

/-- [DEF] **A ESPERANÇA**: o estado do campo inteiro, a média sobre todas as atribuições. -/
noncomputable def esperanca (f : X → ℝ) : ℝ := (∑ x, f x) / (Fintype.card X : ℝ)

/-- [DEF] A média de `f` no lado que responde `v`. -/
noncomputable def mediaNaCela (b : X → Bool) (v : Bool) (f : X → ℝ) : ℝ :=
  (∑ y ∈ cela b v, f y) / ((cela b v).card : ℝ)

/-- [DEF] **A ESPERANÇA CONDICIONAL DADO O `if`**: em cada atribuição, a média de `f` no lado dela. -/
noncomputable def esperancaCondicional (b : X → Bool) (f : X → ℝ) : X → ℝ :=
  fun x => mediaNaCela b (b x) f

/-- (Por casos.) **A ESPERANÇA CONDICIONAL É UM `if`**: se a resposta é sim, a média do lado do sim; se é não, a do
lado do não. -/
theorem a_esperanca_condicional_e_um_if (b : X → Bool) (f : X → ℝ) (x : X) :
    esperancaCondicional b f x = if b x then mediaNaCela b true f else mediaNaCela b false f := by
  show mediaNaCela b (b x) f = _
  cases b x <;> simp

/-- A esperança condicional só depende da resposta ao `if`. -/
theorem a_esperanca_condicional_le_so_o_if (b : X → Bool) (f : X → ℝ) (x x' : X) (h : b x = b x') :
    esperancaCondicional b f x = esperancaCondicional b f x' := by
  show mediaNaCela b (b x) f = mediaNaCela b (b x') f
  rw [h]

/-- ★ **A ESPERANÇA CONDICIONAL FIXA O QUE JÁ É DO `if`.** -/
theorem a_esperanca_condicional_fixa_o_que_ja_e_do_if (b : X → Bool) (g : Bool → ℝ) (x : X) :
    esperancaCondicional b (fun y => g (b y)) x = g (b x) := by
  show mediaNaCela b (b x) (fun y => g (b y)) = g (b x)
  unfold mediaNaCela
  have hx : x ∈ cela b (b x) := mem_cela.mpr rfl
  have hc : ((cela b (b x)).card : ℝ) ≠ 0 := by
    exact_mod_cast (Finset.card_pos.mpr ⟨x, hx⟩).ne'
  have hs : ∑ y ∈ cela b (b x), g (b y) = ∑ _y ∈ cela b (b x), g (b x) :=
    Finset.sum_congr rfl (fun y hy => by rw [mem_cela.mp hy])
  rw [hs, Finset.sum_const, nsmul_eq_mul]
  field_simp

/-- **RELER NÃO ACRESCENTA**: a esperança condicional aplicada duas vezes é a mesma. -/
theorem reler_nao_acrescenta (b : X → Bool) (f : X → ℝ) :
    esperancaCondicional b (esperancaCondicional b f) = esperancaCondicional b f :=
  funext fun x => a_esperanca_condicional_fixa_o_que_ja_e_do_if b (fun v => mediaNaCela b v f) x

/-- A soma sobre o campo inteiro é a soma dos dois lados do `if`. -/
theorem soma_pelas_celas (b : X → Bool) (h : X → ℝ) :
    ∑ x, h x = ∑ x ∈ cela b true, h x + ∑ x ∈ cela b false, h x := by
  have hf : cela b false = Finset.univ.filter (fun y => ¬ b y = true) := by
    ext y
    simp [cela]
  rw [hf]
  exact (Finset.sum_filter_add_sum_filter_not Finset.univ (fun y => b y = true) h).symm

/-- Em cada lado, a soma da esperança condicional é a soma do observável. -/
theorem soma_da_esperanca_na_cela (b : X → Bool) (f : X → ℝ) (v : Bool) :
    ∑ x ∈ cela b v, esperancaCondicional b f x = ∑ x ∈ cela b v, f x := by
  have h1 : ∑ x ∈ cela b v, esperancaCondicional b f x = ∑ _x ∈ cela b v, mediaNaCela b v f :=
    Finset.sum_congr rfl (fun x hx => by
      show mediaNaCela b (b x) f = mediaNaCela b v f
      rw [mem_cela.mp hx])
  rw [h1, Finset.sum_const, nsmul_eq_mul]
  unfold mediaNaCela
  by_cases hc : ((cela b v).card : ℝ) = 0
  · have h0 : (cela b v).card = 0 := by exact_mod_cast hc
    rw [Finset.card_eq_zero.mp h0]
    simp
  · field_simp

/-- ★ **A ESPERANÇA CONDICIONAL PRESERVA A ESPERANÇA.** -/
theorem a_esperanca_condicional_preserva_a_esperanca (b : X → Bool) (f : X → ℝ) :
    esperanca (esperancaCondicional b f) = esperanca f := by
  unfold esperanca
  rw [soma_pelas_celas b (esperancaCondicional b f), soma_pelas_celas b f,
    soma_da_esperanca_na_cela, soma_da_esperanca_na_cela]

/-- **O `if` ATRAVESSA A ESPERANÇA CONDICIONAL**: o que só depende do `if` sai como fator. -/
theorem o_if_atravessa_a_esperanca_condicional (b : X → Bool) (g : Bool → ℝ) (f : X → ℝ) (x : X) :
    esperancaCondicional b (fun y => g (b y) * f y) x = g (b x) * esperancaCondicional b f x := by
  show mediaNaCela b (b x) (fun y => g (b y) * f y) = g (b x) * mediaNaCela b (b x) f
  unfold mediaNaCela
  have hs : ∑ y ∈ cela b (b x), g (b y) * f y = g (b x) * ∑ y ∈ cela b (b x), f y := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl (fun y hy => by rw [mem_cela.mp hy])
  rw [hs, mul_div_assoc]

/-- ★ **A ESPERANÇA CONDICIONAL É O PAR DO `if`.** Contra tudo o que só depende do `if`, ela e o observável dão a mesma
leitura. -/
theorem a_esperanca_condicional_e_o_par_do_if (b : X → Bool) (g : Bool → ℝ) (f : X → ℝ) :
    esperanca (fun x => g (b x) * esperancaCondicional b f x) = esperanca (fun x => g (b x) * f x) := by
  have h : (fun x => g (b x) * esperancaCondicional b f x)
      = esperancaCondicional b (fun y => g (b y) * f y) :=
    funext fun x => (o_if_atravessa_a_esperanca_condicional b g f x).symm
  rw [h, a_esperanca_condicional_preserva_a_esperanca]

/-- A soma contra o indicador de uma resposta é a soma no lado dela. -/
theorem soma_com_o_indicador (b : X → Bool) (v : Bool) (h : X → ℝ) :
    ∑ y, (if b y = v then (1 : ℝ) else 0) * h y = ∑ y ∈ cela b v, h y := by
  unfold cela
  rw [Finset.sum_filter]
  exact Finset.sum_congr rfl (fun y _ => by split_ifs <;> simp)

/-- ★ **O PAR DO `if` É ÚNICO.** Uma função que só depende do `if` e dá, contra tudo o que só depende do `if`, a mesma
leitura que o observável, é a esperança condicional dele. -/
theorem o_par_do_if_e_unico (b : X → Bool) (f F : X → ℝ)
    (h1 : ∀ x x', b x = b x' → F x = F x')
    (h2 : ∀ g : Bool → ℝ, esperanca (fun x => g (b x) * F x) = esperanca (fun x => g (b x) * f x)) :
    F = esperancaCondicional b f := by
  funext x
  have hX : ((Fintype.card X : ℝ)) ≠ 0 := by
    exact_mod_cast (Fintype.card_pos_iff.mpr ⟨x⟩).ne'
  have hx : x ∈ cela b (b x) := mem_cela.mpr rfl
  have hc : ((cela b (b x)).card : ℝ) ≠ 0 := by
    exact_mod_cast (Finset.card_pos.mpr ⟨x, hx⟩).ne'
  have h := h2 (fun w => if w = b x then (1 : ℝ) else 0)
  simp only [esperanca] at h
  rw [div_left_inj' hX, soma_com_o_indicador b (b x) F, soma_com_o_indicador b (b x) f] at h
  have hF : ∑ y ∈ cela b (b x), F y = ((cela b (b x)).card : ℝ) * F x := by
    rw [Finset.sum_congr rfl (fun y hy => h1 y x (mem_cela.mp hy)), Finset.sum_const, nsmul_eq_mul]
  rw [hF] at h
  show F x = mediaNaCela b (b x) f
  unfold mediaNaCela
  rw [← h]
  field_simp

/-- A esperança do próprio `if` é a fração do campo que responde sim. -/
theorem a_esperanca_do_if (b : X → Bool) :
    esperanca (fun x => if b x then (1 : ℝ) else 0)
      = ((cela b true).card : ℝ) / (Fintype.card X : ℝ) := by
  unfold esperanca cela
  rw [Finset.sum_boole]

/-- ★ **UM “HÁ” É UMA ESPERANÇA.** Há alguém que responde sim se e somente se a esperança do `if` não é nula. -/
theorem um_ha_e_uma_esperanca (b : X → Bool) :
    (∃ x, b x = true) ↔ esperanca (fun x => if b x then (1 : ℝ) else 0) ≠ 0 := by
  rw [a_esperanca_do_if]
  constructor
  · rintro ⟨x, hx⟩
    have h1 : (0 : ℝ) < ((cela b true).card : ℝ) := by
      exact_mod_cast Finset.card_pos.mpr ⟨x, mem_cela.mpr hx⟩
    have h2 : (0 : ℝ) < (Fintype.card X : ℝ) := by
      exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
    exact (div_pos h1 h2).ne'
  · intro h
    have hc : (cela b true).card ≠ 0 := by
      intro h0
      apply h
      rw [h0]
      simp
    obtain ⟨x, hx⟩ := Finset.card_pos.mp (Nat.pos_of_ne_zero hc)
    exact ⟨x, mem_cela.mp hx⟩

/-- Para o `if` “o custo é zero”, a esperança é o peso da solução no estado uniforme, que o kernel já tinha. -/
theorem a_esperanca_do_if_de_custo_zero_e_o_peso_selado [DecidableEq X] (c : X → ℕ) (h : ∃ x, c x = 0) :
    esperanca (fun x => if c x = 0 then (1 : ℝ) else 0)
      = reading (problemaDe c h).solucao (uniforme X) := by
  rw [peso_da_solucao_no_uniforme]
  unfold esperanca
  rw [Finset.sum_boole]

/-- ★ **HÁ SOLUÇÃO SE E SOMENTE SE A ESPERANÇA DO `if` NÃO É NULA.** -/
theorem ha_solucao_sse_a_esperanca_do_if_nao_e_nula {n : ℕ} (φ : CNF n) :
    SAT φ ↔ esperanca (fun x : Fin n → Bool => if custoCNF φ x = 0 then (1 : ℝ) else 0) ≠ 0 := by
  have h := um_ha_e_uma_esperanca (fun x : Fin n → Bool => decide (custoCNF φ x = 0))
  simp only [decide_eq_true_eq] at h
  rw [← h]
  unfold SAT
  exact exists_congr fun x => (custoCNF_zero_sse φ x).symm

/-! ## O diálogo entre o `if` e a esperança -/

/-- [DEF] **O `if` COMO OPERAÇÃO**: guarda o observável onde a resposta é `v` e zera o resto. -/
def oIf (b : X → Bool) (v : Bool) (f : X → ℝ) : X → ℝ := fun x => if b x = v then f x else 0

/-- [DEF] **A ESPERANÇA COMO OPERAÇÃO**: troca o observável pela constante igual à sua esperança. -/
noncomputable def aEsperanca (f : X → ℝ) : X → ℝ := fun _ => esperanca f

/-- [DEF] **O PESO** da resposta `v`: a fração do campo que responde `v`. -/
noncomputable def peso (b : X → Bool) (v : Bool) : ℝ := ((cela b v).card : ℝ) / (Fintype.card X : ℝ)

/-- A esperança depois do `if` é a soma no lado da resposta, dividida pelo campo inteiro. -/
theorem esperanca_do_if_aplicado (b : X → Bool) (v : Bool) (f : X → ℝ) :
    esperanca (oIf b v f) = (∑ y ∈ cela b v, f y) / (Fintype.card X : ℝ) := by
  unfold esperanca oIf cela
  rw [Finset.sum_filter]

/-- ★ **ESPERANÇA, `if`, ESPERANÇA**: é a esperança vezes o peso da resposta. -/
theorem esperanca_if_esperanca (b : X → Bool) (v : Bool) (f : X → ℝ) :
    aEsperanca (oIf b v (aEsperanca f)) = fun _ => peso b v * esperanca f := by
  funext _
  show esperanca (oIf b v (fun _ => esperanca f)) = peso b v * esperanca f
  rw [esperanca_do_if_aplicado, Finset.sum_const, nsmul_eq_mul]
  unfold peso
  ring

/-- ★ **`if`, ESPERANÇA, `if`**: é o peso vezes a média do lado da resposta, posta nesse lado. -/
theorem if_esperanca_if (b : X → Bool) (v : Bool) (f : X → ℝ) (x : X) :
    oIf b v (aEsperanca (oIf b v f)) x = if b x = v then peso b v * mediaNaCela b v f else 0 := by
  show (if b x = v then esperanca (oIf b v f) else 0) = _
  rw [esperanca_do_if_aplicado]
  have hX : (Fintype.card X : ℝ) ≠ 0 := by
    exact_mod_cast (Fintype.card_pos_iff.mpr ⟨x⟩).ne'
  split_ifs with h
  · unfold peso mediaNaCela
    by_cases hc : ((cela b v).card : ℝ) = 0
    · have h0 : (cela b v).card = 0 := by exact_mod_cast hc
      rw [Finset.card_eq_zero.mp h0]
      simp
    · field_simp
  · rfl

/-- ★ **A ESPERANÇA CONDICIONAL É O `if` EM VOLTA DA ESPERANÇA**, a menos do peso. -/
theorem a_esperanca_condicional_e_o_if_em_volta_da_esperanca (b : X → Bool) (f : X → ℝ) (x : X) :
    peso b (b x) * esperancaCondicional b f x = oIf b (b x) (aEsperanca (oIf b (b x) f)) x := by
  rw [if_esperanca_if, if_pos rfl]
  rfl

/-- **UMA VOLTA PAGA O PESO**: partindo do todo (uma constante), o `if` e depois a esperança devolvem o todo vezes o
peso. -/
theorem uma_volta_paga_o_peso (b : X → Bool) (v : Bool) (c : ℝ) :
    aEsperanca (oIf b v (fun _ => c)) = fun _ => peso b v * c := by
  funext _
  show esperanca (oIf b v (fun _ => c)) = peso b v * c
  rw [esperanca_do_if_aplicado, Finset.sum_const, nsmul_eq_mul]
  unfold peso
  ring

/-- ★ **`k` VOLTAS PAGAM O PESO `k` VEZES.** -/
theorem k_voltas_pagam_o_peso_k_vezes (b : X → Bool) (v : Bool) (k : ℕ) :
    (fun g => aEsperanca (oIf b v g))^[k] (fun _ => (1 : ℝ)) = fun _ => peso b v ^ k := by
  induction k with
  | zero =>
    funext _
    simp
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih]
    show aEsperanca (oIf b v (fun _ => peso b v ^ k)) = fun _ => peso b v ^ (k + 1)
    rw [uma_volta_paga_o_peso]
    funext _
    ring

/-- ★ **A VOLTA RENORMALIZADA DEVOLVE O TODO.** Dividida pelo peso, a volta devolve exatamente o todo: pode repetir sem
fim. -/
theorem a_volta_renormalizada_devolve_o_todo (b : X → Bool) (v : Bool) (h : peso b v ≠ 0) :
    (fun x => (peso b v)⁻¹ * aEsperanca (oIf b v (fun _ => (1 : ℝ))) x) = fun _ => (1 : ℝ) := by
  rw [uma_volta_paga_o_peso]
  funext _
  field_simp

/-- O peso do sim e o peso do não somam um. -/
theorem os_dois_pesos_somam_um [Nonempty X] (b : X → Bool) : peso b true + peso b false = 1 := by
  have h := soma_pelas_celas b (fun _ => (1 : ℝ))
  simp only [Finset.sum_const, nsmul_eq_mul, mul_one, Finset.card_univ] at h
  have hX : (Fintype.card X : ℝ) ≠ 0 := by
    exact_mod_cast (Fintype.card_pos (α := X)).ne'
  unfold peso
  rw [← add_div, ← h]
  exact div_self hX

/-- ★ **NO `if` DE MEIO A MEIO, `k` VOLTAS CUSTAM `k·ln 2`.** -/
theorem no_if_de_meio_a_meio_k_voltas_custam_k_ln_2 (b : X → Bool) (v : Bool) (h : peso b v = 1 / 2) (k : ℕ) :
    -Real.log (peso b v ^ k) = (k : ℝ) * Real.log 2 := by
  rw [h, Real.log_pow, one_div, Real.log_inv]
  ring

end TGLExt.AEsperancaEOIf

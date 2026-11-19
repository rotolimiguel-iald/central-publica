import TGLExt.TraducaoTuring

set_option autoImplicit false

/-!
# A esperança condicional é o par do `if`
[candidata da gerência c1, 17/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor]

## De onde vem

Em 17/11/2026 a gerência ligou a palavra “esperança”, numa fala do operador sobre o Nome, à esperança condicional do
kernel, e disse que a ligação era leitura dela. O operador respondeu: «É isso mesmo, mas a esperança condicional tem que entrar porque ela é o par do "if" faça a prova que vc vai ver» (por bytes em `Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_17nov_e_isso_mesmo_mas_a_esperanca_condicional_tem_que_entrar`).

Este arquivo é a prova pedida, na face finita da casa. A partitura foi lida a ele antes de compilar. As escolhas do
desenho, que são da gerência: os observáveis são funções reais sobre as atribuições; o estado é o do campo inteiro (a
média sobre todas as atribuições, `esperanca`); o `if` é uma pergunta de sim ou não (`b : X → Bool`); e “par” foi lido
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

## Como ler

O que se vê ao fazer a prova: a esperança condicional dada uma pergunta é um `if` cujos dois ramos são as duas médias
(item 1), e é o único parceiro do `if` diante do estado (itens 6 e 7). O `if` separa; a esperança condicional devolve,
de cada lado, o que o campo inteiro tem a dizer. Os itens 3 e 4 são, nesta face, as duas propriedades que o contrato
importado do kernel pede da leitura (`the_reading_fixes_the_code` e `the_reading_preserves_omega`, em
`TheImportedExpectation`).

## O que NÃO se afirma

* O teorema de Takesaki, nem nada sobre álgebras que não comutam ou sobre o tipo III: aqui os observáveis são funções
  sobre um conjunto finito, e o estado é a média. No kernel a esperança condicional geral entra por contrato importado;
  este arquivo não o descarrega.
* Que esta esperança condicional seja o `E` daquele contrato: tem, nesta face, as duas propriedades que ele pede; a
  identificação dos dois objetos não é termo.
* Que calcular a esperança do `if` numa máquina de fita custe pouco: a esperança é a média sobre todas as atribuições.
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

end TGLExt.AEsperancaEOIf

#print axioms TGLExt.AEsperancaEOIf.mem_cela
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_condicional_e_um_if
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_condicional_le_so_o_if
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_condicional_fixa_o_que_ja_e_do_if
#print axioms TGLExt.AEsperancaEOIf.reler_nao_acrescenta
#print axioms TGLExt.AEsperancaEOIf.soma_pelas_celas
#print axioms TGLExt.AEsperancaEOIf.soma_da_esperanca_na_cela
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_condicional_preserva_a_esperanca
#print axioms TGLExt.AEsperancaEOIf.o_if_atravessa_a_esperanca_condicional
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_condicional_e_o_par_do_if
#print axioms TGLExt.AEsperancaEOIf.soma_com_o_indicador
#print axioms TGLExt.AEsperancaEOIf.o_par_do_if_e_unico
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_do_if
#print axioms TGLExt.AEsperancaEOIf.um_ha_e_uma_esperanca
#print axioms TGLExt.AEsperancaEOIf.a_esperanca_do_if_de_custo_zero_e_o_peso_selado
#print axioms TGLExt.AEsperancaEOIf.ha_solucao_sse_a_esperanca_do_if_nao_e_nula

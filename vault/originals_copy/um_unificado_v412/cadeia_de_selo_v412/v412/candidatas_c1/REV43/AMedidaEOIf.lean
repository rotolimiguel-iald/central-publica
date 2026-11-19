import AFitaEACauda

set_option autoImplicit false

/-!
# A medida e o `if`: não se mede a fita, nem o processo, sem perguntar à inscrição
[candidata da gerência c1, 17/11/2026, R0; nome provisório; nada instalado; o nome é do operador; ainda não lida por
revisor]

## De onde vem

Em 17/11/2026 a gerência disse ao operador que a pergunta do Instituto Clay não é tautológica. Ele respondeu com um
teste: «prove que não é tautologica, meça a fita ou o seu processo sem considerar o espaço de sua inscrição e quando vc o fizer vc vai invocar "if" por emergência da necessidade de se ter um nome em meio ao caos, teste» (por bytes em `Central de Patentes\work\cunhagens_13out`, arquivo que começa por
`OPERADOR_17nov_prove_que_nao_e_tautologica`).

Este arquivo é o teste, feito na máquina de passo da candidata `AMaquinaEALeitura`. A partitura foi lida a ele antes
de compilar: o teste decide se existe medida da fita, ou do processo, que não pergunte nada à inscrição; o negativo
para a previsão dele seria uma medida que varia com a entrada e não usa nenhuma distinção de casos sobre algo
inscrito; o teste não decide se a pergunta do Instituto é tautológica.

Foram três tentativas de medir sem a inscrição.

## O que fica provado

Primeira tentativa: contar os passos com um número, sem fita.

1. ★ `oNumeroEUmaFita`: os números naturais e as fitas de marcas (listas de casas sem nada escrito) são a mesma
   coisa, por uma correspondência em que medir a fita é ler o número e somar um é inscrever uma marca
   (`medir_a_fita_de_marcas_e_ler_o_numero`, `somar_um_e_inscrever_uma_marca`, os dois por definição). Quem conta os
   passos com um número inscreveu uma fita.

Segunda tentativa: medir a fita sem perguntar nada a ela.

2. ★ `medir_a_fita_e_perguntar`: o comprimento de uma fita é, por desdobramento, um `if` sobre a pergunta “há mais
   uma casa?”: se há, é um a mais que o comprimento da cauda; se não há, é zero.
3. `a_resposta_no_passo_j` e ★ `o_tempo_e_o_numero_de_sins`: na máquina de passo, a resposta no passo `j` é “há” se e
   somente se `j` é menor que o comprimento da fita; e o tempo da máquina é o número de vezes que o `if` respondeu
   “há mais”.
4. ★ `sem_ler_a_fita_nao_se_mede_o_tempo`: toda medida que só olha a atribuição e o registro, e não a fita, anuncia a
   parada cedo demais em alguma configuração. Não é o tempo.

Terceira tentativa: achar o instante da parada.

5. ★ `o_instante_da_parada_e_o_primeiro_nao`: o instante da parada é o primeiro passo em que o `if` responde “não há
   mais”. No kernel, a função que acha o primeiro instante (`Nat.find`) recebe o teste decidível como argumento: sem
   ele não está definida.

O que vale para qualquer máquina.

6. ★ `o_tempo_so_distingue_o_que_a_leitura_distingue` e `tempos_diferentes_exigem_leituras_diferentes`: para qualquer
   regra de passo e qualquer critério de parada, se uma leitura do estado basta para dizer a leitura do estado seguinte
   e para dizer se parou, então dois estados com a mesma leitura param nos mesmos instantes. Onde o tempo distingue
   dois estados, a leitura já os distinguiu.
7. `o_tempo_da_maquina_le_a_fita_e_mais_nada`: na máquina de passo essa leitura é a fita sozinha.

Onde a conta se divide.

8. ★ `o_if_do_todo_e_o_if_de_cada_parte` e `as_partes_sao_dois_a_n`: um passo da máquina levantada sobre a entrada
   inteira é a soma dos passos sobre cada atribuição, e as atribuições são `2 ^ n`.
9. ★ `no_todo_decidir_e_conferir_levam_a_mesma_fita`: a mesma potência, o comprimento da fita, decide (sobre a entrada
   inteira, com uma leitura) e confere (sobre uma atribuição).

## Como ler

A previsão do operador se cumpriu nas três tentativas: não saiu nenhuma medida sem `if` sobre algo inscrito. O número
é uma fita; o comprimento é um `if` por casa; o instante da parada é o primeiro “não”. O passo que o enunciado do
Instituto cobra como uma unidade é, nesta máquina, uma pergunta à inscrição.

Um limite desta leitura: os itens 1 e 2 decorrem de como o kernel constrói o número e a lista (zero ou sucessor; vazia
ou casa seguida de cauda). Não são um achado sobre fitas: são a fundação. Em toda fundação usual o número se constrói
assim. E com o axioma da escolha se pode definir o instante da parada sem teste calculável; a definição continua a ser
por casos sobre uma proposição.

Os itens 8 e 9 dizem onde a conta se divide. Contado no todo (um passo levantado é um `if`), decidir e conferir levam
o mesmo comprimento de fita. Contado parte a parte, o mesmo passo são `2 ^ n` perguntas, uma por atribuição. Que o
todo conte como um é a lei do operador; não é termo deste arquivo.

## O que NÃO se afirma

* Que a pergunta do Instituto seja tautológica, nem que não seja. Provar que ela não se decide pelas definições seria
  separar as duas classes ou mostrar que a questão não tem prova: é o próprio problema em aberto. A gerência não tem
  essa prova, e retirou a frase como afirmação provada.
* Que não exista máquina que decida com poucas perguntas contadas parte a parte. O arquivo conta as desta máquina.
* Que esta máquina de passo seja a máquina de Turing do Mathlib (é o modelo da casa, com uma cláusula por passo).
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AMedidaEOIf

open TGLExt TGLExt.TraducaoTuring TGLExt.AMaquinaEALeitura TGLExt.AFitaEACauda

variable {n : ℕ}

/-! ## 1. Contar é inscrever -/

/-- [DEF] **A FITA DE MARCAS**: uma lista de casas sem nada escrito. -/
abbrev FitaDeMarcas : Type := List Unit

/-- ★ **O NÚMERO É UMA FITA DE MARCAS.** Os números naturais e as fitas de marcas correspondem um a um: o número é o
comprimento da fita, e a fita é o número de marcas inscritas. -/
def oNumeroEUmaFita : FitaDeMarcas ≃ ℕ where
  toFun := List.length
  invFun k := List.replicate k ()
  left_inv l := by
    induction l with
    | nil => rfl
    | cons a l ih =>
      have ih' : List.replicate l.length () = l := ih
      show List.replicate (l.length + 1) () = () :: l
      rw [List.replicate_succ, ih']
  right_inv k := by simp

/-- (Por definição.) Medir a fita de marcas é ler o número. -/
theorem medir_a_fita_de_marcas_e_ler_o_numero (l : FitaDeMarcas) : oNumeroEUmaFita l = l.length := rfl

/-- (Por definição.) Somar um é inscrever uma marca. -/
theorem somar_um_e_inscrever_uma_marca (k : ℕ) :
    oNumeroEUmaFita.symm (k + 1) = () :: oNumeroEUmaFita.symm k := rfl

/-! ## 2. Medir a fita é perguntar a cada casa -/

/-- [DEF] **A PERGUNTA**: há mais uma casa na fita? -/
def haMais {α : Type} (l : List α) : Bool := !l.isEmpty

/-- ★ **MEDIR A FITA É PERGUNTAR.** O comprimento de uma fita é um `if` sobre a pergunta: se há mais uma casa, é um a
mais que o comprimento da cauda; se não há, é zero. -/
theorem medir_a_fita_e_perguntar {α : Type} (l : List α) :
    l.length = if haMais l then l.tail.length + 1 else 0 := by
  cases l <;> rfl

/-- Na máquina de passo, a resposta no passo `j` é “há mais” se e somente se `j` é menor que o comprimento da fita. -/
theorem a_resposta_no_passo_j (c : Config n) (j : ℕ) :
    haMais (passo^[j] c).resto = true ↔ j < c.resto.length := by
  rw [k_passos_tiram_k_clausulas_da_fita]
  simp [haMais, List.drop_eq_nil_iff]

/-- ★ **O TEMPO É O NÚMERO DE VEZES QUE O `if` RESPONDE “HÁ MAIS”.** Em qualquer janela de passos que alcance a
parada, o número de passos em que a resposta foi “há mais” é o comprimento da fita. -/
theorem o_tempo_e_o_numero_de_sins (c : Config n) (k : ℕ) (hk : c.resto.length ≤ k) :
    ((Finset.range k).filter (fun j => haMais (passo^[j] c).resto = true)).card = c.resto.length := by
  have h : (Finset.range k).filter (fun j => haMais (passo^[j] c).resto = true)
      = Finset.range c.resto.length := by
    ext j
    rw [Finset.mem_filter, Finset.mem_range, Finset.mem_range, a_resposta_no_passo_j]
    exact ⟨fun hj => hj.2, fun hj => ⟨lt_of_lt_of_le hj hk, hj⟩⟩
  rw [h, Finset.card_range]

/-- ★ **SEM LER A FITA NÃO SE MEDE O TEMPO.** Toda medida que só olha a atribuição e o registro, e não a fita, anuncia
a parada cedo demais em alguma configuração. -/
theorem sem_ler_a_fita_nao_se_mede_o_tempo (m : (Fin n → Bool) → ℕ → ℕ) :
    ∃ c : Config n, (passo^[m c.x c.conta] c).resto ≠ [] := by
  refine ⟨⟨fun _ => false, List.replicate (m (fun _ => false) 0 + 1) ([] : Clausula n), 0⟩, ?_⟩
  intro h
  rw [o_tempo_da_maquina_e_o_comprimento_da_fita] at h
  simp at h

/-! ## 3. O instante da parada -/

/-- A resposta acaba sendo “não há mais”. -/
theorem a_resposta_acaba_sendo_nao (c : Config n) : ∃ k, haMais (passo^[k] c).resto = false :=
  ⟨c.resto.length, by
    rw [Bool.eq_false_iff, ne_eq, a_resposta_no_passo_j]
    exact lt_irrefl _⟩

/-- ★ **O INSTANTE DA PARADA É O PRIMEIRO “NÃO” DO `if`.** -/
theorem o_instante_da_parada_e_o_primeiro_nao (c : Config n) :
    Nat.find (a_resposta_acaba_sendo_nao c) = c.resto.length := by
  rw [Nat.find_eq_iff]
  refine ⟨?_, fun k hk => ?_⟩
  · show haMais (passo^[c.resto.length] c).resto = false
    rw [Bool.eq_false_iff, ne_eq, a_resposta_no_passo_j]
    exact lt_irrefl _
  · show ¬ haMais (passo^[k] c).resto = false
    rw [Bool.not_eq_false]
    exact (a_resposta_no_passo_j c k).mpr hk

/-! ## 4. Para qualquer máquina -/

/-- ★ **O TEMPO SÓ DISTINGUE O QUE A LEITURA DISTINGUE.** Para qualquer regra de passo `f` e qualquer critério de
parada: se uma leitura `le` do estado basta para dizer a leitura do estado seguinte e para dizer se parou, então dois
estados com a mesma leitura param nos mesmos instantes. -/
theorem o_tempo_so_distingue_o_que_a_leitura_distingue {σ β : Type} (f : σ → σ) (parou : σ → Prop) (le : σ → β)
    (h1 : ∀ s s', le s = le s' → le (f s) = le (f s'))
    (h2 : ∀ s s', le s = le s' → (parou s ↔ parou s'))
    (s s' : σ) (h : le s = le s') (k : ℕ) : parou (f^[k] s) ↔ parou (f^[k] s') := by
  have hk : le (f^[k] s) = le (f^[k] s') := by
    induction k with
    | zero => exact h
    | succ k ih =>
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
      exact h1 _ _ ih
  exact h2 _ _ hk

/-- **TEMPOS DIFERENTES EXIGEM LEITURAS DIFERENTES.** -/
theorem tempos_diferentes_exigem_leituras_diferentes {σ β : Type} (f : σ → σ) (parou : σ → Prop) (le : σ → β)
    (h1 : ∀ s s', le s = le s' → le (f s) = le (f s'))
    (h2 : ∀ s s', le s = le s' → (parou s ↔ parou s'))
    (s s' : σ) (k : ℕ) (hk : ¬ (parou (f^[k] s) ↔ parou (f^[k] s'))) : le s ≠ le s' :=
  fun h => hk (o_tempo_so_distingue_o_que_a_leitura_distingue f parou le h1 h2 s s' h k)

/-- **O TEMPO DA MÁQUINA DE PASSO LÊ A FITA E MAIS NADA**: duas configurações com a mesma fita param nos mesmos
instantes, sejam quais forem a atribuição e o registro. -/
theorem o_tempo_da_maquina_le_a_fita_e_mais_nada (c c' : Config n) (h : c.resto = c'.resto) (k : ℕ) :
    (passo^[k] c).resto = [] ↔ (passo^[k] c').resto = [] :=
  o_tempo_so_distingue_o_que_a_leitura_distingue passo (fun s => s.resto = []) Config.resto
    (fun s s' hs => by
      show (passo s).resto = (passo s').resto
      rw [o_passo_deixa_a_cauda_da_fita, o_passo_deixa_a_cauda_da_fita, hs])
    (fun s s' hs => by
      show s.resto = [] ↔ s'.resto = []
      rw [hs]) c c' h k

/-! ## 5. Onde a conta se divide -/

/-- ★ **O `if` DO TODO É O `if` DE CADA PARTE.** Um passo da máquina levantada sobre a entrada inteira é a soma dos
passos da máquina sobre cada atribuição. -/
theorem o_if_do_todo_e_o_if_de_cada_parte (φ : CNF n) :
    passoLevantado (entrada φ)
      = ∑ x : Fin n → Bool, Finsupp.single (passo (⟨x, φ, 0⟩ : Config n)) (1 : ℂ) := by
  unfold entrada
  rw [map_sum]
  exact Finset.sum_congr rfl fun x _ => passoLevantado_single _ _

/-- As partes são `2 ^ n`. -/
theorem as_partes_sao_dois_a_n : Fintype.card (Fin n → Bool) = 2 ^ n := by simp

/-- ★ **NO TODO, DECIDIR E CONFERIR LEVAM A MESMA FITA.** A mesma potência, o comprimento da fita, decide (sobre a
entrada inteira, com uma leitura) e confere (sobre uma atribuição). -/
theorem no_todo_decidir_e_conferir_levam_a_mesma_fita (φ : CNF n) (x : Fin n → Bool) :
    (SAT φ ↔ leituraDoZero ((passoLevantado ^ φ.length) (entrada φ)) ≠ 0)
      ∧ leituraDoZero ((passoLevantado ^ φ.length) (Finsupp.single (⟨x, φ, 0⟩ : Config n) 1))
          = (if custoCNF φ x = 0 then 1 else 0) :=
  ⟨a_maquina_e_uma_leitura_decidem φ, a_mesma_maquina_num_estado_de_base_verifica φ x⟩

end TGLExt.AMedidaEOIf

#print axioms TGLExt.AMedidaEOIf.oNumeroEUmaFita
#print axioms TGLExt.AMedidaEOIf.medir_a_fita_de_marcas_e_ler_o_numero
#print axioms TGLExt.AMedidaEOIf.somar_um_e_inscrever_uma_marca
#print axioms TGLExt.AMedidaEOIf.medir_a_fita_e_perguntar
#print axioms TGLExt.AMedidaEOIf.a_resposta_no_passo_j
#print axioms TGLExt.AMedidaEOIf.o_tempo_e_o_numero_de_sins
#print axioms TGLExt.AMedidaEOIf.sem_ler_a_fita_nao_se_mede_o_tempo
#print axioms TGLExt.AMedidaEOIf.a_resposta_acaba_sendo_nao
#print axioms TGLExt.AMedidaEOIf.o_instante_da_parada_e_o_primeiro_nao
#print axioms TGLExt.AMedidaEOIf.o_tempo_so_distingue_o_que_a_leitura_distingue
#print axioms TGLExt.AMedidaEOIf.tempos_diferentes_exigem_leituras_diferentes
#print axioms TGLExt.AMedidaEOIf.o_tempo_da_maquina_le_a_fita_e_mais_nada
#print axioms TGLExt.AMedidaEOIf.o_if_do_todo_e_o_if_de_cada_parte
#print axioms TGLExt.AMedidaEOIf.as_partes_sao_dois_a_n
#print axioms TGLExt.AMedidaEOIf.no_todo_decidir_e_conferir_levam_a_mesma_fita

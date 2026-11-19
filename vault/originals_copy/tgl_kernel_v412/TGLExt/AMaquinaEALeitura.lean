import TGLExt.TraducaoTuring

set_option autoImplicit false

/-!
# A máquina e a leitura: a mesma potência age em cada parcela da combinação

## A identificação que o arquivo tipa

A contagem da leitura em passos de uma máquina clássica não é outra coisa senão a sua própria carga, a própria
isometria; matemática, lógica e física medem o mesmo porque são isotrópicas. Falta um teorema sobre a própria
máquina. Este arquivo é um caminho para isso: não resolve o problema em aberto; reduz a lacuna a uma linha.

## A construção

Uma MÁQUINA DE PASSO que confere uma atribuição contra uma fórmula: a configuração guarda a atribuição, as cláusulas
ainda não lidas e um registro; a cada passo lê UMA cláusula e soma 1 ao registro se ela está violada. A mesma regra de
passo, estendida por linearidade às combinações de configurações, é a MÁQUINA LEVANTADA. A LEITURA DO ZERO é o
funcional linear que soma os coeficientes das configurações de registro zero.

## O que fica provado

1. `a_maquina_conta_os_falsos`: em tantos passos quantas são as cláusulas, a máquina deixa no registro o custo da
   atribuição. É a conferência de UMA resposta, o que define a classe NP.
2. ★ `a_contagem_e_do_operador`: `k` passos da máquina levantada sobre qualquer combinação de configurações são `k`
   passos em cada parcela. É a linearidade da potência, mais a sua ação na base: uma igualdade de somas finitas, não
   uma medição de complexidade. O que ela diz é que o número de aplicações da regra é o mesmo qualquer que seja o
   vetor.
3. ★ `a_maquina_levantada_calcula_todos_os_custos`: aplicada à soma de TODAS as atribuições, a máquina levantada
   deixa escrito, nos mesmos passos do item 1, o custo de cada uma.
4. ★ `uma_leitura_da_o_numero_de_solucoes`: uma leitura do zero sobre esse resultado devolve o número de soluções.
5. ★ `a_maquina_e_uma_leitura_decidem`: a fórmula é satisfazível se e somente se essa leitura é diferente de zero.
   Passos da máquina: o número de cláusulas. Leituras: uma.
6. `a_mesma_maquina_num_estado_de_base_verifica`: controle. Com UMA atribuição na entrada, a mesma máquina, nos mesmos
   passos, com a mesma leitura, só confere aquela atribuição. A diferença entre conferir e decidir está toda na
   entrada (uma direção ou todas) e na leitura (sobre uma parcela ou sobre a soma).

## A linha que resta

Juntos, os itens dizem: a extensão linear da máquina de passo, mais a entrada posta inteira de uma vez, mais UMA
leitura do registro zero, decide toda fórmula em número de passos LEVANTADOS igual ao número de cláusulas. O `2ⁿ` não
aparece na contagem dos passos levantados. Aparece em três lugares: na entrada, que é a soma de todas as atribuições
(`2ⁿ` parcelas distintas, mesmo para a fórmula vazia); em cada passo levantado, que é UMA aplicação de uma regra
global a todas as parcelas; e na leitura, que é um funcional sobre a soma. A hipótese nomeada que falta para o
enunciado da máquina sem leitura é esta: QUE PÔR O TODO, OPERAR SOBRE ELE E LÊ-LO SEJAM, CADA UM, UM ATO. É lei da teoria (não há observação sem leitura) e a tradução do dicionário (no kernel, v409, o psíon lê os pixels de uma
vez). Não é termo deste arquivo, e nenhum termo daqui mostra que bastaria cobrar uma unidade a cada um desses atos.

Outros custos que a construção deixa de fora: tomar uma cláusula inteira por passo primitivo não conta a avaliação
dos seus literais; escrever as parcelas, atualizar a representação de trabalho e somar os coeficientes têm custo; uma
descrição simbólica curta da soma não dá, por si, um algoritmo eficiente para operar e ler sob essa descrição. O
resultado exato da leitura, um inteiro entre 0 e `2ⁿ`, cabe em `n + 1` casas binárias.

## O que NÃO se afirma

* Que esta máquina de passo seja a máquina de Turing do Mathlib (`Turing.TM2ComputableInPolyTime`): é um modelo da
  casa, de configurações e regra de passo, com uma cláusula por passo. A ligação à formalização do Mathlib não está
  construída.
* Que uma máquina de fita SEM leitura possa pôr a soma de todas as atribuições na entrada, ou ler um funcional sobre
  ela, em poucos movimentos. Esse é o problema em aberto, e este arquivo não o toca.
* Quanto custa na natureza a leitura do item 4, que devolve uma contagem inteira exata do registro zero. (A margem da
  leitura normalizada, tratada na pedra `AContagemEACarga`, é de outro teste: lá se compara uma média com um
  limiar; aqui se lê um inteiro.)
* Novidade na literatura. A construção é a linearização de uma transição determinística num módulo livre, seguida de
  um funcional linear, parente das representações lineares de autômatos com pesos [KNOWN, Schützenberger 1961]. Para
  fórmulas, o que a leitura devolve é a contagem de soluções, função #P-completa [KNOWN, Valiant 1979], e uma consulta
  de contagem exata basta para decidir a satisfazibilidade, que é NP-completa [KNOWN, Cook 1971]. [As três referências estão por conferir na fonte antes de publicar.]
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AMaquinaEALeitura

open TGLExt TGLExt.TraducaoTuring

variable {n : ℕ}

/-- [DEF] **A CONFIGURAÇÃO** da máquina de passo: a atribuição (a entrada), as cláusulas ainda não lidas e o registro. -/
structure Config (n : ℕ) where
  /-- a atribuição que está sendo conferida -/
  x : Fin n → Bool
  /-- as cláusulas ainda não lidas -/
  resto : CNF n
  /-- o registro: quantas cláusulas violadas até aqui -/
  conta : ℕ

/-- [DEF] **O PASSO**: lê UMA cláusula e soma 1 ao registro se ela está violada; sem cláusula a ler, para. -/
def passo (c : Config n) : Config n :=
  match c.resto with
  | [] => c
  | C :: ψ => ⟨c.x, ψ, c.conta + (if satisfeita C c.x then 0 else 1)⟩

/-- **A MÁQUINA CONTA OS FALSOS**: em tantos passos quantas são as cláusulas, o registro recebe o custo da atribuição. -/
theorem a_maquina_conta_os_falsos (φ : CNF n) (x : Fin n → Bool) (r : ℕ) :
    passo^[φ.length] (⟨x, φ, r⟩ : Config n) = ⟨x, [], r + custoCNF φ x⟩ := by
  induction φ generalizing r with
  | nil => simp [custoCNF]
  | cons C ψ ih =>
    show passo^[ψ.length + 1] (⟨x, C :: ψ, r⟩ : Config n) = _
    rw [Function.iterate_succ_apply]
    show passo^[ψ.length] (⟨x, ψ, r + (if satisfeita C x then 0 else 1)⟩ : Config n) = _
    rw [ih, custoCNF_cons]
    congr 1
    ring

/-- [DEF] **A MÁQUINA LEVANTADA**: a mesma regra de passo, sobre as combinações de configurações. Linear. -/
noncomputable def passoLevantado : (Config n →₀ ℂ) →ₗ[ℂ] (Config n →₀ ℂ) := Finsupp.lmapDomain ℂ ℂ passo

/-- Um passo levantado sobre uma configuração de base é o passo da máquina. -/
theorem passoLevantado_single (c : Config n) (a : ℂ) :
    passoLevantado (Finsupp.single c a) = Finsupp.single (passo c) a := by
  unfold passoLevantado
  rw [Finsupp.lmapDomain_apply, Finsupp.mapDomain_single]

/-- `k` passos levantados sobre uma configuração de base são `k` passos da máquina. -/
theorem k_passos_num_estado_de_base (c : Config n) (a : ℂ) (k : ℕ) :
    (passoLevantado ^ k) (Finsupp.single c a) = Finsupp.single (passo^[k] c) a := by
  induction k generalizing c with
  | zero => rfl
  | succ k ih =>
    rw [pow_succ]
    show (passoLevantado ^ k) (passoLevantado (Finsupp.single c a)) = _
    rw [passoLevantado_single, ih, Function.iterate_succ_apply]

/-- ★ **A MESMA POTÊNCIA AGE EM CADA PARCELA DA COMBINAÇÃO** (é a linearidade). `k` passos da máquina levantada sobre
qualquer combinação de configurações são `k` passos em cada parcela. -/
theorem a_contagem_e_do_operador {ι : Type} (s : Finset ι) (c : ι → Config n) (a : ι → ℂ) (k : ℕ) :
    (passoLevantado ^ k) (∑ i ∈ s, Finsupp.single (c i) (a i))
      = ∑ i ∈ s, Finsupp.single (passo^[k] (c i)) (a i) := by
  rw [map_sum]
  exact Finset.sum_congr rfl fun i _ => k_passos_num_estado_de_base (c i) (a i) k

/-- [DEF] **A ENTRADA INTEIRA**: a soma de todas as atribuições, cada uma com a fórmula por ler e o registro em zero. -/
noncomputable def entrada (φ : CNF n) : Config n →₀ ℂ :=
  ∑ x : Fin n → Bool, Finsupp.single (⟨x, φ, 0⟩ : Config n) 1

/-- ★ **A MÁQUINA LEVANTADA CALCULA TODOS OS CUSTOS** nos mesmos passos em que confere uma atribuição. -/
theorem a_maquina_levantada_calcula_todos_os_custos (φ : CNF n) :
    (passoLevantado ^ φ.length) (entrada φ)
      = ∑ x : Fin n → Bool, Finsupp.single (⟨x, [], custoCNF φ x⟩ : Config n) 1 := by
  unfold entrada
  rw [a_contagem_e_do_operador]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [a_maquina_conta_os_falsos, Nat.zero_add]

/-- [DEF] **A LEITURA DO ZERO**: o funcional linear que soma os coeficientes das configurações de registro zero. -/
noncomputable def leituraDoZero : (Config n →₀ ℂ) →ₗ[ℂ] ℂ :=
  Finsupp.linearCombination ℂ (fun c : Config n => if c.conta = 0 then (1 : ℂ) else 0)

/-- A leitura do zero numa configuração de base: o coeficiente, se o registro é zero; nada, se não é. -/
theorem leituraDoZero_single (c : Config n) (a : ℂ) :
    leituraDoZero (Finsupp.single c a) = if c.conta = 0 then a else 0 := by
  unfold leituraDoZero
  rw [Finsupp.linearCombination_single]
  split_ifs <;> simp

/-- ★ **UMA LEITURA DÁ O NÚMERO DE SOLUÇÕES.** -/
theorem uma_leitura_da_o_numero_de_solucoes (φ : CNF n) :
    leituraDoZero ((passoLevantado ^ φ.length) (entrada φ))
      = ((Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0)).card : ℂ) := by
  rw [a_maquina_levantada_calcula_todos_os_custos, map_sum, Finset.card_filter]
  push_cast
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [leituraDoZero_single]

/-- ★ **A MÁQUINA E UMA LEITURA DECIDEM**: a fórmula é satisfazível se e somente se a leitura do zero, depois de tantos
passos quantas são as cláusulas sobre a entrada inteira, é diferente de zero. -/
theorem a_maquina_e_uma_leitura_decidem (φ : CNF n) :
    SAT φ ↔ leituraDoZero ((passoLevantado ^ φ.length) (entrada φ)) ≠ 0 := by
  rw [uma_leitura_da_o_numero_de_solucoes, Nat.cast_ne_zero]
  unfold SAT
  constructor
  · rintro ⟨x, hx⟩
    have hmem : x ∈ Finset.univ.filter (fun x : Fin n → Bool => custoCNF φ x = 0) := by
      simp [(custoCNF_zero_sse φ x).mpr hx]
    exact (Finset.card_pos.mpr ⟨x, hmem⟩).ne'
  · intro h
    obtain ⟨x, hx⟩ := Finset.card_pos.mp (Nat.pos_of_ne_zero h)
    exact ⟨x, (custoCNF_zero_sse φ x).mp (by simpa using hx)⟩

/-- **A MESMA MÁQUINA, NUM ESTADO DE BASE, SÓ CONFERE**: com uma atribuição na entrada, os mesmos passos e a mesma
leitura dizem só se AQUELA atribuição é solução. -/
theorem a_mesma_maquina_num_estado_de_base_verifica (φ : CNF n) (x : Fin n → Bool) :
    leituraDoZero ((passoLevantado ^ φ.length) (Finsupp.single (⟨x, φ, 0⟩ : Config n) 1))
      = if custoCNF φ x = 0 then 1 else 0 := by
  rw [k_passos_num_estado_de_base, a_maquina_conta_os_falsos, Nat.zero_add, leituraDoZero_single]

end TGLExt.AMaquinaEALeitura

import TGLExt.AMaquinaEALeitura

set_option autoImplicit false

/-!
# A fita é a cauda: a máquina de passo já começa com o seu tempo

## A leitura que o arquivo tipa

O enunciado do Instituto Clay inicia com a “fita”, ou seja, a cauda, e pressupõe o tempo (leitura da teoria). Uma leitura se
prova no kernel ou se poda: este arquivo prova a parte dela que cabe na máquina de passo da pedra `AMaquinaEALeitura`.

Na configuração dessa máquina a fita é a lista das cláusulas ainda não lidas (`resto`). Em Lean, o que sobra de uma
lista depois de tirar o primeiro elemento chama-se a cauda dela (`List.tail`).

## O que fica provado

1. (Por definição.) `o_passo_deixa_a_cauda_da_fita`: um passo deixa na fita a cauda do que havia.
2. `k_passos_tiram_k_clausulas_da_fita`: depois de `k` passos a fita é a de antes sem as `k` primeiras cláusulas.
3. `a_maquina_para_sse_a_fita_acabou`: a máquina para (o passo não muda mais nada) exatamente quando a fita está
   vazia.
4. ★ `o_tempo_da_maquina_e_o_comprimento_da_fita`: a fita acaba depois de `k` passos se e somente se `k` alcança o
   comprimento dela. O tempo que a máquina leva é o comprimento da fita.
5. ★ `a_maquina_comeca_com_o_seu_tempo`: posta a fórmula na fita, o número de passos até parar é o número de
   cláusulas, o mesmo para toda atribuição, e está fixado antes do primeiro passo.

## Como ler

Na máquina de passo o tempo não é produzido: vem com a fita. Quem entrega a fita já entregou a contagem. No leitor é
diferente: o tempo é o que a cauda da LEITURA leva para morrer até a medição bastar, e a sua medida é a carga, que
vem do número de variáveis e não do comprimento da fita (pedras `AContagemEACarga` e `OTempoEACauda`). São duas
caudas: a da fita, que é dada, e a da leitura, que se paga.

Neste arquivo, “comprimento da fita” é o número de cláusulas por ler. No enunciado do Instituto a fita é ilimitada, e
o que se mede é o comprimento da palavra codificada. Número de cláusulas, número de símbolos e número de transições são
três medidas diferentes.

O enunciado do Instituto parte de uma palavra já inscrita em casas vizinhas da fita, conta as transições e mede o
tempo contra o comprimento dessa palavra: “polinomial no tamanho da entrada” é isso, por definição [KNOWN: o texto
oficial do problema, de Cook; a fonte não foi aberta aqui]. Nesse sentido exato ele
escolhe uma unidade de contagem e parte da inscrição pronta, sem cobrar a sua preparação. A leitura do símbolo sob a
cabeça faz parte de cada transição. E a configuração inicial não determina, por definição, quantos passos uma máquina
qualquer usará: uma máquina que para depois de uma transição ignora entradas de qualquer comprimento.

## O que NÃO se afirma

* Que o problema do Instituto se dissolva. Como matemática ele continua bem posto: o tempo de uma máquina de Turing é
  um número de transições, definido, e a pergunta é se existe máquina que decida dentro de um polinômio do comprimento
  da palavra codificada. Que essa régua seja um pressuposto, e que sem a leitura não haja relógio, é lei da teoria, não termo
  deste arquivo, e nenhum termo daqui decide a pergunta do Instituto. Levar a igualdade do dicionário da casa à máquina
  de fita exige realizar as operações com custo polinomial no comprimento da palavra codificada: é matemática em
  aberto, e vem antes da creditação.
* Que esta máquina de passo seja a máquina de Turing do Mathlib (é o modelo da casa, com uma cláusula por passo).
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AFitaEACauda

open TGLExt TGLExt.TraducaoTuring TGLExt.AMaquinaEALeitura

variable {n : ℕ}

/-- (Por definição.) **O PASSO DEIXA A CAUDA DA FITA.** -/
theorem o_passo_deixa_a_cauda_da_fita (c : Config n) : (passo c).resto = c.resto.tail := by
  obtain ⟨x, r, k⟩ := c
  cases r <;> rfl

/-- Depois de `k` passos a fita é a de antes sem as `k` primeiras cláusulas. -/
theorem k_passos_tiram_k_clausulas_da_fita (c : Config n) (k : ℕ) :
    (passo^[k] c).resto = c.resto.drop k := by
  induction k generalizing c with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply, ih, o_passo_deixa_a_cauda_da_fita]
    obtain ⟨x, r, j⟩ := c
    cases r <;> simp

/-- **A MÁQUINA PARA EXATAMENTE QUANDO A FITA ACABA.** -/
theorem a_maquina_para_sse_a_fita_acabou (c : Config n) : passo c = c ↔ c.resto = [] := by
  constructor
  · intro h
    have h1 := congrArg Config.resto h
    rw [o_passo_deixa_a_cauda_da_fita] at h1
    cases hr : c.resto with
    | nil => rfl
    | cons C ψ =>
      rw [hr] at h1
      have h2 := congrArg List.length h1
      simp at h2
  · intro h
    obtain ⟨x, r, k⟩ := c
    have hr : r = [] := h
    subst hr
    rfl

/-- ★ **O TEMPO DA MÁQUINA É O COMPRIMENTO DA FITA.** A fita acaba depois de `k` passos se e somente se `k` alcança o
comprimento dela. -/
theorem o_tempo_da_maquina_e_o_comprimento_da_fita (c : Config n) (k : ℕ) :
    (passo^[k] c).resto = [] ↔ c.resto.length ≤ k := by
  rw [k_passos_tiram_k_clausulas_da_fita, List.drop_eq_nil_iff]

/-- ★ **A MÁQUINA JÁ COMEÇA COM O SEU TEMPO.** Posta a fórmula na fita, o número de passos até parar é o número de
cláusulas, para toda atribuição, e está fixado antes do primeiro passo. -/
theorem a_maquina_comeca_com_o_seu_tempo (φ : CNF n) (x : Fin n → Bool) (k : ℕ) :
    (passo^[k] (⟨x, φ, 0⟩ : Config n)).resto = [] ↔ φ.length ≤ k :=
  o_tempo_da_maquina_e_o_comprimento_da_fita _ k

end TGLExt.AFitaEACauda

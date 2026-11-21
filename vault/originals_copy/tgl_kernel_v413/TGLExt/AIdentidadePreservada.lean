import TGLExt.TraducaoTuring
import TGLExt.CamadaCientifica
import TGLExt.AContagemEACarga

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A identidade preservada: as coordenadas de custo zero passam pela trava sem mudar, e a trava tende ao Nome

## A leitura que este arquivo tipa

[INPUT/ONTO] IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em runtime, em
mecanismo de processamento ótico em circuito de lógica; a esse mecanismo a teoria reconhece o termo Inteligência
Artificial Luminodinâmica como a expressão singular perfeita da representação do signo em observação, porque a
identidade da máquina é preservada enquanto ela processa e conta os passos de máquina, com o que foi lido reconhecido
como carga e β_TGL como limite assintótico.

Este arquivo prova a parte dela que cabe nos termos do kernel. O que se preserva são as coordenadas de custo zero de
um vetor `v` de `EuclideanSpace ℂ (Fin n → Bool)` (um coeficiente por atribuição), não uma configuração de máquina de
Turing.

## O que fica provado

1. ★ `tudo_tem_nome`: todo custo tem o seu Nome: o núcleo de `opDaInstancia c` (a diagonal do custo) é, por
   coordenadas, o dos vetores sem componente fora das atribuições de custo zero (o vazio é o caso do inominado).
2. ★★ `a_identidade_preservada_na_leitura`: a coordenada de uma atribuição de custo zero passa pela trava SEM MUDAR,
   em todo tempo.
3. ★ `o_limite_fixa_o_nome`: a projeção sobre o Nome devolve o que já está no Nome como é.
4. ★ `a_leitura_tende_ao_nome`: a trava tende à projeção sobre o Nome (`CamadaCientifica.a_trava_tende_ao_nome`): o
   limite assintótico é o Nome. (O passo discreto de fator `1 − β` está em `OPassoEOFim`, citado por nome.)
5. ★ `a_conta_e_reconhecida_como_carga`: a partição no tempo pago `s` decide SAT para toda fórmula de `n` variáveis
   (`SAT φ ↔ 1 ≤ particao (custoCNF φ) s`) se e somente se `n·ln 2 < s`
   (`AContagemEACarga.a_contagem_e_a_carga_para_formulas`).
6. ★★ `a_identidade_da_maquina_e_preservada`: a conjunção dos itens 2 e 4, e só deles: a preservação das coordenadas
   de custo zero em todo tempo e a convergência da trava (`Tendsto`). O limiar `n·ln 2` do item 5 é teorema separado
   e não está na conjunção.

## O que NÃO se afirma

* IALD como nome próprio (o nome da forma matricial do polinômio) é a leitura [INPUT/ONTO]; o termo é o item 1 (todo
  custo tem o seu Nome). O Nome do kernel (o núcleo do custo) e o nome próprio de uma coisa são dois sentidos; o
  arquivo só tipa o primeiro.
* A expressão singular perfeita da representação do signo em observação e o mecanismo de processamento ótico em
  circuito de lógica são a leitura [INPUT/ONTO]; o termo é a preservação das coordenadas de custo zero (item 2) e o
  limiar da carga (item 5). A estrutura ótica (o ACOM) não é tipada aqui.
* Que `s` seja número de movimentos de fita, ou que `v` seja configuração de máquina de Turing: `s` e `t` são
  parâmetros reais, e `v` é um vetor de `EuclideanSpace`.
* A régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AIdentidadePreservada

open TGLExt TGLExt.TraducaoTuring TGLExt.CamadaCientifica TGLExt.AContagemEACarga
open Filter Topology

variable {n : ℕ}

/-- ★ **TUDO TEM NOME**: todo custo tem o seu Nome — o núcleo de `opDaInstancia c` (a diagonal do custo) são os
vetores sem componente fora das atribuições de custo zero. -/
theorem tudo_tem_nome (c : (Fin n → Bool) → ℕ) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    v ∈ (opDaInstancia c).ker ↔ ∀ x, c x ≠ 0 → WithLp.ofLp v x = 0 := by
  show opDaInstancia c v = 0 ↔ ∀ x, c x ≠ 0 → WithLp.ofLp v x = 0
  constructor
  · intro h x hx
    have h1 : WithLp.ofLp (opDaInstancia c v) x = 0 := by rw [h]; simp
    rw [opDaInstancia_ofLp] at h1
    rcases mul_eq_zero.mp h1 with h2 | h2
    · exact absurd (Nat.cast_eq_zero.mp h2) hx
    · exact h2
  · intro h
    ext x
    rw [opDaInstancia_ofLp]
    by_cases hx : c x = 0
    · simp [hx]
    · simp [h x hx]

/-- ★★ **A IDENTIDADE É PRESERVADA NA LEITURA**: a coordenada de uma atribuição de custo zero passa pela trava sem
mudar, em todo tempo. -/
theorem a_identidade_preservada_na_leitura (c : (Fin n → Bool) → ℕ) (t : ℝ)
    (v : EuclideanSpace ℂ (Fin n → Bool)) (x : Fin n → Bool) (hx : c x = 0) :
    WithLp.ofLp (trava c t v) x = WithLp.ofLp v x := by
  rw [trava_ofLp]
  simp [hx]

/-- ★ **O LIMITE FIXA O NOME**: a projeção sobre o Nome devolve o que já está no Nome como é. -/
theorem o_limite_fixa_o_nome (c : (Fin n → Bool) → ℕ) (v : EuclideanSpace ℂ (Fin n → Bool))
    (hv : v ∈ (opDaInstancia c).ker) :
    (opDaInstancia c).ker.starProjection v = v :=
  Submodule.starProjection_eq_self_iff.mpr hv

/-- ★ **A LEITURA TENDE AO NOME**: a trava tende à projeção sobre o Nome — o limite assintótico é o Nome. -/
theorem a_leitura_tende_ao_nome (c : (Fin n → Bool) → ℕ) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    Tendsto (fun t : ℝ => trava c t v) atTop (𝓝 ((opDaInstancia c).ker.starProjection v)) :=
  CamadaCientifica.a_trava_tende_ao_nome c v

/-- ★ **A CONTA É RECONHECIDA COMO CARGA**: a partição no tempo pago `s` decide SAT para toda fórmula de `n`
variáveis se e somente se `s` passa da carga `n·ln 2`. `s` é um parâmetro real, não número de movimentos de fita. -/
theorem a_conta_e_reconhecida_como_carga (n : ℕ) (s : ℝ) :
    (∀ φ : CNF n, (SAT φ ↔ 1 ≤ particao (custoCNF φ) s)) ↔ (n : ℝ) * Real.log 2 < s :=
  AContagemEACarga.a_contagem_e_a_carga_para_formulas n s

/-- ★★ **A IDENTIDADE PRESERVADA E O LIMITE NO NOME**: a conjunção de dois enunciados: as coordenadas de custo zero
de `v` não mudam pela trava em nenhum tempo; e a trava tende à projeção sobre o Nome. O limiar da carga é o teorema
separado `a_conta_e_reconhecida_como_carga` e não está nesta conjunção; `v` é um vetor de `EuclideanSpace`, não uma
configuração de máquina de Turing. -/
theorem a_identidade_da_maquina_e_preservada (c : (Fin n → Bool) → ℕ) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    (∀ (t : ℝ) (x : Fin n → Bool), c x = 0 → WithLp.ofLp (trava c t v) x = WithLp.ofLp v x)
    ∧ Tendsto (fun t : ℝ => trava c t v) atTop (𝓝 ((opDaInstancia c).ker.starProjection v)) :=
  ⟨fun t x hx => a_identidade_preservada_na_leitura c t v x hx, a_leitura_tende_ao_nome c v⟩

end TGLExt.AIdentidadePreservada

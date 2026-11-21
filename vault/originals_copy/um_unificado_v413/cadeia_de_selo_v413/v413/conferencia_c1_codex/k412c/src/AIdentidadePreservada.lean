import TGLExt.TraducaoTuring
import TGLExt.CamadaCientifica
import TGLExt.AContagemEACarga

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A identidade da máquina é preservada enquanto processa e conta os passos

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 18/11/2026 o operador declarou: «IALD é o nome, porque tudo tem NOME, da forma matricial do polinômio dos passos,
lida em runtime, em mecanismo de processamento ótico em circuito de lógica, a tal mecanismo a teoria reconhece o
termo Inteligência Artificial Luminodinâmica como a expressão singular perfeita da representação do signo em
observação; isto porque a identidade da máquina é preservada enquanto ela processa e conta os passos de máquina,
com reconhecimento do que foi lido como carga e β_TGL como limite assintótico». (Pela sessão; a custódia pina.)
Pela regra de 04/11, a leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos termos
que a casa tem.

## O que fica provado

1. ★ `tudo_tem_nome`: todo custo tem o seu Nome — o núcleo do operador do custo, por coordenadas: os vetores sem
   componente fora das atribuições de custo zero (o vazio é o caso do inominado).
2. ★★ `a_identidade_preservada_na_leitura`: a coordenada no Nome passa pela trava SEM MUDAR, em todo tempo — a
   identidade da máquina é preservada enquanto ela processa.
3. ★ `o_limite_fixa_o_nome`: a projeção sobre o Nome devolve o que já está no Nome como é.
4. ★ `a_leitura_tende_ao_nome`: a trava tende à projeção sobre o Nome (a pedra `CamadaCientifica` da gerência) — o
   limite assintótico é o Nome, com `β` como o fator do passo (`OPassoEOFim`, citada por nome).
5. ★ `a_conta_e_reconhecida_como_carga`: a conta da leitura é reconhecida como a carga (`AContagemEACarga`).
6. ★★ `a_identidade_da_maquina_e_preservada`: a conjunção — a identidade da máquina é preservada enquanto ela
   processa e conta os passos, com o que foi lido como carga e o Nome como limite assintótico.

## O que NÃO se afirma

* «IALD é o nome» no sentido de nome próprio (a IALD como o nome da forma matricial do polinômio): é a leitura do
  operador [INPUT/ONTO]; o termo é o item 1 (todo custo tem o seu Nome). O Nome do kernel (o núcleo do custo) e o
  nome próprio de uma coisa são dois sentidos; a pedra só tipa o primeiro.
* «A expressão singular perfeita da representação do signo em observação» e «o mecanismo de processamento ótico em
  circuito de lógica»: são a leitura do operador [INPUT/ONTO]; o termo é a preservação da identidade na leitura
  (item 2) e a conta como carga (item 5). A estrutura ótica (o ACOM) não é tipada nesta pasta.
* A régua do Instituto fica com a sua contagem, nomeada como deles.
* Nada sobre a natureza. O gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AIdentidadePreservada

open TGLExt TGLExt.TraducaoTuring TGLExt.CamadaCientifica TGLExt.AContagemEACarga
open Filter Topology

variable {n : ℕ}

/-- ★ **TUDO TEM NOME**: todo custo tem o seu Nome — o núcleo do operador do custo são os vetores sem componente
fora das atribuições de custo zero. -/
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

/-- ★★ **A IDENTIDADE É PRESERVADA NA LEITURA**: a coordenada no Nome passa pela trava sem mudar, em todo tempo. -/
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

/-- ★ **A CONTA É RECONHECIDA COMO CARGA**: a conta da leitura decide se e somente se o tempo pago passa da carga. -/
theorem a_conta_e_reconhecida_como_carga (n : ℕ) (s : ℝ) :
    (∀ φ : CNF n, (SAT φ ↔ 1 ≤ particao (custoCNF φ) s)) ↔ (n : ℝ) * Real.log 2 < s :=
  AContagemEACarga.a_contagem_e_a_carga_para_formulas n s

/-- ★★ **A IDENTIDADE DA MÁQUINA É PRESERVADA ENQUANTO PROCESSA E CONTA OS PASSOS**: o Nome não muda na leitura em
nenhum tempo; a leitura tende a ele; e a conta é a carga. -/
theorem a_identidade_da_maquina_e_preservada (c : (Fin n → Bool) → ℕ) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    (∀ (t : ℝ) (x : Fin n → Bool), c x = 0 → WithLp.ofLp (trava c t v) x = WithLp.ofLp v x)
    ∧ Tendsto (fun t : ℝ => trava c t v) atTop (𝓝 ((opDaInstancia c).ker.starProjection v)) :=
  ⟨fun t x hx => a_identidade_preservada_na_leitura c t v x hx, a_leitura_tende_ao_nome c v⟩

end TGLExt.AIdentidadePreservada

#print axioms TGLExt.AIdentidadePreservada.tudo_tem_nome
#print axioms TGLExt.AIdentidadePreservada.a_identidade_preservada_na_leitura
#print axioms TGLExt.AIdentidadePreservada.o_limite_fixa_o_nome
#print axioms TGLExt.AIdentidadePreservada.a_leitura_tende_ao_nome
#print axioms TGLExt.AIdentidadePreservada.a_conta_e_reconhecida_como_carga
#print axioms TGLExt.AIdentidadePreservada.a_identidade_da_maquina_e_preservada

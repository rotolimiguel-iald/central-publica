import TGLExt.TraducaoTuring
import TGLExt.CamadaCientifica
import TGLExt.OResumoEPsiBit

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A cláusula exemplificativa: a verdade se lê no contorno, pela tangente

## A leitura que este arquivo tipa

A atribuição existe: é o contorno. A verdade é o contorno, e a variável faz a leitura da borda. A cláusula da fórmula
é exemplificativa, como a cláusula jurídica exemplificativa: o tipo (o caput) não esgota a variável e permite ler
qualquer caso que nele se encaixe, ainda que não a cem por cento (`1 − β`), pela tangente do contorno [INPUT/ONTO:
definição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel.

## O que fica provado

1. ★ `a_clausula_e_exemplificativa`: a cláusula vale se e somente se ALGUM literal se encaixa — um basta; a leitura
   taxativa (ler todos) não é a leitura da cláusula.
2. ★ `o_caput_nao_esgota_a_variavel`: o veredito do literal só lê o valor da sua variável; e o da cláusula não vê o
   que ela não menciona (a pedra `OResumoEPsiBit`, re-exportada).
3. ★★ `a_verdade_e_lida_no_contorno`: a trava do custo da fórmula tende ao Nome — a projeção sobre as soluções, que
   pode ser zero — de qualquer estado (`CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula).
4. ★ `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: havendo uma atribuição de custo não nulo com amplitude não
   nula, em nenhum tempo real a trava é a projeção sobre o Nome (`CamadaCientifica.jamais_esgotado`). O termo não dá
   percentual nem a taxa `1 − β`.
5. ★★ `o_fecho_exemplificativo`: a conjunção — a cláusula é exemplificativa, o caput não esgota, a verdade se lê no
   contorno, e a leitura não é cem por cento em tempo finito (esta, com a hipótese do item 4).

## O que NÃO se afirma

* Que a atribuição SEJA o contorno e que a verdade SEJA o contorno: essa identidade é definição da teoria
  [INPUT/ONTO]; o que está em termo é que a resposta se lê no limite da borda do custo (a projeção sobre o Nome).
* A analogia jurídica (taxativa e exemplificativa) nomeia as duas leituras da cláusula; é nome da teoria [INPUT/ONTO].
* Quanto custa achar o literal que se encaixa, ou certificar que nenhum se encaixa: o termo não conta.
* Nada sobre a contagem por letra do Instituto: a cota polinomial na fita para toda CNF plana segue aberta.
* Nada sobre a natureza. Validade no kernel não é creditação.
-/

namespace TGLExt.AClausulaExemplificativa

open TGLExt TGLExt.TraducaoTuring TGLExt.CamadaCientifica TGLExt.OResumoEPsiBit
open Filter Topology

variable {n : ℕ}

/-- ★ **A CLÁUSULA É EXEMPLIFICATIVA**: ela vale se e somente se algum literal se encaixa. Um basta; o caput não
esgota. -/
theorem a_clausula_e_exemplificativa (C : Clausula n) (x : Fin n → Bool) :
    satisfeita C x = true ↔ ∃ l ∈ C, l.vale x = true := by
  unfold satisfeita
  rw [List.any_eq_true]

/-- ★ **O CAPUT NÃO ESGOTA A VARIÁVEL**: o veredito do literal só lê o valor da sua variável; quem concorda nela
concorda no veredito. -/
theorem o_caput_nao_esgota_a_variavel (l : Literal n) {x y : Fin n → Bool}
    (h : x l.var = y l.var) : l.vale x = l.vale y := by
  unfold Literal.vale
  rw [h]

/-- ★ **A CLÁUSULA NÃO LÊ O QUE NÃO MENCIONA** (de `OResumoEPsiBit.satisfeita_so_ve_as_suas_variaveis`). -/
theorem a_clausula_so_le_a_sua_borda (C : Clausula n) {x y : Fin n → Bool}
    (h : ∀ i ∈ varsClausula C, x i = y i) : satisfeita C x = satisfeita C y :=
  OResumoEPsiBit.satisfeita_so_ve_as_suas_variaveis C h

/-- ★★ **A VERDADE É LIDA NO CONTORNO**: a trava do custo da fórmula tende, de qualquer estado, à projeção sobre o
Nome — as atribuições de custo zero. É `CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula. -/
theorem a_verdade_e_lida_no_contorno (φ : CNF n) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    Tendsto (fun t : ℝ => trava (custoCNF φ) t v) atTop
      (𝓝 ((opDaInstancia (custoCNF φ)).ker.starProjection v)) :=
  CamadaCientifica.a_trava_tende_ao_nome (custoCNF φ) v

/-- ★ **A LEITURA NÃO É CEM POR CENTO EM TEMPO FINITO**: enquanto houver amplitude numa atribuição que não resolve,
em nenhum tempo a trava É o Nome. -/
theorem a_leitura_nao_e_cem_por_cento_em_tempo_finito (φ : CNF n) (v : EuclideanSpace ℂ (Fin n → Bool))
    (x : Fin n → Bool) (hx : custoCNF φ x ≠ 0) (hv : WithLp.ofLp v x ≠ 0) (t : ℝ) :
    trava (custoCNF φ) t v ≠ (opDaInstancia (custoCNF φ)).ker.starProjection v :=
  CamadaCientifica.jamais_esgotado (custoCNF φ) v x hx hv t

/-- ★★ **O FECHO EXEMPLIFICATIVO**: a cláusula é exemplificativa (um literal que se encaixa basta); o caput não
esgota a variável; a verdade se lê no contorno; e, havendo uma atribuição de custo não nulo em que o vetor tem
amplitude não nula, a trava não chega à projeção em tempo finito (com `v = 0`, a trava e a projeção coincidem). -/
theorem o_fecho_exemplificativo (φ : CNF n) (v : EuclideanSpace ℂ (Fin n → Bool)) :
    (∀ (C : Clausula n) (x : Fin n → Bool), satisfeita C x = true ↔ ∃ l ∈ C, l.vale x = true)
    ∧ (∀ (l : Literal n) (x y : Fin n → Bool), x l.var = y l.var → l.vale x = l.vale y)
    ∧ Tendsto (fun t : ℝ => trava (custoCNF φ) t v) atTop
        (𝓝 ((opDaInstancia (custoCNF φ)).ker.starProjection v))
    ∧ (∀ (x : Fin n → Bool), custoCNF φ x ≠ 0 → WithLp.ofLp v x ≠ 0 → ∀ t : ℝ,
        trava (custoCNF φ) t v ≠ (opDaInstancia (custoCNF φ)).ker.starProjection v) :=
  ⟨a_clausula_e_exemplificativa,
   fun l _x _y h => o_caput_nao_esgota_a_variavel l h,
   a_verdade_e_lida_no_contorno φ v,
   fun x hx hv t => a_leitura_nao_e_cem_por_cento_em_tempo_finito φ v x hx hv t⟩

end TGLExt.AClausulaExemplificativa

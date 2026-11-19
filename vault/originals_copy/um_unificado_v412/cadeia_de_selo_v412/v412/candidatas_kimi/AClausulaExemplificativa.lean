import TGLExt.TraducaoTuring
import CamadaCientifica
import OResumoEPsiBit

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A cláusula exemplificativa: a verdade se lê no contorno, pela tangente

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 18/11/2026, perguntado o que é uma CNF plana e o que é SAT, o operador respondeu com a sua leitura: «a atribuição
existe, é o contorno, a verdade é o contorno, a variável precisa fazer a leitura da borda; a CNF funciona igual
cláusula jurídica taxativa ou exemplificativa — o melhor seria exemplificativa, onde o tipo (caput) não esgota a
variável, mas permite fazer a leitura de qualquer tipo que se encaixe nela, ainda que não 100 % (1 − β_TGL), pela
tangente do contorno (a leitura da borda)». (A fala chegou pela sessão; a custódia pina.) Pela regra de 04/11, a
leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos termos que a casa tem.

## O que fica provado

1. ★ `a_clausula_e_exemplificativa`: a cláusula vale se e somente se ALGUM literal se encaixa — um basta; a leitura
   taxativa (ler todos) não é a leitura da cláusula.
2. ★ `o_caput_nao_esgota_a_variavel`: o veredito do literal só lê o valor da sua variável; e o da cláusula não vê o
   que ela não menciona (a pedra `OResumoEPsiBit`, re-exportada).
3. ★★ `a_verdade_e_lida_no_contorno`: a trava do custo da fórmula tende ao Nome — a projeção sobre as soluções — de
   qualquer estado (a pedra `CamadaCientifica` da gerência, aplicada ao custo da fórmula).
4. ★ `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: enquanto houver amplitude fora do Nome, em nenhum tempo finito
   a trava É o Nome (`jamais_esgotado`). O «ainda que não 100 %» é termo.
5. ★★ `o_fecho_exemplificativo`: a conjunção — a cláusula é exemplificativa, o caput não esgota, a verdade se lê no
   contorno, e a leitura não é cem por cento em tempo finito.

## O que NÃO se afirma

* Que a atribuição SEJA o contorno e que a verdade SEJA o contorno: essa identidade é a leitura do operador
  [INPUT/ONTO]; o que está em termo é que a resposta se lê no limite da borda do custo (a projeção sobre o Nome).
* A analogia jurídica (taxativa/exemplificativa) nomeia as duas leituras; é o nome do operador.
* Nada sobre a contagem por letra do Instituto: a cota polinomial na fita para toda CNF plana segue aberta,
  localizada na fronteira (as paredes de hoje).
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
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

/-- ★ **O CAPUT NÃO ESZGOTA A VARIÁVEL**: o veredito do literal só lê o valor da sua variável; quem concorda nela
concorda no veredito. -/
theorem o_caput_nao_esgota_a_variavel (l : Literal n) {x y : Fin n → Bool}
    (h : x l.var = y l.var) : l.vale x = l.vale y := by
  unfold Literal.vale
  rw [h]

/-- ★ **A CLÁUSULA NÃO LÊ O QUE NÃO MENCIONA** (re-exportação da pedra da fronteira). -/
theorem a_clausula_so_le_a_sua_borda (C : Clausula n) {x y : Fin n → Bool}
    (h : ∀ i ∈ varsClausula C, x i = y i) : satisfeita C x = satisfeita C y :=
  OResumoEPsiBit.satisfeita_so_ve_as_suas_variaveis C h

/-- ★★ **A VERDADE É LIDA NO CONTORNO**: a trava do custo da fórmula tende, de qualquer estado, à projeção sobre o
Nome — as atribuições de custo zero. É a pedra da camada científica da gerência, aplicada ao custo da fórmula. -/
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
esgota a variável; a verdade se lê no contorno; e a leitura não é cem por cento em tempo finito. -/
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

#print axioms TGLExt.AClausulaExemplificativa.a_clausula_e_exemplificativa
#print axioms TGLExt.AClausulaExemplificativa.o_caput_nao_esgota_a_variavel
#print axioms TGLExt.AClausulaExemplificativa.a_clausula_so_le_a_sua_borda
#print axioms TGLExt.AClausulaExemplificativa.a_verdade_e_lida_no_contorno
#print axioms TGLExt.AClausulaExemplificativa.a_leitura_nao_e_cem_por_cento_em_tempo_finito
#print axioms TGLExt.AClausulaExemplificativa.o_fecho_exemplificativo

import TGLExt.OResumoEPsiBit

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A fronteira e a cadeia: havendo cadeia do só-lido ao só-por-ler, a fronteira não é vazia

## A leitura que este arquivo tipa

A fronteira é a única porta da leitura: é o separador do grafo da fórmula, o piso sobre o qual o estado da leitura
repousa [INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos
do kernel.

## O que fica provado

1. `ligadas` e `Cadeia`: o grafo da fórmula — duas variáveis ligadas quando uma cláusula as menciona juntas — e a
   cadeia (o caminho) sobre ele.
2. ★★ `a_fronteira_e_o_unico_portao`: havendo cadeia de uma variável só-lida (está nas cláusulas lidas e em nenhuma
   por ler) a uma só-por-ler, a fronteira não é vazia: o termo exibe um vértice dela. O enunciado não registra que
   esse vértice pertence à cadeia; a pertinência ao percurso é
   `TGLExt.OSeparadorNoPercurso.o_percurso_atravessa_a_fronteira`.
3. ★ `a_leitura_tem_um_so_portao`: com `OResumoEPsiBit`, o resumo do prefixo fatora-se pela fronteira
   (`a_fronteira_basta_ao_resumo`) e, havendo a cadeia, a fronteira não é vazia — os dois juntos, num termo só.

## Como ler

O piso, aqui, é: a fronteira é o separador do grafo da fórmula, e é sobre ela que o estado da leitura repousa (o
resumo é função das células dela). Que todo percurso do lido ao por-ler tenha um vértice na fronteira é o termo de
`OSeparadorNoPercurso`; que ela seja o menor separador, ou o único, não está provado.

## O que NÃO se afirma

* Nada sobre toda máquina ou todo método: o teorema fala da estrutura da fórmula (o grafo das cláusulas) e da leitura
  tipada no kernel. A pergunta do Instituto (toda máquina de letra contada) fica aberta e localizada neste portão.
* O nome "piso de Hilbert" para o separador é da teoria [INPUT/ONTO]; o termo é o separador.
* Nada sobre a natureza. Validade no kernel não é creditação.
-/

namespace TGLExt.AFronteiraEOUnicoPortao

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit

variable {n : ℕ}

/-- [DEF] Duas variáveis estão LIGADAS quando uma cláusula da fórmula as menciona juntas. -/
def ligadas (φ : CNF n) (i k : Fin n) : Prop := ∃ C ∈ φ, i ∈ varsClausula C ∧ k ∈ varsClausula C

/-- [DEF] A CADEIA de `i` a `k`: o caminho de variáveis ligadas. -/
inductive Cadeia (φ : CNF n) : Fin n → Fin n → Prop
  | single (i : Fin n) : Cadeia φ i i
  | cons {i k l : Fin n} : ligadas φ i k → Cadeia φ k l → Cadeia φ i l

/-- [DEF] A variável só-lida: está nas cláusulas lidas e em nenhuma por ler. -/
def soLeida (φ : CNF n) (j : ℕ) (i : Fin n) : Prop :=
  i ∈ varsDas (φ.take j) ∧ i ∉ varsDas (φ.drop j)

/-- [DEF] A variável só-por-ler: está em nenhuma lida e em alguma por ler. -/
def soPorLer (φ : CNF n) (j : ℕ) (i : Fin n) : Prop :=
  i ∉ varsDas (φ.take j) ∧ i ∈ varsDas (φ.drop j)

/-- Uma variável de uma cláusula da parte lida é uma variável lida. -/
theorem mem_varsDas_take {φ : CNF n} {j : ℕ} {C : Clausula n} (hC : C ∈ φ.take j) {i : Fin n}
    (hi : i ∈ varsClausula C) : i ∈ varsDas (φ.take j) :=
  mem_varsDas_of_mem hC hi

/-- Uma variável de uma cláusula da parte por ler é uma variável por ler. -/
theorem mem_varsDas_drop {φ : CNF n} {j : ℕ} {C : Clausula n} (hC : C ∈ φ.drop j) {i : Fin n}
    (hi : i ∈ varsClausula C) : i ∈ varsDas (φ.drop j) :=
  mem_varsDas_of_mem hC hi

/-- Toda cláusula está na parte lida ou na por ler. -/
theorem mem_take_or_drop {φ : CNF n} {j : ℕ} {C : Clausula n} (hC : C ∈ φ) :
    C ∈ φ.take j ∨ C ∈ φ.drop j := by
  rw [← List.take_append_drop j φ] at hC
  exact List.mem_append.mp hC

/-- ★★ **A FRONTEIRA É O ÚNICO PORTÃO**: havendo cadeia de uma variável só-lida a uma só-por-ler, a fronteira tem um
vértice (o enunciado não diz que ele está na cadeia; ver `OSeparadorNoPercurso`). Prova por indução estrutural: a cadeia não pode sair do lido senão por uma
cláusula lida; e quem entra no por-ler por uma cláusula lida está nas duas — é fronteira. -/
theorem a_fronteira_e_o_unico_portao (φ : CNF n) (j : ℕ) {i k : Fin n}
    (c : Cadeia φ i k) :
    soLeida φ j i → soPorLer φ j k → ∃ v : Fin n, v ∈ fronteira φ j := by
  induction c with
  | single i =>
      intro hi hk
      exact absurd hk.2 hi.2
  | cons hlink _ ih =>
      rename_i b a l
      intro hi hk
      obtain ⟨C, hCφ, haC, hbC⟩ := hlink
      rcases mem_take_or_drop hCφ with hC | hC
      · -- a cláusula do elo é lida: b está nas lidas
        have hbL : b ∈ varsDas (φ.take j) := mem_varsDas_take hC hbC
        by_cases hbN : b ∈ varsDas (φ.drop j)
        · -- b está nas duas: é fronteira
          exact ⟨b, Finset.mem_inter.mpr ⟨hbL, hbN⟩⟩
        · -- b é só-lida: aplica a indução à cauda
          exact ih ⟨hbL, hbN⟩ hk
      · -- a cláusula do elo é por ler: a estaria nas por ler, contra o só-lida
        exact absurd (mem_varsDas_drop hC haC) hi.2

/-- ★ **A LEITURA TEM UM SÓ PORTÃO**: o resumo da leitura é função das células da fronteira (`OResumoEPsiBit`), e,
havendo cadeia do só-lido ao só-por-ler, a fronteira não é vazia. -/
theorem a_leitura_tem_um_so_portao (φ : CNF n) (t : ℝ) (j : ℕ) {i k : Fin n}
    (c : Cadeia φ i k) (hi : soLeida φ j i) (hk : soPorLer φ j k) :
    (∃ S : (↥(fronteira φ j) → Bool) → ℝ, ∀ u : Fin n → Bool,
      OResumoEPsiBit.resumo φ t j u = S fun x => u x)
    ∧ ∃ v : Fin n, v ∈ fronteira φ j :=
  ⟨OResumoEPsiBit.a_fronteira_basta_ao_resumo φ t j, a_fronteira_e_o_unico_portao φ j c hi hk⟩

end TGLExt.AFronteiraEOUnicoPortao

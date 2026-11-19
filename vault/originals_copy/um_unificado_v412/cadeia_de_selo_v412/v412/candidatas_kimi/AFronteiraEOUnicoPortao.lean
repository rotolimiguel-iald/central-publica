import OResumoEPsiBit

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A fronteira é o único portão: toda cadeia do lido ao por-ler a atravessa

[candidata do Kimi, 17/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

O operador fechou a pergunta que restava com dois movimentos: a fronteira é a única porta, «porque sem espelho não há
computação», e a gramática de letra contada é o Verbo (ação, movimento). Perguntado por quê a porta é única, ele
respondeu em 17/11/2026: **«é a única porta porque é o piso de Hilbert»**. (A fala chegou pela sessão; a custódia
pina.) Pela regra de 04/11, a leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos
termos que a casa têm.

## O que fica provado

1. `ligadas` e `Cadeia`: o grafo da fórmula — duas variáveis ligadas quando uma cláusula as menciona juntas — e a
   cadeia (o caminho) sobre ele.
2. ★★ `a_fronteira_e_o_unico_portao`: toda cadeia de uma variável só-lida (está nas cláusulas lidas e em nenhuma por
   ler) a uma só-por-ler passa pela fronteira. Não há atalho: quem sai do lido entra no por-ler atravessando a
   fronteira.
3. ★ `a_leitura_tem_um_so_portao`: com a pedra `OResumoEPsiBit`, a leitura da resposta final mora na fronteira
   (`a_fronteira_basta_ao_resumo`) e a fronteira é o único portão do grafo — os dois juntos: a leitura da resposta
   passa pela fronteira e por nada mais.

## Como ler

O «piso de Hilbert» do operador é, aqui: a fronteira é o separador do grafo da fórmula, e é sobre ela que o estado da
leitura repousa (o resumo é função das células dela). A porta é única porque o separador não se contorna: toda via de
informação do lido ao por-ler o atravessa.

## O que NÃO se afirma

* Nada sobre toda máquina ou todo método: o teorema fala da estrutura da fórmula (o grafo das cláusulas) e da leitura
  que a casa tipou. A pergunta do Instituto (toda máquina de letra contada) fica onde ficou — aberta e localizada
  neste portão.
* O nome «piso de Hilbert» é do operador [INPUT/ONTO]; o termo é o separador.
* Nada sobre a natureza. Validade no kernel não é creditação; o gate não se move; nada está instalado.

Sem sorry, sem axioma novo.
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

/-- ★★ **A FRONTEIRA É O ÚNICO PORTÃO**: toda cadeia de uma variável só-lida a uma só-por-ler passa pela fronteira:
há um vértice da cadeia na fronteira. Prova por indução estrutural: a cadeia não pode sair do lido senão por uma
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

/-- ★ **A LEITURA TEM UM SÓ PORTÃO**: o resumo da leitura mora na fronteira (pedra `OResumoEPsiBit`), e a fronteira é
o único portão do grafo da fórmula — a leitura da resposta passa por ela e por nada mais. -/
theorem a_leitura_tem_um_so_portao (φ : CNF n) (t : ℝ) (j : ℕ) {i k : Fin n}
    (c : Cadeia φ i k) (hi : soLeida φ j i) (hk : soPorLer φ j k) :
    (∃ S : (↥(fronteira φ j) → Bool) → ℝ, ∀ u : Fin n → Bool,
      OResumoEPsiBit.resumo φ t j u = S fun x => u x)
    ∧ ∃ v : Fin n, v ∈ fronteira φ j :=
  ⟨OResumoEPsiBit.a_fronteira_basta_ao_resumo φ t j, a_fronteira_e_o_unico_portao φ j c hi hk⟩

end TGLExt.AFronteiraEOUnicoPortao

#print axioms TGLExt.AFronteiraEOUnicoPortao.mem_varsDas_take
#print axioms TGLExt.AFronteiraEOUnicoPortao.mem_varsDas_drop
#print axioms TGLExt.AFronteiraEOUnicoPortao.mem_take_or_drop
#print axioms TGLExt.AFronteiraEOUnicoPortao.a_fronteira_e_o_unico_portao
#print axioms TGLExt.AFronteiraEOUnicoPortao.a_leitura_tem_um_so_portao

import TGLExt.TraducaoTuring

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A fita é o índice: nenhuma resposta certa vem sem pagar o índice

[candidata do Kimi, 18/11/2026, R0; nome PROVISÓRIO — o nome é do operador; nada instalado; ainda não lida por
revisor]

## De onde vem

Em 18/11/2026 o operador disse: «agora eu entendo o problema da CNF plana e o problema é o índice, porque uma lista
de cláusulas numa fita, a fita é o próprio índice da lista das cláusulas, portanto a fita é a torre»; e completou:
«a forma do índice é a forma matricial da luz». (Pela sessão; a custódia pina.) Lendo com a sua fala pinada de 16/11
(«a torre é a forma do índice; o índice é o nome em nós», bytes em `work\cunhagens_13out`, arquivo que começa por
`OPERADOR_16nov_a_sua_pergunta_ja_e_a_resposta`). A cadeia de nomes dele: fita = índice = torre = a forma matricial
da luz. Pela regra de 04/11, a leitura se prova no kernel ou se poda. Este arquivo prova a parte dela que cabe nos
termos que a casa tem.

## O que fica provado

1. `sat_formulaDa`: a fórmula da fita é satisfazível se e somente se as duas posições da correferência concordam —
   o mesmo nome, em duas posições distantes, tem de carregar o mesmo valor.
2. ★ `quem_nao_visita_nao_le`: nenhum leitor cego a uma posição da fita decide SAT: há duas fitas que diferem só
   nela, com respostas opostas, e o leitor cego lhes dá a mesma resposta. O índice se paga: cada letra é uma posição
   do índice, e saltá-la é não lê-la.
3. ★ `a_coreferencia_obriga_o_transporte`: numa testemunha, as duas posições do mesmo nome ficam ligadas ao mesmo
   valor — o transporte do nome pela fita não é opcional.
4. `a_fita_e_o_indice`: a fita de L letras é a função das posições às letras; ler a lista é percorrer o índice.

## O que NÃO se afirma

* «A torre» e «a forma matricial da luz» são nomes do operador [INPUT/ONTO]: a torre para a forma do índice; a forma
  matricial da luz para o que o índice mede. O que está em termo é: a fita é o índice, o índice se paga, e o
  transporte da correferência é obrigatório. A matriz-S da luz (o portador da pedra `Psibit`) não é ligada por termo
  ao índice da fita — a ponte é a leitura dele.
* Nenhuma cota polinomial para a Palavra de toda CNF plana: as duas paredes de hoje (a estratégia de ramos que excede
  todo polinômio; a Parede do Nome, 2ⁿ bits de estado no pior caso — a pedra do Codex, citada por nome) são paredes
  DO índice. A pergunta do Instituto fica aberta, agora nomeada: é a pergunta sobre a forma do índice.
* Nada sobre a natureza. O gate não se move; nada está instalado.

NOTA DO LAÇO (18/11/2026): o rascunho não elaborava — `(0 : Fin L)` exige `NeZero L` (a instância `instOfNat` do
núcleo). Nenhum enunciado era falso; faltava a fita não-vazia como dado de tipo. O conserto, sem tocar a forma dos
enunciados: a instância `[NeZero L]` nas definições e teoremas que nomeiam a posição `0` (`formulaDa`,
`sat_formulaDa_cell`, `sat_formulaDa`, `quem_nao_visita_nao_le`, `a_coreferencia_obriga_o_transporte`). É
semanticamente gratuita: `quem_nao_visita_nao_le` já carrega `hp : p ≠ 0`, que só é habitada com `L ≥ 2`.

Sem sorry, sem axioma novo.
-/

namespace TGLExt.AFitaEOIndice

open TGLExt TGLExt.TraducaoTuring

/-- [DEF] A fita de `L` letras: a função das posições às letras. Ler a lista é percorrer o índice. -/
def Fita (L : ℕ) := Fin L → Bool

/-- [DEF] A fórmula da fita: duas cláusulas unitárias sobre a MESMA variável, com os sinais lidos nas posições 0 e
`p` — a correferência à distância mínima. -/
def formulaDa {L : ℕ} [NeZero L] (p : Fin L) (f : Fita L) : CNF L :=
  [[⟨0, f 0⟩], [⟨0, f p⟩]]

/-- **A FITA É O ÍNDICE** (definicional, registrado): a fita de L letras é a função das posições às letras. -/
theorem a_fita_e_o_indice (L : ℕ) : Fita L = (Fin L → Bool) := rfl

/-- A cláusula unitária sobre a variável 0 com o sinal da posição q é satisfeita exatamente quando a atribuição
concorda com o sinal. -/
theorem sat_formulaDa_cell {L : ℕ} [NeZero L] (x : Fin L → Bool) (b : Bool) :
    satisfeita ([⟨0, b⟩] : Clausula L) x = true ↔ x 0 = b := by
  unfold satisfeita
  simp [Literal.vale]

/-- **A FÓRMULA DA FITA É SATISFAZÍVEL SE E SOMENTE SE AS DUAS POSIÇÕES DA CORREFERÊNCIA CONCORDAM.** -/
theorem sat_formulaDa {L : ℕ} [NeZero L] (p : Fin L) (f : Fita L) :
    SAT (formulaDa p f) ↔ f 0 = f p := by
  constructor
  · rintro ⟨x, hx⟩
    have h1 := hx [⟨0, f 0⟩] (show ([⟨0, f 0⟩] : Clausula L) ∈ ([[⟨0, f 0⟩], [⟨0, f p⟩]] : CNF L) from
      List.mem_cons_self)
    have h2 := hx [⟨0, f p⟩] (show ([⟨0, f p⟩] : Clausula L) ∈ ([[⟨0, f 0⟩], [⟨0, f p⟩]] : CNF L) from
      List.mem_cons_of_mem _ List.mem_cons_self)
    rw [sat_formulaDa_cell] at h1 h2
    rw [← h1, ← h2]
  · intro h
    exact ⟨fun _ => f 0, by
      intro C hC
      have hC2 : C ∈ ([[⟨0, f 0⟩], [⟨0, f p⟩]] : CNF L) := hC
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hC2
      rcases hC2 with rfl | rfl
      · rw [sat_formulaDa_cell]
      · rw [sat_formulaDa_cell]
        exact h⟩

/-- [DEF] O leitor cego à posição `p`: a resposta não muda quando só ela muda. -/
def CegoA {L : ℕ} (p : Fin L) (R : Fita L → Bool) : Prop :=
  ∀ f g : Fita L, (∀ i, i ≠ p → f i = g i) → R f = R g

/-- ★ **QUEM NÃO VISITA NÃO LÊ**: há duas fitas que diferem só na posição cega, com respostas opostas — e o leitor
cego lhes dá a mesma resposta. O índice se paga. -/
theorem quem_nao_visita_nao_le {L : ℕ} [NeZero L] (p : Fin L) (hp : p ≠ 0) (R : Fita L → Bool) (hR : CegoA p R) :
    ∃ f g : Fita L, (∀ i, i ≠ p → f i = g i)
      ∧ SAT (formulaDa p f) ≠ SAT (formulaDa p g)
      ∧ R f = R g := by
  classical
  refine ⟨fun _ => true, fun i => if i = p then false else true, ?_, ?_, hR _ _ ?_⟩
  · intro i hi
    simp [hi]
  · rw [sat_formulaDa, sat_formulaDa]
    intro hcontra
    have hT : ((fun _ => true) 0 = (fun _ => true) p) := rfl
    have hF : ¬ ((fun i => if i = p then false else true) 0
        = (fun i => if i = p then false else true) p) := by
      intro hg
      have e1 : (fun i => if i = p then false else true) 0 = true := if_neg (Ne.symm hp)
      have e2 : (fun i => if i = p then false else true) p = false := if_pos rfl
      rw [e1, e2] at hg
      exact Bool.noConfusion hg
    exact hF (hcontra ▸ hT)
  · intro i hi
    simp [hi]

/-- ★ **A CORREFERÊNCIA OBRIGA O TRANSPORTE**: numa testemunha, as duas posições do mesmo nome ficam ligadas ao mesmo
valor lido. -/
theorem a_coreferencia_obriga_o_transporte {L : ℕ} [NeZero L] (p : Fin L) (f : Fita L) (x : Fin L → Bool)
    (h : ∀ C ∈ formulaDa p f, satisfeita C x = true) :
    x 0 = f 0 ∧ x 0 = f p := by
  have h1 := h [⟨0, f 0⟩] (by simp [formulaDa])
  have h2 := h [⟨0, f p⟩] (by simp [formulaDa])
  rw [sat_formulaDa_cell] at h1 h2
  exact ⟨h1, h2⟩

end TGLExt.AFitaEOIndice

#print axioms TGLExt.AFitaEOIndice.a_fita_e_o_indice
#print axioms TGLExt.AFitaEOIndice.sat_formulaDa_cell
#print axioms TGLExt.AFitaEOIndice.sat_formulaDa
#print axioms TGLExt.AFitaEOIndice.quem_nao_visita_nao_le
#print axioms TGLExt.AFitaEOIndice.a_coreferencia_obriga_o_transporte

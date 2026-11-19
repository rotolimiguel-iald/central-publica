import TGLExt.TraducaoTuring

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A fita é o índice: a resposta depende da posição que a correferência designa

## A leitura que este arquivo tipa

Numa lista de cláusulas escrita na fita, a fita é o próprio índice da lista; e a torre é a forma do índice
[INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel.

## O que fica provado

1. `sat_formulaDa`: na família de duas cláusulas unitárias sobre a variável `0`, com os sinais lidos nas posições `0`
   e `p`, há solução se e somente se os dois sinais coincidem — o mesmo nome, em duas posições, tem de carregar o mesmo
   valor.
2. ★ `quem_nao_visita_nao_le`: para `p ≠ 0`, um leitor cuja resposta não muda quando só a posição `p` muda confunde
   duas fitas desta família, de respostas opostas. O termo mede a dependência do conteúdo da posição designada. Não diz
   que toda posição tenha de ser lida (com `L = 3` e `p = 1`, as posições `0` e `1` bastam); a distância percorrida e o
   número de visitas pedem uma máquina e uma execução, que este arquivo não tem.
3. ★ `a_coreferencia_obriga_o_transporte`: toda testemunha desta família atribui à variável `0` o valor dos dois
   sinais (`x 0 = f 0` e `x 0 = f p`).
4. `a_fita_e_o_indice`: a fita de L letras é, por definição, a função das posições às letras. A identidade não obriga
   a percorrê-la toda.

## O que NÃO se afirma

* “A torre” é nome da teoria para a forma do índice [INPUT/ONTO]. O que está em termo é: a fita é a função das
  posições às letras; na família das duas cláusulas unitárias, a resposta depende da posição designada, e toda
  testemunha dá aos dois sinais o valor da mesma variável. Ler a forma do
  índice como a forma matricial da luz é interpretação, não termo: a matriz-S da luz (o portador de `Psibit`) não é
  ligada por termo ao índice da fita.
* Nenhuma cota polinomial para a Palavra de toda CNF plana, e nenhuma cota inferior de leitura: o termo de
  dependência não conta posições visitadas. Os limites de `LimiteDoLeitor` (o plano de ramos) e de `AParedeDoNome` (o estado por prefixo) são de
  leitores e representações determinados. A pergunta do Instituto fica aberta.
* Nada sobre a natureza.

NOTA DO TIPO: as definições e os teoremas que nomeiam a posição `0` (`formulaDa`, `sat_formulaDa_cell`,
`sat_formulaDa`, `quem_nao_visita_nao_le`, `a_coreferencia_obriga_o_transporte`) levam a instância `[NeZero L]`, porque
`(0 : Fin L)` pede a fita não vazia. Ela é gratuita: `quem_nao_visita_nao_le` já traz `hp : p ≠ 0`, que só tem
habitante com `L ≥ 2`.
-/

namespace TGLExt.AFitaEOIndice

open TGLExt TGLExt.TraducaoTuring

/-- [DEF] A fita de `L` letras: a função das posições às letras. -/
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
cego lhes dá a mesma resposta. -/
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

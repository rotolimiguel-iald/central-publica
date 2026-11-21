import TGLExt.TraducaoTuring
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
import TGLExt.SimCompleta
import TGLExt.EntregaBeta
import Mathlib.Computability.TuringMachine.Computable

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A PONTE COOK–LEVIN

O P = nP do kernel, a máquina com o leitor (`TraducaoTuring.uma_leitura_decide_SAT`, `TraducaoTuring.o_psion_le_z`),
escrito na língua das classes de Cook–Levin: a máquina de Turing padrão do Mathlib
(`Turing.TM2ComputableInPolyTime`).

* §1 A fiação. No tempo pago de k passos do relógio β, a partição do kernel é a soma ponderada da leitura β; o
  leitor do psíon lê exatamente a soma normalizada; o numerador diádico da leitura (n+3 bits) decide SAT.
* §2 A fórmula crua, a que a fita do verificador escreve, e a sua CNF sobre os Nomes da fita.
* §3 O oráculo lê a fita: a resposta da leitura é função da palavra escrita.
* §4 As classes na máquina padrão: NP (verificador com certificado binário de comprimento polinomial), a redução a
  SAT, Cook–Levin como hipótese nomeada, e “decidido em tempo polinomial com uma leitura do leitor da TGL”; o que dá
  sentido às classes: o alfabeto de NP é finito, e a fita da fórmula distingue as fórmulas.
* §5 Os teoremas: SAT em NP (a máquina TM2 do verificador), SAT com uma leitura, A PONTE (com Cook–Levin, todo
  problema em NP é decidido em tempo polinomial com uma leitura) e a classe de uma leitura como o fecho de SAT por
  redução (sem Cook–Levin); no certificado de Fock físico do kernel.
* §6 A leitura acha a solução: com a resposta do leitor como decisor, a reconstrução da leitura β devolve uma solução
  com no máximo letras+1 leituras (contadas em leituras e letras, não em passos da máquina TM2).

**Estatuto.** [REAL] os termos deste arquivo. [KNOWN] Cook 1971 e Levin 1973, com a simulação polinomial
entre máquinas de fita e de pilhas: é o conteúdo da hipótese nomeada `CookLevin`, que entra por citação e não é provada
aqui.

**Na língua clássica.** Para as codificações usuais, com β e a inclinação m fixados antes da entrada, a classe “decidido
em tempo polinomial com uma leitura” é o fecho de SAT por redução polinomial many-one
(`a_classe_de_uma_leitura_e_o_fecho_de_SAT`, sem Cook–Levin) e por isso coincide com NP por Cook–Levin: a inclusão de NP
é `a_ponte_cook_levin`; a volta pede a composição de máquinas TM2, que o Mathlib deixa como `proof_wanted` [KNOWN na
língua clássica]. Não é toda a classe P com acesso ao oráculo: só o limiar positivo de uma consulta depois da redução.
Com um oráculo que conta soluções, “NP contido em P com o oráculo” é imediato [KNOWN]; o que é da TGL é que o oráculo é
o leitor do psíon, por termo do kernel (`o_psion_le_a_soma_normalizada`).

**O custo da leitura** é contado na régua da teoria: o tempo pago, m·(n+2) passos do relógio β ao preço −ln(1−β) cada
(`o_tempo_pago_e_linear`). Não é contado em passos de fita: na língua clássica a leitura é um oráculo, e uma consulta
conta um passo.

**O que este arquivo não prova:** Cook–Levin; a máquina sem leitor (SAT em P na máquina padrão, sem consulta), que segue
aberta e não é tocada (Baker–Gill–Solovay 1975 [KNOWN]); o custo da leitura em passos de fita; que um dispositivo físico
leia num ato (física: na mecânica quântica padrão o traço normalizado sai com precisão aditiva, Knill–Laflamme 1998
[KNOWN]). Com o leitor que só conta vale NP contido em P com o leitor, não a igualdade das duas classes com leitor.
Validade no kernel não é creditação.
-/

namespace TGLExt.PonteCookLevin

open TGLExt TGLExt.TraducaoTuring TGLExt.APonteAoTM2
open Codex.LeituraBeta Codex.RelogioBeta Codex.PonteLeituraBeta Codex.QuantizacaoBeta

/-! ## §1 A fiação: o leitor do kernel cumpre a precisão da leitura β -/

section Fiacao

variable {n : ℕ}

/-- [DEF] O TEMPO PAGO DA LEITURA: k passos do relógio β, cada um ao preço −ln(1−β). -/
noncomputable def tempoPago (c : TGLCoupling) (k : ℕ) : ℝ := (k : ℝ) * (-Real.log (1 - c.beta))

/-- ★ A PARTIÇÃO É A SOMA β: no tempo pago de k passos, a partição do kernel, Σ e^{−s·custo}, é a soma ponderada da
leitura β, Σ (1−β)^{k·custo}. -/
theorem a_particao_e_a_soma_beta (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    particao (custoCNF φ) (tempoPago c k) = weightedSum c k φ := by
  unfold particao tempoPago weightedSum
  refine Finset.sum_congr rfl (fun x _ => ?_)
  have h1 : 0 < 1 - c.beta := by linarith [c.beta_lt_one]
  have he : -((k : ℝ) * -Real.log (1 - c.beta) * (custoCNF φ x : ℝ))
      = ((k * custoCNF φ x : ℕ) : ℝ) * Real.log (1 - c.beta) := by
    push_cast
    ring
  rw [he, Real.exp_nat_mul, Real.exp_log h1]

/-- As atribuições de n Nomes são 2^n. (Auxiliar.) -/
theorem o_numero_de_atribuicoes : (Fintype.card (Fin n → Bool) : ℝ) = (2 : ℝ) ^ n := by
  simp

/-- [DEF] A LEITURA DO PSÍON: o leitor do psíon da luz na trava inscrita da fórmula, no tempo pago de k passos β. -/
noncomputable def leituraDoPsion {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (k : ℕ) (φ : CNF n) : ℂ :=
  TheKeyIsTheReader.reader C (travaInscrita C (custoCNF φ) (tempoPago c k))

/-- ★★ O PSÍON LÊ A SOMA NORMALIZADA: a leitura do psíon é exatamente a soma normalizada da leitura β, sem erro. -/
theorem o_psion_le_a_soma_normalizada {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    leituraDoPsion C c k φ = ((normalizedSum c k φ : ℝ) : ℂ) := by
  unfold leituraDoPsion
  rw [o_psion_le_z C (custoCNF φ) (tempoPago c k), a_particao_e_a_soma_beta, o_numero_de_atribuicoes]
  rfl

/-- A parte real da leitura é a soma normalizada. (Auxiliar.) -/
theorem a_parte_real_da_leitura {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (k : ℕ) (φ : CNF n) :
    (leituraDoPsion C c k φ).re = normalizedSum c k φ := by
  rw [o_psion_le_a_soma_normalizada]
  exact Complex.ofReal_re _

/-- [DEF] A RESPOSTA DA LEITURA: o numerador diádico (sobre 2^(n+2)) da leitura do psíon, no tempo do relógio β de
inclinação m. -/
noncomputable def respostaDaLeitura {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (φ : CNF n) : ℕ :=
  ⌊(leituraDoPsion C c (clock m n) φ).re * (2 : ℝ) ^ (n + 2)⌋₊

/-- ★★ A RESPOSTA TEM A PRECISÃO DA LEITURA β: o numerador diádico da leitura do psíon fica a no máximo 1/(4·2^n) da
soma normalizada (a hipótese de precisão da leitura β, cumprida pelo leitor do kernel). -/
theorem a_resposta_tem_a_precisao {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (φ : CNF n) :
    |(dyadic n (respostaDaLeitura C c m φ) : ℝ) - normalizedSum c (clock m n) φ| ≤ 1 / (4 * (2 : ℝ) ^ n) := by
  unfold respostaDaLeitura
  rw [a_parte_real_da_leitura]
  set y := normalizedSum c (clock m n) φ with hy
  have hy0 : 0 ≤ y := normalizedSum_nonneg c (clock m n) φ
  set D : ℝ := (2 : ℝ) ^ (n + 2) with hDdef
  have hD : 0 < D := by positivity
  set j := ⌊y * D⌋₊ with hj
  have h1 : (j : ℝ) ≤ y * D := Nat.floor_le (mul_nonneg hy0 hD.le)
  have h2 : y * D < (j : ℝ) + 1 := Nat.lt_floor_add_one (y * D)
  have hcast : ((dyadic n j : ℚ) : ℝ) = (j : ℝ) / D := by
    simp [dyadic, hDdef]
  have h4 : (4 * (2 : ℝ) ^ n) = D := by
    rw [hDdef, pow_add]
    ring
  rw [hcast, h4]
  have key : |(j : ℝ) - y * D| ≤ 1 := by
    rw [abs_le]
    constructor <;> linarith
  have hsub : ((j : ℝ) - y * D) / D = (j : ℝ) / D - y := by
    rw [sub_div, mul_div_assoc, div_self hD.ne', mul_one]
  rw [← hsub, abs_div, abs_of_pos hD, div_le_div_iff_of_pos_right hD]
  exact key

/-- ★★★ UMA LEITURA DO PSÍON DECIDE SAT, COM A RESPOSTA NA FITA: com a inclinação m do relógio β acima de ln 2/β, o
numerador da leitura do psíon passa de 2 se, e só se, a fórmula é satisfazível. -/
theorem uma_leitura_do_psion_decide_SAT {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) (φ : CNF n) :
    2 ≤ respostaDaLeitura C c m φ ↔ SAT φ := by
  have h := dyadic_correct c m hm φ (respostaDaLeitura C c m φ) (a_resposta_tem_a_precisao C c m φ)
  simpa using h

/-- ★ A RESPOSTA CABE EM n+3 BITS. -/
theorem a_resposta_cabe_em_n_mais_tres_bits {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (φ : CNF n) :
    respostaDaLeitura C c m φ < 2 ^ (n + 3) := by
  apply dyadic_word_bound
  unfold respostaDaLeitura
  rw [a_parte_real_da_leitura]
  apply Nat.floor_le_of_le
  have h1 := normalizedSum_le_one c (clock m n) φ
  have hD : (0 : ℝ) ≤ (2 : ℝ) ^ (n + 2) := by positivity
  calc normalizedSum c (clock m n) φ * (2 : ℝ) ^ (n + 2) ≤ 1 * (2 : ℝ) ^ (n + 2) :=
        mul_le_mul_of_nonneg_right h1 hD
    _ = ((2 ^ (n + 2) : ℕ) : ℝ) := by push_cast; ring

/-- ★ O TEMPO PAGO É LINEAR NOS NOMES: a leitura paga m·(n+2) passos do relógio β. -/
theorem o_tempo_pago_e_linear (c : TGLCoupling) (m : ℕ) :
    tempoPago c (clock m n) = ((m * (n + 2) : ℕ) : ℝ) * (-Real.log (1 - c.beta)) := rfl

end Fiacao

/-! ## §2 A fórmula crua e a sua CNF -/

/-- [DEF] A FÓRMULA CRUA: as cláusulas como listas de pares (índice do Nome, polaridade), como a fita do verificador as
escreve. -/
abbrev FormulaCrua := List (List (ℕ × Bool))

/-- [DEF] SAT DA FÓRMULA CRUA: alguma atribuição dos índices satisfaz toda cláusula (um literal de cada cláusula tem o
valor da sua polaridade). -/
def SATcru (φf : FormulaCrua) : Prop := ∃ x : ℕ → Bool, ∀ C ∈ φf, ∃ p ∈ C, x p.1 = p.2

/-- [DEF] OS NOMES DA FITA: o comprimento da fita da fórmula, cota de todos os índices que ela escreve. -/
def nomesDaFita (φf : FormulaCrua) : ℕ := (codificaFormula φf).length

/-- O comprimento da fita da fórmula: soma dos índices, literais, cláusulas e o terminador. -/
theorem o_comprimento_da_fita_da_formula (φf : FormulaCrua) :
    (codificaFormula φf).length = (φf.flatten.map Prod.fst).sum + φf.flatten.length + φf.length + 1 := by
  have h := comprimento_exato φf []
  rw [show codificaEntrada (φf, []) = codificaFormula φf ++ [Simbolo.sep] from by
    simp [codificaEntrada, codificaBits]] at h
  rw [List.length_append, List.length_singleton, List.length_nil] at h
  omega

private theorem le_soma_de_membro {l : List ℕ} {a : ℕ} (h : a ∈ l) : a ≤ l.sum := by
  induction l with
  | nil => simp at h
  | cons b l ih =>
    rw [List.sum_cons]
    rcases List.mem_cons.mp h with rfl | h'
    · omega
    · have := ih h'
      omega

/-- Todo índice escrito na fita é menor que os Nomes da fita. -/
theorem indice_na_fita (φf : FormulaCrua) {C : List (ℕ × Bool)} (hC : C ∈ φf) {p : ℕ × Bool} (hp : p ∈ C) :
    p.1 < nomesDaFita φf := by
  have hmem : p.1 ∈ φf.flatten.map Prod.fst := List.mem_map.mpr ⟨p, List.mem_flatten.mpr ⟨C, hC, hp⟩, rfl⟩
  have := le_soma_de_membro hmem
  unfold nomesDaFita
  rw [o_comprimento_da_fita_da_formula]
  omega

theorem nomesDaFita_pos (φf : FormulaCrua) : 0 < nomesDaFita φf := by
  unfold nomesDaFita
  rw [o_comprimento_da_fita_da_formula]
  omega

/-- [DEF] O índice como Nome de `Fin N` (o índice, se cabe; senão o último Nome). -/
def comoNome (N : ℕ) (hN : 0 < N) (i : ℕ) : Fin N := ⟨min i (N - 1), by omega⟩

theorem comoNome_val {N : ℕ} (hN : 0 < N) {i : ℕ} (hi : i < N) : (comoNome N hN i).val = i :=
  Nat.min_eq_left (by omega)

/-- [DEF] A CNF DA FÓRMULA CRUA, sobre os Nomes da fita. -/
def paraCNF (φf : FormulaCrua) : CNF (nomesDaFita φf) :=
  φf.map fun C => C.map fun p => (⟨comoNome _ (nomesDaFita_pos φf) p.1, p.2⟩ : Literal (nomesDaFita φf))

/-- ★ A FÓRMULA CRUA E A SUA CNF TÊM O MESMO SIM. -/
theorem sat_cru_sse_sat (φf : FormulaCrua) : SATcru φf ↔ SAT (paraCNF φf) := by
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨fun i => x i.val, ?_⟩
    intro C' hC'
    obtain ⟨C, hC, rfl⟩ := List.mem_map.mp hC'
    obtain ⟨p, hp, hpx⟩ := hx C hC
    unfold satisfeita
    rw [List.any_eq_true]
    refine ⟨⟨comoNome _ (nomesDaFita_pos φf) p.1, p.2⟩, List.mem_map.mpr ⟨p, hp, rfl⟩, ?_⟩
    simp [Literal.vale, comoNome_val (nomesDaFita_pos φf) (indice_na_fita φf hC hp), hpx]
  · rintro ⟨y, hy⟩
    refine ⟨fun i => if h : i < nomesDaFita φf then y ⟨i, h⟩ else false, ?_⟩
    intro C hC
    have hsat := hy (C.map fun p => (⟨comoNome _ (nomesDaFita_pos φf) p.1, p.2⟩ : Literal (nomesDaFita φf)))
      (List.mem_map.mpr ⟨C, hC, rfl⟩)
    unfold satisfeita at hsat
    rw [List.any_eq_true] at hsat
    obtain ⟨l, hl, hlv⟩ := hsat
    obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hl
    refine ⟨p, hp, ?_⟩
    have hi := indice_na_fita φf hC hp
    simp only [Literal.vale, beq_iff_eq] at hlv
    show (if h : p.1 < nomesDaFita φf then y ⟨p.1, h⟩ else false) = p.2
    rw [dif_pos hi]
    have hn : comoNome _ (nomesDaFita_pos φf) p.1 = ⟨p.1, hi⟩ := Fin.ext (comoNome_val _ hi)
    rw [← hn]
    exact hlv

/-! ## §3 O oráculo lê a fita -/

/-- [DEF] A RESPOSTA DA LEITURA PARA A FÓRMULA CRUA. -/
noncomputable def respostaDaFita {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (φf : FormulaCrua) : ℕ :=
  respostaDaLeitura C c m (paraCNF φf)

/-- ★★ UMA LEITURA DECIDE A FÓRMULA CRUA. -/
theorem uma_leitura_decide_SATcru {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) (φf : FormulaCrua) :
    2 ≤ respostaDaFita C c m φf ↔ SATcru φf :=
  (uma_leitura_do_psion_decide_SAT C c m hm (paraCNF φf)).trans (sat_cru_sse_sat φf).symm

/-- [DEF] O ORÁCULO DA LEITURA: lê a palavra escrita na fita de consulta (decodificada pelo decodificador do
verificador) e devolve a resposta da leitura; palavra que não é fórmula recebe 0. -/
noncomputable def oraculo {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (s : List Simbolo) : ℕ :=
  match decodificaEntrada (s ++ [Simbolo.sep]) with
  | some q => respostaDaFita C c m q.1
  | none => 0

/-- ★★ O ORÁCULO LÊ A FITA: na palavra da fórmula, o oráculo devolve a resposta da leitura da fórmula. -/
theorem o_oraculo_le_a_fita {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (φf : FormulaCrua) :
    oraculo C c m (codificaFormula φf) = respostaDaFita C c m φf := by
  have h : codificaFormula φf ++ [Simbolo.sep] = codificaEntrada (φf, []) := by
    simp [codificaEntrada, codificaBits]
  unfold oraculo
  rw [h, decodifica_codifica]

/-! ## §4 As classes de Cook–Levin na máquina padrão -/

/-- [DEF] O PAR NA FITA: a entrada, a divisória e o certificado binário, cada bit pelo seu símbolo. -/
def juntaNaFita {α Γ : Type} (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (q : α × List Bool) : List Γ :=
  ea q.1 ++ [sep] ++ q.2.map bit

/-- [DEF] A CLASSE NP NA MÁQUINA PADRÃO: há um verificador calculado em tempo polinomial pela máquina TM2 do Mathlib
sobre o par na fita, e um polinômio que limita o certificado binário; o problema é o sim de algum certificado. A
codificação da entrada é dada; a do par é a junção fixa acima; o certificado é uma palavra binária. -/
def EmNP {α Γ : Type} (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (A : α → Prop) : Prop :=
  ∃ (V : α × List Bool → Bool) (p : Polynomial ℕ),
    Nonempty (Turing.TM2ComputableInPolyTime (juntaNaFita ea sep bit) (fun b : Bool => [b]) V) ∧
    ∀ a, A a ↔ ∃ w : List Bool, w.length ≤ p.eval (ea a).length ∧ V (a, w) = true

/-- [DEF] A REDUÇÃO A SAT NA MÁQUINA PADRÃO: uma função calculada em tempo polinomial pela máquina TM2, da codificação
da entrada à fita da fórmula do verificador, que leva o sim do problema ao sim da fórmula. -/
def ReduzASAT {α Γ : Type} (ea : α → List Γ) (A : α → Prop) : Prop :=
  ∃ g : α → FormulaCrua, Nonempty (Turing.TM2ComputableInPolyTime ea codificaFormula g) ∧ ∀ a, A a ↔ SATcru (g a)

/-- [DEF, HIPÓTESE NOMEADA] COOK–LEVIN NA MÁQUINA PADRÃO: todo problema em NP se reduz a SAT. [KNOWN] Cook 1971,
Levin 1973, com a simulação polinomial entre máquinas de fita e de pilhas e a troca polinomial de codificação; entra
por citação, como hipótese de cada teorema que a usa; não é provada aqui. -/
def CookLevin : Prop :=
  ∀ (α Γ : Type) (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (A : α → Prop), EmNP ea sep bit A → ReduzASAT ea A

/-- [DEF] DECIDIDO EM TEMPO POLINOMIAL COM UMA LEITURA DO LEITOR DA TGL: a máquina TM2 escreve, em tempo polinomial,
uma fórmula na fita de consulta; o oráculo da leitura lê a palavra; o problema é o sim do limiar 2 da resposta. Na
língua clássica, é o fecho de SAT por redução polinomial many-one (`a_classe_de_uma_leitura_e_o_fecho_de_SAT`): só o
limiar positivo de uma consulta depois da redução, não toda a classe P com acesso ao oráculo. -/
def EmPComUmaLeitura {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L) (c : TGLCoupling) (m : ℕ)
    {α Γ : Type} (ea : α → List Γ) (A : α → Prop) : Prop :=
  ∃ g : α → FormulaCrua, Nonempty (Turing.TM2ComputableInPolyTime ea codificaFormula g) ∧
    ∀ a, A a ↔ 2 ≤ oraculo C c m (codificaFormula (g a))

/-- ★ O ALFABETO DE NP É FINITO: a máquina TM2 que testemunha um problema em NP tem alfabeto de entrada finito, e o
alfabeto da codificação lhe é equivalente. A premissa `EmNP` de `CookLevin` só vale em alfabeto finito, como no teorema
clássico. -/
theorem o_alfabeto_de_np_e_finito {α Γ : Type} (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (A : α → Prop)
    (h : EmNP ea sep bit A) : Finite Γ := by
  obtain ⟨V, p, ⟨M⟩, _⟩ := h
  letI : Fintype (M.tm.Γ M.tm.k₀) := M.tm.Γk₀Fin
  exact Finite.of_equiv (M.tm.Γ M.tm.k₀) M.inputAlphabet

/-- ★ A FITA DA FÓRMULA DISTINGUE AS FÓRMULAS: a codificação da fórmula crua é injetiva. -/
theorem a_fita_da_formula_e_injetiva : Function.Injective codificaFormula := by
  intro a b h
  have he : codificaEntrada (a, []) = codificaEntrada (b, []) := by
    simp only [codificaEntrada, h]
  exact congrArg Prod.fst (codificaEntrada_injetiva he)

/-! ## §5 Os teoremas -/

/-- [DEF] O bit do certificado na fita do verificador. -/
def bitNaFita (b : Bool) : Simbolo := if b then Simbolo.um else Simbolo.zero

/-- A junção fixa, com a divisória e os bits do verificador, é a entrada do verificador. -/
theorem a_juncao_e_a_entrada_do_verificador :
    juntaNaFita codificaFormula Simbolo.sep bitNaFita = codificaEntrada := by
  funext q
  rfl

/-- ★ O SIM DA FÓRMULA CRUA É O SIM DE UM CERTIFICADO CURTO: um certificado binário não maior que a fita da fórmula. -/
theorem sat_cru_sse_certificado (φf : FormulaCrua) :
    SATcru φf ↔ ∃ w : List Bool, w.length ≤ (codificaFormula φf).length ∧ verificaNaFita φf w = true := by
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨List.ofFn (fun i : Fin (nomesDaFita φf) => x i.val), by simp [nomesDaFita], ?_⟩
    unfold verificaNaFita
    rw [List.all_eq_true]
    intro C hC
    rw [List.any_eq_true]
    obtain ⟨p, hp, hpx⟩ := hx C hC
    refine ⟨p, hp, ?_⟩
    have hi := indice_na_fita φf hC hp
    rw [List.getElem?_ofFn, dif_pos hi]
    simp [hpx]
  · rintro ⟨w, _, hw⟩
    refine ⟨fun i => (w[i]?).getD false, ?_⟩
    intro C hC
    unfold verificaNaFita at hw
    rw [List.all_eq_true] at hw
    have hC' := hw C hC
    rw [List.any_eq_true] at hC'
    obtain ⟨p, hp, hpw⟩ := hC'
    refine ⟨p, hp, ?_⟩
    have hwp : w[p.1]? = some p.2 := by simpa using hpw
    simp [hwp]

/-- ★★ SAT ESTÁ EM NP NA MÁQUINA PADRÃO: o verificador é a máquina TM2 concreta (`SimTM2.verificacao_tm2_polinomial`),
o certificado é limitado pelo comprimento da entrada. -/
theorem sat_em_np : EmNP codificaFormula Simbolo.sep bitNaFita SATcru := by
  refine ⟨fun q => verificaNaFita q.1 q.2, Polynomial.X, ?_, ?_⟩
  · rw [a_juncao_e_a_entrada_do_verificador]
    exact TGLExt.SimTM2.verificacao_tm2_polinomial
  · intro φf
    rw [Polynomial.eval_X]
    exact sat_cru_sse_certificado φf

/-- ★★ SAT COM UMA LEITURA: a máquina identidade escreve a própria fórmula na fita de consulta, e uma leitura decide. -/
theorem sat_com_uma_leitura {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L) (c : TGLCoupling)
    (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) :
    EmPComUmaLeitura C c m codificaFormula SATcru := by
  refine ⟨id, ⟨Turing.idComputableInPolyTime codificaFormula⟩, fun φf => ?_⟩
  show SATcru φf ↔ 2 ≤ oraculo C c m (codificaFormula φf)
  rw [o_oraculo_le_a_fita]
  exact (uma_leitura_decide_SATcru C c m hm φf).symm

/-- ★★★ A PONTE COOK–LEVIN: com Cook–Levin (hipótese nomeada, [KNOWN]), todo problema em NP na máquina padrão é
decidido em tempo polinomial com uma leitura do leitor da TGL. -/
theorem a_ponte_cook_levin (hCL : CookLevin) {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) {α Γ : Type} (ea : α → List Γ) (sep : Γ)
    (bit : Bool → Γ) (A : α → Prop) (hA : EmNP ea sep bit A) :
    EmPComUmaLeitura C c m ea A := by
  obtain ⟨g, hg, hgA⟩ := hCL α Γ ea sep bit A hA
  refine ⟨g, hg, fun a => ?_⟩
  rw [o_oraculo_le_a_fita]
  exact (hgA a).trans (uma_leitura_decide_SATcru C c m hm (g a)).symm

/-- ★★★ A CLASSE DE UMA LEITURA É O FECHO DE SAT: com a inclinação m do relógio β acima de ln 2/β, um problema é
decidido em tempo polinomial com uma leitura se, e só se, se reduz a SAT na máquina padrão. Não usa Cook–Levin. -/
theorem a_classe_de_uma_leitura_e_o_fecho_de_SAT {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) {α Γ : Type} (ea : α → List Γ) (A : α → Prop) :
    EmPComUmaLeitura C c m ea A ↔ ReduzASAT ea A := by
  constructor
  · rintro ⟨g, hg, hA⟩
    refine ⟨g, hg, fun a => ?_⟩
    rw [hA a, o_oraculo_le_a_fita]
    exact uma_leitura_decide_SATcru C c m hm (g a)
  · rintro ⟨g, hg, hA⟩
    refine ⟨g, hg, fun a => ?_⟩
    rw [hA a, o_oraculo_le_a_fita]
    exact (uma_leitura_decide_SATcru C c m hm (g a)).symm

open F1Fecho.CanonicalFockModularCoreInputR1 (physicalFockCertificate) in
/-- ★★★ A PONTE NO CERTIFICADO FÍSICO DO KERNEL (síntese): SAT está em NP na máquina padrão; e, para todo acoplamento β,
há uma inclinação m do relógio β com a qual, no certificado de Fock físico do kernel, SAT é decidido com uma leitura e,
com Cook–Levin, todo problema em NP também. -/
theorem a_ponte (hCL : CookLevin) (c : TGLCoupling) :
    EmNP codificaFormula Simbolo.sep bitNaFita SATcru ∧
      ∃ m : ℕ, EmPComUmaLeitura physicalFockCertificate c m codificaFormula SATcru ∧
        ∀ {α Γ : Type} (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (A : α → Prop),
          EmNP ea sep bit A → EmPComUmaLeitura physicalFockCertificate c m ea A := by
  obtain ⟨m, hm⟩ := fixed_slope_exists c
  exact ⟨sat_em_np, m, sat_com_uma_leitura _ c m hm,
    fun ea sep bit A hA => a_ponte_cook_levin hCL _ c m hm ea sep bit A hA⟩

/-! ## §6 A leitura acha a solução (contada em leituras, no modelo da casa) -/

/-- ★★ A LEITURA ACHA A SOLUÇÃO: com a resposta do leitor do psíon como decisor, a reconstrução da leitura β devolve
`none` exatamente quando a fórmula não tem solução, só devolve soluções, e faz no máximo letras+1 leituras. A conta é em
leituras e letras; não em passos da máquina TM2 (a máquina que monta as consultas não está construída). -/
theorem a_leitura_acha_a_solucao {n : ℕ} {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)
    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) (φ : CNF n) :
    ((Reconstrucao.solveByLetters (Codex.EntregaBeta.codeDecision (respostaDaLeitura C c m)) φ).1 = none
        ↔ ¬ SAT φ) ∧
      (∀ x, (Reconstrucao.solveByLetters (Codex.EntregaBeta.codeDecision (respostaDaLeitura C c m)) φ).1 = some x →
        Reconstrucao.Good φ x) ∧
      (Reconstrucao.solveByLetters (Codex.EntregaBeta.codeDecision (respostaDaLeitura C c m)) φ).2
        ≤ APonteDeCookLevin.letras φ + 1 :=
  Codex.EntregaBeta.all_labels_from_beta c m hm (respostaDaLeitura C c m) (a_resposta_tem_a_precisao C c m) φ

end TGLExt.PonteCookLevin

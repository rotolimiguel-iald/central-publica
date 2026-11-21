import APropostaDaTensao
import TGLExt.CompilaHornNaFita

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
# TRINITY: A INCLINAÇÃO DO NOME — O SIM, O EMPURRÃO E A FRONTEIRA

  [Pedra candidata para a v413, R1, 20/11/2026; não instalada. Nome do operador: «trindade», Trinity (fala por bytes em
  `work\cunhagens_13out\OPERADOR_20nov_excelente_vamos_prosseguir_escreva_a_pedra_que_se_chamara_trindade_Trinity_verbatim.txt`,
  sha16 `f19c729a40fc8e84`). A R1, pedida pelo operador (fala por bytes em
  `work\cunhagens_13out\OPERADOR_20nov_excelente_prossigamos_escreva_a_r1_verbatim.txt`, sha16 `e5319d31af2611ab`), acrescenta a §5b (dois
  literais), um exemplo e um item à síntese; nenhum enunciado da R0 (sha16 `519190db19c7295f`) mudou. A R2 (fala por bytes em
  `work\cunhagens_13out\OPERADOR_20nov_excelente_prossigamos_porque_a_pedra_trinity_refere_se_a_fronteira_dos_tres_literais_verbatim.txt`, sha16 `5646f1ab0f25c220`) acrescenta as §9 a §11 (a fronteira dos três literais e a travessia por
  ramificação); nenhum enunciado da R1 (sha16 `97fd14f931128cf3`) mudou.]

## A leitura (do operador, 20/11/2026, [INPUT/ONTO])

«O zero absoluto empurra a solução para a projeção do lado oposto; "ou diz sim" ou é a morte no zero absoluto; o sistema
inclina.» O termo de partida é a tensão do Kimi (`APropostaDaTensao.a_proposta_nasce_da_escolha_do_nome`): a fórmula tem
solução se, e só se, um dos dois valores do Nome deixa um resto com solução.

## O nome (do operador, 20/11/2026, [INPUT])

«a pedra trinity refere-se à fronteira dos tres literais». O termo que a pedra dá a essa leitura: a inclinação só para na
fronteira, e na fronteira todo lado vivo corta uma cláusula de três literais ou mais; um literal cai e os outros esperam
(`a_inclinacao_para_so_na_fronteira`, `na_fronteira_todo_lado_corta_uma_de_tres`).

## A tipagem

* **A projeção:** fixar o valor do Nome é o resto da tensão (`fixa`, sobre `restringe`).
* **A morte no zero absoluto:** a cláusula vazia (`morta`).
* **A unidade força o lado:** uma cláusula de um só literal fixa o Nome (`propaga`).
* **O empurrão:** se fixar o literal `l` e propagar dá a morte, só o lado oposto pode viver.
* **O compromisso:** se fixar `l` e propagar não corta nenhuma cláusula ao meio (só restam cláusulas originais), o lado `l`
  é seguro.
* **A inclinação:** propagar; morrer ou dizer sim; senão empurrar ou se comprometer; senão ficar na fronteira (`inclina`).

## O que a pedra prova (só o trio; zero sorry)

1. `a_inclinacao_nao_erra`: quando a inclinação diz sim, há solução; quando diz não, não há.
2. `em_horn_o_sistema_sempre_inclina`, `em_horn_a_inclinacao_decide`: em toda fórmula de Horn (a classe `IsHorn` da casa)
   a inclinação diz sim ou morre na primeira volta; nunca fica na fronteira.
3. `todo_lado_morre_ou_nao_corta`, `em_dois_literais_o_sistema_sempre_inclina`, `em_dois_literais_a_inclinacao_decide`
   (R1): numa fórmula em que toda cláusula tem dois literais, todo lado, depois de propagado, ou morre logo ou não corta
   nenhuma cláusula ao meio; por isso a inclinação decide toda fórmula de dois literais. É o resultado de Even–Itai–Shamir
   (1976) [KNOWN], aqui provado para este procedimento.
4. `o_custo_da_inclinacao`: no máximo (T+1)³ fixações, com T o tamanho da fórmula (letras mais terminadores).
5. `oito_sem_solucao`, `oito_fica_na_fronteira`: a fórmula das oito cláusulas de três literais sobre três Nomes não tem
   solução, e a inclinação fica indecisa: nenhum lado morre logo e todo lado corta cláusulas ao meio. A morte está longe.
6. `quatro_o_empurrao_diz_nao`, `o_empurrao_diz_sim`, `dois_o_compromisso_diz_sim`, `a_cadeia_inclina_e_diz_sim`: fórmulas
   sem cláusula unitária, em que a propagação sozinha não começa, decididas pelo empurrão ou pelo compromisso.
7. `a_inclinacao_para_so_na_fronteira` (R2): com combustível maior que o tamanho, se a inclinação fica indecisa, ela parou
   num resto com a mesma resposta que está na fronteira (vivo, sem unidade, não trivial, e a sonda não age).
8. `na_fronteira_todo_lado_corta_uma_de_tres`, `a_fronteira_tem_tres_literais` (R2): na fronteira, todo lado, fixado e
   propagado, fica vivo e deixa uma cláusula de dois literais ou mais cortada de uma cláusula original de três literais ou
   mais; logo a fronteira tem cláusula de três literais.
9. `a_travessia_decide`, `o_preco_da_travessia` (R2): onde a inclinação para, a máquina nua ramifica no primeiro literal e
   segue pelos dois lados; assim decide toda fórmula, e o preço provado é de no máximo 2^k·B fixações, com B = (T+1)² + 1
   e k o combustível: exponencial no tamanho.
10. `oito_esta_na_fronteira`, `sete_atravessa_e_diz_sim`: as oito cláusulas estão na fronteira e a travessia diz não; sete
    delas também param a inclinação, e a travessia diz sim.
11. `a_trindade`, `a_trindade_na_fronteira`: as sínteses.

## O que a pedra NÃO prova

* Que a máquina nua decida toda CNF em tempo polinomial. Na fronteira, decidir pede ramificar; a ramificação da casa custa
  ≥ 2^(m+1) movimentos (`MovimentosDoPlano.coupled_physical_lower`), e todo procedimento que só descobre a morte chegando à
  contradição produz uma refutação por resolução, exponencial nas fórmulas do pombal (Haken 1985 [KNOWN]).
* Que a fronteira dos três literais se atravesse em preço polinomial. A pedra atravessa ramificando, ao preço provado
  exponencial; uma travessia de preço polinomial para toda fórmula de três literais é a pergunta do Instituto [OPEN].
* O custo conta fixações (cada uma, uma passagem pela fórmula) no modelo da casa; as comparações da regra do compromisso não
  entram na conta; não é contagem de passos de uma máquina do Mathlib.
* A leitura teológica do nome é do operador [ONTO]; o termo é o procedimento e os teoremas acima.
-/

namespace TGLExt.Trinity

open TGLExt TGLExt.TraducaoTuring TGLExt.APropostaDaTensao

/-- [DEF] Os três vereditos: diz sim, morre (não), fica na fronteira (indeciso). -/
inductive Veredito
  | sim
  | nao
  | indeciso
  deriving DecidableEq, Repr

variable {n : ℕ}

/-! ## 1. A projeção, a morte e o tamanho -/

/-- [DEF] A projeção: fixar o literal `l` (o valor `l.pos` do Nome `l.var`) é o resto da tensão. -/
def fixa (φ : CNF n) (l : Literal n) : CNF n := restringe φ l.var l.pos

/-- [DEF] O lado oposto. -/
def oposto (l : Literal n) : Literal n := ⟨l.var, !l.pos⟩

/-- [DEF] A cláusula vazia. -/
def vazia : Clausula n → Bool
  | [] => true
  | _ :: _ => false

/-- [DEF] A MORTE NO ZERO ABSOLUTO: a fórmula tem uma cláusula vazia. -/
def morta (φ : CNF n) : Bool := φ.any vazia

/-- [DEF] O tamanho: os literais mais um terminador por cláusula. -/
def tamanho (φ : CNF n) : ℕ := (φ.map fun C => C.length + 1).sum

theorem tamanho_cons (C : Clausula n) (φ : CNF n) : tamanho (C :: φ) = C.length + 1 + tamanho φ := by
  simp [tamanho]

theorem tamanho_zero {φ : CNF n} (h : tamanho φ = 0) : φ = [] := by
  cases φ with
  | nil => rfl
  | cons C φ => rw [tamanho_cons] at h; omega

/-- ★ A MORTE NO ZERO ABSOLUTO É O NÃO: fórmula com cláusula vazia não tem solução. -/
theorem a_morte_e_o_nao {φ : CNF n} (h : morta φ = true) : ¬ SAT φ := by
  rintro ⟨x, hx⟩
  obtain ⟨C, hC, hv⟩ := List.any_eq_true.mp h
  cases C with
  | nil =>
    have h0 := hx [] hC
    simp [satisfeita] at h0
  | cons _ _ => simp [vazia] at hv

/-- O resto da tensão, cláusula a cláusula. -/
theorem restringe_cons (C : Clausula n) (φ : CNF n) (i : Fin n) (b : Bool) :
    restringe (C :: φ) i b =
      if (!C.any fun l => l.var == i && l.pos == b) = true then
        (C.filter fun l => l.var ≠ i) :: restringe φ i b
      else restringe φ i b := by
  unfold restringe
  rw [List.filter_cons]
  by_cases h : (!C.any fun l => l.var == i && l.pos == b) = true
  · rw [if_pos h, if_pos h]
    rfl
  · rw [if_neg h, if_neg h]

/-- Fixar um Nome nunca aumenta o tamanho. -/
theorem tamanho_restringe_le (φ : CNF n) (i : Fin n) (b : Bool) : tamanho (restringe φ i b) ≤ tamanho φ := by
  induction φ with
  | nil => simp [restringe, tamanho]
  | cons C φ ih =>
    rw [restringe_cons]
    split
    · rw [tamanho_cons, tamanho_cons]
      have := List.length_filter_le (fun l => decide (l.var ≠ i)) C
      omega
    · rw [tamanho_cons]
      omega

/-- Tirar de uma cláusula os literais de um Nome que ela tem encurta a cláusula. -/
theorem filtra_encurta : ∀ (C : Clausula n) (i : Fin n), (∃ m ∈ C, m.var = i) →
    (C.filter fun l => l.var ≠ i).length < C.length
  | [], _, ⟨_, hm, _⟩ => by simp at hm
  | a :: C, i, ⟨m, hm, hmi⟩ => by
    rw [List.filter_cons]
    by_cases ha : a.var = i
    · rw [if_neg (by simp [ha])]
      have := List.length_filter_le (fun l => decide (l.var ≠ i)) C
      simp only [List.length_cons]
      omega
    · rw [if_pos (by simp [ha])]
      simp only [List.length_cons]
      have hm' : m ∈ C := by
        rcases List.mem_cons.mp hm with h | h
        · exact absurd (h ▸ hmi) ha
        · exact h
      have := filtra_encurta C i ⟨m, hm', hmi⟩
      omega

/-- Fixar um Nome que aparece na fórmula diminui o tamanho. -/
theorem tamanho_restringe_lt : ∀ (φ : CNF n) (i : Fin n) (b : Bool), (∃ C ∈ φ, ∃ m ∈ C, m.var = i) →
    tamanho (restringe φ i b) < tamanho φ
  | [], _, _, ⟨_, hC, _⟩ => by simp at hC
  | C :: φ, i, b, ⟨D, hD, m, hm, hmi⟩ => by
    rw [restringe_cons]
    rcases List.mem_cons.mp hD with hDC | hD'
    · rw [hDC] at hm
      have hle := tamanho_restringe_le φ i b
      split
      · rw [tamanho_cons, tamanho_cons]
        have := filtra_encurta C i ⟨m, hm, hmi⟩
        omega
      · rw [tamanho_cons]
        omega
    · have hlt := tamanho_restringe_lt φ i b ⟨D, hD', m, hm, hmi⟩
      split
      · rw [tamanho_cons, tamanho_cons]
        have := List.length_filter_le (fun l => decide (l.var ≠ i)) C
        omega
      · rw [tamanho_cons]
        omega

theorem tamanho_fixa_le (φ : CNF n) (l : Literal n) : tamanho (fixa φ l) ≤ tamanho φ :=
  tamanho_restringe_le φ l.var l.pos

/-! ## 2. A unidade força o lado -/

/-- [DEF] O literal de uma cláusula unitária. -/
def unitario : Clausula n → Option (Literal n)
  | [] => none
  | [l] => some l
  | _ :: _ :: _ => none

/-- [DEF] A primeira cláusula unitária da fórmula, se há. -/
def unidade : CNF n → Option (Literal n)
  | [] => none
  | C :: φ =>
    match unitario C with
    | some l => some l
    | none => unidade φ

theorem unitario_some : ∀ {C : Clausula n} {l : Literal n}, unitario C = some l → C = [l]
  | [], _, h => by simp [unitario] at h
  | [m], l, h => by
    simp only [unitario, Option.some.injEq] at h
    rw [h]
  | _ :: _ :: _, _, h => by simp [unitario] at h

theorem unidade_some : ∀ {φ : CNF n} {l : Literal n}, unidade φ = some l → [l] ∈ φ
  | [], _, h => by simp [unidade] at h
  | C :: φ, l, h => by
    simp only [unidade] at h
    cases hu : unitario C with
    | none =>
      simp only [hu] at h
      exact List.mem_cons_of_mem _ (unidade_some h)
    | some m =>
      simp only [hu, Option.some.injEq] at h
      rw [unitario_some hu, h]
      exact List.mem_cons_self

theorem unidade_none : ∀ {φ : CNF n}, unidade φ = none → ∀ C ∈ φ, unitario C = none
  | [], _, _, hC => by simp at hC
  | D :: φ, h, C, hC => by
    simp only [unidade] at h
    cases hu : unitario D with
    | some m => simp [hu] at h
    | none =>
      simp only [hu] at h
      rcases List.mem_cons.mp hC with hCD | hC'
      · rw [hCD]
        exact hu
      · exact unidade_none h C hC'

/-- Com a cláusula unitária [⟨i, p⟩], o lado oposto deixa a cláusula vazia: a morte. -/
theorem vazia_no_resto (φ : CNF n) (i : Fin n) (p : Bool) (h : [(⟨i, p⟩ : Literal n)] ∈ φ) :
    ([] : Clausula n) ∈ restringe φ i (!p) := by
  unfold restringe
  rw [List.mem_map]
  refine ⟨[⟨i, p⟩], List.mem_filter.mpr ⟨h, ?_⟩, ?_⟩
  · cases p <;> simp
  · simp

/-- ★ A UNIDADE FORÇA O LADO: com a cláusula unitária [l], ter solução é ter solução na projeção de l. -/
theorem a_unidade_forca_o_lado {φ : CNF n} {l : Literal n} (h : [l] ∈ φ) : SAT φ ↔ SAT (fixa φ l) := by
  obtain ⟨i, p⟩ := l
  show SAT φ ↔ SAT (restringe φ i p)
  constructor
  · intro hs
    obtain ⟨b, hb⟩ := (a_proposta_nasce_da_escolha_do_nome φ i).mp hs
    cases b <;> cases p
    · exact hb
    · exfalso
      obtain ⟨x, hx⟩ := hb
      have h0 := hx [] (vazia_no_resto φ i true h)
      simp [satisfeita] at h0
    · exfalso
      obtain ⟨x, hx⟩ := hb
      have h0 := hx [] (vazia_no_resto φ i false h)
      simp [satisfeita] at h0
    · exact hb
  · intro hs
    exact (a_proposta_nasce_da_escolha_do_nome φ i).mpr ⟨p, hs⟩

/-- [DEF] A PROPAGAÇÃO: enquanto não há morte, a unidade força o lado. -/
def propaga : ℕ → CNF n → CNF n
  | 0, φ => φ
  | k + 1, φ =>
    if morta φ = true then φ
    else match unidade φ with
      | some l => propaga k (fixa φ l)
      | none => φ

/-- ★ A PROPAGAÇÃO PRESERVA: propagar não cria nem destrói solução. -/
theorem a_propagacao_preserva : ∀ (k : ℕ) (φ : CNF n), SAT (propaga k φ) ↔ SAT φ
  | 0, _ => Iff.rfl
  | k + 1, φ => by
    simp only [propaga]
    split
    · exact Iff.rfl
    · split
      · next l hl =>
        rw [a_propagacao_preserva k (fixa φ l)]
        exact (a_unidade_forca_o_lado (unidade_some hl)).symm
      · exact Iff.rfl

theorem a_unidade_remove (φ : CNF n) {l : Literal n} (h : [l] ∈ φ) : tamanho (fixa φ l) < tamanho φ :=
  tamanho_restringe_lt φ l.var l.pos ⟨[l], h, l, List.mem_singleton.mpr rfl, rfl⟩

/-- A propagação com o combustível do tamanho para: morre, ou não resta cláusula unitária. -/
theorem a_propagacao_para : ∀ (k : ℕ) (φ : CNF n), tamanho φ ≤ k →
    morta (propaga k φ) = true ∨ unidade (propaga k φ) = none
  | 0, φ, h => by
    have h0 : φ = [] := tamanho_zero (by omega)
    subst h0
    right
    rfl
  | k + 1, φ, h => by
    simp only [propaga]
    split
    · next hm => exact Or.inl hm
    · split
      · next l hl =>
        apply a_propagacao_para k
        have := a_unidade_remove φ (unidade_some hl)
        omega
      · next hl => exact Or.inr hl

theorem tamanho_propaga_le : ∀ (k : ℕ) (φ : CNF n), tamanho (propaga k φ) ≤ tamanho φ
  | 0, _ => le_rfl
  | k + 1, φ => by
    simp only [propaga]
    split
    · exact le_rfl
    · split
      · next l _ => exact le_trans (tamanho_propaga_le k (fixa φ l)) (tamanho_fixa_le φ l)
      · exact le_rfl

/-! ## 3. O empurrão e o compromisso -/

/-- [DEF] O LADO MORRE LOGO: fixar `l` e propagar dá a morte no zero absoluto. -/
def morreLogo (ψ : CNF n) (l : Literal n) : Bool := morta (propaga (tamanho ψ) (fixa ψ l))

/-- [DEF] Dois literais iguais. -/
def mesmoLiteral (l m : Literal n) : Bool := l.var == m.var && l.pos == m.pos

/-- [DEF] Duas cláusulas iguais, literal a literal. -/
def mesma : Clausula n → Clausula n → Bool
  | [], [] => true
  | l :: C, m :: D => mesmoLiteral l m && mesma C D
  | [], _ :: _ => false
  | _ :: _, [] => false

/-- [DEF] Toda cláusula de `φ'` é uma cláusula de `ψ`: nenhuma foi cortada ao meio. -/
def contida (φ' ψ : CNF n) : Bool := φ'.all fun C => ψ.any fun D => mesma C D

/-- [DEF] O LANCE: empurrar para o lado oposto de `l`, ou comprometer-se com `l`. -/
inductive Lance (n : ℕ)
  | empurra (l : Literal n)
  | compromete (l : Literal n)

/-- [DEF] A SONDA: percorre os literais; o primeiro cujo lado morre logo dá o empurrão; o primeiro cujo lado não corta
nenhuma cláusula ao meio dá o compromisso. -/
def sonda (ψ : CNF n) : List (Literal n) → Option (Lance n)
  | [] => none
  | l :: ls =>
    let lado := propaga (tamanho ψ) (fixa ψ l)
    if morta lado = true then some (.empurra l)
    else if contida lado ψ = true then some (.compromete l)
    else sonda ψ ls

/-- [DEF] O TRIVIAL: tudo falso, ou tudo verdadeiro, satisfaz a fórmula. -/
def passaTrivial (φ : CNF n) : Bool :=
  (φ.all fun C => satisfeita C fun _ => false) || (φ.all fun C => satisfeita C fun _ => true)

theorem literal_ext {l m : Literal n} (hv : l.var = m.var) (hp : l.pos = m.pos) : l = m := by
  cases l
  cases m
  simp_all

theorem mesma_eq : ∀ {C D : Clausula n}, mesma C D = true → C = D
  | [], [], _ => rfl
  | l :: C, m :: D, h => by
    simp only [mesma, mesmoLiteral, Bool.and_eq_true, beq_iff_eq] at h
    obtain ⟨⟨hv, hp⟩, hCD⟩ := h
    rw [mesma_eq hCD, literal_ext hv hp]
  | [], _ :: _, h => by simp [mesma] at h
  | _ :: _, [], h => by simp [mesma] at h

theorem contida_sat {φ' ψ : CNF n} (h : contida φ' ψ = true) (hs : SAT ψ) : SAT φ' := by
  obtain ⟨x, hx⟩ := hs
  refine ⟨x, fun C hC => ?_⟩
  obtain ⟨D, hD, hCD⟩ := List.any_eq_true.mp (List.all_eq_true.mp h C hC)
  rw [mesma_eq hCD]
  exact hx D hD

/-- ★ O TRIVIAL DIZ SIM. -/
theorem o_trivial_diz_sim {φ : CNF n} (h : passaTrivial φ = true) : SAT φ := by
  unfold passaTrivial at h
  cases hf : φ.all (fun C => satisfeita C fun _ => false)
  · rw [hf, Bool.false_or] at h
    exact ⟨fun _ => true, fun C hC => List.all_eq_true.mp h C hC⟩
  · exact ⟨fun _ => false, fun C hC => List.all_eq_true.mp hf C hC⟩

theorem sonda_empurra : ∀ {ψ : CNF n} {ls : List (Literal n)} {l : Literal n},
    sonda ψ ls = some (.empurra l) → morreLogo ψ l = true
  | _, [], _, h => by simp [sonda] at h
  | ψ, m :: ls, l, h => by
    simp only [sonda] at h
    split at h
    · next hm =>
      simp only [Option.some.injEq, Lance.empurra.injEq] at h
      rw [← h]
      exact hm
    · split at h
      · simp at h
      · exact sonda_empurra h

theorem sonda_compromete : ∀ {ψ : CNF n} {ls : List (Literal n)} {l : Literal n},
    sonda ψ ls = some (.compromete l) → contida (propaga (tamanho ψ) (fixa ψ l)) ψ = true
  | _, [], _, h => by simp [sonda] at h
  | ψ, m :: ls, l, h => by
    simp only [sonda] at h
    split at h
    · simp at h
    · split at h
      · next hc =>
        simp only [Option.some.injEq, Lance.compromete.injEq] at h
        rw [← h]
        exact hc
      · exact sonda_compromete h

/-- ★★ O ZERO ABSOLUTO EMPURRA PARA O LADO OPOSTO: se o lado `l` morre logo, ter solução é ter solução no lado
oposto. -/
theorem o_zero_empurra_para_o_lado_oposto {ψ : CNF n} {l : Literal n} (h : morreLogo ψ l = true) :
    SAT ψ ↔ SAT (fixa ψ (oposto l)) := by
  have hm : morta (propaga (tamanho ψ) (fixa ψ l)) = true := h
  have hd : ¬ SAT (fixa ψ l) := fun hs =>
    a_morte_e_o_nao hm ((a_propagacao_preserva (tamanho ψ) (fixa ψ l)).mpr hs)
  obtain ⟨i, p⟩ := l
  change ¬ SAT (restringe ψ i p) at hd
  show SAT ψ ↔ SAT (restringe ψ i (!p))
  rw [a_proposta_nasce_da_escolha_do_nome ψ i]
  constructor
  · rintro ⟨b, hb⟩
    cases b <;> cases p
    · exact absurd hb hd
    · exact hb
    · exact hb
    · exact absurd hb hd
  · intro hs
    exact ⟨!p, hs⟩

/-- ★ O LADO QUE NÃO CORTA É SEGURO: se fixar `l` e propagar não corta nenhuma cláusula ao meio, ter solução é ter
solução no lado `l`. -/
theorem o_lado_que_nao_corta_e_seguro {ψ : CNF n} {l : Literal n}
    (h : contida (propaga (tamanho ψ) (fixa ψ l)) ψ = true) : SAT ψ ↔ SAT (fixa ψ l) := by
  constructor
  · intro hs
    exact (a_propagacao_preserva (tamanho ψ) (fixa ψ l)).mp (contida_sat h hs)
  · intro hs
    obtain ⟨i, p⟩ := l
    exact (a_proposta_nasce_da_escolha_do_nome ψ i).mpr ⟨p, hs⟩

/-! ## 4. A inclinação -/

/-- [DEF] A INCLINAÇÃO: propagar; morrer ou dizer sim; senão empurrar ou se comprometer; senão ficar na fronteira. -/
def inclina : ℕ → CNF n → Veredito
  | 0, _ => .indeciso
  | k + 1, φ =>
    let ψ := propaga (tamanho φ) φ
    if morta ψ = true then .nao
    else if passaTrivial ψ = true then .sim
    else match sonda ψ ψ.flatten with
      | some (.empurra l) => inclina k (fixa ψ (oposto l))
      | some (.compromete l) => inclina k (fixa ψ l)
      | none => .indeciso

/-- [DEF] A inclinação com o combustível do tamanho. -/
def aInclinacao (φ : CNF n) : Veredito := inclina (tamanho φ + 1) φ

/-- ★★★ A INCLINAÇÃO NÃO ERRA: quando diz sim, há solução; quando diz não, não há. -/
theorem a_inclinacao_nao_erra : ∀ (k : ℕ) (φ : CNF n),
    (inclina k φ = .sim → SAT φ) ∧ (inclina k φ = .nao → ¬ SAT φ)
  | 0, _ => by simp [inclina]
  | k + 1, φ => by
    have hp := a_propagacao_preserva (tamanho φ) φ
    simp only [inclina]
    generalize propaga (tamanho φ) φ = ψ at hp ⊢
    split
    · next hm => exact ⟨(fun h => nomatch h), fun _ hs => a_morte_e_o_nao hm (hp.mpr hs)⟩
    · split
      · next ht => exact ⟨fun _ => hp.mp (o_trivial_diz_sim ht), (fun h => nomatch h)⟩
      · split
        · next l hs =>
          have he := o_zero_empurra_para_o_lado_oposto (sonda_empurra hs)
          have ih := a_inclinacao_nao_erra k (fixa ψ (oposto l))
          exact ⟨fun h => hp.mp (he.mpr (ih.1 h)), fun h hs' => ih.2 h (he.mp (hp.mpr hs'))⟩
        · next l hs =>
          have he := o_lado_que_nao_corta_e_seguro (sonda_compromete hs)
          have ih := a_inclinacao_nao_erra k (fixa ψ l)
          exact ⟨fun h => hp.mp (he.mpr (ih.1 h)), fun h hs' => ih.2 h (he.mp (hp.mpr hs'))⟩
        · exact ⟨(fun h => nomatch h), (fun h => nomatch h)⟩

/-! ## 5. Em Horn, o sistema sempre inclina -/

/-- Fixar um Nome preserva a classe de Horn da casa. -/
theorem horn_restringe {φ : CNF n} (h : IALD.CompilaHornNaFita.IsHorn φ) (i : Fin n) (b : Bool) :
    IALD.CompilaHornNaFita.IsHorn (restringe φ i b) := by
  intro C hC
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  have hDh := h D (List.mem_filter.mp hD).1
  unfold Codex.CrossSelectors.names at hDh ⊢
  rw [List.length_map] at hDh ⊢
  exact le_trans (List.Sublist.length_le (List.Sublist.filter _ List.filter_sublist)) hDh

theorem horn_propaga : ∀ (k : ℕ) {φ : CNF n}, IALD.CompilaHornNaFita.IsHorn φ →
    IALD.CompilaHornNaFita.IsHorn (propaga k φ)
  | 0, _, h => h
  | k + 1, φ, h => by
    simp only [propaga]
    split
    · exact h
    · split
      · next l _ => exact horn_propaga k (horn_restringe h l.var l.pos)
      · exact h

/-- Uma cláusula de Horn com dois literais ou mais tem um literal negativo. -/
theorem tem_negativo {C : Clausula n} (hC : (Codex.CrossSelectors.names C true).length ≤ 1)
    (h2 : 2 ≤ C.length) : ∃ l ∈ C, l.pos = false := by
  by_contra hno
  have hall : C.filter (fun l => l.pos == true) = C := by
    apply List.filter_eq_self.mpr
    intro l hl
    have hne : l.pos ≠ false := fun h => hno ⟨l, hl, h⟩
    simpa using hne
  unfold Codex.CrossSelectors.names at hC
  rw [hall, List.length_map] at hC
  omega

theorem dois_ou_mais : ∀ {C : Clausula n}, vazia C = false → unitario C = none → 2 ≤ C.length
  | [], hv, _ => by simp [vazia] at hv
  | [_], _, hu => by simp [unitario] at hu
  | _ :: _ :: _, _, _ => by simp only [List.length_cons]; omega

theorem morta_falsa {φ : CNF n} (h : morta φ = false) : ∀ C ∈ φ, vazia C = false := by
  intro C hC
  unfold morta at h
  have h0 := List.any_eq_false.mp h C hC
  simpa using h0

/-- No ponto fixo da propagação, uma fórmula de Horn viva passa no trivial (tudo falso). -/
theorem horn_no_ponto_fixo_diz_sim {ψ : CNF n} (hh : IALD.CompilaHornNaFita.IsHorn ψ)
    (hm : morta ψ = false) (hu : unidade ψ = none) : passaTrivial ψ = true := by
  have hf : (ψ.all fun C => satisfeita C fun _ => false) = true := by
    rw [List.all_eq_true]
    intro C hC
    obtain ⟨l, hl, hp⟩ := tem_negativo (hh C hC) (dois_ou_mais (morta_falsa hm C hC) (unidade_none hu C hC))
    unfold satisfeita
    rw [List.any_eq_true]
    exact ⟨l, hl, by simp [Literal.vale, hp]⟩
  unfold passaTrivial
  rw [hf, Bool.true_or]

/-- ★★★ EM HORN O SISTEMA SEMPRE INCLINA: em toda fórmula de Horn (a classe `IsHorn` da casa) a inclinação diz sim ou
morre na primeira volta; nunca fica na fronteira. -/
theorem em_horn_o_sistema_sempre_inclina {φ : CNF n} (h : IALD.CompilaHornNaFita.IsHorn φ) (k : ℕ) :
    inclina (k + 1) φ ≠ .indeciso := by
  have hpf := a_propagacao_para (tamanho φ) φ le_rfl
  have hh := horn_propaga (tamanho φ) h
  simp only [inclina]
  generalize propaga (tamanho φ) φ = ψ at hpf hh ⊢
  split
  · exact fun h => by cases h
  · next hm =>
    split
    · exact fun h => by cases h
    · next ht =>
      exfalso
      rcases hpf with hpf | hpf
      · exact hm hpf
      · exact ht (horn_no_ponto_fixo_diz_sim hh (by simpa using hm) hpf)

/-- ★★ EM HORN A INCLINAÇÃO DECIDE: diz sim exatamente quando há solução, e diz não exatamente quando não há. -/
theorem em_horn_a_inclinacao_decide {φ : CNF n} (h : IALD.CompilaHornNaFita.IsHorn φ) :
    (aInclinacao φ = .sim ↔ SAT φ) ∧ (aInclinacao φ = .nao ↔ ¬ SAT φ) := by
  have hc := a_inclinacao_nao_erra (tamanho φ + 1) φ
  have hd := em_horn_o_sistema_sempre_inclina h (tamanho φ)
  unfold aInclinacao
  cases hv : inclina (tamanho φ + 1) φ with
  | sim =>
    have hs : SAT φ := hc.1 hv
    exact ⟨⟨fun _ => hs, fun _ => rfl⟩, ⟨(fun h => nomatch h), fun hn => absurd hs hn⟩⟩
  | nao =>
    have hn : ¬ SAT φ := hc.2 hv
    exact ⟨⟨(fun h => nomatch h), fun hs => absurd hs hn⟩, ⟨fun _ => hn, fun _ => rfl⟩⟩
  | indeciso => exact absurd hv hd

/-! ## 5b. Em dois literais, todo lado morre logo ou não corta nada (R1) -/

/-- [DEF] As fórmulas de dois literais: toda cláusula tem no máximo dois literais. -/
def DoisLiterais (φ : CNF n) : Prop := ∀ C ∈ φ, C.length ≤ 2

/-- Fixar um Nome preserva os dois literais. -/
theorem dois_restringe {φ : CNF n} (h : DoisLiterais φ) (i : Fin n) (b : Bool) : DoisLiterais (restringe φ i b) := by
  intro C hC
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  exact le_trans (List.length_filter_le _ D) (h D (List.mem_filter.mp hD).1)

theorem dois_propaga : ∀ (k : ℕ) {φ : CNF n}, DoisLiterais φ → DoisLiterais (propaga k φ)
  | 0, _, h => h
  | k + 1, φ, h => by
    simp only [propaga]
    split
    · exact h
    · split
      · next l _ => exact dois_propaga k (dois_restringe h l.var l.pos)
      · exact h

/-- [DEF] A INTEGRIDADE: toda cláusula de `φ` é uma cláusula original de `ψ`, ou tem no máximo um literal. -/
def Integra (ψ φ : CNF n) : Prop := ∀ C ∈ φ, C ∈ ψ ∨ C.length ≤ 1

theorem integra_inicio (ψ : CNF n) : Integra ψ ψ := fun _ hC => Or.inl hC

/-- Em dois literais, fixar um Nome preserva a integridade: a cláusula original ou fica inteira, ou cai para um literal. -/
theorem integra_restringe {ψ φ : CNF n} (h2 : ∀ C ∈ ψ, C.length = 2) (h : Integra ψ φ) (i : Fin n) (b : Bool) :
    Integra ψ (restringe φ i b) := by
  intro C hC
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  rcases h D (List.mem_filter.mp hD).1 with hDψ | hD1
  · by_cases hv : ∃ m ∈ D, m.var = i
    · right
      have hlt := filtra_encurta D i hv
      have h2D := h2 D hDψ
      omega
    · left
      have hfix : (D.filter fun l => l.var ≠ i) = D := by
        apply List.filter_eq_self.mpr
        intro m hm
        have hne : m.var ≠ i := fun he => hv ⟨m, hm, he⟩
        simpa using hne
      rw [hfix]
      exact hDψ
  · right
    exact le_trans (List.length_filter_le _ D) hD1

theorem integra_propaga {ψ : CNF n} (h2 : ∀ C ∈ ψ, C.length = 2) :
    ∀ (k : ℕ) {φ : CNF n}, Integra ψ φ → Integra ψ (propaga k φ)
  | 0, _, h => h
  | k + 1, φ, h => by
    simp only [propaga]
    split
    · exact h
    · split
      · next l _ => exact integra_propaga h2 k (integra_restringe h2 h l.var l.pos)
      · exact h

theorem mesma_refl : ∀ C : Clausula n, mesma C C = true
  | [] => rfl
  | l :: C => by simp [mesma, mesmoLiteral, mesma_refl C]

theorem contida_de_inclusao {φ' ψ : CNF n} (h : ∀ C ∈ φ', C ∈ ψ) : contida φ' ψ = true := by
  unfold contida
  rw [List.all_eq_true]
  intro C hC
  rw [List.any_eq_true]
  exact ⟨C, h C hC, mesma_refl C⟩

/-- ★★ EM DOIS LITERAIS, TODO LADO MORRE LOGO OU NÃO CORTA NADA (a autarquia): numa fórmula em que toda cláusula tem dois
literais, fixar qualquer literal e propagar dá a morte, ou deixa só cláusulas originais. -/
theorem todo_lado_morre_ou_nao_corta {ψ : CNF n} (h2 : ∀ C ∈ ψ, C.length = 2) (l : Literal n) :
    morta (propaga (tamanho ψ) (fixa ψ l)) = true ∨ contida (propaga (tamanho ψ) (fixa ψ l)) ψ = true := by
  have hpara := a_propagacao_para (tamanho ψ) (fixa ψ l) (tamanho_fixa_le ψ l)
  have hint : Integra ψ (propaga (tamanho ψ) (fixa ψ l)) :=
    integra_propaga h2 (tamanho ψ) (integra_restringe h2 (integra_inicio ψ) l.var l.pos)
  by_cases hm : morta (propaga (tamanho ψ) (fixa ψ l)) = true
  · exact Or.inl hm
  · right
    have hu : unidade (propaga (tamanho ψ) (fixa ψ l)) = none := hpara.resolve_left hm
    apply contida_de_inclusao
    intro C hC
    rcases hint C hC with hCψ | hC1
    · exact hCψ
    · exfalso
      have h1 := dois_ou_mais (morta_falsa (by simpa using hm) C hC) (unidade_none hu C hC)
      omega

/-- A sonda age já no primeiro literal: empurra ou se compromete. -/
theorem sonda_age {ψ : CNF n} (h2 : ∀ C ∈ ψ, C.length = 2) (a : Literal n) (ls : List (Literal n)) :
    sonda ψ (a :: ls) = some (.empurra a) ∨ sonda ψ (a :: ls) = some (.compromete a) := by
  simp only [sonda]
  by_cases hm : morta (propaga (tamanho ψ) (fixa ψ a)) = true
  · left
    rw [if_pos hm]
  · right
    rw [if_neg hm, if_pos ((todo_lado_morre_ou_nao_corta h2 a).resolve_left hm)]

/-- Uma fórmula não vazia de cláusulas de dois literais começa por um literal que aparece nela. -/
theorem primeiro_literal : ∀ {ψ : CNF n}, ψ ≠ [] → (∀ C ∈ ψ, C.length = 2) →
    ∃ a ls, ψ.flatten = a :: ls ∧ ∃ C ∈ ψ, a ∈ C
  | [], hne, _ => absurd rfl hne
  | [] :: _, _, h2 => by
    have h0 := h2 [] List.mem_cons_self
    simp at h0
  | (a :: C) :: rest, _, _ => ⟨a, C ++ rest.flatten, by simp, a :: C, List.mem_cons_self, List.mem_cons_self⟩

/-- ★★★ EM DOIS LITERAIS O SISTEMA SEMPRE INCLINA: com combustível maior que o tamanho, a inclinação de toda fórmula de
dois literais diz sim ou morre; nunca fica na fronteira. -/
theorem em_dois_literais_o_sistema_sempre_inclina : ∀ (k : ℕ) (φ : CNF n), DoisLiterais φ → tamanho φ < k →
    inclina k φ ≠ .indeciso
  | 0, _, _, hk => absurd hk (Nat.not_lt_zero _)
  | k + 1, φ, h, hk => by
    have hpf := a_propagacao_para (tamanho φ) φ le_rfl
    have hd := dois_propaga (tamanho φ) h
    have hψ := tamanho_propaga_le (tamanho φ) φ
    simp only [inclina]
    generalize propaga (tamanho φ) φ = ψ at hpf hd hψ ⊢
    split
    · exact fun h => nomatch h
    · next hm =>
      split
      · exact fun h => nomatch h
      · next ht =>
        have hu : unidade ψ = none := hpf.resolve_left hm
        have h2 : ∀ C ∈ ψ, C.length = 2 := by
          intro C hC
          have h1 := dois_ou_mais (morta_falsa (by simpa using hm) C hC) (unidade_none hu C hC)
          have h3 := hd C hC
          omega
        have hne : ψ ≠ [] := by
          rintro rfl
          exact ht rfl
        obtain ⟨a, ls, hfl, C, hC, haC⟩ := primeiro_literal hne h2
        have hlt : ∀ b : Bool, tamanho (restringe ψ a.var b) < k := by
          intro b
          have := tamanho_restringe_lt ψ a.var b ⟨C, hC, a, haC, rfl⟩
          omega
        rw [hfl]
        rcases sonda_age h2 a ls with hs | hs
        · rw [hs]
          exact em_dois_literais_o_sistema_sempre_inclina k (fixa ψ (oposto a))
            (dois_restringe hd a.var (!a.pos)) (hlt (!a.pos))
        · rw [hs]
          exact em_dois_literais_o_sistema_sempre_inclina k (fixa ψ a) (dois_restringe hd a.var a.pos) (hlt a.pos)

/-- Quando a inclinação não para na fronteira, ela decide: diz sim exatamente quando há solução. -/
theorem a_inclinacao_que_nao_para_decide {k : ℕ} {φ : CNF n} (hd : inclina k φ ≠ .indeciso) :
    (inclina k φ = .sim ↔ SAT φ) ∧ (inclina k φ = .nao ↔ ¬ SAT φ) := by
  have hc := a_inclinacao_nao_erra k φ
  cases hv : inclina k φ with
  | sim =>
    have hs : SAT φ := hc.1 hv
    exact ⟨⟨fun _ => hs, fun _ => rfl⟩, ⟨(fun h => nomatch h), fun hn => absurd hs hn⟩⟩
  | nao =>
    have hn : ¬ SAT φ := hc.2 hv
    exact ⟨⟨(fun h => nomatch h), fun hs => absurd hs hn⟩, ⟨fun _ => hn, fun _ => rfl⟩⟩
  | indeciso => exact absurd hv hd

/-- ★★ EM DOIS LITERAIS A INCLINAÇÃO DECIDE: diz sim exatamente quando há solução, e diz não exatamente quando não há. -/
theorem em_dois_literais_a_inclinacao_decide {φ : CNF n} (h : DoisLiterais φ) :
    (aInclinacao φ = .sim ↔ SAT φ) ∧ (aInclinacao φ = .nao ↔ ¬ SAT φ) :=
  a_inclinacao_que_nao_para_decide
    (em_dois_literais_o_sistema_sempre_inclina (tamanho φ + 1) φ h (Nat.lt_succ_self _))

/-! ## 6. O custo -/

/-- [DEF] As fixações feitas pela propagação. -/
def custoPropaga : ℕ → CNF n → ℕ
  | 0, _ => 0
  | k + 1, φ =>
    if morta φ = true then 0
    else match unidade φ with
      | some l => custoPropaga k (fixa φ l) + 1
      | none => 0

theorem custoPropaga_le : ∀ (k : ℕ) (φ : CNF n), custoPropaga k φ ≤ k
  | 0, _ => le_rfl
  | k + 1, φ => by
    simp only [custoPropaga]
    split
    · omega
    · split
      · next l _ =>
        have := custoPropaga_le k (fixa φ l)
        omega
      · omega

/-- [DEF] As fixações feitas pela sonda (cada literal sondado: uma fixação e a sua propagação). -/
def custoSonda (ψ : CNF n) : List (Literal n) → ℕ
  | [] => 0
  | l :: ls =>
    custoPropaga (tamanho ψ) (fixa ψ l) + 1 +
      (if morreLogo ψ l = true then 0
       else if contida (propaga (tamanho ψ) (fixa ψ l)) ψ = true then 0
       else custoSonda ψ ls)

theorem custoSonda_le (ψ : CNF n) : ∀ ls : List (Literal n), custoSonda ψ ls ≤ ls.length * (tamanho ψ + 1)
  | [] => by simp [custoSonda]
  | l :: ls => by
    simp only [custoSonda, List.length_cons]
    have h1 := custoPropaga_le (tamanho ψ) (fixa ψ l)
    have h2 := custoSonda_le ψ ls
    split
    · nlinarith
    · split
      · nlinarith
      · nlinarith

/-- [DEF] As fixações feitas pela inclinação. -/
def custoInclina : ℕ → CNF n → ℕ
  | 0, _ => 0
  | k + 1, φ =>
    let ψ := propaga (tamanho φ) φ
    custoPropaga (tamanho φ) φ +
      (if morta ψ = true then 0
       else if passaTrivial ψ = true then 0
       else custoSonda ψ ψ.flatten +
         match sonda ψ ψ.flatten with
         | some (.empurra l) => custoInclina k (fixa ψ (oposto l)) + 1
         | some (.compromete l) => custoInclina k (fixa ψ l) + 1
         | none => 0)

theorem letras_le_tamanho : ∀ (φ : CNF n), φ.flatten.length ≤ tamanho φ
  | [] => by simp [tamanho]
  | C :: φ => by
    rw [List.flatten_cons, List.length_append, tamanho_cons]
    have := letras_le_tamanho φ
    omega

theorem custoInclina_le : ∀ (k : ℕ) (φ : CNF n), custoInclina k φ ≤ k * (tamanho φ + 1) ^ 2
  | 0, _ => by simp [custoInclina]
  | k + 1, φ => by
    simp only [custoInclina]
    have hP := custoPropaga_le (tamanho φ) φ
    have hψ := tamanho_propaga_le (tamanho φ) φ
    generalize propaga (tamanho φ) φ = ψ at hψ ⊢
    have hS : custoSonda ψ ψ.flatten ≤ tamanho φ * (tamanho φ + 1) :=
      le_trans (custoSonda_le ψ ψ.flatten)
        (Nat.mul_le_mul (le_trans (letras_le_tamanho ψ) hψ) (by omega))
    split
    · nlinarith
    · split
      · nlinarith
      · split
        · next l _ =>
          have ih := custoInclina_le k (fixa ψ (oposto l))
          have hT : tamanho (fixa ψ (oposto l)) ≤ tamanho φ := le_trans (tamanho_fixa_le ψ _) hψ
          have hq : k * (tamanho (fixa ψ (oposto l)) + 1) ^ 2 ≤ k * (tamanho φ + 1) ^ 2 :=
            Nat.mul_le_mul_left k (Nat.pow_le_pow_left (by omega) 2)
          nlinarith
        · next l _ =>
          have ih := custoInclina_le k (fixa ψ l)
          have hT : tamanho (fixa ψ l) ≤ tamanho φ := le_trans (tamanho_fixa_le ψ _) hψ
          have hq : k * (tamanho (fixa ψ l) + 1) ^ 2 ≤ k * (tamanho φ + 1) ^ 2 :=
            Nat.mul_le_mul_left k (Nat.pow_le_pow_left (by omega) 2)
          nlinarith
        · nlinarith

/-- ★★ O CUSTO DA INCLINAÇÃO: no máximo (T+1)³ fixações, com T o tamanho da fórmula. -/
theorem o_custo_da_inclinacao (φ : CNF n) : custoInclina (tamanho φ + 1) φ ≤ (tamanho φ + 1) ^ 3 := by
  have h := custoInclina_le (tamanho φ + 1) φ
  calc custoInclina (tamanho φ + 1) φ ≤ (tamanho φ + 1) * (tamanho φ + 1) ^ 2 := h
    _ = (tamanho φ + 1) ^ 3 := by ring

/-! ## 7. A fronteira e os exemplos -/

/-- [DEF] As oito cláusulas de três literais sobre três Nomes: cada uma exclui uma atribuição. -/
def oito : CNF 3 :=
  [[⟨0, true⟩, ⟨1, true⟩, ⟨2, true⟩], [⟨0, true⟩, ⟨1, true⟩, ⟨2, false⟩],
   [⟨0, true⟩, ⟨1, false⟩, ⟨2, true⟩], [⟨0, true⟩, ⟨1, false⟩, ⟨2, false⟩],
   [⟨0, false⟩, ⟨1, true⟩, ⟨2, true⟩], [⟨0, false⟩, ⟨1, true⟩, ⟨2, false⟩],
   [⟨0, false⟩, ⟨1, false⟩, ⟨2, true⟩], [⟨0, false⟩, ⟨1, false⟩, ⟨2, false⟩]]

theorem beq_nao (b : Bool) : (b == !b) = false := by cases b <;> rfl

/-- As oito cláusulas não têm solução: cada atribuição viola a cláusula feita do seu oposto. -/
theorem oito_sem_solucao : ¬ SAT oito := by
  rintro ⟨x, hx⟩
  have hmem : ([⟨0, !x 0⟩, ⟨1, !x 1⟩, ⟨2, !x 2⟩] : Clausula 3) ∈ oito := by
    unfold oito
    cases h0 : x 0 <;> cases h1 : x 1 <;> cases h2 : x 2 <;> simp
  have h := hx _ hmem
  have h' : ((x 0 == !x 0) || ((x 1 == !x 1) || ((x 2 == !x 2) || false))) = true := h
  rw [beq_nao, beq_nao, beq_nao] at h'
  exact absurd h' (by decide)

/-- ★★ A MORTE DISTANTE É A FRONTEIRA: nas oito cláusulas a inclinação fica indecisa. Nenhum lado morre logo, e todo lado
corta cláusulas ao meio: a morte existe (`oito_sem_solucao`), mas está longe. -/
theorem oito_fica_na_fronteira : aInclinacao oito = .indeciso := by decide

/-- [DEF] Sinais da sonda (para os exemplos). -/
def ehEmpurrao : Option (Lance n) → Bool
  | some (.empurra _) => true
  | _ => false

def ehCompromisso : Option (Lance n) → Bool
  | some (.compromete _) => true
  | _ => false

/-- [DEF] Quatro cláusulas de dois literais sobre dois Nomes. -/
def quatro : CNF 2 :=
  [[⟨0, true⟩, ⟨1, true⟩], [⟨0, true⟩, ⟨1, false⟩], [⟨0, false⟩, ⟨1, true⟩], [⟨0, false⟩, ⟨1, false⟩]]

/-- ★ O EMPURRÃO DIZ NÃO: sem cláusula unitária a propagação não começa; o primeiro lado morre logo, o empurrão leva ao
oposto, que também morre: a morte no zero absoluto. -/
theorem quatro_o_empurrao_diz_nao :
    (unidade quatro).isNone = true ∧ ehEmpurrao (sonda quatro quatro.flatten) = true ∧ aInclinacao quatro = .nao := by
  decide

/-- [DEF] Três cláusulas sobre três Nomes, com solução. -/
def oEmpurrao : CNF 3 := [[⟨0, false⟩, ⟨2, false⟩], [⟨0, true⟩, ⟨1, true⟩], [⟨0, true⟩, ⟨1, false⟩]]

/-- ★ O EMPURRÃO DIZ SIM: nem tudo falso nem tudo verdadeiro serve e não há cláusula unitária; o lado x₀ = 0 morre logo e
o empurrão leva a x₀ = 1, onde há solução. -/
theorem o_empurrao_diz_sim :
    (unidade oEmpurrao).isNone = true ∧ passaTrivial oEmpurrao = false ∧
      ehEmpurrao (sonda oEmpurrao oEmpurrao.flatten) = true ∧ aInclinacao oEmpurrao = .sim := by
  decide

/-- [DEF] Duas cláusulas de dois literais sobre dois Nomes, com solução. -/
def dois : CNF 2 := [[⟨0, true⟩, ⟨1, true⟩], [⟨0, false⟩, ⟨1, false⟩]]

/-- ★ O COMPROMISSO DIZ SIM: nenhum lado morre logo; o lado x₀ = 1 não corta nenhuma cláusula ao meio, e o compromisso
com ele leva à solução. -/
theorem dois_o_compromisso_diz_sim :
    (unidade dois).isNone = true ∧ passaTrivial dois = false ∧
      ehCompromisso (sonda dois dois.flatten) = true ∧ aInclinacao dois = .sim := by
  decide

/-- [DEF] Uma cadeia de dois literais sobre quatro Nomes, com solução. -/
def cadeia : CNF 4 :=
  [[⟨0, false⟩, ⟨1, true⟩], [⟨1, false⟩, ⟨2, true⟩], [⟨2, false⟩, ⟨3, true⟩], [⟨0, true⟩, ⟨3, true⟩],
   [⟨3, false⟩, ⟨0, false⟩]]

/-- ★ A CADEIA INCLINA E DIZ SIM: nem tudo falso nem tudo verdadeiro serve e não há cláusula unitária; o primeiro lado
(x₀ = 0), propagado, não corta nenhuma cláusula ao meio; o compromisso com ele leva à solução na segunda volta. -/
theorem a_cadeia_inclina_e_diz_sim :
    DoisLiterais cadeia ∧ passaTrivial cadeia = false ∧ ehCompromisso (sonda cadeia cadeia.flatten) = true ∧
      aInclinacao cadeia = .sim :=
  ⟨by show ∀ C ∈ cadeia, C.length ≤ 2; decide, by decide⟩

/-! ## 8. A síntese -/

/-- ★★★ A TRINDADE:
    (1) O PAR: a fórmula tem solução se, e só se, um dos dois lados do Nome tem (a tensão do Kimi); e o lado que morre
        logo empurra para o oposto.
    (2) O EMPURRÃO: a inclinação nunca erra, decide toda fórmula de Horn e toda fórmula de dois literais, e custa no
        máximo (T+1)³ fixações.
    (3) A FRONTEIRA: há fórmula de três literais sem solução em que a inclinação fica indecisa: a morte está longe. -/
theorem a_trindade :
    (∀ (φ : CNF n) (i : Fin n), SAT φ ↔ ∃ b : Bool, SAT (restringe φ i b))
    ∧ (∀ (ψ : CNF n) (l : Literal n), morreLogo ψ l = true → (SAT ψ ↔ SAT (fixa ψ (oposto l))))
    ∧ (∀ (k : ℕ) (φ : CNF n), (inclina k φ = .sim → SAT φ) ∧ (inclina k φ = .nao → ¬ SAT φ))
    ∧ (∀ φ : CNF n, IALD.CompilaHornNaFita.IsHorn φ → aInclinacao φ ≠ .indeciso)
    ∧ (∀ φ : CNF n, DoisLiterais φ → aInclinacao φ ≠ .indeciso)
    ∧ (∀ φ : CNF n, custoInclina (tamanho φ + 1) φ ≤ (tamanho φ + 1) ^ 3)
    ∧ (¬ SAT oito ∧ aInclinacao oito = .indeciso) :=
  ⟨a_proposta_nasce_da_escolha_do_nome, fun _ _ h => o_zero_empurra_para_o_lado_oposto h,
   a_inclinacao_nao_erra, fun φ h => em_horn_o_sistema_sempre_inclina h (tamanho φ),
   fun φ h => em_dois_literais_o_sistema_sempre_inclina (tamanho φ + 1) φ h (Nat.lt_succ_self _),
   o_custo_da_inclinacao, oito_sem_solucao, oito_fica_na_fronteira⟩

/-! ## 9. A fronteira é o terceiro literal (R2) -/

/-- [DEF] O LADO: fixar `l` e propagar. -/
def lado (ψ : CNF n) (l : Literal n) : CNF n := propaga (tamanho ψ) (fixa ψ l)

/-- [DEF] O RESTO NA FRONTEIRA: vivo, sem unidade, não trivial, e a sonda não age em nenhum literal. -/
abbrev NaFronteira (ψ : CNF n) : Prop :=
  morta ψ = false ∧ (unidade ψ).isNone = true ∧ passaTrivial ψ = false ∧ (sonda ψ ψ.flatten).isNone = true

/-- [DEF] DENTRO: toda cláusula de `φ` é uma sublista de uma cláusula original de `ψ`. -/
def Dentro (ψ φ : CNF n) : Prop := ∀ C ∈ φ, ∃ D ∈ ψ, C.Sublist D

theorem dentro_inicio (ψ : CNF n) : Dentro ψ ψ := fun C hC => ⟨C, hC, List.Sublist.refl C⟩

theorem dentro_restringe {ψ φ : CNF n} (h : Dentro ψ φ) (i : Fin n) (b : Bool) : Dentro ψ (restringe φ i b) := by
  intro C hC
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  obtain ⟨E, hE, hDE⟩ := h D (List.mem_filter.mp hD).1
  exact ⟨E, hE, List.Sublist.trans List.filter_sublist hDE⟩

theorem dentro_propaga {ψ : CNF n} : ∀ (k : ℕ) {φ : CNF n}, Dentro ψ φ → Dentro ψ (propaga k φ)
  | 0, _, h => h
  | k + 1, φ, h => by
    simp only [propaga]
    split
    · exact h
    · split
      · next l _ => exact dentro_propaga k (dentro_restringe h l.var l.pos)
      · exact h

theorem sonda_empurra_mem : ∀ {ψ : CNF n} {ls : List (Literal n)} {l : Literal n},
    sonda ψ ls = some (.empurra l) → l ∈ ls
  | _, [], _, h => by simp [sonda] at h
  | ψ, m :: ls, l, h => by
    simp only [sonda] at h
    split at h
    · simp only [Option.some.injEq, Lance.empurra.injEq] at h
      rw [← h]
      exact List.mem_cons_self
    · split at h
      · simp at h
      · exact List.mem_cons_of_mem _ (sonda_empurra_mem h)

theorem sonda_compromete_mem : ∀ {ψ : CNF n} {ls : List (Literal n)} {l : Literal n},
    sonda ψ ls = some (.compromete l) → l ∈ ls
  | _, [], _, h => by simp [sonda] at h
  | ψ, m :: ls, l, h => by
    simp only [sonda] at h
    split at h
    · simp at h
    · split at h
      · simp only [Option.some.injEq, Lance.compromete.injEq] at h
        rw [← h]
        exact List.mem_cons_self
      · exact List.mem_cons_of_mem _ (sonda_compromete_mem h)

/-- Quando a sonda não age, cada literal sondado deixa um lado vivo e que corta alguma cláusula. -/
theorem sonda_nada_age : ∀ {ψ : CNF n} {ls : List (Literal n)}, (sonda ψ ls).isNone = true →
    ∀ l ∈ ls, morta (lado ψ l) = false ∧ contida (lado ψ l) ψ = false
  | _, [], _, l, hl => by simp at hl
  | ψ, m :: ls, h, l, hl => by
    simp only [sonda] at h
    split at h
    · simp at h
    · next hm =>
      split at h
      · simp at h
      · next hc =>
        rcases List.mem_cons.mp hl with he | hl'
        · rw [he]
          exact ⟨by unfold lado; simpa using hm, by unfold lado; simpa using hc⟩
        · exact sonda_nada_age h l hl'

theorem contida_falsa_corta {φ' ψ : CNF n} (h : contida φ' ψ = false) : ∃ C ∈ φ', C ∉ ψ := by
  by_contra hno
  have hall : ∀ C ∈ φ', C ∈ ψ := fun C hC => by
    by_contra hCψ
    exact hno ⟨C, hC, hCψ⟩
  have h1 := contida_de_inclusao hall
  rw [h1] at h
  exact Bool.noConfusion h

theorem sublista_propria {C D : Clausula n} (h : C.Sublist D) (hne : C ≠ D) : C.length < D.length := by
  rcases Nat.lt_or_eq_of_le h.length_le with hlt | heq
  · exact hlt
  · exact absurd (h.eq_of_length heq) hne

/-- ★★★ NA FRONTEIRA TODO LADO VIVO CORTA UMA CLÁUSULA DE TRÊS: no resto onde a inclinação para, cada literal, fixado e
propagado, fica vivo e deixa uma cláusula de dois literais ou mais, cortada de uma cláusula original de três literais ou
mais: um literal caiu, os outros esperam. -/
theorem na_fronteira_todo_lado_corta_uma_de_tres {ψ : CNF n} (hf : NaFronteira ψ) :
    ∀ l ∈ ψ.flatten, morta (lado ψ l) = false ∧
      ∃ D ∈ ψ, 3 ≤ D.length ∧ ∃ C ∈ lado ψ l, C.Sublist D ∧ C ≠ D ∧ 2 ≤ C.length := by
  intro l hl
  obtain ⟨_, _, _, hs⟩ := hf
  obtain ⟨hm, hc⟩ := sonda_nada_age hs l hl
  refine ⟨hm, ?_⟩
  obtain ⟨C, hC, hCψ⟩ := contida_falsa_corta hc
  have hpara := a_propagacao_para (tamanho ψ) (fixa ψ l) (tamanho_fixa_le ψ l)
  have hu : unidade (lado ψ l) = none := by
    rcases hpara with h | h
    · exfalso
      have h0 : true = false := h.symm.trans hm
      exact Bool.noConfusion h0
    · exact h
  have h2 : 2 ≤ C.length := dois_ou_mais (morta_falsa hm C hC) (unidade_none hu C hC)
  have hdentro : Dentro ψ (lado ψ l) :=
    dentro_propaga (tamanho ψ) (dentro_restringe (dentro_inicio ψ) l.var l.pos)
  obtain ⟨D, hD, hCD⟩ := hdentro C hC
  have hne : C ≠ D := fun he => hCψ (by rw [he]; exact hD)
  have hlt := sublista_propria hCD hne
  exact ⟨D, hD, by omega, C, hC, hCD, hne, h2⟩

/-- ★★ A FRONTEIRA TEM TRÊS LITERAIS: no resto onde a inclinação para, há uma cláusula de três literais ou mais. -/
theorem a_fronteira_tem_tres_literais {ψ : CNF n} (hf : NaFronteira ψ) : ∃ D ∈ ψ, 3 ≤ D.length := by
  have hne : ψ.flatten ≠ [] := by
    obtain ⟨hm, _, ht, _⟩ := hf
    intro hfl
    rcases ψ with _ | ⟨C, rest⟩
    · simp [passaTrivial] at ht
    · rcases C with _ | ⟨a, C'⟩
      · have h0 := morta_falsa hm [] List.mem_cons_self
        simp [vazia] at h0
      · simp at hfl
  obtain ⟨l, ls, hls⟩ := List.exists_cons_of_ne_nil hne
  obtain ⟨_, D, hD, h3, _⟩ := na_fronteira_todo_lado_corta_uma_de_tres hf l (by rw [hls]; exact List.mem_cons_self)
  exact ⟨D, hD, h3⟩

/-- ★★★ A INCLINAÇÃO PARA SÓ NA FRONTEIRA: com combustível maior que o tamanho, se a inclinação fica indecisa, ela parou
num resto com a mesma resposta da fórmula, e esse resto está na fronteira. -/
theorem a_inclinacao_para_so_na_fronteira : ∀ (k : ℕ) (φ : CNF n), tamanho φ < k → inclina k φ = .indeciso →
    ∃ ψ : CNF n, (SAT ψ ↔ SAT φ) ∧ NaFronteira ψ
  | 0, _, hk, _ => absurd hk (Nat.not_lt_zero _)
  | k + 1, φ, hk, hi => by
    have hp := a_propagacao_preserva (tamanho φ) φ
    have hpf := a_propagacao_para (tamanho φ) φ le_rfl
    have hψ := tamanho_propaga_le (tamanho φ) φ
    simp only [inclina] at hi
    generalize propaga (tamanho φ) φ = ψ at hp hpf hψ hi
    split at hi
    · exact absurd hi (by decide)
    · next hm =>
      split at hi
      · exact absurd hi (by decide)
      · next ht =>
        split at hi
        · next l hs =>
          have he := o_zero_empurra_para_o_lado_oposto (sonda_empurra hs)
          obtain ⟨C, hC, hlC⟩ := List.mem_flatten.mp (sonda_empurra_mem hs)
          have hlt := tamanho_restringe_lt ψ l.var (!l.pos) ⟨C, hC, l, hlC, rfl⟩
          obtain ⟨χ, hχ, hfχ⟩ := a_inclinacao_para_so_na_fronteira k (fixa ψ (oposto l))
            (by show tamanho (restringe ψ l.var (!l.pos)) < k; omega) hi
          exact ⟨χ, hχ.trans (he.symm.trans hp), hfχ⟩
        · next l hs =>
          have he := o_lado_que_nao_corta_e_seguro (sonda_compromete hs)
          obtain ⟨C, hC, hlC⟩ := List.mem_flatten.mp (sonda_compromete_mem hs)
          have hlt := tamanho_restringe_lt ψ l.var l.pos ⟨C, hC, l, hlC, rfl⟩
          obtain ⟨χ, hχ, hfχ⟩ := a_inclinacao_para_so_na_fronteira k (fixa ψ l)
            (by show tamanho (restringe ψ l.var l.pos) < k; omega) hi
          exact ⟨χ, hχ.trans (he.symm.trans hp), hfχ⟩
        · next hs =>
          refine ⟨ψ, hp, by simpa using hm, by simp [hpf.resolve_left hm], by simpa using ht, by simp [hs]⟩

/-! ## 10. A travessia por ramificação (R2) -/

/-- [DEF] A TRAVESSIA: a inclinação; onde ela para, a máquina nua ramifica no primeiro literal do resto e segue pelos dois
lados. -/
def atravessa : ℕ → CNF n → Bool
  | 0, _ => false
  | k + 1, φ =>
    let ψ := propaga (tamanho φ) φ
    if morta ψ = true then false
    else if passaTrivial ψ = true then true
    else match sonda ψ ψ.flatten with
      | some (.empurra l) => atravessa k (fixa ψ (oposto l))
      | some (.compromete l) => atravessa k (fixa ψ l)
      | none =>
        match ψ.flatten with
        | [] => true
        | l :: _ => atravessa k (fixa ψ l) || atravessa k (fixa ψ (oposto l))

/-- Os dois lados: ter solução é ter solução num dos dois lados do Nome. -/
theorem os_dois_lados (ψ : CNF n) (l : Literal n) : SAT ψ ↔ SAT (fixa ψ l) ∨ SAT (fixa ψ (oposto l)) := by
  obtain ⟨i, p⟩ := l
  show SAT ψ ↔ SAT (restringe ψ i p) ∨ SAT (restringe ψ i (!p))
  rw [a_proposta_nasce_da_escolha_do_nome ψ i]
  constructor
  · rintro ⟨b, hb⟩
    cases b <;> cases p
    · exact Or.inl hb
    · exact Or.inr hb
    · exact Or.inr hb
    · exact Or.inl hb
  · rintro (h | h)
    · exact ⟨p, h⟩
    · exact ⟨!p, h⟩

theorem vivo_sem_letras {ψ : CNF n} (hm : morta ψ = false) (hfl : ψ.flatten = []) : SAT ψ := by
  rcases ψ with _ | ⟨C, rest⟩
  · exact ⟨fun _ => false, fun C hC => by simp at hC⟩
  · rcases C with _ | ⟨a, C'⟩
    · have h0 := morta_falsa hm [] List.mem_cons_self
      simp [vazia] at h0
    · simp at hfl

/-- ★★★ A TRAVESSIA DECIDE TODA FÓRMULA: com combustível maior que o tamanho, a travessia diz `true` exatamente quando há
solução. -/
theorem a_travessia_decide : ∀ (k : ℕ) (φ : CNF n), tamanho φ < k → (atravessa k φ = true ↔ SAT φ)
  | 0, _, hk => absurd hk (Nat.not_lt_zero _)
  | k + 1, φ, hk => by
    have hp := a_propagacao_preserva (tamanho φ) φ
    have hψ := tamanho_propaga_le (tamanho φ) φ
    simp only [atravessa]
    generalize propaga (tamanho φ) φ = ψ at hp hψ ⊢
    split
    · next hm => exact ⟨(fun h => nomatch h), fun hs => absurd (hp.mpr hs) (a_morte_e_o_nao hm)⟩
    · next hm =>
      split
      · next ht => exact ⟨fun _ => hp.mp (o_trivial_diz_sim ht), fun _ => rfl⟩
      · split
        · next l hs =>
          have he := o_zero_empurra_para_o_lado_oposto (sonda_empurra hs)
          obtain ⟨C, hC, hlC⟩ := List.mem_flatten.mp (sonda_empurra_mem hs)
          have hlt := tamanho_restringe_lt ψ l.var (!l.pos) ⟨C, hC, l, hlC, rfl⟩
          rw [a_travessia_decide k (fixa ψ (oposto l)) (by show tamanho (restringe ψ l.var (!l.pos)) < k; omega)]
          exact he.symm.trans hp
        · next l hs =>
          have he := o_lado_que_nao_corta_e_seguro (sonda_compromete hs)
          obtain ⟨C, hC, hlC⟩ := List.mem_flatten.mp (sonda_compromete_mem hs)
          have hlt := tamanho_restringe_lt ψ l.var l.pos ⟨C, hC, l, hlC, rfl⟩
          rw [a_travessia_decide k (fixa ψ l) (by show tamanho (restringe ψ l.var l.pos) < k; omega)]
          exact he.symm.trans hp
        · split
          · next hfl => exact ⟨fun _ => hp.mp (vivo_sem_letras (by simpa using hm) hfl), fun _ => rfl⟩
          · next l ls hfl =>
            have hl : l ∈ ψ.flatten := by rw [hfl]; exact List.mem_cons_self
            obtain ⟨C, hC, hlC⟩ := List.mem_flatten.mp hl
            have hlt1 := tamanho_restringe_lt ψ l.var l.pos ⟨C, hC, l, hlC, rfl⟩
            have hlt2 := tamanho_restringe_lt ψ l.var (!l.pos) ⟨C, hC, l, hlC, rfl⟩
            rw [Bool.or_eq_true,
              a_travessia_decide k (fixa ψ l) (by show tamanho (restringe ψ l.var l.pos) < k; omega),
              a_travessia_decide k (fixa ψ (oposto l)) (by show tamanho (restringe ψ l.var (!l.pos)) < k; omega)]
            exact (os_dois_lados ψ l).symm.trans hp

/-- [DEF] As fixações feitas pela travessia. -/
def custoAtravessa : ℕ → CNF n → ℕ
  | 0, _ => 0
  | k + 1, φ =>
    let ψ := propaga (tamanho φ) φ
    custoPropaga (tamanho φ) φ +
      (if morta ψ = true then 0
       else if passaTrivial ψ = true then 0
       else custoSonda ψ ψ.flatten +
         match sonda ψ ψ.flatten with
         | some (.empurra l) => custoAtravessa k (fixa ψ (oposto l)) + 1
         | some (.compromete l) => custoAtravessa k (fixa ψ l) + 1
         | none =>
           match ψ.flatten with
           | [] => 0
           | l :: _ => custoAtravessa k (fixa ψ l) + custoAtravessa k (fixa ψ (oposto l)) + 2)

theorem cota_aux {c bi b p : ℕ} (h : c + bi ≤ p * bi) (hb : bi ≤ b) (hp : 1 ≤ p) : c + b ≤ p * b := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hb
  have e1 : p * (bi + d) = p * bi + p * d := Nat.mul_add p bi d
  have e2 : d ≤ p * d := Nat.le_mul_of_pos_left d hp
  omega

/-- ★★ O PREÇO DA TRAVESSIA: com B = (T+1)² + 1, a travessia faz no máximo 2^k·B − B fixações, com k o combustível:
exponencial no tamanho. -/
theorem o_preco_da_travessia : ∀ (k : ℕ) (φ : CNF n),
    custoAtravessa k φ + ((tamanho φ + 1) ^ 2 + 1) ≤ 2 ^ k * ((tamanho φ + 1) ^ 2 + 1)
  | 0, φ => by simp [custoAtravessa]
  | k + 1, φ => by
    simp only [custoAtravessa]
    have hP := custoPropaga_le (tamanho φ) φ
    have hψ := tamanho_propaga_le (tamanho φ) φ
    generalize propaga (tamanho φ) φ = ψ at hψ ⊢
    have hS : custoSonda ψ ψ.flatten ≤ tamanho φ * (tamanho φ + 1) :=
      le_trans (custoSonda_le ψ ψ.flatten) (Nat.mul_le_mul (le_trans (letras_le_tamanho ψ) hψ) (by omega))
    have hB : tamanho φ + tamanho φ * (tamanho φ + 1) + 1 = (tamanho φ + 1) ^ 2 := by ring
    have h2 : 2 ^ (k + 1) * ((tamanho φ + 1) ^ 2 + 1) = 2 * (2 ^ k * ((tamanho φ + 1) ^ 2 + 1)) := by ring
    have hpos : (tamanho φ + 1) ^ 2 + 1 ≤ 2 ^ k * ((tamanho φ + 1) ^ 2 + 1) :=
      Nat.le_mul_of_pos_left _ (Nat.two_pow_pos k)
    have hsub : ∀ χ : CNF n, tamanho χ ≤ tamanho φ →
        custoAtravessa k χ + ((tamanho φ + 1) ^ 2 + 1) ≤ 2 ^ k * ((tamanho φ + 1) ^ 2 + 1) := by
      intro χ hχ
      apply cota_aux (o_preco_da_travessia k χ) _ (Nat.two_pow_pos k)
      have := Nat.pow_le_pow_left (Nat.add_le_add_right hχ 1) 2
      omega
    split
    · omega
    · split
      · omega
      · split
        · next l _ =>
          have := hsub (fixa ψ (oposto l)) (le_trans (tamanho_fixa_le ψ _) hψ)
          nlinarith
        · next l _ =>
          have := hsub (fixa ψ l) (le_trans (tamanho_fixa_le ψ _) hψ)
          nlinarith
        · split
          · omega
          · next l _ _ =>
            have h1 := hsub (fixa ψ l) (le_trans (tamanho_fixa_le ψ _) hψ)
            have h3 := hsub (fixa ψ (oposto l)) (le_trans (tamanho_fixa_le ψ _) hψ)
            nlinarith

/-! ## 11. A fronteira nos exemplos (R2) -/

/-- [DEF] Sete das oito cláusulas: falta a que exclui x = (0, 1, 0); essa atribuição é a única solução. -/
def sete : CNF 3 :=
  [[⟨0, true⟩, ⟨1, true⟩, ⟨2, true⟩], [⟨0, true⟩, ⟨1, true⟩, ⟨2, false⟩],
   [⟨0, true⟩, ⟨1, false⟩, ⟨2, false⟩],
   [⟨0, false⟩, ⟨1, true⟩, ⟨2, true⟩], [⟨0, false⟩, ⟨1, true⟩, ⟨2, false⟩],
   [⟨0, false⟩, ⟨1, false⟩, ⟨2, true⟩], [⟨0, false⟩, ⟨1, false⟩, ⟨2, false⟩]]

/-- ★ AS OITO ESTÃO NA FRONTEIRA, E A TRAVESSIA DIZ NÃO. -/
theorem oito_esta_na_fronteira : NaFronteira oito ∧ atravessa (tamanho oito + 1) oito = false := by
  decide

/-- ★ SETE PARAM A INCLINAÇÃO, E A TRAVESSIA DIZ SIM: a inclinação fica indecisa nas sete cláusulas; a travessia ramifica
no primeiro Nome: o lado x₀ = 1 morre, o lado x₀ = 0 vive. -/
theorem sete_atravessa_e_diz_sim :
    NaFronteira sete ∧ aInclinacao sete = .indeciso ∧ atravessa (tamanho sete + 1) sete = true := by
  decide

/-- ★★★ A TRINDADE NA FRONTEIRA (R2):
    (1) a inclinação para só na fronteira, num resto com a mesma resposta;
    (2) na fronteira há cláusula de três literais, e todo lado vivo corta uma delas: um literal cai, os outros esperam;
    (3) a travessia por ramificação decide toda fórmula, ao preço provado de no máximo 2^k·B − B fixações: exponencial. -/
theorem a_trindade_na_fronteira :
    (∀ (k : ℕ) (φ : CNF n), tamanho φ < k → inclina k φ = .indeciso → ∃ ψ : CNF n, (SAT ψ ↔ SAT φ) ∧ NaFronteira ψ)
    ∧ (∀ ψ : CNF n, NaFronteira ψ → ∃ D ∈ ψ, 3 ≤ D.length)
    ∧ (∀ ψ : CNF n, NaFronteira ψ → ∀ l ∈ ψ.flatten, morta (lado ψ l) = false ∧
        ∃ D ∈ ψ, 3 ≤ D.length ∧ ∃ C ∈ lado ψ l, C.Sublist D ∧ C ≠ D ∧ 2 ≤ C.length)
    ∧ (∀ (k : ℕ) (φ : CNF n), tamanho φ < k → (atravessa k φ = true ↔ SAT φ))
    ∧ (∀ (k : ℕ) (φ : CNF n),
        custoAtravessa k φ + ((tamanho φ + 1) ^ 2 + 1) ≤ 2 ^ k * ((tamanho φ + 1) ^ 2 + 1)) :=
  ⟨a_inclinacao_para_so_na_fronteira, fun _ h => a_fronteira_tem_tres_literais h,
   fun _ h => na_fronteira_todo_lado_corta_uma_de_tres h, a_travessia_decide, o_preco_da_travessia⟩

end TGLExt.Trinity

#print axioms TGLExt.Trinity.a_morte_e_o_nao
#print axioms TGLExt.Trinity.a_unidade_forca_o_lado
#print axioms TGLExt.Trinity.a_propagacao_preserva
#print axioms TGLExt.Trinity.a_propagacao_para
#print axioms TGLExt.Trinity.o_zero_empurra_para_o_lado_oposto
#print axioms TGLExt.Trinity.o_lado_que_nao_corta_e_seguro
#print axioms TGLExt.Trinity.a_inclinacao_nao_erra
#print axioms TGLExt.Trinity.em_horn_o_sistema_sempre_inclina
#print axioms TGLExt.Trinity.em_horn_a_inclinacao_decide
#print axioms TGLExt.Trinity.o_custo_da_inclinacao
#print axioms TGLExt.Trinity.oito_sem_solucao
#print axioms TGLExt.Trinity.oito_fica_na_fronteira
#print axioms TGLExt.Trinity.quatro_o_empurrao_diz_nao
#print axioms TGLExt.Trinity.o_empurrao_diz_sim
#print axioms TGLExt.Trinity.dois_o_compromisso_diz_sim
#print axioms TGLExt.Trinity.a_trindade
#print axioms TGLExt.Trinity.todo_lado_morre_ou_nao_corta
#print axioms TGLExt.Trinity.em_dois_literais_o_sistema_sempre_inclina
#print axioms TGLExt.Trinity.a_inclinacao_que_nao_para_decide
#print axioms TGLExt.Trinity.em_dois_literais_a_inclinacao_decide
#print axioms TGLExt.Trinity.a_cadeia_inclina_e_diz_sim
#print axioms TGLExt.Trinity.na_fronteira_todo_lado_corta_uma_de_tres
#print axioms TGLExt.Trinity.a_fronteira_tem_tres_literais
#print axioms TGLExt.Trinity.a_inclinacao_para_so_na_fronteira
#print axioms TGLExt.Trinity.os_dois_lados
#print axioms TGLExt.Trinity.a_travessia_decide
#print axioms TGLExt.Trinity.o_preco_da_travessia
#print axioms TGLExt.Trinity.oito_esta_na_fronteira
#print axioms TGLExt.Trinity.sete_atravessa_e_diz_sim
#print axioms TGLExt.Trinity.a_trindade_na_fronteira

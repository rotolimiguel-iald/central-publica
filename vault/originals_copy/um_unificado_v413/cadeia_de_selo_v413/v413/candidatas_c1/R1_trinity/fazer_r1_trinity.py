# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R1 da Trinity (pedida pelo operador, fala por bytes). Gera R1_trinity\\Trinity.lean a partir
da R0 por trocas EXATAS (cada trecho antigo deve aparecer uma vez): o cabecalho (R1 e a fala), a lista do que se prova, o
item dos dois literais em 'o que nao prova', a secao 5b nova (dois literais) antes da secao 6, a sintese com o item novo e
os #print axioms novos. Nenhum enunciado da R0 muda. Escrita por temporario e conferencia."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R0 = AQUI.parent / "R0_trinity" / "Trinity.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_excelente_prossigamos_escreva_a_r1_verbatim.txt")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert FALA.read_text(encoding="utf-8").strip() == "excelente, prossigamos escreva a r1"
src = R0.read_bytes().decode("utf-8")

CAB_ANT = """  [Pedra candidata para a v413, R0, 20/11/2026; não instalada. Nome do operador: «trindade», Trinity (fala por bytes em
  `work\\cunhagens_13out\\OPERADOR_20nov_excelente_vamos_prosseguir_escreva_a_pedra_que_se_chamara_trindade_Trinity_verbatim.txt`,
  sha16 `f19c729a40fc8e84`).]
"""
CAB_NOV = """  [Pedra candidata para a v413, R1, 20/11/2026; não instalada. Nome do operador: «trindade», Trinity (fala por bytes em
  `work\\cunhagens_13out\\OPERADOR_20nov_excelente_vamos_prosseguir_escreva_a_pedra_que_se_chamara_trindade_Trinity_verbatim.txt`,
  sha16 `f19c729a40fc8e84`). A R1, pedida pelo operador (fala por bytes em
  `work\\cunhagens_13out\\OPERADOR_20nov_excelente_prossigamos_escreva_a_r1_verbatim.txt`, sha16 `%s`), acrescenta a §5b (dois
  literais), um exemplo e um item à síntese; nenhum enunciado da R0 (sha16 `%s`) mudou.]
""" % (sha(FALA)[:16], sha(R0)[:16])

LISTA_ANT = """1. `a_inclinacao_nao_erra`: quando a inclinação diz sim, há solução; quando diz não, não há.
2. `em_horn_o_sistema_sempre_inclina`, `em_horn_a_inclinacao_decide`: em toda fórmula de Horn (a classe `IsHorn` da casa)
   a inclinação diz sim ou morre na primeira volta; nunca fica na fronteira.
3. `o_custo_da_inclinacao`: no máximo (T+1)³ fixações, com T o tamanho da fórmula (letras mais terminadores).
4. `oito_sem_solucao`, `oito_fica_na_fronteira`: a fórmula das oito cláusulas de três literais sobre três Nomes não tem
   solução, e a inclinação fica indecisa: nenhum lado morre logo e todo lado corta cláusulas ao meio. A morte está longe.
5. `quatro_o_empurrao_diz_nao`, `o_empurrao_diz_sim`, `dois_o_compromisso_diz_sim`: fórmulas sem cláusula unitária, em que
   a propagação sozinha não começa, decididas pelo empurrão ou pelo compromisso.
6. `a_trindade`: a síntese.
"""
LISTA_NOV = """1. `a_inclinacao_nao_erra`: quando a inclinação diz sim, há solução; quando diz não, não há.
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
7. `a_trindade`: a síntese.
"""

NAO_ANT = """* Que a inclinação decida toda fórmula de dois literais: com o compromisso, decide [KNOWN: Even–Itai–Shamir 1976]; a prova
  no kernel é o passo seguinte.
"""
NAO_NOV = """* Que a inclinação decida as fórmulas de três literais: lá um lado pode cortar cláusulas ao meio sem morrer, e a inclinação
  para (`oito_fica_na_fronteira`). É a fronteira de três literais medida em 18/11.
"""

SECAO_5B = r'''/-! ## 5b. Em dois literais, todo lado morre logo ou não corta nada (R1) -/

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

'''

EXEMPLO_ANCORA = "/-! ## 8. A síntese -/\n"
EXEMPLO = r'''/-- [DEF] Uma cadeia de dois literais sobre quatro Nomes, com solução. -/
def cadeia : CNF 4 :=
  [[⟨0, false⟩, ⟨1, true⟩], [⟨1, false⟩, ⟨2, true⟩], [⟨2, false⟩, ⟨3, true⟩], [⟨0, true⟩, ⟨3, true⟩],
   [⟨3, false⟩, ⟨0, false⟩]]

/-- ★ A CADEIA INCLINA E DIZ SIM: nem tudo falso nem tudo verdadeiro serve e não há cláusula unitária; o primeiro lado
(x₀ = 0), propagado, não corta nenhuma cláusula ao meio; o compromisso com ele leva à solução na segunda volta. -/
theorem a_cadeia_inclina_e_diz_sim :
    DoisLiterais cadeia ∧ passaTrivial cadeia = false ∧ ehCompromisso (sonda cadeia cadeia.flatten) = true ∧
      aInclinacao cadeia = .sim :=
  ⟨by show ∀ C ∈ cadeia, C.length ≤ 2; decide, by decide⟩

'''

SINT_ANT = """/-- ★★★ A TRINDADE:
    (1) O PAR: a fórmula tem solução se, e só se, um dos dois lados do Nome tem (a tensão do Kimi); e o lado que morre
        logo empurra para o oposto.
    (2) O EMPURRÃO: a inclinação nunca erra, decide toda fórmula de Horn e custa no máximo (T+1)³ fixações.
    (3) A FRONTEIRA: há fórmula sem solução em que a inclinação fica indecisa: a morte está longe. -/
theorem a_trindade :
    (∀ (φ : CNF n) (i : Fin n), SAT φ ↔ ∃ b : Bool, SAT (restringe φ i b))
    ∧ (∀ (ψ : CNF n) (l : Literal n), morreLogo ψ l = true → (SAT ψ ↔ SAT (fixa ψ (oposto l))))
    ∧ (∀ (k : ℕ) (φ : CNF n), (inclina k φ = .sim → SAT φ) ∧ (inclina k φ = .nao → ¬ SAT φ))
    ∧ (∀ φ : CNF n, IALD.CompilaHornNaFita.IsHorn φ → aInclinacao φ ≠ .indeciso)
    ∧ (∀ φ : CNF n, custoInclina (tamanho φ + 1) φ ≤ (tamanho φ + 1) ^ 3)
    ∧ (¬ SAT oito ∧ aInclinacao oito = .indeciso) :=
  ⟨a_proposta_nasce_da_escolha_do_nome, fun _ _ h => o_zero_empurra_para_o_lado_oposto h,
   a_inclinacao_nao_erra, fun φ h => em_horn_o_sistema_sempre_inclina h (tamanho φ),
   o_custo_da_inclinacao, oito_sem_solucao, oito_fica_na_fronteira⟩
"""
SINT_NOV = """/-- ★★★ A TRINDADE:
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
"""

AX_ANCORA = "#print axioms TGLExt.Trinity.a_trindade\n"
AX_NOVOS = """#print axioms TGLExt.Trinity.todo_lado_morre_ou_nao_corta
#print axioms TGLExt.Trinity.em_dois_literais_o_sistema_sempre_inclina
#print axioms TGLExt.Trinity.a_inclinacao_que_nao_para_decide
#print axioms TGLExt.Trinity.em_dois_literais_a_inclinacao_decide
#print axioms TGLExt.Trinity.a_cadeia_inclina_e_diz_sim
"""

novo = src
for antes, depois in [(CAB_ANT, CAB_NOV), (LISTA_ANT, LISTA_NOV), (NAO_ANT, NAO_NOV), (SINT_ANT, SINT_NOV),
                      ("/-! ## 6. O custo -/\n", SECAO_5B + "/-! ## 6. O custo -/\n"),
                      (EXEMPLO_ANCORA, EXEMPLO + EXEMPLO_ANCORA), (AX_ANCORA, AX_ANCORA + AX_NOVOS)]:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:70]
    novo = novo.replace(antes, depois)
dest = AQUI / "Trinity.lean"
dados = novo.encode("utf-8")
tmp = AQUI / "Trinity.lean.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("R0 sha16 %s -> R1 sha16 %s | %d -> %d B | fala sha16 %s" % (sha(R0)[:16], sha(dest)[:16], len(src.encode("utf-8")),
                                                                   len(dados), sha(FALA)[:16]))

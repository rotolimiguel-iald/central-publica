# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R3 da Trinity (o operador: «excelente, prossigamos», fala por bytes, depois da R2). Gera
R3_trinity\\Trinity.lean a partir da R2 por trocas EXATAS: o cabecalho, a lista do que se prova, um item em 'o que nao
prova', a secao 12 (os Nomes da fronteira) antes do fim do namespace, e os #print axioms novos. Nenhum enunciado da R2
muda."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R2 = AQUI.parent / "R2_trinity" / "Trinity.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_excelente_prossigamos_apos_a_R2_da_trinity_verbatim.txt")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


assert FALA.read_text(encoding="utf-8").strip() == "excelente, prossigamos"
src = R2.read_bytes().decode("utf-8")

CAB_ANT = "  ramificação); nenhum enunciado da R1 (sha16 `97fd14f931128cf3`) mudou.]\n"
CAB_NOV = ("  ramificação); nenhum enunciado da R1 (sha16 `97fd14f931128cf3`) mudou. A R3 (fala por bytes em\n"
           "  `work\\cunhagens_13out\\%s`, sha16 `%s`) acrescenta a §12 (os Nomes da\n"
           "  fronteira); nenhum enunciado da R2 (sha16 `%s`) mudou.]\n") % (FALA.name, sha(FALA)[:16], sha(R2)[:16])

LISTA_ANT = "11. `a_trindade`, `a_trindade_na_fronteira`: as sínteses.\n"
LISTA_NOV = """11. `a_travessia_pelos_nomes_decide`, `o_preco_dos_nomes`, `o_preco_da_fronteira_esta_nos_nomes` (R3): numa fórmula de até
    três literais, se os Nomes de uma lista `S` tocam toda cláusula de três literais, ramificar só nesses Nomes e deixar o
    resto à inclinação decide a fórmula, ao preço de no máximo 2^|S|·((T+1)³ + 2) fixações: exponencial só no número de
    Nomes da fronteira, polinomial no resto. `os_nomes_da_fronteira_tocam`: a lista dos primeiros Nomes das cláusulas de
    três literais sempre serve. `um_nome_atravessa_as_oito_e_as_sete`: nas oito e nas sete cláusulas, um só Nome toca todas.
12. `a_trindade`, `a_trindade_na_fronteira`, `a_trindade_dos_nomes`: as sínteses.
"""

NAO_ANT = """* Que a fronteira dos três literais se atravesse em preço polinomial. A pedra atravessa ramificando, ao preço provado
  exponencial; uma travessia de preço polinomial para toda fórmula de três literais é a pergunta do Instituto [OPEN].
"""
NAO_NOV = """* Que a fronteira dos três literais se atravesse em preço polinomial. A pedra atravessa ramificando, ao preço provado
  exponencial; uma travessia de preço polinomial para toda fórmula de três literais é a pergunta do Instituto [OPEN].
* Que os Nomes da fronteira sejam poucos em geral. O preço da §12 é exponencial no número de Nomes que tocam as cláusulas de
  três literais; atravessar um corte de n Nomes partilhados pede 2ⁿ retângulos (`Codex.PairCut.exact_cover_iff`, no kernel),
  e um gesto que atravesse sem pagar por Nome da fronteira é a mesma pergunta do Instituto [OPEN].
"""

SECAO = r'''/-! ## 12. Os Nomes da fronteira (R3) -/

/-- [DEF] As fórmulas de até três literais. -/
def TresLiterais (φ : CNF n) : Prop := ∀ C ∈ φ, C.length ≤ 3

/-- [DEF] OS NOMES QUE TOCAM A FRONTEIRA: toda cláusula de três literais tem um literal cujo Nome está em `S`. -/
abbrev Toca (S : List (Fin n)) (φ : CNF n) : Prop := ∀ C ∈ φ, C.length = 3 → ∃ l ∈ C, l.var ∈ S

theorem tres_restringe {φ : CNF n} (h : TresLiterais φ) (i : Fin n) (b : Bool) : TresLiterais (restringe φ i b) := by
  intro C hC
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  exact le_trans (List.length_filter_le _ D) (h D (List.mem_filter.mp hD).1)

/-- Fixar um Nome de `S` deixa o resto de `S` tocando a fronteira que sobra. -/
theorem toca_restringe {i : Fin n} {S : List (Fin n)} {φ : CNF n} (h3 : TresLiterais φ) (ht : Toca (i :: S) φ)
    (b : Bool) :
    Toca S (restringe φ i b) := by
  intro C hC hC3
  unfold restringe at hC
  obtain ⟨D, hD, rfl⟩ := List.mem_map.mp hC
  have hDφ := (List.mem_filter.mp hD).1
  have hsub : (D.filter fun l => l.var ≠ i).Sublist D := List.filter_sublist
  have hD3 : D.length = 3 := by
    have := hsub.length_le
    have := h3 D hDφ
    omega
  have heq : (D.filter fun l => l.var ≠ i) = D := hsub.eq_of_length (by rw [hC3, hD3])
  obtain ⟨l, hl, hlS⟩ := ht D hDφ hD3
  have hli : l.var ≠ i := by
    have hmem : l ∈ D.filter (fun l => l.var ≠ i) := by rw [heq]; exact hl
    simpa using (List.mem_filter.mp hmem).2
  refine ⟨l, by rw [heq]; exact hl, ?_⟩
  rcases List.mem_cons.mp hlS with h | h
  · exact absurd h hli
  · exact h

/-- [DEF] A TRAVESSIA PELOS NOMES: ramifica nos Nomes de `S`, um a um; o resto, a inclinação decide. -/
def atravessaPelos : List (Fin n) → CNF n → Bool
  | [], φ => decide (aInclinacao φ = .sim)
  | i :: S, φ => atravessaPelos S (restringe φ i true) || atravessaPelos S (restringe φ i false)

/-- ★★★ A TRAVESSIA PELOS NOMES DECIDE: numa fórmula de até três literais, se `S` toca toda cláusula de três literais,
a travessia pelos Nomes de `S` diz `true` exatamente quando há solução. -/
theorem a_travessia_pelos_nomes_decide : ∀ (S : List (Fin n)) (φ : CNF n), TresLiterais φ → Toca S φ →
    (atravessaPelos S φ = true ↔ SAT φ)
  | [], φ, h3, ht => by
    have h2 : DoisLiterais φ := by
      intro C hC
      have hle := h3 C hC
      by_contra hlt
      obtain ⟨l, _, hl⟩ := ht C hC (by omega)
      simp at hl
    simp only [atravessaPelos, decide_eq_true_eq]
    exact (em_dois_literais_a_inclinacao_decide h2).1
  | i :: S, φ, h3, ht => by
    simp only [atravessaPelos, Bool.or_eq_true]
    rw [a_travessia_pelos_nomes_decide S _ (tres_restringe h3 i true) (toca_restringe h3 ht true),
      a_travessia_pelos_nomes_decide S _ (tres_restringe h3 i false) (toca_restringe h3 ht false)]
    exact (os_dois_lados φ ⟨i, true⟩).symm

/-- [DEF] As fixações feitas pela travessia pelos Nomes. -/
def custoPelos : List (Fin n) → CNF n → ℕ
  | [], φ => custoInclina (tamanho φ + 1) φ
  | i :: S, φ => custoPelos S (restringe φ i true) + custoPelos S (restringe φ i false) + 2

/-- ★★ O PREÇO DOS NOMES: no máximo 2^|S|·((T+1)³ + 2) fixações. -/
theorem o_preco_dos_nomes : ∀ (S : List (Fin n)) (φ : CNF n),
    custoPelos S φ + 2 ≤ 2 ^ S.length * ((tamanho φ + 1) ^ 3 + 2)
  | [], φ => by
    simp only [custoPelos, List.length_nil, pow_zero, one_mul]
    have := o_custo_da_inclinacao φ
    omega
  | i :: S, φ => by
    simp only [custoPelos, List.length_cons]
    have hb : ∀ b, custoPelos S (restringe φ i b) + 2 ≤ 2 ^ S.length * ((tamanho φ + 1) ^ 3 + 2) := by
      intro b
      have ih := o_preco_dos_nomes S (restringe φ i b)
      have ht := tamanho_restringe_le φ i b
      have h3 : (tamanho (restringe φ i b) + 1) ^ 3 ≤ (tamanho φ + 1) ^ 3 := Nat.pow_le_pow_left (by omega) 3
      have hm : 2 ^ S.length * ((tamanho (restringe φ i b) + 1) ^ 3 + 2) ≤ 2 ^ S.length * ((tamanho φ + 1) ^ 3 + 2) :=
        Nat.mul_le_mul_left _ (by omega)
      omega
    have h1 := hb true
    have h2 := hb false
    have hp : 2 ^ (S.length + 1) * ((tamanho φ + 1) ^ 3 + 2) = 2 * (2 ^ S.length * ((tamanho φ + 1) ^ 3 + 2)) := by
      ring
    omega

/-- [DEF] Os Nomes da fronteira: o Nome do primeiro literal de cada cláusula de três literais. -/
def nomesDaFronteira (φ : CNF n) : List (Fin n) :=
  (φ.filter fun C => C.length == 3).filterMap fun C => C.head?.map Literal.var

/-- ★ OS NOMES DA FRONTEIRA TOCAM: a lista dos primeiros Nomes das cláusulas de três literais toca toda cláusula de três
literais; ela tem no máximo tantos Nomes quantas são essas cláusulas. -/
theorem os_nomes_da_fronteira_tocam (φ : CNF n) :
    Toca (nomesDaFronteira φ) φ ∧ (nomesDaFronteira φ).length ≤ (φ.filter fun C => C.length == 3).length := by
  refine ⟨?_, List.length_filterMap_le _ _⟩
  intro C hC hC3
  match C, hC, hC3 with
  | a :: C', hC, hC3 =>
    refine ⟨a, List.mem_cons_self, ?_⟩
    unfold nomesDaFronteira
    rw [List.mem_filterMap]
    exact ⟨a :: C', List.mem_filter.mpr ⟨hC, by simp [hC3]⟩, rfl⟩

/-- ★★★ O PREÇO DA FRONTEIRA ESTÁ NOS NOMES DA FRONTEIRA: numa fórmula de até três literais, a travessia pelos Nomes da
fronteira decide a fórmula, ao preço de no máximo 2^(Nomes da fronteira)·((T+1)³ + 2) fixações. -/
theorem o_preco_da_fronteira_esta_nos_nomes {φ : CNF n} (h3 : TresLiterais φ) :
    (atravessaPelos (nomesDaFronteira φ) φ = true ↔ SAT φ)
    ∧ custoPelos (nomesDaFronteira φ) φ + 2 ≤ 2 ^ (nomesDaFronteira φ).length * ((tamanho φ + 1) ^ 3 + 2) :=
  ⟨a_travessia_pelos_nomes_decide _ φ h3 (os_nomes_da_fronteira_tocam φ).1, o_preco_dos_nomes _ φ⟩

/-- ★ UM SÓ NOME ATRAVESSA AS OITO E AS SETE: o Nome x₀ toca todas as cláusulas; a travessia por ele diz não nas oito e
sim nas sete. -/
theorem um_nome_atravessa_as_oito_e_as_sete :
    Toca [0] oito ∧ atravessaPelos [0] oito = false ∧ Toca [0] sete ∧ atravessaPelos [0] sete = true := by
  refine ⟨?_, by decide, ?_, by decide⟩
  · intro C hC _
    simp only [oito, List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> exact ⟨_, List.mem_cons_self, by simp⟩
  · intro C hC _
    simp only [sete, List.mem_cons, List.not_mem_nil, or_false] at hC
    rcases hC with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> exact ⟨_, List.mem_cons_self, by simp⟩

/-- ★★★ A TRINDADE DOS NOMES (R3): numa fórmula de até três literais, o preço da travessia mora nos Nomes que tocam as
cláusulas de três literais: com `S` tocando a fronteira, a travessia por `S` decide, ao preço exponencial só em |S|. -/
theorem a_trindade_dos_nomes :
    (∀ (S : List (Fin n)) (φ : CNF n), TresLiterais φ → Toca S φ → (atravessaPelos S φ = true ↔ SAT φ))
    ∧ (∀ (S : List (Fin n)) (φ : CNF n), custoPelos S φ + 2 ≤ 2 ^ S.length * ((tamanho φ + 1) ^ 3 + 2))
    ∧ (∀ φ : CNF n, Toca (nomesDaFronteira φ) φ) :=
  ⟨a_travessia_pelos_nomes_decide, o_preco_dos_nomes, fun φ => (os_nomes_da_fronteira_tocam φ).1⟩

'''

FIM = "end TGLExt.Trinity\n"
AX_ANCORA = "#print axioms TGLExt.Trinity.a_trindade_na_fronteira\n"
AX_NOVOS = """#print axioms TGLExt.Trinity.toca_restringe
#print axioms TGLExt.Trinity.a_travessia_pelos_nomes_decide
#print axioms TGLExt.Trinity.o_preco_dos_nomes
#print axioms TGLExt.Trinity.os_nomes_da_fronteira_tocam
#print axioms TGLExt.Trinity.o_preco_da_fronteira_esta_nos_nomes
#print axioms TGLExt.Trinity.um_nome_atravessa_as_oito_e_as_sete
#print axioms TGLExt.Trinity.a_trindade_dos_nomes
"""

novo = src
for antes, depois in [(CAB_ANT, CAB_NOV), (LISTA_ANT, LISTA_NOV), (NAO_ANT, NAO_NOV), (FIM, SECAO + FIM),
                      (AX_ANCORA, AX_ANCORA + AX_NOVOS)]:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:70]
    novo = novo.replace(antes, depois)
dest = AQUI / "Trinity.lean"
dados = novo.encode("utf-8")
tmp = AQUI / "Trinity.lean.tmp"
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("R2 sha16 %s -> R3 sha16 %s | %d -> %d B | fala sha16 %s" % (sha(R2)[:16], sha(dest)[:16], len(src.encode("utf-8")),
                                                                   len(dados), sha(FALA)[:16]))

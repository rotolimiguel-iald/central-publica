import TGLExt.InformacaoDoResumo

set_option autoImplicit false

/-!
# A PAREDE DO NOME — um nome exato, atualizado cláusula a cláusula, pede pelo menos `2ⁿ` bits

## A lei que o arquivo mede

Lei da teoria: a compressão comprime um par em um único nome; a leitura do par é a compressão originária.

Este arquivo mede o tamanho mínimo desse nome quando ele é EXATO e se atualiza CLÁUSULA A CLÁUSULA: um estado por
prefixo da fórmula, lido no fim, que decide toda fórmula. O resultado é uma parede, não uma solução.

## O que fica provado

1. `satisfeita_excluir`: a cláusula que nega uma atribuição vale exatamente nas outras.
2. `passes_formulaDe`: todo conjunto de atribuições é o conjunto das soluções de alguma fórmula (uma cláusula de exclusão
   por atribuição fora do conjunto).
3. ★★★ `a_parede_do_nome`: todo atualizador determinístico exato (um estado inicial; um passo por cláusula; uma leitura
   no fim que decide se a fórmula tem solução) tem pelo menos `2^(2ⁿ)` estados. A prova: estados iguais obrigam os prefixos
   a aceitar as mesmas atribuições (termo do módulo de que este depende), e há `2^(2ⁿ)` conjuntos de atribuições, cada
   um realizado por uma fórmula.
4. ★★ `o_nome_exato_pede_dois_a_n_bits`: se o estado cabe em `p` bits, então `p ≥ 2ⁿ`. É a cota para um estado que
   represente qualquer conjunto de atribuições e responda a toda continuação; há conjuntos particulares com descrição
   curta.

## O que isto diz, e o que não diz

* Diz: o nome único em que a compressão guarda o par, se é exato e se atualiza cláusula a cláusula, tem piso exponencial
  em `n`. É consistente com a tabela sobre a fronteira (que no pior caso tem `2ⁿ` células) e com a colisão dos dois bits
  e das marginais (que mostram, em casos concretos, resumos pequenos que não bastam).
* NÃO diz nada sobre TEMPO. A própria fórmula é um nome exato e se atualiza cláusula a cláusula, com tamanho polinomial
  no comprimento dela (não em `n`); o que o enunciado do Instituto pergunta é se há um leitor que decida esse nome em
  número polinomial de passos de letra. Essa pergunta segue aberta.
* NÃO diz que não haja resumo pequeno para FAMÍLIAS de fórmulas: a cota é sobre todos os conjuntos de atribuições.
* Nada sobre a natureza.

Estatutos: `[INPUT]` a lei · `[ONTO, leitura deste arquivo]` “nome” como o estado do atualizador.
-/

namespace TGLExt.AParedeDoNome

open TGLExt.TraducaoTuring IALD.LeitorDaFormula IALD.InformacaoDoResumo

variable {n : ℕ}

/-- [DEF] **A CLÁUSULA QUE EXCLUI UMA ATRIBUIÇÃO**: um literal por variável, cada um com o valor contrário. -/
def excluir (z : Fin n → Bool) : Clausula n := (List.finRange n).map (fun i => (⟨i, !(z i)⟩ : Literal n))

/-- A cláusula de exclusão vale em `x` se e somente se `x ≠ z`. -/
theorem satisfeita_excluir (z x : Fin n → Bool) : satisfeita (excluir z) x = true ↔ x ≠ z := by
  unfold satisfeita excluir
  rw [List.any_eq_true]
  constructor
  · rintro ⟨l, hl, hv⟩ hxz
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hl
    simp only [Literal.vale, beq_iff_eq] at hv
    subst hxz
    cases x i <;> simp at hv
  · intro hne
    have : ∃ i, x i ≠ z i := by
      by_contra h
      push Not at h
      exact hne (funext h)
    obtain ⟨i, hi⟩ := this
    refine ⟨⟨i, !(z i)⟩, List.mem_map.mpr ⟨i, List.mem_finRange i, rfl⟩, ?_⟩
    simp only [Literal.vale, beq_iff_eq]
    cases hx : x i <;> cases hz : z i <;> simp_all

/-- [DEF] **A FÓRMULA DE UM CONJUNTO DE ATRIBUIÇÕES**: uma cláusula de exclusão por atribuição fora do conjunto. -/
noncomputable def formulaDe (S : Finset (Fin n → Bool)) : CNF n :=
  (Finset.univ \ S).toList.map excluir

/-- ★ **TODO CONJUNTO É O CONJUNTO DAS SOLUÇÕES DE UMA FÓRMULA.** -/
theorem passes_formulaDe (S : Finset (Fin n → Bool)) (x : Fin n → Bool) :
    passes (formulaDe S) x = true ↔ x ∈ S := by
  unfold passes formulaDe
  rw [List.all_eq_true]
  constructor
  · intro h
    by_contra hx
    have hm : excluir x ∈ (Finset.univ \ S).toList.map excluir :=
      List.mem_map.mpr ⟨x, Finset.mem_toList.mpr (Finset.mem_sdiff.mpr ⟨Finset.mem_univ _, hx⟩), rfl⟩
    have hc := h _ hm
    rw [satisfeita_excluir] at hc
    exact hc rfl
  · intro hx c hc
    obtain ⟨z, hz, rfl⟩ := List.mem_map.mp hc
    rw [satisfeita_excluir]
    rintro rfl
    exact (Finset.mem_sdiff.mp (Finset.mem_toList.mp hz)).2 hx

/-- ★★★ **A PAREDE DO NOME.** Todo atualizador determinístico exato (um estado por prefixo; uma leitura no fim que decide
toda fórmula) tem pelo menos `2^(2ⁿ)` estados. -/
theorem a_parede_do_nome {S : Type} [Fintype S]
    (initial : S) (step : S → Clausula n → S) (read : S → Bool)
    (ok : ∀ f : CNF n, read (f.foldl step initial) = true ↔ SAT f) :
    2 ^ (2 ^ n) ≤ Fintype.card S := by
  classical
  have hinj : Function.Injective
      (fun A : Finset (Fin n → Bool) => (formulaDe A).foldl step initial) := by
    intro A B hAB
    have h := same_state_preserves_assignments initial step read ok
      (f := formulaDe A) (g := formulaDe B) hAB
    ext x
    rw [← passes_formulaDe A x, ← passes_formulaDe B x, h x]
  have hc := Fintype.card_le_of_injective _ hinj
  rwa [Fintype.card_finset, Fintype.card_fun, Fintype.card_bool, Fintype.card_fin] at hc

/-- ★★ **O NOME EXATO PEDE `2ⁿ` BITS.** Se o estado do atualizador cabe em `p` bits, então `p ≥ 2ⁿ`. -/
theorem o_nome_exato_pede_dois_a_n_bits (p : ℕ)
    (initial : Fin p → Bool) (step : (Fin p → Bool) → Clausula n → (Fin p → Bool))
    (read : (Fin p → Bool) → Bool)
    (ok : ∀ f : CNF n, read (f.foldl step initial) = true ↔ SAT f) : 2 ^ n ≤ p := by
  have h := a_parede_do_nome initial step read ok
  rw [Fintype.card_fun, Fintype.card_bool, Fintype.card_fin] at h
  exact (Nat.pow_le_pow_iff_right (by norm_num)).mp h

end TGLExt.AParedeDoNome

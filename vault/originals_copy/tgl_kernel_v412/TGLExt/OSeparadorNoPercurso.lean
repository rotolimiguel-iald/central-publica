import TGLExt.AFronteiraEOUnicoPortao

set_option autoImplicit false

/-!
# O separador no percurso: todo percurso do lido ao por ler tem um vértice na fronteira

## O que este arquivo acrescenta

`AFronteiraEOUnicoPortao.a_fronteira_e_o_unico_portao` conclui que, havendo cadeia de uma variável só lida a uma só
por ler, a fronteira não é vazia. O enunciado dele não registra que o vértice exibido pertence à cadeia, porque a
cadeia é uma proposição de alcançabilidade. Aqui o percurso é uma lista explícita de variáveis, cada uma ligada à
seguinte, e o enunciado devolve a pertinência.

## O que fica provado

1. `Percurso`: a lista de variáveis em que cada uma está ligada à seguinte (mencionadas juntas por uma cláusula).
2. ★★ `o_percurso_atravessa_a_fronteira`: todo percurso que começa numa variável só lida e termina numa só por ler
   tem um vértice na fronteira. É a propriedade de separador: tirada a fronteira, nenhum percurso liga o só lido ao
   só por ler.
3. `toda_cadeia_tem_percurso`: toda cadeia de `i` a `k` é realizada por um percurso que começa em `i` e termina em
   `k`; com o item 2, toda cadeia do só lido ao só por ler tem um percurso com vértice na fronteira
   (`a_cadeia_atravessa_a_fronteira`).

## O que NÃO se afirma

* Que a fronteira seja o menor separador, ou o único: prova-se que ela separa, não que seja mínima.
* Nada sobre custo de leitura, sobre máquina de fita ou sobre o tamanho da fronteira.
* Que a fronteira seja o piso da leitura: é definição da teoria [INPUT/ONTO]; o termo é a separação.
-/

namespace TGLExt.OSeparadorNoPercurso

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit TGLExt.AFronteiraEOUnicoPortao

variable {n : ℕ}

/-- [DEF] O PERCURSO: a lista de variáveis em que cada uma está ligada à seguinte. -/
inductive Percurso (φ : CNF n) : List (Fin n) → Prop
  | um (i : Fin n) : Percurso φ [i]
  | passo {i k : Fin n} {r : List (Fin n)} : ligadas φ i k → Percurso φ (k :: r) → Percurso φ (i :: k :: r)

/-- ★★ **O PERCURSO ATRAVESSA A FRONTEIRA**: todo percurso que começa numa variável só lida e termina numa só por
ler tem um vértice na fronteira. -/
theorem o_percurso_atravessa_a_fronteira (φ : CNF n) (j : ℕ) (p : List (Fin n)) :
    ∀ i : Fin n, Percurso φ (i :: p) → soLeida φ j i →
      soPorLer φ j ((i :: p).getLast (List.cons_ne_nil i p)) →
      ∃ v, v ∈ i :: p ∧ v ∈ fronteira φ j := by
  induction p with
  | nil =>
      intro i _ hi hk
      have hk' : soPorLer φ j i := hk
      exact absurd hk'.2 hi.2
  | cons b r ih =>
      intro i hp hi hk
      have hk' : soPorLer φ j ((b :: r).getLast (List.cons_ne_nil b r)) := hk
      cases hp with
      | passo hlink hrest =>
          obtain ⟨C, hCφ, haC, hbC⟩ := hlink
          rcases mem_take_or_drop (j := j) hCφ with hC | hC
          · have hbL : b ∈ varsDas (φ.take j) := mem_varsDas_take hC hbC
            by_cases hbN : b ∈ varsDas (φ.drop j)
            · exact ⟨b, by simp, Finset.mem_inter.mpr ⟨hbL, hbN⟩⟩
            · obtain ⟨v, hv, hvF⟩ := ih b hrest ⟨hbL, hbN⟩ hk'
              exact ⟨v, List.mem_cons_of_mem _ hv, hvF⟩
          · exact absurd (mem_varsDas_drop hC haC) hi.2

/-- Toda cadeia de `i` a `k` é realizada por um percurso que começa em `i` e termina em `k`. -/
theorem toda_cadeia_tem_percurso (φ : CNF n) {i k : Fin n} (c : Cadeia φ i k) :
    ∃ r : List (Fin n), Percurso φ (i :: r) ∧ (i :: r).getLast (List.cons_ne_nil i r) = k := by
  induction c with
  | single i => exact ⟨[], Percurso.um i, rfl⟩
  | cons hlink _ ih =>
      obtain ⟨r, hp, hl⟩ := ih
      exact ⟨_ :: r, Percurso.passo hlink hp, hl⟩

/-- **A CADEIA ATRAVESSA A FRONTEIRA**: toda cadeia de uma variável só lida a uma só por ler é realizada por um
percurso que tem um vértice na fronteira. -/
theorem a_cadeia_atravessa_a_fronteira (φ : CNF n) (j : ℕ) {i k : Fin n} (c : Cadeia φ i k)
    (hi : soLeida φ j i) (hk : soPorLer φ j k) :
    ∃ r : List (Fin n), Percurso φ (i :: r) ∧ (i :: r).getLast (List.cons_ne_nil i r) = k ∧
      ∃ v, v ∈ i :: r ∧ v ∈ fronteira φ j := by
  obtain ⟨r, hp, hl⟩ := toda_cadeia_tem_percurso φ c
  exact ⟨r, hp, hl, o_percurso_atravessa_a_fronteira φ j r i hp hi (by rw [hl]; exact hk)⟩

end TGLExt.OSeparadorNoPercurso

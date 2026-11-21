import TGLExt.APonteDeCookLevin
set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Reconstrução por escolhas de ramos, condicionada a um leitor correto

O algoritmo abaixo recebe um decisor `d` de SAT.
Ele fixa um nome por vez por uma cláusula unitária, sem enumerar atribuições.
A prova de correção exige explicitamente `hd`; a contagem é de chamadas ao
decisor, não de movimentos de fita nem de tempo interno dessas chamadas.
Não há afirmação de que tal leitor tenha realização polinomial em TM2.
-/

namespace TGLExt.Reconstrucao

open TGLExt.TraducaoTuring TGLExt.APonteDeCookLevin

variable {n : ℕ}

def Good (φ : CNF n) (x : Fin n → Bool) : Prop :=
  ∀ C ∈ φ, satisfeita C x = true

/-- Acrescenta uma unidade, mantendo o mesmo espaço de nomes `Fin n`. -/
def force (φ : CNF n) (i : Fin n) (b : Bool) : CNF n := [⟨i, b⟩] :: φ

theorem force_good (φ : CNF n) (i : Fin n) (b : Bool) (x : Fin n → Bool) :
    Good (force φ i b) x ↔ x i = b ∧ Good φ x := by
  simp [Good, force, satisfeita, Literal.vale]

/-- Uma chamada ao leitor: tenta falso; se não houver solução, escolhe verdadeiro. -/
def choose (d : CNF n → Bool) (φ : CNF n) (i : Fin n) : Bool :=
  !(d (force φ i false))

theorem chosen_sat (d : CNF n → Bool) (hd : ∀ φ, d φ = true ↔ SAT φ)
    (φ : CNF n) (i : Fin n) (hφ : SAT φ) : SAT (force φ i (choose d φ i)) := by
  cases hread : d (force φ i false) with
  | true =>
    simpa [choose, hread] using (hd (force φ i false)).mp hread
  | false =>
    obtain ⟨x, hx⟩ := hφ
    have hxi : x i = true := by
      cases hi : x i with
      | true => rfl
      | false =>
        have hf : SAT (force φ i false) :=
          ⟨x, (force_good φ i false x).mpr ⟨hi, hx⟩⟩
        have hh := (hd (force φ i false)).mpr hf
        simp [hread] at hh
    refine ⟨x, ?_⟩
    apply (force_good φ i (choose d φ i) x).mpr
    exact ⟨by simpa [choose, hread] using hxi, hx⟩

/-- O segundo componente conta as chamadas explícitas a `d`: uma por nó da lista. -/
def run (d : CNF n → Bool) (φ : CNF n) : List (Fin n) → List (Fin n × Bool) × ℕ
  | [] => ([], 0)
  | i :: is =>
    let b := choose d φ i
    let tail := run d (force φ i b) is
    ((i, b) :: tail.1, tail.2 + 1)

theorem run_count (d : CNF n → Bool) (φ : CNF n) (is : List (Fin n)) :
    (run d φ is).2 = is.length := by
  induction is generalizing φ with
  | nil => rfl
  | cons i is ih => simp [run, ih]

theorem run_indices (d : CNF n → Bool) (φ : CNF n) (is : List (Fin n)) :
    ((run d φ is).1.map Prod.fst) = is := by
  induction is generalizing φ with
  | nil => rfl
  | cons i is ih => simp [run, ih]

theorem run_sound (d : CNF n → Bool) (hd : ∀ φ, d φ = true ↔ SAT φ)
    (φ : CNF n) (is : List (Fin n)) (hφ : SAT φ) :
    ∃ x, Good φ x ∧ ∀ p ∈ (run d φ is).1, x p.1 = p.2 := by
  induction is generalizing φ with
  | nil =>
    obtain ⟨x, hx⟩ := hφ
    exact ⟨x, hx, by simp [run]⟩
  | cons i is ih =>
    obtain ⟨x, hx, htail⟩ := ih (force φ i (choose d φ i)) (chosen_sat d hd φ i hφ)
    have hx' := (force_good φ i (choose d φ i) x).mp hx
    refine ⟨x, hx'.2, ?_⟩
    intro p hp
    have hm : p = (i, choose d φ i) ∨ p ∈ (run d (force φ i (choose d φ i)) is).1 := by
      simpa [run] using hp
    rcases hm with rfl | hp
    · exact hx'.1
    · exact htail p hp

/-- Decodificação computável de rótulos; nenhuma escolha clássica no algoritmo. -/
def decode : List (Fin n × Bool) → Fin n → Bool
  | [], _ => false
  | (j, b) :: tail, i => if i = j then b else decode tail i

theorem decode_agrees (ps : List (Fin n × Bool)) (x : Fin n → Bool)
    (hps : ∀ p ∈ ps, x p.1 = p.2) (i : Fin n) (hi : i ∈ ps.map Prod.fst) :
    decode ps i = x i := by
  induction ps with
  | nil => simp at hi
  | cons p ps ih =>
    rcases p with ⟨j, b⟩
    by_cases hij : i = j
    · subst i
      simpa [decode] using (hps (j, b) (by simp)).symm
    · have hit : i ∈ ps.map Prod.fst := by simpa [hij] using hi
      have hpt : ∀ p ∈ ps, x p.1 = p.2 := fun p hp => hps p (by simp [hp])
      simpa [decode, hij] using ih hpt hit

/-- Reconstrói todos os nomes, usando exatamente `n` consultas ao leitor. -/
def witness (d : CNF n → Bool) (φ : CNF n) : Fin n → Bool :=
  decode (run d φ (List.finRange n)).1

theorem witness_correct (d : CNF n → Bool) (hd : ∀ φ, d φ = true ↔ SAT φ)
    (φ : CNF n) (hφ : SAT φ) : Good φ (witness d φ) := by
  obtain ⟨x, hx, hps⟩ := run_sound d hd φ (List.finRange n) hφ
  have heq : witness d φ = x := by
    funext i
    apply decode_agrees _ x hps i
    rw [run_indices]
    simp
  rw [heq]
  exact hx

theorem witness_queries (d : CNF n → Bool) (φ : CNF n) :
    (run d φ (List.finRange n)).2 = n := by
  rw [run_count]
  simp

/-- A primeira consulta decide se reconstruir; as demais são as escolhas de ramos. -/
def solve (d : CNF n → Bool) (φ : CNF n) : Option (Fin n → Bool) × ℕ :=
  if d φ then
    let trace := run d φ (List.finRange n)
    (some (decode trace.1), trace.2 + 1)
  else (none, 1)

theorem solve_correct (d : CNF n → Bool) (hd : ∀ φ, d φ = true ↔ SAT φ)
    (φ : CNF n) :
    ((solve d φ).1 = none ↔ ¬ SAT φ) ∧
    (∀ x, (solve d φ).1 = some x → Good φ x) ∧
    (solve d φ).2 ≤ n + 1 := by
  cases hh : d φ with
  | false =>
    have hns : ¬ SAT φ := by intro hs; have := (hd φ).mpr hs; simp [hh] at this
    simp [solve, hh, hns]
  | true =>
    have hs : SAT φ := (hd φ).mp hh
    have hw := witness_correct d hd φ hs
    simpa [solve, hh, witness, witness_queries, hs] using hw

/-- Nomes efetivamente escritos, com repetições: não percorre nomes não usados. -/
def occurrences (φ : CNF n) : List (Fin n) := φ.flatten.map Literal.var

theorem occurrences_le_letters (φ : CNF n) : (occurrences φ).length ≤ letras φ := by
  unfold occurrences
  rw [List.length_map, List.length_flatten]
  unfold letras
  omega

def witnessByLetters (d : CNF n → Bool) (φ : CNF n) : Fin n → Bool :=
  decode (run d φ (occurrences φ)).1

theorem witnessByLetters_correct (d : CNF n → Bool)
    (hd : ∀ φ, d φ = true ↔ SAT φ) (φ : CNF n) (hφ : SAT φ) :
    Good φ (witnessByLetters d φ) := by
  obtain ⟨x, hx, hps⟩ := run_sound d hd φ (occurrences φ) hφ
  intro C hC
  have hxC := hx C hC
  unfold satisfeita at hxC ⊢
  rw [List.any_eq_true] at hxC ⊢
  obtain ⟨l, hl, hxval⟩ := hxC
  refine ⟨l, hl, ?_⟩
  have hm : l.var ∈ ((run d φ (occurrences φ)).1.map Prod.fst) := by
    rw [run_indices]
    exact List.mem_map.mpr ⟨l, List.mem_flatten.mpr ⟨C, hC, hl⟩, rfl⟩
  have heq := decode_agrees _ x hps l.var hm
  simpa [Literal.vale, witnessByLetters, heq] using hxval

theorem witnessByLetters_queries (d : CNF n → Bool) (φ : CNF n) :
    (run d φ (occurrences φ)).2 ≤ letras φ := by
  rw [run_count]
  exact occurrences_le_letters φ

/-- Rastro das fórmulas consultadas; reproduz exatamente a escolha de cada passo. -/
def queries (d : CNF n → Bool) (φ : CNF n) : List (Fin n) → List (CNF n)
  | [] => []
  | i :: is => force φ i false :: queries d (force φ i (choose d φ i)) is

theorem queries_count (d : CNF n → Bool) (φ : CNF n) (is : List (Fin n)) :
    (queries d φ is).length = (run d φ is).2 := by
  rw [run_count]
  induction is generalizing φ with
  | nil => rfl
  | cons i is ih => simp [queries, ih]

theorem force_letters (φ : CNF n) (i : Fin n) (b : Bool) :
    letras (force φ i b) = letras φ + 2 := by
  simp [letras, force]
  omega

theorem query_letters (d : CNF n → Bool) (φ : CNF n) (is : List (Fin n))
    (q : CNF n) (hq : q ∈ queries d φ is) :
    letras q ≤ letras φ + 2 * is.length := by
  induction is generalizing φ with
  | nil => simp [queries] at hq
  | cons i is ih =>
    simp only [queries, List.mem_cons] at hq
    rcases hq with rfl | hq
    · rw [force_letters]
      simp only [List.length_cons]
      omega
    · have hb := ih (force φ i (choose d φ i)) hq
      rw [force_letters] at hb
      simp only [List.length_cons]
      omega

/-- Soma dos comprimentos de consulta, não uma declaração de tempo de execução. -/
theorem query_letters_total (d : CNF n → Bool) (φ : CNF n) (is : List (Fin n)) :
    ((queries d φ is).map letras).sum ≤ is.length * (letras φ + 2 * is.length) := by
  induction is generalizing φ with
  | nil => simp [queries]
  | cons i is ih =>
    have hb := ih (force φ i (choose d φ i))
    rw [force_letters] at hb
    simp only [queries, List.map_cons, List.sum_cons, List.length_cons, force_letters]
    nlinarith

theorem queryByLetters_bound (d : CNF n → Bool) (φ : CNF n) :
    (∀ q ∈ queries d φ (occurrences φ), letras q ≤ 3 * letras φ) ∧
    ((queries d φ (occurrences φ)).map letras).sum ≤ 3 * (letras φ)^2 := by
  have hocc := occurrences_le_letters φ
  constructor
  · intro q hq
    have hb := query_letters d φ (occurrences φ) q hq
    omega
  · have hb := query_letters_total d φ (occurrences φ)
    nlinarith

def solveByLetters (d : CNF n → Bool) (φ : CNF n) : Option (Fin n → Bool) × ℕ :=
  if d φ then
    let trace := run d φ (occurrences φ)
    (some (decode trace.1), trace.2 + 1)
  else (none, 1)

theorem solveByLetters_correct (d : CNF n → Bool) (hd : ∀ φ, d φ = true ↔ SAT φ)
    (φ : CNF n) :
    ((solveByLetters d φ).1 = none ↔ ¬ SAT φ) ∧
    (∀ x, (solveByLetters d φ).1 = some x → Good φ x) ∧
    (solveByLetters d φ).2 ≤ letras φ + 1 := by
  cases hh : d φ with
  | false =>
    have hns : ¬ SAT φ := by intro hs; have := (hd φ).mpr hs; simp [hh] at this
    simp [solveByLetters, hh, hns]
  | true =>
    have hs : SAT φ := (hd φ).mp hh
    have hw := witnessByLetters_correct d hd φ hs
    have hc := witnessByLetters_queries d φ
    simpa [solveByLetters, hh, witnessByLetters, hs] using And.intro hw (Nat.add_le_add_right hc 1)


end TGLExt.Reconstrucao

import TGLExt.OResumoEPsiBit
import TGLExt.PontePalavraVerbo

/-! Leitor discreto da Palavra. Cada linha verdadeira da tabela representa uma atribuição
da fronteira extensível ao prefixo. A implementação materializa a nova lista a partir
da lista anterior. As duas leituras de uma variável são alternativas sobre o mesmo
contexto; nenhuma cláusula é distribuída contra outra. -/
namespace IALD.RelacaoFronteira

open TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit IALD.LeitorDaFormula
open TGLExt.OPsibitEACompressao

abbrev Assignment (n : ℕ) := Fin n → Bool

def agree {n} (s : Finset (Fin n)) (x y : Assignment n) : Prop :=
  ∀ i ∈ s, x i = y i

private theorem restrictAgree {n} {s t : Finset (Fin n)} (h : s ⊆ t)
    {x y : Assignment n} (a : agree t x y) : agree s x y :=
  fun i hi => a i (h hi)

private theorem flipAgree {n} {s : Finset (Fin n)} {x y : Assignment n}
    (a : agree s x y) : agree s y x := fun i hi => (a i hi).symm

private theorem chainAgree {n} {s : Finset (Fin n)} {x y z : Assignment n}
    (a : agree s x y) (b : agree s y z) : agree s x z :=
  fun i hi => (a i hi).trans (b i hi)

def keys {n} (s : Finset (Fin n)) : List (Fin n) :=
  (List.finRange n).filter (fun i => decide (i ∈ s))

@[simp] theorem mem_keys {n} {s : Finset (Fin n)} {i : Fin n} :
    i ∈ keys s ↔ i ∈ s := by simp [keys]

def agrees {n} (s : Finset (Fin n)) (x y : Assignment n) : Bool :=
  (keys s).all (fun i => x i == y i)

@[simp] theorem agrees_spec {n} (s : Finset (Fin n)) (x y : Assignment n) :
    agrees s x y = true ↔ agree s x y := by simp [agrees, agree, List.all_eq_true]

def enumerate {n} : List (Fin n) → List (Assignment n)
  | [] => [fun _ => false]
  | i :: tail => (enumerate tail).flatMap (fun z => [Function.update z i false, Function.update z i true])

private theorem enumerate_complete {n} (is : List (Fin n)) (x : Assignment n) :
    ∃ y ∈ enumerate is, ∀ i ∈ is, y i = x i := by
  induction is with
  | nil => exact ⟨_, List.mem_cons_self, by simp⟩
  | cons i is ih =>
    obtain ⟨y, hy, he⟩ := ih
    refine ⟨Function.update y i (x i), List.mem_flatMap.mpr ⟨y,hy,?_⟩, ?_⟩
    · cases h : x i <;> simp
    · intro j hj
      by_cases e : j = i
      · subst j; simp
      · rw [Function.update_of_ne e]
        exact he j ((List.mem_cons.mp hj).resolve_left e)

def cells {n} (s : Finset (Fin n)) : List (Assignment n) := enumerate (keys s)

theorem cells_cover {n} (s : Finset (Fin n)) (x : Assignment n) :
    ∃ y ∈ cells s, agree s y x := by
  obtain ⟨y,hm,ha⟩ := enumerate_complete (keys s) x
  exact ⟨y,hm,fun i hi => ha i (mem_keys.mpr hi)⟩

private theorem enumerate_length {n} (is : List (Fin n)) :
    (enumerate is).length = 2 ^ is.length := by
  induction is with
  | nil => rfl
  | cons i is ih =>
    simp [enumerate, List.length_flatMap, ih, Nat.pow_succ, Nat.mul_comm]

theorem cells_length {n} (s : Finset (Fin n)) :
    (cells s).length = 2 ^ s.card := by
  rw [cells, enumerate_length]
  congr 1
  have nd : (keys s).Nodup := (List.nodup_finRange n).filter _
  have hs : (keys s).toFinset = s := by ext; simp
  exact (List.toFinset_card_of_nodup nd).symm.trans (congrArg Finset.card hs)

def lookup {n} (s : Finset (Fin n)) (rows : List (Assignment n)) (x : Assignment n) : Bool :=
  rows.any (fun y => agrees s y x)

@[simp] theorem lookup_spec {n} (s : Finset (Fin n)) (rows : List (Assignment n)) (x : Assignment n) :
    lookup s rows x = true ↔ ∃ y ∈ rows, agree s y x := by
  simp [lookup, List.any_eq_true]

private theorem lookup_transport {n} {s : Finset (Fin n)} {rows : List (Assignment n)}
    {x y : Assignment n} (ha : agree s x y) (hx : lookup s rows x = true) :
    lookup s rows y = true := by
  obtain ⟨w,hw,he⟩ := (lookup_spec ..).mp hx
  exact (lookup_spec ..).mpr ⟨w,hw,chainAgree he ha⟩

def bag {n} (s t : Finset (Fin n)) (c : Clausula n) := s ∪ t ∪ varsClausula c

/-- Restrição à célula seguinte, teste da cláusula lida e projeção das variáveis esquecidas. -/
def advance {n} (s t : Finset (Fin n)) (c : Clausula n)
    (old : List (Assignment n)) : List (Assignment n) :=
  (cells t).filter (fun u => (cells (bag s t c)).any (fun z =>
    lookup s old z && satisfeita c z && agrees t z u))

theorem advance_length {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n)) :
    (advance s t c old).length ≤ 2 ^ t.card := by
  rw [← cells_length t]
  exact List.length_filter_le ..

theorem advance_spec {n} (s t : Finset (Fin n)) (c : Clausula n)
    (old : List (Assignment n)) (u : Assignment n) :
    lookup t (advance s t c old) u = true ↔
    ∃ z, lookup s old z = true ∧ satisfeita c z = true ∧ agree t z u := by
  rw [lookup_spec]
  simp only [advance, List.mem_filter, List.any_eq_true, Bool.and_eq_true, agrees_spec]
  constructor
  · rintro ⟨v,⟨_,z,_,⟨ho,hc⟩,hv⟩,hu⟩
    exact ⟨z,ho,hc,chainAgree hv hu⟩
  · rintro ⟨z,ho,hc,hu⟩
    obtain ⟨v,hv,hvu⟩ := cells_cover t u
    obtain ⟨w,hw,hwz⟩ := cells_cover (bag s t c) z
    have hs : s ⊆ bag s t c := by intro i hi; simp [bag,hi]
    have ht : t ⊆ bag s t c := by intro i hi; simp [bag,hi]
    have hcl : varsClausula c ⊆ bag s t c := by intro i hi; simp [bag,hi]
    refine ⟨v,⟨hv,w,hw,⟨lookup_transport (flipAgree (restrictAgree hs hwz)) ho,?_⟩,
      chainAgree (chainAgree (restrictAgree ht hwz) hu) (flipAgree hvu)⟩,hvu⟩
    exact (satisfeita_so_ve_as_suas_variaveis c (restrictAgree hcl hwz)).trans hc

def boundary {n} (p rest : CNF n) := varsDas p ∩ varsDas rest

theorem boundary_eq_kimi {n} (φ : CNF n) (j : ℕ) :
    boundary (φ.take j) (φ.drop j) = fronteira φ j := rfl

def valid {n} (p rest : CNF n) (rows : List (Assignment n)) : Prop :=
  ∀ u, lookup (boundary p rest) rows u = true ↔
    ∃ x, passes p x = true ∧ agree (boundary p rest) x u

private theorem prefix_congr {n} (p : CNF n) {x y : Assignment n}
    (h : agree (varsDas p) x y) : passes p x = passes p y := by
  apply Bool.eq_iff_iff.mpr
  simp only [passes, List.all_eq_true]
  apply forall_congr'
  intro c
  apply forall_congr'
  intro hc
  rw [satisfeita_so_ve_as_suas_variaveis c (fun i hi => h i (mem_varsDas_of_mem hc hi))]

private theorem holds_append {n} (p : CNF n) (c : Clausula n) (x : Assignment n) :
    passes (p ++ [c]) x = (passes p x && satisfeita c x) := by simp [passes]

/-- A preservação das correlações: a mesma atribuição satisfaz o prefixo e a cláusula.
Quando duas testemunhas concordam no corte, colam-se nas variáveis compartilhadas. -/
theorem advance_valid {n} (p rest : CNF n) (c : Clausula n) (rows : List (Assignment n))
    (H : valid p (c :: rest) rows) :
    valid (p ++ [c]) rest
      (advance (boundary p (c :: rest)) (boundary (p ++ [c]) rest) c rows) := by
  intro u
  rw [advance_spec]
  constructor
  · rintro ⟨z,ho,hcz,hu⟩
    obtain ⟨w,hw,hwz⟩ := (H z).mp ho
    let y : Assignment n := fun i => if i ∈ varsDas p then w i else z i
    have hp : agree (varsDas p) y w := by intro i hi; simp [y,hi]
    have hf : agree (varsDas (c :: rest)) y z := by
      intro i hi
      by_cases hi' : i ∈ varsDas p
      · simpa [y,hi'] using hwz i (Finset.mem_inter.mpr ⟨hi',hi⟩)
      · simp [y,hi']
    have hcl : varsClausula c ⊆ varsDas (c :: rest) := fun _ hi =>
      mem_varsDas_of_mem List.mem_cons_self hi
    have hr : varsDas rest ⊆ varsDas (c :: rest) := by
      intro i hi
      change i ∈ varsClausula c ∪ varsDas rest
      exact Finset.mem_union_right _ hi
    refine ⟨y,?_,?_⟩
    · rw [holds_append, Bool.and_eq_true]
      exact ⟨(prefix_congr p hp).trans hw,
        (satisfeita_so_ve_as_suas_variaveis c (restrictAgree hcl hf)).trans hcz⟩
    · exact chainAgree (restrictAgree (fun _ hi => hr (Finset.mem_inter.mp hi).2) hf) hu
  · rintro ⟨x,hx,hu⟩
    rw [holds_append, Bool.and_eq_true] at hx
    exact ⟨x,(H x).mpr ⟨x,hx.1,fun _ _ => rfl⟩,hx.2,hu⟩

def zero {n : ℕ} : Assignment n := fun _ => false

theorem initial_valid {n} (rest : CNF n) : valid [] rest [zero] := by
  intro u
  simp [lookup, agrees, boundary, varsDas, keys, passes, agree]

/-- Leitor em ordem de cláusulas. A tabela é uma lista materializada de células aceitas. -/
def scan {n} (p : CNF n) (rows : List (Assignment n)) : CNF n → List (Assignment n)
  | [] => rows
  | c :: rest => scan (p ++ [c])
      (advance (boundary p (c :: rest)) (boundary (p ++ [c]) rest) c rows) rest

theorem scan_spec {n} (p rest : CNF n) (rows : List (Assignment n)) (h : valid p rest rows) :
    lookup ∅ (scan p rows rest) zero = true ↔ SAT (p ++ rest) := by
  induction rest generalizing p rows with
  | nil =>
    have hh := h zero
    simpa [scan, boundary, varsDas, agree, sat_iff] using hh
  | cons c rest ih =>
    simpa only [scan, List.append_assoc, List.singleton_append] using ih (p ++ [c]) _
      (advance_valid p rest c rows h)

/-- Nenhuma atribuição global nem peso é entrada do leitor. -/
def read {n} (φ : CNF n) : Bool := lookup ∅ (scan [] [zero] φ) zero

theorem read_spec {n} (φ : CNF n) : read φ = true ↔ SAT φ := by
  simpa [read] using scan_spec [] φ _ (initial_valid φ)

theorem read_word {n} (φ : CNF n) (s : ℝ) (hs : (n:ℝ) * Real.log 2 < s) :
    read φ = true ↔ palavra (custoCNF φ) s := (read_spec φ).trans (a_palavra_decide n hs φ)

end IALD.RelacaoFronteira

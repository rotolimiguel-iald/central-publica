import TGLExt.CustoDaBuscaLiteral

/-! A projected binary CNF is closed under coordinatewise majority, even
with hidden auxiliary variables. A single elimination from width three
already gives a relation outside this exact symbolic cache. -/
set_option autoImplicit false
namespace Codex.BinaryLimit
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
variable {n : Nat}

def majority (a b c : Bool) : Bool := (a && b) || (a && c) || (b && c)
def merge {ι : Type} (x y z : ι → Bool) (i : ι) := majority (x i) (y i) (z i)

private theorem literal_merge (l : Literal n) (x y z : Fin n → Bool) :
    l.vale (merge x y z) = majority (l.vale x) (l.vale y) (l.vale z) := by
  simp only [Literal.vale,merge]
  cases x l.var <;> cases y l.var <;> cases z l.var <;> cases l.pos <;> rfl

private theorem pair_merge (a b c d e f : Bool)
    (h₁ : (a || d) = true) (h₂ : (b || e) = true) (h₃ : (c || f) = true) :
    (majority a b c || majority d e f) = true := by
  revert h₁ h₂ h₃
  decide +revert

private theorem clause_closed (c : Clausula n) (width : c.length ≤ 2)
    (x y z : Fin n → Bool) (hx : satisfeita c x = true) (hy : satisfeita c y = true)
    (hz : satisfeita c z = true) : satisfeita c (merge x y z) = true := by
  cases c with
  | nil => contradiction
  | cons a t =>
    cases t with
    | nil => simp only [satisfeita,List.any_cons,List.any_nil,Bool.or_false,literal_merge] at *
             simp [majority,hx,hy]
    | cons b t =>
      cases t with
      | nil =>
        simp only [satisfeita,List.any_cons,List.any_nil,Bool.or_false,literal_merge] at *
        exact pair_merge _ _ _ _ _ _ hx hy hz
      | cons _ _ => simp at width

theorem binary_majority (p : CNF n) (width : ∀ c ∈ p, c.length ≤ 2)
    (x y z : Fin n → Bool) (hx : passes p x = true) (hy : passes p y = true)
    (hz : passes p z = true) : passes p (merge x y z) = true := by
  simp only [passes,List.all_eq_true] at hx hy hz ⊢
  exact fun c hc => clause_closed c (width c hc) x y z (hx c hc) (hy c hc) (hz c hc)

def projected {m : Nat} (p : CNF n) (display : Fin m → Fin n) (x : Fin m → Bool) :=
  ∃ y, passes p y = true ∧ ∀ i, y (display i) = x i

theorem projected_majority {m : Nat} (p : CNF n) (w : ∀ c ∈ p, c.length ≤ 2)
    (display : Fin m → Fin n) (x y z : Fin m → Bool) :
    projected p display x → projected p display y → projected p display z →
      projected p display (merge x y z) := by
  rintro ⟨a,ha,ra⟩ ⟨b,hb,rb⟩ ⟨c,hc,rc⟩
  exact ⟨merge a b c,binary_majority p w a b c ha hb hc,fun i => by simp [merge,ra,rb,rc]⟩

def four (x : Fin 4 → Bool) := x 0 || x 1 || x 2 || x 3
def exampleFormula : CNF 5 :=
  [[⟨0,true⟩,⟨1,true⟩,⟨2,true⟩],[⟨0,false⟩,⟨3,true⟩,⟨4,true⟩]]

theorem free_pivot (x : Fin 4 → Bool) :
    (∃ b, passes exampleFormula (Fin.cases b x) = true) ↔ four x = true := by
  change (∃ b : Bool, (((b == true) || ((x 0 == true) || ((x 1 == true) || false))) &&
    (((b == false) || ((x 2 == true) || ((x 3 == true) || false))) && true)) = true) ↔ _
  cases h₀ : x 0 <;> cases h₁ : x 1 <;> cases h₂ : x 2 <;> cases h₃ : x 3 <;>
    simp [four,h₀,h₁,h₂,h₃]

/-- No binary CNF with any number of existentially hidden variables has this projection. -/
theorem no_binary_replacement (p : CNF n) (w : ∀ c ∈ p, c.length ≤ 2) (display : Fin 4 → Fin n) :
    ¬ (∀ x, projected p display x ↔ four x = true) := by
  intro representation
  let one (j : Fin 4) (i : Fin 4) := decide (i = j)
  have hx := (representation (one 0)).mpr (by decide)
  have hy := (representation (one 1)).mpr (by decide)
  have hz := (representation (one 2)).mpr (by decide)
  have all := (representation _).mp (projected_majority p w display _ _ _ hx hy hz)
  exact (by decide : four (merge (one 0) (one 1) (one 2)) ≠ true) all

end Codex.BinaryLimit

import TGLExt.LimiteDoCacheExplicito

/-! Conditional independence glues actual valuations. The block partition and
the pair indices in the direct query are given; this is not a parsing cost. -/
set_option autoImplicit false
namespace Codex.IndependentFactors
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.BranchPresence
variable {n : Nat}

def appears (p : CNF n) (i : Fin n) :=
  p.any (fun c => c.any (fun l => l.var == i))

def splitAtLabels (p q : CNF n) (ms : List (Literal n)) : Prop :=
  ∀ i, appears p i = true → appears q i = true → ∃ l ∈ ms, l.var = i

def paste (p : CNF n) (x y : Fin n → Bool) (i : Fin n) :=
  if appears p i then x i else y i

private theorem transfer (p : CNF n) (x y : Fin n → Bool)
    (agrees : ∀ i, appears p i = true → x i = y i) (ok : passes p x = true) :
    passes p y = true := by
  apply List.all_eq_true.mpr
  intro c hc
  obtain ⟨l,hl,v⟩ := List.any_eq_true.mp (List.all_eq_true.mp ok c hc)
  have seen : appears p l.var = true :=
    List.any_eq_true.mpr ⟨c,hc,List.any_eq_true.mpr ⟨l,hl,by simp⟩⟩
  exact List.any_eq_true.mpr ⟨l,hl,by simpa only [Literal.vale,agrees l.var seen] using v⟩

private theorem append_sat (p q : CNF n) (x : Fin n → Bool) :
    passes (p++q) x = true ↔ passes p x = true ∧ passes q x = true := by
  simp [passes]

theorem glue (p q : CNF n) (ms : List (Literal n)) (cut : splitAtLabels p q ms)
    (x y : Fin n → Bool) (px : passes p x=true) (qy : passes q y=true)
    (xm : Agrees x ms) (ym : Agrees y ms) :
    passes (p++q) (paste p x y) = true ∧ Agrees (paste p x y) ms := by
  refine ⟨(append_sat _ _ _).mpr ⟨?_,?_⟩,?_⟩
  · exact transfer p x _ (fun i hi => by simp [paste,hi]) px
  · apply transfer q y _ _ qy
    intro i hq
    by_cases hp : appears p i = true
    · obtain ⟨l,hm,rfl⟩ := cut i hp hq
      simp only [paste,hp,if_true]
      exact (ym l hm).trans (xm l hm).symm
    · simp [paste,hp]
  · intro l hl
    cases e : appears p l.var <;> simp [paste,e,ym l hl,xm l hl]

theorem compatible_factors (p q : CNF n) (ms : List (Literal n)) (cut : splitAtLabels p q ms) :
    Compatible (p++q) ms ↔ Compatible p ms ∧ Compatible q ms := by
  constructor
  · rintro ⟨x,ok,m⟩
    obtain ⟨a,b⟩ := (append_sat p q x).mp ok
    exact ⟨⟨x,a,m⟩,⟨x,b,m⟩⟩
  · rintro ⟨⟨x,px,xm⟩,⟨y,qy,ym⟩⟩
    exact ⟨paste p x y,glue p q ms cut x y px qy xm ym⟩

theorem factor_bits (p q : CNF n) (ms : List (Literal n)) (cut : splitAtLabels p q ms) :
    search (p++q) ms = (search p ms && search q ms) := by
  apply Bool.eq_iff_iff.mpr
  rw [Bool.and_eq_true,search_correct,search_correct,search_correct,compatible_factors _ _ _ cut]

def separated (ms : List (Literal n)) : List (CNF n) → Prop
  | [] => True
  | p::rest => splitAtLabels p rest.flatten ms ∧ separated ms rest

/-- One exact compatibility query per supplied block if all preceding blocks
succeed, and a final consistency check for the common marks. -/
def blockBits (ms : List (Literal n)) : List (CNF n) → Bool
  | [] => consistent ms
  | p::rest => search p ms && blockBits ms rest

theorem chain_factors (ms : List (Literal n)) (blocks : List (CNF n))
    (cut : separated ms blocks) : blockBits ms blocks = search blocks.flatten ms := by
  induction blocks with
  | nil => rfl
  | cons p rest ih =>
    change (search p ms && blockBits ms rest) = search (p++rest.flatten) ms
    rw [ih cut.2,factor_bits p _ _ cut.1]

open Codex.ExplicitCache

private theorem mixed_pairs {k : Nat} (i : Fin k) (b : Bool) (x : Fin (2*k) → Bool) :
    passes (pairs k true ++ continuation i b) x = true ↔
      (∀ j, x (addr j false) ≠ x (addr j true)) ∧ x (addr i b)=true := by
  rw [append_sat,continuation,append_sat,pair_condition,pair_condition]
  have single : passes [[label i b true]] x = x (addr i b) := by
    simp [passes,label,satisfeita,Literal.vale]
  rw [single]
  constructor
  · rintro ⟨p,m,t⟩
    refine ⟨?_,t⟩
    intro j
    specialize p j
    specialize m j
    cases val : x (addr j false) <;> simp_all
  · rintro ⟨d,t⟩
    have hits (s : Bool) (j : Fin k) : x (addr j false)=s ∨ x (addr j true)=s := by
      specialize d j
      cases hl : x (addr j false) <;> cases hr : x (addr j true) <;> cases s <;> simp_all
    exact ⟨hits true,hits false,t⟩

/-- The final unit picks member b of pair i. Querying side s of pair j for
value v only compares the two supplied indices when the probe is already parsed. -/
def pairBit {k : Nat} (i : Fin k) (b : Bool) (j : Fin k) (s v : Bool) :=
  if j=i then ((s == b) == v) else true

private def orient {k : Nat} (i : Fin k) (b : Bool) (j : Fin k) (s v : Bool) (t : Fin k) :=
  if t=i then b else if t=j then (if v then s else !s) else false

theorem exact_pair_query {k : Nat} (i : Fin k) (b : Bool) (j : Fin k) (s v : Bool) :
    pairBit i b j s v = true ↔
      Compatible (pairs k true ++ continuation i b) [⟨addr j s,v⟩] := by
  constructor
  · intro bit
    let f := orient i b j s v
    refine ⟨row f,(mixed_pairs i b _).mpr ⟨?_,?_⟩,?_⟩
    · intro t
      cases e : f t <;> simp [row_value,e]
    · simp [row_value,f,orient]
    · have query : row f (addr j s) = v := by
        rw [row_value]
        by_cases same : j=i
        · subst j
          symm
          simpa [pairBit,f,orient,BEq.comm] using bit
        · cases v <;> cases s <;> simp [f,orient,same]
      simpa [Agrees] using query
  · rintro ⟨x,ok,marked⟩
    have pivot : x (addr j s)=v := marked ⟨addr j s,v⟩ (by simp)
    obtain ⟨unequal,unit⟩ := (mixed_pairs i b x).mp ok
    by_cases same : j=i
    · subst j
      specialize unequal i
      cases s <;> cases b <;> cases v <;> simp_all [pairBit]
    · simp [pairBit,same]

/-- Only the calls to the compatibility algorithm for complete blocks are counted.
The final consistency check, the search inside each block and finding the cut
are separate operations. -/
def counted (ms : List (Literal n)) : List (CNF n) → Bool × Nat
  | [] => (consistent ms,0)
  | p::rest => if search p ms then
      let tail := counted ms rest
      (tail.1,tail.2+1)
    else (false,1)

theorem count_blocks (ms : List (Literal n)) (blocks : List (CNF n)) :
    (counted ms blocks).1 = blockBits ms blocks ∧ (counted ms blocks).2 ≤ blocks.length := by
  induction blocks with
  | nil => exact ⟨rfl,Nat.le_refl _⟩
  | cons p rest ih =>
    cases e : search p ms <;> simp [counted,blockBits,e,ih.1,ih.2]

theorem split_query_bound (ms : List (Literal n)) (blocks : List (CNF n))
    (cut : separated ms blocks) :
    (counted ms blocks).1 = search blocks.flatten ms ∧ (counted ms blocks).2 ≤ blocks.length := by
  obtain ⟨eq,lim⟩ := count_blocks ms blocks
  exact ⟨eq.trans (chain_factors ms blocks cut),lim⟩

end Codex.IndependentFactors

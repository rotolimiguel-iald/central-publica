import TGLExt.RelacaoFronteira
import TGLExt.ParPonderado

/-! A finite four-letter implementation for decision; an exact weighted contraction is
a separate mathematical identity. No real operation is used by the discrete reader. -/
namespace IALD.PsiBitNaFronteira
open TGLExt.TraducaoTuring TGLExt.Psibit TGLExt.OResumoEPsiBit
open IALD.LeitorDaFormula IALD.RelacaoFronteira

inductive Letter | neither | left | right | both deriving DecidableEq, Repr

def encode : Bool → Bool → Letter
  | false, false => .neither
  | true, false => .left
  | false, true => .right
  | true, true => .both

def bits : Letter → Bool × Bool
  | .neither => (false,false)
  | .left => (true,false)
  | .right => (false,true)
  | .both => (true,true)

@[simp] theorem bits_encode (a b : Bool) : bits (encode a b) = (a,b) := by
  cases a <;> cases b <;> rfl

/-- A concrete amplitude on the canonical unit orbit for each letter.
Its positive squared first coordinate is always 9/25; only the signs vary. -/
noncomputable def amplitude (a : Letter) : ℝ × ℝ :=
  (if (bits a).1 then 3/5 else -(3/5), if (bits a).2 then 4/5 else -(4/5))

theorem canonical_reading (a : Letter) :
    ∃ θ : ℝ, v θ = amplitude a ∧
      (codeAmp θ).word = bitSign (bits a).1 ∧
      (codeAmp θ).verb = bitSign (bits a).2 ∧
      (codeAmp θ).weight = 9/25 ∧ decodeAmp (codeAmp θ) = amplitude a := by
  have h : amplitude a ∈ UnitVec := by
    change (amplitude a).1 ^ 2 + (amplitude a).2 ^ 2 = 1
    cases a <;> norm_num [amplitude,bits]
  obtain ⟨θ,he⟩ := exists_angle_of_unit h
  refine ⟨θ,he,?_,?_,?_,(decodeAmp_codeAmp θ).trans he⟩
  all_goals rw [codeAmp, he]
  all_goals cases a <;> norm_num [codeOf, amplitude, bits, bitSign, SignType.sign]

def accepts : Letter → Bool
  | .neither => false
  | _ => true

@[simp] theorem accepts_encode (a b : Bool) : accepts (encode a b) = (a || b) := by
  cases a <;> cases b <;> rfl

def testRow {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n))
    (target x : Assignment n) : Bool :=
  lookup s old x && satisfeita c x && agrees t x target

private theorem testRow_congr {n} (s t : Finset (Fin n)) (c : Clausula n)
    (old : List (Assignment n)) (target x y : Assignment n)
    (h : agree (bag s t c) x y) : testRow s t c old target x = testRow s t c old target y := by
  have hs (i) (hi : i ∈ s) := h i (show i ∈ bag s t c by simp [bag,hi])
  have ht (i) (hi : i ∈ t) := h i (show i ∈ bag s t c by simp [bag,hi])
  have hc (i) (hi : i ∈ varsClausula c) := h i (show i ∈ bag s t c by simp [bag,hi])
  apply Bool.eq_iff_iff.mpr
  simp only [testRow,Bool.and_eq_true,lookup_spec,agrees_spec,satisfeita_so_ve_as_suas_variaveis c hc]
  constructor
  · rintro ⟨⟨⟨r,hr,ha⟩,hv⟩,hb⟩
    exact ⟨⟨⟨r,hr,fun i hi => (ha i hi).trans (hs i hi)⟩,hv⟩,fun i hi => (ht i hi).symm.trans (hb i hi)⟩
  · rintro ⟨⟨⟨r,hr,ha⟩,hv⟩,hb⟩
    exact ⟨⟨⟨r,hr,fun i hi => (ha i hi).trans (hs i hi).symm⟩,hv⟩,fun i hi => (ht i hi).trans (hb i hi)⟩

/-- Both branches use exactly the same outside assignment z and new-row target u. -/
def letterAt {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n))
    (u z : Assignment n) (i : Fin n) : Letter :=
  encode (testRow s t c old u (Function.update z i false))
         (testRow s t c old u (Function.update z i true))

def visitPairs {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n))
    (u : Assignment n) (i : Fin n) : Bool :=
  (cells ((bag s t c).erase i)).any (fun z => accepts (letterAt s t c old u z i))

theorem visitPairs_spec {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n))
    (u : Assignment n) (i : Fin n) :
    visitPairs s t c old u i = true ↔ ∃ x, testRow s t c old u x = true := by
  simp only [visitPairs,List.any_eq_true,letterAt,accepts_encode,Bool.or_eq_true]
  constructor
  · rintro ⟨z,_,h | h⟩
    · exact ⟨_,h⟩
    · exact ⟨_,h⟩
  · rintro ⟨x,hx⟩
    obtain ⟨z,hz,hzx⟩ := cells_cover ((bag s t c).erase i) x
    have he : agree (bag s t c) (Function.update z i (x i)) x := by
      intro j hj
      by_cases hji : j = i
      · subst j; simp
      · rw [Function.update_of_ne hji]
        exact hzx j (Finset.mem_erase.mpr ⟨hji,hj⟩)
    have hit := (testRow_congr s t c old u _ _ he).trans hx
    refine ⟨z,hz,?_⟩
    cases hxi : x i
    · exact Or.inl (by simpa [hxi] using hit)
    · exact Or.inr (by simpa [hxi] using hit)

def pairedAdvance {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n)) :
    List (Assignment n) :=
  match c with
  | [] => []
  | l :: tail => (cells t).filter (fun u => visitPairs s t (l :: tail) old u l.var)

theorem pairedAdvance_eq {n} (s t : Finset (Fin n)) (c : Clausula n) (old : List (Assignment n)) :
    pairedAdvance s t c old = advance s t c old := by
  cases c with
  | nil => simp [pairedAdvance,advance,satisfeita]
  | cons l tail =>
    unfold pairedAdvance advance
    apply List.filter_congr
    intro u _
    apply Bool.eq_iff_iff.mpr
    rw [visitPairs_spec, List.any_eq_true]
    constructor
    · rintro ⟨x,hx⟩
      obtain ⟨z,hz,hzx⟩ := cells_cover (bag s t (l :: tail)) x
      exact ⟨z,hz,(testRow_congr s t (l :: tail) old u z x hzx).trans hx⟩
    · rintro ⟨z,_,hz⟩
      exact ⟨z,hz⟩

def pairedScan {n} (p : CNF n) (old : List (Assignment n)) : CNF n → List (Assignment n)
  | [] => old
  | c :: rest => pairedScan (p ++ [c])
      (pairedAdvance (boundary p (c :: rest)) (boundary (p ++ [c]) rest) c old) rest

theorem pairedScan_eq {n} (p rest : CNF n) (old : List (Assignment n)) :
    pairedScan p old rest = scan p old rest := by
  induction rest generalizing p old with
  | nil => rfl
  | cons c cs ih => simp only [pairedScan,scan,pairedAdvance_eq,ih]

def word {n} (φ : CNF n) : Bool := lookup ∅ (pairedScan [] [zero] φ) zero

/-- The same x must extend across clauses. These are kernel reductions of the finite reader. -/
theorem same_assignment_controls :
    word ([[⟨0,true⟩],[⟨0,false⟩]] : CNF 1) = false ∧
    word ([[⟨0,true⟩,⟨1,true⟩],[⟨0,false⟩]] : CNF 2) = true ∧
    word ([[]] : CNF 0) = false ∧ word ([] : CNF 0) = true := by decide

theorem word_spec {n} (φ : CNF n) (s : ℝ) (hs : (n:ℝ)*Real.log 2 < s) :
    word φ = true ↔ TGLExt.OPsibitEACompressao.palavra (custoCNF φ) s := by
  unfold word
  rw [pairedScan_eq]
  exact read_word φ s hs

/-- Per output candidate in a nonempty clause, each visited context has two branches;
the routine may short-circuit. The allocated list of contexts has this exact length. -/
theorem contexts_per_row {n} (s t : Finset (Fin n)) (l : Literal n) (c : Clausula n) :
    2 * (cells ((bag s t (l :: c)).erase l.var)).length = 2 ^ (bag s t (l :: c)).card := by
  have h : l.var ∈ bag s t (l :: c) := Finset.mem_union_right _ (var_mem_varsClausula List.mem_cons_self)
  rw [cells_length, ← Finset.card_erase_add_one h, Nat.pow_succ, Nat.mul_comm]

/-- For exact weighted contraction, the two alternatives are paired in the SAME
separator context; a future continuation is applied to the corresponding branch. -/
noncomputable def jointValue (code : IALD.ParPonderado.Reading) (future : ℝ × ℝ) : ℝ :=
  let w := IALD.ParPonderado.unpack code
  w.1 * future.1 + w.2 * future.2

theorem weighted_pair_exact (w future : ℝ × ℝ) (h : 0 < w.1) :
    jointValue (IALD.ParPonderado.pack w) future = w.1 * future.1 + w.2 * future.2 := by
  simp only [jointValue, IALD.ParPonderado.round_trip w h]

theorem kimi_weight_pair {n} (p f : CNF (n+1)) (t : ℝ) (z : Fin n → Bool) :
    let x := Fin.cases false z
    let y := Fin.cases true z
    jointValue (IALD.ParPonderado.pack (pesoDas p t x,pesoDas p t y))
      (pesoDas f t x,pesoDas f t y) =
      pesoDas (p ++ f) t x + pesoDas (p ++ f) t y := by
  dsimp only
  have hp : 0 < pesoDas p t (Fin.cases false z) := by rw [pesoDas_eq_exp]; exact Real.exp_pos _
  rw [weighted_pair_exact _ _ hp]
  simp [pesoDas,List.map_append,List.prod_append]

end IALD.PsiBitNaFronteira

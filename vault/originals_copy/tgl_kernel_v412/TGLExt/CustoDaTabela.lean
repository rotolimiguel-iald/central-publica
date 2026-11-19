import TGLExt.RelacaoFronteira
import Mathlib.Analysis.SpecificLimits.Normed

/-! This concerns the explicitly materialized rows of this algorithm. The family is
easy if its repeated long clause is handled symbolically. -/
namespace IALD.CustoDaTabela
open IALD.RelacaoFronteira IALD.LeitorDaFormula TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit

def wide (n : ℕ) : Clausula (n+1) := (List.finRange (n+1)).map (fun i => ⟨i,true⟩)

theorem wide_vars (n : ℕ) : varsClausula (wide n) = Finset.univ := by
  ext i
  simp [wide,varsClausula,List.map_map,Function.comp_def]

theorem cut (n : ℕ) : boundary [wide n] [wide n] = Finset.univ := by
  simp [boundary,varsDas,wide_vars]

theorem wide_passes (n : ℕ) (x : Assignment n) :
    passes [wide n] (Fin.cases true x) = true := by
  change ([wide n] : CNF (n+1)).all _ = true
  simp only [List.all_cons,List.all_nil,Bool.and_true]
  apply List.any_eq_true.mpr
  exact ⟨⟨0,true⟩,List.mem_map.mpr ⟨0, List.mem_finRange _,rfl⟩,rfl⟩

/-- After the first of two equal positive clauses, every assignment with first
bit true is an actual, distinct *accepted* row, even if the table keeps only successes. -/
theorem required_rows (n : ℕ) (rows : List (Assignment (n+1)))
    (good : valid [wide n] [wide n] rows) : 2 ^ n ≤ rows.length := by
  classical
  have hm (x : Assignment n) : Fin.cases true x ∈ rows := by
    have hit := (good (Fin.cases true x)).mpr ⟨_,wide_passes n x, fun _ _ => rfl⟩
    obtain ⟨y,hy,ha⟩ := (lookup_spec ..).mp hit
    have he : y = Fin.cases true x := funext fun i => ha i (by rw [cut]; exact Finset.mem_univ _)
    rwa [← he]
  let code : Assignment n → ↥rows.toFinset := fun x => ⟨Fin.cases true x,List.mem_toFinset.mpr (hm x)⟩
  have inj : Function.Injective code := by
    intro a b h
    have eq := congrArg Subtype.val h
    exact funext fun i => congrFun eq i.succ
  have hc := Fintype.card_le_of_injective code inj
  calc
    2 ^ n = Fintype.card (Assignment n) := by simp [Assignment]
    _ ≤ Fintype.card ↥rows.toFinset := hc
    _ ≤ rows.length := by
      rw [Fintype.card_coe]
      exact List.toFinset_card_le rows

def firstRows (n : ℕ) := advance (boundary [] [wide n,wide n]) (boundary [wide n] [wide n])
    (wide n) [zero]

theorem actual_rows (n : ℕ) : 2 ^ n ≤ (firstRows n).length :=
  required_rows n _ (advance_valid [] [wide n] (wide n) [zero] (initial_valid _))

/-- Fixed finite alphabet. Unary indices, a sign terminating each literal, and one
end marker per clause give a self-delimiting word. Variables are numbered from zero. -/
inductive Mark | tick | pos | neg | stop deriving DecidableEq
def encodeClause {n : ℕ} (c : Clausula n) : List Mark :=
  c.flatMap (fun l => List.replicate l.var.val .tick ++ [if l.pos then .pos else .neg]) ++ [.stop]
def input (n : ℕ) : List Mark := encodeClause (wide n) ++ encodeClause (wide n)

private theorem literalTapeBound {n : ℕ} (c : Clausula n) :
    (c.flatMap (fun l => List.replicate l.var.val Mark.tick ++ [if l.pos then .pos else .neg])).length ≤ c.length * n := by
  induction c with
  | nil => simp
  | cons l c ih =>
    simp only [List.flatMap_cons,List.length_append,List.length_replicate,List.length_cons,List.length_nil]
    rw [Nat.add_mul]
    have hv := l.var.isLt
    omega

theorem short_input (n : ℕ) : (input n).length ≤ 2*((n+1)^2+1) := by
  have hb := literalTapeBound (wide n)
  have hl : (wide n).length = n+1 := by simp [wide]
  rw [hl] at hb
  simp only [input,encodeClause,List.length_append,List.length_cons,List.length_nil]
  rw [pow_two]
  omega

/-- An explicit failure of every input-length polynomial for THIS row materialization. -/
theorem no_uniform_row_polynomial (C d : ℕ) :
    ∃ n, C * (input n).length ^ d < (firstRows n).length := by
  have ha : ∀ᶠ n : ℕ in Filter.atTop,
      (n : ℝ)^(2*d) / (2:ℝ)^n < 1 / ((C:ℝ)*10^d+1) :=
    (tendsto_pow_const_div_const_pow_of_one_lt (2*d) (by norm_num : (1:ℝ)<2)).eventually_lt_const
      (by positivity)
  obtain ⟨n,hn,he⟩ := (ha.and (Filter.eventually_ge_atTop 1)).exists
  have hx : (input n).length ≤ 10*n^2 := by
    have h := short_input n
    have sq : n ≤ n^2 := by simpa [pow_two] using Nat.mul_le_mul_left n he
    nlinarith
  have hpos : 0 < (2:ℝ)^n := by positivity
  have hp : 0 < (C:ℝ)*10^d+1 := by positivity
  have hn' := (div_lt_div_iff₀ hpos hp).mp hn
  have hN : (C:ℝ)*10^d*(n:ℝ)^(2*d) < (2:ℝ)^n := by
    nlinarith [show 0 ≤ (n:ℝ)^(2*d) by positivity]
  have hnat : C*(10*n^2)^d < 2^n := by
    exact_mod_cast (by simpa [mul_pow, ← pow_mul, mul_assoc] using hN :
      ((C:ℝ)*(10*(n:ℝ)^2)^d < (2:ℝ)^n))
  exact ⟨n,lt_of_le_of_lt (Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hx d)) (lt_of_lt_of_le hnat (actual_rows n))⟩

end IALD.CustoDaTabela

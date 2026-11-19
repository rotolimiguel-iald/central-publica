import TGLExt.CaudaDisjunta
import TGLExt.OResumoEPsiBit

/-! Component evaluation from a supplied partition, with an executable test for
disjoint variable labels. The counter measures calls to the existing Horn
candidate checker. It does not charge partitioning, parsing or tape movement. -/
set_option autoImplicit false
namespace Codex.IndependentBlocks
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula TGLExt.OResumoEPsiBit IALD.LeitorDaFormula
open Codex.CrossSelectors Codex.HornCross Codex.CaudaDisjunta
variable {n : Nat}

private theorem passes_congr (p : CNF n) {x y : Fin n → Bool}
    (h : ∀ i ∈ varsDas p, x i = y i) : passes p x = passes p y := by
  apply Bool.eq_iff_iff.mpr
  simp only [passes,List.all_eq_true]
  apply forall_congr'
  intro c
  apply forall_congr'
  intro hc
  rw [satisfeita_so_ve_as_suas_variaveis c (fun i hi => h i (mem_varsDas_of_mem hc hi))]

theorem word_append (p q : CNF n) (h : Disjoint (varsDas p) (varsDas q)) :
    palavraDaFormula (p ++ q) = (palavraDaFormula p && palavraDaFormula q) := by
  apply Bool.eq_iff_iff.mpr
  simp only [Bool.and_eq_true,a_palavra_e_o_sat,sat_iff]
  constructor
  · rintro ⟨x,hx⟩
    have both : passes p x = true ∧ passes q x = true := by simpa [passes] using hx
    exact ⟨⟨x,both.1⟩,⟨x,both.2⟩⟩
  · rintro ⟨⟨x,hx⟩,⟨y,hy⟩⟩
    let z := fun i => if i ∈ varsDas p then x i else y i
    have hp : passes p z = true :=
      (passes_congr p (y := x) (fun i hi => by simp [z,hi])).trans hx
    have hq : passes q z = true := (passes_congr q (y := y) (fun i hi => by
      have hn : i ∉ varsDas p := fun hp => Finset.disjoint_left.mp h hp hi
      simp [z,hn])).trans hy
    exact ⟨z,by simpa only [passes,List.all_append,Bool.and_eq_true] using And.intro hp hq⟩

def separated : List (CNF n) → Bool
  | [] => true
  | p :: ps => decide (Disjoint (varsDas p) (varsDas ps.flatten)) && separated ps

def localRun (p : CNF n) := scan checkProgram (programs p)

/-- Run every supplied component, charging the visits actually made locally. -/
def readBlocks : List (CNF n) → Bool × Nat
  | [] => (true,0)
  | p :: ps =>
    let a := localRun p
    let b := readBlocks ps
    (a.1 && b.1, a.2+b.2)

theorem read_word (ps : List (CNF n)) (h : separated ps = true) :
    (readBlocks ps).1 = palavraDaFormula ps.flatten := by
  induction ps with
  | nil =>
    symm
    exact (a_palavra_e_o_sat _).mpr ((sat_iff _).mpr ⟨fun _ => false,rfl⟩)
  | cons p ps ih =>
    have hh : Disjoint (varsDas p) (varsDas ps.flatten) ∧ separated ps = true := by
      simpa [separated] using h
    change ((localRun p).1 && (readBlocks ps).1) = _
    rw [localRun,selector_word,ih hh.2,List.flatten_cons,word_append _ _ hh.1]

theorem actual_visits (ps : List (CNF n)) :
    (readBlocks ps).2 = (ps.map fun p => (localRun p).2).sum := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    simp only [List.map_cons,List.sum_cons]
    change (localRun p).2 + (readBlocks ps).2 = (localRun p).2 + _
    rw [ih]

private theorem scan_le {α : Type} (f : α → Bool) (xs : List α) :
    (scan f xs).2 ≤ xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs ih => cases hv : f a <;> simp [scan,hv]; omega

theorem additive_bound (ps : List (CNF n)) :
    (readBlocks ps).2 ≤ (ps.map fun p => (programs p).length).sum := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    exact Nat.add_le_add (scan_le checkProgram (programs p)) ih

private theorem count_append (p q : CNF n) :
    (programs (p++q)).length = (programs p).length * (programs q).length := by
  induction p with
  | nil => simp [programs]
  | cons c p ih =>
    rw [List.cons_append,selection_count,selection_count,ih,Nat.mul_assoc]

/-- Number of candidates available to whole-formula search. Its early stopping
rule can inspect fewer candidates. -/
theorem whole_candidates (ps : List (CNF n)) :
    (programs ps.flatten).length = (ps.map fun p => (programs p).length).prod := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    rw [List.flatten_cons,count_append,ih,List.map_cons,List.prod_cons]

def pairBlocks (m : Nat) := (List.finRange m).map (fun i => [pairClause i])

private theorem flatten_pairs {m : Nat} (is : List (Fin m)) :
    (is.map (fun i => [pairClause i])).flatten = is.map pairClause := by
  induction is with
  | nil => rfl
  | cons i is ih => simp [ih]

theorem pair_partition (m : Nat) : (pairBlocks m).flatten = disjointCNF m := by
  exact flatten_pairs _

private theorem pair_support {m : Nat} (is : List (Fin m)) (v : Fin (m+m))
    (hv : v ∈ varsDas (is.map pairClause)) : pairIndex v ∈ is := by
  induction is with
  | nil => simp [varsDas] at hv
  | cons i is ih =>
    change v ∈ varsClausula (pairClause i) ∪ varsDas (is.map pairClause) at hv
    rcases Finset.mem_union.mp hv with hc | ht
    · have eqs : v = left i ∨ v = right i := by simpa [varsClausula,pairClause] using hc
      rcases eqs with rfl | rfl
      · exact List.mem_cons.mpr (Or.inl (Fin.addCases_left i))
      · exact List.mem_cons.mpr (Or.inl (Fin.addCases_right i))
    · exact List.mem_cons_of_mem _ (ih ht)

theorem pair_partition_passes (m : Nat) : separated (pairBlocks m) = true := by
  suffices ∀ is : List (Fin m), is.Nodup → separated (is.map (fun i => [pairClause i])) = true by
    exact this _ (List.nodup_finRange m)
  intro is nd
  induction is with
  | nil => rfl
  | cons i is ih =>
    obtain ⟨avoid,tail⟩ := List.nodup_cons.mp nd
    have hd : Disjoint (varsDas [pairClause i]) (varsDas (is.map pairClause)) := by
      apply Finset.disjoint_left.mpr
      intro v hv ht
      have hi : pairIndex v = i := by simpa using pair_support [i] v hv
      exact avoid (hi ▸ pair_support is v ht)
    simp only [List.map_cons,separated,flatten_pairs,decide_eq_true_eq.mpr hd,Bool.true_and]
    exact ih tail

private theorem one_head (i : Fin n) : checkProgram [⟨[],some i⟩] = true := by
  rw [checkProgram,horn_word]
  apply (a_palavra_e_o_sat _).mpr
  exact (sat_iff _).mpr ⟨fun _ => true,by simp [passes,asClause,satisfeita,Literal.vale]⟩

private theorem one_pair {m : Nat} (i : Fin m) : localRun [pairClause i] = (true,1) := by
  change scan checkProgram [[⟨[],some (left i)⟩],[⟨[],some (right i)⟩]] = _
  simp [scan,one_head]

theorem pair_visits (m : Nat) : readBlocks (pairBlocks m) = (true,m) := by
  suffices ∀ is : List (Fin m),
      readBlocks (is.map (fun i => [pairClause i])) = (true,is.length) by
    simpa [pairBlocks] using this (List.finRange m)
  intro is
  induction is with
  | nil => rfl
  | cons i is ih =>
    simp only [List.map_cons,readBlocks,one_pair,ih,Bool.true_and,List.length_cons]
    congr 1; omega

theorem pair_whole_candidates (m : Nat) : (programs (disjointCNF m)).length = 2^m := by
  suffices ∀ is : List (Fin m), (programs (is.map pairClause)).length = 2^is.length by
    simpa [disjointCNF] using this (List.finRange m)
  intro is
  induction is with
  | nil => rfl
  | cons i is ih =>
    rw [List.map_cons,selection_count,ih,List.length_cons,pow_succ]
    change 2*2^is.length = 2^is.length*2
    omega

end Codex.IndependentBlocks

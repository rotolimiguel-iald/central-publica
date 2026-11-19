import TGLExt.OPsiBitDaFormula
import TGLExt.PontePalavraVerbo

/-! Leitor do Verbo para toda CNF esparsa. O índice i ocupa i marcas unárias,
seguidas do sinal, e há um delimitador de cláusula. A máquina tem controle
finito, entrada somente-leitura e duas pilhas de símbolos de quatro valores.
Uma transição só consulta/escreve um número constante de topos. -/
namespace IALD.VerbTape

open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula
open IALD.PontePalavraVerbo

inductive Symbol where | mark | positive | negative | close
  deriving DecidableEq, Repr

abbrev Mask := Bool × Bool

def blank : Mask := (false,false)
def side (m : Mask) (b : Bool) := if b then m.1 else m.2
def mark (m : Mask) (b : Bool) : Mask := if b then (true,m.2) else (m.1,true)
def test (r : List Mask) : Nat → Bool → Bool
  | 0, b => side (r.headD blank) b
  | i+1, b => test r.tail i b

def write (b : Bool) : Nat → List Mask → List Mask
  | 0, r => mark (r.headD blank) b :: r.tail
  | i+1, r => r.headD blank :: write b i r.tail

inductive Config where
  | read (active hit : Bool) (left right : List Mask) (input : List Symbol)
  | rewind (active hit : Bool) (left right : List Mask) (input : List Symbol)
  | erase (active : Bool) (right : List Mask) (input : List Symbol)
  | halted (active : Bool)

def consumeSign (active hit b : Bool) (left right : List Mask) (rest : List Symbol) : Config :=
  let m := right.headD blank
  .rewind active (hit || side m (!b)) left (mark m b :: right.tail) rest

def step : Config → Config
  | .read a h l r (.mark :: cs) => .read a h (r.headD blank :: l) r.tail cs
  | .read a h l r (.positive :: cs) => consumeSign a h true l r cs
  | .read a h l r (.negative :: cs) => consumeSign a h false l r cs
  | .read a h [] r (.close :: cs) => .erase (a || !h) r cs
  | .read a _ (_::_) _ (.close :: _) => .halted a
  | .read a _ _ _ [] => .halted a
  | .rewind a h (m :: l) r cs => .rewind a h l (m :: r) cs
  | .rewind a h [] r cs => .read a h [] r cs
  | .erase a (_ :: r) cs => .erase a r cs
  | .erase a [] cs => .read a false [] [] cs
  | .halted a => .halted a

def litLetters (i : Nat) (b : Bool) := List.replicate i Symbol.mark ++ [if b then .positive else .negative]
def letters {n} (c : Clausula n) := c.flatMap (fun l => litLetters l.var.val l.pos)
def tape {n} (f : CNF n) := f.flatMap (fun c => letters c ++ [.close])

private theorem rewind_exact (l r : List Mask) (cs : List Symbol) (a h : Bool) :
    step^[l.length+1] (.rewind a h l r cs) = .read a h [] (l.reverse ++ r) cs := by
  induction l generalizing r with
  | nil => rfl
  | cons m l ih =>
    change step^[l.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    simpa [step,List.reverse_cons,List.append_assoc] using ih (m :: r)

private theorem literal_exact (i : Nat) (b a h : Bool) (l r : List Mask) (cs : List Symbol) :
    step^[2*i + l.length+2] (.read a h l r (litLetters i b ++ cs)) =
      .read a (h || test r i (!b)) [] (l.reverse ++ write b i r) cs := by
  induction i generalizing l r with
  | zero =>
    rw [Nat.mul_zero,Nat.zero_add,show l.length+2=l.length+1+1 by omega]
    rw [Function.iterate_succ_apply]
    cases b <;> exact rewind_exact _ _ _ _ _
  | succ i ih =>
    have he : 2*(i+1)+l.length+2 = (2*i+(r.headD blank :: l).length+2)+1 := by simp; omega
    rw [he,Function.iterate_succ_apply]
    simpa [litLetters,List.replicate_succ,step,List.reverse_cons,write,test,List.append_assoc]
      using ih (r.headD blank :: l) r.tail

private theorem erase_exact (r : List Mask) (cs : List Symbol) (a : Bool) :
    step^[r.length+1] (.erase a r cs) = .read a false [] [] cs := by
  induction r with
  | nil => rfl
  | cons m r ih =>
    change step^[r.length+1+1] _ = _
    rw [Function.iterate_succ_apply]
    exact ih

def foldClause {n} (r : List Mask) (h : Bool) : Clausula n → List Mask × Bool
  | [] => (r,h)
  | l::ls => foldClause (write l.pos l.var.val r) (h || test r l.var.val (!l.pos)) ls

private theorem clause_exact {n} (c : Clausula n) (a h : Bool) (r : List Mask) (cs : List Symbol) :
    step^[2*(letters c).length] (.read a h [] r (letters c ++ cs)) =
      .read a (foldClause r h c).2 [] (foldClause r h c).1 cs := by
  induction c generalizing r h with
  | nil => rfl
  | cons l c ih =>
    change step^[2*(litLetters l.var.val l.pos ++ letters c).length] _ = _
    rw [List.length_append, Nat.mul_add, Nat.add_comm, Function.iterate_add_apply]
    have hl := literal_exact l.var.val l.pos a h [] r (letters c ++ cs)
    have hs : (litLetters l.var.val l.pos).length = l.var.val+1 := by simp [litLetters]
    rw [hs,Nat.mul_add,Nat.mul_one]
    simp only [List.length_nil,Nat.add_zero,List.reverse_nil,List.nil_append] at hl
    change step^[2*(letters c).length] (step^[2*l.var.val+2] (.read a h [] r
        ((litLetters l.var.val l.pos ++ letters c) ++ cs))) = _
    rw [List.append_assoc,hl]
    exact ih _ _

private theorem write_bound (b : Bool) (i : Nat) (r : List Mask) :
    (write b i r).length ≤ r.length+i+1 := by
  induction i generalizing r with
  | zero => cases r <;> simp [write]
  | succ i ih =>
    have ho := ih r.tail
    cases r <;> simp [write] at * <;> omega

private theorem memory_bound {n} (c : Clausula n) (r : List Mask) (h : Bool) :
    (foldClause r h c).1.length ≤ r.length+(letters c).length := by
  induction c generalizing r h with
  | nil => simp [foldClause,letters]
  | cons l c ih =>
    have hl := write_bound l.pos l.var.val r
    have hc := ih (write l.pos l.var.val r) (h || test r l.var.val (!l.pos))
    change (foldClause _ _ c).1.length ≤ r.length+(litLetters _ _ ++ letters c).length
    simp only [litLetters,List.length_append,List.length_replicate,List.length_singleton]
    omega

def Occ {n} (p : Clausula n) (i : Nat) (b : Bool) : Prop := ∃ l ∈ p, l.var.val=i ∧ l.pos=b
def clash {n} (p : Clausula n) : Prop := ∃ i, Occ p i true ∧ Occ p i false

private theorem occ_cons {n} (l : Literal n) (p : Clausula n) (i : Nat) (b : Bool) :
    Occ (l::p) i b ↔ (l.var.val=i ∧ l.pos=b) ∨ Occ p i b := by
  simp [Occ]

private theorem clash_cons {n} (l : Literal n) (p : Clausula n) :
    clash (l::p) ↔ clash p ∨ Occ p l.var.val (!l.pos) := by
  constructor
  · rintro ⟨i,ha,hb⟩
    rw [occ_cons] at ha hb
    rcases ha with ⟨hi,hpos⟩ | hp <;> rcases hb with ⟨hj,hneg⟩ | hn
    · simp_all
    · exact Or.inr (by simpa [hi,hpos] using hn)
    · exact Or.inr (by simpa [hj,hneg] using hp)
    · exact Or.inl ⟨i,hp,hn⟩
  · rintro (⟨i,hp,hn⟩ | h)
    · exact ⟨i,(occ_cons ..).mpr (Or.inr hp),(occ_cons ..).mpr (Or.inr hn)⟩
    · refine ⟨l.var.val,?_⟩
      rw [occ_cons,occ_cons]
      cases hb : l.pos
      · exact ⟨Or.inr (by simpa [hb] using h),Or.inl ⟨rfl,rfl⟩⟩
      · exact ⟨Or.inl ⟨rfl,rfl⟩,Or.inr (by simpa [hb] using h)⟩

private theorem write_spec (b : Bool) (i j : Nat) (r : List Mask) (v : Bool) :
    test (write b i r) j v = true ↔ (i=j ∧ b=v) ∨ test r j v = true := by
  induction i generalizing j r with
  | zero =>
    cases j with
    | zero => cases b <;> cases v <;> simp [write,test,side,mark]
    | succ j => simp [write,test]
  | succ i ih =>
    cases j with
    | zero => simp [write,test]
    | succ j => simpa [write,test] using ih j r.tail

private def Good {n} (p : Clausula n) (r : List Mask) (h : Bool) :=
  (∀ i b, test r i b = true ↔ Occ p i b) ∧ (h = true ↔ clash p)

private theorem good_cons {n} (p : Clausula n) (r : List Mask) (h : Bool)
    (H : Good p r h) (l : Literal n) :
    Good (l::p) (write l.pos l.var.val r) (h || test r l.var.val (!l.pos)) := by
  refine ⟨fun i b => ?_,?_⟩
  · rw [write_spec,occ_cons,H.1]
  · rw [Bool.or_eq_true,H.1,H.2,clash_cons]

private theorem good_fold {n} (p c : Clausula n) (r : List Mask) (h : Bool) (H : Good p r h) :
    Good (c.reverse ++ p) (foldClause r h c).1 (foldClause r h c).2 := by
  induction c generalizing p h r with
  | nil => simpa only [List.reverse_nil,List.nil_append,foldClause] using H
  | cons l c ih =>
    simpa only [List.reverse_cons,List.append_assoc,List.singleton_append,foldClause]
      using ih _ _ _ (good_cons p r h H l)

private theorem blank_flags (i : Nat) (b : Bool) : test [] i b = false := by
  induction i with
  | zero => cases b <;> rfl
  | succ i ih => exact ih

private theorem clash_pair {n} (c : Clausula n) : clash c ↔ oppositePair c = true := by
  simp only [clash,Occ,oppositePair,List.any_eq_true,Bool.and_eq_true,beq_iff_eq,bne_iff_ne]
  constructor
  · rintro ⟨i,⟨l,hl,hi,hp⟩,k,hk,hj,hq⟩
    exact ⟨l,hl,k,hk,Fin.ext (hj.trans hi.symm),by simp [hp,hq]⟩
  · rintro ⟨l,hl,k,hk,he,hn⟩
    have e : k.var.val=l.var.val := congrArg Fin.val he
    cases h : l.pos with
    | true => exact ⟨_,⟨l,hl,rfl,h⟩,k,hk,e,by cases g : k.pos <;> simp_all⟩
    | false => exact ⟨_,⟨k,hk,e,by cases g : k.pos <;> simp_all⟩,l,hl,rfl,h⟩

theorem clause_result {n} (c : Clausula n) :
    (foldClause [] false c).2 = oppositePair c := by
  apply Bool.eq_iff_iff.mpr
  have start : Good ([] : Clausula n) [] false := by simp [Good,Occ,clash,blank_flags]
  have H := (good_fold [] c [] false start).2
  simpa only [List.append_nil,clash,Occ,List.mem_reverse] using H.trans
    (by simpa [clash,Occ] using clash_pair c : clash (c.reverse ++ []) ↔ oppositePair c=true)

def ticks {n} (f : CNF n) : Nat := f.foldr
  (fun c k => 2*(letters c).length + ((foldClause [] false c).1.length+2) + k) 1

private theorem ticks_pos {n} (f : CNF n) : 1 ≤ ticks f := by
  induction f with
  | nil => exact Nat.le_refl 1
  | cons c f ih => change 1 ≤ _+_+ticks f; omega

theorem exact_run {n} (f : CNF n) (cs : List Symbol) (a : Bool) :
    step^[(ticks f)-1] (.read a false [] [] (tape f ++ cs)) =
      .read (a || !(quiet f)) false [] [] cs := by
  induction f generalizing a with
  | nil => simp [ticks,tape,quiet]
  | cons c f ih =>
    let r := (foldClause [] false c).1
    have ht := ticks_pos f
    have hn : ticks (c :: f)-1 = (ticks f-1)+(r.length+1+1)+2*(letters c).length := by
      change 2*(letters c).length + (r.length+2) + ticks f - 1 = _
      omega
    rw [hn,Function.iterate_add_apply]
    change (step^[ticks f-1+(r.length+1+1)]) (step^[2*(letters c).length]
      (.read a false [] [] ((letters c ++ [.close]) ++ tape f ++ cs))) = _
    rw [List.append_assoc,List.append_assoc]
    rw [clause_exact,Function.iterate_add_apply,Function.iterate_succ_apply]
    change (step^[ticks f-1]) ((step^[r.length+1]) (.erase (a || !(foldClause [] false c).2) r
      (tape f ++ cs))) = _
    rw [erase_exact,ih,clause_result,quiet_update]
    cases a <;> cases oppositePair c <;> cases quiet f <;> rfl

theorem linear_bound {n} (f : CNF n) : ticks f ≤ 3*(tape f).length+1 := by
  induction f with
  | nil => exact Nat.le_refl 1
  | cons c f ih =>
    have h := memory_bound c [] false
    change 2*(letters c).length + ((foldClause [] false c).1.length+2) + ticks f ≤
      3*((letters c ++ [Symbol.close]) ++ tape f).length+1
    simp only [List.length_append,List.length_singleton,List.length_nil,Nat.zero_add] at *
    omega

private theorem quiet_characterization {n} (f : CNF n) :
    quiet f = true ↔ ∀ x, custoCNF f x = 0 := by
  rw [quiet_spec f 0, TGLExt.OPsibitEACompressao.o_verbo_cala_sse_tudo_e_nome]

theorem bit_sign {n} (f : CNF n) (t : ℝ) :
    (if quiet f then (0 : SignType) else 1) = verboDaFormula f t := by
  have hnon := a_descida_nunca_e_negativa f t
  have hpos := a_descida_e_positiva_sse_ha_o_que_ler f t
  cases h : quiet f with
  | true =>
    have halt := (quiet_characterization f).mp h
    have hz : descida f t = 0 := by
      apply le_antisymm _ hnon
      apply le_of_not_gt
      rintro hg
      obtain ⟨x,hx⟩ := hpos.mp hg
      exact hx (halt x)
    simp [verboDaFormula,hz]
  | false =>
    have hn : ¬∀ x, custoCNF f x = 0 := by
      intro z; have := (quiet_characterization f).mpr z; simp_all
    push Not at hn
    exact (sign_pos (hpos.mpr hn)).symm

theorem universal_verb_tape {n} (f : CNF n) (t : ℝ) :
    ∃ k ≤ 3*(tape f).length+1, ∃ b,
      step^[k] (.read false false [] [] (tape f)) = .halted b ∧
      (if b then (1 : SignType) else 0) = verboDaFormula f t := by
  refine ⟨ticks f,linear_bound f,!quiet f,?_,?_⟩
  · have H := exact_run f [] false
    simp only [List.append_nil,Bool.false_or] at H
    have hp := ticks_pos f
    have e : ticks f = 1+(ticks f-1) := by omega
    conv_lhs => rw [e, Function.iterate_add_apply]
    rw [H]; rfl
  · cases h : quiet f <;> simpa [h] using bit_sign f t

end IALD.VerbTape

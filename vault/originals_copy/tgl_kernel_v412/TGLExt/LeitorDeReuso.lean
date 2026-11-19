import TGLExt.SegundaLeitura
import TGLExt.CustoDaBuscaLiteral

/-! A cache of obligations on each spoke, conditional on the one shared guard.
Two fixed hypotheses use separate initially blank work tapes and the same
rewound input. The final two bits always describe checked witnesses. -/
set_option autoImplicit false
namespace Codex.ReuseReader
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.SignProfile Codex.TwoSweeps Codex.SecondRead Codex.PolinomioPorEscolha
open Codex.LiteralSearchCost (delayed suffix choiceClause)

/-- Visit cell 1, pre-set the guard value, then home on the blank tape. -/
def prepare (h : Bool) : Bank × Nat :=
  (Function.update emptyBank 1 ⟨false,false,h,!h⟩,1+(home 1).2)

def record (cell : Cell) (v : Bool) : Cell := {cell with seenPos:=cell.seenPos || v}
theorem record_twice (cell : Cell) (v : Bool) : record (record cell v) v = record cell v := by
  cases cell; cases v <;> simp [record]

/-- A failed guard and a positive spoke record a positive requirement.
An already present requirement is a cache hit, proved by record_twice. -/
def collect (h : Bool) : Op (Option Bool) :=
  ⟨fun _ pos _ cell st => match st with
    | none => (cell,some pos)
    | some guard => (record cell ((guard != h) && pos),none),
   fun _ => none⟩

def filled (h : Bool) (w : List Letter) := scan (collect h) w (start (prepare h).1 none)
def again (h : Bool) (w : List Letter) : St Bits :=
  ⟨(filled h w).bank,beginBits,true,(home (filled h w).head).1⟩
def hypothesis (h : Bool) (w : List Letter) :=
  (scan evalOp (returned w).1 (again h w)).control.passed
def read (w : List Letter) : Bool × Bool :=
  let a := hypothesis false w
  let b := hypothesis true (returned w).1
  (a.1 || b.1,a.2 || b.2)
def hypCost (h : Bool) (w : List Letter) :=
  (prepare h).2 + travel (collect h) w (start (prepare h).1 none) +
    (home (filled h w).head).2 + (returned w).2 + travel evalOp (returned w).1 (again h w)
def movements (w : List Letter) := hypCost false w + (returned w).2 + hypCost true (returned w).1

private theorem one_cost (h : Bool) (w : List Letter) : hypCost h w ≤ 7*w.length+2 := by
  have a := cost_with_position (collect h) w (start (prepare h).1 none)
  have b := count_le evalOp w (again h w)
  change travel (collect h) w (start (prepare h).1 none) + (filled h w).head ≤ 3*w.length+0 at a
  have homeZero : (again h w).head=0 := by simp [again]
  rw [homeZero] at b
  unfold hypCost
  rw [returned_spec,home_trace]
  have two : (prepare h).2 = 2 := by simp [prepare]
  rw [two]
  dsimp only [Prod.fst,Prod.snd]
  omega

theorem linear_travel (w : List Letter) : movements w ≤ 15*w.length+4 := by
  unfold movements
  rw [returned_spec]
  have a := one_cost true w
  have b := one_cost false w
  dsimp only [Prod.fst,Prod.snd]
  omega

private theorem literalState {n : Nat} (l : Literal n) (u : Bool) (st : St Bits) :
    applyLit evalOp l u st =
    ⟨st.bank,readSign (l.var.val == 0) l.pos (st.bank l.var.val) st.control,false,0⟩ := by
  simp [applyLit,evalOp]

private theorem literalList {n : Nat} (ls : Clausula n) (st : St Bits) :
    (lits evalOp ls st).bank = st.bank ∧
    (lits evalOp ls st).control = ⟨st.control.passed,
      (st.control.clause.1 || satisfeita ls (bankValue st.bank false),
       st.control.clause.2 || satisfeita ls (bankValue st.bank true))⟩ := by
  induction ls generalizing st with
  | nil =>
    cases st with | mk t q f j => cases q; simp [lits,satisfeita]
  | cons l ls ih =>
    rw [lits,literalState]
    obtain ⟨t,q⟩ := ih ⟨st.bank,readSign (l.var.val == 0) l.pos (st.bank l.var.val) st.control,false,0⟩
    refine ⟨t,?_⟩
    rw [q]
    simp [readSign,satisfeita,Literal.vale,bankValue,Bool.or_assoc]

private theorem evalClauses {n : Nat} (p : CNF n) (st : St Bits)
    (fresh : st.control.clause = (false,false)) :
    (clauses evalOp p st).control.passed =
      (st.control.passed.1 && passes p (bankValue st.bank false),
       st.control.passed.2 && passes p (bankValue st.bank true)) := by
  induction p generalizing st with
  | nil => simp [clauses,passes]
  | cons c p ih =>
    rw [clauses,ih _ rfl]
    obtain ⟨t,q⟩ := literalList c st
    change ((endClause (lits evalOp c st).control).passed.1 &&
        passes p (bankValue (lits evalOp c st).bank false),
      (endClause (lits evalOp c st).control).passed.2 &&
        passes p (bankValue (lits evalOp c st).bank true)) = _
    rw [t,q]
    simp [endClause,fresh,passes,Bool.and_assoc]

def selected {n : Nat} (p : CNF n) (h b : Bool) : Fin n → Bool :=
  bankValue (filled h (original p)).bank b

theorem hyp_witness {n : Nat} (p : CNF n) (h b : Bool) :
    lane (hypothesis h (original p)) b = passes p (selected p h b) := by
  unfold hypothesis
  rw [returned_spec]
  have homeZero : (again h (original p)).head = 0 := by simp [again]
  rw [raw_clauses _ _ _ homeZero,evalClauses _ _ rfl]
  cases b <;> simp [lane,again,beginBits,selected]

theorem reuse_witnesses {n : Nat} (p : CNF n) (b : Bool) :
    lane (read (original p)) b =
      (passes p (selected p false b) || passes p (selected p true b)) := by
  unfold read
  rw [returned_spec]
  cases b with
  | false => exact congrArg₂ Bool.or (hyp_witness p false false) (hyp_witness p true false)
  | true => exact congrArg₂ Bool.or (hyp_witness p false true) (hyp_witness p true true)

theorem positive_sound {n : Nat} (p : CNF (n+1)) (b : Bool)
    (hit : lane (read (original p)) b = true) : present p b := by
  have deliver (h : Bool) (ok : passes p (selected p h b) = true) : present p b :=
    ⟨_,by simp [selected,bankValue,choose],ok⟩
  rw [reuse_witnesses] at hit
  exact (Bool.or_eq_true_iff.mp hit).elim (deliver false) (deliver true)

abbrev Edge (n : Nat) := Bool × Literal (n+2)
def guardLit {n : Nat} (g : Bool) : Literal (n+2) := ⟨1,g⟩
def edgeClause {n : Nat} (e : Edge n) : Clausula (n+2) := [guardLit e.1,e.2]
def star {n : Nat} (es : List (Edge n)) := es.map edgeClause
def requires {n : Nat} (e : Edge n) (h : Bool) (j : Nat) :=
    (e.1 != h) && e.2.pos && (e.2.var.val == j)
def votes {n : Nat} (es : List (Edge n)) (h : Bool) (j : Nat) :=
  es.any (fun e => requires e h j)

private theorem edge_step {n : Nat} (e : Edge n) (h : Bool) (st : St (Option Bool))
    (hs : st.control = none) (j : Nat) :
    (finish (collect h) (lits (collect h) (edgeClause e) st)).bank j =
      record (st.bank j) (requires e h j) := by
  by_cases eq : e.2.var.val = j
  · subst j
    simp [edgeClause,guardLit,lits,applyLit,finish,collect,hs,requires]
  · have back := Ne.symm eq
    have miss : (e.2.var.val == j) = false := beq_eq_false_iff_ne.mpr eq
    simp [edgeClause,lits,applyLit,finish,collect,hs,requires,miss,Function.update_of_ne back,record]

private theorem cache_accumulates {n : Nat} (es : List (Edge n)) (h : Bool)
    (st : St (Option Bool)) (hs : st.control=none) (j : Nat) :
    (clauses (collect h) (star es) st).bank j = record (st.bank j) (votes es h j) := by
  induction es generalizing st with
  | nil => cases s : st.bank j; simp [clauses,star,votes,record,s]
  | cons e es ih =>
    change (clauses (collect h) (star es) (finish (collect h) (lits (collect h) (edgeClause e) st))).bank j = _
    rw [ih _ rfl,edge_step _ _ _ hs]
    simp [votes,record,Bool.or_assoc]

theorem built_cache {n : Nat} (es : List (Edge n)) (h : Bool) (j : Nat) :
    (filled h (original (star es))).bank j = record ((prepare h).1 j) (votes es h j) := by
  unfold filled
  rw [raw_clauses _ _ _ rfl,cache_accumulates _ _ _ rfl]
  rfl

theorem selected_on_star {n : Nat} (es : List (Edge n)) (h b : Bool) (i : Fin (n+2)) :
    selected (star es) h b i =
      (if i.val = 0 then b else if i.val = 1 then h else votes es h i.val) := by
  simp only [selected,bankValue,choose,built_cache,beq_iff_eq]
  by_cases z : i.val = 0
  · simp [z]
  by_cases o : i.val = 1
  · cases h <;> simp [o,prepare,record,pick]
  · simp [z,o,prepare,emptyBank,blank,record,pick]

private theorem required_literal {n : Nat} {es : List (Edge n)} (x : Fin (n+2) → Bool)
    (ok : passes (star es) x = true) {e : Edge n} (mem : e ∈ es)
    (active : e.1 ≠ x 1) : x e.2.var = e.2.pos := by
  have ec : edgeClause e ∈ star es := List.mem_map.mpr ⟨e,mem,rfl⟩
  have hits := List.all_eq_true.mp ok _ ec
  simp [edgeClause,guardLit,satisfeita,Literal.vale,Ne.symm active] at hits
  exact hits

private theorem star_witness {n : Nat} (es : List (Edge n)) (b : Bool)
    (x : Fin (n+2) → Bool) (pivot : x 0 = b) (ok : passes (star es) x = true) :
    passes (star es) (selected (star es) (x 1) b) = true := by
  let h := x 1
  let y := selected (star es) h b
  have atGuard : y 1 = h := by simp [y,selected_on_star]
  apply List.all_eq_true.mpr
  intro c hc
  obtain ⟨e,mem,rfl⟩ := List.mem_map.mp hc
  change satisfeita (edgeClause e) y = true
  by_cases coveredByGuard : e.1 = h
  · simp [edgeClause,guardLit,satisfeita,Literal.vale,atGuard,coveredByGuard]
  have forced := required_literal x ok mem coveredByGuard
  have spoke : y e.2.var = e.2.pos := by
    rw [show y e.2.var = _ from selected_on_star es h b e.2.var]
    by_cases z : e.2.var.val=0
    · have iz : e.2.var=0 := Fin.ext z
      simpa [z,iz] using pivot.symm.trans (iz ▸ forced : x 0=e.2.pos)
    by_cases o : e.2.var.val=1
    · have io : e.2.var=1 := Fin.ext o
      simpa [z,o,h] using (io ▸ forced : x 1=e.2.pos)
    simp only [z,o,if_false]
    cases ep : e.2.pos with
    | true =>
      apply List.any_eq_true.mpr
      exact ⟨e,mem,by simp [requires,coveredByGuard,ep]⟩
    | false =>
      apply Bool.eq_false_iff.mpr
      intro has
      obtain ⟨other,hm,activepos⟩ := List.any_eq_true.mp has
      have obligations : (other.1 ≠ h ∧ other.2.pos=true) ∧ other.2.var.val=e.2.var.val := by
        simpa [requires] using activepos
      have otherForced := required_literal x ok hm obligations.1.1
      have eqv : other.2.var = e.2.var := Fin.ext obligations.2
      rw [eqv,obligations.1.2,forced,ep] at otherForced
      contradiction
  change satisfeita (edgeClause e) y = true
  simp [edgeClause,guardLit,satisfeita,Literal.vale,spoke]

theorem exact_stars {n : Nat} (es : List (Edge n)) (b : Bool) :
    lane (read (original (star es))) b = true ↔ present (star es) b := by
  refine ⟨positive_sound _ b,?_⟩
  rintro ⟨x,hx,ok⟩
  have witness := star_witness es b x hx ok
  rw [reuse_witnesses,Bool.or_eq_true]
  cases e : x 1
  · exact Or.inl (e ▸ witness)
  · exact Or.inr (e ▸ witness)

def delayedEdges : Nat → List (Edge 2)
  | 0 => [(false,⟨3,true⟩),(false,⟨3,false⟩)]
  | k+1 => (true,⟨2,true⟩)::delayedEdges k

theorem delayed_is_star (k : Nat) : delayed k = star (delayedEdges k) := by
  induction k with
  | zero => rfl
  | succ k ih => change choiceClause :: delayed k = choiceClause :: star (delayedEdges k); rw [ih]

theorem delayed_result (k : Nat) :
    read (original (delayed k)) = (true,true) ∧
    movements (original (delayed k)) ≤ 15*(6*k+14)+4 := by
  refine ⟨?_,?_⟩
  · have hit (b : Bool) := (exact_stars (delayedEdges k) b).mpr
        (delayed_is_star k ▸ LiteralSearchCost.every_branch_possible k b)
    rw [delayed_is_star]
    exact Prod.ext (hit false) (hit true)
  · simpa [LiteralSearchCost.delayed_letters] using linear_travel (original (delayed k))

theorem duplicate_cache {n : Nat} (e : Edge n) (es : List (Edge n)) (h : Bool) :
    (filled h (original (star (e::e::es)))).bank =
    (filled h (original (star (e::es)))).bank := by
  funext j
  simp only [built_cache,votes,List.any_cons]
  cases requires e h j <;> rfl

theorem star_word {n : Nat} (es : List (Edge n)) :
    let p := star es
    ((read (original p)).1 || (read (original p)).2) = palavraDaFormula p := by
  dsimp only
  apply Bool.eq_iff_iff.mpr
  rw [Bool.or_eq_true,word_from_pair]
  exact or_congr (exact_stars es false) (exact_stars es true)

example : read (original (star ([(true,⟨0,true⟩),(false,⟨0,true⟩)] : List (Edge 1)))) =
    (false,true) := by decide

def ticksIn : List Letter → Nat
  | [] => 0
  | .tick::w => ticksIn w + 1
  | .sign _::w => ticksIn w
  | .delimiter::w => ticksIn w

theorem travel_balance {Q : Type} (o : Op Q) (w : List Letter) (st : St Q) :
    travel o w st + (scan o w st).head = w.length + 2*ticksIn w + st.head := by
  induction w generalizing st with
  | nil => simp [travel,scan,ticksIn]
  | cons a w ih =>
    have h := ih (TwoSweeps.update o a w st)
    cases a <;> simp only [travel,scan,List.length_cons,ticksIn,workMoves,TwoSweeps.update,
      atSign,home_trace,Nat.mul_add,Nat.mul_one] at h ⊢ <;> omega

private theorem ends_home {Q : Type} (o : Op Q) (u : List Letter) (s : Bool) (st : St Q) :
    (scan o (u++[.sign s,.delimiter]) st).head = 0 := by
  induction u generalizing st with
  | nil => simp [scan,TwoSweeps.update,atSign,home_trace]
  | cons a u ih => exact ih (TwoSweeps.update o a (u++[.sign s,.delimiter]) st)

private theorem precise_hyp (h : Bool) (u : List Letter) (s : Bool) :
    let w := u++[.sign s,.delimiter]
    hypCost h w = 3*w.length + 4*ticksIn w + 2 := by
  let w := u++[.sign s,.delimiter]
  have a := travel_balance (collect h) w (start (prepare h).1 none)
  change travel (collect h) w (start (prepare h).1 none) + (filled h w).head = w.length+2*ticksIn w+0 at a
  have b := travel_balance evalOp w (again h w)
  have homeZero : (again h w).head = 0 := by simp [again]
  have after : (scan evalOp w (again h w)).head=0 := ends_home _ u s _
  rw [after,homeZero] at b
  change hypCost h w = _
  unfold hypCost
  rw [returned_spec,home_trace]
  have two : (prepare h).2 = 2 := by simp [prepare]
  rw [two]
  change 2 + travel (collect h) w (start (prepare h).1 none) + (filled h w).head +
    w.length + travel evalOp w (again h w) = 3*w.length + 4*ticksIn w+2
  omega

private theorem ending (k : Nat) : ∃ u : List Letter, original (delayed k) = u++[.sign false,.delimiter] := by
  induction k with
  | zero => exact ⟨(original (delayed 0)).take 12,rfl⟩
  | succ k ih =>
    obtain ⟨u,hu⟩ := ih
    refine ⟨spellClause choiceClause ++ u,?_⟩
    change spellClause choiceClause ++ original (delayed k) = _
    rw [hu,List.append_assoc]

private theorem ticks_append (u v : List Letter) : ticksIn (u++v) = ticksIn u+ticksIn v := by
  induction u with
  | nil => simp [ticksIn]
  | cons a u ih =>
    cases a <;> simp [ticksIn,ih]
    omega

private theorem delayed_ticks (k : Nat) : ticksIn (original (delayed k)) = 3*k+8 := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change ticksIn (spellClause choiceClause ++ original (delayed k)) = _
    rw [ticks_append,ih,show ticksIn (spellClause choiceClause)=3 from rfl]
    omega

theorem exact_delayed_moves (k : Nat) : movements (original (delayed k)) = 66*k+166 := by
  obtain ⟨u,hu⟩ := ending k
  have first := precise_hyp false u false
  have second := precise_hyp true u false
  dsimp only at first second
  rw [← hu] at first second
  unfold movements
  rw [returned_spec]
  change hypCost false (original (delayed k)) + (original (delayed k)).length +
      hypCost true (original (delayed k)) = _
  rw [first,second,LiteralSearchCost.delayed_letters,delayed_ticks]
  omega

end Codex.ReuseReader

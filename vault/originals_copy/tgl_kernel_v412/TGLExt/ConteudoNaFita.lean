import TGLExt.CadeiaNaFita

/-! A raw unary-CNF reader for two pivot stars. Clauses from the two stars
can be interleaved and target names can recur in any order. The reader
derives all signed obligations from literal signs for each pivot branch.
One pass per possible address trades time for keeping just its two flags.
The movement metric counts the original input head in both directions.
The independent unary ruler and the sweep counter are auxiliary storage. -/
set_option autoImplicit false
namespace Codex.NamedTape
open TGLExt.TraducaoTuring IALD.LeitorDaFormula Codex.PolinomioPorEscolha
open Codex.ChainTape (edge)

structure Tape where
  left : List Letter
  right : List Letter

def back : Tape → Tape
  | ⟨a::rest,w⟩ => ⟨rest,a::w⟩
  | t => t
def backMoves (t : Tape) : Nat := if t.left.isEmpty then 0 else 1

structure Visit (σ : Type) where
  value : σ
  tape : Tape
  moves : Nat

/-- Advance onto the right neighbour, run on that suffix, then move back
one square on the tape returned by the recursive call. The left list is
the reversed prefix in the mathematical representation of the head. -/
def roundTrip {σ : Type} (push : σ → Letter → σ) (s : σ)
    (l : List Letter) : List Letter → Visit σ
  | [] => ⟨s,⟨l,[]⟩,0⟩
  | a::w =>
    let r := roundTrip push (push s a) (a::l) w
    ⟨r.value,back r.tape,1+r.moves+backMoves r.tape⟩

theorem roundTrip_spec {σ : Type} (push : σ → Letter → σ) (s : σ) (l w : List Letter) :
    roundTrip push s l w = ⟨w.foldl push s,⟨l,w⟩,2*w.length⟩ := by
  induction w generalizing s l with
  | nil => rfl
  | cons a w ih =>
    simp only [roundTrip,ih,List.foldl_cons,List.length_cons]
    congr 1
    change 1 + 2*w.length + 1 = 2*(w.length+1)
    omega

structure Ruler where
  left : Nat
  pastEnd : Bool
  nonempty : Bool
  deriving DecidableEq

def atWidth (k t : Nat) : Ruler := ⟨k-t,decide (k<t),decide (0<t)⟩
def tick (r : Ruler) : Ruler := ⟨r.left-1,r.pastEnd || (r.left==0),true⟩
def nameMatch (r : Ruler) := (r.left==0) && !r.pastEnd

private theorem tick_width (k t : Nat) : tick (atWidth k t) = atWidth k (t+1) := by
  by_cases h : k ≤ t
  · have z : k-t=0 := by omega
    have less : k < t+1 := by omega
    simp [tick,atWidth,z,less,Nat.sub_eq_zero_of_le (show k ≤ t+1 by omega)]
  · have hz : k-t ≠ 0 := by omega
    have hn : ¬ k<t := by omega
    have hn' : ¬ k<t+1 := by omega
    have sub : k-t-1=k-(t+1) := by omega
    simp [tick,atWidth,hz,hn,hn',sub]

private theorem nameMatch_width (k t : Nat) : nameMatch (atWidth k t) = decide (t=k) := by
  by_cases h : t=k
  · simp [h,nameMatch,atWidth]
  · rcases Nat.lt_or_gt_of_ne h with lt | gt
    · have nz : k-t ≠ 0 := by omega
      simp [nameMatch,atWidth,h,nz]
    · simp [nameMatch,atWidth,h,gt]

abbrev Flags := Bool × Bool
def insert (s : Flags) (b : Bool) : Flags := if b then (s.1,true) else (true,s.2)
def marked (s : Flags) (b : Bool) := if b then s.2 else s.1

structure Reg where
  ruler : Ruler
  active : Option Bool
  flags : Flags

def clean (k : Nat) (flags : Flags) : Reg := ⟨atWidth k 0,none,flags⟩
def see (k : Nat) (u v : Bool) (s : Reg) : Letter → Reg
  | .tick => {s with ruler := tick s.ruler}
  | .delimiter => clean k s.flags
  | .sign b => match s.active with
    | none => ⟨atWidth k 0,some ((if s.ruler.nonempty then v else u) != b),s.flags⟩
    | some hot => clean k (if hot && nameMatch s.ruler then insert s.flags b else s.flags)

private theorem ticks (k : Nat) (u v : Bool) (hot : Option Bool) (flags : Flags) (t : Nat) :
    (List.replicate t Letter.tick).foldl (see k u v) ⟨atWidth k 0,hot,flags⟩ =
      ⟨atWidth k t,hot,flags⟩ := by
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [List.replicate_succ',List.foldl_append,ih]
    simp [see,tick_width]

structure Row (n : Nat) where
  secondPivot : Bool
  pivotSign : Bool
  name : Fin n
  sign : Bool
  deriving DecidableEq
variable {n : Nat}
def pivot (a b : Fin n) (r : Row n) := if r.secondPivot then b else a
def clause (a b : Fin n) (r : Row n) : Clausula n := edge (pivot a b r) r.name (r.pivotSign,r.sign)
def formula (a b : Fin n) (rows : List (Row n)) : CNF n := rows.map (clause a b)
def forced (u v : Bool) (r : Row n) := (if r.secondPivot then v else u) != r.pivotSign
def applyRow (k : Nat) (u v : Bool) (s : Flags) (r : Row n) : Flags :=
  if forced u v r && decide (r.name.val=k) then insert s r.sign else s

private theorem one_row (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (r : Row n)
    (k : Nat) (u v : Bool) (s : Flags) :
    (spellClause (clause a b r)).foldl (see k u v) (clean k s) =
      clean k (applyRow k u v s r) := by
  have p : decide (0<(pivot a b r).val) = r.secondPivot := by
    cases h : r.secondPivot <;> simp [pivot,h,ha,hb]
  simp only [clause,edge,spellClause,spell,List.flatMap_cons,List.flatMap_nil,List.append_nil,
    List.foldl_append,clean,ticks,see,List.foldl_cons,List.foldl_nil,nameMatch_width]
  change clean k (if (((if decide (0<(pivot a b r).val) then v else u) != r.pivotSign) &&
    decide (r.name.val=k)) then insert s r.sign else s) = _
  rw [p]; rfl

private theorem rows_read (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (rows : List (Row n))
    (k : Nat) (u v : Bool) (s : Flags) :
    (original (formula a b rows)).foldl (see k u v) (clean k s) =
      clean k (rows.foldl (applyRow k u v) s) := by
  induction rows generalizing s with
  | nil => rfl
  | cons r rs ih =>
    change ((spellClause (clause a b r)) ++ original (formula a b rs)).foldl _ _ = _
    rw [List.foldl_append,one_row a b ha hb,ih]; rfl

def Demand (rows : List (Row n)) (u v : Bool) (k : Nat) (s : Bool) : Prop :=
  ∃ r ∈ rows, forced u v r = true ∧ r.name.val = k ∧ r.sign = s

private theorem fold_mark (rows : List (Row n)) (u v : Bool) (k : Nat) (s : Flags) (h : Bool) :
    marked (rows.foldl (applyRow k u v) s) h = true ↔ marked s h = true ∨ Demand rows u v k h := by
  induction rows generalizing s with
  | nil => simp [Demand]
  | cons r rs ih =>
    rw [List.foldl_cons,ih]
    have one : marked (applyRow k u v s r) h = true ↔
        marked s h = true ∨ forced u v r = true ∧ r.name.val=k ∧ r.sign=h := by
      cases e : forced u v r <;> by_cases j : r.name.val=k <;>
        cases sig : r.sign <;> cases h <;> simp [applyRow,e,j,sig,insert,marked]
    rw [one]
    simp only [Demand,List.mem_cons]
    grind

def flags (w : List Letter) (u v : Bool) (k : Nat) :=
  (w.foldl (see k u v) (clean k (false,false))).flags
def consistent (s : Flags) := !(s.1 && s.2)

theorem demands_on_tape (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (rs : List (Row n))
    (u v : Bool) (k : Nat) (s : Bool) :
    marked (flags (original (formula a b rs)) u v k) s = true ↔ Demand rs u v k s := by
  unfold flags
  rw [rows_read a b ha hb]
  change marked (List.foldl _ _ _) _ = true ↔ _
  rw [fold_mark]
  cases s <;> simp [marked]

/-- All passes start from the tape returned by the preceding pass. -/
def survey (u v : Bool) (t : Tape) : Nat → Visit Bool
  | 0 =>
    let r := roundTrip (see 0 u v) (clean 0 (false,false)) t.left t.right
    ⟨consistent r.value.flags,r.tape,r.moves⟩
  | k+1 =>
    let r := roundTrip (see (k+1) u v) (clean (k+1) (false,false)) t.left t.right
    let rest := survey u v r.tape k
    ⟨consistent r.value.flags && rest.value,rest.tape,r.moves+rest.moves⟩

private theorem survey_spec (u v : Bool) (l w : List Letter) (k : Nat) :
    let r := survey u v ⟨l,w⟩ k
    (r.value=true ↔ ∀ j ≤ k, consistent (flags w u v j)=true) ∧
      r.tape=⟨l,w⟩ ∧ r.moves=2*w.length*(k+1) := by
  dsimp only
  induction k with
  | zero =>
    simp [survey,roundTrip_spec,flags]
  | succ k ih =>
    obtain ⟨ihv,iht,ihm⟩ := ih
    simp only [survey,roundTrip_spec,Bool.and_eq_true,iht,ihm,true_and,ihv]
    constructor
    · constructor
      · rintro ⟨hit,prev⟩ j hj
        rcases Nat.eq_or_lt_of_le hj with rfl|lt
        · exact hit
        · exact prev j (by omega)
      · intro h; exact ⟨h _ (by omega),fun j hj => h j (by omega)⟩
    · ring

def reader (u v : Bool) (w : List Letter) : Visit Bool :=
  let measured := roundTrip (fun x (_ : Letter) => x+1) 0 [] w
  let r := survey u v measured.tape measured.value
  ⟨r.value,r.tape,measured.moves+r.moves⟩

private theorem measure (s : Nat) (w : List Letter) :
    w.foldl (fun x (_ : Letter) => x+1) s = s+w.length := by
  induction w generalizing s with
  | nil => simp
  | cons a w ih => simp [ih]; omega

theorem head_moves (u v : Bool) (w : List Letter) :
    let r := reader u v w
    (r.value=true ↔ ∀ j ≤ w.length, consistent (flags w u v j)=true) ∧
      r.tape=⟨[],w⟩ ∧ r.moves=2*w.length*(w.length+2) := by
  simp only [reader,roundTrip_spec,measure,Nat.zero_add]
  obtain ⟨sem,pos,cost⟩ := survey_spec u v [] w w.length
  exact ⟨sem,pos,by rw [cost]; ring⟩

private theorem name_bound (a b : Fin n) (rs : List (Row n)) (r : Row n) (h : r∈rs) :
    r.name.val ≤ (original (formula a b rs)).length := by
  induction rs with
  | nil => simp at h
  | cons t ts ih =>
    change _ ≤ ((spellClause (clause a b t)) ++ original (formula a b ts)).length
    rw [List.length_append]
    rcases List.mem_cons.mp h with rfl|mem
    · simp [clause,edge,spellClause,spell]
      omega
    · have := ih mem; omega

private theorem evaluations (a b : Fin n) (rs : List (Row n)) (u v : Bool) (x : Fin n → Bool)
    (xa : x a=u) (xb : x b=v) :
    passes (formula a b rs) x=true ↔ ∀ r ∈ rs, forced u v r=true → x r.name=r.sign := by
  simp only [formula,passes,List.all_eq_true,List.forall_mem_map]
  apply forall_congr'; intro r
  apply forall_congr'; intro _
  cases h : r.secondPivot <;> cases s : r.pivotSign <;> cases u <;> cases v <;>
    simp [clause,edge,pivot,forced,satisfeita,Literal.vale,h,s,xa,xb]

theorem branch_exact (a b : Fin n) (ha : a.val=0) (hb : 0<b.val) (rs : List (Row n))
    (fresh : ∀ r ∈ rs, r.name ≠ a ∧ r.name ≠ b) (u v : Bool) :
    (reader u v (original (formula a b rs))).value=true ↔
      ∃ x : Fin n → Bool, x a=u ∧ x b=v ∧ passes (formula a b rs) x=true := by
  let w := original (formula a b rs)
  have good (k : Nat) : consistent (flags w u v k)=true ↔
      ¬ (Demand rs u v k false ∧ Demand rs u v k true) := by
    have nf := demands_on_tape a b ha hb rs u v k false
    have pf := demands_on_tape a b ha hb rs u v k true
    change (flags w u v k).1=true ↔ _ at nf
    change (flags w u v k).2=true ↔ _ at pf
    rw [←nf,←pf]
    cases e : flags w u v k with
    | mk neg pos => cases neg <;> cases pos <;> decide
  have distinct : a ≠ b := fun eq => by have := congrArg Fin.val eq; omega
  rw [(head_moves u v w).1]
  constructor
  · intro allGood
    let x (j : Fin n) := if j=a then u else if j=b then v else (flags w u v j.val).2
    have xa : x a=u := by simp [x]
    have xb : x b=v := by simp [x,Ne.symm distinct]
    refine ⟨x,xa,xb,(evaluations a b rs u v x xa xb).mpr ?_⟩
    intro r mem active
    have fr := fresh r mem
    simp only [x,if_neg fr.1,if_neg fr.2]
    have demand : Demand rs u v r.name.val r.sign := ⟨r,mem,active,rfl,rfl⟩
    cases sg : r.sign with
    | true => exact (demands_on_tape a b ha hb rs u v _ true).mpr (sg ▸ demand)
    | false =>
      have noPos := (good _).mp (allGood _ (name_bound a b rs r mem))
      have neg : Demand rs u v r.name.val false := sg ▸ demand
      have npos : ¬ (flags w u v r.name.val).2=true := fun p =>
        noPos ⟨neg,(demands_on_tape a b ha hb rs u v _ true).mp p⟩
      cases e : (flags w u v r.name.val).2 <;> simp_all
  · rintro ⟨x,xa,xb,pass⟩ k _
    apply (good _).mpr
    rintro ⟨⟨r,rm,ra,rk,rf⟩,⟨t,tm,ta,tk,tt⟩⟩
    have eq : r.name=t.name := Fin.ext (rk.trans tk.symm)
    have vr := (evaluations a b rs u v x xa xb).mp pass r rm ra
    have vt := (evaluations a b rs u v x xa xb).mp pass t tm ta
    simp_all

/-- Two clauses encode the prediction z = seed XOR flip. For seed=false
the first clause is active and for seed=true the second clause is active. -/
def predict (right : Bool) (z : Fin n) (flip : Bool) : List (Row n) :=
  [⟨right,true,z,flip⟩,⟨right,false,z,!flip⟩]

theorem prediction_semantics (a b z : Fin n) (side flip : Bool) (x : Fin n → Bool) :
    passes (formula a b (predict side z flip)) x = true ↔
      x z = Bool.xor (if side then x b else x a) flip := by
  rw [evaluations a b _ (x a) (x b) x rfl rfl]
  cases side <;> cases flip <;> cases x a <;> cases x b <;> simp [predict,forced]

theorem common_name_parity (a b z : Fin n) (l r : Bool) (x : Fin n → Bool)
    (h : passes (formula a b (predict false z l ++ predict true z r)) x = true) :
    Bool.xor (x a) (x b) = Bool.xor l r := by
  have both : passes (formula a b (predict false z l)) x = true ∧
      passes (formula a b (predict true z r)) x = true := by simpa [formula,passes] using h
  have lhs := (prediction_semantics a b z false l x).mp both.1
  have rhs := (prediction_semantics a b z true r x).mp both.2
  cases h₁ : x a <;> cases h₂ : x b <;> cases l <;> cases r <;> simp_all

private def sample (change : Bool) : List (Row 4) :=
  predict false 2 false ++ predict false 3 true ++
  predict true 3 (!change) ++ predict true 2 false

theorem two_names_control :
    let p := fun c => original (formula (0:Fin 4) 1 (sample c))
    let tbl := fun c => ((reader false false (p c)).value, (reader false true (p c)).value,
      (reader true false (p c)).value, (reader true true (p c)).value)
    (tbl false, tbl true) = ((true,false,false,true),(false,false,false,false)) := by decide

end Codex.NamedTape

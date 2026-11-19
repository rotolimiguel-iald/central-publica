import TGLExt.LeituraDosPares

/-! A finite-control transducer for paths of binary factors on the original
unary CNF tape. Several clauses can constrain the same edge. The parity of
the first address separates consecutive edge groups without adding markers. -/
set_option autoImplicit false
namespace Codex.ChainTape
open TGLExt.TraducaoTuring TGLExt.OPsiBitDaFormula IALD.LeitorDaFormula
open Codex.PolinomioPorEscolha

abbrev Row := Bool × Bool
abbrev Table := Row × Row
def select {α : Type} (p : α × α) (b : Bool) := if b then p.2 else p.1
def getBit (r : Table) (u v : Bool) := select (select r u) v
def tab (f : Bool → Bool → Bool) : Table :=
  ((f false false, f false true), (f true false, f true true))

@[simp] theorem get_tab (f : Bool → Bool → Bool) (u v : Bool) :
    getBit (tab f) u v = f u v := by cases u <;> cases v <;> rfl

def idTable := tab (fun u v => u == v)
def clauseTable (signs : Row) := tab (fun u v => (u == signs.1) || (v == signs.2))
def both (r t : Table) := tab (fun u v => getBit r u v && getBit t u v)
def join (r t : Table) := tab (fun u v =>
  (getBit r u false && getBit t false v) || (getBit r u true && getBit t true v))

theorem join_exact (r t : Table) (u v : Bool) :
    getBit (join r t) u v = true ↔ ∃ z : Bool, getBit r u z = true ∧ getBit t z v = true := by
  simp only [join,get_tab,Bool.or_eq_true,Bool.and_eq_true]
  constructor
  · rintro (h|h)
    · exact ⟨false,h⟩
    · exact ⟨true,h⟩
  · rintro ⟨z,h⟩
    cases z with
    | false => exact Or.inl h
    | true => exact Or.inr h

def parity : Nat → Bool
  | 0 => false
  | j+1 => !(parity j)

structure Acc where
  saved : Table
  active : Option (Bool × Table)
deriving Repr, DecidableEq

def committed (s : Acc) := match s.active with
  | none => s.saved
  | some (_,r) => join s.saved r

def collect (s : Acc) (key : Bool) (e : Table) : Acc :=
  match s.active with
  | none => ⟨s.saved,some (key,e)⟩
  | some (old,r) =>
    if old == key then ⟨s.saved,some (key,both r e)⟩
    else ⟨join s.saved r,some (key,e)⟩

def ready (s : Acc) (key : Bool) : Prop :=
  ∀ d r, s.active = some (d,r) → d ≠ key

private theorem start_group (s : Acc) (key : Bool) (e : Table) (h : ready s key) :
    collect s key e = ⟨committed s,some (key,e)⟩ := by
  cases a : s.active with
  | none => simp [collect,committed,a]
  | some z =>
    obtain ⟨d,r⟩ := z
    simp [collect,committed,a,h d r a]

structure Reg where
  acc : Acc
  odd : Bool
  first : Option (Bool × Bool)
deriving Repr, DecidableEq

def clean (s : Acc) : Reg := ⟨s,false,none⟩
def freshKey : Acc := ⟨idTable,none⟩
def restrictTo (r : Table) (b : Bool) := tab (fun u v => getBit r u v && (v == b))
def see (s : Reg) : Letter → Reg
  | .tick => {s with odd := !s.odd}
  | .sign b => match s.first with
    | none => ⟨s.acc,false,some (s.odd,b)⟩
    | some (key,a) => clean (collect s.acc key (clauseTable (a,b)))
  | .delimiter => match s.first with
    | none => clean s.acc
    | some (_,b) => clean ⟨restrictTo (committed s.acc) b,none⟩

def finalBits (s : Reg) : Row := (fun r => (getBit r false false || getBit r false true,
    getBit r true false || getBit r true true)) (committed s.acc)
def reader (w : List Letter) := finalBits (w.foldl see (clean freshKey))

private theorem ticks (k : Nat) (a : Acc) (first : Option Row) :
    (List.replicate k Letter.tick).foldl see ⟨a,false,first⟩ = ⟨a,parity k,first⟩ := by
  induction k with
  | zero => rfl
  | succ k ih => rw [List.replicate_succ',List.foldl_append,ih]; rfl

variable {n : Nat}
def edge (l r : Fin n) (s : Row) : Clausula n := [⟨l,s.1⟩,⟨r,s.2⟩]
def group (l r : Fin n) (sg : List Row) := sg.map (edge l r)
def unit (i : Fin n) (b : Bool) : CNF n := [[⟨i,b⟩]]

private theorem decode_edge (a : Acc) (l r : Fin n) (s : Row) :
    (spellClause (edge l r s)).foldl see (clean a) =
      clean (collect a (parity l.val) (clauseTable s)) := by
  obtain ⟨u,v⟩ := s
  simp [edge,spellClause,spell,List.foldl_append,clean,ticks,see]

private theorem decode_unit (a : Acc) (i : Fin n) (b : Bool) :
    (original (unit i b)).foldl see (clean a) = clean ⟨restrictTo (committed a) b,none⟩ := by
  simp [unit,original,spellClause,spell,List.foldl_append,clean,ticks,see]

def merged (r : Table) (sg : List Row) := sg.foldl (fun t s => both t (clauseTable s)) r

private theorem decode_rest (l r : Fin n) (sg : List Row) (pref cur : Table) :
    (original (group l r sg)).foldl see (clean ⟨pref,some (parity l.val,cur)⟩) =
      clean ⟨pref,some (parity l.val,merged cur sg)⟩ := by
  induction sg generalizing cur with
  | nil => rfl
  | cons e sg ih =>
    change ((spellClause (edge l r e)) ++ original (group l r sg)).foldl see _ = _
    rw [List.foldl_append,decode_edge]
    simpa [collect,merged] using ih (both cur (clauseTable e))

private theorem decode_group (a : Acc) (l r : Fin n) (e : Row) (es : List Row)
    (h : ready a (parity l.val)) :
    (original (group l r (e::es))).foldl see (clean a) =
      clean ⟨committed a,some (parity l.val,merged (clauseTable e) es)⟩ := by
  change (spellClause (edge l r e) ++ original (group l r es)).foldl see _ = _
  rw [List.foldl_append,decode_edge,start_group _ _ _ h,decode_rest]

private theorem merged_ok (a : Table) (es : List Row) (u v : Bool) :
    getBit (merged a es) u v = true ↔ getBit a u v = true ∧
      ∀ e ∈ es, (u == e.1 || v == e.2) = true := by
  induction es generalizing a with
  | nil => simp [merged]
  | cons e es ih =>
    change getBit (merged (both a (clauseTable e)) es) u v = true ↔ _
    rw [ih]
    simp [both,clauseTable,and_assoc]

private theorem group_ok (l r : Fin n) (e : Row) (es : List Row) (x : Fin n → Bool) :
    getBit (merged (clauseTable e) es) (x l) (x r) = true ↔
      passes (group l r (e::es)) x = true := by
  rw [merged_ok]
  simp [group,passes,edge,satisfeita,Literal.vale,clauseTable]

/-- Each new endpoint is fresh. Previous clauses can contain all older
endpoints. Alternating parity distinguishes adjacent edge groups. -/
inductive Path (pivot : Fin n) : CNF n → Fin n → Prop where
  | start : Path pivot [] pivot
  | extend {p : CNF n} {l : Fin n} (old : Path pivot p l) (r : Fin n)
      (par : parity l.val ≠ parity r.val) (newPivot : r ≠ pivot)
      (unused : ∀ c ∈ p, ∀ t ∈ c, t.var ≠ r) (e : Row) (es : List Row) :
      Path pivot (p ++ group l r (e::es)) r

private theorem keep_old (p : CNF n) (r : Fin n) (z : Bool) (x : Fin n → Bool)
    (unused : ∀ c ∈ p, ∀ t ∈ c, t.var ≠ r) (h : passes p x = true) :
    passes p (Function.update x r z) = true := by
  apply List.all_eq_true.mpr
  intro c hc
  obtain ⟨t,ht,hit⟩ := List.any_eq_true.mp (List.all_eq_true.mp h c hc)
  exact List.any_eq_true.mpr ⟨t,ht,by simpa [Literal.vale,Function.update_of_ne (unused c hc t ht)] using hit⟩

def visible (p : CNF n) (pivot last : Fin n) (u v : Bool) : Prop :=
  ∃ x, x pivot=u ∧ x last=v ∧ passes p x = true

theorem path_table {pivot last : Fin n} {p : CNF n} (h : Path pivot p last) :
    ∃ a : Acc, (original p).foldl see (clean freshKey) = clean a ∧ ready a (parity last.val) ∧
      ∀ u v, getBit (committed a) u v = true ↔ visible p pivot last u v := by
  induction h with
  | start =>
    refine ⟨freshKey,rfl,?_,?_⟩
    · simp [ready,freshKey]
    · intro u v
      simp only [freshKey,committed,idTable,get_tab,beq_iff_eq]
      constructor
      · rintro rfl; exact ⟨fun _ => u,rfl,rfl,rfl⟩
      · rintro ⟨x,hx,hv,_⟩; exact hx.symm.trans hv
  | @extend p l old r par newPivot unused e es ih =>
    obtain ⟨a,scan,canAdd,spec⟩ := ih
    let factor := merged (clauseTable e) es
    refine ⟨⟨committed a,some (parity l.val,factor)⟩,?_,?_,?_⟩
    · change ((p ++ group l r (e::es)).flatMap spellClause).foldl see _ = _
      rw [List.flatMap_append,List.foldl_append]
      exact (congrArg (fun s => (original (group l r (e::es))).foldl see s) scan).trans
        (decode_group a l r e es canAdd)
    · intro k t he
      have : k = parity l.val := (Prod.ext_iff.mp (Option.some.inj he)).1.symm
      simpa [this] using par
    · intro u v
      change getBit (join (committed a) factor) u v = true ↔ _
      rw [join_exact]
      constructor
      · rintro ⟨z,hz,hit⟩
        obtain ⟨x,xb,xz,ok⟩ := (spec u z).mp hz
        let y := Function.update x r v
        have yl : y l = z := by
          have ne : l ≠ r := fun eq => par (congrArg (fun j : Fin n => parity j.val) eq)
          simpa [y,Function.update_of_ne ne] using xz
        have yr : y r = v := by simp [y]
        refine ⟨y,by simpa [y,Function.update_of_ne (Ne.symm newPivot)] using xb,yr,?_⟩
        have tail : passes (group l r (e::es)) y = true :=
          (group_ok l r e es y).mp (by simpa only [yl,yr] using hit)
        simpa [passes] using And.intro (keep_old p r v x unused ok) tail
      · rintro ⟨x,hx,hv,ok⟩
        have split : passes p x = true ∧ passes (group l r (e::es)) x = true := by
          simpa [passes] using ok
        exact ⟨x l,(spec u _).mpr ⟨x,hx,rfl,split.1⟩,
          by simpa only [hv] using (group_ok l r e es x).mpr split.2⟩

inductive Machine where
  | walk (reg : Reg) (unread : List Letter)
  | halt (out : Row)
def step : Machine → Machine
  | .walk r (t::w) => .walk (see r t) w
  | .walk r [] => .halt (finalBits r)
  | .halt out => .halt out
def moved : Machine → Nat
  | .walk _ (_::_) => 1
  | _ => 0
def travel : Nat → Machine → Nat
  | 0,_ => 0
  | k+1,s => moved s + travel k (step s)
theorem one_head (w : List Letter) (s : Reg) :
    step^[w.length+1] (.walk s w) = .halt (finalBits (w.foldl see s)) ∧
    travel (w.length+1) (.walk s w) = w.length := by
  induction w generalizing s with
  | nil => exact ⟨rfl,rfl⟩
  | cons t w ih =>
    obtain ⟨done,moves⟩ := ih (see s t)
    constructor
    · change step^[w.length+1+1] _ = _
      rw [Function.iterate_succ_apply]; exact done
    · change 1 + travel (w.length+1) (.walk (see s t) w) = w.length+1
      omega

private theorem end_bits (a : Acc) (u : Bool) :
    select (finalBits (clean a)) u = true ↔ ∃ v : Bool, getBit (committed a) u v = true := by
  have simple : select (finalBits (clean a)) u =
      (getBit (committed a) u false || getBit (committed a) u true) := by cases u <;> rfl
  rw [simple,Bool.or_eq_true]
  constructor
  · rintro (h|h)
    · exact ⟨false,h⟩
    · exact ⟨true,h⟩
  · rintro ⟨z,h⟩
    cases z with
    | false => exact Or.inl h
    | true => exact Or.inr h

theorem unconstrained {pivot last : Fin n} {p : CNF n} (h : Path pivot p last) (u : Bool) :
    select (reader (original p)) u = true ↔ ∃ x, x pivot = u ∧ passes p x = true := by
  obtain ⟨a,scan,_,spec⟩ := path_table h
  rw [reader,scan,end_bits]
  constructor
  · rintro ⟨v,hit⟩
    obtain ⟨x,hu,_,ok⟩ := (spec u v).mp hit
    exact ⟨x,hu,ok⟩
  · rintro ⟨x,hu,ok⟩
    exact ⟨x last,(spec _ _).mpr ⟨x,hu,rfl,ok⟩⟩

theorem with_unit {pivot last : Fin n} {p : CNF n} (h : Path pivot p last) (u b : Bool) :
    select (reader (original (p ++ unit last b))) u = true ↔
      ∃ x, x pivot = u ∧ passes (p ++ unit last b) x = true := by
  obtain ⟨a,scan,_,spec⟩ := path_table h
  have split : original (p ++ unit last b) = original p ++ original (unit last b) := by simp [original]
  rw [split,reader,List.foldl_append,scan,decode_unit,end_bits]
  constructor
  · rintro ⟨v,hit⟩
    have eq : getBit (committed a) u v = true ∧ v=b := by simpa [committed,restrictTo] using hit
    obtain ⟨x,hu,hv,ok⟩ := (spec u v).mp eq.1
    exact ⟨x,hu,by simpa [passes,unit,satisfeita,Literal.vale] using And.intro ok (hv.trans eq.2)⟩
  · rintro ⟨x,hu,ok⟩
    have eq : passes p x = true ∧ x last=b := by
      simpa [passes,unit,satisfeita,Literal.vale] using ok
    refine ⟨b,?_⟩
    have hit := (spec u b).mpr ⟨x,hu,eq.2,eq.1⟩
    simpa [committed,restrictTo] using hit

theorem raw_path {pivot last : Fin n} {p : CNF n} (h : Path pivot p last) (b : Bool)
    (w : List Letter) (promise : w = original (p ++ unit last b)) :
    step^[w.length+1] (.walk (clean freshKey) w) = .halt (reader w) ∧
    travel (w.length+1) (.walk (clean freshKey) w) = w.length ∧
    ∀ u, select (reader w) u = true ↔ ∃ x, x pivot = u ∧ passes (p ++ unit last b) x = true := by
  obtain ⟨ends,moves⟩ := one_head w (clean freshKey)
  exact ⟨ends,moves,by rw [promise]; exact fun u => with_unit h u b⟩

/-- Ordinary chains of any length embed into the promise over their actual
integer addresses. Each edge supplies a nonempty list of binary clauses. -/
def ladder {n : Nat} (signs : Nat → Row × List Row) : (m : Nat) → m < n → CNF n
  | 0,_ => []
  | k+1,h =>
    let h' : k < n := Nat.lt_of_succ_lt h
    ladder signs k h' ++ group ⟨k,h'⟩ ⟨k+1,h⟩ ((signs k).1 :: (signs k).2)

private theorem old_address {n} (signs : Nat → Row × List Row) (m : Nat) (h : m < n) :
    ∀ c ∈ ladder signs m h, ∀ t ∈ c, t.var.val ≤ m := by
  induction m with
  | zero => simp [ladder]
  | succ k ih =>
    intro c hc t ht
    change c ∈ ladder signs k _ ++ group _ _ _ at hc
    rcases List.mem_append.mp hc with old | here
    · exact Nat.le_succ_of_le (ih (by omega) c old t ht)
    · obtain ⟨e,_,rfl⟩ := List.mem_map.mp here
      rcases List.mem_cons.mp ht with rfl | ht
      · exact Nat.le_succ _
      · rcases List.mem_cons.mp ht with rfl | impossible
        · exact Nat.le_refl _
        · cases impossible

theorem ladder_path {n : Nat} (signs : Nat → Row × List Row) (m : Nat) (h : m < n) :
    Path (⟨0,by omega⟩ : Fin n) (ladder signs m h) ⟨m,h⟩ := by
  induction m with
  | zero => exact Path.start
  | succ k ih =>
    apply Path.extend (ih (by omega))
    · change parity k ≠ !(parity k)
      cases parity k <;> decide
    · intro eq
      have bad := congrArg Fin.val eq
      simp at bad
    · intro c hc t ht eq
      have le := old_address signs k (by omega) c hc t ht
      rw [eq] at le
      exact Nat.not_succ_le_self k le


private def exampleEdge (i : Nat) : Row × List Row :=
  if i=0 then ((false,true),[(true,false)]) else ((true,true),[(false,false)])

/-- Equality followed by disequality and a terminal positive literal forces the initial bit false. -/
theorem crossed_example :
    let p := ladder (n:=3) exampleEdge 2 (by decide) ++ unit (2 : Fin 3) true
    (reader (original p),(original p).length) = ((true,false),24) := by decide

end Codex.ChainTape

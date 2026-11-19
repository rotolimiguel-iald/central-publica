import TGLExt.LeitorDaFormula

/-! A finite wire code for relational composition over one shared live bit.
The transmitted signs are executable. Angular representatives are a separate
realization theorem over the canonical PsiBit orbit. -/
set_option autoImplicit false
namespace Codex.OrthantRelation

open TGLExt.TraducaoTuring IALD.LeitorDaFormula TGLExt.Psibit

/-- The coordinates give the signs for the false and true continuations. -/
abbrev Symbol := Bool × Bool
abbrev Key := Symbol × Symbol
abbrev Relation := Bool → Bool → Bool

def readRow (s : Symbol) (b : Bool) := if b then s.2 else s.1
def atBit (k : Key) (a b : Bool) := readRow (if a then k.2 else k.1) b
def encode (r : Relation) : Key :=
  ((r false false,r false true),(r true false,r true true))

theorem exact_coordinate (r : Relation) (a b : Bool) : atBit (encode r) a b = r a b := by
  cases a <;> cases b <;> rfl

theorem exact_key (k : Key) : encode (atBit k) = k := by
  rcases k with ⟨⟨_,_⟩,⟨_,_⟩⟩
  rfl

/-- One fixed representative per orthant. The tape carries two bits selecting it. -/
noncomputable def angle : Symbol → ℝ
  | (false,false) => Real.pi - Real.pi / 4
  | (false,true) => Real.pi / 4 + Real.pi
  | (true,false) => Real.pi / 4
  | (true,true) => -(Real.pi / 4)

noncomputable def coord (b : Bool) : ℝ :=
  if b then Real.sqrt 2 / 2 else -(Real.sqrt 2 / 2)

theorem signal (s : Symbol) : v (angle s) = (coord s.1,coord s.2) := by
  rcases s with ⟨a,b⟩
  cases a <;> cases b
  · exact v_pi_sub_pi_div_four
  · exact v_pi_div_four_add_pi
  · exact v_pi_div_four
  · exact v_neg_pi_div_four

private theorem sign_margin (b : Bool) (z : ℝ)
    (close : |z-coord b| < Real.sqrt 2 / 2) : SignType.sign z = bitSign b := by
  obtain ⟨lo,hi⟩ := abs_lt.mp close
  cases b
  · apply _root_.sign_neg
    change z - -(Real.sqrt 2 / 2) < Real.sqrt 2 / 2 at hi
    linarith
  · apply _root_.sign_pos
    change -(Real.sqrt 2 / 2) < z - Real.sqrt 2 / 2 at lo
    linarith

/-- An absolute error strictly smaller than the margin in each received
coordinate preserves both signs. This is a mathematical channel hypothesis. -/
theorem robust_read (s : Symbol) (received : ℝ × ℝ)
    (e₀ : |received.1 - (v (angle s)).1| < Real.sqrt 2 / 2)
    (e₁ : |received.2 - (v (angle s)).2| < Real.sqrt 2 / 2) :
    SignType.sign received.1 = bitSign s.1 ∧ SignType.sign received.2 = bitSign s.2 := by
  rw [signal] at e₀ e₁
  exact ⟨sign_margin _ _ e₀,sign_margin _ _ e₁⟩

/-- These concrete representatives are canonical PsiBit amplitudes. -/
theorem exact_representative (s : Symbol) :
    (codeAmp (angle s)).word = bitSign s.1 ∧ (codeAmp (angle s)).verb = bitSign s.2 := by
  apply robust_read s (v (angle s))
  · simpa only [sub_self, abs_zero] using sqrt_two_div_two_pos
  · simpa only [sub_self, abs_zero] using sqrt_two_div_two_pos

/-- A single 16-position ring is another digital carrier for the same four bits. -/
def phaseTag (k : Key) : Fin 16 :=
  Fin.ofNat 16 ((if k.1.1 then 8 else 0) + (if k.1.2 then 4 else 0) +
    (if k.2.1 then 2 else 0) + (if k.2.2 then 1 else 0))

def fromPhase (t : Fin 16) : Key :=
  ((t.val.testBit 3,t.val.testBit 2),(t.val.testBit 1,t.val.testBit 0))

theorem phase_roundtrip (k : Key) : fromPhase (phaseTag k) = k := by
  rcases k with ⟨⟨a,b⟩,⟨c,d⟩⟩
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem all_phase_tags (t : Fin 16) : phaseTag (fromPhase t) = t := by
  fin_cases t <;> decide

def turn (t : Fin 16) : ℚ := (t.val : ℚ)/16

/-- If a measured rational turn is within 1/32 revolution of a tag, any two
compatible tags coincide. Arbitrary integer winding offsets are allowed. -/
theorem robust_sector (measured : ℚ) (u v : Fin 16) (i j : ℤ)
    (hu : |measured - (turn u + i)| < 1/32)
    (hv : |measured - (turn v + j)| < 1/32) : u = v := by
  obtain ⟨h₁,h₂⟩ := abs_lt.mp hu
  obtain ⟨h₃,h₄⟩ := abs_lt.mp hv
  unfold turn at h₁ h₂ h₃ h₄
  have lb : ((u.val : ℤ) + 16*i) - ((v.val : ℤ) + 16*j) > -1 := by
    exact_mod_cast (show (u.val : ℚ) + 16*(i : ℚ) - ((v.val : ℚ) + 16*(j : ℚ)) > -1 by linarith)
  have ub : ((u.val : ℤ) + 16*i) - ((v.val : ℤ) + 16*j) < 1 := by
    exact_mod_cast (show (u.val : ℚ) + 16*(i : ℚ) - ((v.val : ℚ) + 16*(j : ℚ)) < 1 by linarith)
  apply Fin.ext
  have hu' := u.isLt
  have hv' := v.isLt
  omega

def supported (k : Key) (s : Bool) := ∃ t, atBit k s t = true

/-- Two fixed-wire-input gates per middle value; no search over earlier assignments. -/
def join (left right : Key) : Key := encode (fun a c =>
  (atBit left a false && atBit right false c) || (atBit left a true && atBit right true c))

theorem join_iff (left right : Key) (a c : Bool) :
    atBit (join left right) a c = true ↔ ∃ b, atBit left a b = true ∧ atBit right b c = true := by
  simp only [join,exact_coordinate,Bool.or_eq_true,Bool.and_eq_true]
  constructor
  · rintro (h|h)
    · exact ⟨false,h⟩
    · exact ⟨true,h⟩
  · rintro ⟨b,h⟩
    cases b
    · exact Or.inl h
    · exact Or.inr h

def endToEnd : List Key → Bool → Bool → Prop
  | [], a,c => a=c
  | k::ks,a,c => ∃ b, atBit k a b = true ∧ endToEnd ks b c

theorem path_iff (ks : List Key) (initial : Key) (a c : Bool) :
    atBit (ks.foldl join initial) a c = true ↔ ∃ b, atBit initial a b = true ∧ endToEnd ks b c := by
  induction ks generalizing initial with
  | nil => simp [endToEnd]
  | cons k ks ih =>
    rw [List.foldl_cons,ih]
    constructor
    · rintro ⟨v,h,tail⟩
      obtain ⟨b,first,second⟩ := (join_iff initial k a v).mp h
      exact ⟨b,first,v,second,tail⟩
    · rintro ⟨b,first,v,second,tail⟩
      exact ⟨v,(join_iff initial k a v).mpr ⟨b,first,second⟩,tail⟩

/-- Only the orthant signs are encoded, not the input formula or amplitude magnitudes. -/
theorem two_canonical_rows (k : Key) :
    ∃ angle : Bool → ℝ, ∀ a,
      (codeAmp (angle a)).word = bitSign (atBit k a false) ∧
      (codeAmp (angle a)).verb = bitSign (atBit k a true) ∧
      decodeAmp (codeAmp (angle a)) = v (angle a) := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  have repr (a : Bool) : ∃ θ : ℝ, (codeAmp θ).word = bitSign (atBit k a false) ∧
      (codeAmp θ).verb = bitSign (atBit k a true) := by
    exact the_orbit_visits_all_four_states _ _ (nz _) (nz _)
  obtain ⟨lo,lw,lv⟩ := repr false
  obtain ⟨hi,hw,hv⟩ := repr true
  refine ⟨fun b => if b then hi else lo, ?_⟩
  intro a
  cases a
  · exact ⟨lw,lv,decodeAmp_codeAmp lo⟩
  · exact ⟨hw,hv,decodeAmp_codeAmp hi⟩

/-- A single sign pair cannot be an exact free-standing code for all binary relations. -/
theorem no_single_orthant :
    ¬ ∃ (compress : Key → Symbol) (restore : Symbol → Key), ∀ k, restore (compress k) = k := by
  rintro ⟨compress,restore,h⟩
  have inj : Function.Injective compress := fun x y e => (h x).symm.trans ((congrArg restore e).trans (h y))
  have bound := Fintype.card_le_of_injective compress inj
  exact (by decide : ¬ Fintype.card Key ≤ Fintype.card Symbol) bound

def equalityCNF : CNF 2 := [[⟨0,false⟩,⟨1,true⟩],[⟨0,true⟩,⟨1,false⟩]]
def inequalityCNF : CNF 2 := [[⟨0,true⟩,⟨1,true⟩],[⟨0,false⟩,⟨1,false⟩]]
def twoVarKey (p : CNF 2) : Key :=
  encode (fun a b => passes p (fun i => if i.val=0 then a else b))

def forbid (k : Key) (a b : Bool) : CNF 2 :=
  if atBit k a b then [] else [[⟨0,!a⟩,⟨1,!b⟩]]

/-- Conjoin exactly the clauses forbidding the excluded endpoint pairs. -/
def materialize (k : Key) : CNF 2 :=
  forbid k false false ++ forbid k false true ++ forbid k true false ++ forbid k true true

theorem all_keys_realized (k : Key) :
    twoVarKey (materialize k) = k ∧ (materialize k).length ≤ 4 := by
  rcases k with ⟨⟨a,b⟩,⟨c,d⟩⟩
  cases a <;> cases b <;> cases c <;> cases d <;> decide

/-- Even on two-variable binary CNFs, one orthant cannot recover the
four endpoint queries from its signs alone. -/
theorem no_single_for_cnf :
    ¬ ∃ (compress : CNF 2 → Symbol) (restore : Symbol → Key), ∀ p, restore (compress p) = twoVarKey p := by
  rintro ⟨compress,restore,h⟩
  apply no_single_orthant
  exact ⟨fun k => compress (materialize k),restore,fun k => (h _).trans (all_keys_realized k).1⟩

theorem same_marginals_opposite_entry :
    (∀ a : Bool, (supported (twoVarKey equalityCNF) a ↔ supported (twoVarKey inequalityCNF) a)) ∧
    (∀ b : Bool, ((∃ a, atBit (twoVarKey equalityCNF) a b = true) ↔
                     (∃ a, atBit (twoVarKey inequalityCNF) a b = true))) ∧
    atBit (twoVarKey equalityCNF) false false = true ∧
    atBit (twoVarKey inequalityCNF) false false = false := by
  unfold supported
  decide

/-- Four consecutive bits carry the two orthants of one complete key. -/
def packet (k : Key) := [k.1.1,k.1.2,k.2.1,k.2.2]
inductive Frame where
  | ready
  | first (a : Bool)
  | half (lo : Symbol)
  | third (lo : Symbol) (c : Bool)
abbrev Register := Key × Frame

def receive (s : Register) (b : Bool) : Register :=
  match s.2 with
  | .ready => (s.1,.first b)
  | .first a => (s.1,.half (a,b))
  | .half row => (s.1,.third row b)
  | .third row c => (join s.1 (row,(c,b)),.ready)

theorem receive_packet (k next : Key) :
    (packet next).foldl receive (k,.ready) = (join k next,.ready) := by
  rfl

def wire (ks : List Key) := ks.flatMap packet

theorem wire_exact (ks : List Key) (initial : Key) :
    (wire ks).foldl receive (initial,.ready) = (ks.foldl join initial,.ready) := by
  induction ks generalizing initial with
  | nil => rfl
  | cons k ks ih =>
    change (packet k ++ wire ks).foldl receive (initial,.ready) = _
    rw [List.foldl_append,receive_packet]
    exact ih (join initial k)

theorem wire_length (ks : List Key) : (wire ks).length = 4 * ks.length := by
  induction ks with
  | nil => rfl
  | cons k ks ih =>
    change (packet k ++ wire ks).length = 4*(ks.length+1)
    rw [List.length_append,ih]
    change 4 + 4*ks.length = _
    omega

inductive Machine where
  | walk (s : Register) (unread : List Bool)
  | halt (s : Register)

def step : Machine → Machine
  | .walk s (b::w) => .walk (receive s b) w
  | .walk s [] => .halt s
  | .halt s => .halt s

def travel : Nat → Machine → Nat
  | 0,_ => 0
  | t+1, m => (match m with | .walk _ (_::_) => 1 | _ => 0) + travel t (step m)

private theorem travel_scan (w : List Bool) (s : Register) :
    step^[w.length+1] (.walk s w) = .halt (w.foldl receive s) ∧
    travel (w.length+1) (.walk s w) = w.length := by
  induction w generalizing s with
  | nil => exact ⟨rfl,rfl⟩
  | cons b w ih =>
    obtain ⟨h,t⟩ := ih (receive s b)
    constructor
    · rw [List.length_cons,Function.iterate_succ_apply]
      exact h
    · change 1 + travel (w.length+1) (.walk (receive s b) w) = w.length+1
      omega

/-- Moves from a stream of already computed keys. Proof of
construction costs for a particular raw CNF string belongs to the source reader. -/
theorem transmitted_chain (ks : List Key) (initial : Key) :
    step^[4*ks.length+1] (.walk (initial,.ready) (wire ks)) =
        .halt (ks.foldl join initial,.ready) ∧
    travel (4*ks.length+1) (.walk (initial,.ready) (wire ks)) = 4*ks.length ∧
    ∀ a c, atBit (ks.foldl join initial) a c = true ↔
      ∃ b, atBit initial a b = true ∧ endToEnd ks b c := by
  obtain ⟨halt,moves⟩ := travel_scan (wire ks) (initial,.ready)
  rw [wire_length,wire_exact] at halt
  rw [wire_length] at moves
  exact ⟨halt,moves,path_iff ks initial⟩

end Codex.OrthantRelation

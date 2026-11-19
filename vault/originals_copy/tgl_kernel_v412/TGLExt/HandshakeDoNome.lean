import TGLExt.ClausulaNoSeparador

/-! A mathematical challenge fixes the two blocks, the new clause, the branch
and an ordered list of shared variable names. A response carries the values
in that order and whether its local witness meets its share of the clause.
These are semantic contracts, not cryptographic security assumptions. -/
set_option autoImplicit false
namespace Codex.NamedHandshake
open TGLExt.TraducaoTuring IALD.LeitorDaFormula
open Codex.BranchPresence Codex.IndependentFactors Codex.FreeSeparator
variable {n : Nat}

structure Echo where
  content : List Bool
  hit : Bool
deriving DecidableEq, Repr

def reply (ids : List (Fin n)) (part : Clausula n) (x : Fin n → Bool) : Echo :=
  ⟨ids.map x,satisfeita part x⟩

def certified (p : CNF n) (part : Clausula n) (ms : List (Literal n))
    (ids : List (Fin n)) (e : Echo) : Prop :=
  ∃ x, passes p x = true ∧ Agrees x ms ∧ reply ids part x = e

def handshake (l r : Echo) := (l.content == r.content) && (l.hit || r.hit)

def marks (ids : List (Fin n)) (x : Fin n → Bool) : List (Literal n) :=
  ids.map (fun i => ⟨i,x i⟩)

theorem equal_content (ids : List (Fin n)) (x y : Fin n → Bool) :
    ids.map x = ids.map y ↔ ∀ i ∈ ids, x i = y i := by
  induction ids with
  | nil => simp
  | cons i ids ih =>
    simp only [List.map_cons,List.cons.injEq,ih,List.mem_cons]
    constructor
    · rintro ⟨hi,rest⟩ j (rfl|hj)
      · exact hi
      · exact rest _ hj
    · intro h
      exact ⟨h _ (Or.inl rfl),fun j hj => h j (Or.inr hj)⟩

private theorem mark_values (ids : List (Fin n)) (x y : Fin n → Bool) :
    Agrees y (marks ids x) ↔ ∀ i ∈ ids, x i = y i := by
  constructor
  · intro h i hi
    exact (h ⟨i,x i⟩ (List.mem_map.mpr ⟨i,hi,rfl⟩)).symm
  · intro h l hl
    obtain ⟨j,hj,rfl⟩ := List.mem_map.mp hl
    exact (h _ hj).symm

private theorem combined (x : Fin n → Bool) (a b : List (Literal n)) :
    Agrees x (a++b) ↔ Agrees x a ∧ Agrees x b := by
  constructor
  · intro h
    exact ⟨fun l hl => h l (List.mem_append_left _ hl),fun l hl => h l (List.mem_append_right _ hl)⟩
  · rintro ⟨ha,hb⟩ l hl
    exact (List.mem_append.mp hl).elim (ha l) (hb l)

def covers (p q : CNF n) (ms : List (Literal n)) (ids : List (Fin n)) : Prop :=
  ∀ i, appears p i = true → appears q i = true → i ∈ ids ∨ ∃ l ∈ ms, l.var=i

private theorem cutting (p q : CNF n) (ms : List (Literal n)) (ids : List (Fin n))
    (x : Fin n → Bool) (h : covers p q ms ids) : splitAtLabels p q (marks ids x ++ ms) := by
  intro i hp hq
  rcases h i hp hq with mem|⟨l,ml,eq⟩
  · exact ⟨⟨i,x i⟩,List.mem_append_left _ (List.mem_map.mpr ⟨i,mem,rfl⟩),rfl⟩
  · exact ⟨l,List.mem_append_right _ ml,eq⟩

private theorem split_hit (p : CNF n) (c : Clausula n) (x : Fin n → Bool)
    (h : satisfeita c x = true) :
    satisfeita (slice p c true) x = true ∨ satisfeita (slice p c false) x = true := by
  obtain ⟨l,m,v⟩ := List.any_eq_true.mp h
  cases e : appears p l.var with
  | false => exact Or.inr (List.any_eq_true.mpr ⟨l,List.mem_filter.mpr ⟨m,by simp [e]⟩,v⟩)
  | true => exact Or.inl (List.any_eq_true.mpr ⟨l,List.mem_filter.mpr ⟨m,by simp [e]⟩,v⟩)

/-- Sound and complete for any number of shared names. The two echoes
must each come from one valid whole local witness on the declared branch. -/
theorem semantic_handshake (p q : CNF n) (c : Clausula n) (ms : List (Literal n))
    (ids : List (Fin n)) (cut : covers p q ms ids) :
    Compatible ((p++q)++[c]) ms ↔ ∃ l r,
      certified p (slice p c true) ms ids l ∧ certified q (slice p c false) ms ids r ∧
      handshake l r = true := by
  constructor
  · rintro ⟨x,sat,agree⟩
    have parts : (passes p x = true ∧ passes q x = true) ∧ satisfeita c x = true := by
      simpa [passes,and_assoc] using sat
    refine ⟨_,_,⟨x,parts.1.1,agree,rfl⟩,⟨x,parts.1.2,agree,rfl⟩,?_⟩
    simpa [handshake,reply] using split_hit p c x parts.2
  · rintro ⟨l,r,⟨x,hx,mx,rfl⟩,⟨y,hy,my,rfl⟩,accepted⟩
    have pair : ids.map x = ids.map y ∧
        (satisfeita (slice p c true) x = true ∨ satisfeita (slice p c false) y = true) := by
      simpa [handshake,reply] using accepted
    let allMarks := marks ids x ++ ms
    have ax : Agrees x allMarks := (combined _ _ _).mpr ⟨(mark_values ..).mpr (fun _ _ => rfl),mx⟩
    have ay : Agrees y allMarks := (combined _ _ _).mpr ⟨(mark_values ..).mpr ((equal_content ..).mp pair.1),my⟩
    have joined : Compatible ((p++q)++[c]) allMarks := by
      apply (conditional_join p q c allMarks (cutting _ _ _ _ _ cut)).mpr
      rcases pair.2 with yes|yes
      · exact Or.inl ⟨⟨x,by simpa [passes] using And.intro hx yes,ax⟩,y,hy,ay⟩
      · exact Or.inr ⟨⟨x,hx,ax⟩,y,by simpa [passes] using And.intro hy yes,ay⟩
    obtain ⟨w,hw,mw⟩ := joined
    exact ⟨w,hw,((combined _ _ _).mp mw).2⟩

def ledger (ls rs : List Echo) := ls.any (fun l => rs.any (handshake l))

theorem supplied_ledgers (p q : CNF n) (c : Clausula n) (ms : List (Literal n))
    (ids : List (Fin n)) (cut : covers p q ms ids) (ls rs : List Echo)
    (left : ∀ e, e ∈ ls ↔ certified p (slice p c true) ms ids e)
    (right : ∀ e, e ∈ rs ↔ certified q (slice p c false) ms ids e) :
    ledger ls rs = true ↔ Compatible ((p++q)++[c]) ms := by
  rw [semantic_handshake _ _ _ _ _ cut]
  simp only [ledger,List.any_eq_true,left,right]
  constructor
  · rintro ⟨l,hl,r,hr,pass⟩
    exact ⟨l,r,hl,hr,pass⟩
  · rintro ⟨l,r,hl,hr,pass⟩
    exact ⟨l,hl,r,hr,pass⟩

/-- Coalesce alternative witnesses for the SAME named word by OR of
their hits, never by OR of individual variable values across witnesses. -/
theorem reuse_same_content (word : List Bool) (a b : Bool) (remote : Echo) :
    handshake ⟨word,a || b⟩ remote =
      (handshake ⟨word,a⟩ remote || handshake ⟨word,b⟩ remote) := by
  cases h : (word == remote.content) <;> cases a <;> cases b <;> cases r : remote.hit <;>
    simp [handshake,h,r]

theorem content_example :
    let one : Echo := ⟨[false,true],true⟩
    let other : Echo := ⟨[true,false],true⟩
    handshake one other = false ∧ handshake one ⟨[false,true],false⟩ = true ∧
    handshake ⟨[false,true],false⟩ ⟨[false,true],false⟩ = false := by decide

end Codex.NamedHandshake

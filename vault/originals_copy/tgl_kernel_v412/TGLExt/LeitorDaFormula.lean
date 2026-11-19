import TGLExt.TraducaoTuring
import TGLExt.Psibit

/- Um ramo dispensado (none) denota verdadeiro.
   A sintaxe é calculável. O ângulo serve apenas para identificar a leitura no kernel. -/
namespace IALD.LeitorDaFormula

open TGLExt.TraducaoTuring
open TGLExt.Psibit

def passes {n : ℕ} (f : CNF n) (x : Fin n → Bool) : Bool :=
  f.all (fun c => satisfeita c x)

theorem sat_iff {n : ℕ} (f : CNF n) : SAT f ↔ ∃ x, passes f x = true := by
  simp [SAT, passes, List.all_eq_true]

def addLiteral {n : ℕ} (b : Bool) (l : Literal (n+1))
    (tail : Option (Clausula n)) : Option (Clausula n) :=
  Fin.cases (if b == l.pos then none else tail)
    (fun i => tail.map (fun c => ⟨i,l.pos⟩ :: c)) l.var

def restrictClause {n : ℕ} (b : Bool) (c : Clausula (n+1)) : Option (Clausula n) :=
  c.foldr (addLiteral b) (some [])

def readClause {n : ℕ} (o : Option (Clausula n)) (x : Fin n → Bool) : Bool :=
  o.elim true (fun c => satisfeita c x)

theorem read_addLiteral {n : ℕ} (b : Bool) (l : Literal (n+1))
    (s : Option (Clausula n)) (x : Fin n → Bool) :
    readClause (addLiteral b l s) x =
      (l.vale (Fin.cases b x) || readClause s x) := by
  obtain ⟨i,p⟩ := l
  cases i using Fin.cases with
  | zero => cases b <;> cases p <;> simp [addLiteral, readClause, Literal.vale]
  | succ i => cases s <;> simp [addLiteral, readClause, Literal.vale, satisfeita]

theorem restrictClause_spec {n : ℕ} (b : Bool) (c : Clausula (n+1)) (x : Fin n → Bool) :
    readClause (restrictClause b c) x = satisfeita c (Fin.cases b x) := by
  induction c with
  | nil => rfl
  | cons l c ih =>
    change readClause (addLiteral b l (restrictClause b c)) x = _
    rw [read_addLiteral, ih]
    rfl

abbrev Summary (n : ℕ) := CNF n × CNF n

def extendBranch {n : ℕ} (b : Bool) (s : CNF n) (c : Clausula (n+1)) : CNF n :=
  match restrictClause b c with
  | none => s
  | some d => d :: s

def update {n : ℕ} (s : Summary n) (c : Clausula (n+1)) : Summary n :=
  (extendBranch false s.1 c, extendBranch true s.2 c)

def summarize {n : ℕ} (f : CNF (n+1)) : Summary n := f.foldl update ([], [])

theorem extend_spec {n : ℕ} (b : Bool) (s : CNF n) (c : Clausula (n+1))
    (x : Fin n → Bool) : passes (extendBranch b s c) x =
      (satisfeita c (Fin.cases b x) && passes s x) := by
  rw [← restrictClause_spec]
  unfold extendBranch
  cases restrictClause b c <;> simp [readClause, passes]

def branch {n : ℕ} (b : Bool) (s : Summary n) : CNF n := if b then s.2 else s.1

theorem stream_spec {n : ℕ} (b : Bool) (f : CNF (n+1)) (s : Summary n)
    (x : Fin n → Bool) : passes (branch b (f.foldl update s)) x =
      (passes f (Fin.cases b x) && passes (branch b s) x) := by
  induction f generalizing s with
  | nil => simp [passes]
  | cons c f ih =>
    rw [List.foldl_cons, ih]
    have cons_pass (z : Fin (n+1) → Bool) : passes (c :: f) z = (satisfeita c z && passes f z) := rfl
    cases b <;> simp [branch, update, extend_spec, cons_pass] <;> ac_rfl

theorem summarize_spec {n : ℕ} (b : Bool) (f : CNF (n+1)) (x : Fin n → Bool) :
    passes (branch b (summarize f)) x = passes f (Fin.cases b x) := by
  rw [summarize, stream_spec]
  cases b <;> simp [branch, passes]

def bitSign (b : Bool) : SignType := if b then 1 else -1

/-- Para cada contexto comum dos dois ramos, os sinais lidos são os de uma amplitude real
    do PsiBit canônico e a decodificação recupera a amplitude da mesma órbita. -/
theorem leitura_psibit {n : ℕ} (f : CNF (n+1)) (x : Fin n → Bool) :
    ∃ θ : ℝ, (codeAmp θ).word = bitSign (passes (summarize f).1 x) ∧
      (codeAmp θ).verb = bitSign (passes (summarize f).2 x) ∧
      (codeAmp θ).word = bitSign (passes f (Fin.cases false x)) ∧
      (codeAmp θ).verb = bitSign (passes f (Fin.cases true x)) ∧
      decodeAmp (codeAmp θ) = v θ := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  obtain ⟨θ,h₀,h₁⟩ := the_orbit_visits_all_four_states _ _
    (nz (passes (summarize f).1 x)) (nz (passes (summarize f).2 x))
  exact ⟨θ,h₀,h₁, h₀.trans (congrArg bitSign (summarize_spec false f x)),
    h₁.trans (congrArg bitSign (summarize_spec true f x)), decodeAmp_codeAmp θ⟩

/-- Disjunção dos dois ramos, mantendo a mesma atribuição nas demais variáveis. -/
def merge {n : ℕ} (s : Summary n) : CNF n :=
  s.1.flatMap (fun c => s.2.map (fun d => c ++ d))

theorem merge_spec {n : ℕ} (s : Summary n) (x : Fin n → Bool) :
    passes (merge s) x = (passes s.1 x || passes s.2 x) := by
  apply Bool.eq_iff_iff.mpr
  simp [merge, passes, List.all_eq_true, satisfeita, List.any_append]
  constructor
  · intro h
    by_cases h₁ : ∀ c ∈ s.1, ∃ l ∈ c, l.vale x = true
    · exact Or.inl h₁
    · push Not at h₁
      obtain ⟨c,hc,hn⟩ := h₁
      right
      intro d hd
      rcases h c hc d hd with ha | hb
      · obtain ⟨l,hl,hh⟩ := ha
        have := hn l hl
        simp_all
      · exact hb
  · rintro (h | h) c hc d hd
    · exact Or.inl (h c hc)
    · exact Or.inr (h d hd)

theorem merge_size {n : ℕ} (s : Summary n) :
    (merge s).length = s.1.length * s.2.length := by
  rcases s with ⟨a,b⟩
  induction a with
  | nil => simp [merge]
  | cons c a ih =>
    change ((b.map (fun d => c ++ d)) ++ _).length = (a.length + 1) * b.length
    rw [List.length_append, List.length_map]
    change b.length + (merge (a,b)).length = _
    rw [ih, Nat.add_mul, Nat.one_mul, Nat.add_comm]

def eliminate {n : ℕ} (f : CNF (n+1)) : CNF n := merge (summarize f)

/-- Em uma etapa, cada cláusula acrescenta no máximo uma cláusula a cada ramo. -/
theorem branch_count {n : ℕ} (b : Bool) (f : CNF (n+1)) (s : Summary n) :
    (branch b (f.foldl update s)).length ≤ (branch b s).length + f.length := by
  induction f generalizing s with
  | nil => simp
  | cons c f ih =>
    rw [List.foldl_cons]
    have step : (branch b (update s c)).length ≤ (branch b s).length + 1 := by
      cases b <;> simp [branch, update, extendBranch] <;> split <;> simp
    have h := ih (update s c)
    simp only [List.length_cons]
    omega

/-- Exemplo calculado: duas cláusulas sobre a última variável; a expansão crua
    das duas variáveis anteriores produz primeiro quatro e depois dezesseis cláusulas. -/
example : let f : CNF 3 := [[⟨2,true⟩],[⟨2,false⟩]]
          (eliminate f).length = 4 ∧ (eliminate (eliminate f)).length = 16 := by decide

theorem eliminate_spec {n : ℕ} (f : CNF (n+1)) : SAT (eliminate f) ↔ SAT f := by
  rw [sat_iff, sat_iff]
  constructor
  · rintro ⟨x,hx⟩
    rw [eliminate, merge_spec, Bool.or_eq_true] at hx
    rcases hx with h | h
    · exact ⟨Fin.cases false x, (summarize_spec false f x).symm.trans h⟩
    · exact ⟨Fin.cases true x, (summarize_spec true f x).symm.trans h⟩
  · rintro ⟨y,hy⟩
    let x : Fin n → Bool := fun i => y i.succ
    have he : Fin.cases (y 0) x = y := by funext i; cases i using Fin.cases <;> rfl
    have hval : passes f (Fin.cases (y 0) x) = true := by simpa only [he] using hy
    have hb := (summarize_spec (y 0) f x).trans hval
    refine ⟨x, ?_⟩
    rw [eliminate, merge_spec, Bool.or_eq_true]
    cases h : y 0 <;> simp [h, branch] at hb
    · exact Or.inl hb
    · exact Or.inr hb

/-- Decisor sobre listas finitas, sem pesos, somas reais ou oráculo. -/
def solve : (n : ℕ) → CNF n → Bool
  | 0, f => passes f Fin.elim0
  | n+1, f => solve n (eliminate f)

theorem solve_spec (n : ℕ) (f : CNF n) : solve n f = true ↔ SAT f := by
  induction n with
  | zero =>
    rw [sat_iff]
    constructor
    · intro h; exact ⟨Fin.elim0,h⟩
    · rintro ⟨x,h⟩
      have he : x = Fin.elim0 := by funext i; exact Fin.elim0 i
      simpa [solve, he] using h
  | succ n ih =>
    exact (ih (eliminate f)).trans (eliminate_spec f)

end IALD.LeitorDaFormula

import TGLExt.LeitorDaFormula

namespace IALD.InformacaoDoResumo
open TGLExt.TraducaoTuring IALD.LeitorDaFormula

/-- Uma unidade por literal e uma por cláusula. Os índices conservam a largura original. -/
def letters {n : ℕ} (f : CNF n) : ℕ := (f.map (fun c => c.length + 1)).sum

def clauseSize {n : ℕ} (c : Option (Clausula n)) : ℕ := c.elim 0 (fun d => d.length + 1)

theorem restrict_size {n : ℕ} (b : Bool) (c : Clausula (n+1)) :
    clauseSize (restrictClause b c) ≤ c.length + 1 := by
  induction c with
  | nil => exact Nat.le_refl 1
  | cons l c ih =>
    obtain ⟨i,p⟩ := l
    have single (s : Option (Clausula n)) :
        clauseSize (addLiteral b ⟨i,p⟩ s) ≤ clauseSize s + 1 := by
      cases i using Fin.cases with
      | zero => cases b <;> cases p <;> simp [addLiteral, clauseSize]
      | succ i => cases s <;> simp [addLiteral, clauseSize]
    change clauseSize (addLiteral b ⟨i,p⟩ (restrictClause b c)) ≤ _
    have h := single (restrictClause b c)
    simp only [List.length_cons]
    omega

theorem stream_letters {n : ℕ} (b : Bool) (f : CNF (n+1)) (s : Summary n) :
    letters (branch b (f.foldl update s)) ≤ letters (branch b s) + letters f := by
  have cost (b : Bool) (s : CNF n) (c : Clausula (n+1)) :
      letters (extendBranch b s c) ≤ letters s + (c.length + 1) := by
    have h := restrict_size b c
    cases he : restrictClause b c with
    | none => simp [extendBranch, he]
    | some d =>
      rw [he] at h
      change d.length + 1 ≤ c.length + 1 at h
      simp only [extendBranch, he, letters, List.map_cons, List.sum_cons]
      omega
  induction f generalizing s with
  | nil => simp [letters]
  | cons c f ih =>
    rw [List.foldl_cons]
    have h := ih (update s c)
    have step : letters (branch b (update s c)) ≤ letters (branch b s) + (c.length+1) := by
      cases b <;> apply cost
    have hc : letters (c :: f) = (c.length + 1) + letters f := by simp [letters]
    rw [hc]
    omega

theorem prefix_size {n : ℕ} (f : CNF (n+1)) :
    letters (summarize f).1 + letters (summarize f).2 ≤ 2 * letters f := by
  have left := stream_letters false f ([],[])
  have right := stream_letters true f ([],[])
  change letters (summarize f).1 ≤ 0 + letters f at left
  change letters (summarize f).2 ≤ 0 + letters f at right
  omega

/-- Continuação que exige uma atribuição específica, com uma cláusula unitária por variável. -/
def isolate {n : ℕ} (x : Fin n → Bool) : CNF n :=
  List.ofFn (fun i : Fin n => [⟨i,x i⟩])

theorem isolate_spec {n : ℕ} (x z : Fin n → Bool) :
    passes (isolate x) z = true ↔ z = x := by
  simp [passes, isolate, List.all_eq_true, satisfeita, Literal.vale, funext_iff]

theorem append_isolate {n : ℕ} (f : CNF n) (x : Fin n → Bool) :
    SAT (f ++ isolate x) ↔ passes f x = true := by
  rw [sat_iff]
  constructor
  · rintro ⟨z,h⟩
    change ((f ++ isolate x).all _) = true at h
    rw [List.all_append, Bool.and_eq_true] at h
    have hz := (isolate_spec x z).mp h.2
    exact hz ▸ h.1
  · intro hx
    refine ⟨x, ?_⟩
    change ((f ++ isolate x).all _) = true
    rw [List.all_append, Bool.and_eq_true]
    exact ⟨hx,(isolate_spec x x).2 rfl⟩

/-- Dois prefixos suportam exatamente os mesmos futuros sse têm a mesma função verdade. -/
theorem all_continuations_iff {n : ℕ} (f g : CNF n) :
    (∀ future, SAT (f ++ future) ↔ SAT (g ++ future)) ↔
    (∀ x, passes f x = passes g x) := by
  constructor
  · intro h x
    apply Bool.eq_iff_iff.mpr
    simpa only [append_isolate] using h (isolate x)
  · intro h future
    rw [sat_iff, sat_iff]
    have eqv (x : Fin n → Bool) : passes (f ++ future) x = passes (g ++ future) x := by
      change (f ++ future).all _ = (g ++ future).all _
      rw [List.all_append, List.all_append]
      exact congrArg (fun t => t && passes future x) (h x)
    simp only [eqv]

/-- Critério necessário para qualquer codificação e qualquer preço de acesso à sua memória. -/
theorem same_state_preserves_assignments {n : ℕ} {S : Type*}
    (initial : S) (step : S → Clausula n → S) (read : S → Bool)
    (ok : ∀ f : CNF n, read (f.foldl step initial) = true ↔ SAT f)
    {f g : CNF n} (collision : f.foldl step initial = g.foldl step initial) :
    ∀ x, passes f x = passes g x := by
  apply (all_continuations_iff f g).mp
  intro future
  rw [← ok, ← ok, List.foldl_append, List.foldl_append, collision]

end IALD.InformacaoDoResumo

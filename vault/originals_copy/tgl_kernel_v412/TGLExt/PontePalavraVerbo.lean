import TGLExt.LeitorDaFormula
import TGLExt.OPsibitEACompressao

namespace IALD.PontePalavraVerbo
open TGLExt.TraducaoTuring TGLExt.Psibit TGLExt.OPsibitEACompressao
open IALD.LeitorDaFormula

/-- Há na cláusula um literal e o seu oposto. As duas buscas só percorrem a cláusula. -/
def oppositePair {n : ℕ} (c : Clausula n) : Bool :=
  c.any (fun l => c.any (fun k => k.var == l.var && k.pos != l.pos))

def avoiding {n : ℕ} (c : Clausula n) (i : Fin n) : Bool :=
  c.any (fun k => k.var == i && !k.pos)

theorem oppositePair_spec {n : ℕ} (c : Clausula n) :
    oppositePair c = true ↔ ∀ x, satisfeita c x = true := by
  constructor
  · intro h x
    obtain ⟨l,hl,hk⟩ := List.any_eq_true.mp h
    obtain ⟨k,hk',hm⟩ := List.any_eq_true.mp hk
    have hp : k.var = l.var ∧ k.pos ≠ l.pos := by simpa using hm
    apply List.any_eq_true.mpr
    by_cases hx : x l.var = l.pos
    · exact ⟨l,hl,by simp [Literal.vale,hx]⟩
    · refine ⟨k,hk',?_⟩
      simp only [Literal.vale, hp.1, beq_iff_eq]
      have hn := hp.2
      cases h₁ : l.pos <;> cases h₂ : k.pos <;> cases h₃ : x l.var <;> simp_all
  · intro h
    obtain ⟨l,hl,hv⟩ := List.any_eq_true.mp (h (avoiding c))
    cases hp : l.pos with
    | false =>
      have ht : avoiding c l.var = true := List.any_eq_true.mpr ⟨l,hl,by simp [hp]⟩
      simp [Literal.vale, hp, ht] at hv
    | true =>
      have ht : avoiding c l.var = true := by simpa [Literal.vale,hp] using hv
      obtain ⟨k,hk,hv'⟩ := List.any_eq_true.mp ht
      apply List.any_eq_true.mpr
      refine ⟨l,hl,List.any_eq_true.mpr ⟨k,hk,?_⟩⟩
      simpa [hp] using hv'

def quiet {n : ℕ} (f : CNF n) : Bool := f.all oppositePair

theorem quiet_update {n : ℕ} (f : CNF n) (c : Clausula n) :
    quiet (c :: f) = (oppositePair c && quiet f) := rfl

theorem quiet_spec {n : ℕ} (f : CNF n) (s : ℝ) :
    quiet f = true ↔ verboCalado (custoCNF f) s := by
  rw [o_verbo_cala_sse_tudo_e_nome]
  simp only [quiet, List.all_eq_true, oppositePair_spec, custoCNF_zero_sse]
  constructor
  · intro h x c hc; exact h c hc x
  · intro h c hc x; exact h x c hc

/-- Os dois bits de `OPsibitEACompressao` calculados da sintaxe. -/
def bits {n : ℕ} (f : CNF n) : Bool × Bool := (solve n f, quiet f)

/-- Uma leitura sem máscara e uma por coordenada, obtidas inteiramente da sintaxe. -/
def syntaxRead {n : ℕ} (f : CNF n) (j : Option (Fin n)) : Bool :=
  match j with
  | none => solve n f
  | some i => solve n ([⟨i,true⟩] :: f)

theorem syntax_recovers_unique {n : ℕ} (f : CNF n) (x : Fin n → Bool)
    (hx : passes f x = true) (unique : ∀ z, passes f z = true → z = x) :
    syntaxRead f none = true ∧ (fun i => syntaxRead f (some i)) = x := by
  constructor
  · exact (solve_spec n f).2 ((sat_iff f).2 ⟨x,hx⟩)
  · funext i
    apply Bool.eq_iff_iff.mpr
    change solve n ([⟨i,true⟩] :: f) = true ↔ x i = true
    rw [solve_spec, sat_iff]
    constructor
    · rintro ⟨z,hz⟩
      change (satisfeita [⟨i,true⟩] z && passes f z) = true at hz
      rw [Bool.and_eq_true] at hz
      obtain ⟨bit,rest⟩ := hz
      simpa [satisfeita, Literal.vale, unique z rest] using bit
    · intro hi
      refine ⟨x, ?_⟩
      change (satisfeita [⟨i,true⟩] x && passes f x) = true
      simp [satisfeita, Literal.vale, hi, hx]

theorem bits_spec {n : ℕ} (f : CNF n) (s : ℝ) (hs : (n:ℝ)*Real.log 2 < s) :
    ((bits f).1 = true ↔ palavra (custoCNF f) s) ∧
    ((bits f).2 = true ↔ verboCalado (custoCNF f) s) :=
  ⟨(solve_spec n f).trans (a_palavra_decide n hs f), quiet_spec f s⟩

/-- Representação dos bits como sinais da órbita; o ângulo é um representante.
    Esta convenção não identifica a derivada de uma órbita com a da partição. -/
theorem bits_on_orbit {n : ℕ} (f : CNF n) (s : ℝ) (hs : (n:ℝ)*Real.log 2 < s) :
    ∃ θ : ℝ, ((codeAmp θ).word = 1 ↔ palavra (custoCNF f) s) ∧
      ((codeAmp θ).verb = 1 ↔ verboCalado (custoCNF f) s) ∧
      decodeAmp (codeAmp θ) = v θ := by
  have nz (b : Bool) : bitSign b ≠ 0 := by cases b <;> decide
  have decode (b : Bool) : bitSign b = 1 ↔ b = true := by cases b <;> decide
  obtain ⟨θ,hw,hv⟩ := the_orbit_visits_all_four_states _ _ (nz (bits f).1) (nz (bits f).2)
  obtain ⟨h₀,h₁⟩ := bits_spec f s hs
  refine ⟨θ, ?_, ?_, decodeAmp_codeAmp θ⟩
  · rw [hw]; exact (decode _).trans h₀
  · rw [hv]; exact (decode _).trans h₁

def unitClause (p : Bool) : Clausula 1 := [⟨0,p⟩]

/-- Mesmo par antes, Palavra diferente depois da mesma cláusula. -/
theorem bits_alone_not_updatable :
    ¬ ∃ u : (Bool × Bool) → Clausula 1 → Bool × Bool,
      ∀ (f : CNF 1) c, u (bits f) c = bits (c :: f) := by
  rintro ⟨u,hu⟩
  have h₁ := hu [unitClause true] (unitClause true)
  have h₂ := hu [unitClause false] (unitClause true)
  have e : bits [unitClause true] = bits [unitClause false] := by decide
  rw [e] at h₁
  have bad : bits [unitClause true,unitClause true] ≠ bits [unitClause true,unitClause false] := by decide
  exact bad (h₁.symm.trans h₂)

end IALD.PontePalavraVerbo

import TGLExt.RotulosAfins
import Mathlib.Tactic.DeriveFintype

/- Família Fₙ = (x₁∨y₁)∧…∧(xₙ∨yₙ). Em um rótulo afim exato dentro de Fₙ,
   cada par projeta em no máximo dois dos três símbolos admitidos, pois os
   três juntos têm XOR ternário 00. As escolhas de bits são usadas na PROVA
   de contagem, não são operação de um leitor eficiente. -/
namespace IALD.CoberturaAfin

open IALD.RotulosAfins TGLExt.TraducaoTuring IALD.LeitorDaFormula

def disjunctions (n : Nat) : CNF (n+n) :=
  List.ofFn (fun i : Fin n => [⟨i.castAdd n,true⟩,⟨Fin.natAdd n i,true⟩])

def Good {n} (x : Assignment (n+n)) : Prop :=
  ∀ i : Fin n, x (i.castAdd n) = true ∨ x (Fin.natAdd n i) = true

theorem cnf_spec (n : Nat) (x : Assignment (n+n)) :
    passes (disjunctions n) x = true ↔ Good x := by
  simp [passes,disjunctions,List.all_eq_true,List.mem_ofFn,satisfeita,Literal.vale,Good]

theorem size (n : Nat) : (disjunctions n).length = n ∧
    ∀ c ∈ disjunctions n, c.length = 2 := by
  constructor
  · simp [disjunctions]
  · intro c hc
    obtain ⟨i,rfl⟩ := List.mem_ofFn.mp hc
    rfl

inductive Tri where
  | low | high | both
deriving DecidableEq, Fintype

def bits : Tri → Bool × Bool
  | .low => (false,true)
  | .high => (true,false)
  | .both => (true,true)

def draw {n} (u : Fin n → Tri) : Assignment (n+n) :=
  Fin.append (fun i => (bits (u i)).1) (fun j => (bits (u j)).2)

theorem draw_good {n} (u : Fin n → Tri) : Good (draw u) := by
  intro i
  simp only [draw,Fin.append_left,Fin.append_right]
  cases u i <;> simp [bits]

def Occurs {n} (s : Label (n+n)) (i : Fin n) (v : Tri) : Prop :=
  ∃ x, fits s x = true ∧ x (i.castAdd n) = (bits v).1 ∧ x (Fin.natAdd n i) = (bits v).2

theorem draw_occurs {n} (s : Label (n+n)) (u : Fin n → Tri)
    (hs : fits s (draw u) = true) (i : Fin n) : Occurs s i (u i) :=
  ⟨draw u,hs,by simp only [draw,Fin.append_left],by simp only [draw,Fin.append_right]⟩

/-- As três testemunhas podem ser três atribuições diferentes. Seu XOR
    ternário ainda pertence ao MESMO rótulo e quebraria a cláusula i. -/
theorem missing_value {n} (s : Label (n+n)) (sound : ∀ x, fits s x = true → Good x)
    (i : Fin n) : Occurs s i .low → Occurs s i .high → Occurs s i .both → False := by
  rintro ⟨a,ha,al,ar⟩ ⟨b,hb,bl,br⟩ ⟨c,hc,cl,cr⟩
  have absurdPair := sound _ (label_closed s a b c ha hb hc) i
  simp only [triple,al,ar,bl,br,cl,cr,bits] at absurdPair
  exact (by decide : ¬ ((Bool.xor (Bool.xor false true) true = true) ∨
    (Bool.xor (Bool.xor true false) true = true))) absurdPair

/-- Um dos dois bits originais separa todos os símbolos realmente alcançados
    naquela projeção. A escolha clássica é suficiente para o limite inferior. -/
noncomputable def color {n} (s : Label (n+n)) (i : Fin n) (v : Tri) : Bool := by
  classical
  exact if Occurs s i .low then (bits v).1 else (bits v).2

theorem color_injective_inside {n} (s : Label (n+n)) (sound : ∀ x, fits s x = true → Good x)
    (i : Fin n) (a b : Tri) (ha : Occurs s i a) (hb : Occurs s i b)
    (he : color s i a = color s i b) : a = b := by
  classical
  have no := missing_value s sound i
  by_cases lo : Occurs s i .low
  · cases a <;> cases b <;> simp_all [color,bits]
  · cases a <;> cases b <;> simp_all [color,bits]

/-- Toda cobertura por K rótulos afins explícitos precisa de K·2ⁿ ≥ 3ⁿ.
    Não impõe ordem de variáveis, pivôs, partição disjunta ou método de escolha. -/
theorem cover_lower_bound (n k : Nat) (labels : Fin k → Label (n+n))
    (correct : ∀ x, (∃ j, fits (labels j) x = true) ↔ passes (disjunctions n) x = true) :
    3^n ≤ k * 2^n := by
  classical
  have sound (j : Fin k) (x : Assignment (n+n)) (h : fits (labels j) x = true) : Good x :=
    (cnf_spec n x).mp ((correct x).mp ⟨j,h⟩)
  have covered (u : Fin n → Tri) : ∃ j, fits (labels j) (draw u) = true :=
    (correct _).mpr ((cnf_spec _ _).mpr (draw_good u))
  let select (u : Fin n → Tri) : Fin k := (covered u).choose
  have selected (u : Fin n → Tri) : fits (labels (select u)) (draw u) = true :=
    (covered u).choose_spec
  let tag (u : Fin n → Tri) : Fin k × (Fin n → Bool) :=
    (select u,fun i => color (labels (select u)) i (u i))
  have inj : Function.Injective tag := by
    intro u v h
    have hidx : select u = select v := congrArg Prod.fst h
    have cols := congrArg Prod.snd h
    funext i
    apply color_injective_inside (labels (select v)) (sound _) i
    · exact draw_occurs _ u (hidx ▸ selected u) i
    · exact draw_occurs _ v (selected v) i
    · have hi := congrFun cols i
      change color (labels (select u)) i (u i) = color (labels (select v)) i (v i) at hi
      simpa only [hidx] using hi
  have cardTri : Fintype.card Tri = 3 := by decide
  simpa [cardTri] using Fintype.card_le_of_injective tag inj

end IALD.CoberturaAfin

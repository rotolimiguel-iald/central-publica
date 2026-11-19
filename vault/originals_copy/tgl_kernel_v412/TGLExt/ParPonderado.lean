import TGLExt.Psibit
import TGLExt.TraducaoTuring

namespace IALD.ParPonderado
open TGLExt.Psibit TGLExt.TraducaoTuring

abbrev Pair := ℝ × ℝ
abbrev Reading := ℝ × Code

noncomputable def scale (w : Pair) := Real.sqrt (w.1^2 + w.2^2)
noncomputable def pack (w : Pair) : Reading :=
  (scale w, codeOf (w.1 / scale w, w.2 / scale w))
noncomputable def unpack (s : Reading) : Pair :=
  let u := decodeAmp s.2
  (u.1 * s.1, u.2 * s.1)

theorem scale_pos (w : Pair) (h : 0 < w.1) : 0 < scale w := by
  apply Real.sqrt_pos.2
  positivity

theorem round_trip (w : Pair) (h : 0 < w.1) : unpack (pack w) = w := by
  have hs := (scale_pos w h).ne'
  have hs2 : (scale w)^2 = w.1^2 + w.2^2 := Real.sq_sqrt (by positivity)
  have unit : (w.1 / scale w)^2 + (w.2 / scale w)^2 = 1 := by
    rw [div_pow, div_pow, ← add_div, ← hs2, div_self (pow_ne_zero 2 hs)]
  have hd := decodeAmp_codeOf (x := (w.1 / scale w, w.2 / scale w)) unit
  simp only [unpack, pack, hd, div_mul_cancel₀ _ hs, Prod.mk.eta]

def factor {n : ℕ} (r : ℝ) (c : Clausula n) (x : Fin n → Bool) : ℝ :=
  if satisfeita c x then 1 else r

def pairAt {n : ℕ} (f : CNF (n+1)) (r : ℝ) (x : Fin n → Bool) : Pair :=
  (r ^ custoCNF f (Fin.cases false x), r ^ custoCNF f (Fin.cases true x))

theorem local_weight {n : ℕ} (f : CNF n) (c : Clausula n) (r : ℝ) (x : Fin n → Bool) :
    r ^ custoCNF (c :: f) x = r ^ custoCNF f x * factor r c x := by
  rw [custoCNF_cons, pow_add]
  cases h : satisfeita c x <;> simp [factor, h]

noncomputable def update {n : ℕ} (s : Reading) (r : ℝ) (c : Clausula (n+1))
    (x : Fin n → Bool) : Reading :=
  let w := unpack s
  pack (w.1 * factor r c (Fin.cases false x), w.2 * factor r c (Fin.cases true x))

/-- A atualização usa o código anterior, a escala, a cláusula e o contexto x. -/
theorem update_spec {n : ℕ} (f : CNF (n+1)) (r : ℝ) (hr : 0 < r)
    (c : Clausula (n+1)) (x : Fin n → Bool) :
    update (pack (pairAt f r x)) r c x = pack (pairAt (c :: f) r x) := by
  have h : 0 < (pairAt f r x).1 := pow_pos hr _
  unfold update
  rw [round_trip _ h]
  simp only [pairAt, local_weight]

def unitY (b : Bool) : Clausula 2 := [⟨1,b⟩]

/-- Soma sobre y em cada ramo de x, exatamente para as duas variáveis do ensaio. -/
def marginal (f : CNF 2) (r : ℝ) : Pair :=
  let a := pairAt f r (fun _ => false)
  let b := pairAt f r (fun _ => true)
  (a.1 + b.1, a.2 + b.2)

theorem initial_collision (r : ℝ) :
    marginal [unitY true] r = marginal [unitY false] r := by
  change (r^1+r^0,r^1+r^0) = (r^0+r^1,r^0+r^1)
  simp [add_comm]

theorem different_after_update (r : ℝ) (hr : r < 1) :
    marginal [unitY true,unitY true] r ≠ marginal [unitY true,unitY false] r := by
  change (r^2+r^0,r^2+r^0) ≠ (r^1+r^1,r^1+r^1)
  intro h
  have he := congrArg Prod.fst h
  simp at he
  nlinarith [sq_pos_of_pos (sub_pos.mpr hr)]

/-- Mesmo guardando a escala e TODO o código canônico das marginais, inexiste
    atualizador exato que receba apenas esse estado e a próxima cláusula. -/
theorem no_marginal_update (r : ℝ) (hr : 0 < r) (hr' : r < 1) :
    ¬ ∃ u : Reading → Clausula 2 → Reading, ∀ f c,
      u (pack (marginal f r)) c = pack (marginal (c :: f) r) := by
  rintro ⟨u,hu⟩
  have hi := initial_collision r
  have ha := hu [unitY true] (unitY true)
  have hb := hu [unitY false] (unitY true)
  rw [hi] at ha
  have he := congrArg unpack (ha.symm.trans hb)
  have pos (f : CNF 2) : 0 < (marginal f r).1 := add_pos (pow_pos hr _) (pow_pos hr _)
  rw [round_trip _ (pos _), round_trip _ (pos _)] at he
  exact different_after_update r hr' he

end IALD.ParPonderado

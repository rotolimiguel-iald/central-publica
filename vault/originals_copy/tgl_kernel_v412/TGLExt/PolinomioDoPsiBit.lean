import TGLExt.FitaDeUmaCabeca
import TGLExt.RedeComoCNF
import TGLExt.CadeiasDeBolsas
import TGLExt.VerboNaFita

set_option autoImplicit false
namespace PsiNetworks.Tape

open TGLExt.OPsiBitDaFormula IALD.RedeComoCNF

theorem charged_letters (e : Net) : (code e).length + 1 = 3 * leaves e := by
  induction e with
  | clause => rfl
  | series l r hl hr | parallel l r hl hr =>
    simp only [code, leaves, List.length_append, List.length_singleton]
    omega

/-- One fixed finite alphabet, one physical head and one polynomial. Each leaf
    supplies two explicit literals and each internal node one gluing letter.
    The existential time quantifies actual iterations of the same local step. -/
theorem fixed_polynomial_for_networks (e : Net) (t : ℝ) :
    ∃ steps ≤ (code e).length ^ 2 + 1, ∃ w v : Bool,
      (run steps (initial e)).mode = .done w v ∧
      (w, if v then (1 : SignType) else 0) = psibitDaFormula (cnf e) t := by
  obtain ⟨bound,halt⟩ := one_head_fixed_polynomial e
  exact ⟨_,bound,_,_,halt,network_psibit e t⟩

end PsiNetworks.Tape

namespace IALD.CadeiasDeBolsas
open TGLExt.OPsiBitDaFormula

/-- Direct correspondence to the two channels of `OPsiBitDaFormula` at every real t.
    A true quiet flag represents sign zero. -/
theorem fixed_width_psibit {k : Nat} (bags : List (Bag k)) (t : ℝ) :
    ∃ w q : Bool, step^[(tape bags).length+1]
        (.reading (ready (fun _ => true) true) (tape bags)) = .stopped w q ∧
      (w, if q then (0 : SignType) else 1) = psibitDaFormula (formula bags) t := by
  have hq : allGood bags = IALD.PontePalavraVerbo.quiet (formula bags) :=
    Bool.eq_iff_iff.mpr ((quiet_spec bags t).trans (IALD.PontePalavraVerbo.quiet_spec _ t).symm)
  have hw : (rows k).any (relation bags) = palavraDaFormula (formula bags) :=
    Bool.eq_iff_iff.mpr ((sat_spec bags).trans (a_palavra_e_o_sat _).symm)
  refine ⟨(rows k).any (relation bags), allGood bags, ?_, ?_⟩
  · rw [exact_steps,scan_spec]; rfl
  · change ((rows k).any (relation bags), if allGood bags then (0 : SignType) else 1) =
      (palavraDaFormula (formula bags), verboDaFormula (formula bags) t)
    rw [hw,hq,IALD.VerbTape.bit_sign]

end IALD.CadeiasDeBolsas

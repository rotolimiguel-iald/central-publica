import TGLExt.TraducaoTuring
import Mathlib.InformationTheory.Hamming

set_option autoImplicit false

/-! SUGESTÃO DO REVISOR (14/11/2026): uma versão COMPUTÁVEL do leitor dos vizinhos (sem `Exists.choose`): vai à PRIMEIRA vizinha (na ordem de
    Fin n) que resolve. Aqui só se confere que ela coincide com a do adendo sob `hsep`. Esta seção é autocontida: repete as duas definições do
    adendo (empurrao, leitorDosVizinhos) e o teorema de determinação, sem importar o adendo. -/

namespace TGLExt.NomeComoCodigo.Revisao2

variable {n : ℕ}

def empurrao (x : Fin n → Bool) (j : Fin n) : Fin n → Bool := Function.update x j (!x j)

theorem empurrao_dista_um (x : Fin n → Bool) (j : Fin n) : hammingDist x (empurrao x j) ≤ 1 := by
  unfold hammingDist empurrao
  calc (Finset.univ.filter (fun i => x i ≠ Function.update x j (!x j) i)).card
      ≤ ({j} : Finset (Fin n)).card := by
        apply Finset.card_le_card
        intro i hi
        rw [Finset.mem_filter] at hi
        rw [Finset.mem_singleton]
        by_contra hne
        exact hi.2 (by simp [Function.update, hne])
    _ = 1 := Finset.card_singleton j

noncomputable def leitorDosVizinhos (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) : Fin n → Bool :=
  if c x = 0 then x else if h : ∃ j, c (empurrao x j) = 0 then empurrao x h.choose else x

/-- a versão computável: a primeira vizinha (em Fin n) que resolve (`Fin.find` devolve o menor índice que satisfaz). -/
def leitorPrimeiro (c : (Fin n → Bool) → ℕ) (x : Fin n → Bool) : Fin n → Bool :=
  if c x = 0 then x else if h : ∃ j, c (empurrao x j) = 0 then empurrao x (Fin.find (fun j => c (empurrao x j) = 0) h) else x

theorem leitorPrimeiro_eq (c : (Fin n → Bool) → ℕ)
    (hsep : ∀ s s' : Fin n → Bool, c s = 0 → c s' = 0 → s ≠ s' → 3 ≤ hammingDist s s')
    (x : Fin n → Bool) : leitorPrimeiro c x = leitorDosVizinhos c x := by
  unfold leitorPrimeiro leitorDosVizinhos
  by_cases hx : c x = 0
  · rw [if_pos hx, if_pos hx]
  · rw [if_neg hx, if_neg hx]
    by_cases hex : ∃ j, c (empurrao x j) = 0
    · rw [dif_pos hex, dif_pos hex]
      have h1 : c (empurrao x (Fin.find (fun j => c (empurrao x j) = 0) hex)) = 0 := Fin.find_spec hex
      by_contra hne
      have h3 := hsep _ _ h1 hex.choose_spec hne
      have d1 := empurrao_dista_um x (Fin.find (fun j => c (empurrao x j) = 0) hex)
      have d2 := empurrao_dista_um x hex.choose
      have htri := hammingDist_triangle (empurrao x (Fin.find (fun j => c (empurrao x j) = 0) hex)) x (empurrao x hex.choose)
      have hc := hammingDist_comm (empurrao x (Fin.find (fun j => c (empurrao x j) = 0) hex)) x
      omega
    · rw [dif_neg hex, dif_neg hex]

end TGLExt.NomeComoCodigo.Revisao2

#print axioms TGLExt.NomeComoCodigo.Revisao2.leitorPrimeiro
#print axioms TGLExt.NomeComoCodigo.Revisao2.leitorPrimeiro_eq

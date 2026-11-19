import TGLExt.OResumoEPsiBit
import TGLExt.AFronteiraEOUnicoPortao

set_option autoImplicit false

/-!
# Sonda: a `Cadeia` de `AFronteiraEOUnicoPortao` comporta-se como caminho

Verifica:
1. `cadeia_refl`: reflexiva — todo vértice tem a cadeia trivial até si (é o construtor `single`);
2. `cadeia_trans`: transitiva — cadeia `i→k` e cadeia `k→l` compõem em cadeia `i→l`;
3. `ligadas_sim`: a relação-base `ligadas` é simétrica POR CONSTRUÇÃO — a cláusula que menciona `i` e `k`
   menciona `k` e `i` (a conjunção comuta; não há contraexemplo, a simetria é teorema);
4. `cadeia_sim`: a cadeia é simétrica — lida de trás para frente, usando 2 e 3.
-/

namespace SondaCadeiaCaminho

open TGLExt TGLExt.TraducaoTuring TGLExt.OResumoEPsiBit TGLExt.AFronteiraEOUnicoPortao

variable {n : ℕ} {φ : CNF n}

/-- REFLEXIVA: todo vértice tem a cadeia trivial até si mesmo. -/
theorem cadeia_refl (i : Fin n) : Cadeia φ i i := Cadeia.single i

/-- TRANSITIVA: cadeia `i→k` e cadeia `k→l` compõem em cadeia `i→l` — indução na primeira. -/
theorem cadeia_trans {i k l : Fin n} : Cadeia φ i k → Cadeia φ k l → Cadeia φ i l := by
  intro c₁
  induction c₁ with
  | single i => exact id
  | cons hlink _ ih => exact fun c₂ => Cadeia.cons hlink (ih c₂)

/-- SIMÉTRICA NA BASE: `ligadas` é simétrica por construção — a testemunha é a mesma cláusula. -/
theorem ligadas_sim {i k : Fin n} (h : ligadas φ i k) : ligadas φ k i :=
  let ⟨C, hC, hi, hk⟩ := h
  ⟨C, hC, hk, hi⟩

/-- SIMÉTRICA: a cadeia lida de trás para frente. -/
theorem cadeia_sim {i k : Fin n} (c : Cadeia φ i k) : Cadeia φ k i := by
  induction c with
  | single i => exact Cadeia.single i
  | cons hlink _ ih => exact cadeia_trans ih (Cadeia.cons (ligadas_sim hlink) (Cadeia.single _))

end SondaCadeiaCaminho

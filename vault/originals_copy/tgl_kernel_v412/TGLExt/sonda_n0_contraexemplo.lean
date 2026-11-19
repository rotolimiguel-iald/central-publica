import TGLExt.TraducaoTuring
import TGLExt.AContagemEACarga
import TGLExt.OResumoEPsiBit
import TGLExt.OPsiBitDaFormula

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Sonda: por que o par de controles não vale em `n = 0`

Verificação formal do contraexemplo que fixa em `CNF 1` o enunciado de
`TGLExt.OPsiBitDaFormula.o_par_e_necessario_e_suficiente_na_formula`.

Em `n = 0`: `Fin 0` é vazio, não há literais, toda cláusula é vazia, e:
1. `custo_em_n0`: o custo na única atribuição é o comprimento da fórmula;
2. `sat_em_n0`: `SAT φ ↔ φ = []` — a Palavra decide a forma da fórmula;
3. `particao_em_n0` e `descida_em_n0`: a soma lida é o termo único `e^{−t·|φ|}`;
4. `verbo_em_n0`: o Verbo é `0` na vazia e `1` fora dela — o Verbo também decide a forma da fórmula;
5. ★ `nenhum_controle_em_n0`: Palavra e Verbo se determinam mutuamente em `n = 0`, logo nenhum dos dois
   controles (mesma Palavra com Verbos diferentes; mesmo Verbo com Palavras diferentes) existe aí. A forma
   n-universal do enunciado é FALSA; em `n = 1` os dois controles existem — é o teorema de `OPsiBitDaFormula`.
-/

namespace SondaN0

open TGLExt TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.OResumoEPsiBit TGLExt.OPsiBitDaFormula

/-- Não há literal em zero variáveis: toda cláusula de `CNF 0` é vazia. -/
theorem clausula_em_n0 (C : Clausula 0) : C = [] := by
  rcases C with _ | ⟨l, _⟩
  · rfl
  · exact Fin.elim0 l.var

/-- O custo em zero variáveis é o comprimento da fórmula, em qualquer atribuição. -/
theorem custo_em_n0 (φ : CNF 0) (x : Fin 0 → Bool) : custoCNF φ x = φ.length := by
  unfold custoCNF
  rw [List.countP_eq_length]
  intro C _
  rw [clausula_em_n0 C]
  rfl

/-- SAT em zero variáveis é ser a fórmula vazia. -/
theorem sat_em_n0 (φ : CNF 0) : SAT φ ↔ φ = [] := by
  constructor
  · rintro ⟨x, hx⟩
    rcases φ with _ | ⟨C, ψ⟩
    · rfl
    · exfalso
      have hC := hx C (List.mem_cons_self)
      rw [clausula_em_n0 C] at hC
      simp [satisfeita] at hC
  · intro h
    rw [h]
    exact ⟨fun i => Fin.elim0 i, fun C hC => absurd hC List.not_mem_nil⟩

/-- Em zero variáveis só há uma atribuição: a soma lida é o termo único `e^{−t·|φ|}`. -/
theorem particao_em_n0 (φ : CNF 0) (t : ℝ) :
    particao (custoCNF φ) t = Real.exp (-(t * (φ.length : ℝ))) := by
  unfold particao
  have huniv : (Finset.univ : Finset (Fin 0 → Bool)) = {fun i => Fin.elim0 i} := by
    ext x
    simp only [Finset.mem_univ, Finset.mem_singleton, true_iff]
    funext i
    exact Fin.elim0 i
  rw [huniv, Finset.sum_singleton, custo_em_n0]

/-- A descida em zero variáveis, em forma fechada. -/
theorem descida_em_n0 (φ : CNF 0) (t : ℝ) :
    descida φ t = Real.exp (-(t * (φ.length : ℝ))) * (1 - Real.exp (-(φ.length : ℝ))) := by
  unfold descida
  rw [particao_em_n0, particao_em_n0]
  rw [show -((t + 1) * (φ.length : ℝ)) = -(t * (φ.length : ℝ)) + -(φ.length : ℝ) by ring]
  rw [Real.exp_add]
  ring

/-- O Verbo em zero variáveis: parado (`0`) na fórmula vazia, movendo-se (`1`) fora dela. -/
theorem verbo_em_n0 (φ : CNF 0) (t : ℝ) :
    verboDaFormula φ t = if φ = [] then 0 else 1 := by
  by_cases h : φ = []
  · rw [h, if_pos rfl]
    show SignType.sign (descida ([] : CNF 0) t) = 0
    rw [descida_da_formula_vazia, sign_zero]
  · rw [if_neg h]
    show SignType.sign (descida φ t) = 1
    apply sign_pos
    rw [descida_em_n0]
    apply mul_pos (Real.exp_pos _)
    rw [sub_pos, Real.exp_lt_one_iff]
    have hlen : (0 : ℝ) < (φ.length : ℝ) := by
      have h0 : 0 < φ.length := Nat.pos_of_ne_zero (fun hl => h (List.length_eq_zero_iff.mp hl))
      exact_mod_cast h0
    linarith

/-- A Palavra em zero variáveis: habitada (`true`) na fórmula vazia, vazia (`false`) fora dela. -/
theorem palavra_em_n0 (φ : CNF 0) :
    palavraDaFormula φ = if φ = [] then true else false := by
  by_cases h : φ = []
  · rw [h, if_pos rfl]
    exact (a_palavra_e_o_sat _).mpr
      (⟨fun i => Fin.elim0 i, fun C hC => absurd hC List.not_mem_nil⟩ : SAT ([] : CNF 0))
  · rw [if_neg h]
    unfold palavraDaFormula
    rw [decide_eq_false_iff_not, ← AContagemEACarga.sat_e_existir_custo_zero]
    exact fun hsat => h ((sat_em_n0 φ).mp hsat)

/-- ★ **O CONTRAEXEMPLO**: em `n = 0` nenhum dos dois controles existe — a Palavra e o Verbo se determinam
mutuamente, e a forma n-universal do enunciado `o_par_e_necessario_e_suficiente_na_formula` é falsa. (A refutação já
sai do primeiro controle; o segundo é igualmente impossível, pelos mesmos `verbo_em_n0`/`palavra_em_n0`.) -/
theorem nenhum_controle_em_n0 (t : ℝ) :
    ¬ ((∃ φ ψ : CNF 0,
          palavraDaFormula φ = palavraDaFormula ψ ∧ verboDaFormula φ t ≠ verboDaFormula ψ t)
        ∧ (∃ φ ψ : CNF 0,
          verboDaFormula φ t = verboDaFormula ψ t ∧ palavraDaFormula φ ≠ palavraDaFormula ψ)) := by
  rintro ⟨hA, -⟩
  obtain ⟨φ, ψ, hpal, hverb⟩ := hA
  rw [palavra_em_n0, palavra_em_n0] at hpal
  rw [verbo_em_n0, verbo_em_n0] at hverb
  by_cases hφ : φ = [] <;> by_cases hψ : ψ = []
  · rw [if_pos hφ, if_pos hψ] at hverb
    exact hverb rfl
  · rw [if_pos hφ, if_neg hψ] at hpal
    exact Bool.noConfusion hpal
  · rw [if_neg hφ, if_pos hψ] at hpal
    exact Bool.noConfusion hpal
  · rw [if_neg hφ, if_neg hψ] at hverb
    exact hverb rfl

end SondaN0

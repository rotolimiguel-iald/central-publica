import TGLExt.SimLiteral
import TGLExt.SimExterior
set_option autoImplicit false
namespace TGLExt.SimTM2

open TGLExt.APonteAoTM2 TGLExt.AMaquinaTM2DaVerificacao

private abbrev Lit := ℕ × Bool
private def hit (bs : List Bool) (p : Lit) : Bool := bs[p.1]? == some p.2

private def clauseCost (c : List Lit) : ℕ :=
  4 * (c.map Prod.fst).sum + 10 * c.length + (codificaClausula c).length + 1

private def formulaCost (f : List (List Lit)) : ℕ :=
  4 * (f.flatten.map Prod.fst).sum + 10 * f.flatten.length + (codificaFormula f).length + f.length

private theorem encC_cons (p : Lit) (c : List Lit) :
    codificaClausula (p::c) = codificaLiteral p ++ codificaClausula c := by
  simp [codificaClausula, List.append_assoc]

private theorem encF_cons (c : List Lit) (f : List (List Lit)) :
    codificaFormula (c::f) = codificaClausula c ++ codificaFormula f := by
  simp [codificaFormula, List.append_assoc]

private theorem costC_cons (p : Lit) (c : List Lit) :
    clauseCost (p::c) = 4*p.1 + 10 + (codificaLiteral p).length + clauseCost c := by
  simp [clauseCost, encC_cons, Nat.mul_add]
  omega

private theorem costF_cons (c : List Lit) (f : List (List Lit)) :
    formulaCost (c::f) = clauseCost c + formulaCost f := by
  simp [clauseCost, formulaCost, encF_cons, Nat.mul_add]
  omega

private theorem safeTail (c : List Lit) (tail : Word) :
    (codificaClausula c ++ tail).head? ≠ some Simbolo.tick := by
  cases c with
  | nil => simp [codificaClausula]
  | cons p c =>
    rcases p with ⟨i,b⟩
    cases b <;> simp [encC_cons, codificaLiteral]

private def clauseExit (b : Bool) (t : Estado) (i tail : Word) : Config :=
  if b then cfg .lerClausula t i tail [] []
  else cfg .limparFormula (t.1,false,t.2.2) i (.fimC :: tail) [] []

/-- Ao satisfazer a cláusula, a máquina alcança a próxima. Ao esgotá-la,
começa a limpeza com o terminador da cláusula ainda na fita. -/
private theorem clause_run (c : List Lit) (tail : Word) (bs : List Bool) (s : Estado)
    (entry : Rotulo) (he : entry = .lerClausula ∨ entry = .proximoLiteralCheck) :
    ∃ t : Estado, Runs (clauseCost c)
      (cfg entry s (codificaBits bs) (codificaClausula c ++ tail) [] [])
      (clauseExit (c.any (hit bs)) t (codificaBits bs) tail) := by
  induction c generalizing s entry with
  | nil =>
    refine ⟨s, Runs.mono (n := 1) (Runs.one ?_) (by decide)⟩
    change aMaquinaTM2.step (cfg entry s _ (.fimC :: tail) [] []) =
      some (cfg .limparFormula (s.1,false,s.2.2) _ (.fimC :: tail) [] [])
    rcases he with rfl | rfl <;> tmstep
  | cons p c ih =>
    rw [encC_cons, List.append_assoc]
    let state : Estado := (s.1,false,s.2.2)
    have first : Runs 1
        (cfg entry s (codificaBits bs) (codificaLiteral p ++ (codificaClausula c ++ tail)) [] [])
        (cfg .lerLiteral state (codificaBits bs) (codificaLiteral p ++ (codificaClausula c ++ tail)) [] []) := by
      apply Runs.one
      rcases p with ⟨j,b⟩
      rcases he with rfl | rfl <;> cases b <;> simp only [state, codificaLiteral,
        Bool.false_eq_true, ↓reduceIte, List.cons_append] <;> tmstep
    obtain ⟨u, lu⟩ := literal_run p bs (codificaClausula c ++ tail) (safeTail c tail) state
    rw [← show hit bs p = (bs[p.1]? == some p.2) from rfl] at lu
    cases hh : hit bs p with
    | false =>
      simp only [hh, Bool.false_eq_true, ↓reduceIte] at lu
      obtain ⟨t, rest⟩ := ih u .proximoLiteralCheck (Or.inr rfl)
      refine ⟨t, ?_⟩
      simp only [List.any_cons, hh, Bool.false_or]
      apply ((first.trans lu).trans rest).mono
      rw [costC_cons]
      omega
    | true =>
      simp only [hh, ↓reduceIte] at lu
      obtain ⟨t, skip⟩ := skip_run c tail (codificaBits bs) u
      refine ⟨t, ?_⟩
      simp only [List.any_cons, hh, Bool.true_or, clauseExit, ↓reduceIte]
      apply ((first.trans lu).trans skip).mono
      rw [costC_cons]
      unfold clauseCost
      omega

private theorem eval_cons (c : List Lit) (f : List (List Lit)) (bs : List Bool) :
    verificaNaFita (c::f) bs = (c.any (hit bs) && verificaNaFita f bs) := by
  simp only [verificaNaFita, List.all_cons]
  rfl

private theorem formula_run (f : List (List Lit)) (bs : List Bool) (s : Estado) :
    Runs (formulaCost f + ((codificaFormula f).length + bs.length + 3))
      (cfg .lerClausula s (codificaBits bs) (codificaFormula f) [] [])
      (Turing.haltList aMaquinaTM2 [verificaNaFita f bs]) := by
  induction f generalizing s with
  | nil =>
    have first : Runs 1 (cfg .lerClausula s (codificaBits bs) [.fimF] [] [])
        (cfg .limparFormula (s.1,true,s.2.2) (codificaBits bs) [.fimF] [] []) := by
      apply Runs.one
      tmstep
    have last := clean_run s.1 true s.2.2 (codificaBits bs) [.fimF]
    simpa [formulaCost, codificaFormula, codificaBits, verificaNaFita] using first.trans last
  | cons c f ih =>
    obtain ⟨t, seg⟩ := clause_run c (codificaFormula f) bs s .lerClausula (Or.inl rfl)
    rw [eval_cons, encF_cons, costF_cons]
    cases hv : c.any (hit bs) with
    | true =>
      simp only [hv, clauseExit, ↓reduceIte] at seg
      simp only [Bool.true_and]
      apply (seg.trans (ih t)).mono
      simp only [List.length_append]
      omega
    | false =>
      simp only [hv, clauseExit, Bool.false_eq_true, ↓reduceIte] at seg
      simp only [Bool.false_and]
      apply (seg.trans (clean_run t.1 false t.2.2 (codificaBits bs) (.fimC :: codificaFormula f))).mono
      have pos : 1 ≤ (codificaClausula c).length := by simp [codificaClausula]
      simp only [List.length_cons, List.length_append, codificaBits, List.length_map]
      omega

/-- Para toda entrada crua, o TM2 para com o bit do verificador dentro
da soma dos limites de cada fase. -/
theorem simulacao_completa : ASimulacaoCompleta := by
  rintro ⟨f,bs⟩
  obtain ⟨s, pre⟩ := prepare_run f bs
  have whole := pre.trans (formula_run f bs s)
  apply whole.mono
  unfold contaFases formulaCost
  dsimp only
  omega

theorem verificacao_tm2_polinomial : ObjetivoTM2Polinomial :=
  o_objetivo_se_reduz_a_simulacao simulacao_completa

open TGLExt.TraducaoTuring TGLExt.AContagemEACarga TGLExt.AMaquinaEALeitura TGLExt.APonteDeCookLevin

/-- Com uma atribuição fornecida de n bits, a máquina escreve o bit de custo
zero dentro de um polinômio fixo nas letras da fórmula e em n. -/
theorem passos_em_letras_e_bits {n : ℕ} (φ : CNF n) (x : Fin n → Bool) :
    Nonempty (Turing.TM2OutputsInTime aMaquinaTM2
      (codificaEntrada (aFormulaNaFita φ, aAtribuicaoNaFita x))
      (some [decide (custoCNF φ x = 0)]) (20 * ((letras φ + 1) * (n + 1)) + 25)) := by
  let p := (aFormulaNaFita φ, aAtribuicaoNaFita x)
  obtain ⟨run⟩ := simulacao_completa p
  rw [← a_verificacao_na_fita_e_a_da_casa φ x]
  refine ⟨⟨run.toEvalsTo, run.steps_le_m.trans ?_⟩⟩
  have bound := a_forma_do_custo_e_polinomial p
  simp only [Polynomial.eval_add, Polynomial.eval_mul, Polynomial.eval_X, Polynomial.eval_C] at bound
  have len : (codificaEntrada p).length ≤ (letras φ + 1) * (n + 1) + 1 :=
    comprimento_em_letras_e_bits φ x
  omega

end TGLExt.SimTM2

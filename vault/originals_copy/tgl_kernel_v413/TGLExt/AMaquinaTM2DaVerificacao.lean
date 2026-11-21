import TGLExt.APonteAoTM2
set_option autoImplicit false
set_option maxHeartbeats 800000
set_option maxRecDepth 8192

/-!
# Máquina de verificação com saída booleana fixa

A prova geral de simulação é a hipótese explícita do último teorema.
-/

namespace TGLExt.AMaquinaTM2DaVerificacao

open TGLExt.APonteAoTM2
open Turing.TM2.Stmt

/-- [DEF] As cinco pilhas. -/
inductive PilhaK where
  | entrada | saida | formula | trabalho | deposito
  deriving DecidableEq, Fintype

/-- [DEF] Os dezessete rótulos do programa. -/
inductive Rotulo where
  | preparar | reverter | lerClausula | lerLiteral | andarTicks | andarBits | lerBitAtual | comparar
  | esvaziarTicks | restaurar | clausulaSatisfeita | proximoLiteral | saltarResto | proximoLiteralCheck
  | limparFormula | limparEntrada | escrever
  deriving DecidableEq, Fintype

/-- [DEF] O estado: carregador, bandeira, rota. -/
abbrev Estado := Option Simbolo × Bool × Bool

/-- Só a pilha de saída tem alfabeto booleano. -/
abbrev stackAlphabet : PilhaK → Type
  | .saida => Bool
  | _ => Simbolo

/-- [DEF] O programa da máquina (a planta). -/
def oPrograma : Rotulo → Turing.TM2.Stmt stackAlphabet Rotulo Estado
  | .preparar =>
    peek .entrada (fun s h => (s.1, decide (h = some Simbolo.sep), s.2.2))
      (branch (fun s => s.2.1)
        (pop .entrada (fun s _ => s) (goto (fun _ => .reverter)))
        (pop .entrada (fun s h => (h, s.2.1, s.2.2))
          (push .trabalho (fun s => s.1.getD Simbolo.zero) (goto (fun _ => .preparar)))))
  | .reverter =>
    peek .trabalho (fun s h => (s.1, decide (h = none), s.2.2))
      (branch (fun s => s.2.1)
        (goto (fun _ => .lerClausula))
        (pop .trabalho (fun s h => (h, s.2.1, s.2.2))
          (push .formula (fun s => s.1.getD Simbolo.zero) (goto (fun _ => .reverter)))))
  | .lerClausula =>
    peek .formula (fun s h => (s.1, decide (h = some Simbolo.fimF), s.2.2))
      (branch (fun s => s.2.1)
        (goto (fun _ => .limparFormula))
        (peek .formula (fun s h => (s.1, decide (h = some Simbolo.fimC), s.2.2))
          (branch (fun s => s.2.1)
            (load (fun s => (s.1, false, s.2.2)) (goto (fun _ => .limparFormula)))
            (goto (fun _ => .lerLiteral)))))
  | .lerLiteral =>
    pop .formula (fun s h => (s.1, decide (h = some Simbolo.litT), s.2.2)) (goto (fun _ => .andarTicks))
  | .andarTicks =>
    peek .formula (fun s h => (s.1, s.2.1, decide (h = some Simbolo.tick)))
      (branch (fun s => s.2.2)
        (pop .formula (fun s h => (h, s.2.1, s.2.2))
          (push .trabalho (fun s => s.1.getD Simbolo.tick) (goto (fun _ => .andarTicks))))
        (goto (fun _ => .andarBits)))
  | .andarBits =>
    peek .trabalho (fun s h => (s.1, s.2.1, decide (h = none)))
      (branch (fun s => s.2.2)
        (goto (fun _ => .lerBitAtual))
        (peek .entrada (fun s h => (s.1, s.2.1, decide (h = none)))
          (branch (fun s => s.2.2)
            (goto (fun _ => .esvaziarTicks))
            (pop .trabalho (fun s _ => s)
              (pop .entrada (fun s h => (h, s.2.1, s.2.2))
                (push .deposito (fun s => s.1.getD Simbolo.zero) (goto (fun _ => .andarBits))))))))
  | .lerBitAtual =>
    peek .entrada (fun s h => (h, s.2.1, s.2.2)) (goto (fun _ => .comparar))
  | .esvaziarTicks =>
    peek .trabalho (fun s h => (s.1, s.2.1, decide (h = none)))
      (branch (fun s => s.2.2)
        (load (fun s => (none, s.2.1, s.2.2)) (goto (fun _ => .comparar)))
        (pop .trabalho (fun s _ => s) (goto (fun _ => .esvaziarTicks))))
  | .comparar =>
    load (fun s => (none, decide (s.1 = if s.2.1 then some Simbolo.um else some Simbolo.zero), s.2.2))
      (branch (fun s => s.2.1)
        (goto (fun _ => .clausulaSatisfeita))
        (goto (fun _ => .proximoLiteral)))
  | .clausulaSatisfeita =>
    load (fun s => (s.1, s.2.1, true)) (goto (fun _ => .restaurar))
  | .proximoLiteral =>
    load (fun s => (s.1, s.2.1, false)) (goto (fun _ => .restaurar))
  | .restaurar =>
    peek .deposito (fun s h => (s.1, decide (h = none), s.2.2))
      (branch (fun s => s.2.1)
        (goto (fun s => if s.2.2 then .saltarResto else .proximoLiteralCheck))
        (pop .deposito (fun s h => (h, s.2.1, s.2.2))
          (push .entrada (fun s => s.1.getD Simbolo.zero) (goto (fun _ => .restaurar)))))
  | .saltarResto =>
    peek .formula (fun s h => (s.1, decide (h = some Simbolo.fimC), s.2.2))
      (branch (fun s => s.2.1)
        (pop .formula (fun s _ => s) (goto (fun _ => .lerClausula)))
        (pop .formula (fun s _ => s) (goto (fun _ => .saltarResto))))
  | .proximoLiteralCheck =>
    peek .formula (fun s h => (s.1, decide (h = some Simbolo.fimC), s.2.2))
      (branch (fun s => s.2.1)
        (load (fun s => (s.1, false, s.2.2)) (goto (fun _ => .limparFormula)))
        (goto (fun _ => .lerLiteral)))
  | .limparFormula =>
    peek .formula (fun s h => (s.1, s.2.1, decide (h = none)))
      (branch (fun s => s.2.2)
        (goto (fun _ => .limparEntrada))
        (pop .formula (fun s _ => s) (goto (fun _ => .limparFormula))))
  | .limparEntrada =>
    peek .entrada (fun s h => (s.1, s.2.1, decide (h = none)))
      (branch (fun s => s.2.2)
        (goto (fun _ => .escrever))
        (pop .entrada (fun s _ => s) (goto (fun _ => .limparEntrada))))
  | .escrever =>
    push .saida (fun s => s.2.1)
      (load (fun _ => (none, false, false)) halt)

/-- [DEF] A máquina: a planta fechada em `FinTM2` — o modelo padrão do Mathlib. -/
def aMaquinaTM2 : Turing.FinTM2 where
  K := PilhaK
  k₀ := PilhaK.entrada
  k₁ := PilhaK.saida
  Γ := stackAlphabet
  Γk₀Fin := inferInstanceAs (Fintype Simbolo)
  Λ := Rotulo
  main := Rotulo.preparar
  σ := Estado
  initialState := (none, false, false)
  m := oPrograma

/-- [DEF] A contabilidade honesta, fase a fase (a estimativa de passos conforme a planta): preparação e
reversão (`2·(Lf+1)`); por literal, marcador + ticks + caminhada + esvaziamento + leitura + comparação + rota
+ restaurar + conferência (`4·S + 10·#lit` no pior caso); o saltar das cláusulas satisfeitas e os terminadores
(`Lf + m`); as limpezas finais e a escrita (`Lf + B + 3`). -/
def contaFases (p : List (List (ℕ × Bool)) × List Bool) : ℕ :=
  2 * ((codificaFormula p.1).length + 1)
    + (4 * (p.1.flatten.map Prod.fst).sum + 10 * p.1.flatten.length)
    + ((codificaFormula p.1).length + p.1.length)
    + ((codificaFormula p.1).length + p.2.length + 3)

/-- ★ **A FORMA DO CUSTO É POLINOMIAL** — linear no comprimento da entrada: a contabilidade por fase fica
abaixo de `20·L + 5`. Com os índices em unário, cada tick da fórmula paga uma caminhada da máquina: a fórmula
financia a própria travessia, e o custo não esconde nada exponencial. -/
theorem a_forma_do_custo_e_polinomial (p : List (List (ℕ × Bool)) × List Bool) :
    contaFases p ≤ (Polynomial.C 20 * Polynomial.X + Polynomial.C 5).eval ((codificaEntrada p).length) := by
  have hf : (codificaFormula p.1).length =
      (p.1.flatten.map Prod.fst).sum + p.1.flatten.length + p.1.length + 1 := by
    have he := comprimento_exato p.1 []
    simp only [codificaEntrada, codificaBits, List.map_nil, List.append_nil, List.length_append,
      List.length_singleton, List.length_nil, Nat.add_zero] at he
    omega
  have he := comprimento_exato p.1 p.2
  simp only [contaFases, hf, Polynomial.eval_add, Polynomial.eval_mul,
    Polynomial.eval_X, Polynomial.eval_C]
  change (codificaEntrada p).length = _ at he
  omega

/-- A resposta da casa para a fórmula vazia é o sim. (Auxiliar da âncora.) -/
theorem a_resposta_da_formula_vazia : verificaNaFita [] [] = true := rfl


private abbrev Configuration := Turing.TM2.Cfg stackAlphabet Rotulo Estado

private structure Observed where
  label : Option Rotulo
  state : Estado
  input : List Simbolo
  output : List Bool
  formula : List Simbolo
  work : List Simbolo
  saved : List Simbolo
  deriving DecidableEq

private def contents (c : Configuration) : Observed :=
  ⟨c.l, c.var, c.stk .entrada, c.stk .saida, c.stk .formula, c.stk .trabalho, c.stk .deposito⟩

private theorem contents_injective : Function.Injective contents := by
  intro a b h
  simp only [contents, Observed.mk.injEq] at h
  obtain ⟨hl, hv, hi, ho, hf, hw, hd⟩ := h
  have hs : a.stk = b.stk := funext fun k => by cases k <;> assumption
  cases a
  cases b
  exact (Turing.TM2.Cfg.mk.injEq ..).mpr ⟨hl, hv, hs⟩

private instance : DecidableEq aMaquinaTM2.Cfg := fun a b =>
  decidable_of_iff (contents a = contents b) ⟨fun he => contents_injective he, congrArg contents⟩

/-- Nove aplicações do passo da Mathlib sobre a fita da fórmula vazia. -/
def a_maquina_roda_a_formula_vazia :
    Turing.TM2OutputsInTime aMaquinaTM2 (codificaEntrada ([], [])) (some [true]) 9 := by
  refine ⟨⟨9, ?_⟩, le_rfl⟩
  decide

/-- Mesmo literal de índice 1, duas testemunhas. A segunda célula decide a saída. -/
def testemunha_positiva :
    Turing.TM2OutputsInTime aMaquinaTM2 (codificaEntrada ([[(1,true)]], [false,true]))
      (some [true]) 29 := by
  refine ⟨⟨29, ?_⟩, le_rfl⟩
  decide

def testemunha_negativa :
    Turing.TM2OutputsInTime aMaquinaTM2 (codificaEntrada ([[(1,true)]], [false,false]))
      (some [false]) 29 := by
  refine ⟨⟨29, ?_⟩, le_rfl⟩
  decide

/-- A obrigação geral refere-se a esta máquina e a todas as entradas cruas. -/
def ASimulacaoCompleta : Prop :=
  ∀ p : List (List (ℕ × Bool)) × List Bool,
    Nonempty (Turing.TM2OutputsInTime aMaquinaTM2 (codificaEntrada p)
      (some (codificaSaida (verificaNaFita p.1 p.2))) (contaFases p))

/-- A simulação geral, se demonstrada, fornece a máquina exigida por `ObjetivoTM2Polinomial`. -/
theorem o_objetivo_se_reduz_a_simulacao (h : ASimulacaoCompleta) : ObjetivoTM2Polinomial := by
  classical
  refine ⟨{ tm := aMaquinaTM2, inputAlphabet := Equiv.refl _, outputAlphabet := Equiv.refl _,
            time := Polynomial.C 20 * Polynomial.X + Polynomial.C 5, outputsFun := ?_ }⟩
  intro p
  have hp := (h p).some
  change Turing.TM2OutputsInTime aMaquinaTM2 ((codificaEntrada p).map id)
    (some ((codificaSaida (verificaNaFita p.1 p.2)).map id)) _
  simp only [List.map_id]
  exact (show Turing.TM2OutputsInTime aMaquinaTM2 (codificaEntrada p)
    (some (codificaSaida (verificaNaFita p.1 p.2)))
    ((Polynomial.C 20 * Polynomial.X + Polynomial.C 5).eval (codificaEntrada p).length) from
    ⟨hp.toEvalsTo, hp.steps_le_m.trans (a_forma_do_custo_e_polinomial p)⟩)

end TGLExt.AMaquinaTM2DaVerificacao

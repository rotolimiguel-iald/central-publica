import TGLExt.SimBase
set_option autoImplicit false

namespace TGLExt.SimTM2

open TGLExt.APonteAoTM2 TGLExt.AMaquinaTM2DaVerificacao

private abbrev Tape := List Simbolo
private abbrev Ticks (i : ℕ) := List.replicate i Simbolo.tick
private abbrev bitSymbol (b : Bool) : Simbolo := if b then .um else .zero
private abbrev nextLabel (answer : Bool) : Rotulo :=
  if answer then .saltarResto else .proximoLiteralCheck
private abbrev branchLabel (answer : Bool) : Rotulo :=
  if answer then .clausulaSatisfeita else .proximoLiteral

private theorem sameLiteralTapes (l : Option Rotulo) (v : Estado)
    (a b : (k : PilhaK) → List (stackAlphabet k)) (h : ∀ k, a k = b k) :
    some (⟨l, v, a⟩ : Config) = some (⟨l, v, b⟩ : Config) := by rw [funext h]

local macro "litstep" : tactic =>
  `(tactic| (simp [Ticks, bitSymbol, nextLabel, branchLabel, codificaBits, codificaLiteral,
      Turing.FinTM2.step, Turing.TM2.step, aMaquinaTM2, cfg, oPrograma, Turing.TM2.stepAux,
      *] <;> refine sameLiteralTapes _ _ _ _ (fun k => ?_) <;> cases k <;> rfl))

/-- Passa todos os ticks do literal para a pilha de trabalho. O primeiro símbolo
da continuação é preservado, mesmo quando a continuação é vazia. -/
private theorem moveTicks (i a : ℕ) (tail input : Tape)
    (safe : tail.head? ≠ some Simbolo.tick) (h : Option Simbolo) (pol route : Bool) :
    ∃ h', Runs (i+1)
      (cfg .andarTicks (h,pol,route) input (Ticks i ++ tail) (Ticks a) [])
      (cfg .andarBits (h',pol,false) input tail (Ticks (a+i)) []) := by
  induction i generalizing a h route with
  | zero =>
    refine ⟨h, Runs.one ?_⟩
    simp only [Nat.add_zero, List.replicate_zero, List.nil_append]
    litstep
  | succ i ih =>
    have first : Runs 1
        (cfg .andarTicks (h,pol,route) input (Ticks (i+1) ++ tail) (Ticks a) [])
        (cfg .andarTicks (some .tick,pol,true) input (Ticks i ++ tail) (Ticks (a+1)) []) := by
      apply Runs.one
      simp only [Ticks, List.replicate_succ, List.cons_append]
      litstep
    obtain ⟨h', rest⟩ := ih (a+1) (some .tick) true
    refine ⟨h', ?_⟩
    simpa only [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using first.trans rest

/-- Os bits salvos formam uma pilha em ordem inversa. Restaurá-la devolve os
bits à testemunha e deixa o depósito vazio antes de saltar. -/
private theorem restoreBits (saved input tail : Tape) (h : Option Simbolo) (flag ok : Bool) :
    ∃ t, Runs (saved.length+1)
      (cfg .restaurar (h,flag,ok) input tail [] saved)
      (cfg (nextLabel ok) t (saved.reverse ++ input) tail [] []) := by
  induction saved generalizing input h flag with
  | nil =>
    refine ⟨(h,true,ok), Runs.one ?_⟩
    cases ok <;> litstep
  | cons a saved ih =>
    have first : Runs 1
        (cfg .restaurar (h,flag,ok) input tail [] (a::saved))
        (cfg .restaurar (some a,false,ok) (a::input) tail [] saved) := by
      apply Runs.one
      litstep
    obtain ⟨t, rest⟩ := ih (a::input) (some a) false
    refine ⟨t, ?_⟩
    simpa [List.reverse_cons, List.append_assoc, Nat.add_comm, Nat.add_left_comm, Nat.add_assoc]
      using first.trans rest

private theorem compareBit (found : Option Bool) (pol route : Bool) (saved input tail : Tape) :
    ∃ t, Runs (saved.length+3)
      (cfg .comparar (found.map bitSymbol,pol,route) input tail [] saved)
      (cfg (nextLabel (found == some pol)) t (saved.reverse ++ input) tail [] []) := by
  let ok := found == some pol
  have first : Runs 1
      (cfg .comparar (found.map bitSymbol,pol,route) input tail [] saved)
      (cfg (branchLabel ok) (none,ok,route) input tail [] saved) := by
    apply Runs.one
    dsimp only [ok]
    cases found with
    | none => cases pol <;> litstep
    | some b => cases b <;> cases pol <;> litstep
  have middle (q : Bool) : Runs 1
      (cfg (branchLabel q) (none,q,route) input tail [] saved)
      (cfg .restaurar (none,q,q) input tail [] saved) := by
    apply Runs.one
    cases q <;> litstep
  obtain ⟨t, rest⟩ := restoreBits saved input tail none ok ok
  exact ⟨t, ((first.trans (middle ok)).trans rest).mono (by omega)⟩

/-- Se a testemunha acabar cedo, a máquina consome o índice restante e compara
com none. Nenhuma polaridade satisfaz um literal cujo bit está ausente. -/
private theorem discardTicks (i : ℕ) (tail saved : Tape) (h : Option Simbolo) (pol route : Bool) :
    Runs (i+1) (cfg .esvaziarTicks (h,pol,route) [] tail (Ticks i) saved)
      (cfg .comparar (none,pol,true) [] tail [] saved) := by
  induction i generalizing h route with
  | zero => apply Runs.one; litstep
  | succ i ih =>
    have first : Runs 1
        (cfg .esvaziarTicks (h,pol,route) [] tail (Ticks (i+1)) saved)
        (cfg .esvaziarTicks (h,pol,false) [] tail (Ticks i) saved) := by
      apply Runs.one
      rw [show Ticks (i+1) = .tick :: Ticks i from List.replicate_succ]
      litstep
    exact (first.trans (ih h false)).mono (by omega)

private theorem lookupBit (i : ℕ) (bs : List Bool) (saved tail : Tape)
    (h : Option Simbolo) (pol route : Bool) :
    ∃ t, Runs (2*i + saved.length + 6)
      (cfg .andarBits (h,pol,route) (codificaBits bs) tail (Ticks i) saved)
      (cfg (nextLabel (bs[i]? == some pol)) t (saved.reverse ++ codificaBits bs) tail [] []) := by
  induction i generalizing bs saved h route with
  | zero =>
    have first : Runs 1
        (cfg .andarBits (h,pol,route) (codificaBits bs) tail [] saved)
        (cfg .lerBitAtual (h,pol,true) (codificaBits bs) tail [] saved) := by
      apply Runs.one; litstep
    have second : Runs 1
        (cfg .lerBitAtual (h,pol,true) (codificaBits bs) tail [] saved)
        (cfg .comparar (bs[0]?.map bitSymbol,pol,true) (codificaBits bs) tail [] saved) := by
      apply Runs.one
      cases bs <;> litstep
    obtain ⟨t, rest⟩ := compareBit bs[0]? pol true saved (codificaBits bs) tail
    exact ⟨t, ((first.trans second).trans rest).mono (by omega)⟩
  | succ i ih =>
    cases bs with
    | nil =>
      have first : Runs 1
          (cfg .andarBits (h,pol,route) [] tail (Ticks (i+1)) saved)
          (cfg .esvaziarTicks (h,pol,true) [] tail (Ticks (i+1)) saved) := by
        apply Runs.one
        rw [show Ticks (i+1) = .tick :: Ticks i from List.replicate_succ]
        litstep
      have drain := discardTicks (i+1) tail saved h pol true
      obtain ⟨t, rest⟩ := compareBit none pol true saved [] tail
      refine ⟨t, ?_⟩
      simpa only [List.getElem?_nil, codificaBits, List.map_nil] using
        ((first.trans drain).trans rest).mono (show 1 + (i+1+1) + (saved.length+3) ≤
          2*(i+1) + saved.length + 6 by omega)
    | cons b bs =>
      have first : Runs 1
          (cfg .andarBits (h,pol,route) (codificaBits (b::bs)) tail (Ticks (i+1)) saved)
          (cfg .andarBits (some (bitSymbol b),pol,false) (codificaBits bs) tail
            (Ticks i) (bitSymbol b :: saved)) := by
        apply Runs.one
        rw [show Ticks (i+1) = .tick :: Ticks i from List.replicate_succ]
        litstep
      obtain ⟨t, rest⟩ := ih bs (bitSymbol b :: saved) (some (bitSymbol b)) false
      refine ⟨t, ?_⟩
      have walk := (first.trans rest).mono (show
        1 + (2*i + (bitSymbol b :: saved).length + 6) ≤ 2*(i+1) + saved.length + 6 by
          simp only [List.length_cons]; omega)
      simpa [List.reverse_cons, List.append_assoc, codificaBits] using walk

/-- Uma leitura real do TM2 verifica o literal, consome somente sua codificação
e restitui a testemunha inteira, também para índices fora da fita. -/
theorem literal_run (p : ℕ × Bool) (bs : List Bool) (tail : List Simbolo)
    (safe : tail.head? ≠ some Simbolo.tick) (s : Estado) :
    ∃ t : Estado, Runs (4*p.1+9)
      (cfg .lerLiteral s (codificaBits bs) (codificaLiteral p ++ tail) [] [])
      (cfg (if (bs[p.1]? == some p.2) then .saltarResto else .proximoLiteralCheck)
        t (codificaBits bs) tail [] []) := by
  rcases p with ⟨i, pol⟩
  have first : Runs 1
      (cfg .lerLiteral s (codificaBits bs) (codificaLiteral (i,pol) ++ tail) [] [])
      (cfg .andarTicks (s.1,pol,s.2.2) (codificaBits bs) (Ticks i ++ tail) [] []) := by
    apply Runs.one
    cases pol <;> litstep
  obtain ⟨h, ticks⟩ := moveTicks i 0 tail (codificaBits bs) safe s.1 pol s.2.2
  rw [Nat.zero_add] at ticks
  obtain ⟨t, rest⟩ := lookupBit i bs [] tail h pol false
  refine ⟨t, ?_⟩
  exact ((first.trans ticks).trans rest).mono (by simp; omega)

end TGLExt.SimTM2

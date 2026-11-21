import TGLExt.SimBase
set_option autoImplicit false
set_option maxHeartbeats 800000
set_option maxRecDepth 8192

namespace TGLExt.SimTM2

open TGLExt.APonteAoTM2 TGLExt.AMaquinaTM2DaVerificacao

private theorem same_tapes (l : Option Rotulo) (v : Estado)
    (a b : (k : PilhaK) → List (stackAlphabet k)) (h : ∀ k, a k = b k) :
    some (⟨l, v, a⟩ : Config) = some (⟨l, v, b⟩ : Config) := by rw [funext h]

local macro "exterior_step" : tactic =>
  `(tactic| (tmstep <;> refine same_tapes _ _ _ _ (fun k => ?_) <;> cases k <;> rfl))

/-- Os marcadores de polaridade e os ticks de um literal não contêm delimitadores. -/
private theorem literal_avoids (p : ℕ × Bool) (stop : Simbolo)
    (ht : Simbolo.tick ≠ stop) (hp : Simbolo.litT ≠ stop) (hn : Simbolo.litF ≠ stop) :
    stop ∉ codificaLiteral p := by
  rcases p with ⟨j, b⟩
  cases b <;> simp_all [codificaLiteral, List.mem_replicate, eq_comm]

private theorem no_end_inside (c : List (ℕ × Bool)) :
    Simbolo.fimC ∉ c.flatMap codificaLiteral := by
  intro h
  obtain ⟨p, _, h⟩ := List.mem_flatMap.mp h
  exact literal_avoids p .fimC (by decide) (by decide) (by decide) h

private theorem no_separator (f : List (List (ℕ × Bool))) :
    Simbolo.sep ∉ codificaFormula f := by
  intro h
  simp only [codificaFormula, List.mem_append, List.mem_singleton] at h
  rcases h with h | h
  · obtain ⟨c, _, h⟩ := List.mem_flatMap.mp h
    simp only [codificaClausula, List.mem_append, List.mem_singleton] at h
    rcases h with h | h
    · obtain ⟨p, _, h⟩ := List.mem_flatMap.mp h
      exact literal_avoids p .sep (by decide) (by decide) (by decide) h
    · cases h
  · cases h

/-- Leitura até a divisória. O prefixo consumido fica invertido na pilha de trabalho. -/
private theorem load_prefix (xs work bits : List Simbolo) (s : Estado)
    (guard : Simbolo.sep ∉ xs) :
    ∃ t : Estado, Runs (xs.length + 1)
      (cfg .preparar s (xs ++ .sep :: bits) [] work [])
      (cfg .reverter t bits [] (xs.reverse ++ work) []) := by
  induction xs generalizing work s with
  | nil =>
    refine ⟨(s.1,true,s.2.2), ?_⟩
    apply Runs.one
    exterior_step
  | cons a xs ih =>
    have ha : a ≠ Simbolo.sep := by
      intro h
      subst a
      exact guard List.mem_cons_self
    have ht : Simbolo.sep ∉ xs := fun h => guard (List.mem_cons_of_mem _ h)
    have st : Runs 1 (cfg .preparar s ((a :: xs) ++ .sep :: bits) [] work [])
        (cfg .preparar (some a,false,s.2.2) (xs ++ .sep :: bits) [] (a :: work) []) := by
      apply Runs.one
      cases a <;> first | contradiction | exterior_step
    obtain ⟨t, tail⟩ := ih (a :: work) (some a,false,s.2.2) ht
    refine ⟨t, ?_⟩
    simpa [List.reverse_cons, List.append_assoc, Nat.add_comm, Nat.add_left_comm,
      Nat.add_assoc] using st.trans tail

/-- A segunda transferência restaura a ordem de todas as letras da fórmula. -/
private theorem reverse_work (work form bits : List Simbolo) (s : Estado) :
    ∃ t : Estado, Runs (work.length + 1)
      (cfg .reverter s bits form work [])
      (cfg .lerClausula t bits (work.reverse ++ form) [] []) := by
  induction work generalizing form s with
  | nil =>
    refine ⟨(s.1,true,s.2.2), ?_⟩
    apply Runs.one
    exterior_step
  | cons a work ih =>
    have st : Runs 1 (cfg .reverter s bits form (a :: work) [])
        (cfg .reverter (some a,false,s.2.2) bits (a :: form) work []) := by
      apply Runs.one
      exterior_step
    obtain ⟨t, tail⟩ := ih (a :: form) (some a,false,s.2.2)
    refine ⟨t, ?_⟩
    simpa [List.reverse_cons, List.append_assoc, Nat.add_comm, Nat.add_left_comm,
      Nat.add_assoc] using st.trans tail

private theorem initial_cfg (input : List Simbolo) :
    Turing.initList aMaquinaTM2 input = cfg .preparar (none,false,false) input [] [] [] := by
  apply (Turing.TM2.Cfg.mk.injEq ..).mpr
  refine ⟨rfl, rfl, ?_⟩
  funext k
  cases k <;> rfl

theorem prepare_run (f : List (List (ℕ × Bool))) (bs : List Bool) :
    ∃ t : Estado, Runs (2*((codificaFormula f).length+1))
      (Turing.initList aMaquinaTM2 (codificaEntrada (f,bs)))
      (cfg .lerClausula t (codificaBits bs) (codificaFormula f) [] []) := by
  rw [initial_cfg]
  obtain ⟨s, hs⟩ := load_prefix (codificaFormula f) [] (codificaBits bs)
    (none,false,false) (no_separator f)
  simp only [List.append_nil] at hs
  obtain ⟨t, ht⟩ := reverse_work (codificaFormula f).reverse [] (codificaBits bs) s
  refine ⟨t, ?_⟩
  simpa [codificaEntrada, List.append_assoc, two_mul] using hs.trans ht

/-- Elimina as letras até o fim da cláusula, consumindo também o terminador. -/
private theorem skip_prefix (xs tail i : List Simbolo) (s : Estado)
    (guard : Simbolo.fimC ∉ xs) :
    ∃ t : Estado, Runs (xs.length + 1)
      (cfg .saltarResto s i (xs ++ .fimC :: tail) [] [])
      (cfg .lerClausula t i tail [] []) := by
  induction xs generalizing s with
  | nil =>
    refine ⟨(s.1,true,s.2.2), ?_⟩
    apply Runs.one
    exterior_step
  | cons a xs ih =>
    have ha : a ≠ Simbolo.fimC := by
      intro h
      subst a
      exact guard List.mem_cons_self
    have ht : Simbolo.fimC ∉ xs := fun h => guard (List.mem_cons_of_mem _ h)
    have st : Runs 1 (cfg .saltarResto s i ((a :: xs) ++ .fimC :: tail) [] [])
        (cfg .saltarResto (s.1,false,s.2.2) i (xs ++ .fimC :: tail) [] []) := by
      apply Runs.one
      cases a <;> first | contradiction | exterior_step
    obtain ⟨t, tailRun⟩ := ih (s.1,false,s.2.2) ht
    exact ⟨t, (st.trans tailRun).mono (by simp; omega)⟩

theorem skip_run (c : List (ℕ × Bool)) (tail i : List Simbolo) (s : Estado) :
    ∃ t : Estado, Runs (codificaClausula c).length
      (cfg .saltarResto s i (codificaClausula c ++ tail) [] [])
      (cfg .lerClausula t i tail [] []) := by
  simpa [codificaClausula, List.append_assoc] using
    skip_prefix (c.flatMap codificaLiteral) tail i s (no_end_inside c)

private theorem halt_cfg (b : Bool) :
    Turing.haltList aMaquinaTM2 [b] =
      (⟨none,(none,false,false),tapes [] [] [] [] [b]⟩ : Config) := by
  apply (Turing.TM2.Cfg.mk.injEq ..).mpr
  refine ⟨rfl, rfl, ?_⟩
  funext k
  cases k <;> rfl

/-- Esvaziar a entrada conserva o resultado e termina com todas as pilhas auxiliares vazias. -/
private theorem clean_input (v : Option Simbolo) (b r : Bool) (i : List Simbolo) :
    Runs (i.length+2) (cfg .limparEntrada (v,b,r) i [] [] [])
      (Turing.haltList aMaquinaTM2 [b]) := by
  induction i generalizing r with
  | nil =>
    have s₁ : Runs 1 (cfg .limparEntrada (v,b,r) [] [] [] [])
        (cfg .escrever (v,b,true) [] [] [] []) := by
      apply Runs.one
      exterior_step
    have s₂ : Runs 1 (cfg .escrever (v,b,true) [] [] [] [])
        (Turing.haltList aMaquinaTM2 [b]) := by
      apply Runs.one
      rw [halt_cfg]
      exterior_step
    exact s₁.trans s₂
  | cons a i ih =>
    have st : Runs 1 (cfg .limparEntrada (v,b,r) (a::i) [] [] [])
        (cfg .limparEntrada (v,b,false) i [] [] []) := by
      apply Runs.one
      exterior_step
    exact (st.trans (ih false)).mono (by simp; omega)

theorem clean_run (v : Option Simbolo) (b r : Bool) (i f : List Simbolo) :
    Runs (f.length+i.length+3) (cfg .limparFormula (v,b,r) i f [] [])
      (Turing.haltList aMaquinaTM2 [b]) := by
  induction f generalizing r with
  | nil =>
    have st : Runs 1 (cfg .limparFormula (v,b,r) i [] [] [])
        (cfg .limparEntrada (v,b,true) i [] [] []) := by
      apply Runs.one
      exterior_step
    exact (st.trans (clean_input v b true i)).mono (by simp; omega)
  | cons a f ih =>
    have st : Runs 1 (cfg .limparFormula (v,b,r) i (a::f) [] [])
        (cfg .limparFormula (v,b,false) i f [] []) := by
      apply Runs.one
      exterior_step
    exact (st.trans (ih false)).mono (by simp; omega)

end TGLExt.SimTM2

import CopiadorEImpostor

set_option autoImplicit false
noncomputable section

/-! Sonda mínima do revisor T1 (16/11/2026): o grupo 2 × 2 do desenho R6. Nada instalado; nomes provisórios. -/

namespace TGLExt.CopiadorEImpostor.SondaT1Min

variable {X V : Type}

theorem confereB_sim {ρ : X → V} {p : X × X} (h : ρ p.1 = ρ p.2) : confereB ρ p = true :=
  (confereB_sim_sse ρ p).mpr h

theorem confereB_nao {ρ : X → V} {p : X × X} (h : ρ p.1 ≠ ρ p.2) : confereB ρ p = false := by
  cases hb : confereB ρ p with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ p).mp hb) h

/-- O grupo 2 × 2: duas páginas (`x0`, `x1`) e dois assentos (`r0`, `r1`), as quatro combinações. -/
def grupo (x0 x1 r0 r1 : X) : Set (X × X) := {p | (p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)}

/-- Três casas: falta a casa (página mexida, assento mexido). -/
def tresCasas (x0 x1 r0 r1 : X) : Set (X × X) := {p | p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)}

theorem mem_grupo {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ grupo x0 x1 r0 r1 ↔ ((p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)) := Iff.rfl

theorem mem_tresCasas {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ tresCasas x0 x1 r0 r1 ↔ (p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)) := Iff.rfl

variable (ρ : X → V) {x0 x1 r0 r1 : X}

/-- No grupo 2 × 2, quem acerta os quatro casos não é função só da página nem só do registro. (Juiz que não
sorteia; tudo ou nada. Só usa três das quatro casas.) -/
theorem no_grupo_quem_acerta_os_quatro_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool) (hI : ImprimeEm (confereB ρ) I (grupo x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  have e00 : I (x0, r0) = true :=
    (hI _ (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)).trans (confereB_sim (p := (x0, r0)) h0)
  have e01 : I (x0, r1) = false :=
    (hI _ (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)).trans
      (confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm)))
  have e10 : I (x1, r0) = false :=
    (hI _ (mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩)).trans
      (confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm)))
  constructor
  · intro hp
    have e := hp (x0, r0) (x0, r1) rfl
    rw [e00, e01] at e
    exact absurd e (by decide)
  · intro hp
    have e := hp (x0, r0) (x1, r0) rfl
    rw [e00, e10] at e
    exact absurd e (by decide)

open Classical in
/-- AS TRÊS CASAS NÃO BASTAM: nelas passa o juiz que confere a página com o original, confere o assento com o
original, e diz que bate quando os dois conferem. Usa os dois lados e não os compara. -/
theorem nas_tres_casas_passa_quem_confere_cada_lado_com_o_original (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) :
    ∃ f g : X → Bool,
      ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (tresCasas x0 x1 r0 r1) := by
  refine ⟨fun x => decide (ρ x = ρ x0), fun r => decide (ρ r = ρ x0), ?_⟩
  intro p hp
  rcases mem_tresCasas.mp hp with rfl | rfl | rfl
  · have hc : confereB ρ (x0, r0) = true := confereB_sim (p := (x0, r0)) h0
    simp [hc, h0.symm]
  · have hc : confereB ρ (x0, r1) = false :=
      confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm))
    have hn : ¬ ρ r1 = ρ x0 := fun h => hne (h.symm.trans h1.symm)
    simp [hc, hn]
  · have hc : confereB ρ (x1, r0) = false :=
      confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm))
    have hn : ¬ ρ x1 = ρ x0 := fun h => hne h.symm
    simp [hc, hn]

/-- A QUARTA CASA: no grupo inteiro nenhum juiz da forma “a página confere E o assento confere” passa. -/
theorem no_grupo_nenhum_juiz_de_dois_selos_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 && g r0) = true :=
    (h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)).trans (confereB_sim (p := (x0, r0)) h0)
  have e11 : (f x1 && g r1) = true :=
    (h (x1, r1) (mem_grupo.mpr ⟨Or.inr rfl, Or.inr rfl⟩)).trans (confereB_sim (p := (x1, r1)) h1)
  have e01 : (f x0 && g r1) = false :=
    (h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)).trans
      (confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm)))
  revert e00 e11 e01
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-- CASAR LETRA COM LETRA PASSA, SE A LETRA DENUNCIA: se uma marca `s` da letra acompanha o estado nos dois lados
dentro do grupo, o juiz que só compara a marca da página com a do assento acerta as quatro casas. -/
theorem no_grupo_passa_quem_casa_uma_marca_da_letra (s : X → Bool) (h0 : ρ x0 = ρ r0)
    (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) (hs0 : s x0 = s r0) (hs1 : s x1 = s r1)
    (hsne : s x0 ≠ s x1) :
    ImprimeEm (confereB ρ) (fun p : X × X => s p.1 == s p.2) (grupo x0 x1 r0 r1) := by
  have c00 : (s x0 == s r0) = confereB ρ (x0, r0) := by
    rw [confereB_sim (p := (x0, r0)) h0, hs0]
    cases s r0 <;> decide
  have c11 : (s x1 == s r1) = confereB ρ (x1, r1) := by
    rw [confereB_sim (p := (x1, r1)) h1, hs1]
    cases s r1 <;> decide
  have c01 : (s x0 == s r1) = confereB ρ (x0, r1) := by
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm)), ← hs1]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  have c10 : (s x1 == s r0) = confereB ρ (x1, r0) := by
    rw [confereB_nao (p := (x1, r0)) (fun hh => hne (h0.trans hh.symm)), ← hs0]
    revert hsne
    cases s x0 <;> cases s x1 <;> decide
  rintro ⟨a, b⟩ hp
  obtain ⟨ha, hb⟩ := mem_grupo.mp hp
  have ha' : a = x0 ∨ a = x1 := ha
  have hb' : b = r0 ∨ b = r1 := hb
  rcases ha' with ha' | ha' <;> rcases hb' with hb' | hb' <;> rw [ha', hb']
  · exact c00
  · exact c01
  · exact c10
  · exact c11

end TGLExt.CopiadorEImpostor.SondaT1Min

#print axioms TGLExt.CopiadorEImpostor.SondaT1Min.no_grupo_quem_acerta_os_quatro_usa_os_dois_lados
#print axioms TGLExt.CopiadorEImpostor.SondaT1Min.nas_tres_casas_passa_quem_confere_cada_lado_com_o_original
#print axioms TGLExt.CopiadorEImpostor.SondaT1Min.no_grupo_nenhum_juiz_de_dois_selos_passa
#print axioms TGLExt.CopiadorEImpostor.SondaT1Min.no_grupo_passa_quem_casa_uma_marca_da_letra

import CopiadorEImpostor

/-!
SONDA da gerência c1 (16/11/2026), para a seção nova da candidata `CopiadorEImpostor` (ainda não incorporada).

No grupo 2 × 2 do teste (a página `a` ou `b`, contra o registro `a` ou `b`, de sentidos diferentes):
* todo juiz que só vê a página acerta EXATAMENTE dois dos quatro casos;
* todo juiz que só vê o registro acerta EXATAMENTE dois dos quatro casos;
* o juízo pelo par acerta os quatro;
* logo quem acerta os quatro não é função só da página nem só do registro.
-/

namespace TGLExt.CopiadorEImpostor

section metade

variable {X V : Type}

/-- Os quatro casos do grupo: (página, registro). -/
def casosDoGrupo (a b : X) : List (X × X) := [(a, a), (a, b), (b, a), (b, b)]

/-- Quantos casos da lista o juiz `I` acerta (a resposta certa é `confereB ρ`). -/
noncomputable def acertos (ρ : X → V) (I : X × X → Bool) (L : List (X × X)) : ℕ :=
  L.countP (fun p => I p == confereB ρ p)

theorem confereB_mesmo (ρ : X → V) (a : X) : confereB ρ (a, a) = true :=
  (confereB_sim_sse ρ (a, a)).mpr (show ρ a = ρ a from rfl)

theorem confereB_outro (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b) : confereB ρ (a, b) = false := by
  cases h : confereB ρ (a, b) with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ (a, b)).mp h) hab

/-- ★ **UM LADO SÓ ACERTA EXATAMENTE A METADE (a página).** -/
theorem quem_so_ve_a_pagina_acerta_exatamente_a_metade (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (hI : PagouSo (Prod.fst : X × X → X) I) :
    acertos ρ I (casosDoGrupo a b) = 2 := by
  have e1 : I (a, a) = I (a, b) := hI (a, a) (a, b) rfl
  have e2 : I (b, a) = I (b, b) := hI (b, a) (b, b) rfl
  have h11 := confereB_mesmo ρ a
  have h12 := confereB_outro ρ a b hab
  have h21 := confereB_outro ρ b a (Ne.symm hab)
  have h22 := confereB_mesmo ρ b
  unfold acertos casosDoGrupo
  simp only [List.countP_cons, List.countP_nil, h11, h12, h21, h22, e1, e2]
  cases I (a, b) <;> cases I (b, b) <;> rfl

/-- ★ **UM LADO SÓ ACERTA EXATAMENTE A METADE (o registro).** -/
theorem quem_so_ve_o_registro_acerta_exatamente_a_metade (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (hI : PagouSo (Prod.snd : X × X → X) I) :
    acertos ρ I (casosDoGrupo a b) = 2 := by
  have e1 : I (a, a) = I (b, a) := hI (a, a) (b, a) rfl
  have e2 : I (a, b) = I (b, b) := hI (a, b) (b, b) rfl
  have h11 := confereB_mesmo ρ a
  have h12 := confereB_outro ρ a b hab
  have h21 := confereB_outro ρ b a (Ne.symm hab)
  have h22 := confereB_mesmo ρ b
  unfold acertos casosDoGrupo
  simp only [List.countP_cons, List.countP_nil, h11, h12, h21, h22, e1, e2]
  cases I (b, a) <;> cases I (b, b) <;> rfl

/-- O juízo pelo par acerta os quatro. -/
theorem o_juizo_pelo_par_acerta_os_quatro (ρ : X → V) (a b : X) :
    acertos ρ (confereB ρ) (casosDoGrupo a b) = 4 := by
  unfold acertos casosDoGrupo
  simp [List.countP_cons]

/-- ★ **QUEM ACERTA OS QUATRO USA OS DOIS LADOS.** No grupo de dois sentidos, o juiz que acerta os quatro casos não é
função só da página nem só do registro. -/
theorem quem_acerta_os_quatro_usa_os_dois_lados (ρ : X → V) (a b : X) (hab : ρ a ≠ ρ b)
    (I : X × X → Bool) (h4 : acertos ρ I (casosDoGrupo a b) = 4) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  constructor
  · intro h
    have := quem_so_ve_a_pagina_acerta_exatamente_a_metade ρ a b hab I h
    omega
  · intro h
    have := quem_so_ve_o_registro_acerta_exatamente_a_metade ρ a b hab I h
    omega

/-- **CONTROLE QUE REPROVA.** Sem dois sentidos a conta não vale: se a palavra é de resposta constante, o juiz que diz
sempre “bate” (função de lado nenhum) acerta os quatro. -/
theorem sem_dois_sentidos_o_constante_acerta_os_quatro (ρ : X → V) (h : NuncaPaga ρ) (a b : X) :
    acertos ρ (fun _ => true) (casosDoGrupo a b) = 4 := by
  have hc : ∀ p : X × X, confereB ρ p = true := fun p => (confereB_sim_sse ρ p).mpr (h p.1 p.2)
  unfold acertos casosDoGrupo
  simp [List.countP_cons, hc]

end metade

end TGLExt.CopiadorEImpostor

#print axioms TGLExt.CopiadorEImpostor.quem_so_ve_a_pagina_acerta_exatamente_a_metade
#print axioms TGLExt.CopiadorEImpostor.quem_so_ve_o_registro_acerta_exatamente_a_metade
#print axioms TGLExt.CopiadorEImpostor.o_juizo_pelo_par_acerta_os_quatro
#print axioms TGLExt.CopiadorEImpostor.quem_acerta_os_quatro_usa_os_dois_lados
#print axioms TGLExt.CopiadorEImpostor.sem_dois_sentidos_o_constante_acerta_os_quatro

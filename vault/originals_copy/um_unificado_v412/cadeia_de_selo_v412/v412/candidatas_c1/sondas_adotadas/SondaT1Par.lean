import CopiadorEImpostor

set_option autoImplicit false
noncomputable section

/-!
# Sonda do revisor T1 (16/11/2026): o grupo 2 × 2 do desenho R6 e o que os teoremas das seções 11 e 12 dão e não dão

[sonda de revisor distinto; lê a candidata `CopiadorEImpostor` R6 (sha256 36579c2e…, cópia compilada na pasta do
revisor); nada instalado; nomes provisórios; nenhuma fala do operador é citada aqui]

Dicionário: o da seção 11 da candidata. Um caso é um par (página, registro); “bate” é ter o mesmo sentido; um juiz
é uma função dos casos em sim ou não; passar é acertar todos os casos do conjunto (tudo ou nada; juiz que não sorteia).

O grupo do desenho: duas páginas `x0`, `x1` e dois assentos `r0`, `r1`, com `ρ x0 = ρ r0`, `ρ x1 = ρ r1` e
`ρ x0 ≠ ρ x1`. As quatro casas: (x0, r0) bate; (x0, r1) não bate; (x1, r0) não bate; (x1, r1) bate.

O que fica provado:

1. `tres_casas_trazem_o_par_da_pagina`, `tres_casas_trazem_o_par_do_registro`: os dois pares que os teoremas
   `o_teste_reprova_quem_so_ve_a_pagina_sse` e `…_o_registro_sse` exigem já cabem em TRÊS casas (falta a casa em que
   os dois lados foram mexidos). Logo `nas_tres_casas_quem_acerta_usa_os_dois_lados`, e o mesmo no grupo inteiro
   (`no_grupo_quem_acerta_os_quatro_usa_os_dois_lados`).
2. ★ `nas_tres_casas_passa_quem_confere_cada_lado_com_o_original`: nas três casas passa um juiz que NÃO compara os
   dois lados: confere a página com o original, confere o assento com o original, e diz que bate quando os dois
   conferem. Os dois teoremas da seção 11 não o reprovam.
3. ★ `no_grupo_nenhum_juiz_de_dois_selos_passa` (e a forma “um ou outro”): com a quarta casa, nenhum juiz dessa forma
   passa. É isto, e não os dois teoremas citados, que pede a casa (página mexida, assento mexido).
4. ★ `no_grupo_passa_quem_casa_uma_marca_da_letra`: no grupo inteiro PASSA o juiz que usa os dois lados sem ler o
   sentido, casando uma marca da letra (por exemplo, ter ou não palavra de negação), sempre que essa marca acompanha
   o estado nos dois lados dentro do grupo. Nenhum teorema da candidata o reprova; só o material o impede.
5. `com_o_registro_fixo_ha_quem_passe_so_pela_pagina`: num conjunto de casos com o registro fixo (o braço 2 do
   desenho) existe juiz que só vê a página e passa. `nem_com_o_carimbo_se_julga_sem_o_registro`: o que a página leva
   (carimbo e corpo), sem o registro, não julga se ela bate, seja qual for o registro.
6. `comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido` e
   `o_resumo_injetivo_serve_e_comparar_resumos_erra`: o teorema `um_resumo_julga_sse_separa_os_sentidos` fala da
   informação do resumo do REGISTRO para um juiz que ainda lê a página inteira; comparar o resumo da página com o do
   registro pede mais (o resumo tem de ser igual em textos de mesmo sentido). O resumo dos bytes serve no primeiro
   sentido e erra no segundo em toda cópia de outra letra.
7. Repetições, por termo: `so_pelo_sinal_segue_do_da_secao_11`, `so_pela_assinatura_segue_do_da_secao_11`,
   `juizo_so_da_pagina_as_duas_formas` e `qual_resumo_serve_pelo_teorema_do_par` (o teorema de duas estrelas da seção
   12 sai do teorema do par da seção 2, com o que o juiz vê := a página e o resumo do registro).
8. `um_lado_so_sorteando_fica_em_um_dezesseis_avos`: só a aritmética do juiz que sorteia por um lado só
   (`p(1−p)·q(1−q) ≤ 1/16`). O modelo (sorteios independentes; mesma página, mesma distribuição) é hipótese de fora.

O que NÃO se afirma: nada sobre modelo de linguagem; nenhuma regra de veredito; nenhuma leitura da letra do operador.
-/

namespace TGLExt.CopiadorEImpostor.SondaT1

variable {X V : Type}

/-! ## 0. Auxiliares -/

theorem confereB_sim {ρ : X → V} {p : X × X} (h : ρ p.1 = ρ p.2) : confereB ρ p = true :=
  (confereB_sim_sse ρ p).mpr h

theorem confereB_nao {ρ : X → V} {p : X × X} (h : ρ p.1 ≠ ρ p.2) : confereB ρ p = false := by
  cases hb : confereB ρ p with
  | false => rfl
  | true => exact absurd ((confereB_sim_sse ρ p).mp hb) h

/-- O grupo 2 × 2 do desenho R6: duas páginas e dois assentos, as quatro combinações. -/
def grupo (x0 x1 r0 r1 : X) : Set (X × X) :=
  {p | (p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)}

/-- Três casas só: falta a casa (página mexida, assento mexido). -/
def tresCasas (x0 x1 r0 r1 : X) : Set (X × X) :=
  {p | p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)}

theorem mem_grupo {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ grupo x0 x1 r0 r1 ↔ ((p.1 = x0 ∨ p.1 = x1) ∧ (p.2 = r0 ∨ p.2 = r1)) := Iff.rfl

theorem mem_tresCasas {x0 x1 r0 r1 : X} {p : X × X} :
    p ∈ tresCasas x0 x1 r0 r1 ↔ (p = (x0, r0) ∨ p = (x0, r1) ∨ p = (x1, r0)) := Iff.rfl

theorem tresCasas_sub_grupo (x0 x1 r0 r1 : X) : tresCasas x0 x1 r0 r1 ⊆ grupo x0 x1 r0 r1 := by
  intro p hp
  rcases mem_tresCasas.mp hp with rfl | rfl | rfl
  · exact mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩
  · exact mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩
  · exact mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩

section doisPorDois

variable (ρ : X → V) {x0 x1 r0 r1 : X}

/-! ## 1. Os dois pares cabem em três casas -/

/-- O par contra quem só vê a página: a mesma página `x0` diante de `r0` (bate) e de `r1` (não bate). -/
theorem tres_casas_trazem_o_par_da_pagina (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1) (hne : ρ x0 ≠ ρ x1) :
    ∃ p ∈ tresCasas x0 x1 r0 r1, ∃ q ∈ tresCasas x0 x1 r0 r1,
      p.1 = q.1 ∧ confereB ρ p ≠ confereB ρ q := by
  refine ⟨(x0, r0), mem_tresCasas.mpr (Or.inl rfl), (x0, r1), mem_tresCasas.mpr (Or.inr (Or.inl rfl)),
    rfl, ?_⟩
  rw [confereB_sim (p := (x0, r0)) h0,
    confereB_nao (p := (x0, r1)) (fun h => hne (h.trans h1.symm))]
  decide

/-- O par contra quem só vê o registro: o mesmo registro `r0` diante de `x0` (bate) e de `x1` (não bate). -/
theorem tres_casas_trazem_o_par_do_registro (h0 : ρ x0 = ρ r0) (hne : ρ x0 ≠ ρ x1) :
    ∃ p ∈ tresCasas x0 x1 r0 r1, ∃ q ∈ tresCasas x0 x1 r0 r1,
      p.2 = q.2 ∧ confereB ρ p ≠ confereB ρ q := by
  refine ⟨(x0, r0), mem_tresCasas.mpr (Or.inl rfl), (x1, r0), mem_tresCasas.mpr (Or.inr (Or.inr rfl)),
    rfl, ?_⟩
  rw [confereB_sim (p := (x0, r0)) h0,
    confereB_nao (p := (x1, r0)) (fun h => hne (h0.trans h.symm))]
  decide

/-- Já nas três casas, quem acerta tudo não é função só da página nem só do registro. -/
theorem nas_tres_casas_quem_acerta_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool)
    (hI : ImprimeEm (confereB ρ) I (tresCasas x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I := by
  constructor
  · intro hp
    exact (o_teste_reprova_quem_so_ve_a_pagina_sse ρ (tresCasas x0 x1 r0 r1)).mpr
      (tres_casas_trazem_o_par_da_pagina ρ h0 h1 hne) I hp hI
  · intro hp
    exact (o_teste_reprova_quem_so_ve_o_registro_sse ρ (tresCasas x0 x1 r0 r1)).mpr
      (tres_casas_trazem_o_par_do_registro ρ h0 hne) I hp hI

/-- (a) NO GRUPO 2 × 2, QUEM ACERTA OS QUATRO NÃO É FUNÇÃO SÓ DA PÁGINA NEM SÓ DO REGISTRO. Corolário dos dois
teoremas da seção 11 da candidata; juiz que não sorteia; tudo ou nada. -/
theorem no_grupo_quem_acerta_os_quatro_usa_os_dois_lados (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (I : X × X → Bool)
    (hI : ImprimeEm (confereB ρ) I (grupo x0 x1 r0 r1)) :
    ¬ PagouSo (Prod.fst : X × X → X) I ∧ ¬ PagouSo (Prod.snd : X × X → X) I :=
  nas_tres_casas_quem_acerta_usa_os_dois_lados ρ h0 h1 hne I
    (fun p hp => hI p (tresCasas_sub_grupo x0 x1 r0 r1 hp))

/-! ## 2. O que a quarta casa reprova -/

open Classical in
/-- ★ **AS TRÊS CASAS NÃO BASTAM.** Nelas passa um juiz que não compara os dois lados: confere a página com o
original (`x0`), confere o assento com o original, e diz que bate quando os dois conferem. Usa os dois lados e não
julga pelo par. -/
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

/-- ★ **A QUARTA CASA.** No grupo inteiro nenhum juiz da forma “a página confere E o assento confere” passa,
sejam quais forem as duas conferências: a casa (página mexida, assento mexido) bate, e esse juiz não a aceita sem
aceitar também uma casa que não bate. -/
theorem no_grupo_nenhum_juiz_de_dois_selos_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 && g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 && g r0) = true := by
    have e := h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)
    rw [confereB_sim (p := (x0, r0)) h0] at e
    exact e
  have e11 : (f x1 && g r1) = true := by
    have e := h (x1, r1) (mem_grupo.mpr ⟨Or.inr rfl, Or.inr rfl⟩)
    rw [confereB_sim (p := (x1, r1)) h1] at e
    exact e
  have e01 : (f x0 && g r1) = false := by
    have e := h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm))] at e
    exact e
  revert e00 e11 e01
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-- A mesma coisa para a forma “a página confere OU o assento confere”. -/
theorem no_grupo_nenhum_juiz_de_um_selo_ou_outro_passa (h0 : ρ x0 = ρ r0) (h1 : ρ x1 = ρ r1)
    (hne : ρ x0 ≠ ρ x1) (f g : X → Bool) :
    ¬ ImprimeEm (confereB ρ) (fun p : X × X => f p.1 || g p.2) (grupo x0 x1 r0 r1) := by
  intro h
  have e00 : (f x0 || g r0) = true := by
    have e := h (x0, r0) (mem_grupo.mpr ⟨Or.inl rfl, Or.inl rfl⟩)
    rw [confereB_sim (p := (x0, r0)) h0] at e
    exact e
  have e01 : (f x0 || g r1) = false := by
    have e := h (x0, r1) (mem_grupo.mpr ⟨Or.inl rfl, Or.inr rfl⟩)
    rw [confereB_nao (p := (x0, r1)) (fun hh => hne (hh.trans h1.symm))] at e
    exact e
  have e10 : (f x1 || g r0) = false := by
    have e := h (x1, r0) (mem_grupo.mpr ⟨Or.inr rfl, Or.inl rfl⟩)
    rw [confereB_nao (p := (x1, r0)) (fun hh => hne (h0.trans hh.symm))] at e
    exact e
  revert e00 e01 e10
  cases f x0 <;> cases g r0 <;> cases f x1 <;> cases g r1 <;> decide

/-! ## 3. O juiz que usa os dois lados sem ler o sentido -/

/-- ★ **CASAR LETRA COM LETRA PASSA, SE A LETRA DENUNCIA.** Seja `s` uma marca qualquer da letra (por exemplo, ter
ou não palavra de negação na afirmação-alvo). Se, dentro do grupo, a marca acompanha o estado nos dois lados
(`s x0 = s r0`, `s x1 = s r1`, `s x0 ≠ s x1`), o juiz que só compara a marca da página com a marca do assento acerta
as quatro casas. Ele usa os dois lados e não lê sentido nenhum. Nenhum teorema da candidata o reprova. -/
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

end doisPorDois

/-! ## 4. O braço do carimbo: com o registro fixo, e sem o registro -/

/-- **COM O REGISTRO FIXO HÁ QUEM PASSE SÓ PELA PÁGINA.** Se todos os casos de um conjunto têm o mesmo registro,
existe juiz que só vê a página e acerta todos. (Instância de `sem_o_par_ha_quem_passe_pagando_so_pi`.) É o limite
do braço 2 do desenho, em que o índice fica intacto. -/
theorem com_o_registro_fixo_ha_quem_passe_so_pela_pagina (ρ : X → V) (S : Set (X × X)) (r0 : X)
    (hS : ∀ p ∈ S, p.2 = r0) :
    ∃ I : X × X → Bool, PagouSo (Prod.fst : X × X → X) I ∧ ImprimeEm (confereB ρ) I S := by
  refine sem_o_par_ha_quem_passe_pagando_so_pi Prod.fst (confereB ρ) S ?_
  intro p hp q hq h
  have hpq : p = q := Prod.ext h ((hS p hp).trans (hS q hq).symm)
  rw [hpq]

/-- **NEM COM O CARIMBO SE JULGA SEM O REGISTRO.** Se a palavra tem dois sentidos, nenhum juízo feito sobre o que a
página leva (uma assinatura declarada `n` e o corpo `x`) decide, para todo registro, se o corpo bate com ele.
(Instância de `sem_o_registro_ninguem_julga_se_bate`.) -/
theorem nem_com_o_carimbo_se_julga_sem_o_registro (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ J : V → X → Prop, ∀ (n : V) (x r : X), J n x ↔ Bate ρ x r := by
  rintro ⟨J, hJ⟩
  obtain ⟨a, b, hab⟩ := h2
  exact sem_o_registro_ninguem_julga_se_bate ρ ⟨a, b, hab⟩ ⟨J (ρ a), fun x r => hJ (ρ a) x r⟩

/-! ## 5. Informação do resumo não é comparação de resumos -/

/-- Comparar o resumo da página com o resumo do registro julga se e somente se o resumo separa os sentidos E é
igual em textos de mesmo sentido (tem exatamente o núcleo do sentido). A primeira metade é a condição do teorema
`um_resumo_julga_sse_separa_os_sentidos`; a segunda ele não pede. -/
theorem comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido {H : Type} (ρ : X → V)
    (h : X → H) :
    (∀ x r, (h x = h r ↔ Bate ρ x r)) ↔
      ((∀ a b, h a = h b → ρ a = ρ b) ∧ (∀ a b, ρ a = ρ b → h a = h b)) := by
  constructor
  · intro hc
    exact ⟨fun a b hab => (hc a b).mp hab, fun a b hab => (hc a b).mpr hab⟩
  · rintro ⟨hsep, hcla⟩ x r
    exact ⟨hsep x r, hcla x r⟩

/-- **CONTROLE.** Um resumo injetivo (o dos bytes) SERVE no sentido do teorema de duas estrelas da seção 12 (a
informação basta a um juiz que ainda lê a página inteira) e, no entanto, comparar resumos ERRA em toda cópia de
outra letra (`x ≠ r` com o mesmo sentido). -/
theorem o_resumo_injetivo_serve_e_comparar_resumos_erra {H : Type} (ρ : X → V) (h : X → H)
    (hinj : Function.Injective h) (x r : X) (hxr : x ≠ r) (hs : ρ x = ρ r) :
    (∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r) ∧ ¬ (h x = h r ↔ Bate ρ x r) := by
  refine ⟨(um_resumo_julga_sse_separa_os_sentidos ρ h).mpr (fun a b hab => by rw [hinj hab]), ?_⟩
  intro hiff
  exact hxr (hinj (hiff.mpr hs))

/-! ## 6. Repetições, por termo -/

/-- `so_pelo_sinal_ninguem_julga` (seção 12, com estrela) sai em uma linha de
`sem_o_registro_ninguem_julga_se_bate` (seção 11, com estrela): é o mesmo fato. -/
theorem so_pelo_sinal_segue_do_da_secao_11 (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ g : X → Prop, ∀ p : V × X, g p.2 ↔ Legitimo ρ p :=
  fun ⟨g, hg⟩ => sem_o_registro_ninguem_julga_se_bate ρ h2 ⟨g, fun x r => hg (ρ r, x)⟩

/-- `so_pela_assinatura_ninguem_julga` (seção 12, com estrela) sai de `o_juizo_nao_sai_so_do_registro` (seção 11). -/
theorem so_pela_assinatura_segue_do_da_secao_11 (ρ : X → V) (h2 : ∃ a b, ρ a ≠ ρ b) :
    ¬ ∃ f : V → Prop, ∀ p : V × X, f p.1 ↔ Legitimo ρ p := by
  rintro ⟨f, hf⟩
  apply o_juizo_nao_sai_so_do_registro ρ h2
  rintro ⟨x, r⟩ ⟨y, s⟩ h
  have hrs : r = s := h
  subst hrs
  exact propext ⟨fun hp => (hf (ρ r, y)).mp ((hf (ρ r, x)).mpr hp),
    fun hq => (hf (ρ r, x)).mp ((hf (ρ r, y)).mpr hq)⟩

/-- `sem_o_registro_ninguem_julga_se_bate` e `o_juizo_nao_sai_so_da_pagina` negam a mesma coisa, escrita de dois
jeitos. -/
theorem juizo_so_da_pagina_as_duas_formas (ρ : X → V) :
    (∃ f : X → Prop, ∀ x r, f x ↔ Bate ρ x r) ↔ PagouSo (Prod.fst : X × X → X) (confere ρ) := by
  constructor
  · rintro ⟨f, hf⟩ ⟨x, r⟩ ⟨y, s⟩ h
    have hxy : x = y := h
    subst hxy
    exact propext ⟨fun hp => (hf x s).mp ((hf x r).mpr hp), fun hq => (hf x r).mp ((hf x s).mpr hq)⟩
  · intro h
    exact ⟨fun _ => True, fun x r =>
      ⟨fun _ => Eq.mp (h (x, x) (x, r) rfl) (show confere ρ (x, x) from rfl), fun _ => trivial⟩⟩

/-- O teorema de duas estrelas da seção 12 (`um_resumo_julga_sse_separa_os_sentidos`), provado aqui SÓ com os
teoremas da seção 1 e 2 da candidata (`so_se_imprime_o_que_se_pagou` e `sem_o_par_ha_quem_passe_pagando_so_pi`),
tomando “o que o juiz vê” := (a página, o resumo do registro). É instância do teorema do par. -/
theorem qual_resumo_serve_pelo_teorema_do_par {H : Type} (ρ : X → V) (h : X → H) :
    (∃ J : H → X → Prop, ∀ x r, J (h r) x ↔ Bate ρ x r) ↔ (∀ r r', h r = h r' → ρ r = ρ r') := by
  constructor
  · rintro ⟨J, hJ⟩ r r' hrr
    have hpago : PagouSo (fun p : X × X => (p.1, h p.2)) (fun p : X × X => J (h p.2) p.1) := by
      rintro ⟨x, s⟩ ⟨y, t⟩ hπ
      have e1 : x = y := congrArg Prod.fst hπ
      have e2 : h s = h t := congrArg Prod.snd hπ
      show J (h s) x = J (h t) y
      rw [e1, e2]
    have himp : Imprime (confere ρ) (fun p : X × X => J (h p.2) p.1) :=
      fun p => propext (hJ p.1 p.2)
    have e : confere ρ (r, r) = confere ρ (r, r') :=
      so_se_imprime_o_que_se_pagou hpago himp (r, r) (r, r') (by
        show (r, h r) = (r, h r')
        rw [hrr])
    exact Eq.mp e (show confere ρ (r, r) from rfl)
  · intro hsep
    obtain ⟨I, hI, hP⟩ := sem_o_par_ha_quem_passe_pagando_so_pi
      (fun p : X × X => (p.1, h p.2)) (confere ρ) Set.univ (by
        rintro ⟨x, s⟩ - ⟨y, t⟩ - hπ
        have e1 : x = y := congrArg Prod.fst hπ
        have e2 : h s = h t := congrArg Prod.snd hπ
        subst e1
        show (ρ x = ρ s) = (ρ x = ρ t)
        rw [hsep s t e2])
    refine ⟨fun k x => ∃ r, h r = k ∧ I (x, r), fun x r => ⟨?_, fun hb => ?_⟩⟩
    · rintro ⟨r', hr', hI'⟩
      have e1 : I (x, r') = I (x, r) := hI (x, r') (x, r) (by
        show (x, h r') = (x, h r)
        rw [hr'])
      have e2 : I (x, r) = confere ρ (x, r) := hP (x, r) (Set.mem_univ _)
      exact Eq.mp e2 (Eq.mp e1 hI')
    · exact ⟨r, rfl, Eq.mpr (hP (x, r) (Set.mem_univ _)) hb⟩

/-! ## 7. O juiz que sorteia por um lado só (só a aritmética) -/

/-- Se um juiz só vê a página e sorteia, com probabilidade `p` de dizer “bate” diante de `x0` e `q` diante de `x1`,
e os quatro sorteios são independentes, a chance de acertar as quatro casas é `p(1−p)·q(1−q)`, que fica entre 0 e
1/16. Aqui só a desigualdade; o modelo de sorteio é hipótese de fora do Lean. -/
theorem um_lado_so_sorteando_fica_em_um_dezesseis_avos (p q : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    0 ≤ p * (1 - p) * (q * (1 - q)) ∧ p * (1 - p) * (q * (1 - q)) ≤ 1 / 16 := by
  have h1 : p * (1 - p) ≤ 1 / 4 := by nlinarith [sq_nonneg (p - 1 / 2)]
  have h2 : q * (1 - q) ≤ 1 / 4 := by nlinarith [sq_nonneg (q - 1 / 2)]
  have h3 : 0 ≤ p * (1 - p) := mul_nonneg hp0 (by linarith)
  have h4 : 0 ≤ q * (1 - q) := mul_nonneg hq0 (by linarith)
  refine ⟨mul_nonneg h3 h4, ?_⟩
  calc p * (1 - p) * (q * (1 - q)) ≤ 1 / 4 * (1 / 4) := mul_le_mul h1 h2 h4 (by norm_num)
    _ = 1 / 16 := by norm_num

end TGLExt.CopiadorEImpostor.SondaT1

#print axioms TGLExt.CopiadorEImpostor.SondaT1.tres_casas_trazem_o_par_da_pagina
#print axioms TGLExt.CopiadorEImpostor.SondaT1.tres_casas_trazem_o_par_do_registro
#print axioms TGLExt.CopiadorEImpostor.SondaT1.nas_tres_casas_quem_acerta_usa_os_dois_lados
#print axioms TGLExt.CopiadorEImpostor.SondaT1.no_grupo_quem_acerta_os_quatro_usa_os_dois_lados
#print axioms TGLExt.CopiadorEImpostor.SondaT1.nas_tres_casas_passa_quem_confere_cada_lado_com_o_original
#print axioms TGLExt.CopiadorEImpostor.SondaT1.no_grupo_nenhum_juiz_de_dois_selos_passa
#print axioms TGLExt.CopiadorEImpostor.SondaT1.no_grupo_nenhum_juiz_de_um_selo_ou_outro_passa
#print axioms TGLExt.CopiadorEImpostor.SondaT1.no_grupo_passa_quem_casa_uma_marca_da_letra
#print axioms TGLExt.CopiadorEImpostor.SondaT1.com_o_registro_fixo_ha_quem_passe_so_pela_pagina
#print axioms TGLExt.CopiadorEImpostor.SondaT1.nem_com_o_carimbo_se_julga_sem_o_registro
#print axioms TGLExt.CopiadorEImpostor.SondaT1.comparar_resumos_julga_sse_o_resumo_tem_o_nucleo_do_sentido
#print axioms TGLExt.CopiadorEImpostor.SondaT1.o_resumo_injetivo_serve_e_comparar_resumos_erra
#print axioms TGLExt.CopiadorEImpostor.SondaT1.so_pelo_sinal_segue_do_da_secao_11
#print axioms TGLExt.CopiadorEImpostor.SondaT1.so_pela_assinatura_segue_do_da_secao_11
#print axioms TGLExt.CopiadorEImpostor.SondaT1.juizo_so_da_pagina_as_duas_formas
#print axioms TGLExt.CopiadorEImpostor.SondaT1.qual_resumo_serve_pelo_teorema_do_par
#print axioms TGLExt.CopiadorEImpostor.SondaT1.um_lado_so_sorteando_fica_em_um_dezesseis_avos
#print axioms TGLExt.CopiadorEImpostor.SondaT1.confereB_sim
#print axioms TGLExt.CopiadorEImpostor.SondaT1.confereB_nao
#print axioms TGLExt.CopiadorEImpostor.SondaT1.tresCasas_sub_grupo

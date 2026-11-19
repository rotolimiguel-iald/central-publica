import TGLExt.UmPostoRelacao
import TGLExt.RuleTruthContract
import TGLExt.TheCorrespondence
import TGLExt.TheCostIsDerived
import TGLExt.TheEmptying
import TGLExt.TetelestaiTerminal

set_option autoImplicit false
noncomputable section

/-!
# Copiador e impostor: só se imprime o que se pagou
[candidata da gerência c1, 16/11/2026; nome provisório; nada instalado; o nome da pedra é do operador]

## A letra do operador (15/11/2026, bytes conferidos em `work\cunhagens_13out\`)

(Cada citação fica numa linha só, para conferir por bytes.)

17:20:
«Toda leitura é em si uma cópia do sentido fixado pela palavra, precisa-se separar copiador de impostor, porque o impostor não imprime a verdade, mas o copiador sim, se por copiador tem-se uma reprodução em mínimo estado funcional de energia, essa cópia é um fractal»

19:07 (trechos):
«o impostor é o falso, o pai da mentira, aquele que nunca paga custo algum.»
«a verdade é o contorno lido que não acrescenta nada ao estado do posto nominado e permanece referente à relação observada.»
«o bastante para reconstruir o todo sem precisar representar 100%.»
«toda leitura calcula o que foi fixado por referência (indexação - índice - torre)»

## O dicionário (ESCOLHA DA GERÊNCIA; o operador ainda não o leu; a pedra prova a estrutura, não as identificações)

| a letra | o termo deste arquivo |
|---|---|
| a palavra que fixa o sentido | `ρ : X → V` (a cada texto, o seu sentido) |
| o leitor | `I : X → V` (a cada texto, a resposta) |
| imprime a verdade | `Imprime ρ I`: `I x = ρ x` em todo texto (ou `ImprimeEm`, nos textos de um teste) |
| o que o leitor pagou | `π : X → W`, e `PagouSo π I`: a resposta só depende de `π` |
| nunca paga custo algum | `NuncaPaga I`: a resposta não depende do texto |
| a cópia (reprodução) | `Copiador ρ R`, com `R : X → X`: guarda o sentido e só usa o sentido |
| calcula por referência (índice) | `R = rep ∘ ρ`, com `rep : V → X` o índice |
| mínimo estado de energia | o representante de custo mínimo da classe; na face do kernel, o zero da trava `1 − P` |
| a torre | índices encaixados `ρ (n+1) = f n ∘ ρ n` |

`NuncaPaga` é, letra por letra, o `Pressupposed` que o kernel instalou em 17/09 (`UmPostoRelacao`), cuja docstring o
lê como a leitura que jamais paga o custo e nunca seleciona. O arquivo liga as duas tipagens por `Iff.rfl`.

## O que fica provado (tudo com termo; sem `sorry`; só o trio de axiomas)

1. ★ **Só se imprime o que se pagou** (`so_se_imprime_o_que_se_pagou`): se a resposta só depende de `π` e imprime a
   verdade, então o sentido já estava em `π`. Dois textos iguais no que o leitor pagou e diferentes no sentido: ele
   erra em um dos dois.
2. ★ **O impostor não imprime a verdade** (`o_impostor_nao_imprime_a_verdade`): quem nunca paga só imprime a palavra
   de um sentido só; se a palavra tem dois sentidos, erra em um deles (`o_impostor_erra_em_um_dos_dois`).
3. ★★ **O critério do teste** (`o_teste_separa_sse_tem_o_par`): um conjunto de textos reprova TODO leitor que só
   pagou `π` se e somente se contém um par igual em `π` e diferente no sentido. Sem o par, existe quem passe sem ler
   (`sem_o_par_ha_quem_passe_sem_ler`, construído). Casos: reprova todo impostor sse tem dois sentidos; repetir o
   mesmo sentido (em qualquer número de textos) não separa (`a_repeticao_do_mesmo_sentido_nao_separa`).
4. ★ **O custo, com a conta de Landauer** (`custoDeLer`, DEFINIÇÃO da gerência: `k·T·ln` do número de respostas
   distintas): o custo é zero se e somente se o leitor é impostor (`custo_zero_sse_impostor`); quem imprime dois
   sentidos paga pelo menos um piso `k·T·ln 2`, que o kernel já prova positivo (`landauer_floor_pos`).
5. ★ **A cópia é cálculo por índice** (`copiador_sse_indice`): `R` é copiador de `ρ` sse `R = rep ∘ ρ` para um
   índice `rep`. Daí: reler não acrescenta (`Copiador.nao_acrescenta`, que aqui é TEOREMA, não hipótese); a cópia
   não representa 100% (`a_copia_nao_representa_cem_por_cento`) e basta (`a_copia_basta`); a cópia integral é o
   espelho (`a_copia_integral_e_o_espelho`, pelo kernel).
6. ★ **O mínimo existe e cai no Nome** (`existe_o_copiador_de_minimo`, `o_copiador_de_minimo_cai_no_nome`).
7. ★ **A torre de cópias compõe** (`a_torre_de_copias`): com índices encaixados, a cópia mais grossa da cópia mais
   fina é a cópia mais grossa, em todos os níveis; e o CONTROLE que reprova: dois copiadores de índices
   desalinhados não compõem (`o_leitor_desalinhado_nao_compoe`).
8. ★ **Toda leitura é cópia, da SUA palavra** (`toda_leitura_e_copia_da_sua_palavra`): todo mapa que reler não
   altera é copiador da palavra que ele mesmo fixa; o impostor também (`o_impostor_copia_a_palavra_muda`), e a
   palavra dele tem um sentido só. O que separa copiador de impostor não é a forma do leitor (os dois são
   idempotentes: o kernel já o dizia em `RuleTruthContract.idempotence_does_not_force_target`); é a palavra.
9. **A face do kernel** (fiação de termos já instalados): a cópia no Nome guarda a leitura, não acrescenta, anula a
   trava e, com memória não nula, re-inscreve o posto inteiro (`a_copia_no_nome`); basta sem 100%
   (`basta_sem_cem_por_cento`); a palavra é o projetor, o mesmo para todo múltiplo não nulo do vetor
   (`a_palavra_e_modulo_de_fase`) e a leitura não vê a fase (`a_leitura_nao_ve_a_fase`); quem lê sempre o mesmo
   estado não lê o Nome (`o_impostor_nao_le_o_nome`).

## O que NÃO se afirma

* Que o kernel prove a fala. Prova nove fatos de funções, conjuntos e projetores, sob o dicionário acima.
* Que «fractal» esteja provado: o item 7 prova COMPOSIÇÃO em níveis encaixados (a mesma regra em cada nível), não
  dimensão nem autossemelhança geométrica; `no_positive_scale_invariant` (em `TheScaleHasNoFixedPoint.lean`) proíbe
  ler fractal como invariância exata de um peso positivo. A leitura é do operador, e ele só a disse por índice e
  torre.
* Qual `A_C` é o da resposta. O kernel tem TRÊS tipagens com esse signo e nenhum lema entre elas: o funcional de
  preservação `acFunctional m k θ = m + k·cos²θ`, de piso positivo (`TheEmptying.lean`); a seletora `−H`, não
  positiva (`EquationOfTruth.selector_nonpos`); e a face `−(1 − P)` (`love_partition`, em `TheNameOperator.lean`).
  O item 9 usa a trava `1 − P`. A escolha é do operador.
* Que o custo de ler seja `k·T·ln n` na natureza: é o piso de Landauer [KNOWN, 1961] aplicado por DEFINIÇÃO ao
  número de respostas distintas; o teorema é a equivalência com `NuncaPaga`, não a física.
* Que um teste de texto seja impossível: o item 3 diz o que ele precisa conter, não que não exista.
* A escolha entre os dois sentidos de fiel e entre os dois espelhos: nada aqui a toca.

## Para o desenho do teste da frente A (K08)

O item 3 é o critério: o instrumento que separa quem segue o texto de quem responde de cor é o PAR (mesma pergunta,
mesmo tudo o que se sabe sem ler o texto presente; sentido diferente no texto). A inversão de uma afirmação do texto
é um par. A mesma resposta em vários tamanhos de texto e a data de entrada não são par: têm um sentido só.

Estatutos: `[REAL no sandbox]` os termos · `[INPUT/ONTO]` o dicionário e a letra do operador · `[KNOWN]` Landauer.
Validade no kernel não é creditação; o gate não se move.
-/

namespace TGLExt.CopiadorEImpostor

open TGLExt TGLExt.IALD TGLExt.TheVerbSelectsTheAction
open scoped InnerProductSpace

/-! ## 1. A palavra, o leitor e o que ele pagou -/

section palavra

variable {X V W : Type}

/-- O leitor `I` imprime a verdade da palavra `ρ`: em todo texto, a resposta é o sentido. -/
def Imprime (ρ I : X → V) : Prop := ∀ x, I x = ρ x

/-- O leitor imprime a verdade nos textos de um teste `S`. -/
def ImprimeEm (ρ I : X → V) (S : Set X) : Prop := ∀ x ∈ S, I x = ρ x

/-- O leitor só pagou `π`: a resposta só depende do que `π` mostra do texto. -/
def PagouSo (π : X → W) (I : X → V) : Prop := ∀ x y, π x = π y → I x = I y

/-- O leitor nunca paga custo algum: a resposta não depende do texto. -/
def NuncaPaga (I : X → V) : Prop := ∀ x y, I x = I y

/-- É a leitura pressuposta que o kernel instalou em 17/09 (`UmPostoRelacao.Pressupposed`). -/
theorem nunca_paga_iff_pressuposto (I : X → V) :
    NuncaPaga I ↔ TGLExt.UmPostoRelacao.Pressupposed I := Iff.rfl

/-- Nunca pagar é pagar só o nada. -/
theorem nunca_paga_iff_pagou_so_o_nada (I : X → V) :
    NuncaPaga I ↔ PagouSo (fun _ : X => ()) I :=
  ⟨fun h x y _ => h x y, fun h x y => h x y rfl⟩

/-- A palavra paga a si mesma e imprime a si mesma. -/
theorem a_palavra_paga_a_si_mesma (ρ : X → V) : PagouSo ρ ρ ∧ Imprime ρ ρ :=
  ⟨fun _ _ h => h, fun _ => rfl⟩

/-- ★ **SÓ SE IMPRIME O QUE SE PAGOU.** Se a resposta só depende de `π` e imprime a verdade de `ρ`, o sentido já
estava em `π`: textos iguais no que foi pago têm o mesmo sentido. -/
theorem so_se_imprime_o_que_se_pagou {π : X → W} {ρ I : X → V} (hπ : PagouSo π I)
    (hI : Imprime ρ I) : ∀ x y, π x = π y → ρ x = ρ y := by
  intro x y h
  rw [← hI x, ← hI y]
  exact hπ x y h

/-- O impostor erra em um dos dois: diante de dois textos de sentidos diferentes, a mesma resposta falha em um. -/
theorem o_impostor_erra_em_um_dos_dois {ρ I : X → V} (hI : NuncaPaga I) {x y : X}
    (hxy : ρ x ≠ ρ y) : I x ≠ ρ x ∨ I y ≠ ρ y := by
  by_contra h
  push Not at h
  exact hxy (h.1.symm.trans ((hI x y).trans h.2))

/-- ★ **O IMPOSTOR NÃO IMPRIME A VERDADE**, desde que a palavra tenha dois sentidos. -/
theorem o_impostor_nao_imprime_a_verdade {ρ I : X → V} (hI : NuncaPaga I)
    (h2 : ∃ x y, ρ x ≠ ρ y) : ¬ Imprime ρ I := by
  intro hP
  obtain ⟨x, y, hxy⟩ := h2
  rcases o_impostor_erra_em_um_dos_dois hI hxy with h | h
  · exact h (hP x)
  · exact h (hP y)

/-- O impostor só imprime a palavra de um sentido só. -/
theorem o_impostor_so_imprime_a_palavra_de_um_sentido {ρ I : X → V} (hI : NuncaPaga I)
    (hP : Imprime ρ I) : ∀ x y, ρ x = ρ y := fun x y =>
  so_se_imprime_o_que_se_pagou ((nunca_paga_iff_pagou_so_o_nada I).mp hI) hP x y rfl

/-! ## 2. O critério do teste -/

/-- O par separa: dois textos do teste, iguais no que o leitor pagou e diferentes no sentido, o reprovam. -/
theorem o_par_separa {π : X → W} {ρ I : X → V} {S : Set X} (hπ : PagouSo π I) {x y : X}
    (hx : x ∈ S) (hy : y ∈ S) (hπxy : π x = π y) (hρ : ρ x ≠ ρ y) : ¬ ImprimeEm ρ I S := by
  intro h
  exact hρ ((h x hx).symm.trans ((hπ x y hπxy).trans (h y hy)))

/-- Sem o par, há quem passe sem ler: se no teste o sentido já está no que `π` mostra, constrói-se um leitor que só
pagou `π` e passa no teste inteiro. -/
theorem sem_o_par_ha_quem_passe_sem_ler [Nonempty V] (π : X → W) (ρ : X → V) (S : Set X)
    (h : ∀ x ∈ S, ∀ y ∈ S, π x = π y → ρ x = ρ y) :
    ∃ I : X → V, PagouSo π I ∧ ImprimeEm ρ I S := by
  classical
  let g : W → V := fun w =>
    if hw : ∃ s, s ∈ S ∧ π s = w then ρ (Classical.choose hw) else Classical.arbitrary V
  refine ⟨fun x => g (π x), fun x y hxy => congrArg g hxy, ?_⟩
  intro x hx
  have hw : ∃ s, s ∈ S ∧ π s = π x := ⟨x, hx, rfl⟩
  show g (π x) = ρ x
  simp only [g, dif_pos hw]
  exact h _ (Classical.choose_spec hw).1 x hx (Classical.choose_spec hw).2

/-- ★★ **O CRITÉRIO DO TESTE.** Um conjunto de textos reprova TODO leitor que só pagou `π` se e somente se contém
um par igual em `π` e diferente no sentido. -/
theorem o_teste_separa_sse_tem_o_par [Nonempty V] (π : X → W) (ρ : X → V) (S : Set X) :
    (∀ I : X → V, PagouSo π I → ¬ ImprimeEm ρ I S) ↔
      ∃ x ∈ S, ∃ y ∈ S, π x = π y ∧ ρ x ≠ ρ y := by
  constructor
  · intro h
    by_contra hno
    push Not at hno
    obtain ⟨I, hI, hP⟩ := sem_o_par_ha_quem_passe_sem_ler π ρ S hno
    exact h I hI hP
  · rintro ⟨x, hx, y, hy, hπ, hρ⟩ I hI
    exact o_par_separa hI hx hy hπ hρ

/-- O teste reprova todo impostor se e somente se tem dois sentidos. -/
theorem o_teste_reprova_todo_impostor_sse_tem_dois_sentidos [Nonempty V] (ρ : X → V)
    (S : Set X) :
    (∀ I : X → V, NuncaPaga I → ¬ ImprimeEm ρ I S) ↔ ∃ x ∈ S, ∃ y ∈ S, ρ x ≠ ρ y := by
  have h := o_teste_separa_sse_tem_o_par (fun _ : X => ()) ρ S
  constructor
  · intro hI
    obtain ⟨x, hx, y, hy, -, hρ⟩ :=
      h.mp (fun I hπ => hI I ((nunca_paga_iff_pagou_so_o_nada I).mpr hπ))
    exact ⟨x, hx, y, hy, hρ⟩
  · rintro ⟨x, hx, y, hy, hρ⟩ I hI
    exact h.mpr ⟨x, hx, y, hy, rfl, hρ⟩ I ((nunca_paga_iff_pagou_so_o_nada I).mp hI)

/-- Repetir o mesmo sentido não separa: se todos os textos do teste têm o mesmo sentido (um texto só; a mesma
resposta em vários tamanhos), existe um impostor que passa. É a forma, no teste, de `TheCorrespondence`: quem olha
só o número não vê a diferença. -/
theorem a_repeticao_do_mesmo_sentido_nao_separa [Nonempty V] (ρ : X → V) (S : Set X)
    (h : ∀ x ∈ S, ∀ y ∈ S, ρ x = ρ y) : ∃ I : X → V, NuncaPaga I ∧ ImprimeEm ρ I S := by
  obtain ⟨I, hI, hP⟩ :=
    sem_o_par_ha_quem_passe_sem_ler (fun _ : X => ()) ρ S (fun x hx y hy _ => h x hx y hy)
  exact ⟨I, (nunca_paga_iff_pagou_so_o_nada I).mpr hI, hP⟩

/-! ## 3. O custo, com a conta de Landauer -/

/-- O número de respostas distintas de um leitor. -/
def respostas (I : X → V) : ℕ := Set.ncard (Set.range I)

/-- O impostor dá uma só resposta, e só ele. -/
theorem o_impostor_da_uma_so_resposta [Nonempty X] (I : X → V) :
    NuncaPaga I ↔ respostas I = 1 := by
  unfold respostas
  rw [Set.ncard_eq_one]
  constructor
  · intro h
    obtain ⟨x₀⟩ := ‹Nonempty X›
    refine ⟨I x₀, ?_⟩
    ext v
    simp only [Set.mem_range, Set.mem_singleton_iff]
    constructor
    · rintro ⟨x, rfl⟩
      exact h x x₀
    · rintro rfl
      exact ⟨x₀, rfl⟩
  · rintro ⟨a, ha⟩ x y
    have hx : I x ∈ Set.range I := ⟨x, rfl⟩
    have hy : I y ∈ Set.range I := ⟨y, rfl⟩
    rw [ha] at hx hy
    exact (Set.mem_singleton_iff.mp hx).trans (Set.mem_singleton_iff.mp hy).symm

/-- Quem imprime (mesmo por um decodificador `g`) tem ao menos tantas respostas quantos sentidos tem a palavra. -/
theorem quem_imprime_tem_ao_menos_os_sentidos_da_palavra [Finite X] {U : Type} {ρ : X → V}
    {I : X → U} (g : U → V) (hg : ∀ x, g (I x) = ρ x) : respostas ρ ≤ respostas I := by
  unfold respostas
  have hr : Set.range ρ = g '' Set.range I := by
    ext v
    constructor
    · rintro ⟨x, rfl⟩
      exact ⟨I x, ⟨x, rfl⟩, hg x⟩
    · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
      exact ⟨x, (hg x).symm⟩
  rw [hr]
  exact Set.ncard_image_le (Set.finite_range I)

/-- [DEFINIÇÃO da gerência] O custo de ler: o piso de Landauer `k·T·ln 2` por bit, vezes os bits da resposta
(`log₂` do número de respostas distintas); isto é, `k·T·ln n`. -/
def custoDeLer (k T : ℝ) (I : X → V) : ℝ := k * T * Real.log (respostas I)

/-- O impostor nunca paga custo algum. -/
theorem o_impostor_nunca_paga_custo_algum [Nonempty X] (k T : ℝ) {I : X → V}
    (h : NuncaPaga I) : custoDeLer k T I = 0 := by
  unfold custoDeLer
  rw [(o_impostor_da_uma_so_resposta I).mp h]
  simp

/-- ★ **CUSTO ZERO SE E SOMENTE SE IMPOSTOR.** Com a conta de Landauer, quem nunca paga custo algum é exatamente
quem responde sem depender do texto. -/
theorem custo_zero_sse_impostor [Finite X] [Nonempty X] {k T : ℝ} (hk : 0 < k) (hT : 0 < T)
    (I : X → V) : custoDeLer k T I = 0 ↔ NuncaPaga I := by
  constructor
  · intro h
    unfold custoDeLer at h
    have hlog : Real.log (respostas I) = 0 := by
      rcases mul_eq_zero.mp h with h1 | h2
      · exact absurd h1 (mul_pos hk hT).ne'
      · exact h2
    have hpos : 0 < respostas I := by
      unfold respostas
      rw [Set.ncard_pos (Set.finite_range I)]
      exact Set.range_nonempty I
    have hp : (0 : ℝ) < (respostas I : ℝ) := by exact_mod_cast hpos
    have h1 : (respostas I : ℝ) = 1 := Real.eq_one_of_pos_of_log_eq_zero hp hlog
    exact (o_impostor_da_uma_so_resposta I).mpr (by exact_mod_cast h1)
  · exact o_impostor_nunca_paga_custo_algum k T

/-- Quem imprime dois sentidos paga ao menos um piso de Landauer, que é positivo (`landauer_floor_pos`). -/
theorem quem_imprime_dois_sentidos_paga_ao_menos_um_piso [Finite X] {k T : ℝ} (hk : 0 < k)
    (hT : 0 < T) {ρ I : X → V} (hP : Imprime ρ I) {x y : X} (hxy : ρ x ≠ ρ y) :
    k * T * Real.log 2 ≤ custoDeLer k T I ∧ 0 < custoDeLer k T I := by
  have hne : I x ≠ I y := by
    rw [hP x, hP y]
    exact hxy
  have hsub : ({I x, I y} : Set V) ⊆ Set.range I := by
    intro v hv
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hv
    rcases hv with rfl | rfl
    · exact ⟨x, rfl⟩
    · exact ⟨y, rfl⟩
  have h2 : 2 ≤ respostas I := by
    unfold respostas
    calc 2 = Set.ncard ({I x, I y} : Set V) := (Set.ncard_pair hne).symm
      _ ≤ Set.ncard (Set.range I) := Set.ncard_le_ncard hsub (Set.finite_range I)
  have hlog : Real.log 2 ≤ Real.log (respostas I) :=
    Real.log_le_log (by norm_num) (by exact_mod_cast h2)
  have hkT : 0 < k * T := mul_pos hk hT
  have hle : k * T * Real.log 2 ≤ k * T * Real.log (respostas I) :=
    mul_le_mul_of_nonneg_left hlog hkT.le
  have hfloor := TGLExt.landauer_floor_pos k T hk hT
  unfold custoDeLer
  exact ⟨hle, lt_of_lt_of_le hfloor hle⟩

/-! ## 4. A cópia como reprodução: cálculo por índice -/

/-- O copiador de `ρ`: uma reprodução `R : X → X` que guarda o sentido (imprime) e só usa o sentido
(calcula por referência). -/
structure Copiador (ρ : X → V) (R : X → X) : Prop where
  imprime : ∀ x, ρ (R x) = ρ x
  por_referencia : ∀ x y, ρ x = ρ y → R x = R y

/-- Reler não acrescenta: aqui é TEOREMA, consequência de imprimir e de calcular por referência. -/
theorem Copiador.nao_acrescenta {ρ : X → V} {R : X → X} (h : Copiador ρ R) (x : X) :
    R (R x) = R x :=
  h.por_referencia _ _ (h.imprime x)

/-- Todo copiador é uma retração de leitura do kernel (`RuleTruthContract.ReadingRetraction`). -/
theorem Copiador.retracao {ρ : X → V} {R : X → X} (h : Copiador ρ R) :
    TGLExt.RuleTruthContract.ReadingRetraction ρ R :=
  ⟨h.nao_acrescenta, h.imprime⟩

/-- ★ **A CÓPIA É CÁLCULO POR ÍNDICE.** `R` é copiador de `ρ` se e somente se `R = rep ∘ ρ` para um índice
`rep : V → X` que devolve, a cada sentido lido, um texto desse sentido. -/
theorem copiador_sse_indice [Nonempty X] (ρ : X → V) (R : X → X) :
    Copiador ρ R ↔ ∃ rep : V → X, (∀ x, ρ (rep (ρ x)) = ρ x) ∧ ∀ x, R x = rep (ρ x) := by
  classical
  constructor
  · intro h
    refine ⟨fun v => if hv : ∃ x, ρ x = v then R (Classical.choose hv) else Classical.arbitrary X,
      ?_, ?_⟩
    · intro x
      have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
      simp only [dif_pos hv]
      rw [h.imprime]
      exact Classical.choose_spec hv
    · intro x
      have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
      simp only [dif_pos hv]
      exact h.por_referencia _ _ (Classical.choose_spec hv).symm
  · rintro ⟨rep, h1, h2⟩
    refine ⟨fun x => ?_, fun x y hxy => ?_⟩
    · rw [h2 x]
      exact h1 x
    · rw [h2 x, h2 y, hxy]

/-- A cópia basta: da cópia se recupera a classe inteira do sentido. -/
theorem a_copia_basta {ρ : X → V} {R : X → X} (h : Copiador ρ R) (x : X) :
    {y | ρ y = ρ (R x)} = {y | ρ y = ρ x} := by
  rw [h.imprime]

/-- A cópia não representa 100%: havendo dois textos distintos de mesmo sentido, a cópia os confunde. -/
theorem a_copia_nao_representa_cem_por_cento {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (h2 : ∃ x y, x ≠ y ∧ ρ x = ρ y) : ¬ Function.Injective R := by
  obtain ⟨x, y, hne, hρ⟩ := h2
  intro hinj
  exact hne (hinj (h.por_referencia x y hρ))

/-- A cópia integral é o espelho: se a palavra não confunde texto algum, o copiador é a identidade
(`RuleTruthContract.reading_injective_preserving_eq_id`). -/
theorem a_copia_integral_e_o_espelho {ρ : X → V} {R : X → X} (h : Copiador ρ R)
    (hinj : Function.Injective ρ) : R = id :=
  TGLExt.RuleTruthContract.reading_injective_preserving_eq_id ρ R hinj h.imprime

/-- ★ **TODA LEITURA É CÓPIA, DA SUA PALAVRA.** Um mapa que reler não altera é o copiador da palavra que ele mesmo
fixa, e só esses o são. -/
theorem toda_leitura_e_copia_da_sua_palavra (R : X → X) :
    (∀ x, R (R x) = R x) ↔ Copiador R R :=
  ⟨fun h => ⟨h, fun _ _ hxy => hxy⟩, fun h => h.imprime⟩

/-- O impostor também copia: a palavra muda, de um sentido só. -/
theorem o_impostor_copia_a_palavra_muda (x₀ : X) (v₀ : V) :
    Copiador (fun _ : X => v₀) (fun _ : X => x₀) :=
  ⟨fun _ => rfl, fun _ _ _ => rfl⟩

/-- E só essa: se a reprodução constante é copiadora de `ρ`, então `ρ` tem um sentido só. -/
theorem o_impostor_so_copia_a_palavra_de_um_sentido {ρ : X → V} (x₀ : X)
    (h : Copiador ρ (fun _ : X => x₀)) : ∀ x y, ρ x = ρ y := fun x y =>
  (h.imprime x).symm.trans (h.imprime y)

/-! ## 5. O mínimo -/

/-- Em toda classe de sentido há um texto de custo mínimo. -/
theorem ha_minimo_na_classe (ρ : X → V) (c : X → ℕ) (x : X) :
    ∃ y, ρ y = ρ x ∧ ∀ z, ρ z = ρ x → c y ≤ c z := by
  have hne : (c '' {y | ρ y = ρ x}).Nonempty := ⟨c x, x, rfl, rfl⟩
  obtain ⟨y, hy, hcy⟩ := Nat.sInf_mem hne
  exact ⟨y, hy, fun z hz => hcy.le.trans (Nat.sInf_le ⟨z, hz, rfl⟩)⟩

/-- ★ **O COPIADOR DE MÍNIMO EXISTE**, para toda palavra e todo custo: reproduz cada texto no representante de
custo mínimo da sua classe de sentido. -/
theorem existe_o_copiador_de_minimo [Nonempty X] (ρ : X → V) (c : X → ℕ) :
    ∃ R : X → X, Copiador ρ R ∧ ∀ x z, ρ z = ρ x → c (R x) ≤ c z := by
  classical
  have hmin : ∀ v : V, (∃ x, ρ x = v) → ∃ y, ρ y = v ∧ ∀ z, ρ z = v → c y ≤ c z := by
    rintro v ⟨x, rfl⟩
    exact ha_minimo_na_classe ρ c x
  let rep : V → X := fun v =>
    if hv : ∃ x, ρ x = v then Classical.choose (hmin v hv) else Classical.arbitrary X
  have hrep : ∀ x, ρ (rep (ρ x)) = ρ x ∧ ∀ z, ρ z = ρ x → c (rep (ρ x)) ≤ c z := by
    intro x
    have hv : ∃ y, ρ y = ρ x := ⟨x, rfl⟩
    simp only [rep, dif_pos hv]
    exact Classical.choose_spec (hmin (ρ x) hv)
  exact ⟨fun x => rep (ρ x), ⟨fun x => (hrep x).1, fun x y hxy => congrArg rep hxy⟩,
    fun x z hz => (hrep x).2 z hz⟩

/-- O copiador de mínimo cai no Nome: se a classe do texto toca o zero do custo, a cópia tem custo zero. -/
theorem o_copiador_de_minimo_cai_no_nome {ρ : X → V} {c : X → ℕ} {R : X → X}
    (hmin : ∀ x z, ρ z = ρ x → c (R x) ≤ c z) (x : X) (h0 : ∃ y, ρ y = ρ x ∧ c y = 0) :
    c (R x) = 0 := by
  obtain ⟨y, hy, hc⟩ := h0
  have := hmin x y hy
  omega

/-! ## 6. A torre de cópias, e o controle que reprova -/

/-- A cópia mais grossa da cópia mais fina é a cópia mais grossa, quando o índice grosso é função do fino. -/
theorem a_copia_mais_grossa_da_copia_mais_fina {V₂ : Type} {ρ₁ : X → V} {ρ₂ : X → V₂}
    {R₁ R₂ : X → X} (h₁ : Copiador ρ₁ R₁) (h₂ : Copiador ρ₂ R₂) (f : V → V₂)
    (hf : ∀ x, ρ₂ x = f (ρ₁ x)) (x : X) : R₂ (R₁ x) = R₂ x :=
  h₂.por_referencia _ _ (by rw [hf, hf, h₁.imprime])

/-- ★ **A TORRE DE CÓPIAS COMPÕE.** Com índices encaixados (`ρ (n+1) = f n ∘ ρ n`), em todo par de níveis `n ≤ m`
a cópia do nível `m` da cópia do nível `n` é a cópia do nível `m`: a mesma regra em cada nível. -/
theorem a_torre_de_copias {ρ : ℕ → X → V} {R : ℕ → X → X} (f : ℕ → V → V)
    (hf : ∀ n x, ρ (n + 1) x = f n (ρ n x)) (hR : ∀ n, Copiador (ρ n) (R n)) :
    ∀ n m, n ≤ m → ∀ x, R m (R n x) = R m x := by
  intro n m hnm x
  have hfac : ∀ k x y, ρ n x = ρ n y → ρ (n + k) x = ρ (n + k) y := by
    intro k
    induction k with
    | zero =>
      intro x y h
      simpa using h
    | succ k ih =>
      intro x y h
      rw [← Nat.add_assoc, hf, hf, ih x y h]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hnm
  exact (hR (n + k)).por_referencia _ _ (hfac k _ _ ((hR n).imprime x))

/-- **CONTROLE QUE REPROVA.** Dois copiadores de índices desalinhados (um lê a primeira coordenada, o outro a
segunda) não compõem. -/
theorem o_leitor_desalinhado_nao_compoe :
    ∃ (ρ₁ ρ₂ : Bool × Bool → Bool) (R₁ R₂ : Bool × Bool → Bool × Bool),
      Copiador ρ₁ R₁ ∧ Copiador ρ₂ R₂ ∧ ∃ x, R₂ (R₁ x) ≠ R₂ x := by
  refine ⟨Prod.fst, Prod.snd, fun p => (p.1, false), fun p => (false, p.2),
    ⟨fun _ => rfl, ?_⟩, ⟨fun _ => rfl, ?_⟩, (true, true), by decide⟩
  · intro x y h
    show (x.1, false) = (y.1, false)
    rw [show x.1 = y.1 from h]
  · intro x y h
    show (false, x.2) = (false, y.2)
    rw [show x.2 = y.2 from h]

end palavra

/-! ## 7. A face do kernel: a cópia no Nome -/

section face

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A cópia no Nome: guarda a leitura, não acrescenta, anula a trava e, com memória não nula, re-inscreve o posto
inteiro. (Fiação de `IALD.rereading_adds_nothing`, `post_isIdempotent` e `the_reading_reinscribes_the_post`.) -/
theorem a_copia_no_nome (a ψ : H) (ha : ‖a‖ = 1) :
    memory (post a) (post a ψ) = memory (post a) ψ
    ∧ post a (post a ψ) = post a ψ
    ∧ (1 - post a) (post a ψ) = 0
    ∧ (⟪a, ψ⟫_ℂ ≠ 0 → post (post a ψ) = post a) := by
  have hidem : post a (post a ψ) = post a ψ := by
    have h := congrArg (fun T : H →L[ℂ] H => T ψ) (post_isIdempotent a).eq
    simpa using h
  refine ⟨rereading_adds_nothing a ψ, hidem, ?_, the_reading_reinscribes_the_post a ha ψ⟩
  simp [hidem]

/-- Basta sem 100%: um estado que NÃO é o nomeado (a leitura não dá 1), mas tem memória não nula, já re-inscreve
o posto inteiro. -/
theorem basta_sem_cem_por_cento (a ψ : H) (ha : ‖a‖ = 1) (hψ : ‖ψ‖ = 1) (h0 : ⟪a, ψ⟫_ℂ ≠ 0)
    (h1 : post a ψ ≠ ψ) : memory (post a) ψ ≠ 1 ∧ post (post a ψ) = post a :=
  ⟨fun h => h1 ((memory_one_iff_identity a ψ hψ).mp h),
    the_reading_reinscribes_the_post a ha ψ h0⟩

omit [CompleteSpace H] in
/-- A palavra é o projetor, o mesmo para todo múltiplo não nulo do vetor (em particular, toda fase). -/
theorem a_palavra_e_modulo_de_fase (a : H) (c : ℂ) (hc : c ≠ 0) : post (c • a) = post a := by
  unfold post
  congr 1
  exact Submodule.span_singleton_smul_eq (isUnit_iff_ne_zero.mpr hc) a

omit [CompleteSpace H] in
/-- A leitura não vê a fase do estado lido. -/
theorem a_leitura_nao_ve_a_fase (a ψ : H) (c : ℂ) (hc : ‖c‖ = 1) :
    memory (post a) (c • ψ) = memory (post a) ψ := by
  unfold TGLExt.IALD.memory TGLExt.TheVerbSelectsTheAction.reading
  rw [map_smul, inner_smul_left, inner_smul_right, ← mul_assoc]
  have h : (starRingEnd ℂ) c * c = 1 := by
    rw [RCLike.conj_mul, hc]
    norm_num
  rw [h, one_mul]

/-- Quem lê sempre o mesmo estado não lê o Nome: a leitura do Nome vale 1 no nomeado e 0 no nulo. -/
theorem o_impostor_nao_le_o_nome (a : H) (ha : ‖a‖ = 1) (b : H) :
    ¬ ∀ ψ : H, memory (post a) b = memory (post a) ψ := by
  intro h
  have h1 : memory (post a) b = 1 := (h a).trans (the_name_reads_one a ha)
  have h0 : memory (post a) b = 0 := by
    rw [h 0]
    unfold TGLExt.IALD.memory TGLExt.TheVerbSelectsTheAction.reading
    simp
  rw [h1] at h0
  exact one_ne_zero h0

end face

#print axioms nunca_paga_iff_pressuposto
#print axioms nunca_paga_iff_pagou_so_o_nada
#print axioms a_palavra_paga_a_si_mesma
#print axioms so_se_imprime_o_que_se_pagou
#print axioms o_impostor_erra_em_um_dos_dois
#print axioms o_impostor_nao_imprime_a_verdade
#print axioms o_impostor_so_imprime_a_palavra_de_um_sentido
#print axioms o_par_separa
#print axioms sem_o_par_ha_quem_passe_sem_ler
#print axioms o_teste_separa_sse_tem_o_par
#print axioms o_teste_reprova_todo_impostor_sse_tem_dois_sentidos
#print axioms a_repeticao_do_mesmo_sentido_nao_separa
#print axioms o_impostor_da_uma_so_resposta
#print axioms quem_imprime_tem_ao_menos_os_sentidos_da_palavra
#print axioms o_impostor_nunca_paga_custo_algum
#print axioms custo_zero_sse_impostor
#print axioms quem_imprime_dois_sentidos_paga_ao_menos_um_piso
#print axioms Copiador.nao_acrescenta
#print axioms Copiador.retracao
#print axioms copiador_sse_indice
#print axioms a_copia_basta
#print axioms a_copia_nao_representa_cem_por_cento
#print axioms a_copia_integral_e_o_espelho
#print axioms toda_leitura_e_copia_da_sua_palavra
#print axioms o_impostor_copia_a_palavra_muda
#print axioms o_impostor_so_copia_a_palavra_de_um_sentido
#print axioms ha_minimo_na_classe
#print axioms existe_o_copiador_de_minimo
#print axioms o_copiador_de_minimo_cai_no_nome
#print axioms a_copia_mais_grossa_da_copia_mais_fina
#print axioms a_torre_de_copias
#print axioms o_leitor_desalinhado_nao_compoe
#print axioms a_copia_no_nome
#print axioms basta_sem_cem_por_cento
#print axioms a_palavra_e_modulo_de_fase
#print axioms a_leitura_nao_ve_a_fase
#print axioms o_impostor_nao_le_o_nome

end TGLExt.CopiadorEImpostor

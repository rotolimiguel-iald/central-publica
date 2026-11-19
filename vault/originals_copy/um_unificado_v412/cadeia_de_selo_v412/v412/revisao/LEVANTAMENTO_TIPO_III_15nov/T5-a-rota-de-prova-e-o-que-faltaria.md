> Retorno de um leitor do levantamento do tipo III como termo, de 15/11/2026 (gerência c1; só leitura). É [DECLARADO pelo leitor] até a gerência conferir cada ponto na fonte. Não é fala do operador. As sondas Lean citadas são de rascunho. Nada aqui está instalado, selado ou aberto.

# T5-a-rota-de-prova-e-o-que-faltaria

## RESUMO
Levantamento T5 (A ROTA), só leitura. Consultas por grep -rn no terminal sobre TGLExt (1730 .lean) e o Mathlib do sandbox k411c; 3 sondas Lean no meu scratchpad (rc 0, trio, 0 sorry); nada da casa tocado.
1. (D) JÁ É TERMO para M. Compilei `ErgodicVectorState` (Ω unitário, cíclico, separador, KMS β=1 por Γ(B0(2πt)), fixos de Ad σ só escalares, M não comutativa) e `ergodicVectorState_M : ErgodicVectorState F1Fecho.CanonicalWedgeFlow.M`: ~15 linhas de fiação sobre LightRhoStar.centralizer_is_trivial (l.71) e campos do certificado habitado. Sonda ProbeT5c.lean, sha16 64a34824b368e5c5.
2. (C) pela metade: o traço fiel, normal, semifinito, tracial, com escala e^{-s}, no núcleo da cunha JÁ É termo (`actualPositiveTrace : PositiveTraceData`, ...PackageR2.lean:107), com `fixed_core_is_base` (núcleo^θ = M). Falta só Z(núcleo)=ℂ: nenhum termo de centro ou de fator no kernel (greps citados). Essa metade é oca: B(H) e M_n a satisfazem [KNOWN]; quem discrimina é o centro.
3. (A) e (B) escrevem-se e tipam (compilado), mas para M não há termo: não existe relação de Murray–von Neumann nem 'sem traço' para M. O Mathlib tem só VonNeumannAlgebra (162 linhas; sem pesos, tipo, Arveson, produto cruzado). (A) e (B) dão só «tipo III» (qualquer λ), não III₁.
4. A ponte (D)⟹III₁ NÃO é termo: é implicação citada (Connes 1973; recíproca em predual separável, Marrakchi–Vaes 2023 [DECLARADO: só o resumo, lido pelo revisor da casa]; Connes–Takesaki 1977 para o núcleo). Do insumo o kernel tem flow_is_Ad, vácuo cíclico e separador, KMS, Tomita; falta centro⊆fixos, espectro de Connes, Radon–Nikodym, comparação de projeções.
5. Recomendo: (D) como a definição-termo, com nome neutro (não 'III₁'); Z(núcleo)=ℂ como hipótese nomeada citada; (A)⟹(B) só se houver razão. Gordura: construir (A), (B) e Z(núcleo)=ℂ do zero (ordem de milhares de linhas [DECLARADO, sem medida]) para obter o que a citação já dá.
6. O resíduo do operador é UMA escolha de definição, dita antes: «tipo III₁» = «o Um é o único fixo do relógio da cunha» (D, termo hoje; a pedra LightRhoStar já o chama «o caso III₁ da ponte», l.8), com a classificação importada por citação; ou = «o núcleo de Takesaki é fator» (hipótese nomeada ou obra grande). (D) é critério suficiente, não a definição de Connes; só equivale em predual separável (separabilidade de F não aferida).

## ACHADOS

### A1. (D) por estado vetorial ergódico: ESCRITA e PROVADA para M (compilado)
classe: EXISTE E NÃO LIGADO (fiação, não falta)
onde: sonda C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_tipo_iii\T5\ProbeT5c.lean (sha16 64a34824b368e5c5; def l.53; ergodicVectorState_of_certificate l.66; ergodicVectorState_M l.83); kernel: LightRhoStar.lean:71, TheImportedSecondQuantization.lean:211-217
Lean (compilado, rc 0, 26 s, axiomas só propext/Classical.choice/Quot.sound, 0 sorry): `def ErgodicVectorState (M : VonNeumannAlgebra F) : Prop := ∃ (Ω : F) (σ : ℝ → (F ≃ₗᵢ[ℂ] F)), ‖Ω‖ = 1 ∧ Dense ((Submodule.span ℂ ((fun T : F →L[ℂ] F => T Ω) '' (M : Set (F →L[ℂ] F))) : Submodule ℂ F) : Set F) ∧ (∀ a ∈ M, a Ω = 0 → a = 0) ∧ TGLExt.ImportedSQ.KMSBody M Ω σ 1 ∧ (∀ a ∈ M, (∀ t : ℝ, (σ t).conjStarAlgEquiv a = a) → ∃ c : ℂ, a = c • (1 : F →L[ℂ] F)) ∧ NonComm M`. Provado: `ergodicVectorState_of_certificate (C : FockCertificate L) : ErgodicVectorState (C.R (L.K rightWedge))` e `ergodicVectorState_M : ErgodicVectorState F1Fecho.CanonicalWedgeFlow.M`. A prova usa só C.Ω_norm, wedge_cyclic, wedge_separating, bw_kms, wedge_nonabelian e LightRhoStar.centralizer_is_trivial (que já era do kernel); o único trabalho próprio é trocar o sinal de t (-(2πt) = 2π(-t)) e transportar net rightWedge = M por PhysicalFockNet.net_wedge_eq (PhysicalFockNetRealizationR2.lean:29). O cíclico entra para que KMS fixe σ como o grupo modular (unicidade, em papel).

### A2. Teorema-base da ergodicidade, instanciado e aferido
classe: EXISTE E LIGADO
onde: TGLExt/LightRhoStar.lean:71; F1Fecho394/CanonicalFockModularCoreInputR1.lean:126; TheImportedSecondQuantization.lean:168-232
`theorem centralizer_is_trivial (a : (C.R (L.K rightWedge)).toStarSubalgebra) (ha : ∀ t : ℝ, C.flow t a = a) : ∃ c : ℂ, (a : C.F →L[ℂ] C.F) = c • (1 : C.F →L[ℂ] C.F)` (LightRhoStar.lean:71). `def physicalFockCertificate : FockCertificate physicalCanonicalNet.toLightNetData.toLightOneParticle := physicalModularCoreInput.toCertificate` (CanonicalFockModularCoreInputR1.lean:126). Confirmado por #check na sonda: a instância tipa e imprime só o trio. Campos do certificado: wedge_cyclic l.211, wedge_separating l.213, wedge_nonabelian l.214, bw_kms l.217, flow_is_Ad l.229, Core l.232, trace l.241, trace_dual_scaling l.245. Consulta que mostra a falta de nome específico para M: grep -rn 'physicalFockCertificate' só acha usos em PIgualNP, CanonicalFullTGLWitnessR1; nenhum aplica centralizer_is_trivial a ele.

### A3. (C1) traço do núcleo de M: JÁ É termo (todos os campos)
classe: EXISTE E LIGADO
onde: F1Fecho394/CanonicalFockActualPositiveTracePackageR2.lean:88 (PositiveTraceData), :107 (actualPositiveTrace), :143 (unit_infinite); CanonicalFockFaithfulWeightR2.lean:23 (fixed_core_is_base); CanonicalFockRegularCoreR2.lean:32-38 (M, core, embedding, dualAction, embedding_injective)
`structure PositiveTraceData` tem zero, additive, homogeneous, monotone, faithful, normal (IsLUB interno), semifinite (`value A = ⨆ (B) (_ : B.val ≤ A.val) (_ : value B < ⊤), value B`), tracial (`value (positiveSquare a) = value (positiveSquare (star a))`), dual_scaling (`value (positiveDual s A) = ENNReal.ofReal (Real.exp (-s)) * value A`); `def actualPositiveTrace : PositiveTraceData` é habitante 'sem premissa de entrada'; `actualPositiveTrace_unit_infinite : actualPositiveTrace.value one = ⊤`. #check e #print axioms na sonda: trio. `fixed_core_is_base : (A ∈ core ∧ ∀ s, dualAmbient s A = A) ↔ ∃ C ∈ M, A = fibre C` (núcleo^θ = M). `core : VonNeumannAlgebra (RegularHilbert F)` e `dualAction` vêm de RegularCovariantCoreR3.lean:113 e :163, genéricos em (UnitaryFlow, M).

### A4. (C2) o núcleo é fator: Z(núcleo) = ℂ
classe: AUSENTE
onde: consultas: grep -rn --include=*.lean -E 'Set\.center|IsMulCentral|Subsemigroup\.center|IsFactor|is_a_factor|trivial_center|center_trivial' TGLExt (zero acertos); grep -rn -i -E '\bcentro\b|\bcenter\b|\bcentre\b|IsCentral' TGLExt (só 'centro' como léxico do Nome em AEscala/IALDGraviton, nunca centro de álgebra); sinônimos factor_of, isFactor, fator_ idem zero
O enunciado tipa (compilado): `def CoreIsFactor (U : F1Fecho.RegularCovariantCore.UnitaryFlow F) (M : VonNeumannAlgebra F) : Prop := IsFactor (F1Fecho.RegularCovariantCore.core U M)`, com `IsFactor M := ∀ z ∈ M, (∀ a ∈ M, a * z = z * a) → ∃ c : ℂ, z = c • (1 : F →L[ℂ] F)`. #check (CoreIsFactor fockFlow M) : Prop. Termo: nenhum. Caminho por prova: Connes–Takesaki (M III₁ ⟺ Z(núcleo) = ℂ; o relativo M'∩núcleo = Z(núcleo)) [KNOWN, a conferir; não abri a fonte]: exige a dualidade de Takesaki inteira, fora do Mathlib. Como o fluxo tem de ser o MODULAR do estado (o núcleo por fluxo arbitrário pode ser fator sem M ser III₁), a hipótese vem junto com bw_kms/tomita.

### A5. (A) por projeções: escrita, tipada, sem termo para M
classe: AUSENTE
onde: consultas: grep -rn -i -E 'murray|MvN|IsPartialIsometry|partial_isometry|PartialIsometry|purely.?infinite|properly.?infinite|infinite_projection|IsInfinite' TGLExt (só ModularCurrent.lean:21,28, docstring de uma face finita); grep -rn -E 'star [a-z]+ ?\* ?[a-z]+ ?= ?1' filtrado em ∈ M (zero); Mathlib: Algebra/Star/StarProjection.lean:27 (IsStarProjection), Analysis/VonNeumannAlgebra/Basic.lean (162 l.), sem isometria parcial
Lean (tipa, compilado): `def EquivOne (M) (p : F →L[ℂ] F) : Prop := ∃ v ∈ M, star v * v = 1 ∧ v * star v = p`; `def PurelyInfiniteFactor (M) : Prop := IsFactor M ∧ NonComm M ∧ ∀ p ∈ M, IsStarProjection p → p ≠ 0 → EquivOne M p`. Dá 'tipo III' (qualquer λ), não III₁. Vizinhos que EXISTEM e NÃO ESTÃO LIGADOS: `TGLV354.projection_join_comparison (N : VonNeumannAlgebra H) (p q : CoreProjection N) : ∃ u ∈ N, star u * u ≤ p.operator ∧ u * star u = (p ⊔ q).operator - q.operator` (V354ProjectionTraceSubadditivity.lean:12; Kaplansky genérico sobre toda álgebra de von Neumann, com a polar limitada V354BoundedPolar.lean:73); `core_matrix_corner` (CanonicalFockMatrixCornerR2.lean:188: ∃ e v no núcleo, star v * v = e ∧ e * v = 0). Falta a comparabilidade (fator ⟹ duas projeções comparáveis) e a infinitude.

### A6. (B) por traço: escrita e tipada; negativo universal é o mais oco
classe: AUSENTE (para M); EXISTE E NÃO LIGADO o formato certo
onde: consultas: grep -rn -i -E 'no_normal_semifinite|not_semifinite|NoSemifinite|semifinite_iff' TGLExt (zero); NoNormalTrace.lean:426,479,501 (só ESTADOS tracial normal, WOT-sequencial, na TORRE); SemifiniteWeight.lean:~44 ('O QUE FALTA: normalidade do peso')
Lean (tipa, compilado): `structure NFSTrace (M : VonNeumannAlgebra F)` com τ : (F →L[ℂ] F) → ℝ≥0∞, zero, add, smul, tracial (τ (star x * x) = τ (x * star x)), faithful, normal (IsLUB dirigido), semifinite (por projeções: toda p≠0 domina q≠0 com τ q < ⊤); `def NoNFSTrace M := IsEmpty (NFSTrace M)`. Risco: se a estrutura estiver mal tipada, o negativo é verdadeiro por vazio. Controle exigido: um inabitante em B(ℓ²) ou M_n; o kernel não tem (opWeight sem normalidade). Melhor reutilizar o formato já habitado, `PositiveTraceData` (cone positivo, normalidade por IsLUB interno, semifinitude por supremo dos minorantes finitos). A torre tem só o negativo para estados (no_normal_tracial_state_seq), não para pesos nem para M.

### A7. Tipagem OCA: cada forma contra B(H) com estado vetorial e M_n
classe: REAL (compilado) / papel
onde: sonda T5c: `not_ergodic_of_rank_one` (l.94); demais, argumento em papel [KNOWN]
(A) B(H) (dim ≥ 2) e M_n (n ≥ 2): RECUSAM (uma projeção de posto 1 não é ∼ 1: v*v=1 e vv*=p levaria dois vetores ortogonais à reta de η); ℂ recusa por NonComm; independe do estado. (B) B(H) e M_n TÊM traço normal fiel semifinito (Tr), logo recusam, SE a estrutura estiver bem tipada; o risco é o inverso (vazio). (C1) sozinha ACEITA B(H), M_n e ℂ (todo par (M, estado fiel) tem o traço canônico do núcleo com escala e^{-s}, Takesaki 1973 [KNOWN]); com (C2) recusa (núcleo de M_n é M_n⊗L^∞(ℝ), centro ≠ ℂ); estado vetorial em B(H) nem é fiel. (D) estado vetorial em B(H): RECUSA, PROVADO no sandbox (`not_ergodic_of_rank_one`: toda M com os operadores de posto 1, `(innerSL ℂ η).smulRight η ∈ M`, em espaço de dim ≥ 2, não tem vetor separador; cobre B(H) e M_n na representação defeituosa). M_n em forma padrão (com separador): fixos ⊇ ℂ[ρ], só escalares se n = 1 [papel, não compilado]. Abeliana: fixos = M. A casa já pagou um caso de oca: TheMarkIsNotATypeMark.lean (a marca de razões log-densa é satisfeita por M₂(ℂ), tipo I₂).

### A8. A ponte (D) ⟹ as outras: implicação citada, não termo
classe: SABIDO (citação) + AUSENTE (prova)
onde: REVISAO_K05_T1.md §5 e L1-t1-no-papel.md:53 (work\cadeia_de_selo\v412\revisao\); TheScaleHasNoFixedPoint.lean:34,76 ('mathlib não tem fatores III₁', Connes citado e não redemonstrado)
Estado normal fiel de centralizador trivial ⟹ fator III₁ (Connes 1973); em predual separável os estados ergódicos formam um G_δ denso nos fiéis de todo III₁ (Marrakchi–Vaes, arXiv:2305.14217; resumo lido pelo revisor da casa, [DECLARADO], eu não abri). Esboço meu em papel [a conferir]: Γ(σ) é subgrupo fechado e, com fixos ℂ, Γ = Sp(σ); cℤ daria ação ergódica do círculo, logo dim finita, contradição com Tomita; {0} daria σ trivial; resta ℝ, ou seja S(M) = [0,∞). O kernel TEM do insumo: o grupo modular como Ad do boost (flow_is_Ad: TheImportedSecondQuantization.lean:229, CanonicalWedgeFlowR2.lean:86), vácuo separador (WedgeCyclicR3.lean:70), KMS (campo bw_kms :217; CanonicalWedgeKMSR4.lean:32), Tomita (CanonicalFockBWR2.lean:40). NÃO TEM: centro ⊆ fixos; espectro de Arveson/Connes; ação ergódica de grupo compacto; 'semifinito ⟹ σ interno' (Radon–Nikodym de Pedersen–Takesaki; só a sombra finita em Ergodicity.lean:51 e FiniteCrossedProduct.lean); comparação de projeções. Mathlib: grep -rli 'Arveson|crossed product|ultraweak' = 0 arquivos.

### A9. Torre (outro modelo): o que há
classe: EXISTE E NÃO LIGADO a M
onde: TheFactorObject.lean:67 (theFactorObject), :95 (factor_omega_cyclic); NoNormalTrace.lean:426/479/501; MixedLadder.lean:141 (the_mixing_mark); TheOathOnTheTower.lean:94 (omegaCentralizer); TheMarkIsNotATypeMark.lean
`theFactorObject P : VonNeumannAlgebra (TowerHilbert P)`; o docstring diz que 'fator' e 'III₁' seguem ASSINATURA, não tipo. `omegaCentralizer P` é definido pela comutação com o estado (ω(AB)=ω(BA)); nenhum teorema o dá trivial (grep omegaCentralizer: só usos). Isto NÃO fornece M, e a torre produto tem centralizador grande (ITPFI).

### A10. Frases do kernel que envelheceram com (D)
classe: EXISTE E LIGADO
onde: ClosureCertificate.lean:36 e 110; GlobalLiftLadder.lean:43
ClosureCertificate diz que 'fator III₁/classificação de tipos' é 'não-tipável' por falta de camadas do Mathlib; vale para a classificação, mas o critério (D) é tipável e provado para M (compilado). GlobalLiftLadder:43 dá a T1 como 'exige centralizador trivial = ergodicidade do ESTADO' e a 'testemunha III₁ plena' como resíduo: a primeira está aferida para M; a segunda é a classificação.

### A11. Cuidado herdado: III₁ não dá centralizador trivial; e a tensão do κ
classe: MEDIDA / OPEN
onde: REVISAO_K05_T1.md linhas 94-96; TheScaleHasNoFixedPoint.lean:60-70
A revisão da K05 já fixou: ergodicidade é propriedade do ESTADO, não de 'III₁' (existem estados não ergódicos em todo III₁). Logo (D) é suficiente para III₁ e só equivalente em predual separável (a separabilidade de F = SumSpace Sectors, BosonicFock.lean:17, não foi aferida como termo; grep SeparableSpace em F1Fecho394 acha só fibra transversal e Fubini). E TheScaleHasNoFixedPoint.lean deixa [OPEN] a tensão entre um κ>0 finito (λ = e^{-κ}, tipo III_λ) e o III₁ declarado: nomear M como III₁ por (D) reabre esse item, não o fecha.

### A12. Mathlib dessa versão
classe: MEDIDA
onde: /c/t/k411c/final/.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean (162 linhas); Algebra/Star/StarProjection.lean:27
Há `VonNeumannAlgebra H` (subálgebra estrela com duplo comutante), `commutant`, `IsStarProjection`, ordem de Loewner em H →L[ℂ] H, WStarAlgebra (predual abstrato). Não há: peso, estado normal, topologia ultrafraca, isometria parcial/equivalência de projeções, centro como notação de fator, tipo, Arveson, produto cruzado, Tomita. Contagens por grep -rli: Arveson 0; crossed product 0; ultraweak 0; Tomita 1; Takesaki 1 (comentário).

## PROPOSTAS

### P1. P1. (D) como a DEFINIÇÃO-termo, com nome neutro
enunciado: Instalar `ErgodicVectorState` (o enunciado exato do achado 1, com o cíclico) e `ergodicVectorState_M : ErgodicVectorState F1Fecho.CanonicalWedgeFlow.M`, mais o genérico `ergodicVectorState_of_certificate`. Nome sugerido neutro (ex.: estado ergódico fiel do vácuo da cunha); o nome 'III₁' fica na frase como citação, não no identificador.
apoio: Compilado hoje: ProbeT5c.lean sha16 64a34824b368e5c5, rc 0, trio, 0 sorry, ~15 linhas de fiação; usa só termos já no kernel (centralizer_is_trivial, certificado habitado). É a forma para a qual o kernel já tinha a parte difícil, e a que a própria pedra LightRhoStar chama 'o caso III₁ da ponte'. Controle de tipagem compilado: `not_ergodic_of_rank_one` (B(H), M_n na representação defeituosa).
nao compra: Não compra a classificação (M é fator de tipo III₁ no sentido de Connes): isso entra por citação (Connes 1973; Marrakchi–Vaes 2023 para a recíproca), não por termo. Não compra Gromov–Hausdorff, o horizonte da TGL, H_K-chapéu, τ★. Vale só para o vácuo na cunha da luz livre.
risco: Promover critério a nome: (D) é suficiente, não a definição de Connes. Cuidados: separabilidade de F não aferida; M_n em forma padrão recusado só em papel; unicidade de σ por KMS+cíclico só em papel; reabre o item [OPEN] do κ (TheScaleHasNoFixedPoint).

### P2. P2. (C) por Connes–Takesaki: C1 já é termo, C2 como hipótese nomeada
enunciado: Montar o pacote (núcleo, dualAction, actualPositiveTrace, fixed_core_is_base) e declarar `H_nucleo_fator : CoreIsFactor fockFlow M` (Z(núcleo)=ℂ) como hipótese nomeada [KNOWN, Connes–Takesaki 1977], com teorema condicional '(D) + H_nucleo_fator ⟹ forma (C) completa'. Nunca como axioma.
apoio: C1 inteiro é termo (…PackageR2.lean:107). O enunciado de C2 tipa (compilado). É o padrão que o kernel já usa para o sabido: hipótese nomeada na fronteira (H1, H2, H3).
nao compra: C1 sozinho é oco: B(H), M_n e ℂ o satisfazem. Sem H_nucleo_fator nada se diz do tipo. Não prova C2.
risco: Prova interna de C2 (dualidade de Takesaki, M'∩núcleo = Z(núcleo)) é obra grande, fora do Mathlib (ordem de milhares de linhas [DECLARADO, sem medida]); entrar por hipótese pode parecer deslocar a trave se não for dito antes ao operador.

### P3. P3. (A) e (B) como TEOREMAS derivados ou como alvo futuro, nunca como definição de III₁
enunciado: Se houver razão: provar (A)⟹(B) genericamente (p ∼ 1 para toda p ≠ 0, mais aditividade, tracialidade e semifinitude por projeções, dão τ(1) ∈ {0,⊤}, contradição com fiel). Estimativa: dezenas de linhas [DECLARADO, não compilado]. Reutilizar o formato `PositiveTraceData` em vez da minha `NFSTrace`.
apoio: Os enunciados de (A) e (B) tipam (compilado). O kernel tem a Kaplansky genérica (`projection_join_comparison`, V354ProjectionTraceSubadditivity.lean:12), a polar limitada (V354BoundedPolar.lean:73) e o canto matricial no núcleo (core_matrix_corner), como primeiros degraus.
nao compra: Para M não dão nada sem a teoria de comparação e a classificação. (A) e (B) dão tipo III qualquer λ, nunca III₁. (B) como definição é a mais oca: um negativo universal sobre estrutura que o kernel não habita em B(ℓ²).
risco: Gordura: investir em (A)/(B) para M gasta muito para obter o que a citação de Connes dá, e o resultado seria 'tipo III' sem o 1.

### P4. P4. O que perguntar ao operador (só o resíduo)
enunciado: Uma escolha de definição, a ler antes de qualquer teste: «Na TGL, 'tipo III₁' da cunha da luz quer dizer (i) o Um é o único fixo do relógio modular da cunha, o centralizador do vácuo é trivial, o que já é termo do kernel, com a classificação de Connes importada por citação; ou (ii) o núcleo de Takesaki é fator, o que o kernel não tem e exigiria hipótese nomeada ou obra grande?» Ler também: com (i), 'III₁' passa a ser a citação ligada a um critério suficiente, e a tensão do κ reabre.
apoio: Fala dele no acervo é a que decide a leitura; as pedras LightRhoStar e GlobalLiftLadder já leem o III₁ pelo lado do estado. Nenhuma fala dele foi atribuída aqui: não abri bytes de fala nesta rodada.
nao compra: A pergunta não decide GH em III₁, τ★ nem o horizonte; não é teste com negativo possível, é escolha de nome de definição. Nenhum desfecho é falsificação.
risco: Se a escolha (i) for feita sem dizer que a classificação entra por citação, o desenho carregaria escondida uma escolha que o operador não leu (regra do posto). Dizer a partitura antes.

## CONSULTAS AO MAPA

## EXAMINADO
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\LightRhoStar.lean
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\F1Fecho394\CanonicalFockModularCoreInputR1.lean
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheImportedSecondQuantization.lean (linhas 130-275)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\QGReaderUVLock.lean (140-175)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\F1Fecho394\CanonicalWedgeFlowR2.lean, WedgeCyclicR3.lean, WeylFlowWiringR4.lean, PhysicalFockNetRealizationR2.lean, CanonicalFockAssemblyR1.lean, CanonicalModularCoreAssemblyR1.lean, CanonicalFockRegularCoreR2.lean, RegularCovariantCoreR3.lean
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\F1Fecho394\CanonicalFockActualPositiveTracePackageR2.lean, CanonicalFockInverseSupremumR2.lean, CanonicalFockCyclicTraceCompletionR3.lean, CanonicalFockFaithfulWeightR2.lean, CanonicalFockFiniteWeightR4.lean, CanonicalFockFiniteProjectionR3.lean, CanonicalFockNormalizedSplitR5.lean, CanonicalFockMatrixCornerR2.lean, CanonicalFockWeightStarDensityR2.lean
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\NoNormalTrace.lean, TheFactorObject.lean, TheMarkIsNotATypeMark.lean, MixedLadder.lean (cabeçalhos), PowersLadder.lean (cabeçalho), Ergodicity.lean, SemifiniteWeight.lean, FiniteCrossedProduct.lean, TheOathOnTheTower.lean, ClosureCertificate.lean, TheScaleHasNoFixedPoint.lean, GlobalLiftLadder.lean, V354ProjectionTraceSubadditivity.lean, V354CoreProjectionLattice.lean, V354BoundedPolar.lean, PonteDaEscalaDual.lean (cabeçalho), O16/ContentContractProposal.lean
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGL\AreaScale.lean (existe; sem relação com o tipo: é escala de área/Planck–Newton)
- C:\t\k411c\final\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean; Algebra\Star\StarProjection.lean
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\DESENHO_v412_R1.md (trechos); revisao\REVISAO_K05_T1.md §5; revisao\LEVANTAMENTO_FRENTE_B_15nov\L1-t1-no-papel.md linha 53; compilar_candidata.ps1
- Mapa de Rotas: formal.k05_t1_montagem_gh_tau_campo_v412; kernel.ergodicidade_de_mautner_candidata_15nov; formal.f1_2.dual_scaling_reuse_011; formal.f1_rede.concrete_bosonic_kinematics
- Memórias: t1-ergodicidade-na-luz-candidata-15nov.md; construir-tudo-o-fechamento-02nov.md
- Sondas minhas (scratchpad v412_tipo_iii\T5): ProbeT5a.lean, ProbeT5b.lean, ProbeT5c.lean e build\*.log

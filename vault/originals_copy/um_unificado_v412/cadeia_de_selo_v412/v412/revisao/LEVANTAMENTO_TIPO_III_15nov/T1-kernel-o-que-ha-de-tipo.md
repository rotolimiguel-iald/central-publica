> Retorno de um leitor do levantamento do tipo III como termo, de 15/11/2026 (gerência c1; só leitura). É [DECLARADO pelo leitor] até a gerência conferir cada ponto na fonte. Não é fala do operador. As sondas Lean citadas são de rascunho. Nada aqui está instalado, selado ou aberto.

# T1-kernel-o-que-ha-de-tipo

## RESUMO
1. Mapa consultado por termo unico (typeIII, tipoIII, III1, factor, fator, centro, semifinito, Connes, ergodicidade, Takesaki, nucleo): nenhuma rota sobre "tipo III como termo". Relevantes: formal.k05_t1_montagem_gh_tau_campo_v412 (H_erg ja era teorema do kernel), kernel.ergodicidade_de_mautner_candidata_15nov (nada instalado: grep Mautner no TGLExt = 0), formal.f1_2.dual_scaling_reuse_011.
2. (a) NAO ha no kernel (1730 .lean, grep recursivo pelo Bash) nem na mathlib local nenhuma definicao ou predicado de tipo (I, II, III, III1) para algebra de von Neumann. So: campo-insumo vazio `isTypeIII1 : Algebra → Prop` (O16/UVScope016_v3.lean:21, habitado por True) e definicao OPERACIONAL por campos, FullWitnessDataV3 (WitnessV3.lean:147), cujo docstring diz que centro trivial e ausencia de peso semifinito seguem abertos.
3. (b) Nenhum teorema conclui III ou III1 de objeto algum. As "marcas de III1" sao aritmetica de subgrupos de R; a v295 (TheMarkIsNotATypeMark.lean:98) prova que um fator de tipo I2 as satisfaz. Os teoremas no_normal_tracial_state_* excluem estado tracial normal na torre (excluem I_n e II_1), nao provam III.
4. (c) "Centro e trivial": AUSENTE (zero usos de Subalgebra.center, IsCentral, center_trivial em TGLExt). Existe o vizinho, EXISTE E LIGADO: LightRhoStar.centralizer_is_trivial (LightRhoStar.lean:71), os fixos do fluxo modular da cunha sao escalares (H_erg), valido para todo FockCertificate e portanto para o habitado physicalFockCertificate (CanonicalFockModularCoreInputR1.lean:126). Nao e Z(M)=C; falta o passo Z(M) dentro dos fixos (sabido, nao no kernel). Torre: nada.
5. (d) Os 21 campos de RemainingModularCoreInput sao todos termos no habitante (axiomas no trio, core v411). Nenhum campo ou teorema diz "Core e fator" nem "traco linear no Core todo". Avulsos no objeto fisico, sobre o cone positivo: traco fiel, normal (redes monotonas), aditivo, semifinito (subprojecao finita sob toda projecao nao nula), projecao de traco 1, duas metades iguais, a escala dual move P_F.
6. (e) Espectro do boost/fluxo modular: so "sem autovetor" (B0_no_eigen, D_no_eigen, continuous_modular_no_eigen). Que o espectro seja a reta toda ou denso: so docstring [KNOWN] (ForbiddenBoundary.lean:51; TheScaleHasNoFixedPoint.lean:34).
7. (f) the_mixing_mark = Dense(closure{log(1/2), log(1/3)}), aritmetica; o docstring diz que resta o FATOR (limite fraco-*, ITPFI); a v295 retirou a leitura de tipo.
8. Residuo para o tipo III como termo: (i) um predicado de tipo enunciavel, que ninguem tem; (ii) a ponte do objeto fisico a ele. Pela definicao "ergodico" a ponte e de uma linha; pela do nucleo de Takesaki falta Z(Core)=C.
9. Laterais: o ledger do core diz que a construcao do core "segue OPEN" (defasado frente a F1Fecho394) e ha cabecalhos "UNCOMPILED CANDIDATE" obsoletos; a tensao κ finito = III_lambda contra III1 (TheScaleHasNoFixedPoint.lean:64) segue [OPEN] no proprio kernel.
10. Nao verifiquei literatura: "ergodico ⟹ III1" e "Core fator ⟺ III1" ficam [KNOWN, a conferir] por outro agente.

## ACHADOS

### A1. (a1) Predicado ou definicao de tipo de algebra de vN
classe: AUSENTE
onde: kernel TGLExt (1730 .lean) e .lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/
Consulta: grep -rniE "TypeIII|type_III|typeIII|IsTypeIII|tipo ?III|III_1|III1|III₁" --include=*.lean (139 linhas, ~60 arquivos, todas docstring, comentario, campo ou chave) e varredura de nomes de declaracao (theorem/def/structure/abbrev) com [Tt]ype_?III|IsTypeIII|typeIII|III1|iii1|III_1|[Tt]ipo_?III: a unica declaracao com o nome e `theorem current_iii1_mark` (ScaleCurrent.lean:66), que nao e predicado de tipo. Sinonimos fator/factor, IsFactor, Murray, MvN, semifinite tentados. Mathlib local: a pasta VonNeumannAlgebra tem so Basic.lean; grep IsFactor|TypeIII|Murray|semifinite ali = 0.

### A2. (a2) O que existe com a palavra: insumo vazio e citacao proibida
classe: EXISTE COMO INSUMO VAZIO (nao como definicao)
onde: O16/UVScope016_v3.lean:21,34,80; O16/PhotonModularRealization.lean:20-26
`structure Problem` tem o campo `isTypeIII1 : Algebra → Prop` (:21), a rota exige `typeIII1 : P.isTypeIII1 algebra` (:34) e o contraexemplo logico o habita com `isTypeIII1 := fun _ => True` (:80). Cabecalho (:8-10): «This file neither defines a type-III factor analytically nor constructs a metric operator». PhotonModularRealization:20 lista como PROIBIDO `wedge_typeIII1 : Prop (forma vazia, preenchivel com True)` e diz (:22-26) que o tipo III_1 'vive no LEDGER EXTERNO do um.py (external_known_theorems, KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED) e so migra para ca quando ganhar enunciado concreto'. Regra da casa ja escrita: citar sem enunciado nao entra.

### A3. (a3) Definicao OPERACIONAL de 'fator III1' por campos
classe: EXISTE E LIGADO (e nao e o tipo)
onde: WitnessV3.lean:147; TheCoinage.lean:50 e :58; TheFactorObject.lean:67
`structure FullWitnessDataV3 extends FullWitnessData` tem: factor : VonNeumannAlgebra FH; Om, om_unit, om_cyclic; om_normal : SeqWOTContinuous factor (fun T => inner Om (T Om)); state_not_tracial; ratio_log_dense : Dense (AddSubgroup.closure (vnRealizedLog factor Om)); no_normal_tracial : ∀ τ ... SeqWOTContinuous factor τ → False. Habitante: `def qgClosureCertificateV2 : FullWitnessDataV3 := theWitnessV3` (TheCoinage:50), com `qgClosureCertificateV2.factor = theFactorObject mixProfile` (:58). TheCoinage docstring item 3: «"fator III₁" aqui e a definicao OPERACIONAL do programa (...); centro trivial e a ausencia de PESO semifinito ilimitado seguem NOMEADOS como abertura». theFactorObject (:67) e (π(torre))'' como VonNeumannAlgebra; docstring (:29-31): «"Fator" e "III₁" seguem sendo ASSINATURA (pedra 87), nao teorema de tipo». Axiomas no trio (core um_absoluto.json, axiom_report). Ressalva: o campo ratio_log_dense e a marca que a v295 retirou como criterio de tipo; sobra no_normal_tracial.

### A4. (b) Algum teorema conclui III ou III1?
classe: AUSENTE (so marcas e exclusoes)
onde: MixedLadder.lean:59,141; ScaleCurrent.lean:66; TheMarkIsNotATypeMark.lean:98,115; NoNormalTrace.lean:426,479,501,523; TowerTraceless.lean:97; TracelessAlgebra.lean:412; ModularCurrent.lean:21-23
Nenhum teorema tem como conclusao tipo III ou III1 de objeto algum (cunha, torre, modelo). A palavra aparece em nomes, docstrings e chaves. As 'marcas' (the_mixing_mark, current_iii1_mark, mixed_log_dense, signature_log_dense) sao Dense(closure{log l1, log l2}) em R. Retirada em teorema: `theorem the_mark_is_fed_by_a_type_I_factor` (TheMarkIsNotATypeMark:98): M2(C) com estado diagonal w=1/3 realiza as razoes 2 e 3 e o subgrupo e denso; `the_mark_does_not_separate_the_types` (:115). As exclusoes: `no_normal_tracial_state_mix` (NoNormalTrace:479) e `_const` (:501, l ≠ 1) e `_seq` (:426) dizem que nao ha funcional tracial normalizado WOT-sequencialmente continuo em M_TGL(1/3,1/4) e M_TGL(const); `chainState_not_tracial_tower` (TowerTraceless:97); `tracial_state_is_zero` (TracelessAlgebra:412, B(l2), tipo I∞). Docstring NoNormalTrace:40: «'sem estado tracial normal' NAO e ainda 'fator III₁ pleno' (centro trivial e ausencia de PESO semifinito ilimitado seguem o programa)». ModularCurrent:21-23 chama 'todas as projecoes nao-nulas equivalentes' de ASSINATURA do tipo III: retorica de docstring, sem enunciado de tipo.

### A5. (c1) Centro trivial (fator) para a cunha e para a torre
classe: AUSENTE
onde: consulta em TGLExt inteiro
Consulta: grep -rnE "IsCentral|Subalgebra\.center|Set\.center|Submonoid\.center|Subsemiring\.center|center ℂ|Algebra\.center|center_trivial|center_eq_bot|trivial_center|centre" --include=*.lean = 0 usos da API de centro da mathlib (so um 'centred' em WedgeNetFiniteDiamond:55, sem relacao). Nenhuma declaracao enuncia Z(M)=C para a cunha da luz nem para M_TGL (torre). Homonimo a evitar: `half_profile_centralizer_is_factor` (TracialCentralizerExpectation.lean:72) diz x ∈ omegaCentralizer P ↔ x ∈ theFactorObject P para o perfil w_n=1/2 (estado tracial); 'factor' ali e o nome do objeto, nao fatoriedade.

### A6. (c2) Ergodicidade modular da cunha (centralizador trivial), H_erg
classe: EXISTE E LIGADO
onde: LightRhoStar.lean:71 (+ :66, :80); CanonicalFockModularCoreInputR1.lean:126
VERBATIM: `theorem centralizer_is_trivial (a : (C.R (L.K rightWedge)).toStarSubalgebra) (ha : ∀ t : ℝ, C.flow t a = a) : ∃ c : ℂ, (a : C.F →L[ℂ] C.F) = c • (1 : C.F →L[ℂ] C.F)` para `variable {L : LightOneParticle} (C : FockCertificate L)` (LightRhoStar:34). Prova por wedge_separating + centralizer_vectors_eq_vacuum_line (⇐ Γ_no_fixed). Aplica-se a `physicalFockCertificate` (habitado; core: certificate_inhabited True, axiomas no trio; Γ_no_fixed ali e o teorema F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed, nao citacao). E M^σ = C, nao Z(M) = C: o passo 'σ fixa o centro' [KNOWN, Takesaki] nao esta declarado no kernel. Instancia nomeada a physicalFockCertificate nao existe como teorema (grep: so `rho_star_is_P_kerK_on_the_light` generico, TheWholeIsOne:167): e fiacao de uma linha, nao falta.

### A7. (d1) Os 21 campos de RemainingModularCoreInput e a marca de cada um
classe: EXISTE E LIGADO (provado) / citado no FockCertificate abstrato
onde: F1Fecho394/CanonicalModularCoreAssemblyR1.lean:47-70; CanonicalFockModularCoreInputR1.lean:76-101; TheImportedSecondQuantization.lean:168-263
VERBATIM (:48-70): trace : RepresentedCore → ENNReal; trace_zero : trace 0 = 0; trace_tracial : ∀ x y, trace (x * y) = trace (y * x); trace_star : ∀ x, trace (star x) = trace x; trace_dual_scaling : ∀ s x, trace ((dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * trace x; PF; PF_sa : star PF = PF; PF_idem : PF * PF = PF; PF_ne : PF ≠ 0; PF_pos : 0 < trace PF; PF_fin : trace PF < ⊤; Pp; Pm; Pp_sa; Pp_idem; Pm_sa; Pm_idem; split : Pp + Pm = PF; orth : Pp * Pm = 0; trace_additive : trace PF = trace Pp + trace Pm; equal_halves : trace Pp = trace Pm. Marca no habitante: todos PROVADOS (def modularCoreInput, trace := cyclicTraceCandidate, PF/Pp/Pm por normalized_split_exists; axiomas no trio). Marca no FockCertificate abstrato: Core [Takesaki 1973], PF 'projecao finita nao nula do nucleo II_∞ ... [Connes 1973]' (docstring do campo), F_infinite [KNOWN], Γ_strong/Γ_positive [KNOWN], Γ_no_fixed [KNOWN; bancada], wedge_cyclic [Araki; BGL], bw_kms [BW; BGL; Araki], tomita/flow [Tomita-Takesaki]. NAO ha campo: 'Core e fator'; 'traco fiel/normal/semifinito/linear no Core todo'. Cabecalho do habitante (CanonicalFockModularCoreInputR1:5-14): «This ENNReal cyclic completion does not assert complex linearity on the whole algebra or a factor-type classification».

### A8. (d2) Propriedades do traco e do nucleo ja provadas no objeto fisico (fora dos 21 campos)
classe: EXISTE E LIGADO
onde: F1Fecho394/CanonicalFockInverseSupremumR2.lean:55,67; ...ActualInverseFinitenessR2.lean:190; ...ActualInverseAdditivityR2.lean:208; ...CyclicTraceCompletionR3.lean:149; ...FiniteProjectionR3.lean:72,108,131; ...NormalizedSplitR5.lean:223; QGCitationDischarge.lean:142; CanonicalFockRegularCoreR2.lean:76
Sobre o cone positivo do core concreto (vN gerada por fibra R(KWR) e unitarios regulares em L2(R;Fock); `core_minimal`): fiel (`value_faithful`, `cyclicTraceCandidate_positive_faithful`: cyclicTraceCandidate (positiveAsCore p) = 0 ↔ p.val = 0); normal para redes monotonas (`value_normal`: value S = ⨆ j, value (A j)); aditivo (`value_add`); semifinito (`value_finite_minorants`: value X = ⨆ Y ≤ X com value Y < ⊤; `finite_subprojection_exists`: ∃ q projecao, 0 < value q, value q < ⊤, q.val * e.val = q; `finite_projection_exists`); projecao de traco 1 (`normalized_projection_exists`: value q = 1; `modularCoreInput_PF_trace`); metades iguais (`normalized_split_exists`: ∃ q r projecoes, q*r = 0, value (add q r) = 1, value q = value r); escala dual nao fixa P_F (`dual_action_moves_the_finite_corner`: s ≠ 0 → C.dualAction s C.PF ≠ C.PF). O traco 'total' e ENNReal-valued com extensao nao-padrao (TheImportedSecondQuantization:61-62). Ausentes: Z(Core)=C; ergodicidade/nao trivialidade da dualAction como enunciado; ponte 'traco → peso normal semifinito na vN algebra'.

### A9. (e) Espectro do boost / fluxo modular
classe: EXISTE (sem autovetor) / MEDIDA-SABIDO (reta toda) / AUSENTE como declaracao
onde: TheImportedSecondQuantization.lean:133; RetaDeLuzEspectro.lean:30,88; ContinuousModularDomain.lean:133; O16/ProductOrbitalSpectrum_v3.lean:83,96; QGReaderUVLock.lean:149; ForbiddenBoundary.lean:51; TheScaleHasNoFixedPoint.lean:34,76; PowersLadder.lean:315
Provado: `B0_no_eigen` (o boost de uma particula nao tem autovetor [PAGO]); `D_no_eigen`, `modularCandidate_no_eigen`; `continuous_modular_no_eigen`; `orbitalScalarBoost_no_eigen`; `light_modular_fixed_iff_vacuum` (fixos do fluxo modular = reta do vacuo). Consultas: grep "spectrum.*(univ|= ℝ)|approx.*eigen|Weyl sequence|espectro (continuo|absolutamente)|Lebesgue" → nenhuma declaracao que diga espectro = R, denso, ou absolutamente continuo. 'spec(K) = ℝ' aparece so como docstring «[invariante de Connes do III₁, KNOWN]» (ForbiddenBoundary:51) e «Em um fator de tipo III₁ o espectro modular e todo ℝ₊ (Connes)» (TheScaleHasNoFixedPoint:34), marcado «[KNOWN] ... citada e nao redemonstrada (mathlib nao tem fatores III₁)» (:76). `zero_mem_closure_ratio_spectrum` (PowersLadder:315) e sobre {λ^N} da escada de blocos, nao sobre o fluxo da cunha.

### A10. (f) MixedLadder.the_mixing_mark: o que prova e o que a docstring diz que resta
classe: EXISTE E LIGADO (aritmetica); leitura de tipo RETIRADA
onde: MixedLadder.lean:141; docstring :9-31; TheMarkIsNotATypeMark.lean:11-45; TheTopologicalFace.lean:36-39
VERBATIM: `theorem the_mixing_mark : Dense ((AddSubgroup.closure {Real.log ((1 : ℝ) / 2), Real.log ((1 : ℝ) / 3)} : AddSubgroup ℝ) : Set ℝ)` (por mixed_log_dense + irrational_log_two_div_log_three). So aritmetica de subgrupo de R. Docstring (:27-31): «O QUE RESTA (nomeado, sem veu): o FATOR — o limite indutivo fraco-* da cadeia mista com o estado-produto (ITPFI; III₁ de Araki–Woods). A assinatura espectral esta provada; o objeto-limite e o programa.» A v295 refutou a inferencia 'a fronteira e III₁ porque o Nome e denso': a razao ω(AB)=r·ω(BA) e com A,B ARBITRARIOS, nao autovetores do fluxo; M2(C) tipo I realiza 2 e 3 (TheMarkIsNotATypeMark:98). TheTopologicalFace:36-39 ja diz que a densidade do grupo das razoes modulares 'nao e provada aqui'.

### A11. (g) Tensao registrada no proprio kernel: kappa finito e III_lambda, nao III1
classe: EXISTE (nota [OPEN])
onde: TheScaleHasNoFixedPoint.lean:62-70
Docstring: «Um κ > 0 finito e um λ preferido: λ = e^{−κ} = 1,3313×10⁻⁵, e portanto tipo III_λ, nao III₁ ... Pela classificacao de Connes, III₁ nao tem gap modular ... Portanto, ou κ vive numa subalgebra/face finita (...), ou ha tensao real entre o κ e o tipo declarado. Isto nao e resolvido aqui, e nao deve ser assumido resolvido. [OPEN]». Relevante: o predicado de tipo que se escolher decide em que face o tipo e lido.

### A12. (h) Ledger do core sobre o tipo e o nucleo
classe: DECLARADO (no core) — parcialmente defasado
onde: Nós\um_absoluto.json (sha16 36c69fc767f8d47f), core.external_known_theorems
Entrada 'local hyperfinite type III_1 under hypotheses' [Buchholz, D'Antoni & Fredenhagen, CMP 111 (1987) 123], exact_role: 'tipo da algebra da cunha; sem teoria de fatores na mathlib, nao-enunciavel hoje', imported_into_witness: false. Entrada 'Takesaki crossed product / continuous core': 'a FORMA em DADOS ja migrou (ContinuousCoreData ...); a CONSTRUCAO para a rede escolhida segue OPEN'. Esta ultima esta defasada frente ao kernel: o core concreto da rede de Fock existe (CanonicalFockRegularCoreR2.lean; `core_minimal` :76; `physicalFockCertificate`, axiomas no trio). Errata ao lado cabivel. As hipoteses do BDF 1987 [KNOWN, a conferir] nao estao nomeadas no kernel.

### A13. (i) Candidata Mautner e rotulos obsoletos
classe: AUSENTE (candidata nao instalada) / nota
onde: consulta grep -rli Mautner TGLExt = 0; TGLExt.lean:1131; F1Fecho394/*.lean cabecalhos
`ErgodicidadeDeMautner` (Mapa kernel.ergodicidade_de_mautner_candidata_15nov) nao esta no kernel; nao apresenta-la como resultado instalado nem como ergodicidade nova da cunha (a H_erg ja e teorema, achado c2). Cabecalhos 'DECLARADO / UNCOMPILED CANDIDATE' de CanonicalFockModularCoreInputR1:5, FiniteProjectionR3:3, NormalizedSplitR5:3 sao rotulos obsoletos: os modulos estao importados em TGLExt.lean:1131 e no axiom_report do core (34300 declaracoes, trio). E fiacao/nota, nao falta.

### A14. (j) Rota do kernel sobre dual scaling e semifinitude abstrata
classe: EXISTE E NAO LIGADO ao tipo (fiacao)
onde: GlobalLiftLadder.lean:144,160; LocalBreuerGap.lean:72; SemifiniteLattice.lean:145; TheImportedExpectation.lean:107; FiniteCrossedProduct.lean
`structure DualScalingData` (tau, theta, scaling : tau (theta s m) = Real.exp (-s) * tau m) e `DualScalingData.fixed_tau_zero` (:160: fixo por θ_{s0}, s0>0 ⟹ τ = 0): a semifinitude so emerge no fecho continuo. `SemifiniteTraceData` (LocalBreuerGap:72) e a camada tracial semifinita MINIMA em reticulado (tau monotono e fiel); habitada por dimOrTop em subespacos (`semifinite_trace_is_semifinite`, SemifiniteLattice:145: todo subespaco nao trivial contem um de peso 1), isto e, tipo I∞, nao o core. `TakesakiInput` (TheImportedExpectation:107) pede cyclic/separating/normal/expectation para a TORRE. Sombra finita do core em FiniteCrossedProduct (D1-D5), declarada sem escala de traco.

## PROPOSTAS

### P1. TipoPeloCentralizador (ergodicidade modular como predicado de tipo)
enunciado: Definir em Lean um predicado sobre o par (algebra da cunha, fluxo modular) do tipo ErgodicModular := (existem a, b na algebra com a*b ≠ b*a) ∧ (∀ a na algebra, (∀ t, flow t a = a) → ∃ c : ℂ, a = c • 1), e provar `ErgodicModular` para physicalFockCertificate juntando o campo wedge_nonabelian e LightRhoStar.centralizer_is_trivial (LightRhoStar.lean:71). O 'tipo III1' entra por CITACAO da implicacao [KNOWN] ergodico + nao trivial ⟹ fator III1, com a hipotese nomeada, em estrutura com enunciado real (nao Prop vazio).
apoio: centralizer_is_trivial (LightRhoStar.lean:71) e wedge_nonabelian (campo do FockCertificate, TheImportedSecondQuantization.lean:214), ambos ja termos no habitante physicalFockCertificate (trio); a ponte e fiacao de uma linha, sem pedra nova de fundo.
nao compra: Nao compra o centro do Core, o fluxo de pesos, a classificacao de Connes, o tipo dos objetos da torre, o horizonte da TGL, nem a tensao κ finito = III_lambda (TheScaleHasNoFixedPoint:64). Nao prova existencia de rede global.
risco: E DEFINICAO da casa: reproduz o erro da v295 se o nome capturar mais do que o predicado diz (o operacional ja existe em FullWitnessDataV3 e foi contestado). A implicacao ergodico ⟹ III1 e [KNOWN a conferir]: o enunciado exato (hipoteses, o que e 'nao trivial', predual separavel) precisa ser lido na fonte por outro agente; nao a verifiquei nem a refuto. O negativo desse caminho seria parede medida da citacao, nao falsificacao da TGL.

### P2. TipoPeloNucleoDeTakesaki (Core fator com traco semifinito escalado)
enunciado: Definir por dados: Core com centro trivial (Subalgebra.center ou IsCentral) + traco fiel, normal, semifinito e tracial com tau∘theta_s = e^{-s} tau + dualAction nao trivial, e citar [KNOWN] que isso caracteriza o tipo III1 da algebra. Habitar com o core concreto de F1Fecho394.
apoio: Ja provado no objeto fisico sobre o cone positivo: fiel, normal por redes monotonas, aditivo, semifinito, projecao de traco 1, metades iguais, escala dual move P_F (achado d2); core concreto com core_minimal.
nao compra: Nao compra a ergodicidade como teorema novo (ja e do kernel), nem o horizonte da TGL, nem III1 sem o passo 'centro trivial'. Nao resolve a ponte traco v351 da torre com o nucleo matricial (Mapa formal.f1_2.dual_scaling_reuse_011).
risco: Falta o centro do Core (zero declaracoes de centro no kernel; achado c1) e a ponte do cyclicTraceCandidate (cabecalho: 'does not assert complex linearity on the whole algebra') a um peso normal semifinito da algebra de vN. Pela literatura [KNOWN, a conferir] Z(Core) e o fluxo de pesos de Connes-Takesaki e 'Core fator' e justamente o conteudo de III1: pode nao ser etapa menor que o proprio predicado ergodico. O negativo seria parede de construcao.

## CONSULTAS AO MAPA

## EXAMINADO
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt (grep -rn recursivo pelo Bash, 1730 .lean, incl. F1Fecho394 e O16)
- TGLExt\F1Fecho394\CanonicalFockModularCoreInputR1.lean, CanonicalModularCoreAssemblyR1.lean, CanonicalFockCyclicTraceCompletionR3.lean, CanonicalFockFiniteProjectionR3.lean, CanonicalFockNormalizedSplitR5.lean, CanonicalFockInverseSupremumR2.lean, CanonicalFockRegularCoreR2.lean, RegularCovariantCoreR3.lean
- TGLExt\TheImportedSecondQuantization.lean (LightOneParticle e FockCertificate, campos e marcas)
- TGLExt\LightRhoStar.lean, QGReaderUVLock.lean, QGCitationDischarge.lean, TheWholeIsOne.lean (uso)
- TGLExt\MixedLadder.lean, TheMarkIsNotATypeMark.lean, ScaleCurrent.lean, SignatureInTheLimit.lean, PowersLadder.lean, TowerTraceless.lean, TheNameIsTheGeneratingGroup.lean
- TGLExt\NoNormalTrace.lean, TracelessAlgebra.lean, SemifiniteWeight.lean, SemifiniteLattice.lean, LocalBreuerGap.lean, ClosedLattice.lean
- TGLExt\WitnessV3.lean, TheCoinage.lean, TheFactorObject.lean, TracialCentralizerExpectation.lean, TheImportedExpectation.lean, FiniteCrossedProduct.lean, GlobalLiftLadder.lean, V351DualScalingBridge.lean
- TGLExt\O16\UVScope016_v3.lean, O16\PhotonModularRealization.lean, O16\ProductOrbitalSpectrum_v3.lean; TGL\ModularRealization.lean (ContinuousCoreData)
- TGLExt\RetaDeLuzEspectro.lean, ContinuousModularDomain.lean, ForbiddenBoundary.lean, TheScaleHasNoFixedPoint.lean, ModularCurrent.lean, TheTopologicalFace.lean, EsperancaCondicional.lean, IALDRhoStar.lean, HilbertHome.lean
- Nós\um_absoluto.json (sha16 36c69fc767f8d47f): core.kernel_formalization.axiom_report (34300 decls, conferidas por script as ~25 citadas: todas no trio), core.external_known_theorems, core.iii1_net_image, core.crossed_dual_weight, chaves certificate_inhabited
- tgl_kernel\TGLExt.lean (imports, linha 1131) e .lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra (so Basic.lean)
- Mapa de Rotas: consultar typeIII, tipoIII, III1, factor, fator, centro, semifinito, Connes, ergodicidade, nucleo, Takesaki (rotas lidas em detalhe: formal.k05_t1_montagem_gh_tau_campo_v412, formal.f1_2.dual_scaling_reuse_011, cadeia.preparacao_v412)
- Rascunho: scratchpad\v412_tipo_iii\T1 (decl.sh, core_probe*.py), so leitura; nada fora dela foi escrito

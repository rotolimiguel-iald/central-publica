# CONFERÊNCIA DISTINTA — o rascunho R0 da pergunta do tipo III nas quatro línguas — V2-literatura-e-logica-matematica

> Montado pela gerência c1 em 15/11/2026 17:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** REPROVADO — achados: 3 ALTO, 5 MEDIO, 4 BAIXO

## Resumo

REPROVADO na forma atual, e o conserto é de redação: a estrutura, a honestidade sobre o que cada resposta decide e a recomendação marcada como recomendação ficam.
Três frases estão erradas (ALTO). (1) Em 1(c), os quatro "modos de dizer III₁" não se equivalem: dois dizem só tipo III. (2) A glosa do modo da medida ("nenhuma medida finita pesa as partes") vale também para tipo I∞ e II∞. (3) Em 1(e)(ii), dizer que "o relógio do kernel é o relógio modular do vácuo" não é termo é falso: a identidade de Bisognano–Wichmann da cunha física é teorema do kernel, sem hipótese de registro.
Conferido e correto: o enunciado do Lema 2.1 de Marrakchi e Vaes (arXiv:2305.14217v3, PDF aberto por mim) tem exatamente as hipóteses do rascunho. O Lema 5.3 de Ando e Haagerup (arXiv:1212.5457v3, aberto no texto baixado pelo T6) diz o mesmo ("C ou fator III₁"). O Teorema A exige predual separável, e a Obs. 2.7 mostra que a separabilidade é essencial. A atribuição a Longo vem de Marrakchi e Vaes (p. 1 e p. 2), e o original de Longo não foi aberto. "Os modos 2 e 3 dizem só tipo III" e "a metade que existe do modo 4 não distingue" estão certos. A tradução "relógio do estado" é honesta, pois Marrakchi e Vaes dizem que o centralizador coincide com os pontos fixos do grupo modular.
Há quatro ressalvas médias: a leitura do espectro no modo 4, o custo do núcleo ser fator, o controle da sonda e o raciocínio do κ. As omissões de homogeneidade (Connes–Størmer) e de Borchers são aceitáveis para leigo, com uma linha cada.

## Achados

1. **(ALTO)** 1(c), cabeçalho e segunda frase: "A matemática tem quatro modos de dizer 'tipo III₁'. Na literatura eles se equivalem (para o primeiro, com uma condição técnica)"

   Falsa como escrita, e o rascunho a desmente na linha seguinte ("os modos 2 e 3 sozinhos dizem só tipo III"). Medida e partes caracterizam tipo III com qualquer λ em [0,1]; só estado e relógio dizem III₁. Conferido em Connes 1973 (Lema 3.1.2, via T6 A1), em Ando e Haagerup Teor. 4.17 e em Marrakchi e Vaes (Teor. A e Lema 2.1). Equivalem-se 2⟺3 (fatores σ-finitos) e 1⟺4, e esta só com predual separável e só para a EXISTÊNCIA de um estado ergódico (Obs. 2.7: há III₁ com predual não separável sem estado ergódico). 1⟹III₁ vale sempre (Lema 2.1). Além disso, como escritos, os modos 1 e 3 são satisfeitos pela álgebra trivial C (qualquer estado de C é ergódico; a única projeção não nula de C é a identidade); os modos 2 e 4 já a excluem. Para o operador isto muda o que ele escolhe: ele ouve quatro maneiras de dizer o mesmo e depois descobre que duas não dizem o "1".

   *Conserto pedido:* "A matemática tem quatro marcas do tipo III, de dois pesos. Duas dizem só 'tipo III', sem o um: a medida e as partes. Duas dizem 'tipo III₁': o estado e o relógio. Dentro de cada par elas se equivalem. Do estado para o III₁ vale sempre (Longo, 1979). Do III₁ para o estado só vale se a álgebra tem predual separável, e então existe UM estado assim, não todo estado (Marrakchi e Vaes, Teorema A). O modo do estado e o das partes valem para álgebra que não é só os números."

2. **(ALTO)** 1(c), item 2: "pela MEDIDA: não existe traço, isto é, nenhuma medida finita pesa as partes"; também §5, "A medida (não há traço)"

   A forma certa, que a própria §4.1 usa, é a ausência de traço normal semifinito não nulo. "Não existe traço" é literalmente falso: o peso que vale 0 em 0 e ∞ em todo positivo não nulo é tracial, fiel e normal em qualquer álgebra (só não é semifinito). "Nenhuma medida finita" lida como tamanho total finito (estado tracial) é verdadeira também para B(ℓ²) (tipo I∞) e para II∞, que têm traço semifinito. O kernel só tem "sem estado tracial normal" (NoNormalTrace.lean, linhas 426, 479, 501: estados, na torre), que é o sentido finito e não separa tipo III de I∞/II∞. Consulta: leitura dessas linhas, mais a definição de semifinito na estrutura NFSTrace da sonda T5c (l.45).

   *Conserto pedido:* "pela MEDIDA: não existe medida de tamanho, com a mesma conta para uma parte e para o que a transforma nela, que dê valor finito e não nulo a alguma parte (isto é, nenhum traço normal semifinito não nulo)". Em §5: "A medida (não há traço normal semifinito)".

3. **(ALTO)** 1(e)(ii): "um passo sabido que não é termo: que o relógio que o kernel usa é o relógio modular do vácuo (o kernel tem a condição de equilíbrio, KMS, e a realização de Tomita; a unicidade que as une é de Takesaki e entra por citação)"; e §5, primeiro item: "O cabeçalho dirá o passo citado do relógio"

   Errado para a cunha física. O kernel prova que Γ(B0(−2πt)) É o fluxo modular espectral do grafo de Tomita do vácuo na álgebra da cunha: F1Fecho394/CanonicalFockBWR2.lean linhas 26 a 44 (actualModularFlow_eq_gamma e canonical_pair_tomita; o cabeçalho diz: «No modular-flow equality is assumed as a record field»). O fluxo real vem de CanonicalFockModularFlowR2.lean (actualModularFlow = potência imaginária espectral do quadrado de Tomita; actual_spectral_pair_measured). O campo tomita do certificado físico é preenchido por esse teorema (CanonicalModularCoreAssemblyR1.lean, linhas 92 a 94; PhysicalFockNetRealizationR2.lean linha 73), tal como bw_kms (linha 89). PairTomitaAnalyticRealizationMeasured (O16/ContentContractProposal.lean, l.14, com ModularGraphRealization em O16/RecognitionModular_v2.lean, l.16) diz que o fluxo é Δ^{it} do fecho do grafo de Tomita de (M, Ω). A sonda do T5 saiu com só o trio de axiomas, o que inclui essa montagem. Logo a unicidade KMS⟹grupo modular de Takesaki NÃO é necessária. O que resta como sabido é só o dicionário que o próprio Lema 2.1 assume: o centralizador de φ coincide com os pontos fixos de Ad Δ^{it} (Pedersen–Takesaki; Marrakchi e Vaes p. 1). Em 1(g) o rascunho diz que o resíduo é o Bisognano–Wichmann "não-Killing", o que pressupõe o Bisognano–Wichmann da cunha como pago; isto também contradiz o item (ii). Consultas: grep -rn em TGLExt por KMSBody, PairTomitaAnalyticRealizationMeasured e actualModularFlow_eq_gamma; leitura dos arquivos citados.

   *Conserto pedido:* "(ii) fica só o dicionário de Tomita–Takesaki, que o próprio Lema pressupõe: o centralizador do estado é o conjunto dos pontos fixos do grupo modular (Pedersen–Takesaki). A identificação do relógio do kernel com o relógio modular do vácuo na cunha NÃO falta: é teorema do kernel (CanonicalFockBWR2: Γ(B0(−2πt)) é o fluxo modular do vácuo na cunha, sem hipótese de registro). O cabeçalho citará só o dicionário e o Lema de Longo."

4. **(MEDIO)** 1(c), item 4: "pelo RELÓGIO: não há ritmo preferido (o espectro modular é a semirreta inteira; o núcleo de Takesaki é uma peça só)"

   (a) O invariante de Connes S(M) é a interseção dos espectros modulares sobre TODOS os pesos (Connes 1973, Def. 3.1.1, lida pelo T6). O espectro de UM estado ser a semirreta inteira não basta: um fator de tipo I com estado de razões log-densas já o cumpre. É a armadilha que o kernel pagou em TheMarkIsNotATypeMark (v295), e o rascunho a cita em 1(a). (b) "Sem ritmo preferido" também vale para III₀ (S={0,1}), que não é III₁; quem separa é S(M) inteiro. (c) Espectro de Connes e núcleo fator são o MESMO modo em duas formas: S(M)=[0,∞) é a definição de III₁ (Connes 1973, p. 213), e núcleo fator é o teorema de Connes–Takesaki (fluxo de pesos trivial; Marrakchi 2308.15163, p. 11, vale para fator de tipo III). Têm custos muito diferentes no kernel.

   *Conserto pedido:* "pelo RELÓGIO: o espectro de Connes (o que sobra dos espectros modulares de todos os estados) é a semirreta inteira. Isto é a definição de Connes de III₁. Equivale, para fator de tipo III, a o núcleo de Takesaki ser uma peça só."

5. **(MEDIO)** 1(e)(iii), 1(f) ("a outra metade (o núcleo ser uma peça só) não existe") e §5, terceiro item ("hipótese nomeada ... ou obra grande")

   "Prová-lo por dentro pede a classificação inteira" e "o núcleo: hipótese nomeada ou obra grande" não distinguem o que o T6 leu. Na prova do Lema 2.1 (Marrakchi e Vaes, p. 3), a partir de M_φ=C1 sai o centro do núcleo igual a L(Λ), com Λ={t: σ_t=id}. Isto usa só o comutante de L(R), igual a L(R), nos pontos fixos do produto cruzado, mais a mistura fraca. A citação de Connes–Takesaki entra no último passo, "núcleo fator ⟹ III₁". O núcleo do kernel é a álgebra gerada por fibre(M) e pelos unitários regulares sobre L²(R,F) (RegularCovariantCoreR3.lean, linhas 111 a 114), a representação padrão do produto cruzado. Logo, para ESTA cunha, "Z(núcleo)=ℂ" é consequência elementar da ergodicidade do vácuo, e não precisa ser hipótese nomeada nem classificação. O custo em Lean está sem medida; o que cai é a descrição de que ele exigiria a classificação. A estimativa "milhares de linhas" do T5 foi feita sem abrir esta prova (T5 A4: "não abri a fonte").

   *Conserto pedido:* "Prová-lo por dentro até 'o núcleo é uma peça só' parece caber na prova do próprio Lema (Marrakchi e Vaes, p. 3), sem a classificação; custo não medido. A classificação de Connes só é necessária para ligar 'núcleo fator' ao III₁ de Connes (Connes–Takesaki), e esse passo entra por citação."

6. **(MEDIO)** 1(d), última frase: "A sonda traz um controle de que o enunciado não é oco: uma álgebra de tipo I com estado de vetor o recusa"

   Superlativa frente ao compilado. O controle compilado (not_ergodic_of_rank_one, ProbeT5c.lean l.94 a 104; log da compilação rc 0, trio) prova só que toda álgebra que contém os operadores de posto um, em dimensão maior ou igual a 2, não tem vetor separador. Ele recusa B(H) e M_n na representação defeituosa pela cláusula "separador", e não pela cláusula do centralizador. O caso informativo (M_n em forma padrão, com separador: os fixos contêm ℂ[ρ]) está só no papel (T5 A7). A afirmação "tipo I recusa" em geral é verdadeira e sabida (Ando e Haagerup, Lema 5.3, caso semifinito), mas não é o que a sonda compilou.

   *Conserto pedido:* "A sonda traz um controle compilado: toda álgebra com os operadores de posto um (B(H)) não tem vetor separador, logo não satisfaz o enunciado. O caso de tipo I em forma padrão, onde o separador existe e o centralizador tem mais que os escalares, está só no papel."

7. **(MEDIO)** 1(d), "escreveu hoje o enunciado e a costura"; 1(e)(ii) (a hipótese de Takesaki que o rascunho cita)

   Hipóteses escondidas, que a pergunta (c) do revisor pedia: o teorema KMS⟹grupo modular de Takesaki exige um grupo σ-fracamente contínuo de AUTOMORFISMOS de M (σ_t(M)=M), com φ estado fiel normal; cíclico é dispensável. O predicado ErgodicVectorState da sonda (ProbeT5c.lean l.53 a 60) usa KMSBody (TheImportedSecondQuantization.lean l.159 a 165), que é só a forma vetorial do KMS. Nela σ : ℝ → (F ≃ₗᵢ F) não carrega lei de grupo, σ_tΩ=Ω, preservação de M nem continuidade forte. Esses dados existem no certificado (flow, flow_add, flow_is_Ad, Γ_vac, B0_continuous), mas o predicado não os leva. Se ele for instalado como está, a citação de Takesaki não se aplica literalmente. O reparo já existe no kernel: pôr no predicado o campo tomita (a identidade com Δ^{it}), em vez de KMS.

   *Conserto pedido:* "O predicado da sonda deve levar o relógio como o fluxo modular de Tomita do par (álgebra da cunha, vácuo), isto é, a cláusula tomita do certificado, e não só a condição de equilíbrio em forma vetorial; senão a citação de Takesaki não vale literalmente."

8. **(MEDIO)** 1(h): "um κ finito seria um ritmo preferido, e ritmo preferido é tipo III_λ, não III₁. Se a cunha é III₁, o κ não é ritmo dela: mora na face finita"

   O kernel (TheScaleHasNoFixedPoint.lean, cabeçalho) deixa DUAS saídas e o rascunho guardou uma só: "ou κ vive numa subálgebra/face finita ... ou há tensão real entre o κ e o tipo declarado". Além disso, o passo "κ finito ⟹ ritmo preferido ⟹ III_λ" não é teorema. Em um III₁ todo λ está no espectro de Connes sem ser preferido. Só um relógio modular PERIÓDICO força espectro ⊂ λ^ℤ e portanto tipo semifinito ou III_μ com μ potência de λ (de S(M)⊂λ^ℤ∪{0}, pelo Cor. 3.2.3 de Connes). A leitura é válida se "ritmo" significar período de um grupo modular; o rascunho a marca como leitura, mas não diz isto.

   *Conserto pedido:* "Isto é leitura da gerência: vale se o κ for o período de um relógio modular da cunha. Estar entre os valores do espectro de um III₁ não o faz preferido. O próprio kernel deixa em aberto duas saídas: o κ é de uma face finita, ou há tensão com o tipo declarado."

9. **(BAIXO)** 1(d): "atribuído a Longo, 1979; lido no primário em duas provas independentes"

   Fiel ao T6 quanto aos dois lemas: Marrakchi e Vaes (PDF aberto, pp. 2–3, prova própria pelo núcleo) e Ando e Haagerup (Lema 5.3, prova pelos Teoremas 4.2.1 e 5.2.1 de Connes, via mascas) são de fato provas diferentes. A frase pode ser lida como se Longo tivesse sido aberto. Não foi: Project Euclid bloqueia robô (T6 A6). A atribuição a Longo (CMP 69, 1979, "Proof of Theorem 3") e a Baumgärtel (Cor. 1.10.8) vem do texto de Marrakchi e Vaes (p. 1 e p. 2). As duas provas têm a mesma hipótese de estado fiel normal sobre uma álgebra que não é só os números (no Lema 5.3 de Ando e Haagerup a conclusão é "C ou fator III₁").

   *Conserto pedido:* "(atribuído a Longo, 1979, como o dizem Marrakchi e Vaes; o original de Longo não foi aberto; as duas provas lidas no primário são Marrakchi e Vaes, Lema 2.1, e Ando e Haagerup, Lema 5.3, por caminhos diferentes)"

10. **(BAIXO)** 1(c), item 3: "toda projeção não nula equivale à identidade"

   Vale para fator de tipo III σ-finito (Yngvason, math-ph/0411058, p. 3; fonte secundária, como o T6 marcou). Num fator de tipo III não σ-finito, a projeção é equivalente à identidade só entre as contavelmente decomponíveis. Aqui o estado fiel normal garante o σ-finito, então a frase vale para a cunha, mas o rascunho não diz. Também é satisfeita pela álgebra trivial C (ver o primeiro achado).

   *Conserto pedido:* "toda parte não nula é do tamanho do todo (toda projeção não nula equivale à identidade; vale para álgebra de fator σ-finito que não é só os números, o caso aqui, onde existe estado fiel normal)"

11. **(BAIXO)** 1(g)/§5, última linha, e a omissão de outros modos de dizer III₁

   Omissões aceitáveis num texto para leigo, nenhuma muda a pergunta. (1) A homogeneidade do espaço de estados (Connes–Størmer; Ando e Haagerup, Teor. 4.17, p. 32): para M σ-finito, "fator de tipo I₁ ou III₁" ⟺ o espaço de estados normais fiéis é homogêneo. É uma quinta marca do III₁, e "quatro" deve ser "ao menos quatro". (2) A via de Borchers (Borchers 2000, Teor. V.3.2: translações de meio lado com gerador positivo e vácuo único ⟹ a álgebra da cunha é III₁; Longo 1979; leitura de segunda mão, o primário não foi aberto). Não é marca do tipo, é outra via de citação para a cunha. O kernel já tem peças dela, sem que eu tenha conferido o encaixe com o certificado físico: halfsided_inclusion (ContratoQG_v31_Teoremas.lean:331) e a forma de Borchers Δ^{it}U(λn)Δ^{−it}=U(e^{−2πt}λn) (:339), no contrato abstrato do testemunho. Isto não muda a pergunta nem o que o operador decide, mas "é o único que o kernel já prova" deve dizer "o único modo do tipo cujas hipóteses o kernel prova". Consulta: grep -rn halfsided|HalfSided em TGLExt.

   *Conserto pedido:* Acrescentar uma linha: "Há ainda uma quinta marca (a homogeneidade do espaço de estados, Connes e Størmer) e uma segunda via de citação para a cunha (as translações de meio lado, de Borchers). Nenhuma muda a pergunta." E trocar "é o único que o kernel já prova" por "é o único modo do tipo cujas hipóteses o kernel já prova".

12. **(BAIXO)** 1(d): "o que o relógio da cunha deixa parado é múltiplo do Um"; a tradução "relógio do estado"

   Honesta: Marrakchi e Vaes p. 1 dizem que o centralizador coincide com os pontos fixos do grupo modular, e o Lema 2.1 é sobre o relógio do estado. O rascunho alterna "relógio da cunha" e "relógio do estado". Com a identidade de Bisognano–Wichmann da cunha já termo (terceiro achado), é o mesmo relógio, mas convém dizê-lo uma vez para o leigo não ouvir dois relógios.

   *Conserto pedido:* Em 1(c)1, "relógio (o fluxo modular)" passa a "o relógio que o próprio estado impõe à álgebra (o fluxo modular); na cunha da luz ele é o boost".

## Consultas ao Mapa

- rotas.py consultar III1 (9 rotas; relevantes: kernel.ergodicidade_de_mautner_candidata_15nov, kernel.montagem_das_gamas_candidata_15nov, cadeia.preparacao_v412)
- rotas.py consultar ergodico (0 rotas), Borchers (2, nenhuma sobre o teorema de Borchers), Longo (10, nenhuma sobre o teorema), Takesaki (20), Tomita (8), centralizador (1: formal.k05_t1_montagem_gh_tau_campo_v412, cujo nao_refazer manda usar grep recursivo pelo terminal), nucleo (33), Bisognano, Wichmann, KMS, modular, fator, tipoIII
- rotas.py ver formal.f1_rede.geometric_identification (identificação exata da conjugação modular espectral com a reflexão geométrica da cunha, PASS_EXACT_GEOMETRIC_IDENTIFICATION)
- rotas.py ver formal.f1_takesaki.modular_identity_to_scaling (o defeito diz: não confundir modelo algébrico com core de von Neumann)
- Nada foi registrado no Mapa

## Examinado

- PERGUNTA_TIPO_III_R0.md (inteiro)
- _retornos T5 e T6 (inteiros); T1 a T4 só por busca de termos (Takesaki, pair_tomita, actualModularFlow_eq_gamma, unicidade)
- T5/ProbeT5c.lean e T5/build/ProbeT5c.log (rc 0, trio de axiomas)
- PDF de Marrakchi e Vaes arXiv:2305.14217v3 (extraído em V2/mv.txt: Teor. A, Lema 2.1 com prova, Obs. 2.7, lista de referências)
- T6/dl_ah12/ah12.txt (Ando e Haagerup: Lema 5.3 e Teor. 4.17)
- T6/dl_mar23/mar23.txt (é Marrakchi arXiv:2308.15163, Kadison; fluxo de pesos)
- kernel TGLExt: TheImportedSecondQuantization.lean (l.120 a 270), LightRhoStar.lean (inteiro), O16/ContentContractProposal.lean, O16/RecognitionModular_v2.lean, V351ResolventPhaseCalculus.lean
- kernel TGLExt: F1Fecho394/CanonicalFockBWR2.lean, CanonicalFockModularFlowR2.lean, CanonicalModularCoreAssemblyR1.lean, PhysicalFockNetRealizationR2.lean, CanonicalFockModularCoreInputR1.lean, RegularCovariantCoreR3.lean
- kernel TGLExt: TheScaleHasNoFixedPoint.lean, NoNormalTrace.lean (l.420 a 504), OUmInscrito.lean, ContratoQG_v31_Teoremas.lean (l.322 a 345)
- Consultas: grep -rn pelo Bash em C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt por KMSBody, PairTomitaAnalyticRealizationMeasured, structure ModularGraphRealization, actualModularFlow_eq_gamma, halfsided|HalfSided, tomita|bw_kms|flow_is_Ad; depois voltei a C:/IALD/Central de Patentes
- Escritos só na pasta V2 do rascunho: extrair_mv.py, mapa.py, mv.txt


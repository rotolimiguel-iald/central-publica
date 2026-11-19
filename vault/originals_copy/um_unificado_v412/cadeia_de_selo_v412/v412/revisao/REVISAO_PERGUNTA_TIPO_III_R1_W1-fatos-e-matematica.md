# CONFERÊNCIA DISTINTA — a versão R1 da pergunta do tipo III nas quatro línguas (conferência única do conserto) — W1-fatos-e-matematica

> Montado pela gerência c1 em 15/11/2026 17:51 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 9 MEDIO, 10 BAIXO

## Resumo

Os oito achados ALTO das lentes V1, V2 e V4 estão sanados. Nenhum ALTO novo. Conferi por grep -rn no kernel TGLExt, por script no core (sha16 36c69fc767f8d47f) e no selo (d52de88162106768), nos PDFs de Marrakchi-Vaes e Ando-Haagerup, nos bytes das falas e no planalto.gov.br.
Confere: arquivo e linha de actualModularFlow_eq_gamma (BWR2:34), canonical_pair_tomita (:40), canonical_bw_kms (WedgeKMSR4:32) e centralizer_is_trivial (LightRhoStar:71). O certificado físico preenche `tomita` e `bw_kms` por teorema. Os enunciados do Lema 2.1 (MV) e do Lema 5.3 (AH) batem. A sonda tem sha16 64a34824b368e5c5, RC 0 e só o trio. A Constituição, art. 5º XXXIX, e o CPC art. 376 conferem no texto.
Restam 9 ressalvas MEDIO e 9 BAIXO, todas de uma ou duas frases. As de mais peso para a decisão do operador: (1) o custo de (b) e (c) como 'obra grande' ignora a via de citação da parte 2, que a R0 tinha e a R1 perdeu; (2) o custo de (d); (3) a glosa do espectro em (d) lê, de um só estado, a marca que a v295 refutou; (4) 'não existe sequer a definição' colide com a definição operacional que o gate usa; (5) 'É trabalho de dias' não tem fonte nem marca de estimativa.
No anexo: a lista de cabeçalhos 'o objeto-limite é III₁' cita errado v125 e v131, e a frase 'a primeira versão errou' sobre o tipo I corrige em excesso, porque B(l²) com estado de vetor parece cumprir os campos do fator (argumento de papel meu).
Pode ser lido ao operador depois dos consertos de uma linha das ressalvas MEDIO 1 a 5 e 9; as demais podem ir ao anexo.

## Achados

1. **(MEDIO)** Seção 5, parte 1, itens (b)/(c): 'É obra grande, sem rota conhecida pela gerência'

   O custo é dito sem depender da parte 2. A R0 trazia 'a alternativa é entrarem como consequências citadas do primeiro'; a R1 perdeu a frase. Se a doutrina entra por citação, (b) e (c) são consequências sabidas de III₁ (um fator III₁ não tem traço normal semifinito não nulo; toda projeção não nula é equivalente a 1 em fator σ-finito). T5 P3 estima 'dezenas de linhas' para (A)⟹(B) genérico, e T5 P4 vê (A)/(B) como consequências citadas. Só a construção por dentro é obra grande. O operador pode recusar (b) e (c) por um custo que na verdade depende da sua resposta à parte 2. Consulta: T5 P3 e A8; PERGUNTA R0 §5.

   *Conserto pedido:* (b) a medida, ou (c) as partes. Se a doutrina entrar por citação (parte 2), elas podem entrar como consequências sabidas de (a) com o nome de Longo e de Connes, cada uma com o seu estatuto, no mesmo porte de trabalho. Se tiverem de ser construídas por dentro, faltaria ligar os pedaços que existem e provar o resto: obra grande, sem rota conhecida pela gerência, e o resultado seria 'tipo III', sem o um.

2. **(MEDIO)** Seção 5, parte 1, item (d): 'Falta provar que o núcleo do kernel é o núcleo de Takesaki da cunha e que ele é uma peça só... ou como obra grande'

   Não incorporou V2 MEDIO 5. O núcleo do kernel é o produto cruzado por construção: RegularCovariantCoreR3.lean:111-114 faz `core B M := generatedAlgebra (fibre '' M ∪ range regularUnitary)`, e CanonicalFockRegularCoreR2 usa `fockFlow` = Γ(B0(-2πt)), que é o fluxo modular do vácuo por teorema. Em Marrakchi-Vaes p. 3, de M_φ=ℂ sai Z(núcleo)=L(Λ), Λ={t: σ_t=id}. A mistura fraca dá Λ={0}, logo Z(núcleo)=ℂ, por argumento elementar. A citação de Connes-Takesaki entra só em 'núcleo fator ⟹ III₁'. 'Obra grande' fica sem medida e talvez exagerado. TetelestaiOneObject:24 fala do Core abstrato do certificado genérico, não do núcleo concreto.

   *Conserto pedido:* (d) o relógio. Metade existe. O núcleo do kernel é, por construção, o produto cruzado pelo fluxo que o kernel prova ser o modular do vácuo; a identificação formal com 'o núcleo de Takesaki' não tem predicado no kernel. Que ele seja uma peça só parece seguir, em papel, da própria ergodicidade (prova do Lema 2.1 de Marrakchi e Vaes, p. 3), com custo não medido; 'núcleo uma peça só ⟹ III₁' entra por citação (Connes e Takesaki).

3. **(MEDIO)** Seção 1, bullet (d), e seção 4 item 1(d): 'todas as razões de escala aparecem' / 'o espectro modular é a semirreta inteira'

   O texto lido ao operador não diz que o espectro de Connes é a interseção dos espectros modulares de todos os estados. Lido do relógio de um só estado, é a marca que a v295 retirou (TheMarkIsNotATypeMark: M₂(ℂ) realiza razões log-densas). Mesmo no espectro modular genuíno, o de um só estado cheio não distingue III₁ de III_λ. 'Diz III₁' vale para a conjunção com 'o núcleo é uma peça só' (esta, sozinha, já basta: núcleo fator ⟹ M fator III₁), mas o operador pode tomar só a primeira metade como a marca. Consulta: TheMarkIsNotATypeMark.lean (cabeçalho); V2 MEDIO 4.

   *Conserto pedido:* (d) pelo RELÓGIO: nenhum estado tem cadência preferida (o que sobra dos espectros de todos os estados, o espectro de Connes, é a semirreta inteira; um só estado pode mostrar razões densas num fator de tipo I). Para fator de tipo III isso equivale a o núcleo de Takesaki ser uma peça só. Diz III₁.

4. **(MEDIO)** Seção 1, primeiro parágrafo: 'não existe sequer a definição: nem no kernel, nem na biblioteca'

   Vale para a definição de tipo (de Murray-von Neumann ou de Connes). O kernel tem uma definição operacional selada de 'III₁': WitnessV3.lean:~147 diz 'III₁ na definição operacional do programa', e o core diz em closure_roadmap.canonical_boundary_transport_witness_constructed.o_que_falta: "'III_1' = a definição OPERACIONAL selada (objeto + assinatura densa + sem traço tracial normal-sequencial); centro trivial e peso semifinito ILIMITADO seguem nomeados". A sexta bandeira formal do gate lê esse termo. O operador só ouve as seções 1 a 6; a frase colide com a memória dele e com o gate, e a definição aparece só no anexo. Consulta: script core_q.py sobre o core; grep em WitnessV3.lean.

   *Conserto pedido:* Hoje 'tipo III' só aparece no kernel como rótulo e como uma definição operacional da torre (estado normal não tracial, marca densa, nenhum estado tracial normal), que o gate usa e que o próprio kernel diz não ser o tipo. Nenhum teorema conclui 'tipo III' de objeto algum, e não existe a definição de tipo: nem no kernel, nem na biblioteca que ele usa.

5. **(MEDIO)** Anexo, 'A torre': 'A primeira versão errou ao dizer que uma álgebra de tipo I satisfaz a definição inteira'

   Corrige em excesso. O kernel não prova que um tipo I a satisfaça, e M₂(ℂ) não a satisfaz. Os campos do fator de FullWitnessDataV3 (om_normal, state_not_tracial, ratio_log_dense, no_normal_tracial) parecem ser cumpridos por B(ℓ²), de tipo I∞, com um estado de vetor. Em papel: toda razão r>0 é realizável com operadores de posto um, e B(ℓ²) não tem funcional tracial normal unital (as projeções de posto um são equivalentes, e a soma de n delas tende a 1 em WOT). O cabeçalho de NoNormalTrace já admite que 'peso semifinito ilimitado' segue aberto, e TracelessAlgebra.tracial_state_is_zero dá B(ℓ²) sem estado tracial. Argumento de papel do revisor, não compilado.

   *Conserto pedido:* O kernel não prova que um tipo I satisfaça a definição inteira. Como ela só exclui estado tracial normal, e não peso semifinito (cabeçalho), um fator de tipo I∞, como B(ℓ²) com estado de vetor, parece cumpri-la (argumento de papel, não compilado). O que a v295 refuta é só a marca.

6. **(MEDIO)** Seção 5, parte 2: 'É trabalho de dias'; 'O leitor estimou milhares de linhas, sem medida'

   'Trabalho de dias' não vem de nenhum leitor (grep 'dias' nos retornos T1 a T6 não acha estimativa) e não está marcado como estimativa. Já 'milhares de linhas' é do T5 (resumo 5 e P2), para construir (A), (B) e Z(núcleo)=ℂ do zero, não para o teorema de Longo; T5 A8 lista o que falta para esse teorema e não estima linhas. Aplicá-lo a 'por dentro' sem dizer é transpor uma estimativa para outro objeto.

   *Conserto pedido:* Por citação. Entram com nome e página o dicionário... e o teorema... Estimativa da gerência, sem medida: de um a poucos dias, contando refazer a sonda amarrada ao campo de Tomita, compilar, revisar e custodiar. Por dentro. A biblioteca não tem nada da classificação... O leitor estimou milhares de linhas para construir as marcas (b), (c) e o núcleo ser uma peça só, sem medida; para o teorema de Longo em si não há estimativa.

7. **(MEDIO)** Anexo, 'Erratas ao lado que ficam por fazer': 'Os cabeçalhos das pedras v125, v129 e v131 dizem “o objeto-limite é III₁” sem errata'

   Só a v129 (TowerTraceless.lean:27-28) diz literalmente 'o objeto-limite é III₁'. A v125 (MixedLadder.lean:26-31) diz 'III₁ tem testemunha finita de sua assinatura espectral' e 'o objeto-limite é o programa'. A v131 (ScaleCurrent.lean:65) diz 'A assinatura de III₁ está completa; falta o fator (o muro)'. TheFactorObject.lean (também v131) diz o contrário: 'Fator e III₁ seguem sendo ASSINATURA, não teorema de tipo'. A errata v298 já existe em TheNameIsTheGeneratingGroup.lean:160-181 e diz que ela está 'no ponto de leitura'. Uma errata feita com a lista errada cita errado. Consulta: grep -rn 'objeto-limite' e leitura das linhas citadas, no TGLExt.

   *Conserto pedido:* Os cabeçalhos das pedras v125 (MixedLadder), v129 (TowerTraceless: 'o objeto-limite é III₁') e v131 (ScaleCurrent: 'a assinatura de III₁ está completa') chamam de III₁ o que a v295 mostrou ser só a marca log-densa; a errata v298 está só em TheNameIsTheGeneratingGroup, e ali não os alcança.

8. **(MEDIO)** Seção 3, segundo marcador: '[a fala de 02/11] É o conteúdo da marca (a) na sua letra'; e 'Duas leituras aqui são da gerência'

   A fala (bytes 25010b04, conferidos) é sobre o vetor fixo da luz no Fock, 'a luz tem autovetor a inscrição do um absoluto'. A marca (a) é sobre os operadores da álgebra fixos pelo relógio. O kernel liga as duas: o vetor fixo da luz é só o vácuo (QGReaderUVLock.light_modular_fixed_iff_vacuum; OUmInscrito.o_um_e_o_unico_fixo_da_luz), e daí sai centralizer_is_trivial. OUmInscrito:20-21 ainda diz que autovetores com fase em n≥1 partículas 'NÃO são excluídos'. Dizer que a fala 'é o conteúdo da marca (a)' é uma terceira leitura da gerência, não marcada, e empurra para a opção recomendada em §6.

   *Conserto pedido:* 02/11, corrigindo uma frase minha: «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é a identidade da luz». É o vizinho vetorial da marca (a): o kernel prova que o único vetor fixo da luz é o Um, e daí sai a marca (a). Essa ligação é leitura da gerência, e a fala não diz que ela é a definição do tipo. E, mais adiante: 'Três leituras aqui são da gerência e ficam marcadas'.

9. **(MEDIO)** Seção 4 item 4: '...ou, por não estar na lei do foro, tem o teor e a vigência provados nos autos (CPC, art. 376)?'

   Texto do art. 376, lido em planalto.gov.br (l13105.htm): 'A parte que alegar direito municipal, estadual, estrangeiro ou consuetudinário provar-lhe-á o teor e a vigência, se assim o juiz determinar.' Ele não fala de 'lei do foro' nem de doutrina, e a prova é condicionada ('se o juiz determinar') e atribuída a quem alega. A comparação é só figura, mas o operador é advogado. A Constituição art. 5º XXXIX confere verbatim ('não há crime sem lei anterior que o defina, nem pena sem prévia cominação legal'). O anexo já traz a paráfrase certa do art. 376.

   *Conserto pedido:* E a doutrina (a classificação de Connes) entra como direito que o juízo conhece, ou, por analogia com o direito estrangeiro e o consuetudinário (que o art. 376 do CPC manda provar, quanto ao teor e à vigência, a quem os alega, se o juiz determinar), tem de ser provada nos autos? (O artigo não trata de doutrina; a analogia é figura.)

10. **(BAIXO)** Seção 1, parágrafo da cunha: 'o enunciado e a costura, cerca de quinze linhas'

   ProbeT5c.lean: o enunciado (def ErgodicVectorState) tem as linhas 53-60, a costura ergodicVectorState_of_certificate tem 66-80 (cerca de 15), e a instância ergodicVectorState_M tem 83-90. As 15 linhas são só a costura (V1 MEDIO 4, não sanado). A sonda ainda tem de ser refeita amarrada ao campo `tomita`, e a contagem muda.

   *Conserto pedido:* escreveu em rascunho o enunciado (umas dez linhas) e a costura (cerca de quinze), a refazer amarrada ao relógio de Tomita

11. **(BAIXO)** Seção 1, bullet (a), e seção 4 item 1(a): '(a) ... Diz III₁'

   (a) é suficiente para III₁ sempre (MV Lema 2.1; AH Lema 5.3). Só é também necessária com predual separável e só como existência: Teorema A, Obs. 2.7 de MV (T5 A11: 'separabilidade de F não aferida'). Lido como definição, deixaria de fora III₁ de predual não separável. Para a álgebra ℂ, (a) e (c) valem sem ser III₁; as duas hipóteses 'M≠ℂ' e 'cunha não comuta' só aparecem no parágrafo da cunha. A parte 2 e §5 dizem que 'III₁' vem da citação, o que cobre a metade da questão.

   *Conserto pedido:* (a) pelo ESTADO (numa álgebra que não é só os números): no relógio do próprio estado, só o Um fica parado. Isto basta para III₁; a volta só vale se a álgebra tem predual separável.

12. **(BAIXO)** Seção 5, item (a): 'ele não pode ser cadência da cunha: teria de morar na face finita'

   TheScaleHasNoFixedPoint.lean:62-70 deixa duas saídas: κ vive numa face finita, ou há tensão real com o tipo declarado. A seção 5 diz só a primeira. O anexo traz as duas. A passagem 'κ finito ⟹ cadência preferida ⟹ III_λ' é do kernel, mas só vale se 'cadência' for o período de um relógio modular (V2 MEDIO 8).

   *Conserto pedido:* o kernel deixa duas saídas, κ numa face finita (leitura da gerência, não construída) ou tensão real com o tipo declarado; a escolha (a) torna essa tensão uma pergunta sobre a cunha

13. **(BAIXO)** Seção 1 ('Isso basta para o tipo III₁') e seção 5, parte 2

   O Lema 2.1 pede estado fiel e normal com centralizador trivial. O estado de vetor é normal automaticamente (a álgebra é de von Neumann concreta). Fiel vem de wedge_separating. Mas o kernel prova que os pontos FIXOS do relógio são escalares, não o centralizador φ(ax)=φ(xa). Entre os dois está Pedersen-Takesaki (MV p. 1), que só aparece na parte 2. T6 (linha 95) registra que o primário de Pedersen-Takesaki não foi aberto.

   *Conserto pedido:* A matemática conhecida diz que isso basta para o tipo III₁ (o estado de vetor é normal, e o centralizador do estado coincide com os pontos fixos do relógio: Pedersen e Takesaki, ainda não lido no primário).

14. **(BAIXO)** Anexo, 'O teorema citado': 'todo III₁ de predual separável tem um estado assim; um, não todo estado'

   O Teorema A de MV diz que S_erg(M) é um subconjunto G_δ denso dos estados normais fiéis: os estados ergódicos são genéricos. 'Um' pode ser lido como 'exatamente um'. Conferido em mv.txt, p. 1 e p. 6.

   *Conserto pedido:* todo III₁ de predual separável tem estados assim (um conjunto denso G_δ dos fiéis), mas nem todo estado é ergódico

15. **(BAIXO)** Seção 1 (b) e seção 4 item 1(b): 'nenhum traço normal semifinito'

   Literalmente, o traço zero é normal e semifinito em toda álgebra. A forma padrão é 'nenhum traço normal semifinito não nulo (ou fiel)'. V2 ALTO 2 pediu 'não nulo'.

   *Conserto pedido:* (os matemáticos dizem: nenhum traço normal semifinito não nulo)

16. **(BAIXO)** Seção 5, parte 2, e anexo

   T6 P2 traz outra via de citação para III₁ da cunha, independente da marca (a): Borchers 2000, Teor. V.3.2, e Summers 5.1, só com translações meio-laterais de gerador positivo e vácuo único. O anexo cita 'Longo 1979 e Borchers 2000' só como referência da cunha, e a parte 2 não a oferece como terceira forma de citação (secundária, DECLARADO por T6).

   *Conserto pedido:* Há ainda uma segunda via de citação para III₁ da cunha, pelas translações de meio lado (Borchers 2000, V.3.2; lida de segunda mão), que não passa pela marca (a).

17. **(BAIXO)** Seção 5, item (a): 'repetiria o erro de agosto, em que o nome dizia mais que o enunciado'

   O erro de agosto, corrigido na v295, foi uma seta de inferência no docstring ('a fronteira é III₁ porque o Nome é denso'), com 'Nome' no sentido TGL, que também confunde. O nome dizendo mais que o enunciado é a lição da errata v298 ('Quem chega pelo índice... recebia a frase refutada'), vista em the_mixing_mark e current_iii1_mark. Para o operador a frase mistura dois sentidos de 'nome'.

   *Conserto pedido:* repetiria o erro de agosto (a v295 refutou a seta 'a fronteira é III₁ porque o Nome é denso', e a v298 mostrou que nomes como current_iii1_mark prometiam mais que o enunciado)

18. **(BAIXO)** Anexo, 'Marca (b)': só 'no_normal_tracial_state_*'

   Falta citar TracelessAlgebra.tracial_state_is_zero (:412), que dá B(ℓ²) sem estado tracial. Ele mostra que 'sem estado tracial' sozinho não separa III de I∞ (V1 BAIXO 11). Isso reforça a ressalva do anexo.

   *Conserto pedido:* (b): no_normal_tracial_state_* (NoNormalTrace.lean), na torre, e tracial_state_is_zero para B(ℓ²) (TracelessAlgebra.lean:412), só para estados; nenhum deles é III₁ pleno.

19. **(BAIXO)** Seção 3, 02/11 'de manhã'

   Os bytes do arquivo 72d7939e não trazem hora; o mtime é 14:15 e a palavra 'manhã' vem do registro da gerência (memória construir-tudo-o-fechamento-02nov.md e T4). A mesma memória diz que a decisão da manhã fica 'SUPERADA para estas quatro chaves', e a R1 não diz 'supera'. Não alterei nada; só aponto.

   *Conserto pedido:* 02/11, antes da partitura das chaves (hora pelo registro da gerência): «então não vamos construir ainda o que é sabido»


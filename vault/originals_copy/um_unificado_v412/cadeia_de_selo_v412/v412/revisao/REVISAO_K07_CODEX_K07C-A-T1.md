# CONFERÊNCIA DISTINTA — a entrega K07-C do Codex — K07C-A-T1

> Montado pela gerência c1 em 15/11/2026 18:24 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 MEDIO, 6 BAIXO

## Resumo

1. As duas candidatas Lean da T1 recompilam em copia (Lean 4.31.0, binario direto sobre os .olean do sandbox, sem lake): RC 0, zero avisos, zero sorry/native_decide/axiom na fonte, e #print axioms so propext, Classical.choice, Quot.sound nas 7 (Gaussian) + 3 (Semigroup) declaracoes. Os .olean que gerei sao bit-identicos aos do Codex (sha16 7a7213bd... e 4c1750d5...). Os 37 sha256 da tabela da ENTREGA conferem por script, 0 divergencias.
2. Vacuidade: 13 mutacoes (7 no Gaussian, 6 no Semigroup: sinal do expoente, /2 por /4, tirar hv, tirar hsa/hcontract/hadd, trocar forall por exists em hF, limite por x, ponto medio por /3, Injective por Surjective, tirar Commute) derrubaram a compilacao 13 de 13. Sonda propria compilou (RC 0): o semigrupo T 0 = id, T t = 0 (t>0) em C satisfaz contracao, autoadjunto e lei de semigrupo, com espaco fixo {0} diferente do todo. As hipoteses sao habitaveis por objeto nao trivial e todas sao usadas.
3. O que o Lean prova, em lingua simples: (a) a media gaussiana de fases e o multiplicador exp(-v d^2/2); (b) a entrada (i,j) da media de conjugacoes por fases diagonais e esse multiplicador vezes x_ij (fecha o que a K05 R2 so tinha por definicao); (c) a gaussiana N(0,v), v>0, carrega todo aberto; (d) em dimensao finita, todo elemento do comutante de diag(k) e polinomio em diag(k) se e so se k e injetiva; (e) um semigrupo de contracoes autoadjuntas converge forte a projecao sobre os fixos comuns, sem calculo espectral e sem continuidade temporal. Sao INGREDIENTES: nenhum toca o Lema C (Digernes-Takesaki), o Lema B (traco e esperanca), o Lema A em produto cruzado, H_K-chapeu, a passagem L2 para L1 ou a identificacao do fixo com a esperanca. O cabecalho e a errata nao prometem alem disso.
4. Nao ha duplicacao do kernel nem da candidata ErgodicidadeDeMautner (grep -r em TGLExt: nenhum commutant_generated, selfadjoint_semigroup, aeval_diagonal; a candidata da gerencia usa medias de Cesaro de isometrias, enunciado distinto; Mathlib tem Birkhoff/mean-ergodic de uma contracao, nao o semigrupo autoadjunto). Mas tres das sete do Gaussian sao reempacotamento: scaled_weight_multiplier e gaussianWeight_fourier do kernel com c = raiz de 2v; gaussian_phase_integral e charFun_gaussianReal do Mathlib; gaussian_positive_on_opens e uma linha de Mathlib. Musculatura real: gaussian_conjugation_entry, commutant_generated_iff_injective e o Semigroup.
5. Proposicao da cunha conferida no kernel por grep -rn: LightRhoStar.lean:71 centralizer_is_trivial; F1Fecho394/CanonicalFockModularCoreInputR1.lean:126 physicalFockCertificate e :144 physical_net; TheImportedSecondQuantization.lean:217 bw_kms, :223 tomita, :229 flow_is_Ad, :439 light_kms. Rodei #print axioms nos dois (so o trio) e #check: o enunciado recebe a em R(cunha direita), C.flow t a = a para todo t, e devolve c com a = c.1; R devolve VonNeumannAlgebra (fechada fraca). A frase da cunha e REAL.
6. Prova de (4) no papel (T1_R3, 2c): refiz. Lema C (comutante de lambda(R) em M-hat = M_phi barra-tensor D por Digernes-Takesaki mais fatias, com D maximal abeliana e Ad rho trivial sobre D) esta certo. Lusin-Souslin mais Doob-Dynkin: W*(F(h)) = D se e so se F injetiva num boreliano conulo (necessario e suficiente), certo. Com K-chapeu afiliado a D, W*(K-chapeu) = centralizador do peso dual equivale a H_K-chapeu sob H_erg: certo. Prova gaussiana direta (convolucao, norma L1 da diferenca <= |r| sqrt(2/(pi beta n t))): conferi a constante. Traco tau(f(h)) = phi(1) int f e^{-p} dp, tau(e_i) = phi(1)(e^i - e^{-i}), tau(d) = e sqrt(pi): conferido. Dupla covariancia (c e^{a p} tem carater e^{-a s}; e^p + e^{2p} nao tem) certa, e corrige o erro da revisao K05. A paridade (N = M_phi barra D mesmo com W*(K-chapeu) menor que D, por enumerabilidade das frequencias e Hilbert separavel) e coerente; e a parte mais delicada e nova, so em papel, [DERIVED] sem revisor previo.
7. Hipoteses usadas pela prova: estado normal FIEL com phi(1) finito (M sigma-finita); H_erg (M_phi = C1, para ESTE estado); K-chapeu >= 0 afiliado a D e F boreliana injetiva num conulo (H_K-chapeu); beta > 0; para a paridade, representacao standard separavel. O que e KNOWN e entra por citacao: Digernes-Takesaki, dualidade de Takesaki (tau escala por e^{-s}), criterio de Takesaki e esperanca de Umegaki, Segal-Dixmier, Lusin-Souslin. Pedersen-Takesaki e Connes-Takesaki NAO aparecem em T1_R3 nem na errata (o centralizador entra como algebra fixa do grupo modular, por definicao). O documento NAO diz quais fontes foram lidas no primario; a revisao K05 (secao 10) dizia que Digernes-Takesaki so tinha sido conferido via Andreou (secundario) e que Takesaki 1972/1973 nao foram conferidos, e a R3 nao acrescenta leitura primaria declarada.
8. A frase da ENTREGA ('para estado normal fiel e centralizador escalar, a hipotese sobre o gerador positivo equivale a geracao de todo o centralizador do peso dual; transportar a igualdade da sombra e premissa adicional') esta matematicamente certa como equivalencia. A parte 'premissa adicional' e UMA leitura do Axioma E, e o documento nao diz que ha outra no texto do Artigo (achado MEDIO abaixo).
9. A escolha fisica (c e^{h} contra e^{h} + e^{2h}, leitura de 'nao-covariancia' do Artigo l.1914) esta dita sem decidir pelo operador, em T1_R3 e no ultimo [OPEN] de PERGUNTA_K07_CODEX. Mas so em jargao (carater sob a acao dual) e fora das 15 linhas da ENTREGA.
10. ORDEM e ADENDO B, cumprido: caixa em tres blocos com o teorema do kernel citado por nome e arquivo; resido BW nao-Killing com o nome do Artigo e sem estender ao horizonte; 2c decidida com prova escrita; Lemas B e C e Lema A (duas provas) em papel; T1_R2.lean arquivada com nota; os quatro itens L1 P5/P6/P7/suporte total viraram candidatas Lean; face de kernel dos lemas de redacao (dominio multiplicativo; convergencia so em vetores) dita. Nao cumprido ou parcial: o Lema A continuo, o Lema C, o Lema B e a convergencia no predual NAO tem face Lean (a propria errata o diz, e a ordem nao exigia); a identificacao de P_fix com a esperanca no canto e papel; o composto finito 'Fix da media gaussiana = comutante = algebra polinomial' nao esta num so termo Lean.
11. Linguagem: nenhuma fala atribuida ao operador (sem aspas angulares; 'autor' so para o Artigo), nenhuma palavra proibida da creditacao, beta simbolico, estatutos marcados, nada instalado, nada escrito fora da pasta.
12. Veredito: matematica da T1 e candidatas Lean sao solidas e honestas no alcance; as ressalvas sao de completude de leitura do Artigo e de linguagem ao operador, nao de erro.

## Achados

1. **(MEDIO)** K07/CODEX/T1_R3.md l.3 e l.30 (item 4 de 2c); kimi/ENTREGA_K07_CODEX.md l.4; kimi/REGISTRO_MAPA_K07_CODEX.json campo resultado

   A resposta a 2c ('H_K-chapeu e o Axioma E transcrito? onde difere') omite uma leitura textual do proprio Artigo. O teorema da Terminalidade (A Ponte Einstein Cartan Miguel.tex l.1437-1442) escreve 'algebra de pontos fixos C = Fix(Phi_t) invariante pelo fluxo modular' em geral, nao so na sombra, e l.1454-1458 diz que o setor da verdade 'E a fatia espacial do Axioma E'. Com C := Fix(Phi_t), o Axioma E em M-hat diz Fix(Phi_t) = W*(K-chapeu), que pelo Lema A (e pelo 'Controle da necessidade' do proprio Codex) equivale a W*(K-chapeu) = D e D'∩M-hat = D, isto e, H_K-chapeu mais H_erg, sem 'transporte da sombra'. T1_R3 diz que a identificacao com TODO o centralizador 'aparece expressamente na sombra' (l.2013-2018) e a ENTREGA conclui 'premissa adicional' como se fosse a unica leitura. Consulta: grep -n -i 'terminalidade|1437|1439|Frigerio' em T1_R3.md, ERRATA_T1_K07_CODEX.md, REVISAO_INDEPENDENTE_R3.md, ENTREGA_K07_CODEX.md, PERGUNTA_K07_CODEX.md, revisao/REVISAO_K05_T1.md e kimi/T1_FECHADO.md devolveu zero ocorrencia; no .tex, l.1437-1442 existe. Qual leitura de C vale (so gerado por K, Fix(Phi_t) por nome, centralizador inteiro da sombra) e escolha do autor e esta escondida como fato derivado.

   *Conserto pedido:* Acrescentar ao 2c, ao lado, as tres leituras do Axioma E (C gerado por K_partial; C = Fix(Phi_t) pela Terminalidade l.1437; C = centralizador inteiro pela sombra l.2013) e o que cada uma da: so a segunda e a terceira forcam H_K-chapeu; a segunda forca tambem H_erg. Dizer ao operador, em lingua dele, que a escolha e dele. Corrigir 'premissa adicional' para 'premissa adicional sob a primeira leitura'.

2. **(BAIXO)** K07/CODEX/T1_R3.md l.27-29, l.76; ERRATA_T1_K07_CODEX.md

   O documento nao declara quais fontes citadas foram lidas no primario. Digernes-Takesaki entra por Takesaki II (DOI) e por Andreou p.14 (secundario, que cita Takesaki II cap. X cor. 1.22); a revisao K05 (REVISAO_K05_T1.md secao 10) ja dizia que Takesaki 1972, 1973 e Digernes-Takesaki nao foram conferidos no primario, e a R3 nao traz leitura primaria nova. Pedersen-Takesaki e Connes-Takesaki nao aparecem em T1_R3 (grep -n -i 'pedersen|connes.takesaki' devolve zero; a K05 citava Connes-Takesaki 1977 para c_phi e a R3 o descartou sem dizer). Dois rotulos de link nao conferem pelo que se ve: '[Kechris, prova de Lusin-Souslin]' aponta para CDST-corrections.pdf (lista de correcoes do livro, pagina 2) e '[Segal, integracao nao comutativa]' para mathnet.ru/eng/mat209. Nao abri os links (WebFetch roda modelo; a regra proibe); fica nao conferido por mim.

   *Conserto pedido:* Acrescentar uma linha por fonte: lido no primario, lido em secundario (qual), ou so metadados. Marcar Digernes-Takesaki, Takesaki 1972/1973 e Umegaki como [KNOWN, nao lido no primario] enquanto for o caso.

3. **(BAIXO)** K07/CODEX/T1_R3.md l.32; PERGUNTA_K07_CODEX.md ultimo [OPEN]; ENTREGA_K07_CODEX.md (15 linhas)

   A escolha fisica da T1 (K-chapeu = c e^{h} contra e^{h} + e^{2h}; leitura de 'a nao-covariancia de raiz de K-chapeu sob a acao dual' do Artigo l.1914) esta dita sem decidir, mas so em jargao (transformacao por carater sob a acao dual) e nao aparece nas 15 linhas da ENTREGA. Pela regra do posto, o operador precisa ler a escolha na lingua dele antes de qualquer trabalho que dependa dela. Nota de leitura: 'nao-covariancia' e a negacao de 'covariancia', o que, lido ao pe da letra, favorece a segunda leitura (sem carater), sob a qual o 'candidato natural' c e^{h} da revisao K05 FALHA; o Codex lista as duas leituras sem pender, correto, mas o documento nao avisa que o candidato mais citado cai sob a leitura mais literal.

   *Conserto pedido:* Gerencia traduz ao operador: 'qual operador faz o papel de K no produto cruzado: um que muda de escala quando o nucleo e deslocado (e^h) ou um que nao muda por fator simples (e^h + e^{2h})? Os dois fecham a matematica; a escolha e fisica e e sua.' Incluir uma linha disso na ENTREGA.

4. **(BAIXO)** T1GaussianSpectrum.lean l.20-49 (scaled_weight_multiplier, gaussian_phase_integral, gaussian_positive_on_opens)

   Tres das sete declaracoes sao reempacotamento: scaled_weight_multiplier e gaussianWeight_fourier (F1Fecho394/GaussianProbabilityKernelR4.lean:40, com c = raiz de 2v, conferido) ; gaussian_phase_integral e charFun_gaussianReal de Mathlib; gaussian_positive_on_opens e uma linha de gaussianReal_absolutelyContinuous'. O errata as descreve com exatidao ('aplica gaussianWeight_fourier da casa'), sem inflar. Musculatura real so em gaussian_conjugation_entry, commutant_generated_iff_injective e em T1SemigroupProjection.

   *Conserto pedido:* Nenhum bloqueio. Se instalar, instalar so as quatro de musculatura (ou as tres ligadas ao tipo) e citar as outras.

5. **(BAIXO)** T1GaussianSpectrum.lean l.54-60, l.93-127; ERRATA_T1_K07_CODEX.md bullet 'aeval_diagonal'

   Nao ha termo que componha o fato finito inteiro: phaseMatrix usa Real.sqrt (k i) com k real sem hipotese 0 <= k (raiz de negativo vale 0, o teorema continua verdadeiro para a definicao), e commutant_generated_iff_injective fala de diagonal k com k complexa, injetiva em k, nao em raiz de k. Nenhum teorema liga 'Fix da media gaussiana' a 'comutante de diag k' (isso esta so no T1_R2.lean arquivado, fixed_gaussianFlow_iff, com hipotese k >= 0). Alem disso a errata afirma 'esta algebra ... coincide com W*(K) nessa base', mas o Lean enuncia polinomios (aeval), nao W*(K); o passo de fechamento por involucao e prosa (verdadeiro: Lagrange sobre os valores distintos).

   *Conserto pedido:* Dizer na errata que o composto finito Fix = comutante = polinomios nao e um termo, e onde estao as pecas. Opcional: teorema com k >= 0 que una as duas.

6. **(BAIXO)** K07/CODEX/T1_R3.md l.19 e l.21

   O titulo do bloco 2 diz '[REAL na fonte Lean para a ergodicidade...]' e a frase 'H_erg ja tem testemunha formal' vem antes da ponte 'fluxo do certificado = grupo modular do vacuo' (BW + unicidade KMS, [KNOWN + DERIVED], papel). O texto da proxima secao marca o estatuto certo; a ordem das frases e o titulo podem ser lidos como se M_omega = C1 fosse termo. O termo e C.flow t a = a implica a escalar, e fixos de C.flow = M_omega exige Takesaki (KMS determina o grupo modular), que o kernel nao tem como termo.

   *Conserto pedido:* No titulo: '[REAL: fixos de C.flow sao escalares; DERIVED: C.flow = grupo modular do vacuo]'.

7. **(BAIXO)** K07/CODEX/T1_Lean/T1SemigroupProjection.lean l.21-26

   selfadjoint_semigroup_projection nao exige T 0 = 1 (so a lei aditiva), e portanto vale tambem para semigrupos com T 0 projecao. Verdadeiro e provado; nao e oco (a sonda com T 0 = id, T t = 0 compilou); mas o texto de T1_R3 fala 'semigrupo de contracoes autoadjuntas' sem dizer que a hipotese e mais fraca, o que e so mais geral, nao falha.

   *Conserto pedido:* Nenhum.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- As duas provas em Lean do Codex para a T1 estao certas e nao sao ocas: refiz a compilacao, estraguei treze vezes de proposito e a prova caiu todas as vezes. Mas elas so provam pecas pequenas (a media gaussiana como multiplicador, o semigrupo que converge ao fixo); a ponte grande da T1 (produto cruzado) continua escrita no papel, correta, sem termo Lean.
- Para a cunha da luz livre, a ergodicidade (so os escalares ficam parados) ja e termo do kernel, com certificado habitado e so os tres axiomas de sempre; isso eu conferi no proprio kernel.
- Falta a gerencia lhe perguntar duas coisas em lingua simples: (1) quando o Artigo diz que o nucleo comutativo 'e gerado por K', ele quer dizer so isso, ou que o nucleo e exatamente o que fica parado depois da media (Fix); (2) o operador que faz o papel de K muda de escala quando o nucleo e deslocado (e^h) ou nao (e^h + e^{2h})? A matematica fecha nos dois; a escolha e fisica e e sua.
- O que o Codex nao disse: quais livros leu no original. Convem ele marcar isso antes de a gerencia citar Takesaki e Digernes no Artigo.

## Consultas ao Mapa

- rotas.py consultar T1 -> 35 rotas; nenhuma examina o T1 do produto cruzado alem de cadeia.preparacao_v412 e formal.k05_t1_montagem_gh_tau_campo_v412 (EM_CURSO)
- rotas.py consultar ergodicidade -> 5 rotas, incluindo kernel.ergodicidade_de_mautner_candidata_15nov (EXAMINADA_COM_DEFEITO) e formal.k05_t1_montagem_gh_tau_campo_v412
- rotas.py consultar centralizador -> 2 rotas (formal.k05_t1_montagem_gh_tau_campo_v412; kernel.tipo_iii_como_termo_pergunta_e_resposta_15nov, EM_CURSO)
- rotas.py consultar Terminalidade -> 0 rotas (a leitura C := Fix(Phi_t) da Terminalidade nao foi examinada em rota nenhuma)
- Nada registrado.

## Examinado

- Lidos: kimi/ENTREGA_K07_CODEX.md; ORDEM_K07_CODEX_ASTRA_15nov.md; ADENDO_15nov_B; K07/CODEX/LEIA_PRIMEIRO.md, T1_R3.md, ERRATA_T1_K07_CODEX.md (as duas), T1_Lean/T1GaussianSpectrum.lean e T1SemigroupProjection.lean e seus logs, compilar_candidata.ps1; REVISAO_INDEPENDENTE_R3.md; PERGUNTA_K07_CODEX.md; REGISTRO_MAPA_K07_CODEX.json; DEPOSITO e LEITURA_DO_TUNEL; revisao/REVISAO_K05_T1.md; LEVANTAMENTO_FRENTE_B_15nov/L1; candidatas_c1/ErgodicidadeDeMautner.lean (lista de teoremas e l.455, l.1043).
- Artigo .tex: l.1084-1112 (Axioma E), l.1435-1470 (Terminalidade), l.1860-1920 (T1 no produto cruzado), l.1975-2022 (Fix(sigma)=Fix(Phi)=C).
- Kernel por grep -rn em TGLExt (cd /c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt): centralizer_is_trivial, physicalFockCertificate, physical_net, gaussianWeight_fourier, modularPhase, FockCertificate (campos), Lagrange.interpolate, commutant_generated/aeval_diagonal/selfadjoint_semigroup/midpoint (ausentes), WedgeCyclicR3:70, PonteDaEscalaDual:16, BisognanoWichmann:36; Mathlib no sandbox (MeanErgodic.lean; nenhum semigrupo autoadjunto).
- Scripts meus em scratchpad v412_k07_codex\A: copia das candidatas e do compilar_candidata.ps1 (rodado com cwd na copia; escreve so em build\ da copia); mutate.py (13 mutacoes); V_instance.lean (sonda de vacuidade, RC 0); K_axioms.lean (#print axioms de centralizer_is_trivial e physicalFockCertificate, so o trio); verificacao dos 37 sha256 da ENTREGA (0 divergencias) e dos .olean (bit-identicos).
- Nao feito: WebFetch dos links externos (usaria modelo; regra 4); nao abri TIPO_III1_VINCULO; nao li nada fora do escopo; nada instalado, registrado ou escrito fora da pasta de rascunho.


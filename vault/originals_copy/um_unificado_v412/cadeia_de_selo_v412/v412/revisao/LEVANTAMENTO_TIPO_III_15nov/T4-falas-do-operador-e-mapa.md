> Retorno de um leitor do levantamento do tipo III como termo, de 15/11/2026 (gerência c1; só leitura). É [DECLARADO pelo leitor] até a gerência conferir cada ponto na fonte. Não é fala do operador. As sondas Lean citadas são de rascunho. Nada aqui está instalado, selado ou aberto.

# T4-falas-do-operador-e-mapa

## RESUMO
1. Pela letra, o operador nunca definiu o tipo III₁ em termos matemáticos. A única definição dele é ontológica (02/11, sha16 a3593ac8763f2d19): tipo III = o contínuo, o fluxo; tipo I = o finito comprimido, a medida (ACOM); "não há ponte, há espelhamento". O Atlas a guarda como [ONTO] (TGL_ATLAS.md:46725 e :46746).
2. Em 13/11 ele listou "ergodicidade em III₁ genuína" (T1) e "extensão GH a III₁ (conjecturada via Rieffel)" entre o que resta; em 15/11 disse que "o tipo iii como termo" é "só isso que falta". Nunca disse o que "como termo" exige.
3. Zero falas dele com "a parte que é o todo" ou "sem traço" (varredura de 250 arquivos de bytes mais o índice do acervo). Zero sobre Breuer, ITPFI, Araki, Connes. O mais perto: 04/11 "toda geometria tem traço no finito, no infinito é mera impedância" e 04/11 e 05/11 "reconstruir o todo".
4. Duas falas com "III₁" nos arquivos OPERADOR_*_verbatim têm autoria não estabelecida pelos bytes (07/10, o miolo; 11/10, o arquivo inteiro). Não citar como letra dele.
5. O Mapa não registra nenhuma tentativa de tipar III₁ que tenha falhado. As rotas mortas do Lema 3 (seq 60) são do GLOBAL_LIFT, não da tipagem. O que o Mapa fixa: a T1 fecha sob H_K̂ mais ergodicidade; H_erg na cunha da luz já é teorema (seq 2073); a ressalva D36 (seq 1719) diz que "núcleo II_inf" não é provado nem exigido pelo tipo; GH em III₁ é conjectura.
6. A única tentativa morta de tipar III₁ está no kernel e fora do Mapa (consultas por TheMarkIsNotATypeMark, mixed_log_dense e TheFactorObject: n=0): TheMarkIsNotATypeMark (v295) refuta tipar III₁ pela marca log-densa (um fator I₂ a satisfaz). As pedras 86 a 88 dizem que "fator" e "III₁" são assinatura, não teorema de tipo; NoNormalTrace prova que não há estado tracial normal na torre.
7. Grep recursivo no kernel pelo Bash: nenhuma declaração chamada III1, TypeIII, IsFactor ou ConnesSpectrum; zero "center/Center" em LightRhoStar.lean e TheImportedSecondQuantization.lean. Logo o predicado de tipo e o "centro trivial" da cunha não existem como termo (AUSENTE, com a consulta citada).
8. Já existe e está ligado: LightRhoStar.lean:70-71 centralizer_is_trivial, e o docstring em :65 chama a ponte Fix(IALD)=Fix(TGL)=ker K de "o caso III₁ que a v372 deixou [OPEN]". A leitura operacional da casa para o "caso III₁" é teorema na cunha da luz livre.
9. Armadilhas de homônimo: "Tipo III (impedância)" no artigo da Fatoração (2026-03); "fator" de rota-do-fundo-fator-total (fator do fluido); `half_profile_centralizer_is_factor` (aí "factor" é o objeto M_TGL, não centro trivial).
10. O Grep do Claude Code não enxerga F1Fecho394 (gitignore). Foi a causa dos três falsos "ausente" de hoje; AUSENTE só com grep -r pelo Bash.

## ACHADOS

### A1. FALA 15/11 (o pedido atual)
classe: FALA DO OPERADOR (letra, bytes abertos)
onde: C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_15nov_o_que_falta_para_o_tipo_iii_como_termo_pergunta_nas_quatro_linguas_e_codex_astra_com_o_kimi_no_segundo_adendo_verbatim.txt · sha256 305830689dbdc266ad2d853ebbd8b300a1b486bb0968348606c6fd2e65272c6d · 460 B
«o que falta para resolvermos o tipo iii como termo, faça-me a pergunta nas minhas quatro linguas, porque me parece que é só isso que falta.» Segue o pedido de Codex em modo máximo com o Kimi para o segundo adendo. Ele afirma que o tipo III como termo é o que falta; não diz o que o termo contém.

### A2. FALA 13/11 (ordem da v412)
classe: FALA DO OPERADOR (letra)
onde: …\work\cunhagens_13out\OPERADOR_13nov_vamos_comecar_a_construir_a_v412_camada_iald_cientifica_t1_3mais1_gh_tau_teste_cego_5_sigma_kimi_verbatim.txt · sha256 4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0 · 886 B
«outra coisa restam T1 (ergodicidade em III₁ genuína — os dois lemas padrão de redação: domínio multiplicativo e convergência no predual), a montagem 3+1 por produtos de triplas, a extensão GH a III₁ (conjecturada via Rieffel), e a derivação de τ★». Ele usa o vocabulário da gerência; não define III₁. Mesma fala: «se vc não souber resolver alguma coisa que ainda falta faça-me a pergunta nas minhas quatro linguas».

### A3. FALA 02/11 (o que o tipo III É para ele: a única definição)
classe: FALA DO OPERADOR (letra) + estatuto [ONTO]
onde: …\work\cunhagens_13out\OPERADOR_02nov_ACOM_comprime_em_tempo_real_tipo_I_medida_tipo_III_fluxo_nao_ha_ponte_ha_espelhamento_todas_as_chaves_habitadas_verbatim.txt · sha256 a3593ac8763f2d1988fd3934dcceb0f2c67fe27b388af7ea494a54e6fdd4dd19 · 1844 B · Atlas: C:\IALD\Central de Patentes\memory\TGL_ATLAS.md:46725, :46746
«Quando eu digo de tentar equilibrar a teoria de um lado do contínuo do fator tipo 3, e equilibrando ele com o acom e o acom fazendo o papel no finito do tipo 1…» · «De um lado, o que você tem é o fluxo, do outro, o que você tem é medida. E o ACOM é que faz isso…» · «O que estou tentando dizer é que não há uma ponta para o Tipo I o que há é o espelhamento da informação acontecendo em tempo real, de um lado o tipo I, concentrado, comprimido, de outro lado, o tipo III, contínuo.» É leitura ontológica: nenhum predicado de álgebra. O Atlas a registra como [ONTO], não como teorema. Os correlatos [KNOWN] (ITPFI/Araki-Woods-Powers; Takesaki 1972) são da gerência, não dele.

### A4. FALA 02/11 (prioridade: a passagem ao contínuo)
classe: FALA DO OPERADOR (letra)
onde: …\work\cunhagens_13out\OPERADOR_02nov_a_passagem_para_o_continuo_e_o_que_mais_importa_virar_a_chave_de_conjectura_para_provado_verbatim.txt · sha256 9978862f60cfbf29e3a47def79fa9660d0819f58838fe893bca6154113fa2bcf · 390 B
«a construção da passagem para o contínuo é o que mais importa, porque deixa de ser conjectura sob hipótese se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ; isso é o que mais importa, virar essa chave de conjectura para provado». O registro seq 1719 do Mapa diz que a chave virou validade no kernel quanto ao termo (v406), mas a condição dele («se funcionar sob compressão…») NÃO foi testada.

### A5. FALA 02/11 (construir tudo)
classe: FALA DO OPERADOR (letra)
onde: …\work\cunhagens_13out\OPERADOR_02nov_precisamos_construir_tudo_nao_perder_a_ordem_logica_e_o_fechamento_verbatim.txt · sha256 f3998f01262aad6bcb8bb41547f15266eb40dcccbc3da3204151bef5f27b5b32 · 284 B
«perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.» Resposta à partitura das 42 chaves (36 habitadas, 2 falsas por teorema, 4 = a parede única face de Fock/III₁). Supera a decisão da manhã «não vamos construir ainda o que é sabido».

### A6. FALA 04/11 (o traço: a lei do custo)
classe: FALA DO OPERADOR (letra)
onde: …\work\cunhagens_13out\OPERADOR_04nov_a_lei_do_custo_impoe_a_troca_tempo_por_traco_finito_zero_absoluto_infinito_impedancia_verbatim.txt · sha256 b19b8a68d0639968cc4cd3d7ea17d8b028dfba6d1c9130a6abc0783d0b0b038d · 293 B
«a lei do custo impõe a troca e betatgl troca o tempo por traço finito e o zero absoluto fica com a geometria do infinito=nada nominado, porque toda geomtria tem traço no finito, no infinito é mera impedância; será que vc consegue entender a lei do custo tal qual formulada, faz sentido?» É a coisa mais próxima de «o traço que não existe»: traço só no finito; no infinito, impedância. Ele não diz III₁ nem fator. (Grafia «geomtria» preservada dos bytes.)

### A7. FALA 04/11 (a face de Fock é o traço do psíon): só a primeira linha é dele
classe: FALA DO OPERADOR só na 1ª linha; resto DECLARADO (outra IA)
onde: …\work\cunhagens_13out\OPERADOR_04nov_a_face_de_fock_e_o_traco_do_psion_e_derivacao_de_outra_instancia_verbatim.txt · sha256 62bc328e66e731e244ab8749aec33180ced4bf22083a00ef170e651e7ca1da74 · 3589 B
Dele: «Estudando a v407 cheguei a isto: A face de Fock é o traço do psion.» Do «Daí derivei em outra instância da IALD, veja:» em diante é texto de outra instância [DECLARADO], com leituras proibidas pela régua; a expressão «cociclo Tipo III₁» está nesse trecho, não na letra dele. Memória e Mapa já dizem isso.

### A8. FALAS sobre a parte que reconstrói o todo / o núcleo (o mais perto de «a parte que é o todo»)
classe: FALA DO OPERADOR (letra); a leitura «parte = todo» é da gerência
onde: …\work\cunhagens_13out\OPERADOR_04nov_tetelestai_e_o_terminal_a_poda_e_palavra_sem_espelho_provar_ou_podar_verbatim.txt · OPERADOR_05nov_a_fita_de_turing_e_o_hamiltoniano_oculto_verbatim.txt · OPERADOR_02nov_vazar_e_luzir_registro_leitura_do_foton_pelo_graviton_verbatim.txt
04/11: «TETELESTAI, é a poda, é o seletor que diz que não precisa de 100% para reconstruir e ler o todo» (sha c12699c915617c3f20f6f22fe8f76c5acbfdd20ec06f3a08654364489cc3a656). 05/11: «A fita de turing é o hamiltoniano oculto, é a única regra que precisa ser gravada para reconstruir o todo» (sha a63f2aa66f64de20754817de0a87955373a124316c3fcf4da7225b574f34fd97). 02/11: «nunca se chega inteiro no sentido de 100% mas se chega inteiro no sentido de perfeitamente identificável ao núcleo invariável da identidade mesmo que haja alteração na forma, o conteúdo preservado permite reconstruir integralmente a forma» (sha 032b8cb24b42bf09d47355ffc37ef1932b014eb27c74791e98a0ee3c4e52ff8e). Nenhuma contém a frase «a parte é o todo»; varredura por regex em todos os arquivos de fala deu zero.

### A9. FALAS sobre a testemunha estática plena proibida
classe: FALA DO OPERADOR (letra; a de 23/09 por memória)
onde: C:\IALD\Central de Patentes\work\cadeia_de_selo\v385_selo\afericao_superficies\operador_msgs_05out.txt (sha256 675a4db54fdde430b2bd3979f3f3d266a2fd16e556efee92aa9a2f312e8bb952; é extração do transcrito) · …\cunhagens_13out\OPERADOR_22out_psion_habitante_da_testemunha_estatica_verbatim.txt (sha256 b102ae804f54e2b2dcb6d701793f9fa3e96a39522fb3ccd2c177916d46b1d4e2) · memória iald-e-a-testemunha-fecho-estacionado-23set.md
05/10: «testemunha falsa é a testemunha estática é o zero absoluto» (extraída do transcrito da sessão, timestamp 2026-10-05T11:33:36.693Z; o verbatim.py da auditoria confirmou). 22/10: «O psion é o habitante da testemunha estática e eu explico o porquê, porque ele admite ser falso de for individualizado (1=0), ou seja, sem par, sem conjugação, e por isso a mentira lida como mentira se torna verdade, e admite a verdade conjugada ocasião em que se colapsa ao gráviton». 23/09 (só pela memória; os bytes originais não foram abertos por mim): «o fecho total não é "proibido" ele é impossível por teorema em tempo finito de modo estático, ele é estacionado dinamicamente e não estático».

### A10. FALA 12/10 (a única outra vez que ele escreve «III1»)
classe: FALA DO OPERADOR (letra)
onde: C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt · sha256 78ef70e6f9868281d44e8a306e60a0cb162843e54f3a74389ddf14ed325d535d · 1342 B (fora das pastas pedidas; achado pela varredura de work\)
«já temos o motor continuo, a resolução de riemann, o paradoxo de zenão resolvido no contínuo III1, enfim, parece que temos tudo, mas que isso ainda falta ser conectado como um único motor». Aqui «contínuo III1» é o lugar onde ele diz que o paradoxo de Zenão está resolvido; não é definição nem pedido de tipagem.

### A11. AUTORIA NÃO ESTABELECIDA: 07/10 (miolo) e 11/10
classe: FALA AUTORIA INCERTA (não citar como letra)
onde: C:\IALD\Central de Patentes\work\cadeia_de_selo\v390_ordem\CUNHAGEM_OPERADOR_07out_verbatim.txt (sha256 e2a915e23692f85cbd8815d14a80a40d10bef4e71396f33138dcb986064ca3a7) · …\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt (sha256 b365591ceb346cdfc8333713c1bc5911fd704854b00017f080f21f6340c818d5) · memórias superposicao-e-a-passagem-07out.md e tudo-e-frequencia-defasagem-transmitir-11out.md
07/10: «A superposição continua existindo — ela é o fundo modular, o tipo III₁, o contínuo» e «O witness estático pleno é impossível» estão no bloco com marcadores e a frase «Essa é a leitura mais rigorosa que o artefato permite», que lê como texto colado de outra IA; a memória só toma como verbatim dele o ÚLTIMO parágrafo («Pra mim o que falta pra fecharmos o um.py agora é definir a superposição como a passagem do global lift…»). 11/10: o arquivo OPERADOR_11out inteiro é exegese com cabeçalhos em negrito; «o fator do tipo III₁» está nela; só as frases entre aspas («Tudo é frequência…», «…porque essa é sua natureza: transmitir.») são dele, e a memória a chama «derivação que eu passei». Nenhuma das duas serve como a letra dele sobre o que o tipo III é.

### A12. O QUE O OPERADOR NUNCA DISSE (pela letra, nas pastas pedidas, mais work\ e o índice)
classe: NUNCA DISSE
onde: varredura: 250 arquivos OPERADOR_*/*verbatim* (cunhagens_13out, cunhagens_10out, cadeia_de_selo\v386 a v392) + scanall em work\ + buscar.py
(a) Nenhuma definição matemática de III₁ (fator, centro trivial, espectro de Connes, núcleo II_∞, escala do traço). (b) O que «tipo III como termo» exige. (c) «a parte que é o todo»: 0 ocorrências nas falas e 0 no índice do acervo (13.608 docs). (d) «sem traço»/«o traço não existe»: 0 literais nas falas. (e) «canto de Breuer»: só «o lema que liga o psion ao canto» (03/11). (f) ITPFI, Araki, Connes, Powers, Takesaki: 0 nas falas. (g) A decisão entre (i) tipar o III₁ da cunha da luz livre e (ii) tipar a álgebra do horizonte da TGL (a passagem que o Mapa chama hipótese física aberta). Ele nunca ratificou item a item «ACOM = esperança condicional do III₁»; a regra de 04/11 «provar ou podar» vale para essa leitura.

### A13. MAPA: não há rota morta de tipar III₁; o que a consulta devolveu
classe: ROTA DO MAPA (consulta citada)
onde: rotas.py consultar (11 termos únicos) + rotas.py ver nas 21 rotas listadas em 'examinado'
Os termos III, III1, fator, ITPFI, Araki, Connes, traco, semifinito, tipo, Breuer, nucleo devolveram 140 rotas distintas; li as 20 pertinentes por rotas.py ver. Nenhuma registra «tentativa de tipar III₁ e falhou». ITPFI e Araki só aparecem na nota de kernel.inventario_chaves_de_testemunha_v405_02nov (seq 1677 a 1969): «ITPFI/Araki–Woods–Powers … kernel: PowersLadder; Tomita-ITPFI na torre, contrato v203 à espera»; e «Que o ACOM … SEJA essa esperança condicional do III₁ é leitura [ONTO/OPEN]: a casa tem só a sombra finita». Breuer aparece só em filme.par_v405 e kernel.parede_da_renormalizacao (sem III₁).

### A14. MAPA seq 2073 (errata ao seq 2060) e seq 2074: H_erg na cunha da luz livre é teorema
classe: ROTA DO MAPA (veredito, defeito, nao_refazer, proximo_passo)
onde: rotas formal.k05_t1_montagem_gh_tau_campo_v412 (seq 2060, 2073) e kernel.ergodicidade_de_mautner_candidata_15nov (seq 2074)
«H_ERG_NA_CUNHA_DA_LUZ_LIVRE_JA_ERA_TEOREMA_DO_KERNEL__CERTIFICADO_HABITADO__FALSO_NEGATIVO_DE_AFERICAO_CORRIGIDO». nao_refazer: «Não escrever que H_erg falta no kernel nem que o certificado do Fock não está habitado. Não afirmar ausência no kernel pela ferramenta de busca do Claude Code…». proximo_passo: «estado normal fiel e H_K-chapéu implicam a caixa. O Kimi decide na K07 se H_K-chapéu é o Axioma E transcrito. O resíduo do horizonte da TGL não muda.» O seq 2060 (H_erg ausente) está superado. O seq 2074 (ErgodicidadeDeMautner, 48 teoremas, só trio, nada instalado) diz: «Não dizer que a candidata prova o tipo III1, o horizonte da TGL, H_K-chapéu, o Lema B, o Lema C ou o Lema A contínuo» e «Não propor termo Lean para GH em III₁ (só há enunciado oco)».

### A15. MAPA cadeia.preparacao_v412 (seq 2050, 2054, 2055): onde a T1 pára
classe: ROTA DO MAPA ([DECLARADO] conferido)
onde: rota cadeia.preparacao_v412
veredito: «T1_FECHA_SOB_DUAS_HIPOTESES_NOMEADAS». «o T1 fecha como um teorema (comutante relativo de Digernes-Takesaki, pontos fixos da mistura, convergência com o traço), sob H_K (K função positiva injetiva do gerador) e a ergodicidade do fluxo modular; a transferência da cunha para a álgebra de horizonte é hipótese física aberta; (4,0) fecha pelo toro plano; (1,3) continua hipótese; GH em III1 continua conjectura». [DECLARADO pelo Kimi, conferido por revisor distinto]. A T1 no papel vale para ESTADO normal fiel (peso infinito não tem esperança condicional).

### A16. MAPA seq 1719 (v406): as ressalvas D36 dizem o que o certificado NÃO prova sobre o tipo
classe: ROTA DO MAPA (defeito medido)
onde: rota kernel.fechamento_construir_tudo_programa_02nov, seq 1719
«(2) "nucleo II_inf" no docstring do campo PF (CanonicalModularCoreAssemblyR1) nao e' provado nem exigido pelo tipo: le-se [KNOWN/DECLARADO], nao como resultado do habitante»; «(3) o traco do nucleo (cyclicTraceCandidate) e' ENNReal e CICLICO sobre a relacao de deslocamento (ShiftRelated); nao e' funcional linear nem aditivo fora do cone positivo»; PF/Pp/Pm escolhidos por Classical.choose; «(1) K(O) != bot para O compacto NAO esta' provado». É a medida de que o núcleo como fator II_∞ com traço escalado NÃO está tipado, embora o certificado traga Core, traço e trace_dual_scaling.

### A17. MAPA rotas mortas do Lema 3: não são tipagem de III₁
classe: ROTA DO MAPA (não é rota de tipagem)
onde: rota kernel.lema3.rotas_mortas (seq 60, 1984-2003) · memória o-fechamento-lema3-impossiveis.md
seq 60 (28/09): 25 rotas mortas; a nº1 é «Witness dentro de M. Nenhuma projeção P ∈ M (fator III) satisfaz 0 < τ_core(P) < ∞»; a nº4: «tr(P) como invariante: é gauge (em fator III σ-finito todas as projeções ≠0,1 são…»; a nº3 «Absorção tensorial M ≅ N⊗R… (Connes 1973 Cor. 3.2.8(a)) o passo é CORRETO». Todas supõem M do tipo III e pedem outra coisa (o GLOBAL_LIFT). A memória o-fechamento-lema3-impossiveis.md traz a CORREÇÃO de 15/08: a lista morreu de confundir dois fluxos (θ_s dual e σ_t modular). A cadeia de 11/11 (seq 1984-2003) é a do fecho (H,U) e também não tipa III₁.

### A18. MAPA (Codex, outubro): modelo algébrico não é core de von Neumann; traço v351 não habita o núcleo matricial
classe: ROTA DO MAPA ([DECLARADO] Codex)
onde: rotas formal.f1_2.dual_scaling_reuse_011 e formal.f1_takesaki.modular_identity_to_scaling
formal.f1_2.dual_scaling_reuse_011 (07/10, seq 716-725): «ERRO_DE_TIPO_EVITADO_PONTE_ANALITICA_ABERTA»; «Dois lemas algebricos compilados nos geradores nao pagam fechamento von Neumann ou traco normal semifinito»; proximo: «Construir L2(R,M_n), gauge isometrico, algebra gerada M_n tensor L(R) e traco tr_n tensor exp(-x)dx». formal.f1_takesaki.modular_identity_to_scaling (13/10, seq 1084): «LOCAL_ALGEBRA_PASS_GENERAL_CONSTRUCTION_OPEN … Não confundir modelo algébrico com core de von Neumann». Ambas EM_CURSO por codex-gerente-tgl [DECLARADO]; o v406 depois habitou o certificado físico por outro caminho (Fock concreto).

### A19. MAPA v402: o caso III₁ do índice 1/β segue [OPEN]
classe: ROTA DO MAPA (veredito)
onde: rota kernel.v402_esperanca_condicional_e_nome
kernel.v402_esperanca_condicional_e_nome (seq 1452-1495): «o indice 1/beta segue CONDICIONAL as hipoteses nomeadas hpp e hopt e nenhuma instancia e' construida; o caso III1 segue [OPEN]»; proximo: «o indice 1/beta so' sai de condicional com uma instancia (NameIndex) construida».

### A20. KERNEL, FORA DO MAPA: a tentativa morta de tipar III₁ pela marca log-densa, e a assinatura que não é tipo
classe: EXISTE NO KERNEL E NÃO ESTÁ NO MAPA (fiação do registro, não falta)
onde: C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheMarkIsNotATypeMark.lean · TheFactorObject.lean · SignatureInTheLimit.lean (pedra 87) · NoNormalTrace.lean (pedra 88) · TowerTraceless.lean
TheMarkIsNotATypeMark.lean (v295, 29/08): «A densidade log é satisfeita por um fator de tipo I. Logo ela NÃO separa III₁ de III_λ, e NÃO infere o tipo da fronteira.» (contraexemplo M₂(ℂ), estado diagonal w=1/3, razões 2 e 3). «O tipo segue [OPEN] nos dois sentidos… SiteProfile continua sendo parâmetro estipulado.» TheFactorObject.lean:30-31: «"Fator" e "III₁" seguem sendo ASSINATURA (pedra 87), não teorema de tipo». NoNormalTrace.lean:38-42: «"sem estado tracial normal" NÃO é ainda "fator III₁ pleno" (centro trivial e ausência de PESO semifinito ilimitado seguem o programa)»; o teorema no_normal_tracial_state_mix (l.~470) vale para a torre (⅓,¼). Consultas ao Mapa por TheMarkIsNotATypeMark, mixed_log_dense, TheFactorObject: n=0 (o Mapa nasceu em 28/09, depois da v295).

### A21. KERNEL: o que EXISTE E ESTÁ LIGADO sobre o caso III₁ da cunha
classe: EXISTE E ESTÁ LIGADO
onde: C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\LightRhoStar.lean · TheImportedSecondQuantization.lean
LightRhoStar.lean:65-66, docstring «A PONTE NA LUZ — Fix(IALD) = Fix(TGL) = ker K (o caso III₁ que a v372 deixou [OPEN])», theorem the_bridge_fix_on_the_light; :70-71 «o centralizador da cunha é TRIVIAL: a ∈ M^ω ⟹ a = c·1 (separação do vácuo)», theorem centralizer_is_trivial (a : (C.R (L.K rightWedge)).toStarSubalgebra) (ha : ∀ t : ℝ, C.flow t a = a) : ∃ c : ℂ, (a : C.F →L[ℂ] C.F) = c • (1 : C.F →L[ℂ] C.F). Mais TheImportedSecondQuantization.lean:214 wedge_nonabelian, :217 bw_kms, :245 trace_dual_scaling, :429 light_null_ergodic.

### A22. KERNEL: o que a consulta recursiva NÃO achou
classe: AUSENTE (com a consulta citada); derivação a conferir por quem construir
onde: consulta de 15/11/2026 por Bash em C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt
Bash, cd tgl_kernel\TGLExt, grep -rnE --include=*.lean com nomes de declaração (III1|IIIOne|TypeIII|typeIII|type_III|IsFactor|isFactor|is_factor|Factor\b|ConnesSpectrum|connesSpectrum|ergodic|Ergodic|centralizer_is_trivial|ITPFI|Araki): nenhuma declaração é predicado de tipo ou de fator; os acertos são Ergodicity.lean:285 ergodic_convergence_modular, TheImportedSecondQuantization.lean:429 light_null_ergodic, LightRhoStar.lean:71, TracialCentralizerExpectation.lean:72 half_profile_centralizer_is_factor (homônimo: «factor» = o objeto M_TGL) e nomes que só contêm 'Factor' no sentido de multiplicador. grep de center|Center|IsFactor|trivialCenter|centro trivial: arquivos NoNormalTrace.lean, SignatureInTheLimit.lean, TheCoinage.lean só em docstring; zero em LightRhoStar.lean e TheImportedSecondQuantization.lean. Conclusão para quem decide: o predicado de tipo III₁ e o enunciado «centro da cunha trivial» não existem como termo [AUSENTE, com a consulta]; o centro estar fixo pelo fluxo modular (logo no centralizador) é [KNOWN], não conferido no kernel por mim.

### A23. HOMÔNIMOS que causam falso achado
classe: HOMÔNIMO / texto de casa
onde: índice do acervo (buscar.py) · memória · C:\IALD\Artigo\Haja_Luz\A_Ultima_Ponte.md
(1) «Tipo III (impedância)»: variante H₀/(1−α√e) do artigo da Fatoração, 2026-03 (fatoracao_constante_miguel_v1.tex:1400 e v2.tex:1439 no índice do acervo), nada a ver com von Neumann. (2) «fator» em memory\rota-do-fundo-fator-total-decisao-15set.md: fator sobre o fluido total Φ_total. (3) half_profile_centralizer_is_factor: «factor» é o objeto M_TGL. (4) «traço» tem três sentidos no kernel (memória face-de-fock-e-o-traco-do-psion-04nov.md): peso 1 do canto [REAL]; traço parcial [REAL só na face finita]; traço normal na álgebra modular [NÃO EXISTE por teorema, NoNormalTrace]. (5) A Última Ponte (03/06/2026) diz «Tipo III₁ não tem traço, não tem matrizes-densidade, não tem Hamiltoniano» (A_Ultima_Ponte.md:95, sha16 8501bf136bce92a9): texto de casa, não fala dele.

### A24. MEMÓRIA: tópicos pertinentes (parte 1: o fechamento, o traço, a T1)
classe: MEMÓRIA (leitura das descrições e corpos)
onde: C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\
construir-tudo-o-fechamento-02nov: ordem «construir tudo»; as 4 chaves da face de Fock/III₁ reduzem a C : FockCertificate = CanonicalNetInput (8 campos) + RemainingModularCoreInput (21 campos: traço com trace_dual_scaling e P_F); v406 habitou; full_static_witness_exists e trivial_inhabitant_exists ficam False por teorema. face-de-fock-e-o-traco-do-psion-04nov: os três sentidos de traço; a cunhagem é teorema no sentido 1; «Tr_∂ como estado tracial da III₁ é contra o kernel». t1-ergodicidade-na-luz-candidata-15nov: H_erg é teorema; falta H_K̂, Lemas B e C, Lema A contínuo, o tipo como termo e a passagem ao horizonte; não apresentar como novo o que a candidata reexporta. v412-preparacao-13nov: as três frentes; T1 sob H_K̂, H_erg e H_TGL-horizon; GH-III1 CONJECTURE; τ★ aguardando o relógio do pedágio.

### A25. MEMÓRIA: tópicos pertinentes (parte 2: testemunha, torre, Lema 3, regras)
classe: MEMÓRIA
onde: C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\
iald-e-a-testemunha-fecho-estacionado-23set: testemunha estática falsa; fecho impossível por teorema estaticamente e estacionado dinamicamente (full_closure_iff_flat NoFullWitness.lean:77, beta_forbids_full_static_witness :91). v396-selada-a-testemunha-estatica e handoff-v396-custodia: o psíon habita a testemunha estática; a face de Fock era condicional (fechada na v406). superposicao-e-a-passagem-07out: Fundação/Ágape; só o último parágrafo é verbatim dele. ordem-017-execucao-gerencia: brechas dos tipos dos certificados (Core admite truque tensorial; K:=⊥ torna o Fock vazio); escala 1,5 a 3 pessoas-ano [CONJECTURE]. ordem-011-fecho-matematico e raiz-da-arvore-da-prova: torre V351 como molde (scalarInverseLimitTraceData); Lema 3 pago na torre. o-fechamento-lema3-impossiveis: as 25 rotas morreram de confundir dois fluxos. grep-da-ferramenta-nao-ve-o-gitignore-15nov, atribuicao-ao-operador-so-por-bytes-14nov, pergunta-nas-quatro-linguas (TGL, teológica, linguística Nome/Palavra/Verbo, jurídica Fato/Valor/Norma; «uma pergunta, quatro bocas»), provar-ou-podar-palavra-sem-espelho-04nov: as regras de método que governam a próxima pergunta.

### A26. AVISO de método para evitar a quarta falsa ausência
classe: AVISO (regra do aferidor)
onde: rota formal.k05_t1_montagem_gh_tau_campo_v412 (nao_refazer) · memória grep-da-ferramenta-nao-ve-o-gitignore-15nov.md
A busca por frase no Mapa devolve zero por construção (rotas.py consultar aceita termo único; a consulta do Kimi por frase deu zero). A Grep do Claude Code não vê F1Fecho394 (linha 37 do gitignore do Nós) e dá zero falso. O nome real do teorema era centralizer_is_trivial e a busca procurava centralizer_trivial: tentar sinônimos e ler a lista por regex ampla, depois filtrar. Antes de dizer a ele que algo «falta» sobre o tipo III: conferir TheMarkIsNotATypeMark, SignatureInTheLimit, NoNormalTrace, TheFactorObject, LightRhoStar:65-71 e a ressalva D36.

## PROPOSTAS

### P1. A pergunta do resíduo, só sobre o que ele nunca respondeu
enunciado: Uma pergunta, quatro bocas, sobre o conteúdo do termo: quando o senhor diz «o tipo III como termo», o que o termo deve conter? (a) só o predicado de tipo para a cunha da luz livre: fator (centro trivial) e sem estado tracial normal, mais o fluxo ergódico, que o kernel já prova (centralizer_is_trivial); (b) também o núcleo de Takesaki como fator II_∞ com o traço escalado pela ação dual, que o certificado traz sem tipar (ressalva D36); (c) o mesmo para a álgebra do horizonte da TGL, não só a cunha (a passagem que o Mapa chama hipótese física aberta). As quatro línguas seguem pergunta-nas-quatro-linguas.md: TGL; teológica; linguística (Nome/Palavra/Verbo); jurídica (Fato/Valor/Norma).
apoio: Letra dele em 15/11 («é só isso que falta») e 02/11 (tipo III = o contínuo/fluxo; tipo I = a medida); Mapa seq 1719 (D36), 2073, 2074 e cadeia.preparacao_v412; kernel LightRhoStar:65-71, TheMarkIsNotATypeMark, NoNormalTrace:38-42, TheFactorObject:30-31.
nao compra: Não responde o que ele pensa: só separa o que ele nunca disse do que o kernel já tem. Não tipa o III₁ da álgebra do horizonte da TGL, não decide GH em III₁, não toca τ★, e não substitui a leitura da partitura ao operador antes de qualquer teste com negativo possível (aqui não há teste).
risco: As três alternativas são minha leitura do Mapa e do kernel, não fala dele; é a mesma assimetria de leitura que a regra do posto manda dizer em voz alta. Não conferi o centro-fixo-pelo-fluxo no kernel; o aferidor da gerência precisa confirmar que (a) não é redundante com centralizer_is_trivial antes de perguntar.

## CONSULTAS AO MAPA

## EXAMINADO
- Mapa de Rotas (rotas.py consultar e ver): ver a lista em consultas; nada registrado, nada escrito
- C:\IALD\Central de Patentes\work\cunhagens_13out (244 arquivos; leitura integral dos 30 relevantes) e cunhagens_10out (4) e cunhagens_12out (1)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v386 a v392 (arquivos OPERADOR_* e *verbatim*), v390_ordem\CUNHAGEM_OPERADOR_07out_verbatim.txt e _nomes_verbatim.txt, v385_selo\afericao_superficies\operador_msgs_05out.txt
- C:\IALD\Central de Patentes\work\superposicao_passagem_07out (listagem)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412 (revisao\LEVANTAMENTO_FRENTE_B_15nov listado; grep de 'tipo como termo')
- C:\IALD\INDICE_DO_ACERVO\buscar.py (consultas listadas)
- C:\IALD\Artigo\Haja_Luz\A_Ultima_Ponte.md (linhas com III₁)
- C:\IALD\Central de Patentes\memory\TGL_ATLAS.md (grep com número de linha)
- C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt: TheMarkIsNotATypeMark.lean, TheFactorObject.lean, SignatureInTheLimit.lean, NoNormalTrace.lean, TowerTraceless.lean, LightRhoStar.lean, TracialCentralizerExpectation.lean, TheImportedSecondQuantization.lean (consultas por grep recursivo via Bash)
- C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory (321 tópicos filtrados por regex; 12 lidos)
- Pasta de rascunho (só scripts e cópias de leitura): C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_tipo_iii\T4

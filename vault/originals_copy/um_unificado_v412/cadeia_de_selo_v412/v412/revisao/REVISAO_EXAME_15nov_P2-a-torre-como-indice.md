# CONFERÊNCIA DISTINTA — as entregas do Codex (unidade do tipo III) e do Kimi (K10), examinadas por ordem do operador — P2-a-torre-como-indice

> Montado pela gerência c1 em 15/11/2026 19:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 5 MEDIO, 5 BAIXO

## Resumo

1. Recompilei do zero, em cópia minha, os 9 módulos até Classificacao.lean: todos compilam, sem sorry, axiomas só no trio (propext, Classical.choice, Quot.sound), um único aviso inofensivo (TowerWedgeIndex.lean:131, tática que não faz nada). A matemática da Torre está sólida.
2. Seis mutações minhas (rapidez dobrada, fator invertido, só um gerador, sem injetividade, projeção trocada, perfil geral) derrubaram a compilação: os enunciados não estão soltos do código.
3. Como a Torre "indexa" a luz: cada unidade E_ij da Torre carrega um número, log(w_i/w_j), que é a frequência dela no relógio da própria Torre. A cunha lê o seu boost nesse número. A Torre entra nos teoremas só como uma função (N,i,j) para números reais, com duas leis (soma e refino). É uma tabela de referências, não um mapa entre objetos.
4. Prova de que é só rótulo: os três enunciados do "diagrama" valem para qualquer número real (controle compilado sem Torre: C3_sem_torre.lean). A Torre só escolhe quais números entram. Isso confirma a leitura "índice que aponta" (a resposta D do operador: indexação, índice, torre) e não decide nada por ele.
5. O contrário, "parte que contém", é refutado no sentido de caber dentro: o Lean prova que nenhuma cópia fiel (injeção de álgebras com unidade) da Torre na cunha leva o relógio da Torre ao relógio da cunha, nem com troca arbitrária de escala de tempo. O motivo é simples: a Torre tem uma projeção imóvel que não é múltiplo da identidade, e na cunha só o múltiplo da identidade é imóvel. Vale só nessa direção (Torre para cunha) e as hipóteses são satisfazíveis (controle), logo não é vácuo.
6. Vacuidade: indexed_*, rapidity_*, site_*, o não-mergulho e o esticamento da translação valem para todo perfil de sítios; só mixed_*, two_tower_* e o diagrama (ReadsTowerOnWedge) são do perfil misto (pesos de sítio 1/3 e 1/4, razões 1/2 e 1/3, não pesos 1/2 e 1/3). Num perfil todo 1/2 as hipóteses de two_tower valem para todo vetor (C1_perfil_meio.lean), então o resultado depende mesmo da incomensurabilidade log 2 / log 3.
7. "Os dois primeiros fatores já selecionam o vácuo" é exatamente o que two_tower_boosts_read_vacuum prova, mas é consequência trivial de "um só boost não nulo já fixa só o vácuo" (candidata ErgodicidadeDeMautner da gerência): compilei isso em C2_via_mautner.lean. O boost isolado ainda não está no kernel; então a Torre dá uma rota sem Mautner, não um resultado a mais.
8. A marca log-densa da Torre reaparece, mas como argumento de fecho de grupo para vetores fixos, não como critério de tipo; o tipo III1 vem do centro da cunha e do núcleo contínuo. Não reintroduz a leitura refutada na v295 (e os rótulos aqui são autovalores modulares verdadeiros, não os A e B arbitrários do objRatio), mas a entrega não diz isso em lugar nenhum.
9. O kernel já ligava Torre e cunha, por estipulação, no modelo-testemunha (WedgeNet.lean v135 e towerWedgeData v350: a álgebra da cunha direita É o fator da Torre, com translações triviais). A entrega não cita isso, e o não-mergulho mostra que essa identificação não vale para a cunha física de Maxwell.
10. Cerca de metade dos 16 teoremas pedidos são envoltórios de uma linha de resultados do kernel (tower_unit_flow, site_fixed, site_nonscalar, indexed_boost_translation, exp_rapidity, rapidity_unique); o conteúdo próprio é two_tower_*, o esticamento indexado e o não-mergulho.
11. A cópia da fala do operador usada pelo Codex (455 bytes) não é a do acervo (665 bytes) e não tem a frase "A Torre a indexa"; a PROVA chama a cópia de "fala integral".
12. Veredito: o Lean está certo; as ressalvas são de nomes, de texto e de proveniência, e se consertam sem mudar nenhuma prova.

## Achados

1. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K07\CODEX\TIPO_III1_VINCULO\Torre\TowerWedgeIndex.lean:54-70; VinculoCriterion.lean:34-61; Classificacao.lean:33-43

   A relação Torre-cunha provada é de rótulo, e isso não está dito em palavras simples. A Torre entra só pela função (N,i,j) para log(w_i/w_j). Os três enunciados de ReadsTowerOnWedge valem para todo real s: C3_sem_torre.lean (em P2\ctl) compila any_real_translation, tower_case_is_instance (indexed_boost_translation é o caso s = rapidity) e any_real_modular_translation, só no trio. Em light_tower_horizon_observer (Classificacao.lean:33-43) o conjunto (forall N i j, ReadsTowerOnWedge N i j) não menciona L nem a e é independente de IsTypeIII1: são cinco conjuntos independentes sobre a mesma rede. O mapa da Torre para as rapidezes não é injetivo (E_01 em N=0 e E_(0,a)(1,a) em N=1 têm a mesma razão, por rapidity_refine) e perde a não comutatividade. A PROVA dá o dado técnico (Atribuir-lhe s = log lambda) mas não diz ao operador, na língua dele, que 'indexar' provado = apontar números e que o resto é um negativo.

   *Conserto pedido:* Acrescentar à PROVA uma linha para o operador: 'a Torre fornece os números pelos quais a cunha é lida; as três leituras valem para qualquer número real; a Torre não está contida na cunha (negativo provado)'. Enunciar any_real_translation como teorema principal e indexed_boost_translation como corolário. Dizer que o último conjunto de light_tower_horizon_observer é uma conjunção, sem acoplamento entre a Torre e o observador (L,a).

2. **(MEDIO)** VinculoCriterion.lean:34-49 (ReadsTowerOnWedge, tower_observer_diagram); Classificacao.lean:33 (light_tower_horizon_observer); Torre\RESULTADO.json (alcance[1]: 'Seus boosts distinguem...')

   Nomes que prometem mais que o termo. 'Diagram' e 'ReadsTowerOnWedge' sugerem um diagrama entre objetos da Torre e da cunha; o termo é uma conjunção de três igualdades sobre um real s. A perna da Torre (tower_unit_character, Torre\TowerWedgeIndex.lean:109) não está no predicado, e o instante modular da cunha (t = -s/2pi) depende da unidade, logo não é o tempo da Torre. A Torre não tem boosts: os boosts são da cunha (RESULTADO.json alcance[1] diz 'Seus boosts'). A regra da casa (a de agosto, v295 e v298) pede que o nome não diga mais que o termo.

   *Conserto pedido:* Renomear (por exemplo ReadsRapidityOfTowerUnit; 'Seus boosts' vira 'os boosts da cunha lidos nos números da Torre'), ou incluir no predicado a perna tower_unit_character e dizer que os dois tempos são diferentes e que a ponte é só o número s. Os nomes finais são do operador.

3. **(MEDIO)** Torre\TowerWedgeIndex.lean:188-253 (two_tower_boosts_read_vacuum, two_tower_times_read_scalars); PROVA_E_ALCANCE.md:9

   Os dois teoremas valem, mas são consequência trivial de 'um só boost não nulo fixa só o vácuo' (ErgodicidadeDeMautner.os_fixos_de_um_so_boost_da_luz_sao_a_reta_do_vacuo, candidata da gerência, em candidatas_c1). Compilei o fato em C2_via_mautner.lean: one_tower_boost_reads_vacuum e two_tower_from_one_boost, rc=0, só trio; o segundo gerador (1/3) é dispensável e a Torre não acrescenta nada a esse resultado. Consulta no kernel: grep -rn 'um_so_boost|single_boost|one_boost' em TGLExt devolve só ModularSignatureObstruction.single_boost_has_two_signatures (outra coisa), logo o boost isolado ainda NÃO está no kernel instalado (confere com a rota do Mapa kernel.ergodicidade_de_mautner_candidata_15nov: 'um só boost é novo'). Hoje a rota da Torre tem mérito próprio (usa só light_modular_fixed_iff_vacuum + densidade + fecho), mas 'já selecionam' passa a ideia de que os dois primeiros fatores têm papel especial.

   *Conserto pedido:* Dizer na PROVA que a rota é por densidade e que um só boost não nulo basta quando a candidata de Mautner entrar; se ela entrar, two_tower_* viram corolários e a Torre perde o papel nesse ponto.

4. **(MEDIO)** Omissão em PROVA_E_ALCANCE.md e Horizonte\LEITURA_DA_CUNHA.md; kernel: TGLExt\WedgeNet.lean:323 (wedgeNet_M), cabeçalho 28-31; TGLExt\V350WedgeModularData.lean:70 (towerWedgeData); TGLExt\Santo.lean:430-442

   O kernel já ligava Torre e cunha, por estipulação: no modelo-testemunha theSpecificAQFTWitness (v135) a rede da cunha direita É theFactorObject mixProfile, com translações que agem trivialmente (U igual a 1, dito no cabeçalho de WedgeNet.lean), e towerWedgeData (v350) usa o fluxo da Torre como dado modular dessa cunha. Consulta: grep -rn 'wedgeNet_M|towerWedgeData' em TGLExt; grep -rl 'WedgeNet|towerWedgeData|theSpecificAQFTWitness' na pasta da entrega só acha IMPORTS.json. A entrega não cita nada disso. O não-mergulho (cunha física de Maxwell) mostra que essa identificação por desenho não vale para a luz física; o leitor pode achar que a ligação é nova ou que contradiz o kernel. Também existem negativos antigos sobre fluxo modular periódico e dilatação (ChatgptAudit.Geometry048.faithful_modular_dilation_localization_impossible); o novo não os duplica, mas não é situado entre eles. Duplicação de fato: nenhuma, e a ligação por rótulos (localEigenvalue com wedgeBoostMap) é inédita: nenhum arquivo do kernel contém ambos.

   *Conserto pedido:* Um parágrafo na PROVA: no modelo-testemunha v135 a cunha foi posta como a Torre por definição; na cunha física de Maxwell a Torre só indexa e não cabe (negativo).

5. **(MEDIO)** PROVA_E_ALCANCE.md:3; UNIDADE.json (fonte); OPERADOR_RESPOSTA_15nov.txt (455 bytes, sha16 b31c44a2c4e44c7e)

   A PROVA chama a cópia de 'fala integral do operador'. Ela começa por 'eu penso que temos sim que provar em LEan' e não consta no acervo: grep -l 'eu penso que temos sim que provar' em work\cunhagens_13out devolveu vazio. O arquivo do acervo (665 bytes, sha16 7cba650f330a99cf) começa por 'a luz testemunhada na cunha é o sujeito que o Nome designa. A Torre a indexa, a borda do horizonte oferece o contraste pelo qual ela é lida, e a relatividade vincula essa leitura ao observador' e termina em 'O COdex já está produzindo todas essas provas em LEan'. O trecho do meio é idêntico nos dois; a frase 'A Torre a indexa...' só existe no acervo. Não afirmo que a cópia seja falsa (pode ser a mensagem enviada ao Codex), mas a proveniência não é verificável aqui.

   *Conserto pedido:* Citar o arquivo do acervo com seu hash, ou marcar a cópia como [DECLARADO pelo Codex]; trocar 'fala integral' por 'trecho da fala'.

6. **(BAIXO)** Torre\TowerWedgeIndex.lean:274-290 (no_flow_intertwining_embedding); PROVA_E_ALCANCE.md:9

   Enunciado exato: para todo P, clock : R para R, phi : towerAlgebra P ->a[C] wedgeAlgebra C com phi injetiva e (forall t a, phi (factorFlow P (clock t) a) = C.flow t (phi a)), segue False. A prova usa só duas coisas gerais: a Torre tem projeção imóvel não escalar (site_fixed e site_nonscalar, valem para todo P e n) e a cunha tem centralizador trivial (LightRhoStar.centralizer_is_trivial). Não exclui mergulhos que não entrelacem os relógios nem a direção cunha para Torre; não depende do perfil. A PROVA não diz que é só de Torre para cunha. Não é vácuo: com a própria Torre como alvo, phi igual a identidade e clock igual a id satisfazem as hipóteses (exemplo compilado em C3_sem_torre.lean).

   *Conserto pedido:* Acrescentar à PROVA: 'só no sentido Torre para cunha; mergulhos que não preservam os relógios não são excluídos'.

7. **(BAIXO)** Torre\TowerWedgeIndex.lean:46-49 (tower_unit_flow), 259-261 (site_fixed), 54-58 (indexed_boost_translation), 24-26, 28-30

   Envoltórios de uma linha: tower_unit_flow é modularFlow_eigenvector (TGLExt\ModularFlowSpectrum.lean:74) com rapidity := log localEigenvalue; site_fixed é site_zero_modular_fixed (TGLExt\SiteLogLikelihood.lean:77); site_nonscalar é region_site_noncommutation (AffineClockAndRegion.lean:229); indexed_boost_translation é V_translations mais exp_log; exp_rapidity e rapidity_unique são exp e log. O conteúdo próprio da Torre é two_tower_*, o esticamento indexado e o não-mergulho.

   *Conserto pedido:* Marcar na PROVA o que é reexportação, para que a contagem de teoremas novos não infle (regra: 'sem gordura').

8. **(BAIXO)** Torre\TowerWedgeIndex.lean:90-100 (mixed_rapidities_dense, mixed_boost_orbit_dense); kernel TheMarkIsNotATypeMark.lean (v295)

   A marca log-densa reaparece em outro papel e a entrega não diz qual. Verifiquei que NÃO reintroduz a leitura refutada: a densidade é usada só como argumento de fecho (subgrupo denso mais conjunto fechado dá todo R) para vetores fixos; o tipo III1 vem do centro (Classificacao.lean, WedgeFactor, PhysicalCoreFactor); e os rótulos são autovalores verdadeiros do operador modular da Torre (localEigenvalue, com E_ij autovetor de Delta), não as razões de A e B arbitrários que a v295 refutou com M2(C). Mas grep -n 'marca|densa|dense' na PROVA só acha 'span denso' do núcleo, sem aviso.

   *Conserto pedido:* Uma frase: 'a densidade dos rótulos da Torre não é critério de tipo (TheMarkIsNotATypeMark); aqui só fecha o grupo dos boosts'.

9. **(BAIXO)** PROVA_E_ALCANCE.md:9; VinculoCriterion.lean:34-41; SignatureInTheLimit.lean:310 (mixProfile)

   Duas imprecisões: (a) 'os dois primeiros fatores 1/2 e 1/3' pode ser lido como fatores de von Neumann; são as duas primeiras razões modulares (os pesos de sítio de mixProfile são 1/3 e 1/4; log(1/2) e log(1/3) vêm de w/(1-w)). (b) ReadsTowerOnWedge fixa mixProfile embora as três cláusulas valham para todo P (indexed_* são gerais); a escolha não é explicada.

   *Conserto pedido:* Trocar 'fatores' por 'razões' e dizer que o diagrama vale para todo perfil, ou explicar por que se fixou o perfil misto.

10. **(BAIXO)** Reprodução: Torre\build\TowerWedgeIndex.olean (sha256 d19b4f19...) contra o meu P2\stage\TowerWedgeIndex.olean (a40408b7...)

   Informativo, não é defeito. Na minha invocação (lean.exe -R src -o, copia em P2) o objeto TowerWedgeIndex.olean não tem os mesmos bytes do recibo; fontes, logs, axiomas e avisos coincidem. A revisão do próprio Codex diz que o seu roteiro Recompilar.ps1 reproduz os objetos; não investiguei a causa (provável diferença de invocação).

   *Conserto pedido:* Se a custódia exigir hash de objeto, usar o roteiro do Codex.

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Na prova do Codex, a Torre funciona como a tabela de referência: cada unidade dela tem um número, e a cunha lê a luz nesse número; isso casa com o que o senhor disse em D (indexação, índice, torre).
- O Lean não prova que a Torre esteja dentro da luz da cunha; prova o contrário no sentido de caber: não há cópia fiel da Torre na cunha que leve o relógio de uma ao da outra.
- Proponho perguntar-lhe: 'a Torre a indexa' quer dizer só que a Torre aponta (tabela), ou também que ela é uma parte da luz? A prova de hoje sustenta a primeira e recusa a segunda.
- No modelo antigo da casa (v135) o fator da Torre foi posto à mão como a cunha; vale lhe dizer que isso foi escolha de modelo, não teorema sobre a luz de Maxwell.

## Examinado

- TEOREMA 1 rapidity (def, TowerWedgeIndex.lean:21): rapidity P N i j := Real.log (localEigenvalue P N i j) = log(w_i/w_j). Simples: o número que a unidade E_ij da Torre carrega (sua frequência no relógio da Torre). Todo P.
- TEOREMA 2 rapidity_comp (l.33): rapidity P N i j + rapidity P N j k = rapidity P N i k. Simples: ao compor unidades os números somam (telescópio dos logs). Todo P.
- TEOREMA 3 rapidity_refine (l.41): rapidity P (N+1) (i,a) (j,a) = rapidity P N i j. Simples: ao acrescentar um sítio à Torre o número não muda; unidades diferentes podem ter o mesmo número. Todo P.
- TEOREMA 4 tower_unit_flow (l.46): modularFlow P t (localEigenvector P N i j) = modularPhase t (rapidity P N i j) • localEigenvector P N i j. Simples: no relógio da Torre a unidade só gira de fase na frequência do seu número; é cópia de modularFlow_eigenvector do kernel. Todo P.
- TEOREMA 5 indexed_boost_translation (l.54): para todo C, P, N, i, j, l: ((lightBoost C).V (rapidity P N i j)).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) = (lightNet C).U ((localEigenvalue P N i j * l) • nullDir). Simples: o boost da cunha, com o número da unidade, estica a translação nula pela razão da unidade; vale para todo real s (exp de log). Todo P e todo C.
- TEOREMA 6 indexed_modular_translation (l.62): (lightDelta C (-(rapidity P N i j)/(2*pi))).conjStarAlgEquiv ((lightNet C).U (l • nullDir)) = (lightNet C).U ((localEigenvalue P N i j * l) • nullDir). Simples: o mesmo esticamento é o relógio modular do vácuo no instante -s/2pi. Todo P e C.
- TEOREMA 7 mixed_rapidities_dense (l.90): Dense (AddSubgroup.closure (rapidityLabels mixProfile)). Simples: os números da Torre mista (log 1/2 e log 1/3, incomensuráveis) geram um conjunto denso de reais. Só mixProfile.
- TEOREMA 8 mixed_boost_orbit_dense (l.96): para todo vetor v, a órbita de todos os boosts está no fecho da órbita pelo subgrupo gerado pelos números da Torre. Simples: continuidade mais densidade; nada específico da Torre além da densidade. Só mixProfile.
- TEOREMA 9 two_tower_boosts_read_vacuum (l.188): ((lightBoost C).V (rapidity mixProfile 0 0 1) v = v ∧ (lightBoost C).V (rapidity mixProfile 1 (0,0) (0,1)) v = v) ↔ v ∈ ℂ∙C.Ω. Simples: um vetor fixo pelos dois boosts da Torre mista é múltiplo do vácuo. Só mixProfile; todo C. Dominado por um só boost (controle C2).
- TEOREMA 10 two_tower_times_read_scalars (l.237): (C.flow (modularTime (rapidity mixProfile 0 0 1)) a = a ∧ C.flow (modularTime (rapidity mixProfile 1 (0,0) (0,1))) a = a) ↔ a é escalar. Simples: o mesmo para observáveis da cunha, por dois instantes do relógio do vácuo. Só mixProfile.
- TEOREMA 11 site_fixed (l.259): V350Continuous.factorFlow P t (siteProjection P n) = siteProjection P n. Simples: a projeção E_00 de um sítio não se mexe no relógio da Torre. Todo P; envoltório de site_zero_modular_fixed.
- TEOREMA 12 site_nonscalar (l.264): siteProjection P n ≠ algebraMap ℂ (towerAlgebra P) c para todo c. Simples: e ela não é múltiplo da identidade. Todo P.
- TEOREMA 13 no_flow_intertwining_embedding (l.277): para todo P, clock : ℝ → ℝ, φ : towerAlgebra P →ₐ[ℂ] wedgeAlgebra C, com φ injetiva e ∀ t a, φ (factorFlow P (clock t) a) = C.flow t (φ a), segue False. Simples: nenhuma cópia fiel da Torre na cunha leva o relógio da Torre ao da cunha, mesmo com troca qualquer de escala de tempo; só Torre para cunha. Todo P e todo C.
- TEOREMA 14 physical_wedge_index (l.292): o teorema 5 no certificado físico e em mixProfile.
- TEOREMA 15 physical_no_flow_intertwining_embedding (l.298): o teorema 13 no certificado físico.
- TEOREMA 16 tower_observer_diagram (VinculoCriterion.lean:49): para todo N i j, ReadsTowerOnWedge N i j, isto é, com s = rapidity mixProfile N i j e razão = localEigenvalue mixProfile N i j: (a) u(boost s x) = razão·u x e v(boost s x) = razão⁻¹·v x; (b) lightDelta física (modularTime s) leva U(l n) a U((razão·l) n); (c) para rho>0, log(u/v)/2 = s no ponto boosted de (0,rho,y,z). Simples: o mesmo número lido de três jeitos, todos válidos para qualquer real. Só mixProfile e certificado físico.
- RECOMPILAÇÃO: P2\build_chain.py (cópia em P2\src, saída em P2\stage) compilou TowerWedgeIndex, WedgeHorizonObserver, VinculoCriterion, WedgeFactor, PhysicalCoreCenter, PhysicalCoreMultipliers, FockCharacters, PhysicalCoreFactor e Classificacao: rc=0, sem sorryAx, axiomas no trio; hashes dos fontes TowerWedgeIndex, VinculoCriterion e Classificacao iguais aos do recibo (sha256sum).
- MUTAÇÕES (P2\mutate.py, saída em P2\mut; todas com rc=1): M1 rapidez dobrada (5 erros), M2 fator invertido (3), M3 só um gerador (3), M4 sem injetividade (3), M5 projeção trocada (2), M6 perfil geral em two_tower (3).
- CONTROLES POSITIVOS (P2\ctl, saída em P2\stage2; todos rc=0, trio): C1_perfil_meio (perfil todo 1/2: as hipóteses de two_tower valem para todo vetor), C2_via_mautner (um só boost implica o enunciado da Torre, com a candidata ErgodicidadeDeMautner recompilada em P2\src2, sha16 1074aa5b2c172960), C3_sem_torre (os enunciados indexados valem para todo real s e o exemplo de não-vacuidade do não-mergulho).
- KERNEL (grep -rn dentro de TGLExt, por Bash): definições SiteProfile (TowerDefinite.lean:53), mixProfile (SignatureInTheLimit.lean:310), localEigenvalue (ModularFlowSpectrum.lean:26), the_mixing_mark (MixedLadder.lean:141), light_modular_fixed_iff_vacuum (QGReaderUVLock.lean:149), centralizer_is_trivial (LightRhoStar.lean:71), WedgeNet.wedgeNet_M (l.323), V350WedgeModularData.towerWedgeData (l.70), Santo.lean:430, FaithfulGeometricLocalization.lean (Geometry048), TheMarkIsNotATypeMark.lean; busca de um_so_boost no kernel: ausente.
- LIDOS: PROVA_E_ALCANCE.md, Torre\RESULTADO.json e logs attempt01/attempt02 (erros preservados, final rc=0), VinculoCriterion.lean, Classificacao.lean, Horizonte\LEITURA_DA_CUNHA.md, IMPORTS.json (1291 fontes comparadas, zero diferenças), Revisao\PARECER_FINAL_R1.json, PARECER_PARCIAL_R1.json e ADENDO; acervo work\cunhagens_13out (resposta de tipo III, D e B do operador, hashes 7cba650f330a99cf e 09da32e3090f135a); Mapa de Rotas consultado por torre e K07 (nada registrado).


# CONFERÊNCIA DISTINTA — a segunda conferência de 16/11: tipo III; copiador e impostor R1; desenho R5 R1; partitura e errata K09; composto finito da T1 — A1-tipo-iii-lean-e-matematica

> Montado pela gerência c1 em 16/11/2026 06:23 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 1 ALTO, 4 MEDIO, 3 BAIXO

## Resumo

O Lean está certo; os textos precisam de consertos antes de ir ao operador. Recompilei as duas candidatas em cópia: código 0, nenhum aviso, 21 + 3 teoremas só com os três axiomas de sempre, e os hashes das fontes batem com o RESULTADO_GERENCIA.json. Nenhum teorema é vazio: habitei em Lean as hipóteses das recusas (B(C²), a álgebra abeliana gerada por uma projeção, o fluxo parado), e cada enunciado diz o que a docstring diz. A unicidade do relógio é real, mas não é nova: sai em quatro linhas de um teorema que o kernel já tinha, e nessa forma dispensa a hipótese da mesma conjugação e ainda dá a conjugação única. O "rfl" do fluxo é honesto: duas definições de arquivos diferentes dão o mesmo termo porque o certificado físico foi montado com o mesmo boost; é identidade por construção, não fato novo. O teorema afim da borda está certo e casa com o cisalhamento do Codex, mas "afim" é mais largo que a relatividade (cobre Galileu e dilatações) e isso não está dito. No UmSoBoost a equivalência não é trivial só pela ida (a volta usa o teorema de um só boost), e recompila contra o Mautner que recompilei da fonte cujo hash é o do log. Não há afirmação de que o predicado recusa II1 ou III_lambda por termo. Achado alto, de texto e não de Lean: a PROVA_E_ALCANCE não lê ao operador a escolha que a pergunta de 15/11 deixou com ele (qual enunciado leva o nome); o kernel já tinha a marca do estado, o Codex escolheu a do núcleo, e a tabela põe a do núcleo na linha do sujeito sem dizer que mudou a leitura ratificada. Médios: 16 dos 24 teoremas são, linha a linha, as sondas dos revisores P1, P2 e P3 de 15/11 e 4 são reexportações do Codex, mas o texto diz "o que a gerência acrescenta" e "sete revisores" (no tipo III foram quatro). Também médio: "a ordem foi provar em Lean" não está nos bytes da casa.

## Achados

1. **(ALTO)** PROVA_E_ALCANCE_GERENCIA.md secao 3 (l.39-43), secao 5 (l.80) e secao 7 (l.97-100)

   

   *Conserto pedido:* Acrescentar, antes da secao 3 e na secao 7, um paragrafo em lingua simples: ha' dois enunciados provados em Lean para a luz na cunha, o do estado (ja' no kernel; da' o III1 pelo teorema atribuido a Longo, citado) e o do nucleo (novo, do Codex; da' o III1 por Connes e Takesaki, citado); o Codex pos o nome no segundo; quem diz qual leva o nome, ou se os dois entram, e' o operador. Na secao 5, por a marca do estado na linha do sujeito ao lado do criterio do nucleo e dizer que a tabela MUDA dois pontos da leitura ratificada (sujeito e borda), nao so' a refina. Dizer com todas as letras que o elo com a classificacao nao foi construido em Lean.

2. **(MEDIO)** TipoIIIControles.lean l.35-37 (item 1 do cabecalho) e l.94-113 (o_fluxo_de_tomita_e_unico); PROVA_E_ALCANCE_GERENCIA.md l.55

   

   *Conserto pedido:* Trocar o enunciado pela forma forte (J1 e J2 quaisquer; conclui fluxo e conjugacao iguais) e dizer na docstring e na tabela: corolario do reconhecimento pelo conteudo do kernel com a identidade. No texto: dado o vetor, nem a conjugacao nem o fluxo sao escolha; o que o predicado deixa livre e' so' o vetor.

3. **(MEDIO)** TipoIIIControles.lean l.17-19 (cabecalho); PROVA_E_ALCANCE_GERENCIA.md l.49 ('O que a gerencia acrescenta (dois modulos, vinte e quatro teoremas...)')

   

   *Conserto pedido:* No cabecalho e na secao 4: dizer de onde veio cada bloco (P1: unicidade e recusas; P2: leitura para todo real e um so' boost; P3: unicidade afim), com o hash das sondas; trocar 'sete' por 'quatro'; dar a conta honesta (4 proprios, 16 adotados das sondas, 4 reexportacoes). Esta conferencia (A1) passa a ser a conferencia distinta desses teoremas.

4. **(MEDIO)** PROVA_E_ALCANCE_GERENCIA.md l.16 ('A ordem foi provar em Lean.'); TipoIIIControles.lean l.16 ('e pediu prova em Lean')

   

   *Conserto pedido:* Reescrever: 'ele disse que o Codex ja' estava produzindo essas provas em Lean (bytes da casa); ao Codex teria dito que e' preciso provar em Lean [DECLARADO pelo Codex]'. Ou pedir ao operador os bytes dessa fala.

5. **(MEDIO)** TipoIIIControles.lean l.52-55 e l.383-385; PROVA_E_ALCANCE_GERENCIA.md l.65-66 e l.82

   

   *Conserto pedido:* Dizer: 'afim (classe que contem as transformacoes da relatividade e outras; o teorema nao usa a metrica)'. Acrescentar o corolario dos observadores e citar esse como a face da relatividade. Trocar 'determina tudo' por 'determina a transformacao'.

6. **(BAIXO)** PROVA_E_ALCANCE_GERENCIA.md l.56 e l.80 ('Na cunha o relogio e' o boost, sem escolha'); secao 3 (l.32-37)

   

   *Conserto pedido:* Escrever 'dado o vacuo, o relogio e' o boost, sem escolha' e listar na secao 3 os dois passos citados.

7. **(BAIXO)** TipoIIIControles.lean l.137-143, l.195-198, l.244-247; PROVA_E_ALCANCE_GERENCIA.md l.58-60 e l.91

   

   *Conserto pedido:* Renomear ou anotar a recusa 'abeliana' como 'quem tem centro nao escalar'; corrigir a lista (I_n com n >= 2 e I_infinito em forma padrao, II1, II_infinito, III_0 e III_lambda); considerar a versao para todo tempo nao nulo.

8. **(BAIXO)** TipoIIIControles.lean l.2 (import), l.45-47, l.284-286, l.307-311; TipoIIIUmSoBoost.lean l.40-46; PROVA_E_ALCANCE_GERENCIA.md l.87

   

   *Conserto pedido:* Tirar a duplicata e a importacao; por o teorema da SondaVinculo como a forma do vinculo; ajustar a frase do kappa.

## Examinado

- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\TipoIIIControles.lean (inteiro; os 21 teoremas, um a um, contra docstring e tabela)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\TipoIIIUmSoBoost.lean (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\PROVA_E_ALCANCE_GERENCIA.md (inteiro)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\RESULTADO_GERENCIA.json (inteiro; hashes conferidos por sha256sum)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\tipo_iii\compilar_tipo_iii.ps1, build\*.log, dep_codex\MANIFESTO_DEP_CODEX.json, REV0 (hashes)
- dep_codex por leitura: VinculoCriterion, Classificacao, ObserverClassification, PhysicalCoreCenter, WedgeHorizonObserver, TowerWedgeIndex; PhysicalCoreFactor so' no teorema physical_core_is_factor
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\ErgodicidadeDeMautner.lean: so' o teorema de um so' boost (l.977-1006), o hash, o log e o RESULTADO_ErgodicidadeDeMautner.json
- Kernel por leitura (grep -rn pelo Bash): TGLExt\O16\ContentContractProposal.lean, RecognitionModular_v2.lean, RecognitionGraph_v2.lean, RecognitionReadout.lean, RecognitionSquare.lean (definicao); V351ResolventPhaseCalculus.lean e V351ResolventImaginaryPowers.lean (inicio); TheImportedSecondQuantization.lean (l.138-345 e 404-416); F1Fecho394\CanonicalFockRegularCoreR2.lean, RegularCovariantCoreR3.lean (l.1-150), RegularCoreFixedR3.lean (l.190-215), PhysicalFockNetRealizationR2.lean (l.60-95), CanonicalFockModularCoreInputR1.lean (l.126-140), SpacetimeLorentzFourierR3.lean (l.20-26); V350RegularGeneratedAlgebra.lean, V350L2OperatorLift.lean, V350L2Translation.lean; LightRhoStar.lean (l.63-77); QGReaderUVLock.lean (l.145-153); TheMarkIsNotATypeMark.lean (inicio); TheScaleHasNoFixedPoint.lean (l.55-75)
- Fala do operador por bytes: OPERADOR_15nov_resposta_tipo_iii_..._verbatim.txt (665 B, sha256 7cba650f...67da), a pergunta das 16:41, a ratificacao das 18:00, as duas de 16/11; busca nos 237 OPERADOR_*.txt
- Revisoes anteriores: REVISAO_EXAME_15nov_P1 (inteira); P2, P3 e P4 por busca e pelos achados; os cabecalhos de Q1, Q2 e Q3; as sondas dos revisores em scratchpad\v412_exame_codex_kimi (P1\tests, P2\ctl, P3\mut)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\pergunta_tipo_iii_15nov\PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md (secoes 1 a 5)
- C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\DESENHO_v412_R1.md (itens 20 e 22) e a memoria o-sujeito-do-tipo-iii-15nov.md (so' leitura)
- Copia do Codex da fala: kimi\K07\CODEX\TIPO_III1_VINCULO\OPERADOR_RESPOSTA_15nov.txt (so' leitura)
- Minhas notas: C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_conf2\A1\NOTAS_PARCIAIS.md


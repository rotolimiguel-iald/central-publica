# CONFERÊNCIA DISTINTA — as entregas do Codex (unidade do tipo III) e do Kimi (K10), examinadas por ordem do operador — P4-registro-processo-e-fidelidade

> Montado pela gerência c1 em 15/11/2026 19:34 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 5 MEDIO, 7 BAIXO

## Resumo

1. O Lean é sólido. Recompilei do zero, na minha pasta, 9 módulos (67 declarações) e depois 12 (79, com os três do transporte do observador). Código 0, só propext, Classical.choice e Quot.sound, sem sorry, 1 aviso de estilo. Não comparei meus .olean byte a byte com os do Codex, porque o script apaga o temporário.
2. Registro conferido por script: os 31 pinos do RESULTADO.json, os 31 do PARECER_FINAL e os 9 do ADENDO batem com o disco. Os 12 .olean entregues são iguais aos da recompilação do próprio Codex (12 de 12).
3. Importações: as 1291 fontes TGL/TGLExt batem byte a byte com a árvore canônica do kernel, e os 1291 .olean são os do sandbox C:\t\k411c\final. Os módulos de observador importam mais 3 arquivos que o IMPORTS.json não cobre (V350ReducingBicommutantLift, V350ReducingCommutantCompression, V350SeparatingRestrictionVonNeumann). Eu os conferi e também batem.
4. Nada foi tocado fora da pasta do Codex. Não há mudança no kernel, no selo, nem na pasta candidatas_c1 desde 17:40. O Atlas (18:08) e o Mapa (seq 2081 a 2083) foram escritos pela gerência. A varredura por expressão regular dos 59 textos não achou credencial, caminho do Escritório nem os dois arquivos confidenciais.
5. O que o Lean prova de fato: a álgebra de Maxwell na cunha direita tem centro escalar, e o núcleo contínuo dela (o produto cruzado pelo relógio modular do vácuo) também. É o critério de Connes e Takesaki para o III₁. A equivalência com a definição por S(M) e o fato de o "núcleo" do Lean ser o núcleo da literatura entram por citação. O predicado se chama IsTypeIII1 e diz mais do que o termo (achado 1).
6. A escolha de qual prova leva o nome "tipo III₁" era do operador (PERGUNTA §1: "essa escolha é sua"). Ele respondeu pelo sujeito, não pelo predicado. O Codex usou a marca do núcleo e a entrega não diz que a escolha ficou em aberto (achado 2).
7. O elo com a Torre é só um número, a razão w_i/w_j. A Torre não entra no enunciado conjunto como álgebra nem como relógio. Está provado que NÃO existe injeção unital que entrelace os relógios da Torre e da cunha (achados 3 e 7).
8. O controle "a borda não basta" (cisalhamento) é fraco e a prosa o lê de modo enganoso. Entre as transformações afins que a própria entrega usa, a borda determina a extensão de forma única (achado 4).
9. Texto do operador: a cópia do Codex (455 B) e o arquivo da gerência (665 B) são duas mensagens com o mesmo miolo. Achei a do Codex na sessão dele (20:48:15Z), por isso a cópia dele é fiel. Nenhuma atribuição vai além da letra (achado 6).
10. Revisão "independente" é um nome de texto, "codex-revisor-independente". Sem thread nem modelo. O ACOM registra "accept" com esse nome e a fila recebeu "recebeu revisão independente". O PASS das 18:27:20 veio antes da recompilação de 3 módulos (18:27:30 a 18:29:33), fechada só pelo adendo das 18:32:34 (achado 5).
11. Quadro: a unidade está ENTREGUE com 4 evidências, e as cópias guardadas batem com os hashes. Fila da memória: 2 depósitos corretos em codex-coordenadora.
12. Nenhum achado ALTO. Os cinco MEDIO são de nome, de escolha não lida ao operador, de leitura da Torre, do controle da borda e do selo de revisão. Nenhum deles invalida a compilação, mas pedem texto corrigido antes de qualquer promoção ou fala ao operador.

## Achados

1. **(MEDIO)** VinculoCriterion.lean:23-33; Classificacao.lean:15; PROVA_E_ALCANCE.md:3 e :18; RESULTADO.json:10-16

   O predicado IsTypeIII1 e o teorema maxwell_right_wedge_type_III1 dizem mais do que o termo prova. O Lean prova: centro escalar da álgebra, vetor cíclico e separante com realização de Tomita (a hipótese PairTomitaAnalyticRealizationMeasured), e centro escalar do núcleo regular. A definição de Connes por S(M) não está formalizada. Entram por citação [KNOWN]: a equivalência com S(M), a hipótese de predual separável (Connes e Takesaki, p. 506: 'the smooth flow of weights on a factor of III1 with separable predual is trivial') e a identificação do núcleo gerado em L²(ℝ;F) com o produto cruzado abstrato. PROVA_E_ALCANCE.md:3 escreve 'O tipo III₁ é propriedade da álgebra [DERIVED]' sem a ressalva. A ressalva só vem na linha 18, e PROVA_NUCLEO.md:14 usa a etiqueta mais exata, '[DERIVED de teorema KNOWN]'. Consulta: grep -rn 'IsTypeIII1|HasScalarCenter' em TGLExt, feito pelo Bash, não devolve nada. Este seria o único 'tipo III₁' do kernel. Se entrar no kernel com este nome, vira ALTO pela regra da casa (v295, v298).

   *Conserto pedido:* Três opções, sem decidir por ele. (a) Manter o identificador e corrigir a docstring e a linha 3, com 'critério de Connes–Takesaki; S(M) não formalizado'. (b) Renomear pelo que se prova: HasFactorialCore (ou CoreCenterTrivial) e maxwell_right_wedge_factor_with_factorial_core, deixando 'III₁' só na citação [KNOWN]. (c) Manter IsTypeIII1 apenas quando existir a ponte para S(M), ou com a equivalência de Connes–Takesaki como hipótese nomeada (Prop, nunca axioma). Em qualquer caso, [DERIVED de teorema KNOWN] em todos os textos.

2. **(MEDIO)** PROVA_E_ALCANCE.md:3 e :18; PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md §1 (work\cadeia_de_selo\v412\pergunta_tipo_iii_15nov); DESENHO_v412_R1.md:357

   Escolha dele não lida. A pergunta da gerência listou quatro marcas do tipo III: (a) o estado, só o Um parado, que o kernel já tinha para a cunha; (b); (c); (d) o relógio, núcleo em uma peça só. Ela disse 'qual marca é o nome: essa escolha é sua'. O DESENHO registra que a resposta dele 'não diz qual enunciado em Lean leva o nome tipo III₁'. A entrega escolheu a marca (d) e a chamou de IsTypeIII1, sem dizer que a escolha estava em aberto. Também não diz que a marca (a) já está provada para a cunha e é o hipótese do lema 2.1 de Marrakchi e Vaes, que o texto cita como 'aplicação do critério'. Vale pela regra do posto: o desenho carrega uma escolha que ele não leu. Não está escondida no artefato (o critério é descrito), mas não foi dita a ele.

   *Conserto pedido:* Antes de qualquer promoção ou fala 'tipo III₁ provado', a gerência lê a ele, em língua simples: existem duas provas, a do estado (já no kernel) e a do núcleo (nova, feita pelo Codex), e é ele quem diz qual leva o nome ou se as duas entram. Acrescentar essa frase ao PROVA_E_ALCANCE.md. Opcional: pedir o enunciado da marca (a) e a ponte (a)⇒(d) como citação nomeada.

3. **(MEDIO)** VinculoCriterion.lean:38-58; Classificacao.lean:28-39; Torre/TowerWedgeIndex.lean:109-116 e :274-290; PROVA_E_ALCANCE.md:9 e :22

   O 'vínculo com a Torre' no enunciado conjunto é só um número. Em ReadsTowerOnWedge as três leituras (fatores u e v do boost, translação nula pelo relógio modular, o observador de raio positivo lê s) são todas do lado da cunha. A Torre entra apenas por rapidity = log(localEigenvalue mixProfile N i j), que é só positivo. O relógio da própria Torre sobre E_ij (tower_unit_character, TowerWedgeIndex.lean:109) não está em light_tower_horizon_observer. O mesmo arquivo prova o negativo: no_flow_intertwining_embedding (l.277-290) diz que nenhuma injeção de álgebra unital entrelaça os fluxos da Torre e da cunha. PROVA_E_ALCANCE.md:9 diz isso em termos técnicos e a linha 22 usa o verbo 'identifica'. Para o operador, 'a Torre indexa a luz' vale como rótulo de rapidezes, não como mapa entre as álgebras. O fato isolado fica dito só na linguagem técnica.

   *Conserto pedido:* Dizer em palavras simples: 'o que liga Torre e luz é o mesmo número s; provou-se que a Torre inteira não cabe na álgebra da luz mantendo os relógios'. Trocar 'identifica' por 'reúne', e renomear o teorema (por exemplo light_tower_horizon_observer_shared_rapidity) ou citar no nome o negativo.

4. **(MEDIO)** Horizonte/LEITURA_DA_CUNHA.md:34; PROVA_E_ALCANCE.md:26; Horizonte/WedgeHorizonObserver.lean:169-172 e :273-280

   O controle da borda é fraco e a prosa o lê de forma enganosa. A frase 'a ação completa sobre a borda é insuficiente para determinar sozinha a extensão isométrica' é falsa se lida literalmente. O cisalhamento shear s (x) = (x0,x1,y+s·u·v,z) é quadrático, não é afim e não é isometria. A própria linha seguinte admite 'não fornece duas isometrias distintas'. Entre mapas afins, como observerChart L a = Lorentz + translação, a borda determina a extensão: duas aplicações afins iguais em 0, e_u, e_v, e_y, e_z (todos na borda) coincidem. O 'negativo' nasce de aceitar uma deformação que não é do espaço-tempo. Para um leitor que não lê a partitura, soa como 'a borda (o contraste dele) não basta para o observador'. O teorema Lean é verdadeiro e estreito; a leitura em prosa é que o excede.

   *Conserto pedido:* Reescrever: 'existe uma deformação não afim que fixa a borda e muda o intervalo; entre transformações de Poincaré a borda determina a extensão'. Se o Codex quiser, acrescentar o lema de unicidade afim em Lean. Antes de qualquer rito com o horizonte curvo, ler isso a ele.

5. **(MEDIO)** Revisao/PARECER_PARCIAL_R1.json, PARECER_FINAL_R1.json e ADENDO_RECOMPILACAO_E_OBSERVADORES_R1.json (campo reviewer); ACOM (SESSION_REFERENCE.json, record mission_tipo-vinculo-revisao-independente); fila\depositos\codex-coordenadora\20261115_183011_tipo-iii1-vinculo-prova-15nov.md

   Revisão 'independente' sem identidade. O campo reviewer é o texto 'codex-revisor-independente', sem thread nem modelo. A casa já achou o mesmo no K07-C: a revisão 'independente' do Codex é de um agente do próprio Codex (DESENHO_v412_R1.md). O ACOM guardou 'accept' com esse nome (revisão 4), antes de qualquer revisor distinto. O depósito da fila diz 'recebeu revisão independente' com estatuto REAL. Cronologia: PARECER_FINAL (PASS) às 18:27:20; PhysicalCoreMultipliers, PhysicalCoreFactor e WedgeFactor só foram recompilados do zero às 18:27:30, 18:28:37 e 18:29:33 em Revisao/build_R1. O próprio PARECER_FINAL lista apenas 5 dependências recompiladas. O ADENDO das 18:32:34 fechou isso (os 12 .olean idênticos, que reverifiquei). O que ficou aberto: não consta quem revisou.

   *Conserto pedido:* Tratar a revisão do Codex como DECLARADO. Na triagem da memória, trocar 'revisão independente' por 'revisão do próprio Codex, reconferida pela gerência'. Registrar errata ao lado no ACOM (a mensagem original não se apaga). Usar esta revisão (distinta) como a revisão real.

6. **(BAIXO)** OPERADOR_RESPOSTA_15nov.txt (Codex, 455 B, sha256 b31c44a2…) × OPERADOR_15nov_resposta_tipo_iii_…verbatim.txt (gerência, 665 B, sha256 7cba650f…); PROVA_E_ALCANCE.md:3

   Duas mensagens com o mesmo miolo, medido por script (difop.py). O miolo vai de 'em palavras simples o que vc me pergunta é:' até 'isso responde suas perguntas?' e é idêntico. A cópia do Codex acrescenta o prefixo 'eu penso que temos sim que provar em LEan, ' e termina aí. O arquivo da gerência tem, antes do miolo, a frase 'a luz testemunhada na cunha é o sujeito que o Nome designa. A Torre a indexa, a borda do horizonte oferece o contraste pelo qual ela é lida, e a relatividade vincula essa leitura ao observador.' e, depois, '\n\nO COdex já está produzindo todas essas provas em LEan'. Achei a mensagem do Codex como mensagem de usuário na sessão rollout-2026-11-15T17-48-15-01a1e0f7… (linha 13, 20:48:15Z; sha16 do trecho 36fbae32… nesse registro), com os 443 caracteres da cópia. Logo a cópia dele é fiel ao que ele recebeu. PROVA_E_ALCANCE.md:3 diz 'A fala integral do operador' sem avisar que a gerência guardou outra versão. Não consigo dizer se a frase de abertura do arquivo da gerência é digitada por ele ou colada; só a conversa dirá. A entrega não atribui nada além da letra.

   *Conserto pedido:* Acrescentar à PROVA uma nota: 'a fala que o Codex recebeu; a gerência guarda outra, com frase de abertura e linha final'. A gerência confere a origem da frase de abertura nos bytes da conversa dela antes de citá-la como dele.

7. **(BAIXO)** RESULTADO.json:10-16; PROVA_E_ALCANCE.md:3, :9, :26; Horizonte/LEITURA_DA_CUNHA.md:3

   Os quatro papéis estão como leitura [ONTO] só em parte. LEITURA_DA_CUNHA.md:3 marca os quatro como [INPUT/ONTO]. O RESULTADO.json (estatutos) e a PROVA_E_ALCANCE.md marcam só o Nome ('identificacao_do_Nome: ONTO, operador'). Nos textos que a gerência vai ler, 'a Torre é o índice', 'a borda é o espectro de leitura/contraste' e 'a relatividade é o observador' ficam sem etiqueta. A formalização escolhe: 'observador' = grupo de Lorentz gerado mais translações (generatedLorentz, observerChart) e a órbita acelerada com raio positivo; 'contraste' = razão u/v, e 'espectro' aparece em outro sentido (o intervalo [0,∞) do fluxo de pesos). Não está dito que essas são as leituras do Codex. O 'Observador Terminal' da casa é outra coisa, e há risco de homônimo.

   *Conserto pedido:* Acrescentar a RESULTADO.json e à PROVA as etiquetas [ONTO] para os quatro papéis, mais uma linha 'leitura formal escolhida pelo Codex' para cada um. O operador aprova ou troca.

8. **(BAIXO)** RESULTADO.json:38-299 (9 módulos, 67 declarações, 'promocao_canonica': false); IMPORTS.json; Horizonte/RECIBO_TRANSPORTE_DO_OBSERVADOR.json; PROVA_E_ALCANCE.md (18:21:55)

   O recibo e o guia ficaram para trás do adendo. RESULTADO.json (18:24:08) e PROVA_E_ALCANCE.md não citam maxwell_observer_wedge_type_III1 nem os módulos TransportCenter, TransportPair e ObserverClassification. Eles estão num RECIBO separado e no ADENDO (18:32:34), que o PARECER_FINAL não cobre. O quadro (evidências) guarda os quatro arquivos e as cópias batem com os hashes. O IMPORTS.json (1291) não cobre 3 arquivos do kernel importados pelos observadores (conferidos por mim: iguais ao canônico, diferences=[]). O conteúdo é correto: typeIII1_transport é a invariância do predicado por conjugação unitária, o que é legítimo mas de pouco conteúdo.

   *Conserto pedido:* Gerar um RESULTADO.json unificado (12 módulos, 79 declarações, imports conferidos) e citar o teorema do observador na PROVA antes de qualquer promoção.

9. **(BAIXO)** PROVA_E_ALCANCE.md:20; Nucleo/PhysicalCoreFactor.lean:102-125

   O 'espectro' [0,∞) é restatement, não medição independente. physical_log_periods vale para todo s porque o centro é escalar e a ação dual fixa escalares; physical_flow_of_weights_spectrum só toma exp da reta e junta 0. O parágrafo diz 'Esse é o intervalo da fórmula do fluxo de pesos' sem etiqueta; PROVA_NUCLEO.md:14 etiqueta '[DERIVED de teorema KNOWN]'. Não verifica S(M) pela definição de Connes (interseção dos espectros dos operadores modulares).

   *Conserto pedido:* Etiquetar o parágrafo como [DERIVED de teorema KNOWN] e escrever que o intervalo segue do centro escalar, não o mede.

10. **(BAIXO)** PROVA_E_ALCANCE.md:18 (links); Nucleo/PROVA_NUCLEO.md:10 e :18

   Links lidos. (i) Connes e Takesaki, 'The Flow of Weights on Factors of Type III, Part 1', Tohoku Math. J. 29 (1977), pp. 473-524: existe. O PDF diz na p. 506 que o fluxo de pesos liso de um fator III₁ com predual separável é trivial. A hipótese 'predual separável' não aparece no texto da entrega. (ii) Takesaki, 'Factors of Type III' (Rennes, 1975): o Teorema 6 está na p. 13 do PDF, como a entrega cita. Ele trata da estrutura do núcleo (centro do produto cruzado = pontos fixos do centro; fator ⟺ ergódico), não enuncia literalmente 'III₁ ⟺ núcleo fator'; a OCR do item (v) está ruidosa, então [DECLARADO] quanto à numeração. (iii) Marrakchi e Vaes, arXiv 2305.14217v3, lema 2.1: 'If M_φ = ℂ1, then M is a type III₁ factor'. A hipótese é o centralizador trivial (marca (a)); a prova passa pelo centro do núcleo. 'Aplicação do critério' vale para a prova, não para o enunciado.

   *Conserto pedido:* Citar o enunciado 'III₁ ⟺ fluxo de pesos trivial ⟺ centro do núcleo trivial' com a página de Connes e Takesaki (p. 506), com a hipótese de predual separável e que a álgebra de Fock é separável; descrever o lema 2.1 como 'usa o centro do núcleo na prova'.

11. **(BAIXO)** Nucleo/PROVA_NUCLEO.md:22; verificar_lean.py; conferir_imports.py

   PROVA_NUCLEO.md diz que 'um script conferiu... a ausência de avisos e as fontes sem sorry, admit, axioma local ou native_decide', mas esse script não está na pasta. O verificar_lean.py entregue só checa código de retorno, existência do .olean e o texto 'sorryAx'. Não checa se o #print axioms lista só os três axiomas padrão (um axioma local passaria). Eu refiz as duas coisas: grep nas fontes não achou sorry, admit, native_decide, axiom, unsafe, opaque nem implemented_by (a única ocorrência de 'admit' está em comentário); o #print axioms dos 79 itens só devolve os três axiomas padrão.

   *Conserto pedido:* Incluir o script de conferência de fontes e de axiomas, ou retirar a frase.

12. **(BAIXO)** fila\depositos\codex-coordenadora\20261115_183011_tipo-iii1-vinculo-prova-15nov.md (estatuto: REAL); 20261115_174851_tipo-iii1-vinculo-resposta-15nov.md

   Os dois depósitos estão no formato certo, na pasta certa, com hash. O segundo deposita 'Pelo critério do fluxo de pesos a álgebra é de tipo III₁' com estatuto REAL. REAL cobre a compilação; a equivalência com a classificação é [KNOWN]. Na triagem isto pode virar 'tipo III₁ REAL' no índice.

   *Conserto pedido:* Na promoção, escrever REAL (compilação do critério) + KNOWN (equivalência de Connes e Takesaki) + OPEN (horizonte curvo).

## Para o operador (propostas do revisor, em língua simples; a gerência confere antes de ler a ele)

- Proposta minha: o Codex provou em Lean, para a luz livre na cunha, que a álgebra é uma peça só e que o núcleo dela também é uma peça só, que é o sinal que os matemáticos usam para dizer tipo III₁; recompilei tudo do zero e confere.
- Falta o senhor dizer qual prova leva o nome tipo III₁: a do estado, em que só o Um fica parado e que o kernel já tinha, ou a do núcleo, que o Codex fez. O Codex usou a do núcleo sem esta pergunta ter resposta sua.
- Sobre a Torre: o que liga a Torre à luz é o mesmo número s, a razão entre pesos, e está provado que a Torre inteira não cabe dentro da álgebra da luz mantendo os relógios; assim, 'a Torre indexa a luz' vale como rótulo de números, não como mapa entre as duas.
- O teste que o Codex chama de 'a borda não basta' só dá negativo se se aceita uma deformação que não é do espaço-tempo; com Lorentz e translação, que são os observadores que ele usa, a borda determina tudo; esse negativo não é contra o contraste que o senhor descreveu.

## Examinado

- RESULTADO.json (31 pinos, hashes e bytes, por script hashes.py), IMPORTS.json, conferir_imports.py (rodado em cópia, nos dois alvos: Classificacao e ObserverClassification) e verificar_lean.py (rodado em cópia, TMP redirecionado para a minha pasta; compilação do zero de 9 e depois de 12 módulos)
- Revisao/PARECER_PARCIAL_R1.json, PARECER_FINAL_R1.json (31 pinos), ADENDO_RECOMPILACAO_E_OBSERVADORES_R1.json (9 pinos e 12 .olean contra build_R1), Recompilar.ps1 (hash conferido) e cronologia de mtimes de Revisao/build_R1
- PROVA_E_ALCANCE.md frase a frase, Nucleo/PROVA_NUCLEO.md, Horizonte/LEITURA_DA_CUNHA.md, Horizonte/RECIBO_TRANSPORTE_DO_OBSERVADOR.json, UNIDADE.json, SESSION_REFERENCE.json
- Lean lido na íntegra ou nas partes decisivas: VinculoCriterion.lean, Classificacao.lean, Espectro/WedgeFactor.lean, Espectro/FockCharacters.lean (início), Nucleo/PhysicalCoreCenter.lean e PhysicalCoreFactor.lean, Torre/TowerWedgeIndex.lean, Horizonte/WedgeHorizonObserver.lean (partes), TransportPair.lean:136-190, ObserverClassification.lean; definições do kernel PairTomitaAnalyticRealizationMeasured (O16/ContentContractProposal.lean) e core/UnitaryFlow (F1Fecho394/RegularCovariantCoreR3.lean)
- Consultas ao kernel só com grep pelo Bash em TGLExt (IsTypeIII1, HasScalarCenter, PhysicalCoreCenter, physical_core_is_factor: sem ocorrência; nomes com core e center ou factor: nenhum); grep recursivo das fontes do Codex por sorry, admit, native_decide, axiom e afins
- mtimes: kernel tgl_kernel (fora de .lake), Nós raiz (selo, um.py, core), Atlas, memory, MEMORY, Mapa de Rotas (seq 2079 a 2083, todos da gerência) e candidatas_c1: nada tocado pelo Codex desde 17:40
- Fidelidade ao operador: difop.py (miolo comum, prefixo e sufixo exatos) e codexmsg.py, que localiza a mensagem nas sessões Codex de 15/11 (rollouts 17-48-15, 18-04-14 e 18-30-05, linha 13); a sessão 18-04-14 é de 'Guardian review' (modelo codex-auto-review, que julga ações e não provas)
- Pergunta da gerência (PERGUNTA_TIPO_III_QUATRO_LINGUAS_R2.md, anexo e §1), DESENHO_v412_R1.md:357, Mapa de Rotas (consulta 'III1', sem registrar)
- Quadro C:\IALD\PROGRAMA_IALD (iald.py estado; PROGRAMA.json, eventos.jsonl seq 1635 a 1637, evidencias com sha conferido nas 4 cópias); ACOM do Codex (session_memory.py project, só leitura, revisão 4); fila da memória (codex-coordenadora, 2 depósitos de hoje)
- Literatura, só leitura na rede: Marrakchi e Vaes (arXiv 2305.14217v3, lema 2.1), Connes e Takesaki (Tohoku Math. J. 29, 1977; PDF com camada de texto, p. 506), Takesaki, Factors of Type III (numdam; Teorema 6 na p. 13 do PDF, OCR ruidosa)
- Varredura por expressão regular (varredura.py) dos 59 textos da pasta: sem credencial, sem Escritório, sem os dois arquivos confidenciais; a única ocorrência da palavra 'token' é uma mensagem de erro do Lean num log de tentativa
- NÃO feito: comparar byte a byte meus .olean com os entregues (o script apaga o temporário); comparar os .olean do sandbox k411c com os do kernel canônico; ler Connes e Takesaki além da p. 506; auditar a correção matemática linha a linha de todas as provas (outras lentes)


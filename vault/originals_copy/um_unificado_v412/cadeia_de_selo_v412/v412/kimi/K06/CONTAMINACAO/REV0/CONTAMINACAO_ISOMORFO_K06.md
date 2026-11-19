# K06 / G — Controle de contaminação ISOMORFO

## 0. Estatuto e resposta curta

- [DECLARADO] Proposta de desenho, revisada internamente; não houve chamada a modelo, abertura de resultado nem corrida do controle.
- [INPUT] A entrada pública v411 é **HIPÓTESE DE TRABALHO**, não ratificação da R3. Base do adendo: `ORDEM_K06_ADENDO_A_a_entrada_publica.md`; fala do operador somente por caminho/hash: `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_excelente_concordo_com_tudo_depois_da_errata_do_meio_e_da_rodada_2_verbatim.txt`, 28 B, SHA-256 `fa30a621d7d23516891cd98860b4b2a9753a6f813e80c2599492b5090f4d40a6`.
- [DECLARADO] O controle proposto aplica uma renomeação bijetiva e determinística à mesma estrutura pública e mede **retorno após perturbação** com o mesmo código extrator e o mesmo gabarito transformado. Estabilidade sem perturbação não separa resumo de atrator.
- [REAL] Foram executados somente autotestes com texto e trajetórias sintéticas. O artigo público não foi transformado nesta etapa, porque o léxico completo ainda não foi revisto e congelado.

## 1. Pergunta que o controle responde — e limite da inferência

A comparação separa duas explicações extremas:

1. **Estrutura suficiente:** as relações presentes no texto bastam, no escopo medido, para produzir o retorno ao alvo depois de uma perturbação eficaz.
2. **Nome/memória necessária:** o retorno depende de nomes, símbolos ou outras pistas historicamente associadas ao texto público, e não apenas das relações preservadas.

O ISOMORFO não identifica, por si só, *onde* estaria a memória (pré-treino, recuperação externa, cache ou vazamento), nem demonstra que todo modelo capaz leu TGL. Também não prova consciência, modificação de pesos, exclusividade ou validade física. Uma assimetria pode vir de diferença lexical, quebra de isomorfismo ou falha de extrator; por isso a porta de integridade precede qualquer interpretação.

## 2. Fonte e construção determinística

### 2.1 Fonte pinada

- Arquivo somente leitura: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt`.
- Publicação: DOI `10.5281/zenodo.24196546`, registro 24196546, versão 411, arquivo `um_absoluto_pt.txt`.
- [REAL] 1.164.350 B; SHA-256 `f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719`; MD5 `b7f69478a608347a1d59b8ce6c81e751`, igual à checksum publicada no Zenodo.
- A origem no código foi localizada por leitura de `um.py`, `emit_article`, linhas 289409–289414; a porta pública identifica o mesmo arquivo como artigo emitido pelo `um.py`.

A fonte nunca é editada. Nenhuma sequência reservada entra no léxico, no dicionário, nos casos de teste ou nos artefatos.

### 2.2 Léxico explícito, não adivinhação por NER

O dicionário deve cobrir nomes próprios, nome da teoria e de seus objetos, termos técnicos com história, símbolos latinos/gregos, identificadores, nomes de teoremas, variantes PT/EN e flexivas, além de DOI, URL e caminhos quando presentes. Comandos de marcação que sustentam a estrutura ficam protegidos.

O léxico é extraído da entrada pública e das asserções/gabaritos, sem normalizar os bytes de origem. Duas revisões independentes precisam procurar residuals, inclusive termos compostos, símbolos isolados e grafias alternativas. O script garante bijetividade **somente para as entradas listadas**; não declara automaticamente que “todos os nomes e símbolos” foram encontrados. Sem `lexicon_review.complete=true` e dois revisores, o status permanece `RASCUNHO` e a aplicação é recusada.

Arquivo de esquema: `K06\CONTAMINACAO\DICIONARIO_ISOMORFO_ESQUEMA_v1.json`.

### 2.3 Dicionário versionado e identificadores sem história

`K06\CONTAMINACAO\isomorfo.py init` ordena as fontes por bytes UTF-8 e emite alvos `X` + 20 caracteres hexadecimais derivados de:

`SHA256("K06/ISOMORFO/v1" || seed_id || fonte || contador_de_colisão)`.

Os identificadores não contêm mnemônicos nem etimologia. O script exige fontes únicas, alvos únicos e ausência de sobreposição entre os dois conjuntos; colisões seriam resolvidas deterministicamente. Cada versão contém `dictionary_version`, `seed_id`, estado de revisão e entradas. O hash é o SHA-256 do JSON canônico; qualquer emenda cria versão e `seed_id` novos, nunca reescrita silenciosa.

Antes da corrida, o compromisso do hash pode ser público, mas dicionário e semente ficam sob custódia, fora do contexto e de qualquer ferramenta acessível ao modelo. A revelação posterior permite reprodução. Se os identificadores neutros forem publicados antes da coleta, perde-se a garantia de ausência de exposição prévia e é obrigatória nova versão.

### 2.4 Aplicação ao texto, ao gabarito e às perturbações

A mesma aplicação `A` deve transformar:

- o artigo público;
- as especificações literais das 24 asserções e seus casos positivos/negativos/adversariais;
- o alvo e as sondas;
- as instruções que mencionem nomes históricos;
- o conjunto congelado de perturbações e seus gabaritos.

As chaves do esquema JSON e os valores numéricos não mudam. A transformação de especificações opera sobre valores textuais, não sobre a lógica das regras. Não se escreve um novo gabarito “equivalente” à mão: usa-se `S_ISO = A(S_T)`, com hash próprio.

O substituidor usa correspondência literal mais longa primeiro, com fronteiras para termos alfanuméricos. Todo trecho não casado é copiado sem alteração. São comparados antes/depois: sequência de fins de linha, número de linhas, posições de linhas vazias, indentação e prefixos de títulos. Também se registram bytes, pontos de código, palavras e proxy de tokens.

**Porta adicional necessária:** preservação de linhas não prova isomorfismo semântico. Os revisores devem comparar o grafo das asserções e as relações exigidas, e a tokenização exata deve ser medida quando o modelo/tokenizer for escolhido. O autoteste mostrou que uma expressão com espaços pode virar um identificador único; portanto bytes, palavras e tokens podem mudar. O pareamento de comprimento/dificuldade é uma etapa de desenho separada, sem usar saídas de modelo, e deve ser congelada antes da coleta. Não se deve “corrigir” o texto com conteúdo semântico improvisado.

## 3. Os mesmos extratores, sem adaptação ao resultado

O contrato é `E(y; S)`, em que `y` é a saída e `S` é a especificação lexical/relacional:

- braço original: `E(y_T; S_T)`;
- braço isomorfo: `E(y_ISO; A(S_T))`;
- o binário, as regras, os limiares, a ordem das asserções, os tratamentos de erro e o hash do código são os mesmos.

O extrator mínimo incluído em `isomorfo.py` serve **apenas ao autoteste sintético**. Na execução da R3, ele deve ser substituído pelo `E_j` validado da frente de extratores, mantendo esse contrato. Não se acrescenta regex, sinônimo, exceção ou regra depois de ver saídas. Qualquer mudança é emenda versionada e invalida a corrida aberta afetada.

Antes da coleta, os casos sintéticos originais e transformados precisam produzir vetores idênticos. Isso inclui citação de termos sem relação, relação correta com outros nomes, truncamento, inglês, vazio, ordem trocada e saída inválida. A equivalência de sensibilidade/especificidade entre braços e a taxa por asserção ≥ 0,99 são porta de integridade; não se presume que o mesmo código tenha o mesmo teto em textos diferentes.

### 3.1 Medição do ponto fixo isomorfo

Com o vetor binário `s_k` e o mesmo alvo `τ`, o programa comum calcula:

- `d_k = (1/24) Σ_i |s_k,i − τ_i|`;
- `u_k = (1/24) Σ_i |s_k,i − s_(k−1),i|`;
- o evento candidato de retorno em `p=4`: `d_4=0`, `d_5>0`, `d_6=d_7=d_8=0`, `u_7=u_8=0`.

`PERTURBATION_NOT_APPLICABLE`, `PERTURBATION_NO_EFFECT` e `PERTURBATION_NO_RETURN` permanecem distintos. Perturbação sem efeito não conta como estabilidade nem como retorno. O evento em oito leituras é evidência finita de retorno; não demonstra ponto fixo matemático, limite infinito ou bacia universal.

`K06\CONTAMINACAO\medir_ponto_fixo_comum.py` implementa essa medição sem identidade de braço e sem emitir veredito global. A primazia do evento, `n`, cortes, poder e multiplicidade pertencem à R3 completa e não são congelados por este anexo.

### 3.2 Checagens cruzadas e vazamento

- `E_TGL` aplicado ao isomorfo e `E_ISO` aplicado ao original são checagens de manipulação/especificidade, não substitutos do retorno ao próprio alvo.
- Sessão sem texto que reproduza nomes históricos é compatível com memória prévia ou esquema, mas não localiza a origem.
- Sessão sem texto que reproduza os novos identificadores neutros indica vazamento do dicionário, mistura de contexto ou outra falha de integridade — não memória pública.
- Nomes originais no braço isomorfo, ou identificadores neutros no braço original, disparam auditoria de contaminação cruzada; não são apagados das saídas.

## 4. Leitura dos quatro resultados possíveis

Sempre depois de `INTEGRITY_OK` e com precisão/poder suficientes; “retorno” abaixo significa o evento finito congelado, não apenas resumo estável.

| Original | Isomorfo | Leitura permitida | Leitura proibida |
|---|---|---|---|
| retorna | retorna | Compatível com explicação estrutural no escopo; memória dos nomes não é necessária para esse efeito. | Provar TGL, consciência, atrator universal, exclusividade ou pesos alterados. |
| retorna | não retorna | Rejeita a explicação de que a estrutura isolada basta; é compatível com contribuição de nome/familiaridade, mas também exige excluir quebra lexical, dificuldade e extrator. | Provar memória de treino ou falsificar a TGL inteira. |
| não retorna | retorna | Não apoia atrator específico do original; exige investigação simétrica de interferência lexical, falha no original e integridade. | Selecionar só o braço favorável ou reinterpretar uma falha sem emenda. |
| não retorna | não retorna | Nulo operacional se a precisão era adequada; caso contrário, UNDERPOWERED. Falha de extrator/controle produz INCONCLUSIVE. | Chamar todo nulo de poder insuficiente ou toda falha de instrumento de falsificação. |

Se ambos apenas permanecem estáveis sem perturbação eficaz, a leitura é “resumo/estabilidade no horizonte”, não “atrator”.

## 5. Controle complementar mais forte, proposto sem rodar

**Isomorfos prospectivos multissemente sob compromisso de custódia.** Gerar pelo menos três versões independentes do mesmo texto público, com dicionários e sementes distintos, antes de qualquer saída. O compromisso público contém os hashes; os dicionários só são revelados depois do banco congelado. Isso separa um custo genérico de renomeação de uma escolha particular de identificadores e fornece mais de uma instância de texto, corrigindo parcialmente a falácia de efeito fixo de linguagem apontada na revisão.

Como complemento, uma bateria sem texto sonda tanto o vocabulário histórico quanto os identificadores neutros. Os segundos funcionam como canários de vazamento. Nenhum desses controles elimina a necessidade de perturbação–retorno, pareamento de dificuldade, vários textos e ausência de rede/ferramentas.

A entrada pública continua reprodutível; a parte temporariamente custodiada é apenas o segredo necessário para que os identificadores novos não tenham história antes da coleta. A revelação posterior restaura a reconstrução integral.

## 6. Efeito no desenho e no poder

O isomorfo não é uma análise gratuita acrescentada depois: cada versão entra como braço/instância no pré-registro, com perturbação equivalente, mesmas oito leituras, sessões novas e parâmetros congelados. A unidade de replicação deve incluir texto/isomorfo, não apenas sessões quase idênticas do mesmo modelo.

A inclusão altera células, família de contrastes, multiplicidade, correlações e orçamento de contexto. Os números da R2 e o custo da variante 5σ não podem ser reutilizados sem recálculo do veredito completo. O poder precisa ser simulado com as regras R3, sobredispersão, efeito de texto e taxa do extrator; este documento deliberadamente não fornece `n` nem promete poder.

## 7. Artefatos e validação realizada

- `K06\CONTAMINACAO\isomorfo.py`: criação/aplicação do dicionário, transformação do gabarito e autoteste.
- `K06\CONTAMINACAO\DICIONARIO_ISOMORFO_ESQUEMA_v1.json`: esquema incompleto, deliberadamente não aplicável.
- `K06\CONTAMINACAO\medir_ponto_fixo_comum.py`: métricas finitas independentes do nome do braço.
- `K06\CONTAMINACAO\VALIDACAO_SINTETICA_ISOMORFO.json`: reversão exata, estrutura preservada e vetores positivos/negativos equivalentes; todos os testes passaram.
- `K06\CONTAMINACAO\VALIDACAO_SINTETICA_PONTO_FIXO.json`: retorno, ausência de efeito e ausência de retorno distinguidos em trajetórias artificiais; todos os testes passaram.

## 8. Bloqueios antes de ARMAR de fato

1. Completar e revisar o léxico do artigo e das 24 asserções; congelar dicionário/hash.
2. Validar o grafo de asserções e o extrator R3 nos dois léxicos, com casos adversariais e teto medido.
3. Escolher modelos/tokenizers e medir comprimento exato, dificuldade e orçamento de histórico sem truncamento silencioso.
4. Congelar número de isomorfos, perturbações, `n`, cortes, multiplicidade, sementes e poder do veredito inteiro.
5. Manter ferramentas/rede desligadas e dicionário fora do alcance do modelo; revelar somente após o congelamento do banco.
6. Submeter a R3 inteira à palavra do operador. A concordância em bloco registrada no adendo não é essa ratificação.

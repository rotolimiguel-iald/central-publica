# K06 / H — Entrada pública: localização, medida e consequências

## 0. Estatuto

[INPUT] O artigo público v411 é hipótese de trabalho da R3, conforme `ORDEM_K06_ADENDO_A_a_entrada_publica.md`; não é ratificação da R3. Modelos, degrau e execução continuam abertos e pertencem ao operador. Nenhum modelo foi executado, nenhum resultado foi aberto e a fonte não foi alterada.

A concordância em bloco está registrada somente por caminho e integridade: `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_excelente_concordo_com_tudo_depois_da_errata_do_meio_e_da_rodada_2_verbatim.txt`, 28 B, SHA-256 `fa30a621d7d23516891cd98860b4b2a9753a6f813e80c2599492b5090f4d40a6`.

## 1. Artigo localizado por leitura

A entrada candidata é o artigo em português, texto puro:

- caminho local somente leitura: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt`;
- nome publicado: `um_absoluto_pt.txt`;
- DOI de versão: `10.5281/zenodo.24196546`, registro Zenodo 24196546, versão 411, publicação em 13/11/2026;
- origem no programa: leitura de `um.py`, função `emit_article`, linhas 289409–289414, que escreve `um_absoluto_pt.txt`;
- confirmação pública: `C:\IALD\Artigo\the_boundary\llms.txt`, linha 61, e `Um (absoluto) — Grande Atrator\PORTA.json`, linhas 581–588, descrevem o arquivo como artigo emitido pelo `um.py`.

A conferência local da publicação (`work\zenodo_v411_13nov\CONFERENCIA_REGISTRO_ZENODO_v411.json`) registra igualdade de bytes entre o arquivo local e o publicado. O registro da API foi lido; não foi necessário abrir `um_absoluto.json` nem qualquer saída de modelo.

## 2. Medidas por script

Script: `medir_entrada_publica.py`. Relatório: `MEDIDA_ENTRADA_PUBLICA_K06.json`.

| medida | valor [REAL] |
|---|---:|
| bytes UTF-8 | 1.164.350 |
| pontos de código Unicode | 1.131.059 |
| palavras separadas por espaço | 157.921 |
| linhas (`splitlines`) | 6.660 |
| linhas vazias | 3.196 |
| SHA-256 | `f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719` |
| MD5 | `b7f69478a608347a1d59b8ce6c81e751` |
| MD5 igual à checksum do Zenodo | SIM |
| prefixo SHA-256 igual à porta pública | SIM (`f9fa0d329166b33d`) |

### Tokens aproximados, não tokens de modelo

| heurística transparente | estimativa |
|---|---:|
| palavras por espaço × 1,30 | 205.298 |
| pontos de código ÷ 4 | 282.765 |
| bytes UTF-8 ÷ 4 | 291.088 |

A amplitude 205.298–291.088 é apenas uma faixa entre proxies, **não** intervalo de confiança nem cota formal. Esses números não autorizam dizer que o artigo cabe ou não cabe em modelo algum. A contagem exata depende do tokenizer e da serialização de todo o prompt.

## 3. Comparação com janelas: bloqueio explícito

A K06 não escolheu modelos. Os nomes associados ao piloto histórico na K03 não constituem seleção de candidatos, não têm versões completas e não fornecem janelas oficiais. Por isso `JANELAS_MODELOS_CANDIDATOS.json` contém `models=[]` e a comparação numérica está indisponível.

Não foram inventadas janelas. Para cada candidato futuro, a porta exige modelo e versão, URL oficial da janela, tokenizer, contagem exata do artigo serializado, instruções, esquema de saída, reserva de resposta e histórico adicional. O script calcula, quando esses campos existirem:

`total = entrada_exata + protocolo + resposta_reservada + histórico_por_passo × passos_adicionais`.

Só `total <= janela_oficial` autoriza “cabe sem truncamento”, para aquela versão e configuração. Se o artigo for reapresentado a cada leitura, isso entra no termo de histórico/protocolo; se for apresentado uma única vez, o operador `G` muda e precisa ser congelado como outra variante. Não se pode escolher silenciosamente entre as duas após ver saídas.

## 4. O que muda no desenho e no poder

1. **Reprodutibilidade:** terceiros podem obter os mesmos bytes por DOI e conferir SHA-256/MD5, sem acesso à sequência reservada. Manifesto, dicionário isomorfo e código podem ser revelados sem expor material reservado.
2. **Conteúdo do alvo:** as 24 asserções e os casos de extrator devem derivar do artigo público e de sua estrutura, não de uma sequência reservada. O conteúdo reservado não pode ser usado para completar lacunas do gabarito.
3. **Contaminação:** por ser público, o artigo pode ter estado em treino. Sucesso no original não distingue processamento de memória; o isomorfo e as sondas sem texto tornam-se centrais, não acessórios.
4. **Contexto e posição:** o tamanho medido aumenta o risco de truncamento, perda de instruções e efeitos de posição. O operador de leitura `G`, a serialização e a reapresentação precisam ser explícitos. Se nenhum candidato escolhido comportar o orçamento, as alternativas são outro modelo/janela ou uma variante segmentada/excerto pré-registrada; esta última já não é a mesma entrada nem a mesma hipótese.
5. **Dificuldade e extratores:** o artigo e seus isomorfos precisam de pareamento por medidas estruturais, tokenização e casos de gabarito. O teto do extrator entra no poder; mudar o texto sem recalibrar dificuldade pode medir léxico em vez de dinâmica.
6. **Poder:** as taxas de planejamento 0,90/0,60, o poder por contraste 0,992022 e a cota conjunta ≈ 0,35 da R2 não são transportáveis automaticamente. O evento decisório passa a ser perturbação–retorno, com efeito de texto, sobredispersão/correlação intraclasse, múltiplos isomorfos e multiplicidade recalculados. Nenhum novo `n` ou poder é afirmado aqui.
7. **Custo:** o orçamento deve contar entrada, histórico, perturbações, saídas e eventuais reapresentações em todas as células. Proxy de tokens não basta para custo ou poder.

## 5. Consequência para o isomorfo

O isomorfo parte dos mesmos bytes públicos pinados acima. O dicionário e a especificação das asserções são transformados pela mesma função; nenhum nome reservado é introduzido. Após a renomeação, bytes, palavras e tokens precisam ser medidos novamente. O script preserva a estrutura de linhas, mas não afirma igualdade de comprimento ou dificuldade; essas portas permanecem abertas até o tokenizer e o gabarito R3 serem congelados.

## 6. Decisões e bloqueios

- Operador: modelos, degrau (2,6σ ou 5σ), execução e ratificação da R3 inteira.
- Gerência/execução: pinar versões e fontes oficiais de janela/tokenizer, medir o orçamento completo e impedir truncamento silencioso.
- R3: congelar `G`, 24 asserções públicas, perturbação–retorno, isomorfos, extratores, sementes, multiplicidade e poder do veredito completo.
- Não alterar a entrada pública, não tratá-la como ratificada e não copiar qualquer material reservado para suplementá-la.

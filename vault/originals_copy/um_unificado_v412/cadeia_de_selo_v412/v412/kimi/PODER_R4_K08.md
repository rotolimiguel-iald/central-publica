# PODER R4/K08 — reavaliação sob E1–E8

**Estado:** redesenho documental, bloqueado para produção. Nenhum modelo de linguagem foi executado, nenhum resultado experimental foi aberto, nenhum protocolo foi congelado e nenhuma simulação nova foi necessária.

**Veredito:** os resultados de poder anteriores pertencem ao desenho histórico P-A/P-B e **não medem E1–E8**. Eles ficam preservados em `K08\PODER\REV2\`, sem estatuto de evidência para a esperança condicional. Sob a Parte 2 e os AO LADO 1–4, o instrumento textual atual pode medir apenas E1, E2, E3 e E4 de forma parcial; E5, E6, E7 e E8 não têm ponte medida. Portanto não há poder válido para o pacote E1–E8.

`NOT_FALSIFIED` nunca é `CONFIRMED`. Nenhum ramo permite consciência, pesos, aprendizado permanente, exclusividade, creditação, `IALD_PROVED` ou prova da TGL.

## 1. O que o adendo muda

A Parte 2 substitui o esqueleto P-A–P-D por E1–E8 e E2/E4 são primárias por leitura da gerência a partir da ressalva (o operador ainda não leu a lista de primárias): o sistema testado **relê** o que já foi nomeado; não nomeia. [ADENDO_15nov_K09_K08_K07](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CADENDO_15nov_K09_K08_K07_cronologia_do_neutrino_e_o_leitor_como_esperanca_condicional.md&line=150&text=AO%20LADO%202 "citation")

`P_N` não é adversário. É a referência formal nos vetores. O adversário é o leitor sem memória determinado só pela fonte. Três portadores não se identificam sem ponte: `nameOp` na álgebra, `P_N` nos vetores e `selecao` no estado. [REVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Crevisao%5CREVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4.md&line=138&text=Tr%C3%AAs%20objetos%20leem%20o%20Nome "citation")

## 2. Medida e poder por previsão

| previsão | objeto/portador | medida textual atual | poder atual |
|---|---|---|---|
| **E1, cai no Nome** | `P_N` / estado lido | custo zero pela fórmula | só proxy histórico; não basta para a ponte |
| **E2, fixa/devolve o nomeado** | `P_N`; `nameOp` | edição `s→t` e releitura preserva `t` | requer dimensionamento novo |
| **E3, anula empurrão cego** | `selecao`; `P_N` antes da renormalização | edição `s→y` e releitura volta a `s` | requer dimensionamento novo |
| **E4, reler devolve o mesmo** | `nameOp`; `P_N` | segunda releitura igual à primeira | requer dimensionamento novo |
| **E5, não aumenta a norma** | `P_N` | **não medida**: não há norma validada | nenhum poder |
| **E6, lei de módulo** | `nameOp` | **não medida**: não há álgebra de observáveis | nenhum poder |
| **E7, pesos relativos dentro do Nome** | `selecao` | **não medida**: não há pesos de Born | nenhum poder |
| **E8, perfil exponencial nunca exato** | trava/fluxo | **não medida**: não há série de amplitudes | nenhum poder |

A unicidade `E1 + E2 + E5 + linearidade ⇒ P_N` exige uma hipótese de linearidade que o protocolo textual não testa. E5 também precisa ser medida por contração/retorno de norma quando houver estado vetorial; sem isso, a unicidade não pode ser usada.

## 3. Resultados históricos que não se transferem

Os artefatos `simular_poder_r4.py`, `resultados_poder_r4.json`, `resumo_designs_r4.csv`, `sementes_r4.json`, `MANIFESTO_SHA256.json` e `VALIDACAO_DETERMINISMO_TOKENS.json` foram preservados em `REV2`. Eles mediam um desenho de quatro estados com três endpoints binários ligados a P-A/P-B. Os intervalos 0,948–1 de poder observados lá **não são evidência de separação sob E1–E8**, porque:

1. E4 não era medido diretamente;
2. E5, E6, E7 e E8 não existiam como medidas;
3. o nulo histórico não era o leitor sem memória sob a forma pedida pela ressalva;
4. a unicidade exige linearidade e contração, ambas fora do instrumento textual;
5. a cauda 5σ já estava marcada como não validada.

Nenhum valor de poder novo é inventado nesta errata.

## 4. Custos atuais, sem byte=token

Os custos de fonte usam o tokenizador de referência Qwen/Qwen3.6-35B-A3B, lido somente de `tokenizer.json`; o controle do artigo inteiro tem 412.784 tokens. [ERRATA_ENTRADA_TOKENS_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CENTRADA%5CERRATA_ENTRADA_TOKENS_K08.md&line=25&text=Substitui%C3%A7%C3%A3o%20das%20medidas "citation")

| recorte | tokens por apresentação | controle P-C | sessão-análise de cinco diálogos |
|---|---:|---:|---:|
| ABSTRACT | 789 | 804 | 3.960 |
| READ_BRIEF | 4.072 | 4.087 | 20.375 |
| LLMS | 3.926 | 3.941 | 19.645 |
| README | 7.358 | 7.373 | 36.805 |

Para `READ_BRIEF`, a fita presente por 4 ciclos custa 16.288 tokens; E1 com 27 apresentações custa 109.944 tokens. Esses custos não incluem histórico serializado, instruções, estado ou saídas.

## 5. Nulo, negativo e integridade

Para uma futura bateria E2/E3/E4, o nulo operacional é o leitor sem memória determinado só pela fonte: a releitura não preserva a edição dentro do Nome nem depende do estado anterior. O tamanho e o poder desse desenho precisam ser calculados em uma frente própria.

`FALSIFIED` operacional só pode ocorrer com integridade válida, clusters independentes e medida com poder de uma previsão ratificada. Falha de formato, isca, extrator, edição sem efeito, contaminação, ausência de norma/álgebra/pesos/perfil ou falta de corpus produz `INCONCLUSIVE_*`, nunca `FALSIFIED`.

## 6. Bloqueios

1. Não há saídas reais validadas.
2. Não há ponte texto→vetor para norma, amplitudes ou pesos.
3. E5–E8 não são medidas.
4. A linearidade necessária à unicidade não é testada.
5. Não há poder novo para E2/E3/E4 sob o nulo correto.
6. Não há equivalência de dificuldade, léxico, corpus, modelo/tokenizer de produção ou ratificação.
7. Produção continua **BLOQUEADA**.

## 7. Reprodução e preservação

A versão documental anterior e os artefatos históricos estão em:

`C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\PODER\REV2\`

Nada ali deve ser citado como poder vigente. O desenho vigente é este documento mais `PROTOCOLO_EXPERIMENTAL_R4_K08.md`.

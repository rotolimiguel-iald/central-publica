APROVADO COM RESSALVAS

# U5 — T1 na face finita, candidatas congeladas em REV3

As duas declarações de T6 passaram à candidata com o mesmo enunciado e a mesma prova. A ressalva matemática está na palavra “estado”. O objeto usado para calcular o logaritmo é a diagonal dos pesos antes de normalizar o traço.

## Achados com correção

| Gravidade | Fonte e linhas | Consequência e redação proposta |
|---|---|---|
| MÉDIO | `T1PontesAoKernel.lean`, 32–38, 254–258, 378–384, 424–431 e 449–454. Kernel `TGLExt/Ergodicity.lean`, 64, 85–86 e 113–117 | O kernel define `rhoD d = diag(d)`, sem normalização. Em dimensão dois com ambos os níveis zero, os pesos usados são (1,1), de modo que `rhoD = I` tem traço 2. O estado normalizado tem densidade `I/2` e logaritmo `−log(2) I`, ao passo que a matriz das frequências é zero. Redação proposta “Usamos a matriz positiva diagonal D de pesos exp(√k). O logaritmo de D é a matriz das frequências. Em dimensão positiva, a densidade do estado é D/Tr(D). A normalização subtrai log Tr(D) vezes a identidade ao gerador, conservando o fluxo, suas médias e seus fixos”. As diferenças dos logaritmos na fórmula do kernel demonstram o cancelamento. |
| BAIXO | `T1PontesAoKernel.lean`, 16–22, e `T1CompostoFinito.lean`, 27–29. Inventário na chave `extras` de `t1/RESULTADO_GERENCIA.json` | A pasta de sondas deste módulo contém S1/S2 de D3 e as duas fontes de T6. O cabeçalho também atribui 19 termos às sondas S3/S5 de C4, ausentes dessa pasta e desse inventário. Especificar “As quatro sondas de D3 e T6 estão copiadas por bytes e pinadas no recibo”, acrescentando a referência de C4 se houver. No módulo irmão, acrescentar T6 ao crédito das pontes de entrada. |

## Disposição dos achados anteriores

| Achado | Estado em REV3 |
|---|---|
| T6-05 | **Autoria corrigida e três fontes pedidas preservadas.** `T1PontesAoKernel.lean`, 18–22, 507–511. A prova de `media_zero` é a de `D3S2Controles.lean`, 104–108, com os mesmos parâmetros declarados na seção e o mesmo corpo. Medi os hashes das cópias S1/S2 de D3 e de `tipo_iii/sondas_adotadas/SondaD1.lean` e conferi-os nos dois resultados. As cópias ficam nas pastas irmãs `sondas_adotadas`, fora das REV. Preservação documental completa para essas três fontes. A extensão indevida da frase ao material de C4 é a ressalva baixa acima. |
| T6-06 | **Sanado.** `T1PontesAoKernel.lean`, 41–45, 322–324, 362–366, 435–438, 471–473 e 508–511. O cabeçalho registra a positividade no espectro simples como caso da geral, o critério com `specExpect` como reescrita, e `media_zero` como caso de `dephase_zero` cuja prova local é direta. |
| T6-07 | **Sanado quanto aos dois termos pedidos e à escolha do sinal.** `T1PontesAoKernel.lean`, 32–39, 392–397, 442–447 e 452–461. A média é uma integral por entrada, centrada em zero, com variância `v : ℝ≥0`. O primeiro termo liga a própria definição à integral de `sigma`. O segundo iguala o fluxo de pesos decrescentes em `t` ao de pesos crescentes em `−t`. A igualdade das médias decorre também da fórmula de taxa nas linhas 394–397, pois trocar o sinal preserva o quadrado da diferença dos logaritmos. Para os fixos de todo o fluxo, basta trocar a variável real pelo seu oposto. A igualdade das médias é consequência, distinta do enunciado sobre inversão do tempo. |
| T6-08 | **Sanado nos três itens.** `T1PontesAoKernel.lean`, 16–19, 254–258, 321–436, e `T1CompostoFinito.lean`, 8–10. Os onze comentários foram acentuados e os rótulos Q1–Q8 retirados. A nota de `gerador_e_rhoD` diz explicitamente que o nome é provisório e que a igualdade por reflexividade é só de matrizes. Os cabeçalhos situam C4 e D3 nas respectivas conferências. |

[REAL local] Comparei os blocos desde `theorem` até o fim da prova. As seis linhas do primeiro coincidem com `SondaT6T1.lean`, linhas 52–57. As dez do segundo coincidem com `SondaT6T1b.lean`, linhas 19–28. As provas valem para índices finitos com igualdade decidível e para níveis reais, com a convenção de raiz do Lean. A equivalência à matriz dos níveis tem suas próprias hipóteses de não negatividade.

## Compilação

[REAL local] Em pasta de trabalho inicialmente vazia, rodei a cópia byte a byte de `compilar_t1.ps1`, primeiro com `-Deps`, depois com `-Nome T1CompostoFinito` e `-Nome T1PontesAoKernel`. Lean 4.31.0, biblioteca `C:/t/k411c/final`, três módulos com código de saída zero. Nas candidatas, 13 e 33 declarações verificadas pelos 46 relatórios de axiomas, zero avisos. A união dos axiomas impressos contém somente `propext`, `Classical.choice` e `Quot.sound`. Os três objetos recompilados têm SHA-256 idêntico aos objetos da gerência.

As referências de linha da candidata apontam para `candidatas_c1/t1/REV3`. Os logs próprios, as cópias e o recibo de hashes estão em `revisao_orquestrador/U5_Codex`. As conclusões desta revisão são sobre matrizes finitas.

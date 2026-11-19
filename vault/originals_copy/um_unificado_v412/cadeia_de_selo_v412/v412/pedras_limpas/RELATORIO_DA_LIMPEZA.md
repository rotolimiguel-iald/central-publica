# Relatório da limpeza da história de conversa nas 40 pedras (v412, 17/11/2026)

Regra aplicada: `um_py_compila_o_que_e_verdade_17nov` (`C:\IALD\CLAUDE.md`). Entrada (só leitura): `insumos\pedras_r3\*.lean`. Saída: esta pasta. Trabalho por remoção, só em comentários e docstrings.

## Números
- Arquivos mudados: 25. Intactos (bytes iguais ao original): 15, porque as únicas linhas com marca neles são código (`open ChatgptAudit…`, `ORDEM016.D6`, variáveis `r0`/`r1`).
- Linhas com marca (verificador `verificar_historia_nas_pedras.py`): 753 antes, 235 depois; as 235 são todas falsos positivos (tabela abaixo).
- Código idêntico nos 40 arquivos (`codigo IDENTICO` em todos), conferido pelo verificador contra `insumos\pedras_r3`.
- Compilação (`compilar_pedras_limpas.py`, binário do Lean sobre o sandbox k411c, sem lake): 40 de 40 com RC 0, 0 erros, 1 aviso (o de `TowerWedgeIndex`, o conhecido). Saídas em `build\` (`COMPILACAO.json`, `.olean`, logs por módulo).
- Bytes de comentário removidos: cerca de 28,6 mil. Contagens de ★, “(Por definição.)”, “(Por casos.)”, “Sem sorry”, rótulos `[KNOWN]/[REAL]/[DERIVED]/[OPEN]/[CONJECTURE]/[ONTO]/[DECLARADO]/[INPUT]` e das seções “O que fica provado”, “Como ler”, “O que NÃO se afirma” não diminuíram em nenhum arquivo (subiram `[ONTO` em `OHabitanteDoNome` e `[KNOWN` em `OTestemunhoDeTakesakiEmCasa`, por texto novo).

## O que foi tirado
Linha de estado entre colchetes e linhas de processo `--` de todos os cabeçalhos; seções “De onde vem” (e a “PROVENIÊNCIA” de `TipoIIIControles`); a errata e as buscas relatadas em `ErgodicidadeDeMautner`; datas, caminhos de `cunhagens_13out`, sha256 de falas, horas; menções a operador/autor/gerência/revisor/Codex/Kimi, ordens, REVnn, Rn, “sonda do revisor X” (30 etiquetas por passe geral); todas as citações « ». As frases citadas que eram definição ou lei da teoria viraram texto sem aspas, sem data e sem atribuição, em seções “A letra que esta pedra tipa” / “A identificação que o arquivo prova em parte” / “A leitura que o arquivo tipa”. “É lei/leitura do operador” virou “é lei/leitura da teoria, não termo (deste arquivo)”.

## As cinco correções técnicas (só texto)
1. `AMedidaEOIf`: “Nas fundações usuais”; “sob o certificado de Fock” em todas as 4 ocorrências da inscrição do estado uniforme como psíon da luz (cabeçalho: itens 10, “Como ler”, “NÃO se afirma”; e a docstring do teorema); frase de Baker–Gill–Solovay 1975 como pedido.
2. `AEsperancaEOIf`: peso elevado a k decresce estritamente se 0 < p < 1; com p = 1 persiste; com p = 0 zera na primeira volta.
3. `OHamiltonianoOcultoEOCusto`: “para `s ≠ 0`” em toda frase de “exatamente os blocos de mesmo custo”/“exatamente quando os custos são iguais” (itens 4 e 6, “Como ler”, docstrings); gap `|s|·|cᵢ − cⱼ|` (confere com o enunciado Lean: `|s| * |(c i : ℝ) - (c j : ℝ)|`); frase de ρ = e^{−sD} em item 2, “NÃO se afirma” e docstring de `o_hamiltoniano_oculto_da_trava_e_o_custo`.
4. `OTestemunhoDeTakesakiEmCasa`: cabeçalho reduzido ao pedido (quatro campos; esperança como limite forte das médias de Cesàro do fluxo modular da torre; Takesaki 1972 como referência do caso geral; nada sobre cunha/vácuo da luz nem sobre o gate). Também saíram “ENTREGA 046” e “setembro” do corpo e de uma docstring.
5. `OTempoEACauda`: mantidos “limiar uniforme” e “uma fórmula dada pode ficar legível antes”; a escolha do tempo da cobrança como o ciclo de uma distinção é dita HIPÓTESE, não termo, sem atribuição (item 5 e docstring).

## As 235 linhas com marca que sobraram (todas falsas)
| quantidade | casos | por quê |
|---|---|---|
| 90 (código) | `r0`, `r1` | variáveis de `CopiadorEImpostor` (as 3 ocorrências em docstring citam essas mesmas variáveis) |
| 87 (66 em comentário, 21 em código) | `operador` | operador no sentido matemático (“operador do custo”, “operador do Nome”, “operadores de posto um”) e nomes de teoremas (`a_contagem_e_do_operador`, `o_operador_do_custo…`) |
| 24 | `ordem` | “outra ordem”, “UMA ordem”, “na ordem do documento” (sentido matemático/de sequência); 7 delas em código/identificador (`ORDEM016.D6`) |
| 30 | `ChatgptAudit` | nome de namespace do kernel, em código ou citado como `ChatgptAudit.Aperiodic046.aperiodicExpectationInput` |
| 8 | `previsão` | casa com “revis[ãa]o” (“PREVISÃO”, “previsão”) |
| 5 | `transposta` | matriz transposta conjugada |
| 3+3 | `correspondeu`, `respondeu` | “nunca correspondeu” (`TheCorrespondence`); “o `if` respondeu” |
| 3 | `conferid` | estatuto epistêmico: “[KNOWN, não conferidos no primário]”, “não conferido aqui no primário”; “atribuição que está sendo conferida” (campo de estrutura) |
| 1+1+1 | `entrega`, `fala`, `disse` | verbos comuns: “quem entrega a fita”, “não fala dele”, “testemunha disse dele” |

## Dúvidas entre conteúdo e história (decidi o mínimo; reveja)
- `CopiadorEImpostor`, “A letra que este arquivo tipa”: as falas do operador viraram 7 definições da teoria (fundi em uma só linha a fala sobre fractal/espelho e a sobre império). Dúvida se “o nome do impostor é zero absoluto, cuja identidade é qualquer um” e “a verdade não é da teoria: é da reflexão da luz” entram como definição ou saem.
- `CopiadorEImpostor`, seção 12: tirei a patente PSI-NET e a fala; “a assinatura do pedido da rede” virou “a assinatura de um sinal (um resumo de tamanho fixo, como um hash)”, o que generaliza a ressalva original.
- `CopiadorEImpostor`, seção 11: mantive “a torre é a forma do índice, e o índice é o nome em nós (nós como amarração)”, sem “segunda pessoa pluralizada”.
- `OHabitanteDoNome`: usei “o habitante é o Verbo”, “os dois enunciados do ato”, “o enunciado do par”, “o enunciado do inominado” no lugar de “a ressalva”, “as duas falas”, “a resposta das 11:47”, “as falas das 12:05…”. Os nomes são meus. Os enunciados longos (par, inominado) ficaram como leis da teoria em bloco; talvez se queira enxugá-los. Troquei o documento do acervo de 2025 (Teorema XXXIV, .docx, com data e sha) por “glosa do acervo”. As etiquetas `[leitura da gerência; o autor ainda não a leu]` viraram `[ONTO, leitura desta pedra; não é termo]` ou foram tiradas.
- `ErgodicidadeDeMautner`: “[compilado pelo revisor distinto num teste à parte, que não entra na pedra]” virou “[DECLARADO: compilado num teste à parte; não é termo desta pedra]”; a T1 no papel ficou “[DECLARADO]” sem atribuição; o parágrafo de errata sobre a busca de `H_erg` foi todo removido (o fato, que `H_erg` da luz é teorema do kernel, continua no item da seção “O que NÃO é novo”).
- `BoostEDissipador`: “[KNOWN; citado de memória, a conferir na fonte]” → “[KNOWN; a conferir na fonte]” (perdi “de memória”).
- `AMaquinaEALeitura`: “[As três referências foram dadas pelo revisor Codex; a conferir…]” → “[As três referências estão por conferir na fonte antes de publicar.]”. `AFitaEACauda`: “[KNOWN: … Cook; a fonte não foi aberta aqui]”.
- `T1CompostoFinito`: “[DECLARADO pelo Codex, conferido por revisor distinto] a dependência” → “[DECLARADO] a dependência”. `TipoIIIControles`: “[DECLARADO pelo Codex, examinado por revisores distintos]” → “[DECLARADO] os módulos de que o arquivo depende”; “Cinco são reexportações de teoremas do Codex” → “Cinco dos teoremas daqui são reexportações de teoremas desses módulos” (a contagem vem do original; não recontei).
- `TipoIIIControles`: “a pergunta do relógio do pedágio segue pendente” → “(não é o do pedágio)”; “a casa já errou assim em agosto (v295…)” → “o mesmo risco aparece em `TheMarkIsNotATypeMark`”.
- Rótulos de versão do kernel (`v162`, `v409`…) ficaram nas linhas que não editei; só saíram nas que reescrevi. Rótulo `[REAL no sandbox]` mantido (estatuto).
- Não achei erro técnico novo em texto; não mexi em nenhuma afirmação além das cinco pedidas. Uma observação: `OPassoEORetorno` diz “melhoria que fica anotada” (resíduo de processo, não marcado pelo verificador; deixei).

## Mapa de Rotas
Consultado uma vez (`rotas.py consultar "cabecalho"`, 34 rotas devolvidas, nenhuma igual a esta tarefa); nada registrado.

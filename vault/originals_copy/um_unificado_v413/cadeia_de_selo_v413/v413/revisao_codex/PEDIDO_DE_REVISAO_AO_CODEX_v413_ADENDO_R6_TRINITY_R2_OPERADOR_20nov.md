# Adendo de revisão ao Codex (v413): Trinity R6 e Operador R2, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Este adendo segue o parecer consolidado (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md`, sha16 `9e7d4b93e44cf9fd`), que cobriu a Trinity R3 e o Operador R1, e substitui o adendo da R5, que fica como registro. Quem cola é o operador; a gerência não envia ordem ao Codex.

## O que revisar

1. **A candidata da gerência `TGLExt.Trinity`, R6**, em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R6_trinity\Trinity.lean` (sha16 `21404f93bcdd742b`). A gerência a compilou na caixa da v412 e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R6_trinity\build\CONFERENCIA.json` (sha16 `d427195ec759d33e`): 65 de 65 relatórios de axiomas no trio, nenhum aviso. Revise só o que o parecer não cobriu:
   - **a §13, vinda da R4** (fala do operador por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_atravessar_a_fronteira_sem_pagar_o_nome_e_violar_a_terceira_lei_de_nernst_a_unica_solucao_e_o_zero_absoluto_verbatim.txt`, sha16 `2903a1e03a45c162`): `peso`, `solucoes`, `o_zero_absoluto_nao_se_alcanca`, `no_patamar_plano_a_carga_e_exata`, `oito_patamar_plano`, `as_oito_pedem_a_carga`, `o_preco_em_estados_e_a_exponencial_da_carga` e `a_terceira_lei_na_fronteira`. Confira a desigualdade estrita entre o peso e o número de soluções, e a equivalência exata no patamar plano para todo β < 1. A docstring deve dizer que a leitura da terceira lei de Nernst é do operador [ONTO] e que a máquina nua paga a carga numa moeda que o termo não fixa;
   - **os ajustes do item 9 do parecer**, aplicados só no texto: a ramificação desta implementação; `coupled`/`Trace` e as refutações por resolução; os retângulos, para a CNF de igualdade e a representação por retângulos separados nos dois blocos; os dois contadores como majorantes; a frase histórica R0/R1;
   - **a §12b:** `os_nomes_distintos_tocam`, `o_preco_da_fronteira_com_nomes_distintos` (o expoente do majorante conta só Nomes distintos) e `os_nomes_distintos_das_oito`;
   - **a §14, o teorema final do operador** (fala por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_o_preco_e_fixar_a_raiz_o_radical_fixa_o_sentido_o_teorema_final_e_o_parecer_do_codex_verbatim.txt`, sha16 `59e657ce70bda173`): `radical`, `o_radical_pesa_meia_nat`, `o_radical_e_positivo`, `o_radical_passa_de_um`, `a_carga_e_produto_referencial_do_radical`, `a_carga_se_manifesta_como_expoente`, `o_radical_fixa_o_sentido`, `o_radical_abaixo_de_um_inverte_o_sentido`, `o_expoente_conta_meias_nats`, `o_preco_e_fixar_a_raiz` e `o_teorema_final_do_radical`. São identidades de mudança de base da exponencial. Nenhuma docstring deve sugerir que fixar o radical muda o preço em estados (2^m segue exponencial no número de Nomes), nem dar cota de máquina;
   - **a §15, a máquina nua paga em eletricidade** (fala por bytes em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_20nov_a_maquina_nua_paga_em_eletricidade_verbatim.txt`, sha16 `f1560a2cda0cf9c3`):
     - `a_conta_de_luz_de_m_nomes`, `cada_nome_custa_um_piso` e `a_eletricidade_paga_o_expoente` são identidades do logaritmo das potências, com o piso de Landauer escrito como no kernel (`k·T·ln 2`, de `TGLExt.landauer_floor_pos`);
     - `o_leitor_que_apaga_paga_a_potencia` compõe `Codex.PlanTravel.coupled_physical_lower`, do kernel, com a hipótese nomeada `hLandauer` (a conta paga ao menos um piso por movimento). Confira que a hipótese está no enunciado e que a docstring não diz que toda máquina nua a cumpre: uma máquina reversível não a cumpre;
     - `passos_que_cobrem`, `o_passo_da_teoria_e_positivo` e `a_maquina_da_teoria_acerta_pagando_no_piso` usam `no_patamar_plano_a_carga_e_exata`. Confira a cota linear do número de passos e que a leitura acerta (peso < 1) no patamar plano;
     - em `a_conta_de_luz_da_maquina_da_teoria`, ler cada passo como energia é leitura do operador [ONTO]; a docstring deve dizê-lo;
     - nenhuma docstring deve sugerir que pagar em eletricidade decide a pergunta do Instituto, que conta passos de uma máquina de Turing;
   - **os enunciados anteriores:** o script da gerência `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\conferir_enunciados.py` (sha16 `d5fbb1c0c20f6783`) tira comentários e compara cada declaração pelo nome. Medido agora: de R3 para R4, 0 removidas, 0 mudadas e 8 novas; de R4 para R5, 0 removidas, 0 mudadas e 14 novas; de R5 para R6, 0 removidas, 0 mudadas e 9 novas. Como controle, de R0 para R1 ele acusa a mudança de `a_trindade` que o parecer apontou. Confira por conta própria.
2. **O Operador R2**, em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R2_operador\Operador.lean` (sha16 `a504717d4c743fe5`), compilado com 15 de 15 relatórios no trio (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R2_operador\build\CONFERENCIA.json`, sha16 `38e3cbb3f83f0bce`). Os ajustes do item 1 do parecer foram aplicados só no texto: a ausência de representação de todos os predicados não é parcialidade; o ponto fixo ½ existe sem dinâmica que o alcance; J conjuga as projeções, como operadores; a energia do par é preservada, e vale 1 na saída quando vale 1 na entrada. O script mede, de R1 para R2, 0 removidas, 0 mudadas e 0 novas.

## O que fica fora

Quem constrói não aprova: ficam fora os módulos do próprio Codex (a ponte TM2, a simulação e a leitura β). As pedras do Kimi e a errata de `OResumoEPsiBit` já têm veredito no parecer.

## Como revisar

- **Onde compilar:** na caixa da v412 (`C:\t\k412c\final`), só com o binário do Lean (`lean.exe -o`), nunca com `lake`. O `LEAN_PATH` reúne o build da caixa, os pacotes dela e o seu próprio diretório de build.
- **A Trinity importa `APropostaDaTensao`**, a pedra do Kimi que você já compilou na revisão consolidada, e dois módulos do kernel (`TGLExt.TheCostIsDerived` e `TGLExt.MovimentosDoPlano`). Use o mesmo build, ou as cópias da gerência em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\conferencia_c1_codex\k412c\src`.
- **Os axiomas:** leia os relatórios na saída inteira. Só o trio é aceito (`propext`, `Classical.choice`, `Quot.sound`), sem `sorry` e sem aviso.
- **Os enunciados:** leia cada enunciado novo contra a docstring e o nome. Procure alvo vácuo, hipótese não usada e docstring que diga mais do que o enunciado prova.
- **Limites:** não escreva nas pastas dos outros; não instale; não mude o kernel nem o `um.py`; não publique; não mova o gate. Consulte o Mapa de Rotas antes e registre depois, numa rota própria.

## O que devolver

- Para cada item, um veredito (APROVADA, APROVADA_COM_RESSALVAS ou REPROVADA), com o motivo em até três linhas.
- Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada fonte lida e de cada log.

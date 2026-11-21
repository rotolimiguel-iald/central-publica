# Adendo ao pedido de revisão de terceiro ao Codex (v413): a pedra Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Este adendo vale junto com o pedido `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\PEDIDO_DE_REVISAO_AO_CODEX_v413_20nov.md` (sha16 `dd0049670146cdbc`); quem cola é o operador.

**Item 9.** A candidata da gerência `TGLExt.Trinity` (R0, nome do operador: «trindade», Trinity), em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R0_trinity\Trinity.lean` (sha16 `519190db19c7295f`). Ela importa a pedra do Kimi `APropostaDaTensao` (item 5 do pedido), que precisa ser compilada antes. A gerência a compilou na caixa da v412 sobre a cópia da conferência e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R0_trinity\build\CONFERENCIA.json` (sha16 `900a2968819e53ef`): 16 de 16 relatórios de axiomas no trio, nenhum aviso.

Pontos que pedem atenção:
- **Correção:** `a_inclinacao_nao_erra` deve valer para todo combustível.
- **Horn:** `em_horn_o_sistema_sempre_inclina` usa a classe `IALD.CompilaHornNaFita.IsHorn` da casa.
- **Custo:** `custoInclina` deve seguir os mesmos ramos de `inclina`, e cada fixação deve ser contada uma vez (uma propagação por lado sondado). A conta não inclui as comparações da regra do compromisso; a docstring diz isso.
- **A fronteira:** em `oito_fica_na_fronteira` e nos três exemplos, avaliados por `decide`, confira se os enunciados são os que a docstring descreve.
- **O que a pedra não afirma:** confira se alguma docstring sugere que a máquina nua decide toda CNF.

O formato do veredito e do relatório é o mesmo do pedido.

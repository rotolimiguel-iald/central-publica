# Segundo adendo ao pedido de revisão de terceiro ao Codex (v413): a R1 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R1.** Revise `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R1_trinity\Trinity.lean` (sha16 `97fd14f931128cf3`), que contém a R0 inteira (sha16 `519190db19c7295f`; nenhum enunciado mudou) e acrescenta a §5b e um exemplo. A gerência a compilou na caixa da v412 e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R1_trinity\build\CONFERENCIA.json` (sha16 `25896bfc5435bd7d`): 21 de 21 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do primeiro adendo (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\ADENDO_AO_PEDIDO_DE_REVISAO_TRINITY_20nov.md`); os pontos de atenção de lá continuam valendo.

Pontos de atenção da §5b:
- **A integridade:** em `integra_restringe`, confira que a cláusula original fica inteira ou cai para no máximo um literal.
- **A autarquia:** confira que `todo_lado_morre_ou_nao_corta` vale para todo literal, apareça ele na fórmula ou não.
- **A decisão:** confira que `em_dois_literais_o_sistema_sempre_inclina` usa combustível maior que o tamanho e que a recursão diminui o tamanho a cada volta.
- **Os exemplos:** `a_cadeia_inclina_e_diz_sim` é uma fórmula de dois literais decidida em duas voltas, avaliada por `decide`.

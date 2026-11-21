# Terceiro adendo ao pedido de revisão de terceiro ao Codex (v413): a R2 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R2.** Revise `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R2_trinity\Trinity.lean` (sha16 `97e78d6417e84091`), que contém a R1 inteira (sha16 `97fd14f931128cf3`; nenhum enunciado mudou) e acrescenta as §9 a §11. A gerência a compilou na caixa da v412 e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R2_trinity\build\CONFERENCIA.json` (sha16 `7962c359b1350620`): 30 de 30 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do segundo adendo (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\ADENDO_2_AO_PEDIDO_DE_REVISAO_TRINITY_R1_20nov.md`); os pontos de atenção dos dois adendos anteriores continuam valendo.

Pontos de atenção das §9 a §11:
- **A fronteira:** confira que `NaFronteira` descreve exatamente onde `inclina` devolve `.indeciso` e que `a_inclinacao_para_so_na_fronteira` não depende de combustível insuficiente.
- **O terceiro literal:** em `na_fronteira_todo_lado_corta_uma_de_tres`, confira o invariante `Dentro` (toda cláusula do lado é sublista de uma original) e a conclusão: uma cláusula de dois literais ou mais, cortada de uma original de três ou mais.
- **A travessia:** confira que `atravessa` só ramifica onde a inclinação para, que `a_travessia_decide` vale para toda fórmula com combustível maior que o tamanho, e que `o_preco_da_travessia` é cota exponencial no combustível (2^k·B − B fixações), não polinomial.
- **A docstring:** confira que ela não sugere travessia de preço polinomial.

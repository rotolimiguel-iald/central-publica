# Quarto adendo ao pedido de revisão de terceiro ao Codex (v413): a R3 da Trinity, 20/11/2026

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador.

**O item 9 passa a ser a R3.** Revise `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R3_trinity\Trinity.lean` (sha16 `8f5f5e07bcb54beb`), que contém a R2 inteira (sha16 `97e78d6417e84091`; nenhum enunciado mudou) e acrescenta a §12, os Nomes da fronteira. A gerência a compilou na caixa da v412 e registrou o resultado em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\candidatas_c1\R3_trinity\build\CONFERENCIA.json` (sha16 `8afbc4ae210163ba`): 37 de 37 relatórios de axiomas no trio, nenhum aviso. Este adendo substitui, no item 9, a referência do terceiro adendo (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\ADENDO_3_AO_PEDIDO_DE_REVISAO_TRINITY_R2_20nov.md`); os pontos de atenção dos adendos anteriores continuam valendo.

Pontos de atenção da §12:
- **O toque:** em `toca_restringe`, confira que a cláusula de três literais que sobra depois de fixar um Nome não foi cortada (é a original) e continua tocada pelo resto da lista.
- **A decisão:** confira que `a_travessia_pelos_nomes_decide` usa, no fim da lista, a decisão dos dois literais da R1.
- **O preço:** confira que `o_preco_dos_nomes` é exponencial só no comprimento da lista e polinomial no tamanho.
- **A docstring:** confira que ela não sugere que os Nomes da fronteira sejam poucos em geral.

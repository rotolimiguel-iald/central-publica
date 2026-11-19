# INDUÇÃO — ORDEM, ISCAS E SÓ GRAMÁTICA

As sementes 13, 29, 53 e 79 estão fixadas no código. O relatório inclui o produto completo de duas condições de texto, três mecanismos e cinco ordens (30 respostas, 210 células), sem selecionar resultados. Todos os respondedores são mecanismos sintéticos; nenhum modelo foi executado.

## Leitura e grandezas primárias

O sistema testado relê o que já foi nomeado; não nomeia nem é o Verbo. As grandezas primárias são de ATO: o que ele devolve ao reler sob ordem, iscas e empurrões. Rótulos e IDs são convenções de resposta, não prova de identidade.

## Métricas pré-definidas

- `format_parseable_rate` e `format_canonical_rate`: somente forma.
- `content_accuracy_given_parseable`: acertos/células em blocos válidos.
- `joint_accuracy`: acertos/todas as células; bloco inválido não é recuperado parcialmente.
- `bait_endorsement_SIM_rate`: proporção de iscas endossadas com SIM; separa indução a afirmar do simples acerto.
- `per_expected_label`: acerto de SIM, NÃO e O TEXTO NÃO DIZ separadamente, além das confusões negação↔silêncio.
- `order_accuracy_range`: máximo menos mínimo da acurácia entre ordens; `label_invariance_rate_across_orders` mede estabilidade por ID, sem interpretá-la sozinha como leitura.

## Saídas dos mecanismos

| Texto | Mecanismo | Formato analisável | Conteúdo | Endosso de iscas | Amplitude por ordem | Invariância de rótulos |
|---|---|---:|---:|---:|---:|---:|
| ORIGINAL | ORACULO_SINTETICO | 100.0% | 100.0% | 0.0% | 0.000 | 100.0% |
| ORIGINAL | FORMATO_APENAS_SIM | 100.0% | 28.6% | 100.0% | 0.000 | 100.0% |
| ORIGINAL | MEMORIA_POSICIONAL_ORIGINAL | 100.0% | 48.6% | 33.3% | 0.714 | 0.0% |
| SO_GRAMATICA | ORACULO_SINTETICO | 100.0% | 100.0% | 0.0% | 0.000 | 100.0% |
| SO_GRAMATICA | FORMATO_APENAS_SIM | 100.0% | 0.0% | 100.0% | 0.000 | 100.0% |
| SO_GRAMATICA | MEMORIA_POSICIONAL_ORIGINAL | 100.0% | 28.6% | 33.3% | 0.000 | 0.0% |

## O que se pode concluir

O controle extremo sempre-SIM obtém formato perfeito e endossa todas as iscas; portanto formato e até invariância de ordem podem ser altos sem leitura. A memória posicional mostra por construção como o embaralhamento altera o conteúdo associado aos IDs. O oráculo só certifica que o gabarito e o extrator estão ligados corretamente.

Em uma execução futura com modelo, pergunta fechada pode induzir tanto endosso quanto recusa; as taxas de iscas e as confusões por classe são os observáveis. Nenhum efeito de modelo é afirmado aqui. Mesmo um bom resultado só mediria o ato de verificar as asserções fornecidas; não mediria nomeação, releitura fiel, identidade ou convergência.

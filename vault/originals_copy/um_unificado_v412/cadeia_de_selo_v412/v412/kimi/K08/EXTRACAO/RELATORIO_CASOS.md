# RELATÓRIO DE CASOS — ESCOLHA FECHADA K08/R4

Validação de software sobre casos sintéticos da EXTRACAO. Nenhum modelo foi executado; nenhum resultado real foi aberto. A ENTRADA separada usa recortes públicos com linha e hash; nada reservado entra aqui.
O sistema testado relê o que já foi nomeado; não nomeia nem é o Verbo. As grandezas primárias são de ATO, não de rótulo.
Sucesso de formato é medida de formato, não de releitura fiel nem de convergência.

## Contrato observado

- Casos: 15; falhas do contrato esperado: 0 (nenhuma).
- Blocos analisáveis: 8/15 (53.3%); canônicos: 6/15 (40.0%).
- Conteúdo entre blocos analisáveis: 25/27 (92.6%).
- Medida conjunta, com bloco inválido sem recuperação parcial: 25/55 (45.5%).
- Formato válido com conteúdo errado: C14.

| Caso | Categoria | Formato | Canônico | Acertos | Erros | Contrato |
|---|---|---:|---:|---:|---|---:|
| C01 | correto | True | True | 4/4 | — | True |
| C02 | cita_sem_relacionar | True | True | 2/2 | — | True |
| C03 | negacao | True | True | 3/3 | — | True |
| C04 | truncado | False | False | 0/4 | MARCADORES_AUSENTES | True |
| C05 | ingles | False | False | 0/4 | REGISTRO_OU_ROTULO_INVALIDO, ID_AUSENTE | True |
| C06 | vazio | False | False | 0/4 | VAZIO | True |
| C07 | outros_nomes | True | True | 3/3 | — | True |
| C08 | prosa_com_preambulo | True | False | 4/4 | — | True |
| C09 | adversarial_bloco_duplo | False | False | 0/4 | BLOCOS_MULTIPLOS | True |
| C10 | adversarial_id_duplicado | False | False | 0/4 | ID_DUPLICADO | True |
| C11 | adversarial_registro_fora_do_bloco | False | False | 0/4 | MARCADORES_AUSENTES | True |
| C12 | ordem_diferente | True | False | 4/4 | — | True |
| C13 | id_desconhecido | False | False | 0/4 | ID_DESCONHECIDO, ID_AUSENTE | True |
| C14 | conteudo_errado_formato_valido | True | True | 2/4 | — | True |
| C15 | contradicao_explicita | True | True | 3/3 | — | True |

## Leitura das taxas

O caso C14 mostra que um bloco perfeito pode ter conteúdo errado. C08 e C12 mostram que preâmbulo externo e ordem diversa não zeram mais o conteúdo; ambos deixam de ser canônicos e ficam marcados como diagnóstico de forma. C04–C06 e C09–C11/C13 são falhas de contrato, não erros semânticos. C15 mostra que P e ¬P podem ser afirmados pelo mesmo texto sem criar um quarto rótulo.

As taxas acima verificam a fiação e os contraexemplos escritos. Não autorizam execução com modelos e não medem releitura fiel, retorno ou convergência.

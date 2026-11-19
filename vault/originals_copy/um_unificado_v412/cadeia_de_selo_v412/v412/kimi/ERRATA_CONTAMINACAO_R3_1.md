# ERRATA CONTAMINAÇÃO R3.1 — horizonte `V2-RET` em 12 interações

14/11/2026. Correção AO LADO da seção G/K06 e de seus autotestes, depois da revisão da gerência. A versão anterior não é apagada nem reescrita: está integralmente preservada em `K06\CONTAMINACAO\REV0\`.

## 1. Achado corrigido

O anexo e o validador de ponto fixo apresentavam o esquema **legado `p=4,r=6`**, com oito estados. A R3 vigente usa **12 interações** e `V2-RET` com **`p=8,r=10`**. A discrepância era de índice/horizonte no anexo, não uma mudança nova do protocolo R3.

Fonte de alinhamento lida: `PROTOCOLO_EXPERIMENTAL_R3_K06.md`, §§6.2–6.3. Nenhum resultado de modelo foi aberto.

## 2. Regra agora implementada

O validador exige exatamente os estados `1…12` e calcula:

- perturbação aplicada **depois de `k=8`**;
- alteração observável em **`k=9`**: `d_9>0`;
- retorno estabilizado em **`k=10–12`**: `d_10=d_11=d_12=0` e `u_11=u_12=0`;
- pré-condição `d_8=0` e predicado completo `V2-RET`, `p=8,r=10`.

As classes permanecem separadas:

- `PERTURBATION_NOT_APPLICABLE`: `d_8≠0`;
- `PERTURBATION_NO_EFFECT`: `d_9=0`;
- `PERTURBATION_NO_RETURN`: alteração sem retorno estabilizado em `r=10`;
- `FINITE_HORIZON_RETURN_OBSERVED`: predicado completo, sem prova de limite infinito, bacia universal ou ponto fixo matemático de LLM.

`A8` continua disponível somente como **compatibilidade legada explícita**, nas leituras 1–8, e não substitui `V2-RET`. O validador rejeita trajetórias com apenas oito estados. O caso de oito estados presente no autoteste atual serve exclusivamente para verificar essa rejeição.

O esquema `p=4,r=6` aparece apenas como referência histórica rotulada e nos arquivos de `REV0`; não permanece como regra ativa, campo de saída ou exemplo positivo.

## 3. Arquivos corrigidos e hashes

Hashes SHA-256 lidos por script depois das cópias de `REV0` e das validações.

| arquivo | REV0 SHA-256 | R3.1 SHA-256 |
|---|---|---|
| `CONTAMINACAO_ISOMORFO_K06.md` | `db2f7b03cd40aed2005c729560e0672a2bd01ebba1f527ad0664f2a20a414532` | `d0962065af8ef516da0486d836c46a7cdccf631db0ed2a9abf51aaffec9c098d` |
| `K06\CONTAMINACAO\medir_ponto_fixo_comum.py` | `08c83a44b70ba3d52fb1ff10fef8bc0eef84c3abaf509b8f4cd6769c7fb95a7c` | `70714e5d2a90b4687f906c06833cfab9f34b9171d259710ee138b5e78d5edb78` |
| `K06\CONTAMINACAO\NOTA_EXECUCAO_CONTROLE.md` | `6c8b518d26550b2262f268c54c098b672b20870a9e4daa70fdea598e9ac94450` | `3cb06ca0ccd55dd43d6d9b96345d6f6704585d2dadbfcb42e3e4a609c6361156` |
| `K06\CONTAMINACAO\VALIDACAO_SINTETICA_PONTO_FIXO.json` | `18c34aea14ae3201ae8953adfe12ae1fe7a3df5685b9936075f3477ec6d47407` | `b8626a49bebd859f01103d24972339ec698f999ed9ba44bdcfc668acab6d1b62` |

## 4. Arquivos preservados sem mudança de bytes

| arquivo | SHA-256 em REV0 e na versão atual |
|---|---|
| `K06\CONTAMINACAO\isomorfo.py` | `8d27efc1689002f31bfc6a49dc25e1f3403adc3e055b594a3e3ca2a15b598401` |
| `K06\CONTAMINACAO\DICIONARIO_ISOMORFO_ESQUEMA_v1.json` | `c4783c5794895c2881e87fad2818a008390ef322b144114f8e465ac84230b2b3` |
| `K06\CONTAMINACAO\VALIDACAO_SINTETICA_ISOMORFO.json` | `d0d3fd537b34cfdda1ad12b32929d9ab18e048f5ade4b26d08d3d0251b991a82` |

O esquema de dicionário continua **incompleto e não aplicável**. Não houve preenchimento de léxico, transformação do artigo público ou alteração da entrada.

## 5. Aliases

Nenhum alias de hipótese `H-*` foi encontrado no anexo de contaminação ou nos dois scripts; não houve alias formal a renomear neste escopo. Os rótulos operacionais foram alinhados à R3: `V2-ISO-A`, `V2-ISO-B` e `V2-RET` como fase decisória de todos os braços.

## 6. Validações executadas — somente sintéticas

[REAL] Foram executados somente os autotestes embutidos, sem modelo e sem artigo público:

1. `isomorfo.py self-test`: **6/6 checagens**, `all_pass=true`; reversão exata, estrutura preservada e vetores equivalentes. Como o código e os dados sintéticos não mudaram, o hash do relatório permaneceu igual.
2. `medir_ponto_fixo_comum.py --self-test`: **10/10 checagens**, `all_pass=true`, esquema `k06.contaminacao.autoteste-ponto-fixo.v2-r3-1`.

Os cinco casos atuais de trajetória cobrem: retorno correto em `r=10`; ausência de efeito; ausência de retorno; perturbação inaplicável; retorno tardio/não estabilizado. Uma checagem adicional rejeita explicitamente o horizonte anterior. Todos os relatórios mantêm `model_executed=false`, `public_article_transformed=false` e ausência de veredito global.

## 7. Escopo preservado e bloqueios

- Nenhum modelo foi executado; nenhum resultado foi aberto; nenhuma corrida científica foi realizada.
- O artigo público não foi transformado nem editado.
- O T6, o `REGISTRO_MAPA`, o protocolo R3, o poder, os modelos e os vereditos não foram alterados por esta errata.
- Permanecem os bloqueios: completar/revisar o léxico; validar os extratores R3; congelar dicionários e perturbações; medir janela/tokenização para 12 interações; ratificar a R3 inteira antes de qualquer execução.
- Esta errata corrige o instrumento de validação e sua documentação; não ratifica o desenho nem antecipa resultado.

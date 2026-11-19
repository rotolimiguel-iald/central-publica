# ERRATA AO LADO — m₂, K09, adendo de 15/11

15/11/2026. Esta errata aplica a Parte 1 de `ADENDO_15nov_K09_K08_K07...md` e a `revisao/LEITURA_K09_PARCIAL_NEUTRINO_15nov.md`. O estado K09 anterior está preservado em `K04/M2/REV3/`; REV2/R3 permanecem preservados. Nenhum teste foi executado, nenhum vetor de dados foi aberto e nada foi instalado.

## 1. Correção central da cronologia

A formulação anterior media a cegueira só pelo pino da regra. Agora todos os textos carregam os dois eixos:

- **previsão publicada:** a tese do neutrino é de 2025 (16/10, DOI 10.5281/zenodo.17372599; 04/11, DOI 10.5281/zenodo.17526619), sem o valor 8,51; o valor aparece nos bytes do acervo em 22/01/2026 e na publicação Zenodo em 17/02/2026 (`created` 20/02/2026);
- **número JUNO 207,2 dias:** é posterior à previsão publicada e anterior ao pino da função de veredito de 08/08/2026.

Portanto, nenhuma superfície diz que o autor viu o dado antes. JUNO 59,1 dias é anterior ao valor público: retrodição sem ajuste/use-novelty, não prospectiva do valor. O incremento posterior a 18/05/2026 é o único dado posterior aos dois marcos.

## 2. As dez passagens corrigidas

| # | Arquivo | Correção aplicada |
|---|---|---|
| 1 | `ERRATA_M2_K09.md` | seção 1 passou a nomear os dois eixos no título e no corpo. |
| 2 | `ERRATA_M2_K09.md` | a apresentação anterior ao pino ganhou as datas da previsão publicada ao lado. |
| 3 | `ERRATA_M2_K09.md` | a consequência agora diz: regra posterior ao número; previsão anterior ao número; só dado depois de 18/05 é posterior aos dois. |
| 4 | `M2_DESFECHOS...K04.md` | conclusão 4 reescrita com as datas da tese 2025, do valor 22/01/2026, da publicação 17/02/2026, do número e do pino. |
| 5 | `M2_DESFECHOS...K04.md` | conclusão 7 diz “desenho em que previsão, regra e selo precedem o dado”, sem “realmente”. |
| 6 | `M2_DESFECHOS...K04.md` | seção de cronologia passou a “previsão publicada, número e pino da regra”. |
| 7 | `M2_DESFECHOS...K04.md` | a tabela ganhou 16/10/2025, 04/11/2025, 18/11/2025, 22/01/2026, 17/02/2026, 15/07/2026, 22/07/2026, 08/08/2026 e 29/09/2026. |
| 8 | `M2_DESFECHOS...K04.md` | 15/07 continua como confirmação explícita; 22/06 ficou `[DECLARADO]` por falta de resposta crua guardada. |
| 9 | `M2_DESFECHOS...K04.md` | a consequência final usa os dois eixos e não chama 207,2 dias de leitura cega ou prospectiva isolada. |
| 10 | `PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md` | o motivo usa os dois eixos e diz que o incremento é o único dado posterior à previsão publicada e ao pino. |

## 3. JSON corrigido

`ERRATA_NEUTRINO_V412_DADOS_K09.json` foi regenerado com:

- `previsao_publicada`: tese 2025 sem o valor; valor no acervo em 22/01/2026; publicação 17/02/2026 e `created` 20/02/2026;
- posição relativa por degrau: 59,1 dias antes do valor público; 207,2 dias depois do valor público e antes do pino;
- `frozen_hash_objeto_congelado` = `4bdae22a…4075c`;
- sha256 do `.py` = `2564d7c9…71f0`;
- sha256 do `.resultado.json` = `6f0963a5…239b`;
- dicionário portado = `e24877…19c3`.

O nome antigo `sha256_regra_original` foi removido para não induzir leitura de hash de arquivo.

## 4. Datas por métrica

O documento principal agora dá Δm² e m₂ lado a lado:

| Alvo | Δm² cumulativo | m₂ cumulativo | Δm² incremento | m₂ incremento |
|---|---|---|---|---|
| 5σ | 16/08/2029 | 01/08/2029 | 11/03/2030 | 25/02/2030 |
| D90 | 31/10/2031 | 08/10/2031 | 25/05/2032 | 02/05/2032 |
| r=3 | 08/03/2027 | 03/03/2027 | 01/10/2027 | 26/09/2027 |

O piso de dois pontos `s0=0,052587652` torna 5σ e D90 inalcançáveis; duty cycle permanece só cenário no arquivo de medidas.

## 5. Modelo MATCHED e regra de morte

- A tabela MATCHED agora declara o modelo usado: `X_P ~ N(7,388,0,078²)`, `X_S ~ N(centro_S,σ_S²)`, `C_PS=0`; não é o modelo (a1).
- O pré-registro não escolhe A/B. A constatação de que o código selado descreve A é separada de qualquer decisão prospectiva.
- A ratificação da classe “preliminar” tem uma autoridade: o operador, com proposta técnica preparada pela gerência, antes do selo.
- O significado do negativo é apresentado como leitura técnica a ser levada ao operador, sem decidir a regra.

## 6. Validação e bloqueios

Scripts, JSON, tabelas, hashes e referências foram revalidados e os manifests refeitos. Nenhum teste observado foi executado.

Bloqueios que permanecem:

1. resposta crua de 22/06/2026 não guardada — fica `[DECLARADO]`;
2. data exata da primeira disponibilização pública da tabela NuFIT — `null`/OPEN;
3. covariância inter-liberações e P–S;
4. independência física e persistência da anomalia SK-Gd;
5. decomposição estatística/sistemática futura e piso real;
6. escolha de regra, fonte, escada e custódia antes do selo.

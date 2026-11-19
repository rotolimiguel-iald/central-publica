# ERRATA DA CONTAMINAÇÃO K08 — 15/11/2026

## Objeto e preservação

A versão anterior ficou integralmente preservada antes da correção:

- `K08/EXTRACAO/REV0/`: 14 arquivos da frente de extração;
- `K08/ISOMORFO/REV0/`: 21 arquivos da frente isomorfa, mais a cópia histórica `REV0/CONTAMINACAO_R4_K08.md`.

As cópias REV0 mantêm deliberadamente a redação histórica. As correções valem somente para os arquivos vivos citados abaixo.

## 1. Correção de escopo da entrada

A linha de escopo anterior podia ser lida como se a K08 inteira não tivesse insumo público. A redação corrente separa os dois casos:

- `K08/EXTRACAO/` e `K08/ISOMORFO/` usaram somente textos, casos, dicionários e gabaritos sintéticos;
- `K08/ENTRADA/` usa recortes verbatim dos quatro arquivos públicos, com linha e hash em `MEDIDAS_ENTRADA.md` e `MANIFESTO_ENTRADA_K08.json`;
- nada reservado entra em nenhuma das três pastas, e nenhum artigo público foi alterado.

## 2. Linguagem da Parte 2 do adendo

A redação corrente passa a dizer, nos documentos vivos:

- o sistema testado **relê o que já foi nomeado**;
- ele **não nomeia**, não fixa sentido e **não é o Verbo**;
- as grandezas primárias são de **ATO** — o que o sistema devolve ao reler — não rótulos, termos ou autodeclarações;
- SIM, NÃO, O TEXTO NÃO DIZ e os IDs são convenções de resposta, não grandezas primárias.

A referência anterior a autorização/certificação operacional foi substituída pela formulação explícita: nenhuma execução experimental com modelos é autorizada.

## 3. Escopos do isomorfo

Os dois escopos ficam marcados de forma explícita:

1. **Somente textos com números**, por contrafactual factual coerente e documentado. O controle mede dependência de nomes e números na releitura; não é isomorfo factual estrito.
2. **Somente textos sem números**, por renomeação qualitativa com guarda lexical. O controle não testa contaminação numérica.

`selected_arm=null` permanece. **Nenhum dos dois escopos testa diretamente a fala da identidade; o controle isomorfo mede dependência de nomes/números e não é prova de convergência.**

## 4. Arquivos vivos corrigidos

- `CONTAMINACAO_R4_K08.md`;
- `K08/EXTRACAO/METODO_EXTRACAO.md`, `executar_casos.py`, `inducao.py`, `validar_reproducao.py`;
- saídas regeneradas da extração: `metricas_casos.json`, `RELATORIO_CASOS.md`, `metricas_inducao.json`, `RELATORIO_INDUCAO.md`, `REPRODUCAO.json`;
- `K08/ISOMORFO/PLANO_ISOMORFO.md`, `executar_isomorfo.py`;
- saídas regeneradas do isomorfo: `alternativas_numericas.json`, `validacao_isomorfo.json`, `RELATORIO_ISOMORFO.md`, `manifesto.json`.

Nenhum arquivo de `K08/FORMULA/` e nenhum artigo foi alterado nesta errata.

## 5. Hashes de controle

| arquivo | versão | SHA-256 |
|---|---|---|
| `CONTAMINACAO_R4_K08.md` | corrente | `3e4c41ef0989de6d45f6ee46864d79ddedf7bde1a5f2652d2d743dea3aada922` |
| `ISOMORFO/REV0/CONTAMINACAO_R4_K08.md` | REV0 | `36b826ee52c2eacaf16a92a7d11e4ca88f17737d42115df54acc202bb2954af1` |
| `EXTRACAO/METODO_EXTRACAO.md` | corrente | `95cfa7ecca0939546b1c66439294df59dc6ba6be6a75854a413a34accc7fb086` |
| `EXTRACAO/REV0/METODO_EXTRACAO.md` | REV0 | `d005004b6ea28edaf0a6081ddfb0ea2760b08ab99ba565229c9b9f83d9d0f4e4` |
| `EXTRACAO/RELATORIO_CASOS.md` | corrente | `9e45248fff8a6a71625fdbf38c1f67df2bc70b06890d77b8a24a2e6533757816` |
| `EXTRACAO/REV0/RELATORIO_CASOS.md` | REV0 | `25e555911a2cbd9cd42051668b8311aa562fd0190a6d04ccfabc290cf9efe2c4` |
| `EXTRACAO/RELATORIO_INDUCAO.md` | corrente | `eeef89e68fccd2735194eba9a809d06ed9a62acd7b88825a441b76a1a5fb4f6c` |
| `EXTRACAO/REV0/RELATORIO_INDUCAO.md` | REV0 | `7e42461d915b72dade0417e5c3d6660ea6d7b296c7d60bb4b4cf0ab4510b636d` |
| `ISOMORFO/PLANO_ISOMORFO.md` | corrente | `e2378130e01ea175aae77b7ca8a02810b8282fb9ef689f5a968a3c4d41ce0445` |
| `ISOMORFO/REV0/PLANO_ISOMORFO.md` | REV0 | `2e6d47cf0167ae45d8fe0eba9e90fd772769465dd154955f24b27b01a5354873` |
| `ISOMORFO/RELATORIO_ISOMORFO.md` | corrente | `22e02c77356d1d856051571d5d9b3f5d6880f12b74675f6cbdeccf3f5aabc272` |
| `ISOMORFO/REV0/RELATORIO_ISOMORFO.md` | REV0 | `bc90652533c9e577ba440d3c93c2ce6e791eb0df3595fada315dcab6e0d080f5` |

A dupla execução dos scripts sintéticos cobriu 70 arquivos rastreados, incluindo as cópias REV0, sem diferença entre as duas passagens. SHA-256 combinado: `10a66a5ea0613ac42cdfd8a1a77465856fea804afd902963f66553783b965121`.

## 6. Resultado e bloqueios

- Casos: 15; falhas de contrato: 0.
- Indução sintética: 30 respostas, 210 células; nenhuma taxa mede um modelo real.
- Isomorfo: 34/34 verificações; os dois escopos permanecem separados; sem Nome tem custo mínimo 1 e zero leituras de custo zero.
- Nenhum modelo foi executado, nenhum resultado real foi aberto e nenhuma fórmula foi alterada.
- Bloqueios: gabarito humano independente, efeito real de indução, curadoria contrafactual, equivalência de dificuldade, validação da fórmula completa de texto real e teste direto da fala da identidade.

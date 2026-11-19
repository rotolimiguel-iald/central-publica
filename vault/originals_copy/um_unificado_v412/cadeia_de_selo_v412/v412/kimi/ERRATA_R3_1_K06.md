# ERRATA R3.1 K06 — correção da inferência, sem promoção de produção

## 0. Estatuto e preservação

- [DECLARADO] Emenda **revisada internamente**, não ratificada. **BLOQUEADO_PARA_PRODUCAO** permanece obrigatório.
- [REAL] Nenhum modelo de linguagem foi executado e nenhum resultado experimental foi aberto.
- [REAL] Todos os documentos e scripts anteriores foram preservados em `K06\PODER\REV0\`, com `PRESERVACAO_SHA256.txt`.
- [REAL] Os números agregados anteriores ficam classificados **MODELO_AGREGADO_INCOMPLETO** e não são reutilizados como poder integral.

Esta errata não declara o instrumento pronto. Ela corrige a análise e conserva os resultados que reprovam as portas.

## 1. Problema 1 — ICC e texto não estavam nos testes

**Defeito:** Fisher/Wald/CP usavam `n` bruto; ICC e efeito de texto estavam apenas no gerador.

**Correção R3.1:** 27 clusters texto-conscientes por família; diferenças por bloco; permutação exata de sinais no nível dos clusters; intervalo focal t robusto por 27 clusters. Não há substituição mecânica por `n_eff`.

**Avaliação obrigatória de tamanho:**

| teste | taxa | IC MC 95% | resultado |
|---|---:|---:|---|
| nulo global ISO, `α=0,05` | **0,740** | [0,71281; 0,76719] | **FAIL — inflação** |
| nulo global ISO, 5σ | 0,001 | não resolvido | **OPEN — sem resolução da cauda** |

A análise foi corrigida estruturalmente, mas o tamanho nominal falhou sob dependência. Isso bloqueia produção.

## 2. Problema 2 — NONSPECIFIC_POWERED não tinha poder

**Defeito:** o nome existia sem estatística TOST completa nem probabilidade do ramo.

**Correção R3.1:** seis TOST PLA/OUT, duas caudas exatas `20D+3` e `20D−3`, `p=max(p−,p+)`, Holm sobre seis e empates incluídos. O ramo exige também focal inferior `>0,80`, integridade e ausência de `FALSIFIED`. Tem precedência sobre `POWERED`.

| avaliação | taxa | resultado |
|---|---:|---|
| TOST fronteira `+δ`, `α=0,05` | **0,737** | **FAIL** |
| TOST fronteira `−δ`, `α=0,05` | **0,751** | **FAIL** |
| TOST fronteiras 5σ | 0,001 / 0,002 | **OPEN — sem resolução suficiente** |
| `NONSPECIFIC_POWERED`, `n=320` | **0,022** | **FAIL — sem poder de 90%** |
| `NONSPECIFIC_POWERED`, `n=618`, 5σ | **0,311** | **FAIL** |
| `NONSPECIFIC_POWERED`, `n=655`, 5σ | **0,412** | **FAIL** |

O sufixo POWERED agora tem regra e medição, mas não tem promessa de poder.

## 3. Problema 3 — o modelo agregado não representava as sessões

**Defeito:** o modelo binário agregado não continha sessões individuais, A8/retorno separados, falha de manipulação, perdas, dependência Q–S nem integridade.

**Correção R3.1:** blocos individuais com cinco braços, três famílias, focal fixa única, três textos/versões por controle, dependência Q–S, disponibilidade, `d1`, até 30% de candidatos adicionais e integridade simulada.

| cenário | integridade | **POWERED** | IC MC 95% |
|---|---:|---:|---:|
| independente | 0,992 | **0,992** | [0,98648; 0,99752] |
| ICC 0,15 / texto 0,10 | 0,267 | **0,012** | [0,00525; 0,01875] |
| ICC 0,35 / texto 0,20 | 0,000 | **0,000** | [0; 0] |
| controles 0,70 | 0,300 | **0,023** | [0,01371; 0,03229] |
| controles 0,80 | 0,289 | **0,020** | [0,01132; 0,02868] |
| teto pooled / por braço | 0,000 | **0,000** | [0; 0] |
| estresse de integridade | 0,000 | **0,000** | [0; 0] |
| 5σ ideal, `n=618` | 0,990 | **0,599** | [0,56862; 0,62938] |
| 5σ ideal, `n=655` | 0,988 | **0,669** | [0,63983; 0,69817] |

Esses números substituem os agregados como avaliação da análise R3.1, sem se tornarem estimativas de modelos reais.

## 4. Problema 4 — PLA/OUT não era evidência de convergência

**Correção R3.1:** somente seis testes ISO-A/ISO-B integram a evidência primária, com Holm 6. Os seis `Q` de PLA/OUT são diagnóstico de manipulação/contaminação; os doze `S` são checagens separadas. PLA/OUT entra no TOST apenas para o ramo de não especificidade, com precedência sobre `POWERED`.

`FALSIFIED` contém três intervalos focais e seis direções ISO, Bonferroni `α/9`. Uma equivalência PLA/OUT verdadeira não é falha de integridade nem pode ser chamada de convergência específica.

## 5. Validação computacional e repetição

- FFT, DP e enumeração explícita foram comparados em três casos (`raw`, `+δ`, `−δ`).
- Erro máximo: **0,0 / 0,0 / 0,0**.
- Veredito: **PASS**.
- Resolução mínima da permutação: `1/2^27=7,4505805969×10⁻⁹`.
- A repetição do cenário-base produziu bytes idênticos e SHA-256 `2100b5e630943f76bc3083226cb6895b407a92eb4f38cbf2b5811f6dd4afb642`.

Todos os cenários usam 1.000 corridas. O JSON final contém taxas, intervalos Monte Carlo, sementes, custos e limitações.

## 6. Interações, alinhamento e custos

Todos os documentos desta frente usam **12 interações** e **p=8,r=10**. Anexos de outros agentes que usem oito interações ou `p=4,r=6` ficam registrados como dependência de alinhamento, sem edição fora do escopo.

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`; o `k=1` dos selecionados não é contado duas vezes. Calibração, reposições posteriores e tokens permanecem separados e abertos.

## 7. Tabela final de portões

| portão | estado | evidência |
|---|---|---|
| FFT/exata contra enumeração e DP | **PASS** | erro máximo 0 |
| Repetição determinística | **PASS** | bytes idênticos no cenário-base |
| Tamanho global `α=0,05` | **FAIL** | 0,740 |
| Tamanho global 5σ | **OPEN** | resolução insuficiente |
| TOST `α=0,05` | **FAIL** | 0,737/0,751 |
| TOST 5σ | **OPEN** | 0,001/0,002, sem resolução |
| `NONSPECIFIC_POWERED` | **FAIL** | 0,022/0,311/0,412 |
| `POWERED` sob ICC/texto | **FAIL** | 0,012 com ICC 0,15; zero com ICC 0,35 |
| `POWERED` 5σ ideal | **FAIL** | 0,599/0,669 |
| Intervalo t/Wald focal 5σ | **FAIL/BLOQUEADO** | cauda não validada |
| Extrator | **FAIL/BLOQUEADO** | tetos e independência dos 96 erros abertos |
| Modelos/tokenizers/janelas | **OPEN/BLOQUEADO** | não escolhidos |
| Léxico e perturbações | **OPEN/BLOQUEADO** | não congelados |
| Ratificação | **OPEN** | revisão distinta e operador |
| **Produção** | **FAIL/BLOQUEADO** | todas as portas anteriores |

## 8. Arquivos e hashes desta emenda

Documentos atualizados:

- `PROTOCOLO_EXPERIMENTAL_R3_K06.md`;
- `PODER_CONJUNTO_K06.md`;
- `DEGRAU_5_SIGMA_K06.md`;
- `ERRATA_R3_1_K06.md`.

Resultados e código:

- `K06\PODER\resultados_r31.json`: SHA-256 `09b4fb473e61338342644b67e817d99d2be3113a05a2e55004c4d8b6ac3b8f0e`;
- `K06\PODER\r31_motor.py`: SHA-256 `f546067d8e1596dce387c8046c1a774eebb3f8510c8fa133e129c95a6794f57f`;
- `K06\PODER\simular_r31_sessoes.py`: SHA-256 `5cd912e8cb2a938046ce115185e6e777d28fd5e4403608ab6fc41b7f081479ec`;
- `K06\PODER\validar_r31.py`: SHA-256 `6f77689f10b3a25ff912bf21ffb4e9612830ca38a86fd9d9f84e35aa560f8106`;
- `K06\PODER\validacao_r31.json`: SHA-256 `e744a7974fdfc5a3e5e89d75cfcaf8a4191f848b4266ece9f43eaf565bf17a5b`;
- `K06\PODER\manifesto_analise_r31.json`: SHA-256 `f41d17ed5e9e6089fc8045718f57a05c9c0c6e0093d3a3b33d14702df519e749`;
- `K06\PODER\MANIFESTO_R31_SHA256.json`: SHA-256 `0b4b3b6c1b2fc8bbb452bebcbb52be4aab3c107e96a74ed44eafb4f47db3e983`.

**Conclusão:** a emenda fecha os quatro defeitos de implementação e mede suas consequências. Não fecha a validade experimental. Tamanho, TOST, poder, extrator, janela, léxico e cauda 5σ mantêm a R3.1 bloqueada.

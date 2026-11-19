# DEGRAU 5 SIGMA K06 — R3.2 e cauda ainda bloqueada

## 0. Estatuto

[DECLARADO] Correção dirigida **revisada internamente**, não ratificada. O degrau pertence ao operador. A R3.2 permanece **BLOQUEADA_PARA_PRODUCAO**.

[REAL] Nenhum modelo foi executado e nenhum resultado experimental foi aberto. Todos os valores novos são simulações sintéticas com 1.000 corridas por cenário.

O nível candidato continua `α₅=2,866515718792×10⁻⁷` unilateral. Ele não significa confirmação física, creditação ou `CONFIRMED`.

## 1. Benchmarks históricos e escopo atual

Os benchmarks antigos `185`, aproximadamente `215`, `655` e a correção IUT `618`, além de **13.100 sessões/104.800 interações** em oito interações, são somente linhagem. Números agregados antigos continuam **MODELO_AGREGADO_INCOMPLETO**.

A R3.2 usa **12 interações** e **p=8,r=10**. Os anexos foram alinhados por erratas próprias a 12 interações e `p=8,r=10`.

## 2. Poder operacional em 5σ após as correções

| cenário ideal | integridade | **POWERED** | IC MC 95% |
|---|---:|---:|---:|
| `n=618` | 0,990 | **0,599** | [0,56862; 0,62938] |
| `n=655` | 0,988 | **0,669** | [0,63983; 0,69817] |

Nenhum degrau atinge 0,90. Os cenários são ideais: independência e extrator válido. Eles não apagam ICC, efeito de texto, janela desconhecida ou os bloqueios reais.

A evidência primária contém seis testes ISO. PLA/OUT é diagnóstico de manipulação/contaminação e entra apenas no TOST separado, com precedência de `NONSPECIFIC_POWERED` quando as seis equivalências passam.

## 3. Poder de NONSPECIFIC_POWERED em 5σ

| nulo específico verdadeiro | **NONSPECIFIC_POWERED** | IC MC 95% | **POWERED** | IC MC 95% |
|---|---:|---:|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | 0,000 | [0; 0] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | 0,370 | [0,34008; 0,39992] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | 0,350 | [0,32044; 0,37956] |

Essas taxas são poder sob equivalência verdadeira, não tamanho. Não justificam 90% nem resolvem a especificidade em todas as corridas.

## 4. Fronteiras corrigidas e cauda 5σ

Todas as fronteiras usam `Q` parametrizado diretamente para `D=±0,15`, com tolerância 0,005 por família/comparador. Os desvios máximos em 5σ são 0,003044 no nulo global e 0,001628/0,003053 nos dois TOST: **PASS**.

| avaliação | estimativa | porta |
|---|---:|---|
| nulo global ISO, 5σ | 0,000 | **OPEN — resolução insuficiente** |
| TOST fronteira `+δ`, 5σ | 0,000 | **OPEN — não validar a cauda** |
| TOST fronteira `−δ`, 5σ | 0,000 | **OPEN — não validar a cauda** |
| intervalo focal t/Wald, 5σ | não validado | **FAIL/BLOQUEADO** |

Zeros em 1.000 corridas não provam nível 5σ. A permutação exata não valida o intervalo t focal, cuja cauda continua bloqueada.

Em `α=0,05`, o TOST passa com 0,044/0,040. O nulo global fica em 0,057, **OPEN/BORDERLINE**, com IC MC 95% [0,04263; 0,07137]. As antigas taxas de tamanho da R3.1 foram descartadas como cenários mal parametrizados.

## 5. Custos corrigidos de 12 interações e triagem

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| R3.2 base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| R3.2 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| R3.2 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é `candidatos_usados − sessões_primárias`. O `k=1` dos selecionados não é duplicado. Calibração, reposições posteriores e tokens ficam separados e abertos.

O custo legado de 13.100 sessões/104.800 interações permanece válido apenas no benchmark de oito interações.

## 6. Portões e bloqueios

| portão | resultado |
|---|---|
| FFT/exata contra enumeração e DP | **PASS — erro máximo 0** |
| `A8⇒PRE`, `RETORNO⇒PRE`, `Q⇒RETORNO` | **PASS em todos os cenários** |
| Fronteiras `D=±0,15`, tolerância 0,005 | **PASS** |
| TOST `α=0,05` | **PASS — 0,044/0,040** |
| Tamanho global `α=0,05` | **OPEN/BORDERLINE — 0,057** |
| Tamanho e TOST 5σ | **OPEN — resolução insuficiente** |
| `NONSPECIFIC_POWERED` | **FAIL — 0,022/0,311/0,412** |
| `POWERED` 5σ ideal | **FAIL — 0,599/0,669** |
| Intervalo t/Wald 5σ | **FAIL/BLOQUEADO** |
| Extrator | **FAIL/BLOQUEADO** |
| Modelos/tokenizers/janelas | **OPEN/BLOQUEADO** |
| Léxico e perturbações | **OPEN/BLOQUEADO** |
| Ratificação | **OPEN — revisão distinta e operador** |
| Produção | **FAIL/BLOQUEADO** |

## 7. Reprodução e integridade

- resultados: `K06\PODER\resultados_r32.json`, SHA-256 `228e1d99e0a815a62d4ea55a156e3fe45ab5bf091f619bfce496458690105eb2`;
- análise: `K06\PODER\manifesto_analise_r32.json`, SHA-256 `8b20323937488f7c0c77a22d2bb169d3883d5de81efdfed11e2448478ac192ce`;
- manifesto: `K06\PODER\MANIFESTO_R32_SHA256.json`, SHA-256 `2dd32a68ac5b31177a3f0f6683cd4bb980928e41b611ba64c89dda9dd81e1804`;
- validação: `K06\PODER\validacao_r32.json`, SHA-256 `506e1f6805c28b1b835b5fcfd7de4f0e8a48f2595585387e2c26017e4ef21cb3`;
- repetição determinística: bytes idênticos, SHA-256 `455911a61eba5536ed77e73809068394acebfe180a67e66f4317c86c4f8ec07e`;
- sementes: mestra `2026111501`, cenários por `2026111501+101·índice`, todos listados no manifesto.

**Conclusão:** as fronteiras estão corrigidas, mas a R3.2 não atinge poder adequado nem valida a cauda 5σ. O degrau permanece bloqueado.

# DEGRAU 5 SIGMA K06 — R3.1 e bloqueios explícitos

## 0. Decisão e estatuto

[DECLARADO] Documento **revisado internamente**, não ratificado. A escolha do degrau pertence ao operador. A R3.1 permanece **BLOQUEADA_PARA_PRODUCAO**.

[REAL] Nenhum modelo foi executado e nenhum resultado experimental foi aberto. Todos os valores novos são simulações sintéticas com 1.000 corridas por cenário.

O nível candidato continua `α₅=2,866515718792×10⁻⁷` unilateral. Ele não significa confirmação física, creditação ou `CONFIRMED`.

## 1. Benchmarks antigos, não poder da R3.1

A conferência anterior reproduziu:

- `n=184,903788 → 185` para um contraste;
- aproximadamente `n=215` para os 12 dinâmicos antigos;
- `n=655` como primeiro ponto sustentado do CP antigo `/3`;
- `n=618` após correção IUT;
- **13.100 sessões/104.800 interações** no desenho legado de oito interações.

Esses benchmarks são mantidos apenas como linhagem. O poder agregado anterior `0,92080/0,93945` é **MODELO_AGREGADO_INCOMPLETO** e não é reutilizado como poder integral da R3.1.

A R3.1 usa **12 interações** e **p=8,r=10**. Anexos de outros agentes com oito interações ou `p=4,r=6` precisam de alinhamento próprio e não foram editados.

## 2. Poder operacional da R3.1 em 5σ

| cenário ideal | integridade | **POWERED** | IC MC 95% |
|---|---:|---:|---:|
| `n=618` | 0,990 | **0,599** | [0,56862; 0,62938] |
| `n=655` | 0,988 | **0,669** | [0,63983; 0,69817] |

Nenhum degrau atinge 0,90. Os cenários pressupõem independência e extrator válido; não incluem ICC, efeito de texto desfavorável, janela desconhecida ou os bloqueios reais do extrator.

A evidência primária tem seis testes ISO, não os 24 testes antigos. PLA/OUT é diagnóstico de manipulação/contaminação e entra apenas no ramo TOST separado.

## 3. NONSPECIFIC_POWERED nos mesmos degraus

| nulo específico verdadeiro | **NONSPECIFIC_POWERED** | IC MC 95% | **POWERED** | IC MC 95% |
|---|---:|---:|---:|---:|
| `n=320`, `α=0,05` | **0,022** | [0,01291; 0,03109] | 0,000 | [0; 0] |
| `n=618`, 5σ | **0,311** | [0,28231; 0,33969] | 0,370 | [0,34008; 0,39992] |
| `n=655`, 5σ | **0,412** | [0,38149; 0,44251] | 0,350 | [0,32044; 0,37956] |

O sufixo POWERED não representa 90% de probabilidade. A possibilidade de `POWERED` sob nulo específico verdadeiro também mostra que a especificidade não fica resolvida em todas as corridas.

## 4. Tamanho e cauda 5σ

| avaliação | estimativa | porta |
|---|---:|---|
| nulo global ISO, 5σ | 0,001 | **OPEN — 1.000 corridas não resolvem a cauda nominal** |
| TOST fronteira `+δ`, 5σ | 0,001 | **OPEN — não validar a cauda** |
| TOST fronteira `−δ`, 5σ | 0,002 | **OPEN — não validar a cauda** |
| intervalo focal t/Wald, 5σ | não validado | **FAIL/BLOQUEADO** |

A permutação exata dos seis contrastes e dos TOST não valida o intervalo t focal. O número pequeno de rejeições não pode ser convertido em afirmação de nível 5σ: a resolução Monte Carlo é insuficiente e a componente Wald permanece expressamente bloqueada.

Em `α=0,05`, os resultados são mais diretamente desfavoráveis: tamanho global **0,740** e fronteiras TOST **0,737/0,751**, ambos **FAIL**.

## 5. Custos corrigidos de 12 interações e triagem

| desenho | sessões primárias | interações primárias | adicional líquido `k=1` | base + adicional |
|---|---:|---:|---:|---:|
| R3.1 base, `n=320` | 6.400 | 76.800 | **163,27** | **76.963,27** |
| R3.1 5σ, `n=618` | 12.360 | 148.320 | **312,09** | **148.632,09** |
| R3.1 5σ, `n=655` | 13.100 | 157.200 | **335,03** | **157.535,03** |
| estresse, `n=320` | 6.400 | 76.800 | **1.920,00** | **78.720,00** |

O adicional é o número de candidatos usados menos as sessões primárias. O `k=1` dos selecionados já está incluído nas 12 interações e não é duplicado. Calibração, reposições posteriores e tokens continuam separados e abertos.

O antigo custo de 13.100 sessões/104.800 interações permanece correto somente para o benchmark legado de oito interações.

## 6. Alternativas não selecionadas

As alternativas anteriores — menos braços, desfecho contínuo e sequencial pré-registrado — não foram escolhidas nem validadas por esta emenda. Qualquer uma exige nova multiplicidade, avaliação de tamanho e poder sob sessões individuais e clusters. Não recebem números da R3.1 por analogia.

## 7. Portões e bloqueios

| portão | resultado |
|---|---|
| FFT/exata contra enumeração e DP | **PASS — erro máximo 0** |
| Tamanho global `α=0,05` | **FAIL — 0,740** |
| Tamanho global 5σ | **OPEN — resolução insuficiente** |
| TOST `α=0,05` | **FAIL — 0,737/0,751** |
| TOST 5σ | **OPEN — 0,001/0,002, sem resolução suficiente** |
| `NONSPECIFIC_POWERED` | **FAIL — 0,022/0,311/0,412** |
| `POWERED` 5σ ideal | **FAIL — 0,599/0,669** |
| Intervalo t/Wald 5σ | **FAIL/BLOQUEADO** |
| Extrator | **FAIL/BLOQUEADO** |
| Modelos/tokenizers/janelas | **OPEN/BLOQUEADO** |
| Léxico e perturbações | **OPEN/BLOQUEADO** |
| Ratificação | **OPEN — operador e revisão distinta** |
| Produção | **FAIL/BLOQUEADO** |

## 8. Reprodução e integridade

- resultados: `K06\PODER\resultados_r31.json`, SHA-256 `09b4fb473e61338342644b67e817d99d2be3113a05a2e55004c4d8b6ac3b8f0e`;
- análise: `K06\PODER\manifesto_analise_r31.json`, SHA-256 `f41d17ed5e9e6089fc8045718f57a05c9c0c6e0093d3a3b33d14702df519e749`;
- manifesto: `K06\PODER\MANIFESTO_R31_SHA256.json`, SHA-256 `0b4b3b6c1b2fc8bbb452bebcbb52be4aab3c107e96a74ed44eafb4f47db3e983`;
- validação FFT: `K06\PODER\validacao_r31.json`, SHA-256 `e744a7974fdfc5a3e5e89d75cfcaf8a4191f848b4266ece9f43eaf565bf17a5b`;
- repetição determinística do cenário-base: bytes idênticos, SHA-256 `2100b5e630943f76bc3083226cb6895b407a92eb4f38cbf2b5811f6dd4afb642`;
- sementes: mestra `2026111501`, cenários por `2026111501+101·índice`, todos listados no manifesto.

**Conclusão:** os benchmarks antigos foram conferidos, mas a R3.1 não atinge poder ou tamanho adequado em 5σ. O degrau permanece bloqueado; a decisão de qualquer nova rota é do operador, sem promessa desta frente.

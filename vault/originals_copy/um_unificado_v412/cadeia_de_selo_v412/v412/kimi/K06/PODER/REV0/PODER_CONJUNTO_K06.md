# PODER CONJUNTO K06 — veredito completo R3, script e sementes

## 0. Veredito

- [REAL — simulação sintética] A R3 separa resumo de retorno no exemplo construído: `SEPARA_EM_SIMULACAO`.
- [REAL — simulação sintética] A cota superior da R2 foi reproduzida: **0,346125**; a perna CP exata das três famílias é **0,347478**. O valor não era poder de um contraste, mas do ramo inteiro sob as regras antigas.
- [REAL — simulação sintética] O desenho-base R3, com `n=320` por célula, alcança **0,99905** no cenário independente e **0,95245** com ICC 0,15. Não alcança 0,90 com ICC 0,35 nem com controles em 0,80.
- [REAL] Os tetos conservadores atuais do extrator bloqueiam qualquer promessa: 0 sucessos em 20.000 corridas no cenário pooled e 0 em 20.000 no cenário por braço.
- [DECLARADO] Documento **revisado internamente**, não ratificado. A R3 está **BLOQUEADA_PARA_PRODUCAO**. Nenhum modelo foi executado e nenhum resultado experimental foi aberto.

## 1. O que foi simulado: o veredito, não um contraste

O script `K06\PODER\simular_poder_conjunto.py` simula a conjunção completa:

1. três famílias capazes;
2. 12 contrastes dinâmicos de `Q=A8_condicionado_d1 ∧ RETORNO`;
3. 12 contrastes de especificidade `S=1[X≥18/24]`;
4. Holm global sobre os 24 testes;
5. três limites inferiores de Clopper–Pearson para `Q` na focal, com `L_CP>0,80`;
6. regra IUT de `POWERED`, sem a divisão desnecessária por três;
7. taxa da perna CP de `FALSIFIED`, separada da união completa de 27 testes de falha.

O corte CP de `POWERED` no desenho-base é `x_Q≥269/320` em cada uma das três famílias. Todos os 24 testes precisam passar; se um bloco de 12 passa e o outro falha, não há `POWERED`.

As taxas ideais de planejamento são `p_Q(T)=0,90`, `p_Q(PLA/OUT)=0,60` e `p_Q(ISO)=0,90`; para especificidade, 0,95, 0,70 e 0,95. ISO-A/ISO-B testam não inferioridade com margem 0,15. Essas taxas são **hipóteses de desenho**, não dados piloto nem estimativas de modelos.

Cada cenário principal tem 20.000 corridas. A reprodução da R2 tem 40.000 e segue a regra antiga, inclusive especificidade assumida sempre significativa — portanto é cota superior.

## 2. Dependência, textos e `n` efetivo

O gerador usa:

- três estratos de texto por braço de controle;
- dificuldade latente compartilhada entre braços no mesmo estrato;
- efeito de texto no logit, com `σ_texto` conforme o cenário;
- clusters de dez sessões;
- contagens beta-binomiais quando ICC>0;
- `DEFF=1+9·ICC` e `n_eff=n/DEFF`.

Temperatura 0,2 é apenas o rótulo da configuração de planejamento: nenhum LLM foi chamado. ICC 0,15 e 0,35 são cenários, não medições de um provedor. A variância de texto entra separadamente e não é escondida no `n_eff` de ICC.

O teto do extrator é imposto como limite ao evento e à especificidade em todos os braços. É um teste de sensibilidade conservador, não um modelo identificado dos 96 erros de asserção-leitura.

## 3. Resultado completo por cenário

Os intervalos abaixo são aproximações normais do erro Monte Carlo, não intervalos de confiança para taxas de modelos reais. “0,00000” significa 0 sucessos observados em 20.000 corridas, não prova de probabilidade exatamente zero.

| cenário | semente | ICC / `σ_texto` | `n_eff` ICC | CP nas 3 | 24 globais | **POWERED completo** | IC MC 95% |
|---|---:|---:|---:|---:|---:|---:|---:|
| independente | 2026111401 | 0 / 0 | 320,000 | 0,99905 | 1,00000 | **0,99905** | [0,99862; 0,99948] |
| temperatura 0,2, ICC moderado | 2026111502 | 0,15 / 0,10 | 136,170 | 0,95350 | 0,99225 | **0,95245** | [0,94950; 0,95540] |
| temperatura 0,2, ICC alto | 2026111603 | 0,35 / 0,20 | 77,108 | 0,83705 | 0,92850 | **0,82375** | [0,81847; 0,82903] |
| controles PLA/OUT=0,70 | 2026111704 | 0,15 / 0,10 | 136,170 | 0,95215 | 0,98700 | **0,94885** | [0,94580; 0,95190] |
| controles PLA/OUT=0,80 | 2026111805 | 0,15 / 0,10 | 136,170 | 0,95285 | 0,51780 | **0,51605** | [0,50912; 0,52298] |
| teto extrator pooled=0,619206 | 2026111906 | 0 / 0 | 320,000 | 0,00000 | 0,00000 | **0,00000** | 0/20.000 |
| teto por braço=0,091028 | 2026112007 | 0 / 0 | 320,000 | 0,00000 | 0,00000 | **0,00000** | 0/20.000 |
| ICC 0,35 + controle 0,70 + teto pooled | 2026112108 | 0,35 / 0,20 | 77,108 | 0,00000 | 0,00000 | **0,00000** | 0/20.000 |
| 5σ R3, `n=618` | 2026112209 | 0 / 0 | 618,000 | 0,92085 | 0,99925 | **0,92080** | [0,91706; 0,92454] |
| 5σ R3, `n=655` | 2026112310 | 0 / 0 | 655,000 | 0,93945 | 0,99990 | **0,93945** | [0,93614; 0,94276] |

### Leituras que não podem ser trocadas entre si

- O poder de um contraste não aparece como se fosse o valor da tabela: a coluna principal é a **conjunção**.
- Com controles em 0,80, o CP continua alto, mas os 24 caem para 0,51780; a perna dominante deixa de ser o CP.
- Com ICC 0,35, os 24 passam em 0,92850 e o CP em 0,83705; a dependência derruba o conjunto.
- A frequência “um bloco passa e o outro falha” é 0,48210 no cenário de controle 0,80. Esse resultado nunca é promovido a `POWERED`.
- Os valores 5σ são cenários ideais, sem ICC, sem teto de extrator e com uma aproximação normal declarada para não inferioridade; não são certificação de cauda.

## 4. A correção da manchete R2

A reprodução com semente `20261113` obteve:

| componente R2 | resultado |
|---|---:|
| corte CP antigo por família | 89/100 |
| CP exato das três famílias | 0,3474780047 |
| Holm dos 12 dinâmicos | 0,99550 |
| **cota superior do ramo completo** | **0,346125** |

A R3 corrige esse valor pelo desenho, não por apresentar outro contraste: aumenta `n`, introduz retorno no evento, inclui os 24 em uma única família de Holm e remove a penalidade CP indevida do IUT. O preço é 6.400 sessões e 76.800 interações no desenho-base, antes de triagem e calibração.

Esse ganho não supera o bloqueio do instrumento: com o teto pooled ou por braço, a simulação não produz qualquer `POWERED`.

## 5. Separação sintética: resumidor perfeito × atrator

Script: `K06\PODER\simular_separacao_r3.py`; semente `2026111402`; 24 asserções; seis índices perturbados `[12,14,16,18,21,23]`.

Os dois sistemas produzem oito leituras perfeitas antes do empurrão. Assim, o exemplo não confunde dificuldade ou qualidade de resumo com retorno.

| leitura | A8 | C8 legado | distâncias após `k=8` | RETORNO | `Q` |
|---|---:|---:|---|---:|---:|
| resumidor perfeito sem atrator | 1 | 0 | `d9=d10=d11=d12=0,25` | **0** | **0** |
| leitor com atrator | 1 | 0 | `d9=0,25`; `d10=d11=d12=0` | **1** | **1** |

Saída registrada: `VEREDITO=SEPARA_EM_SIMULACAO`. Se `Q` não diferingisse, o script terminaria com código 2 e `NAO_DECIDE`.

A perturbação ocorre em `p=8` e o retorno em `r=10` para que o mesmo período experimental preserve `A8` nas leituras 1–8 e a janela decisória nas leituras 9–12. O predicado `p=4,r=6` dos autotestes anteriores permanece preservado e não foi reescrito.

## 6. Multiplicidade congelada

### `POWERED`: conjunção

- Holm global sobre 24; ordem fixa `F1/F2/F3 × DYN/SPEC × PLA/OUT/ISO-A/ISO-B`.
- Empates ordenados por `contrast_id`; todos os resultados iguais ao observado entram na cauda exata.
- IUT entre blocos e entre as três pernas CP: sem `/2` e sem `/3`.
- PLA/OUT: superioridade Fisher/permutação exata.
- ISO: não inferioridade por score de Wald, margem 0,15; aproximação normal declarada.

A permutação dos testes binários de superioridade é exata via hipergeométrica. Por isso `rng_seed=null` para a permutação: não há sorteio Monte Carlo nem perda de resolução de cauda. As sementes dos dados sintéticos e das sessões permanecem obrigatórias.

### `FALSIFIED`: união

A união contém três pernas CP e 24 testes direcionais opostos. Usa Bonferroni `α/27`; não se aplica a divisão por três do IUT, que pertence só ao ramo de conjunção. O JSON separa a taxa da perna CP, a taxa direcional e a união; `POWERED` é zerado quando qualquer uma delas ocorre. A probabilidade de `NONSPECIFIC_POWERED` não é estimada por essas corridas.

### Nulo com poder

`IALD_COLLAPSE_V2_NONSPECIFIC_POWERED` exige 12 equivalências PLA/OUT × `Q/S` × três famílias, por TOST/Holm com margem 0,15. Se a equivalência não é resolvida, o ramo é `UNDERPOWERED`. Falha de integridade sempre produz `INCONCLUSIVE_CONTROLS` antes de qualquer um desses ramos.

## 7. Teto do extrator: por que o número de casos não basta

[REAL] Os insumos integrados mostram:

- 685 casos no contrato, 0 erros;
- 5 paráfrases fora do contrato, 0/120 células positivas recuperadas;
- erro superior 95% pooled=0,498044%;
- teto conservador pooled `A8=0,619206064`;
- teto por braço `A8=0,091028210`;
- independência dos 96 erros não medida.

O ponto 100% não certifica o limite necessário. Por isso a tabela tem duas perguntas diferentes: “quanto poder o desenho teria se as hipóteses ideais valessem?” e “o instrumento atual permite prometê-lo?”. A resposta à segunda é **não**.

## 8. Scripts, logs, hashes e reprodução

Diretório: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER\`.

```bat
cd /d "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER"
python -B -X utf8 simular_separacao_r3.py
python -B -X utf8 simular_poder_conjunto.py --nsim 20000
python -B -X utf8 verificar_degrau_5sigma.py
python -B -X utf8 gerar_manifestos.py
```

| artefato | SHA-256 |
|---|---|
| `simular_poder_conjunto.py` | `82b7023c180edc35e1c15315c51465e5689c0f5cd81549f0b7260c176b70d697` |
| `simular_separacao_r3.py` | `8fbcc9261238e18991e0f3d5ab91b35cfa4155fab3b910f441a8103bb025805d` |
| `verificar_degrau_5sigma.py` | `98f08165f63d8a082bd4dd9f516200515fc1a6dd2d079d9a9c019200dfa7dc2d` |
| `resultados_poder.json` | `b6eab6d760a384c6224123afd9e71b2ceee75bf6f1f00e4365f6a566cd8b0f04` |
| `separacao_r3.json` | `02a15e34d4afaed66de329c6113d06c05e86aa4e80c0bcc8741d8d2a73edaefd` |
| `degrau_5sigma.json` | `e1955642c07e996fb197cd5d1a959e4aea9b5b8c6a7c6e91b4d2583c1e5ed2d2` |
| `poder_conjunto.log` | `ade3e668addc32ab5869cb6012deb6672149131707dcf18c6a9a4b0a49751bed` |
| `manifesto_analise.json` | `69117f49f2a531d84b1757758fa9ef60e3b03c9893bc6bf4cc9d3e62871665c6` |
| `MANIFESTO_SHA256.json` | `7e6166e1daa5c8aa04337c12fc8d41aa9c0147e500c6780c02635ea29d154cb1` |

O manifesto de análise contém a ordem, os cortes, as regras de permutação, as sementes e os bloqueios. O manifesto de artefatos não contém hash de si mesmo nem dos três documentos narrativos, evitando referência circular.

## 9. Limites do cálculo e bloqueios remanescentes

1. Validação ampliada do extrator e teto por braço.
2. Escolha entre gramática estrita e prosa livre, com nova validação se necessário.
3. Dependência dos 96 erros.
4. Léxico isomorfo e perturbações congelados.
5. Modelos, tokenizers, janelas e orçamento de 12 interações.
6. Textos/controles, dificuldade medida e pareamento.
7. Manifesto final e custódia.
8. Validação da cauda de não inferioridade e nova simulação se o desenho mudar.
9. Ratificação da R3 inteira pelo operador.

**Conclusão:** a R3 corrige logicamente o desfecho e quantifica o veredito inteiro. Seu poder não é uniforme entre cenários e desaba sob os tetos conservadores do extrator. A separação sintética não é certificação de produção.

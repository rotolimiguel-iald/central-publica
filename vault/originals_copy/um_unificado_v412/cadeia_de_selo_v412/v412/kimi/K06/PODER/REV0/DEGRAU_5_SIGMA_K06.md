# DEGRAU 5 SIGMA K06 — benchmark legado, R3 corrigida e alternativas

## 0. Decisão que cabe ao operador

[DECLARADO] Este documento **revisado internamente** não escolhe entre o desenho-base e 5σ. Apresenta custos e poder sintético; modelos, degrau e execução continuam com o operador. A R3 está **BLOQUEADA_PARA_PRODUCAO**.

[REAL] Nenhum modelo foi executado e nenhum resultado experimental foi aberto. Todos os números novos vêm de scripts sintéticos com sementes fixas.

O valor 5σ é aqui `α₅=2,866515718792×10⁻⁷` unilateral. Não significa creditação da natureza, confirmação física nem promoção de `NOT_FALSIFIED` a `CONFIRMED`; é apenas um nível estatístico candidato para comportamento de modelos.

## 1. Conferência dos números pedidos

Script: `K06\PODER\verificar_degrau_5sigma.py`; semente `2026111403`.

### 1.1 Um contraste: aproximadamente 185 por braço/célula

Para `p_T=0,90`, `p_C=0,60`, poder 0,90 e o passo mais estrito `α₅/12=2,388763098993×10⁻⁸`:

- `z=5,459397661`;
- fórmula normal pooled sob H0 e não pooled sob H1: `n=184,903788102`, teto **185**;
- Fisher exato: poder 0,906517552 em `n=184` e 0,908733798 em `n=185`.

Assim, o benchmark **≈185** confere. Ele não é apresentado como mínimo exato inteiro, nem como poder dos 12 ou dos 24 testes.

### 1.2 Os 12 dinâmicos: aproximadamente 215

Com três famílias, quatro controles legados, T compartilhado, Holm/12 e 40.000 corridas por `n`:

| `n` por braço | probabilidade dos 12 rejeitarem |
|---:|---:|
| 210 | 0,89150 |
| **215** | **0,91330** |

O valor é aproximado e Monte Carlo. Não inclui especificidade, CP, isomorfos de não inferioridade nem o veredito completo.

### 1.3 CP antigo: 655 sustentado; IUT corrigido: 618

A revisão legada usava confiança `1−α₅/3` em cada família. A nova simulação confirma:

| regra | primeiro qualquer ponto na grade | primeiro ponto sustentado até 700 | corte | poder CP das três famílias |
|---|---:|---:|---:|---:|
| legado `/3`, `n=655` | 642 | **655** | 575/655 | **0,9181133898** |
| IUT sem `/3`, `n=618` | 606 | **618** | 542/618 | **0,9208472880** |

“Primeiro qualquer ponto” e “primeiro sustentado” diferem porque o corte inteiro produz dente de serra. Por isso se conserva **≥655** como benchmark legado e **≥618** como benchmark IUT, sem apagar o comportamento não monotônico pontual.

A divisão por três era desnecessária somente no `POWERED`, que é uma conjunção/IUT. O `FALSIFIED` continua união e recebe Bonferroni próprio; na R3 completa são três CP + 24 testes direcionais opostos, `α/27`.

## 2. O benchmark de oito interações e a R3 de doze

A R2 usava oito interações. A R3 mede `A8` em `k=1…8`, perturba depois de `k=8` e mede retorno em `k=9…12`. Por isso o custo legado não pode ser apresentado como o custo final da R3.

| desenho | `n`/célula | células | interações/sessão | **sessões** | **interações** |
|---|---:|---:|---:|---:|---:|
| R2 histórica | 100 | 20 | 8 | 2.000 | 16.000 |
| **R3 base** | **320** | **20** | **12** | **6.400** | **76.800** |
| benchmark 5σ legado `/3` | 655 | 20 | 8 | **13.100** | **104.800** |
| benchmark 5σ IUT, oito interações | 618 | 20 | 8 | 12.360 | 98.880 |
| **R3 5σ IUT** | **618** | **20** | **12** | **12.360** | **148.320** |
| R3 5σ com o `n` legado | 655 | 20 | 12 | 13.100 | 157.200 |
| só famílias capazes, benchmark legado | 655 | 15 | 8 | 9.825 | 78.600 |

Os 20 núcleos incluem quatro famílias × cinco braços. A família abaixo do piso não entra na inferência primária, mas permanece no custo quando é executada. Triagem de `d1`, calibração, reposições técnicas e análise não estão incluídas.

## 3. Poder da R3 completa em 5σ

A tabela anterior de `n` é benchmark. O poder do veredito completo foi simulado separadamente com 20.000 corridas, 24 testes globais, três CP e o evento `Q=A8∧RETORNO`:

| cenário ideal | semente | CP nas três | 24 globais | **POWERED completo** | IC MC 95% |
|---|---:|---:|---:|---:|---:|
| R3 5σ, `n=618` | 2026112209 | 0,92085 | 0,99925 | **0,92080** | [0,91706; 0,92454] |
| R3 5σ, `n=655` | 2026112310 | 0,93945 | 0,99990 | **0,93945** | [0,93614; 0,94276] |

Esses valores pressupõem independência, extrator perfeito, `p_Q(T)=0,90`, controles PLA/OUT=0,60 e isomorfos equivalentes. Não incluem ICC, efeito desfavorável de texto, controles 0,70/0,80, teto do extrator ou janela desconhecida. A não inferioridade usa aproximação normal; a cauda 5σ precisa de validação adicional antes de produção.

No desenho-base de 5%, o poder completo é 0,99905 sem ICC e 0,95245 com ICC 0,15; cai para 0,82375 com ICC 0,35 e 0,51605 com controles 0,80. Sob os tetos conservadores do extrator houve 0/20.000 sucessos. Logo, **5σ não resolve o bloqueio do instrumento**.

## 4. Alternativas para o operador, sem escolha desta frente

### 4.1 Menos braços

Reduzir de quatro para três controles produz 9+9 contrastes e 16 células em vez de 24 testes e 20 células.

Com o mesmo `n=618` e 12 interações:

- **9.888 sessões**;
- **118.656 interações**.

É aritmética de custo, não promessa de poder. É necessário nomear qual controle seria removido, reabrir a multiplicidade e recalcular a conjunção; remover um controle informativo muda a pergunta científica.

### 4.2 Desfecho contínuo

Uma aproximação z para **um** contraste, poder 0,90 e `α₅/12`, dá:

| efeito padronizado hipotético | `n` aproximado por braço |
|---:|---:|
| 0,5 | 364 |
| 0,8 | 143 |
| 1,0 | 91 |

Esses números não incluem 24 testes, CP, retorno, texto ou ICC. Um desfecho contínuo só é alternativa real depois de definir distância, escala, distribuição, limiar de retorno e o efeito padronizado sem olhar saídas. Não se substitui o evento decisório por uma média que volte a confundir resumo com atrator.

### 4.3 Sequencial pré-registrado

Candidato: no máximo quatro análises, gasto de `α` O'Brien–Fleming, regras de parada por eficácia e futilidade congeladas antes de qualquer saída, e mesmo conjunto de modelos/textos.

**Nenhum `n` máximo, esperado ou poder é declarado aqui.** Antes seria necessário simular a parada conjunta dos 24 testes, CP, retorno, ICC, variação de texto, teto do extrator e correlação entre análises. Parar cedo porque um bloco favoreceu T, sem a regra global, é proibido.

## 5. Bloqueios que permanecem em qualquer degrau

1. Extrator ampliado e teto por braço certificado.
2. Gramática estrita ratificada ou prosa livre revalidada.
3. Independência/dependência dos 96 erros medida.
4. Léxico isomorfo, versões e perturbações congelados.
5. Modelos/tokenizers e janela exata para 12 interações.
6. Textos/controles e dificuldade medida.
7. Manifesto, hashes e custódia completos.
8. Cauda de não inferioridade validada e poder recalculado após qualquer emenda.
9. Ratificação da R3 inteira pelo operador.

Os proxies de 205.298–291.088 tokens não autorizam dizer que a entrada cabe ou não cabe; nenhum poder de cabimento foi inventado.

## 6. Reprodução e integridade

```bat
cd /d "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K06\PODER"
python -B -X utf8 verificar_degrau_5sigma.py
python -B -X utf8 simular_poder_conjunto.py --nsim 20000
python -B -X utf8 gerar_manifestos.py
```

- `verificar_degrau_5sigma.py`: SHA-256 `98f08165f63d8a082bd4dd9f516200515fc1a6dd2d079d9a9c019200dfa7dc2d`;
- `degrau_5sigma.json`: SHA-256 `e1955642c07e996fb197cd5d1a959e4aea9b5b8c6a7c6e91b4d2583c1e5ed2d2`;
- `degrau_5sigma.log`: SHA-256 `242b8b822842f1a26bbbd35693afcfd8ffc042e86278115551cfda08dc4f3220`;
- análise congelada candidata: `69117f49f2a531d84b1757758fa9ef60e3b03c9893bc6bf4cc9d3e62871665c6`;
- manifesto de artefatos: `7e6166e1daa5c8aa04337c12fc8d41aa9c0147e500c6780c02635ea29d154cb1`.

**Conclusão:** os números 185/215/655 conferem como benchmarks; o IUT corrige o CP para 618. A R3 inteira tem poder simulado acima de 0,90 nesses dois tamanhos apenas no cenário ideal. O custo e o degrau são decisão do operador; a produção continua bloqueada.

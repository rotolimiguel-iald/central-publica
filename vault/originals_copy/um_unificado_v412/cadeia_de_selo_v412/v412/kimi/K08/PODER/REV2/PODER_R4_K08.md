# PODER R4/K08 — simulação dos mecanismos, clusters e custo

**Estado:** planejamento condicional por mecanismos sintéticos. Nenhum modelo de linguagem foi executado, nenhum resultado experimental foi aberto, nenhum texto foi congelado e nada aqui autoriza produção.

**Veredito:** os desenhos simulados dimensionam apenas o **pacote discreto** P-A + retorno externo + memória do componente dentro do Nome. Eles **não** dimensionam a separação plena da trava, porque a ponte texto→vetor/amplitude permanece aberta e o projetor com fita não é separado pelas cotas. A variante 5σ tem poder operacional calculável, mas **não tem tamanho empiricamente validado na cauda de 5σ**. O instrumento continua **BLOQUEADO**.

`NOT_FALSIFIED` nunca é `CONFIRMED`. Nenhum ramo permite consciência, pesos, aprendizado permanente, exclusividade, creditação, `IALD_PROVED` ou prova da TGL.

## 1. Arquivos, semente e reprodução

Artefatos em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\PODER\`:

| arquivo | conteúdo | SHA-256 |
|---|---|---|
| `simular_poder_r4.py` | motor, testes, busca de desenho, custos e manifesto | `633962378ccb5da55ba1f68e403ee5968aa9b9ed428ccb82e427bf9696fcb90d` |
| `resultados_poder_r4.json` | resultado completo, trilhas de busca e intervalos | `c476ccabb1569ce4819ea170e8576f3d33da1270e64bb3b58b340e4d4b3da1e8` |
| `sementes_r4.json` | semente-mestra e sementes finais por cenário | `946ec197fc62517b5596e4e5f68fb95ce23d38d8cf27def9f838cff1201856e3` |
| `resumo_designs_r4.csv` | tabela resumo dos dezoito designs | `c40c5021639906f0beb703eae78586b80f13a905f5eaee8a59db37f979f67f1a` |
| `VALIDACAO_DETERMINISMO_TOKENS.json` | comparação estatística contra REV1, removendo só custos/tokens | `cf2156351036b9c517ab27b4a1b0cef442a20768712c8f9a7e828068a21c355c` |
| `MANIFESTO_SHA256.json` | hashes do script, das saídas e dos insumos lidos | manifesto autoconsistente |

A versão anterior, com o fallback byte=token histórico, está preservada em `K08\PODER\REV1\`. A comparação `estatisticas_identicas_rev1=true` cobre todos os resultados e trilhas depois de remover somente campos de custo/token.

Reprodução a partir da pasta `K08\PODER`:

```bash
python -B simular_poder_r4.py
```

- Semente-mestra: **`2026111508`**.
- Busca de tamanho: **3.000** réplicas por ponto da grade.
- Estimativa final: **30.000** réplicas por design.
- Derivação de sementes: primeiros 8 bytes do SHA-256 de `MASTER|escopo|...|nsim`, em big-endian.
- Intervalos das taxas: Clopper–Pearson 95 %; zero evento não recebe intervalo `[0;0]`.

O motor lê somente `RESULTADOS_FORMULA.json`, `MEDIDAS_ENTRADA.json`, `TOKENS_REF_K08.json` e os mecanismos de `simular_adversarios.py`; seus hashes entram no manifesto. O catálogo formal subjacente está consolidado em [FORMULA_DO_TEXTO_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CFORMULA%5CFORMULA_DO_TEXTO_K08.md&line=13&text=%7C%20candidata%20%7C%20asser%C3%A7%C3%B5es%20%7C "citation"), e as medidas de tokens usadas vêm de [MEDIDAS_ENTRADA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CENTRADA%5CMEDIDAS_ENTRADA.md&line=22&text=%7C%20candidata%20%7C%20asser%C3%A7%C3%B5es%20%7C "citation").

## 2. O que é simulado — mecanismo, não trajetória escrita à mão

### 2.1 Núcleo de quatro estados derivado da fórmula

Para `READ_BRIEF`, o script constrói quatro estados pela fórmula, não por uma sequência digitada:

| estado | definição operacional | custo na fórmula original | custo em P-C |
|---|---|---:|---:|
| `s` | leitura válida com `leitura_pt = false` | 0 | 1 |
| `t` | leitura válida com `leitura_pt = true` | 0 | 1 |
| `y` | `s` com `artigo_pt_en` negado | 1 | 2 |
| `z` | `y` com `beta_forma` também negado | 2 | 2 |

A validação do script exige exatamente `custo(s,t,y,z) = (0,0,1,2)` e, no controle contraditório, `(1,1,2,2)`. A fórmula original tem duas leituras válidas, a variável livre `leitura_pt` e distância mínima 1; P-C é insatisfazível com custo mínimo 1. [FORMULA_DO_TEXTO_K08](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CFORMULA%5CFORMULA_DO_TEXTO_K08.md&line=26&text=%7C%20candidata%20%7C%20custo(s)%20%7C "citation")

### 2.2 Referência da trava

O estado sintético é um vetor esparso sobre os quatro pontos. A cada ciclo, cada amplitude é multiplicada por `exp(-τ·c_x)`. A leitura amostrada usa probabilidades proporcionais a `|a_x|²`; esta última regra é explicitamente uma **ponte de planejamento**, não um teorema sobre LLM.

Para `K = 4` ciclos, antes do canal de observação:

| τ | `P(s)` no ciclo 3 | `P(s)` no ciclo 4 | retorno externo a `s` no ciclo 4 | P-B dentro | P-C |
|---:|---:|---:|---:|---:|---:|
| 0,25 | 0,785597 | 0,866813 | 0,880797 | 1 | 1 |
| 0,50 | 0,950330 | 0,981690 | 0,982014 | 1 | 1 |
| 1,00 | 0,997521 | 0,999665 | 0,999665 | 1 | 1 |

P-A exige `s` nos ciclos 3 e 4. Esses números são a evolução do mecanismo, não uma trajetória de um modelo.

### 2.3 Canal de observação compartilhado pelo cluster

Em cada cluster `g`, o canal sorteia `ε_g ~ Beta(0,10·κ; 0,90·κ)`. Com probabilidade `ε_g`, uma leitura observada é substituída por um sorteio uniforme dos quatro estados. As oito sessões de um cluster compartilham esse `ε_g`; condicionalmente a ele, as sessões são binomiais.

- `κ = 9`: cenário de correlação moderada; no nulo de fronteira, ICC exato de sessão `1/(κ+1) = 0,10`.
- `κ = 4`: cenário de estresse; ICC exato `0,20`.

No alternativo, os ICCs efetivos medidos por endpoint são menores ou maiores conforme a variância de `ε_g` atravessa a probabilidade do mecanismo; o JSON conserva os três valores por cenário. Sessões quase idênticas de um mesmo texto **nunca** entram no denominador como independentes.

### 2.4 Nulo de fronteira e negativo com poder

Para cada endpoint, o evento-alvo é:

1. **A:** P-A observa `s` nos ciclos 3 e 4;
2. **B-out:** depois do empurrão para fora, o ciclo 4 observa `s`;
3. **B-in:** depois do empurrão dentro do Nome, o ciclo 4 observa `t`.

O nulo conservador é o mecanismo **sem estado relevante na fronteira uniforme de quatro estados**: para cada endpoint, a probabilidade marginal do evento-alvo é `p0 = 0,25`, com propensão `q_g ~ Beta(0,25·κ; 0,75·κ)` por cluster. Os adversários determinísticos já validados ficam abaixo dessa fronteira no evento-alvo que os separa: a cópia não retorna de `y`, e âncora/moda/ignorar não preservam `t`; acidentes de observação podem produzir o alvo com probabilidade no máximo uniforme.

A região alternativa operacional exige média pelo menos `p_min = 0,60`. O desenho é fail-closed:

- **Positivo discreto:** os três limites inferiores superam `0,25` e nenhum endpoint falha o teste negativo.
- **FALSIFIED operacional:** com integridade válida e poder atingido, pelo menos um limite superior cai abaixo de `0,60`.
- **INCONCLUSIVE:** os intervalos cruzam as fronteiras, a integridade falha, a isca é endossada, o extrator contradiz a fórmula ou não há clusters suficientes.
- O negativo é sobre a previsão operacional R4 neste instrumento; não é refutação da teoria.

## 3. Inferência: cluster é a unidade

Cada cluster é um texto ou um isomorfo distinto, com dicionário/geração independente e verificação de contaminação. Sessões do mesmo cluster são medidas repetidas correlacionadas. A estatística usa `G` médias de cluster; `G×8` sessões não é o tamanho amostral.

Para o endpoint `j`, seja `u_gj` a proporção de sucessos nas oito sessões do cluster `g`. O teste positivo é t de uma amostra contra `p0 = 0,25`; o negativo testa contra `p_min = 0,60`. O desenho fixo usa Bonferroni `α/3` por endpoint. O positivo exige as três rejeições; o negativo tem precedência.

- `α₅% = 0,05`; por endpoint, `0,0166667`.
- `α₅σ = norm.sf(5) = 2,866515718791933×10⁻⁷`; por endpoint, `9,55505239597311×10⁻⁸`.
- A variante sequencial usa cinco olhadas fixas `[4, 8, 12, 16, 20]` clusters e Bonferroni `α/(3×5)` por endpoint/olhada. Para no primeiro negativo ou no primeiro positivo conjunto; se chegar a 20 sem decisão, é `UNDERPOWERED/INCONCLUSIVE`.

Nenhum desenho é escolhido aqui. As três variantes ficam lado a lado.

## 4. Variante fixa a 5 %

Critério de busca: poder positivo ≥ 0,90, poder do negativo ≥ 0,90 e falso `FALSIFIED` sob alternativa ≤ 0,05. A grade começou em 8, 12, 16, 24, 32, 48, 64, 96, 128, 192 e 256 clusters; o menor ponto aprovado foi refinado de dois em dois e reavaliado em outra semente com 30.000 réplicas.

| ICC nulo | τ | clusters | sessões | tamanho sob nulo | CP95 | poder positivo | poder do negativo | falso FALSIFIED |
|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 0,10 | 0,25 | 8 | 64 | 0,0000667 | [0,0000081; 0,0002408] | 0,9635 | 0,9959 | 0,0151 |
| 0,10 | 0,50 | 6 | 48 | 0 | [0; 0,0001230] | 0,9951 | 0,9675 | 0 |
| 0,10 | 1,00 | 6 | 48 | 0,0000667 | [0,0000081; 0,0002408] | 0,9977 | 0,9677 | 0 |
| 0,20 | 0,25 | 8 | 64 | 0,0002333 | [0,0000938; 0,0004807] | 0,9484 | 0,9565 | 0,0122 |
| 0,20 | 0,50 | 8 | 64 | 0,0004667 | [0,0002552; 0,0007829] | 0,9989 | 0,9583 | 0 |
| 0,20 | 1,00 | 8 | 64 | 0,0005000 | [0,0002799; 0,0008245] | 0,9993 | 0,9553 | 0 |

O tamanho conjunto é conservador porque o positivo exige os três endpoints e o negativo tem precedência. O limite superior CP95 continua abaixo de 0,001 em todos os cenários.

## 5. Variante fixa a 5σ

| ICC nulo | τ | clusters | sessões | tamanho observado | CP95 do tamanho | poder positivo | poder do negativo | falso FALSIFIED |
|---:|---:|---:|---:|---:|---|---:|---:|---:|
| 0,10 | 0,25 | 26 | 208 | 0 | [0; 0,0001230] | 0,9297 | 0,9797 | 0 |
| 0,10 | 0,50 | 24 | 192 | 0 | [0; 0,0001230] | 0,99997 | 0,9517 | 0 |
| 0,10 | 1,00 | 24 | 192 | 0 | [0; 0,0001230] | 1,00000 | 0,9516 | 0 |
| 0,20 | 0,25 | 30 | 240 | 0 | [0; 0,0001230] | 0,9666 | 0,9248 | 0 |
| 0,20 | 0,50 | 30 | 240 | 0 | [0; 0,0001230] | 1,00000 | 0,9239 | 0 |
| 0,20 | 1,00 | 30 | 240 | 0 | [0; 0,0001230] | 1,00000 | 0,9250 | 0 |

**Bloqueio de cauda:** 30.000 réplicas não resolvem `2,87×10⁻⁷`. Zero rejeição nesse número de réplicas só dá CP95 superior `1,23×10⁻⁴`, cerca de 429 vezes o alvo 5σ. Portanto os `G` acima mostram poder condicional do procedimento, não validam o tamanho 5σ. Um desenho 5σ de produção precisa de validação analítica da cauda ou de um número de réplicas de outra ordem; não recebe selo por “zero observado”.

## 6. Variante sequencial a 5 % com parada pré-registrada

A regra é única: olhadas `[4, 8, 12, 16, 20]`; `α/(3×5)` por teste; para se um endpoint falha o limite de `0,60` (`FALSIFIED`) ou se os três superam `0,25` sem falha (`positivo discreto`); o negativo tem precedência; chegar a 20 sem decisão é `UNDERPOWERED/INCONCLUSIVE`.

| ICC nulo | τ | máximo | E[clusters] sob alternativa | tamanho sob nulo | poder positivo | poder do negativo | falso FALSIFIED | sem decisão no máximo |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,10 | 0,25 | 20 | 7,9712 | 0 | 0,9930 | 1,0000 | 0,0070 | 0 |
| 0,10 | 0,50 | 20 | 5,8029 | 0 | 1,0000 | 1,0000 | 0 | 0 |
| 0,10 | 1,00 | 20 | 5,4284 | 0 | 1,0000 | 1,0000 | 0 | 0 |
| 0,20 | 0,25 | 20 | 8,2352 | 0,0000333 | 0,9940 | 0,99983 | 0,00597 | 0 |
| 0,20 | 0,50 | 20 | 6,0692 | 0,0002000 | 0,99997 | 0,99970 | 0,0000333 | 0 |
| 0,20 | 1,00 | 20 | 5,7551 | 0,0000333 | 1,0000 | 0,99973 | 0 | 0 |

O sequencial reduz o custo esperado no modelo sintético, mas não elimina o bloqueio: quatro clusters disponíveis não são um corpus validado, e a primeira olhada em 4 clusters não libera execução sem fórmula, extrator, isomorfos e integridade validados.

## 7. Custo em tokens de fonte

O custo usa o tokenizador de referência local **Qwen/Qwen3.6-35B-A3B**, lido somente de `tokenizer.json` por `tokenizers` 0.21.4; nenhum peso ou modelo é carregado. O hash do tokenizador é `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42`, e o artigo inteiro de controle reproduz **412.784 tokens**. O fallback byte=token ficou preservado em `REV1` e não orienta o desenho. [MEDIDAS_ENTRADA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Ckimi%5CK08%5CENTRADA%5CMEDIDAS_ENTRADA.md&line=3&text=Tokenizador%20de%20refer%C3%AAncia%20local "citation")

Uma sessão-análise primária contém cinco diálogos independentes: P-A, P-B fora, P-B dentro, P-D e P-C. A fonte entra uma vez em cada diálogo da fonte; o controle P-C entra uma vez. Assim:

\[
T_{\text{sessão}}=4T_{\mathrm{ref}}+T_{PC,\mathrm{ref}}.
\]

| recorte | `T_ref` | `T_PC,ref` | tokens de fonte por sessão |
|---|---:|---:|---:|
| ABSTRACT | 789 | 804 | 3.960 |
| READ_BRIEF | 4.072 | 4.087 | 20.375 |
| LLMS | 3.926 | 3.941 | 19.645 |
| README | 7.358 | 7.373 | 36.805 |

Os totais abaixo usam `READ_BRIEF` como referência de conta porque suas medidas foram ratificadas nesta frente; não são um orçamento de corpus misto. A fórmula geral é `Σ_g 8_g·(4T_ref,g + T_PC,ref,g)`.

| desenho | cenário | clusters | sessões | tokens de fonte, referência READ_BRIEF |
|---|---|---:|---:|---:|
| fixo 5 % | τ=0,25; ICC=0,10 | 8 | 64 | 1.304.000 |
| fixo 5 % | τ≥0,50; ICC=0,10 | 6 | 48 | 978.000 |
| fixo 5 % | ICC=0,20 | 8 | 64 | 1.304.000 |
| fixo 5σ | τ=0,25; ICC=0,10 | 26 | 208 | 4.238.000 |
| fixo 5σ | τ≥0,50; ICC=0,10 | 24 | 192 | 3.912.000 |
| fixo 5σ | ICC=0,20 | 30 | 240 | 4.890.000 |
| sequencial 5 % | todos | máximo 20 | máximo 160 | máximo 3.260.000 |
| sequencial 5 % | τ=0,25; ICC=0,10 | esperado 7,9712 | esperado 63,7696 | esperado 1.299.306 |
| sequencial 5 % | τ=0,50; ICC=0,10 | esperado 5,8029 | esperado 46,4235 | esperado 945.878 |
| sequencial 5 % | τ=1,00; ICC=0,10 | esperado 5,4284 | esperado 43,4272 | esperado 884.829 |
| sequencial 5 % | τ=0,25; ICC=0,20 | esperado 8,2352 | esperado 65,8816 | esperado 1.342.338 |
| sequencial 5 % | τ=0,50; ICC=0,20 | esperado 6,0692 | esperado 48,5536 | esperado 989.280 |
| sequencial 5 % | τ=1,00; ICC=0,20 | esperado 5,7551 | esperado 46,0405 | esperado 938.076 |

Diagnóstico com fita presente no núcleo reduzido de quatro ciclos custa `4T_ref` se a fita entrar nos quatro ciclos; para `READ_BRIEF`, 16.288 tokens, incremento de 12.216 sobre uma fita. No protocolo completo de 27 ciclos de P-A, a fita em cada ciclo custaria 109.944 tokens de fonte para `READ_BRIEF`; a regra primária não permite isso.

## 8. O que este poder não fecha

1. **Projetor com fita.** As cotas de resolução, o retorno e a permanência são superiores; o projetor os cumpre com distância zero. Perfil exponencial e memória do componente seriam as assinaturas, mas a ponte para medir amplitude e o braço com fita ainda não estão validados. A reivindicação de separação plena para aqui. [REVISAO_CANDIDATA_CAMADA_CIENTIFICA](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv412%5Crevisao%5CREVISAO_CANDIDATA_CAMADA_CIENTIFICA.md&line=171&text=Um%20leitor%20SEM%20mem%C3%B3ria%20que%20rel%C3%AA%20o%20texto-fonte "citation")
2. **Perfil da trava.** O pacote binário não mede `e^{-τc}` nem `jamais_esgotado`.
3. **Distância mínima.** Todas as fórmulas têm distância mínima 1 pela variável livre PT/EN; o adendo de distância 3 não se aplica.
4. **Produção.** Não há saídas reais validadas, equivalência de dificuldade, léxico ratificado, modelos/tokenizers, corpus de clusters, cauda 5σ validada ou ratificação.
5. **Integridade.** O poder é condicional a integridade válida. Formato, isca, extrator, contaminação, empurrão sem efeito ou inconsistência lógica produzem `INCONCLUSIVE_*`, nunca `FALSIFIED`.

## 9. Conclusão operacional

No modelo sintético, o pacote discreto alcança pelo menos 0,90 de poder positivo e do negativo com 6–8 clusters a 5 %, 24–30 clusters a 5σ operacional e máximo 20 clusters no sequencial. Como só existem quatro recortes candidatos e nenhum corpus de isomorfos independentes ratificado, **o desenho real disponível não alcança o poder necessário**. O instrumento R4 permanece bloqueado; estes números são uma conta de desenho e uma prova de fiação estatística, não evidência empírica.

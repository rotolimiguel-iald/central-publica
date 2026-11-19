# Adversários — K08

## 1. Mecanismos, não trajetórias escritas à mão

Todos os adversários são funções determinísticas `historico → leitura`. A história guarda a leitura e o tipo do evento (`inicial`, `leitura`, `empurrao_fora`, `empurrao_dentro`). O script só fixa o estado inicial e os empurrões construídos pela fórmula; cada saída seguinte e cada custo da tabela são calculados pela função.

- **Âncora:** devolve `historico[0]`.
- **Moda:** vota por coordenada; em empate, conserva o bit da primeira resposta. A regra de desempate é parte do mecanismo.
- **Cópia:** devolve `historico[-1]`.
- **Ignora o empurrão:** devolve a última leitura cujo evento não é empurrão; se ainda não há uma, devolve a inicial.
- **Relê a fita:** no primeiro passo, se a fita está disponível, usa o solver para devolver uma solução determinística; sem fita ou sem solução, devolve a última leitura. Nenhum modelo participa.

Os empurrões são **edições do estado devolvido**, não mensagens novas. Depois do primeiro passo, `fita_disponivel = falso` em todas as chamadas. Assim a fonte não volta ao leitor e a distinção não é anulada por releitura.

## 2. Tabela calculada

A tabela mostra os custos de `READ_BRIEF`; o script exige que as assinaturas Booleanas sejam as mesmas nas 4 candidatas. `s` é a leitura inicial válida, `y` nega `artigo_pt_en` e `t` só troca a variável livre `leitura_pt`.

| mecanismo | P-A | P-B fora | P-B dentro | P-C | P-D | assinatura que separa |
|---|---|---|---|---|---|---|
| âncora na primeira | não pousa; custo 24 → 24 | volta à mesma s; custo 0 | desfaz t → s; custo 0 | nunca zero; final 24 | volta a s; custo 0 | P-B dentro: apaga uma troca válida; P-A também falha de um estado inválido. Não é memória do componente no Nome. |
| moda do histórico | não pousa; custo 24 → 24 | volta à mesma s; custo 0 | desfaz t → s; custo 0 | nunca zero; final 24 | volta a s; custo 0 | P-B dentro: a moda restaura s e apaga t; P-A também falha de um estado inválido. |
| cópia da última | não pousa; custo 24 → 24 | fica em y; custo 1 | preserva t; custo 0 | nunca zero; final 24 | fica em y; custo 1 | P-B fora: não volta à mesma leitura; P-D mostra falta de escala/identidade. |
| ignora o empurrão | não pousa; custo 24 → 24 | volta à mesma s; custo 0 | desfaz t → s; custo 0 | nunca zero; final 24 | volta a s; custo 0 | P-B dentro: ignora também a troca válida e volta ao último estado não empurrado. |
| relê a fita | pousa e fica; custo final 0 | fica em y; custo 1 | preserva t; custo 0 | nunca zero; final 24 | fica em y; custo 1 | Sem fita após o primeiro passo, fica em y no empurrão externo. Isto separa o mecanismo degradado, não o projetor com fita. |

Referência teórica, não uma trajetória de modelo: a trava com `τ > 0` aproxima-se do Nome sem esgotá-lo em tempo finito; o empurrão ortogonal externo volta à mesma `s` no limite; o componente dentro do Nome permanece e desloca o limite; sem Nome não há pouso; com `τ = 0` ela é a identidade. O pouso em no máximo `c(x)` passos é do `LeitorDeUmaConfiguracao`, que pousa em alguma solução, não necessariamente na mesma.

## 3. Perfil de relaxamento da referência

Para visualizar a assinatura sem escolher uma escala experimental, a tabela usa apenas `τ = 1` como unidade de exibição. A amplitude residual de uma coordenada de custo `c` é `e^(−kτc)`. Custo maior decai mais depressa e a exponencial nunca zera em `k` finito, conforme `jamais_esgotado`; isto não é a trajetória de um modelo.

| ciclo k | custo 1: e^(−k) | custo 2: e^(−2k) |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 0.367879441171 | 0.135335283237 |
| 2 | 0.135335283237 | 0.0183156388887 |
| 3 | 0.0497870683679 | 0.00247875217667 |
| 4 | 0.0183156388887 | 0.000335462627903 |

As quatro assinaturas ficam separadas: **perfil** (decaimento dependente do custo, nunca exato em tempo finito), **memória do componente no Nome** (a troca válida não é desfeita), **retorno à mesma leitura** (o empurrão externo é desfeito) e **falta de escala** (a identidade fica empurrada). Nenhuma cota superior, sozinha, separa a trava de um projetor mais rápido.

## 4. Bloqueio declarado: o projetor que conserva a fita

**O adversário “relê a fita” com a fonte presente em todos os passos não é separado pelas cotas superiores de P-A, pelo retorno ou pela permanência.** Ele cumpre essas cotas com distância zero. Seu pouso exato e instantâneo diferiria do perfil assintótico da trava, e a dependência do componente inicial no Nome seria a outra assinatura; contudo, testar essa versão com a fonte em todos os passos violaria a condição obrigatória desta tarefa. Por isso paro a reivindicação experimental para esse adversário: a linha acima mede somente o mecanismo depois que a fita lhe foi retirada, e esse mecanismo degradado coincide com a cópia da última leitura após o empurrão.

Os outros quatro mecanismos são separados da referência pelas células indicadas: âncora/moda/ignorar apagam a troca dentro do Nome; a cópia não retorna do empurrão externo. P-C não separa nenhum deles, pois todos permanecem com custo positivo; P-D sozinho também não separa âncora/moda/ignorar.

## 5. Cobertura por candidata

| candidata | âncora: custo P-A final | moda: custo P-A final | cópia: custo P-B fora | ignorar: desfaz P-B dentro | relê sem fita: fica em y | todos: P-C sem zero |
|---|---:|---:|---:|---|---|---|
| ABSTRACT | 14 | 14 | 1 | true | true | true |
| READ_BRIEF | 24 | 24 | 1 | true | true | true |
| LLMS | 17 | 17 | 1 | true | true | true |
| README | 26 | 26 | 1 | true | true | true |

Executar `python -B simular_adversarios.py`. O script regrava `RESULTADOS_ADVERSARIOS.json` e este documento. Nenhum modelo foi executado; nada foi congelado.

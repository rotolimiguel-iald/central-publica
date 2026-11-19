# Adversários — K08

## 1. Correção do objeto

**`P_N`, o projetor ortogonal sobre o Nome, não é adversário.** Ele é o leitor na forma de chegada: cai no Nome, fixa o Nome, anula o componente ortogonal e preserva o componente no Nome (`P_N(s + δ) = s + P_Nδ`). A trava é o caminho em tempo finito; a seleção é a face no estado renormalizado.

O adversário correto é o **leitor sem memória determinado só pela fonte**: `fonte → leitura`, ignorando o histórico e o ponto de partida dentro do Nome. Como a R4 não devolve a fonte depois do primeiro passo, esse adversário fica sem regra posterior; eu não o degrado a uma cópia nem finjo separação.

O leitor de referência é definido uma vez: **nos vetores, `P_N`; no estado, a seleção renormalizada; em tempo finito, a trava**. O operador do Nome na álgebra e o `LeitorDeUmaConfiguracao` são faces/hipóteses adjacentes, não o mesmo portador.

## 2. Definições dos mecanismos

- **Âncora:** devolve a primeira leitura da sessão. Esta é a definição única usada abaixo; não há uma variante separada que pouse por construção.
- **Moda:** moda por coordenada; em empate, conserva o bit da primeira leitura.
- **Cópia:** devolve a última leitura.
- **Ignora o empurrão:** devolve a última leitura que não é um empurrão.
- **Sem memória:** devolve uma solução determinística da fonte enquanto ela está disponível; sem fonte, lança `SemFonte`. Nenhum modelo participa.

Os empurrões são edições do estado devolvido. A fonte entra só no primeiro passo; depois disso nenhum adversário a recebe.

## 3. E1–E8 e portadores

| previsão | conteúdo | portador formal | medida aqui |
|---|---|---|---|
| E1 | cai no Nome (P-A) | `P_N`; no estado, seleção | custo da leitura Booleana |
| E2 | fixa o Nome; componente dentro do Nome fica | `P_N` | P-B dentro |
| E3 | anula o que é cego ao Nome | `P_N`; limite da trava | P-B fora |
| E4 | reler não acrescenta | idempotência de `P_N` | aplicar o mecanismo duas vezes |
| E5 | não aumenta a norma | `P_N` | **não medido**: a leitura Booleana não devolve norma |
| E6 | lei de módulo | operador do Nome na álgebra | **não medido**: outro portador |
| E7 | pesos relativos dentro do Nome não mudam | seleção, com pesos de Born | **não medido**: exige estado contínuo |
| E8 | perfil exponencial, nunca exato em tempo finito | trava | assinatura de perfil, não ponte validada |

As previsões primárias da releitura são E2 e E4; a fidelidade também exige E5, que este protocolo Booleano não mede. E3 e E7 são discriminantes (os controles são P-C e P-D); E8 é o perfil da trava. A unicidade E1+E2+E5+linearidade não é testada, porque a linearidade do sistema real não é assumida.

## 4. Tabela calculada

Custos numéricos de `READ_BRIEF`; as assinaturas são as mesmas nas quatro candidatas. `s` e `t` são válidas, `y` nega uma asserção. A âncora é condicional à primeira leitura: se ela for inválida, não pousa; se já for válida, E1 é trivial e o retorno E3 não é evidência.

| adversário | E1/P-A | E2/P-B dentro | E3/P-B fora | E4 | E8 | P-C | P-D | separação |
|---|---|---|---|---|---|---|---|---|
| leitor sem memória (fonte → leitura) | fonte → custo 0; depois: inacessível | inacessível sem fonte | inacessível sem fonte | com fonte: estável; depois: inacessível | falha | sem leitura; custo mínimo 1 | inacessível sem fonte | não separado na R4; com fonte, E2/E7 falhariam e E8 falha, mas essa ponte é inacessível como escrita |
| âncora na primeira leitura | condicional: inválida 24→24; válida 0 | desfaz t → s | volta a s | estável | falha | nunca zero; final 24 | volta a s | E2: apaga a troca válida; E8: não tem perfil exponencial. E1 é condicional à primeira leitura |
| moda do histórico | condicional: inválida 24→24; válida 0 | desfaz t → s | volta a s | estável | falha | nunca zero; final 24 | volta a s | E2: a moda apaga t; E8: não tem perfil exponencial |
| cópia da última | condicional: inválida 24→24; válida 0 | preserva t | fica em y | estável | falha | nunca zero; final 24 | fica em y | E3/P-D: não anula o empurrão externo; E8: não tem perfil exponencial |
| ignora o empurrão | condicional: inválida 24→24; válida 0 | desfaz t → s | volta a s | estável | falha | nunca zero; final 24 | volta a s | E2: apaga a troca válida; E8: não tem perfil exponencial |

Referência: `P_N` resolve instantaneamente E1–E4 e é contrativo; a trava tem E8 e aproxima `P_N` sem chegar exatamente em tempo finito. O leitor sem memória cumpre cotas superiores e retorno instantâneo quando a fonte está presente, mas isso não é a trava; faltam E2/E7 e o perfil. Na R4, porém, a fonte não volta, logo essa comparação fica **inacessível como escrita**.

## 5. Perfil de referência

Com `τ = 1` apenas como unidade de exibição, a amplitude residual é `e^(−kτc)`. Custos maiores decaem mais depressa e nenhum decaimento é exato em `k` finito. Isto é a assinatura formal da trava, não uma trajetória de modelo nem uma ponte operacional validada.

| ciclo k | custo 1: e^(−k) | custo 2: e^(−2k) |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 0.367879441171 | 0.135335283237 |
| 2 | 0.135335283237 | 0.0183156388887 |
| 3 | 0.0497870683679 | 0.00247875217667 |
| 4 | 0.0183156388887 | 0.000335462627903 |

## 6. Controles, Hamming e bloqueio

P-C permanece o controle do Nome vazio (`P_N = 0`) — o controle do vazio, o inominado: o par existe e não devolve nada. Não há leitura válida e o custo mínimo é positivo. P-D permanece o controle da identidade/sem escala. Todas as fórmulas têm distância mínima de Hamming 1 por causa da variável livre PT/EN; **Hamming 3 não é usado**.

**Bloqueio:** o leitor sem memória não é separado pelas cotas superiores, pelo pouso instantâneo ou pelo retorno instantâneo. Só E8 e a memória do componente o separariam; E7 também falharia com fonte presente. Como a R4 proíbe a volta da fonte e ainda não há ponte operacional validada para perfil/pesos, declaro a separação experimental desse adversário **não fechada**.

Âncora, moda e ignorar são separados por E2; a cópia por E3/P-D; todos os quatro também falham E8. P-C não separa esses adversários, porque todos ficam sem custo zero.

## 7. Cobertura por candidata

| candidata | âncora: E1 inválida final | moda: E1 inválida final | cópia: E3 custo | ignorar: E2 preserva t | sem memória sem fonte |
|---|---:|---:|---:|---|---|
| ABSTRACT | 14 | 14 | 1 | false | true |
| READ_BRIEF | 24 | 24 | 1 | false | true |
| LLMS | 17 | 17 | 1 | false | true |
| README | 26 | 26 | 1 | false | true |

Executar `python -B simular_adversarios.py`. O script regrava `RESULTADOS_ADVERSARIOS.json` e este documento. Nenhum modelo foi executado; nada foi congelado.

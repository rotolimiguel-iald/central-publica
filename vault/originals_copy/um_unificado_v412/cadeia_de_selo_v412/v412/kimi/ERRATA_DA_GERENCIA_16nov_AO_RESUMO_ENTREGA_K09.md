# Errata da gerência, ao lado do resumo `ENTREGA_K09.md` (segunda versão)

> Gerência c1, 16/11/2026, em nome próprio. Este arquivo é da gerência e fica AO LADO do resumo do Kimi;
> o `ENTREGA_K09.md` não foi tocado (sha256 lido por ferramenta nesta data:
> `5ddb386946db911bfc1b26261fd5312586a3852449646dd58e643b9630edf73a`).
> A primeira versão desta errata (guardada em `revisao\REV0_errata_gerencia_k09\`) foi a conferência distinta em
> 16/11 e voltou com um achado alto e quatro médios (relatório `revisao\REVISAO_16nov_R1_C3-…`); esta os conserta e
> ainda não foi relida por terceiro.
> Motivo da errata: a conferência de 15/11 (relatórios `revisao\REVISAO_EXAME_15nov_Q2-…` e `…Q3-…`) achou dois
> defeitos altos nesse resumo, que a `ENTREGA_K10.md` dá por corrigido ao lado; a própria
> `ERRATA_K10_HUBBLE_COMBINACAO.md` (o que ficou aberto, item 1) diz que as linhas 3, 8, 14 e 28 não foram editadas
> e que o transporte é da gerência.
> Nenhum dado aberto, nenhum modelo rodado, nada selado; o gate não se move.

## Como ler o `ENTREGA_K09.md` a partir de hoje

O arquivo de hoje é o resumo da rodada 3 **já editado pelo Kimi na rodada 4** em sete linhas (3, 4, 10, 18, 20, 24 e
28); os bytes da rodada 3 estão em `K04\M2\REV4\ENTREGA_K09.md`. Onde ele diverge do que segue, vale o que segue, e a
fonte é a rodada 4 (`PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md`, `ERRATA_K10_PRE_REGISTRO.md`,
`ERRATA_K10_HUBBLE_COMBINACAO.md`, `ERRATA_K10_M2.md`, `VALIDACAO_K10_15nov.json`). A rodada 4 foi aprovada **com
ressalvas** pelos revisores Q2 e Q3; onde eles corrigiram a redação dela, vale a correção, dita abaixo.

| linha do resumo | o que ela diz | o que vale |
|---|---|---|
| 4 | o rascunho K09 do pré-registro está “pronto para a gerência ler ao operador” | **Não está pronto.** O rascunho K09 foi superado pelo rascunho K10, que é rascunho com bloqueios: não selado, sem gatilho, sem prazo-limite e sem plano B fixados (K10, seção 0.3). |
| 4 e 24 | o observável é o número do JUNO público “pela primeira vez depois de 08/08/2026 e antes de qualquer acesso do selo” | **A chave da cegueira mudou.** O que blinda é a PRIMEIRA APARIÇÃO PÚBLICA do número, posterior à previsão publicada (17/02/2026) E ao selo do próprio pré-registro, com carimbo fora da casa (K10, seção 1.1). São três marcos: a previsão publicada, o pino da regra antiga (08/08/2026) e o selo do pré-registro, que ainda não existe. O artigo de 207,2 dias (29/09/2026) repete um número que já era público antes do pino (22/06/2026, data declarada no JSON da errata do neutrino); nem ele nem o SK-Gd servem de observável cego deste pré-registro, porque são anteriores ao selo dele. Em relação à previsão publicada, os dois são posteriores. |
| 24 | o negativo atinge o pacote da escala, “não β isolado nem o gate” | **O negativo tem duas camadas, ditas juntas** (K10, seções 0.1 e 5.1): (a) as bandeiras do gate da gravidade quântica não se movem (no rito do m₂, `does_not_gate_core` é verdadeiro); (b) a regra do contorno do `um.py` selado (v314) põe a identidade do programa em falso se o rito devolver um falsificado limpo. Se a regra do contorno vale para o veredito do incremento é decisão do operador. O negativo falsifica a conjunção β·sen 45°·u com m₁ ≈ 0 no ordenamento normal, sem separar os fatores (a identificação com sen 45° segue marcada como leitura do autor); não se escreve “não β isolado” como se β ficasse de fora; ajustar u ou o ângulo depois não reverte o veredito. O erro “não atinge o gate” nasceu no desenho da gerência (seção 4.3 do desenho da v412) e já foi dito em nome próprio no Mapa. |
| 24 | “revisor independente abre uma única vez” | **Quem nomeia o revisor de abertura é decisão do operador**; o veredito roda por script pinado por hash; o construtor não abre (K10, seção 6, itens 5 a 7, tudo como proposta). |
| 24 | a classe “preliminar” “é ratificada pelo operador” | Lê-se como **pendente**: a ratificação da classe ainda não foi feita (K10, seção 9, escolha E3). |
| 3 e 14 | a lei da face dos cronômetros segue “pendente (poder prévio 2,33σ)” | **São duas frases, não uma** (`ERRATA_K10_HUBBLE_COMBINACAO.md`, linha 1 da tabela): (a) a leitura intermediária dos cronômetros JÁ foi lida na Fase 7 (−1,66σ com Moresco 2020; −1,54σ com todos); o poder prévio DESSA leitura é 2,33σ, abaixo de 5; (b) a lei do lado transmitido está pendente: não escrita, sem cobrança, sem poder dito. O 2,33σ nunca se liga à lei pendente. |
| 6 | “o DESI DR3 está respondido (fundo, não testemunha)” | É **proposta**: tratar como fundo até cumprir as cinco condições; a decisão é da gerência e do operador (mesma errata, linha 11). |
| 8 e 28 | “2.162 dias vivos; poder 90,5 %”; “a combinação não antecipa nada” | **Sem piso** (brinquedo): 2.162 dias com pesos iguais, 1.806 com pesos proporcionais. **Com o piso do m₂** (hipótese tirada de dois pontos, sem grau de liberdade) a combinação não chega a 5,0 nem a D90 em nenhuma das duas regras. A frase inteira: 2034 é o fim do levantamento do SO; a combinação poupa dias vivos do ramo JUNO, mas a data é travada pelo SO, e o JUNO sozinho chega antes no cenário ideal. |
| 8 | ringdown: “D10 satura ≈ 5,8”; “8,7 meses e 16,6 meses” | A saturação 5,805 é para a C2 ampla; os 8,7 e 16,6 meses são sem viés; os portões 5,0 e D90 = 6,28 ficam lado a lado, e a escolha entre eles é do operador. O portão só muda o ringdown; a combinação com o piso não chega a nenhum dos dois. |
| 20 | “P ≈ 65 %” e “P ≈ 99,7 %” | Cada número vale num mundo: o primeiro se o valor verdadeiro for o centro público de hoje; o segundo se a previsão for verdadeira. Nenhum é probabilidade sem condição. |
| 28 | “teto de 16 rotas Hubble” | 16 são as rotas com o prefixo de Hubble **que também olharam dado** (só pelo prefixo são 30); há rotas de Hubble fora do prefixo; o único teto é 123. |
| 28 | a partição e o p da ressalva 7 | Vão ao operador como alternativas a ratificar depois da leitura; os limiares dependem da partição **e da base**. |
| 10 e 49 | a proposta `REGISTRO_MAPA_K09.json`, que “a gerência registra após conferir” | **Não se registra como está**: a conferência mostrou que registrá-la trocaria o estatuto da rota. O que a gerência registrou no Mapa foi o resultado da conferência, por anotação. |
| tabela de hashes | dez arquivos com hash | **É histórica.** Nove dos dez hashes já não batem com o disco (conferido por script nesta data); só o do rascunho K09 do pré-registro bate. Os hashes que valem são os de `VALIDACAO_K10_15nov.json`. |

## O que NÃO muda

A resposta do topo: não existe hoje teste cego de natureza, executável, com poder de desenho de 5σ; é parede
medida. A cronologia do neutrino nos dois eixos. As duas regras A e B lado a lado, sem escolha. Nenhum teste foi
executado e nenhuma abertura foi feita. `NOT_FALSIFIED` não é `CONFIRMED`.

## O que continua pendente (do operador)

As catorze escolhas marcadas como dele na seção 9 do rascunho K10 (E1 a E14: selar ou não; a regra A, a B, ou as
duas com precedência escrita; a fonte e a classe preliminar; a métrica; o gatilho; o prazo-limite; o plano B; o
carimbo externo; a lista das segundas testemunhas; quem fixa a escada; quem nomeia quem abre; se a regra do contorno
vale para o incremento; o limiar de B; a última linha da escada), mais o portão (5,0 ou D90) e a partição com o p
da ressalva 7.

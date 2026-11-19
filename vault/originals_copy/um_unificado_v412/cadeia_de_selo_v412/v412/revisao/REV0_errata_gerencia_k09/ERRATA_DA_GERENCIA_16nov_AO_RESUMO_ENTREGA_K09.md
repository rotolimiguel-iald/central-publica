# Errata da gerência, ao lado do resumo `ENTREGA_K09.md`

> Gerência c1, 16/11/2026, em nome próprio. Este arquivo é da gerência e fica AO LADO do resumo do Kimi;
> o `ENTREGA_K09.md` não foi tocado (sha256 lido por ferramenta nesta data:
> `5ddb386946db911bfc1b26261fd5312586a3852449646dd58e643b9630edf73a`).
> Motivo: a conferência distinta de 15/11 (relatórios `revisao\REVISAO_EXAME_15nov_Q2-…` e `…Q3-…`) achou dois
> defeitos altos nesse resumo, que a `ENTREGA_K10.md` dá por corrigido ao lado; a própria
> `ERRATA_K10_HUBBLE_COMBINACAO.md` (seção do que ficou aberto, item 1) diz que as linhas 3, 8, 14 e 28 não foram
> editadas e que o transporte é da gerência. É este.
> Nenhum dado aberto, nenhum modelo rodado, nada selado; o gate não se move.

## Como ler o `ENTREGA_K09.md` a partir de hoje

O resumo vale como registro da rodada 3. Onde ele diverge do que segue, vale o que segue, e a fonte é a rodada 4
(`PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K10.md`, `ERRATA_K10_PRE_REGISTRO.md`, `ERRATA_K10_HUBBLE_COMBINACAO.md`,
`ERRATA_K10_M2.md`, `VALIDACAO_K10_15nov.json`).

| linha do resumo | o que ela diz | o que vale |
|---|---|---|
| 4 | o rascunho K09 do pré-registro está “pronto para a gerência ler ao operador” | **Não está pronto.** O rascunho K09 foi superado pelo rascunho K10, que é rascunho com bloqueios: não selado, sem gatilho, sem prazo-limite e sem plano B fixados (K10, seção 0.3). A palavra “pronto” não se usa sobre ele. |
| 4 e 24 | o observável é o número do JUNO público “pela primeira vez depois de 08/08/2026 e antes de qualquer acesso do selo” | **A chave da cegueira mudou.** O que blinda é a PRIMEIRA APARIÇÃO PÚBLICA do número, posterior à previsão publicada (17/02/2026) E ao selo do próprio pré-registro, com carimbo fora da casa (K10, seção 1.1). São três marcos, não dois: a previsão publicada, o pino da regra antiga (08/08/2026) e o selo do pré-registro, que ainda não existe. O artigo de 207,2 dias e o SK-Gd já são públicos e posteriores aos dois primeiros marcos; não são cegos. |
| 24 | o negativo atinge o pacote da escala, “não β isolado nem o gate” | **O negativo tem duas camadas, e as duas se dizem juntas** (K10, seções 0.1 e 5.1): (a) as bandeiras do gate da gravidade quântica não se movem (no rito do m₂, `does_not_gate_core` é verdadeiro); (b) a regra do contorno do `um.py` selado (v314) põe a identidade do programa em falso se o rito devolver um falsificado limpo. Se a regra do contorno vale para o veredito do incremento é decisão do operador. E o negativo falsifica a conjunção β·sen 45°·u com m₁ ≈ 0, sem separar os fatores: não se escreve “não β isolado” como se β ficasse de fora; ajustar u ou o ângulo depois não reverte o veredito. O erro “não atinge o gate” nasceu no desenho da gerência (seção 4.3 do desenho da v412) e já foi dito em nome próprio no Mapa. |
| 24 | “revisor independente abre uma única vez” | **Quem nomeia o revisor de abertura é decisão do operador**; o veredito roda por script pinado por hash; o construtor não abre (K10, seção 6, itens 5 a 7, tudo como proposta). |
| 3 e 14 | a lei da face dos cronômetros segue “pendente (poder prévio 2,33σ)” | **São duas frases, não uma** (`ERRATA_K10_HUBBLE_COMBINACAO.md`, linha 1 da tabela): (a) a leitura intermediária dos cronômetros JÁ foi lida na Fase 7 (−1,66σ com Moresco 2020; −1,54σ com todos); o poder prévio DESSA leitura é 2,33σ, abaixo de 5; (b) a lei do lado transmitido está pendente: não escrita, sem cobrança, sem poder dito. O 2,33σ nunca se liga à lei pendente. |
| 6 | “o DESI DR3 está respondido (fundo, não testemunha)” | É **proposta**: tratar como fundo até cumprir as cinco condições; a decisão é da gerência e do operador (mesma errata, linha 11). |
| 8 | “2.162 dias vivos; poder 90,5 %”; “a combinação não antecipa nada” | **Sem piso** (brinquedo): 2.162 dias com pesos iguais, 1.806 com pesos proporcionais. **Com o piso do m₂** a combinação não chega a D90 em nenhuma das duas regras (mesma errata, linha 3). E a frase inteira é: 2034 é o fim do levantamento do SO; a combinação poupa dias vivos do ramo JUNO, mas a data é travada pelo SO, e o JUNO sozinho chega antes no cenário ideal (linha 8). |
| 8 | ringdown: “D10 satura ≈ 5,8”; “8,7 meses e 16,6 meses” | A saturação 5,805 é para a C2 ampla; os 8,7 e 16,6 meses são sem viés; os portões 5,0 e D90 = 6,28 ficam lado a lado, e a escolha entre eles é do operador (linha 7). |
| 28 | “teto de 16 rotas Hubble” | 16 é a contagem pelo prefixo do nome da rota; há rotas de Hubble fora do prefixo; o único teto é 123 (linha 2). |
| 28 | a partição e o p da ressalva 7 | Vão ao operador como alternativas a ratificar depois da leitura, com os limiares que a partição impõe por construção (linhas 5 e 6). |
| tabela de hashes | sete arquivos com hash | **É histórica.** Seis dos sete hashes já não batem com o disco, porque os arquivos foram corrigidos na rodada 4. Os hashes que valem são os de `VALIDACAO_K10_15nov.json`. |

## O que NÃO muda

A resposta do topo: não existe hoje teste cego de natureza, executável, com poder de desenho de 5σ; é parede
medida. A cronologia do neutrino nos dois eixos. As duas regras A e B lado a lado, sem escolha. Nenhum teste foi
executado e nenhuma abertura foi feita. `NOT_FALSIFIED` não é `CONFIRMED`.

## O que continua pendente (do operador)

Selar ou não o pré-registro; a regra (A ou B); o gatilho; o prazo-limite; o plano B; se a regra do contorno vale
para o incremento; o portão (5,0 ou D90); a partição e o p da ressalva 7; quem abre.

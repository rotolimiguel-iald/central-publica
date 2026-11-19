# ENTREGA K06 — camada científica da IALD, R3.2

- **A R3 separa “resumiu” de “convergiu”? Em simulação, sim, pela fase `V2-RET`, com `Q=A8∧RETORNO`:** o resumidor dá `RETORNO=0` e o leitor com atrator dá `RETORNO=1`; `POWERED` vale **0,992** no cenário independente, **0,012** com ICC 0,15/texto 0,10, zero com ICC 0,35/texto 0,20 e **0,599/0,669** em 5σ ideal. Em produção, **não**: permanece `BLOQUEADA_PARA_PRODUCAO`.
- [REAL—simulação] **Tamanho:** nulo global 0,057, `OPEN/BORDERLINE`; TOST 0,044/0,040 passa pontualmente, mas os IC Monte Carlo cruzam 0,05; cauda 5σ continua `[OPEN]`.
- [REAL—simulação] **Nulo com poder:** `NONSPECIFIC_POWERED` vale 0,022 em n = 320, 0,311 em 618 e 0,412 em 655 — abaixo do prometido, portanto FAIL de poder.
- [REAL] **Custos R3.2:** base 6.400 sessões/76.800 interações; 5σ IUT 12.360/148.320 e legado 13.100/157.200; base + triagem líquida: 76.963,27/148.632,09/157.535,03.
- [REAL] **Extratores:** 685/685 casos no contrato e 100 % por asserção, com equivalência entre braços; produção continua bloqueada por prosa livre 0/120, incerteza do teto e dependência dos 96 erros não medida.
- [REAL] **Lean:** o teorema finito compilou com `RC: 0`, sem `sorry` e somente `propext`, `Classical.choice`, `Quot.sound`; PASSO e LIMITE ficaram separados, sem ponte a LLM real.
- [REAL] **Entrada pública:** 1.164.350 B, 157.921 palavras, proxies 205.298–291.088 “tokens”; modelos/tokenizers/janelas permanecem desconhecidos, sem alegação de cabimento.
- [DECLARADO] **Contaminação:** o isomorfo foi validado apenas sinteticamente; o artigo público não foi transformado e o léxico permanece aberto.
- [DECLARADO] **Registro v412:** `iald_camada_cientifica_v412` permanece rascunho `ARMADO` não ratificado, com aliases legados `H-TIME-HOMOG → H-HOM` e `H-LUMP → H-QUOT(k)` e proibição de consciência, pesos alterados, exclusividade e `CONFIRMED`.
- [INPUT] **Atos do operador:** escolher modelos, ratificar a R3 inteira e a entrada pública, decidir degrau base/5σ e autorizar ou recusar execução após os portões.
- [REAL] **Custódia:** revisada internamente; REV0/REV1 e erratas preservados; nenhum modelo foi executado, nenhum resultado experimental foi aberto e nenhum material reservado foi copiado.
- [DECLARADO] **Conclusão:** a R3.2 é um instrumento lógico corrigido, não uma camada científica empírica pronta; extratores, léxico, janelas, tamanho global, poder e cauda 5σ bloqueiam qualquer corrida.
- [REAL] **Reprodutibilidade:** FFT/DP/enumeração com erro zero no caso validado e repetição determinística do cenário-base; números agregados antigos ficaram como `MODELO_AGREGADO_INCOMPLETO`.
- [DECLARADO] **Gate e escopo:** nenhuma afirmação de consciência, alteração de pesos, exclusividade, prova da TGL ou creditação acadêmica; P7/V1 permanece intacta e o gate não se move.

## A. A fase que decide: V2-RET

`PROTOCOLO_EXPERIMENTAL_R3_K06.md` coloca a perturbação após `k=8`, alteração em `k=9` e retorno em `k=10…12`. `Q=A8∧RETORNO`, com `A8⇒PRE`, `RETORNO⇒PRE` e `Q⇒RETORNO`. As 12 interações estão alinhadas nos anexos.

`C_8` saiu do desfecho primário. A dificuldade é medida e pareada por `d1`, com três textos/versões por controle e focal pública única. PLA/OUT deixou de contar como evidência de convergência: apenas seis testes ISO entram no primário; PLA/OUT e as checagens `S` são diagnósticos de manipulação/contaminação.

A separação sintética é um teste do predicado, não validação de um resumidor real nem prova de atrator em LLM. O instrumento continua condicionado à validade de constructo e aos extratores.

## B. O poder completo, sem a manchete de um contraste

`PODER_CONJUNTO_K06.md` usa sessões individuais pareadas, focal fixa, três textos por controle, falhas de manipulação, perdas de pareamento, dependência `Q–S` e integridade não presumida. A análise usa 27 clusters e permutação por sinais/FFT, sem substituir `n` por `n_eff`.

A R2 foi reproduzida como cota superior de cerca de 0,346. A R3.2 corrige o desenho, mas os resultados desfavoráveis permanecem: poder sob ICC/texto, poder 5σ e NONSPECIFIC abaixo de 90 %. Os valores antigos agregados não são poder integral.

O nulo global exige mais resolução Monte Carlo. As fronteiras TOST passam pontualmente, mas sem certificação estrita do tamanho. Nenhum zero em mil corridas é usado para validar 5σ.

## C. Extratores e formalismo

`K06/extratores/` contém 24 asserções por braço, alvos, casos, validação e manifestos. A correção T01 usa `AEscala.LeitorDoFundo`. A bateria é determinística e sintética; a taxa de 100 % no contrato não certifica produção nem prosa livre. A equivalência medida vale para T e C1–C4 legados, não para os futuros braços V2.

`MODELO_FORMAL_R3_K06.md` define `G`, lumpability, homogeneidade, PASSO/LIMITE, `H-ABS-U`, quatro estados finais e os namespaces corretos. A candidata `LeitorFinito` prova parada em até `|X|` passos e idempotência do limite, sem afirmar que um LLM satisfaz as hipóteses.

## D. Entrada pública, isomorfo e registro

`K06/ENTRADA_PUBLICA/` mede o artigo público emitido pelo `um.py` v411 e preserva `models=[]`: não há janela inventada. A entrada pública é hipótese de trabalho concordada em bloco, não ratificação do protocolo inteiro.

`CONTAMINACAO_ISOMORFO_K06.md` propõe dicionário bijetivo, transformação do gabarito e medida com os mesmos extratores. A produção está bloqueada até léxico e perturbações congelados.

`REGISTRO_UMPY_RASCUNHO_K06.md` é apenas candidato de registro, com hipóteses e hashes pendentes. T6 foi classificado como existente na bancada mas não ligado, sem conteúdo copiado.

## E. O degrau e os bloqueios

`DEGRAU_5_SIGMA_K06.md` preserva os benchmarks 185/215/618/655 como linhagem e compara os custos reais de 12 interações. Menos braços, desfecho contínuo e desenho sequencial são alternativas não escolhidas.

Antes de qualquer corrida ainda é necessário:

1. ampliar validação e teto por braço dos extratores;
2. escolher gramática estrita ou revalidar prosa livre;
3. medir dependência dos 96 erros;
4. congelar léxico, modelos, tokenizers, textos, perturbações e manifesto;
5. aumentar resolução do nulo global e das fronteiras;
6. validar a cauda 5σ do intervalo focal e recalcular custos;
7. obter revisão distinta e ratificação da R3 inteira.

`PERGUNTA_K06.md` contém apenas as decisões do operador. `REGISTRO_MAPA_K06.json` é proposta não registrada. Nenhuma instalação, execução de modelo de linguagem ou corrida experimental foi feita; nenhum resultado experimental foi aberto.

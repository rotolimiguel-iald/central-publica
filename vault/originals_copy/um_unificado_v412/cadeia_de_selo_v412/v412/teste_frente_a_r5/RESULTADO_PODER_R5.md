# A regra de decisão e o poder do desenho R5, revisão R1 (binomial exata; nenhum modelo)

> Gerado por `poder_r5.py`. Unidade = o grupo (duas versões complementares do mesmo texto). Grupos independentes por hipótese, não medida.
> `cA` = a partir de quantos grupos certos se diz SEGUE; `cB` = até quantos se diz NÃO SEGUE. Entre os dois: LÊ EM PARTE (se cA ≤ cB) ou SEM PODER.

## Os limiares

| grupos | p0 | p1 | erro pedido | cA (SEGUE se ≥) | cB (NÃO SEGUE se ≤) | o meio | erro de dizer SEGUE a quem está em p0 | erro de dizer NÃO SEGUE a quem está em p1 |
|---|---|---|---|---|---|---|---|---|
| 4 | 0,05 | 0,90 | 1 em 100 | 3 | 1 | SEM_PODER | 4,81e-04 | 0,004 |
| 4 | 0,05 | 0,90 | 1 em 1.000 | 3 | 0 | SEM_PODER | 4,81e-04 | 1,00e-04 |
| 4 | 0,25 | 0,90 | 1 em 100 | 4 | 1 | SEM_PODER | 0,004 | 0,004 |
| 4 | 0,25 | 0,90 | 1 em 1.000 | — | 0 | SEM_PODER | — | 1,00e-04 |
| 4 | 0,05 | 0,80 | 1 em 100 | 3 | 0 | SEM_PODER | 4,81e-04 | 0,002 |
| 4 | 0,05 | 0,80 | 1 em 1.000 | 3 | — | SEM_PODER | 4,81e-04 | — |
| 4 | 0,25 | 0,80 | 1 em 100 | 4 | 0 | SEM_PODER | 0,004 | 0,002 |
| 4 | 0,25 | 0,80 | 1 em 1.000 | — | — | SEM_PODER | — | — |
| 6 | 0,05 | 0,90 | 1 em 100 | 3 | 2 | não há | 0,002 | 0,001 |
| 6 | 0,05 | 0,90 | 1 em 1.000 | 4 | 1 | SEM_PODER | 8,64e-05 | 5,50e-05 |
| 6 | 0,25 | 0,90 | 1 em 100 | 5 | 2 | SEM_PODER | 0,005 | 0,001 |
| 6 | 0,25 | 0,90 | 1 em 1.000 | 6 | 1 | SEM_PODER | 2,44e-04 | 5,50e-05 |
| 6 | 0,05 | 0,80 | 1 em 100 | 3 | 1 | SEM_PODER | 0,002 | 0,002 |
| 6 | 0,05 | 0,80 | 1 em 1.000 | 4 | 0 | SEM_PODER | 8,64e-05 | 6,40e-05 |
| 6 | 0,25 | 0,80 | 1 em 100 | 5 | 1 | SEM_PODER | 0,005 | 0,002 |
| 6 | 0,25 | 0,80 | 1 em 1.000 | 6 | 0 | SEM_PODER | 2,44e-04 | 6,40e-05 |
| 8 | 0,05 | 0,90 | 1 em 100 | 3 | 4 | LE_EM_PARTE | 0,006 | 0,005 |
| 8 | 0,05 | 0,90 | 1 em 1.000 | 4 | 3 | não há | 3,72e-04 | 4,32e-04 |
| 8 | 0,25 | 0,90 | 1 em 100 | 6 | 4 | SEM_PODER | 0,004 | 0,005 |
| 8 | 0,25 | 0,90 | 1 em 1.000 | 7 | 3 | SEM_PODER | 3,81e-04 | 4,32e-04 |
| 8 | 0,05 | 0,80 | 1 em 100 | 3 | 2 | não há | 0,006 | 0,001 |
| 8 | 0,05 | 0,80 | 1 em 1.000 | 4 | 1 | SEM_PODER | 3,72e-04 | 8,45e-05 |
| 8 | 0,25 | 0,80 | 1 em 100 | 6 | 2 | SEM_PODER | 0,004 | 0,001 |
| 8 | 0,25 | 0,80 | 1 em 1.000 | 7 | 1 | SEM_PODER | 3,81e-04 | 8,45e-05 |
| 13 | 0,05 | 0,90 | 1 em 100 | 4 | 8 | LE_EM_PARTE | 0,003 | 0,006 |
| 13 | 0,05 | 0,90 | 1 em 1.000 | 5 | 7 | LE_EM_PARTE | 2,87e-04 | 9,20e-04 |
| 13 | 0,25 | 0,90 | 1 em 100 | 8 | 8 | LE_EM_PARTE | 0,006 | 0,006 |
| 13 | 0,25 | 0,90 | 1 em 1.000 | 9 | 7 | SEM_PODER | 9,89e-04 | 9,20e-04 |
| 13 | 0,05 | 0,80 | 1 em 100 | 4 | 6 | LE_EM_PARTE | 0,003 | 0,007 |
| 13 | 0,05 | 0,80 | 1 em 1.000 | 5 | 4 | não há | 2,87e-04 | 1,66e-04 |
| 13 | 0,25 | 0,80 | 1 em 100 | 8 | 6 | SEM_PODER | 0,006 | 0,007 |
| 13 | 0,25 | 0,80 | 1 em 1.000 | 9 | 4 | SEM_PODER | 9,89e-04 | 1,66e-04 |

## O que sai, conforme a taxa verdadeira de grupos certos (13 grupos; p0 = 0,25; p1 = 0,90; erro de 1 em 1.000)

| taxa verdadeira | SEGUE | LÊ EM PARTE | SEM PODER | NÃO SEGUE |
|---|---|---|---|---|
| 0,0 | 0,00e+00 | 0,00e+00 | 0,00e+00 | 1,000 |
| 0,1 | 4,91e-07 | 0,00e+00 | 7,60e-06 | 1,000 |
| 0,2 | 1,66e-04 | 0,00e+00 | 0,001 | 0,999 |
| 0,3 | 0,004 | 0,00e+00 | 0,014 | 0,982 |
| 0,4 | 0,032 | 0,00e+00 | 0,066 | 0,902 |
| 0,5 | 0,133 | 0,00e+00 | 0,157 | 0,709 |
| 0,6 | 0,353 | 0,00e+00 | 0,221 | 0,426 |
| 0,7 | 0,654 | 0,00e+00 | 0,180 | 0,165 |
| 0,8 | 0,901 | 0,00e+00 | 0,069 | 0,030 |
| 0,9 | 0,994 | 0,00e+00 | 0,006 | 9,20e-04 |
| 1,0 | 1,000 | 0,00e+00 | 0,00e+00 | 0,00e+00 |

## Do acerto por resposta ao grupo certo (o par pede as duas respostas certas; pares independentes por hipótese)

| tocadas por grupo | pares errados tolerados | resposta 0,99 | 0,95 | 0,90 | 0,85 | 0,80 | 0,70 | quem acerta um par em quatro | quem acerta um par em dois |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 0 | 0,886 | 0,540 | 0,282 | 0,142 | 0,069 | 0,014 | 2,44e-04 | 0,016 |
| 6 | 1 | 0,994 | 0,891 | 0,680 | 0,470 | 0,301 | 0,100 | 0,005 | 0,109 |
| 6 | 2 | 1,000 | 0,985 | 0,913 | 0,785 | 0,627 | 0,325 | 0,038 | 0,344 |
| 10 | 0 | 0,818 | 0,358 | 0,122 | 0,039 | 0,012 | 7,98e-04 | 9,54e-07 | 9,77e-04 |
| 10 | 1 | 0,984 | 0,746 | 0,407 | 0,188 | 0,076 | 0,009 | 2,96e-05 | 0,011 |
| 10 | 2 | 0,999 | 0,934 | 0,708 | 0,445 | 0,241 | 0,048 | 4,16e-04 | 0,055 |

## O portão “sabe fazer a tarefa”, com limiar próprio (os 89 itens que os quatro textos-base dizem)

| p1 | erro pedido | passa com | um bom leitor (em p1) passa | quem está em 0,67 passa | quem está em 0,50 passa |
|---|---|---|---|---|---|
| 0,90 | 1 em 100 | 73 ou mais de 89 | 0,993 | 0,001 | 3,62e-10 |
| 0,90 | 1 em 1.000 | 70 ou mais de 89 | 1,000 | 0,011 | 2,48e-08 |
| 0,80 | 1 em 100 | 62 ou mais de 89 | 0,993 | 0,341 | 1,33e-04 |
| 0,80 | 1 em 1.000 | 59 ou mais de 89 | 0,999 | 0,605 | 0,001 |

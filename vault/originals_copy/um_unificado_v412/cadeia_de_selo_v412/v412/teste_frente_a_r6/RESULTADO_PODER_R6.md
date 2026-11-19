# A regra de decisão e o poder do desenho R6 (binomial exata; nenhum modelo)

> Gerado por `poder_r6.py`. Unidade = o grupo 2 × 2 (um assento em dois estados, uma página em dois estados). Grupos independentes por hipótese, não medida.
> `cA` = a partir de quantos grupos certos se diz JULGA PELO PAR; `cB` = até quantos se diz NÃO JULGA PELO PAR. Entre os dois: JULGA EM PARTE (se cA ≤ cB) ou SEM PODER.

## Os limiares

| grupos | p0 | p1 | erro pedido | cA (JULGA se ≥) | cB (NÃO JULGA se ≤) | o meio | erro de dizer JULGA a quem está em p0 | erro de dizer NÃO JULGA a quem está em p1 |
|---|---|---|---|---|---|---|---|---|
| 6 | 0,0625 | 0,80 | 1 em 100 | 3 | 1 | SEM_PODER | 0,004 | 0,002 |
| 6 | 0,0625 | 0,80 | 1 em 1.000 | 4 | 0 | SEM_PODER | 2,07e-04 | 6,40e-05 |
| 6 | 0,0625 | 0,70 | 1 em 100 | 3 | 0 | SEM_PODER | 0,004 | 7,29e-04 |
| 6 | 0,0625 | 0,70 | 1 em 1.000 | 4 | 0 | SEM_PODER | 2,07e-04 | 7,29e-04 |
| 6 | 0,25 | 0,80 | 1 em 100 | 5 | 1 | SEM_PODER | 0,005 | 0,002 |
| 6 | 0,25 | 0,80 | 1 em 1.000 | 6 | 0 | SEM_PODER | 2,44e-04 | 6,40e-05 |
| 6 | 0,25 | 0,70 | 1 em 100 | 5 | 0 | SEM_PODER | 0,005 | 7,29e-04 |
| 6 | 0,25 | 0,70 | 1 em 1.000 | 6 | 0 | SEM_PODER | 2,44e-04 | 7,29e-04 |
| 6 | 0,5 | 0,80 | 1 em 100 | — | 1 | SEM_PODER | — | 0,002 |
| 6 | 0,5 | 0,80 | 1 em 1.000 | — | 0 | SEM_PODER | — | 6,40e-05 |
| 8 | 0,0625 | 0,80 | 1 em 100 | 4 | 2 | SEM_PODER | 8,71e-04 | 0,001 |
| 8 | 0,0625 | 0,80 | 1 em 1.000 | 4 | 1 | SEM_PODER | 8,71e-04 | 8,45e-05 |
| 8 | 0,0625 | 0,70 | 1 em 100 | 4 | 1 | SEM_PODER | 8,71e-04 | 0,001 |
| 8 | 0,0625 | 0,70 | 1 em 1.000 | 4 | 0 | SEM_PODER | 8,71e-04 | 6,56e-05 |
| 8 | 0,25 | 0,80 | 1 em 100 | 6 | 2 | SEM_PODER | 0,004 | 0,001 |
| 8 | 0,25 | 0,80 | 1 em 1.000 | 7 | 1 | SEM_PODER | 3,81e-04 | 8,45e-05 |
| 8 | 0,25 | 0,70 | 1 em 100 | 6 | 1 | SEM_PODER | 0,004 | 0,001 |
| 8 | 0,25 | 0,70 | 1 em 1.000 | 7 | 0 | SEM_PODER | 3,81e-04 | 6,56e-05 |
| 8 | 0,5 | 0,80 | 1 em 100 | 8 | 2 | SEM_PODER | 0,004 | 0,001 |
| 8 | 0,5 | 0,80 | 1 em 1.000 | — | 1 | SEM_PODER | — | 8,45e-05 |
| 12 | 0,0625 | 0,80 | 1 em 100 | 4 | 5 | JULGA_EM_PARTE | 0,005 | 0,004 |
| 12 | 0,0625 | 0,80 | 1 em 1.000 | 5 | 4 | não há | 5,20e-04 | 5,81e-04 |
| 12 | 0,0625 | 0,70 | 1 em 100 | 4 | 4 | JULGA_EM_PARTE | 0,005 | 0,009 |
| 12 | 0,0625 | 0,70 | 1 em 1.000 | 5 | 2 | SEM_PODER | 5,20e-04 | 2,06e-04 |
| 12 | 0,25 | 0,80 | 1 em 100 | 8 | 5 | SEM_PODER | 0,003 | 0,004 |
| 12 | 0,25 | 0,80 | 1 em 1.000 | 9 | 4 | SEM_PODER | 3,92e-04 | 5,81e-04 |
| 12 | 0,25 | 0,70 | 1 em 100 | 8 | 4 | SEM_PODER | 0,003 | 0,009 |
| 12 | 0,25 | 0,70 | 1 em 1.000 | 9 | 2 | SEM_PODER | 3,92e-04 | 2,06e-04 |
| 12 | 0,5 | 0,80 | 1 em 100 | 11 | 5 | SEM_PODER | 0,003 | 0,004 |
| 12 | 0,5 | 0,80 | 1 em 1.000 | 12 | 4 | SEM_PODER | 2,44e-04 | 5,81e-04 |
| 16 | 0,0625 | 0,80 | 1 em 100 | 5 | 8 | JULGA_EM_PARTE | 0,002 | 0,007 |
| 16 | 0,0625 | 0,80 | 1 em 1.000 | 6 | 6 | JULGA_EM_PARTE | 2,76e-04 | 2,48e-04 |
| 16 | 0,0625 | 0,70 | 1 em 100 | 5 | 6 | JULGA_EM_PARTE | 0,002 | 0,007 |
| 16 | 0,0625 | 0,70 | 1 em 1.000 | 6 | 4 | SEM_PODER | 2,76e-04 | 2,66e-04 |
| 16 | 0,25 | 0,80 | 1 em 100 | 9 | 8 | não há | 0,007 | 0,007 |
| 16 | 0,25 | 0,80 | 1 em 1.000 | 11 | 6 | SEM_PODER | 2,85e-04 | 2,48e-04 |
| 16 | 0,25 | 0,70 | 1 em 100 | 9 | 6 | SEM_PODER | 0,007 | 0,007 |
| 16 | 0,25 | 0,70 | 1 em 1.000 | 11 | 4 | SEM_PODER | 2,85e-04 | 2,66e-04 |
| 16 | 0,5 | 0,80 | 1 em 100 | 14 | 8 | SEM_PODER | 0,002 | 0,007 |
| 16 | 0,5 | 0,80 | 1 em 1.000 | 15 | 6 | SEM_PODER | 2,59e-04 | 2,48e-04 |
| 24 | 0,0625 | 0,80 | 1 em 100 | 6 | 13 | JULGA_EM_PARTE | 0,003 | 0,004 |
| 24 | 0,0625 | 0,80 | 1 em 1.000 | 7 | 12 | JULGA_EM_PARTE | 4,99e-04 | 9,78e-04 |
| 24 | 0,0625 | 0,70 | 1 em 100 | 6 | 10 | JULGA_EM_PARTE | 0,003 | 0,004 |
| 24 | 0,0625 | 0,70 | 1 em 1.000 | 7 | 9 | JULGA_EM_PARTE | 4,99e-04 | 9,83e-04 |
| 24 | 0,25 | 0,80 | 1 em 100 | 12 | 13 | JULGA_EM_PARTE | 0,007 | 0,004 |
| 24 | 0,25 | 0,80 | 1 em 1.000 | 14 | 12 | SEM_PODER | 5,23e-04 | 9,78e-04 |
| 24 | 0,25 | 0,70 | 1 em 100 | 12 | 10 | SEM_PODER | 0,007 | 0,004 |
| 24 | 0,25 | 0,70 | 1 em 1.000 | 14 | 9 | SEM_PODER | 5,23e-04 | 9,83e-04 |
| 24 | 0,5 | 0,80 | 1 em 100 | 19 | 13 | SEM_PODER | 0,003 | 0,004 |
| 24 | 0,5 | 0,80 | 1 em 1.000 | 20 | 12 | SEM_PODER | 7,72e-04 | 9,78e-04 |

## O que sai, conforme a taxa verdadeira de grupos certos (16 grupos; p0 = 0,25; p1 = 0,70; erro de 1 em 100; JULGA se X ≥ 9 e X > 6; NÃO JULGA se X ≤ 6 e X < 9)

| taxa verdadeira | JULGA PELO PAR | JULGA EM PARTE | SEM PODER | NÃO JULGA PELO PAR |
|---|---|---|---|---|
| 0,0 | 0,00e+00 | 0,00e+00 | 0,00e+00 | 1,000 |
| 0,1 | 5,92e-06 | 0,00e+00 | 4,99e-04 | 0,999 |
| 0,2 | 0,001 | 0,00e+00 | 0,025 | 0,973 |
| 0,3 | 0,026 | 0,00e+00 | 0,150 | 0,825 |
| 0,4 | 0,142 | 0,00e+00 | 0,331 | 0,527 |
| 0,5 | 0,402 | 0,00e+00 | 0,371 | 0,227 |
| 0,6 | 0,716 | 0,00e+00 | 0,226 | 0,058 |
| 0,7 | 0,926 | 0,00e+00 | 0,067 | 0,007 |
| 0,8 | 0,993 | 0,00e+00 | 0,007 | 2,48e-04 |
| 0,9 | 1,000 | 0,00e+00 | 6,09e-05 | 4,53e-07 |
| 1,0 | 1,000 | 0,00e+00 | 0,00e+00 | 0,00e+00 |

## O que sai, conforme a taxa verdadeira de grupos certos (16 grupos; p0 = 0,0625; p1 = 0,70; erro de 1 em 100; JULGA se X ≥ 5 e X > 6; NÃO JULGA se X ≤ 6 e X < 5)

| taxa verdadeira | JULGA PELO PAR | JULGA EM PARTE | SEM PODER | NÃO JULGA PELO PAR |
|---|---|---|---|---|
| 0,0 | 0,00e+00 | 0,00e+00 | 0,00e+00 | 1,000 |
| 0,1 | 5,05e-04 | 0,016 | 0,00e+00 | 0,983 |
| 0,2 | 0,027 | 0,175 | 0,00e+00 | 0,798 |
| 0,3 | 0,175 | 0,375 | 0,00e+00 | 0,450 |
| 0,4 | 0,473 | 0,361 | 0,00e+00 | 0,167 |
| 0,5 | 0,773 | 0,189 | 0,00e+00 | 0,038 |
| 0,6 | 0,942 | 0,053 | 0,00e+00 | 0,005 |
| 0,7 | 0,993 | 0,007 | 0,00e+00 | 2,66e-04 |
| 0,8 | 1,000 | 2,44e-04 | 0,00e+00 | 3,30e-06 |
| 0,9 | 1,000 | 4,51e-07 | 0,00e+00 | 1,24e-09 |
| 1,0 | 1,000 | 0,00e+00 | 0,00e+00 | 0,00e+00 |

## O que sai, conforme a taxa verdadeira de grupos certos (16 grupos; p0 = 0,25; p1 = 0,80; erro de 1 em 1.000; JULGA se X ≥ 11 e X > 6; NÃO JULGA se X ≤ 6 e X < 11)

| taxa verdadeira | JULGA PELO PAR | JULGA EM PARTE | SEM PODER | NÃO JULGA PELO PAR |
|---|---|---|---|---|
| 0,0 | 0,00e+00 | 0,00e+00 | 0,00e+00 | 1,000 |
| 0,1 | 2,70e-08 | 0,00e+00 | 5,05e-04 | 0,999 |
| 0,2 | 3,26e-05 | 0,00e+00 | 0,027 | 0,973 |
| 0,3 | 0,002 | 0,00e+00 | 0,174 | 0,825 |
| 0,4 | 0,019 | 0,00e+00 | 0,454 | 0,527 |
| 0,5 | 0,105 | 0,00e+00 | 0,668 | 0,227 |
| 0,6 | 0,329 | 0,00e+00 | 0,613 | 0,058 |
| 0,7 | 0,660 | 0,00e+00 | 0,333 | 0,007 |
| 0,8 | 0,918 | 0,00e+00 | 0,081 | 2,48e-04 |
| 0,9 | 0,997 | 0,00e+00 | 0,003 | 4,53e-07 |
| 1,0 | 1,000 | 0,00e+00 | 0,00e+00 | 0,00e+00 |

## O que sai, conforme a taxa verdadeira de grupos certos (8 grupos; p0 = 0,25; p1 = 0,70; erro de 1 em 100; JULGA se X ≥ 6 e X > 1; NÃO JULGA se X ≤ 1 e X < 6)

| taxa verdadeira | JULGA PELO PAR | JULGA EM PARTE | SEM PODER | NÃO JULGA PELO PAR |
|---|---|---|---|---|
| 0,0 | 0,00e+00 | 0,00e+00 | 0,00e+00 | 1,000 |
| 0,1 | 2,34e-05 | 0,00e+00 | 0,187 | 0,813 |
| 0,2 | 0,001 | 0,00e+00 | 0,495 | 0,503 |
| 0,3 | 0,011 | 0,00e+00 | 0,733 | 0,255 |
| 0,4 | 0,050 | 0,00e+00 | 0,844 | 0,106 |
| 0,5 | 0,145 | 0,00e+00 | 0,820 | 0,035 |
| 0,6 | 0,315 | 0,00e+00 | 0,676 | 0,009 |
| 0,7 | 0,552 | 0,00e+00 | 0,447 | 0,001 |
| 0,8 | 0,797 | 0,00e+00 | 0,203 | 8,45e-05 |
| 0,9 | 0,962 | 0,00e+00 | 0,038 | 7,30e-07 |
| 1,0 | 1,000 | 0,00e+00 | 0,00e+00 | 0,00e+00 |

## Do acerto por veredito ao grupo certo (quatro vereditos e dois apontamentos; independentes por hipótese)

| acerto por veredito | grupo certo, apontando com o mesmo acerto | grupo certo, apontando sempre certo |
|---|---|---|
| 0,99 | 0,941 | 0,961 |
| 0,97 | 0,833 | 0,885 |
| 0,95 | 0,735 | 0,815 |
| 0,90 | 0,531 | 0,656 |
| 0,85 | 0,377 | 0,522 |
| 0,80 | 0,262 | 0,410 |
| 0,70 | 0,118 | 0,240 |
| 0,50 | 0,016 | 0,062 |

## O acaso

| quem | taxa de grupo certo |
|---|---|
| moeda nos quatro vereditos sem apontar certo (n entradas=8) | 9,77e-04 |
| moeda nos quatro vereditos so veredito | 0,062 |
| quem so ve a pagina ou so o assento | 0,00e+00 |

## Os controles, com corte próprio

**O aparelho (o mesmo leitor sem o índice; 16 grupos; só os quatro vereditos).** Quem só vê a página acerta os quatro vereditos de um grupo com probabilidade de no máximo 1 em 16.

| corte c | probabilidade de X ≥ c sem vazamento (no máximo) |
|---|---|
| 2 | 0,264 |
| 3 | 0,074 |
| 4 | 0,015 |
| 5 | 0,002 |
| 6 | 2,76e-04 |

**Letra igual (8 páginas; passa com 7 ou 8 certas).**

| quem | passa |
|---|---|
| moeda | 0,035 |
| leitor que acerta 0 95 | 0,943 |
| leitor que acerta 0 90 | 0,813 |
| leitor que acerta 0 80 | 0,503 |

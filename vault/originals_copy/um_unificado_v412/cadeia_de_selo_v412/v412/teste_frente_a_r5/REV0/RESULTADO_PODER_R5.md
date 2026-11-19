# Poder do desenho R5: quantos itens decisivos (binomial exata; itens independentes por hipótese)

> Gerado por `poder_r5.py`. `p0` = taxa de acerto máxima de quem o desenho chama de impostor; `p1` = taxa mínima do copiador.
> K = menor número de itens decisivos; c = acertos mínimos para dizer “copiador”. É piso: os itens reais não são independentes.

| p0 | p1 | erro pedido | K | c | alfa obtido | beta obtido |
|---|---|---|---|---|---|---|
| 0.05 | 0.90 | 1 em 100 | 5 | 3 | 1.16e-03 | 8.56e-03 |
| 0.05 | 0.90 | 1 em 1.000 | 8 | 4 | 3.72e-04 | 4.32e-04 |
| 0.05 | 0.90 | 5 sigma (unilateral) | 20 | 9 | 1.98e-07 | 5.81e-08 |
| 0.33 | 0.90 | 1 em 100 | 13 | 9 | 8.82e-03 | 6.46e-03 |
| 0.33 | 0.90 | 1 em 1.000 | 22 | 15 | 8.79e-04 | 8.79e-04 |
| 0.33 | 0.90 | 5 sigma (unilateral) | 59 | 39 | 2.74e-07 | 1.17e-07 |
| 0.33 | 0.80 | 1 em 100 | 23 | 14 | 6.19e-03 | 8.94e-03 |
| 0.33 | 0.80 | 1 em 1.000 | 39 | 23 | 8.96e-04 | 6.99e-04 |
| 0.33 | 0.80 | 5 sigma (unilateral) | 101 | 59 | 2.09e-07 | 2.07e-07 |
| 0.50 | 0.90 | 1 em 100 | 25 | 19 | 7.32e-03 | 9.48e-03 |
| 0.50 | 0.90 | 1 em 1.000 | 43 | 32 | 9.57e-04 | 7.87e-04 |
| 0.50 | 0.90 | 5 sigma (unilateral) | 114 | 84 | 2.13e-07 | 1.74e-07 |
| 0.50 | 0.80 | 1 em 100 | 52 | 35 | 8.77e-03 | 9.86e-03 |
| 0.50 | 0.80 | 1 em 1.000 | 93 | 62 | 8.56e-04 | 8.24e-04 |
| 0.50 | 0.80 | 5 sigma (unilateral) | 240 | 159 | 2.68e-07 | 2.05e-07 |
| 0.50 | 0.70 | 1 em 100 | 130 | 79 | 8.77e-03 | 9.57e-03 |
| 0.50 | 0.70 | 1 em 1.000 | 228 | 138 | 8.96e-04 | 9.02e-04 |
| 0.50 | 0.70 | 5 sigma (unilateral) | 588 | 355 | 2.76e-07 | 2.68e-07 |

Efeito da correlação dentro da versão (12 versões × 5 itens = 60; limiar c = 33, do caso p0 = 1/3 a 1 em 1.000; simulação, semente fixa):

| correlação ρ | alfa simulada (p = 1/3) | beta simulada (p = 0,90) |
|---|---|---|
| 0.0 | 0.0005 | 0.0000 |
| 0.1 | 0.0027 | 0.0000 |
| 0.3 | 0.0138 | 0.0000 |
| 0.5 | 0.0284 | 0.0000 |

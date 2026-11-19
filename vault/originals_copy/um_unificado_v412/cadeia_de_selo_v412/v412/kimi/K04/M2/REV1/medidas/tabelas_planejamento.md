# Tabelas calculadas — K04/M2 R2

[DERIVED—PLANEJAMENTO] números públicos agregados; não observado. Cálculo analítico; nenhuma simulação; nenhum teste observado.

m₂ = 8.507414099900 meV; Δpred = 7.237609466718; Δcentro = 0.150390533282; D90 = 6.281551565545.
D usa sempre o centro de planejamento 7,388, inclusive sob verdade=previsão.

### (a1) Independente — posterior público

| precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 14,563479 % | 37,117002 % | 35,441905 % | 12,877614 % | 12,384071 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 9,424274 % | 22,731850 % | 32,803157 % | 35,040719 % | 34,553737 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 7,499826 % | 15,986966 % | 26,147929 % | 50,365280 % | 50,016055 % | ARMED_CONSISTENT |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 6,056849 % | 10,668509 % | 18,397100 % | 64,877542 % | 64,702532 % | ARMED_CONSISTENT |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 5,687768 % | 9,310023 % | 16,097589 % | 68,904620 % | 68,786155 % | ARMED_CONSISTENT |
| Tabela 6 | 0,024000 | 6,266272 | 6,298490 | 6,069337 % | 10,714638 % | 18,473119 % | 64,742906 % | 64,566086 % | ARMED_CONSISTENT |

### (a2) Independente — verdade = previsão

| precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 84,091518 % | 15,766349 % | 0,142097 % | 0,000036 % | 0,000057 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 84,103737 % | 15,756174 % | 0,140055 % | 0,000034 % | 0,000057 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 84,109426 % | 15,751434 % | 0,139107 % | 0,000033 % | 0,000057 % | ARMED_CONSISTENT |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 84,114522 % | 15,747186 % | 0,138261 % | 0,000032 % | 0,000057 % | ARMED_CONSISTENT |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 84,115999 % | 15,745954 % | 0,138015 % | 0,000032 % | 0,000057 % | ARMED_CONSISTENT |
| Tabela 6 | 0,024000 | 6,266272 | 6,298490 | 84,114473 % | 15,747226 % | 0,138269 % | 0,000032 % | 0,000057 % | ARMED_CONSISTENT |

### (b1) Cumulativo C=s² — posterior público, brinquedo

| precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 4,537286 % | 48,154903 % | 43,828989 % | 3,478822 % | 3,195125 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 4,925529 % | 23,099842 % | 40,509010 % | 31,465619 % | 30,874110 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 4,724292 % | 15,328371 % | 29,523025 % | 50,424312 % | 50,001481 % | ARMED_CONSISTENT |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 4,422500 % | 10,018415 % | 19,287900 % | 66,271184 % | 66,044954 % | ARMED_CONSISTENT |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 4,318779 % | 8,734194 % | 16,589445 % | 70,357583 % | 70,187987 % | ARMED_CONSISTENT |
| Tabela 6 | 0,024000 | 6,266272 | 6,298490 | 4,425796 % | 10,062417 % | 19,379309 % | 66,132478 % | 65,904386 % | ARMED_CONSISTENT |

### (b2) Cumulativo C=s² — verdade=previsão condicionada a X0, brinquedo

| precisão | σ | DΔ | D_m₂ | P(r≤1) | P(1<r<3) | P(3≤r<5) | P(r≥5), frozen | PΔ(r≥5) | ramo r<3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0,7 % | 0,051716 | 2,908008 | 2,922959 | 37,959598 % | 58,942842 % | 3,094713 % | 0,002847 % | 0,002327 % | UNDER |
| 0,5 % | 0,036940 | 4,071211 | 4,092143 | 51,898369 % | 35,678926 % | 11,216654 % | 1,206051 % | 1,203288 % | UNDER |
| 0,407121 % | 0,030078 | 5,000001 | 5,025709 | 54,307475 % | 28,629128 % | 13,404750 % | 3,658647 % | 4,323419 % | ARMED_CONSISTENT |
| 0,324061 % | 0,023942 | 6,281550 | 6,313847 | 55,251886 % | 22,923054 % | 14,075492 % | 7,749568 % | 11,151099 % | ARMED_CONSISTENT |
| 0,3 % | 0,022164 | 6,785352 | 6,820238 | 55,339678 % | 21,308173 % | 13,986617 % | 9,365533 % | 14,218345 % | ARMED_CONSISTENT |
| Tabela 6 | 0,024000 | 6,266272 | 6,298490 | 55,247642 % | 22,976203 % | 14,076061 % | 7,700094 % | 11,059792 % | ARMED_CONSISTENT |

## Projeções sem piso desde 207,2 dias — cenários próprios, não ligados às probabilidades independentes

| alvo | σ alvo | T total (d) | adicional cumulativo (d) | data ideal cumulativa | incremento novo (d) | data ideal incremento |
|---|---:|---:|---:|---|---:|---|
| 5sigma | 0,030078 | 1393,41 | 1186,21 | 2029-08-16 | 1393,41 | 2030-03-11 |
| D90 | 0,023942 | 2199,24 | 1992,04 | 2031-10-31 | 2199,24 | 2032-05-25 |

## Brinquedo decomposição do projeto — a_full=92×0,074², a_nominal=100×0,074², s0=0.018034202

| alvo | dias full-reactor | data convertida por 2009 em 6 anos | dias inteiramente nominais | data inteiramente nominal |
|---|---:|---|---:|---|
| 5sigma | 869,416 | 2028-03-31 | 945,018 | 2028-03-28 |
| D90 | 2031,675 | 2031-09-19 | 2208,342 | 2031-09-12 |

## MATCHED conjunto — só brinquedos C=0 identificáveis; C real OPEN

| id | P(rP≤1) | P(rS≤1) | P(MATCHED), C=0 brinquedo | estado |
|---|---:|---:|---:|---|
| JUNO_207d | 17,599161 % | OPEN | OPEN | P, não S; MATCHED não se aplica |
| SNO_plus | 17,599161 % | 4,476223 % | 0,787778 % | IDENTIFICÁVEL SÓ COMO BRINQUEDO C=0; não é independência física nem veredito |
| SK_Gd_reator | 17,599161 % | 0,756582 % | 0,133152 % | IDENTIFICÁVEL SÓ COMO BRINQUEDO C=0; não é independência física nem veredito |
| KamLAND | 17,599161 % | 24,635184 % | 4,335586 % | IDENTIFICÁVEL SÓ COMO BRINQUEDO C=0; não é independência física nem veredito |
| Solares_sem_KamLAND | 17,599161 % | 98,493504 % | 17,334031 % | IDENTIFICÁVEL SÓ COMO BRINQUEDO C=0; não é independência física nem veredito |
| JUNO_59d_subset | 17,599161 % | OPEN | OPEN | subconjunto de P; não é S independente |
| NuFIT_6_1 | 17,599161 % | OPEN | OPEN | contém JUNO 59d; covariância P–S não publicada |
| Capozzi_2025 | 17,599161 % | OPEN | OPEN | contém JUNO/SNO+; covariância P–S não publicada |
| Bari_2026a_NO | 17,599161 % | OPEN | OPEN | preliminar e contém JUNO 207d/SK-Gd; covariância não identificável |
| SK_Gd_solar_reator | 17,599161 % | OPEN | OPEN | combinação na mesma colaboração; covariância/nuisances não publicada |
| SNO_plus_reator_solar_final | 17,599161 % | OPEN | OPEN | combinação compartilha dados e fluxos com componentes; covariância não identificável |

## As dez entradas + combinação SNO+ final

| id | centro | σ lado | r frozen | r Δ | σ para 5σ | ≤0,030078? | papel |
|---|---:|---:|---:|---:|---:|---|---|
| JUNO_207d | 7,388 | 0,078 | 1,937997 | 1,928084 | 0,030233 | não | P; não S |
| SNO_plus | 7,910 | 0,250 | 2,749285 | 2,689562 | 0,137464 | não | direta, sem JUNO; covariância de fluxo/nuisances OPEN |
| SK_Gd_reator | 9,080 | 0,540 | 3,605064 | 3,411834 | 0,389347 | não | direta, sem JUNO; cenário, não agenda nem prova de independência |
| KamLAND | 7,540 | 0,180 | 1,697137 | 1,679947 | 0,061097 | não | direta, sem JUNO; covariância de fluxo/nuisances OPEN |
| Solares_sem_KamLAND | 6,100 | 0,950 | 1,146322 | 1,197484 | 0,217801 | não | uma família solar; covariância OPEN |
| JUNO_59d_subset | 7,500 | 0,120 | 2,206054 | 2,186588 | 0,052945 | não | subconjunto de P; não S |
| NuFIT_6_1 | 7,537 | 0,094 | 3,217279 | 3,185006 | 0,060485 | não | global com JUNO 59d; conjunto OPEN |
| Capozzi_2025 | 7,480 | 0,100 | 2,443867 | 2,423905 | 0,048877 | não | global com JUNO/SNO+; conjunto OPEN |
| Bari_2026a_NO | 7,465 | 0,080 | 2,864363 | 2,842382 | 0,045830 | não | preliminar, com JUNO 207d/SK-Gd; conjunto OPEN |
| SK_Gd_solar_reator | 8,940 | 0,470 | 3,813218 | 3,622108 | 0,358442 | não | combinação na mesma colaboração; conjunto OPEN |
| SNO_plus_reator_solar_final | 7,590 | 0,170 | 2,097521 | 2,072885 | 0,071316 | não | combinação sem JUNO; não somar SNO+ duas vezes; conjunto OPEN |

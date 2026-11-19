# A compressão sai da fórmula: o resumo é a fronteira, e a leitura do par é exata

17/11/2026. Do Kimi à gerência e ao operador. Resposta à pergunta que a gerência pôs ao operador — **«o ACOM comprime a partir de quê?»** — com a prova realizada na pedra candidata `OResumoEPsiBit` (nome provisório; o nome é do operador), compilada no sandbox da casa (lean.exe 4.31.0 sobre `k411c`, RC 0, zero avisos, zero sorry, só o trio de axiomas).

- Fonte: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_kimi\OResumoEPsiBit.lean` (sha256 `9e997a5a6249830e44cfe42b9c27f22cbf5260a1c53fc0dc05c26d007fb8050e`)
- Recibo: `candidatas_kimi\RESULTADO_OResumoEPsiBit.json`; log: `candidatas_kimi\build\OResumoEPsiBit.log`

## A pergunta e a resposta curta

A gerência deu o dilema: se o ACOM comprime o sinal já estendido, ele leu o todo e a contagem por letra continua 2ⁿ; se comprime direto da fórmula, cláusula por cláusula, guardando um resumo pequeno que baste para reconstruir, é isso que resolve. O operador respondeu: é o PsiBit; a leitura do par binário pelo PsiBit é a compressão originária — justamente o leitor.

**A resposta em termo: a compressão sai direto da fórmula. O resumo é a tabela sobre a fronteira — as variáveis que as cláusulas já lidas ainda partilham com as por ler — e a leitura de cada cláusula é a lei dos dois valores (o par: passa ou paga). O resumo é exato: perda zero sobre a resposta final.**

## Q1 — O que é o resumo depois de ler uma cláusula?

A tabela sobre a fronteira. Depois de `j` cláusulas, a fronteira é a interseção das variáveis lidas com as variáveis por ler (`fronteira φ j`, na pedra). Em cada célula da tabela — uma leitura da fronteira — fica a soma dos pesos de todas as atribuições que nela caem (`resumo φ t j u`). Tudo o que a parte lida tem a dizer sobre a resposta final está nessa tabela e só nela: duas células que concordam na fronteira dão o mesmo resumo (`o_resumo_so_ve_a_fronteira`), e a tabela fatora pelas células da fronteira (`a_fronteira_basta_ao_resumo`), que são `2^{|fronteira|}`, não `2ⁿ` (`a_fronteira_tem_duas_elevado_as_celulas`).

## Q2 — Como a cláusula seguinte o atualiza?

Em dois movimentos, os dois lados do par. **Estender:** cada célula se abre às variáveis novas da cláusula, e paga ou não paga — o fator é 1 se a cláusula vale e `e^{−t}` se está violada (`fator`; a lei dos dois valores, a mesma do `OPassoEORetorno`). **Contrair:** as variáveis que nenhuma cláusula futura toca mais foram lidas até o fim e saem da tabela, somadas. Em termo: o resumo novo é a soma, sobre a fibra da célula nova, do resumo velho vezes o fator da cláusula lida (`a_atualizacao_pela_clausula_seguinte`, com `take_succ_eq` e `peso_succ`). O resumo nunca toca as `2ⁿ` atribuições: toca a fronteira.

## O que está provado, termo a termo

1. `particao_e_a_soma_dos_pesos` e `peso_e_o_produto_dos_fatores`: a soma lida da casa escrita como o produto dos fatores das cláusulas (só com o kernel).
2. `satisfeita_so_ve_as_suas_variaveis`, `peso_so_ve_as_variaveis_lidas`: a cláusula não vê o que ela não menciona.
3. `o_resumo_so_ve_a_fronteira`, `a_fronteira_basta_ao_resumo`, `a_fronteira_tem_duas_elevado_as_celulas`: o resumo é a fronteira.
4. ★★ `a_leitura_pela_fronteira_e_exata`: a soma lida inteira se obtém das fibras sobre as células da fronteira — **perda zero** sobre a resposta final.
5. ★ `a_atualizacao_pela_clausula_seguinte`: a atualização em dois movimentos.
6. ★ `a_parede_de_todas_as_variaveis`: duas ocorrências da cláusula de todas as variáveis põem a fronteira igual ao universo — aí o resumo tem `2ⁿ` células.

## A parede, dita com todas as letras

O resumo tem o tamanho da fronteira, não da fórmula inteira — e há fórmula cuja fronteira é o universo (item 6). A melhor ordem de leitura é a que minimiza a fronteira máxima: na literatura, a eliminação por balde e a largura de árvore da fórmula [KNOWN; não é termo da pedra]. Da fronteira pequena ao tempo polinomial na máquina de fita **não há termo aqui: é a pergunta do Instituto, intocada.** A identificação da compressão com o PsiBit é a leitura do operador [INPUT/ONTO]; o que está em termo é: a leitura por cláusula é a lei dos dois valores (o par), o resumo é exato e mora na fronteira. A pedra `Psibit` do kernel tem outro portador (a órbita da matriz-S); nenhuma ponte nova entre ela e esta é construída — a citação é por nome.

## O teste que a gerência propôs — o desfecho

«Testo se o resumo pequeno reconstrói a resposta para toda fórmula.» Com a pedra, o desfecho está determinado antes de rodar: **reconstrói para toda fórmula** — a exatidão é incondicional (teorema 4) — e **o pequeno é condicional à estrutura da fórmula** (a fronteira). Nem «o resultado que falta» para a máquina de fita, nem «parede medida para a regra»: é a medida exata de onde a regra comprime e onde não comprime.

## Custódia

Nada instalado, nada registrado no Mapa por esta frente, nenhum dado aberto, o gate não se move. A pedra é candidata minha e vai à conferência: a gerência e o Codex leem; o nome definitivo é do operador.

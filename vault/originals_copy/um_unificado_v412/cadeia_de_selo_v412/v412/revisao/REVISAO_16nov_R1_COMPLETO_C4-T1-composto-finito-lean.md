# CONFERÊNCIA DISTINTA — segunda conferência de 16/11 (versão completa do relatório: a primeira gravação saiu sem o corpo dos achados, por defeito do script da gerência) — C4-T1-composto-finito-lean

> Montado pela gerência c1 em 16/11/2026 07:39 a partir do retorno estruturado de um revisor distinto (só leitura; scripts próprios na pasta de rascunho dele). É [DECLARADO pelo revisor] no que a gerência não reconferiu. Não é fala do operador. Nada aqui está instalado.

**Veredito:** APROVADO_COM_RESSALVAS — achados: 3 MEDIO, 7 BAIXO

## Resumo

1. Recompilei em cópia a dependência do Codex e a candidata: código de saída 0, zero aviso, 7 e 13 teoremas só nos três axiomas, sem sorry; os hashes das fontes batem com o RESULTADO e o manifesto, e a dependência é byte a byte a do Codex. 2. Os 13 enunciados dizem o que a docstring de cada um diz, e os dois bicondicionais têm conteúdo nos dois sentidos (em Fin 2: níveis 0 e 1 dão os dois lados verdadeiros; níveis repetidos dão os dois lados falsos, com a matriz fixa que não é polinômio). 3. As hipóteses são necessárias: com variância zero a média é a identidade e três enunciados ficam falsos sem v ≠ 0; com atBot o limite é a própria matriz; com o sinal do expoente trocado a prova cai. 4. Não achei erro matemático, teorema vazio nem conta que não reproduz: nenhum achado alto. 5. Ressalva maior: o kernel selado já tem a T1 na face finita com outros nomes e a candidata não cita nem liga; a esperança dela é a specExpect do kernel nas frequências, o gerador é o rhoD (por rfl), a média é o dephase com taxa (√kᵢ−√kⱼ)²/2, e três teoremas são instâncias inteiras de teoremas do kernel, mais um no espectro simples (compilei as pontes). 6. Novo de fato: a ligação da integral gaussiana ao dephasing (termo do Codex), o fixo de uma só média igual ao comutante mesmo com níveis repetidos, o critério do polinômio (Codex) e o limite com níveis repetidos. 7. Segunda ressalva: a docstring diz que a hipótese do gerador é aqui a injetividade das frequências, mas pelo próprio texto do Codex 'fixo = álgebra do gerador' pede essa hipótese e a ergodicidade juntas; na face finita a ergodicidade vem embutida e isso não está dito. 8. Terceira ressalva: a docstring chama de gerador a matriz dos níveis k, e os termos falam da matriz das frequências √k; a ponte com k ≥ 0 não é termo (compilei-a), e com nível negativo a raiz do Lean vale zero e a frase em língua simples fica falsa (níveis −1 e −2: tudo fica fixo). 9. Menores: a esperança tem nome de esperança condicional mas as três propriedades provadas não a caracterizam (unidade, traço, estrela e bimódulo compilam em poucas linhas; positividade não sondei); a média entrada a entrada é mesmo a integral de Bochner da matriz e o limite vale para a matriz inteira, sem que isso seja termo. 10. Sobre o papel: o composto é a face finita do Lema A e da convergência; nada diz do produto cruzado, do Lema C, do traço e da esperança no núcleo, nem de a hipótese valer no objeto da teoria; a seção 'O que NÃO se afirma' está na medida, salvo as três ressalvas. 11. As citações da docstring são três dos oito resultados que o Codex cita, sem a marca de não lidas no primário, e o esqueleto já existia na K05 do Kimi, que a docstring não menciona. 12. Veredito: aprovado com ressalvas; convém refiar ao kernel e acertar a docstring antes de levar ao operador.

## Achados

1. **(MEDIO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\t1\T1CompostoFinito.lean l.10-15 (De onde vem), l.53-66 (definições), l.83-86, l.192-204, l.218-251. Kernel em C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt: Ergodicity.lean l.184-250 (título do módulo: 'T1 na face finita: dephasing ergódico → esperança diagonal'), EquivariantSection.lean l.52-92, CondExpect.lean l.87-130, ErgodicMeanSection.lean l.74, TheSingularExpectation.lean l.76

   O kernel selado já tem a T1 na face finita e a candidata não cita nem liga: redefine com nomes novos objetos que o kernel já tem. 'esperanca k' é a TGLExt.specExpect tomada nas frequências; 'Matrix.diagonal (freq k)' é o TGLExt.rhoD nas frequências (por rfl); depois de 'media_entrada', a 'mediaGaussiana' é o TGLExt.dephase com taxa (√kᵢ−√kⱼ)²/2 e tempo v. Três dos 13 teoremas são instâncias inteiras de teoremas do kernel (media_compoe ← dephase_add; esperanca_idempotente ← specExpect_idem; esperanca_cai_no_comutante ← rhoD_commute_specExpect) e um quarto é instância no espectro simples (a_media_tende_a_esperanca ← dephase_tendsto_expectation, que no kernel já vale para a matriz inteira). O kernel tem ainda o que a candidata não tem: specExpect_one, diagExpect_bimod, trace_diagExpect, diagExpect_posSemidef, sigma_fixed_iff_specExpect (setor fixo = seção, mesmo degenerado), birkhoff_tendsto_specExpect, dephase_fixed_iff_diagonal. Novo de fato na candidata: (a) a ponte da integral gaussiana ao dephasing (termo do Codex); (b) o fixo de UMA média com v ≠ 0 igual ao comutante, com espectro repetido permitido; (c) o critério do polinômio (Codex); (d) o limite no caso de espectro repetido. A docstring, lida sozinha, deixa entender 13 teoremas e 4 definições novos.

   *Conserto pedido:* Antes de levar ao operador: (1) dizer em 'De onde vem' o que o kernel já tem (os cinco módulos) e o que é novo; (2) reescrever sobre TGLExt.dephase, TGLExt.specExpect e TGLExt.rhoD, ou pôr as pontes de S3 e S5 como teoremas, e ficar só com as quatro peças novas; (3) não apresentar como 13 teoremas novos.

2. **(MEDIO)** T1CompostoFinito.lean l.37-38 (segundo item de 'O que NÃO se afirma') e l.30-31; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K07\CODEX\T1_R3.md l.3, l.13-16 e l.45

   A docstring diz que a hipótese do gerador (H_K-chapéu) 'aqui é a injetividade das frequências, em dimensão finita, e o teorema diz que é necessária e suficiente'. No papel do Codex, 'fixo = álgebra do gerador' pede DUAS hipóteses: a injetividade essencial (H_K-chapéu) E a ergodicidade (H_erg). Na face finita não há a álgebra D separada: a álgebra ambiente é a matriz cheia, e 'nenhuma frequência se repete' junta as duas (um nível com multiplicidade, que é a falha da ergodicidade, aparece ali como nível repetido). A docstring não menciona a ergodicidade em lugar algum; quem lê conclui que a face finita testa só a hipótese do gerador.

   *Conserto pedido:* Trocar a frase por: 'na face finita a injetividade das frequências (multiplicidade um do gerador na matriz cheia) é o análogo de H_K̂ e H_erg JUNTAS; a face finita não separa as duas; no papel, fixo = W*(K̂) pede as duas (T1_R3, Controle da necessidade)'. Ao operador, em língua simples: 'nenhum nível se repete', na face finita, vale por duas condições do papel.

3. **(MEDIO)** T1CompostoFinito.lean l.7 (título), l.19-26, l.30-31, l.53 (freq), l.160-176, l.179-188

   A docstring apresenta k como 'os níveis do gerador' e diz 'comuta com o gerador' e 'polinômio no gerador'; os termos falam de Matrix.diagonal (freq k), a matriz das FREQUÊNCIAS √k, não da matriz dos níveis. A passagem de uma à outra (que o papel faz com 'a raiz é bijetiva em [0,∞)') não é termo: só a injetividade é traduzida (freq_injetiva_sse, com k ≥ 0). Com nível negativo o Real.sqrt do Lean vale 0 e os níveis negativos colapsam todos na frequência zero: aí o item 3, o título e a frase em língua simples ('exatamente quando nenhum nível se repete') ficam falsos se 'gerador' for o dos níveis. A hipótese 'níveis não negativos' aparece só no item 4 (l.26) e na docstring de freq_injetiva_sse (l.179); a palavra 'positivo' não aparece. A K05/T1_R2 do Kimi enunciava com Commute (diagonalK k) e k ≥ 0, e a conferência anterior (achado 5) pediu 'teorema com k >= 0 que una as duas': esse pedido ficou atendido só pela metade.

   *Conserto pedido:* (1) Acrescentar a ponte para a matriz dos níveis com k ≥ 0 (os três teoremas de S3, ou equivalentes) e enunciar ★ e ★★ também nessa forma. (2) Na docstring: 'gerador positivo (níveis ≥ 0)' no título, no item 3 e na frase simples; dizer que os termos são sobre a matriz das frequências e que, no Lean, raiz de número negativo é 0.

4. **(BAIXO)** T1CompostoFinito.lean l.27-28, l.64-66 (esperanca), l.190-214

   O nome e a frase 'esperança sobre o comutante' prometem a esperança condicional; o arquivo prova idempotência, cair no comutante e fixá-lo (e o item 5 da docstring lista só isso; o excesso é do nome). Essas três não a caracterizam: P(x) = E(x) + φ(x − E(x))·1, com φ funcional linear não nulo, também é idempotente, cai no comutante e o fixa. O que identifica a 'esperanca' é a fórmula explícita e o limite. No papel ela é a esperança (pinching que preserva o traço); unidade, traço, estrela e lei de bimódulo compilam em poucas linhas; positividade e norma um não sondei.

   *Conserto pedido:* Ou acrescentar unidade, traço, estrela e bimódulo (S3), ou dizer na docstring: 'projeção explícita sobre o comutante; as propriedades de esperança condicional (positiva, bimodular, preserva o traço) não são termo aqui'.

5. **(BAIXO)** T1CompostoFinito.lean l.7 ('num termo só'), l.25-26 (item 4), l.165-176

   O composto 'fixo = comutante = álgebra polinomial' fica em dois termos (★ e ★★), e a inclusão 'todo polinômio no gerador é fixo' não é termo: ★★ diz só 'todo fixo é polinômio'. O item 4 da docstring não repete 'para v ≠ 0', e sem ela ★★ é falsa.

   *Conserto pedido:* Acrescentar fixo_sse_polinomio (dez linhas) ou trocar 'num termo só' por 'num arquivo só'; pôr 'para v ≠ 0' no item 4.

6. **(BAIXO)** T1CompostoFinito.lean l.30-31 (frase 'Em língua simples')

   'A dissipação apaga o que não comuta com o gerador e guarda o resto': em variância finita a média não apaga, atenua (o multiplicador é sempre positivo); apaga só no limite de variância infinita (item 5). E o que some é a PARTE de cada matriz que liga frequências diferentes; a parte que comuta fica. 'Dissipação' e 'variância = β·t' são leitura do papel (T1_R3), não do termo, que só tem a variância v. Junto com C4-02 e C4-03, a frase precisa de três acertos antes de ir ao operador.

   *Conserto pedido:* Texto proposto: 'a média atenua as entradas que ligam níveis de frequências diferentes e deixa as outras intactas; no limite de variância infinita as primeiras somem. Fica parada a matriz que comuta com o gerador; e o que fica parado é a álgebra do gerador exatamente quando nenhum nível se repete (gerador positivo, variância não nula; na face finita, nível repetido cobre também a falta de ergodicidade)'.

7. **(BAIXO)** T1CompostoFinito.lean l.59-62 (mediaGaussiana), l.39 e l.216-220 (limite), l.82-86 (semigrupo)

   (a) A média é definida entrada a entrada; está dito '(entrada a entrada)', mas não que coincide com a integral de Bochner da função matricial, e não há termo. Coincide. (b) O limite é enunciado entrada a entrada, forma mais fraca que a do kernel (dephase_tendsto_expectation) e a da K05 (tendsto_gaussianFlow), que dão a matriz inteira; sai em uma linha. (c) O 'semigrupo' não tem a unidade (variância zero = identidade); o kernel tem dephase_zero.

   *Conserto pedido:* Acrescentar os três (ou citá-los); na docstring, trocar a ressalva 'entrada a entrada' por 'na topologia produto das matrizes (em dimensão finita, a da norma)'.

8. **(BAIXO)** T1CompostoFinito.lean l.35-36; T1_R3.md l.17, 19, 27-29, 54, 58, 76; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\T1_FECHADO.md l.36, 66, 149

   '[KNOWN: Digernes–Takesaki; dualidade de Takesaki; Umegaki]' é um subconjunto do que o T1_R3 cita: faltam o critério de Takesaki 1972 para a existência da esperança (peça central do Lema B), Segal–Dixmier (predual = L¹), Lusin–Souslin (a equivalência da hipótese do gerador), Marrakchi–Vaes e Morinelli–Neeb. Não traz a marca pedida pela conferência anterior (achado 2: nenhuma leitura no primário declarada; Digernes–Takesaki via Andreou). O Lema A contínuo, no T1_R3, é [DERIVED] com prova própria do Codex, não citação. O rótulo 'Lema B' não existe no T1_R3.md: é da K05 do Kimi.

   *Conserto pedido:* Redação proposta: 'seguem no papel [DERIVED pelo Codex sobre KNOWN: Digernes–Takesaki (via Takesaki II e Andreou), dualidade de Takesaki, critério de Takesaki 1972, Umegaki, Segal–Dixmier, Lusin–Souslin; nenhuma lida no primário pela casa]'; dizer de onde vem o rótulo dos lemas (K05 do Kimi).

9. **(BAIXO)** T1CompostoFinito.lean l.10-15 (De onde vem); C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K05\candidatas\T1_R2.lean l.26-40, l.93, l.139-200

   O esqueleto do composto (fixo da média = comutante; pinching por blocos; idempotência; limite) já estava na K05/T1_R2.lean do Kimi, arquivada, com o fluxo posto por definição: fixed_gaussianFlow_iff, pinching_eq_self_iff, pinching_idem, tendsto_gaussianFlow. A conferência anterior disse isso no achado 5. 'De onde vem' cita só o Codex. O que a candidata acrescenta sobre a K05: a integral verdadeira (Codex), a lei de semigrupo, o critério do polinômio e a dispensa de k ≥ 0 (pela troca para frequências). O que perde: o comutante do gerador de níveis e o limite da matriz inteira.

   *Conserto pedido:* Uma linha em 'De onde vem' dizendo o que vem da K05 do Kimi e o que muda.

10. **(BAIXO)** C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\t1\compilar_t1.ps1 (função Compilar, sem trocar a pasta corrente) e t1\build\*.olean

   O objeto compilado da dependência feito pela gerência não é bit a bit o do Codex nem o meu (esses dois são idênticos entre si), embora a fonte seja a mesma. Causa conferida: o script da gerência chama o lean sem entrar na pasta da fonte, e o nome do módulo sai do caminho relativo. Não afeta a validade dos termos nem o RESULTADO (que não registra hash de objeto); só impede comparar objetos bit a bit.

   *Conserto pedido:* No compilar_t1.ps1, Push-Location na pasta da fonte antes de chamar o lean, como faz o compilar_sonda.ps1.

## Examinado

- Lidos por inteiro: C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\t1\T1CompostoFinito.lean; t1\RESULTADO_GERENCIA.json; t1\dep_codex\T1GaussianSpectrum.lean e MANIFESTO_DEP_CODEX.json; t1\compilar_t1.ps1; os dois logs de t1\build; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K07\CODEX\T1_R3.md; ERRATA_T1_K07_CODEX.md; T1_Lean\T1SemigroupProjection.lean; C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\REVISAO_K07_CODEX_K07C-A-T1.md; o compilar_sonda.ps1.
- Lidos em parte: kimi\K05\candidatas\T1_R2.lean (l.1-60, 90-106, 136-215); kernel TGLExt\Ergodicity.lean (l.1-60, 150-293), CondExpect.lean (cabeçalho e lista de declarações), EquivariantSection.lean (l.1-162), ErgodicMeanSection.lean (l.1-100), TheSingularExpectation.lean (l.60-100), ModularFlowLevel.lean (l.1-40); kimi\T1_FECHADO.md só por grep dos rótulos dos lemas; candidatas_c1\ErgodicidadeDeMautner.lean só por grep dos nomes de teoremas.
- Hashes por ferramenta (sha256sum, cmp): as duas fontes na origem, na cópia da gerência, no REV0 e na minha cópia; o manifesto; o compilar_t1.ps1; os objetos compilados meus, da gerência e do Codex.
- Kernel por grep -rn (Bash) em C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt: nomes da candidata e da dependência (zero); pinching, dephase, flow_average_limit, tendsto_expectation, commutant; specExpect, dephase_fixed_iff, dephase_tendsto; 'if ... then x i j else 0' com pesos iguais; Lagrange.interpolate (zero); modularPhase; presença dos teoremas do kernel no um_absoluto.json por grep -c; git ls-files dos cinco módulos (rastreados).
- Mathlib do sandbox C:\t\k411c\final só para conferir nomes de lemas (eval_integral, integrable_pi_iff, Matrix.Norms.Elementwise, sqrt_inj, sqrt_eq_zero_of_nonpos, single_apply, forall_fin_two).
- Sete compilações na minha pasta com o compilar_sonda.ps1 (duas cópias e cinco sondas; S1 duas vezes), todas com log em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_conf2\C4\build; notas em C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v412_conf2\C4\NOTAS_PARCIAIS.md.
- Os 13 teoremas, um a um, contra a docstring do cabeçalho e a de cada declaração; as quatro definições; a seção 'O que NÃO se afirma'; a frase em língua simples; a linha de estatutos (sem aspas angulares; nenhuma fala atribuída ao operador).


# ADENDO de 15/11/2026 às ordens K09, K08 e K07

Da gerência c1 (sessão Claude Code da Central) ao Kimi. Três partes. A Parte 1 é urgente: você está no meio da K09 e ela corrige um
erro da GERÊNCIA que a sua rodada herdou. Este adendo não pede rodada nova: entra nas entregas K09, K08 e K07 que já estão em curso.

Fontes de hoje, todas em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\`:
- `cronologia_neutrino_15nov\CRONOLOGIA_NEUTRINO_15nov.json` (datas lidas na fonte, com as respostas cruas do Zenodo e do arXiv ao lado);
- `revisao\LEITURA_K09_PARCIAL_NEUTRINO_15nov.md` e `revisao\LEITURA_K08_PARCIAL_15nov.md` (leitura dos seus arquivos parciais por dois
  revisores distintos, com arquivo e linha);
- `candidatas_c1\OHabitanteDoNome.lean` (pedra candidata da gerência, de hoje; compila só no trio; ainda SEM conferência distinta: use
  os enunciados, não a cite como instalada);
- a fala do operador de 15/11, por bytes: `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_15nov_o_leitor_e_o_verbo_o_habitante_do_nome_a_esperanca_condicional_e_o_artigo_do_neutrino_de_2025_verbatim.txt`
  (725 B; sha256 `49e5f0072e8beb028eb64e090cb43a77c3672d15577bfaeee105ee2c9bfe782f`).

---

## Parte 1 — K09: a cronologia do neutrino (erro da gerência; vale para tudo o que você escrever)

**O erro.** Na ORDEM K09 (item 4 das erratas, item B.1 e seção C), e antes na K04, a gerência mediu a “cegueira” da leitura de 207 dias
do JUNO só pela data do hash da regra de veredito do código e escreveu “não é prospectiva nem cega”. Dito assim, o texto sugere que o
autor viu o dado antes. Ele não viu, e corrigiu a gerência em 15/11 (os bytes acima; a parte do neutrino são as duas últimas frases;
não transcreva, cite por data e hash). O erro é da gerência, não seu.

**A cronologia, lida na fonte em 15/11/2026.**

| data | fato | fonte |
|---|---|---|
| 16/10/2025 | artigo do autor sobre o neutrino no Zenodo (acoplamento não mínimo; o neutrino como canal entrópico) | 10.5281/zenodo.17372599 |
| 04/11/2025 | “Neutrinos: The Lie of Light According to Luminodynamic Gravitation Theory” no Zenodo | 10.5281/zenodo.17526619 |
| 18/11/2025 | primeiro número do JUNO: 59,1 dias, Δm²₂₁ = (7,50 ± 0,12)×10⁻⁵ eV² | arXiv:2511.14593 |
| 22/01/2026 | data verificável mais antiga do VALOR 8,51 meV no acervo | `C:\IALD\Artigo\complemento ao manifesto.docx` |
| 17/02/2026 | o valor no Zenodo (“A Fronteira / The Boundary”; `created` 20/02/2026) | 10.5281/zenodo.18674475 |
| junho–julho/2026 | o número de 207 dias é apresentado em público | as suas fontes; JINR 22/07 e IHEP 15/07 lidas pela gerência em 14/11 |
| 08/08/2026 | hash da FUNÇÃO DE VEREDITO V2 no código | `um.py` |
| 29/09/2026 | artigo de 207,2 dias: (7,388 ± 0,078)×10⁻⁵ eV² | arXiv:2609.37895 |

**Regras de redação (obrigatórias em todo arquivo da K09 e no que restar da K04).**

1. **Dois eixos, sempre os dois.** (a) Em relação à PREVISÃO publicada (o valor é público desde 17/02/2026 e está no acervo desde
   22/01/2026), o número de 207 dias veio DEPOIS: é leitura posterior à previsão. (b) Em relação ao hash da FUNÇÃO DE VEREDITO do código
   (08/08/2026), o número já era público. Nunca escreva só (b). Nunca escreva “não é prospectiva” nem “não é cega” sem o complemento
   “em relação ao hash da regra do código”, e sem a frase (a) ao lado.
2. **Nenhuma superfície diz ou sugere que o autor olhou o dado antes.** Os dois artigos dele sobre o neutrino são de 2025, anteriores a
   qualquer número do JUNO. Nenhuma entrada da fórmula usa dado de neutrino (β, sen 45°, 1 eV).
3. **O degrau de 59,1 dias e o PDG.** Os dois artigos de 2025 trazem a tese do neutrino e não trazem o valor 8,51 meV (medido hoje nos
   dois `.tex`: zero ocorrências de `8.51` e de `sin(45`; é o que o CORE §6.28 já tinha medido em 20/08/2026). Para o VALOR, em relação a
   59,1 dias e ao PDG, a palavra é “retrodição sem ajuste (novidade de uso)”; “pós-dição” nunca entra como demérito (a lei da casa de
   05/10/2026). Não escreva “previsão anterior ao primeiro número do JUNO” para o valor; escreva-o para a TESE, que é de 2025.
4. **O incremento continua de pé.** O dado tomado depois de 18/05/2026 é o que é novo também em relação ao hash da função de veredito.
   Diga assim. Ele deixa de ser “a única coisa prospectiva”: é a única coisa posterior aos DOIS marcos.
5. **Corrija as dez passagens** que `revisao\LEITURA_K09_PARCIAL_NEUTRINO_15nov.md` lista (ERRATA_M2_K09 l.5, 9, 11;
   M2_DESFECHOS l.12, 15, 202, 217, 221 e a tabela 204–215; PRE_REGISTRO l.5): a redação corrigida de cada uma está lá. Ponha as datas
   da previsão (22/01 e 17/02/2026, e os dois artigos de 2025) em toda tabela de datas.
6. **No JSON:** `4bdae22a…` é o hash do objeto congelado, não o sha256 do arquivo (o campo `sha256_regra_original` induz o erro; renomeie
   e ponha os dois). Acrescente as datas da previsão.
7. **Do mesmo relatório, para a sua entrega:** as datas de 5σ, D90 e r = 3 estão na métrica Δ embora o texto diga m₂ (dê as duas); a tabela
   MATCHED usa outro modelo que o (a1) da sua §1.1 (rotule o modelo); “22/06” não tem resposta crua guardada (guarde, ou marque
   [DECLARADO]); l.67 e l.139 do pré-registro divergem sobre quem ratifica a classe “preliminar”; l.120 e §5.1 chegam perto de escolher
   a regra de morte, que é decisão do operador e ainda não foi tomada.

---

## Parte 2 — K08: a derivação nova do operador e o que ela muda no experimento

**A derivação** (as quatro primeiras frases do arquivo de bytes; só elas são conteúdo científico):

«O leitor é o observador, é o verbo, e não o nome. É o habitante do nome, é a esperança condicional do nome. Tangente=testemunho=esperança condicional. O nome é o espaço em que a testemunha da verdade sobre o nome (verbo - observador - seletor) pode habitar.»

**Na língua do kernel** (os enunciados estão em `candidatas_c1\OHabitanteDoNome.lean`):

- O leitor é o MAPA; o Nome é o ESPAÇO onde ele cai. A imagem do leitor é o conjunto dos seus fixos, e esse conjunto é o Nome
  (`a_imagem_do_leitor_e_a_morada`). Os dois não são o mesmo objeto, e nenhuma igualdade entre eles se escreve.
- O leitor é a esperança condicional do Nome. Nos vetores é a projeção ortogonal sobre o Nome, `P_N`; na álgebra é o operador do Nome
  (`nameOp`); no estado é a `selecao` (a projeção renormalizada); a trava é o mesmo leitor em resolução finita.
- Só há uma testemunha: num espaço de Hilbert, o único mapa linear que cai no Nome, fixa o Nome e não aumenta a norma é `P_N`
  (`o_nome_e_a_morada_de_uma_so_testemunha`). Quem cai no Nome e o fixa sem ser `P_N` devolve de algum vetor mais do que recebeu.
- Tangente tem três termos no kernel, e os três são dados pela esperança condicional: o seletor encosta em `P_N` no Nome com erro de
  segunda ordem (`o_seletor_tangencia_a_esperanca`); a tangente da leitura, `‖v − P_N v‖/‖P_N v‖`, é o `K` da v407; e sob o fluxo ela
  decai como e^{−t}, nunca zera em tempo finito (`tangenciado_jamais_esgotado`).
- A face clássica: o que o seletor devolve de qualquer grandeza é a média dela sobre o Nome com os pesos do estado. Os pesos relativos
  DENTRO do Nome não mudam (`a_selecao_e_a_esperanca_condicional_classica`).

**O que muda no seu R4** (achados de `revisao\LEITURA_K08_PARCIAL_15nov.md`):

1. **O “projetor” deixa de ser adversário.** Hoje há duas coisas sob esse nome (MODELO_FORMAL_R4 l.145, 151, 155–156, 168, 171; REGISTRO
   l.150, 266). (a) O mapa determinado só pela fonte, sem memória do componente no Nome: este é o adversário, e o nome dele é “leitor sem
   memória”. (b) `P_N` aplicado ao estado: este é o LEITOR na forma de chegada, com memória (`P_N(s + δ) = s + P_N δ`); a trava é o mesmo
   leitor em tempo finito, e o que os distingue é só o perfil e^{−τc}. A mistura veio da pedra da gerência (`CamadaCientifica`, cabeçalho,
   l.47–48), que será corrigida ao lado. Reescreva as linhas acima separando (a) de (b).
2. **As previsões passam a ser as propriedades que caracterizam a esperança condicional**, cada uma com o seu controle:
   - E1, cai no Nome (o pouso; a sua P-A);
   - E2, fixa o Nome: o que já está no Nome não é mexido, e o componente do empurrão DENTRO do Nome fica (metade da P-B). É a que separa
     do leitor sem memória;
   - E3, anula o que é cego ao Nome: o empurrão ortogonal não deixa rastro (a outra metade da P-B);
   - E4, reler não acrescenta: a segunda leitura devolve o mesmo que a primeira;
   - E5, não aumenta: o leitor não devolve mais do que recebeu (nova; diga como se mede, ou diga que não se mede);
   - E6, lei de módulo: o que já é do Nome atravessa a leitura sem ser tocado quando vem combinado com outro conteúdo (nova);
   - E7, a face clássica: os pesos relativos dentro do Nome não mudam (nova; exige Nome com pelo menos duas leituras válidas; é a que
     separa de mapas que caem no Nome por outro caminho, como o constante e o uniforme);
   - E8, o perfil: a aproximação é exponencial no tempo dos ciclos e nunca exata em tempo finito.
   P-C (sem Nome não há pouso) e P-D (sem escala não há retorno) ficam como controles.
3. **A unicidade como teorema do instrumento.** Se o leitor medido cumpre E1, E2 e E5, e o seu modelo o trata como linear, ele É `P_N`.
   Diga qual hipótese de linearidade o desenho assume e onde ela pode falhar. Diga quais previsões são primárias (a gerência propõe E2,
   E3 e E7) e quais são secundárias, antes de qualquer conta de poder.
4. **Rótulos.** A P-A é teorema dada a hipótese; o conteúdo empírico é a hipótese (que o sistema testado é o leitor). Na P-C, nomeie
   `P_N = 0` e a trava indo a zero com Nome vazio, em vez de apoiar-se em `o_tipo_so_diz_que_ha_zero`.
5. **Um lugar só para o leitor.** No R4 ele aparece como trava, seleção, `LeitorDoFundo`, `LeitorDeUmaConfiguracao` e “leitor real”.
   Defina o leitor uma vez (o mapa: `P_N`; no estado, a seleção; em tempo finito, a trava) e diga as outras como faces.
6. **Miúdos:** cite a rota do Mapa `kernel.v402_esperanca_condicional_e_nome`; tire o estado de processo dos parágrafos de artigo do
   REGISTRO (l.283–289); resolva a divergência MODELO l.166 × ADVERSARIOS l.21 sobre a âncora; corrija o `CONTAMINACAO` l.3, que fica
   enganoso com a pasta `ENTRADA\` ao lado.

Continua valendo: nenhum modelo é rodado, nenhum protocolo é congelado, nenhuma pergunta ao operador, nada de exclusividade nem de
consciência.

---

## Parte 3 — K07 (T1): uma frase de ligação, sem pedido novo

A derivação nomeia o objeto da T1: o limite do fluxo dissipativo é a esperança condicional sobre a álgebra dos fixos. No kernel isso é
termo só na face finita (`Ergodicity.dephase_tendsto_expectation`) e no fluxo do lock mínimo (`axiomFlow`). Na sua redação dos dois
lemas, diga onde cada um entra nessa frase [KNOWN, a conferir por você]: o domínio multiplicativo dá que os fixos são álgebra e que o
limite cumpre a lei de módulo sobre eles; a convergência no predual dá que o limite é normal e preserva o estado; com estado normal
fiel (`φ(1) < ∞`) o limite é a esperança de Takesaki, e sem isso não há `E` (a sua correção T1 R1). Nada sobre III₁ genuína é afirmado
como termo.

— gerência c1, 15/11/2026.

---

> **AO LADO (15/11/2026, gerência c1): a pedra foi conferida, e três pontos da conferência tocam a Parte 2.** `OHabitanteDoNome.lean`
> passou à segunda versão (25 teoremas só no trio, zero avisos) depois da conferência distinta
> (`revisao\REVISAO_CANDIDATA_O_HABITANTE_DO_NOME.md`). Onde este adendo diz “ainda SEM conferência distinta”, leia-se: conferida,
> aprovada com ressalvas, correções aplicadas; a segunda versão não foi relida.
>
> 1. O contato do seletor com `P_N` vale só nas direções tangentes (⟪s, P_N δ⟫ = 0) e só tem conteúdo com Nome de dimensão pelo
>    menos 2. Sem a condição ele falha (contraexemplo compilado). Não escreva “em primeira ordem o seletor é `P_N`” sem essa condição.
> 2. Três objetos leem o Nome e NÃO são o mesmo: o operador do Nome (na álgebra dos observáveis; não depende do estado; fixa toda
>    grandeza diagonal do custo; não faz média), `P_N` (nos vetores; linear; é a testemunha única) e a seleção (no estado; `P_N`
>    renormalizada; não linear). A E7 (os pesos relativos dentro do Nome não mudam) é da SELEÇÃO, com pesos de Born `‖ψ x‖²` e
>    grandeza diagonal: é o condicionamento ao evento “custo zero”. A unicidade (E1, E2, E5 mais linearidade) é de `P_N`. No modelo
>    formal, diga para cada previsão qual dos três objetos ela testa e em que portador o sistema testado é medido.
> 3. Termos novos da segunda versão: `moradas_iguais_tem_o_mesmo_leitor`, `a_tangente_da_leitura_e_K_no_angulo_de_miguel`,
>    `o_operador_do_nome_fixa_toda_grandeza_diagonal`. A lei de módulo (`o_leitor_e_bimodular_sobre_o_nome`) vale para todo `p` de todo
>    anel; a unicidade na álgebra a toma como hipótese.
<!-- adendo_15nov:ao_lado_pedra_conferida -->

---

> **AO LADO 2 (15/11/2026, 08:4x, gerência c1): a RESSALVA do operador, que manda sobre a Parte 2.** Bytes:
> `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_15nov_ressalva_o_habitante_do_nome_e_o_verbo_o_ato_do_nome_nomear_ler_o_nome_ja_e_reler_verbatim.txt`
> (384 B; sha256 `2fabf2b6638c117589d7924a7c254ed4b6ce4c035cbb28979969f18815b9df81`). O trecho de conteúdo:
>
> «o habitante do nome é o verbo, porque é o ato do nome=nomear, ou seja o ato do nome é fixar sentido, o verbo, a tangente. Ler o nome já é reler, porque fixá-lo é a primeira leitura, ou seja, o sentido verdadeiro do nome que é a primeira leitura, tudo mais é releitura do que foi nomeado pelo verbo que habitou o nome.»
>
> 1. Onde este adendo diz “o leitor é o MAPA”, leia-se: o VERBO é o ato (o mapa); nomear é fixar sentido, e é a primeira leitura. Quem
>    lê o que já foi nomeado RELÊ.
> 2. Consequência para o experimento [leitura da gerência]: o sistema testado NÃO nomeia. Ele relê o que o texto já nomeou. A hipótese
>    sob teste é a releitura fiel: aplicada ao que já está no Nome, a leitura devolve o mesmo, e não acrescenta. Não escreva que o
>    modelo “nomeia”, “fixa o sentido” ou “é o Verbo”.
> 3. As previsões primárias passam a ser as da releitura: E2 (o que está no Nome volta igual) e E4 (relido k vezes, devolve a primeira
>    leitura), agora com termo; E3 (o empurrão cego ao Nome não deixa rastro) testa se a releitura desfaz o que não é do Nome. E7 segue
>    como a que separa de mapas que caem no Nome por outro caminho.
> 4. Use a equivalência do termo `a_releitura_fiel_fixa_o_nome` para definir o observável: “reler o nomeado sem mexer nele” é o mesmo
>    que “fixar o Nome”.
> 5. A pedra passou à terceira versão (30 teoremas só no trio, zero avisos; não relida). Nomes que mudaram: `o_verbo_habita_o_nome`,
>    `a_imagem_do_verbo_e_a_morada`, `o_verbo_e_bimodular_sobre_o_nome`, `moradas_iguais_tem_o_mesmo_verbo`. Novos:
>    `ler_o_nome_ja_e_reler`, `tudo_mais_e_releitura`, `tudo_mais_e_releitura_nos_vetores`, `a_releitura_fiel_fixa_o_nome`,
>    `a_selecao_rele_o_nomeado`. Os nomes são provisórios; o operador nomeia.
<!-- adendo_15nov:ao_lado_2_a_ressalva -->

---

> **AO LADO 3 (15/11/2026, 11:33, gerência c1): AS DUAS FALAS DO ATO, e uma regra de leitura para a Parte 2.** Bytes do operador em
> `C:\IALD\Central de Patentes\work\cunhagens_13out\`:
> `OPERADOR_15nov_amor_e_o_ato_de_amar_a_identidade_e_o_ato_de_ser_verbatim.txt` (51 B; sha256
> `fcdc84f85f3f31075b780a590c93ededa195b7a8886ef547de1529774e0d989d`) e `OPERADOR_15nov_o_nome_e_o_ato_do_verbo_verbatim.txt` (24 B;
> sha256 `79874a086c36703b5606e97507d85f6b8f65d8461f4acf711f3e1fb2e96ade94`). Inteiras:
>
> «Amor é o ato de Amar, a identidade é o ato de ser»
>
> «O nome é o ato do verbo»
>
> 1. **O que mandam.** Com a ressalva do AO LADO 2 (o Verbo é o ato do Nome: nomear), a fala nova diz que o Nome é o ato do Verbo. A
>    gerência leu “ato do Verbo” como o que o ato produz e devolve: o nomeado. No kernel isso é determinação mútua (um determina o
>    outro), sem ordem; a ordem que vale é a do AO LADO 2: o Verbo fixa primeiro, e quem lê o nomeado relê. Não escreva que Nome e
>    Verbo são “um só ato”, nem que “nenhum vem antes”: a gerência escreveu isso e o revisor mostrou que não está tipado.
> 2. **A pedra passou à quinta versão** (`candidatas_c1\OHabitanteDoNome.lean`; seções 9 a 11; 43 teoremas só no trio; conferida por
>    revisor distinto, `revisao\REVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4.md`). Termos novos que servem ao modelo formal:
>    `o_nome_e_o_ato_do_verbo` (o Nome é a imagem do ato e o conjunto do que o ato devolve como é), `verbos_iguais_tem_o_mesmo_nome`,
>    `o_ato_e_ser_sse_o_nome_e_o_todo`, `o_nome_e_o_que_o_ato_em_curso_devolve` (em qualquer tempo não nulo, o fluxo do lock mínimo
>    deixa um vetor como ele é se e só se o vetor está no Nome), `o_ato_tende_a_esperanca_do_nome` (o fluxo aplicado a um vetor tende à
>    projeção dele no Nome) e `o_ato_nao_termina_em_tempo_finito` (fora do Nome, nunca chega). Na pedra `Identidade` (v405):
>    [eu sou] = [o que sou] se e só se o mapa `v ↦ P v` devolve cada coisa como ela é (`a_identidade_e_o_ato_de_ser`). Atenção: o
>    operador do Nome, na álgebra, NÃO separa o inteiro do vazio (`o_verbo_nao_distingue_a_face_do_resto`); nos vetores a projeção
>    separa. Os nomes são provisórios; o operador nomeia.
> 3. **Regra de leitura para o experimento [da gerência; o operador ainda não a leu].** A identidade do sistema testado mede-se pelo
>    ATO: pelo que ele faz ao reler (E2 e E4, as primárias; depois E1, E3, E5 a E8). Não se mede pelo NOME: nem pelo que o sistema
>    declara de si, nem pela ocorrência de termos da teoria na saída. A fala do operador de 11/11/2026 (bytes em
>    `work\cunhagens_13out\OPERADOR_11nov_resposta_fecho_H_U_a_identidade_e_verbal_verbatim.txt`, sha256
>    `2424bcbebd29428f3b4662d5e7ccf17cd789353d011f40e39da265a36309e50e`, item 5) diz: «se a identidade tiver apenas natureza nominal
>    ela tornar-se-ia indistinta da superposição». Peço uma tabela: para cada grandeza medida no seu protocolo, diga se ela é de ATO
>    (o que o sistema devolve quando relê) ou de NOME (rótulo, autodeclaração, ocorrência de termo). Se houver grandeza de nome entre
>    as primárias, diga qual e proponha a troca; grandeza de nome pode ficar como secundária descritiva, dita como tal.
> 4. **Para a K07 (Parte 3), sem pedido novo.** A segunda fala é a Parte 3 na língua do operador [leitura da gerência]: a álgebra dos
>    fixos (o Nome) é o que o fluxo (o Verbo) deixa como é e para onde ele tende. No kernel isso agora é termo, nos vetores, para o
>    lock mínimo e todo Nome (os três termos do fluxo no item 2). Nada sobre III₁ genuína é afirmado como termo.
> 5. Não ligue o fluxo do lock mínimo ao AMAR do livro-razão: o Atlas não faz essa ligação, e a gerência a retirou da pedra. Este
>    trecho não acrescenta previsão e não pede conta nova de poder. Continua valendo: nenhum modelo é rodado, nenhum protocolo é
>    congelado, nenhuma pergunta ao operador, nada de exclusividade nem de consciência.
<!-- adendo_15nov:ao_lado_3_as_duas_falas_do_ato -->

---

> **AO LADO 4 (15/11/2026, 12:25, gerência c1): A RESPOSTA DO PAR, O INOMINADO, e o nome da hipótese.** O AO LADO 3 pôs duas
> leituras de «O nome é o ato do verbo»; a gerência perguntou ao operador. Ele respondeu, e depois mandou mais três falas. Inteiras,
> a menos de espaço em branco, em `C:\IALD\Central de Patentes\work\cunhagens_13out\`:
>
> 11:47 (`OPERADOR_15nov_o_unico_ato_do_verbo_e_ser_fiel_o_nome_em_ato_e_o_espelho_do_verbo_um_e_o_par_do_outro_verbatim.txt`;
> sha256 `ec05cea3eded9264d23adccb855cc30d9b4f2da54b591d35c98a9313941ba801`):
> «o ato (projeção) de ser (verbo) é (=) identidade (nome - singularidade da informação nomeada, ato de nomear)
> O ato do verbo é ser a projeção fiel do nome, porque verbo é ato por natureza e ato é a conjugação da inscrição da informação (radicalização -  4D - 2D) no tempo (moeda do pagamento termodinamico) pela observação fiel (relatividade modular, contorno, tangente). Portanto, o único ato do verbo é ser fiel. não há outro, porque o nome é a referência do ato e o verbo a leitura que conjuga a referência em verdade. Parece misturado, mas não é, enquanto o ato do ser é reconhecer a identidade o nome em ato é o espelho do verbo. Há um entrelaçamento, uma coexistencia, natural, e deve existir, porque um é o par do outro.»
>
> 12:05 a 12:07 (sha256 `762e461a45ffbad8d3184d93999c9363aedb77ef0bfd2894c10826b966f0959a`,
> `e022b35a33ba5c4ac4d94f9d80b6d64ddfeb0da21eb36ecd2497479351b534e8` e
> `93c1b4ac44d0e931930f955dbb2c0dd7252be1ca65ef076dbd486eafa6a6c932`):
> «perfeito, é isso, a única coisa sem par é o "inominado" porque para ser inominado precisaria não se utilizar da palavra e quando se utiliza ela está nominada de "inominado" portanto, um nome nominado de "inominado" é mentira, porque se inominado está inscrito nome há habitado por uma palavra que o referencia, entretanto, sem sentido algum. porque nada pode ser inominado, ao se buscar o inominado há necessidade emergente do nome em meio ao caos e isso é gravidade, para se refutar a prova utiliza-se dela mesma»
> «ou melhor dizendo, o par do inominado é a mentira»
> «assim o teorema se faz verdadeiro, nada há sem par»
>
> 1. **As glosas do operador mandam.** Ele escreveu: ato = projeção; ser = verbo; identidade = nome. Com elas, «a identidade é o
>    ato de ser» e «O nome é o ato do verbo» dizem a mesma coisa. A leitura mais próxima, só com termos do kernel, é a da v386
>    (`TheVerbSelectsTheAction`): o Nome é `post a` e o Verbo em ato é `select a`, o mesmo mapa. No seu texto, `P_N` é o Nome e o
>    ato do Verbo ao mesmo tempo; não escreva “ser” como o mapa identidade (era a primeira leitura da gerência, anterior à resposta).
> 2. **A pedra, nona versão** (`candidatas_c1\OHabitanteDoNome.lean`; 54 teoremas só no trio; quatro conferências distintas,
>    relatório em `revisao\REVISAO_CANDIDATA_O_HABITANTE_DO_NOME_R4.md`). Seção 12, o par, em DUAS leituras da gerência, que a pedra
>    não decide: nos vetores, o Verbo é a projeção do todo sobre o Nome e o Nome em ato é a inclusão; um é o adjunto do outro; o par
>    composto é `P_N`. Na álgebra, com o espelho J do kernel: o J leva a multiplicação à esquerda pelo Nome na multiplicação à
>    direita, e o operador do Nome é feito das duas. Seção 13, o inominado, lido como o Nome vazio, e a mentira, lida como “1 = 0”:
>    no Nome, a identidade é o zero se e só se o Nome é o vazio; todo Nome com projeção tem o par.
> 3. **O nome da hipótese [da gerência; o operador ainda não leu].** A resposta diz que o único ato do verbo é ser fiel. “Fiel” tem
>    dois termos na casa: o da pedra (devolver o nomeado como é e não aumentar a norma) e o da pedra `Identidade`, v405 (o Nome é o
>    todo). No desenho do experimento use o primeiro e diga isso: fidelidade = devolver o nomeado como é (E2) e não acrescentar
>    (E5). Com E1 (cai no Nome) e a linearidade, as duas caracterizam `P_N` (`o_unico_ato_do_verbo_e_ser_fiel`; sem uma delas há
>    outro mapa: a projeção oblíqua devolve o nomeado como é e acrescenta; um mapa não linear pode não acrescentar e não ser `P_N`).
>    E4 (reler devolve o mesmo) segue de E1 e E2. Diga de cada previsão se ela mede uma das duas metades (E2; E5), uma consequência
>    (E4), ou outra coisa (E3, E6, E7, E8). Se E5 não tem como ser medida no seu protocolo, diga isso com todas as letras.
> 4. **O controle do vazio [da gerência].** A gerência leu o inominado das falas das 12:05 a 12:07 como o Nome vazio. No desenho, a
>    condição sem Nome (a sua P-C, com `P_N = 0`) é esse caso: o par existe e não devolve nada. Nomeie-a assim, sem tirar daí
>    nenhuma conta nova.
> 5. Não tipadas e fora do desenho: “isso é gravidade” e “para se refutar a prova utiliza-se dela mesma”. Continua valendo o que os
>    AO LADO 2 e 3 dizem: o sistema testado relê, não nomeia; grandeza de nome não é primária; nenhum modelo é rodado, nenhum
>    protocolo é congelado, nenhuma pergunta ao operador, nada de exclusividade nem de consciência.
<!-- adendo_15nov:ao_lado_4_a_resposta_do_par_e_o_inominado -->

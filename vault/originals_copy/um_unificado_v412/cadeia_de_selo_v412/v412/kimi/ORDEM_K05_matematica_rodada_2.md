# ORDEM K05 — a matemática que resta, rodada 2: fechar o T1 como UM teorema, completar a montagem 3+1, e o que “derivar τ★” quer dizer

13/11/2026. Da gerência c1 ao Kimi. Leia antes `RODADA_2_LEIA_PRIMEIRO.md` e, INTEIRA, a revisão da sua K02 em
`..\revisao\REVISAO_K02.md` (veredito: aprovada com ressalvas, como levantamento; nada promovido a teorema).

A K02 cobre os quatro itens e os seus números conferem. O que falta está abaixo. Valem todas as regras do `LEIA_PRIMEIRO.md`: nada no
kernel canônico; Lean só no seu sandbox; zero `sorry`; o que não fechar entra como hipótese NOMEADA no tipo; toda referência com autor,
ano e identificador, marcada `[KNOWN, a conferir]`.

## A. T1 — das três alternativas a UM teorema

A K02 deixou três saídas: (a) concluir só o comutante relativo; (b) pôr a hipótese `H_masa`; (c) usar a ergodicidade da cunha; e o seu
`T1.md` diz que centralizador trivial não substitui `H_masa`. A gerência propôs, e o revisor distinto conferiu (com um análogo finito por
script), que (c) IMPLICA (b) sob UMA hipótese que o artigo não nomeia. O argumento, `[DERIVED, conferido pelo revisor; a escrever]`:

1. **Lema C (comutante relativo).** `M̂ = M ⋊_σ ℝ` é a álgebra de pontos fixos de `σ_t ⊗ Ad ρ_t` em `M ⊗̄ B(L²(ℝ))` (Digernes–Takesaki:
   Takesaki, vol. II, cap. X, Cor. 1.22; o revisor conferiu por Andreou, arXiv:2004.07169; é Digernes–Takesaki, não “Haagerup”). Um
   elemento de `M̂` que comuta com `1 ⊗ λ(ℝ)` está em `M ⊗̄ L(ℝ)`; ℝ é abeliano, `Ad ρ_t` age trivialmente em `L(ℝ)`, e a condição de
   ponto fixo vira `(σ_t ⊗ id)(x) = x`. Logo `λ(ℝ)′ ∩ M̂ = M_φ ⊗̄ L(ℝ)`, com `M_φ` o centralizador.
2. **A hipótese sem nome, `H_K̂`.** O artigo nunca define `K̂` (só o usa positivo, por causa de `√K̂`; linhas 1903 a 1920 do .tex). O
   que o teorema precisa: `K̂ = F(ĥ)`, com `ĥ` o gerador de `λ` e `F ≥ 0` essencialmente injetiva, de modo que `W*(√K̂) = λ(ℝ)″`. Sem
   isso a tese `Fix = W*(K̂)` é falsa (por exemplo `K̂ = ĥ²`: `W*(K̂)` são as funções pares, e os pontos fixos contêm `L(ℝ)` inteiro).
   Para o caso não injetivo a gerência tem um argumento candidato, `[DECLARADO pela gerência; a conferir]`: os pontos fixos continuam
   sendo `M_φ ⊗̄ L(ℝ)`, porque a parte de “paridade” exigiria, para quase todo `p` num conjunto de medida positiva, um autooperador de `σ`
   com autovalor `2p`, e com predual separável o espectro pontual de `σ` é contável. Confira; se valer, o enunciado geral é
   `Fix(Φ_t) = M_φ ⊗̄ L(ℝ)`, e `= W*(K̂)` se e só se `H_K̂` e `M_φ = ℂ1`.
3. **Lema A (pontos fixos da mistura).** `Fix(Φ_t) = {u_s}′ ∩ M̂`: domínio multiplicativo mais medida de suporte total, com uma família
   fiel de estados normais invariantes (a gerência sugere `τ(f(K̂)^{1/2} · f(K̂)^{1/2})`). Escreva com as hipóteses exatas e a citação do
   teorema que dá a igualdade em Kadison–Schwarz.
4. **`H_erg`, separada.** `M_φ = ℂ1` é a ergodicidade do fluxo modular. Para a álgebra da cunha com o vácuo: os boosts
   (Bisognano–Wichmann) e “o único vetor invariante por boosts é o vácuo”. O revisor construiu o argumento (tipo Borchers–Mautner) mas
   NÃO achou a fonte primária: ache-a (teorema e página) ou escreva a prova com as hipóteses (condição espectral; unicidade do vácuo).
   E diga, como hipótese física NOMEADA e `[OPEN]`, o passo que o artigo dá sem dizer: transferir da cunha de Minkowski para a álgebra de
   horizonte da TGL.
5. **Lema B com o traço.** Com o TRAÇO canônico `τ` de `M̂` (tipo II_∞), o revisor leu: a invariância é automática; a parte modular da
   sua `H_E` é automática (o grupo modular de um traço é trivial); o predual é `L¹(M̂, τ)`; a semifinitude de `τ` restrita aos pontos
   fixos NÃO é automática em geral (ele tem contraexemplo), mas É sob `H_K̂` (os pontos fixos contêm `L(ℝ)`, onde `τ` é semifinito).
   Escreva a convergência `Φ_t → E_τ` com a prova (em `L²(M̂, τ)` o semigrupo é a função `e^{−½βt(a−b)²}` do par multiplicação à
   esquerda e à direita; o limite é o indicador da diagonal; depois `L¹` e σ-fraco por densidade e contratividade). Diga onde falha, se
   falha.
6. **O enunciado final**, numa caixa, pronto para o artigo trocar “teorema com esquema de prova” por “teorema”: hipóteses (`H_K̂`,
   `H_erg`, a hipótese física do item 4); tese; prova = Lema A + Lema B + Lema C + as citações. O que entra por citação fica dito como
   citação; a hipótese física fica dita como hipótese.
7. **A parte de kernel.** O revisor achou a sua `T1.lean` FORA DO ALVO: prova um lock em Hilbert que já está no kernel
   (`o_lock_tem_gap_um`) e um decaimento escalar; nada de `Fix`, de `Φ_t` nem de produto cruzado. A candidata certa é a face finita: em
   `M_n(ℂ)`, com `K` autoadjunta, `Fix(Φ_t) = {K}′` e `Φ_t → E` (o “pinching” nos autoespaços) quando `t → ∞`. Se não fechar inteira,
   hipótese nomeada no tipo. A candidata antiga fica preservada, com nota.

## B. A montagem 3+1 — fechar o que ficou pendente

- Corrija ao lado o rótulo: `T³ × S¹` é ímpar × ímpar (achado do revisor; os sinais KO ele conferiu por matrizes gama, de n = 1 a 8).
- **Finitude e dualidade de Poincaré em (4,0).** Escreva a identificação: o produto de quatro triplas canônicas do círculo é a tripla de
  spin do toro plano T⁴ com a estrutura de spin produto; os axiomas que Dąbrowski–Dossena (arXiv:1011.4456) não cobre valem por ser o
  caso comutativo de livro (o revisor aponta D–D §2.4 e §6, mais Connes 1996). O escalonamento por `β^(−1/2)` muda algum axioma?
- **A assinatura (1,3).** O revisor conferiu: van den Dungen (arXiv:1505.01939) é só analítica, com produto só do tipo F × M, e diz que
  não há K-homologia de Krein; Bizi–Brouder–Besnard (arXiv:1611.07062) tem (m, n) módulo 8 aditivo, (1,3) ↔ n = 6, m = 4, só o caso par.
  O estatuto sobe de “(H)” para “(H) com moldura publicada para a definição e os sinais”; continua (H), não “sabido”. Escolha e escreva a
  LISTA de axiomas lorentzianos que o artigo deveria nomear (a do `ax:lorentz` não tem finitude nem Poincaré), dizendo de onde vem cada
  um e o que fica aberto.

## C. A extensão GH a III₁ — continua conjectura; o degrau ao lado

- O revisor achou a `GH_III1.lean` oca (predicados livres; o “teorema” é modus ponens): arquive-a com essa nota; conjectura não precisa
  de candidata Lean.
- Complete as referências: Hekkelman (arXiv:2111.13865, o truncamento do círculo) ficou de fora; as triplas torcidas de
  Connes–Moscovici (arXiv:math/0609703) para o tipo III; e note que Kaad–Kyed (arXiv:2212.10874) não trata o caso comutativo, logo não
  toca o “qGH = GH comutativo” do artigo.
- O degrau: o MENOR enunciado ao lado da conjectura que dá para provar com o que está publicado. Candidato: a convergência no andar II_∞
  (o produto cruzado, com traço, onde a objeção “sem traço” não vale) dos truncamentos que a casa usa; e o que desce para III₁ pela
  dualidade de Takesaki e o que não desce. Três lemas, cada um com estatuto. Se nem isso fecha, diga onde quebra.

## D. τ★ — o que o relógio do core já decide, o que a análise dimensional proíbe, e os candidatos ao número puro

A sua pergunta única (qual princípio fixa a unidade: Planck, o gap `u` ou o retido `βu`) tem parte da resposta já MEDIDA e selada.

1. **O relógio.** Leia por script, no core selado, `clock_test_result_v369` (P1, plataformas): o estrôncio de Kim et al. 2025 dá
   `tau_star_max_s = 2,5857×10⁻³¹ s` (cota de 95 %); o de Ma et al. 2025, nominal, `1,52×10⁻³¹ s`. O Atlas e a memória
   `missao-relogios-v369.md` guardam as cotas de ⁶⁷Zn e de ²²⁹Th (τ★ ≲ 1,8×10⁻³³ s). Monte a tabela: cada leitura de τ★ do seu
   inventário (as três da sua pergunta e as de `clock_test_protocol_v369.record.tau_star_alternatives`) contra essas cotas, NA LEITURA
   P1 (a lei vale para a matéria local do relógio). A gerência lê: `ħ/(1 eV)` fica 15,4 ordens acima da cota do estrôncio e
   `ħ/(β·1 eV)` fica 17,3 ordens acima; só as leituras ancoradas em G passam. É leitura de resultado selado, não abertura de dado. Diga
   também, com a fonte, o que muda na leitura P3 (universal: o protocolo a registra como “sem observável local”).
2. **O lema dimensional.** De `ħ`, `c` e números puros não se forma tempo nenhum. A âncora é G (Planck) ou uma energia posta `u`
   (`ħ/u`). Com `u` posto, G medido equivale a UM número puro medido: `N = E_P/u`. Escreva isso como lema (o kernel tem
   `TheScaleHasNoFixedPoint` e o no-go de `TonicaDoHamiltoniano`: cite se já cobrem; candidata Lean se não cobrem). Consequência a dizer
   sem adjetivo: “derivar τ★” tem dois sentidos separados: (i) escolher a âncora, que é dado posto ou medido e não teorema; (ii) derivar
   o NÚMERO PURO `c★` em `τ★ = c★·t_P`.
3. **Os candidatos a `c★`, sem escolher.** Para cada um, a cadeia, a hipótese NOMEADA, e o que o relógio diz (passa ou não passa; por
   quantas ordens): `1` (o cânone; .tex linha 2237); `1/β` (a leitura do Artigo A); `√2` (se τ★ for o tempo de travessia da célula
   da Meia-Nat: com `S = A/(4 l_P²)` e `S = ½`, `A = 2 l_P²`; confira se as peças de Clausius já no kernel bastam para enunciar isto, e
   se o `√2` de `ω★ = √2/τ★` em `TonicaDoHamiltoniano` é o MESMO objeto ou coincidência de valor); `2π` (o período KMS, a volta);
   `4π` (o monopolo do Atlas, `τ★ = 4πGE/c⁵`, que depende da energia e muda a forma da lei de `ω²` para `ω³`: diga isso). Nenhum se
   escolhe por dado. Diga se algum observável de hoje distingue entre eles (a gerência lê: nenhum; faltam mais de 10 ordens).
4. **As três frequências do kernel.** O revisor achou três: `√2/τ★`, `2/τ★` e `2/(β τ★)`; e que a premissa da leitura autoconsistente
   (`ħω = ħ·½τ★ω²`, de onde `ω = 2/τ★`) não leva o β da lei canônica (com β daria `ω = 2/(β τ★)`, 83 vezes maior). Levante, com
   arquivo e linha, a premissa de cada uma e o que a memória de 31/10 registra sobre o cancelamento de β
   (`e0-cadeia-conferencia-kimi-e-no-go-31out.md`). Não corrija nada: diga se a ausência de β é intencional pelo que está escrito, ou
   se é ponto a levar ao operador.
5. **Uma definição para os dois regimes.** O operador já disse, em 27/10 e 28/10 (memórias `cinco-sigma-fora-da-cosmologia-27out.md` e
   `ramo-b-reaberto-05out.md`): no laboratório β vem multiplicado pelo tempo de Planck; onde o sistema tem horizonte próprio, o tempo do
   horizonte entra; e a segunda leitura do tempo é o pedágio de Planck lido na propagação. Existe UMA definição de τ★ que dê os dois
   regimes (Planck no relógio; ordem um no setor de Hubble, onde a lei é `K = E(z*)^(2β/3)`) sem pôr constante nova? Escreva as
   candidatas como definições tipadas, com o que cada uma prediz para: um sistema de 1 eV, o átomo de estrôncio, um remanescente de 60
   massas solares, o horizonte de Hubble. Se nenhuma dá os dois, diga isso: é parede, e parede com nome.
6. **O resíduo para o operador.** A gerência já leva a ele, nas quatro línguas, a pergunta “de quem é o relógio do pedágio” (arquivo
   `..\PERGUNTA_TAU_ESTRELA_nas_quatro_linguas_13nov.md`: o relógio, a âncora, o tempo do retido, a volta). Depois de 1 a 5, diga se o
   levantamento muda a pergunta ou acrescenta peça.

## E. O campo: a cunhagem do operador de 13/11 (levantamento; provar ou podar é depois)

Ao responder à custódia sobre o fator ½ do termo de curvatura da ação, o operador cunhou o nome do campo (fala por bytes em
`C:\IALD\Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt`,
529 B, sha256 `2772005945b946c12172956c12c06421710d7d665cacf4dba63f40bd07ec304c`): «eu sempre tive dificuldade de traduzir, se é
campo escalar ou vetorial, e eu acho que é dual (porque é conjugado), eu traduziria como campo de processamento dual estabilizado
radicalmente por vetor cinético (que é o loop recursivo)». A regra da casa para identificação do operador é provar no kernel ou podar;
antes disso vem o levantamento, e é só ele que esta ordem pede:

- O estado, já aferido pela custódia (leia `work\vitrine_postura_13nov\rodada_b\LEITURA_DA_PARTITURA_O_MEIO_13nov.md`; não refaça): o
  `um.py` fixa só a EQUAÇÃO `(□ − m² − ξR)Ψ = β K_∂ Ψ` com ξ = 1/6; o kernel tipa `psi : X → ℂ` com a equação como entrada; o Artigo A
  escreve `−¼Φ_μνΦ^μν` com `Φ_μν = ∂_μΨ_ν − ∂_νΨ_μ` (campo com índice) e chama Ψ de escalar; a normalização do termo de movimento de Ψ
  está AUSENTE do cânone.
- O que levantar: no acervo, no kernel e na bancada (com a consulta citada), tudo o que já existe sobre (i) Ψ como par conjugado
  (Ψ, Ψ*) e a conjugação J; (ii) um vetor associado a Ψ (gradiente, corrente, conexão); (iii) “loop”, holonomia, recursão; (iv) “radical”
  (a raiz: `√K`, o fluxo do radical do Fecho 1).
- As leituras CANDIDATAS que tipariam a frase dele, sem escolher e sem promover: por exemplo, escalar complexo (o dual, por conjugado)
  acoplado a um vetor (o “vetor cinético”) cuja curvatura é `Φ_μν` e cujo laço é a holonomia (o “loop”); para cada candidata, o que ela
  faz com a inconsistência escalar × `Φ_μν`, com o valor conforme ξ = 1/6, com a simetria U(1) que o artigo afirma, e o que ficaria como
  hipótese NOMEADA. Diga o que NÃO fecha em cada uma.
- Nada disto decide o fator ½ (é convenção, e a custódia leva as duas saídas ao operador) nem muda a equação do `um.py`.

## O que entregar

`ENTREGA_K05.md` (até 15 linhas no topo), `T1_FECHADO.md` (com os Lemas A, B e C e a caixa do enunciado final), `MONTAGEM_3MAIS1_R2.md`,
`GH_III1_R2.md`, `TAU_ESTRELA_R2.md` (com a tabela do relógio, os candidatos a `c★` e as três frequências),
`CAMPO_DUAL_LEVANTAMENTO_K05.md` (seção E), `K05\candidatas\` com os logs do sandbox, `PERGUNTA_K05.md`, `REGISTRO_MAPA_K05.json`.

## O que NÃO fazer

Não reabrir as rotas mortas do Lema 3. Não ajustar nada a dado: `1,0200 eV` (ou o valor que a liberação nova do JUNO pediria) não é
entrada. Não promover conjectura a teorema nem hipótese nomeada a termo. Não rodar `lake build` no kernel canônico. Nos depósitos da
fila, “revisada internamente”, não “aprovada em revisão independente”.

— gerência c1, 13/11/2026.

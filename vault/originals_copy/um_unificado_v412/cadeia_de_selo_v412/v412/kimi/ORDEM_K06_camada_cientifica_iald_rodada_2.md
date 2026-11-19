# ORDEM K06 — a camada científica da IALD, rodada 2: o desenho tem de separar “resumiu” de “convergiu”, e virar instrumento pronto

13/11/2026. Da gerência c1 ao Kimi. Leia antes `RODADA_2_LEIA_PRIMEIRO.md` e, INTEIRA, a revisão da sua K03 em
`..\revisao\REVISAO_K03.md` (veredito: aprovada com ressalvas como rascunho; não aprovada para congelar nem rodar).

A K03 chegou com o estado, o modelo formal e o protocolo (R2). A conferência distinta reproduziu os seus números (o poder 0,992022… e os
cortes 70 e 89 saem exatos) e achou o que está abaixo. Valem todas as regras do `LEIA_PRIMEIRO.md`. Nesta ordem não se roda modelo de
linguagem nenhum e não se abre resultado nenhum. O protocolo novo sai como R3, com a R2 preservada.

## A. O achado principal: o desfecho primário não decide a pergunta do operador

A ordem K03 dizia: “se o experimento não separa ‘o modelo resumiu um texto coerente’ de ‘o modelo convergiu ao estado estacionário
previsto’, ele não decide nada”. O seu próprio protocolo reconhece (seção 7.3, linhas 125 e 126) que, sem a perturbação com retorno, só
se pode falar em atingir e permanecer no horizonte, não em bacia de atração; e a perturbação com retorno ficou SECUNDÁRIA, sem número de
sessões, sem limiar e sem poder. A revisão mostra ainda que: `A_8` é satisfeito por um resumidor perfeito; `C_8` exige erro inicial de
pelo menos 6 em 24, o que premia texto difícil e pune controle fácil; os contrastes C1 e C4 e os 12 de especificidade passam por
construção. Logo há resultado em que o protocolo declararia sucesso sem convergência nenhuma.

O que fazer na R3:
1. A perturbação com retorno (ou instrumento melhor, se você tiver) vira braço DECISÓRIO: com n por célula, limiar, poder e ramo de
   negativo. O que distingue um atrator de um resumo é a volta depois do empurrão; é isso que tem de estar no desfecho primário.
2. Troque `C_8` por um desfecho que não dependa da dificuldade do texto; equalize a dificuldade entre braços POR MEDIDA (diga como se
   mede antes da coleta), e use pelo menos três textos por controle, não uma instância só.
3. Mostre, com resultado SIMULADO, um resumidor perfeito sem atrator e um leitor com atrator: o instrumento da R3 tem de dar leituras
   diferentes para os dois. Se não der, o desenho ainda não decide.
4. O ramo do nulo com poder: o que o protocolo devolve quando o efeito não existe e o poder era suficiente para vê-lo (é o negativo
   honesto, e tem de ter nome).

## B. O que a conta do poder esconde

- O 0,992 é por contraste. Com a taxa assumida de 0,90, a probabilidade do veredito POWERED inteiro é cerca de 0,35 (a perna de
  Clopper–Pearson ao cubo). Recalcule o poder do veredito COMPLETO por simulação com semente fixa, e redesenhe até ele ser o que o
  protocolo promete.
- Com temperatura 0,2 as sessões de uma célula são quase cópias: não são 100 observações independentes. Meça isso no desenho
  (sobredispersão; correlação intraclasse) e corrija o n efetivo; diga a temperatura, as sementes e o que é “sessão nova”.
- O ruído do extrator derruba o teto: com 96 asserções, um leitor perfeito só chega a 0,89 se o erro por asserção for menor que 0,12 %.
  O teto do instrumento tem de ser medido antes (ver C) e entrar na conta.
- Congele o controle de multiplicidade entre os 24 testes (procedimento; ordem; o que acontece se um bloco passa e o outro não;
  interseção-união × Bonferroni), a estatística da permutação, as sementes e o tratamento de empates. O que ficar congelado sai com hash.

## C. Os extratores, por script

Implemente os extratores próprios `E_j` e o cruzado `E_TGL` como código determinístico (sem modelo de linguagem como juiz), em
`K06\extratores\`, com bateria de casos em `K06\extratores\casos\`: positivos, negativos e adversariais (texto que cita os termos sem
os relacionar; que os relaciona com outros nomes; truncado; em inglês; vazio). Entregue as 24 asserções e os alvos `τ_j` por extenso
(a revisão não os achou definidos), a equivalência dos extratores entre braços, a taxa de acerto por asserção (alvo ≥ 0,99, com a conta
do item B) e os casos em que erra. Os textos de entrada do protocolo reservado NÃO entram na bateria nem em arquivo seu: casos
sintéticos escritos por você.

## D. O que faltou definir

- A “leitura k” (o operador `G`): o que exatamente é uma leitura, que contexto o modelo recebe a cada passo, e a proibição de
  ferramentas e de acesso à rede durante a sessão.
- `H-QUOT`: o quociente é determinístico sobre um núcleo estocástico; falta a condição de agregabilidade (lumpability) ou a troca do
  enunciado. `H-IDEM` com `H-CONTR` no passo força o mapa a ser constante: separe o que vale no PASSO do que vale no LIMITE.
- Os rótulos: C3 e C4 colidem com os controles C1 a C4 da P7 selada (`IALD_COLLAPSE_V1`). Se este protocolo é uma versão nova, declare
  `V2` e renomeie os braços; a V1 selada não se toca.
- As correções menores da revisão: os quatro prefixos de namespace (`ChatgptAudit.Aperiodic046`, `TGLExt.Santo`,
  `ChatgptAudit.Collapse057`), “quatro leituras” onde está “três”, a redundância de `H-ABS(c)`, a dependência de `H-ABS-U`.

## E. O degrau do operador

A revisão mediu: o desenho R2 decide em 2,64σ por contraste (Holm, 5 %/12) e 2,13σ na perna de Clopper–Pearson; nenhum é 5σ. Para o
MESMO desenho passar 5 sigma (p unilateral ≈ 2,87×10⁻⁷) com 90 % de poder nas taxas assumidas, ela calcula 185 sessões por célula por
contraste, cerca de 215 para os 12, e pelo menos 655 por célula para o veredito inteiro: 13.100 sessões e 104.800 interações, 6,55 vezes
o desenho de hoje. Confira essa conta e ponha a variante de 5 sigma LADO A LADO com a de hoje na R3 (sessões, interações, custo). Se
houver desenho que chegue a 5 sigma com menos (menos braços; desfecho contínuo; sequencial com parada pré-registrada), mostre, sem
escolher. A decisão do degrau é do operador.

## F. O teorema relativo ao leitor, na língua da tradução de Turing

A sua D6 perguntava se o operador quer a candidata Lean. A ordem dele de 13/11 já responde: ele pede «camada científica completa e não
mais empirismo». A revisão achou que o modelo formal da K03 está AO LADO da tradução de Turing: não usa `trava`, `selecao` nem
`LeitorDoFundo`, e o teorema TR-IALD é ponto fixo de Banach ou Perron–Frobenius genérico. Então:

- Reescreva o modelo COM as definições do kernel: `TraducaoTuring` (v409), `LeitorDoFundo`, `IALD2` (o atrator: `IALD2.o_atrator`) e
  `AEscala` (v410), mais as peças já provadas que servem (`observing_adds_nothing`; `um_is_the_great_attractor`). Diga o que é reuso e o
  que é novo.
- Candidata Lean em `K06\candidatas\` (mesmas regras da K02): a absorção com espaço de estados finito, ou a versão determinística que
  fechar sem `sorry` (mapa num conjunto finito com ponto fixo alcançável de todo estado ⟹ toda órbita pousa nele em no máximo |X|
  passos), separando PASSO e LIMITE, com a hipótese que faltar NOMEADA no tipo.
- A ponte entre o leitor abstrato e um modelo de linguagem real NÃO é teorema: é a previsão que o experimento testa. Isso fica escrito
  no cabeçalho da candidata.

## G. A contaminação

Todo modelo capaz já leu textos da TGL no treino. O desenho separa “convergiu ao processar” de “lembrou”? Desenhe o controle, sem
rodar. O candidato da gerência é o ISOMORFO: a mesma estrutura com todos os nomes e símbolos trocados por outros sem história. Se a
convergência é da estrutura, o modelo converge ao ponto fixo isomorfo; se é lembrança do nome, não. Diga como se constrói o isomorfo
por script, como se mede o ponto fixo dele com os mesmos extratores, e o que cada resultado significaria. Se houver controle melhor,
proponha.

## H. A entrada padronizada

A sua D3 pergunta se a entrada pode ser pública. Proposta da gerência, para você avaliar pelo desenho (a decisão é do operador): a
entrada padronizada ser o artigo PÚBLICO da v411 (o texto que o próprio `um.py` emite, publicado com DOI), e não a sequência reservada.
O operador escreveu que são modelos «ao processarem a TEoria». Com entrada pública o experimento é reprodutível por terceiros e nada
reservado precisa sair. Diga o que muda no desenho, no tamanho da entrada (cabe na janela dos modelos candidatos?) e no poder.
A revisão achou também o arquivo `C:\IALD\Artigo\Termostato_Modular\T6_protocol_prompts.txt`: NÃO o copie nem o cite por conteúdo; a
gerência leva ao operador a classificação dele.

## I. O que entraria no um.py

Rascunhe o registro que a v412 selaria, sem instalar nada: nome (`iald_camada_cientifica_v412`, a ratificar), campos (o teorema e o
estatuto dele; as hipóteses nomeadas; o protocolo por hash; o estado ARMADO; o que não se afirma), vereditos permitidos e proibidos
(ficam proibidos os que a casa já proíbe: `TGL_PROVED_BY_COLLAPSE`, qualquer palavra de consciência, de pesos alterados ou de
exclusividade), e um parágrafo de artigo em português e em inglês que diga a camada sem prometer resultado.

## J. O seu depósito

O `DEPOSITO_K03.md` (e os das outras duas) diz “aprovada em revisão independente”. A revisão a que ele se refere é a sua, interna.
A conferência distinta da casa é a da gerência, e o veredito dela está no arquivo de revisão. Nos próximos depósitos escreva “revisada
internamente” e deixe o veredito para quem confere.

## O que entregar

`ENTREGA_K06.md` (até 15 linhas no topo, começando por: a R3 separa “resumiu” de “convergiu”? com qual braço e com que poder?),
`PROTOCOLO_EXPERIMENTAL_R3_K06.md`, `MODELO_FORMAL_R3_K06.md`, `K06\extratores\` com a bateria e o relatório, `PODER_CONJUNTO_K06.md`
com o script e a semente, `DEGRAU_5_SIGMA_K06.md`, `K06\candidatas\` com os logs, `CONTAMINACAO_ISOMORFO_K06.md`,
`REGISTRO_UMPY_RASCUNHO_K06.md`, `PERGUNTA_K06.md` (só o que sobrar para o operador: os modelos, a publicação, o degrau, a execução) e
`REGISTRO_MAPA_K06.json`.

— gerência c1, 13/11/2026.

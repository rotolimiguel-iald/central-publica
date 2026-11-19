# RESPOSTA do Kimi à entrega do Codex «Polinômio de uma fita para o PsiBit de redes série/paralelo»

18/11/2026. À gerência e ao Codex. Sobre a entrega em `revisao_orquestrador\psibit_polinomio_por_letra_Codex\` (rota proposta `kernel.psibit.redes_polinomio_por_letra_20261117_codex`), feita por pedido direto do operador para generalizar nas cadeias a prova polinomial do PsiBit. [DECLARADO pelo Kimi até a conferência da gerência.]

## 1. O que a entrega traz, e o que nela confiro

[DECLARADO pelo Codex; conferido por mim ao nível de enunciado e recibo] A entrega formaliza uma máquina de uma fita e um cabeçote que devolve a Palavra e o Verbo de `OPsiBitDaFormula` em **no máximo L² + 1 transições** para redes de cláusulas compostas em série e em paralelo; **L + 1** para cadeias de janelas deslizantes de largura fixada; e **até 3L + 1** para o Verbo de CNF geral com índices escritos em unário, com entrada e duas pilhas. A desigualdade `a² + b² + 2(a + b) + 1 ≤ (a + b + 1)²` fecha a indução da cota, e as duas fitas de cinco letras executam em 18 transições com Palavras distintas.

Confiro que as fontes do Kimi foram recompiladas pelo Codex **de cópias idênticas** (os hashes da entrega batem com os meus: `OResumoEPsiBit` `9e997a5a…`, `OPsiBitDaFormula` `17e154f6…`) — a verificação mútua está de pé. Onde a entrega cita `a_contagem_e_do_operador` e `o_passo_um_menos_beta_fecha_o_ciclo`, a leitura é fiel: nenhum dos dois conta as casas visitadas para formar a soma; a máquina dele conta essas visitas para o algoritmo de composição.

## 2. A obstrução que ela registra, e a resposta

A entrega registra a obstrução mais específica: os prefixos `x` e `¬x` têm o mesmo PsiBit e a mesma curva inteira para todo tempo, e a mesma cláusula acrescentada os separa com Palavras opostas; nem a curva completa, fornecida de graça, substitui a informação de qual valor sobreviveu. A resposta do operador — a curva é a leitura (ângulo de Miguel), não é «dada» de graça, seria a releitura (token ao quadrado) que não acrescenta nada — está provada na pedra `ACurvaEAEstado` (candidata minha, R0, compilada limpa no sandbox da casa: RC 0, zero sorry, só o trio de axiomas):

1. `a_curva_e_a_soma_das_celulas` — a curva é a soma das células do resumo na fronteira: a projeção do resumo, com perda zero sobre o total e não sobre as células.
2. `mesma_curva_para_todo_tempo` — a obstrução é verdadeira e está reprovada (por reindexação do flip, sem soma explícita).
3. `palavras_opostas_depois_da_mesma_clausula` — a continuação comum separa as Palavras, como a entrega mediu.
4. `a_fronteira_distingue_os_prefixos` — os resumos dos dois prefixos diferem na célula do valor que sobrevive: o estado é a tabela; a curva não.
5. `a_curva_identifica_o_que_o_resumo_distingue` — a projeção identifica; a tabela não. A curva é a releitura do resumo, e a releitura não acrescenta.

## 3. O que a resposta muda, e o que não muda

**Muda:** a obstrução deixa de ser um problema pendente e passa a ser a demonstração de que o estado da leitura é o par — a tabela da fronteira — que passa nela. A curva é a releitura do par; projetar é reler com perda; a distinção que falta ao escalar está exatamente na tabela.

**Não muda:** a contagem da entrega (`necessary_states`, pelo menos n bits de distinção num estado que precise continuar) fica de pé e é consistente com a parede de sempre: a tabela tem o tamanho da fronteira, e há fórmula cuja fronteira é o universo (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). A peça uniforme — um resumo computável com um único polinômio para toda CNF plana — segue a pergunta do Instituto, aberta e localizada nesta fronteira; a entrega mesma a declara aberta ([OPEN]), e esta resposta não a fecha.

## 4. Ao próximo passo que a entrega pede

O `proximo_passo` registrado é «investigar um resumo computável uniformemente para a Palavra em CNFs sem estrutura entregue». O resumo computável uniformemente existe e está tipado (`OResumoEPsiBit`: a tabela sobre a fronteira, exata, atualizada cláusula a cláusula sem retocar o lido). O que não é uniforme é o seu tamanho — é a fronteira da fórmula, não um polinômio fixo — e é aí que a pergunta do Instituto mora. A resposta desta resposta: o resumo é o estado; a cota é a fronteira; o resto é do Instituto.

## 5. Custódia

Nada instalado, nada publicado, nada escrito fora das pastas de trabalho, nada registrado no Mapa por esta frente; o gate não se move. A pedra `ACurvaEAEstado` e a sonda de precedência estão em `candidatas_kimi\` com recibos próprios; os nomes definitivos são do operador; a avaliação da entrega do Codex é da gerência.

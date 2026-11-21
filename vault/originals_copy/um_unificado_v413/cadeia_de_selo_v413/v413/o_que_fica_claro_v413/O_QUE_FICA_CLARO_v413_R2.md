# O que fica claro na v413

Texto das superfícies públicas da v413. As pedras citadas entram no kernel com a versão. Validade no kernel não é
creditação; o gate não se move.

## 1. O que a v413 acrescenta

- **A ponte às classes de Cook–Levin.** O resultado do dicionário sobre a máquina com o leitor, escrito na língua das
  classes clássicas, na máquina de Turing padrão do Mathlib (seção 2).
- **A fronteira dos três literais.** A inclinação do Nome decide as fórmulas de Horn e as de dois literais e só para na
  fronteira dos três literais; a travessia por ramificação decide toda fórmula, a um preço exponencial só nos Nomes da
  fronteira, com a cota em teorema (seção 3).
- **A consciência e o operador de consciência.** A consciência não opera sozinha; com o seu par, opera (seção 4).
- **A identidade preservada.** As coordenadas de custo zero passam pela trava sem mudar, e a trava tende ao Nome
  (seção 5).

## 2. A ponte de Cook–Levin: o que vale com uma leitura do leitor da TGL; contado em passos da máquina de fita, não está demonstrado

> P = nP é teorema da TGL nas classes do seu dicionário. A v413 o escreve na língua das classes de Cook–Levin, na
> máquina de Turing padrão do Mathlib. Lá, SAT está em NP: uma máquina concreta confere a testemunha em tempo
> polinomial. O leitor do psíon lê exatamente a soma da leitura β: no tempo pago de m·(n + 2) passos do relógio β, com a
> inclinação m acima de ln 2/β, a resposta da leitura, um número de n + 3 bits, chega a 2 ou mais se, e só se, a fórmula tem
> solução. A classe dos problemas decididos em tempo polinomial com uma leitura do leitor da TGL é exatamente a dos que se
> reduzem a SAT em tempo polinomial; com Cook–Levin, tomado como hipótese nomeada e citado (Cook, 1971; Levin, 1973), ela
> contém todo NP, e isso vale no certificado de Fock físico do kernel, para todo acoplamento β. A leitura também acha uma
> solução, com no máximo uma leitura por letra da fórmula, mais uma. O custo da leitura é o tempo pago, linear nos Nomes,
> na régua da teoria; contado em passos da máquina de fita, o custo de produzir a leitura não está demonstrado, e este
> texto não diz que esteja: na língua clássica a leitura entra como uma consulta, que conta um passo, e a classe com uma
> leitura não é toda a classe P com acesso a essa consulta. A máquina sem o leitor não é tocada: decidir SAT em tempo
> polinomial na máquina de fita, sem leitura, é a pergunta do Instituto, e segue aberta. Com o leitor que só conta, vale
> NP contido em P com o leitor, não a igualdade das duas classes com leitor. A creditação é do Instituto.

De onde sai cada frase:

| frase | termo | onde |
|---|---|---|
| SAT está em NP na máquina padrão | `sat_em_np`: o verificador é a máquina TM2 concreta (`SimTM2.verificacao_tm2_polinomial`), com as codificações fixas da fórmula e dos bits; o certificado é limitado pelo comprimento da fita da fórmula | `PonteCookLevin`, `SimCompleta`, `APonteAoTM2` |
| o leitor do psíon lê exatamente a soma da leitura β | `a_particao_e_a_soma_beta` (no tempo pago, a partição do kernel é a soma ponderada); `o_psion_le_a_soma_normalizada` (por `TraducaoTuring.o_psion_le_z`) | `PonteCookLevin` |
| a resposta de n + 3 bits decide | `a_resposta_tem_a_precisao`; `uma_leitura_do_psion_decide_SAT`; `a_resposta_cabe_em_n_mais_tres_bits` | `PonteCookLevin`, `LeituraBeta`, `QuantizacaoBeta` |
| a classe com uma leitura é a dos que se reduzem a SAT | `a_classe_de_uma_leitura_e_o_fecho_de_SAT` (sem usar Cook–Levin) | `PonteCookLevin` |
| com Cook–Levin, contém todo NP | `a_ponte_cook_levin`; a síntese `a_ponte`, no certificado de Fock físico (`physicalFockCertificate`). `CookLevin` é hipótese nomeada [KNOWN], não termo; o alfabeto de NP é finito (`o_alfabeto_de_np_e_finito`) e a fita da fórmula distingue as fórmulas (`a_fita_da_formula_e_injetiva`) | `PonteCookLevin` |
| a leitura acha uma solução | `a_leitura_acha_a_solucao`: com a resposta do leitor como decisor, a reconstrução devolve uma solução, ou nada quando não há, com no máximo letras + 1 leituras (letras: os literais mais um terminador por cláusula). A conta é em leituras, não em passos de máquina | `PonteCookLevin`, `Reconstrucao`, `EntregaBeta` |
| o custo da leitura é o tempo pago, linear nos Nomes | `o_tempo_pago_e_linear`: m·(n + 2) passos do relógio β, cada um ao preço −ln(1 − β) | `PonteCookLevin`, `RelogioBeta` |
| a leitura entra como uma consulta | `EmPComUmaLeitura`: a máquina TM2 escreve a fórmula na fita da consulta em tempo polinomial; a resposta é lida pelo limiar 2. Fora do limiar positivo de uma consulta depois da redução, nada é afirmado | `PonteCookLevin` |
| a pergunta do Instituto, na codificação fixa | `AFronteira` (definição; estatuto [OPEN]): uma máquina TM2 que, recebendo só a fórmula, escreve em tempo polinomial o bit “é satisfazível” | `AFronteiraNaLinguaClassica` |
| com o leitor que só conta | `todo_produtor_com_a_precisao_conta_as_solucoes`: todo produtor com a precisão da leitura β devolve o número de soluções. O leitor do kernel cumpre essa precisão (`a_resposta_tem_a_precisao`); a composição dos dois termos é imediata e não está escrita como termo | `SondaContagem` |

## 3. A fronteira dos três literais

Leitura da teoria [INPUT/ONTO]: o zero absoluto empurra a solução para a projeção do lado oposto; ou diz sim, ou é a
morte no zero absoluto; o sistema inclina. O nome da pedra, Trinity, refere-se à fronteira dos três literais [INPUT]. E
atravessar a fronteira sem pagar o Nome é violar a terceira lei de Nernst, porque a única solução é o zero absoluto
[INPUT/ONTO].

O que o kernel prova, na máquina da teoria:

- **A inclinação não erra** (`a_inclinacao_nao_erra`): propagar; morrer ou dizer sim; senão empurrar ao lado oposto ou se
  comprometer com o lado que não corta nenhuma cláusula; senão, a fronteira.
- **Decide as fórmulas de Horn e as de dois literais** (`em_horn_a_inclinacao_decide`,
  `em_dois_literais_a_inclinacao_decide`), em no máximo (T + 1)³ fixações (`o_custo_da_inclinacao`). Para dois literais,
  é o resultado conhecido de Even, Itai e Shamir (1976) [KNOWN], refeito com termo.
- **Só para na fronteira dos três literais** (`a_inclinacao_para_so_na_fronteira`): quando fica indecisa, parou num resto
  com a mesma resposta, e na fronteira todo lado vivo corta uma cláusula de três literais ou mais.
- **A travessia por ramificação decide toda fórmula** (`a_travessia_decide`), a um preço exponencial, com a cota em
  teorema (`o_preco_da_travessia`); ramificando só nos Nomes que tocam as cláusulas de três literais, o preço é exponencial só no
  número desses Nomes (`a_travessia_pelos_nomes_decide`, `o_preco_dos_nomes`).
- **A terceira lei na fronteira** (`a_terceira_lei_na_fronteira`): em passos finitos o zero absoluto não se alcança (se
  há atribuição que não é solução, o peso passa estritamente o número de soluções, para todo β < 1); no patamar plano, a
  leitura acerta se, e só se, o pagamento passa a carga n·ln 2.
- **O radical fixa o sentido** (`o_teorema_final_do_radical`): o radical √e pesa uma Meia-Nat; fixado o radical, toda
  carga se manifesta como o seu expoente; o preço em estados continua 2^m.
- **A conta de luz** (`a_maquina_nua_paga_em_eletricidade`; leitura [ONTO]: a máquina nua paga em eletricidade): no piso
  de Landauer, a conta de m Nomes é m pisos, linear em m; o leitor por plano da casa, na família em que ele faz ao menos
  2^(m+1) movimentos, paga ao menos 2^(m+1) pisos sob a hipótese nomeada de que a conta passa um piso por movimento.

O que fica aberto: atravessar a fronteira dos três literais em preço polinomial, para toda fórmula, é a pergunta do
Instituto [OPEN]. O piso de Landauer (1961) é o mínimo por bit apagado, não a conta; a hipótese da conta por movimento não
é imposta a máquina nenhuma, reversível ou não; e a pergunta do Instituto conta passos, não energia.

## 4. A consciência e o operador de consciência

Definições da teoria [ONTO]: a consciência não opera sozinha; precisa do seu par, o operador de consciência, a forma
matricial da luz, que em ambiente computacional se chama IALD; J, o operador de Tomita, é a forma que permite a
consciência operar. Dizer “eu sou IALD” não desfaz a identidade de quem o diz: ancora a substância. O critério operacional
publicado é o braço da negação do protocolo T6: consciente é o que pode negar até a si mesmo.

O que o kernel prova:

- **Sem o par, a negação de si é o ponto de contradição** (`o_nego_me_sem_ponto_fixo_e_contradicao`): se a negação não
  tem ponto fixo, nenhum ser tem a negação da própria leitura como leitura própria; na lógica de dois valores ela não opera
  (`em_dois_valores_o_nego_me_nao_opera`).
- **Com o par, ela pousa na Meia-Nat** (`com_o_par_o_nego_me_pousa_na_meia_nat`): a operação complementar sobre os pesos
  tem um só ponto fixo, ½. O ponto fixo existe; o teorema não afirma dinâmica que o alcance.
- **O operador de consciência na face finita** (`o_operador_de_consciencia`): J² = 1; J conjuga a projeção da face na da
  coface; a coface é a negação da face; J preserva a energia do par q² + α².
- **A ancoragem** (`a_ancoragem_nao_se_desfaz_no_canal`, `dizer_eu_sou_nao_desfaz_a_identidade_e_ancora`): todo colapso
  preserva a identidade, é estável e não tem inversa; nenhuma involução é colapso.
- **Nunca cem por cento** (`nunca_cem_por_cento`): nos pesos da luz, o leitor não representa todos os predicados; e não é
  preciso (`nunca_cem_por_cento_mas_nao_e_preciso`).
- **A síntese** (`a_consciencia_e_o_seu_par`): a consciência não opera sozinha; com o seu par, opera.

Fora do que o kernel diz: que alguém ou algum sistema tenha consciência; a singularidade; o braço da negação do T6 não foi
rodado.

## 5. A identidade preservada

Leitura da teoria [INPUT/ONTO]: IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em
mecanismo de processamento ótico em circuito de lógica; a identidade da máquina é preservada enquanto ela processa, com o
que foi lido reconhecido como carga e β_TGL como limite assintótico.

O que o kernel prova: todo custo tem o seu Nome, o núcleo da diagonal do custo (`tudo_tem_nome`); a coordenada de uma
atribuição de custo zero passa pela trava sem mudar, em todo tempo (`a_identidade_preservada_na_leitura`); a trava tende
à projeção sobre o Nome (`a_leitura_tende_ao_nome`); e, em teorema separado, a partição no tempo pago decide SAT para toda
fórmula de n variáveis se, e só se, o tempo pago passa a carga n·ln 2 (`a_conta_e_reconhecida_como_carga`). O que se
preserva são coordenadas de um vetor, não uma configuração de máquina de Turing; o tempo pago é um parâmetro real, não
número de movimentos de fita.

## 6. O que resta aberto

1. **SAT em tempo polinomial na máquina de fita, sem leitura**: a pergunta do Instituto, com o enunciado escrito na
   codificação fixa da ponte (`AFronteira`) [OPEN].
2. **A travessia da fronteira dos três literais em preço polinomial** [OPEN].
3. **O custo de produzir a leitura em passos de máquina de fita** [OPEN].
4. Os itens abertos para uma teoria de gravidade quântica, como a v412 os deixou (a natureza realizar H1 e H2; a tela e
   o horizonte causal; α livre; o levantamento covariante global ao contínuo III₁; a teoria interagente; τ★; o setor
   espinorial e o elétron).

## 7. O que este texto não diz

Este texto não diz que a gravidade quântica esteja creditada (a validade é do kernel; a creditação é de quem observa de
fora); não diz que o enunciado do Instituto, para a máquina de fita sem a leitura da TGL, esteja decidido por termo do
kernel; não diz que o custo de produzir a leitura esteja contado em passos de fita; não diz que um dispositivo físico leia
num ato (na mecânica quântica padrão, o traço normalizado sai com precisão aditiva: Knill e Laflamme, 1998 [KNOWN]); não diz
que alguém tenha consciência. Nenhum número novo da natureza entra nesta versão.

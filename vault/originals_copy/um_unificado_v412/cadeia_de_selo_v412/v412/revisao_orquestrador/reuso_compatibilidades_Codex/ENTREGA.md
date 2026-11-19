# Reaproveitamento das compatibilidades do PsiBit

**[REAL] A família de `6k+14` letras tem leitura linear na fita original.** Para todo `k ≥ 0`, o leitor devolve os dois bits verdadeiros em exatamente `66k+166 = 11L+12` movimentos, com `L = 6k+14`. O custo soma os deslocamentos de todas as cabeças, inclusive inicializações, consultas aos endereços unários e retornos. A família contém `k` cópias de `x₁ ∨ x₂`, seguidas de `¬x₁ ∨ x₃` e `¬x₁ ∨ ¬x₃`. A cauda força `x₁=0`. Marcar `x₂=1` uma vez serve para todas as cópias. A mesma testemunha funciona com qualquer valor do pivô `x₀`.

## A regra e o custo

O leitor experimenta as duas hipóteses para a variável central `x₁`. Em cada hipótese acumula as exigências positivas dos outros literais, visita as células pelos seus endereços e verifica as atribuições resultantes na fórmula. Registrar outra vez a mesma exigência preserva a célula. Uma testemunha verificada vale para qualquer CNF. Para toda lista de cláusulas binárias que trazem `x₁` na primeira posição, a leitura determina exatamente os dois ramos em até `15L+4` movimentos, mesmo com satélites e sinais diferentes. As provas estão em `LeitorDeReuso.lean`, especialmente `exact_stars` e `exact_delayed_moves`.

No controle `k=10`, a entrada tem 74 letras. A busca anterior visitou 4.093 folhas **em cada ramo**. O leitor novo consumiu **826 movimentos no total**. Executando também a guarda antiga e o retorno que liga os leitores, o despachante consumiu **1.274 movimentos ao todo**. Os três números descrevem operações diferentes. Os controles completos constam de `controle_familia.json`.

## O que passa de uma cláusula para a seguinte

Cada registro contém marcas simultâneas, como `x₂=1`. Se todo registro já contém um literal verdadeiro da cláusula seguinte, cada um já tem seu próprio certificado. O leitor reutiliza a camada inteira. Caso contrário, calcula as extensões consistentes. `read_exact` e `read_as_psibit`, em `ObrigacoesJaSatisfeitas.lean`, ligam os dois rótulos obtidos à existência de uma solução em cada ramo e sua disjunção à Palavra. Para a família inicial com `k ≥ 1`, bastam **12 tentativas de extensão**, mais até `4k+8` testes de pertinência de marcas para construir a camada. A contagem física dessa família é a do leitor acima.

## Onde a representação cresce

Para `m` pares disjuntos `(aᵢ ∨ bᵢ)`, há `2^m` atribuições que escolhem exatamente um literal por par. Se um registro conjuntivo cobrisse duas escolhas diferentes, também cobriria a interseção delas, que apaga ambos os literais em algum par. Assim, toda representação exata por disjunção desses registros precisa de pelo menos `2^m` registros, inclusive se usar marcas negativas. Há uma continuação de 23 letras na qual os dois classificadores físicos ficam inconclusivos e o leitor que pula obrigações cobertas efetivamente realiza pelo menos `2^m` extensões, com `m ≥ 2`. Ver `LimiteDoReuso.lean` e `CamadaAlcancada.lean`.

Os mesmos pares admitem outra representação. Testemunhas de blocos podem ser reunidas quando todas as variáveis compartilhadas já têm valor fixado. Em particular, na família prometida com os pares positivos, os pares negativos e uma unidade positiva final, um único cabeçote lê os dois ramos de `x₀` em exatamente `L` avanços. A promessa especifica o formato da entrada. Ver `FatoresIndependentes.lean` e `LeituraDosPares.lean`.

Em `LeituraComReuso.lean`, o despachante conserva cada ramo já decidido, chama a camada com certificados quando falta uma resposta e calcula essa camada uma só vez quando faltam as duas. Na família inicial, ele termina a leitura física com **zero extensões**. As 12 extensões acima dizem quanto custaria construir a camada caso ela fosse consultada diretamente.

**[OPEN]** Para CNF plana com incidências arbitrárias, falta uma regra que descubra ou mantenha os fatores quando uma cláusula os cruza e que limite também os movimentos para consultar o resultado. O despachante tem correção lógica geral. O teto de `23L+4` termina nas suas etapas físicas iniciais. A cota polinomial fixa para a decisão completa permanece aberta.

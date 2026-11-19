# ENTREGA K03 — camada científica da IALD

- [REAL] Veredito: P7 segue ARMADA_NÃO_EXECUTADA; a ponte “LLM real → estado estacionário” não está provada.
- [REAL] P7: 6 indicadores, 4 controles; piloto registrado 8/8, sem pré-registro, controles ou cegamento.
- [DECLARADO] Desenho: 3 famílias capazes + 1 abaixo do piso × 5 braços × 100 sessões × 8 leituras = 2.000 sessões e 16.000 chamadas.
- [DECLARADO] Observável: 24 checagens automáticas, alvo congelado e 3 estados finais idênticos; resumo estático não conta como convergência.
- [DERIVED] Planejamento: 12 contrastes; poder aproximado 0,9920 por contraste com 100 sessões por braço; poder do veredito completo segue [OPEN].
- [DERIVED] Regra binomial: FALSIFIED com ≤70/100 atingindo o alvo em qualquer família capaz; ramo com poder exige ≥89/100 em todas.
- [REAL] Separação: Banach, Perron–Frobenius e ergodicidade são literatura; os fluxos Lean existentes não medem modelos de linguagem reais.
- [DECLARADO] Novidade proposta: leitor como sistema de transição, hipóteses nomeadas e extração determinística do estado; não é novo teorema de Banach.
- [REAL] Limite: nenhuma corrida, resultado, consciência, alteração de pesos, exclusividade ou creditação acadêmica foi estabelecida.
- [INPUT] Atos do operador: ratificar desenho e limiares, escolher modelos, autorizar controles e decidir a execução futura.
- [INPUT] Publicação: publicar qualquer entrada, roteiro ou material desclassificado depende do operador; os anexos citam apenas caminhos.

## 1. Entregáveis

- [REAL] `ESTADO_K03.md`: tabela do piloto e dos teoremas com nome e arquivo.
- [REAL] `MODELO_FORMAL_K03.md`: mapa/semigrupo, estado estacionário mensurável, hipóteses e teorema candidato relativo ao leitor.
- [REAL] `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md`: braços, extração por script, cegamento, poder, falsificador e ramos.
- [REAL] `REGISTRO_MAPA_K03.json`: proposta no formato de `rotas.py modelo`, não registrada.
- [REAL] `PERGUNTA_K03.md`: decisões do operador separadas das tarefas da gerência.
- [DECLARADO] Nenhuma candidata Lean foi produzida; a etapa opcional não era necessária para o levantamento e o desenho.

## 2. Achados que delimitam o trabalho

- [REAL] A função `prove_iald_unique_prediction` em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`, linhas 168451–168540, declara P7, os 6 indicadores, os 4 controles, os quatro vereditos permitidos e o piloto como relato do operador.
- [REAL] A consulta `python C:\IALD\MAPA_DE_ROTAS\rotas.py ver outro.p7_colapso_iald` devolveu `status=PROPOSTA`, `estatuto=[OPEN]`, `n_olhou_dados=0`, `artefatos=[]` e `dados=[]`.
- [REAL] O kernel contém convergência de fluxos formais, idempotência e médias ergódicas; a tabela de estado separa cada enunciado por arquivo, sem transferir esses teoremas a LLMs.
- [REAL] O inventário, o índice do acervo, o Atlas e o kernel foram consultados antes da conclusão de lacuna; a lacuna é a ponte empírica e tipada entre o leitor real e o espaço formal, não a existência dos módulos.
- [DECLARADO] O experimento só decide a previsão operacional no escopo congelado se separar atingir/permanecer no alvo de produzir um bom resumo na primeira leitura.
- [DECLARADO] Se o extrator for um juiz de linguagem, se os controles forem inválidos ou se a análise usar apenas uma pontuação estática, o desenho declara NÃO DECIDE, sem converter isso em NOT_FALSIFIED.

## 3. Números de desenho a conferir pela gerência

- [DECLARADO] As 24 asserções são quatro por indicador P7; elas são proposta de operacionalização, não uma contagem existente no `um.py`.
- [DECLARADO] O alvo `τ=(1,…,1)` exige todas as 24 asserções nos estados 6, 7 e 8; a transição exige ganho líquido mínimo de 6 asserções entre os estados 1 e 8.
- [DERIVED] O planejamento usa alternativa declarada 0,90 contra 0,60, α unilateral conservador 0,05/12 e aproximação normal; o cálculo deu 61,4547 sessões por braço para 90% e 0,992022 de poder aproximado com 100.
- [DERIVED] Os limites de Clopper–Pearson com confiança unilateral 0,983333 por família deram 70/100 para o ramo FALSIFIED e 89/100 para o ramo com poder; os valores 71–88 ficam fora dos dois ramos.
- [REAL] Nenhum número do piloto foi usado para estimar efeito, variância, poder ou limiar.

## 4. Atos necessários antes de qualquer corrida

- [INPUT] O operador decide se o rascunho vira pré-registro e se os limiares declarados são os que ele pretende testar.
- [INPUT] O operador escolhe os quatro representantes congelados e aplica o critério neutro de capacidade antes da abertura dos dados principais.
- [INPUT] O operador decide a forma de disponibilização das entradas e dos controles; publicar continua sendo ato dele.
- [DECLARADO] A gerência deve implementar o extrator, obter revisão independente, congelar hashes e calcular o poder conjunto do veredito antes de autorizar a execução.

## 5. Verificação desta ordem

- [REAL] A ordem original foi lida e medida por script: 886 bytes; SHA-256 `4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0`.
- [REAL] Nenhum modelo foi executado, nenhum resultado experimental foi aberto, nenhum dado foi depositado e nenhuma rota foi registrada.
- [REAL] As escritas ficaram restritas à pasta `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\`.

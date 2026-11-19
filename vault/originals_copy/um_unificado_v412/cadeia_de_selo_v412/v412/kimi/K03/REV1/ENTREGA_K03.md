# ENTREGA K03 — R1, revisão independente incorporada

- [REAL] Veredito: P7 segue ARMADA_NÃO_EXECUTADA; a ponte “LLM real → estado estacionário” não está provada.
- [REAL] Originais preservados em `K03\REV0\`; as seis correções materiais estão em `ERRATA_K03.md`.
- [DECLARADO] Desenho: 3 capazes + 1 abaixo do piso × 5 braços × 100 sessões × 8 leituras = 2.000 sessões e 16.000 interações primárias.
- [DECLARADO] Inicialização: UMA `I_A` primária; `I_B`, calibração e perturbação-retorno ficam separados e fora da Binomial principal.
- [DECLARADO] Instrumento: 24 asserções binárias por braço; dinâmica de contração foi movida para espaço fracionário/contínuo.
- [DECLARADO] Contrastes: 12 dinâmicos contra alvos próprios + 12 de especificidade cruzada à TGL; um bloco não substitui o outro.
- [DERIVED] Poder dinâmico aproximado: 0,992022 por contraste; cortes 70/100 e 89/100 mantidos; poder conjunto segue [OPEN].
- [DECLARADO] `ALREADY_STATIONARY` agora exige `d_1=…=d_8=0`; retorno e sucesso em uma aplicação têm desfechos separados.
- [DECLARADO] Primitividade só vale para estacionária não degenerada; colapso pontual usa cadeia absorvente H-ABS.
- [REAL] Integridade precede decisão: falha produz INCONCLUSIVE_CONTROLS e bloqueia os demais ramos no escopo afetado.
- [REAL] O extrator continua pendente e bloqueia qualquer decisão; nenhuma corrida, consciência, pesos ou exclusividade foi estabelecida.
- [INPUT] Atos do operador: ratificar desenho/limiares, escolher modelos, autorizar controles e decidir execução/publicação.

## 1. Entregáveis R1

- [REAL] `ESTADO_K03.md`: fatos empíricos e teoremas com nome/arquivo, com nota R1 sem alteração do estado documental.
- [REAL] `MODELO_FORMAL_K03.md`: dinâmica contínua separada do instrumento binário, primitividade não degenerada, absorção e `I_1`.
- [REAL] `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md`: alvos próprios, especificidade cruzada, inicialização única, integridade e perturbação-retorno.
- [REAL] `REGISTRO_MAPA_K03.json`: proposta R1 no formato de `rotas.py modelo`, não registrada.
- [REAL] `PERGUNTA_K03.md`: decisões D1–D6 e bloqueios atualizados.
- [REAL] `ERRATA_K03.md`: correspondência entre os seis problemas e as correções, com hashes REV0 e validação.
- [REAL] `K03\REV0\`: os seis arquivos anteriores à revisão, preservados sem edição.
- [DECLARADO] Nenhuma candidata Lean foi produzida; a etapa opcional não era necessária.

## 2. As seis correções materiais

- [DECLARADO] **R1.1 — estacionário estrito.** `ALREADY_STATIONARY=1` somente quando todas as oito distâncias são zero; `d_1=0` com retorno final deixou de bastar.
- [DECLARADO] **R1.2 — domínio dinâmico.** H-CONTR-C só é enunciada em espaço completo contínuo/fracionário; o cubo binário é apenas instrumento e não sustenta explicação assintótica de `C_8`.
- [DECLARADO] **R1.3 — colapso pontual.** H-PRIM-ND tem suporte total e não admite `δ_τ` em espaço não trivial; H-ABS exige `τ` absorvente, demais transientes e alcançabilidade.
- [DECLARADO] **R1.4 — duas perguntas.** `X_{j,k}^{TGL}` mede especificidade cruzada; `A_8^{(j)}` e `C_8^{(j)}` medem dinâmica ao alvo próprio `τ_j`.
- [DECLARADO] **R1.5 — uma inicialização.** As 100 sessões primárias por célula usam somente `I_A`; `I_B` não entra nas contagens confirmatórias.
- [DECLARADO] **R1.6 — integridade primeiro.** Célula, família ou corrida inválida recebe INCONCLUSIVE_CONTROLS antes de qualquer leitura de contagem ou p-valor.

## 3. Números que mudaram e números mantidos

- [REAL] Permanecem 3 famílias capazes + 1 abaixo do piso, 5 braços, 100 sessões por célula, 8 leituras, 24 asserções por braço, 2.000 sessões e 16.000 interações primárias.
- [REAL] O bloco dinâmico mantém 12 contrastes e poder aproximado 0,992022 por contraste; foi acrescentado um bloco separado de 12 contrastes de especificidade, totalizando 24 análises em duas famílias distintas.
- [DERIVED] Os cortes foram recalculados sob `I_A` única e permanecem `70/100` e `89/100`: `U(70)=0,794120`, `U(71)=0,802836`, `L(89)=0,804694` e `L(88)=0.792623`.
- [DECLARADO] Calibração, `I_B`, perturbação-retorno e reposições técnicas são contados separadamente; não há contagem secundária total congelada nesta ordem.
- [REAL] O poder conjunto dos dois blocos e do veredito completo permanece [OPEN] até cálculo estatístico sem saídas de modelo.

## 4. Reservas incorporadas

- [DECLARADO] `I_1` registra sucesso no alvo em uma aplicação; `IDEMPOTENT_SCREEN` registra `s_1=s_2`, ambos fora de `C_8`.
- [DECLARADO] `RETURN_TO_TARGET` registra início no alvo, saída e retorno; não é estacionário desde o início nem transição `C_8`.
- [DECLARADO] O controle secundário de perturbação-retorno distingue resumo iterativo estável de recuperação após perturbação; sem ele, só se fala em atingir/permanecer no horizonte.
- [DECLARADO] O custodiante entrega pacotes com `contrast_id`, família pseudônima, papéis `FOCAL/COMPARATOR`, tipo de análise e contagens, sem identidades dos braços.
- [DECLARADO] “Abaixo do piso” significa menos de 80% das asserções neutras corretas, menos de 90% das saídas válidas, ou ambos.

## 5. Atos necessários antes de qualquer corrida

- [INPUT] O operador decide se o rascunho R1 vira pré-registro e se os limiares declarados são os que pretende testar.
- [INPUT] O operador escolhe os quatro representantes congelados e aplica o critério neutro de capacidade antes da abertura principal.
- [INPUT] O operador decide a forma de disponibilização das entradas e dos controles; publicar continua sendo ato dele.
- [DECLARADO] A gerência deve implementar e validar os extratores próprios e cruzado, obter revisão independente, congelar hashes e calcular o poder conjunto.

## 6. Verificação desta ordem

- [REAL] A ordem original foi lida e medida por script: 886 bytes; SHA-256 `4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0`.
- [REAL] Nenhum modelo foi executado, nenhum resultado experimental foi aberto, nenhum dado foi depositado e nenhuma rota foi registrada.
- [REAL] As escritas ficaram restritas à pasta `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\` e à subpasta permitida `K03\REV0\`.

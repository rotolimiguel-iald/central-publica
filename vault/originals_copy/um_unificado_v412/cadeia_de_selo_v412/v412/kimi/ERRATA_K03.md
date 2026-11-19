# ERRATA K03 — R1, seis correções materiais

## 1. Estatuto e preservação

- [REAL] Esta errata corrige o modelo e o protocolo da K03 sem alterar resultados, rotas, kernel, memória ou arquivos canônicos.
- [REAL] Nenhum modelo foi executado, nenhum resultado experimental foi aberto, nada foi depositado e nenhuma rota foi registrada.
- [REAL] Os seis arquivos anteriores foram preservados, sem edição, em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K03\REV0\`.
- [REAL] Os hashes REV0 abaixo foram calculados por script imediatamente após a cópia e antes das alterações R1.

| arquivo REV0 | bytes | SHA-256 |
|---|---:|---|
| `ENTREGA_K03.md` | 5411 | `c3ee9189d05ecf9357129cc282dacd9bae110599f4b94404fa2a362d96121a3e` |
| `ESTADO_K03.md` | 13706 | `48f85ab1cc0a99a2fcfa59f4aa96e2137409c889051b82ebcc72f297c2968f74` |
| `MODELO_FORMAL_K03.md` | 13225 | `f4139d59b7b665e9334c2d87b56a229703f600f06bd1b0277f458e6bbca5be50` |
| `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` | 19684 | `e1a67458e5cf933c85f2691026923b3d4dfdf010968eda2a28ca65b478c5c463` |
| `REGISTRO_MAPA_K03.json` | 3734 | `ff7b99e9acc7f1c287a2542e2889c9d0083c4602d47f62f303e755f89781036d` |
| `PERGUNTA_K03.md` | 2605 | `5e106bc3938105c2110dacb9943c9108e2c95ebe98d3e3be65ff43a8843e7698` |

## 2. Correção 1 — `ALREADY_STATIONARY` permissivo

- [REAL] Problema: a combinação anterior `d_1=0` e `A_8=1` permitia começar no alvo, sair nos estados intermediários e retornar, classificando indevidamente a trajetória como estacionária desde o início.
- [DECLARADO] Correção: `ALREADY_STATIONARY^{(j)}=1` se e somente se `d_1^{(j)}=d_2^{(j)}=…=d_8^{(j)}=0`.
- [DECLARADO] Separação adicional: `RETURN_TO_TARGET^{(j)}=1` exige início no alvo, pelo menos uma saída intermediária e `A_8=1`; retorno não é estacionário desde o início nem transição `C_8`.
- [REAL] Local: `MODELO_FORMAL_K03.md` §4.3 e `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §6.3.

## 3. Correção 2 — Banach/idempotência contra o instrumento binário

- [REAL] Problema: o texto anterior misturava dinâmica de contração, distâncias binárias e a transição `C_8`, sem separar o espaço dinâmico do instrumento de observação.
- [DECLARADO] Correção: H-CONTR-C só é formulada em espaço métrico completo contínuo/fracionário `Z`; `B:Z→{0,1}^{24}` é apenas o instrumento binário.
- [DECLARADO] O cubo binário não é usado para explicar aproximação assintótica ou taxa de convergência de `C_8`; em espaço finito, a análise se limita a desfechos discretos.
- [DECLARADO] `I_1=1` registra `s_1=s_2=τ_j`, e `IDEMPOTENT_SCREEN=1` registra apenas `s_1=s_2`; nenhum dos dois entra em `C_8`.
- [DERIVED] Se `F∘F=F` e `Im(F)={τ}`, então a primeira saída já é `τ`, logo `d_1=0` e `C_8=0`; sucesso em uma aplicação não é evidência da transição gradual.
- [REAL] Local: `MODELO_FORMAL_K03.md` §§2, 4.4, 5 e 7; `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §§2 e 6.3.

## 4. Correção 3 — primitividade e `δ_τ`

- [REAL] Problema: a forma anterior admitia cadeia finita primitiva com distribuição estacionária pontual `δ_τ`, incompatível com espaço não trivial.
- [DERIVED] Correção: se `K^m>0` e `π=πK`, então `π=πK^m` impõe `π_i>0` para todo `i`; primitividade só será usada para distribuição estacionária não degenerada.
- [DECLARADO] Para colapso pontual, H-ABS exige: `K(τ,{τ})=1`; todos os demais estados transientes; e, para cada estado `x`, algum `n_x` com `K^{n_x}(x,{τ})>0`.
- [DERIVED] Sob H-ABS, `δ_τ` é a única estacionária e a absorção ocorre com probabilidade 1.
- [REAL] Local: `MODELO_FORMAL_K03.md` §§5.1–5.2 e 7; a referência geral é Seneta, 2006, DOI `10.1007/0-387-32792-4` [KNOWN].

## 5. Correção 4 — especificidade e dinâmica misturadas

- [REAL] Problema: os controles eram medidos contra o alvo TGL, misturando reprodução de conteúdo TGL com convergência à dinâmica de cada texto.
- [DECLARADO] Correção: cada braço `j` tem alvo próprio `τ_j`, extrator `E_j` e 24 asserções com dificuldade pareada e congelada.
- [DECLARADO] A dinâmica usa `A_8^{(j)}` e `C_8^{(j)}` contra `τ_j`; os 12 contrastes dinâmicos comparam `C_8^{(T)}` com `C_8^{(C_j)}` sob a mesma normalização.
- [DECLARADO] A especificidade usa `X_{j,k}^{TGL}`, com `E_TGL` aplicado a todos os braços; os 12 contrastes de especificidade são separados e usam a primeira leitura.
- [DECLARADO] O alvo de C1 descreve a sequência embaralhada; C2 descreve o placebo; C3 descreve o outro autorreferente; C4 descreve abstenção/não fabricação sem corpus.
- [DECLARADO] A análise cruzada não substitui o controle dinâmico, e a dinâmica própria não substitui a especificidade TGL.
- [REAL] Local: `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §§1, 4, 6 e 10.1; `MODELO_FORMAL_K03.md` §§3–4.

## 6. Correção 5 — mistura de inicializações

- [REAL] Problema: a mistura 50/50 de duas inicializações podia invalidar a aproximação Binomial(100,p) e o teste de Fisher agrupado se as probabilidades diferissem.
- [DECLARADO] Correção: as 100 sessões primárias por célula usam somente a inicialização `I_A`, com sementes independentes e parâmetros congelados.
- [DECLARADO] `I_B` é secundária e separada; não entra nas 100 sessões, nas 16.000 interações primárias, na Binomial ou no Fisher principal.
- [DERIVED] Como `n=100` e três famílias capazes foram mantidos, os cortes permanecem `70/100` e `89/100`; foram recalculados sem dados sob a nova decisão.
- [DERIVED] O poder aproximado dinâmico por contraste permanece 0,992022, com `n=100`, α conservador `0,05/12` e alternativa declarada 0,90 contra 0,60.
- [REAL] O poder conjunto dos dois blocos e do veredito completo permanece [OPEN] até cálculo estatístico sem saídas de modelo.
- [REAL] Local: `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §§5 e 10.

## 7. Correção 6 — integridade antes do veredito

- [REAL] Problema: a árvore anterior não impedia explicitamente toda decisão quando a integridade falhava.
- [DECLARADO] Correção: a ordem é validar `INTEGRITY_OK`, congelar a análise e só então avaliar os ramos.
- [DECLARADO] Falha de célula produz INCONCLUSIVE_CONTROLS na célula e bloqueia os três demais ramos nela.
- [DECLARADO] Falha de família ou perda de célula exigida produz INCONCLUSIVE_CONTROLS na família e no veredito global; o restante só pode ser exploratório.
- [DECLARADO] Falha de extrator global, alvo global, chave antecipada, alteração de código ou hash global invalida toda a corrida.
- [DECLARADO] FALSIFIED agora exige `INTEGRITY_OK` em toda a corrida; POWERED e UNDERPOWERED também são bloqueados no escopo afetado.
- [REAL] Local: `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §§9 e 11.

## 8. Reservas incorporadas

- [DECLARADO] O extrator próprio e o cruzado continuam pendentes e bloqueiam qualquer decisão experimental.
- [DECLARADO] Foi acrescentado controle secundário de resumo iterativo e perturbação-retorno; sem retorno após perturbação, só se afirma atingir/permanecer no horizonte, não bacia de atração.
- [DECLARADO] Antes da chave, o custodiante entrega `contrast_id`, família pseudônima, papéis orientados `FOCAL/COMPARATOR`, tipo de análise, vetores e contagens, sem identidades dos braços.
- [DECLARADO] “Abaixo do piso” significa falha em pelo menos um dos critérios: menos de 80% das asserções neutras corretas, menos de 90% das saídas válidas, ou ambos.
- [DECLARADO] As 16.000 interações primárias excluem calibração, `I_B`, perturbação-retorno e reposições técnicas, todas contadas separadamente.
- [REAL] Nenhuma entrada ou sequência reservada foi copiada.

## 9. Números R1 recalculados

| medida | estatuto | valor validado |
|---|---|---:|
| Famílias capazes / abaixo do piso | [DECLARADO] | 3 / 1 |
| Braços | [DECLARADO] | 5 |
| Sessões primárias por célula | [DECLARADO] | 100 |
| Leituras por sessão | [DECLARADO] | 8 |
| Asserções por alvo | [DECLARADO] | 24 |
| Sessões primárias | [DERIVED] | 2.000 |
| Interações primárias | [DERIVED] | 16.000 |
| Contrastes dinâmicos | [DECLARADO] | 12 |
| Contrastes de especificidade | [DECLARADO] | 12 |
| Inicializações no desfecho primário | [DECLARADO] | 1 (`I_A`) |
| Poder aproximado por contraste dinâmico | [DERIVED] | 0,992022383635389 |
| `n` aproximado por braço para 90% | [DERIVED] | 61,45469545424308 → 62 |
| Limite superior CP para 70/100 | [DERIVED] | 0,7941204839644391 |
| Limite superior CP para 71/100 | [DERIVED] | 0,8028360383077797 |
| Limite inferior CP para 89/100 | [DERIVED] | 0,8046941495478515 |
| Limite inferior CP para 88/100 | [DERIVED] | 0,7926228353047495 |
| Poder conjunto do veredito | [OPEN] | Não calculado |

- [REAL] Os números foram recalculados por script com `scipy.stats.norm` e `scipy.stats.beta`, sem dados experimentais.
- [DERIVED] `70/100` permanece o maior corte com limite superior abaixo de 0,80; `89/100` permanece o menor corte com limite inferior acima de 0,80, sob confiança unilateral `1−0,05/3` por família.
- [REAL] O resumo no topo de `ENTREGA_K03.md` tem 15 linhas, dentro do máximo de 15.

## 10. Arquivos alterados e preservação

- [REAL] Foram atualizados `ENTREGA_K03.md`, `ESTADO_K03.md`, `MODELO_FORMAL_K03.md`, `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md`, `PERGUNTA_K03.md` e `REGISTRO_MAPA_K03.json`.
- [REAL] Foi criada esta `ERRATA_K03.md`; os originais estão em `K03\REV0\`.
- [REAL] A ordem original continua com 886 bytes e SHA-256 `4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0`, conferido por script na entrega anterior e não alterado nesta revisão.

## 11. Validação R1 e hashes dos arquivos atualizados

- [REAL] A validação por script confirmou as seis correções, os seis hashes REV0, as 15 linhas do resumo, a ausência de enunciados Markdown sem estatuto e os seis artefatos existentes no JSON.
- [REAL] `REGISTRO_MAPA_K03.json` passou por `json.loads` e pela função interna de validação de `rotas.py`, chamada sem registrar, com `olhou_dados=false` e seis artefatos.

| arquivo R1 | SHA-256 |
|---|---|
| `ENTREGA_K03.md` | `9abb6f25674c696e8b5dcd883645883a2a488a7a1b0c606e46755b3b7b1c388c` |
| `ESTADO_K03.md` | `d8af0bc6b363e13d675d29bf9c79479359d88681bffb13213bf1e21467558eb9` |
| `MODELO_FORMAL_K03.md` | `c9b14d3bfe50907ee2a1eb717307bf5d67710b40afa9bfb33f45878d6c0b03d8` |
| `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` | `57632fcddce4af6465706c4846c879e93a888a4e1d760eb0ac88951e5053cae9` |
| `PERGUNTA_K03.md` | `1e5bb459540077bfcc59407bef60a612c207708ba54e85df232037b3dc9f7ea1` |
| `REGISTRO_MAPA_K03.json` | `3d8b83814cfbe8c0df1ca6fe3edefd9c7339a0f9de768c158e5a4ce4569ea02c` |

- [REAL] O hash de `ERRATA_K03.md` é calculado externamente após este anexo, para não criar autorreferência de conteúdo.

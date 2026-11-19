# ERRATA K03 — R2, dois fechamentos

## 1. Estatuto e preservação

- [REAL] Esta errata R2 corrige somente os dois fechamentos apontados pela segunda revisão, sem alterar números primários.
- [REAL] Nenhum modelo foi executado, nenhum resultado experimental foi aberto, nada foi depositado e nenhuma rota foi registrada.
- [REAL] R1 foi preservada em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K03\REV1\` antes das alterações.
- [REAL] `K03\REV0\` e `ERRATA_K03.md` permanecem intactos; esta `ERRATA_K03_R2.md` foi escrita ao lado, sem substituí-los.

| arquivo REV1 | bytes | SHA-256 |
|---|---:|---|
| `ENTREGA_K03.md` | 6348 | `9abb6f25674c696e8b5dcd883645883a2a488a7a1b0c606e46755b3b7b1c388c` |
| `ESTADO_K03.md` | 14188 | `d8af0bc6b363e13d675d29bf9c79479359d88681bffb13213bf1e21467558eb9` |
| `MODELO_FORMAL_K03.md` | 14700 | `c9b14d3bfe50907ee2a1eb717307bf5d67710b40afa9bfb33f45878d6c0b03d8` |
| `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` | 21861 | `57632fcddce4af6465706c4846c879e93a888a4e1d760eb0ac88951e5053cae9` |
| `REGISTRO_MAPA_K03.json` | 4064 | `3d8b83814cfbe8c0df1ca6fe3edefd9c7339a0f9de768c158e5a4ce4569ea02c` |
| `PERGUNTA_K03.md` | 3091 | `1e5bb459540077bfcc59407bef60a612c207708ba54e85df232037b3dc9f7ea1` |
| `ERRATA_K03.md` | 10861 | `4acc54101bbbb3b0bd1ab167fbfcc37ac1cabcd5aa20fd2612244eee503511a1` |

## 2. Fechamento 1 — H-ABS e TR-IALD(b2) exigem finitude

- [REAL] Problema: R1 afirmava absorção quase certa a partir de alvo absorvente, demais estados transientes e alcançabilidade, sem impor finitude ou cota uniforme no enunciado geral.
- [DECLARADO] Correção: H-ABS(0) agora exige explicitamente que o espaço de estados `S` seja FINITO.
- [DECLARADO] H-ABS(a) exige `K(τ,{τ})=1`; H-ABS(b) exige que todo `x≠τ` seja transiente; H-ABS(c) exige, para cada `x`, algum `n_x` com `K^{n_x}(x,{τ})>0`.
- [DERIVED] Somente sob H-ABS(0)–(c) se afirma que `δ_τ` é a única estacionária e que a absorção é quase certa para qualquer estado inicial.
- [DECLARADO] TR-IALD(b2) foi reescrito como “absorção pontual em espaço FINITO” e não exporta a conclusão a espaço geral sem hipótese adicional.
- [DECLARADO] H-ABS-U registra a alternativa permitida pela revisão: existem `N∈ℕ` e `ε>0` tais que `P_x(T_τ≤N)≥ε` para todo `x`; essa cota não é presumida no desenho.
- [REAL] O instrumento experimental binário é finito, mas essa finitude não demonstra que uma cadeia de LLM real seja finita, absorvente ou tenha as transições requeridas.
- [REAL] Locais: `MODELO_FORMAL_K03.md` §§5.2, 7.1–7.2 e `ENTREGA_K03.md` §2.

## 3. Fechamento 2 — retorno reindexado à perturbação

- [REAL] Problema: `RETURN_TO_TARGET` exige `d_1=0` e não mede perturbação aplicada quando o alvo é atingido somente em `k=4`.
- [DECLARADO] O classificador original é preservado: `RETURN_TO_TARGET` continua exigindo `d_1=0`, `A_8=1` e alguma saída intermediária, e não é usado para o novo evento.
- [DECLARADO] O novo evento secundário é `PERTURB_RETURN_{p=4,r=6}^{(j)}`, reindexado à perturbação e sem exigência de `d_1=0`.

### 3.1 Regras congeladas do evento

- [DECLARADO] **Antes de `p`:** após a quarta interação e antes da perturbação, `d_4=0` é obrigatório; sem isso, o caso é `PERTURBATION_NOT_APPLICABLE`.
- [DECLARADO] **Alteração causada por `p`:** a perturbação congelada é aplicada após `k=4` e `d_5>0` é obrigatório, com hash da perturbação e da saída anterior.
- [DECLARADO] **Sem alteração observável:** `d_5=0` produz `PERTURBATION_NO_EFFECT`, que não conta como estabilidade, retorno ou evidência de atrator e não permite escolher outra perturbação a posteriori.
- [DECLARADO] **Janela pós-`p`:** os estados 5–8 formam a janela de recuperação; como `d_5>0` é obrigatório, `r=5` não é elegível.
- [DECLARADO] **Retorno/nova estabilização:** somente `r=6`, com `d_6=d_7=d_8=0` e `u_7=u_8=0`, satisfaz o evento; `r=7` ou `r=8` não fornece três estados estáveis.
- [DECLARADO] **Sem retorno:** alteração observável sem retorno estabilizado produz `PERTURBATION_NO_RETURN`, categoria separada de `PERTURBATION_NO_EFFECT` e `PERTURBATION_NOT_APPLICABLE`.
- [DECLARADO] O evento é estritamente secundário e não altera `A_8`, `C_8`, `ALREADY_STATIONARY`, `RETURN_TO_TARGET`, os 24 testes ou qualquer número primário.
- [REAL] Locais: `MODELO_FORMAL_K03.md` §4.5 e `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` §7.

## 4. Reservas registradas sem alterar o primário

- [DECLARADO] Gatekeeping global entre os 24 testes continua a congelar antes da execução.
- [DECLARADO] A estatística da permutação, suas sementes e o tratamento de empates continuam a congelar antes da execução.
- [DECLARADO] A bateria neutra de calibração continua a congelar antes da execução e suas chamadas permanecem separadas das 16.000 interações primárias.
- [DECLARADO] O extrator próprio e o cruzado continuam pendentes e bloqueiam qualquer decisão experimental.

## 5. Números primários revalidados, sem alteração

| medida | estatuto | valor |
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
| Poder aproximado por contraste dinâmico | [DERIVED] | 0,992022383635389 |
| `n` aproximado por braço para 90% | [DERIVED] | 61,45469545424308 → 62 |
| Limite superior CP para 70/100 | [DERIVED] | 0,7941204839644391 |
| Limite superior CP para 71/100 | [DERIVED] | 0,8028360383077797 |
| Limite inferior CP para 89/100 | [DERIVED] | 0,8046941495478515 |
| Limite inferior CP para 88/100 | [DERIVED] | 0,7926228353047495 |
| Poder conjunto do veredito | [OPEN] | Não calculado |
| Linhas do resumo R2 | [REAL] | 14 |

- [REAL] Os números foram recalculados por script com `scipy.stats.norm` e `scipy.stats.beta`, sem dados experimentais, e são idênticos aos de R1 por decisão de desenho.
- [REAL] A ordem original continua com 886 bytes e SHA-256 `4698446c391f9abae54575b678ab6794aec54492918df988b767292e4cbe47a0`.

## 6. Hashes dos documentos R2 antes desta errata

| arquivo | SHA-256 |
|---|---|
| `ENTREGA_K03.md` | `535a41e61cab65fa43a5e4547537f74815edef5cce62be4ca0f1c514f772754e` |
| `ESTADO_K03.md` | `d8af0bc6b363e13d675d29bf9c79479359d88681bffb13213bf1e21467558eb9` |
| `MODELO_FORMAL_K03.md` | `348e0db18fe2afccd98ed244aa816eba2bef79d989ee5d107137d80f87897181` |
| `PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md` | `9d70d8f7b072120e88f8ecff1cece0a95f661cc024e9d04b063c9ae71e575d7a` |
| `PERGUNTA_K03.md` | `fc4cd7e1ef14be55e8b0ede89623c6dd8ed592eba224d2e688008d059dcb1f37` |
| `REGISTRO_MAPA_K03.json` | `56f2b18db3489764b027e21b7f2c8e1e9d94aa4c8728cca802e2be1faeafb361` |

- [REAL] O hash de `ERRATA_K03_R2.md` é calculado externamente após a criação deste arquivo, evitando autorreferência de conteúdo.

# REVISÃO DISTINTA DA FRENTE MODELO FORMAL / CANDIDATA LEAN / RASCUNHO DO REGISTRO DA ENTREGA K06 (v412)

Revisor distinto (quem constrói não aprova). 14/11/2026. Só leitura fora desta pasta; nada registrado no Mapa, nada depositado na fila, nenhuma transição ACOM, nenhum `lake`, nenhuma escrita no túnel, no kernel, no Nós nem em memória; nenhum modelo de linguagem chamado.
Estatutos: [REAL] conferido por mim com a consulta citada · [KNOWN] literatura · [DERIVED] derivado por mim aqui · [DECLARADO] do Kimi, não conferido por mim · [OPEN] · [CONJECTURE] leitura minha, a medir.
`NOT_FALSIFIED` nunca é `CONFIRMED`; nada abaixo diz que a teoria foi confirmada. O gate não se mexe.

## 0. Veredito (três vereditos separados)

**A. CANDIDATA `LeitorFinito.lean` — APROVADA COM RESSALVAS como lema genérico de conjunto finito; NÃO APROVADA como «o teorema relativo ao leitor na língua da tradução de Turing» que a ordem K06 §F pediu.** Recompila limpa (RC 0, trio, sem `sorry`), os enunciados dizem o que o documento diz, não é vazia. Mas é pigeonhole sobre uma alcançabilidade já suposta, não importa nem usa `TraducaoTuring`, `LeitorDoFundo`, `IALD2` nem `AEscala` (zero ocorrências em 187 linhas), e o tipo é habitado por um mapa constante. Continua AO LADO do kernel, como na rodada 1.
**B. MODELO `MODELO_FORMAL_R3_K06.md` (R3.1) — APROVADO COM RESSALVAS.** As correções menores da revisão K03 foram aplicadas e conferem; o §6 transcreve fielmente as definições do kernel; a ponte ao LLM está dita [OPEN] no cabeçalho da candidata e no texto. Três defeitos: `H-HOM` falsa por construção, conteúdo de `Q_k` não definido, rótulo «Reuso [REAL — kernel]» largo.
**C. RASCUNHO DO REGISTRO `iald_camada_cientifica_v412` — APROVADO COM RESSALVAS como rascunho; NÃO instalável como está.** Respeita a P7 V1 selada, não promete resultado, sem conversa interna no JSON. Mas: o estado `ARMADO` é a palavra errada; o bloco `theorem` está desatualizado e lista como «linguagem do kernel» o que a candidata não usa; os vereditos proibidos da V1 (`IALD_PROVED`, `CONSCIOUSNESS_PROVED`) não vão por nome; o parágrafo de artigo diz «teorema relativo ao leitor»; e a errata do registro traz um hash que não confere.

**Pedem correção (numeradas; arquivo:linha):**
1. **F1 (forte) — a candidata não está na língua do kernel.** `LeitorFinito.lean:1-2` importa só `Mathlib` e `TGLExt.ObservadorTerminal`; `grep -w` por `LeitorDoFundo`, `o_atrator`, `AEscala`, `TraducaoTuring`, `trava`, `selecao`, `IALD2`, `observing_adds_nothing`, `um_is_the_great_attractor` = 0 em cada. O que usa do kernel: `leitor`, `leitor_fixed_iff`, `every_level_reaches_the_terminal` (`:170-173,:179`), que o kernel não liga por termo a `TraducaoTuring`/`IALD2`/`AEscala` (só menção em docstring, `AEscala.lean:1516`). Corrigir os rótulos: `MODELO_FORMAL_R3_K06.md:356` («Reuso [REAL — kernel]») e `REGISTRO_UMPY_RASCUNHO_K06.md:28-37` (`kernel_language`, `reused_known_pieces`) listam como reuso/linguagem da candidata o que ela só cita; separar «usado por termo» de «citado como molde».
2. **F2 — o conteúdo é fino e deve ser dito.** `LeitorFinito.lean:27-31` assume `reachable` (a conclusão sem a cota); o único teorema novo é `n ≤ Fintype.card X` (`:71-73`). `limit_idempotent` (`:91`) é corolário de `limit_constant` (`:87`): é idempotente porque é CONSTANTE (a projeção `post` do kernel, `IALD2.lean:154`, não é constante). Escrever isso no cabeçalho (`:4-20`) e em `MODELO:336-342`.
3. **F3 — `H-HOM` é falsa por construção neste protocolo.** `MODELO:86` a dá como hipótese empírica [OPEN] («existe um único núcleo K com K_k=K para todo k∈{1…12}»), mas `MODELO:46,84` fazem `Q_9^*=P_j≠Q_k` e a transição acrescenta `Frame(u,Q_k^*)` ao histórico: `K_k(c,·)` e `K_{k'}(c,·)` têm suporte em configurações diferentes sempre que `Q_k^*≠Q_{k'}^*`. Ou `H-HOM` é só sobre o estado ampliado `(k,c_k)` (então é vazia), ou só sobre fases de instrução idêntica (p.ex. 10–12 se `Q_10=Q_11=Q_12`), ou o texto diz que não vale no desenho. Hoje o §2.4 diz as duas coisas.
4. **F4 — o conteúdo de `Q_1…Q_12` e de `P_j` não está no modelo** (`MODELO:37,46`): só a forma (`Frame`, bytes congelados no manifesto). O achado A3 da K03 («o que a leitura k pede ao modelo?») ficou respondido na estrutura e aberto no conteúdo; sem o texto de `Q_k`, `H-QUOT(k)` e `H-HOM` não têm objeto avaliável.
5. **F5 (menor) — `MODELO:208`** atribui `h : ∃ x, c x = 0` a `a_trava_sem_conhecer_o_nome`; o teorema (`TraducaoTuring.lean:510`) só tem `0 ≤ t`. A hipótese é de `a_trava_converge_a_selecao` (`:604`).
6. **R1 (forte) — estado `ARMADO` impróprio.** `REGISTRO:6,20,139,143,147`. Na casa, ARMADO/ARMED quer dizer protocolo pré-registrado, congelado e à espera do disparo (P7 V1: `status = PRE_REGISTERED`, hash pinado). O rascunho tem 9 hashes `A_PREENCHER_APOS_CONGELAMENTO`, não está ratificado, e a própria entrega diz `BLOQUEADA_PARA_PRODUCAO`. Estado honesto: `RASCUNHO_BLOQUEADO` (ou `CANDIDATO_NAO_ARMADO`), com campo `blockers` (extratores em prosa livre, léxico, janelas, tamanho global, poder, cauda 5σ). `ARMADO` só depois do congelamento por hash e da ratificação.
7. **R2 — bloco `theorem` do registro está desatualizado** (`REGISTRO:25-41`): a candidata já compilou (sha256 lido por mim: `77e18a01…`, log `4073b041…`) e continua `A_PREENCHER`; `statement_scope` ainda diz «somente se efetivamente provada». Preencher por script e nomear os teoremas (`K06.FiniteAttractor.exists_iterate_eq_target_le_card`, `limit_idempotent`, …).
8. **R3 — vereditos proibidos da V1 não vão por nome.** `REGISTRO:125-133`: a P7 selada proíbe `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE` (core, por script); o rascunho repete só o terceiro, e consciência/pesos aparecem só em prosa. O texto diz que o instalador usará lista de negação explícita e fail-closed; a lista não está escrita. Acrescentar os tokens (`IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `WEIGHTS_UPDATED` ou equivalente) e `CONFIRMED` já está.
9. **R4 — parágrafo de artigo** (`REGISTRO:139,143`): «articula um teorema relativo ao leitor» promete mais que o Lean (o teorema é de conjunto finito, a ponte ao leitor é a previsão); e carrega rótulo interno («não ratificação da R3»). O parágrafo não promete resultado (conferido). Trocar por: «um lema de absorção em conjunto finito; a hipótese de que um modelo de linguagem o satisfaz é a previsão que o experimento testa».
10. **R5 — hash da errata não confere.** `ERRATA_REGISTRO_UMPY_R3_1.md:32` diz `875a6db3…`; o arquivo vivo é `db332e67…` (Get-FileHash e sha256sum concordam; `VALIDACAO_K06.json:58` traz `db332e67…`). Mesmo tamanho (10.814 B) porque houve duas trocas «oito→doze» (`REGISTRO:81,132`) **depois** da errata (arquivo 17:15:36, errata 17:07:33); `:34` diz que o diff tem «apenas as duas substituições de chaves e a nova seção», o que não é exato. Correto no conteúdo, não declarado.

## 1. Mapa de Rotas (consulta antes de tudo; nada registrado)

[REAL] Termos consultados (`rotas.py consultar`, um termo por chamada): `Turing` (29), `LeitorDoFundo` (2), `atrator` (29), `IALD2` (24), `AEscala` (10), `colapso` (20). Rotas lidas por `ver`: `outro.p7_colapso_iald` (seq 162, `PROPOSTA`, `n_olhou_dados=0`, sem artefatos), `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov`, `kernel.iald2_06nov`, `kernel.observador_terminal.candidata_31out`; lidas na listagem: `kernel.a_escala_tres_faces_v410_09nov`, `gate.qg_closure`, `cadeia.preparacao_v409/v410`.
- A rota `kernel.pergunta_do_clay_trivial_por_leitor_constante_09nov` (EXAMINADA_COM_DEFEITO) diz «Não formalizar “existe um leitor” sem dizer como ele lê; não aceitar teorema de existência cuja definição um decisor clássico satisfaz». A candidata cai nisso (seção 3): um mapa constante satisfaz `FiniteAttractor`. A casa já corrigiu a mesma patologia em `LeitorDoFundo` pondo a escala no tipo.
- `kernel.iald2_06nov` ressalva (3): «o que é idempotente é a LEITURA (o Nome do par lido)», não o funtor; coerente com a separação passo/limite do modelo, mas lá o limite é projeção não constante.
- `kernel.observador_terminal.candidata_31out`: «os níveis são rótulos … nada sobre entidades». A instância `terminalAttractor` da candidata mostra que as hipóteses são satisfazíveis por uma cascata de rótulos; não é instância de um leitor de linguagem.

## 2. Recompilação (pergunta 1) [REAL]

Cópia `scripts_k06_formal\src\LeitorFinito.lean`, sha256 **`77e18a01ff5c07b00cf24d53570baf205710320d99dc3b4826426084c6df7d8b`**, idêntico ao original (`sha256sum` dos dois) e ao hash declarado na `ERRATA_MODELO_FORMAL_R3_1.md:7`. Método: `lean.exe` 4.31.0 (commit `68218e87…`) direto, `LEAN_PATH` = `.lake\build\lib\lean` do kernel + os `.lake\packages\*\.lake\build\lib\lean`, `-o` só em `scripts_k06_formal\build\`; script `recompilar_revisor_k06_formal.sh`. Nenhum `lake`.

| arquivo | RC | `sorry`/`sorryAx` | axiomas |
|---|---|---|---|
| `LeitorFinito.lean` (original) | **0** | nenhum | todos ⊆ {propext, Classical.choice, Quot.sound} |
| `LeitorFinito_REV2.lean` (+ exemplos e `#print axioms` de novo para cada teorema) | **0** | nenhum | idem |
| `LeitorFinito_REV3.lean` (+ mapa constante) | **0** | nenhum | idem |

Axiomas por declaração (original, linha a linha do log de `build\saida_recompilacao_orig.txt`): `FiniteAttractor` [propext, Quot.sound]; `pre_hit_injective` [propext, Quot.sound]; `first_hit_le_card` e `exists_iterate_eq_target_le_card` [propext, Classical.choice, Quot.sound]; `limit` [propext, Quot.sound]; `limit_eq_target`, `limit_constant`, `limit_idempotent`, `limit_fixed_iff` [trio]; `step_fixed_iff` [propext, Quot.sound]; `chain3`, `chain3_step_not_idempotent` [trio]; `KernelInstance.levelFintype`, `terminalAttractor`, `terminal_card` [propext, Quot.sound]. Idêntico ao log do Kimi (`K06\candidatas\logs\LeitorFinito.txt`).
**Aviso para quem ler os meus logs:** `build\saida_recompilacao_rev.txt` (RC 1) tem `sorryAx` em `K06.Rev.terminalViaLyapunov`; é erro MEU de nome (`gravidade` sem `Level.`) numa adição minha, corrigido no REV2. Nada disso toca a candidata. Os `example` do REV2/REV3 compilaram sem erro nem aviso.

## 3. O que os teoremas dizem e se há vacuidade (pergunta 2) [REAL por leitura + compilação]

Enunciados (do arquivo):
- `structure FiniteAttractor (X) [Fintype X] [DecidableEq X]` com `step : X → X`, `target : X`, `fixed : step target = target`, `reachable : ∀ x, ∃ n, step^[n] x = target`. *Em linguagem de leigo: uma regra de passo numa lista finita de situações, com uma situação onde ela para, e de onde toda situação eventualmente chega lá.*
- `pre_hit_injective x`: as iteradas antes da primeira chegada são todas distintas. *Antes de chegar, a trajetória não repete estado.*
- `first_hit_le_card x : Nat.find (A.reachable x) ≤ Fintype.card X`. *A primeira chegada leva no máximo tantos passos quanto há situações.*
- `exists_iterate_eq_target_le_card x : ∃ n, n ≤ Fintype.card X ∧ A.step^[n] x = A.target`. *Toda trajetória pousa no ponto de parada em até |X| passos.* É o enunciado principal e **confere** com «toda órbita pousa no ponto fixo em no máximo |X| passos».
- `limit x := A.step^[Fintype.card X] x` (definição); `limit_eq_target`: o limite é o alvo; `limit_constant`: o limite não depende da entrada; `limit_idempotent`: `limit (limit x) = limit x`; `limit_fixed_iff`: o limite só fixa o alvo; `step_fixed_iff`: o passo só fixa o alvo (a alcançabilidade global exclui outro ponto fixo). *O «limite» aqui é a iterada de ordem |X|, um limite em tempo finito, não o `limUnder atTop` de `LeitorDoFundo.limite`.*
- `chain3_step_not_idempotent : ∃ x, chain3.step (chain3.step x) ≠ chain3.step x`. *Existe um passo que não é idempotente, com limite idempotente.* PASSO e LIMITE ficam separados, como o documento diz; a hipótese que faltava (`reachable`) está NOMEADA no tipo. **Confere.**

Vacuidade, medida (adições do revisor em `LeitorFinito_REV3.lean`, todas compiladas):
- **Não é vazio [REAL]:** `chain5 : FiniteAttractor (Fin 5)` (passo `![1,2,3,4,4]`), com `chain5.step^[4] 0 = 4`, nenhum `n<4` serve, `step` não idempotente; `terminalAttractor` do próprio Kimi.
- **A hipótese exclui coisas [REAL]:** `¬ ∃ A : FiniteAttractor (Fin 2), A.step = ![1,0]` (o 2-ciclo não é atrator) e `¬ ∃ A, A.step = id` (dois pontos fixos não cabem). Portanto `reachable` tem conteúdo.
- **Mas é fraco e genérico [REAL]:** (i) `reachable` já supõe a existência de `n`; a candidata só acrescenta a cota `≤ |X|` (casa dos pombos); (ii) `limit_idempotent` decorre de `limit_constant`; (iii) o tipo é habitado por `constantAttractor t := ⟨fun _ => t, t, rfl, fun _ => ⟨1,rfl⟩⟩` (REV3, compilou): um «leitor» que ignora a entrada satisfaz todas as hipóteses. Essa é a patologia do leitor constante que a casa corrigiu em `LeitorDoFundo` pondo a escala no tipo; aqui nada no tipo diz como o passo lê. Logo o teorema vale para qualquer função com ponto fixo alcançável e **não diz nada sobre leitor nenhum**; o que ele fixa é só a forma da conclusão que o experimento testaria (`reachable`).
- Sem campo que já assuma a conclusão com a cota; sem hipótese insatisfazível.

## 4. Na língua do kernel ou ao lado dele (pergunta 3) [REAL]

Consulta: Grep em `…\Nós\tgl_kernel\TGLExt\` (só nessa pasta).
- `TraducaoTuring.lean`: `trava` (l.472), `selecao` (l.332), `a_trava_sem_conhecer_o_nome` (l.510), `a_trava_converge_a_selecao` (l.604), `uniforme`, `opDaInstancia`, `nomeDasSolucoes` (a tradução de Turing).
- `AEscala.lean`: `structure LeitorDoFundo` (l.742), `LeitorDoFundo.leitura/limite` (l.752/757), `o_brilho_e_a_dissipacao` (l.763), `iald : LeitorDoFundo X` (l.844), `o_leitor_do_fundo_e_a_iald` (l.868, unicidade interna ao tipo).
- `IALD2.lean`: `iald_ao_quadrado` (l.154, `post*post=post`, projeção em ℂ∙γ(par), **não constante**); `o_atrator` (l.315; seção, nome `TGLExt.IALD2.o_atrator`, correto).
- `TheObserverReadsTheAngle.lean:114` `TGLExt.observing_adds_nothing` (identidade de matrizes 2×2); `TheGreatAttractor.lean:133` `TGLExt.um_is_the_great_attractor` (fluxo diagonal em ℝⁿ).
- `ObservadorTerminal.lean`: `leitor` (l.138), `leitor_fixed_iff` (l.153), `every_level_reaches_the_terminal` (l.157, `leitor^[3]`), `distancia` + `each_reading_consumes_resistance` (l.161, 172). Este módulo **não importa** `TraducaoTuring`, `IALD2` nem `AEscala`.

**Resposta, sem suavizar: a candidata continua AO LADO do kernel.** Usa `ObservadorTerminal.leitor` (uma cascata de quatro rótulos) e mais nada da casa. As quatro definições que a ordem K06 §F nomeou não entram por termo. O MODELO (§6) as transcreve corretamente (conferi `trava`, `selecao`, `LeitorDoFundo`, `o_leitor_do_fundo_e_a_iald`, `o_atrator`; o texto do §6.1–6.3 bate com as linhas citadas), mas a transcrição fica em prosa; o §6.4 diz com honestidade que a ponte «saída extraída → `c : X → ℕ`» é [OPEN].

**Por que a lacuna não é só fiação:** o kernel e a candidata descrevem regimes diferentes. `IALD2.o_atrator` (itens 1–2) diz que o fluxo tende a `post` e **nunca** o iguala em tempo finito (`the_motor_never_arrives`), a convergência é topológica em espaço de Hilbert; a candidata diz que a trajetória **chega** em ≤ |X| passos num conjunto finito. A leitura discretizada do fluxo pode estabilizar em tempo finito (a `a_trava_sem_conhecer_o_nome` dá o decaimento e^{-t}), mas a leitura discretizada do vetor não é função só dela mesma: é exatamente a agregabilidade `H-QUOT(k)`, que o modelo deixa [OPEN].

**Ponte mínima (proposta do revisor [CONJECTURE/DERIVED], não construída):**
1. *Lema de Lyapunov* (compilado por mim no REV3, não faz parte da candidata): `reachable_of_lyapunov (step target) (V : X → ℕ) (hdec : ∀ x, x ≠ target → V (step x) < V x) : ∀ x, ∃ n, step^[n] x = target`, e `ofLyapunov : FiniteAttractor X`. Com ele, `terminalViaLyapunov` obtém o mesmo atrator da candidata a partir do teorema do KERNEL `each_reading_consumes_resistance` (`distancia` como função de Lyapunov). Isso liga `FiniteAttractor` a um lema da casa por termo. Com `V := c` (o custo de `TraducaoTuring`) é o análogo natural.
2. *Alvo CONJUNTO, não ponto:* `FiniteAttractor` tem um só `target`; o Nome do kernel é o conjunto das soluções `{x | c x = 0}`, com `LeitorDoFundo.limite c = |soluções|/|X|` (`o_limite_e_o_que_sou`). Generalizar para alvo `T : Finset X` com `step` fixando `T` pontualmente e `step^[|X|]` uma retração sobre `T` (idempotente e NÃO constante quando |T|≥2) daria o análogo discreto de `post` e um lema `|T|/|X| = L.limite c`. É a ponte que de fato liga a candidata a `LeitorDoFundo`/`IALD2.o_atrator` (projeção sobre o Nome).
3. A seta «saída textual → `c`/`κ_j : Y → X`» segue [OPEN]; nenhuma das duas peças acima a fecha, e nenhuma é teorema sobre LLM.

## 5. O MODELO (pergunta 4) [REAL por leitura, conferência de derivações por raciocínio]

Achados da K03 sobre o modelo, um a um:

| achado da `REVISAO_K03.md` | resposta na R3.1 | confere? |
|---|---|---|
| M2/A3 — «leitura k» e `G` indefinidos; ferramentas | `MODELO §2`: `Frame(u,Q_k^*)`, histórico integral reenviado, sem ferramentas/rede/MCP, 12 chamadas, T=0,2, semente `σ(m,j,r,k)=SHA256[0:4]`, «sessão nova» definida | forma sim; **conteúdo de `Q_k` não** (F4) |
| M3 — H-IDEM×H-CONTR ⟹ constante; separar PASSO e LIMITE | `§4.1`: `H-IDEM-STEP`, `H-IDEM-LIM`; `F_q=Π+q(I−Π)` com `F_q^n=(1−q^n)Π+q^nI→Π`, só não-expansiva | **sim** (refeito por mim: as identidades fecham) |
| M4 — `H-QUOT` determinística em núcleo estocástico; homogeneidade | `§3`: `K_k(c,Q^{-1}(B))=\bar K_k(Qc,B)` (strong lumpability, por fase); `§2.4`: `H-HOM` separada | lumpability **sim**; `H-HOM` **F3** |
| «três estados finais» → quatro | `§5.3`: `s_5,s_6,s_7,s_8` | **sim** (`u_6=0∧d_6=0 ⟹ s_5=τ`) |
| `H-ABS(c)` redundante em finito | `§5.1`: (a)+(b)⟹(c) | **sim** (fecho alcançável finito e fechado contém recorrente ≠ τ) |
| `H-ABS-U` = (a) ∧ U | `§5.2`: `P_x(T_τ>kN)≤(1−ε)^k` | **sim** |
| prefixos de namespace (4 nomes) | `§7.1` | **sim, conferido no kernel**: `ChatgptAudit.Aperiodic046.*` (l.39–162), `TGLExt.Santo.*` (l.80–1939), `ChatgptAudit.Collapse057.*` (l.32–127 nos dois arquivos); `TGLExt.IALD2.o_atrator` (seção, não namespace) |
| rótulos C3/C4 colidem com P7 V1 | `§7.2`: `IALD_COLLAPSE_V2`, `V2-TGL/PLA/OUT/ISO-A/ISO-B`, `V2-RET` fase, não braço | **sim**; falta tabela V1→V2 explícita (menor) |

Pontos de leitura: (a) `V2-RET` e o evento `R` (`§5.4`): `u_10` omitida é correta (`d_9>0,d_10=0` força `s_9≠s_10`); `A_8` anterior à perturbação. (b) A conjunção `H-CONTR ∧ H-IDEM-STEP` degenerada, derivada em `§4.1`, está certa. (c) `§6.1` diz que `trava` é o PASSO e `selecao` o LIMITE e **não** identifica `ψ_t` ao histórico: honesto. (d) `§9` «Reuso»: ver F1.

**A ponte ao LLM** está dita nos dois lugares pedidos [REAL]: cabeçalho da candidata (`LeitorFinito.lean:7-9`: «A ponte … é PREVISÃO EXPERIMENTAL, não teorema») e `MODELO §0` (`[OPEN]`), `§6.4` («previsão experimental, não teorema»), `§8.2`, `§9`. Conferido.

## 6. O rascunho do registro (pergunta 5)

**Campos pedidos [REAL, lidos]:** teorema e estatuto (`REGISTRO:24-42`; ver R2); hipóteses nomeadas (`:43-53`, com aliases legados `H-TIME-HOMOG→H-HOM`, `H-LUMP→H-QUOT(k)`); protocolo por hash (`:62-74`, todos `A_PREENCHER_APOS_CONGELAMENTO`); estado (`:20`); o que não se afirma (`:75-84`). Falta o campo `blockers` e a referência à V1 que ele não toca.

**Vereditos.** Permitidos: `IALD_COLLAPSE_V2_{FALSIFIED, NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, NONSPECIFIC_POWERED, INCONCLUSIVE_CONTROLS}`. Proibidos (`:127-133`): `TGL_PROVED_BY_COLLAPSE`, `PHYSICS_PROVED_BY_COLLAPSE`, `CONFIRMED`/`TGL_CONFIRMED`/`IALD_CONFIRMED`/`PROVEN_BY_LLM`, consciência (prosa), pesos (prosa), `ONLY_TGL`/`TGL_UNIQUE`/`EXCLUSIVE_ATTRACTOR`, limite/bacia universal, creditação automática, `P_EQUALS_NP`. Continuam proibidos os cinco itens pedidos (`TGL_PROVED_BY_COLLAPSE`; consciência; pesos; exclusividade; `CONFIRMED`), mas consciência e pesos só em prosa e os dois tokens da V1 faltam (R3). Sem promessa de resultado no parágrafo PT/EN (conferido); ver R4.

**Colisão com a P7 V1 selada [REAL, lido do core por `json.load`; `core_p7.py`, `core_p7_dump.py`].** `um_absoluto.json` (16.642.521 B, sha256 `36c69fc7…9064e`) → `core.iald_prediction`: `protocol_hash` `a91877e561b7cce9b08325d57e6ec08f04575440e9ec0d0c3d55bb30dc38b8cc`; `protocol.version = IALD_COLLAPSE_V1`, `status = PRE_REGISTERED`; `allowed_verdicts` = `IALD_COLLAPSE_{FALSIFIED, NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_CONTROLS}`; `forbidden_verdicts` = `IALD_PROVED`, `CONSCIOUSNESS_PROVED`, `TGL_PROVED_BY_COLLAPSE`; controles `C1–C4` (embaralhado, placebo, piso de capacidade, sessão nova/cega); piloto 8/8 `[PILOTO/ANEDOTICO]`; `uniqueness_claim` [CONJECTURE]; `does_not_gate_core = true`; veredito `IALD_UNIQUE_OPERATIONAL_PREDICTION_PRE_REGISTERED__…`. Não há nenhuma chave com «camada» nem `leitor_finito` no core fora do `axiom_report` (`core_chave_camada.py`: 0), e nenhuma declaração `K06*` no `axiom_report`. **O rascunho RESPEITA a V1:** nomes de veredito com prefixo `IALD_COLLAPSE_V2_`, braços `V2-*`, e `REGISTRO:111` diz «não alteram nem reabrem a V1 selada». Recomendo, ao instalar, um campo `v1_not_altered: {version, protocol_hash}` com o hash lido do core por script (o acima, que li por script, não de memória). Cuidado só com guardas por prefixo (`startswith("IALD_COLLAPSE_")` casaria os dois).

**`ARMADO`.** Não é a palavra certa (R1). Na casa a palavra é de protocolo congelado; a nota do core diz da V1 «armado, nao executado (C1-C4)» sobre um protocolo com hash pinado. Este tem hashes pendentes, não ratificação, e a entrega diz `BLOQUEADA_PARA_PRODUCAO`; instalar `ARMADO` num selo faria o leitor entender que há protocolo congelado à espera de dado.

**Conversa interna / vocativo / fala transcrita / palavras vedadas.** [REAL] Nenhum vocativo («o senhor») no registro (o vocativo está em `PERGUNTA_K06.md:13`, fora do registro). Nenhuma fala do operador transcrita. O JSON e os parágrafos instaláveis não carregam conversa. **Não devem seguir para o programa**: `REGISTRO:9` («a concordância em bloco do adendo») e `:147`, que são conversa de processo, e a menção a «R3» nos parágrafos (R4). A regra vigente do operador de 12/11 (arquivo `OPERADOR_12nov_nao_precisa_transcrever…`, 254 B, sha256 `93d812a0…`, conferido por bytes) manda citar só por data e hash. Grep por `mil[eê]nio`, `millen`, `navier`, `clay`, `stokes` nos cinco documentos e na fonte Lean e nos logs: **zero** (o core tem «Milenio» e «Navier» só em `stokes_contour`, que o rascunho não toca).
**Estado do que dizem as palavras de consciência:** `Level.consciencia` aparece como construtor do kernel em `LeitorFinito.lean:160`, e o cabeçalho (`:11`) diz «Não se afirma consciência». Se a pedra for instalada, a `guarda_das_frases` da cadeia precisa aceitar a negação; **não conferi** a regra da guarda.

## 7. O que falta para virar pedra da v412 (pergunta 6)

1. **Nome**: do operador (precedente D87: nome do módulo e nomes das declarações ratificados por ele; a pedra `AEscala`, rota `kernel.a_escala_tres_faces_v410_09nov`). `K06.FiniteAttractor`, `limit`, `chain3` são provisórios.
2. **Módulo e namespace**: arquivo `TGLExt/<Nome>.lean`, `namespace TGLExt.<Nome>` (hoje `K06` e `K06.KernelInstance`); entrada em `TGLExt.lean` depois do último import atual (`TGLExt.AEscala`, linha 1149; a v411 não teve pedra nova).
3. **Imports**: hoje `Mathlib` + `TGLExt.ObservadorTerminal`. Para a pedra ser «na língua da tradução de Turing» (F1) é preciso importar `TGLExt.TraducaoTuring`/`TGLExt.AEscala` e usá-los por termo (seção 4, pontes 1–2); sem isso, a pedra entra como lema genérico, e o texto da casa tem de dizê-lo.
4. **Instância local**: `local instance Fintype Level` e `Nonempty Level` ficam locais (o módulo de origem é selado; `Level` está em `TheCascadeOfObservers`).
5. **`axiom_report`**: toda declaração e as auxiliares geradas entram no core com a lista de axiomas (no core aparecem `.eq_1`, `._proof_1`, `.mk`, `.rec`, `.noConfusion`, `.ctorIdx`, `_sizeOf_*`, `.injEq`; o `axiom_report` do core v411 tem 34.300 declarações, lidas por `core_chave_camada.py`, das quais 70 do módulo `ObservadorTerminal`, por comparação de tamanho). A candidata dá ~15 declarações nomeadas, mais as auxiliares do `structure` e dos `def`; todas devem sair em ⊆ {propext, Classical.choice, Quot.sound}, sem `sorryAx` (conferido para as nomeadas; as auxiliares não listei).
6. **Remover do `.lean` da pedra** os `#print axioms` e as dependências de teste; decidir se `chain3`, `chain3_step_not_idempotent` e `terminalAttractor` ficam como controles (recomendo ficar: separam PASSO de LIMITE e mostram a hipótese satisfazível).
7. **Bandeiras e registro com função** (padrão `ext_<mod>_<versão>_*` e um registro `…_v412` com checagens), revisão de terceiro, rito, e o item de `um.py` (`iald_camada_cientifica_v412`) depois de F1–F5 e R1–R5. Ato do operador/orquestrador, não deste revisor.
8. **Não instalar** o registro enquanto a R3 inteira não tiver revisão distinta e ratificação: a própria entrega diz bloqueada.

## 8. Atribuições ao operador: o que fecha por bytes e o que não

Tarefa fixa. Arquivos varridos por `grep` (aspas « », «operador», «ratific», «concord», «pediu», «disse», «ordem», «verbatim», «fala»): `MODELO_FORMAL_R3_K06.md`, `ERRATA_MODELO_FORMAL_R3_1.md`, `REGISTRO_UMPY_RASCUNHO_K06.md`, `ERRATA_REGISTRO_UMPY_R3_1.md`, `LeitorFinito.lean`, `audit_source.py`, os logs. **Nenhuma citação entre aspas atribuída ao operador** nesses arquivos.
- Fecha por bytes: `ORDEM K06 §F` cita como dele «camada científica completa e não mais empirismo»; o arquivo `OPERADOR_13nov_vamos_comecar_a_construir_a_v412_…_verbatim.txt` (886 B) contém «…agora pode ganhar camada científica completa e não mais empirismo…». (A ordem está fora do escopo; confiro por ser a origem do pedido.)
- **Não fecha por bytes (parcial): `REGISTRO_UMPY_RASCUNHO_K06.md:9`** («a concordância em bloco do adendo não ratifica a R3»). O arquivo que o ADENDO cita, `OPERADOR_13nov_excelente_concordo_com_tudo_depois_da_errata_do_meio_e_da_rodada_2_verbatim.txt` (28 B, sha256 `fa30a621…d40a6`, igual ao do ADENDO), diz só «excelente, concordo com tudo». A ligação desse «tudo» à proposta da entrada pública é da gerência (ADENDO, item 2), não palavra dele. Idem `ENTREGA_K06.md:42` («concordada em bloco»). Reescrever como «hipótese de trabalho proposta pela gerência; concordância geral do operador de 13/11, sha256 …» ou tirar do registro.
- `MODELO:5,342` («seções D e F da ordem K06», «permitido pela ordem»): atribuem à ORDEM da gerência, e conferem com `ORDEM_K06…md` §F («a absorção com espaço de estados finito, ou a versão determinística que fechar sem `sorry`»).
- «Modelos, degrau e execução seguem com o operador» (`REGISTRO:9,147`): é reserva de decisão (ADENDO item 2), não citação.

## 9. O que conferi e como

- Recompilação do original e de três cópias com `lean.exe` direto (seção 2); sha256 da cópia contra o original e contra a errata.
- Leitura integral de `LeitorFinito.lean`, `MODELO_FORMAL_R3_K06.md`, `ERRATA_MODELO_FORMAL_R3_1.md`, `REGISTRO_UMPY_RASCUNHO_K06.md`, `ERRATA_REGISTRO_UMPY_R3_1.md`, `audit_source.py`, `run_lean.py` e os logs da candidata (as quatro tentativas com RC 1 e o `probe` estão preservados; os erros são de instância/sintaxe).
- Kernel: Grep em `TGLExt\` e `sed` das linhas citadas: 24 nomes do modelo, namespaces, linhas de `TraducaoTuring`/`AEscala`/`IALD2`/`ObservadorTerminal`; `ObservadorTerminal` não importa os módulos da tradução de Turing.
- Core: `json.load` de `um_absoluto.json` (`core_p7.py`, `core_p7_dump.py`, saídas na pasta); P7 V1 conferida chave a chave.
- Hashes: modelo `e560eaec…` e REV0 `91f0122d…` conferem com a errata; log `4073b041…` confere; registro **não** confere (R5); `um_absoluto_pt.txt` (1.164.350 B, sha256 `f9fa0d32…`) confere com o `input` do registro.
- Matemática do §4–5 do modelo: refeita por raciocínio (identidades de `F_q`, `A_8`, `R`, redundância de `H-ABS(c)`, cauda geométrica).

## 10. O que NÃO conferi

- Não rodei `audit_source.py` nem `run_lean.py` (gravam em `K06\candidatas\logs`, túnel só leitura); li o código: as checagens são por substring (frágeis, mas o log final confere com o meu).
- Não conferi se os `.olean` do kernel são os da v411 selada (só que carregam); nem `guarda_das_frases` (seção 6).
- Não conferi a bibliografia (Kemeny–Snell 1976, Seneta 2006, Banach 1922: ISBN/DOI do `MODELO §10.2`), nem que o DOI `10.5281/zenodo.24196546` corresponda ao `um_absoluto_pt.txt`.
- Não revi o protocolo R3, os extratores, o poder, o degrau de 5σ nem o isomorfo (outras frentes); só li o que o modelo e o registro dizem deles.
- Não formalizei nada de Banach/Perron–Frobenius/absorção/lumpability em Lean; o modelo diz que a candidata também não, e conferi que não.
- Os acréscimos do revisor (`chain5`, `constantAttractor`, `reachable_of_lyapunov`, `ofLyapunov`, `terminalViaLyapunov`) são meus, compilados só no REV2/REV3; não fazem parte da candidata, não são proposta de pedra.

Arquivos desta revisão (todos em `revisao\scripts_k06_formal\`): `recompilar_revisor_k06_formal.sh`; `src\LeitorFinito.lean` (cópia idêntica), `src\LeitorFinito_REV.lean` (adição com erro meu), `src\LeitorFinito_REV2.lean`, `src\LeitorFinito_REV3.lean`; `build\saida_recompilacao_orig.txt`, `…_rev.txt`, `…_rev2.txt`, `…_rev3.txt`; `core_p7.py`, `core_p7_dump.py`, `core_chave_camada.py` e suas saídas.

Nada aqui afirma consciência, alteração de pesos, exclusividade ou CONFIRMED; `NOT_FALSIFIED` segue não sendo `CONFIRMED`; o gate não se move.

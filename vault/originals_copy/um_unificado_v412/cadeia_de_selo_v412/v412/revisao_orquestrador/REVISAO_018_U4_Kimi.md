APROVADO_COM_RESSALVAS — 0 ALTO, 0 MEDIO, 5 BAIXO.

# REVISÃO 018 — U4 (tipo III, R3) — revisor distinto Kimi (16/11/2026)

> Revisão distinta da unidade U4 da ORDEM 018. Não li `REVISAO_018_U4_Codex.md` nem nada em
> `revisao_orquestrador\U4_Codex\`; este parecer foi formado só dos artefatos, do relatório T6
> (`revisao\REVISAO_16nov_R3_T6-os-termos-adotados-no-tipo-iii-e-na-t1.md`), do `DESENHO_v412_R1.md` e de
> recompilação própria. Só leitura fora da minha pasta; toda escrita ficou em
> `revisao_orquestrador\U4_Kimi\` (cópias de trabalho, logs, objetos) e neste relatório. Nenhum provedor remoto,
> nenhum `lake build`: só `lean.exe` 4.31.0 (commit 68218e87) sobre os `.olean` de `C:\t\k411c\final`.
> Mapa não consultado (não precisei; nada registrei).

**Material da unidade (hashes conferidos por sha256, prefixo 16):**

| arquivo | sha16 | confere com a ordem |
|---|---|---|
| `candidatas_c1\tipo_iii\REV3\TipoIIIControles.lean` | `bbce90f332ff5a64` | sim |
| `candidatas_c1\tipo_iii\REV3\TipoIIIUmSoBoost.lean` | `3e7342cb5478bc3d` | sim |
| `candidatas_c1\tipo_iii\REV3\PROVA_E_ALCANCE_GERENCIA.md` | `c65eca1c28ae50e2` | sim |

## 1. Achados (por gravidade; todos BAIXO)

**B1 (BAIXO) — O objeto `ErgodicidadeDeMautner.olean` arquivado pela gerência não reproduz; causa não determinada.**
Artefato: `candidatas_c1\build\ErgodicidadeDeMautner.olean` (log `candidatas_c1\build\ErgodicidadeDeMautner.log`,
15/11 16:17–16:19, RC 0, sha256 do fonte `1074aa5b2c172960…`, o mesmo do fonte atual). Recompilei o MESMO fonte
(sha256 idêntico), com o MESMO lean.exe 4.31.0 e o MESMO sandbox (oleans do sandbox sem modificação desde
02/11–12/11, anteriores a 15/11), DUAS vezes em pastas distintas: as duas saídas são bit a bit iguais entre si
(sha256 `cf395c3bf9d9c199…`) e diferentes do objeto arquivado (sha256 `5914fe2ff63bf71b…`; 76% dos bytes
diferem, tamanho 1.551.536 vs 1.552.864). O serializador é, portanto, determinístico nas minhas mãos, e a
divergência está nas condições da rodada de 15/11, que não consegui reproduzir nem explicar pelos logs.
Impacto demonstrado: nenhum semântico — as interfaces são equivalentes à prova: o meu `TipoIIIUmSoBoost.olean`,
construído sobre o MEU objeto da Ergodicidade, saiu bit a bit igual ao da gerência (sha16 `0eb51ad10222c62f`),
que foi construído sobre o objeto anômalo. A fonte compila limpa hoje (RC 0, zero avisos, 51 constantes, só o
trio). *Conserto:* recompilar `ErgodicidadeDeMautner.lean` com o script atual (`compilar_candidata.ps1`),
arquivar log e objeto novos, e conferir se dão `cf395c3bf9d9c199…`; se derem, o objeto de 15/11 era transiente e
o caso se fecha; se não derem, investigar antes de selar a v412.

**B2 (BAIXO) — A seção 9 ("Como reproduzir") não prepara a compilação do `TipoIIIUmSoBoost`.**
`REV3\PROVA_E_ALCANCE_GERENCIA.md` l.236-240 diz que `-Deps` prepara as doze dependências e que `-Nome` compila
as candidatas, mas não diz que `TipoIIIUmSoBoost.lean` importa `ErgodicidadeDeMautner` (candidata à parte, fora do
`-Deps`) e que o `LEAN_PATH` do script a busca em `<pasta-pai do script>\build` (l.13-14 de
`compilar_tipo_iii.ps1`). Quem seguir a seção 9 a partir da pasta REV3 falha: o pai da REV3 é `tipo_iii\`, e
`tipo_iii\build` não contém `ErgodicidadeDeMautner.olean` (que mora em `candidatas_c1\build`). O comentário do
script na cópia da REV3 ("o build\ das outras candidatas", l.13) só é verdade para a cópia da raiz de `tipo_iii\`.
Verifiquei as duas montagens: com o objeto da Ergodicidade no build do pai, compila; sem ele, o import falha.
*Conserto:* acrescentar à seção 9 a nota que a própria REV4 já traz ("Para `TipoIIIUmSoBoost`, … compile antes
`ErgodicidadeDeMautner.lean` … ou aponte para onde a compilação verificada dela já está").

**B3 (BAIXO) — No "contra" da opção A, um custo superestimado (resíduo de neutralidade).**
`REV3\PROVA_E_ALCANCE_GERENCIA.md` l.96-99: o contra de A afirma que "os nomes do Codex que dizem III₁ teriam de
mudar, porque as candidatas importam os módulos dele". Não teriam: a própria candidata reexporta o teorema do
Codex com o nome do que ele prova e declara não renomear nada dele (l.122-123), arranjo que compila e lê bem. A
afirmação pesa o prato de A além do fato. (A REV4 do documento já reescreveu este ponto como "Os nomes do Codex
não precisam mudar…".) Não chega a empurrar a resposta — os "a favor"/"contra" principais de A e de B são
espelhos — mas é o único item factualmente forte demais nas duas perguntas. *Conserto:* a redação da REV4, ou
"seria coerente rever os nomes do Codex" no lugar de "teriam de mudar".

**B4 (BAIXO) — Um aviso preexistente numa dependência, não declarado no documento, e é ele que furta a
reprodução bit a bit daquela dependência.**
`candidatas_c1\tipo_iii\dep_codex\TowerWedgeIndex.lean` l.131:6: `warning: 'change …' tactic does nothing`
(linter `unusedTactic`). O aviso é do Codex (o log da gerência o tem igual; as fontes batem com o manifesto, ver
seção 4) e a R3 não o introduziu — mas a `PROVA_E_ALCANCE_GERENCIA.md` não o menciona em nenhum lugar, e quem
reproduzir vai encontrá-lo sem aviso. Efeito colateral medido: a mensagem persistida carrega o caminho absoluto
da fonte para dentro do `.olean`; por isso `TowerWedgeIndex.olean` é a ÚNICA das 12 dependências que não sai bit
a bit igual entre pastas (a minha e a da gerência diferem só nesse trecho e no hash de cabeçalho correspondente;
as outras 11 saem idênticas). *Conserto:* declarar o aviso na seção 2 do documento (um parêntese basta); se um
dia se mexer nas fontes do Codex, remover o `change` morto.

**B5 (BAIXO) — O ponteiro para o `RESULTADO_GERENCIA.json` já não aponta para a R3.**
`REV3\PROVA_E_ALCANCE_GERENCIA.md` l.9-10 manda os "hashes, tempos e a lista de teoremas com os axiomas" para
`RESULTADO_GERENCIA.json`. Hoje esse arquivo (gerado em 16/11 15:55) registra o sha256 `0c28be72049eb776…` para
`TipoIIIControles.lean` — que é o conteúdo da REV4, não o da R3 (`bbce90f332ff5a64`). O registro da R3 existe e
confere (`RESULTADO_GERENCIA.json.bak_R3`, gerado em 16/11 14:17: `bbce90f3…`, RC 0, 0 avisos, 29 teoremas, só o
trio, `log_e_desta_fonte: true`), mas o texto não o nomeia. *Conserto:* citar o backup no texto ("o registro
desta versão está em `RESULTADO_GERENCIA.json.bak_R3`") ou versionar o JSON por revisão.

**Contexto que não é achado da R3:** a pasta de trabalho já vai à frente da unidade revisada — `tipo_iii\` e
`REV4\` contêm `TipoIIIControles.lean` = `0c28be72049eb776…` e `PROVA_E_ALCANCE_GERENCIA.md` =
`1f9011adef951d9e…` (a REV4 aplica emendas posteriores à ordem 018). B2 e B3 já estão cobertos lá, pelo que vi
por diff (não li a revisão alheia). Meu parecer vale para a R3, como ordenado.

## 2. Os oito achados do T6, um a um

| achado | estado | evidência na R3 |
|---|---|---|
| T6-01 (1ª pergunta: "contras" que valiam para as duas; A sem as palavras da pedra; B sem o precedente) | SANADO | `PROVA` l.94-106: A ganha as palavras da pedra ("a luz na cunha cumpre o critério do núcleo", ou "no relógio do vácuo só o Um fica parado", l.96-97); B ganha o precedente Tetelestai com a ressalva de proveniência (l.100-102); e a linha partilhada "Nas duas, o tipo III₁ não é termo e o 'construir' de 15/11 fica por cumprir. O que separa A de B é só o nome que a pedra leva" (l.105-106) elimina a assimetria apontada. Resíduo em B3 acima. |
| T6-02 (2ª pergunta sem favor/contra, sem quem constrói, sem a espera da v412) | SANADO | `PROVA` l.108-118: Sim e Não com "a favor"/"contra" simétricos; "Quem constrói: em 15/11 eu lhe disse que era o Codex; pelas suas ordens de 16/11 a criação fica com a gerência e a revisão vai ao orquestrador" (l.114-115); a errata da estimativa ("milhares de linhas" era de outras três peças; uma delas o Codex fez em ~500) vai dentro do "contra" (l.111-113); "Falta também o senhor dizer se a v412 espera pelo passo ou sela antes" (l.119-120) e seção 8, item 1 (l.229-230). Desvio deliberado e correto em relação ao texto sugerido pelo T6: onde o T6 escreveu "o Codex e o Kimi revisam", a R3 diz "a revisão vai ao orquestrador" — que é a ordem posterior do operador (DESENHO, item 24). |
| T6-03 (o `s` mudo de `a_borda_como_conjunto_nao_determina`; texto dizia mais que o termo) | SANADO (pelas DUAS vias) | Termos novos compilados por mim, só no trio: `todo_boost_da_cunha_leva_a_borda_nela_mesma` (`TipoIIIControles.lean` l.510-520) e `boosts_de_parametros_diferentes_sao_diferentes` (l.524-530). E o texto foi posto na altura do termo: a docstring reparada diz "O `s` do enunciado só escolhe a testemunha (a conclusão não fala dele)" (l.481-484); o cabeçalho atribui a família aos dois termos novos e diz que `a_borda_como_conjunto_nao_determina` "só afirma que existe um, diferente da identidade" (l.80-85); a tabela do documento repete o mesmo (l.153). |
| T6-04 (as duas marcas lado a lado com objetos diferentes; faltava a ponte) | SANADO | `marca_do_estado_na_lingua_do_criterio` (l.462-473): a marca do estado escrita com `net rightWedge` e `fockFlow`, saindo do teorema do kernel por `physicalFockCertificate.flow_is_Ad` — compilada por mim, só o trio. Cabeçalho (l.64-67) e documento (l.62-66) citam as duas igualdades do kernel (`physical_net` e `flow_is_Ad`) como pedido. |
| T6-08 (componente U4: a numeração "segunda"/"terceira" conferência nos cabeçalhos) | SANADO no escopo U4 | `TipoIIIControles.lean` l.12-15 e `PROVA` l.3-7 agora concordam: "a terceira conferência de 16/11, revisor D1" e "a conferência de conserto do mesmo dia … `REVISAO_16nov_R3_T6`". Os componentes (1) e (2) do T6-08 são da T1 (unidade U5): fora do meu escopo, não conferidos. |
| T6-09 ("mesma resposta"; errata sem marca nem consequência; a vírgula) | SANADO | `PROVA` l.21-24: "À gerência ele mandou a mesma parte 'em palavras simples'. A mensagem abre por uma frase do Codex, não traz a frase sobre provar em Lean … e fecha com a frase sobre o Codex e o Lean citada adiante." Errata, terceiro ponto (l.178-184): agora com a marca "[citado de memória por um revisor; não conferido no primário; não é termo]" e a consequência "'Não é a luz' vale, por termo, só mantendo os relógios." A citação de 15/11 volta com a vírgula (l.179: "a do estado é o que se diz do sujeito, e a do espectro é a leitura na borda"). |
| T6-10 (a escolha "testemunhada" fora da lista; a língua única sem justificativa; três palavras sem glosa) | SANADO | `PROVA` l.173-176: "Quatro escolhas formais … e 'testemunhada' foi lida como 'com o vácuo por vetor testemunha'." A língua única justificada em l.91-92 ("o resto da pergunta de 15/11, que foi feita nas quatro línguas; por isso vão numa língua só"). Glosas postas: "predicado (a lista de exigências)" (l.41-42), "reexportada, isto é, o mesmo teorema com outro nome" (l.62-63), "realizações (modos de escrever o relógio e o espelho de um vetor)" (l.140). |
| T6-11 (o script não entrava na pasta da fonte; objetos não reproduziam) | SANADO e VERIFICADO | `compilar_tipo_iii.ps1` l.27-33 (raiz e cópia REV3): `Push-Location (Split-Path -Parent $fonte)` antes do `lean.exe`, com a nota "(revisor T6)"; `PROVA` l.240: "o script entra na pasta de cada fonte antes de compilar." Verificação empírica na minha cópia: o meu `TipoIIIUmSoBoost.olean` saiu com sha16 `0eb51ad10222c62f` — exatamente o valor que o T6 pediu e bit a bit igual ao da gerência; 11 das 12 dependências também saíram bit a bit iguais (a exceção é o B4, cosmético). |

## 3. As duas perguntas da seção 3 estão neutras?

Sim, com um resíduo (B3). Critério aplicado: nenhuma das duas empurra para uma resposta nem lê o operador além
da letra.

* **Primeira pergunta** (l.94-106). A pergunta é aberta ("que nome a pedra leva?") e a linha partilhada ("Nas
  duas, o tipo III₁ não é termo e o 'construir' de 15/11 fica por cumprir. O que separa A de B é só o nome que a
  pedra leva") impede a leitura enviesada que o T6 apontou. Os "a favor"/"contra" centrais são espelhos (o favor
  de A é o contra de B, e vice-versa). O precedente Tetelestai entra no favor de B com a ressalva de proveniência
  ("a fala dele sobre isso não está nos arquivos de bytes de `cunhagens_13out`, por isso vai sem aspas") — marcado
  como manda a casa. Resíduo: o contra de A superestima o custo de renomear (B3).
* **Segunda pergunta** (l.108-120). Aberta ("sim ou não?"), com os dois lados simétricos; diz quem constrói em
  cada cenário e cobra o que faltava (a espera da v412). A errata da estimativa dentro do "contra" do Sim corrige
  um número que a própria gerência tinha dado e que sustentava o medo do custo — é informação devida, não
  advogação. A única fala atribuída ao operador vem pela cópia do Codex, com a ressalva explícita de que "vale
  como declarado pelo Codex, não está nos bytes da casa" (l.17-19) — não lê o operador além da letra. A frase que
  justifica reapresentar a pergunta ("Pergunto agora porque o Codex pôs o nome tipo III₁ num enunciado que prova
  o critério", l.90-91) é fato conferido (`Vinculo.IsTypeIII1`, predicado do critério do núcleo).
* Declaração de não-escolha coerente com a prática: "A candidata da gerência reexporta o teorema do Codex com o
  nome do que ele prova … e não renomeia nada do Codex. Isso não escolhe por ele." (l.122-123).

## 4. O que conferi (com o log da recompilação)

Tudo compilado em CÓPIA minha (`revisao_orquestrador\U4_Kimi\copia\`), com o script da unidade copiado para lá.
Única adaptação, declarada: no laço do `-Deps`, pular o módulo cujo `.olean` já existe (a verificação de hash
contra o manifesto roda a cada rodada), para caber no limite de tempo do executor; cada fonte compilou uma vez,
na ordem do manifesto, RC 0 em todas. `ErgodicidadeDeMautner.lean` (sha16 `1074aa5b2c172960`, o mesmo do
`RESULTADO_ErgodicidadeDeMautner.json`) foi compilada do fonte por script meu equivalente, para
`U4_Kimi\build\` (o build do pai da cópia, como o `LEAN_PATH` do script pede).

| módulo | RC | início → fim (16/11) | sha16 do fonte | avisos |
|---|---|---|---|---|
| TowerWedgeIndex | 0 | 16:23:04 → 16:23:41 | a2771c25c905ee35 | 1 (B4) |
| WedgeHorizonObserver | 0 | 16:23:41 → 16:24:21 | 32b777fc4ebf6e38 | 0 |
| VinculoCriterion | 0 | 16:24:21 → 16:25:03 | 71a5ab2d1562e505 | 0 |
| FockCharacters | 0 | 16:25:03 → 16:25:50 | c269d42209ef7f9f | 0 |
| PhysicalCoreCenter | 0 | 16:25:50 → 16:26:47 | 3e07a77003a4e883 | 0 |
| PhysicalCoreMultipliers | 0 | 16:28:17 → 16:29:30 | 4fe93935cf9465a9 | 0 |
| PhysicalCoreFactor | 0 | 16:29:30 → 16:30:27 | 598cd9d7c5ba7874 | 0 |
| WedgeFactor | 0 | 16:30:28 → 16:31:22 | e13011b5fa886a9c | 0 |
| Classificacao | 0 | 16:31:22 → 16:32:07 | c9ff132bc5b2f763 | 0 |
| TransportCenter | 0 | 16:33:29 → 16:34:29 | 37b53e0be5835998 | 0 |
| TransportPair | 0 | 16:34:29 → 16:35:17 | 62a107e925e0eac6 | 0 |
| ObserverClassification | 0 | 16:35:17 → 16:35:54 | 9e395f44884cdcb8 | 0 |
| ErgodicidadeDeMautner (do fonte) | 0 | duas vezes: 67 s e 59 s (2ª: 16:50:27 → 16:51:26), objetos bit a bit iguais | 1074aa5b2c172960 | 0 |
| **TipoIIIControles (R3)** | 0 | 16:46:23 → 16:47:17 | **bbce90f332ff5a64** | 0 |
| **TipoIIIUmSoBoost (R3)** | 0 | 16:48:46 → 16:49:29 | **3e7342cb5478bc3d** | 0 |

Logs completos: `revisao_orquestrador\U4_Kimi\copia\build\*.log` e `U4_Kimi\build\ErgodicidadeDeMautner.log`.

* **Axiomas.** 29 `#print axioms` do `TipoIIIControles` e 3 do `TipoIIIUmSoBoost`: TODOS `[propext,
  Classical.choice, Quot.sound]` e nada mais (conferido por varredura dos logs; conjunto distinto único). O mesmo
  vale para as 12 dependências e para as 51 constantes impressas da Ergodicidade. Nenhum `sorryAx`.
* **Fontes.** Nenhum `sorry`, `admit` ou `axiom` fora de comentário nos dois módulos R3 (varredura textual).
  29 + 3 = 32 teoremas, como o documento anuncia ("trinta e duas declarações com termo", l.125).
* **Manifesto.** As 12 fontes de `dep_codex\` passam na verificação de hash do próprio script a cada rodada;
  amostra de 6 conferida contra os originais do Codex
  (`kimi\K07\CODEX\TIPO_III1_VINCULO\…`): byte a byte iguais (VinculoCriterion, TowerWedgeIndex, TransportCenter,
  PhysicalCoreFactor, WedgeFactor, ObserverClassification).
* **Reprodutibilidade dos objetos.** 11/12 dependências bit a bit iguais às da gerência; `TowerWedgeIndex`
  difere só no caminho absoluto embutido pela mensagem de aviso (B4). `TipoIIIUmSoBoost.olean` =
  `0eb51ad10222c62f`, bit a bit igual ao da gerência e ao valor exigido pelo T6-11. `TipoIIIControles.olean`: a
  comparação com a gerência não se aplica — o objeto arquivado por ela é do conteúdo REV4 (`0c28be72…`, log das
  15:53); o registro da R3 está em `RESULTADO_GERENCIA.json.bak_R3` (14:17, RC 0, 0 avisos, 29 teoremas, trio) e
  a minha compilação confirma o mesmo resultado. O caso da Ergodicidade é o B1.
* **Enunciados ao acaso, lidos de perto:** os três termos novos do T6 dizem o que as docstrings dizem
  (`todo_boost_da_cunha_leva_a_borda_nela_mesma` quantifica sobre todo `s`; `boosts_de_parametros_diferentes…` é
  injetividade do parâmetro; `marca_do_estado_na_lingua_do_criterio` fala de `net rightWedge` e `fockFlow.U` e
  sai por `flow_is_Ad`). `o_fluxo_da_leitura_e_o_do_criterio` é `rfl` e a docstring o declara ("identidade por
  construção … não fato novo"). `dois_numeros_nao_acrescentam_a_um` usa exatamente os dois parâmetros de rapidez
  do teorema do Codex que invoca.

## 5. Método e limites

Revisão distinta: não li o parecer do outro revisor da U4 nem nada em `revisao_orquestrador\U4_Codex\`. Li os
três artefatos da unidade, o relatório T6 indicado na ordem, o `DESENHO_v412_R1.md`, os scripts de compilação e
JSONs de resultado da pasta da candidata; compilei tudo em cópia minha. Por diff de bytes entre REV3 e REV4 (sem
ler a revisão alheia) registrei que a pasta de trabalho já vai adiante. Não conferi os componentes da T1 no
T6-08 (unidade U5). Não instalei nada, não toquei em kernel, `um.py`, Chatgpt, espelho, site ou memória; nenhuma
chamada a provedor; Mapa não consultado. Escritas: só em `revisao_orquestrador\U4_Kimi\` e neste relatório.

— Kimi (revisor distinto, ORDEM 018, U4), 16/11/2026.

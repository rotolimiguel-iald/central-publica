APROVADO_COM_RESSALVAS

# REVISÃO 018 — U7 (Adendo B) — revisor Kimi

Unidade: candidata `MinimoFuncionalDeEnergia` (R0), pedida pelo operador em 16/11 por bytes.
Fonte revista: `candidatas_c1\REV18\MinimoFuncionalDeEnergia.lean` (sha256 e8a4932297df704dbd6341fd76dec7a37080d6744159d0dad55ae024b46867f3 — idêntica à de `candidatas_c1\MinimoFuncionalDeEnergia.lean`, de onde o log da gerência foi gerado).
Revisão distinta, formada por mim; não li `REVISAO_018_U7_CodexAstra.md` nem pastas de outros revisores. Trabalho em `revisao_orquestrador\U7_Kimi\`.

## Achados

### ALTO
Nenhum.

### MÉDIO
Nenhum.

### BAIXO

**B1 — A glossa do referente é da gerência, não do operador.**
`MinimoFuncionalDeEnergia.lean:13` — o cabeçalho escreve «o operador identificou o leitor que pousa e retorna **(a candidata `CamadaCientifica`)** com o mínimo funcional de energia». A fala por bytes do operador («O leitor que pousa e retorna é o meu mínimo funcional de energia (A_C, lá dos primeiros protocolos…)», verificada no arquivo com o sha256 dado) não nomeia candidata nenhuma. A identificação do referente com `CamadaCientifica` é plausível (é a candidata que prova pouso e retorno — `CamadaCientifica.lean:254,364,371,377`), mas é leitura da gerência posta na voz do operador.
Conserto: marcar a glossa como da gerência — ex.: «o leitor que pousa e retorna [a gerência lê: a candidata `CamadaCientifica`]».

**B2 — A ponte interna do kernel `opDaInstancia c = penalty D` não é construída nem nomeada como lacuna.**
`MinimoFuncionalDeEnergia.lean:22-25, 55-61` — o cabeçalho cita como ponto de partida «a penalidade dos vínculos `H = Σ D†D`, a seletora apofática `A_C = −H` (`selector_nonpos`)» de `TheEquationOfTruth` (`TheEquationOfTruth.lean:51,103`), mas a `seletora` da candidata é `−(opDaInstancia c)` (linha 74) e `selector_nonpos` **nunca é usado**: a não-positividade é re-provada do zero (linha 167-170) via `a_energia_do_custo`. A identificação entre as duas realizações internas do kernel (o `H` de penalidade por vínculos e a diagonal do custo) não existe em Lean; para custo cláusula a cláusula (`c = Σ cj`) ela é curta — `opDaInstancia c = penalty` das projeções de violação, na linha de `a_trava_fatora` (`TraducaoTuring.lean:482-488`). O «O que NÃO se afirma» (linhas 57-61) exclui as realizações de bancada 80_/92_/128_, mas não nomeia esta lacuna interna; a frase «aqui o vínculo é o custo da instância» (linha 59) cobre o sentido, sem construí-lo.
Conserto: adicionar o lema `opDaInstancia (fun y => ∑ j, cj j y) = penalty …` (ou uma frase explícita na seção de não-afirmações declarando que essa identificação interna também não está construída).

**B3 — No caso binário, a ponte trava↔exponencial já era montável na casa.**
`MinimoFuncionalDeEnergia.lean:19-21` — a afirmação verificada do cabeçalho («nenhuma ocorrência de `truthFlow`, `EquationOfTruth` ou `NormedSpace.exp` em `TraducaoTuring`, `AEscala` nem na candidata») é literalmente verdade e eu a aferi (ver §3 abaixo). Mas o caso binário da igualdade central já seguia de duas peças existentes: `a_trava_binaria_e_o_fluxo_do_axioma` (`CamadaCientifica.lean:254-269`: `trava c t v = axiomFlow P t v` para `c ≤ 1`) concatenada com `axiomFlow_eq_exp` (`TheAxiomAndTheFalseWitness.lean:161-166`: `NormedSpace.exp ((-t) • (1 - P)) = axiomFlow P t`). O que é próprio da candidata é o caso geral (`c : X → ℕ` arbitrário, onde o `axiomFlow` não chega), a forma-gerador (derivada) e os fatos de energia — a novidade está correta, só subdeclarada no recorte.
Conserto: opcional; uma frase no «De onde vem» reconhecendo a pré-ponte binária via `axiomFlow` fecha o ponto contra sobreleitura da novidade.

## Respostas aos pontos do adendo

**1. Recompilação em cópia própria — confere.** Copiei a fonte para `U7_Kimi\MinimoFuncionalDeEnergia.lean` (sha16 idêntico, e8a4932297df704d) e compilei com `compilar_candidata.ps1` copiado para a minha pasta, `lean.exe` 4.31.0 sobre os `.olean` de `C:\t\k411c\final`: RC 0, 36 s, saída contendo **somente** as 11 linhas de `#print axioms`, nenhum aviso, nenhum erro. Os 11 teoremas dependem só de `[propext, Classical.choice, Quot.sound]` — sem `sorryAx`. Idêntico ao log da gerência (`build\MinimoFuncionalDeEnergia.log`, RC 0, 15:45:17→15:45:53) e ao `RESULTADO_MinimoFuncionalDeEnergia.json` (11 teoremas, `todos_so_o_trio: true`, `sorryAx: false`, 1 definição `seletora`). Meu log: `U7_Kimi\build\MinimoFuncionalDeEnergia.log` (INICIO 17:12:36, FIM 17:13:12, RC 0). Sem `sorry`/`axiom` na fonte fora do comentário da linha 63 («Sem sorry, sem axioma novo.»).

**2. Enunciados × nomes/comentários — conferem.** Li no kernel cada símbolo usado e comparei:
- `travaOp` é a diagonal `e^{−s·c(x)}` (`TraducaoTuring.lean:982-983`), `travaOp_apply` a iguala a `trava` (:985); `opDaInstancia` é a diagonal do custo (:116-117); `solucao_por_coordenadas` (:237-238) é o que o item 6 usa. `T H s = truthFlow H ↑s = NormedSpace.exp ((-↑s) • H)` (`TheEquationOfTruth.lean:178-181`); `T_apply_eigen` (:420-421) e `hasDerivAt_flow_apply` (:375-376) têm exatamente os enunciados que a candidata lhes atribui.
- Teorema central (`:88-96`): `travaOp c s = T (opDaInstancia c) s` — prova por extensão na base ortonormal, `trava_single` de um lado, `T_apply_eigen` com autovalor `c x` do outro. Diz o que o nome diz. A forma A_C (`:99-107`) é a reescrita correta `(−s)•H = s•(−H)` (`neg_smul`/`smul_neg`). A derivada (`:110-128`) é no parâmetro real, e a regra da cadeia com a inclusão ℝ→ℂ está feita como deve ser: `hasDerivAt_flow_apply` no ponto `((s:ℝ):ℂ)` composto via `HasDerivAt.scomp` com a derivada `(1:ℂ)` de `Complex.ofRealCLM`, ajuste `e2` por `one_smul` + a ponte. Correto.
- Itens 3–6 batem com os nomes; `com_custo_binario…` (`:205-221`) dá `seletora c = −(1 − P)` para `c ≤ 1`, via `solucao_por_coordenadas` — a forma de face do verbete do Atlas (ver §4).

**3. Ausência afirmada no cabeçalho — aferida.** Busca recursiva no kernel do Nós (`Nós\tgl_kernel\`), incluindo arquivos ignorados pelo git (o `.lake\build` apareceu só como `.ilean`/`.trace`): `truthFlow`, `EquationOfTruth`, `NormedSpace.exp` — **0 ocorrências** em `TraducaoTuring.lean`, `AEscala.lean` e `CamadaCientifica.lean`. Mais forte: dos 9 arquivos-fonte do kernel que mencionam `trava` (`AEscala`, `IALD2`, `TraducaoTuring`, `Testemunho`, `QGCitationDischarge`, `FiniteSitePermutations`, `TheStation`, `GNSBridge`, `F1Fecho394\CovariantTensorPullbackR3`), nenhum menciona o fluxo; e dos únicos dois com `opDaInstancia` (`TraducaoTuring`, `AEscala`), idem. Nenhum lema do kernel ligava a trava ao fluxo da equação da verdade. A ressalva de escopo é o achado B3 (a pré-ponte binária via `axiomFlow`, fora do recorte nomeado).

**4. Alcance — dito com clareza suficiente.** Consultei o Atlas um verbete por vez: `A_C (funcional-Amor)` («A_C = −H₃L; … nulo exatamente sobre o Nome, negativo em todo o resto», TGL_ATLAS.md:564-567) e `A_C — anatomia (128_)` («face A_C^∂ = −(1−P) (92_…)», :570-574) — ambos existem e dizem o que o cabeçalho lhes atribui. A seção «O que NÃO se afirma» (:55-61) declara explicitamente que a identificação termo a termo com 80_/92_/128_ não é construída e que a palavra Amor não é tipada — e de fato «Amor» não aparece tipada no arquivo. O título («é o fluxo do A_C: a trava é a exponencial da seletora») afirma o que o arquivo constrói, com `A_C := seletora := −opDaInstancia c`; nada no texto deixa entender mais do que os termos provam — a identificação procede pela assinatura do verbete (forma `−H`, nulo exatamente no Nome, não-positivo, face `−(1−P)`), que é o que os teoremas provam. A lacuna interna não nomeada é o achado B2.

**5. Teoremas vazios/enfeite — não há; estrelas no lugar certo.** Itens 3 e 6 sem ★ e de fato são leitura: `a_seletora_e_nula_exatamente_no_nome` é `neg_eq_zero` + `mem_ker`; `o_nome_por_coordenadas` é desdobramento de definições com `mul_eq_zero`; o item 6 é `congr` + `solucao_por_coordenadas` (lema do kernel), como a legenda declara. `trava_single` é auxiliar não listada como resultado. Os ★ (itens 1, 2, 4, 5) cobrem conteúdo próprio verificado: a ponte geral, o gerador, o funcional de energia `re ⟪v, opDaInstancia c v⟫ = Σ c(x)·‖v_x‖²` (ausente do kernel e de `CamadaCientifica` — conferi) com seu mínimo exato, e a monotonicidade da energia (que não é o `a_performance_decai` do kernel — aquele é sobre a `leituraPerformada` escalar, quantidade distinta).

**6. O adversário — sim, e basta no alcance declarado.** A igualdade central é, matematicamente, «a exponencial de uma diagonal é a diagonal das exponenciais», mediada por `T_apply_eigen` autovetor a autovetor — `travaOp` é *definida* como a diagonal das exponenciais e `opDaInstancia` como a diagonal do custo. O que a candidata acrescenta é a fiação (ausente, ver §3) entre as duas pedras, mais o gerador (a derivada), a energia e seu mínimo, e a forma de face binária. Para o pedido do operador — «conferir e provar que é ele mesmo» — isso basta no alcance declarado: a identidade é provada no nível dos termos do kernel (`travaOp = T ∘ opDaInstancia`, `A_C` gerador, assinatura completa do verbete). O passo que falta — o custo como penalidade de vínculos cláusula a cláusula, i.e. `opDaInstancia c = penalty …` — não é exigido pelo pedido nem pelo escopo que o cabeçalho declara, mas é o elo natural que falta entre as duas realizações internas do kernel; está registrado como B2. A conjugação da bancada (A4 do verbete) está fora por declaração explícita («nada sobre a natureza»), corretamente.

**7. A letra do operador — um deslize menor.** O nome do arquivo vem da fala dele («o meu mínimo funcional de energia») e o cabeçalho o declara («o nome é do operador») — correto. O «de resto concordo com tudo» não é tratado no arquivo (não lhe cabia). O único ponto em que o arquivo lê a fala além do que ela diz é a glossa «(a candidata `CamadaCientifica`)» — achado B1.

## O que conferi (lista)

1. Hashes: fonte REV18 e fonte em `candidatas_c1\` (sha256 e8a4932297df704d…, idênticas); RESULTADO (28f3cc1eba409b1d…); arquivo do operador (7119d4921cea00f3…, lido na íntegra — 1 linha).
2. Recompilação em cópia própria (`U7_Kimi\`), script copiado, `lean.exe` 4.31.0 + `.olean` de `C:\t\k411c\final`: RC 0, zero avisos, 11×`#print axioms` só com o trio; log em `U7_Kimi\build\MinimoFuncionalDeEnergia.log`. Conferido contra o log e o JSON da gerência — idênticos em conteúdo.
3. Enunciados do kernel citados/usados, lidos na fonte: `opDaInstancia`, `opDaInstancia_ofLp`, `opDaInstancia_single`, `solucao_por_coordenadas`, `trava`, `trava_ofLp`, `travaOp`, `travaOp_apply` (`TraducaoTuring.lean`); `penalty`, `selector_nonpos`, `truthFlow`, `T`, `hasDerivAt_flow_apply`, `T_apply_eigen` (`TheEquationOfTruth.lean`); `axiomFlow`, `axiomFlow_eq_exp` (`TheAxiomAndTheFalseWitness.lean`).
4. Ausência da ponte no kernel: varredura recursiva com ignorados incluídos (trava × fluxo; opDaInstancia × fluxo; os três termos nomeados no cabeçalho × os três artefatos nomeados).
5. Cruzamento com `CamadaCientifica` (pouso/retorno citados no cabeçalho: `a_trava_tende_ao_nome`, `a_leitura_de_resolucao_finita_pousa`, `em_k_leituras_pousa`, `pousa`/`permanece`; a pré-ponte binária `a_trava_binaria_e_o_fluxo_do_axioma`).
6. Atlas consultado um termo por vez: verbetes `A_C (funcional-Amor)` e `A_C — anatomia (128_)`.
7. Não-unicidade de data: cabeçalho «16/11/2026» consistente com o arquivo do operador e com o log da gerência.

Nada instalado, nada enviado a provedor, nenhuma pergunta ao operador; kernel lido, não tocado.

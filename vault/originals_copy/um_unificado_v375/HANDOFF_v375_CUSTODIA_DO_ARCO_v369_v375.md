# HANDOFF v375 — a custódia do arco v369 → v375: espelho `the_boundary`, README, portas, raws e o site

**De:** a gerência (sessão da Central / `Nós\`), 27/09/2026. **Para:** a sessão do site — dona do espelho `the_boundary` e do site (ordem do operador de 11/09/2026). Documento de trabalho entre sessões irmãs; todo hash e número abaixo foi LIDO do artefato por script (`medir_handoff_v375.py` → `MEDIDA_HANDOFF_v375.json`, no scratchpad da gerência), nenhum de memória.

## 0. A ordem

**Verbatim do operador (27/09/2026):** «Escreva o Handoff para a sessão irmã que cuida da custódia e do repositório, para ela atualizar tudo por favor, custodiando a versão recente, atualizando readme, portas, raws e a versão do site».

**Push:** vale a autorização vigente do operador (19/09/2026, verbatim): «eu disse que eu faria o push, pode custodiar tudo inclusive a v368 e realizar o push como vínhamos fazendo». Os irreversíveis seguem do operador: force-push, apagar histórico, renomear, Zenodo. Na dúvida, perguntar a ele antes.

**Regra que agora vale também aqui (CLAUDE.md da raiz, 27/09):** o cético é AFERIDOR, não cego. Antes de escrever «falta», consultar o inventário da bancada, o selo e o kernel, e citar a consulta. Nos dois sentidos: nem «falta» falsa, nem «vinculado» falso.

## 1. Onde o espelho está e o que falta custodiar `[REAL — git, só leitura]`

- espelho: `HEAD` = `origin/main` = `659c90a`; árvore limpa.
- última custódia: `e654787 custodia(v368 + sementes v365-v367; v360 nao se custodia): A INVERSAO DO NOME E A OBSTRUCAO ESPINORIAL — selo v3…`
- **pendente: o arco v369 → v375** (sete versões seladas, todas COMPLETAS; a v375 é a custodiada, as outras entram como sementes do arco, no molde «v368 + sementes v365–v367»). **A v360 continua sem custódia**, como decidido.

| versão | data | rodada | `um.py` sha16 | o que é |
|---|---|---|---|---|
| v369 | 19/09/2026 | COMPLETA | `d9f5bd5dffc3333d` | o teste dos relógios: o portão do poder e o registro com hash (não-cego) |
| v370 | 23/09/2026 | COMPLETA | `4b3405de809aef61` | o ¬IsEmpty da testemunha, o fornecedor de Cartan, a conjunta V3 e a Testemunha lida ao lado |
| v371 | 25/09/2026 | COMPLETA | `3c870dea6b42ca03` | a IALD na torre de Jones, o transporte à escada de helicidade ±2 (gráviton: CONJECTURE), a equação da verdade, o contrato v3.1 e a reta de luz |
| v372 | 26/09/2026 | COMPLETA | `dc71229d0395aefb` | a gravidade quântica da TGL formalizada como implicação fechada POR CITAÇÃO (contrato v3.2 habitado sob hipóteses nomeadas), o leitor A-8, a UV dissolvida pela tipagem, o H_min como Hamiltoniano oculto, a ponte IALD = ρ* |
| v373 | 26/09/2026 | COMPLETA | `ba914d49498d209b` | H2 e H3 quitadas POR CITAÇÃO numa classe própria (gpc_), o modo de quitação que separa as classes, duas projeções fora de M, o homônimo de H_min dito, a fronteira sem o item BRST/UV (semiclássico por construção) |
| v374 | 27/09/2026 | COMPLETA | `1c1513dbf03071f8` | A DECLARAÇÃO TETELESTAI: a solução da gravidade quântica da TGL de ponta a ponta, composta por citação (um item aberto no caminho: os tipos dos certificados vs a literatura); dois campos da luz por termo |
| v375 | 27/09/2026 | COMPLETA | `ba234a6d384cb3f5` | TETELESTAI, A CONFERÊNCIA CONSUMATIVA: cada item do caminho da QG fechado, vinculado ou sabido por referência científica, com 3 parâmetros nomeados da implicação (a janela, G > 0, o relógio), lido nesta rodada; a declara |

## 2. O selo da v375 `[REAL — lido de Nós\um_absoluto_selo.json]`

- timestamp `2026-09-27 12:26:31`; selftest `FAIL_CLOSED_SELFTEST_PASSED`; `full_static_witness_exists` = `False` (lê falso e lê certo: é teorema).
- `result_hash` `a3718953021fd41d7e4aecf511a017748bce2b21be1dc466ae3d68b79ae03f1a`
- `formal_source_hash` `ea57265940235547eea9b714940ed0d3c7e43d1348805e7f05276f9484367feb`
- sha256 do próprio `um_absoluto_selo.json`: `a88bb75fc615f4b0fcce4945af27bab0b196f4f35fb600e158382508f4723619`
- gate (string inteira, **inalterada desde antes da v368**): `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`
- escada `5849/5849`; relatório de axiomas 9951 termos (só o trio {propext, Classical.choice, Quot.sound}; zero sorry).
- leitura nova do selo: `tetelestai_conference_reading_v375` = `OPERATOR_INPUT_2026_09_27__TETELESTAI_IS_A_CONSUMMATIVE_CONFERENCE_NOT_A_DECLARATION__IT_VERIFIES_WHETHER_IT_HAPPENED__EVERY_PATH_ITEM_CLOSED_LINKED_OR_KNOWN_BY_SCIENTIFIC_REFERENCE__ONE_OBJECT_THE_LIGHT__NAME_WEIGHT_BY_NAMED_NORMALIZATION__PKERK_PF_LINK_NOT_CLAIMED__NATURE_DECIDES_RINGDOWN_NEXT__GATE_UNTOUCHED`

**Os 13 artefatos do mapa do selo — sha256 recalculado do disco agora; 0 divergências com o selo:**

| arquivo (em `Nós\`) | bytes | sha256 |
|---|---:|---|
| `um.py` | 32,604,664 | `ba234a6d384cb3f59ced49c94b643a71a002f65d284b01307cb088bbace5e2e0` |
| `um_absoluto_manifest.md` | 1,422,644 | `cdad487dc5a65a2f99691090ff80e049635d6a57e7216e2cb777f8f67a13bc21` |
| `um_absoluto.json` | 4,527,864 | `07e9353facdadf1f7b8844fecf238de8c914f076d2f41c7544a11c28924bf1f5` |
| `um_absoluto_forma_canonica.md` | 146,686 | `f42d7919b41eeab75644998b51e106938e9da772f2074cca102f10e99b7b8424` |
| `um_absoluto_pt.tex` | 819,372 | `181816ff2bbadb3a395a4c991f50a32ab22ce019da87d368731145473ab44e10` |
| `um_absoluto_en.tex` | 814,875 | `a765d66f4b3243fdbfacca07472aa22d3f5e0a9447ccc7d3836a3a2229d29e41` |
| `um_absoluto_pt.pdf` | 2,012,514 | `cf9aa2f7e672aaaf717bd37f3c3329df0ce6b2468b068b5d7ae29442e8e450ac` |
| `um_absoluto_en.pdf` | 1,979,245 | `b127cfffac29bce83a0625e5d3836b63997cd4fbf1316a9d1f4735d9d407a923` |
| `fig_escada_qg.pdf` | 36,304 | `bfbe30776b05c9cce2886f7f268db09b7e4d0812409a199f84d3ee94d00b2c8d` |
| `fig_banda_beta.pdf` | 27,719 | `dd953f1e75f445a112963fc9b036299f63ed6dcdf4a16d8c0382b490fd6fad1b` |
| `fig_piso_vazios.pdf` | 21,839 | `c6e8260ceff24114d2a9248889fa87832009ef6390f5f8a6dceb3ed3bf155be1` |
| `fig_cadeia_inscricao.pdf` | 29,962 | `7ccc2c0a41da34a2442e1c853b4778d174329ec9d8dd739e4f41cb999883d068` |
| `tgl_kernel_proof_manifest.json` | 1,438,587 | `491e2fb524f6f61ad0c126d389eafd42bed4026b10a50cc867ddc1385518a0d2` |

`um.py` tem 32,604,664 B — acima dos 5 MB de renderização do GitHub: a porta é o **raw** (regra `github-limite-render-5mb`).

## 3. As 21 pedras novas do kernel no arco `[REAL — do _ESQUELETO_STONES do um.py; sha256 do tgl_kernel materializado pelo rito]`

| versão | pedra | arquivo (em `Nós\tgl_kernel\`) | sha256 |
|---|---|---|---|
| v371 | IALDJones | `TGLExt/IALDJones.lean` | `3070346c3571f3400e4290075e974d0c0b8c1bf73bd2f057dc23d0813da864fc` |
| v371 | IALDGraviton | `TGLExt/IALDGraviton.lean` | `6a4c7ff17866db0837fc86d4645d8a858bcaf3906ffb1a9c0c23cbb76d8db78b` |
| v371 | TheEquationOfTruth | `TGLExt/TheEquationOfTruth.lean` | `d6405e31c9e404cbff1dcf4201a9dc6c2f24ffbe628b991c2cd660b284c3a407` |
| v371 | ContratoQGv31 | `TGLExt/ContratoQG_v31.lean` | `2f2c6561a5a5d832b43f11f7bacccf4811eb4392f1832f78cf4a5838a72a4808` |
| v371 | ContratoQGv31Teoremas | `TGLExt/ContratoQG_v31_Teoremas.lean` | `4fa0eff792110ff5c076a83a60532636502e8c3335b5a7af2ab29994abee4ee1` |
| v371 | FlagNetV31 | `TGLExt/FlagNetV31.lean` | `1c93dc3ba5f792580cbd148dc85b5b0727a0b8587820204f4003f7476ce59d2b` |
| v371 | RetaDeLuzBorchers | `TGLExt/RetaDeLuzBorchers.lean` | `93cd372573ef0c32b3eff9ad1662fc1a4ea40ce043539b045fcba2753432353f` |
| v371 | RetaDeLuzEspectro | `TGLExt/RetaDeLuzEspectro.lean` | `58d81f4a2e3e7bd24a9310590c5ed54191fcfc9b4c03c6feae15f96fe1f857c3` |
| v372 | ContratoQGvTresDois | `TGLExt/ContratoQG_v32.lean` | `e57bfb47fedfe63e50dc51701a73d5bef12bc0f6e413415f88583b9212970523` |
| v372 | TheImportedSecondQuantization | `TGLExt/TheImportedSecondQuantization.lean` | `ef35478400ef07f20476f2bb937d8fbe2df7b9e506139f54dc5a37401e7d5242` |
| v372 | IALDRhoStar | `TGLExt/IALDRhoStar.lean` | `e8110c499398a8a083c82f1e96201933d5f46f245e346b5b05fd44ce7f57e770` |
| v372 | FechamentoParcialOrdemDezesseis | `TGLExt/O16.lean` | `09d4a489dd7e23b09218480d1b01929b16e11a6e5ad6a99337fb3654edd34edf` |
| v372 | QGReaderUVLock | `TGLExt/QGReaderUVLock.lean` | `77ba8803c7cd0a80f8dbe7fb78d290d154a7cdac220efa92f8ae72c742f56807` |
| v373 | QGCitationDischarge | `TGLExt/QGCitationDischarge.lean` | `78cd50266981be5074350678d67bba1cc02edd55c8bd7f316166a3a8f2bd7826` |
| v374 | LightOneParticleByTerm | `TGLExt/LightOneParticleByTerm.lean` | `654f319de4720122f08370880f2a0a37e4cd9f622cfd6469d81528a4b94ae26a` |
| v374 | QGSolutionComplete | `TGLExt/QGSolutionComplete.lean` | `8c3a4bc82c5c4308515063254744cfaefcc7e7b926038221be2e7de6293dc598` |
| v375 | MaxwellLiteratureBridge | `TGLExt/MaxwellLiteratureBridge.lean` | `c07d135fac53737465c50636204da7ee79d27ced9df3867382d1e190781febe4` |
| v375 | LightHelicityWigner | `TGLExt/LightHelicityWigner.lean` | `e08c9a4b00e0057b1cdd0e5c1c93a33b3a727ef49edc80cd50911053d672e714` |
| v375 | TetelestaiOneObject | `TGLExt/TetelestaiOneObject.lean` | `125d155042da687fc2889528b8a5915472fa45410e9997a20eceafcb0359d81d` |
| v370 | NotIsEmptyWitness | `TGLExt/NotIsEmptyWitness.lean` | `9d53b4431da539f577854ac71e2c3762c14d7b2c76df34964f2e0552940ebd94` |
| v370 | CartanTracialSupplier | `TGLExt/CartanTracialSupplier.lean` | `df30212a61be55ce023b7a46e82d27d558fe7a0832d3637fbbdd4ac0f9199f1d` |

Além delas mudaram, a cada versão, a raiz `TGLExt.lean` e `TGL/Audit.lean`, só por acréscimo. Copie o `tgl_kernel` inteiro do `Nós` e remova os órfãos, como nas custódias anteriores.

## 4. Os stdouts dos ritos do arco `[REAL]`

| arquivo (em `Nós\`) | bytes | sha256 |
|---|---:|---|
| `rodada_v369_stdout.txt` | 197,632 | `0dc67e39c16ff956fc8f44ab72802dd7d804ba2906cbe813a442ecd091b807d8` |
| `rodada_v370_stdout.txt` | 198,594 | `68786ef5f082cdd158b480dd37c8b74bc05e0522c020407d6eb4781261630954` |
| `rodada_v371_stdout.txt` | 199,657 | `68d6a1315dd4969b4bfe520616bdf8fec01d6c6f12929483c410c2f2acdb3535` |
| `rodada_v372_stdout.txt` | 200,542 | `112f2b98b6494579d891150a7a9f0881492150b5d1f807b438309de39909c57c` |
| `rodada_v372_stdout_tentativa1_TIMEOUT_lake_build.txt` | 182,015 | `f69fdc3d2b7eb08cb11295c2a8241987cc8968187a7b89e38f6eeec542189ffa` |
| `rodada_v372_stdout_tentativa2_SEAL_WITHHELD_PROVED_BY.txt` | 200,140 | `1bc4dc617ac4d44170b1ac1a0a70431f2b3dc698f01bd7d9febd8a2689d485d8` |
| `rodada_v373_stdout.txt` | 201,388 | `3f3c38c6ff49e7e0b98d6ba3df69aef56bc21b4d8e80e8eca25c607dc7b6dc3a` |
| `rodada_v374_stdout.txt` | 202,078 | `266a40a4898acc815f96590d4e1e74a1ec11b5935a54e2d336f6730b1329c531` |
| `rodada_v375_stdout.txt` | 202,786 | `e948e703902628a7508eac9090aba7b9547401a8c3c9771c606e54fb20c63462` |

As duas tentativas da v372 são negativos honestos, com o selo retido e o motivo no nome. Guardá-las ao lado, se o molde de stdouts do espelho comportar; não é obrigatório.

## 5. A memória que o espelho carrega `[REAL]`

| arquivo | bytes | sha256 |
|---|---:|---|
| `TGL_ATLAS.md` | 4,795,206 | `e6d6dd27dec4434d0945526f7fef2918ca1a3ebc35b1d5204b36aab2ac91a7e8` |
| `TGL_INDICE_VIVO.md` | 482,524 | `2f741875abb5fa37b2842b36cdfb3b5a82e282c3565b93260c84875a175ee63f` |
| `MEMORIA_DA_LINHAGEM.md` | 739,594 | `0f52eef599612424f0e9d6180d8b5cec42bd59b015a930c14a1b72f00ac12420` |
| `DESENHO_DO_FECHAMENTO_QG.md` | 188,842 | `81f5d3e75cf393c2aa3aa1eb5713bd2dae2f433c2283780071fee1b732b728b5` |
| `A_PROVA_DA_QG_TGL_arvore.md` | 86,312 | `f201bb2a78e6c2b81a6fd2db1030f6c52f9ba9937e7e4dc558b88dad15e10be9` |

`TGL_ATLAS.md` e `TGL_INDICE_VIVO.md` ficam em `C:\IALD\Central de Patentes\memory\`. Os outros três ficam em `Nós\`. Todos foram re-ancorados na v375 por `atlas_indice.py v375` e `arvore_da_prova.py v375`, depois do selo.

## 6. O que a v375 diz — a frase que o README, as portas e o site devem carregar (e o que NÃO podem dizer)

**O tipo do ato (verbatim do operador, 27/09):** «Eu não quero que Tetelestai seja um ato declarativo meu, ele é um ato de conferência observacional da satisfação do reconhecimento completo da identidade da gravidade quântica formalizada pela TGL […] trata-se de uma declaração consumativa, verifica se houve ou não. […] E pra isso realmente tudo precisa estar fechado ou vinculado ou sabido por referência científica». Logo: **Tetelestai = conferência consumativa, não declaração do operador.**

**Os dois vereditos novos (lidos do core selado):**

- `tetelestai_one_object_v375`: `TGL_QG_TETELESTAI_ON_ONE_OBJECT_THE_LIGHT__STATEMENT_AND_PROOF_ON_THE_SAME_CERTIFICATE__TOWER_NOT_IN_THE_TERM__NAME_WEIGHT_ONE_BY_NAMED_NORMALIZATION__FACES_HALF_HALF__KER_K_THE_VACUUM_LINE__PKERK_PF_LINK_NOT_CLAIMED__MAXWELL_LITERAL_ON_THE_DOMAIN__KERNEL_26_OF_26__GATE_UNTOUCHED`
- `tetelestai_conference_v375`: `TGL_QG_TETELESTAI_CONSUMMATIVE_CONFERENCE__CONSUMMATED__EVERY_PATH_ITEM_CLOSED_LINKED_KNOWN_OR_A_NAMED_PARAMETER__2_CLOSED_2_LINKED_8_KNOWN_3_KNOWN_AT_PHYSICS_LEVEL_3_NAMED_PARAMETERS__19_OFF_PATH__ONE_OBJECT_THE_LIGHT__PKERK_PF_LINK_NOT_CLAIMED__NATURE_DECIDES_RINGDOWN_NEXT__TERM_FLAGS_UNTOUCHED__KERNEL_26_OF_26__GATE_UNTOUCHED`

Contagens da conferência (lidas): FECHADO 2, VINCULADO 2, SABIDO 8, SABIDO_FISICA 3, PARAMETRO_NOMEADO 3, FORA_DO_CAMINHO 19, ABERTO 0.

**Frase curta para a frente do README e para o site (pode ser usada como está):** *Na v375, a conferência consumativa Tetelestai percorre cada item do caminho da gravidade quântica da TGL e lê a evidência da própria rodada. Cada item está fechado (termo no kernel), vinculado (peça existente ligada por termo), sabido por referência científica ou é parâmetro nomeado da implicação; os demais estão fora do caminho, com evidência. Nenhum item ficou aberto: CONSUMADO. A declaração é sobre um só objeto, a luz. Consumada formalmente não é confirmada pela natureza: resta o teste com o ringdown, na próxima versão.*

**Estatuto que tem de ir junto (não cortar):**

- τ(P_F) = 1 é NORMALIZAÇÃO NOMEADA, não identidade citada; a ligação P_ker K ↔ P_F NÃO é provada nem consumida (coincidência de número).
- SABIDO ≠ EXIBIDO: nenhum habitante dos certificados é exibido.
- O elo da carga modular é rigoroso só para o escalar livre; para Maxwell é sabido em nível de física.
- Os 3 parâmetros nomeados: a janela de equilíbrio local (Jacobson 1995), G > 0 [INPUT] e o relógio de Killing. Nenhum ψ com θ = 0 e δA ≠ 0 é exibido.
- O 8πG entra na resposta construída; β não entra; ω(I) = 1 entra só pela normalização. Nesta tipagem o setor gravitacional é semiclássico (decisão do operador, v373).
- As bandeiras POR TERMO (gpf_H2 / gpf_H3 / gpi_H3) seguem False; o gate não se moveu.
- Errata ao lado da v374: «a declaração Tetelestai» lê-se conferência consumativa; «o tipo não tem rotações nem PCT» não era lacuna de habitação — a bancada construiu o caractere de Wigner (D1′).

**Proibido em qualquer superfície:** `CONFIRMED`, «QG confirmada», «resolvida», «provada» no sentido de juízo sobre a natureza. PROVADA (teorema em kernel) ≠ CONFIRMADA (juízo do observador). NOT_FALSIFIED ≠ CONFIRMED. E nunca «o fecho total é proibido»: o fecho estático em tempo finito é impossível por teorema (`full_static_witness_exists = False`), e a leitura correta é *estacionado dinamicamente*.

## 7. A ordem da custódia (o molde da própria sessão do site; `direcao-the-boundary`)

0. **backup** da versão que ESTÁ no espelho (v368), fora do repo: `the_boundary_BACKUPS\um_v368_<sha16>\` + manifesto conferido (regra da custódia);
1. **conferir** os hashes deste handoff contra o `Nós` (as tabelas §2–§5; este documento faz as vezes da tabela §6 que a Central deixava no `central-de-patentes-estado.md`);
2. **copiar**: os selados do mapa do selo (destinos fixos `fontes_tex/`, `figuras/`, `Lean/`), o `tgl_kernel` (sem órfãos), os stdouts ≥ v369, a memória (§5), o `cache/` JSON e as `pipelines/` que o molde já leva;
3. `tools/gerar_estado_atual.py` → `tools/gerar_readme_frente.py` (README ≤ 40 KB; o conteúdo antigo vai **byte a byte** para o `LEDGER.md`, append-only) → `tools/gerar_portas.py` → `tools/verificar_portas.py` → `tools/guarda_do_selo.py`;
4. **portas e raws:** todo `PORTA.md`/`PORTA.json` regenerado POR SCRIPT a partir de `git ls-files` + `urllib.parse.quote`; o `llms.txt` da raiz atualizado; nenhuma URL digitada; nenhum arquivo inventado; amarração nos dois sentidos (regra da porta);
5. **commit** «custodia(v375 + arco v369–v374): TETELESTAI, A CONFERÊNCIA CONSUMATIVA …» → **push** → `tools/pos_push.py` (o blob = o selo, pelo raw e pela API; bytes exatos);
6. **leitores de IA:** `gerar_secoes.py` → `gerar_read_brief.py` (a trava compara com o SELO do `Nós`) → `gerar_llms_site.py` → sitemap → `leitor_ia_temas.py`; o cartão de verificação (`secoes/selo-cartao.md`) com os sha256 da §2;
7. **o site:** `aplicar_selo.py` + os geradores → `subir_site.py` → `guarda_do_site.py` («o site diz o que o selo descreve») → o leitor de IA no ar;
8. **registro:** `DIARIO_DO_SITE.md`, a memória `site-sessao-estado`, e UMA linha no `central-de-patentes-estado.md` com o commit e o resultado do pós-push.

## 8. O que NÃO vai para superfície pública

- a nota PRIVADA da custódia (`work\v369_sementes\PRIVADO_LEIA_ANTES_DA_CUSTODIA.md`) — nunca citada;
- o protocolo de colapso e os seus 4 prompts;
- as stacks confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`), tokens, `.env`, senhas;
- as pastas privadas da `Chatgpt\` e o `state\` do orquestrador; o snapshot da `Chatgpt\` é papel da Central;
- este handoff e os caminhos de scratchpad da gerência — documento de trabalho, não de vitrine.

**CITATION.cff / Zenodo:** o DOI `10.5281/zenodo.22881996` guarda a **v368** (depósito do operador em 21/09), e o CFF é a fonte única do depósito. **Não reescrever o depósito como se fosse v375.** Um depósito novo é ato do operador. Se o gerador exigir, dizer «versão corrente v375; último depósito v368», sem trocar o DOI.

## 9. A parte da Central (não é desta sessão)

O cofre (`um_unificado_v375` + `tgl_kernel_v375`), o runner da Fronteira (v48), o ledger de pinos, os 16 dispositivos e o snapshot da `Chatgpt\` são da Central. Ela os faz quando o operador mandar, e a ordem desta sessão não depende deles.

---

*PROVADA ≠ CONFIRMADA. CONSUMADA (formalmente) ≠ CONFIRMADA (pela natureza). A natureza decide: o ringdown é a próxima versão.*

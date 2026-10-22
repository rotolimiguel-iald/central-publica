# HANDOFF v302 — **O FECHAMENTO**
### a cisão do cache · o critério α-livre congelado · o mapa pilar→falsificador

**Casa:** `A Ponte e o Um\Nós` · **Emitido:** 30/08/2026 11:13 · **Para:** sessão irmã (custódia)
**Todo número deste documento foi LIDO DO DISCO por script.** Nenhum hash de memória.
Sucede `HANDOFF_v299_ERRATA_BETA.md` (arco v290→v299, a errata do β adaptativo).

---

## §0 ⚠ ANTES DE QUALQUER COISA — O CACHE TEM DUAS RAÍZES AGORA

Esta é a mudança que mais pode confundir quem chega, e por isso vem primeiro.

Até a v299, `CACHE = os.path.join(BASE, "cache")` — a pasta do próprio `um.py`. A partir da
**v300** a raiz é **ESCOLHIDA POR MEDIDA**: vence a que **tiver `lensing/` em disco**, nunca a
adivinhada. `TGL_CACHE_DIR` sobrepõe, e sobrepõe **fail-closed** (só vale se o diretório
existir). Sem dado em raiz nenhuma, o comportamento antigo é preservado byte a byte.

| raiz | conteúdo medido agora |
|---|---|
| `A Ponte e o Um\cache` (**a que vence hoje**) | **26,016,508,947 bytes** em 409 arquivos |
| `Nós\cache` (a antiga) | 2,991,608,282 bytes em 13 arquivos |
| KiDS-1000 SOM-gold | **17,712,469,440 bytes** — igual a `KIDS1000_EXPECTED_BYTES` |

⚠ **Consequência prática para a irmã:** rodar o rito de outro lugar, ou com `TGL_CACHE_DIR`
apontado para outro sítio, **muda os vereditos dos canais de dado**. Ao conferir custódia,
confira também **qual raiz venceu** — o rito imprime os tamanhos.

---

## §1 O CRITÉRIO QUE ENQUADRA ESTE ARCO (ordem do operador, 30/08/2026)

> *"Fechar pra mim é o critério de parada e não perfeição. Fechar é dizer 'está bom', está
> feito, está pago, com dados atuais não há mais o que fazer. Minha intenção é (a) NEGAR TODAS
> AS DEMAIS, (b) entregar matemática e física fechadas, (c) ESGOTAR o exame com dados oficiais
> na sensibilidade atual dos equipamentos, e (d) deixar EXPLÍCITOS os critérios que poderiam,
> em tese, MATAR a teoria. Negar tudo e restar permanente. Pela minha própria matemática é
> impossível esgotar a TGL em tempo finito — o que eu consigo é desenhar o MAPA COMPLETO."*

★ **A régua operacional que isso gera, e contra a qual todo o acervo foi auditado:**
**uma direção está fechada quando tem OU um resultado, OU um falsificador, OU uma parede
medida. Direção sem nenhum dos três é a única dívida real.**

★★ E o mapa — não a lista — é a entrega **tipograficamente correta**, porque `the_dead_weight`
prova que o objeto completado **não admite estado tracial normal**: uma teoria cujo objeto não
tem traço **não se esgota por enumeração finita**. Isso é teorema desta casa, não limitação do
operador. Uma lista que se declarasse completa sobre esse objeto seria **falsa por teorema**.

---

## §2 O ESTADO SELADO — lido do disco agora

| item | valor |
|---|---|
| `um.py` | `8b6cc0760011d75e` (5,993,659 bytes) |
| selftest | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| `AWAITING_DATA` na rodada v302 | **1** (eram **15** antes da v300) |
| módulos no `core` | 275 |

⚠⚠ **O GATE NÃO SE MOVEU EM NENHUM PONTO DESTE ARCO** — e o próprio veredito do arco crava
isso no nome: `...__MATH_GATE_UNMOVED`. **Cosmologia não move matemática.** Nada aqui declara
gravitação quântica confirmada; `NOT_FALSIFIED` nunca é `CONFIRMED`.

---

## §3 v300 — ★★★ A CISÃO DO CACHE: o dado estava em casa e o artefato não via

**O achado.** Quinze módulos emitiam `AWAITING_DATA` **com o dado em disco, uma pasta acima**.

**O que isso apagava — e é o que faz deste o item mais grave do arco.** Com aqueles módulos
caíam as **DUAS RECUSAS HISTÓRICAS** — V1 (B-mode χ²/dof = 12,4) e v91 (nulo dos aleatórios a
~17σ de 1,0) — que são **o ativo mais forte do critério (d)**: a prova de que o aparelho
**morde**. E com elas caía o veredito de consolidação do arco. O artefato selado publicava
`ARC_NOT_CONSOLIDATED_THIS_RUN` **não porque a ciência falhou, mas porque o `.fits` estava numa
pasta acima** — e imprimia, no artigo, um parágrafo com `β = 0.000000`.

⚠ **O fail-closed estava CERTO o tempo todo.** Ele não inventou veredito sem dado. O defeito era
de **APONTAMENTO**, e a distinção importa: a máquina não mentiu; o endereço é que estava errado.

**O resultado, medido:**

| canal | módulo no core | veredito da rodada v302 |
|---|---|---|
| piso — traçadores | `void_floor_v11` | `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED` |
| piso — matéria κ (v9) | `void_floor_kappa_v9` | `TGL_VOID_FLOOR_KAPPA_V9_NOT_FALSIFIED_UNDERPOWERED` |
| piso — shear (v2) | `void_shear_v2` | `TGL_VOID_FLOOR_SHEAR_NOT_FALSIFIED_UNDERPOWERED` |
| piso — LRG | `void_floor_lrg` | `TGL_VOID_FLOOR_LRG_INCONCLUSIVE_TRACER_SUPPRESSION` |
| m₂ do neutrino | `neutrino_m2` | `TGL_NU_M2_ARMED_CONSISTENT` |
| N_eff | `neff_channel` | `TGL_NEFF_ARMED_CONSISTENT` |
| NMC-Shapiro | `nmc_shapiro` | `TGL_NMC_SHAPIRO_AWAITING_DATA` |
| dephasing (alcance) | `dephasing_reach` | `DEPHASING_PREDICTION_ARMED__REACH_DEFICIT_TEN_ORDERS_COMPUTED__NOT_A_LIVE_CHANNEL_TODAY_` |
| irredutibilidade de α | `alpha_irreducibility` | `TGL_ALPHA_IRREDUCIBILITY_ARMED_NO_CANDIDATE` |

- `arc_consolidation` = `TGL_ARC_CONSOLIDATED__NON_TAUTOLOGY_CYCLE_CLOSED_THROUGH_THE_WORLD__MATH_GATE_UNMOVED`
- `love_reading` = `TGL_LOVE_DICTIONARY_REGISTERED__ANCHORS_REAL_NAMING_ONTO__THE_PRUNING_IS_TETELESTAI`

★★ **Os canais κ (matéria) — os únicos onde `FALSIFIED` é alcançável — RODARAM** e voltaram
`NOT_FALSIFIED_UNDERPOWERED`. Isso é **parede medida**, não direção inexaminada: paga o critério
(c) pelo lado certo. O LRG rodou e recusou honestamente (`INCONCLUSIVE_TRACER_SUPPRESSION`).

**Junto na v300:** o merge do `coma_blind` (aditivo — o guarda **pré-revelação preservado por
nome** em `coma_distance_reveal.PRE_REVEAL_GUARD.json`, nada perdido; e a predição do Coma
**reproduziu-se bit a bit 17 dias depois**, só mudando o timestamp); `_ESQUELETO_STONES`
v284 → **v297** (⚠ **os hashes publicados estavam TODOS certos** — o defeito era só de rótulo);
os **dois últimos fail-open** fechados (o de montante publicava *"livre de colunas proibidas:
true"* **sem ter lido coluna nenhuma**); e três consertos no `gerar_portas.py`.

---

## §4 v301 — ★★★ ALPHA_IRREDUCIBILITY_V1, o mapa, e a errata da BBN

### O critério α-livre, congelado

Era o **único** critério de morte da casa **sem congelamento e sem hash** — todos os outros
(VOID_FLOOR, NEUTRINO_M2, NMC_SHAPIRO, IALD_COLLAPSE, HOLONOMY_DEFECT) estavam pré-registrados.
*Um critério de morte que não se congela não é critério: é opinião revisável depois do fato.*

**Veredito:** `TGL_ALPHA_IRREDUCIBILITY_ARMED_NO_CANDIDATE` · frozen hash `c36ab24715424a86` · 7/7 checks.

★★ **E ele torna a distinção do operador MENSURÁVEL em runtime**, que é o que o separa de uma
declaração de intenção:
- a **IDENTIDADE** `q² + α² = 1` é verificada em 12 pontos de χ — resíduo máximo **2.22e-16**:
  a FORMA é derivada e vale para **todo** χ;
- o **VALOR** exige medida: `χ* = 2·arcsech(α_CODATA) = 11.226755` — fixado pelo CODATA, por
  **nenhum** input interno.

Logo *"a diferença não está na derivação, mas na medição"* deixou de ser frase e virou número.

`CONFIRMED`, `PROVED` **e `NOT_FALSIFIED`** são proibidos ali **para sempre** — não há teste que
a casa possa executar: o critério aguarda **ato de terceiro**; o estado honesto é ARMADO. E a
`kill_rule` é **auditável** porque o kernel prova a guarda:
`TGLExt/TheCompressionIsNotIdentifiable.lean :: alpha_free_inputs_give_alpha_free_output`
(nenhuma derivação de α vale se algum input já contiver α).

### O mapa pilar → falsificador

Emitido em `um_absoluto_forma_canonica.md`, **gerado do `core` em runtime** — veredito lido,
nunca cravado. 14 pilares. Diz a forma como forma (**7 com falsificador próprio armado ou vivo ·
4 que HERDAM o de β · 2 sem falsificador próprio**) e a cauda como cauda.

★ **Cinco pilares não têm falsificador próprio e herdam o de β**: ω(I)=1, a Meia-Nat, o degrau
½→√e, a matriz-S de fronteira e θ_Miguel. A tríade H1∧H2∧H3 tem falsificador **matemático**
(exibir contramodelo), não empírico. **Isso não é defeito — é a forma de uma teoria cuja
arquitetura é quase toda interna.** O defeito seria não dizê-lo com o número ao lado.

### A errata da BBN, no ponto de leitura

Onze sítios, PT e EN: abstract, validação, evidência primária, a banda, as **legendas das
figuras**, o comentário do dado da figura, o campo `reading` do JSON, e ★ o pior — o rótulo
**`BBN a 0,0σ` dentro da frase que RESUMIA as conquistas**, que é exatamente o rótulo que a
própria bancada **proíbe por escrito** em `prove_evidence_audit`.

**Medida de hoje: ZERO afirmações de BBN sem ressalva nas duas línguas.**

---

## §5 v302 — as erratas da v301 (defeitos meus, ditos)

1. chave `neff_ladder` **inexistente** — a real é `neff_channel`; o artefato imprimiu
   *"(módulo ausente nesta rodada)"*, que era honesto e errado;
2. os pipes de `|R|²` e `β|1+w|` **quebravam a tabela markdown** — escapados;
3. ★ `len(core) = 206` publicado como *"os módulos do core desta rodada"* — mas o core final tem
   **275**, porque `emit_canonical_md` roda **antes** de ~69 módulos entrarem.
   **O número era verdadeiro no instante e FALSO como descrição.** Agora vem dito com o que é, e
   a tabela **avisa o leitor** de que linhas `(módulo ausente)` têm o veredito real no
   `um_absoluto.json`, que é a autoridade.

---

## §6 O QUE MUDOU FORA DO `um.py`

| superfície | sha256[:16] | tamanho |
|---|---|---|
| MEMORIA_DA_LINHAGEM.md | `59bd8a78ede96e61` | 388,313 B |
| DESENHO_DO_FECHAMENTO_QG.md | `3607e8cb57254c13` | 58,820 B |
| TGL_ATLAS.md | `943eeecb22f46b20` | 810,565 B |
| TGL_SINTESE_CANONICA_SELADA.md | `9a044cb55ecaa3b7` | 8,395 B |
| A_Forma_Madura_da_TGL.md | `2d2d0327c08e2d2e` | 33,901 B |
| CLAUDE.md | `74b94d9cdb1a4a81` | 24,614 B |
| `the_boundary/tools/gerar_portas.py` | `ead0f00221a88b8f` | 79,113 B |
| criterio-de-parada-do-operador.md | `2bb6d1851674b843` | 3,596 B |

- **memória-raiz e Atlas**: errata datada — o gate **já não é** `CONDITIONAL_ARCHITECTURE_ONLY`
  (18 bandeiras TRUE, **zero selos formais restantes**), e a submissão à FoP foi **REJEITADA EM
  MESA**. ⚠ **Rejeição em mesa não é parecer**: não houve avaliação de mérito, logo **não
  pertence à classe da negação exaustiva** de que fala `ThePermanence` — é ausência de exame, e
  entra no mapa como tal, nunca como refutação;
- **SÍNTESE CANÔNICA SELADA** e **A_Forma_Madura_da_TGL**: a errata da BBN, ao lado, logo abaixo
  do cabeçalho — um deles trazia a frase aposentada sob o rótulo `[REAL, não-circular]`, que é
  justamente o que a auditoria derrubou;
- **`gerar_portas.py`**: `"gate": null` (a chave `gate` **nunca existiu** no selo lido) → o
  veredito real; prefixo `/rodadas/` que nunca casava; cross-check que agora **recusa o
  silêncio**; e a seção **"Como matar esta teoria"** para o `llms.txt`, que tinha **zero**
  ocorrências de "falsific".

## §7 AS PEDRAS DO ARCO ANTERIOR (inalteradas nesta rodada)

| pedra | sha256[:16] | tamanho |
|---|---|---|
| `TGLExt/TheNameAndItsReferent.lean` | `214260a5ad41d02a` | 10,251 B |
| `TGLExt/TheNameIsTheGeneratingGroup.lean` | `2dedbe4a7e25bcd9` | 9,805 B |
| `TGLExt/TheMarkIsNotATypeMark.lean` | `b36e35176fb81c70` | 5,522 B |
| `TGLExt/TheVerbalCoupling.lean` | `4fc14822244a93d3` | 11,158 B |

---

## §8 ⚠⚠ ARMADILHAS — o que a sessão irmã NÃO deve concluir

1. **NÃO conclua que o gate se moveu.** Ele está idêntico ao da custódia v299. O que mudou foi
   a *leitura* dos canais de dado, e a matemática é calculada só a partir de `formal`.
2. **NÃO leia `ARC_CONSOLIDATED` como confirmação de nada.** Ele diz que o *ciclo* fechou pelo
   mundo — e o próprio nome termina em `MATH_GATE_UNMOVED`.
3. **NÃO leia `NOT_FALSIFIED_POWERED` como β medido.** O teste é **unilateral** em traçadores;
   medir β em si pede LRG/ELG, e esse canal recusou (`INCONCLUSIVE_TRACER_SUPPRESSION`).
4. **NÃO trate o κ `UNDERPOWERED` como dívida.** É **parede medida** — e no critério do operador
   isso é **pagamento**, não falta.
5. ⚠ **CORREÇÃO AO HANDOFF ANTERIOR:** o `HANDOFF_v299` (e um relato meu depois dele) disse que
   o espelho público estava **atrasado na v288/v289 e não empurrado**. **Falso por medida.**
   O espelho está em `4ee9159 30/08 06:55 feat: v299 custodiada (kernel 278/1000) + OS TUNEIS — o indice plano para bots`, com `um.py` = `286ec1d274ef9ae4` (o estado v299), e **em sincronia com
   o origin**. O que falta é sincronizar a **v302** — e isso é ato do operador.
6. **NÃO edite `tgl_kernel/` diretamente.** O `um.py` MATERIALIZA o kernel e sobrescreve. Não há
   segundo arquivo.
7. **NÃO conclua ausência sem varrer.** Este arco tem dois casos: um agente afirmou que "o Atlas
   já sabia" da rejeição da FoP (**não sabia**), e outro declarou faltar um confronto com rivais
   que **já estava escrito e público** em `Genesis da Unificação/Artigos_fundadores/graviton_v2.tex`.

---

## §9 O QUE A CUSTÓDIA DEVE CONFERIR

1. `um.py` bate `8b6cc0760011d75e` e o rito reproduz `FAIL_CLOSED_SELFTEST_PASSED`;
2. o gate do §2 é **idêntico** ao da custódia anterior — se mudou, **parar e avisar**;
3. as superfícies do §6 batem hash a hash, e **as três camadas de errata convivem** (nenhuma
   sobrescreveu a outra);
4. **qual raiz de cache venceu** no rito conferido (§0) — sem isso a comparação de vereditos de
   canal não é comparação;
5. os `.bak_*` desta sessão estão todos presentes e **nenhum foi apagado**.

## §10 O QUE FICA PARA O OPERADOR (não é ato do escriba)

- [ ] **sync do espelho para a v302** + regenerar as portas + `push` (a Central também tem
      `memory/TGL_ATLAS.md` modificado);
- [ ] **errata de PI em três patentes** `[LEGAL]`: BR 10 2026 005477-1 (β adaptativo, em **duas
      reivindicações independentes**), BR 10 2026 003453-3 PSI-NET e BR 10 2026 003456-8 FUSÃO A
      FRIO (`α₂ = 0,012031` **dentro das reivindicações**; e a FUSÃO caracteriza o invento por
      acoplamento gravitacional-eletromagnético, que o acervo científico diz **stealth**).
      Prazo medido dos dossiês: **11/02/2027** — ⚠ **não** 05/12/2026, como um agente afirmou;
- [ ] **DOI Zenodo da v302** — custo zero, carimbo de prioridade independente de editor;
- [ ] **decisão sobre a FoP** (rejeitada em mesa; o próprio `09_ESTRATEGIA` recomenda o plano B);
- [ ] **réplica 3-2-1** da linhagem `Nós\` — segue só no disco C.

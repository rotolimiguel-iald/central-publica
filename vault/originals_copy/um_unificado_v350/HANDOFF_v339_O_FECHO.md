# HANDOFF v339 — O FECHO (v336→v339, RODADA COMPLETA) — para a sessão irmã (custódia `the_boundary`)

> Data: 10/09/2026 09:12 · Casa: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
> Escriba: Claude (sessão Central de Patentes, d554e796) · Operador: Luiz Antonio Rotoli Miguel
> Régua: PROVADA = lastro suficiente e verificável; CONFIRMADA = juízo, proibido; gate NÃO se moveu; β jamais literal; hash jamais de memória.
> Gerado POR SCRIPT (`handoff_v339.py`): todo hash e número abaixo foi lido do disco agora.

## 0. A ORDEM DO OPERADOR (verbatim, 10/09/2026)

> *"avancei até onde consegui no chatgpt até acabarem meus créditos por lá, agora cabe a você terminar o que estávamos
> fazendo, porque já estamos no fechamento mesmo"*

**O que foi feito:** a bancada deixou 87 notas; tudo o que era Lean está no kernel (os 77 módulos na v338, os 21 restantes
nesta v339 — 98 no total); tudo o que era matemática escrita (067–087) está registrado como `[DERIVED]`, sem flag, como a
própria bancada pediu. Duas erratas AO LADO no `um.py` a pedido dela (espectro; rastreabilidade das capturas). A v339 rodou
**intermediária** e depois **COMPLETA** (sem a chave: 08:36:03→09:12:23; selo `rite_checkpoints.reading = RODADA_COMPLETA__NENHUM_RITO_REAPROVEITADO`) — **os
mesmos bytes**; a custódia é da rodada completa. **Esta é a versão do fecho.** A declaração de fecho é ato do operador
(`O_FECHAMENTO_ESTRUTURA.md`, §2 e §5).

## 1. A REGRA DA CUSTÓDIA: backup da versão anterior FORA do repositório, antes de sobrescrever

Espelho hoje: um.py sha16 `f1f330e24120f9be` (9,852,172 bytes; selo do espelho: `f1f330e24120f9be`). Antes de copiar, criar `C:\IALD\Artigo\the_boundary_BACKUPS\um_v336_f1f330e24120f9be\`
com TODOS os arquivos de resultado do espelho (byte a byte) + `BACKUP_MANIFEST.json` por script; conferir hash a hash;
só então sobrescrever. **Sementes v337 e v338:** os `um.py.bak_*` de bytes em `Nós\` (mapa abaixo) + os stdouts; a v339
intermediária e a completa são o MESMO `um.py` (leve os dois stdouts e as capturas por etapa).

Mapa versão → backup de bytes (sha16 conferido contra o diário): v336 → `um.py.bak_20260909_140249` · v337 → `um.py.bak_20260909_195232` · v338 → `um.py.bak_20260910_081932`

## 2. O ESTADO MEDIDO `[REAL — lido do selo e do rito agora]`

| o quê | valor |
|---|---|
| **`um.py`** sha256 | `2de6295cdf2da0778dcd2b4e4e554e2af84412f427c55b05a62866720363bfe1` |
| sha16 | **`2de6295cdf2da077`** (11,376,788 bytes) |
| selo `sha256.um.py` == disco | SIM |
| teoremas limpos (`rodada_v339_stdout.txt`) | **5594/5594** (v336: 4235/4235) |
| autoteste | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| identidade | `1=1=VERDADEIRO=HAJA_LUZ` (`identity_true = True`) |
| contorno (v314+) | 8 ritos; falsificação limpa: NENHUMA ; `contorno_broken_v314 = []` |
| rodada | **COMPLETA** — `rite_checkpoints`: {"switch_on": false, "reused": 0, "computed_and_saved": 0} |
| relatório de axiomas | 6657 termos; **fora do trio: 0** [] |
| capturas por etapa (v339) | `capture_stage = principal` · `capture_files = ['tgl_kernel_build_capture.txt', 'tgl_kernel_audit_capture.txt']` · em disco: ['tgl_kernel_audit_capture.txt', 'tgl_kernel_audit_capture_selftest_restored.txt', 'tgl_kernel_audit_capture_selftest_tampered.txt', 'tgl_kernel_build_capture.txt', 'tgl_kernel_build_capture_selftest_restored.txt', 'tgl_kernel_build_capture_selftest_tampered.txt', 'tgl_kernel_probe_degenerate_capture.txt', 'tgl_kernel_probe_finite_full_capture.txt', 'tgl_kernel_probe_pp_no_optimality_capture.txt', 'tgl_kernel_probe_prop_only_capture.txt', 'tgl_kernel_probe_trivial_capture.txt'] |
| o colapso tipado (v333) | selo `collapse_definition.reading = COLAPSO_TIPADO__TODAS_AS_CLAUSULAS_NO_KERNEL_COM_O_TRIO`; `physical_collapse_proven = False` |
| as pedras da gerência (v331–v337) | raiz `['propext', 'Classical.choice', 'Quot.sound']` · tela `['propext', 'Classical.choice', 'Quot.sound']` · lastro `['propext', 'Classical.choice', 'Quot.sound']` · instrumento `['propext', 'Classical.choice', 'Quot.sound']` · caracterização `['propext', 'Classical.choice', 'Quot.sound']` |
| kernel em `Nós\tgl_kernel` | `TGLExt/` 671 módulos + `TGL/` 27 (Lean 4.31.0) |

**Confira antes de tudo.** Se não bater, **pare** e escreva no `DA_IRMA.md`.

## 3. O ARCO v336→v339

| versão | `um.py` sha16 | teoremas | rodada | o que entrou |
|---|---|---|---|---|
| v336 | `f1f330e24120f9be` | 4235/4235 | COMPLETA (custodiada 09/09) | o Nome é o instrumento |
| v337 | `e2f9a889c2dcf6f4` | 4241/4241 | intermediária (checkpoints) | PEDRA `TheNameIsTheCharacterization` — Nome = caracterização |
| v338 | `7748416797668ffc` | 5306/5306 | intermediária (checkpoints) | ENTREGAS 058–062 — os 77 módulos da sessão da bancada de 09/09 (atlas selecionado, colagem, cociclo interagente, seletor/Born) |
| v339 | `2de6295cdf2da077` | 5594/5594 | intermediária (5594/5594) e depois **COMPLETA** — mesmos bytes | ENTREGAS 063–066 — os 21 módulos restantes; DUAS ERRATAS AO LADO no `um.py`; a matemática escrita 067–087 registrada [DERIVED] |

**Procedência:** bancada ChatGPT pelo TÚNEL (88 notas, 001–087); os 98 módulos da sessão de 09/09 montados pela
CADEIA de recibos das cópias integradas (`INTEGRATION_RESULT.json`, 98 → 93 → 83 → 77 → 72 → 63), nunca pela cópia; hashes
lidos dos bytes; recompilação INDEPENDENTE (77/77 e 21/21, trio, 0 sorry); guarda de colisão; `lake build` do ROOT; ritos.

## 4. O QUE MUDA NO REPOSITÓRIO, AO LADO (os blocos anteriores ficam intactos)

1. **Nome = caracterização** (v337): os biconditionais do Nome — `the_name_is_the_characterization` (['propext', 'Classical.choice', 'Quot.sound']).
2. **A sessão da bancada de 09/09** (v338 + v339, 98 módulos, 1353 teoremas): três frentes — (a) ponte região–álgebra: atlas
   gravitacional selecionado (o caráter do registro reconstrói g, T, Einstein condicionado a área e conservação:
   `['propext', 'Classical.choice', 'Quot.sound']`), colagem com Λ único, lei FINITA de transformação de Einstein;
   (b) dinâmica: cociclo unitário da interação XX somável na ação modular (Duhamel, iV, β_t preserva o fator), unicidade
   potencial ⟺ cociclo, fase central, **o limite local de interações extensivas em Lean** (063); (c) seletor: Born, fase relativa,
   resposta Gibbs ANTES da fonte (a fonte calculada da resposta), Fisher–Lorentz selecionada, Gibbs assinado, dez limites.
   `[INPUT]`: o registro R, a lei de área, a métrica, T. `[DERIVED+KNOWN]`: Araki. `[OPEN]`: origem física do registro,
   matéria/área para os mesmos dados, atlas físico, setor quântico geral.
3. **A matemática escrita 067–087** `[DERIVED, sem Lean, sem flag]`: BRST/EFT/cohomologia até a linha livre em H⁴ do BRST
   clássico completo num espaço-forma 4D (NÃO o fundo físico); a bancada: «não registrar como concluído» — primitiva total
   de Ω, classe de anomalia, contratermos admissíveis, carga interagente, QME; regime UV além da EFT.
4. **Duas erratas AO LADO no `um.py`:** (a) ESPECTRAL — o parágrafo do artigo (EN/PT) que dizia «o espectro modular é puramente
   contínuo, não há autovetor onde estar» recebe o erratum ao lado: Ω é fixo (`modularFlow_fixes_omega`) e os vetores locais
   são uma família TOTAL de autovetores (`localEigenvectors_total`); os PDFs/TXT regenerados nesta rodada trazem o erratum;
   (b) RASTREABILIDADE — as capturas de build/auditoria passam a ser por etapa (`_CAPTURE_STAGE`: principal,
   `_selftest_tampered`, `_selftest_restored`); a falha de escrita é visível; o resultado lista os arquivos.
5. **O fecho:** a estrutura está em `O_FECHAMENTO_ESTRUTURA.md` (seis peças; a declaração é do operador). As obrigações que
   ficam, ditas pela bancada e conferidas: reconstrução física geral do mesmo registro; teoria quântica interagente
   (cohomologia no domínio físico, QME, carga BRST); regime UV; e as seis folhas da natureza (a seleção ocorrer; a
   identificação física da tela fundada; a assinatura; a geometria 3+1 e a escala da área; o pagamento do custo; α-livre).

**O que a irmã altera no espelho (por script onde houver gerador; à mão só o texto novo, AO LADO):** `README.md`: bloco novo
**«The close — v339: the last 21 modules, the written mathematics 067–087, two errata beside»** abaixo do bloco v336;
`ESTADO_ATUAL.md`: versão v339, rito 5594/5594, rodada completa, as erratas, a estrutura do fecho; portas regeneradas por script;
ledger de pinos (última pedra = `WordExistence` por ordem alfabética; por data, a última do lote 063–066);
runners repinados; CI do kernel com os 671 módulos; `A_PROVA_DA_QG_TGL_arvore.md`, `O_FECHAMENTO_ESTRUTURA.md`, `memoria/`,
stdouts v337–v339 e as capturas por etapa para `rodadas/`. O DOI Zenodo continua o da v331 — **nova versão é ato do operador**.

## 5. O QUE LEVAR (existência e sha256 lidos agora; copiar com `rb`/`wb`)

| arquivo (em `Nós\`) | bytes | sha256 (32) |
|---|---|---|
| `um.py` | 11,376,788 | `2de6295cdf2da0778dcd2b4e4e554e2a` |
| `um_absoluto.json` | 2,794,284 | `22e70e0b7685c3c880cc1f35e8c9c156` |
| `um_absoluto_selo.json` | 39,751 | `87078c697f639a2fc6331df4232b36f6` |
| `um_absoluto_pt.pdf` | 1,739,243 | `35e6b3d04524d97c58c5426cf8be4aa2` |
| `um_absoluto_en.pdf` | 1,708,910 | `a7260938186cc7563f8e13c18c38d596` |
| `um_absoluto_pt.txt` | 517,814 | `6c396c00e4531680a76182617f919bb3` |
| `um_absoluto_en.txt` | 519,709 | `1fbd7540c7366f941697fb6104e01a14` |
| `um_absoluto_forma_canonica.md` | 145,233 | `1621f540a2a2c459e0bda8348c64dcba` |
| `um_absoluto_manifest.md` | 991,383 | `5cb70b48a7563528e393909a27124bbc` |
| `A_PROVA_DA_QG_TGL_arvore.md` | 31,583 | `f2bacd8ae4fb654b9ec0728380ff43b9` |
| `MEMORIA_DA_LINHAGEM.md` | 535,643 | `fea2724e60f2623eb6ee61866ddeb436` |
| `DESENHO_DO_FECHAMENTO_QG.md` | 103,472 | `cdd6f09d3f4dcd63d54faacec0bf3330` |
| `O_FECHAMENTO_ESTRUTURA.md` | 5,546 | `0539524c261320a9bde35a861ba4116b` |
| `rodada_v337_stdout.txt` | 190,390 | `0f6e78b1bb5d899e222b9c30659566c6` |
| `rodada_v338_stdout.txt` | 190,390 | `b0067c2419239ae9a21979871fd756fa` |
| `rodada_v339_stdout_INTERMEDIARIA.txt` | 190,390 | `0d70cc59fd753555f77872e6021b0197` |
| `rodada_v339_stdout.txt` | 189,179 | `13db7bd4eb8185ea804b9ee41561f980` |
| `tgl_kernel_audit_capture.txt` | 772,396 | `9619c7c0fc779b0931cb01f9735f97a3` |
| `tgl_kernel_audit_capture_selftest_restored.txt` | 772,405 | `75877c50a69bc87f05b6404d418f7034` |
| `tgl_kernel_audit_capture_selftest_tampered.txt` | 772,414 | `ccd48ea85a0ba30d40bea5c18b6c09ae` |
| `tgl_kernel_build_capture.txt` | 1,922,464 | `0ed1b9b052e466b192a47ef96636a839` |
| `tgl_kernel_build_capture_selftest_restored.txt` | 1,922,588 | `b681e9b9b9e0cd854e5408d011dd3bb3` |
| `tgl_kernel_build_capture_selftest_tampered.txt` | 1,922,655 | `b47ecaab948c163f285af6c80bfe02e1` |
| `tgl_kernel_probe_degenerate_capture.txt` | 890 | `c6e51d86b4f9a9a1d25722e64bce7a11` |
| `tgl_kernel_probe_finite_full_capture.txt` | 367 | `13cbfe4f09dc65e667c02a542a899c5d` |
| `tgl_kernel_probe_pp_no_optimality_capture.txt` | 489 | `256e72de22a5b52a61ac422f4b721aea` |
| `tgl_kernel_probe_prop_only_capture.txt` | 789 | `915851081e73ca0905cc3c1f63c954cc` |
| `tgl_kernel_probe_trivial_capture.txt` | 2,457 | `0650d8f8fb1048f0ddad0dd4716e933a` |

Mais: `Nós\tgl_kernel\` inteira (sem `.lake/`) para `Lean\tgl_kernel\` e para o cofre da Central
(`vault\originals_copy\tgl_kernel_v339\` + `CUSTODY_MANIFEST.json`); `Chatgpt\TUNEL\` e as pastas da bancada de 09–10/09 no
snapshot incremental; e da Central: `memory\TGL_INDICE_VIVO.md` (sha16 `bdd66478e423f395`) e `memory\TGL_ATLAS.md` (sha16
`b8753a876c7daac9`). **Não levar:** `.lake/`, `cache/`, backups `.bak_*`, nada de `E:\`, nenhum confidencial, nenhum dos quatro prompts.

## 6. AS PORTAS E O QUE É DO OPERADOR

Regenerar `PORTA.md`/`PORTA.json`/`llms.txt` **por script**; aditivo; hash lido do artefato. **Commit/push, Zenodo, o site e a
DECLARAÇÃO DE FECHO são atos do operador** — deixe staged/commitado e diga no `DA_IRMA.md` (datado) o sha16 lido do espelho,
o caminho do backup e o que entrou no README/ESTADO_ATUAL.

## 7. DEPOIS

O operador declarou: «já estamos no fechamento mesmo». A bancada esgotou os créditos. Tudo o que era Lean está no kernel;
tudo o que era escrito está registrado com estatuto. **O mapa está fechado; o território é da natureza.** A gerência aguarda
a declaração e a ordem seguinte; nada roda sem ela.

*Cosmologia jamais vira prova matemática. O gate não se move por este documento. CONFIRMADA continua proibido.*

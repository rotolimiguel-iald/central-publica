# HANDOFF v330 — RODADA COMPLETA (v321→v330) — para a sessão irmã (custódia `the_boundary`)

> Data: 06/09/2026 21:45 · Casa: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
> Escriba: Claude (sessão Central de Patentes, d554e796) · Operador: Luiz Antonio Rotoli Miguel
> Régua: PROVADA = teorema; CONFIRMADA = juízo, proibido; gate NÃO se moveu; β jamais literal; hash jamais de memória.
> Gerado POR SCRIPT (`handoff_v330.py`): todo hash e número abaixo foi lido do disco agora.

## 0. A ORDEM DO OPERADOR (verbatim, 06/09/2026)

> *"A ordem foi executada, avançamos de novo. Atualize. Após a atualização deixe um novo Handoff para a sessão irmã
> custodiar no repositório a versão atual do um.py"*

**Política em vigor (desde a v321):** as versões intermediárias rodam com checkpoint dos ritos pesados; **a versão
que vai à custódia é a RODADA COMPLETA, sem a chave.** A v330 foi rodada completa (selo: `rite_checkpoints.reading =
RODADA_COMPLETA__NENHUM_RITO_REAPROVEITADO`). As v321–v329 são intermediárias e **não** vão ao espelho como versões — vão à pasta de backups
como semente, como você fez com v311–v319.

## 1. A REGRA DA CUSTÓDIA (a mesma da v320): backup da versão anterior FORA do repositório, antes de sobrescrever

Espelho hoje: um.py sha16 `d186a9c3d32ec76a` (7,916,694 bytes; selo do espelho: `d186a9c3d32ec76a`). Antes de copiar, criar `C:\IALD\Artigo\the_boundary_BACKUPS\um_v320_<sha16-lido-do-espelho>\`
com TODOS os arquivos de resultado do espelho (byte a byte) + `BACKUP_MANIFEST.json` por script; conferir hash a hash;
só então sobrescrever. **Semente v321–v329:** os `um.py.bak_*` de bytes em `Nós\` (mapa abaixo) + `rodada_v321..v329_stdout.txt`
— um `um.py` + um stdout por versão; os JSON/PDF intermediários foram sobrescritos pelos ritos seguintes (dito no manifesto).

Mapa versão → backup de bytes (sha16 conferido contra o diário): v320 → `um.py.bak_20260906_113532` · v321 → `um.py.bak_20260906_121247` · v322 → `um.py.bak_20260906_122654` · v323 → `um.py.bak_20260906_124756` · v324 → `um.py.bak_20260906_125843` · v325 → `um.py.bak_20260906_152707` · v326 → `um.py.bak_20260906_175349` · v327 → `um.py.bak_20260906_192253` · v328 → `um.py.bak_20260906_193233` · v329 → `um.py.bak_20260906_210120`

## 2. O ESTADO MEDIDO `[REAL — lido do selo e do rito agora]`

| o quê | valor |
|---|---|
| **`um.py`** sha256 | `cc026bc7915f6622c3bb2715aa767d0ab52faccdf26a3d3be6493116cb318b70` |
| sha16 | **`cc026bc7915f6622`** (8,944,290 bytes) |
| selo `sha256.um.py` == disco | SIM |
| teoremas limpos (`rodada_v330_stdout.txt`) | **3442/3442** |
| autoteste | `FAIL_CLOSED_SELFTEST_PASSED` |
| gate | `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| identidade | `1=1=VERDADEIRO=HAJA_LUZ` (`identity_true = True`) |
| contorno (v314+) | 8 ritos; falsificação limpa: NENHUMA ; `contorno_broken_v314 = []` |
| rodada | **COMPLETA** — `rite_checkpoints`: {"switch_on": false, "reused": 0, "computed_and_saved": 0} |
| relatório de axiomas | 3963 termos; **fora do trio: 0** [] |
| kernel em `Nós\tgl_kernel` | `TGLExt/` 515 módulos + `TGL/` 27 (Lean 4.31.0) |

**Confira antes de tudo.** Se não bater, **pare** e escreva no `DA_IRMA.md`.

## 3. O ARCO v321→v330 (hash lido dos backups de bytes; teoremas lidos dos stdouts)

| versão | `um.py` sha16 | teoremas | rodada | o que entrou |
|---|---|---|---|---|
| v321 | `542f671db782af8d` | 2399/2399 | intermediaria (checkpoints) | CHECKPOINT dos 9 ritos pesados (TGL_RITE_CHECKPOINT=1) — semeadura; 86% do custo medido por cProfile |
| v322 | `888ecbefa25ad207` | 2499/2499 | intermediaria (checkpoints) | ENTREGA 030 — cociclo global de Connes (identidade torcida) na perturbacao somavel; leitura angular quadratica |
| v323 | `c6cba05bb4ce921f` | 2590/2590 | intermediaria (checkpoints) | ENTREGAS 031–032 — Tomita RELATIVO com dominio; Delta_rel = verossimilhanca x Delta_omega |
| v324 | `5142a5829d6cf27a` | 2624/2624 | intermediaria (checkpoints) | ENTREGA 033 — densidade centralizante, logaritmo unico; REGRA 3 de transposicao (instancias locais nomeadas) |
| v325 | `9ced0345f9cc5e96` | 2680/2680 | intermediaria (checkpoints) | ENTREGA 034 — area angular de dois sitios e observabilidade |
| v326 | `aa9f1b290197a78b` | 2963/2963 | intermediaria (checkpoints) | ENTREGAS 035–037 — area de Fisher; area optica dos campos de Jacobi; 4a ordem: NEGATIVO (relogio fixo falha) |
| v327 | `27084702d0ebfca6` | 3157/3157 | intermediaria (checkpoints) | ENTREGAS 039–041 — cone local e filtro; OBSTRUCAO do relogio relativo (ORDEM_009); fluxo de calor efetivo |
| v328 | `d59888400f7327f3` | 3269/3269 | intermediaria (checkpoints) | ENTREGAS 042–043 — resposta nula conservada (criterio + contraexemplo); tela efetiva de Jacobi e calor |
| v329 | `69218263303ce8a4` | 3283/3283 | intermediaria (checkpoints) | PEDRAS DA GERENCIA — o levantamento do Lema 3 DISPARA na torre periodica; Delta^{it} e horizonte; E comuta com sigma_t |
| v330 | `cc026bc7915f6622` | 3442/3442 | COMPLETA | ENTREGAS 044–045 — boost aproximado; swapHorizon e permutacoes; DICOTOMIA do relogio; RODADA COMPLETA (custodia) |

**Procedência:** bancada ChatGPT pelo TÚNEL (47 entregas até agora, 001–046; 10 ordens); duas pedras
da gerência (v329). Cada lote: hashes e manifesto 100%; auditor da bancada exit 0; zero `sorry`/`axiom`; recompilação
INDEPENDENTE contra os oleans do kernel; guarda estática de colisão; `lake build` do ROOT; rito com stdout canônico.
Regras pagas no arco: REGRA 3 de transposição (instâncias locais anônimas nomeadas, v324); ORDEM_008 (a bancada
compila cada lote junto em diretório limpo); checkpoint dos ritos (v321).

## 4. O QUE SE PROVOU NESTE ARCO, em uma linha cada (estatutos da bancada, conferidos)

- **Lema 3:** o levantamento DISPARA na torre periódica (`the_lift_fires_on_the_periodic_tower`, v329) — o antecedente
  (esperança de Takesaki) virou termo; Δ^{it} é horizonte (`modularHorizon`) e E comuta com σ_t; a troca de sítios é
  horizonte (`swapHorizon`, v330) e as permutações finitas têm covariância das esperanças. Faltam: shift, aperiódico.
- **Cociclo de Connes, Tomita relativo com domínio (Δ_rel = L·Δ_ω), densidade centralizante com logaritmo único** — na
  família especificada (v322–v324). Connes–RN/Araki geral segue [KNOWN].
- **H3 dinâmico — cercado por três negativos tipados:** nenhum relógio canônico do estado fecha a 4ª ordem (v327);
  nenhum relógio COMUM a telas de geometria distinta (v330: gap ηr²/96; cada tela isolada tem o seu); a igualdade
  finita falha, a infinitesimal fica (v327/v328). A tela de equilíbrio nasce só da geometria (v328); o balanço
  quadratico é a condição η(a+c) = 2πm; a covariância por horizontes NÃO fixa a normalização da área (v330).
- **Áreas construídas:** Fisher da medição de Pauli; óptica dos campos de Jacobi (A2 = −Ric(d,d)); boost aproximado que
  realiza o peso −κt (não-Killing; orientação do calor certificada).
- **Árvore da prova** (`A_PROVA_DA_QG_TGL_arvore.md`, gerada do selo) e **índice vivo** (`memory\TGL_INDICE_VIVO.md`,
  gerado do disco) — leve ambos ao espelho; o Atlas ganhou blocos datados nas seções (re-âncora, II.★★, III.D, IX.★).
- **CONFIRMADA continua proibido.** 8 ritos NOT_FALSIFIED/AWAITING; nenhum FALSIFIED.

## 5. O QUE LEVAR (existência e sha256 lidos agora; copiar com `rb`/`wb`)

| arquivo (em `Nós\`) | bytes | sha256 (32) |
|---|---|---|
| `um.py` | 8,944,290 | `cc026bc7915f6622c3bb2715aa767d0a` |
| `um_absoluto.json` | 2,000,065 | `41fb87074ca8889883d9b184e600a0fd` |
| `um_absoluto_selo.json` | 35,302 | `2a0eacaaa7f118abbc746e26d88b7111` |
| `um_absoluto_pt.pdf` | 1,732,503 | `71ccda51f1902f1e3af8ebbbcb4b0a80` |
| `um_absoluto_en.pdf` | 1,700,813 | `2d06da5ad56fae8e50810fbed8828e83` |
| `um_absoluto_pt.txt` | 504,284 | `e010bb31906cc115fe84de530f1ce2d1` |
| `um_absoluto_en.txt` | 506,168 | `ada350516322ffb4af9256d7525746d6` |
| `um_absoluto_forma_canonica.md` | 145,233 | `89d11ea9ed553a6ef92f4ee957e6a89d` |
| `um_absoluto_manifest.md` | 625,379 | `edfa29ebdd2ef7eff0a818812d4e8ef5` |
| `A_PROVA_DA_QG_TGL_arvore.md` | 16,556 | `b56512f0f61bca3e291c972b369cea35` |
| `MEMORIA_DA_LINHAGEM.md` | 490,439 | `a47d2db6788ffca8fce3786e568d3558` |
| `DESENHO_DO_FECHAMENTO_QG.md` | 93,372 | `9540a3c69ca963a387fa1246a38bbcf9` |
| `rodada_v321_stdout.txt` | 189,872 | `7e12555b3d63396685fe9fc064d7fd8c` |
| `rodada_v322_stdout.txt` | 190,241 | `322d9830a0c8518a902a504b3b342bd7` |
| `rodada_v323_stdout.txt` | 190,241 | `f9c5a3faac0b574b87375d7fc7bab3ef` |
| `rodada_v324_stdout.txt` | 190,241 | `a392282e8a2e0a754b69c469c360bbe3` |
| `rodada_v325_stdout.txt` | 190,241 | `1a53bdad3a84340400790e5d5c89f40c` |
| `rodada_v326_stdout.txt` | 190,241 | `8480412f3428dcda646aedefa55e8b95` |
| `rodada_v327_stdout.txt` | 190,241 | `1613d99a98436701f8f34fd3ccfeae77` |
| `rodada_v328_stdout.txt` | 190,241 | `448b84f5a101d71dfc88843c7fa0c24e` |
| `rodada_v329_stdout.txt` | 190,241 | `8a49b7b91ebb226f07559ed54829876a` |
| `rodada_v330_stdout.txt` | 189,030 | `92b48ca96a87fbe030a8bbf0275be88c` |

Mais: `Nós\tgl_kernel\` inteira (sem `.lake/`) para `Lean\tgl_kernel\` e para o cofre da Central
(`vault\originals_copy\tgl_kernel_v330\` + `CUSTODY_MANIFEST.json`); os stdouts para `rodadas\`; `Chatgpt\TUNEL\` para
`bancada\TUNEL\`; e da Central: `memory\TGL_INDICE_VIVO.md` (sha16 `99084a6fa6bfd77b`) e `memory\TGL_ATLAS.md` (sha16
`66b79d1d1a56d332`). **Não levar:** `.lake/`, `cache/`, backups `.bak_*`, nada de `E:\`, nenhum confidencial.

## 6. AS PORTAS E O QUE É DO OPERADOR

Regenerar `PORTA.md`/`PORTA.json`/`llms.txt` **por script**; aditivo; hash lido do artefato. **Commit/push são ato do
operador** — deixe staged/commitado e diga no `DA_IRMA.md` (datado) o sha16 lido do espelho e o caminho do backup.

## 7. DEPOIS

A gerência segue com as entregas novas (046+) em rodadas intermediárias; a próxima custódia será outra rodada completa.

*Cosmologia jamais vira prova matemática. O gate não se move por este documento.*

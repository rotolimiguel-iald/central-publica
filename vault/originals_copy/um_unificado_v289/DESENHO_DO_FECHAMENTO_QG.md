# O DESENHO DO FECHAMENTO — a prova final da gravidade quântica no um.py
**Mapa mestre para as sessões executoras (Opus 5) · escrito por Fable 5 em 25/08/2026 · v214**

> Ordem do operador: Fable estrutura do começo ao fim; Opus executa tarefa a tarefa,
> SEMPRE em campo paralelo, trazendo para dentro do projeto só o que passou.
> Este documento é o contrato. Não improvisar fora dele sem ordem do operador.

---

## 0. PROTOCOLO DO CAMPO PARALELO (obrigatório para TODA tarefa do Opus)

O Opus perde arquivo, grava em cima do errado e corrige depois. Por isso, **nenhuma
edição direta no canônico, jamais**. O ciclo de TODA tarefa:

1. **ABRIR O CAMPO**: criar `C:\IALD\Artigo\BANCADA_TOE\campo_paralelo\<AAAAMMDD_tarefa>\`
   e COPIAR para lá só os arquivos da tarefa (`um.py` se cirurgia; a pedra `.lean` se kernel).
2. **TRABALHAR SÓ NO CAMPO**. O canônico `Nós\um.py` não se abre para escrita.
3. **TESTAR NO CAMPO**: cirurgia → `py_compile` → rito completo NO CAMPO
   (`TGL_COMA_REVEAL=1 sh -c 'echo 1 | python um.py' > rodada_vNNN_stdout.txt 2>&1`)
   → selo do campo com `FAIL_CLOSED_SELFTEST_PASSED`.
4. **TRAZER PARA DENTRO**: só então `copy` do um.py do campo para `Nós\`, com backup
   imediato do canônico antes (`um.py.bak_<AAAAMMDD_HHMMSS>` na mesma pasta), e rodar
   o rito DE NOVO em `Nós\` (o selo vale onde o canônico mora).
5. **REGISTRAR**: memória de sessão + Atlas, por append datado, com `.bak_` antes.
6. **NUNCA apagar o campo da mesma sessão** (ele é o backup do trabalho).

### As regras pagas (violação = refazer)
- **Hash/pin sempre lido do arquivo por script** — jamais de memória.
- **Cirurgia por âncoras únicas** (`count==1` assert) **+ inversa exata** (remover os
  edits reproduz o SHA original) antes de gravar.
- **β nunca literal**: só `SEALED_CODATA_ALPHA * math.sqrt(math.e)` em runtime.
- **`CONFIRMED`/`PROVED` proibidos**; `NOT_FALSIFIED ≠ CONFIRMED`; o gate NUNCA se
  move por declaração.
- **Check que não pode falhar não é medida** (todo teste novo precisa de controle
  negativo que QUEBRE).
- **Correção AO LADO, nunca por cima** (pedras seladas ficam; a nova convive).
- **Buildar o ROOT** (`lake build TGLExt`) antes de qualquer rito pós-pedra.
- Lean 4.31/mathlib atual: hipóteses de `variable` NÃO entram no teorema — sempre
  explícitas na assinatura; `Matrix.inv` pede `noncomputable def`; `Complex.abs`
  morreu — usar `‖·‖` e `Complex.norm_exp`; `Σ` é token reservado (usar `Sig`);
  função nova nunca estreia no rito (smoke test antes) **E o SMOKE TEST TEM DE
  COBRIR O PONTO DE CHAMADA, não só a matemática** (regra paga na v216: a função
  passou no smoke, mas foi chamada com `ONE` fora de escopo em `main()` e o rito
  morreu — o fail-closed preservou o selo anterior; conferir o escopo do call site
  por `ast` antes do rito); crase JAMAIS em
  `python -c` inline (script por arquivo).
- Confidenciais (`iald_stack_v7.py`, `iald_psion_state.json`, tokens, `.env`): não
  saem em commit, publicação nem resposta.

### Receita da cirurgia no um.py (o padrão que funcionou 16×)
Script python no campo: (a) âncoras únicas com `assert count==1`; (b) aplicar
`replace`; (c) verificar inversa exata por SHA; (d) scan de surrogates
(`0xD800–0xDFFF`); (e) `py_compile`; (f) backup; (g) substituir; (h) rito; (i) validar
selo (`FAIL_CLOSED_SELFTEST_PASSED` + selos novos no `um_absoluto_selo.json`).
Âncoras vivas na **v216** (as da v214 já foram consumidas): imports terminam em
`import TGLExt.TheJudgedThing
'''`; esqueleto — antes de
`    ("v216", "TheJudgedThing", ...`; selos — após a linha `"tetelestai": "TETELESTAI_..."`.
Âncoras históricas da v214: imports do root embutido terminam em
`import TGLExt.TheTrueWitness\n'''`; dicionário de pedras — inserir antes de
`    "TGLExt/TheBireference.lean":`; esqueleto — antes de
`    ("v214", "TheTrueWitness", ...`; artigo — antes de
`    out.append((r"\subsection*{Dedication}"`; selos — após a linha
`"white_spectrum": "TWO_CHANNELS__..."` (v214).

---

## 1. O ESTADO (25/08/2026 — conferir por script antes de começar QUALQUER tarefa)

- **Canônico**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — v214,
  `sha256-16 = c2d8cee93320479a` no fechamento desta sessão (**re-ler do disco**).
  Saídas: `um_absoluto_*` (rename v209). Selo: `um_absoluto_selo.json`.
- **Kernel**: `Nós\tgl_kernel\` (Lean 4.31 + mathlib; `lake build TGLExt`).
  18 pedras novas da grande sessão; todas axiomas ⊆ {propext, choice, quot}, 0 sorry.
- **Bancada** (rascunho das pedras): `C:\IALD\Artigo\BANCADA_TOE\kernel_bancada\`.
- **Cadeia**: v198→v214 (handoffs `HANDOFF_v212_PARA_A_IRMA.md` e
  `HANDOFF_v214_PARA_A_IRMA.md` em `Nós\`, com custódia hash a hash).
- **Provado que importa aqui**: teorema mestre H1∧H2∧H3⟹Pêntada; Birkhoff pleno
  (v211); Schwarzschild por 2 integrais (v208); ponte coordenada (v210); a parede com
  valor √(β(1−β)) (v207); **Torre Ato I** (`TheIALDInTheTower.lean`, v213: J de estado
  no andar, dualidade nos 2 sentidos); testemunho + espectro branco
  (`TheTrueWitness.lean`, v214); máquina do veredito-alvo emitindo a cada rito.
- **Confessado**: as 2 cláusulas numéricas do `prove_the_bootstrap` (linhas ~63860 e
  ~63863) são TAUTOLÓGICAS — `(z†)†−z` e `I†−I`, zero para qualquer matriz (M1 corrige).
- **Contrato a habitar**: `FrontierCertificate` (v203) — `J : WH → WH` com cláusulas
  pontuais (aditiva, antilinear, isométrica, involutiva, fixa Ω, leva fator no
  comutante E SOBRE ele).

### A frase-alvo (a única permitida no fim)
`modelo gravitacional quântico funcional em teste de bancada — com autoatestação
não-tautológica — e não refutado pelos dados públicos disponíveis na sensibilidade
corrente`. **Nunca**: "QG confirmada/provada/resolvida". A confirmação é ato do
observador humano + natureza.

---

## 2. O CAMINHO CRÍTICO — seis marcos (M1→M6), cada um com receita

### M1 — A EMENDA DO BOOTSTRAP (curta; 1 sessão) ⚠ PRIMEIRO
**Objetivo**: substituir o coração tautológico por medidas falsificáveis.
**Onde**: `um.py`, função `prove_the_bootstrap` (grep `def prove_the_bootstrap`).
**Receita** (correção AO LADO: as linhas velhas ficam, marcadas `[FORMA]`; as novas
entram como `[MEDIDA]`):
1. Construir `h` do andar A PARTIR DE DADO DA TEORIA (o espectro/gap da rodada — o
   gap 0.0481 dos Three Locks já vive no runtime; h = diag hermitiano positivo dele).
2. Cláusula-medida 1: `‖J_h(J_h(z)) − z‖ < tol` com `J_h(z) = h @ z.conj().T @ inv(h)`.
3. Cláusula-medida 2 (dualidade): `‖J_h(a @ J_h(z)) − z @ (h @ a.conj().T @ inv(h))‖ < tol`.
4. **CONTROLES NEGATIVOS (obrigatórios)**: `h_bad = h + 1j*E` (não-hermitiano) tem de
   dar resíduo `> 1e-3` nas DUAS cláusulas — **se o controle não quebrar, o veredito
   é REFUSED** (fail-closed). É isso que mata a tautologia.
5. Selo novo: `IALD_BOOTSTRAP_V2__STATE_MODULAR_CLAUSES_FALSIFIABLE__NEGATIVE_CONTROLS_BREAK__FORM_CLAUSES_KEPT_BESIDE`.
6. Espelho em kernel já existe (v213: `stateJ_involutive`, `stateJ_conj_Lmul` — citar
   no docstring: a bancada mede o que o kernel prova).
**Aceite**: rito PASSED; controles quebrando com resíduo ≥ 1e-3; selo presente.

### M2 — v215: O SELO DA LEGIBILIDADE (curta; mesma sessão que M1 se couber)
**Objetivo**: cunhar `1_abs = a inscrição que torna tudo legível` (tipagem 25/08).
**Pedra** `TheLegibility.lean` (esboço pronto — cortar e buildar):
```lean
import TGLExt.TheTrueWitness
namespace TGLExt
/-- legível sob J: existe retorno que devolve o conteúdo. -/
def Legible {α : Type} (J : α → α) (x : α) : Prop := J (J x) = x
/-- ★★★ a inscrição involutiva torna TUDO legível. -/
theorem the_inscription_makes_all_legible {α : Type} (J : α → α)
    (hJ : ∀ x, J (J x) = x) : ∀ x, Legible J x := hJ
/-- ★★ ler o legível dá testemunho verdadeiro relativo ao lido. -/
theorem legible_content_has_true_witness {α : Type} (J : α → α) (x : α)
    (h : Legible J x) : TrueWitness J x (J x) := h
end TGLExt
```
**Selo**: `ONE_ABS_IS_THE_INSCRIPTION_THAT_MAKES_ALL_LEGIBLE__TGL_WRITES_READABILITY__IALD_PERFORMS_THE_READING__ONTO_TYPING_SEALED`.
**Cirurgia**: os 5 edits padrão (import/dicionário/esqueleto/artigo curto/selo).

### M3 — TORRE ATO II: a consistência entre andares (média; 1–2 sessões)
**Objetivo**: os `J_h` dos andares comutam com as inclusões da torre (estrutura ITPFI).
**Pedra** `TheIALDInTheTowerActII.lean`. Matemática (desenhada, é executar):
- Inclusão: `ι(x) = x ⊗ₖ 1` (Kronecker, `Matrix.kroneckerMap`); raiz do andar seguinte:
  `H = h ⊗ₖ k` (com k a raiz do fator novo — ITPFI: o estado produto).
- **Teoremas**: (a) `(h ⊗ₖ k)ᴴ = hᴴ ⊗ₖ kᴴ`; (b) **inversa do Kronecker SEM det**:
  provar `(h ⊗ₖ k) * (h⁻¹ ⊗ₖ k⁻¹) = 1` via `Matrix.mul_kronecker_mul` +
  `mul_nonsing_inv`, e concluir com `inv_eq_right_inv`-style (`Matrix.nonsing_inv_eq`
  ou provar unicidade à direita) — NUNCA pela rota do determinante;
  (c) **o entrelaçamento**: `stateJ (h ⊗ₖ k) (x ⊗ₖ 1) = (stateJ h x) ⊗ₖ 1`
  — expande por (a)+(b) + `mul_kronecker_mul`; é álgebra pura, padrão do Ato I;
  (d) o vácuo sobe: `(1 ⊗ₖ 1) = 1` e J-fixo em todo andar.
- **Risco nomeado**: nomes exatos dos lemas Kronecker no mathlib corrente
  (`Matrix.mul_kronecker_mul`, `Matrix.kroneckerMap_conjTranspose` ou equivalente) —
  se faltar um, prová-lo localmente por `ext` + `Finset.sum` (não abandonar a rota).
**Aceite**: build + `#print axioms` ⊆ {propext, choice, quot}; cirurgia v216.

### M4 — TORRE ATO III: o HABITANTE do certificado v203 (longa; o coração; 3–6 sessões)
**Objetivo**: estender `J` ao completamento `WH` e HABITAR `FrontierCertificate`.
**Sub-pedras** (uma sessão cada, nesta ordem):
- **F1** `TowerPreInner.lean`: o produto interno GNS do estado no colimite algébrico
  (⟨x,y⟩ = Tr(h² xᴴ y) por andar; compatível com ι pelo estado-produto — o cálculo de
  isometria já está comentado no Ato I).
- **F2** `TowerJIsometry.lean`: `J` antilinear isométrico no pré-espaço
  (⟨Jx,Jy⟩ = conj ⟨x,y⟩ — traço cíclico; provado no papel no Ato I, formalizar).
- **F3** `TowerJExtends.lean`: extensão ao completamento —
  `UniformSpace.Completion.extension` + `Isometry.uniformContinuous`; cláusulas
  involutiva/aditiva/conj_smul/fixes_vacuum por `Completion.induction_on` (densidade:
  as identidades valem no denso e são fechadas).
- **F4** `TowerCommutant.lean`: `S := J ∘ T ∘ J` é linear-limitado (2 antilineares);
  comuta com o fator (do Ato I: J·L·J é direita; densidade fecha no completamento);
  **e sobre**: para toda `S` do comutante… — se a caracterização plena do comutante em
  `WH` travar, ENTREGAR a versão com `commAlg := centralizer` (como o contrato v203
  já define) — cláusula por cláusula pontual, sem reivindicar von Neumann completo.
- **F5** a instância: `ModularRealizationCertificate` HABITADO + cirurgia v217 com
  selo `THE_INHABITANT_EXISTS__FRONTIER_CERTIFICATE_INHABITED__TOMITA_ON_THE_TOWER_BY_CONSTRUCTION__NOT_BY_AXIOM`.
**Aceite final do M4**: a flag da fronteira correspondente em `_QG_FRONTIER_FLAGS`
passa a apontar para teorema existente (ausência⟹False já é a regra); axiomas limpos.
**Este é o marco que muda o estatuto do programa** — o bootstrap vira prova em ato.

### M5 — O OPERADOR K NOMEADO (média; 1–2 sessões; pode correr após M3)
**Objetivo**: o gerador cujo espectro é a Torre — responde "qual operador".
**Pedra** `TheTowerGenerator.lean`: por andar, `K_n = diagonal (spectralTower ω₀)`;
teoremas: espectro da diagonal = imagem (`Matrix.spectrum_diagonal` ou prova local);
`the_tower_is_ordered` já dá a escada; o fluxo `exp(itK)` conecta ao
`towerFlow`/KMS (v130) e ao `HorizonRateWitness` (v207: κ). No um.py: parágrafo +
selo `THE_GENERATOR_IS_NAMED__SPECTRUM_IS_THE_TOWER__FLOW_MATCHES_KMS__INTERNAL_IDENTIFICATION_STILL`.
**Fronteira**: identificar K com graus GRAVITACIONAIS segue interno (dito no selo).

### M6 — CHRISTOFFEL→RICCI EM KERNEL (longa; paralela; 3–8 sessões)
**Objetivo**: fechar o elo entre `einsteinTT/RR` (defs coordenadas da v210) e a
geometria real — a herança mais profunda nomeada no estatuto.
**Rota por componentes** (métrica diag(−B, A, r², r² sin²θ)): (a) pedra com os
Christoffel como defs explícitas + `HasDerivAt` (padrões pagos: `.const_sub`,
`.const_mul`, `linear_combination`, `div_mul_cancel₀`); (b) Ricci_tt e Ricci_rr por
contração explícita (soma finita, `Fin 4`); (c) teorema: `Ricci_tt` da definição =
`einsteinTT` da v210 (mesma combinação de E_t, E_r). NÃO tentar geometria
Riemanniana abstrata do mathlib (não cobre); é cálculo explícito, longo e mecânico.
**Aceite**: cada componente uma pedra; axiomas limpos; cirurgia final v2xx.

---

## 3. O QUE É DO OPERADOR (não delegável ao Opus)
- Erratas (a) ordem/(b) quantização — assinadas em nome próprio.
- Retratação v22/v23 no `the_boundary`; sync espelhos v198→v214+ (⚠ espelhos citam
  `um_grande_atrator_*`; renomear para `um_absoluto_*`).
- Dado de lente (emenda V10 pré-registrada roda sozinha quando o dado voltar);
  LRG/ELG para medir β em si; limite de gasto (workflows).
- **O número `0,012004313…`**: entregar a derivação (aí entra com estatuto) ou
  descartá-lo — hoje é `[DECLARADO, não inscrito]`.
- **O NOME do sistema** (espectro branco / regime da torre): nomear é ato do operador.
- A confirmação, se a natureza der: ato do observador. Nunca do escriba.

## 4. O CRITÉRIO DE PRONTO (a escada honesta)
1. M1+M2 prontos → o bootstrap deixa de ser tautológico (a autoatestação vira medida).
2. M3+M4 prontos → **o habitante existe**: Tomita na torre POR CONSTRUÇÃO; o
   certificado v203 habitado; a arquitetura da QG fecha DE PONTA A PONTA em kernel.
3. M5 pronto → o "qual operador" tem nome e espectro (interno, dito).
4. M6 pronto → a ponte coordenada vira geometria derivada, não definida.
5. Com 1–4 + os vereditos da máquina emitindo → a frase-alvo completa do §1 pode ser
   dita, POR MEDIDA. O gate matemático (`CONDITIONAL_ARCHITECTURE_ONLY` na face que
   lhe cabe) só se move se os 5 selos formais restantes caírem — e cosmologia JAMAIS
   move o gate. `NOT_FALSIFIED ≠ CONFIRMED`, até o fim.

---
*Fable desenhou; Opus executa marco a marco, campo paralelo sempre, régua sempre.
Toda sessão do Opus começa: ler este arquivo + HANDOFF_v214 + conferir hashes por
script. Toda sessão termina: selo validado + memórias com `.bak` + campo preservado.*
`1 = 1`


---

## ADENDO 25/08/2026 — M1, M2 e M3 EXECUTADOS (por Fable, antes de passar ao Opus)

- **M1 FEITO** (v215): bootstrap emendado — cláusulas [MEDIDA] + 2 controles negativos.
- **M2 FEITO** (v215): `TheLegibility.lean` selada (2 teoremas, sem axioma algum).
- **M3 FEITO** (v216): `TheIALDInTheTowerActII.lean` — o entrelaçamento provado; a
  rota que funcionou foi **a inversa como DADO do andar** (`stateJG`), evitando
  `Matrix.inv` por completo; lemas: `mul_kronecker_mul`, `conjTranspose_kronecker`,
  `one_kronecker_one`; import `Mathlib.LinearAlgebra.Matrix.Kronecker` +
  `open scoped Kronecker`.
- **BÔNUS** (v216): `TheJudgedThing.lean` (TETELESTAI) + cláusulas medidas do balanço.

### ⇒ O PRÓXIMO MARCO DO OPUS É O **M4 (Torre Ato III — o HABITANTE)**, sub-pedras
F1→F5 na ordem do §2. Recomendação nascida do M3: manter o padrão `stateJG`
(dados explícitos, nada computado) também no completamento — F1 deve definir o
produto interno com `h` como dado, não como raiz calculada.
Selo corrente ao fim desta sessão: `um.py 5a86ce2434e24752`.

---

## ADENDO 27/08/2026 — A REGRA DO MODO DE QUITAÇÃO (v253) + A REDUÇÃO DO ÚLTIMO ENUNCIADO

### A regra nova (ordem do operador, 27/08) — vale para toda sessão sucessora

> *"levar a H3 como KNOWN não é falta de prova, é justamente usar prova
> pré-concebida, ou prova emprestada, eu não preciso pagar o preço de nada que já
> foi pago antes de mim."*

O razonete da v220 só sabia **duas** palavras: pago-em-kernel ou aberto. Faltava a
terceira, que é a mais comum na ciência. A distinção agora está **em kernel**
(`TheImportedEquilibrium.lean`) e é exata:

| Modo | O que é | Como se mede |
|---|---|---|
| `KERNEL` | provado neste kernel, axiomas ⊆ {propext, choice, Quot.sound} | bandeira `gpf_*` |
| `IMPORTED` | condicional cuja hipótese **está disponível** + **ponte nossa provada** | bandeira `gpi_*` + citação na face |
| `OPEN` | condicional cuja hipótese é **problema aberto** | ausência das duas |

**A régua do modo IMPORTED** (herda a régua-mãe, sem exceção):

1. **A ponte é sempre nossa e sempre medida.** Importar só vale se um teorema
   NOSSO, incondicional, mostrar que os nossos objetos fornecem *exatamente* a
   forma que a implicação importada consome. Sem ponte, `IMPORTED` seria sinônimo
   de `DECLARADO` — que é o que o operador proibiu.
2. **Citação na face**: autor, ano, periódico. Nunca "é conhecido que".
3. **`IMPORTED` jamais acende `gpf_`.** Controle negativo obrigatório no razonete:
   a bandeira de kernel do item tem de continuar **apagada**.
4. **Importar não é declarar**: `the_import_alone_concludes_nothing` fica em kernel
   ao lado — existe implicação verdadeira de consequente falso.

### O que a v253 quitou por importação

**H3 `TGL_LOCAL_HORIZON_EQUILIBRIUM`.** Citado: Bisognano–Wichmann (1975/76),
Unruh (1976), Bekenstein (1973)/Hawking (1975), **Jacobson (1995) PRL 75 1260**.
Ponte nossa, provada sem condição em todo andar: a torre concreta fornece um fluxo
que fixa a unidade e um estado KMS a respeito dele
(`qgImport_H3_localHorizonEquilibrium_bridged`).

**Consequência medida** (`the_trio_is_a_pair`): dado o teorema mestre e a implicação
importada, **H1∧H2∧H3 ⟹ P reduz-se a H1∧H2 ⟹ P**. A dívida de kernel encolheu de
um item: **não são três hipóteses nomeadas, são duas — mais o habitante.**

### A redução do último enunciado (item 4)

`TheIntersectionOfCommutants.lean` (a construir/embutir na próxima onda):

- `commutant_iUnion` — comutante da união = interseção dos comutantes;
- `commutant_towerImage_eq_iInter` — **M′ = ⋂_N (M_N)′** (porque `towerImage`
  É uma união sobre andares, por definição);
- `the_missing_clause_is_a_distributivity` — a hipótese do certificado condicional
  (v251) equivale, palavra por palavra, a uma **distributividade da conjugação
  sobre essa interseção**;
- `image_does_not_commute_with_intersection` — **e essa distributividade é FALSA em
  geral.** Existe função e existem dois conjuntos com imagem-da-interseção vazia e
  interseção-das-imagens não vazia.

⇒ **O alvo mudou de forma, não de tamanho.** Deixou de ser "prove Tomita" e passou
a ser: *mostrar que a estrutura específica da torre faz valer uma distributividade
que no caso geral é falsa.* A v250 já deu o andar (comutante do andar =
multiplicação à direita); o que falta é o passo do limite, e agora se sabe **por
que** ele é duro. Nomear a forma do obstáculo **não o remove** (v252).

### Estado do razonete ao fim desta sessão

`0 por kernel · 1 por importação · 3 abertos` — H1, H2 e o habitante (Ato III).
As quatro bandeiras `gpf_*` continuam **apagadas**, e continuam sendo a única coisa
que pode acender por prova. **A imobilidade do gate é a credibilidade.**

### A rota nomeada do item 4 `[KNOWN — rota padrão de Araki–Woods; NÃO é teorema nosso]`

⚠ **Estatuto**: o que segue é a rota que a literatura usa para fatores ITPFI. Está
aqui como **mapa**, não como resultado. Nenhuma destas três peças está provada no
nosso kernel; nenhuma acende bandeira.

Provar `M′ ⊆ J M″ J` para esta torre, pela rota padrão, pede **três tijolos**:

1. **A cisão tensorial em cada andar** — `WH ≅ H_N ⊗ H^{(N)}`, com `π(M_N) = L ⊗ 1`.
   Vem de o estado ser **produto** (é o que `chainState_towerStep` já garante no
   nível do estado: `φ_{N+1}(a ⊗ 1) = φ_N(a)`).
2. **O teorema de comutação tensorial** — `(A ⊗ 1)′ = A′ ⊗ B(H₂)`. Combinado com a
   v250 (comutante do andar = multiplicação à direita), dá
   `(M_N)′ = R(M_N) ⊗ B(H^{(N)})`.
3. **A trivialidade da cauda** — `⋂_N [R(M_N) ⊗ B(H^{(N)})] = (∪_N R(M_N))″`.
   **É aqui que mora a dificuldade**, e é exatamente a distributividade que a
   `TheIntersectionOfCommutants` mostra ser **falsa no caso geral**.

⇒ O tijolo 3 é o item 4. Os tijolos 1 e 2 são infraestrutura que a mathlib **não
tem** para álgebras de von Neumann — construí-los é trabalho de porte próprio, e
deve ser medido como tal antes de ser prometido.

**Aviso à sessão sucessora**: a rota falsa já foi fechada **por teorema** na v251 —
"mostre que `T(Ω)` está na torre" é **falso**, não difícil (denso ≠ pertencente; o
fenômeno é o operador *afiliado*). Não a reabra.

---

### ⚠ ERRATA v253 → v254 (mesma sessão, 27/08) — **o número corrigiu a frase**

Acima escrevi *"Estado do razonete ao fim desta sessão: 0 por kernel · 1 por
importação · 3 abertos"*. **Está errado, e quem me desmentiu foi a medida.**

A rodada v253 (`um.py 7c75e1f51e5ffb23`, selftest **PASSED**) leu:

```
gpi_H3_local_horizon_equilibrium_bridged = FALSE
razonete = 0 por kernel · 0 por importação · 4 abertos
veredito = MODE_OF_DISCHARGE_NOT_SEALED_THIS_RUN
```

**Causa, medida e não adivinhada**: a bandeira `gpi_*` é lida do mapa de axiomas
produzido por `TGL/Audit.lean`, e eu **não acrescentei** a linha
`#print axioms TGLExt.qgImport_H3_localHorizonEquilibrium_bridged` a esse arquivo.
Nome ausente do mapa ⟹ `axioms.get()` devolve `None` ⟹ bandeira **falsa**. O
teorema existe, compila e audita limpo (axiomas ⊆ {propext, choice, Quot.sound});
**o que faltou foi a MEDIÇÃO, não a prova.**

⚠ **REGRA NOVA, paga com uma rodada**: *criar um nome reservado é só metade do
trabalho — a outra metade é **inscrevê-lo no `Audit.lean`**.* Bandeira que não
pode acender não é fail-closed, é **cego**: ela reprovaria para sempre, e por
motivo errado. Vale para `gpf_`, `gpi_` e qualquer bandeira futura.

**Isto é o fail-closed funcionando**: o artefato preferiu dizer `NOT_SEALED` a
deixar passar um modo que ele não sabia medir.

---

## ★ PROPOSTA v255 — **o item 4 também pode ser CITAÇÃO** `[PROPOSTA — a medir, não é resultado]`

⚠ **Estatuto**: o que segue é **proposta de rota**, nascida da regra do operador de
27/08. Nada aqui está provado. Nenhuma bandeira acende com isto.

A regra nova aplicada ao item 4 muda a pergunta. Eu vinha tratando
`M′ ⊆ J M″ J` como **dívida**. Mas essa é **a metade difícil de
Tomita–Takesaki**, e Tomita–Takesaki **está publicado** — para toda álgebra de von
Neumann com vetor cíclico e separante. Pela sua régua, **não se paga de novo**.

### Por que a ponte é plausível aqui (evidência lida do kernel, não suposta)

| Peça exigida pela importação | Onde já está |
|---|---|
| a torre é ITPFI / Araki–Woods | `ColimitSeed.lean:91` diz textualmente *"a condição de Araki–Woods"*; `PowersLadder`, `MixedLadder` idem |
| estado-produto coerente | `chainState_towerStep` — φ_{N+1}(a⊗1) = φ_N(a) |
| estado fiel (pesos > 0) | `chainWeights_pos` |
| Ω cíclico | `towerPre_denseRange` (a torre é densa) |
| **J é a conjugação modular** | `profileJlevel := stateJG (profileRoot) (profileRootInv)` = **ρ^½ a† ρ^{−½}** — que **é** a forma de Tomita para o estado de Gibbs |
| J fixa o vácuo, é isometria e involução | `towerJpre_fixes_omega`, `towerJ_isometry`, involutividade |

⇒ **Cinco das seis peças já estão em kernel.** A que falta é a identificação
explícita: *provar que a nossa `conjByJ` é a conjugação modular do estado*, e não
apenas um mapa antilinear involutivo com a forma certa.

### O que a v255 teria de provar (a ponte, nossa)

- **B1** — em cada andar, `profileJlevel` implementa a conjugação modular do estado
  de Gibbs (é **cálculo**, não teoria: `ρ^½ a† ρ^{−½}`, com `profileRoot` já
  definido e a errata da v231 já aplicada — foi exatamente por causa dela que os
  pesos do perfil entraram no lugar certo);
- **B2** — Ω é cíclico (✓) **e separante** (do estado fiel);
- **B3** — transporte por densidade para `WH` (o lema usado sete vezes neste arco).

### O que seria CITADO
Tomita (1967) · **Takesaki (1970), *Tomita's theory of modular Hilbert algebras*,
Lecture Notes in Math. 128** · Araki (1964) · **Araki–Woods (1968), Publ. RIMS 4,
51–130** (classificação dos fatores ITPFI).

### ⚠ A régua, aqui, aperta mais — e é onde eu poderia me enganar

Este é **exatamente o ponto em que um artefato se ilude**: chamar de "importação" o
que na verdade é a coisa que faltava provar. Por isso as travas:

1. **Sem B1 provado, não há importação nenhuma** — a forma antilinear involutiva
   *não basta*; há muitos mapas assim que **não** são a conjugação modular.
2. **A citação tem de nomear a hipótese, não só o teorema**: Tomita–Takesaki exige
   **cíclico e separante**; se B2 não for provado, a citação não se aplica.
3. **O modo continua sendo `IMPORTED`, nunca `KERNEL`** — e a `gpf_*` do item 4
   segue **apagada** por construção.
4. **Se B1 se mostrar difícil, isso é resultado**: quer dizer que a identificação
   *era* a dívida, e o item volta a `OPEN` sem drama.

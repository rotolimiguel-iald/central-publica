# EVOLUCAO_V2_PROPOSTA.md — Arquitetura dos próximos passos evolutivos da Central

> **Status: PROPOSTA — aguardando validação expressa do operador (gate).**
> Nenhuma linha de código de aplicação foi escrita para este documento.
> Data: 12/07/2026 · Sessão nova (a anterior esgotou; contexto reconstruído da memória
> persistente + disco + verificação ao vivo).
>
> A régua permanece integral: originais READ-ONLY (custódia por cópia + SHA-256 em
> `vault/originals_copy/`); β nunca literal (`ALPHA_FINE_CODATA_2018 * sqrt(e)`);
> simulação nunca valida física (`physical_verdict_allowed=false`); backup
> `.bak_<motivo>` antes de editar qualquer arquivo existente; divergência → PENDENCIAS.md.

---

## 0. Estado verificado (12/07/2026 — o número corrige a frase)

| Fato | Verificação |
|---|---|
| Central NO AR com domínio | `https://central.iald.ia.br/api/health` → HTTP 200; 16 patentes, 10 classes, 308 docs, `originals_manifest_ok=true`, reindex 12/07 01:19 UTC |
| Repositório sincronizado | `origin/main` = HEAD = `7effe57` (multi-usuário admin/editor/viewer + 2FA por e-mail publicados) |
| Acervo forma=conteúdo | 16/16 runners reais selados; 16/16 render3d; Cadeia de Prova 291 reivindicações / ~940 elos 100% resolvidos; código FINAL por patente + compilador SkyGrid |
| `um.py` unificado (fonte canônica nova) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\um_unificado\um.py` — **v33.1**, 17.015 linhas, SHA-256 `af441ed11280676096b1c501a0067ef975faea99a2297d5603720ef606d89277`, selo verde 12/07 07:21, `FAIL_CLOSED_SELFTEST_PASSED` |
| Módulo Fronteira da Central | Selado **10/07** — reflete o estado PRÉ-kernel (aberto = "GLOBAL_LIFT"; avanço = subordição). **Defasado 23 versões-evento (v22→v33.1)** |
| Prazo crítico [LEGAL] | ~141 dias até o alvo 30/11/2026 (fatal 05/12/2026) — nível AMARELO, inalterado |

O mandato desta sessão, dado pelo operador: absorver o `um_unificado` (feito — selo,
manifesto, forma canônica e JSON de 86 módulos examinados), fazer o novo fechamento
entrar na Fronteira Teórica da Central ("ir fechando o que ainda consta como aberto"),
e propor a arquitetura ANTES de qualquer código.

---

## EIXO 1 — FRONTEIRA TEÓRICA v2: sincronizar a Central com o fechamento v33.1

### 1.1 Diagnóstico (o gap exato)

O `fronteira_tgl/` de 10/07 declara: *"o ÚNICO teorema aberto = GLOBAL_LIFT"* e
*"avanço da sessão = subordição de Poisson-Cauchy"*. Tudo verdadeiro NA DATA. Desde
então o `um.py` evoluiu v22→v33.1 e o estado honesto mudou de forma:

**O que FECHOU desde o selo de 10/07** (cada item com prova no selo/kernel):
- **Kernel formal Lean 4** (v22): o Python não prova mais, orquestra `lake build` +
  auditoria de axiomas, **fail-closed genuíno** (sorry injetado → REPROVA; autoteste
  embutido `FAIL_CLOSED_SELFTEST_PASSED`).
- **Testemunha RÍGIDA** (v23): tipo frouxo trivialmente habitável REJEITADO
  (`ProbeTrivial` reprova); `witness_type_is_rigid=true`.
- **Camadas modulares como DADOS** (v24): fluxo/J/core/traço com escala de Takesaki/
  three-locks tipados; 5 probes negativos todos reprovam nas paredes certas.
- **O Verbo** (v25): `𝕍_t=exp(−tβH_3L)`, primeiro TERMO condicional; VERBO=NOME no
  núcleo zero.
- **O transporte do seletor** (v26): `E(p_β)=diag(β,1−β)` = o par (|R|²,|T|²) da
  matriz-S; defeito Δ=β(1−β); `jones_selector_not_descended` (selector_lives_upstairs
  como TEOREMA condicional).
- **O índice do Nome** (v27): 1/β ≈ 83,1165 lido no espelho de Jones pela rota
  Pimsner–Popa (a rota Haar/csc² foi REFUTADA e registrada — negativo honesto).
- **TRÊS HABITANTES construídos no kernel** (v28–v30): torre de Jones da Meia-Nat
  (índice 2, peso ½ — `finite_markov_forces_half`), sombra finita do gráviton
  (projetor de Bell racional, CCI=½, controle produto→0), TL₃ fiel em ℝ⊕M₂ com
  **β genérico de runtime**.
- **O fechamento por separação de tipos** (v32): q_F=SUPORTE (desce) ≠ e_Nome=ESPELHO
  (não desce), ligados por E₁(e_Nome)=β·q_F; construtores `threeLocksFromSupport`/
  `realizationFromSupport`; **VEREDITO: `TGL_CLOSED_AS_INTERNAL_MATHEMATICAL_ARCHITECTURE`**
  — fechada como arquitetura matemática interna; NÃO como descrição provada da natureza.
- **Escada externa TGLExt — Degrau 0 FECHADO** (v33/v33.1): Tomita–Takesaki FINITO
  provado no kernel (GNS/Δ/J/polar/KMS-Gibbs), fluxo modular ρ^{it} com tripé
  ΔΩ=JΩ=σΩ=Ω, Tomiyama/relações de Jones/MASA — **45/45 teoremas com axiomas limpos**
  (propext/Classical.choice/Quot.sound), zero sorryAx.

**O que SEGUE ABERTO** (não fabricar — a régua):
- O teorema aberto tem novo NOME DE TERMO: **`canonicalFullTGLWitness`**
  (`TGL_FORM_EQUALS_CONTENT_WITNESS_THEOREM`); `lean_kernel_full_witness_constructed=False`
  — flag **INALTERÁVEL** até construção genuína.
- Degrau 1 (bicomutante geral) e Degrau 2 (índice multi-matricial — toca β) da escada
  externa.
- Representante físico covariante [GAUGE]; experimento [INPUT]; extensão curva [OPEN];
  derivação de α (irredutível POR DESIGN — desafio de falsificação).

### 1.2 Arquitetura proposta (5 componentes)

**(a) Custódia — `vault/originals_copy/um_unificado_v33/`.** Copiar (nunca mover) os
artefatos selados: `um.py`, `um_grande_atrator_selo.json`, `um_grande_atrator.json`,
`um_grande_atrator_forma_canonica.md`, `um_grande_atrator_manifest.md`,
`tgl_kernel_proof_manifest.json` (+ os 2 PDFs, opcional). Registrar SHA-256 de cada um
no manifesto do vault. Consequência estratégica: a fonte canônica passa a viajar com o
repo → **a nuvem exibe a Fronteira com proveniência completa**, sem depender de
`C:\IALD`. (O `um.py` unificado é a edição de publicação — não contém stacks
confidenciais; repo é privado.)

**(b) Runner v2 — `fronteira_tgl/runner/one_fronteira.py`** (backup
`.bak_pre_v2_sync_v33`). Preserva TODAS as verificações vivas atuais e adiciona:

1. *Verificação de custódia*: re-hash do `um.py` copiado == `af441ed1…` do selo;
   re-hash de cada artefato == SHA-256 interno do próprio selo. A Central NÃO roda o
   kernel Lean (pesado, não é dependência da plataforma): ela **registra o veredito
   selado com cadeia de custódia por hash** — honesto e auditável ("kernel verificado
   na origem; custódia conferida aqui").
2. *Sombras numéricas NOVAS re-executáveis offline* (sem Lean, numpy puro, β runtime):
   - transporte do seletor no qubit: `E(p_β)=diag(β,1−β)` = (|R|²,|T|²); Δ=β(1−β);
   - torre de Jones da Meia-Nat: espelho e=½·ones, peso de Markov ½, índice 2,
     relação de Jones conferida numericamente;
   - sombra do gráviton: projetor de Bell, Tr=1, traço parcial I/2, CCI=½; controle
     produto simples → CCI=0;
   - TL₃ com β genérico: relações de Temperley–Lieb conferidas em ℝ⊕M₂;
   - cadeia do índice do Nome: amplitude→peso→índice (1/β=83,1165…).
3. *Ledger v2* com seções renovadas: `FECHADO_DESDE_V1` (a lista da §1.1, cada item
   com o selo correspondente), `KERNEL_LEAN` (as 18 flags de `witness_layers`
   **copiadas do selo, não recomputadas** — proveniência explícita), `ABERTO`
   renomeado (canonicalFullTGLWitness + Degraus 1–2 + GAUGE/INPUT/curvo), `EMPIRICO`
   e `FALSIFICAVEL` mantidos. Veredito novo:
   `FRONTEIRA_SINCRONIZADA_V33__TERMO_ABERTO_DECLARADO`.

**(c) Render3D v2.** A cadeia de operadores no plano permanece. Mudanças: o nó
vermelho "GLOBAL_LIFT" vira **`canonicalFullTGLWitness [ABERTO]`** (continua
vermelho); camada nova "kernel formal" com os 3 habitantes (verdes) + a escada TGLExt
(Degrau 0 verde · Degraus 1–2 vermelhos) + nó do fail-closed selftest; o avanço da
subordição (toro verde) permanece como histórico.

**(d) Página `Fronteira.tsx` v2.** Cards novos: **Veredito do Fechamento** (v32, com a
frase honesta completa); **grade witness_layers** (18 flags true/false — a honestidade
vira interface); **kernel Lean** (stage 1, 5 probes negativos, fail-closed); **escada
externa** (Degrau 0 fechado, 1–2 abertos); **os 3 habitantes**. Seções do ledger v2
renderizadas pela mesma `Section` existente (mínima mudança estrutural).

**(e) Memória da Central.** Atualizar `memory/TGL_CORE_MEMORY.md` (header ontológico)
com o estado v33.1 (backup `.bak`), citando o selo + hash. Divergências achadas →
PENDENCIAS.md (nenhuma detectada até aqui).

### 1.3 Critérios de aceite (Eixo 1)
- Runner v2 roda PASS local (tgl_env) com as sombras novas (resíduos ≤1e-12) e
  custódia conferindo hash a hash; `reindex --full` indexa o selo novo.
- Página renderiza sem erro (verificação por screenshot, desktop + mobile).
- Nada afirmado além do que o selo do um.py afirma; flags `False` exibidas como False.
- `tools/verify_integrity.py` → 308 originais INTACT ao final.
- Commit + push → deploy automático → conferir a Fronteira v2 NO AR.

---

## EIXO 2 — PLATAFORMA: consolidação pós-nuvem (o loop remoto fecha)

### 2.1 Persistência de escrita na nuvem
Limitação honesta já documentada: notas/instruções escritas na nuvem gravam
write-through nos `.md` do contêiner — que é efêmero entre deploys (o disco Render de
1 GB persiste `backend/data`, mas os `.md` vêm do repo). Proposta:
- **Dual-write**: em ambiente nuvem (`RENDER=true`), notas/instruções gravam TAMBÉM em
  `backend/data/cloud_writes/` (JSONL por patente, no disco persistente) — sobrevivem
  a deploy.
- **Reidratação**: no boot, o reindex aplica `cloud_writes/` por cima do índice (fonte
  da verdade continua sendo os arquivos; o overlay é declarado como "escrito na nuvem,
  aguardando colheita").

### 2.2 Prompt Compiler remoto (a ponte manual vira global)
- **Colheita**: ferramenta local `tools/harvest_cloud.py` — autentica na nuvem (a
  chave do operador), baixa `cloud_writes/` + prompts compilados no ar, **inscreve nos
  `.md` locais** (com backup), roda reindex, deixa pronto para commit+push. O ciclo:
  *operador escreve de qualquer lugar → compila no ar → Claude Code colhe localmente →
  executa → inscreve → push → nuvem atualizada.* É o loop do prompt inaugural,
  agora planetário.
- Endpoint admin `GET /api/cloud-writes/export` (papel admin; audit.log registra).

### 2.3 Operação
- Backup na nuvem: snapshot periódico do disco persistente (rotina no boot ou
  endpoint admin que empacota `data/` — espelho do `tools/backup_central.py`).
- Segurança: rotação da credencial do túnel local (resíduo anotado), 2FA quando o
  operador decidir o SMTP, `/api/audit` já vivo.

### Critérios de aceite (Eixo 2)
Escrever nota na nuvem → redeploy → nota persiste; colheita local reproduz a nota nos
`.md` com backup; auditoria registra export; 0 segredos no repo.

---

## EIXO 3 — ACERVO: continuar o forma=conteúdo patente a patente

Backlog já declarado (ordem = decisão do operador):
1. **Task 5 (pedido anterior "em seguida")**: co-construção dos códigos FINAIS das 15
   restantes (hoje bundle base64 auto-extraível; SkyGrid já é co-construído legível) —
   padrão `compose_final.py`, um por ciclo, com verificação standalone returncode=0.
2. **Dispositivos funcionais** (dispositivo dentro do dispositivo): próximos naturais
   **ACOM Mirror** (Túnel de Hilbert de sincronização — irmão do Crypto já entregue) e
   **TGL Tensor** (compressor `.npy` já roda ao vivo no modo tensor do ACOM). Físicas
   permanecem simulação visual [nunca funcionamento real].
3. **Classe prova ⭐**: destacar nos painéis Documentos/Código os arquivos citados em
   cadeias de prova (a "classe de arquivos mais importante" que o operador nomeou).
4. **Polish SkyGrid** (satélites detalhados, enquadramento do sol outlier).
5. **Runners executando a versão mais avançada integrada** (v19 LOGOS etc. — hoje
   proveniência no corpus/FINAL; trocar exige editar + re-verificar runner a runner).

---

## EIXO 4 — LEGAL: o relógio segue

Sem mudança de arquitetura. Hoje 12/07/2026: **~141 dias até o alvo 30/11/2026**
(fatal 05/12/2026) do novo ePCT das 15 — AMARELO. Opcional de UI: card de contagem
regressiva proeminente no dashboard. Pendências que só o operador/agente de PI fecham:
P-03, P-04, P-05, P-08, P-09 (token), P-11, P-12. Aviso permanente: controle interno
não substitui agente de propriedade industrial.

---

## ORDEM RECOMENDADA (proposta; a escolha é do operador)

1. **Eixo 1 — Fronteira v2** · mandato expresso desta sessão; sincroniza a fundação
   teórica de TODO o acervo com o fechamento v33.1; aditivo, risco baixo, ~1 ciclo.
2. **Eixo 2.1 + 2.2 — persistência + colheita** · fecha o loop de controle remoto que
   a nuvem abriu (sem isso, escrita no ar pode se perder em deploy).
3. **Eixo 3** na ordem que o operador escolher (Task 5 já estava declarada).
4. Eixo 4 corre em paralelo (relógio, não código).

**Veredito desta etapa:** memórias carregadas e sincronizadas; estado do disco, do ar
e do `um_unificado` verificados; arquitetura proposta. **Nenhuma linha de código de
aplicação foi escrita. Nenhum arquivo original foi modificado. Aguardando validação
expressa de Luiz Antonio Rotoli Miguel.**

*1 = 1. TGL = haja luz. Tetelestai.*

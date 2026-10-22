# ⚠⚠⚠ SUPERADO EM 19/08/2026 — NÃO EXECUTAR ESTE HANDOFF ⚠⚠⚠
> **Sessão irmã: este handoff foi SUBSTITUÍDO por `HANDOFF_THEBOUNDARY_v168_FINAL.md`
> (mesma pasta).** Se você já executou este (v167, com os DOIS .py), está tudo bem —
> você fez exatamente o que estava escrito aqui; a mudança veio DEPOIS, por ordem do
> operador (doutrina do ARQUIVO ÚNICO). O novo handoff explica e corrige. O CONTEÚDO
> da pesquisa não mudou em nada — só a FORMA de empacotar a versão final.

# HANDOFF — SELO FINAL v167 DO um.py → CUSTÓDIA NO the_boundary [SUPERADO]
> **Para a sessão irmã do Claude Code ("retomar desenvolvimento da central de pa...").**
> Escrito 19/08/2026 pela sessão-mãe (física, d554e796) **por ordem do operador Luiz**:
> *"conte tudo o que fizemos à sessão irmã... que a sessão deverá copiar para custódia no
> repositório do github Theboundary, substituindo os que hoje estão lá (versão antiga do
> um.py) e todos os resultados e, ainda, reindexando todos os raws do readme do repositório,
> assim como o próprio conteúdo do readme para ficar adequado à versão final."*
> A doutrina das casas permanece: o canônico de TRABALHO fica em `A Ponte e o Um\Nós`;
> o `the_boundary` é ESPELHO PÚBLICO — esta ordem delega a você a atualização do espelho.

## 1. O QUE FOI FEITO (o arco 19/08, resumo para o commit)

- **v165→v167**: leitura madura completa; **Coma**: árbitro dos SNe ABERTO por ordem do
  operador (D=98,5±2,2, 13 SNe publicada, verificado por painel adversarial) e o rito
  emitiu sozinho `DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL` (z_TGL=1,30 · z_Planck=5,61);
  promoção editorial do setor Coma (o porquê por-nat; 12→13 SNe).
- **O gate vivo**: `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED` (degrau final;
  6 flags formais por construção Lean; degrau empírico do rito V11).
- **Item A (as 3 condicionais do pacote TGL_SOLDERED_BREUER_HILBERT_PACKAGE) resolvido
  na profundidade máxima da mathlib — 4 pedras Lean novas, 0 sorry, 0 axiom:**
  `EquivariantSection` (v166) · `ErgodicMeanSection` (v167, o LIMITE de Birkhoff) ·
  `SolderSignature` (v167, assinatura (1,3) plena) · `BreuerTrace` (v167, o peso é
  TRAÇO: τ(a*a)=τ(aa*) em B(ℓ²)). O que resta [KNOWN] está NOMEADO nos docstrings.
- Livro-razão da sessão-mãe: artefatos 51_–134_ em `C:\IALD\Artigo\MCMC_V2_RAZAO\`.
- **MCMC**: NÃO precisou ajustar nem rodar de novo (item A é kernel puro; o Nível 2 é
  capítulo FECHADO da folha B: S=N2_INCAPAZ, L=N2_NOT_CONVERGED — não reabrir).

## 2. ONDE ESTÁ O um.py (o artefato canônico, AUTOCONTIDO)

```
C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py
sha256[:16] = 2daf1680d6d35661        (72.832 linhas; v167 FINAL)
```
**Autocontido**: os 164 arquivos do kernel Lean estão EMBUTIDOS no próprio um.py
(ele os materializa em `tgl_kernel/` ao rodar); o LaTeX dos PDFs é gerado de dentro;
β jamais literal. **Dependências de runtime** (documentar no README):
- Python 3 + numpy (obrigatório);
- `elan`/Lean 4 (toolchain `leanprover/lean4:v4.31.0`) + `lake` para a verificação
  formal (o um.py baixa/usa mathlib pinada via lake; sem Lean o rito declara
  `FORMAL_CHECKER_UNAVAILABLE` — fail-closed, nunca finge sucesso);
- `pdflatex` para os PDFs (opcional; sem ele os .tex ficam).
**Como rodar**: `echo 1 | python um.py` (o rito pede a inscrição do UM; "1").
Com a revelação de Coma: variável de ambiente `TGL_COMA_REVEAL=1`.
O reveal do árbitro vive em `Nós\cache\coma_blind\coma_distance_reveal.json`
(incluir no repo — sem ele o confronto fica `LOCKED_AWAITING_REVEAL`).
**Opcional-recomendado incluir também**: `um_podado_v167.py`
(sha256[:16] = eb13a92d35dc8907; 68.542 linhas) — versão sem comentários,
validada por saída idêntica (ver §4).

## 3. OS ARQUIVOS DE RESULTADO (o selo v167 FINAL — copiar TODOS)

Custódia durável em: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\SELO_v167_FINAL\`
(cópias idênticas às vivas em `Nós\`). sha256[:16] de cada um:

| sha256[:16] | arquivo |
|---|---|
| bfaa575f5555542c | rodada_v167_FINAL_stdout.txt (o rito inteiro, selado) |
| bba19f741eb20818 | um_grande_atrator.json (resultado estruturado) |
| 7841ee362265d660 | um_grande_atrator_selo.json (o SELO; result_hash c6cbb74c…) |
| f0f475541047bd27 | um_grande_atrator_manifest.md (hash do mundo) |
| 9ca3dbed4076e06b | um_grande_atrator_forma_canonica.md |
| d6289e51410bb330 | um_grande_atrator_pt.tex |
| 4c80413cab4b7961 | um_grande_atrator_pt.pdf |
| 61ba6ea6c55a1872 | um_grande_atrator_en.tex |
| e5abdee9e249cc87 | um_grande_atrator_en.pdf |

**Os três selos da versão**: um.py `2daf1680d6d35661` · podado `eb13a92d35dc8907` ·
hash do mundo `c6cbb74cd8685d97`. Selo interno: kernel `TGL_KERNEL_STAGE1_VERIFIED`
(164 inalterados) · `FAIL_CLOSED_SELFTEST_PASSED` · gate no degrau final · Coma
`DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL`.

## 4. VALIDAÇÃO DA PODA (para o README)

A comparativa da v167 (podado rodando NA casa, mesmas condições) estava EM CURSO no
fechamento deste handoff — o resultado será anexado abaixo em **§7 ADENDO** pela
sessão-mãe. Precedente v165/v166: saída idêntica exceto a linha do "hash do mundo"
(contém o hash do código — difere por construção). NÃO publicar o podado como
validado antes do adendo confirmar.

## 5. INSTRUÇÕES PARA O the_boundary (a ordem do operador)

1. **Substituir** o um.py antigo pelo `um.py` v167 (e, após o adendo, incluir
   `um_podado_v167.py`); **substituir todos os resultados antigos** pelos 9 arquivos
   do §3; incluir `cache/coma_blind/coma_distance_reveal.json` (o árbitro, com
   proveniência) e, se o repo carrega o protocolo, os JSONs de predição de Coma.
2. **Reindexar os raws do README**: todo link raw/blob aponta para os nomes novos
   (um.py, os PDFs, o selo, o stdout) — nada de links à versão antiga.
3. **Reescrever o README** para a versão final. Conteúdo mínimo:
   - o que é (o artefato canônico da TGL: roda, prova em Lean embutido, gera o
     próprio artigo PT/EN; forma=conteúdo);
   - versão v167 + os três selos (§3) + data 19/08/2026;
   - como rodar (§2, incluindo dependências e TGL_COMA_REVEAL);
   - resultados-chave COM AS RESSALVAS DA RÉGUA (obrigatório, texto sugerido):
     `NOT_FALSIFIED ≠ CONFIRMED`; o veredito de Coma testa o PAR (Planck+defasagem)
     vs (Planck sem defasagem) contra a régua local — consistência, não prova da
     escada; o gate matemático nunca é gateado por cosmologia; a confirmação é do
     OBSERVADOR (FoP em submissão); Lema 3: composto na face finita,
     reduzido ao axioma; na face ∞ as condicionais têm agora pedras de kernel
     (v166/v167) e o que resta [KNOWN] está nomeado.
   - a lista das 4 pedras novas do item A com uma linha cada.
4. **Não incluir**: `tgl_kernel/.lake/` (mathlib baixável), stacks confidenciais
   (`iald_stack_v7.py`, `iald_psion_state.json` — NUNCA, memória da casa), nada do
   Escritório. O CLAUDE.md raiz também não (memória interna).
5. Commit sugerido: `feat(the_boundary): selo v167 — item A em kernel (4 pedras Lean),
   Coma revelada e vencida, leitura madura; substitui um.py e resultados; README
   reindexado` — e conferir hash-a-hash após o push (a régua da Central: custódia).

## 6. CONTEXTO ADICIONAL PARA VOCÊ (sessão irmã)

- O diário completo do arco: `Nós\MEMORIA_DA_LINHAGEM.md` (entradas de 19/08).
- O livro-razão 51_–134_ (cada cunhagem do operador medida fail-closed) em
  `C:\IALD\Artigo\MCMC_V2_RAZAO\` — inclusive 114_/116_ (Coma), 118_ (Lema 3),
  128_ (a anatomia do amor), 133_/134_ (a assinatura final).
- A PROMOÇÃO do canônico é ato do operador — você atualiza o ESPELHO por ordem
  expressa dele (citada no topo); qualquer dúvida de escopo, pergunte a ele.

## 7. ADENDO — COMPARATIVA CONFIRMADA (19/08/2026, sessão-mãe)

- [x] **Comparativa v167 do podado: SAÍDA IDÊNTICA** — 1596/1597 linhas iguais;
  a única divergência é a linha do "hash do mundo" (contém o hash do próprio
  código — difere por construção); `FAIL_CLOSED_SELFTEST_PASSED` também no
  podado. **O `um_podado_v167.py` (eb13a92d35dc8907) está VALIDADO e pode ser
  publicado junto** (stdout da comparativa: `Nós\stdout_podado_v167.txt`).
  Este handoff está COMPLETO — pode executar a ordem do §5.

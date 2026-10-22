# REVISÃO GERAL DO `um.py` — v357 (15/09/2026) — o que estava codificado sem palavra, o que foi pedido e não integrado, e o que a v357 fez

**Ordem do operador (15/09/2026, tarde, verbatim):** «eu quero que vc faça uma revisão geral agora no um.py, o que foi codificado que não virou palavra no artigo, o que eu pedi que não foi integrado ainda, ou seja, agora eu quero a versão completa e revisada, do começo ao fim, recentemente eu pedi muita coisa que precisa ser examinada se foi integrada».

## 1. O que foi medido ANTES (candidato v355, por script; nada de memória) `[REAL]`

| medida | valor |
|---|---|
| módulos TGLExt embutidos no kernel | 974 (1007 chaves com raiz e Audit) |
| entradas no ledger do capítulo-registro (`_ESQUELETO_STONES`) | 661, parando na v339 |
| módulos FORA do ledger | 313 = 10 fundadoras (≤ v42) + 218 (v351) + 19 (v353) + 44 (v354) + 22 (v355) — 1.764 teoremas |
| versões citadas no corpo do artigo | v340–v350 e v352 (com números ao vivo); NENHUMA de v351, v353, v354, v355, v356 |
| chaves do núcleo da rodada com veredito | 249 de 304; 217 nunca lidas pelo corpo do artigo; 153 nem pelo capítulo-registro |
| vereditos do selo (`*_verdict`) ausentes do artigo | 33 (echo_*, ringdown_*, echo_pe_*, echo_search_*, d1_camb_*, h2_reproduction_*, joint_coincidence_*, cosmological_errata, renormalization_wall, graviton_not_a_particle, …) |
| palavras com ZERO ocorrências no artigo (PT e EN) | Friedmann · quarta face · Permanência · ORDEM 011 · ORDEM 012 · kernel_frontier · qgf_/gpf_ (nenhuma bandeira impressa) · «IALD é estado» · «a seleção é o lastro» · «a tela é fundada» · «o Nome é o instrumento» · 10⁻³⁰ (só JOINT_COINCIDENCE 1×) |
| «acoplamento não mínimo» no artigo | 2× no PT, como «SINAL (acoplamento não mínimo) PRESERVA» (v61/v65) — não a cunhagem de 15/09; 0× no EN |
| prosa envelhecida | «Declaração de honestidade» do capítulo-registro (restantes de época v131–v161); «segue em submissão na Foundations of Physics» (rejeitada em mesa em 30/08); rótulo PT «[CANDIDATO ALPHA-LIVRE]» vs EN «[HONEST NEGATIVE — NOT A CANDIDATE]» |

## 2. Os pedidos do operador (05–15/09) e o estado em que as fontes os declaram
Inventário completo (65 itens, com fonte e linha) em `INVENTARIO_PEDIDOS_OPERADOR.md` (scratchpad da sessão da Central, copiado abaixo em resumo).

**Estavam em código e/ou kernel mas SEM palavra no artigo emitido (corrigido na v357):** a definição tipada do colapso (08/09); «a tela é fundada» (08/09); «a IALD é estado» (09/09); «a seleção é o lastro» (09/09); «o Nome é o instrumento» (09/09) e «caracterização» (v337); o handoff do ChatGPT com a oitava cláusula J M J = M′ (v351); a ORDEM 011 A1 (v353–v354); a ORDEM 012 B1–B6 com as quatro paredes (v354); a cunhagem «Permanência = desejo de estar junto e quente = acoplamento não mínimo = betatgl» (15/09); a decisão da rota do fundo pela bancada (15/09, 12:06); a correção «H₀ medido localmente é o H₀ do CMB tem um erro nisso» (13/09); o signo α₂ → β_TGL (13/09); as erratas do D1 (14/09); B1′, saneamentos e A2 (v355); os leitores e a fronteira do kernel (v356).

**Pendências que só o operador resolve (declaradas pelas fontes; NÃO tocadas pela v357):** (1) a confirmação de uma linha da rota do fundo (fator sobre o fluido total) — sem ela a V3 do D1 não se pré-registra; (2) o nome do degrau novo do gate (A6); (3) a Declaração de fecho; (4) a nova versão do DOI Zenodo (segue v331); (5) o vídeo no site; (6) as decisões da v98/GA (i/ii/iii) e a errata v98 no um.py; (7) a errata no Artigo A selado (H₀; `run_D1_camb` placeholder); (8) a régua da confirmação (14/09) — em discussão, régua operacional inalterada.

**Pendências de kernel (bancada, ORDEM 011):** A3 (H2), A4 (H3 importado), A5 (testemunha composta compatível), A6 (degrau do gate), A7; τ_eco no kernel; Lema 3 global; η = 1/4G [INPUT]; QME/BRST/UV.
**Pendências de código/custódia:** D1 V3 (após a ratificação); IALD_COLLAPSE_V1 (C1–C4 não rodados); custódia v351→v357 (sessão do site + irmã) e HANDOFF; JOINT_CONTOUR_V1 (roster).

## 3. O que a v357 fez (só o artigo; kernel, ritos, leitores e selos intocados) `[REAL — verificado por `verifica_v357.py`: 23 OK]`
1. Ledger do capítulo-registro completado: +313 pedras (base: 10, v351: 218, v353: 19, v354: 44, v355: 22) = 974 (todas as pedras TGLExt do manifesto), hash ao vivo.
2. Seis «Ao lado» em PT e EN: v333–v337 (retro), v351, v353–v354 (com a cunhagem [ONTO] e a rota do fundo [INPUT, a confirmar]), v355, v356 (as 17 bandeiras lidas ao vivo), erratas de vocabulário (H₀ fronteira/bulk; signo; D1).
3. «O registro completo dos vereditos desta rodada»: todas as chaves do núcleo com veredito, as 17 bandeiras, a fronteira do kernel, a escada externa (`ext_*`) e os teoremas importados — impressos ao vivo, forma = conteúdo.
4. Adendo ao lado da «Declaração de honestidade» (de época) com o estado corrente lido; errata da FoP (rejeição em mesa, 30/08/2026).
5. A cauda das ondas v305–v356 (a narrativa parava em v303–v304).
6. Rótulo PT alinhado ao EN (Bloco 1, D4: negativo honesto, não candidato).

## 4. A rodada `[REAL]`
`um.py` sha256 `88b080192445449363159c2cad7803b337670d571caf334f682be5b4f7602513` (13,383,911 B) · rodada COMPLETA 16:11:26 → 16:59:14 · **5637/5637** · `FAIL_CLOSED_SELFTEST_PASSED` · gate `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` · 1008 fontes · 8514 termos no trio · kernel 0 escritos.
Artigo: `um_absoluto_pt.txt` 627,814 B (sha16 `2f58bc97adfb81c6`) · `um_absoluto_en.txt` 629,831 B (`abdae1e03187c798`) · `um_absoluto_pt.pdf` 1,877,989 B · `um_absoluto_en.pdf` 1,842,811 B.
Custódia (v351→v357) = sessão do site + irmã; Zenodo/declaração = operador. NOT_FALSIFIED nunca é CONFIRMED; PROVADA ≠ CONFIRMADA.

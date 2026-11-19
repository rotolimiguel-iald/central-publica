APROVADO_COM_RESSALVAS — a T1 finita R3 recompila limpa em cópia minha (RC 0, zero avisos, 13 + 33 teoremas só no trio), os quatro achados T6-05 a T6-08 estão SANADOS, e os dois termos da sonda do T6 entraram byte a byte e dizem o que os nomes dizem. Ressalvas: 2 BAIXO (texto) e 2 INFORMATIVO; nenhuma trava matemática.

# REVISÃO 018 — UNIDADE U5 (revisor Kimi; revisão distinta)

> Unidade: a T1 na face finita, R3 — `candidatas_c1\t1\REV3\T1CompostoFinito.lean` (sha16 `09568333f3f3bbb5`) e
> `candidatas_c1\t1\REV3\T1PontesAoKernel.lean` (sha16 `082efd3467053eb0`). sha256 conferidos por script na entrada:
> `09568333f3f3bbb572cb18130bba4e013242f9ba380d7f53baa5ba2d0dd0de2d` e
> `082efd3467053eb0b7b7c508f96144ed7590305e3651227d8347d133bbb17301`. Batem com os da ordem.
> Revisão distinta: não li `REVISAO_018_U5_Codex.md` nem nada em `revisao_orquestrador\U5_Codex\`. Só leitura fora da
> minha pasta (`revisao_orquestrador\U5_Kimi\`); a recompilação rodou em cópia minha
> (`U5_Kimi\fonte_R3\`), com `compilar_t1.ps1` (o da REV3), `-Deps` primeiro. Nada a provedor remoto; Mapa não
> consultado (não precisei); nada escrito em Nós, um.py, kernel, Chatgpt, espelho, site ou memória.

## Achados (por gravidade)

Nenhum ALTO, nenhum MÉDIO.

1. **(BAIXO)** `T1PontesAoKernel.lean` (REV3) — a palavra "estado" para a matriz de pesos não normalizada:
   cabeçalho l.33-34 e l.424-425, e as docstrings de `conjugacao_e_sigma` (l.378-379),
   `fixo_da_media_sse_fixo_do_fluxo` (l.411-413), `sinal_dos_pesos_e_inversao_do_tempo` (l.449-450) e
   `media_gaussiana_do_sigma_e_dephase` (l.392-393). No kernel, `TGLExt.rhoD d = Matrix.diagonal (fun i => (d i : ℂ))`
   (`tgl_kernel\TGLExt\Ergodicity.lean` l.64), sem normalizar o traço: o objeto é a matriz dos pesos, não o estado (a
   densidade seria `D/Tr D`). Inócuo na matemática — o `sigma` e o `logRho` só veem diferenças de logaritmos, que a
   normalização por escalar não muda — mas o gloss diz mais que o objeto.
   *Conserto:* a nota que a própria gerência já escreveu na REV4 ("Nota sobre a palavra estado",
   `t1\REV4\T1PontesAoKernel.lean`; a REV4 é só texto sobre a REV3, conferi por diff): onde se lê "estado de pesos",
   ler "a matriz diagonal desses pesos, antes de normalizar o traço". Para a REV3 sob revisão, registrar a ressalva.

2. **(BAIXO)** `T1PontesAoKernel.lean` (REV3) l.22: "As sondas adotadas estão copiadas por bytes em
   `sondas_adotadas\`." Vale para as quatro de D3 e de T6 (conferi byte a byte: D3S1Pontes `42ea11f635826e45`,
   D3S2Controles `9d2e0f962a9a331e`, SondaT6T1 `c5e8103fb564bc6b`, SondaT6T1b `3936d974d9471591` — os mesmos sha16
   que o T6 registrou); mas as sondas S3 e S5 do C4, de onde o cabeçalho diz que vêm 19 dos 33 teoremas, NÃO estão na
   pasta. A frase cobre mais que a pasta.
   *Conserto:* a redação que a gerência já pôs na REV4 ("As quatro sondas de D3 e de T6 estão copiadas por bytes em
   `sondas_adotadas\` e pinadas no recibo; as sondas S3 e S5 do C4 não estão copiadas nesta pasta"), ou copiar também
   as S3/S5 com o sha256 lido por script.

3. **(INFORMATIVO)** `T1PontesAoKernel.lean` (REV3) l.34-35 (cabeçalho): "com `e^{−√k}` o fluxo é o mesmo com o tempo
   invertido (`sinal_dos_pesos_e_inversao_do_tempo`), e a média e o fixo não mudam". O FIXO não mudar segue dos dois
   termos adotados (`sinal_dos_pesos_e_inversao_do_tempo` + `fixo_da_media_sse_fixo_do_fluxo`, com `t ↦ −t` bijeção).
   A MÉDIA não mudar pede a simetria da gaussiana centrada sob `s ↦ −s`, que não está em termo no módulo nem nas
   sondas (a sonda do T6 só compilou a igualdade dos fluxos). A frase é a que o T6-07 pediu como TEXTO; está certa, e
   não é termo. *Conserto (se a casa quiser termo):* uma linha sobre `gaussianReal` (simetria da medida centrada);
   não trava a revisão.

4. **(INFORMATIVO)** Cadeia de custódia: a pasta `REV3\` não guarda recibo próprio; o recibo da R3 está em
   `t1\RESULTADO_GERENCIA.json.bak_R3` (16/11 14:19; os dois sha16 da REV3, rc 0, 0 avisos, 13 e 33 teoremas só no
   trio), e o `t1\RESULTADO_GERENCIA.json` vivo (15:52) já aponta para os bytes da REV4
   (`4acd9ef1ff8c7dac…`/`64bbbb948ffbd734…`) e pina as quatro sondas na chave `extras`. Nada errado; fica o registro
   para quem auditar a REV3 saber onde está o recibo dela.

## Os achados T6-05 a T6-08, um a um (o que a ordem pede, com a linha)

- **T6-05 (era BAIXO) — SANADO.** O cabeçalho de `T1PontesAoKernel.lean` l.18-22 agora diz "da S1 do D3, onze; da S2
  do D3, um (`media_zero`); da sonda do T6, dois (`media_e_a_media_do_sigma` e
  `sinal_dos_pesos_e_inversao_do_tempo`). Nenhum teorema deste arquivo é da gerência." — a frase pedida. A persistência
  pedida está cumprida no espírito: as sondas vivem em `t1\sondas_adotadas\` (pasta viva, não temporária), copiadas por
  bytes (hashes acima, conferidos por script meu) e pinadas no recibo (`RESULTADO_GERENCIA.json`, `extras`). O conserto
  pedia a cópia "para o REV2 das duas pastas"; a gerência pôs na pasta viva, sem tocar o registro congelado da REV2 —
  melhor que a letra do pedido. Proveniência conferida por script próprio: os 11 teoremas da S1 são byte a byte os da
  candidata; `media_zero` é o da S2 (mesma prova, `ext i j; rw [media_entrada]; simp [mult]`; só os binders recolhidos
  à seção). Conferi também, por diff REV2→REV3, que a frase velha "Só `media_zero` é da gerência" saiu.
- **T6-06 (era BAIXO) — SANADO.** O item 3 do cabeçalho (l.41-45) ganhou, palavra a palavra, o acréscimo pedido:
  "`esperanca_positiva_pelo_kernel` é caso de `esperanca_posSemidef`; `fixo_sse_specExpect` é `fixo_sse_esperanca` com
  o objeto do kernel; `media_zero` é instância de `dephase_zero`, provada à mão." Os fatos conferem no código:
  `esperanca_positiva_pelo_kernel` (l.435-438) tem a conclusão de `esperanca_posSemidef` (l.471-472) com a hipótese
  `hinj` a mais; `fixo_sse_specExpect` (l.362-365) é `fixo_sse_esperanca` reescrito por `esperanca_e_specExpect`;
  `media_zero` (l.507-511) é provada à mão, e a versão pelo kernel compilou na sonda do T6 (`media_zero_pelo_kernel`,
  SondaT6T1.lean l.78-79).
- **T6-07 (era BAIXO) — SANADO.** Os dois termos entraram: `media_e_a_media_do_sigma` (l.442-447) e
  `sinal_dos_pesos_e_inversao_do_tempo` (l.452-461), byte a byte iguais às sondas (comparação por script: IDÊNTICOS,
  enunciado e prova), compilados só no trio. O texto do item 2 do cabeçalho (l.32-40) ganhou a frase pedida sobre o
  sinal dos pesos. A observação que resta é a do achado 3 acima (a invariância da média não é termo).
- **T6-08 (era BAIXO) — SANADO.** (1) Os rótulos "(Q1)" a "(Q8)" saíram e as docstrings foram acentuadas — o diff
  REV2→REV3 mostra cada troca ("(Q1) fixo de UMA media…" → "Ser fixo por UMA média…", etc.); busca por "(Q" na REV3:
  zero ocorrências. (2) `gerador_e_rhoD`: adotada a segunda via do conserto — a docstring (l.254-256) agora traz "O
  nome do teorema é provisório e diz menos que esta docstring: a igualdade é só de matrizes." (3) Cabeçalhos alinhados:
  `T1CompostoFinito.lean` l.8-10 ("a R2 aplicou os consertos da terceira conferência de 16/11, revisor D3") e
  `T1PontesAoKernel.lean` l.16-17 (C4 = segunda, D3 = terceira); a expressão "consertos da segunda" não aparece mais.

## Os dois termos adotados da sonda do T6 (item 3 da ordem)

- `media_e_a_media_do_sigma` (l.442-447): o nome diz "a média é a média do sigma"; o enunciado diz exatamente isso — a
  entrada `(i, j)` da `mediaGaussiana` da candidata É a integral gaussiana da entrada `(i, j)` do fluxo modular
  `TGLExt.sigma` do kernel no estado de pesos `e^{√k}`. É a ponte de entrada sobre a própria definição, que faltava
  (a R2 só ligava o integrando, por `conjugacao_e_sigma`). Byte a byte a sonda; axiomas: só o trio.
- `sinal_dos_pesos_e_inversao_do_tempo` (l.452-461): o nome diz "o sinal dos pesos é a inversão do tempo"; o enunciado
  diz exatamente isso — o fluxo do estado de pesos `e^{−√k}` no tempo `t` É o do estado de pesos `e^{√k}` no tempo
  `−t`. Byte a byte a sonda; axiomas: só o trio.
- O cabeçalho declarava "os dois do T6 ainda não foram lidos por outro": esta revisão é essa leitura. Lidos,
  recompilados, conferidos contra a sonda e contra o que os nomes dizem. O terceiro termo da SondaT6b
  (`fixo_da_media_sse_fixo_do_fluxo_pesos_decrescentes`) não foi adotado, coerente com o "dois" do cabeçalho.

## O que conferi (com o log da recompilação)

1. **Hashes na entrada** (sha256, `sha256sum`): os dois arquivos da REV3 batem com os sha16 da ordem; a dependência
   `dep_codex\T1GaussianSpectrum.lean` bate com o manifesto (`efe44d21…b07a`).
2. **Recompilação em cópia minha** (`U5_Kimi\fonte_R3\`; `lean.exe` 4.31.0 sobre os `.olean` de `C:\t\k411c\final`;
   nunca `lake`; o script confere o hash do manifesto antes de compilar a dependência). Saída de console:

   ```
   T1GaussianSpectrum           RC 0 |    33 s | sha16 efe44d21ad5da1cb
   T1CompostoFinito             RC 0 |    34 s | sha16 09568333f3f3bbb5
   T1PontesAoKernel             RC 0 |    35 s | sha16 082efd3467053eb0
   ```

   Logs em `U5_Kimi\fonte_R3\build\*.log`. Zero avisos (`grep -ci warning` = 0 nos três logs), zero erros. Busca nas
   fontes: nenhum `sorry`/`admit`/`axiom` fora de comentário.
3. **Axiomas de cada teorema** (saída dos `#print axioms`, que estão nos próprios arquivos): os 7 da dependência do
   Codex, os 13 de `T1CompostoFinito` e os 33 de `T1PontesAoKernel` — TODOS `[propext, Classical.choice, Quot.sound]`,
   inclusive os dois termos novos do T6. Nenhum `sorryAx`, nenhum axioma declarado. As contagens 13 e 33 batem com o
   desenho (DESENHO_v412_R1, item 24: "T1 finita R3, 13 e 33") e com o recibo `.bak_R3`.
4. **Conta da proveniência do cabeçalho**: 15 (S3 do C4) + 4 (S5 do C4) + 11 (S1 do D3) + 1 (`media_zero`, S2 do D3) +
   2 (T6) = 33 teoremas; os 11 da S1 e os 2 do T6 conferidos byte a byte contra as sondas (script meu); `media_zero`
   confere em enunciado e prova com a S2 (só binders recolhidos à seção). As sondas S3/S5 do C4 não estão na pasta
   (achado 2).
5. **Diff REV2→REV3**: em `T1CompostoFinito`, só o cabeçalho mudou (l.8-10), como o próprio cabeçalho declara; em
   `T1PontesAoKernel`, as mudanças são exatamente os consertos do T6 (cabeçalho, docstrings sem rótulo e com acento, a
   nota do nome de `gerador_e_rhoD`) mais os dois termos novos e os dois `#print axioms` deles — nenhuma prova
   pré-existente foi tocada.
6. **Sanidade matemática dos pontos que o T6 não cobriu** (leitura minha): `fixo_da_media_sse_fixo_do_fluxo` usa a
   injetividade de `exp` para trocar `specExpect (exp ∘ √k)` por `specExpect √k` (l.418-422) — correto;
   `a_media_tende_a_esperanca` trata `Real.toNNReal t` para `t < 0` (a média vale a própria matriz; `atTop` esquece) —
   correto; o cabeçalho declara às claras que `Real.sqrt` de negativo vale zero no Lean (l.53-54) — honesto;
   `frequencias_e_logRho` e `gerador_e_rhoD` são `rfl`/uma reescrita sobre `rhoD d = diag d` (kernel, Ergodicity l.64)
   — conferem.
7. **Contexto lido**: o relatório do T6 (`revisao\REVISAO_16nov_R3_T6-…md`, achados 5 a 8) e o `DESENHO_v412_R1.md`
   (item 24). Não li a revisão do Codex desta unidade nem a pasta `U5_Codex\`.

— Kimi, revisor distinto da U5, 16/11/2026. Nada instalado; nada escrito fora de `revisao_orquestrador\U5_Kimi\` e
deste relatório.

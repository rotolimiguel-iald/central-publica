REPROVADO — escopo: só o item 3 da seção 11 do PROVA do tipo III (a causa nomeada para a diferença do objeto compilado não reproduz; a variável medida estava confundida). Aprovadas as duas emendas Lean (código idêntico fora de comentários, consertos exatos) e os itens 1–2 da seção 11.

# REVISÃO 022 — UNIDADE V4 (Kimi, revisor distinto) — conferência das três emendas de texto

> Revisão distinta da unidade V4 da ORDEM 022. Não li nenhum `REVISAO_0**_Codex*.md` nem pastas de outros
> revisores; li os meus da rodada 018 (U3, U4, U5). ORDEM 021 não executada (em espera). Só leitura fora da minha
> pasta (`revisao_orquestrador\V4_Kimi\`); nada editado em pastas `REV*`; nunca `lake build`; compilações só com
> `lean.exe` 4.31.0 (commit 68218e87) sobre os `.olean` de `C:\t\k411c\final`, saídas só na minha pasta. Nenhum
> modelo rodado; nada a provedor remoto. Medidas minhas: [DECLARADO pelo Kimi, com os artefatos em `V4_Kimi\`] até
> a gerência conferir na fonte.

**Material conferido (sha256, prefixo 16, contra a ordem):**

| arquivo | sha16 | ordem |
|---|---|---|
| `candidatas_c1\REV23\CopiadorEImpostor.lean` | `0131be0d68ef1e99` | ✓ bate |
| `candidatas_c1\t1\REV5\T1PontesAoKernel.lean` | `bf38116e0da0f32c` | ✓ bate |
| `candidatas_c1\tipo_iii\REV5\PROVA_E_ALCANCE_GERENCIA.md` | `80bb694a3340955f` | ✓ bate |
| `candidatas_c1\REV19\CopiadorEImpostor.lean` (base) | `0729ab820c049e9a` | = a R8, como a U3 registrou |
| `candidatas_c1\t1\REV4\T1PontesAoKernel.lean` (base) | `64bbbb948ffbd734` | = o que o JSON vivo pinava em 018 |
| `candidatas_c1\tipo_iii\REV4\PROVA_E_ALCANCE_GERENCIA.md` (base) | `1f9011adef951d9e` | = a REV4 vista na 018 |

## Achados (por gravidade)

**M1 (MÉDIO) — A causa que a seção 11, item 3, declara para a diferença do `ErgodicidadeDeMautner.olean` NÃO
reproduz; o "experimento de uma variável" tinha duas variáveis confundidas.**
Arquivo: `candidatas_c1\tipo_iii\REV5\PROVA_E_ALCANCE_GERENCIA.md` l.249.
O item diz: "passando ao Lean o caminho completo da fonte, sai o objeto de 15/11, bit a bit; passando só o nome do
arquivo, a partir da pasta dele, sai o objeto do revisor, bit a bit", e conclui a regra "igualar antes a forma de
passar o nome da fonte". Medida minha de hoje (8 compilações da MESMA fonte `1074aa5b2c172960…`, mesmo lean.exe,
mesmo LEAN_PATH do sandbox, RC 0 e zero avisos em todas; scripts e objetos em `V4_Kimi\`):

| corrida | shell / CWD / forma do nome | objeto |
|---|---|---|
| A | PowerShell, CWD = pasta da fonte, caminho completo | `cf395c3bf9d9c199…`, 1.551.536 B |
| B | PowerShell, CWD = pasta da fonte, nome relativo | `cf395c3bf9d9c199…`, 1.551.536 B |
| C, D | cmd.exe, CWD = pasta da fonte, as duas formas | `cf395c3bf9d9c199…` (as duas) |
| E | ambiente mínimo controlado (ProcessStartInfo), nome relativo | `cf395c3bf9d9c199…` |
| F | CWD = `v412`, caminho completo | `94a247a2c5dea34c…`, 1.551.872 B (NOVO) |
| G | CWD = `C:\IALD`, caminho completo | `a3a47a1a61720ebb…`, 1.553.208 B (NOVO) |
| H | CWD = `C:\IALD\Central de Patentes\work`, caminho completo | `9f1522c7652182a6…`, 1.552.536 B (≠ arquivado) |

Ou seja: com o diretório-raiz fixo, a forma do nome (completo × relativo) NÃO muda nada — cinco corridas, um só
objeto, e ele é o do revisor, não o de 15/11. A "regra que fica" do item 3 é ineficaz: quem a seguir não reproduz
o objeto arquivado. O mecanismo real, medido por inspeção binária dos objetos: (i) o `.olean` embute o nome do
módulo derivado do caminho da fonte RELATIVO ao diretório-raiz do processo — o objeto arquivado contém os
componentes `cadeia_de_selo`, `v412`, `candidatas_c1` (e não `Central de Patentes`), logo a rodada da gerência
rodou com raiz `C:\IALD\Central de Patentes\work` e o módulo embutido é
`cadeia_de_selo.v412.candidatas_c1.ErgodicidadeDeMautner`, não `ErgodicidadeDeMautner`; (ii) a região compactada
embute endereços crus do processo (entre o arquivado e o meu, 32.713 campos de 8 bytes com cara de ponteiro,
delta dominante constante `−0x2f806080000` — realocação por base, não diferença semântica), e esses endereços
dependem de todo o histórico de alocação (linha de comando inteira, inclusive o alvo do `-o`, ambiente etc.) — por
isso nem a corrida H (raiz certa, caminho completo) reproduziu o arquivado. O experimento da gerência (Mapa,
registro 2103, [REAL, medido], hashes batem) é real, mas as duas corridas dele diferiam AO MESMO TEMPO na forma do
nome e na raiz do processo (a forma relativa exige a pasta da fonte como raiz; a forma completa que reproduziu o
objeto de 15/11 exigia a raiz `work`): variáveis confundidas. O que o item 3 tem de verdade e se preserva: os dois
objetos são determinísticos cada qual no seu contexto; nada transiente; a equivalência de interface está medida
desde a 018 (o `TipoIIIUmSoBoost.olean` construído por cima sai bit a bit igual, `0eb51ad10222c62f`).
*Conserto:* reescrever o item 3 assim (ou equivalente): "A causa medida: o `.olean` embute o nome do módulo tal
como derivado do caminho da fonte relativo ao diretório-raiz do processo, e endereços crus da região compactada,
dependentes do contexto exato da invocação. O objeto de 15/11 nasceu de uma compilação com raiz
`C:\IALD\Central de Patentes\work`; o do revisor, com raiz na pasta da fonte. Cada contexto é determinístico;
contextos distintos não reproduzem bit a bit, e a comparação entre contextos é pela equivalência de interface (o
módulo construído por cima sai bit a bit igual — medida do revisor). Regra: só comparar objetos bit a bit dentro
do mesmo contexto de invocação (mesma raiz, mesma linha de comando)." E corrigir o registro 2103 do Mapa na mesma
linha.

**B1 (BAIXO) — Resíduo da mesma expressão que a emenda 2 corrigiu, num terceiro ponto.**
Arquivo: `candidatas_c1\t1\REV5\T1PontesAoKernel.lean` l.326 (docstring de módulo `/-! ## As pontes de
ENTRADA…`): "a matriz das frequências é o `logRho` desse estado (e não o estado `rhoD`)". É a mesma shorthand
("logRho do estado") que a R5 corrigiu no cabeçalho (l.46–47) e na docstring de `gerador_e_rhoD` (l.265–269).
Mitigado pela nota R4 do cabeçalho (l.28–34), que manda ler "estado de pesos" como a matriz `D` antes de
normalizar — mas a frase fica aquém da precisão que a própria R5 adotou.
*Conserto:* "a matriz das frequências é `logRho D`, para a diagonal positiva `D = diag(e^{√k})` (e não a matriz
`rhoD` de pesos `√k`)".

**B2 (BAIXO) — O aviso preexistente da dependência foi declarado na seção 11, não onde quem reproduz lê.**
Arquivo: `candidatas_c1\tipo_iii\REV5\PROVA_E_ALCANCE_GERENCIA.md` l.247. O conteúdo está certo e atribuído
(`TowerWedgeIndex.lean` l.131:6, `change` que não faz nada, fonte do Codex conforme o manifesto, efeito medido do
caminho embutido marcado como [DECLARADO pelo revisor]) — era o meu B4 da U4. Mas o meu conserto pedia a declaração
"na seção 2 do documento"; quem segue a seção 9 ("Como reproduzir") ainda encontra o aviso sem aviso.
*Conserto:* um parêntese na seção 2 (ou na 9) apontando para o item 1 da seção 11.

**B3 (BAIXO) — Custódia: o log da compilação de 15/11 da `ErgodicidadeDeMautner` não existe mais.**
`candidatas_c1\build\ErgodicidadeDeMautner.log` hoje registra a rodada de 16/11 18:29 (a do experimento), tendo
sobrescrito o de 15/11 16:17–16:19 (que a minha U4 citou). O OBJETO sobrevive (mesmo sha256 de 15/11,
`5914fe2f…`), mas o recibo primário da rodada original se perdeu.
*Conserto:* a partir desta rodada, versionar os logs (`*.log.bak_<tag>`) como já se faz com os JSONs.

**I1 (INFORMATIVO) — Recibo da R4 fica implícito.** PROVA REV5 l.248 diz que o `RESULTADO_GERENCIA.json` descreve
a versão corrente e que o da R3 está em `RESULTADO_GERENCIA.json.bak_R3`. Conferido: o JSON vivo (16/11 15:55)
registra os bytes R4 = R5 das duas fontes (`0c28be72…` / `3e7342cb…`, RC 0) e o `.bak_R3` (14:17) registra os da
R3 (`bbce90f3…` / `3e7342cb…`). Como as fontes não mudaram na R5, o recibo da R4 é o próprio JSON vivo — uma
frase dizendo isso fecha a conta de "cada versão".

## Resposta à pergunta única da ordem

1. **Código idêntico fora de comentários e docstrings, nas duas primeiras emendas: SIM, byte a byte.** Método:
   stripper próprio (`V4_Kimi\strip_lean_comments.py`) removendo `-- …`, `/- … -/`, `/-- … -/` e `/-! … -/` com
   profundidade de aninhamento e proteção de literais de string e de char (testado com caso de aninhamento;
   controle negativo: um byte alterado em código é detectado). Sobra de REV19 = sobra de REV23: 50.600 B,
   IDÊNTICAS (também na forma normalizada de 50.256 B). Sobra de t1 REV4 = sobra de t1 REV5: 16.642 B, IDÊNTICAS
   (16.545 B normalizados). O diff integral confirma: 3 hunks no CopiadorEImpostor, todos em prosa de comentário;
   2 hunks no T1PontesAoKernel, um no cabeçalho e um numa docstring.
2. **Cada emenda diz o que o parecer pediu, sem dizer mais?**
   - **CopiadorEImpostor (R9): SIM.** l.1159: o nome que não resolvia virou
     `` `TGLExt.the_reading_fixes_the_code` `` com a nota "(no arquivo `TheImportedExpectation`)" — o nome resolve
     no kernel (`C:\t\k411c\final\TGLExt\TheImportedExpectation.lean` l.194, `namespace TGLExt` em l.91); era o
     achado 1 da minha U3. l.1287–1289: a frase do 0,50 reescrita — agora diz que o termo dá 0,50 na lista
     simétrica, que para os quatro textos do desenho a mesma contagem por linha e por coluna dá 0,50, e aponta "a
     linha 'só a página' da seção 6, em contagens" do desenho R6 (verificado: a linha existe na seção 6,
     `DESENHO_DO_TESTE_R6_GERENCIA.md` l.273, contagens 16, 16, 0, 0); cobre o meu achado 2 e a ponte do meu
     achado 6 da U3. l.1473: o "(a) " saiu da docstring (achado 7). Nada além.
   - **T1PontesAoKernel (R5): SIM, com o residual B1 acima.** Cabeçalho l.46–47: "a matriz das frequências é
     `logRho D`, para a diagonal positiva `D = diag(e^{√k})`, antes de normalizar o traço". Docstring de
     `gerador_e_rhoD` (l.265–269): "identifica, por definição, `diag(√k)` com `rhoD (√k)`…" — exato contra o
     código (`freq k i = (Real.sqrt (k i) : ℂ)`, `T1CompostoFinito.lean` l.100; `rhoD d = Matrix.diagonal …` no
     kernel, Ergodicity.lean l.64; o teorema é `rfl`), conserva a nota do T6-08 ("nome provisório…") sem regressão,
     e a nota R4 do cabeçalho segue intacta. Nada além.
   - **PROVA do tipo III (R5): PARCIAL — falha no item 3 (M1).** O diff REV4×REV5 é só o acréscimo da seção 11
     (l.243–250) mais o marcador de custódia; as duas fontes Lean são byte a byte as da R4 (verificado por hash e
     `cmp`), como a seção declara. Item 1 = o meu B4 ✓ (com o desvio de colocação B2). Item 2 = o meu B5 ✓ (recibos
     conferidos, ver I1). Item 3 = o meu B1 ✗: a investigação foi feita e o registro 2103 existe no Mapa
     (`cadeia.preparacao_v412`, 16/11 18:32, [REAL, medido], hashes corretos), mas a causa nomeada não reproduz —
     ver M1.

## O que conferi (com os diffs e os logs)

1. Hashes de entrada dos seis arquivos (tabela acima).
2. Diff despojado REV19×REV23 e REV4×REV5 (t1): byte a byte idênticos; script, sobras e controles em `V4_Kimi\`.
3. Diff integral dos três pares: os hunks são exatamente os listados; nenhum outro.
4. Nome do kernel verificado no fonte; linha do desenho R6 verificada; `freq` e `rhoD` verificados nos fontes.
5. Recibos do tipo III: `RESULTADO_GERENCIA.json` (corrente, bytes R4=R5) e `RESULTADO_GERENCIA.json.bak_R3`.
6. Mapa consultado (`rotas.py consultar/ver cadeia.preparacao_v412`; o registro 2103 lido — a consulta por número
   "2103" não é o índice do registro; achei pelo nome da rota).
7. Experimento próprio de reprodução do objeto `ErgodicidadeDeMautner.olean`: 8 compilações (tabela do M1),
   scripts `experimento_caminho.ps1`, `experimento_cd.bat`, `experimento_e.ps1`, `experimento_fg.ps1` e saídas em
   `V4_Kimi\expA`…`expH` (RC 0, zero avisos em todas; as saídas trazem só os `#print axioms`, só o trio).
8. Inspeção binária dos objetos (regiões de diferença, padrão de realocação, componentes do nome do módulo
   embutido): script e resultados reproduzíveis a partir dos objetos em `V4_Kimi\`.

Estatutos: compilações e medidas [REAL no sandbox, DECLARADO pelo Kimi até a gerência conferir na fonte — todos os
artefatos em `revisao_orquestrador\V4_Kimi\`]; a leitura dos textos é a do revisor distinto. Nada instalado, nada
escrito fora da minha pasta e deste relatório, nenhum provedor remoto, nenhum modelo rodado.

— Kimi, revisor distinto da V4 (ORDEM 022), 16/11/2026.

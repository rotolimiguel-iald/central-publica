# Pedido de leitura de terceiro ao Codex: as pedras limpas da v413 (20/11/2026)

**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador; a gerência não envia ordem ao Codex. Este pedido substitui, para colar, o pedido curto das correções do Kimi (`PEDIDO_DE_CONFERENCIA_DAS_CORRECOES_v413_20nov.md`), que fica como registro e está contido aqui (item 3).

## O que é

As 21 pedras novas da v413 estão na forma do kernel (`TGLExt.X`). O texto (comentários e docstrings) foi limpo pelo método do operador de 17/11: no `um.py` e no kernel que ele carrega entra só o que é verdade (enunciado, prova, estatuto, limites, fonte conhecida); a história fica no registro paralelo. As regras da limpeza: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\REGRAS_DA_LIMPEZA_v413.md` (sha16 `894416ba928ff72c`). Limparam cinco agentes da gerência; a gerência leu cada diff e fez ajustes. O código de cada módulo é o que você revisou ou a gerência conferiu: sem comentários, idêntico (conferido por script); o fim de linha passou a LF e os imports dos módulos novos a `TGLExt.X`. O conjunto limpo compila numa caixa da v413 (links físicos dos .olean da v412; a caixa da v412 só foi lida), com 274 teoremas públicos, todos com relatório de axiomas só no trio (recibo `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\CONJUNTO_pedras_limpas.json`, sha16 `87a7737cce3d0598`). Manifesto com procedência e hashes: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\MANIFESTO_PEDRAS_v413.json` (sha16 `91925c5d537850e5`).

## O que se pede

Ler o texto de cada pedra limpa ao lado do texto anterior, no diff (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\DIFF_DA_LIMPEZA_v413.txt`, sha16 `9ef5b29fd30661ed`; o diff só mostra texto, porque o código é idêntico), e conferir:

1. que nenhum texto limpo afirma mais do que antes, nem mais do que o enunciado;
2. que nenhum localizador técnico se perdeu com a história (nome de módulo ou de teorema citado, arquivo de fonte, rótulo que distingue um objeto); na v412 a limpeza tirou referência junto com a história, e isso é o que mais se procura aqui;
3. que as quatro pedras do Kimi dizem agora o que os itens 4 a 7 do seu parecer consolidado pediram (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md`, sha16 `9e7d4b93e44cf9fd`): `APonteDeCookLevin` (não é ponte de custo de fita; `mov` é custo cobrado por definição; verifica o custo de uma atribuição dada), `APropostaDaTensao` (`_hA`/`_hB` ociosas; o iff não computa a escolha), `ONomeEBeta` (α definido; nenhum valor numérico; `k` é expoente), `AIdentidadePreservada` (a conjunção final sem a carga; o vetor não é configuração de máquina);
4. que os estatutos ficaram como estavam (`[INPUT]`, `[ONTO]`, `[KNOWN]`, `[OPEN]`, `[REAL]`), e que não sobrou formulação antiga ao lado da vigente;
5. a docstring corrigida de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (item 8 do seu parecer): `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\kernel_edits\TGLExt\OResumoEPsiBit.lean` (sha16 `64440cd179da7a4f`; antes e depois em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\kernel_edits\ERRATA_OResumoEPsiBit.json`, sha16 `1ad803a31a984bfd`).

## Os arquivos

| módulo | pedra limpa (sha16) | origem revisada (sha16) |
|---|---|---|
| `TGLExt.AFronteiraNaLinguaClassica` | `f4cedf991fbf1168` | `b42d1a71bf3daeae` |
| `TGLExt.AIdentidadePreservada` | `a1b79c7e3c5ed745` | `e3640a3650902441` |
| `TGLExt.AMaquinaTM2DaVerificacao` | `b9377b9416520cf8` | `373a2e370a23bd3a` |
| `TGLExt.APonteAoTM2` | `d0552b0eaf224fca` | `47365fc2de4778e4` |
| `TGLExt.APonteDeCookLevin` | `680749038dda954e` | `a561b8e29d33eacd` |
| `TGLExt.APropostaDaTensao` | `15f567469a088f33` | `95be88472a0609d8` |
| `TGLExt.EntregaBeta` | `07fd7fa941642c1a` | `f14470b70e640f14` |
| `TGLExt.LeituraBeta` | `48c891ec3b9baa8a` | `c95265993c53d5d2` |
| `TGLExt.ONomeEBeta` | `178a0c5e586d09fa` | `fd5d0083d5121952` |
| `TGLExt.Operador` | `2f15cf482843e123` | `a504717d4c743fe5` |
| `TGLExt.PonteCookLevin` | `ff67b1cbe801abf8` | `21ed7926e50a39cd` |
| `TGLExt.PonteLeituraBeta` | `b32f1e02e1ab717b` | `9d80c1615a84d183` |
| `TGLExt.QuantizacaoBeta` | `d98979f35a3c155d` | `d98979f35a3c155d` |
| `TGLExt.Reconstrucao` | `c4b332767e090fc2` | `291c8dae898b9ee3` |
| `TGLExt.RelogioBeta` | `efb30b0f85ffd4d6` | `e5b665eca734b370` |
| `TGLExt.SimBase` | `ffef326e6d24343c` | `ffef326e6d24343c` |
| `TGLExt.SimCompleta` | `136448407c64bc71` | `136448407c64bc71` |
| `TGLExt.SimExterior` | `57175184d2a65430` | `57175184d2a65430` |
| `TGLExt.SimLiteral` | `8eb4a3bcf795f9a5` | `8eb4a3bcf795f9a5` |
| `TGLExt.SondaContagem` | `6fc209535076c012` | `35213c3703171906` |
| `TGLExt.Trinity` | `cc64de2d8affde5e` | `61b28885f7e22248` |

Pastas: pedras limpas em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt`; origem em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt`.

## Como e o que devolver

- Não é preciso recompilar; se quiser, compile na caixa da v413 (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\caixa_v413`), com o `LEAN_PATH` começando por ela, depois a caixa da v412 e os pacotes; só `lean.exe`, nunca `lake`.
- Sem instalação, sem alteração de kernel, `um.py`, gate ou publicação; não escreva nas pastas da gerência; consulte o Mapa de Rotas antes e registre depois, numa rota própria.
- Para cada módulo: APROVADA, APROVADA_COM_RESSALVAS (com o texto proposto) ou REPROVADA, com o motivo em até três linhas. Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada arquivo lido.

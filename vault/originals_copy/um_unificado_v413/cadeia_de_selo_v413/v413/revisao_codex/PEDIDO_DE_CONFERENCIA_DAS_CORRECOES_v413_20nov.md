# Pedido de conferência ao Codex: as correções das pedras do Kimi na v413 (curto, opcional)

Gerência c1, 20/11/2026. O operador decide se cola. É conferência de que as correções pedidas foram aplicadas, não revisão nova.

## O que mudou desde o seu parecer

1. As pedras novas da v413 estão na forma do kernel (`TGLExt.X`), compiladas juntas numa caixa da v413 (links físicos dos .olean da v412; a caixa da v412 só foi lida). O texto foi limpo pelo método do operador de 17/11 (no kernel entra só o que é verdade; a história fica no registro paralelo). O código de cada módulo é o revisado, conferido por script (sem comentários, idêntico). Regras da limpeza: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\REGRAS_DA_LIMPEZA_v413.md` (sha16 `894416ba928ff72c`). Manifesto: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\MANIFESTO_PEDRAS_v413.json` (sha16 `ffd8e35df44ee628`).
2. Nas quatro pedras do Kimi, o texto aplica os itens 4 a 7 do seu parecer consolidado (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\PARECER.md`, sha16 `9e7d4b93e44cf9fd`; detalhe em `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\revisao_codex\CODEX_CONSOLIDADO_R3\RESULTADO.json`, sha16 `466e1ba9422498ac`). Os enunciados e as provas não mudaram.

## O que se pede

1. Conferir, em cada uma das quatro, que a docstring diz o que o item pediu, e não mais:
   - `APonteDeCookLevin`: limpa `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt\APonteDeCookLevin.lean` (sha16 `680749038dda954e`); origem revisada `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt\APonteDeCookLevin.lean` (sha16 `a561b8e29d33eacd`).
   - `APropostaDaTensao`: limpa `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt\APropostaDaTensao.lean` (sha16 `15f567469a088f33`); origem revisada `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt\APropostaDaTensao.lean` (sha16 `95be88472a0609d8`).
   - `ONomeEBeta`: limpa `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt\ONomeEBeta.lean` (sha16 `178a0c5e586d09fa`); origem revisada `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt\ONomeEBeta.lean` (sha16 `fd5d0083d5121952`).
   - `AIdentidadePreservada`: limpa `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\pedras_limpas\TGLExt\AIdentidadePreservada.lean` (sha16 `a1b79c7e3c5ed745`); origem revisada `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\origem\TGLExt\AIdentidadePreservada.lean` (sha16 `e3640a3650902441`).
2. Por amostra, no diff da limpeza (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\DIFF_DA_LIMPEZA_v413.txt`, sha16 `58674f73abf76a24`), que nenhum texto limpo fortaleceu uma afirmação dos outros módulos (o diff só mostra texto; o código é idêntico).

Sem instalação, sem alteração de kernel, um.py, gate ou publicação. Não é preciso recompilar: a gerência compilou o conjunto limpo (recibo `C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\insumos\CONJUNTO_pedras_limpas.json`).

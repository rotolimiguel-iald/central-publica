#!/bin/sh
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\copiar_k412c.sh; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# v413 (claude-construtor-v412; derivado para a v413 em 20/11/2026): o sandbox do kernel da v413 = COPIA do sandbox C:\t\k412c\final (ordem da Etapa 1 da v413, item 1: sandbox k413c, nascido do k412c;
# robocopy SEM /PURGE). As fontes .lean de k412c\final foram conferidas por sha256 contra o kernel do NOS v412 SELADO antes da copia (conferir_fontes_k412c_vs_nos_v413.py ->
# CONFERENCIA_FONTES_K412C_v413.json: as fontes comuns todas iguais; nenhum dos nomes novos da v413 existe la', sem caixa; o modulo corrigido igual nos dois). A origem k412c\final e' SO' LIDA.
# Os modulos novos da v413 e o modulo corrigido NAO entram aqui: e' o passo seguinte (preparar_bundle_v413.py). Molde: copiar_k412c.sh (so' os rotulos e a origem sobem).
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k413c\final\.lake\packages -> C:\t\k404c\final\.lake\packages
# (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; a mesma da juncao do k412c). Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k413c.sh   (log em C:\t\k413c\robocopy_final.log; rc 0 se o robocopy devolveu < 8 e a juncao alcanca a mathlib)
mkdir -p /c/t/k413c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k412c\final" "C:\t\k413c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k413c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k413c/final/.lake/packages ]; then
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k413c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k413c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k413c/robocopy_done.txt
echo "OK"

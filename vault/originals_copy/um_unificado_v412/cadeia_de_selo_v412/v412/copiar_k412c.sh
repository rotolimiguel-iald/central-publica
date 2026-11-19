#!/bin/sh
# v412 (17/11/2026, claude-construtor-v412): o sandbox do kernel da v412 = COPIA do sandbox C:\t\k411c\final (DESENHO_v412 secao 1: sandbox k412c, nascido do k411c; ordem da Etapa 1, item 1:
# robocopy SEM /PURGE). As fontes .lean de k411c\final foram conferidas por sha256 contra o kernel do NOS v411 SELADO antes da copia (conferir_fontes_k411c_vs_nos_v412.py ->
# CONFERENCIA_FONTES_K411C_v412.json: 1764 fontes comuns, todas iguais, nada so' num dos lados; nenhum dos 34 nomes da v412 existe la', sem caixa). A origem k411c\final e' SO' LIDA.
# Os 34 modulos da v412 NAO entram aqui: e' o passo seguinte (preparar_bundle_v412.py). Molde: copiar_k411c.sh (so' os rotulos e a origem sobem).
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k412c\final\.lake\packages -> C:\t\k404c\final\.lake\packages
# (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; a mesma da juncao do k411c). Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k412c.sh   (log em C:\t\k412c\robocopy_final.log; rc 0 se o robocopy devolveu < 8 e a juncao alcanca a mathlib)
mkdir -p /c/t/k412c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k411c\final" "C:\t\k412c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k412c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k412c/final/.lake/packages ]; then
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k412c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k412c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k412c/robocopy_done.txt
echo "OK"

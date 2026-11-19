@echo off
rem Experimento C/D: cmd.exe puro, CWD = pasta da fonte; so escreve na pasta do revisor.
set "LEAN_PATH=C:\t\k411c\final\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\aesop\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\batteries\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\importGraph\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\LeanSearchClient\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\mathlib\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\plausible\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\proofwidgets\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\Qq\.lake\build\lib\lean"
set "LEAN=C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe"
set "OUT=C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador\V4_Kimi"
cd /d "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1"
"%LEAN%" -o "%OUT%\expC\ErgodicidadeDeMautner.olean" ErgodicidadeDeMautner.lean > "%OUT%\expC\saida.txt" 2>&1
echo C_RC=%ERRORLEVEL%
"%LEAN%" -o "%OUT%\expD\ErgodicidadeDeMautner.olean" "C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\ErgodicidadeDeMautner.lean" > "%OUT%\expD\saida.txt" 2>&1
echo D_RC=%ERRORLEVEL%

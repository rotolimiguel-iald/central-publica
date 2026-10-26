@echo off
rem ============================================================================================================
rem vigia.bat - o VIGIA da custodia (G1, MODO SOMBRA), 24/10/2026.
rem
rem O que faz: roda "custodiar.py vigiar --gravar" (escreve work\custodia_G1\VIGIA_ULTIMO.json e VIGIA_ULTIMO.txt:
rem versao vista, marcas, codigo, plano resumido, hora) e, SE a versao do selo tem as TRES MARCAS do Nos
rem (marcas=PRONTA), roda "custodiar.py planejar --versao vNNN --seco" e guarda o plano em
rem work\custodia_G1\PLANO_vNNN.json (validado, escrita atomica, backup de bytes se o plano mudou).
rem
rem MODO SOMBRA: este arquivo NUNCA executa e NUNCA publica. Ele nao chama "executar", nao passa "--publicar",
rem "--force", "--sem-guarda" nem "--permitir-ftp-em-claro" e nao le credencial. Ligar "executar --publicar" ao
rem vigia (ou parar em "pronto para publicar" ate N custodias sem erro) e a decisao L17 do operador; a tarefa
rem agendada do Windows e' instalada pela gerencia (ex.: a cada 15 min, "cmd /c vigia.bat").
rem
rem Codigo de saida = o do vigiar: 0 custodiada e sem decisao do operador aberta, 1 pendente, 5 custodiada por G1 com
rem decisoes do operador abertas, 10 em obra (WAIT), 20 incompleta/bloqueada, 30 falha de leitura/escrita, 40 divergencia.
rem Se o plano nao puder ser guardado, sai com 30. 99 = o proprio vigia nao achou o Python ou o custodiar.py.
rem
rem Variaveis opcionais (ensaios): G1_PY, G1_CLI, G1_PASTA (onde ficam VIGIA_ULTIMO.* e PLANO_*.json).
rem Log transitorio do stderr da ultima rodada: %G1_PASTA%\VIGIA_STDERR_ULTIMO.txt (sobrescrito a cada rodada; os
rem registros sao os .json, que tem backup quando mudam).
rem ============================================================================================================
setlocal EnableExtensions
if not defined G1_PY set "G1_PY=C:\Python314\python.exe"
if not defined G1_CLI set "G1_CLI=C:\IALD\Central de Patentes\tools\custodiar.py"
if not defined G1_PASTA set "G1_PASTA=C:\IALD\Central de Patentes\work\custodia_G1"

if not exist "%G1_PY%" goto :sem_python
if not exist "%G1_CLI%" goto :sem_cli
if not exist "%G1_PASTA%" mkdir "%G1_PASTA%"

set "ERR=%G1_PASTA%\VIGIA_STDERR_ULTIMO.txt"
set "PLANO_TMP=%TEMP%\g1_vigia_plano_%RANDOM%%RANDOM%.json"

rem 1) o vigia (so le o Nos e o mundo; grava VIGIA_ULTIMO.*). A vista chave=valor da rodada anterior e' DERIVADA do JSON (regeneravel) e sai antes: se o vigiar
rem    falhar sem gravar, nao ha marcas velhas para o passo 3 usar (fail-closed). O registro (VIGIA_ULTIMO.json) fica, com backup quando muda.
if exist "%G1_PASTA%\VIGIA_ULTIMO.txt" del "%G1_PASTA%\VIGIA_ULTIMO.txt" >nul 2>&1
"%G1_PY%" -X utf8 "%G1_CLI%" vigiar --gravar --saida "%G1_PASTA%" --json > nul 2> "%ERR%"
set "RC_VIGIA=%ERRORLEVEL%"

rem 2) versao e marcas, da vista chave=valor (sem analisar JSON em batch)
set "VER="
set "MARCAS="
if exist "%G1_PASTA%\VIGIA_ULTIMO.txt" (
  for /f "usebackq tokens=1,* delims==" %%A in ("%G1_PASTA%\VIGIA_ULTIMO.txt") do (
    if /i "%%A"=="versao" set "VER=%%B"
    if /i "%%A"=="marcas" set "MARCAS=%%B"
  )
)

set "RC_FINAL=%RC_VIGIA%"
if /i not "%MARCAS%"=="PRONTA" goto :fim
if not defined VER goto :fim

rem 3) as tres marcas presentes: o plano em seco (nada e' escrito pelo planejar; quem grava e' o _guardar_plano)
"%G1_PY%" -X utf8 "%G1_CLI%" planejar --versao %VER% --seco --json > "%PLANO_TMP%" 2>> "%ERR%"
"%G1_PY%" -X utf8 "%G1_CLI%" _guardar_plano --de "%PLANO_TMP%" --para "%G1_PASTA%\PLANO_%VER%.json" --versao %VER% >> "%ERR%" 2>&1
if errorlevel 1 set "RC_FINAL=30"

:fim
if exist "%PLANO_TMP%" del "%PLANO_TMP%" >nul 2>&1
exit /b %RC_FINAL%

:sem_python
echo vigia.bat: Python nao achado em "%G1_PY%" 1>&2
exit /b 99

:sem_cli
echo vigia.bat: custodiar.py nao achado em "%G1_CLI%" 1>&2
exit /b 99

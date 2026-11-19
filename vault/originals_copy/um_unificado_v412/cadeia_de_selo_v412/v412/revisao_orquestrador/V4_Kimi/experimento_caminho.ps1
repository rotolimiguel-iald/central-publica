# Experimento de uma variavel (ORDEM 022, V4, revisor Kimi): mesmo fonte, mesmo lean.exe,
# mesmo LEAN_PATH; varia so a forma de passar o nome da fonte. Saidas so nesta pasta.
$ErrorActionPreference = 'Stop'
$minha = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador\V4_Kimi'
$src = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\ErgodicidadeDeMautner.lean'
$srcdir = Split-Path -Parent $src
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$sandbox = 'C:\t\k411c\final\.lake'
$caminhos = @((Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$env:LEAN_PATH = ($caminhos -join ';')
Write-Output ("LEAN_PATH: " + $env:LEAN_PATH)
Write-Output ("sha256 da fonte: " + (Get-FileHash $src -Algorithm SHA256).Hash.ToLower())

New-Item -ItemType Directory -Force (Join-Path $minha 'expA') | Out-Null
New-Item -ItemType Directory -Force (Join-Path $minha 'expB') | Out-Null

# CWD comum: a pasta da fonte (o Lean exige a fonte contida no diretorio raiz).
# Unica variavel: a forma do argumento (caminho completo X nome relativo).
Push-Location $srcdir
# Modo A: caminho completo da fonte (forma do script da gerencia)
$t0 = Get-Date
$saidaA = & $lean -o (Join-Path $minha 'expA\ErgodicidadeDeMautner.olean') $src 2>&1 | Out-String
$rcA = $LASTEXITCODE
$t1 = Get-Date
Write-Output ("A (caminho completo): RC " + $rcA + " | " + [int]($t1-$t0).TotalSeconds + " s")
[System.IO.File]::WriteAllText((Join-Path $minha 'expA\saida.txt'), $saidaA, (New-Object System.Text.UTF8Encoding($false)))

# Modo B: so o nome do arquivo, a partir da pasta dele (forma do T6-11 / do revisor)
$t2 = Get-Date
$saidaB = & $lean -o (Join-Path $minha 'expB\ErgodicidadeDeMautner.olean') 'ErgodicidadeDeMautner.lean' 2>&1 | Out-String
$rcB = $LASTEXITCODE
$t3 = Get-Date
Pop-Location
Write-Output ("B (nome relativo):    RC " + $rcB + " | " + [int]($t3-$t2).TotalSeconds + " s")
[System.IO.File]::WriteAllText((Join-Path $minha 'expB\saida.txt'), $saidaB, (New-Object System.Text.UTF8Encoding($false)))

$hA = (Get-FileHash (Join-Path $minha 'expA\ErgodicidadeDeMautner.olean') -Algorithm SHA256).Hash.ToLower()
$hB = (Get-FileHash (Join-Path $minha 'expB\ErgodicidadeDeMautner.olean') -Algorithm SHA256).Hash.ToLower()
$sA = (Get-Item (Join-Path $minha 'expA\ErgodicidadeDeMautner.olean')).Length
$sB = (Get-Item (Join-Path $minha 'expB\ErgodicidadeDeMautner.olean')).Length
Write-Output ("A: " + $sA + " B  sha256 " + $hA)
Write-Output ("B: " + $sB + " B  sha256 " + $hB)
Write-Output ("esperado A (arquivado 15/11): 1552864 B  5914fe2ff63bf71b...")
Write-Output ("esperado B (revisor, 018):    1551536 B  cf395c3bf9d9c199...")

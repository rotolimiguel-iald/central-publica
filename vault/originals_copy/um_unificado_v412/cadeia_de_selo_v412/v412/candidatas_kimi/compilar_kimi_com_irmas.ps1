# Compila uma candidata da pasta candidatas_kimi, lendo tambem os .olean das irmas
# (candidatas_c1\build e candidatas_kimi\build). Nunca lake. Formato de log da casa.
# Uso: powershell -File compilar_kimi_com_irmas.ps1 <Nome sem .lean>
param([Parameter(Mandatory = $true)][string]$Nome)
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$fonte = Join-Path $aqui "$Nome.lean"
if (-not (Test-Path $fonte)) { throw "fonte ausente: $fonte" }
if (-not (Test-Path $lean)) { throw "lean.exe ausente" }
$build = Join-Path $aqui 'build'
New-Item -ItemType Directory -Force $build | Out-Null
$caminhos = @((Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$irma_c1 = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\build'
if (Test-Path $irma_c1) { $caminhos += $irma_c1 }
$irma_c1s = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\build_sobre_limpas'
if (Test-Path $irma_c1s) { $caminhos += $irma_c1s }
$caminhos += $build
$env:LEAN_PATH = ($caminhos -join ';')
$log = Join-Path $build "$Nome.log"
$olean = Join-Path $build "$Nome.olean"
$t0 = Get-Date
$saida = & $lean -o $olean $fonte 2>&1 | Out-String
$rc = $LASTEXITCODE
$t1 = Get-Date
$sha = (Get-FileHash $fonte -Algorithm SHA256).Hash.ToLower()
$cab = "FONTE: $fonte`nSHA256: $sha`nLEAN: $(& $lean --version)`nINICIO: $($t0.ToString('yyyy-MM-dd HH:mm:ss'))`nFIM: $($t1.ToString('yyyy-MM-dd HH:mm:ss'))`nRC: $rc`nSAIDA:`n"
[System.IO.File]::WriteAllText($log, $cab + $saida, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ("RC: {0} | {1:N0} s | sha16 {2}" -f $rc, ($t1 - $t0).TotalSeconds, $sha.Substring(0, 16))
Write-Output $saida

# Compila uma candidata local usando lean.exe e os modulos ja verificados da unidade e do sandbox.
# Saida (.olean e log) so' nesta pasta. Uso: powershell -File compilar_candidata.ps1 <Nome sem .lean>
param([Parameter(Mandatory = $true)][string]$Nome)
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$fonte = Join-Path $aqui "$Nome.lean"
if (-not (Test-Path $fonte)) { throw "fonte ausente: $fonte" }
if (-not (Test-Path $lean)) { throw "lean.exe ausente" }
$caminhos = @((Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$build = Join-Path $aqui 'build'
$missao = Split-Path -Parent $aqui
$locais = @($build, $missao, (Join-Path $missao 'Nucleo/build'), (Join-Path $missao 'Espectro'), (Join-Path $missao 'Torre/build'))
$env:LEAN_PATH = (($locais + $caminhos) -join ';')
New-Item -ItemType Directory -Force $build | Out-Null
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
exit $rc

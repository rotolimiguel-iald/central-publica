# Igual a compilar_candidata.ps1, mais uma coisa: le tambem os .olean das candidatas irmas ja' compiladas nesta pasta (build\),
# para a candidata que importa outra candidata da gerencia (por exemplo: import OLeitorEALei). Nunca lake.
# Passa o CAMINHO COMPLETO da fonte ao lean, como o script irmao (a forma do nome muda os bytes do objeto: Mapa de Rotas, 2103).
# Uso: powershell -File compilar_candidata_com_irmas.ps1 <Nome sem .lean>
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

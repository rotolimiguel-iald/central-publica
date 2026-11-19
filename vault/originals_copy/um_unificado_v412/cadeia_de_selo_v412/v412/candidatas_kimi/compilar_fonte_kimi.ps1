# Variante de compilar_kimi_com_irmas.ps1 para fontes em subpasta (REV1, etc.):
# recebe o caminho completo da fonte e o nome do artefato (log/olean em build\). Nunca lake.
# Uso: powershell -File compilar_fonte_kimi.ps1 -Fonte "REV1\Nome.lean" -Nome "Nome_R1"
param([Parameter(Mandatory = $true)][string]$Fonte, [Parameter(Mandatory = $true)][string]$Nome)
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$fonteFull = Join-Path $aqui $Fonte
if (-not (Test-Path $fonteFull)) { throw "fonte ausente: $fonteFull" }
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
$caminhos += $build
$env:LEAN_PATH = ($caminhos -join ';')
$log = Join-Path $build "$Nome.log"
$olean = Join-Path $build "$Nome.olean"
$t0 = Get-Date
$saida = & $lean -o $olean $fonteFull 2>&1 | Out-String
$rc = $LASTEXITCODE
$t1 = Get-Date
$sha = (Get-FileHash $fonteFull -Algorithm SHA256).Hash.ToLower()
$cab = "FONTE: $fonteFull`nSHA256: $sha`nLEAN: $(& $lean --version)`nINICIO: $($t0.ToString('yyyy-MM-dd HH:mm:ss'))`nFIM: $($t1.ToString('yyyy-MM-dd HH:mm:ss'))`nRC: $rc`nSAIDA:`n"
[System.IO.File]::WriteAllText($log, $cab + $saida, (New-Object System.Text.UTF8Encoding($false)))
Write-Output ("RC: {0} | {1:N0} s | sha16 {2}" -f $rc, ($t1 - $t0).TotalSeconds, $sha.Substring(0, 16))
Write-Output $saida

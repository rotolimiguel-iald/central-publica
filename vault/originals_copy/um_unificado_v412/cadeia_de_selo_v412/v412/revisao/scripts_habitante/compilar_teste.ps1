# Compila um arquivo de teste do revisor com lean.exe direto (nunca lake). LEAN_PATH = sandbox k411c + candidatas_c1\build (so leitura).
param([Parameter(Mandatory = $true)][string]$Nome)
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$fonte = Join-Path $aqui "$Nome.lean"
$caminhos = @((Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$caminhos += 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\build'
$env:LEAN_PATH = ($caminhos -join ';')
$log = Join-Path $aqui "$Nome.log"
$t0 = Get-Date
$saida = & $lean $fonte 2>&1 | Out-String
$rc = $LASTEXITCODE
$t1 = Get-Date
[System.IO.File]::WriteAllText($log, "RC: $rc`n$saida", (New-Object System.Text.UTF8Encoding($false)))
Write-Output ("RC: {0} | {1:N0} s" -f $rc, ($t1 - $t0).TotalSeconds)
Write-Output $saida

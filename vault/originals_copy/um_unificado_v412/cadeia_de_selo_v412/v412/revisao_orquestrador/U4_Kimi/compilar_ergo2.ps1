# Compila a ErgodicidadeDeMautner (fonte copiado em ergo\) para build\, so' com lean.exe sobre o sandbox k411c.
# Espelha o LEAN_PATH de compilar_tipo_iii.ps1 (revisor Kimi, U4).
$ErrorActionPreference = 'Continue'
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$caminhos = @((Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$env:LEAN_PATH = ($caminhos -join ';')
Push-Location (Join-Path $base 'ergo2')
try {
  $t0 = Get-Date
  $saida = & $lean -o (Join-Path $base 'build\ErgodicidadeDeMautner_2.olean') 'ErgodicidadeDeMautner.lean' 2>&1 | Out-String
  $rc = $LASTEXITCODE
  $t1 = Get-Date
  $cab = "FONTE: ergo\ErgodicidadeDeMautner.lean`nSHA256: $((Get-FileHash 'ErgodicidadeDeMautner.lean' -Algorithm SHA256).Hash.ToLower())`nINICIO: $($t0.ToString('yyyy-MM-dd HH:mm:ss'))`nFIM: $($t1.ToString('yyyy-MM-dd HH:mm:ss'))`nRC: $rc`nSAIDA:`n"
  [System.IO.File]::WriteAllText((Join-Path $base 'build\ErgodicidadeDeMautner.log'), $cab + $saida, (New-Object System.Text.UTF8Encoding($false)))
  Write-Output ("RC {0} | {1:N0} s" -f $rc, ($t1 - $t0).TotalSeconds)
  Write-Output $saida
} finally { Pop-Location }

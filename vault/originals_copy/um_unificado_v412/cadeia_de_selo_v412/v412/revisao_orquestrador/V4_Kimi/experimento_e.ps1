# Experimento E: ambiente minimo via ProcessStartInfo (sem herdar o bloco de ambiente do shell).
# CWD = pasta da fonte; nome relativo; -o na pasta do revisor. So escrita: V4_Kimi\expE.
$ErrorActionPreference = 'Stop'
$minha = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador\V4_Kimi'
New-Item -ItemType Directory -Force (Join-Path $minha 'expE') | Out-Null
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$psi.WorkingDirectory = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1'
$psi.Arguments = '-o "' + (Join-Path $minha 'expE\ErgodicidadeDeMautner.olean') + '" ErgodicidadeDeMautner.lean'
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
# ambiente minimo deliberado
$psi.EnvironmentVariables.Clear()
$psi.EnvironmentVariables['LEAN_PATH'] = 'C:\t\k411c\final\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\aesop\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\batteries\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\importGraph\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\LeanSearchClient\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\mathlib\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\plausible\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\proofwidgets\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\Qq\.lake\build\lib\lean'
$psi.EnvironmentVariables['SystemRoot'] = 'C:\Windows'
$psi.EnvironmentVariables['TEMP'] = Join-Path $minha 'expE'
$psi.EnvironmentVariables['TMP'] = Join-Path $minha 'expE'
$t0 = Get-Date
$p = [System.Diagnostics.Process]::Start($psi)
$so = $p.StandardOutput.ReadToEnd()
$se = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$t1 = Get-Date
Write-Output ("E (ambiente minimo, nome relativo): RC " + $p.ExitCode + " | " + [int]($t1-$t0).TotalSeconds + " s")
[System.IO.File]::WriteAllText((Join-Path $minha 'expE\saida.txt'), ($so + $se), (New-Object System.Text.UTF8Encoding($false)))
if (Test-Path (Join-Path $minha 'expE\ErgodicidadeDeMautner.olean')) {
  $h = (Get-FileHash (Join-Path $minha 'expE\ErgodicidadeDeMautner.olean') -Algorithm SHA256).Hash.ToLower()
  $s = (Get-Item (Join-Path $minha 'expE\ErgodicidadeDeMautner.olean')).Length
  Write-Output ("E: " + $s + " B  sha256 " + $h)
  Write-Output "alvos: 1552864/5914fe2f... (gerencia)  ou  1551536/cf395c3b... (revisor)"
}

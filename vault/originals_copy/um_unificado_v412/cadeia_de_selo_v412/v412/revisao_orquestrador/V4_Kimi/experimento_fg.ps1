# Experimentos F/G: varia o CWD (raiz do Lean) mantendo caminho absoluto da fonte.
# F: CWD = v412 (ancestral). G: CWD = C:\IALD (ancestral). So escrita: V4_Kimi\expF, expG.
$ErrorActionPreference = 'Stop'
$minha = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador\V4_Kimi'
$src = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\ErgodicidadeDeMautner.lean'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
$env:LEAN_PATH = 'C:\t\k411c\final\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\aesop\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\batteries\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\importGraph\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\LeanSearchClient\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\mathlib\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\plausible\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\proofwidgets\.lake\build\lib\lean;C:\t\k411c\final\.lake\packages\Qq\.lake\build\lib\lean'
New-Item -ItemType Directory -Force (Join-Path $minha 'expF') | Out-Null
New-Item -ItemType Directory -Force (Join-Path $minha 'expG') | Out-Null

Push-Location 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412'
$t0 = Get-Date
$sF = & $lean -o (Join-Path $minha 'expF\ErgodicidadeDeMautner.olean') $src 2>&1 | Out-String
$rcF = $LASTEXITCODE
Pop-Location
$t1 = Get-Date
Write-Output ("F (CWD=v412, caminho abs): RC " + $rcF + " | " + [int]($t1-$t0).TotalSeconds + " s")
[System.IO.File]::WriteAllText((Join-Path $minha 'expF\saida.txt'), $sF, (New-Object System.Text.UTF8Encoding($false)))

Push-Location 'C:\IALD'
$t2 = Get-Date
$sG = & $lean -o (Join-Path $minha 'expG\ErgodicidadeDeMautner.olean') $src 2>&1 | Out-String
$rcG = $LASTEXITCODE
Pop-Location
$t3 = Get-Date
Write-Output ("G (CWD=C:\IALD, caminho abs): RC " + $rcG + " | " + [int]($t3-$t2).TotalSeconds + " s")
[System.IO.File]::WriteAllText((Join-Path $minha 'expG\saida.txt'), $sG, (New-Object System.Text.UTF8Encoding($false)))

foreach ($x in 'F','G') {
  $f = Join-Path $minha ("exp" + $x + "\ErgodicidadeDeMautner.olean")
  if (Test-Path $f) {
    Write-Output ($x + ": " + (Get-Item $f).Length + " B  sha256 " + (Get-FileHash $f -Algorithm SHA256).Hash.ToLower())
  } else { Write-Output ($x + ": sem objeto") }
}
Write-Output "alvos: 1552864/5914fe2f... (gerencia)  ou  1551536/cf395c3b... (revisor)"

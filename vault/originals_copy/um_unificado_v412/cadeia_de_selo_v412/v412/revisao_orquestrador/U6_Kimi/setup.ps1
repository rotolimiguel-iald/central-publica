$ErrorActionPreference = 'Stop'
$rev = 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao_orquestrador'
$meu = Join-Path $rev 'U6_Kimi'
New-Item -ItemType Directory -Force $meu | Out-Null

$hRaiz  = (Get-FileHash -Algorithm SHA256 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\PsionVacuoEModoDoTratado.lean').Hash
$hRev17 = (Get-FileHash -Algorithm SHA256 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV17\PsionVacuoEModoDoTratado.lean').Hash
Write-Output "raiz : $hRaiz"
Write-Output "rev17: $hRev17"
Write-Output "iguais: $($hRaiz -eq $hRev17)"

Copy-Item 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\compilar_candidata.ps1' $meu -Force
Copy-Item 'C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\candidatas_c1\REV17\PsionVacuoEModoDoTratado.lean' $meu -Force
Get-ChildItem $meu | Select-Object Name, Length | Format-Table -AutoSize

$f = 'C:\IALD\Central de Patentes\work\vitrine_postura_13nov\rodada_b\consolidacao_das_falas\CONSOLIDACAO_DAS_FALAS_DO_PSION_16nov.md'
if (Test-Path $f) {
  $i = Get-Item $f
  $h = (Get-FileHash -Algorithm SHA256 $f).Hash.ToLower()
  Write-Output ("bytes: " + $i.Length)
  Write-Output ("sha256: " + $h)
} else { Write-Output 'AUSENTE' }

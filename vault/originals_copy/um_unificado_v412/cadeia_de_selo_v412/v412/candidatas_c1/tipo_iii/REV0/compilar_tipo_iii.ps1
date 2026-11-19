# Compila, com o binario lean.exe direto (nunca lake), a candidata da gerencia do tipo III.
# -Deps: compila as doze fontes do Codex copiadas em dep_codex\ (na ordem das dependencias) para build\.
# -Nome <modulo>: compila <modulo>.lean desta pasta para build\ (as dependencias ja' tem de estar em build\).
# Le so' os .olean do sandbox k411c e os de build\. Saida so' nesta pasta.
param([switch]$Deps, [string]$Nome = '')
$ErrorActionPreference = 'Stop'
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$sandbox = 'C:\t\k411c\final\.lake'
$lean = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
if (-not (Test-Path $lean)) { throw 'lean.exe ausente' }
$build = Join-Path $aqui 'build'
New-Item -ItemType Directory -Force $build | Out-Null
# build\ desta pasta; depois o build\ das outras candidatas da gerencia (so' para TipoIIIUmSoBoost, que usa ErgodicidadeDeMautner)
$caminhos = @($build, (Join-Path (Split-Path -Parent $aqui) 'build'), (Join-Path $sandbox 'build\lib\lean'))
foreach ($p in Get-ChildItem (Join-Path $sandbox 'packages') -Directory) {
  $d = Join-Path $p.FullName '.lake\build\lib\lean'
  if (Test-Path $d) { $caminhos += $d }
}
$env:LEAN_PATH = ($caminhos -join ';')

function Compilar([string]$fonte) {
  $nome = [IO.Path]::GetFileNameWithoutExtension($fonte)
  $olean = Join-Path $build "$nome.olean"
  $log = Join-Path $build "$nome.log"
  $sha = (Get-FileHash $fonte -Algorithm SHA256).Hash.ToLower()
  $t0 = Get-Date
  $saida = & $lean -o $olean $fonte 2>&1 | Out-String
  $rc = $LASTEXITCODE
  $t1 = Get-Date
  $cab = "FONTE: $fonte`nSHA256: $sha`nLEAN: $(& $lean --version)`nINICIO: $($t0.ToString('yyyy-MM-dd HH:mm:ss'))`nFIM: $($t1.ToString('yyyy-MM-dd HH:mm:ss'))`nRC: $rc`nSAIDA:`n"
  [System.IO.File]::WriteAllText($log, $cab + $saida, (New-Object System.Text.UTF8Encoding($false)))
  Write-Output ("{0,-28} RC {1} | {2,5:N0} s | sha16 {3}" -f $nome, $rc, ($t1 - $t0).TotalSeconds, $sha.Substring(0, 16))
  if ($rc -ne 0 -or -not (Test-Path $olean)) { Write-Output $saida; throw "falhou: $nome" }
  return $saida
}

if ($Deps) {
  $man = Get-Content (Join-Path $aqui 'dep_codex\MANIFESTO_DEP_CODEX.json') -Raw -Encoding utf8 | ConvertFrom-Json
  foreach ($m in $man.ordem) {
    $f = Join-Path $aqui "dep_codex\$m.lean"
    $esperado = $man.arquivos."$m.lean".sha256
    if ((Get-FileHash $f -Algorithm SHA256).Hash.ToLower() -ne $esperado) { throw "hash diferente do manifesto: $m" }
    Compilar $f | Out-Null
  }
}
if ($Nome -ne '') {
  $f = Join-Path $aqui "$Nome.lean"
  if (-not (Test-Path $f)) { throw "fonte ausente: $f" }
  $s = Compilar $f
  Write-Output $s
}

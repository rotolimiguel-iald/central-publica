param([Parameter(Mandatory)][string]$Destination, [switch]$Observers)
$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $PSScriptRoot
$build = 'C:/t/k411c/final/.lake'
$lean = 'C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe'
if(Test-Path -LiteralPath $Destination){throw 'Choose a new directory'}
$dest=[IO.Directory]::CreateDirectory($Destination).FullName
$paths=@($dest,"$build/build/lib/lean")
foreach($package in Get-ChildItem "$build/packages" -Directory){
  $path=Join-Path $package.FullName '.lake/build/lib/lean'
  if(Test-Path -LiteralPath $path){$paths += $path}
}
$env:LEAN_PATH=$paths -join ';'
$stages=@('Torre/TowerWedgeIndex','Horizonte/WedgeHorizonObserver','VinculoCriterion','Espectro/FockCharacters','Nucleo/PhysicalCoreCenter','Nucleo/PhysicalCoreMultipliers','Nucleo/PhysicalCoreFactor','Espectro/WedgeFactor','Classificacao')
if($Observers){$stages += 'Horizonte/TransportCenter','Horizonte/TransportPair','Horizonte/ObserverClassification'}
foreach($st in $stages){
  $src=Get-Item -LiteralPath "$base/$st.lean"
  $obj=Join-Path $dest ($src.BaseName+'.olean')
  $pin=(Get-FileHash -LiteralPath $src.FullName).Hash
  $out = & $lean -R $src.DirectoryName -o $obj $src.FullName 2>&1
  $rc=$LASTEXITCODE
  [IO.File]::WriteAllLines([IO.Path]::ChangeExtension($obj,'.log'),[string[]]$out)
  if($rc -ne 0 -or $pin -ne (Get-FileHash -LiteralPath $src.FullName).Hash -or -not(Test-Path -LiteralPath $obj)){throw "Failed: $st rc=$rc"}
  Write-Output "$st $pin"
}

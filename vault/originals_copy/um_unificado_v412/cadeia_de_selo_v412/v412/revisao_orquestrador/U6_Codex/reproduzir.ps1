$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    & './compilar_candidata.ps1' -Nome 'PsionVacuoEModoDoTratado'
    $firstLog = Get-Content -Raw -Encoding UTF8 -LiteralPath 'build/PsionVacuoEModoDoTratado.log'
    if ($firstLog -notmatch '(?m)^RC: 0\r?$') { throw 'Falha na compilação da R0' }
    $env:LEAN_PATH = (Join-Path $PSScriptRoot 'build') + ';' + $env:LEAN_PATH
    $lean = 'C:/Users/rotol/.elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe'
    foreach ($probe in @('ReviewProbe', 'ReviewRoute')) {
        $output = & $lean ($probe + '.lean') 2>&1
        $code = $LASTEXITCODE
        $output | Out-File -Encoding utf8 -LiteralPath ('./build/' + $probe + '.log')
        if ($code -ne 0) { throw "Falha na sonda $probe (RC $code)" }
    }
    & 'C:/Python314/python.exe' -B -X utf8 './audit_u6.py'
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao conferir os recibos ou as fontes' }
} finally {
    Pop-Location
}

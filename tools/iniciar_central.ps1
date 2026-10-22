# Central de Patentes TGL — launcher: sobe o backend (se preciso) e abre o navegador.
# CONSERTO 17/07/2026: uvicorn sob pythonw.exe (sem console/stdout) CRASHAVA em silêncio no
# boot do logging — o servidor nunca subia e o atalho "não funcionava". A cura é REDIRECIONAR
# stdout/stderr para um log; com isso o pythonw sobe e permanece. (Diagnóstico: python.exe com
# saída redirecionada subia; pythonw sem redirecionar, não.) Ver backend/logs/uvicorn*.log.
$ErrorActionPreference = 'SilentlyContinue'
$central = 'C:\IALD\Central de Patentes'
$py = Join-Path $central 'backend\.venv\Scripts\pythonw.exe'
$url = 'http://127.0.0.1:8765'
$logDir = Join-Path $central 'backend\logs'
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$outLog = Join-Path $logDir 'uvicorn.out.log'
$errLog = Join-Path $logDir 'uvicorn.err.log'

function Test-Up {
  try { return (Invoke-WebRequest -UseBasicParsing "$url/api/health" -TimeoutSec 2).StatusCode -eq 200 }
  catch { return $false }
}

if (-not (Test-Up)) {
  # O redirecionamento é o que faz o pythonw funcionar (sem ele, uvicorn morre sem stdout).
  Start-Process -FilePath $py `
    -ArgumentList '-m', 'uvicorn', 'backend.app.main:app', '--host', '127.0.0.1', '--port', '8765' `
    -WorkingDirectory $central -WindowStyle Hidden `
    -RedirectStandardOutput $outLog -RedirectStandardError $errLog
  for ($i = 0; $i -lt 40; $i++) { Start-Sleep -Milliseconds 400; if (Test-Up) { break } }
}

if (Test-Up) {
  Start-Process $url
} else {
  # Falha honesta: se não subiu, abre o log do erro em vez de uma tela morta no navegador.
  if (Test-Path $errLog) { Start-Process notepad.exe $errLog }
}

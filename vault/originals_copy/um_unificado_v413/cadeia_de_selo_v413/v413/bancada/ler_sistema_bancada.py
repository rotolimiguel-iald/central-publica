# -*- coding: utf-8 -*-
"""Diagnostico da Bancada (20/11/2026). SO LEITURA do sistema operacional, por PowerShell sem perfil: o ultimo boot, os eventos de
desligar/reiniciar desde 12/11 (System 1074/6005/6006/6008/41), as falhas de python entre o ultimo religamento conhecido (13/11 03:55)
e o boot de 16/11 (Application 1000/1001), os processos cuja linha de comando cita um_bancada/mcp_um/abrir_bancada, a escuta na porta
18777 e qualquer inicio automatico (tarefa agendada, pasta Inicializar, chave Run do usuario) que cite a Bancada.
Nao toca o treino da placa, nao consulta a placa, nao liga nem para nada. Imprime; quem chama redireciona."""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
PS = r"""
$ErrorActionPreference = 'Continue'
'== ultimo boot: ' + (Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('yyyy-MM-dd HH:mm:ss')
'== agora: ' + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
'== System 1074/6005/6006/6008/41 desde 2026-11-12'
try { Get-WinEvent -FilterHashtable @{LogName='System'; Id=@(1074,6005,6006,6008,41); StartTime=(Get-Date '2026-11-12')} -ErrorAction Stop | Sort-Object TimeCreated | ForEach-Object { $m = ($_.Message -replace '\s+',' '); '{0} | Id {1} | {2}' -f $_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss'), $_.Id, $m.Substring(0, [Math]::Min(200, $m.Length)) } } catch { 'erro: ' + $_.Exception.Message }
'== Application 1000/1001 com python entre 2026-11-13 03:50 e 2026-11-16 14:00'
try { $e = Get-WinEvent -FilterHashtable @{LogName='Application'; Id=@(1000,1001); StartTime=(Get-Date '2026-11-13 03:50'); EndTime=(Get-Date '2026-11-16 14:00')} -ErrorAction Stop | Where-Object { $_.Message -match 'python' }; if ($e) { $e | ForEach-Object { $m = ($_.Message -replace '\s+',' '); '{0} | Id {1} | {2}' -f $_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss'), $_.Id, $m.Substring(0, [Math]::Min(200, $m.Length)) } } else { 'nenhum' } } catch { 'erro/nenhum: ' + $_.Exception.Message }
'== processos que citam um_bancada / mcp_um / abrir_bancada'
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'um_bancada|mcp_um|abrir_bancada' } | ForEach-Object { '{0} | {1} | criado {2} | {3}' -f $_.ProcessId, $_.Name, $_.CreationDate.ToString('yyyy-MM-dd HH:mm:ss'), $_.CommandLine }
'== escuta na porta 18777'
$c = Get-NetTCPConnection -LocalPort 18777 -ErrorAction SilentlyContinue; if ($c) { $c | ForEach-Object { '{0} {1} pid {2}' -f $_.LocalAddress, $_.State, $_.OwningProcess } } else { 'nenhuma' }
'== tarefas agendadas que citam a Bancada'
$t = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object { $_.TaskName -match 'ancada|18777' -or ((($_.Actions | ForEach-Object { [string]$_.Execute + ' ' + [string]$_.Arguments }) -join ' ') -match 'ancada') }; if ($t) { $t | ForEach-Object { $_.TaskPath + $_.TaskName + ' | ' + $_.State } } else { 'nenhuma' }
'== pasta Inicializar do usuario'
Get-ChildItem ($env:APPDATA + '\Microsoft\Windows\Start Menu\Programs\Startup') -ErrorAction SilentlyContinue | ForEach-Object { $_.Name }
'== HKCU Run que cita a Bancada'
$r = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -ErrorAction SilentlyContinue; $hit = $r.PSObject.Properties | Where-Object { [string]$_.Value -match 'ancada' }; if ($hit) { $hit | ForEach-Object { $_.Name + ' = ' + $_.Value } } else { 'nenhuma' }
"""
r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", PS], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
print(r.stdout.rstrip())
if r.stderr.strip():
    print("== stderr do PowerShell (registro)")
    print(r.stderr.strip()[-2000:])
print("== rc do PowerShell:", r.returncode)

' Wrapper silencioso: roda o launcher PowerShell escondido (sem piscar console).
Set sh = CreateObject("WScript.Shell")
sh.Run "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""C:\IALD\Central de Patentes\tools\iniciar_central.ps1""", 0, False

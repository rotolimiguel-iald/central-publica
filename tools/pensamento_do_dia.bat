@echo off
rem O pensamento do dia da IALD no X (ordem do operador de 23/10/2026): gera o texto, anota no LIVRO e enfileira ao Codex. Tarefa diaria 17:30 (Goiania).
cd /d "C:\IALD\Central de Patentes"
"C:\Python314\python.exe" -X utf8 "C:\IALD\Central de Patentes\tools\pensamento_do_dia.py" >> "C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\X_DIARIO\_tarefa_log.txt" 2>&1

#!/bin/sh
# [DERIVADO v413, 20/11/2026, Etapa 3 da v413 (construtor da Etapa 3, a servico da gerencia c1)] de v412\rito_v412.sh por etapa3\derivar_rito_e_carimbo_v413.py: o corpo e' o do molde
# (generico); mudam este cabecalho, os rotulos, o PORTAO DO PILAR antes de qualquer parada, a placa que NAO se mede e o VIGIA DO PILAR durante o rito (trocas e diff em etapa3\DERIVACAO_RITO_v413.json).
# O RITO v413 (ato da gerencia c1): roda o um.py v413 instalado no Nos (instalar_v413.py) -- 21 MODULOS NOVOS de kernel e UM modulo CORRIGIDO (TGLExt/OResumoEPsiBit.lean, so' a docstring; o
# um.py materializa o corpo embutido em tgl_kernel\TGLExt: os novos, o corrigido por cima do antigo e a raiz TGLExt.lean com os imports novos), 712 bandeiras novas e os registros por especificacao ponte_cook_levin_v413, trinity_v413, operador_v413, identidade_preservada_v413, cunhagens_v413,
# com as palavras de veredito do contrato R1; os registros anteriores sao RECRIADOS; nenhuma chave antiga muda fora dos numeros; o gate nao se move; o teste H0DN x BG1 nao se reabre.
# O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (75dc30bc9cc8d330e31f99ca, a mesma da v412; _QP_REUSE_V386); TGL_RITE_CHECKPOINT DESLIGADO. HA TREINO EM CURSO NA PLACA (C:\IALD\TGL_IALD_NATIVE_QWEN5090):
# NAO TOCAR, NAO MEDIR, NAO PARAR. Por isso: (a) o PORTAO DO PILAR (portao_ambiente_pilar_v413.py, com o mesmo python do um.py) confere, ANTES de qualquer parada e sem tocar a placa, que o
# ambiente que o um.py vai sondar (torch, cuda, numpy, scipy, python, nome da placa) e' o do cache; senao NAO RODO (19; ilegivel: 21) e a gerencia avisa o operador; (b) a VRAM nao e' lida e as
# recusas 11/12 do molde saem (com o treino na placa elas sempre recusariam); (c) o VIGIA DO PILAR le o stdout canonico e, se o um.py anunciar o CALCULO do pilar (o autoteste do motor, que o
# um.py roda na placa mesmo no reuso, pode falhar por memoria) ou o reuso com outra chave, grava PILAR_PARADA_v413.txt e manda TERM ao lancador (encerra a arvore do um.py; RITO_RC=SINAL_TERM).
# O que o portao NAO decide: o autoteste do motor (E1..E8), curto, que o um.py roda na placa no reuso; esse toque e' do proprio um.py (PORTAO_DO_PILAR_v413.json) e o vigia cobre a falha dele.
# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v413_stdout.txt (o carimbador grava o tempo de cada linha no pacote), trailer RITO_RC=<rc>. RODADA COMPLETA.
# O SERVIDOR DO MODELO NATIVO (molde): a tarefa «IALD Llama Server» e o supervisor sao PARADOS antes SE estavam ligados (estado lido pela tarefa e pelo processo; sonda vazia conta como ligado),
# VIGIADOS durante e RELIGADOS no fim se estavam ligados -- mesmo se o rito falhar ou o lancador receber TERM/HUP/INT; o marcador .servidor_parado_pelo_rito fica no pacote enquanto parado.
# ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v413.pid) NO GIT BASH (o PID do MSYS), conferindo antes /proc/<pid>/cmdline com rito_v413. Codigos de recusa do molde: 6-10, 13-18; novos: 19, 21.
# TEMPO ESPERADO (v413, lido de kernel\construir_marcas.txt do build A FRIO no sandbox k413c e conferido com kernel\KH_N1_v413.json): 22 modulos (os novos e o corrigido) e o lake build em 765 s, o Audit em 265 s.
# No Nos o kernel da v412 ja' esta' compilado em .lake/build: o rito compila os novos, o corrigido e os 96 dependentes antigos dele (BUNDLE_v413.json), a raiz e o Audit; o lake build do um.py tem
# tempo-limite de 3600 s (lido do um.py); a rodada da v412 levou 2 h 02 min (v412\rito_horarios_v412.txt). Se o lake build estourar o tempo-limite (licao v372), a verificacao do kernel sai FAILED
# com rc 0: o conferidor reprova (escada e linha do kernel) e a rodada seguinte, com o cache quente, fecha; preservar o stdout e a captura da que estourou.
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
STOPPS="C:\\IALD\\projetos_pyhton\\IALD\\stop_iald_llama.ps1"
MARCA="$PK/.servidor_parado_pelo_rito"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
cd "$NOS" || exit 9
# a guarda do marcador da rodada ANTERIOR (v412): se a v412 deixou o servidor parado (marcador no pacote dela), a gerencia o resolve antes -- NAO RODO.
# A lista traz o pacote da v412 e a pasta desta cadeia (v413); ao subir de versao (v412->v413) a lista segue valida: a pasta da cadeia anterior existe. Ao menos uma tem de existir.
set -- "/c/IALD/Central de Patentes/work/cadeia_de_selo/v412" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v413"
GUARDAS="$*"
GUARDA_LIDA=0
for PKG in "$@"; do
  if [ "$PKG" != "$PK" ] && [ -d "$PKG" ]; then   # a pasta desta propria rodada (PK) tem a guarda propria mais adiante (restauracao do marcador)
    GUARDA_LIDA=1
    [ -f "$PKG/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado ($(cat "$PKG/.servidor_parado_pelo_rito")) em $PKG -- resolva-o antes -- NAO RODO"; exit 18; }
  fi
done
[ "$GUARDA_LIDA" = 1 ] || { echo "nenhuma pasta de guarda do marcador existe ($GUARDAS): a guarda nao pode ser lida -- NAO RODO"; exit 18; }   # afericao A7
LOGS="$PK/rito_servidor_v413.log"
log() { echo "$(date +%H:%M:%S) $*" | tee -a "$LOGS"; }
h=$(python -c "import hashlib;print(hashlib.sha256(open('um.py','rb').read()).hexdigest()[:16])")
e=$(python -c "import json;print(json.load(open('C:/IALD/Central de Patentes/work/cadeia_de_selo/v413/ESPERADOS_v413.json',encoding='utf-8'))['candidato_sha16'])")
[ "$h" = "$e" ] || { echo "um.py do disco ($h) != candidato esperado ($e) -- NAO RODO"; exit 8; }
v=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | Where-Object { \$_.CommandLine -ne \$null -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'VIGIA_OK'" 2>&1) || { echo "vigia de processos FALHOU: $v -- NAO RODO"; exit 7; }
echo "$v" | grep -q "VIGIA_OK" || { echo "vigia sem VIGIA_OK: $v -- NAO RODO"; exit 7; }
n=$(echo "$v" | grep -c -E '^[0-9]+\s*$'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }
# o PORTAO DO PILAR (v413): o ambiente que o um.py vai sondar tem de ser o do cache do pilar (senao o um.py CALCULARIA o pilar na placa, onde ha treino em curso):
# NAO toca a placa; recusa = PARAR e avisar o operador (19); ilegivel = PARAR (21). Roda com o MESMO python do um.py, sem -I (os mesmos pacotes).
pp_=$(python "$PK/portao_ambiente_pilar_v413.py" "$PK/ESPERADOS_v413.json" 2>&1); prc_=$?
echo "$pp_" | tail -3
[ "$prc_" = "0" ] || { echo "o portao do pilar recusou (rc $prc_): o ambiente da placa nao e' o do cache, ou nao se leu -- NAO RODO; avisar o operador"; [ "$prc_" = "19" ] && exit 19; exit 21; }
# outro LANCADOR vivo (ainda sem um.py, por exemplo na parada do servidor): recusar ANTES de qualquer parada ou dos orfaos (7a afericao)
PID_VELHO=""
if [ -f "$PK/.rito_v413.pid" ]; then
  op_=$(cat "$PK/.rito_v413.pid" 2>/dev/null)
  if [ -n "$op_" ] && kill -0 "$op_" 2>/dev/null && grep -q "rito_v413" "/proc/$op_/cmdline" 2>/dev/null; then echo "OUTRO lancador do rito v413 esta VIVO (PID $op_) -- NAO RODO"; exit 16; fi
  PID_VELHO="$op_"
fi
# a VEZ: o PID deste lancador gravado JA (antes da fase 0) e removido em qualquer saida antecipada; armada a restauracao, so sai no FIM dela (8a e 9a)
echo $$ > "$PK/.rito_v413.pid"
trap 'rm -f "$PK/.rito_v413.pid"' EXIT
# a fase 0 escreve num log PROPRIO; o log real (e o registro dos sinais) so gira depois da ULTIMA recusa (8a afericao)
LOGF="$LOGS"; LOGS="$PK/rito_servidor_v413.log.fase0"
# o .fase0 de tentativas ANTERIORES (recusadas) e' ACRESCENTADO ao .fase0.anterior, com separador datado, antes de ser zerado -- nada se perde (9a e 10a)
if [ -f "$LOGS" ]; then { echo "== tentativa anterior (acrescentada em $(date '+%Y-%m-%d %H:%M:%S')) =="; cat "$LOGS"; } >> "$LOGS.anterior" || { echo "FALHA VISIVEL: o .fase0 da tentativa anterior nao foi guardado -- NAO RODO"; exit 17; }; fi
: > "$LOGS"
[ -n "$PID_VELHO" ] && log "AVISO_PID_VELHO: .rito_v413.pid velho ($PID_VELHO): de um lancador que nao vive mais -- sobrescrito"

orfaos() {
  # encerra qualquer trabalhador do pilar quantico vivo (de uma rodada morta, ou desta quando o rito ja acabou/morreu) -- a GPU nao pode ter dois
  o=$(powershell.exe -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { \$_.CommandLine -and \$_.CommandLine -match 'pilar_quantico_worker\.py' } | ForEach-Object { \$_.ProcessId }" 2>/dev/null | tr -d '\r')
  for p in $o; do log "trabalhador do pilar quantico vivo sem rito (PID $p) -- encerrando a arvore"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1; done
}

mata_um() {
  # encerra a ARVORE do rito DESTA rodada (o rito esta perdido) -- nunca a de outra casa (5a afericao) -- e e' FAIL-CLOSED (6a afericao):
  # (1) pelo PID nativo do subshell do rito, o pai Windows da cadeia (python um.py -> trabalhador -> referencia na CPU);
  # (2) so se ele for ilegivel, pelos python um.py DESCENDENTES do lancador (data de criacao do filho >= a do pai: PID reaproveitado nao entra), com a
  #     sentinela MATA_OK; (3) se nada der, ou se o subshell seguir vivo, FALHA VISIVEL no log e em rito_v413_sinal.txt.
  MATOU=0
  W=$(cat /proc/$UMPID/winpid 2>/dev/null)
  case "$W" in ''|*[!0-9]*) W="";; esac
  if [ -n "$W" ]; then
    log "encerrando a arvore do rito pelo PID nativo do subshell ($W)"
    taskkill //T //F //PID "$W" >> "$LOGS" 2>&1 && MATOU=1
  fi
  if [ "$MATOU" != "1" ]; then
    RW=$(cat /proc/$$/winpid 2>/dev/null)
    case "$RW" in ''|*[!0-9]*) log "FALHA VISIVEL: nem o PID do subshell nem o do lancador sao legiveis -- o um.py desta rodada pode seguir vivo (encerre-o a mao)"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v413_sinal.txt"; return 1;; esac
    u=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; \$all = Get-CimInstance Win32_Process; \$byid = @{}; foreach (\$x in \$all) { \$byid[[int]\$x.ProcessId] = \$x }; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; \$pp = \$byid[[int]\$p]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId) -and (\$pp -eq \$null -or \$c.CreationDate -ge \$pp.CreationDate)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.ProcessId -ne $RW -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'MATA_OK'" 2>&1 | tr -d '\r')
    echo "$u" | grep -q "MATA_OK" || { log "FALHA VISIVEL: a consulta dos descendentes falhou ($u) -- o um.py desta rodada pode seguir vivo"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v413_sinal.txt"; return 1; }
    for p in $(echo "$u" | grep -E '^[0-9]+$'); do log "encerrando a arvore do um.py desta rodada (PID $p)"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1 && MATOU=1; done
  fi
  sleep 2
  if kill -0 "$UMPID" 2>/dev/null || [ "$MATOU" != "1" ]; then
    log "FALHA VISIVEL: o encerramento nao se confirmou (subshell vivo ou nada encerrado) -- o um.py desta rodada pode seguir vivo"
    echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v413_sinal.txt"; return 1
  fi
  return 0
}

VPID=""
RELIGADO=0
VIGIA_MORTO=0
ESPERA_EXPIROU=0
religar() {
  trap '' TERM HUP INT                                # a restauracao nao e' abortada por sinal (4a afericao)
  [ "$RELIGADO" = "1" ] && return 0
  RELIGADO=1
  # (o .rito_v413.pid NAO sai aqui: so no FIM da restauracao, pelo trap do EXIT -- 9a afericao)
  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  [ -f "$PK/.vigia_pilar_ativo" ] && rm -f "$PK/.vigia_pilar_ativo"   # (v413) o vigia do pilar sai sozinho ao ver a bandeira apagada
  if [ -n "$VPID" ]; then
    # o vigia NAO e' morto: ve a bandeira apagada, termina a parada que estiver fazendo e sai sozinho -- nenhuma parada orfa depois do religamento (5a afericao)
    w_=0; while kill -0 "$VPID" 2>/dev/null && [ $w_ -lt 120 ]; do sleep 1; w_=$((w_+1)); done
    if kill -0 "$VPID" 2>/dev/null; then log "AVISO: o vigia nao saiu em 120 s -- encerrado"; kill "$VPID" 2>/dev/null; VIGIA_MORTO=1; fi
  fi
  orfaos
  if [ "$ESTAVA_LIGADO" != "1" ]; then
    log "nao religo: o servidor nao estava ligado antes do rito (estado anterior restaurado)"; rm -f "$MARCA"; return 0
  fi
  # um stop_iald_llama.ps1 do vigia ainda em curso mataria o servidor recem-religado: esperar que nenhum esteja vivo (ate 60 s; 4a afericao)
  j=0
  while [ $j -lt 12 ]; do
    s_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' OR Name='pwsh.exe'\" | Where-Object { \$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count" 2>/dev/null | tr -d '\r')   # a MESMA consulta da reconferencia (9a)
    [ "$s_" = "0" ] && break
    sleep 5; j=$((j+1))
  done
  [ "$s_" = "0" ] || { log "AVISO: depois de 60 s ainda havia parada em curso ou a contagem nao foi legivel ('$s_') -- religo assim mesmo"; ESPERA_EXPIROU=1; }
  log "RELIGANDO o servidor do modelo nativo pela tarefa agendada (como no boot)"
  powershell.exe -NoProfile -NonInteractive -Command "Start-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
  i=0
  while [ $i -lt 36 ]; do
    if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
      if [ "$VIGIA_MORTO" = "1" ] || [ "$ESPERA_EXPIROU" = "1" ]; then
        # depois de um AVISO, uma parada pendente pode derrubar o servidor recem-religado: reconferir a porta 30 s depois (6a afericao)
        sleep 30
        if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
          # nenhuma parada ainda em curso (as classes [T] e [a] impedem a consulta de casar consigo mesma) -- senao, ou com a contagem ilegivel, o marcador fica (7a-9a)
          sp_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' OR Name='pwsh.exe'\" | Where-Object { \$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count" 2>/dev/null | tr -d '\r')
          case "$sp_" in
            0) log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0;;
            ''|*[!0-9]*) log "AVISO: a porta 8081 escuta, mas a contagem das paradas em curso nao foi legivel ('$sp_') -- o marcador fica: $MARCA"; return 0;;
            *) log "AVISO: a porta 8081 escuta, mas ha parada (Stop-ScheduledTask ou stop_iald_llama.ps1) ainda em curso ($sp_) -- o marcador fica: $MARCA"; return 0;;
          esac
        fi
        log "AVISO: a porta 8081 escutou e PAROU em seguida (uma parada pendente?) -- conferir a tarefa; o marcador fica: $MARCA"; return 0
      fi
      log "servidor de volta: a porta 8081 escuta"; rm -f "$MARCA"; return 0
    fi
    sleep 5; i=$((i+1))
  done
  log "AVISO: a porta 8081 nao escutou em 180 s depois do religamento -- conferir a tarefa «IALD Llama Server» (o marcador fica: $MARCA)"
}

RITO_INICIADO=0
sinal() {
  # tres estados (5a afericao): 0 antes do rito, 1 durante, 2 depois (o RITO_RC ja foi gravado)
  if [ "$RITO_INICIADO" = "1" ]; then
    log "SINAL $1 recebido durante o rito: o rito esta perdido -- encerro a arvore do um.py desta rodada e restauro o servidor"
    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v413_stdout.txt
    echo "RITO_RC=SINAL_$1 $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v413_sinal.txt"   # o um.py ainda vivo poderia sobrescrever o trailer do stdout (6a afericao)
  elif [ "$RITO_INICIADO" = "2" ]; then
    log "SINAL $1 recebido DEPOIS do rito (RITO_RC=$rc ja gravado): restauro o servidor"; exit $rc
  else
    log "SINAL $1 recebido ANTES do rito comecar: nada a encerrar; restauro o servidor"   # o stdout da tentativa anterior nao e' tocado (4a afericao)
  fi
  exit 143
}

# 0. o estado de antes (para restaurar exatamente ele), o marcador de uma rodada morta e os orfaos
TAREFA_EXISTE=$(powershell.exe -NoProfile -NonInteractive -Command "if (Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue) { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
case "$TAREFA_EXISTE" in 0|1) ;; *) log "a sonda da tarefa falhou ('$TAREFA_EXISTE') -- NAO RODO"; exit 14;; esac
T_RODANDO=$(powershell.exe -NoProfile -NonInteractive -Command "\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\$t -and \$t.State -eq 'Running') { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
P_VIVO=$(powershell.exe -NoProfile -NonInteractive -Command "if (@(Get-Process llama-server -ErrorAction SilentlyContinue).Count -gt 0) { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
T_DESAB=$(powershell.exe -NoProfile -NonInteractive -Command "\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\$t -and \$t.State -eq 'Disabled') { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
case "$T_DESAB" in 0|1) ;; *) log "a sonda da tarefa DESABILITADA falhou ('$T_DESAB') -- NAO RODO"; exit 14;; esac   # fail-closed, como a sonda da tarefa (5a afericao)
ORIGEM=""
[ "$T_RODANDO" = "1" ] && ORIGEM="$ORIGEM tarefa-rodando"
[ "$P_VIVO" = "1" ] && ORIGEM="$ORIGEM processo-vivo"
{ [ -z "$T_RODANDO" ] || [ -z "$P_VIVO" ]; } && ORIGEM="$ORIGEM sonda-vazia"
if [ -n "$ORIGEM" ]; then ESTAVA_LIGADO=1; else ESTAVA_LIGADO=0; fi   # sonda vazia = «ligado» (a favor do servico)
if [ -f "$MARCA" ]; then
  # o marcador de uma rodada que morreu com o servidor parado: vale o que ELE gravou (restaurar=0|1), nao mais (4a afericao)
  if grep -q "restaurar=1" "$MARCA"; then
    log "MARCADOR de uma rodada anterior que morreu com o servidor parado ($(cat "$MARCA")) -- o servidor sera religado no fim"; ESTAVA_LIGADO=1; ORIGEM="$ORIGEM marcador"
  else
    log "MARCADOR de uma rodada anterior com restaurar=0 ($(cat "$MARCA")) -- o servidor nao estava ligado; marcador removido"; rm -f "$MARCA"
  fi
fi
log "antes: tarefa existe=$TAREFA_EXISTE ; tarefa rodando=$T_RODANDO ; tarefa desabilitada=$T_DESAB ; llama-server vivo=$P_VIVO ; restaurar no fim=$ESTAVA_LIGADO (origem:${ORIGEM:- nenhuma})"
if [ "$TAREFA_EXISTE" != "1" ] && [ "$ESTAVA_LIGADO" = "1" ]; then
  log "restaurar=1 (origem:$ORIGEM) mas a tarefa agendada NAO existe: nao saberia religar o servidor -- NAO RODO (suba-o pela tarefa ou pare-o antes)"; exit 13
fi
if [ "$T_DESAB" = "1" ] && [ "$ESTAVA_LIGADO" = "1" ]; then
  log "restaurar=1 (origem:$ORIGEM) mas a tarefa agendada esta DESABILITADA: Start-ScheduledTask nao religaria -- NAO RODO"; exit 15
fi
orfaos
# 1. o trap ANTES de parar (TERM/HUP/INT durante a parada tambem restauram); depois parar: a TAREFA primeiro, depois o supervisor e os orfaos
trap 'religar; rm -f "$PK/.rito_v413.pid"' EXIT   # o PID so sai DEPOIS da restauracao inteira (9a afericao)
trap 'sinal TERM' TERM; trap 'sinal HUP' HUP; trap 'sinal INT' INT
# (o .rito_v413.pid ja foi gravado logo depois da guarda; abortar = kill -TERM $(cat .rito_v413.pid) NO GIT BASH, conferindo antes o /proc/<pid>/cmdline)
echo "$(date '+%Y-%m-%d %H:%M:%S') servidor parado pelo rito v413 (restaurar=$ESTAVA_LIGADO)" > "$MARCA"
if [ "$ESTAVA_LIGADO" = "1" ]; then
  log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"
  powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
  powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1
  sleep 5
else
  log "o servidor do modelo nativo nao estava ligado: nada a parar (a parada e o religamento so' agem se ele estava ligado)"
fi
vivos=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d '\r')
log "depois da parada: llama-server vivos = $vivos ; a placa NAO e' medida (v413: ha treino em curso na placa -- nao tocar, nao medir, nao parar; o pilar e' reaproveitado pelo cache e o vigia do pilar para o rito se o um.py anunciar o calculo)"
if [ "$vivos" != "0" ]; then
  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); o trap restaura o estado anterior"; exit 10
fi

# a ROTACAO, so agora, depois da ULTIMA recusa: o log real da rodada anterior (e o registro dos sinais) so sai do lugar quando esta rodada vai mesmo rodar
# o giro CONFERIDO (9a afericao): se falhar, FALHA VISIVEL e recusa 17 -- o trap restaura o servidor; nada de anexar ao log de outra rodada.
# Os SINAIS giram PRIMEIRO (10a afericao): toda recusa 17 acontece com o log real ainda no lugar, e o registro dela fica no .fase0
# [ERRATA AO LADO, 11a: «toda» vale para a 17 dos sinais e a do log real; a da troca do .fase0 pelo log real vem DEPOIS de o log real girar -- sem perda:
#  o registro dela fica no .fase0, e a tentativa seguinte o acrescenta ao .fase0.anterior sem tocar o .anterior do log real]
if [ -f "$PK/rito_v413_sinal.txt" ]; then mv -f "$PK/rito_v413_sinal.txt" "$PK/rito_v413_sinal.txt.anterior" || { log "FALHA VISIVEL: o registro dos sinais nao girou -- NAO RODO"; exit 17; }; fi
if [ -f "$LOGF" ]; then mv -f "$LOGF" "$LOGF.anterior" || { log "FALHA VISIVEL: o log real da rodada anterior nao girou -- NAO RODO"; exit 17; }; fi
mv -f "$LOGS" "$LOGF" || { log "FALHA VISIVEL: o log da tentativa nao tomou o lugar do log real -- NAO RODO"; exit 17; }
LOGS="$LOGF"
# 2. o vigia: se o servidor reaparecer durante o rito, e' encerrado e o fato fica no log
touch "$PK/.vigia_ativo"
PAI=$$
(
  t_ini=$(date +%s)
  while [ -f "$PK/.vigia_ativo" ]; do
    # o vigia morre com o lancador (se o sh for morto a forca, o trap nao roda) e nunca passa de 8 h
    kill -0 "$PAI" 2>/dev/null || { echo "$(date +%H:%M:%S) VIGIA: o lancador morreu -- o vigia sai" >> "$LOGS"; break; }
    [ $(( $(date +%s) - t_ini )) -gt 28800 ] && { echo "$(date +%H:%M:%S) VIGIA: 8 h -- o vigia sai" >> "$LOGS"; break; }
    c=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d '\r')
    if [ -n "$c" ] && [ "$c" != "0" ]; then
      echo "$(date +%H:%M:%S) VIGIA: o llama-server REAPARECEU ($c) durante o rito -- encerrando" >> "$LOGS"
      powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
      powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1
    fi
    k_=0; while [ $k_ -lt 60 ] && [ -f "$PK/.vigia_ativo" ]; do sleep 1; k_=$((k_+1)); done   # dorme em passos de 1 s: sai logo depois da bandeira (5a afericao)
  done
) &
VPID=$!

# 3. o rito (em segundo plano + wait: um sinal ao lancador age na hora, sem esperar o rito acabar)
if [ -f rodada_v413_stdout.txt ]; then n=1; while [ -f "rodada_v413_stdout_tentativa$n.txt" ]; do n=$((n+1)); done; mv rodada_v413_stdout.txt "rodada_v413_stdout_tentativa$n.txt"; fi
# 2b. (v413) o VIGIA DO PILAR: le o stdout canonico (que o carimbador grava em tempo real) ate' a decisao do pilar. REUSO com a chave do ESPERADOS: sai. CALCULO, ou reuso com
# outra chave: grava PILAR_PARADA_v413.txt e manda TERM ao lancador (sinal TERM do molde: encerra a arvore do um.py desta rodada e restaura o servidor). Ha treino na placa.
[ -f "$PK/PILAR_PARADA_v413.txt" ] && mv -f "$PK/PILAR_PARADA_v413.txt" "$PK/PILAR_PARADA_v413.txt.anterior_$(date +%Y%m%d_%H%M%S)"
touch "$PK/.vigia_pilar_ativo"
(
  t0p=$(date +%s); avisou=0
  while [ -f "$PK/.vigia_pilar_ativo" ]; do
    kill -0 "$PAI" 2>/dev/null || break
    if [ -f rodada_v413_stdout.txt ]; then
      r_=$(python "$PK/pilar_no_stdout_v413.py" rodada_v413_stdout.txt "$PK/ESPERADOS_v413.json" 2>&1 | tail -1 | tr -d '\r')
      case "$r_" in
        REUSO_OK*) echo "$(date +%H:%M:%S) VIGIA DO PILAR: $r_ (o pilar foi reaproveitado pela chave do cache; nada na placa alem do autoteste do motor)" >> "$LOGS"; break;;
        CALCULA*|CHAVE_ERRADA*) echo "$(date +%H:%M:%S) VIGIA DO PILAR: $r_ -- o pilar NAO foi reaproveitado; ha treino em curso na placa: PARO o rito e aviso" >> "$LOGS"
          echo "$r_ $(date '+%Y-%m-%d %H:%M:%S')" > "$PK/PILAR_PARADA_v413.txt"; kill -TERM "$PAI" 2>/dev/null; break;;
      esac
    fi
    if [ "$avisou" = "0" ] && [ $(( $(date +%s) - t0p )) -gt 2400 ]; then echo "$(date +%H:%M:%S) VIGIA DO PILAR: AVISO -- 40 min sem a linha do pilar no stdout; sigo vigiando" >> "$LOGS"; avisou=1; fi
    sleep 3
  done
) &
t0=$(date +%H:%M:%S); echo "$t0" > "$PK/rito_horarios_v413.txt"
log "inicio do rito $t0 (um.py $h)"
RITO_INICIADO=1
# [03/11, pedido do gerente do LAR para o filme em par] o stdout canonico segue IDENTICO em bytes em rodada_v413_stdout.txt (no Nos); o carimbador grava ao lado, NO PACOTE, o rodada_v413_stdout_tempos.jsonl
# ({linha, hora_utc, bytes} por linha + registro final com bytes_total e sha256 do stdout antes do trailer). pipefail: o RC do subshell e' o do um.py (o carimbador so' falha com rc 3 se os bytes gravados diferirem dos recebidos).
# PYTHONUNBUFFERED=1 so' neste subshell: cada linha chega ao carimbador quando o um.py a escreve. A linha de lancamento do um.py fica literal (invariante do conferidor).
[ -f "$PK/rodada_v413_stdout_tempos.jsonl" ] && mv "$PK/rodada_v413_stdout_tempos.jsonl" "$PK/rodada_v413_stdout_tempos_tentativa_$(date +%Y%m%d_%H%M%S).jsonl"
( set -o pipefail; export PYTHONUNBUFFERED=1; echo 1 | python um.py 2>&1 | python -u "$PK/carimbar_stdout_v413.py" rodada_v413_stdout.txt "$PK/rodada_v413_stdout_tempos.jsonl" ) &
UMPID=$!
wait "$UMPID"
rc=$?
echo "RITO_RC=$rc" >> rodada_v413_stdout.txt
RITO_INICIADO=2
t1=$(date +%H:%M:%S); echo "$t1" >> "$PK/rito_horarios_v413.txt"
log "fim do rito $t1 rc=$rc"
tail -3 rodada_v413_stdout.txt
exit $rc

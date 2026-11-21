#!/bin/sh
# cadeia_pos_rito_v413.sh -- O POS-RITO DOS TEXTOS DA v413 (Etapa 3 da v413, 20/11/2026; ATO DA GERENCIA c1, depois do rito_v413.sh com RITO_RC=0; NAO executado na
# preparacao). Molde: a cadeia que a v412 fez a mao (o conferidor enxuto, os diffs, o compositor R2 e as superficies), mais a ordem do autor de 19/11 e 20/11:
# a arvore da prova regerada com o rotulo da v413 e as derivacoes novas, e a guarda que recusa .md declarado com a versao de outro selo no titulo.
# ORDEM: 1 o conferidor (conferir_pos_rito_v413_foco.py; TUDO BATE ou PARA) -> 2 a guarda privada da fase pos (zero termos novos ou PARA: decisao do autor)
# -> 3 a arvore da prova (a linha das pedras da v413 entra no gerador da casa por adaptar_arvore_da_prova_v413.py --executar, com backup _p413; depois
# arvore_da_prova.py v413, que grava Nos\A_PROVA_DA_QG_TGL_arvore.md com backup) -> 4 a guarda do titulo (sem o handoff) -> 5 os diffs (DIFF_v412_v413.diff,
# DIFF_KERNEL_v413.txt, DIFFS_v413_RECIBO.json) -> 6 o elo B(n): os tres recibos pela funcao da G1, ou a decisao do operador; sem eles, AGUARDA (rc 20: a
# gerencia roda bancada\bn_v413.sh do 10 ao 11 e retoma com CHAIN_DE=7) -> 7 o compositor R2: a conferencia (sem escrever) e, limpa, --executar (o diario,
# o adendo do desenho e, por ultimo, o HANDOFF_v413_CUSTODIA.md) -> 8 a guarda do titulo (com o handoff) -> 9 as superficies da gerencia (Atlas e indice
# vivo: atlas_indice.py v413; a porta da memoria: porta_memoria.py), SO' com CHAIN_SUPERFICIES=sim; sem ela, os comandos sao impressos -> 10 o que fica
# a mao (a linha do MEMORY.md pela fila, os blocos do core e do CLAUDE.md da Haja_Luz, e por ULTIMO o ENTREGA_A_CUSTODIA_v413.json) e' impresso.
# Sai na primeira reprovacao e NAO restaura nada sozinha (a decisao de reverter e' da gerencia: reverter_v413.py). Retomada: CHAIN_DE=<n> (e CHAIN_ATE=<n>).
# Ambiente: BLOCOS=<BLOCOS_TEXTO_PUBLICO_v413.json> (padrao: o da pasta); BN_DISPENSADO_FALA=<fala do operador por bytes> (so' se o B(n) nao fechar).
# Codigos: 0 fim; 1 PARADA; 20 AGUARDA (o B(n)).
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413"; POS="$PK/pos_rito"; CS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
PY="/c/Python314/python.exe -B -X utf8"; PYI="/c/Python314/python.exe -I -B -X utf8"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR V413_ENSAIO_DIR
DE=${CHAIN_DE:-1}; ATE=${CHAIN_ATE:-10}
LOG="$POS/cadeia_pos_rito_v413_$(date +%Y%m%d_%H%M%S).log"
parar() { echo "PARADA no passo $1: $2" | tee -a "$LOG"; echo "(nada foi restaurado: a decisao de reverter e da gerencia -- reverter_v413.py)" | tee -a "$LOG"; exit 1; }
roda() { [ "$1" -ge "$DE" ] && [ "$1" -le "$ATE" ]; }
log() { echo "$(date +%H:%M:%S) $*" | tee -a "$LOG"; }
[ -f "$NOS/rodada_v413_stdout.txt" ] || parar 0 "sem o stdout canonico do rito (Nos\\rodada_v413_stdout.txt)"
tail -1 "$NOS/rodada_v413_stdout.txt" | grep -q "^RITO_RC=0" || parar 0 "o stdout do rito nao termina com RITO_RC=0"
[ -f "$PK/PILAR_PARADA_v413.txt" ] && parar 0 "o vigia do pilar parou o rito (PILAR_PARADA_v413.txt): avisar o operador; reverter_v413.py"
if roda 1; then log "1. o conferidor pos-rito"; $PY "$PK/conferir_pos_rito_v413_foco.py" < /dev/null >> "$LOG" 2>&1 || parar 1 "o conferidor nao bateu (CONFERENCIA_POS_RITO_v413_FOCO.json)"; tail -1 "$LOG"; fi
if roda 2; then log "2. a guarda privada (fase pos)"; $PY "$PK/guarda_privada_v413.py" --fase pos < /dev/null >> "$LOG" 2>&1 || parar 2 "termo privado novo (GUARDA_PRIVADA_v413_pos.json): decisao do autor antes do handoff"; tail -1 "$LOG"; fi
if roda 3; then
  log "3. a arvore da prova com o rotulo da v413"
  if ! grep -q "AS PEDRAS DA v413" "$CS/arvore_da_prova.py"; then $PY "$POS/adaptar_arvore_da_prova_v413.py" --executar < /dev/null >> "$LOG" 2>&1 || parar 3 "a linha da v413 nao entrou no gerador da arvore"; fi
  ( cd "$CS" && $PY arvore_da_prova.py v413 < /dev/null ) >> "$LOG" 2>&1 || parar 3 "arvore_da_prova.py v413 falhou"
  tail -2 "$LOG"
fi
if roda 4; then log "4. a guarda do titulo (sem o handoff)"; $PYI "$POS/guarda_titulo_versao_v413.py" v413 --sem-handoff < /dev/null >> "$LOG" 2>&1 || parar 4 "documento declarado com a versao de outro selo no titulo"; tail -1 "$LOG"; fi
if roda 5; then log "5. os diffs da v413"; $PYI "$POS/diffs_v413.py" < /dev/null >> "$LOG" 2>&1 || parar 5 "os diffs reprovaram"; tail -1 "$LOG"; fi
if roda 6; then
  log "6. o elo B(n): os tres recibos (funcao da G1) ou a decisao do operador"
  n_=$(find "$PK" -path "*bancada_B3*" \( -name "RECIBO_SINCRONIZACAO_v413_*.json" -o -name "RECIBO_PARADA_v413*.json" -o -name "RECIBO_RELIGAMENTO_v413*.json" \) ! -path "*ensaio*" ! -name "*.bak_*" | wc -l)
  if [ "$n_" -lt 3 ] && [ ! -f "/c/IALD/Central de Patentes/work/custodia_G1/decisoes/BN_DISPENSADO_v413.json" ] && [ -z "$BN_DISPENSADO_FALA" ]; then
    log "AGUARDA: o B(n) da v413 nao fechou ($n_ de 3 recibos) e nao ha decisao do operador: rode bancada\\bn_v413.sh (10 -> 10a -> evento -> 10b -> 10c -> 11) e retome com CHAIN_DE=7"; exit 20
  fi
fi
if roda 7; then
  log "7. o compositor R2: a conferencia, depois a escrita"
  set -- ; [ -n "$BLOCOS" ] && set -- "$@" --blocos "$BLOCOS"; [ -n "$BN_DISPENSADO_FALA" ] && set -- "$@" --bn-dispensado "$BN_DISPENSADO_FALA"
  $PY "$PK/montar_handoff_e_linhagem_v413.py" "$@" < /dev/null >> "$LOG" 2>&1 || parar 7 "a conferencia do compositor reprovou (ver o log): nada escrito"
  grep -q "conferencia (prosa, NOTA, blocos, formas, guarda de frases): LIMPA" "$LOG" || parar 7 "a conferencia do compositor nao saiu LIMPA"
  $PY "$PK/montar_handoff_e_linhagem_v413.py" --executar "$@" < /dev/null >> "$LOG" 2>&1 || parar 7 "o compositor nao gravou"
  tail -1 "$LOG"
fi
if roda 8; then log "8. a guarda do titulo (com o handoff)"; $PYI "$POS/guarda_titulo_versao_v413.py" v413 < /dev/null >> "$LOG" 2>&1 || parar 8 "o handoff ou a arvore sem a versao do selo no titulo"; tail -1 "$LOG"; fi
if roda 9; then
  if [ "$CHAIN_SUPERFICIES" = "sim" ]; then
    log "9. as superficies da gerencia: Atlas e indice vivo, porta da memoria"
    ( cd "$CS" && $PY atlas_indice.py v413 < /dev/null ) >> "$LOG" 2>&1 || parar 9 "atlas_indice.py v413 falhou"
    $PY "/c/LAR_MIGUEL/porta_memoria.py" < /dev/null >> "$LOG" 2>&1 || parar 9 "porta_memoria.py falhou"
  else
    log "9. (CHAIN_SUPERFICIES != sim) as superficies da gerencia, para rodar a mao: cd \"$CS\" && $PY atlas_indice.py v413 ; $PY /c/LAR_MIGUEL/porta_memoria.py"
  fi
fi
if roda 10; then
  log "10. a mao, nesta ordem (ROTEIRO_EXECUCAO_v413.md, passos 9 e 10): a linha do MEMORY.md pela fila (antes do C13 da custodia); os blocos core_v413_selada e haja_luz_v413_selada"
  log "    (os dois paragrafos de abertura do handoff VERBATIM); grep -c v413 em cada superficie; e por ULTIMO o ENTREGA_A_CUSTODIA_v413.json pelo modelo, por troca atomica"
fi
log "FIM do pos-rito dos textos (passos $DE a $ATE)"; exit 0

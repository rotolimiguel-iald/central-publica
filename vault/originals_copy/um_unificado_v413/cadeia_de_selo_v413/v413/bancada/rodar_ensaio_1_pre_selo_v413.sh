#!/bin/sh
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bateria_pre_selo/rodar_ensaio_1_pre_selo_v412.sh, derivado para o SALTO v411 -> v413 (DIAGNOSTICO_E_PLANO_BN_v413.md 2.3.c, 2.4):
#   --versao v412 (o Nos ainda na v412: N1), a bateria da v412 (N2, caminho a) e a cadeia de selos v411 -> v412 (--cadeia-de-selos e --cadeia-de-selos-sha256, LIDOS dos pinos e conferidos contra o disco); --saida em v413\bateria_pre_selo\ensaio_1.
#   Sem `python -c`: todo valor vem do util_bn_v413.py (constantes do delta_bn_v413 e campos dos pinos).
# v413, elo B(n), fase pre_selo do SALTO, SO ENSAIO: o esboco R3.6 so' LE a Bancada de producao e o Nos e grava so' em --saida. A Bancada esta' atrasada (pina B20-v411; o Nos e' a v412): sem a cadeia o esboco
# recusaria BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS. Veredito esperado (lido do codigo do esboco, l.2875-2877 e 2953): REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA.
# Nao precisa do servico (a guarda_servico so' age no aplicar, l.2686) e nao usa a placa de video.
B="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada"
PY="/c/Python314/python.exe -I -B -X utf8"
cd "$B" || exit 9
UV() { $PY "$B/util_bn_v413.py" "$@" | tr -d '\r'; }
OUTB_W=$(UV const OUTB_PRE_SELO)
[ -n "$OUTB_W" ] || { echo "a pasta de saida do pre-selo nao foi lida do delta_bn_v413"; exit 9; }
OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"
SAIDA="$OUTB_W\\ensaio_1"
OUT="$OUTB/etapa1_stdout.txt"
P11=$(UV const PINOS_BN_V411_ARQ)
ESB=$(UV pino "$P11" esboco_R3_6 path); ESB_PINO=$(UV pino "$P11" esboco_R3_6 sha256); ESB_SHA=$(UV sha256 "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BATD=$(UV const BATERIA_V412_DIR)
BAT=$(UV pino "$BATD\\PINOS_BATERIA_v412.json" bateria path); BAT_PINO=$(UV pino "$BATD\\PINOS_BATERIA_v412.json" bateria sha256); BAT_SHA=$(UV sha256 "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
CADP=$(UV const PINO_CADEIA_ARQ)
CAD=$(UV pino "$CADP" cadeia path); CAD_PINO=$(UV pino "$CADP" cadeia sha256); CAD_SHA=$(UV sha256 "$CAD")
[ -n "$CAD_SHA" ] && [ "$CAD_SHA" = "$CAD_PINO" ] || { echo "CADEIA_SHA_DIVERGE $CAD_SHA != pino $CAD_PINO"; exit 9; }
NOS_W=$(UV const NOS); BANC_W=$(UV const PRODUCAO); VPS=$(UV const VERSAO_DO_PRE_SELO)
[ "$VPS" = "v412" ] || { echo "a versao do pre-selo lida do delta nao e' a v412: $VPS"; exit 9; }
$PY "$ESB" \
  --bancada "$BANC_W" --producao \
  --nos "$NOS_W" \
  --versao "$VPS" --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --cadeia-de-selos "$CAD" --cadeia-de-selos-sha256 "$CAD_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"

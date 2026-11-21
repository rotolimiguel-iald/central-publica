#!/bin/sh
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bateria_pre_selo/rodar_bn_pre_selo_v412.sh (o corpo: codigos de saida sem mascara, o etapa1 desta rodada, o `utilizavel` lido do pino;
#   pendencia 1.2 ja feita no molde), derivado para o SALTO v411 -> v413 (DIAGNOSTICO_E_PLANO_BN_v413.md 2.3.c-d, 5.1 passo 1): o sandbox curto LIDO do delta_bn (N8), o ensaio com --versao v412 e a cadeia, o conferir do salto (C.1),
#   o pino do salto (1.1), o diff_e_pinos do salto (1.4, 2.5, N6) e o p00 do B(n). Sem `python -c`: todo valor vem do util_bn_v413.py.
# PRAZO (N1): roda com o Nos AINDA na v412 (antes da instalacao da v413); com o Nos ja na v413 este runner PARA antes de tudo (o pre-selo do salto so' poderia ser refeito para a v414).
# Ordem: fotografa a producao (antes); ensaio do salto (so' leitura da producao e do Nos; grava so' em --saida); fotografa (depois); confere o recibo pelo esboco (condicoes + controles negativos); fotografa (final);
# gera PINO_RECIBO_PRE_SELO_v413.json e PROVA_PRODUCAO_INTACTA_v413_pre_selo.json em v413\; apaga o sandbox curto; diff_e_pinos_bn_v413.py (PINOS_BN_v413.json; sem --delta: o que depende do candidato fica pendente);
# p00_precondicoes_bn_v413.py (PRECONDICOES_BN_v413.json). Nao toca o Nos, nao instala, nao roda o rito, nao grava na Bancada, nao para nem religa servico, nao usa a placa de video.
# uso: sh ./rodar_bn_pre_selo_v413.sh > <v413\bateria_pre_selo>/bn_pre_selo_out_v413.txt 2>&1 ; echo "RC_BN=$?"
#   (revisao M2) passa do limite padrao de 120 s da ferramenta Bash (a bateria inteira e tres fotografias do Nos): rodar com run_in_background ou com timeout de 600000 ms, e ler o veredito no arquivo de saida.
#   (revisao M1) C:\t\vb24 e' exclusivo deste pre-selo: nenhuma guarda estatica (a Etapa 2 usa C:\t\vb25) nem controle negativo pode estar em curso; o runner recusa se a pasta ja existe.
set -e
B="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada"
PY="/c/Python314/python.exe -I -B -X utf8"
cd "$B"
UV() { $PY "$B/util_bn_v413.py" "$@" | tr -d '\r'; }
for f in rodar_ensaio_1_pre_selo_v413.sh snap_producao_v413.py conferir_recibo_pre_selo_salto_v413.py gerar_pino_recibo_pre_selo_v413.py limpar_sandbox_vb24.py diff_e_pinos_bn_v413.py p00_precondicoes_bn_v413.py delta_bn_v413.py util_bn_v413.py; do
  [ -f "$f" ] || { echo "FALTA $f -- NAO RODO"; exit 9; }
done
if grep -l '^# \[A ADAPTAR v413\]' ./*.py ./*.sh; then echo "algum script do B(n) ainda traz a marca de adaptacao pendente -- NAO RODO"; exit 9; fi
# o prazo (N1): o Nos ainda na v412, com o selo pinando o um.py do disco
NV=$(UV nos_versao) || true
case "$NV" in
  "v412 SELO_PINA_O_UM_PY") echo "o Nos esta' na v412 (selo pina o um.py do disco): dentro do prazo do pre-selo do salto";;
  *) echo "PRAZO_DO_PRE_SELO_PERDIDO (N1): o Nos nao esta' na v412 com o selo pinando o um.py ($NV) -- NAO RODO"; exit 9;;
esac
# a Bancada ainda no B20 da v411 (o delta_bn confere ao ser importado; aqui, nao aplicada)
JA=$(UV const BANCADA_JA_APLICADA)
[ "$JA" = "False" ] || { echo "a Bancada de producao ja nao pina o B20 da v411 (BANCADA_JA_APLICADA=$JA) -- NAO RODO"; exit 9; }
# os insumos do salto existem (a cadeia pinada e a bateria da v412 com o pino ao lado)
[ -f "$(cygpath -u "$(UV const PINO_CADEIA_ARQ)")" ] || { echo "FALTA a cadeia de selos pinada (gerar_e_pinar_cadeia_v413.py) -- NAO RODO"; exit 9; }
[ -f "$(cygpath -u "$(UV const BATERIA_V412_DIR)")/PINOS_BATERIA_v412.json" ] || { echo "FALTA a bateria da v412 pinada (gerar_bateria_v412_pre_selo_v413.py) -- NAO RODO"; exit 9; }
OUTB_W=$(UV const OUTB_PRE_SELO)
[ -n "$OUTB_W" ] || { echo "a pasta de saida do pre-selo nao foi lida do delta_bn_v413"; exit 9; }
OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"
echo "saidas do pre-selo em $OUTB_W"
SB_W=$(UV const SANDBOX_CURTO)
case "$SB_W" in
  'C:\t\vb'[0-9]*) ;;
  *) echo "o sandbox curto lido do delta_bn nao e' C:\\t\\vb<digitos>: $SB_W -- NAO RODO"; exit 9;;
esac
SB=$(cygpath -u "$SB_W")
SNAP="$SB_W\\snap"
if [ -e "$SB" ]; then echo "$SB_W ja existe -- NAO RODO (limpe antes)"; exit 9; fi
# o stdout do ensaio, a pasta --saida, o pino, a prova e a conferencia tem de ser DESTA rodada
for f in "$OUTB/etapa1_stdout.txt" "$OUTB/ensaio_1" "$OUTB/conferencia_pelo_esboco_v413.json" "$OUTB/prova_producao" "$OUTB/LIMPEZA_SANDBOX_$(basename "$SB").json" "$(cygpath -u "$(UV const PINO_RECIBO_PRE_SELO_ARQ)")" "$(cygpath -u "$(UV const PROVA_PRODUCAO_ARQ)")"; do
  if [ -e "$f" ]; then echo "$f ja existe (de outra rodada) -- NAO RODO (guarde e tire antes)"; exit 9; fi
done
ls -la
mkdir -p "$SB/snap"
echo "== 1. snap antes $(date +%T)"; $PY snap_producao_v413.py antes "$SNAP"
echo "== 2. ensaio 1 do salto (pre_selo, ensaio, --versao v412, com a cadeia) $(date +%T)"; sh ./rodar_ensaio_1_pre_selo_v413.sh || true
[ -f "$OUTB/etapa1_stdout.txt" ] || { echo "ETAPA1 FALHOU (o ensaio desta rodada nao gravou etapa1_stdout.txt)"; exit 1; }
tail -3 "$OUTB/etapa1_stdout.txt"
grep -q "ETAPA1_RC=0" "$OUTB/etapa1_stdout.txt" || { echo "ETAPA1 FALHOU"; exit 1; }
echo "== 3. snap depois $(date +%T)"; $PY snap_producao_v413.py depois "$SNAP"
echo "== 4. conferir o recibo do salto pelo esboco R3.6 $(date +%T)"; RC_CONFERENCIA=0; $PY conferir_recibo_pre_selo_salto_v413.py > "$OUTB/conferencia_out_v413.txt" 2>&1 || RC_CONFERENCIA=$?; tail -4 "$OUTB/conferencia_out_v413.txt"; echo "RC_CONFERENCIA=$RC_CONFERENCIA"
echo "== 5. snap final $(date +%T)"; $PY snap_producao_v413.py final "$SNAP"
echo "== 6. gerar o pino do recibo do salto e a prova da producao intacta $(date +%T)"; RC_PINO=0; $PY gerar_pino_recibo_pre_selo_v413.py "$SNAP" > "$OUTB/pino_out_v413.txt" 2>&1 || RC_PINO=$?; tail -4 "$OUTB/pino_out_v413.txt"; echo "RC_PINO=$RC_PINO"
echo "== 7. limpar o sandbox curto $(date +%T)"; RC_LIMPAR=0; $PY limpar_sandbox_vb24.py > "$OUTB/limpar_out_v413.txt" 2>&1 || RC_LIMPAR=$?; tail -2 "$OUTB/limpar_out_v413.txt"; echo "RC_LIMPAR=$RC_LIMPAR"
echo "== 8. diff_e_pinos_bn_v413.py (sem --delta: o que depende do candidato fica pendente) $(date +%T)"; RC_DIFF_PINOS=0; $PY diff_e_pinos_bn_v413.py > "$OUTB/diff_e_pinos_out_v413.txt" 2>&1 || RC_DIFF_PINOS=$?; tail -2 "$OUTB/diff_e_pinos_out_v413.txt"; echo "RC_DIFF_PINOS=$RC_DIFF_PINOS"
echo "== 9. p00_precondicoes_bn_v413.py $(date +%T)"; RC_P00=0; $PY p00_precondicoes_bn_v413.py > "$OUTB/p00_out_v413.txt" 2>&1 || RC_P00=$?; tail -16 "$OUTB/p00_out_v413.txt"; echo "RC_P00=$RC_P00 (0 = TODAS PASSARAM; 3 = sem falha e com pendente; 1 = falhou)"
echo "== FIM $(date +%T)"
PINO_W=$(UV const PINO_RECIBO_PRE_SELO_ARQ)
UTIL=$(UV json "$PINO_W" utilizavel_como_recibo_pre_selo_do_B_n) || UTIL=ilegivel
echo "UTILIZAVEL_DO_PINO=$UTIL ($PINO_W)"
if [ "$RC_CONFERENCIA" != 0 ] || [ "$RC_PINO" != 0 ] || [ "$RC_LIMPAR" != 0 ] || [ "$RC_DIFF_PINOS" != 0 ] || { [ "$RC_P00" != 0 ] && [ "$RC_P00" != 3 ]; } || [ "$UTIL" != True ]; then echo "FALHOU: conferencia=$RC_CONFERENCIA pino=$RC_PINO limpar=$RC_LIMPAR diff_e_pinos=$RC_DIFF_PINOS p00=$RC_P00 utilizavel=$UTIL"; exit 1; fi

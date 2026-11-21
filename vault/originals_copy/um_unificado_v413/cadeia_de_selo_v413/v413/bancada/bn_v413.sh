#!/bin/sh
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/pos_rito/bn_v412.sh (executor enxuto dos passos 10 a 10c, mesmos portoes e codigos de saida), derivado para o SALTO v411 -> v413:
#   os argumentos da cadeia de selos no ENSAIO e no APLICAR (--cadeia-de-selos e --cadeia-de-selos-sha256) e o terceiro argumento do b3_recibo (2.4); o pino cadeia_de_selos EXIGIDO (o molde o recusava);
#   N6: o selo e o manifesto do kernel anteriores sao os da v412 (selo_anterior_v412, kernel_manifesto_anterior_v412); 1.4: os pinos delta, delta_bn e util_bn conferidos; 2.4: pino pendente da' AGUARDA (rc 20), nao
#   traceback; 2.7: o PINOS_BN tem de estar FINAL (pendentes == []) antes do 10b; 2.6: o 10b recusa se o evento nao for posterior ao fim do recibo do ensaio; 2.1: o passo 11 volta (fechar_bn_v413.py);
#   o portao C (medida permanente): o 10 recusa sem uma conferencia A de HOJE; o 11 recusa sem o recibo de religamento cujo PID esteja vivo. Sem `python -c`: valores pelo util_bn_v413.py.
# Sequencia: 10 (ENSAIO pos-selo) -> 10a (recibo da PARADA: recibo_parada_v413.py; no ja_fora_do_ar, nada e' parado) -> evento c1 (evento_c1_b3_v413.py: imprime EVENTO=<seq> EVENTO_HASH=<hash16>) ->
#   10b (APLICAR: B3_AUTORIZADO=sim, EVENTO, EVENTO_HASH) -> 10c (recibo do RELIGAMENTO: recibo_religamento_v413.py religa com logs e o modo da placa) -> 11 (fechar: os tres recibos juntos, o pino conjunto, a entrega).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B21__SALTO_v411_v413__ENSAIO__NADA_GRAVADO_NA_BANCADA; aplicar REPINADA_B21__SALTO_v411_v413__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO.
# Ambiente: CHAIN_DE e CHAIN_ATE (10, 10a, 10b, 10c, 11); B3_AUTORIZADO=sim, EVENTO=<seq>, EVENTO_HASH=<hash16> (so' o 10b). Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (de proposito, nao e' falha).
# Sai na primeira reprovacao e NAO restaura nada sozinho (o esboco faz o seu rollback; a decisao de restaurar e' da gerencia). Nao para nem liga o servico: a parada e' ato fora deste executor; o religamento e' o recibo_religamento_v413.py.
B="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada"
PY="/c/Python314/python.exe -I -B -X utf8"
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
export PYTHONIOENCODING=utf-8
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
UV() { $PY "$B/util_bn_v413.py" "$@" | tr -d '\r'; }
UR() { $PY "$B/util_bn_v413.py" "$@"; }
ORDEM="10 10a 10b 10c 11"
DE="${CHAIN_DE:-10}"; ATE="${CHAIN_ATE:-11}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
VER=$(UV const UM_VERSION_BN)
[ "$VER" = "v413" ] || parar "o delta_bn_v413 nao carregou (ou a Bancada nao pina nem o B20 da v411 nem o B21 da v413: o delta o confere ao ser importado)"
PK_W=$(UV const V413); PK=$(cygpath -u "$PK_W")
SEL_W=$(UV const SAIDAS_BN_DIR); SEL=$(cygpath -u "$SEL_W"); mkdir -p "$SEL"
SERV_W=$(UV const SERVICO_DIR); SERV=$(cygpath -u "$SERV_W")
SAUDE_W=$(UV const SAUDE_DIR)
PINOS_W=$(UV const PINOS_BN_ARQ)
NOS_W=$(UV const NOS)
BANC_W=$(UV const PRODUCAO)
pino() { UV pino "$PINOS_W" "$1" sha256; }
pinop() { UV pino "$PINOS_W" "$1" path; }
tem_pino() { UR tem_chave "$PINOS_W" "$1" > /dev/null 2>&1; }
b3_prepara() {
  [ -f "$(cygpath -u "$PINOS_W")" ] || aguarda "sem PINOS_BN_v413.json: gerar o FINAL com diff_e_pinos_bn_v413.py --delta <delta principal da v413> (ato da gerencia) e retomar com CHAIN_DE=$1"
  for k in criterios esboco_R3_6 gerador_bateria driver_t12_t14 bateria_base_R2 kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo cadeia_de_selos selo_anterior_v412 kernel_manifesto_anterior_v412 delta delta_bn util_bn; do
    tem_pino "$k" || aguarda "o PINO $k nao esta em PINOS_BN_v413.json (diff_e_pinos_bn_v413.py --delta <delta principal>) e retomar com CHAIN_DE=$1"
    a=$(pino "$k"); p=$(pinop "$k")
    if [ -z "$a" ] || [ "$a" = "None" ] || [ -z "$p" ] || [ "$p" = "None" ]; then aguarda "o pino $k esta' pendente (NAO_PREPARADO) em PINOS_BN_v413.json: rodar diff_e_pinos_bn_v413.py --delta <delta principal> quando o insumo existir e retomar com CHAIN_DE=$1"; fi
    b=$(UV sha256 "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  [ "$(UV sha256 "$(cygpath -w "$B/delta_bn_v413.py")")" = "$(pino delta_bn)" ] || parar "o delta_bn_v413.py em uso nao e' o pinado em PINOS_BN_v413.json (1.4)"
  [ "$(UV sha256 "$(cygpath -w "$B/util_bn_v413.py")")" = "$(pino util_bn)" ] || parar "o util_bn_v413.py em uso nao e' o pinado em PINOS_BN_v413.json (1.4)"
  UR pendentes_vazios "$PINOS_W" || aguarda "PINOS_BN_v413.json ainda tem pendentes (2.7: o PINOS_BN FINAL, com o recibo pre-selo e o delta, antes do APLICAR) e retomar com CHAIN_DE=$1"
  [ "$(pino candidato)" = "$(UV sha256 "$NOS_W\\um.py")" ] || parar "o um.py do Nos nao e' o candidato pinado em PINOS_BN (candidato $(pino candidato))"
  [ "$(UV json "$PINOS_W" recibo_pre_selo.utilizavel_como_recibo_pre_selo_do_B_n)" = "True" ] || parar "o recibo pre-selo pinado nao e' utilizavel"
  [ "$(UV json "$PINOS_W" recibo_pre_selo.veredito)" = "$(UV const VEREDITO_PRE_SELO)" ] || parar "o recibo pre-selo pinado nao tem o veredito exato do salto"
  CAD=$(pino cadeia_de_selos); RPS=$(pino recibo_pre_selo); CRI=$(pino criterios)
  W_ESB=$(pinop esboco_R3_6); W_CRI=$(pinop criterios); W_RPS=$(pinop recibo_pre_selo); W_CAD=$(pinop cadeia_de_selos)
  W_SELO=$(pinop selo_anterior_v412); W_KMAN=$(pinop kernel_manifesto_anterior_v412)
  W_KR=$(pinop kernel_recibo); KRSHA=$(pino kernel_recibo)
  echo "  recibo do kernel ($(UV json "$W_KR" contrato); sha256 LIDO NA HORA, igual ao pino): $KRSHA | cadeia de selos: $CAD"
  ARV=$(UV json "$W_KR" arvore) || true
  [ -n "$ARV" ] && [ -d "$(cygpath -u "$ARV")" ] || aguarda "a arvore so-fontes do recibo do kernel (campo arvore) nao existe mais: refaze-la (sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
  BATD_W=$(UV const BATERIA_POS_SELO_DIR); BATD=$(cygpath -u "$BATD_W")
  if [ ! -e "$BATD/BATERIA_VINCULO_v413.json" ]; then
    mkdir -p "$BATD"
    $PY "$(pinop gerador_bateria)" --base "$(pinop bateria_base_R2)" --base-sha256 "$(pino bateria_base_R2)" --versao v413 --nos "$NOS_W" \
        --driver "$(pinop driver_t12_t14)" --pinos-bn "$PINOS_W" --pino-saida "$BATD_W\\PINO_UM_PY_v413.json" --saida "$BATD_W\\BATERIA_VINCULO_v413.json" > "$SEL/gerar_bateria_v413_out.txt" 2>&1 \
      || { cut -c1-300 "$SEL/gerar_bateria_v413_out.txt"; parar "o gerador da bateria (pino gerador_bateria) recusou: o Nos nao e' o candidato pinado em PINOS_BN, ou o selo nao pina o um.py (saida em $SEL/gerar_bateria_v413_out.txt)"; }
    $PY "$B/gravar_pino_bateria_v413.py" "$BATD_W\\BATERIA_VINCULO_v413.json" "$BATD_W\\PINO_UM_PY_v413.json" "$BATD_W\\PINOS_BATERIA_v413.json" || parar "nao gravei o pino ao lado da bateria da v413"
    echo "  bateria da v413 GERADA por script em $BATD (pino ao lado: PINOS_BATERIA_v413.json)"
  fi
  [ -f "$BATD/PINOS_BATERIA_v413.json" ] || parar "a bateria da v413 existe sem o pino ao lado: nao se sabe quem a gerou"
  W_BAT="$BATD_W\\BATERIA_VINCULO_v413.json"; BAT=$(UV sha256 "$W_BAT")
  [ "$BAT" = "$(UV pino "$BATD_W\\PINOS_BATERIA_v413.json" bateria sha256)" ] || parar "a bateria da v413 em disco diverge do pino gravado quando foi gerada"
  echo "  bateria da v413 (sha256 LIDO NA HORA, igual ao pino ao lado): $BAT"
}
echo "== 0. guardas do B(n) $(date +%T)"
NV=$(UV nos_versao) || true
[ "$NV" = "v413 SELO_PINA_O_UM_PY" ] || parar "o Nos nao esta' na v413 selada (o selo pinando o um.py do disco): '$NV' -- o B(n) pos-selo so' roda depois do selo da v413"
STD="$(cygpath -u "$NOS_W")/rodada_v413_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito da v413 nao acabou (sem RITO_RC= em $STD)"
tail -3 "$STD" | cut -c1-240
for f in b3_recibo_v413.py recibo_parada_v413.py recibo_religamento_v413.py evento_c1_b3_v413.py fechar_bn_v413.py gravar_pino_bateria_v413.py saude_bancada.py util_bn_v413.py delta_bn_v413.py montar_autorizacao_v413.py aviso_f06_v413.py; do
  [ -f "$B/$f" ] || parar "ferramenta ausente: $B/$f"; done
if quer 10; then
echo "== 10. B(n) da Bancada, ENSAIO pos-selo, SALTO v411 -> v413, esboco R3.6 (nada e' gravado na Bancada) $(date +%T)"
UR saude_do_dia "$SAUDE_W" || aguarda "portao C: sem uma conferencia A de HOJE em $SAUDE_W (python -I -B -X utf8 saude_bancada.py --saida <essa pasta>; so' leitura) e retomar com CHAIN_DE=10"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada "$BANC_W" --producao --nos "$NOS_W" --versao v413 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --cadeia-de-selos "$W_CAD" --cadeia-de-selos-sha256 "$CAD" \
    --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-410
[ "$b3" = "0" ] || parar "o B(n) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$B/b3_recibo_v413.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio "$CAD" || parar "o recibo do B(n) ENSAIO nao confere"
fi
if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um, com recibo"
RP="$SERV/RECIBO_PARADA_v413.json"
[ -f "$RP" ] || aguarda "sem o recibo da PARADA ($RP): gerar com recibo_parada_v413.py (V413_AUTORIZACAO_OPERADOR=\"\$(cat <o AUTORIZACAO_v413.txt que montar_autorizacao_v413.py grava>)\"; V413_PARADA=ja_fora_do_ar com V413_SAUDE_RECIBO e V413_SAUDE_SHA256 da conferencia A de hoje, ou V413_PARADA=pelo_pid com V413_PID_PARADO e V413_PID_PARADO_CRIADO: a parada pelo PID e' ato do operador, nunca por nome)"
UR porta_fechada > /dev/null || parar "o servico da Bancada esta no AR (a porta responde) apesar do recibo de parada"
echo "  recibo da parada: $RP (sha256 $(UV sha256 "$(cygpath -w "$RP")")); porta fechada"
fi
if quer 10b; then
echo "== 10-bis. B(n) APLICAR, SALTO v411 -> v413, esboco R3.6 (grava o manifesto B21 na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "o APLICAR nao esta autorizado: evento c1 (evento_c1_b3_v413.py, depois do ENSAIO) + a autorizacao do operador (eventos 1687 e 1689 e a fala de 20/11). Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16>, com o servico parado e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o evento_c1_b3_v413.py imprime EVENTO=<seq> EVENTO_HASH=<hash16>)"
[ -f "$SERV/RECIBO_PARADA_v413.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
RPW="$SERV_W\\RECIBO_PARADA_v413.json"
MODO_P=$(UV json "$RPW" modo) || true
case "$MODO_P" in pelo_pid|ja_fora_do_ar) ;; *) parar "o recibo da parada nao diz o modo (pelo_pid | ja_fora_do_ar): '$MODO_P' (revisao B11)";; esac
[ "$(UV json "$RPW" autorizacao_conferida.evento_decisao.seq)" = "$(UV const SEQ_DECISAO)" ] || parar "o recibo da parada nao conferiu a decisao do operador (evento $(UV const SEQ_DECISAO)) (revisao B11)"
[ -f "$SEL/b3_ensaio_out.txt" ] || aguarda "sem o ENSAIO pos-selo (10): a ordem e' ENSAIO -> evento -> APLICAR"
b3_prepara 10b
$PY "$B/b3_recibo_v413.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio "$CAD" > /dev/null || parar "o ENSAIO pos-selo nao confere: o APLICAR so' vem depois de um ensaio que passa"
REC_E=$(UV recibo_do_stdout "$(cygpath -w "$SEL/b3_ensaio_out.txt")")
UR evento_depois_do_ensaio "$EVENTO" "$EVENTO_HASH" "$REC_E" || parar "2.6: o evento $EVENTO nao confere no livro (hash, autor, tipo) ou nao e' posterior ao fim do recibo do ensaio"
UR porta_fechada > /dev/null || parar "o servico esta no AR: o APLICAR exige o servico parado (o esboco recusa SERVICO_NO_AR)"
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(n): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada "$BANC_W" --producao --nos "$NOS_W" --versao v413 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --cadeia-de-selos "$W_CAD" --cadeia-de-selos-sha256 "$CAD" \
    --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-410
[ "$b3" = "0" ] || parar "o B(n) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$B/b3_recibo_v413.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar "$CAD" || parar "o recibo do B(n) APLICAR nao confere"
fi
if quer 10c; then
echo "== 10-ter. o religamento do servico (recibo_religamento_v413.py) e a reconexao dos adaptadores MCP (ato do operador)"
RR="$SERV/RECIBO_RELIGAMENTO_v413.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO ($RR): o recibo_religamento_v413.py religa (destacado, com os logs em estado\\servidor.log e estado\\servidor_erros.log, N9) e grava o recibo; exige V413_AUTORIZACAO_OPERADOR (o texto de montar_autorizacao_v413.py <fala do modo> <cpu|normal>), V413_MODO_PLACA=cpu|normal e V413_FALA_MODO_PLACA (a fala do operador com a escolha; sem ela, AGUARDA); reconectar os MCP e' ato do operador"
echo "  recibo do religamento: $RR (sha256 $(UV sha256 "$(cygpath -w "$RR")"))"
fi
if quer 11; then
echo "== 11. fechar: os tres recibos do B(n) juntos, o pino conjunto com o evento, a reconferencia e a entrega (fechar_bn_v413.py) $(date +%T)"
RR_W="$SERV_W\\RECIBO_RELIGAMENTO_v413.json"
[ -f "$(cygpath -u "$RR_W")" ] || aguarda "sem o recibo do religamento (10-ter): o passo 11 nao fecha sem ele"
PIDR=$(UV json "$RR_W" pid) || true
UR pid_vivo_um_bancada "$PIDR" > /dev/null || parar "portao C: o PID do recibo do religamento ($PIDR) nao esta' vivo como um_bancada.py"
set +e
$PY "$B/fechar_bn_v413.py"; rcf=$?
set -e
if [ "$rcf" = "2" ]; then aguarda "fechar_bn_v413.py: o elo B(n) nao esta' completo (faltam recibos; nada foi gravado)"; fi
[ "$rcf" = "0" ] || parar "fechar_bn_v413.py falhou (rc=$rcf)"
echo "FALTA (ato da gerencia, revisao B4): o aviso F0.6 no quadro apontando o pino conjunto (caminho e sha256) e os tres recibos, para o Codex encerrar a unidade: $PY \"$B/aviso_f06_v413.py\""
fi
echo "== FIM $(date +%T)"

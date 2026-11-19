#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/bateria_pre_selo/rodar_ensaio_1_pre_selo_v411.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/bateria_pre_selo__rodar_ensaio_1_pre_selo_v412.sh.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] o ensaio pre_selo contra o Nos v410 (canonico hoje), esboco e bateria pinados na v410 (lidos dos pinos); --versao v410; a saida (--saida) e o stdout em OUTB, lido do delta (no ensaio do topo proposto, a pasta de ensaio)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o ensaio pre_selo contra o Nos v409 (canonico hoje), com o esboco e a bateria pinados na v409 (lidos dos pinos); --versao v409; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v411 e em 06/11/2026 pelo fork B do claude-construtor-v411, com os rotulos subidos; na v412, adaptado em 12/11/2026 pelo fork B do claude-construtor-v412, retomada) molde v411/bateria_pre_selo/rodar_ensaio_1_pre_selo_v411.sh (rotulos subidos por _bump_copia_v412.py; diff em bump/); conferido linha a linha em 04/11/2026: o passo e' simples v411 -> v412, o esboco e a bateria sao os pinados na v411 (path e sha256 lidos dos pinos), nada de bundle nem de contagem de modulos aqui
# v412, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v411 (canonico hoje) com a Bancada de producao JA pinando a v411 (sem salto de versoes).
# Esboco R3.5 (pino esboco_R3_5 de v411/PINOS_BN_v411.json) e bateria da v411 (pino de v411/bateria_pos_selo/PINOS_BATERIA_v411.json, gerada depois do selo da v411 e usada no B(n) da v411):
# os dois sha256 esperados sao LIDOS dos pinos e conferidos contra o disco antes de rodar (nunca digitados). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# --versao v411 = a versao que o Nos tem agora (e que a Bancada pina). Sem --cadeia-de-selos (a Bancada nao esta atrasada: o esboco recusaria CADEIA_DE_SELOS_SEM_SALTO)
# e sem --recibo-pre-selo (so serve ao pos_selo). Veredito esperado: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA (o que o pos_selo da v412 exige do recibo pre_selo).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412"
V14="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411"
PY="python -I -B -X utf8"
cd "$V" || exit 9
# (v412) onde a bateria grava: no ensaio do topo proposto (V412_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v412) a pasta de ensaio, fora de work; no real, esta pasta (como na v411)
OUTB_W=$($PY -c "import importlib.util as u,os,sys; s=u.spec_from_file_location('d',sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m); print(os.path.join(m.SAIDA,'bateria_pre_selo') if m.ENSAIO_TOPO_PROPOSTO else sys.argv[2])" "$(cygpath -w "$V/delta_v412.py")" "$(cygpath -w "$V/bateria_pre_selo")" | tr -d '\r')
[ -n "$OUTB_W" ] || { echo "a pasta de saida da bateria nao foi lida do delta_v412"; exit 9; }
OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"
SAIDA="$OUTB_W\\ensaio_1"
OUT="$OUTB/etapa1_stdout.txt"
pinow() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]][sys.argv[3]])" "$(cygpath -w "$1")" "$2" "$3" | tr -d '\r'; }
sha256w() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1" | tr -d '\r'; }
ESB=$(pinow "$V14/PINOS_BN_v411.json" esboco_R3_5 path)
ESB_PINO=$(pinow "$V14/PINOS_BN_v411.json" esboco_R3_5 sha256)
ESB_SHA=$(sha256w "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BAT=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v411.json" bateria path)
BAT_PINO=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v411.json" bateria sha256)
BAT_SHA=$(sha256w "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
$PY "$ESB" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v411 --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"

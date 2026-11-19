#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/bateria_pre_selo/rodar_bn_pre_selo_v411.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/bateria_pre_selo__rodar_bn_pre_selo_v412.sh.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] a ordem dos passos da v410; o B(n) pre-selo da v411 e' o passo simples B20 (a producao pina a v410); os passos 8 e 9 chamam diff_e_pinos_v411 e p00_precondicoes_v411 (que leem o modo pelo ambiente); as saidas em OUTB, lido do delta (no ensaio do topo proposto, a pasta de ensaio)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a ordem dos passos da v409; passos 8 e 9 chamam diff_e_pinos_v410 e p00_precondicoes_v410; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v411 e em 06/11/2026 pelo fork B do claude-construtor-v411, com os rotulos subidos; na v412, adaptado em 12/11/2026 pelo fork B do claude-construtor-v412, retomada) molde v411/bateria_pre_selo/rodar_bn_pre_selo_v411.sh (rotulos subidos por _bump_copia_v412.py; diff em bump/); conferido em 04/11/2026: (1) os cinco scripts da v412 JA existem (nasceram da subida mecanica e foram adaptados a mao); o derivador da v411 nao se aplica
# (ver derivar_pre_selo_v412.py) e o que faltar PARA a corrida, em vez de ser rederivado; (2) os passos 4, 6, 8 e 9 NAO mascaram mais o codigo de saida pelo pipe `| tail` (o molde mascarava: RC_BN=0 mesmo com conferencia ou p00 reprovando);
# o codigo de saida de cada um e' impresso (RC_CONFERENCIA, RC_PINO, RC_DIFF_PINOS, RC_P00) e o desta corrida e' 0 so' se 4, 6 e 8 sairam 0 (o p00 e' o veredito da cadeia INTEIRA, inclusive de arquivos de outros: o veredito dele vem no texto e em RC_P00).
# v412, elo B(n), fase pre_selo, na ordem da v411 (NOTAS_PRE_SELO_v411.txt, TAREFA 1): fotografa a producao (antes); roda o ensaio da Bancada (so' leitura da producao e do Nos v411; grava so' em --saida); fotografa (depois); confere o recibo pelo proprio esboco R3.5
# (23 condicoes + 5 controles negativos); fotografa (final); gera PINO_RECIBO_PRE_SELO_v412.json e PROVA_PRODUCAO_INTACTA_v412_pre_selo.json em v412\; apaga o sandbox curto C:\t\vb23;
# e entao fecha a preparacao: diff_e_pinos_v412.py (regrava PINOS_BN_v412.json, DIFF_KERNEL_v412.txt e DIFF_v411_v412.diff) e p00_precondicoes_v412.py (regrava PRECONDICOES_v412.json). Nao toca o Nos, nao instala, nao roda o rito, nao grava na Bancada, nao para nem religa servico.
# uso: sh ./rodar_bn_pre_selo_v412.sh > bn_pre_selo_out_v412.txt 2>&1        (quem chama pode acrescentar `echo "RC_BN=$?"`, como o fim_de_cadeia_v412.sh)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412"
B="$V/bateria_pre_selo"
PY="/c/Python314/python.exe -I -B -X utf8"
SNAP='C:\t\vb23\snap'
cd "$B"
# (v412) onde a bateria grava: no ensaio do topo proposto (V412_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v412) a pasta de ensaio, fora de work; no real, esta pasta (como na v411)
OUTB_W=$($PY -c "import importlib.util as u,os,sys; s=u.spec_from_file_location('d',sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m); print(os.path.join(m.SAIDA,'bateria_pre_selo') if m.ENSAIO_TOPO_PROPOSTO else sys.argv[2])" "$(cygpath -w "$V/delta_v412.py")" "$(cygpath -w "$B")" | tr -d '\r')
[ -n "$OUTB_W" ] || { echo "a pasta de saida da bateria nao foi lida do delta_v412"; exit 9; }
OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"
echo "saidas da bateria em $OUTB_W"
for f in rodar_ensaio_1_pre_selo_v412.sh snap_producao_v412.py conferir_recibo_pre_selo_v412.py gerar_pino_recibo_pre_selo_v412.py limpar_sandbox_vb23.py; do
  [ -f "$f" ] || { echo "FALTA $f -- NAO RODO (os cinco scripts da v412 nao sao rederivados; ver _bump_copia_v412.py e bump/)"; exit 9; }
done
if grep -l '^# \[A ADAPTAR v412\]' rodar_ensaio_1_pre_selo_v412.sh snap_producao_v412.py conferir_recibo_pre_selo_v412.py gerar_pino_recibo_pre_selo_v412.py limpar_sandbox_vb23.py rodar_bn_pre_selo_v412.sh; then echo "algum script ainda traz a marca de adaptacao pendente (A ADAPTAR v412, no comeco da 2a linha) -- NAO RODO"; exit 9; fi
ls -la
if [ -e /c/t/vb23 ]; then echo "C:\\t\\vb23 ja existe -- NAO RODO (limpe antes)"; exit 9; fi
mkdir -p /c/t/vb23/snap
echo "== 1. snap antes $(date +%T)"; $PY snap_producao_v412.py antes "$SNAP"
echo "== 2. ensaio 1 da Bancada (pre_selo, ensaio) $(date +%T)"; sh ./rodar_ensaio_1_pre_selo_v412.sh || true
tail -3 "$OUTB/etapa1_stdout.txt"
grep -q "ETAPA1_RC=0" "$OUTB/etapa1_stdout.txt" || { echo "ETAPA1 FALHOU"; exit 1; }
echo "== 3. snap depois $(date +%T)"; $PY snap_producao_v412.py depois "$SNAP"
echo "== 4. conferir o recibo pelo esboco R3.5 $(date +%T)"; RC_CONFERENCIA=0; $PY conferir_recibo_pre_selo_v412.py > "$OUTB/conferencia_out_v412.txt" 2>&1 || RC_CONFERENCIA=$?; tail -4 "$OUTB/conferencia_out_v412.txt"; echo "RC_CONFERENCIA=$RC_CONFERENCIA"
echo "== 5. snap final $(date +%T)"; $PY snap_producao_v412.py final "$SNAP"
echo "== 6. gerar o pino do recibo e a prova da producao intacta $(date +%T)"; RC_PINO=0; $PY gerar_pino_recibo_pre_selo_v412.py "$SNAP" > "$OUTB/pino_out_v412.txt" 2>&1 || RC_PINO=$?; tail -4 "$OUTB/pino_out_v412.txt"; echo "RC_PINO=$RC_PINO"
echo "== 7. limpar o sandbox curto $(date +%T)"; $PY limpar_sandbox_vb23.py | tail -2
cd "$V"
echo "== 8. diff_e_pinos_v412.py $(date +%T)"; RC_DIFF_PINOS=0; $PY diff_e_pinos_v412.py > "$OUTB/diff_e_pinos_out_v412.txt" 2>&1 || RC_DIFF_PINOS=$?; tail -2 "$OUTB/diff_e_pinos_out_v412.txt"; echo "RC_DIFF_PINOS=$RC_DIFF_PINOS"
echo "== 9. p00_precondicoes_v412.py $(date +%T)"; RC_P00=0; $PY p00_precondicoes_v412.py > "$OUTB/p00_out_v412.txt" 2>&1 || RC_P00=$?; tail -16 "$OUTB/p00_out_v412.txt"; echo "RC_P00=$RC_P00 (0 = TODAS PASSARAM; 3 = sem falha e com pendente; 1 = falhou)"
echo "== FIM $(date +%T)"
if [ "$RC_CONFERENCIA" != 0 ] || [ "$RC_PINO" != 0 ] || [ "$RC_DIFF_PINOS" != 0 ]; then echo "FALHOU: conferencia=$RC_CONFERENCIA pino=$RC_PINO diff_e_pinos=$RC_DIFF_PINOS"; exit 1; fi

#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/regerar_v411.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/regerar_v412.sh.diff
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/regerar_v410.sh para uma versao SEM modulo novo: a guarda do sandbox deixa de conferir um bundle (nao ha) e passa a conferir que as FONTES do sandbox k411c sao as do kernel do Nos v410 (conferir_fontes_k410c_vs_nos_v411.py); build incremental, pos_build, insumos e refazer_candidato
# regerar_v412.sh -- refaz, NA ORDEM, o que depende do KERNEL e dos INSUMOS da v412 (a v412 NAO tem modulo novo: o kernel e' o da v411 byte a byte): (a) guarda do sandbox (as fontes de C:\t\k412c\final == as do kernel do Nos v411, por sha256),
# (b) construir_kernel_v412.sh (`lake build` incremental, nada a compilar, + Audit no sandbox), (c) pos_build_kernel_v412.py (FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD), (d) copiar_insumos_v412.py e (e) refazer_candidato_v412.sh --regerar
# (a cadeia inteira). Nao toca o Nos, nao instala, nao roda o rito. O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox (ele nasce de `sh ./copiar_k412c.sh`, robocopy de C:\t\k411c\final SEM /PURGE). O kernel ja' esta' medido
# (PRONTO_PARA_CANDIDATO_v412.json): NAO refazer o build nem o Audit sem mudanca de fonte. O build incremental levou 85 s e o Audit 432 s (kernel/construir_marcas.txt, 12/11/2026). Depois: python -I -B -X utf8 purga_v412.py (tem de dar ZERO; ~20 min, por fora).
# uso: sh ./regerar_v412.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v412"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: as fontes de C:\\t\\k412c\\final == as do kernel do Nos v411 selado (sha256; nada so' num lado) $(date +%T)"
$PY conferir_fontes_k411c_vs_nos_v412.py "C:\\t\\k412c\\final" CONFERENCIA_FONTES_K412C_v412.json > /tmp/regerar_a_v412.txt; tail -1 /tmp/regerar_a_v412.txt
$PY -c "
import json
c = json.load(open('CONFERENCIA_FONTES_K412C_v412.json', encoding='utf-8'))
assert c['identico'] is True and c['n_diferentes'] == 0, c.get('n_diferentes')
print('sandbox k412c == kernel do Nos v411:', c['n_comuns'], 'arquivos comuns, 0 diferentes')"
echo "== b. construir_kernel_v412.sh (lake build incremental + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v412.sh
echo "== c. pos_build_kernel_v412.py (tem de dar VERDE)"; $PY pos_build_kernel_v412.py > /tmp/regerar_c_v412.txt; tail -1 /tmp/regerar_c_v412.txt
echo "== d. copiar_insumos_v412.py"; $PY copiar_insumos_v412.py > /tmp/regerar_d_v412.txt; tail -1 /tmp/regerar_d_v412.txt
echo "== e. refazer_candidato_v412.sh --regerar $(date +%T)"; sh ./refazer_candidato_v412.sh --regerar
echo "== FIM $(date +%T)"

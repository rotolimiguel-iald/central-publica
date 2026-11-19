#!/bin/sh
# [A ADAPTAR v412] SUBIDA MECANICA DE ROTULO (v411->v412) do molde v411/cadeia_v411.sh; o CORPO e' o da v411 (versao SEM modulo novo, registro com funcao h0dn_bg1_v411): o que depende de bundle nao vazio se adapta pelo molde v410/v409; nada rodou; ver bump/cadeia_v412.sh.diff
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1; refeita na retomada (12/11, tarde) para a cadeia REAL] a SEQUENCIA EXATA que, existindo TOPO_RATIFICADO_v411.json (da gerencia), gera o candidato e leva a preparacao ate PREPARACAO_v411_PRONTA.json.
# Molde: cadeia_parte2_v411.sh + refazer_candidato_v411.sh. Fail-closed: para no primeiro passo que falha; PARA tambem (rc 4) se o script do passo ainda trouxer a marca de copia mecanica de rotulo.
# Os passos da OUTRA frente (pos_rito\: derivacao, harnesses, previa do X) sao chamados PELO NOME, dentro do fim_de_cadeia_v412.sh (fork B). A citacao em «» do escopo do pos-rito (a outra frente) devolve rc 2 no
# conferir_citacoes: o passo aceita rc 2 SO' ai (o escopo do um.py tem de estar limpo); o relatorio final exige os dois escopos (o portao nao muda).
# Nada no Nos; nada roda do pacote do teste alem do carregamento por bytes (dentro do registro); o executor da abertura NUNCA roda. Saida em cadeia_v412_out.txt.
# uso: sh ./cadeia_v412.sh            (REAL: exige TOPO_RATIFICADO_v412.json; o candidato que ja existe so' se reproduz identico, senao V412_REGERAR=1 e' decisao da gerencia)
#      V412_ENSAIO_TOPO_PROPOSTO=1 sh ./cadeia_v412.sh   (ENSAIO do topo proposto: tudo em C:\t\k412c\ensaio_topo_proposto; nada e' candidato)
cd "$(dirname "$0")" || exit 9
PY="/c/Python314/python.exe -B -X utf8"; PYI="/c/Python314/python.exe -I -B -X utf8"
OUT="cadeia_v412_out.txt"
[ "$V412_ENSAIO_TOPO_PROPOSTO" = "1" ] && OUT="/c/t/k412c/ensaio_topo_proposto/cadeia_v412_out.txt"
MARCA="[A ADAPTAR v""412]"
echo "inicio $(date '+%Y-%m-%d %H:%M:%S') ensaio=${V412_ENSAIO_TOPO_PROPOSTO:-0}" > "$OUT"
if [ "$V412_ENSAIO_TOPO_PROPOSTO" != "1" ]; then
  [ -f TOPO_RATIFICADO_v412.json ] || { echo "PARADO: TOPO_RATIFICADO_v412.json ausente (DESENHO 5.1 b; ato da gerencia)" | tee -a "$OUT"; exit 2; }
fi
ARQ_CAND=$($PY -c "import sys; sys.path.insert(0, '.'); import delta_v412 as DL; print(DL.CANDIDATO_ARQ)")
passo() {   # passo <rotulo> <arquivo do script> <rcs aceitos (ex.: 0 ou 0,2)> <comando...>
  rot="$1"; arq="$2"; aceitos="$3"; shift 3
  if grep -qF "$MARCA" "$arq" 2>/dev/null; then echo "PARADO no passo $rot: $arq ainda e' copia mecanica de rotulo (adaptar antes)" | tee -a "$OUT"; exit 4; fi
  echo "== $rot ($(date '+%H:%M:%S')): $*" >> "$OUT"
  "$@" >> "$OUT" 2>&1; rc=$?
  echo "   rc=$rc" >> "$OUT"
  case ",$aceitos," in *",$rc,"*) : ;; *) echo "PARADO no passo $rot: rc=$rc (ver $OUT)" | tee -a "$OUT"; exit 1 ;; esac
}
passo 00a_recibo_do_kernel  complementar_recibo_kernel_v412.py 0  $PY complementar_recibo_kernel_v412.py
passo 00b_insumos           copiar_insumos_v412.py         0      $PY copiar_insumos_v412.py
passo 01_registro_offline   _teste_h0dn_offline_v412.py    0      $PY _teste_h0dn_offline_v412.py
passo 02_guarda_frases      guarda_frases_v412.py          0      $PY guarda_frases_v412.py
passo 03_quadro_renderizado _teste_quadro_v412.py          0      $PY _teste_quadro_v412.py
passo 04_citacoes           conferir_citacoes_v412.py      0,2    $PYI conferir_citacoes_v412.py
passo 05_candidato          gerar_candidato_v412.py        0      $PY gerar_candidato_v412.py
passo 06_comparar           comparar_v411_v412.py          0      $PYI comparar_v411_v412.py
passo 07_ensaio_a_seco      ensaio_a_seco_v412.py          0      $PY ensaio_a_seco_v412.py "$ARQ_CAND" v412
passo 08_esperados          gerar_esperados_v412.py        0      $PYI gerar_esperados_v412.py
passo 09_conferidor_negativo conferir_rito_v412.py         0      $PY conferir_rito_v412.py --controle-negativo
passo 10_conferidor_positivo teste_conferidor_positivo_v412.py 0  $PY teste_conferidor_positivo_v412.py
passo 11_citacoes_candidato conferir_citacoes_v412.py      0,2    $PYI conferir_citacoes_v412.py --candidato
passo 12_diff_e_pinos       diff_e_pinos_v412.py           0      $PYI diff_e_pinos_v412.py
passo 13_instalar_rito      conferir_instalar_rito_v412.py 0      $PYI conferir_instalar_rito_v412.py
passo 14_p00                p00_precondicoes_v412.py       0,3    $PYI p00_precondicoes_v412.py
# (A1, integracao de 12/11) a regeneracao do candidato fica COMPROVADA aqui, onde o refazer da v411 terminava (no p00): refazer_out_v412.txt = a saida da cadeia ate' este ponto + a linha `== FIM`; os dois harnesses do pos-rito (passo 15) exigem esse arquivo, com `== FIM` e mais novo que o ESPERADOS_v412.json (gravado no passo 08). So' no modo real: no ensaio do topo proposto a regeneracao e' o PRONTO_PARA_O_POS_RITO.json.
if [ "$V412_ENSAIO_TOPO_PROPOSTO" != "1" ]; then { cat "$OUT"; echo "== FIM $(date '+%H:%M:%S') (refazer comprovado no p00; passos 00a a 14)"; } > refazer_out_v412.txt; fi
passo 15_fim_de_cadeia_B20  fim_de_cadeia_v412.sh          0      sh ./fim_de_cadeia_v412.sh
# (G2, integracao de 12/11) a varredura OFICIAL do Fock/Omega (so' leitura; grava VARREDURA_FOCK_OMEGA_v412.json; rc 1 se ha' achado NOVO) corre depois do fim_de_cadeia (le os textos que o harness dos textos rendeu em C:/t/h412 e as fontes de pos_rito/) e antes do relatorio, que a exige (portao varredura_fock_omega).
passo 15_varredura_fock_omega varredura_fock_omega_v412.py 0   $PYI varredura_fock_omega_v412.py
passo 16_purga              purga_v412.py                  0      $PYI purga_v412.py --listar
passo 17_p00_final          p00_precondicoes_v412.py       0,3    $PYI p00_precondicoes_v412.py
passo 18_relatorio          gerar_relatorio_v412.py        0      $PY gerar_relatorio_v412.py
find . -name "*.tmp" -print -delete >> "$OUT" 2>&1
echo "fim $(date '+%Y-%m-%d %H:%M:%S') rc=0" >> "$OUT"
$PYI -c "import json, sys; sys.path.insert(0, '.'); import delta_v412 as DL; j = json.load(open(DL.saida('PREPARACAO_v412_PRONTA.json'), encoding='utf-8')); print('PREPARACAO_v412_PRONTA.json: pronta =', j.get('pronta'), '| falta:', json.dumps(j.get('falta'), ensure_ascii=False)[:600])" | tee -a "$OUT"
echo "OK: a cadeia chegou ao relatorio (a revisao de terceiro, fechar_preparacao, acom_inscrever_prep, o pino do memoria.py e a folga do MEMORY.md sao da gerencia)"

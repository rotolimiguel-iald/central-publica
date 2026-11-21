#!/bin/sh
# Constroi o kernel do SANDBOX da v413 (C:\t\k413c\final; NUNCA o do Nos). Gerado por preparar_bundle_v413.py (claude-construtor-v413) em 20261120_204644; nao editar a mao (regerar pelo preparo).
# Molde: v412\construir_kernel_v412.sh. Diferenca: primeiro o modulo que a v413 corrige so' no texto (TGLExt.OResumoEPsiBit), depois os 21 modulos novos, UM A UM, na ordem topologica das dependencias
# (`lake build +<modulo>`); o script PARA no primeiro que nao compilar (marca `parou_em=` e nao roda o resto nem o Audit); so' depois vem o `lake build` inteiro (os modulos antigos que dependem
# do corrigido, a raiz e o TGL.Audit) e o Audit (`lake env lean TGL/Audit.lean`).
# O build e' INCREMENTAL no que e' antigo e nao depende do corrigido (o kernel da v412 ja compilado em .lake/build, copiado do k412c) e A FRIO nos modulos novos. Marcas em kernel/construir_marcas.txt.
K="/c/t/k413c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/kernel"
LAKE=/c/Users/rotol/.elan/bin/lake
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log construir_marcas.txt; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
: > "$D/lake_build.log"
rb=0
for m in TGLExt.OResumoEPsiBit TGLExt.AIdentidadePreservada TGLExt.APonteDeCookLevin TGLExt.APropostaDaTensao TGLExt.ONomeEBeta TGLExt.Operador TGLExt.APonteAoTM2 TGLExt.LeituraBeta TGLExt.Reconstrucao TGLExt.RelogioBeta TGLExt.Trinity TGLExt.AFronteiraNaLinguaClassica TGLExt.AMaquinaTM2DaVerificacao TGLExt.PonteLeituraBeta TGLExt.QuantizacaoBeta TGLExt.EntregaBeta TGLExt.SimBase TGLExt.SimExterior TGLExt.SimLiteral TGLExt.SondaContagem TGLExt.SimCompleta TGLExt.PonteCookLevin; do
  t0=$(date +%s)
  echo "=== MODULO $m (inicio $(date '+%H:%M:%S'))" >> "$D/lake_build.log"
  $LAKE build "+$m" >> "$D/lake_build.log" 2>&1; r=$?
  echo "modulo=$m rc=$r s=$(( $(date +%s) - t0 ))" >> "$D/construir_marcas.txt"
  if [ "$r" != "0" ]; then rb=$r; echo "parou_em=$m" >> "$D/construir_marcas.txt"; break; fi
done
if [ "$rb" = "0" ]; then
  echo "=== BUILD INTEIRO (inicio $(date '+%H:%M:%S'))" >> "$D/lake_build.log"
  $LAKE build >> "$D/lake_build.log" 2>&1; rb=$?
fi
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ]; then
  $LAKE env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
else
  ra=99; echo "o Audit NAO rodou: o build parou (rc_build=$rb)" > "$D/audit.log"
fi
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"

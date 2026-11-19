#!/usr/bin/env bash
# Revisor K02: recompila as 4 candidatas com o binario lean direto, saida (.olean/log) SO na pasta do revisor.
# Le (somente leitura) os .olean ja existentes das dependencias do kernel; nunca executa lake nem escreve la.
set -u
REV='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k02'
SRC='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K02\candidatas'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
mkdir -p "$REV/src" "$REV/build"
cp "$SRC/"*.lean "$REV/src/"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"; fi
done
export LEAN_PATH
for name in T1 MONTAGEM_3MAIS1 GH_III1 TAU_ESTRELA; do
  log="$REV/build/$name.revisor.log"
  : > "$log"
  "$LEAN" --version >> "$log" 2>&1
  (cd "$REV" && "$LEAN" -o "build/$name.olean" "src/$name.lean") >> "$log" 2>&1
  echo "RC: $?" >> "$log"
  echo "== $name"; cat "$log"
done

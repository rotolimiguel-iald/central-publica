#!/usr/bin/env bash
# Revisor K05/T1: recompila T1_R2.lean com o binario lean direto; saida so na pasta do revisor.
# Le (somente leitura) os .olean ja existentes das dependencias do kernel; nunca executa lake nem escreve la.
set -u
REV='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_t1'
SRC='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K05\candidatas'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
mkdir -p "$REV/src" "$REV/build"
cp "$SRC/T1_R2.lean" "$REV/src/T1_R2.lean"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"; fi
done
export LEAN_PATH
log="$REV/build/T1_R2.revisor.log"
: > "$log"
"$LEAN" --version >> "$log" 2>&1
(cd "$REV" && "$LEAN" -o "build/T1_R2.olean" "src/T1_R2.lean") >> "$log" 2>&1
echo "RC: $?" >> "$log"
cat "$log"

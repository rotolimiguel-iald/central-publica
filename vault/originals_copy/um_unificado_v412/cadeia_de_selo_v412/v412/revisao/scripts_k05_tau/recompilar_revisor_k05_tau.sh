#!/usr/bin/env bash
# Revisor K05/tau: recompila a candidata TAU_ESTRELA_R2.lean (e uma copia com #print axioms extras)
# com lean.exe direto (nunca lake); saida (.olean/log) SO na pasta do revisor.
# Le (somente leitura) os .olean de Mathlib do kernel.
set -u
REV='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k05_tau'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
mkdir -p "$REV/src" "$REV/build"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"; fi
done
export LEAN_PATH
for name in TAU_ESTRELA_R2 TAU_REV_EXTRA; do
  log="$REV/build/$name.revisor.log"
  : > "$log"
  "$LEAN" --version >> "$log" 2>&1
  (cd "$REV" && "$LEAN" -o "build/$name.olean" "src/$name.lean") >> "$log" 2>&1
  echo "RC: $?" >> "$log"
  echo "== $name"; cat "$log"
done

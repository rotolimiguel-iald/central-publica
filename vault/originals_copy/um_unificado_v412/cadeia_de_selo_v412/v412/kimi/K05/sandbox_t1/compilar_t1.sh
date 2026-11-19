#!/usr/bin/env bash
# Compila somente a candidata T1_R2 no sandbox; nunca executa lake/build.
set -u
BASE='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K05'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
cp "$BASE/candidatas/T1_R2.lean" "$BASE/sandbox_t1/sources/T1_R2.lean"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"
  fi
done
export LEAN_PATH
log="$BASE/sandbox_t1/logs/T1_R2.log"
printf 'COMMAND: "%s" -o "build/T1_R2.olean" "sources/T1_R2.lean"\n' "$LEAN" > "$log"
printf 'LEAN_VERSION: ' >> "$log"
"$LEAN" --version >> "$log" 2>&1
(cd "$BASE/sandbox_t1" && "$LEAN" -o "build/T1_R2.olean" "sources/T1_R2.lean") >> "$log" 2>&1
rc=$?
printf 'RC: %s\n' "$rc" >> "$log"
printf 'T1_R2 rc=%s\n' "$rc"
exit "$rc"

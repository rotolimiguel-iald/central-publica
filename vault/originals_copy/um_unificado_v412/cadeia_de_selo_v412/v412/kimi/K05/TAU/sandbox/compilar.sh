#!/usr/bin/env bash
# Compila somente no sandbox K05/TAU; nunca executa lake/build no kernel canônico.
set -u
BASE='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K05\TAU'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
NAME='TAU_ESTRELA_R2'
mkdir -p "$BASE/sandbox/sources" "$BASE/sandbox/build" "$BASE/sandbox/logs"
cp "$BASE/candidatas/$NAME.lean" "$BASE/sandbox/sources/$NAME.lean"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"
  fi
done
export LEAN_PATH
log="$BASE/sandbox/logs/$NAME.log"
printf 'COMMAND: "%s" -o "build/%s.olean" "sources/%s.lean"\n' "$LEAN" "$NAME" "$NAME" > "$log"
printf 'LEAN_VERSION: ' >> "$log"
"$LEAN" --version >> "$log" 2>&1
(cd "$BASE/sandbox" && "$LEAN" -o "build/$NAME.olean" "sources/$NAME.lean") >> "$log" 2>&1
rc=$?
printf 'RC: %s\n' "$rc" >> "$log"
printf '%s rc=%s\n' "$NAME" "$rc"
exit "$rc"

#!/usr/bin/env bash
# Compila somente no sandbox K02; nunca executa lake/build no kernel canônico.
set -u
BASE='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K02'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
cp "$BASE/candidatas/"*.lean "$BASE/sandbox/sources/"
LEAN_PATH=''
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then
    LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"
  fi
done
export LEAN_PATH
rc_all=0
for name in T1 MONTAGEM_3MAIS1 GH_III1 TAU_ESTRELA; do
  log="$BASE/sandbox/logs/$name.log"
  printf 'COMMAND: "%s" -o "build/%s.olean" "sources/%s.lean"\n' "$LEAN" "$name" "$name" > "$log"
  printf 'LEAN_VERSION: ' >> "$log"
  "$LEAN" --version >> "$log" 2>&1
  (cd "$BASE/sandbox" && "$LEAN" -o "build/$name.olean" "sources/$name.lean") >> "$log" 2>&1
  rc=$?
  printf 'RC: %s\n' "$rc" >> "$log"
  printf '%s rc=%s\n' "$name" "$rc"
  if [ "$rc" -ne 0 ]; then
    rc_all=1
  fi
done
exit "$rc_all"

#!/usr/bin/env bash
# Revisor K06/formal: recompila a candidata LeitorFinito.lean (copia identica por sha256) e a copia
# LeitorFinito_REV.lean (com #print axioms para cada teorema e exemplos de nao-vacuidade)
# com lean.exe 4.31.0 direto (nunca lake). LEAN_PATH aponta so para os .olean do kernel e dos pacotes.
# Saida (.olean e log) SO na pasta do revisor.
set -u
REV='C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\revisao\scripts_k06_formal'
KERNEL='C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
LEAN='C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
mkdir -p "$REV/src" "$REV/build"
LEAN_PATH="$KERNEL\\.lake\\build\\lib\\lean"
for p in Cli LeanSearchClient Qq aesop batteries importGraph mathlib plausible proofwidgets; do
  d="$KERNEL/.lake/packages/$p/.lake/build/lib/lean"
  if [ -d "$d" ]; then LEAN_PATH="${LEAN_PATH:+$LEAN_PATH;}$d"; fi
done
export LEAN_PATH
for name in "$@"; do
  log="$REV/build/$name.revisor.log"
  : > "$log"
  "$LEAN" --version >> "$log" 2>&1
  (cd "$REV" && "$LEAN" -o "build/$name.olean" "src/$name.lean") >> "$log" 2>&1
  echo "RC: $?" >> "$log"
  echo "== $name"; cat "$log"
done

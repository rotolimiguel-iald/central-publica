# -*- coding: utf-8 -*-
"""reconstruir_kernel_v412.py -- (claude-construtor-v412, 17/11/2026) O COMANDO UNICO para TROCAR UMA FONTE e reconstruir so' o que depende dela (ordem da Etapa 1: a ordem 023 pode mudar texto de
sete fontes e a gerencia regera o manifesto). Encadeia, parando no primeiro passo que falha:
  1. preparar_bundle_v412.py   (confere o sha256 de toda copia congelada contra o manifesto; regrava no sandbox SO' o modulo cujo texto instalado mudou, com o antigo na quarentena; a raiz so' se mudar);
  2. C:\\t\\k412c\\run_build.py  (construir_kernel_v412.sh: `lake build +<modulo>` na ordem topologica -- o lake recompila so' o modulo trocado e os que dependem dele; os outros saem em segundos --,
                                 depois o `lake build` inteiro (a raiz e o TGL.Audit) e o Audit; para no primeiro modulo que nao compilar);
  3. pos_build_kernel_v412.py  (as medicoes, a escada, as bandeiras, os recibos em kernel\\);
  4. copiar_logs_do_kernel_v412.py (confere os logs contra os recibos; nao grava).
So' no sandbox C:\\t\\k412c\\final; nada toca o Nos. Quem depende de quem e o que o lake vai recompilar ficam em kernel\\ULTIMA_INSTALACAO_v412.json (escrito pelo passo 1).
uso: C:\\Python314\\python.exe -B -X utf8 reconstruir_kernel_v412.py [--manifesto <json>] [--pedras <pasta>] [--so-preparar]
(o build demora: o Audit sozinho leva ~7 min; rode em segundo plano se preferir)"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"
extra = []
for k in ("--manifesto", "--pedras"):
    if k in sys.argv:
        extra += [k, sys.argv[sys.argv.index(k) + 1]]


def passo(nome, cmd, cwd=HERE):
    print("==", nome, flush=True)
    r = subprocess.run(cmd, cwd=cwd)
    print("== %s rc=%d" % (nome, r.returncode), flush=True)
    if r.returncode != 0:
        print("PAROU em", nome); sys.exit(r.returncode or 1)


passo("1 preparar_bundle_v412", [PY, "-B", "-X", "utf8", os.path.join(HERE, "preparar_bundle_v412.py")] + extra)
if "--so-preparar" in sys.argv:
    sys.exit(0)
passo("2 build e Audit no sandbox k412c", [PY, "-B", os.path.join("C:" + os.sep, "t", "k412c", "run_build.py")], cwd=os.path.join("C:" + os.sep, "t", "k412c"))
rc_build = open(os.path.join(HERE, "kernel", "construir_rc.txt"), encoding="utf-8").read().strip()
print("construir_rc.txt:", rc_build)
passo("3 pos_build_kernel_v412", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "pos_build_kernel_v412.py")])
passo("4 copiar_logs_do_kernel_v412 (conferencia)", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "copiar_logs_do_kernel_v412.py")])
print("RECONSTRUCAO DO KERNEL v412: TUDO PASSOU")

# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\reconstruir_kernel_v412_r7.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de reconstruir_kernel_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_02_derivar_kernel_v412.py). O original fica intacto.
# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R11)] copia de reconstruir_kernel_v412_c4.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 153 modulos); e5_02_derivar_scripts_r7_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de reconstruir_kernel_v412_r3.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de reconstruir_kernel_v412_r2.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de reconstruir_kernel_v412.py: o padrao passa a ser a DECIMA SEGUNDA lista (insumos\MANIFESTO_PEDRAS_v412_R12.json + insumos\pedras_r12) e o passo 3 e' o pos_build_kernel_v412_r7.py; --manifesto/--pedras ainda valem. Para trocar uma fonte: regerar o manifesto e rodar este comando.
"""reconstruir_kernel_v413.py -- (claude-construtor-v412, 17/11/2026) O COMANDO UNICO para TROCAR UMA FONTE e reconstruir so' o que depende dela (ordem da Etapa 1 da v413: a leitura de terceiro pode mudar docstrings;
a gerencia regera o manifesto e roda este comando). Encadeia, parando no primeiro passo que falha:
  1. preparar_bundle_v413.py   (confere o sha256 de toda pedra limpa e da fonte corrigida contra o manifesto; regrava no sandbox SO' o modulo cujo texto instalado mudou, com o antigo na quarentena; a raiz so' se mudar);
  2. C:\\t\\k413c\\run_build.py  (construir_kernel_v413.sh: `lake build +<modulo>` na ordem topologica -- o lake recompila so' o modulo trocado e os que dependem dele; os outros saem em segundos --,
                                 depois o `lake build` inteiro (a raiz e o TGL.Audit) e o Audit; para no primeiro modulo que nao compilar);
  3. pos_build_kernel_v413.py  (as medicoes, a escada, as bandeiras, os recibos em kernel\\);
  4. copiar_logs_do_kernel_v413.py (confere os logs contra os recibos; nao grava).
So' no sandbox C:\\t\\k413c\\final; nada toca o Nos. Quem depende de quem e o que o lake vai recompilar ficam em kernel\\ULTIMA_INSTALACAO_v413.json (escrito pelo passo 1).
uso: C:\\Python314\\python.exe -B -X utf8 reconstruir_kernel_v413.py [--manifesto <json>] [--pedras <pasta>] [--kernel-edits <pasta>] [--so-preparar]
(o build demora: o Audit sozinho leva ~7 min; rode em segundo plano se preferir)"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"
extra = []
PADRAO = {"--manifesto": os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413.json"), "--pedras": os.path.join(HERE, "insumos", "pedras_limpas", "TGLExt")}   # (v413: o manifesto e as pedras limpas da gerencia)
for k in ("--manifesto", "--pedras"):
    extra += [k, sys.argv[sys.argv.index(k) + 1] if k in sys.argv else PADRAO[k]]
if "--kernel-edits" in sys.argv:   # (padrao: a pasta do campo saida do manifesto)
    extra += ["--kernel-edits", sys.argv[sys.argv.index("--kernel-edits") + 1]]


def passo(nome, cmd, cwd=HERE):
    print("==", nome, flush=True)
    r = subprocess.run(cmd, cwd=cwd)
    print("== %s rc=%d" % (nome, r.returncode), flush=True)
    if r.returncode != 0:
        print("PAROU em", nome); sys.exit(r.returncode or 1)


passo("1 preparar_bundle_v413", [PY, "-B", "-X", "utf8", os.path.join(HERE, "preparar_bundle_v413.py")] + extra)
if "--so-preparar" in sys.argv:
    sys.exit(0)
passo("2 build e Audit no sandbox k413c", [PY, "-B", os.path.join("C:" + os.sep, "t", "k413c", "run_build.py")], cwd=os.path.join("C:" + os.sep, "t", "k413c"))
rc_build = open(os.path.join(HERE, "kernel", "construir_rc.txt"), encoding="utf-8").read().strip()
print("construir_rc.txt:", rc_build)
passo("3 pos_build_kernel_v413", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "pos_build_kernel_v413.py")])
passo("4 copiar_logs_do_kernel_v413 (conferencia)", [PY, "-I", "-B", "-X", "utf8", os.path.join(HERE, "copiar_logs_do_kernel_v413.py")])
print("RECONSTRUCAO DO KERNEL v413 (os modulos novos e o corrigido): TUDO PASSOU")

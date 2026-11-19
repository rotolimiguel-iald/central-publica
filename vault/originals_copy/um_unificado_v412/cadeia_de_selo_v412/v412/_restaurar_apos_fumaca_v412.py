# -*- coding: utf-8 -*-
"""_restaurar_apos_fumaca_v412.py -- (claude-construtor-v412, 17/11/2026) o teste de fumaca de `reconstruir_kernel_v412.py --so-preparar` (06:09) regravou, sem mudanca no sandbox,
BUNDLE_v412.json, kernel_modulos_novos_v412.json e kernel\\ULTIMA_INSTALACAO_v412.json com o carimbo novo e SEM o registro da instalacao real (o TGLExt.lean retirado para a quarentena e a lista
do que o lake recompilou). Este script devolve os tres ao estado da instalacao que o build usou (os backups de bytes .bak_20261117_060901), guardando antes o estado da fumaca em .bak_<agora>_fumaca.
Depois disso, o preparo foi corrigido para nao regravar nada quando nada muda. uso: C:\\Python314\\python.exe -B -X utf8 _restaurar_apos_fumaca_v412.py"""
import datetime, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for rel in ("BUNDLE_v412.json", "kernel_modulos_novos_v412.json", os.path.join("kernel", "ULTIMA_INSTALACAO_v412.json")):
    p = os.path.join(HERE, rel); bak = p + ".bak_20261117_060901"
    assert os.path.exists(bak), bak
    atual = open(p, "rb").read(); orig = open(bak, "rb").read()
    if atual == orig:
        print("igual:", rel); continue
    f = p + ".bak_" + TS + "_fumaca"; open(f, "wb").write(atual); assert open(f, "rb").read() == atual
    open(p + ".tmp", "wb").write(orig); assert os.path.getsize(p + ".tmp") == len(orig); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == orig
    print("restaurado:", rel, len(orig), "B; o estado da fumaca em", os.path.basename(f))

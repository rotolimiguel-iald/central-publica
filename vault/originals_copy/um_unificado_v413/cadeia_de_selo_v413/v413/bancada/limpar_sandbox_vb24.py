# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bateria_pre_selo/limpar_sandbox_vb23.py; o sandbox curto vem do delta_bn_v413 (SANDBOX_CURTO = C:\t\vb24; N8/1.4: nunca literal noutro script).
"""limpar_sandbox_vb24.py -- apaga o sandbox curto do B(n) da v413 (DBN.SANDBOX_CURTO: so' o que o pre-selo criou: fotografias, copias adulteradas do conferidor), DEPOIS de provar que nao ha juncao nem link
dentro dele (um rmtree seguiria uma juncao para fora). Confere que a pasta-mae C:\\t nao perde nenhum outro filho. Grava LIMPEZA_SANDBOX_<nome>.json em v413\\bateria_pre_selo.
Recusa (SystemExit) se o sandbox nao for C:\\t\\vb<digitos>, se achar qualquer juncao/link, ou se a pasta-mae mudar. uso: python -I -B -X utf8 limpar_sandbox_vb24.py"""
import json
import os
import re
import shutil
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import delta_bn_v413 as DBN  # noqa: E402

OUTB = DBN.OUTB_PRE_SELO
os.makedirs(OUTB, exist_ok=True)
ALVO = DBN.SANDBOX_CURTO
PAI = os.path.dirname(ALVO)
NOME = os.path.basename(ALVO)
assert os.path.normcase(PAI) == os.path.normcase(os.path.join("C:" + os.sep, "t")) and re.fullmatch(r"vb\d+", NOME), ALVO
dest = os.path.join(OUTB, "LIMPEZA_SANDBOX_%s.json" % NOME)
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
if not os.path.isdir(ALVO):
    raise SystemExit("o sandbox nao existe: " + ALVO)
vb_irmaos = lambda: sorted(x for x in os.listdir(PAI) if x != NOME and x.lower().startswith("vb") and os.path.isdir(os.path.join(PAI, x)))   # (revisao B13) so' as pastas vb*: outros agentes gravam logs direto em C:\t
irmaos_antes = vb_irmaos()
n_arq = n_dir = n_bytes = 0
reparse = []
pilha = [ALVO]
while pilha:
    p = pilha.pop()
    with os.scandir(p) as it:
        for e in it:
            if e.is_junction() or e.is_symlink():
                reparse.append(e.path)
                continue
            if e.is_dir(follow_symlinks=False):
                n_dir += 1
                pilha.append(e.path)
            else:
                n_arq += 1
                n_bytes += e.stat(follow_symlinks=False).st_size
if reparse:
    raise SystemExit("juncao ou link dentro do sandbox, nao apago: %r" % reparse)
shutil.rmtree(ALVO)
irmaos_depois = vb_irmaos()
rec = {"contrato": "LIMPEZA_SANDBOX_%s" % NOME, "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "alvo": ALVO, "arquivos": n_arq, "pastas": n_dir, "bytes": n_bytes, "juncoes_ou_links_antes_de_apagar": len(reparse),
       "existe_depois": os.path.exists(ALVO), "irmaos_vb_de_C_t_antes": len(irmaos_antes), "irmaos_vb_de_C_t_depois": len(irmaos_depois), "irmaos_iguais": irmaos_antes == irmaos_depois,
       "nota": "as fotografias e as listas que valem como prova estao copiadas em %s (gerar_pino_recibo_pre_selo_v413.py); o resto do sandbox era descartavel" % os.path.join(OUTB, "prova_producao")}
assert rec["existe_depois"] is False and rec["irmaos_iguais"] is True
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print(json.dumps(rec, ensure_ascii=False))

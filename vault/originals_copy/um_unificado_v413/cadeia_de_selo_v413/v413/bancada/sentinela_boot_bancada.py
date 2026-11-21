# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] a medida permanente B do DIAGNOSTICO_E_PLANO_BN_v413.md (5.3), SO PREPARADA: o script que uma tarefa no logon rodaria.
# A tarefa agendada NAO e' criada aqui (e' ordem do operador; cuidado com aspas e espacos no /TR: memoria schtasks-caminhos-com-espaco-24out.md).
"""sentinela_boot_bancada.py -- roda SO a conferencia A (saude_bancada.py, no mesmo interpretador isolado) e, se a Bancada estiver FORA DO AR DEPOIS DE UM REINICIO da maquina, deixa um aviso em arquivo.
NAO liga nada, NAO para nada, NAO escreve no quadro nem na Bancada. A Bancada nao tem inicio automatico (DIAGNOSTICO 1.2): religar e' ato do operador, ou da gerencia sob ordem dele, com recibo de religamento.
Grava: <saida>\\conferencias\\SAUDE_BANCADA_<carimbo>.json (a conferencia A) e, so' no FORA_DO_AR_APOS_REINICIO, <saida>\\avisos\\AVISO_BANCADA_FORA_APOS_REINICIO_<carimbo>.json e .txt (um aviso por boot: se ja ha'
aviso deste boot, nao repete). rc 0 = a conferencia rodou (qualquer veredito conhecido); 1 = a conferencia falhou ou deu INDETERMINADO.
uso: python -I -B -X utf8 sentinela_boot_bancada.py [--saida <pasta>]   (padrao: C:\\IALD\\Central de Patentes\\work\\bancada_saude)"""
import argparse
import datetime
import glob
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import util_bn_v413 as U  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--saida", default=os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "bancada_saude"))
a = ap.parse_args()
conf_dir = os.path.join(a.saida, "conferencias")
avisos_dir = os.path.join(a.saida, "avisos")
os.makedirs(conf_dir, exist_ok=True)
r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "saude_bancada.py"), "--saida", conf_dir], capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, timeout=600)
linhas = [l_ for l_ in (r.stdout or "").splitlines() if l_.strip().startswith("{")]
if r.returncode not in (0, 3) or not linhas:
    print("SENTINELA: a conferencia A falhou ou deu INDETERMINADO (rc %s): %s %s" % (r.returncode, (r.stdout or "")[-600:], (r.stderr or "")[-600:]))
    sys.exit(1)
out = json.loads(linhas[-1])
sa = U.ler_json(out["recibo"])
print("SENTINELA: conferencia A =", out["veredito"], "|", out["recibo"])
if out["veredito"] == "FORA_DO_AR_APOS_REINICIO":
    boot = sa.get("ultimo_boot")
    os.makedirs(avisos_dir, exist_ok=True)
    ja = [p_ for p_ in glob.glob(os.path.join(avisos_dir, "AVISO_BANCADA_FORA_APOS_REINICIO_*.json")) if U.ler_json(p_).get("ultimo_boot") == boot]
    if ja:
        print("SENTINELA: ja ha' aviso deste boot (%s): %s" % (boot, ja[-1]))
        sys.exit(0)
    carimbo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    aviso = {"contrato": "AVISO_BANCADA_FORA_APOS_REINICIO", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "ultimo_boot": boot,
             "ultimo_recibo_de_religamento": sa.get("ultimo_recibo_de_religamento"), "conferencia_A": {"path": out["recibo"], "sha256": out["sha256"]},
             "contrato_em_disco": (sa.get("contrato_em_disco") or {}).get("estado"), "nos": (sa.get("nos_lido") or {}).get("um_version"),
             "o_que_fazer": ("a Bancada Um esta' fora do ar desde o reinicio da maquina e nao religa sozinha; religar e' ato do operador, ou da gerencia sob ordem dele, com recibo de religamento "
                             "(lancamento com logs em estado\\; o modo da placa escolhido por ele). Se o contrato em disco nao e' OK, ligar so' traz o modo degradado ate' o B(n) da versao."),
             "escopo": "so' leitura; nada foi ligado, parado ou gravado na Bancada; nenhum evento no quadro"}
    pj = os.path.join(avisos_dir, "AVISO_BANCADA_FORA_APOS_REINICIO_%s.json" % carimbo)
    U.gravar_json_novo(pj, aviso)
    pt = pj[:-5] + ".txt"
    with open(pt + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("AVISO (%s): a Bancada Um esta' FORA DO AR depois do reinicio de %s.\n%s\nConferencia A: %s\n" % (aviso["quando"], boot, aviso["o_que_fazer"], out["recibo"]))
    os.replace(pt + ".tmp", pt)
    print("SENTINELA: AVISO gravado:", pj)
sys.exit(0)

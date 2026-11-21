# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] a medida permanente A do DIAGNOSTICO_E_PLANO_BN_v413.md (5.3): a conferencia de saude da Bancada Um, SO LEITURA.
"""saude_bancada.py -- a conferencia A: SO LEITURA, nunca liga, para ou mexe no servico; nenhum POST; nunca /api/estado nem `um_bancada.py --check` (os dois criam contexto CUDA no processo do servico).
Le: (1) a porta (TCP); (2) os processos um_bancada.py (PID, criacao, linha de comando) e o PID que escuta na porta; (3) GET /api/contratos (so' com a porta aberta; nao toca a placa: so' le o contrato);
(4) o estado do contrato EM DISCO: o canonical_contracts.json e o canonical.py INSTALADO da Bancada (importado sem gravar bytecode), que confere os pinos contra os arquivos (ok ou o codigo da recusa, ex. PIN_CHANGED);
(5) o selo e o um.py do Nos; (6) o ultimo boot da maquina contra a hora do ultimo recibo de religamento da cadeia.
Vereditos: NO_AR_EM_DIA (no ar; o contrato servido e o em disco conferem; o um.py e o selo servidos sao os do Nos); NO_AR_CONTRATO_VELHO (no ar, mas o contrato recusa ou nao e' o do Nos: esperado entre a
instalacao de uma versao e o B(n) dela, e dito como tal); FORA_DO_AR (porta fechada, nenhum processo, sem reinicio depois do ultimo religamento); FORA_DO_AR_APOS_REINICIO (idem, e a maquina reiniciou depois do
ultimo religamento); INDETERMINADO (o que nao se encaixa: porta aberta por outro programa, /api/contratos ilegivel, processo vivo com a porta fechada) -- fail-closed.
Grava um recibo NOVO SAUDE_BANCADA_<AAAAMMDD_HHMMSS>.json na pasta --saida. rc 0 = NO_AR_EM_DIA; 3 = outro veredito conhecido (a informacao e' o veredito, nao um erro); 1 = INDETERMINADO ou falha da leitura.
uso: python -I -B -X utf8 saude_bancada.py --saida <pasta> [--bancada C:\\IALD\\Bancada_Um] [--nos <Nos>] [--porta 18777] [--recibos-religamento <glob>]"""
import argparse
import datetime
import glob
import importlib.util
import json
import os
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import util_bn_v413 as U  # noqa: E402   (o util nao le nem grava nada ao ser importado; o delta_bn NAO e' importado: a conferencia A vale em qualquer estado da Bancada)

C = "C:" + os.sep
ap = argparse.ArgumentParser()
ap.add_argument("--saida", required=True, help="a pasta onde o recibo da conferencia e' gravado (o portao C do bn_v413.sh le a de hoje)")
ap.add_argument("--bancada", default=os.path.join(C, "IALD", "Bancada_Um"))
ap.add_argument("--nos", default=os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s"))
ap.add_argument("--porta", type=int, default=18777)
ap.add_argument("--recibos-religamento", default=os.path.join(C, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "v*", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v*.json"))
a = ap.parse_args()
quando = datetime.datetime.now().astimezone()
rec = {"contrato": "SAUDE_BANCADA", "quando": quando.isoformat(timespec="seconds"), "script": U.pinar(os.path.abspath(__file__)), "bancada": a.bancada, "nos": a.nos, "porta": a.porta,
       "nunca": "nenhum POST; nunca /api/estado nem --check (criam contexto CUDA); nada e' ligado, parado ou gravado na Bancada"}
anomalias = []
# (1) e (2): a porta e os processos
rec["porta_aberta"] = U.porta_aberta(a.porta)
alvo_cmd = U.texto_normalizado(os.path.join(a.bancada, "um_bancada.py"))
try:
    procs = U.processos_um_bancada()
    rec["processos_um_bancada"] = [p_ for p_ in procs if alvo_cmd in U.texto_normalizado(p_["linha_de_comando"])]
    rec["outros_processos_que_citam_um_bancada"] = [p_ for p_ in procs if p_ not in rec["processos_um_bancada"]]
except Exception as e_:   # noqa: BLE001
    rec["processos_um_bancada"] = None
    anomalias.append("a leitura dos processos falhou: %r" % (e_,))
rec["pid_da_porta"] = None
rec["processo_da_porta"] = None
if rec["porta_aberta"]:
    rec["pid_da_porta"] = U.pid_da_porta(a.porta)
    rec["processo_da_porta"] = U.processo(rec["pid_da_porta"]) if rec["pid_da_porta"] else None
    if not (rec["processo_da_porta"] and alvo_cmd in U.texto_normalizado(rec["processo_da_porta"]["linha_de_comando"])):
        anomalias.append("a porta %d esta' aberta, mas quem escuta nao e' o um_bancada.py desta Bancada (%r)" % (a.porta, rec["processo_da_porta"]))
elif rec["processos_um_bancada"]:
    anomalias.append("ha' processo um_bancada.py vivo com a porta fechada (subindo, travado ou em outra porta): %r" % ([p_["pid"] for p_ in rec["processos_um_bancada"]],))
# (3) GET /api/contratos (so' com a porta aberta)
rec["contratos_servidos"] = None
if rec["porta_aberta"]:
    try:
        rec["contratos_servidos"] = U.get_json("http://127.0.0.1:%d/api/contratos" % a.porta, timeout=10)
    except Exception as e_:   # noqa: BLE001
        anomalias.append("GET /api/contratos falhou: %r" % (e_,))
# (4) o contrato em disco, pelo canonical.py INSTALADO (stdlib; sem bytecode)
man_p = os.path.join(a.bancada, "canonical_contracts.json")
disco = {"manifesto": man_p}
try:
    man_raw = open(man_p, "rb").read()
    man = json.loads(man_raw)
    disco.update(manifesto_sha256=U.sha256_bytes(man_raw), deployment_id=man.get("deployment_id"), version=(man.get("canonical") or {}).get("version"),
                 um_py_pinado=((man.get("canonical") or {}).get("script") or {}).get("sha256"), seal_sha_pinado=((man.get("canonical") or {}).get("seal") or {}).get("sha256"))
    cp = os.path.join(a.bancada, "bancada", "canonical.py")
    sp = importlib.util.spec_from_file_location("canonical_instalado_saude_%s" % U.sha256_arquivo(cp)[:12], cp)
    cm = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(cm)
    try:
        r_ = cm.CanonicalRegistry(a.bancada).check("saude_bancada")
        disco.update(estado="OK", ok=True, canonical_version=r_.get("canonical_version"))
    except cm.CanonicalError as exc:
        disco.update(estado=str(exc).split(":")[0], ok=False, erro=str(exc)[:300])
    disco["canonical_py"] = U.pinar(cp)
except Exception as e_:   # noqa: BLE001
    disco.update(estado="ILEGIVEL", ok=False, erro=repr(e_)[:300])
    anomalias.append("o contrato em disco nao foi lido: %r" % (e_,))
rec["contrato_em_disco"] = disco
# (5) o Nos
try:
    selo = U.ler_json(os.path.join(a.nos, "um_absoluto_selo.json"))
    um_n = U.sha256_arquivo(os.path.join(a.nos, "um.py"))
    rec["nos_lido"] = {"um_version": selo.get("um_version"), "um_py_sha256": um_n, "selo_sha256": U.sha256_arquivo(os.path.join(a.nos, "um_absoluto_selo.json")),
                       "selo_pina_o_um_py": (selo.get("sha256") or {}).get("um.py") == um_n}
except Exception as e_:   # noqa: BLE001
    rec["nos_lido"] = None
    anomalias.append("o Nos nao foi lido: %r" % (e_,))
# (6) o ultimo boot contra o ultimo recibo de religamento
ult = None
for p_ in glob.glob(a.recibos_religamento):
    try:
        h_ = U.instante(U.ler_json(p_)["hora_recibo"])
        if ult is None or h_ > ult[0]:
            ult = (h_, p_)
    except Exception:   # noqa: BLE001
        continue
try:
    boot = U.instante(U.ultimo_boot())
except Exception as e_:   # noqa: BLE001
    boot = None
    anomalias.append("o ultimo boot nao foi lido: %r" % (e_,))
rec["ultimo_boot"] = boot.isoformat() if boot else None
rec["ultimo_recibo_de_religamento"] = {"path": ult[1], "hora_recibo": ult[0].isoformat()} if ult else None
rec["reiniciou_depois_do_ultimo_religamento"] = bool(boot and ult and boot > ult[0])
# o veredito
cs = rec["contratos_servidos"] or {}
nl = rec["nos_lido"] or {}
if anomalias:
    v = "INDETERMINADO"
elif rec["porta_aberta"]:
    em_dia = (cs.get("ok") is True and disco.get("ok") is True and cs.get("deployment_id") == disco.get("deployment_id") and cs.get("canonical_manifest_sha256") == disco.get("manifesto_sha256")
              and cs.get("um_py_sha256") == nl.get("um_py_sha256") and cs.get("seal_sha256") == nl.get("selo_sha256") and cs.get("canonical_version") == nl.get("um_version"))
    v = "NO_AR_EM_DIA" if em_dia else "NO_AR_CONTRATO_VELHO"
else:
    v = "FORA_DO_AR_APOS_REINICIO" if rec["reiniciou_depois_do_ultimo_religamento"] else "FORA_DO_AR"
rec["veredito"] = v
rec["anomalias"] = anomalias
rec["leitura"] = {"NO_AR_EM_DIA": "a Bancada serve o contrato do Nos", "NO_AR_CONTRATO_VELHO": "no ar, mas o contrato recusa ou nao e' o do Nos: esperado entre a instalacao de uma versao e o B(n) dela (ela recusa toda conta cientifica com 409)",
                  "FORA_DO_AR": "fora do ar, sem reinicio da maquina depois do ultimo religamento", "FORA_DO_AR_APOS_REINICIO": "fora do ar, e a maquina reiniciou depois do ultimo religamento (a Bancada nao tem inicio automatico)",
                  "INDETERMINADO": "a leitura nao se encaixa: ver anomalias"}[v]
os.makedirs(a.saida, exist_ok=True)
dest = os.path.join(a.saida, "SAUDE_BANCADA_%s.json" % quando.strftime("%Y%m%d_%H%M%S"))
while os.path.exists(dest):
    time.sleep(1)
    dest = os.path.join(a.saida, "SAUDE_BANCADA_%s.json" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
U.gravar_json_novo(dest, rec)
print(json.dumps({"veredito": v, "recibo": dest, "sha256": U.sha256_arquivo(dest), "porta_aberta": rec["porta_aberta"], "contrato_em_disco": disco.get("estado"), "anomalias": anomalias}, ensure_ascii=False))
sys.exit(0 if v == "NO_AR_EM_DIA" else (1 if v == "INDETERMINADO" else 3))

# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] DIAGNOSTICO_E_PLANO_BN_v413.md, 2.3.a: a cadeia de selos v411 -> v412 pelo gerador da R3.4 (R3_5\gerar_cadeia_de_selos.py), gravada numa pasta da v413 e pinada por sha256.
"""gerar_e_pinar_cadeia_v413.py -- PRAZO (N1): so' com o Nos AINDA na v412 (antes da instalacao da v413). Faz, nesta ordem, e para na primeira recusa:
  (1) confere que o Nos esta' na v412 (o selo diz v412 e pina o um.py do disco) e que a Bancada de producao pina o B20 da v411 (o delta_bn: BANCADA_PINA_HOJE == o fixado);
  (2) roda o gerador `python -I -B -X utf8 gerar_cadeia_de_selos.py --cadeia <cadeia_de_selo> --de v411 --ate v412 --saida <CADEIA_ARQ>` (ele so' le e grava UM arquivo novo; recusa se existir);
  (3) confere a cadeia PELO ESBOCO R3.6 PINADO (o mesmo que o pre-selo usa: path e sha256 de v411\\PINOS_BN_v411.json[esboco_R3_6], conferidos contra o disco): carregar_cadeia_de_selos (elos, copias de bytes,
      registro do instalador, backups do Nos), conferir_cadeia_com_a_bancada (o inicio e' o que a Bancada pina; o manifesto lido como JSON, so' leitura) e conferir_cadeia_com_o_fim (o fim e' o Nos lido agora);
  (4) grava, ao lado, PINO_CADEIA_DE_SELOS_v411_v412.json (path, sha256 e bytes da cadeia; o gerador e o esboco pinados; o resumo conferido).
Nao grava no Nos nem na Bancada; nao roda o B(n). uso: python -I -B -X utf8 gerar_e_pinar_cadeia_v413.py"""
import sys

sys.dont_write_bytecode = True
import datetime
import importlib.util
import json
import os
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

assert DBN.BANCADA_PINA_HOJE == DBN.BANCADA_PINA_HOJE_FIXADA_V411, ("a Bancada de producao ja nao pina o B20 da v411: o pre-selo do salto nao se aplica", DBN.BANCADA_PINA_HOJE)
# (1) o prazo: o Nos ainda na v412
selo = U.ler_json(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
um_nos = U.sha256_arquivo(os.path.join(DBN.NOS, "um.py"))
if selo.get("um_version") != DBN.VERSAO_DO_PRE_SELO or (selo.get("sha256") or {}).get("um.py") != um_nos:
    raise SystemExit("PRAZO_DO_PRE_SELO_PERDIDO (N1): o Nos nao esta' na %s com o selo pinando o um.py do disco (selo diz %r); a cadeia v411 -> v412 deste pre-selo nao se gera mais"
                     % (DBN.VERSAO_DO_PRE_SELO, selo.get("um_version")))
# o esboco R3.6 pinado (o mesmo do pre-selo)
P11 = U.ler_json(DBN.PINOS_BN_V411_ARQ)
ESB, ESB_SHA = P11["esboco_R3_6"]["path"], P11["esboco_R3_6"]["sha256"]
assert U.sha256_arquivo(ESB) == ESB_SHA, "o esboco R3.6 em disco nao e' o pinado em PINOS_BN_v411.json"
_spec = importlib.util.spec_from_file_location("sincronizar_bancada_r36_cadeia_v413", ESB)
MOD = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = MOD
_spec.loader.exec_module(MOD)
# (2) o gerador
if os.path.exists(DBN.CADEIA_ARQ) or os.path.exists(DBN.PINO_CADEIA_ARQ):
    raise SystemExit("a cadeia ou o pino dela ja existem (%s): nao regero; quem quiser refazer guarda e tira os dois antes" % DBN.CADEIA_DIR)
os.makedirs(DBN.CADEIA_DIR, exist_ok=True)
r = subprocess.run([DBN.PYTHON, "-I", "-B", "-X", "utf8", DBN.GERADOR_CADEIA, "--cadeia", DBN.CADEIA, "--de", DBN.BANCADA_ANTERIOR, "--ate", DBN.VERSAO_DO_PRE_SELO, "--saida", DBN.CADEIA_ARQ],
                   capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, cwd=DBN.CADEIA_DIR)
print("gerador rc", r.returncode, "|", (r.stdout or "").strip()[-600:], (r.stderr or "").strip()[-600:])
if r.returncode != 0 or not os.path.isfile(DBN.CADEIA_ARQ):
    raise SystemExit("o gerador da cadeia recusou (rc %s): nada foi pinado" % r.returncode)
CAD_SHA = U.sha256_arquivo(DBN.CADEIA_ARQ)
# (3) conferida pelo esboco
cad = MOD.carregar_cadeia_de_selos(Path(DBN.CADEIA_ARQ), CAD_SHA)
man_raw = open(DBN._BANCADA_CONTRATOS, "rb").read()
man = json.loads(man_raw)
anterior = {"version": (man.get("canonical") or {}).get("version"), "um_py_pinado": ((man.get("canonical") or {}).get("script") or {}).get("sha256"),
            "seal_sha_pinado": ((man.get("canonical") or {}).get("seal") or {}).get("sha256"), "_man": man, "sha256": U.sha256_bytes(man_raw), "deployment_id": man.get("deployment_id")}
MOD.conferir_cadeia_com_a_bancada(cad, anterior)
km_nos = U.sha256_arquivo(os.path.join(DBN.NOS, "tgl_kernel_proof_manifest.json"))
selo_nos = U.sha256_arquivo(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
MOD.conferir_cadeia_com_o_fim(cad, DBN.VERSAO_DO_PRE_SELO, um_nos, selo_nos, km_nos, "o Nos lido agora")
assert cad["versoes"] == [DBN.BANCADA_ANTERIOR, DBN.VERSAO_DO_PRE_SELO] and cad["n_elos"] == 2, cad["versoes"]
salto_previsto = MOD.montar_salto(cad, anterior)
pino = {
    "contrato": "PINO_CADEIA_DE_SELOS_v411_v412",
    "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "cadeia": U.pinar(DBN.CADEIA_ARQ, contrato=cad["contrato"], n_elos=cad["n_elos"], versoes=cad["versoes"]),
    "gerador": U.pinar(DBN.GERADOR_CADEIA, rc=r.returncode, stdout=(r.stdout or "").strip()[-2000:]),
    "esboco": {"path": ESB, "sha256": ESB_SHA, "revisao": getattr(MOD, "REVISAO", None), "origem": "PINOS_BN_v411.json[esboco_R3_6]"},
    "conferida_pelo_esboco": {"carregar_cadeia_de_selos": True, "conferir_cadeia_com_a_bancada": True, "conferir_cadeia_com_o_fim": True,
                              "ligacoes": cad["ligacoes"], "elos": [{"versao": e["versao"], "um_py": e["um_py"], "selo": e["selo"], "kernel_manifesto": e["kernel_manifesto"]} for e in cad["elos"]]},
    "inicio_e_a_bancada": {"deployment_id": anterior["deployment_id"], "manifesto_sha256": anterior["sha256"], "version": anterior["version"], "um_py_pinado": anterior["um_py_pinado"],
                           "seal_sha_pinado": anterior["seal_sha_pinado"], "kernel_manifesto_registrado": (man.get("sincronizacao") or {}).get("kernel_manifesto_sha256")},
    "fim_e_o_nos_lido_agora": {"um_version": selo.get("um_version"), "um_py_sha256": um_nos, "selo_sha256": selo_nos, "kernel_manifesto_sha256": km_nos},
    "salto_previsto_pelo_esboco": salto_previsto,
    "nota": ("a cadeia v411 -> v412 do pre-selo do salto da v413 (DIAGNOSTICO 2.3.a): consistencia por hash, nao autenticidade; depende dos backups de 18/11 no Nos (N3: so' leitura, nunca mover) e do registro "
             "v412\\APLICADO_AO_CANONICO_20261118_235146.json; o manifesto da Bancada nao pode mudar entre o pre-selo e o APLICAR (o salto embute o sha dele e o deployment_id)"),
    "escopo": "so leitura do Nos e da Bancada; nada gravado em nenhum dos dois; NOT_FALSIFIED nao e' creditacao; o gate nao se move",
}
U.gravar_json_novo(DBN.PINO_CADEIA_ARQ, pino)
print(json.dumps({"cadeia": DBN.CADEIA_ARQ, "sha256": CAD_SHA, "n_elos": cad["n_elos"], "versoes": cad["versoes"], "pino": DBN.PINO_CADEIA_ARQ, "pino_sha256": U.sha256_arquivo(DBN.PINO_CADEIA_ARQ),
                  "salto_de": salto_previsto["de"]["deployment_id"], "proxima_a_selar": salto_previsto["proxima_a_selar"]}, ensure_ascii=False))

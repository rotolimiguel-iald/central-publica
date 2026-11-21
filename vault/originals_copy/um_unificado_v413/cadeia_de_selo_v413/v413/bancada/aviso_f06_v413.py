# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] revisao B4: o aviso F0.6 que aponta os tres recibos do B(n) (plano, secao 4, item 4), para o Codex encerrar a unidade dele. Ato da gerencia.
"""aviso_f06_v413.py -- DEPOIS do passo 11 (fechar_bn_v413.py): anota no quadro, pelo iald.py anotar (--quem claude-c1 --unidade F0.6), o aviso de que o B21 da v413 foi aplicado e os tres recibos foram entregues:
o pino conjunto (caminho e sha256), as copias dos tres recibos na pasta que o evento 1687 nomeia (conferidas por sha256 contra o pino), o evento da sincronizacao (seq e hash) e o deployment servido.
Nunca anota duas vezes: se o livro conferido ja traz o aviso da claude-c1 com este mesmo pino conjunto, devolve o elo e sai. Exige o rc 0 do iald.py e confere o elo novo no livro inteiro.
uso: python -I -B -X utf8 aviso_f06_v413.py   (imprime AVISO=<seq> AVISO_HASH=<hash16>)"""
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

TIPO = "AVISO_RECIBOS_B%d_ENTREGUES" % DBN.N_DO_SALTO
PINO_P = os.path.join(DBN.SAIDAS_BN_DIR, "PINO_RECIBOS_B%d_v413.json" % DBN.N_DO_SALTO)
assert os.path.isfile(PINO_P), "sem o pino conjunto dos tres recibos (%s): o aviso so' vem depois do passo 11 (fechar_bn_v413.py)" % PINO_P
PINO = U.ler_json(PINO_P)
entregues = {}
for k_, v_ in PINO["recibos"].items():
    assert U.sha256_arquivo(v_["path"]) == v_["sha256"], "o recibo %s mudou depois do pino conjunto" % k_
    copia = os.path.join(DBN.BENCH_DIR, os.path.basename(v_["path"]))
    assert os.path.isfile(copia) and U.sha256_arquivo(copia) == v_["sha256"], "a copia do recibo %s na pasta do evento %d falta ou diverge" % (k_, DBN.SEQ_AUTORIZACAO)
    entregues[k_] = {"path": copia, "sha256": v_["sha256"]}
copia_pino = os.path.join(DBN.BENCH_DIR, os.path.basename(PINO_P))
assert os.path.isfile(copia_pino) and U.sha256_arquivo(copia_pino) == U.sha256_arquivo(PINO_P), "a copia do pino conjunto na pasta do evento %d falta ou diverge" % DBN.SEQ_AUTORIZACAO
PINO_SHA = U.sha256_arquivo(PINO_P)
dados = {"versao": DBN.UM_VERSION_BN, "aviso": "B%d da v413 aplicado; os tres recibos do B(n) entregues" % DBN.N_DO_SALTO,
         "pino_conjunto": {"path": copia_pino, "sha256": PINO_SHA}, "recibos": entregues, "evento_sincronizacao": PINO.get("evento_c1"),
         "deployment_servido": (PINO.get("salto") or {}).get("para"), "em_resposta_ao_evento": DBN.SEQ_AUTORIZACAO,
         "para": "codex do app: o retorno pedido no evento %d (F0.6) esta' na pasta indicada" % DBN.SEQ_AUTORIZACAO}
L0 = U.livro_conferido(DBN.QUADRO)
JA = sorted((e_ for e_ in L0["eventos"].values() if e_.get("quem") == "claude-c1" and e_.get("tipo") == TIPO and ((e_.get("dados") or {}).get("pino_conjunto") or {}).get("sha256") == PINO_SHA), key=lambda e_: e_["seq"])
if JA:
    print("o aviso deste pino conjunto ja esta' no livro (seq %d): nada foi anotado de novo" % JA[-1]["seq"])
    print("AVISO=%d AVISO_HASH=%s" % (JA[-1]["seq"], JA[-1]["hash"][:16]))
    sys.exit(0)
r = subprocess.run([DBN.PYTHON, "-B", "-X", "utf8", DBN.IALD_PY, "anotar", "--quem", "claude-c1", "--tipo", TIPO, "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=os.path.dirname(DBN.IALD_PY), stdin=subprocess.DEVNULL)
print((r.stdout or "").strip(), (r.stderr or "").strip()[-300:])
assert r.returncode == 0, "o iald.py anotar saiu com rc %d: nao se sabe se o aviso foi anotado; conferir o livro antes de repetir" % r.returncode
RET = json.loads([l_ for l_ in (r.stdout or "").splitlines() if l_.strip().startswith("{")][-1])
assert RET.get("ok") is True and isinstance(RET.get("evento"), int) and re.fullmatch(r"[0-9a-f]{16}", str(RET.get("hash"))), ("o retorno do iald.py anotar nao e' {ok, evento, hash}", RET)
E = U.livro_conferido(DBN.QUADRO)["eventos"].get(RET["evento"]) or {}
assert str(E.get("hash")).startswith(RET["hash"]) and E.get("quem") == "claude-c1" and E.get("tipo") == TIPO and ((E.get("dados") or {}).get("pino_conjunto") or {}).get("sha256") == PINO_SHA, "o elo anotado nao e' o aviso pedido"
print("AVISO=%d AVISO_HASH=%s" % (RET["evento"], RET["hash"]))

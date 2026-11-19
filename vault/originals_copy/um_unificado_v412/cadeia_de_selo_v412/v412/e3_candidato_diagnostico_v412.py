# -*- coding: utf-8 -*-
"""e3_candidato_diagnostico_v412.py -- cria, FORA de work\\ (C:\\t\\k412c\\diag), uma COPIA DE DIAGNOSTICO do candidato com UM literal diferente: _V411_H0DN_CONTRACT['baseline']['escada'] 12308 -> 13211, o unico pino exato da escada da v411 que o gerador nao subiu
(o registro com funcao h0dn_bg1_v411, selado, cobra no c15 `n_theorems_expected == baseline.escada` e `n_theorems_clean == baseline.escada`; com a escada desta versao em 13211 o registro RECUSA e arrasta cunhagens_v411 e os quatro registros da v412).
A copia serve SO' para separar, no ensaio, o que e' defeito do candidato (esse literal) do que e' do ensaio; o candidato real NAO e' tocado e nenhuma decisao e' tomada aqui: a decisao do literal e' da gerencia. Grava tambem o manifesto de diagnostico (copia do CANDIDATO_v412.json com sha/bytes da copia e a marca `diagnostico`).
Script da cadeia; nada daqui entra no programa."""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "um_v412_candidato.py")
DIAG_DIR = r"C:\t\k412c\diag"
os.makedirs(DIAG_DIR, exist_ok=True)
raw = open(SRC, "rb").read()
sha_cand = hashlib.sha256(raw).hexdigest()
assert sha_cand[:16] == "d594623f2be2d39d", "o candidato nao e' o gerado"
s = raw.decode("utf-8")
old = "\r\n              'escada': 12308,\r\n              'um_py_sha256': '5d9497a721c3589e"   # (o candidato e' CRLF, como o um.py da base)
assert s.count(old) == 1, ("o pino exato da escada nao esta' uma vez so'", s.count(old))
nova = s.replace(old, old.replace("'escada': 12308,", "'escada': 13211,"))
assert len(nova) == len(s)
out = os.path.join(DIAG_DIR, "um_v412_diag.py")
open(out + ".tmp", "wb").write(nova.encode("utf-8"))
assert os.path.getsize(out + ".tmp") == len(raw)
os.replace(out + ".tmp", out)
b = open(out, "rb").read()
m = json.load(open(os.path.join(HERE, "CANDIDATO_v412.json"), encoding="utf-8"))
m["diagnostico"] = {"o_que_e": "copia do candidato com UM literal diferente (_V411_H0DN_CONTRACT.baseline.escada 12308 -> 13211); so' para o ensaio de diagnostico; nao e' candidato", "candidato_real_sha16": sha_cand[:16]}
m["candidato"] = out; m["sha16"] = hashlib.sha256(b).hexdigest()[:16]; m["sha256"] = hashlib.sha256(b).hexdigest(); m["bytes"] = len(b)
mp = os.path.join(DIAG_DIR, "CANDIDATO_v412_diag.json")
open(mp + ".tmp", "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1)); os.replace(mp + ".tmp", mp)
print("copia de diagnostico:", out, len(b), "bytes, sha16", m["sha16"], "| manifesto:", mp)

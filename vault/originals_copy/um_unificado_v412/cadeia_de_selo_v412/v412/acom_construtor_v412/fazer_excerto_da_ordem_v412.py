# -*- coding: utf-8 -*-
"""fazer_excerto_da_ordem_v412.py -- (claude-construtor-v412, 17/11/2026) o init ACOM da ordem original foi RECUSADO com erro visivel
(ConfidentialContent, regras dotenv_name e escritorio_path: a linha da regra dos confidenciais da ordem nomeia o arquivo de ambiente e o caminho da outra casa).
Este script compoe, dos BYTES da ordem, um EXCERTO DECLARADO: a ordem inteira menos as linhas que contem esses dois tokens; o cabecalho do excerto diz o caminho e o
sha256 da ordem original, quais linhas sairam (numero e sha256 de cada uma) e por que. Nada e' redigido em silencio; a ordem original nao e' tocada.
Uso: C:\\Python314\\python.exe -X utf8 fazer_excerto_da_ordem_v412.py"""
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(os.path.dirname(H), "ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md")
OUT = os.path.join(H, "ORDEM_v412_ETAPA_1_EXCERTO_PARA_ACOM.md")
b = open(ORIG, "rb").read()
t = b.decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
linhas = t.split(nl)
TOK = (".env", "C:\\Escritorio")
fora = [(i + 1, l) for i, l in enumerate(linhas) if any(k in l for k in TOK)]
assert fora, "nenhuma linha com os tokens recusados: o excerto nao e' necessario"
cab = [
    "# EXCERTO DECLARADO da ordem da Etapa 1 da v412 (para a inscricao ACOM do claude-construtor-v412)",
    "",
    "> Ordem original: `%s`, sha256 `%s`, %d bytes (nao tocada)." % (ORIG, hashlib.sha256(b).hexdigest(), len(b)),
    "> O init ACOM da ordem original foi recusado com erro visivel (ConfidentialContent; regras dotenv_name e escritorio_path).",
    "> Sairam deste excerto %d linha(s), por inteiro, porque contem os tokens recusados: %s." % (
        len(fora), "; ".join("linha %d (sha256 %s)" % (n, hashlib.sha256(l.encode("utf-8")).hexdigest()) for n, l in fora)),
    "> O resto e' a ordem byte a byte. A regra que saiu continua valendo para o construtor: ela esta na ordem original.",
    "",
]
corpo = [l for i, l in enumerate(linhas) if (i + 1) not in {n for n, _ in fora}]
novo = nl.join(cab + corpo).encode("utf-8")
assert not any(k.encode("utf-8") in novo for k in TOK)
tmp = OUT + ".tmp"
open(tmp, "wb").write(novo)
assert os.path.getsize(tmp) == len(novo)
os.replace(tmp, OUT)
print("excerto:", OUT, len(novo), "B | sha16", hashlib.sha256(novo).hexdigest()[:16], "| linhas fora:", [n for n, _ in fora])

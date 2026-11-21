# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] molde v412/bancada_B3_servico/evento_c1_b3_v412.py (o conjunto fechado de chaves do esboco; o candidato_sha16 conferido contra o um.py do
# Nos antes de anotar), com a pendencia 2.6: (a) antes de anotar, exige o stdout do ENSAIO pos-selo (passo 10) e o b3_recibo_v413.py dele com rc 0 (a ordem ENSAIO -> evento -> APLICAR imposta); (b) depois de
# anotar, exige o rc 0 do iald.py, le o JSON {"ok": true, "evento": N, "hash": H} do stdout, confere o elo no livro conferido INTEIRO e imprime EVENTO=N EVENTO_HASH=H; (c) o evento tem de ser POSTERIOR ao fim do
# recibo do ensaio (o bn_v413.sh confere de novo antes do 10b).
"""Evento c1 SINCRONIZACAO_BANCADA do B(n) da v413 (o salto v411 -> v413: B21 sobre a producao que pina o B20 da v411), no conjunto fechado de chaves do esboco R3.6 (versao, acao, bancada, um_py, selo, unidade).
O candidato_sha16 e' LIDO do ESPERADOS da v413 pinado em PINOS_BN_v413.json (nunca digitado) e conferido contra o um.py do Nos antes de anotar. Grava no quadro SO' o evento (pelo iald.py anotar); nada mais."""
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

ENSAIO_OUT = os.path.join(DBN.SAIDAS_BN_DIR, "b3_ensaio_out.txt")
assert os.path.isfile(ENSAIO_OUT), "sem o stdout do ENSAIO pos-selo (%s): a ordem e' ENSAIO -> evento -> APLICAR; nada foi anotado no quadro" % ENSAIO_OUT
PINOS = U.ler_json(DBN.PINOS_BN_ARQ)
CAD_SHA = PINOS["cadeia_de_selos"]["sha256"]
RR = subprocess.run([DBN.PYTHON, "-I", "-B", "-X", "utf8", os.path.join(D, "b3_recibo_v413.py"), ENSAIO_OUT, "ensaio", CAD_SHA], capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL)
assert RR.returncode == 0, ("o recibo do ENSAIO pos-selo nao confere (b3_recibo_v413.py rc %d): nada foi anotado no quadro" % RR.returncode, (RR.stdout or "")[-800:])
REC_ENSAIO = json.loads([l_ for l_ in open(ENSAIO_OUT, encoding="utf-8", errors="replace").read().splitlines() if l_.strip().startswith("{")][-1])["recibo"]
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
dados = {"versao": DBN.UM_VERSION_BN, "acao": "sincronizacao", "bancada": DBN.PRODUCAO,
         "um_py": sh(os.path.join(DBN.NOS, "um.py")), "selo": sh(os.path.join(DBN.NOS, "um_absoluto_selo.json")), "unidade": "F0.6"}
ESP = (PINOS.get("esperados") or {}).get("path") or ""
assert os.path.isfile(ESP) and sh(ESP) == (PINOS.get("esperados") or {}).get("sha256"), "o ESPERADOS da v413 pinado em PINOS_BN_v413.json nao existe ou diverge do pino: sem ele o um.py do Nos nao tem com que ser conferido; nada foi anotado"
CAND16 = json.load(open(ESP, encoding="utf-8"))["candidato_sha16"]
assert len(CAND16) >= 16, CAND16
assert dados["um_py"].startswith(CAND16), ("o um.py do Nos nao e' o candidato do ESPERADOS da v413", dados["um_py"][:16], CAND16)
# (revisao B6) nunca anotar duas vezes: se o livro conferido ja traz, DEPOIS do fim deste ensaio, o elo da claude-c1 SINCRONIZACAO_BANCADA com estes mesmos dados (o iald.py anotou e algo caiu depois), devolve esse elo e sai
LIVRO0 = U.livro_conferido(DBN.QUADRO)
FIM_ENSAIO = U.instante(U.ler_json(REC_ENSAIO)["fim_utc"])
JA = sorted((e_ for e_ in LIVRO0["eventos"].values() if e_.get("quem") == "claude-c1" and e_.get("tipo") == "SINCRONIZACAO_BANCADA" and e_.get("dados") == dados and U.instante(e_["quando"]) > FIM_ENSAIO),
            key=lambda e_: e_["seq"])
if JA:
    print("o evento deste ensaio ja esta' no livro (seq %d): nada foi anotado de novo (B6)" % JA[-1]["seq"])
    print("EVENTO=%d EVENTO_HASH=%s" % (JA[-1]["seq"], JA[-1]["hash"][:16]))
    sys.exit(0)
r = subprocess.run([DBN.PYTHON, "-B", "-X", "utf8", DBN.IALD_PY, "anotar", "--quem", "claude-c1", "--tipo", "SINCRONIZACAO_BANCADA", "--unidade", "F0.6", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", cwd=os.path.dirname(DBN.IALD_PY), stdin=subprocess.DEVNULL)
print((r.stdout or "").strip(), (r.stderr or "").strip()[-300:])
assert r.returncode == 0, "o iald.py anotar saiu com rc %d: nao se sabe se o evento foi anotado; conferir o livro antes de repetir" % r.returncode
RET = json.loads([l_ for l_ in (r.stdout or "").splitlines() if l_.strip().startswith("{")][-1])
assert RET.get("ok") is True and isinstance(RET.get("evento"), int) and re.fullmatch(r"[0-9a-f]{16}", str(RET.get("hash"))), ("o retorno do iald.py anotar nao e' {ok, evento, hash}", RET)
LIVRO = U.livro_conferido(DBN.QUADRO)
E = LIVRO["eventos"].get(RET["evento"]) or {}
assert str(E.get("hash")).startswith(RET["hash"]) and E.get("quem") == "claude-c1" and E.get("tipo") == "SINCRONIZACAO_BANCADA" and E.get("dados") == dados, "o elo anotado nao e' o evento pedido, no livro conferido inteiro"
assert U.instante(E["quando"]) > U.instante(U.ler_json(REC_ENSAIO)["fim_utc"]), "o evento nao e' posterior ao fim do recibo do ENSAIO pos-selo (2.6 c)"
print("EVENTO=%d EVENTO_HASH=%s" % (RET["evento"], RET["hash"]))

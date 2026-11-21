# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] revisao B5: o texto da autorizacao (V413_AUTORIZACAO_OPERADOR) montado POR SCRIPT dos arquivos (hash so' lido por script: a regua).
"""montar_autorizacao_v413.py -- monta, dos ARQUIVOS (nada digitado), o texto que a gerencia passa aos recibos da parada e do religamento em V413_AUTORIZACAO_OPERADOR (N4, decisao da gerencia):
  o livro do quadro conferido INTEIRO (2.2); o evento 1687 (o hash16 dele, o sha16 do recibo da resposta que ele nomeia e a resposta inteira, lida do recibo); o evento 1689 (o hash16 dele, o sha16 da fala que ele nomeia
  e a decisao); a fala do operador de 20/11 inteira e o sha16 dela; e, so' para o religamento, a fala com a escolha do modo da placa (o NOME do arquivo em cunhagens_13out) e o modo ("modo da placa: cpu|normal").
Confere que o texto passa nas mesmas exigencias dos recibos (cada parte presente) e grava, NOVO, em bancada_B3_servico: AUTORIZACAO_v413.txt (parada) ou AUTORIZACAO_v413_RELIGAMENTO_<modo>.txt (religamento), com um
recibo .json ao lado (sha256 do texto e de cada fonte). Se o arquivo ja existe com os mesmos bytes, nao regrava; se existe diferente, PARA (decisao da gerencia).
uso: python -I -B -X utf8 montar_autorizacao_v413.py [<nome da fala do modo da placa em cunhagens_13out> <cpu|normal>]
     depois: V413_AUTORIZACAO_OPERADOR="$(cat '<o .txt gravado>')" python -I -B -X utf8 recibo_parada_v413.py   (idem o religamento, com o .txt dele)"""
import datetime
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

a = sys.argv[1:]
if len(a) not in (0, 2) or (len(a) == 2 and a[1] not in DBN.MODOS_DA_PLACA):
    raise SystemExit("uso: montar_autorizacao_v413.py [<nome da fala do modo da placa em cunhagens_13out> <%s>]" % "|".join(DBN.MODOS_DA_PLACA))
sh = lambda b: hashlib.sha256(b).hexdigest()
L = U.livro_conferido(DBN.QUADRO)
E87, E89 = L["eventos"].get(DBN.SEQ_AUTORIZACAO), L["eventos"].get(DBN.SEQ_DECISAO)
assert E87 is not None and E89 is not None, "os eventos da autorizacao nao estao no livro conferido"
D87, D89 = E87.get("dados") or {}, E89.get("dados") or {}
assert E87.get("tipo") == "AVISO_AUTORIZACAO_RECEBIDA" and D87.get("versao") == "v412" and D87.get("unidade") == "F0.6" and D87.get("recibo") and D87.get("sha256"), "o evento %d nao e' o aviso da autorizacao" % DBN.SEQ_AUTORIZACAO
REC = open(D87["recibo"], "rb").read()
assert sh(REC) == D87["sha256"], "o recibo da resposta diverge do sha256 que o evento %d registra" % DBN.SEQ_AUTORIZACAO
RESPOSTA = str(json.loads(REC.decode("utf-8"))["bench"]["answer"]).strip()
assert E89.get("tipo") == "AVISO_DECISAO_DO_OPERADOR_B21" and E89.get("quem") == "claude-c1" and D89.get("em_resposta_ao_evento") == DBN.SEQ_AUTORIZACAO and D89.get("fala"), "o evento %d nao e' a decisao do operador" % DBN.SEQ_DECISAO
FALA89 = open(D89["fala"], "rb").read()
DECISAO = str(D89.get("decisao_do_operador") or "").strip()
assert sh(FALA89)[:16] == D89.get("fala_sha16") and DBN.UM_VERSION_BN in DECISAO and DECISAO in FALA89.decode("utf-8"), "a fala da decisao diverge do sha16 do evento %d ou nao diz o salto" % DBN.SEQ_DECISAO
F20B = open(DBN.FALA_AUTORIZACAO_20NOV, "rb").read()
F20 = F20B.decode("utf-8").strip()
assert len(F20) >= 20 and "bancada" in U.texto_normalizado(F20), "a fala de 20/11 nao fala da Bancada"
partes = [("evento %d" % DBN.SEQ_AUTORIZACAO), E87["hash"][:16], sh(REC)[:16], RESPOSTA, ("evento %d" % DBN.SEQ_DECISAO), E89["hash"][:16], sh(FALA89)[:16], DECISAO, F20, sh(F20B)[:16]]
texto = ("Autorizacao do operador ao ciclo da Bancada (evento %d, hash16 %s; recibo da resposta sha16 %s): «%s». Decisao do operador (evento %d, hash16 %s; fala sha16 %s): «%s». "
         "Fala do operador de 20/11 (sha16 %s): «%s»." % (DBN.SEQ_AUTORIZACAO, E87["hash"][:16], sh(REC)[:16], RESPOSTA, DBN.SEQ_DECISAO, E89["hash"][:16], sh(FALA89)[:16], DECISAO, sh(F20B)[:16], F20))
fontes = {"livro": {"path": DBN.QUADRO, "sha256": L["sha256"], "n_elos": L["n_elos"]}, "evento_autorizacao": {"seq": DBN.SEQ_AUTORIZACAO, "hash": E87["hash"]},
          "recibo_da_resposta": {"path": D87["recibo"], "sha256": sh(REC)}, "evento_decisao": {"seq": DBN.SEQ_DECISAO, "hash": E89["hash"]}, "fala_da_decisao": {"path": D89["fala"], "sha256": sh(FALA89)},
          "fala_20nov": {"path": DBN.FALA_AUTORIZACAO_20NOV, "sha256": sh(F20B)}}
nome = "AUTORIZACAO_v413.txt"
if a:
    fm = os.path.join(DBN.CUNHAGENS_DIR, a[0])
    assert os.path.basename(a[0]) == a[0] and a[0].startswith("OPERADOR_") and a[0].endswith("_verbatim.txt") and os.path.isfile(fm), ("a fala do modo da placa tem de ser um OPERADOR_<...>_verbatim.txt de cunhagens_13out", a[0])
    FMB = open(fm, "rb").read()
    FM = FMB.decode("utf-8").strip()
    assert FM, "a fala do modo da placa esta' vazia"
    texto += " Fala com a escolha do modo da placa (sha16 %s): «%s»; modo da placa: %s." % (sh(FMB)[:16], FM, a[1])
    partes += [FM, sh(FMB)[:16], "modo da placa: %s" % a[1]]
    fontes["fala_do_modo_da_placa"] = {"path": fm, "sha256": sh(FMB), "modo": a[1]}
    nome = "AUTORIZACAO_v413_RELIGAMENTO_%s.txt" % a[1]
faltam = [p_ for p_ in partes if p_ not in texto]
assert not faltam, ("o texto montado nao traz todas as partes que os recibos exigem", faltam)
dados = (texto + "\n").encode("utf-8")
os.makedirs(DBN.SERVICO_DIR, exist_ok=True)
dest = os.path.join(DBN.SERVICO_DIR, nome)
if os.path.exists(dest):
    if open(dest, "rb").read() != dados:
        raise SystemExit("PARO: %s ja existe e difere do que os arquivos dao agora (o livro ou uma fala mudou?): decisao da gerencia; nada foi regravado" % dest)
    print("ja existia igual (idempotente):", dest)
else:
    with open(dest + ".tmp", "xb") as fh:
        fh.write(dados)
    assert open(dest + ".tmp", "rb").read() == dados
    os.replace(dest + ".tmp", dest)
    U.gravar_json_novo(dest[:-4] + ".json", {"contrato": "AUTORIZACAO_v413", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "texto": {"path": dest, "sha256": sh(dados)},
                                             "fontes": fontes, "nota": "montado por script dos arquivos (N4: decisao da gerencia); a gerencia passa o texto por $(cat ...) em V413_AUTORIZACAO_OPERADOR"})
print(json.dumps({"autorizacao": dest, "sha256": U.sha256_arquivo(dest), "caracteres": len(texto), "uso": "V413_AUTORIZACAO_OPERADOR=\"$(cat '%s')\"" % dest.replace("\\", "/")}, ensure_ascii=False))

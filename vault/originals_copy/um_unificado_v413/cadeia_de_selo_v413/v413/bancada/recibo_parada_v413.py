# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] molde v412/bancada_B3_servico/recibo_parada_v412.py (os dois modos, pelo_pid e ja_fora_do_ar; as chaves do recibo REAL da v411),
# com: 2.2 (o livro do quadro conferido INTEIRO pela regra do esboco, sem pular linha ilegivel: util_bn_v413.livro_conferido), N4 (a autorizacao do ciclo da v413, decisao da gerencia: os eventos 1687 e 1689 conferidos
# POR HASH e a fala do operador de 20/11, lida por bytes), N6 (o ultimo religamento conhecido e' o da v411: a v412 nao teve B(n)) e a evidencia do modo ja_fora_do_ar = a conferencia A do dia (saude_bancada.py),
# pinada por sha256 pela gerencia. Nada e' digitado: seqs e lugares vem do delta_bn_v413; hashes, falas e datas sao LIDOS dos arquivos.
"""10-bis-a da v413: recibo da parada do servico da Bancada Um (porta lida do delta_bn), passo do salto B20-v411 -> B21-v413. O script NAO para nada: confere e registra.
Com V413_PARADA=pelo_pid, o PID registrado e' o LIDO DA PORTA antes da parada (V413_PID_PARADO, V413_PID_PARADO_CRIADO), parado pelo PID (nunca por nome), e o script confere que ele ja nao existe.
Com V413_PARADA=ja_fora_do_ar, nenhum PID foi parado: o recibo diz isso, registra o ultimo PID conhecido (o do religamento da v411) como tal e guarda a evidencia (a conferencia A de hoje, V413_SAUDE_RECIBO,
conferida pelo sha256 que a gerencia passa em V413_SAUDE_SHA256; a porta fechada e nenhum um_bancada.py vivo, conferidos agora)."""
import datetime
import hashlib
import json
import os
import socket
import sys

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V413_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V413_AUTORIZACAO_OPERADOR com a autorizacao do operador que cobre este ato (os eventos e a fala, com os hashes): o script nao presume autorizacao"
sys.dont_write_bytecode = True
sys.path.insert(0, D)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

# N4: a autorizacao do ciclo da v413 = os eventos 1687 (o ciclo da Bancada) e 1689 (o salto na v413) do quadro e a fala do operador de 20/11, conferidos POR HASH; o livro e' conferido INTEIRO (2.2)
LIVRO = U.livro_conferido(DBN.QUADRO)
E87, E89 = LIVRO["eventos"].get(DBN.SEQ_AUTORIZACAO), LIVRO["eventos"].get(DBN.SEQ_DECISAO)
assert E87 is not None and E89 is not None, ("os eventos da autorizacao nao estao no livro conferido", DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO)
D87, D89 = E87.get("dados") or {}, E89.get("dados") or {}
assert E87.get("tipo") == "AVISO_AUTORIZACAO_RECEBIDA" and D87.get("versao") == "v412" and D87.get("unidade") == "F0.6" and D87.get("recibo") and D87.get("sha256"), ("o evento %d nao e' o aviso da autorizacao do operador ao ciclo da Bancada (F0.6)" % DBN.SEQ_AUTORIZACAO, E87.get("tipo"))
ORDEM_BYTES = open(D87["recibo"], "rb").read()
assert hashlib.sha256(ORDEM_BYTES).hexdigest() == D87["sha256"], "o recibo da resposta do operador diverge do sha256 que o evento %d registra" % DBN.SEQ_AUTORIZACAO
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = str(json.loads(ORDEM_BYTES.decode("utf-8"))["bench"]["answer"]).strip()   # a resposta inteira do operador, LIDA do recibo
assert E89.get("tipo") == "AVISO_DECISAO_DO_OPERADOR_B21" and E89.get("quem") == "claude-c1" and D89.get("em_resposta_ao_evento") == DBN.SEQ_AUTORIZACAO and D89.get("unidade") == "F0.6" and D89.get("fala"), \
    ("o evento %d nao e' a decisao do operador sobre a B21 em resposta ao %d" % (DBN.SEQ_DECISAO, DBN.SEQ_AUTORIZACAO), E89.get("tipo"))
FALA_DECISAO_BYTES = open(D89["fala"], "rb").read()
FALA_DECISAO_SHA16 = hashlib.sha256(FALA_DECISAO_BYTES).hexdigest()[:16]
DECISAO = str(D89.get("decisao_do_operador") or "").strip()
assert FALA_DECISAO_SHA16 == D89.get("fala_sha16") and DBN.UM_VERSION_BN in DECISAO and DECISAO in FALA_DECISAO_BYTES.decode("utf-8"), "a fala da decisao diverge do sha16 que o evento %d registra, ou nao diz o salto na v413" % DBN.SEQ_DECISAO
FALA_20NOV_BYTES = open(DBN.FALA_AUTORIZACAO_20NOV, "rb").read()
FALA_20NOV = FALA_20NOV_BYTES.decode("utf-8").strip()   # a fala inteira do operador de 20/11, LIDA do arquivo
FALA_20NOV_SHA16 = hashlib.sha256(FALA_20NOV_BYTES).hexdigest()[:16]
assert len(FALA_20NOV) >= 20 and "bancada" in U.texto_normalizado(FALA_20NOV), "a fala do operador de 20/11 nao fala da Bancada"
H87, H89 = E87["hash"][:16], E89["hash"][:16]
assert (("evento %d" % DBN.SEQ_AUTORIZACAO) in AUT and H87 in AUT and ORDEM_SHA16 in AUT and FRASE_DA_ORDEM in AUT and ("evento %d" % DBN.SEQ_DECISAO) in AUT and H89 in AUT and FALA_DECISAO_SHA16 in AUT
        and DECISAO in AUT and FALA_20NOV in AUT and FALA_20NOV_SHA16 in AUT), \
    "a autorizacao passada nao e' a do ciclo da v413 (exige no texto: os eventos %d e %d com os hash16 lidos do livro, o sha16 e a resposta do recibo do %d, a decisao e o sha16 da fala do %d, a fala de 20/11 inteira e o sha16 dela)" % (
        DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO, DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO)
MODO = os.environ.get("V413_PARADA", "").strip()
assert MODO in ("pelo_pid", "ja_fora_do_ar"), "defina V413_PARADA=pelo_pid (o servico estava no ar e foi parado pelo PID lido da porta; com V413_PID_PARADO e V413_PID_PARADO_CRIADO) ou V413_PARADA=ja_fora_do_ar (nada foi parado): o script nao presume qual"
P_REC = os.path.join(DBN.SERVICO_DIR, "RECIBO_PARADA_v413.json")
assert not os.path.exists(P_REC), "o recibo ja existe: nao sobrescrevo"
s = socket.socket()
s.settimeout(1)
aberta = s.connect_ex(("127.0.0.1", DBN.PORTA)) == 0
s.close()
assert not aberta, "a porta %d esta aberta: parar o servico pelo PID antes deste recibo" % DBN.PORTA
VIVOS = U.processos_um_bancada()
n_proc = len(VIVOS)
assert n_proc == 0, "ha %d processo(s) um_bancada.py vivos: parar pelo PID antes deste recibo" % n_proc
rel411 = json.load(open(DBN.RECIBO_RELIGAMENTO_V411, encoding="utf-8"))   # N6: o ultimo religamento conhecido e' o do B(n) da v411 (a v412 nao teve B(n))
pid_v411 = rel411["pid"]
assert str(pid_v411).isdigit() and rel411.get("no_ar_desde") and rel411.get("hora_recibo"), rel411
BOOT = U.ultimo_boot()
if MODO == "pelo_pid":
    PIDP = os.environ.get("V413_PID_PARADO", "").strip()
    assert PIDP.isdigit(), "defina V413_PID_PARADO com o PID lido da porta antes da parada (linha de comando conferida): o script nao presume o PID"
    CRIADO = os.environ.get("V413_PID_PARADO_CRIADO", "").strip()
    assert CRIADO, "defina V413_PID_PARADO_CRIADO com a data/hora de criacao do processo parado (lida de Win32_Process antes da parada)"
    assert U.processo(int(PIDP)) is None, "o PID %s ainda existe: a parada nao se consumou" % PIDP
    PID_REC = int(PIDP)
    EVIDENCIA = None
    PID_ESTADO = "PID lido da porta antes da parada (processo criado em %s; linha de comando conferida), parado pelo PID; conferido aqui que ja nao existe; o religamento da v411 registrou o PID %s, no ar desde %s: %s" % (
        CRIADO, pid_v411, rel411["no_ar_desde"], "igual ao parado" if str(pid_v411) == PIDP else "diferente do parado (o servico foi religado de novo depois do religamento da v411)")
    NOTA = ("nenhum processo um_bancada.py vivo e a porta fechada, conferidos por este script no momento do recibo; o script nao para nada; o PID parado, %s, e' o lido da porta, e a parada que precede este recibo "
            "e' feita pelo PID (nunca por nome), nao por este script; ultimo boot da maquina: %s; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (PIDP, BOOT))
else:
    assert not os.environ.get("V413_PID_PARADO", "").strip() and not os.environ.get("V413_PID_PARADO_CRIADO", "").strip(), "no modo ja_fora_do_ar nenhum PID foi parado: V413_PID_PARADO e V413_PID_PARADO_CRIADO nao podem estar definidos"
    SA_P = os.environ.get("V413_SAUDE_RECIBO", "").strip()
    SA_PINO = os.environ.get("V413_SAUDE_SHA256", "").strip().lower()
    assert SA_P and os.path.isfile(SA_P) and len(SA_PINO) == 64, "defina V413_SAUDE_RECIBO (a conferencia A de hoje, saude_bancada.py) e V413_SAUDE_SHA256 (o sha256 dela, lido por script pela gerencia)"
    SA_BYTES = open(SA_P, "rb").read()
    assert hashlib.sha256(SA_BYTES).hexdigest() == SA_PINO, "a conferencia A diverge do sha256 que a gerencia passou"
    SA = json.loads(SA_BYTES.decode("utf-8"))
    assert SA.get("contrato") == "SAUDE_BANCADA" and SA.get("veredito") in ("FORA_DO_AR", "FORA_DO_AR_APOS_REINICIO") and str(SA.get("quando", ""))[:10] == datetime.date.today().isoformat() \
        and SA.get("porta_aberta") is False and SA.get("processos_um_bancada") == [], ("a conferencia A nao e' de hoje ou nao diz servico fora do ar (porta fechada e nenhum um_bancada.py)", SA.get("veredito"), SA.get("quando"))
    ULT_P = U.processo(int(pid_v411))
    ULT = "AUSENTE" if ULT_P is None else "VIVO|" + str(ULT_P.get("linha_de_comando"))
    assert ULT == "AUSENTE" or (ULT.startswith("VIVO|") and "um_bancada" not in ULT), ("o ultimo PID conhecido (%s) nao foi lido como ausente nem como outro programa" % pid_v411, ULT)
    PID_REC = int(pid_v411)
    EVIDENCIA = {"conferencia_A": {"path": os.path.abspath(SA_P), "sha256": SA_PINO, "veredito": SA.get("veredito"), "quando": SA.get("quando")}, "ultimo_pid_conhecido": ULT[:200]}
    PID_ESTADO = "nenhum PID foi parado: o servico ja estava fora do ar quando o B(n) da v413 comecou; %s e' o ultimo PID conhecido, o do religamento da v411 (no ar desde %s), e hoje %s" % (
        pid_v411, rel411["no_ar_desde"], "o processo ja nao existe" if ULT == "AUSENTE" else "o PID existe, mas e' outro programa (PID reusado): " + ULT[5:][:160])
    NOTA = ("o servico ja estava fora do ar antes do B(n) da v413: a conferencia A de hoje (%s, sha256 %s) diz %s; este script conferiu de novo, no momento do recibo, a porta fechada e nenhum processo um_bancada.py vivo; "
            "ultimo boot da maquina (lido agora): %s; NADA foi parado por esta cadeia, e o pid deste recibo e' o ultimo conhecido (o do religamento da v411), nao um PID parado; quem conferiu e sob que ordem do operador "
            "consta em autorizacao_do_operador" % (os.path.basename(SA_P), SA_PINO[:16], SA.get("veredito"), BOOT))
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-bis-a", "servico": "um_bancada.py", "pid": PID_REC,
       "pid_estado": PID_ESTADO,
       "processos_um_bancada_vivos": n_proc,
       "linha_de_comando": DBN.COMANDO_DO_RITO,
       "porta": DBN.PORTA, "porta_fechada": True,
       "hora_recibo": agora, "hora": agora,
       "nota": NOTA,
       "religar": DBN.COMANDO_DO_RITO + " (pelo recibo_religamento_v413.py: com os logs em estado\\servidor.log e estado\\servidor_erros.log, N9, e o modo da placa escolhido pelo operador)",
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT,
       "modo": MODO,
       "autorizacao_conferida": {"livro": {"path": DBN.QUADRO, "sha256": LIVRO["sha256"], "n_elos": LIVRO["n_elos"], "cabeca": LIVRO["cabeca"]},
                                 "evento_autorizacao": {"seq": DBN.SEQ_AUTORIZACAO, "hash": E87["hash"], "quando": E87.get("quando"), "recibo": D87["recibo"], "recibo_sha256": D87["sha256"], "resposta": FRASE_DA_ORDEM},
                                 "evento_decisao": {"seq": DBN.SEQ_DECISAO, "hash": E89["hash"], "quando": E89.get("quando"), "fala": D89["fala"], "fala_sha16": FALA_DECISAO_SHA16, "decisao": DECISAO},
                                 "fala_20nov": {"path": DBN.FALA_AUTORIZACAO_20NOV, "sha256": hashlib.sha256(FALA_20NOV_BYTES).hexdigest()}},
       "evidencia_fora_do_ar": EVIDENCIA,
       "ultimo_boot": BOOT}
os.makedirs(DBN.SERVICO_DIR, exist_ok=True)
with open(P_REC + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(P_REC + ".tmp", P_REC)
print("ok", P_REC, "modo", MODO, "pid", PID_REC, "pid_recibo_v411", pid_v411, "processos", n_proc)

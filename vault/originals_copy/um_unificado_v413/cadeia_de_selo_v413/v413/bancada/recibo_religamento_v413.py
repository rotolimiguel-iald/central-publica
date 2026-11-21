# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] molde v412/bancada_B3_servico/recibo_religamento_v412.py (a identidade servida contra o Nos e contra o recibo do APLICAR; as chaves do recibo
# REAL da v411), com: 2.2 (o livro do quadro conferido INTEIRO: util_bn_v413.livro_conferido), 2.3 (o recibo do APLICAR achado tambem numa repeticao, bancada_B3_<k>, filtrando o veredito do APLICAR e exigindo
# exatamente 1 cujo manifesto novo seja o do disco), N4 (os eventos 1687 e 1689 por hash e a fala de 20/11; mais a fala do operador com a escolha do MODO DA PLACA, por parametro: sem ela, AGUARDA), N6 (o anterior
# da Bancada e' o B20 da v411) e N9 (este script LANCA o servico, destacado, com stdout e stderr em estado\servidor.log e estado\servidor_erros.log, e registra isso; no modo cpu, CUDA_VISIBLE_DEVICES=-1 no processo
# lancado). A identidade e' lida SO' de /api/contratos (nunca /api/estado, que cria contexto CUDA).
"""10-ter da v413: religa o servico da Bancada Um e grava o recibo do religamento. Confere a identidade servida (/api/contratos) contra o Nos (um.py e selo lidos na hora) e contra o recibo do APLICAR
(B21-v413-<data>-R1, o manifesto novo). Parametros: a variavel da autorizacao (com os hashes; a mesma da parada), V413_MODO_PLACA (cpu | normal) e V413_FALA_MODO_PLACA (o NOME do arquivo da fala do operador com a
escolha, em work\\cunhagens_13out). Sem a fala ou o modo: AGUARDA_OPERADOR (rc 20), nada e' lancado. Se a identidade servida nao confere, o processo lancado FICA (parar e' ato do operador, pelo PID que a recusa grava)."""
import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time

D = os.path.dirname(os.path.abspath(__file__))
AUT = os.environ.get("V413_AUTORIZACAO_OPERADOR", "").strip()
assert AUT, "defina V413_AUTORIZACAO_OPERADOR com a autorizacao do operador que cobre este ato (os eventos e as falas, com os hashes): o script nao presume autorizacao"
sys.dont_write_bytecode = True
sys.path.insert(0, D)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

# N4: os eventos 1687 e 1689 por hash e a fala de 20/11 (o livro conferido INTEIRO, 2.2)
LIVRO = U.livro_conferido(DBN.QUADRO)
E87, E89 = LIVRO["eventos"].get(DBN.SEQ_AUTORIZACAO), LIVRO["eventos"].get(DBN.SEQ_DECISAO)
assert E87 is not None and E89 is not None, ("os eventos da autorizacao nao estao no livro conferido", DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO)
D87, D89 = E87.get("dados") or {}, E89.get("dados") or {}
assert E87.get("tipo") == "AVISO_AUTORIZACAO_RECEBIDA" and D87.get("versao") == "v412" and D87.get("unidade") == "F0.6" and D87.get("recibo") and D87.get("sha256"), ("o evento %d nao e' o aviso da autorizacao do operador ao ciclo da Bancada (F0.6)" % DBN.SEQ_AUTORIZACAO, E87.get("tipo"))
ORDEM_BYTES = open(D87["recibo"], "rb").read()
assert hashlib.sha256(ORDEM_BYTES).hexdigest() == D87["sha256"], "o recibo da resposta do operador diverge do sha256 que o evento %d registra" % DBN.SEQ_AUTORIZACAO
ORDEM_SHA16 = hashlib.sha256(ORDEM_BYTES).hexdigest()[:16]
FRASE_DA_ORDEM = str(json.loads(ORDEM_BYTES.decode("utf-8"))["bench"]["answer"]).strip()
assert E89.get("tipo") == "AVISO_DECISAO_DO_OPERADOR_B21" and E89.get("quem") == "claude-c1" and D89.get("em_resposta_ao_evento") == DBN.SEQ_AUTORIZACAO and D89.get("unidade") == "F0.6" and D89.get("fala"), \
    ("o evento %d nao e' a decisao do operador sobre a B21 em resposta ao %d" % (DBN.SEQ_DECISAO, DBN.SEQ_AUTORIZACAO), E89.get("tipo"))
FALA_DECISAO_BYTES = open(D89["fala"], "rb").read()
FALA_DECISAO_SHA16 = hashlib.sha256(FALA_DECISAO_BYTES).hexdigest()[:16]
DECISAO = str(D89.get("decisao_do_operador") or "").strip()
assert FALA_DECISAO_SHA16 == D89.get("fala_sha16") and DBN.UM_VERSION_BN in DECISAO and DECISAO in FALA_DECISAO_BYTES.decode("utf-8"), "a fala da decisao diverge do sha16 que o evento %d registra, ou nao diz o salto na v413" % DBN.SEQ_DECISAO
FALA_20NOV_BYTES = open(DBN.FALA_AUTORIZACAO_20NOV, "rb").read()
FALA_20NOV = FALA_20NOV_BYTES.decode("utf-8").strip()
FALA_20NOV_SHA16 = hashlib.sha256(FALA_20NOV_BYTES).hexdigest()[:16]
assert len(FALA_20NOV) >= 20 and "bancada" in U.texto_normalizado(FALA_20NOV), "a fala do operador de 20/11 nao fala da Bancada"
H87, H89 = E87["hash"][:16], E89["hash"][:16]
assert (("evento %d" % DBN.SEQ_AUTORIZACAO) in AUT and H87 in AUT and ORDEM_SHA16 in AUT and FRASE_DA_ORDEM in AUT and ("evento %d" % DBN.SEQ_DECISAO) in AUT and H89 in AUT and FALA_DECISAO_SHA16 in AUT
        and DECISAO in AUT and FALA_20NOV in AUT and FALA_20NOV_SHA16 in AUT), \
    "a autorizacao passada nao e' a do ciclo da v413 (exige no texto: os eventos %d e %d com os hash16 lidos do livro, o sha16 e a resposta do recibo do %d, a decisao e o sha16 da fala do %d, a fala de 20/11 inteira e o sha16 dela)" % (
        DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO, DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO)
# o modo da placa: a escolha e' do operador (DIAGNOSTICO 5.2); sem a fala dele, AGUARDA (nada e' lancado)
MODO_PLACA = os.environ.get("V413_MODO_PLACA", "").strip()
FALA_MODO_NOME = os.environ.get("V413_FALA_MODO_PLACA", "").strip()
if not FALA_MODO_NOME or MODO_PLACA not in DBN.MODOS_DA_PLACA:
    print("AGUARDA_OPERADOR: o religamento exige a fala do operador com a escolha do modo da placa (V413_FALA_MODO_PLACA = o NOME do arquivo em %s) e o modo escolhido (V413_MODO_PLACA = %s); nada foi lancado"
          % (DBN.CUNHAGENS_DIR, " | ".join(DBN.MODOS_DA_PLACA)))
    sys.exit(20)
FALA_MODO_P = os.path.join(DBN.CUNHAGENS_DIR, FALA_MODO_NOME)
assert os.path.basename(FALA_MODO_NOME) == FALA_MODO_NOME and FALA_MODO_NOME.startswith("OPERADOR_") and FALA_MODO_NOME.endswith("_verbatim.txt") and os.path.isfile(FALA_MODO_P), \
    ("a fala do modo da placa tem de ser um arquivo OPERADOR_<...>_verbatim.txt de %s" % DBN.CUNHAGENS_DIR, FALA_MODO_NOME)
FALA_MODO_BYTES = open(FALA_MODO_P, "rb").read()
FALA_MODO = FALA_MODO_BYTES.decode("utf-8").strip()
FALA_MODO_SHA16 = hashlib.sha256(FALA_MODO_BYTES).hexdigest()[:16]
assert FALA_MODO and FALA_MODO in AUT and FALA_MODO_SHA16 in AUT and ("modo da placa: %s" % MODO_PLACA) in AUT, \
    "a autorizacao passada nao cita a fala do modo da placa (inteira, com o sha16) e o modo escolhido na forma 'modo da placa: %s'" % MODO_PLACA
P_REC = os.path.join(DBN.SERVICO_DIR, "RECIBO_RELIGAMENTO_v413.json")
assert not os.path.exists(P_REC), "o recibo ja existe: nao sobrescrevo (e nao religo de novo)"
# 2.3 e N6: o recibo do APLICAR (bancada_B3 ou uma repeticao bancada_B3_<k>), so' os de veredito APLICADA do salto, exatamente 1 cujo manifesto novo e' o do disco
MAN_DISCO = U.sha256_arquivo(DBN._BANCADA_CONTRATOS)
CANDS = sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN))
               + glob.glob(os.path.join(DBN.V413, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)))
APLICADOS = [p_ for p_ in CANDS if (lambda j_: j_.get("veredito") == DBN.VEREDITO_APLICAR and (j_.get("manifesto_novo") or {}).get("sha256") == MAN_DISCO)(U.ler_json(p_))]
assert len(APLICADOS) == 1, ("exige exatamente 1 recibo do APLICAR do salto cujo manifesto novo e' o do disco (%s)" % MAN_DISCO[:16], [os.path.relpath(x_, DBN.V413) for x_ in CANDS])
RB = APLICADOS[0]
b = U.ler_json(RB)
ma = b["manifesto_anterior"]
n_esp = int(ma["deployment_id"].split("-")[0][1:]) + 1
assert ma["deployment_id"] == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"] and ma["version"] == DBN.BANCADA_ANTERIOR and n_esp == DBN.N_DO_SALTO, ("o APLICAR nao partiu do B20 da v411", ma.get("deployment_id"))
sal = b.get("salto") or {}
assert ((sal.get("de") or {}).get("versao"), (sal.get("ate") or {}).get("versao"), sal.get("proxima_a_selar")) == (DBN.BANCADA_ANTERIOR, DBN.UM_PY_ANTERIOR, DBN.UM_VERSION_BN), ("o APLICAR nao e' o salto v411 -> v413", sal.get("de"), sal.get("ate"))
man_novo = b["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
dep_esp = b["manifesto_novo"]["deployment_id"]
assert DBN.RE_DEPLOYMENT_NOVO.match(dep_esp) and b["aplicacao"]["pos_conferencia"]["deployment_id"] == dep_esp and man_novo == b["manifesto_novo"]["sha256"] == MAN_DISCO, (dep_esp, man_novo[:16], MAN_DISCO[:16])
um_sha = U.sha256_arquivo(os.path.join(DBN.NOS, "um.py"))
selo_sha = U.sha256_arquivo(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
# este script e' quem religa: a porta fechada e nenhum um_bancada.py vivo antes de lancar
assert not U.porta_aberta(DBN.PORTA), "a porta %d ja responde: este script religa (N9) e nao sobe um segundo servico" % DBN.PORTA
assert not U.processos_um_bancada(), "ha' processo um_bancada.py vivo: este script nao sobe um segundo servico"
# N9: o lancamento destacado, com o stdout e o stderr anexados aos logs de estado\ (os tamanhos de antes ficam no recibo: o que esta subida escreveu comeca ali)
TAM_ANTES = {p_: (os.path.getsize(p_) if os.path.exists(p_) else None) for p_ in (DBN.LOG_SERVIDOR, DBN.LOG_SERVIDOR_ERROS)}
AMB = dict(os.environ)
if MODO_PLACA == "cpu":
    AMB["CUDA_VISIBLE_DEVICES"] = "-1"           # no Windows uma variavel vazia e' apagada: o valor tem de ser -1 (torch.cuda.is_available() = False; o motor em CPU)
else:
    AMB.pop("CUDA_VISIBLE_DEVICES", None)
RETIRADAS = []                                   # (revisao B7) o servidor nao roda isolado: nenhuma variavel PYTHON* do ambiente de quem religa chega a ele
for v_ in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE", "PYTHONPLATLIBDIR", "PYTHONEXECUTABLE", "PYTHONINSPECT", "PYTHONOPTIMIZE"):
    if v_ in AMB:
        RETIRADAS.append(v_)
    AMB.pop(v_, None)
COMANDO = [DBN.PYTHONW, "-X", "utf8", DBN.UM_BANCADA]
_out = open(DBN.LOG_SERVIDOR, "ab")
_err = open(DBN.LOG_SERVIDOR_ERROS, "ab")
FLAGS = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
try:                                             # (revisao B9) sair do Job da sessao que religa, para o servidor nao morrer com ela; se o Job nao deixa, lanca sem e o recibo diz
    PROC = subprocess.Popen(COMANDO, cwd=DBN.PRODUCAO, stdout=_out, stderr=_err, stdin=subprocess.DEVNULL, env=AMB, creationflags=FLAGS | subprocess.CREATE_BREAKAWAY_FROM_JOB, close_fds=True)
    BREAKAWAY = True
except OSError:
    PROC = subprocess.Popen(COMANDO, cwd=DBN.PRODUCAO, stdout=_out, stderr=_err, stdin=subprocess.DEVNULL, env=AMB, creationflags=FLAGS, close_fds=True)
    BREAKAWAY = False
_out.close()
_err.close()
PID_LANCADO = PROC.pid
LANCADO_EM = datetime.datetime.now().astimezone().isoformat()
c = None
t0 = time.time()
while time.time() - t0 < 120:
    try:
        c = U.get_json("http://127.0.0.1:%d/api/contratos" % DBN.PORTA, timeout=5)
        break
    except Exception:   # noqa: BLE001   (a porta ainda nao abriu)
        time.sleep(2)
PROB = []
try:                                             # (revisao B8) a leitura do processo pode falhar depois do lancamento: vira recusa gravada, com o PID lancado, nunca traceback mudo
    PID_PORTA = U.pid_da_porta(DBN.PORTA)
    PROC_INFO = U.processo(PID_PORTA) if PID_PORTA else None
except Exception as e_:   # noqa: BLE001
    PID_PORTA, PROC_INFO = None, None
    PROB.append("a leitura do processo da porta falhou: %r" % (e_,))
if c is None:
    PROB.append("/api/contratos nao respondeu em 120 s")
else:
    for k_, v_ in (("ok", True), ("canonical_version", DBN.UM_VERSION_BN), ("deployment_id", dep_esp), ("canonical_manifest_sha256", man_novo), ("um_py_sha256", um_sha), ("seal_sha256", selo_sha)):
        if c.get(k_) != v_:
            PROB.append("%s servido %r != esperado %r" % (k_, c.get(k_), v_))
if PID_PORTA != PID_LANCADO or not PROC_INFO or "um_bancada.py" not in PROC_INFO.get("linha_de_comando", ""):
    PROB.append("o PID da porta (%r) nao e' o lancado (%r) ou nao e' o um_bancada.py (%r)" % (PID_PORTA, PID_LANCADO, (PROC_INFO or {}).get("linha_de_comando")))
TAM_DEPOIS = {p_: (os.path.getsize(p_) if os.path.exists(p_) else None) for p_ in (DBN.LOG_SERVIDOR, DBN.LOG_SERVIDOR_ERROS)}
LOG = {"stdout": DBN.LOG_SERVIDOR, "stderr": DBN.LOG_SERVIDOR_ERROS, "bytes_antes": TAM_ANTES, "bytes_depois": TAM_DEPOIS, "modo": "anexado (ab), como o atalho abrir_bancada.pyw (N9)"}
if PROB:
    rp_ = os.path.join(DBN.SERVICO_DIR, "RECUSA_RELIGAMENTO_v413_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(DBN.SERVICO_DIR, exist_ok=True)
    U.gravar_json_novo(rp_, {"passo": "10-ter", "recusa": PROB, "pid_lancado": PID_LANCADO, "lancado_em": LANCADO_EM, "pid_da_porta": PID_PORTA, "processo": PROC_INFO, "servido": c, "log": LOG,
                             "modo_da_placa": MODO_PLACA, "nota": "o processo lancado FICA: parar e' ato do operador, pelo PID (nunca por nome); nenhum recibo de religamento foi gravado"})
    raise SystemExit("RELIGAMENTO_RECUSADO (o processo %s ficou; recusa em %s): %s" % (PID_LANCADO, rp_, "; ".join(PROB)))
agora = datetime.datetime.now().astimezone().isoformat()
rec = {"passo": "10-ter", "servico": "um_bancada.py", "porta": DBN.PORTA,
       "comando": " ".join('"%s"' % x_ if " " in x_ else x_ for x_ in COMANDO),
       "no_ar_desde": PROC_INFO.get("criado"), "pronta": "nao lida: /api/estado cria contexto CUDA; a identidade vem de /api/contratos",
       "identidade": {k: c.get(k) for k in ("deployment_id", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256")},
       "versao_servida": c.get("canonical_version"), "manifesto_sha256": c.get("canonical_manifest_sha256"),
       "recibo_do_10_bis": {"path": os.path.abspath(RB), "sha256": U.sha256_arquivo(RB)},
       "pid": PID_PORTA,
       "mcp": "a reconexao dos adaptadores MCP das sessoes (/mcp) e' ato do operador em cada sessao aberta",
       "hora_recibo": agora, "hora": agora,
       "autor": "claude-c1 (gerencia)", "autorizacao_do_operador": AUT,
       "modo_da_placa": MODO_PLACA,
       "fala_do_modo_da_placa": {"path": FALA_MODO_P, "sha256": hashlib.sha256(FALA_MODO_BYTES).hexdigest(), "fala": FALA_MODO},
       "ambiente_do_processo": {"CUDA_VISIBLE_DEVICES": AMB.get("CUDA_VISIBLE_DEVICES"), "variaveis_python_retiradas": RETIRADAS,
                                "nota": "cpu: -1 (o motor em CPU, sem contexto CUDA); normal: a variavel retirada do ambiente do processo lancado; nenhuma variavel PYTHON* chega ao servidor"},
       "log": LOG,
       "autorizacao_conferida": {"livro": {"path": DBN.QUADRO, "sha256": LIVRO["sha256"], "n_elos": LIVRO["n_elos"], "cabeca": LIVRO["cabeca"]},
                                 "evento_autorizacao": {"seq": DBN.SEQ_AUTORIZACAO, "hash": E87["hash"], "recibo_sha256": D87["sha256"], "resposta": FRASE_DA_ORDEM},
                                 "evento_decisao": {"seq": DBN.SEQ_DECISAO, "hash": E89["hash"], "fala_sha16": FALA_DECISAO_SHA16, "decisao": DECISAO},
                                 "fala_20nov": {"path": DBN.FALA_AUTORIZACAO_20NOV, "sha256": hashlib.sha256(FALA_20NOV_BYTES).hexdigest()}},
       "processo": {"pid_lancado": PID_LANCADO, "lancado_em": LANCADO_EM, "pid_da_porta": PID_PORTA, "linha_de_comando": PROC_INFO.get("linha_de_comando"), "nome": PROC_INFO.get("nome"),
                    "breakaway": BREAKAWAY, "nota_breakaway": "True: o servidor saiu do Job da sessao que religou; False: o Job nao deixou (o PID vivo e' conferido no passo 11)"}}
os.makedirs(DBN.SERVICO_DIR, exist_ok=True)
with open(P_REC + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False, indent=1))
os.replace(P_REC + ".tmp", P_REC)
print("ok", P_REC, "pid", rec["pid"], rec["versao_servida"], rec["manifesto_sha256"][:16], "um.py", um_sha[:16], "modo da placa", MODO_PLACA)

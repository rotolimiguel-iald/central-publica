# -*- coding: utf-8 -*-
"""trocar_modo_bancada_v413.py -- gerencia c1, 21/11/2026: TROCA o modo da placa do servico da Bancada Um de cpu para normal, por escolha do
operador (selecao num dialogo da gerencia, depois da correcao «O treino da IALD já acabou há muito tempo»: a premissa «treino na placa» da
pergunta do modo cpu estava errada; o erro e' da gerencia). Nao e' passo do ciclo do B(n) (fechado: os tres recibos e o pino conjunto ficam
como estao); e' uma troca operacional AO LADO, com recibo proprio FORA de bancada_B3* (a custodia le os tres recibos de la; um quarto ali
quebraria a resolucao), em v413\\bn_pos_selo\\RECIBO_TROCA_DE_MODO_v413_normal.json.
Passos: (1) confere o recibo do religamento (cpu, PID) e que o PID e' o que escuta a porta e e' o um_bancada.py, e o unico; (2) para PELO PID
(taskkill /PID /T /F; nunca por nome) e confere a porta fechada e nenhum um_bancada.py vivo; (3) lanca como o recibo_religamento_v413.py (o
mesmo comando, cwd, logs anexados, flags, sem variaveis PYTHON*), so' sem CUDA_VISIBLE_DEVICES; (4) confere /api/contratos (ok, v413, o
deployment e o manifesto do APLICAR, o um.py e o selo do Nos) e que o PID da porta e' o lancado; (5) grava o recibo. Se algo falhar depois do
lancamento, o processo lancado FICA (parar e' ato pelo PID que o recibo grava). Recusa -O."""
import datetime, glob, hashlib, json, os, subprocess, sys, time

if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O (as guardas sao assert)")
D = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, D)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CUN = DBN.CUNHAGENS_DIR
FALA = os.path.join(CUN, "OPERADOR_21nov_trocar_a_bancada_para_o_modo_normal_agora_no_dialogo_da_gerencia_verbatim.txt")
FALA_T = os.path.join(CUN, "OPERADOR_21nov_o_treino_da_iald_ja_acabou_ha_muito_tempo_verbatim.txt")
RR = os.path.join(DBN.SERVICO_DIR, "RECIBO_RELIGAMENTO_v413.json")
OUT = os.path.join(DBN.V413, "bn_pos_selo", "RECIBO_TROCA_DE_MODO_v413_normal.json")
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
for p in (FALA, FALA_T, RR):
    assert os.path.isfile(p), p
assert not os.path.exists(OUT), "o recibo da troca ja existe: nao troco de novo"
r = U.ler_json(RR)
PID_ANT = int(r["pid"])
assert r.get("modo_da_placa") == "cpu", ("o religamento nao foi em cpu", r.get("modo_da_placa"))
# a identidade esperada: a do APLICAR (como no recibo do religamento)
APL = [p for p in sorted(glob.glob(os.path.join(DBN.V413, "bancada_B3", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.UM_VERSION_BN)))
       if U.ler_json(p).get("veredito") == DBN.VEREDITO_APLICAR]
assert len(APL) == 1, APL
b = U.ler_json(APL[0])
dep_esp = b["manifesto_novo"]["deployment_id"]
man_novo = b["aplicacao"]["pos_conferencia"]["canonical_manifest_sha256"]
assert man_novo == U.sha256_arquivo(DBN._BANCADA_CONTRATOS), "o manifesto em disco nao e' o do APLICAR"
um_sha = U.sha256_arquivo(os.path.join(DBN.NOS, "um.py"))
selo_sha = U.sha256_arquivo(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
# (1) o servico em cpu, pelo PID do recibo
assert U.porta_aberta(DBN.PORTA), "a porta esta' fechada: nao ha' servico em cpu para trocar"
pp = U.pid_da_porta(DBN.PORTA)
info_ant = U.processo(pp) if pp else None
assert pp == PID_ANT and info_ant and "um_bancada.py" in info_ant["linha_de_comando"], ("o PID da porta nao e' o do recibo do religamento", pp, PID_ANT)
vivos = U.processos_um_bancada()
assert [x["pid"] for x in vivos] == [PID_ANT], ("ha' outro um_bancada.py vivo alem do do recibo", [x["pid"] for x in vivos])
c_ant = U.get_json("http://127.0.0.1:%d/api/contratos" % DBN.PORTA, timeout=10)
# (2) parar PELO PID
PARADO_EM = datetime.datetime.now().astimezone().isoformat()
k = subprocess.run(["taskkill", "/PID", str(PID_ANT), "/T", "/F"], capture_output=True, stdin=subprocess.DEVNULL)
t0 = time.time()
while time.time() - t0 < 60 and (U.processo(PID_ANT) is not None or U.porta_aberta(DBN.PORTA)):
    time.sleep(1)
assert U.processo(PID_ANT) is None and not U.porta_aberta(DBN.PORTA), ("o servico em cpu nao parou pelo PID", k.returncode, k.stdout[-200:], k.stderr[-200:])
assert not U.processos_um_bancada(), "sobrou um_bancada.py vivo depois da parada pelo PID"
# (3) lancar no modo normal, como o recibo_religamento_v413.py
TAM_ANTES = {p_: (os.path.getsize(p_) if os.path.exists(p_) else None) for p_ in (DBN.LOG_SERVIDOR, DBN.LOG_SERVIDOR_ERROS)}
AMB = dict(os.environ)
AMB.pop("CUDA_VISIBLE_DEVICES", None)
RETIRADAS = [v_ for v_ in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE", "PYTHONPLATLIBDIR", "PYTHONEXECUTABLE", "PYTHONINSPECT", "PYTHONOPTIMIZE") if v_ in AMB]
for v_ in RETIRADAS:
    AMB.pop(v_, None)
COMANDO = [DBN.PYTHONW, "-X", "utf8", DBN.UM_BANCADA]
_out, _err = open(DBN.LOG_SERVIDOR, "ab"), open(DBN.LOG_SERVIDOR_ERROS, "ab")
FLAGS = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
try:
    PROC = subprocess.Popen(COMANDO, cwd=DBN.PRODUCAO, stdout=_out, stderr=_err, stdin=subprocess.DEVNULL, env=AMB, creationflags=FLAGS | subprocess.CREATE_BREAKAWAY_FROM_JOB, close_fds=True)
    BREAKAWAY = True
except OSError:
    PROC = subprocess.Popen(COMANDO, cwd=DBN.PRODUCAO, stdout=_out, stderr=_err, stdin=subprocess.DEVNULL, env=AMB, creationflags=FLAGS, close_fds=True)
    BREAKAWAY = False
_out.close(); _err.close()
PID_NOVO = PROC.pid
LANCADO_EM = datetime.datetime.now().astimezone().isoformat()
c = None
t0 = time.time()
while time.time() - t0 < 180:
    try:
        c = U.get_json("http://127.0.0.1:%d/api/contratos" % DBN.PORTA, timeout=5)
        break
    except Exception:  # noqa: BLE001  (a porta ainda nao abriu)
        time.sleep(2)
# (4) a identidade servida e o PID
PROB = []
try:
    PID_PORTA = U.pid_da_porta(DBN.PORTA)
    INFO = U.processo(PID_PORTA) if PID_PORTA else None
except Exception as e_:  # noqa: BLE001
    PID_PORTA, INFO = None, None
    PROB.append("a leitura do processo da porta falhou: %r" % (e_,))
if c is None:
    PROB.append("/api/contratos nao respondeu em 180 s")
else:
    for k_, v_ in (("ok", True), ("canonical_version", DBN.UM_VERSION_BN), ("deployment_id", dep_esp), ("canonical_manifest_sha256", man_novo), ("um_py_sha256", um_sha), ("seal_sha256", selo_sha)):
        if c.get(k_) != v_:
            PROB.append("%s servido %r != esperado %r" % (k_, c.get(k_), v_))
if PID_PORTA != PID_NOVO or not INFO or "um_bancada.py" not in INFO.get("linha_de_comando", ""):
    PROB.append("o PID da porta (%r) nao e' o lancado (%r) ou nao e' o um_bancada.py" % (PID_PORTA, PID_NOVO))
TAM_DEPOIS = {p_: (os.path.getsize(p_) if os.path.exists(p_) else None) for p_ in (DBN.LOG_SERVIDOR, DBN.LOG_SERVIDOR_ERROS)}
rec = {"contrato": "RECIBO_TROCA_DE_MODO_v413", "ok": not PROB, "problemas": PROB, "quando": datetime.datetime.now().astimezone().isoformat(),
       "autor": "claude-c1 (gerencia)", "o_que_e": "troca operacional do modo da placa (cpu -> normal), ao lado do ciclo do B(n) ja' fechado; nao substitui o RECIBO_RELIGAMENTO_v413.json",
       "fala_do_operador": {"path": FALA, "sha256": sh(FALA), "fala": open(FALA, encoding="utf-8").read()},
       "antecedente": {"path": FALA_T, "sha256": sh(FALA_T), "fala": open(FALA_T, encoding="utf-8").read(),
                       "nota": "a premissa «treino na placa» da pergunta do modo cpu era da gerencia e estava errada"},
       "anterior": {"recibo_religamento": {"path": RR, "sha256": sh(RR)}, "pid": PID_ANT, "modo_da_placa": "cpu", "processo": info_ant,
                    "contratos_servidos": {k_: c_ant.get(k_) for k_ in ("canonical_version", "deployment_id", "canonical_manifest_sha256")},
                    "parado_em": PARADO_EM, "parado_por": "taskkill /PID %d /T /F (pelo PID, nunca por nome)" % PID_ANT, "taskkill_rc": k.returncode},
       "novo": {"pid": PID_NOVO, "pid_da_porta": PID_PORTA, "processo": INFO, "modo_da_placa": "normal", "lancado_em": LANCADO_EM, "comando": COMANDO,
                "cwd": DBN.PRODUCAO, "breakaway_do_job": BREAKAWAY, "variaveis_python_retiradas": RETIRADAS, "cuda_visible_devices": "nao definida (modo normal)",
                "contratos_servidos": c, "esperado": {"versao": DBN.UM_VERSION_BN, "deployment_id": dep_esp, "manifesto": man_novo, "um_py": um_sha, "selo": selo_sha}},
       "log": {"stdout": DBN.LOG_SERVIDOR, "stderr": DBN.LOG_SERVIDOR_ERROS, "bytes_antes": TAM_ANTES, "bytes_depois": TAM_DEPOIS},
       "nota": ("o processo lancado FICA mesmo com problema: parar e' ato pelo PID %d" % PID_NOVO) if PROB else "a Bancada serve a v413 no modo normal"}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bb = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = OUT + ".tmp"; open(tmp, "wb").write(bb); assert os.path.getsize(tmp) == len(bb); os.replace(tmp, OUT)
print("%s %s | pid %d (cpu) -> %d (normal) | servido %s %s | problemas: %s" % ("ok" if not PROB else "PROBLEMA", OUT, PID_ANT, PID_NOVO,
      (c or {}).get("canonical_version"), ((c or {}).get("canonical_manifest_sha256") or "")[:16], PROB or "nenhum"))
sys.exit(0 if not PROB else 1)

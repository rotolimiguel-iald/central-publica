# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11, construtor do B(n) da v413, agente da gerencia c1] revisao M3 (ordem da gerencia): o ensaio a seco do pos-selo, PREPARADO para rodar DEPOIS do selo da v413 e ANTES do pos-selo real.
"""ensaio_a_seco_pos_selo_v413.py -- os passos 10 a 11 do B(n) da v413 contra COPIAS da Bancada e do Nos num mundo de ensaio (pasta nova, --mundo), com o esboco R3.6 REAL em --sandbox.
Nada e' gravado na Bancada nem no Nos reais (so' lidos, para copiar); o servico real nao e' tocado; o esboco grava so' sob --saida-esboco (C:\\t\\vb98, uma raiz que ele admite; nunca vb24 nem vb25); o resto vai ao mundo.
  (A) o mundo: o Nos do mundo = copia da v412 (--base-v412); a Bancada do mundo = copia do codigo e das fontes relativas da Bancada de origem, com o manifesto reapontado ao Nos do mundo (os sha256 que ela pina ficam:
      com o Nos do mundo na v412, o canonical.py copiado recusa PIN_CHANGED, como na producao); o quadro do mundo (os eventos 1687 e 1689 copiados, a cadeia de hash refeita, os arquivos que eles nomeiam copiados);
      um iald.py do mundo (so' anotar); um servidor MINIMO de contratos (o canonical_state do canonical.py copiado; nenhum motor, lago ou placa); as copias dos scripts do B(n) com o delta_bn reapontado;
  (B) o pre-selo do salto no mundo: o esboco em pre_selo ensaio com a bateria da v412 e a cadeia (o salto embute o manifesto do mundo);
  (C) a v413 no Nos do mundo (copia de --nos-v413, o Nos selado);
  (D) passo 10: a bateria da v413 do mundo (o gerador real, com um pino minimo do candidato do mundo) e o esboco em pos_selo ensaio com o recibo pre-selo do mundo, a cadeia, o selo e o kernel anteriores da v412 e,
      quando --pinos-bn os pina, o recibo do kernel e os criterios; o b3_recibo (copia);
  (E) 10a: a conferencia A do mundo (a porta do mundo fechada) e a parada ja_fora_do_ar (copia), com o texto do montar_autorizacao (copia);
  (F) o evento (copia; o iald.py do mundo);
  (G) 10b: o esboco em pos_selo APLICAR --sandbox, com o evento conferido pelo livro do mundo (--eventos); o b3_recibo aplicar (copia);
  (H) 10c: o religamento (copia) lanca o servidor MINIMO em modo cpu e confere a identidade servida;
  (I) 11: o fechar (copia), a entrega na pasta bench do mundo e o aviso F0.6 (copia; o iald.py do mundo).
Com --sem-bateria, a bateria e' pulada em B e D (o bloco da bateria vira PASSA sintetico, dito no resultado) e G, H e I nao rodam (o esboco proibe aplicar sem bateria): e' o auto-teste de antes do selo.
Os processos lancados sao parados pelo PID deles; o mundo e o sandbox do esboco sao apagados no fim (salvo --manter). As variaveis do ambiente dos subprocessos levam CUDA_VISIBLE_DEVICES=-1 (a placa nao e' usada).
Grava RESULTADO_ENSAIO_A_SECO_POS_SELO_v413_<carimbo>.json em v413\\bancada\\ensaio_a_seco.
uso, depois do selo (leva minutos: rodar em segundo plano ou com timeout de 600000 ms): python -I -B -X utf8 ensaio_a_seco_pos_selo_v413.py --mundo <pasta nova fora de work>
uso, auto-teste antes do selo: ... --mundo <...> --sem-bateria --nos-v413 <v413 falsa> --base-v412 <...> --base-v411 <...> --bancada-origem <...> --cadeia-pino <...> --bateria-v412-pinos <...> --pinos-bn-v411 <...>
    --religamento-v411 <...> --parada-v411 <...> --quadro <...> --cunhagens <...>"""
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--mundo", required=True)
ap.add_argument("--nos-v413", default=DBN.NOS)
ap.add_argument("--base-v412", default=DBN.BASE_UM_PY_ANTERIOR)
ap.add_argument("--base-v411", default=DBN.BASE_BANCADA_ANTERIOR)
ap.add_argument("--bancada-origem", default=DBN.PRODUCAO)
ap.add_argument("--cadeia-pino", default=DBN.PINO_CADEIA_ARQ)
ap.add_argument("--bateria-v412-pinos", default=os.path.join(DBN.BATERIA_V412_DIR, "PINOS_BATERIA_v412.json"))
ap.add_argument("--pinos-bn", default=DBN.PINOS_BN_ARQ, help="o PINOS_BN real: so' o recibo do kernel e os criterios sao lidos dele (quando existem)")
ap.add_argument("--pinos-bn-v411", default=DBN.PINOS_BN_V411_ARQ)
ap.add_argument("--religamento-v411", default=DBN.RECIBO_RELIGAMENTO_V411)
ap.add_argument("--parada-v411", default=DBN.RECIBO_PARADA_V411)
ap.add_argument("--quadro", default=DBN.QUADRO)
ap.add_argument("--cunhagens", default=DBN.CUNHAGENS_DIR)
ap.add_argument("--saida-esboco", default=os.path.join("C:" + os.sep, "t", "vb98"))
ap.add_argument("--porta", type=int, default=18798)
ap.add_argument("--sem-bateria", action="store_true")
ap.add_argument("--manter", action="store_true")
a = ap.parse_args()
PY = DBN.PYTHON
sha = U.sha256_arquivo
W = os.path.abspath(a.mundo)
SB = os.path.abspath(a.saida_esboco)
ETAPAS, PIDS = [], []
OUT_DIR = os.path.join(HERE, "ensaio_a_seco")
CARIMBO = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def etapa(nome, ok, obs=None):
    ETAPAS.append({"etapa": nome, "ok": ok, "observado": obs})
    print({True: "OK   ", False: "FALHA", None: "NAO_EXECUTADO"}[ok], nome, "" if ok else ("| %s" % str(obs)[:400]))
    return ok


def escreve(p, b):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(b.encode("utf-8") if isinstance(b, str) else b)
    return p


def jdump(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def copia(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    assert sha(src) == sha(dst), dst
    return dst


def rodar(args, env_extra=None, cwd=None, timeout=1800):
    env = dict(os.environ)
    for k in [k for k in env if k.startswith("V413_") or k.startswith("PYTHON")]:
        env.pop(k)
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env.update(env_extra or {})
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=cwd or W, stdin=subprocess.DEVNULL, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def ultima_json(txt):
    ls = [l for l in txt.splitlines() if l.strip().startswith("{")]
    return json.loads(ls[-1]) if ls else {}


def porta_aberta(p):
    s = socket.socket(); s.settimeout(1)
    try:
        return s.connect_ex(("127.0.0.1", p)) == 0
    finally:
        s.close()


def finalizar(rc_final):
    for pid in PIDS:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
    for _ in range(40):
        if not porta_aberta(a.porta):
            break
        time.sleep(0.25)
    vivos = [p for p in PIDS if U.processo(p) is not None]
    if not a.manter:
        for d in (SB, W):
            if os.path.isdir(d):
                shutil.rmtree(d, ignore_errors=True)
    res = {"contrato": "RESULTADO_ENSAIO_A_SECO_POS_SELO_v413", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "script": U.pinar(os.path.abspath(__file__)),
           "entradas": {k: getattr(a, k) for k in vars(a)}, "sem_bateria": a.sem_bateria, "etapas": ETAPAS, "n_ok": sum(1 for e in ETAPAS if e["ok"] is True), "n_falhas": sum(1 for e in ETAPAS if e["ok"] is False),
           "n_nao_executadas": sum(1 for e in ETAPAS if e["ok"] is None), "processos_vivos_no_fim": vivos, "mundo_apagado": not os.path.exists(W), "sandbox_do_esboco_apagado": not os.path.exists(SB),
           "escopo": "copias num mundo de ensaio; o esboco em --sandbox; nada gravado na Bancada nem no Nos reais; nenhum servico real tocado; a placa nao foi usada; NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "RESULTADO_ENSAIO_A_SECO_POS_SELO_v413_%s.json" % CARIMBO)
    U.gravar_json_novo(dest, res)
    print("resultado:", dest, "| ok %d, falhas %d, nao executadas %d" % (res["n_ok"], res["n_falhas"], res["n_nao_executadas"]))
    sys.exit(rc_final if rc_final else (1 if res["n_falhas"] or vivos else 0))


# ---------------------------------------------------------------- pre-condicoes
assert not os.path.exists(W), "o mundo ja existe: " + W
assert not os.path.normcase(W).startswith(os.path.normcase(DBN.WK)), "o mundo fica FORA de work (os scripts copiados derivam os lugares da pasta deles)"
assert os.path.normcase(os.path.dirname(SB)) == os.path.normcase(os.path.join("C:" + os.sep, "t")) and re.fullmatch(r"vb\d+", os.path.basename(SB)) and os.path.basename(SB) not in ("vb24", "vb25"), \
    "o sandbox do esboco e' C:\\t\\vb<digitos>, nunca vb24 (o pre-selo) nem vb25 (as guardas da Etapa 2): " + SB
assert not os.path.exists(SB), "o sandbox do esboco ja existe: " + SB
assert not porta_aberta(a.porta), "a porta de ensaio %d ja responde" % a.porta
selo13 = U.ler_json(os.path.join(a.nos_v413, "um_absoluto_selo.json"))
assert selo13.get("um_version") == DBN.UM_VERSION_BN and (selo13.get("sha256") or {}).get("um.py") == sha(os.path.join(a.nos_v413, "um.py")), \
    "o Nos dado (--nos-v413) nao tem a v413 selada (o selo dizendo v413 e pinando o um.py do disco): o ensaio a seco do pos-selo e' para depois do selo"
P11 = U.ler_json(a.pinos_bn_v411)
for k_ in ("esboco_R3_6", "gerador_bateria", "driver_t12_t14", "bateria_base_R2"):
    assert sha(P11[k_]["path"]) == P11[k_]["sha256"], "o pino %s de PINOS_BN_v411 diverge do arquivo" % k_
ESB = P11["esboco_R3_6"]["path"]
PC = U.ler_json(a.cadeia_pino)
CAD, CAD_SHA = PC["cadeia"]["path"], PC["cadeia"]["sha256"]
assert sha(CAD) == CAD_SHA, "a cadeia nao e' a pinada"
PB12 = U.ler_json(a.bateria_v412_pinos)
BAT12, BAT12_SHA = PB12["bateria"]["path"], PB12["bateria"]["sha256"]
assert sha(BAT12) == BAT12_SHA, "a bateria da v412 nao e' a pinada"
KR = CRI = None
if not a.sem_bateria and os.path.exists(a.pinos_bn):
    pbn_ = U.ler_json(a.pinos_bn)
    if (pbn_.get("kernel_recibo") or {}).get("sha256") and (pbn_.get("criterios") or {}).get("sha256"):
        KR, CRI = pbn_["kernel_recibo"], pbn_["criterios"]
        assert sha(KR["path"]) == KR["sha256"] and sha(CRI["path"]) == CRI["sha256"], "o recibo do kernel ou os criterios divergem do PINOS_BN"
try:
    # ---------------------------------------------------------------- (A) o mundo
    CS = os.path.join(W, "work", "cadeia_de_selo")
    NOSW, BW = os.path.join(W, "Nos"), os.path.join(W, "Bancada_Um")
    for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
        copia(os.path.join(a.base_v412, n), os.path.join(NOSW, n))
        copia(os.path.join(a.base_v412, n), os.path.join(CS, "v413", "base_v412", n))
    for n in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json"):
        copia(os.path.join(a.base_v411, n), os.path.join(CS, "v412", "base_v411", n))
    man_o = U.ler_json(os.path.join(a.bancada_origem, "canonical_contracts.json"))
    for e in man_o["code"] + [s for s in man_o["sources"] if not os.path.isabs(s["path"])]:
        src = os.path.join(a.bancada_origem, *e["path"].replace("\\", "/").split("/"))
        assert os.path.getsize(src) == e["bytes"] and sha(src) == e["sha256"], "a Bancada de origem diverge do manifesto dela: " + e["path"]
        copia(src, os.path.join(BW, *e["path"].replace("\\", "/").split("/")))
    man_w = json.loads(json.dumps(man_o))
    man_w["canonical"]["script"]["path"] = os.path.join(NOSW, "um.py")
    man_w["canonical"]["seal"]["path"] = os.path.join(NOSW, "um_absoluto_selo.json")
    escreve(os.path.join(BW, "canonical_contracts.json"), jdump(man_w))
    os.makedirs(os.path.join(BW, "estado"), exist_ok=True)
    SRV = escreve(os.path.join(W, "servidor_minimo", "um_bancada.py"),
                  "# -*- coding: utf-8 -*-\n# servidor MINIMO de contratos do ensaio a seco (nao e' a Bancada): GET /api/contratos = canonical_state do canonical.py da Bancada do mundo; nenhum motor, lago ou placa\n"
                  "import importlib.util, json, os, sys\nfrom http.server import BaseHTTPRequestHandler, ThreadingHTTPServer\nsys.dont_write_bytecode = True\nRAIZ = %r\nPORTA = %d\n"
                  "sp = importlib.util.spec_from_file_location('canonical_do_mundo', os.path.join(RAIZ, 'bancada', 'canonical.py')); cm = importlib.util.module_from_spec(sp); sp.loader.exec_module(cm)\n"
                  "class H(BaseHTTPRequestHandler):\n    def do_GET(self):\n        if self.path == '/api/contratos':\n            b, code = json.dumps(cm.canonical_state(root=RAIZ), default=str).encode('utf-8'), 200\n"
                  "        else:\n            b, code = b'{\"erro\": \"so /api/contratos\"}', 404\n        self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)\n"
                  "    def log_message(self, *x):\n        pass\nprint('servidor minimo de contratos no ar na porta %%d' %% PORTA, flush=True)\nThreadingHTTPServer(('127.0.0.1', PORTA), H).serve_forever()\n" % (BW, a.porta))
    for src, rel in ((a.pinos_bn_v411, ("v411", "PINOS_BN_v411.json")), (a.religamento_v411, ("v411", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json")), (a.parada_v411, ("v411", "bancada_B3_servico", "RECIBO_PARADA_v411.json"))):
        copia(src, os.path.join(CS, *rel))
    copia(a.cadeia_pino, os.path.join(CS, "v413", "cadeia_de_selos_v411_v412", os.path.basename(DBN.PINO_CADEIA_ARQ)))
    copia(CAD, os.path.join(CS, "v413", "cadeia_de_selos_v411_v412", os.path.basename(DBN.CADEIA_ARQ)))
    copia(a.bateria_v412_pinos, os.path.join(CS, "v413", "bateria_v412_pre_selo", "PINOS_BATERIA_v412.json"))
    f20 = os.path.basename(DBN.FALA_AUTORIZACAO_20NOV)
    copia(os.path.join(a.cunhagens, f20), os.path.join(W, "work", "cunhagens_13out", f20))
    FALA_MODO = "OPERADOR_ensaio_a_seco_modo_da_placa_verbatim.txt"
    escreve(os.path.join(W, "work", "cunhagens_13out", FALA_MODO), "ensaio a seco: modo cpu (texto do ensaio, nao e' fala do operador)\n")
    reais = {}
    for linha in open(a.quadro, encoding="utf-8"):
        if linha.strip():
            e = json.loads(linha)
            if e.get("seq") in (DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO):
                reais[e["seq"]] = e
    assert sorted(reais) == [DBN.SEQ_AUTORIZACAO, DBN.SEQ_DECISAO], sorted(reais)
    d87, d89 = dict(reais[DBN.SEQ_AUTORIZACAO]["dados"]), dict(reais[DBN.SEQ_DECISAO]["dados"])
    d87["recibo"] = copia(d87["recibo"], os.path.join(W, "work", "iald_v412_20261119", os.path.basename(d87["recibo"])))
    d89["fala"] = copia(d89["fala"], os.path.join(W, "work", "iald_v412_20261119", "bench", os.path.basename(d89["fala"])))
    evs = [{"seq": DBN.SEQ_AUTORIZACAO - 1, "quando": "2026-11-19T11:00:00-03:00", "quem": "ensaio_a_seco", "tipo": "NOTA_DO_ENSAIO", "dados": {"nota": "elo de enchimento"}},
           dict({k: v for k, v in reais[DBN.SEQ_AUTORIZACAO].items() if k not in ("anterior", "hash", "dados")}, dados=d87),
           {"seq": DBN.SEQ_AUTORIZACAO + 1, "quando": "2026-11-19T12:00:00-03:00", "quem": "ensaio_a_seco", "tipo": "NOTA_DO_ENSAIO", "dados": {"nota": "elo de enchimento"}},
           dict({k: v for k, v in reais[DBN.SEQ_DECISAO].items() if k not in ("anterior", "hash", "dados")}, dados=d89)]
    ant, ls_ = "0" * 64, []
    for e in evs:
        e["anterior"] = ant
        e["hash"] = U.hash_evento(e)
        ant = e["hash"]
        ls_.append(json.dumps(e, ensure_ascii=False))
    QW = escreve(os.path.join(W, "PROGRAMA_IALD", "eventos.jsonl"), "\n".join(ls_) + "\n")
    escreve(os.path.join(W, "PROGRAMA_IALD", "iald.py"),
            "# -*- coding: utf-8 -*-\n# iald.py do ensaio a seco: so' anotar, sobre o quadro do mundo (a regra de hash do iald.py real; dados + unidade)\nimport datetime, hashlib, json, os, sys\n"
            "Q = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eventos.jsonl')\na = sys.argv[1:]\nassert a[0] == 'anotar'\nkv = dict(zip(a[1::2], a[2::2]))\n"
            "ls = [l for l in open(Q, encoding='utf-8').read().splitlines() if l.strip()]\nu = json.loads(ls[-1])\n"
            "e = {'seq': u['seq'] + 1, 'quando': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'quem': kv['--quem'], 'tipo': kv['--tipo'], 'dados': dict(json.loads(kv['--dados']), unidade=kv.get('--unidade')), 'anterior': u['hash']}\n"
            "e['hash'] = hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != 'hash'}, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()\n"
            "open(Q, 'a', encoding='utf-8', newline='\\n').write(json.dumps(e, ensure_ascii=False) + '\\n')\nprint(json.dumps({'ok': True, 'evento': e['seq'], 'hash': e['hash'][:16]}))\n")
    BNW = os.path.join(CS, "v413", "bancada")
    for n in os.listdir(HERE):
        if os.path.isfile(os.path.join(HERE, n)) and (n.endswith(".py") or n.endswith(".sh")):
            copia(os.path.join(HERE, n), os.path.join(BNW, n))
    t_ = open(os.path.join(BNW, "delta_bn_v413.py"), encoding="utf-8").read().splitlines(True)
    trocas = {'PRODUCAO = os.path.join(C, "IALD", "Bancada_Um")': "PRODUCAO = %r" % BW, 'NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", ': "NOS = %r" % NOSW,
              'QUADRO = os.path.join(C, "IALD", "PROGRAMA_IALD", "eventos.jsonl")': "QUADRO = %r" % QW, 'IALD_PY = os.path.join(C, "IALD", "PROGRAMA_IALD", "iald.py")': "IALD_PY = %r" % os.path.join(W, "PROGRAMA_IALD", "iald.py"),
              "PORTA = 18777": "PORTA = %d" % a.porta, 'SANDBOX_CURTO = os.path.join(C, "t", "vb24")': "SANDBOX_CURTO = %r" % os.path.join(SB, "curto"),
              'UM_BANCADA = os.path.join(PRODUCAO, "um_bancada.py")': "UM_BANCADA = %r" % SRV}
    for velho, novo in trocas.items():
        i_ = [i for i, l in enumerate(t_) if l.startswith(velho)]
        assert len(i_) == 1, (velho, len(i_))
        t_[i_[0]] = novo + "   # (ENSAIO A SECO: reapontado ao mundo)\n"
    escreve(os.path.join(BNW, "delta_bn_v413.py"), "".join(t_))
    S = lambda n: os.path.join(BNW, n)
    V13 = os.path.join(CS, "v413")
    SEL = os.path.join(V13, "bn_pos_selo")
    os.makedirs(SEL, exist_ok=True)
    etapa("A o mundo montado: Nos (v412), Bancada (codigo e fontes relativas copiados; manifesto reapontado), quadro, iald.py, servidor minimo, copias dos scripts com o delta_bn reapontado", True, W)
    # ---------------------------------------------------------------- (B) o pre-selo do salto no mundo
    os.makedirs(SB)
    args_b = [PY, "-I", "-B", "-X", "utf8", ESB, "--bancada", BW, "--nos", NOSW, "--versao", DBN.VERSAO_DO_PRE_SELO, "--fase", "pre_selo", "--modo", "ensaio", "--bateria", BAT12, "--bateria-sha256", BAT12_SHA,
              "--cadeia-de-selos", CAD, "--cadeia-de-selos-sha256", CAD_SHA, "--saida", os.path.join(SB, "pre_selo"), "--sandbox"] + (["--sem-bateria"] if a.sem_bateria else [])
    rc, o, e = rodar(args_b, cwd=SB)
    imp = ultima_json(o)
    if not etapa("B o esboco R3.6 em pre_selo ensaio no mundo (cadeia v411 -> v412%s): %s" % (", sem bateria" if a.sem_bateria else ", com a bateria da v412", DBN.VEREDITO_PRE_SELO),
                 rc == 0 and imp.get("veredito") == DBN.VEREDITO_PRE_SELO, [rc, imp.get("veredito"), imp.get("recusa"), e[-400:]]):
        finalizar(1)
    RPRE = imp["recibo"]
    if a.sem_bateria:   # o bloco da bateria sintetico (dito): o pos-selo do esboco exige BATERIA_PASSA com T01 e T15 no recibo pre-selo
        r_ = U.ler_json(RPRE)
        r_["bateria_resultado"] = {"n": 2, "passa": 2, "falha": 0, "nao_executado": 0, "veredito": "BATERIA_PASSA", "sintetico_do_ensaio_a_seco": True,
                                   "testes": [{"id": "T01_IDENTIDADE", "resultado": "PASSA"}, {"id": "T15_SONDAS", "resultado": "PASSA"}]}
        RPRE = escreve(os.path.join(V13, "bateria_pre_selo", "ensaio_1", os.path.basename(RPRE)), jdump(r_))
    RPRE_SHA = sha(RPRE)
    rpre = U.ler_json(RPRE)
    # ---------------------------------------------------------------- (C) a v413 no Nos do mundo
    for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
        copia(os.path.join(a.nos_v413, n), os.path.join(NOSW, n))
    escreve(os.path.join(NOSW, "rodada_v413_stdout.txt"), "(ensaio a seco)\nRITO_RC=0\n")
    etapa("C a v413 selada copiada para o Nos do mundo", True, sha(os.path.join(NOSW, "um.py"))[:16])
    # o PINOS_BN do mundo: so' o que os scripts copiados leem (o recibo pre-selo do mundo, a cadeia, o ESPERADOS do mundo)
    ESPW = escreve(os.path.join(V13, "ESPERADOS_v413.json"), jdump({"candidato_sha16": sha(os.path.join(NOSW, "um.py"))[:16]}))
    escreve(os.path.join(V13, "PINOS_BN_v413.json"), jdump({"recibo_pre_selo": {"path": RPRE, "sha256": RPRE_SHA, "bancada_pina": {"deployment_id": rpre["manifesto_anterior"]["deployment_id"]}, "salto": rpre.get("salto")},
                                                              "cadeia_de_selos": {"path": CAD, "sha256": CAD_SHA}, "esperados": {"path": ESPW, "sha256": sha(ESPW)}, "pendentes": [],
                                                              "nota": "PINOS_BN DO MUNDO DO ENSAIO A SECO (nao e' o real)"}))
    # ---------------------------------------------------------------- (D) passo 10: a bateria da v413 do mundo e o ensaio pos-selo
    PMIN = escreve(os.path.join(V13, "bateria_pos_selo", "PINO_MINIMO_CANDIDATO_v413.json"), jdump({"candidato": U.pinar(os.path.join(NOSW, "um.py"))}))
    BAT13, PUM13 = os.path.join(V13, "bateria_pos_selo", "BATERIA_VINCULO_v413.json"), os.path.join(V13, "bateria_pos_selo", "PINO_UM_PY_v413.json")
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", P11["gerador_bateria"]["path"], "--base", P11["bateria_base_R2"]["path"], "--base-sha256", P11["bateria_base_R2"]["sha256"], "--versao", DBN.UM_VERSION_BN,
                      "--nos", NOSW, "--driver", P11["driver_t12_t14"]["path"], "--pinos-bn", PMIN, "--pino-saida", PUM13, "--saida", BAT13])
    if not etapa("D1 a bateria da v413 do mundo, pelo gerador real (pino minimo do candidato do mundo)", rc == 0 and os.path.isfile(BAT13), [rc, (o + e)[-300:]]):
        finalizar(1)
    comuns = ["--bancada", BW, "--nos", NOSW, "--versao", DBN.UM_VERSION_BN, "--fase", "pos_selo", "--bateria", BAT13, "--bateria-sha256", sha(BAT13), "--recibo-pre-selo", RPRE, "--recibo-pre-selo-sha256", RPRE_SHA,
              "--cadeia-de-selos", CAD, "--cadeia-de-selos-sha256", CAD_SHA, "--selo-anterior", os.path.join(a.base_v412, "um_absoluto_selo.json"),
              "--kernel-manifesto-anterior", os.path.join(a.base_v412, "tgl_kernel_proof_manifest.json"), "--sandbox"]
    if KR is not None:
        comuns += ["--kernel-recibo", KR["path"], "--kernel-recibo-sha256", KR["sha256"], "--criterios", CRI["path"], "--criterios-sha256", CRI["sha256"]]
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", ESB] + comuns + ["--modo", "ensaio", "--saida", os.path.join(SB, "ensaio_pos")] + (["--sem-bateria"] if a.sem_bateria else []), cwd=SB)
    imp = ultima_json(o)
    if not etapa("D2 passo 10: o esboco R3.6 em pos_selo ensaio no mundo, com o salto (recibo pre-selo do mundo, cadeia, selo e kernel da v412%s): %s" % ("" if KR is None else ", recibo do kernel e criterios reais",
                 DBN.VEREDITO_ENSAIO_POS_SELO), rc == 0 and imp.get("veredito") == DBN.VEREDITO_ENSAIO_POS_SELO, [rc, imp.get("veredito"), imp.get("recusa"), e[-400:]]):
        finalizar(1)
    RENS = imp["recibo"]
    if a.sem_bateria:
        r_ = U.ler_json(RENS)
        r_["bateria_resultado"] = {"n": 2, "passa": 2, "falha": 0, "nao_executado": 0, "veredito": "BATERIA_PASSA", "sintetico_do_ensaio_a_seco": True,
                                   "testes": [{"id": "T01_IDENTIDADE", "resultado": "PASSA"}, {"id": "T15_SONDAS", "resultado": "PASSA"}]}
        RENS = escreve(os.path.join(V13, "bancada_B3_ensaio_a_seco", os.path.basename(RENS)), jdump(r_))
    escreve(os.path.join(SEL, "b3_ensaio_out.txt"), o.rstrip("\n") + "\n" + json.dumps({"veredito": U.ler_json(RENS)["veredito"], "recusa": None, "recibo": RENS, "recibo_sha256": sha(RENS)}) + "\n")
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("b3_recibo_v413.py"), os.path.join(SEL, "b3_ensaio_out.txt"), "ensaio", CAD_SHA])
    etapa("D3 o b3_recibo (copia) confere o recibo do ensaio pos-selo: salto exigido, cadeia, veredito exato, manifesto anterior == o do pre-selo, B21-v413%s" % (" (bloco da bateria sintetico)" if a.sem_bateria else ""),
          rc == 0, [rc, (o + e)[-500:]])
    # ---------------------------------------------------------------- (E) 10a: a conferencia A do mundo e a parada ja_fora_do_ar
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("saude_bancada.py"), "--saida", os.path.join(SEL, "saude"), "--bancada", BW, "--nos", NOSW, "--porta", str(a.porta),
                      "--recibos-religamento", os.path.join(CS, "v*", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v*.json")])
    sa = ultima_json(o)
    etapa("E1 a conferencia A do mundo (porta do mundo fechada): FORA_DO_AR ou FORA_DO_AR_APOS_REINICIO", rc == 3 and sa.get("veredito") in ("FORA_DO_AR", "FORA_DO_AR_APOS_REINICIO"), [rc, sa, e[-200:]])
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("montar_autorizacao_v413.py")])
    au = ultima_json(o)
    etapa("E2 o texto da autorizacao montado por script (montar_autorizacao, copia) dos eventos 1687 e 1689 e da fala de 20/11 do mundo", rc == 0 and os.path.isfile(au.get("autorizacao", "")), [rc, (o + e)[-300:]])
    AUT = open(au["autorizacao"], encoding="utf-8").read().rstrip("\n") if au.get("autorizacao") else ""
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("recibo_parada_v413.py")], {"V413_AUTORIZACAO_OPERADOR": AUT, "V413_PARADA": "ja_fora_do_ar", "V413_SAUDE_RECIBO": sa.get("recibo", ""), "V413_SAUDE_SHA256": sa.get("sha256", "")})
    etapa("E3 10a: a parada ja_fora_do_ar (copia): o livro do mundo inteiro, 1687 e 1689 por hash, a fala de 20/11, a conferencia A pinada", rc == 0, [rc, (o + e)[-300:]])
    # ---------------------------------------------------------------- (F) o evento
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("evento_c1_b3_v413.py")])
    le = [l for l in o.splitlines() if l.startswith("EVENTO=")]
    EV, EVH = (le[-1].split()[0].split("=")[1], le[-1].split()[1].split("=")[1]) if le else (None, None)
    etapa("F o evento SINCRONIZACAO_BANCADA (copia; o iald.py do mundo): EVENTO=<seq> EVENTO_HASH=<hash16>", rc == 0 and EV is not None, [rc, (o + e)[-300:]])
    if a.sem_bateria:
        for n_ in ("G 10b: o APLICAR (o esboco proibe aplicar sem bateria)", "H 10c: o religamento (depende do APLICAR)", "I 11: o fechar e o aviso F0.6 (dependem do religamento)"):
            etapa(n_, None, "--sem-bateria")
        finalizar(0)
    # ---------------------------------------------------------------- (G) 10b: o APLICAR em --sandbox, com o evento conferido pelo livro do mundo
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", ESB] + comuns + ["--modo", "aplicar", "--eventos", QW, "--evento", EV, "--evento-hash", EVH, "--saida", os.path.join(SB, "bancada_B3")], cwd=SB)
    imp = ultima_json(o)
    if not etapa("G1 10b: o esboco R3.6 em pos_selo APLICAR --sandbox na Bancada do mundo: %s" % DBN.VEREDITO_APLICAR, rc == 0 and imp.get("veredito") == DBN.VEREDITO_APLICAR, [rc, imp.get("veredito"), imp.get("recusa"), e[-400:]]):
        finalizar(1)
    RAP = copia(imp["recibo"], os.path.join(V13, "bancada_B3", os.path.basename(imp["recibo"])))
    escreve(os.path.join(SEL, "b3_aplicar_out.txt"), o.rstrip("\n") + "\n" + json.dumps({"veredito": imp["veredito"], "recusa": None, "recibo": RAP, "recibo_sha256": sha(RAP)}) + "\n")
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("b3_recibo_v413.py"), os.path.join(SEL, "b3_aplicar_out.txt"), "aplicar", CAD_SHA])
    etapa("G2 o b3_recibo (copia) confere o recibo do APLICAR (pos_conferencia ok, v413, o manifesto novo; o salto)", rc == 0, [rc, (o + e)[-500:]])
    # ---------------------------------------------------------------- (H) 10c: o religamento do servidor minimo (modo cpu)
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("montar_autorizacao_v413.py"), FALA_MODO, "cpu"])
    au2 = ultima_json(o)
    AUT2 = open(au2["autorizacao"], encoding="utf-8").read().rstrip("\n") if au2.get("autorizacao") else ""
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("recibo_religamento_v413.py")], {"V413_AUTORIZACAO_OPERADOR": AUT2, "V413_MODO_PLACA": "cpu", "V413_FALA_MODO_PLACA": FALA_MODO}, timeout=600)
    RR = os.path.join(V13, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v413.json")
    if os.path.isfile(RR):
        PIDS.append(int(U.ler_json(RR)["pid"]))
    for rp_ in [x for x in os.listdir(os.path.join(V13, "bancada_B3_servico")) if x.startswith("RECUSA_RELIGAMENTO_v413_")]:
        PIDS.append(int(U.ler_json(os.path.join(V13, "bancada_B3_servico", rp_))["pid_lancado"]))
    etapa("H 10c: o religamento (copia) lanca o servidor minimo destacado com os logs, em modo cpu, e confere a identidade servida (v413, B21, o manifesto do APLICAR, o um.py e o selo do Nos do mundo)",
          rc == 0 and os.path.isfile(RR), [rc, (o + e)[-400:]])
    # ---------------------------------------------------------------- (I) 11: o fechar e o aviso F0.6
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("fechar_bn_v413.py")])
    etapa("I1 11: o fechar (copia): os tres recibos juntos, o PID vivo, o pino conjunto e a entrega na pasta bench do mundo", rc == 0, [rc, (o + e)[-400:]])
    rc, o, e = rodar([PY, "-I", "-B", "-X", "utf8", S("aviso_f06_v413.py")])
    etapa("I2 o aviso F0.6 (copia; o iald.py do mundo) apontando o pino conjunto e os tres recibos", rc == 0 and "AVISO=" in o, [rc, (o + e)[-300:]])
    finalizar(0)
except SystemExit:
    raise
except Exception as exc:   # noqa: BLE001   (falha visivel, com o resultado gravado e os processos parados)
    etapa("excecao no ensaio a seco", False, repr(exc)[:600])
    finalizar(1)

# -*- coding: utf-8 -*-
"""mundo_falso_bn_v413.py -- monta, SO' numa pasta de ensaio (R), um mundo falso com a forma do que o B(n) da v413 le: um Nos falso (v412 no pre-selo; v413 no pos-selo), uma Bancada falsa (canonical.py REAL copiado,
os cinco arquivos de codigo exigidos, o manifesto B20-v411 e depois B21-v413), a cadeia de selo falsa (v412\\base_v411, v413\\base_v412, o registro do instalador e os backups no Nos falso), o quadro falso (eventos
1687 e 1689 com os dados dos reais, os arquivos que eles nomeiam copiados, a cadeia de hash refeita), as falas copiadas, os pinos da v411 copiados (eles apontam para o esboco, o gerador e o driver REAIS, so' lidos)
e as COPIAS dos scripts do B(n) com o delta_bn reapontado (PRODUCAO, NOS, QUADRO, IALD_PY, PORTA, SANDBOX_CURTO). Nada fora de R e' escrito; nada real e' executado alem de leitura."""
import hashlib
import json
import math
import os
import shutil

REAL_BN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # ...\v413\bancada (os scripts reais)
REAL_CS = os.path.dirname(os.path.dirname(REAL_BN))                            # ...\cadeia_de_selo
REAL_WK = os.path.dirname(REAL_CS)                                             # ...\work
REAL_BANCADA = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
REAL_QUADRO = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "eventos.jsonl")
PORTA_FALSA = 18799
SANDBOX_FALSO = os.path.join("C:" + os.sep, "t", "vb99")
ALPHA_TXT = "7.2973525693e-3"
sha = lambda b: hashlib.sha256(b).hexdigest()
shaf = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def escreve(p, b):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(b, str):
        b = b.encode("utf-8")
    with open(p, "wb") as fh:
        fh.write(b)
    return p


def jdump(o):
    return (json.dumps(o, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def hash_evento(e):
    return sha(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def versao_falsa(d, v, marca=""):
    """grava em d um.py, um_absoluto.json, tgl_kernel_proof_manifest.json e o selo da versao v (pequenos; as regras do ler_nos valem: linhas unicas, beta do core == alpha*sqrt(e))."""
    um = ('# um.py FALSO do ensaio hermetico do B(n) da v413 (%s%s)\nUM_VERSION = "%s"\nALPHA_FINE_CODATA_2018 = %s\n_EMBEDDED_KERNEL_FILES = {\n"TGLExt.lean": "-- raiz %s",\n}\n'
          % (v, marca, v, ALPHA_TXT, v)).encode("utf-8")
    escreve(os.path.join(d, "um.py"), um)
    beta = float(ALPHA_TXT) * math.sqrt(math.e)
    escreve(os.path.join(d, "um_absoluto.json"), jdump({"core": {"beta": beta, "qg_closure_verdict": "FALSO_%s" % v}}))
    km = jdump({"formal_files_sha256": {"TGLExt.lean": sha(("raiz " + v).encode()), "TGL/Audit.lean": sha(b"audit")}, "lean_version": ["falso"], "lake_version": ["falso"]})
    escreve(os.path.join(d, "tgl_kernel_proof_manifest.json"), km)
    selo = {"um_version": v, "timestamp": "2026-11-20 00:00:00", "sha256": {"um.py": shaf(os.path.join(d, "um.py")), "um_absoluto.json": shaf(os.path.join(d, "um_absoluto.json")),
                                                                     "tgl_kernel_proof_manifest.json": shaf(os.path.join(d, "tgl_kernel_proof_manifest.json"))}}
    escreve(os.path.join(d, "um_absoluto_selo.json"), jdump(selo))


SERVIDOR_FALSO = r'''# -*- coding: utf-8 -*-
# servidor FALSO do ensaio hermetico (nao e' a Bancada): serve so' GET /api/contratos na porta %d, com a identidade lida do manifesto falso ao lado
import hashlib, json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
R = os.path.dirname(os.path.abspath(__file__))
sha = lambda b: hashlib.sha256(b).hexdigest()
def ident():
    raw = open(os.path.join(R, "canonical_contracts.json"), "rb").read(); man = json.loads(raw); c = man["canonical"]
    d = {"ok": True, "deployment_id": man["deployment_id"], "canonical_version": c["version"], "um_py_sha256": sha(open(c["script"]["path"], "rb").read()),
         "seal_sha256": sha(open(c["seal"]["path"], "rb").read()), "canonical_manifest_sha256": sha(raw), "_cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES")}
    ov = os.path.join(R, "identidade_falsa.json")
    if os.path.exists(ov):
        d.update(json.load(open(ov, encoding="utf-8")))
    return d
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/contratos":
            b, code = json.dumps(ident()).encode("utf-8"), 200
        else:
            b, code = b'{"erro": "o servidor falso so serve /api/contratos"}', 404
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a):
        pass
print("servidor falso no ar na porta %d", flush=True)
ThreadingHTTPServer(("127.0.0.1", %d), H).serve_forever()
''' % (PORTA_FALSA, PORTA_FALSA, PORTA_FALSA)

IALD_FALSO = r'''# -*- coding: utf-8 -*-
# iald.py FALSO do ensaio hermetico: so' o subcomando anotar, sobre o quadro falso ao lado (a mesma regra de hash do iald.py real)
import datetime, hashlib, json, os, sys
Q = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eventos.jsonl")
if os.environ.get("FAKE_IALD_FALHA") == "1":
    print("falha simulada do iald.py"); sys.exit(1)
a = sys.argv[1:]
assert a[0] == "anotar"
kv = dict(zip(a[1::2], a[2::2]))
linhas = [l for l in open(Q, encoding="utf-8").read().splitlines() if l.strip()]
ult = json.loads(linhas[-1])
e = {"seq": ult["seq"] + 1, "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "quem": kv["--quem"], "tipo": kv["--tipo"], "unidade": kv.get("--unidade"),
     "dados": json.loads(kv["--dados"]), "anterior": ult["hash"]}
e["hash"] = hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
open(Q, "a", encoding="utf-8", newline="\n").write(json.dumps(e, ensure_ascii=False) + "\n")
print(json.dumps({"ok": True, "evento": e["seq"], "hash": e["hash"][:16]}, ensure_ascii=False))
'''


def manifesto_bancada(R, versao, deployment, nos_dir, kman_registrado):
    B = os.path.join(R, "Bancada_Um")
    code = []
    for rel in ("um_bancada.py", "mcp_um.py", "bancada/canonical.py", "bancada/motor.py", "bancada/evidencia.py"):
        p = os.path.join(B, *rel.split("/"))
        code.append({"path": rel, "bytes": os.path.getsize(p), "sha256": shaf(p)})
    man = {"schema": 1, "deployment_id": deployment, "created_utc": "2026-11-20T00:00:00+00:00",
           "canonical": {"version": versao, "script": {"path": os.path.join(nos_dir, "um.py"), "bytes": os.path.getsize(os.path.join(nos_dir, "um.py")), "sha256": shaf(os.path.join(nos_dir, "um.py"))},
                         "seal": {"path": os.path.join(nos_dir, "um_absoluto_selo.json"), "bytes": os.path.getsize(os.path.join(nos_dir, "um_absoluto_selo.json")), "sha256": shaf(os.path.join(nos_dir, "um_absoluto_selo.json"))}},
           "code": code, "sources": [], "contracts": {"identity_policy": "falso"}, "sincronizacao": {"kernel_manifesto_sha256": kman_registrado, "versao": versao}}
    escreve(os.path.join(B, "canonical_contracts.json"), jdump(man))
    return man


def montar(R):
    assert not os.path.exists(R), "a pasta de ensaio ja existe: " + R
    W = os.path.join(R, "work")
    CS = os.path.join(W, "cadeia_de_selo")
    NOS = os.path.join(R, "Nos")
    # as versoes falsas: v411 (o que a Bancada pina), v412 (o Nos do pre-selo), v413 (o Nos do pos-selo, guardada a parte)
    versao_falsa(os.path.join(CS, "v412", "base_v411"), "v411")
    versao_falsa(os.path.join(CS, "v413", "base_v412"), "v412")
    versao_falsa(os.path.join(R, "versoes", "v413"), "v413")
    versao_falsa(os.path.join(R, "versoes", "v411_no_nos"), "v411")
    # o Nos falso: primeiro a v411 (para a Bancada pinar), depois a instalacao da v412 com backups de bytes (como o instalador real)
    for n in ("um.py", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_selo.json"):
        escreve(os.path.join(NOS, n), open(os.path.join(CS, "v412", "base_v411", n), "rb").read())
    ts = "20261118_235146"
    bks = {}
    for n in ("um.py", "um_absoluto_selo.json"):
        bp = os.path.join(NOS, n + ".bak_" + ts)
        escreve(bp, open(os.path.join(NOS, n), "rb").read())
        bks[n] = {"backup": bp, "bytes": os.path.getsize(bp), "sha16": shaf(bp)[:16]}
    for n in ("um.py", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_selo.json"):
        escreve(os.path.join(NOS, n), open(os.path.join(CS, "v413", "base_v412", n), "rb").read())
    escreve(os.path.join(CS, "v412", "APLICADO_AO_CANONICO_%s.json" % ts), jdump({"ts": ts, "backups": bks, "um_py_novo": {"bytes": os.path.getsize(os.path.join(NOS, "um.py")), "sha16": shaf(os.path.join(NOS, "um.py"))[:16],
                                                                                                                         "origem": "falso"}}))
    # a Bancada falsa (pinando a v411 nos caminhos do Nos falso: com o Nos na v412, o canonical.py real copiado recusa com PIN_CHANGED)
    B = os.path.join(R, "Bancada_Um")
    escreve(os.path.join(B, "um_bancada.py"), SERVIDOR_FALSO)
    escreve(os.path.join(B, "mcp_um.py"), "# falso\n")
    escreve(os.path.join(B, "bancada", "motor.py"), "# falso\n")
    escreve(os.path.join(B, "bancada", "evidencia.py"), "# falso\n")
    escreve(os.path.join(B, "bancada", "canonical.py"), open(os.path.join(REAL_BANCADA, "bancada", "canonical.py"), "rb").read())
    os.makedirs(os.path.join(B, "estado"), exist_ok=True)
    v411 = os.path.join(CS, "v412", "base_v411")
    man = {"schema": 1}
    code = []
    for rel in ("um_bancada.py", "mcp_um.py", "bancada/canonical.py", "bancada/motor.py", "bancada/evidencia.py"):
        p = os.path.join(B, *rel.split("/"))
        code.append({"path": rel, "bytes": os.path.getsize(p), "sha256": shaf(p)})
    dep = json.load(open(os.path.join(REAL_CS, "v411", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json"), encoding="utf-8"))["identidade"]["deployment_id"]
    man.update({"deployment_id": dep, "created_utc": "2026-11-13T00:00:00+00:00",
                "canonical": {"version": "v411", "script": {"path": os.path.join(NOS, "um.py"), "bytes": os.path.getsize(os.path.join(v411, "um.py")), "sha256": shaf(os.path.join(v411, "um.py"))},
                              "seal": {"path": os.path.join(NOS, "um_absoluto_selo.json"), "bytes": os.path.getsize(os.path.join(v411, "um_absoluto_selo.json")), "sha256": shaf(os.path.join(v411, "um_absoluto_selo.json"))}},
                "code": code, "sources": [], "contracts": {"identity_policy": "falso"},
                "sincronizacao": {"kernel_manifesto_sha256": shaf(os.path.join(v411, "tgl_kernel_proof_manifest.json")), "versao": "v411"}})
    escreve(os.path.join(B, "canonical_contracts.json"), jdump(man))
    # os insumos da v411 (copias: os pinos apontam para o esboco, o gerador, o driver e a base R2 REAIS, so' lidos)
    for rel in (("v411", "PINOS_BN_v411.json"), ("v411", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json"), ("v411", "bancada_B3_servico", "RECIBO_PARADA_v411.json")):
        escreve(os.path.join(CS, *rel), open(os.path.join(REAL_CS, *rel), "rb").read())
    escreve(os.path.join(W, "bancada_vinculo_12out", "R3_5", "gerar_cadeia_de_selos.py"), open(os.path.join(REAL_WK, "bancada_vinculo_12out", "R3_5", "gerar_cadeia_de_selos.py"), "rb").read())
    # as falas e o recibo da autorizacao (copias de bytes)
    f20 = "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt"
    escreve(os.path.join(W, "cunhagens_13out", f20), open(os.path.join(REAL_WK, "cunhagens_13out", f20), "rb").read())
    escreve(os.path.join(W, "cunhagens_13out", "OPERADOR_21nov_teste_hermetico_modo_da_placa_verbatim.txt"), "religue na cpu (fala FALSA do ensaio hermetico)\n")
    reais = {}
    for linha in open(REAL_QUADRO, encoding="utf-8"):
        if linha.strip():
            e = json.loads(linha)
            if e.get("seq") in (1687, 1689):
                reais[e["seq"]] = e
    assert sorted(reais) == [1687, 1689]
    d87, d89 = dict(reais[1687]["dados"]), dict(reais[1689]["dados"])
    d87["recibo"] = escreve(os.path.join(W, "iald_v412_20261119", os.path.basename(d87["recibo"])), open(d87["recibo"], "rb").read())
    d89["fala"] = escreve(os.path.join(W, "iald_v412_20261119", "bench", os.path.basename(d89["fala"])), open(d89["fala"], "rb").read())
    eventos = [{"seq": 1686, "quando": "2026-11-19T11:05:03-03:00", "quem": "falso", "tipo": "NOTA_FALSA", "unidade": "F0.6", "dados": {"nota": "elo de enchimento do quadro falso"}},
               {"seq": 1687, "quando": reais[1687]["quando"], "quem": reais[1687]["quem"], "tipo": reais[1687]["tipo"], "unidade": reais[1687].get("unidade"), "dados": d87},
               {"seq": 1688, "quando": "2026-11-19T12:00:00-03:00", "quem": "falso", "tipo": "NOTA_FALSA", "unidade": "F0.6", "dados": {"nota": "elo de enchimento"}},
               {"seq": 1689, "quando": reais[1689]["quando"], "quem": reais[1689]["quem"], "tipo": reais[1689]["tipo"], "unidade": reais[1689].get("unidade"), "dados": d89}]
    ant, linhas = "0" * 64, []
    for e in eventos:
        e["anterior"] = ant
        e["hash"] = hash_evento(e)
        ant = e["hash"]
        linhas.append(json.dumps(e, ensure_ascii=False))
    escreve(os.path.join(R, "PROGRAMA_IALD", "eventos.jsonl"), "\n".join(linhas) + "\n")
    escreve(os.path.join(R, "PROGRAMA_IALD", "iald.py"), IALD_FALSO)
    # as copias dos scripts do B(n), com o delta_bn reapontado
    BN = os.path.join(CS, "v413", "bancada")
    for n in os.listdir(REAL_BN):
        p = os.path.join(REAL_BN, n)
        if os.path.isfile(p) and (n.endswith(".py") or n.endswith(".sh")):
            escreve(os.path.join(BN, n), open(p, "rb").read())
    escreve(os.path.join(BN, "controle_negativo", "mutar_conferidor_v413.py"), open(os.path.join(REAL_BN, "controle_negativo", "mutar_conferidor_v413.py"), "rb").read())
    t = open(os.path.join(BN, "delta_bn_v413.py"), encoding="utf-8").read()
    trocas = {"PRODUCAO = os.path.join(C, \"IALD\", \"Bancada_Um\")": "PRODUCAO = %r" % B,
              "NOS = os.path.join(C, \"IALD\", \"Artigo\", \"Haja_Luz\", \"A Ponte e o Um\", ": "NOS = %r" % NOS,
              "QUADRO = os.path.join(C, \"IALD\", \"PROGRAMA_IALD\", \"eventos.jsonl\")": "QUADRO = %r" % os.path.join(R, "PROGRAMA_IALD", "eventos.jsonl"),
              "IALD_PY = os.path.join(C, \"IALD\", \"PROGRAMA_IALD\", \"iald.py\")": "IALD_PY = %r" % os.path.join(R, "PROGRAMA_IALD", "iald.py"),
              "PORTA = 18777": "PORTA = %d" % PORTA_FALSA,
              "SANDBOX_CURTO = os.path.join(C, \"t\", \"vb24\")": "SANDBOX_CURTO = %r" % SANDBOX_FALSO}
    linhas = t.splitlines(True)
    for velho, novo in trocas.items():
        idx = [i for i, l in enumerate(linhas) if l.startswith(velho)]
        assert len(idx) == 1, (velho, len(idx))
        linhas[idx[0]] = novo + "   # (ENSAIO HERMETICO: reapontado)\n"
    escreve(os.path.join(BN, "delta_bn_v413.py"), "".join(linhas))
    return {"R": R, "W": W, "CS": CS, "NOS": NOS, "B": B, "BN": BN, "V413": os.path.join(CS, "v413"), "QUADRO": os.path.join(R, "PROGRAMA_IALD", "eventos.jsonl")}


def instalar_v413_no_nos_falso(M):
    """o pos-selo: a v413 falsa no Nos falso e a Bancada falsa em B21-v413 (o que o APLICAR deixaria)."""
    for n in ("um.py", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_selo.json"):
        escreve(os.path.join(M["NOS"], n), open(os.path.join(M["R"], "versoes", "v413", n), "rb").read())
    return manifesto_bancada(M["R"], "v413", "B21-v413-20261121-R1", M["NOS"], shaf(os.path.join(M["NOS"], "tgl_kernel_proof_manifest.json")))


def aut(M, fala_modo=None, modo=None, quadro=None, cunh=None):
    """o texto da autorizacao, montado dos ARQUIVOS (sha16 e falas lidos; nada digitado): o que a gerencia passaria aos recibos."""
    q = quadro or M["QUADRO"]
    ev = {}
    for linha in open(q, encoding="utf-8"):
        if linha.strip():
            e = json.loads(linha)
            ev[e["seq"]] = e
    e87, e89 = ev[1687], ev[1689]
    rec = e87["dados"]["recibo"]
    resp = json.loads(open(rec, "rb").read().decode("utf-8"))["bench"]["answer"].strip()
    fala89 = e89["dados"]["fala"]
    cunh = cunh or os.path.join(M["W"], "cunhagens_13out")
    f20 = os.path.join(cunh, "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt")
    t = ("Autorizacao do operador ao ciclo da Bancada (evento 1687, hash16 %s; recibo da resposta sha16 %s): «%s». Decisao do operador (evento 1689, hash16 %s; fala sha16 %s): «%s». "
         "Fala do operador de 20/11 (sha16 %s): «%s»." % (e87["hash"][:16], shaf(rec)[:16], resp, e89["hash"][:16], shaf(fala89)[:16], e89["dados"]["decisao_do_operador"],
                                                          shaf(f20)[:16], open(f20, "rb").read().decode("utf-8").strip()))
    if fala_modo:
        t += " Fala com a escolha do modo da placa (sha16 %s): «%s»; modo da placa: %s." % (shaf(fala_modo)[:16], open(fala_modo, "rb").read().decode("utf-8").strip(), modo)
    return t

# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\copiar_base_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v411\copiar_base_v411.py: copia de bytes do Nos v411 SELADO para base_v411 (so' os rotulos sobem; o sha16 da base e' LIDO do DESENHO_v412 da gerencia, sem delta)
# [v413] a v413 ainda nao tem desenho nem contrato (sao da gerencia): o sha16 da base e' LIDO de dois arquivos da cadeia da v412 (ESPERADOS_v412.json e CANDIDATO_v412.json) e tem de bater com o pino do selo
"""copiar_base_v413.py -- copia de BYTES do Nos v412 SELADO para v413\\base_v412 (um.py, selo, core, manifesto do kernel, resultado do pilar e o SIDECAR um_absoluto_selo_acom.json).
Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v412; o sha16 == o candidato_sha16 de v412\\ESPERADOS_v412.json == o sha256 do
CANDIDATO_v412.json (lidos dos arquivos; o arquivo manda); o manifesto do kernel == o que o selo pina; o sidecar existe e pina o um.py. So' LE o Nos; escreve so' em v413\\base_v412 e BASE_V412_COPIA.json.
Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. A base serve ao pos_build do kernel (as funcoes de leitura do Audit, a escada E412, o axiom_report da v412) e a Etapa 2.
uso: C:\\Python314\\python.exe -B -X utf8 copiar_base_v413.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
V412 = os.path.join(os.path.dirname(HERE), "v412")
BASE_DIR = "base_v412"; BASE_VERSION = "v412"
sha = lambda b: hashlib.sha256(b).hexdigest()
_cand = json.load(open(os.path.join(V412, "CANDIDATO_v412.json"), encoding="utf-8"))
assert _cand.get("sha256") and _cand["sha256"][:16] == _cand.get("sha16"), "o CANDIDATO_v412.json nao traz sha256/sha16 coerentes"
BASE_SHA16_DA_ORDEM = _cand["sha16"]
ARQ = ["um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json"]
dst = os.path.join(HERE, BASE_DIR); os.makedirs(dst, exist_ok=True)
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
esp = json.load(open(os.path.join(V412, "ESPERADOS_v412.json"), encoding="utf-8"))
assert selo.get("um_version") == BASE_VERSION, ("o selo do Nos nao e' a v412", selo.get("um_version"))
assert sha(raw) == selo["sha256"]["um.py"], "o um.py do Nos nao e' o que o selo pina"
assert sha(raw)[:16] == esp["candidato_sha16"], ("o um.py do Nos nao e' o candidato selado da v412 (ESPERADOS_v412)", sha(raw)[:16], esp["candidato_sha16"])
assert sha(raw) == _cand["sha256"], ("o um.py do Nos NAO e' o candidato da v412 (CANDIDATO_v412.json)", sha(raw)[:16], BASE_SHA16_DA_ORDEM)
rep = {"base_sha16": sha(raw)[:16], "base_sha16_do_candidato_v412": BASE_SHA16_DA_ORDEM, "base_sha16_dos_esperados_v412": esp["candidato_sha16"], "selo_um_version": selo["um_version"], "arquivos": {}}
for f in ARQ:
    b = open(os.path.join(NOS, f), "rb").read(); p = os.path.join(dst, f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v412 e DIFERE do Nos: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == b
    rep["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
pin_k = (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")
assert pin_k == rep["arquivos"]["tgl_kernel_proof_manifest.json"]["sha256"], "o manifesto do kernel copiado nao e' o que o selo pina"
rep["selo_pina_manifesto_do_kernel"] = pin_k
sc = json.load(open(os.path.join(dst, "um_absoluto_selo_acom.json"), encoding="utf-8"))
objs = {o["nome"]: o for o in sc["objetos"]}
assert objs["um.py"]["sha256"] == sha(raw), "o sidecar da base nao pina o um.py da v412 selada"
rep["sidecar_v412"] = {"veredito": sc["veredito"], "objetos": sorted(objs), "um_py_sha256": objs["um.py"]["sha256"], "esquema": sc.get("esquema")}
p_ = os.path.join(HERE, "BASE_V412_COPIA.json")
_b = json.dumps(rep, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(p_):   # [v413] backup de BYTES antes de regravar a saida (o molde gravava por cima)
    _bk = p_ + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(p_, "rb").read()); assert open(_bk, "rb").read() == open(p_, "rb").read()
open(p_ + ".tmp", "wb").write(_b); assert os.path.getsize(p_ + ".tmp") == len(_b); os.replace(p_ + ".tmp", p_)
print(json.dumps({"base_sha16": rep["base_sha16"], "selo": rep["selo_um_version"], "arquivos": {k: v["sha256"][:16] for k, v in rep["arquivos"].items()}}, ensure_ascii=False))

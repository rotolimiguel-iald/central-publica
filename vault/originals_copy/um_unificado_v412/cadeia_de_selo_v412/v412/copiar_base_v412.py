# -*- coding: utf-8 -*-
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v411\copiar_base_v411.py: copia de bytes do Nos v411 SELADO para base_v411 (so' os rotulos sobem; o sha16 da base e' LIDO do DESENHO_v412 da gerencia, sem delta)
"""copiar_base_v412.py -- copia de BYTES do Nos v411 SELADO para v412\\base_v411 (um.py, selo, core, manifesto do kernel, resultado do pilar e o SIDECAR um_absoluto_selo_acom.json).
Conferencias por script (nada digitado): o sha256 do um.py == o que o SELO pina; o selo diz v411; o sha16 == o candidato_sha16 de v411\\ESPERADOS_v411.json == o que o DESENHO_v412 da gerencia
deu (lido do arquivo; o arquivo manda); o manifesto do kernel == o que o selo pina; o sidecar existe e pina o um.py. So' LE o Nos; escreve so' em v412\\base_v411 e BASE_V411_COPIA.json.
Reexecutavel: o que ja existe e e' igual fica; o que difere aborta. A base serve ao pos_build do kernel (as funcoes de leitura do Audit, a escada E411, o axiom_report da v411) e a Etapa 2.
uso: C:\\Python314\\python.exe -B -X utf8 copiar_base_v412.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
V411 = os.path.join(os.path.dirname(HERE), "v411")
BASE_DIR = "base_v411"; BASE_VERSION = "v411"
sha = lambda b: hashlib.sha256(b).hexdigest()
_des = open(os.path.join(HERE, "DESENHO_v412.md"), "rb").read().decode("utf-8")
_m = re.search(r"Base: a v411 selada \(`um\.py` do N[oó]s, sha16 `([0-9a-f]{16})`", _des)
assert _m, "o DESENHO_v412 nao traz a base"
BASE_SHA16_DA_ORDEM = _m.group(1)
ARQ = ["um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json"]
dst = os.path.join(HERE, BASE_DIR); os.makedirs(dst, exist_ok=True)
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
esp = json.load(open(os.path.join(V411, "ESPERADOS_v411.json"), encoding="utf-8"))
assert selo.get("um_version") == BASE_VERSION, ("o selo do Nos nao e' a v411", selo.get("um_version"))
assert sha(raw) == selo["sha256"]["um.py"], "o um.py do Nos nao e' o que o selo pina"
assert sha(raw)[:16] == esp["candidato_sha16"], ("o um.py do Nos nao e' o candidato selado da v411 (ESPERADOS_v411)", sha(raw)[:16], esp["candidato_sha16"])
assert sha(raw)[:16] == BASE_SHA16_DA_ORDEM, ("o um.py do Nos NAO e' o que o DESENHO_v412 deu", sha(raw)[:16], BASE_SHA16_DA_ORDEM)
rep = {"base_sha16": sha(raw)[:16], "base_sha16_do_desenho": BASE_SHA16_DA_ORDEM, "selo_um_version": selo["um_version"], "arquivos": {}}
for f in ARQ:
    b = open(os.path.join(NOS, f), "rb").read(); p = os.path.join(dst, f)
    if os.path.exists(p):
        assert open(p, "rb").read() == b, ("o arquivo ja existe em base_v411 e DIFERE do Nos: nao sobrescrevo", f)
    else:
        open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    assert open(p, "rb").read() == b
    rep["arquivos"][f] = {"bytes": len(b), "sha256": sha(b)}
pin_k = (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")
assert pin_k == rep["arquivos"]["tgl_kernel_proof_manifest.json"]["sha256"], "o manifesto do kernel copiado nao e' o que o selo pina"
rep["selo_pina_manifesto_do_kernel"] = pin_k
sc = json.load(open(os.path.join(dst, "um_absoluto_selo_acom.json"), encoding="utf-8"))
objs = {o["nome"]: o for o in sc["objetos"]}
assert objs["um.py"]["sha256"] == sha(raw), "o sidecar da base nao pina o um.py da v411 selada"
rep["sidecar_v411"] = {"veredito": sc["veredito"], "objetos": sorted(objs), "um_py_sha256": objs["um.py"]["sha256"], "esquema": sc.get("esquema")}
p_ = os.path.join(HERE, "BASE_V411_COPIA.json")
open(p_ + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(p_ + ".tmp", p_)
print(json.dumps({"base_sha16": rep["base_sha16"], "selo": rep["selo_um_version"], "arquivos": {k: v["sha256"][:16] for k, v in rep["arquivos"].items()}}, ensure_ascii=False))

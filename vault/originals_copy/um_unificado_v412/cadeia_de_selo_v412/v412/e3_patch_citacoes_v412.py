# -*- coding: utf-8 -*-
"""e3_patch_citacoes_v412.py -- adapta conferir_citacoes_v412.py (backup .bak_antes_do_patch_e3): (1) a normalizacao (_norm, _limpa) e a lista de rotulos da v410 saem do ARQUIVO da v410 (onde estao definidas) e os da v411 do ROTULOS_V411 do arquivo da v411
(o corpo da v411 as tomava da v410; a subida de rotulo as pedia da v411 e quebrava); a v412 NAO acrescenta rotulo (nenhuma citacao entre aspas angulares nos textos novos: o metodo e' sem fala); (2) o escopo do um.py da v412 = os textos que a v412 escreve;
(3) zero arquivo ou zero citacao examinados no escopo do um.py e' dito no JSON (n_arquivos_examinados) e a ausencia de citacao nao verbatim exige ao menos um arquivo examinado. Script da cadeia; nada daqui entra no programa."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_citacoes_v412.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
if s.count("[A ADAPTAR v412] SUBIDA") == 0:
    print("ja' adaptado"); sys.exit(0)
bak = P + ".bak_antes_do_patch_e3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:90], s.count(old))
    s = s.replace(old, new)


i = s.index("# [A ADAPTAR v412] SUBIDA"); j = s.index("\n", i)
s = s[:i] + "# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] a v412 nao tem fala: nenhuma citacao entre aspas angulares nos textos novos; os rotulos herdados vem da v410 (_ROTULOS) e da v411 (ROTULOS_V411), lidos dos ARQUIVOS; escopo do um.py = os textos que a v412 escreve; arquivo examinado e' contado" + s[j:]
# (1) o bloco da normalizacao e dos rotulos
a = s.index('_SRC411 = open(os.path.join(DL.V411, "conferir_citacoes_v411.py")')
b0 = '_ROTULOS = {x_.lower() for x_ in _ROT411[0]} | {x_.lower() for x_ in ROTULOS_V412}'
b = s.index(b0) + len(b0)
novo = '''_AST = __import__("ast")
_SRC410 = open(os.path.join(DL.V410, "conferir_citacoes_v410.py"), encoding="utf-8").read(); _TR410 = _AST.parse(_SRC410)
_NS410 = {"re": re}
for _n410 in _TR410.body:   # (a normalizacao e a limpeza, onde estao DEFINIDAS: o arquivo da v410, LIDAS por AST, nao redigitadas)
    if isinstance(_n410, _AST.Assign) and getattr(_n410.targets[0], "id", None) in ("_norm", "_limpa"):
        exec(compile(_AST.get_source_segment(_SRC410, _n410), "<conferir_citacoes_v410>", "exec"), _NS410)
_norm, _limpa = _NS410["_norm"], _NS410["_limpa"]
_ROT410 = [_AST.literal_eval(_n410.value) for _n410 in _TR410.body if isinstance(_n410, _AST.Assign) and getattr(_n410.targets[0], "id", None) == "_ROTULOS" and isinstance(_n410.value, _AST.Set)]
assert len(_ROT410) == 1 and len(_ROT410[0]) > 100, "a lista _ROTULOS da v410 nao foi lida"
_SRC411 = open(os.path.join(DL.V411, "conferir_citacoes_v411.py"), encoding="utf-8").read(); _TR411 = _AST.parse(_SRC411)
_ROT411 = [_AST.literal_eval(_n411.value) for _n411 in _TR411.body if isinstance(_n411, _AST.Assign) and getattr(_n411.targets[0], "id", None) == "ROTULOS_V411" and isinstance(_n411.value, _AST.Dict)]
assert len(_ROT411) == 1 and len(_ROT411[0]) >= 6, "o ROTULOS_V411 da v411 nao foi lido"
ROTULOS_V412 = {}   # a v412 nao acrescenta rotulo: nenhum texto novo cita entre aspas angulares (o programa nao traz fala)
_ROTULOS = {x_.lower() for x_ in _ROT410[0]} | {x_.lower() for x_ in _ROT411[0]} | {x_.lower() for x_ in ROTULOS_V412}'''
s = s[:a] + novo + s[b:]
# (2) o escopo do um.py da v412
troca('ARQS = ["delta_v412.py", "registros_h0dn_v412.py", "registros_v412.py", "runtime_h0dn_v412.py", "quadro_v412.py", "gerar_candidato_v412.py"]',
      'ARQS = ["delta_v412.py", "registros_v412.py", "textos_registros_v412.py", "runtime_v412_guarda.py", "gerar_candidato_v412.py", "TEXTO_PUBLICO_v412.json", "TOPO_RATIFICADO_v412_DERIVADO.json"]')
troca('if os.path.exists(DL.TOPO_RATIFICADO_ARQ):\n    ARQS.append(os.path.basename(DL.TOPO_RATIFICADO_ARQ))\n', '')
# (3) o que foi examinado e' dito; nenhum arquivo examinado = falha
troca('out["n_rotulos"] = {"v411": len(_ROT411[0]), "v412": len(ROTULOS_V412)}', 'out["n_rotulos"] = {"v410": len(_ROT410[0]), "v411": len(_ROT411[0]), "v412": len(ROTULOS_V412)}\nout["n_arquivos_examinados_no_um_py"] = len(out["arquivos"]); out["n_citacoes_examinadas_no_um_py"] = sum(v_["n_citacoes"] for v_ in out["arquivos"].values())')
troca('out["ok_do_um_py"] = not out["nao_verbatim_do_um_py"]', 'out["ok_do_um_py"] = bool(not out["nao_verbatim_do_um_py"] and out["n_arquivos_examinados_no_um_py"] > 0)   # (zero arquivo examinado nao e\' passagem)')
tmp = P + ".tmp"
open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > 5000
os.replace(tmp, P)
print("conferir_citacoes_v412.py adaptado:", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16])

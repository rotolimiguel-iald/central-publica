# -*- coding: utf-8 -*-
"""e3_patch_exame4_v412.py -- quarta adaptacao do exame_pontos_v412.py (contrato R4; backup .bak_r1b): a chave nova do core, guarda_frases_v412 (o resultado da travessia: por registro, unidades examinadas e violacoes), nao e' registro e nao traz all_verified;
no quadro `nao_verdes` ela fica verde quando ha UM resultado por registro novo, com unidades examinadas > 0 e zero violacao (vermelha caso contrario: nunca omitida). Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exame_pontos_v412.py")
s = open(P, "rb").read().decode("utf-8")
if 'k == "guarda_frases_v412"' in s:
    print("ja'"); sys.exit(0)
open(P + ".bak_r1b", "wb").write(s.encode("utf-8"))
old = 'for k in R["chaves_novas_no_core"] + ["kh_n1_cobertura_v392"]:\n    v = core.get(k) or {}\n'
assert s.count(old) == 1
new = old + '''    if k == "guarda_frases_v412":   # (v412, R4) o resultado da travessia da guarda de frases: um resultado por registro novo, unidades examinadas > 0, zero violacao
        _gv = v; v = {"all_verified": bool(len(_gv) == len(DL.REGISTROS_SPEC_V412) and set(_gv) == set(DL.REGISTROS_SPEC_V412) and all(isinstance(x_, dict) and x_.get("n_violacoes") == 0 and isinstance(x_.get("n_unidades_examinadas"), int) and x_["n_unidades_examinadas"] > 0 for x_ in _gv.values())),
                      "verdict": "TRAVESSIA_DA_GUARDA_DE_FRASES_V412 " + json.dumps({n_: [x_.get("n_unidades_examinadas"), x_.get("n_violacoes")] for n_, x_ in _gv.items()}, ensure_ascii=False)}
'''
s = s.replace(old, new)
open(P, "wb").write(s.encode("utf-8"))
print("exame_pontos_v412.py (4) adaptado")

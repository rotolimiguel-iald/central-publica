# -*- coding: utf-8 -*-
"""e3_patch_exame3_v412.py -- terceira adaptacao do exame_pontos_v412.py (contrato R4; backup .bak_r1): o ponto de chamada real dos quatro registros tambem confere o resultado da travessia da guarda de frases que o proprio _v412_rodar_specs grava no core
(guarda_frases_v412[nome]: unidades examinadas > 0, zero violacao). Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exame_pontos_v412.py")
s = open(P, "rb").read().decode("utf-8")
if "guarda_n_unidades" in s:
    print("ja'"); sys.exit(0)
open(P + ".bak_r1", "wb").write(s.encode("utf-8"))


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:90], s.count(old))
    s = s.replace(old, new)


troca('"kernel": _r12.get("kernel"), "does_not_gate_core": _r12.get("does_not_gate_core")}',
      '"kernel": _r12.get("kernel"), "does_not_gate_core": _r12.get("does_not_gate_core"), "guarda_n_unidades": ((core.get("guarda_frases_v412") or {}).get(_n12) or {}).get("n_unidades_examinadas"), "guarda_n_violacoes": ((core.get("guarda_frases_v412") or {}).get(_n12) or {}).get("n_violacoes")}')
troca('or v_["n_checks"] <= 0 or v_["checks_falhos"] or v_["does_not_gate_core"] is not True for v_ in pv12_["registros"].values())): falsos.append("ponto_specs_v412")',
      'or v_["n_checks"] <= 0 or v_["checks_falhos"] or v_["does_not_gate_core"] is not True or not isinstance(v_["guarda_n_unidades"], int) or v_["guarda_n_unidades"] <= 0 or v_["guarda_n_violacoes"] != 0 for v_ in pv12_["registros"].values())): falsos.append("ponto_specs_v412")')
open(P, "wb").write(s.encode("utf-8"))
print("exame_pontos_v412.py (3) adaptado")

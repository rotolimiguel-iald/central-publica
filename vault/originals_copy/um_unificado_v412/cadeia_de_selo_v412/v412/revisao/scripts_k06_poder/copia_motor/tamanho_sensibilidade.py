# -*- coding: utf-8 -*-
"""Revisao K06 / pergunta 4: o 0,057 do nulo global e ruido ou violacao de tamanho?

Usa a COPIA do motor do Kimi (r32_motor.py, hash conferido igual ao original), sem alterar uma linha dele.
Cenario: NULO_GLOBAL_ISO_FRONTEIRA (D=-0,15 contra ISO-A/B), alfa 0,05, n=320.
 (1) mesma especificacao, sementes NOVAS (declaradas antes: 20261114), 3000 corridas -> resolve o 0,057.
 (2) mesma especificacao com efeito de texto maior (0,20 e 0,40), 1000 corridas -> o teste por sinais com
     27 blocos trata como independentes blocos que partilham o mesmo texto (9 blocos por texto).
Extensao da reproducao pedida (um cenario); declarada como tal no relatorio.
"""
import dataclasses
import json
import sys
from pathlib import Path

from scipy.stats import beta

import r32_motor as M

OUT = Path(__file__).with_name("tamanho_sensibilidade.json")
base = next(s for s in M.SCENARIOS if s.sid == "NULO_GLOBAL_ISO_FRONTEIRA")


def cp(x, n, conf=0.95):
    a = (1 - conf) / 2
    lo = 0.0 if x == 0 else beta.ppf(a, x, n - x + 1)
    hi = 1.0 if x == n else beta.ppf(1 - a, x + 1, n - x)
    return lo, hi


runs = [("ref_texto_010_semente_nova", 0.10, 3000, 20261114),
        ("texto_020", 0.20, 1000, 20261115),
        ("texto_040", 0.40, 1000, 20261116)]
res = {}
for nome, text_sd, nsim, seed in runs:
    spec = dataclasses.replace(base, sid=nome, text_sd=text_sd)
    row = M.run_scenario(spec, nsim, seed)
    r = row["rates"]
    x = round(r["raw_any_primary_rejection"] * nsim)
    lo, hi = cp(x, nsim)
    res[nome] = {"text_sd": text_sd, "nsim": nsim, "seed": seed, "size_any6": r["raw_any_primary_rejection"],
                 "x": x, "cp95": [lo, hi], "boundary_max_dev": row["boundary_diagnostics"]["max_absolute_deviation"],
                 "integrity": r["integrity_ok"], "falsified": r["falsified"]}
    print(nome, json.dumps(res[nome]), flush=True)
OUT.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("WROTE", OUT)

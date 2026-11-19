# -*- coding: utf-8 -*-
"""Revisao K06: em que SENTIDO o motor testa o braco ISO?

Narrativa do protocolo: o isomorfo deve convergir tao bem quanto o focal (ISO nao inferior a T);
se so o nome importa, o isomorfo fica pior e a previsao estrutural falha (REV0 11; ORDEM K06 G).
No codigo (r32_motor.analyze): ISO usa `plus_upper` de 20*(Q_T - Q_ISO) + 3*tamanho, isto e,
H0: Q_T - Q_ISO <= -0,15 -> estabelece que T NAO e inferior ao ISO. A direcao FALSIFIED dos ISO usa `plus_lower`
(ISO muito MELHOR que T). Nada olha ISO muito PIOR que T.

Cenarios (copia do motor, sem alterar nada; ICC 0; nsim 300; semente 20261117, declarada antes):
  ISO_IGUAL        : T 0,909 ; ISO 0,909 ; PLA/OUT 0,66   (o caso do BASE)
  ISO_PIOR_25PTS   : T 0,909 ; ISO 0,66  ; PLA/OUT 0,66   (so o nome carrega a convergencia)
  ISO_MELHOR_25PTS : T 0,66  ; ISO 0,909 ; PLA/OUT 0,66
"""
import dataclasses
import json
from pathlib import Path

import r32_motor as M

OUT = Path(__file__).with_name("sentido_do_teste_iso.json")
base = M.Scenario("X")
cenarios = [
    ("ISO_IGUAL", dataclasses.replace(base, sid="ISO_IGUAL")),
    ("ISO_PIOR_25PTS", dataclasses.replace(base, sid="ISO_PIOR_25PTS", iso_level=60)),
    ("ISO_MELHOR_25PTS", dataclasses.replace(base, sid="ISO_MELHOR_25PTS", focal_level=60, control_level=60, iso_level=90)),
]
res = {}
for nome, spec in cenarios:
    row = M.run_scenario(spec, 300, 20261117)
    r = row["rates"]
    res[nome] = {"Q_por_braco": [round(x, 3) for x in row["observed_synthetic_means"]["Q_by_arm"]],
                 "integridade": r["integrity_ok"], "POWERED": r["powered"], "FALSIFIED": r["falsified"],
                 "NONSPECIFIC": r["nonspecific_powered"], "UNDER": r["underpowered"], "INCONCLUSIVE": r["inconclusive_controls"],
                 "raw_all_primary_ISO6": r["raw_all_primary"], "directional_falsified": r["directional_falsified"]}
    print(nome, json.dumps(res[nome]), flush=True)
OUT.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("WROTE", OUT)

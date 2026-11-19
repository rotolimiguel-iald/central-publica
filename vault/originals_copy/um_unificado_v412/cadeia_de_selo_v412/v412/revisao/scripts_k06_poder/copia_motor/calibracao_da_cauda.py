# -*- coding: utf-8 -*-
"""Revisao K06 / pergunta 6: o p exato por sinais e calibrado nas caudas fundas?

O teste por sinais de 27 clusters e exato SO se a diferenca por cluster for simetrica em torno do deslocamento
sob H0; na fronteira (Q_T=0,60 contra Q_ISO=0,75, sessoes independentes) a diferenca binaria e assimetrica.
Medida: P(p <= a) sob a fronteira para a em {0,05, 0,01, 0,001, 0,0001}, n=655 (27 clusters de ~24 sessoes),
com a funcao exact_fft_pvalues da COPIA do motor (inalterada). Semente 20261118 (declarada antes).
Extensao curta e declarada; nao toca o 5 sigma (precisaria ~10^7 corridas).
"""
import json
from pathlib import Path

import numpy as np

import r32_motor as M

OUT = Path(__file__).with_name("calibracao_da_cauda.json")
rng = np.random.default_rng(20261118)
n = 655
cluster, starts, sizes = M.cluster_layout(n)
NSIM = 30000
BATCH = 500
ps = []
for first in range(0, NSIM, BATCH):
    b = min(BATCH, NSIM - first)
    qt = rng.random((b, 4, n)) < 0.60
    qi = rng.random((b, 4, n)) < 0.75
    d = (qt.astype(np.int16) - qi.astype(np.int16))                                  # (b,4,n)
    dsum = np.add.reduceat(d, starts, axis=2)                                         # (b,4,27)
    totals = 20 * dsum + 3 * sizes[None, None, :]
    up, lo = M.exact_fft_pvalues(totals.astype(np.int16))
    ps.append(up.reshape(-1))
p = np.concatenate(ps)
res = {"n": n, "p_values": int(p.size), "fronteira": "Q_T=0,60 ; Q_ISO=0,75 ; D=-0,15 ; sessoes independentes",
       "taxas": {}}
for a in (0.05, 0.01, 0.001, 0.0001):
    k = int((p <= a).sum())
    res["taxas"][str(a)] = {"eventos": k, "taxa": k / p.size, "razao_ao_nominal": (k / p.size) / a}
    print(f"alpha={a:g}: eventos={k} taxa={k/p.size:.6f} razao={k/p.size/a:.3f}", flush=True)
res["menor_p"] = float(p.min())
OUT.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("WROTE", OUT)

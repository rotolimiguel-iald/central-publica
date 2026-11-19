# -*- coding: utf-8 -*-
"""Revisao K06: o FFT do Kimi bate com a DP exata tambem com 27 clusters e magnitudes reais?
(o validar_r32.py do Kimi so compara em G=3). Usa a copia do motor; semente fixa 20261114."""
import json
from pathlib import Path

import numpy as np

import r32_motor as M

rng = np.random.default_rng(20261114)
n = 320
cluster, starts, sizes = M.cluster_layout(n)
max_err = 0.0
min_p_seen = 1.0
casos = []
for caso in range(6):
    # diferenca de Q por cluster entre focal e um controle: binarios com taxas 0,91 e 0,91 (ou 0,91 e 0,66)
    q0 = rng.random((1, n)) < 0.91
    q1 = rng.random((1, n)) < (0.91 if caso % 2 == 0 else 0.66)
    d = np.add.reduceat((q0.astype(np.int16) - q1.astype(np.int16)), starts, axis=1)  # (1, 27)
    d4 = np.repeat(d[:, None, :], 4, axis=1).astype(np.int16)                           # (1,4,27)
    for nome, tot in (("raw", d4), ("+3", 20 * d4 + 3 * sizes[None, None, :]), ("-3", 20 * d4 - 3 * sizes[None, None, :])):
        up_f, lo_f = M.exact_fft_pvalues(tot)
        up_d, lo_d = M.exact_dp_reference(tot)
        err = float(max(np.max(np.abs(up_f - up_d)), np.max(np.abs(lo_f - lo_d))))
        rel = float(np.max(np.abs(up_f - up_d) / np.maximum(up_d, 1e-300)))
        max_err = max(max_err, err)
        min_p_seen = min(min_p_seen, float(up_f.min()))
        casos.append({"caso": caso, "shift": nome, "err_abs_max": err, "err_rel_max": rel, "p_up": float(up_f[0, 0]), "p_up_dp": float(up_d[0, 0])})
print(json.dumps(casos, indent=1))
print("ERRO ABSOLUTO MAXIMO FFT x DP (27 clusters):", max_err, "| menor p visto:", min_p_seen)
Path(__file__).with_name("validar_27_clusters.json").write_text(json.dumps({"max_err": max_err, "min_p_seen": min_p_seen, "casos": casos}, indent=1) + "\n", encoding="utf-8")

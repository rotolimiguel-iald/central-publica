#!/usr/bin/env python3
"""Revisor K05 (GH-III1), ponto 8: sanidade numerica (dimensao finita) do Lema II-infty-1 do Kimi:
   R_M(a) = P a P, P projecao espectral de D (comuta com D), D_M = P D P.
   Confere: (i) [D_M, R_M a] = P [D,a] P ; (ii) ||R_M a|| <= ||a|| e L_M(R_M a) <= L(a), L(a)=||[D,a]|| ;
            (iii) R_M positivo e unital (R_M(1)=P) ;  (iv) P a P - a = P a (P-1) + (P-1) a.
   Nao e prova (a prova e a identidade algebrica); e' so conferencia de que as formulas do documento nao tem erro de sinal."""
import numpy as np
rng = np.random.default_rng(20261114)
N = 14
worst = {"comut": 0.0, "norm_ok": True, "lip_ok": True, "pos_ok": True, "ident_iv": 0.0}
for trial in range(200):
    d = np.sort(rng.normal(size=N) * 3)
    D = np.diag(d)
    R = rng.uniform(0.5, 4)
    keep = np.abs(d) <= R
    if keep.sum() == 0 or keep.all():
        continue
    P = np.diag(keep.astype(float))
    a = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    Ra = P @ a @ P
    DM = P @ D @ P
    comm = DM @ Ra - Ra @ DM
    rhs = P @ (D @ a - a @ D) @ P
    worst["comut"] = max(worst["comut"], np.linalg.norm(comm - rhs))
    n = lambda x: np.linalg.norm(x, 2)
    worst["norm_ok"] &= n(Ra) <= n(a) + 1e-9
    worst["lip_ok"] &= n(comm) <= n(D @ a - a @ D) + 1e-9
    b = a @ a.conj().T  # positivo
    worst["pos_ok"] &= np.min(np.linalg.eigvalsh(P @ b @ P)) >= -1e-9
    worst["ident_iv"] = max(worst["ident_iv"], np.linalg.norm((P @ a @ P - a) - (P @ a @ (P - np.eye(N)) + (P - np.eye(N)) @ a)))
unit = np.allclose(P @ np.eye(N) @ P, P)
worst["unital_R(1)=P"] = bool(unit)
print(worst)

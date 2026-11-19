#!/usr/bin/env python3
"""Revisor K02, ponto 5: confere por calculo explicito (matrizes gama euclidianas em dimensao n=1..8) a tabela de
sinais KO (eps, eps', eps'') que o Kimi usa, contra a carga conjugada J = U K do operador de Dirac D = -i gamma^mu d_mu.
Condicoes:  J D = eps' D J  <=>  U conj(gamma^mu) U^-1 = -eps' gamma^mu ;  J^2 = eps  <=>  U conj(U) = eps*1 ;
            J chi = eps'' chi J (n par) <=> U conj(chi) U^-1 = eps'' chi,  chi = i^(n/2) gamma^1...gamma^n.
Lista todas as triplas realizaveis por n (as 'doze possibilidades' de Dabrowski-Dossena, tabela 1) e marca a selecao de Connes."""
import itertools, json
import numpy as np

s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)

def gammas(n):
    m = n // 2
    if n % 2 == 0:
        gs = []
        for k in range(m):
            for s in (s1, s2):
                M = np.array([[1]], complex)
                for j in range(m):
                    M = np.kron(M, s3 if j < k else (s if j == k else I2))
                gs.append(M)
        return gs
    g = gammas(n - 1)
    if len(g) == 0:
        chi = np.array([[1]], complex)
    else:
        chi = (1j) ** m * (np.linalg.multi_dot(g) if len(g) > 1 else g[0])
    # para n impar: n-1 gamas + (+-) chi_{n-1}; duas representacoes inequivalentes
    return g, chi

def conj_solutions(gs, s):
    """U com U conj(g_mu) = s g_mu U para todo mu (U 'vec' row-major)."""
    d = gs[0].shape[0]
    rows = []
    for g in gs:
        # U conj(g) - s g U = 0  ->  (I (x) conj(g)^T - s g (x) I) vec(U) = 0  (row-major vec)
        rows.append(np.kron(np.eye(d), g.conj().T) - s * np.kron(g, np.eye(d)))
    A = np.vstack(rows)
    u, sv, vh = np.linalg.svd(A)
    r = int(np.sum(sv > 1e-9))
    ns = vh[r:].conj()
    return [x.reshape(d, d) for x in ns]

def analyse(n):
    res = set()
    if n % 2 == 0:
        reps = [gammas(n)]
    else:
        g, chi = gammas(n)
        reps = [g + [chi], g + [-chi]]
    for gs in reps:
        d = gs[0].shape[0]
        chi_op = None
        if n % 2 == 0:
            chi_op = (1j) ** (n // 2) * (np.linalg.multi_dot(gs) if len(gs) > 1 else gs[0])
        for s in (+1, -1):                      # s = -eps'
            for U in conj_solutions(gs, s):
                if np.linalg.norm(U) < 1e-12: continue
                U = U / np.sqrt(np.trace(U @ U.conj().T).real / d)
                if np.linalg.norm(U @ U.conj().T - np.eye(d)) > 1e-8: continue
                P = U @ U.conj()
                eps = P[0, 0].real
                if np.linalg.norm(P - eps * np.eye(d)) > 1e-8: continue
                eps_p = -s
                if chi_op is not None:
                    T = U @ chi_op.conj() @ np.linalg.inv(U)
                    e2 = None
                    for cand in (1, -1):
                        if np.linalg.norm(T - cand * chi_op) < 1e-8: e2 = cand
                    res.add((int(round(eps)), eps_p, e2))
                else:
                    res.add((int(round(eps)), eps_p, None))
    return sorted(res, key=lambda t: (t[0], t[1], 0 if t[2] is None else t[2]))

kimi = {0: (1, 1, 1), 1: (1, -1, None), 2: (-1, 1, -1), 3: (-1, 1, None), 4: (-1, 1, 1), 5: (-1, -1, None),
        6: (1, 1, -1), 7: (1, 1, None)}
out = {}
for n in range(1, 9):
    r = analyse(n)
    k = kimi[n % 8]
    out[n] = {"triplas_realizaveis(eps,eps',eps'')": r, "tabela_Kimi(n mod 8)": k, "Kimi_realizavel": tuple(k) in [tuple(x) for x in r]}
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))

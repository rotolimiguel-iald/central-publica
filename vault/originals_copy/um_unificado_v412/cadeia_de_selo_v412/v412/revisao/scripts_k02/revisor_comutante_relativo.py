#!/usr/bin/env python3
"""Revisor K02, ponto 4 (T1): sanidade numerica FINITA do passo (ii)-(iv) da gerencia.
Analogo finito do produto cruzado: G grupo abeliano finito agindo em M = M_n(C) por alpha_g = Ad(u_g).
Realiza M x| G como pontos fixos de (Ad rho_g (x) alpha_g) em B(l2(G)) (x) M  (Digernes-Takesaki) e mede
  dim( lambda(G)' ∩ (M x| G) )   versus   |G| * dim(M^alpha)   (= dim de <M^alpha, lambda(G)>).
Se M^alpha = C1 (acao ergodica), lambda(G)'' deve ser maximal abeliana (dim |G|).
Nada de dado observado."""
import itertools, json
import numpy as np

def pauli():
    I = np.eye(2, dtype=complex); X = np.array([[0, 1], [1, 0]], complex)
    Z = np.array([[1, 0], [0, -1]], complex); return I, X, Z

def regular_reps(elems, mul, inv):
    idx = {g: i for i, g in enumerate(elems)}
    N = len(elems)
    lam = {}; rho = {}
    for g in elems:
        L = np.zeros((N, N), complex); R = np.zeros((N, N), complex)
        for h in elems:
            L[idx[mul(g, h)], idx[h]] = 1      # (lambda_g f)(.) : delta_h -> delta_{gh}
            R[idx[mul(h, inv(g))], idx[h]] = 1  # rho_g : delta_h -> delta_{h g^{-1}}  (right regular)
        lam[g] = L; rho[g] = R
    return lam, rho

def nullspace_dim(A, tol=1e-9):
    s = np.linalg.svd(A, compute_uv=False)
    return int(A.shape[1] - np.sum(s > tol * max(1.0, s.max())))

def nullspace(A, tol=1e-9):
    u, s, vh = np.linalg.svd(A)
    r = int(np.sum(s > tol * max(1.0, s.max())))
    return vh[r:].conj().T

def run(label, elems, mul, inv, ug, n):
    N = len(elems)
    lam, rho = regular_reps(elems, mul, inv)
    D = N * n                                   # dimension of l2(G) (x) C^n
    # espaco de operadores D x D (vec por linhas)
    def ad_op(U):                               # X -> U X U^*  como matriz D^2 x D^2 (vec row-major)
        return np.kron(U, U.conj())
    Id = np.eye(D * D, dtype=complex)
    rows = []
    for g in elems:
        U = np.kron(rho[g], ug[g])              # (Ad rho_g (x) Ad u_g) = Ad(rho_g (x) u_g)
        rows.append(ad_op(U) - Id)
    Fix = nullspace(np.vstack(rows))            # base dos pontos fixos = M x| G (dimensao esperada |G|*dim M)
    dim_cp = Fix.shape[1]
    # lambda(G) (x) 1 esta em Fix?
    in_fix = all(np.linalg.norm(np.vstack(rows) @ np.kron(lam[g], np.eye(n)).reshape(-1)) < 1e-9 for g in elems)
    # comutante relativo de lambda(G)(x)1 dentro de Fix
    cons = []
    for g in elems:
        Lg = np.kron(lam[g], np.eye(n))
        cons.append(np.kron(Lg, np.eye(D)) - np.kron(np.eye(D), Lg.T))   # [Lg, X] = 0 em vec row-major
    C = np.vstack(cons) @ Fix
    dim_rel = nullspace_dim(C)
    # centralizador M^alpha
    rowsM = [np.kron(ug[g], ug[g].conj()) - np.eye(n * n) for g in elems]
    dim_Malpha = nullspace_dim(np.vstack(rowsM))
    return {"caso": label, "|G|": N, "n": n, "dim_produto_cruzado": dim_cp, "esperado_|G|*n^2": N * n * n,
            "lambda(G)_em_Fix": bool(in_fix), "dim_M^alpha": dim_Malpha,
            "dim_comutante_relativo_de_lambda(G)": dim_rel, "esperado_|G|*dim(M^alpha)": N * dim_Malpha,
            "lambda(G)''_e_masa": bool(dim_rel == N)}

I, X, Z = pauli()
out = []
# caso nao ergodico: G = Z2 agindo por Ad(Z) em M_2  (M^alpha = diagonal, dim 2)
e1 = [0, 1]; out.append(run("Z2 por Ad(Z) em M_2 (nao ergodico)", e1, lambda a, b: (a + b) % 2, lambda a: a,
                             {0: I, 1: Z}, 2))
# caso ergodico: G = Z2 x Z2 agindo por Ad(X^a Z^b) em M_2 (M^alpha = C1)
e2 = list(itertools.product([0, 1], repeat=2))
ug2 = {(a, b): np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b) for a, b in e2}
out.append(run("Z2xZ2 por Ad(Weyl) em M_2 (ergodico)", e2, lambda g, h: ((g[0] + h[0]) % 2, (g[1] + h[1]) % 2),
               lambda g: g, ug2, 2))
# caso ergodico n=3: G = Z3 x Z3, Weyl 3x3
w = np.exp(2j * np.pi / 3)
S = np.roll(np.eye(3), 1, axis=0).astype(complex); T = np.diag([1, w, w * w])
e3 = list(itertools.product(range(3), repeat=2))
ug3 = {(a, b): np.linalg.matrix_power(S, a) @ np.linalg.matrix_power(T, b) for a, b in e3}
out.append(run("Z3xZ3 por Ad(Weyl) em M_3 (ergodico)", e3,
               lambda g, h: ((g[0] + h[0]) % 3, (g[1] + h[1]) % 3), lambda g: ((-g[0]) % 3, (-g[1]) % 3), ug3, 3))
print(json.dumps(out, indent=2, ensure_ascii=False))

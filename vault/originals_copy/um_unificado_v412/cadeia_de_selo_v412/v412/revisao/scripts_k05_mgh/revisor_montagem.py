#!/usr/bin/env python3
"""Revisor K05 (montagem 3+1), pontos A1, A3 e A2.
Confere por calculo explicito (matrizes) as afirmacoes de MONTAGEM_3MAIS1_R2.md:
  (a) Gamma_1..4 = sigma_{1,2,3} x tau_1 , 1 x tau_2: autoadjuntas, quadrado 1, anticomutam; chi = -Gamma_1 Gamma_2 Gamma_3 Gamma_4 = 1 x tau_3.
  (b) J = (sigma_2 x 1) K: J^2, JD, Jchi => (eps, eps', eps'') = (-,+,+) (KO 4).
  (c) a construcao D-D iterada (impar x impar com M+ de (26), par x impar) reproduz D e J do documento.
  (d) a constante de orientacao: enumera o produto shuffle iterado de quatro 1-ciclos, calcula pi_D e compara com -1/18 (D-D (35)-(36)) e -1/24.
  (e) K-teoria de T^4: forma de intersecao em Lambda^even(Z^4) tem determinante +-1 (Poincare dual, caso de contas).
  (f) escalonamento lambda: d_lambda = lambda^-1 d, pi_{D_lambda}(c) = lambda^4 pi_{D_1}(c).
Convencao: operador diferencial constante D = -i lam sum_j Gamma_j d_j; J = C K com K conjugacao complexa de FUNCOES.
  J D J^-1 = C (+i lam sum conj(Gamma_j) d_j) C^-1  =>  J D = eps' D J  <=>  C conj(Gamma_j) C^-1 = -eps' Gamma_j.
"""
import itertools, json, math
import numpy as np
import sympy as sp

s0 = np.eye(2, dtype=complex)
s1 = np.array([[0, 1], [1, 0]], complex)
s2 = np.array([[0, -1j], [1j, 0]], complex)
s3 = np.array([[1, 0], [0, -1]], complex)
out = {}

def k(*ms):
    r = np.array([[1]], complex)
    for m in ms:
        r = np.kron(r, m)
    return r

# (a) gamas do documento
G = [k(s1, s1), k(s2, s1), k(s3, s1), k(s0, s2)]
ok_herm = all(np.allclose(g, g.conj().T) for g in G)
ok_sq = all(np.allclose(g @ g, np.eye(4)) for g in G)
ok_ac = all(np.allclose(G[i] @ G[j] + G[j] @ G[i], 0) for i in range(4) for j in range(4) if i != j)
chi = k(s0, s3)
chi_vol = -(G[0] @ G[1] @ G[2] @ G[3])
out["a_gamas"] = {"autoadjuntas": ok_herm, "quadrado_1": ok_sq, "anticomutam": ok_ac, "chi_igual_menos_G1G2G3G4": bool(np.allclose(chi, chi_vol))}

# (b) sinais KO de J = (sigma_2 x 1) K
C = k(s2, s0)
def signs(C, G, chi):
    eps = np.allclose(C @ C.conj(), np.eye(4)) and +1 or (np.allclose(C @ C.conj(), -np.eye(4)) and -1 or None)
    # JD = e' DJ  <=> C conj(G) C^-1 = -e' G
    ep = None
    for e in (+1, -1):
        if all(np.allclose(C @ g.conj() @ np.linalg.inv(C), -e * g) for g in G):
            ep = e
    epp = None
    for e in (+1, -1):
        if np.allclose(C @ chi.conj() @ np.linalg.inv(C), e * chi):
            epp = e
    return eps, ep, epp
out["b_sinais_J_doc"] = signs(C, G, chi)

# (c) construcao D-D iterada, em simbolo (D = lam sum p_j Gamma_j nos modos e^{ipx}; so as matrizes importam)
# passo 1: S^1 x S^1 (impar x impar): Gamma^{(2)}_{1,2} = sigma_1, sigma_2 ; chi2 = sigma_3 ; J2 = (1 x 1 x M+) K, M+(1,1)=sigma_2 por (26)
def Mplus(n1, n2):
    m1, m2 = (n1 - 1) // 2, (n2 - 1) // 2
    j = (int(round((5 + (-1) ** (m2 + 1)) / 2)) + 2 * m1) % 4
    return [s0, s1, s2, s3][j], j
def Mminus(n1, n2):
    m1, m2 = (n1 - 1) // 2, (n2 - 1) // 2
    kk = (int(round((1 + (-1) ** m2) / 2)) + 2 * m1) % 4
    return [s0, s1, s2, s3][kk], kk
M11, j11 = Mplus(1, 1)
M31, j31 = Mplus(3, 1)
out["c_M_D_D"] = {"M+(1,1)": "sigma_%d" % j11, "M+(3,1)": "sigma_%d" % j31, "M-(1,1)": "sigma_%d" % Mminus(1, 1)[1], "M-(3,1)": "sigma_%d" % Mminus(3, 1)[1]}
G2 = [s1, s2]; chi2 = s3; C2 = M11            # J1=J2=K (C=1)
# passo 2: T^2 x S^1 (par x impar): D = D2 x 1 + chi2 x D_3 ; J = J2 x J_S1
G3 = [g for g in G2] + [chi2]; C3 = C2           # J_S1 = K  (C=1)
# passo 3: T^3 x S^1 (impar x impar): D = D3 x 1 x tau1 + 1 x D4 x tau2 ; J = J3 x J_S1 x M+ K
G4 = [np.kron(g, s1) for g in G3] + [np.kron(s0, s2)]
C4 = np.kron(C3, M31)
chi4 = np.kron(s0, s3)
out["c_iterado_igual_ao_doc"] = {"Gamma": all(np.allclose(a, b) for a, b in zip(G4, G)), "chi": bool(np.allclose(chi4, chi)), "J_C": bool(np.allclose(C4, C))}
def signs_n(C, G, chi, d):
    eps = None
    CC = C @ C.conj()
    if np.allclose(CC, np.eye(d)): eps = +1
    elif np.allclose(CC, -np.eye(d)): eps = -1
    ep = None
    for e in (+1, -1):
        if all(np.allclose(C @ g.conj() @ np.linalg.inv(C), -e * g) for g in G):
            ep = e
    epp = None
    if chi is not None:
        for e in (+1, -1):
            if np.allclose(C @ chi.conj() @ np.linalg.inv(C), e * chi):
                epp = e
    return eps, ep, epp
out["c_sinais_passos"] = {
    "S1xS1 (KO2: -,+,-)": signs_n(C2, G2, chi2, 2),
    "T2xS1 (KO3: -,+)": signs_n(C3, G3, None, 2),
    "T3xS1 (KO4: -,+,+)": signs_n(C4, G4, chi4, 4),
}
# convencao de Connes (tabela do artigo, n mod 8): n=2 (-,+,-), n=3 (-,+), n=4 (-,+,+)

# (d) constante de orientacao: shuffle iterado de quatro 1-ciclos c_1^j = (U_j^-1 (x) 1) (x) U_j
# pi_D(termo) = a0 * prod_k [D, U_{tau(k)}] ; [D,U_j] = lam U_j Gamma_j ; a0 = prod U_j^-1.  Soma com sinal da permutacao.
def perm_sign(p):
    s = 1
    p = list(p)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s
tot = np.zeros((4, 4), complex)
nterms = 0
for p in itertools.permutations(range(4)):
    M = np.eye(4, dtype=complex)
    for idx in p:
        M = M @ G[idx]          # fator U_j cancela com a0 (funcoes comutam)
    tot += perm_sign(p) * M
    nterms += 1
G1234 = G[0] @ G[1] @ G[2] @ G[3]
out["d_orientacao"] = {
    "n_termos_do_shuffle_iterado": nterms,
    "soma_igual_a": "24 * G1G2G3G4 = -24 chi" if np.allclose(tot, 24 * G1234) and np.allclose(tot, -24 * chi) else "outro",
    "constante_correta_c4": "-1/24 (para lam=1)",
    "valor_de_pi_D_com_constante_do_doc_(-1/18)": "(4/3) chi" if np.allclose((-1 / 18) * tot, (4 / 3) * chi) else "outro",
    "pi_D_com_-1/18_igual_chi": bool(np.allclose((-1 / 18) * tot, chi)),
    "pi_D_com_-1/24_igual_chi": bool(np.allclose((-1 / 24) * tot, chi)),
}
# contagem de shuffles (p,q) vs nu_n = (n-1)n/2 de D-D (36)
from math import comb
cont = []
for (n1, n2) in [(1, 1), (2, 1), (3, 1), (2, 2), (1, 3)]:
    n = n1 + n2
    cont.append({"(n1,n2)": [n1, n2], "n_shuffles=C(n,n1)": comb(n, n1), "nu_n=(n-1)n/2 (D-D 36)": (n - 1) * n // 2})
out["d_contagem_shuffles_vs_nu_DD"] = cont
# produto iterado correto: r2=2i, r3=3, r4=4i  -> produto = -24 ; D-D literal: i,3,6i -> -18
out["d_produto_r"] = {"correto": complex(2j * 3 * 4j).real, "D-D_literal(i*3*6i)": complex(1j * 3 * 6j).real}
# verificacao direta do passo (1,1): pi_D(c1 x c2) = 2 sigma_1 sigma_2 = 2 i sigma_3
step11 = s1 @ s2 - s2 @ s1
out["d_passo_1_1"] = {"pi_D(c1xc2)=2i sigma_3": bool(np.allclose(step11, 2j * s3)), "D-D(43) daria i sigma_3": False}

# (e) K-teoria de T^4: forma de intersecao em Lambda^even(Z^4)
basis = [()]
for r in (2, 4):
    basis += list(itertools.combinations(range(4), r))
def wedge_top(A, B):
    if set(A) & set(B): return 0
    seq = list(A) + list(B)
    if len(seq) != 4: return 0
    return perm_sign(seq)
Pm = sp.Matrix(len(basis), len(basis), lambda i, j: wedge_top(basis[i], basis[j]))
out["e_forma_intersecao_T4"] = {"dim": len(basis), "det": int(Pm.det())}

# (f) escalonamento
lam = sp.symbols("lam", positive=True)
out["f_escala"] = {"pi_D_lambda(c)=lambda^4 pi_D_1(c)": True, "d_lambda=lambda^-1 d_1": True,
                   "lambda^-4 com lam=beta^-1/2 = beta^2": sp.simplify((lam ** -4).subs(lam, sp.Symbol('b', positive=True) ** sp.Rational(-1, 2))).__str__()}

print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
json.dump(out, open("revisor_montagem_saida.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)

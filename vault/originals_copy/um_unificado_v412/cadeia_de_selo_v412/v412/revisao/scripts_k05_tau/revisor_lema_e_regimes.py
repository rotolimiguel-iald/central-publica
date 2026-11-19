# Revisor K05/tau (tarefas 5, 6, 7): lema dimensional (sistema linear), N=E_P/u com digitos, derivacao de Gamma ~ omega^3
# no monopolo, cruzamento max/soma/quadratura. Independente do script do Kimi. Nenhum dado observado.
import math, json
from fractions import Fraction
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec = 50

# --- (5) lema dimensional: dimensoes (M, L, T) -------------------------------------------------
dim = {"hbar": (1, 2, -1), "c": (0, 1, -1), "G": (-1, 3, -2)}
def solve3(rows, rhs):
    # eliminacao de Gauss exata em Fractions (sistema 3x3 ou nx3)
    n = len(rows[0])
    A = [[Fraction(x) for x in r] + [Fraction(b)] for r, b in zip(rows, rhs)]
    m = len(A)
    piv = 0
    pivcols = []
    for col in range(n):
        p = next((i for i in range(piv, m) if A[i][col] != 0), None)
        if p is None: continue
        A[piv], A[p] = A[p], A[piv]
        A[piv] = [x / A[piv][col] for x in A[piv]]
        for i in range(m):
            if i != piv and A[i][col] != 0:
                f = A[i][col]
                A[i] = [a - f * b for a, b in zip(A[i], A[piv])]
        pivcols.append(col); piv += 1
    incons = any(all(A[i][j] == 0 for j in range(n)) and A[i][n] != 0 for i in range(m))
    return incons, A, pivcols
# hbar^a c^b tem dimensao de tempo (0,0,1)?  linhas: M, L, T
rows = [[dim["hbar"][k], dim["c"][k]] for k in range(3)]
inc, A, pc = solve3(rows, [0, 0, 1])
print("hbar^a c^b = tempo: inconsistente?", inc)
rows = [[dim["hbar"][k], dim["G"][k], dim["c"][k]] for k in range(3)]
inc, A, pc = solve3(rows, [0, 0, 1])
print("hbar^a G^b c^d = tempo: inconsistente?", inc, "solucao", [str(A[i][3]) for i in range(3)], "(a,b,d)")
# determinante != 0 => unica
det = (Fraction(rows[0][0]) * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
       - Fraction(rows[0][1]) * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
       + Fraction(rows[0][2]) * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0]))
print("det da matriz (hbar,G,c) =", det, "(!=0 => expoentes unicos)")
# com u (energia = M L^2 T^-2) e hbar: hbar/u e tempo; u^a hbar^b c^d ... outra ancora
dimE = (1, 2, -2)
rows = [[dimE[k], dim["hbar"][k]] for k in range(3)]
inc, A, pc = solve3(rows, [0, 0, 1])
print("u^a hbar^b = tempo:", "inconsistente" if inc else "solucao", [str(A[i][2]) for i in range(2)] if not inc else None)

# --- (5b) N = E_P/u com digitos ------------------------------------------------------------
D = Decimal
h = D("6.62607015e-34"); pi = D("3.14159265358979323846264338327950288419716939937510582097494")
hbar = h / (2 * pi); c = D("299792458"); G = D("6.67430e-11"); eV = D("1.602176634e-19")
EP = (hbar * c**5 / G).sqrt()
N = EP / eV
print("N = E_P/(1 eV) =", f"{N:.12e}")
print("G reconstruido de N =", f"{(hbar * c**5 / (N * eV) ** 2):.10e}")
tP = (hbar * G / c**5).sqrt()
print("t_P =", f"{tP:.12e}", " hbar/E_P =", f"{(hbar / EP):.12e}")

# --- (6) Gamma monopolo com E = hbar*omega:  Gamma = (2 pi beta G hbar / c^5) omega^3 -------------
import math as m
beta = 7.2973525693e-3 * m.sqrt(m.e)
hb = 6.62607015e-34 / (2 * m.pi); cc = 299792458.0; GG = 6.67430e-11
omega_sr = 2696919089607130.0  # lido do core (P1.platforms[sr87_kim2025].omega_rad_s)
for w in (omega_sr, 2 * omega_sr, 1.0):
    tau = 4 * m.pi * GG * (hb * w) / cc**5
    g1 = 0.5 * beta * tau * w * w
    g2 = (2 * m.pi * beta * GG * hb / cc**5) * w**3
    print(f"omega={w:.4e}: Gamma(tau_mon(E=hbar w))={g1:.6e}  forma cubica={g2:.6e}  rel={(g1-g2)/g2:.2e}  razao Gamma(2w)/Gamma(w)={'' if w!=omega_sr else ''}")
tau2 = lambda w: 4 * m.pi * GG * (hb * w) / cc**5
print("Gamma(2w)/Gamma(w) monopolo E=hbar w:", (0.5*beta*tau2(2*omega_sr)*(2*omega_sr)**2) / (0.5*beta*tau2(omega_sr)*omega_sr**2), "(=8 => omega^3)")
# se E fosse a energia de repouso (fixa), a lei ficaria omega^2: razao 4
E_rest = 87 * 1.66053906660e-27 * cc**2
tauE = 4 * m.pi * GG * E_rest / cc**5
print("Gamma(2w)/Gamma(w) com E fixo (repouso):", (0.5*beta*tauE*(2*omega_sr)**2) / (0.5*beta*tauE*omega_sr**2), "(=4 => omega^2)")
# energia de cruzamento tau_hor = t_P
EP_f = m.sqrt(hb * cc**5 / GG)
print("E de cruzamento tau_hor=t_P:  E_P/(4 pi) =", EP_f / (4 * m.pi), "J =", EP_f / (4 * m.pi) / 1.602176634e-19, "eV")
tP_f = m.sqrt(hb * GG / cc**5)
print("no cruzamento: max/tP=1, soma/tP=2, quad/tP=", m.sqrt(2))

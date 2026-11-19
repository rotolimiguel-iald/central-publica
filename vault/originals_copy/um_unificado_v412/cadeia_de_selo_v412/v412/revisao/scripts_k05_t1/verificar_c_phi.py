# Revisor K05/T1 -- verificacao numerica [DERIVED -> contas] da constante c_phi no modelo de matrizes/B(l2).
# Modelo: M = B(H), phi = Tr(k .), k > 0 diagonal; sigma_t = Ad k^{it}; M^ = M x L(R) via U (lambda(t) = k^{it} x lambda_0(t)).
# Trace canonico no modelo: tau = Tr x (e^{-p} dp) na coordenada p de lambda_0; entao, para f(h^) com h^ = log k x 1 + 1 x h0:
#   tau(f(h^)) = sum_i  Int f(log k_i + p) e^{-p} dp = Tr(k) * Int f(q) e^{-q} dq     (mudanca de variavel q = log k_i + p).
# Verifica: (1) a identidade numerica para k finito; (2) que a soma diverge quando Tr(k) = inf (phi(1) = inf),
# i.e. tau|_{L(R)} so toma valores 0 ou inf (nao e semifinito).
import math
from scipy import integrate  # noqa: E402

def f(x):                      # f = indicador de [-1, 1]  (f(h^) = e_1)
    return 1.0 if -1.0 <= x <= 1.0 else 0.0

def tau_f_matriz(k):
    tot = 0.0
    for ki in k:
        lo, hi = -1.0 - math.log(ki), 1.0 - math.log(ki)   # f(log ki + p) != 0  <=>  p in [-1-log ki, 1-log ki]
        val, _ = integrate.quad(lambda p: math.exp(-p), lo, hi)
        tot += val
    return tot

def lado_direito(k):
    val, _ = integrate.quad(lambda q: math.exp(-q), -1.0, 1.0)
    return sum(k) * val

for k in ([0.3, 1.1, 2.5], [0.5] * 7, [i + 1 for i in range(10)]):
    a, b = tau_f_matriz(k), lado_direito(k)
    print(f"k={k[:4]}{'...' if len(k)>4 else ''} Tr(k)={sum(k):.4f}  tau(e_1)={a:.10f}  Tr(k)*Int_[-1,1] e^-q={b:.10f}  dif={abs(a-b):.2e}")

print("\nphi(1)=Tr(k) infinito: somas parciais de tau(e_1) para k_i = i (i=1..N): crescem sem limite")
for N in (10, 100, 1000, 10000):
    k = [i + 1 for i in range(N)]
    print(f"  N={N:6d}  tau(e_1) parcial = {tau_f_matriz(k):.6e}")

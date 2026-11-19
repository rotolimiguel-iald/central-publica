import math
from scipy.stats import norm
ALPHA=0.0072973525693; beta=ALPHA*math.sqrt(math.e); M=beta*math.sin(math.pi/4)*1000.0; pred=(M/1000)**2/1e-5
def sigma_for_5(mu):
    m=math.sqrt(10*mu); return 2*mu*abs(m-M)/(5*m)
print("sigma5 (m2) em 7.388:", sigma_for_5(7.388), " sigma5 (dm2):", (7.388-pred)/5)
# SK-Gd futuro com sigma_S = sigma5(9.08) sob verdade = posterior publico JUNO N(7.388, 0.078)
sS = sigma_for_5(9.08)
def P_ge(t, mean, sd, s):
    mhi=(M+math.sqrt(M*M+20*t*s))/2; p=norm.sf((mhi**2/10-mean)/sd)
    disc=M*M-20*t*s
    if disc>=0:
        ma,mb=(M-math.sqrt(disc))/2,(M+math.sqrt(disc))/2
        p+=norm.cdf((mb**2/10-mean)/sd)-norm.cdf((ma**2/10-mean)/sd)
    return p
print("SK-Gd-like futuro sigma_S=%.4f: P(r_S>=5 | verdade ~ N(7.388,0.078)) = %.3e ; P(r_S>=5 | verdade=9.08 +-0.54 posterior) = %.3f" % (sS, P_ge(5,7.388,math.hypot(0.078,sS),sS), P_ge(5,9.08,math.hypot(0.54,sS),sS)))
# S de precisao 0.030 (0.407%) sob mesma verdade: 
s=0.030078; print("S com sigma 0.030078 (0.407%%): P(r_S>=5) = %.4f" % P_ge(5,7.388,math.hypot(0.078,s),s))
# P(r>=3) em Tabela 6 (a1)
s=0.024; print("Tabela 6 (a1): P(r>=3)=%.4f ; P(r>=5)=%.4f" % (P_ge(3,7.388,math.hypot(0.078,s),s), P_ge(5,7.388,math.hypot(0.078,s),s)))
# faixa de C: P(r>=5) Tabela 6 para C=0 (a1) ... C=s^2 (b1) ... C=s^2 e variância mínima
for C in (0, 0.5*s*s, s*s):
    v=0.078**2+s*s-2*C; print("C=%.6f var=%.6f sd=%.5f P(r>=5)=%.4f" % (C, v, math.sqrt(v), P_ge(5,7.388,math.sqrt(v),s)))
# D90 em m2 tabela 6

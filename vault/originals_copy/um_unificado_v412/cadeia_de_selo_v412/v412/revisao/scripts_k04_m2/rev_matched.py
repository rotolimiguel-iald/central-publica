import math
from scipy.stats import norm
import numpy as np
ALPHA=0.0072973525693; beta=ALPHA*math.sqrt(math.e); M=beta*math.sin(math.pi/4)*1000.0; pred=(M/1000)**2/1e-5
def r_frozen(X,s):
    m=np.sqrt(10.0*X); return np.abs(m-M)*m/(5.0*s)
def p_le1_exact(mean, sd, s):
    # r<=1 : m em [mhi.., ] -> região complementar: r<1 sse m em (m_b', m_hi) com m_b'=(M+sqrt(M^2-20 s))/2 e m_hi=(M+sqrt(M^2+20 s))/2, ou m < m_a
    ma=(M-math.sqrt(M*M-20*s))/2; mb=(M+math.sqrt(M*M-20*s))/2; mhi=(M+math.sqrt(M*M+20*s))/2
    # r<=1: m<=ma OU mb<=m<=mhi
    p = norm.cdf((ma**2/10-mean)/sd) + norm.cdf((mhi**2/10-mean)/sd) - norm.cdf((mb**2/10-mean)/sd)
    return p
rows=[("P JUNO207",7.388,0.078,0.078),("SNO+",7.91,0.25,0.25),("SK-Gd reator",9.08,0.54,0.54),("KamLAND",7.54,0.18,0.18),("Solares sem KamLAND",6.10,0.95,0.95)]
kimi={"P JUNO207":17.599161,"SNO+":4.476223,"SK-Gd reator":0.756582,"KamLAND":24.635184,"Solares sem KamLAND":98.493504}
rng=np.random.default_rng(20261114)
pP=None
for n,mu,sd,s in rows:
    ex=p_le1_exact(mu,sd,s); X=rng.normal(mu,sd,1_000_000); mc=float(np.mean(r_frozen(X,s)<=1))
    print("%-22s P(r<=1) exato=%.4f%%  MC=%.4f%%  Kimi=%.4f%%  diff=%.2f pp" % (n,100*ex,100*mc,kimi[n],kimi[n]-100*ex))
    if n=="P JUNO207": pP=ex
for n,mu,sd,s in rows[1:]:
    ex=p_le1_exact(mu,sd,s); print("%-22s P(MATCHED, C=0 brinquedo) exato=%.4f%%  (Kimi %s)" % (n,100*pP*ex, {"SNO+":0.787778,"SK-Gd reator":0.133152,"KamLAND":4.335586,"Solares sem KamLAND":17.334031}[n]))

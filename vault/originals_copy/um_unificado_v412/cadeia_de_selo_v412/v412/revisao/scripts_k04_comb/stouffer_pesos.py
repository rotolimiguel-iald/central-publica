import math
from statistics import NormalDist
N = NormalDist()
D90 = 5 + N.inv_cdf(0.90)
DN = 0.11946607525373273/0.045
sep = 7.388 - 7.2376094667182915

def lam(w, D):
    return sum(wi*di for wi, di in zip(w, D)) / math.sqrt(sum(wi*wi for wi in w))

# 1) a formula do texto: pesos iguais => hypot?
DJ = sep/0.024
print("pesos iguais, sigma_J=0,024: lambda =", lam((1,1),(DJ,DN)), " | hypot =", math.hypot(DJ,DN))
print("poder (pesos iguais) =", N.cdf(lam((1,1),(DJ,DN))-5), "| poder (hypot) =", N.cdf(math.hypot(DJ,DN)-5))
# 2) w proporcional a D => hypot
print("w=D: lambda =", lam((DJ,DN),(DJ,DN)))
# 3) sigma_J requerido com pesos iguais
DJ_req_eq = math.sqrt(2)*D90 - DN
print("pesos iguais: D_J,req =", DJ_req_eq, "sigma_J,req =", sep/DJ_req_eq, "T_novo (dias vivos) =", 207.2*(0.078/(sep/DJ_req_eq))**2)
DJ_req_opt = math.sqrt(D90**2 - DN**2)
print("w prop D: D_J,req =", DJ_req_opt, "sigma_J,req =", sep/DJ_req_opt, "T_novo =", 207.2*(0.078/(sep/DJ_req_opt))**2)
print("JUNO sozinho: sigma =", sep/D90, " T_novo =", 207.2*(0.078/(sep/D90))**2)
# 4) ganho relativo
for nome, s in (("iguais", sep/DJ_req_eq), ("w~D", sep/DJ_req_opt), ("sozinho", sep/D90)):
    print(nome, "T_novo", 207.2*(0.078/s)**2)

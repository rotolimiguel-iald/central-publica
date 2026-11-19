#!/usr/bin/env python3
"""REVISAO_K05_CAMPO — contas do revisor distinto (tarefas 2 e 3). Somente leitura das fontes.

Parte 1: equacao de movimento (Euler-Lagrange) da lagrangiana fundadora como escrita em
         graviton_v2.tex:186 — escalar complexo com 1/2 no cinetico e +xi R |Psi|^2 sem 1/2.
Parte 2: valor conforme em n dimensoes, verificado por covariancia de Weyl (identidade simbolica),
         sem depender da formula (n-2)/(4(n-1)) citada pelo Kimi.
Parte 3: numeros — beta = ALPHA_FINE_CODATA_2018 * sqrt(e) calculado; massas com e sem o fator 2.
Parte 4: reescala do campo e a "carga modular" |Psi|^2.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import sympy as sp

getcontext().prec = 50
RAIZ = Path(r"C:\IALD")
UM_PY = RAIZ / r"Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
FALA = RAIZ / r"Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt"
SAIDA = Path(__file__).resolve().parent / "conta_campo_saida.json"

out: dict = {}

# ---------------------------------------------------------------- Parte 1: EL
t, x, y, z = sp.symbols("t x y z", real=True)
X = (t, x, y, z)
xi, R, m2 = sp.symbols("xi R m2", real=True)  # R tratado como fundo constante (nao varia com Psi)
Psi = sp.Function("Psi")(*X)
Pb = sp.Function("Pb")(*X)  # Psi^dagger, tratado como independente

res_part1 = {}
for nome, eta in (("(+---)", sp.diag(1, -1, -1, -1)), ("(-+++)", sp.diag(-1, 1, 1, 1))):
    ginv = eta.inv()
    cin = sp.Rational(1, 2) * sum(ginv[i, j] * sp.diff(Pb, X[i]) * sp.diff(Psi, X[j]) for i in range(4) for j in range(4))
    V = m2 * Pb * Psi / 2  # V(Psi) = m^2|Psi|^2/2, so dV/dPsi^dagger = m^2 Psi/2
    L = cin - V + xi * R * Pb * Psi
    # Euler-Lagrange em Psi^dagger: dL/dPb - d_mu( dL/d(d_mu Pb) ) = 0
    dLdPb = sp.diff(L, Pb)
    termo = sum(sp.diff(sp.diff(L, sp.diff(Pb, X[i])), X[i]) for i in range(4))
    eom = sp.simplify(dLdPb - termo)
    # box covariante em fundo plano: g^{mu nu} d_mu d_nu
    box = sum(ginv[i, j] * sp.diff(Psi, X[i], X[j]) for i in range(4) for j in range(4))
    # eom = -(1/2) box Psi + (xi R - m2/2) Psi  =>  multiplicar por -2:
    eom2 = sp.expand(-2 * eom)
    coef_box = sp.simplify(sp.expand(eom2).coeff(sp.Derivative(Psi, (t, 2)))) if False else None
    # extrair coeficientes comparando com a forma  box*Psi + a*R*Psi + b*m2*Psi
    a = sp.symbols("a")
    b = sp.symbols("b")
    ans = sp.expand(eom2 - (box + a * R * Psi + b * m2 * Psi))
    sol = sp.solve([sp.expand(ans).coeff(R * Psi), sp.expand(ans).coeff(m2 * Psi)], [a, b], dict=True)
    # resto sem R, m2 deve ser identicamente zero
    resto = sp.simplify(ans.subs({R: 0, m2: 0}))
    res_part1[nome] = {
        "eom_vezes_menos2": str(eom2),
        "forma": "box Psi + a R Psi + b m2 Psi = 0",
        "solucao": {str(k): str(v) for k, v in sol[0].items()},
        "resto_sem_R_nem_m2_e_zero": bool(resto == 0),
    }
out["parte1_euler_lagrange_L186"] = res_part1

# ---------------------------------------------------------------- Parte 2: Weyl
def weyl_check(n: int) -> dict:
    coords = sp.symbols(f"c0:{n}", real=True)
    sigma = sp.Function("sigma")(*coords)
    psi0 = sp.Function("psi0")(*coords)
    eta = sp.diag(*([-1] + [1] * (n - 1)))
    ginv0 = eta.inv()

    def box_eta(f):
        return sum(ginv0[i, i] * sp.diff(f, coords[i], 2) for i in range(n))

    def dot_eta(f, g):
        return sum(ginv0[i, i] * sp.diff(f, coords[i]) * sp.diff(g, coords[i]) for i in range(n))

    # g = e^{2 sigma} eta  (conformalmente plana).
    # box_g f = e^{-n sigma} d_mu( e^{(n-2) sigma} eta^{mu nu} d_nu f )
    def box_g(f):
        return sp.exp(-n * sigma) * sum(
            sp.diff(sp.exp((n - 2) * sigma) * ginv0[i, i] * sp.diff(f, coords[i]), coords[i]) for i in range(n)
        )

    # R(g) = -2(n-1) e^{-2 sigma} [ box_eta sigma + (n-2)/2 (d sigma)^2 ]  (convencao: esfera tem R>0)
    Rg = -2 * (n - 1) * sp.exp(-2 * sigma) * (box_eta(sigma) + sp.Rational(n - 2, 2) * dot_eta(sigma, sigma))
    xi_c = sp.Rational(n - 2, 4 * (n - 1))
    psi = sp.exp(-sp.Rational(n - 2, 2) * sigma) * psi0
    lhs = sp.simplify(sp.exp(sp.Rational(n + 2, 2) * sigma) * (box_g(psi) - xi_c * Rg * psi) - box_eta(psi0))
    # controle negativo: outro xi falha
    xi_errado = xi_c / 2
    lhs_err = sp.simplify(sp.exp(sp.Rational(n + 2, 2) * sigma) * (box_g(psi) - xi_errado * Rg * psi) - box_eta(psi0))
    return {"n": n, "xi_conforme": str(xi_c), "identidade_weyl_vale": bool(lhs == 0),
            "controle_metade_do_xi_falha": bool(lhs_err != 0)}


out["parte2_valor_conforme"] = [weyl_check(n) for n in (3, 4, 5)]
xi_eom_4d = Fraction(1, 6)
out["parte2_conclusao"] = {
    "xi_c_n4": str(xi_eom_4d),
    "coeficiente_do_R_na_EOM_fundadora": "2*xi_L (magnitude; sinal depende de convencao)",
    "xi_L_para_EOM_conforme": str(xi_eom_4d / 2),
}

# ---------------------------------------------------------------- Parte 3: numeros
txt = UM_PY.read_text(encoding="utf-8", errors="replace").splitlines()
alpha_linha = next(l for l in txt[5580:5590] if l.startswith("ALPHA_FINE_CODATA_2018"))
alpha_str = alpha_linha.split("=")[1].split("#")[0].strip()
alpha = Decimal(alpha_str)
beta = alpha * Decimal(1).exp().sqrt()  # sqrt(e) = exp(1/2) em runtime
u_mev = Decimal(1000)  # u = 1 eV posto, apenas convertido a meV
massa_com2 = beta * u_mev / Decimal(2).sqrt()
massa_sem2 = beta * u_mev / Decimal(2)
out["parte3_numeros"] = {
    "alpha_lido_de_um.py_linha_5584": alpha_str,
    "beta": str(beta),
    "massa_com_fator_2_meV": str(massa_com2),
    "massa_sem_fator_2_meV": str(massa_sem2),
    "razao": str(massa_com2 / massa_sem2),
    "hbar_omega_meV": str(2 * massa_com2),
    "com2_arredondado_6c": f"{massa_com2:.6f}",
    "sem2_arredondado_6c": f"{massa_sem2:.6f}",
}

# ---------------------------------------------------------------- Parte 4: reescala / carga
# L_half = 1/2 |dPsi|^2 + xi R|Psi|^2 ;  L_can = |dPhi|^2 + xi_c R |Phi|^2
# Psi = sqrt(2) Phi => L_half = |dPhi|^2 + 2 xi_L R |Phi|^2  => xi_c = 2 xi_L
lam = sp.symbols("lam", positive=True)
ph, dph, xi_L, xi_c = sp.symbols("ph dph xi_L xi_c", real=True)
Lhalf = sp.Rational(1, 2) * (lam * dph) ** 2 + xi_L * R * (lam * ph) ** 2  # Psi = lam * Phi
Lcan = dph ** 2 + xi_c * R * ph ** 2
solv = sp.solve([sp.Eq(sp.expand(Lhalf).coeff(dph, 2), 1), sp.Eq(sp.expand(Lhalf).coeff(ph, 2), xi_c * R)], [lam, xi_c], dict=True)
out["parte4_reescala"] = {
    "psi_em_funcao_de_phi_canonico": [str(s[lam]) for s in solv],
    "xi_c_em_funcao_de_xi_L": [str(s[xi_c]) for s in solv],
    "|Psi|^2 / |Phi|^2": "2 (quando Psi = sqrt(2) Phi)",
    "EOM_homogenea_linear": "a EOM linear em Psi nao fixa a norma de Psi; a normalizacao vem da ACAO (cinetico 1/2 vs 1) e da carga de Noether",
}

# ---------------------------------------------------------------- Parte 5: um so acoplamento nao reconcilia, em nenhuma normalizacao
um_sexto = Decimal(1) / Decimal(6)
out["parte5_um_so_xi_nao_basta"] = {
    "(1/6)/beta": str(um_sexto / beta),
    "(1/6)/(2*beta)": str(um_sexto / (2 * beta)),
    "leitura": "o coeficiente de R na EOM do Artigo A (1/6, ou 1/12 na escrita fundadora) e o da dispersao do psion (2*beta=0,02406 ou beta=0,01203) "
               "diferem por fator ~6,9 a ~13,9; o fator 2 da normalizacao (1/2 vs 1) nao reconcilia: sao dois acoplamentos (ou uma hipotese nova)",
    "xi_L_beta_da_dispersao_psion_na_escrita_fundadora": "dispersao 2*xi_L*R com xi_L = beta  =>  coef EOM = 2*beta = " + str(2 * beta),
    "xi_L_conforme": "1/12 = " + str(Decimal(1) / Decimal(12)),
}

# ---------------------------------------------------------------- fala: aspas
fala_bytes = FALA.read_bytes()
out["fala"] = {"bytes": len(fala_bytes), "sha256": sha256(fala_bytes).hexdigest()}

SAIDA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))

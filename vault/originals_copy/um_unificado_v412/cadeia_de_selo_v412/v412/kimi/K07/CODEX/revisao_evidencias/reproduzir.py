"""Independent numerical checks for the K07 review. No data from observations."""
import cmath
import hashlib
import itertools
import json
import math
import re
from fractions import Fraction
from functools import reduce
from pathlib import Path


review = Path(__file__).resolve().parent
codex = review.parent
edition = codex.parents[2]
paper = Path("C:/IALD/Artigo/Haja_Luz")
report = json.loads((codex / "MEDIDAS_CAMPO_TAU_R3.json").read_text(encoding="utf-8"))
prior = json.loads((edition / "revisao/scripts_k05_tau/revisor_tau_numeros_saida.json").read_text(encoding="utf-8"))
with (paper / "A Ponte e o Um/Nós/um.py").open(encoding="utf-8") as src:
    for line in src:
        match = re.match(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.Ee+-]+)\s*$", line)
        if match:
            alpha = float(match[1])
            break
    else:
        raise RuntimeError("The named alpha constant is missing")

beta = alpha * math.exp(0.5)
c = 299_792_458
hbar = 6.62607015e-34 / math.tau
u = 1.602176634e-19
G = 6.67430e-11
t_planck = (hbar * G / c**5)**0.5
mu = 60 * 1.3271244e20
t_circ = math.tau * (2 * mu / c**2) / c
t_kms = math.tau / (c**3 / (4 * mu))
gravitational_parameter = 60 * 132712440000000000000
circ_without_2pi = Fraction(2*gravitational_parameter, c**2) / c
kms_without_2pi = 1 / Fraction(c**3, 4*gravitational_parameter)
assert kms_without_2pi == 2*circ_without_2pi
checks = {
    "4pi_seconds": (t_circ, report["clock"]["source_60_Msun_s"]["light_circle_4pi"]),
    "8pi_seconds": (t_kms, report["clock"]["source_60_Msun_s"]["KMS_8pi"]),
    "mass_with_two_meV": (1000 * (2 * beta*beta)**0.5 / 2, report["field"]["zero_point_with_two_meV"]),
    "control_mass_meV": (1000 * (beta*beta)**0.5 / 2, report["field"]["counterfactual_without_two_meV"]),
    "Sr_one_eV_orders": (math.log10(hbar/u) - math.log10(prior["bounds"]["sr87_kim2025"]), report["clock"]["log10_times_over_strontium_P1_95"][0]),
    "Sr_retained_orders": (math.log10(hbar/(beta*u)) - math.log10(prior["bounds"]["sr87_kim2025"]), report["clock"]["log10_times_over_strontium_P1_95"][1]),
}
for tag in ["sr87_kim2025", "zn67_potzel1976"]:
    ratio = prior["bounds"][tag]*beta/t_planck
    checks[tag] = (math.log10(ratio), report["clock"]["log10_margin_largest_planck_candidate"][tag])
for actual, expected in checks.values():
    assert math.isclose(actual, expected, rel_tol=2e-14, abs_tol=0)

def multiply(a, b):
    columns = tuple(zip(*b))
    return [[sum(u*v for u, v in zip(row, col)) for col in columns] for row in a]

def tensor(a, b):
    return [[a[i][j]*b[r][s] for j in range(len(a)) for s in range(len(b))]
            for i in range(len(a)) for r in range(len(b))]

def scale(a, fac):
    return [[fac*v for v in row] for row in a]

def conjugate(a):
    return [[v.conjugate() for v in row] for row in a]

ident = ((1, 0), (0, 1))
pauli = (((0, 1), (1, 0)), ((0, -1j), (1j, 0)), ((1, 0), (0, -1)))
gammas = [tensor(g, pauli[0]) for g in pauli] + [tensor(ident, pauli[1])]
charge = tensor(pauli[1], ident)
chirality = tensor(ident, pauli[2])
for gamma in gammas:
    assert reduce(multiply, [charge, conjugate(gamma), charge]) == scale(gamma, -1)
assert multiply(charge, conjugate(charge)) == scale(tensor(ident, ident), -1)
perms = list(itertools.permutations(range(4)))
for perm in perms:
    inversions = sum(x > y for x, y in itertools.combinations(perm, 2))
    value = reduce(multiply, [gammas[j] for j in perm])
    assert scale(value, (-1)**inversions) == scale(chirality, -1)

# Independent illustration of the Fourier factor; the integral equality is analytic.
n, bound, v, delta = 24000, 12, 2, 3
step = 2*bound/n
def weighted(s):
    return math.exp(-s*s/(2*v)) * cmath.exp(1j*delta*s) / math.sqrt(math.tau*v)
numeric = step*sum(weighted(-bound+(j+.5)*step) for j in range(n))
analytic = math.exp(-v*delta*delta/2)
assert abs(numeric-analytic) < 3e-15

# 2-forms in a Lorentz-orthonormal coframe; standard interior products.
def electromagnetic_invariants(electric, magnetic):
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    return 2*(dot(magnetic, magnetic) - dot(electric, electric)), -4*dot(electric, magnetic)
pure = electromagnetic_invariants((1,0,0), (0,0,0))
wave = electromagnetic_invariants((1,0,0), (0,1,0))
assert pure == (-2, 0) and wave == (0, 0)
assert pure[0] == report["field"]["F_dot_F"] and pure[1] == report["field"]["F_dot_star_F"]
assert report["field"]["null_wave_squared"] == wave[0]

print(json.dumps({
    "numerical_controls_actual_and_authors": checks,
    "comparisons_within_relative_tolerance": 2e-14,
    "orientation_signed_terms_equal_minus_chirality": len(perms),
    "anticommutation_with_charge_conjugation": 4,
    "J_square": -1,
    "gaussian_variance": v, "gaussian_frequency_difference": delta,
    "gaussian_control_reference": analytic, "gaussian_quadrature_abs_error": abs(numeric-analytic),
    "electromagnetic_invariants": {"pure_electric": pure, "null_wave": wave},
    "bounds_source_sha256": hashlib.sha256((edition / "revisao/scripts_k05_tau/revisor_tau_numeros_saida.json").read_bytes()).hexdigest(),
    "comparison_source_sha256": hashlib.sha256((codex / "MEDIDAS_CAMPO_TAU_R3.json").read_bytes()).hexdigest(),
}, ensure_ascii=False, indent=2))

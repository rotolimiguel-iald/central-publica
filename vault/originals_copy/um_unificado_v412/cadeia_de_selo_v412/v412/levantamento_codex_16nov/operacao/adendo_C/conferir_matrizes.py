"""Controles algébricos exatos da seção E, Adendo C. Sem importação do programa da TGL."""
import hashlib
import json
import re
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
KERNEL = NOS / "tgl_kernel" / "TGLExt"
PAULI = KERNEL / "SitePauliObservables.lean"
SOLDER = KERNEL / "Solder4D.lean"


def literal_matrix(source, name):
    line = next(s for s in source.read_text(encoding="utf8").splitlines() if s.startswith(f"def {name} "))
    literal = re.search(r"!!\[([^\]]+)\]", line).group(1)
    constants = {"0": 0, "1": 1, "-1": -1, "Complex.I": sp.I, "-Complex.I": -sp.I}
    return sp.Matrix([[constants[v.strip()] for v in row.split(",")] for row in literal.split(";")])


def commutes(a, b):
    return (a*b - b*a).applyfunc(sp.expand).is_zero_matrix


def run():
    identity = sp.eye(2)
    pauli = [literal_matrix(PAULI, f"pauli{axis}Matrix") for axis in "XYZ"]
    basis = [identity, *pauli]
    generators = [a/2 for a in pauli] + [-sp.I*a/2 for a in pauli]
    results = {}
    for name, g in zip(["K1", "K2", "K3", "J1", "J2", "J3"], generators):
        columns = []
        for b in basis:
            action = g*b + b*g.H
            columns.append(sp.Matrix([(e*action).trace()/2 for e in basis]))
        matrix = sp.Matrix.hstack(*columns)
        assert matrix == literal_matrix(SOLDER, name)
        results[name] = matrix.tolist()

    # Dois instrumentos com o mesmo gerador sem salto. Para s=ln(2)/2, exp(-2s)=1/2.
    ground = sp.diag(1, 0)
    excited = sp.diag(0, 1)
    down = sp.Matrix([[0, 1], [0, 0]])
    q = sp.Rational(1, 2)
    no_jump = sp.diag(1, sp.sqrt(q))
    controls = {}
    for name, jump in [("desfasamento", excited), ("relaxacao", down)]:
        assert jump.H*jump == excited
        observed_jump = sp.sqrt(1-q)*jump
        assert no_jump.H*no_jump + observed_jump.H*observed_jump == identity
        output = no_jump*excited*no_jump.H + observed_jump*excited*observed_jump.H
        assert output.trace() == 1
        assert output == (excited if name == "desfasamento" else (excited+ground)/2)
        controls[name] = str(output.det())

    # Modelo concreto do rito, com os símbolos reais cos(theta), sin(theta) mantidos livres.
    c, s = sp.symbols("c s", real=True)
    j = sp.diag(1, 1, -1, -1)
    rotation = sp.diag(sp.Matrix([[c,s], [-s,c]]), sp.eye(2))
    dc = sp.kronecker_product(j, j) - sp.eye(16)
    db = sp.kronecker_product(rotation, rotation) - sp.eye(16)
    dz = sp.zeros(16)
    for a,b in [(2,3), (3,2)]:
        dz[4*b+a, 4*b+a] = 1
    for ops in ([dc,db,dz], [dc.H*dc,db.H*db,dz.H*dz]):
        assert all(commutes(ops[i],ops[j]) for i,j in [(0,1),(1,2),(2,0)])
    assert all(not commutes(generators[i], generators[j]) for i,j in [(0,1),(1,2),(2,0)])
    return {"estatuto":"DERIVED_CONTROLES_MATRICIAIS_EXATOS", "sympy":sp.__version__,
            "matrizes_4x4_lidas_e_reconstruidas":results, "determinantes_finais":controls,
            "determinante_inicial":"0", "comutadores_defeitos_e_custos_concretos":"zero nos três pares",
            "comutadores_pauli":"não nulos nos três pares",
            "fontes":[{"arquivo":str(f),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}
                      for f in (PAULI, SOLDER, NOS/"um.py")]}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, default=int))


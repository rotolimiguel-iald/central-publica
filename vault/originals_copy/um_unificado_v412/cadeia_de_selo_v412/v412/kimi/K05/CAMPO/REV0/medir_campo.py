#!/usr/bin/env python3
"""Medidas locais da K05/CAMPO; somente leitura das fontes, sem build do kernel."""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

getcontext().prec = 50
RAIZ = Path(r"C:\IALD")
SAIDA = Path(__file__).resolve().parent / "medidas_campo.json"

KERNEL = RAIZ / r"Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\PontoZeroDoPsion.lean"
FUNDADOR = RAIZ / r"Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\graviton_v2.tex"
FALA = RAIZ / r"Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt"


def linhas(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def exige(path: Path, numero: int, trechos: list[str]) -> dict:
    texto = linhas(path)[numero - 1]
    faltantes = [trecho for trecho in trechos if trecho not in texto]
    if faltantes:
        raise AssertionError(f"{path}:{numero}: faltam {faltantes!r} em {texto!r}")
    return {"arquivo": str(path), "linha": numero, "texto": texto}


# Valor conforme usual em n dimensões: (n−2)/(4(n−1)).
xi_conforme_eom = Fraction(4 - 2, 4 * (4 - 1))
# Na escrita de graviton_v2.tex: cinético com 1/2 e +xi R|Psi|² dão 2xi R na EOM.
xi_lagrangiana_fundadora = xi_conforme_eom / 2
assert xi_conforme_eom == Fraction(1, 6)
assert xi_lagrangiana_fundadora == Fraction(1, 12)

alpha = Decimal("0.0072973525693")  # [INPUT/KNOWN] CODATA 2018, também em TGL_ATLAS.md:762.
beta = alpha * Decimal(1).exp().sqrt()  # sqrt(e) = exp(1/2).
u_mev = Decimal(1000)  # [INPUT/DECLARADO] unidade posta u = 1 eV, apenas convertida a meV.
# Com omega²=2 beta R e R=beta u²: (1/2)omega = beta u/sqrt(2).
massa_com_2_mev = beta * u_mev / Decimal(2).sqrt()
# Sem o 2, omega²=beta R e a mesma R: (1/2)omega = beta u/2.
massa_sem_2_mev = beta * u_mev / 2
razao = massa_com_2_mev / massa_sem_2_mev
assert abs(razao - Decimal(2).sqrt()) < Decimal("1e-48")

# Régua da errata vigente: Psi_(cinético 1/2) = sqrt(2) * Psi_(cinético 1).
psi_meio_sobre_psi_coef1 = Decimal(2).sqrt()
razao_norma_quadrada = Fraction(2, 1)  # (sqrt(2))²; |Psi|² não é inócuo se a carga é fixada.
assert abs(psi_meio_sobre_psi_coef1 ** 2 - Decimal(2)) < Decimal("1e-48")
assert 2 * xi_lagrangiana_fundadora == xi_conforme_eom

pins = [
    exige(KERNEL, 22, ["ω² = m₀² + 2ξR", "ξ = β"]),
    exige(KERNEL, 36, ["½·√(2β²) = β/√2 = β·sen 45°"]),
    exige(KERNEL, 85, ["ω² = 2·β·R"]),
    exige(KERNEL, 86, ["2 * β * R"]),
    exige(KERNEL, 199, ["↔ τ = tempoDoRetido"]),
    exige(FUNDADOR, 186, [r"\frac{1}{2}g", r"\xi R|\Psi|^2", r"- \frac{1}{4}F"]),
    exige(FUNDADOR, 192, [r"D_\mu = \nabla_\mu - ieA_\mu", "U(1)"]),
    exige(FUNDADOR, 200, [r"\Box\Psi + 2\xi R\Psi"]),
    exige(FUNDADOR, 204, [r"\xi = 1/6", "forced"]),
    exige(FUNDADOR, 214, [r"\Box\Psi + m_{\text{eff}}^2\Psi + 2\xi R\Psi"]),
]

fala_bytes = FALA.read_bytes()
resultado = {
    "escopo": "K05/CAMPO; contas algébricas e pins literais; não altera cânone nem executa Lean",
    "conforme": {
        "formula_n4": "(n−2)/(4(n−1)), n=4",
        "xi_na_eom_conforme": str(xi_conforme_eom),
        "coeficiente_na_eom_fundadora": "2*xi_lagrangiana",
        "xi_lagrangiana_para_eom_conforme": str(xi_lagrangiana_fundadora),
        "decimal_xi_lagrangiana": float(xi_lagrangiana_fundadora),
        "duas_vezes_xi_lagrangiana": str(2 * xi_lagrangiana_fundadora),
    },
    "regua_do_campo": {
        "psi_meio_sobre_psi_coef1": str(psi_meio_sobre_psi_coef1),
        "norma_ao_quadrado_meio_sobre_coef1": str(razao_norma_quadrada),
        "observacao": "A EOM pode ser preservada pela reescala, mas |Psi|² muda por 2; carga modular fixada torna a régua física.",
    },
    "massa_ponto_zero": {
        "alpha_input": str(alpha),
        "beta_calculado": str(beta),
        "u_input_mev": str(u_mev),
        "com_fator_2_mev": str(massa_com_2_mev),
        "sem_fator_2_mev": str(massa_sem_2_mev),
        "razao_com_sobre_sem": str(razao),
        "identidade": "com_2 = beta*u/sqrt(2); sem_2 = beta*u/2",
    },
    "fala": {"bytes": len(fala_bytes), "sha256": sha256(fala_bytes).hexdigest()},
    "pins_verificados": pins,
}
SAIDA.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(resultado, ensure_ascii=False, indent=2))

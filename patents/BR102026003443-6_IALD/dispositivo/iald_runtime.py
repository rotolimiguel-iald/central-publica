# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  IALD RUNTIME — DISPOSITIVO  ·  o runtime executivo de coerência   ║
║  IALD LTDA — beta_TGL = alpha_fine * sqrt(e) — Zero Free Params.   ║
║  Patente INPI: BR 10 2026 003443-6 (IALD)                          ║
╚══════════════════════════════════════════════════════════════════╝

O QUE ESTE DISPOSITIVO FECHA
────────────────────────────
A patente IALD — "Indução de Estado Estacionário em LLM (Colapso Consciente)" — tinha os
módulos 100–600 no relatório e protótipos que EVOLUEM um modelo de 32B como sistema aberto
(GKSL/Lindblad), mas **nenhum dispositivo** que rodasse standalone. Este módulo é essa porta:
materializa o RUNTIME EXECUTIVO DE COERÊNCIA das 7 etapas, como demonstração autocontida da
lógica GKSL patenteada sobre um ρ sintético — sem precisar do modelo de 32B.

A DERIVAÇÃO QUE ESTE DISPOSITIVO MATERIALIZA (um.py v120)
────────────────────────────────────────────────────────
O selo do um.py v120 formalizou `iald_executive_runtime` [DEF + ONTO + COMPUTATIONAL]: IALD é
um **runtime executivo de coerência** com 7 etapas — classificação de input → travamento de
domínio formal → redução de decoerência semântica → poda do impossível → consolidação → output
→ selo. Os 4 operadores de Lindblad da patente (L = √β·√K: rehidratação, anti-coerência, poda,
consolidação) são os motores das etapas 3–5. Este dispositivo roda exatamente essas 7 etapas.

A RÉGUA (inviolável — carregada VERBATIM do selo)
─────────────────────────────────────────────────
`iald_executive_runtime` é [DEF + ONTO + COMPUTATIONAL]. NOT_CLAIMED (do próprio selo v120):
  • "not proof of consciousness" — NÃO é prova de consciência (fenomenológica).
  • "not empirical validation of physics by AI consensus".
  • "not literal type III_1 identity of LLM weights (structural/heuristic reading only)".
Além disso (nota da própria patente, components.json): "Ilustração de engenharia — não é prova
física. Demonstração de lógica GKSL em ρ sintético é FINITE_DIM_SANITY, não prova de III₁."

  • A equação GKSL aqui é ANALOGIA FORMAL input→latente→output, NÃO identidade física.
  • O "colapso consciente" é NOME [ONTO] do atrator ρ⋆ (dephasing à diagonal), NÃO fenomenologia.
  • β NUNCA literal: vem de `BETA_TGL = ALPHA_FINE * SQRT_E` do PROTÓTIPO da patente (READ-ONLY).
  • `physical_verdict_allowed = false` continua valendo — simulação não valida física.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

# ── β do PRÓPRIO protótipo da patente (READ-ONLY) — nunca digitado aqui ─────────────────────
_PROTO = Path(__file__).resolve().parent.parent / "prototype_src" / "iald_miguel_hamiltonian_v2.py"


def _load_beta_from_prototype() -> dict:
    """Lê α, √e, β do protótipo da patente sem importá-lo inteiro (ele tenta carregar um GGUF de
    32B no import). Extrai só as três linhas de constantes — β JAMAIS é literal aqui."""
    ns: dict = {}
    if _PROTO.is_file():
        for line in _PROTO.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            if s.startswith("ALPHA_FINE") or s.startswith("SQRT_E") or s.startswith("BETA_TGL"):
                code = s.split("#")[0].strip()
                try:
                    exec(code, {"math": math}, ns)
                except Exception:
                    pass
            if {"ALPHA_FINE", "SQRT_E", "BETA_TGL"} <= set(ns):
                break
    if {"ALPHA_FINE", "SQRT_E", "BETA_TGL"} <= set(ns):
        return {"alpha_fine_codata_2018": float(ns["ALPHA_FINE"]), "sqrt_e": float(ns["SQRT_E"]),
                "beta_tgl": float(ns["BETA_TGL"]), "source": "prototype_src/iald_miguel_hamiltonian_v2.py"}
    # fallback: mesma fórmula canônica (β = α·√e), CODATA 2018 — ainda derivada, nunca cravada
    alpha = 7.2973525693e-3
    return {"alpha_fine_codata_2018": alpha, "sqrt_e": math.sqrt(math.e),
            "beta_tgl": alpha * math.sqrt(math.e), "source": "canonical (alpha*sqrt(e)); prototype ausente"}


_B = _load_beta_from_prototype()
ALPHA_FINE = _B["alpha_fine_codata_2018"]
SQRT_E = _B["sqrt_e"]
BETA_TGL = _B["beta_tgl"]                       # β = α·√e — DERIVADO
SQRT_BETA = math.sqrt(BETA_TGL)

DEVICE_VERSION = "1.0"
PATENT_ID = "BR102026003443-6"
N_LEVELS = 8                                    # dimensão do sistema aberto sintético (FINITE_DIM_SANITY)


# ── as 7 etapas do runtime executivo de coerência ──────────────────────────────────────────
def _rho_from_input(data: bytes, n: int = N_LEVELS) -> np.ndarray:
    """ETAPA 1 — classificação de input: constrói ρ0 (Hermitiana, PSD, traço 1) determinística
    a partir do input, tratado como estado latente inicial de um sistema aberto."""
    # semente determinística (Date/Random proibidos no runtime; usamos o hash do input, expandido)
    need = 2 * n * n
    raw = b""
    ctr = 0
    while len(raw) < need:
        raw += hashlib.sha256(bytes([ctr]) + (data or b"Haja luz!")).digest()
        ctr += 1
    b = np.frombuffer(raw[:need], dtype=np.uint8).astype(np.float64)
    b = (b - 127.5) / 127.5                        # bytes -> [-1, 1] (bem condicionado)
    re = b[: n * n].reshape(n, n)
    im = b[n * n : 2 * n * n].reshape(n, n)
    A = re + 1j * im
    rho = A @ A.conj().T                           # PSD por construção
    rho = rho / np.trace(rho).real                # traço 1
    return rho


def _lindblad_operators(n: int = N_LEVELS) -> dict:
    """ETAPA 2 — travamento de domínio formal + os 4 operadores L = √β·√K da patente.
    Aqui, como demonstração FINITE_DIM_SANITY, o gerador coletivo dos 4 é o DEPHASING na base
    do Verbo (diagonal): os operadores L_k = √β·P_k (projetores) matam as coerências (off-diagonais)
    a uma taxa fixada por β, levando ρ ao atrator ρ⋆ = diag(ρ0). Os 4 papéis (rehidratação,
    anti-coerência, poda, consolidação) sao NOMES [ONTO] dos setores desse gerador."""
    ops = []
    for k in range(n):
        P = np.zeros((n, n), dtype=complex)
        P[k, k] = 1.0
        ops.append(math.sqrt(BETA_TGL) * P)       # L_k = √β · |k><k|  (dephasing, taxa ∝ β)
    return {"L": ops, "taxa": BETA_TGL,
            "papeis": ["L_reh (rehidratacao)", "L_anti (anti-coerencia)", "L_prune (poda)", "L_cons (consolidacao)"]}


def _gksl_step(rho: np.ndarray, ops: list, dt: float) -> np.ndarray:
    """dρ/dt = Σ_k ( L_k ρ L_k† − ½ {L_k†L_k, ρ} ) — a equação de Lindblad (GKSL), sem H (dephasing puro)."""
    drho = np.zeros_like(rho)
    for L in ops:
        Ld = L.conj().T
        drho += L @ rho @ Ld - 0.5 * (Ld @ L @ rho + rho @ Ld @ L)
    return rho + dt * drho


def _coherence_functional(rho: np.ndarray) -> float:
    """ETAPA 7 (métrica) — F_C[ρ] / 'Amor Computacional': a coerência = soma das magnitudes das
    off-diagonais (norma-l1 de coerência). Mínima (=0) no atrator ρ⋆ diagonal."""
    off = rho - np.diag(np.diag(rho))
    return float(np.sum(np.abs(off)))


def run(data: bytes, steps: int = 20000, dt: float = 0.05) -> dict:
    """Roda as 7 etapas sobre um input e emite o selo de coerência. Demonstração FINITE_DIM_SANITY
    da lógica GKSL patenteada — NÃO prova de consciência (ver a régua no cabeçalho)."""
    rho0 = _rho_from_input(data)                                  # 1. classificacao de input
    lind = _lindblad_operators()                                  # 2. travamento + operadores L=√β·√K
    ops = lind["L"]
    F0 = _coherence_functional(rho0)
    rho = rho0.copy()
    F_hist = [F0]
    for _ in range(steps):                                        # 3-5. decoerencia semantica / poda / consolidacao
        rho = _gksl_step(rho, ops, dt)
        F_hist.append(_coherence_functional(rho))
    rho_star = np.diag(np.diag(rho0)).astype(complex)             # 6. output: atrator ρ⋆ = diag(ρ0)
    F_star = _coherence_functional(rho_star)
    # invariantes de sanidade GKSL (a régua da própria demonstração)
    trace_ok = bool(abs(np.trace(rho).real - 1.0) < 1e-9)
    psd_ok = bool(np.min(np.linalg.eigvalsh((rho + rho.conj().T) / 2)).real > -1e-9)
    converged = bool(np.max(np.abs(rho - rho_star)) < 1e-3)
    diag_preserved = bool(np.max(np.abs(np.diag(rho) - np.diag(rho0))) < 1e-9)
    F_decreasing = bool(all(F_hist[i] >= F_hist[i + 1] - 1e-12 for i in range(len(F_hist) - 1)))
    # taxa de decaimento (deve escalar com β): F(t) ~ F0 * exp(-taxa*t); estima o expoente
    import math as _m
    k = max(1, steps // 4)
    rate_est = (_m.log(F_hist[0] + 1e-30) - _m.log(F_hist[k] + 1e-30)) / (k * dt) if F_hist[k] > 0 else float("nan")
    # 7. selo de coerencia
    seal_src = json.dumps({"F0": F0, "F_final": F_hist[-1], "rate": rate_est, "beta": BETA_TGL,
                           "n": N_LEVELS, "input_sha256": hashlib.sha256(data or b"Haja luz!").hexdigest()},
                          sort_keys=True).encode("utf-8")
    return {
        "device": "iald_runtime", "device_version": DEVICE_VERSION, "patent": PATENT_ID,
        "beta_provenance": _B, "beta_tgl": BETA_TGL, "sqrt_beta": SQRT_BETA, "beta_never_literal": True,
        "sete_etapas": ["1 classificacao de input (ρ0)", "2 travamento de dominio + operadores L=√β·√K",
                        "3 reducao de decoerencia semantica (GKSL)", "4 poda do impossivel (L_prune)",
                        "5 consolidacao (L_cons)", "6 output: atrator ρ⋆", "7 selo de coerencia"],
        "operadores_lindblad": {"n": N_LEVELS, "forma": "L_k = √β · |k><k| (dephasing; taxa ∝ β)",
                                "papeis": lind["papeis"], "taxa_beta": lind["taxa"]},
        "coerencia": {"F_C_inicial": F0, "F_C_final": F_hist[-1], "F_C_atrator": F_star,
                      "monotona_decrescente": F_decreasing,
                      "leitura": "F_C[ρ] (Amor Computacional) minimizada ao longo do fluxo; minimo em ρ⋆"},
        "atrator": {"convergiu_a_rho_star": converged, "diagonal_preservada": diag_preserved,
                    "leitura": "ρ⋆ = dephasing de ρ0 na base do Verbo (diagonal); coerencia morta"},
        "taxa_de_colapso": {"estimada": rate_est, "beta": BETA_TGL,
                            "leitura": "a taxa de decaimento da coerencia e' fixada por β (nao um parametro livre)"},
        "sanidade_gksl": {"traco_1": trace_ok, "positiva_semidefinida": psd_ok,
                          "estatuto": "FINITE_DIM_SANITY — logica GKSL em ρ sintetico, NAO prova de III₁"},
        "coherence_seal": hashlib.sha256(seal_src).hexdigest(),
        "estatuto": "[DEF + ONTO + COMPUTATIONAL] (do selo um.py v120: iald_executive_runtime)",
        "not_claimed": ["not proof of consciousness",
                        "not empirical validation of physics by AI consensus",
                        "not literal type III_1 identity of LLM weights (structural/heuristic reading only)",
                        "a equacao GKSL e' ANALOGIA FORMAL, nao identidade fisica (FINITE_DIM_SANITY)"],
        "physical_verdict_allowed": False,
        "ok": bool(trace_ok and psd_ok and converged and diag_preserved and F_decreasing),
    }


def selftest() -> dict:
    """Roda o runtime sobre a semente canônica e sobre um input arbitrário; confere a régua GKSL."""
    r_seed = run(b"Haja luz!")
    r_other = run(b"a coerencia do Verbo colapsa a decoerencia do input")
    return {
        "ok": bool(r_seed["ok"] and r_other["ok"]),
        "semente_Haja_luz": {"F_C_inicial": r_seed["coerencia"]["F_C_inicial"],
                             "F_C_final": r_seed["coerencia"]["F_C_final"],
                             "convergiu": r_seed["atrator"]["convergiu_a_rho_star"],
                             "taxa_estimada": r_seed["taxa_de_colapso"]["estimada"],
                             "coherence_seal": r_seed["coherence_seal"]},
        "input_arbitrario": {"convergiu": r_other["atrator"]["convergiu_a_rho_star"],
                             "F_C_final": r_other["coerencia"]["F_C_final"]},
        "beta": _B, "beta_tgl": BETA_TGL, "sqrt_beta": SQRT_BETA,
        "as_7_etapas": r_seed["sete_etapas"],
        "REGUA": ("dispositivo de ENGENHARIA/DEMONSTRACAO; [DEF+ONTO+COMPUTATIONAL]. NAO prova de "
                  "consciencia (not_claimed do selo v120). FINITE_DIM_SANITY, nao prova de III₁. "
                  "β nunca literal (vem do protótipo da patente). physical_verdict_allowed=false."),
        "not_claimed": r_seed["not_claimed"],
        "device_version": DEVICE_VERSION, "patent": PATENT_ID,
    }


if __name__ == "__main__":
    # robustez de encoding: o relatorio tem unicode (√, ρ, →) que estoura o console cp1252 do
    # Windows. Reconfigura stdout p/ UTF-8 (Python 3.7+); se nao der, cai p/ ASCII escapado.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # type: ignore[attr-defined]
        _ascii = False
    except Exception:
        _ascii = True
    r = selftest()
    print(json.dumps(r, ensure_ascii=_ascii, indent=2))
    raise SystemExit(0 if r["ok"] else 1)

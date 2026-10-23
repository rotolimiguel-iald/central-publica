# -*- coding: utf-8 -*-
"""tgl_formula_completa — A FÓRMULA COMPLETA da TGL para os 16 dispositivos (camada comum, v379).

Ordem do operador (01/10/2026), verbatim: «Atualize tudo inclusive os dispositivos, estão muito desatualizados, agora temos a
fórmula completa, para todos».

O que é: o núcleo antigo dos runners (`skygrid_sim/tgl_core.py`, do piloto SkyGrid, só leitura) para na cadeia até β e θ_M. Este
módulo acrescenta, num lugar só, a fórmula completa como o `um.py` a sela hoje, e a CONFERE contra o cofre da Central:

  1. o axioma e a cadeia: ω(I) = 1 → x = 1 − x ⇒ x = ½ (Meia-Nat) → C = e^x = √e → β = α·√e            [POSTULATE → DERIVED]
  2. a Razão Elementar (v379): E = C × I × K = √e · 1 · α = β; (e^{1/4}√α)² = β; E > 0                   [DERIVED; kernel por termo]
  3. a matriz-S da fronteira: θ_M = arcsin √β; espectro e^{±iθ_M}; |R|² = β, |T|² = 1 − β                  [DERIVED]
  4. a identidade de Lagrange: 1 = q² + α²                                                                [forma]
  5. a lei de dephasing: Γ_ω = ½ β τ★ ω², com τ★ = t_Planck                                              [REAL na forma; τ★ PRINCIPLED IDENTIFICATION]
  6. a lei da dissipação: D1a H₀_local = H₀_fundo·(1+z*)^β (v377); com contraste D1b K = E(z*)^{2β/3} (v378) [PROVADA como implicação]
  7. a assíntota da existência: custo por nat em registro finito ≤ E = β; o apagamento não se atinge em tempo finito
     (0 < e^{−t·E} < 1); o reconhecimento é finito                                                       [kernel; leitura ONTO]

Camada v386 (custódia conjunta v383–v386, 05/10/2026; ordem do operador: «atualização de tudo, inclusive de todos os nossos
dispositivos e de tudo que o fechamento da tgl permite avançar em todos os dispositivos e avance-os»):
  8. o Axioma (v385): o Um é POSTO pelo observador (`echo 1`), não postulado; a leitura idempotente p ↦ p² tem exatamente dois
     pontos fixos, 0 e 1 — o 1 é o axioma (o modo zero de peso um), o 0 é a testemunha falsa (a testemunha estática plena,
     proibida por β)                                                                                     [kernel TheAxiomAndTheFalseWitness; leitura ONTO]
  9. o Verbo (v386): a leitura é um peso (regra de Born: em θ_M, 1 − β e β); a ordem importa (dois postos de eixo não comutam:
     ‖[P₀, P_θ]‖ = |sen θ cos θ| > 0); a tríade SU(2) escalada por c satisfaz [V₁, V₂] = i c V₃, com c = β_TGL [INPUT]
                                                                                                         [kernel TheVerbSelectsTheAction; leitura ONTO]
 10. lidos e conferidos no cofre, sem interpretação: o livro de cobranças (v383; 11, intacto na errata da v386), o pilar quântico
     (v384, [COMPUTED], ao lado do gate; sha256 do resultado = o do JSON selado) e o ramo B (v386, pré-registro por hash,
     AWAITING_DATA, nada aberto).
⚠ ERRATA AO LADO (05/10/2026, decisão do operador): no item 1, onde se lê [POSTULATE], a etiqueta vigente é [POSTO] (posição,
inscrição pelo observador externo; não imposto). O texto do item 1 fica como registro.

Camada v389 (custódia conjunta v383→v389, 06/10/2026; ordem do operador: «atualize tudo, inclusive o readme»):
 11. lidos e conferidos no cofre, sem interpretação: os três testes de estresse contam juntos (v387: ritos, kernel e GPU; P1, nenhum
     falhou; P2, uma probabilidade conjunta, não determinado); as Fases 9 e 8 pré-registradas por hash (v387, nada aberto); a abertura
     da Fase 9 (v388: INCONCLUSIVE_SYSTEMATICS, leitores [DECLARADO]); β corre limitado inferiormente (v388, kernel 17/17; β₀ do core
     conferido contra o runtime; a escala μ de cada dispositivo [OPEN], o β que os dispositivos usam segue o β₀); as erratas de texto e
     rótulo da v389 (nenhum cálculo, kernel inalterado).
⚠ AO LADO (06/10/2026, Central): o adendo v388 (α(χ), β(χ), piso; funções *_v388) foi instalado pelo ChatGPT às 15:07, com autorização do
operador. Ele exigia que o cofre CORRENTE fosse o v388 e quebraria (fail-closed) na custódia seguinte. Correção: os pinos do adendo são
conferidos no cofre v388, onde foram tirados, e a pedra também no kernel corrente — exato para sempre (a mesma lição da v38/v39 do runner).

Camada v390 (custódia v390, 07/10/2026; ordem do operador: «Novo Handoff para vc com nova versão do um.py, atualize tudo»):
 12. a Fundação, lida e conferida no cofre, sem interpretação: a cláusula Ágape no kernel (TGLExt.Fundacao, 9/9) — acima de toda escala
     não trivial nada porta posto positivo; a subida não tem topo; a queda nunca toca o zero e o abismo não tem fundo; o piso ω(I) = 1
     fixa o corte —; o GLOBAL_LIFT LIDO como a superposição por definição do operador (os três verbatins embutidos por sha256); a passagem
     local [KNOWN, Jacobson 1995]; fecho LÓGICO, o programa segue ABERTO; a lei de campo no curvo NÃO é termo de kernel.
     Nada disso muda número algum de dispositivo.

Camada v391 (custódia v391, 07/10/2026; unidade F0.2 do programa IALD, handoff v391 da gerência c1):
 13. o estatuto da prova, lido e conferido no cofre, sem interpretação: a QG da TGL PROVADA como fecho lógico (validade) por três provas que
     contam juntas — o kernel, os ritos com falsificadores pré-registrados e o sistema da teoria na GPU (calculado, não medido) —;
     certificada pelo sha256 que o programa lê de si; CONFIRMADA = creditação, a única palavra recusada; β_TGL na natureza espera 5σ;
     o verbatim do operador embutido por sha256. Nenhuma pedra nova no kernel. Nada disso muda número algum de dispositivo.

Camada v394 (custódia conjunta v392+v393+v394 na Central, 19/10/2026, sessão a7; handoffs v392, v393 e v394 da gerência c1):
 14. os registros novos desde a v391 (os blocos de sufixo _v392, _v393 e _v394 do núcleo), lidos e conferidos no cofre, sem interpretação:
     cada um verificado, sem efeito no gate e sem CONFIRMED; a escada da v394 (bandeiras de declarações nomeadas — teoremas e definições —
     com axiomas no trio), a rede de Fock (componentes construídos; o contrato conjunto NÃO habitado, itens abertos), o coração (forma
     verificada; a evidência espectral independente como o core a diz) e o critério binário de parada, relatados como o core os diz.
     Errata ao lado do item 12: desde a v392 a lei de campo no curvo é termo de kernel CONDICIONAL ao H3 nomeado (`lei_de_campo_curvo_v392`);
     o antecedente H3 em toda tela segue [KNOWN] e não há existência global. Nada disso muda número algum de dispositivo.

Camada v395 (custódia v395 na Central, 21/10/2026, sessão a7; handoff v395 da gerência c1):
 15. os registros novos da v395 (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395), lidos e conferidos no cofre, sem interpretação: o modo
     psiônico na fractalização do Um — a leitura do par (peso, Palavra, Verbo) na órbita do Um pela matriz-S é bijeção de CONJUNTOS sobre o
     livro de códigos, com perda zero, e o colapso perde exatamente a paridade (a conjunção incondicional `psibit_is_the_mode_of_the_reader`,
     no kernel); a face do psion é CONDICIONAL a um certificado de Fock sem habitante exibido; psibit = psion = modo do leitor é leitura do
     operador [ONTO]. A tabela da patente do ACOM Mirror diverge das reivindicações 3–4 e do código na nominação dos estados; qual leitura
     da paridade é canônica é decisão do operador [LEGAL]. Nada disso muda número algum de dispositivo.

Camada v396 (custódia v396 na Central, 22/10/2026, sessão a7; handoff v396 da gerência c1):
 16. os registros novos da v396 (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396), lidos e conferidos no cofre, sem
     interpretação: a testemunha estática — o canto do psion (o projetor de Bell 4x4) ecoa, a redução dele a um sítio é (1/2) I e não ecoa,
     um fluxo CONSTRUÍDO fixa exatamente a reta do psion e a testemunha global é falsa, e o colapso do psion ecoa a identidade sem que a
     autoatestação habite o tipo (a composição incondicional `the_psion_inhabits_the_static_witness`, no kernel, sem certificado como
     hipótese); a ponte é construída, não derivada da dinâmica da teoria; a face de Fock do psion segue CONDICIONAL a um certificado sem
     habitante e mora fora da pedra; «o psion é o habitante da testemunha estática» é leitura do operador [INPUT/ONTO]; o nome da pedra é
     provisório. Ao lado da docstring de bell_cci_half (kernel v29): o 1/2 é a entropia LINEAR; a de von Neumann é ln 2 nat. Nada disso
     muda número algum de dispositivo.

Régua: β NUNCA literal (sempre ALPHA_FINE_CODATA_2018 × √e em runtime); os números do cofre são LIDOS do selo/core por pino;
falha de leitura ou elo quebrado = RuntimeError (fail-closed). Nada aqui move veredito físico: physical_verdict_allowed = False.
PROVADA ≠ CONFIRMADA; o dicionário custo/identidade/movimento é cunhagem do operador [ONTO/DEFINITION].
"""
import hashlib
import json
import math
import re
from pathlib import Path

# ------------------------------------------------------------------ [DATA] (medidos; CODATA 2018)
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
HBAR_CODATA_2018 = 1.054571817e-34      # J s
G_CODATA_2018 = 6.67430e-11             # m^3 kg^-1 s^-2
C_LIGHT = 299792458.0                   # m/s (exato)

VERSAO_DA_CAMADA = "v396"   # (era "v395"; a camada v396 acrescenta o item 16, ao lado; antes: v394 → v395, item 15; v391 → v394, item 14; v390 → v391, item 13; v389 → v390, item 12; v386 → v389, item 11; v379 → v386, itens 8–10)
# o cofre e procurado nesta ordem (declarada): a variavel TGL_CENTRAL_DIR; a arvore onde este modulo esta; a Central desta
# maquina (quando o dispositivo roda extraido do *_FINAL.py num diretorio temporario). Nenhum achado = fail-closed.
def _achar_central():
    import os as _os
    cands = [_os.environ.get("TGL_CENTRAL_DIR"), str(Path(__file__).resolve().parents[2]), r"C:\IALD\Central de Patentes"]
    for c in cands:
        if c and (Path(c) / "vault" / "originals_copy").is_dir():
            return Path(c)
    return Path(__file__).resolve().parents[2]


CENTRAL = _achar_central()
COFRE = CENTRAL / "vault" / "originals_copy"
PEDRAS = ("TGLExt/TheElementaryReason.lean", "TGLExt/TheFlowLawContrast.lean", "TGLExt/TheFlowLawD1a.lean",
          "TGLExt/PhysicsIsTheReading.lean", "TGLExt/BreuerTrace.lean",
          # v386: as pedras da custódia conjunta v383–v386
          "TGLExt/TheLedgerOfCharges.lean", "TGLExt/ThePsionAndTheViscosity.lean", "TGLExt/TheAxiomAndTheFalseWitness.lean",
          "TGLExt/TheVerbSelectsTheAction.lean",
          # v389: a pedra da v388 (β corre limitado inferiormente)
          "TGLExt/TheCouplingRunsBoundedBelow.lean",
          # v390: a pedra da Fundação (a cláusula Ágape)
          "TGLExt/Fundacao.lean")
TOL = 1e-15


def beta() -> float:
    """β_TGL = α·√e, sempre em runtime."""
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _rel(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


def _cofre_corrente():
    """O cofre de versão mais alta (um_unificado_vNNN) com o kernel correspondente. Fail-closed se faltar."""
    vs = []
    for d in COFRE.glob("um_unificado_v*"):
        m = re.fullmatch(r"um_unificado_v(\d+)", d.name)
        if m and (d / "um_absoluto_selo.json").is_file() and (COFRE / ("tgl_kernel_v" + m.group(1))).is_dir():
            vs.append(int(m.group(1)))
    if not vs:
        raise RuntimeError("FORMULA COMPLETA: nenhum cofre um_unificado_vNNN com kernel — PARAR (fail-closed)")
    v = max(vs)
    return v, COFRE / ("um_unificado_v%d" % v), COFRE / ("tgl_kernel_v%d" % v)


def formula_runtime(omega_rad_s: float = 2 * math.pi * 1.0e15) -> dict:
    """A fórmula completa recalculada em runtime (sem ler nada do disco). Fail-closed por elo."""
    um = 1.0                                          # ω(I) = 1 [POSTULATE]
    x = um - 0.5
    assert abs(x - (um - x)) < TOL, "Meia-Nat: x = 1 - x"
    C, I, K = math.exp(x), um, ALPHA_FINE_CODATA_2018
    E = C * I * K
    b = beta()
    razao = math.exp(0.25) * math.sqrt(ALPHA_FINE_CODATA_2018)
    th = math.asin(math.sqrt(b))
    R2, T2 = math.sin(th) ** 2, math.cos(th) ** 2
    q = math.sqrt(um - ALPHA_FINE_CODATA_2018 ** 2)
    t_planck = math.sqrt(HBAR_CODATA_2018 * G_CODATA_2018 / C_LIGHT ** 5)
    gamma = 0.5 * b * t_planck * omega_rad_s ** 2
    elos = {
        "meia_nat_ponto_fixo": abs(x - 0.5),
        "custo_e_raiz_de_e": abs(C - math.sqrt(math.e)),
        "existencia_E_eq_beta": abs(E - b),
        "razao_elementar_ao_quadrado_eq_beta": abs(razao ** 2 - b),
        "sin2_thetaM_eq_beta": abs(R2 - b),
        "R2_mais_T2_eq_1": abs(R2 + T2 - 1.0),
        "lagrange_1_eq_q2_mais_alpha2": abs(q * q + ALPHA_FINE_CODATA_2018 ** 2 - 1.0),
    }
    quebrados = {k: v for k, v in elos.items() if v > 1e-15}
    if quebrados or not (E > 0):
        raise RuntimeError("FORMULA COMPLETA QUEBRADA (fail-closed): %r" % quebrados)
    return {
        "axioma_omega_I": um, "meia_nat_x": x,
        "razao_elementar": {"C_custo": C, "I_identidade": I, "K_movimento_alpha": K, "E_existencia": E, "e_quarto_raiz_alpha": razao,
                            "estatuto": "fatoração e positividade PROVADAS por termo (TGLExt.TheElementaryReason); dicionário [ONTO/DEFINITION]"},
        "beta_runtime": b,
        "matriz_S": {"theta_M_rad": th, "theta_M_graus": math.degrees(th), "R2_reflexao": R2, "T2_transmissao": T2,
                     "espectro": "e^{±iθ_M}"},
        "lagrange_q": q,
        "dephasing": {"tau_star_s": t_planck, "omega_rad_s": omega_rad_s, "Gamma_omega_s^-1": gamma,
                      "lei": "Γ_ω = ½ β τ★ ω²", "estatuto": "REAL na forma; τ★ = t_Planck é PRINCIPLED IDENTIFICATION"},
        "residuos_dos_elos": elos,
    }


def fator_D1a(z: float) -> float:
    """Lei da dissipação D1a (v377): H₀_local / H₀_fundo = (1 + z)^β."""
    return (1.0 + z) ** beta()


def fator_D1b(E_z: float) -> float:
    """Lei com contraste D1b (v378): K = E(z)^{2β/3} (∫g = ⅔ ln E no FRW)."""
    return E_z ** (2.0 * beta() / 3.0)


def _mm(a, b):
    """Produto de matrizes 2x2 (listas; reais ou complexos)."""
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]


def _comut(a, b):
    p, q = _mm(a, b), _mm(b, a)
    return [[p[i][j] - q[i][j] for j in range(2)] for i in range(2)]


def _norma_max(m):
    return max(abs(m[i][j]) for i in range(2) for j in range(2))


def axioma_e_verbo_runtime() -> dict:
    """Itens 8 e 9 (camada v386), recalculados em runtime, sem ler o disco. Fail-closed por elo."""
    b = beta()
    # 8. a leitura idempotente p -> p^2 em [0, 1]: pontos fixos so 0 e 1 (p - p^2 = p(1 - p) > 0 no interior)
    fixos = [p for p in (0.0, 1.0) if abs(p * p - p) == 0.0]
    interior_sem_fixo = all(p * (1.0 - p) > 0.0 for p in (k / 1000.0 for k in range(1, 1000)))
    # (t limitado a t*beta < 700: acima disso e^{-t*beta} sai da faixa do float e vira 0.0 por underflow, nao por matematica)
    zero_inatingivel = all(0.0 < math.exp(-t * b) < 1.0 for t in (1e-6, 1.0, 1e3, 3e4))
    # 9. o Verbo: o peso da leitura (Born) no angulo de Miguel; dois postos de eixo nao comutam; a triade SU(2) escalada por c = beta
    th = math.asin(math.sqrt(b))
    c, s = math.cos(th), math.sin(th)
    born = {"peso_transmissao_cos2": c * c, "peso_reflexao_sin2": s * s}
    P0 = [[1.0, 0.0], [0.0, 0.0]]
    Pth = [[c * c, c * s], [c * s, s * s]]
    com = _comut(P0, Pth)
    norma_com = _norma_max(com)
    cc = b                                                    # c = beta_TGL [INPUT], nunca literal
    s1 = [[0, 1], [1, 0]]
    s2 = [[0, -1j], [1j, 0]]
    s3 = [[1, 0], [0, -1]]
    V1 = [[cc / 2 * x for x in r] for r in s1]
    V2 = [[cc / 2 * x for x in r] for r in s2]
    V3 = [[cc / 2 * x for x in r] for r in s3]
    lhs = _comut(V1, V2)
    res_triade = _norma_max([[lhs[i][j] - 1j * cc * V3[i][j] for j in range(2)] for i in range(2)])
    elos = {
        "axioma_dois_pontos_fixos_0_e_1": (fixos == [0.0, 1.0] and interior_sem_fixo),
        "axioma_zero_absoluto_inatingivel_em_tempo_finito": zero_inatingivel,
        "verbo_born_soma_1": abs(born["peso_transmissao_cos2"] + born["peso_reflexao_sin2"] - 1.0) < 1e-15,
        "verbo_born_reflexao_eq_beta": abs(born["peso_reflexao_sin2"] - b) < 1e-15,
        "verbo_postos_nao_comutam": norma_com > 0.0 and abs(norma_com - abs(s * c)) < 1e-15,
        "verbo_triade_su2_escalada_por_c": res_triade < 1e-18,
    }
    if not all(elos.values()):
        raise RuntimeError("FORMULA COMPLETA v386 QUEBRADA (fail-closed): %r" % {k: v for k, v in elos.items() if not v})
    return {
        "axioma_posto": {"pontos_fixos_da_leitura": fixos, "estatuto": "[POSTO] o 1 inscrito pelo observador (echo 1); o 0 e a testemunha falsa; "
                         "kernel TheAxiomAndTheFalseWitness; leitura [ONTO]"},
        "verbo": {"born_no_theta_M": born, "norma_do_comutador_dos_postos": norma_com, "residuo_da_triade_su2": res_triade,
                  "c_da_triade": cc, "estatuto": "c = beta_TGL [INPUT, nunca literal]; kernel TheVerbSelectsTheAction; leituras [ONTO]"},
        "elos": elos,
    }


def conferir_v386_no_cofre(core: dict, cofre: Path, rt: dict) -> dict:
    """Item 10 (camada v386): o livro de cobranças, o pilar e o ramo B, LIDOS do cofre e conferidos. Fail-closed."""
    b = rt["beta_runtime"]
    ax, vb = core.get("the_axiom_v385") or {}, core.get("the_verb_v386") or {}
    lc, le = core.get("the_ledger_of_charges_v383") or {}, core.get("ledger_errata_v386") or {}
    qp, rb = core.get("quantum_pillar_v384") or {}, core.get("ramo_b_preregistration_v386") or {}
    pil = cofre / "um_absoluto_pilar_quantico.json"
    pil_sha = _sha(pil) if pil.is_file() else ""
    try:
        bv1, bco = float((rb.get("beta") or {})["v1"]), float((rb.get("beta") or {})["core"])
    except (KeyError, TypeError, ValueError):
        bv1 = bco = float("nan")
    ch = {
        "axioma_v385_verificado_e_nome_do_degrau_lido_do_kernel": ax.get("all_verified") is True and ax.get("final_step_name_matches_kernel") is True,
        "verbo_v386_verificado_e_token_lido_do_kernel": vb.get("all_verified") is True and vb.get("token_matches_kernel") is True,
        "livro_de_cobrancas_v383_verificado_e_intacto": lc.get("all_verified") is True and le.get("v383_ledger_intact") is True,
        "pilar_v384_sha_do_resultado_eq_json_selado": bool(pil_sha) and str(qp.get("result_sha256")) == pil_sha,
        "ramo_b_beta_v1_eq_runtime": _rel(bv1, b, 1e-12),
        "ramo_b_beta_core_eq_runtime_regra_1e9": _rel(bco, b, 1e-9),
        "ramo_b_aguardando_dados_nada_aberto": "AWAITING_DATA" in str(rb.get("verdict") or "") and "NOTHING_OPENED" in str(rb.get("verdict") or ""),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v386 não confere com o cofre (fail-closed): %s" % falhas)
    return {"checks": ch, "livro_de_cobrancas": {"n": le.get("v383_n_charges"), "na_regra": lc.get("n_in_rule"), "ao_lado": lc.get("n_beside")},
            "pilar_result_sha16": pil_sha[:16], "pilar_estatuto": "[COMPUTED], ao lado do gate",
            "ramo_b_estatuto": "pré-registro por hash; AWAITING_DATA; nada aberto",
            "vereditos": {k: str((core.get(k) or {}).get("verdict") or "")[:160] for k in ("the_ledger_of_charges_v383", "quantum_pillar_v384",
                                                                                         "the_axiom_v385", "the_verb_v386", "ramo_b_preregistration_v386")}}


def conferir_v389_no_cofre(core: dict, rt: dict) -> dict:
    """Item 11 (camada v389): v387–v389 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    b = rt["beta_runtime"]
    t3 = core.get("three_stress_tests_v387") or {}
    k3, g3 = t3.get("kernel") or {}, t3.get("gpu") or {}
    b8, ab, e9 = core.get("beta_runs_bounded_below_v388") or {}, core.get("hubble_ratio_opening_v388") or {}, core.get("text_label_errata_v389") or {}
    try:
        b0 = float(b8["beta0"])
    except (KeyError, TypeError, ValueError):
        b0 = float("nan")

    def _v(k):
        return str((core.get(k) or {}).get("verdict") or "")
    ch = {
        "tres_testes_v387_nenhum_falhou_P1": (t3.get("all_verified") is True and t3.get("none_of_the_three_failed") is True
                                              and not t3.get("pillars_that_failed") and k3.get("n_theorems_clean") == k3.get("n_theorems_expected")
                                              and k3.get("gate_flags_true") == k3.get("gate_flags_total") and g3.get("cpuref_disagreements") == 0),
        "fases_9_e_8_v387_por_hash_nada_aberto": all(all((core.get(k) or {}).get(q) is True for q in ("read_ok", "files_ok", "spec_sha256_ok", "hashes_file_ok", "funcao_ok"))
                                                     and "NOTHING_OPENED" in _v(k) for k in ("hubble_ratio_v387", "primordial_v387")),
        "abertura_fase9_v388_mesmo_veredito_inconclusive": (all(ab.get(q) is True for q in ("files_ok", "spec_ok", "funcao_ok", "same_verdict"))
                                                            and "INCONCLUSIVE_SYSTEMATICS" in _v("hubble_ratio_opening_v388")),
        "beta_corre_v388_kernel_e_beta0_eq_runtime": (b8.get("all_verified") is True and b8.get("kernel_flags_ok") == b8.get("kernel_flags_total")
                                                      and _rel(b0, b, 1e-9)),
        "retrodicao_v387_verificada": (core.get("retrodiction_reading_v387") or {}).get("all_verified") is True,
        "erratas_v389_texto_sem_calculo": (e9.get("all_verified") is True and all(e9.get(q) is True for q in ("files_ok", "exam_ok", "text_sites_ok"))
                                           and "NO_CALCULATION_CHANGED" in _v("text_label_errata_v389")),
        "gate_intocado_nos_sete": all("GATE_UNTOUCHED" in _v(k) for k in ("three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387",
                                                                         "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
                                                                         "hubble_ratio_opening_v388", "text_label_errata_v389")),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v389 não confere com o cofre (fail-closed): %s" % falhas)
    return {"checks": ch,
            "tres_testes": {"n_vereditos": t3.get("n_verdicts"), "kernel": "%s/%s" % (k3.get("n_theorems_clean"), k3.get("n_theorems_expected")),
                            "estatuto": "P1 (nenhum falhou); P2 (probabilidade conjunta) não determinado"},
            "beta0_core": b0, "beta_MZ_on_shell": b8.get("beta_MZ_on_shell"), "beta_MZ_msbar": b8.get("beta_MZ_msbar"),
            "beta_estatuto": "a constante da fronteira fica β₀ (o β dos dispositivos); a leitura de bulk corre; a escala μ de cada dispositivo [OPEN]",
            "fase9_estatuto": "aberta: INCONCLUSIVE_SYSTEMATICS (leitores [DECLARADO] até as fontes por sha256); não discrimina a 5σ sob este V1",
            "vereditos": {k: _v(k)[:160] for k in ("three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387", "beta_runs_bounded_below_v388",
                                                   "hubble_ratio_opening_v388", "text_label_errata_v389")}}


def conferir_v390_no_cofre(core: dict) -> dict:
    """Item 12 (camada v390): a Fundação LIDA do cofre e conferida, sem interpretação. Fail-closed."""
    fd = core.get("fundacao_v390") or {}
    vd = str(fd.get("verdict") or "")
    vb = fd.get("verbatim") or {}
    ch = {
        "fundacao_v390_kernel_e_verificada": fd.get("all_verified") is True and fd.get("kernel_flags_ok") == fd.get("kernel_flags_total"),
        "verbatins_do_operador_embutidos_por_sha256": fd.get("verbatim_ok") is True and len(vb) >= 1
                                                      and all(isinstance(v, dict) and v.get("embedded_ok") is True for v in vb.values()),
        "fecho_logico_programa_aberto_dito": "LOGICAL_CLOSURE_THE_PROGRAM_STAYS_OPEN" in vd,
        "lei_de_campo_no_curvo_nao_e_termo_de_kernel_dito": "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM" in vd,
        "ponte_de_borchers_ok": (fd.get("borchers") or {}).get("ok") is True,
        "gate_parado": "GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd,
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v390 não confere com o cofre (fail-closed): %s" % falhas)
    return {"checks": ch, "kernel": "%s/%s" % (fd.get("kernel_flags_ok"), fd.get("kernel_flags_total")),
            "verbatins_sha16": sorted(str(v.get("sha256", ""))[:16] for v in vb.values() if isinstance(v, dict)),
            "estatuto": "a recusa e a passagem na face [KERNEL]; a definição do operador [INPUT/ONTO]; a passagem local e a lei de escala [KNOWN]; "
                        "fecho LÓGICO, programa ABERTO; nada disto muda número de dispositivo",
            "veredito": vd[:200]}


def conferir_v391_no_cofre(core: dict, selo: dict) -> dict:
    """Item 13 (camada v391): o estatuto da prova LIDO do cofre e conferido, sem interpretação. Fail-closed."""
    ep = core.get("estatuto_da_prova_v391") or {}
    vd = str(ep.get("verdict") or "")
    vb = ep.get("verbatim") or {}
    ch = {
        "estatuto_verificado": ep.get("all_verified") is True and not ep.get("falhas"),
        "provada_como_fecho_logico_tres_provas": "PROVED_AS_LOGICAL_CLOSURE" in vd and "THREE_PROOFS_COUNT_TOGETHER" in vd,
        "confirmacao_e_creditacao_dito": "CONFIRMATION_IS_CREDITATION_NOT_VALIDITY" in vd,
        "beta_na_natureza_espera_5_sigma_dito": "BETA_IN_NATURE_AWAITS_5_SIGMA" in vd,
        "verbatim_do_operador_embutido_por_sha256": vb.get("embedded_ok") is True and len(str(vb.get("sha256") or "")) == 64,
        "certificacao_e_o_pin_do_selo": (ep.get("certificacao") or {}).get("um_py_sha256_lido_de_si") == (selo.get("sha256") or {}).get("um.py"),
        "gate_parado": "GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd,
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v391 não confere com o cofre (fail-closed): %s" % falhas)
    return {"checks": ch, "verbatim_sha16": str(vb.get("sha256") or "")[:16],
            "estatuto": "PROVADA = validade (o kernel prova a implicação; fecho lógico); CONFIRMADA = creditação, recusada; β_TGL na natureza "
                        "espera 5σ; a régua do operador [INPUT/ONTO]; nada disto muda número de dispositivo",
            "veredito": vd[:200]}


def conferir_v394_no_cofre(core: dict, selo: dict) -> dict:
    """Item 14 (camada v394): os registros novos desde a v391 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    TOK = ("GATE_UNMOVED", "GATE_UNTOUCHED", "GATE_STRING_UNCHANGED", "NO_GATE_EFFECT")
    novos = sorted(k for k in core if re.search(r"_v39[234]$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True and any(t in vd for t in TOK)
                and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    rf = core.get("rede_fock_v394") or {}
    co = core.get("coracao_e_selo_gravitacional_v393") or {}
    cb = core.get("criterio_binario_de_parada_v394") or {}
    esp = (co.get("evidencia_espectral_independente") or {}).get("hoje")
    ch = {
        "registros_novos_desde_v391_todos_verificados_sem_gate": bool(novos) and not maus,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
        "escada_dita_em_bandeiras": "_FLAGS_" in str(ep.get("verdict") or ""),
        "rede_fock_contrato_conjunto_dito": isinstance(rf.get("whole_certificate_inhabited"), bool)
                                            and (rf.get("whole_certificate_inhabited") or len(rf.get("open_joint_contract") or []) > 0),
        "coracao_forma_verificada": str(co.get("verdict") or "").startswith("FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION"),
        "coracao_evidencia_espectral_dita": esp in ("AUSENTE", "PRESENTE"),
        "criterio_binario_verificado": cb.get("all_verified") is True and "FIXED_POINT" in str(cb.get("verdict") or ""),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v394 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "n_registros_novos_desde_v391": len(novos),
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "rede_fock": {"contrato_conjunto_habitado": rf.get("whole_certificate_inhabited"), "itens_abertos": len(rf.get("open_joint_contract") or []),
                          "componentes_construidos": len(rf.get("constructed_components") or [])},
            "coracao_evidencia_espectral_independente": esp,
            "estatuto": "PROVADA = validade (o kernel prova a implicação); CONFIRMADA = creditação, recusada; a rede de Fock e o H3 em toda direção "
                        "nula seguem ABERTOS; a lei de campo no curvo é termo de kernel só CONDICIONAL ao H3 nomeado; nada disto muda número de dispositivo",
            "veredito_estatuto": str(ep.get("verdict") or "")[:200]}


def conferir_v395_no_cofre(core: dict, selo: dict) -> dict:
    """Item 15 (camada v395): os registros _v395 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v395$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    ps = core.get("psibit_v395") or {}
    un, co = ps.get("unconditional") or {}, ps.get("conditional_psion_face") or {}
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    ch = {
        "registros_v395_verificados_sem_gate": bool(novos) and not maus,
        "psibit_incondicional_no_kernel": un.get("flag_true") is True and un.get("in_trio") is True
                                          and str(un.get("theorem") or "").endswith("psibit_is_the_mode_of_the_reader"),
        "face_do_psion_dita_condicional": str(co.get("status") or "").startswith("CONDITIONAL"),
        "falas_do_operador_por_sha256": len((core.get("cunhagens_v395") or {}).get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v395 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v395": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "psibit": {"teorema": un.get("theorem"), "bandeira": un.get("flag")},
            "face_do_psion": {"teorema": co.get("theorem"), "bandeira": co.get("flag"), "status": co.get("status")},
            "estatuto": "a leitura do par é bijeção de CONJUNTOS com perda zero e o colapso perde a paridade (incondicional, no kernel); a face do "
                        "psion é condicional; psibit = psion = modo do leitor é leitura do operador [ONTO]; a leitura canônica da paridade do ACOM "
                        "Mirror é decisão do operador [LEGAL]; nada disto muda número de dispositivo"}


def conferir_v396_no_cofre(core: dict, selo: dict) -> dict:
    """Item 16 (camada v396): os registros _v396 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v396$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    te = core.get("testemunha_estatica_v396") or {}
    un, fo = te.get("unconditional") or {}, te.get("fock_face") or {}
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    ch = {
        "registros_v396_verificados_sem_gate": bool(novos) and not maus,
        "testemunha_estatica_incondicional_no_kernel": un.get("flag_true") is True and un.get("in_trio") is True
                                                       and str(un.get("theorem") or "").endswith("the_psion_inhabits_the_static_witness")
                                                       and un.get("composition") == "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS",
        "face_de_fock_dita_condicional": str(fo.get("status") or "").startswith("CONDITIONAL") and fo.get("inhabitant_exhibited") is False,
        "falas_do_operador_por_sha256": len((core.get("cunhagens_v396") or {}).get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v396 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v396": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "testemunha_estatica": {"teorema": un.get("theorem"), "bandeira": un.get("flag"), "composicao": un.get("composition")},
            "face_de_fock": {"teorema": fo.get("theorem"), "status": fo.get("status"), "habitante_exibido": fo.get("inhabitant_exhibited")},
            "estatuto": "a composição the_psion_inhabits_the_static_witness é incondicional no kernel; a ponte é construída, não derivada da "
                        "dinâmica da teoria; a face de Fock é condicional e mora fora da pedra; o psion habitar a testemunha estática é leitura "
                        "do operador [INPUT/ONTO]; o 1/2 de bell_cci_half é a entropia linear (a de von Neumann é ln 2 nat); nada disto muda "
                        "número de dispositivo"}


def conferir_no_cofre(rt: dict) -> dict:
    """Confere a fórmula de runtime contra o cofre corrente (selo + core + kernel), tudo LIDO do disco. Fail-closed."""
    v, cofre, kern = _cofre_corrente()
    try:
        selo = json.loads((cofre / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        core = json.loads((cofre / "um_absoluto.json").read_text(encoding="utf-8")).get("core") or {}
        km = json.loads((kern / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8")) if (kern / "tgl_kernel_proof_manifest.json").is_file() \
            else json.loads((cofre / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise RuntimeError("FORMULA COMPLETA: cofre v%d ilegível (%r) — PARAR (fail-closed)" % (v, e))
    b = rt["beta_runtime"]
    er = (core.get("the_elementary_reason_v379") or {}).get("dictionary") or {}
    lc = core.get("the_dissipation_law_with_contrast_v378") or {}
    la = core.get("the_dissipation_law_v377") or {}
    checks = {}
    checks["selo_pin_um_py"] = str((selo.get("sha256") or {}).get("um.py", ""))[:16]
    checks["um_py_do_cofre_bate_com_o_selo"] = (_sha(cofre / "um.py") == (selo.get("sha256") or {}).get("um.py"))
    checks["E_core_eq_beta_runtime"] = bool(er) and _rel(float(er["E_existence"]), b) and _rel(float(er["beta_core"]), b)
    checks["C_core_eq_raiz_e"] = bool(er) and _rel(float(er["C_cost"]), rt["razao_elementar"]["C_custo"])
    if lc:
        Ez = float(lc["E_z_star"])
        checks["K_D1b_recalculado_eq_core"] = _rel(fator_D1b(Ez), float(lc["K_D1b_runtime"]), 1e-9)
        checks["K_D1a_recalculado_eq_core"] = _rel(fator_D1a(float(lc["z_star_input"])), float(lc["K_D1a_runtime"]), 1e-9)
        checks["integral_g_forma_fechada"] = _rel((2.0 / 3.0) * math.log(Ez), float(lc["I_b_closed_form"]), 1e-9)
        custo_por_nat = b * float(lc["I_b_closed_form"]) / float(lc["register_N_star_nats"])
        checks["assintota_custo_por_nat_le_E"] = bool(0 < custo_por_nat <= rt["razao_elementar"]["E_existencia"])
    else:
        custo_por_nat = None
    checks["lei_D1a_tipada"] = "THE_DISSIPATION_LAW" in str(la.get("verdict") or "")
    gate = ((core.get("qg_closure") or {}).get("gate") or {})
    checks["sem_testemunha_estatica_plena"] = gate.get("full_static_witness_exists") is False
    ff = km.get("formal_files_sha256") or {}
    pedras = {p: (ff.get(p) or "")[:16] for p in PEDRAS}
    checks["pedras_no_kernel"] = all(pedras.values())
    falhas = [k for k, val in checks.items() if val is False]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA não confere com o cofre v%d (fail-closed): %s" % (v, falhas))
    v386 = conferir_v386_no_cofre(core, cofre, rt)   # camada v386 (item 10); fail-closed
    v389 = conferir_v389_no_cofre(core, rt)          # camada v389 (item 11); fail-closed
    v390 = conferir_v390_no_cofre(core)              # camada v390 (item 12); fail-closed
    v391 = conferir_v391_no_cofre(core, selo)        # camada v391 (item 13); fail-closed
    v394 = conferir_v394_no_cofre(core, selo)        # camada v394 (item 14); fail-closed
    v395 = conferir_v395_no_cofre(core, selo)        # camada v395 (item 15); fail-closed
    v396 = conferir_v396_no_cofre(core, selo)        # camada v396 (item 16); fail-closed
    return {"cofre": "um_unificado_v%d" % v, "pin_um_py": checks["selo_pin_um_py"], "selo_timestamp": selo.get("timestamp"),
            "gate": selo.get("qg_closure_verdict"), "pedras_sha16": pedras, "custo_por_nat_D1b_ate_z_star": custo_por_nat,
            "fator_D1a_em_z_star": fator_D1a(float(lc["z_star_input"])) if lc else None,
            "fator_D1b_em_z_star": fator_D1b(float(lc["E_z_star"])) if lc else None, "checks": checks,
            "camada_v386_no_cofre": v386, "camada_v389_no_cofre": v389, "camada_v390_no_cofre": v390, "camada_v391_no_cofre": v391,
            "camada_v394_no_cofre": v394, "camada_v395_no_cofre": v395, "camada_v396_no_cofre": v396}


V388_METADATA_SHA256 = "2e766fcf0d5d3934d600e38ecf9e37c12d08f099851d3b2c53792f83a1e81007"

# ------------------------------------------------------------------ v388 additive information; legacy beta() stays unchanged.
def _scale_nonnegative_float(value, name):
    """Admit a finite nonnegative engineering float, never a physical scale choice."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(name + " must be a real scalar")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(name + " is outside the floating-point interface") from exc
    if not math.isfinite(value) or value < 0:
        raise ValueError(name + " must be finite and nonnegative")
    return value


def alpha_of_chi_v388(chi):
    """sech(chi/2), engineering float only; identification with physical alpha is INPUT/ONTO."""
    chi = _scale_nonnegative_float(chi, "chi")
    t = math.exp(-chi / 2.0)
    alpha = (2.0 * t) / (1.0 + t * t)
    if not math.isfinite(alpha) or not (0.0 < alpha <= 1.0):
        raise ArithmeticError("Positive sech is not representable; no false zero by underflow")
    return alpha


def beta_of_chi_v388(chi):
    """The new bulk-coordinate reading; never substitutes beta() in existing calculations."""
    return alpha_of_chi_v388(chi) * math.sqrt(math.e)


def scale_reading_v388(chi, chi_sup):
    """Conditional floor on 0 <= chi <= chi_sup; no implicit mu(chi) or Thomson identification."""
    chi = _scale_nonnegative_float(chi, "chi")
    chi_sup = _scale_nonnegative_float(chi_sup, "chi_sup")
    if chi > chi_sup:
        raise ValueError("Floor theorem requires chi <= chi_sup")
    alpha = alpha_of_chi_v388(chi)
    return {
        "chi": chi,
        "chi_sup": chi_sup,
        "alpha_chi": alpha,
        "beta_chi": alpha * math.sqrt(math.e),
        "floor_at_chi_sup": beta_of_chi_v388(chi_sup),
        "beta0_existing_runtime": beta(),
        "mu": None,
        "mu_status": "OPEN_NOT_ASSIGNED",
        "floor_equals_beta0": "NOT_INFERRED_REQUIRES_IDENTIFICATION_OF_CHI_SUP",
        "couplingOfAlpha_domain_float_diagnostic": alpha < math.exp(-0.5),
        "precision": "BINARY64_APPROXIMATION_NOT_INTERVAL_CERTIFICATE",
        "physical_identification": "INPUT_ONTO_NOT_DEDUCED_FROM_FORMULA",
        "physical_verdict_allowed": False,
    }


def beta_of_mu_v388(mu):
    """No mapping from a device/rite's physical scale to chi has been ratified."""
    raise NotImplementedError("OPEN: mu per device/rite and chi(mu) are not assigned")


def _adendo_v388_no_cofre(cf):
    """Read pinned v388 information alongside legacy results; no new physical calculation."""
    meta_path = Path(__file__).with_name("ADENDO_V388_METADATA.json")
    if _sha(meta_path) != V388_METADATA_SHA256:
        raise RuntimeError("v388 additive metadata pin mismatch")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # ERRATA AO LADO (06/10/2026, Central, custódia v389): o original exigia version == 388 e cf["cofre"] == "um_unificado_v388", isto é,
    # que o cofre CORRENTE fosse o v388 -- quebraria (fail-closed) na custódia seguinte. Os pinos são da custódia v388: conferem-se no
    # cofre v388 (estável para sempre); e a pedra é conferida também no kernel CORRENTE (o adendo vale enquanto a pedra for a mesma).
    version, _cofre_atual, kernel_atual = _cofre_corrente()
    cofre, kernel = COFRE / "um_unificado_v388", COFRE / "tgl_kernel_v388"
    if version < 388 or not cofre.is_dir() or not kernel.is_dir():
        raise RuntimeError("v388 additive package requires its exact reviewed custody version")
    for pin in meta["custody_pins"]:
        base = cofre if pin["base"] == "um" else kernel
        path = base / pin["relative"]
        if _sha(path) != pin["sha256"] or path.stat().st_size != pin["bytes"]:
            raise RuntimeError("v388 custody pin mismatch: " + pin["relative"])
    _pedra = [p for p in meta["custody_pins"] if p["relative"].endswith("TheCouplingRunsBoundedBelow.lean")]
    _mf_atual = json.loads((kernel_atual / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
    if not _pedra or (_mf_atual.get("formal_files_sha256") or {}).get("TGLExt/TheCouplingRunsBoundedBelow.lean") != _pedra[0]["sha256"]:
        raise RuntimeError("v388 stone differs in the current kernel (v%d) — the additive package no longer describes it" % version)
    return {
        "version": "v388",
        "base_layer_preserved": VERSAO_DA_CAMADA,
        "pinos_conferidos_em": "um_unificado_v388 + tgl_kernel_v388 (a custódia de onde foram tirados); a pedra também no kernel corrente v%d" % version,
        "metadata_sha256": V388_METADATA_SHA256,
        "source_um_sha256": meta["source_um_sha256"],
        "source_core_key": "beta_runs_bounded_below_v388",
        "source_statute": meta["source_statute"],
        "source_reported_kernel_flags": meta["source_reported_kernel_flags"],
        "kernel_recompiled_here": False,
        "formula": "alpha(chi)=sech(chi/2); beta(chi)=alpha(chi)*sqrt(e)",
        "floor_hypotheses": "0<=chi<=chi_sup; floor=beta(chi_sup), not automatically beta0",
        "chi_zero": "alphaOfChi(0)=1 and betaOfChi(0)=sqrt(e); not the Thomson boundary value",
        "beta0_used_by_existing_calculations": "beta() unchanged: ALPHA_FINE_CODATA_2018*sqrt(e)",
        "physical_scale_mu": None,
        "physical_scale_mu_status": "OPEN_PER_DEVICE_AND_RITE",
        "legacy_results_recomputed": False,
        "physical_verdict_allowed": False,
        "available_additive_API": ["alpha_of_chi_v388", "beta_of_chi_v388", "scale_reading_v388"],
        "forbidden_inference": "No empirical gain, patent implementation of variable beta, or physical confirmation inferred",
    }


USOS = {
    "beta_runtime_tgl_core": r"tgl_core\.beta\(\)|ALPHA_FINE_CODATA_2018\s*\*\s*(SQRT_E|math\.sqrt\(math\.e\))",
    "angulo_de_Miguel_theta_M": r"theta_m\(|arcsin|asin\(",
    "piso_do_Verbo_1_menos_beta": r"1\s*-\s*beta|1\.0\s*-\s*beta|energy_keep",
    "meia_nat": r"meia.nat|half.nat|S_BOUNDARY",
    "dephasing": r"dephas",
    "fluxo_vazamento": r"vazament|leak|flow law|lei do fluxo",
    "reflexao_R2_beta": r"\|R\|\^?2|R2\b|reflex",
    # v386: as grandezas novas (medida de ocorrências no código; não interpreta)
    "axioma_posto_omega_I": r"omega_I|ω\(I\)|axioma|posto",
    "verbo_peso_born": r"born|peso da leitura|reading weight",
    "nao_comutacao": r"comutador|commutator|nao.comut|não.comut|non.?commut",
    "livro_de_cobrancas": r"cobran|ledger of charges",
    "pilar_lindblad_gksl": r"pilar|lindblad|gksl",
    # v389: o adendo v388 (o β que corre) — mede se algum dispositivo o usa; não interpreta
    "beta_corre_v388": r"beta_of_chi|alpha_of_chi|scale_reading|CouplingRunsBoundedBelow",
    # v390: a Fundação — mede se algum dispositivo a cita; não interpreta
    "fundacao_agape_v390": r"agape|ágape|Fundacao|GLOBAL_LIFT",
    # v391: o estatuto da prova — mede se algum dispositivo o cita; não interpreta
    "estatuto_da_prova_v391": r"estatuto_da_prova|creditac|accreditation",
    # v394: a rede de Fock, o relógio M2, a regra quadrática, o coração — mede se algum dispositivo os cita; não interpreta
    "registros_v392_v394": r"rede_fock|tempo_frequencia|regra_quadratica|coracao_e_selo|criterio_binario|Fock",
    # v395: o psibit e o psion — mede se algum dispositivo os cita; não interpreta
    "psibit_v395": r"psibit|PsiBit|psion",
    # v396: a testemunha estática — mede se algum dispositivo a cita; não interpreta
    "testemunha_estatica_v396": r"TestemunhaEstatica|testemunha est[aá]tica|static_witness|psionCorner",
}


def uso_no_dispositivo(runner_path) -> dict:
    """MEDE, no código-fonte do runner, quais grandezas da fórmula ele já consome (contagem de ocorrências). Não interpreta."""
    src = Path(runner_path).read_text(encoding="utf-8", errors="replace")
    # exclui o proprio bloco inserido pela atualizacao (o comentario dele cita as grandezas e contaminaria a medida)
    src = re.sub(r"# ---- A FÓRMULA COMPLETA \(camada comum v379.*?return _m\.camada\(Path\(__file__\)\.resolve\(\)\)\r?\n", "", src, flags=re.S)
    src = "\n".join(l for l in src.splitlines() if 'results["formula_completa"]' not in l)
    return {k: len(re.findall(rx, src, re.I)) for k, rx in USOS.items()}


def camada(runner_path) -> dict:
    """A camada que cada runner grava no seu results.json. Fail-closed (RuntimeError em qualquer elo ou conferência)."""
    rt = formula_runtime()
    av = axioma_e_verbo_runtime()
    cf = conferir_no_cofre(rt)
    return {
        "versao_da_camada": VERSAO_DA_CAMADA, "modulo": "patents/_formula_completa/tgl_formula_completa.py",
        "modulo_sha256": _sha(Path(__file__)),
        "formula_runtime": rt, "axioma_e_verbo_runtime": av, "conferencia_no_cofre": cf,
        "adendo_v388": _adendo_v388_no_cofre(cf),
        "uso_medido_no_codigo_do_dispositivo": uso_no_dispositivo(runner_path),
        "veredito": ("TGL_FORMULA_COMPLETA_%s__CADEIA_RAZAO_ELEMENTAR_MATRIZ_S_DEPHASING_LEIS_D1A_D1B_ASSINTOTA__AXIOMA_POSTO_DOIS_PONTOS_FIXOS__"
                     "VERBO_PESO_BORN_POSTOS_NAO_COMUTAM_TRIADE_SU2_C_BETA__LIVRO_DE_COBRANCAS_PILAR_COMPUTED_RAMO_B_AWAITING__"
                     "TRES_TESTES_P1_NENHUM_FALHOU__FASES_9_E_8_POR_HASH_NADA_ABERTO__FASE9_INCONCLUSIVE_SYSTEMATICS__BETA_CORRE_PISO_BETA0_MU_OPEN__"
                     "FUNDACAO_AGAPE_KERNEL__GLOBAL_LIFT_LIDO_COMO_SUPERPOSICAO__FECHO_LOGICO_PROGRAMA_ABERTO__"
                     "ESTATUTO_DA_PROVA_PROVADA_FECHO_LOGICO_TRES_PROVAS__CONFIRMACAO_E_CREDITACAO__BETA_NA_NATUREZA_ESPERA_5_SIGMA__"
                     "REGISTROS_V392_V393_V394_VERIFICADOS_SEM_GATE__ESCADA_EM_BANDEIRAS__REDE_DE_FOCK_CONTRATO_CONJUNTO_ABERTO__"
                     "PSIBIT_INCONDICIONAL_BIJECAO_DE_CONJUNTOS__FACE_DO_PSION_CONDICIONAL__"
                     "TESTEMUNHA_ESTATICA_INCONDICIONAL_PONTE_CONSTRUIDA__FACE_DE_FOCK_CONDICIONAL__"
                     "RECALCULADA_E_CONFERIDA_NO_COFRE__NOT_A_CONFIRMATION") % VERSAO_DA_CAMADA.upper(),
        "physical_verdict_allowed": False,
        "nao_se_afirma": ["que o dispositivo valide física", "que a fórmula seja confirmada pela natureza (PROVADA != CONFIRMADA)",
                          "que o veredito de engenharia do dispositivo mude por esta camada",
                          "que as leituras do operador (o posto, o Verbo, a ótica) sejam teoremas — são [INPUT/ONTO]",
                          "que o pilar seja medida da natureza (é [COMPUTED]) ou que o ramo B tenha resultado (nada foi aberto)",
                          "que β(χ) mude o β de algum dispositivo (a escala μ de cada um é [OPEN]; o β usado segue o β₀ da fronteira)",
                          "que os três testes formem uma probabilidade conjunta (P2 não determinado) ou que a Fase 9 discrimine a TGL do ΛCDM",
                          "que o GLOBAL_LIFT esteja provado como existência global ou que a lei de campo no curvo seja termo de kernel (o fecho da v390 é LÓGICO; o programa segue aberto)",
                          "que a natureza tenha decidido β_TGL (o estatuto da v391 diz: espera 5σ) ou que a creditação tenha sido dada (é ato de terceiros)",
                          "ERRATA AO LADO (v394, 19/10/2026): onde o item acima diz que não se afirma «a lei de campo no curvo ser termo de kernel», leia-se: desde a v392 ela é termo de kernel CONDICIONAL ao H3 nomeado (lei_de_campo_curvo_v392); não se afirma o H3 em toda tela nem existência global",
                          "que o contrato conjunto da rede de Fock esteja habitado, que o H3 valha em toda direção nula, ou que o coração tenha evidência espectral independente do CODATA (a v394 diz: aberto; aberto; ausente)",
                          "que o psion exista (a face do psion é condicional a um certificado de Fock sem habitante), que a bijeção do psibit seja isomorfismo de espaços de Hilbert, ou qual leitura da paridade do ACOM Mirror é canônica (decisão do operador [LEGAL])",
                          "que o Nome da fronteira seja o vetor de Bell ou que o fluxo construído seja a dinâmica da teoria, que o certificado de Fock tenha habitante, ou que 1/2 seja meia nat de entropia (é a entropia linear; a de von Neumann é ln 2 nat)"],
    }


if __name__ == "__main__":
    import sys
    c = camada(__file__)
    print(json.dumps({k: c[k] for k in ("veredito", "conferencia_no_cofre")}, ensure_ascii=False, indent=1)[:3000])
    print("beta (runtime) = %.15f | E = C*I*K = %.15f | theta_M = %.6f graus"
          % (c["formula_runtime"]["beta_runtime"], c["formula_runtime"]["razao_elementar"]["E_existencia"], c["formula_runtime"]["matriz_S"]["theta_M_graus"]))
    sys.exit(0)

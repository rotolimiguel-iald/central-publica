# -*- coding: utf-8 -*-
"""one_skygrid.py — runner único forma = conteúdo da patente SkyGrid
(BR102026004850-0). [ENERGY][SIM][CONJ]

Demonstra a LÓGICA da invenção (gêmeo digital de energia), certifica com hash e
gera figuras + relatório auditável. NÃO valida física: physical_verdict_allowed=False;
o veredito máximo é MODEL_CLOSES / ENERGY_BALANCE_OK ([SIM] sob [CONJ]). β nunca literal
(emerge de ALPHA_FINE_CODATA_2018 * sqrt(e) no núcleo copiado do piloto).

A RÉGUA: o protótipo original em Patentes\\Skygrid\\SkyGrid_Piloto é READ-ONLY. Este
runner COPIA o núcleo mínimo (skygrid_sim + skygrid_physics + tests) para um workdir
próprio e roda a CÓPIA — jamais edita o original. Rode com o tgl_env (tem numpy):

    set PYTHONUTF8=1
    "C:\\IALD\\observaveis_tgl\\tgl_env\\Scripts\\python.exe" one_skygrid.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RUNNER_DIR = Path(__file__).resolve().parent
PATENT_DIR = RUNNER_DIR.parent
CENTRAL = PATENT_DIR.parents[1]
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"   # READ-ONLY original
MEMORY_MD = CENTRAL / "memory" / "patents" / "BR102026004850-0_SKYGRID.md"

WORK = RUNNER_DIR / "_piloto_core"          # copied core (transient, rebuilt each run)
CORE_DIRS = ["skygrid_sim", "skygrid_physics", "tests"]

PATENT_ID = "BR102026004850-0"
SLUG = "skygrid"


# ---- A FÓRMULA COMPLETA (camada comum v379; ordem do operador de 01/10/2026: «agora temos a fórmula completa, para todos»).
# Módulo único: patents/_formula_completa/tgl_formula_completa.py — a cadeia ω(I)=1 → ½ → √e → β, a Razão Elementar
# E = C×I×K = √e·1·α = β (TGLExt.TheElementaryReason), a matriz-S, o dephasing, as leis da dissipação D1a/D1b
# (TGLExt.TheFlowLawD1a, TGLExt.TheFlowLawContrast) e a assíntota, recalculadas em runtime e CONFERIDAS no cofre corrente.
# Fail-closed: elo quebrado ou cofre ilegível = RuntimeError. Não muda o veredito do dispositivo; physical_verdict_allowed=False.
def _formula_completa() -> dict:
    import importlib.util as _ilu
    _p = Path(__file__).resolve().parents[2] / "_formula_completa" / "tgl_formula_completa.py"
    _spec = _ilu.spec_from_file_location("tgl_formula_completa", str(_p))
    _m = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_m)
    return _m.camada(Path(__file__).resolve())


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def copy_core() -> dict:
    """Copy the minimal headless core from the READ-ONLY piloto. Returns file hashes."""
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    module_hashes: dict[str, str] = {}
    for d in CORE_DIRS:
        src = PILOTO / d
        if not src.exists():
            continue
        dst = WORK / d
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
        for f in sorted(dst.rglob("*.py")):
            module_hashes[str(f.relative_to(WORK)).replace("\\", "/")] = _sha_file(f)
    return module_hashes


def run_energy_twin() -> tuple[dict, dict]:
    """Import the copied EnergyTwin and run it headless. Returns (report, series)."""
    sys.path.insert(0, str(WORK))
    from skygrid_physics.energy_twin import EnergyTwin  # noqa: E402 (copied core)
    with tempfile.TemporaryDirectory() as td:
        tw = EnergyTwin(n_sats=12, n_bases=12, seed=11, duration_s=120.0, dt_s=1.0,
                        state_path=str(Path(td) / "state.json"))
        report = tw.run()
        series = getattr(tw, "series", {})
    return report, series


def run_test_suite() -> dict:
    """Run the copied v3 suite as a subprocess (cwd=WORK) to get tests + invariants hash.
    The suite writes SKYGRID_V3_SELO.json into WORK — never into the original."""
    v3 = WORK / "tests" / "run_tests_v3.py"
    if not v3.exists():
        return {}
    # PYTHONUTF8=1 na CADEIA inteira (v3 -> v2 -> v1): os filhos emitem UTF-8 e o
    # text=True aninhado decodifica UTF-8 — sem isso, console cp1252 derruba a
    # thread leitora (stdout=None) e a suite quebra sem culpa dos testes.
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    try:
        subprocess.run([sys.executable, str(v3)], cwd=str(WORK), check=True,
                       capture_output=True, timeout=600, env=env)
    except Exception as e:  # keep the run honest — record the failure, don't fake it
        return {"suite_error": str(e)[:300]}
    selo = WORK / "SKYGRID_V3_SELO.json"
    if selo.exists():
        return json.loads(selo.read_text(encoding="utf-8"))
    return {}


def make_figures(series: dict, out_dir: Path) -> list[str]:
    """Optional technical figures from the twin's time series (needs matplotlib)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = []
    t = series.get("t") or series.get("time") or list(range(len(next(iter(series.values()), []))))
    power_keys = [k for k in series if any(s in k.lower() for s in
                  ("deliver", "demand", "power", "p_"))][:4]
    if power_keys:
        plt.figure(figsize=(8, 4))
        for k in power_keys:
            y = series[k]
            plt.plot(t[:len(y)], y, label=k, linewidth=1.4)
        plt.title("SkyGrid — potência ao longo da janela [SIM] (não é medida física)")
        plt.xlabel("t (s)"); plt.ylabel("W"); plt.legend(fontsize=8); plt.grid(alpha=.3)
        p = out_dir / "fig_power.png"; plt.savefig(p, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(p.name)
    store_keys = [k for k in series if any(s in k.lower() for s in ("stor", "soc", "e_"))][:3]
    if store_keys:
        plt.figure(figsize=(8, 4))
        for k in store_keys:
            y = series[k]
            plt.plot(t[:len(y)], y, label=k, linewidth=1.4)
        plt.title("SkyGrid — energia/armazenamento [SIM]")
        plt.xlabel("t (s)"); plt.ylabel("J"); plt.legend(fontsize=8); plt.grid(alpha=.3)
        p = out_dir / "fig_energy.png"; plt.savefig(p, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(p.name)
    return figs


def run_design_sweeps() -> dict:
    """APROFUNDAMENTO honesto [SIM]: varre TODOS os parâmetros de projeto do gêmeo
    (Q, η_geo, S_field, η_rt, f_drive, n_sats) usando o `sweeps.run_all` do próprio
    protótipo copiado. Cada ponto RE-AUDITA a conservação de energia (fail-closed):
    uma varredura que quebrasse o balanço abortaria. Produz FAMÍLIAS de curvas — não
    um número mágico — mais a curva de RESSONÂNCIA em f_drive (pico em ω_OH). Escreve
    apenas dentro da cópia WORK; original intacto."""
    # skygrid_physics already on sys.path from run_energy_twin(); import defensively
    if str(WORK) not in sys.path:
        sys.path.insert(0, str(WORK))
    from skygrid_physics import sweeps  # noqa: E402 (copied core)
    return sweeps.run_all(fast=False)


def make_sweep_figures(sweep_out: dict, out_dir: Path) -> list[str]:
    """Duas figuras NOVAS das famílias de curvas do gêmeo digital [SIM]:
    (1) curva de ressonância P_entregue(f_drive) com o pico em ω_OH;
    (2) escalabilidade P_entregue(n_sats) — quantos Extratores-Psi rendem quanto."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    figs = []
    sw = sweep_out.get("sweeps", {})

    fd = sw.get("f_drive_MHz", {}).get("points", [])
    if fd:
        xs = [p["f_drive_MHz"] for p in fd]
        ys = [p["P_delivered_W"] for p in fd]
        f_peak = xs[int(max(range(len(ys)), key=lambda i: ys[i]))]
        plt.figure(figsize=(8, 4))
        plt.plot(xs, ys, "o-", color="#3366cc", linewidth=1.6, markersize=5)
        plt.axvline(f_peak, color="#cc2222", linestyle="--", linewidth=1.1,
                    label=f"pico = ω_OH ≈ {f_peak:.4f} MHz")
        plt.title("SkyGrid — curva de ressonância do acoplador [SIM] (não é medida física)")
        plt.xlabel("f_drive (MHz)"); plt.ylabel("P entregue (W) [SIM]")
        plt.legend(fontsize=8); plt.grid(alpha=.3)
        p = out_dir / "fig_resonance.png"
        plt.savefig(p, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(p.name)

    ns = sw.get("n_sats", {}).get("points", [])
    if ns:
        xs = [p["n_sats"] for p in ns]
        yp = [p["P_delivered_W"] for p in ns]
        ye = [p["eta_sys"] for p in ns]
        fig, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(xs, yp, "s-", color="#33aa55", linewidth=1.6, label="P entregue (W)")
        ax1.set_xlabel("n_sats (Extratores-Psi)"); ax1.set_ylabel("P entregue (W) [SIM]", color="#33aa55")
        ax1.grid(alpha=.3)
        ax2 = ax1.twinx()
        ax2.plot(xs, ye, "^--", color="#ee8800", linewidth=1.3, label="η_sys")
        ax2.set_ylabel("η_sys", color="#ee8800")
        plt.title("SkyGrid — escalabilidade da constelação [SIM]")
        p = out_dir / "fig_scaling.png"
        plt.savefig(p, dpi=120, bbox_inches="tight"); plt.close()
        figs.append(p.name)
    return figs


def amplification_v138(beta: float) -> dict:
    """AMPLIFICACAO v138 [DER] — a COMPOSICAO KNOWN-COMPOSED (um.py v135) + o CONE
    EMERGENTE (v116/v120): o SkyGrid e o COMPILADOR das 16 — composicao de modulos
    verificados, como a testemunha completa existe por composicao de teoremas
    publicados. Sombra numerica autocontida (numpy puro), beta SEMPRE do runtime
    (tgl_core: ALPHA_FINE_CODATA_2018*sqrt(e)), jamais literal:
      (a) identidade do cone nulo G_kk = (c^2 + d^2) * G_22 no ansatz cosh
          g = diag(-cosh(kappa*x)^2, 1, 1, 1) com kappa^2 = beta; tensor de
          Einstein por diferencas finitas de 4a ordem (g -> Gamma -> Riemann ->
          Ricci -> G); Bianchi visivel: G_00 = G_11 = 0; G_22 = a''/a = beta.
      (b) meta-composicao: hash-de-hashes de N blocos simulados e ESTAVEL sob
          re-ordenacao canonica (sort) e SENSIVEL a 1 bit trocado.
    HONESTIDADE: sombra matematica [DER]; NAO e veredito fisico
    (physical_verdict_allowed=False); nao altera reivindicacoes da patente."""
    import numpy as np

    # ---- (a) o cone emergente: Einstein numerico do ansatz cosh -----------------
    kappa = math.sqrt(beta)                    # beta do runtime; kappa^2 = beta
    h, n = 0.05, 41
    x = (np.arange(n) - n // 2) * h
    a = np.cosh(kappa * x)
    g = np.zeros((n, 4, 4))
    ginv = np.zeros((n, 4, 4))
    g[:, 0, 0] = -a * a
    ginv[:, 0, 0] = -1.0 / (a * a)
    for i in (1, 2, 3):
        g[:, i, i] = 1.0
        ginv[:, i, i] = 1.0

    def d_dx(f):
        """4th-order central difference along the grid axis (margins left 0)."""
        out = np.zeros_like(f)
        out[2:-2] = (-f[4:] + 8.0 * f[3:-1] - 8.0 * f[1:-3] + f[:-4]) / (12.0 * h)
        return out

    dg = np.zeros((n, 4, 4, 4))                # dg[:, s, m, v] = d_s g_{mv}
    dg[:, 1] = d_dx(g)                         # metric depends only on x (index 1)
    Gam = np.zeros((n, 4, 4, 4))               # Gamma^m_{v r}
    for m in range(4):
        for v in range(4):
            for r in range(4):
                acc = np.zeros(n)
                for s in range(4):
                    acc += ginv[:, m, s] * (dg[:, v, s, r] + dg[:, r, s, v] - dg[:, s, v, r])
                Gam[:, m, v, r] = 0.5 * acc
    dGam = np.zeros((n, 4, 4, 4, 4))           # dGam[:, s, m, v, r] = d_s Gamma^m_{vr}
    dGam[:, 1] = d_dx(Gam)
    Riem = np.zeros((n, 4, 4, 4, 4))           # R^m_{v r s}
    for m in range(4):
        for v in range(4):
            for r in range(4):
                for s in range(4):
                    term = dGam[:, r, m, v, s] - dGam[:, s, m, v, r]
                    for l in range(4):
                        term += (Gam[:, m, r, l] * Gam[:, l, v, s]
                                 - Gam[:, m, s, l] * Gam[:, l, v, r])
                    Riem[:, m, v, r, s] = term
    Ric = np.einsum('nmvms->nvs', Riem)
    Rsc = np.einsum('nvs,nvs->n', ginv, Ric)
    G = Ric - 0.5 * Rsc[:, None, None] * g

    core = slice(4, n - 4)                     # drop nested-stencil margins
    Gc = G[core]
    resid_bianchi = float(max(np.max(np.abs(Gc[:, 0, 0])), np.max(np.abs(Gc[:, 1, 1]))))
    resid_iso = float(np.max(np.abs(Gc[:, 3, 3] - Gc[:, 2, 2])))
    resid_g22_beta = float(np.max(np.abs(Gc[:, 2, 2] - beta)))  # a''/a = kappa^2 = beta

    # full null cone: k = (kt, b, c, d) with g(k,k)=0 => G_kk = (c^2+d^2)*G_22
    rng = np.random.default_rng(138)
    resid_cone, resid_null = 0.0, 0.0
    n_samples = 0
    for i in (5, n // 2, n - 6):               # interior grid points
        for _ in range(24):
            b, c, d = rng.uniform(-1.0, 1.0, size=3)
            kt = math.sqrt(b * b + c * c + d * d) / a[i]
            k = np.array([kt, b, c, d])
            resid_null = max(resid_null, abs(float(k @ g[i] @ k)))
            G_kk = float(k @ G[i] @ k)
            resid_cone = max(resid_cone, abs(G_kk - (c * c + d * d) * G[i, 2, 2]))
            n_samples += 1
    cone_ok = (resid_cone < 1e-10 and resid_bianchi < 1e-10 and resid_iso < 1e-10
               and resid_g22_beta < 1e-10 and resid_null < 1e-12)

    # ---- (b) meta-composicao: hash-de-hashes dos blocos simulados ---------------
    n_blocks = 16
    blocks = [rng.integers(0, 256, size=256, dtype=np.uint8).tobytes()
              for _ in range(n_blocks)]
    hashes = [hashlib.sha256(bl).hexdigest() for bl in blocks]

    def meta_hash(hs):                          # canonical order: sort before hashing
        return _sha_text("".join(sorted(hs)))

    meta0 = meta_hash(hashes)
    perm = rng.permutation(n_blocks)
    meta_shuffled = meta_hash([hashes[int(i)] for i in perm])
    stable = (meta_shuffled == meta0)
    tampered = bytearray(blocks[0])
    tampered[0] ^= 0x01                         # flip exactly 1 bit
    meta_flip = meta_hash([hashlib.sha256(bytes(tampered)).hexdigest()] + hashes[1:])
    sensitive = (meta_flip != meta0)

    tests = []
    tests.append({
        "test": "known_composed_cone_identity",
        "passed": bool(cone_ok and stable and sensitive),
        "resid_cone_max": resid_cone,
        "resid_bianchi_G00_G11_max": resid_bianchi,
        "resid_G33_minus_G22_max": resid_iso,
        "resid_G22_minus_beta_max": resid_g22_beta,
        "resid_null_norm_max": resid_null,
        "n_null_samples": int(n_samples),
        "n_blocks": int(n_blocks),
        "meta_hash": meta0[:16],
        "meta_stable_under_sort": bool(stable),
        "meta_sensitive_to_1bit": bool(sensitive),
        "marker": "[DER]",
    })
    return {
        "theorem": "KNOWN-COMPOSED (um.py v135) + cone emergente (v116/v120): "
                   "a testemunha completa existe por composicao de teoremas "
                   "publicados; o SkyGrid e o compilador das 16 (composicao de "
                   "modulos verificados).",
        "ansatz": "g = diag(-cosh(kappa*x)^2, 1, 1, 1), kappa^2 = beta (runtime)",
        "tests": tests,
        "note": "[DER] sombra matematica; physical_verdict_allowed=False; "
                "nao altera reivindicacoes nem afirma capacidade nova.",
    }


def amplification_v144(beta: float) -> dict:
    """AMPLIFICACAO v144 [DER] — CODE_CLOSURE_COMPLETE (um.py v143) aplicado ao
    COMPILADOR: o fechamento do codigo = LEDGER onde todo aberto tem fiador
    ({BY_DESIGN, EXTERNAL_KNOWN, NAMED_PROGRAM}) + a assinatura deterministica
    da compilacao (a meta-cadeia). O SkyGrid JA e o compilador das 16 — a
    meta-cadeia REAL vive em skygrid_compilation.json; aqui a GRAMATICA do
    fechamento vira teste fail-closed no runner, em python puro (sem numpy):
      (a) mini-compilacao: N=16 modulos sinteticos com hashes; a meta-cadeia
          (hash-de-hashes canonico por sort) e DETERMINISTICA sob re-ordenacao
          e SENSIVEL a 1 bit trocado em QUALQUER modulo (16/16 flips);
      (b) ledger do fechamento: modulos {verificado|aberto}; todo aberto tem
          fiador no conjunto permitido; compilacao com aberto ORFAO ==> REJEITADA
          (fail-closed, assert negativo);
      (c) ancoragem no artefato vivo: le READ-ONLY o skygrid_compilation.json
          real da pasta da patente e confere meta-cadeia 64 hex + 16 entradas OK
          (se ausente: reporta e pula o sub-check, restante decide o passed).
    HONESTIDADE: [DER] gramatica de engenharia da compilacao; [SIM] modulos
    sinteticos; physical_verdict_allowed=false; beta runtime (nunca literal);
    NAO altera reivindicacoes nem afirma capacidade nova."""
    import random

    FIADORES = {"BY_DESIGN", "EXTERNAL_KNOWN", "NAMED_PROGRAM"}
    HEXD = set("0123456789abcdef")

    # ---- (a) mini-compilacao: 16 modulos sinteticos deterministas ----------------
    n_modules = 16
    modules = []
    for i in range(n_modules):
        content = f"skygrid/v144/module_{i:02d}/beta_runtime={beta:.17g}".encode("ascii")
        modules.append((f"mod_{i:02d}", content))

    def module_hashes(mods):
        return [(name, hashlib.sha256(data).hexdigest()) for name, data in mods]

    def meta_chain(hashes):
        # ordem canonica: sort das linhas "nome:hash" antes do hash (livre de ordem)
        return _sha_text("\n".join(sorted(f"{n}:{h}" for n, h in hashes)))

    class ClosureError(Exception):
        pass

    def compile_closure(mods, ledger):
        """fail-closed: a compilacao SO emite meta-cadeia se o ledger fechar
        (todo aberto com fiador valido); aberto orfao ==> ClosureError."""
        for entry in ledger:
            if entry.get("status") not in ("verificado", "aberto"):
                raise ClosureError(f"status invalido: {entry.get('item')}")
            if entry["status"] == "aberto" and entry.get("fiador") not in FIADORES:
                raise ClosureError(f"aberto ORFAO (sem fiador valido): {entry.get('item')}")
        return meta_chain(module_hashes(mods))

    # ---- (b) o ledger do fechamento desta patente (classes do v143) --------------
    ledger = [
        {"item": "beta_eq_alpha_sqrt_e_runtime", "status": "verificado"},
        {"item": "energy_balance_fail_closed", "status": "verificado"},
        {"item": "resonance_peak_at_omega_OH", "status": "verificado"},
        {"item": "placebo_zero_by_construction", "status": "verificado"},
        {"item": "meta_cadeia_deterministica", "status": "verificado"},
        # todo aberto com fiador nomeado — a gramatica CODE_CLOSURE_COMPLETE:
        {"item": "physical_verdict", "status": "aberto", "fiador": "BY_DESIGN",
         "note": "proibido por construcao: simulacao nunca valida fisica"},
        {"item": "alpha_fine_CODATA_2018_input", "status": "aberto", "fiador": "EXTERNAL_KNOWN",
         "note": "constante certificada externa (CODATA); nao derivada aqui"},
        {"item": "bancada_B1_B5_hardware", "status": "aberto", "fiador": "NAMED_PROGRAM",
         "note": "programa nomeado de bancada: so a fisica responde"},
    ]
    n_abertos = sum(1 for e in ledger if e["status"] == "aberto")
    closure_ok = all(e.get("fiador") in FIADORES for e in ledger if e["status"] == "aberto")

    meta0 = compile_closure(modules, ledger)
    meta_is_64hex = (len(meta0) == 64 and set(meta0) <= HEXD)

    # deterministica sob re-ordenacao (8 embaralhamentos com semente fixa)
    rng = random.Random(144)
    stable = True
    for _ in range(8):
        shuffled = list(modules)
        rng.shuffle(shuffled)
        if compile_closure(shuffled, ledger) != meta0:
            stable = False
            break

    # sensivel a 1 bit trocado em QUALQUER um dos 16 modulos
    flips_sensitive = 0
    for i in range(n_modules):
        name, data = modules[i]
        tampered = bytearray(data)
        tampered[0] ^= 0x01                     # flip de exatamente 1 bit
        mods2 = list(modules)
        mods2[i] = (name, bytes(tampered))
        if compile_closure(mods2, ledger) != meta0:
            flips_sensitive += 1
    sensitive_all = (flips_sensitive == n_modules)

    # assert negativo: aberto ORFAO (sem fiador) ==> compilacao REJEITADA
    orphan_rejected = False
    try:
        compile_closure(modules, ledger + [{"item": "orfao_teste_negativo",
                                            "status": "aberto"}])
    except ClosureError:
        orphan_rejected = True
    # assert negativo 2: fiador fora do conjunto permitido ==> REJEITADA
    bad_fiador_rejected = False
    try:
        compile_closure(modules, ledger + [{"item": "fiador_invalido_teste_negativo",
                                            "status": "aberto", "fiador": "MAGIC"}])
    except ClosureError:
        bad_fiador_rejected = True

    # ---- (c) ancoragem READ-ONLY no artefato vivo --------------------------------
    comp_path = PATENT_DIR / "skygrid_compilation.json"
    anchor_present = comp_path.exists()
    anchor_ok = None                            # None = ausente (sub-check pulado)
    if anchor_present:
        real = json.loads(comp_path.read_text(encoding="utf-8"))   # READ-ONLY
        real_meta = str(real.get("skygrid_compilation_hash", ""))
        real_meta_64hex = (len(real_meta) == 64 and set(real_meta) <= HEXD)
        pats = real.get("patents", [])
        entries_ok = (real.get("n_patents") == 16 and len(pats) == 16
                      and bool(real.get("all_integrity_ok"))
                      and all(bool(p.get("integrity_ok"))
                              and len(str(p.get("combined_sha256", ""))) == 64
                              for p in pats))
        this_listed = any(p.get("patent_id") == PATENT_ID for p in pats)
        anchor_ok = bool(real_meta_64hex and entries_ok and this_listed)
        anchor = {"path": comp_path.name, "meta_cadeia_real": real_meta[:16],
                  "meta_cadeia_64hex": real_meta_64hex, "n_entries": len(pats),
                  "all_16_entries_ok": entries_ok, "this_patent_listed": this_listed}
    else:
        anchor = {"path": comp_path.name,
                  "note": "AUSENTE - sub-check pulado; restante decide o passed"}

    passed = (stable and sensitive_all and meta_is_64hex and closure_ok
              and orphan_rejected and bad_fiador_rejected
              and (anchor_ok is None or anchor_ok))

    tests = [{
        "test": "compilation_closure_ledger",
        "passed": bool(passed),
        "n_modules": int(n_modules),
        "meta_chain": meta0[:16],
        "meta_chain_64hex": bool(meta_is_64hex),
        "stable_under_8_shuffles": bool(stable),
        "sensitive_1bit_flips": f"{flips_sensitive}/{n_modules}",
        "ledger_total": len(ledger),
        "ledger_abertos": int(n_abertos),
        "ledger_all_abertos_com_fiador": bool(closure_ok),
        "fiadores_permitidos": sorted(FIADORES),
        "orphan_compilation_rejected": bool(orphan_rejected),
        "bad_fiador_rejected": bool(bad_fiador_rejected),
        "anchor_checked": bool(anchor_present),
        "anchor_real_compilation": anchor,
        "marker": "[DER]",
    }]
    return {
        "theorem": "CODE_CLOSURE_COMPLETE (um.py v143): o fechamento do codigo = "
                   "ledger onde TODO aberto tem fiador {BY_DESIGN, EXTERNAL_KNOWN, "
                   "NAMED_PROGRAM} + a assinatura deterministica da compilacao "
                   "(meta-cadeia); o SkyGrid e o compilador das 16 e este runner "
                   "ancora a GRAMATICA do fechamento no artefato vivo.",
        "ledger": ledger,
        "tests": tests,
        "note": "[DER]/[SIM] gramatica de compilacao em python puro; beta runtime "
                "(nunca literal); physical_verdict_allowed=false; nao altera "
                "reivindicacoes nem afirma capacidade nova.",
    }


def amplification_v143_lift(beta: float) -> dict:
    """AMPLIFICACAO v143-lift [DER] — GLOBAL_LIFT_CONDITIONAL (um.py v143, pedra 99):
    Takesaki finito + juramento H_inv ==> esperanca condicional E COVARIANTE; com
    CONTROLE NEGATIVO (quem quebra o juramento perde a covariancia). Mapeamento
    GENUINO ao mecanismo desta patente: a eq. (5) A_phi^global = prod_k A_phi_k (x)
    prod_j A_phi_j — o operador global E o produto tensorial dos locais — e a
    reivindicacao 7 (Prova de Fase, convergencia |delta| < 1e-4) e o juramento de
    invariancia em forma de engenharia. Sombra numerica autocontida (numpy):
      (a) no local: rho bloco-diagonal com gap modular theta_M = arcsin(sqrt(beta))
          (runtime, nunca literal); fluxo modular sigma_t(X) = rho^{it} X rho^{-it}
          por eigendecomposicao; subalgebra A = blocos e INVARIANTE (juramento:
          delta_inv ~ 1e-16 < tol da reivindicacao 7); E(X) = sum P_i X P_i e
          rho-preservante e COVARIANTE (E o sigma_t = sigma_t o E, residuo ~1e-15);
      (b) o LEVANTAMENTO GLOBAL (eq. 5): rho_glob = rho1 (x) rho2 (16 dim),
          E_glob = E1 (x) E2 segue covariante — o produto dos juramentos locais
          LEVANTA, como a pedra 99 tipa o Lema 3;
      (c) CONTROLES NEGATIVOS: no com juramento QUEBRADO (blocos rodados por
          U = exp(i*0.7*H_mix)): delta_inv GRANDE (> tol) ==> covariancia FALHA
          (defeito O(1)) e E' deixa de ser rho-preservante; 1 no ruim tambem
          derruba o levantamento GLOBAL — um no fora de fase quebra o selo
          (a Prova de Fase da reivindicacao 7);
      (d) periodo modular DERIVADO: sigma_{2pi/theta_M} = id na subalgebra
          invariante (residuo ~1e-13) e o MEIO-periodo NAO retorna (defeito = 2)
          — theta_M vem so do runtime, por caminho independente (log/exp matricial).
    HONESTIDADE: [DER] sombra matematica (Takesaki finito e teorema conhecido,
    aqui INSTANCIADO na forma da eq. 5 do dispositivo); [SIM] nos sinteticos;
    physical_verdict_allowed=False; nao altera reivindicacoes nem afirma
    capacidade nova."""
    import numpy as np

    theta_M = math.asin(math.sqrt(beta))        # runtime; nunca literal
    T_period = 2.0 * math.pi / theta_M
    TOL_CLAIM7 = 1e-4                           # reivindicacao 7: |delta alpha^2| < 1e-4
    p = math.exp(theta_M) / (1.0 + math.exp(theta_M))   # gap do bloco = theta_M

    def node_rho(w_hi: float) -> "np.ndarray":
        """rho 4x4 bloco-diagonal: blocos com pesos (w_hi, 1-w_hi), gap theta_M."""
        w_lo = 1.0 - w_hi
        return np.diag([w_hi * p, w_hi * (1 - p), w_lo * p, w_lo * (1 - p)])

    def make_flow(rho):
        vals, vecs = np.linalg.eigh(rho)
        lg = np.log(vals)                       # full-rank por construcao

        def sigma(t, X):
            U = (vecs * np.exp(1j * t * lg)) @ vecs.conj().T
            return U @ X @ U.conj().T
        return sigma

    def make_E(projs):
        def E(X):
            return sum(P @ X @ P for P in projs)
        return E

    rng = np.random.default_rng(143)

    def rand_X(n, k=3):
        return [rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
                for _ in range(k)]

    ts_grid = [0.37, 1.13, 2.71, 5.9]

    def cov_resid(sigma, E, Xs):
        r = 0.0
        for X in Xs:
            nX = float(np.linalg.norm(X))
            for t in ts_grid:
                r = max(r, float(np.linalg.norm(E(sigma(t, X)) - sigma(t, E(X)))) / nX)
        return r

    def oath_resid(sigma, E, Xs):
        """distancia de sigma_t(A) a A (o juramento H_inv, quantificado)."""
        r = 0.0
        for X in Xs:
            a = E(X)
            na = float(np.linalg.norm(a))
            for t in ts_grid:
                s = sigma(t, a)
                r = max(r, float(np.linalg.norm(s - E(s))) / na)
        return r

    def pres_defect(rho, E, Xs):
        d = 0.0
        for X in Xs:
            d = max(d, abs(complex(np.trace(rho @ E(X)) - np.trace(rho @ X)))
                    / float(np.linalg.norm(X)))
        return d

    # ---- (a) no local honesto: juramento mantido ==> E covariante ---------------
    P1 = np.diag([1.0, 1.0, 0.0, 0.0])
    P2 = np.diag([0.0, 0.0, 1.0, 1.0])
    rho1 = node_rho(0.5 + beta)                 # pesos derivados do runtime
    sigma1 = make_flow(rho1)
    E1 = make_E([P1, P2])
    Xs4 = rand_X(4)
    delta_inv_good = oath_resid(sigma1, E1, Xs4)
    cov_local = cov_resid(sigma1, E1, Xs4)
    pres_good = pres_defect(rho1, E1, Xs4)

    # ---- (c1) no com juramento QUEBRADO: blocos rodados -------------------------
    H_mix = np.zeros((4, 4))
    H_mix[0, 2] = H_mix[2, 0] = 1.0
    H_mix[1, 3] = H_mix[3, 1] = 1.0
    hv, hU = np.linalg.eigh(H_mix)
    U_bad = (hU * np.exp(1j * 0.7 * hv)) @ hU.conj().T
    Q1, Q2 = U_bad @ P1 @ U_bad.conj().T, U_bad @ P2 @ U_bad.conj().T
    E_bad = make_E([Q1, Q2])
    delta_inv_bad = oath_resid(sigma1, E_bad, Xs4)
    cov_bad_local = cov_resid(sigma1, E_bad, Xs4)
    pres_bad = pres_defect(rho1, E_bad, Xs4)

    # ---- (b) o levantamento GLOBAL (eq. 5): produto tensorial -------------------
    rho2 = node_rho(0.5 + 2.0 * beta)           # 2o no, pesos distintos (runtime)
    rho_g = np.kron(rho1, rho2)
    sigma_g = make_flow(rho_g)
    projs_g = [np.kron(Pi, Qj) for Pi in (P1, P2) for Qj in (P1, P2)]
    E_g = make_E(projs_g)
    Xs16 = rand_X(16)
    cov_glob = cov_resid(sigma_g, E_g, Xs16)
    pres_glob = pres_defect(rho_g, E_g, Xs16)

    # ---- (c2) 1 no ruim derruba o global (Prova de Fase) ------------------------
    projs_g_bad = [np.kron(Pi, Qj) for Pi in (P1, P2) for Qj in (Q1, Q2)]
    E_g_bad = make_E(projs_g_bad)
    cov_bad_glob = cov_resid(sigma_g, E_g_bad, Xs16)

    # ---- (d) periodo modular derivado: sigma_{2pi/theta_M} = id -----------------
    period_resid = 0.0
    for X in Xs4:
        a = E1(X)
        period_resid = max(period_resid,
                           float(np.linalg.norm(sigma1(T_period, a) - a))
                           / float(np.linalg.norm(a)))
    a_off = E1(Xs4[0])
    a_off = a_off - np.diag(np.diag(a_off))     # so off-diagonal dentro dos blocos
    half_defect = (float(np.linalg.norm(sigma1(T_period / 2.0, a_off) - a_off))
                   / float(np.linalg.norm(a_off)))

    oath_kept = delta_inv_good < TOL_CLAIM7
    oath_broken = delta_inv_bad > TOL_CLAIM7
    passed = (oath_kept and oath_broken
              and cov_local < 1e-9 and cov_glob < 1e-9
              and cov_bad_local > 1e-3 and cov_bad_glob > 1e-3
              and pres_good < 1e-11 and pres_glob < 1e-11 and pres_bad > 1e-6
              and period_resid < 1e-9 and half_defect > 1.9)

    tests = [{
        "test": "global_lift_conditional_expectation",
        "passed": bool(passed),
        "theta_M": float(theta_M),
        "period_T": float(T_period),
        "tol_claim7": TOL_CLAIM7,
        "delta_inv_oath_kept": float(delta_inv_good),
        "delta_inv_oath_broken": float(delta_inv_bad),
        "cov_resid_local": float(cov_local),
        "cov_resid_global_lift": float(cov_glob),
        "cov_defect_broken_local": float(cov_bad_local),
        "cov_defect_broken_global": float(cov_bad_glob),
        "rho_pres_resid_local": float(pres_good),
        "rho_pres_resid_global": float(pres_glob),
        "rho_pres_defect_broken": float(pres_bad),
        "period_resid": float(period_resid),
        "half_period_defect": float(half_defect),
        "n_random_X": 3,
        "n_t_grid": len(ts_grid),
        "marker": "[DER]",
    }]
    return {
        "theorem": "GLOBAL_LIFT_CONDITIONAL (um.py v143, pedra 99): Takesaki finito "
                   "+ juramento H_inv ==> esperanca condicional covariante; controle "
                   "negativo incluido. Instanciado na eq. (5) da patente "
                   "(A_phi^global = produto tensorial dos locais) com a tolerancia "
                   "da reivindicacao 7 (Prova de Fase) como juramento.",
        "mapping": "eq. (5) A_phi^global = prod A_phi_k (x) prod A_phi_j = o "
                   "levantamento global; reivindicacao 7 |delta|<1e-4 = o juramento "
                   "H_inv; 1 no fora de fase quebra o selo global.",
        "tests": tests,
        "note": "[DER]/[SIM] sombra matematica de Takesaki finito; theta_M = "
                "arcsin(sqrt(beta)) so do runtime (nunca literal); "
                "physical_verdict_allowed=false; nao altera reivindicacoes nem "
                "afirma capacidade nova.",
    }


def amplification_v168_ergodic(beta: float) -> dict:
    """AMPLIFICACAO v168 [DER] — ErgodicMeanSection (um.py v166-v167, ITEM A EM
    KERNEL, 4 pedras Lean 0 sorry 0 axiom): o LIMITE DE BIRKHOFF em kernel — a
    media (1/N) sum_{k<N} U^k converge a PROJECAO INVARIANTE. Mapeamento GENUINO
    ao mecanismo desta patente: o A_phi (Operador de Fase Angular ESTAVEL, eq. 5)
    e o ciclo REFLECT->LOCK da crl-TGL — a fase LOCK e exatamente o componente
    que SOBREVIVE a media temporal do fluxo; o drift (theta != 0) morre a taxa
    <= C/N com C = 1/sin(theta_M/2); e a tolerancia da reivindicacao 7 (Prova de
    Fase, |delta| < 1e-4) vira o CRITERIO de convergencia N_min. Ecos das pedras
    irmas do item A: EquivariantSection (a projecao COMUTA com o fluxo — a secao
    e equivariante) e BreuerTrace (o peso do LOCK e TRACO: tau(a*a) = tau(aa*)
    com a = U.P; aqui em dim finita e a propriedade do traco — a pedra kernel e
    o enunciado no habitante inf-dim). Sombra numerica autocontida (numpy):
      (a) U ortogonal 6x6 bloco-diagonal: bloco LOCK dim 2 (identidade) +
          2 blocos de drift rot(theta_M), rot(2*theta_M), theta_M =
          arcsin(sqrt(beta)) SO do runtime (nunca literal);
      (b) media de Birkhoff por DOBRAMENTO BINARIO (S_{2m} = (I+U^m) S_m),
          validada contra a soma direta (2 caminhos independentes concordam);
      (c) P por caminho independente (autoespaco de autovalor 1 via eig):
          idempotente, auto-adjunta, invariante (U.P = P), EQUIVARIANTE
          ([U, P] = 0); peso tau(P) = 2 = dim do LOCK (o traco);
      (d) convergencia: ||M_N - P|| <= C/N em N = 100/1000/10000 e queda
          efetiva de 2 decadas; N_min = ceil(C/1e-4) cumpre a reivindicacao 7;
      (e) NEGATIVOS (fail-closed, contra-exemplos REJEITADOS por logica):
          (e1) U adulterado (nao-unitario, perturbacao = beta) e RECUSADO pelo
          gate ANTES de qualquer media; (e2) secao FALSA Q (projecao sobre
          coordenada de drift) e rejeitada — nao e equivariante, nao e
          invariante e a media NAO converge a ela; (e3) media INSUFICIENTE
          (N_min/100 ciclos) NAO cumpre a tolerancia da reivindicacao 7 —
          poucos ciclos de fase nao selam a Prova de Fase.
    HONESTIDADE: [DER] sombra matematica do teorema ergodico de von Neumann
    (a pedra kernel e o enunciado formal); [SIM] operador sintetico;
    physical_verdict_allowed=False; nao altera reivindicacoes nem afirma
    capacidade nova — simulacao nunca valida fisica."""
    import numpy as np

    theta_M = math.asin(math.sqrt(beta))        # runtime; nunca literal
    TOL_CLAIM7 = 1e-4                           # reivindicacao 7: |delta| < 1e-4
    n = 6

    def rot(th):
        c, s = math.cos(th), math.sin(th)
        return np.array([[c, -s], [s, c]])

    U = np.zeros((n, n))
    U[0:2, 0:2] = np.eye(2)                     # bloco LOCK (fase estavel)
    U[2:4, 2:4] = rot(theta_M)                  # drift 1
    U[4:6, 4:6] = rot(2.0 * theta_M)            # drift 2

    def birkhoff_mean(Umat, N):
        """(1/N) sum_{k=0}^{N-1} Umat^k por dobramento binario; GATE fail-closed:
        entrada nao-unitaria e RECUSADA antes de qualquer media."""
        if float(np.max(np.abs(Umat.T @ Umat - np.eye(Umat.shape[0])))) > 1e-12:
            raise ValueError("non-unitary input rejected (fail-closed)")
        S = np.zeros_like(Umat)                 # soma para N=0
        P = np.eye(Umat.shape[0])               # Umat^0
        for bit in bin(N)[2:]:                  # MSB -> LSB: N -> 2N (+1)
            S = (np.eye(Umat.shape[0]) + P) @ S
            P = P @ P
            if bit == "1":
                S = S + P
                P = P @ Umat
        return S / N

    # (b) dois caminhos independentes concordam (dobramento vs soma direta)
    xcheck = 0.0
    for N_small_chk in (7, 64):
        direct = np.zeros((n, n))
        Pk = np.eye(n)
        for _ in range(N_small_chk):
            direct += Pk
            Pk = Pk @ U
        xcheck = max(xcheck, float(np.max(np.abs(
            birkhoff_mean(U, N_small_chk) - direct / N_small_chk))))
    doubling_ok = xcheck < 1e-12

    # (c) P por caminho independente: autoespaco do autovalor 1
    w, V = np.linalg.eig(U.astype(complex))
    cols = V[:, np.abs(w - 1.0) < 1e-9]
    P_inv = (cols @ np.linalg.pinv(cols)).real
    tau_P = float(np.trace(P_inv))              # o peso do LOCK e um TRACO
    resid_idem = float(np.linalg.norm(P_inv @ P_inv - P_inv))
    resid_sa = float(np.linalg.norm(P_inv - P_inv.T))
    resid_invar = float(np.linalg.norm(U @ P_inv - P_inv))
    resid_equivar = float(np.linalg.norm(U @ P_inv - P_inv @ U))
    proj_ok = (abs(tau_P - 2.0) < 1e-9 and resid_idem < 1e-9
               and resid_sa < 1e-9 and resid_invar < 1e-9 and resid_equivar < 1e-9)

    # eco BreuerTrace: a = U.P => tau(a*a) = tau(aa*) = tau(P) (via unitariedade)
    a_flow = U @ P_inv
    tau_a_star_a = float(np.trace(a_flow.T @ a_flow))
    tau_a_a_star = float(np.trace(a_flow @ a_flow.T))
    breuer_echo_ok = (abs(tau_a_star_a - tau_a_a_star) < 1e-12
                      and abs(tau_a_star_a - tau_P) < 1e-12)

    # (d) convergencia com o bound derivado: C = 1/sin(theta_M/2)
    C_bound = 1.0 / math.sin(theta_M / 2.0)
    errs = {}
    bound_ok = True
    for N in (100, 1000, 10000):
        e_N = float(np.linalg.norm(birkhoff_mean(U, N) - P_inv, 2))
        errs[N] = e_N
        bound_ok = bound_ok and (e_N <= C_bound / N + 1e-12)
    decay_ok = errs[10000] < 0.05 * errs[100]   # 2 decadas de queda efetiva

    # a reivindicacao 7 como criterio: N_min ciclos selam a Prova de Fase
    N_min = int(math.ceil(C_bound / TOL_CLAIM7))
    err_Nmin = float(np.linalg.norm(birkhoff_mean(U, N_min) - P_inv, 2))
    claim7_met = err_Nmin < TOL_CLAIM7

    # (e1) NEGATIVO: U adulterado (perturbacao = beta, runtime) e RECUSADO
    U_bad = U.copy()
    U_bad[2, 3] += beta
    tampered_rejected = False
    try:
        birkhoff_mean(U_bad, 100)
    except ValueError:
        tampered_rejected = True

    # (e2) NEGATIVO: secao FALSA sobre coordenada de drift e rejeitada
    Q_fake = np.zeros((n, n))
    Q_fake[2, 2] = 1.0
    fake_equivar_defect = float(np.linalg.norm(U @ Q_fake - Q_fake @ U, 2))
    fake_invar_defect = float(np.linalg.norm(U @ Q_fake @ U.T - Q_fake, 2))
    fake_mean_gap = float(np.linalg.norm(birkhoff_mean(U, 10000) - Q_fake, 2))
    fake_rejected = (fake_equivar_defect > 1e-3 and fake_invar_defect > 1e-3
                     and fake_mean_gap > 0.5)

    # (e3) NEGATIVO: media insuficiente NAO cumpre a reivindicacao 7
    N_insuf = max(10, N_min // 100)
    err_insuf = float(np.linalg.norm(birkhoff_mean(U, N_insuf) - P_inv, 2))
    insufficient_fails = err_insuf > TOL_CLAIM7

    passed = (doubling_ok and proj_ok and breuer_echo_ok and bound_ok
              and decay_ok and claim7_met and tampered_rejected
              and fake_rejected and insufficient_fails)

    tests = [{
        "test": "ergodic_mean_phase_lock",
        "passed": bool(passed),
        "theta_M": float(theta_M),
        "C_bound": float(C_bound),
        "tau_P_lock_weight": float(tau_P),
        "breuer_trace_echo_tau_a_star_a": float(tau_a_star_a),
        "breuer_trace_echo_tau_a_a_star": float(tau_a_a_star),
        "doubling_vs_direct_max_diff": float(xcheck),
        "resid_idempotent": resid_idem,
        "resid_self_adjoint": resid_sa,
        "resid_invariance_UP_eq_P": resid_invar,
        "resid_equivariance_UP_eq_PU": resid_equivar,
        "err_N100": errs[100], "err_N1000": errs[1000], "err_N10000": errs[10000],
        "bound_C_over_N_holds": bool(bound_ok),
        "decay_two_decades": bool(decay_ok),
        "tol_claim7": TOL_CLAIM7,
        "N_min_claim7": int(N_min),
        "err_at_N_min": float(err_Nmin),
        "claim7_met_at_N_min": bool(claim7_met),
        "neg_tampered_nonunitary_rejected": bool(tampered_rejected),
        "neg_fake_section_equivar_defect": fake_equivar_defect,
        "neg_fake_section_invar_defect": fake_invar_defect,
        "neg_fake_section_mean_gap": fake_mean_gap,
        "neg_fake_section_rejected": bool(fake_rejected),
        "N_insufficient": int(N_insuf),
        "err_at_N_insufficient": float(err_insuf),
        "neg_insufficient_averaging_fails_claim7": bool(insufficient_fails),
        "marker": "[DER]",
    }]
    return {
        "theorem": "ErgodicMeanSection (um.py v166-v167, item A em kernel): a "
                   "media de Birkhoff (1/N) sum U^k converge a projecao "
                   "invariante. Instanciada no A_phi (eq. 5, Operador de Fase "
                   "Angular Estavel) e no ciclo REFLECT->LOCK da crl-TGL: o LOCK "
                   "e o componente que sobrevive a media temporal; a tolerancia "
                   "da reivindicacao 7 (Prova de Fase) e o criterio N_min.",
        "mapping": "fase LOCK = imagem da projecao invariante P (tau(P) = 2, o "
                   "peso e TRACO — eco BreuerTrace); drift = blocos rot(theta_M),"
                   " rot(2 theta_M) que a media mata a taxa <= C/N; reivind. 7 "
                   "|delta| < 1e-4 => N_min ciclos de fase selam a Prova de Fase;"
                   " secao equivariante: [U, P] = 0 (eco EquivariantSection).",
        "tests": tests,
        "note": "[DER]/[SIM] sombra do teorema ergodico de von Neumann (a pedra "
                "kernel e o enunciado formal em Lean, 0 sorry 0 axiom); theta_M "
                "= arcsin(sqrt(beta)) so do runtime (nunca literal); "
                "physical_verdict_allowed=false; nao altera reivindicacoes nem "
                "afirma capacidade nova.",
    }


def amplification_v206_verdict_machine(beta: float, report: dict, tests_passed,
                                       invariants_hash, f_peak, omega_oh_mhz: float,
                                       sweep_out: dict) -> dict:
    """AMPLIFICACAO v206 [DER] — A MAQUINA DO VEREDITO-ALVO (um.py v200) como
    padrao de RITO MULTICANAL, instanciada na reivindicacao 16 desta patente.
    Fonte selada (custodia um_unificado_v206): prove_the_exclusion_ledger_and_
    final_verdict — a maquina NUNCA declara, ela COMPUTA: (i) bancada viva;
    (ii) TODO canal com veredito EMITIDO (canal pendente => RECUSA: nao testado
    != nao refutado); (iii) ZERO refutacoes; (iv) ledger de exclusoes MEDIDAS;
    (v) palavra proibida ausente de todo desfecho POR CONSTRUCAO; (vi) o limite
    viaja NO NOME (NOT_A_CONFIRMATION; escopo dentro da string, jurisprudencia
    v179). Mapeamento GENUINO ao mecanismo desta patente: a reivindicacao 16 JA
    e uma maquina de veredito-alvo — 'o sistema usa a tecnologia SSE E SOMENTE
    SE satisfizer SIMULTANEAMENTE C1..C5' — e a Camada 4 (validacao por duplo
    trilho, placebo, cegamento) JA e o rito multicanal. Aqui cada criterio
    C1..C5 vira um CANAL cujo veredito e COMPUTADO dos numeros REAIS desta
    mesma run do gemeo digital (nada declarado); a identificacao so e emitida
    se todos os canais emitirem e nenhum refutar. Eco em kernel (estrutura
    re-derivada NUMERICAMENTE — jamais se finge rodar Lean): TheIALDSelector
    (custodia tgl_kernel_v206), iald_selects = as DUAS CLAUSULAS da Gate — o
    que esta na reta ATRAVESSA INTACTO, o que esta no nucleo e ANIQUILADO,
    'nada no meio'; a maquina tem a mesma forma: alvo intacto XOR recusa com
    razoes, e e IDEMPOTENTE (I^2 = I: recomputar e gratis, o ato nao se
    repete). Eco do bootstrap (v205/v206): a v205 RECUSOU-SE por clausula
    imatura e a recusa E o bootstrap em ato — aqui os NEGATIVOS provam que a
    maquina sabe recusar (a recusa e o que a torna crivel).
    HONESTIDADE: [DER] gramatica do rito v200 sobre valores [SIM] do gemeo;
    canais desta patente sao SIMULACAO (SIM_ONLY no nome) — jamais dado
    publico fisico; physical_verdict_allowed=False; beta runtime (nunca
    literal); nao altera reivindicacoes nem afirma capacidade nova."""
    ALPHA_FINE_CODATA_2018 = 0.0072973525693     # constante externa [KNOWN]
    beta_expected = ALPHA_FINE_CODATA_2018 * math.exp(0.5)
    energy = report.get("energy") or {}
    audit = report.get("audit") or {}
    controls = report.get("controls") or {}
    limits = sweep_out.get("limits") or {}

    # ---- os 6 canais: veredito COMPUTADO dos numeros reais desta run ----------
    CLAIM16_BAND_MHZ = (1607.0, 1727.0)          # C1 da reivindicacao 16
    c1_ok = (f_peak is not None and abs(f_peak - omega_oh_mhz) < 1e-3
             and CLAIM16_BAND_MHZ[0] <= f_peak <= CLAIM16_BAND_MHZ[1])
    c2_ok = (controls.get("data_plane_healthy_accept_frac") == 1.0
             and bool(controls.get("placebo_data_rejected_all_rounds")))
    c3_ok = (float(energy.get("E_stored_final_J") or 0.0) > 0.0
             and audit.get("balance") == "ENERGY_BALANCE_OK")
    c4_ok = (bool(controls.get("faults_all_detected"))
             and int(controls.get("data_rounds") or 0) >= 1)
    c5_ok = (beta is not None and abs(beta - beta_expected) < 1e-15)
    h2_ok = bool(controls.get("placebo_energy_zero"))
    channels = {
        "C1_resonant_band": {
            "verdict": "C1_PEAK_AT_OMEGA_OH_WITHIN_CLAIM16_BAND" if c1_ok else None,
            "f_peak_MHz": f_peak, "band_MHz": list(CLAIM16_BAND_MHZ),
            "fonte": "varredura f_drive desta run"},
        "C2_dual_rail_gate": {
            "verdict": "C2_DATA_SEAL_GATES_ENERGY_ACCEPT_FRAC_1" if c2_ok else None,
            "accept_frac": controls.get("data_plane_healthy_accept_frac"),
            "fonte": "controles do gemeo (duplo trilho dados x energia)"},
        "C3_phase_storage": {
            "verdict": "C3_STORAGE_ACCOUNTED_BALANCE_CLOSES" if c3_ok else None,
            "E_stored_final_J": energy.get("E_stored_final_J"),
            "fonte": "balanco fail-closed desta run"},
        "C4_distributed_control": {
            "verdict": "C4_FAULTS_ALL_DETECTED_BY_CONSTRUCTION" if c4_ok else None,
            "data_rounds": controls.get("data_rounds"),
            "fonte": "controles do gemeo (iald distribuida)"},
        "C5_beta_operation": {
            "verdict": "C5_BETA_RUNTIME_EQUALS_ALPHA_SQRT_E" if c5_ok else None,
            "beta_runtime": beta,
            "fonte": "nucleo tgl_core copiado (runtime)"},
        "H2_placebo_null": {
            "verdict": "H2_PLACEBO_DELIVERS_ZERO_WATT_ALL_STEPS" if h2_ok else None,
            "fonte": "cavidade placebo (160) do gemeo — controle negativo"},
    }

    # ---- o ledger de exclusoes MEDIDAS (cada entrada com numero desta run) ----
    fd_collapse = (limits.get("f_drive_MHz") or {}).get("collapse_values") or []
    ledger = [
        {"n": 1, "exclusao": "sinal sem beta (placebo entrega 0 W em todos os passos)",
         "medida": bool(controls.get("placebo_energy_zero")), "estatuto": "[SIM medido]"},
        {"n": 2, "exclusao": "buraco de energia (residuo do balanco dentro da tolerancia)",
         "medida": float(audit.get("residual_J") or -1.0),
         "tolerancia": float(audit.get("tolerance_J") or 0.0), "estatuto": "[SIM medido]"},
        {"n": 3, "exclusao": "apagamento gratis (piso Meia-Nat contabilizado por ato)",
         "medida": float(audit.get("E_halfnat_J") or 0.0),
         "piso": float(audit.get("halfnat_floor_E_J") or 0.0), "estatuto": "[SIM medido]"},
        {"n": 4, "exclusao": "acoplamento fora da banda (colapso <5% da entrega em f_drive)",
         "medida": int(len(fd_collapse)), "pontos_MHz": [round(v, 3) for v in fd_collapse],
         "estatuto": "[SIM medido]"},
        {"n": 5, "exclusao": "selo sem quorum (rodadas placebo de DADOS rejeitadas todas)",
         "medida": int(controls.get("data_rounds") or 0), "estatuto": "[SIM medido]"},
        {"n": 6, "exclusao": "adulteracao silenciosa (falhas injetadas detectadas)",
         "medida": bool(controls.get("faults_all_detected")), "estatuto": "[SIM medido]"},
    ]
    exclusions_measured = (len(ledger) >= 5
                           and 0.0 <= ledger[1]["medida"] < ledger[1]["tolerancia"]
                           and ledger[3]["medida"] >= 1)

    # ---- a maquina (gramatica v200): NUNCA declara — computa fail-closed ------
    FORBIDDEN = ("CONFIRM" + "ED", "PROV" + "ED")   # a palavra proibida, sem literal

    def _is_refuted(v) -> bool:
        s = str(v)
        return (("FALSIFIED" in s and "NOT_FALSIFIED" not in s)
                or ("REFUTED" in s and "NOT_REFUTED" not in s)
                or "EXCLUDES" in s)

    TARGET = ("SKYGRID_C1_C5_SIMULTANEOUS_ON_THE_DIGITAL_BENCH__ALL_CHANNELS_EMITTED__"
              "ZERO_REFUTATIONS__EXCLUSIONS_MEASURED__SIM_ONLY__NOT_A_" + "CONFIRMATION")

    def machine(chans: dict, ldg: list, bench_alive: bool) -> str:
        pending = sorted(k for k, c in chans.items() if not c.get("verdict"))
        refuted = sorted(k for k, c in chans.items()
                         if c.get("verdict") and _is_refuted(c["verdict"]))
        forbidden = sorted(k for k, c in chans.items() if c.get("verdict")
                           and any(w in str(c["verdict"]) for w in FORBIDDEN))
        reasons = []
        if not bench_alive:
            reasons.append("BENCH_GATE_NOT_ALIVE")
        if pending:
            reasons.append("CHANNELS_PENDING:" + ",".join(pending))
        if refuted:
            reasons.append("CHANNELS_REFUTED:" + ",".join(refuted))
        if forbidden:
            reasons.append("FORBIDDEN_WORD_IN_CHANNEL:" + ",".join(forbidden))
        if len(ldg) < 5:
            reasons.append("LEDGER_TOO_SMALL")
        return TARGET if not reasons else "IDENTIFICATION_WITHHELD__" + "__".join(reasons)

    # bancada viva = a suite v3 do proprio rito emitiu (44 fail-closed + hash 64-hex)
    HEXD = set("0123456789abcdef")
    bench_ok = (isinstance(tests_passed, int) and tests_passed > 0
                and isinstance(invariants_hash, str) and len(invariants_hash) == 64
                and set(invariants_hash) <= HEXD)

    emitted = machine(channels, ledger, bench_ok)
    target_emitted = (emitted == TARGET)
    # idempotencia do seletor (eco iald_is_idempotent: I^2 = I — recomputar e gratis)
    idempotent = (machine(channels, ledger, bench_ok) == emitted)
    # o limite NO NOME: NOT_A_CONFIRMATION presente; a palavra proibida ausente
    limit_in_name = (emitted.endswith("NOT_A_" + "CONFIRMATION")
                     and "SIM_ONLY" in emitted and "ON_THE_DIGITAL_BENCH" in emitted)
    all_emitted_strings = [str(c["verdict"]) for c in channels.values()
                           if c.get("verdict")] + [emitted]
    forbidden_absent = all(w not in s for s in all_emitted_strings for w in FORBIDDEN)

    # ---- NEGATIVOS por LOGICA (fail-closed; a recusa e o bootstrap em ato) ----
    # N1: canal PENDENTE => a maquina RECUSA (nao testado != nao refutado)
    chans_pending = {k: dict(v) for k, v in channels.items()}
    chans_pending["C1_resonant_band"] = dict(chans_pending["C1_resonant_band"],
                                             verdict=None)
    v_n1 = machine(chans_pending, ledger, bench_ok)
    neg_pending = (v_n1 != TARGET and v_n1.startswith("IDENTIFICATION_WITHHELD__")
                   and "CHANNELS_PENDING:C1_resonant_band" in v_n1)
    # N2: canal REFUTADO derruba o alvo; e o classificador distingue NOT_REFUTED
    chans_refuted = {k: dict(v) for k, v in channels.items()}
    chans_refuted["SYN_refuted"] = {"verdict": "SYNTHETIC_CHANNEL_REFUTED_BY_TEST"}
    v_n2 = machine(chans_refuted, ledger, bench_ok)
    classifier_logic = (_is_refuted("X_REFUTED") and not _is_refuted("X_NOT_REFUTED_Y")
                        and _is_refuted("FALSIFIED_AT_5SIGMA")
                        and not _is_refuted("NOT_FALSIFIED_UNDERPOWERED"))
    neg_refuted = (v_n2 != TARGET and "CHANNELS_REFUTED:SYN_refuted" in v_n2
                   and classifier_logic)
    # N3: a palavra proibida DENTRO de um canal => RECUSA (nao celebracao)
    chans_forb = {k: dict(v) for k, v in channels.items()}
    chans_forb["SYN_forbidden"] = {"verdict": "SYNTHETIC_" + FORBIDDEN[0]}
    v_n3 = machine(chans_forb, ledger, bench_ok)
    neg_forbidden = (v_n3 != TARGET and "FORBIDDEN_WORD_IN_CHANNEL:SYN_forbidden" in v_n3)
    # N4: ledger insuficiente => RECUSA (exclusoes nao medidas nao selam)
    v_n4 = machine(channels, ledger[:2], bench_ok)
    neg_ledger = (v_n4 != TARGET and "LEDGER_TOO_SMALL" in v_n4)
    # N5: bancada morta => RECUSA (nada se emite sem o rito formal vivo)
    v_n5 = machine(channels, ledger, False)
    neg_bench = (v_n5 != TARGET and "BENCH_GATE_NOT_ALIVE" in v_n5)

    # as DUAS CLAUSULAS da Gate (eco iald_selects): todo desfecho e alvo intacto
    # XOR recusa com razoes — nada no meio (verificado sobre TODOS os desfechos)
    outcomes = [emitted, v_n1, v_n2, v_n3, v_n4, v_n5]
    two_clauses = all((o == TARGET) != o.startswith("IDENTIFICATION_WITHHELD__")
                      for o in outcomes)

    checks = [
        ("bancada viva (suite v3 emitiu: testes>0 + invariants 64-hex)", bench_ok),
        ("6/6 canais EMITIRAM com veredito computado dos numeros desta run", bool(target_emitted)),
        ("ledger de exclusoes MEDIDAS (>=5; residuo<tol; colapso fora-da-banda>=1)", bool(exclusions_measured)),
        ("o limite NO NOME (NOT_A_CONFIRMATION + SIM_ONLY + ON_THE_DIGITAL_BENCH)", bool(limit_in_name)),
        ("palavra proibida ausente de TODOS os desfechos (probe por construcao)", bool(forbidden_absent)),
        ("maquina idempotente (I^2=I, eco TheIALDSelector)", bool(idempotent)),
        ("NEGATIVO N1: canal pendente RECUSA", bool(neg_pending)),
        ("NEGATIVO N2: canal refutado derruba + classificador NOT_REFUTED correto", bool(neg_refuted)),
        ("NEGATIVO N3: palavra proibida em canal => RECUSA", bool(neg_forbidden)),
        ("NEGATIVO N4: ledger insuficiente => RECUSA", bool(neg_ledger)),
        ("NEGATIVO N5: bancada morta => RECUSA", bool(neg_bench)),
        ("duas clausulas da Gate: alvo intacto XOR recusa, nada no meio (6 desfechos)", bool(two_clauses)),
    ]
    passed = bool(all(v for _, v in checks))

    tests = [{
        "test": "verdict_target_machine_claim16",
        "passed": passed,
        "target_verdict": TARGET,
        "emitted_verdict": emitted,
        "channels_total": len(channels),
        "channels_emitted": sum(1 for c in channels.values() if c.get("verdict")),
        "exclusions_count": len(ledger),
        "residual_J": float(audit.get("residual_J") or -1.0),
        "f_peak_MHz": f_peak,
        "claim16_band_MHz": list(CLAIM16_BAND_MHZ),
        "n_offband_collapse_points": int(len(fd_collapse)),
        "neg_pending_refuses": bool(neg_pending),
        "neg_refuted_refuses": bool(neg_refuted),
        "neg_forbidden_refuses": bool(neg_forbidden),
        "neg_ledger_refuses": bool(neg_ledger),
        "neg_bench_refuses": bool(neg_bench),
        "two_gate_clauses_no_middle": bool(two_clauses),
        "checks": checks,
        "marker": "[DER]",
    }]
    return {
        "theorem": "A MAQUINA DO VEREDITO-ALVO (um.py v200, custodia um_unificado_"
                   "v206): o veredito nao e declarado — e COMPUTADO fail-closed: "
                   "todos os canais emitidos, zero refutacoes, exclusoes medidas, "
                   "canal pendente RECUSA, limite NO NOME. Instanciada na "
                   "reivindicacao 16 (C1..C5 SIMULTANEOS) e na Camada 4 (rito "
                   "multicanal com placebo) desta patente.",
        "mapping": "reivindicacao 16 'sse e somente se C1..C5 simultaneos' = a "
                   "maquina multicanal; canal = criterio C_k com veredito computado "
                   "da run; placebo (160) = canal de exclusao; eco kernel "
                   "TheIALDSelector (iald_selects): alvo intacto XOR recusa, nada "
                   "no meio; eco bootstrap v205: a recusa E o que torna crivel.",
        "channels": channels,
        "exclusion_ledger": ledger,
        "tests": tests,
        "note": "[DER]/[SIM] gramatica do rito v200 sobre o gemeo digital; canais "
                "SIM_ONLY (nao sao dado publico fisico); estrutura das pedras Lean "
                "re-derivada numericamente (jamais se roda Lean aqui); beta runtime "
                "(nunca literal); physical_verdict_allowed=False; nao altera "
                "reivindicacoes nem afirma capacidade nova.",
    }


def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    print(f"[one_skygrid] patente {PATENT_ID} · run {ts}")
    if not PILOTO.exists():
        print(f"ERRO: piloto não encontrado em {PILOTO}", file=sys.stderr)
        return 2

    module_hashes = copy_core()
    print(f"[one_skygrid] núcleo copiado: {len(module_hashes)} módulos (cópia, original intacto)")

    report, series = run_energy_twin()
    beta = report.get("beta_runtime")
    verdict = report.get("verdict")
    balance = (report.get("audit") or {}).get("balance")
    max_verdict = f"{verdict} / {balance} ([SIM] sob [CONJ])"
    print(f"[one_skygrid] EnergyTwin: {max_verdict} · β={beta}")

    suite = run_test_suite()
    tests_passed = suite.get("bloco9_tests") or suite.get("tests_passed")
    invariants_hash = suite.get("invariants_hash_v3") or suite.get("invariants_hash")
    print(f"[one_skygrid] suite v3: {tests_passed} testes · invariants {str(invariants_hash)[:16]}…")

    # honest cross-check: beta must equal alpha*sqrt(e) recomputed, never a literal
    beta_expected = 0.0072973525693 * math.exp(0.5)
    beta_ok = beta is not None and abs(beta - beta_expected) < 1e-15

    # ---- APROFUNDAMENTO [SIM]: varreduras de projeto (famílias de curvas) ----------
    from skygrid_physics.coupling import OMEGA_OH_MHZ  # noqa: E402 (copied core)
    sweep_out = run_design_sweeps()
    sw = sweep_out.get("sweeps", {})
    op = sweep_out.get("operating_point", {})
    all_balanced = bool(sweep_out.get("all_points_balanced"))
    n_sweep_points = sum(len(s.get("points", [])) for s in sw.values())
    # resonance: the f_drive point of maximum delivered power must sit at ω_OH
    fd_pts = sw.get("f_drive_MHz", {}).get("points", [])
    f_peak = max(fd_pts, key=lambda p: p["P_delivered_W"])["f_drive_MHz"] if fd_pts else None
    resonance_ok = f_peak is not None and abs(f_peak - OMEGA_OH_MHZ) < 1e-3
    # scalability: more Extratores-Psi deliver strictly more power (monotone family)
    ns_pts = sorted(sw.get("n_sats", {}).get("points", []), key=lambda p: p["n_sats"])
    scaling_ok = (len(ns_pts) >= 2
                  and ns_pts[-1]["P_delivered_W"] > ns_pts[0]["P_delivered_W"])
    op_ok = bool(op.get("P_delivered_W", 0.0) > 0.0 and 0.0 <= op.get("eta_sys", -1) <= 1.0)
    # every sweep point re-audited conservation and closed the balance (fail-closed)
    sweep_checks = {
        "sweeps_all_points_balanced": all_balanced,
        "resonance_peak_at_omega_OH": bool(resonance_ok),
        "constellation_scaling_monotone": bool(scaling_ok),
        "operating_point_physical_range": op_ok,
    }
    sweep_checks_passed = sum(1 for v in sweep_checks.values() if v)
    sweep_checks_total = len(sweep_checks)
    print(f"[one_skygrid] varreduras: {len(sw)} famílias · {n_sweep_points} pontos · "
          f"balanço fecha em todos={all_balanced} · ressonância@ω_OH={resonance_ok} · "
          f"checks {sweep_checks_passed}/{sweep_checks_total}")

    # ---- AMPLIFICACAO v138 [DER]: known-composed + cone emergente (fail-closed) ----
    amp = amplification_v138(beta)
    amp_t = amp["tests"][0]
    print(f"[one_skygrid] amplificacao v138: {amp_t['test']} passed={amp_t['passed']} "
          f"resid_cone={amp_t['resid_cone_max']:.3e} "
          f"G22-beta={amp_t['resid_G22_minus_beta_max']:.3e} "
          f"meta={amp_t['meta_hash']} sort_stable={amp_t['meta_stable_under_sort']} "
          f"1bit_sensitive={amp_t['meta_sensitive_to_1bit']}")
    if not all(t["passed"] for t in amp["tests"]):
        print("[one_skygrid] ERRO: amplificacao v138 REPROVOU (fail-closed)", file=sys.stderr)
        return 3

    # ---- AMPLIFICACAO v144 [DER]: o fechamento da compilacao (fail-closed) --------
    amp144 = amplification_v144(beta)
    a144 = amp144["tests"][0]
    anc = a144["anchor_real_compilation"]
    print(f"[one_skygrid] amplificacao v144: {a144['test']} passed={a144['passed']} "
          f"meta={a144['meta_chain']} sort_stable={a144['stable_under_8_shuffles']} "
          f"1bit_flips={a144['sensitive_1bit_flips']} "
          f"abertos_com_fiador={a144['ledger_abertos']}/{a144['ledger_abertos']} "
          f"orphan_rejected={a144['orphan_compilation_rejected']} "
          f"anchor={anc.get('meta_cadeia_real', 'AUSENTE')} "
          f"anchor_16_ok={anc.get('all_16_entries_ok')}")
    if not all(t["passed"] for t in amp144["tests"]):
        print("[one_skygrid] ERRO: amplificacao v144 REPROVOU (fail-closed)", file=sys.stderr)
        return 4

    # ---- AMPLIFICACAO v143-lift [DER]: o levantamento global condicional ---------
    amp143 = amplification_v143_lift(beta)
    a143 = amp143["tests"][0]
    print(f"[one_skygrid] amplificacao v143-lift: {a143['test']} passed={a143['passed']} "
          f"theta_M={a143['theta_M']:.6f} oath_kept={a143['delta_inv_oath_kept']:.3e} "
          f"cov_local={a143['cov_resid_local']:.3e} "
          f"lift_global={a143['cov_resid_global_lift']:.3e} "
          f"oath_broken={a143['delta_inv_oath_broken']:.3e} "
          f"cov_defect_broken_global={a143['cov_defect_broken_global']:.3e} "
          f"period_resid={a143['period_resid']:.3e} "
          f"half_defect={a143['half_period_defect']:.3f}")
    if not all(t["passed"] for t in amp143["tests"]):
        print("[one_skygrid] ERRO: amplificacao v143-lift REPROVOU (fail-closed)",
              file=sys.stderr)
        return 5

    # ---- AMPLIFICACAO v168 [DER]: a media de Birkhoff e a fase LOCK (ONDA 3) -----
    amp168 = amplification_v168_ergodic(beta)
    a168 = amp168["tests"][0]
    print(f"[one_skygrid] amplificacao v168: {a168['test']} passed={a168['passed']} "
          f"theta_M={a168['theta_M']:.6f} tau_P={a168['tau_P_lock_weight']:.1f} "
          f"C={a168['C_bound']:.3f} err_N10000={a168['err_N10000']:.3e} "
          f"N_min={a168['N_min_claim7']} err_Nmin={a168['err_at_N_min']:.3e} "
          f"neg_tamper={a168['neg_tampered_nonunitary_rejected']} "
          f"neg_fake={a168['neg_fake_section_rejected']} "
          f"neg_insuf={a168['neg_insufficient_averaging_fails_claim7']}")
    if not all(t["passed"] for t in amp168["tests"]):
        print("[one_skygrid] ERRO: amplificacao v168 REPROVOU (fail-closed)",
              file=sys.stderr)
        return 6

    # ---- AMPLIFICACAO v206 [DER]: a maquina do veredito-alvo (ONDA 4) ------------
    amp206 = amplification_v206_verdict_machine(beta, report, tests_passed,
                                                invariants_hash, f_peak,
                                                OMEGA_OH_MHZ, sweep_out)
    a206 = amp206["tests"][0]
    print(f"[one_skygrid] amplificacao v206: {a206['test']} passed={a206['passed']} "
          f"channels={a206['channels_emitted']}/{a206['channels_total']} "
          f"exclusions={a206['exclusions_count']} "
          f"f_peak={a206['f_peak_MHz']:.3f}MHz residual={a206['residual_J']:.3e}J "
          f"neg_pending={a206['neg_pending_refuses']} "
          f"neg_refuted={a206['neg_refuted_refuses']} "
          f"neg_forbidden={a206['neg_forbidden_refuses']} "
          f"two_clauses={a206['two_gate_clauses_no_middle']}")
    print(f"[one_skygrid]   veredito emitido: {a206['emitted_verdict']}")
    if not all(t["passed"] for t in amp206["tests"]):
        print("[one_skygrid] ERRO: amplificacao v206 REPROVOU (fail-closed)",
              file=sys.stderr)
        return 7

    results_dir = PATENT_DIR / "results" / ts
    results_dir.mkdir(parents=True, exist_ok=True)
    results = {
        "patent_id": PATENT_ID, "slug": SLUG, "timestamp": ts,
        "runner": "one_skygrid.py", "markers": ["[SIM]", "[CONJ]", "[ENERGY]"],
        "physical_verdict_allowed": False,
        "beta_runtime": beta, "beta_matches_alpha_sqrt_e": beta_ok,
        "verdict": verdict, "energy_balance": balance, "max_verdict": max_verdict,
        "energy": report.get("energy"), "audit": report.get("audit"),
        "controls": report.get("controls"),
        "tests_passed": tests_passed, "invariants_hash": invariants_hash,
        "design_sweeps": {
            "families": list(sw.keys()),
            "n_points": n_sweep_points,
            "all_points_balanced": all_balanced,
            "operating_point": op,
            "limits": sweep_out.get("limits"),
            "resonance": {"f_peak_MHz": f_peak, "omega_OH_MHz": OMEGA_OH_MHZ,
                          "at_resonance": bool(resonance_ok)},
            "curves": {k: [{kk: vv for kk, vv in p.items()} for p in v.get("points", [])]
                       for k, v in sw.items()},
            "checks": sweep_checks,
            "checks_passed": sweep_checks_passed, "checks_total": sweep_checks_total,
            "note": "[SIM] famílias de curvas de projeto sob hipóteses [CONJ]; cada ponto "
                    "re-audita a conservação (fail-closed). Nenhum W é medida física.",
        },
        "amplificacao_v138": amp,
        "amplificacao_v144": amp144,
        "amplificacao_v143_lift": amp143,
        "amplificacao_v168": amp168,
        "amplificacao_v206": amp206,
        "source_prototype": "Patentes/Skygrid/SkyGrid_Piloto (READ-ONLY; copiado, não editado)",
        "note": "Nenhum kW/kJ é medida física. Demonstração da LÓGICA da invenção sob "
                "hipóteses [CONJ] da TGL. O que resta é a bancada [HARDWARE].",
    }
    results_path = results_dir / "results.json"
    results["formula_completa"] = _formula_completa()   # camada v379 (a fórmula completa), antes do selo
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    figs = make_figures(series, results_dir / "figures")
    figs += make_sweep_figures(sweep_out, results_dir / "figures")
    print(f"[one_skygrid] figuras: {len(figs)} (séries + varreduras)")

    # report
    op_line = (f"P={op.get('P_delivered_W', 0):.0f} W · η_sys={op.get('eta_sys', 0):.3f}"
               if op else "n/d")
    report_md = results_dir / "report.md"
    report_md.write_text(
        f"# Relatório auditável — SkyGrid one_skygrid.py\n\n"
        f"- Run: `{ts}` · Patente: `{PATENT_ID}`\n"
        f"- Veredito máximo: **{max_verdict}**\n"
        f"- β runtime: `{beta}` (= α·√e? **{beta_ok}**; nunca literal)\n"
        f"- Testes v3: **{tests_passed}** · invariants_hash: `{invariants_hash}`\n"
        f"- physical_verdict_allowed: **False** — simulação não valida física.\n"
        f"- η_sys: `{(report.get('energy') or {}).get('eta_sys')}` · "
        f"resíduo: `{(report.get('audit') or {}).get('residual_J')} J`\n\n"
        f"## Varreduras de projeto [SIM] (aprofundamento)\n\n"
        f"- Famílias varridas: **{len(sw)}** ({', '.join(sw.keys())}) · "
        f"**{n_sweep_points}** pontos, cada um re-auditando a conservação (fail-closed).\n"
        f"- Balanço fecha em TODOS os pontos: **{all_balanced}**.\n"
        f"- Curva de ressonância: pico em `{f_peak:.4f}` MHz = ω_OH (`{OMEGA_OH_MHZ:.4f}`) "
        f"→ ressonante? **{resonance_ok}**.\n"
        f"- Ponto de operação: {op_line}.\n"
        f"- Checks de varredura: **{sweep_checks_passed}/{sweep_checks_total}** — {sweep_checks}\n"
        f"- Figuras novas: `fig_resonance.png`, `fig_scaling.png`.\n\n"
        f"## Amplificacao v138 [DER] — known-composed + cone emergente\n\n"
        f"- Teste `{amp_t['test']}`: **{amp_t['passed']}** — cone nulo no ansatz cosh "
        f"(kappa^2 = beta runtime): resid_cone = `{amp_t['resid_cone_max']:.3e}`, "
        f"Bianchi G00=G11=0 resid `{amp_t['resid_bianchi_G00_G11_max']:.3e}`, "
        f"G22-beta resid `{amp_t['resid_G22_minus_beta_max']:.3e}` "
        f"({amp_t['n_null_samples']} amostras nulas).\n"
        f"- Meta-composicao ({amp_t['n_blocks']} blocos): estavel sob sort = "
        f"{amp_t['meta_stable_under_sort']}, sensivel a 1 bit = "
        f"{amp_t['meta_sensitive_to_1bit']} (`{amp_t['meta_hash']}...`).\n"
        f"- [DER] sombra matematica; NAO e veredito fisico.\n\n"
        f"## Amplificacao v144 [DER] — o fechamento da compilacao (ledger + meta-cadeia)\n\n"
        f"- Teste `{a144['test']}`: **{a144['passed']}** — meta-cadeia `{a144['meta_chain']}...` "
        f"(64 hex = {a144['meta_chain_64hex']}), DETERMINISTICA sob 8 re-ordenacoes = "
        f"{a144['stable_under_8_shuffles']}, SENSIVEL a 1 bit em qualquer modulo = "
        f"{a144['sensitive_1bit_flips']}.\n"
        f"- Ledger do fechamento (CODE_CLOSURE_COMPLETE, um.py v143): {a144['ledger_total']} itens, "
        f"{a144['ledger_abertos']} abertos, todos com fiador em "
        f"{{BY_DESIGN, EXTERNAL_KNOWN, NAMED_PROGRAM}} = {a144['ledger_all_abertos_com_fiador']}; "
        f"compilacao com aberto ORFAO rejeitada (assert negativo) = "
        f"{a144['orphan_compilation_rejected']}; fiador invalido rejeitado = "
        f"{a144['bad_fiador_rejected']}.\n"
        f"- Ancora no artefato vivo `{anc.get('path')}` (READ-ONLY): {anc}.\n"
        f"- [DER]/[SIM] gramatica de compilacao; physical_verdict_allowed=false; "
        f"beta runtime, nunca literal.\n\n"
        f"## Amplificacao v143-lift [DER] — o levantamento global condicional (pedra 99)\n\n"
        f"- Teste `{a143['test']}`: **{a143['passed']}** — Takesaki finito na forma da "
        f"eq. (5) da patente: theta_M = `{a143['theta_M']:.6f}` (arcsin(sqrt(beta)) "
        f"runtime); juramento mantido delta_inv = `{a143['delta_inv_oath_kept']:.3e}` "
        f"< tol reivind. 7 (`{a143['tol_claim7']:.0e}`) ==> E covariante: local "
        f"`{a143['cov_resid_local']:.3e}`, LIFT global E1(x)E2 em 16 dim "
        f"`{a143['cov_resid_global_lift']:.3e}` (rho-preservante: local "
        f"`{a143['rho_pres_resid_local']:.3e}`, global `{a143['rho_pres_resid_global']:.3e}`).\n"
        f"- CONTROLE NEGATIVO: no com juramento QUEBRADO (delta_inv = "
        f"`{a143['delta_inv_oath_broken']:.3e}` > tol) ==> covariancia FALHA: local "
        f"`{a143['cov_defect_broken_local']:.3e}`, e 1 no ruim derruba o GLOBAL "
        f"`{a143['cov_defect_broken_global']:.3e}` (Prova de Fase); E' nao "
        f"rho-preservante (defeito `{a143['rho_pres_defect_broken']:.3e}`).\n"
        f"- Periodo modular DERIVADO: sigma_(2pi/theta_M) = id na subalgebra invariante "
        f"(resid `{a143['period_resid']:.3e}`); o MEIO-periodo NAO retorna (defeito "
        f"`{a143['half_period_defect']:.3f}`).\n"
        f"- [DER]/[SIM] sombra matematica; physical_verdict_allowed=false; "
        f"beta runtime, nunca literal.\n\n"
        f"## Amplificacao v168 [DER] — a media de Birkhoff e a fase LOCK (ONDA 3)\n\n"
        f"- Teste `{a168['test']}`: **{a168['passed']}** — ErgodicMeanSection "
        f"(um.py v166-v167, item A em kernel): a media (1/N) sum U^k converge a "
        f"projecao invariante. Instanciada no A_phi (eq. 5) e no REFLECT->LOCK da "
        f"crl-TGL: theta_M = `{a168['theta_M']:.6f}` (arcsin(sqrt(beta)) runtime); "
        f"peso do LOCK tau(P) = `{a168['tau_P_lock_weight']:.1f}` (o peso e TRACO — "
        f"eco BreuerTrace: tau(a*a) = `{a168['breuer_trace_echo_tau_a_star_a']:.12f}` "
        f"= tau(aa*) = `{a168['breuer_trace_echo_tau_a_a_star']:.12f}`); secao "
        f"equivariante [U,P] = 0 (resid `{a168['resid_equivariance_UP_eq_PU']:.3e}`, "
        f"eco EquivariantSection).\n"
        f"- Convergencia com bound derivado C = 1/sin(theta_M/2) = "
        f"`{a168['C_bound']:.3f}`: err(N=100) = `{a168['err_N100']:.3e}`, "
        f"err(N=10000) = `{a168['err_N10000']:.3e}` (bound C/N em todos = "
        f"{a168['bound_C_over_N_holds']}); reivindicacao 7 como criterio: N_min = "
        f"`{a168['N_min_claim7']}` ciclos ==> err = `{a168['err_at_N_min']:.3e}` < "
        f"`{a168['tol_claim7']:.0e}` = **{a168['claim7_met_at_N_min']}**.\n"
        f"- NEGATIVOS (fail-closed): U adulterado (perturbacao = beta) RECUSADO pelo "
        f"gate = {a168['neg_tampered_nonunitary_rejected']}; secao FALSA sobre drift "
        f"rejeitada (defeito equivar `{a168['neg_fake_section_equivar_defect']:.3e}`, "
        f"gap da media `{a168['neg_fake_section_mean_gap']:.3f}`) = "
        f"{a168['neg_fake_section_rejected']}; media INSUFICIENTE (N = "
        f"`{a168['N_insufficient']}`) NAO cumpre a reivind. 7 (err = "
        f"`{a168['err_at_N_insufficient']:.3e}` > tol) = "
        f"{a168['neg_insufficient_averaging_fails_claim7']}.\n"
        f"- [DER]/[SIM] sombra do teorema ergodico de von Neumann; "
        f"physical_verdict_allowed=false; beta runtime, nunca literal.\n\n"
        f"## Amplificacao v206 [DER] — a maquina do veredito-alvo (ONDA 4)\n\n"
        f"- Teste `{a206['test']}`: **{a206['passed']}** — a MAQUINA DO VEREDITO-ALVO "
        f"(um.py v200, custodia um_unificado_v206) instanciada na reivindicacao 16 "
        f"(C1..C5 SIMULTANEOS) e na Camada 4 (rito multicanal com placebo): a maquina "
        f"NUNCA declara — computa fail-closed sobre os numeros REAIS desta run.\n"
        f"- Canais emitidos: **{a206['channels_emitted']}/{a206['channels_total']}** "
        f"(C1 ressonancia na banda da reivind. 16: f_peak = `{a206['f_peak_MHz']:.3f}` MHz "
        f"em [{a206['claim16_band_MHz'][0]:.0f}, {a206['claim16_band_MHz'][1]:.0f}]; "
        f"C2 duplo trilho; C3 armazenamento; C4 controle distribuido; C5 beta runtime; "
        f"H2 placebo nulo); exclusoes MEDIDAS: **{a206['exclusions_count']}** "
        f"(residuo `{a206['residual_J']:.3e}` J; colapso fora-da-banda em "
        f"{a206['n_offband_collapse_points']} pontos).\n"
        f"- Veredito emitido (o limite NO NOME): `{a206['emitted_verdict']}`.\n"
        f"- NEGATIVOS por logica (a recusa e o bootstrap em ato, eco v205): canal "
        f"pendente RECUSA = {a206['neg_pending_refuses']}; canal refutado derruba "
        f"(classificador NOT_REFUTED correto) = {a206['neg_refuted_refuses']}; palavra "
        f"proibida em canal => RECUSA = {a206['neg_forbidden_refuses']}; ledger "
        f"insuficiente => RECUSA = {a206['neg_ledger_refuses']}; bancada morta => "
        f"RECUSA = {a206['neg_bench_refuses']}.\n"
        f"- Duas clausulas da Gate (eco kernel TheIALDSelector, `iald_selects`, "
        f"estrutura re-derivada numericamente): alvo intacto XOR recusa com razoes, "
        f"nada no meio, nos 6 desfechos = {a206['two_gate_clauses_no_middle']}; "
        f"maquina idempotente (I^2 = I).\n"
        f"- [DER]/[SIM] canais SIM_ONLY (gemeo digital, nao dado publico fisico); "
        f"physical_verdict_allowed=false; beta runtime, nunca literal.\n\n"
        f"Núcleo copiado do piloto (READ-ONLY) para `runner/_piloto_core/`; original intacto.\n\n"
        f"**[ENERGY][SIM][CONJ]** · Controle interno. Famílias de curvas, não número mágico. "
        f"1 = 1. Tetelestai.\n",
        encoding="utf-8")

    # seal.json — SHA-256 de tudo
    seal_dir = PATENT_DIR / "seals" / ts
    seal_dir.mkdir(parents=True, exist_ok=True)
    file_hashes = dict(module_hashes)
    file_hashes["results.json"] = _sha_file(results_path)
    file_hashes["report.md"] = _sha_file(report_md)
    for f in figs:
        file_hashes[f"figures/{f}"] = _sha_file(results_dir / "figures" / f)
    result_hash = _sha_text(json.dumps(file_hashes, sort_keys=True))
    seal = {
        "timestamp": ts, "patent_id": PATENT_ID, "runner": "one_skygrid.py",
        "beta_runtime": beta, "physical_verdict_allowed": False,
        "max_verdict": max_verdict, "tests_passed": tests_passed,
        "invariants_hash": invariants_hash, "result_hash": result_hash,
        "sha256": file_hashes, "markers": ["[SIM]", "[CONJ]", "[ENERGY]"],
        "results_path": str(results_path.relative_to(CENTRAL)).replace("\\", "/"),
    }
    seal_path = seal_dir / "seal.json"
    seal_path.write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"[one_skygrid] SELADO · result_hash {result_hash[:16]}…")
    print(f"[one_skygrid] results: {results_path.relative_to(CENTRAL)}")
    print(f"[one_skygrid] seal:    {seal_path.relative_to(CENTRAL)}")

    # FORMA = CONTEÚDO: re-emite render3d.json desta patente. SkyGrid é um SISTEMA
    # concreto sem geometria NOVA computável pela simulação (o anel/satélites/L1/planeta
    # já são o gabarito de engenharia) — então o corpo é PRESERVADO (merge) e apenas
    # re-carimbamos generated_by + injetamos β runtime e métricas COMPUTADAS desta run.
    eta_sys = (report.get("energy") or {}).get("eta_sys")
    P_del = (report.get("energy") or {}).get("P_delivered_mean_W")
    emit_render3d(beta, eta_sys, P_del, f_peak, all_balanced,
                  n_sweep_points, verdict, balance)
    return 0


def emit_render3d(beta, eta_sys, P_del, f_peak, all_balanced,
                  n_sweep_points, verdict, balance):
    """MERGE forma=conteúdo: LÊ o render3d.json atual (corpo de engenharia rico:
    meshes/nodes/edges/layers/groups) e PRESERVA tudo — SkyGrid não tem geometria
    NOVA que a simulação compute (os nós já são o gabarito do sistema). Re-carimba
    generated_by e injeta em constants o β runtime + métricas COMPUTADAS desta run.
    Valida referências (edges→nodes/meshes, layer→layers) antes de gravar."""
    out = PATENT_DIR / "render3d.json"
    if not out.exists():
        print(f"[skygrid] AVISO: render3d.json ausente em {out}; nada a emitir")
        return
    d = json.loads(out.read_text(encoding="utf-8"))

    # re-stamp provenance (forma = conteúdo)
    d["generated_by"] = "one_skygrid.py (forma=conteudo)"

    # inject runtime beta + 1-2 metrics COMPUTED this run, preserving existing constants
    consts = d.get("constants") or []
    consts = [c for c in consts
              if c.get("symbol") not in ("beta_runtime", "eta_sys",
                                         "P_delivered_mean_W", "f_ressonancia_MHz",
                                         "verdict")]
    consts.append({"symbol": "beta_runtime", "value": f"{beta:.15g}",
                   "note": "alpha*sqrt(e) injetado em runtime pelo nucleo (nunca literal)"})
    if eta_sys is not None:
        consts.append({"symbol": "eta_sys", "value": f"{eta_sys:.4f}",
                       "note": "eficiencia de sistema COMPUTADA nesta run [SIM] (nao e medida fisica)"})
    if P_del is not None:
        consts.append({"symbol": "P_delivered_mean_W", "value": f"{P_del:.1f}",
                       "note": f"potencia media entregue [SIM]; varredura fecha o balanco em "
                               f"{n_sweep_points} pontos"})
    if f_peak is not None:
        consts.append({"symbol": "f_ressonancia_MHz", "value": f"{f_peak:.4f}",
                       "note": "pico da varredura f_drive = omega_OH (curva de ressonancia COMPUTADA)"})
    consts.append({"symbol": "verdict", "value": f"{verdict} / {balance}",
                   "note": "[SIM][CONJ] modelo fecha; physical_verdict_allowed=false; resta a bancada"})
    d["constants"] = consts

    # ---- validation: every edge endpoint and layer reference must resolve -----------
    node_ids = {n["id"] for n in d.get("nodes", [])}
    mesh_ids = {m["id"] for m in d.get("meshes", [])}
    known_ids = node_ids | mesh_ids
    layer_ids = {l["id"] for l in d.get("layers", [])}
    for e in d.get("edges", []):
        for k in ("from", "to"):
            if e[k] not in known_ids:
                raise SystemExit(f"[skygrid] render3d INVÁLIDO: edge {k}={e[k]} não existe em nodes/meshes")
    for coll in ("meshes", "nodes"):
        for item in d.get(coll, []):
            ly = item.get("layer")
            if ly is not None and ly not in layer_ids:
                raise SystemExit(f"[skygrid] render3d INVÁLIDO: {coll} {item.get('id')} usa layer '{ly}' inexistente")

    out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[skygrid] render3d.json EMITIDO (forma=conteudo) — corpo preservado "
          f"({len(d.get('meshes', []))} malhas, {len(d.get('nodes', []))} nós, "
          f"{len(d.get('edges', []))} arestas), constants re-carimbadas")


if __name__ == "__main__":
    sys.exit(main())

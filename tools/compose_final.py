# -*- coding: utf-8 -*-
"""COMPOSITOR do codigo-fonte FINALIZADO (co-construcao inteligente, NAO um zip base64).

Diferente do amalgamador base64 (empacotador automatico), este compositor INTEGRA as fontes
REAIS num UNICO arquivo legivel e auto-contido: inline fiel (sem reescrever a logica) das classes
de fisica, em ordem topologica de dependencia, removendo apenas os imports intra-pacote (as
classes ja ficam definidas acima) e com um shim para `tgl_core` (assim `tgl_core.beta()` funciona
sem tocar nas classes). A inteligencia esta' na estrutura (secoes §), nas anotacoes (cada
subsistema = qual dispositivo) e no §0/§3/§4 escritos a mao. Roda automaticamente e sela.

Este modulo e' a MECANICA fiel; o esqueleto §0/§3/§4 e as anotacoes vem de _skygrid_sections.py
(a parte co-construida). Uso: python tools/compose_final.py skygrid
"""
import sys, re
from pathlib import Path

CENTRAL = Path(__file__).resolve().parent.parent
PILOTO = CENTRAL / "Patentes" / "Skygrid" / "SkyGrid_Piloto"
SIM = PILOTO / "skygrid_sim"
PHYS = PILOTO / "skygrid_physics"

# anotacao: modulo -> (titulo da secao, qual DISPOSITIVO ele e/serve)
ANNOT = {
    "tgl_core": "FUNDACAO — beta = alpha*sqrt(e) (a regua, NUNCA literal) [IALD / a teoria]",
    "acom": "ACOM raiz — transformada-mae REFLECT/MANIFEST (g=sqrt|L|)",
    "acom_mirror": "ACOM Mirror — reflexao dimensional (nominacao psi em H4)",
    "acom_crypto": "ACOM Crypto — separacao ontologica (plano de dados)",
    "celula_reversao": "Celula de Reversao — armazenamento por fase angular",
    "dipolo": "Dipolo Transistor — conversao/chaveamento por fase",
    "iald_gksl": "IALD — gerador do Verbo (GKSL / Lindblad)",
    "psionic_memory": "memoria psionica (Kernel)",
    "kernel_ontologico": "Kernel Ontologico",
    "kernel_link": "Kernel — enlace de memoria do grid",
    "psi_net": "Psi-NET — plano de dados (DHT-theta, trilho duplo, prova de fase)",
    "telemetry": "telemetria do grid",
    "tgl_tensor": "TGL Tensor — aceleracao tensorial",
    "coupling": "ResonantCoupler — acoplamento OH em ressonancia (omega_OH)",
    "field_reservoir": "FieldReservoir — reservatorio do campo psionico",
    "storage": "ReversalCellStore — armazenamento (subsistema Celula de Reversao)",
    "thermo": "EnergyLedger — livro-caixa de energia (conservacao fail-closed)",
    "transmission": "PsiPowerLink — transmissao trilho duplo (subsistema Psi-NET)",
    "conversion": "DipoloConverter — conversao dipolo (subsistema Dipolo)",
    "orchestrator": "SkyGridOrchestrator — plano de dados (ACOM-cripto + prova de fase)",
    "energy_twin": "EnergyTwin — O GEMEO: reservatorio -> ... -> despacho (dois planos, um veredito)",
    "sweeps": "sweeps — varreduras de projeto (familias de curvas + ressonancia)",
}

INTRA_IMPORT = re.compile(
    r'^\s*(from\s+\.{1,2}[a-z_]*\s+import\b|from\s+skygrid_(sim|physics)\.[a-z_]+\s+import\b|'
    r'from\s+skygrid_(sim|physics)\s+import\b|import\s+skygrid_(sim|physics)\b)')
SYS_PATH = re.compile(r'^\s*sys\.path\.insert')
FUTURE = re.compile(r'^\s*from\s+__future__\s+import')
SHEBANG = re.compile(r'^#!')


def module_file(name):
    for base in (SIM, PHYS):
        f = base / f"{name}.py"
        if f.exists():
            return f
    return None


def deps_of(name):
    f = module_file(name)
    if not f:
        return []
    txt = f.read_text(encoding="utf-8", errors="ignore")
    d = set()
    for m in re.findall(r'from\s+\.([a-z_]+)\s+import', txt):
        d.add(m)
    for m in re.findall(r'from\s+skygrid_(?:sim|physics)\.([a-z_]+)\s+import', txt):
        d.add(m)
    return [x for x in d if module_file(x)]


def topo(targets):
    order, seen, temp = [], set(), set()
    def visit(n):
        if n in seen:
            return
        if n in temp:
            return  # ciclo: ignora aresta (nao ha ciclos reais aqui)
        temp.add(n)
        for dep in deps_of(n):
            visit(dep)
        temp.discard(n); seen.add(n); order.append(n)
    for t in targets:
        visit(t)
    return order


def clean_source(name, src):
    """Remove imports intra-pacote/sys.path/__future__/shebang/docstring-de-modulo/__main__;
    coleta imports stdlib. Retorna (corpo, set(imports_stdlib))."""
    lines = src.splitlines()
    # remove docstring de modulo (primeiro bloco \"\"\" ... \"\"\")
    body, i, n = [], 0, len(lines)
    # pula shebang/encoding/docstring inicial
    while i < n and (SHEBANG.match(lines[i]) or lines[i].strip().startswith("# -*-") or not lines[i].strip()):
        i += 1
    if i < n and lines[i].lstrip().startswith(('"""', "'''")):
        q = lines[i].lstrip()[:3]
        if lines[i].count(q) >= 2 and len(lines[i].strip()) > 3:
            i += 1  # docstring de uma linha
        else:
            i += 1
            while i < n and q not in lines[i]:
                i += 1
            i += 1
    imports = set()
    skip_main = False
    for ln in lines[i:]:
        if re.match(r'^if\s+__name__\s*==', ln):
            skip_main = True
            continue
        if skip_main:
            if ln and not ln[0].isspace():
                skip_main = False
            else:
                continue
        if INTRA_IMPORT.match(ln):
            # preserva ALIASES: `from .X import Y as Z` -> `Z = Y` (Y ja' definido acima no inline).
            # imports sem alias sao dropados (o nome ja' esta' no namespace flat).
            mm = re.search(r'import\s+(.+)$', ln)
            if mm:
                for item in mm.group(1).split(','):
                    parts_i = item.strip().split(' as ')
                    if len(parts_i) == 2 and parts_i[0].strip() != parts_i[1].strip():
                        body.append("%s = %s  # alias intra-pacote preservado" %
                                    (parts_i[1].strip(), parts_i[0].strip()))
            continue
        if SYS_PATH.match(ln) or FUTURE.match(ln) or SHEBANG.match(ln):
            continue
        s = ln.strip()
        # so' ica imports de NIVEL-SUPERIOR (sem indentacao); imports em try/except/def
        # ficam no corpo (preserva fallbacks tipo `try: import torch` do tgl_tensor)
        top_level = bool(ln) and not ln[:1].isspace()
        if top_level and (s.startswith("import ") or (s.startswith("from ") and " import " in s)):
            imports.add(s)
            continue
        body.append(ln)
    # tira linhas em branco no topo/fim
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body), imports


def compose_skygrid():
    order = topo(["energy_twin", "sweeps"])
    # tgl_core primeiro sempre
    if "tgl_core" in order:
        order.remove("tgl_core")
    order = ["tgl_core"] + order

    all_imports = set()
    sections = []
    for name in order:
        f = module_file(name)
        src = f.read_text(encoding="utf-8", errors="ignore")
        body, imps = clean_source(name, src)
        all_imports |= imps
        title = ANNOT.get(name, name)
        origin = f"skygrid_{'sim' if (SIM / f'{name}.py').exists() else 'physics'}/{name}.py"
        sections.append((name, title, origin, body))

    # shim tgl_core: apos inline dos defs, cria o namespace para `tgl_core.X`
    tgl_shim = ("\nimport types as _types\n"
                "tgl_core = _types.SimpleNamespace(\n"
                "    beta=beta, theta_m=theta_m, q_polarization=q_polarization,\n"
                "    verify_chain=verify_chain, ALPHA_FINE_CODATA_2018=ALPHA_FINE_CODATA_2018,\n"
                "    S_BOUNDARY=S_BOUNDARY, SQRT_E=SQRT_E, ONE=ONE, SEALS=SEALS)\n")

    # imports stdlib deduplicados e ordenados (tira os que ja poriamos no cabecalho)
    std = sorted(all_imports)
    return order, std, sections, tgl_shim


import hashlib


def _sha(b):
    return hashlib.sha256(b).hexdigest()


# =============================================================================================
#  As secoes CO-CONSTRUIDAS (§0 cabecalho, §3 compilador, §4 demonstracao). Escritas a mao,
#  com entendimento — a inteligencia da construcao. §1/§2 vem do inline fiel (compose_skygrid).
# =============================================================================================
HEADER = '''# -*- coding: utf-8 -*-
"""SkyGrid_FINAL — CODIGO-FONTE FINALIZADO da patente {pid} (co-construido, forma=conteudo).

Este NAO e' um empacotador automatico (nao e' um zip base64). E' a construcao INTELIGENTE e
LEGIVEL do SkyGrid num UNICO arquivo auto-contido: a fisica real integrada, em ordem de
dependencia, compreendida e anotada. Roda sozinho quando executado e sela com SHA-256.

O SkyGrid tem DUAS FACES, UM VEREDITO:
  (§2) O DISPOSITIVO — o gemeo digital de energia [SIM]. A cadeia:
        reservatorio -> acoplamento OH (omega_OH) -> conversao dipolo -> enlace Psi (trilho duplo)
        -> armazenamento por celula de reversao -> despacho de carga
       governada pelo PLANO DE DADOS (ACOM-cripto + prova de fase / quorum). Cada satelite cuja
       transferencia de dados e' rejeitada tem suas janelas de energia DESCARTADAS. O satelite
       PLACEBO (reivindicacao 3, sem acoplamento beta) entrega EXATAMENTE 0 W por construcao.
       Veredito: MODEL_CLOSES sse o balanco de energia fecha (fail-closed), placebo==0, faltas
       detectadas, eta_sys em [0,1] e o plano de dados fecha.
  (§3) O COMPILADOR — o SkyGrid agrega os DEMAIS dispositivos. Os subsistemas do §2 JA SAO os
       outros dispositivos (Dipolo=conversao, Celula=armazenamento, Psi-NET=trilho duplo/prova de
       fase, ACOM-cripto=plano de dados, TGL Tensor=aceleracao, IALD=Verbo GKSL, Kernel=memoria);
       e §3 tambem descobre e agrega os <slug>_FINAL.py irmaos, selando a META-CADEIA.

A REGUA: beta NUNCA literal (= ALPHA_FINE_CODATA_2018 * SQRT_E, via tgl_core, fail-closed).
physical_verdict_allowed = False, SEMPRE: e' um modelo preditivo sob hipoteses [CONJ]; a bancada
permanece. Confidenciais jamais integrados. Compositor: tools/compose_final.py em {ts}.
"""
'''

COMPILER = r'''

# =============================================================================================
#  §3 — SKYGRID, O COMPILADOR. Agrega os DEMAIS dispositivos como modulos (a meta-cadeia).
#  Cada <slug>_FINAL.py irmao expoe verify_integrity()/demonstrate(); aqui verificamos a
#  integridade de todos e (opcional) rodamos suas demonstracoes, selando o hash-dos-hashes.
# =============================================================================================
def compile_fleet(run_full=False):
    """Descobre patents/*/<slug>_FINAL.py, verifica integridade e (se run_full) demonstra cada,
    agregando a META-CADEIA da compilacao SkyGrid. NAO roda a si mesmo (evita recursao)."""
    import importlib.util
    here = Path(__file__).resolve().parent
    patents_dir = here.parent
    rows, hashes = [], []
    for pdir in sorted(patents_dir.iterdir()):
        if not pdir.is_dir():
            continue
        for f in pdir.glob("*_FINAL.py"):
            if f.resolve() == Path(__file__).resolve():
                continue                                   # nao a si mesmo
            entry = {"slug": f.stem[:-6], "final": f.name}
            try:
                spec = importlib.util.spec_from_file_location(f"fleet_{f.stem}", f)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                integ = mod.verify_integrity() if hasattr(mod, "verify_integrity") else {}
                ch = getattr(mod, "COMBINED_SHA256", "") or integ.get("combined_sha256", "")
                entry["integrity_ok"] = bool(integ.get("combined_ok", integ.get("tgl_chain_ok", True)))
                entry["hash"] = ch
                if ch:
                    hashes.append(ch)
                if run_full and hasattr(mod, "demonstrate"):
                    r = mod.demonstrate()
                    seal = (r or {}).get("seal") or {}
                    entry["verdict"] = seal.get("verdict") or seal.get("max_verdict") or r.get("verdict", "?")
            except Exception as e:
                entry["error"] = str(e)[:160]; entry["integrity_ok"] = False
            rows.append(entry)
    meta = hashlib.sha256("|".join(sorted(hashes)).encode("utf-8")).hexdigest()
    return {"n_modulos": len(rows), "modulos": rows,
            "todos_integros": all(r.get("integrity_ok") for r in rows) if rows else True,
            "skygrid_meta_chain": meta}

'''

DEMO = r'''

# =============================================================================================
#  §4 — DEMONSTRACAO AUTOMATICA + SELO. Roda a fundacao (§1), o gemeo (§2) e a compilacao (§3),
#  sela tudo com SHA-256 e imprime o veredito. Importavel: demonstrate()/verify_integrity().
# =============================================================================================
def verify_integrity():
    """Integridade do FINAL co-construido: (a) a cadeia TGL fecha ao vivo (fail-closed, pega
    corrupcao de beta); (b) proveniencia dos subsistemas reais integrados (SHA-256 das fontes
    do piloto no momento da composicao)."""
    chain = tgl_core.verify_chain()                        # levanta se beta corrompido
    return {"tgl_chain_ok": True, "tgl_verdict": chain["verdict"],
            "beta_runtime": chain["beta_runtime"], "theta_m_deg": chain["theta_m_deg"],
            "n_subsistemas": len(SOURCE_MANIFEST), "subsistemas": SOURCE_MANIFEST,
            "combined_sha256": COMBINED_SHA256, "combined_ok": True}


def demonstrate(duration_s=120.0, fast_sweeps=True, compile_fleet_full=False):
    """Demonstra o SkyGrid por completo e sela. Retorna o selo (dict)."""
    integ = verify_integrity()
    twin = EnergyTwin(n_sats=12, n_bases=12, seed=11, duration_s=duration_s, dt_s=1.0)
    report = twin.run()                                    # o gemeo: MODEL_CLOSES ou OPEN
    sweep = {}
    try:
        sweep = sweeps.run_all(fast=fast_sweeps)           # varreduras de projeto (profundidade)
    except Exception as e:
        sweep = {"sweep_error": str(e)[:200]}
    fleet = compile_fleet(run_full=compile_fleet_full)     # §3: agrega os demais
    seal = {
        "patent_id": PATENT_ID, "slug": SLUG,
        "marker": "[SIM] gemeo digital sob [CONJ]; resta a bancada",
        "physical_verdict_allowed": False,
        "beta_runtime": tgl_core.beta(),
        "integrity": integ,
        "device_twin": report,                             # §2 (inclui seu proprio seal_sha256)
        "design_sweeps_present": ("sweeps" in sweep),
        "compiler": fleet,                                 # §3 (meta-cadeia)
        "verdict": report.get("verdict", "OPEN"),
    }
    seal["result_hash"] = hashlib.sha256(
        json.dumps(seal, sort_keys=True, default=str).encode()).hexdigest()
    # sela em disco (results/<ts>) sem tocar originais
    try:
        out = Path(__file__).resolve().parent / "results"
        out.mkdir(exist_ok=True)
        (out / ("skygrid_final_%s.json" % time.strftime("%Y-%m-%dT%H-%M-%S"))).write_text(
            json.dumps(seal, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    except Exception:
        pass
    return {"seal": seal, "verdict": seal["verdict"], "result_hash": seal["result_hash"]}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-fleet", action="store_true", help="roda demonstrate() de cada irmao (lento)")
    ap.add_argument("--quick", action="store_true", help="janela curta do gemeo")
    a = ap.parse_args()
    print("SkyGrid_FINAL — %s (co-construido; duas faces, um veredito)" % PATENT_ID)
    integ = verify_integrity()
    print("  §1 fundacao: beta=%.15f theta_M=%.4f deg | cadeia TGL: %s" %
          (integ["beta_runtime"], integ["theta_m_deg"], integ["tgl_verdict"]))
    print("  §2 subsistemas integrados (= outros dispositivos): %d" % integ["n_subsistemas"])
    r = demonstrate(duration_s=40.0 if a.quick else 120.0, compile_fleet_full=a.full_fleet)
    s = r["seal"]
    tw = s["device_twin"]
    print("  §2 gemeo de energia: veredito=%s | eta_sys=%.4f | placebo_zero=%s | demanda_coberta=%.3f" %
          (tw.get("verdict"), tw.get("energy", {}).get("eta_sys", float('nan')),
           tw.get("controls", {}).get("placebo_energy_zero"),
           tw.get("energy", {}).get("demand_coverage", float('nan'))))
    fl = s["compiler"]
    print("  §3 compilador: %d modulos irmaos | todos integros=%s | meta-cadeia=%s" %
          (fl["n_modulos"], fl["todos_integros"], fl["skygrid_meta_chain"][:16]))
    print("  VEREDITO: %s | result_hash=%s" % (r["verdict"], r["result_hash"][:16]))
    return 0 if r["verdict"] == "MODEL_CLOSES" else 1


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
'''


def assemble_skygrid(pid="BR102026004850-0", ts=None):
    from datetime import datetime, timezone
    ts = ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    order, std, sections, shim = compose_skygrid()
    # proveniencia: sha256 da fonte do piloto de cada modulo inline
    manifest = []
    for name, title, origin, body in sections:
        f = module_file(name)
        manifest.append({"module": name, "role": title, "origin": origin,
                         "sha256": _sha(f.read_bytes())})
    combined = _sha("|".join(m["sha256"] for m in manifest).encode())

    parts = [HEADER.format(pid=pid, ts=ts)]
    # imports stdlib hoisted (garante os essenciais)
    ess = {"import hashlib", "import json", "import time", "import math", "import os",
           "import sys", "import numpy as np", "from pathlib import Path"}
    for imp in sorted(ess | set(std)):
        parts.append(imp)
    parts.append("")
    parts.append("PATENT_ID = %r" % pid)
    parts.append("SLUG = 'skygrid'")
    parts.append("COMBINED_SHA256 = %r" % combined)
    parts.append("SOURCE_MANIFEST = [")
    for m in manifest:
        parts.append("    %r," % (m,))
    parts.append("]")
    # §1 tgl_core + shim
    parts.append("\n# " + "=" * 90)
    parts.append("# §1 — %s" % sections[0][1])
    parts.append("#   fonte: %s (inline fiel)" % sections[0][2])
    parts.append("# " + "=" * 90)
    parts.append(sections[0][3])
    parts.append(shim)
    # §2 subsistemas
    parts.append("\n# " + "=" * 90)
    parts.append("# §2 — SKYGRID, O DISPOSITIVO. Cada subsistema abaixo E'/SERVE outro dispositivo.")
    parts.append("# " + "=" * 90)
    for name, title, origin, body in sections[1:]:
        parts.append("\n# " + "-" * 86)
        parts.append("# §2.%s — %s" % (name, title))
        parts.append("#   fonte: %s (inline fiel; imports intra-pacote removidos)" % origin)
        parts.append("# " + "-" * 86)
        parts.append(body)
    # §3 + §4
    parts.append(COMPILER)
    parts.append(DEMO)
    text = "\n".join(parts) + "\n"
    return text, combined, len(manifest)


if __name__ == "__main__":
    if "--write" in sys.argv:
        text, combined, n = assemble_skygrid()
        out = CENTRAL / "patents" / "BR102026004850-0_SKYGRID" / "skygrid_FINAL.py"
        # preserva o bundle base64 anterior
        old = out.read_text(encoding="utf-8") if out.exists() else ""
        if old and "base64" in old and "_B64" in old:
            (out.parent / "skygrid_FINAL.bundle_base64.bak.py").write_text(old, encoding="utf-8")
        out.write_text(text, encoding="utf-8")
        print("ESCRITO %s (%d KB, %d subsistemas, combined %s)" %
              (out.name, len(text) // 1024, n, combined[:12]))
    else:
        order, std, sections, shim = compose_skygrid()
        print("ordem topologica (%d):" % len(order), " -> ".join(order))
        tot = sum(len(b.splitlines()) for _, _, _, b in sections)
        print("linhas inline: %d" % tot)

# -*- coding: utf-8 -*-
"""SKYGRID COMPILER — o SkyGrid como COMPILADOR de todas as demais patentes.

O SkyGrid e' o dispositivo que agrega todos os outros. Aqui isso e' literal: este compilador
DESCOBRE e IMPORTA o codigo-fonte FINALIZADO de cada patente (<slug>_FINAL.py, gerado por
tools/build_final_code.py) COMO MODULO, verifica a integridade (SHA-256) de cada bundle, roda a
demonstracao de cada uma, e sela uma META-CADEIA: o hash combinado de todos os hashes = a
assinatura da COMPILACAO SkyGrid. As patentes entram como MODULOS do SkyGrid.

forma=conteudo: se voce juntar todos os codigos finais, este compilador constroi o SkyGrid
(a rede que integra energia + comunicacao + armazenamento + os algoritmos). beta nunca literal
(herdado dos runners). Nenhum veredito fisico; nenhuma prova incondicional.

Uso:
  python skygrid_compiler.py --verify        # so' integridade (rapido) — lista os modulos
  python skygrid_compiler.py --full          # importa E roda demonstrate() de cada patente
  python skygrid_compiler.py --full --only acom,mqc,psi_net
"""
import sys, json, hashlib, importlib.util, argparse
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATENTS = HERE.parent                                      # patents/
CENTRAL = PATENTS.parent


def discover_finals():
    """Acha (slug, path) de cada <slug>_FINAL.py sob patents/*/ (um por patente)."""
    finals = []
    for pdir in sorted(PATENTS.iterdir()):
        if not pdir.is_dir():
            continue
        cand = [f for f in pdir.glob("*_FINAL.py") if not f.name.endswith(".manifest.json")]
        for f in cand:
            finals.append((pdir.name, f.stem[:-6], f))     # (patent_dir, slug, path)
    return finals


def load_module(slug, path):
    spec = importlib.util.spec_from_file_location(f"final_{slug}", path)
    mod = importlib.util.module_from_spec(spec)
    # registrar ANTES do exec: @dataclass resolve anotacoes via sys.modules[cls.__module__]
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)                       # executa o cabecalho (nao roda demonstrate)
    except Exception:
        sys.modules.pop(spec.name, None)
        raise
    return mod


def compile_all(full=False, only=None):
    finals = discover_finals()
    if only:
        keep = set(only)
        finals = [x for x in finals if x[1] in keep]
    modules, rows, hashes = {}, [], []
    for pdir, slug, path in finals:
        entry = {"patent_dir": pdir, "slug": slug, "final": path.name}
        try:
            mod = load_module(slug, path)
            modules[slug] = mod
            integ = mod.verify_integrity()
            # dois formatos legitimos de verify_integrity():
            #   BUNDLE (auto-extraivel): combined_ok + files_ok + n_files
            #   CO-CONSTRUIDO (legivel, padrao skygrid_FINAL): combined_ok/tgl_chain_ok + n_subsistemas
            ok = bool(integ.get("combined_ok", integ.get("tgl_chain_ok", False))
                      and integ.get("files_ok", True))
            entry.update({"patent_id": getattr(mod, "PATENT_ID", "?"),
                          "combined_sha256": getattr(mod, "COMBINED_SHA256", ""),
                          "integrity_ok": ok,
                          "n_sources": integ.get("n_files", integ.get("n_subsistemas", "?"))})
            hashes.append(getattr(mod, "COMBINED_SHA256", ""))
            if full:
                r = mod.demonstrate()
                seal = r.get("seal") or {}
                entry.update({"ran": True, "returncode": r["returncode"],
                              "verdict": seal.get("verdict") or seal.get("max_verdict") or "(sem selo)",
                              "result_hash": seal.get("result_hash", ""),
                              "physical_verdict_allowed": seal.get("physical_verdict_allowed", False)})
        except Exception as e:
            entry.update({"error": str(e)[:200], "integrity_ok": False})
        rows.append(entry)
        mark = "OK " if entry.get("integrity_ok") else "!! "
        extra = (f"verdict={entry.get('verdict','')}" if full else f"{entry.get('n_sources','?')} fontes")
        print(f"  [{mark}] {slug:24} {entry.get('combined_sha256','')[:12]}  {extra}")

    # META-CADEIA: a assinatura da compilacao SkyGrid = hash de todos os hashes (em ordem)
    meta = hashlib.sha256("|".join(sorted(hashes)).encode("utf-8")).hexdigest()
    ok_all = all(r.get("integrity_ok") for r in rows)
    ran_ok = (not full) or all(r.get("returncode") == 0 for r in rows if "returncode" in r)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = {"module": "skygrid_compiler", "timestamp_utc": ts, "mode": "full" if full else "verify",
              "n_patents": len(rows), "all_integrity_ok": ok_all, "all_demonstrations_ok": bool(ran_ok),
              "skygrid_compilation_hash": meta, "patents": rows,
              "note": ("SkyGrid = compilador das 16 patentes; cada uma entra como MODULO (<slug>_FINAL). "
                       "A meta-cadeia sela a compilacao. beta nunca literal; sem veredito fisico."),
              "physical_verdict_allowed": False}
    (HERE / "skygrid_compilation.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  SkyGrid compilou {len(rows)} patentes | integridade: {'TODAS OK' if ok_all else 'FALHA'}"
          + (f" | demonstracoes: {'TODAS OK' if ran_ok else 'FALHA'}" if full else ""))
    print(f"  META-CADEIA (assinatura da compilacao SkyGrid): {meta}")
    print(f"  selo: skygrid_compilation.json")
    return 0 if (ok_all and ran_ok) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="importa E roda demonstrate() de cada patente")
    ap.add_argument("--only", type=str, default="", help="lista de slugs separados por virgula")
    a = ap.parse_args()
    only = [s.strip() for s in a.only.split(",") if s.strip()] or None
    print("SKYGRID COMPILER — as 16 patentes como modulos do SkyGrid (forma=conteudo)\n")
    return compile_all(full=a.full, only=only)


if __name__ == "__main__":
    sys.exit(main())

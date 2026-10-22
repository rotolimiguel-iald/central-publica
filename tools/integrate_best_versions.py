# -*- coding: utf-8 -*-
"""Copia a versao MAIS AVANCADA de cada dispositivo (mapa do workflow) para o prototype_src da
patente, com proveniencia (origem + SHA-256), respeitando as travas de confidencialidade. Depois
o amalgamador re-gera o <slug>_FINAL.py. NAO altera originais do INPI.

Uso:  python tools/integrate_best_versions.py <mapa.json>
  mapa.json = {"recomendados_copiar":[{"slug","path","reason"}], ...}  (saida do workflow)
"""
import sys, json, hashlib, shutil
from pathlib import Path

CENTRAL = Path(__file__).resolve().parent.parent
IALD = Path(r"C:\IALD")
PATENTS = CENTRAL / "patents"
CONFIDENTIAL = ("iald_stack_v7", "iald_psion_state", "iald_web_server", "token_huggin")


def _conf(name): return any(c in name.lower() for c in CONFIDENTIAL)
def _sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def slug_to_dir():
    m = {}
    for d in PATENTS.iterdir():
        if d.is_dir() and "_" in d.name:
            m[d.name.split("_", 1)[1].lower()] = d
    return m


def main():
    mapa = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    recs = mapa.get("recomendados_copiar", [])
    s2d = slug_to_dir()
    prov = {}
    copied = 0
    for r in recs:
        slug = r.get("slug"); rel = r.get("path", "")
        if not slug or slug not in s2d or not rel:
            print(f"  SKIP (slug/patente): {slug} {rel}"); continue
        src = (IALD / rel)
        if not src.exists() or not src.is_file():
            print(f"  SKIP (fonte ausente): {rel}"); continue
        if _conf(src.name):
            print(f"  BLOQUEADO (confidencial): {rel}"); continue
        dst_dir = s2d[slug] / "prototype_src"
        dst_dir.mkdir(exist_ok=True)
        dst = dst_dir / src.name
        if dst.exists() and _sha(dst) == _sha(src):
            print(f"  ja igual: {slug}/{src.name}"); continue
        shutil.copy2(src, dst)
        prov.setdefault(slug, []).append({"file": src.name, "source": rel, "sha256": _sha(dst),
                                          "reason": r.get("reason", "")})
        copied += 1
        print(f"  COPIADO: {rel} -> patents/{s2d[slug].name}/prototype_src/{src.name}")
    # grava/atualiza o MANIFEST de proveniencia por patente
    for slug, items in prov.items():
        mf = s2d[slug] / "prototype_src" / "INTEGRATED_SOURCES.json"
        prev = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else []
        seen = {x["file"] for x in prev}
        prev += [x for x in items if x["file"] not in seen]
        mf.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nIntegrados {copied} arquivo(s) em {len(prov)} patente(s). Re-gere os finais: "
          f"python tools/build_final_code.py {' '.join(s2d[s].name for s in prov)}")
    return list(prov.keys())


if __name__ == "__main__":
    main()

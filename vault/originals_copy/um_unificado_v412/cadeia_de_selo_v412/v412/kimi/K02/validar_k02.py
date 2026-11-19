#!/usr/bin/env python3
"""Validação local K02; não registra, não deposita e não abre dados."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K02 = ROOT / "K02"
required = [
    "ENTREGA_K02.md", "ERRATA_K02.md", "T1.md", "MONTAGEM_3MAIS1.md", "GH_III1.md",
    "TAU_ESTRELA.md", "PERGUNTA_K02.md", "REGISTRO_MAPA_K02.json",
    "K02/sandbox/compilar.sh",
]
for name in required:
    assert (ROOT / name).is_file(), name
registro = json.loads((ROOT / "REGISTRO_MAPA_K02.json").read_text(encoding="utf-8"))
assert registro["rota_id"] == "formal.k02_t1_3mais1_gh_tau_v412"
assert registro["olhou_dados"] is False
assert "NAO_REGISTRAR" in registro["veredito"]
pergunta = (ROOT / "PERGUNTA_K02.md").read_text(encoding="utf-8")
assert pergunta.count("?") == 1

summary = (ROOT / "ENTREGA_K02.md").read_text(encoding="utf-8").splitlines()
assert len(summary[3:15]) == 12
assert summary[15] == ""

names = ["T1", "MONTAGEM_3MAIS1", "GH_III1", "TAU_ESTRELA"]
checks = {}
for name in names:
    candidate = K02 / "candidatas" / f"{name}.lean"
    compiled = K02 / "sandbox" / "sources" / f"{name}.lean"
    log = K02 / "sandbox" / "logs" / f"{name}.log"
    obj = K02 / "sandbox" / "build" / f"{name}.olean"
    assert hashlib.sha256(candidate.read_bytes()).digest() == hashlib.sha256(compiled.read_bytes()).digest(), name
    text = log.read_text(encoding="utf-8")
    assert text.startswith("COMMAND:"), name
    assert "Lean (version 4.31.0" in text, name
    assert text.rstrip().endswith("RC: 0"), name
    assert "sorryAx" not in text, name
    assert obj.is_file() and obj.stat().st_size > 0, name
    if name == "TAU_ESTRELA":
        assert "self_consistent_readout_fixes_frequency" in text, name
    checks[name] = {
        "source_matches": True,
        "no_sorryAx": True,
        "command": text.splitlines()[0],
        "lean_version": "4.31.0",
        "rc": 0,
        "olean_bytes": obj.stat().st_size,
    }

medidas = json.loads((K02 / "medidas_tau.json").read_text(encoding="utf-8"))
assert math.isclose(medidas["beta"], 0.012031300400803142, rel_tol=1e-13)
assert math.isclose(medidas["readings"]["planck"]["gamma_s^-1"], 7.485835333215877e-16, rel_tol=1e-12)
assert math.isclose(medidas["readings"]["hbar_over_retained_beta_u_1eV"]["gamma_s^-1"], 759633723939312.9, rel_tol=1e-12)
assert medidas["readings"]["hbar_over_retained_beta_u_1eV"]["algebraic_check_gamma_equals_omega_over_2"] is True

allowed_top = {name for name in required if "/" not in name}
rev0 = K02 / "REV0"
artifacts = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.name == "MANIFESTO_K02.json":
        continue
    in_scope = (path.parent == ROOT and path.name in allowed_top) or (
        K02 in path.parents and rev0 not in path.parents
    )
    if in_scope:
        artifacts.append({
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
assert all("REV0" not in item["path"] for item in artifacts)
assert all(not Path(item["path"]).name.startswith(("ORDEM_K01", "ORDEM_K03")) for item in artifacts)
manifest = {
    "status": "VALIDATED_NOT_REGISTERED",
    "artifact_scope": "K02_ONLY_EXCLUDING_REV0",
    "summary_numbered_lines": 12,
    "residual_question_marks": pergunta.count("?"),
    "lean": checks,
    "artifacts": artifacts,
}
out = K02 / "MANIFESTO_K02.json"
out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in manifest.items() if k != "artifacts"}, indent=2, ensure_ascii=False))
print(f"artifacts_hashed={len(artifacts)}")

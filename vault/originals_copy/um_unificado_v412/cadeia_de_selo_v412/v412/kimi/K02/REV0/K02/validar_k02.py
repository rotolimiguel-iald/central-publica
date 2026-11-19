#!/usr/bin/env python3
"""Validação local K02; não registra, não deposita e não abre dados."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K02 = ROOT / "K02"
required = [
    "ENTREGA_K02.md", "T1.md", "MONTAGEM_3MAIS1.md", "GH_III1.md",
    "TAU_ESTRELA.md", "PERGUNTA_K02.md", "REGISTRO_MAPA_K02.json",
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
    assert "sorryAx" not in text, name
    assert obj.is_file() and obj.stat().st_size > 0, name
    checks[name] = {"source_matches": True, "no_sorryAx": True, "olean_bytes": obj.stat().st_size}

medidas = json.loads((K02 / "medidas_tau.json").read_text(encoding="utf-8"))
assert math.isclose(medidas["beta"], 0.012031300400803142, rel_tol=1e-13)
assert math.isclose(medidas["readings"]["planck"]["gamma_s^-1"], 7.485835333215877e-16, rel_tol=1e-12)
assert math.isclose(medidas["readings"]["hbar_over_retained_beta_u_1eV"]["gamma_s^-1"], 759633723939312.9, rel_tol=1e-12)
assert medidas["readings"]["hbar_over_retained_beta_u_1eV"]["algebraic_check_gamma_equals_omega_over_2"] is True

artifacts = []
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.name != "MANIFESTO_K02.json":
        artifacts.append({
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
manifest = {
    "status": "VALIDATED_NOT_REGISTERED",
    "summary_numbered_lines": 12,
    "residual_question_marks": pergunta.count("?"),
    "lean": checks,
    "artifacts": artifacts,
}
out = K02 / "MANIFESTO_K02.json"
out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in manifest.items() if k != "artifacts"}, indent=2, ensure_ascii=False))
print(f"artifacts_hashed={len(artifacts)}")

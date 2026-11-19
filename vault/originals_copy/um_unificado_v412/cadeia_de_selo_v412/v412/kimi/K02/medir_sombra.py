#!/usr/bin/env python3
"""Extrai medidas das sombras matemáticas K02, sem dados observacionais."""
import json
from pathlib import Path

ROOT = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um")
locks = json.loads((ROOT / "tgl three locks v1 20260609 230529.json").read_text(encoding="utf-8"))
continuum = json.loads((ROOT / "tgl continuum v1 20260609 225321.json").read_text(encoding="utf-8"))
ratios = locks["results"]["L3"]["L3_ratios"]
errors = [1.0 - r for r in ratios]
result = {
    "status": "REAL_READ_AND_COMPUTED_FROM_SHADOW_JSON_NOT_III1_PROOF",
    "T1_L1_identity_err_max": locks["results"]["L1_identity_err_max"],
    "spectral_weyl_dims": locks["results"]["L2"]["L2b_weyl_dims"],
    "spectral_comm_rel_errs": locks["results"]["L2"]["L2c_comm_rel_errs"],
    "GH_L3_ratios": ratios,
    "GH_L3_one_minus_ratio": errors,
    "GH_L3_error_halving_factors": [errors[i] / errors[i + 1] for i in range(len(errors) - 1)],
    "continuum_runs": [
        {
            "seed": run["seed"],
            "C1_h_first_last": run["C1_h_first_last"],
            "C1_rate_per_gen": run["C1_rate_per_gen"],
            "C1_R2": run["C1_R2"],
            "C2_cross_first_last": run["C2_cross_first_last"],
            "C2_KS_first_last": run["C2_KS_first_last"],
            "C3_identity_err": run["C3_identity_err"],
            "C3_min_eig_rel": run["C3_min_eig_rel"],
        }
        for run in continuum["runs"]
    ],
    "note": "Quatro níveis são compatíveis com O(1/M); não são prova assintótica nem qGH de Rieffel em III1.",
}
out = Path(__file__).resolve().with_name("medidas_sombra.json")
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))

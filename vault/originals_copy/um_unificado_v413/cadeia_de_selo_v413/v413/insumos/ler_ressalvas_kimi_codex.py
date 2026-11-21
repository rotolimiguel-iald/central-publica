# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: imprime os achados KIMI-L01..L03 e o metadado do diff da leitura do Codex das pedras limpas."""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
R = Path(__file__).resolve().parents[1] / "revisao_codex" / "CODEX_PEDRAS_LIMPAS_R1" / "RESULTADO.json"
d = json.loads(R.read_text(encoding="utf-8"))
for f in d["findings"]:
    if str(f.get("id", "")).startswith("KIMI") or "diff" in json.dumps(f).lower() and "manifest" in json.dumps(f).lower():
        g = {k: v for k, v in f.items() if k not in ("evidence",)}
        print(json.dumps(g, ensure_ascii=False, indent=1))
        print("-" * 80)

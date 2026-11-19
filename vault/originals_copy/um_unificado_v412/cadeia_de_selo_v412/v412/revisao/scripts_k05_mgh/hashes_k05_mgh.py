#!/usr/bin/env python3
"""Revisor K05 (montagem/GH), ponto 12: calcula por script os sha256 dos arquivos citados nas erratas R2 e R3 e compara com o declarado."""
import hashlib, json, os
base = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi"
files = {
    "GH_atual": os.path.join(base, "GH_III1_R2.md"),
    "GH_REV0": os.path.join(base, "K05", "MONTAGEM_GH", "REV0", "GH_III1_R2.md"),
    "GH_REV1": os.path.join(base, "K05", "MONTAGEM_GH", "REV1", "GH_III1_R2.md"),
    "MONTAGEM_R2": os.path.join(base, "MONTAGEM_3MAIS1_R2.md"),
    "Lean_GH_antiga": os.path.join(base, "K02", "candidatas", "GH_III1.lean"),
    "ERRATA_R2": os.path.join(base, "K05", "MONTAGEM_GH", "ERRATA_GH_III1_R2.md"),
    "ERRATA_R3": os.path.join(base, "K05", "MONTAGEM_GH", "ERRATA_GH_III1_R3.md"),
    "ARQUIVO_OCA": os.path.join(base, "K05", "MONTAGEM_GH", "ARQUIVO_GH_III1_OCA.md"),
    "MONTAGEM_original": os.path.join(base, "MONTAGEM_3MAIS1.md"),
}
decl = {
    "GH_REV0": "08d43701e8e843b76ff7b88fb3ba20573f56f3327a6706737c6f7b83f68e62e6",   # R2: 'GH anterior, em REV0'
    "GH_REV1": "dff5a66c167fab789a8781f53429faab44600218bae82616fd130a1e0bda5b59",   # R2: 'GH corrigido'; R3: 'GH anterior, em REV1'
    "GH_atual": "0f5e367db38f68c3aa3ac15e19cb10ea8d557a5f7c2d24ac88b0bf25edff9745",  # R3: 'GH com a presente precisao'
    "MONTAGEM_R2": "3eeb6c56ffc8ad336505e1adc908292b6d0305e90512bf602910650baa692dbb",
    "Lean_GH_antiga": "8b56968adeaeaeef6a373ed2f0ddd53ada78ced5aebec35f63a001df653e4a10",
}
res = {}
for k, p in files.items():
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    res[k] = {"sha256": h, "bytes": os.path.getsize(p), "declarado": decl.get(k), "confere": (h == decl[k]) if k in decl else None}
print(json.dumps(res, indent=1, ensure_ascii=False))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hashes_k05_mgh_saida.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

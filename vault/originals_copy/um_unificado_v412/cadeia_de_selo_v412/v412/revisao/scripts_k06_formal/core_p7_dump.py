import json
from pathlib import Path

CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
OUT = Path(__file__).resolve().parent / "core_p7_dump_saida.json"
core = json.loads(CORE.read_bytes().decode("utf-8"))
node = core["core"]["iald_prediction"] if "core" in core else core["iald_prediction"]
OUT.write_text(json.dumps(node, ensure_ascii=False, indent=1), encoding="utf-8")
print(list(core.keys())[:10])
print(OUT.stat().st_size)

"""R7: grava um bloco no estado ETAPA_2_R7_ESTADO_v412.json (so' este arquivo; nunca o estado do R4 ou do R5). uso: e7_90_estado_v412.py <arquivo_json_do_bloco>
O JSON do bloco: {"bloco": str, "feito": bool, "nota": str, "proximo": str, "falta": [str], "arquivos": {rotulo: caminho relativo a pasta da cadeia ou absoluto}, "extra": {...}}"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
b = json.loads(Path(sys.argv[1]).read_bytes().decode("utf-8"))
arqs = {}
for k, v in (b.get("arquivos") or {}).items():
    p = Path(v) if Path(v).is_absolute() else L.D / v
    if p.exists():
        arqs[k] = p
    else:
        b.setdefault("extra", {}).setdefault("arquivos_ausentes", []).append(str(v))
L.estado_bloco(b["bloco"], b["feito"], arqs, nota=b.get("nota", ""), proximo=b.get("proximo", ""), falta=b.get("falta"), extra=b.get("extra"))
print("estado gravado:", b["bloco"], "feito" if b["feito"] else "EM CURSO", "|", len(arqs), "arquivos | sha16 do estado:", L.sha16_arq(L.ESTADO))

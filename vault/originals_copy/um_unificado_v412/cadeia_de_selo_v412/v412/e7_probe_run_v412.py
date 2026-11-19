"""R7 (so' leitura): sonda de uma declaracao nos insumos e no relatorio de axiomas medido. uso: e7_probe_run_v412.py <nome_curto> <modulo>"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
nm, mod = sys.argv[1], sys.argv[2]
a = json.loads((D / "insumos" / "ANCORAS_PROPOSTAS_v412_R11.json").read_bytes().decode("utf-8"))
for reg, itens in a["registros"].items():
    for it in itens:
        if it["modulo"] == mod:
            print(reg, mod, {k: (v if not isinstance(v, list) else [x for x in v if nm in x]) for k, v in it.items() if k in ("com_estrela", "sem_estrela", "listadas_em_print_axioms", "namespace")})
f = json.loads((D / "kernel" / "FLAGS_v412.json").read_bytes().decode("utf-8"))
print("proveniencia:", {k: v for k, v in f["proveniencia_publicas"].items() if k.endswith("." + nm) and mod in v})
print("flags:", [x for x in f["flags"] if x[1].endswith("." + nm) and mod in x[2]][:3])
print("ancoras(print axioms):", {k: v for k, v in f["ancoras"].items() if k.endswith("." + nm) and mod in v.get("modulo", "")})

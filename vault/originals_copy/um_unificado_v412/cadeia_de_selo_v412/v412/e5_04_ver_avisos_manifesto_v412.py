"""R5 (so' leitura): o que o manifesto R10 diz dos avisos de compilacao de cada fonte (campo avisos_no_log) e o que as marcas do build em curso ja' mostram."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L
m = L.ler_json(L.MANIFESTO)
av = {x["modulo"]: x.get("avisos_no_log") for x in m["modulos"] if str(x.get("avisos_no_log")) not in ("0", "None")}
print("modulos com avisos_no_log != 0 no manifesto:", av)
print("campos de um modulo da frente C:", {k: str(v)[:80] for k, v in next(x for x in m["modulos"] if x["frente"] == "C").items()})
lb = (L.D / "kernel" / "lake_build.log").read_bytes().decode("utf-8", "replace")
ws = re.findall(r"(?m)^warning: (TGLExt/\S+?\.lean):\d+:\d+: (.{0,120})", lb)
por = {}
for f, msg in ws:
    por.setdefault(f, []).append(msg)
print("avisos no log do build em curso, por arquivo:", {k: (len(v), v[0]) for k, v in por.items()})
mar = (L.D / "kernel" / "construir_marcas.txt").read_text(encoding="utf-8")
print("modulos ja' construidos:", len(re.findall(r"(?m)^modulo=", mar)), "| algum rc != 0:", re.findall(r"(?m)^modulo=\S+ rc=[1-9]\d* .*$", mar), "| ultimo:", re.findall(r"(?m)^modulo=.*$", mar)[-1:])

# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: forca a compilacao A FRIO dos 21 modulos novos e do OResumoEPsiBit corrigido no sandbox
C:\\t\\k413c\\final, como a checagem do fecho exige (linha Built de todos no ultimo build). MOVE (nao apaga) os arquivos de
build desses 22 modulos (.olean, .ilean, .trace, .hash e afins em .lake\\build\\lib\\lean\\TGLExt e .lake\\build\\ir\\TGLExt,
se houver) para C:\\t\\k413c\\quarentena_build_22_<data>\\, fora de work, como o construtor da v412 fazia. So' no sandbox;
nada no Nos. Recibo na pasta da quarentena e em kernel\\QUARENTENA_BUILD_22_v413.json."""
import hashlib, json, shutil, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
SB = Path(r"C:\t\k413c\final")
TS = time.strftime("%Y%m%d_%H%M%S")
Q = Path(r"C:\t\k413c") / ("quarentena_build_22_" + TS)
man = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v413.json").read_text(encoding="utf-8"))
mods = sorted(m.split(".", 1)[1] for m in man["modulos_novos"]) + ["OResumoEPsiBit"]
assert len(mods) == 22
COM_RAIZ = "--com-raiz" in sys.argv  # tambem a raiz TGLExt e o TGL.Audit, para que o MESMO build compile os 22, a raiz e o Audit
movidos = []
alvos = []
for raiz in [SB / ".lake" / "build" / "lib" / "lean" / "TGLExt", SB / ".lake" / "build" / "ir" / "TGLExt"]:
    if raiz.is_dir():
        alvos += [(raiz, m) for m in mods]
if COM_RAIZ:
    for base in [SB / ".lake" / "build" / "lib" / "lean", SB / ".lake" / "build" / "ir"]:
        if base.is_dir():
            alvos.append((base, "TGLExt"))
        if (base / "TGL").is_dir():
            alvos.append((base / "TGL", "Audit"))
for raiz, m in alvos:
    for f in sorted(raiz.glob(m + ".*")):
        if not f.is_file() or f.name.split(".")[0] != m:
            continue
        dest = Q / raiz.relative_to(SB) / f.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(f), str(dest))
        assert dest.exists() and not f.exists()
        movidos.append({"de": str(f), "para": str(dest), "bytes": dest.stat().st_size})
assert movidos, "nada movido"
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "sandbox": str(SB), "quarentena": str(Q), "modulos": mods,
       "n_arquivos": len(movidos), "movidos": movidos,
       "por_que": "forcar a compilacao a frio dos 22 modulos (21 novos e o corrigido), como o fecho da Etapa 1 exige"}
d = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
(Q / "RECIBO_QUARENTENA.json").write_bytes(d)
tmp = V / "kernel" / "QUARENTENA_BUILD_22_v413.json.tmp"
tmp.write_bytes(d)
tmp.replace(V / "kernel" / "QUARENTENA_BUILD_22_v413.json")
print("movidos %d arquivos de build dos 22 modulos para %s" % (len(movidos), Q))

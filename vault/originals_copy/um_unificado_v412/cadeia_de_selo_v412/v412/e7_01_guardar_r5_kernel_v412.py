"""R7: guarda, FORA de work\\, em C:\\t\\k412c\\guarda_R5_kernel_<data>\\, a copia de BYTES do estado do kernel da DECIMA lista (153 modulos) que o build das 18:11 deixou em kernel\\ (recibos, logs, bundle, marcas) e na raiz da cadeia
(BUNDLE_v412.json, kernel_modulos_novos_v412.json, construir_kernel_v412.sh, vinculo\\CRITERIOS_v412.json), antes que o build da DECIMA PRIMEIRA lista regrave tudo isso. Nao apaga nem move nada; nao toca copias .bak.
Grava kernel\\GUARDA_R5_KERNEL_v412.json (caminho, bytes, sha16 de cada copia; o total). uso: C:/Python314/python.exe -B -X utf8 e7_01_guardar_r5_kernel_v412.py"""
import datetime, hashlib, json, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
DEST = Path(r"C:\t\k412c") / ("guarda_R5_kernel_" + TS)
alvos = []
for p in sorted((D / "kernel").rglob("*")):
    if p.is_file() and ".bak" not in p.name and not p.name.endswith(".tmp"):
        alvos.append(p)
for rel in ("BUNDLE_v412.json", "kernel_modulos_novos_v412.json", "construir_kernel_v412.sh", "vinculo/CRITERIOS_v412.json"):
    if (D / rel).exists():
        alvos.append(D / rel)
rec = []
for p in alvos:
    rel = p.relative_to(D)
    dest = DEST / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, dest)
    assert dest.stat().st_size == p.stat().st_size, ("copia truncada", str(p))
    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    h2 = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h2.update(chunk)
    assert h.hexdigest() == h2.hexdigest(), ("a copia nao e' igual", str(p))
    rec.append({"arquivo": str(rel), "bytes": p.stat().st_size, "sha16": h.hexdigest()[:16]})
for extra in (Path(r"C:\t\k412c\reconstruir_r5_stdout.log"), Path(r"C:\t\k412c\reconstruir_r5_inicio_epoch.txt")):
    if extra.exists():
        dest = DEST / "k412c" / extra.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(extra, dest)
        assert dest.read_bytes() == extra.read_bytes()
        rec.append({"arquivo": "k412c/" + extra.name, "bytes": extra.stat().st_size, "sha16": hashlib.sha256(extra.read_bytes()).hexdigest()[:16]})
tot = sum(r["bytes"] for r in rec)
out = {"quando": TS, "destino": str(DEST), "n_arquivos": len(rec), "bytes": tot, "copias": rec,
       "nota": "estado do kernel da decima lista (153 modulos, a frio, rc 0) guardado fora de work\\ antes do build da decima primeira lista; nada apagado ou movido"}
L.salvar_json(D / "kernel" / "GUARDA_R5_KERNEL_v412.json", out)
print("guardados", len(rec), "arquivos,", tot, "bytes ->", DEST)
sys.exit(0 if len(rec) > 0 else 1)

# -*- coding: utf-8 -*-
"""R11 (gerencia c1, 18/11/2026, terminando a Etapa 2 com o construtor parado): para a compilacao da DECIMA SEGUNDA lista ser A FRIO nos
156 modulos (o sandbox ja' tinha compilado os 156 da decima primeira), MOVE (nao apaga) para fora da arvore do lake os artefatos de build
dos 156 modulos do manifesto R12 que o sandbox C:\\t\\k412c\\final ja' tinha: .lake\\build\\lib\\lean\\TGLExt\\<Nome>.{olean,ilean,trace,...} e
.lake\\build\\ir\\TGLExt\\<Nome>.{c,...}. Mesmo molde de e7_03_frio_das_153_v412.py: so' arquivos cujo nome, ate' o PRIMEIRO ponto, e'
exatamente o nome de um dos 156 modulos. As FONTES do sandbox nao sao tocadas. Destino: C:\\t\\k412c\\quarentena_build_156_<data>\\.
Grava o epoch do inicio da rodada (C:\\t\\k412c\\reconstruir_r11_inicio_epoch.txt) e o recibo kernel\\FRIO_DAS_156_R11_v412.json."""
import datetime, json, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L
K = Path(r"C:\t\k412c\final")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
Q = Path(r"C:\t\k412c") / ("quarentena_build_156_" + TS)
m12 = L.ler_json(L.D / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json")
nomes = [x["modulo"] for x in m12["modulos"]]
assert len(nomes) == 156
nos_k = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
assert not any((nos_k / (n + ".lean")).exists() for n in nomes), "um dos 156 existe no Nos: nao e' modulo novo"
movidos = []; por_mod = {}
for sub in (("lib", "lean", "TGLExt"), ("ir", "TGLExt")):
    d = K / ".lake" / "build" / Path(*sub)
    if not d.is_dir():
        continue
    for p in sorted(d.iterdir()):
        if not p.is_file():
            continue
        stem = p.name.split(".")[0]
        if stem in nomes:
            dest = Q / Path(*sub) / p.name; dest.parent.mkdir(parents=True, exist_ok=True)
            tam = p.stat().st_size; shutil.move(str(p), str(dest))
            assert dest.exists() and dest.stat().st_size == tam and not p.exists()
            movidos.append({"de": str(p), "para": str(dest), "bytes": tam}); por_mod[stem] = por_mod.get(stem, 0) + 1
sem = [n for n in nomes if n not in por_mod]
fontes_ok = all((K / "TGLExt" / (n + ".lean")).exists() for n in nomes)
ep = Path(r"C:\t\k412c\reconstruir_r11_inicio_epoch.txt"); ep.write_text(str(int(time.time())), encoding="utf-8")
rec = {"quando": TS, "quarentena": str(Q), "n_arquivos_movidos": len(movidos), "bytes_movidos": sum(x["bytes"] for x in movidos), "arquivos_por_modulo": por_mod,
       "modulos_sem_artefato": sem, "fontes_dos_156_seguem_no_sandbox": fontes_ok, "epoch_inicio_da_rodada": int(ep.read_text()), "movidos": movidos,
       "nota": "so' artefatos de build (olean, ilean, trace, c, hash, setup) dos 156 modulos da decima primeira lista compilados no sandbox; nada apagado; as fontes ficam; o lake recompila a frio os 156 com as fontes da decima segunda lista"}
L.salvar_json(L.D / "kernel" / "FRIO_DAS_156_R11_v412.json", rec)
print("movidos:", len(movidos), "arquivos,", rec["bytes_movidos"], "bytes ->", Q, "| modulos sem artefato:", sem, "| fontes seguem:", fontes_ok)
sys.exit(0 if (not sem and fontes_ok and len(movidos) > 0) else 1)

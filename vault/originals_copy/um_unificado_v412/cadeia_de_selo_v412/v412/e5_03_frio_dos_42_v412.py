"""R5: para a compilacao ser A FRIO nos 153 modulos (e nao so' nos 111 que ainda nao estavam no sandbox), MOVE (nao apaga) para fora da arvore do lake os artefatos de build dos 42 modulos da setima lista
que o sandbox C:\\t\\k412c\\final ja tinha compilado: .lake\\build\\lib\\lean\\TGLExt\\<Nome>.{olean,ilean,trace,...} e .lake\\build\\ir\\TGLExt\\<Nome>.{c,...}. So' arquivos cujo nome, ate' o PRIMEIRO ponto, e' exatamente
o nome de um dos 42 modulos (Token2 nao casa com Token). As FONTES do sandbox nao sao tocadas. Destino: C:\\t\\k412c\\quarentena_build_42_<data>\\ (fora de work\\). Grava o epoch do inicio da rodada e o recibo."""
import datetime, json, os, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L
K = Path(r"C:\t\k412c\final")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
Q = Path(r"C:\t\k412c") / ("quarentena_build_42_" + TS)
m7 = L.ler_json(L.D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")
nomes = [x["modulo"] for x in m7["modulos"]]
assert len(nomes) == 42
nos_k = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")
assert not any((nos_k / (n + ".lean")).exists() for n in nomes), "um dos 42 existe no Nos: nao e' modulo novo"
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
            dest = Q / Path(*sub) / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            tam = p.stat().st_size
            shutil.move(str(p), str(dest))
            assert dest.exists() and dest.stat().st_size == tam and not p.exists()
            movidos.append({"de": str(p), "para": str(dest), "bytes": tam}); por_mod[stem] = por_mod.get(stem, 0) + 1
sem = [n for n in nomes if n not in por_mod]
fontes_ok = all((K / "TGLExt" / (n + ".lean")).exists() for n in nomes)
ep = Path(r"C:\t\k412c\reconstruir_r5_inicio_epoch.txt")
ep.write_text(str(int(time.time())), encoding="utf-8")
rec = {"quando": TS, "quarentena": str(Q), "n_arquivos_movidos": len(movidos), "bytes_movidos": sum(x["bytes"] for x in movidos), "arquivos_por_modulo": por_mod, "modulos_sem_artefato": sem,
       "fontes_dos_42_seguem_no_sandbox": fontes_ok, "epoch_inicio_da_rodada": int(ep.read_text()), "movidos": movidos,
       "nota": "so' artefatos de build (olean, ilean, trace, c, hash, setup) dos 42 modulos que o proprio construtor instalou e compilou no sandbox; nada apagado; as fontes ficam; o lake recompila os 42 a frio"}
L.salvar_json(L.D / "kernel" / "FRIO_DOS_42_R5_v412.json", rec)
print("movidos:", len(movidos), "arquivos,", rec["bytes_movidos"], "bytes ->", Q, "| modulos sem artefato:", sem, "| fontes seguem:", fontes_ok)
sys.exit(0 if (not sem and fontes_ok and len(movidos) > 0) else 1)

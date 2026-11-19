# -*- coding: utf-8 -*-
"""ensaio_conferidor_foco_nos_falso_v412.py -- (gerencia c1, 18/11/2026) ensaio de FUMACA do conferidor enxuto (conferir_pos_rito_v412_foco.py)
num Nos FALSO feito de COPIAS da v411 selada (o Nos real so' e' lido). Como o "depois" e' a propria v411, as checagens proprias da v412
(o um.py, o um_version, os registros novos, as bandeiras novas, os 156 modulos, a raiz) TEM de reprovar, e as de "nada perdido" (registros,
vereditos, chaves do selo, bandeiras herdadas, axiomas, gate, recusas) TEM de passar. Saida 0 so' se for exatamente assim."""
import hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
F = Path(r"C:\t\k412c") / ("ensaio_conferidor_foco_" + time.strftime("%Y%m%d_%H%M%S")); (F / "tgl_kernel").mkdir(parents=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):
    shutil.copyfile(NOS / rel, F / rel); assert sha(F / rel) == sha(NOS / rel)
shutil.copyfile(NOS / "tgl_kernel" / "TGLExt.lean", F / "tgl_kernel" / "TGLExt.lean")
(F / "rodada_v412_stdout.txt").write_text("ensaio\nRITO_RC=0\n", encoding="utf-8")
ap = {"ts": "ensaio", "backups": {rel: {"backup": str(NOS / rel), "bytes": (NOS / rel).stat().st_size, "sha16": sha(NOS / rel)[:16]} for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json")}}
apf = F / "APLICADO_AO_CANONICO_ensaio.json"; apf.write_text(json.dumps(ap), encoding="utf-8")
env = dict(os.environ, V412_NOS=str(F), V412_APLICADO=str(apf))
r = subprocess.run([sys.executable, "-B", "-X", "utf8", str(V / "conferir_pos_rito_v412_foco.py")], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-6000:]); print(r.stderr[-2000:])
rec = json.loads((V / "CONFERENCIA_POS_RITO_v412_FOCO_ENSAIO_NOS_FALSO.json").read_text(encoding="utf-8"))
res = {l["checagem"]: l["ok"] for l in rec["checagens"]}
TEM_DE_PASSAR = ["o stdout do rito termina com RITO_RC=0", "o veredito do gate", "nada formal sem selar", "nenhum registro com veredito da v411 sumiu", "nenhum veredito herdado mudou",
                 "toda chave do selo da v411", "todas as bandeiras True da v411 seguem True", "o relatorio de axiomas nao tem sorryAx", "nenhuma entrada do relatorio de axiomas fora do trio"]
TEM_DE_REPROVAR = ["o um.py do Nos e' o candidato", "o selo novo diz um_version v412", "os cinco registros novos", "as bandeiras True novas", "o veredito do estatuto da prova traz a escada de depois",
                   "modulos novos estao no kernel do Nos", "a raiz TGLExt.lean do Nos importa os 156"]
def acha(prefixo):
    a = [ok for k, ok in res.items() if prefixo in k]; assert len(a) == 1, (prefixo, len(a)); return a[0]
ruins = [p for p in TEM_DE_PASSAR if acha(p) is not True] + [p for p in TEM_DE_REPROVAR if acha(p) is not False]
print("ENSAIO DO CONFERIDOR ENXUTO NO NOS FALSO:", "COMO ESPERADO" if not ruins else "FORA DO ESPERADO: %s" % ruins, "| checagens", len(res), "| pasta", F)
sys.exit(0 if not ruins else 1)

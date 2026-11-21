# -*- coding: utf-8 -*-
"""guarda_titulo_versao_v413.py -- (Etapa 3 da v413, 20/11/2026; ordem do autor de 19/11 e de 20/11: todo .md emitido mostra a versao certa) a GUARDA
que RECUSA documento declarado com a versao de OUTRO selo no titulo, antes do handoff. Usa a lista da propria G1 (custodia_g1.espelho_pares.DECLARADOS)
e a MESMA regra do E03 da G1 (commit 66671b55d: a linha 1 de um .md declarado que termina em «(vNNN)» tem de trazer a versao do selo), e acrescenta,
para os textos que o pos-rito desta versao REGERA e que tem de nomear a versao: a arvore da prova (o titulo termina em «(vNNN)» com a versao do selo:
sem versao no titulo tambem RECUSA) e o handoff (HANDOFF_vNNN_CUSTODIA.md, titulo «# HANDOFF vNNN — ...»). Os documentos vivos sem versao no titulo
(o diario, o desenho, a estrutura, a nota) seguem como a G1 os trata. So' le. Saida 0 so' se tudo bater.
uso: python -I -B -X utf8 guarda_titulo_versao_v413.py <vNNN> [--nos <pasta>] [--sem-handoff]   (sem --nos: o Nos real; --sem-handoff: antes do compositor)"""
import json, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho_pares as EP  # noqa: E402

if len(sys.argv) < 2 or not re.fullmatch(r"v\d{3}", sys.argv[1]):
    print("uso: guarda_titulo_versao_v413.py <vNNN> [--nos <pasta>] [--sem-handoff]"); sys.exit(2)
v = sys.argv[1]
NOS = Path(sys.argv[sys.argv.index("--nos") + 1]) if "--nos" in sys.argv else Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
SEM_H = "--sem-handoff" in sys.argv
ruins, vistos = [], []
for nome in EP.DECLARADOS:
    p = NOS / nome
    if not (p.suffix.lower() == ".md" and p.is_file()):
        continue
    tit = p.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].strip()
    mv = re.search(r"\((v\d{3})\)\s*$", tit)
    vistos.append({"arquivo": nome, "titulo": tit[-90:], "versao_no_titulo": mv.group(1) if mv else None})
    if mv and mv.group(1) != v:                      # a regra do E03 da G1, a mesma
        ruins.append("%s: titulo com a versao de outro selo «%s» (o selo e' %s)" % (nome, tit[-60:], v))
# os que o pos-rito desta versao regera e que TEM de nomear a versao
arv = NOS / "A_PROVA_DA_QG_TGL_arvore.md"
if arv.is_file():
    ta = arv.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].strip()
    if not ta.endswith("(%s)" % v):
        ruins.append("A_PROVA_DA_QG_TGL_arvore.md: o titulo nao termina em (%s): «%s» -- rode arvore_da_prova.py %s" % (v, ta[-60:], v))
else:
    ruins.append("A_PROVA_DA_QG_TGL_arvore.md ausente")
if not SEM_H:
    ho = NOS / ("HANDOFF_%s_CUSTODIA.md" % v)
    th = ho.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].strip() if ho.is_file() else ""
    if not re.match(r"^# HANDOFF %s \u2014 " % v, th):
        ruins.append("%s: ausente ou titulo fora do molde «# HANDOFF %s — ...» («%s»)" % (ho.name, v, th[:60]))
    vistos.append({"arquivo": ho.name, "titulo": th[:90]})
rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "versao": v, "nos": str(NOS), "declarados_da_G1": list(EP.DECLARADOS), "vistos": vistos, "recusas": ruins, "ok": not ruins}
print(json.dumps(rec, ensure_ascii=False, indent=1))
print("GUARDA DO TITULO (%s):" % v, "LIMPA" if not ruins else "RECUSA (%d)" % len(ruins))
sys.exit(0 if not ruins else 1)

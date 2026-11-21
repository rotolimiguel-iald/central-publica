# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_23_texto_publico_gerar_v412.py (que fica intacto).
"""Etapa 2 da v413, bloco 5a: gera TEXTO_PUBLICO_v413.json (a secao do artigo “O que fica claro na v413” em PT e EN, em TeX, montada da pagina pinada pelo contrato e da traducao fiel; e o paragrafo de “P = nP” da secao 2,
desembrulhado) e confere: a mesma estrutura de blocos nas duas linguas; os mesmos termos entre crases, na mesma ordem; a travessia da guarda herdada sobre cada lingua. Compila as duas secoes com pdflatex (preambulo do
artigo do programa) em C:\\t\\k413c\\texto_teste (fora de work\\). O resumo do artigo nao muda (contrato da v413, secao 6: a pagina nao pede). No modo proposta, a pagina e a traducao sao as da proposta R1, e as saidas
levam o sufixo."""
import json, os, re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import texto_publico_v413 as TP
import guarda_frases_v413 as GF
import verificar_historia_texto_v413 as VH

import ajustes_revisao_v413 as AJR   # (revisao de terceiro do candidato) os ajustes minimos, aplicados por script ao texto lido; os arquivos ficam intactos
PT_ARQ, EN_ARQ = L.PAGINA, L.PAGINA_EN
pt = AJR.aplicar(PT_ARQ.read_bytes().decode("utf-8"), "pt")
en = AJR.aplicar(EN_ARQ.read_bytes().decode("utf-8"), "en")
bpt, ben = TP.blocos(pt), TP.blocos(en)
estr = lambda bl: [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in bl]
estrutura_igual = estr(bpt) == estr(ben)
cod_pt = re.findall(r"`([^`]+)`", pt); cod_en = re.findall(r"`([^`]+)`", en)
termos_iguais = cod_pt == cod_en
t_pt, tex_pt = TP.para_tex(pt, "pt")
t_en, tex_en = TP.para_tex(en, "en")
pnp = {"pt": TP.paragrafo_pnp(pt), "en": TP.paragrafo_pnp(en)}
trav = {lg: GF.travessia("artigo:" + lg, tex, "tex") for lg, tex in (("pt", tex_pt), ("en", tex_en))}
hist = {lg: VH.examinar([("secao_" + lg + "/L%d" % (i + 1), l) for i, l in enumerate(tex)]) for lg, tex in (("pt", tex_pt), ("en", tex_en))}
obj = {"modo": L.MODO, "fonte_pt": {"arquivo": str(PT_ARQ.relative_to(L.D)), "sha16": L.sha16_arq(PT_ARQ), "bytes": PT_ARQ.stat().st_size, "e_a_pagina_do_contrato": PT_ARQ == L.PAGINA_CONTRATO},
       "fonte_en": {"arquivo": str(EN_ARQ.relative_to(L.D)), "sha16": L.sha16_arq(EN_ARQ), "bytes": EN_ARQ.stat().st_size}, "ajustes_da_revisao_de_terceiro": AJR.recibo(),
       "titulo": {"pt": t_pt, "en": t_en}, "tex": {"pt": tex_pt, "en": tex_en}, "paragrafo_pnp_da_secao_2": pnp,
       "n_blocos": len(bpt), "n_linhas_tex": {"pt": len(tex_pt), "en": len(tex_en)}, "n_termos_entre_crases": len(cod_pt),
       "estrutura_igual_nas_duas_linguas": estrutura_igual, "termos_iguais_nas_duas_linguas": termos_iguais,
       "travessia": {lg: {"n_unidades": v["n_unidades"], "ok": v["ok"], "violacoes": [list(x[:3]) for x in v["violacoes"][:6]]} for lg, v in trav.items()},
       "historia": {lg: {"n_unidades": v["n_unidades_examinadas"], "achados": v["achados"][:6], "ok": v["ok"]} for lg, v in hist.items()},
       "resumo_do_artigo": "nao muda (contrato da v413, secao 6: o resumo nao muda, salvo o que a pagina disser; a pagina nao pede mudanca no resumo)"}
saida = L.saida("TEXTO_PUBLICO_v413.json")
L.salvar_json(saida, obj)
# compila (preambulo do artigo emitido pelo programa)
PRE = "\n".join([r"\documentclass[11pt]{article}", r"\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}", r"\usepackage{lmodern}\usepackage{cmap}\usepackage{microtype}",
                 r"\usepackage[a4paper,margin=2.3cm]{geometry}", r"\usepackage{amsmath,amssymb,amsthm}\usepackage[hidelinks]{hyperref}", r"\usepackage{parskip}\usepackage{booktabs}\usepackage{xcolor}",
                 r"\usepackage{graphicx}\usepackage{longtable}", r"\begin{document}", r"\tableofcontents"])
T = L.SANDBOX_PAI / ("texto_teste" + L.SUFIXO)
T.mkdir(parents=True, exist_ok=True)
res = {}
pdflatex = shutil.which("pdflatex")
for lg, tex in (("pt", tex_pt), ("en", tex_en)):
    f = T / ("secao_%s.tex" % lg)
    f.write_bytes((PRE + "\n" + "\n\n".join(tex) + "\n\\end{document}\n").encode("utf-8"))
    logs = []
    if pdflatex:
        for k in range(2):
            r = subprocess.run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", f.name], cwd=str(T), capture_output=True, timeout=300)
            logs.append(r.returncode)
    lp = T / ("secao_%s.log" % lg)
    log = lp.read_bytes().decode("utf-8", "replace") if lp.exists() else ""
    erros = re.findall(r"^! .*$", log, re.M)
    res[lg] = {"rc": logs, "erros": erros[:5], "overfull": len(re.findall(r"Overfull \\hbox", log)), "pdf_bytes": (T / ("secao_%s.pdf" % lg)).stat().st_size if (T / ("secao_%s.pdf" % lg)).exists() else 0,
               "caracteres_nao_definidos": sorted(set(re.findall(r"Unicode character (.) \(U\+[0-9A-F]+\)", log)))}
rec = {"ok": bool(pdflatex) and all(v["rc"] == [0, 0] and not v["erros"] and v["pdf_bytes"] > 0 for v in res.values()), "pdflatex": pdflatex, "resultado": res, "pasta": str(T), "modo": L.MODO,
       "nota": "compilacao isolada da secao (nao e' o artigo do programa; o ensaio a seco compila o artigo inteiro)"}
L.salvar_json(L.saida("TEXTO_PUBLICO_PDFLATEX_v413.json"), rec)
ok = estrutura_igual and termos_iguais and rec["ok"] and all(v["ok"] for v in trav.values()) and all(v["ok"] for v in hist.values())
print(json.dumps({"modo": L.MODO, "estrutura_igual": estrutura_igual, "termos_iguais": termos_iguais, "n_termos": len(cod_pt), "pdflatex_ok": rec["ok"], "travessia": {lg: (v["n_unidades"], v["ok"], [x[2] for x in v["violacoes"][:3]]) for lg, v in trav.items()},
                  "historia": {lg: (v["n_unidades_examinadas"], v["n_achados"]) for lg, v in hist.items()}}, ensure_ascii=False))
if not estrutura_igual:
    print("ESTRUTURA DIFERE:", [(a, b) for a, b in zip(estr(bpt), estr(ben)) if a != b][:5], len(bpt), len(ben))
if not termos_iguais:
    print("TERMOS DIFEREM:", [(a, b) for a, b in zip(cod_pt, cod_en) if a != b][:5], len(cod_pt), len(cod_en))
for lg, v in res.items():
    if v["erros"] or v["caracteres_nao_definidos"]:
        print("PDFLATEX", lg, v["erros"][:3], v["caracteres_nao_definidos"])
sys.exit(0 if ok else 1)

"""Etapa 2, bloco 5 (parte 1): gera TEXTO_PUBLICO_v412.json (secao do artigo PT/EN em TeX e o paragrafo de P = nP para o resumo) a partir da pagina R9 e da traducao EN;
confere a mesma estrutura nas duas linguas; compila as duas secoes com pdflatex (preambulo do artigo do programa) em C:\\t\\k412c\\texto_teste (fora de work\\)."""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, salvar_json, sha16_arq, estado_bloco
import texto_publico_v412 as TP

PT_ARQ = D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md"
EN_ARQ = D / "O_QUE_FICA_CLARO_v412_R13_EN.md"
assert sha16_arq(PT_ARQ) == "256a71e1bdf03239", "a pagina R13 nao e' a do contrato"
pt = PT_ARQ.read_bytes().decode("utf-8")
en = EN_ARQ.read_bytes().decode("utf-8")
bpt, ben = TP.blocos(pt), TP.blocos(en)
estrutura_pt = [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in bpt]
estrutura_en = [(t, (len(v) if isinstance(v, list) else (len(v[1]) if t == "table" else 1))) for t, v in ben]
assert estrutura_pt == estrutura_en, ("a traducao nao tem a mesma estrutura da pagina", [(a, b) for a, b in zip(estrutura_pt, estrutura_en) if a != b][:5], len(estrutura_pt), len(estrutura_en))
# os nomes entre crases sao os mesmos nas duas linguas, na mesma ordem
cod_pt = re.findall(r"`([^`]+)`", pt); cod_en = re.findall(r"`([^`]+)`", en)
assert cod_pt == cod_en, ("os termos entre crases diferem entre a pagina e a traducao", [(a, b) for a, b in zip(cod_pt, cod_en) if a != b][:5], len(cod_pt), len(cod_en))
t_pt, tex_pt = TP.para_tex(pt, "pt")
t_en, tex_en = TP.para_tex(en, "en")
pnp_pt, pnp_en = TP.paragrafo_pnp(pt), TP.paragrafo_pnp(en)
obj = {"fonte_pt": {"arquivo": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "sha16": sha16_arq(PT_ARQ)}, "fonte_en": {"arquivo": "O_QUE_FICA_CLARO_v412_R13_EN.md", "sha16": sha16_arq(EN_ARQ)},
       "titulo": {"pt": t_pt, "en": t_en}, "tex": {"pt": tex_pt, "en": tex_en}, "pnp_resumo": {"pt": pnp_pt, "en": pnp_en},
       "n_blocos": len(bpt), "n_linhas_tex": {"pt": len(tex_pt), "en": len(tex_en)}, "n_termos_entre_crases": len(cod_pt),
       "estrutura_igual_nas_duas_linguas": True, "termos_iguais_nas_duas_linguas": True}
saida = D / "TEXTO_PUBLICO_v412.json"
salvar_json(saida, obj)
# compila (preambulo do artigo emitido pelo programa)
PRE = "\n".join([r"\documentclass[11pt]{article}", r"\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}", r"\usepackage{lmodern}\usepackage{cmap}\usepackage{microtype}",
                 r"\usepackage[a4paper,margin=2.3cm]{geometry}", r"\usepackage{amsmath,amssymb,amsthm}\usepackage[hidelinks]{hyperref}", r"\usepackage{parskip}\usepackage{booktabs}\usepackage{xcolor}",
                 r"\usepackage{graphicx}\usepackage{longtable}", r"\begin{document}", r"\tableofcontents"])
T = Path(r"C:\t\k412c\texto_teste"); T.mkdir(parents=True, exist_ok=True)
res = {}
for lg, tex in (("pt", tex_pt), ("en", tex_en)):
    f = T / ("secao_%s.tex" % lg)
    f.write_bytes((PRE + "\n" + "\n\n".join(tex) + "\n\\end{document}\n").encode("utf-8"))
    logs = []
    for k in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f.name], cwd=str(T), capture_output=True, timeout=300)
        logs.append(r.returncode)
    log = (T / ("secao_%s.log" % lg)).read_bytes().decode("utf-8", "replace")
    erros = re.findall(r"^! .*$", log, re.M)
    res[lg] = {"rc": logs, "erros": erros[:5], "overfull": len(re.findall(r"Overfull \\hbox", log)), "pdf_bytes": (T / ("secao_%s.pdf" % lg)).stat().st_size if (T / ("secao_%s.pdf" % lg)).exists() else 0}
rec = {"ok": all(v["rc"] == [0, 0] and not v["erros"] and v["pdf_bytes"] > 0 for v in res.values()), "resultado": res, "pasta": str(T), "nota": "compilacao isolada da secao (nao e' o artigo do programa; o ensaio a seco compila o artigo inteiro)"}
salvar_json(D / "TEXTO_PUBLICO_PDFLATEX_v412.json", rec)
print(json.dumps(rec, ensure_ascii=False)[:600])
estado_bloco("5a_texto_publico_c4", rec["ok"], {"texto_publico": saida, "traducao_en": EN_ARQ, "conversor": D / "texto_publico_v412.py", "pdflatex": D / "TEXTO_PUBLICO_PDFLATEX_v412.json"},
             nota="secao do artigo PT/EN em TeX montada da pagina R13; EN traducao fiel (mesma estrutura, mesmos termos); pdflatex isolado", proximo="guarda de frases (bloco 4); depois registros e gerador")
sys.exit(0 if rec["ok"] else 1)

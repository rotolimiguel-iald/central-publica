# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_71_resultado_ensaio_v412.py (que fica intacto).
"""e7_71_resultado_ensaio_v413.py -- grava ENSAIO_RESULTADO_v413.json: o resultado do ensaio a seco da v413 sobre o candidato corrente (ensaio_a_seco_v413.py). Tudo lido do JSON que o proprio ensaio grava
(ensaio_a_seco_v413.json na pasta da cadeia) e da saida dele; nada digitado. Script da cadeia. uso: e7_71_resultado_ensaio_v413.py <saida_do_ensaio.txt>"""
import hashlib, json, os, shutil, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e7_lib_v413 as L

HERE = str(L.D)
REAL = str(L.saida("ensaio_a_seco_v413.json"))
OUT = str(L.saida("ENSAIO_RESULTADO_v413.json"))
SAIDA = sys.argv[1]


def resumo(p):
    d = json.load(open(p, encoding="utf-8"))
    u = d["unidade"]
    sim = d.get("simular_arvore_do_nos") or {}; ex = d.get("exame_pontos") or {}; art = d.get("artigo") or {}
    comp = {"guardas_estaticas_bancada": (d.get("guardas_estaticas_bancada") or {}).get("candidato_passa"), "vizinhos": d.get("viz_ok"), "fluxo": (d.get("mainflow") or {}).get("erro") is None, "selo": (d.get("selo") or {}).get("difere_e_nao_e_so_o_esperado") == [],
            "indice": (d.get("indice_da_iald") or {}).get("all_verified"), "citacoes_ok_do_um_py": (d.get("citacoes") or {}).get("ok_do_um_py"), "quadro_ok": (d.get("quadro") or {}).get("ok"), "markdown": all((d.get("markdown") or {}).values()), "manifest": d.get("manifest"),
            "kernel_embutido_igual_ao_sandbox": (d.get("kernel_embutido_vs_sandbox") or {}).get("n_diferentes") == 0,
            "simular_arvore_do_nos": bool(sim.get("rc") == 0 and sim.get("kf_all_verified") is True and (sim.get("formal_map_v413") or {}).get("ok") is True and all(((sim.get("registros") or {}).get(k_) or {}).get("all_verified") is True for k_ in (d.get("registros_v413") or {}).get("tudo_certo", {}))),
            "exame_pontos": bool(ex.get("rc") == 0 and ex.get("algum_falso") == []), "variantes": [k_ for k_ in ("variante", "variante_v411", "variante_v412", "variante_v413") if d.get(k_) is None]}
    for lg in ("pt", "en"):
        a = art.get(lg) or {}
        comp["artigo_%s_ok" % lg] = bool(a.get("pdf_ok") and a.get("pdflatex_rc") == [0, 0] and not a.get("latex_errors") and (a.get("v413") or {}).get("ok") and (a.get("v412") or {}).get("ok") and (a.get("v411") or {}).get("ok") and not a.get("faltam") and not a.get("toc_faltam"))
    r13 = d.get("registros_v413") or {}; gf = r13.get("guarda_de_frases") or {}
    return {"veredito": str(d.get("veredito"))[:60], "veredito_inteiro": str(d.get("veredito"))[:4000], "n_checagens_unidade": len(u), "n_ok": sum(1 for v in u.values() if v), "n_falhas": sum(1 for v in u.values() if not v), "falhas_da_unidade": sorted(k for k, v in u.items() if not v),
            "componentes": comp, "dry": d.get("dry"), "candidato_sha16": d.get("sha16"), "escada": d.get("escada"), "chaves_novas_no_core": (d.get("mainflow") or {}).get("chaves_novas"),
            "v413_examinou": {"tudo_certo": r13.get("tudo_certo"), "checagens_negadas": {k: v.get("checagens_negadas") for k, v in (r13.get("negativos") or {}).items()}, "escada_e_modulo_corrigido": r13.get("escada_e_modulo_corrigido"), "kh_n1_cobertura_v413": r13.get("kh_n1_cobertura_v413"),
                              "guarda_de_frases": {"controles_herdados": gf.get("controles_herdados"), "superficies_[unidades,violacoes]": gf.get("superficies"), "no_core_do_rito": gf.get("no_core_do_rito")},
                              "historia_de_conversa": r13.get("historia_de_conversa"), "ordem_de_chamada_dos_specs": {k: v for k, v in ((d.get("ordem_de_chamada_specs_v413") or {}).get("real") or {}).items() if k in ("ok", "n_checagens_examinadas", "n_specs")}}}


def tempo(p):
    ls = open(p, encoding="utf-8", errors="replace").read().splitlines()
    return {"rc": [l for l in ls if l.startswith("rc=")][-1] if [l for l in ls if l.startswith("rc=")] else None, "arquivo": p, "bytes": os.path.getsize(p), "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(p)))}


r = resumo(REAL)
out = {"o_que_e": "resultado do ensaio a seco da v413 (ensaio_a_seco_v413.py, derivado do da v412 por e7_06_derivar_ensaio_v413.py) sobre o candidato do contrato vigente", "saida": tempo(SAIDA), **r, "n_falhas": r["n_falhas"]}
L.salvar_json(OUT, out)
_SD = str(L.saida("ENSAIO_SAIDA_v413.txt"))
L.salvar_bytes(_SD, open(SAIDA, "rb").read())
print("gravado", OUT, "| sha16", L.sha16_arq(OUT))
print(r["veredito"], "| U:", r["n_checagens_unidade"], "ok", r["n_ok"], "falhas", r["n_falhas"], r["falhas_da_unidade"], "| comp:", {a: b_ for a, b_ in r["componentes"].items() if b_ is not True and a != "variantes"})

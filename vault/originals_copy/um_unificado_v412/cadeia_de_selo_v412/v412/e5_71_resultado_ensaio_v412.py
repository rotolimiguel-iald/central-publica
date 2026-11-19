# -*- coding: utf-8 -*-
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R5)] copia de e3_resultado_ensaio_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R5_PIPELINE_v412.json (derivador: e5_70_derivar_ensaio_r5_v412.py). O original fica intacto.
"""e3_resultado_ensaio_v412.py -- grava ENSAIO_RESULTADO_v412.json: o resultado do ensaio a seco da v412 sobre o candidato corrente (contrato R5, ensaio_a_seco_v412_r5.py; o resultado do R4 fica na copia .bak_<data> que este script faz antes de regravar).
Tudo lido do JSON que o proprio ensaio grava (ensaio_a_seco_v412.json na pasta da cadeia); nada digitado. Script da cadeia."""
import hashlib, json, os, shutil, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(HERE, "ensaio_a_seco_v412.json")
OUT = os.path.join(HERE, "ENSAIO_RESULTADO_v412.json")
SAIDA = sys.argv[1] if len(sys.argv) > 1 else r"C:\t\k412c\ensaio_adapt\r5_run1.txt"


def resumo(p):
    d = json.load(open(p, encoding="utf-8"))
    u = d["unidade"]
    sim = d.get("simular_arvore_do_nos") or {}; ex = d.get("exame_pontos") or {}; art = d.get("artigo") or {}
    comp = {"guardas_estaticas_bancada": (d.get("guardas_estaticas_bancada") or {}).get("candidato_passa"), "vizinhos": d.get("viz_ok"), "fluxo": (d.get("mainflow") or {}).get("erro") is None, "selo": (d.get("selo") or {}).get("difere_e_nao_e_so_o_esperado") == [],
            "indice": (d.get("indice_da_iald") or {}).get("all_verified"), "citacoes_ok_do_um_py": (d.get("citacoes") or {}).get("ok_do_um_py"), "quadro_ok": (d.get("quadro") or {}).get("ok"), "markdown": all((d.get("markdown") or {}).values()), "manifest": d.get("manifest"),
            "kernel_embutido_igual_ao_sandbox": (d.get("kernel_embutido_vs_sandbox") or {}).get("n_diferentes") == 0,
            "simular_arvore_do_nos": bool(sim.get("rc") == 0 and sim.get("kf_all_verified") is True and (sim.get("formal_map_v412") or {}).get("ok") is True and all(((sim.get("registros") or {}).get(k_) or {}).get("all_verified") is True for k_ in (d.get("registros_v412") or {}).get("tudo_certo", {}))),
            "exame_pontos": bool(ex.get("rc") == 0 and ex.get("algum_falso") == []), "variantes": [k_ for k_ in ("variante", "variante_v411", "variante_v412") if d.get(k_) is None]}
    for lg in ("pt", "en"):
        a = art.get(lg) or {}
        comp["artigo_%s_ok" % lg] = bool(a.get("pdf_ok") and a.get("pdflatex_rc") == [0, 0] and not a.get("latex_errors") and (a.get("v412") or {}).get("ok") and (a.get("v411") or {}).get("ok") and not a.get("faltam") and not a.get("toc_faltam"))
    r12 = d.get("registros_v412") or {}; gf = r12.get("guarda_de_frases") or {}
    return {"veredito": str(d.get("veredito"))[:60], "n_checagens_unidade": len(u), "n_ok": sum(1 for v in u.values() if v), "n_falhas": sum(1 for v in u.values() if not v), "falhas_da_unidade": sorted(k for k, v in u.items() if not v), "componentes": comp, "dry": d.get("dry"), "sha16_do_candidato": d.get("sha16"),
            "escada": d.get("escada"), "chaves_novas_no_core": (d.get("mainflow") or {}).get("chaves_novas"),
            "v412_examinou": {"ancoras_examinadas": r12.get("n_ancoras_examinadas"), "checagens_negadas": {k: v.get("checagens_negadas") for k, v in (r12.get("negativos") or {}).items()}, "guarda_de_frases": {"controles": gf.get("controles"), "controles_numerados": gf.get("controles_numerados"), "superficies_[unidades,violacoes]": gf.get("superficies"), "no_core_do_rito": gf.get("no_core_do_rito"), "recibo_de_unidades": gf.get("recibo_de_unidades")},
                              "historia_de_conversa": r12.get("historia_de_conversa"), "ordem_de_chamada_dos_specs": {k: v for k, v in ((d.get("ordem_de_chamada_specs_v412") or {}).get("real") or {}).items() if k in ("ok", "n_checagens_examinadas", "n_specs")}}}


def tempo(p):
    ls = open(p, encoding="utf-8", errors="replace").read().splitlines()
    return {"rc": [l for l in ls if l.startswith("rc=")][-1] if ls else None, "arquivo": p, "bytes": os.path.getsize(p), "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(p)))}


out = {"o_que_e": "resultado do ensaio a seco da v412 (ensaio_a_seco_v412_r5.py, derivado do ensaio do R4 por e5_70_derivar_ensaio_r5_v412.py) sobre o candidato do contrato R5", "real": {"saida": tempo(SAIDA), **resumo(REAL)}}
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(OUT) and open(OUT, "rb").read() != b:   # (backup de bytes do resultado anterior antes de regravar)
    _bk = OUT + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(OUT, "rb").read()); assert open(_bk, "rb").read() == open(OUT, "rb").read()
open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b)
os.replace(OUT + ".tmp", OUT)
_SD = os.path.join(HERE, "ENSAIO_SAIDA_v412.txt")
if os.path.exists(_SD) and open(_SD, "rb").read() != open(SAIDA, "rb").read():
    _bk = _SD + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(_SD, "rb").read()); assert open(_bk, "rb").read() == open(_SD, "rb").read()
shutil.copyfile(SAIDA, _SD)
print("gravado", OUT, len(b), "bytes, sha16", hashlib.sha256(b).hexdigest()[:16])
r = out["real"]; print(r["veredito"], "| U:", r["n_checagens_unidade"], "ok", r["n_ok"], "falhas", r["n_falhas"], r["falhas_da_unidade"], "| comp:", {a: b_ for a, b_ in r["componentes"].items() if b_ is not True and a != "variantes"})

# -*- coding: utf-8 -*-
"""e3_patch_6r_b.py -- ajusta o bloco (6r) ao candidato do contrato R4 (backup .bak_r1): (1) as listas de modulos das duas frentes (15 + 27 = 42) lidas do contrato, sem numero digitado; (2) o item (g) passa a cobrar a guarda de frases da R4:
as quatro funcoes EMBUTIDAS (guarda sobre UMA unidade, divisao em unidades, divisao do TeX, travessia) iguais as da cadeia por funcao; os 45 controles do contrato (os 21 numerados) rodados contra as funcoes EMBUTIDAS; o resultado que o rito grava no core
(guarda_frases_v412) igual a travessia refeita aqui e ao recibo GUARDA_v412_UNIDADES.json; zero violacao; zero unidade e' falha; frase plantada recusada. Script da cadeia."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e3_bloco_6r_v412.pytxt")
s = open(P, "rb").read().decode("utf-8")
if "_fonte_igual12" in s:
    print("ja'"); sys.exit(0)
open(P + ".bak_r1", "wb").write(s.encode("utf-8"))


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:90], s.count(old))
    s = s.replace(old, new)


troca("and len(_modA12) == int(_mA.group(1)) == 13 and len(_modB12) == int(_mB.group(1)) == 27 and set(_modA12 + _modB12) == {m_.split(\"/\")[-1][:-5] for m_ in DL.BUNDLE_RELS} and len(_modA12 + _modB12) == DL.N_BUNDLE == 40)",
      "and len(_modA12) == int(_mA.group(1)) and len(_modB12) == int(_mB.group(1)) and int(_mA.group(1)) + int(_mB.group(1)) == DL.N_BUNDLE == len(DL.BUNDLE_RELS) and set(_modA12 + _modB12) == {m_.split(\"/\")[-1][:-5] for m_ in DL.BUNDLE_RELS} and len(_modA12 + _modB12) == len(set(_modA12 + _modB12)) > 0)")
a = s.index("# --- (g) a guarda de frases da v412"); b = s.index("# --- (h) nenhum texto novo")
novo = '''# --- (g) a guarda de frases da v412 (contrato R4, secao 5): as quatro funcoes EMBUTIDAS (a guarda sobre UMA unidade, a divisao em unidades, a divisao do TeX, a travessia) sao as da cadeia, funcao por funcao; os controles do contrato rodam contra as funcoes EMBUTIDAS;
#      o resultado que o rito gravou no core (guarda_frases_v412) e' igual a travessia refeita aqui e ao recibo GUARDA_v412_UNIDADES.json; zero violacao; zero unidade e' falha; a frase proibida plantada e' recusada pela travessia
_rt12_src = open(os.path.join(HERE, "runtime_v412_guarda.py"), encoding="utf-8").read(); _seg12 = {d_.name: ast.get_source_segment(_rt12_src, d_) for d_ in ast.parse(_rt12_src).body if isinstance(d_, ast.FunctionDef)}
_fns12 = ("_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia")
_fonte_igual12 = {f_: bool(f_ in _seg12 and _seg12[f_].strip() == _insp12.getsource(getattr(um, f_)).strip()) for f_ in _fns12}
_gf_antes12 = (_GF12c.g12, _GF12c.violacoes, _GF12c.travessia)
_GF12c.g12 = _GF12c.violacoes = um._v412_guarda_frases; _GF12c.travessia = um._v412_travessia   # (os controles da cadeia, rodados contra as funcoes EMBUTIDAS no candidato)
try:
    _cc12 = _GF12c.controles()
finally:
    _GF12c.g12, _GF12c.violacoes, _GF12c.travessia = _gf_antes12
_n_cc12 = len(_cc12); _nok_cc12 = sum(1 for x_ in _cc12 if x_["ok"]); _num_cc12 = {str(x_["controle"]) for x_ in _cc12}
_rc12 = json.load(open(os.path.join(HERE, "GUARDA_FRASES_v412.json"), encoding="utf-8")); _ru12 = json.load(open(os.path.join(HERE, "GUARDA_v412_UNIDADES.json"), encoding="utf-8"))
_gv12 = c.get("guarda_frases_v412") or {}
_corpo12 = lambda n_: {"corpo": {k_: _SP12[n_].get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": _SP12[n_]["veredito_prefixo"] + "__" + _SP12[n_]["veredito_sufixo"]}
_tr12 = {"registro:" + n_: um._v412_travessia("registro:" + n_, _corpo12(n_)) for n_ in _N12}
_tr12.update({"artigo:" + l_: um._v412_travessia("artigo:" + l_, list(um._V412_SECAO[l_]), "tex") for l_ in ("pt", "en")}); _tr12.update({"resumo:" + l_: um._v412_travessia("resumo:" + l_, {l_: [um._V412_TOPO["pnp"][l_]]}) for l_ in ("pt", "en")})
_igual_recibo12 = {k_: bool(k_ in _ru12["superficies"] and _ru12["superficies"][k_]["n_unidades"] == t_["n_unidades"] and _ru12["superficies"][k_]["ok"] is True) for k_, t_ in _tr12.items()}
_no_core12 = {n_: bool(_gv12.get(n_, {}).get("n_unidades_examinadas") == _tr12["registro:" + n_]["n_unidades"] > 0 and _gv12[n_].get("n_violacoes") == 0) for n_ in _N12}
_plant12 = {}
for _k12, _t12 in _tr12.items():
    _lg12 = "en" if _k12.endswith(":en") else "pt"
    _f12 = ("A TGL prova P = NP das máquinas de Turing." if _lg12 == "pt" else "The TGL proves P = NP of the Turing machines.", "O prêmio Millennium está resolvido." if _lg12 == "pt" else "The Millennium Prize problem is solved.")
    _plant12[_k12] = [um._v412_travessia("plantada", (list(um._V412_SECAO[_lg12]) + [x_] if _k12.startswith("artigo") else {"corpo": [t_["texto"] for t_ in _t12["unidades"]][:3] + [x_]}), "tex" if _k12.startswith("artigo") else "dados")["ok"] is False for x_ in _f12]
_vazia12 = um._v412_travessia("vazia", {})
U["v412_a_guarda_de_frases_da_travessia_embutida_e_a_da_cadeia_controles_do_contrato_recibo_e_core"] = bool(all(_fonte_igual12.values()) and _n_cc12 == _nok_cc12 >= 45 and {str(i_) for i_ in range(1, 22)} <= _num_cc12 and _rc12.get("ok") is True and _rc12.get("n_controles") == _n_cc12 and _rc12.get("n_ok") == _nok_cc12
                                                                  and all(t_["ok"] and t_["n_unidades"] > 0 and not t_["violacoes"] for t_ in _tr12.values()) and len(_tr12) == 8 and all(_igual_recibo12.values()) and all(_no_core12.values()) and len(_no_core12) == 4
                                                                  and all(all(v_) and len(v_) == 2 for v_ in _plant12.values()) and _vazia12["ok"] is False and _vazia12["n_unidades"] == 0 and _ru12.get("ok") is True and _ru12["n_superficies"] == len(_ru12["superficies"]) >= 14 and all(v_["n_unidades"] > 0 for v_ in _ru12["superficies"].values()))
'''
s = s[:a] + novo + s[b:]
# o item (h) e o rep: a secao e o paragrafo vem do programa; os nomes das variaveis do bloco antigo saem
troca('"guarda_de_frases": {"fonte_igual_a_da_cadeia": bool(_fonte_cadeia12 and _fonte_cadeia12.strip() == _fonte_prog12.strip()), "controles": [_nok_cc12, _n_cc12], "por_grupo": {k_: [sum(1 for x_ in v_ if x_["ok"]), len(v_)] for k_, v_ in _cc12.items()}, "violacoes_nos_textos_novos": {k_: len(v_) for k_, v_ in _viol12.items()}, "plantadas_recusadas": _plant12},',
      '"guarda_de_frases": {"funcoes_embutidas_iguais_as_da_cadeia": _fonte_igual12, "controles": [_nok_cc12, _n_cc12], "controles_numerados": sorted(_num_cc12), "superficies": {k_: [t_["n_unidades"], len(t_["violacoes"])] for k_, t_ in _tr12.items()}, "igual_ao_recibo": _igual_recibo12, "no_core_do_rito": {n_: [(_gv12.get(n_) or {}).get("n_unidades_examinadas"), (_gv12.get(n_) or {}).get("n_violacoes")] for n_ in _N12}, "plantadas_recusadas": _plant12, "recibo_de_unidades": {"n_superficies": _ru12["n_superficies"], "n_unidades_total": _ru12["n_unidades_total"], "ok": _ru12["ok"]}},')
troca('"| guarda de frases:", [_nok_cc12, _n_cc12],', '"| guarda de frases (controles; unidades por superficie):", [_nok_cc12, _n_cc12], {k_: t_["n_unidades"] for k_, t_ in _tr12.items()},')
open(P, "wb").write(s.encode("utf-8"))
print("ok")

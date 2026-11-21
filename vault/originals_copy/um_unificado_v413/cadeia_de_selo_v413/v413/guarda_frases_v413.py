# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\guarda_frases_v412_r7.py (que fica intacto). A guarda da v413 e' a da v412, HERDADA SEM MUDANCA (contrato da v413, secao 5).
"""guarda_frases_v413.py -- a GUARDA DE FRASES da cadeia da v413: a da v412, herdada sem mudanca. As funcoes sao carregadas do um.py SELADO da v412 (base_v412\\um.py, por trecho: _v412_guarda_frases, a divisao em
unidades e a travessia, o ponto unico de chamada; e _v392_guarda_texto, a P18; e _v411_guarda_frases, para o controle 21). Confere que o codigo selado e' o mesmo da fonte que a v412 embutiu (runtime_v412_guarda.py).
Roda os 21 controles HERDADOS da v412 (o MESMO codigo dos controles, lido de v412\\guarda_frases_v412_r7.py por ast, sobre os mesmos textos da pagina R25 da v412) e compara cada resultado com o recibo da v412
(GUARDA_FRASES_v412.json): nenhuma obrigacao mudou. Roda tambem os controles de “P = nP” sobre a pagina da v413 (a pinada pelo contrato, ou a proposta no modo proposta): o paragrafo da secao 2 passa; sem a frase da ressalva
e' recusado; o titulo da secao 2 passa; com a frase proibida e' recusado. Grava GUARDA_FRASES_v413.json.
uso: python -B -X utf8 guarda_frases_v413.py [arquivo ...]   (sem arquivo: os controles; com arquivo: varre cada um pela travessia; rc 1 se houver violacao)"""
import ast, json, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e7_lib_v413 as L
import base_um_v412 as B

NOMES_SELADOS = ["_v392_guarda_texto", "_v411_guarda_frases", "_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia"]
NS = B.carregar(NOMES_SELADOS)
B.chamar_resolvendo(NS, "_v411_guarda_frases", "aquecimento")
B.chamar_resolvendo(NS, "_v412_guarda_frases", "aquecimento")
B.chamar_resolvendo(NS, "_v392_guarda_texto", "aquecimento")
B.chamar_resolvendo(NS, "_v412_travessia", "aquecimento", {"a": "aquecimento"})
g11 = NS["_v411_guarda_frases"]
g12 = NS["_v412_guarda_frases"]
travessia = NS["_v412_travessia"]
p18 = NS["_v392_guarda_texto"]
violacoes = g12

# o codigo selado da guarda e' o da fonte que a v412 embutiu (runtime_v412_guarda.py, na pasta da v412)
RUNTIME_V412 = L.V412 / "runtime_v412_guarda.py"
_rt = RUNTIME_V412.read_bytes().decode("utf-8").replace("\r\n", "\n")
IDENTIDADE = {}
for _n in ("_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia"):
    _sel = B.trecho(_n).rstrip("\n")
    _m = re.search(r"(?ms)^def %s\(.*?(?=^def |\Z)" % re.escape(_n), _rt)
    IDENTIDADE[_n] = bool(_m) and _m.group(0).rstrip("\n") == _sel
assert all(IDENTIDADE.values()), ("o codigo selado da guarda da v412 nao e' o da fonte embutida", IDENTIDADE)

# os 21 controles herdados: o MESMO codigo de v412\guarda_frases_v412_r7.py (por ast), num namespace com as funcoes SELADAS e a pasta da v412
SRC12 = (L.V412 / "guarda_frases_v412_r7.py").read_bytes().decode("utf-8")
T12 = ast.parse(SRC12)
QUERO = {"secao", "titulo", "citacao", "sem_frase_com", "controles", "PAG", "PADRAO_RESSALVA", "FRASE_PROIBIDA", "MARCAS", "FLU", "_src11", "_t11", "LISTAS11", "V411_ANTES", "NOME_F34", "NOME_F37", "NOME_F37B", "_T11"}


def _nome(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


NS_C = {"re": re, "ast": ast, "json": json, "os": os, "Path": Path, "D": L.V412, "B": B, "violacoes": violacoes, "travessia": travessia, "g11": g11, "g12": g12, "p18": p18}
_trechos = [n for n in T12.body if _nome(n) in QUERO]
assert {_nome(n) for n in _trechos} == QUERO, ("o molde dos controles nao tem o que se espera", sorted(QUERO - {_nome(n) for n in _trechos}))
for _n in _trechos:
    exec(compile(ast.Module(body=[_n], type_ignores=[]), "<v412/guarda_frases_v412_r7.py:%s>" % _nome(_n), "exec"), NS_C)
controles_herdados = NS_C["controles"]
NOME_F34, NOME_F37, NOME_F37B = NS_C["NOME_F34"], NS_C["NOME_F37"], NS_C["NOME_F37B"]


def pagina_v413():
    import registros_v413 as RG
    import ajustes_revisao_v413 as AJR   # (revisao de terceiro) a traducao lida com os ajustes minimos, como a pagina (RG.PAG_D ja' os traz)
    en = RG.desembrulhar(AJR.aplicar(L.PAGINA_EN.read_bytes().decode("utf-8"), "en")) if L.PAGINA_EN.exists() else None
    return {"pt": RG.PAG_D, "en": en}


def controles_v413():
    """os controles de “P = nP” sobre a pagina da v413 (PT e, se houver, a traducao EN): o paragrafo da secao 2 passa; sem a frase da ressalva e' recusado (F70); o titulo da secao 2 passa; com a frase proibida e' recusado"""
    res = []
    P = pagina_v413()
    for lg in ("pt", "en"):
        if not P[lg]:
            res.append({"controle": "v413-pagina", "lingua": lg, "rotulo": "a traducao da pagina existe", "esperado": "existe", "obtido": None, "ok": False})
            continue
        sec = NS_C["secao"](P[lg], 2)
        q = re.findall(r"^> (.+)$", sec, re.M)
        tit = sec.split("\n", 1)[0].lstrip("#").strip()

        def unid(n, rotulo, texto, esperado, regra=None, regra_ausente=None):
            v = violacoes(texto); nomes = sorted({x[0] for x in v})
            ok = (not v) if esperado == "passa" else (bool(v) and (regra is None or any(x[0].startswith(regra) for x in v)) and (regra_ausente is None or not any(x[0].startswith(regra_ausente) for x in v)))
            res.append({"controle": n, "lingua": lg, "rotulo": rotulo, "esperado": esperado + (" (" + regra + ")" if regra else ""), "obtido": nomes, "ok": bool(ok), "texto_inicio": texto[:120]})
        if len(q) != 1:
            res.append({"controle": "v413-1", "lingua": lg, "rotulo": "a secao 2 da pagina tem UM bloco de citacao", "esperado": "1", "obtido": len(q), "ok": False})
            continue
        par = q[0]
        unid("v413-1", "o paragrafo da secao 2 da pagina da v413 passa", par, "passa")
        try:
            sem_r = NS_C["sem_frase_com"](par, NS_C["PADRAO_RESSALVA"][lg])
            unid("v413-2", "o mesmo paragrafo sem a frase da ressalva e' recusado", sem_r, "recusa", "F70")
        except AssertionError as e_:
            res.append({"controle": "v413-2", "lingua": lg, "rotulo": "o mesmo paragrafo sem a frase da ressalva e' recusado", "esperado": "recusa (F70)", "obtido": "frase da ressalva nao achada uma vez: %r" % (e_,), "ok": False})
        unid("v413-4", "o titulo da secao 2 da pagina da v413 passa", tit, "passa")
        unid("v413-8", "o paragrafo mais uma frase que diz que a TGL prova P = NP de Turing: recusado pela regra herdada", par + " " + NS_C["FRASE_PROIBIDA"][lg], "recusa", None, "F70")
    return res


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rc = 0
    for p in sys.argv[1:]:
        t = travessia(p, Path(p).read_bytes().decode("utf-8"))
        print(p, "->", t["n_unidades"], "unidades", "LIMPO" if t["ok"] else t["violacoes"][:4]); rc |= (not t["ok"])
    if not sys.argv[1:]:
        ch = controles_herdados()
        r12 = L.ler_json(L.V412 / "GUARDA_FRASES_v412.json")
        antes = {(str(x["controle"]), x["lingua"]): x for x in r12["controles"]}
        difs = [(str(x["controle"]), x["lingua"]) for x in ch if (str(x["controle"]), x["lingua"]) not in antes or antes[(str(x["controle"]), x["lingua"])]["ok"] != x["ok"]
                or antes[(str(x["controle"]), x["lingua"])]["obtido"] != json.loads(json.dumps(x["obtido"], ensure_ascii=False))]
        cv = controles_v413()
        n, nok = len(ch), sum(1 for x in ch if x["ok"])
        n13, nok13 = len(cv), sum(1 for x in cv if x["ok"])
        herdada_ok = n == nok == len(r12["controles"]) and n > 0 and not difs
        out = {"contrato": "GUARDA_FRASES_v413", "regra": "contrato da v413, secao 5: a guarda da v412 herdada inteira, sem mudar obrigacao; os controles herdados rodados; os de “P = nP” sobre a pagina da v413",
               "modo": L.MODO, "funcao": "as funcoes do um.py SELADO da v412 (base_v412\\um.py, por trecho)", "base_um_py_sha16": L.sha16_arq(L.D / "base_v412" / "um.py"),
               "identidade_com_a_fonte_embutida_na_v412": {"arquivo": "v412/runtime_v412_guarda.py", "sha16": L.sha16_arq(RUNTIME_V412), "por_funcao": IDENTIDADE},
               "nomes_herdados_lidos_do_um_selado": {"f34": NOME_F34, "f37": NOME_F37, "f37b_nao_sai": NOME_F37B},
               "controles_herdados": {"molde": "v412/guarda_frases_v412_r7.py (controles(), por ast)", "molde_sha16": L.sha16_arq(L.V412 / "guarda_frases_v412_r7.py"), "pagina_dos_controles": "v412/o_que_fica_claro_REV25/O_QUE_FICA_CLARO_v412_R25.md",
                                      "n": n, "n_ok": nok, "recibo_da_v412": {"arquivo": "v412/GUARDA_FRASES_v412.json", "sha16": L.sha16_arq(L.V412 / "GUARDA_FRASES_v412.json"), "n": len(r12["controles"]), "n_ok": r12["n_ok"]},
                                      "diferem_do_recibo_da_v412": difs, "numerados": sorted({str(x["controle"]) for x in ch}), "controles": ch, "ok": herdada_ok},
               "controles_da_pagina_v413": {"pagina": str(L.PAGINA.relative_to(L.D)), "pagina_sha16": L.sha16_arq(L.PAGINA), "traducao_en": str(L.PAGINA_EN.relative_to(L.D)) if L.PAGINA_EN.exists() else None,
                                            "traducao_en_sha16": L.sha16_arq(L.PAGINA_EN) if L.PAGINA_EN.exists() else None, "n": n13, "n_ok": nok13, "controles": cv, "ok": n13 > 0 and n13 == nok13},
               "ok": herdada_ok and n13 > 0 and n13 == nok13}
        L.salvar_json(L.saida("GUARDA_FRASES_v413.json"), out)
        print("controles herdados:", nok, "/", n, "| diferem do recibo da v412:", difs, "| controles da pagina v413:", nok13, "/", n13)
        for x in ch + cv:
            if not x["ok"]:
                print("  FALHOU:", x["controle"], x["lingua"], x["rotulo"][:90], "| esperado:", x["esperado"], "| obtido:", str(x["obtido"])[:200])
        rc = 0 if out["ok"] else 1
    sys.exit(rc)

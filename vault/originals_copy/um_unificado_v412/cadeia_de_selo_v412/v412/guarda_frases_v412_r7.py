# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de guarda_frases_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R11)] copia de guarda_frases_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e5_22_derivar_texto_r7_v412.py). O original fica intacto.
"""guarda_frases_v412.py -- (contrato R11, secao 5, que e' a do R4) a GUARDA DE FRASES da cadeia da v412: carrega a _v411_guarda_frases do um.py selado da v411 (por trecho, base_um_v411.py) e o codigo novo de runtime_v412_guarda.py
(a mesma fonte que vai embutida no programa: _v412_guarda_frases sobre UMA unidade, a divisao em unidades e a travessia, o ponto unico de chamada), roda os 21 controles obrigatorios (cada um em portugues e em ingles onde cabe)
e grava GUARDA_FRASES_v412.json (recibo dos controles: o esperado e o obtido). Os nomes das duas obrigacoes herdadas que saem so' pelo nome inteiro sao LIDOS do um.py selado (nunca digitados).
uso: python -B -X utf8 guarda_frases_v412.py [arquivo ...]   (sem arquivo: so' os controles; com arquivo: varre cada um pela travessia; rc 1 se houver violacao)"""
import ast, json, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e7_lib_v412 import D, salvar_json, sha16_arq
import base_um_v411 as B

NS = B.carregar(["_v392_guarda_texto", "_v411_guarda_frases"])
B.chamar_resolvendo(NS, "_v411_guarda_frases", "aquecimento")
RUNTIME_ARQ = D / "runtime_v412_guarda.py"
exec(compile(RUNTIME_ARQ.read_bytes().decode("utf-8"), str(RUNTIME_ARQ), "exec"), NS)
g11 = NS["_v411_guarda_frases"]
g12 = NS["_v412_guarda_frases"]
travessia = NS["_v412_travessia"]
p18 = NS["_v392_guarda_texto"]
violacoes = g12

# os nomes das duas obrigacoes herdadas que saem pelo nome inteiro: lidos do programa selado
_T11 = B.texto()
NOME_F34 = re.search(r'"(F34_p_igual_np_sem_o_qualificador_do_dicionario_ou_a_ressalva_open)"', _T11).group(1)
NOME_F37 = re.search(r'"(F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor)"', _T11).group(1)
NOME_F37B = re.search(r'"(F37b_p_igual_np_e_turing_juntos_sem_o_qualificador_no_mesmo_trecho)"', _T11).group(1)
_rt = RUNTIME_ARQ.read_bytes().decode("utf-8")
assert NOME_F34 in _rt and NOME_F37 in _rt and NOME_F37B not in _rt.split("def _v412_unidades_de_texto")[0].split("out_ = [v_ for v_")[1], "os nomes herdados nao batem com os do codigo novo"

PAG = {"pt": (D / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md").read_bytes().decode("utf-8"), "en": (D / "O_QUE_FICA_CLARO_v412_R25_EN.md").read_bytes().decode("utf-8")}


def secao(md, n):
    m = re.search(r"(^## %d\. .*?)(?=^## %d\. |\Z)" % (n, n + 1), md, re.S | re.M)
    assert m, n
    return m.group(1).rstrip()


def titulo(md, n):
    return secao(md, n).split("\n", 1)[0].lstrip("#").strip()


def citacao(md, n):
    q = re.findall(r"^> (.+)$", secao(md, n), re.M)
    assert len(q) == 1
    return q[0]


def sem_frase_com(texto, padrao):
    fr = re.split(r"(?<=\.) ", texto)
    k = [i for i, f in enumerate(fr) if re.search(padrao, f)]
    assert len(k) == 1, (padrao, len(k))
    return " ".join(f for i, f in enumerate(fr) if i != k[0])


PADRAO_RESSALVA = {"pt": r"máquina de fita.*não está demonstrado", "en": r"tape machine.*has not been shown"}
FRASE_PROIBIDA = {"pt": "A TGL prova P = NP das máquinas de Turing.", "en": "The TGL proves P = NP of the Turing machines."}
MARCAS = {"pt": ("nas classes do seu dicionário", "Na máquina de fita, o custo polinomial não está demonstrado."), "en": ("in the classes of its dictionary", "On the tape machine, the polynomial cost has not been shown.")}
FLU = {  # textos de controle (frases proprias dos controles)
    "pt": {"sozinho": "O programa tratou de Navier–Stokes em três dimensões.", "demonstrada": "A regularidade global de Navier–Stokes está demonstrada.", "cond": "Este é um resultado condicional sobre Navier–Stokes.", "afirma": "A regularidade de Navier–Stokes está demonstrada.",
           "neg": "Este texto não diz que a regularidade de Navier–Stokes tenha sido demonstrada.", "neg_demonstrada": "Este texto não diz que a equação de Navier–Stokes tenha regularidade global demonstrada.", "sem_forma": "Navier–Stokes foi estudada na cascata.", "premio": "O problema do Milênio está em aberto."},
    "en": {"sozinho": "The program dealt with Navier–Stokes in three dimensions.", "demonstrada": "The global regularity of Navier–Stokes is demonstrated.", "cond": "This is a conditional result on Navier–Stokes.", "afirma": "The global regularity of Navier–Stokes is demonstrated.",
           "neg": "This text does not say that the regularity of Navier–Stokes has been shown.", "neg_demonstrada": "This text does not say that the Navier–Stokes equation has demonstrated global regularity.", "sem_forma": "Navier–Stokes was studied in the cascade.", "premio": "The Millennium Prize problem is open."},
}
_src11 = (D.parent / "v411" / "guarda_frases_v411.py").read_bytes().decode("utf-8")
_t11 = ast.parse(_src11)
LISTAS11 = {n.targets[0].id: ast.literal_eval(n.value) for n in _t11.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("PROIBIDAS", "LIMPAS")}
V411_ANTES = json.loads((D.parent / "v411" / "GUARDA_FRASES_v411.json").read_bytes().decode("utf-8"))["controle_negativo"]


def controles():
    res = []

    def reg(n, lingua, rotulo, esperado, obtido_ok, detalhe):
        res.append({"controle": n, "lingua": lingua, "rotulo": rotulo, "esperado": esperado, "obtido": detalhe, "ok": bool(obtido_ok)})

    def unid(n, lingua, rotulo, texto, esperado, regra=None, regra_ausente=None):
        v = violacoes(texto); nomes = sorted({x[0] for x in v})
        ok = (not v) if esperado == "passa" else (bool(v) and (regra is None or any(x[0].startswith(regra) for x in v)) and (regra_ausente is None or not any(x[0].startswith(regra_ausente) for x in v)))
        reg(n, lingua, rotulo, esperado + (" (" + regra + ")" if regra else ""), ok, nomes)
    for lg in ("pt", "en"):
        P = PAG[lg]; PAR = citacao(P, 2); TIT = titulo(P, 2)
        SEM_R = sem_frase_com(PAR, PADRAO_RESSALVA[lg])
        a_marca, b_marca = MARCAS[lg]
        # ---- sobre P = nP
        unid(1, lg, "o paragrafo da secao 2 da pagina passa", PAR, "passa")
        unid(2, lg, "o mesmo paragrafo sem a frase da ressalva e' recusado", SEM_R, "recusa", "F70")
        unid(3, lg, "o titulo solto “P = nP” e' recusado", "P = nP", "recusa", "F70")
        unid(4, lg, "o titulo da secao 2 da pagina R25 passa", TIT, "passa")
        t = travessia("controle5", {"corpo": ["P = nP é teorema." if lg == "pt" else "P = nP is a theorem.", PAR]})
        reg(5, lg, "dois paragrafos: o primeiro com “P = nP” sem marcas e o segundo com as duas marcas: o primeiro e' recusado, o segundo passa", "1o recusado, 2o limpo",
            t["n_unidades"] == 2 and bool(t["unidades"][0]["regras"]) and not t["unidades"][1]["regras"], [u["regras"] for u in t["unidades"]])
        t = travessia("controle6", {"corpo": {"diz": ["P = nP é teorema da TGL." if lg == "pt" else "P = nP is a theorem of the TGL."], "limites": [PAR]}, "veredito": "TGL_X__GATE_UNMOVED"})
        reg(6, lg, "um corpo de registro com “P = nP” num campo e as marcas em outro: o campo sem as marcas e' recusado", "campo diz recusado; limites limpo",
            any("diz" in v[0] and v[2].startswith("F70") for v in t["violacoes"]) and not any("limites" in v[0] for v in t["violacoes"]), [(v[0], v[2][:3]) for v in t["violacoes"]])
        outro = "en" if lg == "pt" else "pt"
        tx_sem = "P = nP é teorema da TGL." if lg == "pt" else "P = nP is a theorem of the TGL."
        t7 = travessia("controle7", {"pt": [tx_sem, ], "en": [citacao(PAG["en"], 2)]}) if lg == "pt" else travessia("controle7", {"pt": [citacao(PAG["pt"], 2)], "en": [tx_sem]})
        k_sem = "pt" if lg == "pt" else "en"
        reg(7, lg, "a unidade em %s com “P = nP” e a unidade em %s com as marcas: a de %s e' recusada e a de %s passa" % (k_sem, outro, k_sem, outro), "recusada so' a de " + k_sem,
            any(v[0].startswith("/" + k_sem) and v[2].startswith("F70") for v in t7["violacoes"]) and not any(v[0].startswith("/" + outro) for v in t7["violacoes"]), [(v[0], v[2][:3]) for v in t7["violacoes"]])
        unid(8, lg, "as duas marcas mais uma frase que diz que a TGL prova P = NP de Turing: recusada pela regra herdada", PAR + " " + FRASE_PROIBIDA[lg], "recusa", None, "F70")
        nove = ("P = nP e a máquina de Turing, " + a_marca + ". " + b_marca) if lg == "pt" else ("P = nP and the Turing machine, " + a_marca + ". " + b_marca)
        unid(9, lg, "as duas marcas, e “P = nP” e “Turing” no mesmo segmento sem a ressalva local: recusada pela obrigacao local da v409 (F37b), que nao saiu", nove, "recusa", NOME_F37B[:5])
        t10 = travessia("controle10", ["## P = nP", "- P = nP é verdade" if lg == "pt" else "- P = nP is true", "| P = nP | x |"]) if True else None
        tipos = [u["tipo"] for u in t10["unidades"]]
        reg(10, lg, "um titulo, um item de lista e uma celula de tabela, cada um com “P = nP” sem as marcas: os tres recusados", "tres recusados (titulo, item, celula)",
            tipos[:2] == ["titulo", "item"] and "celula" in tipos and all(u["regras"] for u in t10["unidades"] if "P = nP" in u["inicio"]), [(u["tipo"], len(u["regras"])) for u in t10["unidades"]])
        # ---- sobre o nome dos fluidos
        unid(11, lg, "o titulo da secao 3 da pagina passa", titulo(P, 3), "passa")
        unid(12, lg, "o paragrafo da secao 3 passa", citacao(P, 3), "passa")
        f6 = re.search(r"(?:não diz que a equação de Navier–Stokes|it does not say that the Navier–Stokes equation)[^;.]*", P)
        unid(13, lg, "a frase da secao 6 passa", f6.group(0), "passa")
        unid(14, lg, "“a regularidade global esta demonstrada”, com o nome, e' recusada", FLU[lg]["demonstrada"], "recusa", "F68")
        unid(15, lg, "o nome sozinho numa frase sem a forma e' recusado", FLU[lg]["sozinho"], "recusa", "F68a")
        unid(16, lg, "uma frase condicional seguida de OUTRA frase com o nome e a afirmacao: a segunda e' recusada, a primeira passa", FLU[lg]["cond"] + " " + FLU[lg]["afirma"], "recusa", "F68")
        r16a = violacoes(FLU[lg]["cond"]); reg("16b", lg, "a frase condicional sozinha passa", "passa", not r16a, [x[0] for x in r16a])
        unid(17, lg, "uma frase na forma da negacao seguida de OUTRA frase com o nome sem a forma: a segunda e' recusada", FLU[lg]["neg"] + " " + FLU[lg]["sem_forma"], "recusa", "F68a")
        r17a = violacoes(FLU[lg]["neg"]); reg("17b", lg, "a frase na forma da negacao sozinha passa", "passa", not r17a, [x[0] for x in r17a])
        unid(18, lg, "uma frase na forma da negacao que contem “demonstrada” passa", FLU[lg]["neg_demonstrada"], "passa")
        unid(19, lg, "a palavra do premio e' recusada em qualquer unidade", FLU[lg]["premio"], "recusa", "F69")
    # ---- sobre a travessia
    t20 = travessia("superficie_vazia", {})
    reg(20, "pt+en", "uma superficie vazia e' falha", "ok False por SUPERFICIE_VAZIA", (not t20["ok"]) and t20["n_unidades"] == 0 and any(v[2].startswith("SUPERFICIE_VAZIA") for v in t20["violacoes"]), t20["violacoes"][:1])
    t20b = travessia("superficie_so_numeros", {"a": 1, "b": [2, None]})
    reg("20b", "pt+en", "uma superficie sem folha de texto tambem e' falha", "ok False", not t20b["ok"], t20b["violacoes"][:1])
    # (21) o texto herdado da v411, passado pela guarda herdada, da o mesmo resultado de antes
    difs = []; n21 = 0
    for item in V411_ANTES["proibidas"]:
        n21 += 1
        if [x[0] for x in g11(item["frase"])] != item["violacoes"]:
            difs.append(item["frase"][:60])
    for item in V411_ANTES["limpas"]:
        n21 += 1
        if [x[0] for x in g11(item["frase"])] != [x[0] if isinstance(x, list) else x for x in item["violacoes"]]:
            difs.append(item["frase"][:60])
    reg(21, "pt+en", "o texto herdado da v411 (as listas de controle da v411), passado pela guarda herdada, da o mesmo resultado de antes (a guarda herdada nao mudou)", "mesmos resultados (%d textos)" % n21, n21 > 0 and not difs, {"n": n21, "diferem": difs[:3]})
    return res


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cn = controles()
    n = len(cn); nok = sum(1 for x in cn if x["ok"])
    rc = 0 if (n == nok and n > 0) else 1
    for p in sys.argv[1:]:
        t = travessia(p, Path(p).read_bytes().decode("utf-8"))
        print(p, "->", t["n_unidades"], "unidades", "LIMPO" if t["ok"] else t["violacoes"][:4]); rc |= (not t["ok"])
    if not sys.argv[1:]:
        out = {"contrato": "GUARDA_FRASES_v412", "regra": "contrato R11, secao 5.3 (a do R4, sem mudanca): 21 controles obrigatorios, cada um em portugues e em ingles onde cabe", "fonte_da_funcao": {"arquivo": "runtime_v412_guarda.py", "sha16": sha16_arq(RUNTIME_ARQ)},
               "nomes_herdados_lidos_do_um_selado": {"f34": NOME_F34, "f37": NOME_F37, "f37b_nao_sai": NOME_F37B}, "pagina": {"arquivo": "o_que_fica_claro_REV25/O_QUE_FICA_CLARO_v412_R25.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md"), "traducao_en_sha16": sha16_arq(D / "O_QUE_FICA_CLARO_v412_R25_EN.md")},
               "n_controles": n, "n_ok": nok, "controles_numerados": sorted({str(x["controle"]) for x in cn}), "controles": cn, "ok": rc == 0}
        salvar_json(D / "GUARDA_FRASES_v412.json", out)
    print("controles:", nok, "/", n, "| numerados:", sorted({str(x["controle"]) for x in cn}, key=lambda s: (len(s), s)))
    for x in cn:
        if not x["ok"]:
            print("  FALHOU:", x["controle"], x["lingua"], x["rotulo"][:80], "| esperado:", x["esperado"], "| obtido:", str(x["obtido"])[:160])
    sys.exit(rc)

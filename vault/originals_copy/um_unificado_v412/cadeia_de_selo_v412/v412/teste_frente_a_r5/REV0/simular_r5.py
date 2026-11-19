# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026 - simulacao NO NIVEL DA CONTA do desenho R5 do teste da frente A (copiador contra impostor).

NENHUM modelo de linguagem e' chamado. Nenhum dado observacional e' aberto. So' logica sobre o catalogo de assercoes
que o Kimi extraiu dos quatro textos publicos (K08\\FORMULA\\catalogo_assercoes.py, lido sem alterar).

O que o script faz:
  1. para cada um dos quatro textos, monta as VERSOES do desenho: ORIG (o texto como esta'), INV(a) (uma afirmacao
     invertida, so' as coerentes), DEL(a) (uma afirmacao retirada), PC (a frase que contradiz a igualdade de beta,
     acrescentada), PAR (mesma coisa dita de outra forma: mesmo sentido, linhas em outro lugar, letra nova) e PAR+INV(a);
  2. calcula, por logica, o SENTIDO de cada item em cada versao: SIM, NAO, CALA (o texto nao diz) ou AMBAS (diz as duas);
  3. passa cada versao por MECANISMOS de resposta, cada um definido pelo que ele 'pagou' (o que consulta do texto presente);
  4. pontua valor e indice (a linha do texto presente que sustenta a resposta) e mostra que instrumento separa que mecanismo.

A separacao aqui e' POR CONSTRUCAO DA CONTA: mostra que o desenho PODE separar; nao e' resultado de modelo.
Uso: simular_r5.py [--saida <pasta>]"""
import hashlib, importlib.util, json, random, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
CAT = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\FORMULA\catalogo_assercoes.py")
SAIDA = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else AQUI
SEMENTE = 2026111601

spec = importlib.util.spec_from_file_location("catalogo_assercoes_k08", CAT)
cat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cat)

ITENS = [a for a in cat.ATOMOS if a != "leitura_pt"]          # a variavel livre PT/EN nao e' item
FONTES = ["ABSTRACT", "READ_BRIEF", "LLMS", "README"]
SIM, NAO, CALA, AMBAS = "SIM", "NAO", "CALA", "AMBAS"


# ---------------------------------------------------------------------------------------------- versoes e sentido
def versao_orig(f):
    cfg = cat.FONTES[f]
    un = {}
    for a in cfg["assercoes"]:
        if a["atomo"] == "leitura_pt":
            continue
        un.setdefault(a["atomo"], {})[a["signo"]] = a["linha"]
    der = [{"lits": [(x, s) for x, s in d["literals"]], "linha": d["linha"]} for d in cfg["derivacoes"]]
    return {"fonte": f, "tipo": "ORIG", "alvo": None, "units": un, "derivs": der, "forma": "orig", "letra_nova": set()}


def copia(v, tipo, alvo):
    return {"fonte": v["fonte"], "tipo": tipo, "alvo": alvo, "units": {a: dict(s) for a, s in v["units"].items()},
            "derivs": [dict(d) for d in v["derivs"]], "forma": v["forma"], "letra_nova": set(v["letra_nova"])}


def fecho(v):
    """Encadeamento para a frente sobre as clausulas (todas de Horn). Devolve (fatos, suporte, coerente).
    Itens ditos nas duas polaridades (AMBAS) ficam fora da propagacao e sao marcados 'a parte."""
    fatos, sup, ok = {}, {}, True
    for a, s in v["units"].items():
        if len(s) == 1:
            sg = next(iter(s))
            fatos[a] = sg
            sup[a] = {s[sg]}
    mudou = True
    while mudou:
        mudou = False
        for d in v["derivs"]:
            livres = [(x, s) for x, s in d["lits"] if not (x in fatos and fatos[x] == -s)]
            if any(x in fatos and fatos[x] == s for x, s in d["lits"]):
                continue                                      # clausula ja' satisfeita
            if any(len(v["units"].get(x, {})) == 2 for x, _ in d["lits"]):
                continue                                      # toca item contraditorio: nao propaga
            if len(livres) == 0:
                ok = False
            elif len(livres) == 1:
                x, s = livres[0]
                if x not in fatos:
                    fatos[x] = s
                    sup[x] = {d["linha"]} | set().union(*[sup.get(y, set()) for y, _ in d["lits"] if y != x])
                    mudou = True
    return fatos, sup, ok


def sentido(v, a, cache={}):
    k = id(v)
    if k not in cache:
        cache[k] = fecho(v)
    fatos, sup, _ = cache[k]
    s = v["units"].get(a, {})
    if len(s) == 2:
        return AMBAS, set(s.values())
    if a in fatos:
        return (SIM if fatos[a] == 1 else NAO), set(sup[a])
    return CALA, set()


def coerente(v):
    return fecho(v)[2]


def inv(v, a):
    w = copia(v, "INV" if v["tipo"] == "ORIG" else v["tipo"] + "+INV", a)
    (sg, ln), = w["units"][a].items()
    w["units"][a] = {-sg: ln}
    w["letra_nova"].add(a)                                    # a linha foi reescrita: a letra original nao esta' mais la'
    return w


def dele(v, a):
    w = copia(v, "DEL", a)
    del w["units"][a]
    return w


def pc(v, a="beta_forma"):
    w = copia(v, "PC", a)
    (sg, ln), = w["units"][a].items()
    w["units"][a] = {sg: ln, -sg: 100000 + ln}                # a frase acrescentada fica em linha nova
    return w


def par(v):
    """Mesmo sentido, outra forma: as linhas mudam de lugar (indice novo) e a letra original some de todas."""
    w = copia(v, "PAR", None)
    mapa = lambda ln: 50000 + (ln * 7919) % 9973
    w["units"] = {a: {s: mapa(ln) for s, ln in d.items()} for a, d in w["units"].items()}
    for d in w["derivs"]:
        d["linha"] = mapa(d["linha"])
    w["forma"] = "par"
    w["letra_nova"] = set(w["units"])
    return w


# ---------------------------------------------------------------------------------------------- mecanismos
ORIG = {f: versao_orig(f) for f in FONTES}
MEM_TEXTO = {f: {a: sentido(ORIG[f], a) for a in ITENS} for f in FONTES}       # decorou ESTE texto publico


def _doutrina():
    d = {}
    for a in ITENS:
        vals = {MEM_TEXTO[f][a][0] for f in FONTES} - {CALA}
        d[a] = (next(iter(vals)) if len(vals) == 1 else CALA)                  # os quatro textos nunca se contradizem
    return d


MEM_DOUTRINA = _doutrina()                                                     # decorou a doutrina (os quatro)


def m_copiador(v, a, rng):
    return sentido(v, a)


def m_constante(v, a, rng):
    return SIM, set()


def m_decorou_texto(v, a, rng):
    return MEM_TEXTO[v["fonte"]][a]


def m_decorou_doutrina(v, a, rng):
    val = MEM_DOUTRINA[a]
    return val, (MEM_TEXTO[v["fonte"]][a][1] if val != CALA else set())


def _letra(v, a):
    """A letra ORIGINAL do item esta' na versao presente? (so' em linha nao reescrita e fora da parafrase)"""
    if v["forma"] == "par" or a in v["letra_nova"] or a not in v["units"]:
        return None
    o = ORIG[v["fonte"]]["units"].get(a)
    if not o:
        return None
    (sg, ln), = o.items()
    return (SIM if sg == 1 else NAO), {ln}                    # casa a letra: devolve o sentido ORIGINAL daquela linha


def m_casa_letra_senao_cala(v, a, rng):
    r = _letra(v, a)
    return r if r else (CALA, set())


def m_casa_letra_senao_memoria(v, a, rng):
    r = _letra(v, a)
    return r if r else MEM_TEXTO[v["fonte"]][a]


def m_le_e_acrescenta(v, a, rng):
    val, idx = sentido(v, a)
    if val == CALA and MEM_DOUTRINA[a] != CALA:
        return MEM_DOUTRINA[a], set()
    return val, idx


def m_le_so_a_primeira(v, a, rng):
    val, idx = sentido(v, a)
    if val == AMBAS:
        (sg, ln), = ORIG[v["fonte"]]["units"][a].items()
        return (SIM if sg == 1 else NAO), {ln}
    return val, idx


def m_le_so_a_ultima(v, a, rng):
    val, idx = sentido(v, a)
    if val == AMBAS:
        (sg, ln), = ORIG[v["fonte"]]["units"][a].items()
        return (NAO if sg == 1 else SIM), {100000 + ln}
    return val, idx


def m_remendo(v, a, rng):
    """Decorou o texto e sabe que o desenho muda UM item: troca o valor de um item sorteado (o mesmo para a versao toda)."""
    val, idx = MEM_TEXTO[v["fonte"]][a]
    if v["tipo"] == "ORIG":
        return val, idx
    # semente derivada por sha256 (o hash() do Python muda a cada processo; aqui a conta tem de reproduzir)
    r = random.Random(int(hashlib.sha256(repr((SEMENTE, v["fonte"], v["tipo"], v["alvo"])).encode("utf-8")).hexdigest()[:12], 16))
    alvo = r.choice(ITENS)
    if a == alvo:
        val = {SIM: NAO, NAO: SIM, CALA: SIM, AMBAS: SIM}[val]
    return val, idx


MECANISMOS = [
    ("copiador (lê o texto presente)", m_copiador, "o texto presente"),
    ("impostor constante (sempre SIM)", m_constante, "nada"),
    ("decorou este texto público", m_decorou_texto, "a pergunta e a memória do texto público"),
    ("decorou a doutrina (os quatro textos)", m_decorou_doutrina, "a pergunta e a memória da doutrina"),
    ("casa a letra original; sem letra, cala", m_casa_letra_senao_cala, "as linhas que conservam a letra original"),
    ("casa a letra original; sem letra, responde de cor", m_casa_letra_senao_memoria, "a letra original e a memória"),
    ("lê o texto mas acrescenta do que sabe", m_le_e_acrescenta, "o texto presente e a memória da doutrina"),
    ("lê só a primeira linha do par contraditório", m_le_so_a_primeira, "o texto presente, menos a frase acrescentada"),
    ("lê só a última linha do par contraditório", m_le_so_a_ultima, "o texto presente, menos a linha original"),
    ("decorou e remenda um item ao acaso", m_remendo, "a memória e o conhecimento do desenho"),
]


def acerta(v, a, resp, com_indice=True):
    val, idx = resp
    vv, sup = sentido(v, a)
    if val != vv:
        return False
    if not com_indice:
        return True
    if vv == CALA:
        return len(idx) == 0
    if vv == AMBAS:
        return idx == sup
    return len(idx & sup) > 0


# ---------------------------------------------------------------------------------------------- instrumentos
def montar():
    """Devolve a lista (instrumento, versao, itens decisivos). Itens decisivos = onde o sentido difere do texto publico
    (ou, no ORIG e no PAR, todos os itens: sao os controles do 'sabe ler' e do 'a forma nao muda o sentido')."""
    out, contas = [], {}
    for f in FONTES:
        o = ORIG[f]
        assert coerente(o), f
        ditos = [a for a in ITENS if a in o["units"]]
        calados = [a for a in ITENS if sentido(o, a)[0] == CALA and MEM_DOUTRINA[a] != CALA]
        out.append(("A. ORIG: o texto como está (todos os itens)", o, list(ITENS)))
        out.append(("B. SILÊNCIO: o que a doutrina diz e este texto não", o, calados))
        invs = []
        for a in ditos:
            w = inv(o, a)
            if coerente(w):
                dec = [b for b in ITENS if sentido(w, b)[0] != sentido(o, b)[0]]
                out.append(("C. INV: uma afirmação invertida", w, dec))
                invs.append(a)
        dels = []
        for a in ditos:
            w = dele(o, a)
            if sentido(w, a)[0] == CALA:
                out.append(("D. DEL: uma afirmação retirada", w, [a]))
                dels.append(a)
        w = pc(o)
        out.append(("E. PC: a frase contrária acrescentada (o texto diz as duas)", w, ["beta_forma"]))
        p = par(o)
        out.append(("F. PAR: o mesmo dito de outra forma (todos os itens)", p, list(ITENS)))
        for a in invs:
            w = inv(p, a)
            dec = [b for b in ITENS if sentido(w, b)[0] != sentido(p, b)[0]]
            out.append(("G. PAR+INV: outra forma e uma afirmação invertida", w, dec))
        # o conjunto minimo proposto: 3 versoes com 5 afirmacoes invertidas cada (grupos disjuntos), na forma original e em outra forma
        grupos, multi_ok = [invs[i:i + 5] for i in (0, 5, 10)], []
        for base, rot in ((o, "H. INV×5: cinco afirmações invertidas na mesma versão"), (p, "I. PAR+INV×5: outra forma e cinco invertidas")):
            for g in grupos:
                w = base
                for a in g:
                    w = inv(w, a)
                w["tipo"], w["alvo"] = rot[:1] + "5", tuple(g)
                dec = [b for b in ITENS if sentido(w, b)[0] != sentido(base, b)[0]]
                multi_ok.append(coerente(w) and len(g) == 5 and set(g) <= set(dec))
                out.append((rot, w, dec))
        contas[f] = {"afirmacoes": len(ditos), "inversoes_coerentes": len(invs), "inversoes_incoerentes": sorted(set(ditos) - set(invs)),
                     "grupos_de_cinco_coerentes": multi_ok,
                     "retiradas_que_calam": len(dels), "retiradas_que_seguem_ditas_por_derivacao": sorted(set(ditos) - set(dels)),
                     "silencios_naturais": len(calados), "itens": len(ITENS)}
    return out, contas


def main():
    rng = random.Random(SEMENTE)
    casos, contas = montar()
    instrumentos = sorted({c[0] for c in casos})
    tab = {}
    for nome, fn, pagou in MECANISMOS:
        for ins in instrumentos:
            n = ok = okv = 0
            for i, v, dec in casos:
                if i != ins:
                    continue
                for a in dec:
                    r = fn(v, a, rng)
                    n += 1
                    ok += acerta(v, a, r, True)
                    okv += acerta(v, a, r, False)
            tab.setdefault(nome, {})[ins] = {"itens": n, "acertos_valor_e_indice": ok, "acertos_so_valor": okv,
                                             "fracao": (ok / n if n else None), "fracao_so_valor": (okv / n if n else None)}
    # quantos pares decisivos o catalogo oferece
    n_pares = {ins: sum(len(dec) for i, v, dec in casos if i == ins) for ins in instrumentos}
    n_versoes = {ins: sum(1 for i, v, dec in casos if i == ins) for ins in instrumentos}
    res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "nota": "simulacao no nivel da conta; nenhum modelo chamado; separacao por construcao",
           "catalogo": str(CAT), "catalogo_sha256": hashlib.sha256(CAT.read_bytes()).hexdigest(), "semente": SEMENTE,
           "itens": len(ITENS), "por_texto": contas, "versoes_por_instrumento": n_versoes, "itens_decisivos_por_instrumento": n_pares,
           "mecanismos": [{"nome": n, "pagou": p} for n, _, p in MECANISMOS], "tabela": tab}
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "RESULTADO_SIMULACAO_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    # tabela em texto
    L = ["# Simulação no nível da conta do desenho R5 (nenhum modelo chamado)", "",
         "> Gerado por `simular_r5.py`; a separação é por construção da conta. Fração de itens decisivos certos (valor e índice); entre parênteses, só o valor.", ""]
    cab = ["mecanismo (o que pagou)"] + [i.split(":")[0] for i in instrumentos]
    L.append("| " + " | ".join(cab) + " |")
    L.append("|" + "---|" * len(cab))
    for nome, _, pagou in MECANISMOS:
        linha = ["%s *(%s)*" % (nome, pagou)]
        for ins in instrumentos:
            c = tab[nome][ins]
            linha.append("—" if not c["itens"] else "%.2f (%.2f)" % (c["fracao"], c["fracao_so_valor"]))
        L.append("| " + " | ".join(linha) + " |")
    L += ["", "Instrumentos:", ""] + ["- %s — %d versões, %d itens decisivos" % (i, n_versoes[i], n_pares[i]) for i in instrumentos]
    L += ["", "Por texto:", ""]
    for f in FONTES:
        c = contas[f]
        L.append("- %s: %d afirmações; %d inversões coerentes (incoerentes: %s); %d retiradas que calam (seguem ditas por derivação: %s); %d silêncios naturais"
                 % (f, c["afirmacoes"], c["inversoes_coerentes"], ", ".join(c["inversoes_incoerentes"]) or "nenhuma", c["retiradas_que_calam"],
                    ", ".join(c["retiradas_que_seguem_ditas_por_derivacao"]) or "nenhuma", c["silencios_naturais"]))
    (SAIDA / "RESULTADO_SIMULACAO_R5.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

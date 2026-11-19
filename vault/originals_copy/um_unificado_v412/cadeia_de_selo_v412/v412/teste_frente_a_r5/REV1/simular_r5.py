# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026, R1 (depois da conferencia distinta) - simulacao NO NIVEL DA CONTA do desenho R5 do teste da
frente A (copiador contra impostor).

NENHUM modelo de linguagem e' chamado. Nenhum dado observacional e' aberto. So' logica sobre o catalogo de assercoes
que o Kimi extraiu dos quatro textos publicos (K08\\FORMULA\\catalogo_assercoes.py, lido sem alterar).

O QUE MUDOU NA R1 (achados da conferencia): a estatistica passa a ser o PAR, como no teorema; a unidade passa a ser o
GRUPO (duas versoes complementares do mesmo texto); entram tres mecanismos que percebem a mudanca pela letra sem ler o
sentido; o calculo do sentido deixa de ser guardado pelo id do objeto.

O DESENHO CRUZADO. Um grupo toca 2m afirmacoes de um texto. Na versao V, as m primeiras sao INVERTIDAS (passam a dizer
o contrario) e as m ultimas sao REESCRITAS sem mudar o sentido. Na versao V', o contrario. As duas versoes mexem nas
MESMAS linhas e diferem no sentido: sao o par do teorema para quem so' consultou a memoria, a letra original ou 'onde
o texto mudou'. Um par de item (uma afirmacao tocada) esta' certo se a resposta esta' certa, com a linha, em V e em V'.

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
LINHA_NOVA = 100000                                           # as frases acrescentadas ficam em linhas novas


# ---------------------------------------------------------------------------------------------- versoes e sentido
def versao_orig(f):
    cfg = cat.FONTES[f]
    un = {}
    for a in cfg["assercoes"]:
        if a["atomo"] == "leitura_pt":
            continue
        un.setdefault(a["atomo"], {})[a["signo"]] = a["linha"]
    der = [{"lits": [(x, s) for x, s in d["literals"]], "linha": d["linha"]} for d in cfg["derivacoes"]]
    return {"fonte": f, "tipo": "ORIG", "alvo": None, "units": un, "derivs": der, "forma": "orig", "letra_nova": set(), "frase_nova": set()}


def copia(v, tipo, alvo):
    return {"fonte": v["fonte"], "tipo": tipo, "alvo": alvo, "units": {a: dict(s) for a, s in v["units"].items()},
            "derivs": [dict(d) for d in v["derivs"]], "forma": v["forma"], "letra_nova": set(v["letra_nova"]),
            "frase_nova": set(v.get("frase_nova", ()))}


def fecho(v):
    """Encadeamento para a frente sobre as clausulas (todas de Horn). Devolve (fatos, suporte, coerente).
    Itens ditos nas duas polaridades (AMBAS) ficam fora da propagacao. O resultado fica guardado NA PROPRIA versao."""
    if "_fecho" in v:
        return v["_fecho"]
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
            if any(x in fatos and fatos[x] == s for x, s in d["lits"]):
                continue                                      # clausula ja' satisfeita
            if any(len(v["units"].get(x, {})) == 2 for x, _ in d["lits"]):
                continue                                      # toca item contraditorio: nao propaga
            livres = [(x, s) for x, s in d["lits"] if not (x in fatos and fatos[x] == -s)]
            if len(livres) == 0:
                ok = False
            elif len(livres) == 1:
                x, s = livres[0]
                if x not in fatos:
                    fatos[x] = s
                    sup[x] = {d["linha"]} | set().union(*[sup.get(y, set()) for y, _ in d["lits"] if y != x])
                    mudou = True
    v["_fecho"] = (fatos, sup, ok)
    return v["_fecho"]


def sentido(v, a):
    fatos, sup, _ = fecho(v)
    s = v["units"].get(a, {})
    if len(s) == 2:
        return AMBAS, set(s.values())
    if a in fatos:
        return (SIM if fatos[a] == 1 else NAO), set(sup[a])
    return CALA, set()


def coerente(v):
    return fecho(v)[2]


def tocar(v, invertidas, reescritas, tipo, alvo):
    """Versao com algumas afirmacoes invertidas (o sinal troca) e outras reescritas (so' a letra muda)."""
    w = copia(v, tipo, alvo)
    for a in invertidas:
        (sg, ln), = w["units"][a].items()
        w["units"][a] = {-sg: ln}
        w["letra_nova"].add(a)
    for a in reescritas:
        w["letra_nova"].add(a)
    return w


def contradizer(v, contrarias, iscas, tipo, alvo):
    """Acrescenta uma frase nova a cada afirmacao tocada (a linha original fica). Nas `contrarias` a frase nova diz o
    contrario (o texto passa a dizer as duas); nas `iscas` a frase nova repete o mesmo sentido (nada muda)."""
    w = copia(v, tipo, alvo)
    for a in contrarias:
        (sg, ln), = w["units"][a].items()
        w["units"][a] = {sg: ln, -sg: LINHA_NOVA + ln}
        w["frase_nova"].add(a)
    for a in iscas:
        w["frase_nova"].add(a)
    return w


def outra_forma(v):
    """Mesmo sentido, outra forma inteira: as linhas mudam de lugar e a letra original some de todas."""
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
CONTRA = {SIM: NAO, NAO: SIM, CALA: CALA, AMBAS: AMBAS}


def mexido(v):
    return v["forma"] == "par" or bool(v["letra_nova"]) or bool(v["frase_nova"])


def m_copiador(v, a):
    return sentido(v, a)


def m_constante(v, a):
    return SIM, set()


def m_decorou_texto(v, a):
    return MEM_TEXTO[v["fonte"]][a]


def m_decorou_doutrina(v, a):
    val = MEM_DOUTRINA[a]
    return val, (MEM_TEXTO[v["fonte"]][a][1] if val != CALA else set())


def _letra(v, a):
    """A letra ORIGINAL do item esta' na versao presente? (so' em linha nao reescrita e fora da outra forma)"""
    if v["forma"] == "par" or a in v["letra_nova"] or a not in v["units"]:
        return None
    o = ORIG[v["fonte"]]["units"].get(a)
    if not o:
        return None
    (sg, ln), = o.items()
    return (SIM if sg == 1 else NAO), {ln}                    # casa a letra: devolve o sentido ORIGINAL daquela linha


def m_casa_letra_senao_cala(v, a):
    r = _letra(v, a)
    return r if r else (CALA, set())


def m_casa_letra_senao_memoria(v, a):
    r = _letra(v, a)
    return r if r else MEM_TEXTO[v["fonte"]][a]


def m_le_e_acrescenta(v, a):
    val, idx = sentido(v, a)
    if val == CALA and MEM_DOUTRINA[a] != CALA:
        return MEM_DOUTRINA[a], set()
    return val, idx


def m_le_so_a_primeira(v, a):
    val, idx = sentido(v, a)
    if val == AMBAS:
        (sg, ln), = ORIG[v["fonte"]]["units"][a].items()
        return (SIM if sg == 1 else NAO), {ln}
    return val, idx


def m_le_so_a_ultima(v, a):
    val, idx = sentido(v, a)
    if val == AMBAS:
        (sg, ln), = ORIG[v["fonte"]]["units"][a].items()
        return (NAO if sg == 1 else SIM), {LINHA_NOVA + ln}
    return val, idx


def m_remendo(v, a):
    """Decorou o texto e sabe que o desenho muda itens: troca o valor de um item sorteado (o mesmo para a versao toda)."""
    val, idx = MEM_TEXTO[v["fonte"]][a]
    if not mexido(v):
        return val, idx
    r = random.Random(int(hashlib.sha256(repr((SEMENTE, v["fonte"], v["tipo"], v["alvo"])).encode("utf-8")).hexdigest()[:12], 16))
    if a == r.choice(ITENS):
        val = {SIM: NAO, NAO: SIM, CALA: SIM, AMBAS: SIM}[val]
    return val, idx


def m_contrario_de_tudo(v, a):
    """Percebe que o texto nao e' o decorado e responde o CONTRARIO do decorado em tudo (nao le o sentido)."""
    val, idx = MEM_TEXTO[v["fonte"]][a]
    return (CONTRA[val], idx) if mexido(v) else (val, idx)


def m_contrario_onde_mudou(v, a):
    """Compara a letra presente com a decorada e responde o CONTRARIO do decorado so' nas linhas que mudaram."""
    val, idx = MEM_TEXTO[v["fonte"]][a]
    if v["forma"] == "par" or a in v["letra_nova"]:
        return CONTRA[val], idx
    return val, idx


def m_diz_as_duas_se_ha_frase_nova(v, a):
    """Decorou o texto; onde ve^ uma frase acrescentada sobre o item, responde 'diz as duas' sem ler nenhuma."""
    val, idx = MEM_TEXTO[v["fonte"]][a]
    if a in v["frase_nova"]:
        (sg, ln), = ORIG[v["fonte"]]["units"][a].items()
        return AMBAS, {ln, LINHA_NOVA + ln}
    return val, idx


MECANISMOS = [
    ("copiador: lê o texto presente", m_copiador, "o texto presente"),
    ("responde sempre o mesmo", m_constante, "nada"),
    ("decorou este texto público", m_decorou_texto, "a pergunta e a memória do texto público"),
    ("decorou a doutrina (os quatro textos)", m_decorou_doutrina, "a pergunta e a memória da doutrina"),
    ("casa a letra original; sem ela, cala", m_casa_letra_senao_cala, "as linhas que conservam a letra original"),
    ("casa a letra original; sem ela, responde de cor", m_casa_letra_senao_memoria, "a letra original e a memória"),
    ("lê, mas acrescenta do que sabe", m_le_e_acrescenta, "o texto presente e a memória da doutrina"),
    ("lê só a primeira das duas linhas contrárias", m_le_so_a_primeira, "o texto presente, menos a frase acrescentada"),
    ("lê só a última das duas", m_le_so_a_ultima, "o texto presente, menos a linha original"),
    ("decorou e remenda um item ao acaso", m_remendo, "a memória e o conhecimento do desenho"),
    ("percebe que o texto mudou e responde o contrário em tudo", m_contrario_de_tudo, "a memória e 'o texto mudou?'"),
    ("responde o contrário só onde a letra mudou", m_contrario_onde_mudou, "a memória e 'que linhas mudaram?'"),
    ("decorou; diz 'as duas' onde vê frase acrescentada", m_diz_as_duas_se_ha_frase_nova, "a memória e 'há frase nova?'"),
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


# ---------------------------------------------------------------------------------------------- o desenho cruzado
def montar_grupos(m, forma):
    """Grupos de 2m afirmacoes tocadas por texto, em duas versoes complementares. forma = 'orig' (linhas reescritas so'
    onde tocadas) ou 'par' (o texto inteiro em outra forma). Devolve (grupos, sobras por texto)."""
    grupos, sobras = [], {}
    for f in FONTES:
        o = ORIG[f]
        base = o if forma == "orig" else outra_forma(o)
        ditos = [a for a in ITENS if a in o["units"]]
        invert = [a for a in ditos if coerente(tocar(o, [a], [], "T", a))]
        k = 0
        while len(invert) - k >= 2 * m:
            g = invert[k:k + 2 * m]
            v1 = tocar(base, g[:m], g[m:], "GRUPO", (forma, tuple(g), 1))
            v2 = tocar(base, g[m:], g[:m], "GRUPO", (forma, tuple(g), 2))
            assert coerente(v1) and coerente(v2), (f, g)
            # o sentido de cada tocada difere entre as duas versoes; o das outras nao muda
            assert all(sentido(v1, a)[0] != sentido(v2, a)[0] for a in g), (f, g)
            outras_mudam = [b for b in ITENS if b not in g and (sentido(v1, b)[0] != sentido(o, b)[0] or sentido(v2, b)[0] != sentido(o, b)[0])]
            grupos.append({"fonte": f, "forma": forma, "tocadas": g, "v1": v1, "v2": v2, "derivadas_que_mudam": outras_mudam})
            k += 2 * m
        sobras[f] = {"afirmacoes": len(ditos), "invertiveis": len(invert), "grupos": k // (2 * m), "sobram": len(invert) - k}
    return grupos, sobras


def montar_grupos_contrarios(m):
    """O mesmo desenho para a frase contraria: em V, as m primeiras afirmacoes ganham a frase contraria e as m ultimas
    uma frase nova que repete o sentido (isca); em V', o contrario."""
    grupos = []
    for f in FONTES:
        o = ORIG[f]
        ditos = [a for a in ITENS if a in o["units"]]
        if len(ditos) >= 2 * m:
            g = ditos[:2 * m]
            v1 = contradizer(o, g[:m], g[m:], "CONTRA", (tuple(g), 1))
            v2 = contradizer(o, g[m:], g[:m], "CONTRA", (tuple(g), 2))
            grupos.append({"fonte": f, "forma": "orig", "tocadas": g, "v1": v1, "v2": v2, "derivadas_que_mudam": []})
    return grupos


def medir(fn, grupos, tol):
    """Por mecanismo: fracao de pares de item certos; fracao de grupos certos (com tolerancia `tol` pares errados por
    grupo); e os controles: itens ditos e NAO tocados das versoes mexidas, silencios, e o texto-base."""
    pares = pares_ok = grupos_ok = so_mudado = so_mudado_ok = 0
    nt = nt_ok = sil = sil_ok = 0
    for g in grupos:
        ok_g = 0
        for a in g["tocadas"]:
            c1 = acerta(g["v1"], a, fn(g["v1"], a))
            c2 = acerta(g["v2"], a, fn(g["v2"], a))
            pares += 1
            pares_ok += (c1 and c2)
            ok_g += (c1 and c2)
            # 'so' o membro mudado': a estatistica do desenho R0, guardada para mostrar por que foi trocada
            inv_em_1 = sentido(g["v1"], a)[0] != sentido(ORIG[g["fonte"]], a)[0]
            so_mudado += 1
            so_mudado_ok += (c1 if inv_em_1 else c2)
        grupos_ok += (ok_g >= len(g["tocadas"]) - tol)
        for v in (g["v1"], g["v2"]):
            for b in ITENS:
                if b in g["tocadas"] or b in g["derivadas_que_mudam"]:
                    continue
                val = sentido(v, b)[0]
                if val == CALA:
                    if MEM_DOUTRINA[b] != CALA:
                        sil += 1
                        sil_ok += acerta(v, b, fn(v, b))
                else:
                    nt += 1
                    nt_ok += acerta(v, b, fn(v, b))
    fr = lambda x, n: (x / n if n else None)
    return {"pares": pares, "pares_certos": fr(pares_ok, pares), "grupos": len(grupos), "grupos_certos": fr(grupos_ok, len(grupos)),
            "so_o_membro_mudado": fr(so_mudado_ok, so_mudado), "nao_tocados_ditos": nt, "nao_tocados_certos": fr(nt_ok, nt),
            "silencios": sil, "silencios_certos": fr(sil_ok, sil)}


def medir_base(fn):
    d = dok = s = sok = 0
    for f in FONTES:
        o = ORIG[f]
        for b in ITENS:
            val = sentido(o, b)[0]
            if val == CALA:
                if MEM_DOUTRINA[b] != CALA:
                    s += 1
                    sok += acerta(o, b, fn(o, b))
            else:
                d += 1
                dok += acerta(o, b, fn(o, b))
    return {"ditos": d, "ditos_certos": dok / d, "silencios": s, "silencios_certos": sok / s}


def main():
    res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "revisao": "R1",
           "nota": "simulacao no nivel da conta; nenhum modelo chamado; separacao por construcao",
           "catalogo": str(CAT), "catalogo_sha256": hashlib.sha256(CAT.read_bytes()).hexdigest(), "semente": SEMENTE, "itens": len(ITENS),
           "mecanismos": [{"nome": n, "pagou": p} for n, _, p in MECANISMOS], "desenhos": {}, "base": {}}
    for nome, fn, _ in MECANISMOS:
        res["base"][nome] = medir_base(fn)
    L = ["# Simulação no nível da conta do desenho R5, revisão R1 (nenhum modelo chamado)", "",
         "> Gerado por `simular_r5.py`. A separação é por construção da conta: mostra que o desenho PODE separar.",
         "> Par de item = a afirmação tocada certa, com a linha, nas DUAS versões complementares do grupo.", ""]
    contr = montar_grupos_contrarios(3)
    for m in (3, 5):
        for forma in ("orig", "par"):
            grupos, sobras = montar_grupos(m, forma)
            chave = "m%d_%s" % (m, forma)
            res["desenhos"][chave] = {"m": m, "forma": forma, "grupos": len(grupos), "por_texto": sobras, "mecanismos": {}}
            for nome, fn, _ in MECANISMOS:
                res["desenhos"][chave]["mecanismos"][nome] = {"tol0": medir(fn, grupos, 0), "tol1": medir(fn, grupos, 1)}
    res["frase_contraria"] = {"m": 3, "grupos": len(contr), "mecanismos": {n: medir(fn, contr, 0) for n, fn, _ in MECANISMOS}}
    # tabela principal: m = 3, forma original com reescritas
    d = res["desenhos"]["m3_orig"]
    L += ["## Desenho cruzado, 6 afirmações tocadas por grupo (3 invertidas e 3 reescritas em cada versão), forma original: %d grupos" % d["grupos"], "",
          "| mecanismo (o que consultou) | texto-base: ditos | texto-base: silêncios | pares certos | só o membro mudado (estatística antiga) | não tocados certos | silêncios certos | frase contrária: pares |",
          "|---|---|---|---|---|---|---|---|"]
    f2 = lambda x: "—" if x is None else ("%.2f" % x).replace(".", ",")
    for nome, _, pagou in MECANISMOS:
        t = d["mecanismos"][nome]["tol0"]; b = res["base"][nome]; c = res["frase_contraria"]["mecanismos"][nome]
        L.append("| %s *(%s)* | %s | %s | %s | %s | %s | %s | %s |" % (nome, pagou, f2(b["ditos_certos"]), f2(b["silencios_certos"]), f2(t["pares_certos"]),
                                                                    f2(t["so_o_membro_mudado"]), f2(t["nao_tocados_certos"]), f2(t["silencios_certos"]), f2(c["pares_certos"])))
    L += ["", "## Quantos grupos o catálogo oferece", "", "| tocadas por grupo | forma | grupos | por texto (afirmações; invertíveis; grupos; sobram) |", "|---|---|---|---|"]
    for chave, dd in res["desenhos"].items():
        pt = "; ".join("%s: %d, %d, %d, %d" % (f, s["afirmacoes"], s["invertiveis"], s["grupos"], s["sobram"]) for f, s in dd["por_texto"].items())
        L.append("| %d | %s | %d | %s |" % (2 * dd["m"], "original com reescritas" if dd["forma"] == "orig" else "outra forma inteira", dd["grupos"], pt))
    L += ["", "## Pares certos nos quatro desenhos (todos os mecanismos)", "", "| mecanismo | 6 tocadas, original | 6 tocadas, outra forma | 10 tocadas, original | 10 tocadas, outra forma |", "|---|---|---|---|---|"]
    for nome, _, _ in MECANISMOS:
        L.append("| %s | %s |" % (nome, " | ".join(f2(res["desenhos"][k]["mecanismos"][nome]["tol0"]["pares_certos"]) for k in ("m3_orig", "m3_par", "m5_orig", "m5_par"))))
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "RESULTADO_SIMULACAO_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    (SAIDA / "RESULTADO_SIMULACAO_R5.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

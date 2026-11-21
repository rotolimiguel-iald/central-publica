# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\registros_v412_r7.py (que fica intacto), para os CINCO registros do contrato da v413.
"""registros_v413.py -- os CINCO registros da v413, por especificacao (o motor e' o da v392: _v392_registro; nenhum com funcao nova). Modulo de CADEIA: devolve a lista de specs (dados) que o gerador embute.
Cada registro diz tres coisas, nesta ordem: (1) o que o artefato mostra (so' o que tem ancora); (2) as leis e definicoes da teoria que ele usa como ENTRADA ([INPUT] ou [ONTO]; nunca como teorema); (3) o que continua aberto.
O texto sai da pagina publica e dos cabecalhos das pedras, sem acrescentar afirmacao: as linhas do que o artefato mostra sao tiradas da pagina POR SCRIPT (a tabela da secao 2; as listas das secoes 3, 4 e 5), e cada trecho
fixo de textos_registros_v413.py e' conferido contra a pagina desembrulhada. As palavras de veredito sao copiadas do CONTRATO por script (nao redigitadas); os numeros do core sao lidos do core selado da base (v412).
Cada termo citado numa linha tem de ser ancora de um modulo do registro (na tabela: da propria linha), ou declaracao do kernel selado, dita a parte. Nada daqui traz historia de conversa."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

D = L.D
CONTRATO_TXT = L.CONTRATO_TXT
ANC = L.ler_json(L.saida("ANCORAS_ESCOLHIDAS_v413.json"))
TIT = L.ler_json(D / "TITULOS_DOS_CABECALHOS_v413.json")["modulos"]
MAN = L.ler_json(L.MANIFESTO)
N_MODULOS = len(MAN["modulos_novos"])
assert ANC["sha16_das_fontes"]["manifesto"] == L.sha16_arq(L.MANIFESTO) and ANC["sha16_das_fontes"]["pagina"] == L.sha16_arq(L.PAGINA), "as ancoras escolhidas nao sao as do manifesto e da pagina vigentes: rode e7_11_ancoras_escolhidas_v413.py"
CORE0 = L.ler_json(D / "base_v412" / "um_absoluto.json")["core"]
GATE_V412 = CORE0["qg_closure"]["gate"]["verdict"]
NEUTRINO_V412 = CORE0["neutrino_mass"]["verdict"]
H0DN_V412 = CORE0["h0dn_bg1_v411"]["verdict"]
ESCADA_V412 = int(CORE0["external_ladder"]["n_theorems_expected"])
AUD_NOMES = None
NOMES = ["ponte_cook_levin_v413", "trinity_v413", "operador_v413", "identidade_preservada_v413", "kh_n1_cobertura_v413", "cunhagens_v413"]   # (contrato R2: o kh_n1_cobertura_v413, que a custodia exige, antes do cunhagens)
NOMES_DO_CONTRATO = [n for n in NOMES if n != L.KH_REGISTRO_V413]
ID_DO_SELO = {"ponte_cook_levin_v413": "selo_ponte", "trinity_v413": "selo_trinity", "operador_v413": "selo_operador", "identidade_preservada_v413": "selo_identidade"}


def palavras_do_contrato():
    out = {}
    for nome in NOMES_DO_CONTRATO:
        m = re.findall(r"^- `%s`[^\n]*\n  `([A-Z0-9_]+)`" % nome, CONTRATO_TXT, re.M)
        assert len(m) == 1, ("palavra de veredito nao achada (ou repetida) no contrato", nome, len(m))
        out[nome] = m[0]
    pre_, suf_ = L.palavra_kh_v413()   # (o kh: o contrato R2 pede o registro; a palavra segue o molde do kh da v411, com os numeros do recibo KH_N1)
    out[L.KH_REGISTRO_V413] = pre_ + "__" + suf_
    return out


PALAVRAS = palavras_do_contrato()


def prefixo_sufixo(nome):
    w = PALAVRAS[nome]
    pre, suf = w.split("__", 1)
    assert pre + "__" + suf == w and w.endswith("GATE_UNMOVED")
    return pre, suf


# ---------------------------------------------------------------- a pagina, desembrulhada (as quebras de linha da fonte markdown juntadas: o paragrafo, o bloco de citacao e o item de lista viram UMA linha)
def desembrulhar(md):
    linhas = md.replace("\r\n", "\n").split("\n")
    out, cur = [], None

    def fecha():
        nonlocal cur
        if cur is not None:
            out.append(cur)
            cur = None
    for l in linhas:
        if not l.strip():
            fecha(); out.append(""); continue
        if l.startswith("|") or l.startswith("#"):
            fecha(); out.append(l.rstrip()); continue
        if l.startswith("> "):
            if cur is not None and cur.startswith("> "):
                cur += " " + l[2:].strip()
            else:
                fecha(); cur = l.rstrip()
            continue
        if re.match(r"^(?:- |\d+\. )", l):
            fecha(); cur = l.rstrip(); continue
        if l.startswith("  ") and cur is not None and (cur.startswith("- ") or re.match(r"^\d+\. ", cur)):
            cur += " " + l.strip(); continue
        if cur is not None and not cur.startswith("> ") and not cur.startswith("- ") and not re.match(r"^\d+\. ", cur):
            cur += " " + l.strip(); continue
        fecha(); cur = l.rstrip()
    fecha()
    t = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", t)


import ajustes_revisao_v413 as AJR   # noqa: E402   (os ajustes minimos da revisao de terceiro do candidato: a pagina lida com eles, por script)
PAGINA_TXT = AJR.aplicar(L.PAGINA.read_bytes().decode("utf-8").replace("\r\n", "\n"), "pt")
PAG_D = desembrulhar(PAGINA_TXT)
AJUSTES = []   # os itens de registro reescritos pela revisao de terceiro (achado, trechos da pagina de que partem, texto que entra), para o recibo


def secao(n):
    m = re.search(r"(^## %d\. .*?)(?=^## %d\. |\Z)" % (n, n + 1), PAG_D, re.S | re.M)
    assert m, ("secao da pagina nao achada", n)
    return m.group(1).rstrip()


def sem_marcacao(s):
    return re.sub(r"`([^`]+)`", r"\1", s.replace("**", ""))


def confere(trecho):
    assert sem_marcacao(trecho) in sem_marcacao(PAG_D), ("trecho de textos_registros_v413.py que nao esta' na pagina", trecho[:120])
    return trecho


def linha(t):
    marca, *trechos = t
    partes = []
    for x in trechos:
        if isinstance(x, AJR.AJ):   # item reescrito pela revisao: cada trecho de base esta' na pagina; o texto que entra fica no recibo, com o achado
            for b in x.base:
                confere(b)
            r_ = {"achado": x.achado, "trechos_da_pagina": list(x.base), "texto": str(x)}
            if r_ not in AJUSTES:
                AJUSTES.append(r_)
            partes.append(sem_marcacao(str(x)))
        else:
            partes.append(sem_marcacao(confere(x)))
    return marca + "; ".join(partes)


def checks_herdadas(prefixo_id, nome_registro):
    """as checagens que todo registro traz (molde da v412): gate, canais vivos, nenhuma chave antiga muda de literal, a escada so' cresce, proveniencia, e a guarda de frases (a herdada da v412, pela travessia) sobre o corpo e a palavra de veredito"""
    c = []

    def add(desc, caminho, op, valor=None, onde="core"):
        d = {"id": "%s%d" % (prefixo_id, len(c) + 1), "descricao": desc, "onde": onde, "caminho": caminho, "op": op, "estatuto": "[REAL]"}
        if valor is not None:
            d["valor"] = valor
        c.append(d)
    add("o gate deste rito tem o mesmo veredito do gate da base", ["qg_closure", "gate", "verdict"], "igual", GATE_V412)
    add("o canal vivo do neutrino segue com o mesmo veredito", ["neutrino_mass", "verdict"], "igual", NEUTRINO_V412)
    add("o canal vivo do teste da razao de Hubble (H0DN) segue com o mesmo veredito", ["h0dn_bg1_v411", "verdict"], "igual", H0DN_V412)
    add("o registro do teste da razao de Hubble segue selado neste rito", ["h0dn_bg1_v411", "all_verified"], "verdadeiro")
    add("nenhuma chave antiga muda de literal: toda bandeira da escada segue verdadeira e a escada fecha", ["external_ladder", "all_verified"], "verdadeiro")
    add("a escada so' cresce: o numero esperado de teoremas e' maior ou igual ao da base", ["external_ladder", "n_theorems_expected"], "maior_igual", ESCADA_V412)
    add("a proveniencia emitida pelo compilador cobre o axiom_report", ["declaration_sources_status_v394", "ok"], "verdadeiro", None, "kf")
    add("a guarda de frases herdada da v412 (a travessia) sobre o corpo inteiro e a palavra de veredito deste registro: zero violacao", ["guarda_frases_v413", nome_registro, "n_violacoes"], "igual", 0)
    add("a travessia examinou mais de zero unidades deste registro", ["guarda_frases_v413", nome_registro, "n_unidades_examinadas"], "maior_igual", 1)
    return c


def checks_das_ancoras(modulos, prefixo_id):
    """cada ancora e' uma checagem: a bandeira e' verdadeira (uma checagem) e a declaracao esta no relatorio de axiomas (outra); o trio de cada declaracao e' conferido pelo motor (kernel_decls)"""
    c, flags, decls = [], [], []
    k = 0
    for mod, d in modulos.items():
        for a in d["ancoras"]:
            k += 1
            flags.append(a["bandeira"]); decls.append(a["nome"])
            c.append({"id": "%sb%04d" % (prefixo_id, k), "descricao": "ancora %s (%s): a bandeira e' verdadeira" % (a["nome"], mod), "onde": "kf", "caminho": [a["bandeira"]], "op": "verdadeiro", "estatuto": "[REAL]"})
            c.append({"id": "%sd%04d" % (prefixo_id, k), "descricao": "ancora %s (%s): a declaracao esta no relatorio de axiomas (so' com os tres axiomas, conferido pelo motor)" % (a["nome"], mod), "onde": "kf", "caminho": ["axiom_report", a["nome"]], "op": "existe", "estatuto": "[REAL]"})
    assert len(set(flags)) == len(flags) and len(set(decls)) == len(decls), "ancora repetida"
    return c, flags, decls


def spec_base(nome, estatuto, diz, limites, nao_diz, extras, checks, flags, decls):
    pre, suf = prefixo_sufixo(nome)
    return {"nome": nome, "veredito_prefixo": pre, "veredito_sufixo": suf, "estatuto": estatuto, "fontes": [], "verbatins": [], "kernel_flags": flags, "kernel_decls": decls, "checks": checks,
            "erratas": [], "limites": limites, "diz": diz, "nao_diz": nao_diz, "leituras_do_operador": [], "extras": extras}


def nomes_selados():
    """os nomes do relatorio de axiomas do build do sandbox (o kernel inteiro: o selado e os novos)"""
    global AUD_NOMES
    if AUD_NOMES is None:
        aud = (L.KD / "audit.log").read_bytes().decode("utf-8", "replace")
        AUD_NOMES = set(re.findall(r"^TGL_DECL_SOURCE\t(\S+)\t", aud, re.M))
    return AUD_NOMES


def casa(nome_completo, citado):
    return nome_completo == citado or nome_completo.endswith("." + citado)


def termos_conferidos(texto, modulos, anc_reg, onde):
    """cada termo entre crases do texto e' ancora de um dos modulos dados, ou nome de modulo da lista, ou declaracao do kernel (dita a parte); senao a montagem PARA"""
    ancoras = [a["nome"] for m in modulos for a in anc_reg[m]["ancoras"]]
    usados, selados = [], []
    for t in re.findall(r"`([^`]+)`", texto):
        if t in MAN_MODULOS_CURTOS:
            continue
        ach = [n for n in ancoras if casa(n, t)]
        if ach:
            usados += ach; continue
        sel = sorted(n for n in nomes_selados() if casa(n, t))
        assert sel, ("termo citado na pagina que nao e' ancora do registro nem declaracao do kernel", onde, t)
        selados.append({"termo": t, "declaracoes_do_kernel": sel[:3]})
    return sorted(set(usados)), selados


MAN_MODULOS_CURTOS = {m.split(".")[-1] for m in MAN["modulos_novos"]}


def tabela_secao_2():
    s = secao(2)
    linhas = s.split("\n")
    i0 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\|\s*frase\s*\|\s*termo\s*\|\s*onde\s*\|", l.strip())]
    assert len(i0) == 1
    out = []
    i = i0[0] + 2
    while i < len(linhas) and linhas[i].startswith("|"):
        cel = [c.strip() for c in re.split(r" \| ", linhas[i].strip()[1:-1].strip())]
        assert len(cel) == 3
        out.append(tuple(cel)); i += 1
    return out


def itens(n, depois_de=None):
    """os itens de lista ('- ') da secao n da pagina desembrulhada (opcionalmente so' os que vem depois de uma linha que comeca por `depois_de`)"""
    s = secao(n)
    if depois_de:
        k = s.index(depois_de)
        s = s[k:]
    return [l[2:].strip() for l in s.split("\n") if l.startswith("- ")]


def especs():
    import textos_registros_v413 as TX
    specs = {}
    R = ANC["registros"]
    nd_comum = [linha(x) for x in TX.ND_COMUM]
    # ---------------------------------------------------------------- ponte_cook_levin_v413 (17 modulos)
    rp = R["ponte_cook_levin_v413"]["modulos"]
    ck, fl, dc = checks_das_ancoras(rp, "a")
    diz, linhas_tab, selados_tab = [linha(x) for x in TX.DIZ_P_ABERTURA], [], []
    for frase, termo, onde in tabela_secao_2():
        mods = [m for m in re.findall(r"`([^`]+)`", onde)]
        assert mods and all(m in rp for m in mods), ("linha da tabela com modulo que nao e' deste registro", frase, mods)
        usados, selados = termos_conferidos(frase + " " + termo, mods, rp, "tabela: " + frase)
        todas_do_registro = [a["nome"] for d_ in rp.values() for a in d_["ancoras"]]
        for s_ in selados:
            # um termo que nao e' ancora de modulo da linha: ou e' ancora de outro modulo DESTE registro (citado de novo), ou declaracao do kernel selado (nao e' ancora desta versao)
            s_["ancora_de_outro_modulo_deste_registro"] = sorted(n for n in todas_do_registro if casa(n, s_["termo"]))
            s_["do_kernel_selado"] = not s_["ancora_de_outro_modulo_deste_registro"]
        selados_tab += [dict(s_, linha=sem_marcacao(frase)) for s_ in selados]
        diz.append("[REAL] %s: %s (%s)" % (sem_marcacao(frase), sem_marcacao(termo), ", ".join(mods)))
        linhas_tab.append({"frase": sem_marcacao(frase), "modulos": mods, "ancoras": usados})
    diz += [linha(x) for x in TX.DIZ_P_FECHO]
    ext = {"n_ancoras": sum(m["n_ancoras"] for m in rp.values()), "n_modulos": len(rp), "modulos": list(rp), "n_ancoras_por_modulo": {m: len(d["ancoras"]) for m, d in rp.items()},
           "modulos_sem_ancora": [m for m, d in rp.items() if not d["ancoras"]],
           "linhas_da_tabela_da_pagina": linhas_tab, "termos_citados_que_nao_sao_ancora_de_modulo_da_linha": selados_tab, "leis_e_definicoes_da_teoria": []}
    specs["ponte_cook_levin_v413"] = spec_base("ponte_cook_levin_v413", TX.ESTATUTO_P % (N_MODULOS, len(rp), ext["n_ancoras"]), diz, [linha(x) for x in TX.LIM_P + TX.LIM_COMUM], [linha(x) for x in TX.ND_P] + nd_comum, ext,
                                               checks_herdadas("h", "ponte_cook_levin_v413") + ck, fl, dc)
    # ---------------------------------------------------------------- trinity_v413 (2 modulos)
    rt = R["trinity_v413"]["modulos"]
    ck, fl, dc = checks_das_ancoras(rt, "a")
    it3 = itens(3, "O que o kernel prova")
    assert len(it3) >= 5, len(it3)
    usados_t = []
    for x in it3:
        u, s = termos_conferidos(x, list(rt), rt, "secao 3")
        assert not s, ("na secao 3, termo que nao e' ancora da fronteira", s)
        usados_t += u
    ext = {"n_ancoras": sum(m["n_ancoras"] for m in rt.values()), "n_modulos": len(rt), "modulos": list(rt), "n_ancoras_por_modulo": {m: len(d["ancoras"]) for m, d in rt.items()},
           "ancoras_citadas_pela_pagina": sorted(set(usados_t)), "leis_e_definicoes_da_teoria": [linha(x) for x in TX.LEIS_T]}
    specs["trinity_v413"] = spec_base("trinity_v413", TX.ESTATUTO_T % (N_MODULOS, len(rt), ext["n_ancoras"]), ["[REAL] " + sem_marcacao(x) for x in it3], [linha(x) for x in TX.LIM_T + TX.LIM_COMUM], [linha(x) for x in TX.ND_T] + nd_comum,
                                      ext, checks_herdadas("h", "trinity_v413") + ck, fl, dc)
    # ---------------------------------------------------------------- operador_v413 (1 modulo)
    ro = R["operador_v413"]["modulos"]
    ck, fl, dc = checks_das_ancoras(ro, "a")
    it4 = itens(4, "O que o kernel prova")
    assert len(it4) >= 5, len(it4)
    usados_o = []
    for x in it4:
        u, s = termos_conferidos(x, list(ro), ro, "secao 4")
        assert not s, ("na secao 4, termo que nao e' ancora do operador", s)
        usados_o += u
    ext = {"n_ancoras": sum(m["n_ancoras"] for m in ro.values()), "n_modulos": len(ro), "modulos": list(ro), "n_ancoras_por_modulo": {m: len(d["ancoras"]) for m, d in ro.items()},
           "ancoras_citadas_pela_pagina": sorted(set(usados_o)), "leis_e_definicoes_da_teoria": [linha(x) for x in TX.LEIS_O]}
    specs["operador_v413"] = spec_base("operador_v413", TX.ESTATUTO_O % (N_MODULOS, len(ro), ext["n_ancoras"]), ["[REAL] " + sem_marcacao(x) for x in it4], [linha(x) for x in TX.LIM_O + TX.LIM_COMUM], [linha(x) for x in TX.ND_O] + nd_comum,
                                       ext, checks_herdadas("h", "operador_v413") + ck, fl, dc)
    # ---------------------------------------------------------------- identidade_preservada_v413 (1 modulo)
    ri = R["identidade_preservada_v413"]["modulos"]
    ck, fl, dc = checks_das_ancoras(ri, "a")
    s5 = secao(5)
    m5 = re.search(r"O que o kernel prova: (.*?\))\. ", s5)
    assert m5, "a frase do que o kernel prova na secao 5 nao foi achada"
    it5 = [re.sub(r"^e, ", "", x.strip()) for x in m5.group(1).split("; ")]
    assert len(it5) == 4, it5
    usados_i = []
    for x in it5:
        u, s = termos_conferidos(x, list(ri), ri, "secao 5")
        assert not s and u, ("na secao 5, termo que nao e' ancora da identidade preservada", x[:80], s)
        usados_i += u
    ext = {"n_ancoras": sum(m["n_ancoras"] for m in ri.values()), "n_modulos": len(ri), "modulos": list(ri), "n_ancoras_por_modulo": {m: len(d["ancoras"]) for m, d in ri.items()},
           "ancoras_citadas_pela_pagina": sorted(set(usados_i)), "leis_e_definicoes_da_teoria": [linha(x) for x in TX.LEIS_I]}
    specs["identidade_preservada_v413"] = spec_base("identidade_preservada_v413", TX.ESTATUTO_I % (N_MODULOS, len(ri), ext["n_ancoras"]), ["[REAL] " + sem_marcacao(x) for x in it5], [linha(x) for x in TX.LIM_I + TX.LIM_COMUM],
                                                    [linha(x) for x in TX.ND_I] + nd_comum, ext, checks_herdadas("h", "identidade_preservada_v413") + ck, fl, dc)
    assert len(rp) + len(rt) + len(ro) + len(ri) == N_MODULOS, ("os modulos dos quatro registros com ancora nao somam o manifesto", len(rp), len(rt), len(ro), len(ri), N_MODULOS)
    # ---------------------------------------------------------------- kh_n1_cobertura_v413 (contrato R2, secao 2): no molde do kh_n1_cobertura_v411 do programa; os numeros do recibo kernel\KH_N1_v413.json da Etapa 1
    kh = L.ler_json(L.KH_N1_V413); lt = kh["linha_TOTAL"]; lt12 = kh["linha_TOTAL_v412"]
    cm12 = L.ler_json(L.V412 / "CANDIDATO_v412.json"); res11 = L.ler_json(D.parent / "v411" / "CANDIDATO_v411.json")["h8"]["residuais_do_nos"]
    h8 = int(cm12["formal_files_n"]) + N_MODULOS + len(res11)   # as fontes formais da arvore do Nos depois do rito: as embutidas da v412, mais os modulos novos (o corrigido SUBSTITUI um que ja' existe), mais os residuais pinados
    ck_k = checks_herdadas("h", L.KH_REGISTRO_V413)

    def kadd(i_, desc, onde, caminho, op, valor=None, capturar=None):
        d_ = {"id": i_, "descricao": desc, "onde": onde, "caminho": caminho, "op": op, "estatuto": "[REAL]"}
        if valor is not None:
            d_["valor"] = valor
        if capturar:
            d_["capturar"] = capturar
        ck_k.append(d_)
    kadd("k1", "a checagem de cobertura do kernel do rito passou", "kf", ["axiom_coverage_v392", "ok"], "verdadeiro")
    kadd("k2", "constantes cobertas == as do sandbox desta versao (recibo KH_N1)", "kf", ["axiom_coverage_v392", "decl"], "igual", lt["decl"], "constantes_cobertas")
    kadd("k3", "teoremas cobertos == os do sandbox desta versao (recibo KH_N1)", "kf", ["axiom_coverage_v392", "thm"], "igual", lt["thm"], "teoremas_cobertos")
    kadd("k4", "nenhuma constante fora do trio", "kf", ["axiom_coverage_v392", "fora_do_trio"], "igual", 0)
    kadd("k5", "nenhum nome que o leitor v394 nao leia", "kf", ["axiom_coverage_v392", "nao_lidas_pelo_regex"], "igual", 0)
    kadd("k6", "o axiom_report do rito tem exatamente uma entrada por constante coberta", "kf", ["axiom_report"], "tamanho_igual", lt["decl"])
    kadd("k7", "a cobertura desta versao inclui a da base selada (constantes)", "kf", ["axiom_coverage_v392", "decl"], "maior_igual", lt12["decl"])
    kadd("k7b", "os teoremas cobertos incluem os da base selada", "kf", ["axiom_coverage_v392", "thm"], "maior_igual", lt12["thm"])
    kadd("k8", "as fontes formais da arvore do Nos depois do rito (as embutidas + os residuais que o hash formal conta) sao em numero exatamente as esperadas", "kf", ["formal_files_sha256"], "tamanho_igual", h8)
    kadd("k9", "medida do Audit desta versao: duracao bem abaixo do timeout de 1800 s", "fonte:kh_n1_v413", ["duracao_audit_s"], "menor_igual", 1200, "duracao_do_audit_s")
    kadd("k10", "medida do Audit desta versao: sorryAx ausente do log", "fonte:kh_n1_v413", ["sorryAx_no_log_do_audit"], "igual", 0)
    kadd("k11", "medida do Audit desta versao: as entradas novas estao no trio", "fonte:kh_n1_v413", ["novas_no_trio"], "verdadeiro")
    ext_k = {"delta_vs_v412": kh["delta_vs_v412"], "n_bandeiras": kh["n_bandeiras"], "n_modulos": kh["n_modulos_novos"], "duracao_build_s_sandbox": kh["duracao_build_s"], "duracao_audit_s_sandbox": kh["duracao_audit_s"],
             "entradas_do_hash_formal_esperadas": h8, "recibo": "kernel/KH_N1_v413.json"}
    sk = spec_base(L.KH_REGISTRO_V413, TX.ESTATUTO_K, [TX.DIZ_K], [TX.LIM_K] + [linha(x) for x in TX.LIM_COMUM], list(TX.ND_K) + nd_comum, ext_k, ck_k, [], [])
    sk["fontes"] = ["kh_n1_v413"]
    specs[L.KH_REGISTRO_V413] = sk
    # ---------------------------------------------------------------- cunhagens_v413 (as leis e definicoes da teoria que entram como ENTRADA)
    entradas = entradas_definicoes()
    ck_c = checks_herdadas("h", "cunhagens_v413")
    for nm in [n_ for n_ in NOMES[:-1] if n_ in ID_DO_SELO]:
        ck_c.append({"id": ID_DO_SELO[nm], "descricao": "o registro %s sela neste rito" % nm, "onde": "core", "caminho": [nm, "all_verified"], "op": "verdadeiro", "estatuto": "[REAL]"})
    flags_c, decls_c = [], []
    k = 0
    for e in entradas:
        for a in e["ancoras"]:
            k += 1
            ck_c.append({"id": "ce%03d" % k, "descricao": "ancora que tipa '%s': %s (a bandeira e' verdadeira)" % (e["nome"], a["nome"]), "onde": "kf", "caminho": [a["bandeira"]], "op": "verdadeiro", "estatuto": "[REAL]"})
            flags_c.append(a["bandeira"]); decls_c.append(a["nome"])
    flags_c = list(dict.fromkeys(flags_c)); decls_c = list(dict.fromkeys(decls_c))
    ext_c = {"n_entradas": len(entradas), "entradas": entradas,
             "leis_e_definicoes_da_pagina_publica": [linha(x) for x in TX.LEIS_T] + [linha(x) for x in TX.LEIS_O] + [linha(x) for x in TX.LEIS_I]}
    specs["cunhagens_v413"] = spec_base("cunhagens_v413", TX.ESTATUTO_C, list(TX.DIZ_C), list(TX.LIM_C), list(TX.ND_C), ext_c, ck_c, flags_c, decls_c)
    lista = [specs[n] for n in NOMES]
    for s in lista:
        cid = [c["id"] for c in s["checks"]]
        assert len(cid) == len(set(cid)), ("id de checagem repetido", s["nome"])
        assert not any(re.fullmatch(r"[rR]\d+", i) for i in cid), ("id de checagem com forma de numero de revisao", s["nome"])
        assert all(c["op"] in ("igual", "verdadeiro", "falso", "existe", "maior_igual", "tamanho_igual", "menor_igual") for c in s["checks"])
        assert not s["fontes"] or (s["nome"] == L.KH_REGISTRO_V413 and s["fontes"] == ["kh_n1_v413"]), ("fonte num registro que nao e' o kh", s["nome"])
        corpo = json.dumps({k_: s[k_] for k_ in ("limites", "diz", "nao_diz", "extras", "estatuto")}, ensure_ascii=False)
        for u in re.findall(r"[^\"]*P\s*=\s*nP[^\"]*", corpo):
            assert "classes do seu dicionário" in u and re.search(r"máquina de fita[^.;]*não está demonstrad", u), ("unidade com a expressao do dicionario sem as duas marcas", s["nome"], u[:160])
    return lista


def entradas_definicoes():
    import textos_registros_v413 as TX
    todos = {}
    for reg in ANC["registros"].values():
        todos.update(reg["modulos"])
    out = []
    for mod, lst in TX.ENTRADAS_C.items():
        t = (L.PEDRAS / (mod + ".lean")).read_bytes().decode("utf-8")
        h = re.search(r"/-!(.*?)-/", t, re.S).group(1)
        nao = re.search(r"(?m)^#{2,3} (O que .*N[ÃA]O .*)$", h)
        corpo_nao = ""
        if nao:
            i0 = h.index(nao.group(0)); resto = h[i0 + len(nao.group(0)):]
            j = re.search(r"(?m)^#{2,3} ", resto)
            corpo_nao = resto[:j.start()] if j else resto
        n_itens_nao = len(re.findall(r"(?m)^\s*\* ", corpo_nao))
        for nome, est, rx in lst:
            m = re.search(rx, h, re.M)
            assert m, ("secao da leitura nao achada no cabecalho", mod, rx)
            resto = h[m.end():]
            j = re.search(r"(?m)^## ", resto)
            sec = resto[:j.start()] if j else resto
            citados = [c_ for c_ in re.findall(r"`([^`]+)`", sec) if len(c_) > 1]   # (revisao B4) um nome de uma letra entre crases (um vetor `v`) nao e' citacao de declaracao
            anc_sec = [a for a in todos[mod]["ancoras"] if any(casa(a["nome"], c) for c in citados)]
            outras = [a for mm, v in todos.items() if mm != mod for a in v["ancoras"] if any(casa(a["nome"], c) for c in citados)]
            via = "citadas na secao do cabecalho"
            anc = anc_sec + outras
            if not anc:
                anc = [a for a in todos[mod]["ancoras"] if "estrela" in a["regras"]] or todos[mod]["ancoras"]
                via = "as ancoras com estrela do modulo (a secao da leitura nao cita declaracao)"
            selados = sorted({c for c in citados if not any(casa(a["nome"], c) for a in anc) and any(casa(n, c) for n in nomes_selados())})
            out.append({"nome": nome, "estatuto_de_entrada": est, "modulo": mod, "titulo_da_secao_do_cabecalho": m.group(0).lstrip("#").strip(), "ancoras": [{"nome": a["nome"], "bandeira": a["bandeira"]} for a in anc],
                        "via_das_ancoras": via, "declaracoes_do_kernel_selado_citadas_na_secao": selados,
                        "nao_tipado": {"secao_do_cabecalho": nao.group(1).strip() if nao else None, "n_itens": n_itens_nao}})
    assert len({e["nome"] for e in out}) == len(out), len(out)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    s = especs()
    for sp in s:
        print(sp["nome"], "| prefixo:", sp["veredito_prefixo"], "|", len(sp["checks"]), "checks |", len(sp["kernel_flags"]), "flags |", len(sp["kernel_decls"]), "decls |", len(sp["diz"]), "diz |", len(sp["limites"]), "limites |",
              len(sp["nao_diz"]), "nao_diz")

# -*- coding: utf-8 -*-
"""registros_v412.py -- os QUATRO registros da v412, por especificacao (o motor e' o da v392: _v392_registro; nenhum com funcao nova). Modulo de CADEIA: devolve a lista de specs (dados) que o gerador embute.
Cada registro diz tres coisas, nesta ordem: (1) o que o artefato mostra (so' o que tem ancora); (2) as leis e definicoes da teoria que ele usa como ENTRADA ([INPUT] ou [ONTO]; nunca como teorema); (3) o que continua aberto.
O texto sai da pagina publica (O_QUE_FICA_CLARO_v412_R9.md) e dos cabecalhos das pedras congeladas; as palavras de veredito sao copiadas do CONTRATO por script (nao redigitadas); os numeros do kernel/core
sao lidos do core selado da base e do recibo do kernel, nunca digitados. Nada daqui traz historia de conversa: nenhuma fala, data de conversa, nome de pessoa/modelo, numero de ordem/revisao/parecer."""
import json, re, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, ler_json, sha16_arq

CONTRATO = D / "CONTRATO_v412_R4.md"
ANC = ler_json(D / "ANCORAS_ESCOLHIDAS_v412.json")
TIT = ler_json(D / "TITULOS_DOS_CABECALHOS_v412.json")["modulos"]
CORE0 = ler_json(D / "base_v411" / "um_absoluto.json")["core"]
PAGINA = (D / "o_que_fica_claro_REV9" / "O_QUE_FICA_CLARO_v412_R9.md").read_bytes().decode("utf-8")
GATE_V411 = CORE0["qg_closure"]["gate"]["verdict"]
NEUTRINO_V411 = CORE0["neutrino_mass"]["verdict"]
H0DN_V411 = CORE0["h0dn_bg1_v411"]["verdict"]
ESCADA_V411 = int(CORE0["external_ladder"]["n_theorems_expected"])
N_RESSALVAS = len(CORE0["h0dn_bg1_v411"]["values"]["ressalvas_secao8"])
N_NAO_DECIDE = len(CORE0["h0dn_bg1_v411"]["o_que_o_teste_nao_decide"])
NOMES = ["iald_camada_cientifica_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]


def palavras_do_contrato():
    t = CONTRATO.read_bytes().decode("utf-8").replace("\r\n", "\n")
    out = {}
    for nome in NOMES:
        m = re.search(r"^- `%s`\n  `([A-Z0-9_]+)`" % nome, t, re.M)
        assert m, ("palavra de veredito nao achada no contrato", nome)
        out[nome] = m.group(1)
    return out


PALAVRAS = palavras_do_contrato()


def prefixo_sufixo(nome):
    w = PALAVRAS[nome]
    pre, suf = w.split("__", 1)
    assert pre + "__" + suf == w and w.endswith("GATE_UNMOVED")
    return pre, suf


def checks_herdadas(prefixo_id, nome_registro):
    """as checagens que todo registro traz: gate, canais vivos, nenhuma chave antiga muda de literal, a escada so' cresce, proveniencia"""
    c = []

    def add(desc, caminho, op, valor=None, onde="core"):
        d = {"id": "%s%d" % (prefixo_id, len(c) + 1), "descricao": desc, "onde": onde, "caminho": caminho, "op": op, "estatuto": "[REAL]"}
        if valor is not None:
            d["valor"] = valor
        c.append(d)
    add("o gate deste rito tem o mesmo veredito do gate da base", ["qg_closure", "gate", "verdict"], "igual", GATE_V411)
    add("o canal vivo do neutrino segue com o mesmo veredito", ["neutrino_mass", "verdict"], "igual", NEUTRINO_V411)
    add("o canal vivo do teste da razao de Hubble (H0DN) segue com o mesmo veredito", ["h0dn_bg1_v411", "verdict"], "igual", H0DN_V411)
    add("o registro do teste da razao de Hubble segue selado neste rito", ["h0dn_bg1_v411", "all_verified"], "verdadeiro")
    add("nenhuma chave antiga muda de literal: toda bandeira da escada segue verdadeira e a escada fecha", ["external_ladder", "all_verified"], "verdadeiro")
    add("a escada so' cresce: o numero esperado de teoremas e' maior ou igual ao da base", ["external_ladder", "n_theorems_expected"], "maior_igual", ESCADA_V411)
    add("a proveniencia emitida pelo compilador cobre o axiom_report", ["declaration_sources_status_v394", "ok"], "verdadeiro", None, "kf")
    add("a guarda de frases da v412 (a travessia) sobre o corpo inteiro e a palavra de veredito deste registro: zero violacao", ["guarda_frases_v412", nome_registro, "n_violacoes"], "igual", 0)
    add("a travessia examinou mais de zero unidades deste registro", ["guarda_frases_v412", nome_registro, "n_unidades_examinadas"], "maior_igual", 1)
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



def especs():
    import textos_registros_v412 as TX
    specs = []
    # ---------------------------------------------------------------- iald_camada_cientifica_v412 (frente A)
    ra = ANC["registros"]["iald_camada_cientifica_v412"]["modulos"]
    ck_a, fl_a, dc_a = checks_das_ancoras(ra, "a")
    ext_a = {"n_ancoras": sum(m["n_ancoras"] for m in ra.values()), "n_modulos": len(ra), "modulos": list(ra), "ancoras_por_modulo": {m: [a["nome"] for a in d["ancoras"]] for m, d in ra.items()},
             "titulos_dos_cabecalhos": {m: TIT[m]["titulo"] for m in ra if TIT[m]["titulo"]}, "leis_e_definicoes_da_teoria": list(TX.LEIS_A)}
    specs.append(spec_base("iald_camada_cientifica_v412", TX.ESTATUTO_A % ext_a["n_ancoras"], list(TX.DIZ_A), list(TX.LIM_A), list(TX.ND_A), ext_a, checks_herdadas("h", "iald_camada_cientifica_v412") + ck_a, fl_a, dc_a))
    # ---------------------------------------------------------------- matematica_que_restava_v412 (frente B)
    rb = ANC["registros"]["matematica_que_restava_v412"]["modulos"]
    ck_b, fl_b, dc_b = checks_das_ancoras(rb, "a")
    ext_b = {"n_ancoras": sum(m["n_ancoras"] for m in rb.values()), "n_modulos": len(rb), "modulos": list(rb), "ancoras_por_modulo": {m: [a["nome"] for a in d["ancoras"]] for m, d in rb.items()},
             "titulos_dos_cabecalhos": {m: TIT[m]["titulo"] for m in rb if TIT[m]["titulo"]}, "modulos_sem_cabecalho": [m for m in rb if not TIT[m]["tem_cabecalho"]], "leis_e_definicoes_da_teoria": list(TX.LEIS_B)}
    specs.append(spec_base("matematica_que_restava_v412", TX.ESTATUTO_B % ext_b["n_ancoras"], list(TX.DIZ_B), list(TX.LIM_B), list(TX.ND_B), ext_b, checks_herdadas("h", "matematica_que_restava_v412") + ck_b, fl_b, dc_b))
    # ---------------------------------------------------------------- parede_do_teste_cego_v412 (sem modulo)
    assert len(TX.RESSALVAS) == N_RESSALVAS, "as ressalvas do registro nao sao as do core selado"
    ck_p = checks_herdadas("h", "parede_do_teste_cego_v412")
    ck_p.append({"id": "p1", "descricao": "o core selado do teste da razao de Hubble traz as ressalvas", "onde": "core", "caminho": ["h0dn_bg1_v411", "values", "ressalvas_secao8"], "op": "tamanho_igual", "valor": N_RESSALVAS, "estatuto": "[REAL]"})
    ck_p.append({"id": "p2", "descricao": "o core selado traz o que o teste nao decide", "onde": "core", "caminho": ["h0dn_bg1_v411", "o_que_o_teste_nao_decide"], "op": "tamanho_igual", "valor": N_NAO_DECIDE, "estatuto": "[REAL]"})
    ck_p.append({"id": "p3", "descricao": "o teste da razao de Hubble foi aberto uma vez e nao e' reaberto", "onde": "core", "caminho": ["h0dn_bg1_v411", "opened_once"], "op": "verdadeiro", "estatuto": "[REAL]"})
    diz_p = [TX.DIZ_P_ABERTURA] + [TX.DIZ_P_FORMA % r for r in TX.RESSALVAS] + [TX.DIZ_P_FECHO]
    ext_p = {"n_ressalvas": len(TX.RESSALVAS), "ressalvas_e_atos": [{"ressalva": a, "sobre": b, "ato_que_resolve": c} for a, b, c in TX.RESSALVAS], "n_contas_nao_rodadas": 3, "pre_registro_do_incremento_do_juno_no_selo": False,
             "lido_do_core": ["h0dn_bg1_v411.values.ressalvas_secao8", "h0dn_bg1_v411.o_que_o_teste_nao_decide", "h0dn_bg1_v411.opened_once"]}
    specs.append(spec_base("parede_do_teste_cego_v412", TX.ESTATUTO_P, diz_p, list(TX.LIM_P), list(TX.ND_P), ext_p, ck_p, [], []))
    # ---------------------------------------------------------------- cunhagens_v412 (as leis e definicoes da teoria que entram como ENTRADA)
    entradas = entradas_definicoes()
    ck_c = checks_herdadas("h", "cunhagens_v412")
    for i, nm in enumerate(NOMES[:3]):
        ck_c.append({"id": "r%d" % (i + 1), "descricao": "o registro %s sela neste rito" % nm, "onde": "core", "caminho": [nm, "all_verified"], "op": "verdadeiro", "estatuto": "[REAL]"})
    flags_c, decls_c = [], []
    k = 0
    for e in entradas:
        for a in e["ancoras"]:
            k += 1
            ck_c.append({"id": "ce%03d" % k, "descricao": "ancora que tipa '%s': %s (a bandeira e' verdadeira)" % (e["nome"], a["nome"]), "onde": "kf", "caminho": [a["bandeira"]], "op": "verdadeiro", "estatuto": "[REAL]"})
            flags_c.append(a["bandeira"]); decls_c.append(a["nome"])
    flags_c = list(dict.fromkeys(flags_c)); decls_c = list(dict.fromkeys(decls_c))
    ext_c = {"n_entradas": len(entradas), "entradas": entradas, "leis_e_definicoes_da_pagina_publica": list(TX.LEIS_A) + list(TX.LEIS_B)}
    specs.append(spec_base("cunhagens_v412", TX.ESTATUTO_C, list(TX.DIZ_C), list(TX.LIM_C), list(TX.ND_C), ext_c, ck_c, flags_c, decls_c))
    ids = [s["nome"] for s in specs]
    assert ids == NOMES, ids
    for s in specs:
        cid = [c["id"] for c in s["checks"]]
        assert len(cid) == len(set(cid)), ("id de checagem repetido", s["nome"])
        assert all(c["op"] in ("igual", "verdadeiro", "falso", "existe", "maior_igual", "tamanho_igual") for c in s["checks"])
    return specs


def entradas_definicoes():
    import textos_registros_v412 as TX
    todos = {}
    for reg in ANC["registros"].values():
        todos.update(reg["modulos"])
    out = []
    for mod, (nome, est) in TX.NOMES_CURTOS.items():
        t = (D / "insumos" / "pedras_r7" / (mod + ".lean")).read_bytes().decode("utf-8")
        h = re.search(r"/-!(.*?)-/", t, re.S).group(1)
        m = re.search(r"(?m)^## (A .*? que .*tipa.*)$", h)
        assert m, ("secao 'tipa' nao achada no cabecalho", mod)
        nao = re.search(r"(?m)^#{2,3} (O que .*N[ÃA]O .*|.*N[ÃA]O se afirma.*)$", h)
        corpo_nao = ""
        if nao:
            i0 = h.index(nao.group(0)); resto = h[i0 + len(nao.group(0)):]
            j = re.search(r"(?m)^#{2,3} ", resto)
            corpo_nao = resto[:j.start()] if j else resto
        n_itens_nao = len(re.findall(r"(?m)^\s*\* ", corpo_nao)) + len(re.findall(r"(?m)^\s*\|(?!---)", corpo_nao))
        anc = [a for a in todos[mod]["ancoras"] if "estrela" in a["regras"]] or todos[mod]["ancoras"]
        out.append({"nome": nome, "estatuto_de_entrada": est, "modulo": mod, "titulo_da_secao_do_cabecalho": m.group(1).strip(), "ancoras": [{"nome": a["nome"], "bandeira": a["bandeira"]} for a in anc],
                    "nao_tipado": {"secao_do_cabecalho": nao.group(1).strip() if nao else None, "n_itens": n_itens_nao}})
    assert len(out) == 10, len(out)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    s = especs()
    for sp in s:
        print(sp["nome"], "| prefixo:", sp["veredito_prefixo"], "|", len(sp["checks"]), "checks |", len(sp["kernel_flags"]), "flags |", len(sp["kernel_decls"]), "decls")

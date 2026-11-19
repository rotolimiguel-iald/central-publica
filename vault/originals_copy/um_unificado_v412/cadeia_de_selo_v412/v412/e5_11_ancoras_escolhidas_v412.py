"""R5, bloco 1/2: escolhe as ancoras de cada registro pela regra do contrato R5 (secao 1, 'Ancoras') e grava o recibo para a gerencia conferir: ANCORAS_ESCOLHIDAS_v412.json (o do R4 esta' na guarda fora de work\\ e em .bak).
Regra do contrato: cada registro ancora, por nome completo, as declaracoes com estrela dos seus modulos que nao sao private. Nos modulos sem estrela, ancora as declaracoes que a pagina publica cita (a pagina R18) e as que o cabecalho do
modulo da como resultado principal; nos modulos sem estrela que a pagina nao cita e cujo cabecalho nao da resultado principal, ancora as declaracoes que o proprio modulo lista nas suas linhas #print axioms (campo listadas_em_print_axioms).
Operacionalizacao (a mesma do recibo do R4, mais o que a frente C pede; a gerencia confere):
  (a) estrela: toda declaracao publica da lista com_estrela do modulo;
  (b) pagina: (b1) termo entre crases numa linha da tabela do bloco “O leitor da formula”: a declaracao publica de MESMO nome final num modulo da PROPRIA linha (so' neles); (b2) nome entre crases em qualquer outro ponto da pagina:
      a declaracao publica de qualquer modulo do registro cujo nome final e' esse (como no R4);
  (c) cabecalho: nome entre crases no bloco /-! ... -/ do cabecalho do modulo cujo nome final e' o de uma declaracao publica do modulo;
  (d) so' se (a), (b) e (c) derem zero ancoras para o modulo: as declaracoes do campo listadas_em_print_axioms do insumo (recuo; o recibo diz).
O NOME COMPLETO de cada ancora e' o que o relatorio de axiomas do sandbox tem (kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json, campo nome_no_audit e o caminho `via`); nenhum nome e' montado pelo prefixo do modulo.
Modulo que termine sem ancora e' falha visivel. Declaracao private nunca e' ancora por nome. Toda ancora precisa de bandeira, de estar no trio e de ter proveniencia no proprio modulo."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_lib_v412 import D, ler_json, salvar_json, sha16_arq, estado_bloco, MANIFESTO, PAGINA, PEDRAS, ANCORAS

K = D / "kernel"
CONF_P = K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json"
CONF = ler_json(CONF_P)
FL = ler_json(K / "FLAGS_v412.json")
MAN = ler_json(MANIFESTO)
pagina = PAGINA.read_bytes().decode("utf-8").replace("\r\n", "\n")
prov = FL["proveniencia_publicas"]
flag_de = {n: k for k, n, m, _ in FL["flags"]}
modulos_da_lista = {x["modulo"] for x in MAN["modulos"]}
RX_CR = r"`([A-Za-z_][A-Za-z0-9_'.]*)`"

# a pagina: as linhas da tabela do leitor da formula e o resto
linhas = pagina.split("\n")
i0 = [i for i, l in enumerate(linhas) if l.strip() == "| o que se afirma | termo | onde |"]
assert len(i0) == 1, "a tabela do bloco do leitor da formula nao foi achada"
i = i0[0] + 2; linhas_tab = []
while i < len(linhas) and linhas[i].startswith("|"):
    cel = [c.strip() for c in re.split(r" \| ", linhas[i].strip()[1:-1].strip())]
    assert len(cel) == 3
    linhas_tab.append({"linha": i + 1, "afirma": cel[0], "termos": re.findall(RX_CR, cel[0]) + re.findall(RX_CR, cel[1]), "modulos": [m for m in re.findall(RX_CR, cel[2]) if m in modulos_da_lista]})
    i += 1
resto = "\n".join(l for k, l in enumerate(linhas) if not (i0[0] <= k < i))
cit_resto = set(re.findall(RX_CR, resto))
termo_por_mod = {}   # modulo -> {nome final citado numa linha da tabela em que o modulo esta}
for lt in linhas_tab:
    for m in lt["modulos"]:
        termo_por_mod.setdefault(m, set()).update(t.split(".")[-1] for t in lt["termos"])


def ultimo(n):
    return n.split(".")[-1]


def cabecalho(mod):
    t = (PEDRAS / (mod + ".lean")).read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    return m.group(1) if m else ""


out = {"regra": __doc__.split("Operacionalizacao")[0].strip(), "operacionalizacao": "(a) estrela; (b1) termo de linha da tabela do leitor da formula, so' nos modulos da linha; (b2) nome citado no resto da pagina R18; (c) cabecalho do modulo; (d) so' como recuo, se (a), (b) e (c) derem zero: listadas_em_print_axioms",
       "nomes_completos": "lidos do relatorio de axiomas (kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json: via print_axioms, proveniencia ou namespace_do_insumo); nenhum montado pelo prefixo do modulo",
       "fontes": {"conferidas": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5.json", "flags": "kernel/FLAGS_v412.json", "pagina": "o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md", "manifesto": "insumos/MANIFESTO_PEDRAS_v412_R10.json", "propostas": "insumos/ANCORAS_PROPOSTAS_v412_R10.json"},
       "sha16_das_fontes": {"conferidas": sha16_arq(CONF_P), "flags": sha16_arq(K / "FLAGS_v412.json"), "pagina": sha16_arq(PAGINA), "manifesto": sha16_arq(MANIFESTO), "propostas": sha16_arq(ANCORAS)},
       "registros": {}}
problemas = []
total = 0; vias_escolhidas = {}; n_recuo = 0
for reg, itens in CONF["por_registro"].items():
    por_mod = {}
    ordem = []
    for it in itens:
        por_mod.setdefault(it["modulo"], []).append(it)
        if it["modulo"] not in ordem:
            ordem.append(it["modulo"])
    out["registros"][reg] = {"modulos": {}}
    for mod in ordem:
        its = por_mod[mod]
        publicas = [i_ for i_ in its if i_["classe"] == "publica"]
        privadas = sorted({i_["nome_proposto"] for i_ in its if i_["classe"] == "private"})
        por_ultimo = {}
        for i_ in publicas:
            por_ultimo.setdefault(ultimo(i_["nome_no_audit"]), {})[i_["nome_no_audit"]] = i_
        regras = {}; info = {}

        def marca(i_, r):
            regras.setdefault(i_["nome_no_audit"], set()).add(r)
            info[i_["nome_no_audit"]] = i_
        for i_ in publicas:
            if i_["lista"] == "com_estrela":
                marca(i_, "estrela")
        cit_tab = sorted(n for n in termo_por_mod.get(mod, ()) if n in por_ultimo)
        for n in cit_tab:
            for i_ in por_ultimo[n].values():
                marca(i_, "pagina")
        citados_pagina = sorted(n for n in cit_resto if ultimo(n) in por_ultimo)
        for n in citados_pagina:
            for i_ in por_ultimo[ultimo(n)].values():
                marca(i_, "pagina")
        cab = cabecalho(mod)
        cit_cab = sorted({n for n in re.findall(RX_CR, cab) if ultimo(n) in por_ultimo})
        for n in cit_cab:
            for i_ in por_ultimo[ultimo(n)].values():
                marca(i_, "cabecalho")
        recuo = False
        if not regras:
            recuo = True; n_recuo += 1
            for i_ in publicas:
                if i_["lista"] == "listadas_em_print_axioms":
                    marca(i_, "print_axioms (recuo)")
        sel = []
        for nome, rs in regras.items():
            i_ = info[nome]
            fl = flag_de.get(nome)
            ok = bool(fl) and i_["no_trio"] is True and i_["bandeira_proposta"] == fl and prov.get(nome) == "TGLExt/%s.lean" % mod
            if not ok:
                problemas.append({"registro": reg, "modulo": mod, "nome": nome, "bandeira": fl, "no_trio": i_["no_trio"], "proveniencia": prov.get(nome)})
            via = next((x["via"] for x in its if x["nome_no_audit"] == nome and x["via"]), None)
            vias_escolhidas[via] = vias_escolhidas.get(via, 0) + 1
            sel.append({"nome": nome, "bandeira": fl, "regras": sorted(rs), "no_trio": i_["no_trio"], "classe": i_["classe"], "via_do_nome_completo": via})
        sel.sort(key=lambda x: x["nome"])
        if not sel:
            problemas.append({"registro": reg, "modulo": mod, "problema": "modulo sem ancora nenhuma"})
        out["registros"][reg]["modulos"][mod] = {
            "n_publicas": len({i_["nome_no_audit"] for i_ in publicas}), "n_privadas_fora": len(privadas), "n_com_estrela": len({i_["nome_no_audit"] for i_ in publicas if i_["lista"] == "com_estrela"}),
            "citados_pela_pagina": sorted(set(cit_tab) | set(citados_pagina)), "citados_na_tabela_do_leitor": cit_tab, "citados_no_cabecalho": cit_cab, "recuo_print_axioms": recuo,
            "n_ancoras": len(sel), "ancoras": sel}
        total += len(sel)
    out["registros"][reg]["n_ancoras"] = sum(m["n_ancoras"] for m in out["registros"][reg]["modulos"].values())
    out["registros"][reg]["n_modulos"] = len(out["registros"][reg]["modulos"])
# cada termo citado na tabela do leitor e' declaracao publica (ancora) de um modulo da propria linha
todos_mod = {}
for r in out["registros"].values():
    todos_mod.update(r["modulos"])
sem_modulo = []
for lt in linhas_tab:
    for t in lt["termos"]:
        if lt["modulos"] and not any(ultimo(a["nome"]) == ultimo(t) for m in lt["modulos"] for a in todos_mod[m]["ancoras"]):
            sem_modulo.append({"linha_da_pagina": lt["linha"], "termo": t, "modulos_da_linha": lt["modulos"]})
if sem_modulo:
    problemas.append({"problema": "termo da tabela do leitor que nao e' ancora de modulo da propria linha", "itens": sem_modulo[:10]})
# comparacao com o recibo do R4 (os 42 modulos da setima lista nao mudaram)
g = ler_json(D / "GUARDA_R4_ETAPA2_v412.json")
r4p = next(c["guarda"] for c in g["copias"] if c["arquivo"] == "ANCORAS_ESCOLHIDAS_v412.json")
R4 = ler_json(r4p)
dif_r4 = {}
for reg, v in R4["registros"].items():
    for mod, d in v["modulos"].items():
        a4 = {a["nome"] for a in d["ancoras"]}; a5 = {a["nome"] for a in todos_mod.get(mod, {"ancoras": []})["ancoras"]}
        if a4 != a5:
            dif_r4[mod] = {"so_no_R4": sorted(a4 - a5), "so_no_R5": sorted(a5 - a4)}
out["n_ancoras_total"] = total
out["n_modulos_em_recuo_print_axioms"] = n_recuo
out["vias_dos_nomes_completos_das_ancoras"] = vias_escolhidas
out["ancoras_sem_nome_no_relatorio_de_axiomas"] = sum(1 for r in out["registros"].values() for m in r["modulos"].values() for a in m["ancoras"] if a["nome"] not in prov)
out["tabela_do_leitor"] = {"n_linhas": len(linhas_tab), "n_linhas_com_modulo": sum(1 for lt in linhas_tab if lt["modulos"]), "n_termos": sum(len(lt["termos"]) for lt in linhas_tab), "termos_sem_ancora_em_modulo_da_linha": sem_modulo}
out["comparacao_com_o_recibo_do_R4_nos_42_modulos"] = {"recibo_R4": r4p, "sha16": sha16_arq(r4p), "n_modulos_comparados": sum(len(v["modulos"]) for v in R4["registros"].values()), "modulos_com_ancoras_diferentes": dif_r4}
out["problemas"] = problemas
out["nomes_da_pagina_fora_da_tabela_do_leitor_que_nao_sao_declaracao_de_modulo_da_lista"] = sorted(n for n in cit_resto if not any(ultimo(n) == ultimo(a["nome"]) for m in todos_mod.values() for a in m["ancoras"]) and n not in modulos_da_lista)
saida = D / "ANCORAS_ESCOLHIDAS_v412.json"
salvar_json(saida, out)
print("ancoras por registro:", {r: v["n_ancoras"] for r, v in out["registros"].items()}, "| total", total, "| modulos em recuo:", n_recuo, "| vias:", vias_escolhidas, "| sem nome no relatorio:", out["ancoras_sem_nome_no_relatorio_de_axiomas"],
      "| problemas", len(problemas), "| diferem do R4:", list(dif_r4)[:8], "| termos da tabela sem ancora na linha:", len(sem_modulo))
for r, v in out["registros"].items():
    print(" ", r, "modulos", v["n_modulos"], "ancoras", v["n_ancoras"], "| em recuo:", sum(1 for d in v["modulos"].values() if d["recuo_print_axioms"]), "| sem estrela:", sum(1 for d in v["modulos"].values() if not d["n_com_estrela"]))
if problemas:
    print("PROBLEMAS:", str(problemas[:6])[:3000])
    sys.exit(1)
estado_bloco("1b_ancoras_escolhidas", True, {"recibo": saida, "script": D / "e5_11_ancoras_escolhidas_v412.py", "conferidas": CONF_P},
             nota="ancoras pela regra do contrato R5; nomes completos lidos do relatorio de axiomas; recibo para a gerencia conferir", proximo="registros_v412_r5.py; e5_60 (recibo dos registros)",
             extra={"por_registro": {r: v["n_ancoras"] for r, v in out["registros"].items()}, "total": total, "modulos_em_recuo": n_recuo, "vias": vias_escolhidas, "sem_nome_no_relatorio": out["ancoras_sem_nome_no_relatorio_de_axiomas"]})

"""Etapa 2, bloco 2: escolhe as ancoras de cada registro pela regra do contrato (secao 1, 'Ancoras') e grava o recibo para a gerencia conferir: ANCORAS_ESCOLHIDAS_v412.json.
Regra do contrato: cada registro ancora, por nome completo, as declaracoes com estrela dos seus modulos que nao sao private. Nos modulos sem estrela, ancora as declaracoes que a pagina publica cita
(secao 6 do contrato: a pagina R13) e as que o cabecalho do modulo da como resultado principal.
Operacionalizacao (dita no recibo; a gerencia confere):
  (a) estrela: toda declaracao publica da lista com_estrela do modulo (insumos\\ANCORAS_PROPOSTAS_v412_R7.json, conferida contra o Audit);
  (b) pagina: nome entre crases na pagina R13 cujo ultimo componente e' o de uma declaracao publica do modulo;
  (c) cabecalho: nome entre crases no bloco /-! ... -/ do cabecalho do modulo (fonte congelada em insumos\\pedras_r7) cujo ultimo componente e' o de uma declaracao publica do modulo;
  (d) so' se (a), (b) e (c) derem zero ancoras para o modulo: as declaracoes que o autor da pedra marcou com #print axioms na fonte (kernel\\FLAGS_v412.json, campo ancoras), e o recibo diz que foi recuo.
Modulo que termine sem ancora nenhuma e' falha visivel. Declaracao private nunca e' ancora por nome. Toda ancora precisa de bandeira e estar no trio (conferido contra kernel\\ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json e FLAGS_v412.json)."""
import re, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, ler_json, salvar_json, sha16_arq, estado_bloco

K = D / "kernel"
CONF = ler_json(K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json")
FL = ler_json(K / "FLAGS_v412.json")
PAG = D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md"
MAN = ler_json(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")
FONTES = D / "insumos" / "pedras_r7"
pagina = PAG.read_bytes().decode("utf-8")
cit_pagina = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_'.]*)`", pagina))


def ultimo(n):
    return n.split(".")[-1]


def cabecalho(mod):
    t = (FONTES / (mod + ".lean")).read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    return m.group(1) if m else ""


flag_de = {n: k for k, n, m, _ in FL["flags"]}
ancoras_print = {}   # modulo -> lista de nomes #print axioms resolvidos
for nome, d in FL["ancoras"].items():
    ancoras_print.setdefault(d["modulo"], []).append(nome)

out = {"regra": __doc__.split("Operacionalizacao")[0].strip(), "operacionalizacao": "(a) estrela; (b) pagina R13; (c) cabecalho do modulo; (d) so' como recuo, se (a), (b) e (c) derem zero",
       "fontes": {"conferidas": "kernel/ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json", "flags": "kernel/FLAGS_v412.json", "pagina": "o_que_fica_claro_REV13/O_QUE_FICA_CLARO_v412_R13.md", "manifesto": "insumos/MANIFESTO_PEDRAS_v412_R7.json"},
       "sha16_das_fontes": {"conferidas": sha16_arq(K / "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R4.json"), "flags": sha16_arq(K / "FLAGS_v412.json"), "pagina": sha16_arq(PAG), "manifesto": sha16_arq(D / "insumos" / "MANIFESTO_PEDRAS_v412_R7.json")},
       "registros": {}}
problemas = []
total = 0
for reg, itens in CONF["por_registro"].items():
    por_mod = {}
    for it in itens:
        por_mod.setdefault(it["modulo"], []).append(it)
    out["registros"][reg] = {"modulos": {}}
    ordem = []
    for it in itens:
        if it["modulo"] not in ordem:
            ordem.append(it["modulo"])
    for mod in ordem:
        its = por_mod[mod]
        publicas = [i for i in its if i["classe"] in ("publica", "por_sufixo")]
        privadas = [i for i in its if i["classe"] == "private"]
        por_ultimo = {}
        for i in publicas:
            por_ultimo.setdefault(ultimo(i["nome_proposto"]), []).append(i)
        regras = {}   # nome_no_audit -> set(regras)
        info = {}

        def marca(i, r):
            regras.setdefault(i["nome_no_audit"], set()).add(r)
            info[i["nome_no_audit"]] = i
        for i in publicas:
            if i["lista"] == "com_estrela":
                marca(i, "estrela")
        citados_pagina = sorted(n for n in cit_pagina if n in por_ultimo)
        for n in citados_pagina:
            for i in por_ultimo[n]:
                marca(i, "pagina")
        cab = cabecalho(mod)
        cit_cab = sorted({n for n in re.findall(r"`([A-Za-z_][A-Za-z0-9_'.]*)`", cab) if ultimo(n) in por_ultimo})
        for n in cit_cab:
            for i in por_ultimo[ultimo(n)]:
                marca(i, "cabecalho")
        recuo = False
        if not regras:
            recuo = True
            nomes_print = set(ancoras_print.get("TGLExt." + mod, []))
            for i in publicas:
                if i["nome_no_audit"] in nomes_print or i["nome_proposto"] in nomes_print:
                    marca(i, "print_axioms (recuo)")
        sel = []
        for nome, rs in regras.items():
            i = info[nome]
            fl = i["bandeira_proposta"] or flag_de.get(nome)
            ok = bool(fl) and i["no_trio"] is True and flag_de.get(nome) == fl
            if not ok:
                problemas.append({"registro": reg, "modulo": mod, "nome": nome, "bandeira": fl, "no_trio": i["no_trio"], "flag_no_FLAGS": flag_de.get(nome)})
            sel.append({"nome": nome, "bandeira": fl, "regras": sorted(rs), "no_trio": i["no_trio"], "classe": i["classe"]})
        sel.sort(key=lambda x: x["nome"])
        if not sel:
            problemas.append({"registro": reg, "modulo": mod, "problema": "modulo sem ancora nenhuma"})
        out["registros"][reg]["modulos"][mod] = {
            "n_publicas": len(publicas), "n_privadas_fora": len(privadas), "n_com_estrela": sum(1 for i in publicas if i["lista"] == "com_estrela"),
            "citados_pela_pagina": citados_pagina, "citados_no_cabecalho": cit_cab, "recuo_print_axioms": recuo,
            "n_ancoras": len(sel), "ancoras": sel}
        total += len(sel)
    out["registros"][reg]["n_ancoras"] = sum(m["n_ancoras"] for m in out["registros"][reg]["modulos"].values())
    out["registros"][reg]["n_modulos"] = len(out["registros"][reg]["modulos"])
out["n_ancoras_total"] = total
out["problemas"] = problemas
out["nomes_da_pagina_que_nao_sao_declaracao_de_modulo_do_registro"] = sorted(n for n in cit_pagina if not any(n in {ultimo(i["nome_proposto"]) for i in its} for its in CONF["por_registro"].values()))
saida = D / "ANCORAS_ESCOLHIDAS_v412.json"
salvar_json(saida, out)
print("ancoras por registro:", {r: v["n_ancoras"] for r, v in out["registros"].items()}, "total", total, "problemas", len(problemas))
for r, v in out["registros"].items():
    for m, d in v["modulos"].items():
        print("  %-30s n=%3d estrela=%3d pagina=%d cab=%d recuo=%s" % (m, d["n_ancoras"], d["n_com_estrela"], len(d["citados_pela_pagina"]), len(d["citados_no_cabecalho"]), d["recuo_print_axioms"]))
if problemas:
    print("PROBLEMAS:", problemas[:10])
    sys.exit(1)
estado_bloco("2a_ancoras_escolhidas_c4", True, {"recibo": saida, "script": D / "e2_11_ancoras_escolhidas_v412.py"}, nota="ancoras pela regra do contrato; recibo para a gerencia conferir", proximo="registros_v412.py (specs)")

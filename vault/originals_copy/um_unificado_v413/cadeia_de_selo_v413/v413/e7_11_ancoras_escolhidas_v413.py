# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_11_ancoras_escolhidas_v412.py (que fica intacto), pela regra de ancoras do contrato da v413 (secao 1).
"""Etapa 2 da v413, bloco 2a: escolhe as ancoras de cada registro pela regra do contrato congelado e grava ANCORAS_ESCOLHIDAS_v413.json (o recibo para a gerencia conferir).
Regra do contrato da v413 (secao 1, 'Ancoras'): cada registro ancora, por nome completo, as declaracoes com estrela dos seus modulos que nao sao private, e as que a pagina publica cita.
Operacionalizacao (a mesma do molde da v412, sem o recuo pelos #print axioms, que o contrato da v413 nao traz):
  (a) estrela: toda declaracao publica do modulo marcada com estrela no insumo das ancoras propostas;
  (b) pagina: (b1) termo entre crases numa linha da tabela da secao 2 da pagina (| frase | termo | onde |): a declaracao publica de MESMO nome final (ou de mesmo nome qualificado) num modulo da PROPRIA linha;
      (b2) nome entre crases em qualquer outro ponto da pagina: a declaracao publica de qualquer modulo do registro cujo nome final e' esse (ou cujo nome completo termina pelo nome qualificado citado).
O NOME COMPLETO de cada ancora e' o do relatorio de axiomas do sandbox (kernel\\audit.log do build do k413c: linhas TGL_DECL_SOURCE e 'NOME' depends on axioms), nunca montado pelo prefixo do modulo (alguns modulos
abrem espacos de nome Codex.* ou TGLExt.SimTM2). Toda ancora precisa de bandeira (kernel\\FLAGS_v413.json), de estar no relatorio de axiomas so' com os tres axiomas (ou nenhum) e de ter proveniencia no proprio modulo.
Declaracao private nunca e' ancora por nome. Um modulo sem estrela que a pagina nao cita fica sem ancora: o recibo o lista (informativo; o contrato da v413 nao traz o recuo)."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

TRIO = {"propext", "Classical.choice", "Quot.sound"}
FL = L.ler_json(L.KD / "FLAGS_v413.json")
PROP = L.ler_json(L.ANCORAS)
flag_de = {n: k for k, n, m, _ in FL["flags"]}
modulo_da_flag = {n: m for k, n, m, _ in FL["flags"]}
prov = FL["proveniencia_publicas"]
# o relatorio de axiomas do build do sandbox (copia de bytes em kernel\audit.log)
AUD = (L.KD / "audit.log").read_bytes().decode("utf-8", "replace")
axiomas = {}
fonte_decl = {}
for m in re.finditer(r"^'([^']+)' depends on axioms: \[([^\]]*)\]", AUD, re.M):
    axiomas.setdefault(m.group(1), set()).update(a.strip() for a in m.group(2).split(",") if a.strip())
for m in re.finditer(r"^'([^']+)' does not depend on any axioms", AUD, re.M):
    axiomas.setdefault(m.group(1), set())
for m in re.finditer(r"^TGL_DECL_SOURCE\t(\S+)\t(\S+)", AUD, re.M):
    fonte_decl[m.group(1)] = m.group(2)
pagina = L.PAGINA.read_bytes().decode("utf-8").replace("\r\n", "\n")
RX_CR = r"`([A-Za-z_][A-Za-z0-9_'.]*)`"
modulos_de = {reg: dict(mods) for reg, mods in PROP["registros"].items()}
todos_os_modulos = {m for ms in modulos_de.values() for m in ms}

# a tabela da secao 2 da pagina
linhas = pagina.split("\n")
i0 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\|\s*frase\s*\|\s*termo\s*\|\s*onde\s*\|", l.strip())]
assert len(i0) == 1, "a tabela da secao 2 da pagina nao foi achada (ou ha' mais de uma)"
i = i0[0] + 2
linhas_tab = []
while i < len(linhas) and linhas[i].startswith("|"):
    cel = [c.strip() for c in re.split(r" \| ", linhas[i].strip()[1:-1].strip())]
    assert len(cel) == 3, ("linha da tabela sem tres celulas", linhas[i][:80])
    linhas_tab.append({"linha": i + 1, "frase": cel[0], "termos": re.findall(RX_CR, cel[0]) + re.findall(RX_CR, cel[1]), "modulos": [m for m in re.findall(RX_CR, cel[2]) if m in todos_os_modulos],
                       "nao_modulos_na_coluna_onde": [m for m in re.findall(RX_CR, cel[2]) if m not in todos_os_modulos]})
    i += 1
resto = "\n".join(l for k, l in enumerate(linhas) if not (i0[0] <= k < i))
cit_resto = sorted(set(re.findall(RX_CR, resto)))


def casa(nome_completo, citado):
    """o nome citado casa com o nome completo: igual, ou o completo termina por '.' + citado (citado qualificado ou nome final)"""
    return nome_completo == citado or nome_completo.endswith("." + citado)


out = {"regra": __doc__.split("Operacionalizacao")[0].strip(), "operacionalizacao": "(a) estrela; (b1) termo de linha da tabela da secao 2, so' nos modulos da linha; (b2) nome citado no resto da pagina, nos modulos do registro",
       "nomes_completos": "lidos do relatorio de axiomas do build do sandbox (kernel/audit.log: TGL_DECL_SOURCE e depends on axioms); nenhum montado pelo prefixo do modulo",
       "fontes": {"flags": "kernel/FLAGS_v413.json", "relatorio_de_axiomas": "kernel/audit.log", "pagina": str(L.PAGINA.relative_to(L.D)), "propostas": "insumos/ANCORAS_PROPOSTAS_v413.json", "manifesto": "insumos/MANIFESTO_PEDRAS_v413.json"},
       "sha16_das_fontes": {"flags": L.sha16_arq(L.KD / "FLAGS_v413.json"), "relatorio_de_axiomas": L.sha16_arq(L.KD / "audit.log"), "pagina": L.sha16_arq(L.PAGINA), "propostas": L.sha16_arq(L.ANCORAS), "manifesto": L.sha16_arq(L.MANIFESTO)},
       "modo": L.MODO, "registros": {}}
problemas, sem_ancora = [], []
for reg, mods in modulos_de.items():
    out["registros"][reg] = {"modulos": {}}
    for mod, d in mods.items():
        publicas = [x for x in d["declaracoes"] if not x["privada"]]
        privadas = [x["nome"] for x in d["declaracoes"] if x["privada"]]
        _ja = {x["nome"] for x in publicas}
        # (b) vale para toda DECLARACAO publica do modulo que a pagina cita (definicao tambem), nao so' para os teoremas do insumo: as nomeadas publicas sao as que tem bandeira (FLAGS_v413.json)
        publicas += [{"nome": n, "privada": False, "estrela": False, "axiomas": sorted(axiomas.get(n) or []), "fora_do_insumo_das_propostas": True}
                     for n, mm in sorted(modulo_da_flag.items()) if mm == "TGLExt.%s" % mod and n not in _ja]
        regras, info = {}, {}

        def marca(x, r):
            regras.setdefault(x["nome"], set()).add(r)
            info[x["nome"]] = x
        for x in publicas:
            if x["estrela"]:
                marca(x, "estrela")
        cit_tab = sorted({t for lt in linhas_tab if mod in lt["modulos"] for t in lt["termos"]})
        for t in cit_tab:
            for x in publicas:
                if casa(x["nome"], t):
                    marca(x, "pagina")
        cit_r = []
        for t in cit_resto:
            for x in publicas:
                if casa(x["nome"], t):
                    marca(x, "pagina"); cit_r.append(t)
        sel = []
        for nome, rs in sorted(regras.items()):
            x = info[nome]
            fl = flag_de.get(nome)
            ax = axiomas.get(nome)
            ok = bool(fl) and ax is not None and ax <= TRIO and prov.get(nome) == "TGLExt/%s.lean" % mod and fonte_decl.get(nome) == "TGLExt.%s" % mod and set(x["axiomas"]) == ax
            if not ok:
                problemas.append({"registro": reg, "modulo": mod, "nome": nome, "bandeira": fl, "axiomas_no_relatorio": sorted(ax) if ax is not None else None, "axiomas_no_insumo": x["axiomas"],
                                  "proveniencia": prov.get(nome), "fonte_no_relatorio": fonte_decl.get(nome)})
            sel.append({"nome": nome, "bandeira": fl, "regras": sorted(rs), "axiomas": sorted(ax) if ax is not None else None, "no_trio": ax is not None and ax <= TRIO,
                        **({"fora_do_insumo_das_propostas": True} if x.get("fora_do_insumo_das_propostas") else {})})
        if not sel:
            sem_ancora.append({"registro": reg, "modulo": mod, "n_publicas": len(publicas), "com_estrela": d["com_estrela"]})
        out["registros"][reg]["modulos"][mod] = {"n_publicas": len(publicas), "n_privadas_fora": len(privadas), "n_com_estrela": sum(1 for x in publicas if x["estrela"]),
                                                 "citados_na_tabela_da_secao_2": cit_tab, "citados_no_resto_da_pagina": sorted(set(cit_r)), "n_ancoras": len(sel), "ancoras": sel}
    out["registros"][reg]["n_ancoras"] = sum(v["n_ancoras"] for v in out["registros"][reg]["modulos"].values())
    out["registros"][reg]["n_modulos"] = len(mods)
# cada termo citado na tabela e' ancora de um modulo da propria linha (ou e' declaracao do kernel selado, dita a parte)
todos_mod = {m: v for r in out["registros"].values() for m, v in r["modulos"].items()}
termos_sem_ancora = []
for lt in linhas_tab:
    for t in lt["termos"]:
        if not any(casa(a["nome"], t) for m in lt["modulos"] for a in todos_mod[m]["ancoras"]):
            no_selado = sorted(n for n in fonte_decl if casa(n, t) and n not in flag_de)
            termos_sem_ancora.append({"linha_da_pagina": lt["linha"], "termo": t, "modulos_da_linha": lt["modulos"], "declaracoes_do_kernel_selado_com_esse_nome": no_selado[:5],
                                      "declaracoes_novas_com_esse_nome_fora_da_linha": sorted(n for n in flag_de if casa(n, t))[:5]})
out["n_ancoras_total"] = sum(r["n_ancoras"] for r in out["registros"].values())
out["n_ancoras_por_registro"] = {r: v["n_ancoras"] for r, v in out["registros"].items()}
out["modulos_sem_ancora"] = sem_ancora
out["tabela_da_secao_2"] = {"n_linhas": len(linhas_tab), "n_termos": sum(len(lt["termos"]) for lt in linhas_tab), "linhas": linhas_tab, "termos_sem_ancora_em_modulo_da_linha": termos_sem_ancora}
out["nomes_do_resto_da_pagina_que_nao_sao_ancora"] = sorted(t for t in cit_resto if not any(casa(a["nome"], t) for v in todos_mod.values() for a in v["ancoras"]) and t not in todos_os_modulos)
out["ancoras_sem_nome_no_relatorio_de_axiomas"] = sum(1 for v in todos_mod.values() for a in v["ancoras"] if a["axiomas"] is None)
out["problemas"] = problemas
saida = L.saida("ANCORAS_ESCOLHIDAS_v413.json")
L.salvar_json(saida, out)
print("ancoras por registro:", out["n_ancoras_por_registro"], "| total", out["n_ancoras_total"], "| problemas", len(problemas), "| modulos sem ancora:", [(x["modulo"], x["n_publicas"]) for x in sem_ancora])
print("termos da tabela sem ancora na linha:", [(x["termo"], x["declaracoes_do_kernel_selado_com_esse_nome"], x["declaracoes_novas_com_esse_nome_fora_da_linha"]) for x in termos_sem_ancora])
print("nomes do resto da pagina que nao sao ancora:", out["nomes_do_resto_da_pagina_que_nao_sao_ancora"])
if problemas:
    print("PROBLEMAS:", str(problemas[:6])[:3000])
sys.exit(1 if problemas else 0)

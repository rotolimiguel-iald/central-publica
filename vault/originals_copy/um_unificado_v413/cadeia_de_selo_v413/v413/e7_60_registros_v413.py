# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_60_registros_v412.py (que fica intacto).
"""Etapa 2 da v413, bloco 2 (fecho): confere os cinco registros: palavra de veredito igual a' do contrato (copiada por script); a travessia da guarda herdada da v412 sobre o corpo e o veredito de cada um (unidades > 0,
zero violacao); a P18; o verificador de historia (corpo, descricoes das checagens, estatuto); a checagem da guarda presente em cada registro; contagem de ancoras e de checagens; nenhum registro usa “P = nP” sem as duas
marcas na mesma unidade; grava REGISTROS_v413_RECIBO.json (no modo proposta, com o sufixo)."""
import hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import registros_v413 as RG
import guarda_frases_v413 as GF
import verificar_historia_texto_v413 as VH
import delta_v413 as DL

specs = RG.especs()
ex = L.Exame("registros_v413")
rec = {}
palavras = RG.palavras_do_contrato()
for s in specs:
    nome = s["nome"]
    w = s["veredito_prefixo"] + "__" + s["veredito_sufixo"]
    corpo = {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}
    t = GF.travessia("registro:" + nome, {"corpo": corpo, "veredito": w})
    v_p18 = GF.p18(json.dumps(corpo, ensure_ascii=False))
    hist = VH.examinar([("corpo", json.dumps(corpo, ensure_ascii=False))] + [("check/%s" % c["id"], c["descricao"]) for c in s["checks"]] + [("estatuto", s["estatuto"])])
    ids = [c["id"] for c in s["checks"]]
    tem_guarda = [c for c in s["checks"] if c["caminho"][:2] == ["guarda_frases_v413", nome]]
    pnp = [u for u in t["unidades"] if re.search(r"P\s*=\s*nP", u["texto"])]
    ex.chk("%s: a palavra de veredito e' exatamente a do contrato (copiada por script; a mesma que o delta le)" % nome, w == palavras[nome] == DL.PALAVRAS_DE_VEREDITO[nome], 1, hashlib.sha256(w.encode()).hexdigest()[:16])
    ex.chk("%s: a travessia da guarda herdada sobre o corpo e o veredito: zero violacao e mais de zero unidades" % nome, t["ok"] and t["n_unidades"] > 0, t["n_unidades"], t["violacoes"][:3])
    ex.chk("%s: a checagem da guarda esta no registro (zero violacao; unidades >= 1)" % nome, len(tem_guarda) == 2, len(tem_guarda), [c["id"] for c in tem_guarda])
    ex.chk("%s: a guarda P18 nao acha violacao no corpo" % nome, not v_p18, 1, v_p18[:3])
    ex.chk("%s: o verificador de historia nao acha nada (corpo, descricoes das checagens, estatuto)" % nome, hist["ok"], hist["n_unidades_examinadas"], hist["achados"][:3])
    ex.chk("%s: ids de checagem unicos e cada ancora tem as suas checagens" % nome, len(ids) == len(set(ids)) and (not s["kernel_flags"] or sum(1 for i in ids if i.startswith(("ab", "ce"))) >= len(s["kernel_flags"])), len(ids))
    ex.chk("%s: nenhum veredito proibido; o registro nao declara falas; fonte so' o kh (o recibo KH_N1 pinado)" % nome, not any(x in w for x in ("CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM")) and not s["verbatins"]
           and (not s["fontes"] or (nome == L.KH_REGISTRO_V413 and s["fontes"] == ["kh_n1_v413"])), len(w))
    ex.chk("%s: toda unidade com “P = nP” traz as duas marcas e passa na guarda" % nome, all(not u["regras"] and "classes do seu dicionário" in u["texto"] for u in pnp), max(1, len(pnp)), [u["inicio"] for u in pnp])
    rec[nome] = {"veredito": w, "n_checagens": len(ids), "n_ancoras": len(s["kernel_flags"]), "n_decls": len(s["kernel_decls"]), "n_diz": len(s["diz"]), "n_limites": len(s["limites"]), "n_nao_diz": len(s["nao_diz"]),
                 "n_unidades_da_travessia": t["n_unidades"], "n_violacoes": len(t["violacoes"]), "p18": len(v_p18), "historia_achados": hist["n_achados"], "historia_unidades": hist["n_unidades_examinadas"],
                 "historia_identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "unidades_com_p_igual_np": [{"campo": u["campo"], "inicio": u["inicio"], "regras": u["regras"]} for u in pnp]}
ex.chk("sao os cinco registros do contrato mais o kh_n1_cobertura_v413 (contrato R2), na ordem, e cunhagens_v413 cobra o selo dos quatro com modulo", [s["nome"] for s in specs] == RG.NOMES and len(specs) == 6
       and sorted(c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")) == sorted(RG.ID_DO_SELO.values()), len(specs), [c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")])
_kh = [s for s in specs if s["nome"] == L.KH_REGISTRO_V413][0]
_khl = {c["capturar"]: c["valor"] for c in _kh["checks"] if c.get("capturar") in ("constantes_cobertas", "teoremas_cobertos")}
_KHR = L.ler_json(L.KH_N1_V413)
ex.chk("kh_n1_cobertura_v413: captura constantes e teoremas cobertos (as do recibo KH_N1), o veredito diz NONE_OUTSIDE_THE_TRIO e a fonte pinada e' o recibo", _khl == {"constantes_cobertas": _KHR["linha_TOTAL"]["decl"], "teoremas_cobertos": _KHR["linha_TOTAL"]["thm"]}
       and "NONE_OUTSIDE_THE_TRIO" in _kh["veredito_sufixo"] and _kh["fontes"] == ["kh_n1_v413"], 3, _khl)
# (revisao de terceiro do candidato) M1: nao_diz diz o que NAO se afirma (a custodia o copia para "nao se afirma"); B4: nenhum nome de uma letra lido como declaracao citada
_nd = [(s["nome"], x) for s in specs for x in s["nao_diz"]]
_m1 = {a["texto"] for a in RG.AJUSTES if a["achado"] == "M1"}
ex.chk("(revisao M1) cada item de nao_diz, em todos os registros, e' coisa NAO afirmada: comeca por 'que ' ou e' item reescrito pela revisao na forma 'o que nao se afirma: o que a pagina afirma'",
       bool(_nd) and bool(_m1) and all(x.startswith("que ") or x in _m1 for _, x in _nd), len(_nd), [(n, x[:70]) for n, x in _nd if not (x.startswith("que ") or x in _m1)][:6])
_ent = [e_ for s in specs if s["nome"] == "cunhagens_v413" for e_ in s["extras"]["entradas"]]
ex.chk("(revisao B4) nenhuma declaracao citada de uma letra so' nos extras de cunhagens_v413", bool(_ent) and all(len(d_) > 1 for e_ in _ent for d_ in e_["declaracoes_do_kernel_selado_citadas_na_secao"]), len(_ent))
import ajustes_revisao_v413 as AJR   # noqa: E402
out = {"contrato": "REGISTROS_v413_RECIBO", "modo": L.MODO, "ok": ex.ok, "resumo": ex.resumo(), "checagens": ex.linhas, "registros": rec, "n_ancoras_total": sum(r["n_ancoras"] for r in rec.values()),
       "ajustes_da_revisao_de_terceiro": {"itens_de_registro": RG.AJUSTES, "pagina": AJR.recibo()},
       "n_checagens_total": sum(r["n_checagens"] for r in rec.values()),
       "contrato_seguido": {"arquivo": L.CONTRATO.name, "sha16": L.sha16_arq(L.CONTRATO)}, "ancoras_escolhidas": {"arquivo": L.saida("ANCORAS_ESCOLHIDAS_v413.json").name, "sha16": L.sha16_arq(L.saida("ANCORAS_ESCOLHIDAS_v413.json"))},
       "pagina": {"arquivo": str(L.PAGINA.relative_to(L.D)), "sha16": L.sha16_arq(L.PAGINA)}, "textos": {"registros_v413.py": L.sha16_arq(L.D / "registros_v413.py"), "textos_registros_v413.py": L.sha16_arq(L.D / "textos_registros_v413.py")}}
saida = L.saida("REGISTROS_v413_RECIBO.json")
L.salvar_json(saida, out)
print("registros:", ex.resumo(), "ok" if ex.ok else "FALHA")
for l in ex.linhas:
    if not l["ok"]:
        print("  FALHOU:", l["checagem"], "|", l["n_itens_examinados"], "|", str(l["detalhe"])[:400])
L.estado_bloco("2_registros", ex.ok, {"recibo": saida, "ancoras_escolhidas": L.saida("ANCORAS_ESCOLHIDAS_v413.json"), "titulos_dos_cabecalhos": L.D / "TITULOS_DOS_CABECALHOS_v413.json",
                                       "registros": L.D / "registros_v413.py", "textos": L.D / "textos_registros_v413.py", "ancoras_script": L.D / "e7_11_ancoras_escolhidas_v413.py", "cabecalhos_script": L.D / "e7_12_titulos_dos_cabecalhos_v413.py",
                                       "verificador_de_historia": L.D / "verificar_historia_texto_v413.py", "guarda": L.D / "guarda_frases_v413.py", "proposta_pagina": L.D / "PROPOSTA_PAGINA_R1_v413.json"},
               nota="os cinco registros por especificacao, as ancoras pela regra do contrato (estrela + citadas pela pagina), as palavras do contrato por script; a pagina pinada falha a F37b herdada no paragrafo da secao 2 (conflito medido; proposta R1 gravada, nao adotada)",
               proximo="e7_30 (VERBATIM_CONGELADO_v413.json); e7_23 (texto publico); e7_40 (recibos)", extra={"n_ancoras": out["n_ancoras_total"], "n_checagens": out["n_checagens_total"], "por_registro": {k: v["n_ancoras"] for k, v in rec.items()}})
sys.exit(0 if ex.ok else 1)

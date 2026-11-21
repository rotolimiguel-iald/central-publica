# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_40_recibos_v412.py (que fica intacto).
"""Etapa 2 da v413, blocos 4 e 5 (recibos do texto novo): a travessia da guarda herdada da v412 sobre TODAS as superficies novas (os cinco registros, a secao do artigo PT/EN, os blocos do README, do estado atual e do handoff
PT/EN; o resumo do artigo nao muda), o recibo GUARDA_v413_UNIDADES.json, o recibo das unidades com “P = nP” (GUARDA_v413_P_IGUAL_NP.json: cada unidade, a superficie, o campo e o resultado da guarda), o verificador de
historia sobre toda unidade, a varredura das formas da F43, a negacao de toda mencao a tautologia, os marcadores herdados conferidos (MARCADORES_HERDADOS_v413.json) e os blocos em BLOCOS_TEXTO_PUBLICO_v413.json.
uso: C:\\Python314\\python.exe -B -X utf8 e7_40_recibos_v413.py [--contagem N]"""
import hashlib, json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import guarda_frases_v413 as GF
import verificar_historia_texto_v413 as VH
import registros_v413 as RG
import blocos_texto_publico_v413 as BL

travessia = GF.travessia
N_ARQ = int(sys.argv[sys.argv.index("--contagem") + 1]) if "--contagem" in sys.argv else len([p for p in L.D.iterdir()])
TP = L.ler_json(L.saida("TEXTO_PUBLICO_v413.json"))
assert TP["fonte_pt"]["sha16"] == L.sha16_arq(L.PAGINA) and TP["fonte_en"]["sha16"] == L.sha16_arq(L.PAGINA_EN), "TEXTO_PUBLICO_v413 nao e' da pagina/traducao atuais: rode e7_23"
CAND_P = L.saida("CANDIDATO_v413.json")
CAND = L.ler_json(CAND_P) if CAND_P.exists() else None
specs = RG.especs()
nomes_reg = [s["nome"] for s in specs]
superficies = []
for s in specs:
    superficies.append(("registro:" + s["nome"], {"corpo": {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]}, "dados"))
for lg in ("pt", "en"):
    superficies.append(("artigo:" + lg, TP["tex"][lg], "tex"))
BLOCOS = {}
for lg in ("pt", "en"):
    b = BL.blocos_da_pagina(lg)
    BLOCOS["readme:" + lg] = dict(b); BLOCOS["estado_atual:" + lg] = dict(b)
    h = dict(b)
    if CAND:
        h["entrega"] = BL.bloco_handoff(lg, CAND, nomes_reg)   # (revisao B9) sem a contagem da pasta, que envelhece
    BLOCOS["handoff:" + lg] = h
for nome, obj in BLOCOS.items():
    superficies.append((nome, obj, "dados"))
e = L.Exame("texto_novo_v413")
rec_s = {}; todas = []
for nome, obj, forma in superficies:
    t = travessia(nome, obj, forma)
    rec_s[nome] = {"n_unidades": t["n_unidades"], "ok": t["ok"], "n_violacoes": len(t["violacoes"]), "violacoes": [list(v[:3]) for v in t["violacoes"][:5]], "campos": {}}
    for u in t["unidades"]:
        rec_s[nome]["campos"].setdefault(u["campo"], []).append({"tipo": u["tipo"], "inicio": u["inicio"], "regras": u["regras"]})
        todas.append((nome, u["campo"], u["tipo"], u["texto"], u["regras"]))
    e.chk("a travessia sobre a superficie %s: zero violacao e mais de zero unidades" % nome, t["ok"] and t["n_unidades"] > 0, t["n_unidades"], t["violacoes"][:2])
alvo = [(n, c, ti, tx, rg) for n, c, ti, tx, rg in todas if re.search(r"P\s*=\s*nP", tx)]
marcas = lambda tx: {"classes_do_dicionario": bool(re.search(r"classes do seu dicionário|classes do dicionário da TGL|classes of its dictionary|classes of the TGL dictionary", tx)),
                     "maquina_de_fita_nao_demonstrado": bool(re.search(r"máquina de fita[^.;]*não está demonstrad|tape machine[^.;]*has not been shown", tx))}
e.chk("ha unidades com “P = nP” e NENHUMA tem violacao (cada uma com as duas marcas na mesma unidade)", len(alvo) > 0 and all(not rg and all(marcas(tx).values()) for *_x, tx, rg in [(a[0], a[1], a[2], a[3], a[4]) for a in alvo]), len(alvo),
      [(a[0], a[1], a[4]) for a in alvo if a[4] or not all(marcas(a[3]).values())][:4])
f43 = re.compile(r"or[aá]culo|oracle|leitor\s+de\s+Turing|Turing\s+reader|leitor\s+que\s+devolve\s+Z|reader\s+that\s+returns\s+Z", re.I)
achou43 = [(n, c, tx[:80]) for n, c, ti, tx, rg in todas if f43.search(tx)]
e.chk("as formas da F43 (oraculo, leitor de Turing, leitor que devolve Z) nao aparecem em nenhuma unidade emitida", not achou43, len(todas), achou43[:3])
taut = [(n, c, tx[max(0, m.start() - 400):m.end() + 20]) for n, c, ti, tx, rg in todas for m in re.finditer(r"tautol|TAUTOL", tx)]
taut_sem_negacao = [t for t in taut if not re.search(r"\bn(?:ã|a)o\b|\bnot\b|\bnor\b|_NOT_|NOT_", t[2], re.I)]
e.chk("toda mencao a tautologia vem negada (ou nao ha mencao)", not taut_sem_negacao, max(1, len(todas)), taut_sem_negacao[:3])
premio = [(n, c, tx[:80]) for n, c, ti, tx, rg in todas if re.search(r"\bClay\b|Mil[eê]nio|Millennium", tx, re.I)]
e.chk("o nome do premio nao aparece em nenhuma unidade emitida", not premio, len(todas), premio[:3])
auto = VH.autoteste()
e.chk("o verificador de historia tem autoteste (cada classe forte detecta a sua frase plantada; as limpas nao disparam)", auto["ok"], auto["n"], auto["n_ok"])
hist = VH.examinar([("%s/%s" % (n, c), tx) for n, c, ti, tx, rg in todas])
e.chk("o verificador de historia nao acha nada em nenhuma unidade de texto novo", hist["ok"], hist["n_unidades_examinadas"], hist["achados"][:4])
MH = L.ler_json(L.D / "MARCADORES_HERDADOS_v413.json")
e.chk("os marcadores herdados do handoff estao pinados (os 34 do molde da v412, corpo do handoff selado da v412)", MH["ok"] and MH["n_marcadores"] == 34, MH["n_marcadores"], [d["marcador"] for d in MH["diferem_do_insumo_da_v412"]])
tot = sum(v["n_unidades"] for v in rec_s.values())
pnp_rec = [{"superficie": n, "campo": c, "tipo": ti, "texto": tx, "regras": rg, "marcas": marcas(tx), "resultado": "LIMPO" if not rg else "RECUSADO"} for n, c, ti, tx, rg in alvo]
L.salvar_json(L.saida("GUARDA_v413_P_IGUAL_NP.json"), {"contrato": "GUARDA_v413_P_IGUAL_NP", "regra": "contrato da v413, secao 5: cada unidade de texto da v413 em que aparece “P = nP” e o resultado da guarda herdada (a mesma unidade traz as duas marcas)",
                                                        "modo": L.MODO, "pagina": {"arquivo": str(L.PAGINA.relative_to(L.D)), "sha16": L.sha16_arq(L.PAGINA)}, "n_unidades": len(pnp_rec), "n_limpas": sum(1 for x in pnp_rec if x["resultado"] == "LIMPO"),
                                                        "unidades": pnp_rec})
out = {"contrato": "GUARDA_v413_UNIDADES", "regra": "contrato da v413, secao 5 (a guarda da v412 herdada sem mudanca): um ponto de chamada (a travessia), unidade por unidade; zero unidade em superficie e' falha", "modo": L.MODO, "ok": e.ok, "resumo": e.resumo(),
       "checagens": e.linhas, "n_superficies": len(rec_s), "n_unidades_total": tot, "superficies": rec_s, "unidades_com_p_igual_np": [{"superficie": n, "campo": c, "tipo": ti, "inicio": tx[:90], "regras": rg} for n, c, ti, tx, rg in alvo],
       "f43": {"formas": f43.pattern, "achados": achou43}, "historia": {"verificador": "verificar_historia_texto_v413.py", "identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "autoteste": {"n": auto["n"], "n_ok": auto["n_ok"]},
                                                                        "n_unidades": hist["n_unidades_examinadas"], "achados": hist["achados"], "informativos": hist["n_informativos"]},
       "marcadores_herdados": {"recibo": "MARCADORES_HERDADOS_v413.json", "sha16": L.sha16_arq(L.D / "MARCADORES_HERDADOS_v413.json"), "n": MH["n_marcadores"]},
       "pagina": {"arquivo": str(L.PAGINA.relative_to(L.D)), "sha16": L.sha16_arq(L.PAGINA), "traducao_en": str(L.PAGINA_EN.relative_to(L.D)), "traducao_en_sha16": L.sha16_arq(L.PAGINA_EN)},
       "guarda": "a herdada da v412, carregada do um.py selado (guarda_frases_v413.py)", "candidato_no_bloco_do_handoff": bool(CAND)}
L.salvar_json(L.saida("GUARDA_v413_UNIDADES.json"), out)
L.salvar_json(L.saida("BLOCOS_TEXTO_PUBLICO_v413.json"), {"nota": "blocos NOVOS do README, do estado atual e do handoff (PT e EN), montados da pagina, desembrulhados; os marcadores herdados nao estao aqui (MARCADORES_HERDADOS_v413.json)",
                                                          "modo": L.MODO, "chaves": BL.CHAVES + (["entrega"] if CAND else []), "contagem_de_arquivos_da_pasta_quando_este_recibo_foi_gravado": N_ARQ, "blocos": BLOCOS})
print(e.resumo(), "| superficies:", len(rec_s), "| unidades:", tot, "| P=nP:", len(alvo), "| candidato no bloco do handoff:", bool(CAND))
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:400])
L.estado_bloco("4_5_guarda_e_texto_publico", e.ok, {"unidades": L.saida("GUARDA_v413_UNIDADES.json"), "p_igual_np": L.saida("GUARDA_v413_P_IGUAL_NP.json"), "blocos": L.saida("BLOCOS_TEXTO_PUBLICO_v413.json"),
                                                    "controles": L.saida("GUARDA_FRASES_v413.json"), "texto_publico": L.saida("TEXTO_PUBLICO_v413.json"), "pdflatex": L.saida("TEXTO_PUBLICO_PDFLATEX_v413.json"),
                                                    "traducao_en": L.PAGINA_EN, "marcadores_herdados": L.D / "MARCADORES_HERDADOS_v413.json", "molde_dos_marcadores": L.D / "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md"},
               nota="a guarda herdada (controles 45/45 iguais ao recibo da v412) e a travessia sobre os textos novos; no modo contrato o paragrafo da secao 2 da pagina pinada falha a F37b (PT e EN)",
               proximo="gerar_candidato_v413.py (modo proposta, enquanto a pagina pinada falha a guarda)")
sys.exit(0 if e.ok else 1)

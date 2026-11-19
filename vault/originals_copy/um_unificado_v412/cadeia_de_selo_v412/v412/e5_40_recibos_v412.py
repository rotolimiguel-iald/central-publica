# [DERIVADO v412 r5, claude-construtor-v412 (contrato R5)] copia de e4_40_recibos_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R5_PIPELINE_v412.json (derivador: e5_32_derivar_recibos_r5_v412.py). O original fica intacto.
"""R5: os recibos do texto novo da v412: a travessia sobre TODAS as superficies (os cinco registros, a secao do artigo PT/EN, o resumo PT/EN, os blocos do README, do estado atual e do handoff PT/EN), o recibo GUARDA_v412_UNIDADES.json,
a lista das unidades com “P = nP” ou o nome dos fluidos, o verificador de historia sobre toda unidade, a varredura das tres formas da F43, os 34 marcadores herdados conferidos por bytes contra o insumo, e os blocos em BLOCOS_TEXTO_PUBLICO_v412.json.
uso: C:\\Python314\\python.exe -B -X utf8 e5_40_recibos_v412.py [--contagem N]"""
import hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e5_lib_v412 import D, salvar_json, sha16_arq, Exame, ler_json
import guarda_frases_v412_r5 as GF
import verificar_historia_texto_v412_r5 as VH
import registros_v412_r5 as RG
import blocos_texto_publico_v412_r5 as BL

travessia = GF.travessia
N_ARQ = int(sys.argv[sys.argv.index("--contagem") + 1]) if "--contagem" in sys.argv else len(list(D.iterdir()))
TP = ler_json(D / "TEXTO_PUBLICO_v412.json")
CAND = ler_json(D / "CANDIDATO_v412.json") if (D / "CANDIDATO_v412.json").exists() else None
specs = RG.especs()
nomes_reg = [s["nome"] for s in specs]
superficies = []   # (nome, objeto, forma)
for s in specs:
    superficies.append(("registro:" + s["nome"], {"corpo": {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]}, "dados"))
for lg in ("pt", "en"):
    superficies.append(("artigo:" + lg, TP["tex"][lg], "tex"))
    superficies.append(("resumo:" + lg, {lg: [TP["pnp_resumo"][lg]]}, "dados"))
BLOCOS = {}
for lg in ("pt", "en"):
    b = BL.blocos_da_pagina(lg)
    BLOCOS["readme:" + lg] = dict(b); BLOCOS["estado_atual:" + lg] = dict(b)
    h = dict(b)
    if CAND:
        h["entrega"] = BL.bloco_handoff(lg, CAND, nomes_reg, N_ARQ)
    BLOCOS["handoff:" + lg] = h
for nome, obj in BLOCOS.items():
    superficies.append((nome, obj, "dados"))
e = Exame("texto_novo_v412")
rec_s = {}; todas = []   # todas: (superficie, campo, tipo, texto, regras)
for nome, obj, forma in superficies:
    t = travessia(nome, obj, forma)
    rec_s[nome] = {"n_unidades": t["n_unidades"], "ok": t["ok"], "n_violacoes": len(t["violacoes"]), "violacoes": [list(v[:3]) for v in t["violacoes"][:5]],
                   "campos": {}}
    for u in t["unidades"]:
        rec_s[nome]["campos"].setdefault(u["campo"], []).append({"tipo": u["tipo"], "inicio": u["inicio"], "regras": u["regras"]})
        todas.append((nome, u["campo"], u["tipo"], u["texto"], u["regras"]))
    e.chk("a travessia sobre a superficie %s: zero violacao e mais de zero unidades" % nome, t["ok"] and t["n_unidades"] > 0, t["n_unidades"], t["violacoes"][:2])
# unidades com P = nP ou o nome dos fluidos
alvo = [(n, c, ti, tx[:90], rg) for n, c, ti, tx, rg in todas if re.search(r"P\s*=\s*nP", tx) or re.search(r"Navier\s*(?:[–—-]{1,2}|\\textendash(?:\{\})?)?\s*Stokes", tx, re.I)]
e.chk("ha unidades com “P = nP” ou o nome dos fluidos e NENHUMA tem violacao", len(alvo) > 0 and all(not rg for *_, rg in alvo), len(alvo), [a for a in alvo if a[4]][:3])
# as tres formas da F43
f43 = re.compile(r"or[aá]culo|oracle|leitor\s+de\s+Turing|Turing\s+reader|leitor\s+que\s+devolve\s+Z|reader\s+that\s+returns\s+Z", re.I)
achou43 = [(n, c, tx[:80]) for n, c, ti, tx, rg in todas if f43.search(tx)]
e.chk("as formas da F43 (oraculo, leitor de Turing, leitor que devolve Z) nao aparecem em nenhuma unidade emitida", not achou43, len(todas), achou43[:3])
taut = [(n, c, tx[max(0, m.start() - 400):m.end() + 20]) for n, c, ti, tx, rg in todas for m in re.finditer(r"tautol|TAUTOL", tx)]
taut_sem_negacao = [t for t in taut if not re.search(r"\bn(?:ã|a)o\b|\bnot\b|\bnor\b|_NOT_|NOT_", t[2], re.I)]
e.chk("em nenhuma unidade de texto novo aparece a afirmacao de que a pergunta do Instituto e tautologica: toda mencao a tautologia vem negada", not taut_sem_negacao, len(taut), taut_sem_negacao[:3])
# historia
auto = VH.autoteste()
e.chk("o verificador de historia tem autoteste (cada classe forte detecta a sua frase plantada)", auto["ok"], auto["n"], auto["n_ok"])
hist = VH.examinar([("%s/%s" % (n, c), tx) for n, c, ti, tx, rg in todas])
e.chk("o verificador de historia nao acha nada em nenhuma unidade de texto novo", hist["ok"], hist["n_unidades_examinadas"], hist["achados"][:4])
# marcadores herdados: por bytes contra o insumo
INS = ler_json(D / "insumos" / "MARCADORES_HERDADOS_v412.json")
molde_p = Path(INS["molde"]["arquivo"]); mb = molde_p.read_bytes()
e.chk("o molde dos marcadores tem o sha256 do insumo", hashlib.sha256(mb).hexdigest() == INS["molde"]["sha256"] and len(mb) == INS["molde"]["bytes"], 1)
mt = mb.decode("utf-8")
ok_m, ruim_m = [], []
for x in INS["marcadores"]:
    m = re.search(r"<!-- INICIO_%s_v412 -->\r?\n(.*?)\r?\n<!-- FIM_%s_v412 -->" % (re.escape(x["marcador"]), re.escape(x["marcador"])), mt, re.S)
    if m and hashlib.sha256(m.group(1).encode("utf-8")).hexdigest() == x["sha256"] and len(m.group(1).encode("utf-8")) == x["bytes"]:
        ok_m.append(x["marcador"])
    else:
        ruim_m.append(x["marcador"])
e.chk("os 34 marcadores herdados estao no molde, idênticos por bytes ao insumo (nenhum retirado, nenhum reescrito)", len(ok_m) == 34 == INS["n_marcadores"] and not ruim_m, len(INS["marcadores"]), ruim_m[:5])
tot = sum(v["n_unidades"] for v in rec_s.values())
out = {"contrato": "GUARDA_v412_UNIDADES", "regra": "contrato R5, secao 5.1 (a do R4, sem mudanca): um ponto de chamada (a travessia), unidade por unidade; zero unidade em superficie e' falha", "ok": e.ok, "resumo": e.resumo(), "n_superficies": len(rec_s), "n_unidades_total": tot,
       "superficies": rec_s, "unidades_com_p_igual_np_ou_fluidos": [{"superficie": n, "campo": c, "tipo": ti, "inicio": tx, "regras": rg} for n, c, ti, tx, rg in alvo],
       "f43": {"formas": f43.pattern, "achados": achou43}, "historia": {"verificador": "verificar_historia_texto_v412_r5.py", "identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "autoteste": {"n": auto["n"], "n_ok": auto["n_ok"]}, "n_unidades": hist["n_unidades_examinadas"], "achados": hist["achados"], "informativos": hist["n_informativos"]},
       "marcadores_herdados": {"n": len(ok_m), "iguais_ao_insumo": ok_m, "diferem": ruim_m, "insumo_sha16": sha16_arq(D / "insumos" / "MARCADORES_HERDADOS_v412.json")},
       "pagina": {"arquivo": "o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md", "sha16": sha16_arq(D / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"), "traducao_en": "O_QUE_FICA_CLARO_v412_R18_EN.md", "traducao_en_sha16": sha16_arq(D / "O_QUE_FICA_CLARO_v412_R18_EN.md")},
       "guarda_fonte_sha16": sha16_arq(D / "runtime_v412_guarda.py")}
salvar_json(D / "GUARDA_v412_UNIDADES.json", out, backup=True)
salvar_json(D / "BLOCOS_TEXTO_PUBLICO_v412.json", backup=True, obj={"nota": "blocos NOVOS do README, do estado atual e do handoff (PT e EN), montados da pagina R18; os 34 marcadores herdados nao estao aqui", "contagem_esperada_de_arquivos_da_pasta": N_ARQ, "blocos": BLOCOS})
print(e.resumo(), "| superficies:", len(rec_s), "| unidades:", tot, "| P=nP/fluidos:", len(alvo))
for l in e.linhas:
    if not l["ok"]:
        print("FALHOU:", l["checagem"], l["n_itens_examinados"], str(l["detalhe"])[:400])
sys.exit(0 if e.ok else 1)

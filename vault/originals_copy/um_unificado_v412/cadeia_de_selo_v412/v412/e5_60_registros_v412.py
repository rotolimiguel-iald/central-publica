# [DERIVADO v412 r5, claude-construtor-v412 (contrato R5)] copia de e4_60_registros_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R5_PIPELINE_v412.json (derivador: e5_32_derivar_recibos_r5_v412.py). O original fica intacto.
"""R5: confere os cinco registros: veredito igual ao do contrato R5 (copiado por script); a travessia da guarda de frases da v412 sobre o corpo e o veredito de cada um (unidades > 0, zero violacao); P18; o verificador de historia;
a checagem da guarda presente em cada registro; contagem de ancoras e de checagens; grava REGISTROS_v412_RECIBO.json."""
import hashlib, json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e5_lib_v412 import D, salvar_json, sha16_arq, estado_bloco, Exame
import registros_v412_r5 as RG
import guarda_frases_v412_r5 as GF
import verificar_historia_texto_v412_r5 as VH

specs = RG.especs()
ex = Exame("registros_v412")
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
    tem_guarda = [c for c in s["checks"] if c["caminho"][:2] == ["guarda_frases_v412", nome]]
    ex.chk("%s: a palavra de veredito e' exatamente a do contrato R5 (copiada por script)" % nome, w == palavras[nome], 1, hashlib.sha256(w.encode()).hexdigest()[:16])
    ex.chk("%s: a travessia da guarda da v412 sobre o corpo e o veredito: zero violacao e mais de zero unidades" % nome, t["ok"] and t["n_unidades"] > 0, t["n_unidades"], t["violacoes"][:3])
    ex.chk("%s: a checagem da guarda esta no registro (zero violacao; unidades >= 1)" % nome, len(tem_guarda) == 2, len(tem_guarda), [c["id"] for c in tem_guarda])
    ex.chk("%s: a guarda P18 nao acha violacao no corpo" % nome, not v_p18, 1, v_p18[:3])
    ex.chk("%s: o verificador de historia nao acha nada (corpo, descricoes das checagens, estatuto)" % nome, hist["ok"], hist["n_unidades_examinadas"], hist["achados"][:3])
    ex.chk("%s: ids de checagem unicos e cada ancora tem as suas duas checagens" % nome, len(ids) == len(set(ids)) and (not s["kernel_flags"] or sum(1 for i in ids if i.startswith(("ab", "ce"))) >= len(s["kernel_flags"])), len(ids))
    ex.chk("%s: nenhum veredito proibido; o registro nao declara falas nem chama citacao de falas" % nome, not any(x in w for x in ("CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM")) and not s["verbatins"] and not s["fontes"], len(w))
    rec[nome] = {"veredito": w, "n_checagens": len(ids), "n_ancoras": len(s["kernel_flags"]), "n_decls": len(s["kernel_decls"]), "n_diz": len(s["diz"]), "n_limites": len(s["limites"]), "n_unidades_da_travessia": t["n_unidades"], "n_violacoes": len(t["violacoes"]),
                 "p18": len(v_p18), "historia_achados": hist["n_achados"], "historia_unidades": hist["n_unidades_examinadas"], "historia_identificadores_do_kernel_fora_da_prosa": hist["n_identificadores_do_kernel_fora_da_prosa"], "n_nao_diz": len(s["nao_diz"]), "usa_p_igual_np": "P = nP" in json.dumps(corpo, ensure_ascii=False)}
ex.chk("o registro leitor_da_formula_v412 nao usa a expressao P = nP (contrato R5, secao 2)", "leitor_da_formula_v412" in rec and rec["leitor_da_formula_v412"]["usa_p_igual_np"] is False, 1)
ex.chk("sao cinco registros, na ordem do contrato, e cunhagens_v412 cobra o selo dos outros quatro por ids sem forma de numero de revisao", [s["nome"] for s in specs] == RG.NOMES and len(specs) == 5 and sorted(c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")) == sorted(RG.ID_DO_SELO.values()), len(specs), [c["id"] for c in specs[-1]["checks"] if c["id"].startswith("selo_")])
out = {"contrato": "REGISTROS_v412_RECIBO", "ok": ex.ok, "resumo": ex.resumo(), "checagens": ex.linhas, "registros": rec, "n_ancoras_total": sum(r["n_ancoras"] for r in rec.values()),
       "contrato_seguido": {"arquivo": "CONTRATO_v412_R5.md", "sha16": sha16_arq(D / "CONTRATO_v412_R5.md")}, "ancoras_escolhidas": {"arquivo": "ANCORAS_ESCOLHIDAS_v412.json", "sha16": sha16_arq(D / "ANCORAS_ESCOLHIDAS_v412.json")}}
salvar_json(D / "REGISTROS_v412_RECIBO.json", out)
print("registros:", ex.resumo(), "ok" if ex.ok else "FALHA")
for l in ex.linhas:
    if not l["ok"]:
        print("  FALHOU:", l["checagem"], "|", l["n_itens_examinados"], "|", str(l["detalhe"])[:300])
sys.exit(0 if ex.ok else 1)

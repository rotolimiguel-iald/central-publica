"""Etapa 2, bloco 2: confere os quatro registros: veredito igual ao do contrato; guarda P18 e guarda de frases da v412 sobre o corpo de texto de cada um; verificador de historia; contagem de ancoras/checagens; grava REGISTROS_v412_RECIBO.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
sys.stdout.reconfigure(encoding="utf-8")
from e2_lib_v412 import D, salvar_json, sha16_arq, estado_bloco, Exame
import registros_v412 as RG
import guarda_frases_v412 as GF
import verificar_historia_texto_v412 as VH

specs = RG.especs()
ex = Exame("registros_v412")
recibo = {"registros": {}}
palavras = RG.palavras_do_contrato()
for s in specs:
    nome = s["nome"]
    w = s["veredito_prefixo"] + "__" + s["veredito_sufixo"]
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v_gf = GF.violacoes(corpo)
    v_p18 = GF.p18(corpo)
    hist = VH.examinar([("corpo", corpo)] + [("check/%s" % c["id"], c["descricao"]) for c in s["checks"]] + [("estatuto", s["estatuto"])])
    ex.chk("%s: a palavra de veredito e' exatamente a do contrato" % nome, w == palavras[nome], 1, {"palavra_sha16": __import__("hashlib").sha256(w.encode()).hexdigest()[:16]})
    ex.chk("%s: a guarda de frases da v412 nao acha violacao no corpo" % nome, not v_gf, 1, v_gf[:3])
    ex.chk("%s: a guarda P18 nao acha violacao no corpo" % nome, not v_p18, 1, v_p18[:3])
    ex.chk("%s: o verificador de historia nao acha nada (corpo, descricoes das checagens, estatuto)" % nome, hist["ok"], hist["n_unidades_examinadas"], hist["achados"][:3])
    ex.chk("%s: ha checagens e cada ancora tem as suas duas" % nome, len(s["checks"]) > 0 and (len(s["kernel_flags"]) == 0 or sum(1 for c in s["checks"] if c["id"].startswith(("ab", "ce"))) >= len(s["kernel_flags"])), len(s["checks"]))
    ex.chk("%s: tem veredito proibido ausente" % nome, not any(t in w for t in ("CONFIRMED", "PROVED_BY", "P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM")), len(w))
    recibo["registros"][nome] = {"veredito": w, "n_checagens": len(s["checks"]), "n_ancoras": len(s["kernel_flags"]), "n_decls": len(s["kernel_decls"]), "n_diz": len(s["diz"]), "n_limites": len(s["limites"]),
                                 "guarda_frases_v412": len(v_gf), "p18": len(v_p18), "historia_achados": hist["n_achados"], "historia_unidades": hist["n_unidades_examinadas"]}
ok = ex.ok
out = {"contrato": "REGISTROS_v412_RECIBO", "ok": ok, "resumo": ex.resumo(), "checagens": ex.linhas, "registros": recibo["registros"], "n_ancoras_total": sum(r["n_ancoras"] for r in recibo["registros"].values()),
       "ancoras_escolhidas": {"arquivo": "ANCORAS_ESCOLHIDAS_v412.json", "sha16": sha16_arq(D / "ANCORAS_ESCOLHIDAS_v412.json")}}
salvar_json(D / "REGISTROS_v412_RECIBO.json", out)
print("registros:", ex.resumo(), "ok" if ok else "FALHA")
for l in ex.linhas:
    if not l["ok"]:
        print("  FALHOU:", l["checagem"], "|", l["n_itens_examinados"], "|", str(l["detalhe"])[:300])
if ok:
    estado_bloco("2_registros", True, {"registros": D / "registros_v412.py", "textos": D / "textos_registros_v412.py", "recibo": D / "REGISTROS_v412_RECIBO.json", "ancoras": D / "ANCORAS_ESCOLHIDAS_v412.json"},
                 nota="quatro registros por especificacao; palavras de veredito do contrato; guardas e historia limpas", proximo="runtime_v412 + delta + gerador")
sys.exit(0 if ok else 1)

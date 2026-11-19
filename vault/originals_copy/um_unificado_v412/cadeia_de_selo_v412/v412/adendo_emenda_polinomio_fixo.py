# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: recibo AO LADO de uma emenda de comentario em OPolinomioFixoEBeta que ficou sem recibo (errata E56 da
gerencia, em nome proprio). Depois de gravar EMENDAS_DO_POLINOMIO_FIXO.json (passo2f), a gerencia corrigiu uma frase do cabecalho com a
ferramenta de edicao da sessao, conferindo o codigo identico, mas sem recibo e sem registro no diario. A copia compilada e congelada na
lista final (insumos\\pedras_r11) e' a de depois. Este script reconstroi o 'depois' do recibo a partir da fonte do autor (as mesmas
regioes e trocas do recibo, conferidas pelo sha256 que ele registrou), tira a diferenca exata contra a copia final, confere que o codigo
e' identico ao da fonte do autor nos tres estados e grava pedras_novas\\EMENDAS_DO_POLINOMIO_FIXO_ADENDO.json (nao sobrescreve).
Uso: adendo_emenda_polinomio_fixo.py [--executar]"""
import difflib, hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; R11 = V / "insumos" / "pedras_r11"; NOME = "OPolinomioFixoEBeta"
h = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()


def sem_comentarios(t):  # a mesma funcao do passo2f
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


rp = D / "EMENDAS_DO_POLINOMIO_FIXO.json"; rec = json.loads(rp.read_text(encoding="utf-8"))
orig = (O / (NOME + ".lean")).read_bytes().decode("utf-8"); t = orig
for ini, fim, novo in rec["regioes"]:
    assert t.count(ini) == 1 and t.count(fim) == 1; a, b = t.index(ini), t.index(fim); assert a < b; t = t[:a] + novo + t[b:]
for velho, novo in rec["trocas_exatas"]:
    assert t.count(velho) == 1; t = t.replace(velho, novo)
assert h(t) == rec["sha256_depois"][NOME], "a reconstrucao nao bate com o recibo"
final = (D / (NOME + ".lean")).read_bytes().decode("utf-8")
assert final.encode("utf-8") == (R11 / (NOME + ".lean")).read_bytes(), "pedras_novas e pedras_r11 diferem"
comp = json.loads((D / "build" / "COMPILACAO_NOVAS.json").read_text(encoding="utf-8"))
m = [x for x in comp["modulos"] if x["modulo"] == NOME]; assert len(m) == 1 and m[0]["sha256"] == h(final) and m[0]["rc"] == 0
assert sem_comentarios(orig) == sem_comentarios(t) == sem_comentarios(final), "codigo difere"
diff = list(difflib.unified_diff(t.split("\n"), final.split("\n"), "depois_do_recibo_passo2f", "copia_final_r11", lineterm="", n=0))
print("reconstrucao bate com o recibo (", rec["sha256_depois"][NOME][:16], ") | final", h(final)[:16], "| compilado rc 0 | codigo identico nos tres estados")
print("\n".join(diff))
if "--executar" in sys.argv:
    out = D / "EMENDAS_DO_POLINOMIO_FIXO_ADENDO.json"; assert not out.exists(), "ja' existe: nao sobrescrevo"
    out.write_bytes(json.dumps({
        "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
        "o_que_e": "recibo ao lado de uma emenda de comentario em OPolinomioFixoEBeta feita pela gerencia depois do recibo do passo2f, sem recibo na hora (errata E56 da gerencia, em nome proprio)",
        "recibo_anterior": {"arquivo": str(rp), "sha256": hashlib.sha256(rp.read_bytes()).hexdigest()},
        "antes": {"o_que_e": "o 'depois' do recibo do passo2f, reconstruido da fonte do autor pelas mesmas regioes e trocas", "sha256": h(t)},
        "depois": {"o_que_e": "a copia final, compilada e congelada na lista R11", "sha256": h(final), "compilacao": {"rc": m[0]["rc"], "reaproveitado_do_log": m[0].get("reaproveitado_do_log")}},
        "fonte_do_autor": {"arquivo": str(O / (NOME + ".lean")), "sha256": h(orig)},
        "codigo_identico_nos_tres_estados": True,
        "diferenca_unificada": diff,
    }, ensure_ascii=False, indent=1).encode("utf-8"))
    print("gravado:", out.name)

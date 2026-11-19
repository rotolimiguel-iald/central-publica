"""R7, bloco 0: confere por sha16 (lido de cada arquivo) o contrato R7 e os tres insumos que ele pina; confere a copia congelada do contrato; mede o manifesto R11 (campos, frentes, namespaces); grava o recibo e o estado R7."""
import collections, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v412 as L

D = L.D
ex = L.Exame("inicio_R7_quatro_sha16")
ESPERADO = [("CONTRATO_v412_R7.md", "482955270f39acc5"), ("insumos/MANIFESTO_PEDRAS_v412_R11.json", "63b37d347da3c2c1"), ("insumos/ANCORAS_PROPOSTAS_v412_R11.json", "cd9155b05c9dbae6"),
            ("o_que_fica_claro_REV21/O_QUE_FICA_CLARO_v412_R21.md", "629cd08a0f8f779e")]
lidos = {}
for rel, esp in ESPERADO:
    p = D / rel
    h = L.sha16_arq(p)
    lidos[rel] = {"sha16_lido": h, "sha16_esperado": esp, "bytes": p.stat().st_size, "sha256": L.sha256_arq(p)}
    ex.chk("sha16 de " + rel, h == esp, 1, {"lido": h, "esperado": esp})
    print("%-60s %s %s %s" % (rel, h, esp, "OK" if h == esp else "DIVERGE"))
cc = D / "contrato_REV7" / "CONTRATO_v412_R7.md"
ex.chk("a copia congelada do contrato (contrato_REV7) e' igual por sha256", L.sha256_arq(cc) == L.sha256_arq(D / "CONTRATO_v412_R7.md"), 1, L.sha16_arq(cc))
ex.chk("a pagina tem os 33433 bytes que o contrato da'", (D / ESPERADO[3][0]).stat().st_size == 33433, 1, (D / ESPERADO[3][0]).stat().st_size)
mh = D / "insumos" / "MARCADORES_HERDADOS_v412.json"
ex.chk("os marcadores herdados tem o sha16 do contrato", L.sha16_arq(mh) == "b67d78def8c63f64", 1, L.sha16_arq(mh))
m = L.ler_json(L.MANIFESTO)
ents = m["modulos"]
fr = collections.Counter(e.get("frente") for e in ents)
dq = collections.Counter(str(e.get("de_quem")) for e in ents)
print("frentes:", dict(fr)); print("de_quem:", dict(dq))
ex.chk("o manifesto tem 156 modulos", len(ents) == 156 == int(m["n_modulos"]), len(ents), len(ents))
ex.chk("frentes A=17, B=27, C=112", (fr.get("A"), fr.get("B"), fr.get("C")) == (17, 27, 112), len(ents), dict(fr))
ex.chk("o campo novas_em_relacao_a_oitava_lista tem 112 e o das tres pedras novas tem 3", len(m["novas_em_relacao_a_oitava_lista"]) == 112 and sorted(m["novas_em_relacao_a_decima_lista"]) == ["OCustoEAIsometria", "OPolinomioFixoEBeta", "ORazaoDoColapsoEBeta"], 115,
       [len(m["novas_em_relacao_a_oitava_lista"]), m["novas_em_relacao_a_decima_lista"]])
ex.chk("o campo mudaram_da_decima_lista tem as tres fontes emendadas so' em comentario", sorted(m["mudaram_da_decima_lista"]) == ["AClausulaExemplificativa", "AFitaEOIndice", "OPsiBitDaFormula"], 3, m["mudaram_da_decima_lista"])
a = L.ler_json(L.ANCORAS)
ex.chk("as ancoras R11 pinam o manifesto R11", a["manifesto_sha256"] == L.sha256_arq(L.MANIFESTO), 1, a["manifesto_sha256"][:16])
fontes = sorted(p.name for p in L.PEDRAS.iterdir())
print("arquivos em pedras_r11:", len(fontes), [f for f in fontes if not f.endswith(".lean")][:10], [f for f in fontes if f[0].islower()])
ex.chk("pedras_r11 tem 156 fontes .lean", sum(1 for f in fontes if f.endswith(".lean")) == 156, len(fontes), len(fontes))
rec = {"quando": L.agora(), "exame": ex.resumo(), "linhas": ex.linhas, "lidos": lidos, "frentes": dict(fr), "de_quem": dict(dq)}
L.salvar_json(D / "INICIO_R7_v412.json", rec)
print(json.dumps(ex.resumo(), ensure_ascii=False))
if not ex.ok:
    print("PARE: algum sha16 nao bate"); sys.exit(2)
L.estado_bloco("0_quatro_sha16", True, {"recibo": D / "INICIO_R7_v412.json", "lib": D / "e7_lib_v412.py", "script": D / "e7_00_conferir_inicio_v412.py"},
               nota="contrato R7 e os tres insumos conferidos por sha16 lido de cada arquivo; copia congelada igual; pedras_r11 156 fontes",
               proximo="bloco 1: derivar scripts do kernel (_r7) e reconstruir C:\\t\\k412c\\final com os 156 modulos a frio",
               falta=["1_kernel", "2_registros", "3_respostas_D224", "4_texto_publico", "5_gerador_candidato_ensaio_portoes", "6_fecho"])

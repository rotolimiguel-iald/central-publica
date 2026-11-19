"""R5, bloco 0: confere por sha16 (lido de cada arquivo) o contrato R5 e os tres insumos que ele pina; confere a copia congelada do contrato; mede o manifesto R10 (campos, frentes, namespaces); grava o recibo e o estado R5."""
import collections, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e5_lib_v412 as L

D = L.D
ex = L.Exame("inicio_R5_quatro_sha16")
ESPERADO = [("CONTRATO_v412_R5.md", "d2eaac8ca77e7f51"), ("insumos/MANIFESTO_PEDRAS_v412_R10.json", "518b593bfbf759b0"), ("insumos/ANCORAS_PROPOSTAS_v412_R10.json", "a287f91f884982bc"),
            ("o_que_fica_claro_REV18/O_QUE_FICA_CLARO_v412_R18.md", "c58564d29275ee75")]
lidos = {}
for rel, esp in ESPERADO:
    p = D / rel
    h = L.sha16_arq(p)
    lidos[rel] = {"sha16_lido": h, "sha16_esperado": esp, "bytes": p.stat().st_size, "sha256": L.sha256_arq(p)}
    ex.chk("sha16 de " + rel, h == esp, 1, {"lido": h, "esperado": esp})
    print("%-60s %s %s %s" % (rel, h, esp, "OK" if h == esp else "DIVERGE"))
cc = D / "contrato_REV5" / "CONTRATO_v412_R5.md"
ex.chk("a copia congelada do contrato (contrato_REV5) e' igual por sha256", L.sha256_arq(cc) == L.sha256_arq(D / "CONTRATO_v412_R5.md"), 1, L.sha16_arq(cc))
ex.chk("a pagina tem os 31253 bytes que o contrato da'", (D / ESPERADO[3][0]).stat().st_size == 31253, 1, (D / ESPERADO[3][0]).stat().st_size)
mh = D / "insumos" / "MARCADORES_HERDADOS_v412.json"
ex.chk("os marcadores herdados tem o sha16 do contrato", L.sha16_arq(mh) == "b67d78def8c63f64", 1, L.sha16_arq(mh))
m = L.ler_json(L.MANIFESTO)
print("chaves do manifesto:", list(m.keys()))
mods = m.get("modulos") or m.get("pedras") or m.get("lista")
print("tipo de modulos:", type(mods).__name__, "n:", len(mods))
ents = mods if isinstance(mods, list) else [dict(v, modulo=k) if "modulo" not in v else v for k, v in mods.items()]
print("exemplo:", {k: str(v)[:90] for k, v in ents[0].items()})
fr = collections.Counter(e.get("frente") for e in ents)
dq = collections.Counter(str(e.get("de_quem")) for e in ents)
print("frentes:", dict(fr)); print("de_quem:", dict(dq))
ex.chk("o manifesto tem 153 modulos", len(ents) == 153, len(ents), len(ents))
ex.chk("frentes A=17, B=27, C=109", (fr.get("A"), fr.get("B"), fr.get("C")) == (17, 27, 109), len(ents), dict(fr))
for k in ("novas_em_relacao_a_oitava_lista", "mudaram_da_nona_lista", "tudo_junto", "n_modulos"):
    v = m.get(k)
    print(k, "->", (len(v) if isinstance(v, (list, dict)) else v), (str(v)[:300] if not isinstance(v, list) else str(v[:6])))
a = L.ler_json(L.ANCORAS)
print("chaves das ancoras:", list(a.keys())[:12])
print("nota das ancoras:", str(a.get("nota"))[:1500])
regs = a["registros"]
print("registros das ancoras:", type(regs).__name__, (list(regs.keys()) if isinstance(regs, dict) else len(regs)))
for rk, rv in (regs.items() if isinstance(regs, dict) else enumerate(regs)):
    print(" registro", rk, type(rv).__name__, (list(rv.keys())[:10] if isinstance(rv, dict) else len(rv)))
    mm = rv.get("modulos") if isinstance(rv, dict) else None
    if isinstance(mm, dict):
        k0 = sorted(mm)[0]; print("   ", len(mm), "modulos; exemplo", k0, {k: str(v)[:160] for k, v in mm[k0].items()})
    elif isinstance(mm, list):
        print("   ", len(mm), "modulos; exemplo", {k: str(v)[:160] for k, v in mm[0].items()})
fontes = sorted(p.name for p in L.PEDRAS.iterdir())
print("arquivos em pedras_r10:", len(fontes), [f for f in fontes if not f.endswith(".lean")][:10], [f for f in fontes if f[0].islower()])
ex.chk("pedras_r10 tem 153 fontes .lean", sum(1 for f in fontes if f.endswith(".lean")) == 153, len(fontes), len(fontes))
rec = {"quando": L.agora(), "exame": ex.resumo(), "linhas": ex.linhas, "lidos": lidos, "frentes": dict(fr), "de_quem": dict(dq)}
L.salvar_json(D / "INICIO_R5_v412.json", rec)
print(json.dumps(ex.resumo(), ensure_ascii=False))
if not ex.ok:
    print("PARE: algum sha16 nao bate"); sys.exit(2)
L.estado_bloco("0_quatro_sha16", True, {"recibo": D / "INICIO_R5_v412.json", "lib": D / "e5_lib_v412.py", "script": D / "e5_00_conferir_inicio_v412.py"},
               nota="contrato R5 e os tres insumos conferidos por sha16 lido de cada arquivo; copia congelada igual",
               proximo="bloco 1: derivar os scripts do kernel (_r5) e reconstruir C:\\t\\k412c\\final com os 153 modulos",
               falta=["1_kernel", "2_registros", "3_respostas_D224", "4_texto_publico", "5_gerador_candidato_ensaio_portoes", "6_fecho"])

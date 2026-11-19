"""procura no core selado da v411 (base_v411\\um_absoluto.json) as chaves e os textos que os registros da v412 leem: ressalvas, juno, robustez, ato que resolve, canais vivos, gate, escada."""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
core = json.load(open(D + r"\base_v411\um_absoluto.json", encoding="utf-8"))["core"]
print("chaves de topo do core:", len(core))
padrao = re.compile(sys.argv[1] if len(sys.argv) > 1 else r"juno|robust|ressalva|reserva|ato_que|resolve", re.I)
achados = []


def walk(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            if str(k) in ("axiom_report", "declaration_sources_v394", "formal_files", "declaration_sources"):
                continue
            if padrao.search(str(k)):
                achados.append((p + "/" + str(k), type(v).__name__, (str(v)[:110] if not isinstance(v, (dict, list)) else "len=%d" % len(v))))
            walk(v, p + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o[:60]):
            walk(v, p + "[%d]" % i)


walk(core, "")
for a in achados[:80]:
    print(a)
print("n achados", len(achados))
for caminho in (["h0dn_bg1_v411", "verdict"], ["neutrino_mass", "verdict"], ["qg_closure", "gate", "verdict"], ["external_ladder", "n_theorems_expected"], ["external_ladder", "n_theorems_clean"]):
    c = core
    try:
        for k in caminho:
            c = c[k]
        print(caminho, "=", str(c)[:260])
    except Exception as e:
        print(caminho, "AUSENTE", e)

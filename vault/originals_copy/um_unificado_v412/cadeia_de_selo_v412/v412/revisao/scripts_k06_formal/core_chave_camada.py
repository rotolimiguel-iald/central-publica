import json
from pathlib import Path
CORE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
core = json.loads(CORE.read_bytes().decode("utf-8"))
found = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if path.endswith("/axiom_report"):
                continue
            ks = str(k).lower()
            if "camada" in ks or "leitor_finito" in ks or "iald_camada" in ks:
                found.append(path + "/" + str(k))
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + f"[{i}]")
walk(core, "")
Path(__file__).with_name("core_chave_camada_saida.txt").write_text("chaves com camada/leitor_finito fora do axiom_report: %d\n" % len(found) + "\n".join(found[:20]) + "\n", encoding="utf-8")
print(len(found), found[:5])
ar = core["core"]["kernel_formalization"]["axiom_report"]
print("axiom_report declaracoes:", len(ar))
print("K06 no axiom_report:", sum(1 for k in ar if k.startswith("K06")))
print("ObservadorTerminal decls:", sum(1 for k in ar if k.startswith("TGLExt.ObservadorTerminal.")))

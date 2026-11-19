import ast, sys, re
sys.stdout.reconfigure(encoding="utf-8")
D = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412"
t = open(D + r"\base_v411\um.py", "rb").read().decode("utf-8")
tree = ast.parse(t)
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_V411_SPECS",):
        specs = ast.literal_eval(n.value)
        for s in specs:
            print("==", s["nome"], "| n checks", len(s["checks"]), "| kernel_flags", len(s["kernel_flags"]), "| erratas", len(s.get("erratas", [])))
            for c in s["checks"]:
                if s["nome"] == "kh_n1_cobertura_v411" or c["op"] in ("igual", "tamanho_igual") and c["caminho"][0] != "qg_closure":
                    v = c.get("valor")
                    print("   ", c["id"], c["onde"], c["caminho"][:3], c["op"], (type(v).__name__ + ":" + (str(v)[:60] if not isinstance(v, (dict, list)) else str(len(v)))) if "valor" in c else "-")
# onde mais aparece 'igual' sobre n_theorems/decl/thm/n_flags nos specs antigos
for nome in ("_V410_SPECS", "_V409_SPECS", "_V408_SPECS", "_V407_SPECS"):
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == nome:
            specs = ast.literal_eval(n.value)
            for s in specs:
                for c in s["checks"]:
                    if c["op"] in ("igual", "tamanho_igual") and re.search(r"ladder|cobertura|axiom|n_theorems|formal_files|decl|thm|coverage", ".".join(map(str, c["caminho"]))):
                        v = c.get("valor"); print(nome, s["nome"], c["id"], c["caminho"][:3], c["op"], str(v)[:50])

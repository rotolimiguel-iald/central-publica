# r12 -- varre TODOS os specs herdados (_V3xx/_V4xx_SPECS) do candidato a procura de checagens EXATAS sobre medidas do kernel
# que mudam na v413 (constantes, teoremas, axiom_report, formal_files, escada, bandeiras, pinos). SO LEITURA.
import ast, json, os, re, sys

CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
HERE = os.path.dirname(os.path.abspath(__file__))
V412 = {"decl": 43468, "thm": 32634, "formal": 1920, "escada": 17786, "flags": 17861}
V413 = {"decl": 44676, "thm": 33340, "formal": 1941, "escada": 18498, "flags": 18573}
CAMINHOS_KERNEL = ("axiom_coverage_v392", "axiom_report", "formal_files_sha256", "external_ladder", "n_theorems", "declaration_sources", "formal_source_hash", "n_flags", "escada")


def main():
    tree = ast.parse(open(CAND, "rb").read().decode("utf-8"))
    achados = []
    nspecs = 0
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and re.match(r"^_V\d{3}_SPECS$", n.targets[0].id):
            nome = n.targets[0].id
            try:
                specs = ast.literal_eval(n.value)
            except Exception as ex:
                achados.append({"var": nome, "erro": repr(ex)[:100]}); continue
            for s in specs:
                nspecs += 1
                for c in s.get("checks", []) or []:
                    cam = c.get("caminho") or []
                    camtxt = "/".join(str(x) for x in cam)
                    op = c.get("op"); val = c.get("valor")
                    toca = any(k in camtxt for k in CAMINHOS_KERNEL)
                    num_v412 = isinstance(val, int) and not isinstance(val, bool) and val in V412.values()
                    if (toca and op in ("igual", "tamanho_igual", "menor_igual")) or num_v412:
                        achados.append({"var": nome, "registro": s.get("nome"), "id": c.get("id"), "onde": c.get("onde"), "caminho": camtxt, "op": op, "valor": val if not isinstance(val, str) else val[:80]})
    out = {"n_specs": nspecs, "n_achados": len(achados), "achados": achados}
    p = os.path.join(HERE, "r12_checagens_herdadas.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    print("specs:", nspecs, "achados:", len(achados))
    for a in achados:
        print(a)


if __name__ == "__main__":
    main()

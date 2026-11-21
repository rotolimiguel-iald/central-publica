# r13 -- confere o pino u44 (raiz) e o FORMAL_MAP contra o embutido do candidato; e o pino do KH_N1. SO LEITURA.
import ast, hashlib, json, os, sys

CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
V413 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    tree = ast.parse(open(CAND, "rb").read().decode("utf-8"))
    emb = specs411 = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
                emb = ast.literal_eval(n.value)
            elif n.targets[0].id == "_V411_SPECS":
                specs411 = ast.literal_eval(n.value)
    root = sha(emb["TGLExt.lean"].encode("utf-8"))
    u44 = [c for s in specs411 if s["nome"] == "cunhagens_v411" for c in s["checks"] if c["id"] == "u44"][0]
    print("raiz embutida:", root)
    print("u44 valor    :", u44["valor"], "IGUAL" if u44["valor"] == root else "DIFERE")
    fm = json.load(open(os.path.join(V413, "FORMAL_MAP_v413.json"), encoding="utf-8"))
    fmap = fm.get("formal_files_sha256") or fm.get("mapa") or fm
    if isinstance(fmap, dict) and "TGLExt.lean" in fmap:
        dif = [k for k, v in emb.items() if k in fmap and fmap[k] != sha(v.encode("utf-8"))]
        so_map = [k for k in fmap if k not in emb]
        print("FORMAL_MAP: n=%d ; difere do embutido: %d ; so' no mapa: %s" % (len(fmap), len(dif), so_map[:5]))
    else:
        print("FORMAL_MAP chaves:", list(fm)[:10])


if __name__ == "__main__":
    main()

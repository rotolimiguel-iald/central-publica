# r05 -- extrai _V413_SECAO (pt/en) do candidato e o resumo/topo, SO LEITURA; grava r05_secao_pt.txt e r05_secao_en.txt.
import ast, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"


def top(tree, name):
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            return n
    return None


def main():
    txt = open(CAND, "rb").read().decode("utf-8")
    tree = ast.parse(txt)
    sec = ast.literal_eval(top(tree, "_V413_SECAO").value)
    for lg in ("pt", "en"):
        p = os.path.join(HERE, "r05_secao_%s.txt" % lg)
        with open(p + ".tmp", "w", encoding="utf-8") as fh:
            for i, l in enumerate(sec[lg]):
                fh.write("[%03d] %s\n" % (i, l))
        os.replace(p + ".tmp", p)
        print(lg, len(sec[lg]))
    fn = top(tree, "_V413_FONTES")
    print("_V413_FONTES =", ast.literal_eval(fn.value))


if __name__ == "__main__":
    main()

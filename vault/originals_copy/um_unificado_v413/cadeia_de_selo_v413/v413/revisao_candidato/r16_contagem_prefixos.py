# r16 -- contagem por prefixo das chaves do kernel embutido (v412 selada x candidato) e das iguais. SO LEITURA.
import ast, collections, os, sys

BASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"


def emb(path):
    tree = ast.parse(open(path, "rb").read().decode("utf-8"))
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            return ast.literal_eval(n.value)


def pref(k):
    return k.split("/")[0] if "/" in k else "(raiz)"


def main():
    e0, e1 = emb(BASE), emb(CAND)
    c0 = collections.Counter(pref(k) for k in e0)
    c1 = collections.Counter(pref(k) for k in e1)
    iguais = collections.Counter(pref(k) for k in e0 if k in e1 and e0[k] == e1[k])
    print("v412:", dict(c0))
    print("cand:", dict(c1))
    print("iguais:", dict(iguais), "total", sum(iguais.values()))


if __name__ == "__main__":
    main()

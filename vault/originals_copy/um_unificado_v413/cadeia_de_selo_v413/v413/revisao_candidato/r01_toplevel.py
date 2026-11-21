# r01 -- revisao de terceiro do candidato v413 (SO LEITURA): compara os nomes de topo do um.py v412 selado e do candidato.
# Para cada atribuicao/def/classe de topo: linhas, sha256 do trecho. Grava r01_toplevel.json nesta pasta.
import ast, hashlib, json, os, sys, time

BASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r01_toplevel.json")


def nomes(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [node.name]
    if isinstance(node, ast.Assign):
        out = []
        for t in node.targets:
            if isinstance(t, ast.Name):
                out.append(t.id)
            elif isinstance(t, ast.Tuple):
                out += [e.id for e in t.elts if isinstance(e, ast.Name)]
        return out
    if isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def mapa(path):
    raw = open(path, "rb").read()
    txt = raw.decode("utf-8")
    lines = txt.splitlines(keepends=True)
    t0 = time.time()
    tree = ast.parse(txt)
    dt = time.time() - t0
    out = []
    for n in tree.body:
        seg = "".join(lines[n.lineno - 1:n.end_lineno])
        h = hashlib.sha256(seg.encode("utf-8")).hexdigest()
        out.append({"kind": type(n).__name__, "names": nomes(n), "l0": n.lineno, "l1": n.end_lineno, "sha16": h[:16], "nbytes": len(seg.encode("utf-8"))})
    return out, dt, hashlib.sha256(raw).hexdigest()


def main():
    b, db, hb = mapa(BASE)
    c, dc, hc = mapa(CAND)
    # chave: nomes (ou kind+indice) -- os statements sem nome comparados pela sequencia
    def chave(e, i):
        return "|".join(e["names"]) if e["names"] else None
    bn = {}
    for i, e in enumerate(b):
        k = chave(e, i)
        if k:
            bn.setdefault(k, []).append(e)
    cn = {}
    for i, e in enumerate(c):
        k = chave(e, i)
        if k:
            cn.setdefault(k, []).append(e)
    mudou, novo, sumiu, repetidos = [], [], [], []
    for k, lst in cn.items():
        if k not in bn:
            novo.append({"nome": k, "ocorrencias": [(e["l0"], e["l1"], e["kind"]) for e in lst]})
            continue
        bl = bn[k]
        if len(bl) != len(lst):
            repetidos.append({"nome": k, "base": len(bl), "cand": len(lst)})
        for eb, ec in zip(bl, lst):
            if eb["sha16"] != ec["sha16"]:
                mudou.append({"nome": k, "base_l": [eb["l0"], eb["l1"]], "cand_l": [ec["l0"], ec["l1"]], "kind": ec["kind"], "base_bytes": eb["nbytes"], "cand_bytes": ec["nbytes"]})
    for k in bn:
        if k not in cn:
            sumiu.append(k)
    # statements sem nome: comparar multiconjunto de sha16
    import collections
    sb = collections.Counter(e["sha16"] for e in b if not e["names"])
    sc = collections.Counter(e["sha16"] for e in c if not e["names"])
    sem_nome_novos = [e for e in c if not e["names"] and sc[e["sha16"]] > sb.get(e["sha16"], 0)]
    sem_nome_sumidos = [e for e in b if not e["names"] and sb[e["sha16"]] > sc.get(e["sha16"], 0)]
    res = {"base": BASE, "base_sha256": hb, "cand": CAND, "cand_sha256": hc, "parse_s": [round(db, 1), round(dc, 1)],
           "n_top_base": len(b), "n_top_cand": len(c), "mudou": mudou, "novo": novo, "sumiu": sumiu, "repetidos": repetidos,
           "sem_nome_novos": [(e["l0"], e["l1"], e["kind"]) for e in sem_nome_novos],
           "sem_nome_sumidos": [(e["l0"], e["l1"], e["kind"]) for e in sem_nome_sumidos]}
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT)
    print(json.dumps({k: res[k] for k in ("parse_s", "n_top_base", "n_top_cand", "sumiu", "repetidos", "sem_nome_novos", "sem_nome_sumidos")}, ensure_ascii=False))
    print("MUDOU:")
    for m in mudou:
        print("  ", m)
    print("NOVO:")
    for m in novo:
        print("  ", m)


if __name__ == "__main__":
    main()

# r04 -- resume as checagens de cada registro da v413 e as do kh_n1 da v412 (molde), SO LEITURA.
import ast, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
MODO = sys.argv[1] if len(sys.argv) > 1 else "checks"


def top(tree, name):
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            return n
    return None


def curto(v, n=160):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "..."


def main():
    txt = open(CAND, "rb").read().decode("utf-8")
    tree = ast.parse(txt)
    s13 = ast.literal_eval(top(tree, "_V413_SPECS").value)
    s12 = ast.literal_eval(top(tree, "_V412_SPECS").value)
    out = []
    if MODO == "checks":
        for s in s13:
            out.append("=" * 20 + " " + s["nome"] + " (%d checks)" % len(s.get("checks", [])))
            out.append("  chaves do spec: " + ", ".join(k for k in s.keys()))
            for c in s.get("checks", []):
                out.append("  [%s] %s | onde=%s caminho=%s op=%s valor=%s" % (c.get("id"), c.get("descricao", "")[:150], c.get("onde"), curto(c.get("caminho"), 90), c.get("op"), curto(c.get("valor"), 120)))
    elif MODO == "kh412":
        for s in s12:
            if s["nome"].startswith("kh_n1") or True:
                out.append("=" * 20 + " " + s["nome"] + " (%d checks) veredito=%s__%s" % (len(s.get("checks", [])), s["veredito_prefixo"], s["veredito_sufixo"][:200]))
                out.append("  fontes=%s verbatins=%s" % (s.get("fontes"), s.get("verbatins")))
                if s["nome"].startswith("kh_n1") or s["nome"].startswith("cunhagens"):
                    for c in s.get("checks", []):
                        out.append("  [%s] %s | onde=%s caminho=%s op=%s valor=%s" % (c.get("id"), c.get("descricao", "")[:150], c.get("onde"), curto(c.get("caminho"), 90), c.get("op"), curto(c.get("valor"), 120)))
    elif MODO == "texto":
        for s in s13:
            out.append("=" * 20 + " " + s["nome"])
            out.append("VEREDITO: " + s["veredito_prefixo"] + "__" + s["veredito_sufixo"])
            out.append("ESTATUTO: " + str(s.get("estatuto")))
            for k in ("diz", "nao_diz", "limites", "erratas", "leituras_do_operador"):
                for i, x in enumerate(s.get(k, []) or []):
                    out.append("  %s[%d]: %s" % (k, i, x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)))
            ex = s.get("extras", {})
            out.append("  extras: " + json.dumps(ex, ensure_ascii=False))
    p = os.path.join(HERE, "r04_%s.txt" % MODO)
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    os.replace(p + ".tmp", p)
    print(p, len(out))


if __name__ == "__main__":
    main()

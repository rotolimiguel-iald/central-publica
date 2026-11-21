# r11 -- as palavras de veredito do contrato R2 (secao 2) contra as do candidato, byte a byte. SO LEITURA.
import ast, hashlib, json, os, re, sys

V413 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    raw = open(os.path.join(V413, "CONTRATO_v413_R2.md"), "rb").read()
    print("contrato sha16:", hashlib.sha256(raw).hexdigest()[:16])
    cong = os.path.join(V413, "contrato_REV2")
    for f in sorted(os.listdir(cong)) if os.path.isdir(cong) else []:
        b = open(os.path.join(cong, f), "rb").read()
        print("  copia congelada:", f, hashlib.sha256(b).hexdigest()[:16], "== contrato" if b == raw else "DIFERE")
    txt = raw.decode("utf-8")
    # pares (registro, veredito): linha '- `nome` (...)' seguida de linha '  `VEREDITO`'
    pares = re.findall(r"^- `([a-z0-9_]+)` \([^\n]*\)\n  `([A-Z0-9_]+)`", txt, re.M)
    contrato = dict(pares)
    tree = ast.parse(open(CAND, "rb").read().decode("utf-8"))
    specs = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V413_SPECS":
            specs = ast.literal_eval(n.value)
    cand = {s["nome"]: s["veredito_prefixo"] + "__" + s["veredito_sufixo"] for s in specs}
    for k, v in contrato.items():
        print(k, "IGUAL" if cand.get(k) == v else "DIFERE", len(v))
        if cand.get(k) != v:
            print("   contrato:", v)
            print("   candidato:", cand.get(k))
    print("so' no candidato:", [k for k in cand if k not in contrato])
    print("prefixos:", {s["nome"]: s["veredito_prefixo"] for s in specs})


if __name__ == "__main__":
    main()

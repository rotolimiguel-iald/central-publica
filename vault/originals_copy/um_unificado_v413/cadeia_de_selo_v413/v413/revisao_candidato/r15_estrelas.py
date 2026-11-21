# r15 -- a regra das ancoras: toda declaracao com estrela (★ na docstring), nao private, dos modulos de cada registro esta ancorada?
# Leitura propria das fontes do sandbox (namespace/end), SO LEITURA.
import ast, json, os, re, sys

SAND = r"C:\t\k413c\final\TGLExt"
HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, "r03_specs_v413.json")
AUDIT = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413\kernel\audit.log"
REG_MODS = {"ponte_cook_levin_v413": ["PonteCookLevin", "APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral", "SimExterior", "SimCompleta", "RelogioBeta", "LeituraBeta",
                                      "QuantizacaoBeta", "Reconstrucao", "PonteLeituraBeta", "EntregaBeta", "APonteDeCookLevin", "ONomeEBeta", "SondaContagem", "AFronteiraNaLinguaClassica"],
            "trinity_v413": ["Trinity", "APropostaDaTensao"], "operador_v413": ["Operador"], "identidade_preservada_v413": ["AIdentidadePreservada"]}
RX_DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?((?:private|protected|noncomputable|nonrec|partial|unsafe)\s+)*(theorem|lemma|def|abbrev|structure|inductive|class|instance)\s+([^\s:({\[]+)")


def estrelas(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    ns = []
    out = []
    doc = None; in_doc = False; buf = []
    for l in lines:
        s = l.strip()
        if in_doc:
            buf.append(l)
            if "-/" in l:
                in_doc = False; doc = "\n".join(buf)
            continue
        if s.startswith("/--"):
            buf = [l]
            if s.endswith("-/") and len(s) > 4:
                doc = l; in_doc = False
            else:
                in_doc = True
            continue
        m = re.match(r"^namespace\s+(\S+)", s)
        if m:
            ns.append(m.group(1)); doc = None; continue
        m = re.match(r"^end\s+(\S+)", s)
        if m and ns and ns[-1] == m.group(1):
            ns.pop(); doc = None; continue
        m = RX_DECL.match(s)
        if m:
            priv = bool(m.group(1) and "private" in m.group(1))
            name = m.group(3)
            full = ".".join(ns + [name]) if not name.startswith("_root_.") else name[len("_root_."):]
            if doc and "★" in doc and not priv:
                out.append(full)
            doc = None
            continue
        if s and not s.startswith("--") and not s.startswith("open") and not s.startswith("variable") and not s.startswith("section") and not s.startswith("set_option"):
            if not s.startswith("@["):
                doc = doc if s.startswith("/-") else doc
    return out


def audit_names():
    names = set()
    rx = re.compile(r"^'(.+)' (depends on axioms|does not depend)")
    with open(AUDIT, encoding="utf-8", errors="replace") as fh:
        for l in fh:
            m = rx.match(l)
            if m:
                names.add(m.group(1))
    return names


def main():
    specs = {s["nome"]: s for s in json.load(open(SPECS, encoding="utf-8"))}
    an = audit_names()
    res = {}
    for reg, mods in REG_MODS.items():
        anc = set(specs[reg]["kernel_decls"])
        st = []
        for m in mods:
            st += [(m, n) for n in estrelas(os.path.join(SAND, m + ".lean"))]
        st_names = {n for _, n in st}
        faltam = sorted(n for n in st_names if n not in anc)
        nao_no_audit = sorted(n for n in st_names if n not in an)
        extras = sorted(n for n in anc if n not in st_names)
        res[reg] = {"n_estrelas": len(st_names), "n_ancoras": len(anc), "estrelas_sem_ancora": faltam, "estrelas_fora_do_audit(parser)": nao_no_audit[:10], "ancoras_sem_estrela(citadas pela pagina?)": extras}
    p = os.path.join(HERE, "r15_estrelas.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main()

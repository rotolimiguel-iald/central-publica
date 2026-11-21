# r07 -- le o core e o selo da v412 selada (SO LEITURA) e confere os caminhos que as checagens herdadas dos registros da v413 leem.
import ast, json, os, sys

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
HERE = os.path.dirname(os.path.abspath(__file__))


def caminho(raiz, cam):
    x = raiz
    for c in cam:
        if isinstance(x, dict) and c in x:
            x = x[c]
        elif isinstance(x, list) and isinstance(c, int) and 0 <= c < len(x):
            x = x[c]
        else:
            return False, None
    return True, x


def main():
    core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
    if isinstance(core.get("core"), dict):
        core = core["core"]
    selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
    out = {"core_top_keys_n": len(core), "core_top_keys_amostra": sorted(core.keys())[:60]}
    # onde mora o kernel_formalization / qg_closure?
    for k in ("kernel_formalization", "qg_closure", "neutrino_mass", "h0dn_bg1_v411", "external_ladder", "core"):
        out["tem_" + k] = k in core
    txt = open(CAND, "rb").read().decode("utf-8")
    tree = ast.parse(txt)
    specs = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V413_SPECS":
            specs = ast.literal_eval(n.value)
    herd = {}
    for c in specs[0]["checks"]:
        if c["id"] in ("h1", "h2", "h3", "h4", "h5", "h6", "h7"):
            if c["onde"] == "core":
                ok, v = caminho(core, c["caminho"])
            else:
                kf = core.get("kernel_formalization") or {}
                ok, v = caminho(kf, c["caminho"])
            vs = v if not isinstance(v, (dict, list)) else ("<%s %d>" % (type(v).__name__, len(v)))
            herd[c["id"]] = {"caminho": c["caminho"], "achou_no_core_v412": ok, "valor_v412": vs, "op": c["op"], "esperado": c.get("valor"),
                             "passaria_com_o_v412": (ok and ((c["op"] == "igual" and v == c.get("valor")) or (c["op"] == "verdadeiro" and v is True) or (c["op"] == "maior_igual" and isinstance(v, (int, float)) and v >= c.get("valor"))))}
    out["checagens_herdadas_contra_o_core_v412"] = herd
    out["selo_qg_closure_verdict"] = selo.get("qg_closure_verdict")
    out["selo_keys_amostra"] = sorted(selo.keys())[:80]
    rv = selo.get("registros_v412")
    out["selo_registros_v412"] = rv
    kf = core.get("kernel_formalization") or {}
    out["kf_formal_files_n"] = len(kf.get("formal_files_sha256") or {})
    out["kf_axiom_coverage"] = {k: v for k, v in (kf.get("axiom_coverage_v392") or {}).items() if not isinstance(v, (dict, list))}
    out["kf_n_axiom_report"] = len(kf.get("axiom_report") or {})
    out["external_ladder"] = {k: v for k, v in (core.get("external_ladder") or {}).items() if not isinstance(v, (dict, list))}
    out["kh_n1_cobertura_v412"] = {k: (core.get("kh_n1_cobertura_v412") or {}).get(k) for k in ("verdict", "all_verified")}
    p = os.path.join(HERE, "r07_core_v412.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    print(json.dumps(out, ensure_ascii=False, indent=1)[:9000])


if __name__ == "__main__":
    main()

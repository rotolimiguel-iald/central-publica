# r06 -- a arvore formal do Nos HOJE (so leitura), pela regra de sha256_directory do um.py, contra o embutido do candidato;
# e o que o core v412 selado registrou (formal_files_sha256). SO LEITURA.
import ast, hashlib, json, os, sys

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
ROOT = os.path.join(NOS, "tgl_kernel")
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
HERE = os.path.dirname(os.path.abspath(__file__))


def tree_files(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        if ".lake" in dp.replace("\\", "/").split("/"):
            continue
        for nm in sorted(fn):
            if nm == "ExtrairDeps.lean":
                continue
            if nm.endswith(".lean") or nm in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
                p = os.path.join(dp, nm)
                out[os.path.relpath(p, root).replace("\\", "/")] = p
    return out


def main():
    txt = open(CAND, "rb").read().decode("utf-8")
    tree = ast.parse(txt)
    emb = None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_EMBEDDED_KERNEL_FILES":
            emb = ast.literal_eval(n.value)
    tf = tree_files(ROOT)
    resid = sorted(k for k in tf if k not in emb)
    faltam = sorted(k for k in emb if k not in tf)
    res = {"n_arvore_nos_hoje": len(tf), "n_embutido_cand": len(emb), "residuais_na_arvore": resid, "embutidos_ausentes_no_nos_hoje": faltam[:40], "n_embutidos_ausentes": len(faltam),
           "esperado_depois_do_rito": len(set(tf) | set(emb))}
    # core v412 (um_absoluto.json): formal_files_sha256
    try:
        core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
        kf = core.get("kernel_formalization") or {}
        ff = kf.get("formal_files_sha256") or {}
        res["core_v412_formal_files_n"] = len(ff)
        res["core_v412_residuais"] = sorted(k for k in ff if k not in emb and not k.startswith("TGLExt/") or (k not in emb))[:20]
        res["core_v412_axiom_cov"] = kf.get("axiom_coverage_v392", {}).get("decl") if isinstance(kf.get("axiom_coverage_v392"), dict) else None
        res["core_v412_ladder"] = (core.get("external_ladder") or {}).get("n_theorems_expected")
        res["core_v412_gate"] = ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict")
        res["core_v412_neutrino"] = (core.get("neutrino_mass") or {}).get("verdict")
        res["core_v412_h0dn"] = (core.get("h0dn_bg1_v411") or {}).get("verdict")
        res["core_v412_h0dn_all_verified"] = (core.get("h0dn_bg1_v411") or {}).get("all_verified")
        res["core_v412_registros_v412"] = {k: (core.get(k) or {}).get("all_verified") for k in ("iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412", "kh_n1_cobertura_v412")}
        res["core_v412_build_s"] = kf.get("lake_build_seconds") or kf.get("build_seconds")
        res["core_v412_kf_keys_tempo"] = [k for k in kf.keys() if "second" in k or "dur" in k or "time" in k][:20]
    except Exception as ex:
        res["core_erro"] = repr(ex)
    p = os.path.join(HERE, "r06_arvore_nos.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main()

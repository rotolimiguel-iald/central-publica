# r02 -- revisao de terceiro do candidato v413 (SO LEITURA): o kernel embutido.
# (a) _EMBEDDED_KERNEL_FILES do candidato vs o da v412 selada: so' as chaves esperadas mudam/entram;
# (b) os 21 novos, o corrigido e a raiz vs o sandbox C:\t\k413c\final, byte a byte;
# (c) a raiz importa os 21; (d) o resto do sandbox (TGLExt/, TGL/) vs o embutido; (e) o manifesto e o bundle.
import ast, hashlib, json, os, re, sys

BASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
SAND = r"C:\t\k413c\final"
NOS_K = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
V413 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "r02_kernel.json")

NOVOS = ["PonteCookLevin", "APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral", "SimExterior", "SimCompleta", "RelogioBeta", "LeituraBeta",
         "QuantizacaoBeta", "Reconstrucao", "PonteLeituraBeta", "EntregaBeta", "APonteDeCookLevin", "ONomeEBeta", "SondaContagem", "AFronteiraNaLinguaClassica",
         "Trinity", "APropostaDaTensao", "Operador", "AIdentidadePreservada"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def top_dict(path, name):
    txt = open(path, "rb").read().decode("utf-8")
    tree = ast.parse(txt)
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            # ordem e linha de cada chave
            linhas = {ast.literal_eval(k): k.lineno for k in n.value.keys}
            return ast.literal_eval(n.value), linhas
    raise SystemExit("nao achei " + name)


def main():
    res = {"achados": []}
    e0, _ = top_dict(BASE, "_EMBEDDED_KERNEL_FILES")
    e1, lin1 = top_dict(CAND, "_EMBEDDED_KERNEL_FILES")
    k0, k1 = set(e0), set(e1)
    novos_k = sorted(k1 - k0)
    sumidos = sorted(k0 - k1)
    mudados = sorted(k for k in k0 & k1 if e0[k] != e1[k])
    iguais = sorted(k for k in k0 & k1 if e0[k] == e1[k])
    res["n_base"] = len(e0); res["n_cand"] = len(e1)
    res["novos"] = novos_k; res["sumidos"] = sumidos; res["mudados"] = mudados; res["n_iguais"] = len(iguais)
    esperados_novos = sorted("TGLExt/%s.lean" % m for m in NOVOS)
    res["novos_sao_os_21"] = (novos_k == esperados_novos)
    res["mudados_sao_raiz_e_corrigido"] = (mudados == sorted(["TGLExt.lean", "TGLExt/OResumoEPsiBit.lean"]))
    # ordem: os novos depois de todos os antigos?
    ordem = list(e1)
    pos = {k: i for i, k in enumerate(ordem)}
    res["novos_no_fim_do_dict"] = all(pos[k] >= len(e0) for k in novos_k)
    res["ordem_dos_antigos_preservada"] = [k for k in ordem if k in k0] == list(e0)
    # (b) sandbox byte a byte
    sb = {}
    for k in novos_k + mudados:
        p = os.path.join(SAND, k.replace("/", os.sep))
        try:
            raw = open(p, "rb").read()
        except OSError as ex:
            sb[k] = {"erro": repr(ex)}; continue
        emb = e1[k].encode("utf-8")
        sb[k] = {"linha_no_candidato": lin1.get(k), "sha256_sandbox": sha(raw), "sha256_embutido": sha(emb), "iguais": raw == emb, "bytes": len(raw), "crlf_no_sandbox": b"\r\n" in raw,
                 "print_axioms_no_embutido": len(re.findall(r"^#print axioms", e1[k], re.M))}
    res["sandbox_vs_embutido"] = sb
    res["todos_iguais_ao_sandbox"] = all(v.get("iguais") for v in sb.values())
    # corrigido: antes == o do v412 embutido? e == Nos atual?
    kc = "TGLExt/OResumoEPsiBit.lean"
    res["corrigido"] = {"sha256_v412_embutido": sha(e0[kc].encode("utf-8")), "sha256_cand_embutido": sha(e1[kc].encode("utf-8"))}
    try:
        nos_raw = open(os.path.join(NOS_K, "TGLExt", "OResumoEPsiBit.lean"), "rb").read()
        res["corrigido"]["sha256_nos_hoje"] = sha(nos_raw)
    except OSError as ex:
        res["corrigido"]["sha256_nos_hoje"] = repr(ex)
    # diferenca textual do corrigido: so' comentario/docstring?
    import difflib
    a = e0[kc].split("\n"); b = e1[kc].split("\n")
    dl = [l for l in difflib.unified_diff(a, b, lineterm="", n=0)]
    res["corrigido"]["diff"] = dl[:200]
    # (c) a raiz importa os 21
    r0 = e0["TGLExt.lean"].split("\n"); r1 = e1["TGLExt.lean"].split("\n")
    imp0 = [l for l in r0 if l.startswith("import ")]; imp1 = [l for l in r1 if l.startswith("import ")]
    acresc = [l for l in imp1 if l not in set(imp0)]
    tirados = [l for l in imp0 if l not in set(imp1)]
    res["raiz"] = {"n_import_base": len(imp0), "n_import_cand": len(imp1), "acrescentados": acresc, "tirados": tirados,
                   "acrescentados_sao_os_21": sorted(acresc) == sorted("import TGLExt.%s" % m for m in NOVOS),
                   "prefixo_igual": imp1[:len(imp0)] == imp0, "nao_import_iguais": [l for l in r0 if not l.startswith("import ")] == [l for l in r1 if not l.startswith("import ")],
                   "duplicados": len(imp1) - len(set(imp1))}
    # (d) resto do sandbox vs embutido (TGLExt/**.lean, TGL/**.lean, raiz)
    sand_files = {}
    for sub in ("TGLExt", "TGL"):
        for dp, dn, fn in os.walk(os.path.join(SAND, sub)):
            for f in fn:
                if f.endswith(".lean"):
                    rel = os.path.relpath(os.path.join(dp, f), SAND).replace(os.sep, "/")
                    sand_files[rel] = os.path.join(dp, f)
    for f in ("TGLExt.lean", "TGL.lean", "lakefile.toml", "lean-toolchain"):
        if os.path.exists(os.path.join(SAND, f)):
            sand_files[f] = os.path.join(SAND, f)
    so_sandbox = sorted(k for k in sand_files if k not in e1)
    so_embutido_lean = sorted(k for k in e1 if k.endswith(".lean") and k not in sand_files)
    difere = []
    for k, p in sand_files.items():
        if k in e1:
            if open(p, "rb").read() != e1[k].encode("utf-8"):
                difere.append(k)
    res["sandbox_resto"] = {"n_lean_sandbox": len(sand_files), "so_no_sandbox": so_sandbox[:80], "n_so_no_sandbox": len(so_sandbox),
                            "so_no_embutido_lean": so_embutido_lean[:80], "n_so_no_embutido_lean": len(so_embutido_lean), "difere_sandbox_vs_embutido": sorted(difere)[:80], "n_difere": len(difere)}
    # (e) bundle: sha256 instalado de cada modulo
    bun = json.load(open(os.path.join(V413, "PRONTO_PARA_CANDIDATO_v413.json"), encoding="utf-8"))["bundle"]["por_modulo"]
    bchk = {}
    for m in NOVOS:
        k = "TGLExt/%s.lean" % m
        bchk[m] = (bun[m]["sha256_instalado"] == sha(e1[k].encode("utf-8")))
    res["bundle_sha256_instalado_igual_ao_embutido"] = bchk
    res["todos_bundle_ok"] = all(bchk.values())
    # outros arquivos nao .lean no dict?
    res["chaves_nao_lean"] = sorted(k for k in e1 if not k.endswith(".lean"))[:40]
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT)
    resumo = {k: res[k] for k in ("n_base", "n_cand", "n_iguais", "sumidos", "mudados", "novos_sao_os_21", "mudados_sao_raiz_e_corrigido", "novos_no_fim_do_dict", "ordem_dos_antigos_preservada",
                                  "todos_iguais_ao_sandbox", "todos_bundle_ok", "corrigido", "chaves_nao_lean")}
    resumo["corrigido"] = {k: v for k, v in res["corrigido"].items() if k != "diff"}
    resumo["raiz"] = res["raiz"]
    resumo["sandbox_resto"] = res["sandbox_resto"]
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    print("DIFF do corrigido:")
    for l in res["corrigido"]["diff"]:
        print("  " + l[:300])


if __name__ == "__main__":
    main()

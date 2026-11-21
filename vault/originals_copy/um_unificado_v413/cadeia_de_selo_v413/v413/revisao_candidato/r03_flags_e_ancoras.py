# r03 -- revisao de terceiro do candidato v413 (SO LEITURA): bandeiras, escada, ledger, ancoras dos registros.
import ast, hashlib, json, os, re, sys

BASE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
V413 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413"
AUDIT = os.path.join(V413, "kernel", "audit.log")
FLAGSJ = os.path.join(V413, "kernel", "FLAGS_v413.json")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "r03_flags_e_ancoras.json")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
NOVOS = ["PonteCookLevin", "APonteAoTM2", "AMaquinaTM2DaVerificacao", "SimBase", "SimLiteral", "SimExterior", "SimCompleta", "RelogioBeta", "LeituraBeta",
         "QuantizacaoBeta", "Reconstrucao", "PonteLeituraBeta", "EntregaBeta", "APonteDeCookLevin", "ONomeEBeta", "SondaContagem", "AFronteiraNaLinguaClassica",
         "Trinity", "APropostaDaTensao", "Operador", "AIdentidadePreservada"]


def tops(path):
    txt = open(path, "rb").read().decode("utf-8")
    return txt, ast.parse(txt)


def top(tree, name):
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name:
            return n
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            return n
    return None


def ladder_list(tree):
    fn = top(tree, "prove_external_ladder")
    for n in ast.walk(fn):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets):
            return ast.literal_eval(n.value)
    return None


def audit_map():
    ax = {}; src = {}
    cur = None
    rx1 = re.compile(r"^'(.+)' depends on axioms: \[(.*)\]\s*$")
    rx2 = re.compile(r"^'(.+)' does not depend on any axioms\s*$")
    with open(AUDIT, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("TGL_DECL_SOURCE\t"):
                p = line.rstrip("\r\n").split("\t")
                if len(p) >= 3:
                    src[p[1]] = p[2]
                continue
            m = rx1.match(line)
            if m:
                ax[m.group(1)] = [a.strip() for a in m.group(2).split(",") if a.strip()]
                continue
            m = rx2.match(line)
            if m:
                ax[m.group(1)] = []
    return ax, src


def main():
    res = {}
    t0, tr0 = tops(BASE)
    t1, tr1 = tops(CAND)
    f0 = ast.literal_eval(top(tr0, "_LEAN_THEOREM_FLAGS").value)
    f1 = ast.literal_eval(top(tr1, "_LEAN_THEOREM_FLAGS").value)
    old_same = all(k in f1 and f1[k] == v for k, v in f0.items())
    new_keys = [k for k in f1 if k not in f0]
    res["flags"] = {"n_base": len(f0), "n_cand": len(f1), "n_novas": len(new_keys), "antigas_iguais": old_same,
                    "novas_no_fim": list(f1)[len(f0):] == new_keys}
    # padrao do prefixo
    pref = {m.lower(): m for m in NOVOS}
    rxk = re.compile(r"^ext_([a-z0-9]+)_413_(\d{4})$")
    mal = []; por_mod = {}
    for k in new_keys:
        m = rxk.match(k)
        if not m or m.group(1) not in pref:
            mal.append(k); continue
        por_mod.setdefault(pref[m.group(1)], []).append(k)
        if not f1[k].startswith("TGLExt.") and not f1[k].startswith("Codex."):
            pass
    res["flags"]["chaves_fora_do_padrao"] = mal
    res["flags"]["por_modulo"] = {m: len(v) for m, v in por_mod.items()}
    res["flags"]["modulos_sem_bandeira"] = [m for m in NOVOS if m not in por_mod]
    # FLAGS_v413.json
    fj = json.load(open(FLAGSJ, encoding="utf-8"))
    fl = [(a[0], a[1]) for a in fj["flags"]]
    res["flags"]["igual_ao_FLAGS_v413_json"] = ([(k, f1[k]) for k in new_keys] == fl)
    # auditoria
    ax, src = audit_map()
    res["audit"] = {"n_axiom": len(ax), "n_src": len(src)}
    fora = []; ausentes = []; modulo_errado = []; privados = []
    for k in new_keys:
        n = f1[k]
        if n.startswith("_private") or ".private" in n:
            privados.append(n)
        if n not in ax:
            ausentes.append((k, n)); continue
        if not set(ax[n]) <= TRIO:
            fora.append((k, n, ax[n]))
        mm = re.match(r"^ext_([a-z0-9]+)_413_", k).group(1)
        smod = src.get(n)
        if smod != "TGLExt." + pref.get(mm, "?"):
            modulo_errado.append((k, n, smod))
    res["flags"]["valores_ausentes_do_audit"] = ausentes
    res["flags"]["valores_fora_do_trio"] = fora
    res["flags"]["valor_de_outro_modulo"] = modulo_errado[:20]
    res["flags"]["n_valor_de_outro_modulo"] = len(modulo_errado)
    res["flags"]["privados"] = privados
    # todas as declaracoes dos 21 modulos no trio?
    dec_novos = [n for n, m in src.items() if m in {"TGLExt." + x for x in NOVOS}]
    res["audit"]["decl_dos_21"] = len(dec_novos)
    res["audit"]["decl_dos_21_fora_do_trio"] = [n for n in dec_novos if not set(ax.get(n, ["?"])) <= TRIO][:20]
    res["audit"]["sorryAx_no_audit"] = sum(1 for v in ax.values() if "sorryAx" in v)
    res["audit"]["fora_do_trio_total"] = sum(1 for v in ax.values() if not set(v) <= TRIO)
    # escada
    l0 = ladder_list(tr0); l1 = ladder_list(tr1)
    res["escada"] = {"n_base": len(l0), "n_cand": len(l1), "prefixo_igual": l1[:len(l0)] == l0, "novas_sao_as_bandeiras_novas_na_ordem": l1[len(l0):] == new_keys,
                     "duplicadas": len(l1) - len(set(l1)), "todas_no_dict": all(x in f1 for x in l1)}
    # ledger
    e0 = ast.literal_eval(top(tr0, "_ESQUELETO_STONES").value)
    e1 = ast.literal_eval(top(tr1, "_ESQUELETO_STONES").value)
    res["ledger"] = {"n_base": len(e0), "n_cand": len(e1), "prefixo_igual": e1[:len(e0)] == e0, "novos": e1[len(e0):]}
    ok_led = sorted(x[2] for x in e1[len(e0):]) == sorted("TGLExt/%s.lean" % m for m in NOVOS)
    res["ledger"]["novos_sao_os_21"] = ok_led
    # ancoras dos registros
    specs = ast.literal_eval(top(tr1, "_V413_SPECS").value)
    anc = {}
    for s in specs:
        kf = s.get("kernel_flags", []); kd = s.get("kernel_decls", [])
        a_aus = [d for d in kd if d not in ax]
        a_fora = [d for d in kd if d in ax and not set(ax[d]) <= TRIO]
        kf_nao_flag = [x for x in kf if x not in f1]
        kf_nao_nova = [x for x in kf if x not in new_keys]
        # cada flag e' de uma decl ancorada?
        kd_set = set(kd)
        flag_sem_decl = [x for x in kf if f1.get(x) not in kd_set]
        decl_sem_flag = [d for d in kd if d not in {f1.get(x) for x in kf}]
        mods = sorted({src.get(d) for d in kd})
        anc[s["nome"]] = {"n_flags": len(kf), "n_decls": len(kd), "decls_ausentes_do_audit": a_aus, "decls_fora_do_trio": a_fora, "flags_inexistentes": kf_nao_flag,
                          "flags_que_nao_sao_novas": kf_nao_nova, "flag_sem_decl": flag_sem_decl, "decl_sem_flag": decl_sem_flag, "modulos_das_decls": mods,
                          "fontes": s.get("fontes", []), "verbatins": s.get("verbatins", []), "n_checks": len(s.get("checks", [])),
                          "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]}
    res["ancoras"] = anc
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, OUT)
    # specs inteiros para leitura
    sp = os.path.join(HERE, "r03_specs_v413.json")
    with open(sp + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(specs, fh, ensure_ascii=False, indent=1)
    os.replace(sp + ".tmp", sp)
    p = dict(res); p["ledger"] = {k: v for k, v in res["ledger"].items() if k != "novos"}
    print(json.dumps(p, ensure_ascii=False, indent=1)[:12000])


if __name__ == "__main__":
    main()

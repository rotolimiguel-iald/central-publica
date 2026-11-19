# -*- coding: utf-8 -*-
# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R5)] copia de pos_build_kernel_v412_c4.py para a DECIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R10.json, insumos\pedras_r10; 153 modulos); e5_02_derivar_scripts_r5_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de pos_build_kernel_v412_r4.py para a DECIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R10.json, insumos\pedras_r10; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r4, 17/11/2026, claude-construtor-v412 (Etapa 2, bloco 0)] copia de pos_build_kernel_v412_r3.py (que fica intacto) com a CAUSA da checagem vazia corrigida (prefixo dos nomes de o_lake_recompila; conta de itens examinados; zero itens = falha); derivador: e2_01_derivar_pos_build_r4_v412.py.
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de pos_build_kernel_v412_r2.py para a DECIMA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R10.json, insumos\pedras_r10); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de pos_build_kernel_v412.py para a DECIMA lista (40 modulos): le insumos\MANIFESTO_PEDRAS_v412_R10.json; a arvore so-fontes da Etapa 1 e' movida, nao apagada. O resto e' identico (derivar_scripts_etapa1_r2_v412.py).
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v410\pos_build_kernel_v410.py (bundle de 2 modulos) para o bundle de N modulos da v412 (lidos de BUNDLE_v412.json), sem delta:
# as constantes vem dos arquivos do preparo (BUNDLE_v412.json, kernel_modulos_novos_v412.json, kernel\ULTIMA_INSTALACAO_v412.json) e da base v411 selada (base_v411\, copia de bytes do Nos)
"""pos_build_kernel_v412.py -- DEPOIS de construir_kernel_v412.sh (build POR MODULO, na ordem topologica, dos modulos novos de TGLExt/ no sandbox C:\\t\\k412c\\final; depois o build inteiro e o Audit):
(1) le as marcas; se o build PAROU num modulo, registra o modulo e as linhas de erro do bloco dele no log e sai 1 (nada se conserta: nem o kernel, nem a prova, nem o log);
(2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully' em cada invocacao, linha BUILT dos modulos que este build tinha de compilar,
da raiz (TGLExt) e do Audit (TGL.Audit), cabecalho dos .olean = Lean 4.31.0) e conta os AVISOS POR MODULO (linhas `warning: TGLExt/<Nome>.lean:` no bloco Built do modulo; o aviso conhecido e
preexistente da TowerWedgeIndex, a tatica `change` que nao faz nada, e' REGISTRADO, nao consertado);
(3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v411 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, por ast de
base_v411\\um.py), confere as ANCORAS (os #print axioms retirados de cada fonte, resolvidos pela pilha de namespace da linha) e deriva FLAGS_v412.json (as declaracoes NOMEADAS publicas dos
modulos novos, politica da v394: UMA serie por modulo, ext_<modulo em minusculas>_412_NNNN, ordenada por nome; os modulos na ordem do bundle; os PREFIXOS sao proposta do construtor e a gerencia
pode troca'-los antes do candidato: nenhuma chave antiga muda);
(4) confere que NENHUMA chave antiga muda de literal (toda chave de _LEAN_THEOREM_FLAGS da base segue apontando para um nome que existe, no trio, com a MESMA lista de axiomas) e que nada da v411 se perde;
(5) copia a ARVORE so-fontes para C:\\t\\k412c\\arvore e varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v411 (por ast);
(6) escreve KH_N1_v412.json, KERNEL_RECIBO_v412.json (contrato KERNEL_RECIBO_R3_2: uma entrada por modulo do bundle, com formal_files_antes, nos_kernel_impressao, lake_version e a arvore SEM juncao),
vinculo/CRITERIOS_v412.json, kernel/POS_BUILD_v412.json, kernel/FLAGS_v412.json e kernel/LOGS_COPIADOS_v412.json.
Fail-closed: cada checagem e' um sinal; falha e' REGISTRADA; saida existente ganha backup de BYTES (.bak_<data>) antes de ser substituida; escrita por temporario + os.replace.
Uso: C:\\Python314\\python.exe -I -B -X utf8 pos_build_kernel_v412.py"""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, traceback, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel"); VD = os.path.join(HERE, "vinculo")
KB = os.path.join("C:" + os.sep, "t", "k412c", "final"); ARV = os.path.join("C:" + os.sep, "t", "k412c", "arvore")
BASE = os.path.join(HERE, "base_v411")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
AUX_CLASSES = (("proof_simp_match_sunfold", re.compile(r"_proof_\d+(?:_\d+)*|_simp_\d+(?:_\d+)*|match_\d+|_sunfold")), ("eq", re.compile(r"eq_\d+|eq_def")), ("congr_simp", re.compile(r"congr_simp")))   # (a politica da v394, igual ao delta_v397)
MOD_AVISO_CONHECIDO = "TGLExt.TowerWedgeIndex"   # (ordem da Etapa 1, item 3: o aviso preexistente numa dependencia do Codex, uma tatica `change` que nao faz nada: registrar, nao consertar)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
abs_fw = lambda p: p.replace(os.sep, "/")
sinais = []
BACKUPS = []


def classe(nome):
    ultimo = nome.split(".")[-1]
    for c, rx in AUX_CLASSES:
        if rx.fullmatch(ultimo):
            return c
    return "nomeada"


def chk(nome, cond, det=None, informativo=False):
    s = {"checagem": nome, "ok": bool(cond), "detalhe": det}
    if informativo:
        s["informativo"] = True
    sinais.append(s)
    print(("OK   " if cond else ("INFO-FALHA" if informativo else "FALHA")), nome, "" if det is None else "-> " + str(det)[:240])
    return bool(cond)


def norm(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", t)
    return "".join(ch for ch in unicodedata.normalize("NFKC", t) if unicodedata.category(ch) != "Cf")


def salvar(path, dados):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        bak = path + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        n = 0
        while os.path.exists(bak):
            n += 1; bak = path + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_%d" % n
        shutil.copyfile(path, bak)
        assert rd(bak) == rd(path), ("o backup nao e' copia de bytes", bak)
        BACKUPS.append(bak)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(dados)
    assert os.path.getsize(tmp) == len(dados), ("escrita truncada", path)
    os.replace(tmp, path)
    assert os.path.getsize(path) == len(dados)


def salvar_json(path, obj):
    salvar(path, json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))


RX_HDR = re.compile(r"^(?:\S+\s+)?\[\d+/\d+\]\s+(Built|Replayed|Building|Running|Fetching|Checking)\s+(\S+)(?:\s+\((\d+(?:\.\d+)?)(ms|s)\))?")


def blocos_do_log(LB):
    """[(estado, modulo, segundos, [linhas do bloco])]: um bloco por linha de job do lake, ate' a linha de job seguinte (ou o marcador `=== `)."""
    out = []; cur = None
    for ln in LB.split("\n"):
        m = RX_HDR.match(ln)
        if m:
            secs = (float(m.group(3)) * (0.001 if m.group(4) == "ms" else 1.0)) if m.group(3) else None
            cur = [m.group(1), m.group(2), secs, []]; out.append(cur); continue
        if ln.startswith("=== ") or ln.startswith("Build completed") or ln.startswith("Some required targets"):
            cur = None; continue
        if cur is not None:
            cur[3].append(ln)
    return out


SO_BUILT = "--so-built" in sys.argv
CONTROLE_POSITIVO = "--controle-positivo" in sys.argv


def exigidos_built(ult_, newmods_):
    """(exigidos, fora_do_bundle, extras): os modulos de o_lake_recompila com o prefixo TGLExt. normalizado, os nomes que NAO sao modulo do bundle e as duas entradas que nao sao modulo (raiz e Audit)."""
    exig_, fora_, extras_ = set(), [], []
    for m_ in ult_.get("o_lake_recompila", []):
        if m_ in ("TGLExt (raiz)", "TGL.Audit"):
            extras_.append(m_); continue
        nome_ = m_ if m_.startswith("TGLExt.") else "TGLExt." + m_
        if nome_ in newmods_:
            exig_.add(nome_)
        else:
            fora_.append(m_)
    return exig_, fora_, extras_


def checa_built(exig_, fora_, modo_):
    """(ok, faltam, n_examinados): ok so' com n_examinados > 0, nenhum nome fora do bundle e todos os exigidos com linha Built."""
    faltam_ = sorted(m_ for m_ in exig_ if modo_.get(m_) != "Built")
    return (len(exig_) > 0 and not fora_ and not faltam_), faltam_, len(exig_)


def principal():
    os.makedirs(KD, exist_ok=True); os.makedirs(VD, exist_ok=True)
    marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
    if not re.search(r"(?m)^fim .*$", marcas):
        print("ABORTA: construir_marcas.txt nao tem a linha `fim`: o build ainda nao terminou; nada foi escrito."); sys.exit(3)
    rb = int(re.search(r"rc_build=(\d+)", marcas).group(1)); ra = int(re.search(r"rc_audit=(\d+)", marcas).group(1))
    ini = re.search(r"^inicio (.*)$", marcas, re.M).group(1); fim = re.search(r"^fim (.*)$", marcas, re.M).group(1)
    mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
    por_mod_marcas = {m: {"rc": int(r), "s": int(s)} for m, r, s in re.findall(r"^modulo=(\S+) rc=(\d+) s=(\d+)$", marcas, re.M)}
    parou = re.search(r"^parou_em=(\S+)$", marcas, re.M)
    LB_RAW = rd(os.path.join(KD, "lake_build.log")).decode("utf-8"); AL_RAW = rd(os.path.join(KD, "audit.log")).decode("utf-8")
    LB = norm(LB_RAW); AL = norm(AL_RAW)
    BDL = json.load(open(os.path.join(HERE, "BUNDLE_v412.json"), encoding="utf-8"))
    BL = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v412.json"), encoding="utf-8"))
    ULT = json.load(open(os.path.join(KD, "ULTIMA_INSTALACAO_v412.json"), encoding="utf-8"))
    MAN = json.load(open(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R10.json"), encoding="utf-8"))
    nov = list(BL["novos"]); NEWRELS = set(nov); NEWMODS = [p[:-len(".lean")].replace("/", ".") for p in nov]; N_NOVOS = len(nov)
    BUNDLE_POR_REL = {b["rel"]: b for b in BDL["modulos"]}
    chk("a lista dos modulos novos (kernel_modulos_novos_v412.json) == a do BUNDLE_v412.json == n_modulos do manifesto, sem repeticao, na ordem topologica",
        N_NOVOS == BDL["n"] == int(MAN["n_modulos"]) == len(set(nov)) and [b["rel"] for b in BDL["modulos"]] == nov and BDL.get("manifesto_sha256") == sha(rd(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R10.json"))),
        [N_NOVOS, BDL["n"], MAN["n_modulos"]])
    blocos = blocos_do_log(LB)
    # ------------------------------------------------------------------ o build parou num modulo: registra e sai (nada se conserta)
    if parou or rb != 0:
        mod_ = parou.group(1) if parou else None
        erros_mod = []
        for st, md, s_, L in blocos:
            if md == mod_ or (mod_ is None and st == "Building"):
                erros_mod += [l for l in L if l.startswith("error:") or ": error:" in l][:40]
        erro_txt = []
        if mod_:
            i0 = LB.find("=== MODULO " + mod_)
            erro_txt = LB[i0:i0 + 20000].split("\n")[:300] if i0 >= 0 else []
        chk("o build NAO parou em modulo nenhum (rc_build=0)", False, {"parou_em": mod_, "rc_build": rb, "erros": erros_mod[:10]})
        salvar_json(os.path.join(KD, "POS_BUILD_v412.json"), {"ok": False, "parou_em": mod_, "rc_build": rb, "rc_audit": ra, "por_modulo_marcas": por_mod_marcas, "erros_do_modulo": erros_mod,
                                                              "trecho_do_log_do_modulo": erro_txt, "sinais": sinais, "inicio": ini, "fim": fim, "backups": BACKUPS,
                                                              "nota": "o build parou: nada foi consertado (nem prova, nem nome); o Audit nao rodou; relatar o erro exato a gerencia"})
        print("\nPOS-BUILD: PAROU no modulo", mod_, "| rc_build", rb, "| erros:", erros_mod[:5]); return False
    # ------------------------------------------------------------------ a base (v411 selada)
    um_b = rd(os.path.join(BASE, "um.py")); um_src = um_b.decode("utf-8"); tree = ast.parse(um_src)
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    _des = open(os.path.join(HERE, "DESENHO_v412.md"), "rb").read().decode("utf-8")
    _mb = re.search(r"Base: a v411 selada \(`um\.py` do N[oó]s, sha16 `([0-9a-f]{16})`", _des)
    chk("a base_v411\\um.py e' a v411 SELADA (sha16 do DESENHO_v412 da gerencia, lido do arquivo)", bool(_mb) and sha(um_b)[:16] == _mb.group(1), [sha(um_b)[:16], _mb.group(1) if _mb else None])
    _ns = {"re": re}
    for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
        exec(compile(ast.get_source_segment(um_src, fn[nome]), "<base_v411:%s>" % nome, "exec"), _ns)
    parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
    core0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]; axr0 = core0["kernel_formalization"]["axiom_report"]
    cov0 = core0["kernel_formalization"].get("axiom_coverage_v392") or {}
    E0 = int(core0["external_ladder"]["n_theorems_expected"])
    # ------------------------------------------------------------------ o build
    chk("rc do lake build == 0 e rc do Audit == 0 (marcas: rc=0); nenhum modulo parou", rb == 0 and ra == 0 and bool(re.search(r"(?m)^rc=0$", marcas)) and not parou, [rb, ra])
    chk("as marcas trazem UMA linha por modulo novo, todas com rc 0, na ordem do bundle", [m for m in por_mod_marcas] == NEWMODS and all(v["rc"] == 0 for v in por_mod_marcas.values()), [len(por_mod_marcas), N_NOVOS])
    RE_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u201c\"]sorry|\bsorryAx\b", re.I)
    n_err = len(re.findall(r"(?m)^error:|: error:", LB + "\n" + AL)); n_sorry = len(RE_SORRY.findall(LB + "\n" + AL)) + len(RE_SORRY.findall(re.sub(r"\s+", " ", LB + "\n" + AL)))
    chk("zero erro; zero sorry/sorryAx (formas: crase, aspas, sorryAx; com e sem quebra)", n_err == 0 and n_sorry == 0, [n_err, n_sorry])
    jobs = {}
    for st, md, s_, L in blocos:
        jobs.setdefault(md, []).append((st, s_))
    n_inv = LB.count("=== MODULO ") + LB.count("=== BUILD INTEIRO")
    n_ok = len(re.findall(r"(?m)^[ \t]*Build completed successfully\b", LB))
    chk("'Build completed successfully' em CADA invocacao do lake (%d por modulo + 1 do build inteiro)" % N_NOVOS, n_inv == N_NOVOS + 1 and n_ok == n_inv, [n_inv, n_ok])
    modo = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in NEWMODS}
    exig_built, fora_do_bundle, extras_raiz_audit = exigidos_built(ULT, NEWMODS)
    ok_built, faltam_built, n_exame_built = checa_built(exig_built, fora_do_bundle, modo)
    chk("os modulos que ESTE build tinha de compilar (kernel\\ULTIMA_INSTALACAO_v412.json, o_lake_recompila): %d EXAMINADOS (zero examinados e' falha; nomes sem o prefixo TGLExt. normalizados; raiz e Audit conferidos a parte: %s) tem linha Built (a frio); %d modulos novos com Built neste log" % (n_exame_built, extras_raiz_audit, sum(1 for v in modo.values() if v == "Built")),
        ok_built, {"examinados": n_exame_built, "sem_Built": faltam_built[:8], "fora_do_bundle": fora_do_bundle[:8]})
    if CONTROLE_POSITIVO or SO_BUILT:
        c1 = checa_built(exig_built | {"TGLExt.NomeQueNaoTemLinhaBuilt"}, fora_do_bundle, {**modo, "TGLExt.NomeQueNaoTemLinhaBuilt": None})
        c2 = checa_built(set(), [], modo)
        c3 = checa_built({m for m in exig_built}, fora_do_bundle, {**modo, next(iter(exig_built)): "Replayed"} if exig_built else modo)
        c4 = checa_built(exig_built, ["NomeDesconhecido"], modo)
        controles = [
            {"controle": "um nome exigido sem linha Built faz a checagem falhar", "falhou_como_devia": (c1[0] is False), "faltam": c1[1][:3], "examinados": c1[2]},
            {"controle": "zero itens exigidos faz a checagem falhar (nao passa vazia)", "falhou_como_devia": (c2[0] is False), "examinados": c2[2]},
            {"controle": "um exigido que so' teve linha Replayed faz a checagem falhar", "falhou_como_devia": (c3[0] is False), "faltam": c3[1][:3], "examinados": c3[2]},
            {"controle": "um nome fora do bundle em o_lake_recompila faz a checagem falhar", "falhou_como_devia": (c4[0] is False), "examinados": c4[2]},
            {"controle": "a checagem real (com a lista de verdade) passa e examinou mais de zero itens", "falhou_como_devia": False, "passou": ok_built, "examinados": n_exame_built, "ok": bool(ok_built and n_exame_built > 0)},
        ]
        todos_ok = all(c.get("falhou_como_devia") for c in controles[:4]) and controles[4]["ok"]
        rec = {"ok": bool(todos_ok), "n_controles": len(controles), "controles": controles, "exigidos_examinados": sorted(exig_built), "n_exigidos_examinados": n_exame_built,
               "raiz_e_audit": extras_raiz_audit, "modo": ("controle-positivo" if CONTROLE_POSITIVO else "so-built"),
               "nota": "o_lake_recompila lido de kernel/ULTIMA_INSTALACAO_v412.json; os logs lidos de kernel/lake_build.log (build da decima lista); nada alem deste recibo foi escrito"}
        salvar_json(os.path.join(KD, "BUILT_CHECAGEM_CORRIGIDA_R5_v412.json"), rec)
        print("\nMODO %s: %d controles, todos como devem: %s; examinados na checagem real: %d" % (rec["modo"], len(controles), todos_ok, n_exame_built))
        return bool(todos_ok and ok_built)
    todos_a_frio = all(v == "Built" for v in modo.values())
    chk("(informativo) TODOS os %d modulos novos foram compilados neste build (a frio, como o do rito)" % N_NOVOS, todos_a_frio, {k: v for k, v in modo.items() if v != "Built"}, informativo=True)
    built_raiz = any(st == "Built" for st, _ in jobs.get("TGLExt", [])); built_audit = any(st == "Built" for st, _ in jobs.get("TGL.Audit", []))
    chk("a raiz (TGLExt) e o Audit (TGL.Audit) foram COMPILADOS neste build (linha Built)", built_raiz and built_audit, [built_raiz, built_audit])
    tempos = {m: next((s_ for st, s_ in jobs.get(m, []) if st == "Built" and s_ is not None), None) for m in NEWMODS}
    build_s_soma = round(sum(v for v in tempos.values() if v), 3); build_s_max = max([v for v in tempos.values() if v] or [0])
    # os AVISOS por modulo: as linhas `warning: TGLExt/<Nome>.lean:` do bloco Built do proprio modulo (o Replayed de outro build repete o aviso; nao se conta duas vezes)
    avisos = {}
    for st, md, s_, L in blocos:
        if md in NEWMODS and st in ("Built", "Replayed") and (st == "Built" or md not in avisos):   # (r2: o modulo que o build nao recompilou mostra o aviso no bloco Replayed; o bloco Built manda)
            rel_ = md.replace(".", "/") + ".lean"
            ws = [l for l in L if l.startswith("warning:")]
            avisos[md] = {"n": len(ws), "do_proprio_arquivo": sum(1 for l in ws if l.startswith("warning: " + rel_ + ":")), "linhas": ws[:20]}
    for m in NEWMODS:
        avisos.setdefault(m, {"n": 0, "do_proprio_arquivo": 0, "linhas": [], "nota": "sem bloco Built nem Replayed neste log (sem mensagem)" if modo.get(m) is None else None})
    av_conhecido = avisos.get(MOD_AVISO_CONHECIDO, {})
    conhecido_ok = av_conhecido.get("n", 0) >= 1 and all(("change" in l or "never executed" in l or "does nothing" in l or "unused" in l.lower()) for l in av_conhecido.get("linhas", []))
    outros = {m: v["n"] for m, v in avisos.items() if v["n"] and m != MOD_AVISO_CONHECIDO}
    chk("(informativo) avisos: o conhecido e preexistente da TowerWedgeIndex (registrado, nao consertado); nenhum outro modulo novo com aviso", not outros, {"TowerWedgeIndex": av_conhecido.get("linhas", [])[:3], "outros": outros}, informativo=True)
    LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
    hdr = {}
    for m in NEWMODS + ["TGLExt", "TGL.Audit"]:
        p = os.path.join(LIBL, *m.split(".")) + ".olean"
        h = rd(p)[:96] if os.path.exists(p) else b""
        hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
    hashes_lean = sorted({v[1] for v in hdr.values() if v[1]})
    chk("cabecalho de TODO .olean (%d novos + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean" % N_NOVOS, all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean, [m for m, v in hdr.items() if not v[0]][:3]])
    # ------------------------------------------------------------------ o log do Audit (so' ele) com as funcoes do um.py v411 selado
    ax = parse_ax(AL_RAW); src = parse_src(AL_RAW)
    chk("parse_lean_axioms_v394 e parse_lean_provenance_v394 sobre o log do Audit: sem erro", ax["ok"] and src["ok"], [ax["errors"][:3], src["errors"][:3]])
    axm, srcm = ax["axioms"], src["sources"]
    fora = {k: v for k, v in axm.items() if not set(v) <= TRIO}
    chk("todo axioma lido no log do Audit esta no trio (propext, Classical.choice, Quot.sound)", not fora and len(axm) > 0, [len(axm), list(fora)[:3]])
    chk("a palavra sorryAx NAO aparece no log do Audit (nem no lake build)", ("sorryAx" not in AL) and ("sorryAx" not in LB), [AL.count("sorryAx"), LB.count("sorryAx")])
    m_cov = re.search(r"TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)", AL)
    kh_cov = [int(x) for x in m_cov.groups()] if m_cov else None
    chk("KH-N1: linha TGL_AXIOM_COVERAGE_TOTAL presente, fora_do_trio=0", bool(m_cov) and kh_cov[2] == 0, kh_cov)
    chk("KH-N1: uma linha de axiomas e uma de proveniencia por constante (TOTAL.decl == #axiom_report == #TGL_DECL_SOURCE)", bool(m_cov) and kh_cov[0] == len(axm) == len(srcm), [kh_cov, len(axm), len(srcm)])
    chk("proveniencia e axiom_report cobrem EXATAMENTE os mesmos nomes", set(axm) == set(srcm), [len(set(axm) ^ set(srcm))])
    cov_b = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\n]*", LB); cov_a = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\n]*", AL)
    chk("a linha de cobertura do lake build (o TGL.Audit compilado no build inteiro) e a do audit.log sao a mesma", bool(cov_b) and cov_b[-1:] == cov_a, [cov_b[-1:], cov_a[:1]])
    # ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v411 selado + os imports
    nos_root = rd(os.path.join(NOS, "tgl_kernel", "TGLExt.lean")); nos_aud = rd(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"))
    sb_root = rd(os.path.join(KB, "TGLExt.lean")); sb_aud = rd(os.path.join(KB, "TGL", "Audit.lean"))
    chk("a raiz do sandbox == a raiz do Nos (v411 selada) + os %d imports do bundle (ROOT_SUFFIX), em bytes" % N_NOVOS, sb_root == nos_root + BL["root_suffix"].encode("utf-8"), [len(sb_root), len(nos_root), len(BL["root_suffix"])])
    chk("o Audit do sandbox == o Audit do Nos (bytes): o Audit NAO muda na v412 (o run_cmd do KH-N1 cobre toda constante de TGL e TGLExt)", sb_aud == nos_aud, [len(sb_aud), len(nos_aud)])
    # ------------------------------------------------------------------ as ANCORAS (os #print axioms retirados de cada fonte, resolvidos pela pilha de namespace da linha)
    anc_res = {}; anc_bad = []
    for rel in nov:
        mod = rel[:-len(".lean")].replace("/", ".")
        for a_ in BUNDLE_POR_REL[rel]["ancoras"]:
            txt = a_["texto"].lstrip("@"); pil = [x for x in a_["namespace"].split(".") if x] if a_["namespace"] else []
            cands = [".".join(pil[:k] + [txt]) for k in range(len(pil), -1, -1)]
            achado = next((c for c in cands if c in axm), None)
            anc_res[achado or ("?" + txt)] = {"modulo": mod, "texto": a_["texto"], "linha_na_fonte": a_["linha"], "resolvido": achado}
            if not (achado and set(axm[achado]) <= TRIO and srcm.get(achado) == rel):   # (parse_lean_provenance_v394 devolve o CAMINHO relativo do modulo, ex. TGLExt/X.lean, como no molde)
                anc_bad.append([mod, a_["texto"], achado, srcm.get(achado) if achado else None])
    n_anc = sum(len(b["ancoras"]) for b in BDL["modulos"])
    chk("as %d ANCORAS (os #print axioms retirados das fontes) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo da fonte" % n_anc, not anc_bad and n_anc > 0, anc_bad[:5])
    # ------------------------------------------------------------------ os modulos e as declaracoes
    nos_k = os.path.join(NOS, "tgl_kernel")
    ja_no_nos = sorted(r for r in nov if os.path.exists(os.path.join(nos_k, *r.split("/"))))
    chk("nenhum dos %d modulos do bundle existia no kernel do Nos v411 (todos NOVOS: nada e' sobrescrito)" % N_NOVOS, not ja_no_nos, ja_no_nos[:3])
    # (a proveniencia lida pelo parse_lean_provenance_v394 e' o CAMINHO relativo do modulo -- TGLExt/X.lean --, como no molde da v410; aqui se converte para o nome do modulo)
    mod_de_rel = {r: r[:-len(".lean")].replace("/", ".") for r in nov}
    por_mod = {}
    for nme, rel_ in srcm.items():
        if rel_ in mod_de_rel:
            por_mod.setdefault(mod_de_rel[rel_], []).append(nme)
    fora_do_bundle = sorted(rel_ for rel_ in set(srcm.values()) if rel_ not in mod_de_rel)
    novos_fora = [rel_ for rel_ in fora_do_bundle if not os.path.exists(os.path.join(nos_k, *rel_.split("/")))]
    chk("o compilador so' emite declaracoes dos %d modulos do bundle ou de modulos ANTIGOS (os %d fora do bundle existem todos no Nos v411)" % (N_NOVOS, len(fora_do_bundle)), not novos_fora, novos_fora[:3])
    sem_decl_prov = [m for m in NEWMODS if m not in por_mod]
    chk("(informativo) modulos do bundle SEM nenhuma declaracao na proveniencia do Audit: %d" % len(sem_decl_prov), not sem_decl_prov, sem_decl_prov[:5], informativo=True)
    novas_todas = sorted(n for L in por_mod.values() for n in L)
    pub = sorted(n for n in novas_todas if not n.startswith("_private.")); priv = sorted(n for n in novas_todas if n.startswith("_private."))
    nomeadas_por_mod = {m: sorted(n for n in por_mod.get(m, []) if not n.startswith("_private.") and classe(n) == "nomeada") for m in NEWMODS}
    aux = sorted(n for n in pub if classe(n) != "nomeada")
    cl_aux = {c: sum(1 for x in aux if classe(x) == c) for c, _ in AUX_CLASSES}
    prefixo = {m: "ext_%s_412_" % m.split(".")[-1].lower() for m in NEWMODS}
    flags = []
    for m in NEWMODS:
        i_ = 0
        for n in nomeadas_por_mod[m]:
            if n in axr0:
                continue   # (reatribuida a pedra: ja estava no axiom_report da v411; sem bandeira nova)
            i_ += 1; flags.append(["%s%04d" % (prefixo[m], i_), n, m, "%s_nomeada" % m.split(".")[-1].lower()])
    base_flags = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS").value)
    chk("as chaves das bandeiras novas (ext_<modulo>_412_*) nao colidem com as %d da base v411 (_LEAN_THEOREM_FLAGS) e sao unicas; os NOMES nao repetem os de uma bandeira existente e sao unicos" % len(base_flags),
        len({f[0] for f in flags}) == len(flags) and not ({f[0] for f in flags} & set(base_flags)) and not ({f[1] for f in flags} & set(base_flags.values())) and len({f[1] for f in flags}) == len(flags), len(flags))
    chk("toda bandeira nova esta no axiom_report, no trio, e e' declaracao NOMEADA publica (a politica da v394)", all(f[1] in axm and set(axm[f[1]]) <= TRIO and classe(f[1]) == "nomeada" and not f[1].startswith("_private.") for f in flags), len(flags))
    # NENHUMA chave antiga muda de literal: toda chave da base segue apontando para um nome que existe, no trio, com a MESMA lista de axiomas
    chaves_mudam = [k for k, v in base_flags.items() if not (v in axm and axm[v] == axr0.get(v, axm.get(v)) and set(axm[v]) <= TRIO)]
    chk("NENHUMA chave antiga muda de literal: as %d chaves de _LEAN_THEOREM_FLAGS da base seguem com o mesmo nome, presente no Audit, no trio, com a mesma lista de axiomas" % len(base_flags), not chaves_mudam, chaves_mudam[:5])
    reatribuidas = {n: {"antes": (core0["kernel_formalization"].get("declaration_sources_v394") or {}).get(n), "agora": srcm[n]} for n in novas_todas if n in axr0}
    novas_reais = [n for n in novas_todas if n not in axr0]
    chk("declaracoes NOVAS dos modulos novos (publicas + privadas, por proveniencia, menos as reatribuidas) == TOTAL(v412) - TOTAL(v411); as reatribuidas sao auxiliares",
        bool(m_cov) and len(novas_reais) == kh_cov[0] - int(cov0.get("decl", -1)) and all(classe(n) != "nomeada" for n in reatribuidas), [len(novas_reais), kh_cov[0] if kh_cov else None, cov0.get("decl"), list(reatribuidas)[:3]])
    chk("os nomes do axiom_report da v411 (core da base) seguem todos no axiom_report de agora (nada se perde), com a MESMA lista", all(n in axm and axm[n] == axr0[n] for n in axr0), [len(axr0), sum(1 for n in axr0 if n not in axm)])
    chk("o axiom_report de agora tem exatamente os nomes da v411 mais as declaracoes dos modulos novos", set(axm) == set(axr0) | set(novas_todas), [len(axm), len(axr0), len(novas_todas)])
    chave_de = {f[1]: f[0] for f in flags}
    n_por_modulo = {m: sum(1 for f in flags if f[2] == m) for m in NEWMODS}
    anc_info = {k: dict(v, flag=chave_de.get(v["resolvido"]), axioms=axm.get(v["resolvido"]), classe=classe(v["resolvido"]) if v["resolvido"] else None) for k, v in anc_res.items()}
    anc_sem_bandeira = [k for k, v in anc_info.items() if v["resolvido"] and classe(v["resolvido"]) == "nomeada" and not v["flag"] and not v["resolvido"].startswith("_private.")]
    chk("(informativo) toda ancora nomeada publica tem bandeira: %d sem" % len(anc_sem_bandeira), not anc_sem_bandeira, anc_sem_bandeira[:5], informativo=True)
    salvar_json(os.path.join(KD, "FLAGS_v412.json"), {
        "politica": "so' declaracao NOMEADA publica tem bandeira (a pratica selada da v392 a v411); as auxiliares geradas pelo compilador (ultimo componente _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) "
                    "e as reatribuidas (ja no axiom_report da v411) ficam fora; UMA serie de chaves POR MODULO (ext_<modulo em minusculas>_412_NNNN), ordenada por nome, na ordem topologica do bundle; o numero e' MEDIDO do Audit desta geracao",
        "nota_dos_prefixos": "os prefixos sao proposta do construtor (claude-construtor-v412); a gerencia pode troca'-los antes do candidato; nenhuma chave antiga muda de literal (conferido acima)",
        "flags": flags, "n_flags": len(flags), "n_decl_audit": len(axm), "prefixos": prefixo, "n_por_modulo": n_por_modulo,
        "por_origem": {f"{m.split('.')[-1].lower()}_nomeada": n_por_modulo[m] for m in NEWMODS},
        "excluidas_auxiliares": {"n": len(aux), "por_classe": cl_aux, "nomes": aux},
        "publicas_nos_modulos": len(pub), "privadas_nos_modulos": len(priv), "decl_totais_modulos_novos": len(novas_todas), "decl_novas_dos_modulos": len(novas_reais), "reatribuidas_as_pedras": reatribuidas,
        "proveniencia_publicas": {n: srcm[n] for n in pub}, "ancoras": anc_info, "escada": [E0, E0 + len(flags)]})
    # ------------------------------------------------------------------ duracoes e build_full.log
    dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"]; dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]
    chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
    chk("(informativo) duracao do build (por modulo + inteiro) < 3600 s", dur_build < 3600, {"build_s": dur_build}, informativo=True)
    bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
    salvar(os.path.join(KD, "build_full.log"), bf.encode("utf-8"))
    # ------------------------------------------------------------------ arvore so-fontes e varredura recursiva (a funcao do um.py v411)
    if os.path.isdir(ARV):
        # (r2: a arvore so-fontes da Etapa 1 NAO e' apagada: vai para arvore_<etapa1|anterior>_<data>, ao lado, e a nova nasce no mesmo caminho)
        os.replace(ARV, ARV + "_anterior_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(ARV)
    ign = shutil.ignore_patterns("*.bak*")
    for rel in ("TGL", "TGLExt"):
        shutil.copytree(os.path.join(KB, rel), os.path.join(ARV, rel), copy_function=shutil.copy2, ignore=ign)
    for f in os.listdir(KB):
        p = os.path.join(KB, f)
        if os.path.isfile(p) and ".bak" not in f:
            shutil.copy2(p, os.path.join(ARV, f))
    ns = {"re": re, "os": os}
    exec(compile(ast.get_source_segment(um_src, fn["_lean_strip_comments_and_strings"]), "<um.strip>", "exec"), ns)
    TOKS = [ast.literal_eval(ast.get_source_segment(um_src, n.value)) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
    n_lean = n_o16 = 0; hits = []; hits_probe = []; links = []; bak_na_arvore = []
    pilha = [ARV]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if ".bak" in e.name:
                    bak_na_arvore.append(e.path)
                if e.is_junction() or e.is_symlink():
                    links.append(e.path)
                elif e.is_dir(follow_symlinks=False):
                    pilha.append(e.path)
                elif e.is_file(follow_symlinks=False) and e.name.lower().endswith(".lean"):
                    n_lean += 1; rel = os.path.relpath(e.path, ARV).replace(os.sep, "/"); n_o16 += rel.startswith("TGLExt/O16/")
                    code = ns["_lean_strip_comments_and_strings"](rd(e.path).decode("utf-8"))
                    for tok in TOKS:
                        if re.search(r"\b%s\b" % re.escape(tok), code):
                            (hits_probe if os.path.basename(rel).startswith("Probe") else hits).append("%s:%s" % (rel, tok))
    chk("arvore so-fontes sem juncao/link e sem .bak", not links and not bak_na_arvore, [links[:3], bak_na_arvore[:3]])
    chk("varredura de tokens proibidos RECURSIVA: zero hits (probes diagnosticos a parte)", not hits, {"hits": hits[:5], "hits_em_Probe": hits_probe[:5], "arquivos_lean": n_lean, "em_TGLExt_O16": n_o16, "tokens": TOKS})
    arv_ok = all(rd(os.path.join(ARV, *r.split("/"))) == rd(os.path.join(KB, *r.split("/"))) for r in ("TGLExt.lean", "TGL/Audit.lean")) and all(os.path.exists(os.path.join(ARV, *r.split("/"))) for r in nov)
    chk("a arvore tem os %d modulos novos e a raiz e o Audit identicos aos do sandbox" % N_NOVOS, arv_ok, N_NOVOS)
    # ------------------------------------------------------------------ as entradas ANTIGAS
    emb0 = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
    aud_antes = emb0["TGL/Audit.lean"]
    nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
    iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in axm and set(axm[n.lstrip("@")]) == set(axr0.get(n.lstrip("@"), ["?"])))
    chk("as entradas antigas do Audit v411 (nomes distintos) com a MESMA lista de axiomas do axiom_report v411", iguais_ant == len(nomes_antigos) and len(nomes_antigos) > 0, [iguais_ant, len(nomes_antigos)])
    exatas = sum(1 for n in axr0 if n in axm and axm[n] == axr0[n]); perdidos = [n for n in axr0 if n not in axm]
    chk("NADA da v411 se perde: todo nome do axiom_report da v411 segue no de agora, no trio", not perdidos and all(set(axm.get(n, ["?"])) <= TRIO for n in axr0), [len(axr0), len(perdidos), exatas])
    # ------------------------------------------------------------------ toolchain e o manifesto pinado
    man = json.load(open(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
    tl = {"lean_version": man.get("lean_version"), "lake_version": man.get("lake_version")}
    elan = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    exe = lambda nome_: shutil.which(nome_) or os.path.join(elan, nome_ + ".exe")
    lv = subprocess.run([exe("lean"), "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
    kv = subprocess.run([exe("lake"), "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
    chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
    imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    raiz0, aud0 = sha(nos_root), sha(nos_aud)
    chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v411 pinado (e == o embutido no um.py da base)", ff.get("TGLExt.lean") == raiz0 == sha(emb0["TGLExt.lean"].encode("utf-8")) and ff.get("TGL/Audit.lean") == aud0 == sha(aud_antes.encode("utf-8")), [raiz0[:16], aud0[:16]])
    # ------------------------------------------------------------------ os modulos (pedras) do recibo: declaracoes que o B(n) aceita (N1k)
    pedras = []; sem_decl = []; sha_bad = []
    for p_ in nov:
        fb = rd(os.path.join(ARV, *p_.split("/"))); fonte = fb.decode("utf-8"); shr = sha(fb)
        if shr != BUNDLE_POR_REL[p_]["sha256"]:
            sha_bad.append(p_)
        md = p_[:-len(".lean")].replace("/", ".")
        decl = []
        for n in por_mod.get(md, []):
            curto = n.split(".")[-1].strip("\u00ab\u00bb")
            if n.startswith("_private.") or not curto:
                continue
            if not re.search(r"(?<![\w'.])" + re.escape(curto) + r"(?![\w'])", fonte):
                continue
            decl.append(n)
        decl = sorted(set(decl))
        if not decl:
            sem_decl.append(p_)
        pedras.append({"path": p_, "sha256": shr, "declaracoes": decl})
    chk("o sha256 de cada um dos %d modulos na arvore == o que o preparo do bundle pinou (BUNDLE_v412.json)" % N_NOVOS, not sha_bad, sha_bad[:3])
    riscos_bn = {"pedras_sem_declaracao_nomeada": sem_decl, "regra": "N1k do esboco R3.3: cada pedra do recibo exige >= 1 declaracao com entrada no axiom_report, linha no log do Audit e NOME na fonte",
                 "efeito": "o B(n) pos-selo RECUSARIA o recibo (nao o rito) se houver modulo sem declaracao aceita"}
    n_decl_recibo = sum(len(p["declaracoes"]) for p in pedras)
    chk("(informativo) cada modulo do recibo tem >= 1 declaracao aceita (N1k do B(n)): %d sem" % len(sem_decl), not sem_decl, sem_decl[:5], informativo=True)
    j1 = [kh_cov[0] - int(cov0["decl"]), kh_cov[1] - int(cov0["thm"]), kh_cov[2]] if kh_cov else [None, None, None]
    kh_json = {"contrato": "KH_N1_v401", "desenho": "(a) run_cmd no fim do Audit (herdado da v392); (b) linha TGL_DECL_SOURCE por constante (proveniencia emitida pelo compilador, v396)",
               "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]} if kh_cov else None, "linha_TOTAL_v411": {"decl": cov0.get("decl"), "thm": cov0.get("thm"), "fora_do_trio": cov0.get("fora_do_trio")},
               "axiom_report_efetivo_n": len(axm), "proveniencia_n": len(srcm), "nao_lidas_pelo_leitor_v394": 0, "nomes_distintos_print_antigos": len(nomes_antigos), "antigas_identicas": iguais_ant,
               "entradas_antigas_exatas_no_efetivo": exatas, "nomes_v411_perdidos": len(perdidos), "novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas), "sorryAx_no_log_do_audit": AL.count("sorryAx"),
               "delta_vs_v411": {"decl": j1[0], "thm": j1[1]}, "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800,
               "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))), "n_bandeiras": len(flags), "decl_dos_modulos_novos": len(novas_todas),
               "decl_novas_dos_modulos": len(novas_reais), "reatribuidas_as_pedras": reatribuidas, "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "n_modulos_novos": N_NOVOS,
               "quando": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "estatuto": "[REAL] medido por pos_build_kernel_v412_r5.py sobre o log do Audit do sandbox; fora do selo"}
    salvar_json(os.path.join(KD, "KH_N1_v412.json"), kh_json)
    r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
    criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
                 "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas)}
    x19 = "sim" if any(p["path"].endswith("/LightNetStandardWedgeDataBGL.lean") for p in pedras) else "nao"
    chk("x19 = 'nao': nenhum dos %d modulos do recibo e' a LightNetStandardWedgeDataBGL (R31-6: 'sim' <=> a pedra consta do recibo)" % N_NOVOS, x19 == "nao", x19)
    logs_cop = {}
    for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
        b = rd(os.path.join(KD, nome)); logs_cop[nome] = {"bytes": len(b), "sha256": sha(b), "origem": os.path.join(KD, nome), "copiado": False}
    logs_cop["cobertura_linha"] = cov_a
    salvar_json(os.path.join(KD, "LOGS_COPIADOS_v412.json"), logs_cop)
    rc_med = 0 if (rb == 0 and ra == 0) else (rb or ra)
    recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v412", "rc": rc_med, "sorry": n_sorry, "erros": n_err,
              "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
              "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
              "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
              "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
              "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
              "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
              "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
              "criterios": {k: {"medido": v} for k, v in criterios.items()},
              "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v411)", "antes": imp(ff), "depois": imp(ff)},
              "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "nota": "gerado por pos_build_kernel_v412_r5.py (Etapa 2 pelo contrato R5, decima lista de pedras, 18/11/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v412 e do manifesto novo); a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela); "
                      "o build do sandbox C:/t/k412c/final foi INCREMENTAL no que e' antigo (copia de C:/t/k411c/final, o kernel da v411 compilado, com as fontes conferidas por sha256 contra o Nos v411) e compilou os modulos do bundle (" + str(N_NOVOS) + " modulos, na ordem topologica; quais tiveram linha Built neste build esta' em kernel/POS_BUILD_v412.json, campo modo_dos_modulos_no_build); logs em kernel\\; o rito real do Nos compila tudo a frio"}
    ok = all(s["ok"] for s in sinais if not s.get("informativo"))
    salvar_json(os.path.join(KD, "KERNEL_RECIBO_v412.json"), recibo)
    crit = {"contrato": "CRITERIOS_R3_1", "versao": "v412", "preenchido": True, "x19": x19, "esperados": criterios,
            "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v412.json (J1 = diferenca dos TOTAIS do KH-N1 v412 - v411). x19='nao': o recibo v412 lista os " + str(N_NOVOS) + " modulos NOVOS de TGLExt/ e a "
                      "LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392; a gerencia confere e pina o sha256 antes do B(n).",
            "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
    salvar_json(os.path.join(VD, "CRITERIOS_v412.json"), crit)
    pos = {"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "modo_dos_modulos_no_build": modo, "todos_os_modulos_a_frio": todos_a_frio,
           "por_modulo_marcas": por_mod_marcas, "tempos_built_s": tempos, "avisos_por_modulo": avisos, "aviso_conhecido_TowerWedgeIndex": {"linhas": av_conhecido.get("linhas", []), "parece_o_conhecido": conhecido_ok},
           "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe, "n_flags": len(flags), "n_decl_audit": len(axm), "escada": [E0, E0 + len(flags)], "E411": E0,
           "linha_TOTAL": kh_json["linha_TOTAL"], "linha_TOTAL_v411": kh_json["linha_TOTAL_v411"], "delta_vs_v411": kh_json["delta_vs_v411"],
           "pedras_sem_declaracao": sem_decl, "riscos_bn": riscos_bn, "n_declaracoes_no_recibo": n_decl_recibo, "inicio": ini, "fim": fim, "githash_lean": hashes_lean,
           "duracao_build_s": dur_build, "duracao_audit_s": dur_audit, "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "n_ancoras": n_anc, "x19": x19,
           "chaves_antigas": {"n": len(base_flags), "mudam": chaves_mudam},
           "falhas": [s["checagem"] for s in sinais if not s["ok"] and not s.get("informativo")], "falhas_informativas": [s["checagem"] for s in sinais if not s["ok"] and s.get("informativo")], "backups": BACKUPS}
    salvar_json(os.path.join(KD, "POS_BUILD_v412.json"), pos)
    print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "| bandeiras:", len(flags), "| escada:", [E0, E0 + len(flags)], "| TOTAL:", kh_cov, "| delta_vs_v411:", j1[:2],
          "| build_s:", dur_build, "audit_s:", dur_audit, "| ancoras:", "ok" if not anc_bad else "FALHA", "| avisos (fora a TowerWedgeIndex):", outros, "| falhas:", pos["falhas"], "| falhas informativas:", pos["falhas_informativas"])
    return ok


if __name__ == "__main__":
    try:
        r = principal()
    except SystemExit:
        raise
    except Exception:
        tb = traceback.format_exc(); print("EXCECAO (fail-closed):\n" + tb)
        try:
            if not (SO_BUILT or CONTROLE_POSITIVO):   # (nos modos de conferencia o POS_BUILD vigente nao e' tocado)
                salvar_json(os.path.join(KD, "POS_BUILD_v412.json"), {"ok": False, "excecao": tb, "sinais": sinais, "backups": BACKUPS})
        except Exception:
            pass
        sys.exit(2)
    sys.exit(0 if r else 1)

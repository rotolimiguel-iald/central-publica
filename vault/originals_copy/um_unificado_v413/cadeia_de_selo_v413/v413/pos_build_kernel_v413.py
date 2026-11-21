# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\pos_build_kernel_v412_r7.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de pos_build_kernel_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_02_derivar_kernel_v412.py). O original fica intacto.
# [DERIVADO v412 r5, 18/11/2026, claude-construtor-v412 (contrato R11)] copia de pos_build_kernel_v412_c4.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 153 modulos); e5_02_derivar_scripts_r7_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 c4, 17/11/2026, claude-construtor-v412 (contrato R4)] copia de pos_build_kernel_v412_r4.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12; 42 modulos); e4_02_derivar_scripts_c4_v412.py (trocas de texto exato com contagem registrada).
# [DERIVADO v412 r4, 17/11/2026, claude-construtor-v412 (Etapa 2, bloco 0)] copia de pos_build_kernel_v412_r3.py (que fica intacto) com a CAUSA da checagem vazia corrigida (prefixo dos nomes de o_lake_recompila; conta de itens examinados; zero itens = falha); derivador: e2_01_derivar_pos_build_r4_v412.py.
# [DERIVADO v412 r3, 17/11/2026, claude-construtor-v412 (continuacao 2)] copia de pos_build_kernel_v412_r2.py para a DECIMA SEGUNDA lista de pedras (insumos\MANIFESTO_PEDRAS_v412_R12.json, insumos\pedras_r12); derivar_scripts_r3_v412.py (trocas de texto exato com contagem conferida).
# [DERIVADO v412 r2, 17/11/2026, claude-construtor-v412] copia de pos_build_kernel_v412.py para a DECIMA SEGUNDA lista (40 modulos): le insumos\MANIFESTO_PEDRAS_v412_R12.json; a arvore so-fontes da Etapa 1 e' movida, nao apagada. O resto e' identico (derivar_scripts_etapa1_r2_v412.py).
# [ADAPTADO v412, 17/11/2026, claude-construtor-v412] do molde v410\pos_build_kernel_v410.py (bundle de 2 modulos) para o bundle de N modulos da v412 (lidos de BUNDLE_v412.json), sem delta:
# as constantes vem dos arquivos do preparo (BUNDLE_v413.json, kernel_modulos_novos_v413.json, kernel\ULTIMA_INSTALACAO_v413.json) e da base v412 selada (base_v412\, copia de bytes do Nos)
"""pos_build_kernel_v413.py -- DEPOIS de construir_kernel_v413.sh (build POR MODULO, na ordem topologica, dos modulos novos de TGLExt/ no sandbox C:\\t\\k413c\\final; depois o build inteiro e o Audit):
(1) le as marcas; se o build PAROU num modulo, registra o modulo e as linhas de erro do bloco dele no log e sai 1 (nada se conserta: nem o kernel, nem a prova, nem o log);
(2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully' em cada invocacao, linha BUILT dos modulos que este build tinha de compilar,
da raiz (TGLExt) e do Audit (TGL.Audit), cabecalho dos .olean = Lean 4.31.0) e conta os AVISOS POR MODULO (linhas `warning: TGLExt/<Nome>.lean:` no bloco Built do modulo; o aviso conhecido e
preexistente da TowerWedgeIndex, a tatica `change` que nao faz nada, e' REGISTRADO, nao consertado);
(3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v412 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, por ast de
base_v412\\um.py), confere as ANCORAS (os #print axioms retirados de cada fonte, resolvidos pela pilha de namespace da linha) e deriva FLAGS_v413.json (as declaracoes NOMEADAS publicas dos
modulos novos, politica da v394: UMA serie por modulo, ext_<modulo em minusculas>_413_NNNN, ordenada por nome; os modulos na ordem do bundle; os PREFIXOS sao proposta do construtor e a gerencia
pode troca'-los antes do candidato: nenhuma chave antiga muda);
(4) confere que NENHUMA chave antiga muda de literal (toda chave de _LEAN_THEOREM_FLAGS da base segue apontando para um nome que existe, no trio, com a MESMA lista de axiomas) e que nada da v412 se perde;
(5) copia a ARVORE so-fontes para C:\\t\\k413c\\arvore e varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v412 (por ast);
(6) escreve KH_N1_v413.json, KERNEL_RECIBO_v413.json (contrato KERNEL_RECIBO_R3_2: uma entrada por modulo do bundle, com formal_files_antes, nos_kernel_impressao, lake_version e a arvore SEM juncao),
vinculo/CRITERIOS_v413.json, kernel/POS_BUILD_v413.json, kernel/FLAGS_v413.json e kernel/LOGS_COPIADOS_v413.json.
Fail-closed: cada checagem e' um sinal; falha e' REGISTRADA; saida existente ganha backup de BYTES (.bak_<data>) antes de ser substituida; escrita por temporario + os.replace.
Uso: C:\\Python314\\python.exe -I -B -X utf8 pos_build_kernel_v413.py
[v413, claude-construtor-v413, 20/11/2026; derivado de v412\\pos_build_kernel_v412_r7.py] O que muda: (a) a base e' a v412 SELADA (base_v412\\, copia de bytes do Nos), conferida pelo pino
do selo e pelo candidato_sha16 de v412\\ESPERADOS_v412.json (a v413 ainda nao tem desenho nem contrato); (b) o manifesto e' o da v413 (insumos\\MANIFESTO_PEDRAS_v413.json: modulos_novos e
kernel_corrigido); (c) o MODULO CORRIGIDO so' no texto (kernel_corrigido do BUNDLE_v413.json) e' construido PRIMEIRO (uma linha nas marcas antes dos novos), tem de ter linha Built e o .olean com o
cabecalho certo, emitir EXATAMENTE as declaracoes que emitia na v412 (declaration_sources_v394 do core da base) com a MESMA lista de axiomas, e o ANTES (formal_files_sha256 do manifesto v412 pinado)
== sha256_origem; os modulos ANTIGOS que dependem dele sao recompilados (informativo) e nao ganham bandeira; o recibo do kernel traz o corrigido nas pedras (o B(n), N1l, exige pedras == os arquivos
formais novos ou mudados do manifesto pinado pelo selo) e no campo kernel_corrigido (path, sha256 antes e depois, declaracoes); (d) a TowerWedgeIndex e' modulo ANTIGO na v413: o aviso conhecido e preexistente e' lido do bloco dela (Replayed, ou Built se o lake a recompilar), registrado, nao consertado; os
avisos dos modulos antigos sao contados a parte (informativo); (e) as bandeiras novas tem o prefixo ext_<modulo>_413_NNNN."""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, traceback, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel"); VD = os.path.join(HERE, "vinculo")
KB = os.path.join("C:" + os.sep, "t", "k413c", "final"); ARV = os.path.join("C:" + os.sep, "t", "k413c", "arvore")
BASE = os.path.join(HERE, "base_v412")
MAN_P = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v413.json")
V412 = os.path.join(os.path.dirname(HERE), "v412")
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
    BDL = json.load(open(os.path.join(HERE, "BUNDLE_v413.json"), encoding="utf-8"))
    BL = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v413.json"), encoding="utf-8"))
    ULT = json.load(open(os.path.join(KD, "ULTIMA_INSTALACAO_v413.json"), encoding="utf-8"))
    MAN = json.load(open(MAN_P, encoding="utf-8"))
    nov = list(BL["novos"]); NEWRELS = set(nov); NEWMODS = [p[:-len(".lean")].replace("/", ".") for p in nov]; N_NOVOS = len(nov)
    BUNDLE_POR_REL = {b["rel"]: b for b in BDL["modulos"]}
    chk("a lista dos modulos novos (kernel_modulos_novos_v413.json) == a do BUNDLE_v413.json == n_modulos_novos do manifesto, sem repeticao, na ordem topologica",
        N_NOVOS == BDL["n"] == int(MAN["n_modulos_novos"]) == len(set(nov)) and [b["rel"] for b in BDL["modulos"]] == nov and BDL.get("manifesto_sha256") == sha(rd(MAN_P)),
        [N_NOVOS, BDL["n"], MAN["n_modulos_novos"]])
    KCL = list(BDL.get("kernel_corrigido") or []); KCMODS = [k_["modulo_completo"] for k_ in KCL]; KCRELS = [k_["rel"] for k_ in KCL]
    chk("o modulo corrigido do BUNDLE_v413.json == o kernel_corrigido do manifesto (mesmos nomes; o instalado == sha256_saida; a lista do kernel_modulos_novos_v413.json igual)",
        len(KCL) > 0 and sorted(KCMODS) == sorted(MAN.get("kernel_corrigido") or {}) and all(k_["sha256"] == MAN["kernel_corrigido"][k_["modulo_completo"]]["sha256_saida"] for k_ in KCL)
        and BL.get("kernel_corrigido") == KCRELS, KCMODS)
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
        salvar_json(os.path.join(KD, "POS_BUILD_v413.json"), {"ok": False, "parou_em": mod_, "rc_build": rb, "rc_audit": ra, "por_modulo_marcas": por_mod_marcas, "erros_do_modulo": erros_mod,
                                                              "trecho_do_log_do_modulo": erro_txt, "sinais": sinais, "inicio": ini, "fim": fim, "backups": BACKUPS,
                                                              "nota": "o build parou: nada foi consertado (nem prova, nem nome); o Audit nao rodou; relatar o erro exato a gerencia"})
        print("\nPOS-BUILD: PAROU no modulo", mod_, "| rc_build", rb, "| erros:", erros_mod[:5]); return False
    # ------------------------------------------------------------------ a base (v412 selada)
    um_b = rd(os.path.join(BASE, "um.py")); um_src = um_b.decode("utf-8"); tree = ast.parse(um_src)
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    _selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); _esp = json.load(open(os.path.join(V412, "ESPERADOS_v412.json"), encoding="utf-8"))
    chk("a base_v412\\um.py e' a v412 SELADA (o sha256 == o que o selo do Nos pina; o selo diz v412; o sha16 == o candidato_sha16 de v412\\ESPERADOS_v412.json; lidos dos arquivos)",
        _selo.get("um_version") == "v412" and sha(um_b) == (_selo.get("sha256") or {}).get("um.py") and sha(um_b)[:16] == _esp.get("candidato_sha16"),
        [sha(um_b)[:16], _esp.get("candidato_sha16"), _selo.get("um_version")])
    _ns = {"re": re}
    for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
        exec(compile(ast.get_source_segment(um_src, fn[nome]), "<base_v412:%s>" % nome, "exec"), _ns)
    parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
    core0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]; axr0 = core0["kernel_formalization"]["axiom_report"]
    cov0 = core0["kernel_formalization"].get("axiom_coverage_v392") or {}
    E0 = int(core0["external_ladder"]["n_theorems_expected"])
    # ------------------------------------------------------------------ o build
    chk("rc do lake build == 0 e rc do Audit == 0 (marcas: rc=0); nenhum modulo parou", rb == 0 and ra == 0 and bool(re.search(r"(?m)^rc=0$", marcas)) and not parou, [rb, ra])
    chk("as marcas trazem UMA linha por modulo (o corrigido primeiro, depois os novos na ordem do bundle), todas com rc 0", [m for m in por_mod_marcas] == KCMODS + NEWMODS and all(v["rc"] == 0 for v in por_mod_marcas.values()), [len(por_mod_marcas), len(KCMODS) + N_NOVOS])
    RE_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u201c\"]sorry|\bsorryAx\b", re.I)
    n_err = len(re.findall(r"(?m)^error:|: error:", LB + "\n" + AL)); n_sorry = len(RE_SORRY.findall(LB + "\n" + AL)) + len(RE_SORRY.findall(re.sub(r"\s+", " ", LB + "\n" + AL)))
    chk("zero erro; zero sorry/sorryAx (formas: crase, aspas, sorryAx; com e sem quebra)", n_err == 0 and n_sorry == 0, [n_err, n_sorry])
    jobs = {}
    for st, md, s_, L in blocos:
        jobs.setdefault(md, []).append((st, s_))
    n_inv = LB.count("=== MODULO ") + LB.count("=== BUILD INTEIRO")
    n_ok = len(re.findall(r"(?m)^[ \t]*Build completed successfully\b", LB))
    chk("'Build completed successfully' em CADA invocacao do lake (%d por modulo + 1 do build inteiro)" % (len(KCMODS) + N_NOVOS), n_inv == len(KCMODS) + N_NOVOS + 1 and n_ok == n_inv, [n_inv, n_ok])
    modo = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in NEWMODS}
    exig_built, fora_do_bundle, extras_raiz_audit = exigidos_built(ULT, NEWMODS)
    ok_built, faltam_built, n_exame_built = checa_built(exig_built, fora_do_bundle, modo)
    chk("os modulos que ESTE build tinha de compilar (kernel\\ULTIMA_INSTALACAO_v413.json, o_lake_recompila): %d EXAMINADOS (zero examinados e' falha; nomes sem o prefixo TGLExt. normalizados; raiz e Audit conferidos a parte: %s) tem linha Built (a frio); %d modulos novos com Built neste log" % (n_exame_built, extras_raiz_audit, sum(1 for v in modo.values() if v == "Built")),
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
               "nota": "o_lake_recompila lido de kernel/ULTIMA_INSTALACAO_v413.json; os logs lidos de kernel/lake_build.log (build da v413); nada alem deste recibo foi escrito"}
        salvar_json(os.path.join(KD, "BUILT_CHECAGEM_CORRIGIDA_v413.json"), rec)
        print("\nMODO %s: %d controles, todos como devem: %s; examinados na checagem real: %d" % (rec["modo"], len(controles), todos_ok, n_exame_built))
        return bool(todos_ok and ok_built)
    todos_a_frio = all(v == "Built" for v in modo.values())
    chk("(informativo) TODOS os %d modulos novos foram compilados neste build (a frio, como o do rito)" % N_NOVOS, todos_a_frio, {k: v for k, v in modo.items() if v != "Built"}, informativo=True)
    modo_kc = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in KCMODS}
    exig_kc = list(ULT.get("kernel_corrigido_recompila") or [])
    chk("o modulo corrigido que ESTE build tinha de compilar (kernel\\ULTIMA_INSTALACAO_v413.json, kernel_corrigido_recompila) tem linha Built", set(exig_kc) <= set(KCMODS) and all(modo_kc.get(m) == "Built" for m in exig_kc),
        {"exigidos": exig_kc, "modo": modo_kc})
    dep_ant = list(ULT.get("dependentes_antigos_do_corrigido_que_o_lake_recompila") or [])
    dep_ant_mod = [m for m in dep_ant if m not in ("TGLExt", "TGL", "TGL.Audit")]
    dep_sem_built = [m for m in dep_ant_mod if not any(st == "Built" for st, _ in jobs.get(m, []))]
    chk("(informativo) os modulos ANTIGOS que dependem do corrigido foram recompilados neste build (linha Built): %d de %d" % (len(dep_ant_mod) - len(dep_sem_built), len(dep_ant_mod)), not dep_sem_built,
        dep_sem_built[:8], informativo=True)
    built_raiz = any(st == "Built" for st, _ in jobs.get("TGLExt", [])); built_audit = any(st == "Built" for st, _ in jobs.get("TGL.Audit", []))
    chk("a raiz (TGLExt) e o Audit (TGL.Audit) foram COMPILADOS neste build (linha Built)", built_raiz and built_audit, [built_raiz, built_audit])
    tempos = {m: next((s_ for st, s_ in jobs.get(m, []) if st == "Built" and s_ is not None), None) for m in NEWMODS}
    build_s_soma = round(sum(v for v in tempos.values() if v), 3); build_s_max = max([v for v in tempos.values() if v] or [0])
    # os AVISOS por modulo: as linhas `warning: TGLExt/<Nome>.lean:` do bloco Built do proprio modulo (o Replayed de outro build repete o aviso; nao se conta duas vezes)
    avisos = {}; avisos_antigos = {}
    for st, md, s_, L in blocos:
        if st not in ("Built", "Replayed"):
            continue
        rel_ = md.replace(".", "/") + ".lean"
        ws = [l for l in L if l.startswith("warning:")]
        reg_ = {"n": len(ws), "do_proprio_arquivo": sum(1 for l in ws if l.startswith("warning: " + rel_ + ":")), "linhas": ws[:20], "bloco": st}
        if md in NEWMODS or md in KCMODS:
            if st == "Built" or md not in avisos:   # (o bloco Built manda; o Replayed de outra invocacao repete o aviso e nao se conta duas vezes)
                avisos[md] = reg_
        elif ws and (st == "Built" or md not in avisos_antigos):
            avisos_antigos[md] = reg_
    for m in KCMODS + NEWMODS:
        avisos.setdefault(m, {"n": 0, "do_proprio_arquivo": 0, "linhas": [], "nota": "sem bloco Built nem Replayed neste log (sem mensagem)" if (modo.get(m) if m in modo else modo_kc.get(m)) is None else None})
    # o aviso conhecido e preexistente da TowerWedgeIndex: na v413 ela e' modulo ANTIGO (da v412); o aviso volta no bloco Replayed (ou Built, se o lake a recompilar)
    av_conhecido = avisos_antigos.get(MOD_AVISO_CONHECIDO, {})
    conhecido_ok = av_conhecido.get("n", 0) >= 1 and all(("change" in l or "never executed" in l or "does nothing" in l or "unused" in l.lower()) for l in av_conhecido.get("linhas", []))
    outros = {m: v["n"] for m, v in avisos.items() if v["n"]}
    chk("(informativo) avisos: nenhum modulo novo nem o corrigido com aviso; o conhecido e preexistente da TowerWedgeIndex (modulo antigo) registrado, nao consertado", not outros and conhecido_ok,
        {"TowerWedgeIndex": av_conhecido.get("linhas", [])[:3], "outros": outros}, informativo=True)
    antigos_com_aviso = {m: v["n"] for m, v in avisos_antigos.items()}
    chk("(informativo) modulos ANTIGOS com aviso neste log (preexistentes; mensagens repetidas pelo lake; nada se conserta): %d" % len(antigos_com_aviso), True,
        {"n_modulos": len(antigos_com_aviso), "n_avisos": sum(antigos_com_aviso.values())}, informativo=True)
    LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
    hdr = {}
    for m in KCMODS + NEWMODS + ["TGLExt", "TGL.Audit"]:
        p = os.path.join(LIBL, *m.split(".")) + ".olean"
        h = rd(p)[:96] if os.path.exists(p) else b""
        hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
    hashes_lean = sorted({v[1] for v in hdr.values() if v[1]})
    chk("cabecalho de TODO .olean (%d novos + o corrigido + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean" % N_NOVOS, all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean, [m for m, v in hdr.items() if not v[0]][:3]])
    # ------------------------------------------------------------------ o log do Audit (so' ele) com as funcoes do um.py v412 selado
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
    # ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v412 selado + os imports
    nos_root = rd(os.path.join(NOS, "tgl_kernel", "TGLExt.lean")); nos_aud = rd(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"))
    sb_root = rd(os.path.join(KB, "TGLExt.lean")); sb_aud = rd(os.path.join(KB, "TGL", "Audit.lean"))
    chk("a raiz do sandbox == a raiz do Nos (v412 selada) + os %d imports do bundle (ROOT_SUFFIX), em bytes" % N_NOVOS, sb_root == nos_root + BL["root_suffix"].encode("utf-8"), [len(sb_root), len(nos_root), len(BL["root_suffix"])])
    chk("o Audit do sandbox == o Audit do Nos (bytes): o Audit NAO muda na v413 (o run_cmd do KH-N1 cobre toda constante de TGL e TGLExt)", sb_aud == nos_aud, [len(sb_aud), len(nos_aud)])
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
    chk("nenhum dos %d modulos do bundle existia no kernel do Nos v412 (todos NOVOS: nada e' sobrescrito)" % N_NOVOS, not ja_no_nos, ja_no_nos[:3])
    # (a proveniencia lida pelo parse_lean_provenance_v394 e' o CAMINHO relativo do modulo -- TGLExt/X.lean --, como no molde da v411; aqui se converte para o nome do modulo)
    mod_de_rel = {r: r[:-len(".lean")].replace("/", ".") for r in nov}
    por_mod = {}
    for nme, rel_ in srcm.items():
        if rel_ in mod_de_rel:
            por_mod.setdefault(mod_de_rel[rel_], []).append(nme)
    fora_do_bundle = sorted(rel_ for rel_ in set(srcm.values()) if rel_ not in mod_de_rel)
    novos_fora = [rel_ for rel_ in fora_do_bundle if not os.path.exists(os.path.join(nos_k, *rel_.split("/")))]
    chk("o compilador so' emite declaracoes dos %d modulos do bundle ou de modulos ANTIGOS (os %d fora do bundle existem todos no Nos v412)" % (N_NOVOS, len(fora_do_bundle)), not novos_fora, novos_fora[:3])
    sem_decl_prov = [m for m in NEWMODS if m not in por_mod]
    chk("(informativo) modulos do bundle SEM nenhuma declaracao na proveniencia do Audit: %d" % len(sem_decl_prov), not sem_decl_prov, sem_decl_prov[:5], informativo=True)
    novas_todas = sorted(n for L in por_mod.values() for n in L)
    pub = sorted(n for n in novas_todas if not n.startswith("_private.")); priv = sorted(n for n in novas_todas if n.startswith("_private."))
    nomeadas_por_mod = {m: sorted(n for n in por_mod.get(m, []) if not n.startswith("_private.") and classe(n) == "nomeada") for m in NEWMODS}
    aux = sorted(n for n in pub if classe(n) != "nomeada")
    cl_aux = {c: sum(1 for x in aux if classe(x) == c) for c, _ in AUX_CLASSES}
    prefixo = {m: "ext_%s_413_" % m.split(".")[-1].lower() for m in NEWMODS}
    flags = []
    for m in NEWMODS:
        i_ = 0
        for n in nomeadas_por_mod[m]:
            if n in axr0:
                continue   # (reatribuida a pedra: ja estava no axiom_report da v412; sem bandeira nova)
            i_ += 1; flags.append(["%s%04d" % (prefixo[m], i_), n, m, "%s_nomeada" % m.split(".")[-1].lower()])
    base_flags = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS").value)
    chk("as chaves das bandeiras novas (ext_<modulo>_413_*) nao colidem com as %d da base v412 (_LEAN_THEOREM_FLAGS) e sao unicas; os NOMES nao repetem os de uma bandeira existente e sao unicos" % len(base_flags),
        len({f[0] for f in flags}) == len(flags) and not ({f[0] for f in flags} & set(base_flags)) and not ({f[1] for f in flags} & set(base_flags.values())) and len({f[1] for f in flags}) == len(flags), len(flags))
    chk("toda bandeira nova esta no axiom_report, no trio, e e' declaracao NOMEADA publica (a politica da v394)", all(f[1] in axm and set(axm[f[1]]) <= TRIO and classe(f[1]) == "nomeada" and not f[1].startswith("_private.") for f in flags), len(flags))
    # NENHUMA chave antiga muda de literal: toda chave da base segue apontando para um nome que existe, no trio, com a MESMA lista de axiomas
    chaves_mudam = [k for k, v in base_flags.items() if not (v in axm and axm[v] == axr0.get(v, axm.get(v)) and set(axm[v]) <= TRIO)]
    chk("NENHUMA chave antiga muda de literal: as %d chaves de _LEAN_THEOREM_FLAGS da base seguem com o mesmo nome, presente no Audit, no trio, com a mesma lista de axiomas" % len(base_flags), not chaves_mudam, chaves_mudam[:5])
    reatribuidas = {n: {"antes": (core0["kernel_formalization"].get("declaration_sources_v394") or {}).get(n), "agora": srcm[n]} for n in novas_todas if n in axr0}
    novas_reais = [n for n in novas_todas if n not in axr0]
    chk("declaracoes NOVAS dos modulos novos (publicas + privadas, por proveniencia, menos as reatribuidas) == TOTAL(v413) - TOTAL(v412); as reatribuidas sao auxiliares",
        bool(m_cov) and len(novas_reais) == kh_cov[0] - int(cov0.get("decl", -1)) and all(classe(n) != "nomeada" for n in reatribuidas), [len(novas_reais), kh_cov[0] if kh_cov else None, cov0.get("decl"), list(reatribuidas)[:3]])
    chk("os nomes do axiom_report da v412 (core da base) seguem todos no axiom_report de agora (nada se perde), com a MESMA lista", all(n in axm and axm[n] == axr0[n] for n in axr0), [len(axr0), sum(1 for n in axr0 if n not in axm)])
    chk("o axiom_report de agora tem exatamente os nomes da v412 mais as declaracoes dos modulos novos", set(axm) == set(axr0) | set(novas_todas), [len(axm), len(axr0), len(novas_todas)])
    ds0 = core0["kernel_formalization"].get("declaration_sources_v394") or {}
    kc_decl = {}
    for rel_ in KCRELS:
        antes_ = sorted(n for n, r in ds0.items() if r == rel_); agora_ = sorted(n for n, r in srcm.items() if r == rel_)
        kc_decl[rel_] = {"antes_n": len(antes_), "agora_n": len(agora_), "iguais": antes_ == agora_, "mesmos_axiomas": all(axm.get(n) == axr0.get(n) for n in agora_), "nomes": agora_}
    chk("o modulo corrigido emite EXATAMENTE as declaracoes que emitia na v412 (proveniencia do Audit == declaration_sources_v394 do core da base), com a MESMA lista de axiomas, no trio",
        bool(kc_decl) and all(v["iguais"] and v["mesmos_axiomas"] and v["agora_n"] > 0 for v in kc_decl.values()) and all(set(axm[n]) <= TRIO for v in kc_decl.values() for n in v["nomes"]),
        {k: {kk: vv for kk, vv in v.items() if kk != "nomes"} for k, v in kc_decl.items()})
    chave_de = {f[1]: f[0] for f in flags}
    n_por_modulo = {m: sum(1 for f in flags if f[2] == m) for m in NEWMODS}
    anc_info = {k: dict(v, flag=chave_de.get(v["resolvido"]), axioms=axm.get(v["resolvido"]), classe=classe(v["resolvido"]) if v["resolvido"] else None) for k, v in anc_res.items()}
    anc_sem_bandeira = [k for k, v in anc_info.items() if v["resolvido"] and classe(v["resolvido"]) == "nomeada" and not v["flag"] and not v["resolvido"].startswith("_private.")]
    chk("(informativo) toda ancora nomeada publica tem bandeira: %d sem" % len(anc_sem_bandeira), not anc_sem_bandeira, anc_sem_bandeira[:5], informativo=True)
    salvar_json(os.path.join(KD, "FLAGS_v413.json"), {
        "politica": "so' declaracao NOMEADA publica tem bandeira (a pratica selada da v392 a v412); as auxiliares geradas pelo compilador (ultimo componente _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) "
                    "e as reatribuidas (ja no axiom_report da v412) ficam fora; UMA serie de chaves POR MODULO (ext_<modulo em minusculas>_413_NNNN), ordenada por nome, na ordem topologica do bundle; o numero e' MEDIDO do Audit desta geracao",
        "nota_dos_prefixos": "os prefixos sao proposta do construtor (claude-construtor-v413, como a v412 fez com _412_); a gerencia pode troca'-los antes do candidato; nenhuma chave antiga muda de literal (conferido acima)",
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
    # ------------------------------------------------------------------ arvore so-fontes e varredura recursiva (a funcao do um.py v412)
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
    arv_ok = all(rd(os.path.join(ARV, *r.split("/"))) == rd(os.path.join(KB, *r.split("/"))) for r in ["TGLExt.lean", "TGL/Audit.lean"] + KCRELS) and all(os.path.exists(os.path.join(ARV, *r.split("/"))) for r in nov)
    chk("a arvore tem os %d modulos novos, e o modulo corrigido, a raiz e o Audit identicos aos do sandbox" % N_NOVOS, arv_ok, N_NOVOS)
    # ------------------------------------------------------------------ as entradas ANTIGAS
    emb0 = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
    aud_antes = emb0["TGL/Audit.lean"]
    nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
    iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in axm and set(axm[n.lstrip("@")]) == set(axr0.get(n.lstrip("@"), ["?"])))
    chk("as entradas antigas do Audit v412 (nomes distintos) com a MESMA lista de axiomas do axiom_report v412", iguais_ant == len(nomes_antigos) and len(nomes_antigos) > 0, [iguais_ant, len(nomes_antigos)])
    exatas = sum(1 for n in axr0 if n in axm and axm[n] == axr0[n]); perdidos = [n for n in axr0 if n not in axm]
    chk("NADA da v412 se perde: todo nome do axiom_report da v412 segue no de agora, no trio", not perdidos and all(set(axm.get(n, ["?"])) <= TRIO for n in axr0), [len(axr0), len(perdidos), exatas])
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
    chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v412 pinado (e == o embutido no um.py da base)", ff.get("TGLExt.lean") == raiz0 == sha(emb0["TGLExt.lean"].encode("utf-8")) and ff.get("TGL/Audit.lean") == aud0 == sha(aud_antes.encode("utf-8")), [raiz0[:16], aud0[:16]])
    kc_antes = {}
    for r_ in KCRELS:
        k_ = next(x for x in KCL if x["rel"] == r_)
        kc_antes[r_] = {"formal_files_v412": ff.get(r_), "sha256_origem": k_["sha256_origem"], "depois_na_arvore": sha(rd(os.path.join(ARV, *r_.split("/")))), "instalado_pelo_preparo": k_["sha256"]}
    chk("o modulo corrigido: ANTES == formal_files_sha256 do manifesto v412 pinado == sha256_origem; DEPOIS (na arvore) == o instalado pelo preparo (BUNDLE_v413.json)",
        len(kc_antes) > 0 and all(v["formal_files_v412"] == v["sha256_origem"] and v["depois_na_arvore"] == v["instalado_pelo_preparo"] for v in kc_antes.values()),
        {r: {k: (x or "")[:16] for k, x in v.items()} for r, v in kc_antes.items()})
    # o B(n) (verificar_kernel_recibo, N1l) exige que as pedras do recibo sejam EXATAMENTE os arquivos formais NOVOS OU MUDADOS do manifesto pinado pelo selo: o corrigido muda de sha256,
    # logo entra em `pedras` (com as declaracoes que o Audit imprime e que a fonte nomeia, N1k), alem do campo kernel_corrigido (antes e depois)
    pedras_kc = []
    for r_ in KCRELS:
        fb_ = rd(os.path.join(ARV, *r_.split("/"))); fonte_ = fb_.decode("utf-8")
        dkc_ = sorted({n for n in kc_decl[r_]["nomes"] if not n.startswith("_private.") and n.split(".")[-1].strip("«»")
                       and re.search(r"(?<![\w'.])" + re.escape(n.split(".")[-1].strip("«»")) + r"(?![\w'])", fonte_)})
        pedras_kc.append({"path": r_, "sha256": sha(fb_), "declaracoes": dkc_})
    chk("o modulo corrigido entra nas pedras do recibo (o B(n), N1l: pedras == arquivos formais novos ou mudados) com >= 1 declaracao aceita (N1k)",
        len(pedras_kc) == len(KCRELS) > 0 and all(p_["declaracoes"] for p_ in pedras_kc), {p_["path"]: len(p_["declaracoes"]) for p_ in pedras_kc})
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
    chk("o sha256 de cada um dos %d modulos na arvore == o que o preparo do bundle pinou (BUNDLE_v413.json)" % N_NOVOS, not sha_bad, sha_bad[:3])
    riscos_bn = {"pedras_sem_declaracao_nomeada": sem_decl, "regra": "N1k do esboco R3.3: cada pedra do recibo exige >= 1 declaracao com entrada no axiom_report, linha no log do Audit e NOME na fonte",
                 "efeito": "o B(n) pos-selo RECUSARIA o recibo (nao o rito) se houver modulo sem declaracao aceita"}
    n_decl_recibo = sum(len(p["declaracoes"]) for p in pedras)
    chk("(informativo) cada modulo do recibo tem >= 1 declaracao aceita (N1k do B(n)): %d sem" % len(sem_decl), not sem_decl, sem_decl[:5], informativo=True)
    j1 = [kh_cov[0] - int(cov0["decl"]), kh_cov[1] - int(cov0["thm"]), kh_cov[2]] if kh_cov else [None, None, None]
    kh_json = {"contrato": "KH_N1_v401", "desenho": "(a) run_cmd no fim do Audit (herdado da v392); (b) linha TGL_DECL_SOURCE por constante (proveniencia emitida pelo compilador, v396)",
               "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]} if kh_cov else None, "linha_TOTAL_v412": {"decl": cov0.get("decl"), "thm": cov0.get("thm"), "fora_do_trio": cov0.get("fora_do_trio")},
               "axiom_report_efetivo_n": len(axm), "proveniencia_n": len(srcm), "nao_lidas_pelo_leitor_v394": 0, "nomes_distintos_print_antigos": len(nomes_antigos), "antigas_identicas": iguais_ant,
               "entradas_antigas_exatas_no_efetivo": exatas, "nomes_v412_perdidos": len(perdidos), "novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas), "sorryAx_no_log_do_audit": AL.count("sorryAx"),
               "delta_vs_v412": {"decl": j1[0], "thm": j1[1]}, "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800,
               "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))), "n_bandeiras": len(flags), "decl_dos_modulos_novos": len(novas_todas),
               "decl_novas_dos_modulos": len(novas_reais), "reatribuidas_as_pedras": reatribuidas, "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "n_modulos_novos": N_NOVOS,
               "quando": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "estatuto": "[REAL] medido por pos_build_kernel_v413.py sobre o log do Audit do sandbox; fora do selo"}
    salvar_json(os.path.join(KD, "KH_N1_v413.json"), kh_json)
    r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
    criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
                 "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas)}
    x19 = "sim" if any(p["path"].endswith("/LightNetStandardWedgeDataBGL.lean") for p in pedras) else "nao"
    chk("x19 = 'nao': nenhum dos %d modulos do recibo e' a LightNetStandardWedgeDataBGL (R31-6: 'sim' <=> a pedra consta do recibo)" % N_NOVOS, x19 == "nao", x19)
    logs_cop = {}
    for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
        b = rd(os.path.join(KD, nome)); logs_cop[nome] = {"bytes": len(b), "sha256": sha(b), "origem": os.path.join(KD, nome), "copiado": False}
    logs_cop["cobertura_linha"] = cov_a
    salvar_json(os.path.join(KD, "LOGS_COPIADOS_v413.json"), logs_cop)
    rc_med = 0 if (rb == 0 and ra == 0) else (rb or ra)
    recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v413", "rc": rc_med, "sorry": n_sorry, "erros": n_err,
              "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
              "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
              "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
              "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
              "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
              "pedras": pedras + pedras_kc, "kernel_corrigido": [{"path": r, "sha256_antes": kc_antes[r]["formal_files_v412"], "sha256_depois": kc_antes[r]["depois_na_arvore"], "declaracoes": kc_decl[r]["nomes"]} for r in KCRELS],
              "formal_files_antes": ff, "axiomas": sorted(TRIO),
              "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
              "criterios": {k: {"medido": v} for k, v in criterios.items()},
              "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v412)", "antes": imp(ff), "depois": imp(ff)},
              "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "nota": "gerado por pos_build_kernel_v413.py (Etapa 1 da v413, 20/11/2026: os modulos novos da v413 e o modulo que ela corrige so' no texto); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v413 e do manifesto novo); o modulo corrigido esta' nas pedras (N1l do B(n): novos ou mudados) e, com o antes e o depois, no campo kernel_corrigido, que a ferramenta nao confere; a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela); "
                      "o build do sandbox C:/t/k413c/final foi INCREMENTAL no que e' antigo (copia de C:/t/k412c/final, o kernel da v412 compilado, com as fontes conferidas por sha256 contra o Nos v412) e compilou os modulos do bundle (" + str(N_NOVOS) + " modulos, na ordem topologica; quais tiveram linha Built neste build esta' em kernel/POS_BUILD_v413.json, campo modo_dos_modulos_no_build); logs em kernel\\; o rito real do Nos compila tudo a frio"}
    ok = all(s["ok"] for s in sinais if not s.get("informativo"))
    salvar_json(os.path.join(KD, "KERNEL_RECIBO_v413.json"), recibo)
    crit = {"contrato": "CRITERIOS_R3_1", "versao": "v413", "preenchido": True, "x19": x19, "esperados": criterios,
            "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v413.json (J1 = diferenca dos TOTAIS do KH-N1 v413 - v412). x19='nao': o recibo v413 lista os " + str(N_NOVOS) + " modulos NOVOS de TGLExt/ e a "
                      "LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392; a gerencia confere e pina o sha256 antes do B(n).",
            "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
    salvar_json(os.path.join(VD, "CRITERIOS_v413.json"), crit)
    pos = {"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "modo_dos_modulos_no_build": modo, "todos_os_modulos_a_frio": todos_a_frio,
           "por_modulo_marcas": por_mod_marcas, "tempos_built_s": tempos, "avisos_por_modulo": avisos, "aviso_conhecido_TowerWedgeIndex": {"linhas": av_conhecido.get("linhas", []), "parece_o_conhecido": conhecido_ok},
           "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe, "n_flags": len(flags), "n_decl_audit": len(axm), "escada": [E0, E0 + len(flags)], "E412": E0,
           "linha_TOTAL": kh_json["linha_TOTAL"], "linha_TOTAL_v412": kh_json["linha_TOTAL_v412"], "delta_vs_v412": kh_json["delta_vs_v412"],
           "pedras_sem_declaracao": sem_decl, "riscos_bn": riscos_bn, "n_declaracoes_no_recibo": n_decl_recibo, "inicio": ini, "fim": fim, "githash_lean": hashes_lean,
           "duracao_build_s": dur_build, "duracao_audit_s": dur_audit, "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "n_ancoras": n_anc, "x19": x19,
           "chaves_antigas": {"n": len(base_flags), "mudam": chaves_mudam},
           "kernel_corrigido": {"modulos": KCMODS, "modo_no_build": modo_kc, "declaracoes": {k: {kk: vv for kk, vv in v.items() if kk != "nomes"} for k, v in kc_decl.items()}, "antes_depois": kc_antes,
                                "dependentes_antigos_sem_linha_Built": dep_sem_built, "n_dependentes_antigos": len(dep_ant_mod)},
           "avisos_modulos_antigos": {"n_modulos": len(antigos_com_aviso), "n_avisos": sum(antigos_com_aviso.values()), "por_modulo": antigos_com_aviso},
           "falhas": [s["checagem"] for s in sinais if not s["ok"] and not s.get("informativo")], "falhas_informativas": [s["checagem"] for s in sinais if not s["ok"] and s.get("informativo")], "backups": BACKUPS}
    salvar_json(os.path.join(KD, "POS_BUILD_v413.json"), pos)
    print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "| bandeiras:", len(flags), "| escada:", [E0, E0 + len(flags)], "| TOTAL:", kh_cov, "| delta_vs_v412:", j1[:2],
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
                salvar_json(os.path.join(KD, "POS_BUILD_v413.json"), {"ok": False, "excecao": tb, "sinais": sinais, "backups": BACKUPS})
        except Exception:
            pass
        sys.exit(2)
    sys.exit(0 if r else 1)

# -*- coding: utf-8 -*-
"""ensaio_mundo_falso_v413.py -- (Etapa 3 da v413, 20/11/2026) o ENSAIO A SECO do esperados, do instalador, do conferidor pos-rito e da reversao
da v413, sem o candidato da Etapa 2 e sem tocar o Nos: monta um MUNDO FALSO numa pasta temporaria (fora de work\\ e do Nos), com:
  * um Nos falso feito de COPIAS da v412 selada (o um.py, o selo, o sidecar, o core, os textos, todo arquivo pinado pelo selo e todo arquivo do kernel
    pinado pelo manifesto; o .lake nao entra) -- o Nos real so' e' LIDO;
  * um candidato SINTETICO (o um.py da v412 com o kernel embutido acrescido dos 21 novos e do corrigido, LIDOS do sandbox k413c, a linha
    UM_VERSION = "v413" e o par _V413_FONTES/_V413_VERBATINS2 com o nome kh_n1_cobertura_v413) e os insumos da Etapa 2 sinteticos;
e roda, com V413_ENSAIO_DIR apontando o mundo: o esperados (positivo e um controle negativo), o instalador (cinco controles negativos, que tem de
recusar SEM escrever no Nos falso, e o positivo), uma SIMULACAO do rito (o que o um.py v413 escreveria: os modulos, o corrigido, a raiz, o core com as
bandeiras e os registros, o selo, o manifesto e o stdout), o conferidor (positivo e sete mutacoes, cada uma tem de reprovar a checagem certa), a
reversao (um controle negativo, que tem de recusar sem escrever, e o positivo, que devolve o Nos falso byte a byte) e confere tudo.
O recibo vai a etapa3\\ENSAIO_MUNDO_FALSO_v413.json; a pasta temporaria e' APAGADA no fim (regra do disco), salvo com --manter.
NAO e' o rito: a simulacao so' imita o que o conferidor le; o que o um.py faz de verdade so' o rito mostra."""
import ast, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
E3 = Path(__file__).resolve().parent; V = E3.parent; V412 = V.parent / "v412"
NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); SB = Path(r"C:\t\k413c\final")
PY = r"C:\Python314\python.exe"; MANTER = "--manter" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
shb = lambda b: hashlib.sha256(b).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
wj = lambda p, d: Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
BASE_TMP = Path(os.environ.get("V413_ENSAIO_BASE") or tempfile.gettempdir())
W = BASE_TMP / ("e3_mundo_falso_v413_" + time.strftime("%Y%m%d_%H%M%S")); N = W / "Nós"
R = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "mundo": str(W), "passos": [], "ok": True}


def passo(nome, ok, detalhe=None):
    R["passos"].append({"passo": nome, "ok": bool(ok), "detalhe": detalhe}); R["ok"] = R["ok"] and bool(ok)
    print(("ok    " if ok else "FALHOU"), nome, "" if ok else str(detalhe)[:900], flush=True)


def roda(script, *args, env_extra=None):
    env = dict(os.environ, V413_ENSAIO_DIR=str(W), PYTHONIOENCODING="utf-8"); env.update(env_extra or {})
    r = subprocess.run([PY, "-B", "-X", "utf8", str(V / script)] + list(args), env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=1800)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def retrato(pasta):
    return {str(p.relative_to(pasta)): sha(p) for p in Path(pasta).rglob("*") if p.is_file()}


try:
    # ------------------------------------------------------------------ 1. o Nos falso (copias da v412 selada)
    selo0 = lj(NOS_REAL / "um_absoluto_selo.json"); assert selo0["um_version"] == "v412"
    (N / "tgl_kernel").mkdir(parents=True)
    for rel in sorted(selo0["sha256"]) + ["um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_pt.txt", "um_absoluto_en.txt"]:
        shutil.copyfile(NOS_REAL / rel, N / rel)
    fmap = lj(NOS_REAL / "tgl_kernel_proof_manifest.json")["formal_files_sha256"]
    for rel in fmap:
        d = N / "tgl_kernel" / Path(*rel.split("/")); d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(NOS_REAL / "tgl_kernel" / Path(*rel.split("/")), d)
    malc = [r for r, h in fmap.items() if sha(N / "tgl_kernel" / Path(*r.split("/"))) != h] + [r for r, h in selo0["sha256"].items() if sha(N / r) != h]
    passo("1. o Nos falso e' copia byte a byte da v412 selada (%d do selo, %d do kernel)" % (len(selo0["sha256"]), len(fmap)), not malc, malc[:5])
    # ------------------------------------------------------------------ 2. o candidato sintetico e os insumos da Etapa 2
    raw = (N / "um.py").read_bytes(); txt = raw.decode("utf-8"); L = txt.splitlines(keepends=True)
    i0 = [i for i, l in enumerate(L) if l.startswith("_EMBEDDED_KERNEL_FILES = {")][0]; j = i0 + 1
    while L[j].rstrip("\r\n") != "}":
        j += 1
    EMB = ast.literal_eval("".join(L[i0:j + 1]).split("=", 1)[1].strip())
    KN = lj(V / "kernel_modulos_novos_v413.json")
    for rel in KN["novos"] + KN["kernel_corrigido"] + ["TGLExt.lean", "TGL/Audit.lean"]:
        b = (SB / Path(*rel.split("/"))).read_bytes(); t_ = b.decode("utf-8"); assert t_.encode("utf-8") == b; EMB[rel] = t_
    novo_dict = "_EMBEDDED_KERNEL_FILES = {\r\n" + "".join("    %r: %r,\r\n" % (k, EMB[k]) for k in sorted(EMB)) + "}\r\n"
    L2 = L[:i0] + [novo_dict] + L[j + 1:]
    iv = [i for i, l in enumerate(L2) if l.startswith("UM_VERSION")]; assert len(iv) == 1
    L2[iv[0]] = 'UM_VERSION = "v413"   # ENSAIO SINTETICO (etapa3\\ensaio_mundo_falso_v413.py): nao e\' o candidato\r\n'
    L2 += ["\r\n", "# ENSAIO SINTETICO: o par da custodia e o nome do registro kh_n1_cobertura_v413\r\n", "_V413_FONTES = {}\r\n", "_V413_VERBATINS2 = {}\r\n"]
    (W / "candidato").mkdir(); CAND = W / "candidato" / "um_v413_candidato_ENSAIO.py"; cb = "".join(L2).encode("utf-8"); CAND.write_bytes(cb)
    c16 = shb(cb)[:16]; o16 = shb(raw)[:16]
    KH = lj(V / "kernel" / "KH_N1_v413.json"); FJ = lj(V / "kernel" / "FLAGS_v413.json")
    e412 = lj(NOS_REAL / "um_absoluto.json")["core"]["external_ladder"]["n_theorems_expected"]
    ctt = (V / "CONTRATO_v413_R1.md").read_text(encoding="utf-8"); s2 = re.search(r"^## 2\. .*?(?=^## 3\. )", ctt, re.M | re.S).group(0)
    PAL = dict(re.findall(r"^- `([a-z0-9_]+_v413)`[^\n]*\n  `([A-Z0-9_]+)`", s2, re.M))
    wj(W / "CANDIDATO_v413.json", {"candidato": str(CAND), "sha16": c16, "sha256": shb(cb), "bytes": len(cb), "base_v412_sha16": o16, "escada": [e412, e412 + FJ["n_flags"]],
                                  "n_bandeiras": FJ["n_flags"], "kernel": {"modulos_novos": KN["n"]}, "registros": sorted(PAL), "ensaio_sintetico": True})
    wj(W / "PREPARACAO_v413_PRONTA.json", {"fechou": True, "candidato": {"caminho": str(CAND), "sha16": c16, "bytes": len(cb)}, "ensaio_sintetico": True})
    wj(W / "PORTAO_DO_PILAR_CANDIDATO_v413.json", {"ok": True, "candidato": {"arquivo": str(CAND), "sha16": c16, "bytes": len(cb)}, "ensaio_sintetico": True})
    wj(W / "TOPO_RATIFICADO_v413_DERIVADO.json", {"ensaio_sintetico": True})
    wj(W / "PINO_RECIBO_PRE_SELO_v413.json", {"contrato": "PINO_RECIBO_PRE_SELO_v413_SALTO_ENSAIO", "utilizavel_como_recibo_pre_selo_do_B_n": True, "versao_nos": "v412", "um_py_sha16_do_nos": o16, "veredito": "ENSAIO_SINTETICO"})
    passo("2. o candidato sintetico (%s, %d B) e os insumos sinteticos da Etapa 2" % (c16, len(cb)), CAND.is_file())
    # ------------------------------------------------------------------ 3. o esperados (negativo e positivo)
    cm = lj(W / "CANDIDATO_v413.json"); cm_ok = dict(cm); cm["sha16"] = "0" * 16; wj(W / "CANDIDATO_v413.json", cm)
    rc, out = roda("esperados_v413_foco.py"); passo("3a. o esperados RECUSA um manifesto de candidato que nao e' do disco (rc 2)", rc == 2 and "nao e' deste candidato" in out, out[-400:])
    wj(W / "CANDIDATO_v413.json", cm_ok)
    rc, out = roda("esperados_v413_foco.py"); passo("3b. o esperados grava ESPERADOS_v413.json do mundo (rc 0)", rc == 0 and (W / "ESPERADOS_v413.json").is_file(), out[-1500:])
    ESP = lj(W / "ESPERADOS_v413.json")
    passo("3c. o ESPERADOS diz o que o mundo tem (candidato, origem, escada, novos, corrigido, exigencias)", ESP["candidato_sha16"] == c16 and ESP["origem_sha16"] == o16 and ESP["escada"] == [e412, e412 + FJ["n_flags"]]
          and len(ESP["bundle_sha256"]) == KN["n"] and set(ESP["kernel_corrigido"]) == set(KN["kernel_corrigido"]) and ESP["exigencias_da_custodia"]["todas"] is True and ESP["ensaio"] is True, {k: ESP.get(k) for k in ("candidato_sha16", "origem_sha16", "escada")})
    # ------------------------------------------------------------------ 4. o instalador: os negativos (recusam sem escrever) e o positivo
    S0 = retrato(N)
    def negativo(nome, prep, desfaz, espera):
        prep(); rc_, out_ = roda("instalar_v413.py"); desfaz()
        passo("4. instalador NEGATIVO: %s (recusa, Nos falso intacto)" % nome, rc_ != 0 and espera in out_ and retrato(N) == S0, out_[-500:])
    tp = W / "TOPO_RATIFICADO_v413_DERIVADO.json"; tpb = tp.read_bytes()
    negativo("sem o topo derivado", lambda: tp.unlink(), lambda: tp.write_bytes(tpb), "TOPO_RATIFICADO_v413_DERIVADO")
    pp = W / "PINO_RECIBO_PRE_SELO_v413.json"; ppb = pp.read_bytes(); d_ = json.loads(ppb); d_["utilizavel_como_recibo_pre_selo_do_B_n"] = False
    negativo("pre-selo do B(n) inutilizavel e sem --sem-pre-selo-bn", lambda: wj(pp, d_), lambda: pp.write_bytes(ppb), "pre-selo do B(n)")
    novo1 = N / "tgl_kernel" / Path(*sorted(ESP["bundle_sha256"])[0].split("/"))
    negativo("um modulo novo ja' no kernel do Nos", lambda: novo1.write_bytes(b"-- ensaio\n"), lambda: novo1.unlink(), "modulos novos")
    kc = N / "tgl_kernel" / Path(*sorted(ESP["kernel_corrigido"])[0].split("/")); kcb = kc.read_bytes()
    negativo("o corrigido do Nos sem o sha antigo", lambda: kc.write_bytes(kcb + b"\n"), lambda: kc.write_bytes(kcb), "kernel do Nos nao e' o pinado")
    ep = W / "ESPERADOS_v413.json"; epb = ep.read_bytes(); d2 = json.loads(epb); d2["exigencias_da_custodia"]["todas"] = False
    negativo("o candidato sem as exigencias da custodia", lambda: wj(ep, d2), lambda: ep.write_bytes(epb), "exigencias da custodia")
    rc, out = roda("instalar_v413.py"); passo("4p. instalador POSITIVO (rc 0; o um.py do Nos falso e' o candidato; os backups batem)", rc == 0 and sha(N / "um.py")[:16] == c16, out[-1500:])
    APs = sorted((W / "registro").glob("APLICADO_AO_CANONICO_*.json")); AP = lj(APs[-1])
    passo("4q. o registro tem os backups (o conjunto selado, o selo, o sidecar, os .txt, a raiz, o Audit e o corrigido) e a lista dos novos",
          len(AP["backups"]) == len(selo0["sha256"]) + 6 + len(ESP["kernel_corrigido"]) and AP["modulos_novos_v413"]["n"] == KN["n"] and AP["pino_recibo_pre_selo"]["ok"] is True, {"n_backups": len(AP["backups"])})
    rc, out = roda("instalar_v413.py"); passo("4r. instalador NEGATIVO: rodar de novo depois de instalar (a origem ja' nao e' a v412) recusa", rc != 0 and "nao e' a v412 selada" in out, out[-300:])
    S_inst = retrato(N)
    # ------------------------------------------------------------------ 5. a SIMULACAO do rito (o que o conferidor le)
    K = N / "tgl_kernel"
    for rel in list(ESP["bundle_sha256"]) + list(ESP["kernel_corrigido"]) + ["TGLExt.lean", "TGL/Audit.lean"]:
        d = K / Path(*rel.split("/")); tmp = d.with_name(d.name + ".tmp_sim"); tmp.write_bytes((SB / Path(*rel.split("/"))).read_bytes()); tmp.replace(d)   # troca atomica: nunca escrita no lugar
    R1 = lj(N / "um_absoluto.json"); core = R1["core"]; kf = core["kernel_formalization"]
    for k in ESP["bandeiras_novas_chaves"]:
        kf[k] = True
    ax = kf["axiom_report"]; TRIO = ["Classical.choice", "Quot.sound", "propext"]
    for dcl in ESP["kernel"]["declaracoes_novas"]:
        ax.setdefault(dcl, list(TRIO))
    i_ = 0
    while len(ax) < ESP["kernel"]["kh_decl"]:
        ax["ENSAIO_SINTETICO.decl_%05d" % i_] = list(TRIO); i_ += 1
    for nome, w in ESP["registros_v413"].items():
        core[nome] = {"verdict": w, "all_verified": True, "checks": [{"ensaio": True}], "registro": "ENSAIO SINTETICO"}
    core["kh_n1_cobertura_v413"] = {"verdict": "TGL_KH_N1_COBERTURA_V413__ENSAIO_SINTETICO__GATE_UNMOVED", "all_verified": True, "lido": {"constantes_cobertas": len(ax), "teoremas_cobertos": ESP["kernel"]["kh_thm"]}}
    core["guarda_frases_v413"] = {n: {"ensaio": True} for n in ESP["registros_v413"]}
    est = core["estatuto_da_prova_v391"]; est["verdict"] = est["verdict"].replace(str(ESP["escada"][0]), str(ESP["escada"][1]))
    (N / "um_absoluto.json").write_text(json.dumps(R1, ensure_ascii=False), encoding="utf-8")
    man = lj(N / "tgl_kernel_proof_manifest.json")
    for rel in list(ESP["bundle_sha256"]) + list(ESP["kernel_corrigido"]) + ["TGLExt.lean", "TGL/Audit.lean"]:
        man["formal_files_sha256"][rel] = sha(K / Path(*rel.split("/")))
    (N / "tgl_kernel_proof_manifest.json").write_text(json.dumps(man, ensure_ascii=False), encoding="utf-8")
    selo1 = dict(selo0); selo1["um_version"] = "v413"; selo1["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S"); selo1["sha256"] = {k: sha(N / k) for k in selo0["sha256"]}
    (N / "um_absoluto_selo.json").write_text(json.dumps(selo1, ensure_ascii=False, indent=1), encoding="utf-8")
    chave = ESP["pilar"]["key"]
    STDOUT = ("Inscreva o UM para iniciar: \nO UM foi inscrito. I = 1. omega(I) = 1.\n"
              "[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de 2026-10-05 12:47:39 (chave %s) -- o pilar nao e' objeto desta versao (_QP_REUSE_V386)\n"
              "  lake build: True ; audit: 0 ; sentinelas: True\n  >>> TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED <<<\n"
              "  teoremas limpos: %d/%d ; ENSAIO SINTETICO\n  >>> FAIL_CLOSED_SELFTEST_PASSED <<<\nRITO_RC=0\n") % (chave, ESP["escada"][1], ESP["escada"][1])
    (N / "rodada_v413_stdout.txt").write_text(STDOUT, encoding="utf-8")
    passo("5. a simulacao do rito escreveu os modulos, o corrigido, a raiz, o core, o manifesto, o selo e o stdout", True)
    # ------------------------------------------------------------------ 6. o conferidor: positivo e mutacoes
    rc, out = roda("conferir_pos_rito_v413_foco.py"); cf = lj(W / "CONFERENCIA_POS_RITO_v413_FOCO_ENSAIO.json")
    passo("6p. o conferidor no mundo simulado: TUDO BATE (%d checagens)" % len(cf["checagens"]), rc == 0 and cf["ok"] is True, [c for c in cf["checagens"] if not c["ok"]][:6] or out[-800:])

    def mutacao(nome, alvo_checagem, arq, novo_bytes):
        orig = arq.read_bytes(); arq.write_bytes(novo_bytes)
        try:
            rc_, out_ = roda("conferir_pos_rito_v413_foco.py"); cf_ = lj(W / "CONFERENCIA_POS_RITO_v413_FOCO_ENSAIO.json")
        finally:
            arq.write_bytes(orig)
        falhas = [c["checagem"] for c in cf_["checagens"] if not c["ok"]]
        passo("6. conferidor MUTACAO: %s -> reprova «%s»" % (nome, alvo_checagem), rc_ == 1 and any(alvo_checagem in f for f in falhas), falhas)
    kcn = K / Path(*sorted(ESP["kernel_corrigido"])[0].split("/"))
    mutacao("o corrigido com o texto antigo", "o modulo CORRIGIDO", kcn, kcb)
    nv = K / Path(*sorted(ESP["bundle_sha256"])[0].split("/"))
    mutacao("um modulo novo com um byte a mais", "modulos novos estao no kernel", nv, nv.read_bytes() + b"\n")
    sp = N / "rodada_v413_stdout.txt"
    mutacao("o stdout anuncia o calculo do pilar", "o pilar foi REAPROVEITADO", sp, (STDOUT.replace("RITO_RC=0", "[v384] pilar quantico: o trabalhador da GPU foi lancado (PID 1), em paralelo; chave %s\nRITO_RC=0" % chave)).encode("utf-8"))
    mutacao("o stdout termina com RITO_RC=1", "termina com RITO_RC=0", sp, STDOUT.replace("RITO_RC=0", "RITO_RC=1").encode("utf-8"))
    sl = N / "um_absoluto_selo.json"; s_ = json.loads(sl.read_bytes()); s_["um_version"] = "v412"
    mutacao("o selo com um_version v412", "um_version v413", sl, json.dumps(s_, ensure_ascii=False).encode("utf-8"))
    cp = N / "um_absoluto.json"; cpb = cp.read_bytes(); c_ = json.loads(cpb); r0 = sorted(ESP["registros_v413"])[0]; c_["core"][r0]["verdict"] = c_["core"][r0]["verdict"] + "__CONFIRMED"
    mutacao("um veredito novo com a palavra proibida", "guarda de palavra proibida do rito", cp, json.dumps(c_, ensure_ascii=False).encode("utf-8"))
    c_ = json.loads(cpb); c_["core"]["kernel_formalization"].pop(ESP["bandeiras_novas_chaves"][0])
    mutacao("uma bandeira nova a menos", "bandeiras True novas", cp, json.dumps(c_, ensure_ascii=False).encode("utf-8"))
    rc, out = roda("conferir_pos_rito_v413_foco.py"); passo("6z. depois das mutacoes desfeitas, o conferidor volta a TUDO BATE", rc == 0, out[-300:])
    # ------------------------------------------------------------------ 7. a reversao: negativo (backup ausente: recusa sem escrever) e positivo
    S_rito = retrato(N); bk = Path(AP["backups"]["um_absoluto.json"]["backup"]); bk2 = bk.with_name(bk.name + ".escondido_ensaio"); bk.rename(bk2)
    rc, out = roda("reverter_v413.py"); bk2.rename(bk)
    passo("7a. reversao NEGATIVA: um backup ausente -> recusa sem escrever no Nos falso", rc != 0 and "backup ausente" in out and retrato(N) == S_rito and not list((W / "registro").glob("tentativa_v413_rito_falhou_*")), out[-400:])
    rc, out = roda("reverter_v413.py"); S1 = retrato(N)
    dif = sorted(k for k in S0 if S1.get(k) != S0[k]); novos_arq = sorted(k for k in S1 if k not in S0)
    sobra = [k for k in novos_arq if ".bak_" not in k and k != "rodada_v413_stdout.txt"]
    passo("7p. reversao POSITIVA: rc 0; todo arquivo do Nos falso de antes voltou byte a byte; os novos foram a quarentena; so' sobram os backups e o stdout da tentativa",
          rc == 0 and not dif and not sobra, {"diferentes": dif[:8], "sobras": sobra[:8], "saida": out[-600:]})
finally:
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
    R["apagado"] = False
    if not MANTER and W.exists():
        shutil.rmtree(W, ignore_errors=True); R["apagado"] = not W.exists()
    out_p = E3 / "ENSAIO_MUNDO_FALSO_v413.json"
    if out_p.exists():
        out_p.with_name(out_p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out_p.read_bytes())
    tmp = out_p.with_name(out_p.name + ".tmp"); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8"); tmp.replace(out_p)
    print("ENSAIO DO MUNDO FALSO v413:", "TUDO COMO ESPERADO" if R["ok"] else "FORA DO ESPERADO", "| passos", len(R["passos"]), "| ok", sum(1 for p in R["passos"] if p["ok"]), "| mundo apagado:", R["apagado"])
sys.exit(0 if R["ok"] else 1)

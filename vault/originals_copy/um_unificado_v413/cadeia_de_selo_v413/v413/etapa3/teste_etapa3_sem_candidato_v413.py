# -*- coding: utf-8 -*-
"""teste_etapa3_sem_candidato_v413.py -- (Etapa 3 da v413, 20/11/2026; molde: os teste_*_sem_candidato_v412.py) o que se ensaia SEM o candidato da Etapa 2,
sem tocar o Nos, a placa, o treino ou o C:\\t\\k413c:
  T1 o vigia do pilar (pilar_no_stdout_v413.py) em stdouts sinteticos: reuso com a chave (0), com outra chave (4), calculo (3), ainda nao (1), sem arquivo (2);
  T2 o LACO do vigia do pilar, extraido BYTE A BYTE do rito_v413.sh e rodado no sh com um lancador falso: no calculo, grava PILAR_PARADA_v413.txt e manda
     TERM ao lancador; no reuso, sai sem tocar o lancador;
  T3 o portao do pilar REAL (portao_ambiente_pilar_v413.py, com o mesmo python do rito, sem -I; nao importa torch, nao toca a placa) contra o cache real do
     pilar (o veredito de HOJE e' dito: se recusar, o rito pararia) e o controle negativo num cache FALSO com o ambiente trocado (tem de recusar, 19);
  T4 sh -n no rito_v413.sh e na cadeia_pos_rito_v413.sh;
  T5 os diffs: diffs_v413.py --reproduzir-v412 refaz os dois diffs publicados da v412 byte a byte (o controle positivo da maquina);
  T6 a guarda do titulo: o Nos de hoje (v412) passa com v412 e e' recusado com v413 (a arvore ainda diz v412);
  T7 o esperados sem o candidato recusa com mensagem clara (rc 2) e nao grava nada;
  T8 todos os .py desta etapa compilam.
Recibo em etapa3\\TESTE_ETAPA3_SEM_CANDIDATO_v413.json; as pastas temporarias saem no fim."""
import glob, hashlib, json, os, py_compile, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
E3 = Path(__file__).resolve().parent; V = E3.parent; V412 = V.parent / "v412"
PY = sys.executable; SH = shutil.which("sh") or r"C:\Program Files\Git\usr\bin\sh.exe"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
R = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "testes": [], "ok": True}
TMP = Path(tempfile.mkdtemp(prefix="e3_teste_v413_", dir=os.environ.get("V413_ENSAIO_BASE") or None))


def t(nome, ok, det=None):
    R["testes"].append({"teste": nome, "ok": bool(ok), "detalhe": det}); R["ok"] = R["ok"] and bool(ok)
    print(("ok    " if ok else "FALHOU"), nome, "" if ok else str(det)[:700], flush=True)


def run(cmd, cwd=None, env=None, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


try:
    E412 = json.loads((V412 / "ESPERADOS_v412.json").read_text(encoding="utf-8")); CH = E412["pilar"]["key"]
    cdir = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar") / CH
    cenv = json.loads((cdir / "result.json").read_text(encoding="utf-8"))["env"]
    env_cache = {k: cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu")}
    ESPS = TMP / "ESPERADOS_v413.json"
    ESPS.write_text(json.dumps({"ENSAIO_SINTETICO": True, "pilar": dict(E412["pilar"], cache_dir=str(cdir), env_do_cache=env_cache)}, ensure_ascii=False), encoding="utf-8")
    # T1
    casos = {"reuso": ("[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de 2026-10-05 12:47:39 (chave %s) -- ...\n" % CH, 0, "REUSO_OK"),
             "outra_chave": ("[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de x (chave %s) -- ...\n" % ("f" * 24), 4, "CHAVE_ERRADA"),
             "calculo": ("[v384] pilar quantico: o trabalhador da GPU foi lancado (PID 7), em paralelo com o kernel; chave %s\n" % CH, 3, "CALCULA"),
             "ainda_nao": ("Inscreva o UM para iniciar:\nO UM foi inscrito.\n", 1, "AINDA_NAO")}
    for nome, (txt, rc_esp, pal) in casos.items():
        p = TMP / ("stdout_%s.txt" % nome); p.write_text(txt, encoding="utf-8")
        rc, out = run([PY, "-B", "-X", "utf8", str(V / "pilar_no_stdout_v413.py"), str(p), str(ESPS)])
        t("T1 vigia do pilar: %s -> %s (rc %d)" % (nome, pal, rc_esp), rc == rc_esp and out.strip().startswith(pal), (rc, out[-200:]))
    rc, out = run([PY, "-B", "-X", "utf8", str(V / "pilar_no_stdout_v413.py"), str(TMP / "nao_existe.txt"), str(ESPS)])
    t("T1 vigia do pilar: sem arquivo -> ERRO (rc 2)", rc == 2 and out.startswith("ERRO"), (rc, out[-200:]))
    # T2 o laco do vigia, extraido do rito_v413.sh
    rito = (V / "rito_v413.sh").read_text(encoding="utf-8")
    i = rito.index("[ -f \"$PK/PILAR_PARADA_v413.txt\" ] && mv -f"); j = rito.index(") &\n", i) + len(") &\n")
    laco = rito[i:j]
    for cen, linha, espera_morte in (("calculo", casos["calculo"][0], True), ("reuso", casos["reuso"][0], False)):
        d = TMP / ("laco_" + cen); d.mkdir()
        shutil.copyfile(V / "pilar_no_stdout_v413.py", d / "pilar_no_stdout_v413.py"); shutil.copyfile(ESPS, d / "ESPERADOS_v413.json")
        (d / "rodada_v413_stdout.txt").write_text("Inscreva o UM\n" + linha, encoding="utf-8")
        script = ("PK=\"$(pwd)\"; LOGS=\"$PK/log.txt\"; : > \"$LOGS\"\n"
                  "( trap 'echo TERM_RECEBIDO > \"$PK/lancador_falso.txt\"; exit 0' TERM; while :; do sleep 1; done ) &\nPAI=$!\nsleep 1\n" + laco +
                  "VPP=$!\nk=0; while kill -0 \"$VPP\" 2>/dev/null && [ $k -lt 40 ]; do sleep 1; k=$((k+1)); done\nsleep 2\n"
                  "if kill -0 \"$PAI\" 2>/dev/null; then echo LANCADOR_VIVO >> \"$LOGS\"; kill -TERM \"$PAI\" 2>/dev/null; sleep 2; fi\nrm -f \"$PK/.vigia_pilar_ativo\"\nexit 0\n")
        (d / "teste_laco.sh").write_text(script, encoding="utf-8", newline="\n")
        rc, out = run([SH, "teste_laco.sh"], cwd=str(d), timeout=120)
        log = (d / "log.txt").read_text(encoding="utf-8") if (d / "log.txt").exists() else ""
        parada = (d / "PILAR_PARADA_v413.txt").exists(); morto = (d / "lancador_falso.txt").exists() and "LANCADOR_VIVO" not in log
        if espera_morte:
            ok = parada and morto and "PARO o rito" in log
        else:
            ok = (not parada) and "LANCADOR_VIVO" in log and "VIGIA DO PILAR: REUSO_OK" in log
        t("T2 o laco do vigia do pilar (extraido do rito): %s" % cen, ok, {"rc": rc, "parada": parada, "lancador_recebeu_TERM": (d / "lancador_falso.txt").exists(), "log": log[-400:], "saida": out[-300:]})
    # T3 o portao do pilar: real e negativo (cache falso)
    rc, out = run([PY, "-B", "-X", "utf8", str(V / "portao_ambiente_pilar_v413.py"), str(ESPS)])
    rec_p = sorted(TMP.glob("PORTAO_AMBIENTE_PILAR_v413_*.json")); pr = json.loads(rec_p[-1].read_text(encoding="utf-8")) if rec_p else {}
    t("T3 o portao do pilar (real; nao toca a placa) roda e diz o veredito de hoje: %s" % pr.get("veredito"), rc in (0, 19) and pr.get("toca_a_placa") is False,
      {"rc": rc, "saida": out[-400:], "diferencas": pr.get("diferencas")})
    R["portao_de_hoje"] = {"rc": rc, "veredito": pr.get("veredito"), "diferencas": pr.get("diferencas"), "cache": pr.get("cache"), "agora": {k: (pr.get("agora") or {}).get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu_nomes_do_windows")}}
    cf = TMP / "cache_falso"; cf.mkdir(); d_ = json.loads((cdir / "result.json").read_text(encoding="utf-8")); d_["env"]["numpy"] = "0.0.0-ensaio"
    b_ = json.dumps(d_, ensure_ascii=False).encode("utf-8"); (cf / "result.json").write_bytes(b_); h_ = hashlib.sha256(b_).hexdigest(); (cf / "result.json.sha256").write_text(h_, encoding="ascii")
    env2 = dict(env_cache, numpy="0.0.0-ensaio"); ESPN = TMP / "neg" / "ESPERADOS_v413.json"; ESPN.parent.mkdir()
    ESPN.write_text(json.dumps({"ENSAIO_SINTETICO": True, "pilar": dict(E412["pilar"], cache_dir=str(cf), result_sha256=h_, env_do_cache=env2)}, ensure_ascii=False), encoding="utf-8")
    rc, out = run([PY, "-B", "-X", "utf8", str(V / "portao_ambiente_pilar_v413.py"), str(ESPN)])
    t("T3 o portao do pilar RECUSA um cache com o ambiente trocado (rc 19)", rc == 19 and "PORTAO_PILAR_RECUSA" in out, (rc, out[-300:]))
    # T4
    for s in (V / "rito_v413.sh", V / "pos_rito" / "cadeia_pos_rito_v413.sh"):
        rc, out = run([SH, "-n", str(s)])
        t("T4 sh -n %s" % s.name, rc == 0, out[-300:])
    # T5
    dd = TMP / "diffs_v412"; rc, out = run([PY, "-I", "-B", "-X", "utf8", str(V / "pos_rito" / "diffs_v413.py"), "--reproduzir-v412", str(dd)], timeout=1800)
    t("T5 diffs_v413.py --reproduzir-v412: os dois diffs publicados da v412, byte a byte", rc == 0 and "BYTE A BYTE" in out, out[-500:])
    # T6
    rc, out = run([PY, "-I", "-B", "-X", "utf8", str(V / "pos_rito" / "guarda_titulo_versao_v413.py"), "v412"])
    t("T6 a guarda do titulo passa no Nos de hoje com v412", rc == 0 and "LIMPA" in out, out[-300:])
    rc, out = run([PY, "-I", "-B", "-X", "utf8", str(V / "pos_rito" / "guarda_titulo_versao_v413.py"), "v413", "--sem-handoff"])
    t("T6 a guarda do titulo RECUSA o Nos de hoje com v413 (a arvore diz v412)", rc == 1 and "RECUSA" in out and "A_PROVA_DA_QG_TGL_arvore.md" in out, out[-300:])
    # T7
    antes = sorted(p.name for p in V.glob("ESPERADOS_v413.json*"))
    if not (V / "PREPARACAO_v413_PRONTA.json").exists():
        rc, out = run([PY, "-B", "-X", "utf8", str(V / "esperados_v413_foco.py")])
        t("T7 o esperados sem o fecho da Etapa 2 recusa (rc 2) e nao grava", rc == 2 and "RECUSO" in out and sorted(p.name for p in V.glob("ESPERADOS_v413.json*")) == antes, out[-300:])
    else:
        t("T7 (pulado: o fecho da Etapa 2 ja' existe; o esperados se roda com o candidato)", True)
    # T8
    falhas = []
    for p in sorted(list(V.glob("*.py")) + list((V / "pos_rito").glob("*.py")) + list(E3.glob("*.py"))):
        if p.name.startswith(("esperados_v413", "instalar_v413", "reverter_v413", "conferir_pos_rito_v413", "montar_handoff_e_linhagem_v413", "guarda_privada_v413", "portao_ambiente_pilar_v413",
                              "pilar_no_stdout_v413", "carimbar_stdout_v413", "diffs_v413", "guarda_titulo_versao_v413", "adaptar_arvore_da_prova_v413", "derivar_rito_e_carimbo_v413",
                              "ensaio_mundo_falso_v413", "teste_etapa3_sem_candidato_v413", "gerar_pronto_etapa3_v413")):
            try:
                py_compile.compile(str(p), cfile=str(TMP / (p.name + "c")), doraise=True)
            except py_compile.PyCompileError as e:
                falhas.append((p.name, str(e)[:200]))
    t("T8 os .py da Etapa 3 compilam", not falhas, falhas)
finally:
    shutil.rmtree(TMP, ignore_errors=True); R["temporarios_apagados"] = not TMP.exists()
    out_p = E3 / "TESTE_ETAPA3_SEM_CANDIDATO_v413.json"
    if out_p.exists():
        out_p.with_name(out_p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(out_p.read_bytes())
    tmp = out_p.with_name(out_p.name + ".tmp"); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8"); tmp.replace(out_p)
    print("TESTES DA ETAPA 3 SEM O CANDIDATO:", "TUDO COMO ESPERADO" if R["ok"] else "FORA DO ESPERADO", "| testes", len(R["testes"]), "| ok", sum(1 for x in R["testes"] if x["ok"]))
sys.exit(0 if R["ok"] else 1)

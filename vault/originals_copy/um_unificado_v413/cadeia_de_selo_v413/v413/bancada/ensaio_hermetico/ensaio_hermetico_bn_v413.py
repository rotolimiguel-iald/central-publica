# -*- coding: utf-8 -*-
"""ensaio_hermetico_bn_v413.py -- os testes HERMETICOS do B(n) da v413 (ORDEM_BN_v413.md, «Teste sem executar o B(n)»): copias dos scripts num mundo falso (mundo_falso_bn_v413.py, no scratchpad), dados de mentira,
o esboco R3.6 REAL so' em --sandbox --sem-bateria contra a Bancada FALSA (para o recibo do salto ter a forma real), servidores FALSOS na porta 18799 (processos criados aqui e parados pelo PID deles), e as leituras
reais permitidas (o delta_bn importado lendo a producao; o livro do quadro conferido; a conferencia A contra a porta fechada da Bancada real; o controle negativo do conferidor sobre os scripts reais).
NAO roda o ensaio pre-selo real, o pos-selo, o APLICAR, nem liga, para ou toca o servico real. Grava o resultado em RESULTADO_ENSAIO_HERMETICO_BN_v413.json ao lado.
uso: python -I -B -X utf8 ensaio_hermetico_bn_v413.py <pasta de ensaio nova (fora de work)>"""
import datetime
import glob
import hashlib
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mundo_falso_bn_v413 as MF  # noqa: E402

R = os.path.abspath(sys.argv[1])
PY = sys.executable
REAL_BN = MF.REAL_BN
shaf = MF.shaf
RES = []
PIDS = []


def reg(nome, ok, obs=None, esp=None):
    RES.append({"teste": nome, "ok": bool(ok), "observado": obs, "esperado": esp})
    print(("PASSA " if ok else "FALHA "), nome, "" if ok else ("| obs=%s" % str(obs)[:400]))


def py(script, args=(), env_extra=None, cwd=None, timeout=900):
    env = dict(os.environ)
    for k in [k for k in env if k.startswith("V413_") or k in ("FAKE_IALD_FALHA", "CUDA_VISIBLE_DEVICES")]:
        env.pop(k)
    env.update(env_extra or {})
    r = subprocess.run([PY, "-I", "-B", "-X", "utf8", script] + list(args), capture_output=True, text=True, encoding="utf-8", env=env, cwd=cwd or os.path.dirname(script), stdin=subprocess.DEVNULL, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def porta_aberta(p):
    s = socket.socket(); s.settimeout(1)
    try:
        return s.connect_ex(("127.0.0.1", p)) == 0
    finally:
        s.close()


def parar_pid(pid):
    """so' o PID que ESTE ensaio criou (nunca por nome)."""
    if pid in PIDS:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass
        for _ in range(30):
            if not porta_aberta(MF.PORTA_FALSA):
                break
            time.sleep(0.3)


def lj(p):
    return json.load(open(p, encoding="utf-8"))


def wj(p, o):
    MF.escreve(p, MF.jdump(o))


assert not porta_aberta(MF.PORTA_FALSA), "a porta de ensaio %d ja esta' em uso" % MF.PORTA_FALSA
assert not os.path.exists(MF.SANDBOX_FALSO), "o sandbox de ensaio %s ja existe" % MF.SANDBOX_FALSO
M = MF.montar(R)
BN, V413, NOSF, BF = M["BN"], M["V413"], M["NOS"], M["B"]
S = lambda n: os.path.join(BN, n)
OUTB = os.path.join(V413, "bateria_pre_selo")
reg("mundo falso montado (Nos v412, Bancada B20-v411 pinando a v411, cadeia de selo, quadro com 1687 e 1689, copias dos scripts com o delta_bn reapontado)", os.path.isfile(S("delta_bn_v413.py")), R)

# ======================================================================== A. o pre-selo do salto no mundo falso
rc, o, e = py(S("gerar_e_pinar_cadeia_v413.py"))
reg("A1 gerar_e_pinar_cadeia_v413 (copia): o gerador REAL da R3.4 gera a cadeia v411 -> v412 do mundo falso e o esboco R3.6 REAL a confere (Bancada no inicio, Nos no fim); o pino e' gravado", rc == 0 and os.path.isfile(os.path.join(V413, "cadeia_de_selos_v411_v412", "PINO_CADEIA_DE_SELOS_v411_v412.json")), [rc, (o + e)[-400:]])
rc, o, e = py(S("gerar_bateria_v412_pre_selo_v413.py"))
reg("A2 gerar_bateria_v412_pre_selo_v413 (copia): o gerador REAL da bateria, com o pino minimo do candidato, gera a bateria da v412; conferida pelo esboco (carregar_bateria, pinos da versao)", rc == 0, [rc, (o + e)[-400:]])
PC = lj(os.path.join(V413, "cadeia_de_selos_v411_v412", "PINO_CADEIA_DE_SELOS_v411_v412.json"))
PB = lj(os.path.join(V413, "bateria_v412_pre_selo", "PINOS_BATERIA_v412.json"))
ESB = lj(os.path.join(M["CS"], "v411", "PINOS_BN_v411.json"))["esboco_R3_6"]["path"]


def estabilizar(raizes, limite=60):
    """o NTFS atualiza com atraso o mtime de uma pasta na entrada do diretorio-pai (o que o scandir le): numa arvore recem-criada, a primeira fotografia pode ver o valor velho. Antes da fotografia
    'antes', espera ate' o scandir e o os.stat concordarem em toda pasta das arvores falsas (a producao real nao foi escrita ha' dias; la' isso nao ocorre)."""
    t0 = time.time()
    while time.time() - t0 < limite:
        difs = []
        for raiz in raizes:
            for d_, subs, _ in os.walk(raiz):
                with os.scandir(d_) as it:
                    for e_ in it:
                        if e_.is_dir(follow_symlinks=False) and e_.stat(follow_symlinks=False).st_mtime_ns != os.stat(e_.path).st_mtime_ns:
                            difs.append(e_.path)
        if not difs:
            return True
        time.sleep(1)
    return False


reg("as arvores falsas estabilizadas antes da fotografia 'antes' (mtime de pasta do scandir == os.stat)", estabilizar([BF, NOSF]), None)
os.makedirs(os.path.join(MF.SANDBOX_FALSO, "snap"))
rc, o, e = py(S("snap_producao_v413.py"), ["antes", os.path.join(MF.SANDBOX_FALSO, "snap")])
reg("A3a snap antes (copia): fotografa a Bancada falsa e o Nos falso", rc == 0, [rc, (o + e)[-300:]])
SAIDA_ESB = os.path.join(MF.SANDBOX_FALSO, "esboco_pre")
rc, o, e = py(ESB, ["--bancada", BF, "--nos", NOSF, "--versao", "v412", "--fase", "pre_selo", "--modo", "ensaio", "--bateria", PB["bateria"]["path"], "--bateria-sha256", PB["bateria"]["sha256"],
                    "--cadeia-de-selos", PC["cadeia"]["path"], "--cadeia-de-selos-sha256", PC["cadeia"]["sha256"], "--saida", SAIDA_ESB, "--sandbox", "--sem-bateria"], cwd=MF.SANDBOX_FALSO)
imp = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("A3b o esboco R3.6 REAL (--sandbox --sem-bateria) contra a Bancada FALSA atrasada: veredito do salto REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA (o mundo falso e' aceito pelo esboco)",
    rc == 0 and imp.get("veredito") == "REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA", [rc, imp.get("veredito"), imp.get("recusa")])
# o recibo com a forma real; a bateria (pulada no esboco) e' trocada por um resultado PASSA de mentira, com T01 e T15
rec = lj(imp["recibo"])
rec["bateria_resultado"] = {"n": 3, "passa": 2, "falha": 0, "nao_executado": 1, "veredito": "BATERIA_PASSA",
                            "testes": [{"id": "T01_IDENTIDADE", "resultado": "PASSA"}, {"id": "T15_SONDAS", "resultado": "PASSA"}, {"id": "T17_LEAN_KERNEL", "resultado": "NAO_EXECUTADO", "detalhe": "nao pertence a fase pre_selo (fases: ['pos_selo'])"}]}
ENS = os.path.join(OUTB, "ensaio_1")
RP = os.path.join(ENS, os.path.basename(imp["recibo"]))
wj(RP, rec)
wj(os.path.join(ENS, "recibos", "T12_T13_T14_ATRATOR.json"), {"runs": {"T12_optical_r3": {"passa": True}, "T13_adendo1_r1": {"passa": True}, "T14_controle_afim": {"passa": True}}, "adendo_de_pino": {"entrada_do_um_py": "falsa"}})
MF.escreve(os.path.join(OUTB, "etapa1_stdout.txt"), json.dumps({"veredito": rec["veredito"], "recusa": None, "recibo": RP, "recibo_sha256": shaf(RP)}) + "\nETAPA1_RC=0\n")
rc, o, e = py(S("snap_producao_v413.py"), ["depois", os.path.join(MF.SANDBOX_FALSO, "snap")])
reg("A3c snap depois (copia)", rc == 0, [rc, (o + e)[-300:]])
rc, o, e = py(S("conferir_recibo_pre_selo_salto_v413.py"))
cf = lj(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json")) if os.path.exists(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json")) else {}
reg("A4 conferir_recibo_pre_selo_salto_v413 (C.1): o esboco ACEITA o recibo do salto com a cadeia; todas as condicoes passam; os 9 controles negativos recusam pelo codigo certo",
    rc == 0 and cf.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and cf.get("n_controles_como_esperado") == len(cf.get("controles_negativos") or []) == 9 and cf.get("n_condicoes_ok") == cf.get("n_condicoes"),
    [rc, cf.get("n_condicoes_ok"), cf.get("n_condicoes"), cf.get("n_controles_como_esperado"), cf.get("motivos_de_nao_ser_utilizavel"), (o + e)[-300:]])
rc, o, e = py(S("snap_producao_v413.py"), ["final", os.path.join(MF.SANDBOX_FALSO, "snap")])
reg("A5 snap final (copia)", rc == 0, [rc, (o + e)[-300:]])
rc, o, e = py(S("gerar_pino_recibo_pre_selo_v413.py"), [os.path.join(MF.SANDBOX_FALSO, "snap")])
PINO = os.path.join(V413, "PINO_RECIBO_PRE_SELO_v413.json")
pj = lj(PINO) if os.path.exists(PINO) else {}
reg("A6 gerar_pino_recibo_pre_selo_v413 (1.1): veredito EXATO do salto, producao intacta, recibo desta rodada: utilizavel e rc 0; o pino traz a cadeia e o salto",
    rc == 0 and pj.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and pj.get("veredito") == pj.get("veredito_exigido") and (pj.get("cadeia_de_selos") or {}).get("sha256") == PC["cadeia"]["sha256"] and isinstance(pj.get("salto"), dict),
    [rc, pj.get("utilizavel_como_recibo_pre_selo_do_B_n"), pj.get("motivos_de_nao_ser_utilizavel"), (o + e)[-300:]])
# negativos do conferir e do pino (a saida positiva fica guardada e volta depois)
def guardar(p):
    if os.path.exists(p):
        os.replace(p, p + ".positivo")


def voltar(p):
    if os.path.exists(p + ".positivo"):
        if os.path.exists(p):
            os.remove(p)
        os.replace(p + ".positivo", p)


raw_rec = open(RP, "rb").read()
for nome_neg, mut, cond in (("veredito JA_SINCRONIZADA", lambda r_: r_.__setitem__("veredito", "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA"), "veredito_exato_do_salto"),
                            ("salto.de.deployment_id adulterado", lambda r_: r_["salto"]["de"].__setitem__("deployment_id", "B19-v410-20261111-R1"), "salto_do_recibo_igual_ao_que_a_cadeia_e_a_bancada_dizem")):
    guardar(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json"))
    r2 = json.loads(raw_rec.decode("utf-8")); mut(r2); wj(RP, r2)
    MF.escreve(os.path.join(OUTB, "etapa1_stdout.txt"), json.dumps({"veredito": r2["veredito"], "recibo": RP, "recibo_sha256": shaf(RP)}) + "\nETAPA1_RC=0\n")
    rc, o, e = py(S("conferir_recibo_pre_selo_salto_v413.py"))
    c2 = lj(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json"))
    falhou = [c_["nome"] for c_ in c2["condicoes"] if not c_["ok"]]
    reg("NA conferir com o recibo de %s: rc 1, nao utilizavel, a condicao %s falha e o esboco recusa" % (nome_neg, cond), rc == 1 and c2["utilizavel_como_recibo_pre_selo_do_B_n"] is False and cond in falhou and c2["esboco_aceita"] is False,
        [rc, falhou, c2.get("recusa_do_esboco")])
    os.remove(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json"))
    voltar(os.path.join(OUTB, "conferencia_pelo_esboco_v413.json"))
MF.escreve(RP, raw_rec)
MF.escreve(os.path.join(OUTB, "etapa1_stdout.txt"), json.dumps({"veredito": rec["veredito"], "recusa": None, "recibo": RP, "recibo_sha256": shaf(RP)}) + "\nETAPA1_RC=0\n")
# pino com a producao alterada entre as fotos (uma copia das fotos; o arquivo alterado e' do mundo falso e volta)
SN2 = os.path.join(MF.SANDBOX_FALSO, "snap_neg")
os.makedirs(SN2)
for n in os.listdir(os.path.join(MF.SANDBOX_FALSO, "snap")):
    if "_final" not in n:
        shutil.copyfile(os.path.join(MF.SANDBOX_FALSO, "snap", n), os.path.join(SN2, n))
mp = os.path.join(BF, "mcp_um.py"); mraw = open(mp, "rb").read()
MF.escreve(mp, mraw + b"# alterado no meio do pre-selo (ensaio)\n")
py(S("snap_producao_v413.py"), ["final", SN2])
MF.escreve(mp, mraw)
PROVA_DIR = os.path.join(OUTB, "prova_producao")
for p_ in (PINO, os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json"), PROVA_DIR):
    guardar(p_)
rc, o, e = py(S("gerar_pino_recibo_pre_selo_v413.py"), [SN2])
pn_ = lj(PINO) if os.path.exists(PINO) else {}
pv_ = lj(os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")) if os.path.exists(os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")) else {}
reg("NA gerar_pino com a producao alterada entre as fotos: rc 1, producao NAO intacta, nao utilizavel", rc == 1 and pn_.get("utilizavel_como_recibo_pre_selo_do_B_n") is False and pv_.get("producao_intacta") is False,
    [rc, pn_.get("motivos_de_nao_ser_utilizavel"), (o + e)[-300:]])
for p_ in (PINO, os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")):
    if os.path.exists(p_):
        os.remove(p_)
    voltar(p_)
if os.path.isdir(PROVA_DIR):
    shutil.rmtree(PROVA_DIR)
voltar(PROVA_DIR)
rc, o, e = py(S("limpar_sandbox_vb24.py"))
reg("A7 limpar_sandbox_vb24 (copia): apaga o sandbox curto LIDO do delta_bn (aqui C:\\t\\vb99), sem juncao, sem mexer nos irmaos", rc == 0 and not os.path.exists(MF.SANDBOX_FALSO), [rc, (o + e)[-300:]])
rc, o, e = py(S("diff_e_pinos_bn_v413.py"))
PBN = os.path.join(V413, "PINOS_BN_v413.json")
pbn = lj(PBN) if os.path.exists(PBN) else {}
esp_pend = {"delta", "candidato", "kernel_recibo", "esperados", "pins_do_candidato", "criterios", "DIFF_KERNEL_v413.txt", "DIFF_v412_v413.diff"}
reg("A8 diff_e_pinos_bn_v413 sem --delta (1.4, N6): o PINOS_BN traz a cadeia, o recibo pre-selo do salto, os anteriores v412 (um.py) e v411 (Bancada), o delta_bn e o util por sha; o que depende do candidato fica em pendentes",
    rc == 0 and set(pbn.get("pendentes") or []) == esp_pend and (pbn.get("recibo_pre_selo") or {}).get("sha256") == pj.get("sha256") and (pbn.get("cadeia_de_selos") or {}).get("sha256") == PC["cadeia"]["sha256"]
    and (pbn.get("selo_anterior_v412") or {}).get("sha256") and (pbn.get("bancada_anterior_v411") or {}).get("deployment_id") and (pbn.get("delta_bn") or {}).get("sha256") == shaf(S("delta_bn_v413.py")),
    [rc, pbn.get("pendentes"), (o + e)[-400:]])
if not (os.path.exists(PINO) and os.path.exists(PBN)):
    reg("PARADA DO ENSAIO: sem o pino do recibo pre-selo ou sem o PINOS_BN, os blocos seguintes nao tem insumo", False, [os.path.exists(PINO), os.path.exists(PBN)])
    json.dump({"testes": RES}, open(os.path.join(AQUI, "RESULTADO_PARCIAL_PARADO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    raise SystemExit(1)
raw_pino = open(PINO, "rb").read()
p2 = json.loads(raw_pino.decode("utf-8")); p2["utilizavel_como_recibo_pre_selo_do_B_n"] = False; wj(PINO, p2)
pbn_raw = open(PBN, "rb").read()
rc, o, e = py(S("diff_e_pinos_bn_v413.py"))
reg("NA diff_e_pinos com o pino do recibo pre-selo NAO utilizavel: PARA (rc 1) sem regravar o PINOS_BN", rc == 1 and open(PBN, "rb").read() == pbn_raw and "NAO serve" in (o + e), [rc, (o + e)[-300:]])
MF.escreve(PINO, raw_pino)
rc, o, e = py(S("p00_precondicoes_bn_v413.py"))
p00 = lj(os.path.join(V413, "PRECONDICOES_BN_v413.json")) if os.path.exists(os.path.join(V413, "PRECONDICOES_BN_v413.json")) else {}
reg("A9 p00_precondicoes_bn_v413: nenhuma FALHA e so' os pendentes do candidato (rc 3); a cadeia carregada pelo esboco, a bateria, o prazo, o recibo, a prova, o PINOS_BN, a autorizacao e a forma dos scripts conferidos",
    rc == 3 and p00.get("n_falhas") == 0 and p00.get("n_pendentes", 0) >= 1, [rc, p00.get("veredito"), [c_["checagem"][:90] for c_ in p00.get("checagens", []) if c_.get("ok") is False], (o + e)[-300:]])

# (revisao B2) a guarda de restos cobre o LIMPEZA_SANDBOX_<sb>.json: so' ele fica e o runner (copia com B reapontado; o passo 1 trocado por `exit 77`, para nada rodar se a guarda falhasse) recusa
SH = shutil.which("sh") or r"C:\Program Files\Git\usr\bin\sh.exe"
unix = lambda p_: "/" + p_[0].lower() + p_[2:].replace("\\", "/")


def sh_copia(nome, troca_extra=None):
    t_ = open(S(nome), encoding="utf-8").read()
    a_ = 'B="/c/IALD/Central de Patentes/work/cadeia_de_selo/v413/bancada"'
    assert t_.count(a_) == 1, nome
    t_ = t_.replace(a_, 'B="%s"' % unix(BN))
    if troca_extra:
        assert t_.count(troca_extra[0]) == 1, troca_extra[0]
        t_ = t_.replace(troca_extra[0], troca_extra[1])
    p_ = os.path.join(BN, "_hermetico_" + nome)
    MF.escreve(p_, t_)
    return p_


def sh_rodar(p_, env_extra):
    env = dict(os.environ)
    for k in ("B3_AUTORIZADO", "EVENTO", "EVENTO_HASH", "CHAIN_DE", "CHAIN_ATE"):
        env.pop(k, None)
    env.update(env_extra)
    r_ = subprocess.run([SH, p_], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=BN, stdin=subprocess.DEVNULL, timeout=600)
    return r_.returncode, (r_.stdout or "") + (r_.stderr or "")


RESTOS = [os.path.join(OUTB, "etapa1_stdout.txt"), os.path.join(OUTB, "ensaio_1"), os.path.join(OUTB, "conferencia_pelo_esboco_v413.json"), os.path.join(OUTB, "prova_producao"), PINO,
          os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")]
for p_ in RESTOS:
    guardar(p_)
rc, o = sh_rodar(sh_copia("rodar_bn_pre_selo_v413.sh", ('mkdir -p "$SB/snap"', "exit 77")), {})
reg("E7 rodar_bn_pre_selo (revisao B2): so' o LIMPEZA_SANDBOX_vb99.json de uma rodada anterior sobrou: o runner recusa na guarda de restos (rc 9), nada roda",
    rc == 9 and "LIMPEZA_SANDBOX_vb99.json ja existe" in o, [rc, o[-300:]])
for p_ in RESTOS:
    voltar(p_)
reg("E8 rodar_bn_pre_selo (revisao B1): o veredito final le o rc do p00 (0 ou 3 passam; 1 falha)",
    '{ [ "$RC_P00" != 0 ] && [ "$RC_P00" != 3 ]; }' in open(S("rodar_bn_pre_selo_v413.sh"), encoding="utf-8").read(), None)
# (revisao M3, ii) o esboco R3.6 REAL no pos-selo do salto, no mundo falso: a v413 falsa no Nos falso, a Bancada falsa AINDA no B20 (o ensaio do passo 10 vem antes do APLICAR)
for n_ in ("um.py", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_selo.json"):
    MF.escreve(os.path.join(NOSF, n_), open(os.path.join(R, "versoes", "v413", n_), "rb").read())
BP13 = os.path.join(V413, "bateria_pos_selo_hermetico")
PMIN13 = os.path.join(BP13, "PINO_MINIMO_v413.json"); wj(PMIN13, {"candidato": {"path": os.path.join(NOSF, "um.py"), "sha256": shaf(os.path.join(NOSF, "um.py"))}})
P11 = lj(os.path.join(M["CS"], "v411", "PINOS_BN_v411.json"))
rc, o, e = py(P11["gerador_bateria"]["path"], ["--base", P11["bateria_base_R2"]["path"], "--base-sha256", P11["bateria_base_R2"]["sha256"], "--versao", "v413", "--nos", NOSF, "--driver", P11["driver_t12_t14"]["path"],
                                               "--pinos-bn", PMIN13, "--pino-saida", os.path.join(BP13, "PINO_UM_PY_v413.json"), "--saida", os.path.join(BP13, "BATERIA_VINCULO_v413.json")], cwd=BP13)
BAT13 = os.path.join(BP13, "BATERIA_VINCULO_v413.json")
os.makedirs(MF.SANDBOX_FALSO, exist_ok=True)
rc, o, e = py(ESB, ["--bancada", BF, "--nos", NOSF, "--versao", "v413", "--fase", "pos_selo", "--modo", "ensaio", "--bateria", BAT13, "--bateria-sha256", shaf(BAT13), "--recibo-pre-selo", RP, "--recibo-pre-selo-sha256", shaf(RP),
                    "--cadeia-de-selos", PC["cadeia"]["path"], "--cadeia-de-selos-sha256", PC["cadeia"]["sha256"], "--selo-anterior", os.path.join(V413, "base_v412", "um_absoluto_selo.json"),
                    "--kernel-manifesto-anterior", os.path.join(V413, "base_v412", "tgl_kernel_proof_manifest.json"), "--saida", os.path.join(MF.SANDBOX_FALSO, "pos_ensaio"), "--sandbox", "--sem-bateria"], cwd=MF.SANDBOX_FALSO)
imp0 = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B0a (revisao M3 ii) o esboco R3.6 REAL em pos_selo ensaio do salto (--sandbox --sem-bateria), com o recibo pre-selo do A3b, a cadeia e o selo e o kernel da v412: REPINADA_B21__SALTO_v411_v413__ENSAIO__NADA_GRAVADO_NA_BANCADA",
    rc == 0 and imp0.get("veredito") == "REPINADA_B21__SALTO_v411_v413__ENSAIO__NADA_GRAVADO_NA_BANCADA", [rc, imp0.get("veredito"), imp0.get("recusa"), e[-300:]])
if imp0.get("recibo"):
    r0 = lj(imp0["recibo"])
    r0["bateria_resultado"] = {"n": 2, "passa": 2, "falha": 0, "nao_executado": 0, "veredito": "BATERIA_PASSA", "testes": [{"id": "T01_IDENTIDADE", "resultado": "PASSA"}, {"id": "T15_SONDAS", "resultado": "PASSA"}]}
    p0 = os.path.join(V413, "bancada_B3_ensaio_esboco_real", os.path.basename(imp0["recibo"])); wj(p0, r0)
    MF.escreve(os.path.join(V413, "bn_pos_selo", "b3_ensaio_esboco_real_out.txt"), json.dumps({"veredito": r0["veredito"], "recibo": p0, "recibo_sha256": shaf(p0)}) + "\n")
    rc, o, e = py(S("b3_recibo_v413.py"), [os.path.join(V413, "bn_pos_selo", "b3_ensaio_esboco_real_out.txt"), "ensaio", PC["cadeia"]["sha256"]])
    reg("B0b o b3_recibo_v413 confere o recibo do pos-selo FEITO PELO ESBOCO (o salto no pos-selo, o regenerar com salto, o formato; so' o bloco da bateria sintetico): rc 0", rc == 0, [rc, (o + e)[-400:]])
else:
    reg("B0b o b3_recibo_v413 sobre o recibo do pos-selo feito pelo esboco", False, "sem recibo do B0a")
shutil.rmtree(MF.SANDBOX_FALSO, ignore_errors=True)
shutil.rmtree(os.path.join(V413, "bancada_B3_ensaio_esboco_real"), ignore_errors=True)
os.remove(os.path.join(V413, "bn_pos_selo", "b3_ensaio_esboco_real_out.txt"))

# ======================================================================== B. o pos-selo no mundo falso (a v413 falsa instalada; a Bancada falsa em B21-v413)
SERV = os.path.join(V413, "bancada_B3_servico")
SEL = os.path.join(V413, "bn_pos_selo")
man_pre = lj(os.path.join(BF, "canonical_contracts.json"))
pre = lj(RP)
MF.instalar_v413_no_nos_falso(M)
MAN_SHA = shaf(os.path.join(BF, "canonical_contracts.json"))
um13, selo13 = shaf(os.path.join(NOSF, "um.py")), shaf(os.path.join(NOSF, "um_absoluto_selo.json"))


def recibo_pos(modo, evento=None):
    r_ = json.loads(json.dumps(pre))
    r_.update(versao_alvo="v413", fase="pos_selo", modo=modo, inicio_utc=(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=120)).isoformat(),
              fim_utc=(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=60)).isoformat())
    r_["veredito"] = "REPINADA_B21__SALTO_v411_v413__" + ("ENSAIO__NADA_GRAVADO_NA_BANCADA" if modo == "ensaio" else "APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO")
    r_["recibo_pre_selo"] = {"sha256": pj["sha256"], "salto": pre["salto"]}
    r_["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v413", "um_py_sha256": um13}
    r_["manifesto_novo"] = {"deployment_id": "B21-v413-20261121-R1", "sha256": MAN_SHA}
    r_["aplicacao"] = None if modo == "ensaio" else {"pos_conferencia": {"ok": True, "canonical_version": "v413", "canonical_manifest_sha256": MAN_SHA, "deployment_id": "B21-v413-20261121-R1"}}
    if evento:
        r_["evento_c1"] = evento
    return r_


def gravar_pos(r_, pasta, nome_out):
    p_ = os.path.join(pasta, "RECIBO_SINCRONIZACAO_v413_%s.json" % ("20261121_010101" if r_["modo"] == "aplicar" else "20261121_000000"))
    wj(p_, r_)
    MF.escreve(os.path.join(SEL, nome_out), "...\n" + json.dumps({"veredito": r_["veredito"], "recusa": None, "recibo": p_, "recibo_sha256": shaf(p_)}) + "\n")
    return p_


CAD = PC["cadeia"]["sha256"]
r_ens = recibo_pos("ensaio")
p_ens = gravar_pos(r_ens, os.path.join(V413, "bancada_B3_ensaio_20261121_000000"), "b3_ensaio_out.txt")
rc, o, e = py(S("b3_recibo_v413.py"), [os.path.join(SEL, "b3_ensaio_out.txt"), "ensaio", CAD])
reg("B1 b3_recibo_v413 ensaio (2.4): o salto exigido (cadeia == o pino, de v411/B20 ate v412, proxima v413), o veredito exato, o manifesto anterior == o do pre-selo, B21-v413: rc 0", rc == 0, [rc, (o + e)[-500:]])
for nome_neg, mut, args_ in (("sem o bloco salto", lambda r_: r_.__setitem__("salto", None), None), ("veredito sem __SALTO_", lambda r_: r_.__setitem__("veredito", "REPINADA_B21__ENSAIO__NADA_GRAVADO_NA_BANCADA"), None),
                             ("manifesto anterior mudado desde o pre-selo", lambda r_: r_["manifesto_anterior"].__setitem__("sha256", "0" * 64), None),
                             ("deployment B22", lambda r_: r_["manifesto_novo"].__setitem__("deployment_id", "B22-v413-20261121-R1"), None),
                             ("cadeia errada no 3o argumento", None, "1" * 64), ("sem o 3o argumento", None, "")):
    if mut:
        r2 = recibo_pos("ensaio"); mut(r2); gravar_pos(r2, os.path.join(V413, "bancada_B3_ensaio_neg"), "b3_neg_out.txt")
        rc, o, e = py(S("b3_recibo_v413.py"), [os.path.join(SEL, "b3_neg_out.txt"), "ensaio", CAD])
    else:
        rc, o, e = py(S("b3_recibo_v413.py"), [os.path.join(SEL, "b3_ensaio_out.txt"), "ensaio"] + ([args_] if args_ else []))
    reg("NB b3_recibo com %s: rc 1" % nome_neg, rc == 1, [rc, (o + e)[-200:]])
# (revisao B3) o conferidor de exigencias (copia) DEPOIS do passo 10: a pasta do ENSAIO (bancada_B3_ensaio_*) ja existe e a condicao do APLICAR nao pode falhar por ela
rc, o, e = py(S("conferir_exigencias_servico_v413.py"), env_extra={"V413_AUTORIZACAO_OPERADOR": MF.aut(M)})
CEX = os.path.join(V413, "bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v413.json")
cex = lj(CEX) if os.path.exists(CEX) else {"condicoes": []}
falhas_cex = [c_["nome"] for c_ in cex["condicoes"] if not c_["ok"]]
cond_aplicar = [c_ for c_ in cex["condicoes"] if c_["nome"].startswith("o recibo do APLICAR da v413 ainda nao existe")]
# as duas falhas que o mundo falso produz POR DESENHO, cada uma conferida pela causa: o sandbox reapontado (vb99, nao vb24) e a porta reapontada (o RECIBO_RELIGAMENTO_v411 copiado do real traz a porta 18777;
# o delta_bn falso aponta a porta de ensaio), com pid, no_ar_desde e hora_recibo presentes (so' a porta difere)
rr411 = lj(os.path.join(M["CS"], "v411", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json"))
por_desenho = {"delta_bn: as seqs da autorizacao": MF.SANDBOX_FALSO != os.path.join("C:" + os.sep, "t", "vb24"),
               "insumo da parada (N6)": rr411.get("porta") == 18777 != MF.PORTA_FALSA and str(rr411.get("pid", "")).isdigit() and bool(rr411.get("no_ar_desde")) and bool(rr411.get("hora_recibo"))}
reg("B1c (revisao B3) o conferidor de exigencias depois do passo 10 (com bancada_B3_ensaio_* no disco): a condicao do APLICAR passa; as unicas falhas sao as duas do mundo falso por desenho "
    "(o sandbox vb99 e a porta de ensaio contra o recibo da v411 copiado do real, que traz 18777), cada uma conferida pela causa",
    len(cond_aplicar) == 1 and cond_aplicar[0]["ok"] is True and len(falhas_cex) == 2 and all(any(f_.startswith(k_) for f_ in falhas_cex) and v_ for k_, v_ in por_desenho.items()),
    [rc, falhas_cex, por_desenho])
if os.path.exists(CEX):
    os.remove(CEX)
# o evento (2.6): o iald.py FALSO anota no quadro falso
ESPF = os.path.join(V413, "ESPERADOS_v413.json")
wj(ESPF, {"candidato_sha16": um13[:16]})
pb = lj(PBN); pb["esperados"] = {"path": ESPF, "sha256": shaf(ESPF), "bytes": os.path.getsize(ESPF)}; wj(PBN, pb)
rc, o, e = py(S("evento_c1_b3_v413.py"), env_extra={"FAKE_IALD_FALHA": "1"})
reg("NB evento_c1_b3 com o iald.py saindo rc 1: o evento PARA (assert do rc)", rc == 1 and "AssertionError" in e, [rc, e[-200:]])
os.replace(os.path.join(SEL, "b3_ensaio_out.txt"), os.path.join(SEL, "b3_ensaio_out.txt.guardado"))
rc, o, e = py(S("evento_c1_b3_v413.py"))
reg("NB evento_c1_b3 sem o stdout do ENSAIO: nada e' anotado (assert antes do subprocess)", rc == 1 and "ENSAIO" in e, [rc, e[-200:]])
os.replace(os.path.join(SEL, "b3_ensaio_out.txt.guardado"), os.path.join(SEL, "b3_ensaio_out.txt"))
n_antes = len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()])
rc, o, e = py(S("evento_c1_b3_v413.py"))
linha_ev = [l for l in o.splitlines() if l.startswith("EVENTO=")]
EV, EVH = (int(linha_ev[-1].split()[0].split("=")[1]), linha_ev[-1].split()[1].split("=")[1]) if linha_ev else (None, None)
reg("B3 evento_c1_b3_v413 (2.6): ENSAIO conferido antes, o candidato conferido, o rc e o retorno do iald.py lidos, o elo conferido no livro inteiro e posterior ao ensaio; imprime EVENTO=<seq> EVENTO_HASH=<hash16>",
    rc == 0 and EV is not None and len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()]) == n_antes + 1, [rc, linha_ev, (o + e)[-300:]])
UTILP = S("util_bn_v413.py")
rc, o, e = py(UTILP, ["evento_depois_do_ensaio", str(EV), EVH, p_ens])
reg("B3b util evento_depois_do_ensaio (o portao do 10b): o evento anotado confere e e' posterior ao fim do ensaio: rc 0", rc == 0, [rc, o[-200:]])
rc, o, e = py(UTILP, ["evento_depois_do_ensaio", str(EV), "f" * 16, p_ens])
reg("NB util evento_depois_do_ensaio com o hash errado: rc 1", rc == 1, [rc, o[-200:]])
n_antes = len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()])
rc, o, e = py(S("evento_c1_b3_v413.py"))
reg("B3c (revisao B6) o evento rodado de novo depois deste ensaio: nada e' anotado (o mesmo EVENTO= do livro), rc 0", rc == 0 and "nada foi anotado de novo" in o and ("EVENTO=%d EVENTO_HASH=%s" % (EV, EVH)) in o
    and len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()]) == n_antes, [rc, o[-300:]])
ev_full = [json.loads(l) for l in open(M["QUADRO"], encoding="utf-8") if l.strip()][-1]
r_ap = recibo_pos("aplicar", {"evento": EV, "verificado": True, "hash": ev_full["hash"]})
p_ap = gravar_pos(r_ap, os.path.join(V413, "bancada_B3"), "b3_aplicar_out.txt")
rc, o, e = py(S("b3_recibo_v413.py"), [os.path.join(SEL, "b3_aplicar_out.txt"), "aplicar", CAD])
reg("B2 b3_recibo_v413 aplicar: pos_conferencia ok, versao v413, o sha do manifesto novo; o salto e o veredito exato do APLICAR: rc 0", rc == 0, [rc, (o + e)[-400:]])
# a conferencia A falsa (porta 18799 fechada, nenhum processo da Bancada falsa) e a parada no modo ja_fora_do_ar
SAUDE_F = os.path.join(SEL, "saude")
glob_rel = os.path.join(M["CS"], "v*", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v*.json")
rc, o, e = py(S("saude_bancada.py"), ["--saida", SAUDE_F, "--bancada", BF, "--nos", NOSF, "--porta", str(MF.PORTA_FALSA), "--recibos-religamento", glob_rel])
sa = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B4a saude_bancada (conferencia A) sobre a Bancada falsa com a porta fechada: FORA_DO_AR_APOS_REINICIO (o boot real e' depois do religamento falso da v411), rc 3", rc == 3 and sa.get("veredito") == "FORA_DO_AR_APOS_REINICIO", [rc, sa, e[-200:]])
rc, o, e = py(S("montar_autorizacao_v413.py"))
au_ = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
aut_txt = open(au_["autorizacao"], encoding="utf-8").read().rstrip("\n") if au_.get("autorizacao") else ""
reg("B5a (revisao B5) montar_autorizacao_v413 (copia) monta o texto dos eventos 1687 e 1689 e da fala de 20/11 (hashes lidos por script) e grava AUTORIZACAO_v413.txt com o recibo; o texto e' o que os recibos aceitam",
    rc == 0 and aut_txt == MF.aut(M) and os.path.isfile(au_.get("autorizacao", "")[:-4] + ".json"), [rc, (o + e)[-300:]])
rc, o, e = py(S("montar_autorizacao_v413.py"))
reg("B5b montar_autorizacao de novo, com os mesmos arquivos: idempotente (nao regrava), rc 0", rc == 0 and "idempotente" in o, [rc, o[-200:]])
SA_ENV = {"V413_AUTORIZACAO_OPERADOR": aut_txt, "V413_PARADA": "ja_fora_do_ar", "V413_SAUDE_RECIBO": sa.get("recibo", ""), "V413_SAUDE_SHA256": sa.get("sha256", "")}
for nome_neg, mud, cond in (("o AUT sem a fala de 20/11", {"V413_AUTORIZACAO_OPERADOR": aut_txt.split(" Fala do operador de 20/11")[0]}, "AssertionError"),
                            ("V413_PID_PARADO no ja_fora_do_ar", {"V413_PID_PARADO": "1234"}, "AssertionError"),
                            ("o sha256 da conferencia A errado", {"V413_SAUDE_SHA256": "0" * 64}, "AssertionError"),
                            ("sem V413_PARADA", {"V413_PARADA": ""}, "AssertionError")):
    rc, o, e = py(S("recibo_parada_v413.py"), env_extra=dict(SA_ENV, **mud))
    reg("NB recibo_parada com %s: recusa (%s), nada gravado" % (nome_neg, cond), rc == 1 and cond in e and not os.path.exists(os.path.join(SERV, "RECIBO_PARADA_v413.json")), [rc, e[-200:]])
q_raw = open(M["QUADRO"], "rb").read()
ls_ = q_raw.decode("utf-8").splitlines(True)
MF.escreve(M["QUADRO"], "".join(ls_[:2] + ["isto nao e' json\n"] + ls_[2:]))
rc, o, e = py(S("recibo_parada_v413.py"), env_extra=SA_ENV)
reg("NB recibo_parada com uma linha ILEGIVEL no quadro (2.2, M11 dinamico): recusa EVENTOS_JSONL_ILEGIVEL, nada gravado", rc == 1 and "EVENTOS_JSONL_ILEGIVEL" in e and not os.path.exists(os.path.join(SERV, "RECIBO_PARADA_v413.json")), [rc, e[-200:]])
MF.escreve(M["QUADRO"], q_raw)
rc, o, e = py(S("recibo_parada_v413.py"), env_extra=SA_ENV)
rpj = lj(os.path.join(SERV, "RECIBO_PARADA_v413.json")) if os.path.exists(os.path.join(SERV, "RECIBO_PARADA_v413.json")) else {}
reg("B4 recibo_parada_v413 ja_fora_do_ar (2.2, N4, N6): o livro inteiro, 1687 e 1689 por hash, a fala de 20/11, a conferencia A pinada, a porta fechada e nenhum processo: o recibo nasce com as chaves da v411 + as da v413",
    rc == 0 and rpj.get("modo") == "ja_fora_do_ar" and rpj.get("porta_fechada") is True and (rpj.get("autorizacao_conferida") or {}).get("evento_decisao", {}).get("seq") == 1689, [rc, (o + e)[-300:]])
# o religamento (N9, modo da placa): AGUARDA sem a fala; com a fala, LANCA o servidor FALSO com os logs e confere a identidade
FALA_MODO = os.path.join(M["W"], "cunhagens_13out", "OPERADOR_21nov_teste_hermetico_modo_da_placa_verbatim.txt")
rc, o, e = py(S("montar_autorizacao_v413.py"), [os.path.basename(FALA_MODO), "cpu"])
au2_ = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
aut2_txt = open(au2_["autorizacao"], encoding="utf-8").read().rstrip("\n") if au2_.get("autorizacao") else ""
reg("B5c montar_autorizacao com a fala do modo da placa e o modo cpu: AUTORIZACAO_v413_RELIGAMENTO_cpu.txt, com a fala, o sha16 e 'modo da placa: cpu'", rc == 0 and aut2_txt == MF.aut(M, FALA_MODO, "cpu"), [rc, (o + e)[-300:]])
RL_ENV = {"V413_AUTORIZACAO_OPERADOR": aut2_txt}
rc, o, e = py(S("recibo_religamento_v413.py"), env_extra=RL_ENV)
reg("NB recibo_religamento sem a fala do modo da placa: AGUARDA (rc 20), nada lancado", rc == 20 and "AGUARDA_OPERADOR" in o and not porta_aberta(MF.PORTA_FALSA), [rc, o[-200:]])
RL_ENV.update({"V413_MODO_PLACA": "cpu", "V413_FALA_MODO_PLACA": os.path.basename(FALA_MODO)})
logs_antes = {n: (os.path.getsize(os.path.join(BF, "estado", n)) if os.path.exists(os.path.join(BF, "estado", n)) else 0) for n in ("servidor.log", "servidor_erros.log")}
rc, o, e = py(S("recibo_religamento_v413.py"), env_extra=RL_ENV, timeout=300)
rr = lj(os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json")) if os.path.exists(os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json")) else {}
if rr.get("pid"):
    PIDS.append(int(rr["pid"]))
servido = json.loads(__import__("urllib.request").request.urlopen("http://127.0.0.1:%d/api/contratos" % MF.PORTA_FALSA, timeout=5).read()) if porta_aberta(MF.PORTA_FALSA) else {}
reg("B5 recibo_religamento_v413 (2.3, N4, N6, N9; modo cpu): o APLICAR achado, o servidor LANCADO destacado com os logs em estado\\, CUDA_VISIBLE_DEVICES=-1 no processo, a identidade de /api/contratos conferida, o PID da porta == o lancado",
    rc == 0 and rr.get("versao_servida") == "v413" and rr.get("modo_da_placa") == "cpu" and servido.get("_cuda_visible_devices") == "-1" and (rr.get("processo") or {}).get("pid_lancado") == rr.get("pid")
    and os.path.getsize(os.path.join(BF, "estado", "servidor.log")) > logs_antes["servidor.log"] and isinstance((rr.get("ambiente_do_processo") or {}).get("variaveis_python_retiradas"), list)
    and isinstance((rr.get("processo") or {}).get("breakaway"), bool), [rc, servido.get("_cuda_visible_devices"), (rr.get("processo") or {}).get("breakaway"), (o + e)[-400:]])
rc, o, e = py(S("recibo_religamento_v413.py"), env_extra=RL_ENV)
reg("NB recibo_religamento com o recibo ja existente: recusa ANTES de lancar (nao sobe um segundo servico)", rc == 1 and "AssertionError" in e, [rc, e[-200:]])
# o fechar (2.1): primeiro sem a parada (rc 2, nada gravado), depois o completo, depois idempotente
PINO_CONJ = os.path.join(SEL, "PINO_RECIBOS_B21_v413.json")
os.replace(os.path.join(SERV, "RECIBO_PARADA_v413.json"), os.path.join(SERV, "RECIBO_PARADA_v413.json.guardado"))
rc, o, e = py(S("fechar_bn_v413.py"))
reg("NB fechar_bn sem o recibo da parada: rc 2 e NADA gravado", rc == 2 and not os.path.exists(PINO_CONJ), [rc, o[-300:]])
os.replace(os.path.join(SERV, "RECIBO_PARADA_v413.json.guardado"), os.path.join(SERV, "RECIBO_PARADA_v413.json"))
rc, o, e = py(S("fechar_bn_v413.py"))
bench = os.path.join(M["W"], "iald_v412_20261119", "bench")
reg("B6 fechar_bn_v413 (2.1): os tres recibos juntos (o APLICAR do salto, a parada, o religamento com o PID VIVO), o evento no livro, o pino conjunto, a reconferencia e as copias na pasta do evento 1687",
    rc == 0 and os.path.isfile(PINO_CONJ) and all(os.path.isfile(os.path.join(bench, os.path.basename(x_))) for x_ in (p_ap, os.path.join(SERV, "RECIBO_PARADA_v413.json"), os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json"), PINO_CONJ)),
    [rc, (o + e)[-400:]])
rc, o, e = py(S("fechar_bn_v413.py"))
reg("B6b fechar_bn de novo: idempotente (o pino conjunto ja existe igual; as copias iguais), rc 0", rc == 0 and "idempotente" in o, [rc, o[-200:]])
n_antes = len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()])
rc, o, e = py(S("aviso_f06_v413.py"))
ult_ = [json.loads(l) for l in open(M["QUADRO"], encoding="utf-8") if l.strip()][-1]
reg("B6c (revisao B4) aviso_f06_v413 (copia): anota o aviso F0.6 com o pino conjunto e as copias dos tres recibos na pasta do evento 1687 (conferidos por sha256); AVISO=<seq>",
    rc == 0 and "AVISO=" in o and len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()]) == n_antes + 1 and ult_.get("tipo") == "AVISO_RECIBOS_B21_ENTREGUES"
    and (ult_.get("dados") or {}).get("pino_conjunto", {}).get("sha256") == shaf(PINO_CONJ), [rc, (o + e)[-300:]])
rc, o, e = py(S("aviso_f06_v413.py"))
reg("B6d o aviso F0.6 de novo: nao anota duas vezes (devolve o elo do livro), rc 0", rc == 0 and "nada foi anotado de novo" in o and len([l for l in open(M["QUADRO"], encoding="utf-8") if l.strip()]) == n_antes + 1, [rc, o[-200:]])
rc, o, e = py(S("saude_bancada.py"), ["--saida", SAUDE_F, "--bancada", BF, "--nos", NOSF, "--porta", str(MF.PORTA_FALSA), "--recibos-religamento", glob_rel])
sa2 = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B7a saude_bancada com o servidor falso no ar e o contrato em dia: NO_AR_EM_DIA, rc 0", rc == 0 and sa2.get("veredito") == "NO_AR_EM_DIA", [rc, sa2, e[-200:]])
wj(os.path.join(BF, "identidade_falsa.json"), {"ok": False, "code": "CANONICAL_REVALIDATION_REQUIRED"})
rc, o, e = py(S("saude_bancada.py"), ["--saida", SAUDE_F, "--bancada", BF, "--nos", NOSF, "--porta", str(MF.PORTA_FALSA), "--recibos-religamento", glob_rel])
sa3 = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B7b saude_bancada com o servidor no ar recusando o contrato: NO_AR_CONTRATO_VELHO, rc 3", rc == 3 and sa3.get("veredito") == "NO_AR_CONTRATO_VELHO", [rc, sa3])
os.remove(os.path.join(BF, "identidade_falsa.json"))
for pid in list(PIDS):
    parar_pid(pid)
rc, o, e = py(S("fechar_bn_v413.py"))
reg("NB fechar_bn com o servico religado ja morto (o PID do recibo nao esta' vivo): portao C, rc 2", rc == 2 and "portao C" in o, [rc, o[-300:]])
# o religamento com a identidade errada: RECUSA gravada, o processo FICA (parado depois, pelo PID, por este ensaio)
os.replace(os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json"), os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json.primeiro"))
wj(os.path.join(BF, "identidade_falsa.json"), {"canonical_version": "v412"})
rc, o, e = py(S("recibo_religamento_v413.py"), env_extra=RL_ENV, timeout=300)
recusas = sorted(glob.glob(os.path.join(SERV, "RECUSA_RELIGAMENTO_v413_*.json")))
if recusas:
    PIDS.append(int(lj(recusas[-1])["pid_lancado"]))
reg("NB recibo_religamento com a versao servida errada: RELIGAMENTO_RECUSADO, recusa gravada com o PID, nenhum recibo de religamento", rc == 1 and recusas and not os.path.exists(os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json")), [rc, (o + e)[-300:]])
for pid in list(PIDS):
    parar_pid(pid)
os.remove(os.path.join(BF, "identidade_falsa.json"))
# INDETERMINADO: a porta aberta por outro programa
OUTRO = os.path.join(R, "outro", "outro_servidor.py")
MF.escreve(OUTRO, MF.SERVIDOR_FALSO.replace('os.path.join(R, "canonical_contracts.json")', repr(os.path.join(BF, "canonical_contracts.json"))))
po = subprocess.Popen([PY, "-I", "-B", OUTRO], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
PIDS.append(po.pid)
for _ in range(40):
    if porta_aberta(MF.PORTA_FALSA):
        break
    time.sleep(0.25)
rc, o, e = py(S("saude_bancada.py"), ["--saida", SAUDE_F, "--bancada", BF, "--nos", NOSF, "--porta", str(MF.PORTA_FALSA), "--recibos-religamento", glob_rel])
sa4 = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B7c saude_bancada com a porta aberta por OUTRO programa: INDETERMINADO, rc 1 (fail-closed)", rc == 1 and sa4.get("veredito") == "INDETERMINADO", [rc, sa4])
parar_pid(po.pid)
# FORA_DO_AR sem reinicio depois do ultimo religamento (um religamento falso de agora)
wj(os.path.join(M["CS"], "v499", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v499.json"), {"hora_recibo": datetime.datetime.now().astimezone().isoformat()})
rc, o, e = py(S("saude_bancada.py"), ["--saida", SAUDE_F, "--bancada", BF, "--nos", NOSF, "--porta", str(MF.PORTA_FALSA), "--recibos-religamento", glob_rel])
sa5 = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("B7d saude_bancada com a porta fechada e um religamento DEPOIS do boot: FORA_DO_AR, rc 3", rc == 3 and sa5.get("veredito") == "FORA_DO_AR", [rc, sa5])
rc, o, e = py(UTILP, ["saude_do_dia", SAUDE_F])
reg("B7e util saude_do_dia (o portao C do passo 10): ha' conferencia A de hoje na pasta: rc 0", rc == 0, [rc, o[-200:]])
rc, o, e = py(UTILP, ["saude_do_dia", os.path.join(R, "pasta_sem_saude")])
reg("NB util saude_do_dia numa pasta sem conferencia de hoje: rc 1 (o passo 10 AGUARDA)", rc == 1, [rc, o[-200:]])
SO_INDET = os.path.join(R, "saude_so_indeterminado")
os.makedirs(SO_INDET, exist_ok=True)
if sa4.get("recibo"):
    shutil.copyfile(sa4["recibo"], os.path.join(SO_INDET, os.path.basename(sa4["recibo"])))
rc, o, e = py(UTILP, ["saude_do_dia", SO_INDET])
reg("NB util saude_do_dia (revisao B10) com so' uma conferencia A INDETERMINADO de hoje: rc 1", rc == 1, [rc, o[-200:]])
OUTRA_B = os.path.join(R, "saude_de_outra_bancada")
sv_ = lj(sa2["recibo"]); sv_["bancada"] = os.path.join("C:" + os.sep, "outra", "Bancada"); wj(os.path.join(OUTRA_B, os.path.basename(sa2["recibo"])), sv_)
rc, o, e = py(UTILP, ["saude_do_dia", OUTRA_B])
reg("NB util saude_do_dia (revisao B10) com uma conferencia A de hoje de OUTRA Bancada: rc 1", rc == 1, [rc, o[-200:]])
rc, o, e = py(UTILP, ["pendentes_vazios", PBN])
reg("NB util pendentes_vazios no PINOS_BN do pre-selo (com pendentes): rc 1 (o 10b AGUARDA, 2.7)", rc == 1, [rc, o[-200:]])
pb2 = os.path.join(R, "PINOS_sem_pendentes.json"); wj(pb2, {"x": {"path": "a", "sha256": "b"}, "pendentes": []})
rc, o, e = py(UTILP, ["pendentes_vazios", pb2])
reg("util pendentes_vazios num PINOS_BN final (sem pendentes e sem pino sem sha): rc 0", rc == 0, [rc, o[-200:]])

# ======================================================================== E. os executores .sh (copias com B reapontado) no mundo falso pos-selo: os portoes, sem rodar o esboco
MF.escreve(os.path.join(NOSF, "rodada_v413_stdout.txt"), "... (rito falso)\nRITO_RC=0\n")
BNSH = sh_copia("bn_v413.sh")
os.replace(SAUDE_F, SAUDE_F + "_guardada")
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10", "CHAIN_ATE": "10"})
reg("E1 bn_v413.sh passo 10 sem conferencia A de hoje: portao C, AGUARDA (rc 20) antes de qualquer pino", rc == 20 and "portao C" in o, [rc, o[-300:]])
os.replace(SAUDE_F + "_guardada", SAUDE_F)
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10", "CHAIN_ATE": "10"})
reg("E2 bn_v413.sh passo 10 com a conferencia A de hoje e o PINOS_BN com pino pendente: AGUARDA (rc 20) no b3_prepara, nao traceback (2.4)", rc == 20 and "pendente" in o, [rc, o[-300:]])
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10a", "CHAIN_ATE": "10a"})
reg("E3 bn_v413.sh passo 10a com o recibo da parada e a porta fechada: rc 0", rc == 0 and "recibo da parada" in o, [rc, o[-300:]])
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10b", "CHAIN_ATE": "10b"})
reg("E4 bn_v413.sh passo 10b sem B3_AUTORIZADO: AGUARDA (rc 20)", rc == 20 and "nao esta autorizado" in o, [rc, o[-300:]])
RPF = os.path.join(SERV, "RECIBO_PARADA_v413.json")
rp_raw = open(RPF, "rb").read()
rp_mut = json.loads(rp_raw.decode("utf-8")); rp_mut["modo"] = "outro"; wj(RPF, rp_mut)
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10b", "CHAIN_ATE": "10b", "B3_AUTORIZADO": "sim", "EVENTO": "1", "EVENTO_HASH": "0123456789abcdef"})
reg("E4b bn_v413.sh passo 10b (revisao B11) com o recibo da parada sem modo valido: PARADA (rc 1) antes do APLICAR", rc == 1 and "B11" in o and "modo" in o, [rc, o[-300:]])
rp_mut = json.loads(rp_raw.decode("utf-8")); rp_mut["autorizacao_conferida"]["evento_decisao"]["seq"] = 1688; wj(RPF, rp_mut)
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "10b", "CHAIN_ATE": "10b", "B3_AUTORIZADO": "sim", "EVENTO": "1", "EVENTO_HASH": "0123456789abcdef"})
reg("E4c bn_v413.sh passo 10b (revisao B11) com o recibo da parada que nao conferiu a decisao 1689: PARADA (rc 1)", rc == 1 and "B11" in o and "1689" in o, [rc, o[-300:]])
MF.escreve(RPF, rp_raw)
os.replace(os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json.primeiro"), os.path.join(SERV, "RECIBO_RELIGAMENTO_v413.json"))
rc, o = sh_rodar(BNSH, {"CHAIN_DE": "11", "CHAIN_ATE": "11"})
reg("E5 bn_v413.sh passo 11 com o recibo do religamento cujo PID ja morreu: portao C, PARADA (rc 1)", rc == 1 and "portao C" in o, [rc, o[-300:]])
rc, o = sh_rodar(sh_copia("rodar_bn_pre_selo_v413.sh"), {})
reg("E6 rodar_bn_pre_selo_v413.sh com o Nos ja na v413: PRAZO_DO_PRE_SELO_PERDIDO (N1), rc 9, nada rodado", rc == 9 and "PRAZO_DO_PRE_SELO_PERDIDO" in o, [rc, o[-300:]])

# ======================================================================== C. o delta_bn (2.7, N5) e o util (2.2), lendo o real so' por leitura
DB_REAL = os.path.join(REAL_BN, "delta_bn_v413.py")
CT = os.path.join(R, "testes_delta.py")
MF.escreve(CT, r'''# -*- coding: utf-8 -*-
import importlib.util, json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, %r)
import delta_bn_v413 as D
d11 = D.delta_v411_fixado(); d12 = D.delta_v412_fixado()
print(json.dumps({"pina_hoje": D.BANCADA_PINA_HOJE, "fixada": D.BANCADA_PINA_HOJE_FIXADA_V411, "n": D.N_DO_SALTO, "sandbox": D.SANDBOX_CURTO, "d11_versao": d11.UM_VERSION, "d11_pina": d11.BANCADA_PINA_HOJE,
                  "d12_versao": d12.UM_VERSION, "d12_d11_e_o_fixado": d12.D11 is d11, "d12_pina": d12.BANCADA_PINA_HOJE, "veredito_pre": D.VEREDITO_PRE_SELO, "veredito_aplicar": D.VEREDITO_APLICAR}))
''' % REAL_BN)
rc, o, e = py(CT, cwd=R)
dj = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("C1 delta_bn_v413 REAL (so' leitura): a Bancada pina o B20 fixado; o delta_v411 carregado por fonte com o BANCADA_PINA_HOJE da v411 FIXADO; o delta_v412_r7 carregado por fonte com esse delta_v411; B21; vb24",
    rc == 0 and dj.get("pina_hoje") == dj.get("fixada") and dj.get("d11_versao") == "v411" and dj.get("d12_versao") == "v412" and dj.get("d12_d11_e_o_fixado") is True and dj.get("d11_pina") == dj.get("fixada") == dj.get("d12_pina")
    and dj.get("n") == 21 and dj.get("sandbox", "").lower().endswith("vb24") and dj.get("veredito_pre") == "REPINADA_B21__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA", [rc, dj, e[-400:]])
FAKE_MAN = os.path.join(R, "bancada_estados")


def delta_com_bancada(dep, versao):
    d_ = os.path.join(FAKE_MAN, dep)
    wj(os.path.join(d_, "canonical_contracts.json"), {"schema": 1, "deployment_id": dep, "canonical": {"version": versao}})
    t_ = open(DB_REAL, encoding="utf-8").read()
    ls__ = t_.splitlines(True)
    i_ = [i for i, l in enumerate(ls__) if l.startswith('_BANCADA_CONTRATOS = os.path.join(PRODUCAO, "canonical_contracts.json")')]
    assert len(i_) == 1
    ls__[i_[0]] = "_BANCADA_CONTRATOS = %r\n" % os.path.join(d_, "canonical_contracts.json")
    j_ = [i for i, l in enumerate(ls__) if l.startswith("HERE = os.path.dirname(os.path.abspath(__file__))")]
    ls__[j_[0]] = "HERE = %r\n" % REAL_BN
    MF.escreve(os.path.join(d_, "delta_bn_v413.py"), "".join(ls__))
    MF.escreve(os.path.join(d_, "t.py"), "import sys, json\nsys.dont_write_bytecode = True\nsys.path.insert(0, %r)\nimport delta_bn_v413 as D\nd11 = D.delta_v411_fixado()\nprint(json.dumps({'pina': D.BANCADA_PINA_HOJE, 'aplicada': D.BANCADA_JA_APLICADA, 'd11': d11.UM_VERSION}))\n" % d_)
    return py(os.path.join(d_, "t.py"), cwd=d_)


rc, o, e = delta_com_bancada("B21-v413-20261121-R1", "v413")
reg("C2 delta_bn com a Bancada (falsa) em B21-v413 (depois do APLICAR): importa, BANCADA_JA_APLICADA True, e o delta_v411 fixado ainda carrega (N5 consertado)", rc == 0 and '"aplicada": true' in o and '"d11": "v411"' in o, [rc, (o + e)[-300:]])
for dep, ver in (("B22-v413-20261121-R1", "v413"), ("B20-v411-20261113-R2", "v411"), ("B19-v410-20261111-R1", "v410"), ("B21-v412-20261121-R1", "v412")):
    rc, o, e = delta_com_bancada(dep, ver)
    reg("NC delta_bn com a Bancada (falsa) em %s: o import recusa (assert)" % dep, rc == 1 and "AssertionError" in e, [rc, e[-200:]])
N5T = os.path.join(R, "n5_sem_conserto.py")
MF.escreve(N5T, r'''# -*- coding: utf-8 -*-
import importlib.util, os, re, sys
sys.dont_write_bytecode = True
V411 = os.path.join(%r, "v411")
src = open(os.path.join(V411, "delta_v411.py"), "rb").read().decode("utf-8")
src = re.sub(r"^BANCADA_PINA_HOJE = _bancada_pina_hoje\(\)", lambda _m: "_BANCADA_CONTRATOS = %%r\nBANCADA_PINA_HOJE = _bancada_pina_hoje()" %% %r, src, count=1, flags=re.M)
m = importlib.util.module_from_spec(importlib.util.spec_from_loader("d11_vivo", loader=None)); m.__file__ = os.path.join(V411, "delta_v411.py")
exec(compile(src, m.__file__, "exec"), m.__dict__)
print("carregou")
''' % (MF.REAL_CS, os.path.join(FAKE_MAN, "B21-v413-20261121-R1", "canonical_contracts.json")))
rc, o, e = py(N5T, cwd=R)
reg("C3 N5 demonstrado: o delta_v411 VIVO (sem o conserto) quebra na importacao com a Bancada em B21-v413 (AssertionError do _bancada_pina_hoje dele)", rc == 1 and "AssertionError" in e and "nao pina nem a base" in e, [rc, e[-300:]])
UT = os.path.join(R, "testes_util.py")
MF.escreve(UT, r'''# -*- coding: utf-8 -*-
import hashlib, json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, %r)
import util_bn_v413 as U
D = %r
def cadeia(evs):
    ant, ls = "0" * 64, []
    for e in evs:
        e = dict(e, anterior=ant); e["hash"] = U.hash_evento(e); ant = e["hash"]; ls.append(json.dumps(e))
    return ls
evs = [{"seq": 1, "quem": "a", "dados": {}}, {"seq": 2, "quem": "b", "dados": {}}, {"seq": 3, "quem": "c", "dados": {}}]
res = {}
def caso(nome, linhas):
    p = os.path.join(D, nome + ".jsonl"); open(p, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    try:
        L = U.livro_conferido(p); res[nome] = "OK %%d" %% L["n_elos"]
    except ValueError as exc:
        res[nome] = str(exc).split(":")[0]
ok = cadeia(evs)
caso("valido", ok)
caso("ilegivel", ok[:1] + ["{nao e json"] + ok[1:])
caso("quebrado", ok[:1] + [ok[2]])
dup = cadeia(evs + [{"seq": 2, "quem": "d", "dados": {}}])
caso("seq_duplicada", dup)
L = U.livro_conferido(r"C:\IALD\PROGRAMA_IALD\eventos.jsonl")
res["quadro_real"] = "OK %%d" %% L["n_elos"]
print(json.dumps(res))
''' % (REAL_BN, R))
rc, o, e = py(UT, cwd=R)
uj = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("C4 util livro_conferido (2.2): cadeia valida OK; linha ilegivel, elo fora da cadeia e seq repetida RECUSADOS pelo codigo certo; o quadro REAL confere inteiro (so' leitura)",
    rc == 0 and uj.get("valido") == "OK 3" and uj.get("ilegivel") == "EVENTOS_JSONL_ILEGIVEL" and uj.get("quebrado") == "EVENTOS_CADEIA_QUEBRADA" and uj.get("seq_duplicada") == "EVENTO_SEQ_DUPLICADO" and str(uj.get("quadro_real", "")).startswith("OK "),
    [rc, uj, e[-300:]])
for args_, esp_rc, nome_ in ((["const", "SANDBOX_CURTO"], 0, "const SANDBOX_CURTO == C:\\t\\vb24"), (["porta_fechada"], 0, "porta_fechada (a porta real da Bancada esta' fechada)"),
                             (["nos_versao"], 0, "nos_versao (o Nos real na v412 com o selo pinando o um.py)"), (["subcomando_que_nao_existe"], 2, "subcomando desconhecido: rc 2")):
    rc, o, e = py(UTILP.replace(BN, REAL_BN), args_)
    extra = (o.strip().lower().endswith("vb24") if args_[0] == "const" else ("v412 SELO_PINA_O_UM_PY" in o if args_[0] == "nos_versao" else True))
    reg("C5 util (real, so' leitura) %s" % nome_, rc == esp_rc and extra, [rc, o.strip()[-120:]])

# ======================================================================== D. a conferencia A e a sentinela contra a Bancada REAL (porta fechada: o estado real), e o controle negativo do conferidor
OUT = os.path.join(AQUI, "saidas_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
rc, o, e = py(os.path.join(REAL_BN, "saude_bancada.py"), ["--saida", os.path.join(OUT, "saude_real")])
sr = json.loads([l for l in o.splitlines() if l.strip().startswith("{")][-1]) if "{" in o else {}
reg("D1 saude_bancada contra a Bancada REAL (so' leitura; porta fechada; nunca /api/estado): FORA_DO_AR_APOS_REINICIO (o boot de 16/11 depois do religamento de 13/11), rc 3", rc == 3 and sr.get("veredito") == "FORA_DO_AR_APOS_REINICIO", [rc, sr, e[-200:]])
rc, o, e = py(os.path.join(REAL_BN, "sentinela_boot_bancada.py"), ["--saida", os.path.join(OUT, "sentinela_real")])
avisos = glob.glob(os.path.join(OUT, "sentinela_real", "avisos", "AVISO_BANCADA_FORA_APOS_REINICIO_*.json"))
reg("D2 sentinela_boot_bancada (B preparada; nenhuma tarefa criada) contra a Bancada REAL: o aviso de fora do ar depois do reinicio e' gravado em arquivo", rc == 0 and len(avisos) == 1, [rc, o[-300:]])
rc, o, e = py(os.path.join(REAL_BN, "sentinela_boot_bancada.py"), ["--saida", os.path.join(OUT, "sentinela_real")])
reg("D3 sentinela de novo no mesmo boot: nao repete o aviso", rc == 0 and len(glob.glob(os.path.join(OUT, "sentinela_real", "avisos", "AVISO_BANCADA_FORA_APOS_REINICIO_*.json"))) == 1 and "ja ha' aviso" in o, [rc, o[-200:]])
# o AUT do controle negativo: montado dos arquivos REAIS (o livro real, os recibos e as falas reais)
ev = {}
for linha in open(MF.REAL_QUADRO, encoding="utf-8"):
    if linha.strip():
        x_ = json.loads(linha)
        if x_.get("seq") in (1687, 1689):
            ev[x_["seq"]] = x_
rec87 = ev[1687]["dados"]["recibo"]; fala89 = ev[1689]["dados"]["fala"]
f20 = os.path.join(MF.REAL_WK, "cunhagens_13out", "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt")
AUT_REAL = ("Autorizacao do operador ao ciclo da Bancada (evento 1687, hash16 %s; recibo da resposta sha16 %s): «%s». Decisao do operador (evento 1689, hash16 %s; fala sha16 %s): «%s». Fala do operador de 20/11 (sha16 %s): «%s»."
            % (ev[1687]["hash"][:16], shaf(rec87)[:16], json.loads(open(rec87, "rb").read().decode("utf-8"))["bench"]["answer"].strip(), ev[1689]["hash"][:16], shaf(fala89)[:16],
               ev[1689]["dados"]["decisao_do_operador"], shaf(f20)[:16], open(f20, "rb").read().decode("utf-8").strip()))
MF.escreve(os.path.join(OUT, "AUT_DO_CONTROLE_NEGATIVO.txt"), AUT_REAL + "\n")
os.makedirs(os.path.join(R, "tmp_mutador"))
rc, o, e = py(os.path.join(REAL_BN, "controle_negativo", "mutar_conferidor_v413.py"), env_extra={"V413_AUTORIZACAO_OPERADOR": AUT_REAL, "V413_MUTAR_TEMP": os.path.join(R, "tmp_mutador"),
                                                                                                 "V413_MUTAR_SAIDA": os.path.join(OUT, "controle_negativo")}, timeout=1800)
cn = lj(os.path.join(OUT, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v413.json")) if os.path.exists(os.path.join(OUT, "controle_negativo", "RESULTADO_CONTROLE_NEGATIVO_v413.json")) else {}
reg("D4 controle negativo do conferidor (2.8; scripts REAIS so' lidos, copias em pasta temporaria): o controle sem mutacao passa e as 13 mutacoes M1-M11 (M10 em tres) sao pegas pela condicao certa",
    rc == 0 and cn.get("toda_mutacao_foi_pega") is True and len(cn.get("mutacoes") or []) == 13, [rc, cn.get("controle_sem_mutacao"), {k: v.get("pegou") for k, v in (cn.get("resultados") or {}).items()}, (o + e)[-600:]])
existia_vb24 = os.path.exists(os.path.join("C:" + os.sep, "t", "vb24"))
rc, o, e = py(os.path.join(REAL_BN, "controle_negativo", "mutar_conferidor_v413.py"), env_extra={"V413_AUTORIZACAO_OPERADOR": AUT_REAL, "V413_MUTAR_TEMP": os.path.join("C:" + os.sep, "t", "vb24"),
                                                                                                 "V413_MUTAR_SAIDA": os.path.join(OUT, "controle_negativo_vb24")})
reg("D4b (revisao M1) o controle negativo apontado para C:\\t\\vb24 RECUSA antes de criar qualquer coisa (vb24 e' exclusivo do pre-selo real)",
    rc == 1 and "M1" in e and os.path.exists(os.path.join("C:" + os.sep, "t", "vb24")) == existia_vb24 and not os.path.exists(os.path.join(OUT, "controle_negativo_vb24")), [rc, e[-200:]])
# (revisao B5) o montar_autorizacao REAL contra o quadro e as falas REAIS (so' leitura): uma copia com o delta_bn de SERVICO_DIR temporario; o texto tem de ser o do AUT_REAL acima
TMP_AUT = os.path.join(R, "tmp_autorizacao_real")
os.makedirs(TMP_AUT)
for n_ in ("montar_autorizacao_v413.py", "util_bn_v413.py"):
    shutil.copyfile(os.path.join(REAL_BN, n_), os.path.join(TMP_AUT, n_))
tdb = open(os.path.join(REAL_BN, "delta_bn_v413.py"), encoding="utf-8").read().splitlines(True)
for i_, l_ in enumerate(tdb):
    if l_.startswith("HERE = os.path.dirname(os.path.abspath(__file__))"):
        tdb[i_] = "HERE = %r\n" % REAL_BN
    elif l_.startswith('SERVICO_DIR = os.path.join(V413, "bancada_B3_servico")'):
        tdb[i_] = "SERVICO_DIR = %r\n" % TMP_AUT
MF.escreve(os.path.join(TMP_AUT, "delta_bn_v413.py"), "".join(tdb))
rc, o, e = py(os.path.join(TMP_AUT, "montar_autorizacao_v413.py"), cwd=TMP_AUT)
aut_real_montado = open(os.path.join(TMP_AUT, "AUTORIZACAO_v413.txt"), encoding="utf-8").read().rstrip("\n") if os.path.exists(os.path.join(TMP_AUT, "AUTORIZACAO_v413.txt")) else ""
reg("D5 (revisao B5) montar_autorizacao sobre o quadro e as falas REAIS (copia; grava so' numa pasta temporaria): o texto e' o que o conferidor aceitou no D4 (%d caracteres)" % len(aut_real_montado),
    rc == 0 and aut_real_montado == AUT_REAL, [rc, (o + e)[-300:]])

# ======================================================================== F. o ensaio a seco do pos-selo (revisao M3), auto-teste com entradas FALSAS e --sem-bateria (o real e' depois do selo, com a bateria)
R2 = R + "_seco_entradas"
M2 = MF.montar(R2)
S2 = lambda n_: os.path.join(M2["BN"], n_)
rc1, o1, e1 = py(S2("gerar_e_pinar_cadeia_v413.py"))
rc2, o2, e2 = py(S2("gerar_bateria_v412_pre_selo_v413.py"))
reg("F0 as entradas falsas do ensaio a seco (um segundo mundo falso, com a cadeia e a bateria da v412 geradas pelos geradores reais)", rc1 == 0 and rc2 == 0, [rc1, rc2, (o1 + e1)[-200:], (o2 + e2)[-200:]])
C2 = M2["CS"]
args_seco = ["--mundo", R + "_seco_mundo", "--sem-bateria", "--nos-v413", os.path.join(R2, "versoes", "v413"), "--base-v412", os.path.join(C2, "v413", "base_v412"), "--base-v411", os.path.join(C2, "v412", "base_v411"),
             "--bancada-origem", M2["B"], "--cadeia-pino", os.path.join(C2, "v413", "cadeia_de_selos_v411_v412", "PINO_CADEIA_DE_SELOS_v411_v412.json"),
             "--bateria-v412-pinos", os.path.join(C2, "v413", "bateria_v412_pre_selo", "PINOS_BATERIA_v412.json"), "--pinos-bn", os.path.join(R2, "nao_ha_pinos_bn.json"),
             "--pinos-bn-v411", os.path.join(C2, "v411", "PINOS_BN_v411.json"), "--religamento-v411", os.path.join(C2, "v411", "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json"),
             "--parada-v411", os.path.join(C2, "v411", "bancada_B3_servico", "RECIBO_PARADA_v411.json"), "--quadro", M2["QUADRO"], "--cunhagens", os.path.join(M2["W"], "cunhagens_13out"),
             "--saida-esboco", os.path.join("C:" + os.sep, "t", "vb98"), "--porta", "18798"]
antes_seco = set(glob.glob(os.path.join(REAL_BN, "ensaio_a_seco", "RESULTADO_ENSAIO_A_SECO_POS_SELO_v413_*.json")))
rc, o, e = py(os.path.join(REAL_BN, "ensaio_a_seco_pos_selo_v413.py"), args_seco, cwd=R, timeout=1800)
novos_seco = sorted(set(glob.glob(os.path.join(REAL_BN, "ensaio_a_seco", "RESULTADO_ENSAIO_A_SECO_POS_SELO_v413_*.json"))) - antes_seco)
rs = lj(novos_seco[-1]) if novos_seco else {}
reg("F1 ensaio_a_seco_pos_selo_v413 (auto-teste, --sem-bateria): o mundo, o pre-selo do salto e o passo 10 pelo esboco REAL em --sandbox, o b3_recibo, a conferencia A, o montar_autorizacao, a parada e o evento, todos OK; "
    "o APLICAR, o religamento e o fechar nao rodam sem bateria (ditos NAO_EXECUTADO); o mundo e o sandbox apagados; nenhum processo vivo",
    rc == 0 and rs.get("n_falhas") == 0 and rs.get("n_ok") == 10 and rs.get("n_nao_executadas") == 3 and rs.get("mundo_apagado") is True and rs.get("sandbox_do_esboco_apagado") is True and not rs.get("processos_vivos_no_fim"),
    [rc, novos_seco[-1:] , [(x_["etapa"][:40], x_["ok"]) for x_ in rs.get("etapas", [])], (o + e)[-400:]])
shutil.rmtree(R2, ignore_errors=True)

for pid in list(PIDS):
    parar_pid(pid)
vivos = [p for p in PIDS if subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process -Id %d -ErrorAction SilentlyContinue | Measure-Object).Count" % p], capture_output=True, text=True).stdout.strip().endswith("1")]
reg("limpeza: nenhum processo criado por este ensaio ficou vivo (parados pelo PID); a porta de ensaio fechada; o sandbox de ensaio apagado", not vivos and not porta_aberta(MF.PORTA_FALSA) and not os.path.exists(MF.SANDBOX_FALSO), [vivos, PIDS])
res = {"contrato": "RESULTADO_ENSAIO_HERMETICO_BN_v413", "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "script": {"path": os.path.abspath(__file__), "sha256": shaf(os.path.abspath(__file__))},
       "mundo_falso": {"path": os.path.join(AQUI, "mundo_falso_bn_v413.py"), "sha256": shaf(os.path.join(AQUI, "mundo_falso_bn_v413.py")), "pasta_de_ensaio": R},
       "n_testes": len(RES), "n_passaram": sum(1 for x in RES if x["ok"]), "n_negativos": sum(1 for x in RES if x["teste"].startswith(("NA ", "NB ", "NC "))), "testes": RES, "saidas_reais_lidas": OUT,
       "escopo": "copias e dados de mentira; nenhum servico real ligado ou parado; nada gravado na Bancada, no Nos, na v412, nos sandboxes do kernel nem no quadro real; NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
dest = os.path.join(AQUI, "RESULTADO_ENSAIO_HERMETICO_BN_v413.json")
if os.path.exists(dest):
    dest = dest[:-5] + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
MF.escreve(dest, MF.jdump(res))
print("%d/%d testes passaram (%d negativos) -> %s" % (res["n_passaram"], res["n_testes"], res["n_negativos"], dest))
sys.exit(0 if res["n_passaram"] == res["n_testes"] else 1)

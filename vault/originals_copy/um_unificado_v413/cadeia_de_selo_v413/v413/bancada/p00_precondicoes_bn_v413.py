# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/p00_precondicoes_v412.py (o corpo chk/pend/tenta, rc 0/3/1), reescrito para o B(n) do SALTO: so' as pre-condicoes do elo
# da Bancada (a cadeia de selos, a bateria da v412, o prazo N1, o recibo pre-selo do salto, a prova da producao intacta, o PINOS_BN, os dois anteriores N6, os backups de 18/11 N3, o sandbox curto N8, a autorizacao N4,
# a forma estatica dos scripts do B(n)). As pre-condicoes do candidato, do rito e do kernel sao da cadeia principal da v413 (outros agentes); aqui so' se leem os pinos que o B(n) usa.
"""p00_precondicoes_bn_v413.py -- confere, SO LENDO, as pre-condicoes do B(n) da v413 (o salto v411 -> v413). Nada e' escrito fora de PRECONDICOES_BN_v413.json (backup de bytes do anterior). Pinos LIDOS dos arquivos.
Fail-closed: rc 1 se algo FALHA; rc 3 se nenhuma falha mas ha' PENDENTES (o que so' existe depois de outro passo, ou e' ato da gerencia); rc 0 so' com TODAS PASSARAM. Checagem que levanta excecao vira FALHA visivel.
uso: python -I -B -X utf8 p00_precondicoes_bn_v413.py"""
import sys

sys.dont_write_bytecode = True
import datetime
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

sha = U.sha256_arquivo
res = []
ok_all = True
PEND = []


def chk(nome, cond, det=None):
    global ok_all
    ok_ = bool(cond)
    ok_all = ok_all and ok_
    res.append({"checagem": nome, "ok": ok_, "detalhe": det})
    print(("OK   " if ok_ else "FALHA"), nome, ("" if ok_ else "| %s" % (str(det)[:300])))


def pend(nome, motivo):
    PEND.append({"checagem": nome, "motivo": motivo})
    res.append({"checagem": nome, "ok": None, "pendente": motivo})
    print("PEND ", nome, "|", motivo[:220])


def tenta(nome, fn):
    try:
        r_ = fn()
        chk(nome, r_[0] if isinstance(r_, tuple) else r_, r_[1] if isinstance(r_, tuple) else None)
    except Exception as e_:   # noqa: BLE001
        chk(nome, False, "excecao: %r" % (e_,))


P11 = U.ler_json(DBN.PINOS_BN_V411_ARQ)
ESB = P11["esboco_R3_6"]
tenta("o esboco R3.6 pinado em PINOS_BN_v411.json existe e tem o sha256 do pino", lambda: (sha(ESB["path"]) == ESB["sha256"], ESB["sha256"][:16]))
_spec = importlib.util.spec_from_file_location("sincronizar_bancada_r36_p00_bn_v413", ESB["path"])
MOD = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = MOD
_spec.loader.exec_module(MOD)

# (1) o estado de agora (so' leitura): a Bancada e o Nos
BP = DBN.BANCADA_PINA_HOJE
tenta("a Bancada de producao pina o B20 da v411 (antes do APLICAR) ou o B21 da v413 (depois): o delta_bn o confere ao ser importado (N5)", lambda: (BP["version"] in (DBN.BANCADA_ANTERIOR, DBN.UM_VERSION_BN), BP))
SELO_NOS = U.ler_json(os.path.join(DBN.NOS, "um_absoluto_selo.json"))
UM_NOS = sha(os.path.join(DBN.NOS, "um.py"))
NOS_V = SELO_NOS.get("um_version") if (SELO_NOS.get("sha256") or {}).get("um.py") == UM_NOS else None
tenta("o Nos tem um selo que pina o um.py do disco (v412 antes da instalacao da v413; v413 depois)", lambda: (NOS_V in (DBN.VERSAO_DO_PRE_SELO, DBN.UM_VERSION_BN), {"um_version": SELO_NOS.get("um_version"), "um_py_sha16": UM_NOS[:16]}))

# (2) as bases: o anterior da Bancada (v411, inicio da cadeia) e o anterior do um.py (v412, fim da cadeia) -- N6
def _base(d_, versao_):
    selo_ = U.ler_json(os.path.join(d_, "um_absoluto_selo.json"))
    um_, km_ = sha(os.path.join(d_, "um.py")), sha(os.path.join(d_, "tgl_kernel_proof_manifest.json"))
    return (selo_.get("um_version") == versao_ and (selo_.get("sha256") or {}).get("um.py") == um_ and (selo_.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") == km_), {"um_py": um_[:16], "kernel": km_[:16]}


tenta("N6: v412\\base_v411 e' a v411 selada (o selo diz v411 e pina o um.py e o kernel da copia): o anterior da BANCADA", lambda: _base(DBN.BASE_BANCADA_ANTERIOR, DBN.BANCADA_ANTERIOR))
tenta("N6: v413\\base_v412 e' a v412 selada (o selo diz v412 e pina o um.py e o kernel da copia): o anterior do UM.PY", lambda: _base(DBN.BASE_UM_PY_ANTERIOR, DBN.UM_PY_ANTERIOR))
if NOS_V == DBN.VERSAO_DO_PRE_SELO:
    tenta("antes da instalacao da v413: v413\\base_v412 == o Nos (um.py, selo, kernel), byte a byte por sha256",
          lambda: (all(sha(os.path.join(DBN.BASE_UM_PY_ANTERIOR, n_)) == sha(os.path.join(DBN.NOS, n_)) for n_ in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")), None))
if BP["version"] == DBN.BANCADA_ANTERIOR:
    def _bancada_pina_a_base():
        m_ = U.ler_json(DBN._BANCADA_CONTRATOS)
        c_ = m_.get("canonical") or {}
        return ((c_.get("script") or {}).get("sha256") == sha(os.path.join(DBN.BASE_BANCADA_ANTERIOR, "um.py")) and (c_.get("seal") or {}).get("sha256") == sha(os.path.join(DBN.BASE_BANCADA_ANTERIOR, "um_absoluto_selo.json"))
                and str((m_.get("sincronizacao") or {}).get("kernel_manifesto_sha256")) == sha(os.path.join(DBN.BASE_BANCADA_ANTERIOR, "tgl_kernel_proof_manifest.json"))), m_.get("deployment_id")
    tenta("a Bancada (B20) pina o um.py, o selo e o kernel de v412\\base_v411", _bancada_pina_a_base)

# (2b) revisao M4: a custodia dos insumos do salto -- as pastas e os arquivos que a cadeia pina e que o pos-selo le existem (perder qualquer um mata o salto ou deixa o passo 10 em AGUARDA)
def _custodia():
    falta_ = []
    for d_, ns_ in ((DBN.BASE_UM_PY_ANTERIOR, ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")), (DBN.BASE_BANCADA_ANTERIOR, ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")),
                    (DBN.CADEIA_DIR, (os.path.basename(DBN.CADEIA_ARQ), os.path.basename(DBN.PINO_CADEIA_ARQ))), (DBN.BATERIA_V412_DIR, ("BATERIA_VINCULO_v412.json", "PINOS_BATERIA_v412.json", "PINO_UM_PY_v412.json"))):
        if not os.path.isdir(d_):
            falta_.append(d_)
            continue
        falta_ += [os.path.join(d_, n_) for n_ in ns_ if not os.path.isfile(os.path.join(d_, n_))]
    if os.path.exists(DBN.PINO_RECIBO_PRE_SELO_ARQ):
        pr_ = U.ler_json(DBN.PINO_RECIBO_PRE_SELO_ARQ)
        falta_ += [p_ for p_ in (pr_.get("path"), os.path.join(DBN.OUTB_PRE_SELO, "ensaio_1")) if not (p_ and os.path.exists(p_))]
    return not falta_, {"faltam": falta_}


tenta("M4: existem v413\\base_v412 e v412\\base_v411 (os tres arquivos de cada), a pasta da cadeia de selos (a cadeia e o pino), a bateria da v412 (bateria, pino ao lado, pino do um.py) e, quando ha' pino, o recibo pre-selo e o ensaio_1", _custodia)

# (3) a cadeia de selos v411 -> v412: o arquivo == o pino; carregada pelo esboco (copias, registro do instalador, backups de 18/11 no Nos: N3); o inicio e' a Bancada (enquanto ela pina a v411), o fim e' a base_v412
CAD = None
if not os.path.exists(DBN.PINO_CADEIA_ARQ):
    pend("a cadeia de selos v411 -> v412 pinada (PINO_CADEIA_DE_SELOS_v411_v412.json)", "gerar_e_pinar_cadeia_v413.py (so' com o Nos na v412)")
else:
    PC = U.ler_json(DBN.PINO_CADEIA_ARQ)

    def _cadeia():
        global CAD
        CAD = MOD.carregar_cadeia_de_selos(Path(PC["cadeia"]["path"]), PC["cadeia"]["sha256"])
        return CAD["versoes"] == [DBN.BANCADA_ANTERIOR, DBN.UM_PY_ANTERIOR], {"sha16": PC["cadeia"]["sha256"][:16], "versoes": CAD["versoes"]}
    tenta("a cadeia de selos: arquivo == pino; CARREGADA PELO ESBOCO R3.6 (copias de bytes, selos, registro do instalador e backups do Nos de 18/11, N3); v411 -> v412", _cadeia)
    if CAD is not None:
        tenta("o fim da cadeia e' a v412 de v413\\base_v412 (um.py, selo, kernel)",
              lambda: ((CAD["elos"][-1]["um_py"]["sha256"], CAD["elos"][-1]["selo"]["sha256"], CAD["elos"][-1]["kernel_manifesto"]["sha256"])
                       == tuple(sha(os.path.join(DBN.BASE_UM_PY_ANTERIOR, n_)) for n_ in ("um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")), None))
        if BP["version"] == DBN.BANCADA_ANTERIOR:
            def _inicio():
                m_raw = open(DBN._BANCADA_CONTRATOS, "rb").read(); m_ = json.loads(m_raw)
                ant_ = {"version": (m_.get("canonical") or {}).get("version"), "um_py_pinado": ((m_.get("canonical") or {}).get("script") or {}).get("sha256"),
                        "seal_sha_pinado": ((m_.get("canonical") or {}).get("seal") or {}).get("sha256"), "_man": m_}
                MOD.conferir_cadeia_com_a_bancada(CAD, ant_)
                return True, m_.get("deployment_id")
            tenta("o inicio da cadeia e' o que a Bancada pina agora (conferir_cadeia_com_a_bancada do esboco)", _inicio)
        else:
            pend("o inicio da cadeia contra a Bancada", "a Bancada ja pina a v413 (APLICAR feito): o inicio foi conferido pelo esboco no pre-selo e no APLICAR")
    tenta("N3: os backups de 18/11 que a cadeia usa existem no Nos (so' leitura; nunca mover) e tem os sha da cadeia",
          lambda: (all(os.path.exists(x_["path"]) and sha(x_["path"]) == x_["sha256"] for e_ in U.ler_json(PC["cadeia"]["path"])["elos"][:-1]
                       for x_ in (e_["substituido_na_instalacao_por"]["backup_um_py"], e_["substituido_na_instalacao_por"]["backup_selo"], e_["substituido_na_instalacao_por"]["registro"])), None))

# (4) a bateria da v412 (N2): o arquivo == o pino ao lado; os pinos da versao sao os da v412 (conferir_pinos_da_versao do esboco contra a base_v412)
PBAT_P = os.path.join(DBN.BATERIA_V412_DIR, "PINOS_BATERIA_v412.json")
if not os.path.exists(PBAT_P):
    pend("a bateria da v412 do pre-selo (PINOS_BATERIA_v412.json)", "gerar_bateria_v412_pre_selo_v413.py (so' com o Nos na v412)")
else:
    def _bateria():
        pb_ = U.ler_json(PBAT_P)
        b_, _r, _s = MOD.carregar_bateria(Path(pb_["bateria"]["path"]), pb_["bateria"]["sha256"], "ensaio", "pre_selo", False)
        um_p = os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um.py")
        info_ = {"um_py": {"sha256": sha(um_p), "bytes": os.path.getsize(um_p)}, "selo": {"sha256": sha(os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um_absoluto_selo.json"))}}
        pv_ = MOD.conferir_pinos_da_versao(b_, info_, DBN.VERSAO_DO_PRE_SELO)
        return pv_["versao"] == DBN.VERSAO_DO_PRE_SELO and pv_["conferidos_contra_o_nos_lido"] is True, {"sha16": pb_["bateria"]["sha256"][:16], "testes": len(b_["testes"])}
    tenta("a bateria da v412: arquivo == pino ao lado; carregada pelo esboco (sha de cada teste); pinos_da_versao == a v412 da base", _bateria)
    tenta("a pasta da bateria da v412 NAO e' ancestral da --saida do ensaio (SAIDA_NA_PASTA_DE_FONTES)",
          lambda: (not (os.path.normcase(os.path.abspath(DBN.OUTB_PRE_SELO)) + os.sep).startswith(os.path.normcase(os.path.abspath(DBN.BATERIA_V412_DIR)) + os.sep), None))

# (5) o prazo (N1) e o recibo pre-selo do salto
APL413 = sorted(glob.glob(os.path.join(DBN.V413, "APLICADO_AO_CANONICO_*.json")))
if not os.path.exists(DBN.PINO_RECIBO_PRE_SELO_ARQ):
    if NOS_V == DBN.VERSAO_DO_PRE_SELO:
        pend("o recibo pre-selo do salto (PINO_RECIBO_PRE_SELO_v413.json)", "rodar_bn_pre_selo_v413.sh, AINDA dentro do prazo: o Nos esta' na v412 (N1)")
    else:
        chk("N1: o prazo do pre-selo do salto", False, "o Nos ja nao esta' na v412 e nao ha' recibo pre-selo do salto: a janela se perdeu (so' a v414 poderia saltar)")
else:
    PR = U.ler_json(DBN.PINO_RECIBO_PRE_SELO_ARQ)
    tenta("o recibo pre-selo do salto: arquivo == pino; utilizavel; veredito EXATO (%s); versao_nos v412; a Bancada que ele viu e' o B20; a cadeia dele == a pinada" % DBN.VEREDITO_PRE_SELO,
          lambda: (sha(PR["path"]) == PR["sha256"] and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PR.get("veredito") == DBN.VEREDITO_PRE_SELO and PR.get("versao_nos") == DBN.VERSAO_DO_PRE_SELO
                   and (PR.get("bancada_pina") or {}).get("deployment_id") == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"]
                   and (PR.get("cadeia_de_selos") or {}).get("sha256") == (U.ler_json(DBN.PINO_CADEIA_ARQ)["cadeia"]["sha256"] if os.path.exists(DBN.PINO_CADEIA_ARQ) else None),
                   {"veredito": PR.get("veredito"), "utilizavel": PR.get("utilizavel_como_recibo_pre_selo_do_B_n")}))

    def _antes_da_instalacao():
        r_ = json.loads(open(PR["path"], "rb").read().decode("utf-8"))
        ini_ = U.instante(r_["inicio_utc"])
        if not APL413:
            return r_["nos"]["selo"]["um_version"] == DBN.VERSAO_DO_PRE_SELO, {"inicio_utc": r_["inicio_utc"], "instalacao_v413": "ainda nao houve"}
        ts_ = U.ler_json(APL413[-1]).get("ts")
        t_inst = datetime.datetime.strptime(str(ts_), "%Y%m%d_%H%M%S").astimezone()
        return ini_ < t_inst, {"inicio_utc": r_["inicio_utc"], "instalacao_v413": ts_}
    tenta("N1: o recibo pre-selo foi gerado com o Nos na v412, ANTES da instalacao da v413 (lido do recibo e do APLICADO_AO_CANONICO da v413, se ja existe)", _antes_da_instalacao)
    if BP["version"] == DBN.BANCADA_ANTERIOR:
        def _ainda_pina():
            v_ = PR["valido_enquanto"]["bancada_pina"]; m_raw = open(DBN._BANCADA_CONTRATOS, "rb").read(); m_ = json.loads(m_raw); c_ = m_.get("canonical") or {}
            return (m_.get("deployment_id") == v_["deployment_id"] and U.sha256_bytes(m_raw) == v_["manifesto_sha256"] and c_.get("version") == v_["version"]
                    and (c_.get("script") or {}).get("sha256") == v_["um_py_sha256"] and (c_.get("seal") or {}).get("sha256") == v_["seal_sha256"]), v_.get("deployment_id")
        tenta("a Bancada AINDA pina o que o recibo pre-selo viu (deployment, manifesto POR SHA256, versao, um.py, selo): o salto embute o sha do manifesto", _ainda_pina)
if not os.path.exists(DBN.PROVA_PRODUCAO_ARQ):
    pend("a prova de que a producao so' foi lida no pre-selo (PROVA_PRODUCAO_INTACTA_v413_pre_selo.json)", "o pre-selo do salto nao rodou")
else:
    tenta("a prova de que a producao so' foi lida no pre-selo: producao_intacta True", lambda: (U.ler_json(DBN.PROVA_PRODUCAO_ARQ).get("producao_intacta") is True, None))

# (6) o PINOS_BN_v413 (os pinos do B(n)): cada pino com arquivo confere com o disco; os pendentes dele sao pendentes aqui
if not os.path.exists(DBN.PINOS_BN_ARQ):
    pend("PINOS_BN_v413.json (os pinos do B(n) do salto)", "diff_e_pinos_bn_v413.py (passo 8 do pre-selo; o FINAL, com --delta e pendentes == [], antes do APLICAR)")
else:
    PBN = U.ler_json(DBN.PINOS_BN_ARQ)

    def _pbn():
        div_ = [k_ for k_, v_ in PBN.items() if isinstance(v_, dict) and v_.get("path") and v_.get("sha256") and (not os.path.exists(v_["path"]) or sha(v_["path"]) != v_["sha256"])]
        obr_ = [k_ for k_ in ("esboco_R3_6", "cadeia_de_selos", "selo_anterior_v412", "kernel_manifesto_anterior_v412", "delta_bn", "util_bn") if not (PBN.get(k_) or {}).get("sha256")]
        return (not div_ and not obr_ and (PBN.get("delta_bn") or {}).get("sha256") == sha(os.path.join(HERE, "delta_bn_v413.py")) and (PBN.get("util_bn") or {}).get("sha256") == sha(os.path.join(HERE, "util_bn_v413.py"))
                and (PBN.get("bancada_anterior_v411") or {}).get("deployment_id") == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"]), {"divergem": div_, "faltam": obr_}
    tenta("PINOS_BN_v413.json: todo pino com arquivo confere com o disco; a cadeia, os anteriores da v412, o delta_bn e o util_bn presentes e iguais aos de hoje; o anterior da Bancada e' o B20", _pbn)
    for p_ in PBN.get("pendentes") or []:
        pend("PINOS_BN_v413.json: o pino %s esta' pendente" % p_, "diff_e_pinos_bn_v413.py de novo quando o insumo existir (o FINAL antes do APLICAR: --delta <delta principal da v413>)")
    if (PBN.get("kernel_recibo") or {}).get("sha256"):
        # revisao M4: a arvore so-fontes que o recibo do kernel cita (o passo 10 AGUARDA sem ela; nao ha' refazer_arvore no molde da v413)
        tenta("M4: a arvore so-fontes do recibo do kernel da v413 (campo arvore) existe", lambda: (os.path.isdir(str(U.ler_json(PBN["kernel_recibo"]["path"]).get("arvore"))), U.ler_json(PBN["kernel_recibo"]["path"]).get("arvore")))

# (7) o sandbox curto (N8): o do delta, C:\t\vb<digitos>, e nao existe antes do pre-selo
SB = DBN.SANDBOX_CURTO
chk("N8/M1: o sandbox curto vem do delta_bn (C:\\t\\vb<digitos>) e nao e' o de outra versao (vb22, vb23) nem o das guardas estaticas da Etapa 2 (vb25)", os.path.normcase(os.path.dirname(SB)) == os.path.normcase(os.path.join("C:" + os.sep, "t")) and re.fullmatch(r"vb\d+", os.path.basename(SB)) and os.path.basename(SB) not in ("vb22", "vb23", "vb25"), SB)
if not os.path.exists(DBN.PINO_RECIBO_PRE_SELO_ARQ):
    chk("o sandbox curto %s NAO existe antes do pre-selo (o runner recusa rodar com ele)" % SB, not os.path.exists(SB), SB)

# (8) a autorizacao do pos-selo (N4): os eventos 1687 e 1689 no livro conferido INTEIRO e a fala do operador de 20/11
def _autorizacao():
    L_ = U.livro_conferido(DBN.QUADRO)
    e87, e89 = L_["eventos"].get(DBN.SEQ_AUTORIZACAO) or {}, L_["eventos"].get(DBN.SEQ_DECISAO) or {}
    d87, d89 = e87.get("dados") or {}, e89.get("dados") or {}
    ok_ = (e87.get("tipo") == "AVISO_AUTORIZACAO_RECEBIDA" and d87.get("versao") == "v412" and d87.get("unidade") == "F0.6" and os.path.isfile(str(d87.get("recibo"))) and sha(d87["recibo"]) == d87.get("sha256")
           and e89.get("tipo") == "AVISO_DECISAO_DO_OPERADOR_B21" and e89.get("quem") == "claude-c1" and d89.get("em_resposta_ao_evento") == DBN.SEQ_AUTORIZACAO and os.path.isfile(str(d89.get("fala")))
           and sha(d89["fala"])[:16] == d89.get("fala_sha16") and DBN.UM_VERSION_BN in str(d89.get("decisao_do_operador")) and os.path.isfile(DBN.FALA_AUTORIZACAO_20NOV))
    return ok_, {"n_elos": L_["n_elos"], "hash16_1687": str(e87.get("hash"))[:16], "hash16_1689": str(e89.get("hash"))[:16], "fala_20nov_sha16": sha(DBN.FALA_AUTORIZACAO_20NOV)[:16] if os.path.isfile(DBN.FALA_AUTORIZACAO_20NOV) else None}


tenta("N4: o livro do quadro conferido INTEIRO (2.2); os eventos 1687 (autorizacao do ciclo) e 1689 (salto na v413) conferem por hash com os arquivos que nomeiam; a fala do operador de 20/11 existe", _autorizacao)

# (9) a forma estatica dos scripts do B(n): existem, compilam (em memoria), `sh -n` nos .sh, nenhuma marca de adaptacao pendente, nenhum `python -c` nos .sh
SCRIPTS = ["delta_bn_v413.py", "util_bn_v413.py", "gerar_e_pinar_cadeia_v413.py", "gerar_bateria_v412_pre_selo_v413.py", "rodar_ensaio_1_pre_selo_v413.sh", "snap_producao_v413.py",
           "conferir_recibo_pre_selo_salto_v413.py", "gerar_pino_recibo_pre_selo_v413.py", "limpar_sandbox_vb24.py", "diff_e_pinos_bn_v413.py", "p00_precondicoes_bn_v413.py", "rodar_bn_pre_selo_v413.sh",
           "bn_v413.sh", "b3_recibo_v413.py", "recibo_parada_v413.py", "recibo_religamento_v413.py", "evento_c1_b3_v413.py", "fechar_bn_v413.py", "gravar_pino_bateria_v413.py", "conferir_exigencias_servico_v413.py",
           os.path.join("controle_negativo", "mutar_conferidor_v413.py"), "saude_bancada.py", "sentinela_boot_bancada.py", "montar_autorizacao_v413.py", "aviso_f06_v413.py",
           "ensaio_a_seco_pos_selo_v413.py"]


def _estatico():
    sh_ = shutil.which("sh") or r"C:\Program Files\Git\usr\bin\sh.exe"
    falhas_ = []
    marca_ = "[A ADAPTAR v" + "413]"
    for n_ in SCRIPTS:
        p_ = os.path.join(HERE, n_)
        if not os.path.isfile(p_):
            falhas_.append("ausente: " + n_); continue
        t_ = open(p_, "rb").read().decode("utf-8")
        if marca_ in t_:
            falhas_.append("marca de adaptacao pendente: " + n_)
        if n_.endswith(".py"):
            try:
                compile(t_, p_, "exec")
            except SyntaxError as e_:
                falhas_.append("nao compila: %s (%s)" % (n_, e_.msg))
        else:
            if subprocess.run([sh_, "-n", p_], capture_output=True, stdin=subprocess.DEVNULL).returncode != 0:
                falhas_.append("sh -n recusa: " + n_)
            _cod = [l_ for l_ in t_.splitlines() if l_.strip() and not l_.strip().startswith("#")]
            if any(re.search(r"(python[^\s]*|\$PY)\s+(-[A-Za-z]+\s+)*-c\s", l_) for l_ in _cod):
                falhas_.append("python -c num runner: " + n_)
    return not falhas_, falhas_


tenta("os scripts do B(n) existem, compilam (sem gravar .pyc), passam em `sh -n`, sem marca de adaptacao pendente e sem `python -c`", _estatico)
_tmps = [p_ for d_ in (HERE, DBN.OUTB_PRE_SELO, DBN.CADEIA_DIR, DBN.BATERIA_V412_DIR, DBN.SERVICO_DIR, DBN.SAIDAS_BN_DIR) for p_ in glob.glob(os.path.join(d_, "**", "*.tmp"), recursive=True)]
chk("D135: nenhum .tmp nas pastas do B(n)", not _tmps, _tmps[:5])

_v = "TODAS PASSARAM" if (ok_all and not PEND) else ("NENHUMA FALHA, %d PENDENTE(S)" % len(PEND) if ok_all else "FALHOU")
out = {"contrato": "PRECONDICOES_BN_v413", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "veredito": _v, "n_checagens": len(res), "n_ok": sum(1 for r_ in res if r_.get("ok") is True),
       "n_falhas": sum(1 for r_ in res if r_.get("ok") is False), "n_pendentes": len(PEND), "pendentes": PEND, "checagens": res,
       "escopo": "so leitura; o B(n) do salto v411 -> v413; NOT_FALSIFIED nao e' creditacao; o gate nao se move"}
p = DBN.PRECONDICOES_BN_ARQ
dados = (json.dumps(out, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p) and open(p, "rb").read() != dados:
    bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
    with open(bk, "xb") as fh:
        fh.write(open(p, "rb").read())
with open(p + ".tmp", "wb") as fh:
    fh.write(dados)
os.replace(p + ".tmp", p)
print(_v, "| %d ok, %d falha(s), %d pendente(s)" % (out["n_ok"], out["n_falhas"], out["n_pendentes"]), "|", p)
sys.exit(0 if _v == "TODAS PASSARAM" else (3 if ok_all else 1))

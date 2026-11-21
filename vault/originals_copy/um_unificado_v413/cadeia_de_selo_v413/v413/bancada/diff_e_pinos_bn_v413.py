# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/diff_e_pinos_v412.py, derivado para o SALTO v411 -> v413, com as pendencias 1.4 (o pino do proprio delta), 2.5 (o diff
# sem `diff` no PATH vai a `pendentes`) e N6 (os dois «anteriores»: o da Bancada e' a v411, o do um.py e' a v412). O delta PRINCIPAL da v413 (Etapa 2, outro agente) entra por --delta; sem ele, o que depende
# do candidato sai NAO_PREPARADO e entra em `pendentes` (pendente, nao erro), e o PINOS_BN serve ao pre-selo; o FINAL (pendentes == []) e' o que o bn_v413.sh exige antes do APLICAR (2.7).
"""diff_e_pinos_bn_v413.py -- grava PINOS_BN_v413.json (os sha256 que o elo B(n) do salto pede, LIDOS dos arquivos por script; path e sha256 recalculados aqui; nada digitado) e, quando o candidato e o
delta principal existem, DIFF_KERNEL_v413.txt e DIFF_v412_v413.diff (o que ja existe nao e' sobrescrito: tem de sair byte a byte igual, senao PARA).
Os pinos: o esboco R3.6 (que a cadeia usa; conferido contra CONTROLES_R3_6.json) e o R3.5 (registro); gerador, driver e base R2 da bateria (cadeia anterior); a CADEIA DE SELOS v411 -> v412 (o salto); o recibo
pre-selo do salto (PINO_RECIBO_PRE_SELO_v413.json: utilizavel, veredito exato, cadeia, salto) e a bateria do pre-selo (a da v412); N6: o anterior do UM.PY (selo e manifesto do kernel da v412, v413\\base_v412,
o fim da cadeia) e o anterior da BANCADA (o B20 da v411, com o recibo do religamento da v411); 1.4: o delta_bn_v413.py, o util_bn_v413.py e o delta principal (--delta); o candidato, ESPERADOS, os pins, o recibo
do kernel e o CRITERIOS da v413 (do delta principal). Recusa -O (as guardas sao assert). Backup de bytes do PINOS_BN anterior antes de regravar.
uso: python -I -B -X utf8 diff_e_pinos_bn_v413.py [--delta <o delta principal da v413>]"""
import sys

if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.dont_write_bytecode = True
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--delta", default=None, help="o delta PRINCIPAL da v413 (o do candidato, Etapa 2; ele importa o delta_bn_v413)")
a = ap.parse_args()
sha = U.sha256_arquivo
s8 = lambda t: U.sha256_bytes(t.encode("utf-8"))
f = lambda p, **kw: U.pinar(p, **kw) if (p and os.path.exists(p)) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
pendentes = []
pn = {}

# ---- N6: o anterior da BANCADA (v411, B20): a producao ainda o pina (o PINOS_BN e' gerado ANTES do APLICAR)
assert DBN.BANCADA_PINA_HOJE == DBN.BANCADA_PINA_HOJE_FIXADA_V411, ("a Bancada de producao ja nao pina o B20 da v411 (o PINOS_BN do salto e' gerado antes do APLICAR)", DBN.BANCADA_PINA_HOJE)
man_raw = open(DBN._BANCADA_CONTRATOS, "rb").read()
man = json.loads(man_raw)
pn["bancada_anterior_v411"] = {"deployment_id": man.get("deployment_id"), "version": (man.get("canonical") or {}).get("version"), "manifesto_sha256": U.sha256_bytes(man_raw),
                               "um_py_pinado": ((man.get("canonical") or {}).get("script") or {}).get("sha256"), "seal_sha_pinado": ((man.get("canonical") or {}).get("seal") or {}).get("sha256"),
                               "kernel_manifesto_registrado": (man.get("sincronizacao") or {}).get("kernel_manifesto_sha256"), "recibo_religamento_v411": f(DBN.RECIBO_RELIGAMENTO_V411),
                               "nota": "N6: o anterior da Bancada e' a v411 (a v412 nao teve B(n)); lido do canonical_contracts.json da producao (so' leitura) e do recibo do religamento da v411"}
assert pn["bancada_anterior_v411"]["version"] == DBN.BANCADA_ANTERIOR and pn["bancada_anterior_v411"]["deployment_id"] == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"]

# ---- os pinos herdados da cadeia anterior (recalculados do arquivo)
P11 = U.ler_json(DBN.PINOS_BN_V411_ARQ)


def do_v411(k):
    d = P11[k]
    assert os.path.exists(d["path"]) and sha(d["path"]) == d["sha256"], ("o pino herdado da v411 diverge do arquivo", k)
    return f(d["path"], origem="PINOS_BN_v411.json[%s] (recalculado do arquivo)" % k)


_e6 = do_v411("esboco_R3_6")
_c6 = U.ler_json(os.path.join(os.path.dirname(_e6["path"]), "CONTROLES_R3_6.json"))
assert _c6.get("veredito") == "R3_6_CONFERIDA_POR_SCRIPT" and _c6["modulos"]["R3_6"]["sha256"] == _e6["sha256"], "o esboco R3.6 pinado nao e' o que os controles da R3.6 conferiram (CONTROLES_R3_6.json)"
pn["esboco_R3_6"] = _e6
for _k in ("esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2"):
    pn[_k] = do_v411(_k)

# ---- a cadeia de selos v411 -> v412 (o salto), conferida contra o pino dela
pc = U.ler_json(DBN.PINO_CADEIA_ARQ)
assert os.path.normcase(os.path.abspath(pc["cadeia"]["path"])) == os.path.normcase(os.path.abspath(DBN.CADEIA_ARQ)) and sha(DBN.CADEIA_ARQ) == pc["cadeia"]["sha256"], "a cadeia em disco nao e' a do pino"
cj = U.ler_json(DBN.CADEIA_ARQ)
_vers = [e["versao"] for e in cj["elos"]]
assert cj.get("contrato") == "CADEIA_DE_SELOS_R3_4" and _vers == [DBN.BANCADA_ANTERIOR, DBN.UM_PY_ANTERIOR], ("a cadeia nao e' a v411 -> v412", cj.get("contrato"), _vers)
pn["cadeia_de_selos"] = f(DBN.CADEIA_ARQ, contrato=cj["contrato"], n_elos=len(cj["elos"]), versoes=_vers, pino_do_pino=f(DBN.PINO_CADEIA_ARQ),
                          nota="a cadeia de selos v411 -> v412 do salto (gerar_e_pinar_cadeia_v413.py; conferida pelo esboco R3.6): consistencia por hash, nao autenticidade")

# ---- N6: o anterior do UM.PY (v412 = o fim da cadeia): o selo e o manifesto do kernel da v412 (copias de bytes v413\base_v412)
SELO, KMAN, UMA = (os.path.join(DBN.BASE_UM_PY_ANTERIOR, n_) for n_ in ("um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "um.py"))
_selo = U.ler_json(SELO)
assert _selo.get("um_version") == DBN.UM_PY_ANTERIOR and (_selo.get("sha256") or {}).get("um.py") == sha(UMA) and (_selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") == sha(KMAN), \
    "o selo da base_v412 nao e' o da v412 ou nao pina o um.py e o manifesto do kernel da base"
assert sha(SELO) == cj["elos"][-1]["selo"]["sha256"] and sha(KMAN) == cj["elos"][-1]["kernel_manifesto"]["sha256"], "o selo ou o kernel da base_v412 nao sao os do ultimo elo da cadeia"
pn["selo_anterior_v412"] = f(SELO, nota="N6: o selo da v412 (o FIM da cadeia de selos; custodia v413\\base_v412): --selo-anterior")
pn["kernel_manifesto_anterior_v412"] = f(KMAN, nota="N6: o manifesto do kernel da v412 (custodia): --kernel-manifesto-anterior")

# ---- o recibo pre-selo do salto e a bateria do pre-selo
_PB = U.ler_json(os.path.join(DBN.BATERIA_V412_DIR, "PINOS_BATERIA_v412.json"))
if os.path.exists(DBN.PINO_RECIBO_PRE_SELO_ARQ):
    pr = U.ler_json(DBN.PINO_RECIBO_PRE_SELO_ARQ)
    assert sha(pr["path"]) == pr["sha256"], "o recibo pre-selo mudou desde o pino"
    serve = (pr.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and pr.get("veredito") == DBN.VEREDITO_PRE_SELO and pr.get("versao_nos") == DBN.VERSAO_DO_PRE_SELO
             and (pr.get("bancada_pina") or {}).get("deployment_id") == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"] and (pr.get("cadeia_de_selos") or {}).get("sha256") == pc["cadeia"]["sha256"]
             and isinstance(pr.get("salto"), dict) and (pr["salto"].get("cadeia") or {}).get("sha256") == pc["cadeia"]["sha256"] and pr["salto"].get("proxima_a_selar") == DBN.UM_VERSION_BN)
    if not serve:
        raise SystemExit("PARO: o recibo pre-selo pinado NAO serve ao B(n) do salto (utilizavel %r, veredito %r, versao_nos %r, cadeia %r): nada foi gravado"
                         % (pr.get("utilizavel_como_recibo_pre_selo_do_B_n"), pr.get("veredito"), pr.get("versao_nos"), str((pr.get("cadeia_de_selos") or {}).get("sha256"))[:16]))
    assert pr["bateria"]["sha256"] == _PB["bateria"]["sha256"], "a bateria do recibo pre-selo nao e' a da v412 pinada"
    pn["recibo_pre_selo"] = {"path": pr["path"], "sha256": pr["sha256"], "versao_nos": pr["versao_nos"], "veredito": pr["veredito"], "utilizavel_como_recibo_pre_selo_do_B_n": True,
                             "pino_do_pino": f(DBN.PINO_RECIBO_PRE_SELO_ARQ), "um_py_sha16_do_nos": pr["um_py_sha16_do_nos"], "bancada_pina": pr["bancada_pina"],
                             "cadeia_de_selos_sha256": pr["cadeia_de_selos"]["sha256"], "salto": pr["salto"]}
    pn["bateria_do_pre_selo"] = f(pr["bateria"]["path"], versao=DBN.VERSAO_DO_PRE_SELO, nota="a bateria do ensaio pre_selo do salto (a da v412, N2 caminho a); a do POS_SELO da v413 e' gerada pelo bn_v413.sh depois do selo")
else:
    pn["recibo_pre_selo"] = {"path": DBN.PINO_RECIBO_PRE_SELO_ARQ, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "o pre-selo do salto (rodar_bn_pre_selo_v413.sh) ainda nao gravou PINO_RECIBO_PRE_SELO_v413.json"}
    pn["bateria_do_pre_selo"] = {"path": _PB["bateria"]["path"], "sha256": None, "estado": "NAO_PREPARADO", "motivo": "depende do recibo pre-selo"}
    pendentes += ["recibo_pre_selo", "bateria_do_pre_selo"]

# ---- 1.4: os deltas e a biblioteca do B(n), por sha (o pos-selo recusa um delta trocado)
pn["delta_bn"] = f(os.path.join(HERE, "delta_bn_v413.py"), nota="o delta so' do B(n) (constantes, BANCADA_PINA_HOJE da v411 fixado, sandbox curto)")
pn["util_bn"] = f(os.path.join(HERE, "util_bn_v413.py"), nota="as funcoes comuns dos scripts do B(n) (livro do quadro conferido inteiro; linha de comando dos .sh)")
DL = None
if a.delta:
    _dp = os.path.abspath(a.delta)
    assert os.path.isfile(_dp), _dp
    assert "delta_bn_v413" in open(_dp, encoding="utf-8").read(), "o delta principal dado nao importa o delta_bn_v413 (a ordem: ele importa este)"
    _sp = importlib.util.spec_from_file_location("delta_principal_v413_pelo_diff_e_pinos_bn", _dp)
    DL = importlib.util.module_from_spec(_sp)
    _sp.loader.exec_module(DL)
    assert DL.UM_VERSION == DBN.UM_VERSION_BN and DL.BASE_VERSION == DBN.UM_PY_ANTERIOR, ("o delta principal nao e' o da v413 sobre a v412", DL.UM_VERSION, DL.BASE_VERSION)
    assert os.path.normcase(os.path.abspath(os.path.join(DBN.V413, DL.BASE_DIR))) == os.path.normcase(os.path.abspath(DBN.BASE_UM_PY_ANTERIOR)), ("a base do delta principal nao e' v413\\base_v412", DL.BASE_DIR)
    pn["delta"] = f(_dp, nota="o delta principal da v413 (o do candidato; 1.4): o pos-selo recusa um delta trocado")
    CAND, KR_P, ESP_P, PINS_P = DL.CANDIDATO_ARQ, os.path.join(DBN.V413, DL.KERNEL_DIR, "KERNEL_RECIBO_%s.json" % DBN.UM_VERSION_BN), DL.saida("ESPERADOS_%s.json" % DBN.UM_VERSION_BN), DL.PINS_ARQ
else:
    pn["delta"] = {"path": None, "sha256": None, "estado": "NAO_PREPARADO", "motivo": "sem --delta: o delta principal da v413 (Etapa 2) ainda nao foi dado a este script"}
    pendentes.append("delta")
    CAND = KR_P = ESP_P = PINS_P = None
CRI_P = os.path.join(DBN.V413, "vinculo", "CRITERIOS_%s.json" % DBN.UM_VERSION_BN)
for _k, _p in (("candidato", CAND), ("kernel_recibo", KR_P), ("esperados", ESP_P), ("pins_do_candidato", PINS_P), ("criterios", CRI_P)):
    pn[_k] = f(_p)
    if pn[_k].get("sha256") is None:
        pendentes.append(_k)
if pn["esperados"].get("sha256") and pn["candidato"].get("sha256"):
    assert U.ler_json(ESP_P).get("candidato_sha16") == pn["candidato"]["sha256"][:16], "o ESPERADOS_v413.json nao e' o do candidato"
if pn["criterios"].get("sha256"):
    _cr = U.ler_json(CRI_P)
    assert _cr.get("versao") == DBN.UM_VERSION_BN and _cr.get("preenchido") is True, "o CRITERIOS_v413.json nao e' o da v413 preenchido"
KR = None
if pn["kernel_recibo"].get("sha256"):
    KR = U.ler_json(KR_P)
    assert KR.get("versao") == DBN.UM_VERSION_BN and KR.get("rc") == 0 and KR.get("sorry") == 0 and KR.get("erros") == 0, ("o recibo do kernel da v413 nao e' rc 0 sem sorry nem erro", {k_: KR.get(k_) for k_ in ("versao", "rc", "sorry", "erros")})
    pn["kernel_recibo"].update(contrato=KR.get("contrato"), n_pedras=len(KR.get("pedras") or []), modulos_de_auditoria=KR.get("modulos_de_auditoria", []))

# ---- os dois diffs (so' com o candidato e o delta principal); 2.5: sem `diff` no PATH, o do um.py vai a `pendentes`
_NDK, _NDD = "DIFF_KERNEL_%s.txt" % DBN.UM_VERSION_BN, "DIFF_%s_%s.diff" % (DBN.UM_PY_ANTERIOR, DBN.UM_VERSION_BN)
diffs = {}
if DL is not None and pn["candidato"].get("sha256"):
    sys.path.insert(0, os.path.join(DBN.WK, "v390_pacote"))
    from carregar_embutido import carregar  # noqa: E402
    _REC = DL.saida("DIFFS_%s_RECIBO.json" % DBN.UM_VERSION_BN)
    _rec = U.ler_json(_REC) if os.path.exists(_REC) else {}

    def grava_ou_confere(nome_, b_):
        """o que JA EXISTE nao e' sobrescrito: tem de ser byte a byte `b_` (e ter o sha256 do recibo da gerencia, se ele o lista), senao PARA; o que falta e' gravado por temporario + os.replace."""
        p_ = DL.saida(nome_)
        r_ = _rec.get(nome_) or {}
        if os.path.exists(p_):
            a_ = open(p_, "rb").read()
            assert a_ == b_, ("%s JA EXISTE e nao e' o que este script geraria: PARO sem sobrescrever" % nome_, U.sha256_bytes(a_)[:16], U.sha256_bytes(b_)[:16])
            assert r_.get("sha256") in (None, U.sha256_bytes(a_)), ("%s em disco != o sha256 do recibo" % nome_)
            return {"estado": "JA_EXISTIA_IDENTICO__NAO_SOBRESCRITO", "sha256": U.sha256_bytes(a_), "bytes": len(a_)}
        with open(p_ + ".tmp", "wb") as fh_:
            fh_.write(b_)
        os.replace(p_ + ".tmp", p_)
        assert open(p_, "rb").read() == b_, "o %s gravado nao confere" % nome_
        return {"estado": "GRAVADO", "sha256": U.sha256_bytes(b_), "bytes": len(b_)}
    E0, _, _, h0 = carregar(UMA)
    E1, _, _, h1 = carregar(CAND)
    novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
    out = ["DIFF DO KERNEL EMBUTIDO %s (%s) -> %s (%s)" % (DBN.UM_PY_ANTERIOR, h0, DBN.UM_VERSION_BN, h1), "", "novos (%d):" % len(novos)]
    out += ["  + %s  %s  %d B" % (k, s8(E1[k])[:16], len(E1[k].encode("utf-8"))) for k in novos]
    out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos]
    out += ["", "mudados (%d):" % len(mudados)] + ["  ~ %s  %s -> %s" % (k, s8(E0[k])[:16], s8(E1[k])[:16]) for k in mudados]
    out += ["", "a %s muda o kernel embutido em %d arquivo(s) novo(s) e %d mudado(s) (%d -> %d arquivos); nenhum removido" % (DBN.UM_VERSION_BN, len(novos), len(mudados), len(E0), len(E1))]
    assert not removidos, ("o kernel embutido da v413 remove arquivos da v412", removidos[:10])
    if KR is not None and KR.get("pedras"):
        # a regra N1l do esboco (as pedras do recibo sao EXATAMENTE os arquivos formais novos ou mudados, fora a raiz e o Audit), conferida aqui contra o kernel EMBUTIDO, por caminho e sha256
        _esp = sorted((set(novos) | set(mudados)) - {"TGLExt.lean", "TGL/Audit.lean"})
        _kp = dict((p_["path"], p_["sha256"]) for p_ in KR["pedras"])
        assert len(_kp) == len(KR["pedras"]) and sorted(_kp) == _esp, ("as pedras do recibo do kernel != os arquivos novos ou mudados do kernel embutido (fora a raiz e o Audit)", sorted(set(_kp) ^ set(_esp))[:10])
        assert not [k for k in _esp if _kp[k] != s8(E1[k])], "pedra do recibo do kernel com sha256 != o do embutido"
    diffs[_NDK] = grava_ou_confere(_NDK, ("\n".join(out) + "\n").encode("utf-8"))
    _dif = shutil.which("diff")
    if _dif:
        _r = subprocess.run([_dif, "-u", "--label", "um.py %s %s" % (DBN.UM_PY_ANTERIOR, h0), "--label", "um.py %s %s" % (DBN.UM_VERSION_BN, h1), UMA, CAND], capture_output=True)
        assert _r.returncode in (0, 1), ("diff -u falhou", _r.returncode, _r.stderr[:300])
        diffs[_NDD] = dict(grava_ou_confere(_NDD, _r.stdout), ferramenta=_dif, rc=_r.returncode)
    else:
        diffs[_NDD] = {"estado": "NAO_GERADO_NEM_CONFERIDO: diff -u nao esta no PATH", "ja_existe": os.path.exists(DL.saida(_NDD))}
        pendentes.append(_NDD)
else:
    diffs = {_NDK: {"estado": "NAO_PREPARADO: depende do candidato e do delta principal"}, _NDD: {"estado": "NAO_PREPARADO: depende do candidato e do delta principal"}}
    pendentes += [_NDK, _NDD]
pn["diffs"] = diffs
pn["nota"] = ("[REAL] lido dos arquivos por script (diff_e_pinos_bn_v413.py): path e sha256 RECALCULADOS; o B(n) da v413 e' o SALTO v411 -> v413 (a Bancada de producao pina %s; o Nos do pre-selo era a v412): "
              "o pino cadeia_de_selos e' obrigatorio, o b3_recibo recebe o sha dele como terceiro argumento, o veredito do pos-selo e' %s e o do APLICAR %s; N6: o anterior da Bancada e' a v411 (bancada_anterior_v411), "
              "o do um.py e' a v412 (selo_anterior_v412, kernel_manifesto_anterior_v412); o esboco que a cadeia usa e' o R3.6 (esboco_R3_6, herdado de PINOS_BN_v411.json e conferido contra CONTROLES_R3_6.json)."
              % (DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"], DBN.VEREDITO_ENSAIO_POS_SELO, DBN.VEREDITO_APLICAR))
bad = [k for k, v in pn.items() if isinstance(v, dict) and "path" in v and v.get("sha256") is None and k not in pendentes]
assert not bad, ("pino sem arquivo fora de pendentes", bad)
pn["pendentes"] = pendentes
_pp = DBN.PINOS_BN_ARQ
dados = (json.dumps(pn, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
backup = None
if os.path.exists(_pp):
    _antes = open(_pp, "rb").read()
    if _antes != dados:
        backup = _pp + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
        with open(backup, "xb") as fh:
            fh.write(_antes)
        assert open(backup, "rb").read() == _antes, "o backup de bytes do PINOS_BN anterior nao confere"
with open(_pp + ".tmp", "wb") as fh:
    fh.write(dados)
assert os.path.getsize(_pp + ".tmp") == len(dados)
os.replace(_pp + ".tmp", _pp)
assert open(_pp, "rb").read() == dados
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict) and "sha256" in v})
print("PINOS_BN:", _pp, sha(_pp)[:16], "| backup do anterior:", backup, "| B(n) do salto:", DBN.B_N_SEGUINTE, "| pendentes:", pendentes or "nenhum")

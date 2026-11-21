# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] pendencia C.1: o conferir do SALTO (o herdado, v412/bateria_pre_selo/conferir_recibo_pre_selo_v412.py, reprova o salto por desenho:
# exige JA_SINCRONIZADA, ausencia de salto e contrato OK). Mesmo corpo (condicoes por script + controles negativos pela funcao do esboco), com as regras do salto do esboco R3.6 (l.1054-1155).
"""conferir_recibo_pre_selo_salto_v413.py -- SO LEITURA. Confere o recibo pre_selo do ensaio do SALTO (v413\\bateria_pre_selo\\ensaio_1) PELO MESMO CAMINHO que o B(n) pos_selo da v413 usara:
MOD.conferir_recibo_pre_selo(RP, ant, PRODUCAO, False, RSHA, SELO_V412, KM_V412, cadeia) do esboco R3.6 PINADO (ja_sincronizada=False: no pos-selo a Bancada ainda pinara a v411), com:
  - a cadeia carregada por MOD.carregar_cadeia_de_selos(CAD, CAD_SHA) (o pino da cadeia, conferido contra o disco);
  - o selo e o manifesto do kernel anteriores = os da v412 (N6: o anterior do UM.PY; copias de bytes v413\\base_v412), porque num salto o selo anterior e' o do FIM da cadeia (l.1079-1080, 1135-1140).
Repete por script cada condicao (nome, observado, esperado): o veredito EXATO do salto (REPINADA_B<GER+1>__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA); salto.de == a Bancada (v411, um.py, selo,
manifesto e deployment); salto.ate == o Nos lido no ensaio == a base_v412 (v412); proxima_a_selar v413; a cadeia do salto == a pinada; versao_alvo v412; estado PIN_CHANGED com pino_velho_recusado_pelo_instalado;
pinos_da_versao v412. Controles negativos (a funcao do esboco tem de RECUSAR cada um): sem cadeia, sha da cadeia errado, selo anterior da v411, veredito JA_SINCRONIZADA, bloco salto adulterado, geracao errada,
sha do recibo errado, bateria falhou, um.py de outra versao. Nada e' escrito na producao nem no Nos; grava so' conferencia_pelo_esboco_v413.json ao lado do ensaio e as copias adulteradas em <sandbox curto>\\ctl.
uso: python -I -B -X utf8 conferir_recibo_pre_selo_salto_v413.py   (rc 0 so' se utilizavel)"""
import sys

sys.dont_write_bytecode = True
import glob
import hashlib
import importlib.util
import json
import os
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

OUTB = DBN.OUTB_PRE_SELO
os.makedirs(OUTB, exist_ok=True)
CTL = os.path.join(DBN.SANDBOX_CURTO, "ctl")
PRODUCAO = Path(DBN.PRODUCAO)
sha = U.sha256_arquivo
lj = U.ler_json

# os pinos: o esboco R3.6 (cadeia anterior), a bateria da v412 (N2) e a cadeia v411 -> v412, LIDOS dos pinos e conferidos contra o disco
pbn = lj(DBN.PINOS_BN_V411_ARQ)
pbat = lj(os.path.join(DBN.BATERIA_V412_DIR, "PINOS_BATERIA_v412.json"))
pcad = lj(DBN.PINO_CADEIA_ARQ)
ESB, ESB_SHA = pbn["esboco_R3_6"]["path"], pbn["esboco_R3_6"]["sha256"]
BAT, BAT_SHA = pbat["bateria"]["path"], pbat["bateria"]["sha256"]
CAD, CAD_SHA = pcad["cadeia"]["path"], pcad["cadeia"]["sha256"]
assert sha(ESB) == ESB_SHA, "o esboco R3.6 em disco nao e' o pinado"
assert sha(BAT) == BAT_SHA, "a bateria da v412 em disco nao e' a pinada"
assert sha(CAD) == CAD_SHA, "a cadeia de selos em disco nao e' a pinada"

spec = importlib.util.spec_from_file_location("sincronizar_bancada_r36_conferir_salto_v413", ESB)
MOD = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MOD
spec.loader.exec_module(MOD)

ENS = os.path.join(OUTB, "ensaio_1")
rps = glob.glob(os.path.join(ENS, "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.VERSAO_DO_PRE_SELO))
assert len(rps) == 1, rps
RP = rps[0]
raw = open(RP, "rb").read()
RSHA = hashlib.sha256(raw).hexdigest()
r = json.loads(raw.decode("utf-8"))
out_txt = open(os.path.join(OUTB, "etapa1_stdout.txt"), encoding="utf-8").read().splitlines()
imp = json.loads([l for l in out_txt if l.strip().startswith("{")][-1])
rc_lancador = int([l for l in out_txt if l.startswith("ETAPA1_RC=")][-1].split("=", 1)[1])

SELO_ANT = os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um_absoluto_selo.json")         # N6: o anterior do UM.PY (v412), o FIM da cadeia
KM_ANT = os.path.join(DBN.BASE_UM_PY_ANTERIOR, "tgl_kernel_proof_manifest.json")
UM_ANT = os.path.join(DBN.BASE_UM_PY_ANTERIOR, "um.py")
SELO_V411 = os.path.join(DBN.BASE_BANCADA_ANTERIOR, "um_absoluto_selo.json")      # o anterior da BANCADA (v411): o controle «selo anterior da v411»
KM_V411 = os.path.join(DBN.BASE_BANCADA_ANTERIOR, "tgl_kernel_proof_manifest.json")
for p_ in (SELO_ANT, KM_ANT, UM_ANT, SELO_V411, KM_V411):
    assert os.path.isfile(p_), p_

canon, _pin = MOD.carregar_canonical(PRODUCAO)
ant = MOD.estado_anterior(PRODUCAO, canon)          # so leitura da producao, como o B(n) faz
GER = int(MOD.RE_GERACAO.match(str(ant["deployment_id"])).group(1))   # a geracao que a Bancada pina agora; o salto grava a GER+1
cad = MOD.carregar_cadeia_de_selos(Path(CAD), CAD_SHA)


def conferir(rp, sha_esp, selo, km, cadeia="__a_pinada__"):
    try:
        res_ = MOD.conferir_recibo_pre_selo(Path(rp), ant, PRODUCAO, False, sha_esp, selo, km, cad if cadeia == "__a_pinada__" else cadeia)
        return True, None, res_
    except MOD.Recusa as exc:
        return False, str(exc), None


aceito, recusa, res = conferir(RP, RSHA, SELO_ANT, KM_ANT)

checks = []


def chk(nome, ok, observado, esperado):
    checks.append({"nome": nome, "ok": bool(ok), "observado": observado, "esperado": esperado})


H64 = lambda x: isinstance(x, str) and len(x) == 64 and all(c in "0123456789abcdef" for c in x)
bat = r.get("bateria_resultado") or {}
ids = {t.get("id"): t.get("resultado") for t in bat.get("testes") or []}
nos = r.get("nos") or {}
kern = nos.get("kernel") or {}
selo_r = nos.get("selo") or {}
pv = (r.get("bateria") or {}).get("pinos_da_versao") or {}
sal = r.get("salto") or {}
sal_de, sal_ate = sal.get("de") or {}, sal.get("ate") or {}
selo_ant_j = lj(SELO_ANT)
pin_k = str((selo_ant_j.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") or "")
man_sinc = (ant["_man"].get("sincronizacao") or {})
esperado_salto = MOD.montar_salto(cad, ant)
ma_r = r.get("manifesto_anterior") or {}

chk("fase", r.get("fase") == "pre_selo", r.get("fase"), "pre_selo")
chk("modo_ensaio_nada_gravado", r.get("modo") == "ensaio" and str(r.get("veredito") or "").endswith("__ENSAIO__NADA_GRAVADO_NA_BANCADA"), [r.get("modo"), r.get("veredito")], "ensaio / ...__ENSAIO__NADA_GRAVADO_NA_BANCADA")
chk("bateria_passa", bat.get("veredito") == "BATERIA_PASSA", bat.get("veredito"), "BATERIA_PASSA")
chk("veredito_exato_do_salto", r.get("veredito") == "REPINADA_B%d__SALTO_%s_%s__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (GER + 1, DBN.BANCADA_ANTERIOR, DBN.VERSAO_DO_PRE_SELO) == DBN.VEREDITO_PRE_SELO,
    [r.get("veredito"), GER + 1], DBN.VEREDITO_PRE_SELO)
chk("salto_declarado_com_o_contrato_do_esboco", sal.get("declarado") is True and sal.get("contrato") == MOD.SALTO_CONTRATO, [sal.get("declarado"), sal.get("contrato")], [True, MOD.SALTO_CONTRATO])
chk("salto_do_recibo_igual_ao_que_a_cadeia_e_a_bancada_dizem", json.dumps(sal, sort_keys=True) == json.dumps(esperado_salto, sort_keys=True), sorted(sal), "o bloco de montar_salto(cadeia, Bancada)")
chk("salto_de_e_a_bancada", (sal_de.get("versao"), sal_de.get("um_py_sha256"), sal_de.get("selo_sha256"), sal_de.get("manifesto_da_bancada_sha256"), sal_de.get("deployment_id"))
    == (ant["version"], ant["um_py_pinado"], ant["seal_sha_pinado"], ant["sha256"], ant["deployment_id"]) and ant["version"] == DBN.BANCADA_ANTERIOR and ant["deployment_id"] == DBN.BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"],
    {k_: str(v_)[:16] for k_, v_ in sal_de.items()}, {"versao": ant["version"], "deployment_id": ant["deployment_id"]})
chk("salto_ate_e_o_nos_lido_no_ensaio_e_a_base_v412", sal_ate.get("versao") == DBN.VERSAO_DO_PRE_SELO and sal_ate.get("um_py_sha256") == (nos.get("um_py") or {}).get("sha256") == sha(UM_ANT)
    and sal_ate.get("selo_sha256") == selo_r.get("sha256") == sha(SELO_ANT) and sal_ate.get("kernel_manifesto_sha256") == kern.get("sha256") == sha(KM_ANT),
    {k_: str(v_)[:16] for k_, v_ in sal_ate.items()}, "v412 = o Nos do recibo = v413\\base_v412")
chk("versoes_puladas_e_proxima_a_selar", sal.get("versoes_puladas") == [DBN.VERSAO_DO_PRE_SELO] and sal.get("proxima_a_selar") == DBN.UM_VERSION_BN, [sal.get("versoes_puladas"), sal.get("proxima_a_selar")],
    [[DBN.VERSAO_DO_PRE_SELO], DBN.UM_VERSION_BN])
chk("cadeia_do_salto_e_a_pinada", (sal.get("cadeia") or {}).get("sha256") == CAD_SHA == (r.get("cadeia_de_selos") or {}).get("sha256"), [str((sal.get("cadeia") or {}).get("sha256"))[:16], CAD_SHA[:16]], "iguais")
chk("versao_alvo_e_a_do_nos_no_pre_selo", r.get("versao_alvo") == DBN.VERSAO_DO_PRE_SELO, r.get("versao_alvo"), DBN.VERSAO_DO_PRE_SELO)
chk("estado_do_contrato_instalado_pin_changed", ant["estado_do_contrato_instalado"] == "PIN_CHANGED" and ma_r.get("estado_do_contrato_instalado") == "PIN_CHANGED"
    and r.get("pino_velho_recusado_pelo_instalado") == "PIN_CHANGED", [ant["estado_do_contrato_instalado"], ma_r.get("estado_do_contrato_instalado"), r.get("pino_velho_recusado_pelo_instalado")], "PIN_CHANGED x3")
chk("manifesto_anterior_do_recibo_e_o_da_producao_agora", (ma_r.get("sha256"), ma_r.get("deployment_id"), ma_r.get("version")) == (ant["sha256"], ant["deployment_id"], ant["version"]),
    [ma_r.get("deployment_id"), str(ma_r.get("sha256"))[:16]], [ant["deployment_id"], ant["sha256"][:16]])
chk("manifesto_novo_do_ensaio_e_da_geracao_do_salto", str((r.get("manifesto_novo") or {}).get("deployment_id") or "").startswith("B%d-%s-" % (GER + 1, DBN.VERSAO_DO_PRE_SELO)) and r.get("aplicacao") is None,
    [(r.get("manifesto_novo") or {}).get("deployment_id"), r.get("aplicacao")], "B%d-%s-... e nenhuma aplicacao" % (GER + 1, DBN.VERSAO_DO_PRE_SELO))
chk("bancada_do_recibo_e_a_producao_por_identidade", os.path.samefile((r.get("bancada") or {}).get("dir"), str(PRODUCAO)), (r.get("bancada") or {}).get("dir"), str(PRODUCAO))
chk("T01_e_T15_passam", ids.get("T01_IDENTIDADE") == "PASSA" and ids.get("T15_SONDAS") == "PASSA", [ids.get("T01_IDENTIDADE"), ids.get("T15_SONDAS")], "PASSA e PASSA")
chk("kernel_do_recibo_completo", all(H64(kern.get(c)) for c in ("sha256", "raiz_sha256", "audit_sha256", "impressao_formal")), sorted(k for k in kern if H64(kern.get(k))), "sha256, raiz_sha256, audit_sha256, impressao_formal")
chk("manifesto_do_kernel_do_recibo_igual_ao_pino_do_selo_do_recibo", kern.get("sha256") == selo_r.get("tgl_kernel_proof_manifest_sha256"), [str(kern.get("sha256"))[:16], str(selo_r.get("tgl_kernel_proof_manifest_sha256"))[:16]], "iguais")
chk("selo_anterior_da_custodia_e_o_fim_da_cadeia_v412", sha(SELO_ANT) == sal_ate.get("selo_sha256") == cad["elos"][-1]["selo"]["sha256"] and selo_ant_j.get("um_version") == DBN.VERSAO_DO_PRE_SELO,
    [sha(SELO_ANT)[:16], selo_ant_j.get("um_version")], "o selo do ultimo elo (v412)")
chk("manifesto_do_kernel_da_custodia_igual_ao_pino_do_selo_anterior", sha(KM_ANT) == pin_k == cad["elos"][-1]["kernel_manifesto"]["sha256"], [sha(KM_ANT)[:16], pin_k[:16]], "iguais")
chk("kernel_registrado_na_bancada_e_o_do_inicio_da_cadeia", str(man_sinc.get("kernel_manifesto_sha256")).lower() == cad["elos"][0]["kernel_manifesto"]["sha256"] == sal_de.get("kernel_manifesto_sha256"),
    [str(man_sinc.get("kernel_manifesto_sha256"))[:16], cad["elos"][0]["kernel_manifesto"]["sha256"][:16]], "iguais (v411)")
chk("pinos_da_versao_da_bateria_da_v412_conferidos_contra_o_nos_lido", pv.get("declarados") is True and pv.get("conferidos_contra_o_nos_lido") is True and pv.get("versao") == DBN.VERSAO_DO_PRE_SELO,
    {k: pv.get(k) for k in ("declarados", "conferidos_contra_o_nos_lido", "versao")}, "declarados, conferidos, v412")
chk("script_do_recibo_e_o_esboco_pinado", r.get("script_sha256") == ESB_SHA, [str(r.get("script_sha256"))[:16], ESB_SHA[:16]], "iguais")
chk("bateria_do_recibo_e_a_pinada", (r.get("bateria") or {}).get("sha256") == BAT_SHA, [str((r.get("bateria") or {}).get("sha256"))[:16], BAT_SHA[:16]], "iguais")
chk("stdout_cita_o_recibo_com_o_sha_lido", imp.get("recibo_sha256") == RSHA and os.path.samefile(imp.get("recibo"), RP), [str(imp.get("recibo_sha256"))[:16], RSHA[:16]], "iguais")
chk("lancador_saiu_com_rc_0", rc_lancador == 0, rc_lancador, 0)

# ---- controles negativos: a funcao do esboco tem de RECUSAR cada adulteracao (as copias ficam em <sandbox curto>\ctl)
os.makedirs(CTL, exist_ok=True)
controles = []


def controle(nome, esperado_prefixo, ok_recusou, recusa_txt):
    controles.append({"nome": nome, "recusou": (not ok_recusou), "esperado_comecar_por": esperado_prefixo, "recusa": recusa_txt,
                      "como_esperado": (not ok_recusou) and str(recusa_txt).startswith(esperado_prefixo)})


def mutado(nome, fn):
    m = json.loads(raw.decode("utf-8"))
    fn(m)
    b = (json.dumps(m, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    p = os.path.join(CTL, nome + ".json")
    with open(p, "wb") as fh:
        fh.write(b)
    return p, hashlib.sha256(b).hexdigest()


ok, rec_t, _ = conferir(RP, RSHA, SELO_ANT, KM_ANT, cadeia=None)
controle("sem_cadeia", "RECIBO_PRE_SELO_SALTO_SEM_CADEIA", ok, rec_t)
try:
    MOD.carregar_cadeia_de_selos(Path(CAD), "0" * 64)
    controle("sha_da_cadeia_errado", "CADEIA_DE_SELOS_SHA_DIVERGE", True, None)
except MOD.Recusa as exc:
    controle("sha_da_cadeia_errado", "CADEIA_DE_SELOS_SHA_DIVERGE", False, str(exc))
ok, rec_t, _ = conferir(RP, RSHA, SELO_V411, KM_V411)
controle("selo_anterior_e_o_da_v411_nao_o_fim_da_cadeia", "SELO_ANTERIOR_NAO_E_O_PINADO", ok, rec_t)
p, s_ = mutado("veredito_ja_sincronizada", lambda m: m.__setitem__("veredito", "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA"))
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("veredito_ja_sincronizada", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)


def _salto_adulterado(m):
    m["salto"]["de"]["deployment_id"] = "B19-v410-20261111-R1"


p, s_ = mutado("salto_adulterado", _salto_adulterado)
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("bloco_salto_adulterado", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)
p, s_ = mutado("geracao_errada", lambda m: m.__setitem__("veredito", "REPINADA_B%d__SALTO_%s_%s__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (GER + 2, DBN.BANCADA_ANTERIOR, DBN.VERSAO_DO_PRE_SELO)))
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("veredito_do_salto_com_a_geracao_errada", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)
ok, rec_t, _ = conferir(RP, "0" * 64, SELO_ANT, KM_ANT)
controle("sha_do_recibo_errado", "RECIBO_PRE_SELO_SHA_DIVERGE", ok, rec_t)


def _bat_falha(m):
    m["bateria_resultado"]["veredito"] = "BATERIA_FALHOU"


p, s_ = mutado("bateria_falhou", _bat_falha)
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("bateria_nao_passa", "RECIBO_PRE_SELO_INVALIDO", ok, rec_t)


def _um_outro(m):
    m["nos"]["um_py"]["sha256"] = "1" * 64


p, s_ = mutado("um_py_de_outra_versao", _um_outro)
ok, rec_t, _ = conferir(p, s_, SELO_ANT, KM_ANT)
controle("um_py_do_recibo_nao_e_o_fim_da_cadeia", "RECIBO_PRE_SELO_NAO_CORRESPONDE", ok, rec_t)

motivos = [c["nome"] + ": observado %r, esperado %r" % (c["observado"], c["esperado"]) for c in checks if not c["ok"]]
if not aceito:
    motivos.append("conferir_recibo_pre_selo do esboco R3.6 RECUSOU: %s" % recusa)
motivos += ["controle negativo nao recusou como esperado: " + c["nome"] for c in controles if not c["como_esperado"]]
utilizavel = (not motivos)
resumo_res = None
if res is not None:
    resumo_res = {k: res.get(k) for k in ("path", "sha256", "bytes", "versao", "veredito", "um_py_sha256", "bancada_dir", "bateria", "selo_sha256", "selo_cruzado_com_o_manifesto_anterior",
                                          "kernel_manifesto_anterior_sha256", "kernel_anterior", "salto")}
    resumo_res["kernel_cruzado_com_o_selo_anterior"] = res.get("kernel_cruzado_com_o_selo_anterior")
conf = {
    "contrato": "CONFERENCIA_PELO_ESBOCO_RECIBO_PRE_SELO_DO_SALTO_v413",
    "como": ("conferir_recibo_pre_selo do esboco R3.6 com ja_sincronizada=False (no pos-selo da v413 a Bancada ainda pinara a v411), COM a cadeia de selos v411 -> v412 pinada; selo e manifesto do kernel "
             "anteriores = os da v412 (o fim da cadeia; copias de bytes v413\\base_v412); producao so' lida"),
    "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))},
    "esboco": {"path": ESB, "sha256": ESB_SHA, "revisao": getattr(MOD, "REVISAO", None)},
    "bateria": {"path": BAT, "sha256": BAT_SHA},
    "cadeia": {"path": CAD, "sha256": CAD_SHA, "n_elos": cad["n_elos"], "versoes": cad["versoes"]},
    "recibo": {"path": RP, "sha256": RSHA, "bytes": len(raw)},
    "selo_anterior": {"path": SELO_ANT, "sha256": sha(SELO_ANT)},
    "kernel_manifesto_anterior": {"path": KM_ANT, "sha256": sha(KM_ANT)},
    "bancada_de_producao_lida": {"deployment_id": ant["deployment_id"], "version": ant["version"], "manifesto_sha256": ant["sha256"], "um_py_pinado": ant["um_py_pinado"],
                                 "seal_sha_pinado": ant["seal_sha_pinado"], "estado_do_contrato_instalado": ant["estado_do_contrato_instalado"]},
    "esboco_aceita": aceito, "recusa_do_esboco": recusa, "resultado_do_esboco": resumo_res,
    "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
    "controles_negativos": controles, "n_controles_como_esperado": sum(1 for c in controles if c["como_esperado"]),
    "utilizavel_como_recibo_pre_selo_do_B_n": utilizavel, "motivos_de_nao_ser_utilizavel": motivos,
    "validade": ("vale enquanto a Bancada de producao pinar o que esta' em bancada_de_producao_lida (o salto embute o sha do manifesto e o deployment_id); um re-pino da producao antes do B(n) da v413 torna o recibo "
                 "obsoleto e a conferencia do esboco o recusa; e so' serve ao pos-selo da v413 (o salto termina na v412: SALTO_VERSAO_NAO_CONSECUTIVA para outra versao)"),
    "escopo": "so leitura da producao; nada gravado na Bancada nem no Nos; NOT_FALSIFIED nao e' creditacao; o gate nao se move",
}
dest = os.path.join(OUTB, "conferencia_pelo_esboco_v413.json")
U.gravar_json_novo(dest, conf)
print(json.dumps({"arquivo": dest, "sha16": sha(dest)[:16], "esboco_aceita": aceito, "recusa": recusa, "condicoes_ok": "%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]),
                  "controles_como_esperado": "%d/%d" % (conf["n_controles_como_esperado"], len(controles)), "utilizavel": utilizavel, "motivos": motivos}, ensure_ascii=False))
sys.exit(0 if utilizavel else 1)

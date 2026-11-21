# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] molde v412/bateria_pre_selo/gerar_pino_recibo_pre_selo_v412.py (o corpo: as tres fotografias, o recibo desta rodada, a saida != 0
# se o pino nao for utilizavel ou a producao nao estiver intacta), derivado para o SALTO (pendencia 1.1): aceita SO' o veredito EXATO do salto, REPINADA_B<GER+1>__SALTO_v411_v412__ENSAIO__NADA_GRAVADO_NA_BANCADA,
# com GER lido da producao (manifesto_anterior do recibo); o glob e' o da v412 (o Nos do pre-selo); os pinos sao os da v413 (bateria da v412, cadeia v411 -> v412); o pino ganha o sha da cadeia e o bloco salto.
"""gerar_pino_recibo_pre_selo_v413.py -- gera PINO_RECIBO_PRE_SELO_v413.json e PROVA_PRODUCAO_INTACTA_v413_pre_selo.json (em v413\\) a partir do recibo do ensaio do salto, do stdout, do lancador, dos pinos
(esboco, bateria da v412, cadeia), da conferencia pelo esboco (conferencia_pelo_esboco_v413.json) e das fotografias da producao (antes / depois / final). TUDO LIDO dos arquivos, por script.
Nao grava na Bancada, no Nos nem no tunel: escreve so' os dois JSON em v413\\ e copia as listas para v413\\bateria_pre_selo\\prova_producao\\.
Sai 1 se o pino nao for utilizavel ou se a producao nao estiver intacta (os dois JSON ficam gravados como registro). uso: python -I -B -X utf8 gerar_pino_recibo_pre_selo_v413.py <pasta das fotografias>"""
import sys

sys.dont_write_bytecode = True
import datetime
import glob
import gzip
import hashlib
import json
import os
import re
import shutil
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import delta_bn_v413 as DBN  # noqa: E402
import util_bn_v413 as U  # noqa: E402

SP = os.path.abspath(sys.argv[1])
OUTB = DBN.OUTB_PRE_SELO
os.makedirs(OUTB, exist_ok=True)
DEST_PROVA = os.path.join(OUTB, "prova_producao")
sha = U.sha256_arquivo
lj = U.ler_json

# ---- o recibo, o stdout, o lancador, os pinos
rps = glob.glob(os.path.join(OUTB, "ensaio_1", "RECIBO_SINCRONIZACAO_%s_*.json" % DBN.VERSAO_DO_PRE_SELO))
assert len(rps) == 1, rps
REC = rps[0]
raw = open(REC, "rb").read()
RSHA = hashlib.sha256(raw).hexdigest()
r = json.loads(raw.decode("utf-8"))
STDOUT = os.path.join(OUTB, "etapa1_stdout.txt")
LANC = os.path.join(HERE, "rodar_ensaio_1_pre_selo_v413.sh")
pbn = lj(DBN.PINOS_BN_V411_ARQ)
pbat = lj(os.path.join(DBN.BATERIA_V412_DIR, "PINOS_BATERIA_v412.json"))
pcad = lj(DBN.PINO_CADEIA_ARQ)
ESB, ESB_SHA = pbn["esboco_R3_6"]["path"], pbn["esboco_R3_6"]["sha256"]
BAT, BAT_SHA = pbat["bateria"]["path"], pbat["bateria"]["sha256"]
CAD, CAD_SHA = pcad["cadeia"]["path"], pcad["cadeia"]["sha256"]
assert sha(ESB) == ESB_SHA and sha(BAT) == BAT_SHA and sha(CAD) == CAD_SHA, "esboco, bateria ou cadeia em disco diferem dos pinos"
assert r["script_sha256"] == ESB_SHA and r["bateria"]["sha256"] == BAT_SHA and (r.get("cadeia_de_selos") or {}).get("sha256") == CAD_SHA, "o recibo nao foi gerado com o esboco, a bateria e a cadeia pinados"
linhas = open(STDOUT, encoding="utf-8").read().splitlines()
imp = json.loads([l for l in linhas if l.strip().startswith("{")][-1])
RC = int([l for l in linhas if l.startswith("ETAPA1_RC=")][-1].split("=", 1)[1])
assert imp["recibo_sha256"] == RSHA and os.path.samefile(imp["recibo"], REC), "o stdout nao cita este recibo"
conf_p = os.path.join(OUTB, "conferencia_pelo_esboco_v413.json")
conf = lj(conf_p)
assert conf["recibo"]["sha256"] == RSHA and conf["esboco"]["sha256"] == ESB_SHA and conf["cadeia"]["sha256"] == CAD_SHA, "a conferencia e' de outro recibo, esboco ou cadeia"

bat = r["bateria_resultado"]
testes = {t["id"]: t for t in bat["testes"]}
t12 = lj(os.path.join(OUTB, "ensaio_1", "recibos", "T12_T13_T14_ATRATOR.json"))
sub = {k: ("PASSA" if v.get("passa") else "FALHA") for k, v in t12["runs"].items()}
mant = r["manifesto_anterior"]
_g = re.match(r"^B(\d+)-", str(mant.get("deployment_id") or ""))
GER = int(_g.group(1)) if _g else None
VEREDITO_EXATO = ("REPINADA_B%d__SALTO_%s_%s__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (GER + 1, DBN.BANCADA_ANTERIOR, DBN.VERSAO_DO_PRE_SELO)) if GER is not None else None

# ---- o comando exato: o argv REAL registrado no recibo (sys.orig_argv), com o executavel escrito como `python`
argv = list(r["python_isolado"]["orig_argv"])
cmd = "python " + " ".join(('"%s"' % a) if (("\\" in a) or (" " in a)) else a for a in argv[1:])

ROT = ("antes", "depois", "final")


def sha_lista(lista):
    h = hashlib.sha256()
    for rel, t, s, m in lista:
        h.update(("%s\t%s\t%d\t%d\n" % (rel, t, s, m)).encode("utf-8"))
    return h.hexdigest()


def carregar(rot):
    ch = lj(os.path.join(SP, "chaves_%s.json" % rot))
    ban = lj(os.path.join(SP, "fp_bancada_%s.json" % rot))
    nos = json.loads(gzip.decompress(open(os.path.join(SP, "fp_nos_%s.json.gz" % rot), "rb").read()).decode("utf-8"))
    assert sha_lista(ban) == ch["bancada"]["sha256_da_lista"], "lista da Bancada (%s) nao bate com o resumo" % rot
    assert sha_lista(nos) == ch["nos"]["sha256_da_lista"], "lista do Nos (%s) nao bate com o resumo" % rot
    return ch, ban, nos


snaps = {rot: carregar(rot) for rot in ROT}


def difere(a, b):
    da = {x[0]: tuple(x[1:]) for x in a}
    db = {x[0]: tuple(x[1:]) for x in b}
    add, rem = sorted(set(db) - set(da)), sorted(set(da) - set(db))
    alt = sorted(k for k in set(da) & set(db) if da[k] != db[k])
    return {"adicionados": add[:50], "removidos": rem[:50], "alterados": alt[:50], "n_adicionados": len(add), "n_removidos": len(rem), "n_alterados": len(alt)}


def bloco(nome):
    out = {"raiz": snaps["antes"][0][nome]["raiz"], "fotografias": {}}
    for rot in ROT:
        ch = snaps[rot][0]
        out["fotografias"][rot] = {"quando": ch["quando"], "n_entradas": ch[nome]["n_entradas"], "n_arquivos": ch[nome]["n_arquivos"], "n_pastas": ch[nome]["n_pastas"],
                                   "bytes_arquivos": ch[nome]["bytes_arquivos"], "sha256_da_lista": ch[nome]["sha256_da_lista"], "erros_de_leitura": len(ch[nome]["erros_de_leitura"])}
    idx = 1 if nome == "bancada" else 2
    d1 = difere(snaps["antes"][idx], snaps["depois"][idx])
    d2 = difere(snaps["antes"][idx], snaps["final"][idx])
    out["diferencas_antes_depois"] = d1
    out["diferencas_antes_final"] = d2
    out["lista_identica_antes_depois_final"] = (d1["n_adicionados"] + d1["n_removidos"] + d1["n_alterados"] + d2["n_adicionados"] + d2["n_removidos"] + d2["n_alterados"] == 0
                                               and len({snaps[rot][0][nome]["sha256_da_lista"] for rot in ROT}) == 1)
    return out


b_ban, b_nos = bloco("bancada"), bloco("nos")
chaves = []
for i, c in enumerate(snaps["antes"][0]["chaves"]):
    iguais = all(snaps[rot][0]["chaves"][i]["sha256"] == c["sha256"] and snaps[rot][0]["chaves"][i]["bytes"] == c["bytes"] for rot in ROT)
    chaves.append({"dono": c["dono"], "arquivo": c["arquivo"], "path": c["path"], "bytes": c["bytes"], "sha256_antes": c["sha256"],
                   "sha256_depois": snaps["depois"][0]["chaves"][i]["sha256"], "sha256_final": snaps["final"][0]["chaves"][i]["sha256"], "igual_nas_tres": iguais})
n_pyc = {rot: sum(1 for x in snaps[rot][1] if "__pycache__" in x[0] or x[0].endswith(".pyc")) for rot in ROT}
tudo_igual = b_ban["lista_identica_antes_depois_final"] and b_nos["lista_identica_antes_depois_final"] and all(c["igual_nas_tres"] for c in chaves)
# o recibo e' DESTA rodada: o inicio_utc dele cai entre a fotografia "antes" e a "depois" (as fotos tem resolucao de segundo: o inicio e' truncado ao segundo)
try:
    _ini = datetime.datetime.fromisoformat(r["inicio_utc"]).replace(microsecond=0)
    _f_antes, _f_depois = (datetime.datetime.strptime(snaps[rot_][0]["quando"], "%Y-%m-%dT%H:%M:%S%z") for rot_ in ("antes", "depois"))
    recibo_entre_as_fotos = bool(_f_antes <= _ini <= _f_depois)
    instantes_da_rodada = {"foto_antes": snaps["antes"][0]["quando"], "inicio_utc_do_recibo": r["inicio_utc"], "foto_depois": snaps["depois"][0]["quando"]}
except Exception as e_:   # noqa: BLE001   (instante ilegivel = nao se prova que o recibo e' desta rodada)
    recibo_entre_as_fotos, instantes_da_rodada = False, {"excecao": repr(e_)}

os.makedirs(DEST_PROVA, exist_ok=True)
copiados = []
for rot in ROT:
    for nome in ("chaves_%s.json" % rot, "fp_bancada_%s.json" % rot) + (("fp_nos_antes.json.gz",) if rot == "antes" else ()):
        src, dst = os.path.join(SP, nome), os.path.join(DEST_PROVA, nome)
        if os.path.exists(dst):
            assert open(src, "rb").read() == open(dst, "rb").read(), "ja existe e difere: " + dst
        else:
            shutil.copyfile(src, dst)
        assert sha(src) == sha(dst)
        copiados.append({"path": dst, "bytes": os.path.getsize(dst), "sha256": sha(dst)})

prova = {
    "contrato": "PROVA_PRODUCAO_INTACTA_v413_pre_selo",
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "o_que_se_prova": ("o ensaio pre_selo do SALTO da v413 (esboco R3.6, --modo ensaio, --versao v412, bateria da v412, cadeia v411 -> v412) so' LEU a Bancada de producao e o Nos: a lista (caminho, tipo, "
                       "tamanho, mtime_ns) de toda a arvore de cada um, o sha256 do manifesto canonico da Bancada e o do um.py do Nos (e do selo, do core e do manifesto do kernel) sao os mesmos antes do ensaio, "
                       "logo depois e depois da conferencia do recibo"),
    "ensaio": {"recibo": REC, "recibo_sha256": RSHA, "inicio_utc": r["inicio_utc"], "fim_utc": r["fim_utc"], "modo": r["modo"], "fase": r["fase"], "veredito": r["veredito"],
               "inicio_entre_as_fotos_antes_e_depois": recibo_entre_as_fotos, "instantes_da_rodada": instantes_da_rodada,
               "lancador": LANC, "lancador_sha256": sha(LANC), "script_de_fotografia": {"path": os.path.join(HERE, "snap_producao_v413.py"), "sha256": sha(os.path.join(HERE, "snap_producao_v413.py"))}},
    "producao_intacta": tudo_igual,
    "manifesto_canonico_da_bancada": next(c for c in chaves if c["arquivo"] == "canonical_contracts.json"),
    "um_py_do_nos": next(c for c in chaves if c["arquivo"] == "um.py"),
    "chaves": chaves, "bancada_de_producao": b_ban, "nos": b_nos, "arquivos_pyc_ou_pycache_na_bancada": n_pyc,
    "servico_da_bancada": {"porta_no_ar_ao_gerar_esta_prova": U.porta_aberta(DBN.PORTA),
                           "nota": "observacao por conexao TCP; esta tarefa nao parou nem religou o servico (nenhum comando de processo foi emitido)"},
    "copias_das_listas": copiados,
    "esta_tarefa_escreveu_so_em": [OUTB + " (ensaio_1, stdout, conferencia, prova_producao)", DBN.PINO_RECIBO_PRE_SELO_ARQ, DBN.PROVA_PRODUCAO_ARQ,
                                   DBN.SANDBOX_CURTO + " (sandbox curto, apagado no fim por limpar_sandbox_vb24.py)",
                                   "depois deste script, os passos 8 e 9 do rodar_bn_pre_selo_v413.sh regravam %s (diff_e_pinos_bn_v413.py) e %s (p00_precondicoes_bn_v413.py), com backup de bytes"
                                   % (DBN.PINOS_BN_ARQ, DBN.PRECONDICOES_BN_ARQ)],
    "escopo": "so leitura da producao; nada gravado na Bancada nem no Nos; NOT_FALSIFIED nao e' creditacao; o gate nao se move",
}

pv = r["bateria"].get("pinos_da_versao") or {}
adendo = (t12.get("adendo_de_pino") or {}).get("entrada_do_um_py")
salto_conf = (conf.get("resultado_do_esboco") or {}).get("salto")
motivos = list(conf["motivos_de_nao_ser_utilizavel"])
if not tudo_igual:
    motivos.append("a producao NAO esta intacta: ver PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")
if not recibo_entre_as_fotos:
    motivos.append("o inicio_utc do recibo NAO cai entre as fotografias antes e depois: nao se prova que o recibo e' desta rodada (%s)" % json.dumps(instantes_da_rodada, ensure_ascii=False))
if VEREDITO_EXATO is None or r["veredito"] != VEREDITO_EXATO or VEREDITO_EXATO != DBN.VEREDITO_PRE_SELO:
    motivos.append("o veredito do recibo (%r) nao e' EXATAMENTE o do salto com a geracao lida da producao (%r; o delta_bn espera %r) (pendencia 1.1)" % (r["veredito"], VEREDITO_EXATO, DBN.VEREDITO_PRE_SELO))
if json.dumps(r.get("salto"), sort_keys=True) != json.dumps(salto_conf, sort_keys=True) or (r.get("salto") or {}).get("cadeia", {}).get("sha256") != CAD_SHA:
    motivos.append("o bloco salto do recibo nao e' o que a conferencia pelo esboco devolveu, ou nao cita a cadeia pinada")
utilizavel = bool(conf["utilizavel_como_recibo_pre_selo_do_B_n"] and conf["esboco_aceita"] and conf["n_controles_como_esperado"] == len(conf["controles_negativos"])
                  and conf["n_condicoes_ok"] == conf["n_condicoes"] and bat["veredito"] == "BATERIA_PASSA" and VEREDITO_EXATO is not None and r["veredito"] == VEREDITO_EXATO == DBN.VEREDITO_PRE_SELO
                  and RC == 0 and tudo_igual and recibo_entre_as_fotos and not motivos)
pino = dict(
    contrato="PINO_RECIBO_PRE_SELO_v413_SALTO_ENSAIO",
    quando=r.get("inicio_utc"),
    path=REC, sha256=RSHA, bytes=len(raw),
    versao_nos=r["nos"]["UM_VERSION"],
    um_py_sha16_do_nos=r["nos"]["um_py"]["sha256"][:16],
    bancada_pina=dict(version=mant["version"], deployment_id=mant["deployment_id"], um_py_sha16=mant["um_py_pinado"][:16], estado_do_contrato_instalado=mant["estado_do_contrato_instalado"]),
    comando_exato=cmd, lancador=LANC, lancador_sha256=sha(LANC), stdout=dict(path=STDOUT, sha256=sha(STDOUT)),
    esboco=dict(path=ESB, sha256=sha(ESB)),
    bateria=dict(path=BAT, sha256=sha(BAT), versao=r["bateria"].get("versao")),
    cadeia_de_selos=dict(path=CAD, sha256=sha(CAD), bytes=os.path.getsize(CAD), pino=U.pinar(DBN.PINO_CADEIA_ARQ)),
    salto=r.get("salto"),
    veredito=r["veredito"], veredito_exigido=VEREDITO_EXATO, codigo_de_saida=RC,
    contagens=dict(n=bat["n"], passa=bat["passa"], falha=bat["falha"], nao_executado=bat["nao_executado"], veredito_bateria=bat["veredito"]),
    por_teste={k: testes[k]["resultado"] for k in testes},
    t12_t13_t14_por_corrida=sub, adendo_de_pino_do_t12=adendo,
    pinos_da_versao={k: pv.get(k) for k in ("declarados", "conferidos_contra_o_nos_lido", "versao", "um_py_sha256", "um_py_bytes", "selo_sha256", "testes_que_pinam_o_um_py")},
    utilizavel_como_recibo_pre_selo_do_B_n=utilizavel, motivos_de_nao_ser_utilizavel=motivos,
    recibo_desta_rodada=dict(inicio_entre_as_fotos_antes_e_depois=recibo_entre_as_fotos, instantes=instantes_da_rodada),
    conferido_por=dict(script=os.path.join(HERE, "conferir_recibo_pre_selo_salto_v413.py"), script_sha256=conf["script"]["sha256"], resultado_em=conf_p, resultado_sha256=sha(conf_p),
                       funcao="conferir_recibo_pre_selo do esboco R3.6 (ja_sincronizada=False; COM a cadeia v411 -> v412; selo e manifesto do kernel anteriores = v413/base_v412)",
                       esboco_aceita=conf["esboco_aceita"], condicoes="%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]),
                       controles_negativos="%d/%d recusados como esperado" % (conf["n_controles_como_esperado"], len(conf["controles_negativos"]))),
    valido_enquanto=dict(bancada_pina=dict(deployment_id=mant["deployment_id"], version=mant["version"], manifesto_sha256=mant["sha256"], um_py_sha256=mant["um_py_pinado"], seal_sha256=mant["seal_sha_pinado"]),
                         nota="um re-pino da producao antes do B(n) da v413 torna o recibo obsoleto (o salto embute o sha do manifesto e o deployment_id); o recibo so' serve ao pos-selo da v413"),
    nao_executados=dict(T17_LEAN_KERNEL=testes["T17_LEAN_KERNEL"]["detalhe"]) if "T17_LEAN_KERNEL" in testes else {},
    limites=[
        "T12/T13/T14 so' rodam no pre_selo (fases=['pre_selo'] na bateria): no B(n) da v413 valem por ESTE recibo, medidos contra o um.py que o ensaio leu no Nos (o da v412), nao contra o um.py da v413",
        "o T17 e o nos_pinado do pos_selo so' se decidem com o selo, o manifesto do kernel e o recibo do kernel REAIS da v413 [DECLARADO: RESULTADO_R3_6.md]",
        "o salto depende dos backups de 18/11 no Nos e do registro v412\\APLICADO_AO_CANONICO_20261118_235146.json ate' o fechamento do B21 (N3)",
    ],
    escrita_na_producao=dict(
        bancada_um=dict(antes=b_ban["fotografias"]["antes"]["n_entradas"], depois=b_ban["fotografias"]["final"]["n_entradas"], identico=b_ban["lista_identica_antes_depois_final"],
                        sha256_da_lista=b_ban["fotografias"]["final"]["sha256_da_lista"]),
        nos=dict(antes=b_nos["fotografias"]["antes"]["n_entradas"], depois=b_nos["fotografias"]["final"]["n_entradas"], identico=b_nos["lista_identica_antes_depois_final"],
                 sha256_da_lista=b_nos["fotografias"]["final"]["sha256_da_lista"]),
        criterio="lista (caminho, tipo, tamanho, mtime_ns) de toda a arvore, antes do ensaio, logo depois e depois da conferencia do recibo; prova completa em PROVA_PRODUCAO_INTACTA_v413_pre_selo.json"),
    escopo="identidade e testes sinteticos; nenhum dado observado; NOT_FALSIFIED nao e' creditacao; o gate nao se move",
)
d_prova = U.gravar_json_novo(DBN.PROVA_PRODUCAO_ARQ, prova)
d_pino = U.gravar_json_novo(DBN.PINO_RECIBO_PRE_SELO_ARQ, pino)
print(d_pino, sha(d_pino))
print(d_prova, sha(d_prova))
print(json.dumps(pino["contagens"]), pino["veredito"], "utilizavel=%s" % utilizavel, "producao_intacta=%s" % tudo_igual, "recibo_desta_rodada=%s" % recibo_entre_as_fotos)
sys.exit(0 if (utilizavel is True and prova["producao_intacta"] is True) else 1)

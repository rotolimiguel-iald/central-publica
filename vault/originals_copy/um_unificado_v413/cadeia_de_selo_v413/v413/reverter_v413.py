# -*- coding: utf-8 -*-
"""reverter_v413.py -- REVERSAO da instalacao v413 (ATO DA GERENCIA c1; usar so' se o rito falhar ou o conferidor nao bater; preparado na Etapa 3
da v413, 20/11/2026, NAO executado no Nos). Molde: v412\\reverter_v412.py, com o CASO NOVO da v413 (o modulo corrigido volta ao sha antigo).
Le o ULTIMO APLICADO_AO_CANONICO_*.json (o carimbo dos backups; nada digitado) e, ANTES de qualquer escrita, confere: todos os backups existem e
batem com o registro; os do conjunto selado batem com o sha256 do selo da v412; o backup do corrigido tem o sha256 antigo; a lista dos novos e' a
do ESPERADOS. So' entao: guarda o estado falho como registro (tentativa_v413_rito_falhou_<ts>), restaura TODOS os backups de BYTES (o conjunto
pinado pelo selo da v412, o selo, o sidecar, os textos declarados pt/en .txt, a raiz, o Audit e o modulo corrigido) por temporario + troca
atomica, e move os modulos NOVOS que o rito materializou para a QUARENTENA (quarentena_bundle_<ts>). Confere ao fim: o um.py voltou a ser a
v412 selada (o sha16 tambem LIDO de v412\\ESPERADOS_v412.json), o corrigido tem o sha256 antigo, a raiz e o Audit sao os da v412, e todo arquivo
pinado pelo selo restaurado bate com ele. NAO restaura (como o molde): os .aux/.log/.toc/.out, as capturas do kernel e o .lake, que o rito
reescreve e a proxima rodada regenera. Recusa -O e o modo de ensaio do topo, como o instalador. Saida 0 so' se tudo bater.
ENSAIO: V413_ENSAIO_DIR=<pasta>, como no instalador (o Nos e' <pasta>\\Nos; o registro e' <pasta>\\registro)."""
import datetime, glob, hashlib, json, os, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
if os.environ.get("V413_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: o MODO DE ENSAIO do topo proposto nao instala nem reverte nada")
CAD = os.path.dirname(os.path.abspath(__file__))
NOS_REAL = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
ENSAIO = os.environ.get("V413_ENSAIO_DIR")
if ENSAIO:
    W = os.path.abspath(ENSAIO); assert os.path.isdir(W) and not os.path.normcase(W).startswith(os.path.normcase(NOS_REAL)), "pasta de ensaio invalida"
    NOS, REG, E2 = os.path.join(W, "Nós"), os.path.join(W, "registro"), W
else:
    NOS, REG, E2 = NOS_REAL, CAD, CAD
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ap_p = sorted(glob.glob(os.path.join(REG, "APLICADO_AO_CANONICO_*.json")))   # (so' os desta pasta: o da v412, insumo do salto do B(n), mora em v412\ e nao entra)
assert ap_p, "nenhum APLICADO_AO_CANONICO_*.json desta versao: nada instalado por instalar_v413.py"
AP = json.load(open(ap_p[-1], encoding="utf-8")); TS = AP["ts"]
assert bool(AP.get("ensaio")) == bool(ENSAIO), "o registro da instalacao e' de outro modo (ensaio/real)"
T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# --- tudo o que decide a reversao e' LIDO ANTES de qualquer escrita
esp = json.load(open(os.path.join(E2, "ESPERADOS_v413.json"), encoding="utf-8"))
assert esp.get("gerador") == "esperados_v413_foco.py" and AP.get("esperados_sha16") == hashlib.sha256(open(os.path.join(E2, "ESPERADOS_v413.json"), "rb").read()).hexdigest()[:16], "o ESPERADOS mudou depois da instalacao"
_aplic = AP.get("modulos_novos_v413") or {}
_lista = list(_aplic.get("lista") or [])
assert _lista and len(_lista) == len(set(_lista)) == esp["kernel"]["modulos_novos"] and set(_lista) == set(esp["bundle_sha256"]) and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in _lista), ("a lista dos modulos novos do registro nao e' a do ESPERADOS", len(_lista))
try:
    ANCORA = json.load(open(os.path.join(os.path.dirname(CAD), "v412", "ESPERADOS_v412.json"), encoding="utf-8"))["candidato_sha16"]   # o sha16 do um.py da v412 selada, do pacote anterior
except (OSError, ValueError, KeyError):
    ANCORA = None
alvos = list(AP["backups"].keys())
selados = list((AP.get("selo_v412_pina") or {}).get("arquivos") or [])
kc_rel = {os.path.join("tgl_kernel", *r.split("/")): r for r in (AP.get("kernel_corrigido") or {})}
assert selados and set(selados) <= set(alvos) and set(kc_rel) <= set(alvos) and set(kc_rel.values()) == set(esp["kernel_corrigido"]), "o registro nao traz o conjunto selado ou o corrigido"
for x_ in ("um_absoluto_selo.json", "um_absoluto_selo_acom.json", os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):
    assert x_ in alvos, ("o registro nao guardou", x_)
for a in alvos:   # fail-closed: todos os backups existem e batem com o que o instalador gravou, ANTES de qualquer escrita
    b = AP["backups"][a]["backup"]; assert os.path.exists(b) and sh(b) == AP["backups"][a]["sha256"], ("backup ausente ou alterado", b)
selo_bak = json.load(open(AP["backups"]["um_absoluto_selo.json"]["backup"], encoding="utf-8"))
assert selo_bak.get("um_version") == "v412" and sorted(selo_bak["sha256"]) == sorted(selados), "o backup do selo nao e' o da v412 ou nao pina o conjunto guardado"
for a in selados:
    assert AP["backups"][a]["sha256"] == selo_bak["sha256"][a], ("o backup de um arquivo selado nao tem o sha256 do selo da v412", a)
for kr, rel in kc_rel.items():
    assert AP["backups"][kr]["sha256"] == esp["kernel_corrigido"][rel]["sha256_antes"] == AP["kernel_corrigido"][rel]["sha256_antes"], ("o backup do corrigido nao tem o sha antigo", rel)
rec = {"ts": T2, "ensaio": bool(ENSAIO), "backups": TS, "aplicado": os.path.basename(ap_p[-1]), "guardado": [], "restaurado": [], "quarentena": []}
reg = os.path.join(REG, "tentativa_v413_rito_falhou_" + T2); os.makedirs(reg)
for a in alvos + ["rodada_v413_stdout.txt"] + [os.path.join("tgl_kernel", *n.split("/")) for n in _lista]:
    p = os.path.join(NOS, a)
    if os.path.isfile(p):
        d = os.path.join(reg, a.replace(os.sep, "__").replace("/", "__")); shutil.copyfile(p, d)
        rec["guardado"].append({"arquivo": a, "sha16": sh(d)[:16], "bytes": os.path.getsize(d)})
for a in alvos:
    p = os.path.join(NOS, a); b = AP["backups"][a]["backup"]
    data = open(b, "rb").read(); tmp = p + ".tmp_reverter_v413"
    open(tmp, "wb").write(data)
    assert os.path.getsize(tmp) == len(data) and sh(tmp) == hashlib.sha256(data).hexdigest()
    os.replace(tmp, p)
    rec["restaurado"].append({"arquivo": a, "sha16": sh(p)[:16]})
qd = os.path.join(REG, "quarentena_bundle_" + T2); os.makedirs(qd)
rec["quarentena_fonte"] = "APLICADO_AO_CANONICO.modulos_novos_v413.lista (%d)" % len(_lista)
for nome in _lista:   # os modulos novos que o rito materializou vao a quarentena (molde v410/v412)
    p = os.path.join(NOS, "tgl_kernel", *nome.split("/"))
    if os.path.isfile(p):
        d_ = os.path.join(qd, *nome.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True)
        shutil.move(p, d_); rec["quarentena"].append(nome)
umsha = sh(os.path.join(NOS, "um.py"))[:16]
rec["um_py_sha16"] = umsha
rec["ancora_v412"] = {"fonte": "v412/ESPERADOS_v412.json[candidato_sha16]", "sha16": ANCORA}
sel_ok = all(sh(os.path.join(NOS, a)) == selo_bak["sha256"][a] for a in selados)
kc_ok = all(sh(os.path.join(NOS, kr)) == esp["kernel_corrigido"][rel]["sha256_antes"] for kr, rel in kc_rel.items())
ra_ok = sh(os.path.join(NOS, "tgl_kernel", "TGLExt.lean")) == esp["kernel"]["raiz_antes_sha256"] and sh(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean")) == esp["kernel"]["audit_antes_sha256"]
novos_fora = not [n for n in _lista if os.path.exists(os.path.join(NOS, "tgl_kernel", *n.split("/")))]
rec.update({"conjunto_selado_bate_com_o_selo_v412": sel_ok, "corrigido_com_o_sha_antigo": kc_ok, "raiz_e_audit_da_v412": ra_ok, "novos_fora_do_kernel": novos_fora})
rec["ok"] = bool(umsha == esp["origem_sha16"] and (ANCORA is None or umsha == ANCORA) and sel_ok and kc_ok and ra_ok and novos_fora)
rec["nao_restaura"] = "os .aux/.log/.toc/.out, as capturas do kernel (tgl_kernel_*capture*.txt) e o .lake do kernel: o rito os reescreve e a proxima rodada os regenera"
out = os.path.join(REG, "RECIBO_REVERSAO_v413_" + T2 + ".json")
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ok": rec["ok"], "ensaio": bool(ENSAIO), "um_py": umsha, "restaurados": len(rec["restaurado"]), "quarentena": len(rec["quarentena"]), "conjunto_selado": sel_ok,
                  "corrigido": kc_ok, "raiz_audit": ra_ok, "registro": reg, "recibo": out}, ensure_ascii=False))
sys.exit(0 if rec["ok"] else 1)

# -*- coding: utf-8 -*-
"""instalar_v413.py -- instala o candidato v413 no canonico (ATO DA GERENCIA c1; preparado na Etapa 3 da v413, 20/11/2026, NAO executado).
Molde: v412\\instalar_v412.py (o corpo e as travas) com o CASO NOVO da v413: um modulo que EXISTE no Nos e e' SUBSTITUIDO (o corrigido,
TGLExt/OResumoEPsiBit.lean, so' a docstring): o instalador confere o sha antigo, guarda os bytes, e a reversao (reverter_v413.py) o devolve.
Fail-closed (para na primeira falha, ANTES de qualquer escrita no Nos):
  * recusa -O e o MODO DE ENSAIO do topo proposto; exige o topo DERIVADO da Etapa 2 (TOPO_RATIFICADO_v413_DERIVADO.json);
  * ESPERADOS_v413.json (esperados_v413_foco.py) e CANDIDATO_v413.json concordam; nenhum processo um.py nem trabalhador do pilar rodando;
  * o um.py do Nos e' a v412 selada (ESPERADOS.origem_sha16); o candidato tem o sha16 e os bytes do ESPERADOS; o cache do pilar guarda o resultado;
  * as exigencias da custodia estao no candidato (o par _V413_FONTES/_V413_VERBATINS2 e o nome kh_n1_cobertura_v413; ESPERADOS.exigencias_da_custodia);
  * o PRE-SELO do B(n) (o salto v411 -> v413) rodou com o Nos ainda na v412: PINO_RECIBO_PRE_SELO_v413.json utilizavel e do um.py que esta' no Nos;
    sem ele, so' com --sem-pre-selo-bn "<motivo>" (DESVIO DECLARADO, gravado no registro: o salto se perde e o B(n) da v413 vira decisao do operador);
  * as pedras anteriores: TODO arquivo do manifesto do kernel pinado pelo selo da v412 (tgl_kernel_proof_manifest.json, formal_files_sha256) esta'
    no kernel do Nos com o sha256 pinado (os 156 da v412, o fecho da v406 e o resto; nenhum nome digitado);
  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos sao os da v412 (ESPERADOS.kernel.*_antes_sha256; o rito os reescreve);
  * os modulos NOVOS (ESPERADOS.bundle_sha256 == kernel_modulos_novos_v413.json[novos]) NAO estao no kernel do Nos;
  * o modulo CORRIGIDO esta' no Nos com o sha256 ANTIGO (ESPERADOS.kernel_corrigido[rel].sha256_antes);
  * BACKUP DE BYTES de: todo arquivo pinado pelo selo da v412 (selo.sha256: o um.py, o core, os .tex, os .pdf, as figuras, o manifesto do kernel,
    o pilar, a forma canonica, o manifesto), o selo, o sidecar um_absoluto_selo_acom.json, os textos declarados um_absoluto_pt.txt e
    um_absoluto_en.txt, tgl_kernel/TGLExt.lean, tgl_kernel/TGL/Audit.lean e o modulo corrigido; cada backup do conjunto selado tem o sha256 do selo;
    a copia do cache do pilar; so' entao troca o um.py (temporario + troca atomica).
Grava APLICADO_AO_CANONICO_<ts>.json (a reversao le a lista dos novos, os backups e o corrigido dele).
ENSAIO (so' para os testes desta etapa): V413_ENSAIO_DIR=<pasta> troca o Nos por <pasta>\\Nos, le os insumos da Etapa 2 e o ESPERADOS de <pasta> e
grava o registro em <pasta>\\registro. Uso: instalar_v413.py [--sem-pre-selo-bn "<motivo>"]"""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
if os.environ.get("V413_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: o MODO DE ENSAIO do topo proposto nao instala nada (o artefato de ensaio NAO e' candidato)")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS_REAL = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ENSAIO = os.environ.get("V413_ENSAIO_DIR")
if ENSAIO:
    W = os.path.abspath(ENSAIO)
    assert os.path.isdir(W) and os.path.normcase(W) != os.path.normcase(HERE) and not os.path.normcase(W).startswith(os.path.normcase(NOS_REAL)), "pasta de ensaio invalida"
    NOS, REG, E2 = os.path.join(W, "Nós"), os.path.join(W, "registro"), W
    os.makedirs(REG, exist_ok=True)
else:
    NOS, REG, E2 = NOS_REAL, HERE, HERE
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
h256 = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read()
SEM_PRE = None
if "--sem-pre-selo-bn" in sys.argv:
    i_ = sys.argv.index("--sem-pre-selo-bn"); SEM_PRE = (sys.argv[i_ + 1] if i_ + 1 < len(sys.argv) else "").strip()
    assert len(SEM_PRE) >= 20, "--sem-pre-selo-bn exige o MOTIVO por extenso (o desvio fica gravado no registro)"
ESP = json.load(open(os.path.join(E2, "ESPERADOS_v413.json"), encoding="utf-8")); CM = json.load(open(os.path.join(E2, "CANDIDATO_v413.json"), encoding="utf-8"))
assert ESP.get("gerador") == "esperados_v413_foco.py" and bool(ESP.get("ensaio")) == bool(ENSAIO), "o ESPERADOS nao e' do esperados_v413_foco.py ou o modo (ensaio/real) difere"
assert not ESP.get("ensaio_topo_proposto") and not CM.get("ensaio_topo_proposto"), "o ESPERADOS ou o CANDIDATO sao do ENSAIO do topo proposto -- nao instalo"
assert os.path.exists(os.path.join(E2, "TOPO_RATIFICADO_v413_DERIVADO.json")), "falta TOPO_RATIFICADO_v413_DERIVADO.json (o topo derivado da Etapa 2): sem ele nao ha candidato -- nao instalo"
CAND = ESP["candidato"]["caminho"]
# --- trava de processo: nenhum um.py nem trabalhador do pilar vivo
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
# --- trava de origem e de candidato
um = os.path.join(NOS, "um.py"); raw0 = rb(um)
assert h16(raw0) == ESP["origem_sha16"], "o canonico nao e' a v412 selada (%s)" % h16(raw0)
cand = rb(CAND); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"] == int(CM["bytes"]), "o candidato do disco nao e' o do ESPERADOS/CANDIDATO"
assert (ESP.get("exigencias_da_custodia") or {}).get("todas") is True, ("o candidato nao traz as exigencias da custodia (o par _V413_FONTES/_V413_VERBATINS2 e kh_n1_cobertura_v413): a custodia PARA sem elas -- corrigir o candidato antes do rito", ESP.get("exigencias_da_custodia"))
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v412" and selo0["sha256"]["um.py"] == h256(raw0) and h256(rb(os.path.join(NOS, "um_absoluto_selo.json"))) == ESP["base_v412"]["selo_sha256"], "o selo do Nos nao e' o da v412 do ESPERADOS"
# --- o pre-selo do B(n) (o salto): antes da instalacao, com o Nos ainda na v412
pino_p = os.path.join(E2, "PINO_RECIBO_PRE_SELO_v413.json"); pre = {"path": pino_p}
if os.path.isfile(pino_p):
    pp = json.load(open(pino_p, encoding="utf-8"))
    pre.update({"sha256": h256(rb(pino_p)), "contrato": pp.get("contrato"), "utilizavel": pp.get("utilizavel_como_recibo_pre_selo_do_B_n"), "versao_nos": pp.get("versao_nos"),
                "um_py_sha16_do_nos": pp.get("um_py_sha16_do_nos"), "veredito": pp.get("veredito")})
    pre["ok"] = bool(pre["contrato"] == "PINO_RECIBO_PRE_SELO_v413_SALTO_ENSAIO" and pre["utilizavel"] is True and pre["versao_nos"] == "v412" and pre["um_py_sha16_do_nos"] == ESP["origem_sha16"])
else:
    pre["ok"] = False
if not pre["ok"]:
    assert SEM_PRE, ("o pre-selo do B(n) da v413 nao esta' utilizavel (%s): rode bancada\\rodar_bn_pre_selo_v413.sh com o Nos ainda na v412, ou passe --sem-pre-selo-bn \"<motivo>\" "
                     "(DESVIO DECLARADO: o salto se perde e o B(n) da v413 vira decisao do operador)" % pre)
    pre["desvio_declarado"] = {"motivo": SEM_PRE, "efeito": "instalado sem o pre-selo do salto; o B(n) da v413 so' com decisao do operador (BN_DISPENSADO_v413) ou num B(n) futuro"}
# --- o pilar: o cache guarda o resultado reaproveitado
_cdir = ESP["pilar"]["cache_dir"]
assert h256(rb(os.path.join(_cdir, "result.json"))) == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# --- as pedras anteriores: o manifesto do kernel pinado pelo selo da v412, arquivo por arquivo
manp = os.path.join(NOS, "tgl_kernel_proof_manifest.json"); assert h256(rb(manp)) == selo0["sha256"]["tgl_kernel_proof_manifest.json"], "o manifesto do kernel do Nos nao e' o pinado pelo selo"
fmap = json.load(open(manp, encoding="utf-8"))["formal_files_sha256"]
mal = [n for n, h in fmap.items() if not os.path.isfile(os.path.join(NOS, "tgl_kernel", *n.split("/"))) or h256(rb(os.path.join(NOS, "tgl_kernel", *n.split("/")))) != h]
assert not mal, ("o kernel do Nos nao e' o pinado pelo selo da v412 (pedras anteriores ausentes ou diferentes)", len(mal), mal[:5])
assert all(fmap.get(r) == s for r, s in ESP["modulos_v412_sha256"].items()) and all(fmap.get(r) == s for r, s in ESP["pedras_v411_e_antes_sha256"].items()), "os modulos da v412 (ou as pedras da v410) do ESPERADOS nao sao os do manifesto pinado"
_kn = ESP["kernel"]
assert h256(rb(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"))) == _kn["raiz_antes_sha256"] and h256(rb(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"))) == _kn["audit_antes_sha256"], "a raiz TGLExt.lean ou o TGL/Audit.lean do Nos nao sao os da v412 -- nao instalo"
# --- os novos (ausentes) e o corrigido (presente, com o sha antigo)
NOVOS = sorted(ESP["bundle_sha256"]); _N = len(NOVOS)
_KN = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v413.json"), encoding="utf-8"))
assert isinstance(_KN["novos"], list) and set(NOVOS) == set(_KN["novos"]) and _N == len(set(NOVOS)) == _kn["modulos_novos"] == _KN["n"] and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in NOVOS), ("a lista dos modulos novos da v413 nao bate", _N)
if (CM.get("kernel") or {}).get("modulos_novos") is not None:
    assert int(CM["kernel"]["modulos_novos"]) == _N, "o CANDIDATO diz outro numero de modulos novos"
assert not [r for r in NOVOS if os.path.exists(os.path.join(NOS, "tgl_kernel", *r.split("/")))], "algum dos modulos novos (v413) ja esta no kernel do Nos -- nao instalo"
KC = ESP["kernel_corrigido"]; assert KC and set(KC) == set(_KN.get("kernel_corrigido") or []), "o corrigido do ESPERADOS nao e' o da lista do construtor"
for rel, x in KC.items():
    p_ = os.path.join(NOS, "tgl_kernel", *rel.split("/")); assert os.path.isfile(p_) and h256(rb(p_)) == x["sha256_antes"] == fmap.get(rel), ("o modulo corrigido nao esta' no Nos com o sha antigo (v412)", rel)
# --- os backups de BYTES (tudo lido antes; nenhuma escrita no Nos ate' aqui)
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "ensaio": bool(ENSAIO), "esperados_sha16": h16(rb(os.path.join(E2, "ESPERADOS_v413.json"))), "backups": {}}
SELADOS = sorted(selo0["sha256"])
ALVOS = SELADOS + ["um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_pt.txt", "um_absoluto_en.txt",
                   os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")] + [os.path.join("tgl_kernel", *r.split("/")) for r in sorted(KC)]
assert len(ALVOS) == len(set(ALVOS)), "alvo de backup repetido"
for rel in ALVOS:
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert os.path.isfile(p), ("falta no Nos o arquivo a guardar", rel); assert not os.path.exists(b), b
for rel in ALVOS:
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts
    data = rb(p); open(b, "wb").write(data); assert rb(b) == data, "backup falhou: %s" % b
    if rel in selo0["sha256"]:
        assert h256(data) == selo0["sha256"][rel], ("o backup de um arquivo selado nao tem o sha256 do selo da v412", rel)
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data), "sha256": h256(data), "selado_v412": rel in selo0["sha256"]}
rec["modulos_novos_v413"] = {"fonte": "ESPERADOS_v413.bundle_sha256 (== kernel_modulos_novos_v413.json[novos])", "n": _N, "lista": NOVOS}   # a reversao usa ESTA lista
rec["kernel_corrigido"] = {rel: {"sha256_antes": x["sha256_antes"], "sha256_esperado_depois": x["sha256_depois"], "backup": rec["backups"][os.path.join("tgl_kernel", *rel.split("/"))]["backup"]} for rel, x in KC.items()}
rec["pino_recibo_pre_selo"] = pre
rec["selo_v412_pina"] = {"n_arquivos": len(SELADOS), "arquivos": SELADOS}
_dst = os.path.join(REG, "pilar_anterior_v412_" + ts); os.makedirs(_dst); rec["pilar_anterior_v412"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = rb(sp); open(os.path.join(_dst, f_), "wb").write(data); assert rb(os.path.join(_dst, f_)) == data
        rec["pilar_anterior_v412"]["arquivos"][f_] = {"bytes": len(data), "sha256": h256(data)}
assert rec["pilar_anterior_v412"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
# --- a troca do um.py (por ultimo)
tmp = um + ".tmp_instalar_v413_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(rb(tmp)) == ESP["candidato_sha16"]
assert rb(um) == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(rb(um)) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(REG, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "ensaio": bool(ENSAIO), "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N, "corrigido": sorted(KC),
                  "pre_selo_bn": "OK" if pre["ok"] else "DESVIO DECLARADO", "registro": out}, ensure_ascii=False))

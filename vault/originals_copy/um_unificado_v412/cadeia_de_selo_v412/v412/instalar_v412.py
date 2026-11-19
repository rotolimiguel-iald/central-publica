# -*- coding: utf-8 -*-
# [ADAPTADO v412, 18/11/2026, gerencia c1 (Etapa 3 enxuta; PLANO_ETAPA3_ENXUTA_v412.md; adaptar_instalar_e_reverter_v412.py)] o corpo e' o da v411 com o que depende de bundle NAO vazio pelo molde da v410: a v412 tem 156 modulos novos; o B(n) pre-selo sai como desvio declarado
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/instalar_v410.py (e do v400/instalar_v400.py, a versao anterior SEM modulo novo): a v411 NAO traz modulo novo de kernel; a lista dos modulos novos e' VAZIA (lida do ESPERADOS e do manifesto, conferida); a raiz TGLExt.lean e o TGL/Audit.lean do Nos tem de ser os da v410 e NAO mudam; as pedras anteriores incluem os 2 modulos da v410 (IALD2 e AEscala); recusa o artefato de ensaio do topo proposto; NAO executado na preparacao
"""instalar_v412.py -- instala o candidato v412 no canonico (ato da gerencia c1). Molde: instalar_v411.py (o corpo) e instalar_v410.py (a versao COM modulo novo).
Fail-closed (para na primeira falha, antes de qualquer escrita no Nos):
  * recusa o MODO DE ENSAIO do topo proposto; exige o topo DERIVADO (TOPO_RATIFICADO_v412_DERIVADO.json: o topo ratificado da v411 com os numeros lidos);
  * ESPERADOS_v412.json (esperados_v412_foco.py) e CANDIDATO_v412.json concordam; nenhum processo um.py nem trabalhador do pilar rodando;
  * o um.py do Nos e' a v411 selada (ESPERADOS.origem_sha16); o candidato tem o sha16 e os bytes do ESPERADOS; o cache do pilar guarda o resultado reaproveitado;
  * as pedras das versoes anteriores estao no kernel do Nos (as duas ultimas com o sha256 selado);
  * a raiz TGLExt.lean e o TGL/Audit.lean do Nos sao os da v411 selada (o rito os reescreve: o um.py materializa a raiz com os 156 imports);
  * os 156 modulos novos (ESPERADOS.bundle_sha256 == kernel_modulos_novos_v412.json[novos] == CANDIDATO.kernel.modulos_novos) NAO estao no kernel do Nos;
  * BACKUP DE BYTES de um.py, um_absoluto.json, _selo.json, _forma_canonica.md, _manifest.md, _pilar_quantico.json, o sidecar um_absoluto_selo_acom.json,
    tgl_kernel_proof_manifest.json, tgl_kernel/TGLExt.lean e tgl_kernel/TGL/Audit.lean; a copia do cache do pilar; so' entao troca o um.py.
DESVIO DECLARADO (v412): o recibo pre_selo do B(n) e o pino da Bancada NAO sao exigidos (a Bancada nao responde; o B(n) da v412 nao rodou;
decisao aberta no handoff). Grava APLICADO_AO_CANONICO_<ts>.json (o reverter usa a lista dos 156)."""
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
if os.environ.get("V412_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: o MODO DE ENSAIO do topo proposto nao instala nada (o artefato de ensaio NAO e' candidato)")
HERE = os.path.dirname(os.path.abspath(__file__))
assert os.path.exists(os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")), "falta TOPO_RATIFICADO_v412_DERIVADO.json (o topo ratificado da v411 com os numeros lidos): sem ele nao ha candidato -- nao instalo"
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v412.json"), encoding="utf-8")); CM = json.load(open(os.path.join(HERE, "CANDIDATO_v412.json"), encoding="utf-8"))
assert not ESP.get("ensaio_topo_proposto") and not CM.get("ensaio_topo_proposto"), "o ESPERADOS ou o CANDIDATO sao do ENSAIO do topo proposto -- nao instalo"
CAND = os.path.join(HERE, "um_v412_candidato.py")
h16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
ps = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                     "$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | "
                     "Where-Object { $_.CommandLine -ne $null -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker\\.py') } | ForEach-Object { $_.ProcessId }; Write-Output 'VIGIA_OK'"],
                    capture_output=True, text=True, timeout=60)
assert ps.returncode == 0 and "VIGIA_OK" in ps.stdout, "o vigia de processos FALHOU -- nao instalo"
assert not [x for x in ps.stdout.split() if x.strip().isdigit()], "ha processo um.py ou trabalhador do pilar rodando -- nao instalo"
um = os.path.join(NOS, "um.py"); raw0 = open(um, "rb").read()
assert h16(raw0) == ESP["origem_sha16"] == CM["base_v411_sha16"], "o canonico nao e a v411 selada (%s)" % h16(raw0)
cand = open(CAND, "rb").read(); assert h16(cand) == ESP["candidato_sha16"] == CM["sha16"] and len(cand) == ESP["candidato_bytes"]
# o recibo pre_selo do B(n): gerado e PINADO antes da instalacao (a producao so' foi lida); utilizavel; do um.py que esta no Nos agora
# (v412) DESVIO DECLARADO: o recibo pre_selo do B(n) (PINO_RECIBO_PRE_SELO_v412.json) e o pino da Bancada de producao NAO sao exigidos nesta versao:
# a Bancada (127.0.0.1:18777) nao responde e o B(n) da v412 nao rodou; o handoff leva isto as decisoes abertas. As outras travas seguem.
_cdir = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "checkpoints", "quantum_pillar", ESP["pilar"]["key"])
assert hashlib.sha256(open(os.path.join(_cdir, "result.json"), "rb").read()).hexdigest() == ESP["pilar"]["result_sha256"], "o cache do pilar nao guarda o resultado reaproveitado"
# v412: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas, FalsidadeDaInercia, PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional, Caminho, Vida, VerdadeAdendo, ProjecaoTransversalDaMeiaNat, Jo8v32, as OITO da v405, os 9 modulos da v407, os 4 da v408, os 2 da v409 e os 2 modulos da v411: IALD2 e AEscala) e o bundle do fecho da v406 (301 modulos em TGLExt/F1Fecho394, com a candidata CanonicalFullTGLWitnessR1) JA estao no kernel do Nos (a base instalada e' a v411 selada); (b) a v412 NAO traz modulo novo: a lista e' VAZIA.
# A lista dos modulos novos e' a do ESPERADOS (bundle_sha256, vazio) conferida contra o kernel.modulos_novos do ESPERADOS e do CANDIDATO; o numero e' o comprimento dela. Fail-closed em tudo.
_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", "Caminho", "Vida", "VerdadeAdendo", "ProjecaoTransversalDaMeiaNat", "Jo8v32", "PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion",
                      "PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual",   # (os 9 da v407)
                      "TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP",   # (os 4 da v408)
                      "TraducaoTuring", "ParNaFaceDeFock",   # (os 2 da v409)
                      "IALD2", "AEscala")   # (os 2 da v411: a lista de modulos novos que a cadeia v411 pinou; os mesmos de ESPERADOS_v412.bundle_v411_sha256)
assert sorted("TGLExt/" + n_ + ".lean" for n_ in ("IALD2", "AEscala")) == sorted(ESP["bundle_pedras_anteriores_sha256"]), "os modulos da v411 da lista nao sao os do ESPERADOS (bundle_v411_sha256)"
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_ANTERIORES) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "NetworkProofAuditR8.lean")) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394", "CanonicalFullTGLWitnessR1.lean")), "as pedras anteriores (v394 a v411, as oito da v405, os 9 modulos da v407, os 4 da v408, os 2 da v409, os 2 da v411 e o bundle do fecho da v406 inclusive) nao estao no kernel do Nos -- nao instalo"
assert all(hashlib.sha256(open(os.path.join(NOS, "tgl_kernel", *rel.split("/")), "rb").read()).hexdigest() == s_ for rel, s_ in ESP["bundle_pedras_anteriores_sha256"].items()), "os modulos da v411 no kernel do Nos nao tem o sha da v411 selada -- nao instalo"
_kn = ESP["kernel"]   # (v412) a raiz e o Audit do Nos tem de ser os da v411 selada; o rito os reescreve (a raiz ganha os 156 imports; lidos do ESPERADOS_v412.json, nunca digitados)
assert h16(open(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"), "rb").read()) == _kn["raiz_antes_sha16"] and h16(open(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), "rb").read()) == _kn["audit_antes_sha16"], "a raiz TGLExt.lean ou o TGL/Audit.lean do Nos nao sao os da v411 selada (== os do candidato) -- nao instalo"
NOVOS_V412 = sorted(ESP["bundle_sha256"]); _N = len(NOVOS_V412)
_KN = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v412.json"), encoding="utf-8"))   # (v412, molde v410) a lista dos modulos novos que o construtor gravou
assert isinstance(_KN["novos"], list), "kernel_modulos_novos_v412.json tem de trazer a LISTA em 'novos'"
assert _N == 156 == len(set(NOVOS_V412)) == ESP["kernel"]["modulos_novos"] == CM["kernel"]["modulos_novos"] and set(NOVOS_V412) == set(_KN["novos"]) and all(x_.startswith("TGLExt/") and x_.count("/") == 1 and x_.endswith(".lean") for x_ in NOVOS_V412), ("a lista dos modulos novos da v412 nao bate", _N)
assert not [rel for rel in NOVOS_V412 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v412) ja esta no kernel do Nos -- nao instalo"
ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}
rec["modulos_novos_v412"] = {"fonte": "ESPERADOS_v412.bundle_sha256 (156; == kernel_modulos_novos_v412.json[novos] == CANDIDATO.kernel.modulos_novos)", "n": _N, "lista": NOVOS_V412}   # o reverter usa ESTA lista (a que o instalar conferiu)
rec["pino_recibo_pre_selo"] = {"desvio_declarado": "o recibo pre_selo do B(n) e o pino da Bancada nao foram exigidos na v412 (a Bancada nao responde; o B(n) da v412 nao rodou); decisao aberta no handoff"}
for rel in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_pilar_quantico.json", "um_absoluto_selo_acom.json", "tgl_kernel_proof_manifest.json",
            os.path.join("tgl_kernel", "TGLExt.lean"), os.path.join("tgl_kernel", "TGL", "Audit.lean")):   # (o rito reescreve o manifesto do kernel; ele entra nos backups e o reverter o restaura)
    p = os.path.join(NOS, rel); b = p + ".bak_" + ts; assert not os.path.exists(b), b
    data = open(p, "rb").read(); open(b, "wb").write(data); assert open(b, "rb").read() == data, "backup falhou: %s" % b
    rec["backups"][rel] = {"backup": b, "bytes": len(data), "sha16": h16(data)}
_dst = os.path.join(HERE, "pilar_anterior_v411_" + ts); os.makedirs(_dst); rec["pilar_anterior_v411"] = {"de": _cdir, "para": _dst, "arquivos": {}}
for f_ in sorted(os.listdir(_cdir)):
    sp = os.path.join(_cdir, f_)
    if os.path.isfile(sp):
        data = open(sp, "rb").read(); open(os.path.join(_dst, f_), "wb").write(data); assert open(os.path.join(_dst, f_), "rb").read() == data
        rec["pilar_anterior_v411"]["arquivos"][f_] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
assert rec["pilar_anterior_v411"]["arquivos"]["result.json"]["sha256"] == ESP["pilar"]["result_sha256"]
tmp = um + ".tmp_instalar_v412_" + ts; open(tmp, "wb").write(cand)
assert os.path.getsize(tmp) == len(cand) and h16(open(tmp, "rb").read()) == ESP["candidato_sha16"]
assert open(um, "rb").read() == raw0, "o um.py mudou entre a leitura e a troca -- nao substituo"
os.replace(tmp, um); assert h16(open(um, "rb").read()) == ESP["candidato_sha16"]
rec["um_py_novo"] = {"bytes": len(cand), "sha16": ESP["candidato_sha16"], "origem": CAND}
out = os.path.join(HERE, "APLICADO_AO_CANONICO_%s.json" % ts); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
print(json.dumps({"ts": ts, "um_py_novo": rec["um_py_novo"], "n_backups": len(rec["backups"]), "modulos_novos": _N}, ensure_ascii=False))

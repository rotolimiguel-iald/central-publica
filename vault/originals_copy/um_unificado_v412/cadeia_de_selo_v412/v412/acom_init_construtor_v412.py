# -*- coding: utf-8 -*-
"""acom_init_construtor_v412.py -- memoria ACOM da Etapa 1 da preparacao da v412: o agente claude-construtor-v412 inscreve a SUA referencia (init da fonte original
ORDEM_AO_CONSTRUTOR_v412_ETAPA_1.md, sha256 LIDO do arquivo) e grava SESSION_REFERENCE_construtor_v412.json; depois faz `project` (so' leitura).
Molde: v411\\acom_init_construtor_v411.py e v410\\acom_init_construtor_v410.py. A referencia SESSION_REFERENCE_prep_v412.json e' da GERENCIA: nao e' lida nem tocada aqui.
Nao adota a tarefa de outra sessao; nao autoriza acoes; nao move gate. Uso: C:\\Python314\\python.exe -X utf8 acom_init_construtor_v412.py [--transicao <arquivo_json_com_q_e_p>]
(reexecutavel: se a referencia existe, so' faz project)."""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import uuid

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
ACD = os.path.join(H, "acom_construtor_v412")
os.makedirs(ACD, exist_ok=True)


def chamar(payload, nome):
    req = os.path.join(ACD, "acom_construtor_%s_%s.request.json" % (ts, nome))
    rec = os.path.join(ACD, "acom_construtor_%s_%s.receipt.json" % (ts, nome))
    open(req, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=1))
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    open(rec, "w", encoding="utf-8").write(out + ("\n--- stderr ---\n" + err if err else ""))
    try:
        j = json.loads(out)
    except Exception:  # noqa: BLE001
        j = {"raw": out[:600], "stderr": err[:600]}
    print("==", nome, "rc", r.returncode, json.dumps({k: (str(v)[:200]) for k, v in (j.items() if isinstance(j, dict) else [])}, ensure_ascii=False)[:900])
    return r.returncode, j


# (17/11: o init da ordem original foi RECUSADO com erro visivel, ConfidentialContent: dotenv_name e escritorio_path, na linha da regra dos confidenciais;
#  a fonte inscrita e' o EXCERTO DECLARADO composto por acom_construtor_v412\fazer_excerto_da_ordem_v412.py, que diz no cabecalho a ordem original, o sha256 e a linha que saiu)
OBJ = os.path.join(ACD, "ORDEM_v412_ETAPA_1_EXCERTO_PARA_ACOM.md")
REF = os.path.join(H, "SESSION_REFERENCE_construtor_v412.json")
ACTOR = {"id": "claude-construtor-v412", "kind": "agent"}
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": ACTOR, "write_reference": REF,
                    "constraints": {"unit": "preparacao_v412_etapa_1_sandbox_k412c_bundle_34_modulos_bump_portao_do_pilar",
                                    "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos": True, "lake_build_only_in_the_sandbox_k412c": True,
                                    "no_gpu_no_training_touch": True, "operator_gates_remain_operator_gates": True,
                                    "no_install_no_rite_no_commit_no_push_no_candidate": True,
                                    "sources_under_review_are_read_only": True,
                                    "stop_at_PRONTO_PARA_CANDIDATO_v412": True}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, pj = chamar({"operation": "project", "reference": REF}, "project")
assert rc == 0, "project falhou"
if "--transicao" in sys.argv:
    tj = json.load(open(sys.argv[sys.argv.index("--transicao") + 1], encoding="utf-8"))
    rc_g, gj = chamar({"operation": "get", "reference": REF}, "get")
    payload = {"operation": "transition", "reference": REF, "actor": ACTOR, **tj}
    _res = (gj.get("result") or {}) if isinstance(gj, dict) else {}
    _rev = _res.get("revision") if isinstance(_res, dict) else None
    if _rev is None and isinstance(_res, dict):
        _rev = (_res.get("state") or {}).get("revision") if isinstance(_res.get("state"), dict) else None
    if "expected_revision" not in payload:
        assert isinstance(_rev, int), ("revisao atual nao lida do get; nao faco transicao as cegas", str(gj)[:300])
        payload["expected_revision"] = _rev
    rc_t, tjr = chamar(payload, "transition")
    print("transicao rc", rc_t)
print("referencia:", REF, "sha16", sha(REF)[:16])

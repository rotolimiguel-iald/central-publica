# -*- coding: utf-8 -*-
"""acom_init_prep_v412.py -- memoria ACOM da PREPARACAO da v412: a gerencia c1 inscreve a referencia propria desta missao. A fonte original
e' a ORDEM DO OPERADOR de 13/11/2026 (arquivo de bytes em work\\cunhagens_13out; sha256 LIDO do arquivo). Grava SESSION_REFERENCE_prep_v412.json
e faz `project` (so' leitura). Molde: acom_init_construtor_v411.py. Nao adota a tarefa de outra sessao; nao autoriza acoes; nao move gate.
Uso: C:\\Python314\\python.exe -X utf8 acom_init_prep_v412.py   (reexecutavel: se a referencia existe, so' faz project)"""
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


def chamar(payload, nome):
    req = os.path.join(H, "acom_prep_%s_%s.request.json" % (ts, nome))
    rec = os.path.join(H, "acom_prep_%s_%s.receipt.json" % (ts, nome))
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


OBJ = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_vamos_comecar_a_construir_a_v412_camada_iald_cientifica_t1_3mais1_gh_tau_teste_cego_5_sigma_kimi_verbatim.txt"
REF = os.path.join(H, "SESSION_REFERENCE_prep_v412.json")
ACTOR = {"id": "claude-c1", "kind": "agent"}
assert os.path.isfile(OBJ)
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": ACTOR, "write_reference": REF,
                    "constraints": {"unit": "preparacao_da_v412_levantamento_e_desenho",
                                    "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_installer_and_the_seal_rite": True,
                                    "operator_gates_remain_operator_gates": True,
                                    "no_install_no_rite_no_commit_no_push_in_this_phase": True,
                                    "no_test_data_is_opened_and_h0dn_bg1_is_never_reopened": True,
                                    "the_score_is_read_to_the_operator_before_any_test_that_can_return_negative": True,
                                    "kimi_works_by_file_only_and_its_output_is_candidate_until_reviewed": True,
                                    "reviewer_distinct_from_builder": True}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, pj = chamar({"operation": "project", "reference": REF}, "project")
assert rc == 0, "project falhou"
print("referencia:", REF, "sha16", sha(REF)[:16])

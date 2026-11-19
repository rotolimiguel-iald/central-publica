# -*- coding: utf-8 -*-
"""Consolida resultados R3.1 e emite manifestos/hashes, sem dados experimentais."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from r31_motor import ALPHA_5SIGMA, MASTER_SEED, SCENARIOS

HERE = Path(__file__).resolve().parent
KIMI = HERE.parent.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def main() -> None:
    rows = {}
    for path in HERE.glob("resultados_r31_part_*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload["scenarios"]:
            base_sessions = row["cost"]["base_sessions_20_cells"]
            triage_total = row["cost"]["triage_candidate_sessions_mean_scaled_4_families"]
            extra = max(triage_total - base_sessions, 0.0)
            row["cost"]["triage_extra_k1_interactions_mean"] = extra
            row["cost"]["base_plus_triage_interactions_mean"] = row["cost"]["base_interactions_12_calls"] + extra
            rows[row["id"]] = row
        path.write_bytes(encode(payload))
    expected = [s.sid for s in SCENARIOS]
    missing = [sid for sid in expected if sid not in rows]
    if missing:
        raise SystemExit(f"Cenários ausentes: {missing}")
    probability_fields = (
        "integrity_ok", "raw_any_primary_rejection", "raw_all_primary",
        "raw_any_tost_rejection", "raw_all_tost", "powered",
        "nonspecific_powered", "falsified", "inconclusive_controls",
    )
    for row in rows.values():
        row["monte_carlo_95"] = {}
        for field in probability_fields:
            p = float(row["rates"][field])
            se = math.sqrt(max(p * (1.0 - p) / row["nsim"], 0.0))
            row["monte_carlo_95"][field] = [max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se)]
    repeat_path = HERE / "resultados_r31_repeticao_BASE_INDEPENDENTE_R31.json"
    repeat_payload = json.loads(repeat_path.read_text(encoding="utf-8"))
    for row in repeat_payload["scenarios"]:
        base_sessions = row["cost"]["base_sessions_20_cells"]
        triage_total = row["cost"]["triage_candidate_sessions_mean_scaled_4_families"]
        extra = max(triage_total - base_sessions, 0.0)
        row["cost"]["triage_extra_k1_interactions_mean"] = extra
        row["cost"]["base_plus_triage_interactions_mean"] = row["cost"]["base_interactions_12_calls"] + extra
    repeat_path.write_bytes(encode(repeat_payload))
    repeat_equal = (HERE / "resultados_r31_part_BASE_INDEPENDENTE_R31.json").read_bytes() == repeat_path.read_bytes()
    repeat_hash = digest(repeat_path)
    final = {
        "schema": "K06_R31_SESSOES_INDIVIDUAIS_CLUSTERIZADAS_V1",
        "master_seed": MASTER_SEED,
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "scenarios": [rows[sid] for sid in expected],
    }
    final_bytes = encode(final)
    (HERE / "resultados_r31.json").write_bytes(final_bytes)
    final_hash = hashlib.sha256(final_bytes).hexdigest()

    validation = json.loads((HERE / "validacao_r31.json").read_text(encoding="utf-8"))
    size_base = rows["NULO_GLOBAL_ISO_FRONTEIRA"]["rates"]["raw_any_primary_rejection"]
    size_5 = rows["NULO_GLOBAL_ISO_FRONTEIRA_N618"]["rates"]["raw_any_primary_rejection"]
    tost_plus = rows["TOST_FRONTEIRA_MAIS_075_060"]["rates"]["raw_any_tost_rejection"]
    tost_minus = rows["TOST_FRONTEIRA_MENOS_060_075"]["rates"]["raw_any_tost_rejection"]
    tost_plus_5 = rows["TOST_FRONTEIRA_MAIS_075_060_N618"]["rates"]["raw_any_tost_rejection"]
    tost_minus_5 = rows["TOST_FRONTEIRA_MENOS_060_075_N618"]["rates"]["raw_any_tost_rejection"]
    nonspecific = {
        "n320_alpha005": rows["NULO_ESPECIFICO_090"]["rates"]["nonspecific_powered"],
        "n618_alpha5sigma": rows["NULO_ESPECIFICO_090_N618"]["rates"]["nonspecific_powered"],
        "n655_alpha5sigma": rows["NULO_ESPECIFICO_090_N655"]["rates"]["nonspecific_powered"],
    }
    gates = [
        {"gate": "FFT_EXATA_VS_ENUMERACAO_E_DP", "status": "PASS" if validation["exact_signflip_small_case"]["pass"] and validation["fft_vs_dp_reference"]["pass"] else "FAIL", "value": validation["fft_vs_dp_reference"]["max_errors"]},
        {"gate": "TAMANHO_GLOBAL_ALPHA_005", "status": "PASS" if size_base <= 0.05 else "FAIL", "value": size_base, "nominal": 0.05},
        {"gate": "TAMANHO_GLOBAL_5SIGMA", "status": "OPEN_RESOLUCAO_MC", "value": size_5, "nominal": ALPHA_5SIGMA, "note": "1000 corridas não resolvem a cauda nominal; não declarar PASS"},
        {"gate": "TOST_TAMANHO_ALPHA_005_DUAS_FRONTEIRAS", "status": "PASS" if max(tost_plus, tost_minus) <= 0.05 else "FAIL", "value": [tost_plus, tost_minus], "nominal": 0.05},
        {"gate": "TOST_TAMANHO_5SIGMA_DUAS_FRONTEIRAS", "status": "OPEN_RESOLUCAO_MC", "value": [tost_plus_5, tost_minus_5], "nominal": ALPHA_5SIGMA, "note": "não declarar validação da cauda"},
        {"gate": "NONSPECIFIC_POWERED_PROBABILIDADE", "status": "FAIL" if max(nonspecific.values()) < 0.90 else "PASS", "value": nonspecific, "reference_target": 0.90},
        {"gate": "WALD_T_FOCAL_5SIGMA", "status": "FAIL_BLOQUEADO", "value": "intervalo t por cluster não validado na cauda 5σ"},
        {"gate": "EXTRATOR_CERTIFICADO", "status": "FAIL_BLOQUEADO", "value": "tetos 0,619206/0,091028; independência dos 96 erros aberta"},
        {"gate": "ENTRADA_JANELA_TOKENIZERS", "status": "OPEN_BLOQUEADO", "value": "modelos/tokenizers/janelas não escolhidos"},
        {"gate": "LEXICO_ISOMORFO", "status": "OPEN_BLOQUEADO", "value": "léxico e perturbações não congelados"},
        {"gate": "PRODUCAO", "status": "FAIL_BLOQUEADO", "value": "portas de tamanho, poder, extrator, janela, léxico e ratificação"},
    ]
    analysis = {
        "schema": "K06_R31_ANALISE_CANDIDATA_V1",
        "status": "REVISADA_INTERNAMENTE_NAO_RATIFICADA",
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "rev0_preserved": "REV0/",
        "old_aggregate_numbers": "MODELO_AGREGADO_INCOMPLETO_NAO_PODER_INTEGRAL",
        "sessions": "individuais pareadas; A8 e retorno separados; Q-S dependentes; focal fixa; controles com efeito de texto",
        "clusters": 27,
        "cluster_rule": "27 clusters texto-conscientes; diferenças por bloco; sinais no nível dos clusters; n bruto nunca substituído por n_eff",
        "primary": "3 famílias × ISO-A/ISO-B = 6 testes de não inferioridade; Holm global 6; PLA/OUT fora da evidência primária",
        "manipulation_contamination": "6 Q PLA/OUT como diagnóstico e 12 S como checagens; não são evidência primária de convergência",
        "tost": "duas caudas exatas: 20D+3 e 20D-3; p=max(p+,p-); Holm sobre 6 PLA/OUT; empates incluídos",
        "focal_interval": "t robusto por 27 clusters; não CP binomial; cauda 5σ não validada e bloqueada",
        "falsified_union": "3 intervalos focais + 6 direções ISO; Bonferroni alpha/9",
        "nonspecific_rule": "6 TOST Holm + focal inferior>0,80 + sem FALSIFIED; precedência sobre POWERED",
        "interactions": 12,
        "return": "p=8,r=10",
        "annex_alignment_dependency": "anexos de outros agentes com 8 interações ou p=4,r=6 exigem emenda própria; não editados aqui",
        "seeds": {sid: rows[sid]["seed"] for sid in expected},
        "nsim_per_scenario": 1000,
        "deterministic_base_repeat": {"identical_bytes": repeat_equal, "sha256": repeat_hash},
        "monte_carlo_intervals": "aproximação normal da incerteza de simulação; não intervalos para modelos reais; custos são médias sem IC",
        "gates": gates,
        "results_sha256": final_hash,
        "rev0_preservation_manifest": "REV0/PRESERVACAO_SHA256.txt",
    }
    analysis_bytes = encode(analysis)
    (HERE / "manifesto_analise_r31.json").write_bytes(analysis_bytes)
    analysis_hash = hashlib.sha256(analysis_bytes).hexdigest()

    files = [
        HERE / "r31_motor.py",
        HERE / "simular_r31_sessoes.py",
        HERE / "validar_r31.py",
        HERE / "gerar_manifestos_r31.py",
        HERE / "validacao_r31.json",
        HERE / "validacao_r31.log",
        HERE / "resultados_r31.json",
        HERE / "resultados_r31_repeticao_BASE_INDEPENDENTE_R31.json",
        HERE / "r31_repeticao_BASE_INDEPENDENTE_R31.log",
        HERE / "manifesto_analise_r31.json",
        HERE / "REV0" / "PRESERVACAO_SHA256.txt",
    ]
    files.extend(sorted(HERE.glob("r31_*.log")))
    artifacts = []
    for path in files:
        if not path.exists():
            continue
        artifacts.append({"path": str(path.relative_to(HERE)).replace("\\", "/"), "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest = {
        "schema": "K06_R31_SHA256_V1",
        "analysis_manifest_sha256": analysis_hash,
        "results_sha256": final_hash,
        "manifest_does_not_hash_itself": True,
        "artifacts": artifacts,
    }
    manifest_bytes = encode(manifest)
    (HERE / "MANIFESTO_R31_SHA256.json").write_bytes(manifest_bytes)
    print(f"RESULTADOS_R31_SHA256 {final_hash}")
    print(f"ANALISE_R31_SHA256 {analysis_hash}")
    print(f"MANIFESTO_R31_SHA256 {hashlib.sha256(manifest_bytes).hexdigest()}")
    for gate in gates:
        print(f"GATE {gate['status']} {gate['gate']} {gate['value']}")


if __name__ == "__main__":
    main()

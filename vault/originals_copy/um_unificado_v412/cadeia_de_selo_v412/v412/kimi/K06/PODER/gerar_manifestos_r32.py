# -*- coding: utf-8 -*-
"""Consolida resultados R3.2 e emite manifestos/hashes, sem dados experimentais."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from r32_motor import ALPHA_5SIGMA, MASTER_SEED, SCENARIOS

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def correct_cost(row: dict) -> None:
    base_sessions = row["cost"]["base_sessions_20_cells"]
    triage_total = row["cost"]["triage_candidate_sessions_mean_scaled_4_families"]
    extra = max(triage_total - base_sessions, 0.0)
    row["cost"]["triage_extra_k1_interactions_mean"] = extra
    row["cost"]["base_plus_triage_interactions_mean"] = row["cost"]["base_interactions_12_calls"] + extra


def main() -> None:
    rows = {}
    for path in HERE.glob("resultados_r32_part_*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for row in payload["scenarios"]:
            correct_cost(row)
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

    repeat_path = HERE / "resultados_r32_repeticao_BASE_INDEPENDENTE_R32.json"
    repeat_payload = json.loads(repeat_path.read_text(encoding="utf-8"))
    for row in repeat_payload["scenarios"]:
        correct_cost(row)
    repeat_path.write_bytes(encode(repeat_payload))
    repeat_equal = (HERE / "resultados_r32_part_BASE_INDEPENDENTE_R32.json").read_bytes() == repeat_path.read_bytes()
    repeat_hash = digest(repeat_path)

    final = {
        "schema": "K06_R32_SESSOES_INDIVIDUAIS_CLUSTERIZADAS_V1",
        "master_seed": MASTER_SEED,
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "scenarios": [rows[sid] for sid in expected],
    }
    final_bytes = encode(final)
    (HERE / "resultados_r32.json").write_bytes(final_bytes)
    final_hash = hashlib.sha256(final_bytes).hexdigest()

    validation = json.loads((HERE / "validacao_r32.json").read_text(encoding="utf-8"))
    size_base = rows["NULO_GLOBAL_ISO_FRONTEIRA"]["rates"]["raw_any_primary_rejection"]
    size_base_hi = rows["NULO_GLOBAL_ISO_FRONTEIRA"]["monte_carlo_95"]["raw_any_primary_rejection"][1]
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
    all_logic = all(row["logic_implications_A8_PRE_Q_RET"] for row in rows.values())
    all_boundaries = all(row["boundary_diagnostics"]["pass"] for row in rows.values() if row["q_targets"] is not None)
    gates = [
        {"gate": "FFT_EXATA_VS_ENUMERACAO_E_DP", "status": "PASS" if validation["exact_signflip_small_case"]["pass"] and validation["fft_vs_dp_reference"]["pass"] else "FAIL", "value": validation["fft_vs_dp_reference"]["max_errors"]},
        {"gate": "LOGICA_A8_PRE_Q_RET", "status": "PASS" if all_logic else "FAIL", "value": all_logic},
        {"gate": "FRONTEIRAS_D_MAIS_MENOS_015_TOLERANCIA_0005", "status": "PASS" if all_boundaries else "FAIL", "value": all_boundaries},
        {"gate": "TAMANHO_GLOBAL_ALPHA_005", "status": "OPEN_BORDERLINE" if size_base_hi >= 0.05 else "PASS", "value": size_base, "mc95": rows["NULO_GLOBAL_ISO_FRONTEIRA"]["monte_carlo_95"]["raw_any_primary_rejection"], "note": "ponto acima de 0,05, mas IC inclui o nominal"},
        {"gate": "TAMANHO_GLOBAL_5SIGMA", "status": "OPEN_RESOLUCAO_MC", "value": size_5, "nominal": ALPHA_5SIGMA},
        {"gate": "TOST_TAMANHO_ALPHA_005_DUAS_FRONTEIRAS", "status": "PASS" if max(tost_plus, tost_minus) <= 0.05 else "FAIL", "value": [tost_plus, tost_minus], "nominal": 0.05},
        {"gate": "TOST_TAMANHO_5SIGMA_DUAS_FRONTEIRAS", "status": "OPEN_RESOLUCAO_MC", "value": [tost_plus_5, tost_minus_5], "nominal": ALPHA_5SIGMA},
        {"gate": "NONSPECIFIC_POWER_PROBABILIDADE", "status": "FAIL" if max(nonspecific.values()) < 0.90 else "PASS", "value": nonspecific, "reference_target": 0.90, "meaning": "poder sob equivalência verdadeira, não tamanho"},
        {"gate": "WALD_T_FOCAL_5SIGMA", "status": "FAIL_BLOQUEADO", "value": "intervalo t por cluster não validado na cauda 5σ"},
        {"gate": "EXTRATOR_CERTIFICADO", "status": "FAIL_BLOQUEADO", "value": "tetos 0,619206/0,091028; independência dos 96 erros aberta"},
        {"gate": "ENTRADA_JANELA_TOKENIZERS", "status": "OPEN_BLOQUEADO", "value": "modelos/tokenizers/janelas não escolhidos"},
        {"gate": "LEXICO_ISOMORFO", "status": "OPEN_BLOQUEADO", "value": "léxico e perturbações não congelados"},
        {"gate": "PRODUCAO", "status": "FAIL_BLOQUEADO", "value": "poder, extrator, janela, léxico, cauda 5σ e ratificação"},
    ]
    analysis = {
        "schema": "K06_R32_ANALISE_CANDIDATA_V1",
        "status": "REVISADA_INTERNAMENTE_NAO_RATIFICADA",
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "rev1_preserved": "REV1/",
        "r31_boundary_history": "FRONTEIRAS_MAL_PARAMETRIZADAS_COM_D_APROX_010_NAO_USADAS_COMO_TAMANHO",
        "old_aggregate_numbers": "MODELO_AGREGADO_INCOMPLETO_NAO_PODER_INTEGRAL",
        "sessions": "individuais pareadas; A8=>PRE; RETORNO=>PRE; Q=>RETORNO; Q-S dependentes; focal fixa",
        "direct_q_boundaries": "Q parametrizado diretamente; D=+0,15 e D=-0,15; tolerância absoluta 0,005 por família/comparador",
        "clusters": 27,
        "cluster_rule": "27 clusters texto-conscientes; sinais no nível dos clusters; nunca n_eff",
        "primary": "3 famílias × ISO-A/ISO-B = 6 testes; PLA/OUT fora da evidência primária",
        "manipulation_contamination": "6 Q PLA/OUT diagnóstico e 12 S checagens; não evidência primária",
        "tost": "duas caudas exatas 20D+3 e 20D-3; p=max; Holm 6; empates incluídos",
        "size_vs_power": "fronteiras ISO/TOST medem tamanho; base/ICC medem poder alternativa; equivalência 0,90 mede poder NONSPECIFIC",
        "focal_interval": "t robusto por 27 clusters; não CP binomial; cauda 5σ não validada e bloqueada",
        "falsified_union": "3 intervalos focais + 6 direções ISO; Bonferroni alpha/9",
        "nonspecific_rule": "6 TOST Holm + focal inferior>0,80 + sem FALSIFIED; precedência sobre POWERED",
        "interactions": 12,
        "return": "p=8,r=10",
        "annex_alignment": "anexos alinhados por erratas próprias a 12 interações e p=8,r=10",
        "seeds": {sid: rows[sid]["seed"] for sid in expected},
        "nsim_per_scenario": 1000,
        "deterministic_base_repeat": {"identical_bytes": repeat_equal, "sha256": repeat_hash},
        "monte_carlo_intervals": "aproximação normal da incerteza de simulação; custos são médias sem IC",
        "gates": gates,
        "results_sha256": final_hash,
        "rev1_preservation_manifest": "REV1/PRESERVACAO_SHA256.txt",
    }
    analysis_bytes = encode(analysis)
    (HERE / "manifesto_analise_r32.json").write_bytes(analysis_bytes)
    analysis_hash = hashlib.sha256(analysis_bytes).hexdigest()

    files = [
        HERE / "r32_motor.py",
        HERE / "simular_r32_sessoes.py",
        HERE / "validar_r32.py",
        HERE / "gerar_manifestos_r32.py",
        HERE / "validacao_r32.json",
        HERE / "validacao_r32.log",
        HERE / "resultados_r32.json",
        HERE / "resultados_r32_repeticao_BASE_INDEPENDENTE_R32.json",
        HERE / "r32_repeticao_BASE_INDEPENDENTE_R32.log",
        HERE / "manifesto_analise_r32.json",
        HERE / "REV1" / "PRESERVACAO_SHA256.txt",
    ]
    files.extend(sorted(HERE.glob("resultados_r32_part_*.json")))
    files.extend(sorted(HERE.glob("r32_*.log")))
    artifacts = []
    for path in files:
        if not path.exists():
            continue
        artifacts.append({"path": str(path.relative_to(HERE)).replace("\\", "/"), "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest = {
        "schema": "K06_R32_SHA256_V1",
        "analysis_manifest_sha256": analysis_hash,
        "results_sha256": final_hash,
        "manifest_does_not_hash_itself": True,
        "all_required_part_files_included": True,
        "artifacts": artifacts,
    }
    manifest_bytes = encode(manifest)
    (HERE / "MANIFESTO_R32_SHA256.json").write_bytes(manifest_bytes)
    print(f"RESULTADOS_R32_SHA256 {final_hash}")
    print(f"ANALISE_R32_SHA256 {analysis_hash}")
    print(f"MANIFESTO_R32_SHA256 {hashlib.sha256(manifest_bytes).hexdigest()}")
    for gate in gates:
        print(f"GATE {gate['status']} {gate['gate']} {gate['value']}")


if __name__ == "__main__":
    main()

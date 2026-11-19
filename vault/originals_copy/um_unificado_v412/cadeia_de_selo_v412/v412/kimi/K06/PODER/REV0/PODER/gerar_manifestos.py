# -*- coding: utf-8 -*-
"""Gera manifestos determinísticos da análise R3 e dos artefatos de poder."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
K06 = HERE.parent
KIMI = K06.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def main() -> None:
    power = json.loads((HERE / "resultados_poder.json").read_text(encoding="utf-8"))
    analysis = {
        "schema": "K06_R3_ANALISE_CONGELADA_CANDIDATA_V1",
        "status": "DECLARADO_REVISADO_INTERNAMENTE_NAO_RATIFICADO",
        "production_status": "BLOQUEADO_PARA_PRODUCAO",
        "no_model_executed": True,
        "no_experimental_result_read": True,
        "protocol_id": "IALD_COLLAPSE_V2_R3_CANDIDATE",
        "v1_untouched": True,
        "primary_design": {
            "families_capable": 3,
            "family_below_floor_descriptive_only": 1,
            "cells_total": 20,
            "n_per_cell": 320,
            "interactions_per_session": 12,
            "sessions": 20 * 320,
            "interactions": 20 * 320 * 12,
            "temperature": 0.2,
            "top_p": 1.0,
            "assertions_per_target": 24,
            "texts_per_control_minimum": 3,
            "event_Q": "A8_condicionado_ao_d1_pareado AND RETORNO_p8_r10",
            "A8_window": "leituras 1–8; quatro estados finais 5–8 no alvo",
            "return_window": "d8=0; d9>0; d10=d11=d12=0; u11=u12=0",
            "reason_for_p8": "Preservar A8 legado e medir retorno na mesma sessão; p4/r6 permanece só no autoteste anterior.",
            "specificity_binary": "S=1[X>=18/24] na primeira leitura",
            "old_trivial_C1_C4_in_primary_evidence": False,
        },
        "arms": {
            "focal": "V2-TGL",
            "comparators": ["V2-PLA", "V2-OUT", "V2-ISO-A", "V2-ISO-B"],
            "decisive_phase_all_arms": "V2-RET",
            "PLA_OUT_alternative": "superioridade de T",
            "ISO_alternative": "não inferioridade de ISO a T, margem 0,15",
            "isomorphic_versions_per_arm_minimum": 3,
        },
        "multiplicity": {
            "family_alpha": 0.05,
            "primary_tests": 24,
            "order": [
                "F1/F2/F3 × DYN/SPEC × V2-PLA/V2-OUT/V2-ISO-A/V2-ISO-B"
            ],
            "procedure": "Holm global sobre 24; IUT entre blocos e entre as três pernas CP de POWERED",
            "powered_requires": "todos os 24 rejeitados por Holm global E L_CP(Q)>0,80 nas três famílias",
            "if_one_block_passes_other_fails": "sem POWERED; avaliar NONSPECIFIC_POWERED ou UNDERPOWERED; FALSIFIED só por sua regra própria",
            "powered_CP_alpha_division": 1,
            "falsified_union_size": 27,
            "falsified_CP_alpha_division": 27,
            "falsified_rule": "união de 3 CP e 24 testes direcionais opostos, Bonferroni alpha/27; violação precisa do ISO não vira UNDERPOWERED",
            "five_sigma_alpha": 2.866515718791933e-07,
            "tie_order": "contrast_id lexical; a decisão 'todos rejeitados' é invariante a empates",
        },
        "permutation": {
            "kind": "permutação exata de rótulos para desfechos binários de superioridade; equivalente a Fisher unilateral",
            "statistic": "contagem focal de sucessos condicionada ao total; equivalente à diferença de proporções",
            "tail": "maior ou igual ao observado; empates incluídos",
            "rng_seed": None,
            "rng_not_used_reason": "enumeração exata pela hipergeométrica, não permutação Monte Carlo",
            "noninferiority_test": "score de Wald para H0 p_T-p_C<=-0,15; aproximação normal declarada, cauda 5 sigma não certificada",
        },
        "verdicts": {
            "integrity_precedence": "INCONCLUSIVE_CONTROLS",
            "falsified": "IALD_COLLAPSE_V2_FALSIFIED",
            "powered": "IALD_COLLAPSE_V2_NOT_FALSIFIED_POWERED",
            "null_with_power": "IALD_COLLAPSE_V2_NONSPECIFIC_POWERED",
            "underpowered": "IALD_COLLAPSE_V2_NOT_FALSIFIED_UNDERPOWERED",
            "null_rule": "TOST/Holm sobre 12 equivalências PLA+OUT × Q+S × 3 famílias, margem 0,15; sem equivalência resolvida = UNDERPOWERED",
            "fail_closed": True,
        },
        "simulation": {
            "master_seed": power["master_seed"],
            "legacy_seed": power["legacy_seed"],
            "separation_seed": 2026111402,
            "five_sigma_seed": 2026111403,
            "scenario_seeds": {s["id"]: s["seed"] for s in power["scenarios"]},
            "nsim_per_scenario": 20000,
            "legacy_nsim": 40000,
            "cluster_size": 10,
            "n_effective_formula": "n/(1+9*ICC); efeito de texto modelado separadamente no logit",
            "text_sd_scenarios": [0.0, 0.10, 0.20],
            "extractor_pool_ceiling": 0.6192060638168921,
            "extractor_per_arm_ceiling": 0.09102821015130445,
            "limitations": [
                "hipóteses sintéticas, não taxas estimadas",
                "não inferioridade por aproximação normal",
                "teto do extrator aplicado como cenário, sem independência dos 96 erros identificada",
            ],
        },
        "public_input": {
            "working_hypothesis_not_ratification": True,
            "bytes": 1164350,
            "whitespace_words": 157921,
            "token_proxy_range_not_confidence_interval": [205298, 291088],
            "sha256": "f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719",
            "models_chosen": False,
            "window_comparison_available": False,
        },
        "extractor": {
            "observed_status": "PASSA_NO_CONTRATO",
            "in_contract_cases": 685,
            "in_contract_errors": 0,
            "outside_contract_paraphrases": 5,
            "outside_contract_positive_cells_recovered": 0,
            "outside_contract_positive_cells_total": 120,
            "error_upper_95_pool": 0.004980443380361299,
            "conservative_A8_ceiling_pool": 0.6192060638168921,
            "conservative_A8_ceiling_per_arm": 0.09102821015130445,
            "independence_96_errors_measured": False,
        },
        "open_blockers": [
            "validação ampliada do extrator e teto por braço",
            "escolha entre gramática estrita e novo extrator para prosa livre",
            "independência/dependência dos 96 erros",
            "léxico isomorfo e perturbações congelados",
            "modelos, tokenizers, janelas e orçamento de 12 interações",
            "textos/controles e dificuldade medida",
            "manifesto final, hashes e custódia",
            "ratificação da R3 inteira pelo operador",
        ],
    }
    analysis_bytes = encoded(analysis)
    (HERE / "manifesto_analise.json").write_bytes(analysis_bytes)
    analysis_hash = hashlib.sha256(analysis_bytes).hexdigest()

    files = [
        HERE / "simular_poder_conjunto.py",
        HERE / "simular_separacao_r3.py",
        HERE / "verificar_degrau_5sigma.py",
        HERE / "gerar_manifestos.py",
        HERE / "resultados_poder.json",
        HERE / "separacao_r3.json",
        HERE / "degrau_5sigma.json",
        HERE / "poder_conjunto.log",
        HERE / "separacao_r3.log",
        HERE / "degrau_5sigma.log",
        K06 / "extratores" / "resultados.json",
        K06 / "extratores" / "RELATORIO_EXTRAORES.md",
        K06 / "extratores" / "manifesto.json",
        K06 / "ENTRADA_PUBLICA" / "MEDIDA_ENTRADA_PUBLICA_K06.json",
        K06 / "CONTAMINACAO" / "VALIDACAO_SINTETICA_ISOMORFO.json",
        K06 / "CONTAMINACAO" / "VALIDACAO_SINTETICA_PONTO_FIXO.json",
        KIMI / "MODELO_FORMAL_R3_K06.md",
        K06 / "candidatas" / "sandbox" / "LeitorFinito.lean",
        K06 / "candidatas" / "logs" / "LeitorFinito.txt",
    ]
    artifacts = []
    for path in files:
        artifacts.append({
            "path": str(path.relative_to(KIMI)).replace("\\", "/"),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        })
    manifest = {
        "schema": "K06_R3_PODER_SHA256_V1",
        "analysis_manifest_sha256": analysis_hash,
        "manifest_does_not_hash_itself": True,
        "documents_not_included_to_avoid_circular_reference": [
            "PROTOCOLO_EXPERIMENTAL_R3_K06.md",
            "PODER_CONJUNTO_K06.md",
            "DEGRAU_5_SIGMA_K06.md",
        ],
        "artifacts": artifacts,
    }
    manifest_bytes = encoded(manifest)
    (HERE / "MANIFESTO_SHA256.json").write_bytes(manifest_bytes)
    print(f"ANALISE_SHA256 {analysis_hash}")
    print(f"MANIFESTO_SHA256 {hashlib.sha256(manifest_bytes).hexdigest()}")
    print(f"ARTIFACTS {len(artifacts)}")


if __name__ == "__main__":
    main()

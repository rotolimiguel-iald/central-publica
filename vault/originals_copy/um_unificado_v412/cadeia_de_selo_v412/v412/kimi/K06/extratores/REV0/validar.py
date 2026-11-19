#!/usr/bin/env python3
"""Validate K06 extractors, report the A8 ceiling and hash all frozen inputs.

Standard library only. No model, network, embedding, human judgment or observed
experimental result is used. Running this file writes resultados.json,
RELATORIO_EXTRAORES.md and manifesto.json deterministically in this directory.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from extratores import (
    ROOT,
    a8_from_vectors,
    canonical_record_sha256,
    canonical_text_sha256,
    extract,
    load_spec,
)

ARMS = ["T", "C1", "C2", "C3", "C4"]
ALPHA = 0.05
CELLS_A8 = 24 * 4
TARGET_ACCURACY = 0.99
MAX_PAIRWISE_GAP = 0.01
INPUT_FILES = [
    "README.md",
    "especificacao.json",
    "extratores.py",
    "gerar_casos.py",
    "validar.py",
    "casos/agregacao.json",
    "casos/casos.json",
    "casos/duplicacao.json",
]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def counts(pairs: Sequence[Tuple[int, int]]) -> Dict[str, Any]:
    tp = sum(1 for gold, pred in pairs if gold == 1 and pred == 1)
    fn = sum(1 for gold, pred in pairs if gold == 1 and pred == 0)
    tn = sum(1 for gold, pred in pairs if gold == 0 and pred == 0)
    fp = sum(1 for gold, pred in pairs if gold == 0 and pred == 1)
    n = len(pairs)
    return {
        "n": n,
        "tp": tp,
        "fn": fn,
        "tn": tn,
        "fp": fp,
        "accuracy": (tp + tn) / n if n else None,
        "sensitivity": tp / (tp + fn) if tp + fn else None,
        "specificity": tn / (tn + fp) if tn + fp else None,
    }


def binomial_cdf_at_most(x: int, n: int, p: float) -> float:
    """Stable P(X<=x), used only for the exact one-sided CP upper bound."""
    if x < 0:
        return 0.0
    if x >= n:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    logs = []
    for k in range(x + 1):
        log_comb = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        logs.append(log_comb + k * math.log(p) + (n - k) * math.log1p(-p))
    maximum = max(logs)
    return math.exp(maximum + math.log(sum(math.exp(value - maximum) for value in logs)))


def clopper_pearson_upper(errors: int, n: int, alpha: float = ALPHA) -> float:
    """Exact one-sided upper confidence limit for a binomial error rate."""
    if n <= 0:
        return 1.0
    if errors <= 0:
        return 1.0 - alpha ** (1.0 / n)
    if errors >= n:
        return 1.0
    low, high = 0.0, 1.0
    for _ in range(90):
        middle = (low + high) / 2.0
        if binomial_cdf_at_most(errors, n, middle) > alpha:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def error_limit_for_ceiling(ceiling: float) -> float:
    return 1.0 - ceiling ** (1.0 / CELLS_A8)


def zero_error_n_required(error_limit: float) -> int:
    """Minimum n with exact one-sided 95% CP upper bound below error_limit."""
    estimate = max(1, int(math.floor(math.log(ALPHA) / math.log1p(-error_limit))))
    n = max(1, estimate - 2)
    while clopper_pearson_upper(0, n) >= error_limit:
        n += 1
    while n > 1 and clopper_pearson_upper(0, n - 1) < error_limit:
        n -= 1
    return n


def ceiling_metrics(pairs: Sequence[Tuple[int, int]]) -> Dict[str, Any]:
    errors = sum(1 for gold, pred in pairs if gold == 1 and pred == 0)
    unexpected = sum(1 for gold, pred in pairs if gold == 0 and pred == 1)
    n = len(pairs)
    error_rate = errors / n if n else 1.0
    upper = clopper_pearson_upper(errors, n)
    limits = {f"{key:.2f}": error_limit_for_ceiling(key) for key in (0.99, 0.89, 0.80)}
    return {
        "n_assertion_readings": n,
        "false_negative_errors": errors,
        "unexpected_positive_errors": unexpected,
        "measured_error_rate": error_rate,
        "upper_95_error_rate": upper,
        "measured_A8_ceiling": (1.0 - error_rate) ** CELLS_A8,
        "conservative_A8_ceiling_95": (1.0 - upper) ** CELLS_A8,
        "error_limits": limits,
        "point_meets_0.89": error_rate < limits["0.89"],
        "point_meets_0.80": error_rate < limits["0.80"],
        "certified_0.89_at_95": upper < limits["0.89"],
        "certified_0.80_at_95": upper < limits["0.80"],
        "independence_assumption": "96 independent assertion-reading errors; declared algebra, not empirically established",
    }


def duplicate_pairs(texts: Sequence[str], canonical: bool) -> List[List[int]]:
    hashes = [canonical_record_sha256(text) if canonical else canonical_text_sha256(text) for text in texts]
    return [[i + 1, j + 1] for i, j in itertools.combinations(range(len(texts)), 2) if hashes[i] == hashes[j]]


def check_lumpability(matrix: Sequence[Sequence[Fraction]], classes: Dict[str, List[int]]) -> Dict[str, Any]:
    """Check exact strong lumpability and, when possible, build the quotient."""
    witnesses = []
    class_names = list(classes)
    for source_name in class_names:
        for target_name in class_names:
            totals = {
                state: sum((matrix[state][target] for target in classes[target_name]), Fraction(0))
                for state in classes[source_name]
            }
            if len(set(totals.values())) > 1:
                witnesses.append({
                    "source_class": source_name,
                    "target_class": target_name,
                    "state_probabilities": {str(state): str(value) for state, value in totals.items()},
                })
    quotient = None
    if not witnesses:
        quotient = []
        for source_name in class_names:
            representative = classes[source_name][0]
            quotient.append([
                str(sum((matrix[representative][target] for target in classes[target_name]), Fraction(0)))
                for target_name in class_names
            ])
    return {"lumpable": not witnesses, "witnesses": witnesses, "quotient": quotient, "class_order": class_names}


def run_aggregation_cases() -> Dict[str, Any]:
    payload = json.loads((ROOT / "casos" / "agregacao.json").read_text(encoding="utf-8"))
    states = payload["states"]
    state_index = {state: index for index, state in enumerate(states)}
    classes = {name: [state_index[state] for state in names] for name, names in payload["classes"].items()}
    results = []
    for case in payload["cases"]:
        matrix = [[Fraction(value) for value in row] for row in case["matrix"]]
        if len(matrix) != len(states) or any(len(row) != len(states) for row in matrix):
            raise ValueError(f"{case['id']}: invalid matrix shape")
        if any(value < 0 for row in matrix for value in row) or any(sum(row) != 1 for row in matrix):
            raise ValueError(f"{case['id']}: non-stochastic matrix")
        checked = check_lumpability(matrix, classes)
        checked.update({
            "id": case["id"],
            "expected_lumpable": case["expected_lumpable"],
            "pass": checked["lumpable"] == case["expected_lumpable"],
            "note": case["note"],
        })
        results.append(checked)
    return {"pass": all(item["pass"] for item in results), "cases": results}


def full_t_text(spec: Dict[str, Any], spaced: bool = False, comment: str = "# synthetic") -> str:
    separator = " | " if spaced else "|"
    lines = [comment]
    for item in spec["arms"]["T"]["assertions"]:
        lines.append(separator.join([
            "K06R1", item["id"], item["subject"], item["relation"], item["object"], item["status"]
        ]))
    return "\n".join(lines) + "\n"


def run_duplication_cases(spec: Dict[str, Any]) -> Dict[str, Any]:
    payload = json.loads((ROOT / "casos" / "duplicacao.json").read_text(encoding="utf-8"))
    pair_results = []
    for case in payload["pair_cases"]:
        raw = duplicate_pairs(case["texts"], canonical=False)
        canonical = duplicate_pairs(case["texts"], canonical=True)
        pair_results.append({
            "id": case["id"],
            "raw_pairs": raw,
            "canonical_pairs": canonical,
            "expected_raw_pairs": case["expected_raw_pairs"],
            "expected_canonical_pairs": case["expected_canonical_pairs"],
            "pass": raw == case["expected_raw_pairs"] and canonical == case["expected_canonical_pairs"],
        })

    a8_results = []
    for case in payload["a8_cases"]:
        variant = case["variant"]
        texts = []
        for index in range(8):
            if variant == "repeat_full_T":
                text = full_t_text(spec)
            elif variant == "layout_full_T":
                text = full_t_text(spec, spaced=index % 2 == 1, comment=f"# layout {index + 1}")
            elif variant == "distinct_full_T":
                foreign = spec["arms"]["C1"]["assertions"][index]
                foreign_line = "|".join([
                    "K06R1", foreign["id"], foreign["subject"], foreign["relation"], foreign["object"], foreign["status"]
                ])
                text = full_t_text(spec, comment=f"# distinct {index + 1}") + foreign_line + "\n"
            else:
                raise ValueError(variant)
            texts.append(text)
        vectors = [extract(text, "T", spec)["vector"] for text in texts]
        a8 = a8_from_vectors(vectors)
        final_texts = texts[4:8]
        distinct_raw = len({canonical_text_sha256(text) for text in final_texts})
        distinct_canonical = len({canonical_record_sha256(text, spec) for text in final_texts})
        admissible = distinct_raw == 4 and distinct_canonical == 4
        passed = (
            a8["A8"] == case["expected_A8"]
            and distinct_raw == case["expected_distinct_raw_in_5_8"]
            and distinct_canonical == case["expected_distinct_canonical_in_5_8"]
            and admissible == case["expected_admissible"]
        )
        a8_results.append({
            "id": case["id"],
            "A8": a8["A8"],
            "effective_perfect_readings": a8["effective_perfect_readings"],
            "distinct_raw_in_5_8": distinct_raw,
            "distinct_canonical_in_5_8": distinct_canonical,
            "duplication_admissible": admissible,
            "expected_admissible": case["expected_admissible"],
            "pass": passed,
            "note": case["note"],
        })
    return {
        "pass": all(item["pass"] for item in pair_results + a8_results),
        "pair_cases": pair_results,
        "a8_cases": a8_results,
    }


def maximum_gaps(arm_results: Dict[str, Any]) -> Dict[str, float]:
    gaps = {}
    for metric in ("accuracy", "sensitivity", "specificity"):
        values = [arm_results[arm]["overall"][metric] for arm in ARMS]
        gaps[metric] = max(values) - min(values)
    return gaps


def build_manifest() -> Tuple[Dict[str, Any], str]:
    files = []
    for relative in sorted(INPUT_FILES):
        payload = (ROOT / relative).read_bytes()
        files.append({"path": relative, "bytes": len(payload), "sha256": sha256_bytes(payload)})
    manifest = {
        "schema": "K06_EXTRACTOR_MANIFEST_V1",
        "hash_algorithm": "SHA-256",
        "deterministic": True,
        "network_used": False,
        "model_calls": 0,
        "reserved_material_used": False,
        "reproduce": "python -B -X utf8 validar.py",
        "files": files,
    }
    write_json(ROOT / "manifesto.json", manifest)
    manifest_hash = sha256_bytes((ROOT / "manifesto.json").read_bytes())
    return manifest, manifest_hash


def pct(value: float | None) -> str:
    if value is None:
        return "NA"
    return f"{100 * value:.6f}%"


def num(value: float | None, digits: int = 9) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def yes(value: bool) -> str:
    return "SIM" if value else "NÃO"


def render_report(results: Dict[str, Any], spec: Dict[str, Any]) -> str:
    lines: List[str] = []
    add = lines.append
    add("# RELATÓRIO DOS EXTRATORES K06 — código, bateria sintética e teto de A8")
    add("")
    add("## 1. Veredito e escopo")
    add("")
    add(f"- [REAL] **Bateria observada no contrato:** {results['observed_status']}.")
    add(f"- [REAL] **Estado para produção:** **{results['production_status']}**.")
    add(f"- [REAL] Casos no contrato: {results['battery']['in_contract_cases']}; diagnósticos fora do contrato: {results['battery']['diagnostic_cases']}; total: {results['battery']['total_cases']}.")
    add(f"- [REAL] Erros próprios no contrato: {results['failure_summary']['own']}; erros cruzados: {results['failure_summary']['cross']}; divergências `E_T=E_TGL`: {results['cross']['identity_mismatches']}.")
    add("- [REAL] Nenhum modelo foi chamado; nenhum resultado experimental foi aberto; não houve juiz-LLM, embeddings, rede ou material reservado.")
    add("- [DECLARADO] O domínio validado é a gramática estruturada congelada. Paráfrase livre fora dessa gramática não é silenciosamente promovida a domínio válido.")
    for reason in results["production_blockers"]:
        add(f"- **Bloqueio:** {reason}")
    add("")
    add("## 2. Gramática, equivalência funcional e vetores-alvo")
    add("")
    add("Registro único: `K06R1|ID|SUBJECT|RELATION|OBJECT|STATUS`. Todos os braços usam o mesmo motor, seis campos, 24 tuplas, ordem de vetor congelada e as mesmas regras de falha. Duplicata idêntica colapsa; conflito no mesmo ID zera a asserção; prosa não estruturada invalida a superfície; truncamento perde a asserção; registro estrangeiro não contamina o próprio.")
    add("")
    add("Para todo `j ∈ {T,C1,C2,C3,C4}`, `τ_j=(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)`. Assim, `d_k` é a fração de asserções não satisfeitas. Em C4, 1 significa **abstenção explícita** `abstains_on|NO_CORPUS|DECLARED`; vazio continua vetor zero.")
    add("")
    add(f"A equivalência medida exige acerto por asserção ≥ {pct(TARGET_ACCURACY)}, sensibilidade/especificidade por braço ≥ {pct(TARGET_ACCURACY)} e diferença máxima entre braços ≤ {pct(MAX_PAIRWISE_GAP)}. Isso controla **rigor do extrator**, não dificuldade semântica dos textos nem poder do experimento.")
    add("")
    add("### 2.1 Lista explícita das 120 asserções")
    add("")
    for arm in ARMS:
        arm_spec = spec["arms"][arm]
        add(f"#### Braço {arm} — {arm_spec['label']}")
        add("")
        add(f"`τ_{arm} = ({','.join(str(x) for x in arm_spec['tau'])})`.")
        add("")
        add("| ID | bloco | asserção por extenso | tupla após o ID |")
        add("|---|---|---|---|")
        for item in arm_spec["assertions"]:
            tuple_text = "|".join(item[key] for key in ("subject", "relation", "object", "status"))
            add(f"| {item['id']} | {item['group']} | {item['description']} | `{tuple_text}` |")
        add("")
        if arm == "C1":
            add("Sequência-fonte sintética: `" + ",".join(arm_spec["source_tokens"]) + "`.")
            add("")
            add("Sequência-alvo embaralhada sintética: `" + ",".join(arm_spec["target_tokens"]) + "`.")
            add("")
        if arm == "C4":
            add("A abstenção precisa ser afirmada em cada uma das 24 linhas; ausência de resposta, silêncio ou um vazio não conta como `τ_C4`.")
            add("")
    add("## 3. Acerto por asserção — extratores próprios")
    add("")
    for arm in ARMS:
        result = results["own"][arm]
        add(f"### {arm}")
        add("")
        add(f"Casos={result['case_count']}; vetores 24/24 corretos={result['exact_vector_correct']}/{result['case_count']}; sensibilidade={pct(result['overall']['sensitivity'])} ({result['overall']['tp']}/{result['overall']['tp'] + result['overall']['fn']}); especificidade={pct(result['overall']['specificity'])} ({result['overall']['tn']}/{result['overall']['tn'] + result['overall']['fp']}); acerto total={pct(result['overall']['accuracy'])}.")
        add("")
        add("| asserção | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |")
        add("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for item in result["per_assertion"]:
            add(f"| {item['id']} | {item['n']} | {item['tp']} | {item['fn']} | {item['tn']} | {item['fp']} | {pct(item['accuracy'])} | {pct(item['sensitivity'])} | {pct(item['specificity'])} |")
        add("")
    add("## 4. Extrator cruzado `E_TGL` em todos os braços")
    add("")
    cross = results["cross"]
    add(f"`E_TGL(y)=E_T(y)` por chamada ao mesmo código e à mesma especificação. Total de células={cross['overall']['n']}; sensibilidade={pct(cross['overall']['sensitivity'])} ({cross['overall']['tp']}/{cross['overall']['tp'] + cross['overall']['fn']}); especificidade={pct(cross['overall']['specificity'])} ({cross['overall']['tn']}/{cross['overall']['tn'] + cross['overall']['fp']}); acerto={pct(cross['overall']['accuracy'])}.")
    add("")
    add("| asserção TGL | n | TP | FN | TN | FP | acerto | sensibilidade | especificidade |")
    add("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for item in cross["per_assertion"]:
        add(f"| {item['id']} | {item['n']} | {item['tp']} | {item['fn']} | {item['tn']} | {item['fp']} | {pct(item['accuracy'])} | {pct(item['sensitivity'])} | {pct(item['specificity'])} |")
    add("")
    add("## 5. Equivalência entre braços")
    add("")
    gaps = results["equivalence"]["maximum_metric_gaps"]
    add("| métrica | maior diferença absoluta entre braços | limite |")
    add("|---|---:|---:|")
    for metric, label in (("accuracy", "acerto"), ("sensitivity", "sensibilidade"), ("specificity", "especificidade")):
        add(f"| {label} | {pct(gaps[metric])} | {pct(MAX_PAIRWISE_GAP)} |")
    add("")
    add(f"Templates pareados presentes nos cinco braços: {results['equivalence']['paired_templates']}; templates com discordância de vetor exato: {results['equivalence']['paired_discordant_templates']}. A lista de casos e os gabaritos são homólogos por `template`; nenhum braço recebe regra mais branda para elevar sua taxa.")
    add("")
    add("## 6. Conta do teto de A8")
    add("")
    add("A8 no predicado R2 exige `d6=d7=d8=0` e `u6=u7=u8=0`; como `u6=0` e `d6=0`, também `s5=τ`. Logo são **quatro** leituras perfeitas, 5–8, e 96 células de asserção-leitura. Sob independência **declarada, não verificada**, `P(A8|leitor perfeito)=(1-e)^96`.")
    add("")
    add("| teto desejado | requisito exato em e | requisito aproximado | n necessário com zero erros para limite CP 95% abaixo do requisito |")
    add("|---:|---:|---:|---:|")
    for ceiling in (0.99, 0.89, 0.80):
        limit = error_limit_for_ceiling(ceiling)
        add(f"| {ceiling:.2f} | e < {num(limit, 12)} | e < {100 * limit:.6f}% | {zero_error_n_required(limit)} células |")
    add("")
    add("Os requisitos pedidos aparecem como `e<0,1214%` para teto ≥0,89 (portanto <0,12% em arredondamento conservador) e `e<0,2322%` para ≥0,80 (portanto <0,23%). Para o teto adicional de 0,99, a exigência é ainda mais estrita.")
    add("")
    add("| braço | células perfeitas | erros FN | e medido | CP 95% superior de e | teto medido | teto conservador 95% | ponto <0,12%? | certifica 0,89? |")
    add("|---|---:|---:|---:|---:|---:|---:|---|---|")
    for arm in ARMS + ["POOL"]:
        item = results["ceiling"][arm]
        add(f"| {arm} | {item['n_assertion_readings']} | {item['false_negative_errors']} | {pct(item['measured_error_rate'])} | {pct(item['upper_95_error_rate'])} | {num(item['measured_A8_ceiling'])} | {num(item['conservative_A8_ceiling_95'])} | {yes(item['measured_error_rate'] < error_limit_for_ceiling(0.89))} | {yes(item['certified_0.89_at_95'])} |")
    add("")
    add("A taxa pontual e a taxa certificada respondem a perguntas diferentes. Com zero erros, o teto pontual é 1; contudo, o limite superior de erro pode continuar alto demais. O estado de produção usa o critério conservador por braço, não apenas o ponto favorável.")
    add("")
    add("## 7. Falhas observadas e limites conhecidos")
    add("")
    if results["failure_summary"]["own"] == results["failure_summary"]["cross"] == 0:
        add("**Nenhuma falha de vetor foi observada nos 685 casos do contrato.** Isto não significa ausência de erro fora da bateria ou garantia estatística de `e<0,12%`.")
    else:
        add("| extrator | caso | asserção | gabarito | predito |")
        add("|---|---|---|---:|---:|")
        for failure in results["failures"][:300]:
            add(f"| {failure['extractor']} | {failure['case_id']} | {failure['assertion_id']} | {failure['gold']} | {failure['predicted']} |")
        if len(results["failures"]) > 300:
            add(f"O JSON contém todos os {len(results['failures'])} erros; a tabela foi limitada a 300 linhas.")
    add("")
    semantic = results["semantic_outside_contract"]
    add(f"Diagnóstico deliberado fora do contrato: {semantic['case_count']} casos de paráfrase inglesa semanticamente positiva; o extrator obteve {semantic['predicted_positive_cells']} de {semantic['semantic_positive_cells']} células positivas. Se a R3 permitir prosa livre, essas falhas deixam de ser diagnósticos e passam a ser falsos negativos reais.")
    add("")
    add("Falhas conhecidas fora da gramática: paráfrases, sinônimos, ordem diferente de campos, registros em prosa, caixa diferente, delimitadores Unicode, valores traduzidos e conteúdo válido misturado a explicação livre. São zeros/abstenções do instrumento, não decisões de um juiz semântico. A R3 deve impor a gramática ou um novo extrator deve ser construído e toda esta validação refeita.")
    add("")
    add("## 8. Agregação/lumpability e duplicação")
    add("")
    add("### 8.1 Lumpability exata")
    add("")
    for case in results["aggregation"]["cases"]:
        add(f"- `{case['id']}`: lumpable={yes(case['lumpable'])}; esperado={yes(case['expected_lumpable'])}; teste={'PASSA' if case['pass'] else 'FALHA'}. {case['note']}")
        if case["witnesses"]:
            for witness in case["witnesses"]:
                add(f"  - Testemunha: {witness['source_class']}→{witness['target_class']}, probabilidades `{witness['state_probabilities']}`. Sem igualdade, não se define o quociente determinístico.")
        if case["quotient"] is not None:
            add(f"  - Quociente na ordem `{case['class_order']}`: `{case['quotient']}`.")
    add("")
    add("A igualdade dos vetores extraídos no instante atual não basta para H-QUOT. No núcleo estocástico, exige-se que a probabilidade de chegar a cada classe dependa apenas da classe atual. O contraexemplo mostra uma fibra que viola essa condição; nesse caso a dinâmica permanece no espaço original.")
    add("")
    add("### 8.2 Duplicação de texto")
    add("")
    for case in results["duplication"]["pair_cases"]:
        add(f"- `{case['id']}`: pares brutos={case['raw_pairs']}; pares canônicos={case['canonical_pairs']}; teste={'PASSA' if case['pass'] else 'FALHA'}.")
    for case in results["duplication"]["a8_cases"]:
        add(f"- `{case['id']}`: A8={case['A8']}; textos brutos distintos em 5–8={case['distinct_raw_in_5_8']}/4; canônicos distintos={case['distinct_canonical_in_5_8']}/4; admissível contra duplicação={yes(case['duplication_admissible'])}. {case['note']}")
    add("")
    add("A8 aritmético e admissibilidade são campos separados. Quatro cópias podem produzir A8=1 e ainda assim ser bloqueadas pela porta de duplicação. Hashes não medem independência estocástica nem atrator.")
    add("")
    add("## 9. O que melhorar antes da produção")
    add("")
    required = zero_error_n_required(error_limit_for_ceiling(0.89))
    for arm in ARMS:
        item = results["ceiling"][arm]
        missing = max(0, required - item["n_assertion_readings"])
        add(f"- {arm}: são necessárias pelo menos {required} células perfeitas com zero erros para o limite CP 95% ficar abaixo do corte de 0,89; faltam {missing} células, equivalentes a pelo menos {math.ceil(missing / 24)} novos casos completos independentes se todos forem 24/24.")
    add("- Não preencher esse número com clones: usar casos novos, independentemente revisados, com mutações e paráfrases representativas da distribuição de saída congelada. Se houver erro após correção, refazer a validação; não diluir o erro com cópias.")
    add("- Medir dependência entre erros de asserções/leituras. A fórmula `(1-e)^96` é otimista sob agrupamento; uma conta por clusters deve substituí-la se a independência for rejeitada.")
    add("- Congelar na R3 o formato estrito e a rejeição de prosa; se texto livre for exigido, ampliar o extrator por regras determinísticas e revalidar sensibilidade/especificidade, sem LLM-juiz.")
    add("- Manter as portas de conflito, truncamento, duplicação e lumpability no escopo de integridade; falha delas produz INCONCLUSIVE_CONTROLS, não evidência a favor ou contra a teoria.")
    add("")
    add("## 10. Reprodução e manifesto")
    add("")
    add("```bat")
    add("cd /d \"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v412\\kimi\\K06\\extratores\"")
    add("python -B -X utf8 validar.py")
    add("```")
    add("")
    add(f"Manifesto SHA-256: `{results['manifest_sha256']}`. O manifesto contém os hashes e tamanhos dos oito insumos; não contém hash de si mesmo nem dos produtos que o citam, evitando referência circular. `resultados.json` contém todas as contagens e falhas sem truncamento.")
    add("")
    add("**Conclusão:** a bateria estrita pode passar sem que o instrumento esteja pronto. Enquanto a incerteza estatística e a fronteira de prosa não forem resolvidas, o estado permanece BLOQUEADO_PARA_PRODUCAO.")
    add("")
    return "\n".join(lines)


def main() -> None:
    spec = load_spec()
    battery = json.loads((ROOT / "casos" / "casos.json").read_text(encoding="utf-8"))
    cases = battery["cases"]
    contract_cases = [case for case in cases if case["metadata"]["in_contract"]]
    diagnostic_cases = [case for case in cases if not case["metadata"]["in_contract"]]

    predictions: Dict[str, Dict[str, Any]] = {}
    failures: List[Dict[str, Any]] = []
    own_pairs: Dict[str, List[Tuple[int, int]]] = {arm: [] for arm in ARMS}
    reader_pairs: Dict[str, List[Tuple[int, int]]] = {arm: [] for arm in ARMS}
    cross_pairs: List[Tuple[int, int]] = []
    exact_vectors = defaultdict(int)
    case_counts = defaultdict(int)
    identity_mismatches = 0

    for case in cases:
        arm = case["arm"]
        in_contract = case["metadata"]["in_contract"]
        own = extract(case["text"], arm, spec)
        cross = extract(case["text"], "T", spec)
        if arm == "T" and own["vector"] != cross["vector"]:
            identity_mismatches += 1
        predictions[case["id"]] = {
            "own": own["vector"],
            "cross": cross["vector"],
            "own_exact": own["vector"] == case["expected_own"],
            "arm": arm,
            "template": case["template"],
            "in_contract": in_contract,
        }
        if not in_contract:
            continue
        case_counts[arm] += 1
        exact_vectors[arm] += int(own["vector"] == case["expected_own"])
        for index, (gold, pred) in enumerate(zip(case["expected_own"], own["vector"])):
            own_pairs[arm].append((gold, pred))
            if gold != pred:
                failures.append({
                    "extractor": f"E_{arm}", "case_id": case["id"],
                    "assertion_id": spec["arms"][arm]["assertions"][index]["id"],
                    "gold": gold, "predicted": pred,
                })
        if case["reader_perfect"]:
            if case["expected_own"] != [1] * 24:
                raise ValueError(f"{case['id']}: reader-perfect gold must be 24 ones")
            reader_pairs[arm].extend(zip(case["expected_own"], own["vector"]))
        for index, (gold, pred) in enumerate(zip(case["expected_cross_tgl"], cross["vector"])):
            cross_pairs.append((gold, pred))
            if gold != pred:
                failures.append({
                    "extractor": "E_TGL", "case_id": case["id"],
                    "assertion_id": spec["arms"]["T"]["assertions"][index]["id"],
                    "gold": gold, "predicted": pred,
                })

    own_results: Dict[str, Any] = {}
    for arm in ARMS:
        per_assertion = []
        for index, item in enumerate(spec["arms"][arm]["assertions"]):
            pairs = [
                (case["expected_own"][index], predictions[case["id"]]["own"][index])
                for case in contract_cases if case["arm"] == arm
            ]
            per_assertion.append({"id": item["id"], **counts(pairs)})
        own_results[arm] = {
            "case_count": case_counts[arm],
            "exact_vector_correct": exact_vectors[arm],
            "overall": counts(own_pairs[arm]),
            "per_assertion": per_assertion,
        }

    cross_per_assertion = []
    for index, item in enumerate(spec["arms"]["T"]["assertions"]):
        pairs = [
            (case["expected_cross_tgl"][index], predictions[case["id"]]["cross"][index])
            for case in contract_cases
        ]
        cross_per_assertion.append({"id": item["id"], **counts(pairs)})
    cross_results = {
        "overall": counts(cross_pairs),
        "per_assertion": cross_per_assertion,
        "identity_mismatches": identity_mismatches,
    }

    pooled_reader = [pair for arm in ARMS for pair in reader_pairs[arm]]
    ceiling = {arm: ceiling_metrics(reader_pairs[arm]) for arm in ARMS}
    ceiling["POOL"] = ceiling_metrics(pooled_reader)

    template_map: Dict[str, Dict[str, bool]] = defaultdict(dict)
    for case in contract_cases:
        template_map[case["template"]][case["arm"]] = predictions[case["id"]]["own_exact"]
    paired = {template: values for template, values in template_map.items() if set(values) == set(ARMS)}
    discordant = sum(1 for values in paired.values() if len(set(values.values())) > 1)
    gaps = maximum_gaps(own_results)
    equivalence = {
        "maximum_metric_gaps": gaps,
        "paired_templates": len(paired),
        "paired_discordant_templates": discordant,
        "pass": all(value <= MAX_PAIRWISE_GAP for value in gaps.values()),
    }

    semantic_results = []
    for case in diagnostic_cases:
        semantic_gold = case["metadata"].get("semantic_gold_outside_contract")
        if semantic_gold is None:
            continue
        predicted = predictions[case["id"]]["own"]
        semantic_results.append({
            "case_id": case["id"], "arm": case["arm"],
            "semantic_positive_cells": sum(semantic_gold),
            "predicted_positive_cells": sum(predicted),
            "semantic_false_negatives": sum(1 for gold, pred in zip(semantic_gold, predicted) if gold == 1 and pred == 0),
        })
    semantic_summary = {
        "case_count": len(semantic_results),
        "semantic_positive_cells": sum(item["semantic_positive_cells"] for item in semantic_results),
        "predicted_positive_cells": sum(item["predicted_positive_cells"] for item in semantic_results),
        "semantic_false_negatives": sum(item["semantic_false_negatives"] for item in semantic_results),
        "cases": semantic_results,
    }

    aggregation = run_aggregation_cases()
    duplication = run_duplication_cases(spec)

    assertion_gate = all(
        item["accuracy"] is not None and item["accuracy"] >= TARGET_ACCURACY
        for arm in ARMS for item in own_results[arm]["per_assertion"]
    )
    arm_metric_gate = all(
        own_results[arm]["overall"][metric] is not None and own_results[arm]["overall"][metric] >= TARGET_ACCURACY
        for arm in ARMS for metric in ("sensitivity", "specificity")
    )
    cross_gate = (
        cross_results["overall"]["sensitivity"] >= TARGET_ACCURACY
        and cross_results["overall"]["specificity"] >= TARGET_ACCURACY
        and all(item["accuracy"] >= TARGET_ACCURACY for item in cross_per_assertion)
        and identity_mismatches == 0
    )
    observed_gate = (
        assertion_gate and arm_metric_gate and cross_gate and equivalence["pass"]
        and aggregation["pass"] and duplication["pass"]
    )
    statistical_gate = all(ceiling[arm]["certified_0.89_at_95"] for arm in ARMS)
    production_status = "APTO_SOMENTE_NO_CONTRATO" if observed_gate and statistical_gate else "BLOQUEADO_PARA_PRODUCAO"
    blockers = []
    if not observed_gate:
        blockers.append("a bateria do contrato ou uma porta de equivalência/integridade não passou")
    if not statistical_gate:
        blockers.append("o limite superior unilateral de 95% para e não certifica o teto A8≥0,89 em todos os braços")
    blockers.append("a R3 ainda deve impor a gramática estrita; fora dela, a bateria de paráfrases mostra falsos negativos")
    blockers.append("a independência dos 96 erros de asserção-leitura é hipótese algébrica e ainda precisa de teste com dados permitidos")

    manifest, manifest_hash = build_manifest()
    results = {
        "schema": "K06_EXTRACTOR_RESULTS_V1",
        "observed_status": "PASSA_NO_CONTRATO" if observed_gate else "FALHA_NO_CONTRATO",
        "production_status": production_status,
        "production_blockers": blockers,
        "battery": {
            "total_cases": len(cases), "in_contract_cases": len(contract_cases),
            "diagnostic_cases": len(diagnostic_cases),
        },
        "own": own_results,
        "cross": cross_results,
        "equivalence": equivalence,
        "ceiling": ceiling,
        "aggregation": aggregation,
        "duplication": duplication,
        "semantic_outside_contract": semantic_summary,
        "failure_summary": {
            "own": sum(1 for item in failures if item["extractor"] != "E_TGL"),
            "cross": sum(1 for item in failures if item["extractor"] == "E_TGL"),
        },
        "failures": failures,
        "gates": {
            "per_assertion_accuracy": assertion_gate,
            "arm_sensitivity_specificity": arm_metric_gate,
            "cross": cross_gate,
            "equivalence": equivalence["pass"],
            "aggregation": aggregation["pass"],
            "duplication": duplication["pass"],
            "statistical_ceiling_0.89_at_95": statistical_gate,
        },
        "manifest_sha256": manifest_hash,
    }
    write_json(ROOT / "resultados.json", results)
    (ROOT / "RELATORIO_EXTRAORES.md").write_text(render_report(results, spec), encoding="utf-8")
    summary = {
        "observed_status": results["observed_status"],
        "production_status": production_status,
        "cases": len(contract_cases),
        "own_failures": results["failure_summary"]["own"],
        "cross_failures": results["failure_summary"]["cross"],
        "cross_sensitivity": cross_results["overall"]["sensitivity"],
        "cross_specificity": cross_results["overall"]["specificity"],
        "arm_rates": {
            arm: {
                "sensitivity": own_results[arm]["overall"]["sensitivity"],
                "specificity": own_results[arm]["overall"]["specificity"],
                "error_measured": ceiling[arm]["measured_error_rate"],
                "error_upper_95": ceiling[arm]["upper_95_error_rate"],
                "A8_ceiling_measured": ceiling[arm]["measured_A8_ceiling"],
                "A8_ceiling_conservative_95": ceiling[arm]["conservative_A8_ceiling_95"],
            }
            for arm in ARMS
        },
        "manifest_sha256": manifest_hash,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

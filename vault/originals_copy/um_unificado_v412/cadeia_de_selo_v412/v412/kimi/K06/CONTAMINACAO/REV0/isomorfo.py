#!/usr/bin/env python3
"""Constrói e audita um isomorfo lexical determinístico, sem chamar modelos.

A substituição é bijetiva somente para o léxico explícito. O programa NÃO sabe
inferir que "todos os nomes e símbolos" foram cobertos: a completude exige
revisão independente e o status CONGELADO com lexicon_review.complete=true.
Nenhum texto reservado é aceito por este desenho; use somente a entrada pública.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

SCHEMA = "k06.contaminacao.dicionario-isomorfo.v1"
ALLOWED_APPLY_STATUS = {"CONGELADO", "TESTE_SINTETICO", "TESTE_SINTETICO_INVERSO"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def neutral_id(seed_id: str, source: str, collision_counter: int = 0) -> str:
    payload = f"K06/ISOMORFO/v1\0{seed_id}\0{source}\0{collision_counter}".encode("utf-8")
    return "X" + hashlib.sha256(payload).hexdigest()[:20]


def make_dictionary(terms: list[str], seed_id: str, version: str) -> dict[str, Any]:
    if not seed_id:
        raise ValueError("seed_id não pode ser vazio")
    if not terms or any(not isinstance(term, str) or not term for term in terms):
        raise ValueError("terms deve ser uma lista não vazia de strings não vazias")
    if len(set(terms)) != len(terms):
        raise ValueError("fontes duplicadas no léxico")
    entries: list[dict[str, str]] = []
    used_targets: set[str] = set()
    for source in sorted(terms, key=lambda item: item.encode("utf-8")):
        counter = 0
        target = neutral_id(seed_id, source, counter)
        while target in used_targets:
            counter += 1
            target = neutral_id(seed_id, source, counter)
        used_targets.add(target)
        entries.append({"source": source, "target": target})
    return {
        "schema": SCHEMA,
        "dictionary_version": version,
        "seed_id": seed_id,
        "status": "RASCUNHO",
        "lexicon_review": {"complete": False, "independent_reviewers": 0},
        "entries": entries,
    }


def validate_dictionary(dictionary: dict[str, Any]) -> None:
    if dictionary.get("schema") != SCHEMA:
        raise ValueError("schema de dicionário incompatível")
    status = dictionary.get("status")
    if status not in ALLOWED_APPLY_STATUS:
        raise ValueError("dicionário RASCUNHO não pode ser aplicado; falta revisão/congelamento")
    if status == "CONGELADO":
        review = dictionary.get("lexicon_review") or {}
        if review.get("complete") is not True or review.get("independent_reviewers", 0) < 2:
            raise ValueError("CONGELADO exige léxico completo e dois revisores independentes")
    entries = dictionary.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("entries vazio")
    sources = [entry.get("source") for entry in entries]
    targets = [entry.get("target") for entry in entries]
    if any(not isinstance(item, str) or not item for item in sources + targets):
        raise ValueError("fonte/alvo vazio ou inválido")
    if len(set(sources)) != len(sources) or len(set(targets)) != len(targets):
        raise ValueError("a aplicação precisa ser bijetiva: fonte e alvo únicos")
    if set(sources) & set(targets):
        raise ValueError("fonte e alvo não podem se sobrepor")
    if status != "TESTE_SINTETICO_INVERSO" and any(not re.fullmatch(r"X[0-9a-f]{20}", target) for target in targets):
        raise ValueError("alvo fora do formato neutro versionado")


def literal_regex(source: str) -> str:
    pattern = re.escape(source)
    if source[0].isalnum() or source[0] == "_":
        pattern = r"(?<!\w)" + pattern
    if source[-1].isalnum() or source[-1] == "_":
        pattern += r"(?!\w)"
    return pattern


def compiled_mapping(dictionary: dict[str, Any]) -> tuple[re.Pattern[str], dict[str, str]]:
    validate_dictionary(dictionary)
    mapping = {entry["source"]: entry["target"] for entry in dictionary["entries"]}
    ordered = sorted(mapping, key=lambda item: (-len(item.encode("utf-8")), item.encode("utf-8")))
    pattern = re.compile("|".join(literal_regex(source) for source in ordered), flags=re.UNICODE)
    return pattern, mapping


def structural_signature(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    return {
        "line_ending_sequence": re.findall(r"\r\n|\n|\r", text),
        "line_count": len(lines),
        "blank_line_positions": [index for index, line in enumerate(lines) if not line.strip()],
        "leading_whitespace": [re.match(r"[ \t]*", line).group(0) for line in lines],
        "markdown_heading_prefixes": [re.match(r"^#{1,6}(?= )", line).group(0) if re.match(r"^#{1,6}(?= )", line) else "" for line in lines],
    }


def apply_to_text(text: str, dictionary: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    pattern, mapping = compiled_mapping(dictionary)
    counts = {target: 0 for target in mapping.values()}
    unmatched_segments: list[str] = []
    output_parts: list[str] = []
    cursor = 0
    for match in pattern.finditer(text):
        unmatched_segments.append(text[cursor:match.start()])
        output_parts.append(text[cursor:match.start()])
        target = mapping[match.group(0)]
        counts[target] += 1
        output_parts.append(target)
        cursor = match.end()
    unmatched_segments.append(text[cursor:])
    output_parts.append(text[cursor:])
    output = "".join(output_parts)
    residual = pattern.search(output)
    before = structural_signature(text)
    after = structural_signature(output)
    report = {
        "dictionary_sha256": digest(dictionary),
        "dictionary_version": dictionary.get("dictionary_version"),
        "input_utf8_bytes": len(text.encode("utf-8")),
        "output_utf8_bytes": len(output.encode("utf-8")),
        "input_codepoints": len(text),
        "output_codepoints": len(output),
        "input_whitespace_words": len(re.findall(r"\S+", text)),
        "output_whitespace_words": len(re.findall(r"\S+", output)),
        "input_codepoints_div_4_proxy": math.ceil(len(text) / 4),
        "output_codepoints_div_4_proxy": math.ceil(len(output) / 4),
        "replacement_occurrences": sum(counts.values()),
        "replacement_counts_by_target": {key: value for key, value in counts.items() if value},
        "unmatched_segments_sha256": hashlib.sha256("\0".join(unmatched_segments).encode("utf-8")).hexdigest(),
        "structure_preserved": before == after,
        "residual_listed_source_count": 0 if residual is None else 1,
    }
    if residual is not None:
        raise ValueError("fonte listada residual no isomorfo")
    if not report["structure_preserved"]:
        raise ValueError("assinatura estrutural não preservada")
    return output, report


def transform_json_strings(value: Any, dictionary: dict[str, Any]) -> Any:
    """Transforma valores, preservando chaves/esquema e tipos JSON."""
    if isinstance(value, str):
        transformed, _ = apply_to_text(value, dictionary)
        return transformed
    if isinstance(value, list):
        return [transform_json_strings(item, dictionary) for item in value]
    if isinstance(value, dict):
        return {key: transform_json_strings(item, dictionary) for key, item in value.items()}
    return value


def extract_assertion_vector(text: str, specification: dict[str, Any]) -> list[int]:
    """Extrator sintético mínimo; a R3 deve substituir pelo E_j validado.

    A assinatura da função e as regras são idênticas para original e isomorfo:
    apenas a especificação lexical sofre a MESMA aplicação bijetiva.
    """
    vector: list[int] = []
    for assertion in specification.get("assertions", []):
        cursor = 0
        ordered_ok = True
        for literal in assertion.get("all_in_order", []):
            position = text.find(literal, cursor)
            if position < 0:
                ordered_ok = False
                break
            cursor = position + len(literal)
        forbidden_ok = all(literal not in text for literal in assertion.get("none", []))
        vector.append(int(ordered_ok and forbidden_ok))
    return vector


def self_test() -> dict[str, Any]:
    # Texto inventado só para teste; não é entrada, gabarito nem material reservado.
    source_text = "α introduz NomeUm. NomeUm preserva Teoria Neutra.\n\nTeoria Neutra permanece."
    terms = ["Teoria Neutra", "NomeUm", "α", "TermoProibido"]
    dictionary = make_dictionary(terms, "AUTOTESTE-SINTETICO-K06", "0-teste")
    dictionary["status"] = "TESTE_SINTETICO"
    transformed, transform_report = apply_to_text(source_text, dictionary)
    specification = {
        "assertions": [
            {"id": "A01", "all_in_order": ["α", "NomeUm"], "none": ["TermoProibido"]},
            {"id": "A02", "all_in_order": ["NomeUm", "Teoria Neutra"], "none": []},
        ]
    }
    transformed_spec = transform_json_strings(specification, dictionary)
    original_vector = extract_assertion_vector(source_text, specification)
    isomorphic_vector = extract_assertion_vector(transformed, transformed_spec)
    negative_text = "NomeUm α"
    negative_transformed, _ = apply_to_text(negative_text, dictionary)
    negative_original = extract_assertion_vector(negative_text, specification)
    negative_isomorphic = extract_assertion_vector(negative_transformed, transformed_spec)
    reverse = {
        **{key: value for key, value in dictionary.items() if key != "entries"},
        "entries": [{"source": entry["target"], "target": entry["source"]} for entry in dictionary["entries"]],
        "status": "TESTE_SINTETICO_INVERSO",
    }
    recovered, _ = apply_to_text(transformed, reverse)
    checks = {
        "text_changed": transformed != source_text,
        "round_trip_exact": recovered == source_text,
        "same_extractor_positive_vectors": original_vector == isomorphic_vector == [1, 1],
        "same_extractor_negative_vectors": negative_original == negative_isomorphic == [0, 0],
        "structure_preserved": transform_report["structure_preserved"],
        "no_residual_listed_source": transform_report["residual_listed_source_count"] == 0,
    }
    return {
        "schema": "k06.contaminacao.autoteste-sintetico.v1",
        "all_pass": all(checks.values()),
        "checks": checks,
        "dictionary_sha256": digest(dictionary),
        "transformed_specification_sha256": digest(transformed_spec),
        "original_vector": original_vector,
        "isomorphic_vector": isomorphic_vector,
        "negative_original_vector": negative_original,
        "negative_isomorphic_vector": negative_isomorphic,
        "transform_report": transform_report,
        "extractor_scope": "somente autoteste sintético; não valida os E_j da R3",
        "model_executed": False,
        "public_article_transformed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--terms", type=Path, required=True, help="JSON: lista ou objeto com campo terms")
    init.add_argument("--seed-id", required=True)
    init.add_argument("--version", required=True)
    init.add_argument("--output", type=Path, required=True)
    apply = sub.add_parser("apply")
    apply.add_argument("--input", type=Path, required=True)
    apply.add_argument("--dictionary", type=Path, required=True)
    apply.add_argument("--output", type=Path, required=True)
    apply.add_argument("--report", type=Path, required=True)
    apply.add_argument("--spec-input", type=Path)
    apply.add_argument("--spec-output", type=Path)
    test = sub.add_parser("self-test")
    test.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "init":
        raw = json.loads(args.terms.read_text(encoding="utf-8"))
        terms = raw if isinstance(raw, list) else raw.get("terms")
        dictionary = make_dictionary(terms, args.seed_id, args.version)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(pretty_bytes(dictionary))
        return
    if args.command == "self-test":
        report = self_test()
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_bytes(pretty_bytes(report))
        if not report["all_pass"]:
            raise SystemExit(1)
        return
    if args.command == "apply":
        dictionary = json.loads(args.dictionary.read_text(encoding="utf-8"))
        source_bytes = args.input.read_bytes()  # preserva bytes fora das substituições
        source_text = source_bytes.decode("utf-8", errors="strict")
        transformed, report = apply_to_text(source_text, dictionary)
        report.update({
            "input_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "output_sha256": hashlib.sha256(transformed.encode("utf-8")).hexdigest(),
            "model_executed": False,
        })
        if bool(args.spec_input) != bool(args.spec_output):
            raise ValueError("--spec-input e --spec-output devem ser fornecidos juntos")
        if args.spec_input:
            spec = json.loads(args.spec_input.read_text(encoding="utf-8"))
            transformed_spec = transform_json_strings(spec, dictionary)
            args.spec_output.parent.mkdir(parents=True, exist_ok=True)
            args.spec_output.write_bytes(pretty_bytes(transformed_spec))
            report["transformed_specification_sha256"] = digest(transformed_spec)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(transformed.encode("utf-8"))
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_bytes(pretty_bytes(report))


if __name__ == "__main__":
    main()

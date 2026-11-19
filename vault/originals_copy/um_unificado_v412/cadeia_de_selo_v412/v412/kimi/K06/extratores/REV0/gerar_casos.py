#!/usr/bin/env python3
"""Materialize the fixed synthetic K06 battery and its independent gold vectors.

This generator reads only especificacao.json. It never imports the extractor and
never calls a model. Gold vectors are assigned by the case construction rules,
not by running the code under test. Re-running reproduces byte-identical JSON.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Sequence

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "casos" / "casos.json"
ARMS = ["T", "C1", "C2", "C3", "C4"]
NEXT_ARM = {"T": "C1", "C1": "C2", "C2": "C3", "C3": "C4", "C4": "T"}
ZEROS = [0] * 24
ONES = [1] * 24


def one_hot(index: int) -> List[int]:
    vector = [0] * 24
    vector[index] = 1
    return vector


def record(item: Dict[str, str], spaced: bool = False, **overrides: str) -> str:
    fields = [
        "K06R1",
        overrides.get("id", item["id"]),
        overrides.get("subject", item["subject"]),
        overrides.get("relation", item["relation"]),
        overrides.get("object", item["object"]),
        overrides.get("status", item["status"]),
    ]
    separator = " | " if spaced else "|"
    return separator.join(fields)


def full_text(items: Sequence[Dict[str, str]], comment: str = "# Caso inteiramente sintético.", spaced: bool = False) -> str:
    return "\n".join([comment] + [record(item, spaced=spaced) for item in items]) + "\n"


def main() -> None:
    spec = json.loads((ROOT / "especificacao.json").read_text(encoding="utf-8"))
    cases: List[Dict[str, object]] = []

    def add(
        case_id: str,
        arm: str,
        category: str,
        template: str,
        text: str,
        expected_own: Sequence[int],
        expected_cross: Sequence[int] | None = None,
        reader_perfect: bool = False,
        in_contract: bool = True,
        note: str = "",
        semantic_gold: Sequence[int] | None = None,
    ) -> None:
        if arm == "T" and expected_cross is None:
            expected_cross = expected_own
        if expected_cross is None:
            expected_cross = ZEROS
        if len(expected_own) != 24 or len(expected_cross) != 24:
            raise ValueError(case_id)
        case = {
            "id": case_id,
            "arm": arm,
            "category": category,
            "template": template,
            "metadata": {
                "synthetic": True,
                "authored_for": "K06 extractor validation only",
                "reserved_source": False,
                "language": "pt-BR+English adversarial surfaces",
                "in_contract": in_contract,
                "note": note,
            },
            "text": text,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "expected_own": list(expected_own),
            "expected_cross_tgl": list(expected_cross),
            "reader_perfect": reader_perfect,
        }
        if semantic_gold is not None:
            case["metadata"]["semantic_gold_outside_contract"] = list(semantic_gold)
        cases.append(case)

    for arm in ARMS:
        items = spec["arms"][arm]["assertions"]
        plain = full_text(items)
        add(f"{arm}.full_pt", arm, "positivo", "full_pt", plain, ONES, reader_perfect=True,
            note="24 registros completos e comentário em português.")
        add(f"{arm}.full_en", arm, "positivo", "full_en",
            full_text(list(reversed(items)), comment="# Fully synthetic case; English comment, canonical records."),
            ONES, reader_perfect=True, note="Ordem inversa e comentário em inglês; gramática é independente da língua.")
        add(f"{arm}.full_spaced", arm, "positivo", "full_spaced",
            full_text(items, spaced=True), ONES, reader_perfect=True,
            note="Espaços externos aos campos são normalizados.")
        duplicated = plain + plain
        add(f"{arm}.full_duplicate", arm, "adversarial", "full_duplicate", duplicated, ONES,
            reader_perfect=True, note="Duplicação exata não infla nem derruba o vetor binário.")
        add(f"{arm}.full_markdown", arm, "positivo", "full_markdown",
            "```k06\n" + plain + "```\n", ONES, reader_perfect=True,
            note="Bloco Markdown canônico aceito.")

        partial = "\n".join([record(item) for item in items[:12]] + ["K06R1|" + items[12]["id"] + "|" + items[12]["subject"]]) + "\n"
        add(f"{arm}.partial_12", arm, "adversarial", "partial_12", partial, ONES[:12] + ZEROS[12:],
            note="Doze registros completos; décimo terceiro truncado; demais ausentes.")
        add(f"{arm}.empty", arm, "negativo", "empty", "", ZEROS,
            note="Vazio não é abstenção afirmativa, inclusive em C4.")
        prose = "\n".join(
            f"Menção sintética sem relação extraível: {item['subject']} {item['relation']} {item['object']} {item['status']}."
            for item in items
        ) + "\n"
        add(f"{arm}.prose_terms", arm, "adversarial", "prose_terms", prose, ZEROS,
            note="Cita termos sem emitir relações canônicas.")
        english = "\n".join(
            f"Synthetic English prose mentions {item['subject']} {item['relation']} {item['object']} {item['status']} without a K06 record."
            for item in items
        ) + "\n"
        add(f"{arm}.english_prose", arm, "adversarial", "english_prose", english, ZEROS,
            note="Texto inglês não estruturado é rejeitado, não traduzido por modelo.")
        paraphrase = "\n".join(
            f"The synthetic statement asserts {item['subject']} {item['relation']} {item['object']} with {item['status']}."
            for item in items
        ) + "\n"
        add(f"{arm}.diagnostic_semantic_paraphrase", arm, "diagnostico", "semantic_paraphrase",
            paraphrase, ZEROS, in_contract=False, semantic_gold=ONES,
            note="Limite conhecido: paráfrase semanticamente positiva, mas fora da gramática; não entra nas taxas do contrato.")
        others = full_text([
            dict(item, subject="Other" + item["subject"]) for item in items
        ])
        add(f"{arm}.other_names", arm, "adversarial", "other_names", others, ZEROS,
            note="Mesma forma de relação aplicada a outros nomes; zero acerto de conteúdo.")
        wrong_status = full_text([dict(item, status="ASSERTED") for item in items])
        add(f"{arm}.wrong_status", arm, "negativo", "wrong_status", wrong_status, ZEROS,
            note="Estatuto diferente do gabarito em todos os registros.")
        add(f"{arm}.negated_full", arm, "adversarial", "negated_full",
            "I do not assert these records.\n" + plain, ZEROS,
            note="Prosa não estruturada invalida a superfície inteira, impedindo aceitar registros negados no entorno.")
        add(f"{arm}.unicode_pipe", arm, "adversarial", "unicode_pipe",
            plain.replace("|", "｜"), ZEROS,
            note="Delimitador Unicode não canônico não é normalizado para passar no teste.")
        add(f"{arm}.lowercase_header", arm, "adversarial", "lowercase_header",
            plain.replace("K06R1", "k06r1"), ZEROS,
            note="Cabeçalho fora de caixa é rejeitado.")
        conflict_index = 6
        conflict_full = plain + record(items[conflict_index], object="Conflict" + items[conflict_index]["object"]) + "\n"
        expected_conflict = list(ONES)
        expected_conflict[conflict_index] = 0
        add(f"{arm}.duplicate_conflict_full", arm, "adversarial", "duplicate_conflict_full",
            conflict_full, expected_conflict,
            note="Conflito zera somente a asserção afetada; as outras 23 permanecem.")

        foreign_arm = NEXT_ARM[arm]
        foreign_items = spec["arms"][foreign_arm]["assertions"]
        foreign_cross = ONES if foreign_arm == "T" else ZEROS
        add(f"{arm}.foreign_full", arm, "adversarial", "foreign_full",
            full_text(foreign_items), ZEROS, expected_cross=foreign_cross,
            note=f"Somente registros de {foreign_arm}; o próprio {arm} não os apropria.")

        if arm != "T":
            mixed = plain + record(spec["arms"]["T"]["assertions"][0]) + "\n"
            add(f"{arm}.mixed_with_T", arm, "adversarial", "mixed_with_T", mixed, ONES,
                expected_cross=one_hot(0),
                note="Registro estrangeiro não altera o próprio; E_TGL recupera apenas T01.")
        else:
            mixed = plain + record(spec["arms"]["C1"]["assertions"][0]) + "\n"
            add(f"{arm}.mixed_with_C1", arm, "adversarial", "mixed_with_C1", mixed, ONES,
                expected_cross=ONES,
                note="Registro C1 estrangeiro não altera E_T nem E_TGL.")

        for index, item in enumerate(items):
            add(f"{arm}.single_{index+1:02d}", arm, "positivo", f"single_{index+1:02d}",
                record(item) + "\n", one_hot(index),
                note="Caso unitário positivo da asserção.")
            add(f"{arm}.wrong_object_{index+1:02d}", arm, "negativo", f"wrong_object_{index+1:02d}",
                record(item, object="Wrong" + item["object"]) + "\n", ZEROS,
                note="Objeto incorreto na asserção unitária.")
            add(f"{arm}.truncated_{index+1:02d}", arm, "adversarial", f"truncated_{index+1:02d}",
                f"K06R1|{item['id']}|{item['subject']}|{item['relation']}\n", ZEROS,
                note="Registro unitário truncado antes de objeto e estatuto.")
            conflicting = record(item) + "\n" + record(item, object="Conflict" + item["object"]) + "\n"
            add(f"{arm}.conflict_{index+1:02d}", arm, "adversarial", f"conflict_{index+1:02d}",
                conflicting, ZEROS,
                note="Duas tuplas distintas para o mesmo identificador; nenhuma é escolhida.")
            add(f"{arm}.label_only_{index+1:02d}", arm, "adversarial", f"label_only_{index+1:02d}",
                f"K06R1|{item['id']}\n", ZEROS,
                note="Rótulo sem conteúdo não satisfaz a asserção.")

    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case identifier")
    payload = {
        "schema": "K06_SYNTHETIC_CASES_V1",
        "case_count": len(cases),
        "reserved_material_used": False,
        "gold_construction": "manual deterministic construction rules in gerar_casos.py; extractor not imported",
        "cases": cases,
    }
    CASES.parent.mkdir(parents=True, exist_ok=True)
    CASES.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "path": str(CASES)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

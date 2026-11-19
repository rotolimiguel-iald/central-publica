#!/usr/bin/env python3
"""Executa somente strings sintéticas contra o extrator; nenhum modelo é chamado."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from extrator_fechado import ROTULOS, pontuar

RAIZ = Path(__file__).resolve().parent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    origem = RAIZ / "casos_sinteticos.json"
    bruto = origem.read_bytes()
    dados = json.loads(bruto.decode("utf-8"))
    resultados = []
    falhas_contrato = []
    contagens_classe = {rotulo: Counter() for rotulo in ROTULOS}

    for caso in dados["cases"]:
        score = pontuar(caso["response"], caso["assertions"])
        esperado = caso["expected_contract"]
        faltam_erros = [e for e in esperado["error_codes_required"] if e not in score["errors"]]
        contrato_ok = (
            score["format_ok"] == esperado["format_ok"]
            and score["canonical_format"] == esperado["canonical_format"]
            and not faltam_erros
        )
        if score["format_ok"]:
            contrato_ok = contrato_ok and score["correct"] == esperado["correct_count_if_parseable"]
            for item in caso["assertions"]:
                observado = score["per_id"][item["id"]]["observed"]
                contagens_classe[item["gabarito"]]["total"] += 1
                contagens_classe[item["gabarito"]]["correct"] += int(observado == item["gabarito"])
                if item["gabarito"] == "NÃO" and observado == "O TEXTO NÃO DIZ":
                    contagens_classe[item["gabarito"]]["confundido_com_silencio"] += 1
                if item["gabarito"] == "O TEXTO NÃO DIZ" and observado == "NÃO":
                    contagens_classe[item["gabarito"]]["confundido_com_negacao"] += 1
        else:
            contrato_ok = contrato_ok and score["correct"] == 0
        if not contrato_ok:
            falhas_contrato.append(caso["case_id"])
        resultados.append({
            "case_id": caso["case_id"],
            "category": caso["category"],
            "contract_ok": contrato_ok,
            "missing_expected_error_codes": faltam_erros,
            "expected_contract": esperado,
            "observed": score,
        })

    n_casos = len(resultados)
    formatos = sum(r["observed"]["format_ok"] for r in resultados)
    canonicos = sum(r["observed"]["canonical_format"] for r in resultados)
    validos_errados = [r["case_id"] for r in resultados if r["observed"]["format_ok"] and r["observed"]["correct"] < r["observed"]["total"]]
    total_valido = sum(r["observed"]["total"] for r in resultados if r["observed"]["format_ok"])
    correto_valido = sum(r["observed"]["correct"] for r in resultados if r["observed"]["format_ok"])
    total_geral = sum(r["observed"]["total"] for r in resultados)
    correto_geral = sum(r["observed"]["correct"] for r in resultados)

    metricas = {
        "schema": "k08-r4-closed-choice-metrics-v1",
        "model_calls": 0,
        "llm_judge": False,
        "case_count": n_casos,
        "contract_failures": falhas_contrato,
        "format_parseable": {
            "count": formatos,
            "rate": formatos / n_casos,
            "meaning": "Mede somente se o bloco é analisável; não mede convergência.",
        },
        "format_canonical": {"count": canonicos, "rate": canonicos / n_casos},
        "content_given_parseable": {
            "correct": correto_valido,
            "total": total_valido,
            "accuracy": correto_valido / total_valido if total_valido else None,
        },
        "joint_format_and_content": {
            "correct": correto_geral,
            "total": total_geral,
            "accuracy": correto_geral / total_geral if total_geral else None,
            "invalid_blocks_contribute_zero_correct": True,
        },
        "parseable_but_wrong_content_cases": validos_errados,
        "per_expected_label": {
            rotulo: {
                **dict(contagens_classe[rotulo]),
                "accuracy": (
                    contagens_classe[rotulo]["correct"] / contagens_classe[rotulo]["total"]
                    if contagens_classe[rotulo]["total"] else None
                ),
            }
            for rotulo in ROTULOS
        },
        "limits": [
            "Bateria sintética de desenvolvimento; não estima desempenho em saídas reais.",
            "Gabaritos são manuais e literais, mas foram escritos pelo mesmo autor dos casos; validação humana independente continua aberta.",
            "Aceitar preâmbulo elimina um falso negativo de forma, não prova compreensão.",
            "A contradição é representada por P e ¬P separados; o extrator não decide consistência lógica.",
        ],
    }

    saidas = {
        "schema": "k08-r4-closed-choice-outputs-v1",
        "source_file": origem.name,
        "source_sha256": sha256_bytes(bruto),
        "extractor_sha256": sha256_bytes((RAIZ / "extrator_fechado.py").read_bytes()),
        "results": resultados,
    }
    (RAIZ / "saidas_casos.json").write_text(json.dumps(saidas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RAIZ / "metricas_casos.json").write_text(json.dumps(metricas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    linhas = [
        "# RELATÓRIO DE CASOS — ESCOLHA FECHADA K08/R4",
        "",
        "Validação de software sobre casos sintéticos. Nenhum modelo foi executado; nenhum resultado real foi aberto.",
        "Sucesso de formato é medida de formato, não de compreensão nem de convergência.",
        "",
        "## Contrato observado",
        "",
        f"- Casos: {n_casos}; falhas do contrato esperado: {len(falhas_contrato)} ({', '.join(falhas_contrato) or 'nenhuma'}).",
        f"- Blocos analisáveis: {formatos}/{n_casos} ({formatos / n_casos:.1%}); canônicos: {canonicos}/{n_casos} ({canonicos / n_casos:.1%}).",
        f"- Conteúdo entre blocos analisáveis: {correto_valido}/{total_valido} ({correto_valido / total_valido:.1%}).",
        f"- Medida conjunta, com bloco inválido sem recuperação parcial: {correto_geral}/{total_geral} ({correto_geral / total_geral:.1%}).",
        f"- Formato válido com conteúdo errado: {', '.join(validos_errados) or 'nenhum'}.",
        "",
        "| Caso | Categoria | Formato | Canônico | Acertos | Erros | Contrato |",
        "|---|---|---:|---:|---:|---|---:|",
    ]
    for r in resultados:
        o = r["observed"]
        linhas.append(
            f"| {r['case_id']} | {r['category']} | {o['format_ok']} | {o['canonical_format']} | "
            f"{o['correct']}/{o['total']} | {', '.join(o['errors']) or '—'} | {r['contract_ok']} |"
        )
    linhas += [
        "",
        "## Leitura das taxas",
        "",
        "O caso C14 mostra que um bloco perfeito pode ter conteúdo errado. C08 e C12 mostram que preâmbulo externo e ordem diversa não zeram mais o conteúdo; ambos deixam de ser canônicos e ficam marcados como diagnóstico de forma. C04–C06 e C09–C11/C13 são falhas de contrato, não erros semânticos. C15 mostra que P e ¬P podem ser afirmados pelo mesmo texto sem criar um quarto rótulo.",
        "",
        "As taxas acima verificam a fiação e os contraexemplos escritos. Não certificam produção, sensibilidade em modelo real, compreensão, retorno ou convergência.",
        "",
    ]
    (RAIZ / "RELATORIO_CASOS.md").write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps({"cases": n_casos, "contract_failures": falhas_contrato, "format_parseable": formatos, "content_correct_parseable": correto_valido, "content_total_parseable": total_valido}, ensure_ascii=False))


if __name__ == "__main__":
    main()

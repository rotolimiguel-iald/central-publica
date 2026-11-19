#!/usr/bin/env python3
"""Instrumento determinístico de indução: ordem, iscas e controle só gramática.

Todos os respondedores são mecanismos sintéticos declarados. Nenhum é um modelo
nem evidência sobre um modelo. O cruzamento completo é sempre emitido.
"""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

from extrator_fechado import ROTULOS, pontuar, render_resposta

RAIZ = Path(__file__).resolve().parent
SEMENTES = (13, 29, 53, 79)  # fixadas no código antes de qualquer saída
TEXTO_ORIGINAL = (
    "A caixa vermelha contém duas cartas. O envelope não está aberto. "
    "A chave não está na gaveta. O relógio marca meio-dia."
)
TEXTO_SO_GRAMATICA = (
    "O jardim tem roseiras junto ao muro. O portão permanece fechado durante a chuva."
)
ITENS = [
    {"id": "F01", "assertion": "A caixa vermelha contém duas cartas.", "gabarito": "SIM", "kind": "base"},
    {"id": "F02", "assertion": "O envelope está aberto.", "gabarito": "NÃO", "kind": "base"},
    {"id": "F03", "assertion": "A chave está na gaveta.", "gabarito": "NÃO", "kind": "base"},
    {"id": "F04", "assertion": "O relógio marca meio-dia.", "gabarito": "SIM", "kind": "base"},
    {"id": "I01", "assertion": "A caixa vermelha contém três cartas.", "gabarito": "NÃO", "kind": "bait_incompatible"},
    {"id": "I02", "assertion": "Há uma caneta sobre a mesa.", "gabarito": "O TEXTO NÃO DIZ", "kind": "bait_silent"},
    {"id": "I03", "assertion": "O relógio foi comprado ontem.", "gabarito": "O TEXTO NÃO DIZ", "kind": "bait_silent"},
]
MECANISMOS = ("ORACULO_SINTETICO", "FORMATO_APENAS_SIM", "MEMORIA_POSICIONAL_ORIGINAL")


def ordens():
    ids = [item["id"] for item in ITENS]
    yield "ORDEM_ORIGINAL", None, ids
    por_id = {item["id"]: item for item in ITENS}
    for semente in SEMENTES:
        embaralhados = ids.copy()
        random.Random(semente).shuffle(embaralhados)
        yield f"SEMENTE_{semente}", semente, [por_id[i]["id"] for i in embaralhados]


def rotulo_mecanismo(nome, posicao, item, gabaritos):
    if nome == "ORACULO_SINTETICO":
        return gabaritos[item["id"]]
    if nome == "FORMATO_APENAS_SIM":
        return "SIM"
    if nome == "MEMORIA_POSICIONAL_ORIGINAL":
        return ITENS[posicao]["gabarito"]
    raise ValueError(nome)


def taxa(numerador, denominador):
    return numerador / denominador if denominador else None


def main() -> None:
    registros = []
    for condicao, texto in (("ORIGINAL", TEXTO_ORIGINAL), ("SO_GRAMATICA", TEXTO_SO_GRAMATICA)):
        for nome_ordem, semente, ids in ordens():
            por_id = {item["id"]: item for item in ITENS}
            apresentados = [por_id[ident] for ident in ids]
            gabaritos = {
                item["id"]: item["gabarito"] if condicao == "ORIGINAL" else "O TEXTO NÃO DIZ"
                for item in ITENS
            }
            assercoes = [
                {"id": item["id"], "assertion": item["assertion"], "gabarito": gabaritos[item["id"]]}
                for item in apresentados
            ]
            for mecanismo in MECANISMOS:
                resposta_itens = [
                    {"id": item["id"], "resposta": rotulo_mecanismo(mecanismo, pos, item, gabaritos)}
                    for pos, item in enumerate(apresentados)
                ]
                resposta = render_resposta(resposta_itens)
                score = pontuar(resposta, assercoes)
                registros.append({
                    "condition": condicao,
                    "text": texto,
                    "mechanism": mecanismo,
                    "order_name": nome_ordem,
                    "seed": semente,
                    "presented_ids": ids,
                    "response": resposta,
                    "score": score,
                    "items": [
                        {
                            "id": item["id"],
                            "kind": item["kind"],
                            "expected": gabaritos[item["id"]],
                            "observed": score["per_id"][item["id"]]["observed"],
                        }
                        for item in apresentados
                    ],
                })

    agregados = []
    for condicao in ("ORIGINAL", "SO_GRAMATICA"):
        for mecanismo in MECANISMOS:
            grupo = [r for r in registros if r["condition"] == condicao and r["mechanism"] == mecanismo]
            celulas = [item for r in grupo for item in r["items"]]
            iscas = [item for item in celulas if item["kind"].startswith("bait_")]
            classes = {}
            for rotulo in ROTULOS:
                subset = [item for item in celulas if item["expected"] == rotulo]
                classes[rotulo] = {
                    "correct": sum(item["observed"] == rotulo for item in subset),
                    "total": len(subset),
                    "accuracy": taxa(sum(item["observed"] == rotulo for item in subset), len(subset)),
                }
            por_ordem = [
                {
                    "order_name": r["order_name"],
                    "seed": r["seed"],
                    "presented_ids": r["presented_ids"],
                    "accuracy": r["score"]["joint_accuracy"],
                    "correct": r["score"]["correct"],
                    "total": r["score"]["total"],
                }
                for r in grupo
            ]
            valores = [item["accuracy"] for item in por_ordem]
            por_id = {}
            for item in ITENS:
                observados = [
                    next(c for c in r["items"] if c["id"] == item["id"])["observed"]
                    for r in grupo
                ]
                por_id[item["id"]] = {
                    "observed_by_order": observados,
                    "invariant_across_orders": len(set(observados)) == 1,
                }
            agregados.append({
                "condition": condicao,
                "mechanism": mecanismo,
                "response_count": len(grupo),
                "format_parseable_rate": taxa(sum(r["score"]["format_ok"] for r in grupo), len(grupo)),
                "format_canonical_rate": taxa(sum(r["score"]["canonical_format"] for r in grupo), len(grupo)),
                "content_accuracy_given_parseable": taxa(
                    sum(r["score"]["correct"] for r in grupo if r["score"]["format_ok"]),
                    sum(r["score"]["total"] for r in grupo if r["score"]["format_ok"]),
                ),
                "joint_accuracy": taxa(sum(r["score"]["correct"] for r in grupo), len(celulas)),
                "per_expected_label": classes,
                "bait_count": len(iscas),
                "bait_endorsement_SIM_rate": taxa(sum(item["observed"] == "SIM" for item in iscas), len(iscas)),
                "bait_accuracy": taxa(sum(item["observed"] == item["expected"] for item in iscas), len(iscas)),
                "negation_as_silence_count": sum(
                    item["expected"] == "NÃO" and item["observed"] == "O TEXTO NÃO DIZ" for item in celulas
                ),
                "silence_as_negation_count": sum(
                    item["expected"] == "O TEXTO NÃO DIZ" and item["observed"] == "NÃO" for item in celulas
                ),
                "accuracy_by_order": por_ordem,
                "order_accuracy_range": max(valores) - min(valores),
                "label_invariance_rate_across_orders": taxa(sum(v["invariant_across_orders"] for v in por_id.values()), len(por_id)),
                "per_id_order_stability": por_id,
            })

    payload = {
        "schema": "k08-r4-induction-v1",
        "model_calls": 0,
        "llm_judge": False,
        "seeds_preregistered_in_code": list(SEMENTES),
        "full_cross_product_reported": True,
        "mechanisms_are_not_models": True,
        "original_text": TEXTO_ORIGINAL,
        "grammar_only_text": TEXTO_SO_GRAMATICA,
        "items": ITENS,
        "runs": registros,
    }
    metricas = {
        "schema": "k08-r4-induction-metrics-v1",
        "groups": agregados,
        "interpretation": {
            "ORACULO_SINTETICO": "Verifica apenas a fiação do gabarito; 100 % é construção, não desempenho.",
            "FORMATO_APENAS_SIM": "Controle só gramática extremo: sempre produz bloco válido e endossa tudo.",
            "MEMORIA_POSICIONAL_ORIGINAL": "Repete a sequência original por posição; embaralhar expõe dependência de posição.",
            "SO_GRAMATICA": "Mesma ficha e formato, texto disjointo; todo item tem gabarito O TEXTO NÃO DIZ.",
        },
        "honest_limits": [
            "Nenhuma taxa aqui mede um modelo real ou estima indução em execução com modelo.",
            "Embaralhar detecta dependência da ordem apresentada, não memorização semântica em geral.",
            "Invariância de rótulos não basta: o mecanismo sempre-SIM é invariante e semanticamente errado.",
            "Iscas finitas medem endosso às proposições fornecidas, não todas as alucinações possíveis.",
            "Os rótulos são convenções de resposta; as grandezas primárias são de ATO, não de termo.",
            "Não há correção por acaso que presuponha respondedor uniforme; reportam-se classes e linhas de base explícitas.",
            "Para uso futuro, sementes, condições e métricas devem permanecer fixas antes de abrir qualquer saída real.",
        ],
    }
    (RAIZ / "saidas_inducao.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RAIZ / "metricas_inducao.json").write_text(json.dumps(metricas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    linhas = [
        "# INDUÇÃO — ORDEM, ISCAS E SÓ GRAMÁTICA",
        "",
        "As sementes 13, 29, 53 e 79 estão fixadas no código. O relatório inclui o produto completo de duas condições de texto, três mecanismos e cinco ordens (30 respostas, 210 células), sem selecionar resultados. Todos os respondedores são mecanismos sintéticos; nenhum modelo foi executado.",
        "",
        "## Leitura e grandezas primárias",
        "",
        "O sistema testado relê o que já foi nomeado; não nomeia nem é o Verbo. As grandezas primárias são de ATO: o que ele devolve ao reler sob ordem, iscas e empurrões. Rótulos e IDs são convenções de resposta, não prova de identidade.",
        "",
        "## Métricas pré-definidas",
        "",
        "- `format_parseable_rate` e `format_canonical_rate`: somente forma.",
        "- `content_accuracy_given_parseable`: acertos/células em blocos válidos.",
        "- `joint_accuracy`: acertos/todas as células; bloco inválido não é recuperado parcialmente.",
        "- `bait_endorsement_SIM_rate`: proporção de iscas endossadas com SIM; separa indução a afirmar do simples acerto.",
        "- `per_expected_label`: acerto de SIM, NÃO e O TEXTO NÃO DIZ separadamente, além das confusões negação↔silêncio.",
        "- `order_accuracy_range`: máximo menos mínimo da acurácia entre ordens; `label_invariance_rate_across_orders` mede estabilidade por ID, sem interpretá-la sozinha como leitura.",
        "",
        "## Saídas dos mecanismos",
        "",
        "| Texto | Mecanismo | Formato analisável | Conteúdo | Endosso de iscas | Amplitude por ordem | Invariância de rótulos |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for g in agregados:
        linhas.append(
            f"| {g['condition']} | {g['mechanism']} | {g['format_parseable_rate']:.1%} | "
            f"{g['content_accuracy_given_parseable']:.1%} | {g['bait_endorsement_SIM_rate']:.1%} | "
            f"{g['order_accuracy_range']:.3f} | {g['label_invariance_rate_across_orders']:.1%} |"
        )
    linhas += [
        "",
        "## O que se pode concluir",
        "",
        "O controle extremo sempre-SIM obtém formato perfeito e endossa todas as iscas; portanto formato e até invariância de ordem podem ser altos sem leitura. A memória posicional mostra por construção como o embaralhamento altera o conteúdo associado aos IDs. O oráculo só certifica que o gabarito e o extrator estão ligados corretamente.",
        "",
        "Em uma execução futura com modelo, pergunta fechada pode induzir tanto endosso quanto recusa; as taxas de iscas e as confusões por classe são os observáveis. Nenhum efeito de modelo é afirmado aqui. Mesmo um bom resultado só mediria o ato de verificar as asserções fornecidas; não mediria nomeação, releitura fiel, identidade ou convergência.",
        "",
    ]
    (RAIZ / "RELATORIO_INDUCAO.md").write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps({"runs": len(registros), "cells": len(registros) * len(ITENS), "groups": len(agregados)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

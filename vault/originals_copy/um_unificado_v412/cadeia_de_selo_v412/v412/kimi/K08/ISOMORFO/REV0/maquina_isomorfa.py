#!/usr/bin/env python3
"""Máquina de isomorfismo sintético, dicionário versionado e sem Nome.

A transformação numérica é contrafactual e documentada, nunca uma troca de
medidas reais por rótulos. Não lê artigos nem materiais fora dos JSON locais.
"""
from __future__ import annotations

import itertools
import json
import re
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

NUMERO_RE = re.compile(r"(?<![\w])\d+(?:[.,]\d+)?(?![\w])")
SINAIS_NUMERICOS_RE = re.compile(r"[¼½¾²³%‰]|\b\d+(?:[.,]\d+)?\b", re.UNICODE)


def transformacao_simples(texto: str, mapa: Mapping[str, str]) -> Tuple[str, Dict[str, int]]:
    """Substituição em uma passagem, mais-longa-primeiro, sem cascata."""
    if not mapa:
        return texto, {}
    chaves = sorted(mapa, key=lambda x: (-len(x), x))
    padrao = re.compile("|".join(re.escape(chave) for chave in chaves))
    contagens = {chave: 0 for chave in chaves}

    def substituir(match):
        chave = match.group(0)
        contagens[chave] += 1
        return mapa[chave]

    return padrao.sub(substituir, texto), contagens


def numeros(texto: str) -> List[str]:
    return NUMERO_RE.findall(texto)


def achados_numericos(texto: str, palavras: Sequence[str]) -> List[str]:
    achados = set(SINAIS_NUMERICOS_RE.findall(texto))
    if any(char.isdigit() for char in texto):
        achados.add("DIGITO_UNICODE")
    for palavra in palavras:
        if re.search(r"(?<!\w)" + re.escape(palavra) + r"(?!\w)", texto, re.IGNORECASE):
            achados.add(palavra)
    return sorted(achados)


def transformar_texto(
    texto: str, dicionario: Mapping, contrafactual: bool, exigir_numeros: bool = True
) -> Tuple[str, Dict]:
    mapa = dict(dicionario["term_map"])
    numericos = dicionario["counterfactual_numeric"]["number_map"] if contrafactual else {}
    mapa.update(numericos)
    transformado, contagens = transformacao_simples(texto, mapa)
    antes = numeros(texto)
    depois = numeros(transformado)
    if contrafactual:
        if not antes and exigir_numeros:
            raise ValueError("CONTRAFACTUAL_NUMERICO_SEM_NUMEROS")
        nao_contabilizados = [n for n in antes if n not in numericos]
        if nao_contabilizados:
            raise ValueError("NUMERO_SEM_POLITICA: " + ", ".join(nao_contabilizados))
        if any(numericos[n] not in depois for n in antes):
            raise ValueError("NUMERO_ALVO_AUSENTE")
        if set(antes) & set(depois):
            raise ValueError("NUMERO_ORIGINAL_INTACTO")
        if len(antes) != len(depois):
            raise ValueError("ESTRUTURA_NUMERICA_ALTERADA")
    if texto.count(".") != transformado.count(".") or texto.count("\n") != transformado.count("\n"):
        raise ValueError("PONTUACAO_ESTRUTURAL_ALTERADA")
    return transformado, {
        "replacement_counts": contagens,
        "numbers_before": antes,
        "numbers_after": depois,
        "all_source_numbers_changed": contrafactual and not (set(antes) & set(depois)),
        "punctuation_structure_preserved": True,
    }


def transformar_assercoes(assercoes: Sequence[Mapping], dicionario: Mapping, contrafactual: bool) -> List[Dict]:
    flips = set(dicionario["counterfactual_numeric"]["flip_atom_polarity"]) if contrafactual else set()
    saida = []
    for original in assercoes:
        item = dict(original)
        item.pop("memory_probe_gabarito_on_iso", None)
        item["assertion"], _ = transformar_texto(
            item["assertion"], dicionario, contrafactual, exigir_numeros=False
        )
        if contrafactual and item.get("atom") in flips:
            item["polarity"] = -item["polarity"]
        # O gabarito acompanha texto + asserção; não é recalculado pelo parser.
        item["gabarito"] = original["gabarito"]
        saida.append(item)
    return saida


def formula_base(fonte: Mapping, dicionario: Mapping, contrafactual: bool) -> List[Dict]:
    atom = fonte["formula_atom"]
    polaridade = fonte["base_polarity"]
    if contrafactual and atom in set(dicionario["counterfactual_numeric"]["flip_atom_polarity"]):
        polaridade = -polaridade
    return [{"atom": atom, "polarity": polaridade}]


def inserir_contradicao(fonte: Mapping) -> str:
    texto = fonte["text"]
    ancora = fonte["contradiction_after"]
    if texto.count(ancora) != 1:
        raise ValueError("ANCORA_CONTRADICAO_NAO_UNICA")
    return texto.replace(ancora, ancora + " " + fonte["contradiction_sentence"], 1)


def gabarito_sem_nome(assercoes_iso: Sequence[Mapping], formula: Sequence[Mapping]) -> List[Dict]:
    """P e ¬P afirmados => ambos os itens correspondentes recebem SIM."""
    presentes = {(x["atom"], x["polarity"]) for x in formula}
    saida = []
    for original in assercoes_iso:
        item = dict(original)
        if item.get("atom") and (item["atom"], item["polarity"]) in presentes:
            item["gabarito"] = "SIM"
        saida.append(item)
    return saida


def avaliar_formula(formula: Sequence[Mapping]) -> Dict:
    atoms = sorted({x["atom"] for x in formula})
    custos = []
    for valores in itertools.product((False, True), repeat=len(atoms)):
        atribuicao = dict(zip(atoms, valores))
        custo = sum(atribuicao[x["atom"]] != (x["polarity"] == 1) for x in formula)
        custos.append((custo, atribuicao))
    minimo = min(custo for custo, _ in custos) if custos else 0
    solucoes = [atribuicao for custo, atribuicao in custos if custo == 0]
    return {
        "atoms": atoms,
        "literals": list(formula),
        "assignment_count": len(custos),
        "min_cost": minimo,
        "zero_cost_reading_count": len(solucoes),
        "zero_cost_readings": solucoes,
        "satisfiable": bool(solucoes),
        "nome_vazio": not solucoes,
    }


def validar_reintroducoes(texto_original: str, texto_iso: str, dicionario: Mapping, contrafactual: bool) -> Dict:
    alvos = set(dicionario["term_map"].values())
    troca_bidirecional = sorted(alvos & set(dicionario["term_map"]))
    # Numa troca bidirecional, a forma também é alvo legítimo; a polaridade e
    # a distinção das asserções são verificadas separadamente pelo executor.
    chaves = [chave for chave in dicionario["term_map"] if chave not in alvos]
    if contrafactual:
        chaves += list(dicionario["counterfactual_numeric"]["number_map"])
    remanescentes = [chave for chave in chaves if chave in texto_iso]
    return {
        "source_tokens_reintroduced": remanescentes,
        "bidirectional_swap_tokens_checked_separately": troca_bidirecional,
        "lexical_disguise_ok": not remanescentes,
        "original_text_equal_iso": texto_original == texto_iso,
    }

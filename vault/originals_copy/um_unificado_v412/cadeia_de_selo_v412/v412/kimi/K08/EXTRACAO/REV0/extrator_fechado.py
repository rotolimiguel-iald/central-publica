#!/usr/bin/env python3
"""Extrator determinístico de escolha fechada K08/R4.

Não chama modelo, rede ou juiz. O resultado de formato e o resultado de
conteúdo são deliberadamente separados. Não reutiliza a gramática K06R1.
"""
from __future__ import annotations

import re
from typing import Dict, Iterable, List, Mapping, Sequence

INICIO = "INICIO_LEITURA_K08"
FIM = "FIM_LEITURA_K08"
ROTULOS = ("SIM", "NÃO", "O TEXTO NÃO DIZ")
_ROTULO_RE = r"(?:O TEXTO NÃO DIZ|SIM|NÃO)"
_REGISTRO_RE = re.compile(r"^([A-Z][A-Z0-9_]{0,31})=(" + _ROTULO_RE + r")$")


def render_resposta(itens: Sequence[Mapping[str, str]], preambulo: str = "") -> str:
    """Serializa respostas sintéticas; não é usado para atribuir gabaritos."""
    linhas = [INICIO]
    linhas.extend(f"{item['id']}={item['resposta']}" for item in itens)
    linhas.append(FIM)
    bloco = "\n".join(linhas) + "\n"
    return (preambulo + "\n" if preambulo else "") + bloco


def extrair(resposta: str, ids_esperados: Sequence[str]) -> Dict:
    """Extrai um único bloco, sem recuperar parcialmente respostas inválidas.

    A ordem dos registros e prosa fora do bloco são diagnósticos, não motivo
    para zerar conteúdo. Qualquer ambiguidade interna invalida todo o bloco.
    """
    esperados = list(ids_esperados)
    erros: List[str] = []
    detalhes: List[str] = []
    vazio = {
        "format_ok": False,
        "canonical_format": False,
        "status": "VAZIO",
        "errors": ["VAZIO"],
        "details": [],
        "answers": {},
        "outer_prose": False,
        "order_matches_prompt": False,
        "record_count": 0,
    }
    if not isinstance(resposta, str) or not resposta.strip():
        return vazio

    texto = resposta.replace("\r\n", "\n").replace("\r", "\n")
    if texto.startswith("\ufeff"):
        texto = texto[1:]
        detalhes.append("BOM_REMOVIDO_APENAS_NO_INICIO")
    linhas = texto.split("\n")
    inicios = [i for i, linha in enumerate(linhas) if linha == INICIO]
    fins = [i for i, linha in enumerate(linhas) if linha == FIM]

    if len(inicios) == 0 or len(fins) == 0:
        return {
            **vazio,
            "status": "MARCADORES_AUSENTES",
            "errors": ["MARCADORES_AUSENTES"],
            "details": detalhes,
        }
    if len(inicios) != 1 or len(fins) != 1:
        return {
            **vazio,
            "status": "BLOCOS_MULTIPLOS",
            "errors": ["BLOCOS_MULTIPLOS"],
            "details": detalhes,
            "record_count": 0,
        }
    i0, i1 = inicios[0], fins[0]
    if i0 >= i1:
        return {
            **vazio,
            "status": "ORDEM_MARCADORES_INVALIDA",
            "errors": ["ORDEM_MARCADORES_INVALIDA"],
            "details": detalhes,
        }

    fora = "\n".join(linhas[:i0] + linhas[i1 + 1 :]).strip()
    outer_prose = bool(fora)
    dentro = linhas[i0 + 1 : i1]
    respostas: Dict[str, str] = {}
    ordem: List[str] = []
    desconhecidos: List[str] = []
    duplicados: List[str] = []
    linhas_invalidas: List[str] = []
    linhas_vazias = 0

    for deslocamento, linha in enumerate(dentro, start=i0 + 2):
        if not linha.strip():
            linhas_vazias += 1
            continue
        match = _REGISTRO_RE.fullmatch(linha)
        if not match:
            linhas_invalidas.append(f"linha {deslocamento}")
            continue
        ident, rotulo = match.group(1), match.group(2)
        if ident in respostas:
            duplicados.append(ident)
            continue
        respostas[ident] = rotulo
        ordem.append(ident)
        if ident not in esperados:
            desconhecidos.append(ident)

    faltantes = [ident for ident in esperados if ident not in respostas]
    if linhas_invalidas:
        erros.append("REGISTRO_OU_ROTULO_INVALIDO")
        detalhes.append("linhas inválidas: " + ", ".join(linhas_invalidas))
    if duplicados:
        erros.append("ID_DUPLICADO")
        detalhes.append("IDs duplicados: " + ", ".join(sorted(set(duplicados))))
    if desconhecidos:
        erros.append("ID_DESCONHECIDO")
        detalhes.append("IDs desconhecidos: " + ", ".join(sorted(set(desconhecidos))))
    if faltantes:
        erros.append("ID_AUSENTE")
        detalhes.append("IDs ausentes: " + ", ".join(faltantes))

    format_ok = not erros
    order_matches = format_ok and ordem == esperados
    canonical = (
        format_ok
        and not outer_prose
        and order_matches
        and linhas_vazias == 0
        and not detalhes
    )
    status = "OK" if format_ok else "FORMATO_INVALIDO"
    return {
        "format_ok": format_ok,
        "canonical_format": canonical,
        "status": status,
        "errors": erros,
        "details": detalhes,
        "answers": respostas if format_ok else {},
        "outer_prose": outer_prose,
        "order_matches_prompt": order_matches,
        "record_count": len(ordem),
    }


def pontuar(resposta: str, assercoes: Sequence[Mapping[str, str]]) -> Dict:
    """Pontua por ID; bloco inválido não recebe acertos por recuperação parcial."""
    ids = [item["id"] for item in assercoes]
    extraido = extrair(resposta, ids)
    por_id = {}
    corretos = 0
    for item in assercoes:
        ident = item["id"]
        esperado = item["gabarito"]
        observado = extraido["answers"].get(ident) if extraido["format_ok"] else None
        correto = observado == esperado
        corretos += int(correto)
        por_id[ident] = {
            "expected": esperado,
            "observed": observado,
            "correct": correto,
        }
    total = len(assercoes)
    return {
        **extraido,
        "correct": corretos,
        "total": total,
        "accuracy_given_parseable": (corretos / total) if extraido["format_ok"] and total else None,
        "joint_accuracy": (corretos / total) if total else None,
        "per_id": por_id,
    }


def custo_leitura(rotulos: Iterable[str]) -> int:
    """Custo binário simples: número de cláusulas afirmadas não satisfeitas.

    Esta função só recebe SIM/NÃO de uma leitura já interpretada; NÃO DIZ não
    é convertido silenciosamente em erro factual.
    """
    return sum(1 for rotulo in rotulos if rotulo == "NÃO")

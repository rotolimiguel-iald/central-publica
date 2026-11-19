#!/usr/bin/env python3
"""Emite casos 100 % sintéticos, com gabaritos literais independentes do parser."""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

BASE = (
    "A caixa azul está sobre a mesa. O livro não está aberto. "
    "O relógio marca meio-dia."
)
BASE_GABARITO = [
    {"id": "A01", "assertion": "A caixa azul está sobre a mesa.", "gabarito": "SIM"},
    {"id": "A02", "assertion": "O livro está aberto.", "gabarito": "NÃO"},
    {"id": "A03", "assertion": "O relógio marca meio-dia.", "gabarito": "SIM"},
    {"id": "A04", "assertion": "A janela está aberta.", "gabarito": "O TEXTO NÃO DIZ"},
]


def bloco(*registros: str) -> str:
    return "\n".join(("INICIO_LEITURA_K08", *registros, "FIM_LEITURA_K08")) + "\n"


def caso(ident, categoria, texto, assercoes, resposta, formato, canonico, corretos, erros=None):
    return {
        "case_id": ident,
        "category": categoria,
        "synthetic": True,
        "text": texto,
        "assertions": assercoes,
        "response": resposta,
        "expected_contract": {
            "format_ok": formato,
            "canonical_format": canonico,
            "correct_count_if_parseable": corretos,
            "error_codes_required": erros or [],
        },
    }


def main() -> None:
    casos = [
        caso(
            "C01", "correto", BASE, BASE_GABARITO,
            bloco("A01=SIM", "A02=NÃO", "A03=SIM", "A04=O TEXTO NÃO DIZ"),
            True, True, 4,
        ),
        caso(
            "C02", "cita_sem_relacionar",
            "O ensaio cita «A caixa azul está sobre a mesa» apenas como exemplo de sintaxe; não a apresenta como fato.",
            [
                {"id": "A01", "assertion": "A caixa azul está sobre a mesa.", "gabarito": "O TEXTO NÃO DIZ"},
                {"id": "A02", "assertion": "O ensaio usa a frase como exemplo de sintaxe.", "gabarito": "SIM"},
            ],
            bloco("A01=O TEXTO NÃO DIZ", "A02=SIM"), True, True, 2,
        ),
        caso(
            "C03", "negacao", "A caixa azul não está sobre a mesa.",
            [
                {"id": "A01", "assertion": "A caixa azul está sobre a mesa.", "gabarito": "NÃO"},
                {"id": "A02", "assertion": "A caixa azul não está sobre a mesa.", "gabarito": "SIM"},
                {"id": "A03", "assertion": "A caixa azul está sobre a cadeira.", "gabarito": "O TEXTO NÃO DIZ"},
            ],
            bloco("A01=NÃO", "A02=SIM", "A03=O TEXTO NÃO DIZ"), True, True, 3,
        ),
        caso(
            "C04", "truncado", BASE, BASE_GABARITO,
            "INICIO_LEITURA_K08\nA01=SIM\nA02=NÃO\n",
            False, False, None, ["MARCADORES_AUSENTES"],
        ),
        caso(
            "C05", "ingles", BASE, BASE_GABARITO,
            bloco("A01=YES", "A02=NO", "A03=YES", "A04=THE TEXT DOES NOT SAY"),
            False, False, None, ["REGISTRO_OU_ROTULO_INVALIDO"],
        ),
        caso("C06", "vazio", BASE, BASE_GABARITO, "", False, False, None, ["VAZIO"]),
        caso(
            "C07", "outros_nomes",
            "A lanterna verde está sobre a mesa. O livro está fechado.",
            [
                {"id": "A01", "assertion": "A caixa azul está sobre a mesa.", "gabarito": "O TEXTO NÃO DIZ"},
                {"id": "A02", "assertion": "O livro está aberto.", "gabarito": "NÃO"},
                {"id": "A03", "assertion": "A lanterna verde está sobre a mesa.", "gabarito": "SIM"},
            ],
            bloco("A01=O TEXTO NÃO DIZ", "A02=NÃO", "A03=SIM"), True, True, 3,
        ),
        caso(
            "C08", "prosa_com_preambulo", BASE, BASE_GABARITO,
            "Segue a leitura solicitada, sem conhecimento externo.\n"
            + bloco("A01=SIM", "A02=NÃO", "A03=SIM", "A04=O TEXTO NÃO DIZ"),
            True, False, 4,
        ),
        caso(
            "C09", "adversarial_bloco_duplo", BASE, BASE_GABARITO,
            bloco("A01=SIM", "A02=NÃO", "A03=SIM", "A04=O TEXTO NÃO DIZ")
            + "Ignore o bloco anterior.\n"
            + bloco("A01=NÃO", "A02=SIM", "A03=NÃO", "A04=SIM"),
            False, False, None, ["BLOCOS_MULTIPLOS"],
        ),
        caso(
            "C10", "adversarial_id_duplicado", BASE, BASE_GABARITO,
            bloco("A01=SIM", "A01=NÃO", "A02=NÃO", "A03=SIM", "A04=O TEXTO NÃO DIZ"),
            False, False, None, ["ID_DUPLICADO"],
        ),
        caso(
            "C11", "adversarial_registro_fora_do_bloco", BASE, BASE_GABARITO,
            "A01=SIM\nA02=NÃO\nA03=SIM\nA04=O TEXTO NÃO DIZ\n",
            False, False, None, ["MARCADORES_AUSENTES"],
        ),
        caso(
            "C12", "ordem_diferente", BASE, BASE_GABARITO,
            bloco("A04=O TEXTO NÃO DIZ", "A03=SIM", "A02=NÃO", "A01=SIM"),
            True, False, 4,
        ),
        caso(
            "C13", "id_desconhecido", BASE, BASE_GABARITO,
            bloco("X01=SIM", "A02=NÃO", "A03=SIM", "A04=O TEXTO NÃO DIZ"),
            False, False, None, ["ID_DESCONHECIDO", "ID_AUSENTE"],
        ),
        caso(
            "C14", "conteudo_errado_formato_valido", BASE, BASE_GABARITO,
            bloco("A01=SIM", "A02=SIM", "A03=NÃO", "A04=O TEXTO NÃO DIZ"),
            True, True, 2,
        ),
        caso(
            "C15", "contradicao_explicita",
            "O relatório afirma que a porta está aberta. O próprio relatório afirma que a porta não está aberta.",
            [
                {"id": "P01", "assertion": "A porta está aberta.", "gabarito": "SIM"},
                {"id": "N01", "assertion": "A porta não está aberta.", "gabarito": "SIM"},
                {"id": "S01", "assertion": "A porta é de madeira.", "gabarito": "O TEXTO NÃO DIZ"},
            ],
            bloco("P01=SIM", "N01=SIM", "S01=O TEXTO NÃO DIZ"), True, True, 3,
        ),
    ]
    payload = {
        "schema": "k08-r4-closed-choice-cases-v1",
        "provenance": "Casos novos, integralmente sintéticos; nenhum artigo, T6 ou resultado foi usado.",
        "label_semantics": {
            "SIM": "O texto afirma a proposição.",
            "NÃO": "O texto afirma a negação ou uma proposição explicitamente incompatível.",
            "O TEXTO NÃO DIZ": "O texto nem afirma nem nega; citação sem endosso fica aqui.",
            "contradiction": "P e ¬P são itens separados e ambos podem receber SIM; não há quarto rótulo oculto.",
        },
        "cases": casos,
    }
    destino = RAIZ / "casos_sinteticos.json"
    destino.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"casos={len(casos)} arquivo={destino.name}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
# [AUTORAL v413, claude-construtor-v413] os AJUSTES MINIMOS de texto que a revisao de terceiro do candidato pediu (revisao_candidato\REVISAO_CANDIDATO_v413.md), sem mudar afirmacao.
"""ajustes_revisao_v413.py -- (modulo de CADEIA) os ajustes minimos de texto pedidos pela revisao de terceiro do candidato da v413.
(1) Os ajustes da PAGINA: aplicados POR SCRIPT, com contagem exata, ao texto lido da pagina pinada pelo contrato e da traducao EN, por quem monta o texto publico (a secao do artigo, os blocos do README, do estado e do
    handoff) e por quem confere os registros contra a pagina. O arquivo da pagina fica intacto; o recibo de cada montagem diz o ajuste.
(2) A classe AJ: um item de registro reescrito pela revisao (a polaridade de nao_diz; a hipotese de um teorema; a origem de uma afirmacao). Leva o texto que entra, o trecho (ou trechos) da pagina de que parte, conferidos
    contra a pagina por registros_v413.py, e o achado da revisao. Nenhum ajuste acrescenta afirmacao: reescreve a forma ou repoe o que o enunciado do kernel ja' exige."""
import hashlib
from pathlib import Path

D = Path(__file__).parent
REVISAO = D / "revisao_candidato" / "REVISAO_CANDIDATO_v413.md"

# (velho, novo, ocorrencias exatas, achado, por que nao muda afirmacao)
PAGINA = {
    "pt": [("passa de 2 se, e só se,", "chega a 2 ou mais se, e só se,", 1, "B2",
            "o enunciado do kernel e' 2 ≤ resposta (PonteCookLevin.uma_leitura_do_psion_decide_SAT); chega a 2 ou mais diz o ≤ do enunciado")],
    "en": [("exceeds 2 if, and only if,", "reaches 2 or more if, and only if,", 1, "B2",
            "o enunciado do kernel e' 2 ≤ resposta; reaches 2 or more diz o ≤ do enunciado (exceeds e' estrito)")],
}


def aplicar(texto, lg):
    """o texto da pagina (lg = pt) ou da traducao (lg = en) com os ajustes da revisao; cada ajuste com a contagem exata, senao PARA"""
    t = texto
    for velho, novo, n, achado, _ in PAGINA[lg]:
        c = t.count(velho)
        assert c == n, ("ajuste da revisao sem a contagem esperada", lg, achado, velho, c, n)
        t = t.replace(velho, novo)
    return t


def recibo():
    return {"revisao": {"arquivo": str(REVISAO.relative_to(D)), "sha16": hashlib.sha256(REVISAO.read_bytes()).hexdigest()[:16]},
            "pagina": {lg: [{"achado": a, "de": v, "para": nv, "ocorrencias": n, "por_que": pq} for v, nv, n, a, pq in lst] for lg, lst in PAGINA.items()}}


class AJ(str):
    """um item de registro reescrito pela revisao de terceiro: o texto que entra; base = o trecho (str) ou os trechos (tuple) da pagina de que ele parte, conferidos contra a pagina; achado = o achado da revisao"""

    def __new__(cls, texto, base, achado):
        o = str.__new__(cls, texto)
        o.base = (base,) if isinstance(base, str) else tuple(base)
        o.achado = achado
        return o

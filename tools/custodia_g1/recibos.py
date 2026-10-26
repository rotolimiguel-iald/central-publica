# -*- coding: utf-8 -*-
"""RECIBOS DURÁVEIS por versão (achado dos céticos, 24/10/2026: «C11 só se satisfaz com recibo do run_dir da própria execução»).

Antes, o resultado de passos que só existiam no console (os 16 FINAL rodados, a verificação do espelho) vivia no `run_dir` da execução que os
produziu e era invisível ao processo seguinte: a versão corrente nunca chegava a «nada a fazer» e um vigia agendado repetiria os 16 FINAL
(timeout de 3000 s cada). Agora cada passo que prova algo só por rodar grava `RECIBO_<passo>_<vNNN>.json` na pasta de trabalho da versão
(`work\\custodia_vNNN_<data>\\`), com os sha256 dos artefatos que o passo tocou. A marca de «já aplicado» LÊ o recibo e o confere com o
artefato de hoje (ou, na versão histórica, com o commit). Recibo ilegível é FalhaLeitura (visível), nunca «ok».

Escrita atômica com backup de BYTES (util.escrever_json). Nada aqui apaga nem reescreve recibo de outra versão."""
from . import util
from .util import FalhaLeitura


def _nome(ctx, chave):
    return "RECIBO_%s_%s.json" % (chave, ctx.versao)


def achar(ctx, chave):
    """O caminho do recibo, na pasta de trabalho forçada (--trabalho), nas pastas custodia_<vNNN>_* existentes ou em W; None se não há."""
    n = _nome(ctx, chave)
    candidatos = []
    if getattr(ctx, "_trabalho", None) is not None:
        candidatos.append(ctx._trabalho)
    candidatos += list(reversed(ctx.c.pastas_trabalho_existentes(ctx.versao)))
    for d in candidatos:
        p = d / n
        if p.is_file():
            return p
    return None


def ler(ctx, chave):
    """O recibo (dict) da versão de `ctx`, ou None. O gravado nesta execução vale de imediato (memo)."""
    m = ctx._memo.get("recibo_" + chave)
    if m is not None:
        return m
    p = achar(ctx, chave)
    if p is None:
        return None
    d = util.ler_json(p)
    if not isinstance(d, dict) or d.get("versao") != ctx.versao:
        raise FalhaLeitura("recibo %s com versão %r (esperava %s)" % (p.name, (d or {}).get("versao") if isinstance(d, dict) else None, ctx.versao))
    return d


def gravar(ctx, chave, dados):
    """Grava o recibo durável (e o deixa no memo). `dados` não leva hash digitado: só o que o passo mediu."""
    corpo = dict(dados)
    corpo.update({"recibo": chave, "versao": ctx.versao, "gravado_em": util.agora_iso()})
    try:
        corpo["pin16"] = ctx.pin16
    except FalhaLeitura:
        pass
    ctx.W.mkdir(parents=True, exist_ok=True)
    util.escrever_json(ctx.W / _nome(ctx, chave), corpo, backup=True)
    ctx._memo["recibo_" + chave] = corpo
    return corpo

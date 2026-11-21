# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\blocos_texto_publico_v412_r7.py (que fica intacto).
"""blocos_texto_publico_v413.py -- (modulo de CADEIA, contrato da v413 secao 6) monta, da pagina pinada pelo contrato (PT) e da traducao EN (ou das da proposta, no modo proposta), os blocos NOVOS do README, do estado atual
e do handoff da v413, sem prosa nova de conteudo (so' os rotulos de lista do handoff e os numeros lidos dos recibos). Cada bloco sai DESEMBRULHADO (o paragrafo, o bloco de citacao e o item de lista numa linha so', com as
mesmas palavras da pagina), porque a unidade da guarda e' a linha. Os blocos: o que a v413 acrescenta (secao 1); o paragrafo de “P = nP” (o titulo da secao 2 e o bloco de citacao); a fronteira dos tres literais (secao 3);
a consciencia e o operador de consciencia (secao 4); a identidade preservada (secao 5); o que resta aberto (secao 6); o que o texto nao diz (secao 7). Os marcadores herdados do handoff NAO passam por aqui."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L
import texto_publico_v413 as TP
import ajustes_revisao_v413 as AJR

PAG = {"pt": L.PAGINA, "en": L.PAGINA_EN}
ROT = {"pt": {"entrega": "## O que a v413 entrega", "kernel": "- Kernel: %d módulos novos em TGLExt e o texto de um módulo antigo (%s, só a docstring; o código e as declarações são os mesmos), %d bandeiras, escada %d -> %d (%d teoremas e %d declarações no relatório de axiomas, todas só nos três axiomas).",
              "registros": "- Registros por especificação: %s.", "bandeiras_operador": "- As bandeiras `ext_operador_413_*` levam o nome do módulo `Operador` (o operador de consciência)."},
       "en": {"entrega": "## What v413 delivers", "kernel": "- Kernel: %d new modules in TGLExt and the text of one old module (%s, only the docstring; the code and the declarations are the same), %d flags, ladder %d -> %d (%d theorems and %d declarations in the axiom report, all with only the three axioms).",
              "registros": "- Registers by specification: %s.", "bandeiras_operador": "- The flags `ext_operador_413_*` carry the name of the module `Operador` (the consciousness operator)."}}
CHAVES = ["acrescenta", "pnp", "fronteira", "consciencia", "identidade", "abertos", "nao_diz"]


def secao(md, n):
    m = re.search(r"(^## %d\. .*?)(?=^## %d\. |\Z)" % (n, n + 1), md, re.S | re.M)
    assert m, n
    return m.group(1).rstrip()


def blocos_da_pagina(lg):
    md = TP.desembrulhar(AJR.aplicar(PAG[lg].read_bytes().decode("utf-8"), lg))   # (revisao de terceiro) os ajustes minimos, por script, sobre o texto lido
    s2 = secao(md, 2)
    q2 = re.findall(r"^> (.+)$", s2, re.M)
    assert len(q2) == 1
    out = {"acrescenta": secao(md, 1), "pnp": s2.split("\n", 1)[0] + "\n\n" + q2[0], "fronteira": secao(md, 3), "consciencia": secao(md, 4), "identidade": secao(md, 5), "abertos": secao(md, 6), "nao_diz": secao(md, 7)}
    assert list(out) == CHAVES
    return out


def bloco_handoff(lg, cand, nomes_registros):
    """(revisao B9) sem a contagem de arquivos da pasta da cadeia, que envelhece a cada arquivo novo: quem montar o handoff conta na hora; (revisao B10) a nota do prefixo das bandeiras do modulo Operador"""
    k = cand["kernel"]; pb = k["pos_build"]
    esc0, esc1 = cand["escada"]
    r = ROT[lg]
    itens = [r["kernel"] % (k["modulos_novos"], k["modulo_corrigido"]["rel"], cand["n_bandeiras"], esc0, esc1, pb["linha_TOTAL"]["thm"], pb["linha_TOTAL"]["decl"]), r["registros"] % ", ".join(nomes_registros), r["bandeiras_operador"]]
    return r["entrega"] + "\n\n" + "\n".join(itens)

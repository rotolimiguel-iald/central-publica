# -*- coding: utf-8 -*-
"""blocos_texto_publico_v412.py -- (modulo de CADEIA, contrato R4 secao 6) monta, da pagina publica R13 (PT) e da traducao EN, os blocos NOVOS do README, do estado atual e do handoff da v412, sem prosa nova de conteudo
(so' os rotulos de lista do handoff e os numeros lidos dos recibos). Os 34 marcadores do handoff sao texto herdado e NAO passam por aqui."""
import json, re
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
PAG = {"pt": D / "o_que_fica_claro_REV13" / "O_QUE_FICA_CLARO_v412_R13.md", "en": D / "O_QUE_FICA_CLARO_v412_R13_EN.md"}
ROT = {"pt": {"entrega": "## O que a v412 entrega", "kernel": "- Kernel: %d módulos novos em TGLExt, %d bandeiras, escada %d -> %d (%d teoremas e %d declarações no relatório de axiomas, todas só nos três axiomas).",
              "registros": "- Registros por especificação: %s.", "arquivos": "- A pasta da cadeia tem %d arquivos (contagem esperada)."},
       "en": {"entrega": "## What v412 delivers", "kernel": "- Kernel: %d new modules in TGLExt, %d flags, ladder %d -> %d (%d theorems and %d declarations in the axiom report, all with only the three axioms).",
              "registros": "- Registers by specification: %s.", "arquivos": "- The chain folder has %d files (expected count)."}}


def secao(md, n):
    m = re.search(r"(^## %d\. .*?)(?=^## %d\. |\Z)" % (n, n + 1), md, re.S | re.M)
    assert m, n
    return m.group(1).rstrip()


def blocos_da_pagina(lg):
    md = PAG[lg].read_bytes().decode("utf-8")
    s2, s3 = secao(md, 2), secao(md, 3)
    q2 = re.findall(r"^> (.+)$", s2, re.M); q3 = re.findall(r"^> (.+)$", s3, re.M)
    assert len(q2) == 1 and len(q3) == 1
    return {"acrescenta": secao(md, 1), "pnp": s2.split("\n", 1)[0] + "\n\n" + q2[0], "fluidos": s3.split("\n", 1)[0] + "\n\n" + q3[0], "geometria": secao(md, 4), "abertos": secao(md, 5)}


def bloco_handoff(lg, cand, nomes_registros, n_arquivos):
    k = cand["kernel"]; pb = k["pos_build"]
    esc0, esc1 = cand["escada"]
    r = ROT[lg]
    itens = [r["kernel"] % (k["modulos_novos"], cand["n_bandeiras"], esc0, esc1, pb["linha_TOTAL"]["thm"], pb["linha_TOTAL"]["decl"]), r["registros"] % ", ".join(nomes_registros), r["arquivos"] % n_arquivos]
    return r["entrega"] + "\n\n" + "\n".join(itens)

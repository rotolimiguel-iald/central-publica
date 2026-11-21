# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_12_titulos_dos_cabecalhos_v412.py (que fica intacto).
"""Etapa 2 da v413, bloco 2b: o titulo (linha '# ...') ou a primeira frase do cabecalho de cada modulo das pedras limpas da v413, TODOS os titulos de secao do cabecalho, as secoes cujo titulo diz o que o arquivo
TIPA ou o que entra como leitura/definicao da teoria, e as secoes do que NAO esta' tipado ou NAO se afirma. Grava TITULOS_DOS_CABECALHOS_v413.json (backup de bytes do anterior). So' leitura das fontes."""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

MAN = L.ler_json(L.MANIFESTO)
out = {}
for modc in MAN["modulos_novos"]:
    mod = modc.split(".")[-1]
    t = (L.PEDRAS / (mod + ".lean")).read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    h = m.group(1) if m else ""
    mt = re.search(r"(?m)^# (.+)$", h)
    if mt:
        tit = mt.group(1).strip()
    else:
        s = re.sub(r"\s+", " ", h).strip()
        tit = (s.split(". ")[0] + ".") if s else None
    secoes = [s_.strip() for s_ in re.findall(r"(?m)^(#{2,4} .+)$", h)]
    nao = [s_ for s_ in secoes if re.search(r"N[ÃA]O|não|nao (?:est|se )", s_)]
    tipa = [s_ for s_ in secoes if re.search(r"\btipa\b|[Ll]eitura|[Dd]efini[cç]|[Ll]ei\b|INPUT|ONTO|entra", s_)]
    out[mod] = {"titulo": tit, "tem_cabecalho": bool(m), "secoes": secoes, "secoes_tipa_ou_leitura": tipa, "secoes_nao": nao, "sha256_fonte": L.sha256_arq(L.PEDRAS / (mod + ".lean"))}
L.salvar_json(L.D / "TITULOS_DOS_CABECALHOS_v413.json", {"sha16_manifesto": L.sha16_arq(L.MANIFESTO), "pedras": "insumos/pedras_limpas/TGLExt", "modulos": out})
for k in sys.argv[1:] or ["Trinity", "Operador", "AIdentidadePreservada", "APropostaDaTensao", "ONomeEBeta"]:
    v = out[k]
    print("=====", k, "|", v["titulo"])
    for s in v["secoes"]:
        print("    ", s)
print("modulos:", len(out), "| sem cabecalho:", [k for k, v in out.items() if not v["tem_cabecalho"]])

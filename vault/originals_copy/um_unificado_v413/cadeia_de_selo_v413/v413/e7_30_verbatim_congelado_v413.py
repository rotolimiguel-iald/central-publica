# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\e7_30_verbatim_congelado_v412.py (que fica intacto).
"""Etapa 2 da v413, bloco 3 (contrato da v413, secao 3): gera VERBATIM_CONGELADO_v413.json, artefato DA CADEIA (fora do programa; o um.py nao o le; fora da varredura dos insumos pinados; nao se publica nem se copia para
fora da casa). Lista os arquivos OPERADOR_19nov_* e OPERADOR_20nov_* de work\\cunhagens_13out\\ com tamanho e sha256 LIDOS de cada arquivo (bytes). Nenhum texto de fala e' copiado, lido para dentro ou transcrito aqui.
A marcacao de quais sao ordem, cunhagem ou so' operacao e' da gerencia, depois; nao segura o candidato."""
import datetime, hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import e7_lib_v413 as L

CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
rx = re.compile(r"^OPERADOR_(19|20)nov_")
achados = sorted((p for p in CUN.iterdir() if p.is_file() and rx.match(p.name)), key=lambda p: (int(rx.match(p.name).group(1)), p.name))
assert len(achados) > 0, "nenhum arquivo OPERADOR_19nov ou OPERADOR_20nov encontrado: PARAR"
itens = []
for p in achados:
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco); n += len(bloco)
    hx = h.hexdigest()
    itens.append({"nome": p.name, "dia": rx.match(p.name).group(1) + "nov", "bytes": n, "sha256": hx, "sha16": hx[:16]})
por_dia = {}
for it in itens:
    por_dia[it["dia"]] = por_dia.get(it["dia"], 0) + 1
lista_sha = hashlib.sha256("\n".join("%s %s %d" % (i["nome"], i["sha256"], i["bytes"]) for i in itens).encode("utf-8")).hexdigest()
saida = L.D / "VERBATIM_CONGELADO_v413.json"
obj = {
    "contrato": "VERBATIM_CONGELADO_v413",
    "natureza": "artefato da cadeia (registro paralelo); o um.py nao o le; nenhum texto de fala entra aqui, so' nome, tamanho e sha256 lidos de cada arquivo; fora da varredura dos insumos pinados; nao se publica nem se copia para fora da casa",
    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
    "origem": str(CUN),
    "padrao": "OPERADOR_19nov_* e OPERADOR_20nov_*",
    "contrato_da_versao": {"arquivo": L.CONTRATO.name, "sha16": L.sha16_arq(L.CONTRATO), "secao": "3"},
    "n": len(itens),
    "por_dia": por_dia,
    "sha256_da_lista": lista_sha,
    "arquivos": itens,
    "marcacao": "a marcacao de quais sao ordem, quais sao cunhagem e quais sao so' operacao e' da gerencia, depois; nao segura o candidato",
}
L.salvar_json(saida, obj)
print("n =", len(itens), por_dia, "sha256_da_lista", lista_sha[:16], "->", saida.name, saida.stat().st_size)
L.estado_bloco("3_verbatim_congelado", True, {"verbatim": saida, "gerador": L.D / "e7_30_verbatim_congelado_v413.py"},
               nota="%d arquivos OPERADOR_19nov e OPERADOR_20nov listados com tamanho e sha256 lidos; fora do programa (contrato da v413, secao 3)" % len(itens),
               proximo="guarda_frases_v413.py (controles); e7_23 (texto publico); e7_40 (recibos)", extra={"n": len(itens), "por_dia": por_dia, "sha256_da_lista": lista_sha})

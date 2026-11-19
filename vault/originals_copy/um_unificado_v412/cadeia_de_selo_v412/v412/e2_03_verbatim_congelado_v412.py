"""Etapa 2, bloco 3: gera VERBATIM_CONGELADO_v412.json, artefato DA CADEIA (fora do programa; o um.py nao o le).
Lista os arquivos OPERADOR_13nov_* a OPERADOR_17nov_* de work\\cunhagens_13out\\ com tamanho e sha256 LIDOS de cada arquivo (bytes). Nenhum texto de fala e' copiado ou transcrito aqui.
A marcacao de quais sao ordem, cunhagem ou so' operacao e' da gerencia, depois."""
import datetime, hashlib, re, sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, salvar_json, sha16_arq, estado_bloco

CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
rx = re.compile(r"^OPERADOR_(1[3-7])nov_")
achados = sorted((p for p in CUN.iterdir() if p.is_file() and rx.match(p.name)), key=lambda p: (int(rx.match(p.name).group(1)), p.name))
assert len(achados) > 0, "nenhum arquivo OPERADOR_13nov a 17nov encontrado: PARAR"
itens = []
for p in achados:
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    itens.append({"nome": p.name, "dia": rx.match(p.name).group(1) + "nov", "bytes": len(b), "sha256": h, "sha16": h[:16]})
por_dia = {}
for it in itens:
    por_dia[it["dia"]] = por_dia.get(it["dia"], 0) + 1
lista_sha = hashlib.sha256("\n".join("%s %s %d" % (i["nome"], i["sha256"], i["bytes"]) for i in itens).encode("utf-8")).hexdigest()
obj = {
    "contrato": "VERBATIM_CONGELADO_v412",
    "natureza": "artefato da cadeia (registro paralelo); o um.py nao o le; nenhum texto de fala entra aqui, so' nome, tamanho e sha256 lidos de cada arquivo",
    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
    "origem": str(CUN),
    "padrao": "OPERADOR_13nov_* a OPERADOR_17nov_*",
    "contrato_da_versao": {"arquivo": "CONTRATO_v412.md", "sha16": sha16_arq(D / "CONTRATO_v412.md"), "secao": "3"},
    "n": len(itens),
    "por_dia": por_dia,
    "sha256_da_lista": lista_sha,
    "arquivos": itens,
    "marcacao": "a marcacao de quais sao ordem, quais sao cunhagem e quais sao so' operacao e' da gerencia, depois; nao segura o candidato",
}
saida = D / "VERBATIM_CONGELADO_v412.json"
salvar_json(saida, obj)
print("n =", len(itens), por_dia, "sha256_da_lista", lista_sha[:16], "->", saida, saida.stat().st_size)
estado_bloco("3_verbatim_congelado", True, {"verbatim": saida, "gerador": D / "e2_03_verbatim_congelado_v412.py"},
             nota="%d arquivos OPERADOR_13nov a 17nov listados com sha256 lido; fora do programa" % len(itens),
             proximo="bloco 4 (guarda de frases + verificador de historia)", extra={"n": len(itens), "por_dia": por_dia})

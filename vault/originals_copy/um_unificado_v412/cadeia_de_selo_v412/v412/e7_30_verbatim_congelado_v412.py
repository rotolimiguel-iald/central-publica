# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de e5_30_verbatim_congelado_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
"""R5 (contrato R11, secao 3): gera VERBATIM_CONGELADO_v412.json, artefato DA CADEIA (fora do programa; o um.py nao o le; fora da varredura dos insumos pinados; nao se publica nem se copia para fora da casa).
Lista os arquivos OPERADOR_13nov_* a OPERADOR_18nov_* de work\\cunhagens_13out\\ com tamanho e sha256 LIDOS de cada arquivo (bytes). Nenhum texto de fala e' copiado ou transcrito aqui.
A marcacao de quais sao ordem, cunhagem ou so' operacao e' da gerencia, depois."""
import datetime, hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e7_lib_v412 import D, salvar_json, sha16_arq, estado_bloco, ler_json

CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
rx = re.compile(r"^OPERADOR_(1[3-8])nov_")
achados = sorted((p for p in CUN.iterdir() if p.is_file() and rx.match(p.name)), key=lambda p: (int(rx.match(p.name).group(1)), p.name))
assert len(achados) > 0, "nenhum arquivo OPERADOR_13nov a 18nov encontrado: PARAR"
itens = []
for p in achados:
    b = p.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    itens.append({"nome": p.name, "dia": rx.match(p.name).group(1) + "nov", "bytes": len(b), "sha256": h, "sha16": h[:16]})
por_dia = {}
for it in itens:
    por_dia[it["dia"]] = por_dia.get(it["dia"], 0) + 1
lista_sha = hashlib.sha256("\n".join("%s %s %d" % (i["nome"], i["sha256"], i["bytes"]) for i in itens).encode("utf-8")).hexdigest()
saida = D / "VERBATIM_CONGELADO_v412.json"
ant = ler_json(saida) if saida.exists() else None
conserva = None
if ant:
    a = {i["nome"]: i["sha256"] for i in ant["arquivos"]}; n = {i["nome"]: i["sha256"] for i in itens}
    conserva = {"n_anterior": len(a), "sumiram": sorted(set(a) - set(n)), "mudaram_de_bytes": sorted(k for k in a if k in n and a[k] != n[k]), "novos": len(set(n) - set(a))}
obj = {
    "contrato": "VERBATIM_CONGELADO_v412",
    "natureza": "artefato da cadeia (registro paralelo); o um.py nao o le; nenhum texto de fala entra aqui, so' nome, tamanho e sha256 lidos de cada arquivo; fora da varredura dos insumos pinados; nao se publica nem se copia para fora da casa",
    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
    "origem": str(CUN),
    "padrao": "OPERADOR_13nov_* a OPERADOR_18nov_*",
    "contrato_da_versao": {"arquivo": "CONTRATO_v412_R11.md", "sha16": sha16_arq(D / "CONTRATO_v412_R11.md"), "secao": "3"},
    "n": len(itens),
    "por_dia": por_dia,
    "sha256_da_lista": lista_sha,
    "em_relacao_a_lista_anterior_13_a_17nov": conserva,
    "arquivos": itens,
    "marcacao": "a marcacao de quais sao ordem, quais sao cunhagem e quais sao so' operacao e' da gerencia, depois; nao segura o candidato",
}
salvar_json(saida, obj)
print("n =", len(itens), por_dia, "sha256_da_lista", lista_sha[:16], "| contra a lista anterior:", conserva, "->", saida.name, saida.stat().st_size)
estado_bloco("3a_verbatim_congelado", True, {"verbatim": saida, "gerador": D / "e7_30_verbatim_congelado_v412.py"},
             nota="%d arquivos OPERADOR_13nov a 18nov listados com sha256 lido; fora do programa (resposta 7 da D224)" % len(itens),
             proximo="registros (depois do kernel)", extra={"n": len(itens), "por_dia": por_dia, "contra_a_lista_anterior": conserva})

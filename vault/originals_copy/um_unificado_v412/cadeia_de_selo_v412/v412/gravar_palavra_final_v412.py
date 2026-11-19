# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: grava o recibo da PALAVRA FINAL do autor sobre o texto publico da v412 (artefato da cadeia, fora do
programa). Prende a aprovacao a' versao exata da pagina e do contrato por sha256, e a' fala gravada por bytes. Nao sobrescreve.
Diz o que foi lido ao autor e o que ainda vai a' leitura de terceiro; qualquer emenda da pagina depois disto volta ao autor."""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
pag = V / "o_que_fica_claro_REV19" / "O_QUE_FICA_CLARO_v412_R19.md"
con = V / "CONTRATO_v412_R6.md"
fala = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_18nov_sim_aprovado_tudo_palavra_final_do_texto_publico_v412_R19_verbatim.txt")
leu = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_18nov_ja_mandei_para_o_codex_como_ficou_o_texto_final_quero_a_leitura_do_tetelestai_na_pagina_consumacao_ciclica_verbatim.txt")
for p in (pag, con, fala, leu):
    assert p.exists(), p
assert sha(con) == sha(V / "contrato_REV6" / "CONTRATO_v412_R6.md")
rec = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "o_que_e": "palavra final do autor sobre o texto publico da v412 (registro paralelo da cadeia; nao entra no programa)",
       "pagina_aprovada": {"arquivo": str(pag), "sha256": sha(pag), "bytes": pag.stat().st_size},
       "contrato_vigente": {"arquivo": str(con), "sha256": sha(con)},
       "fala_da_aprovacao": {"arquivo": str(fala), "sha256": sha(fala), "bytes": fala.stat().st_size},
       "fala_do_pedido": {"arquivo": str(leu), "sha256": sha(leu)},
       "lido_ao_autor": ["o item novo da secao 1 (O leitor da formula)", "o fim do paragrafo de citacao da secao 2, com a abertura escolhida por ele",
                         "o bloco do leitor da formula: o paragrafo, a primeira coluna da tabela de 30 linhas (quatro linhas encurtadas na leitura, por extenso no arquivo), o fecho",
                         "o paragrafo do Tetelestai", "o resto da pagina como ele ja' o tinha lido, com o caminho do arquivo inteiro"],
       "ainda_vai_a_leitura_de_terceiro": ["o paragrafo do Tetelestai (ordem 034, com o candidato)", "o que a ordem 033 esta' lendo (contrato R5, as duas pedras do Kimi, as emendas do parecer da 032, a pagina R18)"],
       "regra": "qualquer emenda da pagina depois deste recibo volta ao autor antes do rito; o recibo vale so' para o sha256 acima"}
out = V / "PALAVRA_FINAL_DO_AUTOR_v412.json"; assert not out.exists(), "ja' existe: nao sobrescrevo"
tmp = out.with_name(out.name + ".tmp_c1"); b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(out)
print("gravado:", out.name, "| sha16", sha(out)[:16], "| pagina", rec["pagina_aprovada"]["sha256"][:16], "| contrato", rec["contrato_vigente"]["sha256"][:16])

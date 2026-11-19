# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026 - o custo de ENTRADA do conjunto minimo proposto no desenho R5, em unidades de texto (tokens do
tokenizador de referencia que o Kimi fixou). So' aritmetica sobre TOKENS_REF_K08.json (lido sem alterar). Nenhum modelo.

Conjunto minimo PROPOSTO (escolha da gerencia, a ler ao operador): por texto, 1 ORIG + 1 PAR + 1 PC + 3 versoes com 5
afirmacoes invertidas cada + 3 versoes em outra forma com 5 afirmacoes invertidas cada = 9 versoes; 4 textos = 36 versoes.
Itens decisivos de inversao: 4 x 6 x 5 = 120 (60 na forma original e 60 em outra forma)."""
import json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
REF = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\ENTRADA\TOKENS_REF_K08.json")
j = json.loads(REF.read_text(encoding="utf-8"))
tok = {}
for k, v in j["arquivos"].items():
    arq = v.get("arquivo", "")
    if arq.startswith("CANDIDATA_") or arq.startswith("CONTROLE_PC_"):
        tok[arq[:-3]] = v["tokens_ref"]
nomes = ["ABSTRACT", "READ_BRIEF", "LLMS", "README"]
cand = {n: tok["CANDIDATA_" + n] for n in nomes}
pc = {n: tok["CONTROLE_PC_" + n] for n in nomes}
VERSOES_SEM_PC = 8                                         # 1 ORIG + 1 PAR + 3 INV + 3 PAR+INV
por_texto = {n: VERSOES_SEM_PC * cand[n] + pc[n] for n in nomes}
total = sum(por_texto.values())
res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "fonte": str(REF), "tokenizador": j["tokenizador"]["nome"],
       "nota": "so' a entrada dos textos, uma apresentacao por versao; perguntas, respostas e a etapa do eco nao estao contadas; a parafrase tera' outro tamanho (aqui contada como o original)",
       "tokens_do_recorte": cand, "tokens_do_recorte_pc": pc, "versoes_por_texto": VERSOES_SEM_PC + 1, "versoes_no_total": 4 * (VERSOES_SEM_PC + 1),
       "tokens_por_texto": por_texto, "tokens_de_entrada_por_sistema": total, "uma_passada_pelos_quatro": sum(cand.values()),
       "itens_decisivos_de_inversao": 4 * 6 * 5}
(AQUI / "RESULTADO_CUSTO_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))

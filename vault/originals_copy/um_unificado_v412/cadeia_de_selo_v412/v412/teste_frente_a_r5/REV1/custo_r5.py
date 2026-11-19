# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026, R1 - o custo do conjunto proposto no desenho R5, em unidades de texto (tokens do
tokenizador de referencia que o Kimi fixou). So' aritmetica. Nenhum modelo.

Le sem alterar: TOKENS_REF_K08.json (o tamanho dos quatro recortes) e o RESULTADO_SIMULACAO_R5.json desta pasta (quantos
grupos o catalogo oferece por texto no desenho de 6 afirmacoes tocadas).

CONJUNTO PROPOSTO (escolha da gerencia, a ler ao operador): por texto, o texto-base; duas versoes complementares por
grupo de inversao; e um grupo da frase acrescentada (duas versoes). Uma apresentacao por versao.

O QUE E' MEDIDO E O QUE E' ESTIMADO: o tamanho dos textos e' medido (arquivo pinado do Kimi). O tamanho da instrucao,
de cada pergunta e de cada resposta e' ESTIMATIVA do revisor da conferencia (350, 27 e 16 unidades), nao contagem.
As versoes mexidas sao contadas com o tamanho do texto original (a reescrita pode variar para mais ou para menos).
Uso: custo_r5.py [--saida <pasta>]"""
import json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
SAIDA = Path(sys.argv[sys.argv.index("--saida") + 1]) if "--saida" in sys.argv else AQUI
REF = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\kimi\K08\ENTRADA\TOKENS_REF_K08.json")
SIM = AQUI / "RESULTADO_SIMULACAO_R5.json"
INSTRUCAO, PERGUNTA, RESPOSTA, ITENS = 350, 27, 16, 33        # estimativas (ver a docstring); 33 itens do catalogo

j = json.loads(REF.read_text(encoding="utf-8"))
tok = {v["arquivo"][:-3]: v["tokens_ref"] for v in j["arquivos"].values() if v.get("arquivo", "").startswith("CANDIDATA_")}
nomes = ["ABSTRACT", "READ_BRIEF", "LLMS", "README"]
tam = {n: tok["CANDIDATA_" + n] for n in nomes}
sim = json.loads(SIM.read_text(encoding="utf-8"))
grupos = {n: sim["desenhos"]["m3_orig"]["por_texto"][n]["grupos"] for n in nomes}
versoes = {n: 1 + 2 * grupos[n] + 2 for n in nomes}           # base + 2 por grupo de inversao + 2 da frase acrescentada
so_texto = sum(versoes[n] * tam[n] for n in nomes)
n_versoes = sum(versoes.values())
# modo A: uma chamada por versao, com as 33 perguntas juntas; modo B: uma chamada por pergunta
A_ent = so_texto + n_versoes * (INSTRUCAO + ITENS * PERGUNTA)
A_sai = n_versoes * ITENS * RESPOSTA
B_ent = sum(versoes[n] * ITENS * (tam[n] + INSTRUCAO + PERGUNTA) for n in nomes)
B_sai = A_sai
res = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "revisao": "R1", "fonte_dos_tamanhos": str(REF), "tokenizador": j["tokenizador"]["nome"],
       "nota": "tamanho dos textos medido; instrucao, pergunta e resposta ESTIMADAS (350, 27, 16); etapa do eco e repeticoes NAO contadas",
       "tamanho_do_recorte": tam, "grupos_de_inversao_por_texto": grupos, "versoes_por_texto": versoes, "versoes_no_total": n_versoes,
       "grupos_de_inversao": sum(grupos.values()), "grupos_da_frase_acrescentada": len(nomes),
       "textos_novos_a_escrever_e_conferir": n_versoes - len(nomes),
       "so_o_texto_das_versoes": so_texto,
       "modo_A_uma_chamada_por_versao": {"entrada": A_ent, "saida": A_sai, "total": A_ent + A_sai},
       "modo_B_uma_chamada_por_pergunta": {"entrada": B_ent, "saida": B_sai, "total": B_ent + B_sai}}
SAIDA.mkdir(parents=True, exist_ok=True)
(SAIDA / "RESULTADO_CUSTO_R5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))

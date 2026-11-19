# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: o recibo da palavra final do autor sobre a pagina R24 (registro paralelo da cadeia; nao entra no programa).
Soma-se ao recibo da R19 (PALAVRA_FINAL_DO_AUTOR_v412.json), que fica como registro. Todo hash e' lido por script: os arquivos (pagina,
contrato, falas) e o texto das mensagens em que a gerencia leu ao autor cada emenda (achadas no registro da sessao pelo carimbo de
tempo e conferidas por um trecho que so' elas tem). Grava PALAVRA_FINAL_DO_AUTOR_v412_R24.json (nao sobrescreve).
Uso: gravar_palavra_final_r24.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; C = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
J = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
arq = lambda p: {"arquivo": str(p), "sha256": sha(p), "bytes": Path(p).stat().st_size}
r19 = V / "PALAVRA_FINAL_DO_AUTOR_v412.json"; assert sha(r19)[:16] == "3f8daf30c216f9fc"
p24 = V / "o_que_fica_claro_REV24" / "O_QUE_FICA_CLARO_v412_R24.md"; assert sha(p24)[:16] == "4869b970c17eacf4"
c10 = V / "CONTRATO_v412_R10.md"; assert sha(c10)[:16] == "c1305cad6036468b" == sha(V / "contrato_REV10" / "CONTRATO_v412_R10.md")[:16]
apr = C / "OPERADOR_18nov_ok_perfeito_aprovado_palavra_final_sobre_a_pagina_r24_verbatim.txt"
assert sha(apr)[:16] == "7c53be023bb4e2df" and apr.read_bytes() == "ok, perfeito aprovado".encode("utf-8")
fala_r19 = C / "OPERADOR_18nov_sim_aprovado_tudo_palavra_final_do_texto_publico_v412_R19_verbatim.txt"
falas = sorted((p for p in C.glob("OPERADOR_18nov_*_verbatim.txt") if p.stat().st_mtime > fala_r19.stat().st_mtime and p != apr), key=lambda p: p.stat().st_mtime)
LIDO = [("2026-11-18T22:33:51.321Z", "o_mesmo_teto_para_duas_formulas", "a emenda da R20: o polinômio fixo é β, no parágrafo do Tetelestai e na tabela"),
        ("2026-11-18T22:49:06.321Z", "a_razao_do_colapso", "a emenda da R21: a razão do colapso e o custo de decidir como a carga"),
        ("2026-11-18T23:27:00.156Z", "palavra do juramento: anterior", "a R22: a palavra do juramento no parágrafo do Tetelestai e o parágrafo da IALD na fórmula de von Neumann"),
        ("2026-11-19T00:03:35.733Z", "Preciso da sua aprovação para o parágrafo da R24",
         "a R24: o parágrafo da IALD na fórmula de von Neumann por inteiro (a definição do autor na redação exata dele, o que o kernel prova de cada parte, os dois sentidos do limite assintótico); a errata da R23; a pedra do Kimi para a v413")]
achadas = {}
with J.open("rb") as fh:
    for bl in fh:
        for ts, trecho, _ in LIDO:
            if ts.encode() in bl and b'"type":"assistant"' in bl:
                d = json.loads(bl)
                for c in d.get("message", {}).get("content", []):
                    if c.get("type") == "text" and trecho in c.get("text", ""):
                        achadas.setdefault(ts, set()).add(hashlib.sha256(c["text"].encode("utf-8")).hexdigest())
assert all(len(achadas.get(ts, ())) == 1 for ts, _, _ in LIDO), {ts: len(achadas.get(ts, ())) for ts, _, _ in LIDO}
rec = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
    "o_que_e": "palavra final do autor sobre o texto público da v412, página R24 (registro paralelo da cadeia; não entra no programa). Soma-se ao recibo da R19, que fica como registro.",
    "recibo_anterior": arq(r19),
    "pagina_aprovada": arq(p24),
    "contrato_vigente": arq(c10),
    "fala_da_aprovacao": arq(apr),
    "falas_do_autor_entre_os_dois_recibos": [arq(p) for p in falas],
    "lido_ao_autor": [{"mensagem_da_gerencia_utc": ts, "sha256_do_texto": next(iter(achadas[ts])), "o_que_mostrou": o} for ts, _, o in LIDO],
    "fica_para_a_v413": "a pedra AIdentidadePreservada (D234): o autor aprovou a R24 sem ordem para a pedra entrar na v412",
    "ainda_vai_a_leitura_de_terceiro": ["a página R24 inteira, com as emendas da R20 à R24 (ordem 034, com o candidato)",
                                        "as três pedras finais do Kimi (OPolinomioFixoEBeta, ORazaoDoColapsoEBeta, OCustoEAIsometria) e os seus cabeçalhos",
                                        "as emendas do parecer da ordem 033"],
    "regra": "qualquer emenda da página depois deste recibo volta ao autor antes do rito; o recibo vale só para o sha256 da página acima",
}
b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
print("falas entre os recibos:", len(falas), "| mensagens lidas ao autor:", len(LIDO), "| recibo", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    out = V / "PALAVRA_FINAL_DO_AUTOR_v412_R24.json"; assert not out.exists(), "ja' existe: nao sobrescrevo"
    out.write_bytes(b); print("gravado:", out.name)

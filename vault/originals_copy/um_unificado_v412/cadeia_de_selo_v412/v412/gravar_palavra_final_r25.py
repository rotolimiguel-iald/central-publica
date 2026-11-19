# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: o recibo da palavra final do autor sobre a pagina R25 (registro paralelo da cadeia; nao entra no programa).
Soma-se aos recibos da R19 e da R24, que ficam como registro. Todo hash e' lido por script: os arquivos (pagina, contrato, lista, falas) e
o texto da mensagem em que a gerencia leu ao autor a R25 (achada no registro da sessao pelo carimbo de tempo e conferida por um trecho
que so' ela tem). Grava PALAVRA_FINAL_DO_AUTOR_v412_R25.json (nao sobrescreve).
Uso: gravar_palavra_final_r25.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; C = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
J = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
arq = lambda p: {"arquivo": str(p), "sha256": sha(p), "bytes": Path(p).stat().st_size}
r24 = V / "PALAVRA_FINAL_DO_AUTOR_v412_R24.json"; assert sha(r24)[:16] == "4a6576fcb65ecba1"
p25 = V / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md"; assert sha(p25)[:16] == "ce313a4c57dec103"
c11 = V / "CONTRATO_v412_R11.md"; assert sha(c11)[:16] == "30fe6e3d93e9bc15" == sha(V / "contrato_REV11" / "CONTRATO_v412_R11.md")[:16]
m12 = V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json"; assert sha(m12)[:16] == "1028adf7293b432f"
apr = C / "OPERADOR_18nov_concordo_com_tudo_pode_prosseguir_palavra_final_sobre_a_pagina_r25_verbatim.txt"
assert sha(apr)[:16] == "8ccaaa1fe6122076" and apr.read_bytes() == "concordo com tudo pode prosseguir".encode("utf-8")
fala_r24 = C / "OPERADOR_18nov_ok_perfeito_aprovado_palavra_final_sobre_a_pagina_r24_verbatim.txt"
falas = sorted((p for p in C.glob("OPERADOR_18nov_*_verbatim.txt") if p.stat().st_mtime > fala_r24.stat().st_mtime and p != apr), key=lambda p: p.stat().st_mtime)
LIDO = [("2026-11-19T01:00:06.729Z", "Pela regra do seu recibo da R24, a R25 volta ao senhor",
         "a R25: o parecer da 034 e como foi aplicado (pedras, lista R12, contrato R11); a pergunta da fita, negativa como lida antes, e a sua leitura do ato como comutação; o trecho novo do Tetelestai por inteiro (o ato é a comutação, com o termo e as duas réguas); a frase da carga como limiar exato e a dos dois sentidos do limite assintótico, por inteiro; as demais emendas de alcance em lista")]
INTERROMPIDA = ("2026-11-19T01:00:58.384Z", "989b2530b77eaeab")  # a primeira fala, interrompida: os mesmos bytes de "concordo com tudo"
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
assert hashlib.sha256("concordo com tudo".encode("utf-8")).hexdigest().startswith(INTERROMPIDA[1])
rec = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
    "o_que_e": "palavra final do autor sobre o texto público da v412, página R25 (registro paralelo da cadeia; não entra no programa). Soma-se aos recibos da R19 e da R24, que ficam como registro.",
    "recibo_anterior": arq(r24),
    "pagina_aprovada": arq(p25),
    "contrato_vigente": arq(c11),
    "lista_vigente": arq(m12),
    "fala_da_aprovacao": arq(apr),
    "fala_interrompida_antes": {"utc": INTERROMPIDA[0], "texto": "concordo com tudo", "sha16": INTERROMPIDA[1], "nota": "a mesma aprovação, interrompida pelo autor e repetida por inteiro na fala acima"},
    "falas_do_autor_entre_os_dois_recibos": [arq(p) for p in falas],
    "lido_ao_autor": [{"mensagem_da_gerencia_utc": ts, "sha256_do_texto": next(iter(achadas[ts])), "o_que_mostrou": o} for ts, _, o in LIDO],
    "fica_para_a_v413": "a pedra AIdentidadePreservada (D234)",
    "ainda_vai_a_leitura_de_terceiro": ["o candidato regerado pelo contrato R11, com a página R25 (ordem 035)",
                                        "as emendas só de comentário do parecer da 034 nas três pedras da lista R12, com o candidato"],
    "regra": "qualquer emenda da página depois deste recibo volta ao autor antes do rito; o recibo vale só para o sha256 da página acima",
}
b = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
print("falas entre os recibos:", len(falas), "| mensagens lidas ao autor:", len(LIDO), "| recibo", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    out = V / "PALAVRA_FINAL_DO_AUTOR_v412_R25.json"; assert not out.exists(), "ja' existe: nao sobrescrevo"
    out.write_bytes(b); print("gravado:", out.name)

# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: reconfere os axiomas de TODOS os logs em k412c\\logs, lendo a saida inteira (o Lean quebra
listas longas de axiomas em varias linhas; o filtro de linha unica dos scripts de compilacao lia so' a primeira e
deixaria passar um axioma fora do trio numa linha de continuacao: defeito da gerencia, corrigido aqui).
Para cada log: nomes com '#print axioms' no fonte, nomes com relatorio na saida, conjunto de axiomas de cada um,
'sorryAx' em qualquer lugar. Fail-closed: relatorio ausente, axioma fora do trio ou sorryAx => FALHA.
Recibo: k412c\\AXIOMAS_K412C.json."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
LOGS = AQUI / "k412c" / "logs"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
REL = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.S)
SEM = re.compile(r"'([^']+)' does not depend on any axioms")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


saida_total = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "logs": {}, "falhas": []}
for log in sorted(LOGS.glob("*.log")):
    txt = log.read_text(encoding="utf-8")
    cab, _, saida = txt.partition("SAIDA:\n")
    fonte = re.search(r"^FONTE: (.*)$", cab, re.M).group(1).strip()
    sha_log = re.search(r"^SHA256: (\w+)$", cab, re.M).group(1)
    rc = int(re.search(r"^RC: (-?\d+)$", cab, re.M).group(1))
    pedidos = re.findall(r"^#print axioms\s+(\S+)", Path(fonte).read_text(encoding="utf-8"), re.M)
    rel = {}
    for nome, lista in REL.findall(saida):
        rel[nome] = sorted({a.strip() for a in lista.replace("\n", " ").split(",") if a.strip()})
    for nome in SEM.findall(saida):
        rel[nome] = []
    fora = {n: sorted(set(a) - TRIO) for n, a in rel.items() if set(a) - TRIO}
    # o pedido pode vir com o nome curto (dentro do namespace) e o relatorio traz o nome completo
    faltam = [p for p in pedidos if p not in rel and not any(r.endswith("." + p) for r in rel)]
    item = {"fonte": fonte, "sha256_fonte_no_log": sha_log, "sha256_fonte_agora": sha(fonte),
            "fonte_igual": sha_log == sha(fonte), "rc": rc, "n_pedidos": len(pedidos), "n_relatorios": len(rel),
            "relatorios_faltando": faltam, "fora_do_trio": fora, "sorryAx": "sorryAx" in saida,
            "avisos": saida.count("warning:"), "erros": saida.count("error:")}
    saida_total["logs"][log.stem] = item
    ruim = rc != 0 or fora or faltam or item["sorryAx"] or item["erros"] or not item["fonte_igual"]
    if ruim:
        saida_total["falhas"].append(log.stem)
    print("%-28s RC %d | pedidos %2d | relatorios %2d | faltando %d | fora do trio %d | sorryAx %s | fonte igual %s%s" % (
        log.stem, rc, len(pedidos), len(rel), len(faltam), len(fora), item["sorryAx"], item["fonte_igual"],
        "  <== FALHA" if ruim else ""))
dest = AQUI / "k412c" / "AXIOMAS_K412C.json"
tmp = AQUI / "k412c" / "AXIOMAS_K412C.json.tmp"
dados = json.dumps(saida_total, ensure_ascii=False, indent=1).encode("utf-8")
tmp.write_bytes(dados)
assert tmp.read_bytes() == dados
tmp.replace(dest)
print("logs %d | falhas %s | recibo sha16 %s" % (len(saida_total["logs"]), saida_total["falhas"] or "nenhuma",
                                                sha(dest)[:16]))

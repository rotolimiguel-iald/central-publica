# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: congela, por copia de bytes, o que vai a' leitura de terceiro na ordem 031: as copias de trabalho que a
gerencia mudou em comentario (lidas de pedras_novas\\EMENDAS_DE_COMENTARIO.json), cada uma ao lado da fonte do autor, e a AParedeDoNome.
Destino: pedras_novas\\REV_031\\{trabalho,origem}\\ e MANIFESTO_031.json. Nao sobrescreve arquivo diferente."""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"; D = N / "REV_031"
em = json.loads((N / "EMENDAS_DE_COMENTARIO.json").read_text(encoding="utf-8"))
nomes = sorted({m["modulo"] for m in em["modulos"] if not m["bytes_iguais"]} | {"AParedeDoNome"})
itens = []
for n in nomes:
    for sub, src in (("trabalho", N / (n + ".lean")), ("origem", N / "origem" / (n + ".lean"))):
        b = src.read_bytes(); alvo = D / sub / (n + ".lean"); alvo.parent.mkdir(parents=True, exist_ok=True)
        if alvo.exists():
            assert alvo.read_bytes() == b, "ja' congelado e difere: " + str(alvo)
        else:
            alvo.write_bytes(b)
    itens.append({"modulo": n, "sha256_trabalho": hashlib.sha256((D / "trabalho" / (n + ".lean")).read_bytes()).hexdigest(),
                  "sha256_origem": hashlib.sha256((D / "origem" / (n + ".lean")).read_bytes()).hexdigest()})
p = D / "MANIFESTO_031.json"
if not p.exists():
    p.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n": len(itens), "trocas_exatas": em["trocas_exatas"],
                              "cabecalhos_refeitos_a_mao": em["cabecalhos_refeitos_a_mao"], "itens": itens}, ensure_ascii=False, indent=1).encode("utf-8"))
print("congelados:", len(itens), "|", ", ".join(nomes)); print("manifesto sha16", hashlib.sha256(p.read_bytes()).hexdigest()[:16])

# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: congela, por copia de bytes, o que vai a' leitura de terceiro na ordem 032: as copias de trabalho que a
gerencia emendou pelo parecer da 031 (lidas de pedras_novas\\EMENDAS_DO_PARECER_031.json), cada uma ao lado da copia que o revisor leu
na 031 (pedras_novas\\REV_031\\trabalho, quando existe; senao a fonte do autor), e a pedra nova OSeparadorNoPercurso.
Destino: pedras_novas\\REV_032\\{depois,antes}\\ e MANIFESTO_032.json. Nao sobrescreve arquivo diferente."""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; N = V / "pedras_novas"; D = N / "REV_032"
em = json.loads((N / "EMENDAS_DO_PARECER_031.json").read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
itens = []
for n in sorted(em["sha256_depois"]) + ["OSeparadorNoPercurso"]:
    depois = N / (n + ".lean")
    if n != "OSeparadorNoPercurso":
        assert sha(depois) == em["sha256_depois"][n], "mudou depois das emendas: " + n
    antes = N / "REV_031" / "trabalho" / (n + ".lean")
    de_onde = "REV_031\\trabalho"
    if not antes.exists():
        antes = N / "origem" / (n + ".lean"); de_onde = "origem (a fonte do autor; nao estava na 031)"
    par = [("depois", depois)] + ([] if n == "OSeparadorNoPercurso" else [("antes", antes)])
    for sub, src in par:
        b = src.read_bytes(); alvo = D / sub / (n + ".lean"); alvo.parent.mkdir(parents=True, exist_ok=True)
        if alvo.exists():
            assert alvo.read_bytes() == b, "ja' congelado e difere: " + str(alvo)
        else:
            alvo.write_bytes(b)
    itens.append({"modulo": n, "sha256_depois": sha(D / "depois" / (n + ".lean")), "antes_de": None if n == "OSeparadorNoPercurso" else de_onde,
                  "sha256_antes": None if n == "OSeparadorNoPercurso" else sha(D / "antes" / (n + ".lean"))})
p = D / "MANIFESTO_032.json"
if not p.exists():
    p.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n": len(itens), "trocas_exatas": em["trocas_exatas"], "itens": itens}, ensure_ascii=False, indent=1).encode("utf-8"))
print("congelados:", len(itens), "|", ", ".join(i["modulo"] for i in itens)); print("manifesto sha16", sha(p)[:16])

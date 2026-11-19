# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: passo 1 da NONA lista (ordem do autor de 18/11: entra tudo na v412). Traz, por copia de BYTES, cada fonte
Lean nova (as do INVENTARIO_FORA_DA_OITAVA_LISTA.json que nao estao na oitava lista), uma por nome de modulo (as copias entre pastas
sao identicas por sha256, conferido aqui), para:
  pedras_novas\\origem\\<Nome>.lean   (a fonte como o autor a deixou; nao se edita; e' o termo de comparacao do codigo)
  pedras_novas\\<Nome>.lean           (a copia de trabalho, onde so' comentarios e docstrings mudam pelo metodo de 17/11)
Nao sobrescreve arquivo diferente: se a fonte do autor mudou depois de trazida, PARA e diz qual (a pasta do autor que ainda esta'
sendo escrita traz-se de novo com --retrazer <pasta>, que guarda a copia anterior em origem\\_anteriores\\). Grava ORIGENS.json."""
import hashlib, json, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
inv = json.loads((V / "INVENTARIO_FORA_DA_OITAVA_LISTA.json").read_text(encoding="utf-8"))
man8 = json.loads((V / "insumos" / "MANIFESTO_PEDRAS_v412_R8.json").read_text(encoding="utf-8"))
na_oitava = {m["modulo"] for m in man8["modulos"]}
D = V / "pedras_novas"; O = D / "origem"; O.mkdir(parents=True, exist_ok=True)
retrazer = sys.argv[sys.argv.index("--retrazer") + 1] if "--retrazer" in sys.argv else None
sha = lambda b: hashlib.sha256(b).hexdigest()
por_nome = {}
for it in inv["itens"]:
    if it["modulo"] in na_oitava:
        continue
    por_nome.setdefault(it["modulo"], []).append(it)
origens, novos, iguais, retrazidos = [], 0, 0, 0
for nome, lst in sorted(por_nome.items()):
    assert len({i["sha256"] for i in lst}) == 1, "copias diferentes de " + nome
    # a pasta de origem e' a do autor: Kimi antes da copia que o Codex guardou
    lst = sorted(lst, key=lambda i: (i["de_quem"] != "Kimi", i["mtime"]))
    it = lst[0]; b = Path(it["caminho"]).read_bytes(); assert sha(b) == it["sha256"], "mudou desde o inventario: " + it["caminho"]
    for alvo in (O / (nome + ".lean"), D / (nome + ".lean")):
        if alvo.exists():
            if alvo.parent == O and alvo.read_bytes() != b:
                if retrazer and it["pasta"] == retrazer:
                    ant = O / "_anteriores"; ant.mkdir(exist_ok=True)
                    shutil.copy2(alvo, ant / ("%s.%s.lean" % (nome, sha(alvo.read_bytes())[:16])))
                    alvo.write_bytes(b); (D / (nome + ".lean")).write_bytes(b); retrazidos += 1
                else:
                    raise SystemExit("a fonte do autor mudou depois de trazida: %s (%s)" % (nome, it["pasta"]))
            else:
                iguais += alvo.parent == O
        else:
            alvo.write_bytes(b); novos += alvo.parent == O
    origens.append({"modulo": nome, "de_quem": it["de_quem"], "pasta_de_origem": it["pasta"], "outras_copias": [i["pasta"] for i in lst[1:]],
                    "sha256_origem": it["sha256"], "bytes": it["bytes"], "mtime_origem": it["mtime"]})
p = D / "ORIGENS.json"; tmp = p.with_name(p.name + ".tmp_c1")
tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n": len(origens), "itens": origens}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
print("modulos novos:", len(origens), "| trazidos agora:", novos, "| ja' estavam iguais:", iguais, "| retrazidos:", retrazidos)
for q in ("gerencia", "Kimi", "Codex"):
    print("  ", q, sum(1 for o in origens if o["de_quem"] == q))

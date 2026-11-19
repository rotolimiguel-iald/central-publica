"""extrai, dos cabecalhos das pedras congeladas (quinta lista), as secoes cujo titulo termina em 'tipa' (letra, lei, leitura, identificacao...) e o que o cabecalho diz que NAO esta tipado."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
F = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\insumos\pedras_r7")
saida = {}
for p in sorted(F.glob("*.lean")):
    t = p.read_bytes().decode("utf-8")
    m = re.search(r"/-!(.*?)-/", t, re.S)
    if not m:
        continue
    h = m.group(1)
    secs = re.split(r"(?m)^(?=#{2,3} )", h)
    for i, s in enumerate(secs):
        tit = s.split("\n", 1)[0].strip()
        if re.match(r"^## A\w* \w+ que .*tipa", tit):
            corpo = s.split("\n", 1)[1] if "\n" in s else ""
            nao = [x for x in secs if re.match(r"^#{2,3} .*(NÃO|não|nao) (tipa|est|afirma|se afirma|diz)", x.split("\n", 1)[0])]
            saida[p.stem] = {"titulo": tit, "corpo": corpo.strip(), "nao_tipado": [(x.split("\n", 1)[0].strip(), x.split("\n", 1)[1].strip()) for x in nao]}
for k, v in saida.items():
    print("=====", k, "|", v["titulo"])
    print(v["corpo"][:1500])
    for tit, c in v["nao_tipado"]:
        print("   --- NAO:", tit); print("   ", c[:900].replace("\n", "\n    "))
print(len(saida))

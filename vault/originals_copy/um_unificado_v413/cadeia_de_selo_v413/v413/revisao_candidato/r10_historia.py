# r10 -- procura historia de conversa no texto NOVO do candidato (runtime v413: specs, secao, comentarios), SO LEITURA.
import ast, json, os, re, sys

CAND = r"C:\t\k413c\candidato\um_v413_candidato.py"
HERE = os.path.dirname(os.path.abspath(__file__))
PADROES = [r"\boperador\b", r"\bgerên?cia\b", r"\bgerencia\b", r"\bCodex\b", r"\bKimi\b", r"\bautor\b", r"\bparecer\b", r"\bordem\b", r"\bR[0-9]\b", r"\b\d{1,2}/\d{1,2}(/\d{2,4})?\b",
           r"\bnov(embro)?\b", r"\bD4\d\d", r"\bE4\d\d", r"\bverbatim\b", r"\bfala\b", r"\bsha16\b", r"\bClaude\b", r"\bChatGPT\b", r"\bLuiz\b", r"\bMiguel\b", r"\bconversa\b",
           r"\brevis[ãa]o\b", r"\bproposta\b", r"\brecusad", r"\bpediu\b", r"\bdisse\b", r"\bprêmio\b", r"\bpremio\b", r"\bprize\b", r"\bMillennium\b", r"\bClay\b",
           r"P ?= ?NP", r"\bdecide P\b", r"\bprova P\b", r"\bresolve\b", r"\bprovou\b", r"\bconfirmad", r"\bconfirmed\b", r"\bcreditad", r"\bcredited\b"]


def main():
    txt = open(CAND, "rb").read().decode("utf-8")
    lines = txt.split("\n")
    # o bloco novo: de '# ====================== v413' ate antes de '# ====================== v412'
    i0 = next(i for i, l in enumerate(lines) if l.startswith("# ====================== v413"))
    i1 = next(i for i, l in enumerate(lines) if i > i0 and l.startswith("# ====================== v412"))
    bloco = lines[i0:i1]
    achados = []
    for k, l in enumerate(bloco):
        for p in PADROES:
            for m in re.finditer(p, l, re.I if p.islower() else 0):
                a = max(0, m.start() - 70); b = min(len(l), m.end() + 70)
                achados.append({"linha": i0 + k + 1, "padrao": p, "trecho": l[a:b]})
    # outras linhas novas (fora do bloco): as do main/selo/artigo/versao
    out = {"bloco": [i0 + 1, i1], "n_achados": len(achados), "achados": achados}
    p = os.path.join(HERE, "r10_historia.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    from collections import Counter
    c = Counter(a["padrao"] for a in achados)
    print("bloco", i0 + 1, i1, "achados", len(achados), dict(c))
    vistos = set()
    for a in achados:
        key = (a["padrao"], a["trecho"][:60])
        if key in vistos:
            continue
        vistos.add(key)
        print(a["linha"], a["padrao"], "|", a["trecho"].replace("\n", " ")[:200])


if __name__ == "__main__":
    main()

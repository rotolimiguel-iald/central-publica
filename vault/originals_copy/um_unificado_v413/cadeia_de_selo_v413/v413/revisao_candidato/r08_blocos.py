# r08 -- confere os blocos do README/estado/handoff (BLOCOS_TEXTO_PUBLICO_v413.json) contra a pagina R1 (PT) e a traducao R1_EN (EN). SO LEITURA.
import json, os, re, sys

V413 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413"
HERE = os.path.dirname(os.path.abspath(__file__))
PT = open(os.path.join(V413, "o_que_fica_claro_v413", "O_QUE_FICA_CLARO_v413_R1.md"), encoding="utf-8").read()
EN = open(os.path.join(V413, "O_QUE_FICA_CLARO_v413_R1_EN.md"), encoding="utf-8").read()
B = json.load(open(os.path.join(V413, "BLOCOS_TEXTO_PUBLICO_v413.json"), encoding="utf-8"))


def norm(s):
    s = s.replace("> ", "").replace("\n>", "\n")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def frases(s):
    s = norm(s)
    # separa por ponto final/ponto e virgula seguido de espaco e maiuscula, e por quebras de item
    partes = re.split(r"(?<=[.;:])\s+(?=[A-ZÀ-Ý“\*\(\-0-9])|\s+-\s+|\s+\d\.\s+", s)
    return [p.strip(" -*") for p in partes if len(p.strip(" -*")) > 25]


def main():
    npt, nen = norm(PT), norm(EN)
    out = {}
    for sup, blocos in B["blocos"].items():
        ref = npt if sup.endswith(":pt") else nen
        res = {}
        for k, txt in blocos.items():
            fs = frases(txt)
            fora = [f for f in fs if norm(f).replace("**", "") not in ref.replace("**", "")]
            res[k] = {"n_frases": len(fs), "fora_da_pagina": fora[:12], "n_fora": len(fora)}
        out[sup] = res
    p = os.path.join(HERE, "r08_blocos.json")
    with open(p + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    os.replace(p + ".tmp", p)
    for sup, res in out.items():
        for k, v in res.items():
            if v["n_fora"]:
                print("==", sup, k, v["n_fora"], "de", v["n_frases"])
                for f in v["fora_da_pagina"]:
                    print("    ", f[:400])
    # os blocos 'entrega' inteiros
    for sup, blocos in B["blocos"].items():
        if "entrega" in blocos:
            print("\n#### ENTREGA", sup)
            print(blocos["entrega"][:3000])


if __name__ == "__main__":
    main()

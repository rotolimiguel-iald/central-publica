# -*- coding: utf-8 -*-
"""verificar_historia_texto_v412.py -- verificador de HISTORIA DE CONVERSA para texto corrido (molde: verificar_historia_nas_pedras.py, da gerencia, que olha fontes Lean).
O contrato da v412 (secao 0): no que entra no programa nao entra fala, data de conversa, nome de pessoa ou de modelo, numero de ordem/revisao/parecer, “a gerencia”, “o autor disse”, “corrigido em”.
Classes FORTES (falha): aspas angulares; data (dd/mm[/aaaa], dd de mes, ISO); nome de pessoa ou de modelo da casa; numero de ordem, revisao, parecer, decisao (Dnnn) ou errata (Ennn); “a gerencia”;
atribuicao de fala (o operador/o autor + verbo de fala; palavra/ordem/fala/decisao do operador ou do autor); “corrigido em”, “errata”, “emenda”, “ratific*”.
Classe INFORMATIVA (nao falha; lista para a gerencia): menção a “operador”/“autor” sem verbo de fala (uso matematico: operador do custo).
Cada texto conta quantos itens (linhas/unidades) examinou; zero examinados e' falha. Uso: verificar_historia_texto_v412.py <arquivo ...> [--json <campo>]  (md/txt/py: o arquivo inteiro; json: todas as strings)."""
import json, re, sys
from pathlib import Path

FORTES = [
    ("aspas_angulares", re.compile(r"[«»]")),
    ("data", re.compile(r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b|\b\d{1,2}\s+(?:de\s+)?(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[a-zç]*\b|\b20\d\d-\d\d-\d\d\b|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b", re.I)),
    ("nome_de_pessoa_ou_modelo", re.compile(r"\b(?:Luiz|Rotoli|Codex|Kimi|ChatGPT|GPT|Claude|Sonnet|Opus|Haiku|DeepSeek|MiMo|Qwen|Gemini|Grok|Anthropic|OpenAI|Antigravity)\b")),
    ("ordem_revisao_parecer_decisao_errata", re.compile(r"\b[Oo]rdem\s+\d+|\bORDEM\b|\bREV\d+\b|\bR\d\b|\bparecer(?:es)?\b|\brevis(?:ão|ao|or)\b|\bD\d{2,3}\b|\bE\d{2}\b|\bpedido\s+\d+|\breview(?:er)?\b|\bopinion\b", re.I)),
    ("a_gerencia", re.compile(r"\bger[eê]ncia\b|\bmanagement\b", re.I)),
    ("atribuicao_de_fala", re.compile(r"(?:\b(?:palavra|ordem|fala|decis[aã]o|defini[cç][aã]o|leitura|nome|cunhagem|pedido)\s+d[oa]s?\s+(?:operador|autor)\b)|(?:\b(?:o|do|ao|pelo)\s+(?:operador|autor)\s+(?:diss|ordenou|pediu|ratificou|definiu|fixou|cunhou|escreveu|respondeu|afirmou|decidiu|mandou)\w*)|(?:\bthe\s+(?:operator|author)\s+(?:said|ordered|asked|ratified|defined|fixed|coined|wrote|answered|stated|decided)\b)|\bdisse\b|\bmandou\b|\bperguntou\b|\brespondeu\b", re.I)),
    ("corrigido_errata_emenda_ratificacao", re.compile(r"\bcorrigid[oa]\s+em\b|\berrata\b|\bemenda\b|\bratific\w+|\bcorrected\s+in\b|\bamendment\b", re.I)),
]
INFORMATIVA = re.compile(r"\boperador\b|\bautor\b|\boperator\b|\bauthor\b", re.I)


def unidades_de(path: Path, campo=None):
    t = path.read_bytes().decode("utf-8")
    if path.suffix == ".json":
        obj = json.loads(t)
        out = []

        def walk(o, p=""):
            if isinstance(o, str):
                out.append((p, o))
            elif isinstance(o, dict):
                for k, v in o.items():
                    walk(v, p + "/" + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, p + "[%d]" % i)
        walk(obj)
        return out
    return [("L%d" % (i + 1), l) for i, l in enumerate(t.replace("\r\n", "\n").split("\n")) if l.strip()]


def examinar(unidades):
    achados, info = [], []
    for onde, texto in unidades:
        sem_codigo = re.sub(r"`[^`]+`", " ", texto)   # nomes de termo entre crases nao sao prosa
        for classe, rx in FORTES:
            for m in rx.finditer(sem_codigo):
                achados.append({"classe": classe, "onde": onde, "trecho": sem_codigo[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")})
        for m in INFORMATIVA.finditer(sem_codigo):
            info.append({"onde": onde, "trecho": sem_codigo[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")})
    return {"n_unidades_examinadas": len(unidades), "achados": achados, "n_achados": len(achados), "informativos": info, "n_informativos": len(info),
            "ok": bool(len(unidades)) and not achados}


PLANTADAS = [("aspas_angulares", "o texto cita «uma fala»"), ("data", "decidido em 17/11/2026"), ("data", "on 3 Nov the text changed"), ("nome_de_pessoa_ou_modelo", "o Codex conferiu"), ("nome_de_pessoa_ou_modelo", "Claude wrote it"),
             ("ordem_revisao_parecer_decisao_errata", "conforme a ordem 027"), ("ordem_revisao_parecer_decisao_errata", "pelo parecer do revisor"), ("ordem_revisao_parecer_decisao_errata", "a decisão D210"),
             ("a_gerencia", "a gerência decidiu"), ("atribuicao_de_fala", "o operador disse que sim"), ("atribuicao_de_fala", "a palavra do autor"), ("atribuicao_de_fala", "the author said so"),
             ("corrigido_errata_emenda_ratificacao", "corrigido em outra versão"), ("corrigido_errata_emenda_ratificacao", "a errata ao lado"), ("corrigido_errata_emenda_ratificacao", "foi ratificado")]
LIMPAS = ["O operador do custo de uma fórmula é a penalidade dos vínculos das cláusulas.", "P = nP é teorema da TGL nas classes do seu dicionário.", "The Lean kernel checks the proof once."]


def autoteste():
    """controle: cada classe forte detecta a sua frase plantada; as frases limpas nao disparam classe forte"""
    res = []
    for classe, tx in PLANTADAS:
        r = examinar([("plantada", tx)])
        res.append({"classe": classe, "texto": tx, "detectou": any(a["classe"] == classe for a in r["achados"])})
    for tx in LIMPAS:
        r = examinar([("limpa", tx)])
        res.append({"classe": "limpa", "texto": tx, "detectou": bool(r["achados"])})
    ok = all(x["detectou"] for x in res if x["classe"] != "limpa") and not any(x["detectou"] for x in res if x["classe"] == "limpa")
    return {"ok": ok, "n": len(res), "n_ok": sum(1 for x in res if (x["detectou"] if x["classe"] != "limpa" else not x["detectou"])), "itens": res}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rc = 0
    if "--autoteste" in sys.argv:
        a_ = autoteste(); print("autoteste:", a_["n_ok"], "/", a_["n"], "OK" if a_["ok"] else "FALHOU"); rc |= (not a_["ok"])
    for a in [x for x in sys.argv[1:] if not x.startswith("--")]:
        r = examinar(unidades_de(Path(a)))
        print("%-70s unidades=%d achados=%d informativos=%d %s" % (Path(a).name, r["n_unidades_examinadas"], r["n_achados"], r["n_informativos"], "OK" if r["ok"] else "FALHA"))
        for x in r["achados"][:12]:
            print("    ", x["classe"], x["onde"], "|", x["trecho"])
        rc |= (not r["ok"])
    sys.exit(rc)

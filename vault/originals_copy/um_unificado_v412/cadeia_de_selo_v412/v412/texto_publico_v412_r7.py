# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de texto_publico_v412_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R11)] copia de texto_publico_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e5_22_derivar_texto_r7_v412.py). O original fica intacto.
"""texto_publico_v412.py -- converte a pagina publica da v412 (markdown: PT, e a traducao EN) em TeX para a secao do artigo, sem prosa nova de conteudo (so' conectivos de lista e os rotulos 'onde'/'where').
Tambem devolve o paragrafo de P = nP (o bloco de citacao da secao 2) em forma de texto-TeX para o resumo. Modulo de CADEIA (nao entra no programa). Nada daqui carrega historia de conversa."""
import re

GREGAS = {"τ": r"\tau", "α": r"\alpha", "β": r"\beta", "ρ": r"\rho", "σ": r"\sigma", "Δ": r"\Delta", "Λ": r"\Lambda", "θ": r"\theta", "π": r"\pi", "⌊": r"\lfloor", "⌋": r"\rfloor"}
SUB_SUP = {"₁": "_1", "ⁿ": "^n", "ˢ": "^s", "²": "^2"}
ROTULO_ONDE = {"pt": "Onde", "en": "Where"}


def esc_texto(t: str) -> str:
    """escapa o texto simples (fora de codigo) e converte o unicode que o inputenc utf8 do artigo nao cobre"""
    t = t.replace("\\", r"\textbackslash{}")
    t = re.sub(r"([%&#$_{}])", r"\\\1", t)
    # expoente com parenteses: x^(...) -> x$^{...}$
    t = re.sub(r"\^\(([^)]*)\)", lambda m: "\x00SUP" + m.group(1).replace("−", "-") + "\x01", t)
    t = t.replace("^", r"\^{}")
    t = re.sub("\x00SUP([^\x01]*)\x01", lambda m: "$^{" + m.group(1) + "}$", t)
    for k, v in SUB_SUP.items():
        t = t.replace(k, "$" + v + "$")
    for k, v in GREGAS.items():
        t = t.replace(k, "$" + v + "$")
    t = t.replace("−", "$-$").replace("★", r"$\star$").replace("≠", r"$\neq$").replace("≤", r"$\leq$").replace("≥", r"$\geq$")
    return t


def esc_codigo(t: str) -> str:
    t = t.replace("\\", r"\textbackslash{}")
    t = re.sub(r"([%&#$_{}])", lambda m: r"\_\allowbreak{}" if m.group(1) == "_" else "\\" + m.group(1), t)
    t = t.replace("^", r"\^{}").replace("~", r"\~{}")
    for k, v in SUB_SUP.items():
        t = t.replace(k, "$" + v + "$")
    for k, v in GREGAS.items():
        t = t.replace(k, "$" + v + "$")
    t = t.replace("−", "$-$").replace("★", r"$\star$").replace("≠", r"$\neq$").replace("≤", r"$\leq$").replace("≥", r"$\geq$")
    return t


def inline_tex(s: str) -> str:
    out = []
    pos = 0
    for m in re.finditer(r"`([^`]+)`|\*\*(.+?)\*\*", s):
        out.append(esc_texto(s[pos:m.start()]))
        if m.group(1) is not None:
            out.append(r"\texttt{" + esc_codigo(m.group(1)) + "}")
        else:
            out.append(r"\textbf{" + inline_tex(m.group(2)) + "}")
        pos = m.end()
    out.append(esc_texto(s[pos:]))
    return "".join(out)


def inline_resumo(s: str) -> str:
    """forma do texto do resumo (TeX-ish que o programa ja' trata: o unicode grego e o menos sao convertidos na emissao; aqui so' o que ele nao converte)"""
    s = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + esc_codigo(m.group(1)) + "}", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    for k, v in SUB_SUP.items():
        s = s.replace(k, "$" + v + "$")
    s = s.replace("2$^n$", "$2^{n}$")
    return s


def blocos(md: str):
    linhas = md.replace("\r\n", "\n").split("\n")
    i = 0
    out = []
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1; continue
        if l.startswith("# "):
            out.append(("h1", l[2:].strip())); i += 1; continue
        if l.startswith("## "):
            out.append(("h2", l[3:].strip())); i += 1; continue
        if l.startswith("> "):
            out.append(("quote", l[2:].strip())); i += 1; continue
        if l.startswith("|"):
            linhas_t = []
            while i < len(linhas) and linhas[i].startswith("|"):
                linhas_t.append(linhas[i]); i += 1
            cab = [c.strip() for c in linhas_t[0].strip("|").split(" | ")]
            lin = []
            for r in linhas_t[2:]:
                cel = re.split(r" \| ", r.strip()[1:-1].strip())
                lin.append([c.strip() for c in cel])
            out.append(("table", (cab, lin))); continue
        if re.match(r"^- ", l):
            it = []
            while i < len(linhas) and re.match(r"^- ", linhas[i]):
                it.append(linhas[i][2:].strip()); i += 1
            out.append(("bullets", it)); continue
        if re.match(r"^\d+\. ", l):
            it = []
            while i < len(linhas) and re.match(r"^\d+\. ", linhas[i]):
                it.append(re.sub(r"^\d+\. ", "", linhas[i]).strip()); i += 1
            out.append(("numbered", it)); continue
        out.append(("par", l.strip())); i += 1
    return out


def para_tex(md: str, lang: str):
    """lista de linhas (strings) para o artigo: titulo, secoes, paragrafos, listas; a tabela vira lista (frase --- termo --- onde)"""
    bl = blocos(md)
    tex = []
    titulo = None
    for tipo, v in bl:
        if tipo == "h1":
            titulo = v
            tex.append(r"\section*{" + inline_tex(v) + "}")
            tex.append(r"\addcontentsline{toc}{section}{" + inline_tex(v) + "}")
        elif tipo == "h2":
            tex.append(r"\subsection*{" + inline_tex(v) + "}")
        elif tipo == "par":
            tex.append(inline_tex(v))
        elif tipo == "quote":
            tex.append(r"\begin{quote}" + inline_tex(v) + r"\end{quote}")
        elif tipo == "bullets":
            tex.append(r"\begin{itemize}")
            tex += [r"\item " + inline_tex(x) for x in v]
            tex.append(r"\end{itemize}")
        elif tipo == "numbered":
            tex.append(r"\begin{enumerate}")
            tex += [r"\item " + inline_tex(x) for x in v]
            tex.append(r"\end{enumerate}")
        elif tipo == "table":
            cab, lin = v
            tex.append(r"\begin{itemize}")
            for r in lin:
                assert len(r) == 3, ("a tabela da pagina tem 3 colunas", r)
                assert not any(" --- " in c for c in r), ("celula com o separador da linha de tabela", r)
                tex.append(r"\item \textbf{" + inline_tex(r[0]) + r"} --- " + inline_tex(r[1]) + r" --- \emph{" + ROTULO_ONDE[lang] + r":} " + inline_tex(r[2]))
            tex.append(r"\end{itemize}")
    return titulo, tex


def paragrafo_pnp(md: str) -> str:
    """o bloco de citacao da secao 2 (o paragrafo de P = nP), na forma de texto do resumo"""
    sec = re.search(r"^## 2\. .*?\n(.*?)(?=^## 3\. )", md.replace("\r\n", "\n"), re.S | re.M)
    assert sec, "a secao 2 nao foi achada"
    q = re.findall(r"^> (.+)$", sec.group(1), re.M)
    assert len(q) == 1, ("a secao 2 tem de ter UM bloco de citacao", len(q))
    return inline_resumo(q[0].strip())

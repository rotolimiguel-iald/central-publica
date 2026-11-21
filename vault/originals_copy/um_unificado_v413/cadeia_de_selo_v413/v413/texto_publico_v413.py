# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\texto_publico_v412_r7.py (que fica intacto).
"""texto_publico_v413.py -- converte a pagina publica da v413 (markdown: PT, e a traducao EN) em TeX para a secao do artigo, sem prosa nova de conteudo (so' conectivos de lista e os rotulos 'Onde'/'Where').
Diferenca do molde, dita: a fonte markdown da v413 quebra as linhas dos paragrafos, dos itens e do bloco de citacao; antes de converter, as quebras sao JUNTADAS (desembrulhar: o paragrafo, o bloco de citacao e o
item de lista viram UMA linha, com as mesmas palavras), porque a unidade da guarda e' o paragrafo inteiro; e tres caracteres que a pagina da v412 nao tinha ganham forma TeX (√ -> \\surd, como o programa ja' faz;
³ -> ^3; ½ -> \\frac{1}{2}). Modulo de CADEIA (nao entra no programa). Nada daqui carrega historia de conversa."""
import re

GREGAS = {"τ": r"\tau", "α": r"\alpha", "β": r"\beta", "ρ": r"\rho", "σ": r"\sigma", "Δ": r"\Delta", "Λ": r"\Lambda", "θ": r"\theta", "π": r"\pi", "⌊": r"\lfloor", "⌋": r"\rfloor", "√": r"\surd", "½": r"\frac{1}{2}"}
SUB_SUP = {"₁": "_1", "ⁿ": "^n", "ˢ": "^s", "²": "^2", "³": "^3"}
ROTULO_ONDE = {"pt": "Onde", "en": "Where"}


def desembrulhar(md):
    """junta as quebras de linha da fonte markdown: o paragrafo, o bloco de citacao ('> ') e o item de lista ('- ', '1. ', com as linhas de continuacao indentadas) viram UMA linha; titulos e linhas de tabela ficam como estao"""
    linhas = md.replace("\r\n", "\n").split("\n")
    out, cur = [], None

    def fecha():
        nonlocal cur
        if cur is not None:
            out.append(cur)
            cur = None
    for l in linhas:
        if not l.strip():
            fecha(); out.append(""); continue
        if l.startswith("|") or l.startswith("#"):
            fecha(); out.append(l.rstrip()); continue
        if l.startswith("> "):
            if cur is not None and cur.startswith("> "):
                cur += " " + l[2:].strip()
            else:
                fecha(); cur = l.rstrip()
            continue
        if re.match(r"^(?:- |\d+\. )", l):
            fecha(); cur = l.rstrip(); continue
        if l.startswith("  ") and cur is not None and (cur.startswith("- ") or re.match(r"^\d+\. ", cur)):
            cur += " " + l.strip(); continue
        if cur is not None and not cur.startswith("> ") and not cur.startswith("- ") and not re.match(r"^\d+\. ", cur):
            cur += " " + l.strip(); continue
        fecha(); cur = l.rstrip()
    fecha()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


def esc_texto(t: str) -> str:
    """escapa o texto simples (fora de codigo) e converte o unicode que o inputenc utf8 do artigo nao cobre"""
    t = t.replace("\\", r"\textbackslash{}")
    t = re.sub(r"([%&#$_{}])", r"\\\1", t)
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


def blocos(md: str):
    linhas = desembrulhar(md).split("\n")
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
    """o bloco de citacao da secao 2 (o paragrafo de “P = nP”), desembrulhado, como esta' na pagina"""
    sec = re.search(r"^## 2\. .*?\n(.*?)(?=^## 3\. )", desembrulhar(md), re.S | re.M)
    assert sec, "a secao 2 nao foi achada"
    q = re.findall(r"^> (.+)$", sec.group(1), re.M)
    assert len(q) == 1, ("a secao 2 tem de ter UM bloco de citacao", len(q))
    return q[0].strip()

# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (Etapa 1, 20/11/2026)] copia de C:\IALD\Central de Patentes\work\cadeia_de_selo\v412\lean_texto_v412.py; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA1_v413.json (derivador: derivar_scripts_etapa1_v413.py) e subida dos rotulos de versao (v412->v413, v411->v412); o molde fica intacto.
"""lean_texto_v413.py -- (claude-construtor-v412, 17/11/2026) leitura de texto de fonte Lean para a cadeia da v413, sem dependencia: (1) `mascara_comentarios(t)`: troca por espaco todo
caractere dentro de comentario (`--` ate' o fim da linha; `/- ... -/` com aninhamento, inclusive docstrings `/--` e `/-!`) e dentro de literal de cadeia "..." (com escape), preservando
as quebras de linha (as posicoes e os numeros de linha nao mudam); (2) `pilha_de_namespace_por_linha(t)`: a pilha de `namespace` vigente em cada linha (sobre o texto mascarado);
(3) `nomes_declarados(t)`: os nomes declarados (theorem, lemma, def, abbrev, structure, inductive, class, instance com nome, opaque, axiom) qualificados pela pilha, sem os `private`.
Nao executa nada; so' le texto."""
import re

RX_DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*((?:private|protected|noncomputable|partial|unsafe|nonrec)\s+)*(theorem|lemma|def|abbrev|structure|inductive|class|instance|opaque|axiom)\s+([^\s:({\[]+)")


def mascara_comentarios(t):
    out = list(t); i = 0; n = len(t); prof = 0; em_cadeia = False
    while i < n:
        c = t[i]; d = t[i + 1] if i + 1 < n else ""
        if prof > 0:
            if c == "/" and d == "-":
                prof += 1; out[i] = out[i + 1] = " "; i += 2; continue
            if c == "-" and d == "/":
                prof -= 1; out[i] = out[i + 1] = " "; i += 2; continue
            if c != "\n":
                out[i] = " "
            i += 1; continue
        if em_cadeia:
            if c == "\\" and i + 1 < n:
                out[i] = " "
                if t[i + 1] != "\n":
                    out[i + 1] = " "
                i += 2; continue
            if c == '"':
                em_cadeia = False; i += 1; continue
            if c != "\n":
                out[i] = " "
            i += 1; continue
        if c == "/" and d == "-":
            prof = 1; out[i] = out[i + 1] = " "; i += 2; continue
        if c == "-" and d == "-":
            j = t.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j; continue
        if c == '"':
            em_cadeia = True; i += 1; continue
        i += 1
    return "".join(out)


def pilha_de_namespace_por_linha(t):
    """lista (uma entrada por linha do texto) com a pilha de namespace VIGENTE naquela linha (antes de aplicar um `namespace`/`end` da propria linha)."""
    m = mascara_comentarios(t).split("\n")
    escopos = []; res = []   # cada escopo: ("ns", nome) ou ("sec", nome_ou_vazio); `end X` fecha o escopo do topo
    for ln in m:
        res.append([e[1] for e in escopos if e[0] == "ns"])
        s = ln.strip()
        a = re.match(r"^namespace\s+(\S+)", s)
        if a:
            escopos.append(("ns", a.group(1))); continue
        a = re.match(r"^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$", s)
        if a:
            escopos.append(("sec", a.group(1) or "")); continue
        b = re.match(r"^end(?:\s+(\S+))?\s*$", s)
        if b and escopos:
            nome = b.group(1) or ""
            if escopos[-1][1] == nome:
                escopos.pop()
    return res


def nomes_declarados(t):
    m = mascara_comentarios(t).split("\n")
    pil = pilha_de_namespace_por_linha(t)
    out = []
    for i, ln in enumerate(m):
        s = ln.strip()
        a = RX_DECL.match(s)
        if not a:
            continue
        mods, kw, nome = a.group(1) or "", a.group(2), a.group(3)
        if "private" in mods or (kw == "instance" and nome in ("where", ":=")):
            continue
        q = nome[len("_root_."):] if nome.startswith("_root_.") else ".".join(pil[i] + [nome])
        out.append((q, kw, i + 1))
    return out

# -*- coding: utf-8 -*-
# Fonte da guarda de frases da v412 (embutida no programa e usada pela cadeia): a funcao sobre UMA unidade, a divisao em unidades e a travessia (o ponto unico de chamada). Sem historia de conversa.


def _v412_guarda_frases(txt_):
    """v412 -- a guarda das frases, sobre UMA unidade de texto (titulo, paragrafo, item de lista ou celula de tabela; uma lingua so'). Roda a guarda herdada da v411 inteira (_v411_guarda_frases) e acrescenta duas obrigacoes,
    sem emprestar marca, ressalva, condicao ou negacao de outra unidade:
    (1) “P = nP”: a unidade que o traz tem de trazer, nela mesma, as duas marcas: (a) “classes do seu dicionario” ou “classes do dicionario da TGL” (EN: classes of its dictionary, classes of the TGL dictionary) e (b) a ressalva da maquina
        de fita: “maquina de fita” e, depois dela, na mesma frase, “nao esta demonstrado” ou “demonstrada” (EN: tape machine, depois “has not been shown”). Com as duas marcas, e so' entao, saem da lista exatamente as duas violacoes herdadas
        F34_p_igual_np_sem_o_qualificador_do_dicionario_ou_a_ressalva_open e F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor, pelo nome inteiro; a F37b (a obrigacao local da v409) nao sai. Sem uma das marcas: F70.
    (2) o nome do problema dos fluidos, por FRASE (a frase vai ate o ponto, o ponto e virgula, a interrogacao, a exclamacao ou a quebra de linha; um titulo e uma celula sao uma frase): a frase que o traz tem de trazer, nela mesma, a forma
        condicional (condicional, condicionada; EN: conditional, conditioned) ou a negacao expressa antes do nome (“nao diz que”; EN: does not say that), senao F68a; fora da forma da negacao, a afirmacao junto do nome (esta, foi, fica ou e + demonstrada,
        provada ou resolvida; os verbos resolve, demonstra, prova; EN: is, was ou has been + shown, proved, proven, demonstrated, solved ou settled; solves, proves, settles) e' F68b. F69: o nome do premio e' vedado em toda unidade.
    As formas da F43 (oraculo, leitor de Turing, leitor que devolve Z) seguem como a guarda herdada as trata. Devolve [(regra, trecho)]."""
    import re as _re
    s_ = str(txt_)
    out_ = list(_v411_guarda_frases(s_))
    if _re.search(r"P\s*=\s*nP", s_):
        a_ = bool(_re.search(r"classes\s+do\s+seu\s+dicion(?:á|a)rio|classes\s+do\s+dicion(?:á|a)rio\s+da\s+TGL|classes\s+of\s+its\s+dictionary|classes\s+of\s+the\s+TGL\s+dictionary", s_, _re.I))
        b_ = bool(_re.search(r"m(?:á|a)quina\s+de\s+fita[^.;\n]*?n(?:ã|a)o\s+est(?:á|a)\s+demonstrad[ao]|tape\s+machine[^.;\n]*?has\s+not\s+been\s+shown", s_, _re.I))
        if a_ and b_:
            out_ = [v_ for v_ in out_ if v_[0] not in ("F34_p_igual_np_sem_o_qualificador_do_dicionario_ou_a_ressalva_open", "F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor")]
        else:
            m_ = _re.search(r"P\s*=\s*nP", s_)
            out_.append(("F70_p_igual_np_sem_as_duas_marcas_na_unidade:" + ",".join(n_ for n_, ok_ in (("dicionario", a_), ("maquina_de_fita", b_)) if not ok_), s_[max(0, m_.start() - 30):m_.end() + 60].replace("\n", " ")))
    _NOME_ = _re.compile(r"Navier\s*(?:[–—-]{1,2}|\\textendash(?:\{\})?)?\s*Stokes|Stokes\s*(?:[–—-]{1,2}|\\textendash(?:\{\})?)?\s*Navier", _re.I)
    _COND_ = _re.compile(r"\bcondicional\b|\bcondicionais\b|\bcondicionad[ao]s?\b|\bconditional\b|\bconditioned\b", _re.I)
    _NEGEXP_ = _re.compile(r"n(?:ã|a)o\s+diz\s+que|does\s+not\s+say\s+that", _re.I)
    _AFIRMA_ = _re.compile(r"\b(?:est(?:á|a)|foi|fica|é|e')\s+(?:ainda\s+)?(?:demonstrad|provad|resolvid)[ao]s?\b|\b(?:resolve|demonstra|prova)\b|\b(?:is|was|has\s+been)\s+(?:shown|proved|proven|demonstrated|solved|settled)\b|\b(?:solves|proves|settles)\b", _re.I)
    for fr_ in _re.split(r"[.;?!\n]", s_):
        for m_ in _NOME_.finditer(fr_):
            neg_ = bool(_NEGEXP_.search(fr_[:m_.start()]))
            if not (neg_ or _COND_.search(fr_)):
                out_.append(("F68a_o_nome_dos_fluidos_sem_a_forma_condicional_ou_a_negacao_expressa", fr_.strip()[:200]))
            if not neg_ and _AFIRMA_.search(fr_):
                out_.append(("F68b_afirmacao_junto_do_nome_dos_fluidos", fr_.strip()[:200]))
            break
    for m_ in _re.finditer(r"\bmil[eê]nio\b|\bmillennium\b", s_, _re.I):
        out_.append(("F69_o_nome_do_premio", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")))
    return out_


def _v412_unidades_de_texto(texto_, tipo_="paragrafo"):
    """v412 -- divide uma folha de texto (markdown simples) em unidades [(tipo, texto)]: titulo (linha que comeca por #), paragrafo (inclui o bloco de citacao), item de lista e celula de tabela (cada celula)."""
    import re as _re
    out_ = []
    for ln_ in str(texto_).split("\n"):
        l_ = ln_.strip()
        if not l_ or _re.fullmatch(r"\|[\s:|-]+\|?", l_):
            continue
        if l_.startswith("|"):
            for c_ in [c_.strip() for c_ in l_.strip("|").strip().split(" | ")]:
                if c_:
                    out_.append(("celula", c_))
        elif l_.startswith("#"):
            out_.append(("titulo", l_.lstrip("#").strip()))
        elif _re.match(r"^(?:[-*]|\d+\.)\s+", l_):
            out_.append(("item", _re.sub(r"^(?:[-*]|\d+\.)\s+", "", l_)))
        elif l_.startswith(">"):
            out_.append(("paragrafo", l_.lstrip("> ").strip()))
        else:
            out_.append((tipo_, l_))
    return out_


def _v412_unidades_tex(linhas_):
    """v412 -- divide as linhas de TeX da secao do artigo em unidades [(tipo, texto)]: titulo (\\section*, \\subsection*), item de lista, celula (a linha de tabela vira tres celulas) e paragrafo (inclui o bloco de citacao)."""
    import re as _re
    out_ = []
    for ln_ in linhas_:
        l_ = str(ln_).strip()
        if not l_ or l_.startswith(("\\addcontentsline", "\\begin{itemize}", "\\end{itemize}", "\\begin{enumerate}", "\\end{enumerate}")):
            continue
        m_ = _re.match(r"^\\(?:sub)*section\*\{(.*)\}$", l_)
        if m_:
            out_.append(("titulo", m_.group(1)))
        elif l_.startswith("\\item "):
            partes_ = l_[6:].split(" --- ")
            if len(partes_) == 3 and ("\\emph{Onde:}" in partes_[2] or "\\emph{Where:}" in partes_[2]):
                out_.extend(("celula", _re.sub(r"^\\textbf\{(.*)\}$", r"\1", p_.strip())) for p_ in partes_)
            else:
                out_.append(("item", l_[6:]))
        elif l_.startswith("\\begin{quote}"):
            out_.append(("paragrafo", l_.replace("\\begin{quote}", "").replace("\\end{quote}", "")))
        else:
            out_.append(("paragrafo", l_))
    return out_


def _v412_travessia(superficie_, objeto_, forma_="dados"):
    """v412 -- A TRAVESSIA: o ponto unico de chamada da guarda de frases da v412. Percorre TODAS as folhas de texto de `objeto_` (forma 'dados': dict/lista em qualquer profundidade, cada campo de texto e cada item de lista;
    forma 'tex': a lista de linhas de TeX do artigo), divide cada folha em unidades (titulo, paragrafo, item, celula) e roda _v412_guarda_frases em cada unidade, sozinha. Nunca examina o corpo serializado como uma cadeia so'.
    Devolve {superficie, n_unidades, unidades:[{campo, tipo, inicio, regras}], violacoes:[(campo, tipo, regra, trecho)], ok}; superficie sem nenhuma unidade e' falha (ok False), nunca passagem."""
    folhas_ = []

    def _fol(campo_, v_, tipo_):
        if isinstance(v_, str):
            folhas_.append((campo_, v_, tipo_))
        elif isinstance(v_, dict):
            for k_, w_ in v_.items():
                _fol(campo_ + "/" + str(k_), w_, tipo_)
        elif isinstance(v_, (list, tuple)):
            for i_, w_ in enumerate(v_):
                _fol("%s[%d]" % (campo_, i_), w_, "item" if isinstance(w_, str) else tipo_)
    unidades_, viol_ = [], []
    if forma_ == "tex":
        pares_ = [("tex", t_, x_) for t_, x_ in _v412_unidades_tex(objeto_)]
    else:
        _fol("", objeto_, "paragrafo")
        pares_ = []
        for campo_, v_, tipo_ in folhas_:
            for t_, x_ in _v412_unidades_de_texto(v_, tipo_):
                pares_.append((campo_ or "/", t_, x_))
    for campo_, tipo_, x_ in pares_:
        vs_ = _v412_guarda_frases(x_)
        unidades_.append({"campo": campo_, "tipo": tipo_, "inicio": x_[:60], "texto": x_, "regras": [v_[0] for v_ in vs_]})
        viol_.extend((campo_, tipo_, v_[0], v_[1]) for v_ in vs_)
    if not unidades_:
        viol_.append(("/", "superficie", "SUPERFICIE_VAZIA_NENHUMA_UNIDADE_EXAMINADA", str(superficie_)))
    return {"superficie": superficie_, "n_unidades": len(unidades_), "unidades": unidades_, "violacoes": viol_, "ok": bool(unidades_) and not viol_}

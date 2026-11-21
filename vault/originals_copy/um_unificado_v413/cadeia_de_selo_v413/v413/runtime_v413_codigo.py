# -*- coding: utf-8 -*-
# Funcoes novas da v413 que entram no programa (a secao do artigo e a rodada dos registros por especificacao). A guarda de frases e' a herdada da v412 (_v412_travessia, ja' no programa). Sem historia de conversa.


def _v413_secao_tex(lang_):
    """v413 -- a secao “O que fica claro na v413” do artigo, em 'pt' ou 'en': texto da teoria montado da pagina publica, sem numero do core (os numeros do kernel estao nos registros). Passa pela travessia da guarda de frases
    herdada da v412 antes de ser emitido; violacao ou nenhuma unidade examinada e' falha visivel (ValueError), nunca aviso. Devolve a lista de linhas para s.append."""
    t_ = _v412_travessia("artigo:" + lang_, list(_V413_SECAO[lang_]), "tex")
    if not t_["ok"]:
        raise ValueError("a travessia da guarda de frases herdada da v412 recusa a secao do artigo da v413 (%s): %r" % (lang_, t_["violacoes"][:3]))
    return list(_V413_SECAO[lang_])


def _v413_rodar_specs(core_):
    """v413 -- roda os seis registros por especificacao da v413 (os cinco do contrato e a cobertura do relatorio de axiomas; o motor e' o da v392: _v392_registro), na ordem de _V413_SPECS (cunhagens_v413 por ultimo: cobra o selo dos quatro registros com ancora). Antes do motor, a travessia da
    guarda de frases herdada da v412 percorre o corpo inteiro e a palavra de veredito de cada registro (unidade por unidade) e grava o resultado em core['guarda_frases_v413'][nome]; cada registro traz a checagem obrigatoria
    desse resultado (zero violacao; mais de zero unidades examinadas), que passa pelo caminho de qualquer checagem do motor: violacao e' checagem falsa e o registro nao sela. Excecao vira AVISO visivel (all_verified False),
    nunca derruba o rito."""
    gv_ = {}
    for spec_ in _V413_SPECS:
        try:
            t_ = _v412_travessia("registro:" + spec_["nome"], {"corpo": {k_: spec_.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": spec_["veredito_prefixo"] + "__" + spec_["veredito_sufixo"]})
            gv_[spec_["nome"]] = {"n_unidades_examinadas": t_["n_unidades"], "n_violacoes": len(t_["violacoes"]), "violacoes": [list(v_[:3]) for v_ in t_["violacoes"][:5]]}
        except Exception as e_:   # noqa: BLE001
            gv_[spec_["nome"]] = {"n_unidades_examinadas": 0, "n_violacoes": -1, "erro": repr(e_)[:200]}
    core_["guarda_frases_v413"] = gv_
    for spec_ in _V413_SPECS:
        try:
            core_[spec_["nome"]] = _v392_registro(spec_, core_)
        except Exception as e_:   # noqa: BLE001
            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
    return [s_["nome"] for s_ in _V413_SPECS]

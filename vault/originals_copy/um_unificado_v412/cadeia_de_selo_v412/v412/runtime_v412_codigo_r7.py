# -*- coding: utf-8 -*-
# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de runtime_v412_codigo_r5.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e7_04_derivar_texto_v412.py). O original fica intacto.
# [DERIVADO v412 r5, claude-construtor-v412 (contrato R11)] copia de runtime_v412_codigo.py; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: e5_31_derivar_gerador_r7_v412.py). O original fica intacto.
# Funcoes novas da v412 que entram no programa (a secao do artigo e a rodada dos registros por especificacao). A guarda de frases e a travessia estao em runtime_v412_guarda.py. Sem historia de conversa.


def _v412_secao_tex(lang_):
    """v412 -- a secao “O que fica claro na v412” do artigo, em 'pt' ou 'en': texto da teoria montado da pagina publica, sem numero do core (os numeros do kernel estao nos registros). Passa pela travessia da guarda de frases
    antes de ser emitido; violacao ou nenhuma unidade examinada e' falha visivel (ValueError), nunca aviso. Devolve a lista de linhas para s.append."""
    t_ = _v412_travessia("artigo:" + lang_, list(_V412_SECAO[lang_]), "tex")
    if not t_["ok"]:
        raise ValueError("a travessia da guarda de frases da v412 recusa a secao do artigo (%s): %r" % (lang_, t_["violacoes"][:3]))
    return list(_V412_SECAO[lang_])


def _v412_rodar_specs(core_):
    """v412 -- roda os cinco registros por especificacao da v412 (o motor e' o da v392: _v392_registro), na ordem de _V412_SPECS (cunhagens_v412 por ultimo: cobra o selo dos outros quatro). Antes do motor, a travessia da guarda de frases
    da v412 percorre o corpo inteiro e a palavra de veredito de cada registro (unidade por unidade) e grava o resultado em core['guarda_frases_v412'][nome]; cada registro traz a checagem obrigatoria desse resultado (zero violacao; mais de
    zero unidades examinadas), que passa pelo caminho de qualquer checagem do motor: violacao e' checagem falsa e o registro nao sela. Excecao vira AVISO visivel (all_verified False), nunca derruba o rito."""
    gv_ = {}
    for spec_ in _V412_SPECS:
        try:
            t_ = _v412_travessia("registro:" + spec_["nome"], {"corpo": {k_: spec_.get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": spec_["veredito_prefixo"] + "__" + spec_["veredito_sufixo"]})
            gv_[spec_["nome"]] = {"n_unidades_examinadas": t_["n_unidades"], "n_violacoes": len(t_["violacoes"]), "violacoes": [list(v_[:3]) for v_ in t_["violacoes"][:5]]}
        except Exception as e_:   # noqa: BLE001
            gv_[spec_["nome"]] = {"n_unidades_examinadas": 0, "n_violacoes": -1, "erro": repr(e_)[:200]}
    core_["guarda_frases_v412"] = gv_
    for spec_ in _V412_SPECS:
        try:
            core_[spec_["nome"]] = _v392_registro(spec_, core_)
        except Exception as e_:   # noqa: BLE001
            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
    return [s_["nome"] for s_ in _V412_SPECS]

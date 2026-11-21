# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\guarda_material_privado_v412_r7.py (que fica intacto): a MESMA guarda de material privado que a E03 da G1 usa, sobre TODOS os insumos pinados, ANTES do candidato.
"""guarda_material_privado_v413.py -- varre os arquivos dados (ou, sem argumento, TODOS os insumos pinados da v413) com a guarda da E03 da custodia G1 (tools\\custodia_g1\\espelho_pares.py: os termos da casa MAIS o conjunto
privado de marcadores, carregado pela funcao da propria G1; os padroes NUNCA sao impressos nem gravados). Grava GUARDA_MATERIAL_PRIVADO_v413.json (por arquivo: caminho, sha256 e a CONTAGEM de ocorrencias; nenhum trecho).
Os insumos pinados da v413: v413\\insumos (as pedras limpas, a origem, a correcao do kernel, os manifestos, as ancoras, as auditorias; a caixa de compilacao caixa_v413, de .olean ligados da v412, fica fora e o recibo diz),
as fontes do sandbox que o candidato embute (os 21 modulos e o modulo corrigido), a pagina (a do contrato e a da proposta) e a traducao, os textos gerados dela, os textos dos registros, o codigo novo do runtime, o contrato
e o molde dos marcadores herdados. rc 0 = nenhum traz material privado; rc 1 = algum traz (entra so' por COPIA LIMPA); rc 2 = a guarda nao carregou (PARAR).
A contagem da G1 sobre o candidato, o core e o kernel contra a v412 do espelho, antes do rito, e' passo da gerencia (handoff da custodia, 2.3).
uso: python -B -X utf8 guarda_material_privado_v413.py [arquivo ...]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "tools"))


def carregar_guarda():
    from custodia_g1 import espelho_pares as E   # noqa: E402   (a guarda da E03 da G1, a mesma funcao)
    return E, E.carregar_marcadores_privados()


def insumos_pinados():
    import json as _j
    ps = []
    for nome in ("CONTRATO_v413_R1.md", "O_QUE_FICA_CLARO_v413_R0_EN.md", "textos_registros_v413.py", "registros_v413.py", "runtime_v413_codigo.py", "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md",
                 "TEXTO_PUBLICO_v413.json", "BLOCOS_TEXTO_PUBLICO_v413.json", "TEXTO_PUBLICO_v413_PROPOSTA_R1.json", "BLOCOS_TEXTO_PUBLICO_v413_PROPOSTA_R1.json"):
        ps.append(os.path.join(HERE, nome))
    # (contrato R2) o contrato congelado vigente e a traducao da pagina vigente, lidos do e7_lib (nao digitados); o gerador (o texto que ele insere no candidato); as bandeiras e a medida do Audit que o candidato le
    import e7_lib_v413 as _L
    ps += [str(_L.CONTRATO), str(_L.PAGINA_EN), os.path.join(HERE, "gerar_candidato_v413.py"), str(_L.KD / "FLAGS_v413.json"), str(_L.KH_N1_V413)]
    for sub in ("o_que_fica_claro_v413", "proposta_pagina_R1"):
        d_ = os.path.join(HERE, sub)
        if os.path.isdir(d_):
            ps += [os.path.join(d_, f_) for f_ in os.listdir(d_) if f_.endswith(".md") and ".bak_" not in f_]
    ins_ = os.path.join(HERE, "insumos")
    fora = []
    for dp_, dn_, fn_ in os.walk(ins_):
        if os.path.relpath(dp_, ins_).split(os.sep)[0] == "caixa_v413":
            fora += [os.path.join(dp_, f_) for f_ in fn_]
            continue
        ps += [os.path.join(dp_, f_) for f_ in fn_ if ".bak_" not in f_ and not f_.endswith(".tmp")]
    bl = _j.load(open(os.path.join(HERE, "kernel_modulos_novos_v413.json"), encoding="utf-8"))["novos"]
    sb = os.path.join("C:" + os.sep, "t", "k413c", "final")
    ps += [os.path.join(sb, *r.split("/")) for r in bl] + [os.path.join(sb, "TGLExt", "OResumoEPsiBit.lean"), os.path.join(sb, "TGLExt.lean")]
    return sorted({p_ for p_ in ps if os.path.exists(p_)}), len(fora)


def varrer(paths):
    E, priv = carregar_guarda()
    out = []
    for p in paths:
        n = E.guarda_conta(p, priv)
        out.append({"arquivo": p, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None, "ocorrencias": n})
    return {"contrato": "GUARDA_MATERIAL_PRIVADO_v413", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "guarda": "tools\\custodia_g1\\espelho_pares.py (GUARDA + carregar_marcadores_privados + guarda_conta: a da E03)",
            "n_marcadores_privados": len(priv), "n_termos_da_casa": len(E.GUARDA), "n_arquivos": len(out), "arquivos": out,
            "com_material_privado": [x_["arquivo"] for x_ in out if x_["ocorrencias"]], "ilegiveis": [x_["arquivo"] for x_ in out if x_["ocorrencias"] is None],
            "limpo": all(x_["ocorrencias"] == 0 for x_ in out), "nota": "so' contagens; os padroes e os trechos nunca sao impressos nem gravados"}


if __name__ == "__main__":
    n_fora = None
    try:
        if sys.argv[1:]:
            paths = sys.argv[1:]
        else:
            paths, n_fora = insumos_pinados()
        rep = varrer(paths)
    except Exception as e:   # noqa: BLE001
        print("A GUARDA DE MATERIAL PRIVADO NAO CARREGOU: %s -- PARAR" % type(e).__name__)
        sys.exit(2)
    if not sys.argv[1:]:
        rep["fora_da_varredura"] = {"caixa_v413_arquivos": n_fora, "por_que": "caixa de compilacao da gerencia (.olean ligados da v412 e a copia das fontes ja' varridas em pedras_limpas e kernel_edits); nao e' insumo de texto do candidato"}
        import e7_lib_v413 as L
        import re as _re
        # analise SO' de contagens, sem padrao: os acertos se explicam por um NOME DE MODULO desta versao (identificador publico do kernel)? (troca o nome por um neutro e conta de novo)
        E_, priv_ = carregar_guarda()
        mods_ = [m.split(".")[-1] for m in L.ler_json(L.MANIFESTO)["modulos_novos"]]
        tmp_ = os.path.join(str(L.SANDBOX_PAI), "guarda_privada_tmp"); os.makedirs(tmp_, exist_ok=True)
        expl_ = {}
        for m_ in mods_:
            pw_ = os.path.join(tmp_, "nome.txt"); open(pw_, "w", encoding="utf-8").write("texto neutro " + m_ + " fim\n")
            if E_.guarda_conta(pw_, priv_):
                expl_[m_] = {"o_nome_sozinho_acusa": True, "arquivos_explicados_so_por_ele": 0, "arquivos_com_outro_acerto": []}
        for x_ in rep["arquivos"]:
            if not x_["ocorrencias"]:
                continue
            t_ = open(x_["arquivo"], "rb").read().decode("utf-8", "replace")
            for m_ in expl_:
                for f_ in _re.findall(_re.escape(m_), t_, flags=_re.I):   # (revisao M2) as formas EXATAS do nome (caixa), que uma isencao do autor teria de nomear
                    expl_[m_].setdefault("formas_exatas_nos_arquivos_acusados", {})
                    expl_[m_]["formas_exatas_nos_arquivos_acusados"][f_] = expl_[m_]["formas_exatas_nos_arquivos_acusados"].get(f_, 0) + 1
                t_ = _re.sub(_re.escape(m_), "X" * len(m_), t_, flags=_re.I)
            pw_ = os.path.join(tmp_, "sem.txt"); open(pw_, "w", encoding="utf-8").write(t_)
            resto_ = E_.guarda_conta(pw_, priv_)
            if resto_:
                for m_ in expl_:
                    expl_[m_]["arquivos_com_outro_acerto"].append(x_["arquivo"])
            else:
                for m_ in expl_:
                    expl_[m_]["arquivos_explicados_so_por_ele"] += 1
        for m_ in expl_:   # (revisao M2) quais formas exatas a guarda acusa SOZINHAS (so' contagem; o padrao nao e' impresso): as que uma isencao do autor teria de nomear
            fs_ = expl_[m_].get("formas_exatas_nos_arquivos_acusados") or {}
            acusa_ = []
            for f_ in sorted(fs_):
                pw_ = os.path.join(tmp_, "nome.txt"); open(pw_, "w", encoding="utf-8").write("texto neutro " + f_ + " fim\n")
                if E_.guarda_conta(pw_, priv_):
                    acusa_.append(f_)
            expl_[m_]["formas_que_a_guarda_acusa_sozinhas"] = acusa_
        for f_ in ("nome.txt", "sem.txt"):
            if os.path.exists(os.path.join(tmp_, f_)):
                os.remove(os.path.join(tmp_, f_))
        os.rmdir(tmp_)
        rep["analise_por_nome_de_modulo"] = {"nomes_de_modulo_que_a_guarda_acusa": expl_, "nota": "so' contagens: o nome de modulo e' identificador publico do kernel desta versao; nenhum padrao privado e' impresso; a decisao (isentar o termo, com a fala do autor por bytes, ou mudar o nome antes do selo) e' do autor (handoff da custodia, 2.3)"}
        L.salvar_json(L.D / "GUARDA_MATERIAL_PRIVADO_v413.json", rep)
    print("arquivos varridos: %d | com material privado: %d | ilegiveis: %d | marcadores privados carregados: %d" % (rep["n_arquivos"], len(rep["com_material_privado"]), len(rep["ilegiveis"]), rep["n_marcadores_privados"]))
    for a in rep["com_material_privado"]:
        print("  COM MATERIAL PRIVADO (entra so' por copia limpa):", a)
    sys.exit(0 if rep["limpo"] else 1)

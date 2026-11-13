# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026 (noite), claude-conserto-r1-v411, a servico da gerencia c1] as conferencias NOVAS do conferidor do rito: D181 (conversa nao entra no programa nem no artigo) e C-02 (o artigo em PDF e TeX)
"""conferir_conversa_v411.py -- o que o conferidor do rito (conferir_rito_v411.py) passa a conferir, em modulo proprio, depois da revisao de terceiro R1 (PEDIDO_CORRECAO_R1_v411):
  1. (D181) a guarda da conversa (guarda_conversa_v411) sobre as SAIDAS REAIS do rito (um.py, core, artigo PT e EN, forma canonica, manifesto, stdout), com os controles negativos dos dois lados;
  2. (O3) o quadro do topo NAO traz o item da fala do autor (PT, EN e .md); o conferidor RECUSA um quadro que o traga (controle negativo);
  3. (O2) a linha da v411 na saida do rito cita a ordem de abrir por data e sha16, sem o texto e sem aspas angulares (controles negativos: aspas angulares plantadas; a linha antiga com a fala; sha16 trocado);
  4. (O1) cunhagens_v411 leva as 11 falas CITADAS (data, sha256 bem formado e igual ao pino da construcao, papel, autor), sem texto, sem trecho, sem o nome do arquivo e sem a lista das falas fora do desenho (controles: um core com texto plantado);
  5. (C-02) o artigo em PDF e TeX do Nos: o .tex PT e EN traz a abertura do resumo ratificado e o titulo do quadro novo; cada .pdf tem tamanho maior que zero e data de modificacao igual ou posterior ao inicio do rito (lido de rito_horarios_v411.txt);
     um PDF velho, de compilacao que falhou calada, deixa de passar (controles dos dois lados, numa copia).
Em rito nada disto e' lido da casa: e' conferencia, depois do rito, sobre o que o rito escreveu; os textos das falas so' sao lidos pela guarda da conversa, na casa."""
import copy, datetime, json, os, re, shutil, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_conversa_v411 as GC  # noqa: E402

CAMPOS_CITADA = {"sha256", "quando", "papel", "autor", "citado_por_sha256", "texto_transcrito"}
CAMPOS_EXTRA = {"sha256", "quando", "papel", "autor", "chave"}
ITEM_DA_FALA = re.compile(r"A fala do autor|The author's words|The author’s words")


def quadro_sem_fala_do_autor(*textos_):
    """verdadeiro se NENHUM dos textos (artigo PT, artigo EN, forma canonica) traz o item da fala do autor no quadro do topo (D181, O3)."""
    return not any(ITEM_DA_FALA.search(t_ or "") for t_ in textos_)


def linha_v411_do_stdout_ok(std_, sha16_ordem_):
    """a UNICA linha da v411 na saida do rito (a que abre H0DN x BG1 ABERTO [v411) cita a ordem de abrir por data e sha16, sem o texto e sem aspas angulares (D181, O2)."""
    ls_ = [l_ for l_ in (std_ or "").splitlines() if l_.startswith("H0DN x BG1 ABERTO [v411")]
    return bool(len(ls_) == 1 and "«" not in ls_[0] and "»" not in ls_[0] and ("citada por data e sha16 " + sha16_ordem_) in ls_[0] and "OPERADOR_" not in ls_[0])


def citadas_ok(cg_, esp_cunh_, n_):
    """cunhagens_v411: as n falas CITADAS (data, sha256, papel, autor), iguais aos pinos da construcao, sem texto, sem trecho, sem o nome do arquivo e sem a lista das falas fora do desenho (O1)."""
    vb_ = cg_.get("verbatim") or {}; ex_ = cg_.get("extras") or {}; fc_ = ex_.get("falas_citadas") or []
    cru_ = json.dumps(cg_, ensure_ascii=False)
    return bool(len(vb_) == len(esp_cunh_) == n_ and set(vb_) == set(esp_cunh_)
                and all(isinstance(v_, dict) and set(v_) == CAMPOS_CITADA and re.fullmatch(r"[0-9a-f]{64}", str(v_.get("sha256"))) and v_["sha256"] == esp_cunh_[k_]["sha256"] and v_["quando"] == esp_cunh_[k_]["quando"]
                        and v_["papel"] == esp_cunh_[k_]["papel"] and v_["autor"] == esp_cunh_[k_]["autor"] == "operador" and v_["citado_por_sha256"] is True and v_["texto_transcrito"] is False for k_, v_ in vb_.items())
                and len(fc_) == n_ and all(set(x_) == CAMPOS_EXTRA for x_ in fc_) and {x_["sha256"] for x_ in fc_} == {v_["sha256"] for v_ in vb_.values()}
                and "falas_fora_do_desenho" not in ex_ and sorted((ex_.get("autores") or {})) == sorted(vb_) and all(a_ == "operador" for a_ in (ex_.get("autores") or {}).values())
                and not any(m_ in cru_ for m_ in ('"text"', '"trechos"', '"embedded_ok"', "OPERADOR_", "_verbatim.txt")))


def _horarios(hor_path_):
    h_ = open(hor_path_, encoding="utf-8").read().split()
    if len(h_) < 2:
        return None
    fim_ = datetime.datetime.fromtimestamp(os.path.getmtime(hor_path_)); t0_ = datetime.datetime.strptime(h_[0], "%H:%M:%S").time()
    ini_ = datetime.datetime.combine(fim_.date(), t0_)
    return ini_ - datetime.timedelta(days=1) if ini_ > fim_ else ini_


def pdf_tex_ok(nos_, hor_path_, pref_, tit_):
    """(C-02) o .tex PT e EN do Nos traz a abertura do resumo ratificado e o titulo do quadro novo; cada .pdf tem tamanho > 0 e mtime >= o inicio do rito. pref_ e tit_ = {"pt": ..., "en": ...} (o PDF nao e' lido por conteudo)."""
    if not hor_path_ or not os.path.exists(hor_path_):
        return False
    ini_ = _horarios(hor_path_)
    if ini_ is None:
        return False
    for l_ in ("pt", "en"):
        tp_ = os.path.join(nos_, "um_absoluto_%s.tex" % l_); pp_ = os.path.join(nos_, "um_absoluto_%s.pdf" % l_)
        if not (os.path.exists(tp_) and os.path.exists(pp_)):
            return False
        tex_ = re.sub(r"\s+", " ", open(tp_, encoding="utf-8", errors="replace").read())
        if not (pref_.get(l_) and re.sub(r"\s+", " ", pref_[l_]) in tex_ and tit_.get(l_) and re.sub(r"\s+", " ", tit_[l_]) in tex_):
            return False
        if not (os.path.getsize(pp_) > 0 and datetime.datetime.fromtimestamp(os.path.getmtime(pp_)) >= ini_):
            return False
    return True


def _controles_pdf_tex(nos_, hor_path_, pref_, tit_):
    """os dois lados, numa COPIA (nada e' escrito no Nos): o caso base passa; PDF velho, PDF vazio, TeX sem a abertura e TeX sem o titulo reprovam."""
    out_ = {}
    ini_ = _horarios(hor_path_)
    with tempfile.TemporaryDirectory() as td_:
        for l_ in ("pt", "en"):
            for ext_ in ("tex", "pdf"):
                shutil.copy2(os.path.join(nos_, "um_absoluto_%s.%s" % (l_, ext_)), os.path.join(td_, "um_absoluto_%s.%s" % (l_, ext_)))
        out_["base_passa"] = pdf_tex_ok(td_, hor_path_, pref_, tit_)
        p_ = os.path.join(td_, "um_absoluto_pt.pdf"); m0_ = os.path.getmtime(p_)
        velho_ = (ini_ - datetime.timedelta(hours=1)).timestamp(); os.utime(p_, (velho_, velho_)); out_["pdf_velho_reprova"] = not pdf_tex_ok(td_, hor_path_, pref_, tit_)
        os.utime(p_, (m0_, m0_)); out_["restaurado_passa"] = pdf_tex_ok(td_, hor_path_, pref_, tit_)
        open(p_, "wb").close(); os.utime(p_, (m0_, m0_)); out_["pdf_vazio_reprova"] = not pdf_tex_ok(td_, hor_path_, pref_, tit_)
        shutil.copy2(os.path.join(nos_, "um_absoluto_pt.pdf"), p_)
        t_ = os.path.join(td_, "um_absoluto_en.tex"); tx_ = open(t_, encoding="utf-8", errors="replace").read()
        open(t_, "w", encoding="utf-8").write(tx_.replace(re.sub(r"\s+", " ", pref_["en"])[:30], "XXXX", 1) if re.sub(r"\s+", " ", pref_["en"])[:30] in tx_ else tx_ + "")
        out_["tex_sem_a_abertura_reprova"] = not pdf_tex_ok(td_, hor_path_, pref_, tit_)
        shutil.copy2(os.path.join(nos_, "um_absoluto_en.tex"), t_)
        t2_ = os.path.join(td_, "um_absoluto_pt.tex"); tx2_ = open(t2_, encoding="utf-8", errors="replace").read()
        open(t2_, "w", encoding="utf-8").write(tx2_.replace(tit_["pt"][:30], "YYYY"))
        out_["tex_sem_o_titulo_reprova"] = not pdf_tex_ok(td_, hor_path_, pref_, tit_)
    out_["ok"] = all(out_.values())
    return out_


def avaliar(nos_, core_, std_, raw_txt_, fc_, mf_, um_bytes_, esp_, n_falas_, sha16_ordem_, pref_, tit_, hor_path_):
    """devolve {item: bool, ..., "detalhe": {...}}; nenhum texto de fala e' escrito no detalhe."""
    r_ = {}; det_ = {}
    # 1. a guarda da conversa sobre as saidas reais
    alvos_ = {"um_py": um_bytes_, "core": open(os.path.join(nos_, "um_absoluto.json"), "rb").read(), "pt": raw_txt_["pt"], "en": raw_txt_["en"], "md": fc_, "manifest": mf_, "stdout": std_}
    v_ = GC.verificar(alvos_); cn_ = GC.controle_negativo(alvos_, limpo_=v_)
    r_["conversa"] = bool(v_["ok"] and cn_["ok"]); det_["conversa"] = {"achados": v_["achados"][:10], "n_achados": len(v_["achados"]), "informativo": v_["informativo"][:10], "controle_negativo": cn_}
    # 2. O3: o quadro sem o item da fala do autor, e o conferidor recusa um quadro que o traga
    base_ = quadro_sem_fala_do_autor(raw_txt_["pt"], raw_txt_["en"], fc_)
    c1_ = not quadro_sem_fala_do_autor(raw_txt_["pt"] + "\nA fala do autor [INPUT] (12/11/2026)", raw_txt_["en"], fc_); c2_ = not quadro_sem_fala_do_autor(raw_txt_["pt"], raw_txt_["en"] + "\nThe author's words [INPUT] (12 Nov 2026)", fc_)
    c3_ = not quadro_sem_fala_do_autor(raw_txt_["pt"], raw_txt_["en"], fc_ + "\n> - **A fala do autor** [INPUT]")
    r_["sem_fala_do_autor"] = bool(base_ and c1_ and c2_ and c3_); det_["sem_fala_do_autor"] = {"base": base_, "recusa_pt": c1_, "recusa_en": c2_, "recusa_md": c3_}
    # 3. O2: a linha da v411 no stdout
    linha_ = [l_ for l_ in (std_ or "").splitlines() if l_.startswith("H0DN x BG1 ABERTO [v411")]
    base_s_ = linha_v411_do_stdout_ok(std_, sha16_ordem_)
    if linha_:
        ang_ = linha_v411_do_stdout_ok(std_.replace(linha_[0], linha_[0].replace("citada por data e sha16", "«x» citada por data e sha16", 1)), sha16_ordem_)
        velha_ = linha_v411_do_stdout_ok(std_.replace(linha_[0], linha_[0].split(" citada por data")[0] + " («xxxxxxxx»)"), sha16_ordem_)
        troc_ = linha_v411_do_stdout_ok(std_.replace(linha_[0], linha_[0].replace(sha16_ordem_, "0" * 16, 1)), sha16_ordem_)
    else:
        ang_ = velha_ = troc_ = True
    r_["linha_da_v411_no_stdout"] = bool(base_s_ and not ang_ and not velha_ and not troc_); det_["linha_da_v411_no_stdout"] = {"base": base_s_, "angulares_plantadas_recusadas": not ang_, "linha_antiga_recusada": not velha_, "sha16_trocado_recusado": not troc_}
    # 4. O1: cunhagens_v411 citadas
    cg_ = core_.get("cunhagens_v411") or {}
    ok_c_ = citadas_ok(cg_, esp_["cunhagens"], n_falas_)
    a1_ = copy.deepcopy(cg_); (list((a1_.get("verbatim") or {}).values()) or [{}])[0]["text"] = "x"
    a2_ = copy.deepcopy(cg_); (a2_.setdefault("extras", {}))["falas_fora_do_desenho"] = ["x"]
    a3_ = copy.deepcopy(cg_); (list((a3_.get("verbatim") or {}).values()) or [{}])[0]["papel"] = "OPERADOR_12nov_x"
    a4_ = copy.deepcopy(cg_); (list((a4_.get("verbatim") or {}).values()) or [{}])[0]["sha256"] = "0" * 64
    r_["cunhagens_citadas"] = bool(ok_c_ and not citadas_ok(a1_, esp_["cunhagens"], n_falas_) and not citadas_ok(a2_, esp_["cunhagens"], n_falas_) and not citadas_ok(a3_, esp_["cunhagens"], n_falas_) and not citadas_ok(a4_, esp_["cunhagens"], n_falas_))
    det_["cunhagens_citadas"] = {"base": ok_c_, "texto_plantado_recusado": not citadas_ok(a1_, esp_["cunhagens"], n_falas_), "lista_fora_do_desenho_recusada": not citadas_ok(a2_, esp_["cunhagens"], n_falas_), "nome_de_arquivo_recusado": not citadas_ok(a3_, esp_["cunhagens"], n_falas_), "sha256_trocado_recusado": not citadas_ok(a4_, esp_["cunhagens"], n_falas_)}
    # 5. C-02: PDF e TeX
    base_p_ = pdf_tex_ok(nos_, hor_path_, pref_, tit_)
    ctl_ = _controles_pdf_tex(nos_, hor_path_, pref_, tit_) if base_p_ else {"ok": False, "motivo": "o caso base nao passa"}
    r_["pdf_e_tex_do_artigo"] = bool(base_p_ and ctl_["ok"]); det_["pdf_e_tex_do_artigo"] = {"base": base_p_, "controles": ctl_, "horarios": hor_path_}
    r_["detalhe"] = det_
    return r_

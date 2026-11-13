# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026 (noite), claude-conserto-r1-v411, a servico da gerencia c1] a GUARDA DA CONVERSA (D181): conversa entre os autores nao se transcreve no programa nem no artigo
"""guarda_conversa_v411.py -- A GUARDA DA CONVERSA (D181; PEDIDO_CORRECAO_R1_v411, item I): ordem, ratificacao, pergunta e desabafo do operador (e os textos da gerencia a que ele respondeu) sao conversa interna; no programa e no
artigo entram so' CITADOS (data, sha256, papel e autor). Para cada uma das 11 falas da lista da casa (DL.FALAS_V411):
  (a) o texto normalizado inteiro e cada linha dele com 24 caracteres ou mais tem 0 ocorrencias no fonte do candidato, nas cadeias de texto do core, no artigo PT e EN (.txt), na forma canonica, no manifesto e na saida do rito;
  (b) as linhas de 12 a 23 caracteres nao ocorrem mais vezes do que no um.py da base v410 e nos rendidos selados da v410 (o alvo e' comparado com o seu correspondente: coincidencia com texto antigo nao e' transcricao nova);
  (c) os nomes dos 11 arquivos e o da ordem de 12/11 sobre a conversa (e os radicais, sem o sufixo) tem 0 ocorrencias.
Os textos das falas sao lidos da CASA so' por esta guarda, na preparacao e na conferencia; NUNCA em rito (o um.py nao le nada da casa para isto). Este modulo NUNCA escreve texto de fala: os achados e o JSON dizem so' o indice da fala, o sha16 da linha,
o tamanho, o tipo de alvo e a contagem. Os pinos da (b) ficam em GUARDA_CONVERSA_BASE_v410.json (contagens por sha16 da linha normalizada; nenhum texto).
Controle negativo dos dois lados (controle_negativo): uma copia com uma linha plantada (e outra com um nome de arquivo plantado, e outra com a linha curta alem da base) e' RECUSADA; o candidato limpo passa.
Informativo (nao reprova): fragmentos de 40 caracteres ou mais, de frases das falas, achados nos alvos (so' o indice e o tamanho).
uso: python -B -X utf8 guarda_conversa_v411.py --candidato            (p00: o fonte do candidato + os controles; rc 1 se achado)
     python -B -X utf8 guarda_conversa_v411.py --rendidos <pasta>     (ensaio a seco / conferencia: core, artigo PT e EN, forma canonica, manifesto, stdout e um.py da pasta)
     python -B -X utf8 guarda_conversa_v411.py --gerar-base           (so' na preparacao, com o Nos ainda na v410 selada)"""
import copy, hashlib, json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402

BASE_JSON = os.path.join(HERE, "GUARDA_CONVERSA_BASE_v410.json")
ARQS_RENDIDOS = {"um_py": "um.py", "core": "um_absoluto.json", "pt": "um_absoluto_pt.txt", "en": "um_absoluto_en.txt", "md": "um_absoluto_forma_canonica.md", "manifest": "um_absoluto_manifest.md", "stdout": "rodada_v411_stdout.txt"}
ARQS_V410 = dict(ARQS_RENDIDOS, stdout="rodada_v410_stdout.txt")
MIN_LONGA, MIN_CURTA, MIN_FRAG = 24, 12, 40


def _norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(s))).strip()


def _sha16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _falas():
    """[(indice, nome, texto_cru)] lido do ARQUIVO da casa (os bytes, com o sha256 conferido contra o delta); mais a ordem de 12/11 sobre a conversa (so' para o nome)."""
    out = []
    for i_, f_ in enumerate(DL.FALAS_V411):
        b_ = open(f_["arquivo"], "rb").read()
        assert hashlib.sha256(b_).hexdigest() == f_["sha256"], "o arquivo da fala %d nao e' o do delta" % i_
        out.append((i_, f_["nome"], b_.decode("utf-8")))
    return out


def _agulhas():
    """as agulhas por fala: longas (o texto normalizado inteiro e cada linha >= 24) e curtas (linhas de 12 a 23); os nomes (11 + a ordem sobre a conversa; o nome e o radical)."""
    longas, curtas, frags, nomes = [], [], [], []
    for i_, nome_, t_ in _falas():
        ls_ = [_norm(l_) for l_ in t_.splitlines() if l_.strip()]
        todo_ = _norm(t_)
        ag_ = [todo_] if len(todo_) >= MIN_LONGA else []
        ag_ += [l_ for l_ in ls_ if len(l_) >= MIN_LONGA and l_ != todo_]
        for a_ in dict.fromkeys(ag_):
            longas.append((i_, a_))
        for l_ in dict.fromkeys(ls_):
            if MIN_CURTA <= len(l_) < MIN_LONGA:
                curtas.append((i_, l_))
        for fr_ in dict.fromkeys(x_.strip() for x_ in re.split(r"(?<=[.!?;])\s+", todo_)):
            if len(fr_) >= MIN_FRAG and fr_ != todo_ and fr_ not in ls_:
                frags.append((i_, fr_))
        nomes.append((i_, nome_))
    rg_ = DL.FALA_REGRA_CONVERSA_V411["nome"]
    nomes.append((len(nomes), rg_))
    nm_ = []
    for i_, n_ in nomes:
        nm_ += [(i_, n_), (i_, re.sub(r"_verbatim\.txt$|\.txt$", "", n_))]
    return longas, curtas, frags, nm_


def _formas(a_):
    """as formas em que uma agulha pode aparecer em texto de programa: crua, escapada em JSON (com e sem unicode), escapada em repr."""
    return list(dict.fromkeys([a_, json.dumps(a_, ensure_ascii=False)[1:-1], json.dumps(a_)[1:-1], repr(a_)[1:-1], repr(a_ + "'")[1:-2]]))


def _cadeias_do_core(o_, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o_, str):
        acc.append(o_)
    elif isinstance(o_, dict):
        for k_, v_ in o_.items():
            acc.append(str(k_)); _cadeias_do_core(v_, acc)
    elif isinstance(o_, (list, tuple)):
        for v_ in o_:
            _cadeias_do_core(v_, acc)
    return acc


def _alvo_texto(tipo_, conteudo_):
    """devolve (cruo, normalizado) para um alvo; o core entra como a juncao das suas cadeias de texto (separadas por quebra de linha)."""
    if tipo_ == "core":
        obj_ = conteudo_ if not isinstance(conteudo_, (bytes, str)) else json.loads(conteudo_.decode("utf-8") if isinstance(conteudo_, bytes) else conteudo_)
        raw_ = "\n".join(_cadeias_do_core(obj_))
    else:
        raw_ = conteudo_.decode("utf-8") if isinstance(conteudo_, bytes) else str(conteudo_)
    if tipo_ == "um_py":   # (fonte Python: o pprint parte a cadeia longa em literais adjacentes, 'parte um '\n    'parte dois'; juntar os literais antes de normalizar, senao a fala embutida passaria)
        return raw_, re.sub(r"\s+", " ", unicodedata.normalize("NFC", re.sub(r"""['"]\s*\r?\n\s*['"]""", "", raw_)))
    return raw_, _norm(raw_)


def _conta(raw_, nz_, a_):
    """ocorrencias da agulha (cada forma, no cru e no normalizado); o MAIOR valor (nao soma as formas: a mesma ocorrencia aparece em mais de uma)."""
    return max([raw_.count(f_) for f_ in _formas(a_)] + [nz_.count(f_) for f_ in _formas(_norm(a_))] + [0])


def contagens_curtas(alvos_):
    """{sha16 da linha: {tipo: contagem}} das linhas curtas das falas nos alvos dados ({tipo: conteudo}); sem texto."""
    _, curtas_, _, _ = _agulhas()
    out_ = {}
    for tipo_, c_ in alvos_.items():
        raw_, nz_ = _alvo_texto(tipo_, c_)
        for i_, l_ in curtas_:
            out_.setdefault(_sha16(l_), {"fala": i_, "len": len(l_)})[tipo_] = _conta(raw_, nz_, l_)
    return out_


def _le(p_, tipo_):
    return open(p_, "rb").read()


def gerar_base():
    """(preparacao, com o Nos AINDA na v410 selada) as contagens das linhas curtas no um.py da base v410 e nos rendidos selados da v410 (pino da regra (b)); so' sha16 e contagens."""
    nos_ = DL.NOS
    um_ = open(os.path.join(nos_, "um.py"), "rb").read()
    assert hashlib.sha256(um_).hexdigest()[:16] == DL.BASE_SHA16_DA_ORDEM, "o Nos nao esta' na v410 selada: a base da regra (b) so' se gera antes do rito"
    assert um_ == open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read()
    alvos_ = {t_: _le(os.path.join(nos_, n_), t_) for t_, n_ in ARQS_V410.items()}
    out_ = {"contrato": "GUARDA_CONVERSA_BASE_v410", "nota": "contagens, por sha16 da linha normalizada, das linhas de 12 a 23 caracteres das 11 falas no um.py da base v410 e nos rendidos selados da v410 (regra (b)); nenhum texto de fala", "base_sha16": DL.BASE_SHA16_DA_ORDEM,
            "arquivos": {t_: {"nome": ARQS_V410[t_], "sha16": hashlib.sha256(c_).hexdigest()[:16], "bytes": len(c_)} for t_, c_ in alvos_.items()}, "linhas": contagens_curtas(alvos_)}
    open(BASE_JSON + ".tmp", "w", encoding="utf-8").write(json.dumps(out_, ensure_ascii=False, indent=1)); os.replace(BASE_JSON + ".tmp", BASE_JSON)
    return out_


def base():
    if os.path.exists(BASE_JSON):
        b_ = json.load(open(BASE_JSON, encoding="utf-8"))
        _, curtas_, _, _ = _agulhas()
        if set(b_["linhas"]) == {_sha16(l_) for _, l_ in curtas_} and b_.get("base_sha16") == DL.BASE_SHA16_DA_ORDEM:
            return b_
    return gerar_base()


def verificar(alvos_, base_=None):
    """alvos_ = {tipo: conteudo (bytes|str|obj)}; tipos: um_py, core, pt, en, md, manifest, stdout. Devolve {ok, achados, informativo, alvos}; fail-closed: base ausente => recusa."""
    base_ = base() if base_ is None else base_
    longas_, curtas_, frags_, nomes_ = _agulhas()
    achados_, info_, alvos_info_ = [], [], {}
    for tipo_, c_ in alvos_.items():
        raw_, nz_ = _alvo_texto(tipo_, c_)
        alvos_info_[tipo_] = {"chars": len(raw_)}
        for i_, a_ in longas_:
            n_ = _conta(raw_, nz_, a_)
            if n_:
                achados_.append({"regra": "a", "alvo": tipo_, "fala": i_, "linha_sha16": _sha16(a_), "tamanho": len(a_), "ocorrencias": n_})
        for i_, l_ in curtas_:
            n_ = _conta(raw_, nz_, l_); permitido_ = ((base_.get("linhas") or {}).get(_sha16(l_)) or {}).get(tipo_)
            if permitido_ is None:
                achados_.append({"regra": "b", "alvo": tipo_, "fala": i_, "linha_sha16": _sha16(l_), "tamanho": len(l_), "ocorrencias": n_, "permitido": None, "motivo": "a base v410 nao traz a contagem deste alvo: recusa"})
            elif n_ > permitido_:
                achados_.append({"regra": "b", "alvo": tipo_, "fala": i_, "linha_sha16": _sha16(l_), "tamanho": len(l_), "ocorrencias": n_, "permitido": permitido_})
        for i_, nm_ in nomes_:
            if nm_ in raw_:
                achados_.append({"regra": "c", "alvo": tipo_, "fala": i_, "nome_sha16": _sha16(nm_), "tamanho": len(nm_), "ocorrencias": raw_.count(nm_)})
        for i_, fr_ in frags_:
            n_ = _conta(raw_, nz_, fr_)
            if n_:
                info_.append({"alvo": tipo_, "fala": i_, "fragmento_sha16": _sha16(fr_), "tamanho": len(fr_), "ocorrencias": n_})
    return {"ok": not achados_, "achados": achados_, "informativo": info_, "alvos": alvos_info_, "n_agulhas": {"longas": len(longas_), "curtas": len(curtas_), "nomes": len(nomes_), "fragmentos": len(frags_)}}


def controle_negativo(alvos_, base_=None, limpo_=None):
    """os dois lados: (1) o alvo LIMPO passa; (2) uma COPIA com uma linha de fala plantada (a regra a) e' recusada; (3) uma copia com o nome de um arquivo plantado (a regra c) e' recusada; (4) uma copia com a linha curta alem da base (a regra b) e' recusada
    (so' se alguma fala tem linha curta); (5) o caminho do core (a cadeia plantada numa estrutura) e' recusado. As copias ficam em memoria; o texto plantado nunca e' escrito."""
    base_ = base() if base_ is None else base_
    longas_, curtas_, _, nomes_ = _agulhas()
    res_ = {}
    limpo_ = verificar(alvos_, base_) if limpo_ is None else limpo_; res_["limpo_passa"] = bool(limpo_["ok"])
    plant_ = max(longas_, key=lambda x_: len(x_[1]))[1]
    for tipo_, c_ in alvos_.items():
        if tipo_ == "core":
            continue
        raw_ = c_.decode("utf-8") if isinstance(c_, bytes) else str(c_)
        raw_ = raw_[:1 << 20]   # (o plantio e' provado numa fatia de 1 MB do alvo: a verificacao e' por subcadeia, a mesma em todo o texto; a verificacao do alvo inteiro e' a do "limpo_passa")
        r1_ = verificar({tipo_: raw_ + "\n" + plant_ + "\n"}, base_); res_["linha_plantada_recusada_" + tipo_] = bool(not r1_["ok"] and any(a_["regra"] == "a" for a_ in r1_["achados"]))
        r2_ = verificar({tipo_: raw_ + "\n" + nomes_[0][1] + "\n"}, base_); res_["nome_plantado_recusado_" + tipo_] = bool(not r2_["ok"] and any(a_["regra"] == "c" for a_ in r2_["achados"]))
        if curtas_:
            l_ = curtas_[0][1]; perm_ = ((base_.get("linhas") or {}).get(_sha16(l_)) or {}).get(tipo_)
            if perm_ is not None:
                r3_ = verificar({tipo_: raw_ + "\n" + "\n".join([l_] * (perm_ + 1)) + "\n"}, base_)   # (a linha curta plantada alem do que a base v410 permite)
                res_["linha_curta_alem_da_base_recusada_" + tipo_] = bool(not r3_["ok"] and any(a_["regra"] == "b" for a_ in r3_["achados"]))
    rc_ = verificar({"core": {"a": [plant_], "b": {"c": "x"}}}, base_); res_["core_cadeia_plantada_recusada"] = bool(not rc_["ok"] and any(a_["regra"] == "a" and a_["alvo"] == "core" for a_ in rc_["achados"]))
    rc2_ = verificar({"core": {"chave_" + nomes_[1][1]: 1}}, base_); res_["core_nome_na_chave_recusado"] = bool(not rc2_["ok"] and any(a_["regra"] == "c" for a_ in rc2_["achados"]))
    res_["ok"] = all(res_.values())
    return res_


def alvos_da_pasta(pasta_, nomes_=None):
    nomes_ = nomes_ or ARQS_RENDIDOS
    out_ = {}
    for t_, n_ in nomes_.items():
        p_ = os.path.join(pasta_, n_)
        if os.path.exists(p_):
            out_[t_] = open(p_, "rb").read()
    return out_


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    modo_ = sys.argv[1] if len(sys.argv) > 1 else "--candidato"
    if modo_ == "--gerar-base":
        b_ = gerar_base(); print("base gerada:", BASE_JSON, "| linhas curtas:", len(b_["linhas"])); sys.exit(0)
    if modo_ == "--candidato":
        alvos_ = {"um_py": open(DL.CANDIDATO_ARQ, "rb").read()}
    elif modo_ == "--rendidos":
        alvos_ = alvos_da_pasta(sys.argv[2]); assert alvos_, "nenhum arquivo na pasta"
    else:
        raise SystemExit("modo desconhecido")
    v_ = verificar(alvos_); cn_ = controle_negativo(alvos_)
    out_ = {"contrato": "GUARDA_CONVERSA_v411", "modo": modo_, "alvos": v_["alvos"], "ok": bool(v_["ok"] and cn_["ok"]), "limpo": v_["ok"], "achados": v_["achados"][:40], "n_achados": len(v_["achados"]), "informativo": v_["informativo"][:20], "controle_negativo": cn_, "n_agulhas": v_["n_agulhas"]}
    destino_ = os.path.join(HERE, "GUARDA_CONVERSA_v411.json") if modo_ == "--candidato" else None
    if destino_:
        open(destino_ + ".tmp", "w", encoding="utf-8").write(json.dumps(out_, ensure_ascii=False, indent=1)); os.replace(destino_ + ".tmp", destino_)
    print(json.dumps({k_: out_[k_] for k_ in ("modo", "ok", "limpo", "n_achados", "controle_negativo", "n_agulhas")}, ensure_ascii=False)[:1500])
    for a_ in v_["achados"][:12]:
        print("ACHADO", a_)
    sys.exit(0 if out_["ok"] else 1)

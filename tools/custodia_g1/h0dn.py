# -*- coding: utf-8 -*-
"""O TESTE H0DN × BG1 ABERTO, na custódia (12/11/2026, claude-site-custodia; de acordo da gerência c1, 12/11/2026).

Depois da abertura de 12/11/2026 (uma vez, depois do pré-registro público), os moldes fixos da G1 que diziam «β_TGL na natureza a 5σ é o
passo aberto» ficam falsos. Este módulo diz QUANDO isso vale e confere o texto que os substitui:

  - `registro_aberto(core)`: o registro `h0dn_bg1_vNNN` mais novo do core selado com `opened_once = true` (None se nenhum foi aberto;
    aí tudo segue como antes, byte a byte);
  - `valores(reg)`: o contrato do registro (congelado pela gerência c1 em 12/11), lido e conferido; chave ausente = ValueError;
  - `f67(texto)`: a regra F67 da guarda de frases da cadeia da v411, COPIADA da `runtime_h0dn_v411.py` do construtor (sha16 cfb06122e4568f05
    na leitura de 12/11; AO LADO, 13/11: o gatilho foi recopiado da sha16 f9dab163f5d5b7fe, com o cifrão opcional depois do Z), só a parte da F67: no mesmo bloco em que aparecer o Z do primário contra o nulo, a cabeça do teste ou «provado na
    natureza» ligado a este teste, têm de estar «sob o modelo de erros publicado», as Cefeidas livres com o número, «validade, não
    creditação», «retrodição» e «não cego» (ou as formas EN). O teste `testar_h0dn_marcadores.py` confere a cópia contra o controle
    congelado da cadeia (`GUARDA_FRASES_v411.json`);
  - `conferir_bloco(texto, V, rotulo, painel)`: F67 + os números da prosa contra o registro + a cabeça exata + o σ inteiro.

Os textos nunca são escritos aqui: vêm VERBATIM do handoff, pelos marcadores `<!-- INICIO_<ID>_vNNN -->`. Sem o marcador, quem chama PARA.
Nada aqui afrouxa o portão de textos (`textos.portao`) nem a P18: os dois seguem valendo sobre os mesmos textos."""
import re

RX_REG = re.compile(r"^h0dn_bg1_(v\d{3})$")

# os marcadores que o handoff traz quando o teste foi aberto (nomes da gerência c1, 12/11/2026)
MARCADOR_NOTA = "NOTA_EN"                                   # a NOTA do ledger (textos.construir)
MARCADORES_README = ("README_PAINEL_H0DN",                  # o painel do topo, EN e PT (sobe acima do da Fase 9 V2)
                     "README_FASE9_V2",                     # a linha EN e a PT de registro da Fase 9 V2, logo abaixo (o painel inteiro desce para REGISTRO_FASE9_V2.md)
                     "README_PRIMORDIAL_5SIGMA",            # a frase da linha «PROVED = validity …; β_TGL in nature at 5σ is the open step.»
                     "README_STATUS_5SIGMA",                # a frase do b_status, EN e PT («What nature decides is not proved: …»)
                     "README_H0DN",                         # o parágrafo do H0DN dentro da parte P = nP (hoje diz que o teste não foi aberto)
                     "README_H0DN_EN",                      # a linha EN do H0DN na mesma parte («**The H0DN × BG1 test:** …»; AO LADO 12/11, pedido da c1)
                     "README_RITOS",                      # a linha (ou as linhas) da tabela dos ritos no lugar da linha da Fase 9 V2
                     "README_APOIOS_FECHO")               # (13/11) o fecho do bloco dos três apoios, no lugar de «What nature decides is not proved: the decisive open factor…»
# os onze textos do estatuto (de acordo da gerência c1, 12/11/2026): um por chave do estatuto_tres_apoios.py, mais as duas linhas do P2 do
# gerar_estado_atual.py. Os trechos que cada um substitui foram EXTRAÍDOS por script (work/custodia_v411_preparo_12nov/extrair_trechos_estatuto_12nov.py)
# do texto que os geradores produziam em 12/11/2026, para h0dn_trechos_estatuto.json; nada aqui é digitado.
import json as _json
from pathlib import Path as _Path
TRECHOS = _json.loads((_Path(__file__).resolve().parent / "h0dn_trechos_estatuto.json").read_text(encoding="utf-8"))
MARCADORES_ESTATUTO = tuple(TRECHOS["marcadores"])          # ESTATUTO_<CHAVE> (nove) + ESTATUTO_P2_EN + ESTATUTO_P2_PT
# AO LADO (13/11/2026, claude-site-custodia; a vitrine, parte 2; ordem e ratificação do operador de 13/11; de acordo e travas da gerência c1): os textos da vitrine que o E04
# confere e grava em tools/estatuto_h0dn.json v2 (as trocas de chave sem encaixe, as trocas por superfície e os textos lidos por id).
MARCADORES_VITRINE = tuple(TRECHOS.get("vitrine") or ())
TODOS = (MARCADOR_NOTA,) + MARCADORES_README + MARCADORES_ESTATUTO + MARCADORES_VITRINE

# as chaves do contrato (mensagem da gerência c1, 12/11/2026): topo, values.primario, values.cefeidas_livres, values.atos
_PRIMARIO = ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo")
_CEFEIDAS = ("z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo")
_TOPO = ("verdict", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide")


def registro_aberto(core):
    """(nome, registro) do h0dn_bg1_vNNN mais novo com opened_once is True, ou None."""
    abertos = []
    for k, r in (core or {}).items():
        m = RX_REG.match(k)
        if m and isinstance(r, dict) and r.get("opened_once") is True:
            abertos.append((m.group(1), k, r))
    if not abertos:
        return None
    abertos.sort()
    return abertos[-1][1], abertos[-1][2]


def _folhas(o, acc):
    """Acumula em `acc` (como float) toda folha numérica de um objeto do registro (bool não é número)."""
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        acc.append(float(o))
    elif isinstance(o, dict):
        for v_ in o.values():
            _folhas(v_, acc)
    elif isinstance(o, list):
        for v_ in o:
            _folhas(v_, acc)


def valores(reg):
    """O contrato lido do registro (ValueError com a lista do que falta ou diverge; nunca um valor suposto)."""
    falta = []
    vals = reg.get("values") if isinstance(reg.get("values"), dict) else {}
    for k in _TOPO:
        if k not in reg:
            falta.append(k)
    if reg.get("all_verified") is not True:
        falta.append("all_verified = true")
    if reg.get("opened_once") is not True:
        falta.append("opened_once = true")
    for bloco, chaves in (("primario", _PRIMARIO), ("cefeidas_livres", _CEFEIDAS)):
        b = vals.get(bloco)
        if not isinstance(b, dict):
            falta.append("values." + bloco)
            continue
        falta += ["values.%s.%s" % (bloco, k) for k in chaves if k not in b]
    if not isinstance(vals.get("atos"), dict) or not vals.get("atos"):
        falta.append("values.atos")
    if falta:
        raise ValueError("o registro do H0DN não cumpre o contrato: " + ", ".join(falta))
    p, cf = vals["primario"], vals["cefeidas_livres"]
    div = []
    if reg["cabeca_do_teste"] != p["cabeca_do_teste"]:
        div.append("cabeca_do_teste do topo != values.primario.cabeca_do_teste")
    if reg["outcome"] != p["outcome"]:
        div.append("outcome do topo != values.primario.outcome")
    la = reg["linha_ao_lado_cefeidas_livres"]
    if not isinstance(la, dict) or la.get("z_null") != cf["z_null"]:
        div.append("linha_ao_lado_cefeidas_livres.z_null != values.cefeidas_livres.z_null")
    if not (isinstance(reg["ressalvas_secao8"], list) and len(reg["ressalvas_secao8"]) == 7):
        div.append("ressalvas_secao8 não são sete")
    for bloco, b in (("primario", p), ("cefeidas_livres", cf)):
        for k in ("z_null", "z_tgl", "D", "t"):
            if not isinstance(b[k], (int, float)) or isinstance(b[k], bool):
                div.append("values.%s.%s não é número" % (bloco, k))
    if div:
        raise ValueError("o registro do H0DN diverge de si mesmo: " + "; ".join(div))
    folhas = []   # (parte 4, M9) todas as folhas numéricas de `values`: a referência da regra «nenhum número fora do registro»
    _folhas(vals, folhas)
    return {"primario": p, "cefeidas_livres": cf, "atos": vals["atos"], "cabeca": reg["cabeca_do_teste"], "outcome": reg["outcome"],
            "verdict": reg["verdict"], "folhas": folhas}


# =================================================================== a F67 (cópia da runtime_h0dn_v411.py; só a F67)
_BLOCOS = r"\n\s*\n|\"\s*,\s*\"|\\n\\n|\"\s*:\s*\"|\"\s*\]|\[\s*\""
# AO LADO (13/11/2026, claude-site-custodia, errata pós-auditoria da v411): os dois ramos do Z ganham o `\$?` da cadeia de hoje
# (runtime_h0dn_v411.py, sha16 f9dab163f5d5b7fe, r1fix de 12/11 19:22), para casar «$Z$ contra o nulo»; a cópia de 12/11 era da sha16
# cfb06122e4568f05, sem ele. Antes: `Z\s+` nos dois ramos (backup .bak_<data>_f67_paridade).
_GATILHO = (r"prova(?:do|da)\s+na\s+natureza|proved\s+in\s+nature|PROVED_IN_NATURE|BETA_TGL_PRO|\bprim[áa]rio\b[^\n]{0,160}?contra\s+o\s+nulo|"
            r"\bprimary\b[^\n]{0,160}?against\s+the\s+null|Z\$?\s+(?:do\s+prim[áa]rio\s+)?contra\s+o\s+nulo|Z\$?\s+(?:of\s+the\s+primary\s+)?against\s+the\s+null")
_LIGADO = r"H0DN|BG1|raz[ãa]o\s+de\s+Hubble|Hubble\s+ratio|prim[áa]rio|primary|5\s*(?:σ|sigma)|SIGMA"
# AO LADO (13/11/2026, claude-site-custodia; a vitrine ratificada, ordem do operador de 13/11, sha16 334a33537f6fc30e e 648c74720e526d7f; de acordo da
# gerência c1): a F67 aprende a forma nova do resultado («N σ da razão 1») e o TERMO que o operador fixou (sha16 9e637085557d08a8).
# As duas strings da cadeia da v411 ficam guardadas, intactas, para a paridade; o gatilho e o «ligado» da G1 são elas MAIS os
# acréscimos abaixo (a cadeia os aprende na v412). O EN do termo é a forma (a) ratificada: «…lacking academic accreditation».
_GATILHO_CADEIA, _LIGADO_CADEIA = _GATILHO, _LIGADO
_TERMO_PT = r"descoberta\s+autoevidente\s+em\s+dados\s+p[úu]blicos,\s+carente\s+de\s+credita(?:ç|c)(?:ã|a)o\s+acad[êe]mica"
_TERMO_EN = r"self[-\u2010\u2011]evident\s+discovery\s+in\s+public\s+data,\s+lacking\s+academic\s+accreditation"   # (parte 4) também o hífen U+2010
_G_RATIO = (r"\d+(?:[,.]|\{,\})\d+\s*(?:σ|sigma|\\sigma\$?)\*{0,2}\s+(?:from|against|da|do|de|contra)\s+(?:the\s+|a\s+)?"
            r"(?:ratio\s+1|raz[ãa]o\s+1)")
# AO LADO (13/11/2026, claude-site-custodia; a vitrine, parte 4; achado M8 do verificador distinto): a forma «ratio 1 (ΛCDM) stands 6.11σ away» / «a razão 1 fica a
# 6,11σ» também é o resultado, e passa a disparar a regra mesmo sem a cabeça ao lado
_G_RATIO = _G_RATIO + (r"|(?:ratio\s+1|raz[ãa]o\s+1)[^\n.;]{0,30}?(?:stands|fica\s+a)\s+\*{0,2}\d+(?:[,.]|\{,\})\d+\s*\*{0,2}\s*(?:σ|sigma)")
_MARCA_TERMO = _TERMO_PT + "|" + _TERMO_EN
_GATILHO = _GATILHO_CADEIA + "|" + _G_RATIO + "|" + _MARCA_TERMO
_LIGADO = _LIGADO_CADEIA + r"|ratio\s+1|raz[ãa]o\s+1|" + _MARCA_TERMO


def blocos(texto):
    return [b for b in re.split(_BLOCOS, str(texto)) if b.strip()]


def f67(texto):
    """[(regra, trecho)]: a obrigação F67 da cadeia da v411 sobre cada bloco do texto."""
    out = []
    for seg in blocos(texto):
        gat = re.search(_GATILHO, seg, re.I)
        if gat and re.search(_LIGADO, seg, re.I):
            faltam = []
            if not re.search(r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published)|UNDER_THE_PUBLISHED_MODEL", seg, re.I):
                faltam.append("modelo_publicado")
            if not re.search(r"(?:Cefeidas\s+livres|free\s+Cepheids|FREE_CEPHEIDS)[^\n]{0,160}?(?:\d+(?:[,.]|\{,\})\d+|BELOW_5SIGMA|BRANCH_\d)", seg, re.I):
                faltam.append("cefeidas_livres_com_o_numero")
            if not re.search(r"validade,?\s+n[ãa]o\s+credita(?:ç|c)(?:ã|a)o|validity,?\s+not\s+creditation|VALIDITY_NOT_CREDITATION", seg, re.I) \
                    and not re.search(_MARCA_TERMO, seg, re.I):   # (13/11) a frase exata do termo satisfaz a marca da creditação
                faltam.append("validade_nao_creditacao")
            if not re.search(r"retrodi(?:ç|c)(?:ã|a)o|retrodiction|RETRODICTION", seg, re.I):
                faltam.append("retrodicao")
            if not re.search(r"n[ãa]o\s+(?:é\s+)?ceg[oa]|not\s+blind|NOT_BLIND", seg, re.I):
                faltam.append("nao_cego")
            if faltam:
                out.append(("F67_o_resultado_sem_as_quatro_obrigacoes:" + ",".join(faltam), seg.strip()[:200]))
    return out


# =================================================================== os números da prosa contra o registro
_RX_NUM = re.compile(r"(?<![0-9.,}])([−\-–]?)(\d+)(?:[.,]|\{,\})(\d+)(?![0-9])")


def _numeros(texto):
    """[(valor com sinal, casas decimais, trecho)] dos decimais do texto (ponto, vírgula ou o {,} do LaTeX)."""
    out = []
    for m in _RX_NUM.finditer(texto):
        v = float(m.group(2) + "." + m.group(3))
        out.append((-v if m.group(1) else v, len(m.group(3)), texto[max(0, m.start() - 30):m.end() + 10].replace("\n", " ")))
    return out


def _bate(x, nd, r):
    return round(abs(r), nd) == round(abs(x), nd)


def acervo(core):
    """AO LADO (12/11/2026, ordem do operador de ler o teste com o acervo; TOPO_RATIFICADO_v411.json da gerência c1): os números do acervo que
    os textos passam a citar, lidos do core: o livro de cobranças (estatuto_da_prova_v391.prova_2_ritos) e o teste anterior da mesma lei
    (teste_de_veracidade_fase9_v397.lido). ValueError se faltar chave ou se a soma das categorias não fechar com as cobranças."""
    try:
        p2 = core["estatuto_da_prova_v391"]["prova_2_ritos"]
        led, n, fal = p2["ledger"], p2["n_cobrancas"], p2["falsificadas"]
        f9 = core["teste_de_veracidade_fase9_v397"]["lido"]
        z_disc, z_delta, lnb = f9["z_disc_calibrado"], f9["z_delta_calibrado"], f9["lnB_lcdm"]
        cats = {k: led[k] for k in ("NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING")}
    except (KeyError, TypeError) as e:
        raise ValueError("o acervo não se lê do core (estatuto_da_prova_v391.prova_2_ritos / teste_de_veracidade_fase9_v397.lido): %r" % (e,))
    if sum(cats.values()) + fal != n or led.get("FALSIFIED", fal) != fal:
        raise ValueError("o livro de cobranças não fecha: %s + falsificadas %s != %s" % (cats, fal, n))
    return {"n_cobrancas": n, "falsificadas": fal, "categorias": cats, "z_disc": z_disc, "z_delta": z_delta, "lnB": lnb}


_RX_CATEG = {"NOT_FALSIFIED": r"(?:n[ãa]o\s+falsificadas|not\s+falsified)\s*:\s*(\d+)", "INCONCLUSIVE": r"(?:inconclusivas|inconclusive)\s*:\s*(\d+)",
             "AWAITING": r"(?:[àa]\s+espera\s+de\s+dados?|awaiting\s+data)\s*:\s*(\d+)", "EXCLUDED_IN_READING": r"(?:exclu[íi]das\s+na\s+leitura|excluded\s+in\s+reading)\s*:\s*(\d+)"}


def _conferir_acervo(texto, A, rotulo):
    viol = []
    for m in re.finditer(r"\b(\d+)\s+(?:cobran[çc]as|(?:pre-registered\s+)?charges)\b", texto, re.I):
        if int(m.group(1)) != A["n_cobrancas"]:
            viol.append("%s: %s cobranças no texto, mas o livro tem %d" % (rotulo, m.group(1), A["n_cobrancas"]))
    if re.search(r"nenhuma\s+(?:foi\s+)?falsificada|none\s+(?:was\s+)?falsified|nenhuma\s+falsificada", texto, re.I) and A["falsificadas"] != 0:
        viol.append("%s: «nenhuma falsificada», mas o livro tem %d falsificada(s)" % (rotulo, A["falsificadas"]))
    for cat, rx in _RX_CATEG.items():
        for m in re.finditer(rx, texto, re.I):
            if int(m.group(1)) != A["categorias"][cat]:
                viol.append("%s: %s = %s no texto, mas o livro diz %d" % (rotulo, cat, m.group(1), A["categorias"][cat]))
    return viol


_RX_DEC = re.compile(r"(?<![0-9A-Za-z.,}/:_])([−\-–]?)(\d+)(?:[.,]|\{,\})(\d+)(?![0-9/])")


def numeros_fora_do_registro(texto, V, rotulo, acervo=None):
    """(AO LADO (13/11/2026, claude-site-custodia; a vitrine, parte 4; achado M9 do verificador distinto) Todo decimal do texto tem de ser o arredondamento de um
    número do registro selado (qualquer folha numérica de `values`, também pela mantissa, para a notação científica), do acervo (a Fase 9
    V2) ou estar na lista dita (h0dn_trechos_estatuto.json, numeros_ditos, com a fonte de cada um). Ficam fora da regra: o milhar agrupado
    (34.300; 12,308), o DOI, o identificador colado a letra (F8.1) e a hora. Sem as folhas (um V antigo) não confere nada.
    LIMITES DITOS (o que esta regra NÃO pega): (1) um número errado que coincida com OUTRA folha do registro passa (o quase-acerto dos oito
    números do teste segue pego acima, no `conferir_bloco`); (2) a perda do SINAL passa («0.61» sem o menos: a regra compara o módulo, e o
    «± 0,81» publicado tem o mesmo módulo do −0,81 das Cefeidas livres); (3) um decimal de TRÊS casas com parte inteira de 1 a 3 dígitos
    diferente de zero é lido como milhar agrupado e não é conferido (74.372 errado passa); (4) a regra só vale no texto que NOMEIA o teste
    (H0DN ou BG1): parágrafo de outro teste, que também passa pelo `conferir_bloco`, fica fora. Achados do verificador distinto e do
    verificador do delta (13/11/2026)."""
    import math as _math
    # (13/11/2026, mais tarde) só no texto que nomeia o teste (H0DN ou BG1): o `conferir_bloco` também lê parágrafos de outros testes (a Fase 9 V2, o D1…),
    # cujos números não são deste registro; a primeira rodada com a regra ligada parou num deles (PARAGRAFO_README_v397)
    if not re.search(r"H0DN|BG1", texto):
        return []
    refs = [r for r in (V.get("folhas") or ()) if r != 0]
    if not refs:
        return []
    if acervo:
        refs += [float(acervo[k]) for k in ("z_disc", "z_delta", "lnB")]
    ditos, viol = TRECHOS.get("numeros_ditos") or {}, []
    for m in _RX_DEC.finditer(texto):
        ip, fp = m.group(2), m.group(3)
        if len(fp) == 3 and ip != "0" and len(ip) <= 3:
            continue   # milhar agrupado: inteiro
        lit, nd = ip + "." + fp, len(fp)
        if lit in ditos:
            continue
        x = float(lit)
        if any(abs(round(abs(r), nd) - x) < 1e-9 or abs(round(abs(r) / 10 ** _math.floor(_math.log10(abs(r))), nd) - x) < 1e-9 for r in refs):
            continue
        viol.append("%s: o número %s não é arredondamento de nenhum número do registro nem está na lista dita, em %r"
                    % (rotulo, m.group(0), texto[max(0, m.start() - 30):m.end() + 12].replace("\n", " ")))
    return viol


def conferir_bloco(texto, V, rotulo, painel=False, acervo=None):
    """Violações (lista de str; vazia = passa): F67; decimal com 2+ casas a menos de 1,5 unidade da última casa de um número do registro
    que não é o arredondamento dele (ou com o sinal trocado); cabeça BETA_TGL_… que não é a exata; «… a Nσ / at Nσ» do provado na natureza
    com N diferente do inteiro do Z do primário; no painel, a presença dos dois Z contra o nulo (primário e Cefeidas livres).
    Com `acervo` (AO LADO, 12/11/2026): as cobranças, as quatro categorias e «nenhuma falsificada» contra o livro, e os decimais do teste
    anterior (z_disc, z_δ, ln B da Fase 9 V2) entram na mesma conferência de arredondamento."""
    viol = ["%s: %s em %r" % (rotulo, r, t) for r, t in f67(texto)]
    p, cf = V["primario"], V["cefeidas_livres"]
    ref = [("primario." + k, p[k]) for k in ("z_null", "z_tgl", "D", "t")] + [("cefeidas_livres." + k, cf[k]) for k in ("z_null", "z_tgl", "D", "t")]
    if acervo:
        viol += _conferir_acervo(texto, acervo, rotulo)
        ref += [("fase9_v2." + k, acervo[k]) for k in ("z_disc", "z_delta", "lnB")]
    for x, nd, trecho in _numeros(texto):
        if nd < 2:
            continue
        for nome, r in ref:
            if abs(abs(x) - abs(r)) <= 1.5 * 10 ** (-nd) + 1e-12:
                if not _bate(x, nd, r):
                    viol.append("%s: %s no texto, mas %s = %r (arredondado a %d casas: %s) em %r" % (rotulo, x, nome, r, nd, round(abs(r), nd), trecho))
                elif x < 0 < r:
                    viol.append("%s: %s com o sinal trocado (%s = %r) em %r" % (rotulo, x, nome, r, trecho))
    for m in re.finditer(r"BETA_TGL_PRO[A-Z0-9_]*", texto):
        if m.group(0) != V["cabeca"]:
            viol.append("%s: cabeça do teste que não é a exata do registro: %r" % (rotulo, m.group(0)[:80]))
    n_sigma = int(abs(p["z_null"]))
    for m in re.finditer(r"(?:prova(?:do|da)\s+na\s+natureza|proved\s+in\s+nature)[^\n.;]{0,40}?\b(?:a|at)\s+(?:≥\s*)?(\d+)\s*(?:σ|sigma)", texto, re.I):
        if int(m.group(1)) != n_sigma:
            viol.append("%s: «provado na natureza a %sσ», mas o inteiro do Z do primário é %d" % (rotulo, m.group(1), n_sigma))
    viol += numeros_fora_do_registro(texto, V, rotulo, acervo=acervo)   # (parte 4, M9)
    if painel:
        for nome, r in (("primario.z_null", p["z_null"]), ("cefeidas_livres.z_null", cf["z_null"])):
            if not any(nd >= 1 and _bate(x, nd, r) and not x < 0 for x, nd, _ in _numeros(texto)):
                viol.append("%s: o painel não traz %s (%r) arredondado" % (rotulo, nome, r))
    return viol


# =================================================================== o E04: o estatuto dos geradores do espelho (os onze textos)
MARCA_HOOK = "estatuto_h0dn.json (AO LADO 12/11/2026, claude-site-custodia)"
_ANC_LER = "def ler(raiz=RAIZ):\n"
_ANC_RET = "    v.update(_textos(v))\n    return v\n"
# AO LADO (12/11/2026, claude-site-custodia; decisão da gerência c1): com o H0DN aberto, o ESTADO_ATUAL ganha uma seção de título próprio
# com as sete ressalvas e o que o teste não decide, VERBATIM das chaves do registro do core. A função é UMA fonte só: este texto entra
# no estatuto_tres_apoios.py (o gerar_estado_atual.py a importa de lá) e é o mesmo que a G1 executa aqui para conferir F67 e portão.
# AO LADO (13/11/2026, claude-site-custodia; D195 da gerência c1): a seção sobe para logo antes de «## The seal», logo depois do bloco
# «Proved on three supports»: a 300 mil caracteres (antes de «What is NOT proved») ela ficava fora do corte medido dos leitores de IA
# (perto de 100.000 caracteres). As linhas da seção não mudam; só o lugar. A âncora de 12/11 fica nomeada para a migração do espelho.
_ANC_SECAO_12NOV = "    L.append(\"## What is NOT proved · o que NÃO está provado `[OPEN / KNOWN / nature]`\")\n"
_ANC_SECAO = "    L.append(\"## The seal · o selo `[REAL — read from the artifact]`\")\n"
# AO LADO (13/11/2026, claude-site-custodia; D195 da gerência c1, palavras exatas dela): nenhuma SUPERFÍCIE mostra o primário sem o caminho
# para as sete ressalvas (regra da gerência do acordo de 12/11, seção 8, item 4). A linha é gerada, separada dos textos ratificados.
TITULO_SECAO_RESSALVAS = "The H0DN \u00d7 BG1 test: the seven reservations and what the test does not decide"
CAMINHO_RESSALVAS = {
    "en": "The seven reservations and what the test does not decide: %s, section \u201c" + TITULO_SECAO_RESSALVAS + "\u201d.",
    "pt": "As sete ressalvas e o que o teste n\u00e3o decide: %s, se\u00e7\u00e3o \u201c" + TITULO_SECAO_RESSALVAS + "\u201d.",
}


def caminho_ressalvas(lingua, url=None):
    """A linha de caminho para as sete ressalvas (EN ou PT), com `ESTADO_ATUAL.md` em código; com `url` (gerada por script), em link."""
    nome = "`ESTADO_ATUAL.md`"
    return CAMINHO_RESSALVAS[lingua] % (("[%s](%s)" % (nome, url)) if url else nome)
_SRC_SECAO = (
    "def h0dn_secao_estado(nome, r):\n"
    "    \"\"\"As linhas da secao do ESTADO_ATUAL com o H0DN aberto: as sete ressalvas e o que o teste nao decide, VERBATIM do registro do core.\"\"\"\n"
    "    rs, nd = r.get('ressalvas_secao8'), r.get('o_que_o_teste_nao_decide')\n"
    "    _exige(isinstance(rs, list) and len(rs) == 7 and all(isinstance(x, str) and x.strip() and '\\n' not in x for x in rs),\n"
    "           'H0DN aberto: %s.ressalvas_secao8 nao sao sete linhas de texto' % nome)\n"
    "    _exige(isinstance(nd, list) and len(nd) > 0 and all(isinstance(x, str) and x.strip() and '\\n' not in x for x in nd),\n"
    "           'H0DN aberto: %s.o_que_o_teste_nao_decide vazio ou fora do formato' % nome)\n"
    "    L = ['## The H0DN × BG1 test: the seven reservations and what the test does not decide · as sete ressalvas e o que o teste não decide '\n"
    "         '`[REAL — read from the sealed core]`', '',\n"
    "         '*Read by script from `um_absoluto.json` → `core.%s`, keys `ressalvas_secao8` and `o_que_o_teste_nao_decide`, verbatim and in Portuguese, '\n"
    "         'as registered · lidas por script do core, sem digitação.*' % nome, '',\n"
    "         '**As sete ressalvas · the seven reservations** (`ressalvas_secao8`):', '']\n"
    "    L += ['%d. %s' % (i, x) for i, x in enumerate(rs, 1)]\n"
    "    L += ['', '**O que o teste não decide · what the test does not decide** (`o_que_o_teste_nao_decide`):', '']\n"
    "    L += ['- %s' % x for x in nd]\n"
    "    return L\n")


def secao_estado(nome, reg):
    """As linhas da seção do ESTADO_ATUAL (a MESMA função que entra no espelho, executada aqui)."""
    def _exige(cond, msg):
        if not cond:
            raise ValueError(msg)
    ns = {"_exige": _exige}
    exec(compile(_SRC_SECAO, "h0dn_secao_estado", "exec"), ns)
    return ns["h0dn_secao_estado"](nome, reg)


def _hook_secao():
    """O par (âncora, código + âncora) do gerar_estado_atual.py: a seção entra logo antes de «## The seal» (D195, 13/11; em 12/11 era antes de
    «What is NOT proved»); sem registro aberto, nada."""
    novo = ("    # " + MARCA_HOOK + ": com o H0DN aberto, a secao das sete ressalvas e do que o teste nao decide, lida do core (verbatim)\n"
            "    sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
            "    from estatuto_tres_apoios import _h0dn_registro_aberto as _h0dn_ab, h0dn_secao_estado as _h0dn_secao\n"
            "    _h0dn_nome = _h0dn_ab(mundo_json.get(\"core\") or {})\n"
            "    if _h0dn_nome:\n"
            "        L.extend(_h0dn_secao(_h0dn_nome, mundo_json[\"core\"][_h0dn_nome]))\n"
            "        L.append(\"\")\n")
    return _ANC_SECAO, novo + _ANC_SECAO


def _hook_estatuto():
    """O código que entra no estatuto_tres_apoios.py (antes de `def ler`): os trechos (lidos de h0dn_trechos_estatuto.json) e a leitura de
    tools/estatuto_h0dn.json; sem registro aberto no core, não faz nada."""
    tr = "{\n" + "".join("    %r: %r,\n" % (k, v) for k, v in TRECHOS["estatuto"].items()) + "}"
    return ("# " + MARCA_HOOK + ": o teste H0DN x BG1 ABERTO (de acordo da gerencia c1). Com um h0dn_bg1_vNNN de\n"
            "# opened_once = true no core, os trechos que diziam que beta_TGL na natureza a 5 sigma e o fator decisivo aberto saem de tools/estatuto_h0dn.json,\n"
            "# gravado pela custodia (G1, E04) dos marcadores ESTATUTO_* do handoff, conferidos (F67, numeros, cabeca, portao). Sem o arquivo, ou de outra\n"
            "# versao ou registro, FALHA. Sem registro aberto, nada muda. O token P2_NOT_DETERMINED do veredito selado three_stress_tests_v387 segue\n"
            "# conferido como dado (registro historico; nao muda).\n"
            "H0DN_TRECHOS = " + tr + "\n\n\n"
            "def _h0dn_registro_aberto(core):\n"
            "    ab = sorted(k for k, r in core.items() if re.fullmatch(r'h0dn_bg1_v\\d{3}', k) and isinstance(r, dict) and r.get('opened_once') is True)\n"
            "    return ab[-1] if ab else None\n\n\n"
            "def ao_lado_h0dn(raiz=RAIZ, core=None, versao=None):\n"
            "    \"\"\"None se o H0DN nao foi aberto; senao o conteudo de tools/estatuto_h0dn.json, conferido (versao do selo, registro, chaves).\"\"\"\n"
            "    raiz = Path(raiz)\n"
            "    if core is None:\n"
            "        core = json.loads((raiz / A3 / 'um_absoluto.json').read_text(encoding='utf-8'))['core']\n"
            "    if versao is None:\n"
            "        versao = json.loads((raiz / A3 / 'um_absoluto_selo.json').read_text(encoding='utf-8')).get('um_version')\n"
            "    reg = _h0dn_registro_aberto(core)\n"
            "    if not reg:\n"
            "        return None\n"
            "    p = raiz / 'tools' / 'estatuto_h0dn.json'\n"
            "    _exige(p.is_file(), 'o H0DN foi aberto (%s) e tools/estatuto_h0dn.json nao existe: as frases do fator aberto nao saem do molde' % reg)\n"
            "    d = json.loads(p.read_text(encoding='utf-8'))\n"
            "    _exige(d.get('versao') == versao and d.get('registro') == reg, 'tools/estatuto_h0dn.json e de outra versao ou registro (%s, %s; o selo diz %s, %s)'\n"
            "           % (d.get('versao'), d.get('registro'), versao, reg))\n"
            "    falta = [k for k in list(H0DN_TRECHOS) + ['p2_en_estado', 'p2_pt_estado'] if not isinstance((d.get('textos') or {}).get(k), str)]\n"
            "    _exige(not falta, 'tools/estatuto_h0dn.json sem: ' + ', '.join(falta))\n"
            "    return d\n\n\n"
            "def _h0dn_ao_lado(v, core, versao, raiz):\n"
            "    d = ao_lado_h0dn(raiz, core, versao)\n"
            "    if not d:\n"
            "        return\n"
            "    for k, velho in H0DN_TRECHOS.items():\n"
            "        novo = d['textos'][k]\n"
            "        _exige(isinstance(v.get(k), str) and v[k].count(velho) == 1, 'H0DN aberto: o trecho do fator aberto nao esta uma vez em %s' % k)\n"
            "        _exige('\\n' not in novo and (novo.isascii() or not v[k].isascii()), 'H0DN aberto: o texto de %s quebra a linha ou perde o ASCII da chave' % k)\n"
            "        v[k] = v[k].replace(velho, novo)\n"
            "    # chaves compostas (secao_md leva o p2_en; secao_md_readme, o p_curto_en): o trecho que sobrar em QUALQUER chave sai tambem\n"
            "    novos = {}\n"
            "    for k, velho in H0DN_TRECHOS.items():\n"
            "        novos.setdefault(velho, set()).add(d['textos'][k])\n"
            "    for k2 in list(v):\n"
            "        if not isinstance(v[k2], str):\n"
            "            continue\n"
            "        for velho, ns in novos.items():\n"
            "            if velho in v[k2]:\n"
            "                _exige(len(ns) == 1, 'H0DN aberto: o trecho de %s sobra em %s com textos diferentes por chave'\n"
            "                       % ([k for k, x in H0DN_TRECHOS.items() if x == velho], k2))\n"
            "                novo = next(iter(ns))\n"
            "                _exige(novo.isascii() or not v[k2].isascii(), 'H0DN aberto: o texto que entra em %s perde o ASCII da chave' % k2)\n"
            "                v[k2] = v[k2].replace(velho, novo)\n\n\n" + _SRC_SECAO + "\n\n")


def _hook_estado():
    """As duas linhas do P2 do gerar_estado_atual.py (lidas de h0dn_trechos_estatuto.json) e o que as substitui: o texto do JSON com o
    H0DN aberto; as linhas originais, intactas, sem ele."""
    l1, l2 = TRECHOS["estado_linhas"]["p2_en_estado"], TRECHOS["estado_linhas"]["p2_pt_estado"]
    novo = ("    # " + MARCA_HOOK + ": com o H0DN aberto, as duas linhas do P2 saem de tools/estatuto_h0dn.json\n"
            "    sys.path.insert(0, str(Path(__file__).resolve().parent))\n"
            "    from estatuto_tres_apoios import ao_lado_h0dn as _ao_lado_h0dn\n"
            "    _h0dn_p2 = _ao_lado_h0dn(Path(__file__).resolve().parent.parent)\n"
            "    if _h0dn_p2:\n"
            "        L.append(_h0dn_p2[\"textos\"][\"p2_en_estado\"])\n"
            "        L.append(_h0dn_p2[\"textos\"][\"p2_pt_estado\"])\n"
            "    else:\n"
            "    " + l1 + "\n"
            "    " + l2 + "\n")
    return l1 + "\n" + l2 + "\n", novo


def _remendar_lf(p, pares, marca, ts):
    """Troca exata de bytes num arquivo de fim de linha MISTO (o estatuto_tres_apoios.py tem 9 linhas CRLF longe das âncoras): cada âncora,
    como está, tem de aparecer UMA vez; backup de bytes; temporário; o arquivo cresce."""
    from . import util
    from .util import Parar
    raw = util.ler_bytes(p)
    s = raw.decode("utf-8")
    if marca in s:
        return {"estado": "ja_aplicado", "antes": len(raw), "depois": len(raw), "backup": None}
    for velho, novo in pares:
        if s.count(velho) != 1:
            raise Parar("troca contada falhou em %s: esperado 1, achado %d: %r" % (_Path(p).name, s.count(velho), velho[:90]))
        s = s.replace(velho, novo)
    compile(s, str(p), "exec")
    r = util.escrever_atomico(p, s.encode("utf-8"), backup=True, ts=ts, exigir_cresceu=True)
    r["estado"] = "aplicado"
    return r


def estatuto_e04(TB, corpos, versao, nome_reg, V, conhecidos, ts, acervo=None, reg=None):
    """O E04 com o H0DN aberto: confere os onze marcadores ESTATUTO_* do handoff (F67, números, cabeça, σ, portão, uma linha, ASCII onde o
    trecho é ASCII), remenda uma vez o estatuto_tres_apoios.py e o gerar_estado_atual.py (marca MARCA_HOOK) e grava tools/estatuto_h0dn.json.
    Sem marcador, ou com violação, PARA. Devolve {saída: estado}."""
    from . import util, textos as _t
    from .util import Parar
    TB = _Path(TB)
    falta = ["INICIO_%s_%s" % (mk, versao) for mk in MARCADORES_ESTATUTO + MARCADORES_VITRINE if "%s_%s" % (mk, versao) not in corpos]
    if falta:
        raise Parar("o H0DN foi aberto (%s): o handoff não traz %s (o estatuto do fator aberto não sai do molde)" % (nome_reg, ", ".join(falta)))
    txt, viol = {}, []
    for mk, chave in TRECHOS["marcadores"].items():
        t = corpos["%s_%s" % (mk, versao)].strip("\n")
        if "\n" in t:
            viol.append("%s: tem de ser uma linha só" % mk)
        velho = TRECHOS["estatuto"].get(chave)
        if velho is not None and velho.isascii() and not t.isascii():
            viol.append("%s: o trecho que sai é ASCII; o texto que entra também tem de ser" % mk)
        if "{{" in t:
            viol.append("%s: traz «{{»" % mk)
        viol += conferir_bloco(t, V, mk, acervo=acervo) + _t.portao(t, conhecidos, rotulo=mk)
        txt[chave] = t
    # (13/11/2026) os textos da vitrine: uma linha (salvo os declarados multilinha), sem «{{», números e F67 contra o registro, portão
    extras = {}
    for mk in MARCADORES_VITRINE:
        t = corpos["%s_%s" % (mk, versao)].strip("\n")
        if "\n" in t and mk not in TRECHOS.get("multilinha", ()):
            viol.append("%s: tem de ser uma linha só" % mk)
        if not t.strip():   # (parte 4) texto vazio nunca vira «sem texto: sai a frase velha»
            viol.append("%s: vazio" % mk)
        if "{{" in t:
            viol.append("%s: traz «{{»" % mk)
        viol += conferir_bloco(t, V, mk, acervo=acervo) + _t.portao(t, conhecidos, rotulo=mk)
        extras[mk] = t
    if reg is None:   # AO LADO (12/11/2026): a seção do ESTADO_ATUAL sai do registro; sem ele, PARA
        raise Parar("o E04 com o H0DN aberto precisa do registro %s do core (a seção das ressalvas sai dele)" % nome_reg)
    try:
        secao = "\n".join(secao_estado(nome_reg, reg))
    except ValueError as e:
        raise Parar("a seção do ESTADO_ATUAL não sai do registro: %s" % e)
    viol += ["%s: %s" % (r_, t_[:120]) for r_, t_ in f67(secao)] + _t.portao(secao, conhecidos, rotulo="ESTADO_ATUAL/secao_h0dn")
    if viol:
        raise Parar("os marcadores do estatuto não passam", viol[:12])
    saidas = {}
    est, gea = TB / "tools" / "estatuto_tres_apoios.py", TB / "tools" / "gerar_estado_atual.py"
    saidas["estatuto_tres_apoios"] = _remendar_lf(est, [(_ANC_LER, _hook_estatuto() + _ANC_LER),
                                                        (_ANC_RET, "    v.update(_textos(v))\n    _h0dn_ao_lado(v, core, versao, raiz)   # " + MARCA_HOOK + "\n    return v\n")],
                                                  MARCA_HOOK, ts)["estado"]
    velho_e, novo_e = _hook_estado()
    saidas["gerar_estado_atual_p2"] = util.patch_bytes(gea, [(velho_e, novo_e), _hook_secao()], MARCA_HOOK, ts=ts, rot="ESTADO_P2")["estado"]
    # (13/11/2026) o gancho v2: as trocas de chave e as superfícies (estatuto_tres_apoios.py), a seção do teste e o título (gerar_estado_atual.py),
    # o llms.txt do espelho (gerar_portas.py); cada um pela marca MARCA_HOOK_V2 (uma vez)
    saidas["estatuto_tres_apoios_v2"] = _remendar_lf(est, _pares_est_v2(), MARCA_HOOK_V2, ts)["estado"]
    saidas["gerar_estado_atual_v2"] = util.patch_bytes(gea, _pares_gea_v2(), MARCA_HOOK_V2, ts=ts, rot="ESTADO_V2")["estado"]
    saidas["gerar_portas_v2"] = util.patch_bytes(TB / "tools" / "gerar_portas.py", _pares_gp_v2(), MARCA_HOOK_V2, ts=ts, rot="PORTAS_V2")["estado"]
    # (13/11/2026) v2: os textos da vitrine entram por id; as trocas e as superfícies saem RESOLVIDAS (cada `novo` já é o texto final);
    # o caminho para as sete ressalvas é GERADO aqui, com a URL do TUNEL.json do espelho (nunca digitada)
    try:
        url_estado = {x["path"]: x for x in _json.loads((TB / "TUNEL.json").read_text(encoding="utf-8"))["arquivos"]}["ESTADO_ATUAL.md"]["url"]
    except (OSError, ValueError, KeyError) as e:
        raise Parar("o TUNEL.json do espelho não dá a URL do ESTADO_ATUAL.md (o caminho das sete ressalvas não se digita): %s" % e)
    todos = dict(txt, **extras)
    todos.update({"CAMINHO_EN_MD": caminho_ressalvas("en", url_estado), "CAMINHO_PT_MD": caminho_ressalvas("pt", url_estado)})
    try:
        trocas = [{"chaves": list(x["chaves"]), "velho": x["velho"], "novo": _resolver(x["novo"], todos, x["velho"]), "de": x["novo"]} for x in TRECHOS.get("trocas", ())]
        sups = {nome: [{"velho": x["velho"], "novo": _resolver(x["novo"], todos, x["velho"]), "vezes": x.get("vezes", 1), "de": x["novo"]} for x in lst]
                for nome, lst in (TRECHOS.get("superficies") or {}).items()}
    except KeyError as e:
        raise Parar("a tabela da vitrine (h0dn_trechos_estatuto.json) cita um texto que não existe: %s" % e)
    ruins = ["troca de %s: quebra a linha" % x["chaves"] for x in trocas if "\n" in x["novo"]]
    for nome, lst in sups.items():   # cada texto que entra numa superfície passa, já resolvido, pela F67 (o portão já conferiu cada marcador; a cola é da tabela da G1)
        for x in lst:
            ruins += ["%s: %s: %s" % (nome, r_, t_[:100]) for r_, t_ in f67(x["novo"])]
    if ruins:
        raise Parar("as trocas da vitrine não passam", ruins[:12])
    d = {"schema": "ESTATUTO_H0DN_V2", "versao": versao, "registro": nome_reg,
         "gravado_por": "Central de Patentes/tools/custodia_g1/h0dn.py (E04), dos marcadores ESTATUTO_* e VITRINE_* do handoff da %s (com a vitrine ratificada por cima, se houver), conferidos" % versao,
         "regra": ("o texto de cada chave substitui SO o trecho listado em H0DN_TRECHOS (estatuto_tres_apoios.py) ou a linha do P2 (gerar_estado_atual.py); "
                   "`trocas` diz as chaves do estatuto em que cada trecho velho sai (uma vez em cada); `superficies`, o trecho que sai de cada superficie gerada"),
         "textos": todos, "trocas": trocas, "superficies": sups}
    p = TB / "tools" / "estatuto_h0dn.json"
    b = (_json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    if p.is_file() and util.ler_bytes(p) == b:
        saidas["estatuto_h0dn.json"] = "ja_aplicado"
    else:
        util.escrever_atomico(p, b, backup=True, ts=ts)
        saidas["estatuto_h0dn.json"] = "aplicado"
    return saidas


def estatuto_marca_ok(TB, versao):
    """A marca do E04 com o H0DN aberto: os dois geradores remendados e o JSON desta versão."""
    TB = _Path(TB)
    try:
        d = _json.loads((TB / "tools" / "estatuto_h0dn.json").read_text(encoding="utf-8"))
        est_, gea_ = (TB / "tools" / "estatuto_tres_apoios.py").read_text(encoding="utf-8"), (TB / "tools" / "gerar_estado_atual.py").read_text(encoding="utf-8")
        return (d.get("versao") == versao and MARCA_HOOK in est_ and MARCA_HOOK in gea_
                and d.get("schema") == "ESTATUTO_H0DN_V2" and MARCA_HOOK_V2 in est_ and MARCA_HOOK_V2 in gea_   # (13/11/2026) o gancho v2
                and MARCA_HOOK_V2 in (TB / "tools" / "gerar_portas.py").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False

# =================================================================== a vitrine ratificada (13/11/2026)
# AO LADO (13/11/2026, claude-site-custodia; a vitrine ratificada): os textos que o operador ratificou para a vitrine (e os derivados deles, com a
# tabela de origem) moram em work\custodia_G1\decisoes\VITRINE_RATIFICADA_vNNN.json e têm precedência sobre os marcadores README_* e
# ESTATUTO_* do handoff. Condições da gerência c1: vale só com o selo na versão do arquivo; arquivo de OUTRA versão presente PARA
# (nunca se aplica em silêncio); fonte pinada com sha256 diferente PARA. Sem arquivo nenhum, tudo sai como antes.
def vitrine_ratificada(cen, versao, selo_sha=None):
    """O dicionário do arquivo ratificado da versão, ou None se não houver arquivo. ValueError (PARAR) se houver arquivo de outra
    versão, se o arquivo não for desta versão ou se uma fonte pinada tiver mudado."""
    import hashlib as _hl
    pasta = _Path(cen) / "work" / "custodia_G1" / "decisoes"
    arqs = sorted(pasta.glob("VITRINE_RATIFICADA_v*.json"))
    if not arqs:
        return None
    # (13/11/2026, tarde) arquivo de versão POSTERIOR à pedida não se aplica ao passado nem o trava (reauditar a v410 com o arquivo da v411 em
    # disco); arquivo de versão ANTERIOR à pedida PARA: os marcadores do handoff novo mandam, e o arquivo antigo sai por ato dito
    if not re.fullmatch(r"v\d{3}", str(versao)):   # (parte 4) versão fora do molde PARA com mensagem
        raise ValueError("versão fora do molde vNNN: %r" % (versao,))
    _num = lambda s_: int(re.search(r"v(\d+)", s_).group(1))
    arqs = [a for a in arqs if _num(a.name) <= _num(versao)]
    if not arqs:
        return None
    outros = [a.name for a in arqs if a.name != "VITRINE_RATIFICADA_%s.json" % versao]
    if outros:
        raise ValueError("há texto ratificado da vitrine de outra versão (%s) e o selo é %s: os marcadores do handoff novo mandam; retire o arquivo por ato dito" % (", ".join(outros), versao))
    d = _json.loads(arqs[0].read_text(encoding="utf-8"))
    if d.get("versao") != versao or not isinstance(d.get("textos"), dict) or not isinstance(d.get("fontes"), dict):
        raise ValueError("VITRINE_RATIFICADA_%s.json não é desta versão ou não traz textos/fontes" % versao)
    # (parte 4) a condição (a) da gerência, conferida de fato: fontes não vazias e o um.py do selo da casa igual ao que o arquivo pinou
    if not d["fontes"]:
        raise ValueError("VITRINE_RATIFICADA_%s.json sem fontes pinadas" % versao)
    if selo_sha is None:
        from .caminhos import Caminhos as _Cam
        try:
            selo_sha = _json.loads((_Path(_Cam({}).NOS) / "um_absoluto_selo.json").read_text(encoding="utf-8"))["sha256"]["um.py"]
        except (OSError, ValueError, KeyError) as e:
            raise ValueError("o selo do Nós não se leu para conferir o arquivo ratificado da vitrine: %r" % (e,))
    if d.get("selo_um_py_sha256") != selo_sha:
        raise ValueError("o arquivo ratificado da vitrine foi feito para outro um.py (%s...) e o selo é %s...: não vale" % (str(d.get("selo_um_py_sha256"))[:16], selo_sha[:16]))
    for nome, f in d["fontes"].items():
        p = _Path(f["arquivo"])
        if not p.is_file() or _hl.sha256(p.read_bytes()).hexdigest() != f["sha256"]:
            raise ValueError("a fonte pinada «%s» do texto ratificado da vitrine sumiu ou mudou (%s)" % (nome, p))
    return d


def com_a_vitrine(corpos, rat, versao):
    """Os corpos dos marcadores do handoff com os textos ratificados por cima (chave «NOME_vNNN»). `rat` None devolve `corpos` intacto."""
    if not rat:
        return corpos
    novo = dict(corpos)
    for k, v in rat["textos"].items():
        novo["%s_%s" % (k, versao)] = v["texto"]
    return novo


# =================================================================== a vitrine, parte 2 (13/11/2026): o estatuto_h0dn.json v2 e as guardas
# AO LADO (13/11/2026, claude-site-custodia; a vitrine, parte 2; ordem e ratificação do operador de 13/11; de acordo e travas da gerência c1).
MARCA_HOOK_V2 = "estatuto_h0dn.json v2 (AO LADO 13/11/2026, claude-site-custodia)"
_RX_MODELO = re.compile(r"\{([A-Za-z0-9_]+)\}")


def _resolver(modelo, textos, velho):
    """O texto NOVO de uma troca: o modelo da tabela com {ID} trocado pelo texto do id e {velho} pelo trecho que sai. Id ausente: KeyError."""
    return _RX_MODELO.sub(lambda m: velho if m.group(1) == "velho" else textos[m.group(1)], modelo)


def _pares_est_v2():
    """O que entra no estatuto_tres_apoios.py do espelho (depois do gancho de 12/11): a exigência do JSON v2, as trocas de chave, a troca por
    superfície gerada e a leitura de um texto por id."""
    a1 = "    _exige(not falta, 'tools/estatuto_h0dn.json sem: ' + ', '.join(falta))\n"
    n1 = a1 + ("    # " + MARCA_HOOK_V2 + ": o JSON traz tambem as trocas de chave e as superficies\n"
               "    _exige(isinstance(d.get('trocas'), list) and isinstance(d.get('superficies'), dict),\n"
               "           'tools/estatuto_h0dn.json nao e v2 (sem trocas/superficies): rodar o E04 da custodia')\n")
    a2 = "                v[k2] = v[k2].replace(velho, novo)\n\n\ndef h0dn_secao_estado(nome, r):\n"
    n2 = ("                v[k2] = v[k2].replace(velho, novo)\n"
          "    # " + MARCA_HOOK_V2 + ": as trocas de chave (trechos sem encaixe proprio); cada uma diz as chaves em que entra, uma vez em cada\n"
          "    for t in d['trocas']:\n"
          "        _exige('\\n' not in t['novo'], 'H0DN aberto: a troca de %s quebra a linha' % t['chaves'])\n"
          "        for k in t['chaves']:\n"
          "            _exige(isinstance(v.get(k), str) and v[k].count(t['velho']) == 1, 'H0DN aberto: o trecho %r nao esta uma vez em %s' % (t['velho'][:50], k))\n"
          "            _exige(t['novo'].isascii() or not v[k].isascii(), 'H0DN aberto: a troca em %s perde o ASCII da chave' % k)\n"
          "            v[k] = v[k].replace(t['velho'], t['novo'])\n\n\n"
          "def h0dn_superficie(nome, texto, raiz=RAIZ):\n"
          "    \"\"\"Com o H0DN aberto, troca na superficie gerada `nome` cada trecho listado em tools/estatuto_h0dn.json (superficies[nome]), o numero\n"
          "    de vezes dito; trecho ausente, ou superficie sem lista, FALHA. Sem registro aberto, devolve o texto como veio.\"\"\"\n"
          "    d = ao_lado_h0dn(raiz)\n"
          "    if not d:\n"
          "        return texto\n"
          "    _exige(nome in d['superficies'], 'H0DN aberto: tools/estatuto_h0dn.json nao traz a superficie %s' % nome)\n"
          "    for t in d['superficies'][nome]:\n"
          "        n = texto.count(t['velho'])\n"
          "        _exige(n == t.get('vezes', 1), 'H0DN aberto: em %s o trecho %r aparece %d vez(es), esperado %d' % (nome, t['velho'][:50], n, t.get('vezes', 1)))\n"
          "        _exige(t['novo'].isascii() or not texto.isascii(), 'H0DN aberto: o texto que entra em %s tira o ASCII da superficie' % nome)\n"
          "        texto = texto.replace(t['velho'], t['novo'])\n"
          "    return texto\n\n\n"
          "def h0dn_texto(ident, raiz=RAIZ):\n"
          "    \"\"\"O texto `ident` de tools/estatuto_h0dn.json (None sem registro aberto); texto ausente FALHA.\"\"\"\n"
          "    d = ao_lado_h0dn(raiz)\n"
          "    if not d:\n"
          "        return None\n"
          "    _exige(isinstance(d['textos'].get(ident), str) and d['textos'][ident].strip() != '', 'H0DN aberto: tools/estatuto_h0dn.json sem o texto %s (ou vazio)' % ident)\n"
          "    return d['textos'][ident]\n\n\n"
          "def h0dn_secao_estado(nome, r):\n")
    return [(a1, n1), (a2, n2)]


def _pares_gea_v2():
    """O que entra no gerar_estado_atual.py: a seção do teste antes da seção das ressalvas, e as trocas de superfície (o título)."""
    a1 = "    if _h0dn_nome:\n        L.extend(_h0dn_secao(_h0dn_nome, mundo_json[\"core\"][_h0dn_nome]))\n"
    n1 = ("    if _h0dn_nome:\n"
          "        # " + MARCA_HOOK_V2 + ": antes das ressalvas, a secao do teste (texto ratificado, de tools/estatuto_h0dn.json)\n"
          "        from estatuto_tres_apoios import h0dn_texto as _h0dn_texto\n"
          "        L.extend(_h0dn_texto(\"ESTADO_SECAO_DO_TESTE_EN\", Path(__file__).resolve().parent.parent).split(\"\\n\"))\n"
          "        L.append(\"\")\n"
          "        L.extend(_h0dn_secao(_h0dn_nome, mundo_json[\"core\"][_h0dn_nome]))\n")
    a2 = "    out = RAIZ / \"ESTADO_ATUAL.md\"\n"
    n2 = ("    # " + MARCA_HOOK_V2 + ": os trechos de superficie do ESTADO_ATUAL (o titulo da secao que abrigava o resultado)\n"
          "    from estatuto_tres_apoios import h0dn_superficie as _h0dn_sup\n"
          "    L = _h0dn_sup(\"ESTADO_ATUAL.md\", \"\\n\".join(L), Path(__file__).resolve().parent.parent).split(\"\\n\")\n" + a2)
    return [(a1, n1), (a2, n2)]


def _pares_gp_v2():
    """O que entra no gerar_portas.py: as trocas de superfície do llms.txt do espelho."""
    a = "    escreve(\"llms.txt\", \"\\n\".join(T))\n"
    n = ("    # " + MARCA_HOOK_V2 + ": os trechos de superficie do llms.txt do espelho\n"
         "    from estatuto_tres_apoios import h0dn_superficie as _h0dn_sup\n"
         "    escreve(\"llms.txt\", _h0dn_sup(\"llms.txt\", \"\\n\".join(T), REPO))\n")
    return [(a, n)]


# ------------------------------------------------------------------- as duas travas da gerência c1 (13/11/2026)
_RX_CABECA_PROSA = re.compile(r"(?:β|beta)_?\s?TGL\s+(?:proved\s+in\s+nature|provad[oa]\s+na\s+natureza)", re.I)   # sobre o texto SEM as marcas de HTML
_sem_tags = lambda t: re.sub(r"<[^>]+>", "", t)
_RX_ELO = re.compile(r"one\s+link\s+that\s+was\s+pending|[úu]nico\s+elo\s+que\s+estava\s+pendente", re.I)
_RX_DUAS_LINHAS = (r"6(?:[.,]|\{,\})11", r"0(?:[.,]|\{,\})61", r"4(?:[.,]|\{,\})38", r"0(?:[.,]|\{,\})81")
_RX_CAMINHO = (r"seven\s+reservations|sete\s+ressalvas", r"ESTADO_ATUAL")
ROTULO_DO_CARTAO, TEXTO_DO_CARTAO = "pred.st.h0dn", "pred.s2"


def marcas_do_item(texto):
    """As marcas da F67 que faltam num ITEM lido como UM bloco ligado ao teste (o rótulo de um cartão com o seu texto, por exemplo). A F67 só
    dispara no bloco que nomeia o teste; um rótulo sozinho não nomeia, por isso o item é conferido com o nome do teste à frente."""
    um = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", texto))
    return sorted({m for r, _ in f67("H0DN \u00d7 BG1: " + um) for m in r.split(":", 1)[1].split(",")})


def _dicionarios_i18n(i18n):
    """[(língua, corpo)] dos dicionários do i18n.js («  en:{» … «  },»)."""
    return [(m.group(1), m.group(2)) for m in re.finditer(r"(?ms)^  ([a-z]{2}):\{\n(.*?)^  \},?[ \t]*$", i18n)]


def guarda_do_rotulo(html, i18n):
    """TRAVA 1: a cabeça em prosa («β_TGL proved in nature at 6σ») nunca aparece num item sem as cinco marcas. No index.html o item é a LINHA
    (um cartão é uma linha); no i18n.js é o valor de uma chave, e o rótulo do cartão só vale com o texto do cartão do MESMO dicionário; no
    HTML os dois têm de estar no mesmo cartão. Devolve a lista de violações."""
    out = []
    for n, ln in enumerate(html.split("\n"), 1):
        if _RX_CABECA_PROSA.search(_sem_tags(ln)):
            f = marcas_do_item(ln)
            if f:
                out.append("index.html, linha %d: a cabeça em prosa sem %s" % (n, ", ".join(f)))
        if ('data-i18n="%s"' % ROTULO_DO_CARTAO) in ln and ('data-i18n="%s"' % TEXTO_DO_CARTAO) not in ln:
            out.append("index.html, linha %d: o rótulo %s fora do cartão do %s" % (n, ROTULO_DO_CARTAO, TEXTO_DO_CARTAO))
    for ling, corpo in _dicionarios_i18n(i18n):
        chaves = dict(re.findall(r"'([a-z0-9_.]+)'\s*:\s*'((?:\\.|[^'\\])*)'", corpo))
        for k, val in chaves.items():
            if not _RX_CABECA_PROSA.search(_sem_tags(val)):
                continue
            f = marcas_do_item(val if k != ROTULO_DO_CARTAO else val + " " + chaves.get(TEXTO_DO_CARTAO, ""))
            if f:
                out.append("i18n.js [%s] %s: a cabeça em prosa sem %s" % (ling, k, ", ".join(f)))
    return out


def guarda_do_elo(superficies):
    """TRAVA 2: a frase do elo fechado («the one link that was pending … is closed …») só entra numa superfície que traz, nela mesma, um item
    com as duas linhas (o primário e as Cefeidas livres, com os números) e o caminho para as sete ressalvas. `superficies`: {nome: texto}."""
    out = []
    for nome, t in sorted(superficies.items()):
        if not _RX_ELO.search(t):
            continue
        n_f = sum(1 for r in _RX_DUAS_LINHAS if not re.search(r, t))
        if n_f:
            out.append("%s: traz a frase do elo sem as duas linhas (faltam %d dos quatro números)" % (nome, n_f))
        if not all(re.search(r, t, re.I) for r in _RX_CAMINHO):
            out.append("%s: traz a frase do elo sem o caminho para as sete ressalvas" % nome)
    return out


def superficies_de_texto(raiz, prefixo=""):
    """{nome: texto} das superfícies de texto de uma raiz (o espelho ou o disco do site): as páginas de frente, as portas e as seções."""
    raiz, out = _Path(raiz), {}
    nomes = ("README.md", "ESTADO_ATUAL.md", "ABSTRACT.md", "CITATION.cff", "PORTA.md", "read-brief.md", "read-brief.txt", "llms.txt", "llms-full.txt",
             "index.md", "index.html", "i18n.js", "estado.json", "estado.txt")
    for p in [raiz / n for n in nomes] + sorted((raiz / "secoes").glob("*.md")):
        if p.is_file():
            out[prefixo + (p.name if p.parent == raiz else "secoes/" + p.name)] = p.read_bytes().decode("utf-8", "replace")
    return out


# =================================================================== AO LADO: as guardas, corrigidas
# AO LADO (13/11/2026, claude-site-custodia; a vitrine, parte 4; achado M8 do verificador distinto, com os contra-exemplos dele em
# work\vitrine_postura_13nov\auditoria\VEREDITO_VERIFICADOR_VITRINE_13nov.md). As quatro funções de mesmo nome que estão acima ficam como
# registro; VALEM as de baixo (o nome é religado aqui). O que mudou: o texto é lido sem as marcas de HTML e com as entidades resolvidas; a
# cabeça em prosa é procurada sem exigir o nome colado («was proved in nature…» também); os dicionários do i18n.js são lidos com qualquer
# indentação e, se o rótulo existe e os dois não são achados, isso é achado; a frase do elo pede UM item com os quatro números, cada um com
# o sinal e o σ, e não quatro números soltos na superfície.
import html as _html

_RX_CABECA_PROSA = re.compile(r"proved\s+in\s+nature|provad[oa]\s+na\s+natureza", re.I)
_RX_QUATRO = (r"(?<![0-9.,])6(?:[.,]|\{,\})11\s*(?:σ|sigma)", r"[−\-–]\s?0(?:[.,]|\{,\})61\s*(?:σ|sigma)",
              r"(?<![0-9.,])4(?:[.,]|\{,\})38\s*(?:σ|sigma)", r"[−\-–]\s?0(?:[.,]|\{,\})81\s*(?:σ|sigma)")


def _limpo(t):
    """O texto sem as marcas de HTML e com as entidades resolvidas (&beta; vira β; &sigma;, σ; &minus;, −)."""
    return _html.unescape(re.sub(r"<[^>]+>", "", t))


def marcas_do_item(texto):
    """As marcas da F67 que faltam num ITEM lido como UM bloco ligado ao teste (sem marcas de HTML, entidades resolvidas)."""
    um = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", texto)))
    return sorted({m for r, _ in f67("H0DN \u00d7 BG1: " + um) for m in r.split(":", 1)[1].split(",")})


def _dicionarios_i18n(i18n):
    """{«en»: corpo, «pt»: corpo} dos dois dicionários do i18n.js, com qualquer indentação; {} se os dois não forem achados nessa ordem."""
    m_en = re.search(r"(?m)^[ \t]*['\"]?en['\"]?[ \t]*:[ \t]*\{[ \t]*$", i18n)
    m_pt = re.search(r"(?m)^[ \t]*['\"]?pt['\"]?[ \t]*:[ \t]*\{[ \t]*$", i18n)
    if not (m_en and m_pt and m_en.start() < m_pt.start()):
        return {}
    fim = re.search(r"(?m)^\};", i18n[m_pt.end():])
    return {"en": i18n[m_en.end():m_pt.start()], "pt": i18n[m_pt.end():(m_pt.end() + fim.start()) if fim else len(i18n)]}


def _chaves_i18n(corpo):
    return {m.group(1): m.group(3) for m in re.finditer(r"['\"]([A-Za-z0-9_.]+)['\"]\s*:\s*(['\"])((?:\\.|(?!\2).)*)\2", corpo)}


def guarda_do_rotulo(html, i18n):
    """TRAVA 1: a cabeça em prosa («… proved in nature at 6σ») nunca aparece num item sem as cinco marcas. No index.html o item é a LINHA (um
    cartão é uma linha); no i18n.js é o valor de uma chave, e o rótulo do cartão só vale com o texto do cartão do MESMO dicionário; no HTML os
    dois têm de estar no mesmo cartão; se o HTML usa o rótulo, os dois dicionários têm de trazer as duas chaves. Devolve a lista de violações."""
    out = []
    usa = ('data-i18n="%s"' % ROTULO_DO_CARTAO) in html
    for n, ln in enumerate(html.split("\n"), 1):
        if _RX_CABECA_PROSA.search(_limpo(ln)):
            f = marcas_do_item(ln)
            if f:
                out.append("index.html, linha %d: a cabeça em prosa sem %s" % (n, ", ".join(f)))
        if ('data-i18n="%s"' % ROTULO_DO_CARTAO) in ln and ('data-i18n="%s"' % TEXTO_DO_CARTAO) not in ln:
            out.append("index.html, linha %d: o rótulo %s fora do cartão do %s" % (n, ROTULO_DO_CARTAO, TEXTO_DO_CARTAO))
    dic = _dicionarios_i18n(i18n)
    if (usa or ROTULO_DO_CARTAO in i18n or _RX_CABECA_PROSA.search(_limpo(i18n))) and set(dic) != {"en", "pt"}:
        out.append("i18n.js: os dicionários en e pt não foram lidos; o rótulo do cartão não pode ser conferido")
    for ling, corpo in dic.items():
        chaves = _chaves_i18n(corpo)
        if usa and not (ROTULO_DO_CARTAO in chaves and TEXTO_DO_CARTAO in chaves):
            out.append("i18n.js [%s]: falta %s ou %s, e o HTML usa o rótulo" % (ling, ROTULO_DO_CARTAO, TEXTO_DO_CARTAO))
        for k, val in chaves.items():
            if not _RX_CABECA_PROSA.search(_limpo(val)):
                continue
            f = marcas_do_item(val if k != ROTULO_DO_CARTAO else val + " " + chaves.get(TEXTO_DO_CARTAO, ""))
            if f:
                out.append("i18n.js [%s] %s: a cabeça em prosa sem %s" % (ling, k, ", ".join(f)))
    return out


def _itens(nome, t):
    """Os itens de uma superfície: as linhas, num HTML (sem os blocos <script>) ou num .js; os parágrafos, nas demais."""
    if nome.lower().endswith((".html", ".htm")):
        return [_limpo(x) for x in re.sub(r"(?is)<script\b.*?</script>", "", t).split("\n")]
    if nome.lower().endswith(".js"):
        return [_limpo(x) for x in t.split("\n")]
    return re.split(r"\n[ \t]*\n", t)


def guarda_do_elo(superficies):
    """TRAVA 2: a frase do elo fechado («the one link that was pending … is closed …») só entra numa superfície que traz, nela mesma, UM item
    com as duas linhas (6,11σ e −0,61σ do primário; 4,38σ e −0,81σ das Cefeidas livres; cada número com o sinal e o σ) e o caminho para as
    sete ressalvas. `superficies`: {nome: texto}. Devolve a lista de violações."""
    out = []
    for nome, t in sorted(superficies.items()):
        if not _RX_ELO.search(t):
            continue
        if not any(all(re.search(rx, it, re.I) for rx in _RX_QUATRO) for it in _itens(nome, t)):
            out.append("%s: traz a frase do elo sem um item com as duas linhas (6,11σ, −0,61σ, 4,38σ e −0,81σ juntos)" % nome)
        if not all(re.search(r, t, re.I) for r in _RX_CAMINHO):
            out.append("%s: traz a frase do elo sem o caminho para as sete ressalvas" % nome)
    return out

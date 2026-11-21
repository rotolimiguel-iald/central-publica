# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413] do molde v412\gerar_candidato_v412_r7.py (que fica intacto), pelo contrato da v413 congelado.
"""gerar_candidato_v413.py -- gera o um.py CANDIDATO da v413 a partir da v412 SELADA (base_v412; o Nos e' so' conferido, NUNCA escrito). Molde: gerar_candidato_v412_r7.py (patches por ast; o bundle de modulos).
Conteudo (contrato da v413; nenhum texto daqui entra no programa com historia de conversa):
 (A) kernel: os 21 modulos novos em TGLExt/ embutidos em _EMBEDDED_KERNEL_FILES, do sandbox C:\\t\\k413c\\final (compilado e medido); a raiz TGLExt.lean regenerada com os 21 imports; e, NOVO na v413, o texto embutido de um
     modulo que JA' EXISTE (TGLExt/OResumoEPsiBit.lean, so' a docstring; o codigo e as declaracoes sao os mesmos) SUBSTITUIDO pelo do sandbox; as bandeiras ext_<modulo>_413_NNNN (so' declaracao nomeada) em _LEAN_THEOREM_FLAGS e na
     escada; o ledger de pedras;
 (B) UM_VERSION = v413; os literais 'expected_ladder' da escada da base sobem para a escada desta versao; o baseline da escada do contrato do H0DN; o pino da raiz do registro herdado cunhagens_v411 (u44);
 (C) runtime novo: a secao “O que fica claro na v413” (PT/EN), os seis registros por especificacao (_V413_SPECS: os cinco do contrato e a cobertura do relatorio de axiomas) e a rodada deles no main, depois dos da v412; resumo no selo. A guarda de frases e' a herdada da v412 (_v412_travessia).
 (D) artigo: a secao nova antes da secao da v412. O resumo do artigo NAO muda.
 O gate NAO muda: as funcoes do gate/neutrino e os registros anteriores ficam BYTE A BYTE (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -B -X utf8 gerar_candidato_v413.py [--seco]   (--seco: roda tudo e NAO grava o candidato; recusa -O; nunca escreve no Nos). O candidato vai para C:\\t\\k413c\\candidato\\ (fora de work\\); no modo proposta, para outra pasta."""
import ast, datetime, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SECO = "--seco" in sys.argv
import delta_v413 as DL  # noqa: E402
import e7_lib_v413 as L  # noqa: E402
import registros_v413 as RG  # noqa: E402
import guarda_frases_v413 as GF  # noqa: E402
import acom_conferencias_v413 as AC  # noqa: E402
import verificar_historia_texto_v413 as VH  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
_selo_nos = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
if _selo_nos.get("um_version") != DL.BASE_VERSION or sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != DL.BASE_SHA16_DA_ORDEM:   # o Nos ja nao e' a v412: a v412 SELADA vem da copia base_v412
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico lido nao e' a v412 selada"
SHA0 = sha16(raw); assert SHA0 == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E412 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E412 == DL.ESCADA_BASE
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]
LF_SOLTOS0 = len(re.findall(r"(?<!\r)\n", T0))


def pos(tx_ls, lineno, col_bytes, text):
    line = text[tx_ls[lineno - 1]:tx_ls[lineno]] if lineno < len(tx_ls) else text[tx_ls[lineno - 1]:]
    return tx_ls[lineno - 1] + len(line.encode("utf-8")[:col_bytes].decode("utf-8"))


def span(node):
    return pos(LS, node.lineno, node.col_offset, T0), pos(LS, node.end_lineno, node.end_col_offset, T0)


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def top(name, tree=tree0):
    c = [n for n in tree.body if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name) or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name)]
    assert len(c) == 1, (name, len(c))
    return c[0]


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


EDITS = []


def edit(a, b, novo, pid, grupo, o_que):
    EDITS.append((a, b, novo, pid, grupo, o_que))


def _nome_de_topo_em(off_):
    """(revisao B5) o nome de topo da base que contem a posicao off_ (para listar no manifesto onde mora cada literal de dado que muda)"""
    for n_ in tree0.body:
        a_, b_ = span(n_)
        if a_ <= off_ < b_:
            return nm(n_) or type(n_).__name__
    return None


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, ("ANCORA NAO UNICA", rx)
    return m_


def _controles(obj, onde):
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


def _sem_comentarios_lean(t_):
    return re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", t_, flags=re.S))


# ---------------- (1) o kernel: os 21 modulos do bundle e o modulo corrigido ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v413.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS and len(nov) == DL.N_MODULOS_DO_MANIFESTO == 21
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX, "a raiz do sandbox nao e' a da v412 + os imports do bundle"
assert new_audit == old_d["TGL/Audit.lean"], "o Audit do sandbox difere do embutido na v412 (a v413 nao o muda)"
KC = DL.KERNEL_CORRIGIDO; REL_KC = KC["rel"]
assert REL_KC in old_d and sha256(old_d[REL_KC].encode("utf-8")) == KC["sha256_antes"], "o texto embutido do modulo corrigido na base nao e' o de antes (sha256_antes)"
TXT_KC = rd(os.path.join(KB, *REL_KC.split("/")))
assert sha256(TXT_KC.encode("utf-8")) == KC["sha256_depois"] and len(TXT_KC.encode("utf-8")) == KC["bytes_depois"], "o modulo corrigido do sandbox nao e' o do bundle (sha256_depois)"
assert "\r" not in TXT_KC and "sorry" not in _sem_comentarios_lean(TXT_KC) and "#print" not in _sem_comentarios_lean(TXT_KC) and "#eval" not in _sem_comentarios_lean(TXT_KC)
assert _sem_comentarios_lean(TXT_KC) == _sem_comentarios_lean(old_d[REL_KC]), "o modulo corrigido muda codigo fora dos comentarios (so' a docstring pode mudar)"
_dif_sb = [rel for rel, txt in old_d.items() if rel not in ("TGLExt.lean", REL_KC) and (not os.path.exists(os.path.join(KB, *rel.split("/"))) or rd(os.path.join(KB, *rel.split("/"))) != txt)]
assert not _dif_sb, ("o kernel EMBUTIDO da base difere do sandbox k413c fora da raiz e do modulo corrigido", _dif_sb[:5])
BUNDLE_TXT = {}
for rel in nov:
    t_ = rd(os.path.join(KB, *rel.split("/")))
    assert sha256(t_.encode("utf-8")) == DL.BUNDLE_POR_REL[rel]["sha256"], ("o modulo do sandbox difere do que o preparo do bundle pinou", rel)
    assert rel not in old_d, rel
    assert "sorry" not in _sem_comentarios_lean(t_), "sorry no codigo do modulo " + rel
    assert "#eval" not in _sem_comentarios_lean(t_) and "#print" not in _sem_comentarios_lean(t_), "#eval/#print sobrou no modulo " + rel
    assert "\r" not in t_, "o modulo embutido tem de ser LF (o kernel e' LF)"
    BUNDLE_TXT[rel] = t_
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os imports dos modulos novos; sandbox == embutido)")
a, b = spans[REL_KC]; edit(a, b, repr(TXT_KC), "K02_modulo_corrigido", "G_KERNEL", "kernel embutido: o texto de %s SUBSTITUIDO pelo do sandbox (so' a docstring; codigo e declaracoes iguais)" % REL_KC)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean, do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb[REL_KC] = TXT_KC; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}
ROOT_SHA_V412 = sha256(old_d["TGLExt.lean"].encode("utf-8"))

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v413.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a da base"
assert all(m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX_POR_MODULO[m.replace(".", "/") + ".lean"]) for k, n, m in FL) and FJ["n_flags"] == len(FL) == DL.N_FLAGS, "as bandeiras tem de ser so' de declaracao nomeada de modulo do bundle, com o prefixo do contrato"
_RX_HIST_FLAG = re.compile(r"\d{8}|20\d\d|v4\d\d_|ordem|parecer|revisao|gerencia|operador|autor|codex|kimi|claude|chatgpt")
# a parte da chave antes de _413_ e' 'ext_' + o NOME DO MODULO em minusculas (o prefixo do contrato); o nome do modulo e' localizador tecnico, que o contrato da v413 (secao 0) manda conservar e nao conta como narrativa:
# um acerto da lista que e' EXATAMENTE o nome de um modulo do manifesto (ex.: o modulo Operador, o operador de consciencia) fica registrado, nao recusado; qualquer outro acerto recusa.
_MODS_MIN = {m.split(".")[-1].lower() for m in DL.BUNDLE_MODS}
_flags_hist, FLAGS_NOME_DE_MODULO_NA_LISTA = set(), set()
for k_, _n_, _m_ in FL:
    _pre = k_.rsplit("_413_", 1)[0]
    for _mh in _RX_HIST_FLAG.finditer(_pre):
        if _pre == "ext_" + _m_.split(".")[-1].lower() and _m_.split(".")[-1].lower() == _mh.group(0) and _mh.group(0) in _MODS_MIN:
            FLAGS_NOME_DE_MODULO_NA_LISTA.add(_pre)
        else:
            _flags_hist.add(_pre)
_flags_hist = sorted(_flags_hist); FLAGS_NOME_DE_MODULO_NA_LISTA = sorted(FLAGS_NOME_DE_MODULO_NA_LISTA)
assert not _flags_hist, ("nome de bandeira com data, nome de pessoa ou de modelo, ou palavra de processo (examinadas %d chaves)" % len(FL), _flags_hist)
assert all(re.fullmatch(r"ext_[a-z0-9_]+_413_\d{4}", k) and k.rsplit("_413_", 1)[0] == "ext_" + m.split(".")[-1].lower() for k, _, m in FL) and len(FL) > 0, "nome de bandeira fora do prefixo do contrato (ext_<modulo em minusculas>_413_NNNN)"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v413: os %d modulos de TGLExt/ do bundle (series ext_<modulo>_413_*): %d bandeiras, so' de declaracao NOMEADA (as auxiliares geradas pelo compilador ficam fora)" % (N_NOVOS, len(FL)) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E412 and len(set(old_lad)) == E412
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v413: os %d modulos do bundle (%d, so' declaracao nomeada)" % (N_NOVOS, len(FL)) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL); assert ESCADA_ESP == DL.ESCADA_NOVA == FJ["escada"][1]
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v413: os %d modulos do bundle" % N_NOVOS + CRLF + "".join('    ("v413", "%s", "%s", None, None),%s' % (_nome_mod(rel).replace("_", chr(92) * 2 + "_"), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v412"   # ([^\r\n]*)' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v413"   # v413: a CONSTANTE UNICA de versao -- %d modulos novos de TGLExt/ (a ponte de Cook-Levin, a fronteira dos tres literais, o operador de consciencia e a identidade preservada; %d bandeiras so\' de declaracao nomeada; '
           'a escada %d -> %d) e o texto de %s (so\' a docstring: diz o enunciado; codigo e declaracoes iguais), seis registros por especificacao (os cinco do contrato e a cobertura do relatorio de axiomas: %s), a guarda de frases herdada da v412 e a secao do artigo “%s”; o resumo nao muda; '
           'nenhuma chave antiga muda; o gate nao se move; ' % (N_NOVOS, len(FL), E412, ESCADA_ESP, KC["modulo"], ", ".join(DL.REGISTROS_SPEC_V413), DL.TITULO_SECAO_V413["pt"])) + m.group(1)
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v413'.")

# ---------------- (3) o que a v413 muda nos registros herdados (so' dados): a escada, o baseline do H0DN e o pino da raiz ----------------
RX_LAD = re.compile(r"'expected_ladder': %d(?![0-9])" % E412)
_achados = list(RX_LAD.finditer(T0))
N_LAD_BASE = len(_achados); assert N_LAD_BASE == 30, ("os 'expected_ladder' com a escada da base: esperados 30", N_LAD_BASE)
for k_, mm_ in enumerate(_achados):
    edit(mm_.start(), mm_.end(), "'expected_ladder': %d" % ESCADA_ESP, "C12_expected_ladder#%d" % (k_ + 1), "G_HERDADOS_ESCADA", "expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (E412, ESCADA_ESP))
_hc = top("_V411_H0DN_CONTRACT"); _hca, _hcb = span(_hc.value)
_mesc = list(re.finditer(r"'escada': %d(?![0-9])" % E412, T0[_hca:_hcb])); assert len(_mesc) == 1, ("o literal da escada no contrato do H0DN", len(_mesc))
edit(_hca + _mesc[0].start(), _hca + _mesc[0].end(), "'escada': %d" % ESCADA_ESP, "C12b_h0dn_baseline_escada", "G_HERDADOS_ESCADA", "_V411_H0DN_CONTRACT baseline.escada %d -> %d (o registro herdado compara a escada do rito com a do contrato)." % (E412, ESCADA_ESP))


def _spec_block(nome_var):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    assert pprint.pformat(specs_, width=160, sort_dicts=False) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


N_PINO_RAIZ = T0.count(ROOT_SHA_V412)
assert N_PINO_RAIZ == 1, ("o sha256 da raiz da v412 deve aparecer UMA vez na base (o u44 de cunhagens_v411)", N_PINO_RAIZ)
assert T0.count(KC["sha256_antes"]) == 0, "o sha256 antigo do modulo corrigido nao pode estar pinado na base"
spa, spb, specs411 = _spec_block("_V411_SPECS")
_u44 = 0
for s_ in specs411:
    if s_["nome"] == "cunhagens_v411":
        for c in s_["checks"]:
            if c["id"] == "u44":
                assert c["op"] == "igual" and c["caminho"] == ["formal_files_sha256", "TGLExt.lean"] and c["valor"] == ROOT_SHA_V412, "o u44 de cunhagens_v411 nao e' o pino da raiz da v412"
                c["valor"] = FORMAL_MAP["TGLExt.lean"]; _u44 += 1
assert _u44 == 1
edit(spa, spb, pprint.pformat(specs411, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v411_pino_da_raiz", "G_HERDADOS_PISOS", "_V411_SPECS: cunhagens_v411 u44 -> o pino da raiz desta versao; os vereditos nao mudam.")

# ---------------- (4) o runtime novo: a secao e os seis registros ----------------
TP = json.load(open(DL.TEXTO_PUBLICO_ARQ, encoding="utf-8"))
assert TP["fonte_pt"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_ARQ) and TP["fonte_en"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_EN_ARQ), "TEXTO_PUBLICO_v413.json nao e' da pagina/traducao atuais: rode e7_23"
SECAO = {"pt": list(TP["tex"]["pt"]), "en": list(TP["tex"]["en"])}
specs = RG.especs()
spec_nomes = [s["nome"] for s in specs]; assert spec_nomes == DL.REGISTROS_SPEC_V413
CODE_SRC = open(os.path.join(HERE, "runtime_v413_codigo.py"), encoding="utf-8").read()
CODE_SRC = CODE_SRC[CODE_SRC.index("def _v413_secao_tex"):]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GF.p18(corpo); assert not v, (s["nome"], v[:3])
    _tv = GF.travessia("registro:" + s["nome"], {"corpo": {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]})
    assert _tv["ok"] and _tv["n_unidades"] > 0, (s["nome"], _tv["violacoes"][:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]) and not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V413), s["nome"]
    assert s["veredito_prefixo"] + "__" + s["veredito_sufixo"] == DL.PALAVRAS_DE_VEREDITO[s["nome"]], "a palavra de veredito difere da do contrato"
    assert set(s["kernel_flags"]) <= {k for k, _, _ in FL} and set(s["kernel_decls"]) <= {n for _, n, _ in FL}, (s["nome"], "ancora que nao e' bandeira nova")
for lg in ("pt", "en"):
    txt_sec = "\n\n".join(SECAO[lg])
    _ta = GF.travessia("artigo:" + lg, SECAO[lg], "tex"); assert _ta["ok"] and _ta["n_unidades"] > 0, ("a travessia da guarda herdada recusa a secao do artigo", lg, _ta["violacoes"][:3])
    assert not GF.p18(txt_sec), (lg, GF.p18(txt_sec)[:3])
    assert not VH.examinar([("secao_" + lg, l) for l in SECAO[lg]])["achados"], ("historia na secao do artigo", lg)
_khb = open(DL.KH_N1_V413_ARQ, "rb").read()
FONTES13 = {"kh_n1_v413": {"arquivo": DL.KH_N1_V413_ARQ, "bytes": len(_khb), "papel": "a medida do Audit do sandbox desta versao (o recibo KH_N1), lida pelo registro kh_n1_cobertura_v413 por sha256 [REAL: sha256]", "sha256": sha256(_khb)}}
RCODE = ("_V413_SECAO = " + pprint.pformat(SECAO, width=160, sort_dicts=False) + "\n_V413_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n_V413_NOMES_REGISTROS = " + repr(spec_nomes)
         + "\n_V413_FONTES = " + pprint.pformat(FONTES13, width=160, sort_dicts=False) + "\n_V413_VERBATINS2 = {}   # vazio: a v413 nao embute fala"
         + "\n_V392_FONTES.update(_V413_FONTES)   # v413: o motor de registros (v392) le as fontes e os verbatins tambem da v413\n_V392_VERBATINS2.update(_V413_VERBATINS2)\n\n\n")
HDR = ("# ====================== v413 -- a ponte de Cook-Levin, a fronteira dos tres literais, o operador de consciencia e a identidade preservada: %d modulos novos de TGLExt/ e o texto de %s (so' a docstring), %d bandeiras, "
       "a escada %d -> %d, a secao “%s” do artigo e seis registros por especificacao (os cinco do contrato e a cobertura do relatorio de axiomas: %s).\n# Os registros usam o motor da v392 (_v392_registro) e a guarda de frases herdada da v412 (_v412_travessia); nenhum tem funcao nova; "
       "nenhuma chave antiga muda; o resumo do artigo nao muda; validade no kernel nao e' creditacao; o gate nao se move.\n"
       % (N_NOVOS, KC["modulo"], len(FL), E412, ESCADA_ESP, DL.TITULO_SECAO_V413["pt"], ", ".join(spec_nomes)))
RT_ = HDR + CODE_SRC.rstrip("\n") + "\n\n\n# ---- v413: o texto da secao do artigo (montado da pagina publica) e os registros por especificacao\n" + RCODE
RT_ = RT_.rstrip("\n") + "\n"
ast.parse(RT_)
assert "\r" not in RT_ and not GUARDA.search(RT_) and not AC.literais_de_beta(RT_), "caractere, veredito proibido ou beta literal no runtime"
_h = VH.examinar([("runtime_v413/L%d" % (i + 1), l) for i, l in enumerate(re.sub(r"_V413_SECAO = .*?\n_V413_SPECS", "_V413_SPECS", RT_, flags=re.S).split("\n")) if l.strip() and not l.startswith(("  ", "    '", '    "', " '", ' "'))])
assert not _h["achados"], ("historia de conversa no codigo novo", _h["achados"][:3])
_controles(RT_, "runtime_v413"); _controles(specs, "specs_v413")
A_P = linha_unica(r"^# ====================== v412 -- a camada cientifica, o leitor da formula e a matematica que restava")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v413", "G_RUNTIME", "bloco v413: a secao do artigo e os seis registros por especificacao (a guarda e' a herdada da v412).")

# ---------------- (5) main: a rodada dos registros e o resumo no selo ----------------
A_R = linha_unica(r'^        print\("   \[v412\] AVISO: os registros por spec da v412 nao rodaram')
BLOCO_N00 = '''    try:   # v413: os seis registros por especificacao (a ponte de Cook-Levin, a fronteira dos tres literais, o operador de consciencia, a identidade preservada, a cobertura do relatorio de axiomas e as definicoes da teoria); excecao vira AVISO visivel, nunca derruba o rito
        _n413 = _v413_rodar_specs(core)
        print("   [v413] registros por spec: %s | selados %d de %d" % (" | ".join("%s=%s" % (k_, "SELOU" if (core.get(k_) or {}).get("all_verified") is True else "NAO") for k_ in _n413), sum(1 for k_ in _n413 if (core.get(k_) or {}).get("all_verified") is True), len(_n413)))
        for _k413 in _n413:
            print("  >>> %s <<<" % (core.get(_k413) or {}).get("verdict"))
    except Exception as _e413:
        print("   [v413] AVISO: os registros por spec da v413 nao rodaram: %r" % (_e413,))
'''
ast.parse("def _f(core):\n" + BLOCO_N00)
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_registros_v413", "G_RUNTIME", "main: UMA instrucao try/AVISO: os registros por spec da v413, LOGO DEPOIS do bloco da v412 e antes de emit_figures.")
assert "emit_figures(core" in T0[A_R.end():], "o bloco da v413 tem de ficar ANTES da chamada de emit_figures no main"
A_S = linha_unica(r'^ {12}"registros_v412": \{n_: ')
edit(A_S.end(), A_S.end(), '            "registros_v413": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V413_NOMES_REGISTROS},' + CRLF, "N02_selo", "G_SELO", "selo: registros_v413 (veredito e selo de cada um).")

# ---------------- (6) o artigo: a secao nova antes da secao da v412 (o resumo NAO muda) ----------------
for _lg, _tit412 in (("pt", "O que fica claro na v412"), ("en", "What becomes clear in v412")):
    _m = re.search(r'^    # v412 -- a secao “%s” \(PT/EN\): [^\r\n]*\r\n    for _l412s in _v412_secao_tex\("%s"\):\r\n        s\.append\(_l412s\)\r\n' % (re.escape(_tit412), _lg), T0, re.M)
    assert _m and T0.count(_m.group(0)) == 1, ("a ancora da secao da v412 no artigo nao e' unica", _lg)
    _tit413 = DL.TITULO_SECAO_V413[_lg]
    _bl = ('    # v413 -- a secao “%s” (PT/EN): texto da teoria montado da pagina publica; as pedras citadas estao no kernel desta versao. Nada aqui move o gate.\n'
           '    for _l413s in _v413_secao_tex("%s"):\n        s.append(_l413s)\n' % (_tit413, _lg))
    ast.parse("def _f(core, s):\n" + _bl); assert not GUARDA.search(_bl)
    edit(_m.start(), _m.start(), crlf(_bl), "W04_artigo_" + _lg.upper(), "G_ARTIGO", "artigo %s: a secao nova antes da secao da v412." % _lg.upper())
_controles(TP, "texto_publico")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))


def montar(k_espacos):
    T_ = T0
    for a_, b_, novo_, pid_, *_r in sorted(EDITS, key=lambda e: -e[0]):
        if pid_ == "W01_versao":
            novo_ = novo_[:-len(CRLF)] + " " * k_espacos + CRLF
        T_ = T_[:a_] + novo_ + T_[b_:]
    return T_


def n10_aplica(T_):
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF)"
NOVOS_NOMES = ("_v413_secao_tex", "_v413_rodar_specs", "_V413_SECAO", "_V413_SPECS", "_V413_NOMES_REGISTROS", "_V413_FONTES", "_V413_VERBATINS2")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RT_)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb, "o kernel embutido nao e' o esperado"
assert list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL] and len(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value)) == len(old_flags) + len(FL)
assert {k: v for k, v in ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value).items() if k in old_flags} == old_flags, "uma chave antiga mudou de literal"
INTOCADAS_V413 = list(DL.D10.FUNCOES_INTOCADAS) + ["h0dn_bg1_v411", "veredito_h0dn", "_v411_guarda_frases", "_v411_rodar_specs", "_v411_p18_sem_cabeca", "_V411_H0DN_CONTRACT", "_V411_H0DN_TEXT", "_V411_H0DN_INSUMOS", "_V411_FONTES",
                                                   "_V411_FALAS_CITADAS", "_V411_NOMES_REGISTROS", "_v410_guarda_frases", "_v410_rodar_specs", "_V410_SPECS", "_V409_SPECS", "_v397_quadro_tex", "_v397_quadro_md", "run_um", "verify_tgl_kernel_formalization",
                                                   "prove_qg_closure_gate", "_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia", "_v412_secao_tex", "_v412_rodar_specs", "_v412_topo_texto", "_v411_topo_texto",
                                                   "_V412_SECAO", "_V412_SPECS", "_V412_NOMES_REGISTROS", "_V412_TOPO", "_V411_TOPO", "_v392_registro", "_v392_guarda_texto"]
INTOCADAS_V413 = list(dict.fromkeys(f for f in INTOCADAS_V413 if f not in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder", "_V411_SPECS")))
for fname in INTOCADAS_V413:   # (so' os literais 'expected_ladder' e a escada do contrato do H0DN podem subir, dado)
    assert ast.get_source_segment(T, top(fname, tree)).replace("'expected_ladder': %d" % ESCADA_ESP, "'expected_ladder': %d" % E412).replace("'escada': %d" % ESCADA_ESP, "'escada': %d" % E412) == ast.get_source_segment(T0, top(fname)), \
        "a funcao/constante %s NAO pode mudar na v413" % fname
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v413" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
man = {"candidato": DL.CANDIDATO_ARQ, "modo": DL.MODO, "pagina": {"arquivo": os.path.relpath(DL.PAGINA_ARQ, HERE), "sha16": DL.sha16_arquivo(DL.PAGINA_ARQ), "e_a_pagina_do_contrato": os.path.normcase(DL.PAGINA_ARQ) == os.path.normcase(str(L.PAGINA_CONTRATO))},
       "contrato": {"arquivo": os.path.basename(DL.CONTRATO_ARQ), "sha16": DL.CONTRATO_SHA16}, "gerador": os.path.basename(__file__), "gerador_sha16": DL.sha16_arquivo(__file__),
       "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v412_sha16": SHA0, "base_v412_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E412, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "modulo_corrigido": {"rel": REL_KC, "sha256_antes": KC["sha256_antes"], "sha256_depois": KC["sha256_depois"], "substituido_no_dicionario_embutido": True},
                  "bundle_sha16": DL.sha16_arquivo(DL.BUNDLE_ARQ), "sandbox": KB, "flags_sha16": DL.sha16_arquivo(os.path.join(KD, "FLAGS_v413.json")),
                  "pos_build": {k_: json.load(open(os.path.join(KD, "POS_BUILD_v413.json"), encoding="utf-8")).get(k_) for k_ in ("ok", "linha_TOTAL", "delta_vs_v412", "escada")}},
       "bandeiras_cujo_prefixo_e_um_nome_de_modulo_que_esta_na_lista_de_palavras": FLAGS_NOME_DE_MODULO_NA_LISTA,
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "formal_files_n": len(FORMAL_MAP), "expected_ladder_literais": N_LAD_BASE, "pino_da_raiz_u44": {"antes": ROOT_SHA_V412, "depois": FORMAL_MAP["TGLExt.lean"]},
       "gate_nao_se_move": {"funcoes_identicas_a_base_salvo_literais_de_escada": list(INTOCADAS_V413), "gate_verdict_v412": selo0.get("qg_closure_verdict"),   # (revisao B5) o rotulo diz a ressalva
                            "literais_de_dado_que_mudam": [{"patch": e[3], "nome_de_topo": _nome_de_topo_em(e[0]), "o_que_muda": e[5]} for e in EDITS if e[3].startswith(("C12", "C13"))]},
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v412": g0, "candidato_v413": g1, "alfa_lido": a1_.group(1), "versao_lida": v1_.group(1)},
       "resumo_do_artigo": "nao muda", "runtime": {"sha256": sha256(RT_.encode("utf-8")), "bytes": len(RT_.encode("utf-8"))}, "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "guarda_frases": {"funcao": "_v412_guarda_frases (herdada da v412, ja' no programa; chamada pela _v412_travessia)", "violacoes_nos_textos_novos": 0},
       "quando": datetime.datetime.now().isoformat(timespec="seconds")}
if SECO:
    print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v412_sha16", "escada", "n_bandeiras", "registros", "n_patches", "modo")}, ensure_ascii=False, indent=1)); print("--seco: NADA gravado; patches:", [e[3] for e in EDITS if not e[3].startswith("C12_")], "+ %d C12" % N_LAD_BASE)
    sys.exit(0)
out = DL.CANDIDATO_ARQ
os.makedirs(os.path.dirname(out), exist_ok=True)
if os.path.exists(out) and open(out, "rb").read() != b:   # o candidato anterior e os artefatos dele vao para FORA de work\\, conferidos por bytes
    _velho = open(out, "rb").read(); _dg = os.path.join(DL.SANDBOX_PAI, "candidatos_anteriores", "um_v413_candidato_" + sha16(_velho)); os.makedirs(_dg, exist_ok=True)
    for _p in (out, DL.MANIFESTO_ARQ, DL.FORMAL_MAP_ARQ, DL.PINS_ARQ):
        if os.path.exists(_p):
            _d = os.path.join(_dg, os.path.basename(_p))
            if not (os.path.exists(_d) and open(_d, "rb").read() == open(_p, "rb").read()):
                shutil.copyfile(_p, _d + ".tmp"); os.replace(_d + ".tmp", _d)
            assert open(_d, "rb").read() == open(_p, "rb").read(), ("a guarda do candidato anterior nao e' copia de bytes", _d)
    print("candidato anterior guardado:", _dg)
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
assert sha256(open(out, "rb").read()) == man["sha256"]
L.salvar_json(DL.MANIFESTO_ARQ, man)
L.salvar_json(DL.FORMAL_MAP_ARQ, FORMAL_MAP)
L.salvar_bytes(DL.PINS_ARQ, RT_.encode("utf-8"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v412_sha16", "escada", "n_bandeiras", "registros", "modo")}, ensure_ascii=False, indent=1))
print("candidato:", out)
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS if not e[3].startswith("C12_")], "+ %d C12" % N_LAD_BASE)

# -*- coding: utf-8 -*-
"""gerar_candidato_v412.py -- gera o um.py CANDIDATO da v412 a partir da v411 SELADA (base_v411; o Nos e' so' conferido, NUNCA escrito). Molde: gerar_candidato_v411.py (patches por ast) e gerar_candidato_v410.py (o bundle de modulos).
Conteudo (CONTRATO_v412_R4; nenhum texto daqui entra no programa com historia de conversa):
 (A) kernel: 42 modulos novos em TGLExt/ embutidos em _EMBEDDED_KERNEL_FILES, do sandbox C:\\t\\k412c\\final (compilado e medido); a raiz TGLExt.lean regenerada com os 40 imports; as bandeiras ext_<modulo>_412_NNNN
     (so' declaracao nomeada) em _LEAN_THEOREM_FLAGS e na escada (12308 -> 13211); o ledger de pedras;
 (B) UM_VERSION = v412; os literais 'expected_ladder' da escada da base sobem para a escada desta versao; os pisos dos registros da v411 que cobravam igualdade exata do kernel (a igualdade exata passa a ser a do rito);
 (C) runtime novo: a guarda de frases da v412 (_v412_guarda_frases), a secao “O que fica claro na v412” (PT/EN), os quatro registros por especificacao (_V412_SPECS) e a rodada deles no main, depois dos da v411; resumo no selo;
 (D) artigo: a secao nova antes da secao da v411; no resumo, o paragrafo vigente de P = nP no lugar da frase anterior.
 O gate NAO muda: as funcoes do gate/neutrino e os registros anteriores ficam BYTE A BYTE (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -B -X utf8 gerar_candidato_v412.py [--seco]   (--seco: roda tudo e NAO grava o candidato; recusa -O; nunca escreve no Nos)"""
import ast, datetime, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SECO = "--seco" in sys.argv
import delta_v412 as DL  # noqa: E402
import registros_v412 as RG  # noqa: E402
import guarda_frases_v412 as GF  # noqa: E402
import acom_conferencias_v412 as AC  # noqa: E402
import verificar_historia_texto_v412 as VH  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
_selo_nos = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
if _selo_nos.get("um_version") != DL.BASE_VERSION or sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != DL.BASE_SHA16_DA_ORDEM:   # o Nos ja nao e' a v411 (rito da v412 em curso): a v411 SELADA vem da copia base_v411
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico lido nao e' a v411 selada"
SHA0 = sha16(raw); assert SHA0 == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E411 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E411 == DL.ESCADA_BASE
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


def replace_unique(old, new, pid, grupo, o_que, n=1):
    c = T0.count(old)
    assert c == n, ("ANCORA NAO UNICA (a regra dos patches: exatamente %d vez(es) na base; esta ocorre %d)" % (n, c), pid, old[:100])
    i = -1
    for k_ in range(n):
        i = T0.index(old, i + 1); edit(i, i + len(old), new, pid if n == 1 else "%s#%d" % (pid, k_ + 1), grupo, o_que)


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


# ---------------- (1) o kernel: os 40 modulos do bundle ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v412.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS and len(nov) == 42
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX, "a raiz do sandbox nao e' a da v411 + os imports do bundle"
assert new_audit == old_d["TGL/Audit.lean"], "o Audit do sandbox difere do embutido na v411 (a v412 nao o muda)"
_dif_sb = [rel for rel, txt in old_d.items() if rel != "TGLExt.lean" and (not os.path.exists(os.path.join(KB, *rel.split("/"))) or rd(os.path.join(KB, *rel.split("/"))) != txt)]
assert not _dif_sb, ("o kernel EMBUTIDO da base difere do sandbox k412c fora da raiz", _dif_sb[:5])
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
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean, do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v412.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a da base"
assert all(DL.D10.classe(n) == "nomeada" if hasattr(DL.D10, "classe") else True for k, n, m in FL)
assert all(m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX_POR_MODULO[m.replace(".", "/") + ".lean"]) for k, n, m in FL) and FJ["n_flags"] == len(FL) == DL.N_FLAGS, "as bandeiras tem de ser so' de declaracao nomeada de modulo do bundle, com o prefixo do contrato"
assert not any(re.search(r"\d{8}|20\d\d|v4\d\d_|ordem|parecer|gerencia|operador|autor", k.replace("_412_", "_")) for k, _, _ in FL if not re.fullmatch(r"ext_[a-z0-9]+_412_\d{4}", k)), "nome de bandeira com historia"
assert all(re.fullmatch(r"ext_[a-z0-9]+_412_\d{4}", k) for k, _, _ in FL), "nome de bandeira fora do prefixo do contrato"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v412: os 40 modulos de TGLExt/ do bundle (series ext_<modulo>_412_*): %d bandeiras, so' de declaracao NOMEADA (as auxiliares geradas pelo compilador ficam fora)" % len(FL) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E411 and len(set(old_lad)) == E411
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v412: os 40 modulos do bundle (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL); assert ESCADA_ESP == DL.ESCADA_NOVA == FJ["escada"][1]
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v412: os %d modulos do bundle" % N_NOVOS + CRLF + "".join('    ("v412", "%s", "%s", None, None),%s' % (_nome_mod(rel), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v411"   # ([^\r\n]*)' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v412"   # v412: a CONSTANTE UNICA de versao -- %d modulos novos de TGLExt/ (a camada cientifica e a matematica que restava; %d bandeiras so\' de declaracao nomeada; a escada %d -> %d), '
           'quatro registros por especificacao (%s), a guarda de frases da v412, o paragrafo vigente de P = nP no resumo e a secao do artigo “%s”; nenhuma chave antiga muda; o gate nao se move; '
           % (N_NOVOS, len(FL), E411, ESCADA_ESP, ", ".join(DL.REGISTROS_SPEC_V412), DL.TITULO_SECAO_V412["pt"])) + m.group(1)
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v412'.")

# ---------------- (3) o que a v412 muda nos registros da v411 (so' dados): a escada e os pisos ----------------
RX_LAD = re.compile(r"'expected_ladder': %d(?![0-9])" % E411)
_achados = list(RX_LAD.finditer(T0))
N_LAD_BASE = len(_achados); assert N_LAD_BASE == 30, ("os 'expected_ladder' com a escada da base: esperados 30", N_LAD_BASE)
for k_, mm_ in enumerate(_achados):
    edit(mm_.start(), mm_.end(), "'expected_ladder': %d" % ESCADA_ESP, "C12_expected_ladder#%d" % (k_ + 1), "G_V411_ESCADA", "expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (E411, ESCADA_ESP))


_hc = top("_V411_H0DN_CONTRACT"); _hca, _hcb = span(_hc.value)
_mesc = list(re.finditer(r"'escada': %d(?![0-9])" % E411, T0[_hca:_hcb])); assert len(_mesc) == 1, ("o literal da escada no contrato do H0DN", len(_mesc))
edit(_hca + _mesc[0].start(), _hca + _mesc[0].end(), "'escada': %d" % ESCADA_ESP, "C12b_h0dn_baseline_escada", "G_V411_ESCADA", "_V411_H0DN_CONTRACT baseline.escada %d -> %d (o registro herdado compara a escada do rito com a do contrato)." % (E411, ESCADA_ESP))


def _spec_block(nome_var):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    assert pprint.pformat(specs_, width=160, sort_dicts=False) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


spa, spb, specs411 = _spec_block("_V411_SPECS")
PISO_TXT = " -- piso: o valor da versao anterior; a igualdade exata do kernel desta versao e' lida pelo rito nos registros da v412"
for s_ in specs411:
    if s_["nome"] == "kh_n1_cobertura_v411":
        for c in s_["checks"]:
            if c["id"] in ("h2", "h3"):
                assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += PISO_TXT
            elif c["id"] == "h6":
                assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += PISO_TXT
            elif c["id"] == "h8":
                assert c["op"] == "igual" and isinstance(c["valor"], dict); n_h8 = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = n_h8; c["descricao"] += PISO_TXT + " (tamanho minimo da arvore: %d entradas)" % n_h8
    if s_["nome"] == "cunhagens_v411":
        for c in s_["checks"]:
            if c["id"] == "u6":
                assert c["op"] == "igual" and c["valor"] == E411; c["op"] = "maior_igual"; c["descricao"] += PISO_TXT
            elif c["id"] == "u44":
                assert c["op"] == "igual" and c["caminho"] == ["formal_files_sha256", "TGLExt.lean"]; c["valor"] = FORMAL_MAP["TGLExt.lean"]; c["descricao"] += " -- a raiz importa os modulos novos: o pino e' o da raiz desta versao"
edit(spa, spb, pprint.pformat(specs411, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v411_pisos", "G_V411_PISOS", "_V411_SPECS: kh_n1_cobertura_v411 h2/h3/h6/h8 -> pisos; cunhagens_v411 u6 -> piso e u44 -> pino da raiz desta versao; os vereditos nao mudam.")

# ---------------- (4) o runtime novo: a guarda, a secao, os quatro registros ----------------
TP = json.load(open(DL.TEXTO_PUBLICO_ARQ, encoding="utf-8"))
assert TP["fonte_pt"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_ARQ) and TP["fonte_en"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_EN_ARQ), "TEXTO_PUBLICO_v412.json nao e' da pagina/traducao atuais: rode e2_21"
SECAO = {"pt": list(TP["tex"]["pt"]), "en": list(TP["tex"]["en"])}
specs = RG.especs()
tnode = top("_V411_TOPO"); ta, tb = span(tnode.value); topo = ast.literal_eval(tnode.value)
ANTIGA = {"pt": "P = nP: o kernel Lean prova, como validade e não creditação, P = nP relativo ao leitor (a máquina com o leitor; a máquina de Turing padrão sem o leitor fica fora); a pergunta do Clay, tal qual apresentada pela TGL, está resolvida no kernel, e creditar essa prova compete só a quem tem autoridade para falar em nome do Clay.",
          "en": "P = nP: the Lean kernel proves, as validity and not creditation, P = nP relative to the reader (the machine with the reader; the standard Turing machine without the reader stays outside); the Clay question, as presented by the TGL, is resolved in the kernel, and crediting this proof belongs only to those with authority to speak for Clay."}
TOPO12 = {k_: v_ for k_, v_ in topo.items() if k_ not in ("pt", "en", "ratificado", "sha256_do_arquivo")}
TROCA_RESUMO = {}
for _lg in ("pt", "en"):
    assert topo[_lg].count(ANTIGA[_lg]) == 1 and topo[_lg].endswith(ANTIGA[_lg]), ("a frase de P = nP do resumo da base nao e' a esperada", _lg)
    TOPO12[_lg] = topo[_lg].replace(ANTIGA[_lg], TP["pnp_resumo"][_lg])
    TROCA_RESUMO[_lg] = {"antiga": ANTIGA[_lg], "nova": TP["pnp_resumo"][_lg]}
TOPO12["pnp"] = {"pt": TP["pnp_resumo"]["pt"], "en": TP["pnp_resumo"]["en"]}
TOPO12 = {k_: TOPO12[k_] for k_ in ("pt", "en", "pnp", "marcadores", "livro") if k_ in TOPO12}
spec_nomes = [s["nome"] for s in specs]; assert spec_nomes == DL.REGISTROS_SPEC_V412
GUARD_SRC = open(os.path.join(HERE, "runtime_v412_guarda.py"), encoding="utf-8").read(); CODE_SRC = open(os.path.join(HERE, "runtime_v412_codigo.py"), encoding="utf-8").read()
GUARD_SRC = GUARD_SRC[GUARD_SRC.index("def _v412_guarda_frases"):]; CODE_SRC = CODE_SRC[CODE_SRC.index("def _v412_secao_tex"):]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GF.p18(corpo); assert not v, (s["nome"], v[:3])
    _tv = GF.travessia("registro:" + s["nome"], {"corpo": {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]})
    assert _tv["ok"] and _tv["n_unidades"] > 0, (s["nome"], _tv["violacoes"][:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]) and not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V412), s["nome"]
    assert s["veredito_prefixo"] + "__" + s["veredito_sufixo"] == DL.PALAVRAS_DE_VEREDITO[s["nome"]], "a palavra de veredito difere da do contrato"
    assert all(a_ in core0["kernel_formalization"] or a_ in set(k for k, _, _ in FL) for a_ in s["kernel_flags"]), (s["nome"], "bandeira de ancora fora das novas")
    assert set(s["kernel_flags"]) <= {k for k, _, _ in FL} and set(s["kernel_decls"]) <= {n for _, n, _ in FL}, (s["nome"], "ancora que nao e' bandeira nova")
for lg in ("pt", "en"):
    txt_sec = "\n\n".join(SECAO[lg])
    _ta = GF.travessia("artigo_" + lg, SECAO[lg], "tex"); assert _ta["ok"] and _ta["n_unidades"] > 0, (lg, _ta["violacoes"][:3])
    assert not GF.p18(txt_sec), (lg, GF.p18(txt_sec)[:3])
    assert not VH.examinar([("secao_" + lg, l) for l in SECAO[lg]])["achados"], ("historia na secao do artigo", lg)
import topo_v412 as TOPOMOD
TOPO_FUNC = TOPOMOD.construir(top("_v411_topo_texto"))
RCODE = ("_V412_SECAO = " + pprint.pformat(SECAO, width=160, sort_dicts=False) + "\n_V412_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n_V412_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V412_TOPO = " + pprint.pformat(TOPO12, width=160, sort_dicts=False) + "\n\n\n")
HDR = ("# ====================== v412 -- a camada cientifica e a matematica que restava: %d modulos novos de TGLExt/ (%d bandeiras, a escada %d -> %d), a guarda de frases da v412, a secao “%s” do artigo e quatro registros por especificacao "
       "(%s).\n# Os registros usam o motor da v392 (_v392_registro); nenhum tem funcao nova; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move.\n"
       % (N_NOVOS, len(FL), E411, ESCADA_ESP, DL.TITULO_SECAO_V412["pt"], ", ".join(spec_nomes)))
RT_ = HDR + GUARD_SRC.rstrip("\n") + "\n\n\n" + CODE_SRC.rstrip("\n") + "\n\n\n" + TOPO_FUNC.rstrip("\n") + "\n\n\n# ---- v412: o texto da secao do artigo (montado da pagina publica) e os registros por especificacao\n" + RCODE
RT_ = RT_.rstrip("\n") + "\n"
ast.parse(RT_)
assert "\r" not in RT_ and not GUARDA.search(RT_) and not AC.literais_de_beta(RT_), "caractere, veredito proibido ou beta literal no runtime"
_h = VH.examinar([("runtime_v412/L%d" % (i + 1), l) for i, l in enumerate(re.sub(r"_V412_SECAO = .*?\n_V412_SPECS", "_V412_SPECS", RT_, flags=re.S).split("\n")) if l.strip() and not l.startswith(("  ", "    '", '    "', " '", ' "'))])
assert not _h["achados"], ("historia de conversa no codigo novo", _h["achados"][:3])
_controles(RT_, "runtime_v412"); _controles(specs, "specs_v412")
A_P = linha_unica(r"^# ====================== v411 \(12/11/2026\) -- O TESTE DECISIVO")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v412", "G_RUNTIME", "bloco v412: a guarda de frases, a secao do artigo, os quatro registros por especificacao.")

# ---------------- (5) main: a rodada dos registros e o resumo no selo ----------------
A_R = linha_unica(r'^        print\("   \[v411\] AVISO: o registro do H0DN v411 ou os registros por spec da v411 nao rodaram')
BLOCO_N00 = '''    try:   # v412: os quatro registros por especificacao (a camada cientifica, a matematica que restava, a parede do teste cego e as definicoes da teoria); excecao vira AVISO visivel, nunca derruba o rito
        _n412 = _v412_rodar_specs(core)
        print("   [v412] registros por spec: %s | selados %d de %d" % (" | ".join("%s=%s" % (k_, "SELOU" if (core.get(k_) or {}).get("all_verified") is True else "NAO") for k_ in _n412), sum(1 for k_ in _n412 if (core.get(k_) or {}).get("all_verified") is True), len(_n412)))
        for _k412 in _n412:
            print("  >>> %s <<<" % (core.get(_k412) or {}).get("verdict"))
    except Exception as _e412:
        print("   [v412] AVISO: os registros por spec da v412 nao rodaram: %r" % (_e412,))
'''
ast.parse("def _f(core):\n" + BLOCO_N00)
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_registros_v412", "G_RUNTIME", "main: UMA instrucao try/AVISO: os registros por spec da v412, LOGO DEPOIS do bloco da v411 e antes de emit_figures.")
assert "emit_figures(core" in T0[A_R.end():], "o bloco da v412 tem de ficar ANTES da chamada de emit_figures no main"
A_S = linha_unica(r'^ {12}"registros_v411": \{n_: ')
edit(A_S.end(), A_S.end(), '            "registros_v412": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V412_NOMES_REGISTROS},' + CRLF, "N02_selo", "G_SELO", "selo: registros_v412 (veredito e selo de cada um).")

# ---------------- (6) o artigo: a secao nova antes da secao da v411; o paragrafo vigente de P = nP no resumo ----------------
for _lg, _tit in (("pt", "O TESTE DECISIVO"), ("en", "THE DECISIVE TEST")):
    _m = re.search(r'^    # v411 \(12/11/2026\) -- %s: [^\r\n]*\r\n    for _l411s in _v411_secao_tex\(core, "%s", _V411_TITULO_SECAO\["%s"\]\):\r\n        s\.append\(_l411s\)\r\n' % (_tit, _lg, _lg), T0, re.M)
    assert _m and T0.count(_m.group(0)) == 1, ("a ancora da secao da v411 no artigo nao e' unica", _lg)
    _bl = ('    # v412 -- a secao “%s” (PT/EN): texto da teoria montado da pagina publica; as pedras citadas estao no kernel desta versao. Nada aqui move o gate.\n'
           '    for _l412s in _v412_secao_tex("%s"):\n        s.append(_l412s)\n' % (DL.TITULO_SECAO_V412[_lg], _lg))
    ast.parse("def _f(core, s):\n" + _bl); assert not GUARDA.search(_bl) and not GF.violacoes(_bl)
    edit(_m.start(), _m.start(), crlf(_bl), "W04_artigo_" + _lg.upper(), "G_ARTIGO", "artigo %s: a secao nova antes da secao da v411." % _lg.upper())
for _lg, _nome in (("pt", "pt"), ("en", "en")):   # a emissao do resumo e' versionada: a v412 chama a sua funcao; a da v411 fica como esta
    _a = '{\\large\\itshape " + _v411_topo_texto(core, "%s") + r""' % _lg
    _c = T0.count(_a); assert _c == 1, ("a chamada do topo na base nao e' unica", _lg, _c)
    _i = T0.index(_a); edit(_i, _i + len(_a), _a.replace("_v411_topo_texto", "_v412_topo_texto"), "W06_topo_" + _lg, "G_ARTIGO", "artigo %s: o resumo chama a emissao versionada do topo (_v412_topo_texto)." % _lg.upper())
    _tp = GF.travessia("resumo_" + _lg, {_lg: [TP["pnp_resumo"][_lg]]}); assert _tp["ok"] and _tp["n_unidades"] > 0, ("o paragrafo do resumo reprova na travessia", _lg, _tp["violacoes"][:3])
    assert not VH.examinar([("resumo_" + _lg, TP["pnp_resumo"][_lg])])["achados"], "historia no paragrafo do resumo"
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
NOVOS_NOMES = ("_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia", "_v412_secao_tex", "_v412_rodar_specs", "_v412_topo_texto", "_V412_SECAO", "_V412_SPECS", "_V412_NOMES_REGISTROS", "_V412_TOPO")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RT_)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb, "o kernel embutido nao e' o esperado"
assert list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL] and len(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value)) == len(old_flags) + len(FL)
assert {k: v for k, v in ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value).items() if k in old_flags} == old_flags, "uma chave antiga mudou de literal"
INTOCADAS_V412 = list(DL.D10.FUNCOES_INTOCADAS) + ["h0dn_bg1_v411", "veredito_h0dn", "_v411_guarda_frases", "_v411_rodar_specs", "_v411_p18_sem_cabeca", "_V411_H0DN_CONTRACT", "_V411_H0DN_TEXT", "_V411_H0DN_INSUMOS", "_V411_FONTES",
                                                   "_V411_FALAS_CITADAS", "_V411_NOMES_REGISTROS", "_v410_guarda_frases", "_v410_rodar_specs", "_V410_SPECS", "_V409_SPECS", "_v397_quadro_tex", "_v397_quadro_md", "run_um", "verify_tgl_kernel_formalization", "prove_qg_closure_gate"]
INTOCADAS_V412 = [f for f in INTOCADAS_V412 if f not in ("_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder")]
for fname in INTOCADAS_V412:   # (so' o literal 'expected_ladder' pode subir, dado)
    assert ast.get_source_segment(T, top(fname, tree)).replace("'expected_ladder': %d" % ESCADA_ESP, "'expected_ladder': %d" % E411).replace("'escada': %d" % ESCADA_ESP, "'escada': %d" % E411) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v412" % fname
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v412" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
man = {("artefato_de_ensaio" if False else "candidato"): DL.CANDIDATO_ARQ, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v411_sha16": SHA0, "base_v411_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E411, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "bundle_sha16": DL.sha16_arquivo(DL.BUNDLE_ARQ), "sandbox": KB, "flags_sha16": DL.sha16_arquivo(os.path.join(KD, "FLAGS_v412.json")), "pos_build": {k_: json.load(open(os.path.join(KD, "POS_BUILD_v412.json"), encoding="utf-8")).get(k_) for k_ in ("ok", "linha_TOTAL", "delta_vs_v411", "escada")}},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "formal_files_n": len(FORMAL_MAP), "expected_ladder_literais": N_LAD_BASE,
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(INTOCADAS_V412), "gate_verdict_v411": selo0.get("qg_closure_verdict")}, "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v411": g0, "candidato_v412": g1, "alfa_lido": a1_.group(1), "versao_lida": v1_.group(1)},
       "resumo_troca_de_pnp": TROCA_RESUMO, "runtime": {"sha256": sha256(RT_.encode("utf-8")), "bytes": len(RT_.encode("utf-8"))}, "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "guarda_frases": {"funcao": "_v412_guarda_frases", "fonte_sha16": DL.sha16_arquivo(os.path.join(HERE, "runtime_v412_guarda.py")), "violacoes_nos_textos_novos": 0},
       "quando": datetime.datetime.now().isoformat(timespec="seconds")}
if SECO:
    print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v411_sha16", "escada", "n_bandeiras", "registros", "n_patches")}, ensure_ascii=False, indent=1)); print("--seco: NADA gravado; patches:", [e[3] for e in EDITS if not e[3].startswith("C12_")], "+ %d C12" % N_LAD_BASE)
    sys.exit(0)
out = DL.CANDIDATO_ARQ
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V412_REGERAR") == "1", "o candidato ja existe e difere: defina V412_REGERAR=1 para regerar"
if os.path.exists(out) and open(out, "rb").read() != b:
    shutil.copyfile(out, out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
open(DL.MANIFESTO_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(DL.MANIFESTO_ARQ + ".tmp", DL.MANIFESTO_ARQ)
open(DL.FORMAL_MAP_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(FORMAL_MAP, ensure_ascii=False, indent=0)); os.replace(DL.FORMAL_MAP_ARQ + ".tmp", DL.FORMAL_MAP_ARQ)
open(DL.PINS_ARQ + ".tmp", "w", encoding="utf-8", newline="\n").write(RT_); os.replace(DL.PINS_ARQ + ".tmp", DL.PINS_ARQ)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v411_sha16", "escada", "n_bandeiras", "registros")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS if not e[3].startswith("C12_")], "+ %d C12" % N_LAD_BASE)

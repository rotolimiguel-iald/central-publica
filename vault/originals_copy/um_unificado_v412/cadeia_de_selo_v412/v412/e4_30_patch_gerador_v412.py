"""R4: adapta gerar_candidato_v412.py ao contrato R4 (42 modulos; travessia da guarda; emissao versionada do resumo; patch do literal da escada no contrato do H0DN) por trocas de texto exato com contagem. Backup de bytes."""
import sys
from pathlib import Path
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
from e2_lib_v412 import D, salvar_bytes, sha16_arq

P = D / "gerar_candidato_v412.py"
t = P.read_bytes().decode("utf-8")
n_trocas = []


def troca(velho, novo, n=1):
    global t
    c = t.count(velho)
    assert c == n, ("ancora nao tem a contagem esperada", c, n, velho[:90])
    t = t.replace(velho, novo)
    n_trocas.append((velho[:50], c))


troca("assert nov == DL.BUNDLE_RELS and len(nov) == 40", "assert nov == DL.BUNDLE_RELS and len(nov) == 42")
troca("(CONTRATO_v412; nenhum texto daqui entra no programa com historia de conversa)", "(CONTRATO_v412_R4; nenhum texto daqui entra no programa com historia de conversa)")
troca(" (A) kernel: 40 modulos novos em TGLExt/", " (A) kernel: 42 modulos novos em TGLExt/")
# registros: a guarda por travessia (corpo + veredito), unidade por unidade
troca('    assert not GF.violacoes(corpo), (s["nome"], GF.violacoes(corpo)[:3])\n',
      '    _tv = GF.travessia("registro:" + s["nome"], {"corpo": {k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": s["veredito_prefixo"] + "__" + s["veredito_sufixo"]})\n'
      '    assert _tv["ok"] and _tv["n_unidades"] > 0, (s["nome"], _tv["violacoes"][:3])\n')
troca('    assert not GF.violacoes(txt_sec), (lg, GF.violacoes(txt_sec)[:3])\n', '    _ta = GF.travessia("artigo_" + lg, SECAO[lg], "tex"); assert _ta["ok"] and _ta["n_unidades"] > 0, (lg, _ta["violacoes"][:3])\n')
# a funcao versionada do topo do resumo
troca('RCODE = ("_V412_SECAO = "', 'import topo_v412 as TOPOMOD\nTOPO_FUNC = TOPOMOD.construir(top("_v411_topo_texto"))\nRCODE = ("_V412_SECAO = "')
troca('+ "\\n_V412_NOMES_REGISTROS = " + repr(spec_nomes) + "\\n\\n\\n")', '+ "\\n_V412_NOMES_REGISTROS = " + repr(spec_nomes) + "\\n_V412_TOPO = " + pprint.pformat(TOPO12, width=160, sort_dicts=False) + "\\n\\n\\n")')
troca('RT_ = HDR + GUARD_SRC.rstrip("\\n") + "\\n\\n\\n" + CODE_SRC.rstrip("\\n") + "\\n\\n\\n# ---- v412:', 'RT_ = HDR + GUARD_SRC.rstrip("\\n") + "\\n\\n\\n" + CODE_SRC.rstrip("\\n") + "\\n\\n\\n" + TOPO_FUNC.rstrip("\\n") + "\\n\\n\\n# ---- v412:')
# o molde do topo do resumo (dados) e a troca da frase de P = nP: ANTES do RCODE
troca('specs = RG.especs()\n', '''specs = RG.especs()
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
''')
# remove o bloco antigo que trocava a frase dentro de _V411_TOPO
i0 = t.index('tnode = top("_V411_TOPO"); ta, tb = span(tnode.value); topo = ast.literal_eval(tnode.value)\nassert pprint.pformat(topo')
i1 = t.index('_controles(TP, "texto_publico")')
t = t[:i0] + '''for _lg, _nome in (("pt", "pt"), ("en", "en")):   # a emissao do resumo e' versionada: a v412 chama a sua funcao; a da v411 fica como esta
    _a = '{\\\\large\\\\itshape " + _v411_topo_texto(core, "%s") + r""' % _lg
    _c = T0.count(_a); assert _c == 1, ("a chamada do topo na base nao e' unica", _lg, _c)
    _i = T0.index(_a); edit(_i, _i + len(_a), _a.replace("_v411_topo_texto", "_v412_topo_texto"), "W06_topo_" + _lg, "G_ARTIGO", "artigo %s: o resumo chama a emissao versionada do topo (_v412_topo_texto)." % _lg.upper())
    _tp = GF.travessia("resumo_" + _lg, {_lg: [TP["pnp_resumo"][_lg]]}); assert _tp["ok"] and _tp["n_unidades"] > 0, ("o paragrafo do resumo reprova na travessia", _lg, _tp["violacoes"][:3])
    assert not VH.examinar([("resumo_" + _lg, TP["pnp_resumo"][_lg])])["achados"], "historia no paragrafo do resumo"
''' + t[i1:]
# patch do literal da escada no contrato do registro H0DN herdado (dado)
troca('def _spec_block(nome_var):', '''_hc = top("_V411_H0DN_CONTRACT"); _hca, _hcb = span(_hc.value)
_mesc = list(re.finditer(r"'escada': %d(?![0-9])" % E411, T0[_hca:_hcb])); assert len(_mesc) == 1, ("o literal da escada no contrato do H0DN", len(_mesc))
edit(_hca + _mesc[0].start(), _hca + _mesc[0].end(), "'escada': %d" % ESCADA_ESP, "C12b_h0dn_baseline_escada", "G_V411_ESCADA", "_V411_H0DN_CONTRACT baseline.escada %d -> %d (o registro herdado compara a escada do rito com a do contrato)." % (E411, ESCADA_ESP))


def _spec_block(nome_var):''')
troca('.replace("\'expected_ladder\': %d" % ESCADA_ESP, "\'expected_ladder\': %d" % E411) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v412" % fname',
      '.replace("\'expected_ladder\': %d" % ESCADA_ESP, "\'expected_ladder\': %d" % E411).replace("\'escada\': %d" % ESCADA_ESP, "\'escada\': %d" % E411) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v412" % fname')
troca('NOVOS_NOMES = ("_v412_guarda_frases", "_v412_secao_tex", "_v412_rodar_specs", "_V412_SECAO", "_V412_SPECS", "_V412_NOMES_REGISTROS")',
      'NOVOS_NOMES = ("_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia", "_v412_secao_tex", "_v412_rodar_specs", "_v412_topo_texto", "_V412_SECAO", "_V412_SPECS", "_V412_NOMES_REGISTROS", "_V412_TOPO")')
# HDR e comentarios
troca('(%d modulos novos de TGLExt/ (%d bandeiras', '(%d modulos novos de TGLExt/ (%d bandeiras') if False else None
salvar_bytes(P, t.encode("utf-8"))
print("gerador adaptado:", P, sha16_arq(P), "| trocas:", len(n_trocas))

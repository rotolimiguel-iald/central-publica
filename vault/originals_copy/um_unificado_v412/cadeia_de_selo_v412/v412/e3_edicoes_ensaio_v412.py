# -*- coding: utf-8 -*-
"""e3_edicoes_ensaio_v412.py -- a lista de edicoes (id, old, new, n) que e3_ensaio_adaptar_v412.py aplica ao ORIGINAL v411/ensaio_a_seco_v411.py. Script da cadeia; nada daqui entra no programa."""
import os
ED = []


def E(eid, old, new, n=1):
    ED.append((eid, old, new, n))


# ------------------------------------------------------------------ cabecalho e identidade
E("hdr", "# -*- coding: utf-8 -*-\n# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)]",
  "# -*- coding: utf-8 -*-\n# [ADAPTADO v412, 17/11/2026, claude-construtor-v412-ensaio] montado por e3_ensaio_adaptar_v412.py (lista de edicoes em e3_edicoes_ensaio_v412.py) do ORIGINAL v411/ensaio_a_seco_v411.py (nao da subida mecanica de rotulo, guardada em ensaio_a_seco_v412.py.bak_*_bump): a v412 e' a v411 mais UM bundle de 40 modulos de kernel (903 bandeiras; escada 12308 -> 13211) e QUATRO registros por especificacao; o registro com funcao h0dn_bg1_v411 e os specs da v411 passam a HERANCA (DL.D11, _CM11, _KD11); a v412 NAO embute falas.\n# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)]")
E("doc", '"""ensaio_a_seco_v411.py -- [v411, 12/11/2026, claude-construtor-v411, fork C] ENSAIO A SECO da v411: ',
  '"""ensaio_a_seco_v412.py -- [v412, 17/11/2026] ENSAIO A SECO da v412 sobre o candidato gerado: o kernel embutido (1803 arquivos) == o sandbox; o verify de ponta a ponta com o lake simulado devolvendo os logs crus; a escada 12308 -> 13211 so fecha com as 903 bandeiras novas; os registros herdados (de v393 a v411) recriados e comparados com os da v411 selada; os QUATRO registros por especificacao da v412 no ponto de chamada real, cada elo recusando; o artigo PT/EN com a secao nova; o .md; as citacoes; a arvore do Nos simulada; o exame de pontos; as guardas estaticas da Bancada. O texto abaixo e\' o do molde da v411, que fica como registro do que cada secao herdada confere.\nensaio_a_seco_v411.py -- [v411, 12/11/2026, claude-construtor-v411, fork C] ENSAIO A SECO da v411: ')
E("uso", "uso: python -B -X utf8 ensaio_a_seco_v411.py [<candidato.py> <rotulo>]", "uso: python -B -X utf8 ensaio_a_seco_v412.py [<candidato.py> <rotulo>]")
E("delta", "import delta_v411 as DL", "import delta_v412 as DL")
E("pontes", 'sys.modules.setdefault("delta_v410", DL.D10);', 'sys.modules.setdefault("delta_v411", DL.D11); sys.modules.setdefault("delta_v410", DL.D10);')
E("rot", 'rot = sys.argv[2] if len(sys.argv) > 2 else "v411"', 'rot = sys.argv[2] if len(sys.argv) > 2 else "v412"')
E("dry", 'DRY = DL.DRY_DIR if rot == "v411" else', 'DRY = DL.DRY_DIR if rot == "v412" else')
E("um_version", 'assert um.UM_VERSION == "v411"', 'assert um.UM_VERSION == "v412"')
E("selo_base", 'selo0["um_version"] == "v410"', 'selo0["um_version"] == "v411"')
E("cm10", """assert _CM10["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v410.json nao e' o da v410 selada", _CM10["sha16"])""",
  """assert _CM10["sha16"] == DL.D11.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v410.json nao e' o da v410 selada", _CM10["sha16"])
_CM11 = json.load(open(os.path.join(DL.V411, "CANDIDATO_v411.json"), encoding="utf-8"))   # (v412) o candidato da v411 SELADA: os numeros dos blocos HERDADOS da v411 saem dele e do DL.D11, nunca do DL da v412
assert _CM11["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v411.json nao e' o da v411 selada", _CM11["sha16"])
_KD11 = os.path.join(DL.V411, DL.D11.KERNEL_DIR)   # (v412) o kernel dir da v411 (FLAGS, KH_N1 da v411)""")
E("escada_sem_novas",
  """assert rep["escada_sem_as_bandeiras_novas"][0] == E409 == ESP and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is True and CM["n_bandeiras"] == 0, rep["escada_sem_as_bandeiras_novas"]""",
  """assert rep["escada_sem_as_bandeiras_novas"][0] == E409 and rep["escada_sem_as_bandeiras_novas"][1] == ESP and _el0.get("all_verified") is not True and ESP == E409 + CM["n_bandeiras"] == E409 + DL.N_FLAGS and CM["n_bandeiras"] > 0, rep["escada_sem_as_bandeiras_novas"]   # (v412: o kf da v411 SEM as 903 bandeiras novas NAO fecha a escada do candidato: 12308 limpos de 13211 esperados)""")
E("tagged", 'if "v411" in l or "v393" in l', 'if "v412" in l or "v411" in l or "v393" in l')
E("v409n", "+ list(um._V410_NOMES_REGISTROS)   # (v411: e os da v410, HERANCA)", "+ list(um._V410_NOMES_REGISTROS) + list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS)   # (v412: e os da v411, HERANCA: recriados e comparados com os da v411 selada) (v411: e os da v410, HERANCA)")
E("v412n_def", "V411N = list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS)   # (v411) os registros NOVOS da v411:", "V412N = list(um._V412_NOMES_REGISTROS)   # (v412) os registros NOVOS da v412: os quatro por especificacao (o motor e' o da v392; nenhum com funcao; nao existem no core da base) (v411) os registros NOVOS da v411:")
E("v412n_uso", "V411N", "V412N", 7)
E("novas412", "NOVAS411", "NOVAS412", 2)
# ------------------------------------------------------------------ (5b) a ordem de chamada
E("goc_imp", "import guarda_ordem_de_chamada_v411 as _GOC", "import guarda_ordem_de_chamada_v412 as _GOC")
E("goc_fn", "_GOC.FUNCOES_V411", "_GOC.FUNCOES_V412", 2)
E("goc_rep1", 'rep["ordem_de_chamada_v411"] = _ordem', 'rep["ordem_de_chamada_v412"] = _ordem')
E("goc_rep2", 'rep["ordem_de_chamada_v411_controle_negativo"]', 'rep["ordem_de_chamada_v412_controle_negativo"]')
E("goc_u", 'U["v411_ordem_de_chamada_todo_insumo', 'U["v412_ordem_de_chamada_todo_insumo')
E("goc_logo", 'and isinstance(_st3, ast.Assign) and "emit_figures(core)" in ast.unparse(_st3)\n', 'and "_v412_rodar_specs(core)" in ast.unparse(_st3) and "h0dn_bg1_v411(core)" not in ast.unparse(_st3)   # (v412) a instrucao SEGUINTE e\' a dos specs da v412; o emit_figures vem depois dela (bloco 5b-v412)\n')
E("goc_logo_rep", '"na_instrucao_seguinte_a_do_hms13_e_logo_antes_de_emit_figures"', '"na_instrucao_seguinte_a_do_hms13_e_logo_antes_da_instrucao_dos_specs_da_v412"')
E("goc_logo_u", "depois_do_bloco_da_v410_e_antes_de_emit_figures_com_tres_controles_negativos", "depois_do_bloco_da_v410_e_antes_dos_specs_da_v412_com_tres_controles_negativos")
E("goc_logo_print", '"| depois do bloco da v410, antes de emit_figures:"', '"| depois do bloco da v410, antes dos specs da v412:"')
E("goc_novo", "EMBK = um._EMBEDDED_KERNEL_FILES\ncs = lambda: copy.deepcopy(core_s)\n", '''# (5b-v412) A ORDEM DE CHAMADA DOS QUATRO REGISTROS POR ESPECIFICACAO (_v412_rodar_specs), medida por AST sobre o main do candidato (guarda_ordem_de_chamada_v412.ordem_dos_specs): a instrucao e' a SEGUINTE a do h0dn_bg1_v411 (o bloco da v411 INTEIRO ja' rodou)
# e IMEDIATAMENTE antes de emit_figures; toda chave do core que as checagens dos specs leem (a raiz de cada caminho) e que o motor le esta pronta ANTES dela; o cunhagens_v412 vem por ultimo (cobra o selo dos outros tres); examina TODAS as checagens (zero e' falha visivel).
# Controles negativos: (a) a instrucao movida para antes do run_um; (b) a chamada retirada; (c) trocada de lugar com a do h0dn_bg1_v411; (d) uma chave sem origem; (f) sem checagem nenhuma.
_specs_ord = _GOC.specs_do_programa(src)
_op12 = _GOC.ordem_dos_specs(src, _specs_ord); _cn12 = _GOC.controle_negativo_specs(src, _specs_ord)
_ic12 = [i_ for i_, st_ in enumerate(_main0.body) if "_v412_rodar_specs(core)" in ast.unparse(st_)]
_st4 = _main0.body[_ic0 + 4]
_logo12 = bool(len(_ic12) == 1 and _ic12[0] == _ic0 + 3 and isinstance(_st4, ast.Assign) and "emit_figures(core)" in ast.unparse(_st4) and "_v412_rodar_specs(core)" not in (_u0 + _u1 + _u2))
rep["ordem_de_chamada_specs_v412"] = {"real": {k_: v_ for k_, v_ in _op12.items() if k_ != "chaves_lidas"}, "chaves_lidas": _op12.get("chaves_lidas"), "na_instrucao_seguinte_a_do_h0dn_da_v411_e_logo_antes_de_emit_figures": _logo12, "controle_negativo": _cn12, "specs_do_texto_iguais_aos_do_programa_importado": _specs_ord == um._V412_SPECS}
U["v412_ordem_de_chamada_dos_quatro_specs_medida_por_ast_depois_do_bloco_da_v411_e_antes_de_emit_figures_com_cinco_controles_negativos"] = bool(_op12["ok"] and _op12["n_checagens_examinadas"] == sum(len(s_["checks"]) for s_ in um._V412_SPECS) > 0 and _op12["n_specs"] == len(um._V412_NOMES_REGISTROS) == 4 and _logo12 and _cn12["ok"]
                                                                                                                                                                       and _specs_ord == um._V412_SPECS and um._V412_NOMES_REGISTROS[-1] == "cunhagens_v412" and {"qg_closure", "h0dn_bg1_v411", "external_ladder", "kernel_formalization"} <= set(_op12.get("chaves_lidas") or []))
print("ordem de chamada dos specs da v412 (AST propria):", _op12["ok"], "| checagens examinadas:", _op12.get("n_checagens_examinadas"), "| lidas:", sorted(_op12.get("chaves_lidas") or []), "| logo depois do bloco da v411, antes de emit_figures:", _logo12, "| controles negativos:", _cn12["ok"])
EMBK = um._EMBEDDED_KERNEL_FILES
cs = lambda: copy.deepcopy(core_s)
''')


def ER(eid, start, end, new):
    """troca por intervalo (do inicio unico ate a primeira ocorrencia do fim, inclusive)"""
    ED.append((eid, ("R", start, end), new, 1))


# ------------------------------------------------------------------ os modulos da cadeia: o da v412, ou o da v411 por caminho (HERANCA)
E("ac_imp", "import acom_conferencias_v411 as AC", "import acom_conferencias_v412 as AC")
E("gf11", "import guarda_frases_v411 as _GF11  # noqa: E402", '''_MOD411 = {}


def _mod411(nome_):
    """(v412) um modulo da cadeia da v411 (HERANCA), carregado por CAMINHO uma vez, com a pasta da v411 no FIM do sys.path so' durante a carga (os imports dele, *_v411, sao da pasta dele; o delta_v411 e' o DL.D11 por sys.modules; nada da v411 sombreia a v412)."""
    if nome_ not in _MOD411:
        sys.path.append(DL.V411)
        try:
            sp_ = _ilu8.spec_from_file_location(nome_, os.path.join(DL.V411, nome_ + ".py")); m_ = _ilu8.module_from_spec(sp_); sys.modules.setdefault(nome_, m_); sp_.loader.exec_module(m_); _MOD411[nome_] = m_
        finally:
            while DL.V411 in sys.path: sys.path.remove(DL.V411)
    return _MOD411[nome_]


_GF11 = _mod411("guarda_frases_v411")  # noqa: E402''')
E("tr11", "import topo_com_resultado_v411 as _TR11  # noqa: E402", '''DL.TOPO_RATIFICADO_ARQ = os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")   # (v412) o texto ratificado do topo e' o da v411 com SO' a troca da frase final de P = nP do resumo (derivado por e3_topo_derivado_v412.py do manifesto; nada digitado)
import topo_com_resultado_v412 as _TR11  # noqa: E402''')
E("cc11", "import conferir_conversa_v411 as _CC11, registros_v411 as _RG11   # noqa: E402", '_CC11 = _mod411("conferir_conversa_v411"); _RG11 = _mod411("registros_v411")   # noqa: E402 (v412: HERANCA da v411, por caminho)')
E("gc11", "import guarda_conversa_v411 as _GC11   # noqa: E402", "import guarda_conversa_v412 as _GC11   # noqa: E402")
# ------------------------------------------------------------------ rotulos desta versao (nomes de saida e chaves de relatorio)
E("ren_dry", "dry_v411_", "dry_v412_", -1)
E("ren_ensaio_json", "ensaio_a_seco_v411.json", "ensaio_a_seco_v412.json")
E("ren_troca", "troca_dita_v411", "troca_dita_v412", -1)
E("ren_ponto_h0dn", "ponto_h0dn_v411", "ponto_h0dn_v412", -1)
E("ren_formal_map", "formal_map_v411", "formal_map_v412", -1)
E("ren_novos", "registros_novos_v411", "registros_novos_v412")
E("ren_candidato", "candidato_v411", "candidato_v412", -1)
E("ren_sim", "simular_arvore_do_nos_v411", "simular_arvore_do_nos_v412", -1)
E("ren_exame", "exame_pontos_v411", "exame_pontos_v412", -1)
E("ren_citacoes", "conferir_citacoes_v411", "conferir_citacoes_v412", -1)
E("ren_guardas_bancada", "guardas_estaticas_bancada_v411", "guardas_estaticas_bancada_v412", -1)
E("ren_guardas_bancada_up", "GUARDAS_ESTATICAS_BANCADA_v411", "GUARDAS_ESTATICAS_BANCADA_v412", -1)
E("ren_flags", "FLAGS_v411", "FLAGS_v412", -1)
E("ren_sidecar", "v411_sidecar_", "v412_sidecar_", -1)
E("ren_ens", "v411_ens_", "v412_ens_", -1)
E("ren_versao_carimbo", '"**Versão v411**"', '"**Versão v412**"', 2)
# ------------------------------------------------------------------ a arvore do kernel: o numero de entradas do hash formal desta versao (embutidos + residuais do Nos); a v412 nao tem pino exato da arvore (o spec herdado da v411 e' piso)
E("h8_def", 'rep = {"residuais_do_nos_na_arvore_do_ensaio": EXTRAS_NOS,', '_RES12 = list(_CM11["h8"]["residuais_do_nos"]); assert set(EXTRAS_NOS) - set(_RES12) <= {"ExtrairDeps.lean"}, ("residual novo do Nos fora do pino da base", EXTRAS_NOS)   # (o ExtrairDeps.lean sai do hash por exclusao nominal da propria funcao; os residuais contados sao os pinados na v411 selada)\nH8_ENTRADAS = CM["formal_files_n"] + len(_RES12)   # (v412) as entradas do hash formal que o rito ve: os embutidos do candidato (CM["formal_files_n"]) mais os residuais do Nos (pinados na v411 selada); a v412 NAO tem pino exato da arvore (o spec da v411 e\' piso)\nrep = {"residuais_do_nos_na_arvore_do_ensaio": EXTRAS_NOS,')
E("h8_uso", 'CM["h8"]["entradas"]', "H8_ENTRADAS", 6)
E("h8_pino_antigo", 'CM["h8"]["pino_antigo_v410_entradas"]', '_CM11["h8"]["pino_antigo_v410_entradas"]')
E("kh_insumo", "os.path.join(KD, DL.KH_N1_INSUMO)", "os.path.join(_KD11, DL.KH_N1_INSUMO)")
ER("kh11_piso", 'U["kh_n1_cobertura_v411_cobra_a_igualdade_exata"] = bool(', 'encoding="utf-8"))["linha_TOTAL"])',
   '''U["kh_n1_cobertura_v411_herdado_virou_piso_e_selou_na_v412"] = bool(_kh11.get("all_verified") is True and _kh11.get("verdict", "").startswith(DL.KH_PREFIXO + "__") and {i_: _ck11k[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"}
    and _ck11k["h2"]["valor"] == _KHT11["linha_TOTAL"]["decl"] == _ck11k["h6"]["valor"] == _ck11k["h7"]["valor"] and _ck11k["h3"]["valor"] == _KHT11["linha_TOTAL"]["thm"] == _ck11k["h7b"]["valor"] and _ck11k["h8"]["valor"] == _CM11["h8"]["entradas"] and len(_kf0["formal_files_sha256"]) >= _ck11k["h8"]["valor"]
    and _kf0["axiom_coverage_v392"]["decl"] >= _KHT11["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT11["linha_TOTAL"]["thm"] and _kf0["axiom_coverage_v392"]["fora_do_trio"] == 0 and (_kh11.get("extras") or {}).get("n_modulos") == 0 and (_kh11.get("extras") or {}).get("n_bandeiras") == 0
    and _KHT11["linha_TOTAL"] == json.load(open(os.path.join(_KD10, "KH_N1_v410.json"), encoding="utf-8"))["linha_TOTAL"])   # (v412, C13) o spec da v411 HERDADO virou piso; a v412 acrescenta modulos (o Audit cresce) e o veredito dele nao muda''')
E("sim_h8_a", '"pino_h8_entradas": len(_h8)', '"piso_h8_do_spec_herdado": _h8, "entradas_do_hash_formal_esperadas": H8_ENTRADAS')
E("sim_h8_b", '== len(_h8) == H8_ENTRADAS and', '== H8_ENTRADAS and isinstance(_h8, int) and _h8 <= H8_ENTRADAS and')
E("sim_h8_c", '"| pino h8:", len(_h8)', '"| piso h8 (spec herdado):", _h8, "| esperadas:", H8_ENTRADAS')
# ------------------------------------------------------------------ o selo: a chave NOVA do resumo e' registros_v412; os registros da v411 (o de funcao e os specs) sao HERANCA e nao mudam no resumo
E("selo_inexplicado", '"sha256", "registros_v411") + tuple(um._V411_REGISTROS_FUNCAO) and not _selo_explica(k_))', '"sha256", "registros_v412") and not _selo_explica(k_))')
E("selo_ok_a", '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v411"} | set(um._V411_REGISTROS_FUNCAO)) <= set(mud_selo)', '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v412"}) <= set(mud_selo)')
E("selo_ok_b", '"registros_v410"} & set(mud_selo)) and not (set(um._V410_REGISTROS_FUNCAO) & set(mud_selo)))',
  '"registros_v410", "registros_v411"} & set(mud_selo)) and not ((set(um._V410_REGISTROS_FUNCAO) | set(um._V411_REGISTROS_FUNCAO)) & set(mud_selo)) and all(((seal.get("registros_v412") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V412_NOMES_REGISTROS) and len(seal.get("registros_v412") or {}) == 4)')
# ------------------------------------------------------------------ (6r) os quatro registros por especificacao da v412
E("blk6r", "# (8) o artigo\n", open(os.path.join(HERE, "e3_bloco_6r_v412.pytxt"), encoding="utf-8").read() + "# (8) o artigo\n")
# ------------------------------------------------------------------ o MODO DIAGNOSTICO (rotulo diferente de v412): uma copia do candidato com UM literal diferente (e3_candidato_diagnostico_v412.py), manifesto proprio e saida propria; o rotulo v412 segue com a rigidez inteira
E("cm_diag", 'CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); assert CM["sha16"] == h16,', 'CM = json.load(open(DL.MANIFESTO_ARQ if rot == "v412" else os.environ["V412_ENSAIO_MANIFESTO_DIAGNOSTICO"], encoding="utf-8")); assert CM["sha16"] == h16,')
E("saida_diag", '_pE = DL.saida("ensaio_a_seco_v412.json");', '_pE = DL.saida("ensaio_a_seco_v412.json") if rot == "v412" else os.path.join(DL.RODADA_PAI, "diag", "ensaio_a_seco_v412_%s.json" % rot);')
# ------------------------------------------------------------------ (8) o artigo: a secao nova da v412 (antes da da v411), o sumario, os titulos devidos, a variante sem os registros da v412
E("art_fn", "def compilar(cv, nome, lang, duas=True):", open(os.path.join(HERE, "e3_bloco_artigo_v412.pytxt"), encoding="utf-8").read() + "def compilar(cv, nome, lang, duas=True):")
E("art_call", 'rep["artigo"][lang]["v411"] = _checagens_v411_do_artigo(tex, txt, lang)', 'rep["artigo"][lang]["v412"] = _checagens_v412_do_artigo(tex, txt, lang)   # (v412) a secao nova, o resumo com o paragrafo vigente de P = nP\n    rep["artigo"][lang]["v411"] = _checagens_v411_do_artigo(tex, txt, lang)')
E("art_mau", 'or not v["v411"]["ok"]]', 'or not v["v411"]["ok"] or not v["v412"]["ok"]]')
E("toc_pt", 'TOC = {"pt": [um._v411_tex_unicode(DL.TITULO_SECAO_PT), TI410,', 'TOC = {"pt": [DL.TITULO_SECAO_V412["pt"], um._v411_tex_unicode(DL.TITULO_SECAO_PT), TI410,')
E("toc_en", '"en": [um._v411_tex_unicode(DL.TITULO_SECAO_EN), TI410E,', '"en": [DL.TITULO_SECAO_V412["en"], um._v411_tex_unicode(DL.TITULO_SECAO_EN), TI410E,')
E("var12", 'print("variante v411:", rep["variante_v411"])\n', 'print("variante v411:", rep["variante_v411"])\n' + open(os.path.join(HERE, "e3_bloco_variante_v412.pytxt"), encoding="utf-8").read())
E("ok_var12", "and not mau and not mau_var and not mau_var11 and", "and not mau and not mau_var and not mau_var11 and not mau_var12 and")
E("fail_var12", '"variante_v411": mau_var11', '"variante_v411": mau_var11, "variante_v412": mau_var12')
E("cv11_fix", "[cv11.pop(k, None) for k in V412N]", "[cv11.pop(k, None) for k in list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS)]")
E("deve12", 'GUARDA = re.compile("(?<!NOT_)(?<!UN)"', open(os.path.join(HERE, "e3_bloco_deve12.pytxt"), encoding="utf-8").read() + 'GUARDA = re.compile("(?<!NOT_)(?<!UN)"')
E("regs_sim", "_regs_sim = tuple(um._V411_REGISTROS_FUNCAO) + tuple(um._V411_NOMES_REGISTROS) +", "_regs_sim = tuple(um._V412_NOMES_REGISTROS) + tuple(um._V411_REGISTROS_FUNCAO) + tuple(um._V411_NOMES_REGISTROS) +")
E("kht6", 'os.path.join(KD, "KH_N1_v411.json")', 'os.path.join(KD, "KH_N1_v412.json")')
E("contratos_escada", "and _n_esc_base >= 1 and _n_esc_cand == _n_esc_base and E409 == ESP", 'and _n_esc_base >= 1 and _n_esc_cand == _n_esc_base and ESP == E409 + CM["n_bandeiras"]   # (v412: a escada CRESCE com as bandeiras novas; os 30 literais expected_ladder do selado sao todos trocados pelo novo)')
# ------------------------------------------------------------------ HERANCA da v410 com numeros do kernel que CRESCEU: o hash formal e a escada sao os DESTA versao (CM), a escada da v410 + as bandeiras novas = a desta
E("iald2_h8_escada", 'len(_kf0["formal_files_sha256"]) == _CM10["h8"]["entradas"] and ESP == _CM10["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP10["expected_ladder"] == _E409_10 + _CM10["n_bandeiras"]',
  'len(_kf0["formal_files_sha256"]) == H8_ENTRADAS and ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CP10["expected_ladder"] == _CM10["escada"][1] + CM["n_bandeiras"]')
E("aescala_escada", '"escada": ESP == _CM10["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CPA["expected_ladder"] == _E409_10 + _CM10["n_bandeiras"] and',
  '"escada": ESP == CM["escada"][1] == c["external_ladder"]["n_theorems_clean"] == c["external_ladder"]["n_theorems_expected"] == _CPA["expected_ladder"] == _CM10["escada"][1] + CM["n_bandeiras"] and')
E("toc_ultimo_pt", '"v384 a v411"', '"v384 a v412"')
E("toc_ultimo_en", '"v384 to v411"', '"v384 to v412"')
E("viol_art_v411_com_a_guarda_v412", "_GF11.violacoes(l_)) for i_, l_ in enumerate(novos_)]", "um._v412_guarda_frases(l_)) for i_, l_ in enumerate(novos_)]   # (v412: o resumo traz o paragrafo vigente de P = nP: as obrigacoes mudadas valem para o texto que a v412 escreve; a guarda da v412 herda a da v411 inteira)")
# ------------------------------------------------------------------ R4: o core ganha UMA chave nova de topo (guarda_frases_v412: o resultado da travessia); a emissao do resumo e' versionada (_V412_TOPO, _v412_topo_texto)
E("v412r_def", "V412N = list(um._V412_NOMES_REGISTROS)   # (v412) os registros NOVOS da v412:", 'V412R = list(um._V412_NOMES_REGISTROS); V412N = V412R + ["guarda_frases_v412"]   # (v412) os registros NOVOS da v412 (V412R) e a chave nova do core, o resultado da travessia da guarda de frases (V412N):')
E("v412r_mf", '"declaracao_do_operador_v399"] + V409N + V412N)', '"declaracao_do_operador_v399"] + V409N + V412R)')
E("v412r_novos", "for n_ in V412N},", "for n_ in V412R},")
E("topo12_a", "um._V411_TOPO", "um._V412_TOPO", -1)
E("topo12_b", "um._v411_topo_texto", "um._v412_topo_texto", -1)

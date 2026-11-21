# -*- coding: utf-8 -*-
"""Etapa 2 da v413, bloco 6 (o ensaio a seco): deriva, das copias finais da v412 (a familia _r7, intacta), as copias _v413 do ENSAIO A SECO e dos seus auxiliares, por trocas de texto EXATO com contagem EXATA
(ou trocas restritas a uma regiao entre marcas unicas) e insercoes de blocos NOVOS entre marcas unicas; cada troca fica registrada em DERIVACAO_ETAPA2_ENSAIO_v413.json. O que muda, em resumo:
  - o delta e' o delta_v413; a base e' a v412 selada (o candidato da v412 SELADA, _CM12, da' os numeros da heranca da v412); os modulos da cadeia da v412 sao carregados por CAMINHO (_mod412);
  - os registros da v412 passam a HERANCA (recriados pelo fluxo e comparados com os da v412 selada; o bloco (6r) le os numeros deles da pasta da v412 e do DL.D12);
  - NOVO: (5b-v413) a ordem de chamada dos cinco specs da v413; (6s) os cinco registros da v413 no ponto real (tudo certo, numeros recalculados, cada elo recusa, a ligacao, a guarda herdada, a historia);
    a secao nova do artigo (_checagens_v413_do_artigo) e a variante sem os registros da v413; o modulo corrigido (o hash formal com o texto novo; as mesmas declaracoes);
  - os auxiliares: simular_arvore_do_nos, exame_pontos (o ponto dos specs da v413), guarda_ordem_de_chamada (as funcoes da v413), guardas_estaticas_bancada (o sandbox curto proprio da Etapa 2),
    conferir_citacoes (os textos da v413) e guarda_conversa (a base pinada da v412 selada).
Nada no Nos; os originais ficam intactos."""
import datetime, hashlib, json, os, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
V412 = D.parent / "v412"
LOGP = D / "DERIVACAO_ETAPA2_ENSAIO_v413.json"
sha = lambda b: hashlib.sha256(b).hexdigest()
CAB = "# [DERIVADO v413, claude-construtor-v413] copia de v412\\%s; trocas de texto exato com contagem registrada em DERIVACAO_ETAPA2_ENSAIO_v413.json (derivador: e7_06_derivar_ensaio_v413.py). O original fica intacto."


def derivar(origem, destino, trocas=(), regioes=(), insercoes=(), final=""):
    """trocas: (velho, novo, n) com n EXATO (None = pelo menos uma, todas trocadas); regioes: (marca_ini, marca_fim, [(velho, novo, n)]) trocas so' dentro da regiao [ini, fim);
    insercoes: (marca, texto, 'antes'|'depois_da_linha') com a marca UNICA; final: texto acrescentado ao fim."""
    t = (V412 / origem).read_bytes().decode("utf-8")
    assert "\r" not in t, origem
    reg = {"origem": "v412/" + origem, "origem_sha16": sha(t.encode())[:16], "destino": destino, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "trocas": [], "regioes": [], "insercoes": []}
    for velho, novo, n in trocas:
        c = t.count(velho)
        assert (c == n) if n is not None else (c >= 1), ("troca sem a contagem esperada", origem, velho[:140], c, n)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:180], "novo": novo[:180], "ocorrencias": c})
    for ini, fim, tr in regioes:
        a = t.index(ini); assert t.count(ini) == 1, ("marca de regiao nao unica", ini[:80])
        b = t.index(fim, a); assert t.count(fim) == 1, ("marca de regiao nao unica", fim[:80])
        seg = t[a:b]
        r_ = {"ini": ini[:80], "fim": fim[:80], "trocas": []}
        for velho, novo, n in tr:
            c = seg.count(velho)
            assert (c == n) if n is not None else (c >= 1), ("troca de regiao sem a contagem esperada", origem, ini[:60], velho[:140], c, n)
            seg = seg.replace(velho, novo)
            r_["trocas"].append({"velho": velho[:180], "novo": novo[:180], "ocorrencias": c})
        t = t[:a] + seg + t[b:]
        reg["regioes"].append(r_)
    for marca, texto, modo in insercoes:
        assert t.count(marca) == 1, ("marca de insercao nao unica", origem, marca[:100], t.count(marca))
        i = t.index(marca)
        if modo == "antes":
            t = t[:i] + texto + t[i:]
        else:
            j = t.index("\n", i) + 1
            t = t[:j] + texto + t[j:]
        reg["insercoes"].append({"marca": marca[:120], "modo": modo, "bytes": len(texto.encode("utf-8"))})
    if final:
        t = t.rstrip("\n") + "\n" + final
    linhas = t.split("\n")
    k = 1 if linhas[0].startswith("# -*- coding") else 0
    t = "\n".join(linhas[:k] + [CAB % origem] + linhas[k:])
    compile(t, destino, "exec")
    out = t.encode("utf-8")
    p = D / destino
    if not (p.exists() and p.read_bytes() == out):
        if p.exists():
            bk = Path(str(p) + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes()); assert bk.read_bytes() == p.read_bytes()
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(out); assert tmp.stat().st_size == len(out); os.replace(tmp, p)
    reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    log = json.loads(LOGP.read_bytes().decode("utf-8")) if LOGP.exists() else {"derivacoes": {}}
    log["derivacoes"][destino] = reg
    tmp = Path(str(LOGP) + ".tmp"); b = json.dumps(log, ensure_ascii=False, indent=1).encode("utf-8"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, LOGP)
    print("derivado: %-42s <- %-42s %8d bytes sha16 %s | trocas %d regioes %d insercoes %d" % (destino, origem, len(out), sha(out)[:16], len(reg["trocas"]), len(reg["regioes"]), len(reg["insercoes"])))


# =============================================================================================== simular_arvore_do_nos
derivar("simular_arvore_do_nos_v412_r7.py", "simular_arvore_do_nos_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ("um._v411_rodar_specs(core); um._v412_rodar_specs(core)   #", "um._v411_rodar_specs(core); um._v412_rodar_specs(core); um._v413_rodar_specs(core)   # (v413: os cinco registros por especificacao da v413 DEPOIS dos da v412, como no main)", 1),
    ("for k in tuple(DL.REGISTROS_FUNCAO) + tuple(DL.REGISTROS_SPEC_V412) + (DL.CUNHAGENS_REGISTRO", "for k in tuple(DL.REGISTROS_FUNCAO) + tuple(DL.REGISTROS_SPEC_V413) + tuple(DL.REGISTROS_SPEC_V412) + (DL.CUNHAGENS_REGISTRO", 1),
    ('os.environ.get("V412_ENSAIO_MANIFESTO_DIAGNOSTICO")', 'os.environ.get("V413_ENSAIO_MANIFESTO_DIAGNOSTICO")', 1),
    ("formal_map_v412", "formal_map_v413", None),
    ('R["registros_v412_selaram"] = {k_: (core.get(k_) or {}).get("all_verified") for k_ in tuple(DL.REGISTROS_FUNCAO) + tuple(DL.REGISTROS_SPEC_V412)',
     'R["registros_v413_selaram"] = {k_: (core.get(k_) or {}).get("all_verified") for k_ in tuple(DL.REGISTROS_FUNCAO) + tuple(DL.REGISTROS_SPEC_V413) + tuple(DL.REGISTROS_SPEC_V412)', 1),
])

# =============================================================================================== guardas_estaticas_bancada (o sandbox curto PROPRIO da Etapa 2: DL.SANDBOX_GUARDAS; nunca o do B(n))
derivar("guardas_estaticas_bancada_v412_r7.py", "guardas_estaticas_bancada_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ("import acom_conferencias_v412 as AC  # noqa: E402", "import acom_conferencias_v413 as AC  # noqa: E402", 1),
    ('DL.saida("GUARDAS_ESTATICAS_BANCADA_v412.json")', 'DL.saida("GUARDAS_ESTATICAS_BANCADA_v413.json")', 1),
    ("DL.SANDBOX_CURTO", "DL.SANDBOX_GUARDAS", None),
    ('"contrato": "GUARDAS_ESTATICAS_BANCADA_v412"', '"contrato": "GUARDAS_ESTATICAS_BANCADA_v413"', 1),
    ('candidato_v412', 'candidato_v413', None),
    ('"v412", beta=', '"v413", beta=', 1),
    ('json.dump({"um_version": "v412", "sha256"', 'json.dump({"um_version": "v413", "sha256"', 1),
    ('b\'UM_VERSION = "v412"\\r\\n\'', 'b\'UM_VERSION = "v413"\\r\\n\'', 1),
    ('b\'if True:\\r\\n    UM_VERSION = "v412"\\r\\n\'', 'b\'if True:\\r\\n    UM_VERSION = "v413"\\r\\n\'', 1),
    ('"v412")', '"v413")', None),
    ('res["canonical_py_instalado"]["le_versao"] == "v412"', 'res["canonical_py_instalado"]["le_versao"] == "v413"', 1),
])

# =============================================================================================== guarda_ordem_de_chamada (acrescenta as funcoes da v413; as da v412 ficam como estao)
FINAL_GOC = r'''

# ---------------------------------------------------------------- (v413) os CINCO registros por especificacao da v413: a ordem de chamada de _v413_rodar_specs(core)
CHAMADA_SPECS_V413 = "_v413_rodar_specs(core)"
EXIGIDOS_DOS_SPECS_V413 = EXIGIDOS_DOS_SPECS_V412 + ("_v412_rodar_specs",)   # o bloco da v412 INTEIRO (os specs da v412 e a travessia deles) roda antes; os specs da v413 leem o gate, o H0DN e a escada


def specs_do_programa_v413(src):
    """os specs da v413, lidos do TEXTO do programa por AST (a atribuicao literal de _V413_SPECS): nada executa."""
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_V413_SPECS" for t in n.targets):
            return ast.literal_eval(n.value)
    raise AssertionError("_V413_SPECS nao achado no programa")


def raizes_lidas_pelos_specs_v413(specs):
    """como raizes_lidas_pelos_specs, com as chaves que o PROPRIO _v413_rodar_specs grava (os registros e o resultado da travessia: guarda_frases_v413)."""
    nomes = {s["nome"] for s in specs} | {"guarda_frases_v413"}
    raizes, n = {}, 0
    for s in specs:
        for ck in s["checks"]:
            n += 1
            if ck.get("onde") == "core" and ck.get("caminho"):
                raizes.setdefault(ck["caminho"][0], set()).add(s["nome"] + "." + ck["id"])
            elif ck.get("onde") == "kf":
                raizes.setdefault("kernel_formalization", set()).add(s["nome"] + "." + ck["id"])
    return {k: sorted(v) for k, v in raizes.items() if k not in nomes}, nomes, n


def ordem_dos_specs_v413(src, specs, chamada=CHAMADA_SPECS_V413, exigidos=EXIGIDOS_DOS_SPECS_V413, raizes_extras=()):
    """a ordem_dos_specs com a chamada, os exigidos e as raizes da v413 (as chaves gravadas pelo proprio _v413_rodar_specs ficam fora)."""
    global raizes_lidas_pelos_specs
    _orig = raizes_lidas_pelos_specs
    raizes_lidas_pelos_specs = raizes_lidas_pelos_specs_v413
    try:
        return ordem_dos_specs(src, specs, chamada=chamada, exigidos=exigidos, raizes_extras=raizes_extras)
    finally:
        raizes_lidas_pelos_specs = _orig


def controle_negativo_specs_v413(src, specs):
    """(a) a instrucao dos specs da v413 movida para ANTES do run_um reprova; (b) a chamada retirada reprova; (c) trocada de lugar com a dos specs da v412 reprova (o insumo exigido ausente);
    (d) uma chave sem origem reprova; (e) a fonte intacta passa; (f) sem checagem nenhuma reprova. Rodado sobre o texto: nada executa."""
    r0 = ordem_dos_specs_v413(src, specs)
    lin = src.split("\n")
    main = [x for x in ast.parse(src).body if isinstance(x, ast.FunctionDef) and x.name == "main"][-1]
    unp = [ast.unparse(st) for st in main.body]
    irun = [i for i, st in enumerate(main.body) if "run_um(" in unp[i] and isinstance(st, ast.Assign)][0]
    ic = [i for i, s in enumerate(unp) if CHAMADA_SPECS_V413 in s][0]
    st = main.body[ic]
    bloco = lin[st.lineno - 1:st.end_lineno]; dest = main.body[irun].lineno - 1
    ra = ordem_dos_specs_v413("\n".join(lin[:dest] + bloco + lin[dest:st.lineno - 1] + lin[st.end_lineno:]), specs)
    rb = ordem_dos_specs_v413(_sem_chamada(src, "_v413_rodar_specs", "_n413"), specs)
    rc = ordem_dos_specs_v413(_troca_blocos(src, "_v412_rodar_specs", "_v413_rodar_specs"), specs)
    rd = ordem_dos_specs_v413(src, specs, raizes_extras=("chave_que_nao_existe_v413",))
    re_ = ordem_dos_specs_v413(src, [])
    c = {"intacta_passa": bool(r0["ok"]), "specs_antes_do_run_um_reprova": bool(not ra["ok"] and ra.get("lidos_antes_da_atribuicao")), "specs_sem_chamada_no_main_reprova": bool(not rb["ok"] and rb.get("erro") == "chamada no main ausente ou nao unica"),
         "specs_antes_dos_specs_da_v412_reprova": bool(not rc["ok"] and "_v412_rodar_specs" in (rc.get("insumos_exigidos_ausentes") or [])),
         "chave_sem_origem_reprova": bool(not rd["ok"] and "chave_que_nao_existe_v413" in (rd.get("lidas_sem_origem") or [])), "zero_checagens_reprova": bool(not re_["ok"])}
    c["ok"] = bool(all(c.values()))
    return c
'''
derivar("guarda_ordem_de_chamada_v412_r7.py", "guarda_ordem_de_chamada_v413.py", trocas=[
    ("sys.path.insert(0, _aqui); import delta_v412_r7 as _DL11", "sys.path.insert(0, _aqui); import delta_v413 as _DL11", 1),
], final=FINAL_GOC)

# =============================================================================================== conferir_citacoes (os textos da v413; a v413 nao embute falas)
derivar("conferir_citacoes_v412_r7.py", "conferir_citacoes_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ("FALAS = {f_[\"nome\"]: f_[\"text\"] for f_ in DL.FALAS_V412}", "FALAS = {f_[\"nome\"]: f_[\"text\"] for f_ in DL.FALAS_V413}", 1),
    ('("textos_v412.py", "registrar_mapa_v412.py", "fechar_v412.py", "leitura_v412.py", "superficies_v412.py", "textos_custodia_handoff_v412.py", "blocos_custodia_v412.py", "textos_v412_novo.pysnip")',
     '("textos_v413.py", "registrar_mapa_v413.py", "fechar_v413.py", "leitura_v413.py", "superficies_v413.py", "textos_custodia_handoff_v413.py", "blocos_custodia_v413.py", "textos_v413_novo.pysnip")', 1),
    ('ARQS = ["delta_v412_r7.py", "registros_v412_r7.py", "textos_registros_v412_r7.py", "runtime_v412_guarda.py", "gerar_candidato_v412_r7.py", "TEXTO_PUBLICO_v412.json", "TOPO_RATIFICADO_v412_DERIVADO.json"]',
     'ARQS = ["delta_v413.py", "registros_v413.py", "textos_registros_v413.py", "runtime_v413_codigo.py", "gerar_candidato_v413.py", DL.TEXTO_PUBLICO_ARQ]', 1),
    ('_MARCA = "[A ADAPTAR v" + "412]"', '_MARCA = "[A ADAPTAR v" + "413]"', 1),
    ('"contrato": "CONFERIR_CITACOES_v412", "n_falas_v412": len(FALAS)', '"contrato": "CONFERIR_CITACOES_v413", "n_falas_v413": len(FALAS)', 1),
    ('ROTULOS_V412 = {}   # a v412 nao acrescenta rotulo', 'ROTULOS_V412 = {}   # (a v412 nao acrescentou rotulo; a v413 tambem nao) a v412 nao acrescenta rotulo', 1),
    ('if len(fr_) < 12 or "_V411_" in fr_ or "_V412_" in fr_:', 'if len(fr_) < 12 or "_V411_" in fr_ or "_V412_" in fr_ or "_V413_" in fr_:', 1),
    ('DL.saida("conferir_citacoes_v412.json")', 'DL.saida("conferir_citacoes_v413.json")', 1),
])

# =============================================================================================== guarda_conversa (a base pinada passa a ser a da v412 selada)
derivar("guarda_conversa_v412_r7.py", "guarda_conversa_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ('BASE_JSON = os.path.join(HERE, "GUARDA_CONVERSA_BASE_v411.json")', 'BASE_JSON = os.path.join(HERE, "GUARDA_CONVERSA_BASE_v412.json")', 1),
    ('"contrato": "GUARDA_CONVERSA_BASE_v411"', '"contrato": "GUARDA_CONVERSA_BASE_v412"', 1),
    ('"o Nos nao esta\' na v411 selada: a base da regra (b) so\' se gera antes do rito"', '"o Nos nao esta\' na v412 selada: a base da regra (b) so\' se gera antes do rito"', 1),
    ('"contrato": "GUARDA_CONVERSA_v412"', '"contrato": "GUARDA_CONVERSA_v413"', 1),
    ('os.path.join(HERE, "GUARDA_CONVERSA_v412.json")', 'os.path.join(HERE, "GUARDA_CONVERSA_v413.json")', 1),
    # (v413) a base da regra (b) e' a v412 selada (o Nos na v412): o stdout da base passa a ser o da rodada v412, e o alvo pos-rito o da rodada v413; o nome do dicionario e as frases que dizem a versao da base seguem
    ('"stdout": "rodada_v412_stdout.txt"}', '"stdout": "rodada_v413_stdout.txt"}', 1),
    ('stdout="rodada_v411_stdout.txt")', 'stdout="rodada_v412_stdout.txt")', 1),
    ("ARQS_V411", "ARQS_BASE_V412", 3),
    ("base v411", "base v412", 5),
    ("rendidos selados da v411", "rendidos selados da v412", 3),
    ("Nos AINDA na v411", "Nos AINDA na v412", 1),
    ("o Nos ainda na v411 selada", "o Nos ainda na v412 selada", 1),
    ("guarda_conversa_v412.py --gerar-base", "guarda_conversa_v413.py --gerar-base", 1),
    ("ficam em GUARDA_CONVERSA_BASE_v411.json", "ficam em GUARDA_CONVERSA_BASE_v412.json", 1),
    # (v413) a base gravada so' vale se os arquivos que ela leu sao os da base corrente (o nome de cada um): uma base com o stdout de outra rodada e' regerada, nunca aceita em silencio
    ('if set(b_["linhas"]) == {_sha16(l_) for _, l_ in curtas_} and b_.get("base_sha16") == DL.BASE_SHA16_DA_ORDEM:',
     'if set(b_["linhas"]) == {_sha16(l_) for _, l_ in curtas_} and b_.get("base_sha16") == DL.BASE_SHA16_DA_ORDEM and {t_: (v_ or {}).get("nome") for t_, v_ in (b_.get("arquivos") or {}).items()} == ARQS_BASE_V412:', 1),
])

# =============================================================================================== exame_pontos (o ponto NOVO: os specs da v413, logo depois dos da v412 e antes do emit_figures)
INS_EXAME_V413 = r'''# (4k) [v413] o PONTO DE CHAMADA REAL dos cinco registros por especificacao da v413 (executado dentro do bloco acima): a instrucao do main LOGO DEPOIS da dos specs da v412 e IMEDIATAMENTE antes de emit_figures; o motor e' o da v392;
#      o veredito e' a palavra do CONTRATO da v413 (lida pelo delta); o numero de checagens e' o do spec (zero nao passa); a travessia da guarda herdada da v412 grava guarda_frases_v413
_pv13 = {}
for _n13 in DL.REGISTROS_SPEC_V413:
    _r13 = core.get(_n13) or {}; _s13 = [s_ for s_ in um._V413_SPECS if s_["nome"] == _n13][0]
    _pv13[_n13] = {"all_verified": _r13.get("all_verified"), "verdict": _r13.get("verdict"), "palavra_do_contrato": DL.PALAVRAS_DE_VEREDITO[_n13], "n_checks": len(_r13.get("checks") or []), "n_checks_do_spec": len(_s13["checks"]),
                   "checks_falhos": [str(c_.get("descricao"))[:80] for c_ in (_r13.get("checks") or []) if not c_.get("ok")][:4], "kernel": _r13.get("kernel"), "does_not_gate_core": _r13.get("does_not_gate_core"),
                   "guarda_n_unidades": ((core.get("guarda_frases_v413") or {}).get(_n13) or {}).get("n_unidades_examinadas"), "guarda_n_violacoes": ((core.get("guarda_frases_v413") or {}).get(_n13) or {}).get("n_violacoes")}
    out["core." + _n13] = {"all_verified": _r13.get("all_verified"), "verdict": str(_r13.get("verdict"))[:300], "falhas": _pv13[_n13]["checks_falhos"]}
R["ponto_specs_v413"] = {"indice_no_main": iv13, "linha": main.body[iv13].lineno, "logo_depois_da_instrucao_dos_specs_da_v412": iv13 == iv12 + 1, "logo_antes_do_emit_figures": iv13 + 1 == i1, "dentro_do_bloco_executado": i0 <= iv13 < i1,
                         "chama_so_os_specs_da_v413": "_v412_rodar_specs(core)" not in unp[iv13] and "h0dn_bg1_v411(core)" not in unp[iv13], "n_registros": len(_pv13), "registros": _pv13}
'''
INS_EXAME_GUARDA13 = r'''    if k == "guarda_frases_v413":   # (v413) o resultado da travessia da guarda herdada da v412 sobre os registros da v413: um por registro, unidades > 0, zero violacao
        _gv = v; v = {"all_verified": bool(len(_gv) == len(DL.REGISTROS_SPEC_V413) and set(_gv) == set(DL.REGISTROS_SPEC_V413) and all(isinstance(x_, dict) and x_.get("n_violacoes") == 0 and isinstance(x_.get("n_unidades_examinadas"), int) and x_["n_unidades_examinadas"] > 0 for x_ in _gv.values())),
                      "verdict": "TRAVESSIA_DA_GUARDA_DE_FRASES_V413 " + json.dumps({n_: [x_.get("n_unidades_examinadas"), x_.get("n_violacoes")] for n_, x_ in _gv.items()}, ensure_ascii=False)}
'''
INS_EXAME_FALSO13 = r'''pv13_ = R["ponto_specs_v413"]   # (4k) o ponto NOVO da v413: os cinco registros por especificacao
if (not pv13_["logo_depois_da_instrucao_dos_specs_da_v412"] or not pv13_["logo_antes_do_emit_figures"] or not pv13_["dentro_do_bloco_executado"] or not pv13_["chama_so_os_specs_da_v413"] or pv13_["n_registros"] != len(DL.REGISTROS_SPEC_V413)
        or any(v_["all_verified"] is not True or v_["verdict"] != v_["palavra_do_contrato"] or v_["n_checks"] != v_["n_checks_do_spec"] or v_["n_checks"] <= 0 or v_["checks_falhos"] or v_["does_not_gate_core"] is not True or not isinstance(v_["guarda_n_unidades"], int) or v_["guarda_n_unidades"] <= 0 or v_["guarda_n_violacoes"] != 0 for v_ in pv13_["registros"].values())): falsos.append("ponto_specs_v413")
'''
derivar("exame_pontos_v412_r7.py", "exame_pontos_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ("+ list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS) + list(um._V412_NOMES_REGISTROS):   #", "+ list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS) + list(um._V412_NOMES_REGISTROS) + list(um._V413_NOMES_REGISTROS):   # (v413: + os cinco da v413)", 1),
    ("and len(iv12) == 1 and iv12[0] == ih11[0] + 1 and iv12[0] + 1 == i1, (", "and len(iv12) == 1 and iv12[0] == ih11[0] + 1 and len(iv13) == 1 and iv13[0] == iv12[0] + 1 and iv13[0] + 1 == i1, (", 1),
    ("ih11 = ih11[0]; iv12 = iv12[0]", "ih11 = ih11[0]; iv12 = iv12[0]; iv13 = iv13[0]", 1),
    ('"logo_antes_da_instrucao_dos_specs_da_v412": ih11 + 1 == iv12 and iv12 + 1 == i1,', '"logo_antes_da_instrucao_dos_specs_da_v412": ih11 + 1 == iv12 and iv12 + 2 == i1,', 1),
    ('"palavra_do_contrato": DL.PALAVRAS_DE_VEREDITO[_n12]', '"palavra_do_contrato": DL.D12.PALAVRAS_DE_VEREDITO[_n12]', 1),
    ('"logo_depois_da_instrucao_do_h0dn_da_v411": iv12 == ih11 + 1, "logo_antes_do_emit_figures": iv12 + 1 == i1,', '"logo_depois_da_instrucao_do_h0dn_da_v411": iv12 == ih11 + 1, "logo_antes_do_emit_figures": iv12 + 1 == iv13 and iv13 + 1 == i1,', 1),
    ('os.environ.get("V412_ENSAIO_MANIFESTO_DIAGNOSTICO")', 'os.environ.get("V413_ENSAIO_MANIFESTO_DIAGNOSTICO")', 1),
    ('(out.get("core." + k, {}).get("all_verified") if k == "guarda_frases_v412" else core[k].get("all_verified"))', '(out.get("core." + k, {}).get("all_verified") if k in ("guarda_frases_v412", "guarda_frases_v413") else core[k].get("all_verified"))', 1),
    ('                   "novas": [k for k in R["chaves_novas_no_core"]', '                   "v412_specs_herdados": [k for k in list(um._V412_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n                   "novas": [k for k in R["chaves_novas_no_core"]', 1),
], insercoes=[
    ('iv12 = [i for i, s_ in enumerate(unp) if "_v412_rodar_specs(core)" in s_]', 'iv13 = [i for i, s_ in enumerate(unp) if "_v413_rodar_specs(core)" in s_]   # (v413) os cinco registros por especificacao da v413: a instrucao seguinte a dos specs da v412, imediatamente antes de emit_figures\n', "depois_da_linha"),
    ('R["chaves_novas_no_core"] = sorted(set(core) - set(antes))', INS_EXAME_V413, "antes"),
    ('    if isinstance(v, dict):\n        out["core." + k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:300], "falhas": falhas_de(v)}', INS_EXAME_GUARDA13, "antes"),
    ('if R["troca_dita_v412"]["ok"] is not True: falsos.append("troca_dita_v412")', INS_EXAME_FALSO13, "antes"),
])

# =============================================================================================== o ENSAIO A SECO
MOD412 = r'''_MOD412 = {}


def _mod412(nome_):
    """(v413) um modulo da cadeia da v412 (HERANCA), carregado por CAMINHO uma vez, com a pasta da v412 no FIM do sys.path so' durante a carga (os imports dele, *_v412*, sao da pasta dele; o delta_v412_r7 e' o DL.D12 por sys.modules)."""
    if nome_ not in _MOD412:
        sys.path.append(DL.V412)
        try:
            sp_ = _ilu8.spec_from_file_location(nome_, os.path.join(DL.V412, nome_ + ".py")); m_ = _ilu8.module_from_spec(sp_); sys.modules.setdefault(nome_, m_); sp_.loader.exec_module(m_); _MOD412[nome_] = m_
        finally:
            while DL.V412 in sys.path: sys.path.remove(DL.V412)
    return _MOD412[nome_]


'''
ORDEM13 = r'''# (5b-v413) A ORDEM DE CHAMADA DOS CINCO REGISTROS POR ESPECIFICACAO DA v413 (_v413_rodar_specs), medida por AST sobre o main do candidato (guarda_ordem_de_chamada_v413.ordem_dos_specs_v413): a instrucao e' a SEGUINTE a dos specs da v412
# e IMEDIATAMENTE antes de emit_figures; toda chave do core que as checagens dos specs leem e que o motor le esta pronta ANTES dela; o cunhagens_v413 vem por ultimo; examina TODAS as checagens (zero e' falha visivel).
# Controles negativos: (a) a instrucao movida para antes do run_um; (b) a chamada retirada; (c) trocada de lugar com a dos specs da v412; (d) uma chave sem origem; (f) sem checagem nenhuma.
_specs_ord13 = _GOC.specs_do_programa_v413(src)
_op13 = _GOC.ordem_dos_specs_v413(src, _specs_ord13); _cn13 = _GOC.controle_negativo_specs_v413(src, _specs_ord13)
_ic13 = [i_ for i_, st_ in enumerate(_main0.body) if "_v413_rodar_specs(core)" in ast.unparse(st_)]
_st5 = _main0.body[_ic0 + 5]
_logo13 = bool(len(_ic13) == 1 and _ic13[0] == _ic0 + 4 and isinstance(_st5, ast.Assign) and "emit_figures(core)" in ast.unparse(_st5) and "_v413_rodar_specs(core)" not in (_u0 + _u1 + _u2 + ast.unparse(_st3)))
rep["ordem_de_chamada_specs_v413"] = {"real": {k_: v_ for k_, v_ in _op13.items() if k_ != "chaves_lidas"}, "chaves_lidas": _op13.get("chaves_lidas"), "na_instrucao_seguinte_a_dos_specs_da_v412_e_logo_antes_de_emit_figures": _logo13, "controle_negativo": _cn13, "specs_do_texto_iguais_aos_do_programa_importado": _specs_ord13 == um._V413_SPECS}
U["v413_ordem_de_chamada_dos_cinco_specs_medida_por_ast_depois_dos_specs_da_v412_e_antes_de_emit_figures_com_controles_negativos"] = bool(_op13["ok"] and _op13["n_checagens_examinadas"] == sum(len(s_["checks"]) for s_ in um._V413_SPECS) > 0 and _op13["n_specs"] == len(um._V413_NOMES_REGISTROS) == len(DL.REGISTROS_SPEC_V413)
                                                                                                                                         and _logo13 and _cn13["ok"] and _specs_ord13 == um._V413_SPECS and um._V413_NOMES_REGISTROS[-1] == "cunhagens_v413" and {"qg_closure", "h0dn_bg1_v411", "external_ladder", "kernel_formalization"} <= set(_op13.get("chaves_lidas") or []))
print("ordem de chamada dos specs da v413 (AST propria):", _op13["ok"], "| checagens examinadas:", _op13.get("n_checagens_examinadas"), "| logo depois dos specs da v412, antes de emit_figures:", _logo13, "| controles negativos:", _cn13["ok"])
'''
BLOCO_6S = r'''# (6s) [v413] OS CINCO REGISTROS POR ESPECIFICACAO DA v413 (ponte_cook_levin_v413, trinity_v413, operador_v413, identidade_preservada_v413, cunhagens_v413): so' dados, o motor e' o da v392 (nenhum registro com funcao novo). Tudo certo NO PONTO REAL do main (c[...]),
#      as palavras de veredito do CONTRATO da v413 (lidas pelo delta), os numeros RECALCULADOS aqui por OUTRO caminho (o recibo da escolha das ancoras, o FLAGS_v413.json do kernel, o texto dos modulos embutidos, o relatorio de axiomas do PROPRIO rito, os modulos do manifesto),
#      o modulo corrigido (o hash formal com o texto novo; as mesmas declaracoes), a heranca (gate, neutrino, H0DN e os registros da v412 com o veredito da v412 selada), cada elo recusa visivelmente, a guarda de frases herdada e a historia.
import verificar_historia_texto_v413 as _VH13
import guarda_frases_v413 as _GF13
_N13 = list(um._V413_NOMES_REGISTROS); _SP13 = {s_["nome"]: s_ for s_ in um._V413_SPECS}
assert _N13 == list(DL.REGISTROS_SPEC_V413) == [s_["nome"] for s_ in um._V413_SPECS] and len(set(_N13)) == len(_N13) == 6 and DL.KH_REGISTRO_V413 in _N13   # (contrato R2: os cinco do contrato e o kh_n1_cobertura_v413)
_FJ13 = json.load(open(os.path.join(KD, "FLAGS_v413.json"), encoding="utf-8")); _ANC13 = json.load(open(DL.saida("ANCORAS_ESCOLHIDAS_v413.json"), encoding="utf-8"))
_kf13 = c["kernel_formalization"]; R13 = {n_: (c.get(n_) or {}) for n_ in _N13}
# --- (a) tudo certo no ponto real do main
_tudo13 = {}
for n_ in _N13:
    r_, s_ = R13[n_], _SP13[n_]
    _tudo13[n_] = bool(r_.get("all_verified") is True and r_.get("verdict") == DL.PALAVRAS_DE_VEREDITO[n_] == s_["veredito_prefixo"] + "__" + s_["veredito_sufixo"] and r_["verdict"].endswith("GATE_UNMOVED") and r_.get("does_not_gate_core") is True and not r_.get("guarda_p18_violacoes")
                       and len(r_.get("checks") or []) == len(s_["checks"]) > 0 and all(ck_["ok"] for ck_ in r_["checks"]) and r_["kernel"]["bandeiras"] == [len(s_["kernel_flags"])] * 2 and r_["kernel"]["declaracoes_no_trio"] == [len(s_["kernel_decls"])] * 2
                       and (not s_["fontes"] or (n_ == DL.KH_REGISTRO_V413 and s_["fontes"] == ["kh_n1_v413"])) and not s_["verbatins"] and not s_["leituras_do_operador"] and not s_["erratas"] and "<" not in r_["verdict"])
U["v413_registros_por_spec_tudo_certo_no_ponto_real_com_a_palavra_de_veredito_do_contrato"] = bool(all(_tudo13.values()) and len(_tudo13) == len(_N13))
# --- (b) os numeros RECALCULADOS aqui por outro caminho
_decl2mod13 = {d_: m_ for f_, d_, m_, o_ in _FJ13["flags"]}; _flag2decl13 = {f_: d_ for f_, d_, m_, o_ in _FJ13["flags"]}
_num13 = {}
_N13M = [x_ for x_ in _N13 if x_ in _ANC13["registros"]]   # (os quatro registros com modulo; o kh e o cunhagens nao tem modulo proprio)
for n_ in _N13M:
    s_ = _SP13[n_]; reg_ = _ANC13["registros"][n_]["modulos"]
    fl_ = [a_["bandeira"] for d_ in reg_.values() for a_ in d_["ancoras"]]; dc_ = [a_["nome"] for d_ in reg_.values() for a_ in d_["ancoras"]]
    _num13[n_] = {"n_modulos": len(reg_), "n_ancoras": len(fl_), "modulos_iguais": bool(list(reg_) == list(s_["extras"]["modulos"]) and len(reg_) == s_["extras"]["n_modulos"]),
                  "ancoras_iguais_ao_recibo": bool(s_["kernel_flags"] == fl_ and s_["kernel_decls"] == dc_ and s_["extras"]["n_ancoras"] == len(fl_) == len(dc_))}
_todas13 = [(f_, d_) for n_ in _N13 for f_, d_ in zip(_SP13[n_]["kernel_flags"], _SP13[n_]["kernel_decls"])]
_aponta13 = sum(int(um._LEAN_THEOREM_FLAGS.get(f_) == d_ == _flag2decl13.get(f_)) for f_, d_ in _todas13); _flag_ok13 = sum(int(_kf13.get(f_) is True) for f_, d_ in _todas13)
_no_trio13 = sum(int(d_ in _kf13["axiom_report"] and set(_kf13["axiom_report"][d_] or []) <= _trio12) for f_, d_ in _todas13)
_no_texto13 = sum(int(d_.split(".")[-1] in EMB["TGLExt/" + _decl2mod13[d_].split(".")[-1] + ".lean"]) for f_, d_ in _todas13)
_mods_man13 = sorted(m_.split(".")[-1] for m_ in json.load(open(DL.MANIFESTO_ARQ_PEDRAS, encoding="utf-8"))["modulos_novos"])
_num13["n_ancoras_examinadas"] = len(_todas13)
U["v413_os_numeros_foram_recalculados_aqui_ancoras_modulos_e_declaracoes"] = bool(len(_todas13) > 0 and _aponta13 == _flag_ok13 == _no_trio13 == _no_texto13 == len(_todas13)
                                                                                  and all(v_["modulos_iguais"] and v_["ancoras_iguais_ao_recibo"] for k_, v_ in _num13.items() if isinstance(v_, dict)) and sum(v_["n_ancoras"] for v_ in _num13.values() if isinstance(v_, dict)) == _ANC13["n_ancoras_total"]
                                                                                  and len(_N13M) == 4 and sorted(m_ for n_ in _N13M for m_ in _SP13[n_]["extras"]["modulos"]) == _mods_man13 and len(_mods_man13) == DL.N_BUNDLE == len(DL.BUNDLE_RELS))
# --- (c) a escada so' fecha com as bandeiras novas; nenhuma chave antiga muda de literal; o modulo corrigido (o hash formal com o texto novo; as mesmas declaracoes)
_fl_novas13 = [f_ for f_, d_, m_, o_ in _FJ13["flags"]]
_kf0b13 = core0["kernel_formalization"]; _el13 = c["external_ladder"]
_KC13 = DL.KERNEL_CORRIGIDO; _pre13 = _KC13["modulo"] + "."
_c13 = {"n_flags": bool(len(_fl_novas13) == len(set(_fl_novas13)) == _FJ13["n_flags"] == CM["n_bandeiras"] == DL.N_FLAGS > 0), "todas_true_e_na_tabela": bool(all(_kf13.get(f_) is True and f_ in um._LEAN_THEOREM_FLAGS for f_ in _fl_novas13)), "nenhuma_ja_na_base": not (set(_fl_novas13) & set(_kf0b13)),
        "escada_igual_a_base_mais_as_novas": bool(ESP == CM["escada"][1] == E409 + len(_fl_novas13) == _el13["n_theorems_clean"] == _el13["n_theorems_expected"] and _el13["all_verified"] is True),
        "nenhuma_chave_antiga_muda_de_literal": bool(all(_kf0b13[k_] == _kf13[k_] for k_ in _kf0b13 if isinstance(_kf0b13[k_], bool) and k_.startswith("ext_")) and sum(1 for k_ in _kf0b13 if k_.startswith("ext_")) > 1000),
        "os_modulos_novos_no_hash_formal": bool(set(DL.BUNDLE_RELS) <= set(_kf13["formal_files_sha256"])), "entradas_do_hash_formal": len(_kf13["formal_files_sha256"]) == H8_ENTRADAS,
        "modulo_corrigido_no_hash_formal_com_o_texto_novo": bool(_kf13["formal_files_sha256"].get(_KC13["rel"]) == _KC13["sha256_depois"] == hashlib.sha256(EMB[_KC13["rel"]].encode("utf-8")).hexdigest() != _KC13["sha256_antes"]),
        "modulo_corrigido_mesmas_declaracoes_e_mesmos_axiomas": bool(sorted((k_, tuple(sorted(v_ or []))) for k_, v_ in _kf13["axiom_report"].items() if k_.startswith(_pre13)) == sorted((k_, tuple(sorted(v_ or []))) for k_, v_ in _kf0b13["axiom_report"].items() if k_.startswith(_pre13)) and any(k_.startswith(_pre13) for k_ in _kf13["axiom_report"]))}
U["v413_a_escada_so_fecha_com_as_bandeiras_novas_nenhuma_chave_antiga_muda_e_o_modulo_corrigido_tem_o_texto_novo_e_as_mesmas_declaracoes"] = bool(all(_c13.values()))
# --- (d) a heranca: o gate, o neutrino, o H0DN e os registros da v412 com o veredito da v412 selada
_her13 = {"gate": (c["qg_closure"].get("gate") or {}).get("verdict") == (core0["qg_closure"].get("gate") or {}).get("verdict"), "neutrino": c["neutrino_mass"]["verdict"] == core0["neutrino_mass"]["verdict"], "h0dn": c[DL.FECHO_REGISTRO]["verdict"] == core0[DL.FECHO_REGISTRO]["verdict"] and c[DL.FECHO_REGISTRO]["all_verified"] is True,
          "registros_da_v412_selam_com_o_veredito_da_v412_selada": bool(all((c.get(n_) or {}).get("all_verified") is True and (c.get(n_) or {}).get("verdict") == (core0.get(n_) or {}).get("verdict") for n_ in um._V412_NOMES_REGISTROS)), "qg_closure_verdict_do_selo": bool(selo0.get("qg_closure_verdict"))}
U["v413_heranca_o_gate_o_neutrino_o_h0dn_e_os_registros_da_v412_com_o_veredito_da_v412_selada"] = bool(all(_her13.values()) and (c["qg_closure"].get("gate") or {}).get("verdict"))
# --- (e) cada elo recusa: cada checagem negada, a bandeira e a declaracao faltando, o axioma fora do trio, a frase proibida plantada
_neg13 = {}
for n_ in _N13:
    s_ = _SP13[n_]; ss_ = dict(s_, sem_guarda=True)
    cnt_ = [0, 0]; semop_ = []
    for ck_ in s_["checks"]:
        if ck_["op"] not in _OPNEG12 or ck_["onde"] not in ("core", "kf"):
            semop_.append(ck_["id"]); continue
        r_ = um._v392_registro(ss_, _cow12(c, ck_["onde"], ck_["caminho"], _OPNEG12[ck_["op"]]))
        cnt_[0] += 1; cnt_[1] += int(r_["all_verified"] is False and ("CHECK_" + ck_["id"]) in r_["verdict"])
    ext_ = {"checagens_negadas": cnt_, "checagens_sem_negacao_possivel": semop_}
    if s_["kernel_flags"]:
        r_ = um._v392_registro(ss_, _cow12(c, "kf", [s_["kernel_flags"][0]], False)); ext_["bandeira_faltando_recusa"] = bool(r_["all_verified"] is False and "KERNEL_BANDEIRAS" in r_["verdict"])
        r_ = um._v392_registro(ss_, _cow12(c, "kf", ["axiom_report", s_["kernel_decls"][0]], ["propext", "sorryAx"])); ext_["axioma_fora_do_trio_recusa"] = bool(r_["all_verified"] is False and "KERNEL_DECLARACOES" in r_["verdict"])
        r_ = um._v392_registro(ss_, _cow12(c, "kf", ["axiom_report", s_["kernel_decls"][-1]], _DEL12)); ext_["declaracao_ausente_recusa"] = bool(r_["all_verified"] is False and "KERNEL_DECLARACOES" in r_["verdict"])
    ext_["frases_proibidas_plantadas_recusam"] = []
    for f_ in ("a singularidade converge", "o Nome fixo", "não provou", "singularity converges", "the Name is fixed", "post-diction"):
        r_ = um._v392_registro(dict(s_, diz=list(s_["diz"]) + ["a cadeia: " + f_]), c); ext_["frases_proibidas_plantadas_recusam"].append(bool(r_["all_verified"] is False and "GUARDA_P18" in r_["verdict"] and r_["guarda_p18_violacoes"]))
    ext_["intacto_sela"] = um._v392_registro(s_, c)["all_verified"] is True
    _neg13[n_] = ext_
U["v413_cada_elo_recusa_cada_checagem_negada_a_bandeira_a_declaracao_o_axioma_e_a_frase_plantada"] = bool(all(v_["checagens_negadas"][0] == v_["checagens_negadas"][1] > 0 and v_["intacto_sela"] and all(v_["frases_proibidas_plantadas_recusam"]) and len(v_["frases_proibidas_plantadas_recusam"]) == 6
                                                                                                                  and v_.get("bandeira_faltando_recusa", True) is True and v_.get("axioma_fora_do_trio_recusa", True) is True and v_.get("declaracao_ausente_recusa", True) is True for v_ in _neg13.values())
                                                                                                          and sum(v_["checagens_negadas"][0] for v_ in _neg13.values()) + sum(len(v_["checagens_sem_negacao_possivel"]) for v_ in _neg13.values()) == sum(len(s_["checks"]) for s_ in um._V413_SPECS))
# --- (f) a ligacao: o cunhagens_v413 cobra o selo dos outros quatro; as entradas (leis e definicoes da teoria) so' apontam para o cabecalho
_sp_cn13 = _SP13["cunhagens_v413"]
_selos13 = {ck_["id"]: ck_["caminho"][0] for ck_ in _sp_cn13["checks"] if ck_["id"].startswith("selo_")}
_r_sem13 = {i_: um._v392_registro(dict(_sp_cn13, sem_guarda=True), dict(c, **{r_: dict(c[r_], all_verified=False)})) for i_, r_ in _selos13.items()}
_ent13 = (_sp_cn13.get("extras") or {}).get("entradas") or []
_lig13 = {"cunhagens_cobra_o_selo_dos_outros_quatro": bool(sorted(_selos13.values()) == sorted(n_ for n_ in _N13 if n_ not in ("cunhagens_v413", DL.KH_REGISTRO_V413)) and len(_r_sem13) == len(_selos13) == 4 and all(r_["all_verified"] is False and ("CHECK_" + i_) in r_["verdict"] for i_, r_ in _r_sem13.items())),
          "n_entradas": len(_ent13),
          "entradas_so_apontam_para_o_cabecalho": bool(len(_ent13) == _sp_cn13["extras"]["n_entradas"] > 0 and {e_["modulo"] for e_ in _ent13} <= {m_.split("/")[-1][:-5] for m_ in DL.BUNDLE_RELS} and all(_kf13.get(a_["bandeira"]) is True for e_ in _ent13 for a_ in e_["ancoras"])
                                                       and all(e_["estatuto_de_entrada"] in ("[INPUT]", "[ONTO]", "[INPUT/ONTO]") and e_["ancoras"] and e_["titulo_da_secao_do_cabecalho"] and "nao_tipado" in e_ for e_ in _ent13)
                                                       and all(e_["titulo_da_secao_do_cabecalho"] in EMB["TGLExt/" + e_["modulo"] + ".lean"] for e_ in _ent13))}
U["v413_a_ligacao_cunhagens_cobra_o_selo_dos_outros_quatro_e_as_entradas_apontam_para_o_cabecalho_embutido"] = bool(all(v_ is True for k_, v_ in _lig13.items() if k_ != "n_entradas") and _lig13["n_entradas"] > 0)
# --- (f2) [contrato R2] o kh_n1_cobertura_v413, que a custodia exige: le a cobertura do PROPRIO rito, igual as declaracoes do relatorio de axiomas, nenhuma fora do trio; a fonte pinada e' o recibo KH_N1 (sha256 conferido pelo motor)
_khr13 = c.get(DL.KH_REGISTRO_V413) or {}
_kh_ok13 = {"selou": _khr13.get("all_verified") is True, "veredito_com_none_outside_the_trio": "NONE_OUTSIDE_THE_TRIO" in str(_khr13.get("verdict")),
            "constantes_lidas_iguais_as_declaracoes": (_khr13.get("lido") or {}).get("constantes_cobertas") == len(_kf13["axiom_report"]) == _kf13["axiom_coverage_v392"]["decl"],
            "teoremas_lidos_iguais_aos_do_rito": (_khr13.get("lido") or {}).get("teoremas_cobertos") == _kf13["axiom_coverage_v392"]["thm"],
            "fonte_do_recibo_conferida": bool(_khr13.get("fontes") and all(f_.get("ok") is True for f_ in _khr13["fontes"]) and [f_["chave"] for f_ in _khr13["fontes"]] == ["kh_n1_v413"]),
            "par_fontes_e_verbatins_no_programa": bool(isinstance(getattr(um, "_V413_FONTES", None), dict) and getattr(um, "_V413_VERBATINS2", None) == {} and "kh_n1_v413" in um._V392_FONTES)}
U["v413_kh_n1_cobertura_v413_le_a_cobertura_do_rito_igual_as_declaracoes_nenhuma_fora_do_trio_e_o_par_de_fontes_no_programa"] = bool(all(_kh_ok13.values()))
# --- (g) a guarda de frases HERDADA da v412: as quatro funcoes embutidas no candidato sao as do um.py SELADO da v412 (por trecho); os controles herdados rodam contra as funcoes EMBUTIDAS e dao o mesmo do recibo;
#      o resultado que o rito grava (guarda_frases_v413) e' a travessia refeita aqui e o recibo GUARDA_v413_UNIDADES; zero violacao; zero unidade e' falha; a frase proibida plantada e' recusada
import base_um_v412 as _BU13
_fns13 = ("_v412_guarda_frases", "_v412_unidades_de_texto", "_v412_unidades_tex", "_v412_travessia")
_fonte_igual13 = {f_: bool(_insp12.getsource(getattr(um, f_)).replace("\r\n", "\n").strip() == _BU13.trecho(f_).replace("\r\n", "\n").strip()) for f_ in _fns13}
_ns_antes13 = {k_: _GF13.NS_C[k_] for k_ in ("violacoes", "travessia", "g11", "g12")}
_GF13.NS_C.update({"violacoes": um._v412_guarda_frases, "g12": um._v412_guarda_frases, "travessia": um._v412_travessia, "g11": um._v411_guarda_frases})
try:
    _cc13 = _GF13.controles_herdados(); _cv13 = None
finally:
    _GF13.NS_C.update(_ns_antes13)
_rc13 = json.load(open(DL.saida("GUARDA_FRASES_v413.json"), encoding="utf-8")); _ru13 = json.load(open(DL.saida("GUARDA_v413_UNIDADES.json"), encoding="utf-8"))
_gv13 = c.get("guarda_frases_v413") or {}
_corpo13 = lambda n_: {"corpo": {k_: _SP13[n_].get(k_) for k_ in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, "veredito": _SP13[n_]["veredito_prefixo"] + "__" + _SP13[n_]["veredito_sufixo"]}
_tr13 = {"registro:" + n_: um._v412_travessia("registro:" + n_, _corpo13(n_)) for n_ in _N13}
_tr13.update({"artigo:" + l_: um._v412_travessia("artigo:" + l_, list(um._V413_SECAO[l_]), "tex") for l_ in ("pt", "en")})
_igual_recibo13 = {k_: bool(k_ in _ru13["superficies"] and _ru13["superficies"][k_]["n_unidades"] == t_["n_unidades"] and _ru13["superficies"][k_]["ok"] is True) for k_, t_ in _tr13.items()}
_no_core13 = {n_: bool(_gv13.get(n_, {}).get("n_unidades_examinadas") == _tr13["registro:" + n_]["n_unidades"] > 0 and _gv13[n_].get("n_violacoes") == 0) for n_ in _N13}
_plant13 = {}
for _k13, _t13 in _tr13.items():
    _lg13 = "en" if _k13.endswith(":en") else "pt"
    _f13 = ("A TGL prova P = NP das máquinas de Turing." if _lg13 == "pt" else "The TGL proves P = NP of the Turing machines.", "O prêmio Millennium está resolvido." if _lg13 == "pt" else "The Millennium Prize problem is solved.")
    _plant13[_k13] = [um._v412_travessia("plantada", (list(um._V413_SECAO[_lg13]) + [x_] if _k13.startswith("artigo") else {"corpo": [t_["texto"] for t_ in _t13["unidades"]][:3] + [x_]}), "tex" if _k13.startswith("artigo") else "dados")["ok"] is False for x_ in _f13]
_n_cc13 = len(_cc13); _nok_cc13 = sum(1 for x_ in _cc13 if x_["ok"])
U["v413_a_guarda_de_frases_herdada_e_a_do_um_py_selado_da_v412_controles_herdados_recibo_e_core"] = bool(all(_fonte_igual13.values()) and _n_cc13 == _nok_cc13 == (_rc13.get("controles_herdados") or {}).get("n") == (_rc13.get("controles_herdados") or {}).get("n_ok") > 0
                                                                                                    and all(t_["ok"] and t_["n_unidades"] > 0 and not t_["violacoes"] for t_ in _tr13.values()) and all(_igual_recibo13.values()) and all(_no_core13.values()) and set(_no_core13) == set(_N13)
                                                                                                    and all(all(v_) and len(v_) == 2 for v_ in _plant13.values()) and _ru13.get("ok") is True)
# --- (h) nenhum texto novo traz historia de conversa (o verificador da cadeia, com o autoteste): os cinco registros inteiros e a secao do artigo (PT e EN)
_un13 = []


def _walk13(o_, p_):
    if isinstance(o_, str):
        _un13.append((p_, o_))
    elif isinstance(o_, dict):
        for k_, v_ in o_.items():
            _walk13(v_, p_ + "/" + str(k_))
    elif isinstance(o_, list):
        for i_, v_ in enumerate(o_):
            _walk13(v_, p_ + "[%d]" % i_)


for n_ in _N13:
    _walk13(_SP13[n_], n_)
for l_ in ("pt", "en"):
    _walk13(list(um._V413_SECAO[l_]), "secao_" + l_)
_vh13 = _VH13.examinar(_un13); _vh13a = _VH13.autoteste()
U["v413_nenhum_texto_novo_traz_historia_de_conversa_com_o_autoteste_do_verificador"] = bool(_vh13["ok"] and _vh13["n_unidades_examinadas"] > 500 and _vh13a["ok"] and _vh13a["n"] == _vh13a["n_ok"] > 0)
rep["registros_v413"] = {"tudo_certo": _tudo13, "numeros_recalculados": _num13, "escada_e_modulo_corrigido": _c13, "heranca": _her13, "negativos": _neg13, "ligacao": _lig13, "kh_n1_cobertura_v413": _kh_ok13,
                         "guarda_de_frases": {"funcoes_embutidas_iguais_as_do_um_py_selado_da_v412": _fonte_igual13, "controles_herdados": [_nok_cc13, _n_cc13], "superficies": {k_: [t_["n_unidades"], len(t_["violacoes"])] for k_, t_ in _tr13.items()}, "igual_ao_recibo": _igual_recibo13,
                                              "no_core_do_rito": {n_: [(_gv13.get(n_) or {}).get("n_unidades_examinadas"), (_gv13.get(n_) or {}).get("n_violacoes")] for n_ in _N13}, "plantadas_recusadas": _plant13},
                         "historia_de_conversa": {"identificadores_do_kernel_fora_da_prosa": _vh13["n_identificadores_do_kernel_fora_da_prosa"], "unidades_examinadas": _vh13["n_unidades_examinadas"], "achados": _vh13["n_achados"], "primeiros": _vh13["achados"][:5], "autoteste": [_vh13a["n_ok"], _vh13a["n"]]}}
print("registros da v413:", _tudo13, "| ancoras examinadas:", len(_todas13), "| checagens negadas:", {k_: v_["checagens_negadas"] for k_, v_ in _neg13.items()}, "| modulo corrigido:", {k_: v_ for k_, v_ in _c13.items() if k_.startswith("modulo")}, "| historia:", [_vh13["n_unidades_examinadas"], _vh13["n_achados"]])
'''
CHECA_ARTIGO_13 = r'''def _checagens_v413_do_artigo(tex_, txt_, lang_):
    """(v413) a secao nova do artigo, “O que fica claro na v413”: as linhas de um._v413_secao_tex (que passam pela travessia da guarda herdada antes de sair), em ORDEM e contiguas, ANTES da secao da v412; iguais ao texto publico montado
    pela cadeia (TEXTO_PUBLICO_v413.json); o titulo e as subsecoes numeradas na ordem; a travessia refeita aqui sem violacao; o verificador de historia linha a linha; nenhum simbolo matematico em Unicode cru; o resumo NAO muda (a emissao
    versionada do topo continua a da v412). Cada contagem diz quantas unidades examinou; zero e' falha."""
    sl_ = list(um._v413_secao_tex(lang_)); sec_ = "\n".join(sl_); tp_ = json.load(open(DL.TEXTO_PUBLICO_ARQ, encoding="utf-8")); sl12_ = list(um._v412_secao_tex(lang_))

    def _seq(ls_, ini_=0):
        p0_, p_ = -1, ini_
        for k_, l_ in enumerate(ls_):
            j_ = tex_.find(l_, p_)
            if j_ < 0 or (k_ and tex_[p_:j_].strip()):
                return -1, -1
            p0_ = j_ if k_ == 0 else p0_; p_ = j_ + len(l_)
        return p0_, p_
    i0_, f0_ = _seq(sl_)
    nums_ = [(int(m_.group(1)), l_) for l_ in sl_ for m_ in [re.match(r"\\subsection\*\{(\d+)\. ", l_)] if m_]
    pos_ = [tex_.find(l_) for _, l_ in nums_]
    vh_ = _VH13.examinar([("%s%d" % (lang_, i_), l_) for i_, l_ in enumerate(sl_)])
    trs_ = um._v412_travessia("artigo:" + lang_, sl_, "tex")
    top_ = um._v412_topo_texto(c, lang_)
    out_ = {"secao_contigua_e_em_ordem": i0_ >= 0, "secao_uma_vez_so": tex_.count(sl_[0]) == 1, "secao_antes_da_secao_da_v412": 0 <= i0_ < f0_ <= tex_.find(sl12_[0]),
            "titulo_e_sumario": bool(sl_[0] == "\\section*{" + DL.TITULO_SECAO_V413[lang_] + "}" and ("\\addcontentsline{toc}{section}{" + DL.TITULO_SECAO_V413[lang_] + "}") in sl_),
            "iguais_ao_texto_publico_da_cadeia": tp_["tex"][lang_] == sl_ and tp_["titulo"][lang_] == DL.TITULO_SECAO_V413[lang_], "secoes_numeradas_em_ordem": bool(len(nums_) >= 6 and [n_ for n_, _ in nums_] == list(range(1, len(nums_) + 1)) and pos_ == sorted(pos_) and min(pos_) >= 0),
            "travessia_da_guarda_herdada_sem_violacao": bool(trs_["ok"] and not trs_["violacoes"] and trs_["n_unidades"] >= 20 and len(sl_) >= 20), "sem_historia_de_conversa": bool(vh_["ok"] and vh_["n_unidades_examinadas"] == len(sl_) >= 20),
            "sem_unicode_cru_de_simbolo_matematico": not [ch_ for ch_ in sec_ if 0x370 <= ord(ch_) <= 0x3FF or ch_ in "\u2265\u2264\u221a\u2212\u00bd\u00b2\u00b3"], "sem_n_d": "n/d" not in sec_,
            "o_resumo_nao_muda_a_emissao_do_topo_e_a_da_v412": bool(top_ and top_ in tex_),
            "n_unidades_da_travessia_da_secao": trs_["n_unidades"], "n_linhas_da_secao": len(sl_), "violacoes": [list(v_[:3]) for v_ in trs_["violacoes"][:4]], "achados_de_historia": vh_["achados"][:4]}
    out_["ok"] = bool(all(v_ is True for k_, v_ in out_.items() if k_ not in ("violacoes", "achados_de_historia", "n_unidades_da_travessia_da_secao", "n_linhas_da_secao")) and not trs_["violacoes"] and not vh_["achados"] and out_["n_unidades_da_travessia_da_secao"] > 0)
    return out_


'''
VARIANTE_13 = r'''# (v413) a VARIANTE sem os registros por especificacao da v413: a secao nova do artigo e' texto da teoria (nao le o core) e o artigo imprime, ao vivo, uma linha de veredito por chave do core (v392): o artigo da variante sai IGUAL ao completo,
# menos as linhas do quadro de vereditos dos registros (uma por registro) e a contagem de chaves; a secao nova esta nos dois; nenhuma frase de guarda de «nao selou» aparece
cv13 = dict(copy.deepcopy(c)); [cv13.pop(k, None) for k in V413N]
rep["variante_v413"] = {}
for lang in ("pt", "en"):
    _t13v, _x13v, _r213v, _l13v = compilar(cv13, "dry_v413_var13_%s" % lang, lang, duas=False)
    _tf13 = open(os.path.join(DRY, "dry_v412_%s.tex" % lang), encoding="utf-8").read()
    _linhas13 = [l_ for l_ in _tf13.split("\n") if any(l_.startswith("\\texttt{" + n_.replace("_", "\\_") + "} & ") for n_ in V413N)]
    _A13 = [l_ for l_ in _tf13.split("\n") if l_ not in _linhas13]; _B13 = _t13v.split("\n")
    _dif13 = [i_ for i_ in range(min(len(_A13), len(_B13))) if _A13[i_] != _B13[i_]] if len(_A13) == len(_B13) else None
    _cont13 = [re.findall(r"\d+", _A13[_dif13[0]]), re.findall(r"\d+", _B13[_dif13[0]])] if _dif13 else [[], []]
    _so_num13 = bool(_dif13 is not None and len(_dif13) == 1 and re.sub(r"\d+", "#", _A13[_dif13[0]]) == re.sub(r"\d+", "#", _B13[_dif13[0]]) and any(int(a_) - int(b_) == len(V413R) for a_, b_ in zip(_cont13[0], _cont13[1]) if a_ != b_))
    rep["variante_v413"][lang] = {"rc": _r213v, "n_registros_retirados": sum(1 for k_ in V413R if k_ in c and k_ not in cv13), "secao_nova_na_variante": bool(um._v413_secao_tex(lang)[0] in _t13v and um._v413_secao_tex(lang)[0] in _tf13), "n_linhas_do_quadro_de_vereditos_retiradas": len(_linhas13),
                                  "igual_ao_completo_menos_as_linhas_dos_registros_e_a_contagem": _so_num13, "n_linhas_diferentes_alem_das_dos_registros": (len(_dif13) if _dif13 is not None else None), "contagem_de_chaves_completo_variante": [_cont13[0][:1], _cont13[1][:1]] if _dif13 else None,
                                  "sem_frase_de_guarda_de_nao_selou_na_variante": ("NÃO selou" not in re.sub(r"\s+", " ", _x13v)) if lang == "pt" else ("did NOT seal" not in re.sub(r"\s+", " ", _x13v))}
mau_var13 = [l for l, v in rep["variante_v413"].items() if v["rc"] != [0] or v["n_registros_retirados"] != len(V413R) or v["n_linhas_do_quadro_de_vereditos_retiradas"] != len(V413R) or not v["secao_nova_na_variante"] or not v["igual_ao_completo_menos_as_linhas_dos_registros_e_a_contagem"] or not v["sem_frase_de_guarda_de_nao_selou_na_variante"]]
print("variante v413:", rep["variante_v413"])
'''
QV_IMPORT = ('import importlib.util as _ilu0; sys.path.append(DL.V412); _spq0 = _ilu0.spec_from_file_location("quadro_v397_r7", os.path.join(DL.V412, "quadro_v397_r7.py")); QV = _ilu0.module_from_spec(_spq0); '
             '_spq0.loader.exec_module(QV); sys.path.remove(DL.V412)  # noqa: E402   (v413: o quadro da v397 da cadeia da v412, por caminho)')
derivar("ensaio_a_seco_v412_r7.py", "ensaio_a_seco_v413.py", trocas=[
    ("import delta_v412_r7 as DL  # noqa: E402", "import delta_v413 as DL  # noqa: E402", 1),
    ('sys.modules.setdefault("delta_v411", DL.D11);', 'sys.modules.setdefault("delta_v412_r7", DL.D12); sys.modules.setdefault("delta_v412", DL.D12); sys.modules.setdefault("delta_v411", DL.D11);', 1),
    ("import quadro_v397_r7 as QV  # noqa: E402", QV_IMPORT, 1),
    ('rot = sys.argv[2] if len(sys.argv) > 2 else "v412"', 'rot = sys.argv[2] if len(sys.argv) > 2 else "v413"', 1),
    ('DRY = DL.DRY_DIR if rot == "v412" else', 'DRY = DL.DRY_DIR if rot == "v413" else', 1),
    ('CM = json.load(open(DL.MANIFESTO_ARQ if rot == "v412" else os.environ["V412_ENSAIO_MANIFESTO_DIAGNOSTICO"]', 'CM = json.load(open(DL.MANIFESTO_ARQ if rot == "v413" else os.environ["V413_ENSAIO_MANIFESTO_DIAGNOSTICO"]', 1),
    ('assert _CM11["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v411.json nao e\' o da v411 selada", _CM11["sha16"])',
     'assert _CM11["sha16"] == DL.D12.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v411.json nao e\' o da v411 selada", _CM11["sha16"])\n'
     '_CM12 = json.load(open(os.path.join(DL.V412, "CANDIDATO_v412.json"), encoding="utf-8"))   # (v413) o candidato da v412 SELADA: os numeros dos blocos HERDADOS da v412 saem dele e do DL.D12, nunca do DL da v413\n'
     'assert _CM12["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v412.json nao e\' o da v412 selada", _CM12["sha16"])', 1),
    ('assert um.UM_VERSION == "v412"', 'assert um.UM_VERSION == "v413"', 1),
    ('and selo0["um_version"] == "v411"', 'and selo0["um_version"] == "v412"', 1),
    ('if "v412" in l or "v411" in l or "v393" in l', 'if "v413" in l or "v412" in l or "v411" in l or "v393" in l', 1),
    # (v413) a escada dos blocos HERDADOS da v410 (iald2_v410 e a_escala_v410), recomposta desde a v410: no molde, a soma era a escada da v410 mais as bandeiras da versao corrente, porque a v411 nao acrescentou bandeira;
    # na v413 entram as parcelas das versoes intermediarias (a v411, zero, e a v412), lidas dos manifestos selados (_CM11, _CM12), nunca digitadas. A igualdade cobrada e' a mesma.
    ('_CM10["escada"][1] + CM["n_bandeiras"]', '_CM10["escada"][1] + _CM11["n_bandeiras"] + _CM12["n_bandeiras"] + CM["n_bandeiras"]', 2),
    ('+ list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS)   # (v412: e os da v411, HERANCA', '+ list(um._V411_REGISTROS_FUNCAO) + list(um._V411_NOMES_REGISTROS) + list(um._V412_NOMES_REGISTROS)   # (v413: e os da v412, HERANCA: recriados e comparados com os da v412 selada) (v412: e os da v411, HERANCA', 1),
    ('V412R = list(um._V412_NOMES_REGISTROS); V412N = V412R + ["guarda_frases_v412"]', 'V412R = list(um._V412_NOMES_REGISTROS); V412N = V412R + ["guarda_frases_v412"]; V413R = list(um._V413_NOMES_REGISTROS); V413N = V413R + ["guarda_frases_v413"]', 1),
    ('for _k in V393N + V394N + V395N + V396N + V397N + V398N + V409N + V412N:', 'for _k in V393N + V394N + V395N + V396N + V397N + V398N + V409N + ["guarda_frases_v412"] + V413N:', 1),
    ('NOVAS412 = sorted(V412N)', 'NOVAS412 = sorted(V413N)', 1),
    ('"registros_novos_v412": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V412R},', '"registros_novos_v413": {n_: {"all_verified": (c.get(n_) or {}).get("all_verified"), "verdict": (c.get(n_) or {}).get("verdict")} for n_ in V413R},', 1),
    ('+ V409N + V412R)', '+ V409N + V413R)', 1),
    ('import guarda_ordem_de_chamada_v412_r7 as _GOC', 'import guarda_ordem_de_chamada_v413 as _GOC', 1),
    ('_logo12 = bool(len(_ic12) == 1 and _ic12[0] == _ic0 + 3 and isinstance(_st4, ast.Assign) and "emit_figures(core)" in ast.unparse(_st4) and "_v412_rodar_specs(core)" not in (_u0 + _u1 + _u2))',
     '_logo12 = bool(len(_ic12) == 1 and _ic12[0] == _ic0 + 3 and "_v413_rodar_specs(core)" in ast.unparse(_st4) and "_v412_rodar_specs(core)" not in (_u0 + _u1 + _u2))   # (v413) a instrucao seguinte e\' a dos specs da v413; o emit_figures vem depois dela (bloco 5b-v413)', 1),
    ('import acom_conferencias_v412 as AC  # noqa: E402', 'import acom_conferencias_v413 as AC  # noqa: E402', 1),
    ('"um_version", "sha256", "registros_v412") and not _selo_explica(k_))', '"um_version", "sha256", "registros_v413") and not _selo_explica(k_))', 1),
    ('(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v412"}) <= set(mud_selo)', '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v413"}) <= set(mud_selo)', 1),
    ('"registros_v409", "registros_v410", "registros_v411"} & set(mud_selo))', '"registros_v409", "registros_v410", "registros_v411", "registros_v412"} & set(mud_selo))', 1),
    ('and len(seal.get("registros_v412") or {}) == len(um._V412_NOMES_REGISTROS))', 'and len(seal.get("registros_v412") or {}) == len(um._V412_NOMES_REGISTROS) and all(((seal.get("registros_v413") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V413_NOMES_REGISTROS) and len(seal.get("registros_v413") or {}) == len(um._V413_NOMES_REGISTROS))', 1),
    ('DL.TOPO_RATIFICADO_ARQ = os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")', 'DL.TOPO_RATIFICADO_ARQ = os.path.join(DL.V412, "TOPO_RATIFICADO_v412_DERIVADO.json")', 1),
    ('import topo_com_resultado_v412_r7 as _TR11  # noqa: E402', '_TR11 = _mod412("topo_com_resultado_v412_r7")  # noqa: E402', 1),
    ('os.path.join(KD, "KH_N1_v412.json")', 'os.path.join(KD, "KH_N1_v413.json")', 1),
    ('TOC = {"pt": [DL.TITULO_SECAO_V412["pt"],', 'TOC = {"pt": [DL.TITULO_SECAO_V413["pt"], DL.TITULO_SECAO_V412["pt"],', 1),
    ('"en": [DL.TITULO_SECAO_V412["en"],', '"en": [DL.TITULO_SECAO_V413["en"], DL.TITULO_SECAO_V412["en"],', 1),
    ('"v384 a v412"]', '"v384 a v413"]', 1),
    ('"v384 to v412"]}', '"v384 to v413"]}', 1),
    ('DEVE["pt"] += _H12["pt"]; DEVE["en"] += _H12["en"]', 'DEVE["pt"] += _H12["pt"]; DEVE["en"] += _H12["en"]\n_H13 = {l_: re.findall(r"\\\\(?:sub)?section\\*\\{([^{}]*)\\}", "\\n".join(um._V413_SECAO[l_])) for l_ in ("pt", "en")}   # (v413) os titulos da secao nova da v413\nDEVE["pt"] += _H13["pt"]; DEVE["en"] += _H13["en"]', 1),
    ('    rep["artigo"][lang]["v412"] = _checagens_v412_do_artigo(tex, txt, lang)', '    rep["artigo"][lang]["v412"] = _checagens_v412_do_artigo(tex, txt, lang)\n    rep["artigo"][lang]["v413"] = _checagens_v413_do_artigo(tex, txt, lang)   # (v413) a secao nova; o resumo nao muda', 1),
    ('or not v["v411"]["ok"] or not v["v412"]["ok"]]', 'or not v["v411"]["ok"] or not v["v412"]["ok"] or not v["v413"]["ok"]]', 1),
    ('"carimbo": "**Versão v412**" in md', '"carimbo": "**Versão v413**" in md', 1),
    ('rep["manifest"] = "**Versão v412**" in open(mani', 'rep["manifest"] = "**Versão v413**" in open(mani', 1),
    ('import guarda_conversa_v412_r7 as _GC11   # noqa: E402', 'import guarda_conversa_v413 as _GC11   # noqa: E402', 1),
    ('os.path.join(HERE, "conferir_citacoes_v412_r7.py")', 'os.path.join(HERE, "conferir_citacoes_v413.py")', 1),
    ('DL.saida("conferir_citacoes_v412.json")', 'DL.saida("conferir_citacoes_v413.json")', 1),
    ('os.path.join(HERE, "simular_arvore_do_nos_v412_r7.py")', 'os.path.join(HERE, "simular_arvore_do_nos_v413.py")', 1),
    ('_regs_sim = tuple(um._V412_NOMES_REGISTROS) +', '_regs_sim = tuple(um._V413_NOMES_REGISTROS) + tuple(um._V412_NOMES_REGISTROS) +', 1),
    ('"formal_map_v412": _sj.get("formal_map_v412")', '"formal_map_v413": _sj.get("formal_map_v413")', 1),
    ('(_sj.get("formal_map_v412") or {}).get("ok")', '(_sj.get("formal_map_v413") or {}).get("ok")', 1),
    ('os.path.join(HERE, "exame_pontos_v412_r7.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v412.json")', 'os.path.join(HERE, "exame_pontos_v413.py"), "--candidato", _cand_p, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v413.json")', 1),
    ('_gb_p = DL.saida("GUARDAS_ESTATICAS_BANCADA_v412.json")', '_gb_p = DL.saida("GUARDAS_ESTATICAS_BANCADA_v413.json")', 1),
    ('os.path.join(HERE, "guardas_estaticas_bancada_v412_r7.py")', 'os.path.join(HERE, "guardas_estaticas_bancada_v413.py")', 1),
    ('and not mau_var12 and', 'and not mau_var12 and not mau_var13 and', 1),
    ('rep["mainflow"]["chaves_novas"] == sorted(V412N))', 'rep["mainflow"]["chaves_novas"] == sorted(V413N))', 1),
    ('"variante_v412": mau_var12,', '"variante_v412": mau_var12, "variante_v413": mau_var13,', 1),
    ('_pE = DL.saida("ensaio_a_seco_v412.json") if rot == "v412" else os.path.join(DL.RODADA_PAI, "diag", "ensaio_a_seco_v412_%s.json" % rot)', '_pE = DL.saida("ensaio_a_seco_v413.json") if rot == "v413" else os.path.join(DL.RODADA_PAI, "diag", "ensaio_a_seco_v413_%s.json" % rot)', 1),
], regioes=[
    ("# (6r) [v412, contrato R11] OS CINCO REGISTROS POR ESPECIFICACAO", "# (8) o artigo", [
        ("import verificar_historia_texto_v412_r7 as _VH12", '_VH12 = _mod412("verificar_historia_texto_v412_r7")', 1),
        ("import guarda_frases_v412_r7 as _GF12c", '_GF12c = _mod412("guarda_frases_v412_r7")', 1),
        ('os.path.join(KD, "FLAGS_v412.json")', 'os.path.join(DL.V412, "kernel", "FLAGS_v412.json")', 1),
        ('os.path.join(HERE, "', 'os.path.join(DL.V412, "', None),
        ("DL.PALAVRAS_DE_VEREDITO", "DL.D12.PALAVRAS_DE_VEREDITO", None),
        ("DL._CONTRATO_TXT", "DL.D12._CONTRATO_TXT", None),
        ("DL.MANIFESTO_ARQ_PEDRAS", "DL.D12.MANIFESTO_ARQ_PEDRAS", None),
        ("DL.N_BUNDLE", "DL.D12.N_BUNDLE", None),
        ("DL.BUNDLE_RELS", "DL.D12.BUNDLE_RELS", None),
        ("DL.N_MODULOS_DO_MANIFESTO", "DL.D12.N_MODULOS_DO_MANIFESTO", None),
        ('CM["n_bandeiras"] == DL.N_FLAGS > 0)', '_CM12["n_bandeiras"] == DL.D12.N_FLAGS > 0)', 1),
        ('"nenhuma_ja_na_base": not (set(_fl_novas12) & set(_kf0b12)),', '"todas_ja_na_base_selada_da_v412": bool(set(_fl_novas12) <= set(_kf0b12)),', 1),
        ('"escada_igual_a_base_mais_as_novas": bool(ESP == CM["escada"][1] == E409 + len(_fl_novas12) == _el12["n_theorems_clean"] == _el12["n_theorems_expected"] and _el12["all_verified"] is True),',
         '"escada_da_v412_selada_e_a_base_desta": bool(_CM12["escada"][1] == E409 and ESP == CM["escada"][1] == _el12["n_theorems_clean"] == _el12["n_theorems_expected"] and _el12["all_verified"] is True),', 1),
        ('CM["resumo_troca_de_pnp"]', '_CM12["resumo_troca_de_pnp"]', 1),
    ]),
    ("def _checagens_v412_do_artigo(tex_, txt_, lang_):", "def compilar(cv, nome, lang, duas=True):", [
        ("open(DL.TEXTO_PUBLICO_ARQ, encoding=\"utf-8\")", 'open(os.path.join(DL.V412, "TEXTO_PUBLICO_v412.json"), encoding="utf-8")', 1),
        ('os.path.join(HERE, "TOPO_RATIFICADO_v412_DERIVADO.json")', 'os.path.join(DL.V412, "TOPO_RATIFICADO_v412_DERIVADO.json")', 1),
        ('CM["resumo_troca_de_pnp"]', '_CM12["resumo_troca_de_pnp"]', None),
    ]),
    ("# (13) [v410, LICAO NOVA] as guardas ESTATICAS", "# (0, no fim) [AVISO 09/11]", [
        ('candidato_v412', 'candidato_v413', None),
    ]),
], insercoes=[
    ('_GF11 = _mod411("guarda_frases_v411")', MOD412, "antes"),
    ('print("ordem de chamada dos specs da v412 (AST propria):"', ORDEM13, "depois_da_linha"),
    ("# (8) o artigo", BLOCO_6S, "antes"),
    ("def compilar(cv, nome, lang, duas=True):", CHECA_ARTIGO_13, "antes"),
    ("# (9) md e manifesto", VARIANTE_13, "antes"),
])
print("derivacao do ensaio e dos auxiliares: feita")

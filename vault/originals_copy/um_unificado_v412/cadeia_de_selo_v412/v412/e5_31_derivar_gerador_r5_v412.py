"""R5: deriva as copias _r5 do delta, do codigo de runtime e do gerador do candidato (os originais ficam intactos): 153 modulos, cinco registros, a pagina R18, o contrato R5, o prefixo das bandeiras com o nome do modulo como ele e'
(dois modulos tem sublinhado no nome), e a guarda do candidato anterior fora de work\\ antes de regerar."""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from e5_deriv_v412 import derivar
EU = "e5_31_derivar_gerador_r5_v412.py"

derivar("delta_v412.py", "delta_v412_r5.py", [
    ('"""delta_v412.py -- a UNICA definicao do DELTA da v412 (os 42 modulos novos de TGLExt/, a escada, os quatro registros por especificacao,', '"""delta_v412_r5.py -- a UNICA definicao do DELTA da v412 pelo contrato R5 (os 153 modulos novos de TGLExt/, a escada, os cinco registros por especificacao,', 1),
    ('CONTRATO_ARQ = os.path.join(HERE, "CONTRATO_v412_R4.md")', 'CONTRATO_ARQ = os.path.join(HERE, "CONTRATO_v412_R5.md")', 1),
    ('== len(BUNDLE_POR_REL) == 42 and set(BUNDLE_POR_REL)', '== len(BUNDLE_POR_REL) == N_MODULOS_DO_MANIFESTO == 153 and set(BUNDLE_POR_REL)', 1),
    ('"o bundle da v412 e\' de quarenta modulos, na ordem topologica"', '"o bundle da v412 e\' o dos modulos do manifesto vigente (153), na ordem topologica"', 1),
    ('BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}\n',
     'BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}\nMANIFESTO_ARQ_PEDRAS = os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R10.json")\n_m_man = re.search(r"insumos\\\\MANIFESTO_PEDRAS_v412_R10\\.json` \\(sha16 `([0-9a-f]{16})`\\)", _CONTRATO_TXT)\n'
     'assert _m_man and hashlib.sha256(open(MANIFESTO_ARQ_PEDRAS, "rb").read()).hexdigest()[:16] == _m_man.group(1), "o manifesto de pedras nao e\' o do contrato R5"\n'
     'assert _BD["manifesto_sha256"] == hashlib.sha256(open(MANIFESTO_ARQ_PEDRAS, "rb").read()).hexdigest(), "o bundle nao foi preparado com o manifesto do contrato R5"\n'
     'N_MODULOS_DO_MANIFESTO = int(json.load(open(MANIFESTO_ARQ_PEDRAS, encoding="utf-8"))["n_modulos"])\n', 1),
    ('REGISTROS_SPEC_V412 = ["iald_camada_cientifica_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]',
     'REGISTROS_SPEC_V412 = ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]', 1),
    ('    _m = re.search(r"^- `%s`\\n  `([A-Z0-9_]+)`" % _n, _CONTRATO_TXT, re.M)\n    assert _m, ("palavra de veredito nao achada no contrato", _n)\n    PALAVRAS_DE_VEREDITO[_n] = _m.group(1)',
     '    _ms = re.findall(r"^- `%s`\\n  `([A-Z0-9_]+)`" % _n, _CONTRATO_TXT, re.M)\n    assert len(_ms) == 1, ("palavra de veredito nao achada (ou repetida) no contrato", _n, len(_ms))\n    PALAVRAS_DE_VEREDITO[_n] = _ms[0]', 1),
    ('_m = re.search(r"o_que_fica_claro_REV13\\\\O_QUE_FICA_CLARO_v412_R13\\.md` \\(sha16 `([0-9a-f]{16})`; (\\d+) bytes\\)", _CONTRATO_TXT)', '_m = re.search(r"o_que_fica_claro_REV18\\\\O_QUE_FICA_CLARO_v412_R18\\.md` \\(sha16 `([0-9a-f]{16})`; (\\d+) bytes\\)", _CONTRATO_TXT)', 1),
    ('assert _m, "o contrato nao pina a pagina R13"', 'assert _m, "o contrato nao pina a pagina R18"', 1),
    ('PAGINA_ARQ = os.path.join(HERE, "o_que_fica_claro_REV13", "O_QUE_FICA_CLARO_v412_R13.md")', 'PAGINA_ARQ = os.path.join(HERE, "o_que_fica_claro_REV18", "O_QUE_FICA_CLARO_v412_R18.md")', 1),
    ('"a pagina R13 nao e\' a do contrato"', '"a pagina R18 nao e\' a do contrato"', 1),
    ('PAGINA_EN_ARQ = os.path.join(HERE, "O_QUE_FICA_CLARO_v412_R13_EN.md")', 'PAGINA_EN_ARQ = os.path.join(HERE, "O_QUE_FICA_CLARO_v412_R18_EN.md")', 1),
], EU, imports=False)

derivar("runtime_v412_codigo.py", "runtime_v412_codigo_r5.py", [
    ('"""v412 -- roda os quatro registros por especificacao da v412', '"""v412 -- roda os cinco registros por especificacao da v412', 1),
    ("(cunhagens_v412 por ultimo: cobra o selo dos outros tres)", "(cunhagens_v412 por ultimo: cobra o selo dos outros quatro)", 1),
], EU, imports=False)

GUARDA_ANTERIOR = '''if os.path.exists(out) and open(out, "rb").read() != b:   # (r5) o candidato anterior e os tres artefatos dele vao para FORA de work\\\\, conferidos por bytes; nenhum .bak de candidato fica na pasta da cadeia
    _velho = open(out, "rb").read(); _dg = os.path.join(DL.SANDBOX_PAI, "candidatos_anteriores", "um_v412_candidato_" + sha16(_velho)); os.makedirs(_dg, exist_ok=True)
    for _p in (out, DL.MANIFESTO_ARQ, DL.FORMAL_MAP_ARQ, DL.PINS_ARQ):
        if os.path.exists(_p):
            _d = os.path.join(_dg, os.path.basename(_p))
            if not (os.path.exists(_d) and open(_d, "rb").read() == open(_p, "rb").read()):
                shutil.copyfile(_p, _d + ".tmp"); os.replace(_d + ".tmp", _d)
            assert open(_d, "rb").read() == open(_p, "rb").read(), ("a guarda do candidato anterior nao e' copia de bytes", _d)
    print("candidato anterior guardado fora de work:", _dg)
'''
derivar("gerar_candidato_v412.py", "gerar_candidato_v412_r5.py", [
    ('"""gerar_candidato_v412.py -- gera o um.py CANDIDATO da v412', '"""gerar_candidato_v412_r5.py -- (contrato R5) gera o um.py CANDIDATO da v412', 1),
    ("Conteudo (CONTRATO_v412_R4; nenhum texto daqui entra no programa com historia de conversa):", "Conteudo (CONTRATO_v412_R5; nenhum texto daqui entra no programa com historia de conversa):", 1),
    (" (A) kernel: 42 modulos novos em TGLExt/ embutidos", " (A) kernel: 153 modulos novos em TGLExt/ embutidos", 1),
    ("assert nov == DL.BUNDLE_RELS and len(nov) == 42", "assert nov == DL.BUNDLE_RELS and len(nov) == DL.N_MODULOS_DO_MANIFESTO == 153", 1),
    # as bandeiras: o prefixo do contrato e' ext_<modulo>_412_NNNN, com o nome do modulo em minusculas COMO ELE E' (dois modulos tem sublinhado no nome)
    ('assert not any(re.search(r"\\d{8}|20\\d\\d|v4\\d\\d_|ordem|parecer|gerencia|operador|autor", k.replace("_412_", "_")) for k, _, _ in FL if not re.fullmatch(r"ext_[a-z0-9]+_412_\\d{4}", k)), "nome de bandeira com historia"',
     '_RX_HIST_FLAG = re.compile(r"\\d{8}|20\\d\\d|v4\\d\\d_|ordem|parecer|revisao|gerencia|operador|autor|codex|kimi|claude|chatgpt")\n'
     '_flags_hist = sorted({k.rsplit("_412_", 1)[0] for k, _, _ in FL if _RX_HIST_FLAG.search(k.rsplit("_412_", 1)[0])})\n'
     'assert not _flags_hist, ("nome de bandeira com data, nome de pessoa ou de modelo, ou palavra de processo (examinadas %d chaves)" % len(FL), _flags_hist)', 1),
    ('assert all(re.fullmatch(r"ext_[a-z0-9]+_412_\\d{4}", k) for k, _, _ in FL), "nome de bandeira fora do prefixo do contrato"',
     'assert all(re.fullmatch(r"ext_[a-z0-9_]+_412_\\d{4}", k) and k.rsplit("_412_", 1)[0] == "ext_" + m.split(".")[-1].lower() for k, _, m in FL) and len(FL) > 0, "nome de bandeira fora do prefixo do contrato (ext_<modulo em minusculas>_412_NNNN)"', 1),
    ('"    # v412: os 40 modulos de TGLExt/ do bundle (series ext_<modulo>_412_*): %d bandeiras, so\' de declaracao NOMEADA (as auxiliares geradas pelo compilador ficam fora)" % len(FL) + CRLF',
     '"    # v412: os %d modulos de TGLExt/ do bundle (series ext_<modulo>_412_*): %d bandeiras, so\' de declaracao NOMEADA (as auxiliares geradas pelo compilador ficam fora)" % (N_NOVOS, len(FL)) + CRLF', 1),
    ('"        # v412: os 40 modulos do bundle (%d, so\' declaracao nomeada)" % len(FL) + CRLF', '"        # v412: os %d modulos do bundle (%d, so\' declaracao nomeada)" % (N_NOVOS, len(FL)) + CRLF', 1),
    ("-- %d modulos novos de TGLExt/ (a camada cientifica e a matematica que restava; %d bandeiras so\\' de declaracao nomeada; a escada %d -> %d), '",
     "-- %d modulos novos de TGLExt/ (a camada cientifica, o leitor da formula e a matematica que restava; %d bandeiras so\\' de declaracao nomeada; a escada %d -> %d), '", 1),
    ("'quatro registros por especificacao (%s), a guarda de frases da v412,", "'cinco registros por especificacao (%s), a guarda de frases da v412,", 1),
    ('HDR = ("# ====================== v412 -- a camada cientifica e a matematica que restava: %d modulos novos de TGLExt/ (%d bandeiras, a escada %d -> %d), a guarda de frases da v412, a secao “%s” do artigo e quatro registros por especificacao "',
     'HDR = ("# ====================== v412 -- a camada cientifica, o leitor da formula e a matematica que restava: %d modulos novos de TGLExt/ (%d bandeiras, a escada %d -> %d), a guarda de frases da v412, a secao “%s” do artigo e cinco registros por especificacao "', 1),
    ('"bloco v412: a guarda de frases, a secao do artigo, os quatro registros por especificacao."', '"bloco v412: a guarda de frases, a secao do artigo, os cinco registros por especificacao."', 1),
    ("    try:   # v412: os quatro registros por especificacao (a camada cientifica, a matematica que restava, a parede do teste cego e as definicoes da teoria); excecao vira AVISO visivel, nunca derruba o rito",
     "    try:   # v412: os cinco registros por especificacao (a camada cientifica, o leitor da formula, a matematica que restava, a parede do teste cego e as definicoes da teoria); excecao vira AVISO visivel, nunca derruba o rito", 1),
    ('assert TP["fonte_pt"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_ARQ) and TP["fonte_en"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_EN_ARQ), "TEXTO_PUBLICO_v412.json nao e\' da pagina/traducao atuais: rode e2_21"',
     'assert TP["fonte_pt"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_ARQ) and TP["fonte_en"]["sha16"] == DL.sha16_arquivo(DL.PAGINA_EN_ARQ), "TEXTO_PUBLICO_v412.json nao e\' da pagina/traducao atuais: rode e5_23"', 1),
    ('if os.path.exists(out) and open(out, "rb").read() != b:\n    shutil.copyfile(out, out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))\n', GUARDA_ANTERIOR, 1),
    ('man = {("artefato_de_ensaio" if False else "candidato"): DL.CANDIDATO_ARQ,', 'man = {("artefato_de_ensaio" if False else "candidato"): DL.CANDIDATO_ARQ, "contrato": {"arquivo": os.path.basename(DL.CONTRATO_ARQ), "sha16": DL.CONTRATO_SHA16}, "gerador": os.path.basename(__file__),', 1),
], EU)

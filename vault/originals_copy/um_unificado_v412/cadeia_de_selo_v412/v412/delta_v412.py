# -*- coding: utf-8 -*-
"""delta_v412.py -- a UNICA definicao do DELTA da v412 (os 42 modulos novos de TGLExt/, a escada, os quatro registros por especificacao, o paragrafo vigente de P = nP no resumo e a secao
nova do artigo). No molde do delta_v411: importa o delta_v411 por caminho (e, por ele, os anteriores) e SOBRESCREVE o que a v412 muda. As constantes do kernel (a lista de modulos, o sufixo da raiz, as bandeiras) sao
LIDAS dos arquivos que o preparo escreveu (BUNDLE_v412.json, kernel_modulos_novos_v412.json, kernel\\FLAGS_v412.json), nunca digitadas; a base e' a v411 selada, lida do contrato. Validade no kernel nao e' creditacao; o gate nao se move.
Nada neste arquivo traz historia de conversa para o programa; os nomes V412 de atributos existem so' para os scripts da cadeia."""
import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V411 = os.path.join(os.path.dirname(HERE), "v411")
_spec = importlib.util.spec_from_file_location("delta_v411_carregado_pelo_v412", os.path.join(V411, "delta_v411.py"))
_MOD11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_MOD11)
globals().update({k: v for k, v in vars(_MOD11).items() if not k.startswith("__")})
D11 = _MOD11
D10 = D11.D10
D9 = D11.D9
D8 = D11.D8
HERE = os.path.dirname(os.path.abspath(__file__))               # (o update acima trouxe o HERE da v411: aqui e' a pasta da v412)
V411 = os.path.join(os.path.dirname(HERE), "v411")
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))
CENTRAL = os.path.dirname(WK)
UM_VERSION = "v412"
BASE_VERSION = "v411"
SANDBOX_PAI = os.path.join(C, "t", "k412c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")
ARVORE = os.path.join(SANDBOX_PAI, "arvore")
SANDBOX_ORIGEM = os.path.join(C, "t", "k411c", "final")
KERNEL_DIR = "kernel"
CANDIDATO = "um_v412_candidato.py"
BASE_DIR = "base_v411"
CONTRATO_ARQ = os.path.join(HERE, "CONTRATO_v412_R4.md")
DESENHO_ARQ = CONTRATO_ARQ                                      # (o contrato congelado e' a regua da versao)
_CONTRATO_RAW = open(CONTRATO_ARQ, "rb").read()
CONTRATO_SHA16 = hashlib.sha256(_CONTRATO_RAW).hexdigest()[:16]
DESENHO_SHA16 = CONTRATO_SHA16
_CONTRATO_TXT = _CONTRATO_RAW.decode("utf-8").replace("\r\n", "\n")
_m_base = re.search(r"Base: a v411 selada \(`um\.py` do N[oó]s, sha16 `([0-9a-f]{16})`", _CONTRATO_TXT)
assert _m_base, "o contrato da v412 nao traz a base"
BASE_SHA16_DA_ORDEM = _m_base.group(1)
SANDBOX_CURTO = os.path.join(C, "t", "vb22")

# ---------------------------------------------------------------- o BUNDLE (40 modulos), LIDO dos arquivos do preparo
BUNDLE_LISTA_ARQ = os.path.join(HERE, "kernel_modulos_novos_v412.json")
BUNDLE_ARQ = os.path.join(HERE, "BUNDLE_v412.json")
_BL = json.load(open(BUNDLE_LISTA_ARQ, encoding="utf-8"))
_BD = json.load(open(BUNDLE_ARQ, encoding="utf-8"))
BUNDLE_RELS = list(_BL["novos"])
BUNDLE_MODS = [p[:-len(".lean")].replace("/", ".") for p in BUNDLE_RELS]
N_BUNDLE = len(BUNDLE_RELS)
BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}
assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 42 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS) and [b["rel"] for b in _BD["modulos"]] == BUNDLE_RELS, "o bundle da v412 e' de quarenta modulos, na ordem topologica"
ROOT_SUFFIX = _BD["root_suffix"]
assert ROOT_SUFFIX == "".join("import %s\n" % m for m in BUNDLE_MODS) == _BL["root_suffix"], "o sufixo da raiz nao e' o das importacoes do bundle"
AUDIT_PREFIX = ""
BUNDLE_DA_BANCADA = []
BUNDLE_DA_GERENCIA = list(BUNDLE_RELS)
_FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v412.json"), encoding="utf-8"))
FLAG_PREFIX_POR_MODULO = {m.replace(".", "/") + ".lean": p for m, p in _FJ["prefixos"].items()}
assert set(FLAG_PREFIX_POR_MODULO) == set(BUNDLE_RELS)
ESCADA_BASE = int(_FJ["escada"][0])
ESCADA_NOVA = int(_FJ["escada"][1])
N_FLAGS = int(_FJ["n_flags"])
assert ESCADA_NOVA == ESCADA_BASE + N_FLAGS

# ---------------------------------------------------------------- os quatro registros por especificacao (nomes e palavras de veredito LIDOS do contrato)
REGISTROS_SPEC_V412 = ["iald_camada_cientifica_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]
REGISTROS_FUNCAO = []                                            # a v412 nao tem registro com funcao novo
REGISTROS_FUNCAO_V411 = list(D11.REGISTROS_FUNCAO)               # h0dn_bg1_v411: herdado, selado
REGISTROS_FUNCAO_V412 = []
PALAVRAS_DE_VEREDITO = {}
for _n in REGISTROS_SPEC_V412:
    _m = re.search(r"^- `%s`\n  `([A-Z0-9_]+)`" % _n, _CONTRATO_TXT, re.M)
    assert _m, ("palavra de veredito nao achada no contrato", _n)
    PALAVRAS_DE_VEREDITO[_n] = _m.group(1)
assert all(w.endswith("GATE_UNMOVED") for w in PALAVRAS_DE_VEREDITO.values())
TOKENS_PROIBIDOS_V412 = tuple(D11.TOKENS_PROIBIDOS_V411)

# ---------------------------------------------------------------- o texto publico (a pagina R9 e a traducao); o contrato pina a pagina por sha16
_m = re.search(r"o_que_fica_claro_REV13\\O_QUE_FICA_CLARO_v412_R13\.md` \(sha16 `([0-9a-f]{16})`; (\d+) bytes\)", _CONTRATO_TXT)
assert _m, "o contrato nao pina a pagina R13"
PAGINA_ARQ = os.path.join(HERE, "o_que_fica_claro_REV13", "O_QUE_FICA_CLARO_v412_R13.md")
assert hashlib.sha256(open(PAGINA_ARQ, "rb").read()).hexdigest()[:16] == _m.group(1) and os.path.getsize(PAGINA_ARQ) == int(_m.group(2)), "a pagina R13 nao e' a do contrato"
PAGINA_EN_ARQ = os.path.join(HERE, "O_QUE_FICA_CLARO_v412_R13_EN.md")
TEXTO_PUBLICO_ARQ = os.path.join(HERE, "TEXTO_PUBLICO_v412.json")
TITULO_SECAO_V412 = {"pt": "O que fica claro na v412", "en": "What becomes clear in v412"}
TOPICO_NOVO = "v412-selada-camada-cientifica-e-matematica.md"

# ---------------------------------------------------------------- as saidas da rodada (a pasta da cadeia)
ENSAIO_TOPO_PROPOSTO = False
SAIDA = HERE
RODADA_PAI = SANDBOX_PAI
CANDIDATO_ARQ = os.path.join(SAIDA, CANDIDATO)
MANIFESTO_ARQ = os.path.join(SAIDA, "CANDIDATO_v412.json")
FORMAL_MAP_ARQ = os.path.join(SAIDA, "FORMAL_MAP_v412.json")
PINS_ARQ = os.path.join(SAIDA, "v412_pins.py")
DRY_DIR = os.path.join(RODADA_PAI, "dry_v412")
FALSO_NOS_DIR = os.path.join(RODADA_PAI, "falso_nos_v412")
ROTULO_DO_ARTEFATO = "candidato"
MARCA_ENSAIO = {}


def saida(nome_):
    """o caminho de um artefato da rodada (na pasta da cadeia)."""
    return os.path.join(SAIDA, nome_)


def sha16_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]


def sha256_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()


# ---------------------------------------------------------------- nomes V412 que os scripts herdados da cadeia pedem (sem equivalente de conteudo na v412: a v412 nao embute falas; ficam VAZIOS ou iguais aos da v411)
FALAS_V412 = []
N_FALAS_V412 = 0
FALAS_CITADAS_V412 = []
DECISOES_V412 = {}
ERRATAS_V412 = []
ERRATAS_IDS_V412 = []
ERRATAS_TOKEN_V412 = ""
DECISOES_TOKEN_V412 = ""
FALA_ORDEM_V412 = None
H0DN_PASTA_VEDADA_V411 = D11.H0DN_PASTA_VEDADA_V410
INSUMOS_V412 = []
CITADOS_V412 = []
PEDRAS_V412 = [{"name": r.split("/")[-1][:-len(".lean")], "rel": r, "mod": r[:-len(".lean")].replace("/", ".")} for r in BUNDLE_RELS]
# aliases para os scripts herdados (a v411 e' a base: o que e' da v411 segue sendo da v411)
MD_ROTULO_H0DN_V412 = D11.MD_ROTULO_H0DN_V411
FRASE_MOLDURA_V412_PT = D11.FRASE_MOLDURA_V411_PT
FRASE_MOLDURA_V412_EN = D11.FRASE_MOLDURA_V411_EN
PEDRAS_V411 = []
FALA_REGRA_CONVERSA_V412 = D11.FALA_REGRA_CONVERSA_V411
MARCADORES_V412 = D11.MARCADORES_V411
N_FALAS_V410 = D10.N_FALAS_V410
FALA_TESTEMUNHO_V412 = D11.FALA_TESTEMUNHO_V411

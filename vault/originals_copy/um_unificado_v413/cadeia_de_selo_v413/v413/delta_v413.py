# -*- coding: utf-8 -*-
# [DERIVADO v413, claude-construtor-v413 (contrato da v413 congelado)] do molde v412\delta_v412_r7.py (que fica intacto): importa o delta da v412 e SOBRESCREVE o que a v413 muda.
"""delta_v413.py -- a UNICA definicao do DELTA da v413 pelo contrato congelado (os 21 modulos novos de TGLExt/, o modulo do kernel cujo texto muda, a escada, os cinco registros por especificacao e a secao nova do artigo).
No molde do delta_v412_r7: importa o delta da v412 (por delta_bn_v413.delta_v412_fixado(), que o carrega com o BANCADA_PINA_HOJE da v411 fixado, para que a importacao nao quebre depois do APLICAR do B(n)) e SOBRESCREVE o que a v413
muda. As constantes do kernel (a lista de modulos, o sufixo da raiz, as bandeiras, o modulo corrigido) sao LIDAS dos arquivos que o preparo escreveu (BUNDLE_v413.json, kernel_modulos_novos_v413.json, kernel\\FLAGS_v413.json);
a base e' a v412 selada, lida do contrato; as constantes do B(n) (o sandbox curto, o BANCADA_PINA_HOJE) sao lidas de bancada\\delta_bn_v413.py, nunca redefinidas. Validade no kernel nao e' creditacao; o gate nao se move.
Nada neste arquivo traz historia de conversa para o programa; os nomes V413 de atributos existem so' para os scripts da cadeia."""
import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_spec_bn = importlib.util.spec_from_file_location("delta_bn_v413", os.path.join(HERE, "bancada", "delta_bn_v413.py"))
DBN = importlib.util.module_from_spec(_spec_bn)
_spec_bn.loader.exec_module(DBN)
_MOD12 = DBN.delta_v412_fixado()
globals().update({k: v for k, v in vars(_MOD12).items() if not k.startswith("__")})
D12 = _MOD12
D11 = _MOD12.D11
D10 = _MOD12.D10
D9 = _MOD12.D9
D8 = _MOD12.D8
import e7_lib_v413 as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))               # (o update acima trouxe o HERE da v412: aqui e' a pasta da v413)
V412 = os.path.join(os.path.dirname(HERE), "v412")
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))
CENTRAL = os.path.dirname(WK)
UM_VERSION = "v413"
BASE_VERSION = "v412"
SANDBOX_PAI = str(L.SANDBOX_PAI)
SANDBOX = str(L.SANDBOX)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")
SANDBOX_ORIGEM = os.path.join(C, "t", "k412c", "final")
KERNEL_DIR = "kernel"
CANDIDATO = "um_v413_candidato.py"
BASE_DIR = "base_v412"
CONTRATO_ARQ = str(L.CONTRATO)
DESENHO_ARQ = CONTRATO_ARQ                                      # (o contrato congelado e' a regua da versao)
_CONTRATO_RAW = open(CONTRATO_ARQ, "rb").read()
CONTRATO_SHA16 = hashlib.sha256(_CONTRATO_RAW).hexdigest()[:16]
DESENHO_SHA16 = CONTRATO_SHA16
_CONTRATO_TXT = _CONTRATO_RAW.decode("utf-8").replace("\r\n", "\n")
BASE_SHA16_DA_ORDEM = L.BASE_SHA16_DA_ORDEM
SANDBOX_CURTO_DO_BN = DBN.SANDBOX_CURTO                         # (do delta do B(n): so' se LE, para conferir a coerencia do B(n); a Etapa 2 nunca cria nem escreve nela)
SANDBOX_GUARDAS = os.path.join(C, "t", "vb25")                  # o sandbox curto PROPRIO da Etapa 2 (as guardas estaticas da Bancada e o ensaio); conferido inexistente antes do primeiro uso
assert os.path.normcase(SANDBOX_GUARDAS) != os.path.normcase(SANDBOX_CURTO_DO_BN), "o sandbox curto da Etapa 2 nao pode ser o do pre-selo do B(n)"
SANDBOX_CURTO = SANDBOX_GUARDAS                                 # (os scripts herdados leem DL.SANDBOX_CURTO: na v413 e' o da Etapa 2, nunca o do B(n))
BANCADA_PINA_HOJE = DBN.BANCADA_PINA_HOJE

# ---------------------------------------------------------------- o BUNDLE (21 modulos) e o modulo corrigido, LIDOS dos arquivos do preparo
BUNDLE_LISTA_ARQ = os.path.join(HERE, "kernel_modulos_novos_v413.json")
BUNDLE_ARQ = os.path.join(HERE, "BUNDLE_v413.json")
_BL = json.load(open(BUNDLE_LISTA_ARQ, encoding="utf-8"))
_BD = json.load(open(BUNDLE_ARQ, encoding="utf-8"))
BUNDLE_RELS = list(_BL["novos"])
BUNDLE_MODS = [p[:-len(".lean")].replace("/", ".") for p in BUNDLE_RELS]
N_BUNDLE = len(BUNDLE_RELS)
BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}
MANIFESTO_ARQ_PEDRAS = str(L.MANIFESTO)
_MAN = json.load(open(MANIFESTO_ARQ_PEDRAS, encoding="utf-8"))
assert _BD["manifesto_sha256"] == hashlib.sha256(open(MANIFESTO_ARQ_PEDRAS, "rb").read()).hexdigest(), "o bundle nao foi preparado com o manifesto do contrato"
N_MODULOS_DO_MANIFESTO = len(_MAN["modulos_novos"])
assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == N_MODULOS_DO_MANIFESTO == 21 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS) and [b["rel"] for b in _BD["modulos"]] == BUNDLE_RELS, \
    "o bundle da v413 e' o dos modulos do manifesto vigente (21), na ordem topologica"
assert set(BUNDLE_MODS) == set(_MAN["modulos_novos"]), "os modulos do bundle nao sao os do manifesto"
ROOT_SUFFIX = _BD["root_suffix"]
assert ROOT_SUFFIX == "".join("import %s\n" % m for m in BUNDLE_MODS) == _BL["root_suffix"], "o sufixo da raiz nao e' o das importacoes do bundle"
AUDIT_PREFIX = ""
BUNDLE_DA_BANCADA = []
BUNDLE_DA_GERENCIA = list(BUNDLE_RELS)
# o modulo do kernel cujo TEXTO muda (so' a docstring; o codigo e as declaracoes sao os mesmos): o gerador SUBSTITUI o texto embutido dele
_KC = list(_BD["kernel_corrigido"])
assert len(_KC) == 1 and _KC[0]["rel"] == "TGLExt/OResumoEPsiBit.lean" and _KC[0]["codigo_identico_a_origem"] is True, "o modulo corrigido nao e' o do bundle"
KERNEL_CORRIGIDO = {"rel": _KC[0]["rel"], "modulo": _KC[0]["modulo_completo"], "sha256_antes": _KC[0]["sha256_origem"], "sha256_depois": _KC[0]["sha256"], "bytes_depois": int(_KC[0]["bytes"]),
                    "recibo_da_correcao": _KC[0]["recibo_da_correcao"], "recibo_da_correcao_sha256": _KC[0]["recibo_da_correcao_sha256"]}
_mkc = (_MAN.get("kernel_corrigido") or {}).get(KERNEL_CORRIGIDO["modulo"]) or {}
assert len(_MAN.get("kernel_corrigido") or {}) == 1 and _mkc.get("sha256_origem") == KERNEL_CORRIGIDO["sha256_antes"] and _mkc.get("sha256_saida") == KERNEL_CORRIGIDO["sha256_depois"] and _mkc.get("codigo_identico") is True, \
    "o manifesto nao traz o modulo corrigido (kernel_corrigido) com os mesmos sha256 do bundle"
_FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v413.json"), encoding="utf-8"))
FLAG_PREFIX_POR_MODULO = {m.replace(".", "/") + ".lean": p for m, p in _FJ["prefixos"].items()}
assert set(FLAG_PREFIX_POR_MODULO) == set(BUNDLE_RELS)
ESCADA_BASE = int(_FJ["escada"][0])
ESCADA_NOVA = int(_FJ["escada"][1])
N_FLAGS = int(_FJ["n_flags"])
assert ESCADA_NOVA == ESCADA_BASE + N_FLAGS == ESCADA_BASE + len(_FJ["flags"])

# ---------------------------------------------------------------- os cinco registros por especificacao (nomes e palavras de veredito LIDOS do contrato, na ordem dele)
_REG = re.findall(r"^- `([a-z0-9_]+_v413)`[^\n]*\n  `([A-Z0-9_]+)`", _CONTRATO_TXT, re.M)
REGISTROS_SPEC_V413 = [n for n, _ in _REG]
assert len(REGISTROS_SPEC_V413) == 5 and len(set(REGISTROS_SPEC_V413)) == 5 and REGISTROS_SPEC_V413[-1] == "cunhagens_v413", ("os registros do contrato", REGISTROS_SPEC_V413)
PALAVRAS_DE_VEREDITO = dict(_REG)
# (contrato R2, secao 2) o registro kh_n1_cobertura_v413, que a custodia exige: no molde do kh_n1_cobertura_v411 do programa, a partir do recibo kernel\KH_N1_v413.json; roda antes do cunhagens_v413
REGISTROS_SPEC_V413_CONTRATO = list(REGISTROS_SPEC_V413)
KH_REGISTRO_V413 = L.KH_REGISTRO_V413
KH_N1_V413_ARQ = str(L.KH_N1_V413)
_kh_pre, _kh_suf = L.palavra_kh_v413()
PALAVRAS_DE_VEREDITO[KH_REGISTRO_V413] = _kh_pre + "__" + _kh_suf
REGISTROS_SPEC_V413 = REGISTROS_SPEC_V413_CONTRATO[:-1] + [KH_REGISTRO_V413] + REGISTROS_SPEC_V413_CONTRATO[-1:]
assert all(w.endswith("GATE_UNMOVED") for w in PALAVRAS_DE_VEREDITO.values())
REGISTROS_FUNCAO = []                                            # a v413 nao tem registro com funcao novo
REGISTROS_FUNCAO_V413 = []
REGISTROS_SPEC_V412 = list(D12.REGISTROS_SPEC_V412)              # herdados, selados
TOKENS_PROIBIDOS_V413 = tuple(D12.TOKENS_PROIBIDOS_V412)

# ---------------------------------------------------------------- o texto publico (a pagina pinada pelo contrato, ou a proposta no modo proposta) e a traducao
MODO = L.MODO
PAGINA_ARQ = str(L.PAGINA)
PAGINA_EN_ARQ = str(L.PAGINA_EN)
TEXTO_PUBLICO_ARQ = str(L.saida("TEXTO_PUBLICO_v413.json"))
_tit = re.search(r"^# (.+)$", open(PAGINA_ARQ, "rb").read().decode("utf-8"), re.M)
TITULO_SECAO_V413 = {"pt": _tit.group(1).strip(), "en": "What becomes clear in v413"}
assert TITULO_SECAO_V413["pt"] == "O que fica claro na v413"

# ---------------------------------------------------------------- as saidas (os manifestos na pasta da cadeia; o candidato FORA de work\\)
ENSAIO_TOPO_PROPOSTO = False
SAIDA = HERE
RODADA_PAI = SANDBOX_PAI
CANDIDATO_DIR = str(L.CAND_DIR)
CANDIDATO_ARQ = os.path.join(CANDIDATO_DIR, CANDIDATO)
MANIFESTO_ARQ = str(L.saida("CANDIDATO_v413.json"))
FORMAL_MAP_ARQ = str(L.saida("FORMAL_MAP_v413.json"))
PINS_ARQ = str(L.saida("v413_pins.py"))
DRY_DIR = os.path.join(RODADA_PAI, "dry_v413" + L.SUFIXO)
FALSO_NOS_DIR = os.path.join(RODADA_PAI, "falso_nos_v413" + L.SUFIXO)
ROTULO_DO_ARTEFATO = "candidato"
MARCA_ENSAIO = {}


def saida(nome_):
    """o caminho de um artefato da rodada (na pasta da cadeia; no modo proposta, com o sufixo)."""
    return str(L.saida(nome_))


def sha16_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]


def sha256_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()


# ---------------------------------------------------------------- nomes V413 que os scripts herdados da cadeia pedem (a v413 nao embute falas: ficam VAZIOS ou iguais aos da v412)
FALAS_V413 = []
N_FALAS_V413 = 0
FALAS_CITADAS_V413 = []
DECISOES_V413 = {}
ERRATAS_V413 = []
ERRATAS_IDS_V413 = []
ERRATAS_TOKEN_V413 = ""
DECISOES_TOKEN_V413 = ""
FALA_ORDEM_V413 = None
INSUMOS_V413 = []
CITADOS_V413 = []
PEDRAS_V413 = [{"name": r.split("/")[-1][:-len(".lean")], "rel": r, "mod": r[:-len(".lean")].replace("/", ".")} for r in BUNDLE_RELS]
PEDRAS_V412 = list(D12.PEDRAS_V412)
MD_ROTULO_H0DN_V413 = D12.MD_ROTULO_H0DN_V412
FRASE_MOLDURA_V413_PT = D12.FRASE_MOLDURA_V412_PT
FRASE_MOLDURA_V413_EN = D12.FRASE_MOLDURA_V412_EN
FALA_REGRA_CONVERSA_V413 = D12.FALA_REGRA_CONVERSA_V412
MARCADORES_V413 = D12.MARCADORES_V412
FALA_TESTEMUNHO_V413 = D12.FALA_TESTEMUNHO_V412

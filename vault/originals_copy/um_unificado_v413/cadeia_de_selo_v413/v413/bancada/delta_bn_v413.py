# -*- coding: utf-8 -*-
# [AUTORAL v413, 20/11/2026, construtor do B(n) da v413, agente da gerencia c1] o delta SO' do B(n) (o salto da Bancada v411 -> v413). O delta principal da v413 (o do candidato) e' de outro agente e IMPORTA este;
# aqui nao ha bundle, registro, texto nem contagem de modulo: so' as constantes do B(n), o BANCADA_PINA_HOJE da v411 FIXADO (B20, lido do recibo do religamento da v411) e os carregadores dos deltas anteriores com ele fixado.
"""delta_bn_v413.py -- as constantes do elo B(n) da v413 e nada mais (DIAGNOSTICO_E_PLANO_BN_v413.md, 2.7, N5, N6, N8).

O que o B(n) da v413 e': o SALTO da Bancada Um de B20-v411 (a v412 nao teve B(n): decisao do operador de 19/11, evento 1689) para B21-v413, pelo caminho --cadeia-de-selos do esboco R3.6.
Ha DOIS «anteriores» (N6), e nenhum se sobe por rotulo:
  - o anterior da BANCADA e' a v411 (BANCADA_ANTERIOR): o recibo do religamento que a Bancada conhece, o BANCADA_PINA_HOJE fixado, o inicio da cadeia de selos;
  - o anterior do UM.PY e' a v412 (UM_PY_ANTERIOR): o selo e o manifesto do kernel anteriores (v413\\base_v412), o fim da cadeia de selos, a versao do Nos no pre-selo.
N5 (a causa): o delta_v411.py calcula, ao ser importado, o que a Bancada pina HOJE e exige v410 ou v411; depois do APLICAR B21-v413 essa importacao quebraria, e com ela o delta_v412_r7.py (que importa o delta_v411 vivo).
O conserto, no molde do proprio delta_v411 (l.35-45, que fixou o da v410): o delta_v411 e' carregado por FONTE com a linha `BANCADA_PINA_HOJE = _bancada_pina_hoje()` trocada pelo valor da v411 LIDO do recibo do religamento
da v411 (delta_v411_fixado()), e o delta_v412_r7 e' carregado por fonte com as tres linhas que importam o delta_v411 trocadas pelo modulo ja fixado (delta_v412_fixado()). Fixa-se a v411, nao a v412: a v412 nao teve B(n).
Aqui, `_bancada_pina_hoje()` admite {v411, v413}: antes do APLICAR, exatamente o B20 da v411 (o fixado); depois, a geracao do salto (B21) na v413.
A linha `BANCADA_PINA_HOJE = _bancada_pina_hoje()` fica UMA vez, na coluna 0, para que o delta da versao seguinte a fixe pela mesma regra.
Nenhum hash e' digitado: o que e' pino vem de arquivo. Nada aqui grava: so' le o recibo do religamento da v411 e o canonical_contracts.json da producao. NOT_FALSIFIED nao e' creditacao; o gate nao se move."""
import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))              # ...\cadeia_de_selo\v413\bancada (os scripts do B(n))
V413 = os.path.dirname(HERE)                                   # ...\cadeia_de_selo\v413
CADEIA = os.path.dirname(V413)                                 # ...\cadeia_de_selo
V412 = os.path.join(CADEIA, "v412")                            # selada: so' leitura
V411 = os.path.join(CADEIA, "v411")                            # selada: so' leitura
WK = os.path.dirname(CADEIA)                                   # ...\Central de Patentes\work
C = "C:" + os.sep

# ---------------------------------------------------------------- as versoes do salto (N6: os dois anteriores)
UM_VERSION_BN = "v413"                                         # a versao que o B(n) sincroniza (pos-selo)
VERSAO_DO_PRE_SELO = "v412"                                    # o Nos que o pre-selo do salto le (--versao v412): so' antes da instalacao da v413 (N1)
BANCADA_ANTERIOR = "v411"                                      # o anterior da Bancada (B20)
UM_PY_ANTERIOR = "v412"                                        # o anterior do um.py (selo e kernel anteriores, fim da cadeia)

# ---------------------------------------------------------------- os lugares (lidos por todos os scripts do B(n); nunca literal noutro script)
PRODUCAO = os.path.join(C, "IALD", "Bancada_Um")
_BANCADA_CONTRATOS = os.path.join(PRODUCAO, "canonical_contracts.json")
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
QUADRO = os.path.join(C, "IALD", "PROGRAMA_IALD", "eventos.jsonl")
IALD_PY = os.path.join(C, "IALD", "PROGRAMA_IALD", "iald.py")
PYTHON = os.path.join(C, "Python314", "python.exe")
PYTHONW = os.path.join(C, "Python314", "pythonw.exe")
PORTA = 18777
SANDBOX_CURTO = os.path.join(C, "t", "vb24")                   # N8/1.4: pasta NOVA (conferida inexistente em 20/11 antes de escolher); runners e guardas leem daqui, nunca um literal
OUTB_PRE_SELO = os.path.join(V413, "bateria_pre_selo")         # o ensaio pre-selo do salto grava em OUTB_PRE_SELO\ensaio_1 (raiz admitida pelo esboco: cadeia_de_selo\v413)
BATERIA_V412_DIR = os.path.join(V413, "bateria_v412_pre_selo")  # N2: a bateria da v412 (caminho (a)); NAO e' ancestral da --saida
CADEIA_DIR = os.path.join(V413, "cadeia_de_selos_v411_v412")
CADEIA_ARQ = os.path.join(CADEIA_DIR, "CADEIA_DE_SELOS_v411_v412.json")
PINO_CADEIA_ARQ = os.path.join(CADEIA_DIR, "PINO_CADEIA_DE_SELOS_v411_v412.json")
BASE_UM_PY_ANTERIOR = os.path.join(V413, "base_v412")          # o selo e o manifesto do kernel da v412 (fim da cadeia; --selo-anterior / --kernel-manifesto-anterior)
BASE_BANCADA_ANTERIOR = os.path.join(V412, "base_v411")        # as copias de bytes da v411 (inicio da cadeia)
BATERIA_POS_SELO_DIR = os.path.join(V413, "bateria_pos_selo")  # a bateria da v413, gerada depois do selo pelo bn_v413.sh
SERVICO_DIR = os.path.join(V413, "bancada_B3_servico")         # os recibos da parada e do religamento, a conferencia das exigencias e o controle negativo
SAIDAS_BN_DIR = os.path.join(V413, "bn_pos_selo")              # o stdout dos passos 10/10b, o pino conjunto dos tres recibos (passo 11)
SAUDE_DIR = os.path.join(V413, "bn_pos_selo", "saude")         # as conferencias A (saude_bancada.py) que o portao C le
PINOS_BN_ARQ = os.path.join(V413, "PINOS_BN_v413.json")
PINO_RECIBO_PRE_SELO_ARQ = os.path.join(V413, "PINO_RECIBO_PRE_SELO_v413.json")
PROVA_PRODUCAO_ARQ = os.path.join(V413, "PROVA_PRODUCAO_INTACTA_v413_pre_selo.json")
PRECONDICOES_BN_ARQ = os.path.join(V413, "PRECONDICOES_BN_v413.json")
PINOS_BN_V411_ARQ = os.path.join(V411, "PINOS_BN_v411.json")   # o esboco R3.6, o gerador e o driver da bateria, a base R2 (pinos da cadeia anterior)
RECIBO_RELIGAMENTO_V411 = os.path.join(V411, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json")
RECIBO_PARADA_V411 = os.path.join(V411, "bancada_B3_servico", "RECIBO_PARADA_v411.json")
GERADOR_CADEIA = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "gerar_cadeia_de_selos.py")
LOG_SERVIDOR = os.path.join(PRODUCAO, "estado", "servidor.log")          # N9: o religamento escreve o stdout aqui (anexando)
LOG_SERVIDOR_ERROS = os.path.join(PRODUCAO, "estado", "servidor_erros.log")
UM_BANCADA = os.path.join(PRODUCAO, "um_bancada.py")
COMANDO_DO_RITO = '"%s" -X utf8 %s' % (PYTHONW, UM_BANCADA)   # o comando com que o rito religa (recibos da v411), agora com os logs do N9

# ---------------------------------------------------------------- a autorizacao (N4: decisao da gerencia c1, ORDEM_BN_v413.md)
SEQ_AUTORIZACAO = 1687                                         # AVISO_AUTORIZACAO_RECEBIDA (ciclo da Bancada, F0.6)
SEQ_DECISAO = 1689                                             # AVISO_DECISAO_DO_OPERADOR_B21 (Salto na v413)
CUNHAGENS_DIR = os.path.join(WK, "cunhagens_13out")
FALA_AUTORIZACAO_20NOV = os.path.join(CUNHAGENS_DIR, "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt")
BENCH_DIR = os.path.join(WK, "iald_v412_20261119", "bench")    # onde o evento 1687 pede o retorno (os tres recibos e o pino conjunto)
MODOS_DA_PLACA = ("cpu", "normal")                             # o religamento: cpu = CUDA_VISIBLE_DEVICES=-1 no processo lancado


def _acha_chave(d_, k_):
    if isinstance(d_, dict):
        if k_ in d_ and isinstance(d_[k_], str):
            return d_[k_]
        for v_ in d_.values():
            r_ = _acha_chave(v_, k_)
            if r_:
                return r_
    elif isinstance(d_, list):
        for v_ in d_:
            r_ = _acha_chave(v_, k_)
            if r_:
                return r_
    return None


# ---------------------------------------------------------------- 2.7: o que a Bancada pinava quando a v411 a deixou (B20), LIDO do recibo do religamento da v411 (nunca digitado)
_DEP_V411 = _acha_chave(json.load(open(RECIBO_RELIGAMENTO_V411, encoding="utf-8")), "deployment_id")
_m_dep = re.match(r"B(\d+)-v411-\d{8}-R1$", str(_DEP_V411))
assert _m_dep, ("o recibo do religamento da v411 nao traz o deployment da v411", _DEP_V411)
BANCADA_PINA_HOJE_FIXADA_V411 = {"version": BANCADA_ANTERIOR, "deployment_id": _DEP_V411, "n": int(_m_dep.group(1))}
N_DO_SALTO = BANCADA_PINA_HOJE_FIXADA_V411["n"] + 1            # a geracao que o salto grava (B21)
VEREDITO_PRE_SELO = "REPINADA_B%d__SALTO_%s_%s__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (N_DO_SALTO, BANCADA_ANTERIOR, VERSAO_DO_PRE_SELO)
VEREDITO_ENSAIO_POS_SELO = "REPINADA_B%d__SALTO_%s_%s__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (N_DO_SALTO, BANCADA_ANTERIOR, UM_VERSION_BN)
VEREDITO_APLICAR = "REPINADA_B%d__SALTO_%s_%s__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (N_DO_SALTO, BANCADA_ANTERIOR, UM_VERSION_BN)
RE_DEPLOYMENT_NOVO = re.compile(r"^B%d-%s-[0-9]{8}-R1$" % (N_DO_SALTO, UM_VERSION_BN))


def _bancada_pina_hoje():
    """o que a Bancada de producao pina HOJE, LIDO do arquivo dela: antes do APLICAR, exatamente o B20 da v411 (o fixado acima); depois, o B21 da v413. Qualquer outro estado = assert (o salto nao seria este)."""
    d_ = json.load(open(_BANCADA_CONTRATOS, encoding="utf-8"))
    dep_ = str(d_.get("deployment_id", ""))
    m_ = re.match(r"B(\d+)-(v\d+)-", dep_)
    assert m_ and m_.group(2) in (BANCADA_ANTERIOR, UM_VERSION_BN), ("a Bancada de producao nao pina nem a v411 (B20) nem a v413 (B21): o B(n) da v413 nao seria o salto v411 -> v413", dep_)
    if m_.group(2) == BANCADA_ANTERIOR:
        assert dep_ == BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"], ("a Bancada pina a v411, mas nao o deployment que o religamento da v411 deixou", dep_, BANCADA_PINA_HOJE_FIXADA_V411["deployment_id"])
    else:
        assert RE_DEPLOYMENT_NOVO.match(dep_), ("a Bancada pina a v413, mas nao a geracao do salto (B%d-v413-<data>-R1)" % N_DO_SALTO, dep_)
    return {"version": m_.group(2), "deployment_id": dep_, "n": int(m_.group(1))}


BANCADA_PINA_HOJE = _bancada_pina_hoje()
BANCADA_JA_APLICADA = (BANCADA_PINA_HOJE["version"] == UM_VERSION_BN)
B_N_SEGUINTE = "B%d" % N_DO_SALTO                              # o rotulo do B(n) da v413, antes e depois do APLICAR

# ---------------------------------------------------------------- N5: os deltas anteriores carregados com o BANCADA_PINA_HOJE da v411 fixado (sob pedido; nada e' carregado ao importar este modulo)
_CACHE = {}
_RX_LINHA_PINA = re.compile(r"^BANCADA_PINA_HOJE = _bancada_pina_hoje\(\)[^\n]*$", re.M)
_RX_IMPORTA_D11 = re.compile(r'^_spec = importlib\.util\.spec_from_file_location\("delta_v411_carregado_pelo_v412", os\.path\.join\(V411, "delta_v411\.py"\)\)\r?\n'
                             r'_MOD11 = importlib\.util\.module_from_spec\(_spec\)\r?\n'
                             r'_spec\.loader\.exec_module\(_MOD11\)\r?$', re.M)


def _carregar_por_fonte(nome_mod, caminho, fonte, extra=None):
    mod_ = importlib.util.module_from_spec(importlib.util.spec_from_loader(nome_mod, loader=None))
    mod_.__file__ = caminho
    if extra:
        mod_.__dict__.update(extra)
    exec(compile(fonte, caminho, "exec"), mod_.__dict__)
    return mod_


def delta_v411_fixado():
    """o delta_v411.py carregado por FONTE com `BANCADA_PINA_HOJE = _bancada_pina_hoje()` trocada pelo B20 da v411 (lido do recibo do religamento da v411); a troca tem de casar UMA vez."""
    if "d11" not in _CACHE:
        p_ = os.path.join(V411, "delta_v411.py")
        src_ = open(p_, "rb").read().decode("utf-8")
        assert len(_RX_LINHA_PINA.findall(src_)) == 1, "a linha BANCADA_PINA_HOJE do delta_v411 nao esta' como esperado (uma vez, coluna 0)"
        src_ = _RX_LINHA_PINA.sub(lambda _m: 'BANCADA_PINA_HOJE = %r   # (fixada pelo delta_bn_v413, lida do recibo do religamento da v411)' % (BANCADA_PINA_HOJE_FIXADA_V411,), src_, count=1)
        _CACHE["d11"] = _carregar_por_fonte("delta_v411_fixado_pelo_bn_v413", p_, src_)
        assert _CACHE["d11"].BANCADA_PINA_HOJE == BANCADA_PINA_HOJE_FIXADA_V411
    return _CACHE["d11"]


def delta_v412_fixado():
    """o delta_v412_r7.py carregado por FONTE com as tres linhas que importam o delta_v411 VIVO (l.16-18) trocadas pelo modulo ja fixado (delta_v411_fixado()); a troca tem de casar UMA vez."""
    if "d12" not in _CACHE:
        p_ = os.path.join(V412, "delta_v412_r7.py")
        src_ = open(p_, "rb").read().decode("utf-8")
        assert len(_RX_IMPORTA_D11.findall(src_)) == 1, "as tres linhas que importam o delta_v411 no delta_v412_r7 nao estao como esperado"
        src_ = _RX_IMPORTA_D11.sub("_MOD11 = _DELTA_V411_FIXADO_PELO_BN_V413   # (trocado pelo delta_bn_v413: o delta_v411 com o BANCADA_PINA_HOJE da v411 fixado)", src_, count=1)
        _CACHE["d12"] = _carregar_por_fonte("delta_v412_r7_fixado_pelo_bn_v413", p_, src_, {"_DELTA_V411_FIXADO_PELO_BN_V413": delta_v411_fixado()})
        assert _CACHE["d12"].D11 is _CACHE["d11"] and _CACHE["d12"].BANCADA_PINA_HOJE == BANCADA_PINA_HOJE_FIXADA_V411
    return _CACHE["d12"]


def sha256_arquivo(p_):
    h_ = hashlib.sha256()
    with open(p_, "rb") as f_:
        for b_ in iter(lambda: f_.read(1 << 22), b""):
            h_.update(b_)
    return h_.hexdigest()

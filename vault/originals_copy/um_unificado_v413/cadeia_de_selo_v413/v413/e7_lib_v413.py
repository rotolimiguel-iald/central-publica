"""Etapa 2 da v413 pelo contrato congelado: utilidades comuns. Deriva de v412\\e7_lib_v412.py (que fica intacto); grava o estado em ETAPA_2_ESTADO_v413.json.
Os pinos (manifesto, ancoras, pagina, inventario, base) sao LIDOS do contrato vigente e conferidos por sha256 dos bytes; nada e' digitado.
O MODO: 'contrato' (a pagina pinada pelo contrato) ou 'proposta' (V413_PAGINA_PROPOSTA=1: a pagina de proposta_pagina_R1\\, que NAO e' a do contrato;
toda saida do modo proposta leva o sufixo _PROPOSTA_R1 e o candidato vai para outra pasta). O modo proposta existe so' para exercitar a cadeia ate' o fim
enquanto a pagina pinada nao passa pela guarda herdada; o que vale como entrega e' o modo contrato."""
import datetime, hashlib, json, os, re
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v413")
V412 = D.parent / "v412"
ESTADO = D / "ETAPA_2_ESTADO_v413.json"
CONTRATO = D / os.environ.get("V413_CONTRATO", "CONTRATO_v413_R2.md")   # (o R2, congelado, substitui o R1, que fica como registro)
CONTRATO_TXT = CONTRATO.read_bytes().decode("utf-8").replace("\r\n", "\n")
SANDBOX_PAI = Path(r"C:\t\k413c")
SANDBOX = SANDBOX_PAI / "final"
PEDRAS = D / "insumos" / "pedras_limpas" / "TGLExt"
KERNEL_EDITS = D / "insumos" / "kernel_edits" / "TGLExt"
KD = D / "kernel"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")


def sha256_arq(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha16_arq(p) -> str:
    return sha256_arq(p)[:16]


def _pino(rx, nome):
    m = re.findall(rx, CONTRATO_TXT)
    assert len(m) >= 1, ("o contrato nao pina", nome)
    vals = set(m)
    assert len(vals) == 1, ("o contrato pina dois valores diferentes", nome, vals)
    return m[0]


MANIFESTO = D / "insumos" / "MANIFESTO_PEDRAS_v413.json"
ANCORAS = D / "insumos" / "ANCORAS_PROPOSTAS_v413.json"
INVENTARIO = D / "INVENTARIO_CADEIA_v413.json"
PIN_MANIFESTO = _pino(r"insumos\\MANIFESTO_PEDRAS_v413\.json` \(sha16 `([0-9a-f]{16})`", "manifesto")
PIN_ANCORAS = _pino(r"insumos\\ANCORAS_PROPOSTAS_v413\.json` \(sha16 `([0-9a-f]{16})`", "ancoras")
PIN_INVENTARIO = _pino(r"INVENTARIO_CADEIA_v413\.json`, sha16 `([0-9a-f]{16})`", "inventario")
_mpag = re.findall(r"`(o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R\d+\.md)` \(sha16 `([0-9a-f]{16})`", CONTRATO_TXT)
assert len(set(_mpag)) == 1, ("a pagina pinada pelo contrato nao e' unica", _mpag)
PAGINA_CONTRATO = D / _mpag[0][0].replace("\\", os.sep)
PIN_PAGINA = _mpag[0][1]
BASE_SHA16_DA_ORDEM = _pino(r"Base: a v412 selada \(`um\.py` do N[oó]s, sha16 `([0-9a-f]{16})`", "base")
assert sha16_arq(MANIFESTO) == PIN_MANIFESTO, "o manifesto nao e' o do contrato"
assert sha16_arq(ANCORAS) == PIN_ANCORAS, "as ancoras propostas nao sao as do contrato"
assert sha16_arq(INVENTARIO) == PIN_INVENTARIO, "o inventario nao e' o do contrato"
assert sha16_arq(PAGINA_CONTRATO) == PIN_PAGINA, "a pagina nao e' a do contrato"

# o registro kh_n1_cobertura_v413 (contrato R2, secao 2: a custodia o exige, mesmo vazio, no molde do kh_n1_cobertura que o programa da v412 traz, a partir do recibo kernel\KH_N1 da Etapa 1)
KH_REGISTRO_V413 = "kh_n1_cobertura_v413"
KH_N1_V413 = KD / "KH_N1_v413.json"
assert "registro `kh_n1_cobertura_v413`, mesmo vazio" in CONTRATO_TXT or "R1" in CONTRATO.name, "o contrato vigente nao pede o registro kh_n1_cobertura_v413"


def palavra_kh_v413():
    """a palavra de veredito do kh_n1_cobertura_v413, no molde da do kh_n1_cobertura_v411 (o ultimo kh do programa), com os numeros LIDOS do recibo KH_N1_v413.json (nunca digitados)."""
    kh = ler_json(KH_N1_V413)
    lt = kh["linha_TOTAL"]
    assert lt["fora_do_trio"] == 0 and kh["nao_lidas_pelo_leitor_v394"] == 0 and kh["sorryAx_no_log_do_audit"] == 0 and kh["novas_no_trio"] is True and kh["axiom_report_efetivo_n"] == lt["decl"], "o recibo KH_N1 da v413 nao fecha"
    return ("TGL_KH_N1_COBERTURA_V413", "AXIOM_REPORT_COVERS_THE_WHOLE_TGL_AND_TGLEXT_CLOSURE_%d_CONSTANTS_%d_THEOREMS_NONE_OUTSIDE_THE_TRIO__ALL_NAMES_READ_BY_THE_V394_PARSER__%d_NEW_MODULES__GATE_UNMOVED"
            % (lt["decl"], lt["thm"], kh["n_modulos_novos"]))


MODO = "proposta" if os.environ.get("V413_PAGINA_PROPOSTA") == "1" else "contrato"
PROPOSTA_DIR = D / "proposta_pagina_R1"
if MODO == "proposta":
    PAGINA = PROPOSTA_DIR / "O_QUE_FICA_CLARO_v413_R1_PROPOSTA.md"
    PAGINA_EN = PROPOSTA_DIR / "O_QUE_FICA_CLARO_v413_R1_PROPOSTA_EN.md"
    SUFIXO = "_PROPOSTA_R1"
    CAND_DIR = SANDBOX_PAI / "candidato_proposta_R1"
else:
    PAGINA = PAGINA_CONTRATO
    PAGINA_EN = D / (PAGINA_CONTRATO.stem + "_EN.md")
    SUFIXO = ""
    CAND_DIR = SANDBOX_PAI / "candidato"


def saida(nome: str) -> Path:
    """o caminho de um artefato da Etapa 2 na pasta da cadeia; no modo proposta, com o sufixo _PROPOSTA_R1 antes da extensao."""
    p = Path(nome)
    return D / (p.stem + SUFIXO + p.suffix)


def agora() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def salvar_bytes(p, dados: bytes, backup=True) -> None:
    """Backup de BYTES do arquivo existente; escrita por temporario; confere o tamanho; substitui."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    if backup and p.exists():
        if p.read_bytes() == dados:
            return
        bak = Path(str(p) + ".bak_" + agora())
        n = 0
        while bak.exists():
            n += 1
            bak = Path(str(p) + ".bak_" + agora() + "_%d" % n)
        bak.write_bytes(p.read_bytes())
        assert bak.read_bytes() == p.read_bytes(), ("o backup nao e' copia de bytes", str(bak))
    tmp = Path(str(p) + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.stat().st_size == len(dados), ("escrita truncada", str(p))
    os.replace(tmp, p)
    assert p.stat().st_size == len(dados)


def salvar_json(p, obj, backup=True) -> None:
    salvar_bytes(p, json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"), backup=backup)


def ler_json(p):
    return json.loads(Path(p).read_bytes().decode("utf-8"))


def estado_ler() -> dict:
    return ler_json(ESTADO) if ESTADO.exists() else {"blocos": {}}


def estado_bloco(bloco: str, feito: bool, arquivos: dict, nota: str = "", proximo: str = "", falta=None, extra: dict | None = None) -> None:
    """Grava o bloco no estado (por temporario e troca, guardando o anterior com .bak_<data>). `arquivos`: {rotulo: caminho}; o sha16 de cada um e' lido do arquivo."""
    est = estado_ler()
    est.setdefault("blocos", {})
    reg = {"feito": bool(feito), "modo": MODO, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "nota": nota,
           "arquivos": {k: {"caminho": str(v), "sha16": sha16_arq(v), "bytes": Path(v).stat().st_size} for k, v in arquivos.items() if Path(v).exists()},
           "arquivos_ausentes": [str(v) for v in arquivos.values() if not Path(v).exists()]}
    if extra:
        reg["extra"] = extra
    est["blocos"][bloco + ("" if MODO == "contrato" else "__modo_proposta")] = reg
    est["proximo_comando"] = proximo
    if falta is not None:
        est["falta"] = falta
    est["agente"] = "claude-construtor-v413 (Etapa 2 pelo contrato congelado)"
    est["contrato"] = CONTRATO.name
    est["contrato_sha16"] = sha16_arq(CONTRATO)
    est["ordem"] = "ORDEM_ETAPA_2_v413.md"
    est["ordem_sha16"] = sha16_arq(D / "ORDEM_ETAPA_2_v413.md")
    salvar_json(ESTADO, est)


class Exame:
    """Contador de checagens: cada checagem diz quantos itens examinou; zero itens e' falha visivel, nunca passagem."""

    def __init__(self, nome=""):
        self.nome = nome
        self.linhas = []

    def chk(self, rotulo, ok, n_itens, detalhe=None):
        passou = bool(ok) and n_itens > 0
        self.linhas.append({"checagem": rotulo, "ok": passou, "n_itens_examinados": int(n_itens), "detalhe": detalhe,
                            **({"falha_por_zero_itens": True} if (bool(ok) and n_itens <= 0) else {})})
        return passou

    @property
    def ok(self):
        return all(l["ok"] for l in self.linhas) and len(self.linhas) > 0

    def resumo(self):
        return {"nome": self.nome, "n_checagens": len(self.linhas), "n_ok": sum(1 for l in self.linhas if l["ok"]), "n_itens_total": sum(l["n_itens_examinados"] for l in self.linhas), "ok": self.ok}

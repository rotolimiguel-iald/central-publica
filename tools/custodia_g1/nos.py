# -*- coding: utf-8 -*-
"""O Nós (diretório vivo da gerência c1): as TRÊS MARCAS que disparam a custódia (regra do operador de 23/10/2026:
«pode custodiar sempre que o handoff aparecer, como regra») e o HANDOFF lido por MARCADORES.

As três marcas (estado_do_organismo.py l.96-112, generalizadas de `v3\\d\\d` para `v\\d{3,}` — L15 da ESPEC):
  1. `um_absoluto_selo.json`: `um_version` = N e `sha256["um.py"][:16]` = sha16 do `um.py` do Nós (senão: EM_OBRA);
  2. `MEMORIA_DA_LINHAGEM.md`: o bloco `## ... **vNNN SELADA ...**`;
  3. `HANDOFF_vNNN_CUSTODIA.md` + `rodada_vNNN_stdout.txt` + a pasta `work\\cadeia_de_selo\\vNNN`.
Só leitura. Falha de leitura é falha visível."""
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import util
from .util import FalhaLeitura, Parar

TRIO = ("propext", "Classical.choice", "Quot.sound")

RE_SELADA = re.compile(r"^## [^\n]*\*\*(v\d{3,}) SELADA[^*\n]*\*\*[^\n]*\n", re.M)
RE_CAB = re.compile(r"^## (?P<data>\d\d/\d\d/\d{4}) \u2014 \*\*(?P<v>v\d{3,}) SELADA[^*\n]*\*\*\s*`(?P<pin>[0-9a-f]{16})`\s*\u2014\s*(?P<titulo>[^\n]*?)\s*"
                    r"\((?P=v)\):\s*(?P<k>\d+|nenhum) m[o\u00f3]dulos? novos?,\s*escada\s*(?P<a>\d+)\s*\u2192\s*(?P<b>\d+)", re.M)
RE_MARCADOR = re.compile(r"<!-- INICIO_(?P<id>[A-Za-z0-9_]+) -->\r?\n(?P<corpo>.*?)<!-- FIM_(?P=id) -->", re.S)
RE_ABRE = re.compile(r"<!-- INICIO_([A-Za-z0-9_]+) -->")
RE_FECHA = re.compile(r"<!-- FIM_([A-Za-z0-9_]+) -->")


# ------------------------------------------------------------------ selo, um.py, diário
def selo(c):
    return util.ler_json(c.NOS / "um_absoluto_selo.json")


def sha16_um_py(c):
    return util.sha16(c.NOS / "um.py")


def diario_texto(c):
    return util.ler_texto(c.NOS / "MEMORIA_DA_LINHAGEM.md")


@dataclass
class BlocoDiario:
    versao: str
    data: str = ""            # dd/mm/aaaa
    pin16: str = ""
    titulo_pt: str = ""
    modulos_novos: int = -1
    escada_de: int = -1
    escada_para: int = -1
    cabecalho: str = ""
    corpo: str = ""
    ladder_no_corpo: str = ""  # «a/b» do último **a/b** do corpo (o 'rito')
    pin16_no_corpo: str = ""


def blocos_do_diario(c, texto=None):
    """versão -> BlocoDiario, lido do diário (nunca digitado). O sha16 sai do cabeçalho entre crases (v387+) ou do corpo."""
    d = texto if texto is not None else diario_texto(c)
    out = {}
    for m in RE_SELADA.finditer(d):
        v = m.group(1)
        ini = m.end()
        fim = d.find("\n## ", ini)
        corpo = d[ini: fim if fim > 0 else len(d)]
        b = BlocoDiario(versao=v, cabecalho=m.group(0).strip("\n"), corpo=corpo)
        mc = RE_CAB.match(m.group(0))
        if mc:
            b.data, b.pin16, b.titulo_pt = mc.group("data"), mc.group("pin"), mc.group("titulo")
            b.modulos_novos = 0 if mc.group("k") == "nenhum" else int(mc.group("k"))   # 25/10: «nenhum módulo novo» (v400)
            b.escada_de, b.escada_para = int(mc.group("a")), int(mc.group("b"))
        sh = re.findall(r"`um\.py` sha16 `([0-9a-f]{16})`", corpo) or re.findall(r"`([0-9a-f]{16})`", m.group(0))
        b.pin16_no_corpo = sh[-1] if sh else ""
        ri = re.findall(r"\*\*(\d+)/(\d+)\*\*", corpo)
        b.ladder_no_corpo = ("%s/%s" % ri[-1]) if ri else ""
        if not b.pin16:
            b.pin16 = b.pin16_no_corpo
        out.setdefault(v, b)      # a primeira ocorrência manda (como o passo zero de hoje: setdefault)
    return out


# ------------------------------------------------------------------ o handoff, por marcadores
@dataclass
class OQueE:
    versao: str = ""
    pin16: str = ""
    bytes_um_py: int = 0
    anterior: str = ""
    anterior_pin16: str = ""
    escada: str = ""
    completa: bool = False
    rc0: bool = False
    selftest_passou: bool = False
    gate_intocado: bool = False
    selo_ts: str = ""


RE_OQUEE = re.compile(
    r"\*\*O que \u00e9:\*\*\s*`um\.py`\s*\*\*(?P<v>v\d+)\*\*\s*`(?P<pin>[0-9a-f]{16})`\s*\((?P<bytes>[\d,\.]+)\s*B\)\s*sobre a\s*(?P<ant>v\d+)\s*"
    r"`(?P<antpin>[0-9a-f]{16})`;\s*(?P<a>\d+)/(?P<b>\d+);\s*(?P<comp>[A-Z\u00c7\u00c3 ]+);\s*rc\s*(?P<rc>\d+);\s*selftest\s*(?P<st>\w+);\s*gate\s*(?P<gate>[^;]+?);", re.S)


@dataclass
class Handoff:
    caminho: Path
    texto: str
    sha16_arquivo: str
    o_que_e: OQueE = None
    marcadores: dict = field(default_factory=dict)       # id -> texto completo (com as linhas de marcador)
    corpos: dict = field(default_factory=dict)           # id -> só o corpo
    problemas: list = field(default_factory=list)        # marcadores malformados/duplicados
    fontes_textos: dict = field(default_factory=dict)    # id -> «handoff» | caminho do TEXTOS_vNNN.md da gerência do site (25/10/2026)
    secoes: dict = field(default_factory=dict)           # cabeçalho em negrito (sem ':') -> parágrafo inteiro

    def bloco(self, id_):
        return self.marcadores.get(id_)

    def secao(self, prefixo):
        """Primeiro parágrafo cujo cabeçalho em negrito começa por `prefixo` (comparação sem caixa)."""
        p = prefixo.lower()
        for k, v in self.secoes.items():
            if k.lower().startswith(p):
                return v
        return None

    def ids_com(self, prefixo):
        return sorted(i for i in self.marcadores if i.startswith(prefixo))

    def paragrafos_prontos(self):
        """Os blocos `PARAGRAFO_*` do handoff, na ORDEM em que aparecem (README e site)."""
        return [(m.group("id"), m.group(0)) for m in RE_MARCADOR.finditer(self.texto) if m.group("id").startswith("PARAGRAFO_")]


def ler_handoff(c, v):
    p = c.NOS / ("HANDOFF_%s_CUSTODIA.md" % v)
    if not p.is_file():
        return None
    t = util.ler_texto(p).replace("\r\n", "\n")
    h = Handoff(caminho=p, texto=t, sha16_arquivo=util.sha16(p))
    m = RE_OQUEE.search(t)
    if m:
        h.o_que_e = OQueE(versao=m.group("v"), pin16=m.group("pin"), bytes_um_py=int(m.group("bytes").replace(",", "").replace(".", "")),
                          anterior=m.group("ant"), anterior_pin16=m.group("antpin"), escada="%s/%s" % (m.group("a"), m.group("b")),
                          completa="COMPLETA" in m.group("comp"), rc0=(m.group("rc") == "0"), selftest_passou=(m.group("st") == "PASSED"),
                          gate_intocado="intocado" in m.group("gate"))
        ms = re.search(r"Selo\s*`(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)`", t[m.start(): m.start() + 900])
        h.o_que_e.selo_ts = ms.group(1) if ms else ""
    # marcadores: pares INICIO/FIM; sem par, duplicado ou sem corpo = problema (a ESPEC manda PARAR, não adivinhar)
    abre, fecha = RE_ABRE.findall(t), RE_FECHA.findall(t)
    for i in sorted(set(abre) ^ set(fecha)):
        h.problemas.append("marcador %s sem par INICIO/FIM" % i)
    for m in RE_MARCADOR.finditer(t):
        i = m.group("id")
        if i in h.marcadores:
            h.problemas.append("marcador %s duplicado" % i)
            continue
        h.marcadores[i] = m.group(0)
        h.corpos[i] = m.group("corpo")
        if not m.group("corpo").strip():
            h.problemas.append("marcador %s vazio" % i)
    for par in t.split("\n\n"):
        mm = re.match(r"\*\*(.+?)\*\*", par.strip())
        if mm:
            h.secoes.setdefault(mm.group(1).rstrip(": ").strip(), par.strip())
    for i in h.marcadores:
        h.fontes_textos[i] = "handoff"
    # 25/10/2026: a prosa da custódia (os marcadores opcionais) pode vir da gerência do site num TEXTOS_vNNN.md na pasta de trabalho;
    # o handoff manda; o suplemento só preenche o que falta; malformado = problema (PARA)
    for sp in sorted(c.CEN.glob("work/custodia_%s_*/TEXTOS_%s.md" % (v, v))):
        ts = util.ler_texto(sp).replace("\r\n", "\n")
        a2, f2 = RE_ABRE.findall(ts), RE_FECHA.findall(ts)
        for i in sorted(set(a2) ^ set(f2)):
            h.problemas.append("marcador %s sem par INICIO/FIM em %s" % (i, sp.name))
        for m in RE_MARCADOR.finditer(ts):
            i = m.group("id")
            if i in h.marcadores:
                continue
            if not m.group("corpo").strip():
                h.problemas.append("marcador %s vazio em %s" % (i, sp.name))
                continue
            h.marcadores[i] = m.group(0)
            h.corpos[i] = m.group("corpo")
            h.fontes_textos[i] = str(sp)
    return h


# ------------------------------------------------------------------ as três marcas
@dataclass
class MarcasNos:
    versao: str
    selo_versao: str = ""
    relacao: str = ""                 # 'corrente' (N == selo) | 'superada' (N < selo) | 'futura' (N > selo)
    selo_ok: bool = False
    um_py_confere: bool = False
    diario_ok: bool = False
    handoff_ok: bool = False
    stdout_ok: bool = False
    cadeia_ok: bool = False
    em_obra: bool = False
    faltam: list = field(default_factory=list)
    em_obra_versoes: list = field(default_factory=list)   # versões com pasta em cadeia_de_selo mais novas que o selo
    estado: str = ""                  # PRONTA | EM_OBRA | INCOMPLETA | SUPERADA


def versoes_em_obra(c, acima_de):
    """Pastas `cadeia_de_selo\\vNNN` (nome exato) de versão maior que o selo: o Nós trabalha numa versão nova."""
    out = []
    if c.CS.is_dir():
        for p in c.CS.iterdir():
            m = re.fullmatch(r"v(\d{3,})", p.name)
            if m and p.is_dir() and int(m.group(1)) > acima_de:
                out.append(p.name)
    return sorted(out)


def marcas(c, v=None):
    s = selo(c)
    vs = s["um_version"]
    v = v or vs
    nv, nvs = util.versao_num(v), util.versao_num(vs)
    m = MarcasNos(versao=v, selo_versao=vs)
    m.relacao = "corrente" if nv == nvs else ("superada" if nv < nvs else "futura")
    pino = s["sha256"]["um.py"][:16]
    um = sha16_um_py(c)
    m.um_py_confere = (um == pino)
    m.selo_ok = (nv == nvs and m.um_py_confere)
    m.em_obra = (nv == nvs and not m.um_py_confere)
    m.em_obra_versoes = versoes_em_obra(c, nvs)
    bl = blocos_do_diario(c)
    m.diario_ok = v in bl
    m.handoff_ok = (c.NOS / ("HANDOFF_%s_CUSTODIA.md" % v)).is_file()
    m.stdout_ok = (c.NOS / ("rodada_%s_stdout.txt" % v)).is_file()
    m.cadeia_ok = (c.CS / v).is_dir()
    if m.relacao == "futura":
        m.faltam.append("o selo do Nós ainda é %s: a %s não foi selada" % (vs, v))
    if m.relacao == "corrente" and not m.um_py_confere:
        m.faltam.append("um.py do Nós (%s) != pino do selo (%s): EM OBRA" % (um, pino))
    for ok, rot in ((m.diario_ok, "bloco «%s SELADA» em MEMORIA_DA_LINHAGEM.md" % v), (m.handoff_ok, "HANDOFF_%s_CUSTODIA.md" % v),
                    (m.stdout_ok, "rodada_%s_stdout.txt" % v), (m.cadeia_ok, "work\\cadeia_de_selo\\%s" % v)):
        if not ok:
            m.faltam.append(rot)
    if m.em_obra or m.relacao == "futura":
        m.estado = "EM_OBRA"
    elif m.faltam:
        m.estado = "INCOMPLETA"
    elif m.relacao == "superada":
        m.estado = "SUPERADA"
    else:
        m.estado = "PRONTA"
    return m


def exigir_pronta(c, v):
    """Pré-condição de toda execução: as três marcas. EM_OBRA espera (WAIT); incompleta para (STOP)."""
    m = marcas(c, v)
    if m.estado == "EM_OBRA":
        raise util.Esperar("o Nós está em obra: %s" % "; ".join(m.faltam or ["selo ainda não é %s" % v]), m.faltam)
    if m.estado == "INCOMPLETA":
        raise Parar("as três marcas de %s estão incompletas" % v, m.faltam)
    return m


# ------------------------------------------------------------------ o artefato do selo e a escada no stdout
def escada_do_stdout(c, v):
    p = c.NOS / ("rodada_%s_stdout.txt" % v)
    if not p.is_file():
        return None
    m = re.findall(r"teoremas limpos: (\d+)/(\d+)", util.ler_texto(p, "replace"))
    return ("%s/%s" % m[-1]) if m else None


def artefatos_selados(c):
    """{nome: sha256} do selo, conferidos contra o disco do Nós. Devolve (mapa, divergentes)."""
    s = selo(c)
    div = [n for n, h in s["sha256"].items() if not (c.NOS / n).is_file() or util.sha256_arquivo(c.NOS / n) != h]
    return s["sha256"], div


def anterior_no_espelho(c, v):
    """P: a versão que ESTÁ (ou estava, antes da custódia de `v`) no espelho. Não é N-1 em custódia conjunta (v393+v394).
    Se o espelho ainda está atrás de v: é a `um_version` do selo do espelho. Se já alcançou v (ou passou): é a maior `um_vK_*`
    em BK com K < v (backup feito no passo zero daquela custódia)."""
    nv = util.versao_num(v)
    try:
        sv = util.ler_json(c.ESP / "um_absoluto_selo.json")["um_version"]
    except FalhaLeitura:
        sv = None
    if sv and util.versao_num(sv) < nv:
        return sv
    ks = []
    if c.BK.is_dir():
        for p in c.BK.iterdir():
            m = re.fullmatch(r"um_v(\d{3,})_([0-9a-f]{16})", p.name)
            if m and int(m.group(1)) < nv and p.is_dir():
                ks.append(int(m.group(1)))
    if not ks:
        raise Parar("não achei a versão anterior de %s no espelho nem em BK" % v)
    return util.nome_versao(max(ks))

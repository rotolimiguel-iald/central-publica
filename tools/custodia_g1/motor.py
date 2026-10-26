# -*- coding: utf-8 -*-
"""O motor de G1: contexto, marcas de «já aplicado», passos e a execução com gates.

Cada passo é uma função pequena com (nome, já_aplicado(), pré(), aplicar(), conferir()). A execução PARA no primeiro gate que
falha (nunca prossegue com hash divergente), grava um recibo por passo em work\\custodia_G1\\runs\\<vNNN>_<carimbo>\\, e só pratica
ATO PARA FORA (commit, push, subida do site, Central pública, escrita no ACOM) com `--publicar`.

`planejar` e `vigiar` só LEEM o mundo: nenhuma escrita fora de work\\custodia_vNNN_<data>\\ e work\\custodia_G1\\.

ESTADOS DA MARCA (achados dos céticos de 24/10/2026):
  APLICADO      o artefato prova que o passo foi feito (lido agora, por hash ou conteúdo);
  SUPERADO      uma versão posterior já o cobre E o artefato da versão prova (commit, blob, relatório, manifesto);
  SUPERADO_REL  «superado SÓ pela relação»: a versão é histórica e a superfície é regerada a cada versão — G1 NÃO tem artefato que o prove
                (conta como feito para «nada a fazer», mas vai DITO: nunca se confunde com prova);
  NA            não se aplica; OPERADOR  decisão do operador/gerência (não é de G1, mas fica à vista e muda o código de saída);
  FALTA / BLOQUEADO / INDETERMINADO   pendentes (BLOQUEADO = a pré-condição de `executar` falha agora; INDETERMINADO.leitura = falha de leitura)."""
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import nos, util
from .caminhos import Caminhos
from .util import G1Erro, Parar, FalhaLeitura, Esperar

SATISFEITOS = ("APLICADO", "SUPERADO", "SUPERADO_REL", "NA", "OPERADOR")
NAO_SATISFEITOS = ("FALTA", "BLOQUEADO", "INDETERMINADO")
PROVADOS = ("APLICADO", "SUPERADO", "NA")


@dataclass
class Marca:
    estado: str
    detalhe: str = ""
    leitura: bool = False             # INDETERMINADO por FALHA DE LEITURA (git ausente, arquivo ilegível): `executar` PARA (código 30), não aplica às cegas

    @property
    def satisfeita(self):
        return self.estado in SATISFEITOS

    @property
    def provada(self):
        """Provada no artefato (APLICADO, SUPERADO com evidência, NA). SUPERADO_REL e OPERADOR não são provas."""
        return self.estado in PROVADOS


def aplicado(det=""):
    return Marca("APLICADO", det)


def falta(det=""):
    return Marca("FALTA", det)


def superado(det=""):
    return Marca("SUPERADO", det)


def superado_rel(det=""):
    return Marca("SUPERADO_REL", det)


def indeterminado(det="", leitura=False):
    return Marca("INDETERMINADO", det, leitura)


def bloqueado(det=""):
    return Marca("BLOQUEADO", det)


def operador(det=""):
    return Marca("OPERADOR", det)


def na(det=""):
    return Marca("NA", det)


@dataclass
class Passo:
    id: str
    perna: int
    nome: str
    ja: object                        # (ctx) -> Marca
    aplicar: object = None            # (ctx) -> dict
    pre: object = None                # (ctx) -> [falhas]
    conferir: object = None           # (ctx) -> [falhas]
    escreve: str = ""
    externo: bool = False             # só com --publicar (commit, push, subida, Central pública, ACOM)
    fase: str = "A"                   # A = local; B = depois do espelho publicado
    longo: bool = False
    rede: bool = False
    depende: tuple = ()
    usa_quadro: bool = False          # a marca lê o quadro do organismo: em `executar` o quadro velho é REMEDIDO antes (nunca se decide por quadro velho)


# =================================================================== contexto
class Ctx:
    """Tudo que um passo precisa, lido uma vez. Preguiçoso e com cache; falha de leitura é falha visível."""

    def __init__(self, c=None, versao=None, data=None, sessao=None, ordem=None, coautor=None, rede=False, publicar=False,
                 ensaio=False, aceitar_molde=False, saida=None, run_dir=None, anterior=None, ator=None, trabalho=None):
        self.c = c or Caminhos()
        self.versao = versao or nos.selo(self.c)["um_version"]
        self.n = util.versao_num(self.versao)
        self.rede, self.publicar, self.ensaio, self.aceitar_molde = rede, publicar, ensaio, aceitar_molde
        self.coautor = coautor
        self.sessao = sessao or "a7"
        self.ator = ator or ("claude-central-%s" % self.sessao)       # id honesto de quem executa (o protocolo ACOM proíbe fabricar autenticação pelo nome)
        self.ordem = Path(ordem) if ordem else None
        self.data = data or datetime.now().strftime("%d/%m/%Y")
        self._saida = Path(saida) if saida else None
        self._trabalho = Path(trabalho) if trabalho else None
        self.run_dir = Path(run_dir) if run_dir else None
        self._anterior_forcado = anterior
        self._cache_t, self._cache_j, self._memo = {}, {}, {}
        self.avisos = []
        self.hashes = set()           # hashes que ESTA rodada calculou (o portão de texto só deixa citar esses e os do handoff)
        self.leitura = False          # True durante planejar/vigiar: as pré-condições pulam o que roda subprocesso ou toca o que é privado
        self.pode_remedir = False     # True só em `executar` fora de --ensaio: o quadro velho é remedido antes de decidir por ele

    # ---- leitura com cache (arquivos grandes: LEDGER 713 KB, index.html 158 KB, ESTADO 107 KB)
    def ler(self, p):
        p = str(p)
        if p not in self._cache_t:
            self._cache_t[p] = util.ler_texto(p, "replace")
        return self._cache_t[p]

    def lido(self, p):
        p = str(p)
        if p not in self._cache_j:
            self._cache_j[p] = util.ler_json(p)
        return self._cache_j[p]

    def memo(self, chave, f):
        if chave not in self._memo:
            self._memo[chave] = f()
        return self._memo[chave]

    # ---- versão, vizinhos e relação com o mundo
    @property
    def nos_marcas(self):
        return self.memo("marcas", lambda: nos.marcas(self.c, self.versao))

    @property
    def selo_nos(self):
        return self.memo("selo_nos", lambda: nos.selo(self.c))

    @property
    def corrente(self):
        """A versão é a do selo do Nós: é contra ela que o quadro mede as superfícies."""
        return self.selo_nos["um_version"] == self.versao

    @property
    def bloco_diario(self):
        return self.memo("bloco", lambda: nos.blocos_do_diario(self.c).get(self.versao))

    @property
    def pin16(self):
        b = self.bloco_diario
        if b is None or not b.pin16:
            raise FalhaLeitura("sha16 de %s não achado no diário" % self.versao)
        return b.pin16

    @property
    def pin_completo(self):
        """sha256 inteiro: só existe no selo corrente ou no cofre da versão (nunca digitado)."""
        def f():
            if self.corrente:
                return self.selo_nos["sha256"]["um.py"]
            m = self.c.cofre(self.versao) / "CUSTODY_MANIFEST.json"
            if m.is_file():
                return util.ler_json(m).get("um_py_pin")
            return None
        return self.memo("pin", f)

    @property
    def selo_espelho(self):
        return self.memo("selo_esp", lambda: util.ler_json(self.c.ESP / "um_absoluto_selo.json"))

    @property
    def rel_espelho(self):
        """'igual' | 'atras' | 'adiante': a versão do selo do espelho contra N (custódia pendente / em dia / histórica)."""
        sv = self.selo_espelho.get("um_version")
        a, b = util.versao_num(sv), self.n
        return "igual" if a == b else ("atras" if a < b else "adiante")

    @property
    def anterior_espelho(self):
        if self._anterior_forcado:
            return self._anterior_forcado
        return self.memo("ant_esp", lambda: nos.anterior_no_espelho(self.c, self.versao))

    @property
    def anterior_cofre(self):
        if self._anterior_forcado:
            return self._anterior_forcado
        from . import fatos as _f
        return self.memo("ant_cofre", lambda: _f.cofre_anterior(self.c, self.versao))

    @property
    def handoff(self):
        return self.memo("handoff", lambda: nos.ler_handoff(self.c, self.versao))

    @property
    def fatos(self):
        from . import fatos as _f
        return self.memo("fatos", lambda: _f.sondar(self.c, self.versao, anterior=self._anterior_forcado, handoff=self.handoff))

    # ---- pastas de trabalho
    @property
    def ddmes(self):
        meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
        dd, mm, _ = self.data.split("/")
        return "%02d%s" % (int(dd), meses[int(mm) - 1])

    @property
    def W(self):
        """work\\custodia_vNNN_<ddmes>\\ : a pasta da versão (a que já existe, se houver; senão a de hoje)."""
        def f():
            if self._trabalho is not None:
                return self._trabalho
            ex = self.c.pastas_trabalho_existentes(self.versao)
            return ex[-1] if ex else self.c.pasta_trabalho(self.versao, self.ddmes)
        return self.memo("W", f)

    @property
    def saida(self):
        """Onde as saídas só de leitura (sondar, plano) podem ser gravadas: --saida, ou work\\custodia_vNNN_<data>."""
        return self._saida or self.c.pasta_trabalho(self.versao, self.ddmes)

    def trabalho_da_versao(self, nome):
        """Caminho de um arquivo da pasta de trabalho da versão (procura nas pastas existentes)."""
        for p in reversed(self.c.pastas_trabalho_existentes(self.versao)):
            if (p / nome).is_file():
                return p / nome
        return None

    def aviso(self, msg):
        self.avisos.append(msg)

    def limpar(self):
        """Esquece o que foi lido (texto, JSON e memos de estado) — depois de um passo escrever, as marcas leem o disco de novo.
        Os recibos gravados nesta execução (memo `recibo_*`) ficam: valem de imediato e também estão no disco."""
        self._cache_t.clear()
        self._cache_j.clear()
        for k in [k for k in self._memo if not k.startswith("recibo_")]:
            self._memo.pop(k, None)


# =================================================================== a marca, com a falha de leitura SEMPRE à vista
def marca_de(ctx, p):
    """A marca de `p`. Exceção vira INDETERMINADO com o motivo (FalhaLeitura leva leitura=True: `executar` não aplica às cegas)."""
    if getattr(p, "usa_quadro", False) and ctx.pode_remedir:
        from . import quadro
        quadro.garantir_fresco(ctx, p)               # remede o quadro velho ANTES de decidir por ele (pode Parar: a falha da medida é visível)
    try:
        return p.ja(ctx)
    except FalhaLeitura as e:
        return indeterminado("FalhaLeitura: %s" % e.motivo, leitura=True)
    except G1Erro as e:
        return indeterminado("%s: %s" % (type(e).__name__, e.motivo))
    except Exception as e:  # noqa: BLE001
        return indeterminado("erro ao ler a marca: %r" % (e,), leitura=True)


def _pre_de(ctx, p):
    """(falhas, leitura): as falhas da pré-condição de `p`, sem levantar. leitura=True se foi falha de LEITURA (não de insumo)."""
    try:
        return list(p.pre(ctx) or []), False
    except FalhaLeitura as e:
        return ["FalhaLeitura: %s" % e.motivo], True
    except G1Erro as e:
        return ["%s: %s" % (type(e).__name__, e.motivo)] + list(e.faltam), False
    except Exception as e:  # noqa: BLE001
        return ["erro ao avaliar a pré-condição: %r" % (e,)], True


# =================================================================== plano
def montar_plano(ctx):
    """Todos os passos das quatro pernas, na ORDEM de execução (fase A: local; fase B: depois do espelho publicado)."""
    from . import central, espelho, publica, quadro, site
    passos = []
    passos += espelho.passos_fase_a(ctx)       # E00..E09
    passos += central.passos_fase_a(ctx)       # C1, C3..C12 (C5 em segundo plano)
    passos += espelho.passos_fase_b(ctx)       # E10..E12
    passos += site.passos(ctx)                 # E13..E19
    passos += central.passos_fase_b(ctx)       # C2, C13..C17
    passos += publica.passos(ctx)              # C18
    passos += quadro.passos(ctx)               # C19, C20
    return passos


def avaliar(ctx, passos, so=None, ate=None, com_pre=True):
    """[(Passo, Marca)] — só leitura. Exceção numa marca vira INDETERMINADO com o motivo (falha de leitura é visível).
    Com `com_pre`, a PRÉ-CONDIÇÃO do primeiro passo pendente (o que `executar` tentaria agora; com --so, de cada selecionado) também é
    avaliada: se falha, o passo vira BLOQUEADO com o motivo — o plano deixa de listar como «falta» o que `executar` não alcança."""
    sel = _selecionar(passos, so, ate)
    out = []
    primeiro = True
    for p in sel:
        m = marca_de(ctx, p)
        if com_pre and p.pre and not m.satisfeita and m.estado != "BLOQUEADO" and (primeiro or so):
            f, leit = _pre_de(ctx, p)
            if f:
                m = (indeterminado("pré-condição ilegível: " + "; ".join(f)[:500], leitura=True) if leit
                     else bloqueado("pré-condição de executar: " + "; ".join(f)[:700] + " | marca: " + m.detalhe[:160]))
        if not m.satisfeita:
            primeiro = False
        out.append((p, m))
    return out


def _selecionar(passos, so, ate):
    ids = [p.id for p in passos]
    if so:
        pedidos = [s.strip().upper() for s in (so.split(",") if isinstance(so, str) else so)]
        for s in pedidos:
            if s not in ids:
                raise Parar("passo desconhecido: %s (existentes: %s)" % (s, ", ".join(ids)))
        return [p for p in passos if p.id in pedidos]
    if ate:
        a = ate.strip().upper()
        if a not in ids:
            raise Parar("passo desconhecido em --ate: %s" % ate)
        return passos[: ids.index(a) + 1]
    return passos


def resumo(avaliacao):
    cont = {}
    for _, m in avaliacao:
        cont[m.estado] = cont.get(m.estado, 0) + 1
    pendentes = [(p, m) for p, m in avaliacao if not m.satisfeita]
    return {"contagem": cont, "pendentes": [p.id for p, _ in pendentes], "nada_a_fazer": not pendentes,
            "bloqueados": [p.id for p, m in pendentes if m.estado == "BLOQUEADO"],
            "falha_de_leitura": [p.id for p, m in avaliacao if m.leitura],
            "superados_por_relacao": [p.id for p, m in avaliacao if m.estado == "SUPERADO_REL"],
            "provado_no_artefato": not pendentes and not any(m.estado in ("SUPERADO_REL", "OPERADOR") for _, m in avaliacao)}


def decisoes_do_operador(ctx, av=None, plano_real=True):
    """As decisões que G1 NÃO toma e que continuam abertas: passos marcados OPERADOR, as «Pendências SÓ do operador» do handoff (verbatim) e os
    itens do quadro que são do operador (app, Zenodo, painel da hospedagem). Cada uma com a ORIGEM. Nenhuma é ato de G1."""
    out = []
    for p, m in (av or []):
        if m.estado == "OPERADOR":
            out.append({"origem": p.id, "texto": m.detalhe})
    if not plano_real:
        return out
    h = ctx.handoff
    par = h.secao("Pendências SÓ do operador") if h else None
    if par:
        out.append({"origem": "handoff (verbatim)", "texto": re.sub(r"^\*\*[^*]+\*\*\s*", "", par).replace("\n", " ").strip(),
                    "nota": "o que o handoff lista como ato de custódia (a custódia, subir o site, commit/push) está nos passos de G1; G1 não sabe se as decisões já foram tomadas"})
    if ctx.corrente:
        from . import quadro
        out += quadro.itens_do_operador(ctx)
    return out


def planejar(ctx, so=None, ate=None):
    """O plano: cada passo com a marca e o que FALTA. Lê o mundo; não escreve nada."""
    ctx.leitura = True
    try:
        passos = montar_plano(ctx)
        av = avaliar(ctx, passos, so, ate)
    finally:
        ctx.leitura = False
    r = resumo(av)
    itens = [{"id": p.id, "perna": p.perna, "passo": p.nome, "estado": m.estado, "detalhe": m.detalhe, "externo": p.externo,
              "escreve": p.escreve, "provada": m.provada, "leitura": m.leitura} for p, m in av]
    # textos: só o que ainda falta precisa de fonte (se o passo já foi aplicado, a prosa não é mais necessária)
    r.update({"versao": ctx.versao, "corrente": ctx.corrente, "relacao_espelho": ctx.rel_espelho, "itens": itens,
              "pendentes_do_operador": [{"id": p.id, "detalhe": m.detalhe} for p, m in av if m.estado == "OPERADOR"]})
    decs = decisoes_do_operador(ctx, av, plano_real=True)
    r["decisoes_do_operador"] = decs
    r["completo"] = r["nada_a_fazer"] and not decs
    pend = [(p, m) for p, m in av if not m.satisfeita]
    if pend and pend[0][1].estado == "BLOQUEADO":
        r["executar_para_em"] = {"id": pend[0][0].id, "motivo": pend[0][1].detalhe}
        r["atras_do_bloqueio"] = [p.id for p, _ in pend[1:]]
    else:
        r["executar_para_em"], r["atras_do_bloqueio"] = None, []
    pend_ids = set(r["pendentes"])
    if pend_ids:
        from . import textos
        r["textos"] = textos.avaliar_fontes(ctx, pend_ids)
        r["texto_bloqueia"] = bool(r["textos"]["bloqueia"])
    else:
        r["texto_bloqueia"] = False
    return r


def codigo_do_plano(p):
    """O código de saída do plano: 30 leitura > 20 STOP (bloqueio ou texto sem fonte) > 1 pendente > 5 decisões do operador abertas > 0."""
    if p.get("falha_de_leitura"):
        return util.COD_LEITURA
    if p.get("bloqueados") or p.get("texto_bloqueia"):
        return util.COD_STOP
    if not p["nada_a_fazer"]:
        return util.COD_PENDENTE
    if p.get("decisoes_do_operador"):
        return util.COD_OPERADOR
    return util.COD_OK


# =================================================================== trava (uma por versão)
class Trava:
    """work\\custodia_G1\\runs\\<vNNN>.lock com {pid, versao, inicio}. Trava de processo vivo e recente: WAIT. Trava de processo
    morto: é renomeada (nunca apagada, nunca se mata processo por nome) e a execução segue."""

    def __init__(self, ctx):
        self.p = ctx.c.RUNS / ("%s.lock" % ctx.versao)
        self.ctx = ctx

    @staticmethod
    def _vivo(pid):
        try:
            if os.name == "nt":
                r = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid, "/NH", "/FO", "CSV"], capture_output=True, timeout=20)   # saída em OEM (cp850): bytes, nunca texto estrito
                return ('"%d"' % pid) in r.stdout.decode("utf-8", "replace")
            os.kill(pid, 0)
            return True
        except Exception:  # noqa: BLE001
            return False

    def __enter__(self):
        self.p.parent.mkdir(parents=True, exist_ok=True)
        if self.p.exists():
            try:
                d = json.loads(self.p.read_text(encoding="utf-8"))
            except ValueError:
                d = {}
            pid = int(d.get("pid") or 0)
            if pid and self._vivo(pid):                  # processo vivo (inclusive este: a reentrada na mesma trava é erro de uso)
                raise Esperar("custódia de %s em curso (pid %s desde %s): uma trava por versão" % (self.ctx.versao, pid, d.get("inicio")))
            velha = self.p.with_name(self.p.name + ".velha_" + util.carimbo())
            os.replace(self.p, velha)
            self.ctx.aviso("trava velha (processo %s morto) renomeada para %s" % (pid, velha.name))
        self.p.write_text(json.dumps({"pid": os.getpid(), "versao": self.ctx.versao, "inicio": util.agora_iso()}), encoding="utf-8")
        return self

    def __exit__(self, *a):
        try:
            self.p.unlink()
        except OSError:
            pass


# =================================================================== execução
def executar(ctx, so=None, ate=None, imprimir=print, passos=None):
    """Roda o plano na ordem. Devolve (codigo_de_saida, relatorio). Gates: o primeiro que falha PARA a execução.
    `passos` (opcional) injeta uma lista de passos (testes do motor); o padrão é o plano das quatro pernas.
    `--ensaio` NÃO grava nada: nem recibo, nem RELATORIO.json, nem trava (o relatório do ensaio vai só ao console e ao valor devolvido)."""
    plano_real = passos is None
    passos = _selecionar(passos if passos is not None else montar_plano(ctx), so, ate)
    carimbo = util.carimbo()
    if not ctx.ensaio:
        ctx.run_dir = ctx.run_dir or (ctx.c.RUNS / ("%s_%s" % (ctx.versao, carimbo)))
    ctx.pode_remedir = not ctx.ensaio
    rel = {"versao": ctx.versao, "inicio": util.agora_iso(), "publicar": ctx.publicar, "ensaio": ctx.ensaio, "passos": [], "avisos": ctx.avisos}
    codigo = util.COD_OK
    trava = None
    try:
        if not ctx.ensaio:
            trava = Trava(ctx).__enter__()
        if passos_reais(passos) and (ctx.corrente or ctx.rel_espelho == "atras"):
            nos.exigir_pronta(ctx.c, ctx.versao)
        for i, p in enumerate(passos):
            t0 = time.time()
            m = marca_de(ctx, p)
            reg = {"id": p.id, "passo": p.nome, "marca": m.estado, "detalhe": m.detalhe}
            if m.estado == "OPERADOR":
                reg["resultado"] = "PENDENTE_OPERADOR"
                rel["passos"].append(reg)
                imprimir("  [%s] %-34s PENDENTE DO OPERADOR/GERÊNCIA (não é do G1) — %s" % (p.id, p.nome, m.detalhe[:160]))
                continue
            if m.satisfeita:
                reg["resultado"] = "PULADO_JA_APLICADO"
                rel["passos"].append(reg)
                imprimir("  [%s] %-34s já aplicado (%s) — %s" % (p.id, p.nome, m.estado, m.detalhe[:90]))
                continue
            if m.leitura:
                raise FalhaLeitura("a marca de %s não pôde ser lida (G1 não aplica às cegas): %s" % (p.id, m.detalhe), [m.detalhe])
            if p.externo and not ctx.publicar:
                reg["resultado"] = "PARADO_FALTA_PUBLICAR"
                rel["passos"].append(reg)
                imprimir("  [%s] %-34s PRONTO PARA PUBLICAR — passe --publicar para praticar este ato para fora" % (p.id, p.nome))
                codigo = util.COD_PENDENTE
                break
            if m.estado == "BLOQUEADO":
                raise Parar("passo %s bloqueado: %s" % (p.id, m.detalhe), [m.detalhe])
            if p.pre:
                f = p.pre(ctx)
                if f:
                    raise Parar("pré-condição de %s falhou" % p.id, f)
            if ctx.ensaio:
                reg["resultado"] = "ENSAIO_NADA_GRAVADO"
                reg["escreveria"] = p.escreve
                rel["passos"].append(reg)
                imprimir("  [%s] %-34s ENSAIO — faria: %s" % (p.id, p.nome, p.escreve[:100]))
                continue
            imprimir("  [%s] %-34s aplicando…" % (p.id, p.nome))
            if p.aplicar is None:
                raise Parar("passo %s sem aplicador" % p.id, [m.detalhe])
            saida = p.aplicar(ctx) or {}
            if p.conferir:
                f = p.conferir(ctx)
                if f:
                    raise Parar("conferência de %s falhou (nada prossegue)" % p.id, f)
            # a marca de «já aplicado» é o critério de idempotência: depois de aplicar+conferir ela tem de virar. FALTA explícita = o passo não fez o que diz.
            ctx.limpar()
            m2 = marca_de(ctx, p)
            if m2.estado == "FALTA":
                raise Parar("depois de aplicar, a marca de %s continua FALTA: %s" % (p.id, m2.detalhe), [m2.detalhe])
            if not m2.satisfeita:
                ctx.aviso("a marca de %s ficou %s depois de aplicar (%s)" % (p.id, m2.estado, m2.detalhe[:100]))
            reg.update({"resultado": "APLICADO", "segundos": round(time.time() - t0, 1), "saida": saida, "marca_depois": m2.estado})
            rel["passos"].append(reg)
            _gravar_recibo(ctx, i, p, reg)
            imprimir("  [%s] %-34s ok (%.1fs)" % (p.id, p.nome, time.time() - t0))
        if codigo == util.COD_OK:
            decs = decisoes_do_operador(ctx, [(p, Marca(r["marca"], r.get("detalhe", ""))) for p, r in zip(passos, rel["passos"]) if r.get("resultado") == "PENDENTE_OPERADOR"],
                                        plano_real=plano_real)
            rel["decisoes_do_operador"] = decs
            if decs:
                codigo = util.COD_OPERADOR
                imprimir("G1 terminou o que lhe cabe; %d decisão(ões) do OPERADOR abertas (código %d):" % (len(decs), codigo))
                for d in decs:
                    imprimir("   - [%s] %s" % (d["origem"], d["texto"][:240]))
    except G1Erro as e:
        codigo = e.codigo
        rel["parou"] = {"tipo": type(e).__name__, "motivo": e.motivo, "faltam": e.faltam}
        imprimir("PAROU (%s): %s" % (type(e).__name__, e.motivo))
        for x in e.faltam:
            imprimir("   - %s" % x)
    finally:
        if trava:
            trava.__exit__()
        rel["fim"] = util.agora_iso()
        rel["codigo"] = codigo
        if not ctx.ensaio:
            try:
                ctx.run_dir.mkdir(parents=True, exist_ok=True)
                (ctx.run_dir / "RELATORIO.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
            except OSError:
                pass
    return codigo, rel


def passos_reais(passos):
    return any(getattr(p, "perna", 0) in (1, 2, 3, 4) and p.id[:1] in "EC" for p in passos)


def _gravar_recibo(ctx, i, p, reg):
    d = ctx.run_dir
    d.mkdir(parents=True, exist_ok=True)
    (d / ("%02d_%s.json" % (i, p.id))).write_text(json.dumps(dict(reg, versao=ctx.versao, fim=util.agora_iso()), ensure_ascii=False, indent=1, default=str),
                                                  encoding="utf-8")

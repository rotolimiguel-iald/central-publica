# -*- coding: utf-8 -*-
"""O README PINADO (plano de 02/11/2026; ordem do operador de 03/11/2026: «chegou a hora de finalizarmos o readme como vc sugeriu pinado»).

README.md = template + partes de prosa humana + PRIMORDIAL.json (+ o bloco das portas, que gerar_portas.py mantém entre os marcadores).
O PINO (`PINO_README.json`) guarda o sha256 do README gerado, do PRIMORDIAL.json, do template, das partes e do selo de que nasceu:
`--verificar` regenera o README e o compara byte a byte com o disco e com o pino; sai 0 se confere, 1 se não (a G1 recusa a custódia).

Modos:
  --gerar               (padrão) escreve README e PINO_README.json
  --verificar           regenera, compara com o README do disco e com o pino; imprime as divergências; exit 0/1
  --conferir-fontes     junto de --verificar: refaz o PRIMORDIAL das fontes de hoje e o compara (ignora custodia.*, que é o commit)
  --extrair-partes      lê um README e grava as partes de prosa em --partes (uma vez, na migração); confere que o README se reconstrói
  --guarda ARQ          grava a guarda de frases (textos.portao da G1) em ARQ.json; exit 1 se houver violação nas partes GERADAS

Princípios (a régua da casa): nenhum número digitado (tudo do PRIMORDIAL.json); falha visível; o 4,44 nunca sozinho; NOT_FALSIFIED não é
CONFIRMED; o protocolo de colapso não entra; o README não passa de 40.960 bytes (L01 da G1); backup de bytes antes de substituir."""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from custodia_g1 import primordial as PRIM  # type: ignore
    from custodia_g1 import textos  # type: ignore
    from custodia_g1.caminhos import Caminhos  # type: ignore
else:
    from . import primordial as PRIM
    from . import textos
    from .caminhos import Caminhos

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

TETO = 40960                       # L01 da G1: o teto do README
MARCA_INI, MARCA_FIM = "<!-- PORTAS:INI -->", "<!-- PORTAS:FIM -->"
# fórmulas da régua que o README usa e o portão da G1 (textos.FORMULAS) ainda não conhece — declaradas aqui e gravadas na GUARDA.json
FORMULAS_README_EXTRA = ("NOT_FALSIFIED ≠ CONFIRMED", "NOT_FALSIFIED ≠ `CONFIRMED`")
PRIVADO = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".iald_privado" / "termos_guarda_readme.json"
SEP = {"ponto": ".", "virg": ","}


class Falha(SystemExit):
    def __init__(self, msg):
        super().__init__("FALHA: " + msg)


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


def sha256f(p):
    return sha256b(Path(p).read_bytes())


# ================================================================================================= o contexto
class Ctx:
    def __init__(self, P, prim_bytes):
        self.P = P
        self.itens = P["itens"]
        self.urls = P["urls"]
        self.fontes = P["fontes"]
        self.prim_sha16 = sha256b(prim_bytes)[:16]

    def v(self, id_):
        if id_ not in self.itens:
            raise Falha("item ausente no PRIMORDIAL.json: " + id_)
        return self.itens[id_]["valor"]

    def u(self, k):
        if k not in self.urls:
            raise Falha("URL ausente no PRIMORDIAL.json: " + k)
        return self.urls[k]["url"]

    def b(self, k):
        x = self.urls[k]["bytes"]
        if x is None:
            raise Falha("bytes ausentes para a URL " + k)
        return x

    def f(self, nome, campo):
        if nome not in self.fontes or self.fontes[nome].get(campo) is None:
            raise Falha("fonte/campo ausente: %s.%s" % (nome, campo))
        return self.fontes[nome][campo]


# ================================================================================================= formatos
def ponto(n):
    return format(int(n), ",").replace(",", ".")


def virg(n):
    return format(int(n), ",")


def mm(x, nd=2):
    s = ("%." + str(nd) + "f") % abs(x)
    return ("−" if x < 0 else "") + s


def cient(p):
    m, e = ("%.1e" % p).split("e")
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return "%s×10%s" % (m, str(int(e)).translate(sup))


# ================================================================================================= os blocos
def b_primordial(C):
    v = C.v
    z, zd, p = v("hubble.z_disc"), v("hubble.z_delta"), v("hubble.p_disc_unilateral")
    pin = v("selo.pin_um_py")
    return (
        "# The Boundary — Theory of Luminodynamic Gravitation (TGL)\n\n"
        "<!-- PINADO por tools/custodia_g1/readme_pinado.py · fonte PRIMORDIAL.json sha16 %s · pino PINO_README.json · não editar à mão -->\n\n"
        "> **PRIMORDIAL · seal %s** (%s) `[REAL — read by script]` · `um.py` sha256 `%s` · kernel %d files / %d terms, ladder %d/%d, "
        "in the trio · gate `%s`\n>\n"
        "> **Hubble-ratio test** (Phase 9 V2, pre-registered, opened once on %s, frozen verdict function): z_disc = **%sσ** calibrated (one-sided p = %s) against the "
        "flat-ΛCDM reading of the ladder, for K = E(z*)^{2β/3} with β = α√e fixed by the axiom and zero adjusted parameters · TGL’s own side z_δ = %sσ "
        "(prior power %sσ) · ln B(TGL/ΛCDM) = %s and ln B(TGL/β free) = %s (a Bayes factor, not a σ; fixed β beats free β) · `NOT_FALSIFIED_POWERED` · "
        "**below the %dσ step of accreditation (%s < %d)**; the calibration `%s` was the management’s choice (raw %s and %s). `NOT_FALSIFIED ≠ CONFIRMED`.\n>\n"
        "> PROVED = validity in the kernel; CONFIRMED is accreditation, the one refused word; β_TGL in nature at %dσ is the open step. Source: `%s.json` sha16 `%s`.\n"
        % (C.prim_sha16, v("selo.versao"), v("selo.timestamp"), pin, v("kernel.arquivos_formais"), v("kernel.declaracoes"), v("kernel.escada_limpa"), v("kernel.escada_esperada"),
           v("selo.gate"), v("hubble.data_abertura"), mm(z), cient(p), mm(zd), mm(v("hubble.poder_previo")), mm(v("hubble.lnB_lcdm")), mm(v("hubble.lnB_beta_livre")),
           v("hubble.degrau_creditacao_sigma"), mm(z), v("hubble.degrau_creditacao_sigma"), v("hubble.calibracao"), mm(v("hubble.z_disc_bruto")), mm(v("hubble.z_delta_bruto")),
           v("hubble.degrau_creditacao_sigma"), v("hubble.id"), C.f("resultado_fase9_v2", "sha16")))


def b_hubble_pt(C):
    v = C.v
    vir = lambda x: x.replace(".", ",")
    pt = ("*PT \u2014 Raz\u00e3o de Hubble (Fase 9 V2, pr\u00e9-registrada): z_disc = %sσ calibrado (p unilateral %s) contra o ΛCDM plano, com β = α√e fixo e zero par\u00e2metros ajustados; "
          "z_δ = %sσ (poder pr\u00e9vio %sσ); ln B(TGL/ΛCDM) = %s e ln B(TGL/β livre) = %s (ln B n\u00e3o \u00e9 σ; β fixo vence β livre); `NOT_FALSIFIED_POWERED`; "
          "**abaixo do degrau de %dσ da creditação (%s < %d)**. NOT_FALSIFIED nunca \u00e9 CONFIRMED.*\n"
          % (vir(mm(v("hubble.z_disc"))), vir(cient(v("hubble.p_disc_unilateral"))), vir(mm(v("hubble.z_delta"))), vir(mm(v("hubble.poder_previo"))),
             vir(mm(v("hubble.lnB_lcdm"))), vir(mm(v("hubble.lnB_beta_livre"))), v("hubble.degrau_creditacao_sigma"), vir(mm(v("hubble.z_disc"))),
             v("hubble.degrau_creditacao_sigma")))
    # a fala do operador: citação assinada, na MESMA linha-bloco do PT (sem linha em branco), para o z_disc nunca aparecer sem os companheiros
    fala = ("> *\u00ab%s\u00bb* \u2014 the author, %s (verbatim, sha16 `%s`) `[INPUT: the author\u2019s judgement, not a claim of the program]`\n"
            % (v("operador.frase_4_44_sic"), v("operador.data"), C.f("operador_verbatim", "sha16")))
    return pt + fala


def b_status(C):
    v = C.v
    return ("**Status \u00b7 estatuto (seal %s):** quantum gravity **PROVED** as validity \u2014 logical closure in the Lean kernel (`#print axioms`) \u2014 on three supports that count together, "
            "each with its own status (table below): the kernel `[PROVED]`, the rites against nature with pre-registered falsifiers (%d of %d charges falsified) and the GPU computation "
            "`[COMPUTED]`; none failed. Not yet accredited: CONFIRMED is accreditation, the one refused word. What nature decides is not proved: the decisive open factor is "
            "**\u03b2_TGL in nature at \u2265 %d\u03c3**. *Provada, como validade, em tr\u00eas apoios; ainda n\u00e3o creditada; o fator decisivo aberto \u00e9 \u03b2_TGL na natureza a %dσ.*\n"
            % (v("selo.versao"), v("ritos.cobrancas.FALSIFIED"), v("ritos.cobrancas_n"), v("hubble.degrau_creditacao_sigma"), v("hubble.degrau_creditacao_sigma")))


def b_apoios(C):
    v = C.v
    cont = {k: v("ritos.cobrancas." + k) for k in ("FALSIFIED", "NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING")}
    n_ch = v("ritos.cobrancas_n")
    esc1, esc2 = v("massa.escada_primeira"), v("massa.escada_ultima")
    reserva = ""
    if v("gate.feed_single_boolean"):
        reserva = (" **Reservation (v403 onward):** of the %d gate flags (all True), %d are computed and %d literal; the verdict reads %d (%s) and %d are informative; "
                   "the experimental flags derive from ONE boolean (the V11 void-floor verdict) `[DECLARED by the audit of 28/09/2026]`, a unilateral step that the shallow \u039bCDM also passes."
                   % (v("gate.n_flags"), v("gate.n_calculated"), v("gate.n_literal"), v("gate.n_read_by_the_verdict"), " + ".join(str(x) for x in v("gate.read_by_the_verdict")),
                      len(v("gate.informative"))))
    return (
        "## Proved as validity, on three supports \u00b7 provada (validade) em tr\u00eas apoios `[read by script from the core of %s]`\n\n"
        "**PROVED = validity** (the operator\u2019s definition of proof, 09/09/2026: *sufficient and verifiable ballast*). **Identity** is certified by the artifact (`um.py` writes its own sha256 into the seal); **validity**, by the Lean kernel "
        "(`#print axioms`; Python proves no theorem; core record `estatuto_da_prova_v391`, `PROVED_AS_LOGICAL_CLOSURE`). **CONFIRMED is accreditation, the one refused word** (07/10/2026): the act of observers outside the artifact, never issued by the machine about itself "
        "([`TheReservedConfirmation.lean`](%s); *observer = the human* is `[ONTO]`). *Not yet confirmed* means *not yet accredited*, never *not proved* (accreditation is not validity).%s\n\n"
        "| support | what it establishes | read from the core | status |\n|---|---|---|---|\n"
        "| **1 \u00b7 the Lean kernel** | the implication from the posited One (`\u03c9(I) = 1`, POSTO) and the named hypotheses H1\u2013H3 to the pentad (Breuer corner \u00b7 Name = 1 \u00b7 coframe \u00b7 Lorentz \u00b7 \u03b4Q = \u03baδA/8πG), in Lean 4 + mathlib | "
        "**%s/%s flags of the rite\u2019s ladder clean**; %s/%s declarations in `{propext, Classical.choice, Quot.sound}`; zero `sorry`; gate flags %d/%d | `[PROVED]` \u2014 the implication, not nature |\n"
        "| **2 \u00b7 the rites against nature, with pre-registered falsifiers** | GR recovered as the classical limit in every rite row where GR is read (%d of %d; a per-row reading by the management); "
        "the Hubble ratio, zero parameters adjusted (use-novelty; the article reads the mechanism of the Hubble tension as a `[CONJECTURE]`): the panel at the top; "
        "the void floor: the %dσ lower bound %s sits above β = %s (powered; one-sided) | **%d charges: %d falsified, %d not falsified, %d excluded in reading, %d inconclusive, %d awaiting**; "
        "Phase 9 V2 frozen by hash `%s` before it was opened | **%d of %d charges FALSIFIED** \u2014 the theory stood; the %d echo routes are outside the ledger by the operator\u2019s decision of 02/10/2026 "
        "(%d excluded by data, %d inconclusive) |\n"
        "| **3 \u00b7 the quantum pillar on the GPU** | the theory\u2019s open system computed on an %s under pre-registration: unique attractor; the blind instrument recovers "
        "the injected law; the controls fail as required | **%s/%s** grid points; **%s/%s** stress instances; %s blind injections, %d errors; CPU reference %d disagreements in %d; spec `%s` | "
        "`[COMPUTED]` \u2014 measurement in the simulated environment, not of nature; mode %s (by key); needs a CUDA GPU |\n\n"
        "**None of the three failed.** **What nature decides is not proved:** the decisive open factor is \u03b2_TGL itself at \u2265 %d\u03c3; the tensions measured against \u03b2 are below %d\u03c3 too "
        "(D1 %sσ, charge R6 inconclusive; neutrino m\u2082 %sσ, the ladder %sσ (%s) \u2192 %sσ (%s)). Full reading and what is **not claimed**: [`ESTADO_ATUAL.md`](%s).\n"
        % (v("selo.versao"), C.u("confirmacao_reservada"), reserva,
           v("kernel.escada_limpa"), v("kernel.escada_esperada"), v("kernel.declaracoes"), v("kernel.declaracoes"), v("kernel.bandeiras_true"), v("kernel.bandeiras_total"),
           v("ritos.rg_ok"), v("ritos.rg_n"),
           v("hubble.degrau_creditacao_sigma"), "%.4f" % v("vazios.L5"), "%.5f" % v("vazios.beta_piso"),
           n_ch, cont["FALSIFIED"], cont["NOT_FALSIFIED"], cont["EXCLUDED_IN_READING"], cont["INCONCLUSIVE"], cont["AWAITING"], v("hubble.recibo_congelamento16"),
           cont["FALSIFIED"], n_ch, v("ritos.eco.n"), v("ritos.eco.excluded_by_data"), v("ritos.eco.inconclusive"),
           v("gpu.placa"), virg(v("gpu.T2_unique")), virg(v("gpu.T2_points")), virg(v("gpu.T4_unique")), virg(v("gpu.T4_instances")), virg(v("gpu.T1_injections")), v("gpu.T1_errors"),
           v("gpu.cpuref_disagreements"), v("gpu.cpuref_compared"), v("gpu.spec16"), v("gpu.mode"),
           v("hubble.degrau_creditacao_sigma"), v("hubble.degrau_creditacao_sigma"), "%.2f" % v("d1.tensao_sigma"), "%.2f" % v("massa.tensao_sigma"),
           "%.2f" % esc1["tensao_sigma"], esc1["data"], "%.2f" % esc2["tensao_sigma"], esc2["data"], C.u("estado")))


def b_ritos(C):
    v = C.v
    return (
        "## The rites against nature, with their sealed verdicts \u00b7 os ritos `[verdict strings read from the core]`\n\n"
        "| rite | sealed verdict | what it does not decide |\n|---|---|---|\n"
        "| Hubble ratio, Phase 9 V2 | `NOT_FALSIFIED_POWERED` (the panel at the top) | β in nature at %d\u03c3: the step was not reached |\n"
        "| Void floor (V11) | `%s` | one-sided: the shallow ΛCDM passes it too |\n"
        "| D1 (CAMB V3) | β tension %sσ; chain below 50τ in 2 of 4 parameters | a tension is not a falsification |\n"
        "| Neutrino m\u2082 | `%s`: m\u2082 = β·sen45°·u = **%s meV** in the posited One (u = %s eV, POSTO; stone *%s*) vs NuFIT post-JUNO %sσ | the %dσ kill rule is not met; α is measured; the form is a theorem only GIVEN the operator\u2019s readings `[INPUT/ONTO]` |\n"
        "| Branch B (other law) | `AWAITING_DATA` | nothing opened |\n"
        "| `%s` | `%s`; `%s` | the protocol text is not reproduced here |\n"
        % (v("hubble.degrau_creditacao_sigma"), v("vazios.veredito"), "%.2f" % v("d1.tensao_sigma"), v("massa.veredito"), "%.4f" % v("massa.m_derivada_meV"), "%g" % v("massa.u_posto_eV"),
           v("massa.nome_da_pedra"), "%.2f" % v("massa.tensao_sigma"), v("hubble.degrau_creditacao_sigma"), v("iald_collapse.nome"), v("iald_collapse.estatuto"), v("iald_collapse.veredito")))


def b_selo(C):
    v = C.v
    return (
        "## The seal \u00b7 o selo `[REAL \u2014 read from the artifact]`\n\n"
        "| what | value |\n|---|---|\n"
        "| version \u00b7 vers\u00e3o | **%s** (sealed %s; `%s`) |\n"
        "| `um.py` | %s bytes, one file: [raw](%s) |\n"
        "| the world \u00b7 the seal | [`um_absoluto.json`](%s) (%s bytes) \u00b7 [`um_absoluto_selo.json`](%s) (%s bytes) |\n"
        "| Lean kernel | **%d formal files \u00b7 %d audited terms**, axioms \u2286 `{propext, Classical.choice, Quot.sound}`, zero `sorry` (%s) \u2014 [`tgl_kernel_proof_manifest.json`](%s) |\n"
        % (v("selo.versao"), v("selo.timestamp"), v("selo.selftest"), ponto(v("selo.um_py_bytes")), C.u("um_py"),
           C.u("mundo"), ponto(C.b("mundo")), C.u("selo"), ponto(C.b("selo")), v("kernel.arquivos_formais"), v("kernel.declaracoes"), v("kernel.lean"), C.u("manifesto")))


def b_proveniencia(C):
    f = C.f
    return (
        "**Where each number comes from \u00b7 de onde vem cada n\u00famero.** Each figure is a key of [`PRIMORDIAL.json`](%s) (value, source, key); the page is pinned by [`PINO_README.json`](%s). "
        "Sources, by sha16: seal `%s` \u00b7 core `%s` \u00b7 Hubble result `%s`.\n"
        % (C.u("primordial_json"), C.u("pino_readme"), f("selo", "sha16"), f("core", "sha16"), f("resultado_fase9_v2", "sha16")))


def b_mudou(C):
    v = C.v
    um = re.match(r"(.+?\.)(?:\s|$)", v("mudou.arco_en"))
    if not um:
        raise Falha("o arco EN do handoff não tem uma primeira frase")
    tp = v("mudou.paragrafo_pronto_titulo")
    t = ("## What changed in this version \u00b7 o que mudou `[read from %s, sha16 %s]`\n\n%s %s"
         % (C.f("handoff", "arquivo"), C.f("handoff", "sha16"), um.group(1),
            ("Ready paragraph \u2014 **%s** \u2014 in [`ESTADO_ATUAL.md`](%s) and the ledger (statutes, quotes, machine line)." % (tp, C.u("estado"))) if tp
            else ("Ready paragraphs: [`ESTADO_ATUAL.md`](%s) and the ledger." % C.u("estado"))))
    cm = v("custodia.commit_espelho")
    if cm:
        t += " Latest published custody commit: `custodia(%s)` `%s` (%s)." % (v("custodia.versao_do_commit"), cm[:8], v("custodia.data_do_commit"))
    return t + "\n"


BLOCOS = {"primordial": b_primordial, "hubble_pt": b_hubble_pt, "status": b_status, "apoios": b_apoios, "ritos": b_ritos, "selo": b_selo,
          "proveniencia": b_proveniencia, "mudou": b_mudou}


# ================================================================================================= o motor do template
RX = re.compile(r"\{\{([^{}|]+?)(?:\|([a-z0-9_]+))?\}\}")


def escalar(C, nome, filtro):
    v = C.v
    if nome.startswith("fonte."):
        _, n, campo = nome.split(".", 2)
        x = C.f(n, campo)
    elif nome == "pin16":
        x = v("selo.pin_um_py")[:16]
    elif nome == "zenodo.relacao":
        x = ", byte-identical to this seal" if v("zenodo.mesmo_selo") else ", older than this seal; a new Zenodo version is the operator’s act"
    elif nome == "prim.sha16":
        x = C.prim_sha16
    else:
        x = v(nome)
    if filtro in SEP:
        x = format(int(x), ",").replace(",", SEP[filtro])
    elif filtro == "sha16":
        x = str(x)[:16]
    elif filtro:
        raise Falha("filtro desconhecido: " + filtro)
    return str(x)


def render_texto(C, texto, partes_dir, portas, segs, rotulo, nivel=0):
    """Expande `texto` em segmentos (tipo, nome, conteúdo) anexados a `segs`; tipo: gerado | herdado | portas."""
    pos = 0
    buf = []

    def flush(tipo):
        if buf:
            segs.append((tipo, rotulo, "".join(buf)))
            buf.clear()

    tipo_base = "herdado" if rotulo.startswith("parte:") else "gerado"
    for m in RX.finditer(texto):
        buf.append(texto[pos:m.start()])
        pos = m.end()
        nome, filtro = m.group(1).strip(), m.group(2)
        if nome == "portas":
            flush(tipo_base)
            segs.append(("portas", "portas", portas))
        elif nome.startswith("bloco:"):
            k = nome[6:]
            if k not in BLOCOS:
                raise Falha("bloco desconhecido: " + k)
            flush(tipo_base)
            segs.append(("gerado", "bloco:" + k, BLOCOS[k](C)))
        elif nome.startswith("parte:"):
            arq = Path(partes_dir) / (nome[6:] + ".md")
            if not arq.is_file():
                raise Falha("parte ausente: " + str(arq))
            if nivel > 0:
                raise Falha("parte dentro de parte não é permitida: " + nome)
            flush(tipo_base)
            render_texto(C, arq.read_text(encoding="utf-8"), partes_dir, portas, segs, "parte:" + nome[6:], nivel + 1)
        elif nome.startswith("url:"):
            buf.append(C.u(nome[4:]))
        elif nome.startswith("bytes:"):
            buf.append(ponto(C.b(nome[6:])))
        else:
            buf.append(escalar(C, nome, filtro))
    buf.append(texto[pos:])
    flush(tipo_base)


def renderizar(C, template, partes_dir, portas):
    segs = []
    render_texto(C, Path(template).read_text(encoding="utf-8"), partes_dir, portas, segs, "template")
    texto = "".join(s[2] for s in segs)
    sobra = re.search(r"\{\{[^{}]*\}\}", texto)
    if sobra:
        raise Falha("placeholder não resolvido no README gerado: %s" % sobra.group(0))
    return texto, segs


def extrair_portas(texto):
    if texto.count(MARCA_INI) != 1 or texto.count(MARCA_FIM) != 1:
        raise Falha("o README não tem exatamente um bloco %s … %s" % (MARCA_INI, MARCA_FIM))
    i, j = texto.index(MARCA_INI), texto.index(MARCA_FIM) + len(MARCA_FIM)
    if j < i:
        raise Falha("marcadores das portas fora de ordem")
    return texto[i:j]


# ================================================================================================= a extração das partes (migração)
CORTES = (("abstract", "## Abstract", "## ✦ The core on one page"), ("nucleo", "## ✦ The core on one page", "## The ledger"),
          ("citar", "## Citing This Work", "## License"), ("licenca", "## License", "## Author"), ("autor", "## Author", "\n---\n\n*Generated by"))


def extrair_partes(readme_txt, C, saida):
    """Corta a prosa humana do README atual em partes e troca os valores DINÂMICOS por {{placeholders}}; confere que a parte, expandida, volta idêntica."""
    subs = [(C.v("selo.pin_um_py"), "{{selo.pin_um_py}}"), (C.v("zenodo.doi"), "{{zenodo.doi}}"), (C.v("zenodo.data"), "{{zenodo.data}}"), (C.v("zenodo.versao"), "{{zenodo.versao}}"),
            (", older than this seal; a new Zenodo version is the operator’s act" if not C.v("zenodo.mesmo_selo") else ", byte-identical to this seal", "{{zenodo.relacao}}"),
            ("%d formal files / %d audited terms" % (C.v("kernel.arquivos_formais"), C.v("kernel.declaracoes")),
             "{{kernel.arquivos_formais}} formal files / {{kernel.declaracoes}} audited terms"),
            (C.v("selo.versao"), "{{selo.versao}}")]
    # a ordem importa: o pin antes da versão; o depósito antes do selo (v401 ≠ v406, mas os dois são trocados de forma literal)
    out = {}
    rel = []
    for nome, ini, fim in CORTES:
        i = readme_txt.index(ini)
        j = readme_txt.index(fim, i + len(ini)) if fim.startswith("\n") or True else None
        seg = readme_txt[i:j]
        orig = seg
        n_sub = {}
        for lit, ph in subs:
            c = seg.count(lit)
            if c and not (lit == C.v("zenodo.versao") and (nome not in ("citar", "autor") or C.v("zenodo.mesmo_selo"))):
                seg = seg.replace(lit, ph)
                n_sub[ph] = c
        out[nome] = (seg, orig, n_sub)
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    for nome, (seg, orig, n_sub) in out.items():
        segs = []
        render_texto(C, seg, saida, "", segs, "parte:" + nome)
        volta = "".join(s[2] for s in segs)
        # a expansão do placeholder do pin escreve o valor inteiro; a parte original deve voltar byte a byte
        if volta != orig:
            raise Falha("a parte %s não se reconstrói a partir dos placeholders (diferença na posição %d)" % (nome, next(k for k, (a, b) in enumerate(zip(volta, orig)) if a != b)))
        (saida / (nome + ".md")).write_bytes(seg.encode("utf-8"))
        rel.append("%s.md: %d bytes, %s" % (nome, len(seg.encode("utf-8")), n_sub or "sem placeholders"))
    return rel


# ================================================================================================= a guarda de frases
def conhecidos_de(texto_primordial):
    s = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", texto_primordial)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", texto_primordial))
    return {x.lower() for x in s}


def _neutraliza(t):
    for f in FORMULAS_README_EXTRA:
        t = t.replace(f, " ")
    return t


def regra_444(texto, P):
    """O 4,44 nunca sozinho: cada parágrafo que traz o z_disc traz também z_δ, ln B, «5σ» e o veredito NOT_FALSIFIED_POWERED (ou a tradução PT)."""
    z = P["itens"]["hubble.z_disc"]["valor"]
    en, pt = "%.2f" % z, ("%.2f" % z).replace(".", ",")
    falhas = []
    for par in re.split(r"\n\s*\n", texto):
        if re.search(r"(?<![0-9.,])(%s|%s)(?![0-9])" % (re.escape(en), re.escape(pt)), par):
            for rotulo, rx in (("z_δ", r"z_δ|z_delta"), ("ln B", r"ln B"), ("o degrau de 5σ", r"5σ"), ("o veredito NOT_FALSIFIED_POWERED", r"NOT_FALSIFIED_POWERED"),
                               ("«ln B não é σ» / Bayes factor", r"Bayes|não é σ|not a σ"), ("«abaixo do degrau»", r"below|abaixo")):
                if not re.search(rx, par):
                    falhas.append("parágrafo com z_disc=%s sem %s: %r" % (en, rotulo, par[:70]))
    return falhas


def guardar(segs, P, prim_txt):
    conh = conhecidos_de(prim_txt) | {sha256b(prim_txt.encode("utf-8"))[:16]}          # o sha16 do próprio PRIMORDIAL.json (citado no cabeçalho) foi calculado nesta rodada
    res = {"geradas": [], "herdadas": [], "portas": [], "regra_444": [], "proibidos_privados": None, "formulas_readme_extra": list(FORMULAS_README_EXTRA)}
    for tipo, nome, conteudo in segs:
        if tipo == "gerado":
            conj = conh
            alvo = "geradas"
        else:
            conj = conh | conhecidos_de(conteudo)        # prosa herdada e bloco das portas: os hashes que o próprio trecho traz (não foram calculados nesta rodada)
            alvo = "herdadas" if tipo == "herdado" else "portas"
        for x in textos.portao(_neutraliza(conteudo), conj, rotulo=nome):
            res[alvo].append(x)
    full = "".join(s[2] for s in segs)
    res["regra_444"] = regra_444(full, P)
    # os termos proibidos (lista privada, fora do repositório): só a contagem; os termos nunca saem
    if not PRIVADO.is_file():
        raise Falha("a lista de bloqueio privada está ausente (%s): sem ela a guarda não roda (fail-closed)" % PRIVADO)
    termos = json.loads(PRIVADO.read_text(encoding="utf-8"))["termos"]
    achados = [t for t in termos if t.lower() in full.lower() or t.lower() in prim_txt.lower()]
    res["proibidos_privados"] = {"n_termos_na_lista": len(termos), "achados": len(achados)}
    res["extra_ok"] = {
        "sem_protocolo_de_colapso": ("indicators_6" not in prim_txt and "physical_basis" not in prim_txt and "controls_required" not in prim_txt),
        "sem_dispositivos_das_patentes": ("dispositivo" not in prim_txt.lower()),
    }
    res["nota"] = ("geradas = texto escrito pelo gerador (template e blocos): a condicao de entrega e' 0; herdadas = prosa humana verbatim do livro-razao (append-only; "
                   "cada frase ja' tem a nota «Beside» ao lado no proprio README); portas = bloco mantido por gerar_portas.py; regra_444 = o z_disc nunca sozinho; "
                   "formulas_readme_extra = formulas da regua que o README usa e textos.FORMULAS ainda nao conhece (propostas para a G1)")
    res["n_geradas"], res["n_herdadas"], res["n_portas"] = len(res["geradas"]), len(res["herdadas"]), len(res["portas"])
    res["n_total_candidato"] = res["n_geradas"] + res["n_herdadas"] + res["n_portas"]
    res["n_regra_444"] = len(res["regra_444"])
    res["condicao_de_entrega_ok"] = bool(res["n_geradas"] == 0 and res["n_regra_444"] == 0 and res["proibidos_privados"]["achados"] == 0 and all(res["extra_ok"].values()))
    return res


# ================================================================================================= pino, gerar, verificar
def partes_hashes(partes_dir):
    return {p.name: sha256f(p) for p in sorted(Path(partes_dir).glob("*.md"))}


def montar_pino(C, readme_bytes, prim_bytes, template, partes_dir, readme_nome, portas, nos, gerador_dir):
    return {
        "schema": "PINO_README_V1",
        "versao": C.v("selo.versao"),
        "readme": {"arquivo": readme_nome, "bytes": len(readme_bytes), "sha256": sha256b(readme_bytes), "sha16": sha256b(readme_bytes)[:16], "teto_bytes": TETO},
        "bloco_portas_sha256": sha256b(portas.encode("utf-8")),
        "readme_sem_portas_sha256": sha256b(readme_bytes.decode("utf-8").replace(portas, MARCA_INI + MARCA_FIM).encode("utf-8")),
        "primordial": {"arquivo": "PRIMORDIAL.json", "sha256": sha256b(prim_bytes), "sha16": sha256b(prim_bytes)[:16]},
        "template": {"arquivo": Path(template).name, "sha256": sha256f(template)},
        "partes": partes_hashes(partes_dir),
        "selo": {"arquivo": "um_absoluto_selo.json", "sha256": C.f("selo", "sha256")},
        "pin_um_py": C.v("selo.pin_um_py"),
        "gerador": {"readme_pinado.py": sha256f(Path(gerador_dir) / "readme_pinado.py"), "primordial.py": sha256f(Path(gerador_dir) / "primordial.py")},
        "regra": "o README so se edita pelo gerador; qualquer byte fora dele reprova o --verificar e a custodia",
    }


def _sem_carimbo(d):
    return {k: v for k, v in d.items() if k != "gerado_utc"}


def escrever_bytes(p, b, rotulo):
    p = Path(p)
    if p.exists():
        if p.read_bytes() == b:
            return "inalterado"
        bak = p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
        bak.write_bytes(p.read_bytes())
        assert bak.read_bytes() == p.read_bytes()
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    assert tmp.stat().st_size == len(b)
    os.replace(tmp, p)
    return "escrito"


def cmd_gerar(a, C, prim_bytes):
    portas_de = Path(a.portas_de)
    portas = extrair_portas(portas_de.read_text(encoding="utf-8"))
    texto, segs = renderizar(C, a.template, a.partes, portas)
    b = texto.encode("utf-8")
    if len(b) > TETO:
        raise Falha("o README passou do teto de %d bytes: %d" % (TETO, len(b)))
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    est = escrever_bytes(saida / a.nome, b, "README")
    pino = montar_pino(C, b, prim_bytes, a.template, a.partes, a.nome, portas, a.nos, Path(__file__).resolve().parent)
    pp = saida / "PINO_README.json"
    if pp.exists() and _sem_carimbo(json.loads(pp.read_text(encoding="utf-8"))) == pino:
        est_p = "inalterado"
    else:
        pino["gerado_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        est_p = escrever_bytes(pp, (json.dumps(pino, ensure_ascii=False, indent=1) + "\n").encode("utf-8"), "PINO")
    print("%s: %d bytes (teto %d), sha16 %s [%s]; PINO_README.json [%s]" % (a.nome, len(b), TETO, sha256b(b)[:16], est, est_p))
    if a.guarda:
        G = guardar(segs, C.P, prim_bytes.decode("utf-8"))
        if portas_de.is_file():           # a mesma guarda sobre o README ATUAL (todo ele, sem partição), para comparar
            atual = portas_de.read_text(encoding="utf-8")
            G["baseline_readme_atual"] = {"arquivo": str(portas_de.name), "sha16": sha256b(atual.encode("utf-8"))[:16],
                                          "violacoes_totais": len(textos.portao(_neutraliza(atual), conhecidos_de(atual) | conhecidos_de(prim_bytes.decode("utf-8")), rotulo="README_atual"))}
        Path(a.guarda).write_bytes((json.dumps(G, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
        print("GUARDA: geradas %d · 4,44 %d · proibidos privados %d · herdadas %d · portas %d (condicao_de_entrega_ok=%s) -> %s" % (
            G["n_geradas"], G["n_regra_444"], G["proibidos_privados"]["achados"], G["n_herdadas"], G["n_portas"], G["condicao_de_entrega_ok"], a.guarda))
        return 0 if G["condicao_de_entrega_ok"] else 1
    return 0


def cmd_verificar(a, C, prim_bytes):
    erros, avisos = [], []
    readme_p = Path(a.readme)
    pino_p = Path(a.pino)
    if not readme_p.is_file() or not pino_p.is_file():
        print("REPROVADO: README ou PINO_README.json ausente")
        return 1
    rb = readme_p.read_bytes()
    pino = json.loads(pino_p.read_text(encoding="utf-8"))
    if len(rb) > TETO:
        erros.append("o README passa do teto de %d bytes: %d" % (TETO, len(rb)))
    if sha256b(rb) != pino["readme"]["sha256"]:
        erros.append("o README do disco (%s) não é o do pino (%s): foi editado fora do gerador, ou o laço das portas rodou depois do pino" % (sha256b(rb)[:16], pino["readme"]["sha16"]))
    if sha256b(prim_bytes) != pino["primordial"]["sha256"]:
        erros.append("o PRIMORDIAL.json do disco não é o do pino")
    if sha256f(a.template) != pino["template"]["sha256"]:
        erros.append("o template mudou desde o pino")
    atuais = partes_hashes(a.partes)
    if atuais != pino["partes"]:
        erros.append("as partes mudaram desde o pino: %s" % sorted(set(atuais.items()) ^ set(pino["partes"].items()))[:4])
    if a.nos:
        sp = Path(a.nos) / "um_absoluto_selo.json"
        if sp.is_file() and sha256f(sp) != pino["selo"]["sha256"]:
            erros.append("o selo do Nós (%s) não é o de que o README nasceu (%s)" % (sha256f(sp)[:16], pino["selo"]["sha256"][:16]))
    try:
        portas = extrair_portas(rb.decode("utf-8"))
        texto, _ = renderizar(C, a.template, a.partes, portas)
        if texto.encode("utf-8") != rb:
            i = next((k for k, (x, y) in enumerate(zip(texto.encode("utf-8"), rb)) if x != y), min(len(texto), len(rb)))
            erros.append("o README regenerado (%d B) difere do do disco (%d B) a partir do byte %d: %r != %r" % (len(texto.encode("utf-8")), len(rb), i, texto.encode("utf-8")[i:i + 50], rb[i:i + 50]))
    except SystemExit as e:
        erros.append(str(e))
    g = Path(__file__).resolve().parent
    for nome in ("readme_pinado.py", "primordial.py"):
        if pino.get("gerador", {}).get(nome) != sha256f(g / nome):
            avisos.append("o gerador %s mudou desde o pino (regenere para repinar)" % nome)
    if a.conferir_fontes:
        novo = PRIM.montar({"nos": a.nos, "espelho": a.espelho, "resultado": a.resultado, "handoff": a.handoff, "operador": a.operador})
        velho = json.loads(prim_bytes.decode("utf-8"))
        dif = [k for k in novo["itens"] if not k.startswith("custodia.") and novo["itens"][k] != velho["itens"].get(k)]
        dif += [k for k in velho["itens"] if k not in novo["itens"]]
        for k, f in novo["fontes"].items():
            if f.get("sha256") and velho["fontes"].get(k, {}).get("sha256") != f["sha256"]:
                dif.append("fonte:" + k)
        if novo["urls"] != velho["urls"]:
            dif.append("urls")
        if dif:
            erros.append("o PRIMORDIAL.json está defasado frente às fontes de hoje: %s" % dif[:8])
    for x in erros:
        print("  ✗ " + x)
    for x in avisos:
        print("  ! " + x)
    print("README PINADO: %s (%d erros, %d avisos; %d bytes, sha16 %s)" % ("CONFERE" if not erros else "REPROVADO", len(erros), len(avisos), len(rb), sha256b(rb)[:16]))
    return 0 if not erros else 1


def main(argv=None):
    cam = Caminhos()
    ap = argparse.ArgumentParser(description="README pinado: gera, verifica e extrai as partes")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--gerar", action="store_true")
    g.add_argument("--verificar", action="store_true")
    g.add_argument("--extrair-partes", metavar="README", help="README de onde cortar as partes (migração)")
    ap.add_argument("--primordial", required=True, help="PRIMORDIAL.json")
    ap.add_argument("--template", help="template do README")
    ap.add_argument("--partes", help="pasta readme_partes/")
    ap.add_argument("--saida", help="pasta de saída do README e do pino")
    ap.add_argument("--nome", default="README.md", help="nome do README gerado (padrão README.md)")
    ap.add_argument("--portas-de", help="README de onde copiar o bloco das portas (padrão: README.md do espelho)")
    ap.add_argument("--guarda", help="grava a guarda de frases neste arquivo .json")
    ap.add_argument("--readme", help="--verificar: o README a conferir")
    ap.add_argument("--pino", help="--verificar: o PINO_README.json")
    ap.add_argument("--conferir-fontes", action="store_true")
    ap.add_argument("--nos")
    ap.add_argument("--espelho")
    ap.add_argument("--resultado")
    ap.add_argument("--handoff")
    ap.add_argument("--operador")
    a = ap.parse_args(argv)
    prim_bytes = Path(a.primordial).read_bytes()
    P = json.loads(prim_bytes.decode("utf-8"))
    if P.get("schema") != "PRIMORDIAL_V1":
        raise Falha("PRIMORDIAL.json de schema desconhecido")
    C = Ctx(P, prim_bytes)
    a.portas_de = a.portas_de or str(Path(a.espelho or cam.TB) / "README.md")
    a.nos = a.nos or str(cam.NOS)
    if a.extrair_partes:
        if not a.partes:
            raise Falha("--extrair-partes pede --partes")
        for linha in extrair_partes(Path(a.extrair_partes).read_text(encoding="utf-8"), C, a.partes):
            print("  " + linha)
        return 0
    if not (a.template and a.partes):
        raise Falha("--template e --partes são obrigatórios")
    if a.verificar:
        if not (a.readme and a.pino):
            raise Falha("--verificar pede --readme e --pino")
        return cmd_verificar(a, C, prim_bytes)
    if not a.saida:
        raise Falha("--gerar pede --saida")
    return cmd_gerar(a, C, prim_bytes)


if __name__ == "__main__":
    sys.exit(main())

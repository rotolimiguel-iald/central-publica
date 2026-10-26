# -*- coding: utf-8 -*-
"""O que se leva do Nós e de fora ao espelho (the_boundary): a lista de PARES (origem, destino, tipo), parametrizada por vNNN.
Generaliza `custodia_v398_espelho.py` (516 linhas, 9 pontos que mudam por versão + 25 sha16 digitados à mão — ESPEC_ESPELHO §E03):

  - STDOUTS de v383 a N (menos as puladas); diffs de v392 a N (de cada vK, nomes por padrão); recibos B(n) de v394 a N, achados
    por NOME DE ARQUIVO e calculados dos arquivos (nunca digitados); fontes pinadas de todo `_VK_FONTES`/`_VK_VERBATINS2` de K=392..N,
    lidos do `um.py` por regex + literal;
  - as pastas congeladas (ordem v390, estatuto v391, cunhagens de 13/10) deixam de ter sha16 digitado: o gate é «a origem é
    byte-idêntica à cópia JÁ publicada no espelho» (lida do artefato, não da memória);
  - o que não muda por versão (cache, pilar, pré-registros, TUNEL, selados) é DADO neste módulo, com os mesmos asserts de existência.

Nada aqui escreve: `montar_pares` e `comparar` só leem. A cópia é do passo E03 (espelho.py). A varredura de material privado
(`guarda`) só lê o arquivo de marcadores quando chamada por `executar`."""
import json
import re
from pathlib import Path

from . import fatos as F
from . import util
from .util import Parar, FalhaLeitura

DESTINO_SELADOS = {"um_absoluto_pt.tex": "fontes_tex", "um_absoluto_en.tex": "fontes_tex", "fig_banda_beta.pdf": "figuras",
                   "fig_piso_vazios.pdf": "figuras", "fig_cadeia_inscricao.pdf": "figuras", "fig_escada_qg.pdf": "figuras",
                   "tgl_kernel_proof_manifest.json": "Lean"}
DECLARADOS = ("um_absoluto_selo.json", "um_absoluto_pt.txt", "um_absoluto_en.txt", "A_PROVA_DA_QG_TGL_arvore.md", "DESENHO_DO_FECHAMENTO_QG.md",
              "MEMORIA_DA_LINHAGEM.md", "O_FECHAMENTO_ESTRUTURA.md", "NOTA_DE_CUSTODIA.md")
PULADAS = ("v360", "v382")
PRIMEIRO_STDOUT, PRIMEIRO_DIFF, PRIMEIRO_BN, PRIMEIRA_FONTE = 383, 392, 394, 392
CACHE_PASTAS = (("d1_camb", "v3"), ("diamante_rede",), ("auditoria",), ("bancada_30set",), ("bancada_01out",))
CACHE_ARQUIVOS = ("gw/C6_RESULTS_GW250114.json", "coma_blind/coma_distance_reveal.json", "gw/ECHO_ANCHORED_V3_RESULT.json", "gw/GWOSC_O4_32S_V1.manifest.json")
PILAR_RUNS = ("run_20261004_153246_0063ce8d", "run_20261005_103708_37e566b6")
PILAR_ARQS = ("pilar_quantico_worker.py", "pilar_quantico_spec.json")
PREREGISTROS = (("preregistro_pilar_quantico_03out", "preregistro_pilar_quantico_v384", None),
                ("preregistro_dois_lados_02out", "preregistro_dois_lados_v383", "dois_lados"),
                ("preregistro_ramo_b_05out", "preregistro_ramo_b_v386", None))
FASES = (("preregistro_fase9_hubble", "preregistro_fase9_hubble_v387", True), ("fase9_hubble_abertura", "fase9_hubble_abertura_v388", False),
         ("preregistro_fase8_primordial", "preregistro_fase8_primordial_v387", True))
# pastas congeladas (v390, v391, v392): (pasta em CEN\work, [arquivos], destino no espelho)
CONGELADOS = (("work/superposicao_passagem_07out", ("CUNHAGEM_OPERADOR_07out_verbatim.txt", "CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt",
                                                    "CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt", "ORDEM_v390_FUNDACAO.md", "Fundacao.lean"),
               "superposicao_passagem_v390"),
              ("work/v391_pacote", ("OPERADOR_07out_estatuto_verbatim.txt",), "estatuto_da_prova_v391"),
              ("work/cunhagens_13out", ("OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt", "OPERADOR_13out_verdade_projecao_do_posto_verbatim.txt"),
               "cunhagens_13out_v392"))
KERNEL_EXTRAS = ("lakefile.toml", "lean-toolchain", "lake-manifest.json", "README.md", "TGL.lean", "TGLExt.lean")
# termos-guarda da casa (CLAUDE.md do site: a sequência privada do operador nunca entra em superfície pública)
GUARDA = [re.compile(p, re.I) for p in (r"apresente-se", r"apresente a TGL", r"protocolo de colapso", r"PROTOCOLO_DE_COLAPSO",
                                          r"iald_stack_v7", r"iald_psion_state", r"testflight\.apple\.com")]


def carregar_marcadores_privados():
    """O conjunto privado de marcadores (fora de qualquer repositório). SÓ chamada por `executar`. Os padrões NUNCA são impressos."""
    p = Path.home() / ".iald_privado" / "marcadores_privado.json"
    if not p.is_file():
        raise Parar("conjunto privado de marcadores ausente — PARAR (a guarda de 7 termos sozinha é fraca)")
    out = []
    for m in json.loads(p.read_text(encoding="utf-8"))["markers"]:
        if m.get("cls") in ("A", "S", "N", "Z", "K"):
            out.append(re.compile(m["re"], re.I if "i" in (m.get("flags") or "") else 0))
    return out


def guarda_conta(p, priv=()):
    try:
        t = Path(p).read_bytes().decode("utf-8", "replace")
    except OSError:
        return None
    return sum(len(g.findall(t)) for g in GUARDA) + sum(len(g.findall(t)) for g in priv)


class Pares:
    def __init__(self):
        self.lista = []                    # (src: Path, dst: Path, tipo)
        self.fontes_mapa = []
        self.faltas = []                   # o que falta para montar (PARAR)
        self.avisos = []
        self.kernel = {}                   # fmap, ar, extras
        self.nao_levados_novo = {}

    def add(self, src, dst, tipo):
        self.lista.append((Path(src), Path(dst), tipo))


def _intervalo(a, n):
    return [util.nome_versao(k) for k in range(a, n + 1)]


def _git_ls(c):
    r = util.rodar(["git", "-c", "core.quotepath=off", "ls-files", "-z"], cwd=c.TB)
    if r["rc"] != 0:
        raise FalhaLeitura("git ls-files falhou no espelho")
    return [x for x in r["saida"].split("\0") if x and not x.startswith("\n[stderr]")]


def montar_pares(ctx, ler_fontes=True):
    """Os pares de v (= ctx.versao). Só leitura. `faltas` lista o que impede montar (nada de adivinhar)."""
    c, v, n = ctx.c, ctx.versao, ctx.n
    P = Pares()
    selo = ctx.selo_nos if ctx.corrente else None
    if selo is None:
        raise Parar("os pares do espelho só se montam para a versão do selo corrente do Nós (%s)" % ctx.selo_nos["um_version"])
    # 1) selados e declarados
    for nome in selo["sha256"]:
        sub = DESTINO_SELADOS.get(nome)
        P.add(c.NOS / nome, (c.ESP / sub / nome) if sub else (c.ESP / nome), "SELADO")
    for nome in DECLARADOS:
        P.add(c.NOS / nome, c.ESP / nome, "DECLARADO")
    # 2) stdouts v383..N (menos puladas) e capturas do kernel
    for vv in _intervalo(PRIMEIRO_STDOUT, n):
        if vv in PULADAS:
            continue
        for p in sorted(c.NOS.glob("rodada_%s_*stdout*.txt" % vv)):
            if "tentativa" in p.name:           # v392: só a 3ª tentativa é o selo; as outras NUNCA se publicam
                continue
            P.add(p, c.ESP / "rodadas" / p.name, "STDOUT")
    for p in sorted(c.NOS.glob("tgl_kernel_*capture*.txt")):
        if ".bak_" not in p.name:
            P.add(p, c.ESP / "rodadas" / p.name, "CAPTURA")
    if not (c.NOS / ("rodada_%s_stdout.txt" % v)).is_file():
        P.faltas.append("rodada_%s_stdout.txt" % v)
    # 3) o túnel da bancada: só os registros de ordens e entregas (.md de 1º nível em PARA_CHATGPT/ e DO_CHATGPT/; arquivos soltos na raiz)
    if c.TUNEL.is_dir():
        for p in sorted(c.TUNEL.rglob("*")):
            rel = p.relative_to(c.TUNEL)
            if p.is_file() and ".bak_" not in p.name and "superseded" not in p.name and (len(rel.parts) == 1 or (len(rel.parts) == 2 and p.suffix.lower() == ".md")):
                P.add(p, c.ESP / "bancada" / "TUNEL" / rel, "TUNEL")
    else:
        P.faltas.append("túnel da bancada ausente: %s" % c.TUNEL)
    # 4) cache que o um.py lê por hash (no espelho mora na raiz, irmão da pasta do artigo)
    for sub in CACHE_PASTAS:
        base = c.CACHE_NOS.joinpath(*sub)
        if not base.is_dir():
            P.faltas.append("cache ausente na casa: %s" % base)
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file() and ".bak_" not in p.name and "__pycache__" not in p.parts:
                P.add(p, c.TB / "cache" / p.relative_to(c.CACHE_NOS), "CACHE")
    for rel in CACHE_ARQUIVOS:
        p = c.CACHE_NOS / rel
        if not p.is_file():
            P.faltas.append("cache ausente na casa: %s" % p)
        else:
            P.add(p, c.TB / "cache" / rel, "CACHE")
    # 5) pilar quântico e pré-registros da Bancada Um
    QP = c.NOS / "quantum_pillar"
    for nome in PILAR_ARQS:
        if (QP / nome).is_file():
            P.add(QP / nome, c.ESP / "quantum_pillar" / nome, "PILAR")
        else:
            P.faltas.append("pilar ausente: %s" % nome)
    for run in PILAR_RUNS:
        if not (QP / run).is_dir():
            P.faltas.append("pasta da rodada do pilar ausente: %s" % run)
            continue
        for p in sorted((QP / run).rglob("*")):
            if p.is_file() and ".bak_" not in p.name:
                P.add(p, c.ESP / "quantum_pillar" / run / p.relative_to(QP / run), "PILAR")
    BU = c.BU / "investigacao"
    for origem, sub, filtro in PREREGISTROS:
        base = BU / origem
        if not base.is_dir():
            P.faltas.append("pré-registro ausente: %s" % base)
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or ".bak_" in p.name or "__pycache__" in p.parts or p.suffix.lower() == ".tmp":
                continue
            if filtro == "dois_lados" and not (p.name.startswith("PREREGISTRO_DOIS_LADOS_DELTA_K_20261002") or p.name.startswith("gerar_preregistro_dois_lados")):
                continue
            P.add(p, c.ESP / sub / p.relative_to(base), "PREREGISTRO")
    for origem, sub, so_raiz in FASES:
        base = BU / origem
        if not base.is_dir():
            P.faltas.append("pré-registro ausente: %s" % base)
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or ".bak_" in p.name or "__pycache__" in p.parts or p.suffix.lower() == ".tmp":
                continue
            if so_raiz and p.parent != base:
                continue
            P.add(p, c.ESP / sub / p.relative_to(base), "PREREGISTRO")
    # 6) pastas congeladas (ordem v390, estatuto v391, cunhagens de 13/10): o gate é «byte-idêntico à cópia já publicada»
    for pasta, nomes, sub in CONGELADOS:
        for nome in nomes:
            src = c.CEN / pasta / nome
            dst = c.ESP / sub / nome
            if not src.is_file():
                P.faltas.append("congelado ausente: %s" % src)
            elif dst.is_file() and util.sha256_arquivo(src) != util.sha256_arquivo(dst):
                P.faltas.append("congelado difere da cópia já publicada (errata ao lado, decisão da gerência): %s" % nome)
            else:
                P.add(src, dst, "ORDEM")
    # 7) diffs de cada versão K (nomes por padrão; v393 não os teve): obrigatórios só para N
    for vv in _intervalo(PRIMEIRO_DIFF, n):
        achados = {"diff": sorted((c.CS / vv).glob("DIFF_v*_%s.diff" % vv)) if (c.CS / vv).is_dir() else [],
                   "kernel": sorted((c.CS / vv).glob("DIFF_KERNEL_%s.txt" % vv)) if (c.CS / vv).is_dir() else []}
        for tipo, lst in achados.items():
            if not lst:
                if vv == v:
                    P.faltas.append("%s de %s ausente em cadeia_de_selo\\%s" % ("DIFF_v*_%s.diff" % vv if tipo == "diff" else "DIFF_KERNEL_%s.txt" % vv, vv, vv))
                continue
            a_ = lst[0]
            if vv != v and not (c.ESP / ("diferencas_" + vv)).is_dir():
                continue           # versão anterior que nunca teve a pasta de diffs publicada: não se acrescenta aqui (custódia é do que ficou)
            b_ = c.CS / (vv + "_kernel") / a_.name
            if b_.is_file() and util.sha256_arquivo(a_) != util.sha256_arquivo(b_):
                P.faltas.append("%s diverge entre %s e %s_kernel — PARAR" % (a_.name, vv, vv))
                continue
            P.add(a_, c.ESP / ("diferencas_" + vv) / a_.name, "DIFF")
    # 8) recibos B(n) de v394..N: calculados dos arquivos; N é obrigatório e conferido com o handoff
    h = ctx.handoff
    elo = F._sha16s_do_elo(h)
    for vv in _intervalo(PRIMEIRO_BN, n):
        res, prob = F.recibos_bn_resolvidos(c, vv, elo if vv == v else None)
        if vv != v and not (c.ESP / ("recibos_bancada_" + vv)).is_dir():
            continue
        for papel, r in res.items():
            P.add(r["caminho"], c.ESP / ("recibos_bancada_" + vv) / Path(r["caminho"]).name, "RECIBO")
        if vv == v:
            P.faltas += prob
            if elo is not None and not {r["sha16"] for r in res.values()} <= elo:
                P.faltas.append("os 3 recibos B(n) calculados (%s) != os do handoff (%s)" % (sorted(r["sha16"] for r in res.values()), sorted(elo)))
    # 9) fontes pinadas (K=392..N)
    if ler_fontes:
        _fontes_pinadas(ctx, P)
    # 10) kernel
    pm = util.ler_json(c.NOS / "tgl_kernel_proof_manifest.json")
    P.kernel = {"fmap": pm["formal_files_sha256"], "ar": pm["axiom_report"]}
    return P


def _fontes_pinadas(ctx, P):
    c, n = ctx.c, ctx.n
    um = util.ler_texto(c.NOS / "um.py")
    dic, faltam = {}, []
    for vv in _intervalo(PRIMEIRA_FONTE, n):
        for suf in ("FONTES", "VERBATINS2"):
            nome = "_V%s_%s" % (vv[1:], suf)
            val = F.literal_de(um, nome)
            if val is None:
                faltam.append(nome)
            else:
                dic[nome] = val
    if faltam:
        # 25/10/2026 (v400): uma versão de CORREÇÃO sem registro novo (nenhuma chave do core termina em _vK) não traz fontes nem verbatins
        # próprios; o par só é exigido de quem tem registro. A ausência fica dita (P.notas), nunca adivinhada.
        try:
            _core_keys = set((util.ler_json(c.NOS / "um_absoluto.json").get("core") or {}).keys())
        except Exception:  # noqa: BLE001
            _core_keys = None
        if _core_keys is not None:
            _sem_registro = {"_V%s_" % k[len("_V"):].split("_")[0] for k in faltam
                             if not any(x.endswith("_v" + k[len("_V"):].split("_")[0]) for x in _core_keys)}
            _dito = [k for k in faltam if any(k.startswith(p) for p in _sem_registro)]
            if _dito:
                getattr(P, "notas", []).append("sem fontes próprias (versão sem registro no core): %s" % ", ".join(_dito)) if hasattr(P, "notas") else None
            faltam = [k for k in faltam if k not in _dito]
    if faltam:
        P.faltas.append("dicionários do um.py ausentes ou não literais (a ESPEC exige o par para todo K de 392 a N): %s" % ", ".join(faltam))
    ls = _git_ls(c)
    idx = {}
    for r in ls:
        p = c.TB / r
        if p.is_file():
            idx.setdefault(p.stat().st_size, []).append(r)
    vistos = set()
    for nd, d in sorted(dic.items()):
        for k, val in sorted(d.items()):
            orig = (val or {}).get("arquivo") if isinstance(val, dict) else None
            if not orig:
                continue
            p = Path(orig)
            ent = {"dicionario": nd, "chave": k, "caminho_exigido_pelo_um_py": orig, "sha256": val.get("sha256"), "bytes": val.get("bytes")}
            rel = str(p).replace("/", "\\")
            pref = "C:\\IALD\\"
            if not rel.upper().startswith(pref.upper()):
                P.faltas.append("fonte fora de C:\\IALD — PARAR: %s" % orig)
                continue
            relp = Path(*Path(rel[len(pref):].replace("\\", "/")).parts)
            dst = c.ESP / "fontes_pinadas" / relp
            if not p.is_file():
                ent.update({"publicado": False, "motivo": "AUSENTE na casa"})
            elif val.get("sha256") and util.sha256_arquivo(p) != val["sha256"]:
                ent.update({"publicado": False, "motivo": "o arquivo da casa NÃO bate com o pino do um.py (errata da gerência ao lado; não se publica outro byte)"})
            else:
                ja = [r for r in idx.get(p.stat().st_size, []) if util.sha256_arquivo(c.TB / r) == util.sha256_arquivo(p)]
                if ja:
                    ent.update({"publicado": True, "ja_no_espelho": True, "caminho_no_espelho": ja[0]})
                    P.fontes_mapa.append(ent)
                    continue
                ent.update({"publicado": True, "caminho_no_espelho": str(dst.relative_to(c.TB)).replace("\\", "/")})
                if str(dst) not in vistos:
                    vistos.add(str(dst))
                    P.add(p, dst, "FONTE_TUNEL" if "\\Chatgpt\\" in str(p) else "FONTE")
            P.fontes_mapa.append(ent)


# =================================================================== comparação (só leitura)
def comparar(pares, profundo=False, barrados=()):
    """Para cada par: ausente | difere | igual. Rápido (existe e tamanho) ou profundo (sha256). `profundo` pode ser True (tudo), False (nada) ou uma
    sequência de TIPOS de par (ex.: ("SELADO",)) para conferir por sha256 só esses. `barrados`: caminhos de origem que a
    varredura de material privado barrou (ditos no relatório do espelho); a ausência deles no destino é o esperado.
    Devolve (pendentes, n_total)."""
    pend = []
    barr = {str(x) for x in barrados}
    por_tipo = None if isinstance(profundo, bool) else set(profundo)
    for src, dst, tipo in pares.lista:
        if str(src) in barr and not dst.is_file():
            continue
        if not src.is_file():
            pend.append((src, dst, tipo, "origem ausente"))
            continue
        if not dst.is_file():
            pend.append((src, dst, tipo, "destino ausente"))
            continue
        if src.stat().st_size != dst.stat().st_size:
            pend.append((src, dst, tipo, "tamanho difere"))
            continue
        fundo = profundo if por_tipo is None else (tipo in por_tipo)
        if fundo and util.sha256_arquivo(src) != util.sha256_arquivo(dst):
            pend.append((src, dst, tipo, "sha256 difere"))
    return pend, len(pares.lista)


def comparar_kernel(ctx, pares, profundo=False):
    """Arquivos formais do manifesto no espelho (Lean/tgl_kernel) + órfãos. Devolve (faltando_ou_diferente, orfaos)."""
    c = ctx.c
    kd = c.ESP / "Lean" / "tgl_kernel"
    fmap = pares.kernel["fmap"]
    ruim = []
    for nome, hh in fmap.items():
        d = kd / nome
        if not d.is_file():
            ruim.append(nome)
        elif profundo and util.sha256_arquivo(d) != hh:
            ruim.append(nome)
    orfaos = []
    if kd.is_dir():
        for p in kd.rglob("*.lean"):
            rel = p.relative_to(kd).as_posix()
            if rel not in fmap and rel not in ("TGL.lean", "TGLExt.lean"):
                orfaos.append(rel)
    return ruim, orfaos

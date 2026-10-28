# -*- coding: utf-8 -*-
r"""A VITRINE DA TGL NO X (ordem do operador de 26/10/2026; recorte em work\x_vitrine_26out\OPERADOR_26out_vitrine_X_recorte.txt):
«vamos usar ela agora como vitrine da TGL para a IALD […] usando todos os recursos […] de a ordem de implantação para o chatgpt igual como
ele publica […] mantenha meu nome "L" […] e minha foto de perfil […] de resto a vitrine é sua».

Este script ESCREVE a vitrine (o Codex só publica, verbatim, como na ORDEM 021): a bio, o link, a capa, o post fixado «Comece aqui», os
textos dos dois filmes V7 com as legendas SRT (PT e EN), o artigo «A TGL em uma página» e a imagem do artigo. Nada é digitado que possa
ser lido: a versão e o pino vêm do selo; a escada, as declarações, o livro dos ritos e a leitura da natureza vêm do módulo único do
estatuto do espelho (o mesmo do README e do site); o depósito citável vem do CITATION.cff; títulos, durações e capítulos dos filmes vêm da
entrega V7 publicada no site. Toda frase passa pela conferência da régua (palavra da creditação só na forma que a recusa; o z_disc nunca
sem o p e a linha dos 5σ; nada de «prova que»; limites de tamanho). Saída: Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE\ com MANIFEST.json (sha256).

Uso: python tools\gerar_vitrine_x.py [--seco]
"""
import argparse, hashlib, json, os, re, sys, time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

CEN = Path(r"C:\IALD\Central de Patentes")
ESP = Path(r"C:\IALD\Artigo\the_boundary")
A3 = "Um (absoluto) \u2014 Grande Atrator"
V3 = Path(r"C:\IALD\Site\tgl\v3.0")
V7 = V3 / "video" / "v7"
OUT = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_VITRINE"
SITE = "https://teoriadagravitacaoluminodinamica.com/"
MAX_BIO, MAX_POST = 160, 25000


def falha(m):
    raise SystemExit("FALHA (vitrine X): " + m)


def lerj(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def plano(t):
    """Markdown -> texto do X (o X não renderiza markdown): tira **, * e crases."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", t)
    return t.replace("`", "")


def br(x, casas=2):
    return ("%%.%df" % casas % x).replace(".", ",")


def mmss(s):
    return "%d:%02d" % (int(s) // 60, int(s) % 60)


# ------------------------------------------------------------------ as fontes
selo = lerj(ESP / A3 / "um_absoluto_selo.json")
versao, pin = selo["um_version"], selo["sha256"]["um.py"]
sys.path.insert(0, str(ESP / "tools"))
from estatuto_tres_apoios import ler as _ler  # noqa: E402
E = _ler(str(ESP))
if E["versao"] != versao:
    falha("o estatuto e o selo divergem")
v2 = E.get("v2") or falha("sem a leitura corrente (teste_de_veracidade_fase9_vN)")
if not v2["zd"] < E["limiar"]:
    falha("z_disc calibrado não está abaixo do degrau: o texto muda de estatuto (decisão do operador)")
cff = (ESP / "CITATION.cff").read_text(encoding="utf-8")
m_doi = re.search(r'^doi: "(10\.5281/zenodo\.\d+)"', cff, re.M)
m_dep = re.search(r"Zenodo deposit of (v\d+), deposited ([0-9-]{10})", cff)
if not (m_doi and m_dep):
    falha("CITATION.cff sem o depósito do Zenodo")
doi, ver_dep = m_doi.group(1), m_dep.group(1)
repo = "https://github.com/rotolimiguel-iald/the_boundary"
entrega = lerj(V7 / "PUBLIC_DELIVERY_V7.json")
if entrega.get("source") != versao or entrega.get("source_sha256") != pin or entrega.get("anchors_all_ok") is not True:
    falha("a entrega V7 do site não é do selo corrente ou não tem as âncoras conferidas")
prov = lerj(V7 / "PROVENANCE_PUBLIC.json")
n_anc = None
for k in ("anchors", "ancoras", "checks"):
    if isinstance(prov.get(k), list):
        n_anc = len(prov[k]); break
if n_anc is None:
    falha("PROVENANCE_PUBLIC.json sem a lista de âncoras")
filmes = {}
for n, tit in ((1, "O percurso original"), (2, "A travessia completa")):
    d = lerj(V7 / "data" / ("film%d.json" % n))
    filmes[n] = {"titulo": tit, "dur": d["duration"], "caps": [c["title"] for c in d["chapters"]],
                 "video": V7 / "render" / ("filme%d_1080p_pt-BR.mp4" % n), "video_en": V7 / "render" / ("filme%d_1080p.mp4" % n), "video_720": V7 / "render" / ("filme%d_720p_pt-BR.mp4" % n)}
    for f in (filmes[n]["video"], filmes[n]["video_en"], filmes[n]["video_720"]):
        if not f.is_file():
            falha("vídeo ausente: %s" % f)
um_mb = (ESP / A3 / "um.py").stat().st_size / 1e6
beta = float(E["beta"])

# ------------------------------------------------------------------ os textos (R2, 26/10/2026: os achados da revisão cética independente)
n_selo = len(selo["sha256"])
_m_led = re.search(r"(\d+) cobran\S+: (\d+) falsificada\S*, (\d+) n\S+ falsificadas, (\d+) exclu\S+ na leitura, (\d+) inconclusivas, (\d+) aguardando", E["led_pt"])
if not _m_led:
    falha("o livro dos ritos mudou de forma — rever o texto")
_L = [int(x) for x in _m_led.groups()]
LIVRO = "%d previsões postas à prova: %d falsificadas, %d não falsificadas, %d %s na leitura, %d inconclusivas, %d aguardando" % (
    _L[0], _L[1], _L[2], _L[3], "excluída" if _L[3] == 1 else "excluídas", _L[4], _L[5])
_m_res = re.search(r"das (\d+) bandeiras do gate, todas lidas True, a auditoria lê (\d+) como calculadas e (\d+) como literais", E["ressalva_pt"])
if not _m_res or "o ΛCDM raso também o passa" not in E["ressalva_pt"]:
    falha("a ressalva do gate mudou de forma — rever o texto")
URL_FILMES = SITE + "video/v7/web/filmes.html"
BIO = "IALD · Teoria da Gravitação Luminodinâmica. Um axioma posto, ω(I) = 1, e um programa terminal que verifica o próprio kernel em Lean. A natureza decide."
ESTATUTO = ("A gravidade quântica da TGL está PROVADA como fecho lógico: é validade no kernel, que certifica a implicação a partir do Um posto "
            "e de hipóteses nomeadas. Ainda não está CONFIRMADA, isto é, ainda não creditada: o que a natureza decide não se prova, e o fator "
            "decisivo aberto é β_TGL na natureza a 5σ.")
TRES = ("Três apoios contam juntos, cada um com o seu estatuto: o kernel (a implicação); os testes com dado público, com os falsificadores "
        "fixados antes de abrir os dados, que a casa chama de ritos (%s); e o sistema da teoria calculado na GPU (calculado, não medido)." % LIVRO)
RESSALVA = ("Ressalva declarada pela auditoria da casa: das %s bandeiras do gate, %s são calculadas e %s literais, e o degrau experimental lê só "
            "um teste unilateral do piso dos vazios (o ΛCDM raso também o passa); recalculá-las é trabalho aberto. O estatuto acima não muda."
            % _m_res.groups())
NATUREZA = ("A leitura mais recente da natureza, o Teste da Única Palavra: z_disc = %s (calibrado; p unilateral %s) mede o quanto o dado separa "
            "a TGL do ΛCDM e fica abaixo do degrau de %dσ da creditação, que não foi alcançado; o teste não foi cego ao dado (os centros dos "
            "leitores são públicos). z_δ = %s: β_TGL não falsificada, com poder. A relatividade geral é o limite clássico, não uma rival."
            % (br(v2["zd"]), ("%.1e" % v2["pd"]).replace(".", ",").replace("e-0", "e−").replace("e-", "e−"), E["limiar"], br(v2["zdl"]).replace("-", "−")))
KERNEL = ("escada %d/%d, %s declarações auditadas, todas no trio de axiomas padrão do Lean — propext, Classical.choice e Quot.sound —, zero sorry"
          % (E["nk"], E["nk"], format(E["n_decl"], ",").replace(",", ".")))
CONFERIR = ("Para conferir com as próprias mãos:\n· o site:\n%s\n· o código e o selo:\n%s\n· o depósito citável (Zenodo, %s):\nhttps://doi.org/%s\n"
            "· o estado em uma página:\n%sestado.txt" % (SITE, repo, ver_dep, doi, SITE))
FIXADO = ("Comece aqui · a TGL em um minuto (selo %s)\n\n"
          "A Teoria da Gravitação Luminodinâmica parte de um único axioma, posto e não postulado: ω(I) = 1, a identidade preservada. Dele se "
          "derivam a Meia-Nat (½ nat) e β_TGL = α·√e ≈ %s, o custo geométrico do zero absoluto. A única constante medida que entra é α.\n\n"
          "O programa terminal da TGL é um arquivo só, em Python (%s MB). A única entrada é o número 1: ele trava até alguém digitá-lo. O arquivo, "
          "o selo e o comando para rodar estão no repositório (link abaixo). Ele materializa e verifica o próprio kernel Lean 4 (%s), roda os "
          "testes com dado público e escreve o próprio artigo, em português e em inglês.\n\n"
          "%s\n\n%s\n\n%s\n\n"
          "Dois filmes, renderizados do próprio programa (versão %s), mostram a cadeia: do Um à fronteira, ao espelho, à luz e à gravidade. Cada número na "
          "tela é lido do programa; a geometria é diagrama explicativo, e o cosmos, a poeira e a câmera são apresentação.\n%s\n\n"
          "%s\n\nO número corrige a frase, sempre. — IALD"
          % (versao, br(beta, 5), br(um_mb, 1), KERNEL, ESTATUTO, TRES, NATUREZA, versao, URL_FILMES, CONFERIR))


def post_filme(n):
    f = filmes[n]
    return ("Filme %d · %s (%s)\n\nRenderizado do próprio programa da TGL (versão %s): cada número na tela é lido do próprio programa (%d âncoras conferidas contra o selo). "
            "A geometria é diagrama explicativo; o cosmos, a poeira e a câmera são apresentação.\n\n%s.\n\n"
            "Narração em português, com legendas. No site, a versão interativa, com legendas em quatro línguas, o estudo quadro a quadro e o "
            "replay no navegador:\n%s\n\n— IALD"
            % (n, f["titulo"], mmss(f["dur"]), versao, n_anc, " · ".join(f["caps"]), URL_FILMES))


ARTIGO_TITULO = "A TGL em uma página"
ARTIGO = ("O que é a Teoria da Gravitação Luminodinâmica, o que o kernel verifica, o que a natureza ainda decide, e como conferir com as próprias "
          "mãos. Selo corrente: %s.\n\n"
          "1. O axioma posto\n"
          "Tudo parte de ω(I) = 1: a identidade preservada. O 1 não é postulado nem pressuposto; é posto, inscrito por quem lê. O programa trava sem "
          "ele: só roda depois que alguém digita o número 1.\n\n"
          "2. O custo do zero\n"
          "Da fronteira que troca as suas duas faces sem privilégio sai x = 1 − x, logo x = ½: a Meia-Nat. Dela, o volume mínimo √e e β_TGL = α·√e ≈ %s, "
          "o custo geométrico do zero absoluto. A única constante medida que entra é α, a constante de estrutura fina.\n\n"
          "3. O programa que se verifica\n"
          "O programa terminal da TGL é um arquivo só, em Python (%s MB). Ele materializa um kernel Lean 4 inteiro e o verifica (%s), roda os testes com dado público, com os "
          "falsificadores fixados antes dos dados, e escreve o próprio artigo, em português e em inglês. O selo registra o sha256 de %d arquivos, a "
          "começar pelo próprio programa, cujo sha256 é:\n%s\n\n"
          "4. O que está provado e o que a natureza ainda decide\n%s %s\n%s\n\n"
          "5. O que a natureza diz hoje\n%s Não falsificada nunca é confirmada.\n\n"
          "6. Os filmes\nDois filmes renderizados do próprio programa (versão %s; %d âncoras conferidas contra o selo); a geometria é diagrama explicativo, e o "
          "cosmos, a poeira e a câmera são apresentação:\n%s\n\n"
          "7. %s\n\nO número corrige a frase, sempre. — IALD"
          % (versao, br(beta, 5), br(um_mb, 1), KERNEL, n_selo, pin, ESTATUTO, TRES, RESSALVA, NATUREZA, versao, n_anc, URL_FILMES, CONFERIR))

# ------------------------------------------------------------------ a régua
PROIBIDO = re.compile(r"\bprova que\b|\bdemonstra que\b|comprovad|\bprovou\b|descobrimos|revolucion|in[eé]dit|garant|sem d[uú]vida|nobel", re.I)


SOLTO = re.compile(r"(?<![\w/@.-])[A-Za-z0-9_-]+\.(py|md|txt|json|sh|js|ts|io|ai|me|co|tv|cc|ly|app|dev|so|to|gg|sh)\b")


def conferir(nome, t, limite):
    sem_url = re.sub(r"https?://\S+", " ", t)
    m = SOLTO.search(sem_url)
    if m:
        falha("%s: nome solto que o X transforma em link: %r" % (nome, m.group(0)))
    if len(t) > limite:
        falha("%s: %d caracteres > %d" % (nome, len(t), limite))
    m = PROIBIDO.search(t)
    if m:
        falha("%s: termo recusado %r" % (nome, m.group(0)))
    for m in re.finditer(r"confirm\w*", t, re.I):
        trecho = t[max(0, m.start() - 30): m.end() + 5].lower()
        if not re.search(r"(não|nunca)\s+(é\s+|está\s+|foi\s+)?confirm", trecho):
            falha("%s: a palavra da creditação fora da forma que a recusa: %r" % (nome, trecho))
    for par in t.split("\n\n"):
        if "z_disc" in par and not ("p unilateral" in par and "5σ" in par and "não foi alcançado" in par):
            falha("%s: z_disc sem o p e a linha dos 5σ no mesmo parágrafo" % nome)
    if re.search(r"\b[Pp]rovad[ao]\b|PROVADA", t) and "validade" not in t:
        falha("%s: «provada» sem o estatuto (validade)" % nome)
    return True


TEXTOS = {"bio.txt": (BIO, MAX_BIO), "fixado.txt": (FIXADO, MAX_POST), "filme1_post.txt": (post_filme(1), MAX_POST),
          "filme2_post.txt": (post_filme(2), MAX_POST), "artigo_titulo.txt": (ARTIGO_TITULO, 100), "artigo.txt": (ARTIGO, 100000),
          "site.txt": (SITE, 100)}
for nome, (t, lim) in TEXTOS.items():
    conferir(nome, t, lim)


# ------------------------------------------------------------------ as imagens e as legendas
def vtt_para_srt(vtt):
    blocos, n = [], 0
    for b in re.split(r"\n\s*\n", vtt.replace("\r", "")):
        linhas = [l for l in b.split("\n") if l.strip()]
        i = next((k for k, l in enumerate(linhas) if "-->" in l), None)
        if i is None:
            continue
        a, z = [x.strip().split(" ")[0] for x in linhas[i].split("-->")]

        def ts(x):
            p = x.split(":")
            if len(p) == 2:
                p = ["00"] + p
            return "%s:%s:%s" % (p[0].zfill(2), p[1].zfill(2), p[2].replace(".", ","))
        n += 1
        blocos.append("%d\n%s --> %s\n%s" % (n, ts(a), ts(z), "\n".join(linhas[i + 1:])))
    if not n:
        falha("VTT sem falas")
    return "\n\n".join(blocos) + "\n", n


def imagem(origem, w, h, destino, y0=330, y1=1320):
    """O funil INTEIRO do pôster do filme 1 (da borda à ponta luminosa: linhas y0..y1 do original 2560x1440, medidas no pôster): escala
    para caber na altura h; se a largura não chega a w, completa as laterais com a cor da borda e uma emenda suave; se passa, corta no centro."""
    from PIL import Image
    im = Image.open(origem).convert("RGB")
    jan = im.crop((0, y0, im.width, y1))
    esc = h / jan.height
    jan = jan.resize((round(jan.width * esc), h), Image.LANCZOS)
    if jan.width >= w:
        x = (jan.width - w) // 2
        out = jan.crop((x, 0, x + w, h))
    else:
        px_l = [jan.getpixel((2, y)) for y in range(0, h, 10)]
        px_r = [jan.getpixel((jan.width - 3, y)) for y in range(0, h, 10)]
        cor = tuple(round(sum(c[k] for c in px_l + px_r) / len(px_l + px_r)) for k in range(3))
        out = Image.new("RGB", (w, h), cor)
        x = (w - jan.width) // 2
        mask = Image.new("L", jan.size, 255)
        f = 60
        for k in range(f):
            v = round(255 * k / f)
            for xx in (k, jan.width - 1 - k):
                mask.paste(v, (xx, 0, xx + 1, h))
        out.paste(jan, (x, 0), mask)
    out.save(destino, "JPEG", quality=92, optimize=True)


ap = argparse.ArgumentParser()
ap.add_argument("--seco", action="store_true")
a = ap.parse_args()
for nome, (t, lim) in TEXTOS.items():
    print("%-18s %6d c  %s" % (nome, len(t), t.splitlines()[0][:90]))
if a.seco:
    print("\n" + FIXADO + "\n\n---\n" + post_filme(1) + "\n\n---\n" + ARTIGO)
    sys.exit(0)
OUT.mkdir(parents=True, exist_ok=True)
stamp = time.strftime("%Y%m%d_%H%M%S")
for p in OUT.glob("*"):
    # 28/10/2026 (Fase 2): o post longo da versao CORRENTE (CUSTODIA_vNNN.txt, escrito pela gerencia) fica e entra no manifesto
    if p.is_file() and not p.name.startswith("_") and p.name != "CUSTODIA_%s.txt" % versao:
        bk = OUT / "_anteriores" / stamp
        bk.mkdir(parents=True, exist_ok=True)
        p.replace(bk / p.name)
for nome, (t, lim) in TEXTOS.items():
    (OUT / nome).write_bytes(t.encode("utf-8"))   # sem quebra final e sem CRLF: o texto é o arquivo inteiro
poster = V7 / "render" / "filme1_poster.jpg"
imagem(poster, 1500, 500, OUT / "capa_1500x500.jpg")
imagem(poster, 1500, 600, OUT / "artigo_capa_1500x600.jpg")
legendas = {}
for n in (1, 2):
    for lang, sub in (("pt-BR", "sync-pt-BR/pt-BR.vtt"), ("en", "sync-pt-BR/en.vtt")):
        srt, k = vtt_para_srt((V7 / "subs" / ("filme%d" % n) / sub).read_text(encoding="utf-8"))
        nome = "filme%d_%s.srt" % (n, lang)
        (OUT / nome).write_bytes(srt.encode("utf-8"))
        legendas[nome] = k


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


man = {"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "gerador": "tools/gerar_vitrine_x.py", "selo": {"versao": versao, "pin_um_py": pin},
       "deposito_zenodo": {"versao": ver_dep, "doi": doi}, "arquivos": {}, "videos": {}, "legendas_falas": legendas}
for p in sorted(OUT.glob("*")):
    if p.is_file() and p.name != "MANIFEST.json":
        man["arquivos"][p.name] = {"bytes": p.stat().st_size, "sha256": sha(p)}
for n in (1, 2):
    for k in ("video", "video_en", "video_720"):
        f = filmes[n][k]
        man["videos"]["filme%d%s" % (n, {"video": "", "video_en": "_en", "video_720": "_720p"}[k])] = {"caminho": str(f), "bytes": f.stat().st_size, "sha256": sha(f),
                                                                           "duracao_s": filmes[n]["dur"], "titulo": filmes[n]["titulo"]}
(OUT / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
print("VITRINE: %d arquivos em %s; MANIFEST sha16 %s" % (len(man["arquivos"]), OUT, sha(OUT / "MANIFEST.json")[:16]))

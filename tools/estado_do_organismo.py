# -*- coding: utf-8 -*-
r"""ESTADO DO ORGANISMO — mede, SÓ POR LEITURA, se cada superfície da IALD carrega o selo corrente do um.py, e diz o que está defasado.
(23/10/2026, sessão a7 da Central; ordem do operador: «atualizei o um.py ... já atualiza tudo automaticamente ... de modo que o sistema já
saiba sempre o que fazer»). O número corrige a frase: a verdade do organismo não é a memória de quem custodiou, é a medida de cada
superfície contra o selo do Nós. Nada é digitado: versão e pino vêm de `um_absoluto_selo.json`; cada superfície é lida no disco ou no ar.
Nenhuma credencial é lida; as leituras no ar são GET públicos.

Superfícies: Nós · espelho the_boundary (disco e GitHub raw) · site da TGL (fonte e ar) · Central privada (cofre, kernel, runner, 16
dispositivos, FINAL, ledger, Atlas, git) · snapshot da bancada · Central pública (3 repositórios, um.acom, /central/, llms) · fila do app ·
mapa de rotas · memória da sessão de gerência · iald.ia.br · segurança do servidor.

Saída: organismo/ESTADO_DO_ORGANISMO.md e .json (o quadro) + resumo no stdout. Exit 0 se tudo OK, 1 se há defasagem, 2 se há falha de leitura.
Uso: python tools/estado_do_organismo.py [--sem-rede]"""
import glob, hashlib, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SEM_REDE = "--sem-rede" in sys.argv
CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TB = Path(r"C:\IALD\Artigo\the_boundary")
ESP = TB / "Um (absoluto) \u2014 Grande Atrator"
BK = Path(r"C:\IALD\Artigo\the_boundary_BACKUPS")
SITE = Path(r"C:\IALD\Site\tgl\v3.0")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
PUB = Path(r"C:\IALD\Central_publica")
MEM = Path.home() / ".claude" / "projects" / "c--IALD-Central-de-Patentes" / "memory"
RAW = "https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/"
URL = "https://teoriadagravitacaoluminodinamica.com/"
OUT = CEN / "organismo"
R = []   # (superficie, item, esperado, achado, status)   status: OK | DEFASADO | FALHA | PENDENTE_OPERADOR | INFO


def sha(p, n=64):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()[:n]


def item(sup, nome, esperado, achado, ok, pendente=False):
    st = "OK" if ok else ("PENDENTE_OPERADOR" if pendente else "DEFASADO")
    R.append((sup, nome, str(esperado), str(achado), st))


def falha(sup, nome, e):
    import traceback
    if os.environ.get("ESTADO_DEBUG"):
        traceback.print_exc()
    tb = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == __file__] or traceback.extract_tb(e.__traceback__)
    onde = ("linha %d: %s" % (tb[-1].lineno, (tb[-1].line or "")[:60])) if tb else ""
    R.append((sup, nome, "-", (repr(e)[:110] + " @ " + onde), "FALHA"))


def info(sup, nome, achado):
    R.append((sup, nome, "-", str(achado), "INFO"))


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


def get(url, binario=False):
    if SEM_REDE:
        raise RuntimeError("--sem-rede")
    rq = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "iald-estado-do-organismo"})
    with urllib.request.urlopen(rq, timeout=30) as r:
        b = r.read()
        return (r.status, dict((k.lower(), v) for k, v in r.getheaders()), b if binario else b.decode("utf-8", "replace"))


def head(url):
    if SEM_REDE:
        raise RuntimeError("--sem-rede")
    import http.client, urllib.parse
    u = urllib.parse.urlsplit(url)
    C = http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection
    c = C(u.hostname, u.port, timeout=30)      # a porta explícita (os serviços locais não estão na 80)
    try:
        c.request("GET", u.path or "/", headers={"Cache-Control": "no-cache", "User-Agent": "iald-estado-do-organismo"})
        r = c.getresponse(); r.read()
        return r.status, dict((k.lower(), v) for k, v in r.getheaders())
    finally:
        c.close()


def rede(sup, nome, fn):
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        R.append((sup, nome, "-", "sem leitura no ar: " + repr(e)[:80], "FALHA"))


# ---------------- 0. o selo (a verdade) ----------------
selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
V, PIN = selo["um_version"], selo["sha256"]["um.py"]
PIN16, N, TS = PIN[:16], int(V[1:]), selo.get("timestamp", "")
SELO_DIA = TS[:10].replace("-", "")
info("Nós", "selo corrente", "%s %s (%s) — %s" % (V, PIN16, TS, selo.get("qg_closure_verdict", "")[:60]))
_pin_nos = sha(NOS / "um.py", 16)
if _pin_nos == PIN16:
    item("Nós", "um.py do Nós = o selo", PIN16, _pin_nos, True)
else:   # a casa está no meio de uma versão (a gerência c1 trabalha no um.py depois do selo): estado, não erro — o vigia (G2) espera o selo novo
    R.append(("Nós", "um.py do Nós = o selo", PIN16, _pin_nos + " — EM OBRA: a casa trabalha na versão seguinte; o quadro mede contra o último selo", "EM_OBRA"))
diario = (NOS / "MEMORIA_DA_LINHAGEM.md").read_text(encoding="utf-8")
vs = re.findall(r"^## [^\n]*\*\*(v\d{3,}) SELADA", diario, re.M)
item("Nós", "diário da linhagem: última versão selada", V, vs[-1] if vs else "?", bool(vs) and vs[-1] == V)
item("Nós", "handoff de custódia HANDOFF_%s_CUSTODIA.md" % V, "existe", (NOS / ("HANDOFF_%s_CUSTODIA.md" % V)).is_file(), (NOS / ("HANDOFF_%s_CUSTODIA.md" % V)).is_file())
item("Nós", "rodada_%s_stdout.txt (o stdout canônico)" % V, "existe", (NOS / ("rodada_%s_stdout.txt" % V)).is_file(), (NOS / ("rodada_%s_stdout.txt" % V)).is_file())
item("Nós", "cadeia de selo work/cadeia_de_selo/%s" % V, "existe", (CEN / "work" / "cadeia_de_selo" / V).is_dir(), (CEN / "work" / "cadeia_de_selo" / V).is_dir())

# ---------------- 1. espelho the_boundary ----------------
try:
    se = json.loads((ESP / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    pe = sha(ESP / "um.py", 16)
    item("Espelho", "um.py do espelho = pino do Nós", PIN16, pe, pe == PIN16)
    item("Espelho", "selo do espelho um_version", V, se.get("um_version"), se.get("um_version") == V)
    bks = sorted(BK.glob("um_v%d_*" % (N - 1)))
    item("Espelho", "backup da versão anterior fora do repo (um_v%d_*)" % (N - 1), "existe", bool(bks), bool(bks))
    for nome, pat in (("LEDGER.md", "### The custody \u2014 %s" % V), ("ESTADO_ATUAL.md", PIN16), ("CITATION.cff", PIN), ("README.md", PIN16)):
        t = (TB / nome).read_text(encoding="utf-8", errors="replace")
        item("Espelho", "%s traz o selo corrente" % nome, "sim", pat in t, pat in t)
    for d in ("diferencas_%s" % V, "recibos_bancada_%s" % V):
        item("Espelho", d, "existe", (ESP / d).is_dir(), (ESP / d).is_dir())
    h, o = git(TB, "rev-parse", "--short=8", "HEAD"), git(TB, "rev-parse", "--short=8", "origin/main")
    pend = git(TB, "status", "--porcelain", "--untracked-files=no")
    item("Espelho", "git: HEAD = origin/main e nada pendente", "sim", "%s/%s%s" % (h, o, " | pendente" if pend else ""), h == o and not pend)
except Exception as e:  # noqa: BLE001
    falha("Espelho", "leitura", e)
rede("Espelho (GitHub raw)", "README raw traz o pino", lambda: item("Espelho (GitHub raw)", "README raw traz o pino", PIN16, "sim" if PIN16 in get(RAW + "README.md")[2] else "não", PIN16 in get(RAW + "README.md")[2]))
rede("Espelho (GitHub raw)", "selo raw um_version", lambda: item("Espelho (GitHub raw)", "selo raw um_version", V, json.loads(get(RAW + "Um%20(absoluto)%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json")[2]).get("um_version"), json.loads(get(RAW + "Um%20(absoluto)%20%E2%80%94%20Grande%20Atrator/um_absoluto_selo.json")[2]).get("um_version") == V))

# ---------------- 2. site da TGL (fonte e ar) ----------------
try:
    idx = (SITE / "index.html").read_text(encoding="utf-8", errors="replace")
    i18 = (SITE / "i18n.js").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Current seal: <strong>(v\d{3})</strong>, pin <span class=\"notranslate\">([0-9a-f]{16})", idx)
    item("Site (fonte)", "nota «Current seal» do index", "%s %s" % (V, PIN16), ("%s %s" % m.groups()) if m else "?", bool(m) and m.groups() == (V, PIN16))
    item("Site (fonte)", "data-selo pin do index", PIN16, PIN16 in idx, PIN16 in idx)
    item("Site (fonte)", "linha do arco art.c.cl.arc%d (index e i18n)" % N, "sim", ('data-i18n="art.c.cl.arc%d"' % N in idx, "'art.c.cl.arc%d'" % N in i18), 'data-i18n="art.c.cl.arc%d"' % N in idx and "'art.c.cl.arc%d'" % N in i18)
    for nome in ("read-brief.md", "llms.txt", "llms-full.txt", "index.md"):
        p = SITE / nome
        t = p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""
        item("Site (fonte)", "%s traz o pino" % nome, PIN16, PIN16 in t, PIN16 in t)
    ht = (SITE / ".htaccess").read_text(encoding="utf-8", errors="replace")
    item("Site (fonte)", ".htaccess com o bloco IALD-SEGURANCA-ESTATICO", "sim", "IALD-SEGURANCA-ESTATICO" in ht, "IALD-SEGURANCA-ESTATICO" in ht)
    subs = sorted((d for d in (BANC / "subidas").iterdir() if d.is_dir() and not d.name.endswith("_dryrun")), key=lambda d: d.name)
    sem_rel = [d.name for d in subs if not (d / "RELATORIO.md").is_file()]     # subida interrompida ou em curso: dita, não é «ok» nem erro
    if sem_rel:
        info("Site (fonte)", "pastas de subida sem RELATORIO.md (interrompidas ou em curso)", sem_rel[-3:])
    subs = [d for d in subs if (d / "RELATORIO.md").is_file()]
    ult = subs[-1] if subs else None
    rel_ok = ult and "SUBIDA VERIFICADA" in (ult / "RELATORIO.md").read_text(encoding="utf-8", errors="replace")
    t_sub = time.mktime(time.strptime(ult.name[:15], "%Y%m%d_%H%M%S")) if ult else 0
    mais_novo = 0.0
    for dp, dns, fns in os.walk("\\\\?\\" + str(SITE)):      # caminhos longos em central/ (prefixo \\?\)
        for f in fns:
            if ".bak_" in f or ".tmp" in f:
                continue
            try:
                mais_novo = max(mais_novo, os.path.getmtime(os.path.join(dp, f)))
            except OSError:
                pass
    item("Site (fonte)", "última subida verificada", "SUBIDA VERIFICADA", ult.name if ult else "nenhuma", bool(rel_ok))
    item("Site (fonte)", "nenhum arquivo da fonte mais novo que a última subida", "fonte ≤ subida", "fonte %s | subida %s" % (time.strftime("%d/%m %H:%M", time.localtime(mais_novo)), ult.name[:15] if ult else "-"), mais_novo <= t_sub + 120)
except Exception as e:  # noqa: BLE001
    falha("Site (fonte)", "leitura", e)


def _site_ar():
    st, hd, body = get(URL)
    item("Site (ar)", "index no ar diz «%s · %s»" % (V, PIN16), "sim", ("%s \u00b7 %s" % (V, PIN16)) in body, ("%s \u00b7 %s" % (V, PIN16)) in body)
    for k in ("strict-transport-security", "x-content-type-options", "x-frame-options"):
        item("Site (ar)", "cabeçalho %s" % k, "presente", hd.get(k, "ausente"), k in hd)
    for nome in ("llms.txt", "read-brief.md"):
        item("Site (ar)", "%s no ar traz o pino" % nome, PIN16, PIN16 in get(URL + nome)[2], PIN16 in get(URL + nome)[2])
    s2, h2 = head(URL + "x.php")
    item("Site (ar)", "/x.php → 403 sem X-Powered-By (o PHP não recebe o pedido)", "403 e sem cabeçalho", "%s %s" % (s2, "com X-Powered-By" if "x-powered-by" in h2 else "sem"), s2 == 403 and "x-powered-by" not in h2)
    s3, h3 = head("http://teoriadagravitacaoluminodinamica.com/")
    item("Site (ar)", "http → 301 https", "301", "%s %s" % (s3, h3.get("location", "")), s3 == 301)
    hs = hd.get("strict-transport-security", "")
    item("Site (ar)", "HSTS fase 2 (max-age=31536000)", "31536000", hs, "31536000" in hs, pendente=True)


rede("Site (ar)", "leitura do ar", _site_ar)

# ---------------- 3. Central privada ----------------
try:
    OC = CEN / "vault" / "originals_copy"
    cm = OC / ("um_unificado_%s" % V) / "CUSTODY_MANIFEST.json"
    km = OC / ("tgl_kernel_%s" % V) / "CUSTODY_MANIFEST.json"
    item("Central privada", "cofre um_unificado_%s (pino)" % V, PIN16, json.loads(cm.read_text(encoding="utf-8")).get("um_py_pin", "?")[:16] if cm.is_file() else "ausente", cm.is_file() and json.loads(cm.read_text(encoding="utf-8")).get("um_py_pin") == PIN)
    kj = json.loads(km.read_text(encoding="utf-8")) if km.is_file() else {}
    item("Central privada", "cofre tgl_kernel_%s" % V, "existe", "%s formais / %s declarações" % (kj.get("formal_files"), kj.get("declaracoes_no_axiom_report")) if kj else "ausente", bool(kj))
    run = (CEN / "fronteira_tgl" / "runner" / "one_fronteira.py").read_text(encoding="utf-8", errors="replace")
    item("Central privada", "runner da Fronteira lê o cofre %s (pedra _medir_%s_custodia)" % (V, V), "sim", "_medir_%s_custodia" % V in run, "_medir_%s_custodia" % V in run)
    res = sorted(glob.glob(str(CEN / "fronteira_tgl" / "results" / "fronteira_*.json")), key=os.path.getmtime)
    vf = json.loads(open(res[-1], encoding="utf-8").read()).get("verdict", "") if res else ""
    item("Central privada", "último resultado do runner", "FRONTEIRA_SINCRONIZADA_%s…" % V.upper(), vf[:40], vf.startswith("FRONTEIRA_SINCRONIZADA_%s" % V.upper()))
    fm = (CEN / "patents" / "_formula_completa" / "tgl_formula_completa.py")
    mcam = re.search(r'VERSAO_DA_CAMADA = "(v\d{3})"', fm.read_text(encoding="utf-8", errors="replace"))
    item("Central privada", "camada do módulo comum dos 16 dispositivos", V, mcam.group(1) if mcam else "?", bool(mcam) and mcam.group(1) == V)
    n_disp = 0
    pats = sorted(glob.glob(str(CEN / "patents" / "BR*")))
    for pat in pats:
        rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
        if rs and ('"camada_%s_no_cofre"' % V) in open(rs[-1], encoding="utf-8", errors="replace").read():
            n_disp += 1
    item("Central privada", "dispositivos com a camada %s no último resultado" % V, "16/16", "%d/16" % n_disp, n_disp == 16)
    fins = glob.glob(str(CEN / "patents" / "*" / "*_FINAL.manifest.json"))
    n_fin = sum(1 for f in fins if os.path.getmtime(f) >= os.path.getmtime(fm))
    item("Central privada", "FINAL regerados depois da camada corrente", "16/16", "%d/%d" % (n_fin, len(fins)), n_fin == 16)
    led = json.loads((CEN / "fronteira_tgl" / "ledger_de_pinos.json").read_text(encoding="utf-8"))
    item("Central privada", "ledger de pinos no kernel %s, sem erros" % V, "sim", "erros %s | %s" % (led.get("erros"), "kernel %s" % V if V in json.dumps(led) else "kernel ≠ %s" % V), led.get("erros") == 0 and V in json.dumps(led))
    atlas = (CEN / "memory" / "TGL_ATLAS.md").read_text(encoding="utf-8", errors="replace")
    item("Central privada", "Atlas §X registra a custódia da %s" % V, "sim", "A CUSTÓDIA DA %s" % V in atlas, "A CUSTÓDIA DA %s" % V in atlas)
    h, o = git(CEN, "rev-parse", "--short=8", "HEAD"), git(CEN, "rev-parse", "--short=8", "origin/main")
    pend = git(CEN, "status", "--porcelain", "--untracked-files=no", "--", "vault/originals_copy", "fronteira_tgl", "patents/_formula_completa", "memory/TGL_ATLAS.md")
    item("Central privada", "git: HEAD = origin/main e nada pendente nos caminhos da custódia", "sim", "%s/%s%s" % (h, o, " | pendente: " + pend[:60] if pend else ""), h == o and not pend)
    snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
    sm = json.loads(open(os.path.join(snaps[-1], "MANIFEST.json"), encoding="utf-8").read()) if snaps else {}
    item("Central privada", "snapshot da bancada Chatgpt/ posterior ao selo", "≥ %s" % SELO_DIA, sm.get("snapshot", "nenhum")[:15], str(sm.get("snapshot", ""))[:8] >= SELO_DIA and sm.get("conferido_contra_origem") is True)
except Exception as e:  # noqa: BLE001
    falha("Central privada", "leitura", e)

# ---------------- 4. Central pública ----------------
try:
    for r in ("central-publica", "central-publica-work", "central-publica-bancada"):
        d = PUB / r
        h, o = git(d, "rev-parse", "--short=8", "HEAD"), git(d, "rev-parse", "--short=8", "origin/main")
        pend = git(d, "status", "--porcelain", "--untracked-files=no")
        rd = (d / "README.md").read_text(encoding="utf-8", errors="replace")
        n = json.loads((d / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["n_arquivos"]
        item("Central pública", "%s: git HEAD = origin/main, nada pendente" % r, "sim", "%s/%s%s" % (h, o, " | pendente" if pend else ""), h == o and not pend)
        item("Central pública", "%s: README com o pino" % r, PIN16, PIN16 in rd, PIN16 in rd)
        item("Central pública", "%s: llms.txt rastreado" % r, "sim", bool(git(d, "ls-files", "llms.txt")), bool(git(d, "ls-files", "llms.txt")))
        info("Central pública", "%s: arquivos no índice" % r, n)
    ai = json.loads((BANC / "central_publica" / "acom" / "um_acom_info.json").read_text(encoding="utf-8"))
    ger = time.mktime(time.strptime(ai["gerado_em"], "%d/%m/%Y %H:%M"))
    t_selo = time.mktime(time.strptime(TS, "%Y-%m-%d %H:%M:%S"))
    item("Central pública", "um.acom público gerado depois do selo", "≥ %s" % TS, "%s (sha %s)" % (ai["gerado_em"], ai["sha256"][:16]), ger >= t_selo)
    ACOM16 = ai["sha256"][:16]
    sc = SITE / "central" / "um.acom"
    item("Central pública", "um.acom montado no site = o gerado", ACOM16, sha(sc, 16) if sc.is_file() else "ausente", sc.is_file() and sha(sc, 16) == ACOM16)
    lp = (SITE / "linhas-de-pesquisa.html").read_text(encoding="utf-8", errors="replace")
    item("Central pública", "cartão das linhas de pesquisa com o sha do um.acom", ACOM16, ACOM16 in lp, ACOM16 in lp)
    ll = (SITE / "llms.txt").read_text(encoding="utf-8", errors="replace")
    item("Central pública", "llms.txt do site cita o um.acom corrente", ACOM16, ACOM16 in ll, ACOM16 in ll)
    sync = glob.glob(str(CEN / "work" / ("scientific_memory_sync_*_%s" % V) / "DELIVERY_R1.json"))
    item("App (fila científica)", "memória científica da fila sincronizada à %s" % V, "DELIVERY_R1.json", os.path.basename(os.path.dirname(sync[0])) if sync else "nenhuma", bool(sync))

    def _pub_ar():
        st, hd, b = get(URL + "central/um_acom_info.json")
        item("Central pública (ar)", "/central/um_acom_info.json no ar = o gerado", ACOM16, json.loads(b)["sha256"][:16], json.loads(b)["sha256"][:16] == ACOM16)
        item("Central pública (ar)", "linhas-de-pesquisa no ar com o sha do um.acom", ACOM16, ACOM16 in get(URL + "linhas-de-pesquisa.html")[2], ACOM16 in get(URL + "linhas-de-pesquisa.html")[2])
        s, _, _ = get(URL + "central/")
        item("Central pública (ar)", "/central/ responde", 200, s, s == 200)
        for r in ("central-publica", "central-publica-work", "central-publica-bancada"):
            rr = get("https://raw.githubusercontent.com/rotolimiguel-iald/%s/main/README.md" % r)[2]
            item("Central pública (ar)", "%s: README raw com o pino" % r, PIN16, PIN16 in rr, PIN16 in rr)
    rede("Central pública (ar)", "leitura do ar", _pub_ar)
except Exception as e:  # noqa: BLE001
    falha("Central pública", "leitura", e)

# ---------------- 5. iald.ia.br (ato do operador onde marcado) ----------------
def _iald():
    s1, _ = head("https://iald.ia.br/llms.txt")
    item("iald.ia.br", "llms.txt no ar (Kimi, 23/10)", 200, s1, s1 == 200, pendente=True)
    s2, _ = head("https://iald.ia.br/sitemap.xml")
    item("iald.ia.br", "sitemap.xml no ar (Kimi, 23/10)", 200, s2, s2 == 200, pendente=True)
    s3, h3 = head("https://iald.ia.br/x.php")
    item("iald.ia.br", "/x.php não chega ao PHP (segurança)", "sem X-Powered-By", "%s %s" % (s3, h3.get("x-powered-by", "sem")), "x-powered-by" not in h3, pendente=True)
    try:                                   # 23/10/2026: a origem serve página de erro no robots.txt (404) — isso não pode derrubar a leitura inteira
        rb = get("https://iald.ia.br/robots.txt")[2]
        st_rb = 200
    except Exception as e:  # noqa: BLE001
        rb, st_rb = "", getattr(e, "code", type(e).__name__)
    item("iald.ia.br", "robots.txt no ar (ORDEM 020 C: upload pelo painel da hospedagem)", 200, st_rb, st_rb == 200, pendente=True)
    bloq = bool(re.search(r"User-agent: ClaudeBot\s+Disallow: /", rb))
    item("iald.ia.br", "robots.txt não bloqueia os leitores de IA (Cloudflare)", "sem Disallow para ClaudeBot/GPTBot", ("bloqueia" if bloq else "não bloqueia") + ("" if st_rb == 200 else " (sem robots: tratado como permitido)"), not bloq, pendente=True)
    # (23/10/2026, ordem do operador: «tudo que eu quero é justamente a IA lendo meu repositório») — a borda responde 200 a um leitor de IA?
    import http.client as _hc
    for host, caminho in (("iald.ia.br", "/"), ("teoriadagravitacaoluminodinamica.com", "/llms.txt")):
        for ua in ("ClaudeBot/1.0", "GPTBot/1.0"):
            try:
                cx = _hc.HTTPSConnection(host, timeout=30)
                cx.request("GET", caminho, headers={"User-Agent": "Mozilla/5.0 (compatible; %s; +https://example.invalid/bot)" % ua, "Cache-Control": "no-cache"})
                rr = cx.getresponse(); rr.read(); st = rr.status; cx.close()
            except Exception as e:  # noqa: BLE001
                st = "sem resposta (%s)" % type(e).__name__
            item("Leitura por IA", "%s%s responde a %s" % (host, caminho, ua.split("/")[0]), 200, st, st == 200, pendente=(host == "iald.ia.br"))


rede("iald.ia.br", "leitura do ar", _iald)

# ---------------- 6. mapa de rotas e memória da gerência ----------------
try:
    rot = (Path(r"C:\IALD\MAPA_DE_ROTAS") / "rotas.jsonl").read_text(encoding="utf-8", errors="replace")
    item("Mapa de rotas", "rota custodia.%s" % V, "existe", '"custodia.%s"' % V in rot, '"custodia.%s"' % V in rot)
    mm = (MEM / "MEMORY.md").read_text(encoding="utf-8", errors="replace")
    lin = [l for l in mm.splitlines() if ("HANDOFF %s" % V) in l]
    item("Memória da gerência", "MEMORY.md: linha do HANDOFF %s diz CUSTODIADO/PUBLICADA" % V, "sim", (lin[0][:90] + "…") if lin else "sem linha", bool(lin) and ("CUSTODIADO" in lin[0] or "PUBLICADA" in lin[0]))
    item("Memória da gerência", "handoff-%s-custodia.md" % V, "existe", (MEM / ("handoff-%s-custodia.md" % V)).is_file(), (MEM / ("handoff-%s-custodia.md" % V)).is_file())
except Exception as e:  # noqa: BLE001
    falha("Memória da gerência", "leitura", e)

# ---------------- 7. as outras superfícies do organismo (apontadas pelo cético de completude em 23/10/2026) ----------------
try:
    t_selo = time.mktime(time.strptime(TS, "%Y-%m-%d %H:%M:%S"))
    nv = Path(r"C:\IALD\NOS_VIVO") / "nos_vivo.sqlite3"
    item("Nós vivo", "banco nos_vivo.sqlite3 gravado depois do selo", "≥ %s" % TS, time.strftime("%Y-%m-%d %H:%M", time.localtime(nv.stat().st_mtime)) if nv.is_file() else "ausente", nv.is_file() and nv.stat().st_mtime >= t_selo)
    for nome in ("MEMORIA_DA_LINHAGEM.md", "DESENHO_DO_FECHAMENTO_QG.md"):       # a regra da linhagem completa: grep -c vNNN em cada superfície
        p = NOS / nome
        c = p.read_text(encoding="utf-8", errors="replace").count(V) if p.is_file() else -1
        item("Linhagem", "%s conhece a %s (ocorrências)" % (nome, V), "≥ 1", c, c >= 1)
    TUN = CEN / "Chatgpt" / "TUNEL"
    abertas = [d.name for d in sorted((TUN / "DO_CHATGPT").glob("ORDEM_*")) if d.is_dir() and not list(d.rglob("RESULTADO*.json"))]
    info("Túneis", "ordens do Codex em DO_CHATGPT sem RESULTADO", abertas or "nenhuma")
    ult = max((p.stat().st_mtime for p in (TUN / "DO_CHATGPT").rglob("*") if p.is_file()), default=0)
    info("Túneis", "última entrega do Codex no túnel", time.strftime("%Y-%m-%d %H:%M", time.localtime(ult)) if ult else "nenhuma")
    inv = CEN / "memory" / "INVENTARIO_BANCADA_CHATGPT.json"
    info("Bancada ChatGPT", "inventário da bancada (última regeneração)", time.strftime("%Y-%m-%d %H:%M", time.localtime(inv.stat().st_mtime)) if inv.is_file() else "ausente")
    # a obrigação diária da IALD no X (ordem do operador de 23/10/2026): o recibo do dia e a tarefa das 17:30
    hoje = time.strftime("%Y-%m-%d")
    rx = TUN / "DO_CHATGPT" / "ORDEM_021" / ("%s.json" % hoje)
    if rx.is_file():
        dx = json.loads(rx.read_text(encoding="utf-8", errors="replace"))
        item("X diário", "pensamento de hoje publicado (recibo do Codex)", "publicado: true, URL", "publicado: %s %s" % (dx.get("publicado"), str(dx.get("url", ""))[:60]), dx.get("publicado") is True)
    elif time.localtime().tm_hour * 60 + time.localtime().tm_min < 18 * 60 + 30:
        info("X diário", "pensamento de hoje (publica-se às 18:00; recibo ainda não devido)", "texto do dia: %s" % ("pronto" if (TUN / "PARA_CHATGPT" / "X_DIARIO" / ("%s.md" % hoje)).is_file() else "ainda não"))
    else:
        item("X diário", "pensamento de hoje publicado (recibo do Codex)", "publicado: true até 18:30", "sem recibo", False)
    qx = subprocess.run(["schtasks", "/Query", "/TN", "IALD_pensamento_do_dia"], capture_output=True, timeout=30)   # bytes: o console do Windows nao e UTF-8
    item("X diário", "tarefa agendada IALD_pensamento_do_dia (17:30)", "existe", "existe" if qx.returncode == 0 else "ausente", qx.returncode == 0)
    # 24/10/2026: as pernas que o SELO já puxa fora desta cadeia — a Bancada Um (B(n) a cada versão selada) e a memória canônica da fila
    recs = sorted(Path("C:/IALD/Bancada_Um/estado/sincronizacao").glob("RECIBO_SINCRONIZACAO_v*.json"), key=lambda p: p.stat().st_mtime)
    if recs:
        mrb = re.search(r"RECIBO_SINCRONIZACAO_(v\d{3})_", recs[-1].name)
        vb = mrb.group(1) if mrb else "?"
        try:
            vd = str((json.loads(recs[-1].read_text(encoding="utf-8", errors="replace")) or {}).get("veredito") or "")[:60]
        except Exception:  # noqa: BLE001
            vd = "?"
        item("Bancada Um", "último recibo B(n) da sincronização = selo corrente", V, "%s (%s; %s)" % (vb, recs[-1].name[-20:-5], vd), vb == V)
    else:
        item("Bancada Um", "último recibo B(n) da sincronização = selo corrente", V, "nenhum recibo", False)
    act = Path("C:/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/state/canonical_memory/ACTIVE.json")
    try:
        rel = str(json.loads(act.read_text(encoding="utf-8", errors="replace")).get("release") or "?")
    except Exception as e:  # noqa: BLE001
        rel = "sem leitura (%s)" % type(e).__name__
    item("Memória canônica (fila)", "ACTIVE.json release = selo corrente", V, rel, rel == V)
    # 24/10/2026: o APP tem pacote de ciência próprio (iald_nucleo_fixo.json), fora da cadeia até a release entrar nela (G1)
    nuc = Path("C:/IALD/projetos_pyhton/IALD/iald_nucleo_fixo.json")
    try:
        nj = json.loads(nuc.read_text(encoding="utf-8", errors="replace"))
        rel_app = str(((nj.get("operational_core") or {}).get("current_release")) or ((nj.get("active_cluster") or {}).get("release")) or "?")
    except Exception as e:  # noqa: BLE001
        rel_app = "sem leitura (%s)" % type(e).__name__
    item("App IALD (ciência própria)", "release instalada no app = selo corrente (release do app: pipeline work/iald_vNNN_*/app)", V, rel_app, rel_app == V)
    cff = (TB / "CITATION.cff").read_text(encoding="utf-8", errors="replace")
    mz = re.search(r"Zenodo deposit holds (v\d{3})", cff)
    item("Zenodo", "versão depositada = selo corrente (depósito é ato do operador)", V, mz.group(1) if mz else "?", bool(mz) and mz.group(1) == V, pendente=True)
    smp = SITE / "sitemap.xml"
    sm = smp.read_text(encoding="utf-8", errors="replace") if smp.is_file() else ""
    item("Site (fonte)", "sitemap.xml lista /central/", "sim", "/central/" in sm, "/central/" in sm)
    lei = sorted((BANC / "revisoes").glob("leitor_ia_*.md"), key=lambda p: p.stat().st_mtime)
    lt = lei[-1].read_text(encoding="utf-8", errors="replace") if lei else ""
    lei_ok = bool(lei) and "PASSA" in lt and lei[-1].stat().st_mtime >= t_selo      # o relatório do leitor não traz o pino; vale PASSA depois do selo
    item("Site (fonte)", "último leitor de IA passa, rodado depois do selo", "PASSA, ≥ %s" % TS, (lei[-1].name if lei else "nenhum") + (" PASSA" if "PASSA" in lt else " ?"), lei_ok)
except Exception as e:  # noqa: BLE001
    falha("Organismo (outras)", "leitura", e)


def _locais():
    for nome, url, obrig in (("Central (backend local :8765)", "http://127.0.0.1:8765/api/health", True), ("IALD nativa (web :8082)", "http://127.0.0.1:8082/", True),
                             ("IALD nativa (modelo :8081)", "http://127.0.0.1:8081/", False)):
        try:
            st, _ = head(url)
            ach = st
        except Exception as e:  # noqa: BLE001
            ach, st = "sem resposta (%s)" % type(e).__name__, 599
        if obrig:
            item("Serviços locais", nome, "responde", ach, st < 500)
        else:
            info("Serviços locais", nome, ach)


if not SEM_REDE:
    _locais()

# ---------------- o quadro ----------------
OUT.mkdir(exist_ok=True)
cont = {}
for _, _, _, _, st in R:
    cont[st] = cont.get(st, 0) + 1
falta = [(s, n, e, a) for s, n, e, a, st in R if st == "DEFASADO"]
pend = [(s, n, e, a) for s, n, e, a, st in R if st == "PENDENTE_OPERADOR"]
falh = [(s, n, a) for s, n, e, a, st in R if st == "FALHA"]
agora = time.strftime("%Y-%m-%d %H:%M:%S")
md = ["# ESTADO DO ORGANISMO — %s" % agora, "",
      "Selo corrente (a verdade, lida do Nós): **%s** `%s` (%s). Medido só por leitura; nenhuma credencial lida. Gerado por `tools/estado_do_organismo.py`." % (V, PIN16, TS), "",
      "**Resumo:** %s" % " · ".join("%s %d" % (k, v) for k, v in sorted(cont.items())), ""]
if falta:
    md += ["## O que está DEFASADO (o que o organismo tem de fazer)", ""] + ["- **%s** — %s: esperado `%s`, achado `%s`" % x for x in falta] + [""]
if pend:
    md += ["## Pendente do operador (painel, hospedagem, decisão)", ""] + ["- **%s** — %s: esperado `%s`, achado `%s`" % x for x in pend] + [""]
obra = [(s, n, a) for s, n, e, a, st in R if st == "EM_OBRA"]
if obra:
    md += ["## Em obra (a casa trabalha na versão seguinte; nada a custodiar até o selo novo)", ""] + ["- **%s** — %s: %s" % x for x in obra] + [""]
if falh:
    md += ["## Sem leitura (falha de rede ou de disco — não é «ok»)", ""] + ["- **%s** — %s: %s" % x for x in falh] + [""]
md += ["## Quadro completo", "", "| superfície | item | esperado | achado | estado |", "|---|---|---|---|---|"]
md += ["| %s | %s | %s | %s | %s |" % tuple(str(x).replace("|", "\\|")[:140] for x in r) for r in R]
md.append("")
(OUT / "ESTADO_DO_ORGANISMO.md").write_text("\n".join(md), encoding="utf-8")
(OUT / "ESTADO_DO_ORGANISMO.json").write_text(json.dumps({"medido_em": agora, "selo": {"versao": V, "pin": PIN, "timestamp": TS}, "resumo": cont,
                                                         "itens": [dict(zip(("superficie", "item", "esperado", "achado", "estado"), r)) for r in R]},
                                                        ensure_ascii=False, indent=1), encoding="utf-8")
print("ESTADO DO ORGANISMO %s %s | %s | quadro: %s" % (V, PIN16, " · ".join("%s %d" % (k, v) for k, v in sorted(cont.items())), OUT / "ESTADO_DO_ORGANISMO.md"))
for x in falta:
    print("  DEFASADO  %s — %s: esperado %s, achado %s" % x)
for x in pend:
    print("  OPERADOR  %s — %s: achado %s" % (x[0], x[1], x[3]))
for x in falh:
    print("  FALHA     %s — %s: %s" % x)
for x in obra:
    print("  EM_OBRA   %s — %s: %s" % x)
sys.exit(2 if falh else (1 if falta else 0))

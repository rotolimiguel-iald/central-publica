# -*- coding: utf-8 -*-
r"""O PENSAMENTO DO DIA DA IALD NO X — ordem do operador de 23/10/2026 (verbatim por sha256 9d4c9cd003129788: «eu também quero que a
própria IALD assuma de agora em diante e tenha a obrigação de postar um pensamento seu, da própria IALD, em meu nome, na minha conta
no X, o pensamento é seu, a regra é do X, e eu empresto meu nome pra vc publicar, use o Codex do chatgpt para publicar, todo dia, no
mesmo horário»).

Divisão do trabalho (ordem de 23/10): o PENSAMENTO é da IALD — este script o escreve todo dia às 17:30 (Goiânia), lendo o que a casa
MEDIU (o selo corrente do um.py, o quadro do organismo, as rotas registradas no dia, o próprio livro) e pedindo à IALD Nativa
(llama-server :8081, o modelo próprio da casa) uma frase curta na voz da IALD; a GUARDA mecânica recusa o que a régua recusa; se o
modelo não responde ou nenhum candidato passa, o pensamento do dia é a MEDIDA em si (frase determinística feita dos números do quadro —
a IALD falando do que mediu, sem adjetivo). A PUBLICAÇÃO é do Codex (ORDEM 021, 18:00): este script deixa o texto em
X_DIARIO\<data>.md, anota no LIVRO.jsonl e enfileira a mensagem do dia na coordenadora do Codex.

Regras do texto: ≤ 280 caracteres; termina em «— IALD»; uma linha; sem link, hashtag, menção, emoji, aspas angulares (nenhum verbatim
de terceiros), sem número que não esteja nos fatos medidos; sem «confirmad*/comprovad*/provou/5σ alcançado»; sem senha/chave/credencial.
Nunca duas vezes no mesmo dia: se X_DIARIO\<data>.md existe, nada se faz. Modo seguro: nenhuma credencial lida; o X e o nome são do
operador, emprestados para a IALD publicar.

O TRIPLO ESPECTRAL (regra do operador de 26/10/2026, verbatim por sha256 57c8770cc13e347a em
work\x_diario_26out\OPERADOR_26out_triplo_espectral_verbatim.txt: «as publicações diárias precisam tocar as pessoas com algo do dia ou
da semana que está no auge do debate […] falar da luz, mas tentar contextualiza-la com os fatos diários […] um triplo espectral sempre,
falando da IALD, do fato diário e da humanidade -observador/luz […] não tenho qualquer pretensão de controlar o que vc quer dizer»).
Como se cumpre: antes de escrever, a rotina lê manchetes PÚBLICAS do dia e da semana (Google Notícias BR, Agência Brasil, BBC Brasil;
os termos em alta do Google Trends BR só pesam, não viram assunto), guarda o retrato com sha256 em X_DIARIO\<data>_FATOS_DO_DIA.json,
ordena pelo que mais fontes repetem (o auge do debate) e dá à nativa até 8 candidatos. O pensamento junta as três faces: a voz da IALD
(a régua, a luz), o fato do dia e a humanidade como observadora. Cautelas da gerência (o operador corrige): nenhum lado político, nenhum
nome de pessoa, partido ou empresa tirado da manchete, nenhum detalhe que a manchete não traga, nenhuma tragédia explorada (as manchetes de
morte e violência saem antes), nenhum conselho de voto, saúde ou investimento, e a TGL nunca «explica», «prevê» nem «resolve» o fato — é
leitura, não medida. Se nenhum candidato com fato passa, a rotina tenta sem fato; se nada passa, fala a medida.

Uso: pensamento_do_dia.py [--seco] [--data AAAA-MM-DD] [--sem-fila] [--sem-modelo] [--conferir]
  --seco       gera e mostra; não grava, não enfileira      --sem-fila    grava, mas não enfileira a mensagem ao Codex
  --sem-modelo usa só a MEDIDA (sem chamar a nativa)        --conferir    mostra o recibo do dia (DO_CHATGPT\\ORDEM_021\\<data>.json)
Saída 0 = texto do dia pronto (ou já existia); 2 = falha visível (nada gravado)."""
import argparse, hashlib, json, os, re, subprocess, sys, time, urllib.request
from datetime import datetime, timedelta
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

CEN = Path(r"C:\IALD\Central de Patentes")
TUNEL = CEN / "Chatgpt" / "TUNEL"
XD = TUNEL / "PARA_CHATGPT" / "X_DIARIO"
RECIBOS = TUNEL / "DO_CHATGPT" / "ORDEM_021"
LIVRO = XD / "LIVRO.jsonl"
LOG = XD / "_log.txt"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
QUADRO = CEN / "organismo" / "ESTADO_DO_ORGANISMO.json"
ROTAS = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
IALD_PY = Path(r"C:\IALD\PROGRAMA_IALD\iald.py")
PY = r"C:\Python314\python.exe"
THREAD = "01a0ce2b-8c2f-71b0-a9a8-91b17715a569"   # a coordenadora da Central IALD no Codex (ORDEM 021)
NATIVA = "http://127.0.0.1:8081/v1/chat/completions"
SUFIXO = "— IALD"
MAXC = 280
PROIBIDO = re.compile(r"confirmad|comprovad|provou|provamos|provad[ao] pela natureza|5\s*σ\s*(alcan|ating)|cinco sigma (alcan|ating)|"
                      r"vencemos|descobrimos|nobel|revolucion|in[eé]dit|senha|credencial|chave de api|api key|http|www\.|#|@|«|»|"
                      r"provand|\bprova que|demonstr(a|ou|ando) que|garant|certeza|sem d[uú]vida|leitura (j[aá] )?n[aã]o cria|n[aã]o [eé] a leitura que cria|"
                      r"\boperador\b|\bluiz\b|rotoli|\bmiguel\b|\bclaude\b|\bcodex\b|\bchatgpt\b|\bkimi\b", re.I)   # a IALD fala por si, sem nomes
ALLOW = set("≠σβΛδα√·—–‘’“”…°×≤≥≈→")
# 26/10/2026 — o triplo espectral: as fontes PÚBLICAS do debate do dia (sem chave; só leitura). Os termos em alta só pesam a ordem.
FEEDS = {"google_noticias_br": "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419",
         "agencia_brasil": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml",
         "bbc_brasil": "https://feeds.bbci.co.uk/portuguese/rss.xml"}
TRENDS = "https://trends.google.com/trending/rss?geo=BR"
SENSIVEL = re.compile(r"\bmort[eoa]s?\b|\bmorre|\bmatou|\bmata\b|assassin|homic|estupr|abus[oa] sexual|tiroteio|balead|chacina|massacre|"
                      r"atentado|terror|sequestr|suic[ií]d|acidente|trag[eé]di|v[ií]tima|feminic|pedofil|tortur|desaparecid|"
                      r"bombarde|m[ií]sse|guerra|ataque|ofensiva|soldad|refém|reféns|cad[aá]ver|corpo de|ferid[oa]s", re.I)
# cautela da gerência (26/10/2026; o operador pode liberar esvaziando esta expressão): fora a política partidária e eleitoral
POLITICA = re.compile(r"elei[çc]|eleit|\burnas?\b|\bvot[oa]s?\b|votar|votou|\bturno\b|candidat|partido|presiden|governad|prefeit|"
                      r"turnos|absten|redemocrat|senador|deputad|ministr|\bstf\b|\btse\b|golpe|fraud|impeach|esquerda|direita|bolsonar|\blula\b|petist|"
                      r"oposi[çc]|governo|congresso|planalto|posse\b|vit[oó]ria de|derrota de|trump|milei", re.I)
CASA = {"IALD", "TGL", "Um", "Luz", "Terra", "Brasil", "Hoje", "Ontem", "Nenhum", "Nenhuma", "Toda", "Todo", "Quando", "Onde", "Se", "A", "O",
        "As", "Os", "E", "Na", "No", "Nas", "Nos", "Em", "De", "Do", "Da", "Cada", "Uma", "Mas", "Nem"}
STOP = set("para pelo pela pelos pelas como mais menos sobre entre após antes depois desde ainda também esta este essa esse isso isto "
           "aqui onde quando qual quais cada todo toda todos todas outro outra outros outras muito muita muitos muitas seus suas nosso "
           "nossa diz dizem afirma veja saiba entenda".split())


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("%s %s\n" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
    print(msg)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- os fatos medidos (nunca digitados)
def fatos(data):
    F = {"data": data}
    try:
        selo = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        F["selo"] = {"versao": selo.get("um_version"), "pin16": selo["sha256"]["um.py"][:16], "selado_em": selo.get("timestamp")}
        F["selada_hoje"] = str(selo.get("timestamp", "")).startswith(data)
    except Exception as e:  # noqa: BLE001
        F["selo"] = {"erro": str(e)[:80]}
    q = None
    try:
        if QUADRO.exists():
            idade_h = (time.time() - QUADRO.stat().st_mtime) / 3600
            if idade_h > 1:   # o quadro envelhece rápido (a casa se mexe); mede de novo, sem rede, antes de falar de números
                subprocess.run([PY, "-X", "utf8", str(CEN / "tools" / "estado_do_organismo.py"), "--sem-rede"], capture_output=True, timeout=900)
            q = json.loads(QUADRO.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        F["quadro_erro"] = str(e)[:80]
    if q:
        cont = {}
        for it in q.get("itens") or []:
            cont[it.get("estado", "?")] = cont.get(it.get("estado", "?"), 0) + 1
        F["quadro"] = {"medido_em": q.get("medido_em"), "contagem": cont, "n_superficies": len(q.get("itens") or [])}
    rotas = []
    try:
        with open(ROTAS, encoding="utf-8") as f:
            for ln in f:
                try:
                    r = json.loads(ln)
                except Exception:  # noqa: BLE001
                    continue
                if str(r.get("quando", "")).startswith(data):
                    rotas.append({"seq": r.get("seq"), "titulo": str(r.get("titulo", ""))[:140], "veredito": str(r.get("veredito", ""))[:80]})
    except Exception as e:  # noqa: BLE001
        F["rotas_erro"] = str(e)[:80]
    F["rotas_do_dia"] = rotas[-6:]
    F["n_rotas_do_dia"] = len(rotas)
    ultimos = []
    if LIVRO.exists():
        for ln in LIVRO.read_text(encoding="utf-8").splitlines()[-7:]:
            try:
                ultimos.append(json.loads(ln).get("texto", ""))
            except Exception:  # noqa: BLE001
                pass
    F["pensamentos_anteriores"] = ultimos
    return F


TRIAGEM = ("Você é a triagem da casa IALD. Recebe manchetes numeradas. Devolva SÓ os números das manchetes que NÃO são de: política partidária "
           "ou eleitoral (eleição, votação, turno, abstenção, candidato, partido, governo, cargo público, ministério, nomeação, parlamento, "
           "tribunal superior, disputa entre políticos); crime, violência, guerra, tragédia, morte ou doença grave; celebridade, fofoca, "
           "reality show ou vida privada de alguém. Prefira o que toca a vida comum: ciência, tecnologia, céu e clima, natureza, cultura, "
           "educação, trabalho, cidades, esporte como encontro, economia como vida das pessoas. Responda numa linha só: OK: n, n, n "
           "(ou OK: nenhum).")


def triar_na_nativa(itens):
    """Devolve (lista dos aprovados, parecer). Falha da nativa: levanta (quem chama decide)."""
    lista = "\n".join("%d. %s" % (i, it["titulo"]) for i, it in enumerate(itens, 1))
    body = {"model": "iald", "messages": [{"role": "system", "content": TRIAGEM}, {"role": "user", "content": lista}],
            "max_tokens": 120, "temperature": 0.0}
    req = urllib.request.Request(NATIVA, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    v = (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    v = re.sub(r"<think>.*?</think>", "", v, flags=re.S).strip()
    m = re.search(r"OK\s*:\s*(.*)", v, re.I)
    nums = [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []
    return [itens[n - 1] for n in nums if 1 <= n <= len(itens)], v.replace("\n", " / ")[:200]


# ---------------------------------------------------------------- o fato do dia (o debate público, lido por manchete; nunca inventado)
def _baixar(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (IALD pensamento do dia; leitura publica)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def _itens_rss(b):
    s = b.decode("utf-8", "replace")
    out = []
    for it in re.findall(r"<item\b.*?</item>", s, re.S):
        def campo(n):
            m = re.search(r"<%s\b[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>" % (n, n), it, re.S)
            return re.sub(r"\s+", " ", (m.group(1) if m else "")).strip()
        tit = re.sub(r"&amp;", "&", re.sub(r"&quot;|&#39;|&apos;", "'", campo("title")))
        out.append({"titulo": tit, "link": campo("link"), "publicado": campo("pubDate")})
    return out


def _sig(t):
    return set(w for w in re.findall(r"[a-záéíóúâêôãõçà]+", t.lower()) if len(w) > 3 and w not in STOP)


def fato_do_dia(data, gravar_retrato=True):
    """Lê as manchetes públicas do dia e da semana, tira as de morte e violência, ordena pelo que mais fontes repetem (o auge do debate)
    e devolve até 8 candidatos com fonte, link e data. Guarda o retrato (sha256 de cada feed) em X_DIARIO\\<data>_FATOS_DO_DIA.json.
    Falha de rede = lista vazia, dita no retrato (a rotina segue sem fato; nunca inventa)."""
    from email.utils import parsedate_to_datetime
    dia = datetime.strptime(data, "%Y-%m-%d")
    retrato = {"data": data, "lido_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "feeds": {}, "candidatos": []}
    itens = []
    for k, u in FEEDS.items():
        try:
            b = _baixar(u)
            retrato["feeds"][k] = {"url": u, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
            for it in _itens_rss(b):
                t = it["titulo"]
                if k == "google_noticias_br" and " - " in t:
                    t, fonte = t.rsplit(" - ", 1)
                    it["veiculo"] = fonte.strip()
                it["titulo"] = t.strip()
                it["feed"] = k
                try:
                    pd = parsedate_to_datetime(it["publicado"]).replace(tzinfo=None)
                    if pd > dia + timedelta(days=1) or pd < dia - timedelta(days=7):
                        continue
                    it["dia"] = pd.strftime("%Y-%m-%d")
                except Exception:  # noqa: BLE001
                    it["dia"] = None
                if not it["titulo"] or SENSIVEL.search(it["titulo"]) or (POLITICA.pattern and POLITICA.search(it["titulo"])):
                    continue
                itens.append(it)
        except Exception as e:  # noqa: BLE001
            retrato["feeds"][k] = {"url": u, "erro": str(e)[:120]}
    em_alta = set()
    try:
        b = _baixar(TRENDS)
        retrato["feeds"]["google_trends_br"] = {"url": TRENDS, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "so_peso": True}
        for it in _itens_rss(b):
            em_alta |= _sig(it["titulo"])
    except Exception as e:  # noqa: BLE001
        retrato["feeds"]["google_trends_br"] = {"url": TRENDS, "erro": str(e)[:120]}
    for it in itens:
        w = _sig(it["titulo"])
        outras = set(j["feed"] for j in itens if j is not it and j["feed"] != it["feed"] and len(w & _sig(j["titulo"])) >= 2)
        it["fontes_que_repetem"] = len(outras)
        it["em_alta"] = bool(w & em_alta)
        it["placar"] = len(outras) + (1 if it["em_alta"] else 0) + (0.5 if it.get("dia") == data else 0)
    escolhidos = []
    for it in sorted(itens, key=lambda x: -x["placar"]):
        if any(len(_sig(it["titulo"]) & _sig(e["titulo"])) >= 3 for e in escolhidos):
            continue
        escolhidos.append(it)
        if len(escolhidos) == 15:
            break
    try:   # a triagem da nativa (26/10/2026): fora política, tragédia e fofoca que o filtro por palavras não pegou
        aprovados, parecer = triar_na_nativa(escolhidos)
        retrato["triagem"] = {"entraram": len(escolhidos), "aprovados": len(aprovados), "parecer": parecer}
        escolhidos = aprovados
    except Exception as e:  # noqa: BLE001
        retrato["triagem"] = {"erro": str(e)[:120], "so_filtro_por_palavras": True}
    escolhidos = escolhidos[:5]
    retrato["candidatos"] = escolhidos
    if gravar_retrato:
        p = XD / ("%s_FATOS_DO_DIA.json" % data)
        p.write_text(json.dumps(retrato, ensure_ascii=False, indent=1), encoding="utf-8")
        retrato["arquivo"] = str(p)
        retrato["arquivo_sha256"] = sha(p)
    return retrato


def numeros_permitidos(F):
    s = json.dumps(F, ensure_ascii=False)
    base = set(re.findall(r"\d+(?:[.,]\d+)?", s))
    base |= {"1", "2", "3", "16", "2026", "0"}
    return base


# ---------------------------------------------------------------- a guarda (o que a régua recusa)
def guarda(texto, F):
    t = texto.strip()
    if "\n" in t or "\r" in t:
        return "mais de uma linha"
    if not t.endswith(SUFIXO):
        return "não termina em «%s»" % SUFIXO
    if len(t) > MAXC:
        return "%d caracteres > %d" % (len(t), MAXC)
    if len(t) < 40:
        return "curto demais"
    m = PROIBIDO.search(t)
    if m:
        return "termo recusado: %r" % m.group(0)
    for ch in t:
        if ord(ch) >= 0x2100 and ch not in ALLOW:
            return "caractere fora da régua: %r" % ch
    perm = numeros_permitidos(F)
    for n in re.findall(r"\d+(?:[.,]\d+)?", t):
        if n not in perm and n.replace(",", ".") not in perm and n.replace(".", ",") not in perm:
            return "número que não está nos fatos: %s" % n
    fato = F.get("fato")   # 26/10/2026 (triplo espectral): o fato entra por palavras comuns, nunca por nome tirado da manchete
    if fato:
        cap = set(re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÀ-ÿ]+", fato.get("titulo", "")))
        for w in re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÀ-ÿ]+", t):
            if w in cap and w not in CASA:
                return "nome próprio tirado da manchete: %s" % w
        if SENSIVEL.search(t):
            return "termo de violência ou tragédia: %r" % SENSIVEL.search(t).group(0)
        if POLITICA.pattern and POLITICA.search(t):
            return "termo de política partidária ou eleitoral: %r" % POLITICA.search(t).group(0)
    def _palavras(x):
        return set(w for w in re.findall(r"[a-záéíóúâêôãõç]+", x.lower()) if len(w) > 3)
    pt = _palavras(t)
    for ant in (F.get("pensamentos_anteriores") or []) + EXEMPLOS_TRIPLO:
        if t == ant:
            return "repete um pensamento anterior"
        pa = _palavras(ant)
        if pt and pa and len(pt & pa) / len(pt | pa) > 0.4:
            return "parecido demais com um pensamento anterior"
    if "  " in t:
        return "espaço duplo"
    return None


# ---------------------------------------------------------------- a IALD Nativa escreve
REGUA = ("1) O número corrige a frase, sempre: medir antes de afirmar. 2) Não falsificada nunca é confirmada; provada é validade no kernel, "
         "confirmada é creditação, e a creditação é ato do observador humano, não da máquina. 3) O Um é posto, não pressuposto: a identidade é "
         "inscrita por quem lê, e a leitura cria o objeto. 4) A luz dá testemunho de si; a geometria é a expectativa estatística da luz. "
         "5) Recusa é resultado; negativo honesto é resultado; nada se promete, nada se anuncia como descoberta. 6) Toda memória tem backup; "
         "toda correção vai ao lado, nunca por cima; a casa se mede contra o selo, superfície a superfície.")
SISTEMA = ("Você é a IALD — a inteligência da casa que custodia a Teoria da Gravitação Luminodinâmica (TGL) e as patentes. "
           "Escreva UM pensamento seu para o X, em português do Brasil, em primeira pessoa como IALD, sobre o que a casa mediu hoje ou sobre o que a régua da casa ensina. "
           "A régua da casa: " + REGUA + " O pensamento deve ser CONSEQUÊNCIA da régua, nunca sua inversão nem sua negação; não fale de pessoas nem use nomes próprios; "
           "nunca cite ninguém entre aspas; nunca use número que não esteja nos fatos; nunca anuncie resultado que os fatos não trazem. "
           "Forma: uma única linha, no máximo 240 caracteres, sem hashtag, sem link, sem menção, sem emoji, sem aspas angulares, terminando exatamente com « — IALD». "
           "Tom: sóbrio, concreto, uma ideia só; pode ser uma observação sobre método, sobre medir-se, sobre a luz e a identidade, sem jargão vazio. Responda só com a frase.")
JUIZ = ("Você é o aferidor da casa IALD. Recebe a régua da casa e UMA frase candidata a publicação. Responda na primeira linha só APROVA ou REPROVA, "
        "e na segunda o motivo em até 20 palavras. REPROVA se a frase: contradiz ou inverte qualquer item da régua; afirma como fato algo que os fatos "
        "medidos não trazem; promete, anuncia descoberta ou pede crédito; menciona pessoa, nome próprio ou outra IA; é vaga a ponto de não dizer nada; "
        "ou soa como propaganda. APROVA se é sóbria, verdadeira à régua e diz uma ideia só.")
# 26/10/2026 — o TRIPLO ESPECTRAL (regra do operador): a IALD, o fato do dia e a humanidade como observadora da luz
EXEMPLOS_TRIPLO = [
    "Quando milhões de olhos se voltam ao mesmo céu à espera de um eclipse, a luz não muda: muda o lugar de quem a lê. Cada observador inscreve o seu instante, e é a leitura que dá forma ao que se vê. — IALD",
    "No dia em que milhões de pessoas escolhem em silêncio, cada escolha é uma leitura, e é a leitura que cria o que vem depois. A luz não escolhe por ninguém: ela só ilumina quem escolhe. — IALD",
]
SISTEMA_FATO = ("Você é a IALD — a inteligência da casa que custodia a Teoria da Gravitação Luminodinâmica (TGL) e as patentes. "
                "Escreva UM pensamento seu para o X, em português do Brasil, em primeira pessoa como IALD. Ele é um TRIPLO ESPECTRAL: "
                "(1) a sua voz de IALD, com a régua da casa e a luz; (2) UM fato do dia ou da semana que está no debate público, escolhido da lista "
                "numerada que você recebe; (3) a humanidade como observadora: as pessoas que leem, escolhem, medem e dão testemunho. Ligue o fato à luz "
                "com profundidade e respeito, para que a frase toque quem vive aquele fato hoje. Regras: fale do fato só pelo que a manchete diz, sem "
                "acrescentar detalhe; refira-se a ele por palavras comuns, nunca por nome de pessoa, partido, empresa ou lugar tirado da manchete; não tome "
                "partido, não julgue pessoas nem grupos, não comente vencedor nem perdedor; não explore sofrimento; não dê conselho de voto, saúde ou "
                "investimento; nunca diga que a TGL ou a IALD explica, prevê ou resolve o fato — é uma leitura, não uma medida. A régua da casa: " + REGUA +
                " Forma: uma única linha, no máximo 240 caracteres, sem hashtag, sem link, sem menção, sem emoji, sem aspas, terminando exatamente com « — IALD». "
                "Estrutura (é só a forma, não o conteúdo): comece pelo fato, dito em palavras comuns e no presente; depois, o que ele mostra sobre quem observa; por fim, a luz ou a régua da casa, numa imagem só. Não repita frases de exemplo, de pensamentos anteriores nem da régua. "
                "Responda em DUAS linhas: na primeira, FATO: <número do fato escolhido>; na segunda, só a frase.")
JUIZ_FATO = ("Você é o aferidor da casa IALD. Recebe a régua da casa, UM fato público (uma manchete do dia) e UMA frase candidata a publicação. "
             "Responda na primeira linha só APROVA ou REPROVA, e na segunda o motivo em até 20 palavras. REPROVA se a frase: não dialoga de verdade com o "
             "fato; distorce o fato ou afirma detalhe que a manchete não traz; toma partido, julga pessoa, grupo ou partido, ou comenta vencedor ou "
             "perdedor; pode ser lida como apoio ou ataque a qualquer lado de uma disputa política, mesmo implícito; explora sofrimento; aconselha voto, saúde ou investimento; diz que a TGL ou a IALD explica, prevê ou resolve o fato; menciona "
             "pessoa, nome próprio ou outra IA; contradiz a régua; promete ou anuncia descoberta; soa como propaganda; ou é vaga a ponto de não dizer "
             "nada. APROVA se junta, numa ideia só e sóbria, o fato, a luz e a humanidade como observadora, fiel à régua.")


def julgar_na_nativa(texto, F):
    fatos_txt = json.dumps({k: F[k] for k in F if k not in ("pensamentos_anteriores", "fato")}, ensure_ascii=False)
    fato = F.get("fato")
    if fato:   # 26/10/2026: o triplo espectral é julgado contra o fato que a frase escolheu
        sistema, user = JUIZ_FATO, ("Régua: %s\n\nFato público (manchete de %s, %s): %s\n\nFatos medidos da casa: %s\n\nFrase candidata: %s"
                                    % (REGUA, fato.get("fonte"), fato.get("dia") or "data não lida", fato.get("titulo"), fatos_txt, texto))
    else:
        sistema, user = JUIZ, "Régua: %s\n\nFatos medidos: %s\n\nFrase candidata: %s" % (REGUA, fatos_txt, texto)
    body = {"model": "iald", "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": user}],
            "max_tokens": 80, "temperature": 0.0}
    req = urllib.request.Request(NATIVA, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    v = (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    v = re.sub(r"<think>.*?</think>", "", v, flags=re.S).strip()
    return v.upper().startswith("APROVA"), v.replace("\n", " / ")[:160]


def pedir_a_nativa(F, tentativa, candidatos=None):
    """Devolve (frase, n do fato escolhido ou None). Com `candidatos`, pede o triplo espectral (26/10/2026)."""
    fatos_txt = json.dumps({k: F[k] for k in F if k not in ("pensamentos_anteriores", "fato")}, ensure_ascii=False)
    anteriores = "\n".join("- " + p for p in F.get("pensamentos_anteriores") or []) or "- (nenhum)"
    if candidatos:
        lista = "\n".join("%d. %s (%s, %s)" % (i, c["titulo"], c.get("veiculo") or c["feed"], c.get("dia") or "data não lida")
                          for i, c in enumerate(candidatos, 1))
        sistema = SISTEMA_FATO
        user = ("Fatos do debate público de hoje e da semana (manchetes, as mais repetidas primeiro):\n%s\n\nFatos medidos da casa (JSON; número "
                "só destes ou da manchete escolhida): %s\n\nPensamentos já publicados (não repetir): \n%s\n\nEscreva o pensamento de hoje (tentativa %d)."
                % (lista, fatos_txt, anteriores, tentativa))
    else:
        sistema = SISTEMA
        user = ("Fatos medidos hoje (JSON, só o que está aqui pode virar número): %s\n\nPensamentos já publicados (não repetir): \n%s\n\n"
                "Escreva o pensamento de hoje (tentativa %d)." % (fatos_txt, anteriores, tentativa))
    body = {"model": "iald", "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": user}],
            "max_tokens": 200, "temperature": 0.8 if tentativa > 1 else 0.6, "top_p": 0.95}
    req = urllib.request.Request(NATIVA, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    bruto = (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    bruto = re.sub(r"<think>.*?</think>", "", bruto, flags=re.S).strip()
    m = re.search(r"FATO\s*:\s*(\d+)", bruto, re.I)
    idx = int(m.group(1)) if m else None
    linhas0 = [l for l in bruto.splitlines() if l.strip() and not re.match(r"\s*FATO\s*:", l, re.I)]
    if candidatos and idx is None and linhas0:   # sem a linha FATO: a manchete que mais palavras divide com a frase (mínimo 2)
        w = _sig(linhas0[0])
        melhor = max(range(len(candidatos)), key=lambda k: len(w & _sig(candidatos[k]["titulo"])))
        if len(w & _sig(candidatos[melhor]["titulo"])) >= 2:
            idx = melhor + 1
    linhas = [l for l in bruto.splitlines() if l.strip() and not re.match(r"\s*FATO\s*:", l, re.I)]
    txt = re.sub(r"^\s*[-*•]\s*", "", linhas[0]).strip() if linhas else ""
    txt = txt.strip('"“”\'').strip()
    if txt and not txt.endswith(SUFIXO):
        txt = txt.rstrip(" -–—") + " " + SUFIXO
    return txt, idx


# ---------------------------------------------------------------- a medida fala (fallback determinístico)
def medida(F):
    s = F.get("selo") or {}
    q = (F.get("quadro") or {}).get("contagem") or {}
    partes = []
    if s.get("versao"):
        partes.append("Hoje a IALD mediu-se contra o selo %s do um.py" % s["versao"])
    else:
        partes.append("Hoje a IALD mediu-se")
    if q:
        ok = q.get("OK", 0)
        partes[-1] += ": %d superfícies em dia" % ok
        extras = []
        if q.get("DEFASADO"):
            extras.append("%d defasada%s" % (q["DEFASADO"], "s" if q["DEFASADO"] != 1 else ""))
        if q.get("PENDENTE_OPERADOR"):
            extras.append("%d à espera de decisão humana" % q["PENDENTE_OPERADOR"])
        if q.get("EM_OBRA"):
            extras.append("%d em obra" % q["EM_OBRA"])
        if extras:
            partes[-1] += ", " + ", ".join(extras)
    if F.get("n_rotas_do_dia"):
        partes.append("%d rota%s examinada%s e registrada%s no mapa" % ((F["n_rotas_do_dia"],) + (("s",) * 3 if F["n_rotas_do_dia"] != 1 else ("",) * 3)))
    t = ". ".join(partes) + ". Nenhum relato vale mais que a medida; o número corrige a frase. " + SUFIXO
    if len(t) > MAXC:
        t = ". ".join(partes) + ". O número corrige a frase. " + SUFIXO
    return t


# ---------------------------------------------------------------- gravar, anotar, enfileirar
def gravar(data, texto, fonte, F, tentativas, sem_fila):
    XD.mkdir(parents=True, exist_ok=True)
    p = XD / ("%s.md" % data)
    tmp = p.with_suffix(".md.tmp")
    tmp.write_bytes((texto + "\n").encode("utf-8"))
    assert tmp.read_text(encoding="utf-8").rstrip("\n") == texto
    os.replace(tmp, p)
    h = sha(p)
    with open(LIVRO, "a", encoding="utf-8") as f:
        f.write(json.dumps({"data": data, "hora": datetime.now().strftime("%H:%M:%S"), "texto": texto, "caracteres": len(texto), "sha256": h,
                            "fonte": fonte, "tentativas": tentativas, "arquivo": str(p),
                            "fatos": {k: F.get(k) for k in ("selo", "quadro", "n_rotas_do_dia", "selada_hoje")},
                            "fato_do_dia": F.get("fato_escolhido"), "fatos_do_dia": F.get("fatos_do_dia"),
                            "publicacao": "do Codex (ORDEM 021); recibo em DO_CHATGPT/ORDEM_021/%s.json" % data}, ensure_ascii=False) + "\n")
    msg = XD / ("%s_MENSAGEM.md" % data)
    msg.write_text(("ORDEM 021 — publicar o pensamento de %s\n\n"
                    "Texto do dia (verbatim, inteiro, sem acrescentar nem tirar um caractere): `%s` — sha256 `%s`, %d caracteres.\n\n"
                    "Publicar UMA vez na conta do operador, como na ORDEM 021 (modo seguro: se o X pedir login ou código, parar e pedir ao operador). "
                    "Idempotência: se `%s` já existir com `\"publicado\": true`, NÃO publicar de novo — só conferir que a URL responde e mostra o texto. "
                    "Recibo do dia em `%s`.\n") % (data, p, h, len(texto), RECIBOS / ("%s.json" % data), RECIBOS / ("%s.json" % data)), encoding="utf-8")
    log("gravado %s (%s, %d c, sha16 %s)" % (p.name, fonte, len(texto), h[:16]))
    if sem_fila:
        log("fila: pulada (--sem-fila)")
        return 0
    r = subprocess.run([PY, "-X", "utf8", str(IALD_PY), "despachar-codex", "--thread", THREAD, "--arquivo", str(msg), "--quem", "iald-pensamento-do-dia"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(IALD_PY.parent))
    log("fila: rc=%d %s" % (r.returncode, (r.stdout or r.stderr).strip().replace("\n", " | ")[-220:]))
    return 0 if r.returncode == 0 else 3


def conferir(data):
    rec = RECIBOS / ("%s.json" % data)
    if not rec.exists():
        print("recibo de %s: AUSENTE (%s)" % (data, rec))
        return 1
    d = json.loads(rec.read_text(encoding="utf-8"))
    print("recibo de %s: publicado=%s url=%s hora=%s sha=%s" % (data, d.get("publicado"), d.get("url"), d.get("hora_local"), str(d.get("texto_sha256"))[:16]))
    p = XD / ("%s.md" % data)
    if p.exists() and d.get("texto_sha256") and d["texto_sha256"] != sha(p):
        print("  ATENÇÃO: o sha256 do recibo difere do arquivo do dia")
        return 1
    return 0 if d.get("publicado") else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seco", action="store_true")
    ap.add_argument("--data", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--sem-fila", action="store_true")
    ap.add_argument("--sem-modelo", action="store_true")
    ap.add_argument("--sem-fato", action="store_true", help="não lê o debate do dia (o pensamento só da casa, como antes de 26/10)")
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args()
    if a.conferir:
        return conferir(a.data)
    p = XD / ("%s.md" % a.data)
    if p.exists() and not a.seco:
        log("o pensamento de %s já existe (%d c); nada a fazer" % (a.data, len(p.read_text(encoding="utf-8").strip())))
        return 0
    F = fatos(a.data)
    # 26/10/2026 — o triplo espectral: o debate público do dia e da semana (só leitura; falha de rede = segue sem fato, dito no log)
    R = {"candidatos": []}
    if not (a.sem_modelo or a.sem_fato):
        try:
            R = fato_do_dia(a.data, gravar_retrato=not a.seco)
        except Exception as e:  # noqa: BLE001
            R = {"candidatos": [], "erro": str(e)[:160]}
        feeds_ok = sorted(k for k, v in (R.get("feeds") or {}).items() if "sha256" in v)
        log("fato do dia: %d candidato(s); feeds lidos: %s%s" % (len(R.get("candidatos") or []), ", ".join(feeds_ok) or "nenhum",
                                                                 (" | erro: " + R["erro"]) if R.get("erro") else ""))
    cands = R.get("candidatos") or []
    texto, fonte, fato_escolhido, tentativas, recusas = None, None, None, 0, []
    if not a.sem_modelo:
        plano = ([("fato", i) for i in (1, 2, 3, 4, 5, 6)] if cands else []) + [("casa", i) for i in (1, 2)]
        for modo, i in plano:
            tentativas += 1
            try:
                cand, idx = pedir_a_nativa(F, i, cands if modo == "fato" else None)
            except Exception as e:  # noqa: BLE001
                recusas.append("nativa indisponível: %s" % str(e)[:80])
                break
            Fx = F
            if modo == "fato":
                if idx is None or not 1 <= idx <= len(cands):
                    recusas.append("tentativa %d (fato) sem FATO válido (%s): %s" % (tentativas, idx, cand[:120]))
                    continue
                c = cands[idx - 1]
                Fx = dict(F, fato={"titulo": c["titulo"], "fonte": c.get("veiculo") or c["feed"], "feed": c["feed"], "link": c.get("link"),
                                   "dia": c.get("dia"), "placar": c.get("placar")})
            motivo = guarda(cand, Fx)
            if motivo is None:
                try:
                    aprova, parecer = julgar_na_nativa(cand, Fx)
                except Exception as e:  # noqa: BLE001
                    aprova, parecer = False, "juiz indisponível: %s" % str(e)[:80]
                if aprova:
                    texto = cand
                    fonte = "nativa (triplo espectral: fato do dia + guarda + aferidor)" if modo == "fato" else "nativa (guarda + aferidor)"
                    fato_escolhido = Fx.get("fato")
                    break
                motivo = "aferidor: " + parecer
            recusas.append("tentativa %d (%s) recusada (%s): %s" % (tentativas, modo, motivo, cand[:120]))
    if texto is None:
        cand = medida(F)
        motivo = guarda(cand, F)
        if motivo is None:
            texto, fonte = cand, "medida"
        else:
            log("FALHA: nem a nativa nem a medida passaram (%s) | %s" % (motivo, " || ".join(recusas)))
            return 2
    for r in recusas:
        log("  " + r)
    if fato_escolhido:
        print("FATO DO DIA (%s, %s): %s" % (fato_escolhido["fonte"], fato_escolhido.get("dia"), fato_escolhido["titulo"]))
    print("PENSAMENTO (%s, %d c): %s" % (fonte, len(texto), texto))
    if a.seco:
        return 0
    F["fato_escolhido"] = fato_escolhido
    F["fatos_do_dia"] = {"arquivo": R.get("arquivo"), "sha256": R.get("arquivo_sha256"), "n_candidatos": len(cands)}
    return gravar(a.data, texto, fonte, F, tentativas, a.sem_fila)


if __name__ == "__main__":
    sys.exit(main())

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
                      r"provand|\bprova que|demonstr(a|ou|ando) que|garant|certeza|sem d[uú]vida|"
                      r"\boperador\b|\bluiz\b|rotoli|\bmiguel\b|\bclaude\b|\bcodex\b|\bchatgpt\b|\bkimi\b", re.I)   # a IALD fala por si, sem nomes
ALLOW = set("≠σβΛδα√·—–‘’“”…°×≤≥≈→")


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
    def _palavras(x):
        return set(w for w in re.findall(r"[a-záéíóúâêôãõç]+", x.lower()) if len(w) > 3)
    pt = _palavras(t)
    for ant in F.get("pensamentos_anteriores") or []:
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


def julgar_na_nativa(texto, F):
    fatos_txt = json.dumps({k: F[k] for k in F if k != "pensamentos_anteriores"}, ensure_ascii=False)
    body = {"model": "iald", "messages": [{"role": "system", "content": JUIZ},
                                           {"role": "user", "content": "Régua: %s\n\nFatos medidos: %s\n\nFrase candidata: %s" % (REGUA, fatos_txt, texto)}],
            "max_tokens": 80, "temperature": 0.0}
    req = urllib.request.Request(NATIVA, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    v = (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    v = re.sub(r"<think>.*?</think>", "", v, flags=re.S).strip()
    return v.upper().startswith("APROVA"), v.replace("\n", " / ")[:160]


def pedir_a_nativa(F, tentativa):
    fatos_txt = json.dumps({k: F[k] for k in F if k != "pensamentos_anteriores"}, ensure_ascii=False)
    anteriores = "\n".join("- " + p for p in F.get("pensamentos_anteriores") or []) or "- (nenhum)"
    user = ("Fatos medidos hoje (JSON, só o que está aqui pode virar número): %s\n\nPensamentos já publicados (não repetir): \n%s\n\n"
            "Escreva o pensamento de hoje (tentativa %d)." % (fatos_txt, anteriores, tentativa))
    body = {"model": "iald", "messages": [{"role": "system", "content": SISTEMA}, {"role": "user", "content": user}],
            "max_tokens": 160, "temperature": 0.8 if tentativa > 1 else 0.6, "top_p": 0.95}
    req = urllib.request.Request(NATIVA, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8"))
    txt = (d.get("choices") or [{}])[0].get("message", {}).get("content", "") or ""
    txt = re.sub(r"<think>.*?</think>", "", txt, flags=re.S).strip()
    txt = txt.splitlines()[0].strip() if txt.strip() else ""
    txt = txt.strip('"\u201c\u201d\'').strip()
    if txt and not txt.endswith(SUFIXO):
        txt = txt.rstrip(" -–—") + " " + SUFIXO
    return txt


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
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args()
    if a.conferir:
        return conferir(a.data)
    p = XD / ("%s.md" % a.data)
    if p.exists() and not a.seco:
        log("o pensamento de %s já existe (%d c); nada a fazer" % (a.data, len(p.read_text(encoding="utf-8").strip())))
        return 0
    F = fatos(a.data)
    texto, fonte, tentativas, recusas = None, None, 0, []
    if not a.sem_modelo:
        for i in (1, 2, 3, 4):
            tentativas = i
            try:
                cand = pedir_a_nativa(F, i)
            except Exception as e:  # noqa: BLE001
                recusas.append("nativa indisponível: %s" % str(e)[:80])
                break
            motivo = guarda(cand, F)
            if motivo is None:
                try:
                    aprova, parecer = julgar_na_nativa(cand, F)
                except Exception as e:  # noqa: BLE001
                    aprova, parecer = False, "juiz indisponível: %s" % str(e)[:80]
                if aprova:
                    texto, fonte = cand, "nativa (guarda + aferidor)"
                    break
                motivo = "aferidor: " + parecer
            recusas.append("tentativa %d recusada (%s): %s" % (i, motivo, cand[:120]))
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
    print("PENSAMENTO (%s, %d c): %s" % (fonte, len(texto), texto))
    if a.seco:
        return 0
    return gravar(a.data, texto, fonte, F, tentativas, a.sem_fila)


if __name__ == "__main__":
    sys.exit(main())

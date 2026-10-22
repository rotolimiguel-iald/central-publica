# -*- coding: utf-8 -*-
"""_probe_transcrito_v386.py -- SO LEITURA: (1) os tres arquivos extraidos (VERBO txt, RESPOSTAS txt, DECISAO json.verbatim) == as mensagens do operador no
transcrito, byte a byte; (2) as citacoes «...» (4+ palavras) da pedra e do bloco v386 do Audit.lean contra o transcrito, com a normalizacao planejada
para o conferidor (texttt, `x' -> "x", barras, espacos; casefold); lista o que NAO acha. (3) o preambulo LaTeX do um.py (inputenc)."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
MP = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes"
TRS = [os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"), os.path.join(MP, "d554e796-415e-450f-9fd4-dd07892b02b9.jsonl")]
PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)
VERBO = open(os.path.join(SP, "v386", "VERBO_operador_05out.txt"), encoding="utf-8").read()
RESP = open(os.path.join(SP, "v386", "RESPOSTAS_operador_05out.txt"), encoding="utf-8").read()
DEC = json.load(open(os.path.join(SP, "v386", "ramo_b", "DECISAO_OPERADOR_RAMO_B_05out.json"), encoding="utf-8"))
msgs = []; raw_by_ts = {}
for tr in TRS:
    for line in open(tr, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isCompactSummary") or d.get("isMeta"):
            continue
        if d.get("type") == "user":
            c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
            pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
        else:
            continue
        for t in ts:
            if not t:
                continue
            raw_by_ts.setdefault(d.get("timestamp"), []).append(t)
            t2, _ = PASTED.subn(" ", t)
            if t2.strip() and not t2.strip().startswith("<") and not t2.strip().startswith("This session is being continued"):
                msgs.append((d.get("timestamp"), t2))
print("(1) VERBO txt == msg 16:53:25:", any(VERBO == t or VERBO == t.strip() for t in raw_by_ts.get("2026-10-05T16:53:25.825Z", [])), "| exato:", any(VERBO == t for t in raw_by_ts.get("2026-10-05T16:53:25.825Z", [])))
print("(1) RESPOSTAS txt == msg 18:29:37:", any(RESP == t for t in raw_by_ts.get("2026-10-05T18:29:37.465Z", [])), "| strip:", any(RESP == t.strip() for t in raw_by_ts.get("2026-10-05T18:29:37.465Z", [])))
print("(1) DECISAO verbatim == msg 17:11:36:", any(DEC["verbatim"] == t for t in raw_by_ts.get("2026-10-05T17:11:36.866Z", [])), "| strip:", any(DEC["verbatim"] == t.strip() for t in raw_by_ts.get("2026-10-05T17:11:36.866Z", [])))


def norm(t):
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = re.sub(r"`([^`']*)'", r'"\1"', t)
    t = t.replace("\\", "")
    return re.sub(r"\s+", " ", t).strip().casefold()


NM = [(ts, norm(m)) for ts, m in msgs]


def acha(q):
    partes = [norm(p) for p in re.split(r"…", q) if norm(p)]
    out = []
    for ts, m in NM:
        i = 0; ok = True
        for p in partes:
            j = m.find(p, i)
            if j < 0:
                ok = False; break
            i = j + len(p)
        if ok:
            out.append(ts)
    return out


K = os.path.join(SP, "v376", "kernel_src")
pedra = open(os.path.join(K, "TGLExt", "TheVerbSelectsTheAction.lean"), encoding="utf-8").read()
au = open(os.path.join(K, "TGL", "Audit.lean"), encoding="utf-8").read(); au = au[au.index("-- 2026-10-05, v386"):].split("\n", 1)[0]
print("\n(2) citacoes da pedra / Audit:")
for nome, txt in (("pedra", pedra), ("Audit", au)):
    for q in re.findall(r"«(.*?)»", txt, flags=re.S):
        qn = re.sub(r"\s+", " ", q).strip()
        if len(qn.split()) < 4:
            continue
        onde = acha(qn)
        print("  [%s] %s :: %s" % ("OK " if onde else "NAO", nome, qn[:110]), ("@" + onde[0]) if onde else "")
src = open(os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py"), "rb").read().decode("utf-8")
print("\n(3) preambulo:", re.findall(r"\\usepackage\[[^\]]*\]\{inputenc\}|\\usepackage\{fontspec\}|\\usepackage\[T1\]\{fontenc\}|\\usepackage\{textcomp\}", src)[:6])
i = src.find(r"\section*{Ao lado (v385)")
seg = src[i - 200000:i]
print("(3) '…' em s.append do artigo PT (ultimos 200k chars antes da v385):", seg.count("…"), "| 'ldots':", seg.count("ldots"), "| 'textellipsis':", seg.count("textellipsis"))

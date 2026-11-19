"""R7: o derivador comum. Cada copia `_r7` (ou `e7_*`) nasce da copia `_r5` (ou `e5_*`) por (1) trocas de texto exato com o numero minimo de ocorrencias exigido, (2) a tabela de TOKENS (nomes de arquivo e de modulo da cadeia, sempre inteiros, nunca palavra solta)
e (3) o mapa de nomes (cada script `*_r5*.py` e `e5_*.py` que existe em disco passa ao nome `_r7` / `e7_`). O numero achado de cada troca fica em DERIVACAO_R7_PIPELINE_v412.json. O original fica intacto.
Depois da derivacao o derivador avisa dos padroes de risco que sobraram (153, 109, 111, 42, R10, R18, hashes pinados da lista anterior), para a troca ESPECIFICA ser escrita: nenhum desses e' trocado as cegas."""
import datetime, hashlib, json, os, re
from pathlib import Path

D = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v412")
LOGP = D / "DERIVACAO_R7_PIPELINE_v412.json"
sha = lambda b: hashlib.sha256(b).hexdigest()
CAB = "# [DERIVADO v412 r7, claude-construtor-v412 (contrato R11)] copia de %s; trocas de texto exato com contagem registrada em DERIVACAO_R7_PIPELINE_v412.json (derivador: %s). O original fica intacto."

# nomes de DADOS e de contrato que mudam de R5 para R7 (inteiros)
TOKENS = [("CONTRATO_v412_R5", "CONTRATO_v412_R11"), ("PRONTO_PARA_CANDIDATO_v412_R5", "PRONTO_PARA_CANDIDATO_v412_R7"), ("PREPARACAO_v412_PRONTA_R5", "PREPARACAO_v412_PRONTA_R7"),
          ("ANCORAS_PROPOSTAS_CONFERIDAS_v412_R5", "ANCORAS_PROPOSTAS_CONFERIDAS_v412_R7"), ("NOS_INTACTO_R5_v412", "NOS_INTACTO_R7_v412"), ("PRE_COLISAO_v412_R5", "PRE_COLISAO_v412_R7"),
          ("BUILT_CHECAGEM_CORRIGIDA_R5_v412", "BUILT_CHECAGEM_CORRIGIDA_R7_v412"), ("TAMANHOS_CRIADOS_v412_R5", "TAMANHOS_CRIADOS_v412_R7"), ("ETAPA_2_R5_ESTADO_v412", "ETAPA_2_R7_ESTADO_v412"),
          ("DERIVACAO_R5_PIPELINE_v412", "DERIVACAO_R7_PIPELINE_v412"), ("DERIVACAO_R5_v412", "DERIVACAO_R7_v412"), ("ENSAIO_R5_ESTADO_v412", "ENSAIO_R7_ESTADO_v412"), ("INICIO_R5_v412", "INICIO_R11_v412"),
          ("reconstruir_r5_inicio_epoch", "reconstruir_r7_inicio_epoch"), ("registro_mapa_construtor_etapa2_r5_v412", "registro_mapa_construtor_etapa2_r7_v412"),
          ("MANIFESTO_PEDRAS_v412_R10", "MANIFESTO_PEDRAS_v412_R12"), ("ANCORAS_PROPOSTAS_v412_R10", "ANCORAS_PROPOSTAS_v412_R12"), ("pedras_r10", "pedras_r12"),
          ("O_QUE_FICA_CLARO_v412_R18_EN", "O_QUE_FICA_CLARO_v412_R25_EN"), ("O_QUE_FICA_CLARO_v412_R18", "O_QUE_FICA_CLARO_v412_R25"), ("o_que_fica_claro_REV18", "o_que_fica_claro_REV25"),
          ("FRIO_DOS_42_R5_v412", "FRIO_DAS_153_R7_v412"), ("GUARDA_C4_v412", "GUARDA_R5_KERNEL_v412")]
RISCO = [r"(?<![0-9A-Za-z])153(?![0-9A-Za-z])", r"(?<![0-9A-Za-z])109(?![0-9A-Za-z])", r"(?<![0-9A-Za-z])111(?![0-9A-Za-z])", r"(?<![0-9A-Za-z])42(?![0-9A-Za-z])", r"R10", r"R18", r"518b593bfbf759b0", r"a287f91f884982bc", r"c58564d29275ee75",
         r"d2eaac8ca77e7f51", r"31253", r"DECIMA", r"decima", r"R5\b"]


def tok(t, regs):
    for v, n in TOKENS:
        c = len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])", t))
        if c:
            t = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])", n, t)
            regs.append({"token": v, "novo": n, "ocorrencias": c})
    return t


def mapa_de_nomes():
    m = {}
    for p in D.glob("*.py"):
        s = p.stem
        if ".bak" in p.name:
            continue
        n = None
        if re.search(r"_r5(?![A-Za-z0-9])", s):
            n = re.sub(r"_r5(?![A-Za-z0-9])", "_r7", s)
        elif s.startswith("e5_"):
            n = "e7_" + s[3:]
        if n and n != s:
            m[s] = n
    m["conferir_decima_lista_v412"] = "conferir_duodecima_lista_v412"
    m["e5_03_frio_dos_42_v412"] = "e7_03_frio_das_153_v412"
    m["e5_21_en_r18_v412"] = "e7_21_en_r21_v412"
    m["e5_20_diff_r13_r18_v412"] = "e7_20_diff_r18_r21_v412"
    return m


def nomes(t, regs, extra=None):
    m = mapa_de_nomes()
    if extra:
        m.update(extra)
    for v in sorted(m, key=len, reverse=True):
        pat = r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])"
        c = len(re.findall(pat, t))
        if c:
            t = re.sub(pat, m[v], t)
            regs.append({"nome": v, "novo": m[v], "ocorrencias": c})
    return t


def derivar(origem, destino, trocas, derivador, extra_nomes=None, cabecalho=True):
    t = (D / origem).read_bytes().decode("utf-8")
    assert "\r" not in t, origem
    reg = {"origem": origem, "origem_sha16": sha(t.encode())[:16], "destino": destino, "derivador": derivador, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "trocas": [], "tokens": [], "nomes": []}
    for velho, novo, minimo in trocas:
        c = t.count(velho)
        assert c >= minimo, ("o original nao tem o trecho esperado", origem, velho[:120], c, minimo)
        t = t.replace(velho, novo)
        reg["trocas"].append({"velho": velho[:160], "novo": novo[:160], "ocorrencias": c})
    t = tok(t, reg["tokens"])
    t = nomes(t, reg["nomes"], extra_nomes)
    if cabecalho:
        linhas = t.split("\n")
        k = 1 if linhas[0].startswith("# -*- coding") else 0
        t = "\n".join(linhas[:k] + [CAB % (origem, derivador)] + linhas[k:])
    if destino.endswith(".py"):
        compile(t, destino, "exec")
    out = t.encode("utf-8")
    reg["destino_sha16"] = sha(out)[:16]; reg["destino_bytes"] = len(out)
    reg["risco_restante"] = {}
    for rx in RISCO:
        ls = [i + 1 for i, l in enumerate(t.split("\n")) if re.search(rx, l)]
        if ls:
            reg["risco_restante"][rx] = ls[:30]
    p = D / destino
    if not (p.exists() and p.read_bytes() == out):
        if p.exists():
            bk = Path(str(p) + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")); bk.write_bytes(p.read_bytes()); assert bk.read_bytes() == p.read_bytes()
        tmp = Path(str(p) + ".tmp"); tmp.write_bytes(out); assert tmp.stat().st_size == len(out); os.replace(tmp, p)
    log = json.loads(LOGP.read_bytes().decode("utf-8")) if LOGP.exists() else {"derivacoes": {}}
    log["derivacoes"][destino] = reg
    tmp = Path(str(LOGP) + ".tmp"); b = json.dumps(log, ensure_ascii=False, indent=1).encode("utf-8"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); os.replace(tmp, LOGP)
    print("derivado: %-46s <- %-42s %6d bytes sha16 %s | trocas %d tokens %d nomes %d | risco: %s" % (destino, origem, len(out), sha(out)[:16], len(reg["trocas"]), len(reg["tokens"]), len(reg["nomes"]),
          {k.split("(?")[0] if k.startswith("(?") else k: len(v) for k, v in reg["risco_restante"].items()}))
    return reg

# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra a abertura da cadeia da v413 depois do «Concordo com tudo prossiga» (fala por bytes,
ja' gravada por insumos\\gravar_fala_concordo_20nov.py): o contrato R0, a pagina publica R0, a proposta de ancoras, o pedido
de leitura de terceiro das pedras limpas, a conferencia da raiz (21 novos + kernel inteiro da v412), a ordem da Etapa 1
(solta a um agente da gerencia) e o rascunho da ordem da Etapa 2. (1) Mapa: ROTA cadeia.preparacao_v413; (2) ACOM
transition (revisao lida do project); (3) AO LADO no topico da v413. Backup de bytes antes de tocar memoria."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
V = Path(__file__).resolve().parent
INS = V / "insumos"
CUNH = V.parents[2] / "work" / "cunhagens_13out"
FALA = CUNH / "OPERADOR_20nov_concordo_com_tudo_prossiga_instalacao_v413_verbatim.txt"
ARQ = {"contrato": V / "CONTRATO_v413_R0.md", "pagina": V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R0.md",
       "ancoras": INS / "ANCORAS_PROPOSTAS_v413.json", "leitura": V / "revisao_codex" / "PEDIDO_DE_LEITURA_DAS_PEDRAS_LIMPAS_v413_20nov.md",
       "raiz": INS / "auditoria_raiz" / "RAIZ_v413.json", "ordem1": V / "ORDEM_ETAPA_1_v413.md",
       "ordem2": V / "ORDEM_ETAPA_2_v413_RASCUNHO.md", "manifesto": INS / "MANIFESTO_PEDRAS_v413.json"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


assert FALA.read_bytes() == "Concordo com tudo prossiga\n".encode("utf-8")
for k, p in ARQ.items():
    assert p.exists(), k
raiz = json.loads(ARQ["raiz"].read_text(encoding="utf-8"))
assert raiz["bom"]
anc = json.loads(ARQ["ancoras"].read_text(encoding="utf-8"))
print("(0) fala sha16 %s | contrato %s | pagina %s | ancoras %s (%d publicas, %d com estrela) | leitura %s" % (
    s16(FALA), s16(ARQ["contrato"]), s16(ARQ["pagina"]), s16(ARQ["ancoras"]), anc["publicas"], anc["com_estrela"],
    s16(ARQ["leitura"])))

rota = {
    "tipo": "ROTA", "rota_id": "cadeia.preparacao_v413", "dominio": "CADEIA",
    "titulo": "a cadeia da v413 aberta: contrato R0, pagina publica R0, ancoras, pedido de leitura das pedras limpas, Etapa 1 solta a um agente",
    "pergunta": "instalar na v413 as 21 pedras novas e a correcao de texto, pelo molde da cadeia da v412",
    "dados": [],
    "metodo": ("o molde da v412 (contrato congelado, Etapa 1 do construtor no sandbox, Etapa 2 ate' o candidato, revisao de "
               "terceiro do candidato, leitura do texto publico ao autor, rito, handoff), com o metodo de 17/11 em todo texto "
               "novo do programa"),
    "resultado": ("CONTRATO_v413_R0.md (sha16 %s; rascunho, congela depois da leitura de terceiro das pedras e da pagina); "
                  "O_QUE_FICA_CLARO_v413_R0.md (sha16 %s; lida ao autor antes do rito); ANCORAS_PROPOSTAS_v413.json (sha16 %s: "
                  "%d teoremas publicos, %d com estrela, nomes completos conferidos no relatorio de axiomas); a raiz da v412 "
                  "importada com os 21 novos compila (RAIZ_v413.json, sha16 %s): nenhuma colisao de nome; o pedido de leitura "
                  "de terceiro das pedras limpas (sha16 %s; licao da v412: texto limpo por agente vai a terceiro antes de valer; "
                  "o autor cola); ORDEM_ETAPA_1_v413.md (sha16 %s) solta a um agente da gerencia (o construtor da v413); "
                  "rascunho da ordem da Etapa 2 (sha16 %s). Um localizador tecnico tirado pela limpeza (o modulo da folga real "
                  "em LeituraBeta) foi reposto, licao da v412.") % (
        s16(ARQ["contrato"]), s16(ARQ["pagina"]), s16(ARQ["ancoras"]), anc["publicas"], anc["com_estrela"],
        s16(ARQ["raiz"]), s16(ARQ["leitura"]), s16(ARQ["ordem1"]), s16(ARQ["ordem2"])),
    "veredito": "CADEIA_DA_v413_ABERTA__CONTRATO_E_PAGINA_R0__ANCORAS_PROPOSTAS__RAIZ_SEM_COLISAO__ETAPA_1_EM_CURSO__NADA_INSTALADO",
    "estatuto": "REAL (os arquivos e as compilacoes); DECLARADO (o que o agente da Etapa 1 devolver, ate' a conferencia)",
    "status": "EM_CURSO", "olhou_dados": False,
    "defeito": ("o contrato e a pagina sao R0; a leitura de terceiro das pedras limpas depende do autor colar o pedido no "
                "Codex; o B(n) da v413 depende da Bancada no ar com a atualizacao do Codex"),
    "nao_refazer": "nao refazer a limpeza nem as compilacoes de conferencia; nao reconstruir o sandbox fora do comando unico da Etapa 1",
    "proximo_passo": ("conferir o fecho da Etapa 1; aplicar a leitura de terceiro das pedras (se vier); congelar o contrato R1; "
                      "soltar a Etapa 2; a revisao de terceiro do candidato (o autor cola); ler a pagina ao autor; rito; handoff"),
    "onde": str(V),
    "artefatos": [str(p) for p in ARQ.values()] + [str(FALA)],
    "refs": ["cadeia.preparacao_v413.pedras_limpas_20nov", "cadeia.preparacao_v412", "cadeia.preparacao_v412.etapa1_k412c",
             "cadeia.preparacao_v412.etapa2_candidato"],
    "nota": "fala do operador de 20/11 por bytes: «Concordo com tudo prossiga»",
}
pj = V / "mapa_rota_preparacao_v413_20nov.json"
pj.write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
out = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
print("(1) Mapa ROTA %s" % out[out.find('"seq"'):][:14])

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


def acha_revisao(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "revision" and isinstance(v, int):
                return v
            x = acha_revisao(v)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = acha_revisao(v)
            if x is not None:
                return x
    return None


rc, o = acom({"operation": "project", "reference": REF})
proj = json.loads(o.decode("utf-8"))
assert proj.get("ok") is True
rev = acha_revisao(proj)
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d350-cadeia-v413-aberta",
       "changes": {"records": [
           {"id": "c1-20nov-d350-cadeia-v413-aberta", "kind": "fact", "statute": "REAL",
            "text": ("O autor: «Concordo com tudo prossiga» (20/11, bytes). A cadeia da v413 abriu pelo molde da v412: contrato "
                     "R0, pagina publica R0, ancoras propostas (274 publicas, 112 com estrela), a raiz da v412 com os 21 novos "
                     "sem colisao, o pedido de leitura de terceiro das pedras limpas (o autor cola), a Etapa 1 solta a um "
                     "agente da gerencia (sandbox C:\\t\\k413c) e o rascunho da Etapa 2. Nada instalado."),
            "sources": [src(FALA), src(ARQ["contrato"]), src(ARQ["pagina"]), src(ARQ["ancoras"]), src(ARQ["raiz"]),
                        src(ARQ["leitura"]), src(ARQ["ordem1"])]}],
           "flow": {"phase": "v413_EM_PREPARACAO__CADEIA_ABERTA__ETAPA_1_EM_CURSO",
                    "next_action": ("(1) conferir o fecho da Etapa 1 (PRONTO_PARA_CANDIDATO_v413.json) quando o agente devolver; "
                                    "(2) o autor cola no Codex o pedido de leitura das pedras limpas; aplicar o que voltar e "
                                    "reconstruir pelo comando unico; (3) congelar o contrato R1 e soltar a Etapa 2 pela ordem "
                                    "final; (4) revisao de terceiro do candidato (o autor cola); (5) ler a pagina ao autor; "
                                    "(6) rito; (7) handoff a' custodia.")}}}
(V / "acom_c1_20261120_d350_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                  encoding="utf-8")
rc, ot = acom(req)
(V / "acom_c1_20261120_d350_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %d | rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
a = T.read_bytes()
mt = "<!-- ao_lado_20nov_cadeia_v413_aberta -->"
assert mt.encode() not in a and b"<!-- ao_lado_20nov_revisao_final_e_pedras_v413 -->" in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
tt = ("**AO LADO (20/11/2026, gerência c1): a cadeia da v413 aberta.** A fala (bytes, sha16 `%s`): «Concordo com tudo "
      "prossiga». Feito, pelo molde da v412: `work\\cadeia_de_selo\\v413\\CONTRATO_v413_R0.md` (sha16 `%s`, rascunho); a página "
      "pública `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md` (sha16 `%s`; lida ao autor antes do rito); as âncoras "
      "propostas (`insumos\\ANCORAS_PROPOSTAS_v413.json`: %d públicas, %d com estrela); a raiz da v412 com os 21 novos sem "
      "colisão; o pedido de leitura de terceiro das pedras limpas para o autor colar no Codex "
      "(`revisao_codex\\PEDIDO_DE_LEITURA_DAS_PEDRAS_LIMPAS_v413_20nov.md`, sha16 `%s`; lição da v412: texto limpo por agente vai a "
      "terceiro antes de valer); um localizador técnico que a limpeza tirou (`LeituraBeta`) foi reposto. A Etapa 1 "
      "(`ORDEM_ETAPA_1_v413.md`, sandbox `C:\\t\\k413c`) foi solta a um agente da gerência; o rascunho da Etapa 2 está pronto. "
      "Mapa: rota `cadeia.preparacao_v413`.\n%s") % (
    s16(FALA), s16(ARQ["contrato"]), s16(ARQ["pagina"]), anc["publicas"], anc["com_estrela"], s16(ARQ["leitura"]), mt)
novo = a.rstrip(b"\r\n") + fim + fim + tt.replace("\n", fim.decode()).encode("utf-8") + fim
bk = T.with_name(T.name + ".bak_" + TS + "_c1")
bk.write_bytes(a)
assert bk.read_bytes() == a
tmp = T.with_name(T.name + ".tmp_c1")
tmp.write_bytes(novo)
assert tmp.read_bytes() == novo
tmp.replace(T)
assert T.read_bytes() == novo and len(novo) > len(a)
print("(3) topico: %d -> %d B | backup %s" % (len(a), len(novo), bk.name))

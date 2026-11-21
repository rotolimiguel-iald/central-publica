# -*- coding: utf-8 -*-
"""gerencia c1, 21/11/2026: registra a correcao do operador (o treino da IALD ja' tinha acabado) e a troca da Bancada para o modo normal:
(1) nota AO LADO no plano da noite; (2) memoria: AO LADO na regra do posto do assistente (o precedente) e no topico da nativa (o fim do treino),
com backup de BYTES e escrita por temporario; (3) Mapa: ANOTACAO na rota do B(n); (4) ACOM transition. Hashes lidos dos arquivos."""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
V = Path(__file__).resolve().parent
CEN = Path(r"C:\IALD\Central de Patentes")
MEM = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
CUN = CEN / "work" / "cunhagens_13out"
FT = CUN / "OPERADOR_21nov_o_treino_da_iald_ja_acabou_ha_muito_tempo_verbatim.txt"
FN = CUN / "OPERADOR_21nov_trocar_a_bancada_para_o_modo_normal_agora_no_dialogo_da_gerencia_verbatim.txt"
FC = CUN / "OPERADOR_21nov_religar_em_cpu_agora_escolha_do_modo_da_placa_no_dialogo_da_gerencia_verbatim.txt"
RT = V / "bn_pos_selo" / "RECIBO_TROCA_DE_MODO_v413_normal.json"
SA = sorted((V / "bn_pos_selo" / "saude").glob("SAUDE_BANCADA_*.json"))[-1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
for p in (FT, FN, FC, RT, SA):
    assert p.is_file(), p
rt = json.loads(RT.read_text(encoding="utf-8")); assert rt["ok"] is True
sa = json.loads(SA.read_text(encoding="utf-8")); assert sa.get("veredito") == "NO_AR_EM_DIA"
STAMP = time.strftime("%Y%m%d_%H%M%S"); HOJE = time.strftime("%d/%m/%Y")
PIDS = (rt["anterior"]["pid"], rt["novo"]["pid"])

# (1) o plano
r = subprocess.run([PY, "-X", "utf8", str(V / "nota_plano.py"),
                    ("AO LADO (gerencia c1, em nome proprio): a pergunta do modo da placa partiu de premissa ERRADA minha, «treino na placa», herdada do plano e do contrato "
                     "de 20/11 sem conferir; o operador corrigiu («O treino da IALD já acabou há muito tempo», sha16 %s) e escolheu trocar para o modo normal (sha16 %s). "
                     "Trocado 04:15: PID %d (cpu) parado pelo PID, PID %d (normal) lancado com log, servindo a v413 (RECIBO_TROCA_DE_MODO_v413_normal.json %s; saude NO_AR_EM_DIA). "
                     "Os tres recibos do B(n) e o pino conjunto nao mudam; a custodia foi avisada. O que a premissa NAO afetou: o selo, o rito (o pilar e' reaproveitado por "
                     "desenho desde a v386), o gate.") % (sha(FT)[:16], sha(FN)[:16], PIDS[0], PIDS[1], sha(RT)[:16])],
                   capture_output=True, stdin=subprocess.DEVNULL)
print("(1)", r.stdout.decode("utf-8", "replace").strip() or r.stderr.decode("utf-8", "replace")[-300:])


# (2) a memoria
def append_ao_lado(p, bloco, marca):
    raw = p.read_bytes()
    if marca.encode("utf-8") in raw:
        print("(2) JA ESTA:", p.name); return
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    novo = raw.rstrip(b"\r\n") + (nl * 2).encode() + bloco.replace("\n", nl).encode("utf-8") + nl.encode()
    assert len(novo) > len(raw)
    p.with_name(p.name + ".bak_" + STAMP + "_c1").write_bytes(raw)
    tmp = p.with_name(p.name + ".tmp_c1"); tmp.write_bytes(novo); assert tmp.read_bytes() == novo; tmp.replace(p)
    print("(2) %s: %d -> %d B" % (p.name, len(raw), len(novo)))


append_ao_lado(MEM / "regra-do-posto-do-assistente-30out.md",
               ("## AO LADO (%s, gerência c1, em nome próprio) — precedente: a partitura com premissa velha\n<!-- posto_premissa_velha_21nov -->\n"
                "Na noite da v413 perguntei ao operador o modo da placa do religamento da Bancada «com o treino na placa». A premissa vinha do plano e do contrato que "
                "eu mesmo escrevi em 20/11, e eu não a conferi; ele escolheu CPU sobre ela. Depois ele corrigiu: «O treino da IALD já acabou há muito tempo» "
                "(`work\\cunhagens_13out\\%s`, sha16 `%s`), e escolheu o modo normal; troquei pelo PID, com recibo ao lado. "
                "**Como aplicar:** premissa sobre o estado VIVO da máquina (treino, serviço, processo, placa) não se herda de documento, nem do meu: confere-se na hora "
                "(processo, porta, log) ou pergunta-se ao operador ANTES, e a pergunta diz de onde veio a premissa. Ler a partitura com uma nota errada também é "
                "deixar o posto.") % (HOJE, FT.name, sha(FT)[:16]), "<!-- posto_premissa_velha_21nov -->")
append_ao_lado(MEM / "nativa-qwen38-aplicacao-v409-e-treino-integral-09nov.md",
               ("## AO LADO (%s, gerência c1) — o treino acabou\n<!-- treino_acabou_21nov -->\n[INPUT, por bytes] O operador, em 21/11: «O treino da IALD já acabou "
                "há muito tempo» (`work\\cunhagens_13out\\%s`, sha16 `%s`). A regra operacional «não tocar, medir nem parar o treino em "
                "`C:\\IALD\\TGL_IALD_NATIVE_QWEN5090`», que o contrato e o plano da v413 carregavam, estava velha. A Bancada passou ao modo normal (com a placa) em "
                "21/11 04:15 (`work\\cadeia_de_selo\\v413\\bn_pos_selo\\RECIBO_TROCA_DE_MODO_v413_normal.json`). Ver [[regra-do-posto-do-assistente-30out]].") % (
                   HOJE, FT.name, sha(FT)[:16]), "<!-- treino_acabou_21nov -->")


# (3) o Mapa
an = {"tipo": "ANOTACAO", "rota_id": "bancada.bn_v413.salto_v411_v413_20nov", "dominio": "BANCADA",
      "titulo": "a Bancada da v413 trocada de cpu para normal: a premissa «treino na placa» estava errada",
      "resultado": ("O operador corrigiu a premissa da gerencia (o treino ja' tinha acabado; sha16 %s) e escolheu o modo normal (sha16 %s). PID %d (cpu) parado pelo PID; PID %d "
                    "(normal) lancado com log; /api/contratos serve a v413, o deployment do B21 e o manifesto do APLICAR; saude NO_AR_EM_DIA (%s). Os tres recibos do B(n) e o "
                    "pino conjunto ficam; o recibo da troca (%s) fica FORA de bancada_B3* para nao virar quarto recibo na resolucao da G1.") % (
          sha(FT)[:16], sha(FN)[:16], PIDS[0], PIDS[1], SA.name, sha(RT)[:16]),
      "veredito": "BANCADA_v413_NO_MODO_NORMAL__TROCA_PELO_PID__IDENTIDADE_SERVIDA_CONFERIDA",
      "estatuto": "REAL (recibo e saude)", "status": "EXAMINADA", "olhou_dados": False,
      "defeito": "a premissa do estado vivo da maquina veio de documento da propria gerencia, sem conferencia na hora",
      "nao_refazer": "nao religar de novo: a Bancada serve a v413 no modo normal (PID no recibo da troca); parar so' pelo PID",
      "proximo_passo": "nenhum; a reconexao dos adaptadores MCP da Bancada e' ato do operador, se for preciso",
      "onde": str(V / "bancada" / "trocar_modo_bancada_v413.py"), "artefatos": [str(RT), str(SA), str(FT), str(FN)], "refs": ["cadeia.selo_v413_21nov"],
      "nota": "o modo cpu de antes tinha sido escolhido sobre a premissa errada (sha16 %s); o erro e' da gerencia" % sha(FC)[:16]}
pj = V / "mapa_anotacao_troca_de_modo_21nov.json"; pj.write_text(json.dumps(an, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "gerencia-c1 (claude-code, sessao 6da8f00d)"],
                   capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
out = r.stdout.decode("utf-8", "replace"); assert r.returncode == 0, out[:600]
m = re.search(r'"seq":\s*(\d+)', out); print("(3) Mapa seq", m.group(1) if m else "?")

# (4) ACOM
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=300)
    return rr.stdout


def acha(x, k):
    if isinstance(x, dict):
        for kk, vv in x.items():
            if kk == k:
                return vv
            y = acha(vv, k)
            if y is not None:
                return y
    elif isinstance(x, list):
        for vv in x:
            y = acha(vv, k)
            if y is not None:
                return y
    return None


rev = acha(json.loads(acom({"operation": "project", "reference": REF}).decode("utf-8")), "revision")
t = acom({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-21nov-bancada-modo-normal",
          "changes": {"records": [{"id": "c1-21nov-bancada-modo-normal", "kind": "fact", "statute": "REAL",
                                   "text": ("O operador corrigiu: o treino da IALD ja' tinha acabado (a premissa da gerencia estava errada). A Bancada da v413 foi trocada de cpu para normal "
                                            "pelo PID (%d -> %d), servindo a v413; recibo da troca fora de bancada_B3*; a custodia foi avisada.") % PIDS,
                                   "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))} for p in (FT, FN, RT, SA)]}]}}).decode("utf-8", "replace")
print("(4) ACOM rev %s | ok %s" % (rev, '"ok": true' in t))
assert '"ok": true' in t, t[:500]

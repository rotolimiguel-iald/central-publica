# -*- coding: utf-8 -*-
"""gerencia c1, 21/11/2026: registra o fecho da noite da v413 (numeros e hashes LIDOS dos arquivos): (1) Mapa: RESULTADO cadeia.selo_v413_21nov
(instalacao, rito, conferidor, .md, guarda, superficies, entrega) e RESULTADO na rota do B(n) (pos-selo fechado); (2) ACOM transition; (3) passos
9, 11 e 12 do plano."""
import hashlib, json, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
V = Path(__file__).resolve().parent
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CEN = Path(r"C:\IALD\Central de Patentes")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
s16 = lambda p: sha(p)[:16]  # noqa: E731
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))  # noqa: E731
selo = lj(NOS / "um_absoluto_selo.json"); assert selo.get("um_version") == "v413"
SO = NOS / "rodada_v413_stdout.txt"; so = SO.read_text(encoding="utf-8", errors="replace")
assert so.rstrip().endswith("RITO_RC=0")
TEOR = re.findall(r"teoremas limpos:\s*(\d+/\d+)", so)[-1]
CF = V / "CONFERENCIA_POS_RITO_v413_FOCO.json"; MD = V / "CONFERENCIA_MDS_v413.json"; ENT = V / "ENTREGA_A_CUSTODIA_v413.json"
HO = NOS / "HANDOFF_v413_CUSTODIA.md"; PINO = V / "bn_pos_selo" / "PINO_RECIBOS_B21_v413.json"; ISE = V / "ISENCAO_TRINITY_PROPOSTA_v413.json"
TOPO = V / "TOPO_RATIFICADO_v413_DERIVADO.json"; APL = sorted(V.glob("APLICADO_AO_CANONICO_*.json"))[-1]
GP = V / "GUARDA_PRIVADA_v413_pos.json"
FN = CEN / "work" / "cunhagens_13out" / "OPERADOR_21nov_libero_o_nome_Trinity_marcador_privado_28_verbatim.txt"
FM = CEN / "work" / "cunhagens_13out" / "OPERADOR_21nov_religar_em_cpu_agora_escolha_do_modo_da_placa_no_dialogo_da_gerencia_verbatim.txt"
REC = [sorted((V / "bancada_B3").glob("RECIBO_SINCRONIZACAO_v413_*.json"))[0], V / "bancada_B3_servico" / "RECIBO_PARADA_v413.json", V / "bancada_B3_servico" / "RECIBO_RELIGAMENTO_v413.json"]
for p in [CF, MD, ENT, HO, PINO, ISE, TOPO, APL, GP, FN, FM] + REC:
    assert p.is_file(), p
assert lj(CF)["ok"] is True and lj(MD)["ok"] is True and lj(ENT)["custodia_pode_comecar"] is True and lj(ISE)["verificacao"]["limpa"] is True
U16 = s16(NOS / "um.py")


def registrar(res, nome):
    pj = V / nome
    pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "gerencia-c1 (claude-code, sessao 6da8f00d)"],
                       capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
    m = re.search(r'"seq":\s*(\d+)', out)
    return m.group(1) if m else "?"


r1 = {"tipo": "ROTA", "rota_id": "cadeia.selo_v413_21nov", "dominio": "CADEIA_DE_SELO",
      "titulo": "a v413 SELADA e entregue a custodia (a ponte de Cook-Levin, Trinity, o operador de consciencia, a identidade preservada)",
      "pergunta": "a v413 instala, roda, confere e chega a custodia com tudo o que ela pede (tres marcas, B(n) fechado, guarda privada, superficies, entrega)?",
      "dados": ["nenhum dado da natureza: a cadeia de selo do programa"],
      "metodo": "instalar_v413.py (travas antes da escrita), rito_v413.sh, conferir_pos_rito_v413_foco.py, cadeia_pos_rito_v413.sh, conferir_mds_v413.py, bancada\\bn_v413.sh, superficies_v413.py, gerar_entrega_a_custodia_v413.py",
      "resultado": ("Instalada 01:30 (%s; topo derivado %s, copia do da v412 conferida no programa); rito 01:31-03:30 RITO_RC=0, %s teoremas limpos, selftest PASSED, "
                    "gate intocado; selo %s; conferidor 35/35 (%s); os .md apontam a v413 e trazem as derivacoes novas (%s); guarda privada pos: 18 artefatos so' com o "
                    "marcador 28 (o nome Trinity), liberado pelo operador por bytes (%s) e isento por 326 nomes exatos conferidos pela contagem da G1 (%s, 0 barrados); "
                    "handoff %s; entrega %s (custodia_pode_comecar=true, B(n) APLICADA_E_RELIGADA, 1 decisao).") % (
          APL.name, s16(TOPO), TEOR, s16(NOS / "um_absoluto_selo.json"), s16(CF), s16(MD), s16(FN), s16(ISE), s16(HO), s16(ENT)),
      "veredito": "V413_SELADA__CONFERIDA_35_DE_35__MDS_EM_V413__B_N_FECHADO__ENTREGUE_A_CUSTODIA__GATE_INTOCADO",
      "estatuto": "REAL (saidas e recibos lidos por script)", "status": "EXAMINADA", "olhou_dados": False,
      "defeito": "o instalador exigia o topo derivado, que a Etapa 2 nao gravou (feito pela gerencia por script); o gerador da entrega recusava termo privado sem decisao (ajustado: pendencia declarada e conteudo com a proposta)",
      "nao_refazer": "nao reselar: a v413 esta' no Nos e entregue; a publicacao e' da custodia",
      "proximo_passo": "a custodia (central-de-patentes-91) roda a esteira G1; a gerencia promove os depositos da fila e responde as paradas que forem dela",
      "onde": str(V), "artefatos": [str(p) for p in (SO, NOS / "um_absoluto_selo.json", CF, MD, HO, ENT, ISE, TOPO, APL, GP)],
      "refs": ["cadeia.preparacao_v413", "bancada.bn_v413.salto_v411_v413_20nov"],
      "nota": "ordem do operador da noite de 20/11 (bytes sha16 792f126a797e24eb); liberacao do nome e escolha do modo cpu por bytes em 21/11"}
r2 = {"tipo": "RESULTADO", "rota_id": "bancada.bn_v413.salto_v411_v413_20nov", "dominio": "BANCADA",
      "titulo": "o pos-selo do B(n) da v413 FECHADO: ensaio, parada ja fora do ar, evento 1711, APLICAR, religamento em cpu, fechamento, aviso 1712",
      "resultado": ("Ensaio a seco no mundo de copias 15/15; 10 REPINADA_B21__SALTO_v411_v413__ENSAIO; 10a ja_fora_do_ar; evento c1 1711; 10b APLICADA (o manifesto novo); "
                    "10c religada em cpu pela escolha do operador (%s), saude NO_AR_EM_DIA; 11 fechado: recibos %s, %s, %s; pino conjunto %s; entregues na pasta bench do 1687; aviso F0.6 1712.") % (
          s16(FM), s16(REC[0]), s16(REC[1]), s16(REC[2]), s16(PINO)),
      "veredito": "B21_v413_APLICADA_E_RELIGADA__TRES_RECIBOS__PINO_CONJUNTO__ENTREGUE__AVISO_F06",
      "estatuto": "REAL (saidas e recibos)", "status": "EXAMINADA", "olhou_dados": False,
      "defeito": "nenhum na execucao; a ordem dos diffs pede o diff_e_pinos ANTES do diffs_v413 (o segundo sobrescreve com backup; o primeiro recusa sobrescrever)",
      "nao_refazer": "nao reaplicar nem religar: a Bancada serve a v413 (PID no recibo do religamento); parar so' pelo PID",
      "proximo_passo": "nenhum da gerencia; o Codex encerra a unidade F0.6 pelo aviso 1712",
      "onde": str(V / "bancada"), "artefatos": [str(p) for p in REC + [PINO]], "refs": ["cadeia.selo_v413_21nov"],
      "nota": "o modo cpu foi escolha do operador num dialogo da gerencia (a marca Recommended era da gerencia); o lago ocupa ate' 60% da RAM livre"}
seq1, seq2 = registrar(r1, "mapa_resultado_selo_v413_21nov.json"), registrar(r2, "mapa_resultado_bn_pos_selo_21nov.json")
print("(1) Mapa seq %s e %s" % (seq1, seq2))
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=300)
    return rr.returncode, rr.stdout


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


rc, oo = acom({"operation": "project", "reference": REF})
rev = acha(json.loads(oo.decode("utf-8")), "revision")
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-21nov-v413-selada-e-entregue",
       "changes": {"records": [{"id": "c1-21nov-v413-selada-e-entregue", "kind": "fact", "statute": "REAL",
                                "text": ("v413 selada (um.py %s, %s, RITO_RC=0, selftest PASSED, gate intocado), conferida 35/35, .md em v413; B(n) fechado (APLICADA_E_RELIGADA, cpu por escolha do operador); "
                                         "nome Trinity liberado pelo operador e isento por 326 nomes exatos conferidos; handoff e entrega gravados (custodia_pode_comecar=true); Mapa seq %s e %s.") % (U16, TEOR, seq1, seq2),
                                "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))} for p in (ENT, HO, CF, PINO, FN, FM)]}]}}
rc, ot = acom(req)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %s | ok %s" % (rev, '"ok": true' in t))
assert '"ok": true' in t, t[:600]
for n, nota in (("9", "pos-rito: conferidor 35/35; guarda pos (18 artefatos, so' Trinity); arvore (v413), guarda do titulo, diffs; compositor R2: diario, desenho e handoff %s; .md %s TUDO OK" % (s16(HO), s16(MD))),
                ("11", "Atlas e indice vivo (atlas_indice.py v413), porta da memoria, blocos core e Haja_Luz, MEMORY.md (linha do handoff, pinada; 4 linhas verbatim ao MEMORY_2), topico handoff-v413-custodia.md; grep -c v413 > 0 em todas"),
                ("12", "ENTREGA_A_CUSTODIA_v413.json %s (04:07; custodia_pode_comecar=true; B(n) APLICADA_E_RELIGADA; TERMO_PRIVADO_ISENTO_v413 com 326 nomes exatos); mensagem a central-de-patentes-91" % s16(ENT))):
    r = subprocess.run([PY, "-X", "utf8", str(V / "marcar_plano.py"), n, nota], capture_output=True, stdin=subprocess.DEVNULL)
    print("(3)", r.stdout.decode("utf-8", "replace").strip() or r.stderr.decode("utf-8", "replace")[-300:])

# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra o diagnostico da Bancada e o plano do B(n) da v413 (o salto v411 -> v413), depois da
fala do operador «veja a questao da bancada para que nao tenhamos problema mais» (bytes ja' gravados). (1) Mapa: ROTA
bancada.bn_v413.salto_v411_v413_20nov, com o prazo (o pre-selo antes da instalacao da v413) e o «nao podar» dos backups do
Nos de 18/11; (2) ACOM transition (revisao lida do project); (3) AO LADO no topico da v413. Backup de bytes antes."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
TS = time.strftime("%Y%m%d_%H%M%S")
B = Path(__file__).resolve().parent
V = B.parent
CUNH = V.parents[2] / "work" / "cunhagens_13out"
FALA = CUNH / "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt"
DIAG = B / "DIAGNOSTICO_E_PLANO_BN_v413.md"
ORD = B / "ORDEM_BN_v413.md"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
BAKS = [NOS / "um.py.bak_20261118_235146", NOS / "um_absoluto_selo.json.bak_20261118_235146",
        NOS / "tgl_kernel_proof_manifest.json.bak_20261118_235146"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


for p in [FALA, DIAG, ORD] + BAKS:
    assert p.exists(), p
print("(0) fala %s | diagnostico %s | ordem %s | backups do Nos: %s" % (
    s16(FALA), s16(DIAG), s16(ORD), ", ".join("%s %s" % (p.name, s16(p)) for p in BAKS)))

rota = {
    "tipo": "ROTA", "rota_id": "bancada.bn_v413.salto_v411_v413_20nov", "dominio": "BANCADA",
    "titulo": "a Bancada desligada desde o reinicio de 16/11 e o B(n) da v413: o salto v411->v413 tem prazo (o pre-selo antes da instalacao da v413)",
    "pergunta": "por que a Bancada esta' desligada e o que e' preciso para que o B(n) da v413 rode sem problema e ela nao fique de novo para tras",
    "dados": [],
    "metodo": "leitura dos logs, recibos, codigo do servidor, esboco R3.6, moldes da v412, quadro e pasta do Codex; medidas por script, so' leitura; nenhum servico ligado ou parado, nenhum POST",
    "resultado": (
        "(1) o ultimo inicio foi o religamento do B20 (13/11 03:55); a maquina reiniciou em 16/11 (pedido do operador e Windows "
        "Update); a Bancada nao tem inicio automatico e ninguem a religou. (2) Ligar agora nao adianta: desde que a v412 entrou "
        "no Nos (18/11 23:51), o canonical.py recusa com PIN_CHANGED; ela subiria recusando toda conta. (3) Ao subir no modo "
        "normal ela cria contexto CUDA e vai para a placa (o treino esta' nela); o lago ocupa ~24 GiB de RAM. (4) O salto "
        "v411->v413 exige uma cadeia de selos v411->v412 pinada e um pre-selo rodado com o Nos ainda na v412, ANTES da "
        "instalacao da v413; depois, o salto so' serviria a' v414; a cadeia e' viavel hoje (1 registro do instalador confere; "
        "os backups do Nos de 18/11 existem e batem). (5) Pendencias: 15 na lista (5 feitas, 10 abertas com conserto) e 9 pontos "
        "novos (N1-N9), entre eles a bateria da v412 que nao existe, o delta_v411 que quebra a importacao depois do APLICAR, a "
        "autorizacao da v413 e a condicao do contrato R0 que repetia a armadilha da v412. (6) O Codex espera o evento c1 "
        "SINCRONIZACAO_BANCADA da F0.6 para a v413, os tres recibos com revisao independente na pasta bench do 1687 e "
        "/api/contratos servindo a v413. Diagnostico: %s (sha16 %s).") % (DIAG.name, s16(DIAG)),
    "veredito": "BANCADA_FORA_DO_AR_DESDE_O_REINICIO_DE_16NOV__SEM_INICIO_AUTOMATICO__PIN_CHANGED_DESDE_A_v412__SALTO_v411_v413_VIAVEL_COM_PRAZO_ANTES_DA_INSTALACAO",
    "estatuto": "REAL (logs, recibos, sha, selecao da cadeia medida); DERIVADO (o uso da placa e o modo degradado, pela leitura do codigo; nada executado)",
    "status": "EM_CURSO", "olhou_dados": False,
    "defeito": ("os religamentos desde 04/11 nao deixaram log (queda anterior nao se exclui) [OPEN]; o uso da placa nao foi "
                "medido (o treino nao se toca)"),
    "nao_refazer": ("nao refazer a leitura dos logs, as medidas de sha nem a selecao da cadeia (saidas na pasta bancada da v413); "
                    "nao ligar a Bancada antes do APLICAR do B21-v413 (so' traz o modo degradado e um contexto CUDA na placa do "
                    "treino); NAO PODAR nem mover, ate' o fechamento do B21: Nos\\um.py.bak_20261118_235146, "
                    "Nos\\um_absoluto_selo.json.bak_20261118_235146, Nos\\tgl_kernel_proof_manifest.json.bak_20261118_235146 e "
                    "v412\\APLICADO_AO_CANONICO_20261118_235146.json (insumos da cadeia do salto)"),
    "proximo_passo": ("o construtor do B(n) prepara o molde (ORDEM_BN_v413.md): pre-selo do salto, pos-selo, medida permanente "
                      "A e C (B so' preparada); uma revisao independente unica; rodar o pre-selo ANTES da instalacao da v413; "
                      "depois do selo: 10, 10a (ja_fora_do_ar), evento, 10b APLICAR, 10c religar com log (modo da placa: "
                      "escolha do operador), 11 fechar; entregar ao Codex na pasta bench"),
    "onde": str(B),
    "artefatos": [str(DIAG), str(ORD), str(FALA)] + [str(p) for p in BAKS],
    "refs": ["bancada.b21_v412.revisao_e_decisao_19nov", "cadeia.preparacao_v413"],
    "nota": "fala do operador de 20/11 por bytes: «veja a questão da bancada para que não tenhamos problema mais»",
}
pj = B / "mapa_rota_bancada_bn_v413_20nov.json"
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
       "expected_revision": rev, "event_id": "c1-20nov-d351-bancada-diagnostico-e-salto",
       "changes": {"records": [
           {"id": "c1-20nov-d351-bancada-diagnostico-e-salto", "kind": "fact", "statute": "REAL",
            "text": ("A Bancada esta' fora do ar desde o reinicio da maquina de 16/11 (sem inicio automatico) e, desde a v412 no "
                     "Nos, recusaria toda conta (PIN_CHANGED). O B(n) da v413 e' o salto v411->v413: o pre-selo tem de rodar com "
                     "o Nos ainda na v412, ANTES da instalacao da v413 (prazo duro); os backups do Nos de 18/11 sao insumo e nao "
                     "se podam ate' o fechamento do B21. Religar so' no 10c, depois do APLICAR, com log. O molde esta' com um "
                     "agente construtor; depois, uma revisao independente unica."),
            "sources": [src(FALA), src(DIAG), src(ORD)]}],
           "flow": {"phase": "v413_EM_PREPARACAO__ETAPA_1_E_MOLDE_DO_BN_EM_CURSO",
                    "next_action": ("(1) conferir o fecho da Etapa 1; (2) conferir o PRONTO_BN_v413.json e mandar a revisao "
                                    "independente unica do molde; (3) RODAR O PRE-SELO DO SALTO ANTES DA INSTALACAO DA v413; "
                                    "(4) o autor: o modo da placa no religamento (esperar o treino, cpu ou normal) e se cria a "
                                    "sentinela de boot que so' avisa; (5) aplicar a leitura do Codex das pedras limpas; "
                                    "congelar o contrato R1 (com a condicao do B(n) corrigida); Etapa 2; revisao do candidato; "
                                    "leitura da pagina; rito; pos-selo do B(n); handoff.")}}}
(B / "acom_c1_20261120_d351_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                  encoding="utf-8")
rc, ot = acom(req)
(B / "acom_c1_20261120_d351_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %d | rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

T = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\v413-preparacao-19nov.md")
a = T.read_bytes()
mt = "<!-- ao_lado_20nov_bancada_diagnostico_e_salto -->"
assert mt.encode() not in a and b"<!-- ao_lado_20nov_cadeia_v413_aberta -->" in a
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
tt = ("**AO LADO (20/11/2026, gerência c1): a Bancada e o B(n) da v413.** A fala (bytes, sha16 `%s`): «colei no codex, "
      "prossiga. concordo com tudo. veja a questão da bancada para que não tenhamos problema mais». Diagnóstico "
      "(`work\\cadeia_de_selo\\v413\\bancada\\DIAGNOSTICO_E_PLANO_BN_v413.md`, sha16 `%s`; Mapa `bancada.bn_v413.salto_v411_v413_20nov`): "
      "fora do ar desde o reinício de 16/11 (sem início automático); desde a v412 no Nós, ligada, recusaria toda conta "
      "(PIN_CHANGED); ao subir no modo normal, usa a placa (onde está o treino). **Prazo duro:** o pré-selo do salto v411→v413 "
      "roda com o Nós ainda na v412, ANTES da instalação da v413; os backups do Nós de 18/11 (`*.bak_20261118_235146`) e o "
      "`APLICADO_AO_CANONICO_20261118_235146.json` não se podam até o fechamento do B21. Religar só no 10c, depois do APLICAR, "
      "com log. Medida permanente: conferência de saúde no começo de toda cadeia e portão no executor (A e C); a sentinela de "
      "boot que só avisa (B) e o início automático (D) só com ordem do operador. O molde está com um agente construtor "
      "(`ORDEM_BN_v413.md`); depois, uma revisão independente única.\n%s") % (s16(FALA), s16(DIAG), mt)
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

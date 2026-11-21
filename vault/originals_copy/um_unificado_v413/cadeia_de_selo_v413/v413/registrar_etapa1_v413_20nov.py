# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra o fecho da Etapa 1 da v413 (construtor da v413, agente da gerencia), conferido pela
gerencia por script (CONFERENCIA_ETAPA1_v413.json). (1) Mapa: RESULTADO na rota cadeia.preparacao_v413; (2) ACOM
transition (revisao lida do project). Numeros lidos dos recibos."""
import hashlib, json, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
V = Path(__file__).resolve().parent
PRONTO, CONF = V / "PRONTO_PARA_CANDIDATO_v413.json", V / "CONFERENCIA_ETAPA1_v413.json"
K = V / "kernel"
ART = [PRONTO, CONF] + [p for p in [K / "KERNEL_RECIBO_v413.json", K / "FLAGS_v413.json", K / "POS_BUILD_v413.json",
                                    V / "INVENTARIO_CADEIA_v413.json", V / "DERIVACAO_ETAPA1_v413.json"] if p.exists()]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


pr = json.loads(PRONTO.read_text(encoding="utf-8"))
cf = json.loads(CONF.read_text(encoding="utf-8"))
assert cf["bom"] is True
esc = pr.get("escada_de_teoremas_e_bandeiras")
nb = pr.get("n_bandeiras_novas")
dec = pr.get("declaracoes_no_relatorio_de_axiomas")
print("(0) PRONTO %s | conferencia %s (bom) | escada %s | bandeiras novas %s | declaracoes %s" % (s16(PRONTO), s16(CONF), esc,
                                                                                               nb, dec))
res = {
    "tipo": "RESULTADO", "rota_id": "cadeia.preparacao_v413", "dominio": "CADEIA",
    "titulo": "a Etapa 1 da v413 fechada no sandbox C:\\t\\k413c e conferida pela gerencia",
    "resultado": ("PRONTO_PARA_CANDIDATO_v413.json (sha16 %s): o sandbox C:\\t\\k413c\\final nasceu do k412c (fontes conferidas "
                  "contra o Nos v412: 1920 de 1920); os 21 modulos novos compilaram a frio com saida zero e sem aviso; o "
                  "OResumoEPsiBit corrigido emite as mesmas declaracoes da v412, com os mesmos axiomas (93 dependentes "
                  "recompilados); escada de teoremas e bandeiras %s, com %s bandeiras novas ext_<modulo>_413_NNNN e nenhuma "
                  "chave antiga mudada; %s declaracoes no relatorio de axiomas, todas no trio, sem sorry; nenhuma colisao de "
                  "nome; portao do pilar: nada da v413 entra na chave do cache. Conferencia da gerencia (CONFERENCIA_ETAPA1_v413.json, "
                  "sha16 %s): as 21 instaladas sao as pedras limpas sem as linhas #print; o corrigido e' o da revisao; a raiz "
                  "importa os 21; as 1244 fontes antigas sao as do Nos.") % (s16(PRONTO), esc, nb, dec, s16(CONF)),
    "veredito": "ETAPA_1_DA_v413_FECHADA__21_MODULOS_A_FRIO__ESCADA_17786_PARA_18498__TODAS_AS_DECLARACOES_NO_TRIO__CONFERIDA_PELA_GERENCIA__NADA_NO_NOS",
    "estatuto": "REAL (os recibos do construtor e a conferencia da gerencia por script)",
    "status": "EM_CURSO", "olhou_dados": False,
    "defeito": ("o gerador do candidato tera' de SUBSTITUIR o texto embutido de um arquivo que ja' existe (o OResumoEPsiBit); o "
                "da v412 so' acrescentava; o instalador, o reverter e o conferidor precisam tratar esse arquivo "
                "(INVENTARIO_CADEIA_v413.json); a regra N1l do B(n) exige que as pedras sejam exatamente os arquivos novos ou "
                "mudados (o corrigido entra nas pedras e no campo kernel_corrigido); um script herdado regravou um recibo sem "
                "backup (causa corrigida em quatro scripts) e a medida de espaco livre antes da copia ficou [DECLARADO]"),
    "nao_refazer": "nao refazer o build e o Audit sem mudanca de fonte; trocar fonte: reconstruir_kernel_v413.py --manifesto <json> --pedras <pasta>",
    "proximo_passo": "aplicar a leitura de terceiro das pedras (quando voltar); congelar o contrato R1; a Etapa 2 (o candidato)",
    "onde": str(V),
    "artefatos": [str(p) for p in ART],
    "refs": ["cadeia.preparacao_v413.pedras_limpas_20nov", "cadeia.preparacao_v412.etapa1_k412c"],
    "nota": "construtor da v413: agente da gerencia c1 nesta sessao",
}
pj = V / "mapa_resultado_etapa1_v413_20nov.json"
pj.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                    "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
out = r.stdout.decode("utf-8", "replace")
assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
print("(1) Mapa RESULTADO %s" % out[out.find('"seq"'):][:14])

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
       "expected_revision": rev, "event_id": "c1-20nov-d352-etapa1-v413-fechada",
       "changes": {"records": [
           {"id": "c1-20nov-d352-etapa1-v413-fechada", "kind": "fact", "statute": "REAL",
            "text": ("Etapa 1 da v413 fechada no sandbox C:\\t\\k413c e conferida pela gerencia: 21 modulos a frio, sem aviso; o "
                     "OResumoEPsiBit corrigido com as mesmas declaracoes; escada %s, %s bandeiras novas; %s declaracoes no trio; "
                     "sem colisao; o pilar nao muda de chave. Para a Etapa 2: o gerador substitui o texto embutido de um arquivo "
                     "existente (o corrigido).") % (esc, nb, dec),
            "sources": [src(p) for p in ART]}],
           "flow": {"phase": "v413_EM_PREPARACAO__ETAPA_1_FECHADA__MOLDE_DO_BN_EM_CURSO",
                    "next_action": ("(1) a leitura do Codex das pedras limpas: aplicar e reconstruir pelo comando unico; (2) "
                                    "congelar o contrato R1 (a condicao do B(n) corrigida; o arquivo substituido); (3) a Etapa 2; "
                                    "(4) o molde do B(n): conferir, revisao independente unica, rodar o pre-selo ANTES da "
                                    "instalacao; (5) o autor: o modo da placa no religamento e a sentinela de boot.")}}}
(V / "acom_c1_20261120_d352_transition.request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1),
                                                                  encoding="utf-8")
rc, ot = acom(req)
(V / "acom_c1_20261120_d352_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %d | rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

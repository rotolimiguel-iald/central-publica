# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: registra (1) no Mapa: RESULTADO na rota cadeia.preparacao_v413 (a Etapa 1 refeita a frio depois
da leitura do Codex, 18/18; o contrato R1 congelado; as Etapas 2 e 3 soltas) e RESULTADO na rota
bancada.bn_v413.salto_v411_v413_20nov (o molde pronto, 76/76 hermeticos; a revisao independente solta); (2) ACOM transition;
(3) marca os passos 1 e 2 no PLANO_DA_NOITE (ao lado, com hora e sha16). Numeros lidos dos recibos."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"
V = Path(__file__).resolve().parent
CUNH = V.parents[2] / "work" / "cunhagens_13out"
A = {"pronto": V / "PRONTO_PARA_CANDIDATO_v413.json", "conf1": V / "CONFERENCIA_ETAPA1_v413.json",
     "r1": V / "CONTRATO_v413_R1.md", "ord2": V / "ORDEM_ETAPA_2_v413.md", "ord3": V / "ORDEM_ETAPA_3_v413.md",
     "par": V / "revisao_codex" / "CODEX_PEDRAS_LIMPAS_R1" / "PARECER.md", "man": V / "insumos" / "MANIFESTO_PEDRAS_v413.json",
     "bn": V / "bancada" / "PRONTO_BN_v413.json", "plano": V / "PLANO_DA_NOITE_v413_20nov.md",
     "fala": CUNH / ("OPERADOR_20nov_faca_tudo_ate_a_v413_rodada_e_disponivel_para_a_custodia_regenere_os_mds_sem_codex_"
                     "sem_delegar_a_outro_modelo_verbatim.txt")}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


def acha(o, chave):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == chave:
                return v
            x = acha(v, chave)
            if x is not None:
                return x
    elif isinstance(o, list):
        for v in o:
            x = acha(v, chave)
            if x is not None:
                return x
    return None


for k, p in A.items():
    assert p.exists(), k
pr = json.loads(A["pronto"].read_text(encoding="utf-8"))
cf = json.loads(A["conf1"].read_text(encoding="utf-8"))
assert cf["bom"] and cf["pronto_sha256"] == sha(A["pronto"])
esc, dec = acha(pr, "escada_de_teoremas_e_bandeiras"), acha(pr, "declaracoes_no_relatorio_de_axiomas")
chk = acha(pr, "checagens")
nchk = len(chk) if isinstance(chk, list) else None
nok = sum(1 for c in chk if c.get("ok")) if isinstance(chk, list) else None
print("(0) PRONTO %s (%s de %s) | escada %s | declaracoes %s | R1 %s | BN %s" % (s16(A["pronto"]), nok, nchk, esc, dec, s16(A["r1"]),
                                                                              s16(A["bn"])))


def mapa(obj, nome):
    pj = V / nome
    pj.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([PY, "-B", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem",
                        "gerencia-c1 (claude-code, sessao 6da8f00d)"], capture_output=True, stdin=subprocess.DEVNULL, timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    assert r.returncode == 0, out[:800] + r.stderr.decode("utf-8", "replace")[:800]
    return out[out.find('"seq"'):][:14]


r1 = {"tipo": "RESULTADO", "rota_id": "cadeia.preparacao_v413", "dominio": "CADEIA",
      "titulo": "a leitura do Codex das pedras limpas aplicada; a Etapa 1 refeita a frio (18/18); o contrato R1 congelado; Etapas 2 e 3 soltas",
      "resultado": ("Leitura de terceiro das pedras limpas pelo Codex (parecer sha16 %s): 16 aprovadas, 5 com ressalvas de texto, todas "
                    "aplicadas (tres localizadores tecnicos repostos; reader/hr; a unidade do expoente; o manifesto regerado depois do "
                    "diff). O sandbox C:\\t\\k413c refeito pelo comando unico, com os 22 modulos, a raiz e o Audit compilados a frio "
                    "no mesmo build (quarentena dos objetos antigos fora de work): fecho %s, %s de %s checagens, escada %s, %s "
                    "declaracoes no trio; conferencia da gerencia bom. CONTRATO_v413_R1.md congelado (sha16 %s; copia em "
                    "contrato_REV1): o arquivo do kernel substituido, as ancoras, o B(n) corrigido (o pre-selo antes da "
                    "instalacao; o religamento so' depois do APLICAR), D413.5 e D413.6. A ordem final da Etapa 2 (sha16 %s) e a "
                    "da Etapa 3 (sha16 %s) soltas a agentes da gerencia (mesmo modelo), pela ordem do operador da noite (bytes, "
                    "sha16 %s): tudo ate' a v413 rodada e disponivel para a custodia, sem o Codex.") % (
          s16(A["par"]), s16(A["pronto"]), nok, nchk, esc, dec, s16(A["r1"]), s16(A["ord2"]), s16(A["ord3"]), s16(A["fala"])),
      "veredito": "LEITURA_DAS_PEDRAS_APLICADA__ETAPA_1_A_FRIO_18_DE_18__CONTRATO_R1_CONGELADO__ETAPAS_2_E_3_EM_CURSO",
      "estatuto": "REAL (recibos e conferencias por script)", "status": "EM_CURSO", "olhou_dados": False,
      "defeito": "a checagem do fecho exige linha Built dos 22, da raiz e do Audit no MESMO build; um build incremental nao a cumpre (quarentena do conjunto antes de reconstruir)",
      "nao_refazer": "nao reconstruir o k413c sem mudanca de fonte; trocar fonte: quarentena_build_novos_v413.py --com-raiz e reconstruir_kernel_v413.py",
      "proximo_passo": "o candidato (Etapa 2); a preparacao do rito e do pos-rito (Etapa 3); a revisao de terceiro do candidato; o pre-selo do B(n) antes da instalacao",
      "onde": str(V), "artefatos": [str(A[k]) for k in ("pronto", "conf1", "r1", "ord2", "ord3", "par", "man", "fala")],
      "refs": ["cadeia.preparacao_v413.pedras_limpas_20nov"], "nota": "ordem do operador da noite por bytes"}
print("(1a) Mapa %s" % mapa(r1, "mapa_resultado_r1_etapas_20nov.json"))
bn = json.loads(A["bn"].read_text(encoding="utf-8"))
r2 = {"tipo": "RESULTADO", "rota_id": "bancada.bn_v413.salto_v411_v413_20nov", "dominio": "BANCADA",
      "titulo": "o molde do B(n) da v413 pronto (o salto v411->v413): 26 scripts, 76/76 testes hermeticos; revisao independente unica solta",
      "resultado": ("PRONTO_BN_v413.json (sha16 %s): a cadeia de selos v411->v412 gerada e conferida pelo esboco (2 elos); a bateria "
                    "da v412 pelo caminho (a); o runner, o conferir do salto, o gerar_pino, o diff_e_pinos, o p00 e o rodar do "
                    "pre-selo; o pos-selo inteiro (10 a 11, com a parada ja_fora_do_ar, o religamento com log e modo cpu, o "
                    "fechamento com os tres recibos); a conferencia de saude A, o portao C e o script da sentinela B (sem tarefa "
                    "agendada). Testes hermeticos 76/76 (34 negativos), controles do conferir 9/9, mutacoes 13/13, em mundo falso; "
                    "nada gravado na Bancada, no Nos, na v412, nos sandboxes ou no quadro. O pre-selo real so' roda depois da "
                    "revisao independente unica e antes da instalacao da v413.") % s16(A["bn"]),
      "veredito": "MOLDE_DO_BN_v413_PRONTO__76_DE_76_HERMETICOS__REVISAO_INDEPENDENTE_EM_CURSO__PRE_SELO_NAO_RODADO",
      "estatuto": "REAL (o fecho e os testes); DECLARADO (o construtor) ate' a revisao", "status": "EM_CURSO", "olhou_dados": False,
      "defeito": "a fotografia de arvore recem-escrita pode acusar producao alterada falsa (data de pasta atrasada no NTFS); erro do lado seguro",
      "nao_refazer": "nao regerar a cadeia v411->v412 nem a bateria da v412 sem mudanca",
      "proximo_passo": "a revisao independente; os consertos; rodar o pre-selo antes da instalacao; depois do selo, o pos-selo",
      "onde": str(V / "bancada"), "artefatos": [str(A["bn"])], "refs": ["cadeia.preparacao_v413"], "nota": ""}
print("(1b) Mapa %s" % mapa(r2, "bancada\\mapa_resultado_molde_bn_20nov.json"))

REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"


def acom(req):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                        input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return rr.returncode, rr.stdout


rc, o = acom({"operation": "project", "reference": REF})
proj = json.loads(o.decode("utf-8"))
assert proj.get("ok") is True
rev = acha(proj, "revision")
src = lambda p: {"kind": "artifact", "ref": "%s#sha256:%s" % (p, sha(p))}  # noqa: E731
req = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"},
       "expected_revision": rev, "event_id": "c1-20nov-d354-r1-congelado-etapas-2-3-bn",
       "changes": {"records": [
           {"id": "c1-20nov-d354-ordem-da-noite", "kind": "fact", "statute": "INPUT",
            "text": ("Ordem do operador da noite de 20/11 (bytes): fazer tudo ate' a v413 rodada e disponivel para a custodia; "
                     "regenerar os .md todos apontando a v413 com as derivacoes novas; sem o Codex; sem delegar a outro modelo; "
                     "entregar pelo handoff que a custodia deixou em work\\custodia_v413_preparo_20nov\\."),
            "sources": [src(A["fala"])]},
           {"id": "c1-20nov-d354-r1-e-etapas", "kind": "fact", "statute": "REAL",
            "text": ("Leitura do Codex das pedras aplicada; Etapa 1 refeita a frio, 18/18; contrato R1 congelado; Etapas 2 e 3 "
                     "soltas a agentes da gerencia; molde do B(n) pronto (76/76 hermeticos), revisao independente unica solta. "
                     "Plano duravel: PLANO_DA_NOITE_v413_20nov.md."),
            "sources": [src(A["pronto"]), src(A["r1"]), src(A["bn"]), src(A["plano"])]}],
           "flow": {"phase": "v413_NOITE__ETAPA_2_E_3_EM_CURSO__REVISAO_DO_BN_EM_CURSO",
                    "next_action": ("seguir o PLANO_DA_NOITE_v413_20nov.md: candidato; revisao de terceiro do candidato; pre-selo "
                                    "do B(n) ANTES da instalacao; guarda privada; instalar; rito; pos-rito com os .md v413; B(n) "
                                    "pos-selo em modo cpu; superficies; linha do MEMORY.md pelo memoria.py pinar; ENTREGA por ultimo.")}}}
rc, ot = acom(req)
(V / "acom_c1_20261120_d354_transition.receipt.json").write_bytes(ot)
t = ot.decode("utf-8", "replace")
print("(2) ACOM rev %s | rc %d | ok %s | %s" % (rev, rc, '"ok": true' in t, t[t.find('"revision"'):][:20]))
assert '"ok": true' in t

pl = A["plano"].read_bytes().decode("utf-8")
hora = time.strftime("%H:%M")
for antes, depois in [
        ("1. [ ] Reconstrução a frio", "1. [x] (%s; fecho %s, 18/18; conferência bom) Reconstrução a frio" % (hora, s16(A["pronto"]))),
        ("2. [ ] Contrato R1 congelado", "2. [x] (%s; R1 %s; ordem 2 %s) Contrato R1 congelado" % (hora, s16(A["r1"]), s16(A["ord2"])))]:
    assert pl.count(antes) == 1
    pl = pl.replace(antes, depois)
bk = A["plano"].with_name(A["plano"].name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
bk.write_bytes(A["plano"].read_bytes())
tmp = A["plano"].with_name(A["plano"].name + ".tmp")
tmp.write_bytes(pl.encode("utf-8"))
tmp.replace(A["plano"])
print("(3) plano: passos 1 e 2 marcados")

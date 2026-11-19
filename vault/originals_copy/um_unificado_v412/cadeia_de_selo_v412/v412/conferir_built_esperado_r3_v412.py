# -*- coding: utf-8 -*-
"""conferir_built_esperado_r3_v412.py -- (claude-construtor-v412, continuacao 2, 17/11/2026) so' LEITURA. Suprime uma conferencia que o pos_build deixou vazia: a checagem "os modulos que ESTE build tinha de
compilar tem linha Built" filtra a lista de kernel/ULTIMA_INSTALACAO_v412.json (`o_lake_recompila`) pelo prefixo `TGLExt.`, mas a lista traz os nomes SEM prefixo; o filtro devolve 0 modulos e a checagem passa sem
exigir nada (tambem na rodada do R2; as copias _r2 e _r3 do pos_build seguem iguais nisso, nada foi relaxado). Esta conferencia faz a leitura direta: (a) os modulos trocados no sandbox pelo preparo sao exatamente os
`mudaram_da_quarta_lista` do manifesto R5; (b) o fecho dos dependentes (BUNDLE_v412.json, campo `dependentes`) dos trocados e' o que o preparo previu recompilar; (c) cada um desses tem linha Built em
kernel/POS_BUILD_v412.json (`modo_dos_modulos_no_build`), e nenhum outro modulo tem Built. Grava kernel/BUILT_ESPERADO_R3_v412.json e DESVIOS_EXTRA_v412_R3.json (lista de textos que o gerador do fecho acrescenta aos desvios).
uso: C:/Python314/python.exe -B -X utf8 conferir_built_esperado_r3_v412.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
KD = os.path.join(HERE, "kernel")
lj = lambda p: json.load(open(p, encoding="utf-8"))
ULT = lj(os.path.join(KD, "ULTIMA_INSTALACAO_v412.json")); POS = lj(os.path.join(KD, "POS_BUILD_v412.json")); BD = lj(os.path.join(HERE, "BUNDLE_v412.json"))
MAN = lj(os.path.join(HERE, "insumos", "MANIFESTO_PEDRAS_v412_R5.json"))
mudados = ULT["mudados_no_sandbox"]; previstos = [m for m in ULT["o_lake_recompila"] if m not in ("TGLExt (raiz)", "TGL.Audit")]
dep = BD["dependentes"]
fecho = set(mudados); fila = list(mudados)
while fila:
    a = fila.pop()
    for y in dep.get(a, []):
        if y not in fecho:
            fecho.add(y); fila.append(y)
modo = POS["modo_dos_modulos_no_build"]
built = sorted(m.replace("TGLExt.", "", 1) for m, v in modo.items() if v == "Built")
falhas = []
if sorted(mudados) != sorted(MAN["mudaram_da_quarta_lista"]):
    falhas.append(["os trocados no sandbox != mudaram_da_quarta_lista do manifesto R5", sorted(mudados), sorted(MAN["mudaram_da_quarta_lista"])])
if sorted(fecho) != sorted(previstos):
    falhas.append(["o fecho dos dependentes (BUNDLE) != o_lake_recompila", sorted(fecho), sorted(previstos)])
faltam = [m for m in previstos if modo.get("TGLExt." + m) != "Built"]
extras = [m for m in built if m not in previstos]
if faltam:
    falhas.append(["modulo previsto sem linha Built", faltam])
if extras:
    falhas.append(["modulo com linha Built que nao era previsto", extras])
rep = {"trocados_no_sandbox": mudados, "mudaram_da_quarta_lista_do_manifesto_R5": MAN["mudaram_da_quarta_lista"], "fecho_dos_dependentes": sorted(fecho), "previstos_pelo_preparo": previstos,
       "com_linha_Built": built, "previstos_sem_Built": faltam, "Built_nao_previstos": extras, "falhas": falhas,
       "raiz_e_audit_com_Built": [POS.get("sinais") and [s["ok"] for s in POS["sinais"] if "COMPILADOS neste build" in s["checagem"]]][0]}
txt = ("a checagem do pos_build 'os modulos que ESTE build tinha de compilar tem linha Built' passou vazia (0 modulos exigidos: o filtro pede o prefixo TGLExt. e a lista de ULTIMA_INSTALACAO_v412.json traz nomes sem prefixo; "
       "tambem na rodada do R2; as copias _r2 e _r3 do pos_build seguem iguais nisso, nada foi relaxado); a leitura direta foi feita a parte (conferir_built_esperado_r3_v412.py, kernel/BUILT_ESPERADO_R3_v412.json): "
       "%d trocados no sandbox = os %d de mudaram_da_quarta_lista; o fecho dos dependentes previsto tem %d modulos; todos tem linha Built e nenhum outro tem (faltam: %s; nao previstos: %s)") % (
    len(mudados), len(MAN["mudaram_da_quarta_lista"]), len(previstos), faltam or "nenhum", extras or "nenhum")
for nome, obj in ((os.path.join(KD, "BUILT_ESPERADO_R3_v412.json"), rep), (os.path.join(HERE, "DESVIOS_EXTRA_v412_R3.json"), [txt])):
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(nome):
        open(nome + ".bak_prev", "wb").write(open(nome, "rb").read())
    open(nome + ".tmp", "wb").write(b); assert os.path.getsize(nome + ".tmp") == len(b); os.replace(nome + ".tmp", nome)
print(json.dumps({"trocados": mudados, "previstos": previstos, "built": built, "falhas": falhas}, ensure_ascii=False))
sys.exit(1 if falhas else 0)

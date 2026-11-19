# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026 (terminando a Etapa 2 com o construtor parado): deriva conferir_duodecima_lista_v412.py de
conferir_undecima_lista_v412.py, por trocas exatas com contagem. O e7_02 o derivava de conferir_decima_lista_v412.py, que compara com a
lista R10 (onde OCustoEAIsometria nao existe), e a conferencia quebrava; a comparacao certa e' com a lista anterior, a R11, que e' o
que a conferencia da decima primeira faz um degrau abaixo. O arquivo derivado pelo e7_02 fica ao lado (.bak) e e' substituido.
Uso: derivar_conferir_duodecima_v412.py [--executar]"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
t = (V / "conferir_undecima_lista_v412.py").read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo, n=1):
    global t
    assert t.count(velho) == n, "%d (esperava %d): %s" % (t.count(velho), n, velho[:80])
    t = t.replace(velho, novo); feitas.append((velho[:50], n))


troca("conferir_undecima_lista_v412.py -- (contrato R10) confere a DECIMA PRIMEIRA lista", "conferir_duodecima_lista_v412.py -- (contrato R11) confere a DECIMA SEGUNDA lista")
troca("pedras_r11", "pedras_r12", 7)
troca("MANIFESTO_PEDRAS_v412_R11", "MANIFESTO_PEDRAS_v412_R12", 3)
troca('R10_ANT = HERE / "insumos" / ("pedras_" + "r10")', 'R10_ANT = HERE / "insumos" / ("pedras_" + "r11")')
troca('mud = list(M10.get("mudaram_da_decima_lista") or [])', 'mud = list(M10.get("mudaram_da_decima_primeira_lista") or [])')
troca('"as tres fontes que mudaram da decima lista (campo mudaram_da_decima_lista) mudaram so\' em comentario: o codigo sem comentarios e\' identico; os bytes diferem (a emenda existe)", mud == ["AClausulaExemplificativa", "AFitaEOIndice", "OPsiBitDaFormula"]',
      '"as tres fontes que mudaram da decima primeira lista (campo mudaram_da_decima_primeira_lista; o parecer da ordem 034) mudaram so\' em comentario: o codigo sem comentarios e\' identico; os bytes diferem (a emenda existe)", sorted(mud) == ["AClausulaExemplificativa", "OCustoEAIsometria", "OPolinomioFixoEBeta"]')
troca('resto_igual = [m for m in ent10 if m not in mud and m not in (M10.get("novas_em_relacao_a_decima_lista") or [])',
      'resto_igual = [m for m in ent10 if m not in mud and m not in (M10.get("novas_em_relacao_a_decima_primeira_lista") or [])')
troca('e.chk("as outras 150 fontes sao identicas byte a byte as da decima lista; as tres novas (novas_em_relacao_a_decima_lista) nao existem na decima", not resto_igual and all(not (R10_ANT / (m + ".lean")).exists() for m in M10["novas_em_relacao_a_decima_lista"]) and len(M10["novas_em_relacao_a_decima_lista"]) == 3, len(ent10) - 3, resto_igual[:5])',
      'e.chk("as outras 153 fontes sao identicas byte a byte as da decima primeira lista; nenhuma fonte nova (novas_em_relacao_a_decima_primeira_lista vazio)", not resto_igual and M10["novas_em_relacao_a_decima_primeira_lista"] == [], len(ent10) - 3, resto_igual[:5])')
troca('salvar_json(HERE / "kernel" / "UNDECIMA_LISTA_CONFERIDA_v412.json", out)', 'salvar_json(HERE / "kernel" / "DUODECIMA_LISTA_CONFERIDA_v412.json", out)')
t = t.replace("# [DERIVADO v412 r7, claude-construtor-v412 (contrato R10)] copia de conferir_decima_lista_v412.py;",
              "# [DERIVADO v412, gerencia c1 (contrato R11), por derivar_conferir_duodecima_v412.py] copia de conferir_undecima_lista_v412.py, que era\n# [DERIVADO v412 r7, claude-construtor-v412 (contrato R10)] copia de conferir_decima_lista_v412.py;", 1)
compile(t, "conferir_duodecima_lista_v412.py", "exec")
b = t.encode("utf-8")
print("trocas:", feitas, "| bytes", len(b), "| sha16", hashlib.sha256(b).hexdigest()[:16])
if "--executar" in sys.argv:
    out = V / "conferir_duodecima_lista_v412.py"
    if out.exists():
        bak = out.with_name(out.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bak.write_bytes(out.read_bytes()); assert bak.read_bytes() == out.read_bytes()
    tmp = out.with_name(out.name + ".tmp_c1"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(out); print("gravado:", out.name)

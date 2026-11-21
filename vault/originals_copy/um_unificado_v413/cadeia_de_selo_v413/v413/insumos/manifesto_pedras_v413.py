# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: o MANIFESTO das pedras novas da v413, para a etapa de instalacao. Le' (nunca digita) os
recibos: ORIGEM_v413.json (procedencia e hash de cada fonte revisada), CONJUNTO_origem.json e CONJUNTO_pedras_limpas.json
(compilacao e auditoria de axiomas de todo teorema publico, na caixa da v413), CONJUNTO_kernel_edits.json e
kernel_edits\\ERRATA_OResumoEPsiBit.json (o modulo do kernel corrigido so' no texto) e caixa_v413\\CAIXA.json. Confere,
por modulo, que o codigo da pedra limpa (sem comentarios) e' o da origem. Fail-closed. Saida:
insumos\\MANIFESTO_PEDRAS_v413.json."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def le(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


orig = le(AQUI / "ORIGEM_v413.json")["modulos"]
c_o = le(AQUI / "CONJUNTO_origem.json")
c_l = le(AQUI / "CONJUNTO_pedras_limpas.json")
c_k = le(AQUI / "CONJUNTO_kernel_edits.json")
err = le(AQUI / "kernel_edits" / "ERRATA_OResumoEPsiBit.json")
caixa = le(AQUI / "caixa_v413" / "CAIXA.json")
assert c_o["todos_bons"] and c_l["todos_bons"] and c_k["todos_bons"]
mods = {}
for nome, o in sorted(orig.items()):
    po, pl = AQUI / "origem" / "TGLExt" / (nome + ".lean"), AQUI / "pedras_limpas" / "TGLExt" / (nome + ".lean")
    assert sha(po) == o["sha256_origem"], nome
    ident = sem_comentarios(po.read_text(encoding="utf-8")) == sem_comentarios(pl.read_text(encoding="utf-8"))
    assert ident, "codigo mudou: " + nome
    rl = c_l["modulos"][nome]
    assert rl["sha256"] == sha(pl) and rl["bom"], nome
    assert rl["teoremas"] == c_o["modulos"][nome]["teoremas"] == rl["relatorios"], nome
    mods["TGLExt." + nome] = {
        "autor_da_construcao": o["autor_da_construcao"], "fonte_revisada": o["fonte"],
        "sha256_fonte_revisada": o["sha256_fonte"], "recibo_do_hash": o["recibo_do_hash"],
        "sha256_origem": o["sha256_origem"], "pedra_limpa": str(pl), "sha256_pedra_limpa": sha(pl),
        "codigo_identico_a_origem": True, "bytes": pl.stat().st_size, "teoremas_publicos": rl["teoremas"],
        "relatorios_no_trio": rl["relatorios"], "imports_tglext": c_l["dependencias"][nome]}
k = c_k["modulos"]["OResumoEPsiBit"]
assert k["sha256"] == err["sha256_saida"] and k["bom"] and err["codigo_identico"]
rec = {
    "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
    "o_que_e": ("as pedras novas da v413 na forma do kernel (TGLExt.X), com o texto limpo pelo metodo de 17/11 e o codigo "
                "identico ao revisado; e o modulo do kernel que a v413 corrige so' no texto"),
    "caixa": {"onde": caixa["caixa"], "oleans_da_v412_por_link": caixa["oleans_da_v412"],
              "nota": "a caixa da v412 (C:\\t\\k412c) so' foi lida; a v413 compila numa arvore de links fisicos"},
    "modulos_novos": mods,
    "n_modulos_novos": len(mods),
    "teoremas_publicos_novos": sum(m["teoremas_publicos"] for m in mods.values()),
    "ordem_topologica_sugerida": None,
    "kernel_corrigido": {"TGLExt.OResumoEPsiBit": {
        "origem": err["origem"], "sha256_origem": err["sha256_origem"], "saida": err["saida"],
        "sha256_saida": err["sha256_saida"], "codigo_identico": True, "teoremas_publicos": k["teoremas"],
        "relatorios_no_trio": k["relatorios"], "fundamento": err["fundamento"],
        "sha256_fundamento": err["sha256_fundamento"]}},
    "recibos": {n: {"caminho": str(AQUI / n), "sha256": sha(AQUI / n)} for n in [
        "ORIGEM_v413.json", "CONJUNTO_origem.json", "CONJUNTO_pedras_limpas.json", "CONJUNTO_kernel_edits.json",
        "REGRAS_DA_LIMPEZA_v413.md", "DIFF_DA_LIMPEZA_v413.txt"]},
}
deps = c_l["dependencias"]
feito, ordem = set(), []
while len(ordem) < len(deps):
    prox = sorted(m for m in deps if m not in feito and all(d in feito for d in deps[m]))
    assert prox, "ciclo"
    for m in prox:
        ordem.append("TGLExt." + m)
        feito.add(m)
rec["ordem_topologica_sugerida"] = ordem
d = json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8")
tmp = AQUI / "MANIFESTO_PEDRAS_v413.json.tmp"
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(AQUI / "MANIFESTO_PEDRAS_v413.json")
print("MANIFESTO_PEDRAS_v413.json: %d modulos novos | %d teoremas publicos, todos no trio | kernel corrigido: "
      "OResumoEPsiBit (%d/%d) | sha16 %s" % (len(mods), rec["teoremas_publicos_novos"], k["relatorios"], k["teoremas"],
                                             sha(AQUI / "MANIFESTO_PEDRAS_v413.json")[:16]))

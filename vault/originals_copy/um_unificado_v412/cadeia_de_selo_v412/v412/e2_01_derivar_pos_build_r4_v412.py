"""Etapa 2, bloco 0: deriva pos_build_kernel_v412_r4.py do _r3 (que fica intacto) por trocas de texto exato com contagem conferida.
Causa corrigida: a checagem 'os modulos que ESTE build tinha de compilar tem linha Built' filtrava por m.startswith("TGLExt.") uma lista (kernel\\ULTIMA_INSTALACAO_v412.json, o_lake_recompila)
cujos nomes vem SEM o prefixo; o conjunto exigido ficava vazio e a checagem passava com zero itens. Agora: normaliza o prefixo, separa as duas entradas que nao sao modulo do bundle
(raiz e Audit, conferidas a parte), recusa nome desconhecido, e conta quantos itens examinou; zero itens e' falha. Modos novos: --so-built (nao escreve nada alem do recibo do modo) e o controle positivo."""
import hashlib, os, sys
from pathlib import Path

D = Path(__file__).resolve().parent
SRC = D / "pos_build_kernel_v412_r3.py"
DST = D / "pos_build_kernel_v412_r4.py"
src = SRC.read_bytes().decode("utf-8")
crlf = "\r\n" in src
assert not crlf, "o r3 e' LF"


def troca(t, velho, novo, n=1):
    c = t.count(velho)
    assert c == n, ("ancora nao unica ou ausente", c, n, velho[:80])
    return t.replace(velho, novo)


# 1) cabecalho
src = troca(src, "# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n# [DERIVADO v412 r4, 17/11/2026, claude-construtor-v412 (Etapa 2, bloco 0)] copia de pos_build_kernel_v412_r3.py (que fica intacto) com a CAUSA da checagem vazia corrigida (prefixo dos nomes de o_lake_recompila; conta de itens examinados; zero itens = falha); e_ _derivar: e2_01_derivar_pos_build_r4_v412.py.\n".replace("e_ _derivar", "derivador"), 1)

# 2) a checagem: funcao unica, usada na checagem real e no controle
VELHO = '''    exig_built = set(m for m in ULT.get("o_lake_recompila", []) if m.startswith("TGLExt."))
    modo = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in NEWMODS}
    chk("os modulos que ESTE build tinha de compilar (kernel\\\\ULTIMA_INSTALACAO_v412.json: %d) tem linha Built (a frio); %d modulos novos com Built neste log" % (len(exig_built), sum(1 for v in modo.values() if v == "Built")),
        all(modo.get(m) == "Built" for m in exig_built), [m for m in exig_built if modo.get(m) != "Built"][:5])
'''
assert src.count(VELHO) == 1, src.count(VELHO)
NOVO = '''    modo = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in NEWMODS}
    exig_built, fora_do_bundle, extras_raiz_audit = exigidos_built(ULT, NEWMODS)
    ok_built, faltam_built, n_exame_built = checa_built(exig_built, fora_do_bundle, modo)
    chk("os modulos que ESTE build tinha de compilar (kernel\\\\ULTIMA_INSTALACAO_v412.json, o_lake_recompila): %d EXAMINADOS (zero examinados e' falha; nomes sem o prefixo TGLExt. normalizados; raiz e Audit conferidos a parte: %s) tem linha Built (a frio); %d modulos novos com Built neste log" % (n_exame_built, extras_raiz_audit, sum(1 for v in modo.values() if v == "Built")),
        ok_built, {"examinados": n_exame_built, "sem_Built": faltam_built[:8], "fora_do_bundle": fora_do_bundle[:8]})
    if CONTROLE_POSITIVO or SO_BUILT:
        c1 = checa_built(exig_built | {"TGLExt.NomeQueNaoTemLinhaBuilt"}, fora_do_bundle, {**modo, "TGLExt.NomeQueNaoTemLinhaBuilt": None})
        c2 = checa_built(set(), [], modo)
        c3 = checa_built({m for m in exig_built}, fora_do_bundle, {**modo, next(iter(exig_built)): "Replayed"} if exig_built else modo)
        c4 = checa_built(exig_built, ["NomeDesconhecido"], modo)
        controles = [
            {"controle": "um nome exigido sem linha Built faz a checagem falhar", "falhou_como_devia": (c1[0] is False), "faltam": c1[1][:3], "examinados": c1[2]},
            {"controle": "zero itens exigidos faz a checagem falhar (nao passa vazia)", "falhou_como_devia": (c2[0] is False), "examinados": c2[2]},
            {"controle": "um exigido que so' teve linha Replayed faz a checagem falhar", "falhou_como_devia": (c3[0] is False), "faltam": c3[1][:3], "examinados": c3[2]},
            {"controle": "um nome fora do bundle em o_lake_recompila faz a checagem falhar", "falhou_como_devia": (c4[0] is False), "examinados": c4[2]},
            {"controle": "a checagem real (com a lista de verdade) passa e examinou mais de zero itens", "falhou_como_devia": False, "passou": ok_built, "examinados": n_exame_built, "ok": bool(ok_built and n_exame_built > 0)},
        ]
        todos_ok = all(c.get("falhou_como_devia") for c in controles[:4]) and controles[4]["ok"]
        rec = {"ok": bool(todos_ok), "n_controles": len(controles), "controles": controles, "exigidos_examinados": sorted(exig_built), "n_exigidos_examinados": n_exame_built,
               "raiz_e_audit": extras_raiz_audit, "modo": ("controle-positivo" if CONTROLE_POSITIVO else "so-built"),
               "nota": "o_lake_recompila lido de kernel/ULTIMA_INSTALACAO_v412.json; os logs lidos de kernel/lake_build.log (build da quinta lista, sem reconstruir); nada alem deste recibo foi escrito"}
        salvar_json(os.path.join(KD, "BUILT_CHECAGEM_CORRIGIDA_R4_v412.json"), rec)
        print("\\nMODO %s: %d controles, todos como devem: %s; examinados na checagem real: %d" % (rec["modo"], len(controles), todos_ok, n_exame_built))
        return bool(todos_ok and ok_built)
'''
src = troca(src, VELHO, NOVO, 1)

# 3) as funcoes e as chaves de modo, antes de principal()
FUNCS = '''SO_BUILT = "--so-built" in sys.argv
CONTROLE_POSITIVO = "--controle-positivo" in sys.argv


def exigidos_built(ult_, newmods_):
    """(exigidos, fora_do_bundle, extras): os modulos de o_lake_recompila com o prefixo TGLExt. normalizado, os nomes que NAO sao modulo do bundle e as duas entradas que nao sao modulo (raiz e Audit)."""
    exig_, fora_, extras_ = set(), [], []
    for m_ in ult_.get("o_lake_recompila", []):
        if m_ in ("TGLExt (raiz)", "TGL.Audit"):
            extras_.append(m_); continue
        nome_ = m_ if m_.startswith("TGLExt.") else "TGLExt." + m_
        if nome_ in newmods_:
            exig_.add(nome_)
        else:
            fora_.append(m_)
    return exig_, fora_, extras_


def checa_built(exig_, fora_, modo_):
    """(ok, faltam, n_examinados): ok so' com n_examinados > 0, nenhum nome fora do bundle e todos os exigidos com linha Built."""
    faltam_ = sorted(m_ for m_ in exig_ if modo_.get(m_) != "Built")
    return (len(exig_) > 0 and not fora_ and not faltam_), faltam_, len(exig_)


def principal():
'''
src = troca(src, "def principal():\n", FUNCS, 1)
src = troca(src, '''        tb = traceback.format_exc(); print("EXCECAO (fail-closed):\\n" + tb)
        try:
            salvar_json(os.path.join(KD, "POS_BUILD_v412.json"), {"ok": False, "excecao": tb, "sinais": sinais, "backups": BACKUPS})
''', '''        tb = traceback.format_exc(); print("EXCECAO (fail-closed):\\n" + tb)
        try:
            if not (SO_BUILT or CONTROLE_POSITIVO):   # (nos modos de conferencia o POS_BUILD vigente nao e' tocado)
                salvar_json(os.path.join(KD, "POS_BUILD_v412.json"), {"ok": False, "excecao": tb, "sinais": sinais, "backups": BACKUPS})
''', 1)
DST.write_bytes(src.encode("utf-8"))
print("gravado", DST, DST.stat().st_size, hashlib.sha256(DST.read_bytes()).hexdigest()[:16])

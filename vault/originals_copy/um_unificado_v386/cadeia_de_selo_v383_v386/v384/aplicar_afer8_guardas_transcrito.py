# -*- coding: utf-8 -*-
"""8a afericao: o candidato instalavel, a fumaca, os esperados e o instalador RECUSAM um pre-registro cuja ratificacao veio de transcrito de TESTE (ou nao diz
qual transcrito leu). Backups de BYTES: .bak_antes_afer8 (ja feitos para candidato/esperados/instalador; o da fumaca e' feito aqui)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
FU = os.path.join(HERE, "fumaca_v384.py")
if not os.path.exists(FU + ".bak_antes_afer8"):
    _r = open(FU, "rb").read(); open(FU + ".bak_antes_afer8", "wb").write(_r); assert open(FU + ".bak_antes_afer8", "rb").read() == _r
EDITS = {
    "gerar_candidato_v384.py": [
        ('''    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"
''', '''    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"
    assert (RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao nao diz qual transcrito leu, ou veio de transcrito de TESTE"   # 8a afericao
''')],
    "gerar_esperados_v384.py": [
        ('''assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
''', '''assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
assert (_RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao do candidato veio de transcrito de TESTE (ou nao diz qual) -- nao sigo"   # 8a afericao
''')],
    "instalar_v384.py": [
        ('''assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
''', '''assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
assert (_RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao do candidato veio de transcrito de TESTE (ou nao diz qual) -- nao sigo"   # 8a afericao
''')],
    "fumaca_v384.py": [
        ('''assert (PJ.get("ratificacao_do_operador") or {}).get("verbatim"), "o pre-registro nao foi ratificado pelo operador -- a fumaca nao roda"
''', '''assert (PJ.get("ratificacao_do_operador") or {}).get("verbatim"), "o pre-registro nao foi ratificado pelo operador -- a fumaca nao roda"
assert ((PJ.get("ratificacao_do_operador") or {}).get("transcrito") or {}).get("de_teste") is False, "a ratificacao veio de transcrito de TESTE (ou nao diz qual) -- a fumaca nao roda"   # 8a
''')],
}
for fn, pairs in EDITS.items():
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    assert open(p + ".bak_antes_afer8", "rb").read() == raw, fn
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c)
        s = s.replace(old, new)
    ast.parse(s)
    b = s.encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("ok", fn)

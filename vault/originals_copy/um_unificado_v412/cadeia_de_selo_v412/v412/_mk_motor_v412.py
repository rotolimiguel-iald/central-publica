# -*- coding: utf-8 -*-
"""_mk_motor_v412.py -- gera derivar_v412_motor.py a partir de v411\\derivar_v411_motor.py (mesmo motor; origem unica "v411"; mapa 410 -> 411 e 411 -> 412;
as LISTAS de versoes crescem, acrescentando o 411, nao se deslocam). Nao executa nada derivado. claude-construtor-v412, a servico da gerencia c1, 17/11/2026.
Molde: v411\\_mk_motor_v411.py (so' os rotulos sobem). Escrito pela ferramenta Write."""
import ast, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v411", "derivar_v411_motor.py"), "rb").read().decode("utf-8")
t = src
L11 = "(399|400|401|402|403|404|405|406|407|408|409|410)"; L12 = "(399|400|401|402|403|404|405|406|407|408|409|410|411)"
assert t.count(L11) >= 4, t.count(L11)
assert t.count("399..411") >= 2, t.count("399..411")
assert t.count('padrao=r"39[9]|40[0123456789]|41[01]"') == 1
t = t.replace(L11, "@L@").replace("399..411", "399..@12@").replace('padrao=r"39[9]|40[0123456789]|41[01]"', 'padrao=r"39[9]|40[0123456789]|41[012]"')
t = re.sub(r"(?<![0-9])(409|410|411)(?![0-9])", lambda m: str(int(m.group(1)) + 1), t)
t = t.replace("@L@", L12).replace("@12@", "412")
for esperado in ('ORIGENS = {"v411": os.path.join(CH, "v411")}', 'MAPAS = {"v411": {"410": "411", "411": "412"}}',
                 'NUM3 = re.compile(r"(?<![0-9])' + L12 + '(?![0-9])")', 'base_v411', 'padrao=r"39[9]|40[0123456789]|41[012]"', 'origem="v411"', "399..412"):
    assert esperado in t, esperado
assert "@" + "L@" not in t and "@12@" not in t
ast.parse(t)
out = os.path.join(HERE, "derivar_v412_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v412_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t), hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])

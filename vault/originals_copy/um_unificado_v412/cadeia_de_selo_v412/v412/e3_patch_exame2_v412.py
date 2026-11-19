# -*- coding: utf-8 -*-
"""e3_patch_exame2_v412.py -- segunda adaptacao do exame_pontos_v412.py (depois do e3_patch_exame_v412.py; o ensaio de diagnostico mostrou tres pontos falsos por rotulo/numero de heranca):
(1) _FLAGS10 e' o FLAGS da versao que INTRODUZIU o IALD2 e a AEscala (v410), nao o da v411 (que nao tem modulo novo e daria zero bandeiras): ponto_iald2 e ponto_aescala conferem o numero de bandeiras do modulo contra ele;
(2) a veredito do three_stress_tests_v387 no core desta versao difere do da base SO' nos numeros do kernel (KERNEL_n_OF_n, LADDER, contagens): a igualdade com a base se confere a menos de numeros (o mesmo criterio que o exame usa em vereditos_que_mudaram_vs_core0); o token do rotulo selado segue exigido. Script da cadeia."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "exame_pontos_v412.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")


def troca(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:100], s.count(old))
    s = s.replace(old, new)


if 'FLAGS_v410.json' in s:
    print("ja' adaptado"); sys.exit(0)
troca('_FLAGS10 = os.path.join(DL.V411, DL.D10.KERNEL_DIR, "FLAGS_v411.json")   # (v412) as bandeiras da v411, para os pontos HERDADOS da v411',
      '_FLAGS10 = os.path.join(DL.V410, DL.D10.KERNEL_DIR, "FLAGS_v410.json")   # (v412) as bandeiras da v410 (a versao que introduziu o IALD2 e a AEscala), para os pontos HERDADOS da v410; o FLAGS da v411 nao tem bandeira nova')
old = '"v387_veredito_selado_igual_ao_da_base": _nc387(str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) == _nc387(str((core0.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")))'
new = '"v387_veredito_selado_igual_ao_da_base": _n387(str((core.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict"))) == _n387(str((core0.get(DL.P2_REGISTRO_SELADO) or {}).get("verdict")))'
troca(old, new)
troca('_nc387 = lambda v_: re.sub(r"CORE_\\d+_TGL_VERDICTS_CONTAINING_\\d+_NOT_FALSIFIED_\\d+_INCONCLUSIVE_\\d+_AWAITING_OVERLAPPING_\\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)',
      '_nc387 = lambda v_: re.sub(r"CORE_\\d+_TGL_VERDICTS_CONTAINING_\\d+_NOT_FALSIFIED_\\d+_INCONCLUSIVE_\\d+_AWAITING_OVERLAPPING_\\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)\n_n387 = lambda v_: re.sub(r"\\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", _nc387(v_)))   # (v412) a menos de numeros: o kernel cresceu (a escada, as declaracoes, as contagens)')
tmp = P + ".tmp"
open(tmp, "wb").write(s.encode("utf-8")); assert os.path.getsize(tmp) > len(raw)
os.replace(tmp, P)
print("exame_pontos_v412.py (2) adaptado:", hashlib.sha256(open(P, "rb").read()).hexdigest()[:16])

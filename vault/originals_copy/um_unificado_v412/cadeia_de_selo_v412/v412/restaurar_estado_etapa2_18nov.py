# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026, em nome proprio: desfaz um engano meu. Rodei por engano o script de estado do construtor
(e2_41_estado_candidato_v412.py), que regravou um bloco de ETAPA_2_ESTADO_v412.json com a nota de um estado antigo. O script guardou,
antes de gravar, a copia ETAPA_2_ESTADO_v412.json.bak_20261118_150050. Aqui: mostra o que mudou entre a copia e o arquivo atual; guarda
o arquivo atual (o errado) como .engano_c1_20261118_150050; repoe os BYTES da copia. Uso: restaurar_estado_etapa2_18nov.py [--executar]"""
import hashlib, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
atual = V / "ETAPA_2_ESTADO_v412.json"; bak = V / "ETAPA_2_ESTADO_v412.json.bak_20261118_150050"
a, b = atual.read_bytes(), bak.read_bytes()
ja, jb = json.loads(a), json.loads(b)
print("atual:", len(a), "B", hashlib.sha256(a).hexdigest()[:16], "| copia anterior:", len(b), "B", hashlib.sha256(b).hexdigest()[:16])


def difs(x, y, c=""):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                print("  so' em um:", c + "/" + k)
            else:
                difs(x[k], y[k], c + "/" + k)
    elif x != y:
        print("  difere:", c, "|", str(y)[:110], "->", str(x)[:110])


difs(ja, jb)
if "--executar" in sys.argv:
    eng = V / "ETAPA_2_ESTADO_v412.json.engano_c1_20261118_150050"; assert not eng.exists()
    eng.write_bytes(a)
    tmp = atual.with_name(atual.name + ".tmp_c1"); tmp.write_bytes(b); assert tmp.stat().st_size == len(b); tmp.replace(atual)
    assert atual.read_bytes() == b
    print("reposto: o arquivo volta a ter os bytes da copia anterior | sha16", hashlib.sha256(atual.read_bytes()).hexdigest()[:16])

# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: confere, por script, que uma revisao de pedra nao mudou enunciado nem prova da anterior.
Tira comentarios e docstrings, corta o texto em declaracoes (theorem, lemma, def, abbrev, instance, structure, inductive)
e compara cada declaracao da versao velha com a de mesmo nome na nova, com os espacos normalizados.
Uso: conferir_enunciados.py VELHO.lean NOVO.lean  (rc 0 = nenhuma declaracao da velha removida ou mudada)."""
import hashlib, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
                  r"(theorem|lemma|def|abbrev|instance|structure|inductive)\s+(\S+)", re.M)
CORTE = re.compile(r"^(?:#print|end\s|namespace\s|section|open\s|variable)", re.M)


def sem_comentarios(s):
    s = re.sub(r"/-.*?-/", " ", s, flags=re.S)
    return re.sub(r"--[^\n]*", " ", s)


def declaracoes(p):
    s = sem_comentarios(Path(p).read_bytes().decode("utf-8"))
    ms = list(DECL.finditer(s))
    res = {}
    for i, m in enumerate(ms):
        fim = ms[i + 1].start() if i + 1 < len(ms) else len(s)
        corpo = CORTE.split(s[m.start():fim])[0]
        assert m.group(2) not in res, "nome repetido: " + m.group(2)
        res[m.group(2)] = " ".join(corpo.split())
    return res


velho, novo = sys.argv[1], sys.argv[2]
a, b = declaracoes(velho), declaracoes(novo)
removidas = sorted(set(a) - set(b))
mudadas = sorted(n for n in a if n in b and a[n] != b[n])
novas = [n for n in b if n not in a]
print("velho %s (%d declaracoes) -> novo %s (%d) | removidas %d | mudadas %d | novas %d" % (
    hashlib.sha256(Path(velho).read_bytes()).hexdigest()[:16], len(a),
    hashlib.sha256(Path(novo).read_bytes()).hexdigest()[:16], len(b), len(removidas), len(mudadas), len(novas)))
for n in removidas:
    print("  REMOVIDA:", n)
for n in mudadas:
    print("  MUDADA:", n)
if novas:
    print("  novas:", ", ".join(novas))
sys.exit(1 if (removidas or mudadas) else 0)

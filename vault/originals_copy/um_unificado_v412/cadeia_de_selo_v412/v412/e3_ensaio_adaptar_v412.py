# -*- coding: utf-8 -*-
"""e3_ensaio_adaptar_v412.py -- monta ensaio_a_seco_v412.py a partir do ORIGINAL v411/ensaio_a_seco_v411.py (a subida mecanica de rotulo fica guardada em ensaio_a_seco_v412.py.bak_*_bump):
cada edicao abaixo e' dita, com o numero de ocorrencias que tem de achar no original; ocorrencia diferente da dita = PARA (nada e' trocado por palpite). Roda de novo a qualquer momento (idempotente: parte sempre do original).
A v412 e' a v411 mais UM bundle de 40 modulos de kernel (903 bandeiras; escada 12308 -> 13211) e QUATRO registros por especificacao (so' dados; motor da v392); o registro com funcao e os specs da v411 passam a HERANCA.
Nada daqui entra no programa: e' script da cadeia."""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(os.path.dirname(HERE), "v411", "ensaio_a_seco_v411.py")
OUT = os.path.join(HERE, "ensaio_a_seco_v412.py")
EDS = os.path.join(HERE, "e3_edicoes_ensaio_v412.py")

raw = open(ORIG, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == "bf30e53cef035fe9", "o original da v411 nao e' o conferido"
src = raw.decode("utf-8")
ns = {"HERE": HERE}   # (os blocos longos ficam em arquivos .pytxt ao lado, lidos pela lista de edicoes)
exec(compile(open(EDS, encoding="utf-8").read(), EDS, "exec"), ns)
ED = ns["ED"]
log = []
for i, (eid, old, new, n) in enumerate(ED):
    if isinstance(old, tuple) and old[0] == "R":   # troca por INTERVALO: do inicio dito (unico) ate o fim dito (a primeira ocorrencia depois do inicio), inclusive
        _, a_, b_ = old
        if src.count(a_) != 1:
            print("PARA na edicao %d (%s): o inicio do intervalo aparece %d vezes (dito 1)" % (i, eid, src.count(a_))); sys.exit(2)
        i0 = src.index(a_); i1 = src.find(b_, i0 + len(a_))
        if i1 < 0:
            print("PARA na edicao %d (%s): o fim do intervalo nao foi achado" % (i, eid)); sys.exit(2)
        src = src[:i0] + new + src[i1 + len(b_):]
        log.append((eid, "intervalo de %d bytes" % (i1 + len(b_) - i0)))
        continue
    c = src.count(old)
    if (n == -1 and c < 1) or (n != -1 and c != n):   # n == -1: "uma ou mais" (renomeacao de rotulo, ocorrencias contadas e registradas)
        print("PARA na edicao %d (%s): achei %d ocorrencia(s), dito %d" % (i, eid, c, n))
        print("old[:200] =", repr(old[:200]))
        sys.exit(2)
    src = src.replace(old, new)
    log.append((eid, n))
tmp = OUT + ".tmp"
open(tmp, "wb").write(src.encode("utf-8"))
if os.path.getsize(tmp) < 0.9 * len(raw):
    print("PARA: o arquivo montado encolheu demais", os.path.getsize(tmp), len(raw)); sys.exit(3)
os.replace(tmp, OUT)
print("ensaio_a_seco_v412.py montado:", len(ED), "edicoes,", os.path.getsize(OUT), "bytes, sha16", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])

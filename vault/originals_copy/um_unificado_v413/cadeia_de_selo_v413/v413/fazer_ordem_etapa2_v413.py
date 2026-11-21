# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: grava a ORDEM FINAL da Etapa 2 da v413 (ORDEM_ETAPA_2_v413.md) a partir do rascunho, com os
sha16 lidos por script (fecho da Etapa 1, contrato R1 congelado, manifesto, ancoras, pagina) e as duas notas que a Etapa 1
deixou (o arquivo do kernel substituido; o delta do B(n))."""
import hashlib, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
RASC = V / "ORDEM_ETAPA_2_v413_RASCUNHO.md"
DEST = V / "ORDEM_ETAPA_2_v413.md"
A = {"fecho": V / "PRONTO_PARA_CANDIDATO_v413.json", "contrato": V / "CONTRATO_v413_R1.md",
     "manifesto": V / "insumos" / "MANIFESTO_PEDRAS_v413.json", "ancoras": V / "insumos" / "ANCORAS_PROPOSTAS_v413.json",
     "pagina": V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R0.md", "inventario": V / "INVENTARIO_CADEIA_v413.json"}


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


for k, p in A.items():
    assert p.exists(), k
t = RASC.read_text(encoding="utf-8")
m = re.search(r"^# Ordem da Etapa 2 da v413 — RASCUNHO.*?\n\n(?=Você é o)", t, re.S | re.M)
assert m
t = t[:m.start()] + "# Ordem da Etapa 2 da v413 (gerência c1, 20/11/2026)\n\n" + t[m.end():]
antes = ("Confira por script, antes de começar, os sha16 que a ordem final der (fecho, contrato, manifesto\n"
         "`insumos\\MANIFESTO_PEDRAS_v413.json`, âncoras `insumos\\ANCORAS_PROPOSTAS_v413.json`, página\n"
         "`o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md` ou a revisão que o contrato der). Se algum não bater, PARE.")
assert t.count(antes) == 1
depois = ("Confira por script, antes de começar, estes sha16: o fecho `PRONTO_PARA_CANDIDATO_v413.json` (`%s`); o contrato\n"
          "`CONTRATO_v413_R1.md` (`%s`; cópia em `contrato_REV1\\`); o manifesto `insumos\\MANIFESTO_PEDRAS_v413.json` (`%s`); as\n"
          "âncoras `insumos\\ANCORAS_PROPOSTAS_v413.json` (`%s`); a página `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md`\n"
          "(`%s`); o inventário da cadeia `INVENTARIO_CADEIA_v413.json` (`%s`). Se algum não bater, PARE.\n\n"
          "**Duas notas da Etapa 1, que valem aqui:** (a) o gerador SUBSTITUI o texto embutido de um arquivo que já existe no\n"
          "programa (`TGLExt/OResumoEPsiBit.lean`, só a docstring), além de acrescentar os 21 novos; o da v412 só acrescentava;\n"
          "(b) as constantes do B(n) (o sandbox curto, a fixação do `BANCADA_PINA_HOJE` na v411) ficam no `bancada\\delta_bn_v413.py`\n"
          "que o construtor do B(n) está fazendo; o delta da versão o importa quando ele existir, e não as redefine. O B(n) em si\n"
          "não é desta ordem.") % (s16(A["fecho"]), s16(A["contrato"]), s16(A["manifesto"]), s16(A["ancoras"]), s16(A["pagina"]),
                                   s16(A["inventario"]))
t = t.replace(antes, depois)
d = t.encode("utf-8")
tmp = DEST.with_name(DEST.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(DEST)
print("%s sha16 %s (%d B)" % (DEST.name, s16(DEST), len(d)))

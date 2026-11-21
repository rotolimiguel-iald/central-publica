# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: o CONTRATO_v413_R2.md (CONGELADO), por trocas EXATAS sobre o R1 (que fica): (1) a pagina publica
passa a R1 (a F37b herdada e o «provado» sem estatuto, achados da preparacao da Etapa 3); (2) as exigencias da custodia no
candidato (o par _V413_FONTES/_V413_VERBATINS2, mesmo vazio, e o registro kh_n1_cobertura_v413); (3) a guarda herdada
INTEIRA, inclusive a F37b, sobre todos os textos novos em portugues e ingles, com o ajuste minimo dito no relatorio e
refletido na pagina. Hashes lidos dos arquivos. Copia em contrato_REV2\\."""
import hashlib, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
R1, DEST = V / "CONTRATO_v413_R1.md", V / "CONTRATO_v413_R2.md"
P0 = V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R0.md"
P1 = V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R1.md"
HC = V.parents[1] / "custodia_v413_preparo_20nov" / "HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md"
E3 = V / "PRONTO_ETAPA3_v413.json"


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


for p in (R1, P0, P1, HC, E3):
    assert p.exists(), p
t = R1.read_bytes().decode("utf-8")
TROCAS = [
    ("# CONTRATO DA v413 — R1 (CONGELADO)\n", "# CONTRATO DA v413 — R2 (CONGELADO)\n"),
    ("> Gerência c1, ", ("> **R2** (gerência c1, %s): o R1 (sha16 `%s`) com três emendas: a página pública passa à R1 (`%s`, sha16 `%s`;\n"
                         "> a F37b herdada e o «provado» sem estatuto, achados pela preparação da Etapa 3, `PRONTO_ETAPA3_v413.json`, sha16\n"
                         "> `%s`); as exigências da custódia no candidato (seção 2); e a guarda herdada inteira sobre os textos novos (seção 5).\n"
                         "> Cópia congelada em `contrato_REV2\\`.\n>\n> Gerência c1, ") % (
        time.strftime("%d/%m/%Y %H:%M"), s16(R1), P1.name, s16(P1), s16(E3))),
    ("A página é `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md` (sha16 `%s`):" % s16(P0),
     "A página é `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R1.md` (sha16 `%s`; a R0 fica como registro):" % s16(P1)),
    ("**Checagens que todo registro traz**",
     ("**O que a custódia exige no candidato** (`work\\custodia_v413_preparo_20nov\\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md`,\n"
      "sha16 `%s`, seção 2.1): o par `_V413_FONTES` / `_V413_VERBATINS2` no `um.py`, mesmo vazio (a v413 não embute fala); o\n"
      "registro `kh_n1_cobertura_v413`, mesmo vazio, no molde do da v412, a partir do recibo `kernel\\KH_N1` da Etapa 1; e, na\n"
      "conferência C1 da custódia, o KH igual às declarações e os registros do artigo iguais aos blocos novos do core.\n\n"
      "**Checagens que todo registro traz**") % s16(HC)),
    ("O construtor entrega um recibo com cada unidade de texto da v413 em que aparece “P = nP” e o resultado da guarda.",
     ("O construtor entrega um recibo com cada unidade de texto da v413 em que aparece “P = nP” e o resultado da guarda. A guarda\n"
      "roda INTEIRA (todas as regras herdadas, inclusive a F37b: em cada trecho onde «P = nP» e «Turing» aparecem juntos, o próprio\n"
      "trecho traz «relativo ao leitor» ou uma negação) sobre TODOS os textos novos, em português e em inglês. Se um texto reprovar,\n"
      "o construtor faz o ajuste mínimo que não muda afirmação, diz cada ajuste no relatório, e a página pública recebe o mesmo\n"
      "ajuste numa revisão nova; nenhuma guarda se afrouxa.")),
    ("<!-- contrato_v413:R1_congelado -->", "<!-- contrato_v413:R2_congelado -->"),
]
for a, b in TROCAS:
    assert t.count(a) == 1, "trecho nao achado exatamente uma vez: %r" % a[:80]
    t = t.replace(a, b, 1)
d = t.encode("utf-8")
for dest in [DEST, V / "contrato_REV2" / DEST.name]:
    dest.parent.mkdir(exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(d)
    assert tmp.read_bytes() == d
    tmp.replace(dest)
print("%s sha16 %s (%d B) | pagina R1 %s" % (DEST.name, s16(DEST), len(d), s16(P1)))

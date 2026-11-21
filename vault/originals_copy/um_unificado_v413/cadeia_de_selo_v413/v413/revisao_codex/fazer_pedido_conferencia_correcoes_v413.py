# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: gera o pedido CURTO e OPCIONAL de conferencia ao Codex (o operador decide se cola): conferir
que as pedras do Kimi agora dizem o que os itens 4 a 7 do parecer consolidado pediram, e, por amostra, que a limpeza dos
textos (metodo de 17/11) nao fortaleceu nenhuma afirmacao. Hashes lidos dos arquivos por script."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REV = Path(__file__).resolve().parent
V413 = REV.parent
INS = V413 / "insumos"
PL = INS / "pedras_limpas" / "TGLExt"
OR = INS / "origem" / "TGLExt"
PAR = REV / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
RES = REV / "CODEX_CONSOLIDADO_R3" / "RESULTADO.json"
MAN = INS / "MANIFESTO_PEDRAS_v413.json"
DIF = INS / "DIFF_DA_LIMPEZA_v413.txt"
REG = INS / "REGRAS_DA_LIMPEZA_v413.md"
DEST = REV / "PEDIDO_DE_CONFERENCIA_DAS_CORRECOES_v413_20nov.md"


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


kimi = ["APonteDeCookLevin", "APropostaDaTensao", "ONomeEBeta", "AIdentidadePreservada"]
linhas = [
    "# Pedido de conferência ao Codex: as correções das pedras do Kimi na v413 (curto, opcional)",
    "",
    "Gerência c1, 20/11/2026. O operador decide se cola. É conferência de que as correções pedidas foram aplicadas, não "
    "revisão nova.",
    "",
    "## O que mudou desde o seu parecer",
    "",
    "1. As pedras novas da v413 estão na forma do kernel (`TGLExt.X`), compiladas juntas numa caixa da v413 (links físicos "
    "dos .olean da v412; a caixa da v412 só foi lida). O texto foi limpo pelo método do operador de 17/11 (no kernel entra "
    "só o que é verdade; a história fica no registro paralelo). O código de cada módulo é o revisado, conferido por script "
    "(sem comentários, idêntico). Regras da limpeza: `%s` (sha16 `%s`). Manifesto: `%s` (sha16 `%s`)." % (
        REG, s16(REG), MAN, s16(MAN)),
    "2. Nas quatro pedras do Kimi, o texto aplica os itens 4 a 7 do seu parecer consolidado (`%s`, sha16 `%s`; detalhe em "
    "`%s`, sha16 `%s`). Os enunciados e as provas não mudaram." % (PAR, s16(PAR), RES, s16(RES)),
    "",
    "## O que se pede",
    "",
    "1. Conferir, em cada uma das quatro, que a docstring diz o que o item pediu, e não mais:",
]
for n in kimi:
    linhas.append("   - `%s`: limpa `%s` (sha16 `%s`); origem revisada `%s` (sha16 `%s`)." % (
        n, PL / (n + ".lean"), s16(PL / (n + ".lean")), OR / (n + ".lean"), s16(OR / (n + ".lean"))))
linhas += [
    "2. Por amostra, no diff da limpeza (`%s`, sha16 `%s`), que nenhum texto limpo fortaleceu uma afirmação dos outros "
    "módulos (o diff só mostra texto; o código é idêntico)." % (DIF, s16(DIF)),
    "",
    "Sem instalação, sem alteração de kernel, um.py, gate ou publicação. Não é preciso recompilar: a gerência compilou o "
    "conjunto limpo (recibo `%s`)." % (INS / "CONJUNTO_pedras_limpas.json"),
]
d = ("\n".join(linhas) + "\n").encode("utf-8")
tmp = DEST.with_name(DEST.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(DEST)
print("%s sha16 %s (%d B)" % (DEST.name, s16(DEST), len(d)))

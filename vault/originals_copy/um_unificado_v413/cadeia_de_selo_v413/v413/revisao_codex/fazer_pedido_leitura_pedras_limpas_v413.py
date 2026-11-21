# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: gera o pedido de LEITURA DE TERCEIRO das pedras limpas da v413 (licao da v412, 17/11: texto
limpo por agente vai a terceiro antes de valer). Substitui, para colar, o pedido curto das correcoes do Kimi (que fica
como registro). O operador decide e cola; a gerencia nao envia ordem ao Codex. Hashes lidos dos arquivos por script."""
import hashlib, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REV = Path(__file__).resolve().parent
V413 = REV.parent
INS = V413 / "insumos"
PL, OR = INS / "pedras_limpas" / "TGLExt", INS / "origem" / "TGLExt"
KE = INS / "kernel_edits"
MAN, CONJ, DIF, REG = (INS / "MANIFESTO_PEDRAS_v413.json", INS / "CONJUNTO_pedras_limpas.json",
                       INS / "DIFF_DA_LIMPEZA_v413.txt", INS / "REGRAS_DA_LIMPEZA_v413.md")
PAR = REV / "CODEX_CONSOLIDADO_R3" / "PARECER.md"
CURTO = REV / "PEDIDO_DE_CONFERENCIA_DAS_CORRECOES_v413_20nov.md"
DEST = REV / "PEDIDO_DE_LEITURA_DAS_PEDRAS_LIMPAS_v413_20nov.md"


def s16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


man = json.loads(MAN.read_text(encoding="utf-8"))
conj = json.loads(CONJ.read_text(encoding="utf-8"))
assert conj["todos_bons"] and man["n_modulos_novos"] == 21
L = [
    "# Pedido de leitura de terceiro ao Codex: as pedras limpas da v413 (20/11/2026)",
    "",
    "**Escrito para:** o Codex, revisor de terceiro da v413. Quem cola é o operador; a gerência não envia ordem ao Codex. "
    "Este pedido substitui, para colar, o pedido curto das correções do Kimi (`%s`), que fica como registro e está contido "
    "aqui (item 3)." % CURTO.name,
    "",
    "## O que é",
    "",
    "As %d pedras novas da v413 estão na forma do kernel (`TGLExt.X`). O texto (comentários e docstrings) foi limpo pelo "
    "método do operador de 17/11: no `um.py` e no kernel que ele carrega entra só o que é verdade (enunciado, prova, "
    "estatuto, limites, fonte conhecida); a história fica no registro paralelo. As regras da limpeza: `%s` (sha16 `%s`). "
    "Limparam cinco agentes da gerência; a gerência leu cada diff e fez ajustes. O código de cada módulo é o que você "
    "revisou ou a gerência conferiu: sem comentários, idêntico (conferido por script); o fim de linha passou a LF e os "
    "imports dos módulos novos a `TGLExt.X`. O conjunto limpo compila numa caixa da v413 (links físicos dos .olean da v412; "
    "a caixa da v412 só foi lida), com %d teoremas públicos, todos com relatório de axiomas só no trio (recibo `%s`, sha16 "
    "`%s`). Manifesto com procedência e hashes: `%s` (sha16 `%s`)." % (
        man["n_modulos_novos"], REG, s16(REG), conj["teoremas"], CONJ, s16(CONJ), MAN, s16(MAN)),
    "",
    "## O que se pede",
    "",
    "Ler o texto de cada pedra limpa ao lado do texto anterior, no diff (`%s`, sha16 `%s`; o diff só mostra texto, porque "
    "o código é idêntico), e conferir:" % (DIF, s16(DIF)),
    "",
    "1. que nenhum texto limpo afirma mais do que antes, nem mais do que o enunciado;",
    "2. que nenhum localizador técnico se perdeu com a história (nome de módulo ou de teorema citado, arquivo de fonte, "
    "rótulo que distingue um objeto); na v412 a limpeza tirou referência junto com a história, e isso é o que mais se "
    "procura aqui;",
    "3. que as quatro pedras do Kimi dizem agora o que os itens 4 a 7 do seu parecer consolidado pediram (`%s`, sha16 "
    "`%s`): `APonteDeCookLevin` (não é ponte de custo de fita; `mov` é custo cobrado por definição; verifica o custo de uma "
    "atribuição dada), `APropostaDaTensao` (`_hA`/`_hB` ociosas; o iff não computa a escolha), `ONomeEBeta` (α definido; "
    "nenhum valor numérico; `k` é expoente), `AIdentidadePreservada` (a conjunção final sem a carga; o vetor não é "
    "configuração de máquina);" % (PAR, s16(PAR)),
    "4. que os estatutos ficaram como estavam (`[INPUT]`, `[ONTO]`, `[KNOWN]`, `[OPEN]`, `[REAL]`), e que não sobrou "
    "formulação antiga ao lado da vigente;",
    "5. a docstring corrigida de `TGLExt.OResumoEPsiBit.a_atualizacao_pela_clausula_seguinte` (item 8 do seu parecer): "
    "`%s` (sha16 `%s`; antes e depois em `%s`, sha16 `%s`)." % (
        KE / "TGLExt" / "OResumoEPsiBit.lean", s16(KE / "TGLExt" / "OResumoEPsiBit.lean"),
        KE / "ERRATA_OResumoEPsiBit.json", s16(KE / "ERRATA_OResumoEPsiBit.json")),
    "",
    "## Os arquivos",
    "",
    "| módulo | pedra limpa (sha16) | origem revisada (sha16) |",
    "|---|---|---|",
]
for nome in sorted(man["modulos_novos"]):
    n = nome.split(".", 1)[1]
    L.append("| `%s` | `%s` | `%s` |" % (nome, s16(PL / (n + ".lean")), s16(OR / (n + ".lean"))))
L += [
    "",
    "Pastas: pedras limpas em `%s`; origem em `%s`." % (PL, OR),
    "",
    "## Como e o que devolver",
    "",
    "- Não é preciso recompilar; se quiser, compile na caixa da v413 (`%s`), com o `LEAN_PATH` começando por ela, depois a "
    "caixa da v412 e os pacotes; só `lean.exe`, nunca `lake`." % (INS / "caixa_v413"),
    "- Sem instalação, sem alteração de kernel, `um.py`, gate ou publicação; não escreva nas pastas da gerência; consulte o "
    "Mapa de Rotas antes e registre depois, numa rota própria.",
    "- Para cada módulo: APROVADA, APROVADA_COM_RESSALVAS (com o texto proposto) ou REPROVADA, com o motivo em até três "
    "linhas. Um relatório de até 15 linhas e um recibo JSON com o sha256 de cada arquivo lido.",
]
d = ("\n".join(L) + "\n").encode("utf-8")
tmp = DEST.with_name(DEST.name + ".tmp")
tmp.write_bytes(d)
assert tmp.read_bytes() == d
tmp.replace(DEST)
print("%s sha16 %s (%d B)" % (DEST.name, s16(DEST), len(d)))

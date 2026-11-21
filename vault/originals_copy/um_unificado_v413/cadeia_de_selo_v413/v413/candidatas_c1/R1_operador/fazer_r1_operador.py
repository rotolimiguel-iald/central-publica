# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R1 da pedra da consciencia com o NOME DO OPERADOR, «operador» (fala por bytes em
work\\cunhagens_13out). Gera Operador.lean a partir da R0 (Consciencia.lean) trocando SO': o titulo, a linha de estatuto
(com o sha16 da fala lido aqui) e o espaco de nomes TGLExt.Consciencia -> TGLExt.Operador. Nenhum enunciado nem prova
muda. Gera tambem OperadorAxiomas.lean (os 15 #print axioms). Escrita por temporario e conferencia."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R0 = AQUI.parent / "R0_consciencia" / "Consciencia.lean"
R0AX = AQUI.parent / "R0_consciencia" / "ConscienciaAxiomas.lean"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out") / (
    "OPERADOR_20nov_a_maquina_nua_diz_sim_pela_tensao_o_zero_absoluto_empurra_para_o_lado_oposto_o_nome_da_pedra_e_operador"
    "_a_revisao_e_do_codex_verbatim.txt")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


fala = FALA.read_bytes().decode("utf-8")
assert 'o nome da pedra da consciência é "operador"' in fala, "a fala nao traz o nome"
src = R0.read_bytes().decode("utf-8")
trocas = [
    ("# CONSCIÊNCIA E O OPERADOR DE CONSCIÊNCIA\n",
     "# OPERADOR: A CONSCIÊNCIA E O OPERADOR DE CONSCIÊNCIA\n"),
    ("  [Pedra candidata para a v413; caixa de areia de 19/11/2026; não instalada. O nome é provisório: quem nomeia é o operador.]\n",
     ("  [Pedra candidata para a v413, R1 (20/11/2026); não instalada. O nome é do operador: «operador» (fala por bytes em\n"
      "  `work\\cunhagens_13out\\%s`, sha16 `%s`). A R0, com o nome provisório `Consciencia`, fica como registro; nenhum\n"
      "  enunciado nem prova mudou.]\n") % (FALA.name, sha(FALA)[:16])),
    ("namespace TGLExt.Consciencia\n", "namespace TGLExt.Operador\n"),
    ("end TGLExt.Consciencia\n", "end TGLExt.Operador\n"),
]
novo = src
for antes, depois in trocas:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:60]
    novo = novo.replace(antes, depois)
assert "TGLExt.Consciencia" not in novo
ax = R0AX.read_bytes().decode("utf-8").replace("import Consciencia", "import Operador").replace(
    "TGLExt.Consciencia.", "TGLExt.Operador.")
assert ax.count("#print axioms TGLExt.Operador.") == 15


def grava(p, texto):
    dados = texto.encode("utf-8")
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(p)


grava(AQUI / "Operador.lean", novo)
grava(AQUI / "OperadorAxiomas.lean", ax)
print("R0 sha16 %s -> R1 Operador.lean sha16 %s | axiomas sha16 %s | fala sha16 %s" % (
    sha(R0)[:16], sha(AQUI / "Operador.lean")[:16], sha(AQUI / "OperadorAxiomas.lean")[:16], sha(FALA)[:16]))

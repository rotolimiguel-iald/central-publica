# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: deriva candidatas_c1\\Token2.lean de candidatas_c1\\OSignoEAImagem.lean (REV57), por trocas exatas:
o nome dado pelo autor (Token2; o kernel selado ja' tem TGLExt.Token, da v397); a importacao da pedra Token selada; a leitura
em conjunto das duas, com a conjuncao por citacao (como a propria Token faz). O codigo dos demais teoremas nao muda.
Nao sobrescreve. Uso: derivar_token2.py [--executar]"""
import hashlib, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
C = Path(__file__).resolve().parent / "candidatas_c1"
src = C / "OSignoEAImagem.lean"
assert hashlib.sha256(src.read_bytes()).hexdigest() == hashlib.sha256((C / "REV57" / "OSignoEAImagem.lean").read_bytes()).hexdigest(), "a fonte nao e' a REV57"
t = src.read_bytes().decode("utf-8"); assert "\r\n" not in t
TROCAS = [
    ("import AMedidaEOIf\nimport OTempoEACauda\n", "import AMedidaEOIf\nimport OTempoEACauda\nimport TGLExt.Token\n", 1),
    ("# O SIGNO E A IMAGEM — a unidade de leitura é o signo, e a leitura é pela imagem",
     "# TOKEN2 — a unidade de leitura é o token: o signo, lido pela imagem", 1),
    ("A pedra `Token` (v397) nomeia o token como o psibit na testemunha estática. Esta pedra nomeia o token como a unidade de\nleitura. Nenhum termo daqui liga as duas.",
     "Esta pedra lê-se em conjunto com a pedra `Token` (v397): lá o token é o psibit na testemunha estática; aqui é a unidade de\nleitura. O termo `os_dois_tokens_leem_se_em_conjunto` é a conjunção das duas, por citação. Nenhum termo identifica o psibit\ncom o conjunto singularizado.", 1),
    ("/-- [DEF] **O CONTEÚDO DA FORMA**: o conjunto das atribuições que satisfazem a fórmula escrita. -/",
     "/-- **OS DOIS TOKENS LEEM-SE EM CONJUNTO.** A conjunção, por citação, do termo da pedra `Token` (o token como o psibit na\ntestemunha estática) com o termo desta pedra (no token, decidir e conferir levam os mesmos atos). Nenhuma matemática nova. -/\n"
     "theorem os_dois_tokens_leem_se_em_conjunto (φ : CNF n) (x : Fin n → Bool) :\n"
     "    (type_of% TGLExt.Token.token_is_the_psibit_in_the_static_witness)\n"
     "    ∧ (type_of% (no_token_decidir_e_conferir_levam_os_mesmos_atos φ x)) :=\n"   # (o parentese foi posto depois da 1a compilacao, que acusou erro de sintaxe; o Token2.lean gravado foi corrigido 'a mao, com esta mesma troca)
     "  ⟨TGLExt.Token.token_is_the_psibit_in_the_static_witness, no_token_decidir_e_conferir_levam_os_mesmos_atos φ x⟩\n\n"
     "/-- [DEF] **O CONTEÚDO DA FORMA**: o conjunto das atribuições que satisfazem a fórmula escrita. -/", 1),
    ("#print axioms TGLExt.OSignoEAImagem.o_signo_de_uma_parcela_confere",
     "#print axioms TGLExt.OSignoEAImagem.os_dois_tokens_leem_se_em_conjunto\n#print axioms TGLExt.OSignoEAImagem.o_signo_de_uma_parcela_confere", 1),
]
for a, b, n in TROCAS:
    assert t.count(a) == n, (t.count(a), n, a[:70]); t = t.replace(a, b)
k = t.count("TGLExt.OSignoEAImagem"); assert k >= 16, k
t = t.replace("TGLExt.OSignoEAImagem", "TGLExt.Token2")
assert "OSignoEAImagem" not in t and "«" not in t and "»" not in t
alvo = C / "Token2.lean"
print("Token2.lean", len(t.encode("utf-8")), "B | ocorrencias do espaco de nomes trocadas:", k, "| sha16", hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
if "--executar" in sys.argv:
    assert not alvo.exists(), "ja' existe"
    alvo.write_bytes(t.encode("utf-8")); print("gravado:", alvo)
else:
    print("ENSAIO A SECO")

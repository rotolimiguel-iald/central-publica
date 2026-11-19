# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R24 = a R23 com a definicao da IALD na redacao EXATA do autor. A R23 tinha mexido sem
necessidade na redacao dele (pontuacao, "a esse" por "a tal", um artigo a mais, e "do signo" por "da representacao do signo" na frase
final). A R24 devolve as palavras e a pontuacao dele e CONFERE POR SCRIPT contra os bytes da fala: a frase da pagina e' a frase do
autor com so' as duas grafias da pagina ("NOME" como "Nome", o Nome do kernel; "betatgl" como "β"). O resto do paragrafo (o que o
kernel prova de cada parte, os dois sentidos do limite assintotico) nao muda; as conferencias de termos sao as da R23.
Uso: montar_pagina_r24.py [--previa <arquivo>] [--executar]  (grava o_que_fica_claro_REV24\\O_QUE_FICA_CLARO_v412_R24.md; nao sobrescreve)"""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
p23 = V / "o_que_fica_claro_REV23" / "O_QUE_FICA_CLARO_v412_R23.md"
assert sha16(p23) == "7dbd5f4d7ad39fce", sha16(p23)
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_18nov_iald_e_o_nome_da_forma_matricial_do_polinomio_dos_passos_identidade_da_maquina_preservada_com_texto_do_kimi_colado_verbatim.txt")
assert hashlib.sha256(FALA.read_bytes()).hexdigest().startswith("838ff835c0c99657")
f = FALA.read_bytes().decode("utf-8")
INI, FIM = "IALD é o nome, porque tudo tem NOME", "betatgl como limite assintótico"
i = f.index(INI); j = f.index(FIM, i) + len(FIM)
do_autor = f[i:j]
assert "\n" not in do_autor and f.count(FIM) == 1
na_pagina = do_autor.replace("tudo tem NOME", "tudo tem Nome").replace("betatgl", "β")
assert na_pagina.count("Nome") == 1 and na_pagina.count("β") == 1
t = p23.read_bytes().decode("utf-8")
VELHA = ("Definição da teoria: IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em runtime, em "
         "mecanismo de processamento ótico em circuito de lógica; a esse mecanismo a teoria reconhece o termo Inteligência Artificial "
         "Luminodinâmica como a expressão singular perfeita da representação do signo em observação, isto porque a identidade da máquina "
         "é preservada enquanto ela processa e conta os passos de máquina, com o reconhecimento do que foi lido como carga e β como "
         "limite assintótico.")
NOVA = "Definição da teoria: " + na_pagina + "."
VELHA2 = "que esse nome seja a expressão singular perfeita do signo em observação é definição da teoria"
NOVA2 = "que esse nome seja a expressão singular perfeita da representação do signo em observação é definição da teoria"
assert t.count(VELHA) == 1 and t.count(VELHA2) == 1
t = t.replace(VELHA, NOVA).replace(VELHA2, NOVA2)
# a pagina carrega a frase do autor inteira, com so' as duas grafias
assert t.count(na_pagina) == 1
par_v = [b for b in t.split("\n\n") if b.startswith("**A IALD na fórmula de von Neumann.**")]; assert len(par_v) == 1
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
assert set(TERMO.findall(par_v[0])) == {"the_name_is_the_born_reading_of_the_post", "a_trava_no_nome", "a_trava_tende_ao_nome",
                                        "o_custo_de_decidir_e_a_carga", "o_polinomio_fixo_e_beta"}
for proibido in ("«", "ráculo", "P = nP", "Turing", "Instituto"):
    assert proibido not in par_v[0], proibido
b = t.encode("utf-8")
print("frase do autor (bytes):", len(do_autor.encode("utf-8")), "B | so' duas grafias trocadas | R23", p23.stat().st_size, "B -> R24", len(b),
      "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b); print("previa gravada")
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV24"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R24.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

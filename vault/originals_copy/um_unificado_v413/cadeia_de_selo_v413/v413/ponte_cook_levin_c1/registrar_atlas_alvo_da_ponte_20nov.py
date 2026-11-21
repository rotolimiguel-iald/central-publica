# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: nono registro de 20/11 no Atlas (append no fim, apos o oitavo), a errata ao lado do alvo da
ponte de Cook-Levin. Backup de bytes antes; escrita por temporario; confere que cresceu."""
import hashlib, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
TS = time.strftime("%Y%m%d_%H%M%S")
A = Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md")
FALA20 = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out"
              r"\OPERADOR_20nov_o_que_falta_para_fechar_a_ponte_cook_levin_a_pergunta_nao_e_a_que_vc_formulou_a_de_clay"
              r"_esta_respondida_verbatim.txt")
s20 = hashlib.sha256(FALA20.read_bytes()).hexdigest()[:16]
fala = FALA20.read_text(encoding="utf-8").strip()
a = A.read_bytes()
marca_ant = b"<!-- registro_20nov_trinity_r6_eletricidade -->"
marca = "<!-- registro_20nov_o_alvo_da_ponte_cook_levin -->"
assert marca.encode() not in a
assert marca_ant in a and len(a) - a.rfind(marca_ant) < 600, "o oitavo registro nao esta' no fim"
fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
texto = (
    "### Registro de 20/11/2026, nono (gerência c1) — o alvo da ponte de Cook–Levin (errata ao lado, em nome próprio)\n\n"
    "**A fala (do operador, 20/11/2026; bytes, sha16 `%s`) [INPUT]:** «%s».\n\n"
    "**A errata [REAL, as falas por bytes]:** a ordem de 19/11 pede levar o P = nP do dicionário às classes de "
    "Cook–Levin; «o alvo é a máquina de Turing nua» era enquadramento da gerência, e o plano da ponte (Mapa 2171) "
    "deixava fora a máquina com o leitor (v409). Leitura vigente: a ponte leva a máquina com o leitor "
    "(`uma_leitura_decide_SAT`, `o_psion_le_z`) à máquina padrão do Mathlib, com Cook–Levin por citação; a máquina sem "
    "leitor é a letra do enunciado do Instituto, fora do suporte fático da regra (D61), e não bloqueia a ponte. Onde o "
    "oitavo registro diz «[OPEN] os passos da máquina de Turing nua», leia-se: esse aberto é o da máquina sem leitor, não "
    "o da ponte. A Trinity fica como a parede medida da máquina sem leitor (Mapa 2200).\n\n"
    "**O que já existe e o que falta [REAL, levantamento por leitura e grep; Mapa 2201]:** existem o verificador na "
    "máquina padrão (Codex; até 20(letras+1)(n+1)+25 passos), a leitura β condicional (Codex; decide e reconstrói com no "
    "máximo letras+1 leituras) e o leitor exato do kernel (`o_psion_le_z`). O Mathlib da caixa não tem NP, nem "
    "Cook–Levin, nem máquina com oráculo e relógio (só `TM2ComputableInPolyTime`, com a composição como `proof_wanted`, "
    "e oráculo sem relógio em `RecursiveIn`). Faltam: a fiação (a partição do kernel em s = k·(−ln(1−β)) é a soma do "
    "Codex, logo o leitor do kernel cumpre a precisão com erro zero); a classe NP e a redução a uma leitura na língua do "
    "Mathlib; SAT em NP com a máquina do Codex; Cook–Levin como hipótese nomeada; revisão e instalação.\n\n"
    "**O que a ponte não diz:** na língua clássica o leitor é um oráculo; com um oráculo que conta soluções, «NP contido "
    "em P com o oráculo» é imediato [KNOWN]; o que é da TGL é que o oráculo é o leitor dela, por termo do kernel, e que "
    "ele lê num ato (física; Knill–Laflamme 1998 [KNOWN]). A E28 continua. A máquina sem leitor não é tocada "
    "(Baker–Gill–Solovay 1975 [KNOWN]).\n\n"
    "Estatuto: [INPUT] a fala; [REAL] a errata e o levantamento; [KNOWN] Cook 1971, Levin 1973, Baker–Gill–Solovay 1975, "
    "Knill–Laflamme 1998; [OPEN] a máquina sem leitor. Validade no kernel não é creditação; o gate não se move.\n%s"
) % (s20, fala, marca)
novo = a.rstrip(b"\r\n") + fim + fim + texto.replace("\n", fim.decode()).encode("utf-8") + fim
bk = A.with_name(A.name + ".bak_" + TS + "_c1")
bk.write_bytes(a)
assert bk.read_bytes() == a
tmp = A.with_name(A.name + ".tmp_c1")
tmp.write_bytes(novo)
assert tmp.read_bytes() == novo
tmp.replace(A)
assert A.read_bytes() == novo and len(novo) > len(a)
print("Atlas: %d -> %d B | backup %s | fala sha16 %s" % (len(a), len(novo), bk.name, s20))

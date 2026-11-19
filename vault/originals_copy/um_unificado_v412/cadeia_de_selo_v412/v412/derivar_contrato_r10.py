# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R10.md do R9 congelado, por trocas exatas (cada marca casa UMA vez), com os sha16
LIDOS dos arquivos. O R10 muda so' a pagina (R24: a definicao da IALD na redacao exata do autor, conferida por script contra os bytes
da fala, com so' as duas grafias da pagina) e acrescenta a decisao D235. Hora do relogio.
Uso: derivar_contrato_r10.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
r9p = V / "CONTRATO_v412_R9.md"; assert sha16(r9p) == sha16(V / "contrato_REV9" / "CONTRATO_v412_R9.md") == "b9aedccb000e308b"
p23 = V / "o_que_fica_claro_REV23" / "O_QUE_FICA_CLARO_v412_R23.md"; p24 = V / "o_que_fica_claro_REV24" / "O_QUE_FICA_CLARO_v412_R24.md"
assert sha16(p23) == "7dbd5f4d7ad39fce"
t = r9p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:90])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova, contem=None):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo) and (contem is None or contem in l)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R9 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R10 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, ",
            "> Gerência c1, 18/11/2026, %s. Substitui o R9 (`contrato_REV9\\CONTRATO_v412_R9.md`, sha16 `%s`), que fica como registro, como o R8, o R7, o R6, o R5, o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R9 trouxe, muda só a página (R24) e acrescenta a decisão D235." % (time.strftime("%H:%M"), sha16(r9p)),
            contem="Substitui o R8")
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R10.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R11.md`), nunca por cima.")
troca("**O que mudou do R8 para o R9** (para quem já estava seguindo o R8):",
      "**O que mudou do R9 para o R10** (para quem já estava seguindo o R9):\n\n"
      "1. Seção 6: a página passa a R24, que é a R23 com a definição da IALD na redação exata do autor (D235).\n"
      "2. Seção 4: a decisão D235.\n"
      "3. A lista de pedras não muda (a décima primeira, D230).\n"
      "4. O resto é o do R9, sem mudança.\n\n"
      "**O que tinha mudado do R8 para o R9:**")
troca("## 6. O texto público: a página R23", "## 6. O texto público: a página R24")
troca("O texto público novo é `o_que_fica_claro_REV23\\O_QUE_FICA_CLARO_v412_R23.md` (sha16 `7dbd5f4d7ad39fce`; 35368 bytes). É a R22 (",
      "O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R23 (`%s`, sha16 `%s`) com a definição da IALD na redação exata do autor (D235): a frase da página é a dele, conferida por script contra os bytes da fala, com só as duas grafias da página. A R23 é a R22 ("
      % (rel(p24), sha16(p24), p24.stat().st_size, rel(p23), sha16(p23)))
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D235** (18/11, da gerência, em nome próprio): a R23 tinha mexido sem necessidade na redação do autor (a pontuação, “a esse” por “a tal”, um artigo a mais e, na frase final, “do signo” por “da representação do signo”). A R24 devolve as palavras e a pontuação dele, e `montar_pagina_r24.py` confere contra os bytes da fala que a frase da página é a do autor com só as duas grafias da página: “NOME” como “Nome” (o Nome do kernel) e “betatgl” como “β”. O resto da D234 vale.\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca("<!-- contrato_v412:consolidado_R9_congelado:18nov -->", "<!-- contrato_v412:consolidado_R10_congelado:18nov -->")
assert "«" not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| R9", r9p.stat().st_size, "B -> R10", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R24", sha16(p24))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R10.md"; cp = V / "contrato_REV10" / "CONTRATO_v412_R10.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV10")

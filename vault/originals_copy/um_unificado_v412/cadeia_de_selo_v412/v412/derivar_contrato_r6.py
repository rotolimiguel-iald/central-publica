# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R6.md do R5 congelado, por trocas exatas (cada marca casa UMA vez), com os
sha16 LIDOS dos arquivos. O R6 muda so' a pagina (R19: a R18 com o paragrafo do Tetelestai) e acrescenta a decisao D227.
Hora do relogio. Uso: derivar_contrato_r6.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
r5p = V / "CONTRATO_v412_R5.md"; assert sha16(r5p) == sha16(V / "contrato_REV5" / "CONTRATO_v412_R5.md")
p18 = V / "o_que_fica_claro_REV18" / "O_QUE_FICA_CLARO_v412_R18.md"; p19 = V / "o_que_fica_claro_REV19" / "O_QUE_FICA_CLARO_v412_R19.md"
t = r5p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:80])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R5 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R6 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, 18:04. Substitui o R4",
            "> Gerência c1, 18/11/2026, %s. Substitui o R5 (`contrato_REV5\\CONTRATO_v412_R5.md`, sha16 `%s`), que fica como registro, como o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R5 trouxe, muda só a página (R19) e acrescenta a decisão D227." % (time.strftime("%H:%M"), sha16(r5p)))
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R6.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R7.md`), nunca por cima.")
troca("**O que mudou do R4 para o R5** (para quem já estava seguindo o R4):",
      "**O que mudou do R5 para o R6** (para quem já estava seguindo o R5):\n\n"
      "1. Seção 6: a página passa a R19, que é a R18 com um parágrafo novo na seção 2 (“Tetelestai: a consumação do ciclo”), logo antes de “O que esta seção não diz”.\n"
      "2. Seção 4: a decisão D227.\n"
      "3. O resto é o do R5, sem mudança.\n\n"
      "**O que tinha mudado do R4 para o R5:**")
troca("## 6. O texto público: a página R18", "## 6. O texto público: a página R19")
troca("O texto público novo é `o_que_fica_claro_REV18\\O_QUE_FICA_CLARO_v412_R18.md` (sha16 `c58564d29275ee75`; 31253 bytes). É a R14",
      "O texto público novo é `o_que_fica_claro_REV19\\O_QUE_FICA_CLARO_v412_R19.md` (sha16 `%s`; %d bytes). É a R18 (`o_que_fica_claro_REV18\\O_QUE_FICA_CLARO_v412_R18.md`, sha16 `%s`) com um parágrafo novo na seção 2, “Tetelestai: a consumação do ciclo”, logo antes de “O que esta seção não diz”: a definição da teoria, como entrada, e os seis termos que a sustentam na máquina da teoria (cada um conferido por script como teorema na fonte), com a ressalva de que os passos são atos sobre o todo e de que `1 − β` é o fator de cada passo, não um polinômio no número de letras. Esse parágrafo ainda não foi lido por terceiro: vai com a revisão do candidato. A R18 é a R14"
      % (sha16(p19), p19.stat().st_size, sha16(p18)))
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D227** (18/11): o autor pediu a leitura do Tetelestai na página, como a melhor palavra para a consumação cíclica do processamento mecânico que permite resposta coerente. Entra na seção 2 como definição da teoria, sem atribuição a pessoa, ligada à leitura que a casa já dá ao Tetelestai (a conferência que devolve consumado ou não consumado), com os termos que a sustentam na máquina da teoria. Não entra como resposta na régua do Instituto: os passos são atos sobre o todo, e `1 − β` não é um polinômio no número de letras. A comparação com o supercondutor, que veio na mesma formulação, fica fora do texto público.\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca("<!-- contrato_v412:consolidado_R5_congelado:18nov -->", "<!-- contrato_v412:consolidado_R6_congelado:18nov -->")
for proibido in ("«",):
    assert proibido not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| R5", r5p.stat().st_size, "B -> R6", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R19", sha16(p19))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R6.md"; cp = V / "contrato_REV6" / "CONTRATO_v412_R6.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV6")

# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R9.md do R8 congelado, por trocas exatas (cada marca casa UMA vez), com os sha16
LIDOS dos arquivos. O R9 muda so' a pagina (R23: a definicao da IALD escrita pelo autor no paragrafo de von Neumann, com o que o kernel
prova de cada parte) e acrescenta a decisao D234. Hora do relogio.
Uso: derivar_contrato_r9.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
r8p = V / "CONTRATO_v412_R8.md"; assert sha16(r8p) == sha16(V / "contrato_REV8" / "CONTRATO_v412_R8.md") == "f9d68ee5a1529186"
p22 = V / "o_que_fica_claro_REV22" / "O_QUE_FICA_CLARO_v412_R22.md"; p23 = V / "o_que_fica_claro_REV23" / "O_QUE_FICA_CLARO_v412_R23.md"
assert sha16(p22) == "92edc64b5038f4eb"
t = r8p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:90])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova, contem=None):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo) and (contem is None or contem in l)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R8 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R9 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, ",
            "> Gerência c1, 18/11/2026, %s. Substitui o R8 (`contrato_REV8\\CONTRATO_v412_R8.md`, sha16 `%s`), que fica como registro, como o R7, o R6, o R5, o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R8 trouxe, muda só a página (R23) e acrescenta a decisão D234." % (time.strftime("%H:%M"), sha16(r8p)),
            contem="Substitui o R7")
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R9.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R10.md`), nunca por cima.")
troca("**O que mudou do R7 para o R8** (para quem já estava seguindo o R7):",
      "**O que mudou do R8 para o R9** (para quem já estava seguindo o R8):\n\n"
      "1. Seção 6: a página passa a R23, que é a R22 com a definição da IALD escrita pelo autor no parágrafo “A IALD na fórmula de von Neumann”, seguida do que o kernel prova de cada parte (quatro termos citados por nome: um do kernel selado e três da lista final).\n"
      "2. Seção 4: a decisão D234.\n"
      "3. A lista de pedras não muda (a décima primeira, D230).\n"
      "4. O resto é o do R8, sem mudança.\n\n"
      "**O que tinha mudado do R7 para o R8:**")
troca("## 6. O texto público: a página R22", "## 6. O texto público: a página R23")
troca("O texto público novo é `o_que_fica_claro_REV22\\O_QUE_FICA_CLARO_v412_R22.md` (sha16 `92edc64b5038f4eb`; 34137 bytes). É a R21 (",
      "O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R22 (`%s`, sha16 `%s`) com uma troca pedida pelo autor no parágrafo “A IALD na fórmula de von Neumann”: sai a frase que dava como leitura da teoria que a IALD fosse a forma matricial do polinômio dos passos; entra a definição da teoria escrita por ele (D234), seguida do que o kernel prova de cada parte, com os termos `a_trava_no_nome` (kernel selado), `a_trava_tende_ao_nome`, `o_custo_de_decidir_e_a_carga` e `o_polinomio_fixo_e_beta` (lista final), e da leitura do limite assintótico nos dois sentidos que esses termos sustentam. Volta ao autor e vai à leitura de terceiro com o candidato. A R22 é a R21 ("
      % (rel(p23), sha16(p23), p23.stat().st_size, rel(p22), sha16(p22)))
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D234** (18/11): por pedido do autor, a página (R23) troca, no parágrafo “A IALD na fórmula de von Neumann”, a frase que dava como leitura da teoria que a IALD fosse a forma matricial do polinômio dos passos pela definição da teoria escrita por ele, sem atribuição (como na D231): IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em runtime, em mecanismo de processamento ótico em circuito de lógica; a identidade da máquina é preservada enquanto ela processa e conta os passos, com o que foi lido como carga e β como limite assintótico. O que o kernel prova de cada parte vai dito com o termo: `a_trava_no_nome` (kernel selado: a partir do estado uniforme, a coordenada de cada atribuição que resolve passa pela trava sem mudar, em todo tempo), `a_trava_tende_ao_nome` (a trava tende à projeção sobre o Nome), `o_custo_de_decidir_e_a_carga` (a leitura decide para toda fórmula se e somente se o tempo pago passa de n·ln 2) e `o_polinomio_fixo_e_beta` (qualquer número de passos acima do polinômio que β fixa antes de qualquer fórmula fecha o ciclo). “Limite assintótico” se lê nos dois sentidos que esses termos sustentam: β fixa o teto dos passos; o limite para onde a leitura tende é o Nome. Que o mecanismo seja ótico e que esse nome seja a expressão singular perfeita do signo em observação é definição da teoria, não teorema. A pedra candidata `AIdentidadePreservada`, que o Kimi provou para essa frase (seis teoremas; o recibo dele declara compilação sem sorry e só o trio; sem revisor), reembala termos que já estão na lista final e no kernel selado; pela D230 (ciclo de produção encerrado) ela fica para a v413, salvo ordem do autor, e a página não depende dela.\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca("<!-- contrato_v412:consolidado_R8_congelado:18nov -->", "<!-- contrato_v412:consolidado_R9_congelado:18nov -->")
assert "«" not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| R8", r8p.stat().st_size, "B -> R9", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R23", sha16(p23))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R9.md"; cp = V / "contrato_REV9" / "CONTRATO_v412_R9.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV9")

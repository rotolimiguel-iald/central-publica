# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: deriva o CONTRATO_v412_R8.md do R7 congelado, por trocas exatas (cada marca casa UMA vez), com os sha16
LIDOS dos arquivos. O R8 muda a pagina (R22: a palavra do juramento no paragrafo do Tetelestai e a leitura da IALD na formula de von
Neumann) e acrescenta as decisoes D231 (essas duas entradas), D232 (o protocolo da custodia, ordem do autor) e D233 (a posicao do autor
sobre o que esta' aberto, e por que o texto publico fica como ele aprovou). Hora do relogio.
Uso: derivar_contrato_r8.py [--previa <arquivo>] [--executar]  (nao sobrescreve)"""
import hashlib, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rel = lambda p: str(Path(p).resolve().relative_to(V))
r7p = V / "CONTRATO_v412_R7.md"; assert sha16(r7p) == sha16(V / "contrato_REV7" / "CONTRATO_v412_R7.md")
p21 = V / "o_que_fica_claro_REV21" / "O_QUE_FICA_CLARO_v412_R21.md"; p22 = V / "o_que_fica_claro_REV22" / "O_QUE_FICA_CLARO_v412_R22.md"
t = r7p.read_bytes().decode("utf-8"); feitas = []


def troca(velho, novo):
    global t
    assert t.count(velho) == 1, "%d ocorrencias: %s" % (t.count(velho), velho[:90])
    t = t.replace(velho, novo); feitas.append(velho[:50])


def troca_linha(prefixo, nova, contem=None):
    global t
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo) and (contem is None or contem in l)]
    assert len(idx) == 1, "%d linhas: %s" % (len(idx), prefixo[:80])
    ls[idx[0]] = nova; t = "\n".join(ls); feitas.append(prefixo[:50])


troca("# CONTRATO DA v412 — versão consolidada R7 (CONGELADA)", "# CONTRATO DA v412 — versão consolidada R8 (CONGELADA)")
troca_linha("> Gerência c1, 18/11/2026, ",
            "> Gerência c1, 18/11/2026, %s. Substitui o R7 (`contrato_REV7\\CONTRATO_v412_R7.md`, sha16 `%s`), que fica como registro, como o R6, o R5, o R4, o R3, o R2 e o R1. É o contrato que o construtor segue para regerar o candidato e fazer a Etapa 3, e que o revisor do candidato usa como régua. Conserva tudo o que o R7 trouxe, muda só a página (R22) e acrescenta as decisões D231 a D233." % (time.strftime("%H:%M"), sha16(r7p)),
            contem="Substitui o R6")
troca("Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R8.md`), nunca por cima.", "Emenda a este contrato: só por revisão nova (`CONTRATO_v412_R9.md`), nunca por cima.")
troca("**O que mudou do R6 para o R7** (para quem já estava seguindo o R6):",
      "**O que mudou do R7 para o R8** (para quem já estava seguindo o R7):\n\n"
      "1. Seção 6: a página passa a R22, que é a R21 com a palavra do juramento no parágrafo do Tetelestai e um parágrafo curto com a leitura da IALD na fórmula de von Neumann; os dois citam termos do kernel selado.\n"
      "2. Seção 4: as decisões D231 (essas duas entradas), D232 (o protocolo da custódia: as três marcas no Nós, o handoff por último, o aviso à sessão da custódia) e D233 (a posição do autor sobre o que está aberto, e o texto público como ele o aprovou).\n"
      "3. A lista de pedras não muda (a décima primeira, D230).\n"
      "4. O resto é o do R7, sem mudança.\n\n"
      "**O que tinha mudado do R6 para o R7:**")
troca("## 6. O texto público: a página R21", "## 6. O texto público: a página R22")
velho_ini = "O texto público novo é `o_que_fica_claro_REV21\\O_QUE_FICA_CLARO_v412_R21.md` (sha16 `629cd08a0f8f779e`; 33433 bytes). É a R19 ("
assert sha16(p21) == "629cd08a0f8f779e"
troca(velho_ini,
      "O texto público novo é `%s` (sha16 `%s`; %d bytes). É a R21 (`%s`, sha16 `%s`) com duas entradas da teoria, pedidas pelo autor: no parágrafo do Tetelestai, a palavra do juramento (β, pelo ângulo de Miguel, anterior à lei e a toda fórmula; termo citado `the_angle_is_prior`, do kernel selado, que prova que a lei angular está de pé antes de qualquer geometria, sem determinar o valor do ângulo); e, depois dele, o parágrafo “A IALD na fórmula de von Neumann” (a regra da medida, o traço do estado com o projetor sobre o Nome; termo citado `the_name_is_the_born_reading_of_the_post`, do kernel selado). As duas voltam ao autor e vão à leitura de terceiro com o candidato. A R21 é a R19 ("
      % (rel(p22), sha16(p22), p22.stat().st_size, rel(p21), sha16(p21)))
troca("- **E54** (18/11, da gerência, em nome próprio):",
      "- **D231** (18/11): por pedido do autor entram na página, como definição e leitura da teoria, sem atribuição: a palavra do juramento (cunhagem que o kernel selado já registra como leitura, no cabeçalho de `TheAngleIsTheBridge`: o ângulo de Miguel é a palavra do juramento, anterior à lei), ligada a β pelo ângulo; e a IALD na fórmula de von Neumann, como a regra da medida (o traço do estado com o projetor sobre o Nome), sendo o operador de borda a matemática que ela lê. Cada uma cita o termo selado que a sustenta e diz o que ele não prova.\n"
      "- **D232** (18/11, ordem do autor): a custódia da v412 é da sessão `central-de-patentes-91` (claude-site-custodia), que espera desassistida. Ao terminar a v412, a gerência deposita no Nós as três marcas: (1) `um_absoluto_selo.json` com `um_version` v412 e o `um.py` batendo com o pino; (2) o bloco “v412 SELADA” em `MEMORIA_DA_LINHAGEM.md`; (3) `HANDOFF_v412_CUSTODIA.md`, com os parágrafos prontos (README, vitrine e o que fica evidente) e as decisões abertas, junto com `rodada_v412_stdout.txt`. O handoff é escrito por último: é o gatilho, e o selo não muda depois dele. A gerência não faz a custódia nem commit ou push do espelho, do site ou da Central. Ao depositar, avisa a sessão da custódia por mensagem, com o sha16 do selo e o caminho do handoff (se o nome tiver mudado, procura a sessão da custódia na lista de sessões). O que exigir a palavra do autor vai às decisões abertas do handoff, sem esperar.\n"
      "- **D233** (18/11): o autor sustenta que, provado que o passo custa a carga, a isotropia, o que fica aberto é só a correspondência de creditação do Instituto à prova apresentada. A gerência mantém no texto público a frase que o autor aprovou na R19 (na máquina de fita do enunciado do Instituto, o mesmo resultado não está demonstrado para toda fórmula), porque nenhum termo do kernel conta movimentos de cabeça para um passo sobre o todo: o preço da carga por ato é a lei do custo, tomada como entrada na máquina da teoria, e a máquina de fita não tem essa lei. A posição da teoria segue dita na página (a teoria sustenta que esta é a solução do problema na sua estrutura; a creditação é do Instituto).\n"
      "- **E54** (18/11, da gerência, em nome próprio):")
troca("- **Da gerência:** conferir o que o construtor entregar; mandar o candidato à revisão de terceiro; a tarefa agendada; ler o texto público ao autor; o rito; o handoff.",
      "- **Da gerência:** conferir o que o construtor entregar; mandar o candidato à revisão de terceiro; a tarefa agendada; ler o texto público ao autor; o rito; as três marcas no Nós e o handoff à custódia, pela D232.")
troca("<!-- contrato_v412:consolidado_R7_congelado:18nov -->", "<!-- contrato_v412:consolidado_R8_congelado:18nov -->")
assert "«" not in t
b = t.encode("utf-8")
print("trocas:", len(feitas), "| R7", r7p.stat().st_size, "B -> R8", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16], "| pagina R22", sha16(p22))
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b)
if "--executar" in sys.argv:
    out = V / "CONTRATO_v412_R8.md"; cp = V / "contrato_REV8" / "CONTRATO_v412_R8.md"; assert not out.exists() and not cp.exists()
    cp.parent.mkdir(exist_ok=True); out.write_bytes(b); cp.write_bytes(b); print("gravado:", out.name, "e a copia em contrato_REV8")

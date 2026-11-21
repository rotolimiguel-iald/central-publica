# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: gera o CONTRATO_v413_R1.md (CONGELADO) a partir do rascunho R0, por trocas EXATAS (o R0 fica
intacto), com: a leitura de terceiro das pedras limpas aplicada; o fecho da Etapa 1; o arquivo do kernel substituido; a
proposta de ancoras; o B(n) corrigido pelo diagnostico da Bancada (o pre-selo do salto antes da instalacao; o religamento
so' depois do APLICAR); a decisao da autorizacao. Hashes lidos dos arquivos. Copia congelada em contrato_REV1\\."""
import hashlib, json, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent
R0 = V / "CONTRATO_v413_R0.md"
DEST = V / "CONTRATO_v413_R1.md"
INS = V / "insumos"
ARQ = {"man": INS / "MANIFESTO_PEDRAS_v413.json", "anc": INS / "ANCORAS_PROPOSTAS_v413.json",
       "pronto": V / "PRONTO_PARA_CANDIDATO_v413.json", "conf1": V / "CONFERENCIA_ETAPA1_v413.json",
       "inv": V / "INVENTARIO_CADEIA_v413.json", "par_leit": V / "revisao_codex" / "CODEX_PEDRAS_LIMPAS_R1" / "PARECER.md",
       "diag": V / "bancada" / "DIAGNOSTICO_E_PLANO_BN_v413.md", "pag": V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R0.md",
       "ord_bn": V / "bancada" / "ORDEM_BN_v413.md",
       "fala_bn": V.parents[2] / "work" / "cunhagens_13out" / "OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


for k, p in ARQ.items():
    assert p.exists(), k
conf1 = json.loads(ARQ["conf1"].read_text(encoding="utf-8"))
assert conf1["bom"] is True and conf1["pronto_sha256"] == sha(ARQ["pronto"]), "a conferencia da Etapa 1 nao e' do fecho atual"
anc = json.loads(ARQ["anc"].read_text(encoding="utf-8"))
assert anc["manifesto_sha256"] == sha(ARQ["man"]), "as ancoras nao sao do manifesto atual"
t = R0.read_bytes().decode("utf-8")
cab = re.search(r"\n> Gerência c1, .*?nunca por cima\.\n", t, re.S)
assert cab
NOVO_CAB = (
    "\n> Gerência c1, {data}. **Congelado.** Consolida o rascunho R0 (`CONTRATO_v413_R0.md`, sha16 `{r0}`) com: a leitura de\n"
    "> terceiro das pedras limpas (parecer `revisao_codex\\CODEX_PEDRAS_LIMPAS_R1\\PARECER.md`, sha16 `{pl}`: 16 aprovadas, 5\n"
    "> com ressalvas de texto, todas aplicadas); o fecho da Etapa 1 (`PRONTO_PARA_CANDIDATO_v413.json`, sha16 `{pr}`, conferido\n"
    "> pela gerência em `CONFERENCIA_ETAPA1_v413.json`, sha16 `{cf}`); e o diagnóstico da Bancada\n"
    "> (`bancada\\DIAGNOSTICO_E_PLANO_BN_v413.md`, sha16 `{dg}`). Cópia congelada em `contrato_REV1\\`. Emenda só por revisão\n"
    "> nova (`CONTRATO_v413_R2.md`), nunca por cima.\n").format(
    data=time.strftime("%d/%m/%Y %H:%M"), r0=s16(R0), pl=s16(ARQ["par_leit"]), pr=s16(ARQ["pronto"]), cf=s16(ARQ["conf1"]),
    dg=s16(ARQ["diag"]))
t = t[:cab.start()] + NOVO_CAB + t[cab.end():]
TROCAS = [
    ("# CONTRATO DA v413 — RASCUNHO R0\n", "# CONTRATO DA v413 — R1 (CONGELADO)\n"),
    (None, "MAN"),
    ("**Âncoras.** Cada registro ancora,",
     "**Âncoras.** A proposta é `insumos\\ANCORAS_PROPOSTAS_v413.json` (sha16 `%s`: %d teoremas públicos, %d com estrela, nomes\n"
     "completos conferidos no relatório de axiomas). Cada registro ancora," % (s16(ARQ["anc"]), anc["publicas"], anc["com_estrela"])),
    ("**Bandeiras.** Prefixo `ext_<modulo>_413_NNNN`.",
     "**O arquivo substituído.** O gerador do candidato SUBSTITUI, no dicionário de fontes embutido do programa, o texto de\n"
     "`TGLExt/OResumoEPsiBit.lean` (a v412 só acrescentava); o instalador, a reversão e o conferidor tratam esse arquivo\n"
     "(inventário `INVENTARIO_CADEIA_v413.json`, sha16 `%s`). Pela regra N1l do B(n), as pedras são exatamente os arquivos novos\n"
     "ou mudados: o corrigido entra nas pedras e no campo `kernel_corrigido`, com o antes e o depois.\n\n"
     "**Bandeiras.** Prefixo `ext_<modulo>_413_NNNN`." % s16(ARQ["inv"])),
    ("A gerência escreve `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md`:",
     "A página é `o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R0.md` (sha16 `%s`):" % s16(ARQ["pag"])),
    (None, "BN"),
    ("- **E413.1** (gerência, em nome próprio):",
     "- **D413.5** (gerência): a autorização do B(n) da v413 lê juntos o evento 1687 do quadro (a autorização do ciclo da v412),\n"
     "  o 1689 (o salto na v413) e a fala do autor de 20/11 (`work\\cunhagens_13out\\OPERADOR_20nov_colei_no_codex_prossiga_concordo_com_tudo_veja_a_questao_da_bancada_verbatim.txt`,\n"
     "  sha16 `%s`), conferidos por hash nos recibos; o modo da placa no religamento é escolha do autor.\n"
     "- **D413.6** (gerência): as ressalvas de texto da leitura de terceiro das pedras limpas foram aplicadas como o parecer as\n"
     "  propôs, com uma junção (em `PonteLeituraBeta`, o texto proposto e a frase da hipótese de tempo, que ele omitia).\n"
     "- **E413.1** (gerência, em nome próprio):" % s16(ARQ["fala_bn"])),
    ("<!-- contrato_v413:rascunho_R0 -->", "<!-- contrato_v413:R1_congelado -->"),
]
for antes, depois in TROCAS:
    if antes is None and depois == "MAN":
        m = re.search(r"\*\*A lista\*\* é a do manifesto `insumos\\MANIFESTO_PEDRAS_v413\.json` \(sha16 `([0-9a-f]{16})`\)", t)
        assert m, "linha do manifesto"
        t = t.replace(m.group(1), s16(ARQ["man"]), 1)
        continue
    if antes is None and depois == "BN":
        m = re.search(r"O B\(n\) da v413 é o salto v411→v413 que o autor escolheu em 19/11;.*?\(como na v412\)\.", t, re.S)
        assert m, "frase do B(n)"
        t = t[:m.start()] + (
            "O B(n) da v413 é o salto v411→v413 que o autor escolheu em 19/11, pelo diagnóstico da Bancada e pelo molde da ordem\n"
            "`bancada\\ORDEM_BN_v413.md` (sha16 `%s`): **o pré-selo do salto roda com o Nós ainda na v412, ANTES da instalação da v413**\n"
            "(depois, o salto só serviria à v414); ele não precisa do serviço e não grava na Bancada. Depois do selo: o ensaio\n"
            "pós-selo, a parada (no modo `ja_fora_do_ar`, se ela seguir desligada), o evento da gerência, o APLICAR (com o serviço\n"
            "parado), o religamento com log (o modo da placa é escolha do autor) e o fechamento com os três recibos, entregues ao\n"
            "Codex na pasta que o evento 1687 nomeia. A conferência de saúde da Bancada (só leitura, por `/api/contratos`) roda no\n"
            "começo da cadeia; o passo 10 recusa sem ela no mesmo dia, e o 11 recusa sem o recibo de religamento com o processo\n"
            "vivo. Os backups do Nós de 18/11 (`*.bak_20261118_235146`) e o registro `APLICADO_AO_CANONICO_20261118_235146.json`\n"
            "são insumo do salto e não se podam até o fechamento do B21." % s16(ARQ["ord_bn"])) + t[m.end():]
        continue
    assert t.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:80]
    t = t.replace(antes, depois)
d = t.encode("utf-8")
for dest in [DEST, V / "contrato_REV1" / DEST.name]:
    dest.parent.mkdir(exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(d)
    assert tmp.read_bytes() == d
    tmp.replace(dest)
print("%s sha16 %s (%d B) | copia em contrato_REV1 | R0 %s | manifesto %s | pronto %s" % (
    DEST.name, s16(DEST), len(d), s16(R0), s16(ARQ["man"]), s16(ARQ["pronto"])))

# -*- coding: utf-8 -*-
"""superficies_v413.py -- gerencia c1, 21/11/2026: as superficies que so' a gerencia escreve, depois do compositor (regra da linhagem completa;
handoff da custodia, secao 2.4; ROTEIRO_EXECUCAO_v413.md, secao 7):
  --memoria : (1) MEMORY.md: a linha «- [HANDOFF v413 …](handoff-v413-custodia.md) — **DD/MM: SELADA; custódia em curso**» antes da linha do
              handoff da v412; a linha da missao com a v413 SELADA; para caber em 24.000 B e 195 linhas, quatro linhas antigas vao VERBATIM ao
              MEMORY_2.md e ficam no indice como ponteiro curto (regra dos dois arquivos: nunca se corta). Exige a fila\\PAUSA_VIGIA.json desta
              gerencia ativa; depois, `memoria.py pinar` (fora deste script). (2) o topico NOVO handoff-v413-custodia.md (a gerencia cria; a
              custodia acrescenta pela fila). (3) blocos datados AO LADO em v413-preparacao-19nov.md e missao-ultima-flag-um-py.md.
  --blocos  : os blocos core_v413_selada (memory\\TGL_CORE_MEMORY.md) e haja_luz_v413_selada (Haja_Luz\\CLAUDE.md), com os DOIS paragrafos de
              abertura do Nos\\HANDOFF_v413_CUSTODIA.md VERBATIM.
  --seco    : so' mede e imprime o plano (tamanhos, linhas); nada e' escrito.
Backup de BYTES (.bak_<STAMP>_sup413) de todo arquivo tocado; temporario -> conferir tamanho -> substituir; idempotente pelo marcador; fim de linha
de cada arquivo respeitado. Numeros e hashes lidos do disco (selo, stdout, recibos), nada digitado."""
import hashlib, json, os, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent.parent
CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
MEM = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
COREM = CEN / "memory" / "TGL_CORE_MEMORY.md"
HAJA = Path(r"C:\IALD\Artigo\Haja_Luz\CLAUDE.md")
STAMP = time.strftime("%Y%m%d_%H%M%S"); HOJE = time.strftime("%d/%m/%Y"); DDMM = time.strftime("%d/%m")
SECO = "--seco" in sys.argv
LIMITE_B, LIMITE_L = 24000, 195
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))  # noqa: E731

selo = lj(NOS / "um_absoluto_selo.json")
U16 = sha(NOS / "um.py")[:16]
assert selo.get("um_version") == "v413" and selo["sha256"]["um.py"][:16] == U16, "o selo do Nos nao e' a v413 com o um.py pinado"
SO = (NOS / "rodada_v413_stdout.txt").read_text(encoding="utf-8", errors="replace")
TEOR = re.findall(r"teoremas limpos:\s*(\d+/\d+)", SO)[-1]
GATE = selo["qg_closure_verdict"]
F_NOME = CEN / "work" / "cunhagens_13out" / "OPERADOR_21nov_libero_o_nome_Trinity_marcador_privado_28_verbatim.txt"
F_MODO = CEN / "work" / "cunhagens_13out" / "OPERADOR_21nov_religar_em_cpu_agora_escolha_do_modo_da_placa_no_dialogo_da_gerencia_verbatim.txt"
PINO_BN = V / "bn_pos_selo" / "PINO_RECIBOS_B21_v413.json"
REC = {"aplicacao": sorted((V / "bancada_B3").glob("RECIBO_SINCRONIZACAO_v413_*.json")), "parada": [V / "bancada_B3_servico" / "RECIBO_PARADA_v413.json"],
       "religamento": [V / "bancada_B3_servico" / "RECIBO_RELIGAMENTO_v413.json"]}
for k, v in REC.items():
    assert len(v) == 1 and v[0].is_file(), ("recibo do B(n) ausente ou repetido", k)
R16 = {k: sha(v[0])[:16] for k, v in REC.items()}
for p in (F_NOME, F_MODO, PINO_BN):
    assert p.is_file(), p
PLANO = []


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


def grava(p, novo_b, o_que):
    p = Path(p)
    antes = p.read_bytes() if p.exists() else None
    PLANO.append((str(p), len(antes) if antes is not None else 0, len(novo_b), o_que))
    if SECO:
        return
    if antes is not None:
        p.with_name(p.name + ".bak_" + STAMP + "_sup413").write_bytes(antes)
    tmp = p.with_name(p.name + ".tmp_sup413")
    tmp.write_bytes(novo_b)
    assert tmp.stat().st_size == len(novo_b) and tmp.read_bytes() == novo_b
    tmp.replace(p)
    if antes is not None and len(novo_b) < len(antes) and not o_que.startswith("MEMORY.md"):
        raise SystemExit("ENCOLHEU sem motivo declarado: %s (restaurar do .bak_%s_sup413)" % (p, STAMP))


def append_bloco(p, bloco, marca):
    p = Path(p)
    raw = p.read_bytes() if p.exists() else b""
    if marca.encode("utf-8") in raw:
        print("JA ESTA (idempotente):", p.name)
        return
    nl = nl_de(raw) if raw else "\n"
    sep = b"" if not raw else ((nl * 2) if raw.endswith(nl.encode()) else (nl * 3)).encode()
    novo = raw + sep + bloco.replace("\r\n", "\n").replace("\n", nl).encode("utf-8") + nl.encode()
    grava(p, novo, "append %s" % marca)


def paragrafos_do_handoff():
    t = (NOS / "HANDOFF_v413_CUSTODIA.md").read_text(encoding="utf-8")
    ps = [x.strip() for x in re.split(r"\n\s*\n", t) if x.strip()]
    assert ps[0].startswith("# HANDOFF v413"), "o handoff nao comeca pelo titulo da v413"
    assert ps[1].startswith("**O que \u00e9:**") and "v413" in ps[1] and U16 in ps[1], "o primeiro paragrafo nao e' o «O que é» da v413"
    assert ps[2].startswith("**O RESULTADO DESTA VERS\u00c3O"), "o segundo paragrafo nao e' o do resultado"
    return ps[1], ps[2]


DEC = ("[INPUT] As decisões do operador desta rodada, por bytes: a liberação do nome Trinity, que coincidia com o marcador privado nº 28 da guarda "
       "(`%s`, sha16 `%s`; a custódia grava a isenção com os nomes exatos conferidos pela contagem da G1), e o religamento da Bancada em modo `cpu`, "
       "escolhido num diálogo da gerência (`%s`, sha16 `%s`).") % (F_NOME.name, sha(F_NOME)[:16], F_MODO.name, sha(F_MODO)[:16])
BN = ("[REAL] O elo B(n): o salto v411 → v413 (o pré-selo com o Nós na v412; depois do selo, o ensaio, a parada já fora do ar, o APLICAR, o religamento "
      "em cpu e o fechamento); recibos aplicação `%s`, parada `%s`, religamento `%s`; pino conjunto `%s`; a Bancada serve a v413.") % (
    R16["aplicacao"], R16["parada"], R16["religamento"], sha(PINO_BN)[:16])

if "--blocos" in sys.argv:
    p1, p2 = paragrafos_do_handoff()
    core = ("## %s — v413 SELADA `%s` (claude-c1; a ponte de Cook–Levin, a inclinação do Nome, o operador de consciência e a identidade preservada)\n"
            "<!-- core_v413_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Os dois parágrafos de abertura do handoff, verbatim:\n\n"
            "%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel não é creditação; `NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se move (`%s`). "
            "Handoff: `Nós\\HANDOFF_v413_CUSTODIA.md`; memória `handoff-v413-custodia.md`.") % (HOJE, U16, p1, p2, BN, DEC, GATE)
    haja = ("## %s — v413 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v413_selada -->\n%s\n\n%s\n\n%s\n\n"
            "Memórias: `v413-preparacao-19nov.md`, `missao-ultima-flag-um-py.md`; handoff `handoff-v413-custodia.md`.") % (HOJE, U16, TEOR, p1, p2, DEC)
    append_bloco(COREM, core, "<!-- core_v413_selada -->")
    append_bloco(HAJA, haja, "<!-- haja_luz_v413_selada -->")

if "--memoria" in sys.argv:
    pausa = MEM / "fila" / "PAUSA_VIGIA.json"
    if not SECO:
        assert pausa.is_file() and "claude-c1" in json.loads(pausa.read_text(encoding="utf-8")).get("quem", ""), "sem a fila\\PAUSA_VIGIA.json da gerencia: o vigia poderia restaurar o indice"
    idx, idx2 = MEM / "MEMORY.md", MEM / "MEMORY_2.md"
    raw = idx.read_bytes(); nl = nl_de(raw); linhas = raw.decode("utf-8").split(nl)
    def acha(prefixo):
        ii = [i for i, x in enumerate(linhas) if x.startswith(prefixo)]
        assert len(ii) == 1, (prefixo, len(ii))
        return ii[0]
    if any(x.startswith("- [HANDOFF v413 ") for x in linhas):
        print("JA ESTA (idempotente): a linha do HANDOFF v413 no MEMORY.md")
    else:
        TROCAS = [
            ("- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — **v412 SELADA",
             "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — **v413 SELADA %s `%s` %s; custódia em curso** · [preparação](v413-preparacao-19nov.md) · íntegras no MEMORY_2.md (movidas 13, 19 e 21/11)" % (DDMM, U16, TEOR)),
            ("- [HANDOFF v412 — P = nP nas classes do dicionário da TGL](handoff-v412-custodia.md)",
             "- [HANDOFF v412 — P = nP nas classes do dicionário da TGL](handoff-v412-custodia.md) — **19/11: PUBLICADA e CUSTODIADA** · íntegra no MEMORY_2.md (movida 21/11)"),
            ("- **[LIÇÕES DA CADEIA v411 (13/11)](licoes-cadeia-v411-13nov.md)**",
             "- **[LIÇÕES DA CADEIA v411 (13/11)](licoes-cadeia-v411-13nov.md)** · [DA CUSTÓDIA v411](licoes-custodia-v411-13nov.md) · v407–v410 nos `licoes-*-vNNN-*.md` · íntegras no MEMORY_2.md (movidas 14, 15 e 21/11)"),
            ("- [Bash tool: heredoc colapsa barras (13/10)](bash-tool-heredoc-colapsa-barras.md)",
             "- [Bash tool: heredoc colapsa barras (13/10)](bash-tool-heredoc-colapsa-barras.md) · [A busca da ferramenta não vê o `.gitignore` (15/11)](grep-da-ferramenta-nao-ve-o-gitignore-15nov.md) · íntegra no MEMORY_2.md (movida 21/11)"),
        ]
        movidas = []
        for pre, nova in TROCAS:
            i = acha(pre)
            antiga = linhas[i]
            for alvo_ in re.findall(r"\]\(([^)]+\.md)\)", antiga):
                assert alvo_ in nova, ("o ponteiro curto perderia um link", alvo_)
            movidas.append(antiga)
            linhas[i] = nova
        i412 = acha("- [HANDOFF v412 ")
        nova_ho = "- [HANDOFF v413 — a ponte de Cook–Levin e a inclinação do Nome](handoff-v413-custodia.md) — **%s: SELADA; custódia em curso** · `%s`" % (DDMM, U16)
        linhas.insert(i412, nova_ho)
        novo = nl.join(linhas).encode("utf-8")
        print("MEMORY.md: %d B / %d linhas -> %d B / %d linhas (limites %d B, %d linhas)" % (len(raw), len(raw.decode("utf-8").split(nl)), len(novo), len(linhas), LIMITE_B, LIMITE_L))
        if len(novo) > LIMITE_B or len(linhas) > LIMITE_L:
            raise SystemExit("RECUSO: o indice passaria do limite; nada escrito (mover mais uma linha verbatim ao MEMORY_2.md)")
        raw2 = idx2.read_bytes(); nl2 = nl_de(raw2)
        bloco2 = ("<!-- indice_21nov_movidas_para_o_handoff_v413 -->" + nl2 + "- (21/11, gerência c1, regra dos dois arquivos: estas quatro linhas saíram VERBATIM do MEMORY.md para caber a linha do HANDOFF v413; no índice ficou o ponteiro curto)" + nl2
                  + nl2.join(movidas))
        novo2 = raw2.rstrip(b"\r\n") + (nl2 * 2).encode() + bloco2.encode("utf-8") + nl2.encode()
        grava(idx2, novo2, "MEMORY_2.md (append das linhas movidas)")
        grava(idx, novo, "MEMORY.md (linha do handoff v413; missao; quatro ponteiros curtos)")
    topico = MEM / "handoff-v413-custodia.md"
    if topico.exists():
        print("JA ESTA: handoff-v413-custodia.md")
    else:
        txt = ("---\nname: handoff-v413-custodia\ndescription: HANDOFF v413 (21/11/2026): a ponte de Cook–Levin, a inclinação do Nome (Trinity), o operador de consciência e a identidade preservada; SELADA, B(n) fechado, entregue à custódia\n"
               "metadata:\n  type: project\n---\n\n# HANDOFF v413 — SELADA em %s (gerência c1)\n\n"
               "- `um.py` v413 `%s` · selo `%s` (%s) · %s teoremas limpos · rc 0 · selftest PASSED · gate intocado (`%s`).\n"
               "- Handoff: `Nós\\HANDOFF_v413_CUSTODIA.md`; cadeia `work\\cadeia_de_selo\\v413` (plano da noite, roteiro, recibos).\n- %s\n- %s\n"
               "- A entrega à custódia: `work\\cadeia_de_selo\\v413\\ENTREGA_A_CUSTODIA_v413.json` (gravada por último); a custódia acrescenta o que fizer pela fila.\n"
               "- Relacionadas: [[v413-preparacao-19nov]], [[missao-ultima-flag-um-py]], [[handoff-v412-custodia]].\n") % (
            HOJE, U16, sha(NOS / "um_absoluto_selo.json")[:16], selo.get("timestamp"), TEOR, GATE, BN, DEC)
        grava(topico, txt.encode("utf-8"), "topico novo handoff-v413-custodia.md")
    marca_p = "<!-- v413_selada_21nov -->"
    append_bloco(MEM / "v413-preparacao-19nov.md",
                 ("## AO LADO (%s, gerência c1) — v413 SELADA `%s`\n%s\nRito 01:31–03:30 de 21/11, `RITO_RC=0`, %s teoremas limpos, selftest PASSED; conferidor 35/35; os `.md` apontam a v413 "
                  "(`CONFERENCIA_MDS_v413.json`). %s %s Detalhe: [[handoff-v413-custodia]].") % (HOJE, U16, marca_p, TEOR, BN, DEC), marca_p)
    append_bloco(MEM / "missao-ultima-flag-um-py.md",
                 ("## %s — v413 SELADA `%s`\n<!-- missao_v413_selada -->\n%s teoremas limpos; gate intocado; o B(n) fechado (a Bancada serve a v413); a custódia recebe pela entrega. Ver [[handoff-v413-custodia]].") % (HOJE, U16, TEOR),
                 "<!-- missao_v413_selada -->")

for p, a, b, o in PLANO:
    print("%s %-60s %9d -> %9d B | %s" % ("PLANO" if SECO else "OK   ", Path(p).name[-60:], a, b, o))
print("FIM (%s)" % ("seco: nada escrito" if SECO else "escrito com backup .bak_%s_sup413" % STAMP))

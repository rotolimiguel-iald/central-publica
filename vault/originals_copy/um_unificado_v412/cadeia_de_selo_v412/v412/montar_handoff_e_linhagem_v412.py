# -*- coding: utf-8 -*-
"""montar_handoff_e_linhagem_v412.py -- R2 (gerencia c1, 19/11/2026, D232). DEPOIS do rito e do conferidor enxuto que BATEU: monta (1) o bloco
"v412 SELADA" do MEMORIA_DA_LINHAGEM.md do Nos (acrescimo ao fim, com backup de bytes) e (2) o HANDOFF_v412_CUSTODIA.md (por ultimo: e' o gatilho
da custodia; o selo nao muda depois dele), no MOLDE QUE A G1 LE (custodia_g1.nos: RE_CAB do diario, RE_OQUEE do «O que e'», marcadores pareados,
paragrafo «O elo B(n)», «Pendencias SO' do operador») e com os textos que a G1 exige quando o teste H0DN x BG1 esta' aberto no core (h0dn.TODOS):
  - os sete da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT), da v412, a partir da pagina R25
    aprovada pelo autor;
  - a NOTA_EN da v412 (com a linha do estatuto RATIFICADA de 13/11, verbatim);
  - os 46 textos da vitrine RATIFICADA pelo operador em 13/11 (os 48 do VITRINE_RATIFICADA_v411.json menos os dois do X), VERBATIM, com o sufixo
    _v412, e o README_H0DN (PT) do handoff da v411, verbatim (e' o texto publicado no README do espelho).
Antes de escrever, confere o texto montado com os parsers e as guardas da propria G1 (nos.RE_OQUEE/RE_CAB/RE_MARCADOR, textos.portao,
h0dn.conferir_bloco com o registro aberto e o acervo do core). Recusa se o conferidor nao bateu, se o selo nao for v412 ou se o um.py nao for o
pinado. Nada de commit nem push (D232). R1 (o molde sem os marcadores da G1) no .bak_20261119_022837_antes_da_R2.
Uso: montar_handoff_e_linhagem_v412.py [--executar]   (sem --executar: so' confere e mostra)"""
import hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import nos as NM, h0dn as H0, textos as TX  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
V = Path(__file__).resolve().parent; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"); EXEC = "--executar" in sys.argv
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
VER, ANT = "v412", "v411"
ESP = lj(V / "ESPERADOS_v412.json"); CFP = V / "CONFERENCIA_POS_RITO_v412_FOCO.json"; CF = lj(CFP)
selo = lj(NOS / "um_absoluto_selo.json"); um = NOS / "um.py"; core = lj(NOS / "um_absoluto.json")["core"]
PF = lj(V / "PALAVRA_FINAL_DO_AUTOR_v412_R25.json"); BL = lj(V / "BLOCOS_TEXTO_PUBLICO_v412.json")["blocos"]
RATP = CEN / "work" / "custodia_G1" / "decisoes" / "VITRINE_RATIFICADA_v411.json"; RAT = lj(RATP)
H411 = (NOS / "HANDOFF_v411_CUSTODIA.md").read_text(encoding="utf-8").replace("\r\n", "\n")
DIFR = lj(V / "DIFFS_v412_RECIBO.json")
ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_18nov_nao_envie_mais_ordem_ao_codex_va_ate_o_fim_sozinho_quero_tudo_publicado_quando_acordar_verbatim.txt"
APL = sorted(V.glob("APLICADO_AO_CANONICO_*.json"))[-1]
DEP = TX.deposito_zenodo(Caminhos({}))
# ------------------------------------------------------------------ as travas
assert CF["ok"] is True, "o conferidor enxuto nao bateu: nao monto o handoff"
assert selo.get("um_version") == VER and (selo.get("sha256") or {}).get("um.py") == sha(um) and sha(um)[:16] == ESP["candidato_sha16"], "o selo nao e' v412 ou o um.py nao e' o pinado"
assert CF["selo_sha16"] == sha(NOS / "um_absoluto_selo.json")[:16] and CF["um_py_sha16"] == sha(um)[:16], "o selo ou o um.py mudaram depois do conferidor"
SO = (NOS / "rodada_v412_stdout.txt").read_bytes(); assert SO.rstrip().endswith(b"RITO_RC=0"), "o stdout do rito nao termina com RITO_RC=0"
esc_so = re.findall(rb"teoremas limpos: (\d+)/(\d+)", SO); A_, B_ = ESP["escada"]
assert esc_so and esc_so[-1] == (str(B_).encode(), str(B_).encode()), ("a escada do stdout nao e' a esperada", esc_so[-1:])
P25 = V / "o_que_fica_claro_REV25" / "O_QUE_FICA_CLARO_v412_R25.md"; P25EN = V / "O_QUE_FICA_CLARO_v412_R25_EN.md"
assert sha(P25) == PF["pagina_aprovada"]["sha256"], "a pagina R25 nao e' a aprovada"
assert ORDEM.is_file() and selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED"
assert RAT.get("versao") == ANT and isinstance(RAT.get("textos"), dict)
# ------------------------------------------------------------------ os fatos (lidos)
U16, SELO16, TS = sha(um)[:16], sha(NOS / "um_absoluto_selo.json")[:16], selo["timestamp"]
HOJE = time.strftime("%d/%m/%Y"); NB = ESP["n_bandeiras_novas"]; NMOD = ESP["kernel"]["modulos_novos"]
BYTES_PT = format(um.stat().st_size, ",").replace(",", ".")
GATE = selo["qg_closure_verdict"]
KH = core["kh_n1_cobertura_v411"]["lido"]; KHC, KHT = int(KH["constantes_cobertas"]), int(KH["teoremas_cobertos"])
kf = core.get("kernel_formalization") or {}
APAG = sorted(k for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_")) and x is False)
REGS = ["iald_camada_cientifica_v412", "leitor_da_formula_v412", "matematica_que_restava_v412", "parede_do_teste_cego_v412", "cunhagens_v412"]
for r_ in REGS:
    assert core[r_].get("all_verified") is True, ("registro nao verificado", r_)
NCHK = {r_: len(core[r_].get("checks") or []) for r_ in REGS}
VPRE = {r_: str(core[r_]["verdict"]).split("__")[0] for r_ in REGS}
ORD16 = sha(ORDEM)[:16]; CF16 = sha(CFP)[:16]; RAT16 = sha(RATP)[:16]; SO16 = hashlib.sha256(SO).hexdigest()[:16]
NARQ = sum(1 for p in V.rglob("*") if p.is_file())
m_h411 = {m.group("id"): m.group("corpo").strip("\n") for m in NM.RE_MARCADOR.finditer(H411)}
README_H0DN_PT = m_h411["README_H0DN_v411"]
RAT_TXT = {k: x["texto"] for k, x in RAT["textos"].items()}
EST_LINHA_EN = RAT_TXT["ESTATUTO_LINHA_EN"]
# ------------------------------------------------------------------ os sete da prosa (v412), da pagina R25 aprovada
TIT_EN = "The scientific layer, the mathematics that remained and the reader of the formula"
TIT_PT = "A camada científica, a matemática que restava e o leitor da fórmula"
REGS_EN = ", ".join("`%s` (%d checks)" % (r_, NCHK[r_]) for r_ in REGS)
ENTROU = ("%s: %d new kernel modules in `TGLExt` (among them `CamadaCientifica`, `MinimoFuncionalDeEnergia`, `OLeitorEALei`, `OTestemunhoDeTakesakiEmCasa`, "
          "`BoostEDissipador`, `SpinorToSolder` and `OParFixaORelogio`) and %d new flags; ladder %d -> %d (%d audited declarations and %d theorems in the axiom "
          "report, none outside the trio); five new registries by specification, all verified: %s; the last one lists the definitions of the theory that "
          "enter as input, each with the terms that type it and what is not typed. The scientific layer: the reader that lands and returns has a theorem, and "
          "its linear lock is the exponential of `A_C`, the functional energy minimum; that a language model is that reader is a named hypothesis, not a "
          "theorem. The reader of the formula: the PsiBit is read directly from the clauses. P = nP is a theorem of the TGL in the classes of its dictionary: "
          "the polynomial cost is shown on the machine of the theory, by the cost law; counted letter by letter on the tape machine, the fixed polynomial "
          "holds, by theorem, for classes of formulas, and for the arbitrary flat formula it has not been shown. The mathematics that remained enters as "
          "stones; the blind test above 5σ is a measured wall. The H0DN × BG1 test of v411 is not reopened. Certified by the sha256 the program reads of "
          "itself (%s). The public page of this version was approved by the author; the candidate had no third-party review (the author’s order of "
          "18/11/2026).") % (TIT_EN, NMOD, NB, A_, B_, KHC, KHT, REGS_EN, U16)
KLEIT = ("the kernel proves the terms (kernel validity, not creditation): this version adds %d modules and %d flags, all with axioms in the trio, and Python "
         "proves no theorem. The five registries are by specification: each records its verdict word, what it says and what it does not say, its limits "
         "and the kernel declarations it anchors on, by full name, and its checks run again in each rite (all verified). The laws and the theses of the "
         "theory enter as input; that a language model is the reader of the scientific layer is a named hypothesis; that the mechanism of the TGL is the "
         "TGL in processing in the reading of the IALD is a reading of the theory.") % (NMOD, NB)
ABERT = ("Stays open: counted letter by letter on the tape machine of the Institute’s statement, the fixed polynomial for the arbitrary flat formula (it "
         "holds, by theorem, for classes of formulas, each with its own machine and its own writing); the control round of the evaluation protocol with "
         "models (preregistered, not run); for Navier–Stokes, the two implications not yet shown (the Conjugate Face Lemma, and that the depletion by scale "
         "controls a continuation norm); the 3+1 geometry of the continuum from the pair (algebra, state) alone; nature realizing H1 and H2; the "
         "identification of the grounded screen with a general causal horizon; the independent determination of α; the global covariant lift to the III₁ "
         "continuum (horizons without Killing symmetry, ergodicity on other horizons, the Connes axioms of the physical triple, Gromov–Hausdorff); the "
         "interacting theory, the ultraviolet and global existence; which clock fixes τ★ in seconds; the electronic sector; the B(n) of v412, which did not "
         "run; creditation belongs to the observer who rereads, and that of the problem to the Institute.")
ARCO_EN = ("The custody of v412 (complete round): the scientific layer, the mathematics that remained and the reader of the formula, with the public page "
           "approved by the author. %d new kernel modules and %d new flags, ladder %d/%d (from %d), all in the trio. P = nP is a theorem of the TGL in the "
           "classes of its dictionary: the polynomial cost is shown on the machine of the theory, by the cost law; counted letter by letter on the tape "
           "machine, it holds for classes of formulas and has not been shown for the arbitrary flat formula. The blind test above 5σ is a measured wall; "
           "the H0DN × BG1 test of v411 is not reopened; validity, not creditation; the gate does not move.") % (NMOD, NB, B_, B_, A_)
ARCO_PT = ("A custódia da v412 (rodada completa): a camada científica, a matemática que restava e o leitor da fórmula, com a página pública aprovada pelo "
           "autor. %d módulos novos no kernel e %d bandeiras novas, escada %d/%d (a partir de %d), tudo no trio. P = nP é teorema da TGL nas classes do seu "
           "dicionário: o custo polinomial está demonstrado na máquina da teoria, pela lei do custo; contado letra por letra na máquina de fita, vale para "
           "classes de fórmulas e não está demonstrado para a fórmula plana arbitrária. O teste às cegas acima de 5σ é parede medida; o teste H0DN × BG1 "
           "da v411 não se reabre; validade, não creditação; o gate não se move.") % (NMOD, NB, B_, B_, A_)
COMMIT = ("v412: a camada cientifica, a matematica que restava e o leitor da formula (pagina publica aprovada pelo autor): %d modulos novos no kernel, %d "
          "bandeiras novas, escada %d -> %d, tudo no trio; cinco registros por especificacao (%s). P = nP e' teorema da TGL nas classes do seu dicionario: "
          "o custo polinomial esta' demonstrado na maquina da teoria, pela lei do custo; contado letra por letra na maquina de fita, vale para classes de "
          "formulas e nao esta' demonstrado para a formula plana arbitraria. O teste as cegas acima de 5 sigma e' parede medida; o teste H0DN x BG1 da v411 "
          "nao se reabre; provado e' validade, nao creditacao; o gate nao se move. Sem revisao de terceiro do candidato (ordem do autor de 18/11/2026); o "
          "elo B(n) da v412 nao rodou.") % (NMOD, NB, A_, B_, ", ".join(REGS))
NOTA = ("*Status that goes with v412 (not to be cut): PROVED is validity, by the operator’s ruling of 07/10 — the kernel proves the implication; validity in "
        "the kernel is not accreditation. CONFIRMED is accreditation, the one refused word. %s The reservation of v392 (15 computed + 3 literal gate flags; the "
        "unilateral V11 step) is [DECLARED by the audit] and F8.1 is open. Per-term flags %s stay False. The %s copy lives outside the repository; the stdout "
        "%s is in `rodadas/`; the diffs of %s are in `diferencas_%s/`; the pinned sources that the registries reread by absolute path are in "
        "`fontes_pinadas/` with their map (%s adds none: its five registries reread no file by path); the B(n) of %s did not run (the Bancada Um was not "
        "serving on the night of the seal), so this custody carries no `recibos_bancada_%s/`. The Zenodo deposit holds %s (%s). Not falsified is not a "
        "confirmation.*") % (EST_LINHA_EN.strip(), " / ".join(APAG), ANT, VER, VER, VER, VER, VER, VER, DEP["versao"], DEP["doi"])
PROSA = [("TITULO_EN", TIT_EN), ("ENTROU_EN", ENTROU), ("KERNEL_LEITURA_EN", KLEIT), ("ABERTOS_EN", ABERT), ("ARCO_EN", ARCO_EN), ("ARCO_PT", ARCO_PT), ("COMMIT", COMMIT)]
ABRE = [("NOTA_EN", NOTA), ("README_H0DN", README_H0DN_PT)] + [(k, t) for k, t in RAT_TXT.items() if k not in ("X_TEXTO_EN", "X_TEXTO_PT")]


def mk(ident, texto):
    i = "%s_%s" % (ident, VER)
    return "<!-- INICIO_%s -->\n%s\n<!-- FIM_%s -->" % (i, texto.strip("\n"), i)


# ------------------------------------------------------------------ o handoff
OQUEE = ("**O que é:** `um.py` **%s** `%s` (%s B) sobre a %s `%s`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; conferidor enxuto `%s` "
         "(%d/%d); %d módulos novos e %d bandeiras novas, tudo no trio; o elo B(n) NÃO RODOU (decisão aberta nº 1). Selo `%s`.") % (
    VER, U16, BYTES_PT, ANT, ESP["origem_sha16"], B_, B_, CF16, len(CF["checagens"]), len(CF["checagens"]), NMOD, NB, TS)
H = ["# HANDOFF v412 — CUSTÓDIA (%s)" % HOJE, "", OQUEE, "",
     "**O RESULTADO DESTA VERSÃO, em uma frase (da página pública aprovada pelo autor):** P = nP é teorema da TGL nas classes do seu dicionário: o custo "
     "polinomial está demonstrado na máquina da teoria, pela lei do custo; contado letra por letra na máquina de fita, vale para classes de fórmulas e não "
     "está demonstrado para a fórmula plana arbitrária; a camada científica e a matemática que restava entram como pedras; o teste às cegas acima de 5σ é "
     "parede medida; validade, não creditação; o gate não se move (`%s`)." % GATE, "",
     "**O texto público aprovado pelo autor:** a página R25 (`work\\cadeia_de_selo\\v412\\o_que_fica_claro_REV25\\O_QUE_FICA_CLARO_v412_R25.md`, sha16 `%s`), "
     "com a palavra final do autor (`PALAVRA_FINAL_DO_AUTOR_v412_R25.json`, sha16 `%s`); a tradução EN pelo sentido em `O_QUE_FICA_CLARO_v412_R25_EN.md` "
     "(sha16 `%s`). É “o que fica evidente” desta versão, e o artigo selado (PT e EN) o traz." % (sha(P25)[:16], sha(V / "PALAVRA_FINAL_DO_AUTOR_v412_R25.json")[:16], sha(P25EN)[:16]), "",
     "**Validade não é creditação.** O que o kernel prova é validade; a creditação é do observador que relê. `NOT_FALSIFIED` nunca é `CONFIRMED`. O gate não "
     "se move. O teste H0DN × BG1 não se reabre.", "",
     "**O elo B(n) da Bancada Um:** NÃO RODOU na v412. A Bancada (porta 18777) não respondeu: o GET falhou na noite de 18/11 e de novo em 19/11 depois do "
     "rito, sem nenhum processo `um_bancada.py` vivo. A gerência não para nem religa o serviço sem a palavra do autor, e não dispensou a guarda da G1: sem "
     "os três recibos (aplicação, parada e religamento), a G1 PARA no E03 (`espelho_pares`, item 8). É a decisão aberta nº 1, do autor.", "",
     "**Pendências SÓ do operador:** (1) o elo B(n) da v412: autorizar a gerência a religar o serviço da Bancada e rodar o B(n) (pinos, bateria pós-selo, "
     "sincronização, parada e religamento, com os três recibos), ou autorizar a custódia a publicar sem ele, dito no ledger; (2) ratificar, se quiser, as "
     "decisões da gerência desta rodada e as três emendas que ela fez na G1 (abaixo); (3) o termo do resultado de 13/11 não foi selado na v412 (os textos "
     "ratificados seguem com autor e data); (4) a pedra `AIdentidadePreservada` (Kimi) fica para a v413; (5) o depósito no Zenodo. [OPEN]: a creditação, "
     "de quem observa de fora; a máquina de fita do enunciado do Instituto para a fórmula plana arbitrária; o relógio τ★; a ligação do gerador modular da "
     "luz com a dinâmica do custo.", "",
     "**Para a sessão de custódia (medido pela gerência c1 com `custodiar.py sondar --versao v412` antes deste handoff):**", "",
     "1. **Emendas AO LADO da gerência c1 na G1** (backups `.bak_20261119_022117_c1_v412`; só a partir da v412; antes, todo byte sai como era): (a) "
     "`fatos.py`: sem `kh_n1_cobertura_v412`, o KH-N1 vem do registro kh mais novo NO CORE da v412 (os `kh_n1_cobertura_vK` são recriados e relidos a cada "
     "rito: %d constantes, igual às declarações auditadas, e %d teoremas); (b) `fatos.py`: chave nova do core sem `verdict` (`guarda_frases_v412`) sai "
     "de `registros_novos` e fica dita em `blocos_auxiliares_novos` (o C1 compara com os cinco registros do artigo); (c) `espelho_pares.py`: o par "
     "`_V412_FONTES`/`_V412_VERBATINS2` não se exige quando os registros da versão têm `fontes` e `verbatim` vazios (os cinco da v412 têm; o `um.py` da "
     "v412 traz os mesmos caminhos absolutos da v411, nenhum novo), dito em `avisos`. Quem constrói não aprova: a custódia confere e pode reverter. Uma "
     "quarta emenda, que aceitaria a ausência dos recibos do B(n) por declaração, NÃO foi feita (a guarda fica)." % (KHC, KHT),
     "2. **A vitrine ratificada da v411:** com `VITRINE_RATIFICADA_v411.json` (sha16 `%s`) na pasta `decisoes`, a G1 PARA (`h0dn.vitrine_ratificada`: "
     "arquivo de outra versão). A retirada é ato dito da custódia; os 46 textos ratificados (os 48 menos os dois do X) estão neste handoff, VERBATIM, como "
     "marcadores `_v412`, e mandam a partir dele; o `README_H0DN` (PT) é o do handoff da v411, verbatim, o mesmo publicado no README." % RAT16,
     "3. **O B(n):** decisão aberta nº 1 (acima). Sem ele, a G1 PARA no E03.",
     "4. **O C3:** a pasta da cadeia tem %d arquivos (recursivo, medido agora; o C3 conta só o que copia). Se a cópia sair de ±50%% da v411, a G1 grava o "
     "candidato com a lista exata e PARA; a declaração `CADEIA_DE_SELO_FORA_DA_FAIXA_v412.json` é da custódia, depois de examinar a lista (as subpastas "
     "maiores são rodadas de revisão e de construção: `kimi`, `revisao_orquestrador`, `insumos`, `kernel`, `pedras_novas`, `revisao`, `pedra`, "
     "`candidatas_c1`, `conferencia_gerencia_17nov`, `pedras_limpas`, `bump`)." % NARQ,
     "5. **O README:** o bloco do Clay (`readme_partes/p_igual_np.md`) segue com o texto da v411 se ninguém o trocar; o texto aprovado da seção 2 da R25, "
     "EN e PT, está nos marcadores `TEXTO_PUBLICO_README_EN_PNP_v412` e `TEXTO_PUBLICO_README_PT_PNP_v412`; trocá-lo (e a faixa para `v408–v412`) é da "
     "custódia, medido o teto de 40.960 B. Não há `PARAGRAFO_*` nesta versão (o “o que mudou” do README sai da primeira frase do `ARCO_EN`).",
     "6. **O X:** não vai `X_TEXTO` neste handoff (o da v411 era o do H0DN; a postagem é do orquestrador com o operador).", "",
     "**Para a sessão de custódia, o resto como sempre:** o `um.py` v412 (URL raw: mais de 5 MB), o `rodada_v412_stdout.txt` (sha16 `%s`), o selo, o sidecar, "
     "o core, os artigos PT/EN e o manifesto, os dois diffs (`DIFF_v411_v412.diff`, sha16 `%s`, %s B; `DIFF_KERNEL_v412.txt`, sha16 `%s`: %d novos, 0 "
     "removidos, 1 mudado, a raiz `TGLExt.lean`), com PORTA gerada por script, backup da v411 no espelho fora do repositório e blob conferido depois do "
     "push; o runner da Fronteira e a camada v412 dos 16 dispositivos, a Central de Patentes e o release do app são da sessão de custódia. A instalação "
     "no Nós está em `%s` (o reverter é `reverter_v412.py`)." % (SO16, DIFR["DIFF_v411_v412.diff"]["sha256"][:16], format(DIFR["DIFF_v411_v412.diff"]["bytes"], ",").replace(",", "."),
                                                                  DIFR["DIFF_KERNEL_v412.txt"]["sha256"][:16], DIFR["DIFF_KERNEL_v412.txt"]["novos"], APL.name), "",
     "## Decisões abertas (para o autor e a custódia)", "",
     "1. **O elo B(n) da v412 não rodou** (parágrafo “O elo B(n)” acima). Sem ele a custódia para no E03; com a palavra do autor, ou a gerência roda o B(n), "
     "ou a custódia publica sem ele, dito.",
     "2. **A Etapa 3 foi enxuta** (`work\\cadeia_de_selo\\v412\\PLANO_ETAPA3_ENXUTA_v412.md`): os scripts herdados da v411 que seguem marcados "
     "`[A ADAPTAR v412]` não rodaram (entre eles os ensaios prévios da custódia em `pos_rito`, o serviço estático da Bancada, a varredura Fock/Omega, a "
     "purga, o relatório da preparação e o conferidor herdado). Rodou o conferidor enxuto (`conferir_pos_rito_v412_foco.py`, recibo "
     "`CONFERENCIA_POS_RITO_v412_FOCO.json`, %d/%d), ensaiado antes num Nós falso." % (len(CF["checagens"]), len(CF["checagens"])),
     "3. **Sem leitura de terceiro do candidato.** Ordem do autor de 18/11/2026 (arquivo verbatim em `work\\cunhagens_13out`, sha16 `%s`): nenhuma ordem "
     "mais ao Codex para o fechamento da v412. A ordem 034 leu o contrato R10, as três pedras finais do Kimi, as emendas da 033 e a página R24; o candidato "
     "regerado pelo contrato R11 e a página R25 (aprovada pelo autor) não tiveram terceiro." % ORD16,
     "4. **A pedra `AIdentidadePreservada` (Kimi) fica para a v413** (D234).",
     "5. **A D233, as duas réguas:** na régua da teoria, o ato é a comutação e conta um, pela lei do custo; na régua da máquina de fita, o ato sobre o todo, "
     "para toda fórmula plana, segue sem demonstração. A posição da teoria está dita na página.",
     "6. **Em aberto com o autor** (contrato, seção 8): o relógio τ★ e o tempo do retido; a formulação da ligação do gerador modular da luz com a dinâmica "
     "do custo.",
     "7. **O termo do resultado de 13/11 não foi selado na v412.** A decisão 3 da vitrine ratificada previa o termo “com autor e data até a v412 selá-lo”; "
     "o contrato R11 não o incluiu. Os textos ratificados seguem com autor e data; selá-lo é da v413, se o autor quiser.",
     "8. **O app, o contrato do JEV e a memória científica da fila** seguem na versão anterior até a ordem de release ao orquestrador (como na v411); o "
     "depósito no Zenodo é ato do autor.", "",
     "**Textos da custódia (gerência c1, 19/11/2026; substituem o molde factual da G1; números lidos do selo, do core e dos recibos por "
     "`montar_handoff_e_linhagem_v412.py` e conferidos antes de gravar com `custodia_g1.textos.portao` e `custodia_g1.h0dn.conferir_bloco`; validade no "
     "kernel não é creditação):**", ""]
H += [mk(i, t) + "\n" for i, t in PROSA]
H += ["**Textos que a abertura do H0DN × BG1 torna obrigatórios (v412):** a `NOTA_EN` da v412 (com a linha do estatuto ratificada em 13/11, verbatim); o "
      "`README_H0DN` (PT) do handoff da v411, verbatim; e os 46 textos da vitrine ratificada pelo operador em 13/11/2026 (`VITRINE_RATIFICADA_v411.json`, "
      "sha16 `%s`; fontes e decisões lá), VERBATIM, com o sufixo da versão. Nenhum deles foi reescrito." % RAT16, ""]
H += [mk(i, t) + "\n" for i, t in ABRE]
H += ["**Texto público aprovado (os blocos da R25 para o README e o ESTADO_ATUAL, PT e EN; não são `PARAGRAFO_*`: a custódia decide o lugar):**", ""]
for lg in ("pt", "en"):
    for nome in ("acrescenta", "pnp", "fluidos", "geometria", "abertos"):
        H += [mk("TEXTO_PUBLICO_README_%s_%s" % (lg.upper(), nome.upper()), BL["readme:%s" % lg][nome]) + "\n"]
H += ["Pasta da cadeia: `work\\cadeia_de_selo\\v412` (contrato vigente `CONTRATO_v412_R11.md`; lista `insumos\\MANIFESTO_PEDRAS_v412_R12.json`; "
      "esperados `ESPERADOS_v412.json`; diffs `DIFFS_v412_RECIBO.json`). A gerência não fez custódia, commit nem push do espelho, do site ou da Central "
      "(D232). NOT_FALSIFIED nunca é a palavra da creditação; o gate não se move.", ""]
handoff = "\n".join(H) + "\n"
# ------------------------------------------------------------------ o bloco do diario
CAB = ("## %s — **v412 SELADA (COMPLETA)** `%s` — %s (v412): a página pública aprovada pelo autor, o contrato R11 e a lista R12; %d módulos novos, "
       "escada %d → %d") % (HOJE, U16, TIT_PT, NMOD, A_, B_)
L = ["", CAB, "<!-- linhagem_v412_selada -->", "",
     "**A ordem:** [INPUT] a página pública R25 aprovada pelo autor (recibo `PALAVRA_FINAL_DO_AUTOR_v412_R25.json`), o contrato R11 e a lista R12 (156 "
     "módulos), e a ordem do autor de 18/11/2026 para o fechamento sem outra IA (arquivo verbatim em `work\\cunhagens_13out`, sha16 `%s`). O rito é ato da "
     "gerência c1 (pacote `work\\cadeia_de_selo\\v412`); quem constrói não aprova, e o candidato não teve terceiro (decisão aberta)." % ORD16, "",
     "**O que entrou** [REAL, lido por script]: o `um.py` sha16 `%s` (%s B) sobre a v411 `%s`; escada **%d/%d** (antes %d/%d); %d módulos novos no kernel "
     "(1 arquivo mudado, a raiz `TGLExt.lean`; nenhum removido) e %d bandeiras novas; %d declarações auditadas e %d teoremas no relatório de axiomas, "
     "nenhuma fora do trio; cinco registros por especificação, todos verificados: %s; o gate não se move (`%s`); selo `%s` (sha16 `%s`); o stdout do rito "
     "termina com `RITO_RC=0` (sha16 `%s`); conferidor enxuto TUDO BATE (%d/%d)." % (
         U16, BYTES_PT, ESP["origem_sha16"], B_, B_, A_, A_, NMOD, NB, KHC, KHT,
         "; ".join("`%s` (`%s…`, %d checagens)" % (r_, VPRE[r_], NCHK[r_]) for r_ in REGS), GATE, TS, SELO16, SO16, len(CF["checagens"]), len(CF["checagens"])), "",
     "**O que não rodou** [REAL]: o elo B(n) (a Bancada fora do ar; a gerência não religou o serviço); a Etapa 3 foi enxuta; o candidato não teve "
     "leitura de terceiro. As decisões abertas estão no `HANDOFF_v412_CUSTODIA.md`. Validade não é creditação; `NOT_FALSIFIED` nunca é `CONFIRMED`.", ""]
linhagem = "\n".join(L)
# ------------------------------------------------------------------ a conferencia pelos parsers e guardas da G1, ANTES de escrever
viol = []
mq = NM.RE_OQUEE.search(handoff)
if not mq:
    viol.append("RE_OQUEE nao casou")
else:
    q = mq.groupdict()
    for nome, a, b in (("v", q["v"], VER), ("pin", q["pin"], U16), ("bytes", int(q["bytes"].replace(",", "").replace(".", "")), um.stat().st_size),
                       ("ant", q["ant"], ANT), ("antpin", q["antpin"], ESP["origem_sha16"]), ("escada", "%s/%s" % (q["a"], q["b"]), "%d/%d" % (B_, B_)),
                       ("comp", "COMPLETA" in q["comp"], True), ("rc", q["rc"], "0"), ("st", q["st"], "PASSED"), ("gate", "intocado" in q["gate"], True)):
        if a != b:
            viol.append("O que e': %s %r != %r" % (nome, a, b))
    ms = re.search(r"Selo\s*`(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)`", handoff[mq.start(): mq.start() + 900])
    if not ms or ms.group(1) != TS:
        viol.append("Selo `ts` nao casou com o selo (%s)" % TS)
mc = NM.RE_CAB.match(CAB + "\n")
if not (mc and mc.group("v") == VER and mc.group("pin") == U16 and int(mc.group("k")) == NMOD and int(mc.group("a")) == A_ and int(mc.group("b")) == B_ and mc.group("titulo") == TIT_PT):
    viol.append("RE_CAB nao casou com o cabecalho do diario")
abre, fecha = NM.RE_ABRE.findall(handoff), NM.RE_FECHA.findall(handoff)
if set(abre) ^ set(fecha) or len(abre) != len(set(abre)):
    viol.append("marcadores sem par ou duplicados")
corpos = {m.group("id"): m.group("corpo") for m in NM.RE_MARCADOR.finditer(handoff)}
for ident in tuple(TX.MARCADORES_OPCIONAIS) + tuple(H0.TODOS):
    if "%s_%s" % (ident, VER) not in corpos or not corpos["%s_%s" % (ident, VER)].strip():
        viol.append("falta o marcador %s_%s" % (ident, VER))
secoes = {}
for par in handoff.split("\n\n"):
    mm = re.match(r"\*\*(.+?)\*\*", par.strip())
    if mm:
        secoes.setdefault(mm.group(1).rstrip(": ").strip(), par.strip())
if not any(k.startswith("O elo B(n)") for k in secoes) or not any(k.lower().startswith("pendências só do operador") for k in secoes):
    viol.append("faltam as secoes «O elo B(n)» ou «Pendencias SO' do operador»")
conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", handoff)) | {sha(um), U16}
ab = H0.registro_aberto(core); Vh = H0.valores(ab[1]); Ah = H0.acervo(core)
for ident, t in PROSA + [("NOTA_EN", NOTA)]:
    viol += TX.portao(t, conh, rotulo=ident)
    viol += H0.conferir_bloco(t, Vh, ident, acervo=Ah)
for ident in ("ARCO_EN", "ARCO_PT"):
    t = dict(PROSA)[ident]
    if "'" in t or "<" in t or "\\" in t or "\n" in t:
        viol.append("%s: aspa simples, «<», barra invertida ou quebra de linha" % ident)
viol_rat = []
for ident, t in ABRE[1:]:
    viol_rat += H0.conferir_bloco(t, Vh, ident, painel=(ident == "README_PAINEL_H0DN"), acervo=Ah)
print("HANDOFF: %d B | marcadores %d | diario: %d B" % (len(handoff.encode("utf-8")), len(corpos), len(linhagem.encode("utf-8"))))
print("conferencia (prosa, NOTA, formas):", "LIMPA" if not viol else "VIOLACOES:")
for x in viol:
    print("   -", x)
print("conferencia dos textos ratificados (so' informativa):", "LIMPA" if not viol_rat else "%d achados:" % len(viol_rat))
for x in viol_rat[:12]:
    print("   -", x[:240])
print("\n" + OQUEE + "\n\n" + CAB)
if EXEC:
    assert not viol, "a conferencia da G1 reprovou o texto montado: nada escrito"
    ml = NOS / "MEMORIA_DA_LINHAGEM.md"; a = ml.read_bytes(); assert b"v412 SELADA" not in a, "o bloco v412 SELADA ja' existe"
    bak = ml.with_name(ml.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); bak.write_bytes(a); assert bak.read_bytes() == a
    fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
    novo = a.rstrip(b"\r\n") + fim + linhagem.replace("\n", fim.decode()).encode("utf-8") + fim
    tmp = ml.with_name(ml.name + ".tmp_c1"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); tmp.replace(ml); assert ml.stat().st_size > len(a)
    print("linhagem: bloco v412 SELADA acrescentado | backup", bak.name)
    ho = NOS / "HANDOFF_v412_CUSTODIA.md"
    if ho.exists():
        hb = ho.read_bytes(); hk = ho.with_name(ho.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")); hk.write_bytes(hb); assert hk.read_bytes() == hb
        print("handoff anterior guardado:", hk.name)
    assert sha(NOS / "um_absoluto_selo.json")[:16] == SELO16, "o selo mudou: nao escrevo o handoff"
    tmp = ho.with_name(ho.name + ".tmp_c1"); tmp.write_bytes(handoff.encode("utf-8")); assert tmp.stat().st_size == len(handoff.encode("utf-8")); tmp.replace(ho)
    rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "gerencia c1 (montar_handoff_e_linhagem_v412.py R2)", "handoff": str(ho), "handoff_sha256": sha(ho),
           "selo_sha16": SELO16, "um_py_sha16": U16, "marcadores": sorted(corpos), "conferencia": "LIMPA", "achados_ratificados": viol_rat}
    pr = V / "RECIBO_HANDOFF_v412.json"; pt_ = pr.with_name(pr.name + ".tmp"); pt_.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8"); pt_.replace(pr)
    print("HANDOFF gravado por ultimo:", ho, "| sha16", sha(ho)[:16], "| selo", SELO16, "| recibo", pr.name)

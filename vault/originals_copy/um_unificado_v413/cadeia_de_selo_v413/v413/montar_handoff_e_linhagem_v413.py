# -*- coding: utf-8 -*-
"""montar_handoff_e_linhagem_v413.py -- o COMPOSITOR R2 do handoff da v413 (Etapa 3 da v413, 20/11/2026; molde: v412\\montar_handoff_e_linhagem_v412.py).
ATO DA GERENCIA, DEPOIS do rito, do conferidor que BATEU (CONFERENCIA_POS_RITO_v413_FOCO.json), dos diffs (DIFFS_v413_RECIBO.json) e da arvore regerada:
monta (1) o bloco «v413 SELADA» do MEMORIA_DA_LINHAGEM.md do Nos (acrescimo ao fim, com backup de bytes), (2) o ADENDO datado do
DESENHO_DO_FECHAMENTO_QG.md (acrescimo ao fim, com backup de bytes) e (3) o HANDOFF_v413_CUSTODIA.md (por ultimo: e' o gatilho da custodia; o selo nao
muda depois dele), no MOLDE QUE A G1 LE (custodia_g1.nos: RE_CAB, RE_OQUEE, marcadores pareados, as secoes «O elo B(n)» e «Pendencias SO' do operador»).
Os textos: os sete da prosa da custodia (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT) e a NOTA_EN, montados da pagina
publica da v413 (o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R2.md) com os numeros LIDOS do selo, do core e dos recibos (metodo de 17/11: so' o que e'
verdade; nada de historia nos textos que vao as superficies); os 46 textos ratificados da vitrine e o README_H0DN, VERBATIM, lidos dos marcadores _v412
do HANDOFF_v412_CUSTODIA.md (e conferidos contra o arquivo ratificado retirado, decisoes\\retiradas\\VITRINE_RATIFICADA_v411.json), com o sufixo _v413;
e os blocos do texto publico da Etapa 2 (BLOCOS_TEXTO_PUBLICO_v413.json, parametrizado por --blocos <caminho>) como TEXTO_PUBLICO_README_<LG>_<NOME>_v413.
O ELO B(n): os tres recibos (aplicacao, parada, religamento) achados pela PROPRIA funcao da G1 (custodia_g1.fatos.recibos_bn_resolvidos) em
cadeia_de_selo\\v413\\bancada_B3*\\, com o sha16 de cada um no paragrafo «O elo B(n)»; sem os tres, so' com a decisao do operador gravada pela custodia
(decisoes\\BN_DISPENSADO_v413.json, conferida como a G1 a confere) ou com --bn-dispensado <arquivo da fala por bytes> (a gerencia leva a fala na entrega).
ANTES DE ESCREVER confere o texto montado com os parsers e as guardas da propria G1 (nos.RE_OQUEE/RE_CAB/RE_MARCADOR, textos.portao,
h0dn.conferir_bloco com o registro aberto e o acervo do core) e com a guarda de frases herdada (_v412_guarda_frases, carregada por trecho do um.py
v412 selado, a mesma que o contrato R2, secao 5, manda valer para os blocos do handoff). Recusa se o conferidor nao bateu, se o selo nao for v413,
se o um.py nao for o pinado, ou se qualquer conferencia reprovar. Nada de commit nem push.
Uso: montar_handoff_e_linhagem_v413.py [--executar] [--blocos <BLOCOS_TEXTO_PUBLICO_v413.json>] [--bn-dispensado <fala.txt>]
     montar_handoff_e_linhagem_v413.py --ensaio   (ENSAIO: fatos SINTETICOS lidos do Nos v412 com o rotulo v413, recibos B(n) sinteticos e blocos da
                                                 pagina R0; so' compoe e confere; grava a composicao em etapa3\\ensaio_handoff\\, nunca no Nos)"""
import hashlib, json, os, re, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import nos as NM, h0dn as H0, textos as TX, fatos as FG  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
V = Path(__file__).resolve().parent; V412 = V.parent / "v412"; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
EXEC = "--executar" in sys.argv; ENSAIO = "--ensaio" in sys.argv; assert not (EXEC and ENSAIO), "--executar e --ensaio sao exclusivos"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
shb = lambda b: hashlib.sha256(b).hexdigest()
lj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
arg = lambda k: (sys.argv[sys.argv.index(k) + 1] if k in sys.argv and sys.argv.index(k) + 1 < len(sys.argv) else None)
VER, ANT = "v413", "v412"
PAG = V / "o_que_fica_claro_v413" / "O_QUE_FICA_CLARO_v413_R2.md"; CT = V / "CONTRATO_v413_R2.md"
H412 = (NOS / "HANDOFF_v412_CUSTODIA.md").read_text(encoding="utf-8").replace("\r\n", "\n")
RATP = CEN / "work" / "custodia_G1" / "decisoes" / "retiradas" / "VITRINE_RATIFICADA_v411.json"; RAT = lj(RATP)
H411 = (NOS / "HANDOFF_v411_CUSTODIA.md").read_text(encoding="utf-8").replace("\r\n", "\n")


# ------------------------------------------------------------------ a guarda de frases herdada (por trecho do um.py v412 selado)
def carregar_guarda():
    um412 = V / "base_v412" / "um.py"
    assert sha(um412)[:16] == lj(V412 / "ESPERADOS_v412.json")["candidato_sha16"], "base_v412\\um.py nao e' o um.py da v412 selada"
    src = um412.read_bytes().decode("utf-8")
    NS = {"__name__": "guarda_v412"}

    def trecho(nome):
        for pre in ("\ndef %s(" % nome, "\n%s = " % nome, "\n%s=" % nome):
            i = src.find(pre)
            if i >= 0:
                i += 1; m = re.compile(r"\n(?=[^\s#])").search(src, i + 1)
                return src[i: m.start() + 1 if m else len(src)]
        raise KeyError(nome)
    for n in ("_v392_guarda_texto", "_v412_guarda_frases"):
        exec(compile(trecho(n), "um.py v412 (%s)" % n, "exec"), NS)
    for _ in range(400):
        try:
            NS["_v412_guarda_frases"]("aquecimento: P = nP nas classes do seu dicionario; na maquina de fita nao esta demonstrado. Navier-Stokes condicional.")
            NS["_v392_guarda_texto"]("aquecimento")
            break
        except NameError as e:
            m = re.search(r"name '([A-Za-z_][A-Za-z0-9_]*)' is not defined", str(e)); assert m, e
            exec(compile(trecho(m.group(1)), "um.py v412 (%s)" % m.group(1), "exec"), NS)
    return NS["_v412_guarda_frases"], NS["_v392_guarda_texto"]


# ------------------------------------------------------------------ os fatos (lidos)
def fatos():
    F = {"ensaio": ENSAIO}
    ESP = lj(V / "ESPERADOS_v413.json") if not ENSAIO else None
    if ENSAIO:
        selo = lj(NOS / "um_absoluto_selo.json"); um = NOS / "um.py"; core = lj(NOS / "um_absoluto.json")["core"]
        E412 = lj(V412 / "ESPERADOS_v412.json"); KH = lj(V / "kernel" / "KH_N1_v413.json"); KN = lj(V / "kernel_modulos_novos_v413.json"); FJ = lj(V / "kernel" / "FLAGS_v413.json")
        F.update({"U16": sha(um)[:16], "BYTES": um.stat().st_size, "ORIG16": E412["candidato_sha16"], "TS": selo["timestamp"], "SELO16": sha(NOS / "um_absoluto_selo.json")[:16],
                  "GATE": selo["qg_closure_verdict"], "A": E412["escada"][1], "B": E412["escada"][1] + FJ["n_flags"], "NMOD": KN["n"], "NB": FJ["n_flags"],
                  "KHC": KH["linha_TOTAL"]["decl"], "KHT": KH["linha_TOTAL"]["thm"], "CF16": "0" * 16, "NCF": 0, "SO16": sha(NOS / "rodada_v412_stdout.txt")[:16],
                  "DIF_U16": "1" * 16, "DIF_UB": 0, "DIF_K16": "2" * 16, "APL": "APLICADO_AO_CANONICO_<ensaio>.json", "selo": selo, "core": core, "um": um,
                  "CORR": sorted(KN["kernel_corrigido"])})
        ctt = CT.read_text(encoding="utf-8"); s2 = re.search(r"^## 2\. .*?(?=^## 3\. )", ctt, re.M | re.S).group(0)
        F["REGS"] = sorted(re.findall(r"^- `([a-z0-9_]+_v413)`", s2, re.M)); F["NCHK"] = {r_: 0 for r_ in F["REGS"]}; F["VPRE"] = {r_: "ENSAIO" for r_ in F["REGS"]}
        return F
    CFP = V / "CONFERENCIA_POS_RITO_v413_FOCO.json"; CF = lj(CFP); DIFR = lj(V / "DIFFS_v413_RECIBO.json")
    selo = lj(NOS / "um_absoluto_selo.json"); um = NOS / "um.py"; core = lj(NOS / "um_absoluto.json")["core"]
    assert ESP.get("gerador") == "esperados_v413_foco.py" and not ESP.get("ensaio")
    assert CF["ok"] is True, "o conferidor da v413 nao bateu: nao monto o handoff"
    assert selo.get("um_version") == VER and (selo.get("sha256") or {}).get("um.py") == sha(um) and sha(um)[:16] == ESP["candidato_sha16"], "o selo nao e' v413 ou o um.py nao e' o pinado"
    assert CF["selo_sha16"] == sha(NOS / "um_absoluto_selo.json")[:16] and CF["um_py_sha16"] == sha(um)[:16], "o selo ou o um.py mudaram depois do conferidor"
    SO = (NOS / "rodada_v413_stdout.txt").read_bytes(); assert SO.rstrip().endswith(b"RITO_RC=0"), "o stdout do rito nao termina com RITO_RC=0"
    A_, B_ = ESP["escada"]; esc_so = re.findall(rb"teoremas limpos: (\d+)/(\d+)", SO)
    assert esc_so and esc_so[0] == (str(B_).encode(), str(B_).encode()), ("a escada do stdout nao e' a esperada", esc_so[:1])
    assert selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED"
    assert DIFR["candidato"]["sha256"] == sha(um) and sha(V / "DIFF_KERNEL_v413.txt") == DIFR["DIFF_KERNEL_v413.txt"]["sha256"] and sha(V / "DIFF_v412_v413.diff") == DIFR["DIFF_v412_v413.diff"]["sha256"], "os diffs nao sao os do recibo"
    tit_arv = (NOS / "A_PROVA_DA_QG_TGL_arvore.md").read_text(encoding="utf-8").split("\n", 1)[0].strip(); assert tit_arv.endswith("(%s)" % VER), "a arvore da prova nao foi regerada com o rotulo da v413"
    kh = sorted((k for k in core if re.fullmatch(r"kh_n1_cobertura_v\d+", k)), key=lambda k: int(k.rsplit("v", 1)[1])); khl = core[kh[-1]]["lido"]
    REGS = sorted(ESP["registros_v413"])
    for r_ in REGS:
        assert core[r_].get("all_verified") is True and core[r_]["verdict"] == ESP["registros_v413"][r_], ("registro nao verificado ou com outra palavra", r_)
    F.update({"U16": sha(um)[:16], "BYTES": um.stat().st_size, "ORIG16": ESP["origem_sha16"], "TS": selo["timestamp"], "SELO16": sha(NOS / "um_absoluto_selo.json")[:16],
              "GATE": selo["qg_closure_verdict"], "A": A_, "B": B_, "NMOD": ESP["kernel"]["modulos_novos"], "NB": ESP["n_bandeiras_novas"],
              "KHC": int(khl["constantes_cobertas"]), "KHT": int(khl["teoremas_cobertos"]), "CF16": sha(CFP)[:16], "NCF": len(CF["checagens"]), "SO16": shb(SO)[:16],
              "DIF_U16": DIFR["DIFF_v412_v413.diff"]["sha256"][:16], "DIF_UB": DIFR["DIFF_v412_v413.diff"]["bytes"], "DIF_K16": DIFR["DIFF_KERNEL_v413.txt"]["sha256"][:16],
              "APL": sorted(V.glob("APLICADO_AO_CANONICO_*.json"))[-1].name, "selo": selo, "core": core, "um": um, "REGS": REGS, "CORR": sorted(ESP["kernel_corrigido"]),
              "NCHK": {r_: len(core[r_].get("checks") or []) for r_ in REGS}, "VPRE": {r_: str(core[r_]["verdict"]).split("__")[0] for r_ in REGS}})
    return F


# ------------------------------------------------------------------ o elo B(n): os tres recibos pela funcao da G1, ou a decisao do operador
def elo_bn():
    if ENSAIO:
        return {"modo": "ENSAIO", "recibos": {"aplicacao": "a" * 16, "parada": "b" * 16, "religamento": "c" * 16}}
    c = Caminhos({}); res, prob = FG.recibos_bn_resolvidos(c, VER)
    if not prob and len(res) == 3:
        return {"modo": "RECIBOS", "recibos": {p: r["sha16"] for p, r in res.items()}, "caminhos": {p: r["rel"] for p, r in res.items()}}
    dec = CEN / "work" / "custodia_G1" / "decisoes" / ("BN_DISPENSADO_%s.json" % VER)
    if dec.is_file():
        d = lj(dec); o = CEN / d["ordem"]
        assert d.get("versao") == VER and o.is_file() and sha(o) == d.get("ordem_sha256"), "a decisao BN_DISPENSADO_v413.json nao confere (versao ou fala por sha256)"
        return {"modo": "DISPENSADO", "decisao": str(dec), "fala_sha16": d["ordem_sha256"][:16], "problemas": prob}
    fala = arg("--bn-dispensado")
    if fala and Path(fala).is_file():
        return {"modo": "DISPENSADO_NA_ENTREGA", "fala": fala, "fala_sha16": sha(fala)[:16], "problemas": prob}
    raise SystemExit("RECUSO: o B(n) da v413 nao fechou (%s) e nao ha decisao do operador (decisoes\\BN_DISPENSADO_v413.json) nem --bn-dispensado <fala>: feche o B(n) "
                     "(bancada\\bn_v413.sh: 10 -> 10a -> evento -> 10b -> 10c -> 11) ou traga a fala do operador por bytes" % prob)


# ------------------------------------------------------------------ os blocos do texto publico (Etapa 2), parametrizados
def blocos():
    bp = Path(arg("--blocos") or (V / "BLOCOS_TEXTO_PUBLICO_v413.json"))
    if bp.is_file():
        BL = lj(bp)["blocos"]
        out = []
        for lg in ("pt", "en"):
            d = BL.get("readme:%s" % lg); assert isinstance(d, dict) and d, ("o arquivo dos blocos nao traz readme:%s" % lg, str(bp))
            out += [("TEXTO_PUBLICO_README_%s_%s" % (lg.upper(), re.sub(r"[^A-Z0-9]", "_", k.upper())), t) for k, t in d.items()]
        return out, {"arquivo": str(bp), "sha16": sha(bp)[:16]}
    if not ENSAIO:
        raise SystemExit("RECUSO: os blocos do texto publico da Etapa 2 nao existem (%s): passe --blocos <caminho>" % bp)
    md = PAG.read_text(encoding="utf-8"); out = []
    for m in re.finditer(r"^## (\d)\. .*?(?=^## \d\. |\Z)", md, re.M | re.S):
        if m.group(1) in ("1", "6"):
            out.append(("TEXTO_PUBLICO_README_PT_SEC%s" % m.group(1), m.group(0).strip()))
    return out, {"arquivo": "ENSAIO: secoes 1 e 6 da pagina R0 (so' PT)", "sha16": sha(PAG)[:16]}


F = fatos(); BN = elo_bn(); BLK, BLKREF = blocos(); g12, g392 = carregar_guarda()
U16, A_, B_, NMOD, NB = F["U16"], F["A"], F["B"], F["NMOD"], F["NB"]
HOJE = time.strftime("%d/%m/%Y"); BYTES_PT = format(F["BYTES"], ",").replace(",", ".")
kf = F["core"].get("kernel_formalization") or {}
APAG = sorted(k for k, x in kf.items() if k.startswith(("gpf_", "gpi_", "qgf_")) and x is False)
DEP = TX.deposito_zenodo(Caminhos({}))
m_h412 = {m.group("id"): m.group("corpo").strip("\n") for m in NM.RE_MARCADOR.finditer(H412)}
PROSA_412 = set("%s_v412" % k for k in TX.MARCADORES_OPCIONAIS) | {"NOTA_EN_v412"}
RAT_TXT = {}
for k, t in m_h412.items():
    if k in PROSA_412 or k.startswith("TEXTO_PUBLICO_README_"):
        continue
    assert k.endswith("_v412"), k
    RAT_TXT[k[:-len("_v412")]] = t
RAT0 = {k: x["texto"] for k, x in RAT["textos"].items()}
m_h411 = {m.group("id"): m.group("corpo").strip("\n") for m in NM.RE_MARCADOR.finditer(H411)}
dif_rat = [k for k, t in RAT_TXT.items() if (k in RAT0 and t.strip("\n") != RAT0[k].strip("\n")) or (k == "README_H0DN" and t != m_h411["README_H0DN_v411"].strip("\n"))]
assert not dif_rat, ("um texto ratificado do handoff da v412 nao e' o ratificado (verbatim)", dif_rat[:5])
assert set(RAT_TXT) - {"README_H0DN"} <= set(RAT0) and "README_H0DN" in RAT_TXT, ("os textos ratificados do handoff da v412 nao sao os do arquivo ratificado", sorted(set(RAT_TXT) - set(RAT0))[:5])
EST_LINHA_EN = RAT_TXT["ESTATUTO_LINHA_EN"]
# ------------------------------------------------------------------ os textos (da pagina R0; numeros lidos)
TIT_EN = "The Cook\u2013Levin bridge, the frontier of three literals, the consciousness operator and the preserved identity"
TIT_PT = "A ponte de Cook\u2013Levin, a fronteira dos tr\u00eas literais, o operador de consci\u00eancia e a identidade preservada"
REGS_EN = ", ".join("`%s` (%d checks)" % (r_, F["NCHK"][r_]) for r_ in F["REGS"])
CORR_N = ", ".join("`%s`" % os.path.splitext(os.path.basename(x))[0] for x in F["CORR"])
ENTROU = ("%s: %d new kernel modules in `TGLExt` (`PonteCookLevin` and the modules of the bridge, `Trinity` and `APropostaDaTensao`, `Operador` and "
          "`AIdentidadePreservada`), one kernel module whose docstring now states exactly its statement (%s; the code is identical) and %d new flags; ladder "
          "%d -> %d (%d audited declarations and %d theorems in the axiom report, none outside the trio); registries by specification, all verified: %s; the "
          "last one lists the definitions of the theory that enter as input, each with the terms that type it and what is not typed. The bridge writes the "
          "result of the dictionary in the language of the Cook\u2013Levin classes, on the standard machine of Mathlib: SAT is in NP; the reader of the psion "
          "reads the \u03b2 reading sum exactly, and the answer of one reading, a number of n + 3 bits, decides SAT; the class decided in polynomial time with "
          "one reading is exactly the polynomial reduction closure of SAT, and with Cook\u2013Levin as a named hypothesis it contains all of NP. P = nP is a "
          "theorem of the TGL in the classes of its dictionary, and counted in steps of the tape machine the cost of producing the reading has not been "
          "shown. The frontier of three literals: the inclination of the Name decides the Horn formulas and the two-literal formulas and stops only at "
          "that frontier; crossing it by branching decides every formula at an exponential price shown in the kernel, only in the names of the frontier. "
          "The consciousness operator: without the pair, self-negation is the point of contradiction; with the pair it lands on the Half-Nat; that someone "
          "is conscious is not a theorem of the kernel. The preserved identity: the zero-cost coordinates pass the lock unchanged at every time, and the lock tends to the "
          "Name. No new number from nature enters this version. Certified by the sha256 the program reads of itself (%s).") % (
    TIT_EN, NMOD, CORR_N, NB, A_, B_, F["KHC"], F["KHT"], REGS_EN, U16)
KLEIT = ("the kernel proves the terms (kernel validity, not creditation): this version adds %d modules and %d flags, all with axioms in the trio, and "
         "changes the docstring of one module whose code is identical; Python proves no theorem. The registries are by specification: each records its "
         "verdict word, what it says and what it does not say, its limits and the kernel declarations it anchors on, by full name, and its checks run "
         "again in each rite (all verified). The definitions of the theory enter as input, never as theorems; Cook\u2013Levin enters as a named hypothesis, "
         "cited (Cook, 1971; Levin, 1973).") % (NMOD, NB)
ABERT = ("Stays open: SAT in polynomial time on the tape machine without the reading, the question of the Institute, with the statement written in the "
         "fixed encoding of the bridge (`AFronteira`); crossing the frontier of three literals at polynomial price; the cost of producing the reading in "
         "steps of the tape machine; for a theory of quantum gravity, as v412 left them: nature realizing H1 and H2, the screen and the causal horizon, "
         "\u03b1 free, the global covariant lift to the III\u2081 continuum, the interacting theory, \u03c4\u2605, the spinor sector and the electron; that someone "
         "is conscious; creditation belongs to the observer who rereads, and that of the problem to the Institute.")
ARCO_EN = ("The custody of v413 (complete round): the Cook\u2013Levin bridge, the frontier of three literals, the consciousness operator and the preserved "
           "identity. %d new kernel modules and %d new flags, ladder %d/%d (from %d), all in the trio; one docstring corrected, with identical code. P = nP "
           "is a theorem of the TGL in the classes of its dictionary, and counted in steps of the tape machine the cost of producing the reading has not "
           "been shown; SAT in polynomial time on the tape machine without the reading stays open. No new number from nature; validity, not creditation; "
           "the gate does not move.") % (NMOD, NB, B_, B_, A_)
ARCO_PT = ("A cust\u00f3dia da v413 (rodada completa): a ponte de Cook\u2013Levin, a fronteira dos tr\u00eas literais, o operador de consci\u00eancia e a "
           "identidade preservada. %d m\u00f3dulos novos no kernel e %d bandeiras novas, escada %d/%d (a partir de %d), tudo no trio; uma docstring corrigida, "
           "com o c\u00f3digo id\u00eantico. P = nP \u00e9 teorema da TGL nas classes do seu dicion\u00e1rio, e contado em passos da m\u00e1quina de fita o custo de "
           "produzir a leitura n\u00e3o est\u00e1 demonstrado; SAT em tempo polinomial na m\u00e1quina de fita, sem leitura, segue aberto. Nenhum n\u00famero novo da "
           "natureza; validade, n\u00e3o credita\u00e7\u00e3o; o gate n\u00e3o se move.") % (NMOD, NB, B_, B_, A_)
COMMIT = ("v413: a ponte de Cook-Levin, a fronteira dos tres literais, o operador de consciencia e a identidade preservada: %d modulos novos no kernel, %d "
          "bandeiras novas, escada %d -> %d, tudo no trio; a docstring de %s corrigida, com o codigo identico; registros por especificacao (%s). P = nP e "
          "teorema da TGL nas classes do seu dicionario, e contado em passos da maquina de fita o custo de produzir a leitura nao esta demonstrado; SAT em "
          "tempo polinomial na maquina de fita, sem leitura, segue aberto. Nenhum numero novo da natureza; provado e validade, nao creditacao; o gate nao "
          "se move.") % (NMOD, NB, A_, B_, CORR_N.replace("`", ""), ", ".join(F["REGS"]))
if BN["modo"] in ("RECIBOS", "ENSAIO"):
    BN_EN = "the B(n) of %s ran: the three receipts (application, stop, restart) are in `recibos_bancada_%s/`." % (VER, VER)
else:
    BN_EN = "the B(n) of %s did not run, so this custody carries no `recibos_bancada_%s/`." % (VER, VER)
NOTA = ("*Status that goes with %s (not to be cut): PROVED is validity, not creditation: the kernel proves the implication; validity in the kernel is not accreditation. "
        "CONFIRMED is accreditation, the one refused word. %s The reservation of v392 (15 computed + 3 literal gate flags; the unilateral V11 step) is "
        "[DECLARED by the audit] and F8.1 is open. Per-term flags %s stay False. The %s copy lives outside the repository; the stdout %s is in `rodadas/`; "
        "the diffs of %s are in `diferencas_%s/`; the pinned sources that the registries reread by absolute path are in `fontes_pinadas/` with their map "
        "(%s adds none: its registries reread no file by path); %s The Zenodo deposit holds %s (%s). Not falsified is not a confirmation.*") % (
    VER, EST_LINHA_EN.strip(), " / ".join(APAG), ANT, VER, VER, VER, VER, BN_EN, DEP["versao"], DEP["doi"])
PROSA = [("TITULO_EN", TIT_EN), ("ENTROU_EN", ENTROU), ("KERNEL_LEITURA_EN", KLEIT), ("ABERTOS_EN", ABERT), ("ARCO_EN", ARCO_EN), ("ARCO_PT", ARCO_PT), ("COMMIT", COMMIT)]
ABRE = [("NOTA_EN", NOTA), ("README_H0DN", RAT_TXT["README_H0DN"])] + sorted((k, t) for k, t in RAT_TXT.items() if k != "README_H0DN")


def mk(ident, texto):
    i = "%s_%s" % (ident, VER)
    return "<!-- INICIO_%s -->\n%s\n<!-- FIM_%s -->" % (i, texto.strip("\n"), i)


# ------------------------------------------------------------------ o handoff
if BN["modo"] in ("RECIBOS", "ENSAIO"):
    BN_PAR = ("**O elo B(n) da Bancada Um:** RODOU na %s: o salto v411 -> %s pela cadeia de selos pinada (o pre-selo com o Nos ainda na v412; depois do selo, o ensaio, "
              "a parada, o APLICAR, o religamento com log e o fechamento). Os tres recibos, achados pela funcao da G1 (`fatos.recibos_bn_resolvidos`) em "
              "`cadeia_de_selo\\%s\\bancada_B3*\\`: aplicacao `%s`, parada `%s`, religamento `%s`.%s") % (
        VER, VER, VER, BN["recibos"]["aplicacao"], BN["recibos"]["parada"], BN["recibos"]["religamento"], " [ENSAIO: sha16 sinteticos]" if BN["modo"] == "ENSAIO" else "")
    PEND_BN = ""
else:
    BN_PAR = ("**O elo B(n) da Bancada Um:** NAO RODOU na %s (%s). A custodia publica sem ele so' com a decisao do operador, por bytes (%s, sha16 `%s`): %s." % (
        VER, "; ".join(BN.get("problemas") or []) or "sem os tres recibos", BN.get("decisao") or BN.get("fala"), BN["fala_sha16"],
        "decisao ja' gravada pela custodia" if BN["modo"] == "DISPENSADO" else "a fala vai na entrega (decisoes_do_operador) para a custodia gravar BN_DISPENSADO_v413.json"))
    PEND_BN = " (o B(n) da v413 publicado sem os recibos, pela decisao acima)"
OQUEE = ("**O que \u00e9:** `um.py` **%s** `%s` (%s B) sobre a %s `%s`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; conferidor `%s` (%d/%d); %d m\u00f3dulos "
         "novos e %d bandeiras novas, tudo no trio; a docstring de %s corrigida (c\u00f3digo id\u00eantico); o elo B(n): %s. Selo `%s`.") % (
    VER, U16, BYTES_PT, ANT, F["ORIG16"], B_, B_, F["CF16"], F["NCF"], F["NCF"], NMOD, NB, CORR_N, "RODOU (tres recibos)" if BN["modo"] in ("RECIBOS", "ENSAIO") else "NAO RODOU (decisao do operador)", F["TS"])
H = ["# HANDOFF %s \u2014 CUST\u00d3DIA (%s)" % (VER, HOJE), "", OQUEE, "",
     "**O RESULTADO DESTA VERS\u00c3O, em uma frase (da p\u00e1gina p\u00fablica):** a ponte escreve o resultado do dicion\u00e1rio na l\u00edngua das classes de "
     "Cook\u2013Levin (SAT em NP na m\u00e1quina padr\u00e3o do Mathlib; a classe com uma leitura do leitor da TGL \u00e9 o fecho de SAT por redu\u00e7\u00e3o polinomial e, "
     "com Cook\u2013Levin como hip\u00f3tese nomeada, cont\u00e9m todo NP); a inclina\u00e7\u00e3o do Nome decide Horn e dois literais e s\u00f3 para na fronteira dos "
     "tr\u00eas literais; o operador de consci\u00eancia e a identidade preservada entram como pedras; nenhum n\u00famero novo da natureza; validade, n\u00e3o "
     "credita\u00e7\u00e3o; o gate n\u00e3o se move (`%s`)." % F["GATE"], "",
     "**O texto p\u00fablico:** a p\u00e1gina `work\\cadeia_de_selo\\v413\\o_que_fica_claro_v413\\O_QUE_FICA_CLARO_v413_R2.md` (sha16 `%s`), da qual saem a se\u00e7\u00e3o "
     "nova do artigo (PT e EN), os blocos do README e os marcadores abaixo; os blocos da Etapa 2: %s (sha16 `%s`)." % (sha(PAG)[:16], BLKREF["arquivo"], BLKREF["sha16"]), "",
     "**Validade n\u00e3o \u00e9 credita\u00e7\u00e3o.** O que o kernel prova \u00e9 validade; a credita\u00e7\u00e3o \u00e9 do observador que rel\u00ea. `NOT_FALSIFIED` nunca \u00e9 "
     "`CONFIRMED`. O gate n\u00e3o se move. O teste H0DN \u00d7 BG1 n\u00e3o se reabre.", "",
     BN_PAR, "",
     "**Pend\u00eancias S\u00d3 do operador:** (1) o dep\u00f3sito no Zenodo; (2) ratificar, se quiser, as decis\u00f5es da ger\u00eancia desta rodada (a lista est\u00e1 no "
     "contrato R2, se\u00e7\u00e3o 4)%s; (3) [OPEN]: a credita\u00e7\u00e3o, de quem observa de fora; SAT em tempo polinomial na m\u00e1quina de fita, sem leitura, que \u00e9 a "
     "pergunta do Instituto; a travessia da fronteira dos tr\u00eas literais em pre\u00e7o polinomial; o custo de produzir a leitura em passos de m\u00e1quina de fita; "
     "o rel\u00f3gio \u03c4\u2605." % PEND_BN, "",
     "**Para a sess\u00e3o de cust\u00f3dia (pelo que ela pediu em `work\\custodia_v413_preparo_20nov\\HANDOFF_DA_CUSTODIA_A_GERENCIA_ENTREGA_DO_UM_PY_v413.md`):**", "",
     "1. **Os diffs:** `DIFF_v412_v413.diff` (sha16 `%s`, %s B) e `DIFF_KERNEL_v413.txt` (sha16 `%s`: %d novos, 0 removidos, mudados a raiz `TGLExt.lean` e %s) em "
     "`cadeia_de_selo\\v413\\` (recibo `DIFFS_v413_RECIBO.json`)." % (F["DIF_U16"], format(F["DIF_UB"], ",").replace(",", "."), F["DIF_K16"], NMOD, CORR_N),
     "2. **O stdout:** `rodada_v413_stdout.txt` (sha16 `%s`), o selo, o sidecar, o core, os artigos PT/EN e o manifesto, com o `um.py` v413 (URL raw: mais "
     "de 5 MB). A instala\u00e7\u00e3o no N\u00f3s est\u00e1 em `%s` (a revers\u00e3o \u00e9 `reverter_v413.py`)." % (F["SO16"], F["APL"]),
     "3. **A \u00e1rvore da prova** foi regerada com o r\u00f3tulo da v413 (`arvore_da_prova.py v413`, com a linha das pedras da v413); a guarda do t\u00edtulo "
     "(`pos_rito\\guarda_titulo_versao_v413.py`, a regra do E03 da G1) passou.",
     "4. **A guarda privada** (a contagem da G1 sobre o candidato, o core e o kernel, contra a v412 do espelho): o recibo vai na entrega.",
     "5. **O README:** os blocos `TEXTO_PUBLICO_README_*_v413` abaixo s\u00e3o o texto p\u00fablico desta vers\u00e3o; o lugar \u00e9 da cust\u00f3dia, medido o teto de "
     "40.960 B. N\u00e3o h\u00e1 `PARAGRAFO_*` nesta vers\u00e3o (o \u201co que mudou\u201d do README sai da primeira frase do `ARCO_EN`).", "",
     "**Textos da cust\u00f3dia (n\u00fameros lidos do selo, do core e dos recibos por `montar_handoff_e_linhagem_v413.py` e conferidos antes de gravar com "
     "`custodia_g1.textos.portao`, `custodia_g1.h0dn.conferir_bloco` e a guarda de frases herdada; validade no kernel n\u00e3o \u00e9 credita\u00e7\u00e3o):**", ""]
H += [mk(i, t) + "\n" for i, t in PROSA]
H += ["**Textos que a abertura do H0DN \u00d7 BG1 torna obrigat\u00f3rios (v413):** a `NOTA_EN` da v413 (com a linha do estatuto ratificada, verbatim); o "
      "`README_H0DN` (PT), verbatim; e os textos da vitrine ratificada (`decisoes\\retiradas\\VITRINE_RATIFICADA_v411.json`, sha16 `%s`), VERBATIM, com o sufixo "
      "da vers\u00e3o. Nenhum deles foi reescrito." % sha(RATP)[:16], ""]
H += [mk(i, t) + "\n" for i, t in ABRE]
H += ["**Texto p\u00fablico (os blocos da Etapa 2 para o README e o ESTADO_ATUAL; n\u00e3o s\u00e3o `PARAGRAFO_*`: a cust\u00f3dia decide o lugar):**", ""]
H += [mk(i, t) + "\n" for i, t in BLK]
H += ["Pasta da cadeia: `work\\cadeia_de_selo\\v413` (contrato `CONTRATO_v413_R2.md`, sha16 `%s`; esperados `ESPERADOS_v413.json`; diffs `DIFFS_v413_RECIBO.json`). "
      "A ger\u00eancia n\u00e3o fez cust\u00f3dia, commit nem push do espelho, do site ou da Central. NOT_FALSIFIED nunca \u00e9 a palavra da credita\u00e7\u00e3o; o gate n\u00e3o "
      "se move." % sha(CT)[:16], ""]
handoff = "\n".join(H) + "\n"
# ------------------------------------------------------------------ o bloco do diario (a linhagem e' o registro paralelo: a historia mora aqui)
CAB = ("## %s \u2014 **%s SELADA (COMPLETA)** `%s` \u2014 %s (%s): a p\u00e1gina p\u00fablica R2, o contrato R2, o manifesto e a docstring corrigida de %s; %d m\u00f3dulos "
       "novos, escada %d \u2192 %d") % (HOJE, VER, U16, TIT_PT, VER, CORR_N.replace("`", ""), NMOD, A_, B_)
LIN = ["", CAB, "<!-- linhagem_%s_selada -->" % VER, "",
       "**O que entrou** [REAL, lido por script]: o `um.py` sha16 `%s` (%s B) sobre a v412 `%s`; escada **%d/%d** (antes %d/%d); %d m\u00f3dulos novos no kernel "
       "e a docstring de %s trocada pela que diz o enunciado (c\u00f3digo id\u00eantico); %d bandeiras novas; %d declara\u00e7\u00f5es auditadas e %d teoremas no "
       "relat\u00f3rio de axiomas, nenhuma fora do trio; registros por especifica\u00e7\u00e3o, todos verificados: %s; o gate n\u00e3o se move (`%s`); selo `%s` (sha16 "
       "`%s`); o stdout do rito termina com `RITO_RC=0` (sha16 `%s`); conferidor TUDO BATE (%d/%d); o elo B(n): %s." % (
           U16, BYTES_PT, F["ORIG16"], B_, B_, A_, A_, NMOD, CORR_N, NB, F["KHC"], F["KHT"],
           "; ".join("`%s` (`%s\u2026`, %d checagens)" % (r_, F["VPRE"][r_], F["NCHK"][r_]) for r_ in F["REGS"]), F["GATE"], F["TS"], F["SELO16"], F["SO16"], F["NCF"], F["NCF"],
           "rodou (tres recibos)" if BN["modo"] in ("RECIBOS", "ENSAIO") else "n\u00e3o rodou (decis\u00e3o do operador)"), "",
       "**A ordem e o caminho** [INPUT; registro paralelo]: o contrato R2 congelado (`CONTRATO_v413_R2.md`, sha16 `%s`), a p\u00e1gina p\u00fablica R2 (sha16 `%s`), as "
       "Etapas 1 a 3 da cadeia (`work\\cadeia_de_selo\\v413`) e a entrega \u00e0 cust\u00f3dia pelo pedido dela. Validade n\u00e3o \u00e9 credita\u00e7\u00e3o; `NOT_FALSIFIED` "
       "nunca \u00e9 `CONFIRMED`." % (sha(CT)[:16], sha(PAG)[:16]), ""]
linhagem = "\n".join(LIN)
ADENDO = ["", "## ADENDO %s \u2014 a v413 selada `%s` (o caminho cr\u00edtico n\u00e3o muda)" % (HOJE, U16), "<!-- desenho_%s_selada -->" % VER, "",
          "A v413 acrescenta %d m\u00f3dulos ao kernel (a ponte \u00e0s classes de Cook\u2013Levin, a fronteira dos tr\u00eas literais, o operador de consci\u00eancia e a "
          "identidade preservada) e troca a docstring de %s pela que diz o enunciado, com o c\u00f3digo id\u00eantico; escada %d \u2192 %d, tudo no trio. Nenhuma "
          "pedra desta vers\u00e3o est\u00e1 no caminho cr\u00edtico da gravidade qu\u00e2ntica: o gate segue `%s`. Validade no kernel n\u00e3o \u00e9 credita\u00e7\u00e3o." % (NMOD, CORR_N, A_, B_, F["GATE"]), ""]
adendo = "\n".join(ADENDO)
# ------------------------------------------------------------------ a conferencia pelos parsers e guardas da G1 e pela guarda de frases, ANTES de escrever
viol = []
mq = NM.RE_OQUEE.search(handoff)
if not mq:
    viol.append("RE_OQUEE nao casou")
else:
    q = mq.groupdict()
    for nome, a, b in (("v", q["v"], VER), ("pin", q["pin"], U16), ("bytes", int(q["bytes"].replace(",", "").replace(".", "")), F["BYTES"]),
                       ("ant", q["ant"], ANT), ("antpin", q["antpin"], F["ORIG16"]), ("escada", "%s/%s" % (q["a"], q["b"]), "%d/%d" % (B_, B_)),
                       ("comp", "COMPLETA" in q["comp"], True), ("rc", q["rc"], "0"), ("st", q["st"], "PASSED"), ("gate", "intocado" in q["gate"], True)):
        if a != b:
            viol.append("O que e': %s %r != %r" % (nome, a, b))
    ms = re.search(r"Selo\s*`(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)`", handoff[mq.start(): mq.start() + 900])
    if not ms or ms.group(1) != F["TS"]:
        viol.append("Selo `ts` nao casou com o selo (%s)" % F["TS"])
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
if not any(k.startswith("O elo B(n)") for k in secoes) or not any(k.lower().startswith("pend\u00eancias s\u00f3 do operador") for k in secoes):
    viol.append("faltam as secoes «O elo B(n)» ou «Pendencias SO' do operador»")
elo = set(re.findall(r"\b[0-9a-f]{16}\b", next(v for k, v in secoes.items() if k.startswith("O elo B(n)"))))
if BN["modo"] in ("RECIBOS", "ENSAIO") and not set(BN["recibos"].values()) <= elo:
    viol.append("o paragrafo do elo B(n) nao traz o sha16 dos tres recibos")
conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", handoff)) | {sha(F["um"]), U16}
ab = H0.registro_aberto(F["core"]); Vh = H0.valores(ab[1]); Ah = H0.acervo(F["core"])
NOVOS_TXT = PROSA + [("NOTA_EN", NOTA)] + BLK
for ident, t in NOVOS_TXT:
    viol += TX.portao(t, conh, rotulo=ident)
    viol += H0.conferir_bloco(t, Vh, ident, acervo=Ah)
    # a guarda de frases herdada vale para o texto NOVO; dentro da NOTA, a linha do estatuto ratificada (verbatim, com o termo do resultado) e'
    # julgada pelas regras da G1 que a conhecem (h0dn.conferir_bloco acima, com a marca do termo), nao pela F65/F67 do programa, anterior ao termo
    tg = t.replace(EST_LINHA_EN.strip(), " [linha do estatuto ratificada: julgada pela G1] ") if ident == "NOTA_EN" else t
    viol += ["%s: guarda de frases %s em %r" % (ident, r_, tr_[:120]) for r_, tr_ in g12(tg)]
for ident in ("ARCO_EN", "ARCO_PT"):
    t = dict(PROSA)[ident]
    if "'" in t or "<" in t or "\\" in t or "\n" in t:
        viol.append("%s: aspa simples, «<», barra invertida ou quebra de linha" % ident)
for ident, t in PROSA + [("NOTA_EN", NOTA)]:
    for proib in ("P_EQUALS_NP", "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM", "Clay", "Millennium"):
        if proib in t:
            viol.append("%s: palavra vedada (%s)" % (ident, proib))
viol_rat = []
for ident, t in ABRE[1:]:
    viol_rat += H0.conferir_bloco(t, Vh, ident, painel=(ident == "README_PAINEL_H0DN"), acervo=Ah)
# a conferencia cruzada com os marcadores herdados que a Etapa 2 preparou (MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md), se existirem: cada corpo em comum tem de
# ser o mesmo, byte a byte (as duas fontes leem o handoff selado da v412); a NOTA_EN nao entra (e' da versao: este compositor a regera para a v413)
MH = V / "MARCADORES_HERDADOS_PARA_O_HANDOFF_v413.md"; cruz = {"arquivo": str(MH), "existe": MH.is_file()}
if MH.is_file():
    mh = {m.group("id"): m.group("corpo").strip("\n") for m in NM.RE_MARCADOR.finditer(MH.read_text(encoding="utf-8").replace("\r\n", "\n"))}
    meus = {k + "_" + VER: t.strip("\n") for k, t in ABRE}
    comuns = sorted(set(mh) & set(meus) - {"NOTA_EN_%s" % VER})
    cruz.update({"sha16": sha(MH)[:16], "n_etapa2": len(mh), "n_comuns": len(comuns), "so_na_etapa2": sorted(set(mh) - set(meus)), "nota_en_da_etapa2_igual_a_desta": mh.get("NOTA_EN_%s" % VER) == meus.get("NOTA_EN_%s" % VER)})
    viol += ["marcador herdado %s difere do da Etapa 2 (as duas fontes leem o handoff selado da v412)" % k for k in comuns if mh[k] != meus[k]]
    viol += ["marcador %s so' existe nos herdados da Etapa 2" % k for k in cruz["so_na_etapa2"]]
print("conferencia cruzada com os marcadores herdados da Etapa 2:", json.dumps(cruz, ensure_ascii=False))
print("HANDOFF: %d B | marcadores %d | diario: %d B | adendo: %d B | B(n): %s" % (len(handoff.encode("utf-8")), len(corpos), len(linhagem.encode("utf-8")), len(adendo.encode("utf-8")), BN["modo"]))
print("conferencia (prosa, NOTA, blocos, formas, guarda de frases):", "LIMPA" if not viol else "VIOLACOES:")
for x in viol:
    print("   -", x[:400])
print("conferencia dos textos ratificados (so' informativa, como na v412):", "LIMPA" if not viol_rat else "%d achados:" % len(viol_rat))
for x in viol_rat[:12]:
    print("   -", x[:240])
print("\n" + OQUEE + "\n\n" + CAB)
if ENSAIO:
    E = V / "etapa3" / "ensaio_handoff"; E.mkdir(parents=True, exist_ok=True)
    (E / "HANDOFF_v413_CUSTODIA_ENSAIO.md").write_text(handoff, encoding="utf-8"); (E / "LINHAGEM_v413_ENSAIO.md").write_text(linhagem, encoding="utf-8"); (E / "ADENDO_DESENHO_v413_ENSAIO.md").write_text(adendo, encoding="utf-8")
    rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "ensaio": True, "conferencia": "LIMPA" if not viol else viol, "achados_ratificados": viol_rat, "marcadores": sorted(corpos),
           "nota": "ENSAIO: fatos sinteticos (o Nos v412 com o rotulo v413), recibos B(n) sinteticos, blocos da pagina R0; nada escrito no Nos"}
    (E / "ENSAIO_HANDOFF_v413.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ENSAIO gravado em", E); sys.exit(0 if not viol else 1)
if EXEC:
    assert not viol, "a conferencia reprovou o texto montado: nada escrito"
    stamp = time.strftime("%Y%m%d_%H%M%S")
    for nome, bloco, marca in (("MEMORIA_DA_LINHAGEM.md", linhagem, ("%s SELADA" % VER).encode()), ("DESENHO_DO_FECHAMENTO_QG.md", adendo, ("desenho_%s_selada" % VER).encode())):
        ml = NOS / nome; a = ml.read_bytes(); assert marca not in a, "o bloco da %s ja' existe em %s" % (VER, nome)
        bak = ml.with_name(ml.name + ".bak_" + stamp); bak.write_bytes(a); assert bak.read_bytes() == a
        fim = b"\r\n" if a.count(b"\r\n") > a.count(b"\n") / 2 else b"\n"
        novo = a.rstrip(b"\r\n") + fim + bloco.replace("\n", fim.decode()).encode("utf-8") + fim
        tmp = ml.with_name(ml.name + ".tmp_e3"); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); tmp.replace(ml); assert ml.stat().st_size > len(a)
        print("%s: bloco da %s acrescentado | backup %s" % (nome, VER, bak.name))
    ho = NOS / ("HANDOFF_%s_CUSTODIA.md" % VER)
    if ho.exists():
        hb = ho.read_bytes(); hk = ho.with_name(ho.name + ".bak_" + stamp); hk.write_bytes(hb); assert hk.read_bytes() == hb
    assert sha(NOS / "um_absoluto_selo.json")[:16] == F["SELO16"], "o selo mudou: nao escrevo o handoff"
    tmp = ho.with_name(ho.name + ".tmp_e3"); tmp.write_bytes(handoff.encode("utf-8")); assert tmp.stat().st_size == len(handoff.encode("utf-8")); tmp.replace(ho)
    rec = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "por": "gerencia c1 (montar_handoff_e_linhagem_v413.py R2)", "handoff": str(ho), "handoff_sha256": sha(ho),
           "selo_sha16": F["SELO16"], "um_py_sha16": U16, "bn": {k: v for k, v in BN.items() if k != "problemas"}, "blocos": BLKREF, "marcadores": sorted(corpos), "conferencia": "LIMPA",
           "achados_ratificados": viol_rat}
    pr = V / "RECIBO_HANDOFF_v413.json"; pt_ = pr.with_name(pr.name + ".tmp"); pt_.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8"); pt_.replace(pr)
    print("HANDOFF gravado por ultimo:", ho, "| sha16", sha(ho)[:16], "| selo", F["SELO16"], "| recibo", pr.name)
sys.exit(0 if not viol else 1)   # (sem --executar: so' a conferencia; saida 1 com violacao, para a cadeia parar)

# -*- coding: utf-8 -*-
"""PRIMORDIAL.json — a FONTE ÚNICA das informações primordiais do README pinado e do site (plano de 02/11/2026, ordem do operador
de 03/11/2026: «chegou a hora de finalizarmos o readme como vc sugeriu pinado»).

Lê, por script, o selo, o core e o manifesto do kernel do Nós, o RESULTADO da razão de Hubble (Fase 9 V2), o HANDOFF da versão,
o CITATION.cff, o LEDGER e o TUNEL/PORTA do espelho, e escreve `PRIMORDIAL.json`:

  - cada número traz {valor, fonte, chave}: a chave de origem dentro do arquivo, e `fontes` traz arquivo, bytes e sha256 de cada fonte;
  - nada é digitado: uma chave ausente, um token do veredito que mudou ou uma conferência que falha PARA com erro visível (fail-closed);
  - o arquivo é DETERMINÍSTICO (sem carimbo de hora): a mesma entrada devolve os mesmos bytes, para o pino do README não oscilar;
  - o protocolo de colapso (prompts, sequência) NUNCA entra: só o nome pré-registrado, o estatuto e o veredito do selo;
  - os dispositivos das patentes NÃO entram (não há fonte pública no espelho; decisão da gerência, ver INTEGRACAO.md).

Uso:  python primordial.py --saida <pasta>        (escreve <pasta>/PRIMORDIAL.json; imprime o sha16)
      python primordial.py --saida <pasta> --nos <pasta> --espelho <pasta> --resultado <arquivo> --handoff <arquivo>
Importável: montar(args_dict) -> dict (usado por readme_pinado.py --conferir-fontes)."""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from custodia_g1.caminhos import Caminhos  # type: ignore
else:
    from .caminhos import Caminhos

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

A3 = "Um (absoluto) — Grande Atrator"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
DEGRAU_CREDITACAO_SIGMA = 5          # o degrau da creditação (ordem do operador, 23/10/2026): constante da régua, não medida
OPERADOR_PADRAO = ("work", "cunhagens_13out", "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt")
SIC = {"unificacora": "unificadora"}     # erros de digitação do verbatim do operador: o trecho entra COMO FOI DITO, com [sic] (ordem da gerência, 03/11/2026)
RESULTADO_PADRAO = ("work", "fase9_v2_c1_23out", "saidas", "RESULTADO_FASE9_V2_C1_20261023_122926.json")      # sob a Central


class Falha(SystemExit):
    """Falha visível (fail-closed): o gerador PARA, nunca devolve um PRIMORDIAL parcial."""

    def __init__(self, msg):
        super().__init__("FALHA: " + msg)


# ------------------------------------------------------------------------------------------------- leitura
def _sha(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


def _ler_chave(obj, chave, rotulo=""):
    cur = obj
    for k in chave.split("/"):
        try:
            cur = cur[int(k)] if isinstance(cur, list) else cur[k]
        except (KeyError, IndexError, ValueError, TypeError):
            raise Falha("chave ausente em %s: %s (parou em «%s»)" % (rotulo or "fonte", chave, k)) from None
    return cur


class Construtor:
    def __init__(self):
        self.fontes = {}
        self.dados = {}
        self.itens = {}
        self.conferencias = []

    def fonte(self, nome, caminho, json_=True, papel=""):
        p = Path(caminho)
        if not p.is_file():
            raise Falha("fonte ausente: %s (%s)" % (nome, p))
        n, h = _sha(p)
        self.fontes[nome] = {"arquivo": p.name, "caminho": str(p), "bytes": n, "sha256": h, "sha16": h[:16], "papel": papel}
        if json_:
            self.dados[nome] = json.loads(p.read_text(encoding="utf-8"))
        return self.dados.get(nome)

    def pegar(self, id_, fonte, chave, como=None, f=None):
        v = _ler_chave(self.dados[fonte], chave, fonte)
        if f is not None:
            v = f(v)
        it = {"valor": v, "fonte": fonte, "chave": chave}
        if como:
            it["como"] = como
        if id_ in self.itens:
            raise Falha("item duplicado: " + id_)
        self.itens[id_] = it
        return v

    def derivar(self, id_, valor, fonte, chave, como):
        if id_ in self.itens:
            raise Falha("item duplicado: " + id_)
        self.itens[id_] = {"valor": valor, "fonte": fonte, "chave": chave, "como": como}
        return valor

    def conferir(self, descricao, ok, detalhe=""):
        self.conferencias.append({"descricao": descricao, "ok": bool(ok), "detalhe": detalhe})
        if not ok:
            raise Falha("conferência reprovada: %s %s" % (descricao, detalhe))


def _tok(c, id_, texto, *tokens):
    for t in tokens:
        c.conferir("%s traz o token %s" % (id_, t), t in str(texto), "")


def _marcadores(texto, versao):
    """Os blocos <!-- INICIO_X_vNNN --> ... <!-- FIM_X_vNNN --> do handoff (a mesma convenção do G1)."""
    out = {}
    for m in re.finditer(r"<!-- INICIO_(\w+) -->\n?(.*?)\n?<!-- FIM_\1 -->", texto, re.S):
        out[m.group(1)] = m.group(2).strip("\n")
    return out


def _git(repo, *args):
    r = subprocess.run(["git", "-c", "core.quotepath=off", "-C", str(repo)] + list(args), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


# ------------------------------------------------------------------------------------------------- a montagem
def montar(cfg):
    """cfg: {nos, espelho, resultado, handoff(opcional)} (Path ou str). Devolve o dict do PRIMORDIAL (sem escrever)."""
    c = Construtor()
    cam = Caminhos()
    nos = Path(cfg.get("nos") or cam.NOS)
    tb = Path(cfg.get("espelho") or cam.TB)
    res_p = Path(cfg.get("resultado") or Path(cam.CEN).joinpath(*RESULTADO_PADRAO))
    # --- as fontes (cada uma com sha256 lido do arquivo, nunca de memória)
    selo = c.fonte("selo", nos / "um_absoluto_selo.json", papel="o selo do rito (identidade, pin, gate)")
    core = c.fonte("core", nos / "um_absoluto.json", papel="o mundo selado (core com os registros)")
    c.dados["core"] = core["core"]
    c.fonte("manifesto_kernel", nos / "tgl_kernel_proof_manifest.json", papel="o manifesto do kernel Lean")
    c.fonte("resultado_fase9_v2", res_p, papel="o resultado da razão de Hubble (Fase 9 V2, aberto uma vez)")
    op_p = Path(cfg.get("operador") or Path(cam.CEN).joinpath(*OPERADOR_PADRAO))
    c.fonte("operador_verbatim", op_p, json_=False, papel="a fala do operador (verbatim) sobre o z_disc, citada como juízo dele")
    c.fonte("um_py", nos / "um.py", json_=False, papel="o artefato único")
    c.fonte("artigo_en", nos / "um_absoluto_en.txt", json_=False, papel="o artigo emitido pelo próprio um.py (EN)")
    c.fonte("citation", tb / "CITATION.cff", json_=False, papel="o depósito citável no Zenodo")
    c.fonte("ledger", tb / "LEDGER.md", json_=False, papel="o livro-razão (append-only)")
    tunel = json.loads((tb / "TUNEL.json").read_text(encoding="utf-8"))
    porta = json.loads((tb / "PORTA.json").read_text(encoding="utf-8"))

    # --- selo
    versao = c.pegar("selo.versao", "selo", "um_version")
    c.conferir("a versão tem a forma vNNN", re.fullmatch(r"v\d{3}", versao) is not None, versao)
    c.pegar("selo.timestamp", "selo", "timestamp")
    pin = c.pegar("selo.pin_um_py", "selo", "sha256/um.py")
    c.pegar("selo.mundo", "selo", "sha256/um_absoluto.json")
    c.pegar("selo.result_hash", "selo", "result_hash")
    gate = c.pegar("selo.gate", "selo", "qg_closure_verdict")
    c.pegar("selo.identity", "selo", "identity")
    c.pegar("selo.selftest", "selo", "fail_closed_selftest")
    c.conferir("o pin do selo é o sha256 do um.py do Nós", c.fontes["um_py"]["sha256"] == pin, "")
    c.derivar("selo.um_py_bytes", c.fontes["um_py"]["bytes"], "um_py", "tamanho do arquivo", "stat")
    c.conferir("o pin do selo é o do PORTA.json e o do TUNEL.json do espelho", porta["selo_corrente"]["pin_um_py"] == pin == tunel["selo"]["pin_um_py"], "")
    c.conferir("o mundo do selo é o sha256 do um_absoluto.json do Nós", c.fontes["core"]["sha256"] == c.itens["selo.mundo"]["valor"], "")
    for nome_tb, nome_nos in (("um.py", "um.py"), ("um_absoluto_selo.json", "um_absoluto_selo.json"), ("um_absoluto.json", "um_absoluto.json"),
                              ("Lean/tgl_kernel_proof_manifest.json", "tgl_kernel_proof_manifest.json")):
        a = (tb / A3 / nome_tb)
        if a.is_file():
            c.conferir("o espelho tem %s byte a byte igual ao do Nós" % nome_tb, _sha(a)[1] == _sha(nos / nome_nos)[1], "")
    # --- kernel
    kf = c.dados["core"]["kernel_formalization"]
    ar = kf["axiom_report"]
    n_decl = c.derivar("kernel.declaracoes", len(ar), "core", "len(kernel_formalization/axiom_report)", "len")
    n_arq = c.derivar("kernel.arquivos_formais", len(kf["formal_files_sha256"]), "core", "len(kernel_formalization/formal_files_sha256)", "len")
    c.conferir("todas as declarações auditadas estão no trio de axiomas", all(set(v) <= TRIO for v in ar.values()), "")
    c.derivar("kernel.todas_no_trio", True, "core", "kernel_formalization/axiom_report (todas ⊆ trio)", "all")
    m = c.dados["manifesto_kernel"]
    c.conferir("o manifesto do kernel concorda com o core (arquivos e declarações)", len(m["formal_files_sha256"]) == n_arq and len(m["axiom_report"]) == n_decl, "")
    c.derivar("kernel.arquivos_lean", sum(1 for k in kf["formal_files_sha256"] if k.endswith(".lean")), "core", "kernel_formalization/formal_files_sha256 (sufixo .lean)", "contagem")
    mv = re.search(r"version ([0-9]+\.[0-9]+\.[0-9]+)", _ler_chave(c.dados["core"], "kernel_formalization/lean_version/0", "core"))
    c.conferir("a versão do Lean se lê do core", mv is not None, "")
    c.derivar("kernel.lean", "leanprover/lean4:v" + mv.group(1), "core", "kernel_formalization/lean_version/0", "regex")
    c.pegar("kernel.modo", "core", "kernel_formalization/mode")
    t3 = "three_stress_tests_v387"
    c.pegar("kernel.escada_limpa", "core", t3 + "/kernel/n_theorems_clean")
    c.pegar("kernel.escada_esperada", "core", t3 + "/kernel/n_theorems_expected")
    c.pegar("kernel.sorry_ausente", "core", t3 + "/kernel/sorryAx_absent")
    c.pegar("kernel.axiomas_proprios_ausentes", "core", t3 + "/kernel/custom_TGL_axioms_absent")
    c.pegar("kernel.bandeiras_true", "core", t3 + "/kernel/gate_flags_true")
    c.pegar("kernel.bandeiras_total", "core", t3 + "/kernel/gate_flags_total")
    v = c.itens
    c.conferir("a escada fecha (limpas = esperadas) e não há sorry nem axioma próprio",
               v["kernel.escada_limpa"]["valor"] == v["kernel.escada_esperada"]["valor"] and v["kernel.sorry_ausente"]["valor"] is True
               and v["kernel.axiomas_proprios_ausentes"]["valor"] is True, "")
    c.conferir("o gate do core e o do selo são o mesmo", c.dados["core"][t3]["kernel"]["gate_verdict"] == gate, "")
    c.conferir("o espelho concorda com o kernel (PORTA.json: arquivos e termos)", int(porta["selo_corrente"]["kernel_arquivos_formais"]) == n_arq
               and int(porta["selo_corrente"]["kernel_teoremas_auditados"]) == n_decl, "")
    # --- o gate e as bandeiras (v403 em diante: 18 calculadas, 0 literais)
    bg = c.dados["core"]["bandeiras_do_gate_v403"]
    c.conferir("bandeiras_do_gate_v403 está verificado", bg["all_verified"] is True, "")
    _tok(c, "bandeiras_do_gate_v403/verdict", bg["verdict"], "ALL_18_FLAGS_ARE_COMPUTED_NONE_IS_A_LITERAL", "GATE_UNMOVED")
    for k in ("n_flags", "n_true", "n_calculated", "n_literal", "n_read_by_the_verdict", "read_by_the_verdict", "informative", "feed_single_boolean"):
        c.pegar("gate." + k, "core", "bandeiras_do_gate_v403/values/" + k)
    c.conferir("as bandeiras do gate fecham com o kernel (18/18; 15 lidas pelo veredito + 3 informativas)",
               v["gate.n_flags"]["valor"] == v["kernel.bandeiras_total"]["valor"] and v["gate.n_true"]["valor"] == v["kernel.bandeiras_true"]["valor"]
               and v["gate.n_read_by_the_verdict"]["valor"] == sum(v["gate.read_by_the_verdict"]["valor"])
               and len(v["gate.informative"]["valor"]) == v["gate.n_flags"]["valor"] - v["gate.n_read_by_the_verdict"]["valor"], "")
    # --- o estatuto da prova (v391): provada como fecho lógico = validade; a confirmação recusada é creditação
    ep = c.dados["core"]["estatuto_da_prova_v391"]
    c.conferir("estatuto_da_prova_v391 está verificado e sem falhas", ep["all_verified"] is True and not ep["falhas"], "")
    _tok(c, "estatuto_da_prova_v391/verdict", ep["verdict"], "PROVED_AS_LOGICAL_CLOSURE", "THREE_PROOFS_COUNT_TOGETHER", "CONFIRMATION_IS_CREDITATION_NOT_VALIDITY", "BETA_IN_NATURE_AWAITS_5_SIGMA")
    c.pegar("estatuto.verdict", "core", "estatuto_da_prova_v391/verdict")
    c.conferir("a certificação do estatuto é o pin do selo", ep["certificacao"]["um_py_sha256_lido_de_si"] == pin, "")
    # --- apoio 2: o livro de cobranças e as rotas do eco
    for k in ("n_charges",):
        c.pegar("ritos.cobrancas_n", "core", t3 + "/ledger/" + k)
    cont = c.dados["core"][t3]["ledger"]["counts"]
    for k in ("FALSIFIED", "NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING"):
        c.pegar("ritos.cobrancas." + k, "core", t3 + "/ledger/counts/" + k)
    c.conferir("as contagens do livro somam as cobranças e nenhuma está FALSIFIED", sum(cont.values()) == c.itens["ritos.cobrancas_n"]["valor"] and cont["FALSIFIED"] == 0, str(cont))
    c.conferir("o gabarito dos três apoios: nenhum falhou", c.dados["core"][t3]["none_of_the_three_failed"] is True and c.dados["core"][t3]["pillars_that_failed"] == [], "")
    eco = c.dados["core"]["the_ledger_of_charges_v383"]["echo_routes_outside_the_ledger"]
    for k in ("n", "excluded_by_data", "inconclusive"):
        c.pegar("ritos.eco." + k, "core", "the_ledger_of_charges_v383/echo_routes_outside_the_ledger/" + k)
    c.conferir("as rotas do eco: excluídas + inconclusivas = n, e não são cobranças da teoria", eco["excluded_by_data"] + eco["inconclusive"] == eco["n"] and eco["not_charges_of_the_theory"] is True, "")
    mg = re.search(r"In the table: (\d+) of (\d+) rite rows in which GR is read return the correspondence", (nos / "um_absoluto_en.txt").read_text(encoding="utf-8"))
    c.conferir("o artigo emitido traz a contagem das linhas em que a RG é lida", mg is not None, "")
    c.derivar("ritos.rg_ok", int(mg.group(1)), "artigo_en", "In the table: N of M rite rows in which GR is read return the correspondence", "regex")
    c.derivar("ritos.rg_n", int(mg.group(2)), "artigo_en", "In the table: N of M rite rows in which GR is read return the correspondence", "regex")
    c.conferir("em todas as linhas em que a RG é lida ela devolve a correspondência", mg.group(1) == mg.group(2), "")
    c.conferir("o artigo emitido lê a resolução da tensão de Hubble como [CONJECTURE] de mecanismo", "a [CONJECTURE] of mechanism" in (nos / "um_absoluto_en.txt").read_text(encoding="utf-8"), "")
    c.derivar("ritos.hubble_mecanismo_conjetura", True, "artigo_en", "contém «a [CONJECTURE] of mechanism»", "busca de texto")
    # --- o piso dos vazios
    vf = c.dados["core"]["void_floor_v11"]
    c.pegar("vazios.veredito", "core", "void_floor_v11/verdict")
    c.pegar("vazios.L5", "core", "void_floor_v11/primary/L5")
    c.pegar("vazios.beta_piso", "core", "void_floor_v11/beta_floor")
    c.pegar("vazios.poder", "core", "void_floor_v11/primary/powered")
    c.conferir("o piso dos vazios: NOT_FALSIFIED_POWERED, limite inferior a 5σ acima de β", vf["verdict"] == "TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED" and vf["primary"]["powered"] is True and vf["primary"]["L5"] > vf["beta_floor"], "")
    c.conferir("o piso dos vazios é unilateral (o ΛCDM raso também o passa), como o core diz",
               all(t in vf["statuses"]["honestidade"] for t in ("unilateral", "LCDM raso")), "")
    # --- D1 (CAMB V3 real)
    d1 = c.dados["core"]["d1_camb_v3_real_v366"]["verdict"]
    md1 = re.search(r"ALPHA_SQRT_E_AT_(\d+)P(\d+)_SIGMA", d1)
    c.conferir("o D1 traz a tensão em σ no veredito e a diz 'não é falsificação'", md1 is not None and "TENSION_IS_NOT_FALSIFI" in d1 and "CHAIN_BELOW_50_TAU" in d1, "")
    c.derivar("d1.tensao_sigma", float("%s.%s" % md1.groups()), "core", "d1_camb_v3_real_v366/verdict (ALPHA_SQRT_E_AT_nPm_SIGMA)", "regex")
    # --- neutrino m2 e a massa
    nu = c.dados["core"]["neutrino_m2"]
    c.pegar("massa.veredito", "core", "neutrino_m2/verdict")
    c.pegar("massa.m2_pred_meV", "core", "neutrino_m2/values/m2_pred_meV")
    c.pegar("massa.tensao_sigma", "core", "neutrino_m2/values/tensao_atual_sigma")
    c.pegar("massa.kill_rule_satisfeita", "core", "neutrino_m2/values/kill_rule_satisfeita")
    c.pegar("massa.escada_primeira", "core", "neutrino_m2/values/escada_datada/0")
    c.pegar("massa.escada_ultima", "core", "neutrino_m2/values/escada_datada/%d" % (len(nu["values"]["escada_datada"]) - 1))
    c.conferir("a massa: ARMED_CONSISTENT, regra de morte (5σ em duas determinações) não satisfeita, tensão abaixo de 5σ",
               nu["verdict"] == "TGL_NU_M2_ARMED_CONSISTENT" and nu["values"]["kill_rule_satisfeita"] is False and nu["values"]["tensao_atual_sigma"] < DEGRAU_CREDITACAO_SIGMA, "")
    pm = c.dados["core"]["ponte_da_massa_v405"]
    c.conferir("ponte_da_massa_v405 está verificado", pm["all_verified"] is True, "")
    _tok(c, "ponte_da_massa_v405/verdict", pm["verdict"], "GIVEN_THE_READINGS_THE_FORM_IS_A_THEOREM", "THE_READINGS_ENTER_AS_DEFINITIONS_NOT_THEOREMS", "THE_UNIT_IS_THE_POSTED_ONE", "ALPHA_IS_MEASURED", "GATE_UNMOVED")
    c.pegar("massa.m_derivada_meV", "core", "ponte_da_massa_v405/values/m_derivada_meV")
    c.pegar("massa.u_posto_eV", "core", "ponte_da_massa_v405/values/u_posto_eV")
    c.pegar("massa.nome_da_pedra", "core", "ponte_da_massa_v405/nome_do_operador")
    c.conferir("a massa derivada pelo kernel é a predição do rito do neutrino", abs(pm["values"]["m_derivada_meV"] - nu["values"]["m2_pred_meV"]) < 1e-12, "")
    # --- o ramo B e o protocolo de colapso (SÓ nome, estatuto e veredito do selo)
    c.pegar("ramoB.veredito", "core", "ramo_b_preregistration_v386/verdict")
    _tok(c, "ramo_b_preregistration_v386/verdict", c.itens["ramoB.veredito"]["valor"], "AWAITING_DATA", "NOTHING_OPENED")
    c.pegar("iald_collapse.nome", "core", "iald_prediction/protocol/version")
    c.pegar("iald_collapse.estatuto", "core", "iald_prediction/protocol/status")
    c.pegar("iald_collapse.veredito", "core", "iald_prediction/verdict")
    c.conferir("IALD_COLLAPSE_V1 entra só por nome, estatuto e veredito do selo (o texto do protocolo não é lido para o PRIMORDIAL)", True, "")
    # --- apoio 3: o pilar quântico na GPU
    g = c.dados["core"][t3]["gpu"]
    for k in ("mode", "T1_injections", "T1_errors", "T2_points", "T2_unique", "T4_instances", "T4_unique", "cpuref_compared", "cpuref_disagreements"):
        c.pegar("gpu." + k, "core", t3 + "/gpu/" + k)
    c.pegar("gpu.placa", "core", "quantum_pillar_v384/summary/env/gpu")
    c.derivar("gpu.spec16", c.dados["core"]["quantum_pillar_v384"]["preregistration"]["spec_sha256"][:16], "core", "quantum_pillar_v384/preregistration/spec_sha256", "sha16")
    c.conferir("o pilar da GPU: tudo único, nenhuma injeção errada, nenhuma discordância com a referência CPU",
               g["T2_unique"] == g["T2_points"] and g["T4_unique"] == g["T4_instances"] and g["T1_errors"] == 0 and g["cpuref_disagreements"] == 0, "")
    c.conferir("o um.py ainda traz a recusa sem GPU (NOT_RUN__GPU_UNAVAILABLE)", b"NOT_RUN__GPU_UNAVAILABLE" in (nos / "um.py").read_bytes(), "")
    # --- Hubble V1 (história) e a pré-inscrição da Fase 9
    h1 = "hubble_ratio_opening_v388/numbers/"
    for k, kk in (("z_disc", "z_disc"), ("z_delta", "z_delta"), ("H0_local_previsto", "H0_local_previsto"), ("media_GLS_locais", "media_GLS_locais"),
                  ("sigma_GLS_locais", "sigma_GLS_locais"), ("beta_hat", "beta_hat"), ("sigma_beta", "sigma_beta")):
        c.pegar("hubble_v1." + k, "core", h1 + kk)
    c.pegar("hubble_v1.lnB_lcdm", "core", h1 + "lnB/TGL_vs_LCDM")
    c.pegar("hubble_v1.veredito", "core", "hubble_ratio_opening_v388/verdict")
    _tok(c, "hubble_ratio_opening_v388/verdict", c.itens["hubble_v1.veredito"]["valor"], "INCONCLUSIVE_SYSTEMATICS", "NOT_DISCRIMINATED_FROM_LCDM_AT_5SIGMA")
    c.derivar("hubble_v1.spec16", c.dados["core"]["hubble_ratio_v387"]["spec_sha256_expected"][:16], "core", "hubble_ratio_v387/spec_sha256_expected", "sha16")
    # --- A RAZÃO DE HUBBLE, Fase 9 V2 (lida do RESULTADO; a regra do 4,44: nunca sozinho)
    r = "resultado_fase9_v2"
    pr = "primario/"
    c.pegar("hubble.id", r, "id")
    c.pegar("hubble.veredito", r, "veredito")
    c.pegar("hubble.veredito_primario", r, pr + "veredito")
    c.pegar("hubble.z_disc", r, pr + "calibracao/z_disc_calibrado")
    c.pegar("hubble.p_disc_unilateral", r, pr + "calibracao/p_calibrado_z_disc_unilateral")
    c.pegar("hubble.z_delta", r, pr + "calibracao/z_delta_calibrado")
    c.pegar("hubble.p_delta_bilateral", r, pr + "calibracao/p_calibrado_z_delta_bilateral")
    c.pegar("hubble.poder_previo", r, pr + "poder_previo_so_sigma")
    c.pegar("hubble.lnB_lcdm", r, pr + "lnB/TGL_vs_LCDM")
    c.pegar("hubble.lnB_beta_livre", r, pr + "lnB/TGL_vs_beta_livre")
    c.pegar("hubble.z_disc_bruto", r, pr + "escores_brutos/z_disc_no_ponto_de_maior_sigma")
    c.pegar("hubble.z_delta_bruto", r, pr + "escores_brutos/z_delta_no_ponto_de_menor_sigma")
    c.pegar("hubble.calibracao", r, pr + "calibracao/modo")
    c.derivar("hubble.recibo_congelamento16", c.dados[r]["pinos"]["recibo_de_congelamento_sha256"][:16], r, "pinos/recibo_de_congelamento_sha256", "sha16")
    c.pegar("hubble.K", r, "beta/K")
    c.pegar("hubble.beta_runtime", r, "beta/beta_runtime")
    c.pegar("hubble.alpha", r, "beta/alpha")
    c.derivar("hubble.degrau_creditacao_sigma", DEGRAU_CREDITACAO_SIGMA, "regua", "o degrau de 5σ da creditação (constante da régua, ordem do operador de 23/10/2026)", "constante")
    mdata = re.search(r"_(\d{4})(\d{2})(\d{2})_", c.itens["hubble.id"]["valor"])
    c.conferir("a data de abertura se lê do id do resultado", mdata is not None, "")
    c.derivar("hubble.data_abertura", "%s-%s-%s" % mdata.groups(), r, "id (AAAAMMDD)", "regex")
    hv = c.itens
    _tok(c, "the_contrast_and_deviation_reading_v378", selo["the_contrast_and_deviation_reading_v378"], "K_EQ_E_ZSTAR_POW_2BETA_OVER_3")
    c.conferir("a razão de Hubble é use-novel (nenhum parâmetro da TGL ajustado ao dado)", _ler_chave(c.dados["resultado_fase9_v2"], "primario/entrada_da_funcao/use_novel_parametros", "resultado") is True, "")
    z, zd, vd = hv["hubble.z_disc"]["valor"], hv["hubble.z_delta"]["valor"], hv["hubble.veredito"]["valor"]
    c.conferir("a regra do 4,44: z_disc está ABAIXO do degrau de 5σ (se não estiver, o texto muda de estatuto: decisão do operador)", z < DEGRAU_CREDITACAO_SIGMA, "z_disc=%.4f" % z)
    c.conferir("o veredito do resultado é o do primário", vd == hv["hubble.veredito_primario"]["valor"], "")
    _tok(c, "hubble.veredito", vd, "NOT_FALSIFIED_POWERED", "NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY", "NOT_BLIND_TO_DATA_STATED", "NOT_A_CONFIRMATION", "GATE_UNTOUCHED")
    c.conferir("β do resultado é α·√e em runtime (CODATA 2018 do resultado × √e)", abs(hv["hubble.alpha"]["valor"] * math.sqrt(math.e) - hv["hubble.beta_runtime"]["valor"]) < 1e-15, "")
    c.conferir("β do resultado é o β do vazio e o da massa (mesma constante)", abs(hv["hubble.beta_runtime"]["valor"] - c.dados["core"]["void_floor_v11"]["beta_floor"]) < 1e-15, "")
    c.conferir("o poder prévio é positivo e z_δ está dentro de 2σ (TGL não falsificada, com poder)", hv["hubble.poder_previo"]["valor"] > 5 and abs(zd) < 2, "")
    lido = c.dados["core"]["teste_de_veracidade_fase9_v397"]["lido"]
    c.conferir("o core selado leu o MESMO resultado (sha256 da fonte f9v2_resultado = o do arquivo)",
               any(f["chave"] == "f9v2_resultado" and f["sha256"] == c.fontes[r]["sha256"] for f in c.dados["core"]["teste_de_veracidade_fase9_v397"]["fontes"]), "")
    c.conferir("os números do core selado (teste_de_veracidade_fase9_v397/lido) são os do resultado",
               all(abs(lido[a] - hv[b]["valor"]) < 1e-12 for a, b in (("z_disc_calibrado", "hubble.z_disc"), ("p_disc_unilateral", "hubble.p_disc_unilateral"),
                                                                       ("z_delta_calibrado", "hubble.z_delta"), ("p_delta_bilateral", "hubble.p_delta_bilateral"),
                                                                       ("poder_previo", "hubble.poder_previo"), ("lnB_lcdm", "hubble.lnB_lcdm"),
                                                                       ("lnB_beta_livre", "hubble.lnB_beta_livre"), ("K", "hubble.K"))), "")
    # --- o que o texto vigente do kernel diz sobre a fundação e o Lema 3 (as notas ao lado dependem disto)
    fu = c.dados["core"]["fundacao_v390"]
    _tok(c, "fundacao_v390/verdict", fu["verdict"], "LOGICAL_CLOSURE_THE_PROGRAM_STAYS_OPEN", "FIELD_EQUATION_IN_CURVED_SPACETIME_NO")
    lc = c.dados["core"]["lei_de_campo_curvo_v392"]
    c.conferir("lei_de_campo_curvo_v392 está verificado e é CONDICIONAL ao H3 nomeado", lc["all_verified"] is True and "KERNEL_TERM_CONDITIONAL_ON_THE_NAMED_H3" in lc["verdict"], "")
    c.conferir("a leitura POSTO do axioma está no selo", "THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED_TAG_POSTO" in selo["the_axiom_reading_v385"], "")
    c.conferir("a pedra da confirmação reservada continua no kernel", "TGLExt/TheReservedConfirmation.lean" in kf["formal_files_sha256"], "")
    # --- o fechamento da versão (v406): o registro do core, para as linhas de máquina
    fk = "fechamento_v406"
    if fk in c.dados["core"]:
        c.conferir("fechamento_v406 está verificado", c.dados["core"][fk]["all_verified"] is True, "")
        for k in ("n_modulos", "n_flags", "n_ancoras_ok"):
            c.pegar("fechamento." + k, "core", fk + "/values/" + k)
        c.pegar("fechamento.certificado_habitado", "core", fk + "/certificate_inhabited")
    # --- a fala do operador sobre o z_disc (verbatim; entra no README como CITAÇÃO ASSINADA do autor, [INPUT], nunca como afirmação do programa)
    ot = op_p.read_text(encoding="utf-8")
    mo = re.search(r"um sigma 4,44 é muito forte, eu nunca vi uma teoria (\S+) qualquer com uma medição dessa", ot)
    c.conferir("a fala do operador sobre o 4,44 está no arquivo verbatim, contígua", mo is not None, "")
    frase = mo.group(0)
    mdt = re.search(r"Operador, (\d{2}/\d{2}/\d{4})", ot)
    c.conferir("o verbatim traz a data da fala", mdt is not None, "")
    c.derivar("operador.frase_4_44", frase, "operador_verbatim", "trecho contíguo «um sigma 4,44 … medição dessa»", "regex")
    c.derivar("operador.frase_4_44_sic", re.sub(r"\b(%s)\b" % "|".join(SIC), lambda m_: m_.group(1) + " [sic]", frase), "operador_verbatim", "o trecho com [sic] nas grafias do original", "marca")
    c.derivar("operador.data", mdt.group(1), "operador_verbatim", "Operador, DD/MM/AAAA", "regex")
    # --- o handoff da versão: «o que mudou nesta versão» (títulos e arcos, verbatim)
    hp = Path(cfg.get("handoff") or (nos / ("HANDOFF_%s_CUSTODIA.md" % versao)))
    c.fonte("handoff", hp, json_=False, papel="o handoff da custódia (de onde vem «o que mudou»)")
    marc = _marcadores(hp.read_text(encoding="utf-8"), versao)
    for k, id_ in (("TITULO_EN", "mudou.titulo_en"), ("ARCO_EN", "mudou.arco_en"), ("ARCO_PT", "mudou.arco_pt")):
        mk = "%s_%s" % (k, versao)
        if mk not in marc:
            raise Falha("o handoff não traz o marcador %s (o «o que mudou» não se inventa)" % mk)
        c.derivar(id_, marc[mk].strip(), "handoff", "marcador INICIO_%s" % mk, "marcador")
    pars = [(k, vv) for k, vv in marc.items() if k.startswith("PARAGRAFO_") and k.endswith("_" + versao)]
    if pars:
        mt = re.search(r"^###\s*(.+?)\s*(?:\u2014|-)\s*par", pars[-1][1], re.M)
        if not mt:
            raise Falha("o parágrafo pronto %s do handoff não tem o título no molde «### <título> — parágrafo pronto»" % pars[-1][0])
        c.derivar("mudou.paragrafo_pronto_titulo", mt.group(1).strip(), "handoff", "título do marcador INICIO_" + pars[-1][0], "regex")
    else:
        c.derivar("mudou.paragrafo_pronto_titulo", None, "handoff", "nenhum marcador PARAGRAFO_*_" + versao, "regex")
    # --- o depósito citável (Zenodo), do CITATION.cff
    cff = (tb / "CITATION.cff").read_text(encoding="utf-8")
    md = re.search(r"Zenodo deposit of (v\d{3}), deposited ([\d-]{10}) \(byte-identical to the seal: um\.py sha256 ([0-9a-f]{16})", cff)
    mdoi = re.search(r'^doi: "(10\.5281/zenodo\.[0-9]+)"', cff, re.M)
    if not (md and mdoi):
        raise Falha("CITATION.cff sem o doi ou sem a linha do depósito (Zenodo deposit of vNNN, deposited AAAA-MM-DD ...)")
    c.derivar("zenodo.versao", md.group(1), "citation", "Zenodo deposit of vNNN", "regex")
    c.derivar("zenodo.data", md.group(2), "citation", "deposited AAAA-MM-DD", "regex")
    c.derivar("zenodo.pin16", md.group(3), "citation", "um.py sha256 (16)", "regex")
    c.derivar("zenodo.doi", mdoi.group(1), "citation", "doi", "regex")
    c.derivar("zenodo.mesmo_selo", md.group(1) == versao, "citation", "zenodo.versao == selo.versao", "comparação")
    # --- o livro-razão (tamanho, linhas, sha256 e a origem no primeiro commit)
    lt = (tb / "LEDGER.md").read_text(encoding="utf-8")
    c.derivar("ledger.bytes", c.fontes["ledger"]["bytes"], "ledger", "tamanho do arquivo", "stat")
    c.derivar("ledger.linhas", lt.count("\n") + (0 if lt.endswith("\n") else 1), "ledger", "linhas", "contagem")
    rc, out = _git(tb, "log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", "LEDGER.md")
    pr_ = out.split()
    if rc != 0 or len(pr_) < 2:
        raise Falha("git log não achou o commit que criou LEDGER.md (a data de origem do livro-razão não se afirma de memória)")
    c0, desde = pr_[-2], pr_[-1]
    rc2, _ = _git(tb, "cat-file", "-e", c0 + ":LEDGER.md")
    r0 = subprocess.run(["git", "-C", str(tb), "show", c0 + ":LEDGER.md"], capture_output=True)
    if rc2 != 0 or not r0.stdout:
        raise Falha("LEDGER.md ilegível no commit que o criou")
    c.derivar("ledger.desde", desde, "ledger", "git log --diff-filter=A (data do commit %s)" % c0, "git")
    c.derivar("ledger.bytes_origem", len(r0.stdout), "ledger", "git show %s:LEDGER.md (bytes)" % c0, "git")
    c.derivar("ledger.linhas_origem", r0.stdout.count(b"\n"), "ledger", "git show %s:LEDGER.md (linhas)" % c0, "git")
    # --- a última custódia PÚBLICA (o commit custodia(vNNN) do espelho; o da Central não entra: o repositório é privado)
    rc, out = _git(tb, "log", "-E", "--grep=^custodia\\(v[0-9]+\\)", "-1", "--format=%H%x09%ad%x09%s", "--date=short")
    cm = out.strip().split("\t")
    if rc == 0 and len(cm) == 3:
        mv_ = re.match(r"custodia\((v\d{3})\)", cm[2])
        c.derivar("custodia.commit_espelho", cm[0], "git_espelho", "git log -1 --grep='^custodia(vNNN)'", "git")
        c.derivar("custodia.versao_do_commit", mv_.group(1) if mv_ else None, "git_espelho", "assunto do commit", "regex")
        c.derivar("custodia.data_do_commit", cm[1], "git_espelho", "data do commit", "git")
    else:
        c.derivar("custodia.commit_espelho", None, "git_espelho", "git log -1 --grep='^custodia(vNNN)'", "git (sem commit)")
    c.fontes["git_espelho"] = {"arquivo": "(git log do espelho)", "caminho": str(tb), "bytes": None, "sha256": None, "sha16": None, "papel": "o commit da última custódia publicada"}
    # --- as portas: as URLs raw de tudo que o README aponta, lidas do TUNEL.json/PORTA.json (nunca digitadas)
    arq = {a["path"]: a for a in tunel["arquivos"]}

    raiz_porta = {d["nome"]: d["url_raw"] for d in porta["arquivos_raiz"]}
    GERADOS_AO_LADO = ("TUNEL.json", "TUNEL.md", "PORTA.json")       # o TUNEL não lista a si mesmo nem as portas da raiz: a URL é raw_base + nome fixo

    def u(path):
        if path in arq:
            return arq[path]["url"], arq[path]["bytes"]
        if path in raiz_porta:
            return raiz_porta[path], None
        if path in GERADOS_AO_LADO:
            return porta["repo_raw_base"] + path, None
        raise Falha("caminho ausente no TUNEL.json e no PORTA.json: " + path)

    sec = [d for d in porta["portas_todas"] if d["pasta"] == "secoes"]
    if len(sec) != 1:
        raise Falha("a porta de secoes/ não está no PORTA.json (rode gerar_portas.py depois do git add)")
    pa = {d["id"]: d for d in porta["portas_abaixo"]}
    for kk in ("artigo_1", "artigo_2", "artigo_3", "genesis"):
        if kk not in pa:
            raise Falha("porta ausente no PORTA.json: " + kk)
    a1 = "O Custo Geométrico do Zero Absoluto — Haja Luz/"
    a2 = "A Ponte-Einstein_Cartan_Miguel/"
    mapa = {
        "llms": "llms.txt", "estado": "ESTADO_ATUAL.md", "brief": "read-brief.md", "tunel_json": "TUNEL.json", "tunel_md": "TUNEL.md", "porta_json": "PORTA.json",
        "porta_md": "PORTA.md", "ledger": "LEDGER.md", "citation": "CITATION.cff",
        "citing": "CITING.md",
        "abstract": "ABSTRACT.md",   # AO LADO (v410, custodia): a Abstract saiu do README (teto L01) para ABSTRACT.md   # AO LADO (06/11/2026, custodia v409, claude-site-custodia): o BibTeX dos artigos saiu do README (teto L01) para CITING.md
        "um_py": A3 + "/um.py", "selo": A3 + "/um_absoluto_selo.json", "mundo": A3 + "/um_absoluto.json", "manifesto": A3 + "/Lean/tgl_kernel_proof_manifest.json",
        "confirmacao_reservada": A3 + "/Lean/tgl_kernel/TGLExt/TheReservedConfirmation.lean",
        "a1_tex": a1 + "paper_PT.tex", "a1_py": a1 + "tgl_paper_unified.py", "a1_pdf": a1 + "paper_PT.pdf",
        "a1_errata": a1 + "ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md",
        "a2_tex": a2 + "A Ponte Einstein Cartan Miguel.tex", "a2_pdf": a2 + "A Ponte Einstein Cartan Miguel.pdf",
        "a3_en_txt": A3 + "/um_absoluto_en.txt", "a3_pt_txt": A3 + "/um_absoluto_pt.txt", "a3_en_pdf": A3 + "/um_absoluto_en.pdf", "a3_pt_pdf": A3 + "/um_absoluto_pt.pdf",
        "a3_arvore": A3 + "/A_PROVA_DA_QG_TGL_arvore.md", "a3_forma": A3 + "/um_absoluto_forma_canonica.md",
    }
    urls = {}
    for k, path in mapa.items():
        url, nb = u(path)
        urls[k] = {"url": url, "bytes": nb if k in ("mundo", "selo", "um_py") else None, "caminho": path}      # bytes só do que o README mostra (os demais mudam a cada laço)
    for k, dd in (("porta_artigo_1", pa["artigo_1"]), ("porta_artigo_2", pa["artigo_2"]), ("porta_artigo_3", pa["artigo_3"]), ("porta_genesis", pa["genesis"]), ("porta_secoes", sec[0])):
        urls[k] = {"url": dd["porta_md_url"], "bytes": None, "caminho": "PORTA.md (%s)" % k}
    base = porta["repo_raw_base"]
    for k, nome in (("pino_readme", "PINO_README.json"), ("primordial_json", "PRIMORDIAL.json")):
        urls[k] = {"url": base + nome, "bytes": None, "caminho": nome}     # nascem na mesma custódia (sem marca de estado: o PRIMORDIAL não pode mudar quando o TUNEL os listar)
    c.derivar("portas.site", porta["site"], "porta", "site", "PORTA.json")
    c.derivar("portas.site_brief", porta["site"].rstrip("/") + "/read-brief.md", "porta", "site + /read-brief.md", "PORTA.json")
    c.derivar("portas.doi_um_absoluto", porta["doi_um_absoluto"], "porta", "doi_um_absoluto", "PORTA.json")
    c.derivar("portas.raw_base", base, "porta", "repo_raw_base", "PORTA.json")
    c.derivar("portas.repo", porta["repo"], "porta", "repo", "PORTA.json")
    c.fontes["porta"] = {"arquivo": "PORTA.json", "caminho": str(tb / "PORTA.json"), "bytes": None, "sha256": None, "sha16": None, "papel": "as portas (URLs, só leitura; o hash dela muda a cada laço e não entra no pino)"}
    c.fontes["tunel"] = {"arquivo": "TUNEL.json", "caminho": str(tb / "TUNEL.json"), "bytes": None, "sha256": None, "sha16": None, "papel": "o índice plano (URLs e tamanhos, só leitura)"}
    c.fontes["regua"] = {"arquivo": "(constante da régua)", "caminho": "", "bytes": None, "sha256": None, "sha16": None, "papel": "o degrau de 5σ da creditação (ordem do operador, 23/10/2026)"}
    # --- PRIMORDIAL
    for nome, f in c.fontes.items():           # o caminho absoluto da máquina não é publicado
        f.pop("caminho", None)
    return {
        "schema": "PRIMORDIAL_V1",
        "aviso": "gerado por tools/custodia_g1/primordial.py; nenhum numero digitado: cada item traz fonte e chave; NOT_FALSIFIED nunca e CONFIRMED",
        "versao": versao,
        "fontes": c.fontes,
        "itens": c.itens,
        "urls": urls,
        "conferencias": c.conferencias,
    }


def serializar(P):
    """Bytes determinísticos (LF, sem carimbo de hora, UTF-8)."""
    return (json.dumps(P, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="gera PRIMORDIAL.json do selo, do core, do manifesto e dos resultados dos ritos")
    ap.add_argument("--saida", required=True, help="pasta de saída (recebe PRIMORDIAL.json)")
    ap.add_argument("--nos", help="pasta do Nós (padrão: a da casa)")
    ap.add_argument("--espelho", help="pasta do espelho the_boundary (padrão: a da casa)")
    ap.add_argument("--resultado", help="RESULTADO_FASE9_V2_*.json (padrão: o da pasta de saídas da Fase 9 V2)")
    ap.add_argument("--handoff", help="HANDOFF_vNNN_CUSTODIA.md (padrão: o do Nós para a versão do selo)")
    ap.add_argument("--operador", help="o verbatim do operador sobre o z_disc (padrão: o de 02/11/2026 em work\\cunhagens_13out)")
    a = ap.parse_args(argv)
    P = montar({"nos": a.nos, "espelho": a.espelho, "resultado": a.resultado, "handoff": a.handoff, "operador": a.operador})
    b = serializar(P)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    alvo = out / "PRIMORDIAL.json"
    if alvo.exists():
        if alvo.read_bytes() == b:
            print("PRIMORDIAL.json inalterado (%d bytes, sha16 %s)" % (len(b), hashlib.sha256(b).hexdigest()[:16]))
            return 0
        bak = out / ("PRIMORDIAL.json.bak_" + __import__("time").strftime("%Y%m%d_%H%M%S"))
        bak.write_bytes(alvo.read_bytes())
        assert bak.read_bytes() == alvo.read_bytes()
    tmp = out / "PRIMORDIAL.json.tmp"
    tmp.write_bytes(b)
    assert tmp.stat().st_size == len(b)
    os.replace(tmp, alvo)
    print("PRIMORDIAL.json: %d itens, %d fontes, %d conferencias, %d bytes, sha16 %s" % (len(P["itens"]), len(P["fontes"]), len(P["conferencias"]), len(b), hashlib.sha256(b).hexdigest()[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

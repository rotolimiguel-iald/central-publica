# -*- coding: utf-8 -*-
"""gerencia c1, 20/11/2026: a R1 da Ponte Cook-Levin. Aplica a ressalva PCL-F1 do parecer do Codex
(revisao_codex\\CODEX_PONTE_COOK_LEVIN_R0\\PARECER.md): a classe «com uma leitura» e' o fecho de SAT por reducao
many-one, agora por termo (o enunciado e a prova sao os do controle do revisor, CheckBridgeR2.one_read_iff_reduces), e
o texto diz o que a classe e' e o que nao e'. Acrescenta dois teoremas que dao sentido as classes (os controles
np_input_alphabet_finite e formula_encoding_injective do mesmo revisor). O custo da leitura passa a ser dito na regua
da teoria (o tempo pago), conforme o adendo do Codex de releitura do custo. Nenhum enunciado da R0 muda (conferido
depois por conferir_enunciados.py). Gera R1_ponte_cook_levin\\PonteCookLevin.lean por trocas EXATAS; copia o
compilador."""
import hashlib, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
R0D = AQUI.parent / "R0_ponte_cook_levin"
R0 = R0D / "PonteCookLevin.lean"
PARECER = AQUI.parents[1] / "revisao_codex" / "CODEX_PONTE_COOK_LEVIN_R0" / "PARECER.md"
ADENDO = AQUI.parents[1] / "revisao_codex" / "CODEX_RELEITURA_CUSTO_KIMI" / "PARECER.md"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


src = R0.read_bytes().decode("utf-8")
assert "\r\n" not in src
s_par, s_r0 = sha(PARECER)[:16], sha(R0)[:16]

ESTATUTO_VELHO = src[src.index("**Estatuto.** [REAL no sandbox]"):src.index("Validade no kernel não é creditação.\n-/")]
ESTATUTO_NOVO = (
    "**Estatuto.** [REAL no sandbox] os termos deste arquivo. [KNOWN] Cook 1971 e Levin 1973, com a simulação polinomial\n"
    "entre máquinas de fita e de pilhas: é o conteúdo da hipótese nomeada `CookLevin`, que entra por citação e não é provada\n"
    "aqui.\n\n"
    "**Na língua clássica.** Para as codificações usuais, com β e a inclinação m fixados antes da entrada, a classe «decidido\n"
    "em tempo polinomial com uma leitura» é o fecho de SAT por redução polinomial many-one\n"
    "(`a_classe_de_uma_leitura_e_o_fecho_de_SAT`, sem Cook–Levin) e por isso coincide com NP por Cook–Levin: a inclusão de NP\n"
    "é `a_ponte_cook_levin`; a volta pede a composição de máquinas TM2, que o Mathlib deixa como `proof_wanted` [KNOWN na\n"
    "língua clássica]. Não é toda a classe P com acesso ao oráculo: só o limiar positivo de uma consulta depois da redução.\n"
    "Com um oráculo que conta soluções, «NP contido em P com o oráculo» é imediato [KNOWN]; o que é da TGL é que o oráculo é\n"
    "o leitor do psíon, por termo do kernel (`o_psion_le_a_soma_normalizada`).\n\n"
    "**O custo da leitura** é contado na régua da teoria: o tempo pago, m·(n+2) passos do relógio β ao preço −ln(1−β) cada\n"
    "(`o_tempo_pago_e_linear`). Não é contado em passos de fita: na língua clássica a leitura é um oráculo, e uma consulta\n"
    "conta um passo.\n\n"
    "**O que este arquivo não prova:** Cook–Levin; a máquina sem leitor (SAT em P na máquina padrão, sem consulta), que segue\n"
    "aberta e não é tocada (Baker–Gill–Solovay 1975 [KNOWN]); o custo da leitura em passos de fita; que um dispositivo físico\n"
    "leia num ato (física: na mecânica quântica padrão o traço normalizado sai com precisão aditiva, Knill–Laflamme 1998\n"
    "[KNOWN]). Com o leitor que só conta vale NP contido em P com o leitor, não a igualdade das duas classes com leitor\n"
    "(E28). ")

INSERE_SENTIDO = (
    "def EmPComUmaLeitura {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L) (c : TGLCoupling) (m : ℕ)\n"
    "    {α Γ : Type} (ea : α → List Γ) (A : α → Prop) : Prop :=\n"
    "  ∃ g : α → FormulaCrua, Nonempty (Turing.TM2ComputableInPolyTime ea codificaFormula g) ∧\n"
    "    ∀ a, A a ↔ 2 ≤ oraculo C c m (codificaFormula (g a))\n")
SENTIDO = (
    "\n"
    "/-- ★ O ALFABETO DE NP É FINITO: a máquina TM2 que testemunha um problema em NP tem alfabeto de entrada finito, e o\n"
    "alfabeto da codificação lhe é equivalente. A premissa `EmNP` de `CookLevin` só vale em alfabeto finito, como no teorema\n"
    "clássico. -/\n"
    "theorem o_alfabeto_de_np_e_finito {α Γ : Type} (ea : α → List Γ) (sep : Γ) (bit : Bool → Γ) (A : α → Prop)\n"
    "    (h : EmNP ea sep bit A) : Finite Γ := by\n"
    "  obtain ⟨V, p, ⟨M⟩, _⟩ := h\n"
    "  letI : Fintype (M.tm.Γ M.tm.k₀) := M.tm.Γk₀Fin\n"
    "  exact Finite.of_equiv (M.tm.Γ M.tm.k₀) M.inputAlphabet\n"
    "\n"
    "/-- ★ A FITA DA FÓRMULA DISTINGUE AS FÓRMULAS: a codificação da fórmula crua é injetiva. -/\n"
    "theorem a_fita_da_formula_e_injetiva : Function.Injective codificaFormula := by\n"
    "  intro a b h\n"
    "  have he : codificaEntrada (a, []) = codificaEntrada (b, []) := by\n"
    "    simp only [codificaEntrada, h]\n"
    "  exact congrArg Prod.fst (codificaEntrada_injetiva he)\n")

INSERE_FECHO = (
    "  obtain ⟨g, hg, hgA⟩ := hCL α Γ ea sep bit A hA\n"
    "  refine ⟨g, hg, fun a => ?_⟩\n"
    "  rw [o_oraculo_le_a_fita]\n"
    "  exact (hgA a).trans (uma_leitura_decide_SATcru C c m hm (g a)).symm\n")
FECHO = (
    "\n"
    "/-- ★★★ A CLASSE DE UMA LEITURA É O FECHO DE SAT: com a inclinação m do relógio β acima de ln 2/β, um problema é\n"
    "decidido em tempo polinomial com uma leitura se, e só se, se reduz a SAT na máquina padrão. Não usa Cook–Levin. -/\n"
    "theorem a_classe_de_uma_leitura_e_o_fecho_de_SAT {L : ImportedSQ.LightOneParticle} (C : ImportedSQ.FockCertificate L)\n"
    "    (c : TGLCoupling) (m : ℕ) (hm : Real.log 2 / c.beta < (m : ℝ)) {α Γ : Type} (ea : α → List Γ) (A : α → Prop) :\n"
    "    EmPComUmaLeitura C c m ea A ↔ ReduzASAT ea A := by\n"
    "  constructor\n"
    "  · rintro ⟨g, hg, hA⟩\n"
    "    refine ⟨g, hg, fun a => ?_⟩\n"
    "    rw [hA a, o_oraculo_le_a_fita]\n"
    "    exact uma_leitura_decide_SATcru C c m hm (g a)\n"
    "  · rintro ⟨g, hg, hA⟩\n"
    "    refine ⟨g, hg, fun a => ?_⟩\n"
    "    rw [hA a, o_oraculo_le_a_fita]\n"
    "    exact (uma_leitura_decide_SATcru C c m hm (g a)).symm\n")

TROCAS = [
    ("# A PONTE COOK–LEVIN (candidata da gerência c1, R0; nome provisório, das palavras do operador)\n",
     ("# A PONTE COOK–LEVIN (candidata da gerência c1, R1; nome provisório, das palavras do operador)\n\n"
      "[A R1 aplica a ressalva PCL-F1 da revisão do Codex (`C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v413\\"
      "revisao_codex\\CODEX_PONTE_COOK_LEVIN_R0\\PARECER.md`, sha16 `%s`): a classe «com uma leitura» é o fecho de SAT por\n"
      "redução, agora por termo, e o texto diz o que a classe é e o que não é; acrescenta dois teoremas que dão sentido às\n"
      "classes. Nenhum enunciado da R0 (sha16 `%s`) mudou.]\n") % (s_par, s_r0)),
    ("  SAT, Cook–Levin como hipótese nomeada, e «decidido em tempo polinomial com uma leitura do leitor da TGL».\n",
     "  SAT, Cook–Levin como hipótese nomeada, e «decidido em tempo polinomial com uma leitura do leitor da TGL»; o que dá\n"
     "  sentido às classes: o alfabeto de NP é finito, e a fita da fórmula distingue as fórmulas.\n"),
    ("* §5 Os teoremas: SAT em NP (a máquina TM2 do verificador), SAT com uma leitura e A PONTE: com Cook–Levin, todo\n"
     "  problema em NP é decidido em tempo polinomial com uma leitura; no certificado de Fock físico do kernel.\n",
     "* §5 Os teoremas: SAT em NP (a máquina TM2 do verificador), SAT com uma leitura, A PONTE (com Cook–Levin, todo\n"
     "  problema em NP é decidido em tempo polinomial com uma leitura) e a classe de uma leitura como o fecho de SAT por\n"
     "  redução (sem Cook–Levin); no certificado de Fock físico do kernel.\n"),
    (ESTATUTO_VELHO, ESTATUTO_NOVO),
    ("uma fórmula na fita de consulta; o oráculo da leitura lê a palavra; o problema é o sim do limiar 2 da resposta. -/\n",
     "uma fórmula na fita de consulta; o oráculo da leitura lê a palavra; o problema é o sim do limiar 2 da resposta. Na\n"
     "língua clássica, é o fecho de SAT por redução polinomial many-one (`a_classe_de_uma_leitura_e_o_fecho_de_SAT`): só o\n"
     "limiar positivo de uma consulta depois da redução, não toda a classe P com acesso ao oráculo. -/\n"),
    (INSERE_SENTIDO, INSERE_SENTIDO + SENTIDO),
    (INSERE_FECHO, INSERE_FECHO + FECHO),
    ("#print axioms TGLExt.PonteCookLevin.a_ponte_cook_levin\n",
     "#print axioms TGLExt.PonteCookLevin.o_alfabeto_de_np_e_finito\n"
     "#print axioms TGLExt.PonteCookLevin.a_fita_da_formula_e_injetiva\n"
     "#print axioms TGLExt.PonteCookLevin.a_ponte_cook_levin\n"
     "#print axioms TGLExt.PonteCookLevin.a_classe_de_uma_leitura_e_o_fecho_de_SAT\n"),
]
novo = src
for antes, depois in TROCAS:
    assert novo.count(antes) == 1, "trecho nao achado exatamente uma vez: %r" % antes[:90]
    novo = novo.replace(antes, depois)


def grava(dest, dados):
    tmp = dest.with_name(dest.name + ".tmp")
    tmp.write_bytes(dados)
    assert tmp.read_bytes() == dados
    tmp.replace(dest)


grava(AQUI / "PonteCookLevin.lean", novo.encode("utf-8"))
grava(AQUI / "compilar.py", (R0D / "compilar.py").read_bytes())
print("R0 sha16 %s -> R1 sha16 %s | %d -> %d B | parecer sha16 %s | adendo sha16 %s" % (
    s_r0, sha(AQUI / "PonteCookLevin.lean")[:16], len(src.encode("utf-8")), len(novo.encode("utf-8")), s_par,
    sha(ADENDO)[:16]))

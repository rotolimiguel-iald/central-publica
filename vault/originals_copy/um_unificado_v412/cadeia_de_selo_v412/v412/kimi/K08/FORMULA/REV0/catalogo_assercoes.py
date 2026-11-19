#!/usr/bin/env python3
"""Catálogo literal K08: somente afirmações dos quatro textos públicos permitidos.

Cada asserção atômica é uma cláusula unitária. Relações de derivação explicitamente
escritas na fonte ficam em cláusulas próprias. A variável leitura_pt é livre: a
fonte disponibiliza PT/EN, mas não escolhe a língua de uma leitura experimental.
"""
from pathlib import Path

PUBLICO = Path(r"C:\IALD\Artigo\the_boundary")
FORMULA_DIR = Path(__file__).resolve().parent
ENTRADA_DIR = FORMULA_DIR.parent / "ENTRADA"

ATOMOS = {
    "beta_forma": "β_TGL é igual a α·√e",
    "beta_runtime": "β é calculado em runtime e não é um literal",
    "alpha_input": "α é insumo conhecido/declarado na derivação",
    "alpha_livre_aberto": "o valor α-livre permanece aberto",
    "alpha_livre_nao_confirmavel": "a ausência de derivação α-livre não é confirmável",
    "axioma_um": "ω(I) = 1 é o axioma/Um posto",
    "fronteira_autoconjugada": "a fronteira é autoconjugada, com x = 1 − x",
    "meia_nat": "a Meia-Nat é S_∂ = ½ nat",
    "smatrix_beta": "a matriz-S de fronteira tem |R|² = β",
    "dephasing_lei": "a lei de dephasing é Γ_ω = ½βτ★ω²",
    "eom_xi": "a EOM usa ξ = 1/6, e não β",
    "gksl_l": "o objeto não unitário é L = √β·√K_∂",
    "breuer_piso": "H = −log ρ⋆ é limitado inferiormente",
    "um_unico": "um.py é apresentado como artefato/arquivo único",
    "um_verifica_escreve": "um.py verifica a teoria e emite seu próprio artigo",
    "um_entrada_um": "a entrada humana indicada para um.py é o dígito 1",
    "artigo_pt_en": "o artigo é disponibilizado em PT e EN",
    "proved_validade": "PROVED/PROVADA denota validade na definição do operador",
    "qg_tres_apoios": "a gravidade quântica é dita provada como validade em três apoios",
    "kernel_implicacao": "o kernel prova a implicação a partir do Um e das hipóteses, não a natureza",
    "confirm_creditacao": "CONFIRMED é creditação por observadores externos",
    "maquina_autoconfirma": "a máquina confirma a si mesma",
    "nf_eq_confirmed": "NOT_FALSIFIED é equivalente a CONFIRMED",
    "h0_6sigma": "o teste H0DN × BG1 reporta 6,11σ da razão 1 e −0,61σ da lei",
    "h0_k_7427": "a lei K leva o fundo ao valor local 74,27",
    "retrodicao_nao_cega": "o resultado é retrodição sem ajuste, declarada não cega",
    "ritos_0_de_11": "as cobranças dos ritos somam 0 falsificadas em 11",
    "gpu_computa": "o sistema aberto é calculado na GPU, com o estatuto COMPUTED",
    "p_np_com_leitor": "P = nP com o leitor é PROVED como validade no kernel",
    "escala_zero_um": "com constante de escala zero, toda leitura é 1",
    "nome_singularidade": "unicidade de x com P(x) equivale à singularidade por igualdade",
    "ponte_condicional": "a ponte/equação de campo tem fechamento condicional",
    "mais_sensivel_revisa": "dados mais sensíveis podem revisar o veredito",
    "leitura_pt": "a leitura experimental escolhida é a edição PT",
}

# signo +1: o texto afirma o átomo; signo -1: o texto afirma sua negação.
def A(atomo, linha, ancora, signo=1):
    return {"atomo": atomo, "linha": linha, "ancora": ancora, "signo": signo}


def D(literals, linha, ancora):
    """Cláusula não unitária; literals = [(átomo, signo), ...]."""
    return {"literals": literals, "linha": linha, "ancora": ancora}


FONTES = {
    "ABSTRACT": {
        "arquivo": "ABSTRACT.md",
        "rotulo": "ABSTRACT — régua corrente",
        # O recorte mantém o Abstract e as duas correções de régua, sem os títulos vazios.
        "faixas": [(7, 43)],
        "assercoes": [
            A("beta_forma", 11, "\\beta_{\\text{TGL}} = \\alpha \\times \\sqrt{e}"),
            A("beta_runtime", 13, "never hard-coded"),
            A("axioma_um", 15, "`ω(I) = 1`"),
            A("meia_nat", 14, "`S_∂ = ½` nat"),
            A("smatrix_beta", 15, "`|R|² = β`"),
            A("dephasing_lei", 15, "`Γ_ω = ½βτ★ω²`"),
            A("um_unico", 21, "self-contained and single"),
            A("um_verifica_escreve", 23, "machine-checks it and writes its own article"),
            A("artigo_pt_en", 23, "PT/EN"),
            A("proved_validade", 43, "PROVED is read in the operator’s definition of proof"),
            A("qg_tres_apoios", 43, "on three supports that count together"),
            A("kernel_implicacao", 41, "What is proved is the implication from the axiom and the named hypotheses"),
            A("confirm_creditacao", 43, "CONFIRMED = accreditation"),
            A("maquina_autoconfirma", 36, "forbidden by construction", -1),
            A("nf_eq_confirmed", 26, "NOT_FALSIFIED ≠ CONFIRMED", -1),
            A("mais_sensivel_revisa", 31, "MORE_SENSITIVE_DATA_COULD_REVISE"),
        ],
        "derivacoes": [
            D([("axioma_um", -1), ("meia_nat", 1)], 14, "itself derived from the single axiom"),
        ],
    },
    "READ_BRIEF": {
        "arquivo": "read-brief.md",
        "rotulo": "read-brief — estatuto, oito partes e limites",
        "faixas": [(15, 28), (76, 83)],
        "assercoes": [
            A("beta_forma", 22, "β = α·√e ≈ 0.0120313"),
            A("beta_runtime", 16, "β = α·√e is computed at runtime, never a literal"),
            A("alpha_input", 22, "α `[KNOWN]`"),
            A("alpha_livre_aberto", 22, "the α-free value stays `[OPEN]`"),
            A("axioma_um", 21, "The single axiom is ω(I) = 1"),
            A("fronteira_autoconjugada", 21, "self-conjugate boundary x = 1 − x"),
            A("meia_nat", 21, "Half-Nat S_∂ = ½ nat"),
            A("eom_xi", 23, "with ξ = 1/6 the conformal value, not β"),
            A("gksl_l", 25, "The only non-unitary object is L = √β·√K_∂"),
            A("dephasing_lei", 25, "Γ_ω = ½·β·τ★·ω²"),
            A("breuer_piso", 24, "H = −log ρ⋆ is bounded below"),
            A("um_unico", 27, "One file, 46.828.680 bytes"),
            A("um_verifica_escreve", 16, "the article emitted"),
            A("um_entrada_um", 27, "whose only input is `1`"),
            A("artigo_pt_en", 28, "article as text, EN"),
            A("proved_validade", 26, "PROVED in the operator’s definition of proof"),
            A("qg_tres_apoios", 26, "on three supports that count together"),
            A("kernel_implicacao", 26, "the implication, not nature"),
            A("confirm_creditacao", 16, "CONFIRMED = accreditation"),
            A("maquina_autoconfirma", 16, "The machine never issues it about itself", -1),
            A("nf_eq_confirmed", 16, "`NOT_FALSIFIED ≠ CONFIRMED`", -1),
            A("h0_6sigma", 15, "6.11σ away"),
            A("retrodicao_nao_cega", 15, "A retrodiction with nothing fitted to the data"),
            A("ritos_0_de_11", 15, "11 charges: 0 falsified"),
            A("gpu_computa", 15, "the theory’s open system computed on the GPU"),
            A("mais_sensivel_revisa", 80, "more sensitive data can revise"),
        ],
        "derivacoes": [
            D([("fronteira_autoconjugada", -1), ("meia_nat", 1)], 21, "follows from the self-conjugate boundary"),
        ],
    },
    "LLMS": {
        "arquivo": "llms.txt",
        "rotulo": "llms — sumário, programa, falsificação e régua",
        "faixas": [(3, 5), (47, 61), (117, 173)],
        "assercoes": [
            A("beta_forma", 3, "beta_TGL = alpha*sqrt(e)"),
            A("beta_runtime", 3, "nunca literal"),
            A("alpha_livre_nao_confirmavel", 156, "a sua ausencia e' NAO-CONFIRMAVEL por construcao"),
            A("axioma_um", 3, "um axioma, omega(I) = 1"),
            A("um_unico", 59, "Nao ha segundo arquivo"),
            A("um_entrada_um", 59, "roda com `echo 1 | python um.py`"),
            A("artigo_pt_en", 61, "o artigo emitido pelo um.py, em TEXTO"),
            A("proved_validade", 5, "PROVADA na definicao de prova do operador"),
            A("qg_tres_apoios", 5, "em tres apoios que contam juntos"),
            A("kernel_implicacao", 5, "o kernel Lean prova a IMPLICACAO"),
            A("confirm_creditacao", 5, "confirmar e' CREDITAR"),
            A("maquina_autoconfirma", 5, "a maquina nunca o emite sobre si mesma", -1),
            A("nf_eq_confirmed", 5, "NOT_FALSIFIED nunca e' CONFIRMED", -1),
            A("h0_6sigma", 5, "6,11 sigma"),
            A("retrodicao_nao_cega", 5, "declarada nao cega"),
            A("ritos_0_de_11", 5, "11 cobrancas: 0 falsificadas"),
            A("gpu_computa", 5, "o sistema aberto da teoria e' calculado na GPU"),
            A("ponte_condicional", 51, "fechamento CONDICIONAL"),
            A("mais_sensivel_revisa", 159, "MORE_SENSITIVE_DATA_COULD_REVISE"),
        ],
        "derivacoes": [],
    },
    "README": {
        "arquivo": "README.md",
        "rotulo": "README — resultado, estatuto, artigos e núcleo",
        "faixas": [(7, 8), (15, 44), (136, 187), (246, 246)],
        "assercoes": [
            A("beta_forma", 163, "β_TGL = α√e ≈ 0.012031"),
            A("beta_runtime", 163, "β is **never a literal**"),
            A("alpha_input", 163, "α is **[INPUT]**"),
            A("axioma_um", 161, "`ω(I) = 1`"),
            A("fronteira_autoconjugada", 162, "the boundary is self-conjugate"),
            A("meia_nat", 162, "`S_∂ = ½` nat"),
            A("smatrix_beta", 167, "`\\|R\\|² = β`"),
            A("dephasing_lei", 168, "`Γ_ω = ½βτ★ω²`"),
            A("um_unico", 15, "Não há segundo arquivo"),
            A("um_verifica_escreve", 15, "checks it in an embedded Lean kernel and writes its own article"),
            A("um_entrada_um", 15, "From the human input `1`"),
            A("artigo_pt_en", 142, "article as text [EN]"),
            A("proved_validade", 36, "PROVED = validity"),
            A("qg_tres_apoios", 17, "on three supports that count together"),
            A("kernel_implicacao", 40, "the implication from the posited One"),
            A("confirm_creditacao", 36, "CONFIRMED is accreditation"),
            A("maquina_autoconfirma", 36, "never issued by the machine about itself", -1),
            A("nf_eq_confirmed", 246, "NOT_FALSIFIED ≠ CONFIRMED", -1),
            A("h0_6sigma", 7, "6.11σ"),
            A("h0_k_7427", 7, "to **74.27** for the local one"),
            A("retrodicao_nao_cega", 7, "declared not blind"),
            A("ritos_0_de_11", 41, "11 charges: 0 falsified"),
            A("gpu_computa", 42, "the theory’s open system computed on an NVIDIA GeForce RTX 5090"),
            A("p_np_com_leitor", 20, "P = nP of Turing"),
            A("escala_zero_um", 26, "With the constant of the scale equal to 0"),
            A("nome_singularidade", 26, "there is a unique x with P(x) if and only if"),
            A("ponte_condicional", 169, "REAL]** as a **conditional** closure"),
            A("mais_sensivel_revisa", 183, "can revise it"),
        ],
        "derivacoes": [
            D([("fronteira_autoconjugada", -1), ("meia_nat", 1)], 162, "self-conjugate (`𝒞² = 1`"),
            D([("axioma_um", -1), ("meia_nat", 1)], 162, "it descends from the axiom"),
            D([("meia_nat", -1), ("beta_forma", 1)], 163, "`½` nat ⟹ `Vol_∂^min = √e` ⟹"),
        ],
    },
}


def linhas_fonte(nome):
    cfg = FONTES[nome]
    return (PUBLICO / cfg["arquivo"]).read_text(encoding="utf-8").splitlines()


def validar_catalogo():
    """Falha fechada: âncora, faixa e átomo precisam ser literais e declarados."""
    erros = []
    for nome, cfg in FONTES.items():
        linhas = linhas_fonte(nome)
        permitidas = {n for a, b in cfg["faixas"] for n in range(a, b + 1)}
        for grupo in ("assercoes", "derivacoes"):
            for i, item in enumerate(cfg[grupo], 1):
                prefixo = nome if grupo == "assercoes" else nome + "D"
                item["id"] = f"{prefixo}{i:02d}"
                linha = item["linha"]
                if linha not in permitidas:
                    erros.append(f"{item['id']}: linha {linha} fora do recorte")
                if not (1 <= linha <= len(linhas)):
                    erros.append(f"{item['id']}: linha inexistente")
                    continue
                if item["ancora"] not in linhas[linha - 1]:
                    erros.append(f"{item['id']}: âncora ausente na linha {linha}: {item['ancora']!r}")
                atoms = [item["atomo"]] if grupo == "assercoes" else [a for a, _ in item["literals"]]
                for atomo in atoms:
                    if atomo not in ATOMOS:
                        erros.append(f"{item['id']}: átomo não declarado: {atomo}")
        if not any(a["atomo"] == "artigo_pt_en" for a in cfg["assercoes"]):
            erros.append(f"{nome}: falta a base literal da variável livre PT/EN")
        if not any(a["atomo"] == "beta_forma" and a["signo"] == 1 for a in cfg["assercoes"]):
            erros.append(f"{nome}: falta beta_forma para o controle P-C")
    if erros:
        raise ValueError("\n".join(erros))


def texto_compacto(nome):
    """Recorte verbatim; só emende linhas das faixas declaradas, sem texto novo."""
    cfg = FONTES[nome]
    linhas = linhas_fonte(nome)
        # Uma linha em branco entre faixas é separador tipográfico, não asserção.
    partes = []
    for a, b in cfg["faixas"]:
        partes.append("\n".join(linhas[a - 1:b]))
    return "\n\n".join(partes) + "\n"


validar_catalogo()

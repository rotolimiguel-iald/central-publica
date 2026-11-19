# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: o metodo de 17/11 nos comentarios das duas ultimas pedras do Kimi que entram por ordem do autor
(ORazaoDoColapsoEBeta; OCustoEAIsometria), nas copias de trabalho de pedras_novas\\. Sai a linha de estado, a secao De onde vem com
citacoes e atribuicoes, o gate e o balanco; a leitura entra como definicao da teoria, sem atribuicao; beta e' parametro. Trocas por
regiao e exatas; confere codigo identico ao da fonte do autor e ausencia de residuos. So' trata os modulos presentes em pedras_novas.
Uso: nona_lista_passo2g_cabecalhos_do_colapso_e_da_isometria.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
PLANO = {
 "ORazaoDoColapsoEBeta": {
  "regioes": [
   ("[candidata do Kimi, 18/11/2026, R0;", "## O que fica provado",
    "## A leitura que este arquivo tipa\n\nO colapso é a razão do polinômio existir: sem o pagamento, o ciclo não fecha; com o passo `1 − β`, o ciclo fecha em\n"
    "linha na carga, para toda fórmula [INPUT/ONTO: definição da teoria, entrada, não teorema]. Este arquivo prova a parte\n"
    "dela que cabe nos termos do kernel, na máquina da teoria.\n\n"),
   ("* «A razão do colapso IALD» como razão do ser", "-/\n\nnamespace TGLExt.ORazaoDoColapsoEBeta",
    "* Que o colapso seja a razão do ser do polinômio: é definição da teoria [INPUT/ONTO]. O termo é a conjunção do item 3,\n"
    "  na família de passos de fator `1 − β`: com `β = 0` (nenhum pagamento), nenhum número de passos fecha o ciclo para\n"
    "  toda fórmula; com `β` entre 0 e 1, bastam `k > n·ln 2/β` passos.\n"
    "* Que a IALD seja a forma matricial do polinômio lida em runtime, e o que ela representa na fórmula de von Neumann: é\n"
    "  leitura da teoria [INPUT/ONTO]. Nenhum termo deste arquivo trata de matrizes, de runtime ou da fórmula de von\n"
    "  Neumann; β é parâmetro real, e a identificação com o β da teoria é entrada.\n"
    "* Os passos são atos sobre o todo, não movimentos de cabeça na fita: a régua do Instituto fica com a sua contagem.\n"
    "* Nada sobre a natureza.\n"),
  ],
  "trocas": [
   ("todas as fórmulas (a pedra `OPassoEOFim` da gerência).", "todas as fórmulas (é `OPassoEOFim.com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`)."),
   ("2. ★ `com_colapso_ha_fim_linear`: com o fator `1 − β`, bastam `k > n·ln 2 / β` passos para toda fórmula.",
    "2. ★ `com_colapso_ha_fim_linear`: com o fator `1 − β`, bastam `k > n·ln 2 / β` passos para toda fórmula (é\n   `OPassoEOFim.bastam_passos_lineares`)."),
   ("3. ★★ `a_razao_do_colapso`: a conjunção — **o polinômio existe porque o colapso paga**: sem o colapso, o ciclo não\n   fecha; com o passo `1 − β_TGL`, o ciclo fecha em linha na carga. O colapso é a razão do polinômio existir.",
    "3. ★★ `a_razao_do_colapso`: a conjunção dos dois, para o mesmo `n` e o mesmo número de passos: sem o pagamento, o\n   ciclo não fecha para toda fórmula; com o passo `1 − β`, fecha em linha na carga."),
   ("/-- ★★ **A RAZÃO DO COLAPSO**: o polinômio existe porque o colapso paga. Sem o pagamento, o ciclo não fecha para\ntoda fórmula;",
    "/-- ★★ **A RAZÃO DO COLAPSO**: sem o pagamento, o ciclo não fecha para\ntoda fórmula;"),
  ]},
 "OCustoEAIsometria": {
  "regioes": [
   ("[candidata do Kimi, 18/11/2026, R0;", "## O que fica provado",
    "## A leitura que este arquivo tipa\n\nO custo é a carga, a isometria: a contagem da leitura é a sua própria carga [INPUT/ONTO: definição da teoria,\n"
    "entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel, na máquina da teoria.\n\n"),
   ("* «A isometria» é o nome do operador para a carga", "-/\n\nnamespace TGLExt.OCustoEAIsometria",
    "* “A isometria” é nome da teoria para a carga [INPUT/ONTO]; o termo é o logaritmo do número de configurações.\n"
    "* A régua do Instituto (movimentos de cabeça na fita) fica com a sua contagem; aqui a contagem é por atos sobre o\n"
    "  todo.\n"
    "* Nada sobre a natureza.\n"),
  ],
  "trocas": [
   ("   tempo pago passa da carga, nem mais, nem menos (a pedra `AContagemEACarga` da gerência).",
    "   tempo pago passa da carga, nem mais, nem menos (é `AContagemEACarga.a_contagem_e_a_carga_para_formulas`)."),
   ("2. ★ `a_isometria_e_a_carga`: a carga é a isometria — o logaritmo do número de configurações: `n·ln 2` para `n`\n   variáveis, e o limiar da leitura normalizada é `e^{−carga}`.",
    "2. ★ `a_isometria_e_a_carga`: a carga é o logaritmo do número de configurações, `n·ln 2` para `n` variáveis, e o\n   limiar da leitura normalizada é `e^{−carga}`."),
   ("   e uma leitura (a pedra `AMaquinaEALeitura` da gerência).", "   e uma leitura (é `AMaquinaEALeitura.a_maquina_e_uma_leitura_decidem`)."),
   ("4. ★★ `o_custo_total_e_a_carga_por_ato`: os atos da leitura são `|φ| + 2`; cada ato sobre o todo pagando a carga, o\n   custo total é `(|φ| + 2)·n·ln 2`; cada ato pagando um, é `|φ| + 2`. As duas formas são polinomiais na carga.",
    "4. ★★ `o_custo_total_e_a_carga_por_ato`: os atos da leitura são `|φ| + 2`, e esse número de atos vezes a carga é\n   `(|φ| + 2)·n·ln 2`. Que cada ato sobre o todo pague a carga é a lei do custo, tomada como entrada; a conta é a de\n   `Token2.o_custo_pela_lei_e_polinomial`."),
  ]},
}


def sem_comentarios(t):
    out, i, n, prof = [], 0, len(t), 0
    while i < n:
        if t.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and t.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if t.startswith("--", i):
            while i < n and t[i] != "\n":
                i += 1
            continue
        out.append(t[i]); i += 1
    return "\n".join(l.rstrip() for l in "".join(out).split("\n") if l.strip())


RESIDUOS = ("«", "operador", "Kimi", "gerência", "18/11", "16/11", "candidata", "instalado", "Sem sorry", "gate", "a casa", "De onde vem", "custódia")
feitos = {}
for nome, pl in PLANO.items():
    f = D / (nome + ".lean")
    if not f.exists():
        print(nome, "| ainda nao esta' em pedras_novas: pulado"); continue
    orig = (O / (nome + ".lean")).read_bytes().decode("utf-8"); t = f.read_bytes().decode("utf-8")
    if t == orig:
        for ini, fim, novo in pl["regioes"]:
            assert t.count(ini) == 1 and t.count(fim) == 1, (nome, t.count(ini), t.count(fim), ini[:50])
            a, b = t.index(ini), t.index(fim); assert a < b
            t = t[:a] + novo + t[b:]
        for velho, novo in pl["trocas"]:
            assert t.count(velho) == 1, (nome, t.count(velho), velho[:60])
            t = t.replace(velho, novo)
    assert sem_comentarios(orig) == sem_comentarios(t), "codigo difere: " + nome
    for r in RESIDUOS:
        assert r not in t, "sobrou em %s: %s" % (nome, r)
    feitos[nome] = t
    print(nome, "| codigo identico | bytes", len(orig.encode("utf-8")), "->", len(t.encode("utf-8")), "| sha16", hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
if EXEC:
    for nome, t in feitos.items():
        f = D / (nome + ".lean"); b = t.encode("utf-8")
        if f.read_bytes() != b:
            tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
    p = D / "EMENDAS_DO_COLAPSO_E_DA_ISOMETRIA.json"; tmp = p.with_name(p.name + ".tmp_c1")
    tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "plano": PLANO,
                                "sha256_depois": {n: hashlib.sha256((D / (n + ".lean")).read_bytes()).hexdigest() for n in feitos}}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
    print("gravado:", p.name)

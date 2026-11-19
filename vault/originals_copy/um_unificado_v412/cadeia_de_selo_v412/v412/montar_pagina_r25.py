# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R25 = a R24 com (a) as emendas de alcance do parecer da ordem 034 (REVISAO_034_Y4_Codex.md) nos
paragrafos do Tetelestai e de von Neumann: as hipoteses de beta (beta < 1 no "se e so' se"; 0 < beta < 1 no limiar suficiente); o
limiar suficiente e o orcamento inteiro floor(p(n)) + 1, sem minimalidade; m (as clausulas) e k (os passos da soma lida) separados, com
m + 2 atos; com o fator 1, nenhum k decide todas as formulas; a carga como limiar exato (no tempo igual a' carga ja' ha' formula que a
leitura nao decide); o estado uniforme de a_trava_no_nome; o que the_angle_is_prior prova e que ele nao fixa o angulo fisico nem o
identifica com beta; a leitura de Born no caso de um posto (cos^2 theta); os dois sentidos do limite assintotico com o vetor projetado,
que pode ser zero; e (b) a definicao do autor "o ato e' a comutacao" (fala de 18/11), com o termo a_contagem_e_do_operador
(AMaquinaEALeitura) e as duas reguas ditas. A frase do autor sobre a IALD fica byte a byte, conferida de novo contra os bytes da fala.
Confere cada termo citado como theorem na fonte (lista final R12 e kernel selado) e repete a conferencia da tabela sobre a R12.
Uso: montar_pagina_r25.py [--previa <arquivo>] [--executar]  (grava o_que_fica_claro_REV25\\O_QUE_FICA_CLARO_v412_R25.md; nao sobrescreve)"""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; R12 = V / "insumos" / "pedras_r12"; K = Path(r"C:\t\k411c\final\TGLExt")
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
p24 = V / "o_que_fica_claro_REV24" / "O_QUE_FICA_CLARO_v412_R24.md"; assert sha16(p24) == "4869b970c17eacf4"
assert sha16(V / "insumos" / "MANIFESTO_PEDRAS_v412_R12.json") == "1028adf7293b432f"
FALA = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_18nov_iald_e_o_nome_da_forma_matricial_do_polinomio_dos_passos_identidade_da_maquina_preservada_com_texto_do_kimi_colado_verbatim.txt")
f = FALA.read_bytes().decode("utf-8"); i = f.index("IALD é o nome, porque tudo tem NOME"); j = f.index("betatgl como limite assintótico", i) + len("betatgl como limite assintótico")
AUTOR = "Definição da teoria: " + f[i:j].replace("tudo tem NOME", "tudo tem Nome").replace("betatgl", "β") + "."
FALA2 = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_18nov_pra_mim_o_ato_e_a_comutacao_com_resumo_do_codex_da_ordem_034_e_texto_colado_verbatim.txt")
assert hashlib.sha256(FALA2.read_bytes()).hexdigest().startswith("13289201408b8835") and "pra mim o ato é a comutação" in FALA2.read_bytes().decode("utf-8")
t = p24.read_bytes().decode("utf-8")
blocos = t.split("\n\n")
velho_t = [b for b in blocos if b.startswith("**Tetelestai: a consumação do ciclo.**")]; velho_v = [b for b in blocos if b.startswith("**A IALD na fórmula de von Neumann.**")]
assert len(velho_t) == 1 and len(velho_v) == 1 and velho_v[0].count(AUTOR) == 1
T_NOVO = (
 "**Tetelestai: a consumação do ciclo.** Definição da teoria: Tetelestai é a consumação cíclica do processamento mecânico que permite "
 "resposta coerente, a conferência que devolve consumado ou não consumado. Na máquina da teoria, a forma dela está em termo. O mecanismo "
 "de processamento por circuito chega ao ponto fixo e à seleção depois de m aplicações do ato levantado, m o número de cláusulas, e "
 "então responde se a fórmula tem solução (`ha_o_mecanismo`); com a preparação e a leitura, são m + 2 atos "
 "(`o_custo_total_e_a_carga_por_ato`). Um segundo teste, o da soma lida, usa outro parâmetro, o número k de passos de fator `1 − β`: "
 "com β < 1, a soma depois de k passos decide toda fórmula de n variáveis se e só se os passos pagam a carga, "
 "n·ln 2 < k·(−ln(1 − β)) (`o_passo_um_menos_beta_fecha_o_ciclo`); com 0 < β < 1, basta qualquer número inteiro de passos acima de "
 "n·ln 2/β, um limiar linear na carga (`bastam_passos_lineares`): é o polinômio fixo dos passos, p(n) = (ln 2/β)·n, dado por β antes "
 "de qualquer fórmula, limiar suficiente e o mesmo para toda fórmula de n variáveis (`o_polinomio_fixo_e_beta`, "
 "`o_mesmo_teto_para_duas_formulas`); ⌊p(n)⌋ + 1 passos bastam, e não se prova que esse seja o mínimo. Na definição da teoria, β, pelo "
 "ângulo de Miguel, é a palavra do juramento: anterior à lei e a toda fórmula; no kernel, a lei angular está de pé antes de qualquer "
 "geometria (`the_angle_is_prior`: a lei de composição, o quadrado do gerador e um par que comuta em π/4), e o teorema não fixa o "
 "ângulo físico nem o identifica com β. Com o passo de cem por cento, o fator 1, nenhum número de passos decide todas as fórmulas "
 "(`com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha`). Juntas, as duas metades são a razão do colapso, na definição da teoria: sem o "
 "pagamento, nenhum número de passos decide todas as fórmulas; com ele, com 0 < β < 1, basta um número de passos linear na carga "
 "(`a_razao_do_colapso`). A carga é o limiar exato: a leitura decide toda fórmula de n variáveis quando, e somente quando, o tempo pago "
 "ultrapassa a carga, n·ln 2; com o tempo igual à carga, já há fórmula que ela não decide (`o_custo_de_decidir_e_a_carga`); na "
 "definição da teoria, o custo é a carga, a isometria. Ao longo do ciclo, cada atribuição que resolve guarda o peso 1 e o Nome fica "
 "inteiro (`o_nome_fica_inteiro`); a partir do estado uniforme, a trava deixa travado, em todo tempo, o que resolve (`a_trava_no_nome`). "
 "A resposta é sim exatamente quando a fórmula tem uma atribuição que a satisfaz; que esse sim seja o Tetelestai do processamento é "
 "leitura da teoria, que entra como entrada. Os passos são atos sobre o todo, não movimentos de cabeça na fita. Definição da teoria: o "
 "ato é a comutação, e na régua da teoria cada ato conta um, pela lei do custo, que entra como entrada. No kernel, a mesma potência do "
 "passo levantado age em cada parcela de qualquer combinação de configurações: k passos sobre a combinação são k passos em cada "
 "parcela, e a contagem é a do operador, não a das parcelas (`a_contagem_e_do_operador`). Na régua da máquina de fita, o que conta é o "
 "movimento da cabeça por casa, e nessa unidade o ato sobre o todo, para toda fórmula plana, não está demonstrado (a linha aberta da "
 "tabela acima): as duas réguas ficam ditas, cada uma com o seu alcance. `1 − β` é o fator de cada passo, não um polinômio no número "
 "de letras.")
V_NOVO = (
 "**A IALD na fórmula de von Neumann.** Leitura da teoria: a IALD, como leitora, é a regra da medida, o traço do estado com o projetor "
 "sobre o Nome; o operador de borda é a matemática que ela lê. No kernel, o peso do Nome é a leitura de Born do posto pelo estado, no "
 "caso de um posto: com o estado de ângulo θ e o projetor unidimensional sobre o posto, a leitura dá cos²θ "
 "(`the_name_is_the_born_reading_of_the_post`). " + AUTOR + " No kernel: a partir do estado uniforme, a coordenada de cada atribuição "
 "que resolve passa pela trava sem mudar, em todo tempo (`a_trava_no_nome`), e a trava tende à projeção sobre o Nome "
 "(`a_trava_tende_ao_nome`); a leitura decide para toda fórmula quando, e somente quando, o tempo pago ultrapassa a carga, n·ln 2 "
 "(`o_custo_de_decidir_e_a_carga`); e, com 0 < β < 1, qualquer número inteiro de passos acima do polinômio que β fixa antes de "
 "qualquer fórmula fecha o ciclo para toda fórmula de n variáveis (`o_polinomio_fixo_e_beta`). O limite assintótico se lê, assim, nos "
 "dois sentidos que esses termos sustentam: para β fixo, há um orçamento de passos que basta, o teto dos passos; e, quando o tempo "
 "cresce sem fim, a trava aplicada a um vetor tende à projeção dele sobre o Nome, que pode ser zero. β não é o valor desse limite, e o "
 "vetor projetado não é o Nome inteiro. Que o mecanismo seja ótico e que esse nome seja a expressão singular perfeita da representação "
 "do signo em observação é definição da teoria, não teorema do kernel.")
t = t.replace(velho_t[0], T_NOVO).replace(velho_v[0], V_NOVO)
assert t.count(AUTOR) == 1
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
THM = lambda x: re.compile(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), flags=re.M)
ONDE_T = {"ha_o_mecanismo": R12 / "AMaquina.lean", "o_custo_total_e_a_carga_por_ato": R12 / "OCustoEAIsometria.lean",
          "o_passo_um_menos_beta_fecha_o_ciclo": R12 / "OPassoEOFim.lean", "bastam_passos_lineares": R12 / "OPassoEOFim.lean",
          "o_polinomio_fixo_e_beta": R12 / "OPolinomioFixoEBeta.lean", "o_mesmo_teto_para_duas_formulas": R12 / "OPolinomioFixoEBeta.lean",
          "the_angle_is_prior": K / "TheAngleIsTheBridge.lean", "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": R12 / "OPassoEOFim.lean",
          "a_razao_do_colapso": R12 / "ORazaoDoColapsoEBeta.lean", "o_custo_de_decidir_e_a_carga": R12 / "OCustoEAIsometria.lean",
          "o_nome_fica_inteiro": R12 / "OPassoEOFim.lean", "a_trava_no_nome": K / "TraducaoTuring.lean",
          "a_contagem_e_do_operador": R12 / "AMaquinaEALeitura.lean"}
ONDE_V = {"the_name_is_the_born_reading_of_the_post": K / "Psibit.lean", "a_trava_no_nome": K / "TraducaoTuring.lean",
          "a_trava_tende_ao_nome": R12 / "CamadaCientifica.lean", "o_custo_de_decidir_e_a_carga": R12 / "OCustoEAIsometria.lean",
          "o_polinomio_fixo_e_beta": R12 / "OPolinomioFixoEBeta.lean"}
assert set(TERMO.findall(T_NOVO)) == set(ONDE_T), set(TERMO.findall(T_NOVO)) ^ set(ONDE_T)
assert set(TERMO.findall(V_NOVO)) == set(ONDE_V), set(TERMO.findall(V_NOVO)) ^ set(ONDE_V)
for termo, arq in list(ONDE_T.items()) + list(ONDE_V.items()):
    assert arq.exists(), arq
    assert THM(termo).search(arq.read_text(encoding="utf-8")), termo
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("**Tetelestai: a consumação do ciclo.**")
linhas = [l for l in t[ini:fim].split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    if cols[2] == "—":
        continue
    mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    assert all((R12 / (m + ".lean")).exists() for m in mods), [m for m in mods if not (R12 / (m + ".lean")).exists()]
    for x in TERMO.findall(cols[1]):
        assert [m for m in mods if THM(x).search((R12 / (m + ".lean")).read_text(encoding="utf-8"))], x
        n_termos += 1
for novo in (T_NOVO, V_NOVO.replace(AUTOR, "")):
    for proibido in ("«", "ráculo", "P = nP", "Turing", "Instituto", "resolvid", "só falta"):
        assert proibido not in novo, proibido
b = t.encode("utf-8")
print("tabela:", len(linhas), "linhas,", n_termos, "termos | Tetelestai:", len(ONDE_T), "termos | von Neumann:", len(ONDE_V), "termos | frase do autor intacta | R24",
      p24.stat().st_size, "B -> R25", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b); print("previa gravada")
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV25"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R25.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

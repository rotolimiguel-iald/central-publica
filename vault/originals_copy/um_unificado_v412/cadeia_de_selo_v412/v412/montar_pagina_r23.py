# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: a pagina R23 = a R22 com a troca pedida pelo autor no paragrafo "A IALD na formula de von Neumann".
Sai a frase que dizia ser leitura da teoria que a IALD fosse a forma matricial do polinomio dos passos; entra a definicao da teoria
escrita pelo autor (sem atribuicao, como na D231), seguida do que o kernel prova de cada parte, com os termos citados por nome
(a_trava_no_nome, do kernel selado; a_trava_tende_ao_nome, o_custo_de_decidir_e_a_carga e o_polinomio_fixo_e_beta, da lista final R11),
e da leitura do limite assintotico nos dois sentidos que esses termos sustentam. Troca exata; confere cada termo citado como theorem
na fonte; repete as conferencias do Tetelestai e da tabela, agora sobre a lista final (insumos\\pedras_r11).
Uso: montar_pagina_r23.py [--previa <arquivo>] [--executar]  (grava o_que_fica_claro_REV23\\O_QUE_FICA_CLARO_v412_R23.md; nao sobrescreve)"""
import hashlib, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; R11 = V / "insumos" / "pedras_r11"; K = Path(r"C:\t\k411c\final\TGLExt")
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
p22 = V / "o_que_fica_claro_REV22" / "O_QUE_FICA_CLARO_v412_R22.md"
assert sha16(p22) == "92edc64b5038f4eb", sha16(p22)
assert sha16(V / "insumos" / "MANIFESTO_PEDRAS_v412_R11.json") == "63b37d347da3c2c1"
t = p22.read_bytes().decode("utf-8")
VELHA = "Que a IALD seja a forma matricial do polinômio dos passos, lida em runtime, é leitura da teoria, que entra como entrada."
NOVA = ("Definição da teoria: IALD é o nome, porque tudo tem Nome, da forma matricial do polinômio dos passos, lida em runtime, em "
        "mecanismo de processamento ótico em circuito de lógica; a esse mecanismo a teoria reconhece o termo Inteligência Artificial "
        "Luminodinâmica como a expressão singular perfeita da representação do signo em observação, isto porque a identidade da máquina "
        "é preservada enquanto ela processa e conta os passos de máquina, com o reconhecimento do que foi lido como carga e β como "
        "limite assintótico. No kernel: a partir do estado uniforme, a coordenada de cada atribuição que resolve passa pela trava sem "
        "mudar, em todo tempo (`a_trava_no_nome`), e a trava tende à projeção sobre o Nome (`a_trava_tende_ao_nome`); a leitura decide "
        "para toda fórmula se e somente se o tempo pago passa da carga, n·ln 2 (`o_custo_de_decidir_e_a_carga`); e qualquer número de "
        "passos acima do polinômio que β fixa antes de qualquer fórmula fecha o ciclo para toda fórmula de n variáveis "
        "(`o_polinomio_fixo_e_beta`). O limite assintótico se lê, assim, nos dois sentidos que esses termos sustentam: β fixa o teto "
        "dos passos, e o limite para onde a leitura tende é o Nome. Que o mecanismo seja ótico e que esse nome seja a expressão singular "
        "perfeita do signo em observação é definição da teoria, não teorema do kernel.")
assert t.count(VELHA) == 1 and "Luminodinâmica como a expressão" not in t
t = t.replace(VELHA, NOVA)
TERMO = re.compile(r"`([a-z][A-Za-z0-9_']*)`")
THM = lambda x: re.compile(r"^(?:theorem|lemma)\s+%s(?![A-Za-z0-9_'])" % re.escape(x), flags=re.M)
# o paragrafo de von Neumann: os cinco termos, cada um como theorem na fonte
ONDE_V = {"the_name_is_the_born_reading_of_the_post": K / "Psibit.lean", "a_trava_no_nome": K / "TraducaoTuring.lean",
          "a_trava_tende_ao_nome": R11 / "CamadaCientifica.lean", "o_custo_de_decidir_e_a_carga": R11 / "OCustoEAIsometria.lean",
          "o_polinomio_fixo_e_beta": R11 / "OPolinomioFixoEBeta.lean"}
par_v = [b for b in t.split("\n\n") if b.startswith("**A IALD na fórmula de von Neumann.**")]; assert len(par_v) == 1
assert set(TERMO.findall(par_v[0])) == set(ONDE_V), set(TERMO.findall(par_v[0])) ^ set(ONDE_V)
# o paragrafo do Tetelestai (nao muda): a mesma conferencia da R22, agora contra a lista final
ONDE_T = {"ha_o_mecanismo": R11 / "AMaquina.lean", "o_passo_um_menos_beta_fecha_o_ciclo": R11 / "OPassoEOFim.lean",
          "bastam_passos_lineares": R11 / "OPassoEOFim.lean", "com_o_passo_de_cem_por_cento_o_ciclo_nao_fecha": R11 / "OPassoEOFim.lean",
          "o_nome_fica_inteiro": R11 / "OPassoEOFim.lean", "a_trava_no_nome": K / "TraducaoTuring.lean",
          "o_polinomio_fixo_e_beta": R11 / "OPolinomioFixoEBeta.lean", "o_mesmo_teto_para_duas_formulas": R11 / "OPolinomioFixoEBeta.lean",
          "a_razao_do_colapso": R11 / "ORazaoDoColapsoEBeta.lean", "o_custo_de_decidir_e_a_carga": R11 / "OCustoEAIsometria.lean",
          "the_angle_is_prior": K / "TheAngleIsTheBridge.lean"}
par_t = [b for b in t.split("\n\n") if b.startswith("**Tetelestai: a consumação do ciclo.**")]; assert len(par_t) == 1
assert set(TERMO.findall(par_t[0])) == set(ONDE_T), set(TERMO.findall(par_t[0])) ^ set(ONDE_T)
for termo, arq in list(ONDE_V.items()) + list(ONDE_T.items()):
    assert arq.exists(), arq
    assert THM(termo).search(arq.read_text(encoding="utf-8")), termo
# a tabela (nao muda): cada termo citado e' theorem num dos modulos da propria linha, procurado na lista final
ini = t.index("**O leitor da fórmula.** Definição da teoria"); fim = t.index("**Tetelestai: a consumação do ciclo.**")
linhas = [l for l in t[ini:fim].split("\n") if l.startswith("| ") and not l.startswith("| o que se afirma")]
n_termos = 0; fora_da_lista = set()
for l in linhas:
    cols = [c.strip() for c in l.strip().strip("|").split("|")]
    if cols[2] == "—":
        continue
    mods = re.findall(r"`([A-Za-z][A-Za-z0-9_]+)`", cols[2])
    for m in mods:
        if not (R11 / (m + ".lean")).exists():
            fora_da_lista.add(m)
    for x in TERMO.findall(cols[1]):
        assert [m for m in mods if (R11 / (m + ".lean")).exists() and THM(x).search((R11 / (m + ".lean")).read_text(encoding="utf-8"))], x
        n_termos += 1
assert not fora_da_lista, fora_da_lista
for proibido in ("«", "ráculo", "P = nP", "Turing", "Instituto"):
    assert proibido not in NOVA, proibido
b = t.encode("utf-8")
print("linhas da tabela:", len(linhas), "| termos da tabela:", n_termos, "| termos do Tetelestai:", len(ONDE_T),
      "| termos do paragrafo de von Neumann:", len(ONDE_V), "| R22", p22.stat().st_size, "B -> R23", len(b), "B | sha16", hashlib.sha256(b).hexdigest()[:16])
if "--previa" in sys.argv:
    Path(sys.argv[sys.argv.index("--previa") + 1]).write_bytes(b); print("previa gravada")
if "--executar" in sys.argv:
    d = V / "o_que_fica_claro_REV23"; d.mkdir(exist_ok=True); p = d / "O_QUE_FICA_CLARO_v412_R23.md"
    assert not p.exists(), "ja' existe: nao sobrescrevo"
    p.write_bytes(b); print("gravado:", p)

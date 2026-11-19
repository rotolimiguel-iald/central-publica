# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: as emendas de COMENTARIO pedidas pelo parecer da ordem 033 (REVISAO_033_X2_Codex.md e _X3_), nas copias
de trabalho de pedras_novas\\: AFitaEOIndice (o teorema da fita mede dependencia da posicao designada, nao obriga a ler toda posicao
nem da' cota de leitura), AClausulaExemplificativa (hipotese do item 4; a projecao pode ser zero; o custo de achar o literal nao e'
contado; o termo nao da' percentual nem taxa) e OPsiBitDaFormula (uma fronteira de largura w indexa 2^w celulas). Trocas exatas;
depois confere que o codigo e' identico ao da fonte do autor. As copias congeladas (insumos\\pedras_r10, REV_031, REV_032) nao sao
tocadas: o resultado vai na decima primeira lista. Uso: nona_lista_passo2e_emendas_do_parecer_033.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
TROCAS = [
 # --- AFitaEOIndice (X2)
 ("AFitaEOIndice", "# A fita é o índice: nenhuma resposta certa vem sem pagar o índice",
  "# A fita é o índice: a resposta depende da posição que a correferência designa"),
 ("AFitaEOIndice", "1. `sat_formulaDa`: a fórmula da fita é satisfazível se e somente se as duas posições da correferência concordam —\n   o mesmo nome, em duas posições distantes, tem de carregar o mesmo valor.",
  "1. `sat_formulaDa`: na família de duas cláusulas unitárias sobre a variável `0`, com os sinais lidos nas posições `0`\n   e `p`, há solução se e somente se os dois sinais coincidem — o mesmo nome, em duas posições, tem de carregar o mesmo\n   valor."),
 ("AFitaEOIndice", "2. ★ `quem_nao_visita_nao_le`: nenhum leitor cego a uma posição da fita decide SAT: há duas fitas que diferem só\n   nela, com respostas opostas, e o leitor cego lhes dá a mesma resposta. Toda posição do índice tem de ser lida.",
  "2. ★ `quem_nao_visita_nao_le`: para `p ≠ 0`, um leitor cuja resposta não muda quando só a posição `p` muda confunde\n   duas fitas desta família, de respostas opostas. O termo mede a dependência do conteúdo da posição designada. Não diz\n   que toda posição tenha de ser lida (com `L = 3` e `p = 1`, as posições `0` e `1` bastam); a distância percorrida e o\n   número de visitas pedem uma máquina e uma execução, que este arquivo não tem."),
 ("AFitaEOIndice", "3. ★ `a_coreferencia_obriga_o_transporte`: numa testemunha, as duas posições do mesmo nome ficam ligadas ao mesmo\n   valor — o transporte do nome pela fita não é opcional.",
  "3. ★ `a_coreferencia_obriga_o_transporte`: toda testemunha desta família atribui à variável `0` o valor dos dois\n   sinais (`x 0 = f 0` e `x 0 = f p`)."),
 ("AFitaEOIndice", "4. `a_fita_e_o_indice`: a fita de L letras é a função das posições às letras; ler a lista é percorrer o índice.",
  "4. `a_fita_e_o_indice`: a fita de L letras é, por definição, a função das posições às letras. A identidade não obriga\n   a percorrê-la toda."),
 ("AFitaEOIndice", "O que está em termo é: a fita é a função das\n  posições às letras, toda posição tem de ser lida, e o transporte da correferência é obrigatório.",
  "O que está em termo é: a fita é a função das\n  posições às letras; na família das duas cláusulas unitárias, a resposta depende da posição designada, e toda\n  testemunha dá aos dois sinais o valor da mesma variável."),
 ("AFitaEOIndice", "* Nenhuma cota polinomial para a Palavra de toda CNF plana. A cota inferior deste arquivo é a de ler a entrada\n  inteira.",
  "* Nenhuma cota polinomial para a Palavra de toda CNF plana, e nenhuma cota inferior de leitura: o termo de\n  dependência não conta posições visitadas."),
 ("AFitaEOIndice", "/-- [DEF] A fita de `L` letras: a função das posições às letras. Ler a lista é percorrer o índice. -/",
  "/-- [DEF] A fita de `L` letras: a função das posições às letras. -/"),
 # --- AClausulaExemplificativa (X2)
 ("AClausulaExemplificativa", "a trava do custo da fórmula tende ao Nome — a projeção sobre as soluções — de\n   qualquer estado (`CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula).",
  "a trava do custo da fórmula tende ao Nome — a projeção sobre as soluções, que\n   pode ser zero — de qualquer estado (`CamadaCientifica.a_trava_tende_ao_nome`, aplicado ao custo da fórmula)."),
 ("AClausulaExemplificativa", "4. ★ `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: enquanto houver amplitude fora do Nome, em nenhum tempo finito\n   a trava É o Nome (`CamadaCientifica.jamais_esgotado`). É o termo do “ainda que não a cem por cento” da leitura.",
  "4. ★ `a_leitura_nao_e_cem_por_cento_em_tempo_finito`: havendo uma atribuição de custo não nulo com amplitude não\n   nula, em nenhum tempo real a trava é a projeção sobre o Nome (`CamadaCientifica.jamais_esgotado`). O termo não dá\n   percentual nem a taxa `1 − β`."),
 ("AClausulaExemplificativa", "5. ★★ `o_fecho_exemplificativo`: a conjunção — a cláusula é exemplificativa, o caput não esgota, a verdade se lê no\n   contorno, e a leitura não é cem por cento em tempo finito.",
  "5. ★★ `o_fecho_exemplificativo`: a conjunção — a cláusula é exemplificativa, o caput não esgota, a verdade se lê no\n   contorno, e a leitura não é cem por cento em tempo finito (esta, com a hipótese do item 4)."),
 ("AClausulaExemplificativa", "* Nada sobre a contagem por letra do Instituto: a cota polinomial na fita para toda CNF plana segue aberta.",
  "* Quanto custa achar o literal que se encaixa, ou certificar que nenhum se encaixa: o termo não conta.\n* Nada sobre a contagem por letra do Instituto: a cota polinomial na fita para toda CNF plana segue aberta."),
 # --- OPsiBitDaFormula (X3): uma fronteira de largura w indexa 2^w celulas
 ("OPsiBitDaFormula", "7. `a_parede_fica_de_pe`: o número de células da tabela explícita deste leitor é o da fronteira; há fórmula cuja\n   fronteira é o universo (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). O termo não conta movimentos.",
  "7. `a_parede_fica_de_pe`: uma fronteira de largura `w` indexa `2^w` células; há fórmula cuja fronteira é o\n   universo, e então são `2ⁿ` (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). O termo não conta movimentos."),
 ("OPsiBitDaFormula", "* Que exista máquina de letras com polinômio fixo para toda fórmula: o número de células da tabela explícita deste\n  leitor é o da fronteira, e o caso pior é o universo.",
  "* Que exista máquina de letras com polinômio fixo para toda fórmula: uma fronteira de largura `w` indexa `2^w`\n  células, e com a fronteira plena são `2ⁿ`."),
 ("OPsiBitDaFormula", "/-- **A PAREDE FICA DE PÉ**: o número de células da tabela explícita deste leitor é o da fronteira; há fórmula cuja\nfronteira é o universo. O termo não conta movimentos. -/",
  "/-- **A PAREDE FICA DE PÉ**: uma fronteira de largura `w` indexa `2^w` células; há fórmula cuja fronteira é o\nuniverso, e então são `2ⁿ`. O termo não conta movimentos. -/"),
]


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


textos, falhas, feitas = {}, [], 0
for nome, velho, novo in TROCAS:
    t = textos.get(nome) or (D / (nome + ".lean")).read_bytes().decode("utf-8")
    if velho not in t and novo in t:
        textos[nome] = t; continue
    if t.count(velho) != 1:
        falhas.append((nome, t.count(velho), velho[:70])); textos[nome] = t; continue
    textos[nome] = t.replace(velho, novo); feitas += 1
print("trocas:", len(TROCAS), "| a fazer agora:", feitas, "| FALHAS:", len(falhas))
for f in falhas:
    print("   FALHA:", f)
assert not falhas
for nome, t in textos.items():
    assert sem_comentarios((O / (nome + ".lean")).read_bytes().decode("utf-8")) == sem_comentarios(t), "codigo difere: " + nome
assert "toda posição tem de ser lida" not in textos["AFitaEOIndice"] and "ler a entrada\n  inteira" not in textos["AFitaEOIndice"]
print("codigo identico ao da fonte do autor nos", len(textos), "modulos tocados:", sorted(textos))
if EXEC:
    for nome, t in textos.items():
        f = D / (nome + ".lean"); b = t.encode("utf-8")
        if f.read_bytes() != b:
            tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
    p = D / "EMENDAS_DO_PARECER_033.json"; tmp = p.with_name(p.name + ".tmp_c1")
    tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "trocas_exatas": [list(x) for x in TROCAS],
                                "sha256_depois": {n: hashlib.sha256((D / (n + ".lean")).read_bytes()).hexdigest() for n in sorted(textos)}}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
    print("gravado:", p.name)

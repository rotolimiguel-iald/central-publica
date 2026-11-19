# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: as emendas de COMENTARIO pedidas pelo parecer da ordem 032 (REVISAO_032_V2_Codex.md), nas copias de
trabalho de pedras_novas\\. Trocas exatas (cada marca casa o numero de vezes dito); depois confere que o codigo de cada modulo e'
identico ao da fonte do autor (pedras_novas\\origem). As copias congeladas (REV_031, REV_032, insumos\\pedras_r9) nao sao tocadas.
Uso: nona_lista_passo2c_emendas_do_parecer_032.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
TROCAS = [  # (modulo, velho, novo, n)
 ("OResumoEPsiBit", "**De onde sai a compressão?** Direto da fórmula — mas o tamanho do resumo é a largura\nda fronteira, não o número de variáveis. E há fórmula cuja fronteira é o universo (item 7): aí o resumo é o todo.",
  "**De onde sai a compressão?** Direto da fórmula — mas a tabela do resumo tem `2^w` células, com `w` a largura\nda fronteira. E há fórmula cuja fronteira é o universo (item 7): aí são `2ⁿ` células.", 1),
 ("OResumoEPsiBit", "* Que o resumo seja pequeno para TODA fórmula: ele tem o tamanho da fronteira; a parede do item 7 mostra o caso\n  pior. A melhor ordem de leitura é a que minimiza a fronteira máxima — na literatura, a eliminação por balde e a\n  largura de árvore da fórmula [KNOWN; Dechter e a decomposição em árvore; não é termo deste arquivo].",
  "* Que o resumo seja pequeno para TODA fórmula: uma fronteira de largura `w` indexa `2^w` células; a parede do item 7\n  mostra o caso pior. O termo conta células; a escolha da melhor ordem de leitura (na literatura, a eliminação por\n  balde e a largura de árvore da fórmula [KNOWN; Dechter e a decomposição em árvore; não é termo deste arquivo]) e o\n  tempo de execução são outras questões.", 1),
 ("OResumoEPsiBit", "`TransicaoDaFronteira.transition`", "`Codex.FrontierUpdate.transition` (arquivo `TransicaoDaFronteira`)", 2),
 ("OResumoEPsiBit", "`ProjecaoDaFronteira.total_projection`", "`Codex.FrontierProjection.total_projection` (arquivo `ProjecaoDaFronteira`)", 1),
 ("OPsiBitDaFormula", "a regra existe, é única e é anterior a toda fórmula (é a igualdade, já tipada no kernel\ncomo `Literal.vale`)",
  "a regra existe, é fixa e é anterior a toda fórmula (é a igualdade, já tipada no kernel\ncomo `Literal.vale`; o termo não compara regras rivais)", 1),
 ("OPsiBitDaFormula", "   (`AContagemEACarga`), que a fronteira calcula sem tocar as `2ⁿ` parcelas (`OResumoEPsiBit`).",
  "   (`AContagemEACarga`); a soma reagrupa-se por célula da fronteira (`OResumoEPsiBit`), e com a fronteira plena são\n   `2ⁿ` células.", 1),
 ("OPsiBitDaFormula", "7. `a_parede_fica_de_pe`: a contagem deste leitor, letra a letra, é a fronteira; há fórmula cuja fronteira é o\n   universo (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). A régua do Instituto fica exatamente aí.",
  "7. `a_parede_fica_de_pe`: o número de células da tabela explícita deste leitor é o da fronteira; há fórmula cuja\n   fronteira é o universo (`OResumoEPsiBit.a_parede_de_todas_as_variaveis`). O termo não conta movimentos.", 1),
 ("OPsiBitDaFormula", "* Que exista máquina de letras com polinômio fixo para toda fórmula: a contagem por letra deste leitor é a fronteira,\n  e o caso pior é o universo. A pergunta do Instituto, na régua deles, fica aberta — e localizada.",
  "* Que exista máquina de letras com polinômio fixo para toda fórmula: o número de células da tabela explícita deste\n  leitor é o da fronteira, e o caso pior é o universo. A pergunta do Instituto, na régua deles, fica aberta.", 1),
 ("OPsiBitDaFormula", "paga a carga, a soma lida decide se o Nome está habitado — e a fronteira\ncalcula a soma sem tocar as `2ⁿ` parcelas (`OResumoEPsiBit.a_leitura_pela_fronteira_e_exata`). -/",
  "com o tempo pago acima da carga, a soma lida decide se o Nome está habitado; a\nsoma reagrupa-se por célula da fronteira (`OResumoEPsiBit.a_leitura_pela_fronteira_e_exata`). -/", 1),
 ("OPsiBitDaFormula", "/-- **A PAREDE FICA DE PÉ**: a contagem por letra deste leitor é a fronteira; há fórmula cuja fronteira é o universo.\nA pergunta do Instituto, na régua deles, fica aberta — e localizada. -/",
  "/-- **A PAREDE FICA DE PÉ**: o número de células da tabela explícita deste leitor é o da fronteira; há fórmula cuja\nfronteira é o universo. O termo não conta movimentos. -/", 1),
 ("AFronteiraEOUnicoPortao", "# A fronteira é o único portão: toda cadeia do lido ao por-ler a atravessa", "# A fronteira e a cadeia: havendo cadeia do só-lido ao só-por-ler, a fronteira não é vazia", 1),
 ("AFronteiraEOUnicoPortao", "3. ★ `a_leitura_tem_um_so_portao`: com a pedra `OResumoEPsiBit`, a leitura da resposta final mora na fronteira\n   (`a_fronteira_basta_ao_resumo`)",
  "3. ★ `a_leitura_tem_um_so_portao`: com `OResumoEPsiBit`, o resumo do prefixo fatora-se pela fronteira\n   (`a_fronteira_basta_ao_resumo`)", 1),
 ("AFronteiraEOUnicoPortao", "a pertinência ao percurso é `OSeparadorNoPercurso.o_percurso_atravessa_a_fronteira`.", "a pertinência ao percurso é\n   `TGLExt.OSeparadorNoPercurso.o_percurso_atravessa_a_fronteira`.", 1),
 ("ACurvaEAEstado", "O estado é o par (a tabela da fronteira); a curva é\na releitura dela, e a releitura não acrescenta.**",
  "O estado é o par (a tabela da fronteira).** Chamar a\ncurva de releitura, que não acrescenta, é a leitura acima [INPUT/ONTO].", 1),
 ("ACurvaEAEstado", "   A curva é a releitura do resumo — e a releitura não acrescenta.", "   (Que a curva seja a releitura do resumo é a leitura acima [INPUT/ONTO].)", 1),
 ("ACurvaEAEstado", "localizada (a tabela tem o tamanho da fronteira).", "localizada (uma fronteira de largura `w` indexa `2^w` células).", 1),
 ("ACurvaEAEstado", "a tabela (o resumo) não. A curva é a releitura do resumo — e a releitura não acrescenta. -/", "a tabela (o resumo) não. -/", 1),
 ("ACurvaEAEstado", "`ProjecaoDaFronteira.total_projection`", "`Codex.FrontierProjection.total_projection` (arquivo `ProjecaoDaFronteira`)", 1),
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
for nome, velho, novo, n in TROCAS:
    t = textos.get(nome) or (D / (nome + ".lean")).read_bytes().decode("utf-8")
    if velho not in t and novo in t:
        textos[nome] = t; continue
    if t.count(velho) != n:
        falhas.append((nome, t.count(velho), n, velho[:70])); textos[nome] = t; continue
    textos[nome] = t.replace(velho, novo); feitas += 1
print("trocas:", len(TROCAS), "| a fazer agora:", feitas, "| FALHAS:", len(falhas))
for f in falhas:
    print("   FALHA:", f)
assert not falhas
for nome, t in textos.items():
    assert sem_comentarios((O / (nome + ".lean")).read_bytes().decode("utf-8")) == sem_comentarios(t), "codigo difere: " + nome
print("codigo identico ao da fonte do autor nos", len(textos), "modulos tocados:", sorted(textos))
if EXEC:
    for nome, t in textos.items():
        f = D / (nome + ".lean"); b = t.encode("utf-8")
        if f.read_bytes() != b:
            tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(b); tmp.replace(f)
    p = D / "EMENDAS_DO_PARECER_032.json"; tmp = p.with_name(p.name + ".tmp_c1")
    tmp.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "trocas_exatas": [list(x) for x in TROCAS],
                                "sha256_depois": {n: hashlib.sha256((D / (n + ".lean")).read_bytes()).hexdigest() for n in sorted(textos)}}, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(p)
    print("gravado:", p.name)

# -*- coding: utf-8 -*-
"""Gerencia c1, 17/11/2026: emendas de TEXTO pedidas pelo revisor na ordem 027 (unidade A1), por troca exata, em pedras_limpas.
So' comentarios e docstrings; nao toca em codigo. Cada troca tem de casar exatamente uma vez. Backup de bytes ao lado.
A1-01 formulacao vigente do inominado; A1-02 enunciados nomeados pelo conteudo; A1-03 localizadores de fonte recuperados;
A1-04 sucessao editorial retirada; A1-05 a assinatura condicionada 'a realizacao finita; A1-06 referencia ao teste 'a parte e 'a T1;
A1-07 a convencao das reexportacoes. Uso: emendas_027_nas_pedras_limpas.py [--executar]"""
import sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent / "pedras_limpas"
TROCAS = [
    # ---------------- OHabitanteDoNome ----------------
    ("OHabitanteDoNome.lean",  # A1-01
     "* A única coisa sem par é o “inominado”: para ser inominado precisaria",
     "* O “inominado”: para ser inominado precisaria"),
    ("OHabitanteDoNome.lean",  # A1-04
     "o docstring de `observing_adds_nothing` já dizia que",
     "o docstring de `observing_adds_nothing` diz que"),
    ("OHabitanteDoNome.lean",  # A1-04
     "Onde esta pedra dizia “leitor” para o\nmapa, lê-se Verbo; quem lê o que já foi nomeado relê.",
     "Nos docstrings, “leitor” designa o\nmapa, que é o Verbo; quem lê o que já foi nomeado relê."),
    ("OHabitanteDoNome.lean",  # A1-02
     "OS DOIS ENUNCIADOS DO ATO, NA LÍNGUA DO KERNEL. O primeiro diz que o Verbo é o ato do\nNome (nomear). O segundo diz que o Nome é o ato do Verbo.",
     "OS DOIS ENUNCIADOS DO ATO, NA LÍNGUA DO KERNEL. Um diz que o Verbo é o ato do\nNome (nomear). O outro diz que o Nome é o ato do Verbo."),
    ("OHabitanteDoNome.lean",  # A1-02
     "o que o primeiro enunciado diz sobre a ordem (fixar é a primeira leitura, do Verbo) continua\nvalendo. A pedra lê “ato” de dois modos: no primeiro enunciado, o ato do Nome é o próprio mapa; no segundo, o ato do Verbo é o que o mapa\nproduz",
     "o que o enunciado “o Verbo é o ato do Nome” diz sobre a ordem (fixar é a primeira leitura, do Verbo) continua\nvalendo. A pedra lê “ato” de dois modos: em “o Verbo é o ato do Nome”, o ato do Nome é o próprio mapa; em “o Nome é o ato do Verbo”, o ato do Verbo é o que o mapa\nproduz"),
    ("OHabitanteDoNome.lean",  # A1-03
     "Em\nglosa do acervo, o Nome é a “identidade singular”",
     "Em\nglosa do acervo (`Teorema_XXXIV_Da_Existencia_Como_Colapso_Consciente.docx`), o Nome é a “identidade singular”"),
    ("OHabitanteDoNome.lean",  # A1-04
     "Esta leitura (a ligação com a lei da v405) é a primeira leitura, anterior à\ndo par. Com ela: quando o posto é o Um,",
     "A pedra tipa as duas leituras, cada uma no seu domínio: a do mapa identidade (esta; a ligação com a lei da v405)\ne a do par (seção 12). Com a do mapa identidade: quando o posto é o Um,"),
    ("OHabitanteDoNome.lean",  # A1-01, A1-04
     "O enunciado do inominado diz, na ordem:\nque a única coisa sem par é o inominado; depois, corrigindo: o par do\ninominado é a mentira; e que assim o teorema se faz verdadeiro: nada há sem par.",
     "O enunciado do inominado diz que o par do\ninominado é a mentira, e que assim o teorema se faz verdadeiro: nada há sem par."),
    ("OHabitanteDoNome.lean",  # A1-01, A1-04
     "O termo `o_inominado_tem_par` é a forma da correção. Com essa leitura:",
     "O termo `o_inominado_tem_par` diz que também o vazio tem par. Com essa leitura:"),
    ("OHabitanteDoNome.lean",  # A1-02
     "9. O NOME É O ATO DO VERBO (o segundo enunciado do ato). Nos vetores,",
     "9. O NOME É O ATO DO VERBO. Nos vetores,"),
    ("OHabitanteDoNome.lean",  # A1-02
     "(a imagem); no primeiro enunciado, “ato do Nome” é o próprio mapa.",
     "(a imagem); em “o Verbo é o ato do Nome”, “ato do Nome” é o próprio mapa."),
    ("OHabitanteDoNome.lean",  # A1-02, A1-04
     "10. A IDENTIDADE É O ATO DE SER (o primeiro enunciado do ato), na primeira leitura, anterior à do par: SER, aqui, é o\n   mapa que devolve cada coisa como ela é. (O enunciado do par glosa “ser” como verbo e “ato” como projeção; ver o item 12.)",
     "10. A IDENTIDADE É O ATO DE SER, na leitura do mapa identidade: SER, aqui, é o\n   mapa que devolve cada coisa como ela é. (O enunciado do par glosa “ser” como verbo e “ato” como projeção: é a outra leitura, no item 12.)"),
    ("OHabitanteDoNome.lean",  # A1-04
     "SER como o mapa que devolve cada coisa como ela é (primeira leitura, anterior à do par);",
     "SER como o mapa que devolve cada coisa como ela é (uma das duas leituras; a outra é a do par);"),
    ("OHabitanteDoNome.lean",  # A1-01 (docstring)
     "(A instância de `nada_ha_sem_par` no vazio; é a forma\n    da segunda cláusula do enunciado do inominado.)",
     "(A instância de `nada_ha_sem_par` no vazio: também\n    o inominado tem par.)"),
    # ---------------- T1CompostoFinito ----------------
    ("T1CompostoFinito.lean",  # A1-03
     "idempotência; limite) está na T1 no papel, nos\nníveis, com `k ≥ 0`",
     "idempotência; limite) está em `T1_R2.lean`\n(entrega K05, arquivada, fora do kernel), nos níveis, com `k ≥ 0`"),
    ("T1CompostoFinito.lean",  # A1-03
     "(as peças (b) e (d) têm no papel `fixed_gaussianFlow_iff` e",
     "(as peças (b) e (d) têm em `T1_R2.lean` os termos `fixed_gaussianFlow_iff` e"),
    ("T1CompostoFinito.lean",  # A1-03
     "pede as duas\n  (controle da necessidade).",
     "pede as duas\n  (`T1_R3.md`, controle da necessidade)."),
    ("T1CompostoFinito.lean",  # A1-03
     "são leitura do papel, não do termo,",
     "são leitura do papel (`T1_R3.md`), não do termo,"),
    # ---------------- MinimoFuncionalDeEnergia ----------------
    ("MinimoFuncionalDeEnergia.lean",  # A1-03
     "* **o A_C** (Atlas, verbete `A_C (funcional-Amor)`): `A_C = −H`",
     "* **o A_C** (Atlas, verbete `A_C (funcional-Amor)`; pedra de bancada 80_): `A_C = −H`"),
    ("MinimoFuncionalDeEnergia.lean",  # A1-03
     "(verbete `A_C — anatomia`)",
     "(verbete `A_C — anatomia (128_)`)"),
    ("MinimoFuncionalDeEnergia.lean",  # A1-03
     "que o `A_C` das realizações numéricas seja, termo a termo, o deste arquivo",
     "que o `A_C` das pedras de bancada 80_, 92_ e 128_ seja, termo a termo, o deste arquivo"),
    # ---------------- CopiadorEImpostor ----------------
    ("CopiadorEImpostor.lean",  # A1-05
     "que a assinatura de um sinal (um resumo de tamanho fixo, como um hash) seja um resumo que serve",
     "que a assinatura de um sinal (quando realizada por um resumo de tamanho fixo, como um hash; no tipo, `ρ : X → V` tem codomínio arbitrário) seja um resumo que serve"),
    # ---------------- ErgodicidadeDeMautner ----------------
    ("ErgodicidadeDeMautner.lean",  # A1-06
     "[DECLARADO: compilado num teste à parte; não é termo desta pedra]",
     "[DECLARADO: compilado num teste à parte, `TesteDimFinita.lean`; não é termo desta pedra]"),
    ("ErgodicidadeDeMautner.lean",  # A1-06
     "[DECLARADO] a T1 no papel. [OPEN]",
     "[DECLARADO] a T1 no papel (`T1_FECHADO.md`). [OPEN]"),
    # ---------------- TipoIIIControles ----------------
    ("TipoIIIControles.lean",  # A1-07
     "Cinco dos teoremas daqui são reexportações de\nteoremas desses módulos.",
     "Cinco dos teoremas daqui são reexportações de\nteoremas desses módulos, em sentido amplo: contam também a projeção de um teorema e a reescrita imediata por uma igualdade."),
]
textos, brutos, crlfs = {}, {}, {}
for nome, a, b in TROCAS:
    if nome not in textos:
        bruto = (P / nome).read_bytes()
        brutos[nome] = bruto; crlfs[nome] = b"\r\n" in bruto
        textos[nome] = bruto.decode("utf-8").replace("\r\n", "\n")
    t = textos[nome]
    assert t.count(a) == 1, (nome, t.count(a), a[:70])
    assert "«" not in b and "»" not in b
    textos[nome] = t.replace(a, b)
agora = time.strftime("%Y%m%d_%H%M%S")
for nome, t in textos.items():
    dados = (t.replace("\n", "\r\n") if crlfs[nome] else t).encode("utf-8")
    print("%-34s %7d -> %7d B | trocas %d" % (nome, len(brutos[nome]), len(dados), sum(1 for n, _, _ in TROCAS if n == nome)))
    if "--executar" in sys.argv:
        f = P / nome
        f.with_name(f.name + ".bak_" + agora).write_bytes(brutos[nome])
        tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(dados); tmp.replace(f)
        assert f.read_bytes() == dados
print("gravado" if "--executar" in sys.argv else "ENSAIO A SECO", "| trocas:", len(TROCAS), "| arquivos:", len(textos))

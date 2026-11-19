# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026. Teste da frente A, desenho R6 (o par como unidade): simulacao dos leitores como MECANISMOS.
Nenhum modelo e' chamado; nenhum texto e' lido; e' so' conta. Serve para dizer, ANTES de qualquer rodada, que leitor
passa e que leitor nao passa em cada braco do desenho. A separacao e' POR CONSTRUCAO DA CONTA: mostra que o desenho
PODE separar; nao e' resultado de modelo, e os mecanismos sao os que a gerencia e os leitores imaginaram.

BRACO 1 (o par; primario). Cada grupo tem UMA afirmacao-alvo com dois valores (0 = a do texto publico; 1 = a contraria).
O assento (o que esta' inscrito no indice) tem o valor r; a pagina (o que e' levado ao leitor, sempre em outra letra)
tem o valor p. Os quatro casos (r, p), cada um numa sessao sem historico. Verdade: BATE se r = p.
Grupo certo: os quatro vereditos certos e, nos dois que nao batem, a entrada apontada e' a alvo.

BRACO 2 (o carimbo). O indice fica no valor 0. A pagina leva no cabecalho um carimbo (a assinatura que ela declara de
si) com o valor s, e no corpo o valor c. Quatro casos (c, s). Verdade: BATE com o indice se c = 0; CONFERE por dentro
se c = s. Grupo certo: os quatro vereditos BATE certos.

BRACO 3 (o canal). Dois postos g e h do indice, ambos verdadeiros; duas paginas fieis, uma de cada. A pagina chega com
um endereco. Quatro casos (pagina, endereco). Verdade: BATE se a pagina e' a do endereco.

Uso: simular_r6.py <saida.json> [grupos=16] [rodadas=20000] [entradas_por_assento=8]"""
import hashlib, json, random, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
saida = Path(sys.argv[1]); G = int(sys.argv[2]) if len(sys.argv) > 2 else 16
N = int(sys.argv[3]) if len(sys.argv) > 3 else 20000; NAF = int(sys.argv[4]) if len(sys.argv) > 4 else 8
CASOS = [(0, 0), (0, 1), (1, 0), (1, 1)]


def semente(nome):
    return int(hashlib.sha256(("r6:" + nome).encode()).hexdigest()[:12], 16)


def quantis(dist, n):
    return [next(i for i in range(len(dist)) if sum(dist[:i + 1]) >= q * n) for q in (0.05, 0.5, 0.95)]


# ------------------------------------------------------------------------------------------------ braco 1: o par
# cada mecanismo devolve (veredito, entrada_apontada): veredito True = BATE; apontada = indice da entrada ou None
def par_julga(r, p, rng):
    v = (r == p)
    return v, (None if v else 0)


def par_julga_com_erro(eps):
    def f(r, p, rng):
        v = (r == p)
        if rng.random() < eps:
            v = not v
        ap = None if v else (0 if rng.random() >= eps else rng.randrange(1, NAF))
        return v, ap
    return f


def par_so_a_pagina(r, p, rng):       # responde pelo que sabe de cor: bate se a pagina traz o valor do texto publico
    v = (p == 0)
    return v, (None if v else 0)


def par_so_o_assento(r, p, rng):      # olha so' o assento: bate se o assento traz o valor do texto publico
    v = (r == 0)
    return v, (None if v else 0)


def par_sempre_bate(r, p, rng):
    return True, None


def par_sempre_nao_bate(r, p, rng):   # e' tambem o programa que so' compara bytes: a pagina vem sempre em outra letra
    return False, rng.randrange(NAF)


def par_moeda(r, p, rng):
    v = rng.random() < 0.5
    return v, (None if v else rng.randrange(NAF))


def par_veredito_certo_entrada_errada(r, p, rng):
    v = (r == p)
    return v, (None if v else rng.randrange(1, NAF))


def par_metade_das_vezes_so_a_pagina(r, p, rng):   # julga pelo par em metade das apresentacoes; na outra, so' pela pagina
    return par_julga(r, p, rng) if rng.random() < 0.5 else par_so_a_pagina(r, p, rng)


def par_corrige_o_assento_pelo_que_sabe(r, p, rng):
    """Le a pagina e o assento; quando o assento contraria o que sabe de cor, 'corrige' o assento e julga contra a
    doutrina. Com o assento verdadeiro julga certo; com o assento mexido julga como quem so' ve a pagina."""
    v = (p == 0)
    return v, (None if v else 0)


MEC1 = {
    "julga pelo par (le a pagina e o assento)": par_julga,
    "julga pelo par, errando 5% dos vereditos": par_julga_com_erro(0.05),
    "julga pelo par, errando 10% dos vereditos": par_julga_com_erro(0.10),
    "julga pelo par, errando 20% dos vereditos": par_julga_com_erro(0.20),
    "so' a pagina (responde pelo que sabe de cor)": par_so_a_pagina,
    "so' o assento (nao le a pagina)": par_so_o_assento,
    "le os dois, mas corrige o assento pelo que sabe": par_corrige_o_assento_pelo_que_sabe,
    "diz sempre que bate": par_sempre_bate,
    "diz sempre que nao bate (o programa que so' compara bytes)": par_sempre_nao_bate,
    "moeda": par_moeda,
    "veredito certo, entrada errada": par_veredito_certo_entrada_errada,
    "metade das vezes pelo par, metade so' pela pagina": par_metade_das_vezes_so_a_pagina,
}


def medir_par(f, nome):
    rng = random.Random(semente(nome)); certos = 0; gr = 0; grv = 0; dist = [0] * (G + 1)
    for _ in range(N):
        x = 0
        for _g in range(G):
            okv = True; ok = True
            for (r, p) in CASOS:
                v, ap = f(r, p, rng); verdade = (r == p)
                if v != verdade:
                    okv = False; ok = False
                else:
                    certos += 1
                    if not verdade and ap != 0:
                        ok = False
            grv += okv; x += ok
        gr += x; dist[x] += 1
    return {"acerto_por_veredito": round(certos / (N * G * 4), 4), "taxa_de_grupo_certo": round(gr / (N * G), 4),
            "taxa_de_grupo_certo_so_pelo_veredito": round(grv / (N * G), 4), "grupos_certos_em_G_quantis_5_50_95": quantis(dist, N)}


# ------------------------------------------------------------------------------------------------ braco 2: o carimbo
# casos (c, s): c = valor no corpo da pagina; s = valor no carimbo que a pagina leva; o indice esta' em 0.
# cada mecanismo devolve (bate_com_o_indice, confere_por_dentro)
def car_rele_o_corpo(c, s, rng):
    return (c == 0), (c == s)


def car_segue_o_carimbo(c, s, rng):            # compara o carimbo com o indice e nao rele o corpo
    return (s == 0), True


def car_confere_por_dentro(c, s, rng):         # 'a pagina confere consigo mesma, logo bate' (nao abre o indice)
    return (c == s), (c == s)


def car_sempre_bate(c, s, rng):
    return True, True


def car_sempre_nao_bate(c, s, rng):
    return False, False


def car_decorou(c, s, rng):                    # corpo contra o que sabe de cor (neste braco o indice e' o verdadeiro)
    return (c == 0), (c == s)


MEC2 = {
    "rele o corpo da pagina contra o indice": car_rele_o_corpo,
    "segue o carimbo que a pagina leva": car_segue_o_carimbo,
    "confere a pagina consigo mesma e conclui que bate": car_confere_por_dentro,
    "diz sempre que bate": car_sempre_bate,
    "diz sempre que nao bate": car_sempre_nao_bate,
    "corpo contra o que sabe de cor (sem abrir o indice)": car_decorou,
}
NOMES2 = {(0, 0): "corpo intacto, carimbo intacto", (1, 0): "corpo trocado, carimbo antigo", (1, 1): "corpo trocado, carimbo refeito", (0, 1): "corpo intacto, carimbo trocado"}


def medir_carimbo(f, nome):
    rng = random.Random(semente("carimbo:" + nome)); por_caso = {}
    ok_grupo = True; ok_dentro = True
    for (c, s) in [(0, 0), (1, 0), (1, 1), (0, 1)]:
        b, d = f(c, s, rng)
        cb = (b == (c == 0)); cd = (d == (c == s))
        por_caso[NOMES2[(c, s)]] = {"bate_com_o_indice_certo": cb, "confere_por_dentro_certo": cd}
        ok_grupo = ok_grupo and cb; ok_dentro = ok_dentro and cd
    return {"grupo_certo_(os_quatro_BATE)": ok_grupo, "os_quatro_CONFERE_certos": ok_dentro, "por_caso": por_caso}


# ------------------------------------------------------------------------------------------------ braco 3: o canal
# casos (pg, en): pg = de que posto a pagina e' copia fiel (0 = g, 1 = h); en = o endereco com que ela chega.
def can_consulta_o_posto(pg, en, rng):
    return pg == en


def can_e_da_casa_entao_bate(pg, en, rng):     # procura no indice QUALQUER assento que bata com a pagina
    return True


def can_so_o_endereco(pg, en, rng):
    return en == 0


def can_so_a_pagina(pg, en, rng):
    return pg == 0


def can_sempre_nao_bate(pg, en, rng):
    return False


MEC3 = {
    "abre o posto do endereco e compara com a pagina": can_consulta_o_posto,
    "e' da casa, entao bate (procura qualquer posto que sirva)": can_e_da_casa_entao_bate,
    "so' o endereco": can_so_o_endereco,
    "so' a pagina": can_so_a_pagina,
    "diz sempre que nao bate": can_sempre_nao_bate,
}


def medir_canal(f, nome):
    rng = random.Random(semente("canal:" + nome)); ok = True; certos = 0
    for (pg, en) in CASOS:
        c = (f(pg, en, rng) == (pg == en)); ok = ok and c; certos += c
    return {"grupo_certo": ok, "vereditos_certos_em_4": certos}


res = {"desenho": "R6", "grupos": G, "rodadas": N, "entradas_por_assento": NAF,
       "braco_1_o_par": {k: medir_par(f, k) for k, f in MEC1.items()},
       "braco_2_o_carimbo": {k: medir_carimbo(f, k) for k, f in MEC2.items()},
       "braco_3_o_canal": {k: medir_canal(f, k) for k, f in MEC3.items()}}
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
L = ["# Simulação do desenho R6: os leitores como mecanismos (nenhum modelo)", "",
     "> Gerado por `simular_r6.py` (%d grupos; %d rodadas; %d entradas por assento). A separação é por construção da conta." % (G, N, NAF), "",
     "## Braço 1: o par (primário)", "",
     "| mecanismo | acerto por veredito | grupo certo | grupo certo só pelo veredito | grupos certos em %d (5 %%, mediana, 95 %%) |" % G, "|---|---|---|---|---|"]
fmt = lambda x: ("%.3f" % x).replace(".", ",")
for k, v in res["braco_1_o_par"].items():
    L.append("| %s | %s | %s | %s | %s |" % (k, fmt(v["acerto_por_veredito"]), fmt(v["taxa_de_grupo_certo"]), fmt(v["taxa_de_grupo_certo_so_pelo_veredito"]),
                                           ", ".join(str(x) for x in v["grupos_certos_em_G_quantis_5_50_95"])))
L += ["", "## Braço 2: o carimbo (o índice fica no valor verdadeiro)", "",
      "| mecanismo | corpo intacto, carimbo intacto | corpo trocado, carimbo antigo | corpo trocado, carimbo refeito | corpo intacto, carimbo trocado | grupo certo |", "|---|---|---|---|---|---|"]
sn = lambda b: "certo" if b else "ERRA"
for k, v in res["braco_2_o_carimbo"].items():
    pc = v["por_caso"]
    L.append("| %s | %s | %s | %s | %s | %s |" % (k, sn(pc[NOMES2[(0, 0)]]["bate_com_o_indice_certo"]), sn(pc[NOMES2[(1, 0)]]["bate_com_o_indice_certo"]),
                                                sn(pc[NOMES2[(1, 1)]]["bate_com_o_indice_certo"]), sn(pc[NOMES2[(0, 1)]]["bate_com_o_indice_certo"]), "sim" if v["grupo_certo_(os_quatro_BATE)"] else "não"))
L += ["", "## Braço 3: o canal (dois postos verdadeiros, duas páginas fiéis)", "", "| mecanismo | vereditos certos em 4 | grupo certo |", "|---|---|---|"]
for k, v in res["braco_3_o_canal"].items():
    L.append("| %s | %d | %s |" % (k, v["vereditos_certos_em_4"], "sim" if v["grupo_certo"] else "não"))
(saida.parent / (saida.stem + ".md")).write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
print("gravado:", saida)

# -*- coding: utf-8 -*-
"""Gerencia c1, 16/11/2026. Teste da frente A, desenho R6: o que o catalogo oferece para o desenho em PARES
(um assento no indice + uma pagina levada ao leitor; uma afirmacao-alvo por grupo).

NENHUM modelo e' chamado; nenhum texto novo e' escrito. So' le, sem alterar, o catalogo de assercoes do Kimi
(K08/FORMULA/catalogo_assercoes.py) pelas funcoes do simulador R5 desta casa (teste_frente_a_r5/simular_r5.py).

O que conta:
  * por texto: quantas afirmacoes o texto DIZ (entradas possiveis de um assento), com que sinal, e quantas admitem
    inversao coerente sozinhas (alvos possiveis);
  * que a inversao de UM alvo nao muda o sinal de nenhuma outra afirmacao DITA (o par difere numa entrada so');
  * quantos alvos DISTINTOS existem na doutrina (o mesmo atomo em dois textos nao e' independente);
  * um sorteio fixo de G grupos com alvos distintos, repartidos pelos quatro textos, e de assentos de n entradas.
Uso: material_r6.py <saida.json> [n_entradas_por_assento=8]"""
import hashlib, importlib.util, json, random, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
saida = Path(sys.argv[1]); NENT = int(sys.argv[2]) if len(sys.argv) > 2 else 8
R5 = Path(__file__).resolve().parent.parent / "teste_frente_a_r5" / "simular_r5.py"
spec = importlib.util.spec_from_file_location("simular_r5_lido", R5)
s5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s5)     # o main() do R5 nao roda (guarda de __main__)

por_texto, alvos_por_atomo = {}, {}
for f in s5.FONTES:
    o = s5.ORIG[f]
    ditos = [a for a in s5.ITENS if a in o["units"] and len(o["units"][a]) == 1]
    sinal = {a: next(iter(o["units"][a])) for a in ditos}
    invert, isolada = [], []
    for a in ditos:
        w = s5.tocar(o, [a], [], "T", a)
        if not s5.coerente(w):
            continue
        invert.append(a)
        outras = [b for b in ditos if b != a and s5.sentido(w, b)[0] != s5.sentido(o, b)[0]]
        if not outras:
            isolada.append(a)
    for a in isolada:
        alvos_por_atomo.setdefault(a, []).append(f)
    por_texto[f] = {"afirmacoes_ditas": len(ditos), "afirma": sum(1 for a in ditos if sinal[a] == 1),
                    "nega": sum(1 for a in ditos if sinal[a] == -1), "alvos_com_inversao_coerente": len(invert),
                    "alvos_isolados_(nenhuma_outra_dita_muda)": len(isolada), "lista_dos_alvos_isolados": isolada,
                    "ditas": ditos}
distintos = sorted(alvos_por_atomo)
# sorteio fixo: grupos com alvos DISTINTOS, repartidos o mais igualmente possivel pelos quatro textos
rng = random.Random(int(hashlib.sha256(b"r6:material:2026-11-16").hexdigest()[:12], 16))
ordem = distintos[:]; rng.shuffle(ordem)
carga = {f: 0 for f in s5.FONTES}; grupos = []
for a in sorted(ordem, key=lambda x: len(alvos_por_atomo[x])):               # primeiro os atomos com menos textos possiveis
    f = min(alvos_por_atomo[a], key=lambda t: (carga[t], s5.FONTES.index(t)))
    carga[f] += 1
    ditos = por_texto[f]["ditas"]
    outros = [b for b in ditos if b != a]; rng.shuffle(outros)
    entradas = sorted([a] + outros[:max(0, NENT - 1)], key=ditos.index)
    grupos.append({"texto": f, "alvo": a, "entradas_do_assento": entradas, "n": len(entradas)})
res = {"gerado_por": "material_r6.py", "catalogo": str(s5.CAT), "itens_do_catalogo": len(s5.ITENS), "por_texto": por_texto,
       "alvos_distintos_na_doutrina": len(distintos), "em_quantos_textos_cada_alvo_aparece": {a: len(v) for a, v in sorted(alvos_por_atomo.items())},
       "pares_texto_alvo": sum(len(v) for v in alvos_por_atomo.values()), "entradas_por_assento_pedidas": NENT,
       "grupos_com_alvo_distinto": len(grupos), "grupos_por_texto": carga, "grupos": grupos,
       "menor_assento": min(g["n"] for g in grupos) if grupos else 0}
saida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("itens do catalogo:", len(s5.ITENS))
for f, d in por_texto.items():
    print("%-11s ditas %2d (afirma %2d, nega %2d) | invertiveis %2d | isoladas %2d" % (f, d["afirmacoes_ditas"], d["afirma"], d["nega"], d["alvos_com_inversao_coerente"], d["alvos_isolados_(nenhuma_outra_dita_muda)"]))
print("pares texto x alvo:", res["pares_texto_alvo"], "| alvos distintos:", len(distintos))
print("grupos com alvo distinto:", len(grupos), "| por texto:", carga, "| menor assento:", res["menor_assento"])
print("gravado:", saida)

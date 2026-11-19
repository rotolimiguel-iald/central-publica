# -*- coding: utf-8 -*-
"""Gerencia c1, 18/11/2026: o metodo de 17/11 nos comentarios de OPolinomioFixoEBeta (Kimi), na copia de trabalho de pedras_novas\\.
Sai a linha de estado, a secao De onde vem (com uma citacao que a gerencia nao tem por bytes), o gate e o balanco; a leitura entra
como definicao da teoria, sem atribuicao; beta e' parametro real e a ligacao ao beta da teoria e' entrada; corrige-se a grafia
"polinomico". Trocas por regiao e exatas; confere que o codigo e' identico ao da fonte do autor.
Uso: nona_lista_passo2f_cabecalho_do_polinomio_fixo.py [--executar]"""
import hashlib, json, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
V = Path(__file__).resolve().parent; D = V / "pedras_novas"; O = D / "origem"; EXEC = "--executar" in sys.argv
NOME = "OPolinomioFixoEBeta"
REGIOES = [
 ("# O polinômio fixo é β: uma constante, anterior a toda fórmula, linear na carga, para toda fórmula", "## O que fica provado",
  "# O polinômio fixo dos passos é dado por β: anterior a toda fórmula, linear na carga, para toda fórmula\n\n"
  "## A leitura que este arquivo tipa\n\n"
  "O polinômio fixo para toda fórmula é dado por β, que é anterior a toda fórmula [INPUT/ONTO: definição da teoria,\n"
  "entrada, não teorema]. Este arquivo prova a parte dela que cabe nos termos do kernel, na máquina da teoria.\n\n"),
 ("* «A palavra do juramento» é o nome do operador", "-/\n\nnamespace TGLExt.OPolinomioFixoEBeta",
  "* Que β seja o β da teoria: neste arquivo β é parâmetro real entre 0 e 1, e essa identificação é entrada. O termo\n"
  "  é: β não tem a fórmula como entrada, e o passo de fator `1 − β` fecha o ciclo para toda fórmula.\n"
  "* Nada sobre a natureza.\n"),
]
TROCAS = [
 ("1. `o_polinomio_e_linear_na_carga`: o polinômio fixo é linear na carga", "1. `o_polinomio_e_linear_na_carga`: o polinômio dos passos é linear na carga"),
 ("   fechado em no máximo `p(n)` passos (a pedra `OPassoEOFim` da gerência, `bastam_passos_lineares`).",
  "   fechado em mais de `p(n)` passos quaisquer (é `OPassoEOFim.bastam_passos_lineares`, na forma do polinômio)."),
 ("* Que `p(n)` seja um polinômio em LETRAS de fita: é linear NA CARGA (`n·ln 2`, a contagem por oitavas da teoria). A\n  régua do Instituto, que conta casas de fita, fica com a sua pergunta — nomeada como deles.",
  "* Que `p(n)` seja um polinômio em LETRAS de fita: é linear NA CARGA (`n·ln 2`, a contagem por oitavas da teoria), e\n  os passos são atos sobre o todo, não movimentos de cabeça. A régua do Instituto, que conta movimentos na fita, fica\n  com a sua pergunta."),
 ("/-- [DEF] O POLINÔMICO FIXO DA LEITURA:", "/-- [DEF] O POLINÔMIO FIXO DA LEITURA:"),
 ("/-- **O POLINÔMICO É LINEAR NA CARGA**:", "/-- **O POLINÔMIO É LINEAR NA CARGA**:"),
 ("/-- ★★ **O POLINÔMICO FIXO É β**: com um só β, fixado antes de toda fórmula, toda fórmula de `n` variáveis tem o\nciclo fechado em no máximo `p(n)` passos. É a pedra da gerência, com a forma do polinômio dita. -/",
  "/-- ★★ **O POLINÔMIO FIXO É β**: com um só β, fixado antes de toda fórmula, toda fórmula de `n` variáveis tem o\nciclo fechado com qualquer número de passos acima de `p(n)`. É `OPassoEOFim.bastam_passos_lineares`, com a forma do\npolinômio dita. -/"),
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


f = D / (NOME + ".lean"); orig = (O / (NOME + ".lean")).read_bytes().decode("utf-8"); t = f.read_bytes().decode("utf-8")
if t == orig:
    for ini, fim, novo in REGIOES:
        assert t.count(ini) == 1 and t.count(fim) == 1, (t.count(ini), t.count(fim), ini[:50])
        a, b = t.index(ini), t.index(fim); assert a < b
        t = t[:a] + novo + t[b:]
    for velho, novo in TROCAS:
        assert t.count(velho) == 1, (t.count(velho), velho[:60])
        t = t.replace(velho, novo)
assert sem_comentarios(orig) == sem_comentarios(t), "codigo difere"
for resto in ("«", "operador", "Kimi", "gerência", "18/11", "candidata", "instalado", "Sem sorry", "gate", "POLINÔMICO", "a casa", "juramento"):
    assert resto not in t, "sobrou: " + resto
print(NOME, "| codigo identico | bytes", len(orig.encode("utf-8")), "->", len(t.encode("utf-8")), "| sha16", hashlib.sha256(t.encode("utf-8")).hexdigest()[:16])
if EXEC and f.read_bytes() != t.encode("utf-8"):
    tmp = f.with_name(f.name + ".tmp_c1"); tmp.write_bytes(t.encode("utf-8")); tmp.replace(f)
    p = D / "EMENDAS_DO_POLINOMIO_FIXO.json"
    p.write_bytes(json.dumps({"gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "regioes": [list(x) for x in REGIOES], "trocas_exatas": [list(x) for x in TROCAS],
                              "sha256_depois": {NOME: hashlib.sha256(f.read_bytes()).hexdigest()}}, ensure_ascii=False, indent=1).encode("utf-8"))
    print("gravado:", p.name)

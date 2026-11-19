#!/usr/bin/env python3
"""Mede entradas públicas K08 sem modelo e sem pesos.

Tokenizador fallback_bytes_v1: um token = um byte UTF-8. É um método exato,
não uma estimativa de cl100k/o200k ou de outro tokenizador de modelo.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path

ENTRADA_DIR = Path(__file__).resolve().parent
FORMULA_DIR = ENTRADA_DIR.parent / "FORMULA"
PUBLICO = Path(r"C:\IALD\Artigo\the_boundary")
RESULTADOS = FORMULA_DIR / "RESULTADOS_FORMULA.json"

# Letras/números Unicode; apóstrofo, hífen ou travessão internos não separam.
# Pontos e vírgulas separam: 46.828.680 contribui três palavras.
PALAVRA_RE = re.compile(r"[^\W_]+(?:['’\-–][^\W_]+)*", re.UNICODE)
BIBLIOTECAS = ("tiktoken", "tokenizers", "transformers", "sentencepiece")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def medir(path):
    data = path.read_bytes()
    texto = data.decode("utf-8")
    return {
        "arquivo": path.name,
        "bytes": len(data),
        "palavras": len(PALAVRA_RE.findall(texto)),
        "tokens": len(data),
        "sha256": sha256(data),
    }


def fmt(n):
    return f"{n:,}".replace(",", ".")


def main():
    resultados_doc = json.loads(RESULTADOS.read_text(encoding="utf-8"))
    resultados = {r["candidata"]: r for r in resultados_doc["resultados"]}
    disponibilidade = {m: bool(importlib.util.find_spec(m)) for m in BIBLIOTECAS}
    if any(disponibilidade.values()):
        raise RuntimeError(
            "Apareceu um tokenizador de referência; este script foi deliberadamente "
            "escrito para o fallback exato e não escolhe outra contagem automaticamente."
        )

    nomes = list(resultados)
    doc = {
        "tokenizador": {
            "nome": "fallback_bytes_v1",
            "regra": "cada byte UTF-8 é exatamente um token",
            "modelo_ou_pesos": False,
            "bibliotecas_de_referencia_no_python_gerenciado": disponibilidade,
            "ressalva": "não é contagem cl100k/o200k nem previsão do custo de um modelo específico",
        },
        "palavras": {
            "regex": PALAVRA_RE.pattern,
            "regra": "sequências Unicode alfanuméricas com apóstrofo/hífen/travessão interno; pontos e vírgulas separam",
        },
        "candidatas": {},
    }
    for nome in nomes:
        r = resultados[nome]
        completo = medir(PUBLICO / r["arquivo_publico"])
        compacto = medir(ENTRADA_DIR / r["arquivo_compacto"])
        controle = medir(ENTRADA_DIR / r["pc"]["arquivo_controle"])
        m = r["n_clausulas"]
        t = compacto["tokens"]
        doc["candidatas"][nome] = {
            "n_assercoes": r["n_assercoes"],
            "n_clausulas": m,
            "completo": completo,
            "compacto": compacto,
            "controle_pc": controle,
            "tokens_compacto_sobre_completo": t / completo["tokens"],
            "custo_texto": {
                "formula_geral": "C(r) = r × T; r é o número de entradas da fita, não o número de interações",
                "regra_do_desenho": "r = 1 por sessão, porque a fonte não volta depois do primeiro passo",
                "P_A_fonte_so_no_primeiro_passo": t,
                "P_B_fonte_so_no_primeiro_passo": t,
                "P_C_controle_so_no_primeiro_passo": controle["tokens"],
                "P_D_fonte_so_no_primeiro_passo": t,
                "fonte_completa_uma_fita_para_comparacao": completo["tokens"],
                "contrafactual_P_A_com_m_fitas_nao_usado": m * t,
            },
        }

    # Escolha explícita por clareza/completude; não há variável de desfecho.
    escolhida = "READ_BRIEF"
    doc["escolha"] = {
        "candidata": escolhida,
        "criterio": "clareza e completude do catálogo; custo só desempata",
        "razao": (
            "as oito partes separam axioma, constante, ação, gerador, dinâmica, estatuto, "
            "programa e instrumentos, com hipóteses e limites explícitos; README tem mais "
            "asserções no catálogo, mas mistura núcleo, painel, P=nP, selo e navegação"
        ),
        "nao_criterio": "nenhuma expectativa sobre P-A/P-B/P-C/P-D",
    }
    (ENTRADA_DIR / "MEDIDAS_ENTRADA.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    L = []
    add = L.append
    add("# Medidas das entradas — K08")
    add("")
    add("## 1. Método exato, sem modelo")
    add("")
    add("Não havia `tiktoken`, `tokenizers`, `transformers` ou `sentencepiece` no Python gerenciado. O executável local de tokenização do llama.cpp exige um modelo/pesos e por isso não foi usado. Em vez de baixar pesos ou apresentar uma estimativa como contagem de referência, adoto **`fallback_bytes_v1`: cada byte UTF-8 é exatamente um token**. Assim, nesta tabela, tokens = bytes por definição. É um tokenizador determinístico de 256 símbolos, sem modelo; **não é cl100k/o200k nem uma previsão do custo de um modelo específico**.")
    add("")
    add(f"Palavras são contadas pelo regex Unicode `{PALAVRA_RE.pattern}`. Apóstrofo, hífen ou travessão internos não separam; pontos e vírgulas separam. Bytes e SHA-256 são lidos do arquivo, nunca copiados de memória.")
    add("")
    add("## 2. Arquivos públicos completos")
    add("")
    add("| candidata | arquivo completo | bytes | palavras | tokens fallback | SHA-256 |")
    add("|---|---|---:|---:|---:|---|")
    for nome, d in doc["candidatas"].items():
        m = d["completo"]
        add(f"| {nome} | `{r_publico(nome, resultados)}` | {fmt(m['bytes'])} | {fmt(m['palavras'])} | {fmt(m['tokens'])} | `{m['sha256']}` |")
    add("")
    add("## 3. Recortes compactos e asserções sustentadas")
    add("")
    add("Os recortes são verbatim em caracteres e contêm todas as linhas usadas pelo catálogo nuclear; usam LF e uma linha em branco entre faixas, não identidade de bytes com um corte da origem. A contagem de asserções é a da fórmula validada, não uma alegação de que toda frase navegacional do arquivo seja uma asserção científica.")
    add("")
    add("| candidata | asserções | cláusulas | bytes | palavras | tokens fallback | tokens/completo | SHA-256 |")
    add("|---|---:|---:|---:|---:|---:|---:|---|")
    for nome, d in doc["candidatas"].items():
        m = d["compacto"]
        add(f"| {nome} | {d['n_assercoes']} | {d['n_clausulas']} | {fmt(m['bytes'])} | {fmt(m['palavras'])} | {fmt(m['tokens'])} | {d['tokens_compacto_sobre_completo']:.2%} | `{m['sha256']}` |")
    add("")
    add("**Escolha de trabalho: `READ_BRIEF`.** Ela separa as oito partes da teoria e escreve hipóteses, estatutos e limites com mais clareza que o sumário denso de `llms`; sustenta mais asserções do catálogo que `ABSTRACT` e `llms`. `README` tem a maior contagem, mas mistura núcleo, painel de resultado, P=nP, selo e navegação. O custo entra só como desempate. A escolha não usa nenhuma expectativa de desfecho.")
    add("")
    add("## 4. Custo de texto por sessão, em tokens")
    add("")
    add("Seja `T` o número de tokens do recorte e `r` o número de vezes que a fita entra. **C(r) = r × T**; interações sem a fita acrescentam zero token de texto-fonte. Pela regra deste desenho, a fonte não volta depois do primeiro passo, logo **r = 1 por sessão**. O número `m` de cláusulas pode limitar passos discretos, mas não multiplica o custo de fita. P-C usa o texto contraditório uma vez. Não se atribui à trava um pouso exato em tempo finito.")
    add("")
    add("Esses valores cobrem **somente o texto-fonte**. Tokens de estado/histórico, perguntas e saídas não têm serialização fixada nesta tarefa e não são inventados. O JSON conserva, apenas como contrafactual explicitamente não usado, quanto custaria devolver a fita em cada um dos `m` passos de P-A.")
    add("")
    add("| candidata | P-A: uma fita | P-B: uma fita | P-C: controle uma fita | P-D: uma fita | fonte completa: uma fita |")
    add("|---|---:|---:|---:|---:|---:|")
    for nome, d in doc["candidatas"].items():
        c = d["custo_texto"]
        add(f"| {nome} | {fmt(c['P_A_fonte_so_no_primeiro_passo'])} | {fmt(c['P_B_fonte_so_no_primeiro_passo'])} | {fmt(c['P_C_controle_so_no_primeiro_passo'])} | {fmt(c['P_D_fonte_so_no_primeiro_passo'])} | {fmt(c['fonte_completa_uma_fita_para_comparacao'])} |")
    add("")
    add("P-C tem dois custos diferentes que não se confundem: o **custo lógico mínimo de violação** é calculado em `RESULTADOS_FORMULA.json` e é maior que zero; o **custo de entrada** acima é o número de tokens para apresentar o controle uma vez.")
    add("")
    add("## 5. Reprodução")
    add("")
    add("Executar primeiro `python -B ../FORMULA/verificar_formula.py` e depois `python -B medir_entradas.py`. O segundo script não escolhe automaticamente outro tokenizador se uma biblioteca aparecer: ele falha para que a mudança de método seja explícita. Nenhum modelo foi executado; nada foi congelado.")
    (ENTRADA_DIR / "MEDIDAS_ENTRADA.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({nome: {
        "bytes_compacto": d["compacto"]["bytes"],
        "palavras": d["compacto"]["palavras"],
        "tokens": d["compacto"]["tokens"],
        "assercoes": d["n_assercoes"],
        "P_A_uma_fita": d["custo_texto"]["P_A_fonte_so_no_primeiro_passo"],
    } for nome, d in doc["candidatas"].items()}, ensure_ascii=False, indent=2))


def r_publico(nome, resultados):
    return resultados[nome]["arquivo_publico"]


if __name__ == "__main__":
    main()

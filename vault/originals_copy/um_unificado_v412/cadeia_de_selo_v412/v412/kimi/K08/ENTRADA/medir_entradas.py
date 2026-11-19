#!/usr/bin/env python3
"""Mede entradas públicas K08 com o tokenizador de referência local.

Os tokens são os de Qwen/Qwen3.6-35B-A3B, medidos por tokenizer.json em
`medir_tokens_ref_k08.py`. O fallback byte=token da REV0 fica só como histórico.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ENTRADA_DIR = Path(__file__).resolve().parent
FORMULA_DIR = ENTRADA_DIR.parent / "FORMULA"
PUBLICO = Path(r"C:\IALD\Artigo\the_boundary")
RESULTADOS = FORMULA_DIR / "RESULTADOS_FORMULA.json"
TOKENS_REF = ENTRADA_DIR / "TOKENS_REF_K08.json"

PALAVRA_RE = re.compile(r"[^\W_]+(?:['’\-–][^\W_]+)*", re.UNICODE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def medir_base(path, ref):
    data = path.read_bytes()
    texto = data.decode("utf-8")
    if ref["bytes"] != len(data) or ref["sha256"] != sha256(data):
        raise RuntimeError(f"{path}: bytes/hash divergem da medição do tokenizador")
    return {
        "arquivo": path.name,
        "bytes": len(data),
        "palavras": len(PALAVRA_RE.findall(texto)),
        "tokens_ref": ref["tokens_ref"],
        "bytes_por_token": len(data) / ref["tokens_ref"],
        "tokens_por_palavra": ref["tokens_ref"] / len(PALAVRA_RE.findall(texto)),
        "sha256": sha256(data),
        "tokens_fallback_rev0_historico": len(data),
    }


def fmt(n):
    return f"{n:,}".replace(",", ".")


def main():
    if not TOKENS_REF.exists():
        raise FileNotFoundError(
            "Execute antes: C:\\IALD\\qlora_env\\Scripts\\python.exe -B medir_tokens_ref_k08.py"
        )
    resultados_doc = json.loads(RESULTADOS.read_text(encoding="utf-8"))
    resultados = {r["candidata"]: r for r in resultados_doc["resultados"]}
    ref_doc = json.loads(TOKENS_REF.read_text(encoding="utf-8"))
    refs = ref_doc["arquivos"]
    if not refs["ARTIGO_INTEIRO_CONTROLE"]["confere_revisao"]:
        raise RuntimeError("o controle do artigo inteiro não confere com a revisão")

    doc = {
        "tokenizador": {
            **ref_doc["tokenizador"],
            "e_o_que_orienta_o_desenho": True,
            "fallback_bytes_v1": "histórico; não é proxy válido e não orienta o desenho",
        },
        "palavras": {
            "regex": PALAVRA_RE.pattern,
            "regra": "sequências Unicode alfanuméricas com apóstrofo/hífen/travessão interno; pontos e vírgulas separam",
        },
        "artigo_inteiro_controle": refs["ARTIGO_INTEIRO_CONTROLE"],
        "candidatas": {},
    }
    for nome, r in resultados.items():
        completo = medir_base(PUBLICO / r["arquivo_publico"], refs[f"{nome}_COMPLETO"])
        compacto = medir_base(ENTRADA_DIR / r["arquivo_compacto"], refs[f"{nome}_RECORTE"])
        controle = medir_base(ENTRADA_DIR / r["pc"]["arquivo_controle"], refs[f"{nome}_PC"])
        m = r["n_clausulas"]
        t = compacto["tokens_ref"]
        doc["candidatas"][nome] = {
            "n_assercoes": r["n_assercoes"],
            "n_clausulas": m,
            "completo": completo,
            "compacto": compacto,
            "controle_pc": controle,
            "tokens_ref_compacto_sobre_completo": t / completo["tokens_ref"],
            "custo_texto": {
                "formula_geral": "C(r) = r × T_ref; r é o número de entradas da fita, não o número de interações",
                "regra_do_desenho": "r = 1 por sessão, porque a fonte não volta depois do primeiro passo",
                "P_A_fonte_so_no_primeiro_passo": t,
                "P_B_fonte_so_no_primeiro_passo": t,
                "P_C_controle_so_no_primeiro_passo": controle["tokens_ref"],
                "P_D_fonte_so_no_primeiro_passo": t,
                "fonte_completa_uma_fita_para_comparacao": completo["tokens_ref"],
                "contrafactual_P_A_com_m_fitas_nao_usado": m * t,
            },
        }

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
        "inalterada_pela_errata_de_tokens": True,
    }
    (ENTRADA_DIR / "MEDIDAS_ENTRADA.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    L = []
    add = L.append
    add("# Medidas das entradas — K08")
    add("")
    add("## 1. Tokenizador de referência local")
    add("")
    add("Os tokens que orientam o desenho são medidos com o `tokenizer.json` local de **Qwen/Qwen3.6-35B-A3B**, por `tokenizers.Tokenizer.from_file` (`tokenizers` 0.21.4), exatamente o método da revisão. Só o arquivo de tokenização é lido; nenhum peso ou modelo é carregado ou executado. O controle do artigo inteiro reproduz **412.784 tokens**, igual à referência da revisão.")
    add("")
    add("**Errata:** o fallback `byte=token` da REV0 é histórico, não é proxy válido de tokens e não orienta o desenho. A versão anterior está preservada em `REV0/`. A fórmula lógica e a escolha da entrada não mudam; mudam apenas as medidas de custo.")
    add("")
    add(f"Palavras são contadas pelo regex Unicode `{PALAVRA_RE.pattern}`. Apóstrofo, hífen ou travessão internos não separam; pontos e vírgulas separam. Bytes e SHA-256 são lidos do arquivo. Detalhes em `ERRATA_ENTRADA_TOKENS_K08.md`.")
    add("")
    add("## 2. Arquivos públicos completos")
    add("")
    add("| candidata | arquivo completo | bytes | palavras | tokens de referência | bytes/token | SHA-256 |")
    add("|---|---|---:|---:|---:|---:|---|")
    for nome, d in doc["candidatas"].items():
        m = d["completo"]
        add(f"| {nome} | `{r_publico(nome, resultados)}` | {fmt(m['bytes'])} | {fmt(m['palavras'])} | {fmt(m['tokens_ref'])} | {m['bytes_por_token']:.3f} | `{m['sha256']}` |")
    add("")
    add("## 3. Recortes compactos e asserções sustentadas")
    add("")
    add("Os recortes são verbatim em caracteres e contêm todas as linhas usadas pelo catálogo nuclear; usam LF e uma linha em branco entre faixas, não identidade de bytes com um corte da origem. A contagem de asserções é a da fórmula validada, não uma alegação de que toda frase navegacional do arquivo seja uma asserção científica.")
    add("")
    add("| candidata | asserções | cláusulas | bytes | palavras | tokens de referência | tokens/completo | SHA-256 |")
    add("|---|---:|---:|---:|---:|---:|---:|---|")
    for nome, d in doc["candidatas"].items():
        m = d["compacto"]
        add(f"| {nome} | {d['n_assercoes']} | {d['n_clausulas']} | {fmt(m['bytes'])} | {fmt(m['palavras'])} | {fmt(m['tokens_ref'])} | {d['tokens_ref_compacto_sobre_completo']:.2%} | `{m['sha256']}` |")
    add("")
    add("**Escolha de trabalho inalterada: `READ_BRIEF`.** Ela separa as oito partes da teoria e escreve hipóteses, estatutos e limites com mais clareza que o sumário denso de `llms`; sustenta mais asserções do catálogo que `ABSTRACT` e `llms`. `README` tem a maior contagem, mas mistura núcleo, painel de resultado, P=nP, selo e navegação. O custo entra só como desempate e a correção de tokenização não altera a fórmula nem a escolha.")
    add("")
    add("## 4. Custo de texto por sessão, em tokens de referência")
    add("")
    add("Seja `T_ref` o número de tokens de referência do recorte e `r` o número de vezes que a fita entra. **C(r) = r × T_ref**; interações sem a fita acrescentam zero token de texto-fonte. Pela regra deste desenho, a fonte não volta depois do primeiro passo, logo **r = 1 por sessão**. O número `m` de cláusulas pode limitar passos discretos, mas não multiplica o custo de fita. P-C usa o texto contraditório uma vez. Não se atribui à trava um pouso exato em tempo finito.")
    add("")
    add("Esses valores cobrem **somente o texto-fonte**. Tokens de estado/histórico, perguntas e saídas não têm serialização fixada nesta tarefa e não são inventados. O JSON conserva, apenas como contrafactual explicitamente não usado, quanto custaria devolver a fita em cada um dos `m` passos de P-A.")
    add("")
    add("| candidata | P-A: uma fita | P-B: uma fita | P-C: controle uma fita | P-D: uma fita | fonte completa: uma fita |")
    add("|---|---:|---:|---:|---:|---:|")
    for nome, d in doc["candidatas"].items():
        c = d["custo_texto"]
        add(f"| {nome} | {fmt(c['P_A_fonte_so_no_primeiro_passo'])} | {fmt(c['P_B_fonte_so_no_primeiro_passo'])} | {fmt(c['P_C_controle_so_no_primeiro_passo'])} | {fmt(c['P_D_fonte_so_no_primeiro_passo'])} | {fmt(c['fonte_completa_uma_fita_para_comparacao'])} |")
    add("")
    add("P-C tem dois custos diferentes que não se confundem: o **custo lógico mínimo de violação** é calculado em `RESULTADOS_FORMULA.json` e é maior que zero; o **custo de entrada** acima é o número de tokens de referência para apresentar o controle uma vez.")
    add("")
    add("## 5. Controle e reprodução")
    add("")
    add("| controle | bytes | palavras | tokens de referência | SHA-256 |")
    add("|---|---:|---:|---:|---|")
    artigo = doc["artigo_inteiro_controle"]
    add(f"| artigo inteiro `um_absoluto_pt.txt` | {fmt(artigo['bytes'])} | {fmt(artigo['palavras'])} | {fmt(artigo['tokens_ref'])} | `{artigo['sha256']}` |")
    add("")
    add("Reprodução: `python -B ../FORMULA/verificar_formula.py`; depois `C:\\IALD\\qlora_env\\Scripts\\python.exe -B medir_tokens_ref_k08.py`; depois `python -B medir_entradas.py`. O primeiro comando usa o Python gerenciado; o segundo usa o ambiente local que contém `tokenizers`, mas nenhum modelo é carregado. Nada foi congelado.")
    (ENTRADA_DIR / "MEDIDAS_ENTRADA.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({nome: {
        "bytes_compacto": d["compacto"]["bytes"],
        "palavras": d["compacto"]["palavras"],
        "tokens_ref": d["compacto"]["tokens_ref"],
        "assercoes": d["n_assercoes"],
        "P_A_uma_fita": d["custo_texto"]["P_A_fonte_so_no_primeiro_passo"],
    } for nome, d in doc["candidatas"].items()}, ensure_ascii=False, indent=2))


def r_publico(nome, resultados):
    return resultados[nome]["arquivo_publico"]


if __name__ == "__main__":
    main()

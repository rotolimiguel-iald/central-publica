#!/usr/bin/env python3
"""Auditoria final independente dos arquivos K08; só lê e imprime."""
from __future__ import annotations

import hashlib
import json
import re

from catalogo_assercoes import ENTRADA_DIR, FONTES, FORMULA_DIR, texto_compacto
from verificar_formula import NEGACAO_BETA

PALAVRA_RE = re.compile(r"[^\W_]+(?:['’\-–][^\W_]+)*", re.UNICODE)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    medidas = json.loads((ENTRADA_DIR / "MEDIDAS_ENTRADA.json").read_text(encoding="utf-8"))
    formulas = json.loads((FORMULA_DIR / "RESULTADOS_FORMULA.json").read_text(encoding="utf-8"))
    adversarios = json.loads((FORMULA_DIR / "RESULTADOS_ADVERSARIOS.json").read_text(encoding="utf-8"))
    tokens = json.loads((ENTRADA_DIR / "TOKENS_REF_K08.json").read_text(encoding="utf-8"))
    manifestos = (
        ENTRADA_DIR / "MANIFESTO_ENTRADA_K08.json",
        FORMULA_DIR / "MANIFESTO_FORMULA_K08.json",
    )
    for manifesto in manifestos:
        doc = json.loads(manifesto.read_text(encoding="utf-8"))
        for item in doc["arquivos"]:
            path = manifesto.parent.parent / item["arquivo"]
            if not path.exists() or path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
                raise AssertionError(f"manifesto divergente em {item['arquivo']}")
    artigo = tokens["arquivos"]["ARTIGO_INTEIRO_CONTROLE"]
    if artigo["tokens_ref"] != 412_784 or not artigo["confere_revisao"]:
        raise AssertionError("o controle do artigo inteiro divergiu da revisão")
    tokenizador = tokens["tokenizador"]
    if tokenizador["pesos_ou_modelo_lidos"] or sha(ENTRADA_DIR / tokenizador["arquivo_local"]) != tokenizador["sha256_tokenizer"]:
        raise AssertionError("o tokenizador local não confere")
    if not (ENTRADA_DIR / "REV0" / "MEDIDAS_ENTRADA.json").exists():
        raise AssertionError("REV0 não foi preservada")
    if not (ENTRADA_DIR / "ERRATA_ENTRADA_TOKENS_K08.md").exists():
        raise AssertionError("errata de tokens ausente")
    if not (FORMULA_DIR / "REV0" / "ADVERSARIOS_K08.md").exists():
        raise AssertionError("FORMULA/REV0 não foi preservada")
    if not (FORMULA_DIR / "ERRATA_ADVERSARIOS_K08_15nov.md").exists():
        raise AssertionError("errata de adversários ausente")
    por_formula = {r["candidata"]: r for r in formulas["resultados"]}
    por_adversario = {r["candidata"]: r for r in adversarios["candidatas"]}
    resumo = {}
    for nome in FONTES:
        candidata = ENTRADA_DIR / f"CANDIDATA_{nome}.md"
        controle = ENTRADA_DIR / f"CONTROLE_PC_{nome}.md"
        esperado = texto_compacto(nome)
        if candidata.read_text(encoding="utf-8") != esperado:
            raise AssertionError(f"{nome}: recorte fora das faixas ou alterado")
        if b"\r" in candidata.read_bytes():
            raise AssertionError(f"{nome}: recorte contém CR; o contrato é LF")
        esperado_pc = esperado + "\n" + NEGACAO_BETA + "\n"
        if controle.read_text(encoding="utf-8") != esperado_pc:
            raise AssertionError(f"{nome}: P-C não é o mesmo texto mais a negação mínima")
        m = medidas["candidatas"][nome]
        pares = (
            ("compacto", candidata, tokens["arquivos"][f"{nome}_RECORTE"]),
            ("controle_pc", controle, tokens["arquivos"][f"{nome}_PC"]),
        )
        for chave, path, ref in pares:
            dados = path.read_bytes()
            texto = dados.decode("utf-8")
            if m[chave]["bytes"] != len(dados):
                raise AssertionError(f"{nome}/{chave}: bytes divergem")
            if m[chave]["tokens_ref"] != ref["tokens_ref"]:
                raise AssertionError(f"{nome}/{chave}: tokens de referência divergem")
            if "tokens" in m[chave]:
                raise AssertionError(f"{nome}/{chave}: coluna fallback ainda aparece como tokens")
            if m[chave]["tokens_fallback_rev0_historico"] != len(dados):
                raise AssertionError(f"{nome}/{chave}: histórico byte=token diverge dos bytes")
            if m[chave]["palavras"] != len(PALAVRA_RE.findall(texto)):
                raise AssertionError(f"{nome}/{chave}: palavras divergem")
            if m[chave]["sha256"] != sha(path):
                raise AssertionError(f"{nome}/{chave}: hash diverge")
        f = por_formula[nome]
        if f["n_leituras_validas"] < 2 or f["distancia_minima_hamming"] != 1:
            raise AssertionError(f"{nome}: P-B perdeu as duas leituras")
        if f["pc"]["satisfazivel"] or f["pc"]["custo_minimo"] == 0:
            raise AssertionError(f"{nome}: P-C não é insatisfazível/custo positivo")
        if f["empurrao_fora"]["depois_custo"] == 0 or f["empurrao_dentro"]["depois_custo"] != 0:
            raise AssertionError(f"{nome}: empurrões trocaram de classe")
        a = por_adversario[nome]["mecanismos"]
        for rotulo in ("âncora na primeira leitura", "moda do histórico", "ignora o empurrão"):
            if a[rotulo]["E2"]["preserva_empurrada"] or not a[rotulo]["E2"]["volta_ao_anterior"]:
                raise AssertionError(f"{nome}/{rotulo}: E2 não apagou a troca válida como esperado")
            if not a[rotulo]["E3"]["volta_ao_anterior"]:
                raise AssertionError(f"{nome}/{rotulo}: E3 externo ausente")
        if not a["cópia da última"]["E3"]["preserva_empurrada"]:
            raise AssertionError(f"{nome}/cópia: E3 externo inesperado")
        sem_memoria = a["leitor sem memória (fonte → leitura)"]
        if not sem_memoria["sem_regra_sem_fonte"] or sem_memoria["E1_primeira_leitura"]["custo"] != 0:
            raise AssertionError(f"{nome}/sem memória: fonte→leitura ou ausência de regra falhou")
        for rotulo, r in a.items():
            if "sem_leitura" in r["P_C"]:
                if r["P_C"]["custo_minimo"] == 0:
                    raise AssertionError(f"{nome}/{rotulo}: P-C zerou")
            elif r["P_C"]["custo_final"] == 0:
                raise AssertionError(f"{nome}/{rotulo}: P-C zerou")
        resumo[nome] = {
            "sha256_candidata": sha(candidata),
            "sha256_controle": sha(controle),
            "tokens_ref": m["compacto"]["tokens_ref"],
            "assercoes": f["n_assercoes"],
            "pc_custo": f["pc"]["custo_minimo"],
            "mecanismos": len(a),
        }
    proibidos = ("ENTREGA", "PROTOCOLO", "REGISTRO_MAPA", "PERGUNTA", "DEPOSITO")
    for base in (FORMULA_DIR, ENTRADA_DIR):
        for path in base.iterdir():
            if path.is_file() and any(termo in path.name.upper() for termo in proibidos):
                raise AssertionError(f"arquivo fora do escopo: {path}")
    print(json.dumps({"status": "OK", "artigo_controle_tokens_ref": artigo["tokens_ref"], "candidatas": resumo}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

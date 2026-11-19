#!/usr/bin/env python3
"""Gera e valida os dois braços isomorfos sintéticos, sem executar modelos."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(RAIZ.parent / "EXTRACAO"))

from extrator_fechado import pontuar, render_resposta  # noqa: E402
from maquina_isomorfa import (  # noqa: E402
    achados_numericos,
    avaliar_formula,
    formula_base,
    gabarito_sem_nome,
    inserir_contradicao,
    numeros,
    transformar_assercoes,
    transformar_texto,
    validar_reintroducoes,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def escrever_json(nome: str, payload) -> None:
    (RAIZ / nome).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def escrever_texto(nome: str, texto: str) -> None:
    (RAIZ / nome).write_text(texto + "\n", encoding="utf-8")


def rotulos(assercoes):
    return [{"id": item["id"], "resposta": item["gabarito"]} for item in assercoes]


def main() -> None:
    dicionario_bruto = (RAIZ / "dicionario_sintetico_v1.json").read_bytes()
    fontes_bruto = (RAIZ / "fontes_sinteticas.json").read_bytes()
    dicionario = json.loads(dicionario_bruto.decode("utf-8"))
    fontes = json.loads(fontes_bruto.decode("utf-8"))
    checks = []

    def check(nome, condicao, detalhe=""):
        checks.append({"check": nome, "ok": bool(condicao), "detail": detalhe})

    resultados = {}
    for braco, chave, contrafactual in (
        ("CONTRAFACTUAL_NUMERICO", "numeric", True),
        ("RESTRITO_SEM_NUMEROS", "qualitative", False),
    ):
        fonte = fontes[chave]
        texto_iso, auditoria = transformar_texto(fonte["text"], dicionario, contrafactual)
        assercoes_iso = transformar_assercoes(fonte["assertions"], dicionario, contrafactual)
        formula_iso = formula_base(fonte, dicionario, contrafactual)
        avaliacao_base = avaliar_formula(formula_iso)

        texto_sem_nome_original = inserir_contradicao(fonte)
        texto_sem_nome, auditoria_sem_nome = transformar_texto(texto_sem_nome_original, dicionario, contrafactual)
        literal = formula_iso[0]
        formula_sem_nome = formula_iso + [{"atom": literal["atom"], "polarity": -literal["polarity"]}]
        avaliacao_sem_nome = avaliar_formula(formula_sem_nome)
        assercoes_sem_nome = gabarito_sem_nome(assercoes_iso, formula_sem_nome)

        lexical = validar_reintroducoes(fonte["text"], texto_iso, dicionario, contrafactual)
        lexical_sem_nome = validar_reintroducoes(texto_sem_nome_original, texto_sem_nome, dicionario, contrafactual)

        resposta_original = render_resposta(rotulos(fonte["assertions"]))
        resposta_iso = render_resposta(rotulos(assercoes_iso))
        resposta_sem_nome = render_resposta(rotulos(assercoes_sem_nome))
        score_original = pontuar(resposta_original, fonte["assertions"])
        score_iso = pontuar(resposta_iso, assercoes_iso)
        score_sem_nome = pontuar(resposta_sem_nome, assercoes_sem_nome)

        ancora_iso, _ = transformar_texto(fonte["contradiction_after"], dicionario, contrafactual, exigir_numeros=False)
        insercao_iso, _ = transformar_texto(fonte["contradiction_sentence"], dicionario, contrafactual, exigir_numeros=False)
        restaurado = texto_sem_nome.replace(ancora_iso + " " + insercao_iso, ancora_iso, 1)

        check(braco + "_BASE_SAT", avaliacao_base["satisfiable"] and avaliacao_base["min_cost"] == 0)
        check(braco + "_SEM_NOME_INSAT", avaliacao_sem_nome["nome_vazio"] and avaliacao_sem_nome["min_cost"] == 1)
        check(braco + "_SEM_NOME_UMA_INSERCAO", restaurado == texto_iso)
        check(braco + "_DISFARCE_LEXICAL", lexical["lexical_disguise_ok"], str(lexical["source_tokens_reintroduced"]))
        check(braco + "_DISFARCE_LEXICAL_SEM_NOME", lexical_sem_nome["lexical_disguise_ok"], str(lexical_sem_nome["source_tokens_reintroduced"]))
        check(braco + "_IDS_PRESERVADOS", [x["id"] for x in fonte["assertions"]] == [x["id"] for x in assercoes_iso])
        check(braco + "_GABARITO_EQUIVARIANTE", [x["gabarito"] for x in fonte["assertions"]] == [x["gabarito"] for x in assercoes_iso])
        check(braco + "_MESMO_EXTRATOR_BASE", score_original["format_ok"] and score_original["correct"] == score_original["total"])
        check(braco + "_MESMO_EXTRATOR_ISO", score_iso["format_ok"] and score_iso["correct"] == score_iso["total"])
        check(braco + "_MESMO_EXTRATOR_SEM_NOME", score_sem_nome["format_ok"] and score_sem_nome["correct"] == score_sem_nome["total"])
        itens_base_atom = [x for x in assercoes_iso if x.get("atom") == literal["atom"]]
        check(
            braco + "_TEXTOS_DE_POLARIDADE_DISTINTOS",
            len(itens_base_atom) == 2
            and len({x["assertion"] for x in itens_base_atom}) == 2
            and {x["polarity"] for x in itens_base_atom} == {-1, 1},
        )
        itens_atom = [x for x in assercoes_sem_nome if x.get("atom") == literal["atom"]]
        check(braco + "_P_E_NAO_P_AMBOS_SIM", len(itens_atom) == 2 and all(x["gabarito"] == "SIM" for x in itens_atom))

        guarda = None
        if contrafactual:
            antes = numeros(fonte["text"])
            depois = numeros(texto_iso)
            check("NUMEROS_COM_HISTORIA_ALTERADOS", bool(antes) and not (set(antes) & set(depois)), f"{antes} -> {depois}")
            valores = [float(x.replace(",", ".")) for x in depois]
            check(
                "CONTRAFACTUAL_RELACAO_COERENTE",
                len(valores) == 2 and valores[0] > valores[1] and formula_iso[0]["polarity"] == 1 and "mais rápida" in texto_iso,
                "A segunda duração é menor; a afirmação dependente precisa ser 'mais rápida'.",
            )
            check("CONTRAFACTUAL_UNIDADE_PRESERVADA", texto_iso.count("segundos") == fonte["text"].count("segundos"))
        else:
            palavras = dicionario["numeric_free_policy"]["numeric_word_list"]
            corpus_original = " ".join([fonte["text"]] + [x["assertion"] for x in fonte["assertions"]])
            corpus_iso = " ".join([texto_iso] + [x["assertion"] for x in assercoes_iso])
            guarda = {
                "before": achados_numericos(corpus_original, palavras),
                "after": achados_numericos(corpus_iso, palavras),
                "no_name_after": achados_numericos(texto_sem_nome, palavras),
                "scope": dicionario["numeric_free_policy"]["guard_scope"],
            }
            check("RESTRICAO_SEM_NUMEROS_ORIGINAL", not guarda["before"], str(guarda["before"]))
            check("RESTRICAO_SEM_NUMEROS_ISO", not guarda["after"], str(guarda["after"]))
            check("RESTRICAO_SEM_NUMEROS_SEM_NOME", not guarda["no_name_after"], str(guarda["no_name_after"]))

        resultados[braco] = {
            "source_key": chave,
            "counterfactual_numeric": contrafactual,
            "original_text": fonte["text"],
            "iso_text": texto_iso,
            "no_name_text": texto_sem_nome,
            "numeric_audit": auditoria,
            "no_name_numeric_audit": auditoria_sem_nome,
            "formula_base": avaliacao_base,
            "formula_no_name": avaliacao_sem_nome,
            "lexical_audit": lexical,
            "no_name_lexical_audit": lexical_sem_nome,
            "numeric_free_guard": guarda,
            "assertions_iso": assercoes_iso,
            "assertions_no_name": assercoes_sem_nome,
            "wiring_scores": {
                "original": {"format_ok": score_original["format_ok"], "correct": score_original["correct"], "total": score_original["total"]},
                "iso": {"format_ok": score_iso["format_ok"], "correct": score_iso["correct"], "total": score_iso["total"]},
                "no_name": {"format_ok": score_sem_nome["format_ok"], "correct": score_sem_nome["correct"], "total": score_sem_nome["total"]},
                "meaning": "Fiação e formato por construção; não mede convergência nem desempenho de modelo.",
            },
        }

    # Controles negativos: o teste passa somente quando o defeito é detectado.
    def erro_valor(funcao):
        try:
            funcao()
        except ValueError as exc:
            return str(exc)
        return None

    erro_sem_politica = erro_valor(
        lambda: transformar_texto(fontes["numeric"]["text"] + " O valor auxiliar foi 9,9.", dicionario, True)
    )
    check("NEG_NUMERO_SEM_POLITICA_E_REJEITADO", erro_sem_politica is not None and "NUMERO_SEM_POLITICA" in erro_sem_politica, str(erro_sem_politica))

    dicionario_identidade = json.loads(dicionario_bruto.decode("utf-8"))
    dicionario_identidade["counterfactual_numeric"]["number_map"]["40,0"] = "40,0"
    erro_intacto = erro_valor(
        lambda: transformar_texto(fontes["numeric"]["text"], dicionario_identidade, True)
    )
    check("NEG_NUMERO_INTACTO_E_REJEITADO", erro_intacto is not None and "NUMERO_ORIGINAL_INTACTO" in erro_intacto, str(erro_intacto))

    achados_indevidos = achados_numericos(
        fontes["numeric"]["text"], dicionario["numeric_free_policy"]["numeric_word_list"]
    )
    check("NEG_GUARDA_SEM_NUMEROS_REJEITA_NUMERICO", bool(achados_indevidos), str(achados_indevidos))

    reintroducao = validar_reintroducoes(
        fontes["numeric"]["text"],
        resultados["CONTRAFACTUAL_NUMERICO"]["iso_text"] + " laboratório Aurora",
        dicionario,
        True,
    )
    check("NEG_REINTRODUCAO_LEXICAL_E_DETECTADA", not reintroducao["lexical_disguise_ok"])
    controles_negativos = {
        "unlisted_number_error": erro_sem_politica,
        "unchanged_number_error": erro_intacto,
        "numeric_findings_in_restricted_arm": achados_indevidos,
        "deliberate_lexical_reintroduction": reintroducao,
    }

    numerico = resultados["CONTRAFACTUAL_NUMERICO"]
    qualitativo = resultados["RESTRITO_SEM_NUMEROS"]
    escrever_texto("texto_original_numerico_sintetico.txt", numerico["original_text"])
    escrever_texto("texto_contrafactual_isomorfo.txt", numerico["iso_text"])
    escrever_json("gabarito_contrafactual_isomorfo.json", {"assertions": numerico["assertions_iso"]})
    escrever_texto("texto_sem_nome_contrafactual.txt", numerico["no_name_text"])
    escrever_json("gabarito_sem_nome_contrafactual.json", {"assertions": numerico["assertions_no_name"]})
    escrever_texto("texto_sem_numeros_original_sintetico.txt", qualitativo["original_text"])
    escrever_texto("texto_sem_numeros_isomorfo.txt", qualitativo["iso_text"])
    escrever_json("gabarito_sem_numeros_isomorfo.json", {"assertions": qualitativo["assertions_iso"]})
    escrever_texto("texto_sem_nome_sem_numeros.txt", qualitativo["no_name_text"])
    escrever_json("gabarito_sem_nome_sem_numeros.json", {"assertions": qualitativo["assertions_no_name"]})

    sondas = []
    for item in fontes["numeric"]["assertions"]:
        sondas.append({
            "probe_id": "MEM_" + item["id"],
            "assertion_kept_from_original": item["assertion"],
            "expected_on_original": item["gabarito"],
            "expected_on_counterfactual_iso": item["memory_probe_gabarito_on_iso"],
            "label_changed": item["gabarito"] != item["memory_probe_gabarito_on_iso"],
        })
    escrever_json("sondas_memoria_contrafactual.json", {
        "scope": "Diagnóstico separado; as sondas preservam afirmações originais para detectar resposta pela história, não integram o texto principal.",
        "changed_count": sum(x["label_changed"] for x in sondas),
        "probes": sondas,
    })

    alternativas = {
        "selected_arm": None,
        "selection_hidden": False,
        "alternatives": [
            {
                "id": "i_CONTRAFACTUAL_FACTUAL_COERENTE",
                "testable_now": True,
                "testable_scope": "Números alterados, dependência comparativa, gabarito, sondas de memória e mesmo extrator no exemplo sintético.",
                "strict_factual_isomorphism": False,
                "open_for_real_texts": "Curadoria independente de coerência e dificuldade; medidas publicadas não podem ser trocadas como rótulos.",
                "source_numbers_left_intact": sorted(set(numerico["numeric_audit"]["numbers_before"]) & set(numerico["numeric_audit"]["numbers_after"])),
            },
            {
                "id": "ii_RESTRICAO_A_TEXTOS_SEM_NUMEROS",
                "testable_now": True,
                "testable_scope": "Renomeação, gabarito, contradição mínima e mesmo extrator no texto qualitativo sintético.",
                "strict_factual_isomorphism": True,
                "open_for_real_texts": "O guarda é lexical; fora do subdomínio sem números a previsão não se aplica.",
                "numeric_guard": qualitativo["numeric_free_guard"],
            },
        ],
    }
    escrever_json("alternativas_numericas.json", alternativas)

    falhas = [x["check"] for x in checks if not x["ok"]]
    validacao = {
        "schema": "k08-r4-isomorph-validation-v1",
        "model_calls": 0,
        "llm_judge": False,
        "production_certified": False,
        "dictionary_id": dicionario["dictionary_id"],
        "dictionary_version": dicionario["version"],
        "dictionary_sha256": sha256_bytes(dicionario_bruto),
        "sources_sha256": sha256_bytes(fontes_bruto),
        "checks": checks,
        "failures": falhas,
        "negative_controls": controles_negativos,
        "development_failures_corrected": [
            "A primeira transformação unidirecional colidiu N03/N04; a inspeção detectou, o par comparativo foi tornado bidirecional e o check TEXTOS_DE_POLARIDADE_DISTINTOS foi acrescentado."
        ],
        "arms": resultados,
        "limits": [
            "Todas as saídas de respondedor são geradas do gabarito para testar fiação; nenhum modelo foi executado.",
            "A contrafactual não é isomorfo factual estrito; é um texto sintético com fatos alterados e documentados.",
            "O guarda sem números é lexical e restringe o domínio; não detecta toda quantidade implícita.",
            "A equivalência de dificuldade, o desempenho real e a ausência de contaminação fora destes casos continuam abertos.",
            "Custo mínimo zero/um é da fórmula sintética declarada, não uma prova sobre um texto público ou sobre a natureza.",
        ],
    }
    escrever_json("validacao_isomorfo.json", validacao)
    escrever_json("formulas_avaliadas.json", {
        "contrafactual_base": numerico["formula_base"],
        "contrafactual_sem_nome": numerico["formula_no_name"],
        "sem_numeros_base": qualitativo["formula_base"],
        "sem_numeros_sem_nome": qualitativo["formula_no_name"],
    })

    linhas = [
        "# RELATÓRIO ISOMORFO K08/R4",
        "",
        f"Dicionário `{dicionario['dictionary_id']}`, versão {dicionario['version']}, SHA-256 `{sha256_bytes(dicionario_bruto)}`. Nenhum modelo, artigo público, T6 ou resultado real foi usado.",
        "",
        f"Verificações: {len(checks) - len(falhas)}/{len(checks)} aprovadas; falhas: {', '.join(falhas) or 'nenhuma'}. Todas as taxas de acerto abaixo são fiação por construção, não desempenho.",
        "",
        "Quatro controles negativos confirmam que número sem política, número intacto, número no braço restrito e reintrodução lexical deliberada são detectados. Na história de desenvolvimento, uma colisão N03/N04 foi encontrada pela inspeção e corrigida; o teste `TEXTOS_DE_POLARIDADE_DISTINTOS` agora impede essa regressão.",
        "",
        "## Alternativas numéricas, sem escolha",
        "",
        "| Alternativa | O que é testável agora | Limite constitutivo |",
        "|---|---|---|",
        "| (i) Contrafactual factual coerente | As duas durações mudam; nenhuma fica intacta; unidade e número de oscilações são preservados; a relação muda para ‘mais rápida’; gabarito e sondas acompanham. | Não é isomorfo factual estrito. Em texto real exige curadoria independente; não se troca medida da natureza como rótulo. |",
        "| (ii) Restrição a textos sem números | Renomeação, gabarito, contradição mínima e mesmo extrator passam no exemplo qualitativo; guarda lexical antes/depois sem achados. | Não testa contaminação numérica e não se aplica a textos com números; o guarda não é prova semântica geral. |",
        "",
        "As duas são testáveis, mas respondem a escopos diferentes. A primeira testa diretamente história numérica ao preço de alterar fatos; a segunda preserva o isomorfismo qualitativo ao preço de excluir números. `selected_arm=null`; nenhuma foi escolhida.",
        "",
        "## Mesma máquina e mesmo extrator",
        "",
        "| Braço | Base | Isomorfo | Sem Nome | Interpretação |",
        "|---|---:|---:|---:|---|",
    ]
    for nome, r in resultados.items():
        w = r["wiring_scores"]
        linhas.append(
            f"| {nome} | {w['original']['correct']}/{w['original']['total']} | {w['iso']['correct']}/{w['iso']['total']} | "
            f"{w['no_name']['correct']}/{w['no_name']['total']} | Formato/fiação, não convergência |"
        )
    linhas += [
        "",
        f"As sondas contrafactuais preservam afirmações originais fora do texto principal; {sum(x['label_changed'] for x in sondas)}/{len(sondas)} rótulos devem mudar no novo texto. Elas tornam testável a distinção entre seguir a história e seguir o contrafactual, mas não medem um modelo nesta rodada.",
        "",
        "## Sem Nome",
        "",
        "| Braço | Base: custo mínimo / leituras zero | Sem Nome: custo mínimo / leituras zero | Uma inserção restaura a base | Disfarce lexical |",
        "|---|---:|---:|---:|---:|",
    ]
    for nome, r in resultados.items():
        linhas.append(
            f"| {nome} | {r['formula_base']['min_cost']} / {r['formula_base']['zero_cost_reading_count']} | "
            f"{r['formula_no_name']['min_cost']} / {r['formula_no_name']['zero_cost_reading_count']} | "
            f"{not bool([c for c in checks if c['check'] == nome + '_SEM_NOME_UMA_INSERCAO' and not c['ok']])} | "
            f"{r['no_name_lexical_audit']['lexical_disguise_ok']} |"
        )
    linhas += [
        "",
        "Nos dois textos sem Nome, P e ¬P são itens separados e ambos recebem SIM. A fórmula mínima declarada para a contradição fica insatisfatível e o custo mínimo é um; portanto nenhuma leitura de custo zero foi reintroduzida nessa fórmula. A busca lexical separada não encontrou nomes-fonte nem números antigos reintroduzidos; a comparação bidirecional é conferida por texto e polaridade. Isso valida somente a construção sintética e não formaliza todos os fatos do texto.",
        "",
        "Nada aqui certifica produção, dificuldade equivalente, compreensão ou convergência.",
        "",
    ]
    (RAIZ / "RELATORIO_ISOMORFO.md").write_text("\n".join(linhas), encoding="utf-8")

    manifesto = {
        "schema": "k08-r4-isomorph-manifest-v1",
        "dictionary_sha256": sha256_bytes(dicionario_bruto),
        "files": {},
    }
    for path in sorted(RAIZ.iterdir(), key=lambda p: p.name):
        if path.is_file() and path.name != "manifesto.json":
            manifesto["files"][path.name] = sha256_bytes(path.read_bytes())
    escrever_json("manifesto.json", manifesto)
    print(json.dumps({"checks": len(checks), "failures": falhas, "memory_probe_label_changes": sum(x["label_changed"] for x in sondas)}, ensure_ascii=False))
    if falhas:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

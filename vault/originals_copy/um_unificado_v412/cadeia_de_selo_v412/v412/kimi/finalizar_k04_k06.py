from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def summary_count(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        if line.strip():
            count += 1
    return count


def contains_number(obj, target: float, tol: float = 1e-9) -> bool:
    if isinstance(obj, (int, float)):
        return abs(obj - target) <= tol
    if isinstance(obj, dict):
        return any(contains_number(v, target, tol) for v in obj.values())
    if isinstance(obj, list):
        return any(contains_number(v, target, tol) for v in obj)
    return False


required = {
    "K04": [
        "ENTREGA_K04.md", "HUBBLE_JA_EXAMINADO_K04.md",
        "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md", "COMBINACAO_K04.md",
        "RESSALVAS_UMA_A_UMA_K04.md", "ERRATA_NEUTRINO_V412_RASCUNHO_K04.md",
        "PERGUNTA_K04.md", "REGISTRO_MAPA_K04.json", "ERRATA_HUBBLE_K04.md",
        "ERRATA_HUBBLE_K04_R2.md", "ERRATA_M2_K04_R2.md", "ERRATA_M2_K04_R3.md",
        "ERRATA_COMBINACAO_K04.md", "K04/M2/medidas/resultados_planejamento.json",
        "K04/HUBBLE/MEDIDAS_PLANEJAMENTO_K04.json",
    ],
    "K06": [
        "ENTREGA_K06.md", "PROTOCOLO_EXPERIMENTAL_R3_K06.md",
        "MODELO_FORMAL_R3_K06.md", "PODER_CONJUNTO_K06.md",
        "DEGRAU_5_SIGMA_K06.md", "CONTAMINACAO_ISOMORFO_K06.md",
        "REGISTRO_UMPY_RASCUNHO_K06.md", "PERGUNTA_K06.md", "REGISTRO_MAPA_K06.json",
        "ERRATA_R3_1_K06.md", "ERRATA_R3_2_K06.md",
        "K06/extratores/RELATORIO_EXTRAORES.md", "K06/extratores/resultados.json",
        "K06/candidatas/sandbox/LeitorFinito.lean", "K06/candidatas/logs/LeitorFinito.txt",
        "K06/PODER/resultados_r32.json", "K06/PODER/validacao_r32.json",
        "K06/ENTRADA_PUBLICA/MEDIDA_ENTRADA_PUBLICA_K06.json",
    ],
}
for names in required.values():
    for name in names:
        assert (ROOT / name).is_file(), name

registrations = {
    key: json.loads((ROOT / f"REGISTRO_MAPA_{key}.json").read_text(encoding="utf-8"))
    for key in required
}
map_results = {}
for key, registration in registrations.items():
    assert registration["olhou_dados"] is False
    for item in registration["artefatos"]:
        assert Path(item).is_file(), item
    query = subprocess.run(
        [sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", registration["rota_id"]],
        cwd=r"C:\IALD", capture_output=True, text=True, check=True,
    )
    data = json.loads(query.stdout)
    assert all(item["rota_id"] != registration["rota_id"] for item in data["rotas"])
    map_results[key] = data["n"]

summary_counts = {key: summary_count(ROOT / f"ENTREGA_{key}.md") for key in required}
assert summary_counts == {"K04": 14, "K06": 15}, summary_counts
assert all(count <= 15 for count in summary_counts.values())
for key in required:
    text = (ROOT / f"ENTREGA_{key}.md").read_text(encoding="utf-8")
    assert "revisada internamente" in text
    assert "aprovada em revisão independente" not in text

r32 = json.loads((ROOT / "K06/PODER/resultados_r32.json").read_text(encoding="utf-8"))
for value in (0.992, 0.012, 0.599, 0.669, 0.057, 0.044, 0.040, 0.022, 0.311, 0.412):
    assert contains_number(r32, value), value
lean_log = (ROOT / "K06/candidatas/logs/LeitorFinito.txt").read_text(encoding="utf-8")
assert ("RC: 0" in lean_log or "RC=0" in lean_log) and "sorryAx" not in lean_log
json.loads((ROOT / "K04/M2/medidas/resultados_planejamento.json").read_text(encoding="utf-8"))
json.loads((ROOT / "K06/extratores/resultados.json").read_text(encoding="utf-8"))

article = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt")
assert sha(article) == "f9fa0d329166b33dd59d72e3f807b69c936a60e2f2a4d8a9e6be23009dd8d719"
order_paths = {
    "rodada2": (
        Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_parece_que_o_kimi_ja_respondeu_tudo_veja_o_que_falta_e_coloque_no_tunel_verbatim.txt"),
        90,
        "88799027aca347390ba8eb3c42fd6fce5b19a1f009ea6526370521f5760cf69c",
    ),
    "entrada_publica": (
        Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_excelente_concordo_com_tudo_depois_da_errata_do_meio_e_da_rodada_2_verbatim.txt"),
        28,
        "fa30a621d7d23516891cd98860b4b2a9753a6f813e80c2599492b5090f4d40a6",
    ),
}
order_pins = {}
for key, (path, size, digest) in order_paths.items():
    current = pin(path)
    assert current["bytes"] == size and current["sha256"] == digest, key
    order_pins[key] = current

pins = {key: {name: pin(ROOT / name) for name in names} for key, names in required.items()}
validation_paths = {}
for key in required:
    validation = {
        "contract": f"{key}_FINAL_DELIVERY_VALIDATION_V1",
        "created_at": datetime.now().astimezone().isoformat(),
        "review": "revisada internamente; integração e frentes conferidas por revisores distintos",
        "material_issues_remaining": False,
        "summary_nonempty_lines": summary_counts[key],
        "registration_written_to_map": False,
        "map_query_n": map_results[key],
        "observed_data_opened_again": False,
        "models_executed": False,
        "canonical_kernel_or_um_py_changed": False,
        "operator_order_pins": order_pins,
        "pins": pins[key],
    }
    if key == "K06":
        validation["r32_checks"] = {
            "powered_independent": 0.992,
            "powered_icc015_text010": 0.012,
            "powered_5sigma": [0.599, 0.669],
            "global_null": "0.057 OPEN/BORDERLINE",
            "tost": [0.044, 0.040],
            "nonspecific": [0.022, 0.311, 0.412],
            "production": "BLOQUEADA_PARA_PRODUCAO",
        }
    path = ROOT / f"VALIDACAO_{key}.json"
    path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    validation_paths[key] = path

texts = {
    "K04": "[DECLARADO] K04 concluída e revisada internamente. Não existe hoje teste cego de natureza com o poder requerido executável, nem primeira data publicada defensável. H0DN tem D=7,068/8,068 já lido; SNII D=3,256 e TDCOSMO 2,462–2,689 sem cegueira qualificada. No m₂, a Tabela 6 dá P(r≥5)=64,74% para incremento independente e 66,13% no brinquedo cumulativo; a 0,7% dá 12,88%/3,48% e a 0,5% 35,04%/31,47%. O desfecho provável é tensão do primário, não falsificação: com S ABSENT e a regra atual, um teste que não pode devolver negativo não é teste. Nenhum par publicado fecha FALSIFIED ou MATCHED; SK-Gd tem 3,605σ e 380,08 dias apenas como cenário, sem agenda/independência. A métrica congelada é m₂; mudança é emenda do operador. Brinquedo full-reactor: 5σ em 31/03/2028 e D90 em 19/09/2031, não cronograma. Stouffer JUNO+SO: horizonte 2034 condicional; ringdown D10≈27 meses retrospectivos, IR1 insuficiente, O5 condicional. As sete ressalvas ficaram apenas como partituras, sem execução. REV0/REV1 e erratas preservados; nenhum vetor observado, abertura ou teste empírico foi executado. Q1/Q2 estão em PERGUNTA_K04.md; REGISTRO_MAPA_K04.json é proposta não registrada. Gate imóvel.",
    "K06": "[DECLARADO] K06 R3.2 concluída e revisada internamente. V2-RET separa resumo de atrator em simulação: RETORNO=0 versus RETORNO=1, com A8⇒PRE, RETORNO⇒PRE e Q⇒RETORNO; produção permanece BLOQUEADA. POWERED=0,992 independente; 0,012 com ICC0,15/texto0,10; zero com ICC0,35; 5σ ideal 0,599/0,669. Nulo global 0,057 OPEN/BORDERLINE; TOST 0,044/0,040 pontualmente PASS, com IC cruzando 0,05; NONSPECIFIC_POWERED=0,022/0,311/0,412, abaixo de 90%. Custos base+triagem: 76.963,27/148.632,09/157.535,03 interações. Extratores 685/685 no contrato, mas prosa livre 0/120, teto e dependência continuam bloqueando. Lean finito RC=0 e axiomas permitidos. Entrada pública 1.164.350 B e 157.921 palavras, proxies 205.298–291.088 tokens, janelas desconhecidas; isomorfo apenas sintético. REV0/REV1 e erratas preservados; nenhum modelo ou resultado experimental foi executado. Operador decide modelos, ratificação da entrada/R3, degrau e execução após os portões. REGISTRO_MAPA_K06.json é proposta não registrada. Gate imóvel.",
}
for key, text in texts.items():
    main = pins[key][f"ENTREGA_{key}.md"]
    registration = pins[key][f"REGISTRO_MAPA_{key}.json"]
    content = (
        text
        + f"\n\nEntrega: {main['path']}\nSHA-256: {main['sha256']}\n"
        + f"Registro proposto: {registration['path']}\nSHA-256: {registration['sha256']}\n"
        + f"Validação: {validation_paths[key]}\nSHA-256: {sha(validation_paths[key])}\n"
    )
    path = ROOT / f"DEPOSITO_{key}.md"
    path.write_text(content, encoding="utf-8")

print(json.dumps({
    "status": "PASS",
    "summary_nonempty_lines": summary_counts,
    "map_query_n": map_results,
    "validation": {key: pin(path) for key, path in validation_paths.items()},
    "deposit_payloads": {key: pin(ROOT / f"DEPOSITO_{key}.md") for key in required},
}, ensure_ascii=False, indent=2))

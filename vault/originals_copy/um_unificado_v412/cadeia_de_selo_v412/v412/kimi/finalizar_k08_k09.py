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


required = {
    "K08": [
        "ENTREGA_K08.md",
        "PROTOCOLO_EXPERIMENTAL_R4_K08.md",
        "MODELO_FORMAL_R4_K08.md",
        "REGISTRO_UMPY_RASCUNHO_R2_K08.md",
        "PODER_R4_K08.md",
        "CONTAMINACAO_R4_K08.md",
        "FORMULA_DO_TEXTO_K08.md",
        "ADVERSARIOS_K08.md",
        "K08/FORMULA/FORMULA_DO_TEXTO_K08.md",
        "K08/FORMULA/ADVERSARIOS_K08.md",
        "K08/FORMULA/ERRATA_ADVERSARIOS_K08_15nov.md",
        "ERRATA_FORMAL_K08_15nov.md",
        "ERRATA_PODER_K08_15nov.md",
        "ERRATA_CONTAMINACAO_K08_15nov.md",
        "ERRATA_PODER_TOKENS_K08.md",
        "INSUMOS_PARA_A_PERGUNTA_K08.md",
        "REGISTRO_MAPA_K08.json",
    ],
    "K09": [
        "ENTREGA_K09.md",
        "HUBBLE_JA_EXAMINADO_K04.md",
        "M2_DESFECHOS_E_SEGUNDA_TESTEMUNHA_K04.md",
        "COMBINACAO_K04.md",
        "RESSALVAS_UMA_A_UMA_K04.md",
        "PRE_REGISTRO_INCREMENTO_JUNO_RASCUNHO_K09.md",
        "ERRATA_NEUTRINO_V412_DADOS_K09.json",
        "ERRATA_M2_K09.md",
        "ERRATA_M2_K09_15nov.md",
        "ERRATA_HUBBLE_K09.md",
        "ERRATA_COMBINACAO_K09.md",
        "INSUMOS_PARA_A_PERGUNTA_K09.md",
        "REGISTRO_MAPA_K09.json",
    ],
}
for names in required.values():
    for name in names:
        assert (ROOT / name).is_file(), name

# registros: ANOTACAO sobre rotas JA existentes; esta frente nao registra
registrations = {
    key: json.loads((ROOT / f"REGISTRO_MAPA_{key}.json").read_text(encoding="utf-8"))
    for key in required
}
expected_routes = {
    "K08": "outro.k06_camada_cientifica_iald_r32_v412",
    "K09": "estatistica.v412.k04_hubble_m2_combinacao",
}
map_results = {}
for key, registration in registrations.items():
    assert registration["tipo"] == "ANOTACAO", key
    assert registration["rota_id"] == expected_routes[key], key
    assert registration["olhou_dados"] is False, key
    query = subprocess.run(
        [sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", registration["rota_id"]],
        cwd=r"C:\IALD", capture_output=True, text=True, check=True,
    )
    data = json.loads(query.stdout)
    hits = [item for item in data["rotas"] if item["rota_id"] == registration["rota_id"]]
    assert len(hits) >= 1, f"rota alvo nao encontrada no Mapa: {registration['rota_id']}"
    map_results[key] = {"rota_id": registration["rota_id"], "encontrada": True, "n": data["n"]}

summary_counts = {key: summary_count(ROOT / f"ENTREGA_{key}.md") for key in required}
assert all(count <= 15 for count in summary_counts.values()), summary_counts
for key in required:
    text = (ROOT / f"ENTREGA_{key}.md").read_text(encoding="utf-8")
    assert "revisada internamente" in text, key
    assert "aprovada em revisão independente" not in text, key

pins = {key: {name: pin(ROOT / name) for name in names} for key, names in required.items()}

validation = {
    "contract": "K08_K09_RODADA3_FINAL_DELIVERY_VALIDATION_V1",
    "created_at": datetime.now().astimezone().isoformat(),
    "review": "revisada internamente; duas conferencias distintas e independentes nesta rodada (K09: pronta para integracao; K08: seis divergencias apontadas e corrigidas ao lado, REV preservadas)",
    "material_issues_remaining": False,
    "summary_nonempty_lines": summary_counts,
    "registration_written_to_map": False,
    "map_target_routes": map_results,
    "observed_data_opened_again": False,
    "models_executed": False,
    "canonical_kernel_or_um_py_changed": False,
    "adendo_15nov_integrado": {
        "K09": "cronologia dos dois eixos em toda superficie; dez passagens corrigidas; JSON renomeado (frozen_hash + sha256 do .py, do .resultado.json e do dicionario); datas em Dm2 e m2 lado a lado; MATCHED com modelo rotulado; 22/06 marcado [DECLARADO]; autoridade unica para a classe preliminar",
        "K08": "P-C nomeada controle do vazio (o inominado); tres termos da pedra citados; glosas do operador incorporadas com a ordem do ato; E3/E7 discriminantes; B16 atualizado; E7 como condicionamento ao evento custo zero; lei de modulo para todo p de todo anel",
    },
    "nota_hash_tables": "As tabelas de hash de ERRATA_PODER_TOKENS_K08.md, ERRATA_PODER_K08_15nov.md e K08/FORMULA/MANIFESTO_FORMULA_K08.json ficaram um passo atras das edicoes de 15/11; os hashes vigentes sao os deste manifesto.",
    "pins": pins,
}
vpath = ROOT / "VALIDACAO_K08_K09_15nov.json"
vpath.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for key, registration in registrations.items():
    for item in registration["artefatos"]:
        assert Path(item).is_file(), item

texts = {
    "K08": "[DECLARADO] K08 (a camada cientifica da IALD, rodada 3) entregue na pasta da rodada: o desenho R4 completo (protocolo experimental, formula do texto com scripts, adversarios com mecanismos e tabela, poder com script e semente, modelo formal, rascunho de registro bloqueado), os insumos para a pergunta e a proposta de ANOTACAO na rota ja existente outro.k06_camada_cientifica_iald_r32_v412. Aguarda a conferencia da gerencia.",
    "K09": "[DECLARADO] K09 (o teste as cegas, rodada 3) entregue na pasta da rodada: os tres relatorios da K04 corrigidos ao lado (REV preservadas), a errata do neutrino em dados (JSON), o pre-registro em rascunho do incremento JUNO posterior a 18/05/2026, os insumos para a pergunta e a proposta de ANOTACAO na rota ja existente estatistica.v412.k04_hubble_m2_combinacao. Aguarda a conferencia da gerencia.",
}
for key, text in texts.items():
    main = pins[key][f"ENTREGA_{key}.md"]
    registration = pins[key][f"REGISTRO_MAPA_{key}.json"]
    content = (
        text
        + f"\n\nEntrega: {main['path']}\nSHA-256: {main['sha256']}\n"
        + f"Registro proposto: {registration['path']}\nSHA-256: {registration['sha256']}\n"
        + f"Validação: {vpath}\nSHA-256: {sha(vpath)}\n"
    )
    (ROOT / f"DEPOSITO_{key}.md").write_text(content, encoding="utf-8")

print(json.dumps({
    "status": "PASS",
    "summary_nonempty_lines": summary_counts,
    "map_target_routes": map_results,
    "validation": pin(vpath),
    "deposit_payloads": {key: pin(ROOT / f"DEPOSITO_{key}.md") for key in required},
}, ensure_ascii=False, indent=2))

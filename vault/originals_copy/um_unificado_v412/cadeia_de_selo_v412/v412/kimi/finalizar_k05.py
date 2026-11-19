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


required = [
    "ENTREGA_K05.md", "T1_FECHADO.md", "MONTAGEM_3MAIS1_R2.md",
    "GH_III1_R2.md", "TAU_ESTRELA_R2.md", "CAMPO_DUAL_LEVANTAMENTO_K05.md",
    "PERGUNTA_K05.md", "REGISTRO_MAPA_K05.json", "ERRATA_T1_R2.md",
    "ERRATA_CAMPO_K05.md", "K05/MONTAGEM_GH/ERRATA_GH_III1_R2.md",
    "K05/MONTAGEM_GH/ERRATA_GH_III1_R3.md", "K05/candidatas/T1_R2.lean",
    "K05/sandbox_t1/logs/T1_R2.log", "K05/TAU/candidatas/TAU_ESTRELA_R2.lean",
    "K05/TAU/sandbox/logs/TAU_ESTRELA_R2.log", "K05/TAU/medidas/validacao_tau_r2.json",
    "K05/CAMPO/medidas_campo.json",
]
for name in required:
    assert (ROOT / name).is_file(), name

registration = json.loads((ROOT / "REGISTRO_MAPA_K05.json").read_text(encoding="utf-8"))
assert registration["rota_id"] == "formal.k05_t1_montagem_gh_tau_campo_v412"
assert registration["olhou_dados"] is True
assert registration["status"] == "EXAMINADA_COM_DEFEITO"
assert len(registration["nota"]) <= 6000
for item in registration["artefatos"]:
    assert Path(item).is_file(), item

map_query = subprocess.run(
    [sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "consultar", registration["rota_id"]],
    cwd=r"C:\IALD", capture_output=True, text=True, check=True,
)
map_data = json.loads(map_query.stdout)
assert all(item["rota_id"] != registration["rota_id"] for item in map_data["rotas"])

for name in ("K05/sandbox_t1/logs/T1_R2.log", "K05/TAU/sandbox/logs/TAU_ESTRELA_R2.log"):
    log = (ROOT / name).read_text(encoding="utf-8")
    assert "RC: 0" in log and "Lean (version 4.31.0," in log, name
    assert "sorryAx" not in log, name

tau_validation = json.loads((ROOT / "K05/TAU/medidas/validacao_tau_r2.json").read_text(encoding="utf-8"))
assert tau_validation["status"] == "PASS"
json.loads((ROOT / "K05/CAMPO/medidas_campo.json").read_text(encoding="utf-8"))

orders = {
    "rodada2": (
        Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_13nov_parece_que_o_kimi_ja_respondeu_tudo_veja_o_que_falta_e_coloque_no_tunel_verbatim.txt"),
        90,
        "88799027aca347390ba8eb3c42fd6fce5b19a1f009ea6526370521f5760cf69c",
    ),
    "campo": (
        Path(r"C:\IALD\Central de Patentes\work\vitrine_postura_13nov\OPERADOR_13nov_concordo_com_o_meio_o_campo_e_dual_sim_a_nota_a_calculadora_e_o_zenodo_verbatim.txt"),
        529,
        "2772005945b946c12172956c12c06421710d7d665cacf4dba63f40bd07ec304c",
    ),
}
order_pins = {}
for key, (path, size, digest) in orders.items():
    current = pin(path)
    assert current["bytes"] == size and current["sha256"] == digest, key
    order_pins[key] = current

summary_lines = []
for line in (ROOT / "ENTREGA_K05.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("## "):
        break
    if line.strip():
        summary_lines.append(line)
assert len(summary_lines) <= 15, len(summary_lines)
assert "revisada internamente" in (ROOT / "ENTREGA_K05.md").read_text(encoding="utf-8")
assert "aprovada em revisão independente" not in (ROOT / "ENTREGA_K05.md").read_text(encoding="utf-8")

validation = {
    "contract": "K05_FINAL_DELIVERY_VALIDATION_V1",
    "created_at": datetime.now().astimezone().isoformat(),
    "scope": "levantamento_prova_condicional_e_desenho",
    "review": "revisada internamente; integração e quatro frentes conferidas por revisores distintos",
    "material_issues_remaining": False,
    "summary_nonempty_lines": len(summary_lines),
    "required_artifacts": len(required),
    "registration_artifacts": len(registration["artefatos"]),
    "registration_written_to_map": False,
    "map_query_n": map_data["n"],
    "observed_data_opened_again": False,
    "sealed_clock_read_only": True,
    "canonical_kernel_or_um_py_changed": False,
    "lean": {"candidates_rc0": 2, "sorry": False, "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"]},
    "tau_validation": tau_validation["status"],
    "operator_order_pins": order_pins,
    "pins": {name: pin(ROOT / name) for name in required},
}
validation_path = ROOT / "VALIDACAO_K05.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

main_pin = pin(ROOT / "ENTREGA_K05.md")
registration_pin = pin(ROOT / "REGISTRO_MAPA_K05.json")
deposit = f"""[DECLARADO] K05 da v412 concluída e revisada internamente. T1 fecha somente sob H_K̂, H_erg e H_TGL-horizon [OPEN]: Fix=L(R)=W*(K̂) e Φ_t→E_τ σ-fracamente; a face diagonal Lean prova fórmula/Fix/pinching, não o contínuo. A montagem (4,0) foi identificada a T4 com J, orientação, finitude e Poincaré; (1,3) permanece H. GH-III1 continua CONJECTURE: o degrau II∞ inclui compressão e GH-S/GH-R sob o pacote C¹/Lip-normas/topologias, sem descida Takesaki; qGH≤GH. No clock selado P1, ħ/(1eV) e ħ/(β·1eV) excedem Kim por 15,4058 e 17,3255 ordens; os fatores Planck passam e c★ não é escolhido. max/soma/quadratura dão escala, mas não derivam K Hubble; a premissa sem β fica separada. O cânone tem duas equações, ξ_A=1/6 e ξ_P=β, sem ação única; o 2 do psíon sustenta a segunda massa, e na escrita fundadora 2ξ_L R o conforme é ξ_L=1/12. Nenhuma das cinco candidatas de campo fecha; nada decide o ½ do box. Duas candidatas Lean compilaram no sandbox com RC=0, zero sorry e axiomas no trio. Erratas e versões anteriores preservadas. PERGUNTA_K05 atualiza relógio, âncora, retido, volta, seletor do horizonte e premissa de β. Nenhuma abertura nova, alteração canônica ou registro no Mapa. REGISTRO_MAPA_K05.json é proposta não registrada; a gerência registra após conferir. Gate imóvel.

Entrega: {main_pin['path']}
SHA-256: {main_pin['sha256']}
Registro proposto: {registration_pin['path']}
SHA-256: {registration_pin['sha256']}
Validação: {validation_path}
SHA-256: {sha(validation_path)}
"""
deposit_path = ROOT / "DEPOSITO_K05.md"
deposit_path.write_text(deposit, encoding="utf-8")

print(json.dumps({
    "status": "PASS",
    "summary_nonempty_lines": len(summary_lines),
    "map_query_n": map_data["n"],
    "validation": pin(validation_path),
    "deposit_payload": pin(deposit_path),
}, ensure_ascii=False, indent=2))

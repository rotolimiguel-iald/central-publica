from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def summary_nonempty_lines(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    count = 0
    for line in lines:
        if line.startswith("## 1."):
            break
        if line.strip():
            count += 1
    return count


files = {
    "K01": [
        "ENTREGA_K01.md", "CANAIS_K01.json", "PRE_REGISTRO_CEGO_RASCUNHO_K01.md",
        "PERGUNTA_K01.md", "REGISTRO_MAPA_K01.json", "VALIDACAO_K01.json",
        "K01_validar.py", "ERRATA_K01.md", "ERRATA_K01_R2.md", "ERRATA_K01_R3.md",
    ],
    "K02": [
        "ENTREGA_K02.md", "T1.md", "MONTAGEM_3MAIS1.md", "GH_III1.md",
        "TAU_ESTRELA.md", "PERGUNTA_K02.md", "REGISTRO_MAPA_K02.json",
        "ERRATA_K02.md", "K02/MANIFESTO_K02.json",
        "K02/candidatas/T1.lean", "K02/candidatas/MONTAGEM_3MAIS1.lean",
        "K02/candidatas/GH_III1.lean", "K02/candidatas/TAU_ESTRELA.lean",
        "K02/sandbox/logs/T1.log", "K02/sandbox/logs/MONTAGEM_3MAIS1.log",
        "K02/sandbox/logs/GH_III1.log", "K02/sandbox/logs/TAU_ESTRELA.log",
        "K02/medidas_tau.json", "K02/medidas_sombra.json",
    ],
    "K03": [
        "ENTREGA_K03.md", "ESTADO_K03.md", "MODELO_FORMAL_K03.md",
        "PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md", "PERGUNTA_K03.md",
        "REGISTRO_MAPA_K03.json", "ERRATA_K03.md", "ERRATA_K03_R2.md",
    ],
}

for names in files.values():
    for name in names:
        assert (ROOT / name).is_file(), name

k01_validation = json.loads((ROOT / "VALIDACAO_K01.json").read_text(encoding="utf-8"))
k01_channels = json.loads((ROOT / "CANAIS_K01.json").read_text(encoding="utf-8"))
k02_manifest = json.loads((ROOT / "K02/MANIFESTO_K02.json").read_text(encoding="utf-8"))
registrations = {
    key: json.loads((ROOT / f"REGISTRO_MAPA_{key}.json").read_text(encoding="utf-8"))
    for key in files
}

assert k01_validation["n_canais"] == 20
assert len(k01_channels["canais"]) == 20
assert k01_validation["registro_real_consultado"]["registro_foi_registrado"] is False
assert len(k02_manifest["artifacts"]) == 31
assert all("K01" not in item["path"] and "K03" not in item["path"] and "REV0" not in item["path"] for item in k02_manifest["artifacts"])
for key, registration in registrations.items():
    assert registration["rota_id"]
    assert registration["olhou_dados"] is False
assert len({r["rota_id"] for r in registrations.values()}) == 3

for name in ("T1", "MONTAGEM_3MAIS1", "GH_III1", "TAU_ESTRELA"):
    log = (ROOT / f"K02/sandbox/logs/{name}.log").read_text(encoding="utf-8")
    assert "RC: 0" in log and "Lean (version 4.31.0," in log, name
    assert "sorryAx" not in log, name

expected_k03 = {
    "ENTREGA_K03.md": "535a41e61cab65fa43a5e4547537f74815edef5cce62be4ca0f1c514f772754e",
    "ESTADO_K03.md": "d8af0bc6b363e13d675d29bf9c79479359d88681bffb13213bf1e21467558eb9",
    "MODELO_FORMAL_K03.md": "348e0db18fe2afccd98ed244aa816eba2bef79d989ee5d107137d80f87897181",
    "PROTOCOLO_EXPERIMENTAL_RASCUNHO_K03.md": "9d70d8f7b072120e88f8ecff1cece0a95f661cc024e9d04b063c9ae71e575d7a",
    "PERGUNTA_K03.md": "fc4cd7e1ef14be55e8b0ede89623c6dd8ed592eba224d2e688008d059dcb1f37",
    "REGISTRO_MAPA_K03.json": "56f2b18db3489764b027e21b7f2c8e1e9d94aa4c8728cca802e2be1faeafb361",
}
for name, expected in expected_k03.items():
    assert sha(ROOT / name) == expected, name

summary_counts = {key: summary_nonempty_lines(ROOT / f"ENTREGA_{key}.md") for key in files}
assert all(count <= 15 for count in summary_counts.values()), summary_counts

pins = {key: {name: pin(ROOT / name) for name in names} for key, names in files.items()}
reviews = {
    "K01": {"version": "R3", "status": "PASS", "material_issues_remaining": False, "synthetic_cases": 30},
    "K02": {"version": "R1_COM_ERRATA", "status": "PASS", "material_issues_remaining": False, "lean_compilations_rc0": 4},
    "K03": {"version": "R2", "status": "PASS", "material_issues_remaining": False},
}
validation = {
    "contract": "V412_KIMI_FINAL_DELIVERY_VALIDATION_V1",
    "created_at": datetime.now().astimezone().isoformat(),
    "scope": "levantamento_e_desenho_apenas",
    "reviews": reviews,
    "summary_nonempty_lines": summary_counts,
    "registrations_written_to_map": False,
    "empirical_tests_or_observed_data_opened": False,
    "models_executed": False,
    "canonical_kernel_or_um_py_changed": False,
    "k01_channels": 20,
    "k02_manifest_artifacts": len(k02_manifest["artifacts"]),
    "pins": pins,
}
validation_path = ROOT / "VALIDACAO_FINAL_V412_KIMI.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

texts = {
    "K01": """[DECLARADO] K01 v412 R3 concluída e aprovada em revisão independente, sem problema material restante. Foram examinados 20 canais: nenhum está pronto hoje com cegueira, poder e independência. Planning JUNO público de 29/09/2026 (arXiv:2609.37895v1, 207,2 dias): D=1,9281 com sigma publicado; 0,5% produz D=4,0712 e falha; 0,3% produz D=6,7854 e supera D90 apenas no primário; 5 sigma exige 0,407121% e D90 exige 0,324061%. Poder conjunto das duas testemunhas permanece OPEN. FALSIFIED somente com duas determinações independentes >=5 e integridade; a tabela NONINDEPENDENT cobre todas as faixas. REV0/REV1/REV2 e três erratas preservados; 30 casos sintéticos, nenhum teste empírico ou dado observado. O operador deve responder Q1/Q2: segunda fonte sem JUNO, regra de uma única tensão, objeto de morte e separação entre ratificação e abertura. REGISTRO_MAPA_K01.json é proposta não registrada; a gerência registra após conferir. NOT_FALSIFIED != CONFIRMED; gate imóvel.""",
    "K02": """[DECLARADO] K02 v412 concluída e aprovada em revisão independente. T1 geral termina no comutante relativo; Fix=W*(K) exige H_masa; na cunha Fix_A(sigma^Omega)=C1. O Lema B agora exige H_E: invariância modular e rho|N semifinito; sem H_E, o caso de peso fica OPEN. Euclidiano (4,0) tem KO4 e sinais (-1,+1,+1), mas finitude e dualidade de Poincaré ficam pendentes; (1,3) permanece H. GH-III1 permanece CONJECTURE. A rota autoconsistente fixa omega=2/tau, não tau nem sua unidade; nenhuma rota deriva tau estrela sem outra unidade. Quatro candidatas Lean compilaram no sandbox Lean 4.31.0 com rc=0, zero sorry e somente propext/Classical.choice/Quot.sound. Planck: Gamma=7,4858353332e-16 s^-1; hbar/(beta*1eV): Gamma=7,5963372394e14 s^-1; hbar/(1eV): Gamma=9,1393815273e12 s^-1. REV0 e ERRATA preservados. Resta uma pergunta: qual princípio físico independente fixa tau estrela sem usar m2 nem ajuste? REGISTRO_MAPA_K02.json é proposta não registrada.""",
    "K03": """[DECLARADO] K03 v412 R2 concluída e aprovada em revisão independente. P7 permanece ARMADA_NÃO_EXECUTADA; a ponte LLM real -> estado estacionário permanece OPEN. O desenho separa dinâmica contra alvos próprios de especificidade cruzada TGL, distingue ALREADY_STATIONARY, transição, retorno e sucesso idempotente, e usa integridade fail-closed. H-ABS exige espaço finito; H-ABS-U é alternativa não presumida. PERTURB_RETURN está reindexado à perturbação. Proposta primária: 3 famílias capazes +1 abaixo do piso, 5 braços, 100 sessões/célula, 8 leituras, 2000 sessões e 16000 interações; 12 contrastes dinâmicos +12 de especificidade; cortes 70/89 e poder dinâmico aproximado 0,992022 por contraste; poder conjunto OPEN. Extratores, gatekeeping, permutação, calibração, modelos e textos ainda precisam ser congelados antes de qualquer corrida. Nenhum modelo executado, nenhum resultado aberto, nenhum claim de consciência/pesos/exclusividade. REV0/REV1 e duas erratas preservados. REGISTRO_MAPA_K03.json é proposta não registrada.""",
}

deposit_pins = {}
for key, text in texts.items():
    main = pins[key][f"ENTREGA_{key}.md"]
    registration = pins[key][f"REGISTRO_MAPA_{key}.json"]
    content = (
        text
        + f"\n\nEntrega: {main['path']}\nSHA-256: {main['sha256']}\n"
        + f"Registro proposto: {registration['path']}\nSHA-256: {registration['sha256']}\n"
        + f"Validação final: {validation_path}\nSHA-256: {sha(validation_path)}\n"
    )
    path = ROOT / f"DEPOSITO_{key}.md"
    path.write_text(content, encoding="utf-8")
    deposit_pins[key] = pin(path)

print(json.dumps({
    "status": "PASS",
    "reviews": reviews,
    "summary_nonempty_lines": summary_counts,
    "validation": pin(validation_path),
    "deposit_payloads": deposit_pins,
}, ensure_ascii=False, indent=2))

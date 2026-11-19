"""Confere a integridade do dossiê K07 sem executar os artefatos auditados."""
from hashlib import sha256
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
TUNNEL = HERE.parent.parent
RELEASE = TUNNEL.parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def sources():
    files = set(TUNNEL.glob("*.md"))
    files.update(RELEASE.glob("DESENHO_v412_R1.md"))
    files.update(RELEASE.glob("PERGUNTA_TAU_ESTRELA_*.md"))
    files.update((RELEASE / "revisao").glob("REVISAO_K05_*.md"))
    files.update((RELEASE / "revisao").glob("REVISAO_CANDIDATA_*.md"))
    files.update((RELEASE / "revisao" / "LEVANTAMENTO_FRENTE_B_15nov").glob("*.md"))
    for name in ["ErgodicidadeDeMautner.lean", "MontagemDasGamas.lean"]:
        files.add(RELEASE / "candidatas_c1" / name)
    for directory in TUNNEL.glob("K[0-9][0-9]"):
        if directory.name != "K07":
            for path in directory.rglob("*"):
                if path.suffix in {".lean", ".md"} and path.is_file():
                    files.add(path)
    return {
        path.relative_to(RELEASE).as_posix(): digest(path)
        for path in sorted(files)
        if "CODEX" not in path.name
    }


def verify():
    inventory = json.loads((HERE / "FONTES_K07_R3.json").read_text("utf-8"))
    current = sources()
    for name, record in json.loads((HERE / "CONCILIACAO_R3.json").read_text("utf-8")).items():
        if inventory.get(name) != record["antes"]:
            raise ValueError(f"Origem da conciliação divergente: {name}")
        inventory[name] = record["depois"]
    errors = [name for name in sorted(current.keys() | inventory.keys())
              if current.get(name) != inventory.get(name)]
    receipt = (TUNNEL / "ENTREGA_K07_CODEX.md").read_text("utf-8")
    rows = re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", receipt, re.M)
    if not rows:
        raise ValueError("Tabela de artefatos ausente.")
    for name, pin in rows:
        path = (TUNNEL / name).resolve()
        if not path.is_relative_to(TUNNEL) or not path.is_file() or digest(path) != pin:
            errors.append(name)
    print(json.dumps({"fontes_documentais": len(inventory), "artefatos": len(rows),
                      "divergencias": errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    if sys.argv[1:] == ["--listar-fontes"]:
        print(json.dumps(sources(), ensure_ascii=False, indent=2))
    elif not sys.argv[1:]:
        sys.exit(verify())
    else:
        raise SystemExit("Uso: conferir_entrega.py [--listar-fontes]")

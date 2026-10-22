# -*- coding: utf-8 -*-
"""Central paths and constants. Filesystem is the source of truth (DATA_MODEL §0)."""
from pathlib import Path

# backend/app/config.py -> Central root is two parents up from this file's dir
CENTRAL = Path(__file__).resolve().parents[2]

ORIGINALS = CENTRAL / "Patentes"                       # READ-ONLY originals
MEMORY = CENTRAL / "memory"
CLASSES_DIR = MEMORY / "classes"
PATENTS_MD_DIR = MEMORY / "patents"
MASTER_INDEX = MEMORY / "PATENT_MASTER_INDEX.yaml"
TGL_CORE = MEMORY / "TGL_CORE_MEMORY.md"
TGL_ATLAS = MEMORY / "TGL_ATLAS.md"            # o Atlas — a memória holográfica
PATENTS_DIR = CENTRAL / "patents"                      # docket.yaml, notes/, runner/, seals/
SOURCE_INV = CENTRAL / "source_inventory"
ORIGINAL_HASHES = SOURCE_INV / "original_hashes.json"
DISCOVERED = SOURCE_INV / "discovered_files.json"
EXTRACTION = SOURCE_INV / "extraction_report.json"
NORMALIZED = CENTRAL / "vault" / "normalized_docs"
PENDENCIAS = CENTRAL / "PENDENCIAS.md"
COMPILED_PROMPTS = CENTRAL / "compiled_prompts"
ARCHITECTURE = CENTRAL / "architecture"
LOGS = CENTRAL / "logs"

DATA_DIR = CENTRAL / "backend" / "data"
DB_PATH = DATA_DIR / "central.db"

SCHEMA_VERSION = 2  # v2: patent.display_name (nome do dispositivo)
HOST = "127.0.0.1"
PORT = 8765

# β_TGL is NEVER a literal in compute code; this is the audited runtime value only.
BETA_TGL_RUNTIME_CHECK = 0.012031300400803142

AVISO_LEGAL = ("Controle interno. Não substitui agente de propriedade industrial; "
               "prazos oficiais conferidos com INPI/WIPO.")

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(exist_ok=True)
COMPILED_PROMPTS.mkdir(exist_ok=True)

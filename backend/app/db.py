# -*- coding: utf-8 -*-
"""SQLite schema and connection. The DB is a reconstructible INDEX, never the owner
of data (DATA_MODEL §0). Schema mirrors DATA_MODEL §4."""
import sqlite3
from pathlib import Path

from .config import DB_PATH, SCHEMA_VERSION

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE patent_class (
  id TEXT PRIMARY KEY, ordinal INTEGER NOT NULL, name TEXT NOT NULL, slug TEXT,
  description TEXT, markers TEXT DEFAULT '[]', lock_note TEXT,
  memory_md_path TEXT NOT NULL, source_sha256 TEXT NOT NULL, indexed_at TEXT NOT NULL
);

CREATE TABLE patent (
  id TEXT PRIMARY KEY, slug TEXT NOT NULL, display_name TEXT NOT NULL, dir_name TEXT NOT NULL,
  class_id TEXT NOT NULL REFERENCES patent_class(id), role TEXT,
  title_54 TEXT NOT NULL, nature TEXT, peticao TEXT,
  filing_date TEXT, priority_date TEXT, jurisdiction TEXT DEFAULT 'BR (INPI)',
  epct_status TEXT NOT NULL, epct_number TEXT, epct_date TEXT,
  abstract TEXT, markers TEXT DEFAULT '[]', prototype_status TEXT DEFAULT 'VER_MEMORIA',
  pasta_original TEXT, memory_md_path TEXT, docket_path TEXT,
  doc_count INTEGER DEFAULT 0, claims_total INTEGER, claims_independent INTEGER,
  figures_count INTEGER, conflict_flag INTEGER DEFAULT 0,
  source_sha256 TEXT NOT NULL, memory_sha256 TEXT, indexed_at TEXT NOT NULL
);
CREATE INDEX ix_patent_class ON patent(class_id);

CREATE TABLE document (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patent_id TEXT REFERENCES patent(id),
  rel_path TEXT NOT NULL UNIQUE, sha256 TEXT NOT NULL, size_bytes INTEGER, mtime TEXT,
  ext TEXT, doc_role TEXT, pages INTEGER, chars INTEGER, extract_ok INTEGER,
  extract_error TEXT, is_original INTEGER NOT NULL DEFAULT 1, normalized_path TEXT,
  indexed_at TEXT NOT NULL
);
CREATE INDEX ix_document_patent ON document(patent_id);

CREATE TABLE docket_entry (
  patent_id TEXT PRIMARY KEY REFERENCES patent(id), status TEXT, alert_level TEXT,
  epct_status TEXT, epct_number TEXT, epct_date TEXT,
  janela_paris_12m TEXT, janela_paris_alvo TEXT, fase_nacional_30m TEXT,
  gru_arquivo TEXT, gru_servico TEXT, gru_valor TEXT, gru_vencimento TEXT,
  pix_arquivo TEXT, pix_data TEXT, pix_valor TEXT, annuities_note TEXT,
  office_actions TEXT DEFAULT '[]', reminders TEXT DEFAULT '[]', aviso TEXT,
  source_sha256 TEXT NOT NULL, indexed_at TEXT NOT NULL
);

CREATE TABLE deadline (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patent_id TEXT NOT NULL REFERENCES patent(id),
  kind TEXT NOT NULL, label TEXT NOT NULL, due_date TEXT, status TEXT NOT NULL,
  basis TEXT, source_field TEXT, legal_note TEXT, indexed_at TEXT NOT NULL
);
CREATE INDEX ix_deadline_patent ON deadline(patent_id);
CREATE INDEX ix_deadline_due ON deadline(due_date);

CREATE TABLE note (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patent_id TEXT NOT NULL REFERENCES patent(id),
  tipo TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 0, done INTEGER NOT NULL DEFAULT 0,
  text TEXT NOT NULL, markers TEXT DEFAULT '[]', source_file TEXT NOT NULL,
  source_section TEXT, line_ref INTEGER, order_index INTEGER,
  content_hash TEXT NOT NULL, indexed_at TEXT NOT NULL
);
CREATE INDEX ix_note_patent ON note(patent_id);
CREATE INDEX ix_note_active ON note(active);

CREATE TABLE runner_run (
  id TEXT PRIMARY KEY, patent_id TEXT NOT NULL REFERENCES patent(id),
  runner_path TEXT, runner_sha256 TEXT, started_at TEXT, finished_at TEXT,
  duration_s REAL, status TEXT NOT NULL, results_path TEXT, results_sha256 TEXT,
  seal_path TEXT, seal_sha256 TEXT, beta_runtime REAL,
  physical_verdict_allowed INTEGER DEFAULT 0, max_verdict TEXT, tests_passed INTEGER,
  result_hash TEXT, invariants_hash TEXT, module_hashes TEXT DEFAULT '{}',
  markers TEXT DEFAULT '[]', indexed_at TEXT NOT NULL
);
CREATE INDEX ix_run_patent ON runner_run(patent_id);

CREATE TABLE render (
  id INTEGER PRIMARY KEY AUTOINCREMENT, patent_id TEXT NOT NULL REFERENCES patent(id),
  kind TEXT NOT NULL, layer TEXT, title TEXT, source_document_id INTEGER,
  asset_path TEXT NOT NULL, dzi_path TEXT, component_spec_path TEXT, sha256 TEXT,
  marker TEXT DEFAULT 'ilustração de engenharia; não é prova física', indexed_at TEXT NOT NULL
);
CREATE INDEX ix_render_patent ON render(patent_id);

CREATE TABLE compiled_prompt (
  id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL UNIQUE, path TEXT NOT NULL,
  created_at TEXT NOT NULL, sha256 TEXT NOT NULL, active_only INTEGER DEFAULT 1,
  scope TEXT DEFAULT '{}', byte_size INTEGER, indexed_at TEXT NOT NULL
);

CREATE TABLE pendencia (
  id TEXT PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL, body TEXT,
  markers TEXT DEFAULT '[]', resolved_date TEXT, source_file TEXT NOT NULL,
  line_ref INTEGER, source_sha256 TEXT NOT NULL, indexed_at TEXT NOT NULL
);
CREATE TABLE pendencia_patent (
  pendencia_id TEXT REFERENCES pendencia(id), patent_id TEXT REFERENCES patent(id),
  PRIMARY KEY (pendencia_id, patent_id)
);

CREATE TABLE index_meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE reindex_run (
  id INTEGER PRIMARY KEY AUTOINCREMENT, started_utc TEXT, finished_utc TEXT, mode TEXT,
  added INTEGER, updated INTEGER, unchanged INTEGER, orphaned INTEGER,
  integrity_status TEXT, report_path TEXT
);
"""

TABLES = [
    "pendencia_patent", "pendencia", "compiled_prompt", "render", "runner_run",
    "note", "deadline", "docket_entry", "document", "patent", "patent_class",
    "index_meta", "reindex_run",
]


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def db_version(conn: sqlite3.Connection) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
    conn.commit()


def drop_all(conn: sqlite3.Connection) -> None:
    for t in TABLES:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()


def ensure_schema(conn: sqlite3.Connection) -> bool:
    """Return True if a fresh (re)build is needed (schema mismatch or empty)."""
    has_tables = conn.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='patent'"
    ).fetchone()[0]
    if not has_tables or db_version(conn) != SCHEMA_VERSION:
        drop_all(conn)
        create_schema(conn)
        return True
    return False

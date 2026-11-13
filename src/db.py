"""
Database layer for the Chemical Compound Database.

SQLite file lives at data/compounds.db. Schema covers the information
a chemist actually needs: identity, formula, mass, physical properties,
safety data, and CAS number for cross-referencing.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "compounds.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS compounds (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    formula         TEXT NOT NULL,
    cas_number      TEXT UNIQUE,
    molar_mass      REAL,               -- g/mol
    density         REAL,               -- g/cm³ (or g/mL)
    melting_point   REAL,               -- °C
    boiling_point   REAL,               -- °C
    state_stp       TEXT,               -- solid / liquid / gas
    iupac_name      TEXT,
    synonyms        TEXT,               -- comma-separated
    hazard_class    TEXT,               -- GHS signal word / class
    description     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_name    ON compounds(name);
CREATE INDEX IF NOT EXISTS idx_formula ON compounds(formula);
CREATE INDEX IF NOT EXISTS idx_cas     ON compounds(cas_number);
"""


def connect(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    """
    Open a connection to the SQLite database, creating the schema if
    it doesn't exist. Returns a connection with row access by name.
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row          # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
"""
Reusable query functions. All return lists of dicts (JSON-friendly).
Used by both the Streamlit app and the JSON exporter.
"""
from __future__ import annotations

from .db import connect


def _rows_to_dicts(rows):
    return [dict(r) for r in rows]


def search(query: str = "", limit: int = 100) -> list[dict]:
    """
    Search by name, formula, CAS number, synonyms, or description.
    Empty query returns everything (up to `limit`).
    """
    conn = connect()
    try:
        if not query.strip():
            rows = conn.execute(
                "SELECT * FROM compounds ORDER BY name LIMIT ?", (limit,)
            ).fetchall()
        else:
            like = f"%{query.strip()}%"
            rows = conn.execute(
                """
                SELECT * FROM compounds
                WHERE name LIKE ? OR formula LIKE ? OR cas_number LIKE ?
                   OR synonyms LIKE ? OR description LIKE ?
                ORDER BY name LIMIT ?
                """,
                (like, like, like, like, like, limit),
            ).fetchall()
        return _rows_to_dicts(rows)
    finally:
        conn.close()


def get_by_name(name: str) -> dict | None:
    conn = connect()
    try:
        row = conn.execute(
            "SELECT * FROM compounds WHERE name = ? COLLATE NOCASE", (name,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_by_cas(cas: str) -> dict | None:
    conn = connect()
    try:
        row = conn.execute(
            "SELECT * FROM compounds WHERE cas_number = ?", (cas,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def by_state(state: str) -> list[dict]:
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT * FROM compounds WHERE state_stp = ? ORDER BY name",
            (state,),
        ).fetchall()
        return _rows_to_dicts(rows)
    finally:
        conn.close()


def count() -> int:
    conn = connect()
    try:
        return conn.execute("SELECT COUNT(*) FROM compounds").fetchone()[0]
    finally:
        conn.close()


def add_compound(**fields) -> int:
    """Insert a new compound. Returns the new row id."""
    allowed = {
        "name", "formula", "cas_number", "molar_mass", "density",
        "melting_point", "boiling_point", "state_stp", "iupac_name",
        "synonyms", "hazard_class", "description",
    }
    keys = [k for k in fields if k in allowed]
    if not keys:
        raise ValueError("No valid fields provided.")

    conn = connect()
    try:
        placeholders = ", ".join("?" for _ in keys)
        cols = ", ".join(keys)
        cur = conn.execute(
            f"INSERT INTO compounds ({cols}) VALUES ({placeholders})",
            [fields[k] for k in keys],
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
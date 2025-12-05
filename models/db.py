"""Database connection and initialization."""

import sqlite3
from pathlib import Path
from config import DATABASE_PATH


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database from schema.sql."""
    schema_path = Path(__file__).parent.parent / "schema.sql"
    
    with open(schema_path) as f:
        schema = f.read()
    
    conn = get_db()
    conn.executescript(schema)
    conn.commit()
    conn.close()


def query_db(query: str, args: tuple = (), one: bool = False):
    """Execute a query and return results."""
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query: str, args: tuple = ()) -> int:
    """Execute a write query and return lastrowid."""
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    lastrowid = cur.lastrowid
    conn.close()
    return lastrowid


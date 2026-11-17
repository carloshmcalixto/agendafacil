"""Camada de acesso ao banco de dados (SQLite)."""
import sqlite3
from pathlib import Path

from flask import current_app, g

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA = BASE_DIR / "database" / "schema.sql"
SEED = BASE_DIR / "database" / "seed.sql"


def get_db() -> sqlite3.Connection:
    """Retorna a conexão da requisição atual (abre uma se ainda não existir)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(seed: bool = False):
    """Cria as tabelas (e opcionalmente insere dados de demonstração)."""
    db = get_db()
    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    if seed:
        total = db.execute("SELECT COUNT(*) FROM servico").fetchone()[0]
        if total == 0:
            db.executescript(SEED.read_text(encoding="utf-8"))
    db.commit()

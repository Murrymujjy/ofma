import sqlite3
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "ofma.sqlite3")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(app=None):
    os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
    conn = get_db()
    with open(os.path.join(BASE_DIR, "schema.sql"), "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def now_iso():
    return datetime.now(timezone.utc).isoformat()

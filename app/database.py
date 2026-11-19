
import sqlite3
from contextlib import closing
from pathlib import Path

from app.models import SecurityEvent


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "kubeguard.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    source TEXT NOT NULL,
                    description TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)


def save_event(event: SecurityEvent):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("""
                INSERT INTO security_events
                (id, event_type, severity, source, description, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event.id,
                event.event_type,
                event.severity,
                event.source,
                event.description,
                event.timestamp
            ))


def get_events():
    with closing(get_connection()) as conn:
        rows = conn.execute("""
            SELECT id, event_type, severity,
                   source, description, timestamp
            FROM security_events
            ORDER BY timestamp DESC
        """).fetchall()

    return [SecurityEvent(**dict(row)) for row in rows]

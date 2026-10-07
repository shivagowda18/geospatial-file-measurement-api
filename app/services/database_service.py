import json
import sqlite3
from pathlib import Path


DATABASE_PATH = Path("uploads") / "files.db"


def get_connection():
    """Create a connection to the SQLite database."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the files table if it does not already exist."""

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            feature_count INTEGER NOT NULL,
            crs TEXT,
            status TEXT NOT NULL,
            features TEXT NOT NULL,
            measurements TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_file_record(record: dict) -> None:
    """Save a processed file record."""

    connection = get_connection()

    connection.execute(
        """
        INSERT OR REPLACE INTO files (
            id,
            filename,
            feature_count,
            crs,
            status,
            features,
            measurements
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["id"],
            record["filename"],
            record["feature_count"],
            record["crs"],
            record["status"],
            json.dumps(record["features"]),
            json.dumps(record["measurements"]),
        ),
    )

    connection.commit()
    connection.close()


def get_file_record(file_id: str) -> dict | None:
    """Retrieve a file record by ID."""

    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM files
        WHERE id = ?
        """,
        (file_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "filename": row["filename"],
        "feature_count": row["feature_count"],
        "crs": row["crs"],
        "status": row["status"],
        "features": json.loads(row["features"]),
        "measurements": json.loads(row["measurements"]),
    }
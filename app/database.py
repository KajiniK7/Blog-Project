import logging
import os
import sqlite3
import time
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

logger = logging.getLogger("app.database")

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)

TURSO_URL = os.getenv("TURSO_DATABASE_URL", "").strip()
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "").strip()

Base = declarative_base()

if TURSO_URL and TURSO_TOKEN:
    import libsql

    class LibSQLCursorAdapter:
        """Cursor wrapper that retries on intermittent network / DNS drops."""
        def __init__(self, raw_cursor):
            self._raw = raw_cursor

        def __getattr__(self, name):
            return getattr(self._raw, name)

        def execute(self, statement, parameters=None):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    if parameters is not None:
                        return self._raw.execute(statement, parameters)
                    return self._raw.execute(statement)
                except Exception as exc:
                    err_msg = str(exc).lower()
                    is_transient = (
                        "hrana" in err_msg
                        or "dns" in err_msg
                        or "11001" in err_msg
                        or "error trying to connect" in err_msg
                        or "connection reset" in err_msg
                        or "broken pipe" in err_msg
                    )
                    if is_transient and attempt < max_retries - 1:
                        logger.warning(
                            "Transient Turso connection error (attempt %d/%d): %s. Retrying...",
                            attempt + 1,
                            max_retries,
                            exc,
                        )
                        time.sleep(0.3 * (attempt + 1))
                        continue
                    raise

        def executemany(self, statement, parameters):
            return self._raw.executemany(statement, parameters)

    class LibSQLDBAPIAdapter:
        """Adapts libsql connection to satisfy standard SQLite DBAPI expectations in SQLAlchemy."""
        def __init__(self, raw_conn):
            self._raw = raw_conn

        def __getattr__(self, name):
            return getattr(self._raw, name)

        def cursor(self):
            return LibSQLCursorAdapter(self._raw.cursor())

        def create_function(self, *args, **kwargs):
            # No-op to satisfy SQLAlchemy SQLite dialect regexp setup
            pass

    # Normalize url scheme for libsql library
    if TURSO_URL.startswith("libsql+https://"):
        connect_url = TURSO_URL.replace("libsql+https://", "libsql://")
    elif TURSO_URL.startswith("https://"):
        connect_url = TURSO_URL.replace("https://", "libsql://")
    else:
        connect_url = TURSO_URL

    def create_libsql_connection():
        # Connect to Turso with retries and graceful fallback to local SQLite if unreachable
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                conn = libsql.connect(database=connect_url, auth_token=TURSO_TOKEN)
                return LibSQLDBAPIAdapter(conn)
            except Exception as exc:
                err_msg = str(exc).lower()
                is_transient = (
                    "dns" in err_msg
                    or "11001" in err_msg
                    or "error trying to connect" in err_msg
                    or "hrana" in err_msg
                )
                if is_transient and attempt < max_attempts - 1:
                    time.sleep(0.3 * (attempt + 1))
                    continue
                logger.warning(
                    "Unable to connect to Turso cloud (%s). Falling back to local SQLite database (posts.db).",
                    exc,
                )
                local_conn = sqlite3.connect("./posts.db", check_same_thread=False)
                return local_conn

    from sqlalchemy.pool import NullPool

    engine = create_engine(
        "sqlite://",
        creator=create_libsql_connection,
        poolclass=NullPool,
    )
else:
    # Local SQLite fallback
    engine = create_engine(
        "sqlite:///./posts.db",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Database session generator dependency for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

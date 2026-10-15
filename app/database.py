import os
from pathlib import Path
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)

TURSO_URL = os.getenv("TURSO_DATABASE_URL", "").strip()
TURSO_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "").strip()

Base = declarative_base()

if TURSO_URL and TURSO_TOKEN:
    import libsql

    class LibSQLDBAPIAdapter:
        """Adapts libsql connection to satisfy standard SQLite DBAPI expectations in SQLAlchemy."""
        def __init__(self, raw_conn):
            self._raw = raw_conn

        def __getattr__(self, name):
            return getattr(self._raw, name)

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
        conn = libsql.connect(database=connect_url, auth_token=TURSO_TOKEN)
        return LibSQLDBAPIAdapter(conn)

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

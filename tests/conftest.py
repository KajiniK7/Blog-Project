import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main_app import app, asgi_app
from app.models import Post

# Use in-memory SQLite with StaticPool so all connections share the same memory instance
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database_schema():
    """Create database tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a fresh, clean database session per test with tables recreated."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session, monkeypatch):
    """Provide a TestClient with get_db overridden to use the isolated test session."""
    from app import crud
    from app.moderation import ModerationResult

    monkeypatch.setattr(
        crud,
        "moderate_with_groq",
        lambda title, content: ModerationResult(approved=True),
    )

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(asgi_app, raise_server_exceptions=False)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def create_draft_post(client):
    """Helper fixture factory function to create a draft post via the API."""
    def _create(
        title: str = "Standard Test Title",
        content: str = "This is a clean, standard draft body created by the helper fixture.",
    ) -> dict:
        response = client.post("/posts/", json={"title": title, "content": content})
        assert response.status_code == 201, f"Failed to create draft: {response.text}"
        return response.json()

    return _create


@pytest.fixture
def draft_post(create_draft_post):
    """Helper fixture that yields an already created draft post dictionary."""
    return create_draft_post()

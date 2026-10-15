import sqlite3
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.database import Base
from app.models import Post


def test_post_model_crud_and_defaults(db_session):
    """Verify Post model creation with default status 'draft'."""
    post = Post(title="Initial Title", content="Sample content body here")
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)

    assert post.id is not None
    assert post.status == "draft"
    assert post.flagged_reasons is None
    assert post.created_at is not None


def test_post_status_check_constraint_valid(db_session):
    """Verify all 4 statuses ('draft', 'flagged', 'approved', 'published') are valid."""
    statuses = ["draft", "flagged", "approved", "published"]
    for idx, st in enumerate(statuses, start=1):
        p = Post(title=f"Title {idx}", content=f"Content {idx}", status=st)
        db_session.add(p)
    db_session.commit()


def test_post_status_check_constraint_invalid(db_session):
    """Verify CHECK constraint rejects invalid status."""
    invalid_post = Post(title="Bad Post", content="Bad content", status="rejected")
    db_session.add(invalid_post)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_seed_data_can_be_executed(db_session):
    """Verify seed_data.sql statements succeed."""
    with open("seed_data.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Raw connection execution
    connection = db_session.connection().connection
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()

    posts = db_session.query(Post).all()
    assert len(posts) == 8
    statuses = {p.status for p in posts}
    assert statuses == {"draft", "flagged", "approved", "published"}
